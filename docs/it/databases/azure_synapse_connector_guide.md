---
title: Connettore Azure Synapse – Integrazione Database | Documentazione digna
description: Configura digna per connettersi ad Azure Synapse Analytics utilizzando il driver Python nativo o il driver ODBC. Supporta pool SQL serverless e dedicati.
image: /assets/logo_square.png
---


# Connettore sorgente per Azure Synapse Analytics

Questa guida descrive come configurare *digna* per connettersi ad Azure Synapse Analytics utilizzando il connettore Python nativo oppure il driver ODBC.
Supporta sia i pool SQL serverless che quelli dedicati.

Si riferisce alla schermata **"Create a Database Connection"**.

![Crea una connessione al database](images/data_source_config_input_mask.png)

---

## Driver Python nativo

**Library:** `pymssql`  
**Autenticazione supportata:** Solo autenticazione tramite password

> Per altri metodi di autenticazione, usa il driver ODBC.

### Configurazione di *digna* (Driver nativo)

Fornisci le seguenti informazioni nella schermata **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Driver ODBC

Il driver ODBC può supportare una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione tramite password usando il driver **ODBC Driver 18 for SQL Server**.

### 1. Installa il driver ODBC

Installa il driver **ODBC Driver 18 for SQL Server** (o simili) seguendo la guida di installazione ufficiale del fornitore.

### 2. Configura la sorgente dati ODBC

Segui questi passaggi per configurare una nuova sorgente dati ODBC usando l'autenticazione tramite password:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Compila il campo "Server".
Usa il nome del workspace Synapse e aggiungi ".sql.azuresynapse.net".  
**Attenzione**, se desideri connetterti usando un pool SQL serverless, assicurati di includere "-ondemand" come mostrato nello screenshot qui sotto.

Fai clic sul pulsante **Next >**.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Scegli il metodo di autenticazione (es. username e password)
e fornisci i dati richiesti.

Fai clic sul pulsante **Next >**.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Scegli le impostazioni compatibili ANSI poi fai clic sul pulsante **Next >**.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Puoi lasciare le impostazioni predefinite o scegliere le opzioni necessarie 
e fare clic sul pulsante **Finish**. 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Ora fai clic sul pulsante ** Test datasource **.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Quando compare la schermata di successo, ODBC è configurato correttamente.

---

Ora puoi configurare *digna* per utilizzare la connessione ODBC, sia con una **DSN (Data Source Name)** sia con una configurazione **senza DSN**.

---

### A. Configurazione basata su DSN

#### Configurazione di *digna*

Nella schermata **"Create a Database Connection"**, fornisci quanto segue:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Proprietà ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Configurazione senza DSN

#### Configurazione di *digna*

Nella schermata **"Create a Database Connection"**, fornisci quanto segue:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Proprietà ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Nota** riguardo alla proprietà SERVER:  
Usa il nome del workspace Synapse e aggiungi ".sql.azuresynapse.net". Se vuoi connetterti usando un pool SQL serverless, assicurati di includere "-ondemand" come mostrato nello screenshot qui sotto.