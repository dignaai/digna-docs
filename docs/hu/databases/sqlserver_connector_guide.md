---
title: MS SQL Server Connector – Adatbázis-integráció | digna dokumentáció
description: Konfigurálja a digna-t, hogy csatlakozzon a Microsoft SQL Serverhez a pymssql Python driver vagy az SQL Server ODBC driver használatával. Támogatja a jelszó alapú hitelesítést DSN-es és DSN-nélküli beállításokkal.
image: /assets/logo_square.png
---


# Forráskapcsoló MS SQL Serverhez

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t, hogy SQL Serverhez csatlakozzon vagy a natív Python-connector (`pymssql`), vagy az ODBC driver használatával.

A leírás a **"Create a Database Connection"** képernyőre vonatkozik.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python driver

**Library:** `pymssql`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC drivert.

### *digna* konfiguráció (natív driver)

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

## ODBC driver

Az ODBC driver szélesebb hitelesítési és csatlakozási lehetőségeket támogathat. Ez a szakasz a jelszó alapú hitelesítésre fókuszál az **SQL Server** driver használatával.

### 1. Telepítse az ODBC drivert

Telepítse az **SQL Server** (vagy hasonló) drivert a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/sqlserver/create_odbc_data_source_step1.png)

Kattintson a **Next >** gombra.

#### 2. lépés
![2. lépés](images/sqlserver/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módszert (pl. felhasználónév és jelszó) és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### 3. lépés
![3. lépés](images/sqlserver/create_odbc_data_source_step3.png)

Válassza az ANSI kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![4. lépés](images/sqlserver/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy választhat naplózási opciókat szükség szerint, majd kattintson a **Finish** gombra.

#### 5. lépés
![5. lépés](images/sqlserver/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### 6. lépés
![6. lépés](images/sqlserver/create_odbc_data_source_step6.png)

Ha megjelenik a siker képernyő, az ODBC megfelelően konfigurálva van.

---

Most már konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN-nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

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

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC driver konfigurációjában megadott névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

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