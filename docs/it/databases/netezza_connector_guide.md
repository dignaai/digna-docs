---
title: Connettore Netezza – Integrazione Database | Documentazione digna
description: Configura digna per connettersi a Netezza usando il driver ODBC NetezzaSQL. Supporta l'autenticazione tramite password con configurazioni DSN o DSN-less per una connettività flessibile.
image: /assets/logo_square.png
---


# Connettore sorgente per Netezza

Questa guida descrive come configurare *digna* per connettersi a Netezza usando il driver ODBC.

Si riferisce alla schermata **"Create a Database Connection"**.

![Creare una connessione al database](images/data_source_config_input_mask.png)

---

## ODBC Driver

Il driver ODBC può supportare diverse opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione tramite password usando il driver **NetezzaSQL**.

### 1. Installare il driver ODBC

Installa il driver **NetezzaSQL** (o analogo) seguendo la guida di installazione ufficiale del fornitore.

### 2. Configurare la sorgente dati ODBC

Segui questi passaggi per configurare una nuova sorgente dati ODBC utilizzando l'autenticazione basata su password:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

A seconda del tuo driver Netezza, delle impostazioni e dei requisiti di sicurezza, potrebbe essere necessario fornire dati anche nelle schede **Advanced DSN Options**, **SSL DSN Options** o **Driver Options**. Per la configurazione più semplice è sufficiente inserire i dati in **DSN Options**.

Fai clic sul pulsante **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Quando compare la schermata di successo, ODBC è configurato correttamente.

---

Ora puoi configurare *digna* per usare la connessione ODBC, sia con una configurazione basata su **DSN (Data Source Name)** sia in modalità **DSN-less**.

---

### A. Configurazione basata su DSN

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornisci quanto segue:

```
Technology:      Netezza
Database Name:   Database che contiene lo schema di origine
Schema Name:     Schema che contiene i dati di origine
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 Il `DSN` deve corrispondere al nome definito nella configurazione del driver ODBC.

---

### B. Configurazione DSN-less

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornisci quanto segue:

```
Technology:      Netezza
Database Name:   Schema che contiene i dati di origine (uguale a Schema Name)
Schema Name:     Schema che contiene i dati di origine
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```