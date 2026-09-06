---
sidemenu: true
summary: false
title: Référentiel géographique
resume: >-
  Communes, départements et régions, avec l'historique des fusions et des
  changements de nom. Accès libre.
theme: Territoires
acces: ouverte
statut: production
producteur: Pôle données de référence
contact_nom: Équipe données de référence
contact_email: api-geo@exemple.gouv.fr
version: 1.12.0
maj: 2026-01-15
base_url: https://geo.exemple.gouv.fr/api/v1
openapi: assets/openapi/referentiel-geographique.yaml
tags:
  - commune
  - code INSEE
  - territoire
  - donnée de référence
---

# Référentiel géographique

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API expose le découpage administratif : communes, départements, régions, avec
leurs codes officiels, leurs codes postaux, leur population et les coordonnées de
leur centre.

Sa particularité est l'**historique** : fusions, scissions et changements de nom
sont conservés et datés, et chaque requête peut être adressée à un millésime
donné. Un traitement rejoué sur des données de 2018 retrouve le découpage en
vigueur cette année-là, au lieu d'échouer sur des codes disparus.

C'est la donnée de référence la plus consommée du catalogue : elle sert de
socle à presque toutes les autres, qui s'y rattachent par le code INSEE.

## Cas d'usage identifiés

### Compléter une adresse dans un formulaire

Un téléservice propose l'autocomplétion des communes à partir du code postal,
puis enregistre le code INSEE plutôt que le libellé — seul moyen de rester
stable dans le temps.

### Agréger des données par territoire

Un service statistique remonte des données communales au département ou à la
région, sans maintenir sa propre table de correspondance.

### Rejouer un historique de données

Un traitement de reprise applique le millésime de l'époque à des données
anciennes, et traite correctement les 2 800 communes ayant fusionné depuis 2015.

### Cartographier des indicateurs

Une direction produit une carte par commune à partir des coordonnées de centre
fournies, sans dépendre d'un fond de carte propriétaire.

## Proposition de valeur

**Le problème.** Chaque application maintenait sa propre table de communes, mise
à jour au gré des occasions. Les fusions de communes provoquaient chaque année
des rejets de traitement et des rapprochements de données impossibles.

**Ce que l'API change.** Une table de référence maintenue une fois, avec
l'historique nécessaire pour traiter le passé, et un versionnement par
millésime.

**Les gains observés.**

- 47 applications raccordées, autant de tables locales supprimées ;
- 18 millions d'appels par mois, le service le plus sollicité du catalogue ;
- rejets de traitement liés aux fusions de communes ramenés à zéro sur le
  périmètre raccordé.

**Pourquoi elle est ouverte.** Ce sont des données publiques, sans enjeu de
confidentialité, et leur valeur croît avec le nombre de réutilisateurs qui
s'alignent dessus. Toute barrière d'accès aurait poussé chacun à conserver sa
copie locale — exactement le problème qu'il s'agissait de résoudre.

## Modalités d'accès

!!! success "API ouverte"

    Aucune inscription, aucun jeton, aucun quota. Données diffusées sous
    Licence Ouverte 2.0.

```bash
curl "https://geo.exemple.gouv.fr/api/v1/communes?codePostal=01110"
curl "https://geo.exemple.gouv.fr/api/v1/communes/01185?millesime=2018"
```

### Bonnes pratiques

| Élément | Recommandation |
| --- | --- |
| Cache | Les réponses portent un en-tête `Cache-Control` d'une heure. Respectez-le. |
| Millésime | Précisez-le pour tout traitement rejouable ; à défaut, le millésime courant s'applique. |
| Volumétrie | Pour un chargement initial complet, utilisez l'export plutôt que 35 000 appels unitaires. |
| Disponibilité | 99,9 % en 24/7. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 1.12.0 — 15 janvier 2026

- Millésime 2026 publié : 34 fusions intégrées.
- Ajout des coordonnées du centre de chaque commune.

### Version 1.10.0 — 3 septembre 2025

- Historique des changements de nom, en plus des fusions et scissions.

### Version 1.0.0 — 12 mars 2025

- Ouverture du service, millésimes 2015 à 2025.

### Prochaines évolutions

- Exposition des établissements publics de coopération intercommunale et de leur
  composition. Prévue au T2 2027.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Pôle données de référence |
| Courriel | [api-geo@exemple.gouv.fr](mailto:api-geo@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 9 h – 18 h. Réponse sous trois jours ouvrés. |
| Millésime annuel | Publié chaque année à la mi-janvier, annoncé un mois à l'avance. |
