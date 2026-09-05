# Source Connector for MS SQL Server

Questa guida descrive come configurare *digna* per connettersi a SQLServer usando sia il connettore Python nativo sia il driver ODBC.

Si riferisce alla schermata **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Solo autenticazione basata su password

> Per altri metodi di autenticazione, utilizzare il driver ODBC.

### *digna* Configuration (Native Driver)

Fornire le seguenti informazioni nella schermata **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Il driver ODBC può supportare una gamma più ampia di opzioni di autenticazione e connettività. Questa sezione si concentra sull'autenticazione basata su password utilizzando il driver **SQL Server**.

### 1. Installare il driver ODBC

Installare il driver **SQL Server** (o simile) seguendo la guida di installazione ufficiale del fornitore.

### 2. Configurare la Data Source ODBC

Seguire questi passaggi per configurare una nuova data source ODBC utilizzando l'autenticazione basata su password:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Cliccare il pulsante **Next >**.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Scegliere il metodo di autenticazione (es. nome utente e password)
e fornire i dati richiesti.

Cliccare il pulsante **Next >**.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Scegliere le impostazioni compatibili ANSI quindi cliccare il pulsante **Next >**.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

È possibile lasciare le impostazioni predefinite o scegliere opzioni di logging se necessario
e cliccare il pulsante **Finish**.

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Ora cliccare il pulsante ** Test datasource **.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Quando si riceve la schermata di successo, l'ODBC è configurato correttamente.

---

Ora è possibile configurare *digna* per usare la connessione ODBC, sia con un **DSN (Data Source Name)** sia con una configurazione **DSN-less**.

---

### A. Configurazione basata su DSN

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire i seguenti dati:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Configurazione DSN-less

#### *digna* Configuration

Nella schermata **"Create a Database Connection"**, fornire i seguenti dati:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```