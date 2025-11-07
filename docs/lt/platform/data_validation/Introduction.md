---
title: Data Validation – Taisymais pagrįsti patikrinimai atitikties ir audito poreikiams | digna Documentation
description: Sužinokite, kaip digna Data Validation įgyvendina deterministinius, taisymais pagrįstus patikrinimus su slenkstiais, intervalais ir referencinėmis sąrašais. Užtikrinkite atitiktį, audito galimybę ir reguliavimo ataskaitų rengimą finansų, sveikatos priežiūros ir kitose duomenų jautrumą turinčiose srityse.
image: /assets/logo_square.png
keywords:
  - data validation
  - taisymais pagrįsti duomenų patikrinimai
  - duomenų kokybė
  - duomenų kokybės užtikrinimas
  - duomenų stebėsena
  - slenkstiai ir intervalai
  - referencinių sąrašų patikrinimas
  - audito galimybė
  - atitikties stebėjimas
  - digna data validation
lang: lt
robots: index, follow
og_title: Data Validation – Taisymais pagrįsti patikrinimai atitikties ir audito poreikiams | digna Documentation
og_description: digna Data Validation įgyvendina deterministinius, taisymais pagrįstus patikrinimus su slenkstiais, intervalais ir referencinėmis sąrašais. Sukurta reguliuojamoms pramonės šakoms, užtikrina atitiktį, skaidrumą ir audito galimybę.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Data Validation – Rule-Based Checks
<h1 style="display:none;">AI varomas Data Validation modulis duomenų kokybei ir stebėsenai – digna</h1>

---

## Tikslas

Modulis **Data Validation** užtikrina **duomenų kokybę** per tikslius, taisymais pagrįstus patikrinimus.  
Jis leidžia organizacijoms apibrėžti deterministinę verslo ir techninę validacijos logiką, užtikrinančią, kad duomenys atitiktų atitikties standartus, sutartinius SLA ir reguliavimo reikalavimus.

Sujungus *duomenų bazėje vykdomus taisyklių patikrinimus*, *pilnus audito kelių įrašus* ir *integraciją su kitais digna moduliais*, **Data Validation** garantuoja nuoseklų ir atsekamą **duomenų kokybės ir stebėsenos** lygį sudėtingose įmonės aplinkose.

---

## Techninis apžvalga

### Palaikomi validacijos tipai

- **Lygybės patikrinimai**  
  Patikrina, ar reikšmės atitinka lūkesčius (pvz., referenciniai kodai, loginiai žymenys, kategoriniai atitikmenys).

- **Slenkstiai ir intervalai**  
  Tikrina skaitmeninius rodiklius ar KPI pagal apibrėžtas ribas — statines arba dinamiškai gaunamas.

- **Referenciniai sąrašai ir paieškos**  
  Patikrina, ar laukų reikšmės yra patvirtintų pagrindinių duomenų rinkiniuose (pvz., PVM kodai, ISO šalių sąrašai, produktų katalogai).

- **Tarpstulpelinis nuoseklumas**  
  Užtikrina reliacinį teisingumą (pvz., valiuta atitinka regioną, rizikos kategorija atitinka turto tipą).

- **Trūkstamų reikšmių tvarkymo taisyklės**  
  Aptinka nenumatytas null arba tuščias reikšmes kritiniuose stulpeliuose.

### Vykdymas ir žurnavimas

- **In-Database Processing** – Visos validacijos taisyklės vykdomos tiesiogiai jūsų duomenų bazėje (Teradata, Snowflake, Databricks, PostgreSQL ir kt.).  
- **No Data Extraction** – digna niekada neiškelia žalių duomenų už jūsų aplinkos ribų.  
- **Full Traceability** – Kiekvieno taisyklės rezultatas registruojamas su laiko žyma, atsakingu duomenų rinkiniu, įrašų skaičiais ir praėjusiais/neišlaikius rezultatais.  
- **Auditas**
