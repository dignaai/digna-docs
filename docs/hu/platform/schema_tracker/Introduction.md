---
title: Data Schema Tracker – Séma evolúciójának nyomon követése | digna Dokumentáció
description: Ismerje meg, hogyan figyeli a digna Data Schema Tracker az oszlopváltozásokat, adattípus-frissítéseket és a séma driftet. Észlelje és riasztson szándékos és szándékolatlan sémaváltozások esetén, hogy megelőzze az ETL-hibákat, törött dashboardokat és az adatok megfigyelhetőségének elvesztését.
image: /assets/logo_square.png
keywords:
  - adat séma követés
  - séma drift észlelés
  - séma evolúció monitorozása
  - metaadat megfigyelhetőség
  - adat megfigyelhetőség
  - adatok minősége
  - adatstruktúra monitorozás
  - adatbázis metaadat
  - ETL csővezeték stabilitás
  - digna data schema tracker
lang: hu
robots: index, follow
og_title: Data Schema Tracker – Séma evolúciójának nyomon követése | digna Dokumentáció
og_description: A digna Data Schema Tracker figyeli a séma driftet, az adattípus-változásokat és az oszlopmódosításokat. Kapjon riasztásokat, mielőtt az ETL csővezetékek vagy a dashboardok meghibásodnának váratlan szerkezeti változások miatt.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Monitor Schema Evolution
<h1 style="display:none;">MI-vezérelt modul a metaadat-megfigyeléshez és az adatmínőséghez – digna Data Schema Tracker</h1>

---

## Cél

A **Data Schema Tracker** tájékoztatja Önt arról, hogyan változnak az adatbázis-struktúrái.  
Folyamatosan figyeli a **táblák sémáit, az oszlopokat és az adattípusokat**, hogy észlelje a **séma driftet** — legyen az szándékos vagy szándékolatlan szerkezeti változás, amely megszakíthatja a pipeline-okat, ETL feladatokat vagy BI dashboardokat.

A séma evolúció átláthatóságának biztosításával a digna segíti a szervezeteket abban, hogy megőrizzék az **adatok minőségébe vetett bizalmat**, fenntartsák az **adat rendszerek megfigyelhetőségét**, és elkerüljék a nem észlelt sémaváltozásokból eredő költséges éles problémákat.

---

## Műszaki áttekintés

### Mit figyel

- **Hozzáadott vagy eltávolított oszlopok** – Észleli az újonnan bevezetett, átnevezett vagy törölt oszlopokat.  
- **Adattípus-módosítások** – Azonosít olyan változásokat, mint `INT → VARCHAR` vagy `DATE → TIMESTAMP`.  
- **Táblák és nézetek módosításai** – Követi a táblák és nézetek létrehozását, átnevezését vagy eltávolítását.  
- **Környezeti különbségek** – Összehasonlítja a séma verziókat Dev, Test és Production környezetek között.  

### Észlelés és riasztás

- Közvetlenül a **adatbázis metaadatait** vagy a **rendszerkatalógusokat** vizsgálja az Ön adatplatformján belül.  
- Összehasonlítja az egyes séma pillanatképeket a digna megfigyelhetőségi sémájában tárolt korábban ismert verzióval.  
- **Valós idejű riasztásokat** generál a dashboardon, API-n keresztül vagy külső értesítési csatornákon (e-mail, Slack, webhook).  
- Naplózza minden séma verzióját a **történeti követés és audit-készültség** érdekében.

---

## Architektúra és végrehajtás

- **Adatbázison belüli végrehajtás:** a digna teljes egészében az Ön környezetében fut, metaadat-nézeteket lekérdezve anélkül, hogy bármilyen felhasználói adatot kinyerne.  
- **Könnyűsúlyú szkennelés:** csak strukturális információkat ér el — soha nem a felhasználói adatokat.  
- **Központosított tárolás:** a séma metaadatai és a drift rekordok a digna observability sémájában tárolódnak vizualizációhoz és elemzéshez.  
- **Automatizálás:** támogatja az ütemezett vagy eseményalapú vizsgálatokat a digna Core-on keresztül vagy külső orkestrációs eszközökkel.  

---

## Használati esetek

| Use Case | Leírás |
|-----------|--------------|
| **ETL stabilitás monitorozása** | Észlelje a feláramló struktúraváltozásokat, mielőtt a pipeline-ok meghibásodnának sémaeltérések miatt. |
| **Üzleti intelligencia megbízhatósága** | Megelőzheti a törött dashboardokat, amelyeket átnevezett vagy hiányzó oszlopok okoznak. |
| **Adatraktár kormányzás** | Fenntartja a séma evolúciójának auditálható történetét megfelelőség és hatáselemzés céljából. |
| **Integrációs felügyelet** | Biztosítja, hogy az adat-tó és az adatraktár sémái szinkronban maradjanak struktúrális frissítések után. |

---

## Előnyök

| Terület | Előny |
|------|----------|
| **Adatminőség** | Megakadályozza a nem észlelt séma driftet, amely tönkreteheti vagy érvénytelenítheti az adatcsővezetékeket. |
| **Megfigyelhetőség** | Strukturális monitorozást ad az adatökológia általános megfigyelhetőségéhez. |
| **Megfelelőség** | Verzionált séma történetet tart fenn audit, nyomonkövethetőség és változáskezelés céljából. |
| **Megelőzés** | Észleli a szerkezeti problémákat, mielőtt azok riportolási vagy éles hibákká fajulnának. |

---

## Hogyan működik

1. **Pillanatkép gyűjtése** – a digna rögzíti az aktuális séma metaadatait.  
2. **Összehasonlítás** – az új pillanatképet összehasonlítják
