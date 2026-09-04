---
title: Connettore Databricks con Unity Catalog – Integrazione Database | documentazione digna
description: Configura digna per connettersi a Databricks con Unity Catalog usando il connector nativo Python o il driver ODBC. Supporta autenticazione basata su token e connettività flessibile.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Questa guida descrive come configurare *digna* per connettersi a Databricks usando il connector nativo Python oppure il driver ODBC.

Si fa riferimento alla schermata **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Per altri metodi di autenticazione, utilizzare il driver ODBC.

### Personal Access Token (PAT)

Per autenticarsi usando un personal access token, consultare la documentazione ufficiale di Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Fornire le seguenti informazioni nella schermata **"Create a Database Connection"**:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Il driver ODBC supporta un insieme più ampio di opzioni di autenticazione e connettività. Questa sezione è focalizzata sull'autenticazione basata su token usando il **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Installare il **Simba Spark ODBC Driver** seguendo la guida di installazione ufficiale del fornitore.

### 2. Configure the ODBC Data Source

Seguire questi passaggi per configurare una nuova data source ODBC usando un Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Cliccare il pulsante **TEST**. Una connessione riuscita dovrebbe apparire così:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Ora è possibile configurare *digna* per utilizzare la connessione ODBC, sia con una configurazione **DSN (Data Source Name)** sia in modalità **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire quanto segue:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> Il `DSN` deve corrispondere al nome definito nella configurazione del driver ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire quanto segue:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```