---
title: Snowflake Connector – Integrazione del Database | digna Documentation
description: Configura digna per connettersi a Snowflake usando il connettore Python o il driver ODBC di Snowflake. Supporta l'autenticazione tramite password con configurazioni DSN o senza DSN.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

Questa guida descrive come configurare *digna* per connettersi a Snowflake usando il connettore Python nativo o il driver ODBC.

Si fa riferimento alla schermata **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Supported Authentication:** solo autenticazione basata su password

> Per altri metodi di autenticazione, usare il driver ODBC.

### *digna* Configuration (Native Driver)

Fornire le seguenti informazioni nella schermata **"Create a Database Connection"**:

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

Il driver ODBC può supportare una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione tramite password usando il **SnowflakeDSIIDriver**.

### 1. Install the ODBC Driver

Installa il **SnowflakeDSIIDriver** seguendo la guida di installazione ufficiale del fornitore.

### 2. Configure the ODBC Data Source

Segui questi passaggi per configurare una nuova sorgente dati ODBC utilizzando l'autenticazione basata su password:

#### Step 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Note:
- Se non fornisci valori per Database, Schema e Warehouse, dovrai fornirli come proprietà ODBC durante la configurazione della sorgente dati in *digna*.
- Il valore per "Server" è costituito dal nome del tuo account Snowflake seguito da ".snowflakecomputing.com"

#### Step 2 – Test the connection

Clicca il pulsante **TEST**. Una connessione riuscita dovrebbe apparire così:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Ora puoi configurare *digna* per usare la connessione ODBC, sia con una configurazione **DSN (Data Source Name)** sia con una configurazione **senza DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire quanto segue:

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

> Il valore `DSN` deve corrispondere al nome definito nella configurazione del tuo driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire quanto segue:

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