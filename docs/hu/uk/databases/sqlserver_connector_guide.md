---
title: MS SQL Server Connector – Adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t, hogy kapcsolódjon a Microsoft SQL Serverhez a pymssql Python driverrel vagy a SQL Server ODBC driverrel. Támogatja a jelszó-alapú hitelesítést DSN-es vagy DSN nélküli beállításokkal.
image: /assets/logo_square.png
---


# Forráscsatlakozó MS SQL Serverhez

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t SQL Serverhez való csatlakozáshoz a natív Python-illesztő vagy az ODBC driver használatával.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `pymssql`  
**Támogatott hitelesítés:** Csak jelszó-alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC illesztőt.

### *digna* konfiguráció (natív illesztő)

Adja meg a következő adatokat a **"Create a Database Connection"** képernyőn:

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

Az ODBC driver szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész a jelszó-alapú hitelesítésre fókuszál a **SQL Server** driver használatával.

### 1. Telepítse az ODBC drivert

Telepítse a **SQL Server** (vagy hasonló) drivert a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó-alapú hitelesítéssel:

#### Lépés 1
![Lépés 1](images/sqlserver/create_odbc_data_source_step1.png)

Kattintson a **Next >** gombra.

#### Lépés 2
![Lépés 2](images/sqlserver/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módot (pl. felhasználónév és jelszó),
és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### Lépés 3
![Lépés 3](images/sqlserver/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### Lépés 4
![Lépés 4](images/sqlserver/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy szükség szerint válasszon naplózási opciókat,
majd kattintson a **Finish** gombra.

#### Lépés 5
![Lépés 5](images/sqlserver/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### Lépés 6
![Lépés 6](images/sqlserver/create_odbc_data_source_step6.png)

Amikor megjelenik a siker képernyő, az ODBC megfelelően konfigurálva van.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN nélküli** beállítással.

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

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC driver konfigurációjában definiált névvel.

---

### B. DSN nélküli konfiguráció

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