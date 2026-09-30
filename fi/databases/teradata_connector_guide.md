# Lähdeliitin Teradatalle

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Teradataan **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Teradatalle ominaista.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **ODBC Driver for Teradata** koneelle, jolla *dignan* backend toimii, toimittajan
virallisen asennusohjeen mukaisesti.

Ajuri rekisteröityy nimellä, joka sisältää sen version, esimerkiksi
**Teradata Database ODBC Driver 20.00**. Lue tarkka rekisteröity nimi palvelimeltasi, kuten on
kuvattu kohdassa [Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat Teradatan
    ODBC-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden välillä — versio on osa itse ajurin nimeä — sekä alustojen välillä. Käytä
    tätä lähtökohtana ja tarkista asentamasi ajuriversion dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `DBCNAME` | `teradata.example.com` | Palvelimen nimi tai IP-osoite. Teradatan oma nimi isäntäominaisuudelle |
| `UID` | `digna_source_user` | Tietokantakäyttäjä |
| `PWD` | `<password>` | Valitse **Encrypted** |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Hyödyllisiä lisäominaisuuksia:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `MechanismName` | `TD2` | Kirjautumismekanismi. `TD2` on Teradatan oletus; käytä hakemistotodennukseen arvoa `LDAP` |
| `DefaultDatabase` | `dad` | Tietokanta, josta istunto alkaa |
| `CharacterSet` | `UTF8` | Aseta tämä, jos istunnon oletusmerkistö turmelisi muun kuin ASCII-datan |

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Huomioita Teradatasta {: #4-notes-on-teradata }

- **Teradata-tietokanta on katalogi, ei skeema.** *digna* listaa tietokannat, jotka käyttäjä saa
  nähdä (näkymästä `DBC.DatabasesV`), katalogeina, eikä skeemataso ole käytössä. Kun lisäät
  tietolähteen, valitse tietokanta katalogiksi; skeema ilmoitetaan arvolla *not applicable*.
- **Yksi yhteys tavoittaa jokaisen sallitun tietokannan**, joten yksi yhteys voi palvella
  lähteitä useissa tietokannoissa — toisin kuin teknologiat, joissa yhteys on sidottu yhteen
  tietokantaan.
- **Work Schema on tietokanta.** *Permanent*-profilointia varten nimeä Teradata-tietokanta, joka
  sisältää työtaulut, ja anna käyttäjälle siihen `CREATE TABLE` -oikeudet sekä `PERM`-tilan
  varaus — tietokanta, jonka perm-tila on nolla, ei voi sisältää taulua.
- **Profilointitilat.** *Permanent* luo taulut **Work Schemaan**. *Session* käyttää
  `VOLATILE`-taulua, joka tarvitsee `SPOOL`-tilaa mutta ei perm-tilaa eikä oikeuksia
  **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että ajuri ja tunnistetietosi toimivat, ennen kuin syötät ne
*dignaan*.

#### Vaihe 1
![Vaihe 1](images/teradata/create_odbc_data_source_step1.png)

Tämän ikkunan **Name or IP address** -kenttä on [kohdan 2](#2-odbc-properties)
`DBCNAME`-ominaisuus.

Klikkaa **Test**-painiketta.

#### Vaihe 2
![Vaihe 2](images/teradata/create_odbc_data_source_step2.png)

Anna käyttäjätunnus ja salasana ja klikkaa sitten **OK**-painiketta. Onnistumisnäkymä
vahvistaa, että ajuri ja tunnistetiedot toimivat.