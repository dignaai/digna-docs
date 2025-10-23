---
title: Data Schema Tracker – Surveiller l'évolution du schéma | digna Documentation
description: Découvrez comment digna Data Schema Tracker surveille les changements de colonnes, les mises à jour de types de données et la dérive de schéma. Recevez des alertes pour les changements intentionnels et non intentionnels afin d'éviter les échecs ETL et les erreurs dans les tableaux de bord.
---

# Data Schema Tracker – Surveiller l'évolution du schéma

## Purpose
Suivre et alerter les évolutions du schéma.

## Technical Features
- Surveille :
  - Colonnes ajoutées ou supprimées
  - Modifications de type de données
- Alerte sur les modifications de schéma intentionnelles et non intentionnelles  
- Empêche la **dérive silencieuse du schéma** qui peut casser les pipelines ETL ou les tableaux de bord  

## Example Use Cases
- Identifier les modifications de type de données (p.ex., `INT` → `VARCHAR`) susceptibles de provoquer des erreurs en aval  
- Alerter les data engineers avant que les pipelines n'échouent en raison d'incohérences de schéma  

## Value
Permet aux équipes de garder le contrôle des **ensembles de données en évolution rapide**.