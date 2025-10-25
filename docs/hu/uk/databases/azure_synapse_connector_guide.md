---
title: Azure Synapse Connector – Database Integration | digna Dokumentáció
description: Állítsa be a digna-t, hogy csatlakozzon az Azure Synapse Analytics-hez akár natív Python-illesztőprogrammal, akár ODBC-illesztőprogrammal. Támogatja a serverless és a dedicated SQL poolokat is.
image: /assets/logo_square.png
---


# Azure Synapse Analytics forráskapcsoló

Ez az útmutató leírja, hogyan állítsa be a *digna*-t az Azure Synapse Analytics-hez való csatlakozáshoz, akár a natív Python-kapcsolóval, akár az ODBC-illesztőprogrammal. Támogatottak a serverless és a dedicated SQL poolok is.

Hivatkozik a **"Create a Database Connection"** képernyőre.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natív Python driver

**Könyvtár:** `pymssql`  
**Támogatott hitelesítés:** csak jelszó alapú hitelesítés

> ⚠️ Más hitelesítési módokhoz használja az ODBC-illesztőprogramot.

### *digna* konfiguráció (natív driver)

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

Az ODBC-illesztőprogram többféle hitelesítési és csatlakozási lehetőséget támogat. Ez a rész a jelszó alapú hitelesítésre összpontosít az **ODBC Driver 18 for SQL Server** használatával.

### 1. ODBC-illesztőprogram telepítése

Telepítse az **ODBC Driver 18 for SQL Server** (vagy hasonló) illesztőprogramot a gyártó hivatalos útmutatása szerint.

### 2. ODBC adatforrás beállítása

Kövesse az alábbi lépéseket egy új ODBC adatforrás beállításához jelszó alapú hitelesítéssel:

#### 1. lépés
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Töltse ki a "Server" mezőt.  
Használja a Synapse workspace nevét, és adja hozzá a ".sql.azuresynapse.net" kiterjesztést.  
Figyelem: ha a serverless SQL poolhoz szeretne csatlakozni, győződjön meg róla, hogy hozzáadta a "-ondemand" részt, ahogy a következő képernyőképen is látható.

Kattintson a **Tovább >** gombra.

#### 2. lépés
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módszert (például felhasználónév és jelszó), és adja meg a szükséges adatokat.

Kattintson a **Tovább >** gombra.

#### 3. lépés
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Tovább >** gombra.

#### 4. lépés
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Hagyhatja az alapértelmezett beállításokat, vagy válasszon opciókat igény szerint, majd kattintson a **Kész** gombra.

#### 5. lépés
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Most kattintson az **Adatforrás tesztelése** gombra.

#### 6. lépés
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Ha megjelenik a siker képernyő, az ODBC helyesen van konfigurálva.

---

Most beállíthatja a *digna*-t az ODBC-kapcsolat használatára, akár **DSN (Data Source Name)** alapúan, akár **DSN nélküli** módban.

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

> 🔹 A `DSN`-nek meg kell egyeznie az ODBC-illesztőprogram konfigurációjában megadott névvel.

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

Megjegyzés a SERVER tulajdonsághoz:  
Használja a Synapse workspace nevét, és adja hozzá a ".sql.azuresynapse.net" kiterjesztést. Ha a serverless SQL poolhoz szeretne csatlakozni, ügyeljen rá, hogy tartalmazza a "-ondemand" részt, ahogy a következő képernyőképen látható.