---
title: Data Schema Tracker – Overvåg skemaudvikling | digna-dokumentation
description: Lær hvordan digna Data Schema Tracker overvåger kolonneændringer, opdateringer af datatyper og schema drift. Få advarsler om tilsigtede og utilsigtede ændringer for at forhindre ETL-fejl og dashboardfejl.
---

# Data Schema Tracker – Overvåg skemaudvikling

## Formål
Spor og giv advarsler ved skemaudvikling.

## Tekniske funktioner
- Overvåger:
  - Tilføjede eller fjernede kolonner
  - Ændringer i datatyper
- Advarer om både tilsigtede og utilsigtede skemaændringer  
- Forhindrer **silent schema drift** som kan bryde ETL-pipelines eller dashboards  

## Eksempler på brugstilfælde
- Identificere ændringer i datatyper (f.eks. `INT` → `VARCHAR`), der kan forårsage nedstrømsfejl  
- Underrette dataingeniører inden pipelines fejler på grund af skema-uoverensstemmelser  

## Værdi
Holder teams i kontrol over **hurtigt skiftende, udviklende datasæt**.