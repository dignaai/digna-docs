---
title: Databricks csatlakoztatása Unity Catalogdal — adatbázis integráció | digna dokumentáció
description: Állítsa be a digna-t, hogy csatlakozzon a Databrickshez Unity Catalog használatával natív Python-kapcsolóval vagy ODBC-illesztőprogrammal. Támogatott a token-alapú hitelesítés és rugalmas csatlakozási beállítások.
image: /assets/logo_square.png
---

# Forráskapcsoló Databrickshez — Unity Catalog használatával

Ez az útmutató leírja, hogyan állítsa be a *digna*-t Databrickshez való csatlakozáshoz, a natív Python-kapcsoló vagy az ODBC-illesztőprogram használatával.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python driver

**Library:** `databricks-sql-connector`  
**Támogatott hitelesítés:** csak Personal Access Token (PAT)

> ⚠️ Egyéb hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### Personal Access Token (PAT)

Ha személyes hozzáférési tokennel szeretne hitelesíteni, tekintse meg a Databricks hivatalos dokumentációját:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguráció (natív driver)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

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

## ODBC-illesztőprogram

Az ODBC-illesztőprogram szélesebb körű hitelesítési módszereket és csatlakozási lehetőségeket támogat. Ez a rész a token-alapú hitelesítésre fókuszál, a **Simba Spark ODBC Driver** használatával.

### 1. Az ODBC-illesztőprogram telepítése

Telepítse a **Simba Spark ODBC Driver**-t a gyártó hivatalos útmutatójának megfelelően.

### 2. Az ODBC adatforrás beállítása

Végezze el az alábbi lépéseket egy új ODBC adatforrás beállításához Personal Access Token használatával:

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

Most beállíthatja a *digna*-t ODBC-kapcsolat használatára — vagy **DSN (Data Source Name)**-alapú módban, vagy **DSN nélküli** módban.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** ablakban adja meg a következőket:

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

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** ablakban adja meg a következőket:

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