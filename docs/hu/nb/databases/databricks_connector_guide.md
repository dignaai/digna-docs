---
title: Databricks csatlakozó Unity Catalog használatával – Adatbázis-integráció | digna dokumentáció
description: Konfigurálja a digna-t, hogy csatlakozzon a Databricks-hez Unity Catalog használatával a natív Python-connectorral vagy ODBC-driverrel. Támogatja a token alapú hitelesítést és a rugalmas kapcsolódást.
image: /assets/logo_square.png
---

# Databricks-kapcsolat Unity Catalog használatával

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t, hogy csatlakozzon a Databricks-hez a natív Python-connectorral vagy az ODBC-driverrel.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python Driver

**Library:** `databricks-sql-connector`  
**Támogatott hitelesítés:** csak Personal Access Token (PAT)

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC drivert.

### Personal Access Token (PAT)

A személyes hozzáférési tokennel történő hitelesítéshez lásd a Databricks hivatalos dokumentációját:  
👉 [Hogyan szerezzünk PAT-et](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

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

## ODBC-driver

Az ODBC-driver szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a token alapú hitelesítésre összpontosít a **Simba Spark ODBC Driver** használatával.

### 1. Az ODBC-driver telepítése

Telepítse a **Simba Spark ODBC Driver**-t a gyártó hivatalos telepítési útmutatójának követésével.

### 2. Az ODBC adatforrás konfigurálása

Kövesse az alábbi lépéseket egy új ODBC-adatforrás konfigurálásához Personal Access Token használatával:

#### 1. lépés
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. lépés
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. lépés
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. lépés
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. lépés – A kapcsolat tesztelése

Kattintson a **TEST** gombra. Sikeres kapcsolódás így néz ki:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** segítségével, akár **DSN-less** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

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

### B. DSN-less konfiguráció

#### *digna* Configuration

In the **"Create a Database Connection"** screen, provide the following:

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