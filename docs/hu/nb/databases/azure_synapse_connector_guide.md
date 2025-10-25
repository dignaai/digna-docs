---
title: Azure Synapse Connector – Adatbázis-integráció | digna Dokumentáció
description: Konfigurálja a digna-t az Azure Synapse Analytics-hez való csatlakozáshoz a natív Python-illesztőprogrammal vagy az ODBC-illesztőprogrammal. Támogatja a serverless és a dedikált SQL poolokat is.
image: /assets/logo_square.png
---


# Forráskapcsoló az Azure Synapse Analytics-hez

Ez az útmutató bemutatja, hogyan konfigurálja a digna-t az Azure Synapse Analytics-hez való csatlakozáshoz, akár a natív Python-illesztőprogram, akár az ODBC-illesztőprogram használatával.
Támogatja mind a serverless, mind a dedikált SQL poolokat.

A leírás a **"Create a Database Connection"** képernyőre hivatkozik.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python-illesztőprogram

**Könyvtár:** `pymssql`  
**Támogatott hitelesítés:** Csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módszerekhez kérjük, használja az ODBC-illesztőprogramot.

### *digna* konfiguráció (natív illesztő)

Adja meg a következő információkat a **"Create a Database Connection"** képernyőn:

```
Technológia:     MS SQL Server
Szervercím:      <synapse-workspace>[-ondemand].sql.azuresynapse.net
Portszám:        Portszám, pl. 1433
Adatbázisnév:    Adatbázis neve
Séma:            A forrásadatokat tartalmazó séma
Felhasználónév:  Adatbázis felhasználóneve
Jelszó:          A felhasználó jelszava
Használjon ODBC-t: Letiltva (alapértelmezett)
```

---

## ODBC-illesztőprogram

Az ODBC-illesztőprogram szélesebb körű hitelesítési és csatlakozási lehetőségeket támogat. Ez a rész a jelszó alapú hitelesítésre összpontosít, az **ODBC Driver 18 for SQL Server** használatával.

### 1. Telepítse az ODBC-illesztőt

Telepítse az **ODBC Driver 18 for SQL Server** (vagy egyenértékű) illesztőt a gyártó hivatalos telepítési útmutatóját követve.

### 2. Konfigurálja az ODBC-adatforrást

Kövesse az alábbi lépéseket egy új ODBC-adatforrás jelszó alapú hitelesítéssel történő konfigurálásához:

#### Lépés 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Töltse ki a "Server" mezőt.
Használja a Synapse munkaterület nevét, és adja hozzá a ".sql.azuresynapse.net" kiterjesztést.  
**Megjegyzés**, ha serverless SQL poolhoz szeretne csatlakozni, ügyeljen rá, hogy tartalmazza a "-ondemand" részt, ahogy az alábbi képernyőképen látható.

Kattintson a **Next >** gombra.

#### Lépés 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módot (pl. felhasználónév és jelszó)
és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### Lépés 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### Lépés 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy válasszon opciókat szükség szerint,
majd kattintson a **Finish** gombra.

#### Lépés 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Kattintson most a **Test datasource** gombra.

#### Lépés 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Amikor sikeres üzenetet kap, az ODBC megfelelően konfigurálva van.

---

Most konfigurálhatja a digna-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapúan, akár **DSN-less** módon.

---

### A. DSN-alapú konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technológia:     MS SQL Server
Adatbázisnév:    Az adatbázis, amely a forrás-sémát tartalmazza
Séma:            A forrásadatokat tartalmazó séma
Használjon ODBC-t: Engedélyezve
```

#### ODBC-tulajdonságok

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztő konfigurációjában megadott névvel.

---

### B. DSN-less konfiguráció

#### *digna* konfiguráció

A **"Create a Database Connection"** képernyőn adja meg a következőket:

```
Technológia:     MS SQL Server
Adatbázisnév:    A forrásadatokat tartalmazó séma (ugyanaz, mint a Séma)
Séma:            A forrásadatokat tartalmazó séma
Használjon ODBC-t: Engedélyezve
```

#### ODBC-tulajdonságok

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Megjegyzés** a SERVER tulajdonságról:  
Használja a Synapse munkaterület nevét és adja hozzá a ".sql.azuresynapse.net" kiterjesztést. Ha serverless SQL poolhoz kíván csatlakozni, győződjön meg róla, hogy tartalmazza a "-ondemand" részt, ahogy az alábbi képernyőképen látható.