---
title: Apache Hive Connector – Database Integration | digna Documentation
description: Configure digna to connect to Apache Hive using the native PyHive driver or the Cloudera ODBC driver. Supports password-based authentication and DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Source Connector for Hive

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Hive med antingen den inbyggda Python-anslutningen eller ODBC-drivrutinen.

Den hänvisar till skärmen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `PyHive`  
**Supported Authentication:** Password-based authentication only

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna* Configuration (Native Driver)

Ange följande information i skärmen **"Create a Database Connection"**:

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

ODBC-drivrutinen kan stödja ett bredare utbud av autentiserings- och anslutningsalternativ. Detta avsnitt fokuserar på lösenordsbaserad autentisering med drivrutinen **Cloudera ODBC Driver for Apache Hive**.

### 1. Install the ODBC Driver

Installera **Cloudera ODBC Driver for Apache Hive** (eller liknande) genom att följa leverantörens officiella installationsguide.

### 2. Configure the ODBC Data Source

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Step 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Step 2 – Test the connection

Ange lösenordet och klicka på **Test**-knappen.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Efter ett lyckat test klickar du på **OK**-knappen.

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-less**-konfiguration.

---

### A. DSN-Based Configuration

#### *digna* Configuration

I skärmen **"Create a Database Connection"** ange följande:

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

> `DSN` måste matcha namnet som är definierat i din ODBC-drivrutinskonfiguration.

---

### B. DSN-less Configuration

#### *digna* Configuration

I skärmen **"Create a Database Connection"** ange följande:

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