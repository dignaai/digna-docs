---
title: Snowflake jungtis – Duomenų bazės integracija | digna dokumentacija
description: Konfigūruokite digna prisijungimui prie Snowflake naudojant Python jungtį arba Snowflake ODBC tvarkyklę. Palaikoma autentifikacija su slaptažodžiu naudojant DSN arba be DSN.
image: /assets/logo_square.png
---


# Šaltinio jungtis Snowflake

Šis vadovas aprašo, kaip sukonfigūruoti *digna*, kad prisijungtų prie Snowflake, naudojant arba natyvią Python jungtį, arba ODBC tvarkyklę.

Jame nurodoma ekrano dalis **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natyvi Python tvarkyklė

**Biblioteka:** `snowflake-connector-python`  
**Palaikoma autentifikacija:** Tik autentifikacija su slaptažodžiu

> Jei naudojate kitus autentifikacijos metodus, naudokite ODBC tvarkyklę.

### *digna* konfigūracija (natyvi tvarkyklė)

Pateikite šią informaciją ekrane **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC tvarkyklė

ODBC tvarkyklė gali palaikyti platesnį autentifikacijos ir prisijungimo parinkčių spektrą. Ši dalis yra skirta autentifikacijai su slaptažodžiu naudojant **SnowflakeDSIIDriver**.

### 1. Įdiekite ODBC tvarkyklę

Įdiekite **SnowflakeDSIIDriver** pagal tiekėjo oficialią diegimo instrukciją.

### 2. Konfigūruokite ODBC duomenų šaltinį

Atlikite šiuos veiksmus, kad sukonfigūruotumėte naują ODBC duomenų šaltinį, naudojant autentifikaciją su slaptažodžiu:

#### 1 žingsnis
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Pastabos:
- Jei nepateiksite reikšmių laukams Database, Schema ir Warehouse, tuomet juos turėsite nurodyti kaip ODBC savybes konfigūruodami *digna* duomenų šaltinį.
- Lauko "Server" reikšmė susideda iš jūsų Snowflake paskyros vardo, kuriam pridedama ".snowflakecomputing.com"

#### 2 žingsnis – Išbandyti ryšį

Spustelėkite mygtuką **TEST**. Sėkmingas prisijungimas turėtų atrodyti taip:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Dabar galite sukonfigūruoti *digna* naudoti ODBC ryšį, arba su **DSN (Data Source Name)**, arba be **DSN**.

---

### A. Konfigūracija su DSN

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> `DSN` turi atitikti vardą, nurodytą jūsų ODBC tvarkyklės konfigūracijoje.

---

### B. Konfigūracija be DSN

#### *digna* konfigūracija

Ekrane **"Create a Database Connection"** pateikite šią informaciją:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC savybės

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```