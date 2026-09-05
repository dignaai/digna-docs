# Data Timeliness – Ajoissa toimitusten valvonta
<h1 style="display:none;">Tekoälyllä ohjattu Data Timeliness -moduuli datan laadun ja havainnoitavuuden tueksi – digna</h1>

---

## Tarkoitus

Data Timeliness -moduuli varmistaa, että data saapuu ajoissa — joka kerta.  
Se valvoo jatkuvasti toimitusaikatauluja ja tunnistaa automaattisesti, kun datasetit, taulut tai tiedostot ovat **myöhässä, puuttuvat tai puutteelliset**.  

Yhdistämällä tekoälyn oppimisen ja käyttäjän määrittelemät aikataulut *digna* auttaa organisaatioita estämään ketjureaktiot virheisiin ja pitämään kiinni tiukoista **SLA (Service Level Agreement)** -tavoitteista sekä **datan laadun** että **tietoputkien havainnoitavuuden** osalta.

---

## Tekninen yleiskuva

### Kaksinkertainen valvontatila
- **AI:n oppimat saapumismallit**  
  digna oppii automaattisesti datatoimitustesi luontaisen rytmin — päivittäinen, tunnittainen tai tapahtumapohjainen — analysoimalla historiallisia aikaleimoja ja valmistumisaikoja.  
  Se mukautuu muutoksiin liiketoimintakalentereissa, viikonloppuihin tai kuukauden loppuun liittyviin huippuihin.

- **Käyttäjän määrittelemät aikataulut**  
  Käyttäjät voivat määritellä odotetut toimitusajat eksplisiittisesti (esim. joka arkipäivä ennen klo 7.30).  
  digna vertaa todellista saapumisaikaa suunniteltuun aikatauluun ja lähettää hälytyksiä, kun data on myöhässä tai puuttuu.

### Havaitsemismekanismi
- Arvioi **metatietojen aikaleimoja**, **rivitilejä** ja **taulujen tuoreutta**  
- Havaitsee **jumittuneet ETL-työt**, **epäonnistuneet uuttamiset** ja **osittaiset tiedostotoimitukset**  
- Integroituu *Data Anomalies*- ja *Data Validation* -moduuleihin yhdistettyjen näkymien saamiseksi

---

## Havaitsemisskenaariot

| Scenario | Description |
|-----------|--------------|
| **Late data arrival** | Päivittäinen markkinadatasyöte myöhästyy kahdella tunnilla, mikä aiheuttaa raporttien SLA-tavoitteiden ylittymisen |
| **Missing load** | Aikataulutettua taulua tai partitioita ei ole päivitetty kuluvan päivän osalta |
| **Chained dependency delay** | Ylemmän tason työn viivästys vaikuttaa alemman tason putken päivitykseen |
| **Weekend pattern shift** | AI-malli mukautuu automaattisesti, kun sunnuntaisin ei odoteta dataa |

---

## Arkkitehtuuri ja suoritus

- **Tietokantasisäinen suoritus:** digna suorittaa ajantasaisuustarkistukset suoraan tietokannassasi tai data warehouse -ympäristössä.  
- **Kevyt metatiedon käyttö:** lukee työn aikaleimoja, rivimääriä ja partitio­tietoja — ei vaadi datan ulosottoa.  
- **Konfiguroitava taajuus:** ajoita valvonta per dataset, skeema tai putki.  
- **Ristiin-moduulihälytykset:** tulokset voivat laukaista visuaalisia varoituksia *Inspection Hubissa* tai ilmoituksia sähköpostitse, Slackissa tai API:n kautta.  

---

## Esimerkkikäyttötapaukset

- **Rahoitusmarkkinasyötteet:** havaitse viiveet hintojen tai kaupankäynnin datapäivityksissä.  
- **Data Warehouse -ladaukset:** seuraa, kun yölliset ETL-työt valmistuvat odotettua myöhemmin.  
- **Tiimien välinen datanjako:** varmista, että osastojen datatoimitukset tapahtuvat ennen päivän rajojaikoja.  
- **Sääntelyraportointi:** varmista, että toimitukset sisältävät viimeisimmän saatavilla olevan datan tilannekuvan.  

---

## Hyödyt

| Area | Benefit |
|------|----------|
| **Business Continuity** | Estää toimintakatkoksia myöhästyneen tai puuttuvan datan vuoksi |
| **Data Quality** | Parantaa tietoputkien luotettavuutta ja johdonmukaisuutta |
| **Compliance** | Varmistaa SLA:n noudattamisen ja auditoinnin läpinäkyvyyden |
| **Automation** | AI poistaa manuaalisen aikataulujen seurannan tarpeen |
| **Integration** | Toimii saumattomasti yhdessä *Data Analytics* -moduulin kanssa, jotta ajoissa-toimitustrendit voidaan visualisoida ajan kuluessa |

---

## Kuinka digna oppii odotetut toimitusajat

1. **Historiallinen analyysi:** digna tarkkailee aiempia latausaikoja ja kestoja.  
2. **AI-mallinnus:** koneoppiminen luo dynaamisen perustason odotetulle saapumiselle.  
3. **Valvonta:** jokaista uutta toimitusta verrataan perustasoon.  
4. **Hälytys:** poikkeamat laukaisevat hälytyksiä, jotka sisältävät kontekstuaalisia mittareita ja luottamuspisteytyksiä.  

Tämä jatkuva oppiminen mukautuu kehittyviin prosesseihin pitäen väärien positiivisten määrän alhaisena.

---

## Usein kysytyt kysymykset

**Voinko määritellä omat toimitusaikani?**  
Kyllä. digna tukee sekä kiinteitä käyttäjän määrittelemiä aikatauluja että AI:n oppimia malleja.

**Voiko se integroitua ETL- tai orkestrointityökaluuni?**  
Kyllä. digna integroituu työkaluihin kuten Airflow, dbt, Informatica tai mukautetut ajastimet.

**Missä laskenta tapahtuu?**  
Kaikki analyysit ajetaan tietokannassasi tai pilviwarehouse-ympäristössä — ulkoista palvelua ei käytetä.

**Mitä tapahtuu, kun data on myöhässä?**  
digna lähettää hälytyksiä hallintapaneelissa, Inspection Hubissa sekä API:n/webhookien kautta ilmoittaakseen operatiivisille tiimeille välittömästi.

---


**digna Data Timeliness** auttaa varmistamaan **luottamuksen dataan**, yhdistäen **tekoälyllä ohjatun havaitsemisen**, **paikallisen suorituksen** ja **datan havainnoitavuuden** — kaikki hallitussa ympäristössäsi.