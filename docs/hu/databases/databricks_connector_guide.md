---
title: Databricks konnektor – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Unity Cataloggal rendelkező Databricks-hez való csatlakozásra ODBC-n keresztül, DSN nélküli kapcsolati karakterlánccal. Lefedi a Databricks ODBC illesztőprogramot, a personal access tokeneket, a HTTP path-ot és a digna-oldali kapcsolatbeállításokat.
image: /assets/logo_square.png
---

# Forráskonnektor Databricks-hez

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t a Databricks-hez való csatlakozásra
**ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami a Databricks-re jellemző.

!!! note "Unity Catalog szükséges"

    A *digna* az elérhető katalógusokat a `system.information_schema.catalogs` táblából
    olvassa ki, ezért a workspace-en engedélyezni kell a Unity Catalogot. A korábbi *digna*
    kiadások külön "Databricks Legacy" technológiát kínáltak a Unity Catalog nélküli
    workspace-ekhez; ez már nem érhető el.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse a **Databricks ODBC Driver** illesztőprogramot arra a gépre, amely a *digna*
backendet futtatja, a [Databricks telepítési útmutatója](https://docs.databricks.com/aws/en/integrations/odbc/)
szerint.

A verziótól függően az illesztőprogram **Simba Spark ODBC Driver** vagy
**Databricks ODBC Driver** néven regisztrálja magát. Olvassa le a pontos regisztrált nevet a
gépén, ahogyan az [Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver)
részben le van írva.

---

## 2. A kapcsolati adatok összegyűjtése {: #2-gather-the-connection-details }

Minden érték abból az SQL warehouse-ból (vagy clusterből) származik, amelyet a *digna*-val
használni szeretne. Nyissa meg a Databricks workspace-ben, és lépjen a
**Connection details** részre:

| Databricks mező | Felhasználás |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, általában `443` |
| **HTTP path** | `HTTPPath` |

A hitelesítéshez hozzon létre egy **personal access tokent** — lásd:
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
A tokenek egy felhasználóhoz vagy service principalhoz tartoznak, és ennek a principalnak
`USE CATALOG`, `USE SCHEMA` és `SELECT` jogosultságra van szüksége a forrásadatokon.

---

## 3. ODBC tulajdonságok {: #3-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    Databricks/Simba illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek illesztőprogram-verziónként eltérnek — az illesztőprogramot többször
    átnevezték, és a hitelesítési lehetőségeit többször bővítették —, valamint platformonként
    is. Használja ezt kiindulópontként, és nézze meg a telepített illesztőprogram-verzió
    dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `Host` | `<workspace>.cloud.databricks.com` | A warehouse server hostname-je, pl. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | A warehouse vagy cluster HTTP path-ja |
| `SSL` | `1` | A Databricks végpontok csak TLS-t fogadnak |
| `ThriftTransport` | `2` | HTTP transport, ezt beszélik az SQL végpontok |
| `AuthMech` | `3` | Tokenes hitelesítés |
| `UID` | `token` | Szó szerint a `token` szó, nem felhasználónév |
| `PWD` | `dapi…` | A personal access token. Jelölje be az **Encrypted** opciót |
| `UseNativeQuery` | `1` | A *digna* SQL-jét változatlanul továbbítja — lásd lent |

Az így kapott kapcsolati karakterlánc így néz ki:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Tartsa meg a `UseNativeQuery=1` beállítást"

    `UseNativeQuery=0` esetén — ez az illesztőprogram alapértelmezése — az illesztőprogram a
    bejövő SQL-t átírja arra, amit hordozható ODBC-szintaxisnak gondol. A *digna* már eleve
    Databricks SQL-t generál, így az átírás megváltoztathatja a backtick-es idézést és a
    dátumliterálokat, és a profilozás ekkor olyan utasításokon bukik el, amelyek az eredeti
    formájukban érvényesek.

### OAuth token helyett

OAuth machine-to-machine hitelesítést használó service principal esetén cserélje le az
`AuthMech`, `UID` és `PWD` tulajdonságokat a következőkre:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Jelölje be az **Encrypted** opciót |

---

## 4. *digna* konfiguráció {: #4-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Megjegyzések a Databricks-hez {: #5-notes-on-databricks }

- **A warehouse-nak futnia kell**, vagy el kell tudnia indulni, amikor a *digna* csatlakozik.
  Egy leállított állapotból induló warehouse-nak több idő kellhet, mint a kapcsolati
  időkorlát — ha a teszt egy tétlen időszak utáni első próbálkozáskor sikertelen, próbálja
  újra.
- **A katalógusok a workspace-ből származnak.** A legtöbb technológiával ellentétben egy
  Databricks kapcsolat minden olyan katalógust elér, amelyet a principal láthat, így egyetlen
  kapcsolat több katalógus forrásait is kiszolgálhatja.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre, a
  forrás katalógusán belül, ezért a principalnak ott `CREATE TABLE` jogosultság kell. A
  *Session* `CREATE TEMPORARY TABLE`-t használ, és nem érinti a **Work Schema**-t. A
  *Standard*-hoz csak olvasási hozzáférés szükséges.
- **A serverless warehouse-ok** ugyanígy működnek; csak a `HTTPPath` különbözik.

---

## 6. Az illesztőprogram ellenőrzése (opcionális) {: #6-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az illesztőprogram, a warehouse és a token működik, mielőtt megadná őket a *digna*-ban.

#### 1. lépés
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### 2. lépés
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### 3. lépés
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### 4. lépés
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### 5. lépés – A kapcsolat tesztelése

Kattintson a **TEST** gombra. Egy sikeres kapcsolat így néz ki:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Az itt megadott host, HTTP path és token pontosan azok az értékek, amelyeket a
[3. szakasz](#3-odbc-properties) tulajdonságai kapnak.
