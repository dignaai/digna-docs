# Lähdeliitin Databricksille

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Databricksiin **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Databricksille ominaista.

!!! note "Unity Catalog on pakollinen"

    *digna* lukee käytettävissä olevat katalogit näkymästä `system.information_schema.catalogs`,
    joten työtilassa on oltava Unity Catalog käytössä. Aiemmat *dignan* julkaisut tarjosivat
    erillisen "Databricks Legacy" -teknologian työtiloille ilman Unity Catalogia; sitä ei ole
    enää saatavilla.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **Databricks ODBC Driver** koneelle, jolla *dignan* backend toimii,
[Databricksin asennusohjeen](https://docs.databricks.com/aws/en/integrations/odbc/) mukaisesti.

Versiosta riippuen ajuri rekisteröityy nimellä **Simba Spark ODBC Driver** tai
**Databricks ODBC Driver**. Lue tarkka rekisteröity nimi palvelimeltasi, kuten on kuvattu
kohdassa [Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. Kerää yhteystiedot {: #2-gather-the-connection-details }

Kaikki arvot tulevat SQL warehousesta (tai klusterista), jota haluat *dignan* käyttävän. Avaa
se Databricks-työtilassa ja siirry kohtaan **Connection details**:

| Databricks-kenttä | Käytetään ominaisuutena |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, tavallisesti `443` |
| **HTTP path** | `HTTPPath` |

Luo todennusta varten **personal access token** — katso
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokenit kuuluvat käyttäjälle tai service principalille, ja kyseinen principal tarvitsee
lähdedataan oikeudet `USE CATALOG`, `USE SCHEMA` ja `SELECT`.

---

## 3. ODBC-ominaisuudet {: #3-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat
    Databricks/Simba-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden välillä — ajuri on nimetty uudelleen ja sen todennusvaihtoehtoja
    laajennettu useammin kuin kerran — sekä alustojen välillä. Käytä tätä lähtökohtana ja
    tarkista asentamasi ajuriversion dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `Host` | `<workspace>.cloud.databricks.com` | Warehousen palvelinnimi, esim. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Warehousen tai klusterin HTTP-polku |
| `SSL` | `1` | Databricks-päätepisteet ovat vain TLS-yhteyksiä varten |
| `ThriftTransport` | `2` | HTTP-siirto, jota SQL-päätepisteet käyttävät |
| `AuthMech` | `3` | Token-todennus |
| `UID` | `token` | Kirjaimellisesti sana `token`, ei käyttäjätunnus |
| `PWD` | `dapi…` | Personal access token. Valitse **Encrypted** |
| `UseNativeQuery` | `1` | Välittää *dignan* SQL:n muuttamattomana — katso alla |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Pidä `UseNativeQuery=1`"

    Arvolla `UseNativeQuery=0` — ajurin oletus — ajuri kirjoittaa saapuvan SQL:n uudelleen
    muotoon, jota se pitää siirrettävänä ODBC-syntaksina. *digna* tuottaa jo valmiiksi
    Databricks-SQL:ää, joten uudelleenkirjoitus voi muuttaa backtick-lainauksia ja
    päivämääräliteraaleja, jolloin profilointi epäonnistuu lauseissa, jotka ovat sellaisenaan
    kelvollisia.

### OAuth tokenin sijaan

Service principalille, joka käyttää OAuth machine-to-machine -todennusta, korvaa `AuthMech`,
`UID` ja `PWD` seuraavilla:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Valitse **Encrypted** |

---

## 4. *digna*-määritys {: #4-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Huomioita Databricksista {: #5-notes-on-databricks }

- **Warehousen on oltava käynnissä** tai kyettävä käynnistymään, kun *digna* yhdistää.
  Pysäytetystä tilasta käynnistyvä warehouse voi viedä kauemmin kuin yhteyden aikakatkaisu
  sallii — jos testi epäonnistuu ensimmäisellä yrityksellä käyttämättömän jakson jälkeen,
  yritä uudelleen.
- **Katalogit tulevat työtilasta.** Toisin kuin useimmissa teknologioissa, yksi
  Databricks-yhteys tavoittaa jokaisen katalogin, jonka principal saa nähdä, joten yksi yhteys
  voi palvella lähteitä useissa katalogeissa.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan** lähteen katalogin sisällä,
  joten principal tarvitsee siellä `CREATE TABLE` -oikeuden. *Session* käyttää lausetta
  `CREATE TEMPORARY TABLE` eikä koske **Work Schemaan**. *Standard* tarvitsee vain
  lukuoikeuden.
- **Serverless-warehouset toimivat** samalla tavalla; vain `HTTPPath` eroaa.

---

## 6. Ajurin tarkistaminen (valinnainen) {: #6-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että ajuri, warehouse ja token toimivat, ennen kuin syötät ne
*dignaan*.

#### Vaihe 1
![Vaihe 1](images/databricks/create_odbc_data_source_step1.png)

#### Vaihe 2
![Vaihe 2](images/databricks/create_odbc_data_source_step2.png)

#### Vaihe 3
![Vaihe 3](images/databricks/create_odbc_data_source_step3.png)

#### Vaihe 4
![Vaihe 4](images/databricks/create_odbc_data_source_step4.png)

#### Vaihe 5 – Testaa yhteys

Klikkaa **TEST**-painiketta. Onnistunut yhteys näyttää tältä:

![Vaihe 5](images/databricks/create_odbc_data_source_step5.png)

Tähän syötetyt isäntä, HTTP-polku ja token ovat täsmälleen ne arvot, jotka
[kohdan 3](#3-odbc-properties) ominaisuudet saavat.