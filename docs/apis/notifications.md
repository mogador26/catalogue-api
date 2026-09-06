---
sidemenu: true
summary: false
title: Notifications transactionnelles
resume: >-
  Envoi mutualisé de courriels et de SMS transactionnels pour les applications
  du ministère, avec suivi de remise.
theme: Technique
acces: api-key
statut: production
producteur: Socle applicatif — équipe notifications
contact_nom: Équipe notifications
contact_email: api-notifications@exemple.gouv.fr
version: 2.0.3
maj: 2026-08-30
base_url: https://notifications.exemple.gouv.fr/api/v2
openapi: assets/openapi/notifications.yaml
tags:
  - courriel
  - SMS
  - socle
  - mutualisation
---

# Notifications transactionnelles

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API envoie des courriels et des SMS transactionnels pour le compte des
applications du ministère : accusés de réception, notifications de décision,
codes à usage unique, relances.

L'envoi est asynchrone. La réponse confirme la prise en compte, pas la remise ;
l'état final (`envoye`, `remis`, `echec`) se consulte ensuite, ou se reçoit par
rappel HTTP si l'application déclare une URL de retour.

Le contenu n'est jamais transmis en clair par l'appelant : l'application
référence un **gabarit** déclaré au préalable et fournit les variables. Ce choix
garantit que la relecture juridique et la conformité d'un message sont faites
une fois, à la déclaration du gabarit, et non à chaque envoi.

L'API ne gère pas les envois de masse : une campagne d'information relève d'un
autre outil, avec ses règles de consentement propres.

## Cas d'usage identifiés

### Accuser réception d'une démarche

Un téléservice confirme le dépôt d'un dossier par courriel dans la minute, avec
le numéro de dossier et la date de dépôt.

### Envoyer un code à usage unique

Une application d'authentification envoie un code par SMS, avec un suivi de
remise qui permet de proposer un renvoi si l'opérateur signale un échec.

### Notifier une décision

Un service instructeur informe le demandeur de la décision prise sur son
dossier, avec le même gabarit pour toutes les applications d'un même domaine.

### Relancer sur pièce manquante

Une relance automatique est déclenchée sept jours après une demande de
complément restée sans réponse.

## Proposition de valeur

**Le problème.** Chaque application gérait son propre envoi : serveur de
messagerie dédié, contrat SMS distinct, gabarits recopiés. Les conséquences
étaient prévisibles — messages classés en indésirable faute de réputation de
domaine maîtrisée, aucun suivi de remise, et autant de contrats à renégocier.

**Ce que l'API change.** Un service, une réputation d'expéditeur soignée, des
gabarits relus une fois, un suivi de remise homogène.

**Les gains observés.**

- taux de remise des courriels porté de 91 % à 99,2 % ;
- coût unitaire du SMS réduit de 35 % par la mutualisation des volumes ;
- 34 applications raccordées, 11 infrastructures d'envoi décommissionnées ;
- délai de mise en service d'un nouveau canal d'envoi : deux jours contre six
  semaines.

**Pour qui c'est utile.** Toute application qui envoie des messages
individuels déclenchés par une action. Pour de la communication de masse,
adressez-vous à l'outil de campagnes.

## Modalités d'accès

!!! info "API avec autorisation d'accès — clé d'API"

    Une clé par application et par environnement, transmise dans l'en-tête
    `X-API-Key`. Le raccordement suppose la déclaration préalable des gabarits.

### Obtenir un accès

1. Décrire les messages à envoyer : canal, contenu, variables, volumétrie
   attendue.
2. L'équipe crée les gabarits après relecture, et délivre les clés de recette.
3. Après un envoi de test validé, la clé de production est délivrée.

### S'authentifier

```bash
curl -X POST "$BASE_URL/envois" \
  -H "X-API-Key: $CLE_API" \
  -H "Content-Type: application/json" \
  -d '{
        "gabarit": "accuse-reception",
        "destinataire": "usager@exemple.fr",
        "variables": {"numeroDossier": "SUB-2026-004512"}
      }'
```

### Quotas et disponibilité

| Élément | Engagement |
| --- | --- |
| Débit | 100 envois par seconde et par application, en pic. |
| Disponibilité | 99,9 % en 24/7. |
| Remise courriel | 95 % remis en moins de 60 secondes. |
| Conservation | Journal des envois conservé 90 jours ; le contenu ne l'est pas. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 2.0.3 — 30 août 2026

- Correction : les rappels HTTP n'étaient pas rejoués après une erreur 5xx de
  l'application destinataire.

### Version 2.0.0 — 4 février 2026

- Rappels HTTP sur changement d'état.
- Le contenu libre n'est plus accepté : tous les envois passent par un gabarit.
  Les applications concernées ont été accompagnées pendant trois mois.

### Version 1.0.0 — 6 mai 2025

- Mise en production, canal courriel seul. Le canal SMS a suivi en
  septembre 2025.

### Prochaines évolutions

- Envoi de courriers postaux pour les usagers non joignables par voie
  électronique. À l'étude avec le prestataire d'affranchissement.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Socle applicatif — équipe notifications |
| Courriel | [api-notifications@exemple.gouv.fr](mailto:api-notifications@exemple.gouv.fr) |
| Support | 24/7 pour les incidents de production. |
| Déclaration de gabarit | Sous cinq jours ouvrés, relecture comprise. |
