# Lähdeliitin PostgreSQL:lle

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään PostgreSQL:ään **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on PostgreSQL:lle ominaista.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna PostgreSQL:n ODBC-ajuri (**psqlODBC**) koneelle, jolla *dignan* backend toimii,
toimittajan virallisen asennusohjeen mukaisesti.

Ajuri rekisteröityy nimellä, joka vaihtelee alustan ja paketin mukaan — yleensä
**PostgreSQL Unicode(x64)** Windowsissa ja **PostgreSQL ODBC Driver(UNICODE)** Linuxissa.
Lue tarkka nimi palvelimeltasi, kuten on kuvattu kohdassa
[Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver), ja käytä tätä nimeä
alla olevalle `DRIVER`-ominaisuudelle.

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat
    psqlODBC-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden ja alustojen välillä, ja myös palvelimesi vaatimukset — erityisesti SSL —
    voivat poiketa. Käytä tätä lähtökohtana ja tarkista asentamasi ajuriversion dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `SERVER` | `db.example.com` | Palvelimen nimi tai IP-osoite |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Tietokanta, joka sisältää lähdeskeemat. Se on ainoa tietokanta, jota tämä yhteys voi profiloida |
| `UID` | `digna_source_user` | Tietokantakäyttäjä |
| `PWD` | `<password>` | Valitse **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` tai `verify-full` — palvelimen on hyväksyttävä se |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Minkä tahansa muun psqlODBC-asetuksen voi lisätä lisäominaisuutena — esimerkiksi
`ReadOnly=1` vain luku -istuntoa varten tai `ConnSettings`, jolla ajetaan `SET`-lauseita
yhteyden muodostamisen yhteydessä.

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Huomioita PostgreSQL:stä {: #4-notes-on-postgresql }

- **`SSLMode`n on vastattava palvelinta.** Palvelin, joka on määritetty `hostssl`-asetuksella,
  hylkää arvon `SSLMode=disable`, ja `verify-ca` tai `verify-full` vaativat lisäksi, että
  juurivarmenne on ajurin käytettävissä *digna*-palvelimella. Jos jouduit valitsemaan tietyn
  tilan ajuria testatessasi, käytä samaa tilaa tässä.
- **Yksi yhteys näkee yhden tietokannan.** *digna* tarjoaa `DATABASE`-ominaisuudessa nimetyn
  tietokannan skeemat, koska PostgreSQL ilmoittaa katalogiksi vain nykyisen tietokannan.
  Toisessa tietokannassa olevat lähdetaulut tarvitsevat oman yhteytensä.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan**, joten käyttäjä tarvitsee
  kyseiseen skeemaan `CREATE`-oikeuden. *Session* käyttää lausetta `CREATE TEMPORARY TABLE`
  eikä koske **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että ajuri toimii ja että palvelin hyväksyy
tunnistetietosi ja SSL-tilasi, ennen kuin syötät ne *dignaan*.

#### Vaihe 1
![Vaihe 1](images/postgres/create_odbc_data_source_step1.png)

#### Vaihe 2 – Testaa yhteys

Klikkaa **Test Connection** -painiketta.

![Vaihe 2](images/postgres/create_odbc_data_source_step2.png)

Tähän syöttämäsi arvot ovat täsmälleen ne arvot, jotka [kohdan 2](#2-odbc-properties)
ominaisuudet saavat.