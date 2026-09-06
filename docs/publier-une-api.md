---
title: Publier une API
description: Comment ajouter ou mettre à jour une fiche dans le catalogue.
---

# Publier une API dans le catalogue

Le catalogue est alimenté par les producteurs eux-mêmes. Une fiche est un
fichier Markdown déposé dans `docs/apis/`, avec un en-tête YAML qui porte les
métadonnées. Tout le reste — tuile, compteurs, filtres, badges, export JSON —
en découle automatiquement : il n'y a rien d'autre à mettre à jour.

## 1. Créer la fiche

Copiez une fiche existante, ou partez de ce gabarit.

```yaml
---
title: Nom de l'API                     # obligatoire
resume: >-                              # obligatoire, deux lignes maximum
  Ce que l'API expose, en une phrase compréhensible par un non-technicien.
theme: Référentiel                      # obligatoire, voir la liste ci-dessous
acces: oauth2                           # ouverte | api-key | oauth2 | mtls
statut: production                      # projet | experimentation | beta | production | deprecie
producteur: Direction, service, équipe
contact_nom: Nom de l'équipe
contact_email: mon-api@exemple.gouv.fr
contact_url: https://…                  # facultatif
version: 1.0.0
maj: 2026-09-01
base_url: https://mon-api.exemple.gouv.fr/api/v1
openapi: assets/openapi/mon-api.yaml    # spécification hébergée par le catalogue
openapi_url: https://…/openapi.yaml     # facultatif : spécification publiée par le producteur
tags: [mot-clé, mot-clé]
---
```

Les valeurs de `theme` sont libres, mais utilisez de préférence un thème
existant : chaque nouveau thème ajoute une ligne au panneau de filtres.
Les thèmes actuels sont Transport, Armes, Finances, Entreprises et
associations, Support, Technique, Référentiel et Territoires.

Une valeur de `acces` inconnue déclenche un avertissement à la construction et
la fiche est classée comme ouverte : vérifiez les journaux de la chaîne
d'intégration en cas de doute.

## 2. Rédiger le contenu

Le plan est imposé, pour que deux fiches restent comparables :

```markdown
# Nom de l'API

[[FICHE_ENTETE]]

## Description fonctionnelle
## Cas d'usage identifiés
## Proposition de valeur
## Modalités d'accès
## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit
## Contact du producteur
```

Trois jetons sont remplacés à la construction du site :

| Jeton | Effet |
| --- | --- |
| `[[FICHE_ENTETE]]` | Badges et tableau des métadonnées, à partir de l'en-tête YAML. |
| `[[REDOC]]` | Bloc de documentation OpenAPI rendu par Redoc. |
| `[[CATALOGUE]]`, `[[COMPTEURS]]`, `[[FEUILLE_DE_ROUTE]]` | Réservés aux pages du catalogue. |

Quelques exigences de fond :

- **Un cas d'usage nomme son porteur.** « Pourrait servir à… » n'est pas un cas
  d'usage ; « la plateforme X vérifie Y avant Z » en est un.
- **La proposition de valeur cite des chiffres.** Volume d'appels, délai
  supprimé, jours-homme économisés. À défaut, dites que la mesure n'existe pas
  encore.
- **Les modalités d'accès décrivent la procédure**, pas seulement le protocole :
  à qui écrire, sous quel délai, avec quelles pièces.
- **Les évolutions listent aussi les ruptures de compatibilité**, avec la date
  de retrait de l'ancienne version.

## 3. Déposer la spécification OpenAPI

Deux options, cumulables :

Fichier hébergé par le catalogue
:   Déposez le YAML ou le JSON dans `docs/assets/openapi/` et renseignez
    `openapi`. Le site reste alors autonome, y compris hors ligne.

URL publiée par le producteur
:   Renseignez `openapi_url`. La spécification est chargée depuis votre serveur
    au moment de l'affichage. Pensez à autoriser l'origine du catalogue dans
    votre configuration CORS, sans quoi le navigateur bloquera la lecture.

Quand les deux sont renseignées, la fiche propose un sélecteur de source. La
copie hébergée reste affichée par défaut.

## 4. Proposer la fiche

Ouvrez une demande de fusion sur le dépôt du catalogue. La revue porte sur
quatre points : exactitude des modalités d'accès, présence d'un contact joignable,
validité de la spécification OpenAPI, et lisibilité de la description
fonctionnelle par une personne extérieure au domaine.

Une fiche est publiée en général sous cinq jours ouvrés.

## 5. La tenir à jour

Une fiche périmée est pire qu'une fiche absente : elle envoie les réutilisateurs
vers un contact qui ne répond plus. Mettez à jour `version`, `maj` et la section
« Évolutions du produit » à chaque livraison, et le champ `statut` dès qu'une
API entre en dépréciation.

Une API qui n'est plus maintenue doit être marquée `deprecie` avec sa date de
retrait, et non supprimée du catalogue : les réutilisateurs ont besoin de
comprendre ce qui leur arrive.
