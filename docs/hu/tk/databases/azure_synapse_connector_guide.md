---
title: Azure Synapse Connector – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Azure Synapse Analytics-hez való csatlakozáshoz a natív Python-illesztőprogrammal vagy az ODBC-illesztővel. Támogatja a szerver nélküli (serverless) és a dedicated SQL poolokat.
image: /assets/logo_square.png
---


# Forráskapcsolat Azure Synapse Analytics-hez

Ez az útmutató azt ismerteti, hogyan csatlakoztathatja a *digna*-t Azure Synapse Analytics-hez vagy a natív Python illesztőprogramon keresztül, vagy az ODBC-illesztő segítségével.
Támogatja a szerver nélküli (serverless) és a dedicated SQL poolokat.

Ez a dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Adatbázis kapcsolat létrehozása](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Könyvtár:** `pymssql`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módokhoz kérjük, használja az ODBC-illesztőt.

### *digna* konfiguráció (natív illesztő)

A **"Create a Database Connection"** képernyőn adja meg az alábbi adatokat:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port száma, pl. 1433
Database Name:   Adatbázis neve
Schema Name:     A forrás adatot tartalmazó sémanév
User Name:       Adatbázis felhasználónév
User Password:   Felhasználó jelszava
Use ODBC:        Ki (alapértelmezett)
```

---

## ODBC Driver

Az ODBC-illesztő szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogat. Ez a rész a jelszó alapú hitelesítésre koncentrál, az **ODBC Driver 18 for SQL Server** használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse az **ODBC Driver 18 for SQL Server** (vagy hasonló) illesztőt a gyártó hivatalos telepítési útmutatóját követve.

### 2. Konfigurálja az ODBC adatforrást

Jelszó alapú hitelesítés használatával új ODBC adatforrást az alábbi lépésekkel hozhat létre:

#### 1. lépés
![1. lépés](images/azure_synapse/create_odbc_data_source_step1.png)

Töltse ki a "Server" mezőt.
Használja a Synapse munkaterület nevét, és adja hozzá a végére a ".sql.azuresynapse.net" kiterjesztést.  
Figyelem: ha egy szerver nélküli (serverless) SQL poolhoz csatlakozik, győződjön meg róla, hogy a névhez hozzáfűzte a "-ondemand" részt, ahogy az alábbi képernyőképen látható.

Kattintson a **Next >** gombra.

#### 2. lépés
![2. lépés](images/azure_synapse/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módot (pl. felhasználónév és jelszó),
és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### 3. lépés
![3. lépés](images/azure_synapse/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![4. lépés](images/azure_synapse/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy szükség szerint módosíthatja a lehetőségeket,
majd kattintson a **Finish** gombra.

#### 5. lépés
![5. lépés](images/azure_synapse/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### 6. lépés
![6. lépés](images/azure_synapse/create_odbc_data_source_step6.png)

Ha sikeres üzenetet kap, az ODBC megfelelően konfigurálva van.

---

Most konfigurálhatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN-less** módon.

---

### A. DSN alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg az alábbiakat:

```
Technology:      MS SQL Server
Database Name:   Az adatforrást tartalmazó adatbázis
Schema Name:     A forrás adatot tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "adatbázis felhasználóneve"
name: "PWD",        value: "adatbázis jelszava"
name: "DATABASE",   value: "az a adatbázis neve, amely a forrás séma adatait tartalmazza"
```

> 🔹 A `DSN` értékének meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN-less konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg az alábbiakat:

```
Technology:      MS SQL Server
Database Name:   A forrás sémát tartalmazó adat (azonos a Schema Name-nel)
Schema Name:     A forrás adatot tartalmazó séma
Use ODBC:        Engedélyezve
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "adatbázis felhasználóneve"
name: "PWD",        value: "adatbázis jelszava"
name: "DATABASE",   value: "az a adatbázis neve, amely a forrás séma adatait tartalmazza"
```

**Megjegyzés**: a SERVER tulajdonsággal kapcsolatban:  
Használja a Synapse munkaterület nevét, és adja hozzá a végére a ".sql.azuresynapse.net" kiterjesztést. Ha egy szerver nélküli (serverless) SQL poolhoz csatlakozik, győződjön meg róla, hogy a névhez hozzáfűzte a "-ondemand" részt, ahogy az alábbi képernyőképen látható.