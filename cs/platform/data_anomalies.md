# digna Data Anomalies – AI-poháněné zjišťování problémů s kvalitou dat

**AI-poháněná pozorovatelnost pro nepřetržitou důvěru v data**

digna Data Anomalies je součástí **digna Data Observability Platform** — modulárního řešení, které zlepšuje **kvalitu dat** průběžnou analýzou chování datových sad v čase.

Automaticky se učí, jak „normální“ vypadá vaše data, a upozorní vás, když se chování změní — bez definování statických prahů nebo napsání jediného pravidla.  
Modul běží přímo ve vaší databázi, takže data nikdy neopouštějí vaše prostředí.

---

## Účel digna Data Anomalies

Modul **digna Data Anomalies** poskytuje nepřetržitou **pozorovatelnost dat** výpočtem a sledováním předdefinovaných statistických metrik, jako jsou:

- Objem dat a počet záznamů  
- Poměry chybějících hodnot  
- Rozdělení hodnot a histogramy  
- Numerické rozsahy a průměry  
- Unikátnost sloupců a délka textu  

Tyto metriky jsou automaticky sbírány pro každou datovou sadu.  
Na jejich základě digna vytváří modely, které reprezentují typické chování každé metriky — učí se denní, týdenní nebo sezónní vzory.  
Po natrénování modul predikuje očekávané hodnoty pro nová data a detekuje odchylky, které mohou indikovat problémy s kvalitou, selhání procesů nebo změny ve zdrojích.

---

## Klíčové schopnosti

- Automaticky se učí očekávané chování dat pomocí AI — bez konfigurace prahů.  
- Detekuje náhlé poklesy, výkyvy nebo drift v objemu dat a rozděleních.  
- Identifikuje prohozené sloupce nebo nesprávná mapování atributů.  
- Zvýrazňuje neočekávané kategoriální hodnoty (např. nové regiony nebo kódy).  
- Podporuje všechny typy sloupců: numerické, kategoriální i nedefinované.  
- Funguje kompletně v zákaznickém prostředí — bez přesunu dat.  
- Integruje se s **digna Data Analytics** pro dlouhodobou analýzu trendů.

---

## Jak to funguje

### Krok 1 – Výpočet metrik
digna vypočítává sadu profilových metrik pro každou tabulku a sloupec.  
Tyto metriky popisují strukturu a statistické chování vašich dat a jsou uloženy pro další analýzu.

### Krok 2 – Trénink modelu
Na základě historických hodnot metrik digna natrénuje kompaktní strojové modely (signature models), které zachycují normální rozsah každé metriky.

### Krok 3 – Automatické stanovení prahů
Pomocí *conformal inference* digna vypočítá adaptivní intervaly spolehlivosti (auto-thresholds), které se vyvíjejí spolu s vašimi daty.  
Pokud nové hodnoty metrik spadnou mimo predikovaný rozsah, jsou označeny jako anomálie.

Tato nepřetržitá zpětná vazba zajišťuje, že monitorování zůstává relevantní i při přirozeném růstu objemu nebo změně vzorů v datech.

---

## Příklady scénářů

### Neočekávaný pokles počtu záznamů
Datová sada obvykle obsahuje kolem 500 000 záznamů denně.  
Když nová dodávka obsahuje pouze 50 000 záznamů, digna označí anomálii a ukáže, o kolik se hodnota liší od naučeného rozsahu.

### Detekce prohozených sloupců
Průměrná délka řetězce ve sloupci `last_name` náhle odpovídá délce ve `first_name`.  
digna rozpozná odchylku ve vzorcích metrik a signalizuje možnou výměnu sloupců.

### Detekce neočekávané kategorie
Sloupec obsahující rakouská města náhle obsahuje „Zurich“.  
Na základě historických rozdělení digna označí novou hodnotu jako neočekávanou a upozorní uživatele.

---

## Integrace s ostatními moduly

- **digna Data Analytics** — agreguje historii anomálií a metrik volatility pro odhalení dlouhodobých trendů.  
- **digna Data Validation** — vynucuje explicitní obchodní pravidla pro deterministické kontroly kvality.  
- **digna Data Timeliness** — monitoruje časy příchozích dat a koreluje zpoždění s výskytem anomálií.  
- **digna Data Schema Tracker** — detekuje strukturální změny, které mohou vysvětlit nové anomálie.

---

## Typické použití

- Detekce chybějících nebo duplicitních importů dat.  
- Identifikace prohozených nebo oříznutých sloupců.  
- Detekce driftu rozdělení u numerických nebo kategoriálních atributů.  
- Nalezení neočekávaných referenčních hodnot nebo kódů.  
- Monitorování kontinuálních ingestních pipeline pro nepravidelnosti.  
- Sledování celkové **kvality a pozorovatelnosti dat** napříč doménami.

---

## Přínosy

- Okamžitá detekce abnormálního chování dat.  
- Eliminuje ruční ladění prahů.  
- Snižuje provozní náklady ve velkých datových prostředích.  
- Buduje důvěru v analytické a reportingové systémy.  
- Posiluje **kvalitu dat** a end-to-end **pozorovatelnost dat**.

---

## Související moduly digna

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — metriky trendů a volatility.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — ověřování dat na základě pravidel.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — monitorování harmonogramů dodání dat.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — detekce změn schématu.

---

## Shrnutí

Modul **digna Data Anomalies** tvoří jádro dignaho AI-řízeného **Data Observability Platform**.  
Nepřetržitým sledováním klíčových metrik, učením vzorů a identifikací odchylek pomáhá organizacím zajistit, že **kvalita dat** zůstane důvěryhodná, stabilní a vysvětlitelná — bez manuální konfigurace.