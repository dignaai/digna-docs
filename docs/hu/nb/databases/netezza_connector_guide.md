---
title: Netezza-kapcsolat – Adatbázis-integráció | digna-dokumentáció
description: Állítsa be a digna-t, hogy Netezza-hez csatlakozzon a NetezzaSQL ODBC-illesztő használatával. Támogatja a jelszalapú hitelesítést DSN vagy DSN-less beállítással a rugalmas csatlakozás érdekében.
image: /assets/logo_square.png
---


# Forráskapcsoló Netezza-hez

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Netezza-hez való csatlakozáshoz az ODBC-illesztő használatával.

Ez a képernyőre hivatkozik: **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC-illesztő

Az ODBC-illesztő különböző hitelesítési és csatlakozási opciókat támogathat. Ez a szakasz a jelszalapú hitelesítésre koncentrál a **NetezzaSQL** illesztő használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse a **NetezzaSQL** (vagy azzal egyenértékű) illesztőt az beszállító hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás jelszalapú hitelesítéssel történő konfigurálásához:

#### Lépés 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

A Netezza-illesztőjétől, a beállítástól és a biztonsági követelményektől függően előfordulhat, hogy az **Advanced DSN Options**, **SSL DSN Options** vagy **Driver Options** lapokon is meg kell adnia adatokat. A legegyszerűbb beállításhoz elegendő az **DSN Options** mezők kitöltése.

Kattintson a **Test Connection** gombra.

#### Lépés 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Ha sikerüzenetet kap, az ODBC helyesen van konfigurálva.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**, akár **DSN-less** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-tulajdonságok

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 A `DSN`-nek meg kell egyeznie azzal a névvel, amelyet az ODBC-illesztő konfigurációjában definiált.

---

### B. DSN-less konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-tulajdonságok

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```