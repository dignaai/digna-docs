---
title: PostgreSQL Csatlakozó – Adatbázis integráció | digna Dokumentáció
description: Konfigurálja a *digna*-t, hogy PostgreSQL-hez csatlakozzon a psycopg Python-illesztőprogrammal vagy a PostgreSQL ODBC-illesztőprogrammal. Támogatja a jelszó alapú hitelesítést DSN és DSN-less konfigurációkban.
image: /assets/logo_square.png
---


# PostgreSQL forrás csatlakozó

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Postgreshez való csatlakozáshoz a natív Python-illesztőprogrammal vagy az ODBC-illesztőprogrammal.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Könyvtár:** `psycopg`  
**Támogatott hitelesítés:** csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### *digna* — konfiguráció (natív illesztőprogram)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Postgres
Host Address:    Szerver neve vagy IP-címe
Host Port:       Port száma, például 5432
Database Name:   Adatbázis neve
Schema Name:     A forrást tartalmazó séma
User Name:       Adatbázis felhasználónév
User Password:   Felhasználói jelszó
Use ODBC:        Disabled (default)
```

---

## ODBC-illesztőprogram

Az ODBC-illesztőprogram szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész jelszó alapú hitelesítéssel foglalkozik a **PostgreSQL Unicode(x64)** illesztőprogram használatával.

### 1. Telepítse az ODBC-illesztőprogramot

Telepítse a **PostgreSQL Unicode(x64)** (vagy hasonló) illesztőprogramot a gyártó hivatalos útmutatása szerint.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket, hogy új ODBC-adatforrást állítson be jelszó alapú hitelesítéssel:

#### 1. lépés
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Megjegyzés: Ha az adatbázis-konfigurációja konkrét "SSLMode" kiválasztását igényli, mindenképpen használja ugyanazt a beállítást a DSN nélküli konfiguráció megadásakor.

#### 2. lépés – Kapcsolat tesztelése

Kattintson a **Test Connection** gombra.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Most konfigurálhatja a *digna*-t ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN-less** módban.

---

### A. DSN alapú konfiguráció

#### *digna* — konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   Az adatbázis, amely a forrás sémát tartalmazza
Schema Name:     A forrást tartalmazó séma
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció (DSN-less)

#### *digna* — konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   A forrást tartalmazó séma (ugyanaz, mint a Schema Name)
Schema Name:     A forrást tartalmazó séma
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user"
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```