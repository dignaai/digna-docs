---
title: Teradata-csatoló – Adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t úgy, hogy teradatasql Python-illesztő vagy Teradata ODBC-illesztő használatával csatlakozzon Teradata-hoz. Támogatja a jelszó alapú hitelesítést DSN-es és DSN nélküli telepítésekkel.
image: /assets/logo_square.png
---


# Teradata forráscsatoló

Ez az útmutató elmagyarázza, hogyan konfigurálható a *digna* Teradata-hoz való csatlakoztatása helyi Python-illesztő vagy ODBC-illesztő használatával.

A továbbiakban a **„Adatbázis kapcsolat létrehozása”** képernyőre hivatkozunk.

![Egy adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Helyi Python-illesztő

**Könyvtár:** `teradatasql`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőt.

### *digna* konfiguráció (helyi illesztő)

A **„Adatbázis kapcsolat létrehozása”** képernyőn adja meg a következőket:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre összpontosít, a **Teradata Database ODBC Driver 20.00** illesztő használatával.

### 1. ODBC-illesztő telepítése

Telepítse a **Teradata Database ODBC Driver 20.00** (vagy hasonló) illesztőt a gyártó hivatalos telepítési útmutatóját követve.

### 2. ODBC-adatforrás konfigurálása

Kövesse az alábbi lépéseket egy új ODBC-adatforrás beállításához jelszó alapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/teradata/create_odbc_data_source_step1.png)

Kattintson a Test gombra.

#### 2. lépés
![2. lépés](images/teradata/create_odbc_data_source_step2.png)

Adja meg a felhasználónevet és a jelszót.

Kattintson az OK gombra. Ha sikeres üzenetet kap, az ODBC helyesen van konfigurálva.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (adatforrás-név)**-nel, akár **DSN nélküli** telepítéssel.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **„Adatbázis kapcsolat létrehozása”** képernyőn adja meg a következőket:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **„Adatbázis kapcsolat létrehozása”** képernyőn adja meg a következőket:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```