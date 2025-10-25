---
title: Databricks-kapcsolat (Legacy, Unity Catalog nélkül) | digna dokumentáció
description: Konfiguráld a *digna*-t a Databrickshez Unity Catalog nélkül, a natív Python-connector vagy a Simba Spark ODBC-illesztő használatával. Támogatja a token-alapú hitelesítést és rugalmas csatlakozást.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Ez az útmutató bemutatja, hogyan konfiguráld a *digna*-t, hogy csatlakozzon a Databricks-hez a natív Python-connector vagy az ODBC-illesztő használatával.

A cikk a **"Create a Database Connection"** képernyőre utal.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Más hitelesítési módszerekhez használd az ODBC-illesztőt.

### Personal Access Token (PAT)

A personal access tokennel való hitelesítéshez lásd a hivatalos Databricks dokumentációt:  
👉 [Hogyan szerezz PAT-et](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Add meg a következő információkat a **"Create a Database Connection"** képernyőn:

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

## ODBC Driver

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a szakasz a token-alapú hitelesítésre összpontosít a **Simba Spark ODBC Driver** használatával.

### 1. Telepítsd az ODBC-illesztőt

Telepítsd a **Simba Spark ODBC Driver**-t a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Az ODBC adatforrás konfigurálása

Kövesd az alábbi lépéseket egy új ODBC-adatforrás konfigurálásához Personal Access Token használatával:

#### 1. lépés
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. lépés
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. lépés
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. lépés
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. lépés – Kapcsolat tesztelése

Kattints a **TEST** gombra. Egy sikeres kapcsolat így néz ki:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Most beállíthatod a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN-less** konfigurációval.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn add meg a következőket:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 A `DSN`-nek meg kell egyeznie azzal a névvel, amit az ODBC-illesztő konfigurációjában definiáltál.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn add meg a következőket:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
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