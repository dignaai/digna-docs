---
title: Data Schema Tracker – Spremljanje razvoja sheme | digna Dokumentacija
description: Spoznajte, kako digna Data Schema Tracker spremlja spremembe stolpcev, posodobitve podatkovnih tipov in schema drift. Prejmite opozorila za namensko in nenamerno spreminjanje, da preprečite odpovedi ETL in napake na nadzornih ploščah.
---

# Data Schema Tracker – Spremljanje razvoja sheme

## Namen
Spremljanje in pošiljanje opozoril ob razvoju sheme.

## Tehnične značilnosti
- Spremlja:
  - dodane ali odstranjene stolpce
  - spremembe podatkovnih tipov
- Pošilja opozorila pri namenskih in nenamernih spremembah sheme  
- Preprečuje **silent schema drift**, ki lahko prekine ETL cevovode ali povzroči napake na nadzornih ploščah  

## Primeri uporabe
- Prepoznavanje sprememb podatkovnih tipov (npr. `INT` → `VARCHAR`), ki lahko povzročijo napake v nadaljnjih procesih  
- Opozorila podatkovnim inženirjem, preden cevovodi odpovejo zaradi neskladnosti sheme  

## Vrednost
Omogoča ekipam nadzor nad **hitro spreminjajočimi se, razvijajočimi se zbirkami podatkov**.