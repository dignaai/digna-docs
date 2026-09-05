# Connettore sorgente per Oracle

Questa guida descrive come configurare *digna* per connettersi a Oracle DB usando il connettore nativo Python o il driver ODBC.

Si riferisce alla schermata **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver Python nativo

**Libreria:** `python-oracledb`  
**Autenticazione supportata:** Solo autenticazione basata su password

> Per altri metodi di autenticazione, utilizzare il driver ODBC.

### Configurazione *digna* (Driver nativo)

Inserire le seguenti informazioni nella schermata **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Nome server o indirizzo IP
Host Port:       Numero di porta, es. 1521
Database Name:   Nome dell'istanza, nome del servizio
Schema Name:     Schema che contiene i dati di origine
User Name:       Nome utente del database
User Password:   Password per l'utente
Use ODBC:        Disabilitato (predefinito)
```

---

## Driver ODBC

Il driver ODBC può supportare una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione basata su password usando il driver **Oracle in OraDB21Home1**.

### 1. Installa il driver ODBC

Installa **Oracle in OraDB21Home1** (o simile) seguendo la guida ufficiale di installazione del fornitore.

### 2. Configura la sorgente dati ODBC

Segui questi passaggi per configurare una nuova sorgente dati ODBC usando l'autenticazione basata su password:

#### Passo 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Nota:
Il TNS Service Name deve essere configurato nel file tnsnames.ora della tua installazione del client Oracle. Qui è dove fornisci il descrittore di connessione (host, porta, service name).

#### Passo 2 – Test della connessione

Clicca sul pulsante **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Inserisci la password e clicca il pulsante **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Ora puoi configurare *digna* per usare la connessione ODBC, sia con una configurazione **DSN (Data Source Name)** sia con una configurazione **senza DSN**.

---

### A. Configurazione basata su DSN

#### Configurazione *digna*

Nella schermata **"Create a Database Connection"**, inserire quanto segue:

```
Technology:      Oracle
Database Name:   Database che contiene lo schema di origine
Schema Name:     Schema che contiene i dati di origine
Use ODBC:        Abilitato
```

#### Proprietà ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> Il `DSN` deve corrispondere al nome definito nella configurazione del driver ODBC.

---

### B. Configurazione senza DSN

#### Configurazione *digna*

Nella schermata **"Create a Database Connection"**, inserire quanto segue:

```
Technology:      Oracle
Database Name:   Schema che contiene i dati di origine (uguale a Schema Name)
Schema Name:     Schema che contiene i dati di origine
Use ODBC:        Abilitato
```

#### Proprietà ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```