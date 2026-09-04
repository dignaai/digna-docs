---
title: Snowflake-liitin – Tietokantaintegraatio | digna-dokumentaatio
description: Määritä digna yhdistymään Snowflakeen Python-liittimen tai Snowflake ODBC -ajurin avulla. Tukee salasanapohjaista todennusta DSN- tai DSN-vapaissa kokoonpanoissa.
image: /assets/logo_square.png
---


# Lähdeyhteys Snowflakeen

Tässä ohjeessa kuvataan, miten *digna* konfiguroidaan yhdistämään Snowflakeen joko natiivin Python-liittimen tai ODBC-ajurin avulla.

Ohje viittaa näyttöön **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natiivinen Python-ajuri

**Kirjasto:** `snowflake-connector-python`  
**Tuettu todennus:** Vain salasanapohjainen todennus

> Muille todennusmenetelmille käytä ODBC-ajuria.

### *digna*-kokoonpano (natiivinen ajuri)

Anna seuraavat tiedot **"Create a Database Connection"** -näytössä:

```
Technology:      Snowflake
Host Address:    Snowflake-tilin nimi
Host Port:       Ei tarvita
Database Name:   Tietokanta, joka sisältää lähdeskeeman
Schema Name:     Skeema, joka sisältää lähdetiedot
User Name:       Käyttäjänimi ja warehouse muodossa "user<@>warehouse"
User Password:   Käyttäjän salasana
Use ODBC:        Pois käytöstä (oletus)
```

---

## ODBC-ajuri

ODBC-ajuri voi tukea laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tämä osio keskittyy salasanapohjaiseen todennukseen käyttäen **SnowflakeDSIIDriver**-ajuria.

### 1. Asenna ODBC-ajuri

Asenna **SnowflakeDSIIDriver** seuraamalla toimittajan virallista asennusohjetta.

### 2. Konfiguroi ODBC-tietolähde

Toimi seuraavasti konfiguroidaksesi uuden ODBC-tietolähteen käyttäen salasanapohjaista todennusta:

#### Vaihe 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Huom:
- Jos et täytä Database-, Schema- ja Warehouse-kenttiä, sinun täytyy antaa ne ODBC-ominaisuuksina *digna*-tietolähteen konfiguroinnin aikana.
- "Server"-kentän arvo muodostuu Snowflake-tilisi nimestä, johon lisätään ".snowflakecomputing.com"

#### Vaihe 2 – Testaa yhteys

Klikkaa **TEST**-painiketta. Onnistunut yhteys näyttää tältä:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -asetuksella tai **DSN-vapaalla** kokoonpanolla.

---

### A. DSN-pohjainen kokoonpano

#### *digna*-kokoonpano

Anna seuraavat tiedot **"Create a Database Connection"** -näytössä:

```
Technology:      Snowflake
Database Name:   Tietokanta, joka sisältää lähdeskeeman
Schema Name:     Skeema, joka sisältää lähdetiedot
Use ODBC:        Käytössä
```

#### ODBC-ominaisuudet

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{salasanasi aaltosulkeissa}"

valinnaisesti:
name: "Database",       value: "Tietokanta, joka sisältää lähdeskeeman"
name: "Schema",         value: "Skeema, joka sisältää lähdetiedot"
name: "Warehouse",      value: "Warehouse, jota käytetään SQL-lauseiden suorittamiseen"
```

> `DSN`-arvon on oltava sama kuin ODBC-ajurin konfiguroinnissa määritelty nimi.

---

### B. DSN-vapaa kokoonpano

#### *digna*-kokoonpano

Anna seuraavat tiedot **"Create a Database Connection"** -näytössä:

```
Technology:      Snowflake
Database Name:   Skeema, joka sisältää lähdetiedot (sama kuin Schema Name)
Schema Name:     Skeema, joka sisältää lähdetiedot
Use ODBC:        Käytössä
```

#### ODBC-ominaisuudet

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "tilisi-nimi.snowflakecomputing.com"
name: "UID",        value: "Snowflake-käyttäjäsi"
name: "PWD",        value: "Snowflake-salasanasi"
name: "Database",   value: "Tietokanta, joka sisältää lähdeskeeman"
name: "Schema",     value: "Skeema, joka sisältää lähdetiedot"
name: "Warehouse",  value: "Warehouse, jota käytetään SQL-lauseiden suorittamiseen"
```