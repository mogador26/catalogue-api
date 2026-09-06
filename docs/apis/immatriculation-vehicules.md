---
sidemenu: true
summary: false
title: Immatriculation des véhicules
resume: >-
  Caractéristiques techniques, situation administrative et historique des
  certificats d'immatriculation d'un véhicule.
theme: Transport
acces: oauth2
statut: production
producteur: Bureau des titres — équipe immatriculation
contact_nom: Équipe immatriculation
contact_email: api-immatriculation@exemple.gouv.fr
version: 3.4.0
maj: 2026-07-16
base_url: https://immatriculation.exemple.gouv.fr/api/v3
openapi: assets/openapi/immatriculation-vehicules.yaml
tags:
  - véhicule
  - certificat d'immatriculation
  - gage
  - contrôle
---

# Immatriculation des véhicules

[[FICHE_ENTETE]]

## Description fonctionnelle

À partir d'un numéro d'immatriculation, l'API restitue l'identité technique du
véhicule (marque, modèle, énergie, puissance fiscale, date de première mise en
circulation), sa situation administrative (gage, opposition, déclaration de vol
ou de destruction) et l'historique de ses certificats d'immatriculation.

Elle ne restitue **aucune donnée sur le titulaire**. L'identité du propriétaire
relève d'un autre dispositif, soumis à des conditions d'accès distinctes.

Les données proviennent du système d'immatriculation des véhicules et sont
mises à jour en temps réel : une déclaration de cession enregistrée le matin est
visible dans la minute.

## Cas d'usage identifiés

### Sécuriser une transaction entre particuliers

Une plateforme de petites annonces automobiles vérifie, au dépôt de l'annonce,
que le véhicule n'est ni gagé ni déclaré volé. Les annonces frauduleuses ont
reculé de 70 % en un an sur le périmètre couvert.

### Instruire un dossier d'assurance

Un assureur pré-remplit le contrat à partir des caractéristiques techniques
réelles du véhicule plutôt que d'une saisie du client. Les écarts de tarification
liés à une erreur de version de modèle ont quasiment disparu.

### Contrôler l'accès à une zone à faibles émissions

Une métropole interroge la vignette Crit'Air associée au véhicule pour autoriser
ou refuser l'entrée dans sa zone réglementée, sans conserver de base locale.

### Préparer un contrôle routier

Les applications embarquées des forces de l'ordre affichent la situation du
véhicule avant l'interception, ce qui évite un appel radio au centre
d'information.

## Proposition de valeur

**Le problème.** Vérifier l'état d'un véhicule imposait jusqu'ici une demande de
certificat de situation administrative, obtenue en différé et transmise en PDF.
Le délai — souvent plusieurs heures — était incompatible avec une transaction en
ligne ou un contrôle sur le terrain.

**Ce que l'API change.** La même vérification devient une requête de 200
millisecondes, intégrable dans un parcours utilisateur existant.

**Les gains observés.**

- 4,2 millions d'appels par mois, dont 60 % émis par des plateformes privées ;
- fraude à la revente en recul sur les plateformes équipées ;
- suppression de 180 000 demandes annuelles de certificat de situation
  administrative, et de leur traitement.

**Pour qui c'est utile.** Assureurs, plateformes de vente, loueurs,
collectivités gérant une zone à faibles émissions, forces de l'ordre.

## Modalités d'accès

!!! warning "API soumise à habilitation — OAuth 2.0"

    L'accès est ouvert aux organismes dont la finalité relève d'un cas d'usage
    prévu par le cadre juridique applicable. Chaque appel est journalisé pendant
    trois ans et rattaché au client habilité.

### Obtenir un accès

1. Déposer une demande d'habilitation décrivant la finalité poursuivie, la
   volumétrie attendue et le fondement juridique invoqué.
2. Instruction par le bureau des titres, sous quinze jours ouvrés. Une
   convention est signée avec l'organisme.
3. Un client OAuth 2.0 est créé pour l'environnement de recette, puis pour la
   production après recette conjointe.

### S'authentifier

```bash
curl "$BASE_URL/vehicules/AB-123-CD" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Quotas et disponibilité

| Élément | Engagement |
| --- | --- |
| Débit | 300 requêtes par minute, relevable sur justification. |
| Disponibilité | 99,9 % en 24/7. |
| Temps de réponse | 200 ms au 95ᵉ centile. |
| Journalisation | Conservation des appels pendant trois ans. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 3.4.0 — 16 juillet 2026

- Ajout du champ `crit_air` sur la fiche véhicule.
- Le champ `situation` distingue désormais `gage` et `opposition`, jusqu'ici
  fusionnés sous une valeur unique.

### Version 3.2.0 — 4 février 2026

- Nouveau point d'entrée `/vehicules/{immatriculation}/historique`.

### Version 3.0.0 — 12 septembre 2025

- Passage à OAuth 2.0. La version 2, authentifiée par clé partagée, a été
  retirée le 31 décembre 2025 après six mois de fonctionnement en parallèle.

### Prochaines évolutions

- **Version 3.6.0, T4 2026** — consultation du dernier procès-verbal de contrôle
  technique, pour les habilitations qui le prévoient. En cours de développement.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Bureau des titres — équipe immatriculation |
| Courriel | [api-immatriculation@exemple.gouv.fr](mailto:api-immatriculation@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 8 h – 19 h. Réponse sous un jour ouvré. |
| Incident bloquant | Astreinte 24/7 via le centre de services, référence `SIV-API`. |
