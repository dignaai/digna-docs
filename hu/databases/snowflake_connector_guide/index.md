# Forráskonnektor Snowflake-hez

Ez az útmutató leírja, hogyan konfigurálhatja a *digna*-t a Snowflake-hez való csatlakozásra
**ODBC**-n keresztül, **DSN nélküli** kapcsolati karakterlánccal.

A beállítás *digna*-oldali része minden technológiánál ugyanaz — hol jönnek létre a
kapcsolatok, hogyan titkosíthatók a tulajdonságértékek, hogyan tesztelhető egy kapcsolat és mit
jelentenek a profilozási módok. Ezt az [Adatbázis-kapcsolatok áttekintése](overview.md) írja
le. Ez az oldal azt tárgyalja, ami a Snowflake-re jellemző.

---

## 1. Az ODBC illesztőprogram telepítése {: #1-install-the-odbc-driver }

Telepítse a **Snowflake ODBC Driver** illesztőprogramot arra a gépre, amely a *digna*
backendet futtatja, a [Snowflake telepítési útmutatója](https://docs.snowflake.com/en/developer-guide/odbc/odbc)
szerint.

Az illesztőprogram **SnowflakeDSIIDriver** néven regisztrálja magát. Olvassa le a pontos
regisztrált nevet a gépén, ahogyan az [Az ODBC illesztőprogram telepítése a digna gépre](overview.md#install-the-driver)
részben le van írva.

---

## 2. ODBC tulajdonságok {: #2-odbc-properties }

A Snowflake **programmatic access tokennel (PAT)** érhető el — ez az a hitelesítési mód,
amellyel a *digna*-t ellenőrizték, és amelyet a Snowflake megkövetel azoknál a fiókoknál,
ahol a csak jelszavas bejelentkezés le van tiltva.

!!! important "Példa, nem specifikáció"

    Az alábbi készlet egy olyan kombináció, amelyről ismert, hogy működik. A tulajdonságok a
    Snowflake ODBC illesztőprogramhoz tartoznak, így nevük, alapértelmezett értékeik és az
    elfogadott értékek illesztőprogram-verziónként és platformonként eltérnek, és hogy a fiókja
    milyen hitelesítési lehetőségeket enged, azt a fiók biztonsági szabályzata határozza meg.
    Használja ezt kiindulópontként, és nézze meg a telepített illesztőprogram-verzió
    dokumentációját.

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Egyeznie kell a *digna* gépen regisztrált illesztőprogram-névvel |
| `Server` | `<account>.snowflakecomputing.com` | A fiókazonosító plusz az utótag, pl. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Az a Snowflake felhasználó, amelyhez a token tartozik |
| `Database` | `TEST` | A forrássémákat tartalmazó adatbázis. Ez az egyetlen adatbázis, amelyet ez a kapcsolat profilozni tud |
| `Schema` | `PUBLIC` | A munkamenet alapértelmezett sémája |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Tokenes hitelesítést választ ki |
| `token` | `<programmatic access token>` | Jelölje be az **Encrypted** opciót |

Az így kapott kapcsolati karakterlánc így néz ki:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse és szerepkör

A lekérdezésekhez warehouse szükséges. Ha a *digna* felhasználónak van alapértelmezett
warehouse-a és alapértelmezett szerepköre, a munkamenet ezeket használja, és semmit sem kell
konfigurálni. Ellenkező esetben adja hozzá a következőket:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | A profilozási lekérdezéseket futtató warehouse |
| `Role` | `DIGNA_READER` | Az a szerepkör, amelynek jogosultságait a munkamenet használja |

!!! tip "Adjon a dignának saját warehouse-t"

    Egy külön, kicsi, automatikusan felfüggesztődő warehouse láthatóvá teszi a profilozás
    költségét, és megakadályozza, hogy a *digna* az interaktív felhasználókkal versengjen a
    számítási kapacitásért.

### Jelszavas hitelesítés

Ahol a fiók még engedi, a token helyett jelszó is használható — hagyja el az `authenticator`
és `token` tulajdonságokat, és adja hozzá a következőt:

| Kulcs | Példaérték | Megjegyzések |
|---|---|---|
| `PWD` | `<password>` | Jelölje be az **Encrypted** opciót |

---

## 3. *digna* konfiguráció {: #3-digna-configuration }

Az **Add DB Connection** képernyőn adja meg a következőket:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Megjegyzések a Snowflake-hez {: #4-notes-on-snowflake }

- **A tokenek lejárnak.** Egy programmatic access token meghatározott élettartammal kerül
  kiadásra, és a profilozás azon a napon leáll, amikor lejár. Jegyezze fel a lejárati dátumot a
  létrehozáskor, és adja meg újra az új tokent a `token` tulajdonságban — a titkosított értékek
  lecserélhetők, de nem olvashatók vissza.
- **Egy kapcsolat egy adatbázist lát.** A *digna* a `Database`-ben megnevezett adatbázis
  sémáit kínálja fel, mert a Snowflake csak az aktuális adatbázist jelenti katalógusként. Egy
  másik adatbázisban lévő forrástáblákhoz saját kapcsolat kell.
- **Az azonosítók nagybetűsek**, hacsak nem idézőjelek között hozták létre őket. A *digna* a
  neveket úgy használja, ahogyan a Snowflake jelenti őket.
- **Profilozási módok.** A *Permanent* a munkatáblákat a **Work Schema**-ban hozza létre, ezért
  a szerepkörnek ott `CREATE TABLE` jogosultság kell. A *Session* `CREATE TEMPORARY TABLE`-t
  használ, és nem érinti a **Work Schema**-t. A *Standard*-hoz csak olvasási hozzáférés
  szükséges — írási jogosultság egyáltalán nem.

---

## 5. Az illesztőprogram ellenőrzése (opcionális) {: #5-verifying-the-driver-optional }

ODBC adatforrás konfigurálása nem szükséges egy DSN nélküli kapcsolathoz, de az
illesztőprogram saját párbeszédablaka kényelmes módja annak, hogy megbizonyosodjon arról, hogy
az illesztőprogram, a fiók URL-je és a hitelesítő adatai működnek, mielőtt megadná őket a
*digna*-ban.

#### 1. lépés
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Megjegyzések:

- A **Server** értéke a Snowflake fiókazonosítóból és az azt követő
  `.snowflakecomputing.com` utótagból áll.
- Az itt megadott **Database**, **Schema** és **Warehouse** a [2. szakasz](#2-odbc-properties)
  `Database`, `Schema` és `Warehouse` tulajdonságainak felel meg.

#### 2. lépés – A kapcsolat tesztelése

Kattintson a **TEST** gombra. Egy sikeres kapcsolat így néz ki:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)