---
title: Data Anomalies – Automatikus rendellenesség-felismerés az adatokban | digna Dokumentáció
description: Ismerd meg, hogyan észleli a digna Data Anomalies automatikusan a volumencsökkenéseket, hiányzó értékeket, eloszláseltolódásokat és váratlan mintázatokat manuális szabályírás nélkül. Javítsd az adatok minőségét és az adati folyamatok megfigyelhetőségét AI-alapú anomáliafelismeréssel.
image: /assets/logo_square.png
keywords:
  - adat anomáliák
  - ai anomália felismerés
  - adatminőség monitorozás
  - adatok minősége
  - adatok megfigyelhetősége
  - hiányzó adatok észlelése
  - adatvolumen monitorozás
  - eloszlás drift
  - adatok megbízhatósága
  - digna data anomalies
lang: hu
robots: index, follow
og_title: Data Anomalies – Automatikus észlelés | digna Dokumentáció
og_description: A digna Data Anomalies automatikusan észleli az adatok voluménében, értékeiben és eloszlásaiban előforduló rendellenességeket manuális szabályok nélkül — javítva az adatminőséget és megfigyelhetőséget több platformon.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Anomalies – Automatikus rendellenesség-felismerés
<h1 style="display:none;">AI-alapú modul az adatok minőségéhez és megfigyelhetőségéhez – digna Data Anomalies</h1>

---

## Cél

A **Data Anomalies** modul automatikusan felismeri a datasetjeidben előforduló rendellenességeket — nincs szükség szabályok írására.  
Folyamatosan monitorozza az **adatszolgáltatás minőségét**, megtanulva, mi a „normális”, és valós időben jelzi az eltéréseket.

AI-alapú észlelés révén a digna felfedi a „néma” adathibákat, például a hiányzó, duplikált vagy sérült rekordokat, amelyek torzíthatják a riportokat, ML-modelleket és dashboardokat.

---

## Technikai áttekintés

### Elemzett metrikák

digna folyamatosan profilozza az adataid az alábbi szempontokat:

- **Rekordvolumen** – sorok összesített száma, napi vagy batch-alapú  
- **Hiányzó értékek** – null vagy üres mezők detektálása  
- **Eloszlások és hisztogramok** – a mintázatváltozások monitorozása  
- **Értéktartományok** – automatikus extrém vagy határon túli értékek azonosítása  
- **Egyediségi vizsgálat** – duplikált kulcsok vagy ismétlődő bejegyzések ellenőrzése  

### Intelligens anomáliafelismerés

- **Történeti tanulást** alkalmaz a várható határok dinamikus definiálásához  
- Eltéréseket észlel a **volumenben, értékeloszlásokban vagy logikai összefüggésekben**  
- AI-t használ a küszöbértékek automatikus adaptálására napi időpontok vagy szezonális minták alapján  
- Megkülönbözteti a **statisztikai ingadozásokat** a valós anomáliáktól  
- Részletes metrikákat és konfidencia-pontszámokat állít elő dataset- és oszlop-szinten  

---

## Észlelési forgatókönyvek

Az alábbiakban valós példák láthatók, amelyeket a **Data Anomalies** modul automatikusan észlel:

| Forgatókönyv | Leírás |
|-----------|--------------|
| **Volumencsökkenés vagy -kiugrások** | A napi tranzakciók felének hiánya, duplikált batch betöltések vagy hirtelen adatnövekedés |
| **Hiányzó vagy null értékek** | Adatkivonások lefutottak, de kritikus oszlopok üresek maradtak |
| **Eloszláseltolódások** | Az átlagos vásárlási összeg vagy régiónkénti tranzakciószám váratlanul megváltozik |
| **Oszlopcserék** | Olyan oszlopok, mint a *first_name* és *last_name* véletlenül felcserélődnek az ETL során |
| **Váratlan kategóriás értékek** | pl.: „Zurich” megjelenik az osztrák városok listájában |
| **Hirtelen egyediségi veszteség** | Korábban egyedi azonosítók elkezdenek duplikálódni upstream join hibák miatt |

---

## Architektúra és végrehajtás

- **Adatbázison belüli végrehajtás:** Az összes anomáliaészlelési logika *az adatbázismotoron belül* fut (Teradata, Snowflake, Databricks, PostgreSQL stb.)  
- **Nincs adatmozgatás:** digna csak metrikákat olvas, a nyers adatokat soha nem továbbítja külső helyre  
- **Inkrementális frissítések:** Minden futásnál csak az új adat-szegmenseket elemzi a hatékonyság érdekében  
- **Konfigurálható ellenőrzési gyakoriság:** Óránkénti, napi vagy upstream folyamatok által indított futások  
- **Eredménytárolás:** A metrikákat és anomália jelzéseket visszaírja a digna observability sémájába vizualizáció és riasztás céljából  

---

## Előnyök

| Terület | Előny |
|------|----------|
| **Automatizálás** | Elszámol több száz manuális SQL vagy szabálydefiníciótól |
| **Pontosság** | Olyan problémákat is felismer, amelyeket a statikus küszöbök gyakran elvétenek |
| **Skálázhatóság** | Milliós tételszámokat is hatékonyan monitoroz táblánként |
| **Integráció** | Zökkenőmentesen működik együtt a *Data Analytics*-szel trendanalízishez |
| **Megfelelőség** | Folyamatos kontrollt biztosít az **adatszolgáltatás minősége és megfigyelhetősége** felett |
| **Átláthatóság** | Minden anomáliához konfidencia-pontszámokat, időbélyegeket és okkódokat ad |

---

## Hogyan tanulja meg a digna, mi a „normális”

1. **Profilozási fázis:** digna metrikákat gyűjt a történeti datasetekből.  
2. **Tanulási fázis:** AI modellek azonosítják a visszatérő mintákat (szezonális, heti, napi).  
3. **Monitorozási fázis:** A jövőbeli dataseteket összehasonlítja a dinamikusan megtanult küszöbökkel.  
4. **Riasztási fázis:** A statisztikai konfidenciakereteket meghaladó eltéréseket anomáliaként jelzi.

Minden modell magyarázható, determinisztikus és vállalati adatmennyiségekre optimalizált.

---

## Példák felhasználási esetekre

- Adatminőség monitorozása **banki tranzakciós rendszerekben**  
- Betöltési hibák detektálása **ETL vagy adat-raktár munkafolyamatokban**  
- Rendellenes ügyféltevékenység azonosítása **telekommunikációs rekordokban**  
- Klinikai adatok konzisztenciájának megfigyelése **egészségügyi analitika csatornákban**  
- Törött dashboardok megelőzése **BI és riportolási környezetekben**

---

## Gyakran ismételt kérdések

**Szükség van előre definiált szabályokra a Data Anomalies használatához?**  
Nem — a modul automatikusan tanul az adatok viselkedéséből.

**Megadhatok mégis speciális küszöböket, ha szükséges?**  
Igen. digna lehetővé teszi az AI-alapú és szabályalapú észlelés kombinálását (a *Data Validation* segítségével).

**Hogyan csökkentik a hamis riasztásokat?**  
A modul adaptív tanulást és statisztikai konfidencia-értékelést használ, hogy figyelmen kívül hagyja a normális szezonális ingadozásokat.

**Hol történik a számítás?**  
Az összes feldolgozás az adatbázisodon belül történik — digna soha nem emeli ki a nyers adatokat.

**Alkalmas érzékeny vagy szabályozott adatokhoz?**  
Igen. digna teljesen **on-premises vagy privát felhőben** futtatható, és megfelel az európai megfelelőségi szabványoknak.

---