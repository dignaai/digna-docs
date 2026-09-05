# Source Connector for Hive

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai savienotos ar Hive, izmantojot vai nu iebūvēto Python savienotāju, vai ODBC draiveri.

Tā attiecas uz ekrānu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `PyHive`  
**Supported Authentication:** Password-based authentication only

> Citiem autentifikācijas veidiem, lūdzu, izmantojiet ODBC draiveri.

### *digna* Configuration (Native Driver)

Norādiet šādu informāciju ekrānā **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības opciju klāstu. Šī sadaļa koncentrējas uz autentifikāciju ar paroli, izmantojot draiveri **Cloudera ODBC Driver for Apache Hive**.

### 1. Install the ODBC Driver

Instalējiet **Cloudera ODBC Driver for Apache Hive** (vai līdzīgu), sekojot piegādātāja oficiālajai instalācijas instrukcijai.

### 2. Configure the ODBC Data Source

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot autentifikāciju ar paroli:

#### Step 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Step 2 – Test the connection

Ievadiet paroli un noklikšķiniet uz pogas **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Pēc veiksmīgas pārbaudes noklikšķiniet uz pogas **OK**.

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai ar **DSN-less** iestatījumu.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```