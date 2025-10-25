---
title: Snowflake Connector – Integracija baze podatkov | digna-dokumentacija
description: Konfigurirajte digna za povezavo s Snowflake z uporabo Python-connectorja ali Snowflake ODBC gonilnika. Podpira preverjanje pristnosti z geslom z DSN ali DSN-brez nastavitve.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo s Snowflake z uporabo bodisi izvornega Python-connectorja bodisi ODBC-gonilnika.

Sklicuje se na zaslon **"Create a Database Connection"**.

![Opprett en databaseforbindelse](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Podprto preverjanje pristnosti:** Samo preverjanje pristnosti z geslom

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC-gonilnik.

### *digna*-konfiguracija (native driver)

Na zaslonu **"Create a Database Connection"** vnesite naslednje podatke:

```
Teknologija:      Snowflake
Naslov gostitelja: Ime Snowflake računa
Vrata gostitelja:  Ni potrebno
Ime baze podatkov: Baza, ki vsebuje izvorno shemo
Schema Name:      Shema, ki vsebuje izvorne podatke
Uporabniško ime:  Uporabnik in warehouse v obliki "user<@>warehouse"
Uporabniško geslo: Geslo za uporabnika
Uporabi ODBC:      Onemogočeno (privzeto)
```

---

## ODBC Driver

ODBC-gonilnik lahko podpira širši nabor metod preverjanja pristnosti in možnosti povezave. Ta razdelek se osredotoča na preverjanje pristnosti z geslom z uporabo **SnowflakeDSIIDriver**.

### 1. Namestite ODBC-gonilnik

Namestite **SnowflakeDSIIDriver** tako, da sledite uradnim navodilom dobavitelja.

### 2. Konfigurirajte ODBC-datoteko vira

Sledite tem korakom za konfiguracijo nove ODBC-datoteke vira z uporabo preverjanja pristnosti z geslom:

#### Korak 1
![Trinn 1](images/snowflake/create_odbc_data_source_step1.png)

Opombe:
- Če ne vnesete vrednosti za Database, Schema in Warehouse, jih morate navesti kot ODBC-lastnosti v konfiguraciji podatkovnega vira v *digna*.
- Vrednost za "Server" je vaše ime Snowflake računa, za katerim sledi ".snowflakecomputing.com"

#### Korak 2 – Testirajte povezavo

Kliknite na gumb **TEST**. Uspešna povezava bi morala izgledati takole:

![Trinn 2](images/snowflake/create_odbc_data_source_step2.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-brez** nastavitvijo.

---

### A. Konfiguracija na podlagi DSN

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Teknologija:        Snowflake
Ime baze podatkov:  Baza, ki vsebuje izvorno shemo
Schema Name:        Shema, ki vsebuje izvorne podatke
Uporabi ODBC:       Omogočeno
```

#### ODBC-lastnosti

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{vaše geslo v zavitih oklepajih}"

neobvezno:
name: "Database",       value: "Baza, ki vsebuje izvorno shemo"
name: "Schema",         value: "Shema, ki vsebuje izvorne podatke"
name: "Warehouse",      value: "Warehouse, ki naj se uporablja za izvajanje SQL-ov"
```

> 🔹 `DSN` se mora ujemati z imenom, ki je definirano v konfiguraciji vašega ODBC-gonilnika.

---

### B. Konfiguracija brez DSN

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Teknologija:        Snowflake
Ime baze podatkov:   Shema, ki vsebuje izvorne podatke (enako kot Schema Name)
Schema Name:         Shema, ki vsebuje izvorne podatke
Uporabi ODBC:        Omogočeno
```

#### ODBC-lastnosti

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com"
name: "UID",        value: "vaš Snowflake-uporabnik"
name: "PWD",        value: "vaše Snowflake-geslo"
name: "Database",   value: "Baza, ki vsebuje izvorno shemo"
name: "Schema",     value: "Shema, ki vsebuje izvorne podatke"
name: "Warehouse",  value: "Warehouse, ki naj se uporablja za izvajanje SQL-ov"
```