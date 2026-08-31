---
title: digna izlaidums 2026.06 | Python SDK, Docker izvietošana un uzlabota validācijas pārvaldība
description: Uzziniet, kas jauns digna izlaidumā 2026.06. Šī versija ievieš jauno digna Python SDK, Docker izvietošanas atbalstu, pārdizainētu informācijas paneļa pieredzi un paplašinātas importēšanas/eksportēšanas iespējas datu validācijas noteikumiem.
keywords: digna izlaidums 2026.06, digna Python SDK, digna Docker atbalsts, datu kvalitātes automatizācija, datu profilēšana, validācijas noteikumu imports/eksports, digna panelis, datu novērošanas platforma, Python API, metadatu automatizācija, Data Anomalies, Data Analytics, Data Validation, Data Timeliness, Data Schema Tracker
image: /assets/logo_square.png
---

# Izmaiņu žurnāls – versija 2026.06  

Ar izlaidumu 2026.06 digna sper lielu soli uz priekšu automatizācijas, paplašināmības un platformas lietojamības jomā.  
Šī versija ievieš jauno **digna Python SDK**, oficiālu **Docker izvietošanas atbalstu**, pārdizainētu informācijas paneļa pieredzi un uzlabotu pārnēsājamību validācijas noteikumu pārvaldībā.

---

## 🚀 Jaunumi  

### digna Python SDK – Automatizējiet visu ar Python  
- Instalēšanai:
  ```bash
  pip install digna-sdk
  ```
- Programmatīvi pārvaldīt un automatizēt digna, izmantojot Python  
- Izveidot un konfigurēt projektus, izmantojot kodu  
- Aktivizēt inspekcijas un monitoringa izpildes  
- Programmatīvi pārvaldīt datu kopas, noteikumus un konfigurācijas  
- Profilēt tabulas un iegūt metadatu ieskatus  
- Eksportēt profilēšanas un datu kvalitātes rezultātus uz ārējām repozitorijām un sistēmām  
- Integrēt ar notebookiem, orkestrācijas rīkiem un CI/CD cauruļvadiem  

**Ietekme:** Iespējota pilnīga infrastruktūra-kā-kods un dziļa datu kvalitātes un novērošanas darba plūsmu automatizācija, izmantojot Python.

---

### Docker atbalsts – vienkāršota izvietošana un darbība  
- Oficiāls Docker attēla atbalsts digna  
- Ātra un konsekventa iestatīšana dažādās vidēs  
- Vienkāršota ieviešana izstrādes, testēšanas un produkcijas vidēs  
- Viegla integrācija ar Kubernetes un citiem konteineru platformu risinājumiem  
- Uzlabota izvietojumu pārnēsājamība un reproducējamība  

**Ietekme:** Padara digna vienkāršāku izvietošanai un pārvaldībai mūsdienu mākoņnatīvās arhitektūrās.

---

### QueryMode – elastīga SQL izpildes stratēģija

Konfigurējiet vaicājumu izpildes stratēģiju: **Single** vai **Combined** režīms

**Single režīms**: Katra statistika tiek aprēķināta ar vienu atsevišķu SQL vaicājumu

  - Ideāli lielām datu avotu vidēm, kur ir bažas par atmiņas ierobežojumiem  
  - Novērš kombinētā vaicājuma resursu izsīkšanu (piem., atmiņas izsīkšana, spool ierobežojumi)  
  - Lielāks vaicājumu skaits, bet mazāks atmiņas patēriņš uz vaicājumu

**Combined režīms**: Visas statistikas tiek aprēķinātas vienā SQL vaicājumā

  - Samazina kopējo vaicājumu skaitu un tīkla režiju  
  - Optimizē veiktspēju, ja datu avoti ir pārvaldāmi atmiņā  
  - Efektīvāks biežām, paralēlām izpildēm

**Ietekme:** Lietotājiem tiek dota smalkāka kontrole pār vaicājumu izpildi, ļaujot balansēt veiktspēju, resursu patēriņu un atmiņas drošību atkarībā no datu avotu īpašībām.

---

### Pārdizainēta informācijas paneļa pieredze  
- Modernizēta un uzlabota UI/UX dizains  
- Skaidrāka navigācija un struktūra  
- Labāka monitoringa rezultātu un datu kvalitātes ieskatu pārskatāmība  
- Uzlabota trauksmju, statistiku un paneļu lasāmība  
- Ātrāka piekļuve svarīgākajai operacionālajai informācijai  

**Ietekme:** Uzlabo lietojamību un ikdienas produktivitāti visiem lietotājiem.

---

### Paplašināta importēšana un eksportēšana validācijas noteikumiem  
- Uzlabota importēšanas/eksportēšanas funkcionalitāte validācijas noteikumiem  
- Vienkāršāka migrācija starp vidēm un projektiem  
- Uzlabota standarta noteikumu kopu atkārtota izmantošana  
- Labāka pārvaldība un noteikumu dzīves cikla kontrolēšana  
- Vienkāršota sadarbība starp komandām  

**Ietekme:** Iespējo mērogojamu un konsekventu datu kvalitātes pārvaldību visā organizācijā.

---

## 🧪 Platformas uzlabojumi  

- Pilnīga Python SDK integrācija automatizācijai  
- Konteinerizēta izvietošana caur Docker  
- Uzlabota UX ar pārdizainētu informācijas paneli  
- Paplašināta validācijas loģikas pārnēsājamība  

---

## 🎯 Kam šī versija noder  

- Datu inženieri: automatizācija, SDK izmantošana, cauruļvadu integrācija  
- Platformas komandas: vienkāršota izvietošana ar Docker  
- Datu pārvaldības komandas: atkārtoti izmantojama validācijas noteikumu pārvaldība  
- Analītikas komandas: uzlabota lietojamība un ieskatu redzamība  

---

## 🛠 CLI atjauninājumi  
- Pievienota SDK integrācijas atbalsts  
- Uzlaboti importēšanas/eksportēšanas darbplūsmas  
- Vispārīgi stabilitātes un veiktspējas uzlabojumi