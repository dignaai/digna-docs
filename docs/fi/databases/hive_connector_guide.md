---
title: Apache Hive -liitin – tietokantaintegraatio | digna-dokumentaatio
description: Konfiguroi digna yhdistämään Apache Hiveen natiivin PyHive-ajurin tai Cloudera ODBC -ajurin avulla. Tukee salasanaan perustuvaa todennusta sekä DSN- ja DSN-vapaita (DSN-less) asetuksia.
image: /assets/logo_square.png
---


# Lähdeyhdistin Hive:lle

Tässä ohjeessa kerrotaan, miten *digna* konfiguroidaan yhdistämään Hiveen joko natiivin Python-yhteysohjaimen tai ODBC-ajurin kautta.

Ohje viittaa näyttöön **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natiivi Python-ajuri

**Kirjasto:** `PyHive`  
**Tuettu todennus:** Vain salasanaan perustuva todennus

> Muita todennusmenetelmiä varten käytä ODBC-ajuria.

### *digna* -konfiguraatio (natiivi ajuri)

Anna seuraavat tiedot **"Create a Database Connection"** -näytöllä:

```
Technology:      Apache Hive
Host Address:    Palvelimen nimi tai IP-osoite
Host Port:       Porttinumero, esim. 10000
Database Name:   Skeema, joka sisältää lähdetiedot
Schema Name:     Skeema, joka sisältää lähdetiedot
User Name:       Tietokannan käyttäjänimi
User Password:   Käyttäjän salasana
Use ODBC:        Disabled (oletus)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tässä osiossa keskitytään salasanaan perustuvaan todennukseen käyttäen **Cloudera ODBC Driver for Apache Hive** -ajuria.

### 1. Asenna ODBC-ajuri

Asenna **Cloudera ODBC Driver for Apache Hive** (tai vastaava) seuraamalla toimittajan virallista asennusopasta.

### 2. Konfiguroi ODBC-datalähde

Noudata näitä vaiheita määrittääksesi uuden ODBC-datalähteen käyttäen salasanaan perustuvaa todennusta:

#### Vaihe 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Vaihe 2 – Testaa yhteys

Syötä salasana ja napsauta **Testaa**-painiketta.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Onnistuneen testin jälkeen klikkaa **OK**-painiketta.

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -pohjaisesti tai **DSN-vapaalla** asetuksella.

---

### A. DSN-pohjainen konfiguraatio

#### *digna* -konfiguraatio

Anna **"Create a Database Connection"** -näytöllä seuraavat tiedot:

```
Technology:      Apache Hive
Database Name:   Skeema, joka sisältää lähdetiedot (sama kuin Schema Name)
Schema Name:     Skeema, joka sisältää lähdetiedot
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` on oltava sama kuin ODBC-ajurikonfiguraatiossasi määritelty nimi.

---

### B. DSN-vapaa konfiguraatio

#### *digna* -konfiguraatio

Anna **"Create a Database Connection"** -näytöllä seuraavat tiedot:

```
Technology:      Apache Hive
Database Name:   Skeema, joka sisältää lähdetiedot (sama kuin Schema Name)
Schema Name:     Skeema, joka sisältää lähdetiedot
Use ODBC:        Enabled
```

#### ODBC-ominaisuudet

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "palvelimesi nimi tai IP-osoite"
name: "PORT",       value: "Porttinumero, esim. 10000"
name: "Schema",     value: "Skeema, joka sisältää lähdetiedot"
name: "UID",        value: "hive-käyttäjänimesi"
name: "PWD",        value: "hive-salasanasi"
name: "AuthMech",   value: "3"
```