---
title: Teradata Connector – Adatbázis-integráció | digna dokumentáció
description: Állítsa be a digna-t Teradata-hoz való csatlakozáshoz a teradatasql Python driver vagy a Teradata ODBC driver használatával. Támogatja a jelszavas hitelesítést DSN-es és DSN nélküli beállításokkal.
image: /assets/logo_square.png
---


# Teradata forráskapcsoló

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Teradata-hoz való csatlakozáshoz, vagy a natív Python csatlakozót, vagy az ODBC drivert használva.

A leírás a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python driver

**Library:** `teradatasql`  
**Támogatott hitelesítés:** csak jelszavas hitelesítés

> Más hitelesítési módszerek esetén kérjük, használja az ODBC drivert.

### *digna* konfiguráció (natív driver)

Adja meg a következő adatokat a **"Create a Database Connection"** képernyőn:

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

## ODBC driver

Az ODBC driver szélesebb körű hitelesítési és csatlakozási lehetőségeket támogathat. Ez a rész a jelszavas hitelesítést ismerteti a **Teradata Database ODBC Driver 20.00** driver használatával.

### 1. Telepítse az ODBC drájvert

Telepítse a **Teradata Database ODBC Driver 20.00** (vagy hasonló) drivert a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszavas hitelesítéssel:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Kattintson a **Test** gombra.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Adja meg a felhasználónevet és a jelszót.

Kattintson az **OK** gombra.
Amikor megjelenik a sikerességet jelző képernyő, az ODBC megfelelően konfigurálva van.

---

Most már konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> A `DSN`-nek meg kell egyeznie az ODBC driver konfigurációjában definiált névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```