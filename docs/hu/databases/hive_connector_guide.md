---
title: Apache Hive Connector – Adatbázis-integráció | digna dokumentáció
description: Konfigurálja a digna-t az Apache Hive-hoz való csatlakozáshoz a natív PyHive driver vagy a Cloudera ODBC driver használatával. Támogatja a jelszó alapú hitelesítést, valamint DSN-es és DSN-nélküli beállításokat.
image: /assets/logo_square.png
---


# Hive forráskapcsoló

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t, hogy Hive-hoz csatlakozzon vagy a natív Python-illesztővel, vagy az ODBC driverrel.

Ez a következő képernyőre hivatkozik: **"Adatbázis-kapcsolat létrehozása"**.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python driver

**Library:** `PyHive`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> Más hitelesítési módszerekhez kérjük, használja az ODBC drivert.

### *digna* konfiguráció (natív illesztő)

Adja meg a következő információkat az **"Adatbázis-kapcsolat létrehozása"** képernyőn:

```
Technology:      Apache Hive
Host Address:    Szerver neve vagy IP-címe
Host Port:       Port száma, pl. 10000
Database Name:   A forrásadatokat tartalmazó séma
Schema Name:     A forrásadatokat tartalmazó séma
User Name:       Adatbázis felhasználónév
User Password:   A felhasználó jelszava
Use ODBC:        Disabled (alapértelmezett)
```

---

## ODBC driver

Az ODBC driver szélesebb körű hitelesítési és csatlakozási opciókat támogathat. Ez a rész a jelszó alapú hitelesítésre fókuszál a **Cloudera ODBC Driver for Apache Hive** driver használatával.

### 1. Az ODBC driver telepítése

Telepítse a **Cloudera ODBC Driver for Apache Hive**-t (vagy hasonlót) a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Az ODBC adatforrás beállítása

Kövesse az alábbi lépéseket, hogy új ODBC adatforrást konfiguráljon jelszó alapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/hive/create_odbc_data_source_step1.png)


#### 2. lépés – A kapcsolat tesztelése

Adja meg a jelszót, majd kattintson a **Test** gombra.

![2. lépés](images/hive/create_odbc_data_source_step2.png)

Sikeres teszt után kattintson az **OK** gombra.

---

Most konfigurálhatja a *digna*-t, hogy ODBC kapcsolatot használjon, akár **DSN (Data Source Name)**-nel, akár **DSN-nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

Az **"Adatbázis-kapcsolat létrehozása"** képernyőn adja meg a következőket:

```
Technology:      Apache Hive
Database Name:   A forrásadatokat tartalmazó séma (ugyanaz, mint a Schema Name)
Schema Name:     A forrásadatokat tartalmazó séma
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{a jelszavát kapcsos zárójelek között}"
```

> A `DSN`-nek meg kell egyeznie az ODBC driver konfigurációjában megadott névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

Az **"Adatbázis-kapcsolat létrehozása"** képernyőn adja meg a következőket:

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
name: "PORT",       value: "Port száma, pl. 10000"
name: "Schema",     value: "A forrásadatokat tartalmazó séma"
name: "UID",        value: "a hive felhasználója'
name: "PWD",        value: "a hive jelszava"
name: "AuthMech",   value: "3"
```