---
title: Oracle csatlakozó – Adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t az Oracle-hez való csatlakozáshoz a python-oracledb vagy az Oracle ODBC illesztő segítségével. Támogatott a jelszalapú hitelesítés DSN-nel vagy DSN nélkül.
image: /assets/logo_square.png
---


# Oracle forráscsatlakozó

Ez az útmutató leírja, hogyan állítsa be a *digna*-t Oracle DB-hez való csatlakozáshoz, natív Python-csatlakozóval vagy ODBC-illesztővel.

Ez a **"Create a Database Connection"** képernyőre vonatkozik.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `python-oracledb`  
**Támogatott hitelesítés:** csak jelszalapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez használja az ODBC-illesztőt.

### Konfiguráció *digna*-hoz (natív illesztő)

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

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ebben a részben a jelszalapú hitelesítésre koncentrálunk, a **Oracle in OraDB21Home1** illesztő használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse az **Oracle in OraDB21Home1** (vagy hasonlót) a beszállító hivatalos útmutatása szerint.

### 2. Állítsa be az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás jelszalapú hitelesítéssel történő beállításához:

#### 1. lépés
![1. lépés](images/oracle/create_odbc_data_source_step1.png)

Megjegyzés:
A TNS Service Name-t a Oracle kliens telepítésének tnsnames.ora fájljában kell konfigurálni. Itt adja meg a csatlakozási leírást (host, port, service name).

#### 2. lépés – Kapcsolat tesztelése

Kattintson a **Test Connection** gombra.

![2. lépés](images/oracle/create_odbc_data_source_step2.png)

Adja meg a jelszót, majd kattintson az **OK** gombra.

![2. lépés](images/oracle/create_odbc_data_source_step3.png)

---

Most beállíthatja a *digna*-t ODBC-csatlakozás használatára, vagy **DSN (Data Source Name)** segítségével, vagy **DSN nélküli** konfigurációban.

---

### A. DSN-alapú konfiguráció

#### Konfiguráció *digna*-hoz

A **"Create a Database Connection"** képernyőn adja meg a következőt:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 A `DSN` értékének meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### Konfiguráció *digna*-hoz

A **"Create a Database Connection"** képernyőn adja meg a következőt:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```