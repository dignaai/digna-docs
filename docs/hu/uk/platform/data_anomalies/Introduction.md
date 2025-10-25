---
title: Data Anomalies – Automatikus észlelés | digna dokumentáció
description: Tudja meg, hogyan észleli a digna Data Anomalies automatikusan a forgalomcsökkenéseket, hiányzó értékeket, eloszláseltolódásokat és váratlan mintákat manuális szabályok nélkül. Javítsa az adatok minőségét MI-alapú anomáliaészleléssel.
---

# Data Anomalies – Automatikus észlelés

## Cél
Észleljen anomáliákat szabályok írása nélkül.

## Technikai képességek
### Elemezett metrikák
- Rekordok mennyisége  
- Hiányzó értékek  
- Eloszlások és hisztogramok  
- Értéktartományok  
- Egyediség  

### Intelligens észlelés
- Használja a **történeti adatokon történő tanulást** az elvárt határok dinamikus meghatározásához  
- Jelöli az anomáliákat, amikor a tényleges adatok kilépnek az elvárt tartományból  

## Észlelési forgatókönyvek
- **Forgalom csökkenése/kiugrása** → például a napi tranzakciók fele hiányzik  
- **Oszlopok összekeveredése** → az «keresztnév» és «vezetéknév» oszlop felcserélődött  
- **Váratlan értékek** → «Zurich» megjelenik az osztrák városok listájában  

## Előny
Automatizálja azt, ami általában több száz kézi szabályt igényelne.