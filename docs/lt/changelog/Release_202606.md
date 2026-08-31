---
title: digna Leidimas 2026.06 | Python SDK, Docker diegimas ir išplėstas validacijos valdymas
description: Sužinokite, kas naujo digna leidime 2026.06. Ši versija pristato naują **digna Python SDK**, oficialią **Docker** diegimo palaikymą, atnaujintą dashboard patirtį ir išplėstą validacijos taisyklių importo/eksporto funkcionalumą.
keywords: digna Leidimas 2026.06, digna Python SDK, digna Docker palaikymas, duomenų kokybės automatizacija, duomenų profiliavimas, validacijos taisyklių importas eksportas, digna dashboard, duomenų stebėjimo platforma, Python API, metaduomenų automatizacija
image: /assets/logo_square.png
---

# Leidimo pastabos – 2026.06  

Su leidimu 2026.06 digna žengia reikšmingą žingsnį į priekį automatizavimo, praplėtimumo ir platformos naudojimo patogumo srityse.  
Šis leidimas pristato naują **digna Python SDK**, oficialų **Docker** diegimo palaikymą, atnaujintą dashboard patirtį ir pagerintą validacijos taisyklių valdymo perkeliamosios galimybes.

---

## 🚀 Naujos funkcijos  

### digna Python SDK – Automatizuokite viską naudodami Python  
- Diegimas:
  ```bash
  pip install digna-sdk
  ```
- Programiškai valdykite ir automatizuokite digna naudodami Python  
- Kurkite ir konfigūruokite projektus per kodą  
- Paleiskite inspections ir monitoring vykdymus  
- Programiškai valdykite datasetus, taisykles ir konfigūracijas  
- Profilizuokite lenteles ir ištraukite metaduomenų įžvalgas  
- Eksportuokite profiliavimo ir duomenų kokybės rezultatus į išorines saugyklas ir sistemas  
- Integruokite su notebook’ais, orkestracijos įrankiais ir CI/CD pipeline’ais  

**Poveikis:** Leidžia pilną infrastruktūrą-kaip-kodą ir gilią duomenų kokybės bei stebėjimo darbo srautų automatizaciją naudojant Python.

---

### Docker palaikymas – Supaprastintas diegimas ir eksploatavimas  
- Oficiali Docker image palaikymas digna  
- Greitas ir nuoseklus diegimas skirtingose aplinkose  
- Supaprastintas įsitraukimas kūrimo, testavimo ir produkcijos aplinkose  
- Lengva integracija su Kubernetes ir kitomis konteinerių platformomis  
- Pagerinta diegimų perkeliama ir atkartojamumas  

**Poveikis:** Palengvina digna diegimą ir valdymą moderniose cloud-native architektūrose.

---

### QueryMode – Lanksti SQL vykdymo strategija

Sukonfigūruokite užklausų vykdymo strategiją: **Single** arba **Combined** režimas

**Single Mode**: Kiekvienas statistinis rodiklis apskaičiuojamas atskira SQL užklausa

  - Idealiai tinka didelėms duomenų saugykloms, kur riboja atmintis  
  - Apsaugo nuo užklausų sujungimo metu įvykstančio išteklių išeikvojimo (pvz., atminties trūkumo ar spool limitų)  
  - Didesnis užklausų skaičius, bet mažesnis atminties poreikis vienai užklausai

**Combined Mode**: Visi statistiniai rodikliai apskaičiuojami vienoje SQL užklausoje

  - Sumažina bendrą užklausų skaičių ir tinklo overhead’ą  
  - Optimizuoja našumą, kai duomenų šaltiniai yra valdomi atmintyje  
  - Efektyviau dažnai ir lygiagrečiai vykdomoms užklausoms

**Poveikis:** Leidžia vartotojams smulkiai valdyti užklausų vykdymą, subalansuojant našumą, resursų naudojimą ir atminties saugumą pagal duomenų šaltinio charakteristikas.

---

### Perdaryta dashboard patirtis  
- Modernizuotas ir pagerintas UI/UX dizainas  
- Aiškesnė navigacija ir struktūra  
- Geresnis monitoring rezultatų ir duomenų kokybės įžvalgų matomumas  
- Pagerintas perspėjimų, statistikos ir dashboardų skaitomumas  
- Greitesnis priėjimas prie svarbios operacinės informacijos  

**Poveikis:** Didina naudojimo patogumą ir kasdienį produktyvumą visiems vartotojams.

---

### Išplėstas validacijos taisyklių importas ir eksportas  
- Patobulinta importo/eksporto funkcionalumas validacijos taisyklėms  
- Lengvesnė migracija tarp aplinkų ir projektų  
- Pagerintas standartizuotų taisyklių rinkinių pakartotinis naudojimas  
- Geresnė valdymo ir taisyklių gyvavimo ciklo kontrolė  
- Supaprastintas bendradarbiavimas tarp komandų  

**Poveikis:** Leidžia mastelį didinančią ir nuoseklią duomenų kokybės valdymo praktiką visoje organizacijoje.

---

## 🧪 Platformos patobulinimai  

- Pilna Python SDK integracija automatizavimui  
- Konteinerizuotas diegimas per Docker  
- Pagerintas UX per perdarytą dashboard  
- Išplėstas validacijos logikos perkeliamosis gebėjimas  

---

## 🎯 Kam naudingas šis leidimas  

- Duomenų inžinieriams: automatizavimas, SDK naudojimas, pipeline integracija  
- Platformos komandoms: supaprastintas diegimas per Docker  
- Duomenų valdymo (governance) komandoms: pakartotinai naudojamų validacijos taisyklių valdymas  
- Analitikos komandoms: geresnis naudojimosi patogumas ir įžvalgų matomumas  

---

## 🛠 CLI atnaujinimai  
- Įtraukta SDK integracijos palaikymas  
- Patobulinti importo/eksporto darbo srautai  
- Bendri stabilumo ir našumo pagerinimai