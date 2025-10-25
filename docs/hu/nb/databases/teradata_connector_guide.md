---
title: Teradata-kapcsolat – Adatbázis-integráció | digna-dokumentáció
description: Konfigurálja a digna-t Teradata-hoz való csatlakozáshoz a teradatasql Python-illesztő vagy a Teradata ODBC-illesztő használatával. Támogatja a jelszalapú hitelesítést DSN-sel vagy DSN-nélküli beállítással.
image: /assets/logo_square.png
---


# Forráscsatlakozó Teradata-hoz

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t Teradata-hoz való kapcsolódáshoz a natív Python-csatolóval vagy ODBC-illesztővel.

A **"Új adatbázis-kapcsolat létrehozása"** képernyőre hivatkozik.

![Új adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Natív Python-illesztő

**Library:** `teradatasql`  
**Támogatott hitelesítés:** Csak jelszalapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez használja az ODBC-illesztőt.

### *digna* konfiguráció (natív illesztő)

Adja meg a következő információkat az **"Új adatbázis-kapcsolat létrehozása"** képernyőn:

```
Technology:      Teradata
Host Address:    Szerver neve vagy IP-címe
Host Port:       Port száma, pl. 1025
Database Name:   Adatbázis neve
Schema Name:     Séma neve
User Name:       Felhasználónév
User Password:   Felhasználó jelszava
Use ODBC:        Disabled (alapértelmezett)
```

---

## ODBC-illesztő

Az ODBC-illesztő szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész a jelszalapú hitelesítésre fókuszál a **Teradata Database ODBC Driver 20.00** illesztő használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse a **Teradata Database ODBC Driver 20.00** (vagy ekvivalens) illesztőt a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás konfigurálásához jelszalapú hitelesítéssel:

#### 1. lépés
![1. lépés](images/teradata/create_odbc_data_source_step1.png)

Kattintson a **Teszt** gombra.

#### 2. lépés
![2. lépés](images/teradata/create_odbc_data_source_step2.png)

Adja meg a felhasználónevet és a jelszót.

Kattintson az **OK** gombra. Ha sikerüzenetet kap, az ODBC helyesen van konfigurálva.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)**-nel, akár **DSN-nélküli** beállítással.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

Az **"Új adatbázis-kapcsolat létrehozása"** képernyőn adja meg a következőket:

```
Technology:      Teradata
Database Name:   Az az adatbázis, amely a forrás sémát tartalmazza
Schema Name:     A séma, amely a forrásadatokat tartalmazza
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "adatbázis felhasználója"
name: "PWD",        value: "adatbázis jelszava"
```

> 🔹 `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában meghatározott névvel.

---

### B. DSN-nélküli konfiguráció

#### *digna* konfiguráció

Az **"Új adatbázis-kapcsolat létrehozása"** képernyőn adja meg a következőket:

```
Technology:      Teradata
Database Name:   A séma, amely a forrásadatokat tartalmazza (ugyanaz, mint a Schema Name)
Schema Name:     A séma, amely a forrásadatokat tartalmazza
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "szerver neve vagy IP-cím"
name: "UID",        value: "adatbázis felhasználója"
name: "PWD",        value: "adatbázis jelszava"
```