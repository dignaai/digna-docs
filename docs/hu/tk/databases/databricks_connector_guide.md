---
title: Databricks csatlakozó Unity Catalogbal – Adatbázis-integráció | digna dokumentációja
description: Konfigurálja a *digna*-t úgy, hogy natív Python-csatlakozóval vagy ODBC-illesztőprogrammal kapcsolódjon a Unity Catalogon keresztül a Databricks-hez. Támogatja a token alapú hitelesítést és rugalmas kapcsolódási lehetőségeket.
image: /assets/logo_square.png
---

# Databricks forráscsatlakozó – Unity Catalog használatával

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t úgy, hogy a Databricks-hez natív Python-csatlakozóval vagy ODBC-illesztőprogrammal csatlakozzon.

It refers to the screen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Könyvtár:** `databricks-sql-connector`  
**Támogatott hitelesítés:** Csak Személyes hozzáférési token (PAT)

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### Személyes hozzáférési token (PAT)

Személyes hozzáférési tokennel történő hitelesítéshez tekintse meg a hivatalos Databricks dokumentációt:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* konfigurációja (natív illesztőprogram)

A **"Create a Database Connection"** képernyőn adja meg a következő adatokat:

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

Az ODBC-illesztőprogram szélesebb körű hitelesítési és kapcsolatbeállítási lehetőségeket támogat. Ez a rész a token alapú hitelesítéssel foglalkozik a **Simba Spark ODBC Driver** használatával.

### 1. ODBC-illesztőprogram telepítése

A gyártó hivatalos telepítési útmutatóját követve telepítse a **Simba Spark ODBC Driver**-t.

### 2. ODBC adatforrás konfigurálása

Személyes hozzáférési token használatával új ODBC adatforrást az alábbi lépésekkel konfigurálhatja:

#### Adım 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Adım 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Adım 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Adım 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Adım 5 – Kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolatnak így kell kinéznie:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Most már beállíthatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN-less** konfigurációval.

---

### A. DSN-alapú konfiguráció

#### *digna* konfigurációja

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 A `DSN`-nek egyeznie kell az ODBC-illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN-less konfiguráció

#### *digna* konfigurációja

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
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