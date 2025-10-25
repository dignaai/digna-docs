---
title: Data Schema Tracker – Kövesse a séma változásait | digna dokumentációja
description: Tudja meg, hogyan követi a digna Data Schema Tracker az oszlopváltozásokat, az adattípus-frissítéseket és a sémaeltéréseket. Kapjon értesítéseket szándékos és véletlen változásokra, hogy megelőzze az ETL-hibákat és a dashboard hibáit.
---

# Data Schema Tracker – Kövesse a séma változásait

## Cél
A séma evolúciójának nyomon követése és riasztások küldése.

## Műszaki jellemzők
- Követi:
  - Hozzáadott vagy eltávolított oszlopok
  - Adattípus-változások
- Riasztások szándékos és véletlen séma-változások esetén  
- Megelőzi az ETL-pipeline-okat vagy dashboardokat megszakítható **néma sémaeltérést**  

## Használati példák
- Az adattípus-változások (pl. `INT` → `VARCHAR`) észlelése, amelyek későbbi hibákhoz vezethetnek  
- Figyelmeztetés az adatmérnököknek, mielőtt a séma-inkompatibilitások miatt a pipeline-ok meghibásodnának  

## Érték
Lehetővé teszi a csapatok számára, hogy irányítás alatt tartsák a **gyorsan változó, fejlődő adatkészleteket**.