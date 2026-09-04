---
title: Snowflake Connector – Adatbázis-integráció | digna Dokumentáció
description: Állítsa be a digna-t, hogy csatlakozzon a Snowflake-hez a Python connector vagy a Snowflake ODBC driver használatával. Támogatja a jelszóalapú hitelesítést DSN-es vagy DSN-nélküli konfigurációkban.
image: /assets/logo_square.png
---


# Snowflake forráscsatlakozó

Ez az útmutató bemutatja, hogyan konfigurálható a *digna* a Snowflake-hez való csatlakozáshoz a natív Python-connector vagy az ODBC-illesztőprogram használatával.

A leírás a **"Create a Database Connection"** képernyőre vonatkozik.

![Adatbáziskapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Könyvtár:** `snowflake-connector-python`  
**Támogatott hitelesítés:** Csak jelszóalapú hitelesítés

> Más hitelesítési módszerekhez kérjük, használja az ODBC illesztőprogramot.

### *digna* konfiguráció (natív illesztőprogram)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC illesztőprogram

Az ODBC illesztőprogram szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogathat. Ez a rész a jelszóalapú hitelesítésre fókuszál, a **SnowflakeDSIIDriver** használatával.

### 1. Telepítse az ODBC illesztőprogramot

Telepítse a **SnowflakeDSIIDriver**-t a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszóalapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/snowflake/create_odbc_data_source_step1.png)

Megjegyzések:
- Ha nem ad meg értékeket a Database, Schema és Warehouse mezőkhöz, akkor ezeket az ODBC tulajdonságokként kell megadnia a *digna* adatforrás konfiguráció során.
- A "Server" értéke az ön snowflake fióknevéből és a ".snowflakecomputing.com" kiterjesztésből áll.

#### 2. lépés – A kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![2. lépés](images/snowflake/create_odbc_data_source_step2.png)

---

Most konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

Adja meg a következőket a **"Create a Database Connection"** képernyőn:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> A `DSN`-nek meg kell egyeznie az ODBC illesztőprogram konfigurációjában definiált névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

Adja meg a következőket a **"Create a Database Connection"** képernyőn:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```