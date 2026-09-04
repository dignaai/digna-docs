---
title: Connettore Databricks (Legacy, senza Unity Catalog) | Documentazione digna
description: Configura digna per connettersi a Databricks senza Unity Catalog usando il connettore Python nativo o il driver ODBC Simba Spark. Supporta l'autenticazione tramite token e connettività flessibile.
image: /assets/logo_square.png
---

# Connettore Sorgente per Databricks - senza Unity Catalog

Questa guida descrive come configurare *digna* per connettersi a Databricks usando il connettore Python nativo oppure il driver ODBC.

Si fa riferimento alla schermata **"Create a Database Connection"**.

![Crea una connessione al database](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Autenticazione supportata:** solo Personal Access Token (PAT)

> Per altri metodi di autenticazione, usare il driver ODBC.

### Personal Access Token (PAT)

Per autenticarsi usando un Personal Access Token, consulta la documentazione ufficiale di Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Fornisci le seguenti informazioni nella schermata **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Questo parametro non è utilizzato per Databricks senza Unity Catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Il driver ODBC supporta una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione tramite token usando il **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Installa il **Simba Spark ODBC Driver** seguendo la guida di installazione ufficiale del fornitore.

### 2. Configure the ODBC Data Source

Segui questi passaggi per configurare una nuova origine dati ODBC usando un Personal Access Token:

#### Passo 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Passo 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Passo 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Passo 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Passo 5 – Test della connessione

Clicca il pulsante **TEST**. Una connessione riuscita dovrebbe apparire così:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Ora puoi configurare *digna* per usare la connessione ODBC, sia con un **DSN (Data Source Name)** sia in modalità **senza DSN**.

---

### A. Configurazione basata su DSN

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornisci quanto segue:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Configurazione senza DSN

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornisci quanto segue:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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