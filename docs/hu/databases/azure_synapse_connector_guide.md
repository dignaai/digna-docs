---
title: Azure Synapse Csatlakozó – Adatbázis integráció | digna Dokumentáció
description: Állítsa be a digna-t, hogy csatlakozzon az Azure Synapse Analyticshez a natív Python driver vagy az ODBC driver használatával. Mind a serverless, mind a dedicated SQL pool támogatott.
image: /assets/logo_square.png
---


# Forrás csatlakozó az Azure Synapse Analyticshez

Ez az útmutató leírja, hogyan konfigurálja a *digna*-t, hogy csatlakozzon az Azure Synapse Analyticshez a natív Python csatlakozó vagy az ODBC driver használatával.
Mind a serverless, mind a dedicated SQL pool támogatott.

A dokumentum a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python illesztőprogram

**Könyvtár:** `pymssql`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez használja az ODBC drivert.

### *digna* konfiguráció (natív illesztőprogram)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Az ODBC driver szélesebb körű hitelesítési és kapcsolódási lehetőségeket támogathat. Ez a rész a jelszó alapú hitelesítésre koncentrál, a **ODBC Driver 18 for SQL Server** használatával.

### 1. Telepítse az ODBC drivert

Telepítse az **ODBC Driver 18 for SQL Server** (vagy hasonló) drivert a gyártó hivatalos telepítési útmutatójának megfelelően.

### 2. Konfigurálja az ODBC adatforrást

Kövesse az alábbi lépéseket egy új ODBC adatforrás konfigurálásához jelszó alapú hitelesítéssel:

#### 1. lépés
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Töltse ki a "Server" mezőt.
Használja a Synapse workspace nevét, és egészítse ki ".sql.azuresynapse.net"-tel.  
**Figyelem**, ha serverless SQL poolon keresztül kíván csatlakozni, győződjön meg róla, hogy tartalmazza a "-ondemand" kiegészítést, ahogy az alábbi képernyőképen látható.

Kattintson a **Next >** gombra.

#### 2. lépés
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módszert (pl. felhasználónév és jelszó)
és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### 3. lépés
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Válassza az ANSI kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy válassza ki a szükséges opciókat,
majd kattintson a **Finish** gombra.

#### 5. lépés
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Most kattintson a ** Test datasource ** gombra.

#### 6. lépés
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Ha a siker képernyőt kapja, az ODBC megfelelően van konfigurálva.

---

Most konfigurálhatja a *digna*-t az ODBC kapcsolat használatára, akár **DSN (Data Source Name)** alapú, akár **DSN nélküli** beállítással.

---

### A. DSN alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC driver konfigurációjában megadott névvel.

---

### B. DSN nélküli konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC tulajdonságok

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Megjegyzés** a SERVER tulajdonsággal kapcsolatban:  
Használja a Synapse workspace nevét, és egészítse ki ".sql.azuresynapse.net"-tel. Ha serverless SQL poolon keresztül szeretne csatlakozni, győződjön meg róla, hogy tartalmazza a "-ondemand" kiegészítést, ahogy az alábbi képernyőképen látható.