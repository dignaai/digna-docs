# Data Anomalies – Automated Detection
<h1 style="display:none;">Tekoälypohjainen moduuli datan laadulle ja observoitavuudelle – digna Data Anomalies</h1>

---

## Tarkoitus

**Data Anomalies** -moduuli tunnistaa tietojoukoissasi esiintyvät epäsäännöllisyydet automaattisesti — sääntöjen kirjoittamista ei tarvita.  
Se valvoo jatkuvasti **datan toimituksen laatua**, oppii mitä “normaali” on ja havaitsee poikkeamat reaaliajassa.

Käyttämällä tekoälypohjaista havaitsemista digna tunnistaa hiljaiset datavirheet, kuten puuttuvat, duplikaatit tai korruptoituneet rivit, jotka voivat vääristää raportteja, koneoppimismalleja ja dashboardeja.

---

## Tekninen yleiskuva

### Analysoitavat metrikat

digna profiloit jatkuvasti seuraavia datasi osa-alueita:

- **Tietueiden määrä** – rivien kokonaismäärä, päivittäinen tai eräkohtainen  
- **Puuttuvat arvot** – null- tai tyhjien kenttien havaitseminen  
- **Jakaumat ja histogrammit** – datan muodon muutosten seuranta  
- **Arvoalueet** – automaattinen poikkeavien tai äärimmäisten arvojen tunnistus  
- **Yksilöllisyys** – tarkastukset duplikoituneista avaimista tai toistuvista merkinnöistä  

### Älykäs poikkeamien havaitseminen

- Käyttää **historiallista oppimista** odotettavien rajojen dynaamiseen määrittelyyn  
- Havaitsee poikkeamat **volyymissa, arvojakaumissa tai loogisissa suhteissa**  
- Hyödyntää tekoälyä kynnysarvojen automaattiseen mukauttamiseen vuorokaudenaikojen tai kausivaihteluiden perusteella  
- Eritteleee **tilastolliset vaihtelut** ja todelliset poikkeamat  
- Tuottaa yksityiskohtaiset metrikat ja luottamuspisteet per tietojoukko ja sarake  

---

## Havaitsemisskenaariot

Alla esimerkkejä tosielämän ongelmista, jotka **Data Anomalies** -moduuli tunnistaa automaattisesti:

| Scenario | Description |
|-----------|--------------|
| **Volume drops or spikes** | Puuttuu puolet päivän transaktioista, duplikoidut erälataukset tai äkilliset datan piikit |
| **Missing or null values** | Datan uutto on suoritettu mutta kriittiset sarakkeet ovat tyhjiä |
| **Distribution drifts** | Keskimääräinen ostosumma tai transaktioiden määrä alueittain muuttuu odottamatta |
| **Column swaps** | Sarakkeet kuten *first_name* ja *last_name* ovat vahingossa vaihtuneet ETL:ssä |
| **Unexpected categorical values** | esim. “Zurich” ilmestyy Itävallan kaupunkilistan alle |
| **Sudden uniqueness loss** | Aiemmin uniikit ID:t alkavat duplikoitua upstream-join-virheen vuoksi |

---

## Arkkitehtuuri ja suoritus

- **Tietokannan sisäinen suoritus:** Kaikki poikkeamien havaitsemislogiikka suoritetaan *tietokantamoottorin sisällä* (Teradata, Snowflake, Databricks, PostgreSQL jne.)  
- **Ei datan siirtoa:** digna lukea vain metrikat, eikä koskaan siirrä raakadataa ulkoisesti  
- **Inkrementaaliset päivitykset:** Vain uudet datasegmentit analysoidaan jokaisella ajokerralla tehokkuuden takaamiseksi  
- **Konfiguroitava tarkastusväli:** Tuntikohtainen, päivittäinen tai upstream-prosessien laukaisema  
- **Tulosten tallennus:** Metrikat ja poikkeamaliput kirjoitetaan takaisin dignan observoitavuusskeemaan visualisointia ja hälytyksiä varten  

---

## Hyödyt

| Area | Benefit |
|------|----------|
| **Automation** | Poistaa satoja manuaalisia SQL- tai sääntömäärittelyjä |
| **Precision** | Havaitsee ongelmat, jotka staattiset kynnysarvot usein missaavat |
| **Scalability** | Valvoo tehokkaasti miljoonia rivejä per taulu |
| **Integration** | Toimii saumattomasti yhdessä *digna Data Analytics* -moduulin kanssa trendianalyysia varten |
| **Compliance** | Varmistaa jatkuvan kontrollin **datan laadun ja observoitavuuden** yli |
| **Transparency** | Tarjoaa luottamuspisteet, aikaleimat ja syykoodit jokaiselle poikkeamalle |

---

## Miten digna oppii “normaalin”

1. **Profilointivaihe:** digna kerää metrikat historiallisista tietojoukoista.  
2. **Oppimisvaihe:** Tekoälymallit tunnistavat toistuvat kuviot (kausivaihtelut, viikoittaiset, päivittäiset).  
3. **Seurantavaihe:** Tulevia tietojoukkoja verrataan dynaamisesti opittuihin kynnyksiin.  
4. **Hälytysvaihe:** Tilastollisen luottamusrajan ylittävät poikkeamat nostetaan hälytyksiksi.  

Kaikki mallit ovat selitettäviä, deterministisiä ja optimoitu yritystason datamäärille.

---

## Esimerkkikäyttötapauksia

- Datan laadun valvonta **pankkitransaktiojärjestelmissä**  
- Latausvirheiden havaitseminen **ETL- tai tietovarastotyöissä**  
- Epätavallisen asiakastoiminnan tunnistus **telekommunikaatiotietueissa**  
- Kliinisen datan johdonmukaisuuden seuranta **terveystietoanalytiikan putkissa**  
- Rikkinäisten dashboardien estäminen **BI- ja raportointialustoilla**

---

## Usein kysytyt kysymykset

**Vaatiiko Data Anomalies ennalta määritettyjä sääntöjä?**  
Ei — moduuli oppii datan käyttäytymisestä automaattisesti.

**Voinko silti määritellä tiettyjä kynnysarvoja tarvittaessa?**  
Kyllä. digna mahdollistaa tekoälypohjaisen ja sääntöperusteisen havaitsemisen yhdistämisen (via *Data Validation*).

**Miten väärien positiivisten määrä minimoidaan?**  
Moduuli käyttää adaptiivista oppimista ja tilastollista luottamuspisteytystä normaalien kausivaihteluiden sivuuttamiseksi.

**Missä laskenta tapahtuu?**  
Kaikki prosessointi ajetaan tietokannassasi — digna ei koskaan pura raakadataa.

**Sopiiko se arkaluonteisille tai säädellyille datoille?**  
Kyllä. digna ajetaan täysin paikallisesti tai yksityisessä pilvessä ja noudattaa eurooppalaisia vaatimuksia.

---