---
title: Netezza-connector – Adatbázis-integráció | digna Dokumentáció
description: Állítsa be a digna-t, hogy csatlakozzon a Netezza-hez a NetezzaSQL ODBC-illesztőprogramon keresztül. Jelszavas hitelesítés támogatott DSN-nel vagy DSN nélküli módban a rugalmas csatlakozáshoz.
image: /assets/logo_square.png
---


# Netezza forrás csatlakoztatása

Ez az útmutató leírja, hogyan állítsa be a *digna*-t Netezza-hez való csatlakozáshoz ODBC-illesztőprogram használatával.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC-illesztőprogram

Az ODBC-illesztőprogram különböző hitelesítési és csatlakozási lehetőségeket támogathat. Ebben a részben a jelszavas hitelesítést tárgyaljuk a **NetezzaSQL** illesztőprogrammal.

### 1. Telepítse az ODBC-illesztőprogramot

Telepítse a **NetezzaSQL** (vagy hasonló) illesztőprogramot a gyártó hivatalos útmutatójának megfelelően.

### 2. Állítson be egy ODBC adatforrást

Végezze el az alábbi lépéseket egy új ODBC adatforrás jelszavas hitelesítéssel történő beállításához:

#### 1. lépés
![Step 1](images/netezza/create_odbc_data_source_step1.png)

A Netezza-illesztőprogramtól, a beállítási és biztonsági követelményektől függően előfordulhat, hogy meg kell adnia adatokat az olyan füleken, mint a **Advanced DSN Options**, **SSL DSN Options** vagy **Driver Options**. A legegyszerűbb beállításhoz elegendő a **DSN Options** fülön megadni az adatokat.

Kattintson a **Test Connection** gombra.

#### 2. lépés
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Ha megjelenik a siker képernyő, az ODBC helyesen van beállítva.

---

Most beállíthatja a *digna*-t az ODBC-kapcsolat használatára — vagy **DSN (Data Source Name)** segítségével, vagy **DSN-less** módban.

---

### A. DSN-alapú konfiguráció

#### *digna* konfigurációja

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN`-nek meg kell egyeznie az ODBC-illesztőprogram konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció (DSN-less)

#### *digna* konfigurációja

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```