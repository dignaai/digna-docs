---
title: Data Schema Tracker – Spremljajte evolucijo sheme | digna dokumentacija
description: Izvedite, kako Data Schema Tracker v digna spremlja spremembe stolpcev, posodobitve tipov podatkov in odstopanja v shemi. Z opozorili za namerne in nenamerne spremembe preprečite napake v ETL procesih in na dashboardih.
---

# Data Schema Tracker – Spremljajte evolucijo sheme

## Namen
Spremljanje evolucije sheme in opozarjanje.

## Tehnične značilnosti
- Sledi:
  - Dodani ali odstranjeni stolpci
  - Spremembe tipov podatkov
- Opozorila za namerne in nenamerne spremembe sheme  
- Preprečuje **tihi odklon sheme**, ki lahko pokvari ETL pipeline-e ali dashboarde  

## Primeri uporabe
- Prepoznavanje sprememb tipov podatkov (npr. `INT` → `VARCHAR`), ki lahko povzročijo napake v poznejših fazah  
- Opozoriti podatkovne inženirje, preden zaradi neskladnosti sheme pipeline-i odpovejo  

## Vrednost
Omogoča ekipam, da imajo nadzor nad **hitro spreminjajočimi se, razvijajočimi podatkovnimi nabori**.