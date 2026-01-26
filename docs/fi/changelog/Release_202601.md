---
title: digna Release 2026.01 | Loogiset tietolähteet, globaalit yhteydet & Edistynyt Data Validation
description: Lue, mitä uutta digna Release 2026.01 sisältää. Tässä versiossa on globaalit tietokantayhteydet, loogiset tietolähteet, poikkeamien merkitysehdot, CSV-viennit sekä edistynyt Data Validation, mukaan lukien viite-eheystarkistukset.
keywords: digna Release 2026.01, digna muutosloki, digna tietolähde, digna tietokantayhteydet, digna Data Anomalies, digna Data Validation, viite-eheysvalidaatio, datalaatusäännöt, datan havaittavuus, digna CSV-vienti
image: /assets/logo_square.png
---

# Muutokset – Release 2026.01  

Release 2026.01 tuo dignalle merkittäviä parannuksia tietolähdemallinnukseen, yhteyksien hallintaan ja tarkastusten käytettävyyteen.  
Tämä julkaisu lisää joustavuutta kaikissa moduuleissa ja laajentaa merkittävästi datalaadun ja validoinnin kattavuutta.

---

## 🚀 Uudet ominaisuudet  

### Globaalit tietokantayhteydet  
- Tietokantayhteydet konfiguroidaan nyt **globaalilla tasolla**.  
- Globaalit yhteydet voidaan käyttää uudelleen **kaikissa projekteissa**, mikä yksinkertaistaa konfigurointia ja ylläpitoa.  
- **Vaikutus:** Vähentää operatiivista työtä ja varmistaa yhtenäisen yhteydenhallinnan eri ympäristöissä.

### Useita lähdeyhteyksiä projektia kohden  
- Projektit voivat nyt viitata **useisiin lähdeyhteyskonfiguraatioihin**.  
- Mahdollistaa joustavammat asetukset monimutkaisemmissa dataympäristöissä.  
- **Vaikutus:** Tukee realistisia yritysarkkitehtuureja, joissa on heterogeenisiä tietolähteitä.

### Loogiset tietolähteet  
- Tietolähteet edustavat nyt **loogista tasoa** projektissa.  
- Jokainen tietolähde voi olla tuettuina:
    - **tietokantataululla**
    - **tietokantanäkymällä**
    - **mukautetulla SQL-lauseella**  
- Tämä erottelu parantaa uudelleenkäytettävyyttä, selkeyttä ja tarkastusmallintamista eri moduuleissa.  
- **Vaikutus:** Irrottaa tarkastukset ja datalaatusäännöt fyysisestä tallennuksesta, mikä parantaa ylläpidettävyyttä ja uudelleenkäyttöä.

### Poikkeaman merkitysehto  
- Nyt voidaan määrittää **Poikkeaman merkitysehto**, joka ohjaa poikkeaman tilan arviointia aineistotasolla.  
- Tilastot lasketaan riippumatta siitä, onko ehto asetettu tai täyttyy.  
- Jos ehto **ei täyty**, **digna Data Anomalies** ei anna poikkeaman tilaa (vihreä / keltainen / punainen).  
- **Esimerkki:** Poissulje aineisto poikkeaman arvioinnista, kun tietueiden määrä on alle 10.  
- **Vaikutus:** Varmistaa, että poikkeamia arvioidaan vain liiketoimintakonteksteissa, joissa ne ovat merkityksellisiä.

### Moduulikohtaiset ilmoitusasetukset  
- Ilmoitukset voidaan nyt konfiguroida **moduulikohtaisesti** suoraan dignassa.  
- Mahdollistaa hälytysten toimintatavan erillisen hallinnan **digna Data Anomalies**, **digna Data Timeliness**, **digna Data Validation** ja muiden moduulien osalta.  
- **Vaikutus:** Mahdollistaa tarkat ilmoitusstrategiat, jotka vastaavat tiimien vastuuta ja kriittisyyttä.

### Tarkastustulosten vienti (CSV)  
- Käyttäjät voivat nyt **ladata tarkastustulokset CSV-tiedostoina**.  
- Mahdollistaa offline-analyysit, raportoinnin ja integroinnin ulkoisiin työkaluihin.  
- **Vaikutus:** Yksinkertaistaa auditointeja, raportointia ja jatkoanalyysejä datalaadun osalta.

---

## 🧪 Laajennetut Data Validation -ominaisuudet  

Tässä julkaisussa **digna Data Validation** tukee nyt laajaa joukkoa datalaatusääntöjä:

- **Rivikohtaiset validointisäännöt**  
- **Usean sarakkeen yksilöllisyystarkistukset**  
- **Viite-eheyden validointi tietolähteiden välillä**

Nämä tarkistukset yhdessä mahdollistavat **rakenteellisten ja relaatioiden datalaatusääntöjen** toimeenpanon monimutkaisissa dataympäristöissä.

### Yksilöllisyystarkistukset useille sarakkeille
- Lisätty **yksilöllisyystarkistuksia** konfiguroitavalle **sarakekokonaisuudelle**.  
- Mahdollistaa yhdistettyjen avainten ja liiketoimintatasoisten yksilöllisyysrajoitteiden validoinnin.  
- **Vaikutus:** Havaitsee duplikaatit liiketoimintayksiköt, joita ei voida tunnistaa yksittäissarakkeen tarkistuksilla.

### Viite-eheystarkistukset
- Lisätty **viite-eheystarkistukset** validoimaan suhteita tietolähteiden välillä.  
- Varmistaa, että lähdetietolähteen vierasavaimen arvot löytyvät viitatusta kohdetietolähteestä.  
- Auttaa havaitsemaan orpoja rivejä, rikkinäisiä suhteita ja datan yhdenmukaisuuteen liittyviä ongelmia varhaisessa vaiheessa.  
- Suunniteltu toimimaan **loogisten tietolähteiden** kanssa, mukaan lukien näkymät ja mukautetut SQL-lauseet.  
- **Käyttötapaukset:** tietovaraston eheys, sääntelyraportointi, master-datan yhdenmukaisuus ja luotettava analytiikka jatkokäsittelyssä.

---

## 🎯 Kenelle tämä julkaisu hyödyttää  

- **Data-insinöörit:** Joustavampi tietolähdemallinnus ja uudelleenkäytettävät tietokantayhteydet  
- **Datalaatu- ja hallintotiimit:** Laajentunut validointikattavuus, mukaan lukien relaatiotason eheys säännöt  
- **Analytiikka- & BI-tiimit:** Puhdistetummat syötteet ja vietävissä olevat tarkastustulokset  
- **Alustan omistajat:** Vähentynyt konfigurointien monimutkaisuus ja parantunut operatiivinen ylläpidettävyys

---

## 🛠 CLI-päivitykset  
- Ei muutoksia

---