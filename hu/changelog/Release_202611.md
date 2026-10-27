# Változáslista – Kiadás 2026.11  

A 2026.11-es kiadás három jelentős újdonságra épül:

- **digna Data Reconciliation**: ellenőrzi, hogy az adatok konzisztensek maradnak-e, miközben rendszerek között mozognak  
- **digna Agentic**: a digna MCP Serveren keresztül megnyitja a dignát az AI-ágensek előtt  
- **digna Engine**: opcionálisan a dignán belül profilozza az adatokat, és lehetővé teszi a referenciális integritás ellenőrzését különböző adatbázis-technológiák között  

---

## Új funkciók  

### digna Data Reconciliation (Beta) – Konzisztencia a forrástól a célig  
Az adatok gyakran több rendszeren haladnak át, mielőtt egy riportba kerülnek. A digna Data Reconciliation összehasonlít egy **cél** adatforrást azokkal a **forrásokkal**, amelyekből előállt, és riaszt, ha már nem egyeznek.

- Elnevezett szabályokként konfigurálható a cél adatforrás új **Data Reconciliation** lapján  
- A projekt bármely adatforrása lehet forrás, amelyen a Data Reconciliation be van kapcsolva  
- Felhasználási területek: szabványos egyeztetési eljárások és az ETL-folyamatok eredményeinek validálása  
- Kétféle szabály: **Exact** és **AI**  

**Exact szabályok – Egyeztetés adatminőségi szabályként**: Pontosan meghatározod, minek kell egyeznie egy forrás és egy cél között, akárcsak egy adatminőségi szabálynál.

  - Egy forrás adatforrás összehasonlítása egy cél adatforrással  
  - Egy cél-ellenőrzés párosítása egy forrás-ellenőrzéssel statisztika és attribútum szerint, pl. a sorok száma vagy egy összegoszlop összege  
  - Eltérés engedélyezése **absolute** tűréssel (pl. ± 10) vagy **relative** tűréssel (pl. a forrás ± 0,5 %-a)  
  - Az idővonal minden napra megmutatja az eltérést a tűréshez képest  

**AI szabályok – Egyeztetés adatmegfigyelhetőségként**: A digna megtanulja, hogyan követi a cél a forrásait – ugyanúgy, ahogy más modulokban is megfigyeli az adatokat –, és riaszt, ha ez a kapcsolat megszakad.

  - Több forrás adatforrás ellenőrzéseinek kombinálása egy cél ellenőrzéseivel  
  - Nem kell ismerni vagy leírni a köztük lévő logikát (joinok, szűrők, aggregációk)  
  - Egy modell az előzményekből tanulja meg, hogyan követi a cél ugyanazon a napon a forrásait  
  - Minden cél-ellenőrzés értékét a nap forrásértékeiből jelzi előre a modell, és a digna riaszt, ha a cél kilép a szabály saját korábbi hibáiból képzett sávból  
  - Minden szabálynak saját **Model settings** beállításai vannak: **Sensitivity**, **Memory** és **Model Complexity**  

Az egyeztetési ellenőrzések a Dashboardon szabályonként egy idővonallal jelennek meg. Beleszámítanak az inspekció összesített állapotába, és értesítéseket váltanak ki.

**Hatás:** Az egyeztetés mindkét oldalát lefedi. Az Exact szabályok ismert kontrollokat érvényesítenek a forrás és a cél között, az AI szabályok pedig összetett folyamatokat, például ETL-folyamatokat figyelnek, így az útközben elveszett vagy megváltozott adatok kézzel írt egyeztető SQL nélkül is kiderülnek.

---

### digna Agentic (Beta) – digna AI-ágenseknek  
A digna Agentic első verziója. Az AI-ágensek mostantól együtt tudnak dolgozni a dignával, üzleti kérdésekre válaszolnak az adataidról, és segítenek javítani a konfigurációdat.

**digna MCP Server**: Lehetővé teszi, hogy Claude és más AI-ágensek a Model Context Protocolon keresztül dolgozzanak a dignával.

  - Projektek, adatforrások, szabályok, inspekciós ütemezések és feliratkozások kezelése  
  - Inspekciós állapotok olvasása egészen az egyes ellenőrzésekig, a riasztások kivizsgálásához  

