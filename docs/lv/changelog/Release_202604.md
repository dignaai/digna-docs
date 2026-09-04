---
title: digna izlaidums 2026.04 | Analytics Chart, Enumerations & Validation Rule Templates
description: Uzziniet, kas jauns digna izlaidumā 2026.04. Šajā versijā ir pievienota uzlabota laika rindu analīze ar Analytics Chart, atkārtoti izmantojami validācijas noteikumu veidnes, enumerācijas atļautajām vērtībām un kolonnu līmeņa relevances nosacījumi.
keywords: digna Release 2026.04, digna changelog, digna Data Analytics, time series analysis, regression, data validation templates, enumerations, allowed values validation, data quality rules, data observability
image: /assets/logo_square.png
---

# Izmaiņu žurnāls – izlaidums 2026.04  

Ar izlaidumu 2026.04 digna būtiski paplašina savas iespējas analītikā un datu validācijā.  
Šajā izlaidumā pievienota uzlabota laika rindu analīze, atkārtoti izmantojami validācijas komponenti un centralizēta vērtību standartizācija.

---

## Jaunumi  

### Analytics Chart – laika rindu analīze bez datu zinātnes  
- Jauns **Analytics Chart** interaktīvai laika rindu analīzei  
- Iebūvētas analītiskās metodes:
    - Lineārā, kvadrātiskā un kubiskā regresija  
    - Daļējas (piecewise) regresijas ar konfigurējamiem pārrāvuma punktiem  
    - Gludināšanas (smoothing) tehnikas  
    - Kvantilu analīze  
- Automātiska tendenču, sezonāluma un modeļu izmaiņu identifikācija  
- Reziduālu analīze dziļākai noviržu izpratnei  
- Laika rindas tiek automātiski aprēķinātas katram datu kopumam  

**Ietekme:** Lietotāji var saprast sarežģītu datu uzvedību laika gaitā, neprasot datu zinātnes ekspertīzi vai ārējas rīkus.

---

### Enumerations – centralizēta atļauto vērtību definīcija  
- Definējiet atkārtoti izmantojamus atļauto vērtību kopumus (piem., valstis, štati, statusu kodi)  
- Pārbaudiet kolonnas vērtības pret iepriekš definētām enumerācijām programmā **digna Data Validation**  
- Izmantojiet enumerācijas atkārtoti projektos un datu avotos  
- Lietojiet enumerācijas jebkurā vietā, izmantojot `#ENUM:MY_ENUM#`  
- Visas pārbaudes tiek izpildītas **tieši avota datubāzē**  

**Ietekme:** Nodrošina konsekventas un standartizētas datu vērtības visā organizācijā.

---

### Validation Rule Templates – atkārtoti izmantojama datu kvalitātes loģika  
- Definējiet atkārtoti izmantotamus validācijas noteikumus (piem., pārbaudes uz tukšām atstarpēm, NOT NULL, formāta pārbaudes)  
- Pielietojiet veidnes vairākos datu kopumos  
- Nodrošiniet konsekventu noteikumu loģiku projektos  
- Samaziniet dublēšanos un manuālo konfigurēšanu  
- Visas pārbaudes tiek izpildītas **tieši avota datubāzē**  

**Ietekme:** Nodrošina mērogojamu un augstas veiktspējas datu validāciju bez datu pārvietošanas.

---

### Kolonnu līmeņa statistiku relevances nosacījumi  
- Definējiet relevances nosacījumus uz **kolonnu līmeņa katrai statistikai**  
- Paplašina anomaliju relevances nosacījumu konceptu  
- Kontrolējiet, kad statistika ir uzskatāma par relevantu  
- Samaziniet troksni, izslēdzot nekritiskas situācijas  

**Ietekme:** Uzlabo signāla kvalitāti, koncentrējoties tikai uz nozīmīgām novirzēm.

---

## Paplašinātas Data Analytics & Validation iespējas  

Ar šo izlaidumu digna paplašina gan jomu saistītu datu izpratni, gan datu validācijas standartizāciju:

- Uzlabota laika rindu interpretācija bez datu zinātnes zināšanām  
- Centralizēta **atļauto vērtību definīcija**, izmantojot enumerācijas  
- Atkārtoti izmantojama **validācijas loģika** caur veidnēm  
- Smalki regulējama **statistiku un trauksmju relevances kontrole**  

Kopā šīs iespējas ļauj organizācijām ne tikai atklāt problēmas, bet arī **izprast, standartizēt un kontrolēt datu kvalitāti**.

---

## Kam šis izlaidums noder  

- **Datubūvēšanas inženieri (Data Engineers):** atkārtoti izmantojama validācijas loģika un uzlabota kontrole pār monitoringa uzvedību  
- **Datu kvalitātes un pārvaldības komandas:** standartizēti noteikumi un konsekventa datu validācija visos sistēmas slāņos  
- **Analītikas un BI komandas:** labāka tendenču un noviržu izpratne  
- **Platformas īpašnieki:** palielināta adopcija, pateicoties vienkāršākai analītikai un mērogojamai validācijai  

---

## CLI atjauninājumi  
- Izmaiņu nav  

---