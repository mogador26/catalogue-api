"""
Hook MkDocs du catalogue des API.

Le hook lit l'en-tête YAML (front matter) de chaque fiche située dans
``docs/apis/`` et génère automatiquement, au format DSFR :

* les tuiles du catalogue (page d'accueil) ;
* le panneau de thèmes et de filtres affiché en colonne de gauche ;
* les compteurs d'API ouvertes / soumises à authentification ;
* la feuille de route des nouvelles API ;
* l'en-tête et le conteneur Redoc de chaque fiche API ;
* un export ``catalogue.json`` publié à la racine du site.

Aucune donnée n'est saisie deux fois : les fiches Markdown sont la source
de vérité, le catalogue en est la projection.
"""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Any

import yaml

log = logging.getLogger("mkdocs.hooks.catalogue")

# ---------------------------------------------------------------------------
# Référentiels de valeurs
# ---------------------------------------------------------------------------

#: Modalités d'accès reconnues. ``ouverte`` est la seule modalité sans
#: authentification : les compteurs du catalogue en découlent.
MODALITES = {
    "ouverte": {
        "libelle": "API ouverte",
        "court": "Ouverte",
        "badge": "fr-badge--success",
        "authentification": False,
        "description": "Accès libre, sans inscription ni jeton.",
    },
    "api-key": {
        "libelle": "Clé d'API",
        "court": "Clé d'API",
        "badge": "fr-badge--info",
        "authentification": True,
        "description": "Accès sur habilitation, jeton statique transmis en en-tête.",
    },
    "oauth2": {
        "libelle": "OAuth 2.0",
        "court": "OAuth 2.0",
        "badge": "fr-badge--info",
        "authentification": True,
        "description": "Accès sur habilitation, jeton d'accès à durée de vie limitée.",
    },
    "mtls": {
        "libelle": "mTLS",
        "court": "mTLS",
        "badge": "fr-badge--warning",
        "authentification": True,
        "description": "Accès sur habilitation, authentification mutuelle par certificat.",
    },
}

#: Cycle de vie du produit.
STATUTS = {
    "production": {"libelle": "En production", "badge": "fr-badge--success"},
    "beta": {"libelle": "Bêta", "badge": "fr-badge--new"},
    "experimentation": {"libelle": "Expérimentation", "badge": "fr-badge--new"},
    "projet": {"libelle": "En construction", "badge": "fr-badge--info"},
    "deprecie": {"libelle": "Dépréciée", "badge": "fr-badge--warning"},
}

#: Icônes DSFR associées aux thèmes, utilisées dans le panneau de filtres.
ICONES_THEME = {
    "Transport": "car-line",
    "Armes": "shield-line",
    "Finances": "money-euro-circle-line",
    "Entreprises et associations": "government-line",
    "Support": "customer-service-2-line",
    "Technique": "terminal-line",
    "Référentiel": "database-2-line",
    "Territoires": "map-pin-2-line",
}

TOKEN = re.compile(r"^\s*\[\[(?P<nom>[A-Z_]+)\]\]\s*$", re.MULTILINE)

FRONT_MATTER = re.compile(r"\A---\s*\n(?P<yaml>.*?)\n---\s*\n", re.DOTALL)

# Renseigné par ``on_files`` puis consommé par ``on_page_markdown``.
_ETAT: dict[str, Any] = {"apis": [], "themes": [], "compteurs": {}, "roadmap": []}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------


