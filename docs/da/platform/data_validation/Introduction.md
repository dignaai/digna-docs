---
title: Data Validation – Regelsatte Kontroller for Overholdelse & Revisionsspor | digna Dokumentation
description: Opdag hvordan digna Data Validation håndhæver deterministiske, regelsatte kontroller med tærskler, intervaller og referencelister. Sikr overholdelse, revisionsspor og rapportering til tilsynsmyndigheder inden for finans, sundhedsvæsen og andre datakritiske industrier.
image: /assets/logo_square.png
keywords:
  - data validation
  - rule-based data checks
  - data quality
  - quality of data
  - data observability
  - thresholds and ranges
  - reference list validation
  - auditability
  - compliance monitoring
  - digna data validation
lang: da
robots: index, follow
og_title: Data Validation – Regelsatte Kontroller for Overholdelse & Revisionsspor | digna Dokumentation
og_description: digna Data Validation håndhæver deterministiske, regelsatte kontroller med tærskler, intervaller og referencelister. Designet til regulerede brancher sikrer det overholdelse, gennemsigtighed og revisionsspor.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Regelsatte Kontroller
<h1 style="display:none;">AI-drevet Data Validation-modul for datakvalitet og observabilitet – digna</h1>

---

## Purpose

The **Data Validation** module sikrer **kvaliteten af data** gennem præcise, regelsatte kontroller.  
Det giver organisationer mulighed for at definere deterministisk forretnings- og teknisk valideringslogik og sikrer, at data opfylder compliance-standarder, kontraktlige SLA'er og regulatoriske krav.

Ved at kombinere *in-database rule execution*, *komplette revisionsspor* og *integration med andre digna-moduler* garanterer **Data Validation** konsekvent og sporbar **datakvalitet og observerbarhed** på tværs af komplekse virksomhedslandskaber.

---

## Technical Overview

### Supported Validation Types

- **Equality Checks**  
  Bekræft, at værdier stemmer overens med forventede resultater (f.eks. referencekoder, boolske flag, kategorimappinger).

- **Thresholds & Ranges**  
  Valider numeriske målinger eller KPI'er mod definerede grænser — statiske eller dynamisk afledte.

- **Reference Lists & Lookups**  
  Tjek om feltværdier findes i godkendte masterdatasæt (f.eks. momsnumre, ISO-landelister, produktkataloger).

- **Cross-Column Consistency**  
  Sikr relationsmæssig korrekthed (f.eks. at valuta stemmer overens med region, at risikokategori matcher aktivtype).

- **Null Handling Rules**  
  Opdag uventede null- eller tomme værdier i kritiske kolonner.

### Execution and Logging

- **In-Database Processing** – Alle valideringsregler køres direkte i din database (Teradata, Snowflake, Databricks, PostgreSQL osv.).  
- **No Data Extraction** – digna overfører aldrig rådata uden for dit miljø.  
- **Full Traceability** – Hvert regels resultat logges med tidsstempel, ansvarligt dataset, posttællinger og bestået/ikke-bestået udfald.  
- **Revision**
