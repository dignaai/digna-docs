---
title: digna Data Anomalies | AI varoma duomenų stebėsena
description: digna Data Anomalies yra digna Duomenų stebėjimo platformos dalis. Ji automatiškai išmoksta jūsų duomenų modelius ir aptinka anomalijas, kad pagerintų duomenų kokybę ir stebėseną tarp duomenų bazių, duomenų ežerų ir sandėlių.
tags:
  - duomenų kokybė
  - duomenų stebėsena
  - duomenų kokybė
  - duomenų stebėsena
  - dirbtinio intelekto varomas stebėjimas
  - anomalijų aptikimas
  - digna
  - digna platforma
hide:
  - toc                # optional: hide the small top-level TOC if you use inline nav
  - navigation         # optional: hide side navigation for standalone pages
image: /assets/logo_square.png
---


# digna Data Anomalies – dirbtinio intelekto pagrindu atliekamas duomenų kokybės problemų aptikimas

**Dirbtiniu intelektu pagrįsta stebėsena dėl nuolatinio pasitikėjimo duomenimis**

digna Data Anomalies yra dalis **digna Duomenų stebėjimo platformos** — modulinio sprendimo, kuris gerina **duomenų kokybę** nuolat analizuodamas, kaip duomenų rinkiniai elgiasi laikui bėgant.

Ji automatiškai išmoksta, kaip jūsų duomenyse atrodo „normalu“, ir įspėja, kai elgsena pasikeičia — be statinių ribų nustatymo ar vienos taisyklės rašymo.  
Modulis veikia tiesiogiai jūsų duomenų bazėje, todėl duomenys niekada neišeina iš jūsų aplinkos.

---

## digna Data Anomalies paskirtis

**digna Data Anomalies** modulis užtikrina nuolatinę **duomenų stebėseną** apskaičiuodamas ir sekdamas iš anksto apibrėžtus statistinius rodiklius, tokius kaip:

- Duomenų apimtis ir įrašų skaičius  
- Trūkstamų reikšmių santykiai  
- Reikšmių pasiskirstymai ir histogramos  
- Skaitiniai intervalai ir vidurkiai  
- Stulpelio unikalumas ir teksto ilgis  

Šie rodikliai renkami automatiškai kiekvienam duomenų rinkiniui.  
Remdamasi jais, digna kuria modelius, reprezentuojančius tipinę kiekvieno rodiklio elgseną — išmokdama dieninius, savaitinius ar sezoninius modelius.  
Kartą apmokytas, modulis prognozuoja laukiamas reikšmes naujiems duomenims ir aptinka nukrypimus, kurie gali reikšti kokybės problemas, procesų gedimus arba upstream pakeitimus.

---

## Pagrindinės galimybės

- Automatiškai išmoksta laukiamą duomenų elgseną naudojant DI — nereikia konfigūruoti ribų.  
- Aptinka staigius kritimus, šuolius ar dreifus duomenų apimtyje ir pasiskirstymuose.  
- Nustato sukeistus stulpelius arba neteisingus atributų atitikimus.  
- Išryškina netikėtas kategorines reikšmes (pvz., naujos regionų reikšmės arba kodai).  
- Palaiko visų tipų stulpelius: skaitinius, kategorinius ar nenustatytus.  
- Veikia visiškai kliento aplinkoje — be duomenų judėjimo.  
- Integruojasi su **digna Data Analytics** ilgalaikei tendencijų analizei.

---

## Kaip tai veikia

### 1 žingsnis – rodiklių skaičiavimas
digna apskaičiuoja profilio rodiklių rinkinį kiekvienai lentelei ir stulpeliui.  
Šie rodikliai apibūdina jūsų duomenų struktūrą ir statistinę elgseną ir saugomi tolimesnei analizei.

### 2 žingsnis – modelio apmokymas
Remiantis istorinėmis rodiklių reikšmėmis, digna apmoko kompaktiškus mašininio mokymosi modelius (signature models), kurie fiksuoja normalaus kiekvieno rodiklio intervalą.

### 3 žingsnis – automatinis ribų nustatymas
Naudodama *conformal inference*, digna apskaičiuoja adaptuojamus pasitikėjimo intervalus (auto-thresholds), kurie kinta kartu su jūsų duomenimis.  
Jei naujos rodiklių reikšmės patenka už prognozuoto intervalo ribų, jos žymimos kaip anomalijos.

Šis nuolatinis atsiliepimų ciklas užtikrina, kad stebėsena išliktų aktuali net ir tada, kai duomenų apimtys arba modeliai natūraliai auga.

---

## Pritaikymo pavyzdžiai

### Netikėtas įrašų apimties sumažėjimas
Duomenų rinkinys paprastai turi apie 500 000 įrašų per dieną.  
Kai naujas tiekimas turi tik 50 000 įrašų, digna pažymi anomaliją ir parodo, kiek reikšmė nukrypo nuo išmokto intervalo.

### Nustatytas stulpelių sukeitimas
Stulpelio `last_name` vidutinis simbolių ilgis staiga atitinka `first_name` ilgį.  
digna atpažįsta nukrypimą rodiklių modeliuose ir signalizuoja apie galimą stulpelių sukeitimą.

### Nustatyta netikėta kategorija
Stulpelyje, kuriame buvo Austrijos miestų sąrašas, staiga pasirodo „Zurich“.  
Remiantis istoriniais pasiskirstymais, digna pažymi naują reikšmę kaip netikėtą ir įspėja vartotoją.

---

## Integracija su kitais moduliais

- **digna Data Analytics** — agreguoja anomalijų istoriją ir kintamumo rodiklius, atskleidžiant ilgalaikes tendencijas.  
- **digna Data Validation** — taiko aiškias verslo taisykles deterministinėms kokybės patikroms.  
- **digna Data Timeliness** — stebi duomenų atvykimo laikus ir koreliuoja vėlavimus su anomalijų įvykiais.  
- **digna Data Schema Tracker** — aptinka struktūrinius pakeitimus, kurie gali paaiškinti naujas anomalijas.

---

## Tipiniai naudojimo atvejai

- Trūkstamų arba pasikartojančių duomenų užkrovimų aptikimas.  
- Sukeistų arba nutrumpintų stulpelių identifikavimas.  
- Skaitinių ar kategorinių požymių pasiskirstymo dreifo aptikimas.  
- Netikėtų referencinių reikšmių arba kodų radimas.  
- Nuolatinių įkėlimo srautų stebėjimas dėl nereguliarumų.  
- Bendros **duomenų kokybės** ir end-to-end **duomenų stebėsenos** sekimas per domenus.

---

## Privalumai

- Greitas nenormalaus duomenų elgesio aptikimas.  
- Pašalina rankinį ribų derinimą.  
- Sumažina operacinę veiklą didelėse duomenų aplinkose.  
- Didina pasitikėjimą analizės ir ataskaitų sistemomis.  
- Stiprina **duomenų kokybę** ir visapusišką **duomenų stebėseną**.

---

## Susiję digna moduliai

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — tendencijų ir kintamumo rodikliai.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — taisyklėmis pagrįsta duomenų patikra.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — duomenų pristatymo grafikų stebėsena.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — schemos pakeitimų aptikimas.

---

## Santrauka

**digna Data Anomalies** modulis sudaro kertinę digna DI varomos **Duomenų stebėjimo platformos** dalį.  
Nuolat stebėdamas pagrindinius rodiklius, išmokdamas modelius ir identifikuodamas nukrypimus, jis padeda organizacijoms užtikrinti, kad **duomenų kokybė** išliktų patikima, stabili ir paaiškinama — be rankinės konfigūracijos.