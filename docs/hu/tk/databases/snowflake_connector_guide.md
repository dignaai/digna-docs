---
title: Snowflake Csatlakozó – Adatbázis Integráció | digna Dokumentáció
description: Konfigurálja a digna-t úgy, hogy Snowflake-hez csatlakozzon a Python connector vagy a Snowflake ODBC illesztőprogram használatával. Támogatja a jelszóalapú hitelesítést DSN-es és DSN nélküli beállításokkal.
image: /assets/logo_square.png
---


# Snowflake forrás csatlakozó

Ez az útmutató bemutatja, hogyan csatlakoztassa a *digna*-t helyi Python connectorral vagy ODBC illesztőprogrammal a Snowflake-hez.

Ez a dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Helyi Python illesztőprogram

**Könyvtár:** `snowflake-connector-python`  
**Támogatott hitelesítés:** Csak jelszóalapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC illesztőprogramot.

### *digna* konfiguráció (helyi illesztőprogram)

A **"Create a Database Connection"** képernyőn adja meg a következő információkat:

```
Technology:      Snowflake
Host Address:    Snowflake fiók neve
Host Port:       Nem szükséges
Database Name:   Az a adatbázis, amely a forrás sémát tartalmazza
Schema Name:     Az a séma, amely a forrás adatokat tartalmazza
User Name:       "user<@>warehouse" formátumú felhasználónév és warehouse
User Password:   A felhasználó jelszava
Use ODBC:        Kikapcsolva (alapértelmezett)
```

---

## ODBC illesztőprogram

Az ODBC illesztőprogram szélesebb körű hitelesítési és csatlakozási beállításokat támogathat. Ez a rész a **SnowflakeDSIIDriver** használatával történő jelszóalapú hitelesítésre összpontosít.

### 1. Telepítse az ODBC illesztőprogramot

Telepítse a **SnowflakeDSIIDriver**-t a gyártó hivatalos telepítési útmutatójának követésével.

### 2. Konfigurálja az ODBC adatforrást

Új ODBC adatforrást az alábbi lépésekkel konfigurálhat jelszóalapú hitelesítéshez:

#### 1. lépés
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Megjegyzések:
- Ha nem ad meg értékeket a Database, Schema és Warehouse mezőkhöz, akkor ezeket a *digna* adatforrás konfigurációja során kell ODBC tulajdonságokként megadnia.
- A "Server" érték a Snowflake fióknevéhez hozzáadott ".snowflakecomputing.com" végződés lesz.

#### 2. lépés – A kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Most konfigurálhatja a *digna*-t az ODBC kapcsolat használatára; vagy egy **DSN (Data Source Name)** segítségével, vagy **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Snowflake
Database Name:   Az a adatbázis, amely a forrás sémát tartalmazza
Schema Name:     Az a séma, amely a forrás adatokat tartalmazza
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{a jelszava kapcsos zárójelben}"

opcionális:
name: "Database",       value: "Az a adatbázis, amely a forrás sémát tartalmazza"
name: "Schema",         value: "Az a séma, amely a forrás adatokat tartalmazza"
name: "Warehouse",      value: "Az a warehouse, amelyet a SQL-ek futtatásához használnak"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Snowflake
Database Name:   A forrás adatokat tartalmazó séma (ugyanaz, mint a Schema Name)
Schema Name:     A forrás adatokat tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Az a adatbázis, amely a forrás sémát tartalmazza"
name: "Schema",     value: "Az a séma, amely a forrás adatokat tartalmazza"
name: "Warehouse",  value: "Az a warehouse, amelyet a SQL-ek futtatásához használnak"
```