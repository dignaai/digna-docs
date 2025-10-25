---
title: Databricks csatlakozó (Legacy, Unity Catalog nélkül) | digna dokumentáció
description: Állítsa be a digna-t Databricks Unity Catalog nélküli csatlakoztatásához a natív Python-kapcsolón vagy a Simba Spark ODBC meghajtón keresztül. Támogatott token alapú hitelesítés és rugalmas csatlakozási lehetőségek.
image: /assets/logo_square.png
---

# Databricks forráscsatlakozó — Unity Catalog nélkül

Ez az útmutató leírja, hogyan állítsa be a *digna*-t Databricks csatlakoztatásához natív Python-kapcsolón vagy ODBC-meghajtón keresztül.

Hivatkozik a **"Create a Database Connection"** képernyőre.

![Створити підключення до бази даних](images/data_source_config_input_mask.png)

---

## Natív Python-meghajtó

**Könyvtár:** `databricks-sql-connector`  
**Támogatott hitelesítés:** csak Personal Access Token (PAT)

> ⚠️ Más hitelesítési módszerekhez használja az ODBC-meghajtót.

### Personal Access Token (PAT)

A Personal Access Token megszerzéséhez tekintse meg a Databricks hivatalos dokumentációját:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfiguráció (natív meghajtó)

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

## ODBC-meghajtó

Az ODBC-meghajtó szélesebb körű hitelesítési módszereket és csatlakozási opciókat támogat. Ebben a részben a token alapú hitelesítést ismertetjük a **Simba Spark ODBC Driver** használatával.

### 1. Telepítse az ODBC-meghajtót

Telepítse a **Simba Spark ODBC Driver**-t a beszállító hivatalos telepítési útmutatójának megfelelően.

### 2. Állítsa be az ODBC adatforrást

Végezze el az alábbi lépéseket egy új ODBC adatforrás létrehozásához Personal Access Token használatával:

#### Lépés 1
![Крок 1](images/databricks/create_odbc_data_source_step1.png)

#### Lépés 2
![Крок 2](images/databricks/create_odbc_data_source_step2.png)

#### Lépés 3
![Крок 3](images/databricks/create_odbc_data_source_step3.png)

#### Lépés 4
![Крок 4](images/databricks/create_odbc_data_source_step4.png)

#### Lépés 5 – Kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![Крок 5](images/databricks/create_odbc_data_source_step5.png)

---

Most beállíthatja a *digna*-t ODBC-kapcsolat használatára — vagy **DSN (Data Source Name)** alapú, vagy **DSN-less** konfigurációban.

---

### A. DSN alapú konfiguráció

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

> 🔹 `DSN`-nek meg kell egyeznie az ODBC-meghajtó beállításaiban megadott névvel.

---

### B. DSN-less konfiguráció

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