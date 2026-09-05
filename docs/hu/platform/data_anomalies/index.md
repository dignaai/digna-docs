---
title: digna Data Anomalies | AI-alapú megfigyelhetőség az adatokhoz
description: A digna Data Anomalies a digna Data Observability Platform része. Automatikusan megtanulja az adatmintákat és anomáliákat észlel, javítva ezzel az adatok minőségét és megfigyelhetőségét adatbázisokban, data lake-ekben és adattárházakban.
tags:
  - adatminőség
  - adatmegfigyelhetőség
  - adatok minősége
  - adatok megfigyelhetősége
  - MI-vezérelt megfigyelés
  - anomáliaészlelés
  - digna
  - digna platform
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – AI-alapú adatminőségi problémák észlelése

**AI-alapú megfigyelhetőség az állandó adatbizalomért**

A digna Data Anomalies a **digna Data Observability Platform** része — egy moduláris megoldás, amely folyamatosan elemzi az adatkészletek viselkedését az időben, és ezáltal javítja az **adatok minőségét**.

Automatikusan megtanulja, hogy mi a „normális” az adataidban, és riaszt, amikor a viselkedés megváltozik — statikus küszöbszintek meghatározása vagy egyetlen szabály írása nélkül.  
A modul közvetlenül az adatbázisban fut, így az adatok soha nem hagyják el a környezetedet.

---

## A digna Data Anomalies célja

A **digna Data Anomalies** modul folyamatos **adatmegfigyelhetőséget** biztosít előre definiált statisztikai metrikák kiszámításával és nyomon követésével, mint például:

- Adatmennyiség és rekordszámok  
- Hiányzó értékek aránya  
- Értékeloszlások és hisztogramok  
- Numerikus tartományok és átlagok  
- Oszlopok egyedisége és szöveg hosszúsága  

Ezeket a metrikákat minden adatkészletre automatikusan gyűjtjük.  
Ezek alapján a digna modelleket épít, amelyek jellemzik az egyes metrikák tipikus viselkedését — naponta, heti vagy szezonális minták szerint tanulva.  
Az edzés után a modul előrejelzi az új adatok várható értékeit és észleli az eltéréseket, amelyek minőségi problémára, folyamathibára vagy upstream változásokra utalhatnak.

---

## Fő képességek

- AI segítségével automatikusan megtanulja a várt adatviselkedést — nincs szükség küszöbök konfigurálására.  
- Észleli a hirtelen csökkenéseket, belövéseket vagy eltolódásokat az adatmennyiségben és eloszlásokban.  
- Felismeri az átcserélt oszlopokat vagy helytelen attribútumtérképezéseket.  
- Kiemeli a váratlan kategóriás értékeket (pl. új régiók vagy kódok).  
- Támogat minden oszloptípust: numerikus, kategóriás vagy nem meghatározott.  
- Teljes mértékben az ügyfél környezetében működik — nincs adatmigráció.  
- Integrálható a **digna Data Analytics**-szel hosszú távú trendanalízishez.

---

## Működési elv

### 1. lépés – Metrika számítás
A digna profil metrikák halmazát számítja ki minden táblára és oszlopra.  
Ezek a metrikák leírják az adataid szerkezetét és statisztikai viselkedését, és tárolódnak a további elemzéshez.

### 2. lépés – Modell tanítás
A metrikaértékek történeti adatai alapján a digna kompakt gépi tanulási modelleket (signature models) tanít, amelyek leképezik az egyes metrikák normál tartományát.

### 3. lépés – Automatikus küszöbölés
*conformal inference* használatával a digna adaptív konfidencia intervallumokat (auto-thresholds) számít, amelyek együtt változnak az adataiddal.  
Ha új metrikaértékek kívül esnek a várt tartományon, anomáliaként jelöljük őket.

Ez a folyamatos visszacsatolási kör biztosítja, hogy a monitorozás releváns maradjon még akkor is, ha az adatmennyiségek vagy minták természetesen változnak.

---

## Példaszcenáriók

### Váratlan csökkenés a rekordmennyiségben
Egy adatkészlet jellemzően napi körülbelül 500 000 rekordot tartalmaz.  
Amikor egy új feltöltés csak 50 000 rekordot hoz, a digna anomáliát jelez, és megmutatja, mennyire tér el az érték a megtanult tartománytól.

### Átcserélt oszlopok észlelése
A `last_name` átlagos karakterhossza hirtelen megegyezik a `first_name` értékével.  
A digna felismeri a metrikák mintázatának eltérését, és potenciális oszlopcserét jelez.

### Váratlan kategória észlelése
Egy oszlop, amely osztrák városokat listáz, hirtelen „Zurich” értéket tartalmaz.  
A történeti eloszlások alapján a digna a új értéket váratlanként jelöli és riasztást küld.

---

## Integráció más modulokkal

- **digna Data Analytics** — összegzi az anomália történetet és volatilitási metrikákat a hosszú távú trendek feltárásához.  
- **digna Data Validation** — explicit üzleti szabályokat érvényesít determinisztikus minőségellenőrzéshez.  
- **digna Data Timeliness** — figyeli az adatok érkezési idejét és korrelálja a késéseket az anomáliák előfordulásával.  
- **digna Data Schema Tracker** — detektálja a szerkezeti változásokat, amelyek magyarázatot adhatnak új anomáliákra.

---

## Tipikus felhasználási esetek

- Hiányzó vagy duplikált adathalmazok észlelése.  
- Átcserélt vagy levágott oszlopok azonosítása.  
- Eloszláselmozdulás észlelése numerikus vagy kategóriás jellemzőkben.  
- Váratlan referenciaértékek vagy kódok felderítése.  
- Folyamatos betöltési csatornák monitorozása rendellenességekért.  
- Az adatok általános **minőségének és megfigyelhetőségének** nyomon követése több doménben.

---

## Előnyök

- Azonnali észlelés a rendellenes adatviselkedésre.  
- Kézi küszöbhangolás megszüntetése.  
- Csökkenti az üzemeltetési erőfeszítést nagy adatkörnyezetekben.  
- Növeli az analitikai és riportálási rendszerek megbízhatóságát.  
- Erősíti az **adatok minőségét** és az end-to-end **adatmegfigyelhetőséget**.

---

## Kapcsolódó digna modulok

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trend- és volatilitási metrikák.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — szabályalapú adatellenőrzés.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — adatszállítási ütemtervek monitorozása.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — sémaváltozások észlelése.

---

## Összefoglalás

A **digna Data Anomalies** modul a digna AI-vezérelt **Data Observability Platform** magját képezi.  
A kulcsmetrikák folyamatos monitorozásával, minták tanulásával és eltérések azonosításával segít a szervezeteknek abban, hogy az **adatok minősége** megbízható, stabil és magyarázható maradjon — manuális konfiguráció nélkül.