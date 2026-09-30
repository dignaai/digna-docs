---
title: Adatbázis-kapcsolatok áttekintése – DSN nélküli ODBC beállítás | digna dokumentáció
description: Hogyan működnek az adatbázis-kapcsolatok a digna rendszerben. Minden forrástechnológia ODBC-n keresztül érhető el, ODBC tulajdonságokból összeállított, DSN nélküli kapcsolati karakterlánccal. Lefedi az illesztőprogram telepítését a digna gépen, az Add DB Connection képernyőt, a tulajdonságok titkosítását, a kapcsolat tesztelését, a hibakeresést, valamint a technológiánkénti útmutatókra mutató hivatkozásokat.
image: /assets/logo_square.png
keywords:
  - digna adatbázis-kapcsolat
  - dsn nélküli odbc
  - odbc kapcsolati karakterlánc
  - odbc illesztőprogram beállítása
  - unixodbc
  - odbc tulajdonságok
  - adatforrás konfigurálása
lang: en
robots: index, follow
og_title: digna Database Connections – DSN-less ODBC Setup
og_description: Configure a digna source connection over ODBC without a DSN. Driver installation, ODBC properties, encryption, testing and troubleshooting.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Adatbázis-kapcsolatok áttekintése

---

## Tartalomjegyzék

