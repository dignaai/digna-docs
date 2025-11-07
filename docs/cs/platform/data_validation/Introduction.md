---
title: Data Validation – Kontroly řízené pravidly pro shodu a auditovatelnost | digna Dokumentace
description: Zjistěte, jak digna Data Validation uplatňuje deterministické kontroly založené na pravidlech s prahy, rozmezími a referenčními seznamy. Zajistěte shodu, auditovatelnost a plnění regulačních hlášení ve financích, zdravotnictví a dalších odvětvích citlivých na data.
image: /assets/logo_square.png
keywords:
  - data validation
  - kontroly dat řízené pravidly
  - kvalita dat
  - úroveň kvality dat
  - observabilita dat
  - prahy a rozmezí
  - validace referenčních seznamů
  - auditovatelnost
  - monitorování shody
  - digna data validation
lang: cs
robots: index, follow
og_title: Data Validation – Kontroly řízené pravidly pro shodu a auditovatelnost | digna Dokumentace
og_description: digna Data Validation provádí deterministické kontroly založené na pravidlech s prahy, rozmezími a referenčními seznamy. Navrženo pro regulovaná odvětví, zajišťuje shodu, transparentnost a auditovatelnost.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Kontroly řízené pravidly
<h1 style="display:none;">Modul Data Validation řízený umělou inteligencí pro kvalitu dat a observabilitu – digna</h1>

---

## Účel

Modul **Data Validation** zajišťuje **kvalitu dat** prostřednictvím přesných kontrol založených na pravidlech.  
Umožňuje organizacím definovat deterministickou obchodní a technickou validační logiku, která zajišťuje, že data splňují standardy shody, smluvní SLA a regulatorní požadavky.

Kombinací *spouštění pravidel přímo v databázi*, *kompletních auditních stop* a *integrace s dalšími moduly digna*, **Data Validation** garantuje konzistentní a sledovatelnou **kvalitu dat a observabilitu** napříč složitými podnikovými prostředími.

---

## Technický přehled

### Podporované typy validací

- **Kontroly shody**  
  Potvrďte, že hodnoty odpovídají očekávaným výsledkům (např. referenční kódy, Booleovy příznaky, kategoriální mapování).

- **Prahy a rozmezí**  
  Validujte číselné metriky nebo KPI vůči definovaným limitům — statickým nebo dynamicky odvozeným.

- **Referenční seznamy a vyhledávání**  
  Zkontrolujte, zda hodnoty polí existují ve schválených master datech (např. DIČ, ISO seznam zemí, katalogy produktů).

- **Konzistence napříč sloupci**  
  Zajistěte relační správnost (např. měna odpovídá regionu, kategorie rizika souhlasí s typem aktiva).

- **Pravidla pro zpracování NULL hodnot**  
  Detekujte neočekávané NULL nebo prázdné hodnoty v kritických sloupcích.

### Provedení a protokolování

- **Zpracování přímo v databázi** – Všechna validační pravidla se spouštějí přímo ve vaší databázi (Teradata, Snowflake, Databricks, PostgreSQL atd.).  
- **Bez extrakce dat** – digna nikdy nepřenáší surová data mimo vaše prostředí.  
- **Plná sledovatelnost** – Každý výsledek pravidla je zaznamenán s časovou známkou, odpovědným datasetem, počty záznamů a výsledkem prošel/neprošel.  
- **Audit**
