---
title: Oracle csatlakozó – Adatbázis-integráció | digna dokumentáció
description: Konfigurálja a digna-t Oracle-hez a python-oracledb illesztő vagy az Oracle ODBC-illesztő használatával. Támogatja a jelszó alapú hitelesítést DSN vagy DSN nélküli beállításokkal.
image: /assets/logo_square.png
---


# Oracle forráscsatlakozó

Ez az útmutató elmagyarázza, hogyan csatlakoztassa a *digna*-t egy Oracle adatbázishoz natív Python-illesztő vagy ODBC-illesztő használatával.

Ez a **"Create a Database Connection"** képernyőre utal.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Helyi Python-illesztő

**Könyvtár:** `python-oracledb`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Egyéb hitelesítési módszerekhez kérjük, használja az ODBC-illesztőt.

### *digna* konfiguráció (helyi illesztő)

A **"Create a Database Connection"** képernyőn adja meg a következő adatokat:

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

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész az Oracle in OraDB21Home1 illesztőt használva a jelszó alapú hitelesítésre összpontosít.

### 1. Az ODBC-illesztő telepítése

Telepítse az Oracle in OraDB21Home1 (vagy hasonló) illesztőt a gyártó hivatalos telepítési útmutatóját követve.

### 2. ODBC adatforrás konfigurálása

A jelszó alapú hitelesítést használó új ODBC adatforrás konfigurálásához kövesse az alábbi lépéseket:

#### 1. lépés
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Megjegyzés:
A TNS Service Name-t az Oracle kliens telepítésének tnsnames.ora fájljában kell konfigurálni. Itt adja meg a csatlakozási azonosítót (host, port, service name).

#### 2. lépés – Kapcsolat tesztelése

Kattintson a **Test Connection** gombra.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Adja meg a jelszót, majd kattintson az **OK** gombra.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Most már beállíthatja a *digna*-t ODBC-kapcsolat használatára akár DSN (Data Source Name) alapú, akár DSN nélküli konfigurációval.

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

#### ODBC tulajdonságok

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

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