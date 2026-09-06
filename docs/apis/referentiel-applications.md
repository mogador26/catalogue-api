---
sidemenu: true
summary: false
title: Référentiel des applications
resume: >-
  La cartographie du système d'information : applications, briques techniques,
  responsables, dépendances et cycle de vie.
theme: Référentiel
acces: oauth2
statut: production
producteur: Direction du numérique — pôle architecture et urbanisation
contact_nom: Équipe Référentiel des applications
contact_email: referentiel-applications@exemple.gouv.fr
contact_url: https://github.com/dnum-mi/referentiel-applications/issues
version: 1.72.0
maj: 2026-08-28
base_url: https://referentiel-applications.exemple.gouv.fr/api/v1
openapi: assets/openapi/referentiel-applications.yaml
openapi_url: https://raw.githubusercontent.com/dnum-mi/referentiel-applications/main/frontend/openapi/swagger.yaml
tags:
  - cartographie
  - urbanisation
  - système d'information
  - inventaire
  - homologation
---

# Référentiel des applications

[[FICHE_ENTETE]]

## Description fonctionnelle

L'API expose la cartographie du système d'information du ministère : la liste
des applications, ce qu'elles font, qui en est responsable, sur quelles briques
techniques elles reposent et à quelles autres applications elles sont reliées.

Elle sert de source de vérité à toutes les questions qu'on se pose sur le parc
applicatif — « quelles applications utilisent cette base de données ? », « qui
appeler si ce service tombe ? », « lesquelles arrivent en fin de support ? » —
sans passer par des tableurs éparpillés.

Le référentiel couvre cinq familles d'objets :

Applications
:   Nom, code, description métier, direction porteuse, criticité, statut dans le
    cycle de vie (en construction, en production, en décommissionnement,
    décommissionnée), date de mise en service et date de fin de vie prévue.

Responsabilités
:   Propriétaire métier, responsable technique, hébergeur, équipe de support.
    Chaque rôle est rattaché à une structure de l'organigramme, pas à une
    personne, pour survivre aux mobilités.

Composants techniques
:   Langages, cadriciels, serveurs d'application, bases de données, systèmes
    d'exploitation et leurs versions, avec les dates de fin de support éditeur.

Dépendances
:   Liens dirigés entre applications, qualifiés par leur nature (appel
    synchrone, échange de fichiers, réplication de données) et par leur
    criticité.

Conformité
:   Statut d'homologation de sécurité, date de la dernière analyse de risques,
    présence d'une analyse d'impact relative à la protection des données.

Les données sont alimentées par les équipes projet via l'application web du
référentiel, et rafraîchies en continu. L'API restitue l'état courant ; les
modifications sont horodatées et l'historique d'une application est consultable
sur les vingt-quatre derniers mois.

Le code du référentiel est ouvert et publié sur
[github.com/dnum-mi/referentiel-applications](https://github.com/dnum-mi/referentiel-applications).

## Cas d'usage identifiés

### Préparer un plan de remédiation de fin de support

Le pôle sécurité interroge chaque trimestre `/composants?finSupportAvant=…`
pour lister les applications reposant sur une version dont le support éditeur
s'achève dans les six mois, puis croise le résultat avec la criticité métier.
Le plan de remédiation qui demandait trois semaines de collecte manuelle est
désormais produit en une journée.

### Alimenter l'outil de supervision

La plateforme d'hébergement synchronise chaque nuit les métadonnées
d'application (responsable, criticité, canal d'astreinte) depuis
`/applications?modifieDepuis=…`. Les alertes remontent au bon interlocuteur sans
que personne n'ait à tenir à jour une seconde liste de contacts.

### Instruire une demande d'homologation

L'équipe homologation ouvre la fiche d'une application, récupère ses
dépendances et ses composants, et pré-remplit le dossier d'homologation. Le
temps d'instruction passe de quatre à deux semaines, l'essentiel du délai étant
auparavant consacré à reconstituer le périmètre technique.

### Mesurer la dette technique d'une direction

La direction du numérique publie un tableau de bord trimestriel construit sur
`/applications` et `/composants` : part des applications sur des socles
obsolètes, âge moyen du parc, taux de couverture des responsabilités. Les
arbitrages budgétaires s'appuient sur ces indicateurs.

### Préparer une reprise de contrat d'infogérance

Lors du renouvellement d'un marché, l'acheteur extrait le périmètre applicatif
concerné et ses interdépendances pour dimensionner le lot. L'extraction sert
directement d'annexe technique au dossier de consultation.

## Proposition de valeur

**Le problème.** Le parc applicatif d'un ministère se compte en centaines
d'applications, gérées par des dizaines d'équipes. En l'absence de référentiel
partagé, chaque direction reconstitue sa propre cartographie dans un tableur.
Ces tableurs divergent en quelques semaines, et toute question transverse —
sécurité, budget, continuité d'activité — impose une campagne de collecte.

**Ce que l'API change.** Une seule source, tenue à jour par ceux qui
connaissent l'application, consommable par tous les outils qui en ont besoin.
La cartographie cesse d'être un livrable annuel pour devenir une donnée vivante.

**Les gains observés** sur la première année d'exploitation :

- campagne de cartographie annuelle supprimée, soit environ 40 jours-homme
  économisés côté équipes projet ;
- délai d'instruction d'une homologation réduit de moitié ;
- 92 % des applications en production disposent d'un responsable technique
  identifié, contre 61 % avant la mise en service ;
- trois tableurs de suivi concurrents décommissionnés.

