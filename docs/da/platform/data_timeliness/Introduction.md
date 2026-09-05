---
title: Data Timeliness – Overvågning af rettidig levering | digna Dokumentation
description: Lær, hvordan digna Data Timeliness sikrer, at data ankommer til forventet tid. Opdag forsinkede eller manglende leverancer, overvåg SLA'er, og beskyt forretningsprocesser mod skjulte forsinkelser. AI-drevet detektion for forbedret datakvalitet og observabilitet af datapipelines.
image: /assets/logo_square.png
keywords:
  - data rettidighed
  - leveringsovervågning
  - datakvalitet
  - kvalitet af data
  - observabilitet af data
  - forsinket data detektion
  - manglende data varsling
  - sla overvågning
  - ai leveringsanalyse
  - digna data timeliness
lang: da
robots: index, follow
og_title: Data Timeliness – Overvågning af rettidig levering | digna Dokumentation
og_description: digna Data Timeliness opdager automatisk forsinkede eller manglende dataleverancer ved hjælp af AI. Beskyt forretningsprocesser, overvåg SLA'er, og sikre rettidig, pålidelig data i alle pipelines.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI-drevet Data Timeliness-modul til datakvalitet og observabilitet – digna</h1>

---

## Formål

Modulet **Data Timeliness** sikrer, at **data ankommer til tiden** – hver gang.  
Det overvåger løbende leveringsplaner og opdager automatisk, når datasæt, tabeller eller filer er **forsinkede, manglende eller ufuldstændige**.  

Ved at kombinere AI-læring med brugerdefinerede tidsplaner gør *digna* det muligt for organisationer at forhindre downstream-fejl og opretholde strenge **SLA (Service Level Agreement)**-mål for både **Data Quality** og **observabilitet af datapipelines**.

---

## Teknisk oversigt

### To overvågningsmåder
- **AI-lærte ankomstmønstre**  
  digna lærer automatisk den naturlige rytme i dine dataleverancer — dagligt, timebaseret eller hendelsesdrevet — ved at analysere historiske tidsstempler og færdiggørelsestider.  
  Den tilpasser sig ændringer i forretningskalendere, weekender eller månedsafslutningsspidsbelastninger.

- **Brugerdefinerede tidsplaner**  
  Brugere kan eksplicit definere forventede leveringstider (fx *hver hverdag før 07:30*).  
  digna sammenligner den faktiske ankomsttid med den planlagte tidsplan og udløser advarsler, når data er forsinkede eller mangler.

### Detektionsmekanisme
- Evaluerer **metadata-tidsstempler**, **posttællinger** og **tabelfreshness**  
- Registrerer **stagnerede ETL-jobs**, **mislykkede ekstraktioner** og **delvise filleverancer**  
- Integrerer med *Data Anomalies* og *Data Validation* for kombinerede indsigter

---

## Detektionsscenarier

| Scenario | Beskrivelse |
|-----------|--------------|
| **Sen dataankomst** | Daglig markeddatastrøm forsinket med to timer, hvilket gør at rapporter ikke når SLA'er |
| **Manglende indlæsning** | En planlagt tabel eller partition er ikke opdateret for den aktuelle dato |
| **Kædede afhængighedsforsinkelse** | Forsinkelse i upstream-job påvirker downstream pipeline-refresh |
| **Weekend mønsterskift** | AI-modellen tilpasser sig automatisk, når der ikke forventes data om søndagen |

---

## Arkitektur og eksekvering

- **Kørsel i databasen:** digna udfører timeliness-tjek direkte i din database eller datawarehouse.  
- **Letvægtig metadataadgang:** læser jobtidsstempler, posttællinger og partitioninfo — ingen dataekstraktion nødvendig.  
- **Konfigurerbar frekvens:** planlæg overvågning per datasæt, schema eller pipeline.  
- **Tværmodulære advarsler:** resultater kan udløse visuelle advarsler i *Inspection Hub* eller meddelelser via e-mail, Slack eller API.  

---

## Eksempler på anvendelser

- **Finansielle markedsfeeds:** opdag forsinkelser i opdateringer af pris- eller handelsdata.  
- **Data Warehouse-indlæsninger:** overvåg når natlige ETL-jobs færdiggøres senere end forventet.  
- **Datarating mellem teams:** sikr, at afdelingsdata leveres inden daglige cutoffs.  
- **Regulatorisk rapportering:** bekræft, at indberetninger indeholder det seneste tilgængelige datasnapshot.  

---

## Fordele

| Område | Fordel |
|------|----------|
| **Forretningskontinuitet** | Forhindrer operationelle forstyrrelser pga. forsinkede eller manglende data |
| **Data Quality** | Forbedrer pålidelighed og konsistens i datapipelines |
| **Overholdelse** | Sikrer SLA-overholdelse og revisionsgennemsigtighed |
| **Automatisering** | AI eliminerer manuel overvågning af tidsplaner |
| **Integration** | Arbejder sømløst sammen med *Data Analytics* for at visualisere timeliness-tendenser over tid |

---

## Hvordan digna lærer forventede leveringstider

1. **Historisk analyse:** digna observerer tidligere indlæsningstider og varigheder.  
2. **AI-modellering:** Maskinlæring skaber en dynamisk baseline for forventet ankomst.  
3. **Overvågning:** Hver ny levering sammenlignes med baseline.  
4. **Alertering:** Afvigelser udløser advarsler med kontekstuelle målinger og konfidensscorer.  

Denne kontinuerlige læringstilgang tilpasser sig udviklende processer samtidig med, at falske positiver holdes lave.

---

## Ofte stillede spørgsmål

**Kan jeg definere mine egne leveringstider?**  
Ja. digna understøtter både faste brugerdefinerede tidsplaner og AI-lærte mønstre.

**Kan det integreres med mit ETL- eller orkestreringsværktøj?**  
Ja. digna integrerer med værktøjer såsom Airflow, dbt, Informatica eller brugerdefinerede schedulere.

**Hvor foregår beregningen?**  
Al analyse kører inden for din database eller cloud-warehouse — ingen ekstern service anvendes.

**Hvad sker der, når data er forsinkede?**  
digna udløser advarsler i dashboardet, Inspection Hub og via API/webhooks for at underrette driftsteams øjeblikkeligt.

---


**digna Data Timeliness** hjælper med at sikre **tillid til data**, ved at kombinere **AI-drevet detektion**, **lokal kørsel**, og **data observabilitet** — alt sammen inden for dit kontrollerede miljø.