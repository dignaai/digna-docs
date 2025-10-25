---
title: digna Release 2024.12 | Változásnapló és új funkciók
description: Tudja meg, mi újság a digna Release 2024.12-ben. Ebben a kiadásban beépített ütemező, PDF-jelentések, rugalmas egyéni oszloptípusok, dinamikus helykitöltők snapshot-lekérdezésekben és intelligensebb küszöboptimalizálás került bevezetésre az anomáliák és az adatok minőségének monitorozásának javítása érdekében.
keywords: digna Release 2024.12, digna változásnapló, kiadási megjegyzések, beépített ütemező, PDF-jelentések, egyéni oszloptípus, helykitöltők snapshot-lekérdezésekben, küszöboptimalizálás, adatok megfigyelhetősége, adatok minőségének monitorozása, anomáliafelismerés
canonical_url: https://docs.digna.ai/changelog/Release_202412/
image: /assets/logo_square.png
---



# Változásnapló – Release 2024.12

A 2024.12-es kiadás számos új funkciót és fejlesztést hoz, amelyek automatizáltabbá, rugalmasabbá és üzletre készebbé teszik a digna-t.  
Ez a verzió javítja az ütemezést, jelentéskészítést, lekérdezéskezelést és az anomáliafelismerés pontosságát.  

---

## Új funkciók

### Beépített ütemező
A ellenőrzések már nem függenek kizárólag a parancssortól vagy az API-hívásoktól.  
Az új, beépített digna ütemezővel az ellenőrzések automatikusan lefuthatnak meghatározott időpontokban.  

- Támogatja a **Cron-kifejezéseket** ismétlődő ütemezésekhez (napi, heti vagy egyedi intervallumok).  
- Pontos vezérlést nyújt **eltolásokkal (offsets)**, **kezdő dátumokkal** és **befejezési dátumokkal**.  
- Lehetővé teszi a csapatok számára, hogy következetes és hibamentes ellenőrzést biztosítsanak minden kritikus adatforráshoz.  

---

### PDF-formátumú jelentések
A csapatok mostantól könnyen megoszthatják az eredményeket az érintettekkel a **PDF-export** segítségével.  

- Diagramok, mutatók és anomáliaeredmények professzionális PDF-fájlba exportálhatók.  
- A jelentések egyesítik a **vizualizációkat** és a **kulcsadatokat**, kielégítve mind a technikai, mind az üzleti felhasználókat.  
- Megszünteti a külső eszközök szükségességét a jelentéskészítéshez.  

---

### Új oszloptípus: `CUSTOM`
Több rugalmasság érdekében a digna bevezeti az új oszloptípust: **`CUSTOM`**.  

- A felhasználók pontosan megadhatják, mely **statisztikák és metrikák** alkalmazandók adott attribútumokra.  
- Különösen hasznos speciális esetekhez, amelyek nem illenek a szabványos kategóriákhoz, mint a NUMERICAL vagy CATEGORICAL.  
- Segít, hogy az elemzés fókuszált maradjon, és az eredmények relevánsak legyenek az üzleti kontextus számára.  

---

### Új helykitöltők a snapshot-lekérdezésekben
A snapshot-lekérdezések egyszerűbbé és kevésbé hibára hajlamossá váltak a **dinamikus helykitöltők** révén.  

- Olyan tokenek, mint a `#date+n#` vagy `#date-n#`, automatikusan szabják át a dátumokat a lekérdezésekben.  
- Példa:  
  - `#date+1#` → holnap  
  - `#date-2#` → két nappal ezelőtt  
- Megszünteti a kézi dátumszámításokat és biztosítja a csapatok közötti következetességet.  

---

### Küszöboptimalizálás
Az anomália-küszöbök intelligensebbé és kontextusérzékennyé váltak.  

- Olyan metrikák esetén, mint a **NULL COUNT**, az alsó küszöb automatikusan korlátozva van **0** értékre.  
- Megakadályozza a hibás vagy értelmetlen küszöbök beállítását.  
- Csökkenti a hamis riasztások számát és növeli az anomáliafelismerés megbízhatóságát.  

---

## Általános fejlesztések
- Fejlesztett **UI-komponensek** a projekt- és attribútumkonfiguráció nézetekben.  
- Javult a **dashboard** teljesítménye nagy adatmennyiség esetén.  
- Kiterjesztett naplózás és hibajelentés az egyszerűbb hibakeresés érdekében.  

---

## Összefoglalás
A 2024.12-es kiadás tovább erősíti a digna pozícióját, mint az adatok minőségéért, anomáliafelismerésért és adatok megfigyelhetőségéért felelős platformot.  
Az ütemezéssel történő automatizálás, a megosztható PDF-jelentések, az egyénre szabható oszlopok, az egyszerűsített snapshot-lekérdezések és az intelligensebb küszöbök révén a digna még értékesebb eszközzé válik mind a technikai felhasználók, mind az üzleti érintettek számára.