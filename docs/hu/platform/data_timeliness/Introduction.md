---
title: Data Timeliness – Időben történő kézbesítés figyelése | digna Dokumentáció
description: Ismerje meg, hogyan biztosítja a digna Data Timeliness, hogy az adatok a vártnak megfelelően érkezzenek. Észlelje a késői vagy hiányzó kézbesítéseket, figyelje az SLA-kat, és védje az üzleti folyamatokat a néma késésektől. MI-alapú észlelés a jobb adatminőségért és a csővezetékek megfigyelhetőségéért.
image: /assets/logo_square.png
keywords:
  - adatok időszerűsége
  - kézbesítés figyelése
  - adatminőség
  - adatok minősége
  - adatok megfigyelhetősége
  - késői adatok észlelése
  - hiányzó adatok riasztása
  - sla monitoring
  - ai delivery analysis
  - digna data timeliness
lang: hu
robots: index, follow
og_title: Data Timeliness – Időben történő kézbesítés figyelése | digna Dokumentáció
og_description: A digna Data Timeliness automatikusan észleli a késve vagy hiányosan megérkező adatkiszállításokat MI segítségével. Védje az üzleti folyamatokat, figyelje az SLA-k betartását, és biztosítsa az adatok időbeniségét és megbízhatóságát minden csővezetékben.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI-Driven Data Timeliness Module for Data Quality and Observability – digna</h1>

---

## Cél

A **Data Timeliness** modul biztosítja, hogy az **adatok időben érkezzenek** — minden alkalommal.  
Folyamatosan figyeli a kézbesítési ütemezéseket, és automatikusan észleli, amikor adatállományok, táblák vagy fájlok **késnek, hiányoznak vagy hiányosak**.  

A felhasználó által meghatározott ütemezéseket és a MI-alapú tanulást kombinálva a *digna* lehetővé teszi a szervezetek számára, hogy megelőzzék a lefelé irányuló hibákat és betartsák a szigorú **SLA (Service Level Agreement)** célokat mind az **adatminőség**, mind az **adatcsővezetékek megfigyelhetősége** tekintetében.

---

## Technikai áttekintés

### Kettős figyelési módok
- **MI által megtanult érkezési minták**  
  A digna automatikusan megtanulja az adatszállítók természetes ritmusát — napi, óránkénti vagy eseményvezérelt — a korábbi időbélyegek és befejezési idők elemzésével.  
  Alkalmazkodik az üzleti naptárak változásaihoz, a hétvégéhez vagy a hónapvégi csúcsokhoz.

- **Felhasználó által definiált ütemezések**  
  A felhasználók explicit módon definiálhatják a várt kézbesítési időket (pl. *minden hétköznap 7:30 előtt*).  
  A digna összehasonlítja a tényleges érkezési időt a tervezett ütemezéssel, és riasztást küld, ha az adatok késnek vagy hiányoznak.

### Észlelési mechanizmus
- Értékeli a **metaadat időbélyegeket**, **rekordszámokat** és a **tábla frissességét**  
- Észleli a **megrekedt ETL-feladatokat**, **sikertelen kinyeréseket** és a **részleges fájlkézbesítéseket**  
- Integrálódik a *Data Anomalies* és a *Data Validation* modulokkal a kombinált betekintés érdekében

---

## Észlelési forgatókönyvek

| Forgatókönyv | Leírás |
|-----------|--------------|
| **Késő adatérkezés** | A napi piaci adatok két órát késnek, ami miatt a riportok nem teljesítik az SLA-kat |
| **Hiányzó betöltés** | Egy ütemezett tábla vagy partíció nincs frissítve a jelenlegi dátumra |
| **Láncolt függőség késése** | Egy felülről érkező feladat késése hatással van a lefelé haladó csővezeték frissítésére |
| **Hétvégi mintaeltolódás** | Az MI modell automatikusan alkalmazkodik, ha vasárnaponként nem várható adat |

---

## Architektúra és végrehajtás

- **Adatbázison belüli végrehajtás:** a digna a timeliness ellenőrzéseket közvetlenül az Ön adatbázisában vagy adat-tárházában futtatja.  
- **Könnyű metaadat-hozzáférés:** olvassa a feladatok időbélyegeit, rekordszámokat és partícióinformációkat — nincs szükség adatkinyerésre.  
- **Konfigurálható gyakoriság:** ütemezze a figyelést dataset, séma vagy csővezeték szerint.  
- **Modulok közötti riasztások:** az eredmények vizuális figyelmeztetéseket indíthatnak a *Inspection Hub*-ban vagy értesítéseket küldhetnek e-mailen, Slack-en vagy API-n keresztül.  

---

## Példák a felhasználásra

- **Pénzügyi piaci adatok:** késések észlelése ár- vagy kereskedési adatok frissítéseiben.  
- **Adatraktár betöltések:** figyelje, ha az éjszakai ETL-feladatok később fejeződnek be, mint várható.  
- **Adatmegosztás csapatok között:** biztosítsa, hogy az osztályok közötti adatszállítások a napi határidők előtt megtörténjenek.  
- **Szabályozói jelentések:** ellenőrizze, hogy a benyújtások a legfrissebb adatszeletet tartalmazzák-e.

---

## Előnyök

| Terület | Előny |
|------|----------|
| **Üzletmenet-folytonosság** | Megakadályozza az működési zavarokat a késő vagy hiányzó adatok miatt |
| **Adatminőség** | Javítja az adatszállítmányok megbízhatóságát és következetességét |
| **Megfelelés** | Biztosítja az SLA-k betartását és az auditálhatóságot |
| **Automatizáció** | Az MI kiküszöböli a kézi ütemezéskövetést |
| **Integráció** | Zökkenőmentesen működik együtt a *Data Analytics*-szel, hogy időbeli timeliness trendeket jelenítsen meg |

---

## Hogyan tanulja meg a digna a várt kézbesítési időket

1. **Történeti elemzés:** a digna megfigyeli a korábbi betöltési időket és tartamokat.  
2. **MI modellezés:** a gépi tanulás dinamikus alapvonalat hoz létre a várt érkezéshez.  
3. **Monitoring:** minden új kézbesítést összehasonlítanak az alapvonallal.  
4. **Riasztás:** a eltérések riasztásokat váltanak ki kontextuális metrikákkal és megbízhatósági pontszámokkal.  

Ez a folyamatos tanulási megközelítés alkalmazkodik a változó folyamatokhoz, miközben alacsonyan tartja a téves pozitívokat.

---

## GYIK

**Megadhatok saját kézbesítési időket?**  
Igen. A digna támogatja mind a fix felhasználói ütemezéseket, mind az MI által megtanult mintákat.

**Integrálható az ETL vagy orkesztrációs eszközömmel?**  
Igen. A digna integrálható olyan eszközökkel, mint az Airflow, dbt, Informatica vagy egyedi ütemezők.

**Hol történik a számítás?**  
Az összes elemzés az Ön adatbázisában vagy felhő-tárházában fut — nincs külső szolgáltatás használatban.

**Mi történik, ha az adatok késnek?**  
A digna riasztásokat küld a dashboardon, az Inspection Hub-ban, valamint API/webhookokon keresztül, hogy az üzemeltetési csapatokat azonnal értesítse.

---


A **digna Data Timeliness** segít biztosítani az **adatokba vetett bizalmat**, ötvözve az **MI-alapú észlelést**, a **helyszíni végrehajtást** és az **adatmegfigyelhetőséget** — mindezt az Ön kontrollált környezetén belül.