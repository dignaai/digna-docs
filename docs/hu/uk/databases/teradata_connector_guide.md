---
title: Teradata Connector – adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t a Teradata-hoz való csatlakozáshoz a teradatasql Python-illesztővel vagy a Teradata ODBC-illesztővel. A jelszalapú hitelesítés támogatott DSN-es és DSN nélküli konfigurációkban.
image: /assets/logo_square.png
---


# Teradata forráskapcsoló

Ez az útmutató bemutatja, hogyan állítsa be a *digna*-t Teradata-hoz való csatlakozáshoz natív Python-illesztővel vagy ODBC-meghajtóval.

A útmutató a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `teradatasql`  
**Támogatott hitelesítés:** csak jelszalapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez használja az ODBC-illesztőt.

### A *digna* beállítása (natív illesztő)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

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

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ebben a részben a jelszalapú hitelesítést tárgyaljuk a **Teradata Database ODBC Driver 20.00** illesztő használatával.

### 1. ODBC-illesztő telepítése

Telepítse a **Teradata Database ODBC Driver 20.00** (vagy hasonló) illesztőt a gyártó hivatalos telepítési útmutatója szerint.

### 2. ODBC adatforrás beállítása

Kövesse az alábbi lépéseket egy új ODBC adatforrás jelszalapú hitelesítéssel történő beállításához:

#### 1. lépés
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Kattintson a **Test** gombra.

#### 2. lépés
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Adja meg a felhasználónevet és a jelszót.

Kattintson az **OK** gombra. Ha megjelenik a sikeres beállítást jelző képernyő, az ODBC megfelelően van konfigurálva.

---

Most beállíthatja a *digna*-t az ODBC-kapcsolat használatához — akár **DSN (Data Source Name)** használatával, akár DSN nélküli (DSN-less) konfigurációban.

---

### A. DSN-alapú konfiguráció

#### A *digna* beállítása

A **"Create a Database Connection"** képernyőn adja meg a következőket:

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

> 🔹 A `DSN` értékének meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció (DSN-less)

#### A *digna* beállítása

A **"Create a Database Connection"** képernyőn adja meg a következőket:

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