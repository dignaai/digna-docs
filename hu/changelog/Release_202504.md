# Changelog – 2025.04 kiadás

A 2025.04 kiadással a digna nagy lépést tesz afelé, hogy az adatminőség és az observability könnyebben kezelhetővé váljon, átláthatóbb legyen a csapatok számára, és világszerte hozzáférhető legyen a felhasználók számára.  
Ez a kiadás ötvözi a **nagy teljesítményű új funkciókat**, a **munkafolyamat-automatizálás fejlesztéseit** és a **felhasználói élmény finomhangolását**.  

---

## Új funkciók

### Inspection Hub – Az új irányítóközpont
Az **Inspection Hub** mostantól elérhető mint a központi hely az összes inspection feladat kezelésére. Ahelyett, hogy modulok között ugrálnál vagy kizárólag parancssori futtatásra támaszkodnál, mostantól egy letisztult felületről figyelheted és irányíthatod az inspectiókat.  

Fő képességek:  
- On-demand inspectiók: Indíts új feladatokat azonnal, amikor friss eredményekre van szükséged.  
- Inspectiótörténet: Lásd az inspectiók idővonalát — mi futott, ki indította és mikor.  
- Állapotkövetés: A feladatok egyértelműen jelölve vannak, hogy befejeződtek, folyamatban vannak vagy függőben vannak.  
- Indító információk: Gyorsan ellenőrizheted, hogy egy inspectió felhasználó, ütemező vagy a CLI által lett-e indítva.  
- Takarító eszközök: Töröld a régi vagy szükségtelen feladatokat a munkaterület tisztán tartásához.  
- Részletes naplók: Mélyedj el minden feladatban, hogy lásd, mennyi ideig tartott, mely források voltak benne, és hogyan alkalmazódtak a küszöbértékek.  

Az Inspection Hub teljes körű láthatóságot és irányítást ad a csapatoknak, megkönnyítve az inspectiók kezelését nagyobb projektekben.  

---

### Többnyelvű támogatás – digna a te nyelveden beszél
A digna mostantól nemzetközi csapatok számára is készen áll a **többnyelvű támogatás** bevezetésével.  

Ebben a kiadásban közvetlenül a Felhasználói beállításokban állíthatod be a **preferált felületnyelvet**. A támogatott nyelvek:  
- Angol (UK, US, CA, AU)  
- Német (DE, AT, CH)  
- Lengyel (PL)  

Ez megkönnyíti a digna használatát többnyelvű szervezetek számára, és elősegíti a zökkenőmentes bevezetést a különböző régiókban dolgozó csapatoknál. További nyelvek a jövőbeli kiadásokban lesznek elérhetők.  

---

### Adatforrások importálása és exportálása – egyszerű konfigurációkezelés
A környezetek közötti következetesség alapvető a vállalati telepítésekben. A 2025.04-gyel a digna bevezeti az **adatforrások import/exportját** a haladó felhasználók számára készült **dignacli** parancssori eszközön keresztül.  

Előnyök:  
- Exportálj egy adatforrás-konfigurációt egyszer, majd használd újra Fejlesztés, Teszt és Termelés környezetekben.  
- Szűntesd meg a manuális újrakonfigurálást és kerüld el a költséges hibákat.  
- Támogasd az automatizált munkafolyamatokat és a CI/CD pipeline-okat egyszerű CLI parancsokkal (`export-ds` és `import-ds`).  
- Gyorsan másold át az adatforrásokat projektek között az egyszerűbb együttműködés érdekében.  

Ez a funkció biztosítja, hogy a csapatok magabiztosan telepíthessenek, tudva, hogy a konfigurációk minden környezetben következetesek.  

---

### Module Analytics (v1) – A detektálástól a megértésig
A digna detektálásra és adatminőség-figyelésre épült platformként indult. A 2025.04 kiadással tovább fejlődik a **Module Analytics első verziója**.  

A Module Analytics segít a felhasználóknak abban, hogy **megértsék az adataikat**, ne csak reagáljanak a problémákra. Ezzel az új modullal képes vagy:  
- Hosszú távú trendeket követni az adatkészleteidben.  
- Volatilitás észlelésére és monitorozására, hogy megértsd az ingadozásokat.  
- Időbeli viselkedés feltérképezésére mélyebb kontextusért.  

Például a digna automatikusan kiemelheti, hogy „A sorok száma az év eleje óta 15,8%-kal nőtt.”  
Nincs szükség SQL lekérdezésekre vagy manuális ellenőrzésekre — csak egy pillantásra értelmezhető, használható insightok.  

Ez a digna útjának az alapja az előrehaladott adatelemzés felé, lehetővé téve az adatos csapatok számára, hogy a reaktív helyett proaktív monitorozásra térjenek át.  

---

### Irányítópult fejlesztések – zökkenőmentesebb felhasználói élmény
A fő funkciókon túl a 2025.04 kiadás számos **irányítópult-finomítást** tartalmaz, amelyek célja, hogy a digna intuitívabbá és élvezetesebbé váljon:  
- Gyorsabb navigáció a projektek és inspectiók között.  
- Tisztább elrendezés az inspectió naplók és feladatbeküldések megjelenítéséhez.  
- Finom design módosítások, amelyek segítenek gyorsabban megtalálni az insightokat.  

Ezek a fejlesztések közvetlenül az ügyfélvisszajelzésekre épülnek, és bemutatják elkötelezettségünket amellett, hogy a digna **napi használatra épített platform** legyen.  

---

## Általános fejlesztések
- Teljesítményoptimalizálások az inspectió feladatokhoz nagy adathalmazok esetén.  
- Javított hibakezelés a dignacli-ben, hogy világosabb visszajelzést adjon.  
- Stabilitásjavítások sok egyidejű feladattal rendelkező projektek számára.  
- UI finomhangolások a feladatnaplók szűréséhez és a projektkezeléshez.  

---

## Összefoglalás
A 2025.04 kiadás a **kontrollról, hozzáférhetőségről és betekintésről** szól.  

- Az új **Inspection Hub** teljes láthatóságot ad az inspectió feladatokhoz.  
- A **többnyelvű támogatás** biztosítja, hogy a digna globális csapatok számára használható legyen.  
- Az **import/export funkcionalitás** egyszerűsíti a konfigurációkezelést a különböző környezetek között.  
- A **Module Analytics (v1)** a detektálásról a megértésre helyezi a hangsúlyt, trend- és volatilitáskövetéssel.  
- Az **irányítópult fejlesztések** finomítják az általános felhasználói élményt.  

Ezek az újdonságok együtt még hatékonyabbá, felhasználóbarátabbá és nemzetközileg is jobban alkalmazkodóvá teszik a dignát, mint valaha.