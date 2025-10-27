---
title: Data Schema Tracker – Seuraa skeeman kehitystä | digna Dokumentaatio
description: Opi, miten digna Data Schema Tracker valvoo sarakemuutoksia, tietotyyppipäivityksiä ja skeeman muutoksia. Saat hälytyksiä tarkoituksellisista ja tahattomista muutoksista estääksesi ETL-virheitä ja dashboard-ongelmia.
---

# Data Schema Tracker – Seuraa skeeman kehitystä

## Purpose
Seuraa skeeman kehitystä ja lähettää hälytyksiä.

## Technical Features
- Valvoo:
  - Lisättyjä tai poistettuja sarakkeita
  - Tietotyyppimuutoksia
- Hälyttää sekä tarkoituksellisista että tahattomista skeeman muutoksista  
- Estää **hiljaisen skeeman driftin**, joka voi rikkoa ETL-putket tai dashboardit  

## Example Use Cases
- Tietotyyppimuutosten tunnistaminen (esim. `INT` → `VARCHAR`), jotka voivat aiheuttaa alavirran virheitä  
- Hälyttää data-insinöörejä ennen kuin putket kaatuvat skeeman ristiriitojen vuoksi  

## Value
Auttaa tiimejä hallitsemaan **nopeasti muuttuvia ja kehittyviä tietojoukkoja**.