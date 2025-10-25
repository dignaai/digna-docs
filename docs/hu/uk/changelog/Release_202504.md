---
title: digna Kiadás 2025.04 | Inspection Hub, többnyelvűség, Module Analytics
description: Ismerje meg a digna 2025.04-es kiadásának újdonságait. Ebben a verzióban bemutatjuk az Inspection Hubot, a többnyelvű támogatást (angol, német, lengyel), az adatforrások import/exportját a dignacli segítségével, a Module Analytics első kiadását és a továbbfejlesztett dashboard-élményt.
keywords: digna Kiadás 2025.04, digna changelog, digna inspection hub, digna többnyelvűség, digna module analytics, digna import export, digna CLI, release notes, data observability, adatminőség-figyelés
canonical_url: https://docs.digna.ai/changelog/Release_202504/
image: /assets/logo_square.png
---

# Changelog – Kiadás 2025.04

A 2025.04-es kiadással a digna nagy lépést tesz előre abban, hogy az adatok minőségének kezelése és az observability egyszerűbbé, átláthatóbbá és a világ minden táján elérhetővé váljon a csapatok számára.  
Ez a kiadás ötvözi a **erőteljes új funkciókat**, a **munkafolyamatok automatizálásának fejlesztését** és a **felhasználói élmény javítását**.  

---

## Újdonságok

### Inspection Hub – az új irányítóközpont
Az **Inspection Hub** mostantól elérhető, mint az összes ellenőrzési feladat központi kezelőfelülete. A különböző modulok között váltogatás vagy kizárólag a parancssorra támaszkodás helyett mostantól egy rendezett felületről monitorozhatja és vezérelheti az ellenőrzéseket.  

Főbb funkciók:  
- Ellenőrzések igény szerint: indítson új feladatokat azonnal, ha friss eredményekre van szükség.  
- Ellenőrzési előzmények: tekintse át az ellenőrzések időrendjét — mi lett futtatva, ki indította és mikor.  
- Állapotkövetés: a feladatok egyértelműen jelölve vannak, mint befejezett, folyamatban lévő vagy várakozó.  
- Indító információk: gyorsan ellenőrizze, hogy az ellenőrzést felhasználó, ütemező vagy CLI indította-e.  
- Takarító eszközök: távolítsa el az elavult vagy felesleges feladatokat, hogy rendezetten tartsa a munkaterületet.  
- Részletes naplók: mélyedjen el minden feladatban, hogy lássa a futás időtartamát, mely források voltak bevonva és hogyan alkalmazódtak a küszöbértékek.  

Az Inspection Hub a csapatok számára biztosítja az **egységes láthatóságot és kontrollt**, megkönnyítve az ellenőrzések kezelését nagyobb projektekben.  

---

### Többnyelvű támogatás – digna a saját nyelvén beszél
A digna mostantól felkészült a nemzetközi csapatokra a **többnyelvű támogatás** bevezetésével.  

Ebben a kiadásban a felhasználói beállításoknál megadhatja a **preferált felületnyelvet**. A támogatott nyelvek:  
- Angol (UK, US, CA, AU)  
- Német (DE, AT, CH)  
- Lengyel (PL)  

Ez megkönnyíti a digna használatát többnyelvű szervezetek számára, és elősegíti a zökkenőmentes bevezetést olyan csapatoknál, amelyek különböző régiókban dolgoznak. További nyelvek a következő kiadásokban lesznek elérhetők.  

---

### Adatforrások importja és exportja – egyszerűbb konfiguráció
A környezetek közötti konzisztencia kritikus a vállalati telepítéseknél. A 2025.04-es verzióban a digna bevezeti az **adatforrások import/export** funkcióját a **dignacli**-n keresztül — a haladó felhasználóknak szánt parancssori eszközön.  

Előnyök:  
- Exportálja egyszer az adatforrás konfigurációját, majd újrahasználhatja Development, Test és Production környezetekben.  
- Megszünteti a manuális újrakonfigurálást és elkerüli a költséges hibákat.  
- Támogatja az automatizált munkafolyamatokat és CI/CD csővonalakat egyszerű CLI-parancsokkal (`export-ds` és `import-ds`).  
- Gyorsan másolhat adatforrásokat projektek között az együttműködés megkönnyítése érdekében.  

Ez a funkció biztosítja, hogy a csapatok magabiztosan telepíthessenek, tudva, hogy a konfigurációk egységesek minden környezetben.  

---

### Module Analytics (v1) – a felismeréstől a megértésig
A digna eredetileg az anomáliák felismerésére és az adatminőség monitorozására épült. A 2025.04-es kiadásban továbbfejlődik az első verzióval: **Module Analytics**.  

A Module Analytics segít a felhasználóknak a **adataik megértésében**, nem csupán a problémákra való reagálásban. Ezzel az új modullal képes lesz:  
- Hosszú távú trendek követésére az adatkészleteiben.  
- A volatilitás azonosítására és monitorozására, hogy megértse az ingadozásokat.  
- Az adatok viselkedésének időbeli feltárására mélyebb kontextusért.  

Például a digna automatikusan kiemelheti, hogy *„A sorok száma 15,8%-kal nőtt az év eleje óta.”*  
Sem SQL-lekérdezésekre, sem kézi ellenőrzésekre nincs szükség — csak **hasznos betekintések egy pillantásra**.  

Ez a lépés alapot ad a digna fejlődéséhez az előrehaladott adat-analitikába, lehetővé téve a csapatok számára a reaktív megközelítésről a proaktív monitorozásra való átállást.  

---

### Dashboard-fejlesztések – simább felhasználói élmény
Az alapfunkciók mellett a 2025.04-es kiadás számos **dashboard-fejlesztést** tartalmaz, amelyek célja, hogy a digna intuitívabb és élvezetesebb legyen a használat során:  
- Gyorsabb navigáció a projektek és ellenőrzések között.  
- Tisztább elrendezés az ellenőrzési logok és feladatbeküldések számára.  
- Finom dizájnjavítások, amelyek segítenek gyorsabban megtalálni az insighteket.  

Ezek a fejlesztések közvetlenül az ügyfélvisszajelzésekre épülnek, és demonstrálják elkötelezettségünket a digna folyamatos fejlesztése iránt, hogy az **napi használatra alkalmas platform** legyen.  

---

## Általános fejlesztések
- Teljesítményoptimalizáció az ellenőrzési feladatokhoz nagy adatkészletek esetén.  
- Hibakezelés javítása a dignacli-ben, hogy érthetőbb visszajelzést nyújtson.  
- Stabilitás növelése olyan projekteknél, ahol sok egyidejű feladat fut.  
- UI-fejlesztések a feladatnaplók szűréséhez és a projektek kezeléséhez.  

---

## Összegzés
A 2025.04-es kiadás a **kontroll, elérhetőség és betekintések** témáira összpontosít.  

- Az új **Inspection Hub** teljes rálátást biztosít az ellenőrzési feladatokra.  
- A **többnyelvű támogatás** garantálja, hogy a digna globális csapatoknál is használható legyen.  
- Az **import/export** funkció megkönnyíti a konfigurációk kezelését a környezetek között.  
- A **Module Analytics (v1)** a felismeréstől a megértés felé mozdítja el a fókuszt, trend- és volatilitáskövetést kínálva.  
- A **dashboard-fejlesztések** jobb felhasználói élményt nyújtanak.  

Ezek az újítások együtt még erősebbé, felhasználóbarátabbá és nemzetközi használatra készsé teszik a dignát, mint valaha.