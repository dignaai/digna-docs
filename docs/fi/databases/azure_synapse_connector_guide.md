---
title: Azure Synapse -liitin – tietokantaintegraatio | digna-dokumentaatio
description: Määritä digna yhdistämään Azure Synapse Analyticsiin ODBC:n kautta DSN-vapaalla yhteysmerkkijonolla. Tukee serverless- ja dedicated SQL -pooleja, ja kattaa tarvittavat ODBC-ominaisuudet sekä dignan puolen yhteysasetukset.
image: /assets/logo_square.png
---


# Lähdeliitin Azure Synapse Analyticsille

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Azure Synapse Analyticsiin **ODBC:n**
kautta **DSN-vapaalla** yhteysmerkkijonolla. Sekä serverless- että dedicated SQL -poolit ovat
tuettuja.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Azure Synapselle ominaista.

!!! note "Technology"

    Synapse käyttää SQL Serverin murretta, joten yhteys luodaan valinnalla **Technology:
    SQL Server**. Paikallisen (on-premises) palvelimen osalta katso
    [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **ODBC Driver 18 for SQL Server** koneelle, jolla *dignan* backend toimii,
[Microsoftin asennusohjeen](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server) mukaisesti,
ja lue rekisteröidyn ajurin tarkka nimi palvelimeltasi, kuten on kuvattu kohdassa
[Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat Microsoftin
    ODBC-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden ja alustojen välillä, ja se, mitä työtila (workspace) vaatii, riippuu sen
    määrityksestä — poolin tyyppi, todennustapa, palomuuri. Käytä tätä lähtökohtana ja
    tarkista asentamasi ajuriversion dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Työtilan nimi ja päätepisteen pääte — katso alla |
| `DATABASE` | `dignadata` | Tietokanta, joka sisältää lähdeskeemat. Se on ainoa tietokanta, jota tämä yhteys voi profiloida |
| `UID` | `sqladminuser` | SQL-kirjautuminen |
| `PWD` | `<password>` | Valitse **Encrypted** |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### `SERVER`-arvo

Ota Synapse-työtilan nimi ja lisää siihen päätepisteen pääte:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "`-ondemand`-osa jää helposti huomaamatta"

    Ilman sitä nimi ohjautuu dedicated-päätepisteeseen, ja yhteys joko epäonnistuu tai päätyy
    huomaamatta eri pooliin kuin oli tarkoitus. Molemmat päätepisteet näkyvät Azure-portaalin
    työtilan yleiskatsaussivulla.

### Palomuuri

Synapse-työtilan palomuurin on sallittava *digna*-palvelimen lähtevä osoite. Lisää se
työtilan kohdassa **Networking** ennen yhteyden testaamista — estetty osoite näkyy yhteyden
aikakatkaisuna eikä todennusvirheenä.

### Microsoft Entra ID -todennus

SQL-kirjautumisen sijaan ajuri voi todentaa Entra ID:tä vasten. Korvaa `UID`/`PWD` sillä
todennustavalla, jota työtilasi odottaa, esimerkiksi:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` saa tällöin sovelluksen (client) ID:n ja `PWD` client secretin |
| `Authentication` | `ActiveDirectoryMSI` | *digna*-palvelimen hallittu identiteetti (managed identity), tunnistetietoja ei tarvita |

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Huomioita Azure Synapsesta {: #4-notes-on-azure-synapse }

- **Serverless-poolit tukevat vain *Standard*-profilointia.** Serverless SQL pool ei voi luoda
  tauluja tietokantaan, joten *Permanent*- tai *Session*-profilointia ei voi ajaa. *Standard*
  laskee metriikat suoraan lähteestä, mikä on myös edullisempi vaihtoehto, koska serverless
  laskutetaan käsitellyn datan mukaan.
- **Yksi yhteys näkee yhden tietokannan.** *digna* tarjoaa `DATABASE`-ominaisuudessa nimetyn
  tietokannan skeemat, koska Synapse, kuten SQL Server, ilmoittaa katalogiksi vain nykyisen
  tietokannan.
- **Salaus on oletuksena käytössä** Driver 18:ssa, ja Synapse-päätepisteet esittävät voimassa
  olevat julkiset varmenteet, joten `Encrypt`- tai `TrustServerCertificate`-ominaisuutta ei
  tarvita.
- **Serverless-päätepiste saattaa herätä lepotilasta** ensimmäisellä yhteydellä. Jos
  yhteystesti aikakatkaistaan poolissa, jota ei ole käytetty vähään aikaan, yritä uudelleen.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ohjattu toiminto on kätevä tapa varmistaa, että ajuri toimii ja että työtila hyväksyy
tunnistetietosi, ennen kuin syötät ne *dignaan*.

#### Vaihe 1
![Vaihe 1](images/azure_synapse/create_odbc_data_source_step1.png)

Täytä "Server"-kenttä.
Käytä Synapse-työtilan nimeä ja lisää sen perään ".sql.azuresynapse.net".  
**Huomio**: jos haluat yhdistää serverless SQL poolin kautta, muista lisätä
"-ondemand" yllä olevan kuvakaappauksen mukaisesti.

Klikkaa **Next >** -painiketta.

#### Vaihe 2
![Vaihe 2](images/azure_synapse/create_odbc_data_source_step2.png)

Valitse todennustapa (esim. käyttäjätunnus ja salasana)
ja anna tarvittavat tiedot.

Klikkaa **Next >** -painiketta.

#### Vaihe 3
![Vaihe 3](images/azure_synapse/create_odbc_data_source_step3.png)

Valitse ANSI-yhteensopivat asetukset ja klikkaa sitten **Next >** -painiketta.

#### Vaihe 4
![Vaihe 4](images/azure_synapse/create_odbc_data_source_step4.png)

Voit jättää oletusasetukset tai valita asetukset tarpeen mukaan
ja klikata **Finish**-painiketta.

#### Vaihe 5
![Vaihe 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klikkaa nyt **Test datasource** -painiketta.

#### Vaihe 6
![Vaihe 6](images/azure_synapse/create_odbc_data_source_step6.png)

Onnistumisnäkymä vahvistaa, että ajuri, päätepiste ja tunnistetiedot toimivat. Syöttämäsi
arvot ovat täsmälleen ne arvot, jotka [kohdan 2](#2-odbc-properties) ominaisuudet saavat.
