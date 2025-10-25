---
title: Apache Hive csatlakozó – Adatbázis integráció | digna dokumentáció
description: Állítsa be a *digna*-t Apache Hive-hoz való csatlakozásra a natív PyHive driverrel vagy a Cloudera ODBC driverrel. Támogatja a jelszó alapú hitelesítést és DSN-es vagy DSN-nélküli konfigurációkat.
image: /assets/logo_square.png
---


# Hive forrás csatlakozó

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Hive-hoz való csatlakozásra a natív Python-kapcsolóval vagy az ODBC-illesztővel.

A leírás a **"Create a Database Connection"** képernyőre hivatkozik.

![Hozzon létre egy adatbázis-kapcsolatot](images/data_source_config_input_mask.png)

---

## Natív Python driver

**Könyvtár:** `PyHive`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőt.

### *digna* konfiguráció (natív driver)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      Apache Hive
Host Address:    Szerver neve vagy IP-címe
Host Port:       Portszám, pl. 10000
Database Name:   A forrásadatokat tartalmazó séma
Schema Name:     A forrásadatokat tartalmazó séma
User Name:       Adatbázis felhasználónév
User Password:   A felhasználó jelszava
Use ODBC:        Disabled (default)
```

---

## ODBC driver

Az ODBC-illesztő szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre összpontosít a **Cloudera ODBC Driver for Apache Hive** használatával.

### 1. Az ODBC-illesztő telepítése

Telepítse a **Cloudera ODBC Driver for Apache Hive** (vagy hasonlót) a gyártó hivatalos telepítési útmutatója szerint.

### 2. Az ODBC adatforrás konfigurálása

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/hive/create_odbc_data_source_step1.png)


#### 2. lépés – A kapcsolat tesztelése

Adja meg a jelszót, majd kattintson a **Teszt** gombra.

![2. lépés](images/hive/create_odbc_data_source_step2.png)

Sikeres teszt után kattintson az **OK** gombra.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Apache Hive
Database Name:   A forrásadatokat tartalmazó séma (ugyanaz, mint a Schema Name)
Schema Name:     A forrásadatokat tartalmazó séma
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{a jelszavad kapcsos zárójelek között}"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Apache Hive
Database Name:   A forrásadatokat tartalmazó séma (ugyanaz, mint a Schema Name)
Schema Name:     A forrásadatokat tartalmazó séma
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "a szerver neve vagy IP-címe"
name: "PORT",       value: "Portszám, pl. 10000"
name: "Schema",     value: "A forrásadatokat tartalmazó séma"
name: "UID",        value: "a hive felhasználója'
name: "PWD",        value: "a hive jelszava"
name: "AuthMech",   value: "3"
```