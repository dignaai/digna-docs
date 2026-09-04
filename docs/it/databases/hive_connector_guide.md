---
title: Apache Hive Connector – Integrazione Database | Documentazione digna
description: Configura digna per connettersi ad Apache Hive usando il driver Python nativo PyHive o il driver ODBC di Cloudera. Supporta l'autenticazione basata su password e configurazioni con DSN o senza DSN.
image: /assets/logo_square.png
---


# Connettore sorgente per Hive

Questa guida descrive come configurare *digna* per connettersi a Hive usando il connettore Python nativo o il driver ODBC.

Si riferisce alla schermata **"Crea una connessione al database"**.

![Crea una connessione al database](images/data_source_config_input_mask.png)

---

## Driver Python nativo

**Library:** `PyHive`  
**Autenticazione supportata:** Solo autenticazione basata su password

> Per altri metodi di autenticazione, utilizzare il driver ODBC.

### Configurazione di *digna* (Driver nativo)

Fornire le seguenti informazioni nella schermata **"Crea una connessione al database"**:

```
Technology:      Apache Hive
Host Address:    Nome server o indirizzo IP
Host Port:       Numero di porta, es. 10000
Database Name:   Schema che contiene i dati di origine
Schema Name:     Schema che contiene i dati di origine
User Name:       Nome utente del database
User Password:   Password dell'utente
Use ODBC:        Disabilitato (predefinito)
```

---

## Driver ODBC

Il driver ODBC può supportare una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione basata su password usando il driver **Cloudera ODBC Driver for Apache Hive**.

### 1. Installare il driver ODBC

Installare il **Cloudera ODBC Driver for Apache Hive** (o simile) seguendo la guida di installazione ufficiale del vendor.

### 2. Configurare la sorgente dati ODBC

Seguire questi passaggi per configurare una nuova sorgente dati ODBC utilizzando l'autenticazione basata su password:

#### Passaggio 1
![Passaggio 1](images/hive/create_odbc_data_source_step1.png)


#### Passaggio 2 – Test della connessione

Inserire la password e cliccare il pulsante **Test**.

![Passaggio 2](images/hive/create_odbc_data_source_step2.png)

Dopo un test riuscito, cliccare il pulsante **OK**.

---

Ora puoi configurare *digna* per usare la connessione ODBC, oppure con una configurazione **DSN (Data Source Name)** o **senza DSN**.

---

### A. Configurazione basata su DSN

#### Configurazione di *digna*

Nella schermata **"Crea una connessione al database"**, fornire quanto segue:

```
Technology:      Apache Hive
Database Name:   Schema che contiene i dati di origine (uguale a Schema Name)
Schema Name:     Schema che contiene i dati di origine
Use ODBC:        Abilitato
```

#### Proprietà ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{la tua password tra parentesi graffe}"
```

> Il `DSN` deve corrispondere al nome definito nella configurazione del tuo driver ODBC.

---

### B. Configurazione senza DSN

#### Configurazione di *digna*

Nella schermata **"Crea una connessione al database"**, fornire quanto segue:

```
Technology:      Apache Hive
Database Name:   Schema che contiene i dati di origine (uguale a Schema Name)
Schema Name:     Schema che contiene i dati di origine
Use ODBC:        Abilitato
```

#### Proprietà ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "il tuo nome server o indirizzo IP"
name: "PORT",       value: "Numero di porta, es. 10000"
name: "Schema",     value: "Schema che contiene i dati di origine"
name: "UID",        value: "il tuo utente Hive'
name: "PWD",        value: "la tua password Hive"
name: "AuthMech",   value: "3"
```