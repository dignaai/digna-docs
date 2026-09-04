---
title: Databricks Connector with Unity Catalog – Database Integration | digna Documentation
description: Configure digna to connect to Databricks with Unity Catalog using the native Python connector or ODBC driver. Supports token-based authentication and flexible connectivity.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Databrickshez való csatlakozáshoz, akár a natív Python connectorral, akár az ODBC driverrel.

Ez a képernyőre hivatkozik: **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Támogatott hitelesítés:** csak Personal Access Token (PAT)

> Más hitelesítési módszerekhez használja az ODBC drivert.

### Personal Access Token (PAT)

A személyes hozzáférési tokennel való hitelesítéshez lásd a hivatalos Databricks dokumentációt:  
[Hogyan szerezzünk PAT-et](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Konfiguráció (Natív illesztőprogram)

Adja meg a következő adatokat a **"Create a Database Connection"** képernyőn:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   A használni kívánt katalógus neve.
Schema Name:     Az adatok forrását tartalmazó séma
User Name:       A Databricks által megadott HTTP Path, pl. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, pl. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (alapértelmezett)
```

---

## ODBC Driver

Az ODBC driver szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a token-alapú hitelesítésre fókuszál a **Simba Spark ODBC Driver** használatával.

### 1. Telepítse az ODBC drivert

Telepítse a **Simba Spark ODBC Driver**-t a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához Personal Access Token használatával:

#### 1. lépés
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. lépés
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. lépés
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. lépés
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. lépés – A kapcsolat tesztelése

Kattintson a **TEST** gombra. Egy sikeres kapcsolat így néz ki:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Most konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)**-nel, akár **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Databricks
Database Name:   A használni kívánt katalógus neve.
Schema Name:     Az adatok forrását tartalmazó séma
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
Technology:      Databricks
Database Name:   A használni kívánt katalógus neve.
Schema Name:     Az adatok forrását tartalmazó séma
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