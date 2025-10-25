---
title: Oracle-kapcsolat – Adatbázis-integráció | digna-dokumentáció
description: Konfigurálja a digna-t Oracle-hez való csatlakozáshoz a python-oracledb-vezérlő vagy az Oracle ODBC-vezérlő használatával. Támogatja a jelszalapú hitelesítést DSN-es vagy DSN-nélküli beállítással.
image: /assets/logo_square.png
---


# Oracle forráskapcsoló

Ez az útmutató bemutatja, hogyan konfigurálja a *digna*-t Oracle DB-hez való csatlakozáshoz, akár a natív Python-csatolóval, akár az ODBC-vezérlővel.

A bemutatott képernyő a **"Create a Database Connection"**.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python-driver

**Library:** `python-oracledb`  
**Támogatott hitelesítés:** Csak jelszalapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez használja az ODBC-drivert.

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

## ODBC-driver

Az ODBC-driver szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a jelszalapú hitelesítésre összpontosít az **Oracle in OraDB21Home1** vezérlő használatával.

### 1. Telepítse az ODBC-drivert

Telepítse az **Oracle in OraDB21Home1** (vagy hasonló) vezérlőt a szállító hivatalos telepítési útmutatójának megfelelően.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás konfigurálásához jelszalapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/oracle/create_odbc_data_source_step1.png)

Megjegyzés:
A TNS Service Name-t a tnsnames.ora fájlban kell konfigurálni az Oracle kliens telepítésében. Itt adja meg a kapcsolat leírását (host, port, service name).

#### 2. lépés – Kapcsolat tesztelése

Kattintson a **Test Connection** gombra.

![2. lépés](images/oracle/create_odbc_data_source_step2.png)

Adja meg a jelszót, majd kattintson az **OK** gombra.

![2. lépés](images/oracle/create_odbc_data_source_step3.png)

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**-nel, akár egy **DSN-nélküli** beállítással.

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

> 🔹 `DSN`-nek meg kell egyeznie a nevvel, amelyet az ODBC-driver konfigurációjában definiált.

---

### B. DSN-nélküli beállítás

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