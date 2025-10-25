---
title: Data Schema Tracker – A sémák evolúciójának monitorozása | digna dokumentáció
description: Tudja meg, hogyan követi a digna Data Schema Tracker az oszlopváltozásokat, az adattípus-frissítéseket és a séma elcsúszását. Kapjon értesítéseket a szándékos és véletlen sémaváltozásokról, hogy megelőzze az ETL-meghibásodásokat és a dashboard hibáit.
---

# Data Schema Tracker – A sémák evolúciójának monitorozása

## Cél
A séma változásainak nyomon követése és jelentése.

## Műszaki képességek
- Követi:
  - Hozzáadott vagy eltávolított oszlopok
  - Adattípus-változások
- Értesítéseket küld a szándékos és a véletlen sémaváltozásokról  
- Megelőzi a **csendes sémadriftet**, amely tönkreteheti az ETL-pipeline-okat vagy a dashboardokat  

## Használati példák
- Adattípus-változások észlelése (például `INT` → `VARCHAR`), amelyek hibákat okozhatnak a feldolgozás további lépéseiben  
- Értesítés az adatmérnököknek még azelőtt, hogy a pipeline-ok leállnának a séma-inkonzisztencia miatt  

## Érték
Lehetővé teszi a csapatok számára, hogy ellenőrizzék a **gyorsan fejlődő adatkészleteket**.