---
title: Azure Synapse konnektor – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Azure Synapse Analytics-hez való csatlakozásra ODBC-n keresztül, DSN nélküli kapcsolati karakterlánccal. Támogatja a serverless és a dedicated SQL poolokat, a szükséges ODBC tulajdonságokkal és a digna-oldali kapcsolatbeállításokkal.
image: /assets/logo_square.png
---


# Forráskonnektor Azure Synapse Analytics-hez

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t az Azure Synapse Analytics-hez való
csatlakozásra **ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal. Serverless és
dedicated SQL poolok egyaránt támogatottak.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami az Azure Synapse-ra jellemző.

!!! note "Technológia"

    A Synapse az SQL Server dialektust beszéli, ezért a kapcsolatot **Technology:
    SQL Server** beállítással kell létrehozni. On-premises szerverhez lásd az
    [MS SQL Server](sqlserver_connector_guide.md) útmutatót.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse az **ODBC Driver 18 for SQL Server** illesztőprogramot arra a gépre, amely a *digna*
backendet futtatja, a [Microsoft telepítési útmutatója](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
szerint, és olvassa le a pontos regisztrált illesztőprogram-nevet a gépén, ahogyan az
[Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben le
van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    Microsoft ODBC illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek illesztőprogram-verziónként és platformonként eltérnek, és hogy a
    workspace mit követel meg, az a konfigurációjától függ — pool típusa, hitelesítési mód,
    tűzfal. Használja ezt kiindulópontként, és nézze meg a telepített illesztőprogram-verzió
    dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | A workspace neve plusz a végpont utótagja — lásd lent |
| `DATABASE` | `dignadata` | A forrássémákat tartalmazó adatbázis. Ez az egyetlen adatbázis, amelyet ez a kapcsolat profilozni tud |
| `UID` | `sqladminuser` | SQL login |
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |

Az így kapott kapcsolati karakterlánc így néz ki:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### A `SERVER` érték

Vegye a Synapse workspace nevét, és fűzze hozzá a végpont utótagját:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "A `-ondemand` részt könnyű kihagyni"

    Nélküle a név a dedicated végpontra oldódik fel, és a kapcsolat vagy sikertelen lesz, vagy
    csendben egy másik poolhoz csatlakozik, mint amit szándékozott. Mindkét végpont látható az
    Azure portal workspace-áttekintő oldalán.

### Tűzfal

A Synapse workspace tűzfalának engedélyeznie kell a *digna* gép kimenő címét. Adja hozzá a
workspace **Networking** részében, mielőtt tesztelné a kapcsolatot — egy blokkolt cím
kapcsolati időtúllépésként jelenik meg, nem hitelesítési hibaként.

### Microsoft Entra ID hitelesítés

SQL login helyett az illesztőprogram Entra ID-val is tud hitelesíteni. Cserélje le a
`UID`/`PWD` párt arra a hitelesítési módra, amelyet a workspace elvár, például:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | Ekkor a `UID` az alkalmazás (client) ID-t, a `PWD` pedig a client secretet kapja |
| `Authentication` | `ActiveDirectoryMSI` | A *digna* gép managed identity-je, nincs szükség hitelesítő adatokra |

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Megjegyzések az Azure Synapse-hoz {: #4-notes-on-azure-synapse }

- **A serverless poolok csak a *Standard* profilozást támogatják.** Egy serverless SQL pool nem
  tud táblákat létrehozni egy adatbázisban, így sem a *Permanent*, sem a *Session* profilozás
  nem futhat. A *Standard* a metrikákat közvetlenül a forráson számítja ki, ami egyben az
  olcsóbb megoldás is, mivel a serverless a feldolgozott adatmennyiség alapján kerül
  számlázásra.
- **Egy kapcsolat egy adatbázist lát.** A *digna* a `DATABASE`-ben megnevezett adatbázis
  sémáit kínálja fel, mert a Synapse — az SQL Serverhez hasonlóan — csak az aktuális
  adatbázist jelenti katalógusként.
- **A titkosítás alapértelmezetten be van kapcsolva** a Driver 18-ban, és a Synapse végpontok
  érvényes nyilvános tanúsítványokat mutatnak be, így nincs szükség `Encrypt` vagy
  `TrustServerCertificate` tulajdonságra.
- **Egy serverless végpont az első kapcsolódáskor tétlen állapotból ébredhet.** Ha a
  kapcsolatteszt időtúllépéssel leáll egy olyan poolon, amelyet egy ideje nem használtak,
  próbálja újra.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját varázslója kényelmes módja annak, hogy megbizonyosodjon arról, hogy az
illesztőprogram működik, és a workspace elfogadja a hitelesítő adatait, mielőtt megadná őket a
*digna*-ban.

#### 1. lépés
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Töltse ki a "Server" mezőt.
Használja a Synapse workspace nevét, és egészítse ki a ".sql.azuresynapse.net" utótaggal.  
**Figyelem**, ha serverless SQL poolon keresztül szeretne csatlakozni, feltétlenül adja hozzá a
"-ondemand" részt, ahogyan a fenti képernyőképen látható.

Kattintson a **Next >** gombra.

#### 2. lépés
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módot (pl. felhasználónév és jelszó),
és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### 3. lépés
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Meghagyhatja az alapértelmezett beállításokat, vagy szükség szerint választhat opciókat,
majd kattintson a **Finish** gombra.

#### 5. lépés
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### 6. lépés
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Egy sikert jelző képernyő megerősíti, hogy az illesztőprogram, a végpont és a hitelesítő adatok
működnek. A megadott értékek pontosan azok, amelyeket a [2. szakasz](#2-odbc-properties)
tulajdonságai kapnak.
