---
title: digna Data Anomalies | Ar MI darbināta datu novērojamība
description: digna Data Anomalies ir daļa no digna datu novērojamības platformas. Tas automātiski apgūst datu likumsakarības un atklāj anomālijas, lai uzlabotu datu kvalitāti un novērojamību datubāzēs, datu ezeros un datu noliktavās.
tags:
  - datu kvalitāte
  - datu novērojamība
  - datu kvalitātes nodrošināšana
  - datu novērošana
  - MI vadīta uzraudzība
  - anomāliju noteikšana
  - digna
  - digna platforma
hide:
  - toc                # neobligāti: paslēpj mazo augšējā līmeņa satura rādītāju, ja izmantojat iekļauto navigāciju
  - navigation         # neobligāti: paslēpj sānu navigāciju atsevišķām lapām
image: /assets/logo_square.png
---


# digna Data Anomalies – uz MI balstīta datu kvalitātes problēmu noteikšana

**Ar MI darbināta novērojamība pastāvīgai uzticībai datiem**

digna Data Anomalies ir daļa no **digna datu novērojamības platformas** — modulāra risinājuma, kas uzlabo **datu kvalitāti**, nepārtraukti analizējot, kā datu kopas uzvedas laika gaitā.

Tas automātiski apgūst, kas jūsu datiem ir “normāli”, un brīdina jūs, kad uzvedība mainās — bez statisku sliekšņu definēšanas vai kaut vienas kārtulas rakstīšanas.  
Modulis darbojas tieši jūsu datubāzē, tāpēc dati nekad neatstāj jūsu vidi.

---

## digna Data Anomalies mērķis

**digna Data Anomalies** modulis nodrošina nepārtrauktu **datu novērojamību**, aprēķinot un izsekojot iepriekš definētus statistiskos rādītājus, piemēram:

- Datu apjoms un ierakstu skaits  
- Trūkstošo vērtību īpatsvars  
- Vērtību sadalījumi un histogrammas  
- Skaitliskie diapazoni un vidējās vērtības  
- Kolonnu unikalitāte un teksta garums  

Šie rādītāji tiek automātiski apkopoti katrai datu kopai.  
Izmantojot tos, digna izveido modeļus, kas atspoguļo katra rādītāja tipisko uzvedību — apgūstot dienas, nedēļas vai sezonālas likumsakarības.  
Pēc apmācības modulis prognozē jauno datu sagaidāmās vērtības un atklāj novirzes, kas var liecināt par kvalitātes problēmām, procesu kļūmēm vai izmaiņām augšpusē.

---

## Galvenās iespējas

- Automātiski apgūst sagaidāmo datu uzvedību, izmantojot MI — bez sliekšņu konfigurēšanas.  
- Atklāj pēkšņus kritumus, lēcienus vai novirzes datu apjomā un sadalījumos.  
- Identificē samainītas kolonnas vai nepareizu atribūtu savstarpējo atbilstību.  
- Izceļ negaidītas kategoriskās vērtības (piemēram, jaunus reģionus vai kodus).  
- Atbalsta visus kolonnu tipus: skaitliskus, kategoriskus vai nenorādītus.  
- Darbojas pilnībā klienta vidē — bez datu pārvietošanas.  
- Integrējas ar **digna Data Analytics** ilgtermiņa tendenču analīzei.

---

## Kā tas darbojas

### 1. solis – rādītāju aprēķināšana
digna aprēķina profila rādītāju kopu katrai tabulai un kolonnai.  
Šie rādītāji apraksta jūsu datu struktūru un statistisko uzvedību un tiek saglabāti turpmākai analīzei.

### 2. solis – modeļu apmācība
Pamatojoties uz vēsturiskajām rādītāju vērtībām, digna apmāca kompaktus mašīnmācīšanās modeļus (parakstu modeļus), kas aptver katra rādītāja normālo diapazonu.

