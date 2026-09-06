---
summary: false
title: Feuille de route
description: Les nouvelles API et les évolutions majeures programmées.
---

# Feuille de route

Cette page présente les API en cours de construction et les évolutions
majeures des API existantes. Elle est alimentée par un fichier unique,
`docs/data/feuille-de-route.yml`, versionné avec le reste du site : une échéance
qui change se voit dans l'historique Git.

Les échéances sont données au trimestre. Un jalon « à l'étude » n'est pas un
engagement de livraison : il signale un besoin identifié dont le cadrage
juridique ou technique n'est pas terminé.

[[FEUILLE_DE_ROUTE]]

## Ce que signifient les niveaux d'avancement

| Niveau | Signification |
| --- | --- |
| À l'étude | Besoin qualifié, cadrage en cours. Ni périmètre ni date ferme. |
| Prévue | Périmètre arrêté, développement inscrit au plan de charge. |
| En cours | Développement démarré, spécification OpenAPI publiée en amont. |
| Livrée | API disponible et documentée dans le catalogue. |

## Proposer un besoin

Un besoin d'API non couvert par cette feuille de route se signale par courriel
à [architecture@exemple.gouv.fr](mailto:architecture@exemple.gouv.fr), ou par
une issue sur le dépôt du catalogue. Une demande est instruite d'autant plus
vite qu'elle décrit l'usage métier visé, la volumétrie attendue et le calendrier
du projet consommateur.

Les besoins exprimés par au moins deux directions différentes sont priorisés :
c'est le meilleur signal qu'une API mutualisée vaut mieux qu'un échange de
fichiers dédié.
