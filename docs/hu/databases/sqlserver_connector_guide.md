---
title: MS SQL Server konnektor – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Microsoft SQL Serverhez való csatlakozásra ODBC-n keresztül, DSN nélküli kapcsolati karakterlánccal. Lefedi a Microsoft ODBC illesztőprogramot, a szükséges ODBC tulajdonságokat, a titkosítási beállításokat és a digna-oldali kapcsolatbeállításokat.
image: /assets/logo_square.png
---


# Forráskonnektor MS SQL Serverhez

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t a Microsoft SQL Serverhez való
csatlakozásra **ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami az SQL Serverre jellemző.

!!! note "Azure Synapse Analytics"

    A Synapse szintén SQL Server kapcsolatként konfigurálható, eltérő hostnévvel és néhány
    további szemponttal — lásd: [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse az **ODBC Driver 18 for SQL Server** illesztőprogramot arra a gépre, amely a *digna*
backendet futtatja, a [Microsoft telepítési útmutatója](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server)
szerint.

A Windowszal egyszerűen **SQL Server** néven szállított illesztőprogram is működik, de már
régen elavult, és sem a modern TLS-beállításokat, sem az Azure-hitelesítést nem támogatja.
Csak ott használja, ahol az aktuális illesztőprogram telepítése nem lehetséges.

Olvassa le a pontos regisztrált illesztőprogram-nevet a gépén, ahogyan az
[Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben le
van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    Microsoft ODBC illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek illesztőprogram-verziónként eltérnek — például a Driver 18
    alapértelmezetten titkosít, míg a Driver 17 nem —, valamint platformonként is. Használja
    ezt kiindulópontként, és nézze meg a telepített illesztőprogram-verzió dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `SERVER` | `sql.example.com` | Szervernév vagy IP-cím. Nevesített példányok: `host\instance`; nem alapértelmezett port: `host,1433` |
| `PORT` | `1433` | Hagyja el, ha a port már a `SERVER` része |
| `DATABASE` | `digna_source_db` | A forrássémákat tartalmazó adatbázis. Ez az egyetlen adatbázis, amelyet ez a kapcsolat profilozni tud |
| `UID` | `digna_source_user` | Adatbázis-felhasználó |
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |

Az így kapott kapcsolati karakterlánc így néz ki:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Titkosítás az ODBC Driver 18-cal

A Driver 18 alapértelmezetten titkosítja a kapcsolatokat, és ellenőrzi a szervertanúsítványt.
Olyan szerver esetén, amelynek tanúsítványában a *digna* gép nem bízik meg — jellemzően egy
önaláírt tanúsítvány —, a kapcsolódás tanúsítványlánc-hibával meghiúsul. Adja hozzá a
következőket:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Encrypt` | `yes` | A Driver 18 alapértelmezése; csak akkor állítsa `no` értékre, ha a szerver nem képes TLS-re |
| `TrustServerCertificate` | `yes` | Kihagyja a tanúsítvány ellenőrzését. Tesztkörnyezetekben kényelmes; éles környezetben inkább telepítse a tanúsítványt |

### Windows-hitelesítés

Ha SQL login helyett a *digna* szolgáltatást futtató fiókként szeretne csatlakozni, hagyja el a
`UID` és `PWD` tulajdonságokat, és adja hozzá a következőt:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Trusted_Connection` | `yes` | A *digna* szolgáltatásfióknak kell rendelkeznie az adatbázis-jogosultságokkal |

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Megjegyzések az MS SQL Serverhez {: #4-notes-on-ms-sql-server }

- **Egy kapcsolat egy adatbázist lát.** A *digna* a `DATABASE`-ben megnevezett adatbázis
  sémáit kínálja fel, mert az SQL Server csak az aktuális adatbázist jelenti katalógusként. Egy
  másik adatbázisban lévő forrástáblákhoz saját kapcsolat kell.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre, ezért
  a felhasználónak ott `CREATE TABLE` jogosultság kell. A *Session* helyi ideiglenes táblákat
  (`#wt_…`) használ a `tempdb`-ben, és nem érinti a **Work Schema**-t. A *Standard*-hoz csak
  olvasási hozzáférés szükséges.
- **A `SERVER` tartalmazza a példányt és a portot.** Nevesített példány esetén a
  `host\instance` formához elérhetőnek kell lennie a SQL Server Browser szolgáltatásnak; a
  `host,port` forma ezt elkerüli.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját varázslója kényelmes módja annak, hogy megbizonyosodjon arról, hogy az
illesztőprogram működik, és a szerver elfogadja a hitelesítő adatait, mielőtt megadná őket a
*digna*-ban.

#### 1. lépés
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kattintson a **Next >** gombra.

#### 2. lépés
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Válassza ki a hitelesítési módot (pl. felhasználónév és jelszó),
és adja meg a szükséges adatokat.

Kattintson a **Next >** gombra.

#### 3. lépés
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Válassza az ANSI-kompatibilis beállításokat, majd kattintson a **Next >** gombra.

#### 4. lépés
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Meghagyhatja az alapértelmezett beállításokat, vagy szükség szerint választhat naplózási
opciókat, majd kattintson a **Finish** gombra.

#### 5. lépés
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Most kattintson a **Test datasource** gombra.

#### 6. lépés
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Egy sikert jelző képernyő megerősíti, hogy az illesztőprogram és a hitelesítő adatok működnek.
A megadott értékek pontosan azok, amelyeket a [2. szakasz](#2-odbc-properties) tulajdonságai
kapnak.
