---
title: Teradata savienotājs – datubāzes integrācija | digna dokumentācija
description: Konfigurējiet digna, lai izveidotu savienojumu ar Teradata, izmantojot teradatasql Python driveri vai Teradata ODBC driveri. Atbalsta paroles autentifikāciju ar DSN vai bez DSN.
image: /assets/logo_square.png
---


# Source Connector for Teradata

Šajā rokasgrāmatā aprakstīts, kā konfigurēt *digna*, lai izveidotu savienojumu ar Teradata, izmantojot vai nu nativā Python savienotāja draiveri, vai ODBC draiveri.

Tas attiecas uz ekrānu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Supported Authentication:** Password-based authentication only

> ⚠️ For other authentication methods, please use the ODBC driver.

### *digna* Configuration (Native Driver)

Sniedziet šādu informāciju **"Create a Database Connection"** ekrānā:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības iespēju klāstu. Šī sadaļa koncentrējas uz paroles autentifikāciju, izmantojot draiveri **Teradata Database ODBC Driver 20.00**.

### 1. Install the ODBC Driver

Instalējiet draiveri **Teradata Database ODBC Driver 20.00** (vai līdzīgu), sekojot piegādātāja oficiālajai instalācijas instrukcijai.

### 2. Configure the ODBC Data Source

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot paroles autentifikāciju:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Noklikšķiniet uz pogas **Test**.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Ievadiet lietotājvārdu un paroli.

Noklikšķiniet uz pogas **OK**. Kad redzat veiksmīgas konfigurācijas ekrānu, ODBC ir konfigurēts pareizi.

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai **bez DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

"Create a Database Connection" ekrānā norādiet sekojošo:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

"Create a Database Connection" ekrānā norādiet sekojošo:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```