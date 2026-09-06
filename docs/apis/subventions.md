---
sidemenu: true
summary: false
title: Subventions et concours financiers
resume: >-
  Dépôt et suivi des demandes de subvention : instruction, décision et
  versements, pour les organismes instructeurs et les éditeurs.
theme: Finances
acces: api-key
statut: production
producteur: Direction des affaires financières — pôle subventions
contact_nom: Équipe subventions
contact_email: api-subventions@exemple.gouv.fr
version: 1.4.0
maj: 2026-04-09
base_url: https://subventions.exemple.gouv.fr/api/v1
openapi: assets/openapi/subventions.yaml
tags:
  - subvention
  - finances publiques
  - association
  - collectivité
---

# Subventions et concours financiers

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API couvre le cycle de vie d'une demande de subvention : dépôt, instruction,
décision et versements. Elle sert deux populations : les organismes instructeurs,
qui suivent leur portefeuille de demandes, et les éditeurs de logiciels de
gestion associative, qui déposent pour le compte de leurs utilisateurs.

Une demande porte un numéro stable, un exercice budgétaire, un bénéficiaire
identifié par son SIRET, un objet, un montant demandé puis accordé, et la liste
des versements réalisés. Chaque dépôt donne lieu à un accusé de réception
horodaté, opposable.

## Cas d'usage identifiés

### Déposer depuis un logiciel de gestion associative

Un éditeur intègre le dépôt dans son outil : l'association saisit son dossier là
où sont déjà ses pièces comptables, et n'a pas à ressaisir sur un portail
distinct. 4 200 dossiers ont été déposés par cette voie en 2026.

### Suivre un portefeuille de demandes

Un service instructeur départemental construit son tableau de bord sur l'API
plutôt que sur des extractions hebdomadaires. Les demandes en attente de
complément sont relancées automatiquement.

### Consolider les concours financiers d'un territoire

Une préfecture agrège les subventions accordées sur son ressort, tous exercices
confondus, pour le rapport annuel d'activité.

### Détecter les doublons de financement

Le rapprochement par SIRET et par objet signale les demandes déposées auprès de
plusieurs financeurs pour la même opération.

## Proposition de valeur

**Le problème.** Le dépôt passait par un portail unique, mal articulé avec les
outils réellement utilisés par les associations. Le suivi reposait sur des
extractions manuelles, avec un décalage d'une semaine.

**Ce que l'API change.** Le dépôt se fait depuis l'outil du demandeur, et le
suivi devient continu. L'accusé de réception horodaté sécurise juridiquement le
respect des délais de dépôt.

**Les gains observés.**

- délai moyen d'instruction ramené de 68 à 45 jours ;
- 30 % des dépôts réalisés par API en 2026, contre 8 % en 2025 ;
- réclamations sur les dates de dépôt quasiment disparues depuis l'accusé
  horodaté.

**Pour qui c'est utile.** Organismes instructeurs, éditeurs de logiciels de
gestion associative, collectivités cofinanceuses.

## Modalités d'accès

!!! info "API avec autorisation d'accès — clé d'API"

    La clé est délivrée à l'organisme instructeur ou à l'éditeur, après signature
    d'une convention précisant le périmètre des dossiers accessibles.

### Obtenir une clé

1. Adresser la demande à l'équipe subventions, en précisant les exercices et les
   territoires concernés.
2. Signer la convention de mise à disposition.
3. Réception de deux clés : recette puis production, après recette conjointe.

### S'authentifier

```bash
curl "$BASE_URL/subventions?exercice=2026&statut=en-instruction" \
  -H "X-API-Key: $CLE_API"
```

### Quotas et disponibilité

| Élément | Engagement |
| --- | --- |
| Débit | 600 requêtes par heure et par clé. |
| Disponibilité | 99,5 % en heures ouvrées. |
| Pièces jointes | Non gérées par l'API à ce stade — voir la feuille de route. |
| Conservation | Dossiers accessibles sur cinq exercices glissants. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 1.4.0 — 9 avril 2026

- Ajout du statut `complement-demande` et de la date d'échéance associée.
- Les versements sont désormais servis dans la fiche de la demande.

### Version 1.2.0 — 15 janvier 2026

- Filtre par SIRET du bénéficiaire.

### Version 1.0.0 — 2 septembre 2025

- Mise en production, dépôt et suivi.

### Prochaines évolutions

- **T1 2027** — dépôt et suivi des pièces justificatives, avec accusé de
  réception horodaté par pièce. Périmètre arrêté.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Direction des affaires financières — pôle subventions |
| Courriel | [api-subventions@exemple.gouv.fr](mailto:api-subventions@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 9 h – 17 h. Réponse sous deux jours ouvrés. |
| Conventionnement | [conventions-subventions@exemple.gouv.fr](mailto:conventions-subventions@exemple.gouv.fr) |