**Leírások adatforrásokhoz és attribútumokhoz**: Írd le közérthető nyelven, mit tartalmaz egy adatforrás vagy attribútum.

  - Az AI-ágensek a leírások alapján értelmezik az adataidat  
  - Tegyél fel üzleti kérdéseket az adataidról, és az AI-ágensek abból válaszolnak, amit a digna monitoroz  
  - Ha a digna jelenlegi konfigurációja nem tud megválaszolni egy kérdést, az AI-ágens lehetőség szerint módosításokat javasol az adatforráson és annak attribútumain, pl. egy új adatkészlet hozzáadását  

**Hatás:** Közérthető nyelven tehetsz fel üzleti kérdéseket az adataidról, az AI-ágensek pedig segítenek a digna konfigurálásában és az adatminőségi problémák kivizsgálásában.

---

### digna Engine – Profilozás ott, ahol te választod  
Alapértelmezés szerint a digna ott profilozza az adatokat, ahol azok vannak: a forrásadatbázisban. A digna Engine új lehetőséget ad: a digna exportálja az adatokat a forrásból, és a digna Engine-en belül profilozza őket.

- Opcionális, nem kötelező: a forrásadatbázisban történő profilozás továbbra is elérhető  
- Adatbázis-kapcsolatonként választható ki **profilozási helyként**: **Source Database** vagy **digna Engine**  
- Minden támogatott forrástechnológiához elérhető  

**Kapcsolatokon átívelő referenciális integritás**: Egyes ellenőrzésekhez exportálni kell az adatokat. A digna Engine ezekre az esetekre kibővíti a **digna Data Validation** modult.

  - **Referential Integrity Checks** **különböző adatbázis-kapcsolatokon** lévő adatforrások között, beleértve a különböző adatbázis-technológiákat is (pl. Oracle és PostgreSQL)  
  - Mindkét profilozási hellyel működik: Source Database esetén csak a kulcsoszlopok kerülnek exportálásra a digna Engine-be  
  - A dashboard jelzi, ha egy ellenőrzés két kapcsolaton átívelően fut  

**Hatás:** Te választhatod meg, hol történjen az adatok profilozása, és érvényesíthetők a kapcsolatok olyan rendszerek között, amelyek különböző adatbázis-technológiákon futnak.

---

## Profilozási fejlesztések  

Ez a kiadás azt is jobban a felhasználók kezébe adja, hogy mi és hogyan legyen profilozva.

### Lekérdezési attribútumok – Felhasználó által definiált oszlopok  
- Mesterséges oszlopok definiálása: SQL-kifejezés az adatforrás egy vagy több oszlopa felett  
- Minden lekérdezési attribútumnak saját neve van  
- Ugyanúgy profilozható és ellenőrizhető, mint bármely más attribútum  

### DATE oszlopkategória  
- Új **Date** kategória az attribútumokhoz  
- Az inspektált dátumhoz viszonyított metrikák  

### Igény szerinti profilozás  
- Bármely attribútum profilozása egy adott dátum teljes pillanatképén, inspekció futtatása nélkül  
- Segít beállítani az attribútum oszloptípusát: **Numerical**, **Categorical**, **Date** vagy **Unspecified**  

---

## Kiknek hasznos ez a kiadás  

- **Data Engineers:** ETL-eredmények validálása a digna Data Reconciliation segítségével  
- **Pénzügyi, kockázatkezelési és kontrolling csapatok:** Szabványos egyeztetési eljárások Exact szabályokként a digna Data Reconciliation modulban  
- **Data Quality & Governance csapatok:** Referenciális integritás különböző adatbázis-technológiák között a digna Engine segítségével  
- **Üzleti felhasználók:** Az adatokkal kapcsolatos üzleti kérdésekre AI-ágensek válaszolnak a digna Agentic segítségével  
- **AI- és automatizálási csapatok:** A dignával dolgozó AI-ágensek a digna Agentic révén  

---

## CLI frissítések  
- Nincs változás  

---