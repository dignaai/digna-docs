---
title: Data Schema Tracker – Stebėkite schemų evoliuciją | digna dokumentacija
description: Sužinokite, kaip digna Data Schema Tracker stebi stulpelių pasikeitimus, duomenų tipų atnaujinimus ir schemos dreifą. Aptikite ir gaukite įspėjimus apie tiek tyčinius, tiek netyčinius schemos pakeitimus, kad išvengtumėte ETL gedimų, sulaužytų ataskaitų ir duomenų stebimumo praradimo.
image: /assets/logo_square.png
keywords:
  - duomenų schemos stebėjimas
  - schemos dreifo aptikimas
  - schemos evoliucijos stebėjimas
  - metaduomenų stebimumas
  - duomenų stebimumas
  - duomenų kokybė
  - duomenų struktūros stebėjimas
  - duomenų bazės metaduomenys
  - ETL vamzdynų stabilumas
  - digna data schema tracker
lang: lt
robots: index, follow
og_title: Data Schema Tracker – Stebėkite schemų evoliuciją | digna dokumentacija
og_description: digna Data Schema Tracker stebi schemos dreifą, duomenų tipų pakeitimus ir stulpelių atnaujinimus. Gaukitė įspėjimus prieš tai, kai ETL vamzdynai arba ataskaitos sugestų dėl netikėtų struktūros pokyčių.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Schema Tracker – Stebėkite schemų evoliuciją
<h1 style="display:none;">AI valdomas modulis metaduomenų stebimumui ir duomenų kokybei – digna Data Schema Tracker</h1>

---

## Paskirtis

The **Data Schema Tracker** informuoja apie jūsų duomenų bazių struktūrų evoliuciją.  
Jis nuolat stebi **lentelių schemas, stulpelius ir duomenų tipus**, kad aptiktų **schemos dreifą** — tyčinius arba netyčinius struktūrinius pokyčius, kurie gali sutrikdyti vamzdynus, ETL užduotis arba BI ataskaitas.

Užtikrindama skaidrumą schemų evoliucijoje, digna padeda organizacijoms išlaikyti **pasitikėjimą duomenų kokybe**, užtikrinti **duomenų sistemų stebimumą** ir išvengti brangiai kainuojančių gamybos incidentų, kuriuos sukelia nenustatyti schemos pakeitimai.

---

## Techninis apžvalga

### Ką jis stebi

- **Pridėti arba pašalinti stulpeliai** – aptinka naujai pridėtus, pervadintus ar ištrintus stulpelius.  
- **Duomenų tipų pakeitimai** – identifikuoja pokyčius, tokius kaip `INT → VARCHAR` arba `DATE → TIMESTAMP`.  
- **Lentelių ir vaizdų pakeitimai** – fiksuoja lentelių ir vaizdų kūrimą, pervardijimą ar pašalinimą.  
- **Skirtumai tarp aplinkų** – lygina schemų versijas tarp Dev, Test ir Production aplinkų.  

### Aptikimas ir įspėjimai

- Skenuoja **duomenų bazės metaduomenis** arba **sisteminius katalogus** tiesiogiai jūsų duomenų platformoje.  
- Palygina kiekvieną schemos momentinį atvaizdą su anksčiau žinoma versija, saugoma digna stebėjimo schemoje.  
- Generuoja **realaus laiko įspėjimus** informacijos suvestinėje, per API arba išoriniais pranešimų kanalais (el. paštas, Slack, webhook).  
- Logina kiekvieną schemos versiją istoriniam sekimui ir audito pasirengimui.

---

## Architektūra ir vykdymas

- **Vykdymas duomenų bazėje:** digna veikia visiškai jūsų aplinkoje, užklausdamas metaduomenų vaizdų be jokio faktinio duomenų perdavimo.  
- **Lengvas skenavimas:** prieina tik prie struktūrinės informacijos — niekada ne prie vartotojų duomenų.  
- **Centralizuotas saugojimas:** schemos metaduomenys ir dreifo įrašai saugomi digna stebėjimo schemoje vizualizacijai ir analitikai.  
- **Automatizacija:** palaiko suplanuotus arba įvykiu paremtus skenavimus per digna Core arba išorinius orkestravimo įrankius.  

---

## Pavyzdinės naudojimo situacijos

| Use Case | Description |
|-----------|--------------|
| **ETL Stability Monitoring** | Aptinka aukštesnio lygio struktūros pakeitimus prieš tai, kai vamzdynai sugenda dėl schemos neatitikimų. |
| **Business Intelligence Reliability** | Užkerta kelią sulaužytoms ataskaitoms dėl pervardytų arba trūkstamų stulpelių. |
| **Data Warehouse Governance** | Laiko audituotiną schemų evoliucijos istoriją atitikties ir poveikio analizės tikslais. |
| **Integration Oversight** | Užtikrina, kad duomenų ežero ir sandėlio schemos išliktų sinchronizuotos po struktūrinių atnaujinimų. |

---

## Privalumai

| Area | Benefit |
|------|----------|
| **Data Quality** | Apsaugo nuo nenustatyto schemos dreifo, kuris gali sugadinti arba neteisingai interpretuoti duomenų vamzdynus. |
| **Observability** | Papildo bendrą duomenų ekosistemos stebimumą struktūriniu monitoringu. |
| **Compliance** | Išlaiko versijuotą schemų istoriją audito, atsekamumo ir pakeitimų valdymo tikslais. |
| **Prevention** | Aptinka struktūrinius nesklandumus prieš jiems išsiliejant į ataskaitas arba gamybos klaidas. |

---

## Kaip tai veikia

1. **Momentinio atvaizdo rinkimas** – digna užfiksuoja esamus schemos metaduomenis.  
2. **Palyginimas** – naujas momentinis atvaizdas lyginamas