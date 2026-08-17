# agent.md — Catalogue d'API d'administration (mkdocs-dsfr)

Ce fichier décrit le projet à un agent (humain ou IA) chargé de générer et maintenir
un site statique de catalogue d'API pour une administration, basé sur **MkDocs** et
le thème **mkdocs-dsfr** (version `0.26.0`).

Objectif : produire un site conforme au DSFR (Système de Design de l'État), listant
les API exposées par l'administration, avec fiche fonctionnelle, cas d'usage,
documentation technique (Swagger/Redoc), mode d'accès et thème métier — et rendre
l'ajout d'une nouvelle API aussi simple qu'un `git add` + remplissage d'un template.

---

## 1. Stack technique

| Composant | Détail |
|---|---|
| Générateur | [MkDocs](https://www.mkdocs.org/) `>=1.6.1` |
| Thème | [mkdocs-dsfr](https://pypi.org/project/mkdocs-dsfr/) `==0.26.0` |
| Doc technique API | Swagger UI / Redoc (embarqués en HTML statique, un fichier OpenAPI par API) |
| Langue | `fr` |
| Hébergement | Pages statiques (GitLab Pages / GitHub Pages) via CI |

### 1.1 Dépendances (`requirements.txt`)

```txt
mkdocs==1.6.1
mkdocs-dsfr==0.26.0
mkdocs-macros-plugin>=1.0
mkdocs-awesome-pages-plugin>=2.9
pyyaml>=6.0
```

- `mkdocs-macros-plugin` : génère automatiquement les pages d'index/catalogue
  (listing, filtres par thème et par mode d'accès) à partir des métadonnées de
  chaque fiche API.
- `mkdocs-awesome-pages-plugin` : gère l'ordre et le regroupement des pages de
  navigation sans avoir à toucher `mkdocs.yml` à chaque ajout d'API.

### 1.2 Installation

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## 2. Arborescence du dépôt

```
.
├── agent.md
├── mkdocs.yml
├── requirements.txt
├── docs/
│   ├── index.md                     # Page d'accueil du catalogue
│   ├── themes/
│   │   └── index.md                 # Vue par thème (auto-générée)
│   ├── apis/
│   │   ├── index.md                 # Catalogue complet (auto-généré, macro)
│   │   ├── _template/                # Gabarit pour créer une nouvelle API
│   │   │   ├── index.md
│   │   │   ├── cas-usage.md
│   │   │   ├── technique.md
│   │   │   └── openapi.yaml
│   │   ├── annuaire-entreprises/
│   │   │   ├── index.md              # Fiche fonctionnelle + métadonnées
│   │   │   ├── cas-usage.md          # Cas d'usage détaillé
│   │   │   ├── technique.md          # Page embarquant Swagger/Redoc
│   │   │   └── openapi.yaml          # Spécification OpenAPI de l'API
│   │   └── ... (une fiche par API)
│   ├── assets/
│   │   └── redoc/redoc.standalone.js # Redoc en local (pas de CDN obligatoire)
│   └── stylesheets/extra.css
├── scripts/
│   └── new_api.py                    # Scaffolding d'une nouvelle fiche API
└── .gitlab-ci.yml / .github/workflows/deploy.yml
```

---

## 3. Modèle de données d'une API

Chaque API est représentée par un dossier sous `docs/apis/<slug-api>/` contenant un
`index.md` avec un **front matter YAML** normalisé. Ce front matter est la source de
vérité utilisée par les macros pour générer le catalogue, les filtres par thème et
par mode d'accès.

```yaml
---
title: "Annuaire des Entreprises"
slug: annuaire-entreprises
description_courte: >
  Recherche et consultation des informations légales des entreprises françaises.
theme: entreprise            # cf. §3.1 liste des thèmes autorisés
acces: public                 # public | contrat
version: "1.2.0"
producteur: "Direction Interministérielle du Numérique"
contact: api-annuaire@exemple.gouv.fr
lien_swagger: technique.md
lien_openapi: openapi.yaml
statut: production            # beta | production | deprecie
date_maj: 2026-08-17
tags: [entreprises, siren, données ouvertes]
---
```

### 3.1 Thèmes autorisés

Liste fermée, à faire évoluer dans `scripts/new_api.py` (variable `THEMES`) si besoin :

- `service-socle`
- `entreprise`
- `association`
- `transport`
- `education`
- `sante`
- `justice`
- `emploi`
- `logement`
- `environnement`

### 3.2 Mode d'accès

- `public` : accès libre, sans authentification préalable (clé API éventuelle en
  libre-service).
- `contrat` : accès conditionné à une convention/habilitation (ex. France Connect,
  API Particulier, API Entreprise sous convention).

---

## 4. Contenu attendu d'une fiche API

Chaque fiche API doit comporter **4 pages** dans son dossier :

1. **`index.md`** — Fiche fonctionnelle
   - Front matter (§3)
   - Description fonctionnelle : à quoi sert l'API, quelles données elle expose
   - Périmètre et limites (ce que l'API ne fait pas)
   - Badges visuels : thème + mode d'accès (générés automatiquement par macro,
     ne pas les écrire à la main)
   - Liens vers `cas-usage.md` et `technique.md`

2. **`cas-usage.md`** — Cas d'usage
   - Contexte métier concret (qui l'utilise, pourquoi)
   - Scénario pas à pas (appel(s) type, enchaînement)
   - Exemple de requête/réponse minimal (extrait, pas le contrat complet)

3. **`technique.md`** — Documentation technique
   - Embarque **Swagger UI** ou **Redoc** pointant sur `openapi.yaml` du même
     dossier (voir §5)
   - Informations d'environnement : URL de base (prod/bac à sable), format
     d'authentification, quotas/rate-limiting

4. **`openapi.yaml`** — Spécification OpenAPI 3.x de l'API (fournie par l'équipe
   produit de l'API, ou générée depuis leur outillage). C'est le fichier que
   Swagger/Redoc consomment.

---

## 5. Intégration Swagger / Redoc

mkdocs-dsfr n'embarque pas nativement un rendu OpenAPI. On génère donc une page
HTML légère par API, à partir d'un template Jinja injecté par
`mkdocs-macros-plugin`.

### 5.1 Template Redoc (recommandé, lecture seule)

Dans `technique.md` :

```markdown
---
title: Documentation technique
---

# Documentation technique

{{ redoc("openapi.yaml") }}
```

La macro `redoc(path)` (définie dans `main.py` à la racine, chargé par
`mkdocs-macros-plugin`) injecte :

```html
<redoc spec-url="{{ path }}"></redoc>
<script src="/assets/redoc/redoc.standalone.js"></script>
```

### 5.2 Alternative Swagger UI (si tests interactifs "Try it out" requis)

```markdown
{{ swagger_ui("openapi.yaml") }}
```

qui injecte un conteneur `<div id="swagger-ui">` + initialisation JS pointant vers
le fichier `openapi.yaml` local.

> Règle : ne jamais dupliquer le contrat d'API dans le Markdown. La page technique
> ne fait qu'embarquer le rendu du fichier `openapi.yaml`, qui reste la seule
> source de vérité.

---

## 6. Génération automatique du catalogue

`docs/apis/index.md` et `docs/themes/index.md` ne sont **jamais édités à la main**.
Ils utilisent une macro qui parcourt `docs/apis/*/index.md`, lit le front matter de
chaque fiche, et génère :

- un tableau/liste de toutes les API (nom, thème, mode d'accès, statut, lien)
- une vue groupée par thème
- une vue filtrée par mode d'accès (`public` / `contrat`)

```markdown
# Catalogue des API

{{ catalogue_apis() }}
```

La macro `catalogue_apis()` doit :
1. Lister les sous-dossiers de `docs/apis/` (en excluant `_template`)
2. Charger le front matter de chaque `index.md`
3. Trier par `theme` puis `title`
4. Rendre une carte DSFR (`fr-card`) par API avec badges thème/accès et lien vers
   la fiche

---

## 7. Ajouter une nouvelle API (workflow)

L'objectif : qu'ajouter une API tienne en **une commande + remplissage d'un
front matter**, sans toucher `mkdocs.yml` ni au code des macros.

### 7.1 Étapes pour un contributeur

```bash
# 1. Scaffolding depuis le template
python scripts/new_api.py --slug mon-api --titre "Mon API" --theme transport --acces public

# 2. Compléter les fichiers générés
#    docs/apis/mon-api/index.md       -> description fonctionnelle + front matter
#    docs/apis/mon-api/cas-usage.md   -> cas d'usage
#    docs/apis/mon-api/technique.md   -> déjà pré-rempli (macro redoc/swagger)
#    docs/apis/mon-api/openapi.yaml   -> remplacer par la vraie spec

# 3. Prévisualiser en local
mkdocs serve

# 4. Committer et pousser
git add docs/apis/mon-api
git commit -m "Ajout API: Mon API"
git push origin ma-branche
# -> ouvrir une Merge/Pull Request
```

Aucune autre modification n'est nécessaire : le catalogue, la vue par thème et
la navigation se régénèrent automatiquement au build suivant grâce à
`mkdocs-awesome-pages-plugin` et aux macros.

### 7.2 `scripts/new_api.py` — comportement attendu

Le script doit :
1. Vérifier que `--theme` fait partie de la liste `THEMES` (§3.1) et que
   `--acces` vaut `public` ou `contrat`
2. Vérifier que le slug n'existe pas déjà sous `docs/apis/`
3. Copier `docs/apis/_template/` vers `docs/apis/<slug>/`
4. Pré-remplir le front matter de `index.md` avec les valeurs passées en argument
   et `date_maj` = date du jour
5. Afficher un résumé des fichiers créés et des champs restant à compléter

### 7.3 Validation automatique (CI)

Avant merge, la CI doit exécuter un contrôle qui, pour chaque dossier sous
`docs/apis/` (hors `_template`) :

- vérifie la présence des 4 fichiers attendus (§4)
- valide le front matter (`theme` dans la liste autorisée, `acces` ∈
  `{public, contrat}`, champs obligatoires présents)
- valide que `openapi.yaml` est un document OpenAPI syntaxiquement correct
  (ex. `openapi-spec-validator`)
- exécute `mkdocs build --strict` pour s'assurer qu'aucun lien n'est cassé

---

## 8. `mkdocs.yml` de référence

```yaml
site_name: Catalogue des API — [Nom de l'administration]
site_description: Catalogue des API exposées par [administration]
site_url: https://exemple.gouv.fr/catalogue-api/
repo_url: https://github.com/exemple-administration/catalogue-api
repo_name: catalogue-api
docs_dir: docs
site_dir: public

theme:
  name: dsfr
  locale: fr
  logo_title: Catalogue<br>des API
  header:
    service_title: Catalogue des API

plugins:
  - search
  - macros:
      module_name: main
  - awesome-pages

markdown_extensions:
  - admonition
  - tables
  - toc:
      permalink: true
  - attr_list
  - md_in_html

extra_css:
  - stylesheets/extra.css

nav:
  - Accueil: index.md
  - Catalogue: apis/index.md
  - Par thème: themes/index.md
```

---

## 9. Intégration continue et déploiement

`.gitlab-ci.yml` (ou équivalent GitHub Actions) doit :

1. Installer les dépendances (`pip install -r requirements.txt`)
2. Lancer la validation des fiches API (§7.3)
3. Construire le site : `mkdocs build --strict`
4. Publier `public/` sur Pages (branche/artefact selon la plateforme)

Déclencheurs : à chaque push sur la branche principale, et en pipeline de
vérification sur chaque Merge/Pull Request touchant `docs/apis/`.

---

## 10. Checklist de revue pour une nouvelle API (Merge Request)

- [ ] Front matter complet et conforme au schéma §3
- [ ] `theme` dans la liste autorisée
- [ ] `acces` = `public` ou `contrat`, cohérent avec la réalité de l'API
- [ ] Description fonctionnelle claire, sans jargon technique excessif
- [ ] Au moins un cas d'usage concret décrit
- [ ] `openapi.yaml` valide et à jour
- [ ] Page technique affiche correctement Swagger/Redoc en `mkdocs serve`
- [ ] `mkdocs build --strict` passe sans erreur ni warning

---

## 11. Tâches restant à réaliser par l'agent

Lorsqu'un agent (humain ou IA) reprend ce fichier pour initialiser le projet,
il doit, dans l'ordre :

1. Créer l'arborescence du §2
2. Écrire `mkdocs.yml` (§8) et `requirements.txt` (§1.1)
3. Écrire les macros Python (`main.py`) : `catalogue_apis()`, `redoc()`,
   `swagger_ui()`
4. Créer `docs/apis/_template/` avec les 4 fichiers types et un front matter
   à trous
5. Écrire `scripts/new_api.py` (§7.2)
6. Écrire le script/étape de validation CI (§7.3)
7. Écrire les pipelines CI/CD (§9)
8. Créer 1 à 2 fiches API d'exemple pour valider le rendu de bout en bout
   (`mkdocs serve` puis `mkdocs build --strict`)