**Les alternatives écartées.** Un outil de cartographie du marché a été évalué :
coût de licence élevé, modèle de données rigide, et surtout absence d'API
ouverte, qui aurait reconduit le problème d'origine. L'export CSV nocturne,
solution intermédiaire, a été abandonné parce qu'il ne permettait ni la
recherche ciblée ni la fraîcheur attendue par la supervision.

**Pour qui c'est utile.** Toute équipe qui doit raisonner sur le parc plutôt que
sur une application : sécurité, architecture, achats, continuité d'activité,
pilotage budgétaire. Les données ne contiennent aucune donnée à caractère
personnel autre que des coordonnées professionnelles de contact.

## Modalités d'accès

!!! info "API soumise à habilitation — OAuth 2.0"

    L'API est réservée aux agents et prestataires de l'État disposant d'une
    habilitation nominative. Les données de cartographie renseignent sur la
    surface d'attaque du système d'information : leur diffusion est restreinte.

### Obtenir un accès

1. Adresser une demande d'habilitation à
   [referentiel-applications@exemple.gouv.fr](mailto:referentiel-applications@exemple.gouv.fr)
   en précisant l'application consommatrice, la finalité, la volumétrie estimée
   et le responsable de traitement.
2. L'équipe instruit la demande sous cinq jours ouvrés et crée un client OAuth 2.0
   dédié à l'application consommatrice.
3. L'identifiant et le secret sont transmis par un canal chiffré. Le secret est
   valable douze mois et son renouvellement est notifié trente jours à l'avance.

### S'authentifier

L'API utilise le flux `client_credentials`. Le jeton d'accès est valable une
heure et doit être présenté dans l'en-tête `Authorization`.

```bash
# 1. Obtenir un jeton
curl -X POST https://auth.exemple.gouv.fr/realms/agents/protocol/openid-connect/token \
  -d "grant_type=client_credentials" \
  -d "client_id=$CLIENT_ID" \
  -d "client_secret=$CLIENT_SECRET" \
  -d "scope=referentiel:lecture"

# 2. Appeler l'API
curl https://referentiel-applications.exemple.gouv.fr/api/v1/applications?criticite=vitale \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Portées disponibles

| Portée | Droits |
| --- | --- |
| `referentiel:lecture` | Consultation des applications, composants et dépendances. |
| `referentiel:ecriture` | Création et mise à jour des applications dont le client est propriétaire. |
| `referentiel:admin` | Administration du modèle de données. Réservé à l'équipe produit. |

### Quotas et disponibilité

| Élément | Engagement |
| --- | --- |
| Débit | 60 requêtes par minute et par client, 10 000 par jour. |
| Pagination | 100 éléments par page, 1 000 au maximum sur les exports. |
| Disponibilité | 99,5 % en heures ouvrées, hors fenêtres de maintenance annoncées. |
| Temps de réponse | 300 ms au 95ᵉ centile sur les lectures unitaires. |

Un dépassement de quota renvoie un code `429` accompagné de l'en-tête
`Retry-After`. Les quotas sont relevables sur demande motivée.

## Documentation OpenAPI

Deux sources sont proposées. La **copie hébergée par le catalogue** correspond
à la version installée en production et ne dépend d'aucun service extérieur.
La **spécification publiée par le producteur** est générée à chaque build depuis
le code source et reflète l'état de la branche principale : c'est la référence
pour préparer une montée de version.

Dans les deux cas, le rendu est produit par Redoc exécuté dans votre navigateur,
à partir du bundle servi par ce site. La spécification est téléchargeable pour
générer un client dans le langage de votre choix.

[[REDOC]]

## Évolutions du produit

### Version 1.72.0 — 28 août 2026

- Ajout du filtre `finSupportAvant` sur `/composants`, pour cibler les briques
  arrivant en fin de support éditeur.
- Le champ `criticite` accepte désormais la valeur `vitale`, alignée sur la
  nomenclature de continuité d'activité.

### Version 1.68.0 — 12 juin 2026

- Nouveau point d'entrée `/applications/{id}/dependances` restituant le graphe
  des dépendances sur deux niveaux.
- Correction : la pagination renvoyait un `total` erroné lorsqu'un filtre de
  recherche textuelle était combiné à un filtre de statut.

### Version 1.60.0 — 4 mars 2026

- Historisation des modifications, exposée par `/applications/{id}/historique`.
- Dépréciation du champ `responsable` au profit de `responsables[]`, qui
  distingue les rôles. Le champ déprécié reste servi jusqu'à la version 2.0.0.

### Version 1.40.0 — 15 octobre 2025

- Ouverture de l'écriture aux équipes projet via la portée
  `referentiel:ecriture`.

### Version 1.0.0 — 3 février 2025

- Première mise en production, en lecture seule.

### Prochaines évolutions

- **Version 1.75.0, T4 2026** — webhooks de notification de changement d'état,
  pour remplacer les scrutations horaires. En cours de développement.
- **Version 2.0.0, T2 2027** — retrait du champ `responsable` déprécié. La
  migration sera annoncée six mois à l'avance et l'ancienne version restera
  servie trois mois après la bascule.

## Contact du producteur

| | |
| --- | --- |
| Équipe | Référentiel des applications — pôle architecture et urbanisation |
| Courriel | [referentiel-applications@exemple.gouv.fr](mailto:referentiel-applications@exemple.gouv.fr) |
| Support | Du lundi au vendredi, 9 h – 18 h. Réponse sous deux jours ouvrés. |
| Incident bloquant | Astreinte via le centre de services, référence `REFAPP`. |
| Code source et anomalies | [github.com/dnum-mi/referentiel-applications](https://github.com/dnum-mi/referentiel-applications) |

Les demandes d'évolution sont instruites lors du comité produit mensuel. Une
demande portée par plusieurs directions passe en priorité.
