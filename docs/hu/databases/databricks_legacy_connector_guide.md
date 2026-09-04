---
title: Databricks Connector (Legacy, Unity Catalog nélkül) | digna dokumentáció
description: Konfigurálja a digna-t Databrickshez Unity Catalog nélkül a natív Python connectorral vagy a Simba Spark ODBC driverrel. Támogatja a token-alapú hitelesítést és rugalmas csatlakozást.
image: /assets/logo_square.png
---

# Forráskapcsoló Databrickshez - Unity Catalog nélkül

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Databrickshez való csatlakozáshoz a natív Python connector vagy az ODBC driver használatával.

A leírás a **"Create a Database Connection"** képernyőre vonatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python Driver

**Library:** `databricks-sql-connector`  
**Támogatott hitelesítés:** csak Személyes hozzáférési token (PAT)

> Más hitelesítési módszerekhez kérjük, használja az ODBC drivert.

### Személyes hozzáférési token (PAT)

A személyes hozzáférési token beszerzéséhez lásd a hivatalos Databricks dokumentációt:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguráció (natív driver)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

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

Az ODBC driver szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a szakasz a token-alapú hitelesítésre fókuszál a **Simba Spark ODBC Driver** használatával.

### 1. Telepítse az ODBC drivert

Telepítse a **Simba Spark ODBC Driver**-t a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához Személyes hozzáférési tokennel:

#### 1. lépés
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. lépés
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. lépés
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. lépés
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. lépés – Kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Most már konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)**-nel, akár **DSN nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",    value: "*digna*data_databricks"
```

> A `DSN`-nek meg kell egyeznie az ODBC driver konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

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