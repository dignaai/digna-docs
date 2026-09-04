---
title: Connettore PostgreSQL – Integrazione Database | Documentazione digna
description: Configura digna per connettersi a PostgreSQL utilizzando il driver Python psycopg o il driver ODBC di PostgreSQL. Supporta l'autenticazione basata su password con configurazioni DSN o senza DSN.
image: /assets/logo_square.png
---


# Source Connector for PostgreSQL

Questa guida descrive come configurare *digna* per connettersi a Postgres utilizzando il connettore Python nativo o il driver ODBC.

Si riferisce alla schermata **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Solo autenticazione basata su password

> Per altri metodi di autenticazione, utilizzare il driver ODBC.

### *digna* Configuration (Native Driver)

Fornire le seguenti informazioni nella schermata **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Nome del server o indirizzo IP
Host Port:       Numero di porta, es. 5432
Database Name:   Nome del database
Schema Name:     Schema che contiene i dati sorgente
User Name:       Nome utente del database
User Password:   Password dell'utente
Use ODBC:        Disabilitato (predefinito)
```

---

## ODBC Driver

Il driver ODBC può supportare una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione basata su password utilizzando il driver **PostgreSQL Unicode(x64)**.

### 1. Installare il driver ODBC

Installare **PostgreSQL Unicode(x64)** (o simile) seguendo la guida di installazione ufficiale del fornitore.

### 2. Configurare la sorgente dati ODBC

Seguire questi passaggi per configurare una nuova sorgente dati ODBC utilizzando l'autenticazione basata su password:

#### Passo 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Nota: Se la configurazione del database richiede di scegliere un "SSLMode" specifico, assicurarsi di usare lo stesso valore anche quando si definisce una configurazione senza DSN.

#### Passo 2 – Test della connessione

Fare clic sul pulsante **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Ora è possibile configurare *digna* per utilizzare la connessione ODBC, sia con una configurazione **DSN (Data Source Name)** sia una configurazione **senza DSN**.

---

### A. Configurazione basata su DSN

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire quanto segue:

```
Technology:      PostgreSQL
Database Name:   Database che contiene lo schema sorgente
Schema Name:     Schema che contiene i dati sorgente
Use ODBC:        Abilitato
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> Il `DSN` deve corrispondere al nome definito nella configurazione del driver ODBC.

---

### B. Configurazione senza DSN

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire quanto segue:

```
Technology:      PostgreSQL
Database Name:   Schema che contiene i dati sorgente (stesso valore di Schema Name)
Schema Name:     Schema che contiene i dati sorgente
Use ODBC:        Abilitato
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "nome del tuo server o indirizzo IP"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres o altro nome del tuo database"
name: "UID",        value: "il tuo utente postgres"
name: "PWD",        value: "la tua password postgres"
name: "SSLMode",    value: "require"
```