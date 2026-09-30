---
title: Apache Hive -liitin – tietokantaintegraatio | digna-dokumentaatio
description: Määritä digna yhdistämään Apache Hiveen ODBC:n kautta DSN-vapaalla yhteysmerkkijonolla. Kattaa Clouderan Hive-ODBC-ajurin, todennusmekanismit, siirtotilat ja dignan puolen yhteysasetukset.
image: /assets/logo_square.png
---


# Lähdeliitin Hivelle

Tämä ohje kuvaa, miten *digna* määritetään yhdistämään Apache Hiveen **ODBC:n** kautta
**DSN-vapaalla** yhteysmerkkijonolla.

Määrityksen *dignan* puoli on sama jokaiselle teknologialle — missä yhteydet luodaan, miten
ominaisuuksien arvot salataan, miten yhteys testataan ja mitä profilointitilat tarkoittavat.
Se on kuvattu sivulla [Tietokantayhteyksien yleiskatsaus](overview.md). Tämä sivu kattaa sen,
mikä on Hivelle ominaista.

---

## 1. Asenna ODBC-ajuri {: #1-install-the-odbc-driver }

Asenna **Cloudera ODBC Driver for Apache Hive** koneelle, jolla *dignan* backend toimii,
toimittajan virallisen asennusohjeen mukaisesti.

Lue rekisteröidyn ajurin tarkka nimi palvelimeltasi, kuten on kuvattu kohdassa
[Asenna ODBC-ajuri digna-palvelimelle](overview.md#install-the-driver).

---

## 2. ODBC-ominaisuudet {: #2-odbc-properties }

!!! important "Esimerkki, ei määrittely"

    Alla oleva joukko on yksi toimivaksi todettu yhdistelmä. Ominaisuudet kuuluvat Clouderan
    Hive-ajurille, joten niiden nimet, oletusarvot ja hyväksytyt arvot vaihtelevat
    ajuriversioiden ja alustojen välillä, ja se, mitä HiveServer2 hyväksyy, riippuu täysin
    klusterin suojauksesta — todennusmekanismi, siirtotila, TLS, yhdyskäytävä. Käytä tätä
    lähtökohtana ja tarkista asentamasi ajuriversion dokumentaatio.

Lisää seuraavat ominaisuudet **Add DB Connection** -näkymässä:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Täytyy vastata *digna*-palvelimelle rekisteröityä ajurin nimeä |
| `HOST` | `hive.example.com` | HiveServer2:n isäntänimi tai IP-osoite |
| `PORT` | `10000` | HiveServer2:n portti; `10001` HTTP-siirrolle |

Tuloksena oleva yhteysmerkkijono näyttää tältä:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Todennus

Suojaamaton HiveServer2 hyväksyy yllä olevat kolme ominaisuutta sellaisenaan. Jos todennus on
käytössä, lisää:

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `AuthMech` | `3` | `0` ei todennusta, `2` vain käyttäjätunnus, `3` käyttäjätunnus ja salasana, `1` Kerberos |
| `UID` | `digna_source_user` | Pakollinen, kun `AuthMech` on `2` tai `3` |
| `PWD` | `<password>` | Pakollinen, kun `AuthMech` on `3`. Valitse **Encrypted** |

Kerberosta (`AuthMech=1`) varten *digna*-palvelin tarvitsee lisäksi voimassa olevan tiketin tai
keytabin sekä ajurin dokumentoimat ominaisuudet `KrbHostFQDN`, `KrbServiceName` ja `KrbRealm`.

### Siirto ja TLS

| Avain | Esimerkkiarvo | Huomiot |
|---|---|---|
| `ThriftTransport` | `2` | `0` binääri (oletus, portti 10000), `1` SASL, `2` HTTP (portti 10001, ja se, mitä Knox-yhdyskäytävä odottaa) |
| `HTTPPath` | `cliservice` | Kun `ThriftTransport=2` |
| `SSL` | `1` | Kun HiveServer2 on TLS-suojattu |
| `Schema` | `dignadata` | Hive-tietokanta, josta istunto alkaa. Valinnainen — *digna* kirjoittaa kyselyihinsä täydelliset nimet |

---

## 3. *digna*-määritys {: #3-digna-configuration }

Anna **Add DB Connection** -näkymässä seuraavat tiedot:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Huomioita Hivestä {: #4-notes-on-hive }

- **Katalogit tulevat ajurilta.** Hivellä ei ole omaa katalogia, joten *digna* käyttää sitä, mitä
  ajuri ilmoittaa — tavallisesti yhden merkinnän nimeltä `HIVE` — ja listaa Hive-tietokannat
  sen alle skeemoina.
- **Work Schema on Hive-tietokanta.** *Permanent*-profilointia varten käyttäjällä on oltava
  oikeus luoda ja poistaa siinä tauluja, ja taustalla olevan tallennussijainnin on oltava
  kirjoitettavissa.
- **Profilointitilat.** *Permanent* luo työtaulut **Work Schemaan**. *Session* käyttää lausetta
  `CREATE TEMPORARY TABLE`, mikä edellyttää väliaikaisia tauluja tukevaa HiveServer2:ta, eikä
  koske **Work Schemaan**. *Standard* tarvitsee vain lukuoikeuden, ja se on oikea tila
  klusterissa, jossa *dignalla* ei ole lainkaan kirjoitusoikeutta.
- **Profilointi on joukko kyselyjä, ei skannaus.** HiveServer2 laskee jokaisen tilaston, joten
  jonolla, johon *dignan* käyttäjä lähettää kyselyt, on oltava riittävästi kapasiteettia
  inspektioikkunan ajaksi.

---

## 5. Ajurin tarkistaminen (valinnainen) {: #5-verifying-the-driver-optional }

ODBC-tietolähteen määrittäminen ei ole tarpeen DSN-vapaassa yhteydessä, mutta ajurin oma
ikkuna on kätevä tapa varmistaa, että ajuri, siirtotila ja tunnistetietosi toimivat, ennen kuin
syötät ne *dignaan*.

#### Vaihe 1
![Vaihe 1](images/hive/create_odbc_data_source_step1.png)

Tämän ikkunan kentät **Host**, **Port**, **Database**, **Mechanism** ja **Thrift Transport**
ovat [kohdan 2](#2-odbc-properties) ominaisuudet `HOST`, `PORT`, `Schema`, `AuthMech` ja
`ThriftTransport`.

#### Vaihe 2 – Testaa yhteys

Anna salasana ja klikkaa **Test**-painiketta.

![Vaihe 2](images/hive/create_odbc_data_source_step2.png)

Onnistuneen testin jälkeen klikkaa **OK**-painiketta.
