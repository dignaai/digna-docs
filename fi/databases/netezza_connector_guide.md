# Lähdeliitin Netezzalle

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Netezzaan **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Netezzalle ominaista.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **NetezzaSQL**-ODBC-ajuri (osa IBM Netezza -asiakastyökaluja) koneelle, jolla *dignan*
backend toimii, toimittajan virallisen asennusohjeen mukaisesti.

Lue rekisteröidyn ajurin tarkka nimi palvelimeltasi, kuten on kuvattu kohdassa
[Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat
    NetezzaSQL-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    client-versioiden ja alustojen välillä, ja TLS-suojattu laite (appliance) tarvitsee
    enemmän kuin tässä näytetyt ominaisuudet. Käytä tätä lähtökohtana ja tarkista asentamasi
    client-version dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä. Aaltosulkeet ovat tavallinen tapa kirjoittaa tämä nimi |
| `SERVER` | `netezza.example.com` | Palvelimen nimi tai IP-osoite |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Tietokanta, josta istunto alkaa |
| `UID` | `ADMIN` | Tietokantakäyttäjä |
| `PWD` | `<password>` | Valitse **Encrypted** |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Ajuriversiosta, määrityksestä ja tietoturvavaatimuksista riippuen lisäominaisuuksia voidaan
tarvita — esimerkiksi `SecurityLevel` ja `CaCertFile` TLS-suojatulle laitteelle. Jokaisen
asetuksen, jota ajurin *Advanced*-, *SSL*- ja *Driver*-ikkunat tarjoavat, voi lisätä
ominaisuutena.

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Huomioita Netezzasta {: #4-notes-on-netezza }

- **Sekä katalogit että skeemat ovat käytössä.** *digna* listaa tietokannat, jotka käyttäjä saa
  nähdä (näkymästä `_V_DATABASE`), katalogeina ja niiden skeemat (näkymästä `_V_SCHEMA`) niiden
  alla, joten yksi yhteys voi palvella lähteitä useammassa kuin yhdessä tietokannassa.
  `DATABASE` ratkaisee vain, mistä istunto alkaa.
- **Tunnisteet ovat isoilla kirjaimilla**, ellei niitä ole luotu lainausmerkeissä, minkä vuoksi
  yllä olevat esimerkit käyttävät arvoja `TEST` ja `ADMIN`.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan**, joten käyttäjä tarvitsee
  siellä `CREATE TABLE` -oikeuden. *Session* käyttää lausetta `CREATE TEMPORARY TABLE` eikä
  koske **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että ajuri ja tunnistetietosi toimivat, ennen kuin syötät ne
*dignaan*.

#### Vaihe 1
![Vaihe 1](images/netezza/create_odbc_data_source_step1.png)

**DSN Options** -kohdan kentät vastaavat yksi yhteen [kohdan 2](#2-odbc-properties)
ominaisuuksia. Netezza-ajuristasi, määrityksestä ja tietoturvavaatimuksista riippuen saatat
tarvita tietoja myös välilehdillä **Advanced DSN Options**, **SSL DSN Options** tai
**Driver Options**; yksinkertaisimmassa määrityksessä **DSN Options** riittää.

Klikkaa **Test Connection** -painiketta.

#### Vaihe 2
![Vaihe 2](images/netezza/create_odbc_data_source_step2.png)

Kun saat onnistumisnäkymän, ajuri toimii ja arvot ovat oikein.