---
title: Data Schema Tracker – Monitorare l'evoluzione dello schema | Documentazione di digna
description: Scopri come il Data Schema Tracker di digna monitora le modifiche alle colonne, gli aggiornamenti dei tipi di dato e lo schema drift. Ricevi avvisi per cambiamenti intenzionali e non intenzionali per prevenire fallimenti ETL e errori nei dashboard.
---

# Data Schema Tracker – Monitorare l'evoluzione dello schema

## Scopo
Monitorare e inviare avvisi sull'evoluzione dello schema.

## Caratteristiche tecniche
- Monitora:
  - Colonne aggiunte o rimosse
  - Modifiche ai tipi di dato
- Invia avvisi sia per cambiamenti intenzionali che non intenzionali dello schema  
- Previene **silent schema drift** che può interrompere le pipeline ETL o i dashboard  

## Esempi d'uso
- Identificare modifiche ai tipi di dato (ad es., `INT` → `VARCHAR`) che possono causare errori a valle  
- Avvisare i data engineer prima che le pipeline falliscano a causa di incongruenze di schema  

## Valore
Mantiene i team al controllo di dataset **in rapida evoluzione**.