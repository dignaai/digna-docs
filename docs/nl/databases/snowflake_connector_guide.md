---
title: Snowflake Connector – Database-integratie | digna Documentatie
description: Stel digna in om verbinding te maken met Snowflake met de Python-connector of de Snowflake ODBC-driver. Ondersteunt wachtwoordgebaseerde authenticatie met DSN- of DSN-less configuraties.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

Deze handleiding beschrijft hoe je *digna* configureert om verbinding te maken met Snowflake met behulp van de native Python-connector of de ODBC-driver.

Dit verwijst naar het scherm **"Create a Database Connection"**.

![Maak een databaseverbinding](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Ondersteunde authenticatie:** Alleen wachtwoordgebaseerde authenticatie

> ⚠️ Voor andere authenticatiemethoden, gebruik de ODBC-driver.

### *digna* Configuratie (Native Driver)

Geef de volgende informatie op in het scherm **"Create a Database Connection"**:

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

De ODBC-driver ondersteunt mogelijk een breder scala aan authenticatie- en connectiviteitsopties. Dit gedeelte richt zich op wachtwoordgebaseerde authenticatie met de **SnowflakeDSIIDriver**.

### 1. Installeer de ODBC-driver

Installeer de **SnowflakeDSIIDriver** door de officiële installatierichtlijn van de leverancier te volgen.

### 2. Configureer de ODBC Data Source

Volg deze stappen om een nieuwe ODBC-data source te configureren met wachtwoordgebaseerde authenticatie:

#### Stap 1
![Stap 1](images/snowflake/create_odbc_data_source_step1.png)

Opmerkingen:
- Als je geen waarden opgeeft voor Database, Schema en Warehouse, moet je deze als ODBC-eigenschappen opgeven tijdens de *digna* data source configuratie.
- De waarde voor "Server" bestaat uit je Snowflake-accountnaam gevolgd door ".snowflakecomputing.com"

#### Stap 2 – Test de verbinding

Klik op de **TEST** knop. Een succesvolle verbinding ziet er als volgt uit:

![Stap 2](images/snowflake/create_odbc_data_source_step2.png)

---

Je kunt nu *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of een **DSN-less** configuratie.

---

### A. DSN-Based Configuratie

#### *digna* Configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> 🔹 De `DSN` moet overeenkomen met de naam die is gedefinieerd in je ODBC-driverconfiguratie.

---

### B. DSN-less Configuratie

#### *digna* Configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```