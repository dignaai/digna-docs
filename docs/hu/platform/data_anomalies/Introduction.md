---
title: Data Anomalies – Automatizált észlelés | digna Dokumentáció
description: Fedezze fel, hogyan észleli a digna Data Anomalies automatikusan a volumencsökkenéseket, hiányzó értékeket, eloszlásváltozásokat és váratlan mintákat manuális szabályok nélkül. Javítsa az adatok minőségét AI-vezérelt anomáliaészleléssel.
---

# Data Anomalies – Automatizált észlelés

## Cél
Anomáliák észlelése szabályok írása nélkül.

## Technikai jellemzők
### Elemzett metrikák
- Rekordok volumene  
- Hiányzó értékek  
- Eloszlások & hisztogramok  
- Értéktartományok  
- Egyediség  

### Intelligens észlelés
- A **történeti tanulást** használja az elvárt tartományok dinamikus meghatározására  
- Jelöli az anomáliákat, ha a tényleges adatok kívül esnek az elvárt határokon  

## Észlelési forgatókönyvek
- **Forgalomcsökkenések/kiugrások** → pl. a napi tranzakciók felének hiánya  
- **Oszlopok felcserélése** → a keresztnév és vezetéknév oszlop felcserélődése  
- **Váratlan értékek** → “Zurich” megjelenése osztrák városok között  

## Előny
Automatizálja azt, ami normálisan több száz kézi szabályt igényelne.