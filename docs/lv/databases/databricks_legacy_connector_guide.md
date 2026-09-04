---
title: Databricks Connector (Legacy, without Unity Catalog) | digna Documentation
description: Configure digna to connect to Databricks without Unity Catalog using the native Python connector or the Simba Spark ODBC driver. Supports token-based authentication and flexible connectivity.
image: /assets/logo_square.png
---

# Avota savienotājs Databricks — bez Unity Catalog

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai izveidotu savienojumu ar Databricks, izmantojot vai nu nativā Python konektoru, vai ODBC draiveri.

Tā atsaucas uz ekrānu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativais Python draiveris

**Bibliotēka:** `databricks-sql-connector`  
**Atbalstītā autentifikācija:** tikai Personīgais piekļuves tokens (PAT)

> Citu autentifikācijas metožu gadījumā, lūdzu, izmantojiet ODBC draiveri.

### Personīgais piekļuves tokens (PAT)

Lai autentificētos, izmantojot personīgo piekļuves tokenu, skatiet oficiālo Databricks dokumentāciju:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfigurācija (nativais draiveris)

Norādiet sekojošo informāciju ekrānā **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC draiveris

ODBC draiveris atbalsta plašāku autentifikācijas un savienošanās iespēju klāstu. Šī sadaļa koncentrējas uz autentifikāciju, izmantojot tokenu, ar **Simba Spark ODBC Driver**.

### 1. Instalējiet ODBC draiveri

Instalējiet **Simba Spark ODBC Driver**, sekojot piegādātāja oficiālajai instalācijas rokasgrāmatai.

### 2. Konfigurējiet ODBC datu avotu

Izpildiet šos soļus, lai konfigurētu jaunu ODBC datu avotu, izmantojot Personīgo piekļuves tokenu:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – savienojuma pārbaude

Nospiediet pogu **TEST**. Veiksmīgs savienojums izskatīsies šādi:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu — vai nu ar **DSN (Data Source Name)**, vai ar **bez-DSN** konfigurāciju.

---

### A. DSN bāzēta konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC rekvizīti

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` ir jāatbilst nosaukumam, kas definēts jūsu ODBC draivera konfigurācijā.

---

### B. Bez-DSN konfigurācija

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC rekvizīti

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