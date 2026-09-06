# Catalogue des API

Site du catalogue des API d'une administration, construit avec **MkDocs** et le
thème **mkdocs-dsfr 0.26.1** (système de design de l'État).

Chaque API est décrite par un fichier Markdown ; tout le reste — tuiles,
compteurs, filtres, badges, export JSON — est calculé à partir de ces fichiers
au moment de la construction du site.

## Démarrer

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

mkdocs serve      # http://127.0.0.1:8000
mkdocs build      # génère le dossier site/
```

Le site est entièrement statique : le dossier `site/` se dépose sur n'importe
quel serveur web ou sur un hébergement de pages.

## Organisation

```
mkdocs.yml                      Configuration : thème, en-tête, pied de page, navigation
hooks/catalogue.py              Génère catalogue, compteurs, filtres, feuille de route, blocs Redoc
docs/
  index.md                      Page du catalogue (tuiles + filtres à gauche)
  feuille-de-route.md           Feuille de route des nouvelles API
  publier-une-api.md            Mode d'emploi pour les producteurs
  accessibilite.md              Déclaration d'accessibilité RGAA
  mentions-legales.md           Mentions légales et licence
  donnees-personnelles.md       Traitements, cookies, droits
  apis/*.md                     Une fiche par API (en-tête YAML + contenu)
  data/feuille-de-route.yml     Source unique de la feuille de route
  assets/
    openapi/*.yaml              Spécifications hébergées par le catalogue
    javascripts/catalogue.js    Filtrage des tuiles
    javascripts/redoc-loader.js Chargement de Redoc à la demande
    javascripts/vendor/         Bundle Redoc servi localement (fonctionne hors ligne)
    stylesheets/catalogue.css   Surcouche du DSFR, sans couleur en dur
```

## Ajouter une API

1. Créer `docs/apis/mon-api.md` avec l'en-tête YAML documenté dans
   [Publier une API](docs/publier-une-api.md).
2. Déposer la spécification dans `docs/assets/openapi/`, ou renseigner
   `openapi_url` si elle est publiée par le producteur.
3. Ajouter la page à la section `nav` de `mkdocs.yml`.

Les compteurs, la tuile, les filtres et l'export JSON se mettent à jour seuls.

## Ce que fait le hook

`hooks/catalogue.py` lit l'en-tête YAML de chaque fiche de `docs/apis/`, puis
remplace des jetons dans le Markdown :

| Jeton | Effet |
| --- | --- |
| `[[COMPTEURS]]` | Nombre d'API publiées, ouvertes, sur habilitation, détaillé par modalité |
| `[[CATALOGUE]]` | Colonne de filtres à gauche et grille de tuiles à droite |
| `[[FEUILLE_DE_ROUTE]]`, `[[FEUILLE_DE_ROUTE_EXTRAIT]]` | Tableau des jalons |
| `[[FICHE_ENTETE]]` | Badges et métadonnées d'une fiche |
| `[[REDOC]]` | Bloc de documentation OpenAPI |

Les jetons situés dans un bloc de code ne sont pas substitués : la page
« Publier une API » peut donc les montrer en exemple.

Après la construction, le hook publie `site/catalogue.json` : métadonnées de
chaque API, compteurs et feuille de route, pour alimenter un portail tiers sans
recopie manuelle.

## Contrôles avant publication

```bash
mkdocs build --strict          # échoue au moindre avertissement
python3 -c "import yaml,glob; [yaml.safe_load(open(f)) for f in glob.glob('docs/assets/openapi/*.yaml')]"
```

Vérifier aussi qu'aucune fiche ne signale de modalité d'accès inconnue : le hook
émet un avertissement et classe alors l'API comme ouverte, ce qui fausserait les
compteurs.

## Choix techniques

**Le Markdown est la source de vérité.** Aucune base de données, aucun fichier
de configuration parallèle listant les API : une fiche supprimée disparaît
partout, une modalité d'accès modifiée se répercute sur les compteurs.

**Redoc est servi localement.** Le bundle (environ 900 ko) est versionné dans
`docs/assets/javascripts/vendor/`, avec repli sur le CDN. Le site fonctionne donc
sur un réseau fermé. Le rendu n'est déclenché que par un bouton explicite.

**Le filtrage fonctionne sans réseau et dégrade proprement.** Les métadonnées
sont portées par les tuiles en attributs `data-*`. Sans JavaScript, toutes les
API restent affichées et consultables.

**Aucune couleur n'est écrite en dur.** La surcouche CSS n'utilise que les
variables du DSFR, pour que les thèmes clair et sombre restent corrects.

## Adapter à votre administration

À reprendre avant mise en ligne : `site_name`, `site_url`, `repo_url` et les
blocs `theme.header` et `theme.footer` dans `mkdocs.yml` ; les adresses en
`exemple.gouv.fr` dans les fiches et les pages transverses ; la déclaration
d'accessibilité, qui doit refléter un audit réel ; les mentions légales.

Le bloc-marque « République française » du DSFR est réservé aux sites de l'État
et de ses opérateurs. Un opérateur ajoute son logo par `theme.header.logo_url`.