1. [Hogyan működnek a kapcsolatok](#how-connections-work)
2. [Technológiai útmutatók](#technology-guides)
3. [Előfeltétel: az ODBC illesztőprogram telepítése a digna gépre](#install-the-driver)
4. [Adatbázis-kapcsolat létrehozása](#create-a-database-connection)
5. [ODBC tulajdonságok](#odbc-properties)
6. [Tulajdonságértékek titkosítása](#encrypting-property-values)
7. [Kapcsolat tesztelése](#testing-a-connection)
8. [Melyik adatbázist látja a kapcsolat](#which-database-the-connection-sees)
9. [Profilozási mód és munkaséma](#profiling-mode-and-work-schema)
10. [DSN használata helyette](#using-a-dsn-instead)
11. [Hibakeresés](#troubleshooting)

---

## Hogyan működnek a kapcsolatok {: #how-connections-work }

A *digna* minden forrástechnológiát **ODBC**-n keresztül ér el. Egy kapcsolat ODBC
tulajdonságok listája, amelyeket kulcs/érték párokként ad meg. Amikor a *digna* megnyitja a
kapcsolatot, ezeket a párokat kapcsolati karakterlánccá fűzi össze — `Key=Value`, `;`-vel
elválasztva, abban a sorrendben, ahogyan felsorolta őket —, és átadja a *digna* gépen futó
ODBC illesztőprogram-kezelőnek.

Az teszi a beállítást **DSN nélkülivé**, hogy a tulajdonságokat Ön adja meg: a kapcsolat
mindent tartalmaz, amire az illesztőprogramnak szüksége van, így a gépen nem kell ODBC
adatforrást (DSN) regisztrálni. Ez a *digna* ajánlott konfigurálási módja, mert a kapcsolat
definíciója teljes egészében a *digna*-ban található, és együtt mozog vele.

### Miért ODBC {: #why-odbc }

A korábbi kiadásokban választani lehetett a technológiánkénti illesztőprogram és az ODBC
között, egy **Use ODBC** kapcsolóval. A Release 2026.06-tól a *digna* kizárólag ODBC-re épül.
Egyetlen, szabványos interfész többet nyújt, mint egyedi illesztőprogramok gyűjteménye:

- **Hitelesítés** — a hitelesítés az ODBC része, így egy kapcsolat bármit használhat, amit az
  illesztőprogramja támogat: jelszavakat, tokeneket és PAT-okat, Kerberost és Active
  Directoryt, MFA-t és böngészőalapú single sign-ont, felhőalapú identitást, kliens-
  tanúsítványokat és TLS-t. Az új módszerek egy illesztőprogram-frissítéssel érkeznek, nem kell
  egy *digna* kiadásra várni.
- **Az adatbázis-gyártók által karbantartott illesztőprogramok** — a gyártó saját
  illesztőprogramja követi az új szerververziókat és biztonsági javításokat, és Ön a saját
  ütemezése szerint frissítheti, a *digna*-tól függetlenül.
- **Egyetlen módja mindennek a konfigurálására** — minden technológia kulcs/érték
  tulajdonságok listája, ugyanazzal az interfésszel, az érzékeny értékek ugyanolyan
  titkosításával és ugyanazzal a hibakereséssel, forrásonként eltérő mezőkészletek helyett.
- **Hangolás és elérés** — az illesztőprogram-szintű beállítások, például időkorlátok,
  TLS-beállítások, proxyk és lekérési méretek minden forrásnál elérhetők, és bármely olyan
  technológia csatlakoztatható, amelyhez megfelelő ODBC illesztőprogram létezik, azokat is
  beleértve, amelyekhez a *digna* nem ad ki külön útmutatót.

!!! note "Mi változott a felületen"

    A **Use ODBC** kapcsoló, valamint a külön host, port, adatbázis, felhasználó és jelszó
    mezők megszűntek. Egy olyan kapcsolatnál, amely még nem ODBC-t használ, meg kell adni az
    ODBC tulajdonságokat, mielőtt újra működne — lásd:
    [Adatbázis-kapcsolat létrehozása](#create-a-database-connection).

---

## Technológiai útmutatók {: #technology-guides }

A tulajdonságok neve illesztőprogramonként eltér, és minden technológiának van egy-két
sajátossága, amely a többinél nincs meg. Az alábbi útmutatók ezt a részt fedik le; ez az oldal
a *digna* oldalt írja le, amely mindegyiknél ugyanaz.

!!! important "Az útmutatókban szereplő tulajdonságkészletek példák"

    Minden útmutató egy olyan kombinációt mutat be, amelyről ismert, hogy működik — azt,
    amellyel a *digna*-t tesztelik. Ez kiindulópont, nem specifikáció: a tulajdonságok az ODBC
    illesztőprogramhoz tartoznak, és hogy melyek léteznek, hogyan hívják őket és milyen
    értékeket fogadnak el, az eltér az illesztőprogram-verziók és gyártók között, Windows, Linux
    és macOS között, valamint attól függően, hogyan van konfigurálva a forrásszerver —
    hitelesítési mód, TLS, átjáró, port. Számítson rá, hogy egy-két értéket módosítania kell, és
    a telepített illesztőprogram-verzió dokumentációját tekintse mérvadónak.

| Technológia | Útmutató | Érdemes tudni |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | A serverless poolokhoz `-ondemand` kell a hostnévben, és csak a *Standard* profilozást támogatják |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Tokenes hitelesítés: `UID=token`, a PAT a `PWD`-be kerül |
| **Apache Hive** | [Hive](hive_connector_guide.md) | A katalógusok az illesztőprogramtól származnak, nem lekérdezésből |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Az illesztőprogram neve kapcsos zárójelben áll: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | A `DBQ` teljes connect descriptort vagy `tnsnames.ora` aliast fogad el |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | Az `SSLMode`-nak egyeznie kell azzal, amit a szerver megkövetel |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | A programmatic access token a tesztelt hitelesítési mód |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | A `DATABASE` dönti el, mely sémákat látja a *digna* |
| **Teradata** | [Teradata](teradata_connector_guide.md) | A host a `DBCNAME`-be kerül; az adatbázisok sémaként működnek |

---

## Előfeltétel: az ODBC illesztőprogram telepítése a digna gépre {: #install-the-driver }

A *digna* a forráskapcsolatokat **a digna backendet futtató szerverről** nyitja meg, nem a
böngészőből. Az ODBC illesztőprogramot ezért erre a gépre kell telepíteni, és a nevét
regisztrálni kell a helyi illesztőprogram-kezelőben.

=== "Windows"

    Telepítse a gyártó 64 bites illesztőprogramját, majd nyissa meg az
    **ODBC Data Source Administrator (64-bit)** alkalmazást, és váltson a **Drivers** fülre.
    Az ott felsorolt nevek pontosan azok az értékek, amelyeket a `Driver` tulajdonsághoz
    használhat.

=== "Linux"

    Telepítse a **unixODBC**-t és a gyártó illesztőprogramját, majd listázza a regisztrált
    illesztőprogram-neveket:

    ```bash
    odbcinst -q -d
    ```

    A szögletes zárójelben kiírt nevek azok az értékek, amelyeket a `Driver` tulajdonsághoz
    használhat. Ezek az `/etc/odbcinst.ini` fájlból (vagy abból a fájlból, amelyet az
    `odbcinst -j` jelez) származnak.

=== "macOS"

    Telepítse a **unixODBC**-t (például a `brew install unixodbc` paranccsal) és a gyártó
    illesztőprogramját, majd listázza a regisztrált illesztőprogram-neveket:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Az illesztőprogram nevének karakterre pontosan egyeznie kell"

    A `Driver` változatlanul kerül át az illesztőprogram-kezelőhöz. A `Simba Spark ODBC Driver`
    és a `Simba Spark ODBC Driver 64` az illesztőprogram-kezelő számára két különböző
    illesztőprogram, és egy nem regisztrált név *data source name not found* hibát okoz, holott
    semmilyen DSN nem érintett.

Regisztrált név helyett minden elterjedt illesztőprogram-kezelő elfogadja az
illesztőprogram-könyvtár teljes elérési útját is, például
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Ez akkor hasznos, ha az
illesztőprogram telepítve van, de nincs regisztrálva.

---

## Adatbázis-kapcsolat létrehozása {: #create-a-database-connection }

Nyissa meg az **Admin Panel**-t, lépjen a **Database Connections** fülre, és kattintson az
**Add DB Connection** gombra. A képernyő öt dolgot kér:

| Mező | Leírás |
|---|---|
| **Name** | A kapcsolat neve. Ezzel hivatkoznak a kapcsolatra más képernyőkön. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake vagy Hive. Ez választja ki, milyen SQL-dialektust generál a *digna*, ezért a forráshoz kell illeszkednie — nem az illesztőprogramhoz. Az Azure Synapse Analytics **SQL Server** kapcsolat. |
| **ODBC Properties** | Az [ODBC tulajdonságok](#odbc-properties) részben leírt kulcs/érték párok. |
| **Profiling Mode** | *Standard*, *Permanent* vagy *Session* — lásd: [Profilozási mód és munkaséma](#profiling-mode-and-work-schema). |
| **Work Schema** | Az a séma, amely a *Permanent* profilozás munkatábláit tartalmazza. |

A kapcsolatot központilag kezelik, majd egy vagy több projekthez rendelik hozzá, így ugyanaz a
kapcsolat több projektet is kiszolgálhat.

---

## ODBC tulajdonságok {: #odbc-properties }

Minden tulajdonsághoz kattintson az **Add Property** gombra, és töltse ki a **Key** és
**Value** mezőt, titkos értékeknél pedig jelölje be az **Encrypted** jelölőnégyzetet. Minden
technológiai útmutató felsorol egy példakészletet az adott technológiához, amelyet az Ön
illesztőprogram-verziójához és szerveréhez kell igazítani — lásd
[a fenti megjegyzést](#technology-guides).

Az illesztőprogramtól függetlenül egy tulajdonságkészlet ugyanazt a négy dolgot fedi le:

- **`Driver`** — a regisztrált illesztőprogram-név, ahogyan [fent](#install-the-driver) le van
  írva.
- **A szerver címe** — a kulcs illesztőprogramonként eltér: `SERVER`, `HOST`, `DBCNAME`,
  `Server`, Oracle esetén pedig a `DBQ` connect descriptor.
- **Hitelesítő adatok** — általában `UID` és `PWD`; a Snowflake `UID`-t és egy `token`-t
  használ, a Databricks pedig a szó szerinti `token` felhasználót és a personal access tokent a
  `PWD`-ben.
- **Az adatbázis vagy katalógus, amelyben dolgozni kell**, ahol a technológiának van ilyen —
  lásd: [Melyik adatbázist látja a kapcsolat](#which-database-the-connection-sees).

Bármi más, amit az illesztőprogram dokumentál, ugyanígy hozzáadható — kapcsolatkészletezés
(connection pooling), socket-időkorlátok, Kerberos-beállítások, proxybeállítások. A *digna* nem
értelmezi a tulajdonságokat; csak továbbadja őket.

!!! warning "Az értékek nincsenek escape-elve — a pontosvesszőt tartalmazó értékeket tegye kapcsos zárójelbe"

    Mivel a tulajdonságok `;`-vel vannak összefűzve, egy olyan érték, amely maga is `;`-t
    tartalmaz, rossz helyen vágná ketté a kapcsolati karakterláncot. Az ilyen értékeket tegye
    kapcsos zárójelbe: `PWD={p@ss;word}`. Ugyanez vonatkozik az `=`-t vagy kezdő szóközöket
    tartalmazó értékekre. Ezért írnak egyes illesztőprogramokat hagyományosan kapcsos
    zárójelben, mint a `{NetezzaSQL}` vagy a `{SnowflakeDSIIDriver}`.

---

## Tulajdonságértékek titkosítása {: #encrypting-property-values }

Jelölje be az **Encrypted** opciót minden olyan tulajdonságnál, amely titkot tartalmaz —
`PWD`, `token`, egy client secret. Az érték ekkor titkosítva kerül a *digna* repositoryba, a
képernyőn maszkolva jelenik meg, és csak a kapcsolati karakterlánc összeállításakor kerül
visszafejtésre.

!!! tip "Tipp"

    Egy titkosított érték nem olvasható vissza, sem a felületen, sem az API-n keresztül — csak
    lecserélni lehet. A titkokat tárolja a saját jelszókezelőjében is.

A nem titkos tulajdonságokat — az illesztőprogram nevét, a hostot, a portot, az adatbázist —
érdemes titkosítatlanul hagyni, hogy olvashatók maradjanak annak, aki később a kapcsolatot
karbantartja.

---

## Kapcsolat tesztelése {: #testing-a-connection }

Kattintson a **Test** gombra az *Add DB Connection* párbeszédablakban, **mielőtt** mentene. A
teszt az űrlapon éppen szereplő értékeket használja, és valódi kapcsolódást hajt végre, így
pontosan azt jelzi, amibe egy inspection is beleütközne — rossz illesztőprogram-név, elutasított
jelszó, elérhetetlen host. Semmi sem kerül tárolásra: a tesztkapcsolat visszagörgetésre kerül,
akár sikeres, akár nem.

Egy már létező kapcsolatnál vigye az egeret a sora fölé a **Database Connections** fülön, és
kattintson a **dugó** ikonra az újrateszteléshez. Ez a leggyorsabb módja annak ellenőrzésére,
hogy egy forrás elérhető-e jelszócsere vagy tűzfalmódosítás után.

---

## Melyik adatbázist látja a kapcsolat {: #which-database-the-connection-sees }

Amikor adatforrást ad hozzá, a *digna* felajánlja azokat a katalógusokat, sémákat és táblákat,
amelyeket a kapcsolat elér. Hogy ez meddig terjed, az a technológiától függ:

| Technológia | Felajánlott katalógusok |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Csak a kapcsolat **aktuális** adatbázisa |
| **Teradata**, **Netezza**, **Databricks** | Minden adatbázis vagy katalógus, amelyet a felhasználó láthat |
| **Hive**, **Impala** | Az illesztőprogram jelenti |

!!! important "Egy kapcsolat, egy adatbázis"

    PostgreSQL, SQL Server, Oracle és Snowflake esetén a tulajdonságoknak arra az adatbázisra
    kell mutatniuk, amely a forrássémákat tartalmazza — `DATABASE=…`, `Database=…`, vagy a
    szolgáltatásnév az Oracle `DBQ`-ján belül. Egy másik adatbázis táblái nem érhetők el azon
    a kapcsolaton keresztül; ahhoz adjon hozzá egy második kapcsolatot.

---

## Profilozási mód és munkaséma {: #profiling-mode-and-work-schema }

A profilozási mód határozza meg, hogyan dolgozza fel a *digna* az adatokat és számítja ki a
metrikákat:

- **Standard:** A metrikák közvetlenül a forrástáblákon kerülnek kiszámításra, az adatok
  másolása nélkül.
- **Permanent:** A vizsgált nap adatai egy állandó táblába kerülnek átmásolásra, és a metrikák a
  másolt adatokon kerülnek kiszámításra.
- **Session:** Az adatok egy munkamenet- vagy ideiglenes táblába kerülnek átmásolásra, és a
  metrikák ezeken az ideiglenes adatokon kerülnek kiszámításra.

A mód dönti el, mit kell engedélyezni a kapcsolat felhasználójának:

| Mód | Mit ír | A kapcsolat felhasználójának szükséges jogai |
|---|---|---|
| **Standard** | semmit | Olvasás a forrástáblákon |
| **Permanent** | adatforrásonként egy táblát a **Work Schema**-ban | Táblák létrehozása és törlése a **Work Schema**-ban |
| **Session** | egy ideiglenes táblát, amelyet az adatbázis a munkamenettel együtt töröl | Ideiglenes táblák létrehozása — a **Work Schema** nincs használatban |

A *Standard* csak olvas, ezért ezt a módot kell választani, ha a *digna* csak olvasási
hozzáférést kap. A **Work Schema** csak *Permanent* esetén kerül beolvasásra, de érdemes így is
kitölteni, hogy a kapcsolat akkor is működjön, ha a módot később megváltoztatják.

---

## DSN használata helyette {: #using-a-dsn-instead }

A DSN továbbra is működik — a `DSN` csak egy újabb tulajdonság:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

A DSN-t a *digna* gépen kell regisztrálni, ugyanahhoz a felhasználói fiókhoz, amely a *digna*
backendet futtatja, és **System DSN**-ként, ha a *digna* szolgáltatásként fut. Minden, ami a
DSN-ben be van állítva, felülírható, ha tulajdonságként is hozzáadja.

A DSN nélküli beállítás a dokumentált alapértelmezés, mert elkerüli ezt a gépen tárolt
állapotot: a kapcsolat teljes egészében a *digna*-ban van leírva, és egy új *digna* gépre csak
az illesztőprogramot kell telepíteni, konfigurálni semmit sem kell.

---

## Hibakeresés {: #troubleshooting }

### Data source name not found / no default driver specified

**Tünetek:**
- A **Test** gomb *data source name not found* hibát jelez, holott a beállítás DSN nélküli

**Okok és megoldások:**
1. A `Driver` értéke nem egyezik egyetlen regisztrált illesztőprogram-névvel sem — vesse össze
   az *ODBC Data Source Administrator (64-bit)* **Drivers** fülével, vagy az `odbcinst -q -d`
   kimenetével
2. Az illesztőprogram a munkaállomásán telepítve van, de a *digna* gépen nem
3. Az illesztőprogram 32 bites, míg a *digna* 64 bites — telepítse a 64 bites illesztőprogramot
4. A `Driver` tulajdonság teljesen hiányzik, és `DSN` sem lett megadva
5. Linuxon és macOS-en az illesztőprogram telepítve van, de nincs regisztrálva — adja meg
   helyette az illesztőprogram-könyvtár teljes elérési útját, vagy regisztrálja az
   `odbcinst.ini` fájlban

---

### A kapcsolatteszt időtúllépéssel leáll

**Tünetek:**
- A **Test** elakad, majd nagyjából fél perc után hibával leáll

**Okok és megoldások:**
1. A host vagy a port nem érhető el a *digna* gépről — ellenőrizze a tűzfalat, felhőalapú
   forrásoknál pedig az IP-engedélyezési listát
2. A hostnév helyes, de a port egy másik szolgáltatáshoz tartozik
3. A forrásnak az alapértelmezett 30 másodpercnél több idő kell a kapcsolat elfogadásához —
   növelje a `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` értékét a `config.toml` `[base]` szakaszában
   (a `0` korlátlan ideig vár), és indítsa újra a backendet
4. Egy serverless végpont éppen tétlen állapotból ébred — próbálja újra, és ha ez rendszeresen
   előfordul, növelje a bejelentkezési időkorlátot a fentiek szerint

---

### A hitelesítés sikertelen, pedig a hitelesítő adatok helyesek

**Tünetek:**
- Az illesztőprogram érvénytelen hitelesítő adatokat jelez, de ugyanaz a felhasználó egy másik
  SQL-kliensben működik

**Okok és megoldások:**
1. A jelszó `;`-t tartalmaz — tegye az értéket kapcsos zárójelbe: `{p@ss;word}`
2. Egy záró szóköz is bemásolódott az értékbe
3. Az illesztőprogram egy adott hitelesítési mechanizmust vár — például `AuthMech`-et a Hive és
   Databricks illesztőprogramoknál, vagy `authenticator`-t a Snowflake-nél
4. Az értéket titkosítva tárolták, majd szerkesztették — a titkosított értékek nem olvashatók
   vissza, ezért adja meg újra a teljes titkot
5. Egy token lejárt — a personal access tokenek és a programmatic access tokenek lejárati
   dátummal kerülnek kiadásra

---

### Az adatforrás-képernyő nem kínálja fel a várt adatbázist vagy sémát

**Tünetek:**
- Adatforrás hozzáadásakor katalógusok, sémák vagy táblák hiányoznak

**Okok és megoldások:**
1. A kapcsolat egy másik adatbázisra mutat — lásd:
   [Melyik adatbázist látja a kapcsolat](#which-database-the-connection-sees)
2. A kapcsolat felhasználójának nincs olvasási joga a sémán vagy az adatszótáron
3. A **Technology** nem egyezik a forrással, ezért a *digna* rossz adatszótárat kérdez le
4. Snowflake esetén a felhasználóhoz nincs alapértelmezett warehouse rendelve, és `Warehouse`
   tulajdonság sem lett megadva, így a metaadat-lekérdezések nem futhatnak le

---

### A profilozás sikertelen, míg a kapcsolatteszt sikeres

**Tünetek:**
- A **Test** sikeres, de egy inspection a munkatáblák létrehozásakor meghiúsul

**Okok és megoldások:**
1. *Permanent* profilozás van kiválasztva, és a kapcsolat felhasználója nem hozhat létre
   táblákat a **Work Schema**-ban — adja meg a jogokat, vagy váltson *Session* vagy *Standard*
   módra
2. A **Work Schema** üres, vagy nem létező sémát nevez meg, miközben *Permanent* profilozás van
   kiválasztva
3. *Session* profilozás van kiválasztva, és a kapcsolat felhasználója nem hozhat létre
   ideiglenes táblákat
4. Egy hosszan futó profilozási lekérdezés eléri a lekérdezési időkorlátot — növelje a
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` értékét a `config.toml` `[base]` szakaszában
   (alapértelmezés 3600 másodperc, a `0` kikapcsolja az időkorlátot)

---

## Bevált gyakorlatok

**TEGYE:**

- Telepítse és regisztrálja az illesztőprogramot a *digna* gépen, mielőtt a kapcsolatot
  konfigurálja
- Jelölje be az **Encrypted** opciót minden jelszónál és tokennél
- Kattintson a **Test** gombra mentés előtt, és teszteljen újra jelszócsere után
- Nevezze el a kapcsolatokat a forrás és a környezet alapján, például `sales_dwh_prod`
- Adjon a *digna*-nak dedikált adatbázis-felhasználót, csak olvasási joggal, ahol a *Standard*
  profilozás elegendő
- Forrásadatbázisonként egy kapcsolatot tartson fenn, és inkább adjon hozzá egy másodikat,
  mint hogy az elsőt átállítsa

**NE TEGYE:**

- Ne tároljon titkokat titkosítatlanul, és ne használjon közös adatbázis-felhasználót a *digna*
  és más eszközök között
- Ne használjon 32 bites illesztőprogramot 64 bites *digna* telepítéssel
- Ne hagyatkozzon User DSN-re, ha a *digna* szolgáltatásként fut — nem lesz látható
- Ne adjon meg `;`-t tartalmazó értéket kapcsos zárójelek nélkül egy tulajdonságban
- Ne állítsa a **Work Schema**-t olyan sémára, amely forrásadatokat tartalmaz

---

## Támogatás

Segítségre van szüksége egy adatbázis-kapcsolattal?

- **E-mail:** support@digna.ai
- **Dokumentáció:** https://docs.digna.ai
- **Weboldal:** https://www.digna.ai

---

**Kiadás:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
