---
sidemenu: true
summary: false
title: Entreprises et établissements
resume: >-
  Identité légale des entreprises et de leurs établissements : dénomination,
  activité, adresse et état administratif.
theme: Entreprises et associations
acces: api-key
statut: production
producteur: Pôle données économiques
contact_nom: Équipe données entreprises
contact_email: api-entreprises@exemple.gouv.fr
version: 2.6.1
maj: 2026-08-11
base_url: https://entreprises.exemple.gouv.fr/api/v2
openapi: assets/openapi/entreprises-etablissements.yaml
tags:
  - entreprise
  - SIRET
  - SIREN
  - marché public
---

# Entreprises et établissements

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API restitue l'identité légale d'une entreprise à partir de son numéro SIREN,
celle d'un établissement à partir de son SIRET, et permet une recherche par
raison sociale, activité ou territoire.

Chaque fiche comporte la dénomination, la forme juridique, le code d'activité
principale, la date de création, l'état administratif (active ou cessée) et
l'adresse de l'établissement. Les données sont rafraîchies quotidiennement
depuis le répertoire national.

L'API ne diffuse ni les données financières, ni les dirigeants, ni les
bénéficiaires effectifs : ces informations relèvent d'autres dispositifs.

## Cas d'usage identifiés

### Vérifier un candidat à un marché public

Les plateformes d'achat public contrôlent l'existence et l'état administratif du
candidat au dépôt de son offre. Une entreprise radiée est écartée avant
l'ouverture des plis, et non après.

### Pré-remplir un formulaire administratif

Les téléservices de l'État demandent le SIRET et remplissent seuls les huit
champs d'identité qui suivent. Le taux d'abandon de formulaire a reculé de 12 %
sur les démarches équipées.

### Fiabiliser un fichier fournisseurs

Un service financier rapproche mensuellement sa base fournisseurs du répertoire
et détecte les cessations d'activité avant l'émission d'un bon de commande.

### Cartographier un tissu économique local

Une intercommunalité recense les établissements par code d'activité sur son
territoire pour cibler un dispositif d'accompagnement.

## Proposition de valeur

**Le problème.** Chaque service reconstituait sa propre base d'identités
d'entreprises, alimentée par saisie manuelle. Les écarts d'orthographe et les
états administratifs périmés généraient des rejets de paiement et des relances
inutiles.

**Ce que l'API change.** Une identité de référence, servie à la demande, plutôt
qu'une copie locale qui vieillit.

**Les gains observés.**

- 26 téléservices de l'État équipés ;
- rejets de mandatement pour identité erronée en baisse de 40 % sur le périmètre
  équipé ;
- environ 900 000 saisies manuelles évitées par an.

**Pourquoi une clé d'API.** Les données sont publiques, mais la volumétrie
justifie un identifiant : la clé permet de contacter les réutilisateurs avant une
évolution incompatible, et d'ajuster les quotas au cas par cas. Elle n'ouvre
aucun droit supplémentaire sur les données.

## Modalités d'accès

!!! info "API avec autorisation d'accès — clé d'API"

    L'accès demande une clé nominative, transmise dans l'en-tête `X-API-Key`.
    L'obtention est déclarative : elle prend quelques minutes, sans instruction
    de dossier.

### Obtenir une clé

1. Créer un compte sur le portail des réutilisateurs avec une adresse
   professionnelle.
2. Déclarer l'application consommatrice et l'usage envisagé.
3. La clé est délivrée immédiatement pour l'environnement de recette, et sous un
   jour ouvré pour la production.

### S'authentifier

```bash
curl "$BASE_URL/entreprises/130025265" \
  -H "X-API-Key: $CLE_API"
```

La clé identifie une application, pas une personne. Elle ne doit jamais être
publiée dans du code exécuté côté navigateur : les appels se font depuis votre
serveur.

### Quotas et disponibilité

| Élément | Engagement |
| --- | --- |
| Débit | 2 000 requêtes par heure et par clé, relevable sur demande motivée. |
| Disponibilité | 99,7 % en 24/7. |
| Fraîcheur | Mise à jour quotidienne, à 6 h. |
| Rotation | La clé est valable deux ans ; le renouvellement est notifié 60 jours avant. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 2.6.1 — 11 août 2026

- Correction : les établissements fermés remontaient dans la recherche malgré
  le filtre d'état.

### Version 2.6.0 — 3 juin 2026

- Recherche par code d'activité et par département.

### Version 2.0.0 — 20 novembre 2025

- Séparation des ressources `entreprises` et `etablissements`, auparavant
  fusionnées. La version 1 a été retirée le 30 juin 2026.

### Prochaines évolutions

- Signalement des changements par abonnement, afin d'éviter le rapprochement
  périodique de fichiers entiers. À l'étude.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Pôle données économiques |
| Courriel | [api-entreprises@exemple.gouv.fr](mailto:api-entreprises@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 9 h – 18 h. Réponse sous deux jours ouvrés. |
| Relèvement de quota | Sur demande motivée, réponse sous cinq jours ouvrés. |
