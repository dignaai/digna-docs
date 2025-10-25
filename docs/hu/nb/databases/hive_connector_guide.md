---
title: Apache Hive Connector – Adatbázis-integráció | digna-dokumentáció
description: Állítsd be a digna-t Apache Hive-hoz való csatlakozáshoz a beépített PyHive-illesztő vagy a Cloudera ODBC-illesztő használatával. Támogatja a jelszó alapú hitelesítést és DSN vagy DSN-less konfigurációt.
image: /assets/logo_square.png
---


# Forráskapcsolat Hive-hoz

Ez az útmutató bemutatja, hogyan konfiguráld a *digna*-t Hive-hoz úgy, hogy vagy a natív Python-kapcsolót, vagy az ODBC-illesztőt használod.

A képernyőre hivatkozik: **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `PyHive`  
**Támogatott hitelesítési módok:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módokhoz használd az ODBC-illesztőt.

### *digna*-konfiguráció (natív illesztő)

Add meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Apache Hive
Host Address:    Szervernév vagy IP-cím
Host Port:       Portszám, pl. 10000
Database Name:   A sémá, amely tartalmazza a forrásadatokat
Schema Name:     A sémá, amely tartalmazza a forrásadatokat
User Name:       Az adatbázis felhasználóneve
User Password:   A felhasználó jelszava
Use ODBC:        Disabled (default)
```

---

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre koncentrál a **Cloudera ODBC Driver for Apache Hive** használatával.

### 1. Telepítsd az ODBC-illesztőt

Telepítsd a **Cloudera ODBC Driver for Apache Hive** (vagy az egyenértékű) illesztőt a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfiguráld az ODBC-adatforrást

Kövesd az alábbi lépéseket egy új ODBC-adatforrás konfigurálásához jelszó alapú hitelesítéssel:

#### 1. lépés
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### 2. lépés – Teszteld a kapcsolatot

Add meg a jelszót, majd kattints a **Test** gombra.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Sikeres teszt után kattints az **OK** gombra.

---

Most konfigurálhatod a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-less** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna*-konfiguráció

A **"Create a Database Connection"** képernyőn add meg a következőket:

```
Technology:      Apache Hive
Database Name:   A séma, amely tartalmazza a forrásadatokat (ugyanaz, mint a Schema Name)
Schema Name:     A séma, amely tartalmazza a forrásadatokat
Use ODBC:        Enabled
```

#### ODBC-tulajdonságok

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{a jelszavad kapcsos zárójelek között}"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN-less konfiguráció

#### *digna*-konfiguráció

A **"Create a Database Connection"** képernyőn add meg a következőket:

```
Technology:      Apache Hive
Database Name:   A séma, amely tartalmazza a forrásadatokat (ugyanaz, mint a Schema Name)
Schema Name:     A séma, amely tartalmazza a forrásadatokat
Use ODBC:        Enabled
```

#### ODBC-tulajdonságok

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "a szerverneved vagy IP-címed"
name: "PORT",       value: "Portszám, pl. 10000"
name: "Schema",     value: "A séma, amely tartalmazza a forrásadatokat"
name: "UID",        value: "a hive felhasználóneved"
name: "PWD",        value: "a hive jelszavad"
name: "AuthMech",   value: "3"
```