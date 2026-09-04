---
title: digna Release 2026.04 | Analytics Chart, Enumerations & Validation Rule Templates
description: Sužinokite, kas naujo digna Release 2026.04. Ši versija pristato pažangią laiko eilučių analizę su Analytics Chart, pakartotinai naudojamus validacijos taisyklių šablonus, enumeracijas leistinų reikšmių centralizavimui ir stulpelio lygio aktualumo sąlygas.
keywords: digna Release 2026.04, digna changelog, digna Data Analytics, time series analysis, regression, data validation templates, enumerations, allowed values validation, data quality rules, data observability
image: /assets/logo_square.png
---

# Changelog – Release 2026.04  

Su Release 2026.04 digna žymiai plečia savo gebėjimus analitikoje ir duomenų validacijoje.  
Ši versija pristato pažangią laiko eilučių analizę, pakartotinai naudojamus validacijos komponentus ir centralizuotą reikšmių standartizavimą.

---

## Naujos funkcijos  

### Analytics Chart – laiko eilučių analizė be duomenų mokslo  
- Naujas **Analytics Chart** interaktyviai laiko eilučių analizei  
- Įmontuoti analitiniai metodai:
    - Linijinė, kvadratinė ir kubinė regresija  
    - Dalių regresija su konfigūruojamais lūžio taškais  
    - Suteikimo (smoothing) technikos  
    - Kvantilių analizė  
- Automatinis tendencijų, sezoninių reiškinių ir modelio pokyčių identifikavimas  
- Rezidualų analizė giliau suprasti nuokrypius  
- Laiko eilutės automatiškai apskaičiuojamos kiekvienam duomenų rinkiniui  

**Poveikis:** Leidžia vartotojams suprasti sudėtingą duomenų elgseną laikui bėgant be duomenų mokslo žinių ar išorinių įrankių.

---

### Enumerations – leistinų reikšmių centralizuotas apibrėžimas  
- Apibrėžkite pakartotinai naudojamus leistinų reikšmių rinkinius (pvz., šalys, regionai, būsenų kodai)  
- Validuokite stulpelių reikšmes prieš apibrėžtas enumeracijas naudojant **digna Data Validation**  
- Naudokite enumeracijas pakartotinai įvairiuose projektuose ir duomenų šaltiniuose  
- Naudokite enumeracijas visur per `#ENUM:MY_ENUM#`  
- Visi patikrinimai vykdomi **tiesiogiai šaltinio duomenų bazėje**  

**Poveikis:** Užtikrina nuoseklias ir standartizuotas duomenų reikšmes visoje organizacijoje.

---

### Validation Rule Templates – pakartotinai naudojama duomenų kokybės logika  
- Apibrėžkite pakartotinai naudojamas validacijos taisykles (pvz., tuščių tarpų patikrinimai, NOT NULL, formato patikrinimai)  
- Taikykite šablonus keliuose duomenų rinkiniuose  
- Užtikrinkite nuoseklią taisyklių logiką projektuose  
- Sumažinkite dubliavimą ir rankinę konfigūraciją  
- Visi patikrinimai vykdomi **tiesiogiai šaltinio duomenų bazėje**  

**Poveikis:** Leidžia mastelį pasiekti veiksmingą ir našų duomenų validavimą be duomenų perkėlimo.

---

### Statistikos lygio aktualumo sąlygos  
- Apibrėžkite aktualumo sąlygas **stulpelio lygiu kiekvienai statistikai**  
- Išplečia anomalijų aktualumo sąvoką  
- Kontroliuokite, kada statistika turėtų būti laikoma aktualia  
- Sumažinkite triukšmą neįtraukdami neesminių situacijų  

**Poveikis:** Gerina signalų kokybę, orientuojantis tik į prasmingus nuokrypius.

---

## Išplėstos Data Analytics & Validation galimybės  

Su šia versija digna plečia tiek **duomenų supratimą**, tiek **duomenų validacijos standartizavimą**:

- Pažangus **laiko eilučių interpretavimas** be duomenų mokslo žinių  
- Centralizuotas **leistinų reikšmių apibrėžimas per enumeracijas**  
- Pakartotinai naudojama **validacijos logika per šablonus**  
- Smulkesnės kontrolės galimybės dėl **statistikų ir įspėjimų aktualumo**  

Šios galimybės kartu leidžia organizacijoms ne tik aptikti problemas, bet ir **suprasti, standartizuoti ir kontroliuoti duomenų kokybę**.

---

## Kas gauna naudą iš šios versijos  

- **Duomenų inžinieriai:** Pakartotinai naudojama validacijos logika ir pagerinta kontrolė stebėjimo elgesiui  
- **Duomenų kokybės ir valdymo komandos:** Standartizuotos taisyklės ir nuosekli duomenų validacija tarp sistemų  
- **Analitikos ir BI komandos:** Geresnis tendencijų ir nuokrypių supratimas  
- **Platformos savininkai:** Didesnis priėmimas dėl supaprastintos analizės ir mastelinio validavimo  

---

## CLI atnaujinimai  
- Nėra pakeitimų  

---