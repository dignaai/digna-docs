---
title: digna Išleidimas 2025.09 | Modulinis dizainas, penki nauji moduliai, MFA per OIDC
description: Sužinokite, kas naujo digna Išleidime 2025.09. Ši versija pristato modulinę architektūrą, penkis naujus modulius, MFA per OIDC ir pranešimus po modulį.
keywords: digna leidimas 2025.09, digna pakeitimų žurnalas, digna Data Anomalies, digna Data Analytics, digna Data Timeliness, digna Data Validation, digna Data Schema Tracker, digna modulinis dizainas, digna OIDC MFA
image: /assets/logo_square.png
---

# Changelog – Išleidimas 2025.09  

Su Išleidimu 2025.09 digna pristato naują **modulinę architektūrą** ir paleidžia **penkis specializuotus modulius** skirtiems Duomenų Kokybei ir Observability.  
Šis leidimas taip pat sustiprina autentifikaciją ir pagerina pranešimų valdymą visoje platformoje.  

---

## 🚀 Naujos funkcijos  

### Modulinis dizainas  
- digna dabar naudoja **modulinę architektūrą**.  
- Klientai gali įjungti tik tuos modulius, kurių jiems reikia, ir pridėti daugiau pagal augančius reikalavimus.  
- Ankstesnė funkcionalumas dabar yra dalis **digna Data Anomalies**.  

### Nauji moduliai  
- **digna Data Anomalies** – AI pagrindu atliekama anomalijų aptikta apimčių, pasiskirstymų ir trūkstamų reikšmių duomenyse.  
- **digna Data Analytics** – Laiko eilių observability metrikų vertinimas, skirtas ilgalaikėms tendencijoms ir kintamumui nustatyti.  
- **digna Data Timeliness** – Laukiamų duomenų atvykimo laiko stebėjimas, tiek AI pagrindu, tiek pagal taisykles.  
- **digna Data Validation** – Taisyklėmis pagrįsti įrašų lygio patikrinimai, užtikrinantys verslo taisyklių atitikimą.  
- **digna Data Schema Tracker** – Schemos pakeitimų (DDL modifikacijų) aptikimas prižiūrimose duomenų bazėse.  

### MFA per OIDC  
- Palaikymas **daugiaveiksnės autentifikacijos (MFA)** su OIDC vienkartiniu prisijungimu (Single Sign-On).  
- Suteikia įmonės lygio saugumą visiems vartotojų prisijungimams.  

### Pranešimų el. laiškai po modulį  
- Pranešimai dabar siunčiami **po modulį**, todėl lengviau atskirti įspėjimus iš Data Anomalies, Data Analytics ir kitų modulių.  

---

## 🛠 CLI atnaujinimai  

- **Nauja komanda: `inspect-cancel`** – Atšaukti inspekcijas pagal užklausos ID arba nutraukti visas aktyvias užklausas.  
- **Nauja komanda: `check-config`** – Patikrinti konfigūracijos failus prieš paleidimą.  
- **Nauja komanda: `remove-orphans`** – Išvalyti apleistas saugyklos įrašų eilutes.  
- **Patobulinta `inspect` komanda** – Nauja parinktis `--bypass-backend` (`-bb`) ir standartizuotos grąžinimo reikšmės (`0 = OK, 1 = INFO, 2 = WARNING`).  


## 📘 Dokumentacija  
- Nauji vadovai:  
  - Single Sign-On integracijos vadovas