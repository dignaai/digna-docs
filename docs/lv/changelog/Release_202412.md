---
title: digna izlaidums 2024.12 | Izmaiņu žurnāls un jaunas funkcijas
description: Uzziniet, kas jauns digna izlaidumā 2024.12. Šī versija ievieš iebūvētu scheduler, PDF atskaites, elastīgas pielāgotas kolonnas, dinamiskas snapshot vaicājumu vietturas un gudrāku sliekšņu optimizāciju, lai uzlabotu anomāliju noteikšanu un datu kvalitātes uzraudzību.
keywords: digna izlaidums 2024.12, digna izmaiņu žurnāls, release notes, iebūvēts scheduler, PDF atskaites, pielāgota kolonnas tips, snapshot vaicājumu vietturas, sliekšņu optimizācija, datu novērojamība, datu kvalitātes uzraudzība, anomāliju noteikšana
image: /assets/logo_square.png
---



# Izmaiņu žurnāls – izlaidums 2024.12

Izlaidums 2024.12 sniedz jaunu iespēju un uzlabojumu kopumu, kas padara digna vairāk automatizētu, elastīgu un gatavu biznesam.  
Šī versija uzlabo plānošanu, atskaišu ģenerēšanu, vaicājumu apstrādi un anomāliju noteikšanas precizitāti.  

---

## Jaunas funkcijas

### Iebūvētais Scheduler
Inspekcijas vairs nav atkarīgas tikai no komandrindas vai API izsaukumiem.  
Ar **jauno digna Scheduler** inspekcijas var tikt izpildītas automātiski noteiktos laikos.  

- Atbalsta **Cron izteiksmes** atkārtotām grafikiem (dienas, nedēļas vai pielāgoti intervāli).  
- Piedāvā precīzu kontroli ar **offsetiem**, **sākuma datumiem** un **beigu datumiem**.  
- Ļauj komandām nodrošināt, ka visi kritiskie datu avoti tiek pārbaudīti konsekventi un bez manuālas iesaistes.  

---

### Atskaites PDF formātā
Komandas tagad var ērti dalīties ar rezultātiem ar ieinteresētajām pusēm, izmantojot **PDF eksportus**.  

- Diagrammas, metrikas un anomāliju rezultāti var tikt eksportēti profesionālā PDF formātā.  
- Atskaites apvieno **vizualizācijas** un **pamata datus**, lai apmierinātu gan tehniskos, gan biznesa lietotājus.  
- Novērš nepieciešamību pēc ārējiem rīkiem atskaišu veidošanai.  

---

### Jauns kolonnas tips: `CUSTOM`
Lai nodrošinātu lielāku elastību, digna ievieš jaunu **`CUSTOM` kolonnas tipu**.  

- Lietotāji var precīzi noteikt, kuras **statistikas un metrikas** tiek piemērotas konkrētām atribūtam.  
- Ideāli piemērots īpašiem gadījumiem, kas neietilpst standarta kategorijās, piemēram, NUMERICAL vai CATEGORICAL.  
- Palīdz saglabāt analīzes fokusu un nodrošina rezultātus, kas atbilst biznesa kontekstam.  

---

### Jaunas vietturas snapshot vaicājumos
Snapshot vaicājumi tagad ir vienkāršāki un mazāk kļūdaini, pateicoties **dynamiskajām vietturām**.  

- Toki kā `#date+n#` vai `#date-n#` automātiski pielāgo datumus vaicājumos.  
- Piemērs:  
  - `#date+1#` → rītdiena  
  - `#date-2#` → pirms divām dienām  
- Izslēdz nepieciešamību manuāli aprēķināt datumus un nodrošina konsekvenci komandās.  

---

### Sliekšņu optimizācija
Anomāliju sliekšņi tagad ir gudrāki un kontekstuālāk pielāgoti.  

- Metrikām, piemēram, **NULL COUNT**, zemākie sliekšņi automātiski tiek ierobežoti līdz **0**.  
- Novērš nederīgus vai bezjēdzīgus sliekšņus.  
- Rezultātā mazāk kļūdpositīvu un uzticamāka anomāliju noteikšana.  

---

## Vispārīgi uzlabojumi
- Pārvilcināti **UI komponenti** projekta un atribūtu konfigurācijas skatos.  
- Uzlabota **paneļa (dashboard) veiktspēja** lielu datu apjomu gadījumā.  
- Uzlabota **žurnālu un kļūdu ziņojumu** informativitāte problēmu diagnostikai.  

---

## Kopsavilkums
Izlaidums 2024.12 nostiprina digna kā platformu **datu kvalitātes, anomāliju noteikšanas un novērojamības** jomā.  
Ar automatizāciju, ko nodrošina plānošana, kopīgojamām PDF atskaitēm, pielāgojamām kolonnām, vienkāršotiem snapshot vaicājumiem un gudrākiem sliekšņiem, digna kļūst vēl vērtīgāka gan tehniskiem lietotājiem, gan biznesa ieinteresētajām personām.