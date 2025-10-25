---
title: Povezava Databricks z Unity Catalog — integracija baze podatkov | dokumentacija digna
description: Nastavite digna za povezavo z Databricks z Unity Catalog z uporabo izvornega Python konektorja ali ODBC gonilnika. Podprta je avtentikacija na osnovi žetona in prilagodljive možnosti povezave.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Ta vodič opisuje, kako nastaviti *digna* za povezavo z Databricks, z uporabo bodisi izvornega Python konektorja bodisi ODBC gonilnika.

Navaja zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Izvorni Python gonilnik

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ For other authentication methods, please use the ODBC driver.

### Personal Access Token (PAT)

Za avtentikacijo z personal access token se obrnite na uradno dokumentacijo Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Provide the following information in the **"Create a Database Connection"** screen:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC gonilnik

ODBC-gonilnik podpira širši nabor načinov avtentikacije in možnosti povezave. Ta razdelek se osredotoča na avtentikacijo na osnovi žetona z uporabo **Simba Spark ODBC Driver**.

### 1. Namestite ODBC gonilnik

Namestite **Simba Spark ODBC Driver** v skladu z uradnim navodilom ponudnika.

### 2. Konfigurirajte ODBC vir podatkov

Izvedite naslednje korake, da nastavite nov ODBC vir podatkov z uporabo Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Kliknite gumb **TEST**. Uspešna povezava bi morala izgledati tako:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Zdaj lahko nastavite *digna*, da uporablja ODBC-povezavo — bodisi z **DSN (Data Source Name)** ali v **DSN-less** načinu.

---

### A. Konfiguracija na osnovi DSN

#### *digna* Configuration

V oknu **"Create a Database Connection"** navedite naslednje:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less konfiguracija

#### *digna* Configuration

V oknu **"Create a Database Connection"** navedite naslednje:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
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