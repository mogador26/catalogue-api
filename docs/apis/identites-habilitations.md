---
sidemenu: true
summary: false
title: Identités et habilitations
resume: >-
  Annuaire des agents, affectations et habilitations applicatives. Accès par
  certificat client, sur le réseau interne uniquement.
theme: Référentiel
acces: mtls
statut: production
producteur: Direction du numérique — pôle identités
contact_nom: Équipe identités
contact_email: api-identites@exemple.gouv.fr
version: 5.1.0
maj: 2026-03-18
base_url: https://identites.interne.exemple.gouv.fr/api/v5
openapi: assets/openapi/identites-habilitations.yaml
tags:
  - annuaire
  - habilitation
  - identité
  - sécurité
---

# Identités et habilitations

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API expose l'annuaire des agents et leurs habilitations applicatives :
identité professionnelle, structure d'affectation, statut, et rôles détenus sur
une application donnée.

Elle répond à trois questions : qui est cet agent, à quelle structure
appartient-il, et de quoi a-t-il le droit sur telle application. Les
habilitations retournées sont celles en cours de validité ; les habilitations
échues ne sont pas servies.

C'est l'API la plus sensible du catalogue. Trois précautions l'encadrent :
authentification par certificat client, exposition limitée au réseau
interministériel, et périmètre de consultation borné par le certificat lui-même
— une application ne voit que les structures qui la concernent.

## Cas d'usage identifiés

### Décider d'un droit d'accès applicatif

Une application métier interroge les habilitations de l'agent connecté pour
composer son menu. Les droits ne sont plus dupliqués dans chaque application.

### Alimenter un annuaire interne

L'intranet affiche l'organigramme et les coordonnées professionnelles à partir
de la même source que les applications métier. Une mobilité se répercute
partout en une nuit.

### Auditer les habilitations d'une application

Le pôle sécurité extrait chaque trimestre les habilitations actives par
application pour la revue des droits, obligatoire au titre de l'homologation.

### Détecter les comptes orphelins

Le rapprochement entre agents partis et habilitations encore actives signale les
comptes à fermer. 1 400 habilitations résiduelles ont été supprimées lors de la
première campagne.

## Proposition de valeur

**Le problème.** Chaque application gérait sa propre table d'utilisateurs et de
droits, alimentée à la main. Un départ n'était répercuté nulle part
automatiquement, ce qui laissait des accès ouverts — un constat récurrent des
audits de sécurité.

**Ce que l'API change.** Une source unique pour l'identité et les droits, avec
une révocation qui se propage.

**Les gains observés.**

- délai de révocation d'un accès après départ : moins de 24 heures, contre
  plusieurs semaines auparavant ;
- 1 400 habilitations orphelines supprimées à la première campagne ;
- 22 applications raccordées, autant de tables d'utilisateurs supprimées ;
- revue trimestrielle des droits réalisée en deux jours au lieu de trois
  semaines.

**Pour qui c'est utile.** Les équipes applicatives internes, le pôle sécurité,
les exploitants. L'API n'est pas ouverte aux partenaires externes.

## Modalités d'accès

!!! danger "API soumise à habilitation — authentification mutuelle (mTLS)"

    L'accès exige un certificat client délivré par l'autorité de certification
    interne, présenté à chaque appel, et une adresse IP déclarée. L'API n'est
    pas joignable depuis Internet.

### Obtenir un accès

1. L'application doit être inscrite au référentiel des applications et disposer
   d'une homologation de sécurité en cours de validité.
2. Le responsable de l'application dépose une demande de certificat auprès du
   pôle identités, en précisant le périmètre de structures nécessaire et la
   finalité de chaque champ consulté.
3. Après avis du RSSI, le certificat est délivré pour deux ans. Les adresses IP
   sortantes de l'application sont déclarées en parallèle.

### S'authentifier

```bash
curl "$BASE_URL/agents/a.dupont/habilitations?application=REFAPP" \
  --cert /etc/certs/mon-application.crt \
  --key /etc/certs/mon-application.key
```

### Règles d'usage

| Élément | Engagement |
| --- | --- |
| Débit | 120 requêtes par minute et par certificat. |
| Disponibilité | 99,9 % en 24/7. |
| Journalisation | Chaque consultation est tracée et conservée six ans. |
| Minimisation | Seuls les champs déclarés dans la demande sont servis. |
| Renouvellement | Certificat valable deux ans, alerte 90 jours avant l'échéance. |

Toute mise en cache locale des habilitations est limitée à quinze minutes : une
révocation doit produire son effet rapidement.

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 5.1.0 — 18 mars 2026

- Ajout du filtre `application` sur les habilitations d'un agent.
- Le statut `parti` remplace la suppression pure et simple de la fiche, pour
  permettre l'audit des comptes orphelins.

### Version 5.0.0 — 7 octobre 2025

- Passage à l'authentification mutuelle. La version 4, authentifiée par jeton
  partagé, a été retirée le 31 mars 2026.

### Prochaines évolutions

- Notification des changements d'affectation par rappel HTTP, pour éviter la
  synchronisation nocturne complète. Prévue au T2 2027.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Direction du numérique — pôle identités |
| Courriel | [api-identites@exemple.gouv.fr](mailto:api-identites@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 8 h – 18 h. Astreinte 24/7 pour les incidents bloquants. |
| Demande de certificat | [pki@exemple.gouv.fr](mailto:pki@exemple.gouv.fr), instruction sous dix jours ouvrés. |
