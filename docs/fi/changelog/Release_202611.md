---
title: digna Release 2026.11 | Data Reconciliation (Beta), digna Agentic (Beta) ja digna Engine
description: Tutustu, mitä uutta digna Release 2026.11 tuo. Tämä versio esittelee kolme merkittävää lisäystä - digna Data Reconciliation (Beta), digna Agentic (Beta) ja digna MCP Server sekä digna Engine, joka mahdollistaa viite-eheyden tarkistukset eri tietokantateknologioiden välillä.
keywords: digna Release 2026.11, digna muutosloki, digna Data Reconciliation, datan täsmäytys, ETL-validointi, täsmäytys lähteestä kohteeseen, digna Agentic, digna MCP Server, tekoälyagentit datan laatu, digna Engine, viite-eheys yhteyksien välillä, kyselyattribuutit, dataprofilointi, data observability
image: /assets/logo_square.png
---

# Muutosloki – Release 2026.11  

Release 2026.11 rakentuu kolmen merkittävän lisäyksen ympärille:

- **digna Data Reconciliation (Beta)**: tarkistaa, että data pysyy yhdenmukaisena, kun se siirtyy järjestelmästä toiseen  
- **digna Agentic (Beta)**: avaa dignan tekoälyagenteille digna MCP Serverin kautta  
- **digna Engine**: profiloi datan valinnaisesti dignan sisällä ja mahdollistaa viite-eheyden tarkistukset eri tietokantateknologioiden välillä  

---

## Uudet ominaisuudet  

### digna Data Reconciliation (Beta) – Yhdenmukaisuus lähteestä kohteeseen  
Data kulkee usein useiden järjestelmien läpi ennen kuin se päätyy raporttiin. digna Data Reconciliation (Beta) vertaa **kohde**tietolähdettä niihin **lähteisiin**, joista se on muodostettu, ja hälyttää, kun ne eivät enää täsmää.

- Määritetään nimettyinä sääntöinä kohdetietolähteen uudella **Data Reconciliation** -välilehdellä  
- Mikä tahansa projektin tietolähde, jossa Data Reconciliation on käytössä, voi toimia lähteenä  
- Käyttötapauksia ovat muun muassa vakiintuneet täsmäytysmenettelyt ja ETL-prosessien tulosten validointi  
- Kaksi sääntötyyppiä: **Exact** ja **AI**  

**Exact-säännöt – Täsmäytys datan laatusääntönä**: Määrität tarkasti, minkä on täsmättävä yhden lähteen ja yhden kohteen välillä, kuten datan laatusäännössä.

  - Vertaa yhtä lähdetietolähdettä yhteen kohdetietolähteeseen  
  - Yhdistä kohteen tarkistus lähteen tarkistukseen tilaston ja attribuutin perusteella, esim. rivimäärät tai summasarakkeen summa  
  - Salli ero **absolute**-toleranssilla (esim. ± 10) tai **relative**-toleranssilla (esim. ± 0,5 % lähteestä)  
  - Aikajana näyttää kunkin päivän eron suhteessa toleranssiin  

**AI-säännöt – Täsmäytys datan havainnointina**: digna oppii, miten kohde seuraa lähteitään, samaan tapaan kuin digna havainnoi dataa muissa moduuleissa, ja hälyttää, kun tämä suhde katkeaa.

  - Yhdistä useiden lähdetietolähteiden tarkistukset yhden kohteen tarkistuksiin  
  - Niiden välistä logiikkaa (joinit, suodattimet, aggregoinnit) ei tarvitse tuntea eikä kirjoittaa auki  
  - Malli oppii historiasta, miten kohde seuraa lähteitään samana päivänä  
  - Jokainen kohteen tarkistus ennustetaan päivän lähdearvoista, ja digna hälyttää, kun kohde poistuu säännön omien aiempien virheiden muodostamalta kaistalta  
  - Jokaisella säännöllä on omat **Model settings** -asetuksensa: **Sensitivity**, **Memory** ja **Model Complexity**  

Täsmäytystarkistukset näkyvät Dashboardilla, ja jokaisella säännöllä on oma aikajanansa. Ne vaikuttavat tarkastuksen kokonaistilaan ja käynnistävät ilmoituksia.

**Vaikutus:** Kattaa täsmäytyksen molemmat puolet. Exact-säännöt valvovat tunnettuja kontrolleja lähteen ja kohteen välillä, ja AI-säännöt monitoroivat monimutkaisia virtoja, kuten ETL-prosesseja, joten matkalla kadonnut tai muuttunut data havaitaan ilman käsin kirjoitettua täsmäytys-SQL:ää.

---

