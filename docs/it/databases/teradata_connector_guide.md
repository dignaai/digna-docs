---
title: Connettore Teradata – Integrazione Database | Documentazione digna
description: Configura digna per connettersi a Teradata usando il driver Python teradatasql o il driver ODBC di Teradata. Supporta l'autenticazione tramite password con configurazioni DSN o senza DSN.
image: /assets/logo_square.png
---


# Connettore sorgente per Teradata

Questa guida descrive come configurare *digna* per connettersi a Teradata usando il connettore Python nativo o il driver ODBC.

Si fa riferimento alla schermata **"Crea una connessione al database"**.

![Crea una connessione al database](images/data_source_config_input_mask.png)

---

## Driver Python nativo

**Library:** `teradatasql`  
**Autenticazione supportata:** Solo autenticazione tramite password

> Per altri metodi di autenticazione, utilizza il driver ODBC.

### Configurazione di *digna* (Driver nativo)

Fornisci le seguenti informazioni nella schermata **"Crea una connessione al database"**:

```
Tecnologia:       Teradata
Indirizzo host:   Nome del server o indirizzo IP
Porta host:       Numero di porta, es. 1025
Nome database:    Nome del database
Nome schema:      Nome del database
Nome utente:      Nome utente del database
Password utente:  Password per l'utente
Usa ODBC:         Disabilitato (predefinito)
```

---

## Driver ODBC

Il driver ODBC può supportare un’ampia gamma di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione tramite password usando il driver **Teradata Database ODBC Driver 20.00**.

### 1. Installa il driver ODBC

Installa il driver **Teradata Database ODBC Driver 20.00** (o simile) seguendo la guida di installazione ufficiale del fornitore.

### 2. Configura la sorgente dati ODBC

Segui questi passaggi per configurare una nuova sorgente dati ODBC utilizzando l'autenticazione tramite password:

#### Passaggio 1
![Passaggio 1](images/teradata/create_odbc_data_source_step1.png)

Clicca il pulsante **Test**.

#### Passaggio 2
![Passaggio 2](images/teradata/create_odbc_data_source_step2.png)

Inserisci nome utente e password.

Clicca il pulsante **OK**.  
Quando viene visualizzata la schermata di successo, l'ODBC è configurato correttamente.

---

Ora puoi configurare *digna* per usare la connessione ODBC, sia con una configurazione **DSN (Data Source Name)** sia senza **DSN-less**.

---

### A. Configurazione basata su DSN

#### Configurazione *digna*

Nella schermata **"Crea una connessione al database"**, fornisci quanto segue:

```
Tecnologia:       Teradata
Nome database:    Database che contiene lo schema sorgente
Nome schema:      Schema che contiene i dati sorgente
Usa ODBC:         Abilitato
```

#### Proprietà ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "il tuo utente del database"
name: "PWD",        value: "la tua password del database"
```

> Il `DSN` deve corrispondere al nome definito nella configurazione del tuo driver ODBC.

---

### B. Configurazione senza DSN

#### Configurazione *digna*

Nella schermata **"Crea una connessione al database"**, fornisci quanto segue:

```
Tecnologia:       Teradata
Nome database:    Schema che contiene i dati sorgente (uguale a Nome schema)
Nome schema:      Schema che contiene i dati sorgente
Usa ODBC:         Abilitato
```

#### Proprietà ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "il nome del tuo server o indirizzo IP"
name: "UID",        value: "il tuo utente del database"
name: "PWD",        value: "la tua password del database"
```