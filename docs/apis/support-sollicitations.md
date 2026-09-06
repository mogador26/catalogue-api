---
sidemenu: true
summary: false
title: Sollicitations de support
resume: >-
  Ouverture et suivi des tickets du centre de services depuis les applications
  métier, sans quitter l'outil de travail.
theme: Support
acces: oauth2
statut: production
producteur: Centre de services numériques
contact_nom: Équipe centre de services
contact_email: api-support@exemple.gouv.fr
version: 4.2.0
maj: 2026-08-20
base_url: https://support.exemple.gouv.fr/api/v4
openapi: assets/openapi/support-sollicitations.yaml
tags:
  - support
  - centre de services
  - ticket
  - ITSM
---

# Sollicitations de support

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API permet à une application métier d'ouvrir une sollicitation auprès du
centre de services, de la suivre et de la clore, sans que l'agent quitte son
outil de travail.

Une sollicitation porte l'application concernée, un objet, une description, une
priorité et le contact du demandeur. Le centre de services y répond selon
l'engagement de service associé à la priorité, l'échéance étant retournée dès la
création.

L'API sert aussi de canal de remontée automatique : une application peut ouvrir
un incident depuis sa supervision, avec le contexte technique déjà renseigné.

## Cas d'usage identifiés

### Signaler une anomalie depuis l'application

Un bouton « signaler un problème » ouvre la sollicitation avec le contexte
technique (version, écran, identifiant de session) déjà rempli. Le temps de
qualification par le centre de services a chuté de 40 %, faute d'aller-retours
pour reconstituer le contexte.

### Ouvrir un incident depuis la supervision

Une alerte de supervision qui persiste plus de dix minutes crée
automatiquement une sollicitation de priorité haute, rattachée à l'application
concernée. La détection ne dépend plus d'un appel d'usager.

### Suivre ses sollicitations dans son outil

Un chef de projet consulte l'état des tickets de son application depuis son
tableau de bord, sans compte dédié sur l'outil du centre de services.

## Proposition de valeur

**Le problème.** Signaler un incident imposait de quitter l'application, de se
connecter à un portail distinct et de redécrire un contexte que l'application
connaissait déjà. Beaucoup d'anomalies n'étaient tout simplement pas signalées.

**Ce que l'API change.** Le signalement se fait là où le problème se produit,
avec le contexte technique attaché.

**Les gains observés.**

- volume de sollicitations qualifiées en hausse de 25 %, sans hausse du temps de
  traitement — les tickets arrivent mieux renseignés ;
- délai moyen de qualification ramené de 25 à 15 minutes ;
- 18 applications intégrées.

**Pour qui c'est utile.** Toute équipe produit qui veut réduire la friction du
signalement, et toute chaîne de supervision qui doit déclencher une prise en
charge humaine.

## Modalités d'accès

!!! info "API soumise à habilitation — OAuth 2.0"

    Réservée aux applications internes. Chaque application dispose de son propre
    client OAuth 2.0 et ne voit que ses sollicitations.

### Obtenir un accès

1. Demander le rattachement de l'application au catalogue de services, si ce
   n'est pas déjà fait.
2. Le centre de services crée le client OAuth 2.0 et déclare les gabarits de
   sollicitation propres à l'application.
3. Une recette conjointe valide les priorités et les engagements associés.

### Engagements de service

| Priorité | Prise en charge | Résolution visée |
| --- | --- | --- |
| Critique | 15 minutes, 24/7 | 4 heures |
| Haute | 1 heure ouvrée | 1 jour ouvré |
| Normale | 4 heures ouvrées | 5 jours ouvrés |
| Basse | 1 jour ouvré | 15 jours ouvrés |

L'échéance calculée est retournée dans le champ `echeanceEngagement` à la
création : l'application peut l'afficher à l'agent, plutôt que de lui laisser
deviner un délai.

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 4.2.0 — 20 août 2026

- Le champ `echeanceEngagement` est retourné dès la création.
- Ajout du statut `en-attente-usager`, jusque-là confondu avec
  `prise-en-charge`.

### Version 4.0.0 — 5 mars 2026

- Passage à OAuth 2.0 et cloisonnement par application. La version 3, à clé
  partagée, a été retirée le 30 juin 2026.

### Prochaines évolutions

- Rappels HTTP à chaque changement d'état, pour supprimer la scrutation
  périodique. À l'étude.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Centre de services numériques |
| Courriel | [api-support@exemple.gouv.fr](mailto:api-support@exemple.gouv.fr) |
| Support | 24/7 pour les incidents critiques, heures ouvrées sinon. |
| Intégration | Accompagnement sur demande, deux ateliers d'une heure. |
