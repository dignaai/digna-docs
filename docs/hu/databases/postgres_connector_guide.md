---
title: PostgreSQL-connector – Adatbázis-integráció | digna dokumentáció
description: Konfigurálja a digna-t PostgreSQL-hez való csatlakozáshoz a psycopg Python-illesztőprogrammal vagy a PostgreSQL ODBC-illesztőprogrammal. Támogatja a jelszavas hitelesítést DSN-es vagy DSN-nélküli beállításokkal.
image: /assets/logo_square.png
---


# Forráscsatlakozó PostgreSQL-hez

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Postgreshez való csatlakozáshoz vagy a natív Python-illesztőprogram, vagy az ODBC-illesztőprogram használatával.

Ez a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Library:** `psycopg`  
**Támogatott hitelesítés:** csak jelszavas hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### *digna* konfiguráció (natív illesztőprogram)

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

## ODBC-illesztőprogram

Az ODBC-illesztőprogram szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogathat. Ez a rész a jelszavas hitelesítésre összpontosít a **PostgreSQL Unicode(x64)** illesztőprogram használatával.

### 1. Telepítse az ODBC-illesztőprogramot

Telepítse a **PostgreSQL Unicode(x64)** (vagy hasonló) illesztőprogramot a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Állítsa be az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás jelszavas hitelesítéssel történő konfigurálásához:

#### Step 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Megjegyzés: Ha az adatbázis-környezet megköveteli, hogy egy konkrét "SSLMode" értéket válasszon, kérjük, ezt a DSN-nélküli konfiguráció megadásakor is használja.

#### Step 2 – Test the connection

Kattintson a **"Test Connection"** gombra.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztőprogram konfigurációjában definiált névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```