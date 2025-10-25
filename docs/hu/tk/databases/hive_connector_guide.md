---
title: Apache Hive Csatoló – Adatbázis-integráció | digna Dokumentációja
description: A digna beállítása Apache Hive-hoz történő csatlakozáshoz helyi PyHive illesztő vagy Cloudera ODBC illesztő használatával. Támogatja a jelszó-alapú hitelesítést és a DSN-es vagy DSN nélküli konfigurációkat.
image: /assets/logo_square.png
---


# Hive forráscsatlakozó

Ez az útmutató ismerteti, hogyan állítható be a *digna*, hogy Hive-hoz csatlakozzon helyi Python-csatlakozón (PyHive) vagy ODBC-illesztőn keresztül.

Bu, **"Create a Database Connection"** képernyőre utal.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Helyi Python illesztő

**Könyvtár:** `PyHive`  
**Támogatott hitelesítés:** Csak jelszó-alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőt.

### *digna* konfigurációja (helyi illesztő)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Apache Hive
Host Address:    Szervernév vagy IP-cím
Host Port:       Portszám, pl. 10000
Database Name:   A forrásadatokat tartalmazó séma
Schema Name:     A forrásadatokat tartalmazó séma
User Name:       Adatbázis felhasználónév
User Password:   Felhasználó jelszava
Use ODBC:        Letiltva (alapértelmezett)
```

---

## ODBC illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész a jelszó-alapú hitelesítésre összpontosít a **Cloudera ODBC Driver for Apache Hive** illesztő használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse a **Cloudera ODBC Driver for Apache Hive** (vagy hasonló) illesztőt a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó-alapú hitelesítéssel:

#### 1. lépés
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### 2. lépés – Tesztelje a kapcsolatot

Adja meg a jelszót, majd kattintson a **Test** gombra.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Sikeres teszt esetén kattintson az **OK** gombra.

---

Most beállíthatja a *digna*-t, hogy ODBC-kapcsolatot használjon: vagy **DSN (Data Source Name)** alapú konfigurációval, vagy **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfigurációja

Adja meg a következőket a **"Create a Database Connection"** képernyőn:

```
Technology:      Apache Hive
Database Name:   A forrásadatokat tartalmazó séma (megegyezik a Schema Name-nel)
Schema Name:     A forrásadatokat tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{a jelszava kapcsos zárójelek között}"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában definiált névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfigurációja

Adja meg a következőket a **"Create a Database Connection"** képernyőn:

```
Technology:      Apache Hive
Database Name:   A forrásadatokat tartalmazó séma (megegyezik a Schema Name-nel)
Schema Name:     A forrásadatokat tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "szerver neve vagy IP-címe"
name: "PORT",       value: "Portszám, pl. 10000"
name: "Schema",     value: "A forrásadatokat tartalmazó séma"
name: "UID",        value: "A Hive felhasználó"
name: "PWD",        value: "A Hive jelszava"
name: "AuthMech",   value: "3"
```