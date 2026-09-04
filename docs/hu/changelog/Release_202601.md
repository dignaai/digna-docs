---
title: digna 2026.01 kiadás | Logikai adatforrások, globális kapcsolatok és fejlett Data Validation
description: Ismerd meg, mi újság a digna 2026.01 kiadásában. Ez a verzió bevezeti a globális adatbázis-kapcsolatokat, logikai adatforrásokat, anomália relevancia feltételeket, CSV exportokat és fejlett adatellenőrzést, beleértve a referenciális integritás-ellenőrzéseket.
keywords: digna 2026.01 kiadás, digna changelog, digna adatforrás, digna adatbázis-kapcsolatok, digna Data Anomalies, digna Data Validation, referenciális integritás ellenőrzés, adatminőségi szabályok, adatmegfigyelés, digna CSV export
image: /assets/logo_square.png
---

# Changelog – Release 2026.01  

A 2026.01 kiadással a digna jelentős fejlesztéseket vezet be az adatforrás-modellezésben, a kapcsolatok kezelésében és az ellenőrzések használhatóságában.  
Ez a kiadás növeli a rugalmasságot az összes modulban, és jelentősen kiterjeszti a **adatminőség és validáció lefedettségét**.

---

## Új funkciók  

### Globális adatbázis-kapcsolatok  
- Az adatbázis-kapcsolatok mostantól **globális szinten** konfigurálhatók.  
- A globális kapcsolatok újrahasznosíthatók **minden projektben**, egyszerűsítve a beállítást és karbantartást.  
- **Hatás:** Csökkenti az üzemeltetési terheket és biztosítja a konzisztens kapcsolódást különböző környezetekben.

### Több forráskapcsolat projektenként  
- A projektek mostantól hivatkozhatnak **több forráskapcsolat-konfigurációra**.  
- Lehetővé teszi a rugalmasabb beállításokat összetett adatlandscape-ek számára.  
- **Hatás:** Támogatja a valós vállalati architektúrákat heterogén adathalmazokkal.

### Logikai adatforrások  
- Az adatforrások mostantól egy projektben **logikai réteget** képviselnek.  
- Minden adatforrás mögött állhat:
    - egy **adatbázis-tábla**
    - egy **adatbázis-view**
    - egy **egyedi SQL lekérdezés**  
- Ez a szétválasztás javítja az újrafelhasználhatóságot, az átláthatóságot és az ellenőrzések modellezését a modulok között.  
- **Hatás:** Szétválasztja az ellenőrzéseket és adatminőségi szabályokat a fizikai tárolástól, javítva a karbantarthatóságot és az újrafelhasználhatóságot.

### Anomália relevancia feltétel  
- Mostantól definiálható egy **Anomaly Relevance Condition**, amely szabályozza az anomália státusz értékelését adathalmaz-szinten.  
- A statisztikákat függetlenül számítjuk, attól, hogy a feltétel be van-e állítva vagy teljesül-e.  
- Ha a feltétel **nem teljesül**, a **Data Anomalies** nem ad anomália státuszt (zöld / sárga / piros).  
- **Példa:** Zárd ki az adathalmazt az anomália értékelésből, ha a rekordok száma 10 alatt van.
- **Hatás:** Biztosítja, hogy az anomáliák csak releváns üzleti kontextusban legyenek értékelve.

### Modulonkénti értesítési konfiguráció  
- Az értesítések mostantól **modulonként** konfigurálhatók közvetlenül a digna felületén.  
- Lehetővé teszi az riasztási viselkedés független szabályozását a **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** és más modulok számára.  
- **Hatás:** Pontos riasztási stratégiákat tesz lehetővé, amelyek igazodnak a csapatok felelősségéhez és a kritikalitáshoz.

### Ellenőrzési eredmények exportja (CSV)  
- A felhasználók mostantól **letölthetik az ellenőrzési eredményeket CSV fájlokként**.  
- Lehetővé teszi az offline elemzést, jelentést és integrációt külső eszközökkel.  
- **Hatás:** Egyszerűsíti az auditokat, jelentéskészítést és a későbbi adatminőségi elemzést.

---

## Kiterjesztett Data Validation képességek  

Ezzel a kiadással a **Data Validation** mostantól átfogó adatminőségi szabálykészletet támogat:

- **Sor-szintű validációs szabályok**  
- **Többoszlopos egyediség ellenőrzések**  
- **Referenciális integritás ellenőrzések adatforrások között**

Ezek a vizsgálatok együtt lehetővé teszik a **strukturális és relációs adatminőségi szabályok** érvényesítését összetett adatrendszerekben.

### Többoszlopos egyediség-ellenőrzések
- Bevezetésre kerültek a **Uniqueness Checks** konfigurálható **oszlopkészletre**.  
- Lehetővé teszi kombinált kulcsok és üzleti szintű egyediség érvényesítését.  
- **Hatás:** Felismeri az olyan duplikált üzleti entitásokat, amelyeket egyetlen oszlop-ellenőrzéssel nem lehet azonosítani.

### Referenciális integritás ellenőrzések
- Bevezetésre kerültek a **Referential Integrity Checks**, amelyek ellenőrzik az adatforrások közötti kapcsolatokat.  
- Biztosítja, hogy a forrás adatforrásban található **külső kulcs értékek** létezzenek a hivatkozott cél adatforrásban.  
- Segít korán felismerni az árva rekordokat, megszakadt kapcsolatokat és az adatok konzisztenciájával kapcsolatos problémákat.  
- Úgy tervezték, hogy működjön a **logikai adatforrásokkal**, beleértve a view-kat és az egyedi SQL-t is.  
- **Használati esetek:** adattárház integritás, szabályozási jelentések, master adat-konzisztencia és megbízható downstream analitikák.

---

## Kiknek előnyös ez a kiadás  

- **Data Engineers:** Rugalmasabb adatforrás-modellezés és újrahasználható adatbázis-kapcsolatok  
- **Data Quality & Governance csapatok:** Bővített validációs lefedettség, beleértve a relációs integritási szabályokat  
- **Analytics & BI csapatok:** Tisztább bemenetek és exportálható ellenőrzési eredmények  
- **Platform tulajdonosok:** Csökkentett konfigurációs komplexitás és javított üzemeltethetőség

---

## CLI frissítések  
- Nincs változás

---