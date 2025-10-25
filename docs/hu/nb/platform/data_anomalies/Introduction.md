---
title: Data Anomalies – Automatikus észlelés | digna dokumentáció
description: Fedezze fel, hogyan észleli a digna Data Anomalies automatikusan a volumencsökkenéseket, hiányzó értékeket, eloszláseltolódásokat és váratlan mintázatokat manuális szabályok nélkül. Javítsa az adatok minőségét AI-vezérelt anomáliaészleléssel.
---

# Data Anomalies – Automatikus észlelés

## Cél
Anomáliák észlelése szabályok megírása nélkül.

## Technikai jellemzők
### Elemzett metrikák
- Rekordok száma  
- Hiányzó értékek  
- Eloszlások & hisztogramok  
- Értéktartományok  
- Egyediség  

### Intelligens észlelés
- Használja a **történeti tanulást** a várható intervallumok dinamikus meghatározásához  
- Jelöli az anomáliákat, ha a tényleges adatok kívül esnek a várható határokon  

## Észlelési forgatókönyvek
- **Volumcsökkenés/növekedés** → pl. a napi tranzakciók felének hiánya  
- **Oszlopok felcserélve** → a keresztnév- és vezetéknév-oszlopok felcserélődtek  
- **Váratlan értékek** → “Zurich” megjelenik osztrák városok között  

## Előny
Automatizálja azt, ami normálisan több száz manuális szabályt igényelne.