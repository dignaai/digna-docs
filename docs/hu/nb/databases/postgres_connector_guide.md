---
title: PostgreSQL Connector – Adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t, hogy csatlakozzon PostgreSQL-hez a psycopg Python-illesztőprogram vagy a PostgreSQL ODBC-illesztő használatával. Támogatja a jelszóalapú hitelesítést DSN-es és DSN-nélküli beállításokkal.
image: /assets/logo_square.png
---


# Forráskapcsolat PostgreSQL-hez

Ez az útmutató bemutatja, hogyan konfigurálja a *digna*-t, hogy Postgres-hez csatlakozzon vagy a natív Python-csatlakozó, vagy az ODBC-illesztő használatával.

Ez a képernyőre hivatkozik: **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `psycopg`  
**Támogatott hitelesítés:** Csak jelszóalapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőt.

### *digna*-konfiguráció (natív illesztő)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész a jelszóalapú hitelesítésre fókuszál a **PostgreSQL Unicode(x64)** illesztő használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse a **PostgreSQL Unicode(x64)** (vagy annak megfelelő) illesztőt a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás konfigurálásához, amely jelszóalapú hitelesítést használ:

#### Lépés 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Megjegyzés: Ha az adatbázis-környezet megköveteli, hogy egy konkrét "SSLMode"-ot válasszon, ügyeljen arra, hogy ezt is használja, amikor DSN-nélküli konfigurációt definiál.

#### Lépés 2 – Tesztelje a kapcsolatot

Kattintson a **Test Connection** gombra.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Most már konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár egy **DSN (Data Source Name)**, akár egy **DSN-nélküli** beállítás segítségével.

---

### A. DSN-alapú konfiguráció

#### *digna*-konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egyenértékek

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN`-nek meg kell egyeznie azzal a névvel, amelyet az ODBC-illesztő konfigurációjában definiált.

---

### B. DSN-nélküli konfiguráció

#### *digna*-konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egyenértékek

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```