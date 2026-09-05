---
title: Data Timeliness – Õigeaegse kohaletoimetamise jälgimine | digna Documentation
description: Saa teada, kuidas digna Data Timeliness tagab andmete õigeaegse saabumise. Tuvasta hilinenud või puuduvad kohaletoimetamised, jälgi SLA-sid ja kaitse äriprotsesse vaikselt esinevate viivituste eest. AI-põhine tuvastus andmete kvaliteedi ja torustike nähtavuse parandamiseks.
image: /assets/logo_square.png
keywords:
  - Data Timeliness
  - kohaletoimetamise jälgimine
  - andmete kvaliteet
  - andmete kvaliteet
  - andmete vaatlusvõime
  - hilinenud andmete tuvastamine
  - puuduvate andmete teavitamine
  - sla jälgimine
  - ai kohaletoimetamise analüüs
  - digna Data Timeliness
lang: en
robots: index, follow
og_title: Data Timeliness – Õigeaegse kohaletoimetamise jälgimine | digna Documentation
og_description: digna Data Timeliness tuvastab AI abil automaatselt hilinenud või puuduvad andmekohaletoimetamised. Kaitse äriprotsesse, jälgi SLA-sid ja tagage andmete õigeaegsus ja usaldusväärsus kõigis torustikes.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Timeliness – On-Time Delivery Monitoring
<h1 style="display:none;">AI-põhine Data Timeliness moodul andmete kvaliteedi ja vaatlusvõime jaoks – digna</h1>

---

## Eesmärk

The **Data Timeliness** module tagab, et **andmed jõuavad õigel ajal** — iga kord.  
See jälgib pidevalt kohaletoimetamise ajakavasid ja tuvastab automaatselt, kui andmekogumid, tabelid või failid on **hilinenud, puuduvad või puudulikud**.  

Kombineerides AI-õppe kasutaja määratud ajakavadega võimaldab *digna* organisatsioonidel ennetada edasisi vigu ja hoida ranged **SLA (Service Level Agreement)** sihid nii **andmete kvaliteedi** kui ka **andmetorustike vaatlusvõime** osas.

---

## Tehniline ülevaade

### Kaks jälgimisrežiimi
- **AI-õpitud saabumise mustrid**  
  digna õpib automaatselt teie andmete kohaletoimetamiste loomuliku rütmi — igapäevased, tunnised või sündmuspõhised — analüüsides ajaloolisi ajatempleid ja lõpetamisaegu.  
  See kohandub muutustega ärikalendrites, nädalavahetustes või kuu lõpu haripunktides.

- **Kasutaja määratud ajakavad**  
  Kasutajad saavad oodatavad kohaletoimetamised selgelt määratleda (nt *iga tööpäev enne 7:30*).  
  digna võrdleb tegelikku saabumisaega planeeritud ajakavaga ja teavitab, kui andmed hilinevad või puuduvad.

### Tuvastusmehhanism
- Hindab **metaandmete ajatempleid**, **kirjete arvu** ja **tabeli värskust**  
- Tuvastab **seiskunud ETL-töid**, **ebaõnnestunud ekstraktsioone** ja **osaliselt saabunud faile**  
- Integreerub *Data Anomalies* ja *Data Validation*iga kombineeritud ülevaadete saamiseks

---

## Tuvastussituatsioonid

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Igapäevane turuandmete voog hilineb kaks tundi, põhjustades aruannete SLA-de mittetäitmise |
| **Missing load** | Ajastatud tabelit või partiitsiooni ei uuendatud jooksva kuupäeva jaoks |
| **Chained dependency delay** | Ülemise taseme töö hilinemine mõjutab madalama taseme torustiku värskendust |
| **Weekend pattern shift** | AI-mudel kohaneb automaatselt, kui pühapäeviti andmeid ei oodata |

---

## Arhitektuur ja täitmine

- **Täitmine andmebaasis:** digna käivitab timeliness-kontrollid otse teie andmebaasis või andmeladustuses.  
- **Kergekaaluline metaandmete ligipääs:** loeb tööde ajatempleid, kirjete arvu ja partiitsiooniinfot — andmete väljavõtmist ei ole vaja.  
- **Konfigureeritav sagedus:** planeerige jälgimine per andmekogum, skeem või torustik.  
- **Ristmoodulite hoiatused:** tulemused võivad vallandada visuaalseid hoiatusi *Inspection Hub*is või teavitusi e-posti, Slacki või API kaudu.  

---

## Näited kasutusjuhtudest

- **Finantsturu voogude jälgimine:** tuvastage hinnainfo või kauplemisandmete uuenduste hilinemised.  
- **Andmeladustuse laadimised:** jälgige, kui öised ETL-tööd lõpevad oodatust hiljem.  
- **Andmete jagamine meeskondade vahel:** tagage, et osakondlikud andmed jõuaksid enne päevaseid tähtaegu.  
- **Regulatiivne aruandlus:** kinnitage, et esitused sisaldavad viimast saadavalolevat andmetehetktõmmist.

---

## Eelised

| Area | Benefit |
|------|----------|
| **Business Continuity** | Ennetab toimimistakistusi, mis on põhjustatud hilinenud või puuduvatest andmetest |
| **Data Quality** | Parandab andmetorustike usaldusväärsust ja järjepidevust |
| **Compliance** | Tagab SLA-de järgimise ja auditeerimise läbipaistvuse |
| **Automation** | AI kõrvaldab käsitsi ajakavade jälgimise |
| **Integration** | Töötab sujuvalt koos *Data Analytics*iga, et visualiseerida õigeaegsuse trende ajas |

---

## Kuidas digna õpib eeldatavaid kohaletoimetamise aegu

1. **Ajalooline analüüs:** digna jälgib varasemaid laadimisaegu ja kestusi.  
2. **AI-modelleerimine:** masinõpe loob dünaamilise aluse eeldatavale saabumisele.  
3. **Jälgimine:** iga uut kohaletoimetamist võrreldakse baasjoonega.  
4. **Hoiatamine:** kõrvalekalded vallandavad hoiatused kontekstuaalsete mõõdikute ja usalduspunktidega.  

See pidev õppimine kohaneb muutuvate protsessidega, säilitades samal ajal madala väärhäirete taseme.

---

## Korduma kippuvad küsimused

**Kas ma saan määrata oma kohaletoimetamise ajad?**  
Jah. digna toetab nii fikseeritud kasutaja ajakavasid kui ka AI-õpitud mustreid.

**Kas see integreerub minu ETL- või orkestreerimislahendusega?**  
Jah. digna integreerub tööriistadega nagu Airflow, dbt, Informatica või kohandatud ajakavadega.

**Kus toimub arvutus?**  
Kõik analüüsid käivad teie andmebaasis või pilvelaos — välisteenust ei kasutata.

**Mis juhtub, kui andmed hilinevad?**  
digna tekitab hoiatusi juhtpaneelil, Inspection Hubis ning API/webhookide kaudu, et operatsioonimeeskonnad saaksid viivitamatult teavituse.

---


**digna Data Timeliness** aitab tagada **usaldust andmete vastu**, kombineerides **AI-põhise tuvastuse**, **paigasisese täitmise** ja **andmete vaatlusvõime** — kõik teie kontrollitud keskkonnas.