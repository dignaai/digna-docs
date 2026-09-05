# Data Validation – Pārbaudes pēc noteikumiem
<h1 style="display:none;">Mākslīgā intelekta darbināts Data Validation modulis datu kvalitātei un observabilitātei – digna</h1>

---

## Mērķis

The **Data Validation** modulis nodrošina **datu kvalitāti** ar precīzām, pēc noteikumiem pamatotām pārbaudēm.  
Tas ļauj organizācijām definēt deterministisku biznesa un tehnisko validācijas loģiku, nodrošinot, ka dati atbilst atbilstības standartiem, līgumisko SLA un regulatīvajām prasībām.

Apvienojot *noteikumu izpildi datubāzē (in-database)*, *pilnīgas revīzijas pēdas* un *integrāciju ar citiem digna moduļiem*, **Data Validation** garantē konsekventu un izsekojamu **datu kvalitātes un observabilitātes** nodrošinājumu sarežģītās uzņēmuma vidēs.

---

## Tehniskais pārskats

### Atbalstītie validācijas veidi

- **Vienādības pārbaudes**  
  Pārbaudiet, ka vērtības atbilst gaidītajiem rezultātiem (piem., atsauces kodi, Boolean vērtības, kategoriju atbilstības).

- **Sliekšņi un diapazoni**  
  Validējiet skaitliskos rādītājus vai KPI pret definētajām robežām — statiskām vai dinamiski iegūtām.

- **Atsauces saraksti un uzmeklēšana**  
  Pārbaudiet, vai lauku vērtības pastāv apstiprinātajos pamatdatu kopumos (piem., PVN kodi, ISO valstu saraksti, produktu katalogi).

- **Savstarpējā kolonnu konsekvence**  
  Nodrošiniet relāciju pareizību (piem., valūta atbilst reģionam, riska kategorija sakrīt ar aktīva tipu).

- **Null vērtību apstrādes noteikumi**  
  Atklājiet negaidītas null vai tukšas vērtības kritiskajās kolonnās.

### Izpilde un reģistrēšana

- **Apstrāde datubāzē** – Visas validācijas noteikumi tiek izpildīti tieši jūsu datubāzē (Teradata, Snowflake, Databricks, PostgreSQL utt.).  
- **Nav datu izvilkšanas** – digna nekad nepārvieto neapstrādātus datus ārpus jūsu vides.  
- **Pilnīga izsekojamība** – Katrs noteikuma rezultāts tiek reģistrēts ar laika zīmogu, atbildīgo datu kopu, ierakstu skaitu un izpildes/neizpildes rezultātiem.  
- **Audits**