---
title: PostgreSQL Csatlakozó – Adatbázis Integráció | digna Dokumentáció
description: Leírja, hogyan kell a digna-t a psycopg Python-illesztőprogrammal vagy a PostgreSQL ODBC-vezérlővel konfigurálni PostgreSQL-hez való kapcsolódáshoz. Támogatja a jelszó alapú hitelesítést DSN-nel vagy DSN nélkül.
image: /assets/logo_square.png
---


# PostgreSQL Forráscsatlakozó

Ez az útmutató ismerteti, hogyan konfigurálja a *digna*-t úgy, hogy helyi Python-illesztőprogramot vagy ODBC-vezérlőt használva csatlakozzon Postgres-hez.

Ez az **„Adatbázis-kapcsolat létrehozása”** képernyőre vonatkozik.

![Adatbázis-kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Helyi Python-illesztőprogram

**Könyvtár:** `psycopg`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-vezérlőt.

### *digna* konfigurációja (helyi illesztőprogram)

Az **„Adatbázis-kapcsolat létrehozása”** képernyőn adja meg a következő adatokat:

```
Technology:      Postgres
Host Address:    Szerver neve vagy IP-címe
Host Port:       Port szám, pl. 5432
Database Name:   Adatbázis neve
Schema Name:     A forrásadatot tartalmazó séma
User Name:       Adatbázis felhasználónév
User Password:   Felhasználói jelszó
Use ODBC:        Kikapcsolva (alapértelmezett)
```

---

## ODBC-vezérlő

Az ODBC-vezérlő szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a jelszó alapú hitelesítésre fókuszál, a **PostgreSQL Unicode(x64)** vezérlő használatával.

### 1. Telepítse az ODBC-vezérlőt

Kövesse a gyártó hivatalos telepítési útmutatóját a **PostgreSQL Unicode(x64)** (vagy hasonló) vezérlő telepítéséhez.

### 2. Konfigurálja az ODBC adatforrást

Új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéssel kövesse az alábbi lépéseket:

#### 1. lépés
![Adım 1](images/postgres/create_odbc_data_source_step1.png)

Megjegyzés: Ha az adatbázis konfigurációja megkövetel egy adott "SSLMode" beállítást, győződjön meg róla, hogy azt a DSN nélküli konfiguráció megadásakor is használja.

#### 2. lépés – Kapcsolat tesztelése

Kattintson a **Kapcsolat tesztelése** gombra.

![Adım 2](images/postgres/create_odbc_data_source_step2.png)

---

Most már konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár egy **DSN (Adatforrás-név)** segítségével, akár **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfigurációja

Az **„Adatbázis-kapcsolat létrehozása”** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   A forrássémát tartalmazó adatbázis
Schema Name:     A forrásadatot tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN`-nek meg kell egyeznie az ODBC-vezérlő konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfigurációja

Az **„Adatbázis-kapcsolat létrehozása”** képernyőn adja meg a következőket:

```
Technology:      PostgreSQL
Database Name:   A forrásadatot tartalmazó séma (ugyanaz, mint a Schema Name)
Schema Name:     A forrásadatot tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "szerver neve vagy IP-címe"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres vagy az adatbázis más neve"
name: "UID",        value: "Postgres felhasználóneve"
name: "PWD",        value: "Postgres jelszava"
name: "SSLMode",    value: "require"
```