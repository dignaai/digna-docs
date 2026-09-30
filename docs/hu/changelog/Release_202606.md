---
title: digna kiadás 2026.06 | Python SDK, Docker telepítés és továbbfejlesztett érvényesítés-kezelés
description: Ismerd meg, mi újság a digna 2026.06-os kiadásában. Ez a verzió bemutatja az új digna Python SDK-t, a Docker telepítési támogatást, az átdolgozott dashboard élményt és a bővített import/export lehetőségeket az érvényesítési szabályok kezeléséhez.
keywords: digna kiadás 2026.06, digna Python SDK, digna Docker támogatás, adatminőség automatizálás, adatprofilozás, érvényesítési szabály import export, digna dashboard, adatmegfigyelési platform, Python API, metaadat automatizálás
image: /assets/logo_square.png
---

# Változáslista – Kiadás 2026.06  

A 2026.06-os kiadással a digna jelentős előrelépést tesz az automatizálás, az bővíthetőség és a platform használhatósága terén.  
Ez a verzió bemutatja az új **digna Python SDK**-t, a hivatalos **Docker telepítési támogatást**, egy megújult dashboard élményt és a továbbfejlesztett hordozhatóságot az érvényesítési szabályok kezelésében.

---

## Nézze meg a kiadást

<!--YOUTUBE EMBED START--><div style="position: relative; padding-bottom: 56.25%; height: 0; width: 100%;"><iframe src="https://www.youtube-nocookie.com/embed/g6ZQl9pc4vg" title="What&#39;s New in digna | The Major Release of 2026" frameborder="0" loading="lazy" allowfullscreen allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div><!--YOUTUBE EMBED END-->

