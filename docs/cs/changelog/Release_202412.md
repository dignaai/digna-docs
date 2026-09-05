---
title: digna Release 2024.12 | Changelog & New Features
description: Objevte novinky v digna Release 2024.12. Tato verze přináší vestavěný plánovač, PDF reporty, flexibilní vlastní sloupce, dynamické zástupné symboly pro snapshot dotazy a chytřejší optimalizaci prahů pro lepší detekci anomálií a monitorování kvality dat.
keywords: digna Release 2024.12, digna changelog, release notes, built-in scheduler, PDF reports, custom column type, snapshot query placeholders, threshold optimization, data observability, data quality monitoring, anomaly detection
image: /assets/logo_square.png
---



# Changelog – Release 2024.12

Release 2024.12 přináší sadu nových funkcí a vylepšení, která činí dignu více automatizovanou, flexibilní a připravenou pro byznys.  
Tato verze zlepšuje plánování, reporting, zpracování dotazů a přesnost detekce anomálií.  

---

## Nové funkce

### Vestavěný plánovač
Inspekce už nezávisí pouze na příkazovém řádku nebo API voláních.  
S **novým digna Schedulerem** lze inspekce spouštět automaticky v definovaných časech.  

- Podporuje **Cron expressions** pro opakované plánování (denně, týdně nebo vlastní intervaly).  
- Nabízí přesnou kontrolu pomocí **offsetů**, **start date** a **end date**.  
- Umožňuje týmům zajistit, že všechny kritické zdroje dat jsou kontrolovány konzistentně a bez manuálního zásahu.  

---

### Reporty ve formátu PDF
Týmy nyní mohou snadno sdílet výsledky se zainteresovanými stranami prostřednictvím **exportů do PDF**.  

- Grafy, metriky a výsledky anomálií lze exportovat v profesionálním PDF formátu.  
- Reporty kombinují **vizualizace** a **základní data**, aby vyhovovaly jak technickým, tak byznys uživatelům.  
- Odstraňuje potřebu externích nástrojů pro tvorbu reportů.  

---

### Nový typ sloupce: `CUSTOM`
Pro větší flexibilitu digna zavádí nový **`CUSTOM` typ sloupce**.  

- Uživatelé mohou přesně definovat, jaké **statistiky a metriky** se aplikují na konkrétní atributy.  
- Ideální pro speciální případy, které nezapadají do standardních kategorií jako NUMERICAL nebo CATEGORICAL.  
- Pomáhá udržet analýzy cílené a výsledky relevantní v kontextu byznysu.  

---

### Nové zástupné symboly v snapshot dotazech
Snapshot dotazy jsou nyní jednodušší a méně náchylné k chybám díky **dynamickým placeholderům**.  

- Tokeny jako `#date+n#` nebo `#date-n#` automaticky upravují datum v dotazech.  
- Příklad:  
  - `#date+1#` → zítra  
  - `#date-2#` → před dvěma dny  
- Odstraňuje ruční výpočty datumů a zajišťuje konzistenci napříč týmy.  

---

### Optimalizace prahových hodnot
Prahové hodnoty pro anomálie jsou nyní inteligentnější a kontextově uvědomělé.  

- Pro metriky jako **NULL COUNT** jsou dolní prahy automaticky omezeny na **0**.  
- Zabraňuje neplatným nebo nesmyslným prahem.  
- Výsledkem je méně falešných poplachů a spolehlivější detekce anomálií.  

---

## Obecná vylepšení
- Vylepšené **UI komponenty** ve zobrazeních konfigurace projektů a atributů.  
- Lepší výkon **dashboardu** pro velké objemy dat.  
- Vylepšené **logování a chybové zprávy** pro snadnější řešení problémů.  

---

## Shrnutí
Release 2024.12 posiluje dignu jako platformu pro **kvalitu dat, detekci anomálií a observabilitu dat**.  
S automatizací pomocí plánování, sdílitelnými PDF reporty, přizpůsobitelnými sloupci, zjednodušenými snapshot dotazy a chytřejšími prahy se digna stává ještě cennějším nástrojem pro technické i byznys uživatele.