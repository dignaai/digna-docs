---
title: Snowflake Connector – Database Integration | digna Documentation
description: Konfigurer digna til at oprette forbindelse til Snowflake ved hjælp af Python-connectoren eller Snowflake ODBC-driveren. Understøtter adgangskodebaseret godkendelse med DSN eller DSN-less opsætninger.
image: /assets/logo_square.png
---


# Kildeconnector for Snowflake

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Snowflake ved enten at bruge den native Python-connector eller ODBC-driveren.

Den henviser til skærmen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Supported Authentication:** Kun adgangskodebaseret godkendelse

> For andre godkendelsesmetoder, brug venligst ODBC-driveren.

### *digna* Konfiguration (Native Driver)

Angiv følgende oplysninger i skærmen **"Create a Database Connection"**:

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

## ODBC Driver

ODBC-driveren kan understøtte et bredere udvalg af godkendelses- og forbindelsesmuligheder. Dette afsnit fokuserer på adgangskodebaseret godkendelse ved brug af **SnowflakeDSIIDriver**.

### 1. Installer ODBC-driveren

Installer **SnowflakeDSIIDriver** ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved brug af adgangskodebaseret godkendelse:

#### Trin 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Bemærk:
- Hvis du ikke angiver værdier for Database, Schema og Warehouse, skal du angive dem som ODBC-egenskaber under *digna*-datakildekonfigurationen.
- Værdien for "Server" består af dit Snowflake-kontonavn efterfulgt af ".snowflakecomputing.com"

#### Trin 2 – Test forbindelsen

Klik på **TEST**-knappen. En vellykket forbindelse bør se sådan ud:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* Konfiguration

I skærmen **"Create a Database Connection"** angiver du følgende:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaber

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> `DSN` skal matche navnet, der er defineret i din ODBC-driverkonfiguration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

I skærmen **"Create a Database Connection"** angiver du følgende:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaber

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```