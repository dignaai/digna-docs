# Data Anomalies – Automatické zjišťování
<h1 style="display:none;">Modul poháněný AI pro kvalitu a observabilitu dat – digna Data Anomalies</h1>

---

## Účel

Modul **Data Anomalies** automaticky identifikuje nepravidelnosti ve vašich datových sadách — bez nutnosti psát pravidla.  
Nepřetržitě sleduje **kvalitu doručování dat**, učí se, jak vypadá „normál“, a detekuje odchylky v reálném čase.

Díky detekci založené na AI rozpoznává digna *tiché chyby v datech* jako chybějící, duplikované nebo poškozené záznamy, které mohou zkreslit reporty, ML modely a dashboardy.

---

## Technický přehled

### Analyzované metriky

digna nepřetržitě profiluje následující aspekty vašich dat:

- **Objem záznamů** – celkový počet řádků, denní nebo dávkově  
- **Chybějící hodnoty** – detekce null nebo prázdných polí  
- **Distribuce a histogramy** – sledování změn tvaru dat  
- **Rozsahy hodnot** – automatická identifikace hodnot mimo rozsah nebo extrémních hodnot  
- **Unikátnost** – kontroly na duplicitní klíče nebo opakující se záznamy  

### Inteligentní detekce anomálií

- Využívá **učení z historie** k dynamickému vymezení očekávaných hranic  
- Detekuje odchylky v **objemu, distribucích hodnot nebo logických vztazích**  
- Používá AI k automatickému přizpůsobení prahů podle denní doby nebo sezónních vzorců  
- Rozlišuje mezi **statistickými fluktuacemi** a skutečnými anomáliemi  
- Generuje podrobné metriky a skóre důvěryhodnosti pro každou datovou sadu a sloupec  

---

## Scénáře detekce

Níže jsou příklady reálných problémů, které modul **Data Anomalies** automaticky zachytí:

| Scénář | Popis |
|-----------|--------------|
| **Poklesy nebo výkyvy objemu** | Chybějící polovina denních transakcí, duplikované načtení dávky nebo náhlé přírůstky dat |
| **Chybějící nebo null hodnoty** | Extrakce dat dokončena, ale kritické sloupce zůstaly prázdné |
| **Posuny v distribucích** | Průměrná částka nákupu nebo počet transakcí na region se nečekaně změní |
| **Prohození sloupců** | Sloupce jako *first_name* a *last_name* byly při ETL omylem prohozeny |
| **Neočekávané kategorické hodnoty** | např. „Zurich“ se objeví v seznamu rakouských měst |
| **Náhlá ztráta unikátnosti** | Dříve unikátní ID začnou duplicitně vznikat kvůli chybě v upstream joinu |

---

## Architektura a provádění

- **Spuštění v databázi:** Veškerá logika detekce anomálií se vykonává *přímo v databázovém enginu* (Teradata, Snowflake, Databricks, PostgreSQL atd.)  
- **Žádný přesun dat:** digna čte pouze metriky, nikdy nepřenáší surová data externě  
- **Inkrementální aktualizace:** Při každém běhu se analyzují pouze nové segmenty dat pro efektivitu  
- **Konfigurovatelná frekvence inspekce:** Hodinově, denně nebo spuštěné událostí v upstream procesech  
- **Ukládání výsledků:** Metriky a příznaky anomálií se zapisují zpět do observability schématu digna pro vizualizaci a alertování  

---

## Výhody

| Oblast | Přínos |
|------|----------|
| **Automatizace** | Odstraní stovky ručně psaných SQL dotazů nebo definic pravidel |
| **Přesnost** | Detekuje problémy, které statické prahy často přehlédnou |
| **Škálovatelnost** | Efektivně monitoruje miliony záznamů na tabulku |
| **Integrace** | Bezproblémově spolupracuje s *digna Data Analytics* pro analýzu trendů |
| **Shoda** | Zajišťuje nepřetržitou kontrolu nad **kvalitou a observabilitou dat** |
| **Transparentnost** | Poskytuje skóre důvěry, časová razítka a kódy důvodů pro každou anomálii |

---

## Jak se digna učí „normál“

1. **Fáze profilování:** digna sbírá metriky z historických datových sad.  
2. **Fáze učení:** AI modely identifikují opakující se vzorce (sezónní, týdenní, denní).  
3. **Fáze monitorování:** Budoucí datové sady jsou porovnávány s dynamicky naučenými prahy.  
4. **Fáze upozornění:** Odchylky přesahující statistické hranice důvěry jsou hlášeny jako anomálie.  

Všechny modely jsou vysvětlitelné, deterministické a optimalizované pro podnikové objemy dat.

---

## Příklady použití

- Monitorování kvality dat v **systémech bankovních transakcí**  
- Detekce chyb načítání v **ETL nebo úlohách datového skladu**  
- Identifikace abnormální aktivity zákazníků v **telekomunikačních záznamech**  
- Sledování konzistence klinických dat v **analytických pipeline zdravotnictví**  
- Prevence rozbitých dashboardů v **BI a reportingových prostředích**

---

## Často kladené otázky

**Vyžaduje Data Anomalies předdefinovaná pravidla?**  
Ne — modul se učí chování dat automaticky.

**Mohu si přesto definovat konkrétní prahy, pokud potřebuji?**  
Ano. digna umožňuje kombinovat detekci založenou na AI a pravidlovou detekci (přes *Data Validation*).

**Jak jsou minimalizovány falešně pozitivní hlášení?**  
Modul používá adaptivní učení a statistické skórování důvěry, aby ignoroval běžné sezónní výkyvy.

**Kde probíhá výpočet?**  
Veškeré zpracování běží ve vaší databázi — digna nikdy nevytahuje surová data.

**Je vhodné pro citlivá nebo regulovaná data?**  
Ano. digna může běžet plně on-premises nebo v privátním cloudu a dodržuje evropské předpisy pro soulad.

---