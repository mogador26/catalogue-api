---
sidemenu: true
summary: false
title: Répertoire national des associations
resume: >-
  Identité, objet et siège des associations déclarées en préfecture. Accès
  libre, sans inscription ni jeton.
theme: Entreprises et associations
acces: ouverte
statut: production
producteur: Bureau des associations
contact_nom: Équipe répertoire des associations
contact_email: api-associations@exemple.gouv.fr
version: 1.9.0
maj: 2026-06-02
base_url: https://associations.exemple.gouv.fr/api/v1
openapi: assets/openapi/repertoire-associations.yaml
tags:
  - association
  - RNA
  - vie associative
  - donnée ouverte
---

# Répertoire national des associations

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API expose le répertoire des associations déclarées : titre, objet statutaire,
adresse du siège, date de déclaration et, le cas échéant, date de dissolution et
numéro SIRET.

Deux opérations suffisent à couvrir l'essentiel des usages : une recherche
plein texte filtrable par département et par état d'activité, et la consultation
d'une association par son numéro RNA.

Les données diffusées sont celles publiées au Journal officiel des associations.
Elles ne comportent aucune donnée à caractère personnel : les dirigeants ne sont
pas diffusés, conformément au cadre applicable au répertoire.

## Cas d'usage identifiés

### Pré-remplir une demande de subvention

Une plateforme de subventions locale récupère l'identité de l'association à
partir de son numéro RNA. Le demandeur ne ressaisit ni le titre, ni l'objet, ni
l'adresse du siège : quatre champs en moins, et plus d'écart avec le répertoire.

### Animer un annuaire local

Une commune publie l'annuaire des associations de son territoire à partir du
filtre départemental, puis l'enrichit de ses propres informations
(créneaux d'équipements, contacts).

### Fiabiliser un fichier interne

Un service instructeur rapproche chaque trimestre son fichier de bénéficiaires
du répertoire, pour détecter les associations dissoutes avant d'engager un
versement.

### Alimenter un travail de recherche

Les chercheurs en sociologie de la vie associative utilisent l'API pour
constituer des échantillons par objet statutaire et par territoire.

## Proposition de valeur

**Le problème.** Le répertoire était diffusé sous forme d'un export national
mensuel de plusieurs gigaoctets. Le réutilisateur devait le télécharger,
l'intégrer et le rafraîchir lui-même — un coût d'entrée disproportionné pour
qui n'a besoin que de vérifier un numéro RNA.

**Ce que l'API change.** Une requête HTTP suffit. L'export en masse reste
disponible pour les usages statistiques, mais il n'est plus le seul point
d'entrée.

**Les gains observés.**

- 340 réutilisateurs identifiés en dix-huit mois, dont 200 collectivités ;
- 12 millions d'appels par mois ;
- volume de téléchargement de l'export mensuel divisé par trois, avec l'économie
  de bande passante correspondante.

**Pourquoi elle est ouverte.** Les données sont publiques et sans risque de
réidentification. Toute barrière d'accès — même une simple inscription — aurait
écarté les réutilisations spontanées, qui constituent l'essentiel du trafic.

## Modalités d'accès

!!! success "API ouverte"

    Aucune inscription, aucun jeton, aucune convention. Les données sont
    diffusées sous Licence Ouverte 2.0 : la réutilisation est libre, y compris
    commerciale, à condition de mentionner la source et la date de mise à jour.

```bash
curl "https://associations.exemple.gouv.fr/api/v1/associations?q=plongée&departement=01"
```

### Usage raisonnable

Aucun quota n'est appliqué, mais un mécanisme de limitation protège le service
en cas d'usage anormal : au-delà de 50 requêtes par seconde et par adresse IP,
les réponses sont temporairement ralenties. Pour une extraction massive,
l'export national reste plus efficace, pour vous comme pour nous.

| Élément | Engagement |
| --- | --- |
| Disponibilité | 99,5 % en 24/7. |
| Cache | Réponses mises en cache une heure, en-tête `Cache-Control` renseigné. |
| Fraîcheur | Publication au Journal officiel répercutée sous 24 heures. |

## Documentation OpenAPI

[[REDOC]]

## Évolutions du produit

### Version 1.9.0 — 2 juin 2026

- Ajout du filtre `active`, qui exclut par défaut les associations dissoutes.
- Le champ `siret` est désormais servi lorsqu'il est connu.

### Version 1.6.0 — 14 janvier 2026

- Recherche plein texte étendue à l'objet statutaire.

### Version 1.0.0 — 9 avril 2025

- Ouverture du service.

### Prochaines évolutions

- Exposition des annonces publiées au Journal officiel associées à chaque
  association. À l'étude, sous réserve du volume d'archives à reprendre.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Bureau des associations |
| Courriel | [api-associations@exemple.gouv.fr](mailto:api-associations@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 9 h – 18 h. Réponse sous trois jours ouvrés. |
| Signaler une donnée erronée | Auprès de la préfecture du siège de l'association, qui seule peut corriger la déclaration. |
