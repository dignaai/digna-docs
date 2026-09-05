# Data Validation – Szabályalapú ellenőrzések
<h1 style="display:none;">Mesterséges intelligencia által vezérelt Data Validation modul az adatminőség és megfigyelhetőség számára – digna</h1>

---

## Cél

A **Data Validation** modul a **adatminőség** biztosítását szolgálja pontos, szabályalapú ellenőrzéseken keresztül.  
Lehetővé teszi a szervezetek számára, hogy determinisztikus üzleti és technikai érvényesítési logikát definiáljanak, biztosítva, hogy az adatok megfeleljenek a megfelelőségi előírásoknak, szerződéses SLA-knak és szabályozói követelményeknek.

Az *adatbázison belüli szabályvégrehajtás*, a *teljes auditálási nyomvonalak* és a *más digna modulokkal való integráció* kombinálásával a **Data Validation** konzisztens és nyomon követhető **adatminőséget és megfigyelhetőséget** garantál a komplex vállalati környezetekben.

---

## Technikai áttekintés

### Támogatott érvényesítési típusok

- **Egyenlőség-ellenőrzések**  
  Ellenőrzi, hogy az értékek megegyeznek-e a várt eredményekkel (pl. referenciakódok, logikai jelzők, kategóriák egyeztetése).

- **Küszöbértékek és tartományok**  
  Számértékek vagy KPI-k érvényesítése meghatározott korlátokhoz képest — statikus vagy dinamikusan származtatott módon.

- **Referencialisták és lekérdezések**  
  Ellenőrzi, hogy egy mező értéke szerepel-e az elfogadott master/adatkészletekben (pl. ÁFA-kódok, ISO országlisták, termékkatalógusok).

- **Oszlopok közötti konzisztencia**  
  Biztosítja a relációs helyességet (pl. valuta megfelel a régiónak, kockázati kategória illeszkedik az eszköztípushoz).

- **Null kezelési szabályok**  
  Felismeri a kritikus oszlopokban előforduló váratlan null vagy üres értékeket.

### Végrehajtás és naplózás

- **In-Database Feldolgozás** – Minden érvényesítési szabály közvetlenül az Ön adatbázisában fut (Teradata, Snowflake, Databricks, PostgreSQL stb.).  
- **Nincs Adatkivitel** – A digna soha nem viszi ki a nyers adatokat az Ön környezetéből.  
- **Teljes Nyomonkövethetőség** – Minden szabályeredmény időbélyeggel, felelős adathalmaz megjelöléssel, rekordszámmal és siker/sikertelenség eredménnyel kerül naplózásra.  
- **Audit**