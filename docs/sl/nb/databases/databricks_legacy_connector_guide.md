---
title: Povezava Databricks (Legacy, brez Unity Catalog) | digna-dokumentacija
description: Konfigurirajte digna za povezavo z Databricks brez Unity Catalog z uporabo native Python-connectorja ali Simba Spark ODBC-driverja. Podpira preverjanje pristnosti s tokenom in fleksibilne možnosti povezave.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Ta navodila opisujejo, kako konfigurirati *digna* za povezavo z Databricks z uporabo bodisi native Python-connectorja ali ODBC-driverja.

Navaja zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Za druge metode preverjanja pristnosti uporabite ODBC-driver.

### Personal Access Token (PAT)

Za avtentikacijo s personal access token glejte uradno Databricks dokumentacijo:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Vnesite naslednje informacije na zaslonu **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    ime gostitelja Databricks, npr. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Ta parameter se ne uporablja za Databricks brez Unity Catalog
Schema Name:     Shema, ki vsebuje izvorne podatke
User Name:       HTTP Path, ki ga zagotavlja Databricks, npr. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token (PAT), npr. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-driver podpira širši nabor možnosti preverjanja pristnosti in povezav. Ta razdelek se osredotoča na preverjanje pristnosti s tokenom z uporabo **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Namestite **Simba Spark ODBC Driver** tako, da sledite uradnim navodilom dobavitelja.

### 2. Configure the ODBC Data Source

Sledite tem korakom za konfiguracijo nove ODBC-datakilde z uporabo Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Kliknite gumb **TEST**. Uspešna povezava naj bi izgledala takole:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali v **DSN-less** nastavitvi.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   Ta parameter se ne uporablja za Databricks brez Unity Catalog
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` se mora ujemati z imenom, definiranem v vaši konfiguraciji ODBC-driverja.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      Databricks (Legacy)
Database Name:   Ta parameter se ne uporablja za Databricks brez Unity Catalog
Schema Name:     Shema, ki vsebuje izvorne podatke
Use ODBC:        Enabled
```

#### ODBC Properties

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```