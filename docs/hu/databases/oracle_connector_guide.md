---
title: Oracle konnektor – Adatbázis-integráció | digna dokumentáció
description: A digna konfigurálása Oracle-höz való csatlakozásra ODBC-n keresztül, DSN nélküli kapcsolati karakterlánccal. Lefedi az Oracle ODBC illesztőprogramot, a DBQ connect descriptort, a TNS aliasokat és a digna-oldali kapcsolatbeállításokat.
image: /assets/logo_square.png
---


# Forráskonnektor Oracle-höz

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t az Oracle Database-hez való
csatlakozásra **ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami az Oracle-re jellemző.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Az Oracle ODBC illesztőprogram az **Oracle Client** része (az Instant Client "ODBC" csomagja
elegendő). Telepítse arra a gépre, amely a *digna* backendet futtatja, a gyártó hivatalos
telepítési útmutatója szerint.

Az illesztőprogram **Oracle in `<OracleHomeName>`** néven regisztrálja magát — például
`Oracle in OraDB21Home1` vagy `Oracle in instantclient_21_13`. A home neve telepítésenként
eltér, ezért olvassa le a pontos nevet a gépén, ahogyan az
[Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben le
van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok az
    Oracle ODBC illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek kliensverziónként eltérnek, és különösen az illesztőprogram neve függ a
    gépén lévő Oracle home-tól. Használja ezt kiindulópontként, és nézze meg a telepített
    kliensverzió dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Az adatbázis, amelyhez csatlakozni kell — lásd lent |
| `UID` | `DIGNA_SOURCE_USER` | Adatbázis-felhasználó |
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |

Az így kapott kapcsolati karakterlánc így néz ki:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### A `DBQ` érték

A `DBQ` háromféle formát fogad el. A *digna* számára egyenértékűek; abban különböznek, hogy mit
kell konfigurálni a *digna* gépen:

| Forma | Példa | Előfeltétel |
|---|---|---|
| **Teljes connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Semmi — minden a tulajdonságban van. Ajánlott |
| **TNS alias** | `DIGNA_SOURCE` | Az aliasnak léteznie kell a *digna* gépen lévő Oracle Client `tnsnames.ora` fájljában |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Easy Connectet támogató Oracle Client (12c és újabb) |

!!! tip "Részesítse előnyben a teljes descriptort"

    Egy TNS alias a kapcsolatdefiníció felét egy fájlba helyezi át a *digna* gépen, ahol
    könnyű megfeledkezni róla, amikor a gépet újraépítik vagy a *digna*-t áthelyezik. A teljes
    descriptor önállóan tartja a kapcsolatot — éppen ez a DSN nélküli beállítás lényege.

A descriptorban lévő zárójelek nem okoznak gondot a kapcsolati karakterláncban, de ha a jelszava
`;`-t tartalmaz, tegye kapcsos zárójelbe: `PWD={p@ss;word}`.

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Megjegyzések az Oracle-höz {: #4-notes-on-oracle }

- **A sémák felhasználók.** A *digna* az Oracle felhasználókat sémaként listázza, így a
  forrásséma a táblák tulajdonosa — a fenti példában `DIGNA_SOURCE_USER`. A kapcsolat
  felhasználójának `SELECT` jogosultság kell ezeken a táblákon, közvetlenül vagy egy szerepkörön
  keresztül.
- **Egy kapcsolat egy adatbázist lát.** A *digna* által felajánlott katalógus az az adatbázis,
  amelyhez a kapcsolat csatlakozik, így a `DBQ` dönti el, melyik szolgáltatás, és ezáltal
  melyik adatbázis kerül profilozásra.
- **Az azonosítók idézőjelezés után megkülönböztetik a kis- és nagybetűket.** A *digna*
  idézőjelek közé teszi az adatszótárból kiolvasott neveket, vagyis azt, amit az Oracle tárol —
  az idézőjel nélkül létrehozott objektumoknál nagybetűvel.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre, ezért
  a felhasználónak ott `CREATE TABLE` jogosultság és kvóta kell a tablespace-en. A *Session*
  privát ideiglenes táblát (`ORA$PTT_…`, Oracle 18c és újabb) használ, és nem érinti a
  **Work Schema**-t. A *Standard*-hoz csak olvasási hozzáférés szükséges.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az Oracle Client, a szolgáltatásnév és a hitelesítő adatai működnek, mielőtt megadná őket a
*digna*-ban.

#### 1. lépés
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Az itt felkínált **TNS Service Name** az Oracle Client telepítésének `tnsnames.ora` fájljából
származik — ott van definiálva az alias, és vele együtt a host, a port és a szolgáltatásnév. A
*digna*-ban az aliast használhatja `DBQ`-ként, vagy helyette a teljes descriptort.

#### 2. lépés – A kapcsolat tesztelése

Kattintson a **Test Connection** gombra.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Adja meg a jelszót, és kattintson az **OK** gombra.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Egy sikert jelző üzenet megerősíti, hogy az illesztőprogram és a hitelesítő adatok működnek.
