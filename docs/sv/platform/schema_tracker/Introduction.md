---
title: Data Schema Tracker – Övervaka schemautveckling | digna Dokumentation
description: Lär dig hur digna Data Schema Tracker övervakar kolumnändringar, datatypuppdateringar och schemadrift. Få varningar vid avsiktliga och oavsiktliga förändringar för att förhindra ETL-fel och fel i dashboards.
---

# Data Schema Tracker – Övervaka schemats utveckling

## Syfte
Spåra och skicka varningar vid schemaändringar.

## Tekniska funktioner
- Övervakar:
  - Tillagda eller borttagna kolumner
  - Datatypändringar
- Skickar varningar vid både avsiktliga och oavsiktliga schemaändringar  
- Förhindrar **tyst schemadrift** som kan bryta ETL-pipelines eller dashboards  

## Exempel på användningsfall
- Identifiera datatypändringar (t.ex. `INT` → `VARCHAR`) som kan orsaka fel nedströms  
- Varnar dataingenjörer innan pipelines misslyckas på grund av schemamismatch  

## Värde
Håller teamen i kontroll över **snabbrörliga, föränderliga datamängder**.