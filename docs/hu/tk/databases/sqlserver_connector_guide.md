---
title: MS SQL Server csatlakozó – Adatbázis-integráció | digna dokumentációja
description: Állítsa be a digna-t úgy, hogy a pymssql Python-illesztőprogram vagy az SQL Server ODBC-illesztőprogram használatával csatlakozzon a Microsoft SQL Serverhez. Támogatja a jelszó alapú hitelesítést DSN-es vagy DSN nélküli beállításokkal.
image: /assets/logo_square.png
---


# Forráscsatlakozó MS SQL Serverhez

Ez az útmutató leírja, hogyan konfigurálható a *digna* úgy, hogy natív Python-illesztőprogramot vagy ODBC-illesztőprogramot használva kapcsolódjon SQL Serverhez.

Ez az útmutató a "Create a Database Connection" képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Helyi Python-illesztőprogram

**Könyvtár:** `pymssql`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### *digna* konfiguráció (helyi illesztőprogram)

Adja meg a következő információkat a "Create a Database Connection" képernyőn:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-illesztőprogram

Az ODBC-illesztőprogram szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a jelszó alapú hitelesítésre fókuszál, és az SQL Server illesztőprogramot használja.

### 1. Telepítse az ODBC-illesztőprogramot

Telepítse az SQL Server (vagy hasonló) illesztőprogramot a gyártó hivatalos telepítési útmutatóját követve.

### 2. Konfigurálja az ODBC adatforrást

Az alábbi lépések egy új ODBC adatforrás jelszó alapú hitelesítéssel történő konfigurálásához:

#### 1. lépés
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kattintson a **Next >** gombra.

#### 2. lépés
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módszert (pl. felhasználónév és jelszó), és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### 3. lépés
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy szükség szerint válasszon naplózási (logging) opciókat, majd kattintson a **Finish** gombra.

#### 5. lépés
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### 6. lépés
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Ha sikerüzenetet kap, az ODBC megfelelően van konfigurálva.

---

Most már konfigurálhatja a *digna*-t az ODBC csatlakozás használatára; ez történhet egy **DSN (Data Source Name)** segítségével vagy **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfiguráció

Adja meg a következőket a "Create a Database Connection" képernyőn:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

Adja meg a következőket a "Create a Database Connection" képernyőn:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```