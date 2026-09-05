# Changelog – Release 2026.01  

Ar izlaidumu 2026.01 digna ievieš būtiskus uzlabojumus datu avotu modelēšanā, savienojumu pārvaldībā un inspekciju lietojamībā.  
Šis izlaidums palielina elastību visos moduļos un būtiski paplašina **datu kvalitātes un validācijas pārklājumu**.

---

## Jaunās iespējas  

### Globālas datubāzu savienojumu konfigurācijas  
- Datubāzu savienojumi tagad konfigurējami **globālā līmenī**.  
- Globālos savienojumus var atkārtoti izmantot visos **projektos**, vienkāršojot konfigurāciju un uzturēšanu.  
- **Ietekme:** Samazina operatīvo slogu un nodrošina konsekventu pieslēgšanos starp vidiem.

### Vairāki avota savienojumi vienam projektam  
- Projektos tagad var atsaukties uz **vairākiem avota savienojumu konfigurācijas**.  
- Iespēja veidot elastīgākas konfigurācijas sarežģītām datu ainavām.  
- **Ietekme:** Atbalsta reālistiskas uzņēmuma arhitektūras ar heterogēniem datu avotiem.

### Loģiskie datu avoti  
- Datu avoti tagad pārstāv **loģisku slāni** projektā.  
- Katru datu avotu var nodrošināt no:
    - **datubāzes tabulas**
    - **datubāzes skata (view)**
    - **pielāgota SQL vaicājuma**  
- Šī nodalīšana uzlabo atkārtotu izmantošanu, skaidrību un inspekciju modelēšanu visos moduļos.  
- **Ietekme:** Atbrīvo inspekcijas un datu kvalitātes noteikumus no fiziskās glabāšanas, uzlabojot uzturēšanu un atkārtotu izmantošanu.

### Anomāliju nozīmības nosacījums  
- Tagad var definēt **anomāliju nozīmības nosacījumu**, lai kontrolētu anomāliju statusa vērtēšanu uz datu kopas līmeņa.  
- Statistika tiek aprēķināta neatkarīgi no tā, vai nosacījums ir iestatīts vai izpildīts.  
- Ja nosacījums **nav izpildīts**, **digna Data Anomalies** nenodrošina anomāliju statusu (zaļš / dzeltens / sarkans).  
- **Piemērs:** Izslēgt datu kopu no anomāliju vērtēšanas, ja ierakstu skaits ir mazāks par 10.  
- **Ietekme:** Nodrošina, ka anomālijas tiek vērtētas tikai atbilstošos biznesa kontekstos.

### Paziņojumu konfigurācija pa moduļiem  
- Paziņojumus tagad var konfigurēt **pa moduļiem** tieši digna saskarnē.  
- Ļauj neatkarīgi kontrolēt brīdinājumu uzvedību priekš **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** un citiem moduļiem.  
- **Ietekme:** Iespējot precīzas brīdināšanas stratēģijas, saskaņā ar komandas atbildībām un kritiskumu.

### Inspekcijas rezultātu eksports (CSV)  
- Lietotāji tagad var **lejupielādēt inspekciju rezultātus kā CSV failus**.  
- Nodrošina iespēju veikt analīzi bezsaistē, sagatavot atskaites un integrēt ar ārējiem rīkiem.  
- **Ietekme:** Vienkāršo auditus, atskaites un turpmāku datu kvalitātes analīzi.

---

## Paplašinātās datu validācijas iespējas  

Ar šo izlaidumu **digna Data Validation** tagad atbalsta plašu datu kvalitātes noteikumu kopumu:

- **Pārbaudes rindas līmenī**  
- **Vairāku kolonnu unikāluma pārbaudes**  
- **Referenciālās integritātes validācija starp datu avotiem**

Kopā šīs pārbaudes ļauj īstenot **strukturālās un attiecību datu kvalitātes prasības** sarežģītās datu ainavās.

### Unikalitātes pārbaudes vairākiem kolonnu kopumiem
- Ieviestas **unikalitātes pārbaudes** konfigurējamam **kolonnu kopumam**.  
- Ļauj validēt kombinētās atslēgas un biznesa līmeņa unikāluma ierobežojumus.  
- **Ietekme:** Atklāj dublētus biznesa entītijas, kuras nav iespējams identificēt ar vienas kolonnas pārbaudēm.

### Referenciālās integritātes pārbaudes
- Ieviestas **referenciālās integritātes pārbaudes**, lai validētu attiecības starp datu avotiem.  
- Nodrošina, ka **ārzemes atslēgu (foreign key) vērtības** avota datu avotā pastāv atsauces mērķa datu avotā.  
- Palīdz savlaicīgi atklāt bāreņu ierakstus, pārtrauktas attiecības un datu konsekvences problēmas.  
- Izstrādāts darbam ar **loģiskajiem datu avotiem**, tostarp skatiem un pielāgotiem SQL vaicājumiem.  
- **Lietošanas gadījumi:** datu noliktavas integritāte, regulatīvā ziņošana, pamatdatu konsekvence un uzticama turpmāka analītika.

---

## Kam šis izlaidums noder  

- **Datu inženieri:** Elastīgāka datu avotu modelēšana un atkārtoti izmantojami datubāzu savienojumi  
- **Datu kvalitātes un pārvaldības komandas:** Paplašināts validācijas pārklājums, ieskaitot attiecību integritātes noteikumus  
- **Analītikas un BI komandas:** Tīrāki dati ievadei un eksporta iespējas inspekciju rezultātu formā  
- **Platformas īpašnieki:** Samazināta konfigurācijas sarežģītība un uzlabota operatīvā uzturēšana

---

## CLI atjauninājumi  
- Izmaiņu nav

---