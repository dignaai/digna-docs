---
title: Data Schema Tracker – Overvåg skemaudvikling | digna Dokumentation
description: Lær hvordan digna Data Schema Tracker overvåger kolonneændringer, datatypeopdateringer og schema drift. Opdag og alarmer om både tilsigtede og utilsigtede skemaændringer for at forhindre ETL-fejl, ødelagte dashboards og tab af dataobservability.
canonical_url: https://docs.digna.ai/platform/data_schema_tracker/
image: /assets/logo_square.png
keywords:
  - data schema tracker
  - schema drift detection
  - overvågning af skemaudvikling
  - metadata observability
  - data observability
  - datakvalitet
  - overvågning af datastruktur
  - database metadata
  - etl pipeline stabilitet
  - digna data schema tracker
lang: da
robots: index, follow
og_title: Data Schema Tracker – Overvåg skemaudvikling | digna Dokumentation
og_description: digna Data Schema Tracker overvåger schema drift, datatypeændringer og kolonneopdateringer. Modtag alarmer før ETL-pipelines eller dashboards fejler pga. uventede strukturændringer.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Overvåg skemaudvikling
<h1 style="display:none;">AI-drevet modul til metadata observability og datakvalitet – digna Data Schema Tracker</h1>

---

## Formål

Den **Data Schema Tracker** holder dig orienteret om, hvordan dine databasestrukturer udvikler sig.  
Den overvåger løbende **tabelskemaer, kolonner og datatyper** for at opdage **schema drift** — tilsigtede eller utilsigtede strukturændringer, der kan forstyrre pipelines, ETL-jobs eller BI-dashboards.

Ved at sikre gennemsigtighed i skemaudvikling hjælper digna organisationer med at opretholde **tillid til datakvaliteten**, bevare **observability af datasystemer** og undgå dyre produktionshændelser forårsaget af uopdagede skemaændringer.

---

## Teknisk oversigt

### Hvad den overvåger

- **Tilføjede eller fjernede kolonner** – Registrerer nyintroducerede, omdøbte eller slettede kolonner.  
- **Ændringer i datatyper** – Identificerer ændringer som `INT → VARCHAR` eller `DATE → TIMESTAMP`.  
- **Ændringer i tabeller og views** – Sporer oprettelse, omdøbning eller fjernelse af tabeller og views.  
- **Forskelle på tværs af miljøer** – Sammenligner skemaversioner mellem Dev, Test og Production-miljøer.  

### Detektion & alarmering

- Scanner **database metadata** eller **systemkataloger** direkte inden for din dataplatform.  
- Sammenligner hvert skema-snapshot med den tidligere kendte version, som er lagret i digna’s observability schema.  
- Genererer **real-time alarmer** i dashboardet, via API eller eksterne notifikationskanaler (email, Slack, webhook).  
- Logger hver skema-version til **historisk sporing og revisionsparathed**.

---

## Arkitektur og eksekvering

- **Kørsel i databasen:** digna kører fuldstændigt i dit miljø og forespørger metadata-views uden at ekstraktere nogen data.  
- **Letvægts scanning:** tilgår kun strukturel information — aldrig brugerdata.  
- **Centraliseret lagring:** skemametadata og drift-poster gemmes i digna observability schema til visualisering og analyse.  
- **Automation:** understøtter planlagte eller hændelsesbaserede scanninger via digna Core eller eksterne orkestreringsværktøjer.  

---

## Eksempler på brugstilfælde

| Brugstilfælde | Beskrivelse |
|-----------|--------------|
| **Overvågning af ETL-stabilitet** | Opdag ændringer i upstream-strukturen, før pipelines fejler pga. skema-uoverensstemmelser. |
| **Business Intelligence-pålidelighed** | Forebyg ødelagte dashboards forårsaget af omdøbte eller manglende kolonner. |
| **Governance i Data Warehouse** | Oprethold en reviderbar historik over skemaudvikling til compliance og konsekvensanalyse. |
| **Integrationsovervågning** | Sikr, at data lake- og warehouse-skemaer forbliver synkroniserede efter strukturændringer. |

---

## Fordele

| Område | Fordel |
|------|----------|
| **Datakvalitet** | Forhindrer uopdaget schema drift, der kan korruptere eller ugyldiggøre datapipelines. |
| **Observability** | Tilføjer strukturel overvågning til den samlede observability af dataøkosystemer. |
| **Compliance** | Vedligeholder versioneret skemahistorik til revision, sporbarhed og ændringskontrol. |
| **Forebyggelse** | Finder strukturelle problemer, før de eskalerer til fejl i rapportering eller produktion. |

---

## Hvordan det virker

1. **Snapshot-indsamling** – digna indsamler den aktuelle skemametadata.  
2. **Sammenligning** – det nye snapshot sammenlignes