# Lähdeliitin MS SQL Serverille

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Microsoft SQL Serveriin **ODBC:n**
kautta **DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on SQL Serverille ominaista.

!!! note "Azure Synapse Analytics"

    Myös Synapse määritetään SQL Server -yhteytenä, eri isäntänimellä ja muutamalla
    lisähuomiolla — katso [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **ODBC Driver 18 for SQL Server** koneelle, jolla *dignan* backend toimii,
[Microsoftin asennusohjeen](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) mukaisesti.

Windowsin mukana pelkällä nimellä **SQL Server** toimitettava ajuri toimii myös, mutta se on
aikoja sitten korvattu, eikä se tue nykyaikaisia TLS-asetuksia eikä Azure-todennusta. Käytä
sitä vain, jos nykyisen ajurin asentaminen ei ole mahdollista.

Lue rekisteröidyn ajurin tarkka nimi palvelimeltasi, kuten on kuvattu kohdassa
[Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat Microsoftin
    ODBC-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden välillä — esimerkiksi Driver 18 salaa oletuksena, mitä Driver 17 ei tehnyt —
    sekä alustojen välillä. Käytä tätä lähtökohtana ja tarkista asentamasi ajuriversion
    dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `SERVER` | `sql.example.com` | Palvelimen nimi tai IP-osoite. Nimetyt instanssit: `host\instance`; muu kuin oletusportti: `host,1433` |
| `PORT` | `1433` | Jätä pois, kun portti on jo osa `SERVER`-arvoa |
| `DATABASE` | `digna_source_db` | Tietokanta, joka sisältää lähdeskeemat. Se on ainoa tietokanta, jota tämä yhteys voi profiloida |
| `UID` | `digna_source_user` | Tietokantakäyttäjä |
| `PWD` | `<password>` | Valitse **Encrypted** |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Salaus ODBC Driver 18:lla

Driver 18 salaa yhteydet oletuksena ja validoi palvelimen varmenteen. Jos palvelimen
varmenteeseen *digna*-palvelimesi ei luota — tyypillisesti itse allekirjoitettu varmenne —
yhteys epäonnistuu varmenneketjuvirheeseen. Lisää:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Encrypt` | `yes` | Oletus Driver 18:ssa; aseta arvoksi `no` vain, jos palvelin ei tue TLS:ää |
| `TrustServerCertificate` | `yes` | Ohittaa varmenteen validoinnin. Kätevä testiympäristöissä; tuotannossa asenna mieluummin varmenne |

### Windows-todennus

Jos haluat yhdistää *digna*-palvelua ajavana tilinä SQL-kirjautumisen sijaan, poista `UID` ja
`PWD` ja lisää:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Trusted_Connection` | `yes` | *dignan* palvelutili tarvitsee tietokantaoikeudet |

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Huomioita MS SQL Serveristä {: #4-notes-on-ms-sql-server }

- **Yksi yhteys näkee yhden tietokannan.** *digna* tarjoaa `DATABASE`-ominaisuudessa nimetyn
  tietokannan skeemat, koska SQL Server ilmoittaa katalogiksi vain nykyisen tietokannan.
  Toisessa tietokannassa olevat lähdetaulut tarvitsevat oman yhteytensä.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan**, joten käyttäjä tarvitsee
  siellä `CREATE TABLE` -oikeuden. *Session* käyttää paikallisia väliaikaistauluja (`#wt_…`)
  tietokannassa `tempdb` eikä koske **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden.
- **`SERVER` sisältää instanssin ja portin.** Nimetyn instanssin kanssa `host\instance`
  edellyttää, että SQL Server Browser -palvelu on tavoitettavissa; `host,port` välttää tämän.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ohjattu toiminto on kätevä tapa varmistaa, että ajuri toimii ja että palvelin hyväksyy
tunnistetietosi, ennen kuin syötät ne *dignaan*.

#### Vaihe 1
![Vaihe 1](images/sqlserver/create_odbc_data_source_step1.png)

Klikkaa **Next >** -painiketta.

#### Vaihe 2
![Vaihe 2](images/sqlserver/create_odbc_data_source_step2.png)

Valitse todennustapa (esim. käyttäjätunnus ja salasana)
ja anna tarvittavat tiedot.

Klikkaa **Next >** -painiketta.

#### Vaihe 3
![Vaihe 3](images/sqlserver/create_odbc_data_source_step3.png)

Valitse ANSI-yhteensopivat asetukset ja klikkaa sitten **Next >** -painiketta.

#### Vaihe 4
![Vaihe 4](images/sqlserver/create_odbc_data_source_step4.png)

Voit jättää oletusasetukset tai valita lokitusasetukset tarpeen mukaan
ja klikata **Finish**-painiketta.

#### Vaihe 5
![Vaihe 5](images/sqlserver/create_odbc_data_source_step5.png)

Klikkaa nyt **Test datasource** -painiketta.

#### Vaihe 6
![Vaihe 6](images/sqlserver/create_odbc_data_source_step6.png)

Onnistumisnäkymä vahvistaa, että ajuri ja tunnistetiedot toimivat. Syöttämäsi arvot ovat
täsmälleen ne arvot, jotka [kohdan 2](#2-odbc-properties) ominaisuudet saavat.