---
title: Data Schema Tracker – Sémaváltozások figyelése | digna-dokumentáció
description: Ismerje meg, hogyan figyeli a digna Data Schema Tracker az oszlopváltozásokat, az adattípusok frissítéseit és a sémaeltolódást. Kapjon riasztásokat szándékos és nem szándékos változásokról az ETL-hibák és a dashboard hibáinak megelőzéséhez.
---

# Data Schema Tracker – Sémaváltozások figyelése

## Cél
Kövesse és jelezze a sémaváltozásokat.

## Műszaki jellemzők
- Figyel:
  - Hozzáadott vagy eltávolított oszlopokat
  - Adattípus-változásokat
- Értesítést küld mind szándékos, mind nem szándékos sémaváltozásokról  
- Megakadályozza a **silent schema drift**-et, amely megtörheti az ETL-pipeline-okat vagy a dashboardokat  

## Használati példák
- Az adattípus-változások azonosítása (pl. `INT` → `VARCHAR`), amelyek hibákat okozhatnak a lefelé irányuló folyamatokban  
- Az adatmérnökök értesítése, mielőtt a pipeline-ok hibára futnának sémaeltérések miatt  

## Érték
Segít a csapatoknak ellenőrzés alatt tartani a **gyorsan mozgó, folyamatosan fejlődő adatkészleteket**.