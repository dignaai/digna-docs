---
title: Data Schema Tracker – Spremljanje sprememb sheme | digna-dokumentacija
description: Izvedite, kako digna Data Schema Tracker spremlja spremembe stolpcev, posodobitve podatkovnih tipov in drift sheme. Prejmite opozorila o namernih in nenamernih spremembah, da preprečite napake ETL in napake na nadzornih ploščah.
---

# Data Schema Tracker – Spremljanje sprememb sheme

## Namen
Spremljanje in obveščanje o spremembah sheme.

## Tehnične funksjoner
- Spremlja:
  - Dodane ali odstranjene stolpce
  - Spremembe podatkovnih tipov
- Opozarja pri namernih in nenamernih spremembah sheme  
- Preprečuje **silent schema drift**, ki lahko zlomi ETL-pipelines ali nadzorne plošče  

## Primeri uporabe
- Prepoznati spremembe podatkovnih tipov (npr. `INT` → `VARCHAR`), ki lahko povzročijo napake v nadaljnjih procesih  
- Opozoriti podatkovne inženirje, preden pipelines odpovejo zaradi odstopanj v shemi  

## Vrednost
Omogoča ekipam nadzor nad **hitro spreminjajočimi se, stalno razvijajočimi se nabori podatkov**.