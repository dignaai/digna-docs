---
title: digna Vydání 2026.04 | Analytics Chart, Enumerations & Validation Rule Templates
description: Zjistěte, co je nového ve vydání digna 2026.04. Tato verze přináší pokročilou analýzu časových řad pomocí Analytics Chart, znovupoužitelné šablony validačních pravidel, enumerations pro povolené hodnoty a podmínky relevance na úrovni sloupců.
keywords: digna Release 2026.04, digna changelog, digna Data Analytics, time series analysis, regression, data validation templates, enumerations, allowed values validation, data quality rules, data observability
image: /assets/logo_square.png
---

# Záznam změn – Vydání 2026.04  

Ve vydání 2026.04 digna významně rozšiřuje své schopnosti v oblasti analytiky a validace dat.  
Tato verze představuje pokročilou analýzu časových řad, znovupoužitelné validační komponenty a centralizovanou standardizaci hodnot.

---

## 🚀 Nové funkce  

### Analytics Chart – analýza časových řad bez data science  
- Nový **Analytics Chart** pro interaktivní analýzu časových řad  
- Vestavěné analytické metody:
    - Lineární, kvadratická a kubická regrese  
    - Piecewise regrese s konfigurovatelnými breakpoints  
    - Techniky vyhlazování  
    - Kvantilová analýza  
- Automatická identifikace trendů, seasonality a změn vzorů  
- Analýza reziduí pro hlubší vhled do odchylek  
- Časové řady jsou automaticky počítány pro každou datovou sadu  

**Dopad:** Umožňuje uživatelům porozumět složitému chování dat v čase bez potřeby odborných znalostí data science nebo externích nástrojů.

---

### Enumerations – centrální definice povolených hodnot  
- Definujte znovupoužitelné sady povolených hodnot (např. země, státy, stavové kódy)  
- Validujte hodnoty sloupců proti předdefinovaným enumeracím v **digna Data Validation**  
- Znovupoužívejte enumerace napříč projekty a zdroji dat  
- Používejte enumerace všude přes `#ENUM:MY_ENUM#`  
- Všechny kontroly se provádějí **přímo v zdrojové databázi**  

**Dopad:** Zajišťuje konzistentní a standardizované hodnoty dat napříč organizací.

---

### Validation Rule Templates – znovupoužitelná logika datové kvality  
- Definujte znovupoužitelné validační pravidla (např. kontroly mezer, NOT NULL, kontroly formátu)  
- Aplikujte šablony napříč více datovými sadami  
- Zajistěte konzistentní logiku pravidel mezi projekty  
- Snižte duplikaci a manuální konfiguraci  
- Všechny kontroly se provádějí **přímo v zdrojové databázi**  

**Dopad:** Umožňuje škálovatelnou a vysokovýkonnou validaci dat bez přesunu dat.

---

### Podmínky relevance na úrovni statistik sloupce  
- Definujte podmínky relevance na **úrovni sloupce pro každou statistiku**  
- Rozšiřuje koncept podmínek relevance anomálií  
- Řiďte, kdy by měla být statistika považována za relevantní  
- Snižte šum v datech vyloučením méně kritických situací  

**Dopad:** Zlepšuje kvalitu signálu tím, že se soustředí pouze na významné odchylky.

---

## 🧪 Rozšířené možnosti Data Analytics a validace  

S tímto vydáním digna rozšiřuje jak schopnosti pro porozumění datům, tak standardizaci validace:

- Pokročilá interpretace časových řad bez nutnosti znalostí data science  
- Centralizovaná definice **povolených hodnot pomocí Enumerations**  
- Znovupoužitelná **validační logika pomocí šablon**  
- Jemnozrnná kontrola relevance statistik a upozornění  

Tyto schopnosti organizacím umožňují nejen detekovat problémy, ale také **porozumět, standardizovat a kontrolovat kvalitu dat**.

---

## 🎯 Kdo z tohoto vydání profitujete  

- Datoví inženýři: znovupoužitelná validační logika a lepší kontrola monitoringu  
- Týmy pro kvalitu dat a správu (Data Quality & Governance): standardizovaná pravidla a konzistentní validace napříč systémy  
- Týmy Analytics & BI: lepší porozumění trendům a odchylkám  
- Majitelé platforem: vyšší adopce díky zjednodušené analytice a škálovatelné validaci  

---

## 🛠 Aktualizace CLI  
- Žádné změny  

---