*[What's New in digna | The Major Release of 2026](https://www.youtube.com/watch?v=g6ZQl9pc4vg) — áttekintés erről a kiadásról a digna YouTube-csatornáján.*

---

## Új funkciók  

### digna Python SDK – Automatizálj mindent Pythonnal  
- Telepítés:
  ```bash
  pip install digna-sdk
  ```
- A digna programozott kezelése és automatizálása Python segítségével  
- Projektek létrehozása és konfigurálása kódból  
- Inspekciók és monitorozási futtatások indítása  
- Adatkészletek, szabályok és konfigurációk programozott kezelése  
- Táblák profilozása és metaadat-információk kinyerése  
- Profilozási és adatminőségi eredmények exportálása külső tárolókba és rendszerekbe  
- Integráció notebookokkal, orchestration eszközökkel és CI/CD pipeline-okkal  

Hatás: Lehetővé teszi az infrastruktúra teljes körű kódalapú kezelését és az adatminőség- valamint megfigyelési munkafolyamatok mély automatizálását Python segítségével.

---

### Docker támogatás – Egyszerűsített telepítés és üzemeltetés  
- Hivatalos Docker image támogatás a digna számára  
- Gyors és következetes beállítás különböző környezetekben  
- Egyszerűbb onboarding fejlesztéshez, teszteléshez és éles környezethez  
- Könnyű integráció Kubernetes-szel és egyéb konténerplatformokkal  
- Javított hordozhatóság és reprodukálhatóság a telepítésekben  

Hatás: A digna egyszerűbben telepíthető és üzemeltethető modern, cloud-native architektúrákban.

---

### QueryMode – Rugalmas SQL-végrehajtási stratégia

Állítsd be a lekérdezés-végrehajtási stratégiát: **Single** vagy **Combined** mód

**Single Mode**: Minden statisztika külön, dedikált SQL lekérdezéssel számolódik

  - Ideális nagy adatforrásokhoz, ahol memória-korlátok jelentősek
  - Megakadályozza a kombinált lekérdezések erőforrás-kimerülését (memória túlcsordulás, spool limit)
  - Több lekérdezés, de alacsonyabb lekérdezésenkénti memóriaigény

**Combined Mode**: Minden statisztika egyetlen SQL lekérdezésben kerül kiszámításra

  - Csökkenti a lekérdezések összszámát és a hálózati overhead-et
  - Teljesítmény-optimalizálás olyan esetekben, amikor az adatforrások kezelhetők memóriában
  - Hatékonyabb gyakori, párhuzamos futtatásoknál

Hatás: Finomhangolási lehetőséget ad a lekérdezés-végrehajtás felett, hogy a felhasználók az adatforrás jellemzői alapján egyensúlyozhassanak teljesítmény, erőforrás-használat és memória-biztonság között.

---

### Konfigurálható előrejelzési modell

Az anomáliadetektálás mögötti modell mostantól minden sorozatnál egymással versengő magyarázatokat mérlegel – egy mintázatot a legutóbbi megfigyelések értelmezésével kombinálva –, és előrejelzéseiket aszerint vegyíti, mennyire erősen támasztja alá őket az adat. Egyetlen szélsőséges érték már nem szivároghat át a következő előrejelzésekbe.

Az adatforrás új **Model** lapján két beállítás irányítja, mindkettő `0.0` és `1.0` között állítható, az alapértelmezés `0.5`:

- **Break Sensitivity** – milyen gyorsan fogadja el a modell egy új szintre ugrást vagy egy forduló trendet ahelyett, hogy kiugró értékeknek tekintené
- **Model Complexity** – mennyi struktúrát keres a modell: a naptári hatásoktól és egyetlen szinteltolódástól egészen az ismeretlen ciklusokig, a hónap napjaihoz kötött hatásokig és a havi nullázódásokig

Mindkettő bármikor visszaállítható az alapértelmezett értékére. Hogy melyik hogyan hat, lásd: [Modellbeállítások](../platform/data_anomalies/how_it_works.md#model-settings).

Hatás: Az eddigi, tűréssávra vonatkozó Sensitivity és Memory beállítások mellett – amelyek mostantól a **Thresholds** lapon találhatók – magát az előrejelzési modellt is a felhasználó kezébe adja.

---

### Anomália-értesítések szabályozása

- Új **Notifications** lap az adatforrás anomáliabeállításai között:
  - **Minimum Alerts** – hány sikertelen ellenőrzés (a bizonytalanok nem számítanak) szükséges egy inspekcióban ahhoz, hogy értesítés menjen ki (alapértelmezés: `1`)
  - **Pause After Notification (Days)** – mennyi ideig marad néma egy feliratkozás, miután értesített az adatforrásról (alapértelmezés: `0`, nincs szünet)
- A feliratkozók mostantól értesítést kapnak, ha egy inspekció teljes egészében meghiúsul (**Notify Inspection Errors**)
- Minden értesítés közvetlenül arra az oldalra mutat, amelyről szól – az inspekció sikertelen ellenőrzéseire, illetve a Schema Tracker és Timeliness nézetekre
- Egyértelműbb feliratkozási kapcsolók: **Notify on Passed Inspections**, **Notify Inspection Errors**, **Notify Data Volume Checks**

**Hogyan működnek az értesítések:** az értesítések **értesítési csatornákon** keresztül mennek ki – Email (SMTP-kapcsolaton keresztül), Slack vagy Jira –, amelyeket az adminisztrátorok állítanak be, és a **Test Notification Channel** funkcióval ellenőrizhetnek. Egy **feliratkozás** egy csatornát kapcsol egy projekthez: az összes adatforrásra vagy csak a kiválasztottakra vonatkozik, kapcsolói pedig meghatározzák, miről tájékoztat – az egyes modulokról (Data Anomalies, Data Validation, Data Analytics, Timeliness, Schema Tracker és az adatmennyiség-ellenőrzések), a teljes egészében meghiúsuló inspekciókról, és igény szerint a sikeres inspekciókról is.

Hatás: Kevesebb, de hasznosabb értesítés – az elszigetelt eltérések és a tartósan fennálló anomáliák többé nem árasztják el a csatornát.

---

### Átdolgozott dashboard élmény  
- Modernizált és javított UI/UX dizájn  
- Átláthatóbb navigáció és struktúra  
- Jobb láthatóság a monitorozási eredmények és adatminőségi betekintések számára  
- Javított olvashatóság riasztások, statisztikák és dashboardok esetén  
- Gyorsabb hozzáférés a kulcsfontosságú üzemeltetési információkhoz  

Hatás: Javítja a használhatóságot és a napi termelékenységet minden felhasználó számára.

---

### Bővített import & export az érvényesítési szabályokhoz  
- Kiterjesztett import/export funkcionalitás az érvényesítési szabályokhoz  
- Könnyebb migráció környezetek és projektek között  
- Standardizált szabálykészletek jobb újrafelhasználhatósága  
- Jobb governance és szabály-életciklus kezelése  
- Egyszerűsített együttműködés csapatok között  

Hatás: Lehetővé teszi az adatminőség skálázható és következetes irányítását szervezeti szinten.

---

## Platform fejlesztések  

- Teljes Python SDK integráció az automatizáláshoz  
- Konténeres telepítés Dockerrel  
- Javított UX az átdolgozott dashboardon keresztül  
- Kibővített hordozhatóság az érvényesítési logika számára  

---

## Kiknek hasznos ez a kiadás  

- Data Engineers: automatizálás, SDK használat, pipeline integráció  
- Platform csapatok: egyszerűsített telepítés Dockerrel  
- Data Governance csapatok: újrahasználható érvényesítési szabálykezelés  
- Analytics csapatok: jobb használhatóság és betekintés- láthatóság  

---

## CLI frissítések  
- SDK integráció támogatás hozzáadva  
- Javított import/export munkafolyamatok  
- Általános stabilitás- és teljesítményjavítások