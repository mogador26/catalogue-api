---
sidemenu: true
summary: false
title: Détention d'armes (SIA)
resume: >-
  Râtelier numérique d'un détenteur, statut d'une arme et validité d'une
  autorisation, pour les armuriers et les fédérations.
theme: Armes
acces: oauth2
statut: production
producteur: Service central des armes et explosifs
contact_nom: Équipe SIA
contact_email: api-sia@exemple.gouv.fr
version: 2.1.0
maj: 2026-05-22
base_url: https://sia.exemple.gouv.fr/api/v2
openapi: assets/openapi/detention-armes.yaml
tags:
  - armes
  - armurier
  - fédération sportive
  - contrôle réglementaire
---

# Détention d'armes (SIA)

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API donne accès au système d'information sur les armes : la liste des armes
rattachées à un détenteur — son râtelier numérique —, le statut réglementaire
d'une arme identifiée par son numéro de série, et la validité d'une
autorisation de détention.

Trois principes gouvernent la conception :

Périmètre restreint
:   Un armurier ne voit que les détenteurs qui se présentent chez lui, après
    saisie de leur numéro SIA. Aucune requête de balayage n'est possible.

Réponse minimale
:   La vérification d'une autorisation renvoie un booléen et une date
    d'échéance, jamais le motif d'un refus. Le contrôle n'a pas à révéler la
    situation personnelle du détenteur.

Traçabilité
:   Chaque consultation est horodatée et imputée au client appelant. Les
    journaux sont accessibles au détenteur sur demande.

## Cas d'usage identifiés

### Vendre une arme en armurerie

Le logiciel de caisse de l'armurier vérifie l'autorisation du client et
l'inscription de l'arme au râtelier avant d'enregistrer la cession. Le contrôle
qui demandait un appel téléphonique à la préfecture est instantané.

### Contrôler une licence en club de tir

Une fédération sportive vérifie, à l'inscription annuelle de ses licenciés, la
cohérence entre les armes déclarées et les autorisations détenues. Les écarts
sont signalés au licencié avant qu'ils ne deviennent une infraction.

### Instruire une demande d'autorisation

Le service instructeur récupère le râtelier existant du demandeur pour vérifier
les seuils de détention par catégorie, sans ressaisie.

## Proposition de valeur

**Le problème.** Les vérifications réglementaires reposaient sur des documents
papier présentés par le détenteur, invérifiables en séance, et sur des appels
téléphoniques aux services préfectoraux. La charge retombait sur les
préfectures, l'incertitude sur les professionnels.

**Ce que l'API change.** La vérification est intégrée au logiciel métier de
l'armurier ou du club. Elle est immédiate, tracée, et opposable.

**Les gains observés.**

- 90 % des cessions en armurerie contrôlées automatiquement ;
- appels téléphoniques aux préfectures divisés par quatre sur le sujet armes ;
- délai d'instruction d'une demande d'autorisation réduit d'une semaine.

**Ce que l'API ne fait pas.** Elle ne permet ni la déclaration ni la
modification du râtelier : l'écriture depuis les logiciels métier est à la
feuille de route, sous réserve d'un cadrage juridique complémentaire.

## Modalités d'accès

!!! warning "API soumise à habilitation — OAuth 2.0"

    Réservée aux armuriers agréés, aux fédérations délégataires et aux services
    instructeurs. L'habilitation est nominative et limitée au périmètre du
    demandeur.

### Obtenir un accès

1. Le demandeur justifie de son agrément ou de sa délégation.
2. Le service central des armes et explosifs instruit sous dix jours ouvrés.
3. Un client OAuth 2.0 est créé, avec la portée `sia:lecture` et un périmètre
   territorial ou fédéral déclaré.

### Quotas et disponibilité

| Élément | Engagement |
| --- | --- |
| Débit | 30 requêtes par minute et par client. |
| Disponibilité | 99,5 % en heures ouvrées étendues (7 h – 22 h). |
| Journalisation | Conservation des consultations pendant cinq ans. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 2.1.0 — 22 mai 2026

- Ajout du point d'entrée `/autorisations/{numero}/validite`, à réponse binaire.
- Le statut `neutralisee` est distingué de `detruite`.

### Version 2.0.0 — 8 janvier 2026

- Refonte du modèle de données aligné sur les catégories réglementaires A1 à D.
- Suppression du champ `nomDetenteur` : le nom n'est plus servi, l'identifiant
  SIA suffit à l'usage.

### Prochaines évolutions

- **Version 2.4.0, T1 2027** — écriture des déclarations de cession depuis les
  logiciels d'armurerie. Périmètre arrêté, développement inscrit au plan de
  charge.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Service central des armes et explosifs |
| Courriel | [api-sia@exemple.gouv.fr](mailto:api-sia@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 9 h – 17 h. Réponse sous deux jours ouvrés. |
| Habilitations | [habilitations-sia@exemple.gouv.fr](mailto:habilitations-sia@exemple.gouv.fr) |
