# Változáslista – Kiadás 2026.06  

A 2026.06-os kiadással a digna jelentős előrelépést tesz az automatizálás, az bővíthetőség és a platform használhatósága terén.  
Ez a verzió bemutatja az új **digna Python SDK**-t, a hivatalos **Docker telepítési támogatást**, egy megújult dashboard élményt és a továbbfejlesztett hordozhatóságot az érvényesítési szabályok kezelésében.

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