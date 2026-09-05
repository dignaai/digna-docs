---
title: digna Kiadás 2024.12 | Változásnapló és új funkciók
description: Tudja meg, mi újság a digna 2024.12-es kiadásában. Ez a verzió beépített ütemezőt, PDF-jelentéseket, rugalmas egyéni oszlopokat, dinamikus snapshot lekérdezéshelyettesítőket és okosabb küszöboptimalizálást hoz az anomáliaészlelés és az adatminőség-ellenőrzés javítására.
keywords: digna Kiadás 2024.12, digna változásnapló, kiadási megjegyzések, beépített ütemező, PDF jelentések, egyéni oszloptípus, snapshot lekérdezés helyettesítők, küszöb optimalizálás, adat megfigyelhetőség, adatminőség-ellenőrzés, anomáliaészlelés
image: /assets/logo_square.png
---



# Változásnapló – Kiadás 2024.12

A 2024.12-es kiadás új funkciókat és fejlesztéseket hoz, amelyek révén a digna még inkább automatizált, rugalmas és üzleti használatra kész lesz.  
Ez a verzió javítja az ütemezést, a jelentéskészítést, a lekérdezéskezelést és az anomáliaészlelés pontosságát.  

---

## Új funkciók

### Beépített ütemező
Az ellenőrzések már nem függenek kizárólag parancssortól vagy API-hívásoktól.  
A **beépített digna ütemezővel** az ellenőrzések meghatározott időpontokban automatikusan lefuttathatók.  

- Támogatja a **Cron kifejezéseket** ismétlődő ütemezésekhez (napi, heti vagy egyedi időközök).  
- Precíz vezérlést kínál **eltolások**, **kezdő dátumok** és **záró dátumok** révén.  
- Segít biztosítani, hogy minden kritikus adatforrást következetesen és manuális beavatkozás nélkül ellenőrizzenek.  

---

### PDF formátumú jelentések
A csapatok mostantól könnyen megoszthatják az eredményeket az érintettekkel **PDF exportok** segítségével.  

- Diagramok, metrikák és anomáliaeredmények professzionális PDF formátumban exportálhatók.  
- A jelentések kombinálják a **vizualizációkat** és az **alapul szolgáló adatokat**, így mind a technikai, mind az üzleti felhasználókat kiszolgálják.  
- Megszünteti a jelentéskészítéshez szükséges külső eszközök igényét.  

---

### Új oszloptípus: `CUSTOM`
A nagyobb rugalmasság érdekében a digna bemutat egy új **`CUSTOM` oszloptípust**.  

- A felhasználók pontosan meghatározhatják, mely **statisztikák és metrikák** alkalmazhatók adott attribútumokra.  
- Ideális speciális esetekhez, amelyek nem illenek a hagyományos kategóriákba, mint a NUMERICAL vagy CATEGORICAL.  
- Segít, hogy az elemzések célzottak maradjanak és az eredmények üzleti kontextushoz igazodjanak.  

---

### Új helyettesítők a snapshot lekérdezésekben
A snapshot lekérdezések most egyszerűbbek és kevésbé hibára hajlamosak a **dinamikus helyettesítőkkel**.  

- Olyan tokenek, mint a `#date+n#` vagy `#date-n#`, automatikusan igazítják a dátumokat a lekérdezésekben.  
- Példa:  
  - `#date+1#` → holnap  
  - `#date-2#` → két nappal ezelőtt  
- Megszünteti a kézi dátumszámításokat és biztosítja az egységességet a csapatok között.  

---

### Küszöboptimalizálás
Az anomália-küszöbök most intelligensebbek és kontextusérzékenyebbek.  

- Olyan metrikák esetén, mint a **NULL COUNT**, az alsó küszöbök automatikusan **0**-ra lesznek korlátozva.  
- Megelőzi az érvénytelen vagy értelmetlen küszöbértékeket.  
- Kevesebb hamis pozitív eredményt és megbízhatóbb anomáliaészlelést eredményez.  

---

## Általános fejlesztések
- Finomított **UI komponensek** a projekt- és attribútumkonfiguráció nézetekben.  
- Javított **dashboard teljesítmény** nagy adatvolumen esetén.  
- Kiterjesztett **naplózás és hibaüzenetek** a hibakeresés megkönnyítésére.  

---

## Összefoglaló
A 2024.12-es kiadás tovább erősíti a dignát, mint az **adatminőség, anomáliaészlelés és megfigyelhetőség** platformját.  
Az ütemezés általi automatizálás, megosztható PDF-jelentések, testreszabható oszlopok, egyszerűsített snapshot lekérdezések és okosabb küszöbök révén a digna még értékesebbé válik mind technikai, mind üzleti felhasználók számára.