### digna Agentic (Beta) – digna tekoälyagenteille  
digna Agenticin (Beta) ensimmäinen versio. Tekoälyagentit voivat nyt työskennellä dignan kanssa, vastata dataasi koskeviin liiketoimintakysymyksiin ja auttaa parantamaan konfiguraatiotasi.

**digna MCP Server**: Antaa Clauden ja muiden tekoälyagenttien työskennellä dignan kanssa Model Context Protocolin kautta.

  - Hallitse projekteja, tietolähteitä, sääntöjä, tarkastusaikatauluja ja tilauksia  
  - Lue tarkastusten tilat yksittäiseen tarkistukseen asti hälytysten selvittämiseksi  

**Kuvaukset tietolähteille ja attribuuteille**: Kuvaa selkokielellä, mitä tietolähde tai attribuutti sisältää.

  - Tekoälyagentit käyttävät kuvauksia datasi tulkitsemiseen  
  - Esitä dataasi koskevia liiketoimintakysymyksiä, ja tekoälyagentit vastaavat niihin sen perusteella, mitä digna monitoroi  
  - Jos dignan nykyinen konfiguraatio ei pysty vastaamaan kysymykseen, tekoälyagentti ehdottaa mahdollisuuksien mukaan muutoksia tietolähteeseen ja sen attribuutteihin, esim. uuden datasetin lisäämistä  

**Vaikutus:** Voit esittää dataasi koskevia liiketoimintakysymyksiä selkokielellä, ja tekoälyagentit voivat auttaa dignan konfiguroinnissa ja datan laatuongelmien selvittämisessä.

---

### digna Engine – Profiloi siellä, missä haluat  
Oletuksena digna profiloi datan siellä, missä se sijaitsee, eli lähdetietokannassa. digna Engine tuo lisävaihtoehdon: digna vie datan lähteestä ja profiloi sen digna Enginen sisällä.

- Valinnainen, ei pakollinen: profilointi lähdetietokannassa on edelleen käytettävissä  
- Valitaan tietokantayhteyskohtaisesti yhteyden **profilointisijainniksi**: **Source Database** tai **digna Engine**  
- Käytettävissä kaikille tuetuille lähdeteknologioille  

**Viite-eheys yhteyksien välillä**: Jotkin tarkistukset edellyttävät datan vientiä. digna Engine laajentaa **digna Data Validationia** näitä tapauksia varten.

  - **Viite-eheyden tarkistukset** tietolähteiden välillä, jotka ovat **eri tietokantayhteyksissä**, myös eri tietokantateknologioiden välillä (esim. Oracle ja PostgreSQL)  
  - Toimii molempien profilointisijaintien kanssa: Source Databasea käytettäessä digna Engineen viedään vain avainsarakkeet  
  - Kojelauta näyttää, kun tarkistus suoritetaan kahden yhteyden välillä  

**Vaikutus:** Voit valita, missä data profiloidaan, ja valvoa suhteita järjestelmien välillä, jotka toimivat eri tietokantateknologioilla.

---

## Profiloinnin parannukset  

Tämä julkaisu antaa käyttäjille myös enemmän hallintaa siihen, mitä profiloidaan ja miten.

### Kyselyattribuutit – Käyttäjän määrittämät sarakkeet  
- Määritä keinotekoisia sarakkeita: SQL-lauseke yhden tai useamman tietolähteen sarakkeen pohjalta  
- Jokaisella kyselyattribuutilla on oma nimensä  
- Profiloidaan ja tarkistetaan kuten mikä tahansa muu attribuutti  

### DATE-sarakekategoria  
- Uusi **Date**-kategoria attribuuteille  
- Mittarit suhteessa tarkastettavaan päivämäärään  

### Profilointi tarvittaessa  
- Profiloi mikä tahansa attribuutti yhden päivämäärän täydestä tilannevedoksesta ilman tarkastuksen ajamista  
- Auttaa asettamaan attribuutin saraketyypin: **Numerical**, **Categorical**, **Date** tai **Unspecified**  

---

## Ketä tämä julkaisu hyödyttää  

- **Data-insinöörit:** ETL-tulosten validointi digna Data Reconciliationilla (Beta)  
- **Talous-, riski- ja controlling-tiimit:** Vakiintuneet täsmäytysmenettelyt tarkkoina sääntöinä digna Data Reconciliationissa (Beta)  
- **Datan laadun ja hallinnan tiimit:** Viite-eheys eri tietokantateknologioiden välillä digna Enginen avulla  
- **Liiketoimintakäyttäjät:** Tekoälyagentit vastaavat dataa koskeviin liiketoimintakysymyksiin digna Agenticin (Beta) avulla  
- **Tekoäly- ja automaatiotiimit:** Tekoälyagentit työskentelevät dignan kanssa digna Agenticin (Beta) kautta  

---

## CLI-päivitykset  
- Ei muutoksia  

---
