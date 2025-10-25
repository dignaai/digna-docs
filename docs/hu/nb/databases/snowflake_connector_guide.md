---
title: Snowflake Connector – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Snowflake csatlakoztatásához natív Python-connectorral vagy a Snowflake ODBC-illesztőprogrammal. Támogatja a jelszó alapú hitelesítést DSN-es vagy DSN nélküli beállítással.
image: /assets/logo_square.png
---


# Snowflake forráscsatlakozó

Ez az útmutató leírja, hogyan konfiguráld a *digna*-t, hogy csatlakozzon a Snowflake-hez a natív Python-connector vagy az ODBC-illesztőprogram használatával.

A útmutató a **"Create a Database Connection"** képernyőre hivatkozik.

![Hozzon létre egy adatbázis-kapcsolatot](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `snowflake-connector-python`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használd az ODBC-illesztőprogramot.

### *digna*-konfiguráció (natív illesztő)

Add meg a következő adatokat a **"Create a Database Connection"** képernyőn:

```
Technológia:        Snowflake
Szervercím:         Snowflake-fióknév
Szerverport:        Nem szükséges
Adatbázisnév:       Az adatbázis, amely tartalmazza a forrássémát
Séma neve:          A séma, amely tartalmazza a forrásadatokat
Felhasználónév:     Felhasználónév és warehouse formátumban: "user<@>warehouse"
Felhasználói jelszó: A felhasználó jelszava
ODBC használata:    Kikapcsolva (alapértelmezett)
```

---

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a jelszó alapú hitelesítésre és a **SnowflakeDSIIDriver** használatára összpontosít.

### 1. Telepítse az ODBC-illesztőt

Telepítse a **SnowflakeDSIIDriver**-t a gyártó hivatalos telepítési útmutatója szerint.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás jelszó alapú hitelesítésű konfigurálásához:

#### 1. lépés
![1. lépés](images/snowflake/create_odbc_data_source_step1.png)

Megjegyzés:
- Ha nem ad meg értékeket a "Database", "Schema" és "Warehouse" mezőkhöz, akkor azokat az ODBC-tulajdonságok között kell megadnia a *digna* adatforrás-konfigurációban.
- A "Server" értéke a Snowflake-fiókneve, amelyet a ".snowflakecomputing.com" követ.

#### 2. lépés – Kapcsolat tesztelése

Kattintson a **TEST** gombra. A sikeres kapcsolat így néz ki:

![2. lépés](images/snowflake/create_odbc_data_source_step2.png)

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár egy **DSN (Data Source Name)**-nel, akár egy **DSN nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna*-konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technológia:        Snowflake
Adatbázisnév:       Az adatbázis, amely tartalmazza a forrássémát
Séma neve:          A séma, amely tartalmazza a forrásadatokat
ODBC használata:    Engedélyezve
```

#### ODBC-tulajdonságok

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{a jelszavad kapcsos zárójelek között}"

opcionális:
name: "Database",       value: "Az adatbázis, amely tartalmazza a forrássémát"
name: "Schema",         value: "A séma, amely tartalmazza a forrásadatokat"
name: "Warehouse",      value: "A Warehouse, amelyet az SQL-ek futtatásához használni kell"
```

> 🔹 `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna*-konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technológia:        Snowflake
Adatbázisnév:       A séma, amely tartalmazza a forrásadatokat (megegyezik a Séma nevével)
Séma neve:          A séma, amely tartalmazza a forrásadatokat
ODBC használata:    Engedélyezve
```

#### ODBC-tulajdonságok

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com"
name: "UID",        value: "az Ön Snowflake felhasználója"
name: "PWD",        value: "az Ön Snowflake jelszava"
name: "Database",   value: "Az adatbázis, amely tartalmazza a forrássémát"
name: "Schema",     value: "A séma, amely tartalmazza a forrásadatokat"
name: "Warehouse",  value: "A Warehouse, amelyet az SQL-ek futtatásához használni kell"
```