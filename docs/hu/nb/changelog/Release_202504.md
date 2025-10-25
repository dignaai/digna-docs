---
title: digna Release 2025.04 | Inspection Hub, többnyelvűség, Module Analytics
description: Tudja meg, mi újság a digna Release 2025.04-ben. Ez a kiadás bemutatja az Inspection Hubot, többnyelvű támogatást (angol, német, lengyel), adatforrások import/eksportját a dignacli segítségével, a Module Analytics első kiadását és egy finomított irányítópult-élményt.
keywords: digna Release 2025.04, digna changelog, digna inspection hub, digna multi-language support, digna module analytics, digna import export, digna CLI, release notes, data observability, data quality monitoring
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Változásnapló – Release 2025.04

A Release 2025.04-gyel a digna nagy lépést tesz afelé, hogy az adatok minőségének és observability-jának kezelése egyszerűbb legyen, átláthatóbb a csapatok számára, és elérhető legyen a világ minden táján dolgozó felhasználók számára.  
Ez a kiadás ötvözi a **erőteljes új funkciókat**, a **munkafolyamat-automatizálás fejlesztéseit**, és a **felhasználói élmény finomhangolásait**.  

---

## Új funkciók

### Inspection Hub – Egy új irányítóközpont
Az **Inspection Hub** mostantól elérhető mint központi hely az összes ellenőrzési feladat (inspection) kezelésére. Ahelyett, hogy különböző modulok között kellene ugrálnod, vagy kizárólag a parancssorra támaszkodnál, most egy letisztult felületen követheted és kezelheted az ellenőrzéseidet.  

Főbb funkciók:  
- Ellenőrzések igény szerint: Indíts új feladatokat azonnal, amikor friss eredményekre van szükséged.  
- Ellenőrzési előzmények: Nézd meg az ellenőrzések idővonalát — mit futtattak, ki indította és mikor.  
- Állapotkövetés: A feladatok egyértelműen jelölve vannak, mint befejezett, folyamatban lévő vagy várakozó.  
- Indító forrás információ: Gyorsan ellenőrizheted, hogy egy ellenőrzést egy felhasználó, egy ütemező vagy a CLI indított-e.  
- Tisztító eszközök: Töröld a régi vagy szükségtelen feladatokat a munkaterület rendezetten tartásához.  
- Részletes naplók: Mélyedj el minden feladatban, hogy lásd, mennyi ideig tartott, mely források voltak bevonva, és hogyan alkalmazódtak a küszöbértékek.  

Az Inspection Hub a csapatok számára **végponttól-végpontig terjedő láthatóságot és kontrollt** biztosít, és megkönnyíti az ellenőrzések kezelését nagy projektekben.  

---

### Többnyelvű támogatás – digna beszéli a nyelved
A digna mostantól készen áll a nemzetközi csapatokra a **többnyelvű támogatás** bevezetésével.  

Ebben a kiadásban a **preferált felületnyelvedet** közvetlenül a Felhasználói beállításokban állíthatod be. A támogatott nyelvek:  
- Angol (UK, US, CA, AU)  
- Német (DE, AT, CH)  
- Lengyel (PL)  

Ez megkönnyíti a digna használatát többnyelvű szervezetek számára, és elősegíti a zökkenőmentes bevezetést olyan csapatoknál, amelyek különböző régiókban dolgoznak. További nyelvek a későbbi kiadásokban lesznek elérhetők.  

---

### Adatforrások importálása és exportálása – Konfiguráció egyszerűen
A környezetek közötti konzisztencia kulcsfontosságú vállalati telepítések esetén. A 2025.04 verzióval a digna bemutatja az **adatforrások import/export** funkcióját a **dignacli** segítségével, amely a haladó felhasználók számára készült parancssori eszköz.  

Előnyök:  
- Exportálj egy adatforrás-konfigurációt egyszer, és használd újra Development, Test és Production környezetekben.  
- Kerüld el a manuális újrakonfigurálást és a költséges hibákat.  
- Támogasd az automatizált munkafolyamatokat és a CI/CD pipeline-okat egyszerű CLI parancsokkal (`export-ds` és `import-ds`).  
- Gyorsan másold át az adatforrásokat projektek között az egyszerűbb együttműködés érdekében.  

Ez a funkció lehetővé teszi, hogy a csapatok magabiztosan telepítsenek, tudva, hogy a konfigurációk minden környezetben következetesek.  

---

### Module Analytics (v1) – Az észleléstől a megértésig
A digna eredetileg anomáliaérzékelésre és adatkvalitás-figyelésre indult. A Release 2025.04-gyel továbbfejlődik a **Module Analytics első verziójával**.  

A Module Analytics segít a felhasználóknak abban, hogy **megértsék az adataikat** ahelyett, hogy csak reagálnának a problémákra. Ezzel az új modullal képes vagy:  
- Hosszú távú trendek követésére az adatállományokban.  
- A volatilitás észlelésére és monitorozására, hogy megértsd az ingadozásokat.  
- Az adatelőállítás viselkedésének időbeli vizsgálatára a mélyebb kontextusért.  

Például a digna automatikusan kiemelheti, hogy *„A sorok száma 15,8%-kal nőtt az év eleje óta.”*  
Nincs szükség SQL lekérdezésekre vagy manuális ellenőrzésekre — csak **cselekvésre alkalmas betekintések egy pillantással**.  

Ez a digna útjának alapja az előrehaladott adattudás felé, lehetővé téve az adattudó csapatok számára, hogy reaktívról proaktív megfigyelésre váltsanak.  

---

### Irányítópult-fejlesztések – Simaabb felhasználói élmény
A nagyobb funkciókon túl a Release 2025.04 több **irányítópult-fejlesztést** is tartalmaz, amelyek célja, hogy a digna intuitívabbá és élvezetesebbé váljon:  
- Gyorsabb navigáció projektek és ellenőrzések között.  
- Tisztább elrendezés az ellenőrzési naplók és feladatbeküldések megjelenítéséhez.  
- Finom design-igazítások, amelyek segítenek gyorsabban megtalálni az értékes betekintéseket.  

Ezeket a fejlesztéseket közvetlenül az ügyfélvisszajelzésekre alapozzuk, és azt mutatják, hogy folyamatosan elkötelezettek vagyunk amellett, hogy a digna **napi használatra tervezett platform** legyen.  

---

## Általános fejlesztések
- Teljesítményoptimalizálások az ellenőrzési feladatokhoz nagy adathalmazok esetén.  
- Javított hibakezelés a dignacli-ban a világosabb visszajelzések érdekében.  
- Stabilitásjavítások sok egyidejű feladattal rendelkező projektek számára.  
- UI-fejlesztések a feladatnaplók és projektkezelés szűréséhez.  

---

## Összefoglalás
A Release 2025.04 a **kontrollról, elérhetőségről és betekintésről** szól.  

- Az új **Inspection Hub** teljes láthatóságot ad az ellenőrzési feladatokhoz.  
- A **többnyelvű támogatás** biztosítja, hogy a digna globális csapatok számára is használható legyen.  
- Az **import/export funkció** leegyszerűsíti a konfigurációkezelést a környezetek között.  
- A **Module Analytics (v1)** a hangsúlyt az észlelésről a megértésre helyezi, trend- és volatilitáskövetéssel.  
- Az **irányítópult fejlesztései** finomhangolják az általános felhasználói élményt.  

Ezek a frissítések együtt még erősebbé, felhasználóbarátabbá és nemzetközileg is felkészültebbé teszik a dignát, mint valaha.