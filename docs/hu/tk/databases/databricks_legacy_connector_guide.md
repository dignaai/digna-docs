---
title: Databricks Csatlakozó (Régi, Unity Catalog Nélkül) | digna Dokumentáció
description: A *digna* Databrickshez való konfigurálása natív Python connectorral vagy a Simba Spark ODBC driverrel Unity Catalog nélkül. Támogatja a token alapú hitelesítést és a rugalmas csatlakozási lehetőségeket.
image: /assets/logo_square.png
---

# Forráscsatlakozó Databrickshez – Unity Catalog nélkül

Ez a útmutató megmutatja, hogyan konfigurálja a *digna*-t Databrickshez natív Python connectorral vagy ODBC driverrel.

Ez az alábbi képernyőre utal: **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC drivert.

### Personal Access Token (PAT)

A személyes hozzáférési tokennel történő hitelesítéshez nézze meg a hivatalos Databricks dokumentációt:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Konfiguráció (Natív Driver)

Adja meg az alábbi adatokat a **"Create a Database Connection"** képernyőn:

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

Az ODBC driver szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész a token alapú hitelesítésre fókuszál a **Simba Spark ODBC Driver** használatával.

### 1. ODBC Driver telepítése

Telepítse a **Simba Spark ODBC Driver**-t a gyártó hivatalos telepítési útmutatóját követve.

### 2. ODBC Adatforrás konfigurálása

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához személyes hozzáférési token használatával:

#### Lépés 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Lépés 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Lépés 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Lépés 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Lépés 5 – Kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Most már konfigurálhatja a *digna*-t, hogy az ODBC kapcsolatot használja; vagy egy **DSN (Data Source Name)**-nel, vagy **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* Konfiguráció

Adja meg a **"Create a Database Connection"** képernyőn a következőket:

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

> 🔹 A `DSN` értéknek meg kell egyeznie az ODBC driver konfigurációjában definiált névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* Konfiguráció

Adja meg a **"Create a Database Connection"** képernyőn a következőket:

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