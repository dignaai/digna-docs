# Data Validation – Rule-Based Checks
<h1 style="display:none;">AI-Driven Data Validation Module for Data Quality and Observability – digna</h1>

---

## Namen

Modul **Data Validation** zagotavlja **kakovost podatkov** s pomočjo natančnih preverjanj na osnovi pravil.  
Omogoča organizacijam, da definirajo deterministične poslovne in tehnične validacijske logike ter s tem zagotovijo, da podatki izpolnjujejo standarde skladnosti, pogodbene SLA in regulatorne zahteve.

S kombinacijo *in-database rule execution*, *complete audit trails* in *integracije z drugimi digna moduli*, **Data Validation** zagotavlja dosledno in sledljivo **kakovost podatkov in opazljivost** v kompleksnih podjetniških okoljih.

---

## Tehnični pregled

### Podprti tipi validacij

- **Preverjanja enakosti**  
  Potrdite, da se vrednosti ujemajo s pričakovanimi rezultati (npr. referenčne kode, Boolean zastavice, kategorialne preslikave).

- **Meje in razponi**  
  Validirajte numerične meritve ali KPI-je glede na določene omejitve — statične ali dinamično izpeljane.

- **Referenčni seznami in poizvedbe (lookups)**  
  Preverite, ali vrednosti polj obstajajo v odobrenih glavnih podatkovnih nizih (npr. DDV kode, ISO seznami držav, produktni katalogi).

- **Konsistentnost med stolpci**  
  Zagotovite relacijsko pravilnost (npr. valuta ustreza regiji, kategorija tveganja se ujema z vrsto premoženja).

- **Pravila za ravnanje z NULL vrednostmi**  
  Zaznajte nepričakovane NULL ali prazne vrednosti v kritičnih stolpcih.

### Izvedba in beleženje

- **In-database processing** – Vsa pravila se izvajajo neposredno v vaši bazi podatkov (Teradata, Snowflake, Databricks, PostgreSQL itd.).  
- **Brez izvažanja podatkov** – digna nikoli ne prenaša surovih podatkov izven vašega okolja.  
- **Popolna sledljivost** – Vsak rezultat pravila je zabeležen z žigom časa, odgovornim naborom podatkov, številom zapisov in izidom (uspeh/neuspeh).  
- **Revizija**