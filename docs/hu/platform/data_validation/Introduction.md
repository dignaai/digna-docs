---
title: Data Validation – Szabályalapú ellenőrzések a megfeleléshez és auditálhatósághoz | digna Dokumentáció
description: Fedezze fel, hogyan érvényesíti a digna Data Validation determinisztikus, szabályalapú ellenőrzéseket küszöbértékekkel, tartományokkal és referencialistákkal. Biztosítsa a megfelelést, az auditálhatóságot és a szabályozói jelentéstételt a pénzügyi, egészségügyi és más adatszenzitív iparágakban.
image: /assets/logo_square.png
keywords:
  - data validation
  - szabályalapú adatellenőrzések
  - adatminőség
  - az adatok minősége
  - data observability
  - küszöbértékek és tartományok
  - referencialista ellenőrzés
  - auditálhatóság
  - megfelelés-ellenőrzés
  - digna Data Validation
lang: hu
robots: index, follow
og_title: Data Validation – Szabályalapú ellenőrzések a megfeleléshez és auditálhatósághoz | digna Dokumentáció
og_description: A digna Data Validation determinisztikus, szabályalapú ellenőrzéseket érvényesít küszöbértékekkel, tartományokkal és referencialistákkal. Szabályozott iparágak számára tervezve, biztosítja a megfelelést, az átláthatóságot és az auditálhatóságot.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

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
