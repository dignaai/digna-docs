# Forráskonnektor Teradata-hoz

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t a Teradata-hoz való csatlakozásra
**ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami a Teradata-ra jellemző.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse az **ODBC Driver for Teradata** illesztőprogramot arra a gépre, amely a *digna*
backendet futtatja, a gyártó hivatalos telepítési útmutatója szerint.

Az illesztőprogram a nevében a verziószámmal regisztrálja magát, például
**Teradata Database ODBC Driver 20.00**. Olvassa le a pontos regisztrált nevet a gépén, ahogyan
az [Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver) részben
le van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    Teradata ODBC illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek illesztőprogram-verziónként eltérnek — a verzió maga is az
    illesztőprogram nevének része —, valamint platformonként is. Használja ezt
    kiindulópontként, és nézze meg a telepített illesztőprogram-verzió dokumentációját.

Adja hozzá a következő tulajdonságokat az **Add DB Connection** képernyőn:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `DBCNAME` | `teradata.example.com` | Szervernév vagy IP-cím. A Teradata saját neve a host tulajdonságra |
| `UID` | `digna_source_user` | Adatbázis-felhasználó |
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |

Az így kapott kapcsolati karakterlánc így néz ki:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Hasznos további tulajdonságok:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `MechanismName` | `TD2` | Bejelentkezési mechanizmus. A `TD2` a Teradata alapértelmezése; címtáralapú hitelesítéshez használjon `LDAP`-ot |
| `DefaultDatabase` | `dad` | Az adatbázis, amelyben a munkamenet indul |
| `CharacterSet` | `UTF8` | Akkor állítsa be, ha a munkamenet alapértelmezett karakterkészlete eltorzítaná a nem ASCII adatokat |

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Megjegyzések a Teradata-hoz {: #4-notes-on-teradata }

- **Egy Teradata adatbázis katalógus, nem séma.** A *digna* katalógusként listázza azokat az
  adatbázisokat, amelyeket a felhasználó láthat (a `DBC.DatabasesV` alapján), és a sémaszint
  nem alkalmazható. Adatforrás hozzáadásakor az adatbázist katalógusként válassza ki; a séma
  *nem alkalmazható*ként jelenik meg.
- **Egy kapcsolat minden engedélyezett adatbázist elér**, így egyetlen kapcsolat több adatbázis
  forrásait is kiszolgálhatja — ellentétben azokkal a technológiákkal, ahol a kapcsolat egyetlen
  adatbázishoz van kötve.
- **A Work Schema egy adatbázis.** *Permanent* profilozáshoz adja meg azt a Teradata
  adatbázist, amely a munkatáblákat tartalmazza, és adjon a felhasználónak `CREATE TABLE`
  jogosultságot, valamint `PERM` területkiosztást benne — egy nulla perm területű adatbázis nem
  tud táblát tárolni.
- **Profilozási módok.** A *Permanent* a táblákat a **Work Schema**-ban hozza létre. A
  *Session* `VOLATILE` táblát használ, amelyhez `SPOOL` terület szükséges, de perm terület és
  jogosultság a **Work Schema**-ban nem. A *Standard*-hoz csak olvasási hozzáférés szükséges.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az illesztőprogram és a hitelesítő adatai működnek, mielőtt megadná őket a *digna*-ban.

#### 1. lépés
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Az itt látható **Name or IP address** mező a [2. szakasz](#2-odbc-properties) `DBCNAME`
tulajdonságának felel meg.

Kattintson a **Test** gombra.

#### 2. lépés
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Adja meg a felhasználónevet és a jelszót, majd kattintson az **OK** gombra. Egy sikert jelző
képernyő megerősíti, hogy az illesztőprogram és a hitelesítő adatok működnek.