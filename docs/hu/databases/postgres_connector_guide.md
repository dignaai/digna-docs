---
title: PostgreSQL konnektor – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása PostgreSQL-hez való csatlakozásra ODBC-n keresztül, DSN nélküli kapcsolati karakterlánccal. Lefedi a psqlODBC illesztőprogramot, a szükséges ODBC tulajdonságokat, az SSL-módokat és a digna-oldali kapcsolatbeállításokat.
image: /assets/logo_square.png
---


# Forráskonnektor PostgreSQL-hez

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t a PostgreSQL-hez való csatlakozásra
**ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami a PostgreSQL-re jellemző.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse a PostgreSQL ODBC illesztőprogramot (**psqlODBC**) arra a gépre, amely a *digna*
backendet futtatja, a gyártó hivatalos telepítési útmutatója szerint.

Az illesztőprogram platformonként és csomagonként eltérő néven regisztrálja magát — Windowson
jellemzően **PostgreSQL Unicode(x64)**, Linuxon **PostgreSQL ODBC Driver(UNICODE)** néven.
Olvassa le a pontos nevet a gépén, ahogyan az
[Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben le
van írva, és ezt a nevet használja az alábbi `DRIVER` tulajdonsághoz.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    psqlODBC illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az elfogadott
    értékek illesztőprogram-verziónként és platformonként eltérnek, és az is eltérhet, amit a
    szervere megkövetel — különösen az SSL. Használja ezt kiindulópontként, és nézze meg a
    telepített illesztőprogram-verzió dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `SERVER` | `db.example.com` | Szervernév vagy IP-cím |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | A forrássémákat tartalmazó adatbázis. Ez az egyetlen adatbázis, amelyet ez a kapcsolat profilozni tud |
| `UID` | `digna_source_user` | Adatbázis-felhasználó |
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` vagy `verify-full` — a szervernek el kell fogadnia |

Az így kapott kapcsolati karakterlánc így néz ki:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Bármely további psqlODBC opció hozzáadható további tulajdonságként — például `ReadOnly=1` egy
csak olvasható munkamenethez, vagy `ConnSettings` `SET` utasítások futtatásához a
kapcsolódáskor.

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Megjegyzések a PostgreSQL-hez {: #4-notes-on-postgresql }

- **Az `SSLMode`-nak egyeznie kell a szerverrel.** Egy `hostssl`-lel konfigurált szerver
  elutasítja az `SSLMode=disable` beállítást, a `verify-ca` vagy `verify-full` pedig ezenfelül
  megköveteli, hogy a gyökértanúsítvány elérhető legyen az illesztőprogram számára a *digna*
  gépen. Ha az illesztőprogram tesztelésekor egy adott módot kellett választania, itt is
  ugyanazt használja.
- **Egy kapcsolat egy adatbázist lát.** A *digna* a `DATABASE`-ben megnevezett adatbázis
  sémáit kínálja fel, mert a PostgreSQL csak az aktuális adatbázist jelenti katalógusként. Egy
  másik adatbázisban lévő forrástáblákhoz saját kapcsolat kell.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre, ezért
  a felhasználónak `CREATE` jogosultság kell azon a sémán. A *Session* `CREATE TEMPORARY TABLE`-t
  használ, és nem érinti a **Work Schema**-t. A *Standard*-hoz csak olvasási hozzáférés
  szükséges.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az illesztőprogram működik, és a szerver elfogadja a hitelesítő adatait és az SSL-módot, mielőtt
megadná őket a *digna*-ban.

#### 1. lépés
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### 2. lépés – A kapcsolat tesztelése

Kattintson a **Test Connection** gombra.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Az itt megadott értékek pontosan azok, amelyeket a [2. szakasz](#2-odbc-properties)
tulajdonságai kapnak.
