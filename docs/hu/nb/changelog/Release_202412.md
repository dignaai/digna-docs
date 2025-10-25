---
title: digna Release 2024.12 | Változásnapló és új funkciók
description: Ismerje meg, mi újság a digna Release 2024.12-ben. Ez a kiadás beépített ütemezőt, PDF-jelentéskészítést, rugalmas egyedi oszloptípusokat, dinamikus helyőrzőket snapshot-lekérdezésekben és intelligensebb küszöboptimalizálást vezet be az anomáliaészlelés és az adathatékonyság javítására.
keywords: digna Release 2024.12, digna változásnapló, kiadási jegyzetek, beépített Scheduler, PDF-jelentések, egyedi oszloptípus, snapshot-lekérdezés helyőrzők, küszöboptimalizálás, data observability, adatok minőségellenőrzése, anomáliaészlelés
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Változásnapló – Release 2024.12

A Release 2024.12 új funkciók és fejlesztések sorát tartalmazza, amelyek automatizáltabbá, rugalmasabbá és üzletre készebbé teszik a dignát.  
Ez a verzió javítja az ütemezést, jelentéskészítést, lekérdezéskezelést és az anomáliaészlelés pontosságát.  

---

## Új funkciók

### Beépített Scheduler
Az ellenőrzések már nem csak parancssorból vagy API-hívásokból indíthatók.  
Az új, beépített **digna Scheduler** segítségével az ellenőrzések automatikusan lefuthatnak meghatározott időpontokban.  

- Támogatja a **Cron**-kifejezéseket ismétlődő ütemezéshez (napi, heti vagy egyedi intervallumok).  
- Pontos vezérlést ad **offsetek**, **kezdődátumok** és **záródátumok** segítségével.  
- Lehetővé teszi a csapatok számára, hogy biztosítsák: minden kritikus adatforrást következetesen ellenőriznek manuális beavatkozás nélkül.  

---

### PDF-jelentések
A csapatok mostantól könnyedén megoszthatják az eredményeket az érintettekkel **PDF-exportok** segítségével.  

- Diagramok, metrikák és anomáliaeredmények professzionális PDF-formátumban exportálhatók.  
- A jelentések kombinálják a **vizualizációkat** és az **alapul szolgáló adatokat**, kiszolgálva mind a technikai, mind az üzleti felhasználókat.  
- Megszünteti a külső eszközök szükségességét a jelentéskészítéshez.  

---

### Új oszloptípus: `CUSTOM`
Nagyobb rugalmasság érdekében a digna bevezet egy új oszloptípust: **`CUSTOM`**.  

- A felhasználók meghatározhatják, pontosan mely **statisztikák és metrikák** legyenek alkalmazva adott attribútumokra.  
- Kiváló speciális esetekre, amelyek nem illeszkednek az olyan szabványos kategóriákhoz, mint a NUMERICAL vagy a CATEGORICAL.  
- Segít, hogy az elemzések fókuszáltak legyenek, és az eredmények relevánsak maradjanak az üzleti kontextusban.  

---

### Új helyőrzők a snapshot-lekérdezésekben
A snapshot-lekérdezések egyszerűbbé és kevésbé hibára hajlamossá válnak a **dinamikus helyőrzőkkel**.  

- A `#date+n#` vagy `#date-n#` tokenek automatikusan igazítják a dátumokat a lekérdezésekben.  
- Példa:  
  - `#date+1#` → holnap  
  - `#date-2#` → két nappal ezelőtt  
- Kizárja a manuális dátumszámításokat és biztosítja a következetességet a csapatok között.  

---

### Küszöboptimalizálás
Az anomália-küszöbök mostantól intelligensebbek és kontextusérzékenyek.  

- Olyan metrikák esetén, mint a **NULL COUNT**, az alsó küszöbök automatikusan korlátozottak **0**-ra.  
- Megakadályozza az érvénytelen vagy értelmetlen küszöbök beállítását.  
- Kevesebb hamis pozitívot és megbízhatóbb anomáliaészlelést eredményez.  

---

## Általános fejlesztések
- Javított **UI-összetevők** a projekt- és attribútumkonfigurációs nézetekben.  
- Jobb **dashboard teljesítmény** nagy adatmennyiségek esetén.  
- Kiterjedtebb **naplózás és hibaüzenetek** a hibaelhárításhoz.  

---

## Összefoglaló
A Release 2024.12 megerősíti a dignát, mint a **adatminőség, anomáliaészlelés és data observability** platformját.  
Az ütemezés általi automatizálással, megosztható PDF-jelentésekkel, testreszabható oszlopokkal, egyszerűsített snapshot-lekérdezésekkel és okosabb küszöbökkel a digna még értékesebbé válik mind a technikai felhasználók, mind az üzleti érdekeltek számára.