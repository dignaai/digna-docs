---
title: digna Verzió 2025.04 | Inspection Hub, Többnyelvű, Module Analytics
description: Tudja meg, mi újság a digna Verzió 2025.04-ben. Ez a kiadás bemutatja az Inspection Hubot, többnyelvű támogatást (angol, német, lengyel), a dignacli-val történő adatforrás import/exportot, a Module Analytics első kiadását és egy továbbfejlesztett irányítópult-élményt.
keywords: digna Verzió 2025.04, digna változásnapló, digna inspection hub, digna többnyelvű támogatás, digna module analytics, digna import export, digna CLI, verziójegyzetek, adatmegfigyelhetőség, adatminőség-figyelés
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Változásnapló – Release 2025.04

A Release 2025.04 nagy lépést jelent a digna számára abban, hogy a csapatok számára könnyebbé, átláthatóbbá és globálisan elérhetővé tegye az adatminőség és megfigyelhetőség kezelését.  
Ez a kiadás egyesíti a **erős új funkciókat**, a **munkafolyamat-automatizálás fejlesztéseit** és a **felhasználói élmény javításait**.  

---

## Új Funkciók

### Inspection Hub – Új irányítóközpont
Az **Inspection Hub** mostantól központi helyként szolgál minden ellenőrzési feladat kezelésére. A különböző modulok közti váltás vagy kizárólag parancssorra támaszkodás helyett mostantól egyetlen egyszerűsített felületen követheti és irányíthatja az ellenőrzéseket.  

Fő képességek:  
- Igény szerinti ellenőrzések: Indítsa el az ellenőrzéseket azonnal, amikor új eredményekre van szüksége.  
- Ellenőrzési előzmények: Idősoros nézetben láthatja, mely ellenőrzések futottak le, ki indította őket és mikor.  
- Állapotkövetés: A feladatok egyértelműen jelölve vannak „befejezett”, „fut” vagy „függőben” állapotokkal.  
- Indítási információk: Gyorsan ellenőrizze, hogy egy ellenőrzést felhasználó, időzítő vagy a CLI indított-e.  
- Tisztítási eszközök: Távolítsa el a régi vagy felesleges feladatokat a munkaterület tisztán tartásához.  
- Részletes naplók: Adjon meg minden feladatot, hogy megnézze a futási időt, az érintett forrásokat és azt, hogyan alkalmazódtak a küszöbértékek.  

Az Inspection Hub segít a csapatoknak abban, hogy **teljes körű láthatóságot és irányítást** kapjanak, megkönnyítve az ellenőrzések kezelését nagyobb projektekben.  

---

### Többnyelvű Támogatás – digna az Ön nyelvén
A digna mostantól készen áll a nemzetközi csapatokra a **többnyelvű támogatás** bevezetésével.  

Ebben a kiadásban az interfész nyelvét közvetlenül a Felhasználói beállításokban állíthatja be. A támogatott nyelvek:  
- Angol (UK, US, CA, AU)  
- Német (DE, AT, CH)  
- Lengyel (PL)  

Ez megkönnyíti a digna használatát többnyelvű szervezetek számára, és gördülékenyebb bevezetést tesz lehetővé különböző régiókban dolgozó csapatok között. A jövőbeli kiadásokban további nyelvek kerülnek hozzáadásra.  

---

### Adatforrások importálása & exportálása – Egyszerűbb konfigurációkezelés
A vállalati telepítések esetén a környezetek közötti konzisztencia kritikus. A 2025.04-es kiadással a digna lehetővé teszi az adatforrások **importálását és exportálását** a fejlett felhasználók számára elérhető parancssori eszköz, a **dignacli** segítségével.  

Előnyök:  
- Egy adatforrás konfigurációját egyszer exportálhatja, majd újrahasználhatja Development, Test és Production környezetekben.  
- Megszünteti a manuális újrakonfigurálást és csökkenti a költséges hibákat.  
- Egyszerű CLI-parancsokkal (`export-ds` és `import-ds`) támogatja az automatizált munkafolyamatokat és a CI/CD csővezetékeket.  
- Gyorsan másolhat adatforrásokat projektek között, elősegítve az együttműködést.  

Ez a funkcionalitás lehetővé teszi a csapatok számára, hogy magabiztosan telepítsenek, biztosítva a konfigurációk konzisztenciáját minden környezetben.  

---

### Module Analytics (v1) – A felismeréstől a megértésig
A digna anomáliaészlelésre és adatminőség-figyelésre épült platformként indult. A Release 2025.04-gyel tovább lép a **Module Analytics első verziójával**.  

A Module Analytics segít a felhasználóknak, hogy a problémákra reagálás helyett **megértsék az adataikat**. Ezzel az új modullal a következőket teheti:  
- Kövesse a hosszú távú trendeket az adathalmazokban.  
- Az ingadozások megértéséhez és nyomon követéséhez mérje a volatilitást.  
- Fedezze fel az adatviselkedést az időben, hogy mélyebb kontextust kapjon.  

Például a digna automatikusan kiemelheti: „A sorok száma az év eleje óta 15,8%-kal nőtt.”  
Nincs SQL-lekérdezés, nincs manuális ellenőrzés — csak azonnal alkalmazható betekintések.  

Ez lefekteti a digna további fejlett adatelemzési irányú fejlődésének alapját, és segíti az adatcsapatokat abban, hogy a reaktív figyelésről a proaktív megfigyelésre térjenek át.  

---

### Irányítópult fejlesztések – Zökkenőmentesebb felhasználói élmény
Az alapfunkciókon túl a Release 2025.04 több **irányítópult-elrendezési** módosítást is tartalmaz a digna intuitívabbá és élvezetesebbé tételéhez:  
- Gyorsabb navigáció projektek és ellenőrzések között.  
- Tisztább elrendezés az ellenőrzési naplók és feladatbeküldések számára.  
- Finom dizájnigazítások, amelyek megkönnyítik a betekintések megtalálását.  

Ezek a fejlesztések közvetlenül az ügyféli visszajelzéseken alapulnak, és megerősítik a digna elköteleződését amellett, hogy „napi használatra épített” platform legyen.  

---

## Általános fejlesztések
- Teljesítményoptimalizálások az ellenőrzési feladatokhoz nagy adathalmazok esetén.  
- Fejlettebb hibakezelés a dignacli-ben, hogy tisztább visszajelzést adjon.  
- Stabilitásjavítások olyan projektekben, ahol egyszerre sok feladat fut.  
- Felhasználói felület (UI) fejlesztések a munkanapló-szűrés és a projektkezelés számára.  

---

## Összegzés
A Release 2025.04 a **vezérlésről, elérhetőségről és betekintésről** szól.  

- Az új **Inspection Hub** teljes láthatóságot biztosít a felhasználóknak az ellenőrzési feladatok felett.  
- A **többnyelvű támogatás** lehetővé teszi, hogy a digna globális csapatok számára is használható legyen.  
- Az **import/export funkció** egyszerűsíti a konfigurációkezelést környezetek között.  
- A **Module Analytics (v1)** a trend- és ingadozáskövetéssel a felismerésről a megértésre helyezi a hangsúlyt.  
- Az **irányítópult fejlesztések** finomítják az általános felhasználói élményt.  

Ezek a frissítések együtt még erősebbé, felhasználóbarátabbá és nemzetközileg használhatóvá teszik a dignát.