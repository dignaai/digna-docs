---
title: Oracle Csatlakozó – Adatbázis-integráció | digna Dokumentáció
description: Konfigurálja a digna-t, hogy Oracle-hoz csatlakozzon a python-oracledb driverrel vagy az Oracle ODBC driverrel. Támogatja a jelszó alapú hitelesítést DSN-es és DSN-less beállításokkal.
image: /assets/logo_square.png
---


# Oracle forráscsatlakozó

Ez az útmutató bemutatja, hogyan konfigurálható a *digna*, hogy Oracle DB-hez csatlakozzon a natív Python-illesztőprogram vagy az ODBC driver használatával.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Library:** `python-oracledb`  
**Támogatott hitelesítés:** csak jelszó alapú hitelesítés

> Más hitelesítési módszerekhez kérjük, használja az ODBC drivert.

### *digna* konfiguráció (natív driver)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Az ODBC driver szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre összpontosít az Oracle in OraDB21Home1 driverrel.

### 1. Az ODBC-illesztőprogram telepítése

Telepítse az **Oracle in OraDB21Home1** (vagy hasonló) illesztőprogramot a gyártó hivatalos telepítési útmutatóját követve.

### 2. Az ODBC adatforrás konfigurálása

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéssel:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Megjegyzés:
A TNS Service Name-t a tnsnames.ora fájlban kell beállítani az Oracle kliens telepítésében. Itt adja meg a kapcsolatleíró paramétereket (host, port, service name).

#### Step 2 – Test the connection

Kattintson a **Test Connection** gombra.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Adja meg a jelszót, majd kattintson az **OK** gombra.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Most már konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-less** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> A `DSN`-nek meg kell egyeznie az ODBC illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```