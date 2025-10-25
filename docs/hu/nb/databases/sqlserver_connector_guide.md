---
title: MS SQL Server-csatlakozás – Adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t, hogy Microsoft SQL Serverhez csatlakozzon a pymssql Python-illesztőprogrammal vagy az SQL Server ODBC-illesztővel. Támogatja a jelszó alapú hitelesítést DSN vagy DSN-nélküli konfigurációval.
image: /assets/logo_square.png
---


# MS SQL Server forráskapcsolat

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t, hogy SQL Serverhez csatlakozzon akár a natív Python-illesztővel, akár az ODBC-illesztővel.

Az útmutató a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `pymssql`  
**Supported Authentication:** csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőt.

### *digna* konfiguráció (natív illesztő)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

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

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész a **SQL Server** illesztővel történő jelszó alapú hitelesítésre összpontosít.

### 1. Telepítse az ODBC-illesztőt

Telepítse a **SQL Server** illesztőt (vagy egy megfelelőt) a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás jelszó alapú hitelesítéssel történő konfigurálásához:

#### 1. lépés
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kattintson a **Next >** gombra.

#### 2. lépés
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módot (pl. felhasználónév és jelszó)
és adja meg a szükséges információkat.

Kattintson a **Next >** gombra.

#### 3. lépés
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Megőrizheti az alapértelmezett beállításokat, vagy szükség szerint választhat naplózási opciókat, majd kattintson a **Finish** gombra. 

#### 5. lépés
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### 6. lépés
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Amikor megjelenik a sikeres képernyő, az ODBC megfelelően van konfigurálva.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-less** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN`-nek meg kell egyeznie azzal a névvel, amely az ODBC-illesztő konfigurációjában szerepel.

---

### B. DSN-less konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```