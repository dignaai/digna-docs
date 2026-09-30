---
title: Tietokantayhteyksien yleiskatsaus – DSN-vapaa ODBC-määritys | digna-dokumentaatio
description: Näin tietokantayhteydet toimivat dignassa. Jokaiseen lähdeteknologiaan yhdistetään ODBC:n kautta DSN-vapaalla yhteysmerkkijonolla, joka muodostetaan ODBC-ominaisuuksista. Kattaa ajurin asennuksen digna-palvelimelle, Add DB Connection -näkymän, ominaisuuksien salauksen, yhteyden testauksen, vianetsinnän ja linkit teknologiakohtaisiin ohjeisiin.
image: /assets/logo_square.png
keywords:
  - digna tietokantayhteys
  - dsn-vapaa odbc
  - odbc-yhteysmerkkijono
  - odbc-ajurin määritys
  - unixodbc
  - odbc-ominaisuudet
  - tietolähteen määritys
lang: en
robots: index, follow
og_title: digna Database Connections – DSN-less ODBC Setup
og_description: Configure a digna source connection over ODBC without a DSN. Driver installation, ODBC properties, encryption, testing and troubleshooting.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Tietokantayhteyksien yleiskatsaus

---

## Sisällysluettelo

1. [Miten yhteydet toimivat](#how-connections-work)
2. [Teknologiakohtaiset ohjeet](#technology-guides)
3. [Edellytys: asenna ODBC-ajuri digna-palvelimelle](#install-the-driver)
4. [Luo tietokantayhteys](#create-a-database-connection)
5. [ODBC-ominaisuudet](#odbc-properties)
6. [Ominaisuuksien arvojen salaaminen](#encrypting-property-values)
7. [Yhteyden testaaminen](#testing-a-connection)
8. [Minkä tietokannan yhteys näkee](#which-database-the-connection-sees)
9. [Profilointitila ja Work Schema](#profiling-mode-and-work-schema)
10. [DSN:n käyttäminen](#using-a-dsn-instead)
11. [Vianetsintä](#troubleshooting)

---

## Miten yhteydet toimivat {: #how-connections-work }

*digna* yhdistää jokaiseen lähdeteknologiaan **ODBC:n** kautta. Yhteys on luettelo
ODBC-ominaisuuksia, jotka syötät avain–arvo-pareina. Kun *digna* avaa yhteyden, se yhdistää
parit yhteysmerkkijonoksi — `Key=Value`, erottimena `;`, siinä järjestyksessä kuin ne on
lueteltu — ja välittää sen *digna*-palvelimen ODBC-ajurinhallinnalle (driver manager).

Koska syötät ominaisuudet itse, määritys on **DSN-vapaa**: yhteys sisältää kaiken, mitä ajuri
tarvitsee, joten palvelimelle ei tarvitse rekisteröidä ODBC-tietolähdettä (DSN). Tämä on
suositeltu tapa määrittää *digna*, koska yhteyden määritelmä on kokonaan *dignassa* ja siirtyy
sen mukana.

### Miksi ODBC {: #why-odbc }

Aiemmissa julkaisuissa sai valita teknologiakohtaisen ajurin ja ODBC:n välillä **Use ODBC**
-kytkimellä. Release 2026.06:sta alkaen *digna* perustuu pelkästään ODBC:hen. Yksi
standardoitu rajapinta tarjoaa enemmän kuin joukko erillisiä ajureita:

- **Todennus** — todennus on osa ODBC:tä, joten yhteys voi käyttää mitä tahansa ajurinsa
  tukemaa menetelmää: salasanoja, tokeneita ja PAT-tunnuksia, Kerberosta ja Active Directorya,
  MFA:ta ja selainpohjaista kertakirjautumista, pilvi-identiteettejä, asiakasvarmenteita ja TLS:ää.
  Uudet menetelmät tulevat ajuripäivityksen mukana, eikä niitä tarvitse odottaa *dignan*
  julkaisuun.
- **Tietokantatoimittajien ylläpitämät ajurit** — toimittajan oma ajuri pysyy ajan tasalla uusien
  palvelinversioiden ja tietoturvakorjausten kanssa, ja voit päivittää sen omassa aikataulussasi,
  *dignasta* riippumatta.
- **Yksi tapa määrittää kaikki** — jokainen teknologia on luettelo avain–arvo-ominaisuuksia,
  samalla käyttöliittymällä, samalla arkaluonteisten arvojen salauksella ja samalla vianetsinnällä,
  eikä jokaisella lähteellä ole omaa kenttäjoukkoaan.
- **Hienosäätö ja kattavuus** — ajuritason asetukset, kuten aikakatkaisut, TLS-asetukset,
  välityspalvelimet ja noutokoot, ovat käytettävissä jokaiselle lähteelle, ja mihin tahansa
  teknologiaan, jolla on yhteensopiva ODBC-ajuri, voidaan yhdistää — myös niihin, joille *digna*
  ei julkaise erillistä ohjetta.

!!! note "Mikä muuttui käyttöliittymässä"

    **Use ODBC** -kytkintä ja erillisiä kenttiä palvelimelle, portille, tietokannalle,
    käyttäjälle ja salasanalle ei enää ole. Yhteys, joka ei jo käytä ODBC:tä, tarvitsee
    ODBC-ominaisuutensa syötettyinä ennen kuin se toimii taas — katso
    [Luo tietokantayhteys](#create-a-database-connection).

---

## Teknologiakohtaiset ohjeet {: #technology-guides }

Ominaisuuksien nimet vaihtelevat ajureittain, ja jokaisella teknologialla on yksi tai kaksi
yksityiskohtaa, joita muilla ei ole. Alla olevat ohjeet kattavat sen osan; tämä sivu kattaa
*dignan* puolen, joka on sama kaikille.

!!! important "Ohjeiden ominaisuusjoukot ovat esimerkkejä"

    Jokainen ohje näyttää yhden toimivaksi todetun yhdistelmän — sen, jolla *digna* on testattu.
    Se on lähtökohta, ei määrittely: ominaisuudet kuuluvat ODBC-ajurille, ja se, mitkä niistä
    ovat olemassa, miten ne on nimetty ja mitä arvoja ne hyväksyvät, vaihtelee ajuriversioiden
    ja toimittajien välillä, Windowsin, Linuxin ja macOS:n välillä sekä sen mukaan, miten
    lähdepalvelin on määritetty — todennusmenetelmä, TLS, yhdyskäytävä, portti. Varaudu
    säätämään arvoa tai kahta, ja pidä asentamasi ajuriversion dokumentaatiota ratkaisevana.

| Teknologia | Ohje | Hyvä tietää |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless-poolit tarvitsevat isäntänimeen `-ondemand` ja tukevat vain *Standard*-profilointia |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Token-todennus: `UID=token`, PAT kenttään `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Katalogit tulevat ajurilta, eivät kyselystä |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Ajurin nimi on aaltosulkeissa: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` hyväksyy joko täydellisen connect descriptorin tai `tnsnames.ora`-aliaksen |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode`n on vastattava palvelimen vaatimuksia |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token on testattu todennustapa |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` ratkaisee, mitkä skeemat *digna* näkee |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Isäntä annetaan kohdassa `DBCNAME`; tietokannat toimivat skeemoina |

---

## Edellytys: asenna ODBC-ajuri digna-palvelimelle {: #install-the-driver }

*digna* avaa lähdeyhteydet **palvelimelta, jolla digna-backend toimii**, ei selaimesta.
ODBC-ajuri on siksi asennettava tälle koneelle, ja sen nimi on rekisteröitävä paikalliseen
ajurinhallintaan.

=== "Windows"

    Asenna toimittajan 64-bittinen ajuri, avaa sitten **ODBC Data Source Administrator (64-bit)**
    ja siirry **Drivers**-välilehdelle. Siinä luetellut nimet ovat täsmälleen ne arvot, joita
    voit käyttää `Driver`-ominaisuudelle.

=== "Linux"

    Asenna **unixODBC** ja toimittajan ajuri, ja listaa sitten rekisteröityjen ajurien nimet:

    ```bash
    odbcinst -q -d
    ```

    Hakasulkeissa tulostetut nimet ovat arvot, joita voit käyttää `Driver`-ominaisuudelle. Ne
    tulevat tiedostosta `/etc/odbcinst.ini` (tai tiedostosta, jonka `odbcinst -j` ilmoittaa).

=== "macOS"

    Asenna **unixODBC** (esimerkiksi komennolla `brew install unixodbc`) ja toimittajan ajuri,
    ja listaa sitten rekisteröityjen ajurien nimet:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Ajurin nimen on vastattava merkki merkiltä"

    `Driver` välitetään ajurinhallinnalle muuttamattomana. `Simba Spark ODBC Driver` ja
    `Simba Spark ODBC Driver 64` ovat ajurinhallinnan kannalta eri ajureita, ja nimi, jota ei
    ole rekisteröity, tuottaa virheen *data source name not found*, vaikka DSN:ää ei käytetä
    lainkaan.

Rekisteröidyn nimen sijaan kaikki yleiset ajurinhallinnat hyväksyvät myös ajurikirjaston
täyden polun, esimerkiksi `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Tämä on
hyödyllistä, kun ajuri on asennettu mutta ei rekisteröity.

---

## Luo tietokantayhteys {: #create-a-database-connection }

Avaa **Admin Panel**, siirry **Database Connections** -välilehdelle ja klikkaa
**Add DB Connection**. Näkymä kysyy viittä asiaa:

| Kenttä | Kuvaus |
|---|---|
| **Name** | Yhteyden nimi. Sillä viitataan yhteyteen muissa näkymissä. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake tai Hive. Se valitsee SQL-murteen, jota *digna* tuottaa, joten sen on vastattava lähdettä — ei ajuria. Azure Synapse Analytics on **SQL Server** -yhteys. |
| **ODBC Properties** | Avain–arvo-parit, jotka on kuvattu kohdassa [ODBC-ominaisuudet](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* tai *Session* — katso [Profilointitila ja Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Skeema, joka sisältää *Permanent*-profiloinnin työtaulut. |

Yhteyttä hallinnoidaan keskitetysti, ja se liitetään sitten yhteen tai useampaan projektiin,
joten sama yhteys voi palvella useita projekteja.

---

## ODBC-ominaisuudet {: #odbc-properties }

Klikkaa **Add Property** jokaiselle ominaisuudelle ja täytä **Key**, **Value** sekä salaisuuksille
**Encrypted**-valintaruutu. Jokainen teknologiakohtainen ohje luettelee esimerkkijoukon kyseiselle
teknologialle, ja sovitat sen omaan ajuriversioosi ja palvelimeesi — katso
[yllä oleva huomautus](#technology-guides).

Ajurista riippumatta ominaisuusjoukko kattaa samat neljä asiaa:

- **`Driver`** — rekisteröity ajurin nimi, kuten on kuvattu [yllä](#install-the-driver).
- **Palvelimen osoite** — avain vaihtelee ajureittain: `SERVER`, `HOST`, `DBCNAME`,
  `Server` tai Oraclella `DBQ`-connect descriptor.
- **Tunnistetiedot** — yleensä `UID` ja `PWD`; Snowflake käyttää `UID`:tä ja `token`-ominaisuutta,
  ja Databricks käyttää kirjaimellista käyttäjää `token` sekä henkilökohtaista käyttötunnusta
  (personal access token) kentässä `PWD`.
- **Tietokanta tai katalogi, jossa työskennellään**, jos teknologialla sellainen on — katso
  [Minkä tietokannan yhteys näkee](#which-database-the-connection-sees).

Kaiken muun, mitä ajurin dokumentaatio kuvaa, voi lisätä samalla tavalla — yhteyspoolauksen,
socket-aikakatkaisut, Kerberos-asetukset, välityspalvelinasetukset. *digna* ei tulkitse
ominaisuuksia; se vain välittää ne eteenpäin.

!!! warning "Arvoja ei escapata — laita aaltosulkeisiin kaikki, joissa on puolipiste"

    Koska ominaisuudet yhdistetään merkillä `;`, arvo, joka itse sisältää merkin `;`,
    katkaisisi yhteysmerkkijonon väärästä kohdasta. Kirjoita tällaiset arvot aaltosulkeisiin:
    `PWD={p@ss;word}`. Sama koskee arvoja, joissa on `=` tai alkuvälilyöntejä. Tästä syystä
    joidenkin ajurien nimet kirjoitetaan tavallisesti aaltosulkeisiin, kuten `{NetezzaSQL}` tai
    `{SnowflakeDSIIDriver}`.

---

## Ominaisuuksien arvojen salaaminen {: #encrypting-property-values }

Valitse **Encrypted** jokaiselle ominaisuudelle, joka sisältää salaisuuden — `PWD`, `token`,
client secret. Arvo salataan silloin ennen kuin se tallennetaan *dignan* repositorioon, se
peitetään näkymässä, ja se puretaan vasta, kun yhteysmerkkijono kootaan.

!!! tip "Vinkki"

    Salattua arvoa ei voi lukea takaisin käyttöliittymässä eikä API:n kautta — sen voi vain
    korvata. Säilytä salaisuudet myös omassa salasanojen hallintaohjelmassasi.

Ominaisuudet, jotka eivät ole salaisia — ajurin nimi, isäntä, portti, tietokanta — kannattaa
jättää salaamatta, jotta ne pysyvät luettavina sille, joka ylläpitää yhteyttä myöhemmin.

---

## Yhteyden testaaminen {: #testing-a-connection }

Klikkaa **Test** *Add DB Connection* -ikkunassa **ennen** tallentamista. Testi käyttää
lomakkeen nykyisiä arvoja ja muodostaa todellisen yhteyden, joten se ilmoittaa täsmälleen sen,
mihin inspektio törmäisi — väärän ajurin nimen, hylätyn salasanan, tavoittamattoman isännän.
Mitään ei tallenneta: testiyhteys perutaan (rollback), onnistuipa se tai ei.

Jo olemassa olevan yhteyden voit testata uudelleen viemällä osoittimen sen rivin päälle
**Database Connections** -välilehdellä ja klikkaamalla **pistoke**-kuvaketta. Se on nopein tapa
tarkistaa, onko lähde tavoitettavissa salasanan vaihdon tai palomuurimuutoksen jälkeen.

---

## Minkä tietokannan yhteys näkee {: #which-database-the-connection-sees }

Kun lisäät tietolähteen, *digna* tarjoaa ne katalogit, skeemat ja taulut, jotka yhteys
tavoittaa. Se, kuinka laajalle tämä ulottuu, riippuu teknologiasta:

| Teknologia | Tarjotut katalogit |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Vain yhteyden **nykyinen** tietokanta |
| **Teradata**, **Netezza**, **Databricks** | Kaikki tietokannat tai katalogit, jotka käyttäjä saa nähdä |
| **Hive**, **Impala** | Ajurin ilmoittamat |

!!! important "Yksi yhteys, yksi tietokanta"

    PostgreSQL:ssä, SQL Serverissä, Oraclessa ja Snowflakessa ominaisuuksien on osoitettava
    tietokantaan, joka sisältää lähdeskeemat — `DATABASE=…`, `Database=…` tai palvelun nimi
    Oraclen `DBQ`:ssa. Toisen tietokannan tauluihin ei pääse kyseisen yhteyden kautta; lisää
    sitä varten toinen yhteys.

---

## Profilointitila ja Work Schema {: #profiling-mode-and-work-schema }

Profilointitila määrää, miten *digna* käsittelee dataa ja laskee metriikat:

- **Standard:** Metriikat lasketaan suoraan lähdetauluista kopioimatta dataa.
- **Permanent:** Tarkasteltavan päivän data kopioidaan pysyvään tauluun, ja metriikat lasketaan
  kopioidusta datasta.
- **Session:** Data kopioidaan istunto- tai väliaikaistauluun, ja metriikat lasketaan tästä
  väliaikaisesta datasta.

Tila ratkaisee, mitä yhteyden käyttäjällä on oltava oikeus tehdä:

| Tila | Kirjoittaa | Yhteyden käyttäjän tarvitsemat oikeudet |
|---|---|---|
| **Standard** | ei mitään | Lukuoikeus lähdetauluihin |
| **Permanent** | yhden taulun tietolähdettä kohden **Work Schemaan** | Taulujen luonti ja poisto **Work Schemassa** |
| **Session** | väliaikaisen taulun, jonka tietokanta poistaa istunnon päättyessä | Väliaikaisten taulujen luonti — **Work Schemaa** ei käytetä |

*Standard* vain lukee, joten se on oikea tila, kun *dignalle* annetaan vain lukuoikeus.
**Work Schema** luetaan vain *Permanent*-tilassa, mutta se kannattaa silti täyttää, jotta
yhteys toimii edelleen, jos tilaa muutetaan myöhemmin.

---

## DSN:n käyttäminen {: #using-a-dsn-instead }

DSN toimii edelleen — `DSN` on vain yksi ominaisuus muiden joukossa:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN on rekisteröitävä *digna*-palvelimelle samalle käyttäjätilille, joka ajaa *dignan*
backendiä, ja **System DSN** -tyyppisenä, kun *digna* toimii palveluna. Kaiken DSN:ssä
määritetyn voi myös ohittaa lisäämällä sen ominaisuutena.

DSN-vapaa on dokumentoitu oletus, koska se välttää tämän palvelinpuolen tilan: yhteys on
kuvattu kokonaan *dignassa*, ja uudelle *digna*-palvelimelle tarvitsee asentaa ajuri mutta
ei määrittää mitään.

---

## Vianetsintä {: #troubleshooting }

### Data source name not found / no default driver specified

**Oireet:**
- **Test**-painike ilmoittaa virheestä, jossa mainitaan *data source name not found*, vaikka
  määritys on DSN-vapaa

**Syyt ja ratkaisut:**
1. `Driver`-arvo ei vastaa rekisteröidyn ajurin nimeä — vertaa sitä *ODBC Data Source
   Administrator (64-bit)* -ohjelman **Drivers**-välilehteen tai komennon `odbcinst -q -d` tulosteeseen
2. Ajuri on asennettu työasemallesi mutta ei *digna*-palvelimelle
3. Ajuri on 32-bittinen, kun taas *digna* on 64-bittinen — asenna 64-bittinen ajuri
4. `Driver`-ominaisuus puuttuu kokonaan, eikä `DSN`:ää ole annettu
5. Linuxissa ja macOS:ssä ajuri on asennettu mutta ei rekisteröity — anna sen sijaan
   ajurikirjaston täysi polku tai rekisteröi ajuri tiedostoon `odbcinst.ini`

---

### Yhteystesti aikakatkaistaan

**Oireet:**
- **Test** jumittuu ja epäonnistuu noin puolen minuutin kuluttua

**Syyt ja ratkaisut:**
1. Isäntä tai portti ei ole tavoitettavissa *digna*-palvelimelta — tarkista palomuuri ja
   pilvilähteiden osalta IP-sallittujen luettelo
2. Isäntänimi on oikein, mutta portti kuuluu toiselle palvelulle
3. Lähde tarvitsee yhteyden hyväksymiseen oletusarvoista 30 sekuntia pidemmän ajan — kasvata
   arvoa `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` tiedoston `config.toml` osiossa `[base]` (`0` odottaa
   rajattomasti) ja käynnistä backend uudelleen
4. Serverless-päätepiste herää lepotilasta — yritä uudelleen, ja jos tätä tapahtuu
   säännöllisesti, kasvata kirjautumisen aikakatkaisua kuten yllä

---

### Todennus epäonnistuu, vaikka tunnistetiedot ovat oikein

**Oireet:**
- Ajuri ilmoittaa virheellisistä tunnistetiedoista, mutta sama käyttäjä toimii toisessa
  SQL-asiakasohjelmassa

**Syyt ja ratkaisut:**
1. Salasana sisältää merkin `;` — kirjoita arvo aaltosulkeisiin: `{p@ss;word}`
2. Arvoon on kopioitunut välilyönti loppuun
3. Ajuri odottaa tiettyä todennusmekanismia — esimerkiksi `AuthMech` Hive- ja
   Databricks-ajureille tai `authenticator` Snowflakelle
4. Arvo on tallennettu salattuna ja sitä on sitten muokattu — salattuja arvoja ei voi lukea
   takaisin, joten syötä salaisuus uudelleen kokonaan
5. Token on vanhentunut — personal access tokenit ja programmatic access tokenit myönnetään
   voimassaolon päättymispäivän kanssa

---

### Tietolähdenäkymä ei tarjoa odotettua tietokantaa tai skeemaa

**Oireet:**
- Katalogeja, skeemoja tai tauluja puuttuu, kun tietolähdettä lisätään

**Syyt ja ratkaisut:**
1. Yhteys osoittaa eri tietokantaan — katso
   [Minkä tietokannan yhteys näkee](#which-database-the-connection-sees)
2. Yhteyden käyttäjällä ei ole lukuoikeutta skeemaan tai tietosanakirjaan (data dictionary)
3. **Technology** ei vastaa lähdettä, joten *digna* kyselee väärää tietosanakirjaa
4. Snowflakessa käyttäjälle ei ole määritetty oletus-warehousea eikä `Warehouse`-ominaisuutta
   ole annettu, joten metatietokyselyjä ei voi suorittaa

---

### Profilointi epäonnistuu, vaikka yhteystesti onnistuu

**Oireet:**
- **Test** menee läpi, mutta inspektio epäonnistuu työtauluja luotaessa

**Syyt ja ratkaisut:**
1. *Permanent*-profilointi on valittu, eikä yhteyden käyttäjä voi luoda tauluja
   **Work Schemaan** — myönnä oikeudet tai vaihda tilaksi *Session* tai *Standard*
2. **Work Schema** on tyhjä tai viittaa skeemaan, jota ei ole olemassa, kun *Permanent*-profilointi
   on valittu
3. *Session*-profilointi on valittu, eikä yhteyden käyttäjä saa luoda väliaikaisia tauluja
4. Pitkäkestoinen profilointikysely ylittää kyselyn aikakatkaisun — kasvata arvoa
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` tiedoston `config.toml` osiossa `[base]` (oletus 3600
   sekuntia, `0` poistaa aikakatkaisun käytöstä)

---

## Parhaat käytännöt

**TEE NÄIN:**

- Asenna ja rekisteröi ajuri *digna*-palvelimelle ennen yhteyden määrittämistä
- Valitse **Encrypted** jokaiselle salasanalle ja tokenille
- Klikkaa **Test** ennen tallentamista ja testaa uudelleen salasanan vaihdon jälkeen
- Nimeä yhteydet lähteen ja ympäristön mukaan, esimerkiksi `sales_dwh_prod`
- Anna *dignalle* oma tietokantakäyttäjä, jolla on vain lukuoikeus, kun *Standard*-profilointi riittää
- Pidä yksi yhteys lähdetietokantaa kohden, ja lisää toinen yhteys ensimmäisen vaihtamisen sijaan

**ÄLÄ:**

- Tallenna salaisuuksia salaamattomina tai jaa yhtä tietokantakäyttäjää *dignan* ja muiden työkalujen kesken
- Käytä 32-bittistä ajuria 64-bittisen *digna*-asennuksen kanssa
- Luota User DSN:ään, kun *digna* toimii palveluna — se ei ole näkyvissä
- Syötä ominaisuuteen merkin `;` sisältävää arvoa ilman aaltosulkeita
- Osoita **Work Schemaa** skeemaan, joka sisältää lähdedataa

---

## Tuki

Tarvitsetko apua tietokantayhteyden kanssa?

- **Sähköposti:** support@digna.ai
- **Dokumentaatio:** https://docs.digna.ai
- **Verkkosivusto:** https://www.digna.ai

---

**Julkaisu:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
