---
title: Data Schema Tracker – Séma evolúciójának nyomon követése | digna dokumentáció
description: Ismerje meg, hogyan követi a digna Data Schema Tracker az oszlopok változásait, az adattípusok frissülését és a sémaeltolódást. Kapjon értesítéseket szándékos és nem szándékos változásokról, hogy megelőzze az ETL-hibákat és a dashboard hibáit.
---

# Data Schema Tracker – Séma evolúciójának nyomon követése

## Cél
A séma változásainak nyomon követése és riasztás.

## Technikai jellemzők
- Figyel:
  - Hozzáadott vagy eltávolított oszlopok
  - Adattípus-változások
- Értesít szándékos és nem szándékos sémaváltozásokról  
- Megakadályozza a **néma sémaeltolódást**, amely megszakíthatja az ETL-pipeline-okat vagy hibákat okozhat a dashboardokon  

## Példák
- Adattípus-változások azonosítása (pl. `INT` → `VARCHAR`), amelyek később hibákat okozhatnak  
- Értesítés az adatmérnököknek, mielőtt a pipeline-ok hibába futnának sémaeltérések miatt  

## Előny
Segít a csapatoknak kontroll alatt tartani a **gyorsan változó, fejlődő adatkészleteket**.