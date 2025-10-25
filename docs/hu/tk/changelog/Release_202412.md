---
title: digna Verzió 2024.12 | Változások és Újdonságok
description: Fedezze fel, mi újság a digna 2024.12 verziójában. Ez a kiadás beépített ütemezőt, PDF-jelentéseket, rugalmas egyedi oszlopokat, dinamikus snapshot lekérdezési helyőrzőket és anomáliafelismerést hoz, valamint intelligensebb küszöboptimalizálást az adatminőség-ellenőrzéshez.
keywords: digna Verzió 2024.12, digna változásnapló, kiadási megjegyzések, beépített ütemező, PDF-jelentések, CUSTOM oszloptípus, snapshot lekérdezés helyőrzők, küszöboptimalizálás, adatok megfigyelhetősége, adatminőség-ellenőrzés, anomáliafelismerés
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Változások – Verzió 2024.12

A 2024.12 verzió új funkciókat és fejlesztéseket hoz, amelyek a dignát automatikusabbá, rugalmasabbá és üzleti használatra készebbé teszik.  
Ez a kiadás javítja az ütemezést, a jelentéskészítést, a lekérdezés-feldolgozást és az anomáliafelismerés pontosságát.  

---

## Újdonságok

### Beépített ütemező
Az ellenőrzések már nem csak parancssori vagy API-hívásoktól függenek.  
Az új **digna Scheduler** segítségével az ellenőrzések a megadott időpontokban automatikusan futtathatók.  

- Ismétlődő ütemezések (napi, heti vagy egyéni intervallumok) esetén támogatja a **Cron kifejezéseket**.  
- **Offsets**, **kezdő dátumok** és **befejezési dátumok** segítségével finom, pontos vezérlést tesz lehetővé.  
- Biztosítja, hogy a csapatok minden kritikus adatforrást következetesen és manuális beavatkozás nélkül ellenőrizzenek.  

---

### PDF formátumú jelentések
A csapatok mostantól könnyen megoszthatják az eredményeket az érintettekkel **PDF-exportokkal**.  

- Grafikonok, metrikák és anomáliaeredmények professzionális PDF-formátumban exportálhatók.  
- A jelentések egyesítik a **vizualizációkat** és az **infrastruktúra-adatokat**, hogy mind a technikai, mind az üzleti felhasználóknak megfeleljenek.  
- Megszünteti a külső eszközök iránti igényt a jelentéskészítéshez.  

---

### Új oszloptípus: `CUSTOM`
A nagyobb rugalmasság érdekében a digna bemutat egy új **`CUSTOM` oszloptípust**.  

- A felhasználók pontosan meghatározhatják, hogy mely **statisztikák és metrikák** alkalmazandók egy adott attribútumra.  
- Ideális olyan speciális esetekhez, amelyek nem illeszkednek a NUMERICAL vagy CATEGORICAL szabványos kategóriákba.  
- Segít abban, hogy az elemzések fókuszáltak maradjanak és az eredmények illeszkedjenek az üzleti kontextushoz.  

---

### Snapshot lekérdezésekben új helyőrzők
A snapshot lekérdezések mostantól egyszerűbbek és kevesebb hibára hajlamosak a **dinamikus helyőrzők** használatával.  

- Olyan tokenek, mint a `#date+n#` vagy `#date-n#`, automatikusan beállítják a lekérdezésekben szereplő dátumokat.  
- Példák:  
  - `#date+1#` → holnap  
  - `#date-2#` → két nappal ezelőtt  
- Eltörli a manuális dátumszámításokat és következetességet biztosít a csapatok között.  

---

### Küszöboptimalizálás
Az anomália-küszöbök mostantól intelligensebbek és kontextusérzékenyek.  

- Olyan metrikék, mint a **NULL COUNT**, esetén az alsó küszöbök automatikusan **0**-ra vannak korlátozva.  
- Megakadályozza érvénytelen vagy értelmetlen küszöbök kialakulását.  
- Kevesebb fals pozitívot és megbízhatóbb anomáliafelismerést eredményez.  

---

## Általános fejlesztések
- Finomított **UI komponensek** a projekt- és attribútumkonfiguráció nézetekben.  
- Nagy adatmennyiségek esetén javított **irányítópult teljesítmény**.  
- Fejlettebb **naplózás és hibaüzenetek** a hibakereséshez.  

---

## Összegzés
A 2024.12 verzió a dignát erősebb platformmá teszi az **adatminőség, anomáliafelismerés és megfigyelhetőség** terén.  
Az ütemezés és automatizálás, a megosztható PDF-jelentések, testreszabható oszlopok, egyszerűsített snapshot lekérdezések és az intelligensebb küszöbök révén a digna még értékesebbé válik mind a technikai felhasználók, mind az üzleti érintettek számára.