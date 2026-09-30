# Forráskonnektor Hive-hoz

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t az Apache Hive-hoz való
csatlakozásra **ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami a Hive-ra jellemző.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse a **Cloudera ODBC Driver for Apache Hive** illesztőprogramot arra a gépre, amely a
*digna* backendet futtatja, a gyártó hivatalos telepítési útmutatója szerint.

Olvassa le a pontos regisztrált illesztőprogram-nevet a gépén, ahogyan az
[Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben le
van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    Cloudera Hive illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek illesztőprogram-verziónként és platformonként eltérnek, és hogy a
    HiveServer2 mit fogad el, az teljes mértékben attól függ, hogyan van védve a cluster —
    hitelesítési mechanizmus, átviteli mód, TLS, átjáró. Használja ezt kiindulópontként, és
    nézze meg a telepített illesztőprogram-verzió dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `HOST` | `hive.example.com` | A HiveServer2 hostneve vagy IP-címe |
| `PORT` | `10000` | HiveServer2 port; HTTP transport esetén `10001` |

Az így kapott kapcsolati karakterlánc így néz ki:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Hitelesítés

Egy védelem nélküli HiveServer2 a fenti három tulajdonságot változtatás nélkül elfogadja. Ahol
a hitelesítés engedélyezve van, adja hozzá a következőket:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `AuthMech` | `3` | `0` nincs hitelesítés, `2` csak felhasználónév, `3` felhasználónév és jelszó, `1` Kerberos |
| `UID` | `digna_source_user` | `AuthMech` `2` és `3` esetén kötelező |
| `PWD` | `<password>` | `AuthMech` `3` esetén kötelező. Jelölje be az **Encrypted** opciót |

Kerberos (`AuthMech=1`) esetén a *digna* gépnek ezenfelül érvényes ticketre vagy keytabra van
szüksége, valamint az illesztőprogram által dokumentált `KrbHostFQDN`, `KrbServiceName` és
`KrbRealm` tulajdonságokra.

### Átvitel és TLS

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `ThriftTransport` | `2` | `0` bináris (az alapértelmezés, 10000-es port), `1` SASL, `2` HTTP (10001-es port, és ezt várja egy Knox átjáró) |
| `HTTPPath` | `cliservice` | `ThriftTransport=2` esetén |
| `SSL` | `1` | Ahol a HiveServer2 TLS-sel védett |
| `Schema` | `dignadata` | Az a Hive adatbázis, amelyben a munkamenet indul. Opcionális — a *digna* minősített neveket használ a lekérdezéseiben |

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Megjegyzések a Hive-hoz {: #4-notes-on-hive }

- **A katalógusok az illesztőprogramtól származnak.** A Hive-nak nincs saját katalógusa, ezért
  a *digna* azt veszi át, amit az illesztőprogram jelent — általában egyetlen `HIVE` nevű
  bejegyzést —, és alatta sémaként listázza a Hive adatbázisokat.
- **A Work Schema egy Hive adatbázis.** *Permanent* profilozáshoz a felhasználónak jogosultság
  kell táblák létrehozására és törlésére benne, és a mögöttes tárolási helynek írhatónak kell
  lennie.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre. A
  *Session* `CREATE TEMPORARY TABLE`-t használ, amihez ideiglenes táblákat támogató
  HiveServer2 szükséges, és nem érinti a **Work Schema**-t. A *Standard*-hoz csak olvasási
  hozzáférés kell, és ezt a módot kell választani olyan clusteren, ahol a *digna*-nak egyáltalán
  nincs írási hozzáférése.
- **A profilozás lekérdezések sorozata, nem szkennelés.** Minden statisztikát a HiveServer2
  számít ki, ezért annak a queue-nak, amelybe a *digna* felhasználója küldi a lekérdezéseket,
  elegendő kapacitással kell rendelkeznie az inspection időablakához.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az illesztőprogram, az átviteli mód és a hitelesítő adatai működnek, mielőtt megadná őket a
*digna*-ban.

#### 1. lépés
![Step 1](images/hive/create_odbc_data_source_step1.png)

Az itt látható **Host**, **Port**, **Database**, **Mechanism** és **Thrift Transport** mezők a
[2. szakasz](#2-odbc-properties) `HOST`, `PORT`, `Schema`, `AuthMech` és `ThriftTransport`
tulajdonságainak felelnek meg.

#### 2. lépés – A kapcsolat tesztelése

Adja meg a jelszót, és kattintson a **Test** gombra.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Sikeres teszt után kattintson az **OK** gombra.