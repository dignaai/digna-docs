---
title: Data Schema Tracker – Nadzor evolucije shem | dokumentacija digna
description: Izvedite, kako digna Data Schema Tracker spremlja spremembe stolpcev, posodobitve tipov podatkov in odmik sheme. Prejemajte obvestila o namernih in nenamernih spremembah, da preprečite prekinitve ETL in napake na nadzornih ploščah.
---

# Data Schema Tracker – Nadzor evolucije shem

## Namen
Spremljati in obveščati o evoluciji sheme.

## Tehnične zmogljivosti
- Spremlja:
  - Dodani ali odstranjeni stolpci
  - Spremembe tipov podatkov
- Pošilja obvestila o namernih in nenamernih spremembah sheme  
- Preprečuje **tihi odmik sheme**, ki lahko zruši ETL-pipelines ali dashboards  

## Primeri uporabe
- Odkritje sprememb tipov podatkov (na primer `INT` → `VARCHAR`), ki lahko povzročijo napake v naslednjih korakih obdelave  
- Obveščanje inženirjev podatkov, preden se pipelines ustavijo zaradi neskladnosti shem  

## Vrednost
Omogoča ekipam nadzor nad **hitro razvijajočimi se nabori podatkov**.