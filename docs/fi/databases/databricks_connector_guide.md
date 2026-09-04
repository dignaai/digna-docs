---
title: Databricks-yhdistin Unity Catalogin kanssa – Tietokantaintegraatio | digna-dokumentaatio
description: Konfiguroi digna yhdistämään Databricksiin Unity Catalogin kautta käyttäen natiivista Python-yhdistäjää tai ODBC-ajuria. Tukee token-pohjaista todennusta ja joustavia yhteysvaihtoehtoja.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Tämä oppa kuvaa, miten *digna* konfiguroidaan yhdistämään Databricksiin käyttäen joko natiivia Python-yhdistäjää tai ODBC-ajuria.

Ohje viittaa näyttöön **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Muita todennustapoja varten käytä ODBC-ajuria.

### Personal Access Token (PAT)

Henkilökohtaisen käyttöoikeustunnuksen avulla todennukseen katso Databricksin virallinen dokumentaatio:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Anna seuraavat tiedot **"Create a Database Connection"** -näytössä:

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

## ODBC Driver

ODBC-ajuri tukee laajempaa valikoimaa todennus- ja yhteysvaihtoehtoja. Tässä osiossa keskitytään token-pohjaiseen todennukseen käyttäen **Simba Spark ODBC Driver** -ajuria.

### 1. Install the ODBC Driver

Asenna **Simba Spark ODBC Driver** noudattamalla toimittajan virallista asennusohjetta.

### 2. Configure the ODBC Data Source

Seuraa näitä ohjeita luodaksesi uuden ODBC-tietolähteen käyttäen Personal Access Tokenia:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Klikkaa **TEST**-painiketta. Onnistunut yhteys näyttää tältä:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nyt voit konfiguroida *digna*:n käyttämään ODBC-yhteyttä joko **DSN (Data Source Name)** -pohjaisella asetuksella tai ilman DSN:ää (DSN-less).

---

### A. DSN-Based Configuration

#### *digna* Configuration

Anna **"Create a Database Connection"** -näytössä seuraavat tiedot:

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

> `DSN` on vastattava nimeä, joka on määritelty ODBC-ajurin asetuksissa.

---

### B. DSN-less Configuration

#### *digna* Configuration

Anna **"Create a Database Connection"** -näytössä seuraavat tiedot:

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