---
title: Data Anomalies – Automatikus észlelés | digna Dokumentáció
description: Fedezze fel, hogyan észleli a digna Data Anomalies automatikusan a volumencsökkenéseket, hiányzó értékeket, eloszlásváltozásokat és váratlan mintázatokat kézi szabályok írása nélkül. Javítsa az adatminőséget mesterséges intelligenciával támogatott anomáliaészleléssel.
---

# Data Anomalies – Automatikus észlelés

## Cél
Anomáliák észlelése szabályok írása nélkül.

## Műszaki jellemzők
### Elemzett metrikák
- Adatmennyiség  
- Hiányzó értékek  
- Eloszlások és hisztogramok  
- Értéktartományok  
- Egyediség  

### Intelligens észlelés
- A várt tartományok dinamikus meghatározásához **történeti adatokból tanulást** használ  
- Ha a valós adatok a várt határokon kívül esnek, anomáliaként jelöli őket  

## Észlelési forgatókönyvek
- **Adatmennyiség csökkenései/kiugrásai** → pl. a napi tranzakciók felének hiánya  
- **Oszlopok felcserélődése** → pl. a keresztnév és vezetéknév oszlopok felcserélődése  
- **Váratlan értékek** → pl. osztrák városok között megjelenik a “Zurich”  

## Előny
Általában több száz kézi szabályt igénylő feladatokat automatizálja.