### 3. solis – automātiska sliekšņu noteikšana
Izmantojot *konformālo secināšanu*, digna aprēķina adaptīvus ticamības intervālus (automātiskos sliekšņus), kas attīstās līdz ar jūsu datiem.  
Ja jaunās rādītāju vērtības iekrīt ārpus prognozētā diapazona, tās tiek atzīmētas kā anomālijas.

Šī nepārtrauktā atgriezeniskās saites cilpa nodrošina, ka uzraudzība paliek aktuāla pat tad, kad datu apjomi vai likumsakarības dabiski pieaug.

---

## Piemēru scenāriji

### Negaidīts ierakstu apjoma kritums
Datu kopa parasti satur aptuveni 500 000 ierakstu dienā.  
Kad jauna piegāde ietver tikai 50 000 ierakstu, digna atzīmē anomāliju un parāda, cik tālu vērtība novirzās no apgūtā diapazona.

### Atklātas samainītas kolonnas
Vidējais `last_name` virknes garums pēkšņi sakrīt ar `first_name` garumu.  
digna atpazīst novirzi rādītāju likumsakarībās un signalizē par iespējamu kolonnu samainīšanu.

### Atklāta negaidīta kategorija
Kolonna, kurā uzskaitītas Austrijas pilsētas, pēkšņi satur “Cīrihe”.  
Pamatojoties uz vēsturiskajiem sadalījumiem, digna atzīmē jauno vērtību kā negaidītu un brīdina lietotāju.

---

## Integrācija ar citiem moduļiem

- **digna Data Analytics** — apkopo anomāliju vēsturi un svārstīguma rādītājus, lai atklātu ilgtermiņa tendences.  
- **digna Data Validation** — piemēro skaidri definētas biznesa kārtulas deterministiskām kvalitātes pārbaudēm.  
- **digna Data Timeliness** — uzrauga datu pienākšanas laikus un sasaista kavējumus ar anomāliju rašanos.  
- **digna Data Schema Tracker** — atklāj strukturālas izmaiņas, kas var izskaidrot jaunas anomālijas.

---

## Tipiski lietošanas gadījumi

- Trūkstošu vai dublētu datu ielāžu atklāšana.  
- Samainītu vai apcirstu kolonnu identificēšana.  
- Sadalījuma novirzes atklāšana skaitliskās vai kategoriskās pazīmēs.  
- Negaidītu atsauces vērtību vai kodu atrašana.  
- Nepārtrauktu datu uzņemšanas konveijeru uzraudzība attiecībā uz neatbilstībām.  
- Kopējās **datu kvalitātes un novērojamības** izsekošana visās jomās.

---

## Ieguvumi

- Tūlītēja neparastas datu uzvedības atklāšana.  
- Novērš manuālu sliekšņu pieregulēšanu.  
- Samazina darbības izmaksas lielās datu vidēs.  
- Vairo uzticību analītikas un pārskatu sistēmām.  
- Stiprina **datu kvalitāti** un pilnu **datu novērojamību**.

---

## Saistītie digna moduļi

- [digna Data Analytics](https://docs.digna.ai/platform/data_analytics/index.md) — tendenču un svārstīguma rādītāji.  
- [digna Data Validation](https://docs.digna.ai/platform//data_validation/index.md) — uz kārtulām balstīta datu pārbaude.  
- [digna Data Timeliness](https://docs.digna.ai/platform//data_timeliness/index.md) — datu piegādes grafiku uzraudzība.  
- [digna Data Schema Tracker](https://docs.digna.ai/platform//data_schema_tracker/index.md) — shēmas izmaiņu noteikšana.

---

## Kopsavilkums

**digna Data Anomalies** modulis veido digna MI vadītās **datu novērojamības platformas** kodolu.  
Nepārtraukti uzraugot galvenos rādītājus, apgūstot likumsakarības un identificējot novirzes, tas palīdz organizācijām nodrošināt, ka **datu kvalitāte** paliek uzticama, stabila un izskaidrojama — bez manuālas konfigurēšanas.
