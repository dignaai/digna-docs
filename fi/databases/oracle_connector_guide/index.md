# Lähdeliitin Oraclelle

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Oracle Databaseen **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Oraclelle ominaista.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Oraclen ODBC-ajuri on osa **Oracle Clientia** (Instant Clientin "ODBC"-paketti riittää).
Asenna se koneelle, jolla *dignan* backend toimii, toimittajan virallisen asennusohjeen
mukaisesti.

Ajuri rekisteröityy nimellä **Oracle in `<OracleHomeName>`** — esimerkiksi
`Oracle in OraDB21Home1` tai `Oracle in instantclient_21_13`. Home-nimi vaihtelee
asennuksittain, joten lue tarkka nimi palvelimeltasi, kuten on kuvattu kohdassa
[Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat Oraclen
    ODBC-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    client-versioiden välillä, ja erityisesti ajurin nimi riippuu palvelimesi Oracle homesta.
    Käytä tätä lähtökohtana ja tarkista asentamasi client-version dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Tietokanta, johon yhdistetään — katso alla |
| `UID` | `DIGNA_SOURCE_USER` | Tietokantakäyttäjä |
| `PWD` | `<password>` | Valitse **Encrypted** |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ`-arvo

`DBQ` hyväksyy kolme muotoa. Ne ovat *dignan* kannalta samanarvoisia; ne eroavat siinä, mitä
*digna*-palvelimelle on määritettävä:

| Muoto | Esimerkki | Edellyttää |
|---|---|---|
| **Täydellinen connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Ei mitään — kaikki on ominaisuudessa. Suositeltu |
| **TNS-alias** | `DIGNA_SOURCE` | Aliaksen on oltava olemassa *digna*-palvelimen Oracle Clientin tiedostossa `tnsnames.ora` |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client, joka tukee Easy Connectia (12c ja uudemmat) |

!!! tip "Suosi täydellistä descriptoria"

    TNS-alias siirtää puolet yhteyden määritelmästä *digna*-palvelimella olevaan tiedostoon,
    jossa se unohtuu helposti, kun palvelin rakennetaan uudelleen tai *digna* siirretään.
    Täydellinen descriptor pitää yhteyden itsenäisenä — mikä on DSN-vapaan määrityksen
    tarkoitus.

Huomaa, että descriptorin sulkeet toimivat yhteysmerkkijonossa ongelmitta, mutta jos
salasanasi sisältää merkin `;`, kirjoita se aaltosulkeisiin: `PWD={p@ss;word}`.

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Huomioita Oraclesta {: #4-notes-on-oracle }

- **Skeemat ovat käyttäjiä.** *digna* listaa Oraclen käyttäjät skeemoina, joten lähdeskeema on
  taulujen omistaja — yllä olevassa esimerkissä `DIGNA_SOURCE_USER`. Yhteyden käyttäjä tarvitsee
  `SELECT`-oikeuden näihin tauluihin joko suoraan tai roolin kautta.
- **Yksi yhteys näkee yhden tietokannan.** *dignan* tarjoama katalogi on tietokanta, johon
  yhteys on liitetty, joten `DBQ` ratkaisee, mikä palvelu — ja siten mikä tietokanta —
  profiloidaan.
- **Tunnisteet ovat kirjainkokoherkkiä lainausmerkeissä.** *digna* lainaa nimet, jotka se lukee
  tietosanakirjasta (data dictionary), eli sen, mitä Oracle tallentaa — isot kirjaimet
  lainaamattomille objekteille.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan**, joten käyttäjä tarvitsee
  siellä `CREATE TABLE` -oikeuden ja kiintiön taulualueelle (tablespace). *Session* käyttää
  yksityistä väliaikaistaulua (`ORA$PTT_…`, Oracle 18c ja uudemmat) eikä koske
  **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että Oracle Client, palvelun nimi ja tunnistetietosi
toimivat, ennen kuin syötät ne *dignaan*.

#### Vaihe 1
![Vaihe 1](images/oracle/create_odbc_data_source_step1.png)

Tässä tarjottu **TNS Service Name** tulee Oracle Client -asennuksesi tiedostosta
`tnsnames.ora` — siellä alias ja sen mukana isäntä, portti ja palvelun nimi on määritetty.
Voit käyttää *dignassa* aliasta `DBQ`:na tai sen sijaan täydellistä descriptoria.

#### Vaihe 2 – Testaa yhteys

Klikkaa **Test Connection** -painiketta.

![Vaihe 2](images/oracle/create_odbc_data_source_step2.png)

Anna salasana ja klikkaa **OK**-painiketta.

![Vaihe 3](images/oracle/create_odbc_data_source_step3.png)

Onnistumisilmoitus vahvistaa, että ajuri ja tunnistetiedot toimivat.