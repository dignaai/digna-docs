---
title: Snowflake Connector – adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t Snowflake-hez való csatlakozáshoz Python-connectorral vagy ODBC-illesztőprogrammal. Támogatott a jelszó alapú hitelesítés DSN-es és DSN nélküli konfigurációkban.
image: /assets/logo_square.png
---


# Adatforrás a Snowflake-hez

Ez az útmutató leírja, hogyan állítsa be a *digna*-t Snowflake-hez való csatlakozáshoz natív Python-connectorral vagy ODBC-illesztőprogrammal.

Ez a dokumentum a **„Create a database connection”** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Könyvtár:** `snowflake-connector-python`  
**Támogatott hitelesítés:** csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### digna konfiguráció (natív illesztőprogram)

Adja meg a következő információkat a **„Create a database connection”** képernyőn:

```
Technology:      Snowflake
Host Address:    Назва облікового запису Snowflake
Host Port:       Не потрібно
Database Name:   База даних, що містить вихідну схему
Schema Name:     Схема, що містить вихідні дані
User Name:       Ім'я користувача та warehouse у форматі "user<@>warehouse"
User Password:   Пароль для користувача
Use ODBC:        Вимкнено (за замовчуванням)
```

---

## ODBC-illesztőprogram

Az ODBC-illesztőprogram szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész a jelszó alapú hitelesítésre összpontosít a **SnowflakeDSIIDriver** használatával.

### 1. Telepítse az ODBC-illesztőprogramot

Telepítse a **SnowflakeDSIIDriver**-t a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Állítsa be az ODBC adatforrást

Végezze el ezeket a lépéseket egy új ODBC-adatforrás létrehozásához jelszó alapú hitelesítéssel:

#### Крок 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Megjegyzések:
- Ha nem ad meg értéket a Database, Schema és Warehouse mezőknek, akkor azokat ODBC tulajdonságként kell megadnia a *digna* adatforrás-konfigurációja során.
- A "Server" értéke a Snowflake-fiókneve + ".snowflakecomputing.com"

#### Крок 2 – Kapcsolat ellenőrzése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Most már beállíthatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN nélküli** konfigurációban.

---

### A. DSN-alapú konfiguráció

#### digna konfigurációja

Adja meg a következőket a **„Create a database connection”** képernyőn:

```
Technology:      Snowflake
Database Name:   База даних, що містить вихідну схему
Schema Name:     Схема, що містить вихідні дані
Use ODBC:        Увімкнено
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

> 🔹 A `DSN` értékének meg kell egyeznie az ODBC-illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### digna konfigurációja

Adja meg a következőket a **„Create a database connection”** képernyőn:

```
Technology:      Snowflake
Database Name:   Схема, що містить вихідні дані (те саме, що Schema Name)
Schema Name:     Схема, що містить вихідні дані
Use ODBC:        Увімкнено
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