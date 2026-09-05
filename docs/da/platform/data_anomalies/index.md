---
title: digna Data Anomalies | AI-drevet observabilitet af data
description: digna Data Anomalies er en del af digna Data Observability Platform. Den lærer automatisk mønstre i dine data og opdager anomalier for at forbedre datakvaliteten og observabiliteten på tværs af databaser, data lakes og warehouses.
tags:
  - datakvalitet
  - dataobservabilitet
  - kvalitet af data
  - observabilitet af data
  - AI-drevet overvågning
  - anomaliedetektion
  - digna
  - digna platform
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – AI-baseret detektion af datakvalitetsproblemer

**AI-drevet observabilitet for konstant datatillid**

digna Data Anomalies er en del af **digna Data Observability Platform** — en modulær løsning, der forbedrer **datakvaliteten** ved kontinuerligt at analysere, hvordan datasæt opfører sig over tid.

Den lærer automatisk, hvordan “normal” ser ud for dine data, og alarmerer, når adfærden ændrer sig — uden at du skal definere statiske tærskler eller skrive en eneste regel.  
Modulet kører direkte i din database, så data aldrig forlader dit miljø.

---

## Formålet med digna Data Anomalies

Modulet **digna Data Anomalies** leverer kontinuerlig **observabilitet af data** ved at beregne og spore foruddefinerede statistiske metrikker såsom:

- Datavolumen og rekordtællinger  
- Andel manglende værdier  
- Værdifordelinger og histogrammer  
- Numeriske intervaller og gennemsnit  
- Kolonneunikhed og tekstlængder  

Disse metrikker indsamles automatisk for hvert datasæt.  
På baggrund af dem bygger digna modeller, der repræsenterer den typiske adfærd for hver metrik — og lærer daglige, ugentlige eller sæsonmæssige mønstre.  
Når modellerne er trænede, forudsiger modulet forventede værdier for nye data og detekterer afvigelser, som kan indikere kvalitetsproblemer, procesfejl eller ændringer upstream.

---

## Nøglefunktioner

- Lærer forventet dataadfærd automatisk ved hjælp af AI — ingen konfiguration af tærskler.  
- Opfanger pludselige fald, spring eller drift i datavolumen og fordelinger.  
- Identificerer byttede kolonner eller forkerte mappinger mellem attributter.  
- Fremhæver uventede kategoriske værdier (f.eks. nye regioner eller koder).  
- Understøtter alle kolonnetyper: numeriske, kategoriske eller uspecificerede.  
- Kører fuldstændigt i kundens miljø — ingen dataoverførsel.  
- Integreres med **digna Data Analytics** for langsigtet trendanalyse.

---

## Sådan fungerer det

### Trin 1 – Beregning af metrikker
digna beregner et sæt profilmetrikker for hver tabel og kolonne.  
Disse metrikker beskriver strukturen og den statistiske adfærd i dine data og gemmes til videre analyse.

### Trin 2 – Modeltræning
Baseret på historiske metrikværdier træner digna kompakte maskinlæringsmodeller (signature models), der indfanger det normale spænd for hver metrik.

### Trin 3 – Automatisk tærskelbestemmelse
Ved hjælp af *conformal inference* beregner digna adaptive konfidensintervaller (auto-thresholds), som tilpasser sig din data.  
Hvis nye metrikværdier falder uden for det forudsagte område, markeres de som anomalier.

Denne kontinuerlige feedback-loop sikrer, at overvågningen forbliver relevant, også når datamængder eller mønstre naturligt ændrer sig.

---

## Eksempelscenarier

### Uventet fald i antal poster
Et datasæt indeholder typisk omkring 500.000 poster om dagen.  
Når en ny levering kun indeholder 50.000 poster, markerer digna en anomali og viser, hvor stort afvigelsen er i forhold til det lærte område.

### Påvisning af byttede kolonner
Gennemsnitslængden af strengen i `last_name` matcher pludselig den i `first_name`.  
digna genkender afvigelsen i metrikmønstrene og signalerer en potentiel kolonnebytte.

### Uventet kategori fundet
En kolonne med østrigske byer indeholder pludselig “Zurich”.  
Baseret på historiske fordelinger markerer digna den nye værdi som uventet og advarer brugeren.

---

## Integration med andre moduler

- **digna Data Analytics** — aggregerer anonymitetshistorik og volatilitetmetrikker for at afdække langsigtede trends.  
- **digna Data Validation** — håndhæver eksplicitte forretningsregler til deterministiske kvalitetskontroller.  
- **digna Data Timeliness** — overvåger ankomsttider for data og korrelerer forsinkelser med anomalihændelser.  
- **digna Data Schema Tracker** — opdager strukturelle ændringer, som kan forklare nye anomalier.

---

## Typiske anvendelsestilfælde

- Opdagelse af manglende eller duplikerede dataloads.  
- Identifikation af byttede eller trunkerede kolonner.  
- Detektion af fordelingdrift i numeriske eller kategoriske features.  
- Fund af uventede referenceværdier eller koder.  
- Overvågning af kontinuerlige ingest-pipelines for uregelmæssigheder.  
- Sporing af den overordnede **kvalitet og observabilitet af data** på tværs af domæner.

---

## Fordele

- Øjeblikkelig opdagelse af unormal dataadfærd.  
- Eliminering af manuel tærskeljustering.  
- Reducerer driftsindsats for store dataomgivelser.  
- Opbygger tillid til analyse- og rapportsystemer.  
- Styrker **datakvaliteten** og end-to-end **dataobservabilitet**.

---

## Relaterede digna-moduler

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — trends og volatilitetmetrikker.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — regelbaseret dataverifikation.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — overvågning af dataleveringsplaner.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — detektion af skemændringer.

---

## Resumé

Modulet **digna Data Anomalies** udgør kernen i dignas AI-drevne **Data Observability Platform**.  
Ved kontinuerligt at overvåge nøglemetrikker, lære mønstre og identificere afvigelser hjælper det organisationer med at sikre, at **datakvaliteten** forbliver pålidelig, stabil og forklarlig — uden manuel konfiguration.