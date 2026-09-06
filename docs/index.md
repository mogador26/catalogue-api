---
summary: false
title: Catalogue des API
description: >-
  Toutes les API exposées par la direction du numérique : description
  fonctionnelle, cas d'usage, modalités d'accès, documentation OpenAPI et
  contact du producteur.
hide_breadcrumb: true
---

# Catalogue des API

Ce catalogue recense les interfaces de programmation applicative mises à
disposition par la direction du numérique. Chaque fiche décrit à quoi sert
l'API, qui l'utilise déjà, comment y accéder et qui contacter.

Les compteurs ci-dessous sont recalculés à chaque publication du site à partir
des fiches elles-mêmes : ils ne peuvent pas diverger du contenu réel du
catalogue.

[[COMPTEURS]]

[[CATALOGUE]]

## Comment lire une fiche

Chaque fiche suit le même plan, pour que la comparaison entre API reste
immédiate :

Description fonctionnelle
:   Ce que l'API expose, sur quel périmètre, avec quelle fraîcheur de données.

Cas d'usage identifiés
:   Les usages déjà en production, nommés avec leur porteur. Un cas d'usage sans
    utilisateur réel n'est pas un cas d'usage.

Proposition de valeur
:   La lecture « bizdev » : le problème résolu, le gain mesuré, les alternatives
    écartées.

Modalités d'accès
:   API ouverte, clé d'API, OAuth 2.0 ou mTLS, avec la procédure d'habilitation
    et les quotas applicables.

Documentation OpenAPI
:   La spécification affichée avec Redoc, téléchargeable au format YAML ou JSON.

Évolutions du produit
:   L'historique des versions et ce qui est prévu ensuite.

Contact du producteur
:   L'équipe responsable, son canal de support et son engagement de réponse.

## Prochaines API

Quatre jalons à venir. La [feuille de route complète](feuille-de-route.md)
détaille l'ensemble des travaux engagés.

[[FEUILLE_DE_ROUTE_EXTRAIT]]

## Réutiliser le catalogue

Le catalogue est publié au format JSON à l'adresse
<a class="fr-link" href="catalogue.json"><code>/catalogue.json</code></a>. Il contient les métadonnées de chaque API,
les compteurs et la feuille de route : de quoi alimenter un tableau de bord ou
un portail tiers sans recopier ces informations à la main.
