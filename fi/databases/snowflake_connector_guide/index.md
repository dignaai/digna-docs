# Lähdeliitin Snowflakelle

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Snowflakeen **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Snowflakelle ominaista.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **Snowflake ODBC Driver** koneelle, jolla *dignan* backend toimii,
[Snowflaken asennusohjeen](https://docs.snowflake.com/en/developer-guide/odbc/odbc) mukaisesti.

Ajuri rekisteröityy nimellä **SnowflakeDSIIDriver**. Lue tarkka rekisteröity nimi
palvelimeltasi, kuten on kuvattu kohdassa [Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

Snowflakeen yhdistetään **programmatic access tokenilla (PAT)** — todennustavalla, jolla *digna*
on varmennettu ja jota Snowflake edellyttää tileiltä, joilla pelkkä salasanakirjautuminen on
estetty.

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat Snowflaken
    ODBC-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden ja alustojen välillä, ja tilisi sallimat todennusvaihtoehdot ratkaisee tilin
    tietoturvakäytäntö. Käytä tätä lähtökohtana ja tarkista asentamasi ajuriversion
    dokumentaatio.

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `Server` | `<account>.snowflakecomputing.com` | Tilin tunniste ja pääte, esim. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake-käyttäjä, jolle token kuuluu |
| `Database` | `TEST` | Tietokanta, joka sisältää lähdeskeemat. Se on ainoa tietokanta, jota tämä yhteys voi profiloida |
| `Schema` | `PUBLIC` | Istunnon oletusskeema |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Valitsee token-todennuksen |
| `token` | `<programmatic access token>` | Valitse **Encrypted** |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse ja rooli

Kyselyt tarvitsevat warehousen. Jos *dignan* käyttäjällä on oletus-warehouse ja oletusrooli,
istunto ottaa ne käyttöön eikä mitään tarvitse määrittää. Muussa tapauksessa lisää:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse, joka suorittaa profilointikyselyt |
| `Role` | `DIGNA_READER` | Rooli, jonka oikeuksia istunto käyttää |

!!! tip "Anna dignalle oma warehouse"

    Erillinen, pieni, automaattisesti keskeytyvä warehouse pitää profiloinnin kustannukset
    näkyvinä ja estää *dignaa* kilpailemasta laskentakapasiteetista interaktiivisten
    käyttäjien kanssa.

### Salasanatodennus

Jos tili vielä sallii sen, salasana toimii tokenin sijaan — poista `authenticator` ja `token`
ja lisää:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `PWD` | `<password>` | Valitse **Encrypted** |

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Huomioita Snowflakesta {: #4-notes-on-snowflake }

- **Tokenit vanhenevat.** Programmatic access token myönnetään tietyksi ajaksi, ja profilointi
  pysähtyy sinä päivänä, kun se raukeaa. Kirjaa voimassaolon päättymispäivä muistiin, kun luot
  tokenin, ja syötä uusi token `token`-ominaisuuteen — salatut arvot voi korvata mutta ei lukea
  takaisin.
- **Yksi yhteys näkee yhden tietokannan.** *digna* tarjoaa `Database`-ominaisuudessa nimetyn
  tietokannan skeemat, koska Snowflake ilmoittaa katalogiksi vain nykyisen tietokannan.
  Toisessa tietokannassa olevat lähdetaulut tarvitsevat oman yhteytensä.
- **Tunnisteet ovat isoilla kirjaimilla**, ellei niitä ole luotu lainausmerkeissä. *digna*
  käyttää nimiä sellaisina kuin Snowflake ne ilmoittaa.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan**, joten rooli tarvitsee
  siellä `CREATE TABLE` -oikeuden. *Session* käyttää lausetta `CREATE TEMPORARY TABLE` eikä
  koske **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden — eikä lainkaan
  kirjoitusoikeuksia.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että ajuri, tilin URL-osoite ja tunnistetietosi toimivat,
ennen kuin syötät ne *dignaan*.

#### Vaihe 1
![Vaihe 1](images/snowflake/create_odbc_data_source_step1.png)

Huomioita:

- **Server**-arvo koostuu Snowflake-tilisi tunnisteesta, jota seuraa
  `.snowflakecomputing.com`.
- Tässä syötetyt **Database**, **Schema** ja **Warehouse** vastaavat [kohdan 2](#2-odbc-properties)
  ominaisuuksia `Database`, `Schema` ja `Warehouse`.

#### Vaihe 2 – Testaa yhteys

Klikkaa **TEST**-painiketta. Onnistunut yhteys näyttää tältä:

![Vaihe 2](images/snowflake/create_odbc_data_source_step2.png)