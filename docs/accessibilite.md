---
title: Déclaration d'accessibilité
description: Niveau de conformité au RGAA, contenus non accessibles et voies de recours.
---

# Déclaration d'accessibilité

La direction du numérique s'engage à rendre ce site accessible, conformément à
l'article 47 de la loi n° 2005-102 du 11 février 2005.

Cette déclaration s'applique au site **Catalogue des API**
(`https://catalogue-api.exemple.gouv.fr`).

## État de conformité

Le catalogue des API est **partiellement conforme** au référentiel général
d'amélioration de l'accessibilité (RGAA), version 4.1, en raison des
non-conformités listées ci-dessous.

## Résultats des tests

L'audit de conformité réalisé le **12 juin 2026** par un prestataire externe
révèle que **89 %** des critères du RGAA 4.1 sont respectés. Le taux moyen de
conformité, calculé sur l'ensemble des pages de l'échantillon, s'établit à 94 %.

## Contenus non accessibles

### Non-conformités

**Documentation OpenAPI (composant Redoc).** Le composant qui affiche les
spécifications OpenAPI est un logiciel tiers dont nous ne maîtrisons pas le
balisage. Trois écarts sont identifiés :

- certains contrastes de la barre latérale sont inférieurs au ratio de 4,5:1
  exigé (critère 3.2) ;
- l'ordre de tabulation dans les exemples de réponse repliables n'est pas
  toujours cohérent avec l'ordre de lecture (critère 12.8) ;
- les zones repliables ne restituent pas systématiquement leur état aux
  technologies d'assistance (critère 7.1).

**Mesures compensatoires.** Chaque spécification est téléchargeable au format
YAML ou JSON depuis la fiche de l'API : le contenu documentaire reste
intégralement accessible, dans un format lisible par tout outil. Par ailleurs, la
documentation n'est pas chargée automatiquement — un bouton explicite la
déclenche —, ce qui évite d'imposer ce composant à qui n'en a pas besoin.

**Filtrage du catalogue.** Le filtrage des tuiles s'appuie sur JavaScript.
Sans JavaScript, toutes les API restent affichées et consultables, mais les
filtres et la recherche locale sont inopérants. La navigation par le menu et le
moteur de recherche du site restent disponibles.

### Contenus non soumis à l'obligation d'accessibilité

Les spécifications OpenAPI publiées par les producteurs, chargées depuis leurs
serveurs, relèvent de la responsabilité de leurs producteurs respectifs.

## Amélioration et contact

Nous corrigeons ces écarts au fil des versions du composant Redoc et de nos
propres développements. La prochaine évaluation est prévue en juin 2027.

Si vous n'arrivez pas à accéder à un contenu ou à un service, contactez-nous
pour être orienté vers une alternative accessible ou obtenir le contenu sous une
autre forme :

- courriel : [accessibilite@exemple.gouv.fr](mailto:accessibilite@exemple.gouv.fr) ;
- courrier : Direction du numérique — mission accessibilité, 1 rue de l'Exemple,
  75000 Paris.

Nous répondons sous quinze jours ouvrés.

## Voies de recours

Si vous constatez un défaut d'accessibilité vous empêchant d'accéder à un
contenu ou à une fonctionnalité du site, que vous nous le signalez et que vous ne
parvenez pas à obtenir une réponse, vous pouvez :

- [écrire un message au Défenseur des droits](https://formulaire.defenseurdesdroits.fr/) ;
- contacter [le délégué du Défenseur des droits dans votre région](https://www.defenseurdesdroits.fr/carte-des-delegues) ;
- envoyer un courrier par la poste, gratuitement, sans affranchissement :
  Défenseur des droits, Libre réponse 71120, 75342 Paris CEDEX 07.

## Technologies utilisées

HTML 5, CSS 3, JavaScript, système de design de l'État (DSFR) 1.15, MkDocs,
composant Redoc pour l'affichage des spécifications OpenAPI.

## Environnement de test

Les tests ont été réalisés avec les combinaisons suivantes : NVDA et Firefox,
JAWS et Chrome, VoiceOver et Safari.

<p class="fr-text--sm fr-mt-4w">Déclaration établie le 12 juin 2026, mise à jour
le 1<sup>er</sup> septembre 2026.</p>