def _echapper(valeur: Any) -> str:
    """Échappe une valeur destinée à du contenu HTML."""
    texte = "" if valeur is None else str(valeur)
    return (
        texte.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def _slug(valeur: str) -> str:
    """Transforme un libellé en identifiant utilisable en attribut HTML."""
    table = str.maketrans("àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ", "aaaeeeeiioouuucAAAEEEEIIOOUUUC")
    valeur = valeur.translate(table).lower()
    return re.sub(r"[^a-z0-9]+", "-", valeur).strip("-")


def _prefixe(page) -> str:
    """Chemin relatif de la page courante vers la racine du site."""
    return "../" * page.file.url.count("/")


def _est_url(valeur: str) -> bool:
    return valeur.startswith(("http://", "https://", "//"))


# ---------------------------------------------------------------------------
# Lecture des fiches API
# ---------------------------------------------------------------------------


def _lire_fiches(docs_dir: Path) -> list[dict[str, Any]]:
    """Charge l'en-tête YAML de chaque fiche de ``docs/apis``."""
    fiches: list[dict[str, Any]] = []
    dossier = docs_dir / "apis"
    if not dossier.is_dir():
        log.warning("Catalogue : le dossier %s est introuvable.", dossier)
        return fiches

    for chemin in sorted(dossier.glob("*.md")):
        contenu = chemin.read_text(encoding="utf-8")
        entete = FRONT_MATTER.match(contenu)
        if not entete:
            log.warning("Catalogue : %s n'a pas d'en-tête YAML, fiche ignorée.", chemin.name)
            continue
        try:
            meta = yaml.safe_load(entete.group("yaml")) or {}
        except yaml.YAMLError as erreur:
            log.error("Catalogue : en-tête YAML invalide dans %s (%s).", chemin.name, erreur)
            continue

        acces = str(meta.get("acces", "ouverte")).lower()
        if acces not in MODALITES:
            log.warning(
                "Catalogue : modalité d'accès inconnue « %s » dans %s, valeur « ouverte » retenue.",
                acces,
                chemin.name,
            )
            acces = "ouverte"

        statut = str(meta.get("statut", "production")).lower()
        if statut not in STATUTS:
            statut = "production"

        fiches.append(
            {
                "identifiant": chemin.stem,
                "titre": meta.get("title") or chemin.stem,
                "resume": meta.get("resume", ""),
                "theme": meta.get("theme", "Non classé"),
                "acces": acces,
                "statut": statut,
                "producteur": meta.get("producteur", ""),
                "contact_nom": meta.get("contact_nom", ""),
                "contact_email": meta.get("contact_email", ""),
                "contact_url": meta.get("contact_url", ""),
                "version": meta.get("version", ""),
                "maj": str(meta.get("maj", "")),
                "openapi": meta.get("openapi", ""),
                "openapi_url": meta.get("openapi_url", ""),
                "base_url": meta.get("base_url", ""),
                "tags": meta.get("tags", []) or [],
                "url": f"apis/{chemin.stem}/",
            }
        )
    return fiches


def _compter(fiches: list[dict[str, Any]]) -> dict[str, Any]:
    """Calcule les compteurs affichés en tête de catalogue."""
    par_modalite = {cle: 0 for cle in MODALITES}
    par_theme: dict[str, int] = {}
    par_statut = {cle: 0 for cle in STATUTS}

    for fiche in fiches:
        par_modalite[fiche["acces"]] += 1
        par_statut[fiche["statut"]] += 1
        par_theme[fiche["theme"]] = par_theme.get(fiche["theme"], 0) + 1

    ouvertes = par_modalite["ouverte"]
    return {
        "total": len(fiches),
        "ouvertes": ouvertes,
        "authentifiees": len(fiches) - ouvertes,
        "par_modalite": par_modalite,
        "par_theme": dict(sorted(par_theme.items())),
        "par_statut": par_statut,
    }


# ---------------------------------------------------------------------------
# Fragments HTML DSFR
# ---------------------------------------------------------------------------


def _badges(fiche: dict[str, Any], taille: str = "fr-badge--sm") -> str:
    modalite = MODALITES[fiche["acces"]]
    statut = STATUTS[fiche["statut"]]
    elements = [
        f'<li><p class="fr-badge {taille} fr-badge--no-icon">{_echapper(fiche["theme"])}</p></li>',
        f'<li><p class="fr-badge {taille} {modalite["badge"]}">{_echapper(modalite["court"])}</p></li>',
        f'<li><p class="fr-badge {taille} {statut["badge"]}">{_echapper(statut["libelle"])}</p></li>',
    ]
    return '<ul class="fr-badges-group">' + "".join(elements) + "</ul>"


def _tuile(fiche: dict[str, Any], prefixe: str) -> str:
    """Tuile DSFR représentant une API dans le catalogue."""
    recherche = " ".join(
        [
            fiche["titre"],
            fiche["resume"],
            fiche["theme"],
            fiche["producteur"],
            " ".join(str(tag) for tag in fiche["tags"]),
        ]
    ).lower()

    lien = f'{prefixe}{fiche["url"]}'
    version = (
        f'<p class="fr-tile__detail">Version {_echapper(fiche["version"])}</p>'
        if fiche["version"]
        else ""
    )

    return (
        '<div class="fr-col-12 fr-col-md-6 fr-col-lg-4 catalogue__item"'
        f' data-theme="{_slug(fiche["theme"])}"'
        f' data-acces="{fiche["acces"]}"'
        f' data-authentification="{"oui" if MODALITES[fiche["acces"]]["authentification"] else "non"}"'
        f' data-statut="{fiche["statut"]}"'
        f' data-recherche="{_echapper(recherche)}">'
        '<div class="fr-tile fr-tile--vertical fr-enlarge-link catalogue__tuile">'
        '<div class="fr-tile__body"><div class="fr-tile__content">'
        f'<h3 class="fr-tile__title"><a href="{_echapper(lien)}">{_echapper(fiche["titre"])}</a></h3>'
        f'<p class="fr-tile__desc">{_echapper(fiche["resume"])}</p>'
        f"{version}"
        f'<div class="fr-tile__start">{_badges(fiche)}</div>'
        "</div></div></div></div>"
    )


def _compteurs_html(compteurs: dict[str, Any]) -> str:
    """Bandeau de compteurs, calculé à chaque construction du site."""
    modalites = compteurs["par_modalite"]
    detail = ", ".join(
        f'{modalites[cle]} en {MODALITES[cle]["libelle"]}'
        for cle in ("api-key", "oauth2", "mtls")
        if modalites[cle]
    )
    cartes = [
        ("total", "API publiées", compteurs["total"], "Toutes modalités confondues."),
        ("ouvertes", "API ouvertes", compteurs["ouvertes"], "Sans authentification."),
        (
            "authentifiees",
            "API sur habilitation",
            compteurs["authentifiees"],
            detail or "Aucune API soumise à authentification.",
        ),
    ]
    blocs = "".join(
        '<div class="fr-col-12 fr-col-sm-4">'
        f'<div class="catalogue__compteur" data-compteur="{cle}">'
        f'<p class="catalogue__compteur-valeur">{valeur}</p>'
        f'<p class="catalogue__compteur-libelle">{_echapper(libelle)}</p>'
        f'<p class="catalogue__compteur-detail fr-text--xs">{_echapper(aide)}</p>'
        "</div></div>"
        for cle, libelle, valeur, aide in cartes
    )
    return f'<div class="fr-grid-row fr-grid-row--gutters catalogue__compteurs">{blocs}</div>'


def _case(groupe: str, valeur: str, libelle: str, nombre: int, icone: str = "") -> str:
    identifiant = f"filtre-{groupe}-{_slug(valeur)}"
    pastille = f'<span class="catalogue__pastille">{nombre}</span>'
    prefixe_icone = (
        f'<span class="fr-icon-{icone} fr-icon--sm catalogue__icone" aria-hidden="true"></span>'
        if icone
        else ""
    )
    return (
        '<div class="fr-checkbox-group fr-checkbox-group--sm">'
        f'<input type="checkbox" id="{identifiant}" name="{groupe}" value="{_echapper(valeur)}"'
        f' data-filtre="{groupe}">'
        f'<label class="fr-label" for="{identifiant}">{prefixe_icone}'
        f"{_echapper(libelle)}{pastille}</label>"
        "</div>"
    )


def _filtres_html(compteurs: dict[str, Any]) -> str:
    """Panneau de thèmes et de filtres affiché en colonne de gauche."""
    themes = "".join(
        _case("theme", _slug(theme), theme, nombre, ICONES_THEME.get(theme, "price-tag-3-line"))
        for theme, nombre in compteurs["par_theme"].items()
    )
    modalites = "".join(
        _case("acces", cle, MODALITES[cle]["libelle"], compteurs["par_modalite"][cle])
        for cle in MODALITES
        if compteurs["par_modalite"][cle]
    )
    statuts = "".join(
        _case("statut", cle, STATUTS[cle]["libelle"], compteurs["par_statut"][cle])
        for cle in STATUTS
        if compteurs["par_statut"][cle]
    )

    return (
        '<nav class="catalogue__filtres" id="catalogue-filtres"'
        ' aria-label="Thèmes et filtres du catalogue">'
        '<div class="fr-search-bar fr-search-bar--sm" role="search">'
        '<label class="fr-label" for="catalogue-recherche">Rechercher une API</label>'
        '<input class="fr-input" id="catalogue-recherche" type="search"'
        ' placeholder="Nom, usage, producteur…" autocomplete="off">'
        '<button class="fr-btn" type="button" id="catalogue-recherche-btn">Rechercher</button>'
        "</div>"
        '<fieldset class="fr-fieldset catalogue__groupe">'
        '<legend class="fr-fieldset__legend fr-text--bold">Thèmes</legend>'
        f'<div class="fr-fieldset__content">{themes}</div></fieldset>'
        '<fieldset class="fr-fieldset catalogue__groupe">'
        '<legend class="fr-fieldset__legend fr-text--bold">Modalités d\'accès</legend>'
        f'<div class="fr-fieldset__content">{modalites}</div></fieldset>'
        '<fieldset class="fr-fieldset catalogue__groupe">'
        '<legend class="fr-fieldset__legend fr-text--bold">Cycle de vie</legend>'
        f'<div class="fr-fieldset__content">{statuts}</div></fieldset>'
        '<button class="fr-btn fr-btn--secondary fr-btn--sm fr-icon-refresh-line'
        ' fr-btn--icon-left" type="button" id="catalogue-reinitialiser">'
        "Réinitialiser les filtres</button>"
        "</nav>"
    )


def _catalogue_html(fiches: list[dict[str, Any]], compteurs: dict[str, Any], prefixe: str) -> str:
    """Assemble la colonne de filtres (gauche) et la grille de tuiles (droite)."""
    tuiles = "".join(_tuile(fiche, prefixe) for fiche in fiches)
    return (
        '<div class="fr-grid-row fr-grid-row--gutters catalogue">'
        '<div class="fr-col-12 fr-col-md-4 fr-col-lg-3 catalogue__colonne-filtres">'
        f"{_filtres_html(compteurs)}"
        "</div>"
        '<div class="fr-col-12 fr-col-md-8 fr-col-lg-9">'
        '<div class="catalogue__barre">'
        f'<p class="fr-text--sm catalogue__resultats" id="catalogue-resultats"'
        f' role="status">{len(fiches)} API sur {len(fiches)}</p>'
        '<div class="catalogue__actifs" id="catalogue-actifs"></div>'
        "</div>"
        f'<div class="fr-grid-row fr-grid-row--gutters" id="catalogue-grille">{tuiles}</div>'
        '<div class="fr-callout catalogue__vide" id="catalogue-vide" hidden>'
        '<h3 class="fr-callout__title">Aucune API ne correspond à votre recherche</h3>'
        '<p class="fr-callout__text">Élargissez les filtres, ou consultez la feuille de'
        " route : l'API que vous cherchez est peut-être en cours de construction.</p>"
        "</div></div></div>"
    )


# ---------------------------------------------------------------------------
# Feuille de route
# ---------------------------------------------------------------------------


def _lire_roadmap(docs_dir: Path) -> list[dict[str, Any]]:
    chemin = docs_dir / "data" / "feuille-de-route.yml"
    if not chemin.is_file():
        return []
    donnees = yaml.safe_load(chemin.read_text(encoding="utf-8")) or {}
    return donnees.get("jalons", [])


def _roadmap_html(jalons: list[dict[str, Any]], limite: int | None = None) -> str:
    if not jalons:
        return '<p class="fr-text--sm">La feuille de route n\'est pas encore renseignée.</p>'

    etapes = {
        "livre": ("Livrée", "fr-badge--success"),
        "en-cours": ("En cours", "fr-badge--info"),
        "prevu": ("Prévue", "fr-badge--new"),
        "etude": ("À l'étude", "fr-badge--grey"),
    }

    selection = jalons[:limite] if limite else jalons
    lignes = []
    for jalon in selection:
        etape, badge = etapes.get(str(jalon.get("etape", "prevu")), etapes["prevu"])
        acces = MODALITES.get(str(jalon.get("acces", "ouverte")), MODALITES["ouverte"])
        lignes.append(
            "<tr>"
            f'<td><span class="fr-badge fr-badge--sm fr-badge--no-icon">'
            f'{_echapper(jalon.get("echeance", "—"))}</span></td>'
            f'<th scope="row">{_echapper(jalon.get("api", ""))}'
            f'<span class="fr-hint-text">{_echapper(jalon.get("description", ""))}</span></th>'
            f'<td>{_echapper(jalon.get("theme", "—"))}</td>'
            f'<td>{_echapper(acces["court"])}</td>'
            f'<td><p class="fr-badge fr-badge--sm {badge}">{etape}</p></td>'
            "</tr>"
        )

    return (
        '<div class="fr-table fr-table--bordered" id="feuille-de-route">'
        '<div class="fr-table__wrapper"><div class="fr-table__container">'
        '<div class="fr-table__content"><table>'
        "<caption>Nouvelles API et évolutions majeures programmées</caption>"
        "<thead><tr><th scope=\"col\">Échéance</th><th scope=\"col\">API</th>"
        '<th scope="col">Thème</th><th scope="col">Accès prévu</th>'
        '<th scope="col">Avancement</th></tr></thead>'
        f"<tbody>{''.join(lignes)}</tbody>"
        "</table></div></div></div></div>"
    )


# ---------------------------------------------------------------------------
# Fiche API : en-tête et documentation Redoc
# ---------------------------------------------------------------------------


def _fiche_par_identifiant(identifiant: str) -> dict[str, Any] | None:
    for fiche in _ETAT["apis"]:
        if fiche["identifiant"] == identifiant:
            return fiche
    return None


MOIS = (
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre",
)


def _date_fr(valeur: str) -> str:
    """Transforme une date ISO en date lisible (« 28 août 2026 »)."""
    correspondance = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", valeur.strip())
    if not correspondance:
        return valeur
    annee, mois, jour = (int(part) for part in correspondance.groups())
    return f"{'1er' if jour == 1 else jour} {MOIS[mois - 1]} {annee}"


def _entete_fiche(fiche: dict[str, Any]) -> str:
    modalite = MODALITES[fiche["acces"]]
    contact = fiche["contact_email"]
    lien_contact = (
        f'<a class="fr-link" href="mailto:{_echapper(contact)}">{_echapper(contact)}</a>'
        if contact
        else "Non renseigné"
    )
    lignes = [
        ("Producteur", _echapper(fiche["producteur"]) or "—"),
        ("Contact", lien_contact),
        ("Modalité d'accès", f'{_echapper(modalite["libelle"])} — {_echapper(modalite["description"])}'),
        ("Version courante", _echapper(fiche["version"]) or "—"),
        ("Dernière mise à jour", _echapper(_date_fr(fiche["maj"])) or "—"),
    ]
    if fiche["base_url"]:
        lignes.insert(3, ("URL de base", f'<code>{_echapper(fiche["base_url"])}</code>'))

    corps = "".join(
        f'<div class="fiche__ligne"><dt>{cle}</dt><dd>{valeur}</dd></div>' for cle, valeur in lignes
    )
    return (
        f'<div class="fiche__entete">{_badges(fiche, "fr-badge--sm")}'
        f'<dl class="fiche__meta">{corps}</dl></div>'
    )


def _redoc_html(fiche: dict[str, Any], prefixe: str, version_redoc: str) -> str:
    """Bloc de documentation Redoc.

    Deux sources sont acceptées et peuvent coexister : un fichier de
    spécification hébergé par ce site (``openapi``) et l'URL publiée par le
    producteur (``openapi_url``). Le bundle Redoc est servi localement, avec
    repli sur le CDN si le fichier n'a pas été déposé.
    """
    locale = str(fiche["openapi"] or "")
    distante = str(fiche["openapi_url"] or "")

    if not locale and not distante:
        return (
            '<div class="fr-alert fr-alert--info"><h3 class="fr-alert__title">'
            "Documentation OpenAPI à venir</h3>"
            "<p>La spécification de cette API n'est pas encore publiée. Elle le sera"
            " avant la première mise à disposition d'un environnement de test.</p></div>"
        )

    sources: list[tuple[str, str, str]] = []
    if locale:
        url = locale if _est_url(locale) else f"{prefixe}{locale.lstrip('/')}"
        sources.append(("site", "Copie hébergée par le catalogue", url))
    if distante:
        sources.append(("producteur", "Spécification publiée par le producteur", distante))

    identifiant = _slug(fiche["identifiant"])
    bundle_local = f"{prefixe}assets/javascripts/vendor/redoc.standalone.js"
    bundle_cdn = f"https://cdn.redoc.ly/redoc/v{version_redoc}/bundles/redoc.standalone.js"
    defaut = sources[0]

    selecteur = ""
    if len(sources) > 1:
        boutons = "".join(
            '<div class="fr-radio-group fr-radio-group--sm">'
            f'<input type="radio" name="redoc-source-{identifiant}"'
            f' id="redoc-source-{identifiant}-{cle}" value="{_echapper(url)}"'
            f'{" checked" if cle == defaut[0] else ""} data-redoc-source>'
            f'<label class="fr-label" for="redoc-source-{identifiant}-{cle}">'
            f"{_echapper(libelle)}</label></div>"
            for cle, libelle, url in sources
        )
        selecteur = (
            '<fieldset class="fr-fieldset redoc__sources">'
            '<legend class="fr-fieldset__legend fr-text--sm fr-text--bold">'
            "Source de la spécification</legend>"
            f'<div class="fr-fieldset__content">{boutons}</div></fieldset>'
        )

    liens = "".join(
        f'<li><a class="fr-btn fr-btn--tertiary fr-btn--sm fr-icon-download-line"'
        f' href="{_echapper(url)}" download>{_echapper(libelle)}</a></li>'
        for _cle, libelle, url in sources
    )

    return (
        f'<div class="redoc" id="redoc-{identifiant}"'
        f' data-redoc-spec="{_echapper(defaut[2])}"'
        f' data-redoc-bundle="{_echapper(bundle_local)}"'
        f' data-redoc-cdn="{_echapper(bundle_cdn)}">'
        f"{selecteur}"
        '<ul class="fr-btns-group fr-btns-group--inline fr-btns-group--sm'
        f' fr-btns-group--icon-left">{liens}'
        '<li><button type="button" class="fr-btn fr-btn--sm fr-icon-book-2-line"'
        " data-redoc-afficher>Afficher la documentation interactive</button></li></ul>"
        '<p class="fr-hint-text">Documentation rendue par Redoc, exécuté dans votre'
        " navigateur : la spécification n'est envoyée à aucun service tiers.</p>"
        '<div class="redoc__conteneur" data-redoc-cible><noscript>'
        '<p class="fr-alert fr-alert--info fr-alert--sm">L\'affichage interactif de la'
        " documentation nécessite JavaScript. La spécification reste téléchargeable"
        " ci-dessus et lisible dans n'importe quel outil compatible OpenAPI.</p>"
        "</noscript></div>"
        "</div>"
    )


# ---------------------------------------------------------------------------
# Points d'entrée MkDocs
# ---------------------------------------------------------------------------


def on_files(files, config):  # noqa: D103 - signature imposée par MkDocs
    docs_dir = Path(config["docs_dir"])
    fiches = _lire_fiches(docs_dir)
    _ETAT["apis"] = fiches
    _ETAT["compteurs"] = _compter(fiches)
    _ETAT["roadmap"] = _lire_roadmap(docs_dir)
    log.info(
        "Catalogue : %s API indexées (%s ouvertes, %s sur habilitation).",
        _ETAT["compteurs"]["total"],
        _ETAT["compteurs"]["ouvertes"],
        _ETAT["compteurs"]["authentifiees"],
    )
    return files


#: Blocs de code délimités par des accents graves. Les jetons qui s'y trouvent
#: sont des exemples de documentation : ils ne doivent pas être substitués.
BLOC_CODE = re.compile(r"^(?P<cloture>`{3,}).*?^(?P=cloture)\s*$", re.DOTALL | re.MULTILINE)


def on_page_markdown(markdown, page, config, files):  # noqa: D103
    prefixe = _prefixe(page)
    version_redoc = str(config.get("extra", {}).get("redoc_version", "2.5.0"))
    fiche = _fiche_par_identifiant(Path(page.file.src_uri).stem)

    def remplacer(correspondance: re.Match) -> str:
        nom = correspondance.group("nom")
        if nom == "CATALOGUE":
            return _catalogue_html(_ETAT["apis"], _ETAT["compteurs"], prefixe)
        if nom == "COMPTEURS":
            return _compteurs_html(_ETAT["compteurs"])
        if nom == "FEUILLE_DE_ROUTE":
            return _roadmap_html(_ETAT["roadmap"])
        if nom == "FEUILLE_DE_ROUTE_EXTRAIT":
            return _roadmap_html(_ETAT["roadmap"], limite=4)
        if nom == "FICHE_ENTETE" and fiche:
            return _entete_fiche(fiche)
        if nom == "REDOC" and fiche:
            return _redoc_html(fiche, prefixe, version_redoc)
        log.warning("Catalogue : jeton [[%s]] non résolu dans %s.", nom, page.file.src_uri)
        return ""

    # Le contenu est traité par segments : les blocs de code sont recopiés tels
    # quels, le reste est soumis à la substitution des jetons.
    sortie: list[str] = []
    position = 0
    for bloc in BLOC_CODE.finditer(markdown):
        sortie.append(TOKEN.sub(remplacer, markdown[position : bloc.start()]))
        sortie.append(bloc.group(0))
        position = bloc.end()
    sortie.append(TOKEN.sub(remplacer, markdown[position:]))
    return "".join(sortie)


def on_post_build(config):  # noqa: D103
    """Publie le catalogue au format JSON pour les réutilisateurs."""
    export = {
        "genere_le": None,
        "compteurs": _ETAT["compteurs"],
        "apis": _ETAT["apis"],
        "feuille_de_route": _ETAT["roadmap"],
    }
    from datetime import date

    export["genere_le"] = date.today().isoformat()
    cible = Path(config["site_dir"]) / "catalogue.json"
    cible.write_text(
        json.dumps(export, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    log.info("Catalogue : export JSON écrit dans %s.", cible)
