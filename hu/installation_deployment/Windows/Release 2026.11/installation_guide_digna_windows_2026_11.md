# digna Release 2026.11 Windows telepítési útmutató

**Kiadás:** 2026.11

**Utoljára frissítve:** 2026. november 7.


---

## Tartalomjegyzék

1. [Bevezetés](#introduction)
2. [Rendszerkövetelmények](#system-requirements)
3. [Előkészítő lépések](#pre-installation-setup)
4. [PostgreSQL szerver beállítása](#postgresql-server-setup)
5. [Webkiszolgáló konfiguráció](#web-server-configuration)
6. [Kezdeti telepítés](#initial-installation)
7. [Backend konfiguráció](#backend-configuration)
8. [Dashboard konfiguráció](#dashboard-configuration)
9. [digna futtatása Windows szolgáltatásként](#running-digna-as-a-windows-service)
10. [Frissítés új kiadásra](#upgrading-to-a-new-release)

---

## Bevezetés {: #introduction }

### A dignáról

digna egy átfogó, mesterséges intelligencia által vezérelt platform, amely a különböző adatkörnyezeteiben (adatraktárak, adat-tavak és lakehouse-ok) optimalizálja az adatok minőségkezelését. Nagy skálázhatóságra és alkalmazkodóképességre tervezve, digna automatizálással, valós idejű monitorozással és anomália-észleléssel kezeli a modern adathasználat kihívásait.

A digna két fő komponensből áll:

- **digna**: az alkalmazás magja, amely az adatok feldolgozásáért és a minőségi ellenőrzések végrehajtásáért felel. Egyetlen futtatható fájlban egyesíti a háttérrendszert és a parancssori felületet, felváltva a korábbi kiadások különálló `dignabackend` és `dignacli` programjait.
- **dignadashboard**: webalapú felület, amely webkiszolgálón fut és felhasználóbarát módon biztosít hozzáférést a digna platformhoz és az adatok minőségi metrikáinak megjelenítéséhez.

### Mi újság a 2026.11-os kiadásban

Ez a kiadás bevezeti a digna Data Reconciliation-t, a digna Agentic-et a digna MCP Serverrel, valamint a digna Engine-t, amely a dignán belül képes adatokat profilozni, és különböző adatbázis-technológiák között is ellenőrzi a referenciális integritást. A részletekért lásd a [kiadási megjegyzéseket](../../../changelog/Release_202611.md).

A telepítés szempontjából a kiadás új migrációs mechanizmust hoz a tárolóséma kezelésére, egy opcionális `[duckdb]` szekciót a `config.toml` fájlban a digna Engine számára, valamint új licencfájlt. Mindegyikkel a [frissítésről szóló szakasz](#upgrading-to-a-new-release) foglalkozik.

### macOS vagy Linux telepítést keresel?

Ez az útmutató Windowsra vonatkozik. Más platformokhoz lásd a [macOS telepítési útmutatót](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) vagy a [Linux telepítési útmutatót](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Rendszerkövetelmények {: #system-requirements }

Mielőtt elkezdenéd a telepítést, győződj meg róla, hogy a rendszered megfelel az alábbi minimális követelményeknek:

| Követelmény | Specifikáció |
|---|---|
| **Operációs rendszer** | Windows Server vagy Windows 10/11 |
| **Memória (minimális telepítés)** | 16 GB RAM |
| **Lemezterület** | 10 GB szabad tárhely |
| **Adatbázis** | PostgreSQL Server 12 vagy újabb |
| **Webkiszolgáló** | IIS, Apache Tomcat vagy egyenértékű |

!!! info "digna Engine"

    Azokat az adatbázis-kapcsolatokat, amelyek profilozási helyként a digna Engine-t használják,
    magán a digna gazdagépen profilozza a rendszer. Ezekhez további memóriát és lemezterületet kell
    tervezni, lásd: [\[duckdb\] szekció](#duckdb-section).

### Adatbázis telepítési opciók

**Ha a PostgreSQL már telepítve van:**
Új adatbázist hozhatsz létre a digna számára a meglévő PostgreSQL szerveren.

**Ha ugyanarra a gépre telepíted a PostgreSQL-t, mint a digna:**

!!! info "Ajánlott specifikációk"

    - **Memória**: 32 GB RAM (a 16 GB helyett)
    - **Lemezterület**: 50 GB szabad tárhely (a 10 GB helyett)

    Ezek a magasabb erőforrások azt szolgálják, hogy a digna és a PostgreSQL adatbázis egyszerre fusson optimálisan.

---

## Előkészítő lépések {: #pre-installation-setup }

A digna telepítése előtt győződj meg róla, hogy két kulcsfontosságú előfeltétel rendelkezésre áll:

1. **PostgreSQL szerver** – a számított metrikák és teljesítményadatok tárolásához
2. **Webkiszolgáló** – a digna Dashboard hosztolásához

Ha ezek a komponensek még nincsenek telepítve, kövesd az alábbi szakaszokat az installáláshoz és konfiguráláshoz.

---

## PostgreSQL szerver beállítása {: #postgresql-server-setup }

### Ha már van PostgreSQL-ed

Ha a PostgreSQL már telepítve és fut a helyi gépeden, vagy ha menedzselt távoli PostgreSQL szervert használsz, átugorhatod ezt a részt és folytathatod a [következő szakaszra](#web-server-configuration).

### PostgreSQL telepítése

Kövesd az alábbi lépéseket a PostgreSQL Windowsra történő telepítéséhez:

#### 1. lépés: PostgreSQL letöltése

1. Látogass el a [PostgreSQL Downloads page](https://www.postgresql.org/download/) oldalra
2. Válaszd a **Windows** opciót
3. Töltsd le a legfrissebb telepítőt

#### 2. lépés: Futtasd a telepítőt

1. Kattints duplán a letöltött telepítőfájlra
2. Kövesd a telepítővarázsló utasításait

#### 3. lépés: Telepítési könyvtár kiválasztása

Válaszd ki a PostgreSQL telepítési könyvtárát. Az alapértelmezett hely általában megfelelő.

#### 4. lépés: Komponensek kiválasztása

Egy standard telepítéshez hagyd meg az alapértelmezett komponensbeállításokat.

#### 5. lépés: PostgreSQL szuperfelhasználó jelszó megadása

Add meg és erősítsd meg a PostgreSQL szuperfelhasználó (`postgres`) jelszavát. **Tárold ezt a jelszót biztonságosan** — később szükséged lesz rá.

#### 6. lépés: Portszám konfigurálása

Az alapértelmezett PostgreSQL port a `5432`. Használhatod az alapértelmezettet, vagy megadhatsz más portot, ha szükséges.

!!! tip "Tipp"

    Ha a 5432-es port már használatban van, válassz alternatív portot és jegyezd fel a későbbi konfigurációhoz.

#### 7. lépés: Locale kiválasztása

Válaszd ki az adatbázis locale-beállítását. Az alapértelmezett általában megfelelő a legtöbb telepítéshez.

#### 8. lépés: Telepítés befejezése

Kattints a **Next** gombra a fennmaradó lépéseknél, majd a **Finish** gombra.

#### 9. lépés: Telepítés ellenőrzése

Nyisd meg a Parancssort és ellenőrizd, hogy a PostgreSQL telepítve van:

```bash
psql --version
```

A parancs kimenetében meg kell jelennie a PostgreSQL verziónak, ha a telepítés sikeres volt.

---

## Webkiszolgáló konfiguráció {: #web-server-configuration }

A digna dashboard hosztolásához webkiszolgálóra van szükség. Válassz egyet az alábbi lehetőségek közül:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Elegendő, ha **egy** webkiszolgálót telepítesz és konfigurálsz.

### IIS beállítása {: #iis-setup }

#### Áttekintés

Az Internet Information Services (IIS) a Microsoft webszervere weboldalak és webalkalmazások hosztolásához.

#### IIS engedélyezése

1. **Nyisd meg a Vezérlőpultot**
   - Nyomd meg a `Win + R` billentyűket
   - Írd be: `control` és nyomj Entert

2. **Nyisd meg a Windows szolgáltatások beállításait**
   - Kattints a **Programok** menüpontra
   - Válaszd a **Windows-szolgáltatások be- vagy kikapcsolása** lehetőséget

3. **Engedélyezd az Internet Information Services-t**
   - Görgess le és keresd meg az **Internet Information Services (IIS)** elemet
   - Jelöld be a jelölőnégyzetet
   - Kattints a **+** jelre az alkönyvtárak kibontásához, és győződj meg róla, hogy a következő alkomponensek ki vannak választva:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Kattints az OK gombra** a változtatások alkalmazásához

5. **IIS telepítés ellenőrzése**
   - Nyisd meg a böngészőt
   - Navigálj a `http://localhost` címre
   - Az IIS kezdőoldalának kell megjelennie

#### Kötelező: URL Rewrite modul

Az IIS-nek szüksége van a URL Rewrite komponensre. Töltsd le és telepítsd a [hivatalos Microsoft oldalról](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Kötelező: MIME típus Markdown fájlokhoz

Annak érdekében, hogy az IIS helyesen szolgálja ki a Markdown fájlokat (`.md`):

1. Nyisd meg az **IIS Manager**-t (nyomd meg a `Win + R`, írd be `inetmgr`, majd Enter)
2. Navigálj a **Siteod > MIME Types** pontra
3. Kattints az **Add...** gombra
4. Állítsd be:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Fontos"

    Ennek a beállításnak hiányában a `.md` fájlok nem biztos, hogy megfelelően lesznek kiszolgálva.

---

### Apache Tomcat beállítása {: #apache-tomcat-setup }

#### Áttekintés

Az Apache Tomcat egy nyílt forráskódú Java servlet konténer és webszerver.

#### Telepítés

1. **Töltsd le az Apache Tomcat-et**
   - Látogass el az [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) oldalra
   - Töltsd le a Windows ZIP kiadást

2. **Csomag kicsomagolása**
   - Csomagold ki a ZIP fájlt egy könyvtárba a rendszeren
   - Példa: `C:\Program Files\Apache Tomcat`

3. **Ellenőrizd, hogy a Tomcat fut-e**
   - Nyisd meg a böngészőt
   - Navigálj a `http://localhost:8080` címre
   - Az Apache Tomcat kezdőoldalának kell megjelennie

!!! tip "Tipp"

    Az Apache Tomcat általában automatikusan elindul a telepítés után. Ha nem indul el, navigálj a `bin` mappába és futtasd a `startup.bat` fájlt.

---

## Kezdeti telepítés {: #initial-installation }

### 1. lépés: Hozd létre a digna adattárat (repository)

A digna adattára tárolja a digna által számított összes metrikát. Központi adatbázisként szolgál az analitikai és teljesítményadatokhoz.

#### Séma és felhasználó létrehozása az adattárhoz

Nyisd meg a PostgreSQL kliensedet (pgAdmin, psql vagy hasonló) és futtasd az alábbi SQL parancsokat:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Cseréld ki az alábbi helyőrzőket:**

- `<digna_repo_schema>` — a kívánt sémanév (pl.: `dignarepo`)
- `<digna_repo_user>` — a kívánt felhasználónév (pl.: `digna_user`)
- `<digna_repo_password>` — ennek a felhasználónak a biztonságos jelszava

**Példa:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Legjobb gyakorlat"

    Használj erős, komplex jelszavakat az adatbázis-felhasználókhoz. Kerüld az könnyen kitalálható hitelesítő adatokat.

---

### 2. lépés: Csomagold ki a digna telepítési csomagot

1. Keresd meg a neked átadott digna telepítési ZIP fájlt
2. Csomagold ki a kívánt telepítési helyre
3. A kicsomagolás után a következő elemeket kell látnod:
   - `dashboard/` — webes dashboard felület
   - `digna` — fő futtatható állomány (backend + CLI kombinálva)

!!! info "A konfigurációs és a licencfájl nincs benne a csomagban"

    Sem a `config.toml`, sem a `dashboard/dashboard_config.toml` nem része a telepítésnek — mindkettőt
    magadnak kell létrehoznod, a [Backend konfiguráció](#backend-configuration) és a
    [Dashboard konfiguráció](#dashboard-configuration) szakaszban leírtak szerint. A `license.toml` sem
    része a csomagnak; a digna külön biztosítja, ahogyan a 3. lépés leírja.

### 3. lépés: Telepítsd a licenc fájlt

!!! warning "Fontos"

    A licenc fájl **nem** része a telepítési csomagnak, és külön kerül átadásra a dignától.

1. Keresd meg a számodra átadott `license.toml` fájlt
2. Másold be a digna telepítési gyökérkönyvtárába (ahol a `config.toml` és a `digna` futtatható található)

**Miért fontos ez:**
A licenc fájl tartalmazza a vásárlói információkat, a licenc lejárati dátumát és a digitális aláírást. **Ne módosítsd ezt a fájlt** — bármilyen változtatás érvényteleníti a licencet.

**Könyvtárstruktúra a telepítés után:**

```
digna_installation/
├── config.toml         (konfigurációs fájl)
├── license.toml        (SAJÁT LICENC FÁJL - ide másold)
├── digna               (fő futtatható)
└── dashboard/          (webes felület)
    └── (dashboard fájlok)
```

---

## Backend konfiguráció {: #backend-configuration }

### 1. lépés: Hozd létre és szerkeszd a konfigurációs fájlt

A `config_template.toml` fájl megtalálható a digna telepítési könyvtárában. Ezt csak át kell nevezned `config.toml`-ra.

**Elérési út:** `digna_installation/config.toml`

Nyisd meg a `config.toml`-t egy szövegszerkesztőben és állítsd be az alábbi szekciókat.

#### [app] szekció

Ez a rész a dashboard és a backend közötti, eltérő eredetű erőforrás-megosztást (CORS) állítja be:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard URL-ek | Azok az URL-ek, amelyekről a dashboardot kiszolgálják. Bármely más eredetből érkező böngészőkérést a rendszer elutasít |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Kötelező, hogy a böngésző minden kéréssel elküldje a munkamenet-sütit |

!!! info "Az [app] szekció opcionális"

    A Release 2026.11-től mindkét kulcs, sőt a teljes `[app]` szekció is elhagyható. Ez a helyes
    beállítás, ha egy fordított proxy egyetlen eredet alatt szolgálja ki a dashboardot és a
    backendet: a böngésző ilyenkor nem küld eltérő eredetű kéréseket, és alapértelmezés szerint
    egyik sincs engedélyezve.

#### [repo] szekció

Ez a rész a PostgreSQL adatbázishoz való kapcsolódást konfigurálja:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` vagy IP | A PostgreSQL szerver hosztneve/IP-je |
| `DIGNA_REPO_PORT` | `5432` (alapértelmezett) | A PostgreSQL portja |
| `DIGNA_REPO_DB` | `postgres` | Adatbázis neve |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | A korábban létrehozott séma |
| `DIGNA_REPO_USER` | `digna_user` | A PostgreSQL-ben létrehozott felhasználó |
| `DIGNA_REPO_PASSWORD` | A jelszavad | A séma létrehozásakor beállított jelszó |
| `DIGNA_REPO_SSLMODE` | `prefer` (alapértelmezett) | Opcionális. PostgreSQL SSL mód: `disable`, `allow`, `prefer`, `require`, `verify-ca` vagy `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (alapértelmezett) | Opcionális. A digna által az adattárhoz nyitva tartott kapcsolatok száma |

#### [base] szekció

Ez a rész a biztonsági, cookie- és vizsgálati beállításokat tartalmazza:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_FERNET_KEY` | A fent látható érték | A korábbi kiadások által használt titkosítás kulcsa. Szerepelnie kell; a fent látható értéket kell megtartani |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Az a gazdagép, amelyen a dashboard elérhető. A `""` nem állít be domaint, ami akkor helyes, ha egy proxy egyetlen eredet alatt szolgálja ki a dashboardot és a backendet |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Értéke mindig `true` kell legyen, ha a digna HTTPS-en keresztül érhető el |
| `DIGNA_COOKIE_HTTPONLY` | `true` | A munkamenet-sütit elzárja a szkriptek elől |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 óra) | Munkamenet lejárata másodpercben |
| `DIGNA_MAX_WORKERS` | CPU magok száma - 1 | Az egyszerre futtatható vizsgálatok száma |
| `DIGNA_FRONTEND_BASEURL` | Dashboard URL | Kötelező. Az értesítő üzenetekben lévő hivatkozásokhoz használatos, ezért olyan URL-nek kell lennie, amelyet a címzettek meg tudnak nyitni |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (alapértelmezett) | Opcionális. Ennyi másodpercig futhat egy forrásadatbázison végrehajtott egyetlen lekérdezés, mielőtt megszakad; a `0` kikapcsolja az időkorlátot |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (alapértelmezett) | Opcionális. Ennyi másodpercig vár a rendszer a forrásadatbázishoz való kapcsolódásra; a `0` korlátlan várakozást jelent |

#### [encryption] szekció

Ez a szekció tartalmazza azt a kulcsot, amellyel a tárolóban őrzött érzékeny értékek titkosítva vannak. **Kötelező** — a `config check` FAILED állapotúnak jelenti az `[encryption]` szekciót, ha a kulcs hiányzik.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 kódolású kulcs | Titkosítja a digna tárolóban őrzött érzékeny értékeket |

!!! warning "Védje a config.toml fájlt"

    Ez a kulcs rögzített érték, amely minden digna telepítésben azonos, és éppen ez fejti vissza a tárolóban lévő érzékeny értékeket. Korlátozza a `config.toml` hozzáférését arra a fiókra, amely alatt a digna fut, tartsa a fájlt verziókövetésen és megosztott meghajtókon kívül, és hagyja ki minden olyan mentésből, amelyet a tárolónál kevésbé biztonságosan őriznek.

#### [logging] szekció

Ez a rész a naplózás viselkedését állítja be:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` vagy `DEBUG` | `INFO` éles környezethez, `DEBUG` hibakereséshez. A `TRACE`, `WARN` és `ERROR` érték is elfogadott |
| `DIGNA_LOGGING_DIR` | `logs` (alapértelmezett) | Opcionális. A rotált naplófájlok könyvtára, a munkakönyvtárhoz viszonyítva |
| `DIGNA_LOGGING_MAX_FILES` | `30` (alapértelmezett) | Opcionális. A megőrzött rotált naplófájlok száma |

!!! warning "Szolgáltatásként futtatva tartsd meg a naplókönyvtárat"

    A Windows-szolgáltatásnak nincs konzolja, így a naplófájlok jelentik az egyetlen feljegyzést arról,
    mit csinál a szolgáltatás. Ne állítsd a `DIGNA_LOGGING_DIR` értékét üres karakterláncra, mert az
    kikapcsolja a naplófájlokat.

#### [duckdb] szekció (opcionális) {: #duckdb-section }

Újdonság a Release 2026.11-ben. Ez a szekció a **digna Engine** erőforrásait állítja be. A digna Engine
a dignán belül profilozza az adatokat azoknál az adatbázis-kapcsolatoknál, amelyek profilozási helye
**digna Engine**, és referenciális integritási ellenőrzéseket futtat a különböző adatbázis-kapcsolatokon
lévő adatforrások között. Lásd: [Profilozási hely](../../../platform/profiling/profiling_location.md).

A szekció opcionális. Nélküle az alábbi alapértelmezett értékek érvényesek.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (alapértelmezett) | Egy digna Engine-futás által használható memória MB-ban. Egyszerre legfeljebb `DIGNA_MAX_WORKERS` futás lehet aktív |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Alapértelmezés: a dignát futtató fiók ideiglenes könyvtára (`%TEMP%`) | Az ideiglenes fájlok könyvtára arra az esetre, ha az adatok nem férnek el a memóriában |

!!! tip "A digna Engine méretezése"

    A digna gazdagépen a digna saját memóriaigényén felül legfeljebb `DIGNA_MAX_WORKERS` ×
    `DIGNA_DUCKDB_MEMORY_LIMIT_MB` memóriával kell számolni, az ideiglenes könyvtárban pedig annyi
    szabad lemezterülettel, amennyi a digna Engine-t használó adatforrások legnagyobb vizsgált napjának
    adatait befogadja. A `DIGNA_DUCKDB_TEMP_DIRECTORY` beállítást egy ekkora szabad hellyel rendelkező
    lemezre kell irányítani, amelyre a dignát futtató fiók írni tud:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Erre a szekcióra csak akkor van szükség, ha legalább egy adatbázis-kapcsolat a digna Engine-t
    használja, vagy egy referenciális integritási ellenőrzés különböző kapcsolatokon lévő
    adatforrásokat hasonlít össze.

---

### 2. lépés: Ellenőrizze a konfigurációt

A tároló inicializálása előtt ellenőrizze, hogy a `config.toml` teljes és helyesen felépített. A digna telepítési könyvtárában futtassa:

```bash
digna config check
```

Minden szekció külön kerül ellenőrzésre, így egyetlen hiba nem takarja el a többi állapotát:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Javítson ki mindent, amit FAILED állapotúként jelent, és a folytatás előtt futtassa újra a parancsot. Az **Unknown keys** alatti WARNING azokat a `config.toml`-ban lévő kulcsokat sorolja fel, amelyeket a digna nem olvas be; ezeknek nincs hatásuk, ezért el kell távolítani őket, vagy ki kell javítani a nevüket. A beállítások teljes listája a [CLI-referenciában](../../../cli/Command_Line_Interface_202611.md) található.

### 3. lépés: Inicializáld az adattárat (repository)

1. Nyisd meg a Parancssort
2. Navigálj a digna telepítési könyvtárába (ahol a `config.toml` és a `digna` futtatható található)
3. Futtasd a kapcsolat tesztet:

```bash
digna repo check
```

Új séma esetén a parancs csatlakozik, majd jelzi, hogy még nincs telepített adattár:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Ezen a ponton ez a várt eredmény: megerősíti, hogy a digna eléri a PostgreSQL-t és a sémát. Kapcsolódási vagy hitelesítési hiba esetén viszont a `[repo]` szekcióban vagy a PostgreSQL beállításában van a hiba.

### 4. lépés: Telepítsd a séma tábláit az adattárba

Ugyanebben a könyvtárban futtasd:

```bash
digna repo upgrade
```

Ez a parancs létrehozza a szükséges táblákat az adattár sémájában, és a következő üzenettel zárul:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "A repo upgrade telepít és frissít"

    A Release 2026.11-től a `repo upgrade` új adattárat telepít, a meglévőt pedig frissíti.
    A `repo install` továbbra is működik, ugyanennek a parancsnak a másik neveként.

### 5. lépés: Hozz létre egy admin felhasználót

1. Nyiss meg egy **új** Parancssor ablakot
2. Navigálj a digna telepítési könyvtárába
3. Futtasd az alábbi parancsot egy admin felhasználó létrehozásához:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Példa:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Ez létrehoz egy teljes adminisztrátori jogosultságokkal rendelkező felhasználót.

!!! tip "Legjobb gyakorlat"

    Használj erős jelszót, amely tartalmaz nagy- és kisbetűket, számokat és speciális karaktereket.

---

### 6. lépés: Indítsd el a digna szervert

A digna telepítési könyvtárában indítsd el a szervert:

```bash
digna serve --address <host> --port <port>
```

**Paraméterek:**
- `--address` — szerver hosztneve/IP-je (alapértelmezett: `127.0.0.1`)
- `--port` — szerver portja (alapértelmezett: `8000`)

Amikor a szerver elindult, kiírja a címet, amelyen figyel:

```text
Server running on http://127.0.0.1:8082
```

!!! note "A kiszolgáló lefoglalja a terminált"

    A `serve` az előtérben fut, és addig működik, amíg le nem állítja a ++ctrl+c++ billentyűkkel. Hagyja futni, amíg befejezi a beállítást; ha inkább rendszerindításkor indulna automatikusan, lásd: [A digna futtatása Windows-szolgáltatásként](#running-digna-as-a-windows-service).

## Dashboard konfiguráció {: #dashboard-configuration }

### 1. lépés: Telepítsd a dashboardot a webkiszolgálóra

A digna dashboard a saját konfigurációját a `dashboard/dashboard_config.toml` fájlból olvassa. Ez a fájl nem része a telepítésnek — neked kell létrehoznod a `dashboard/` könyvtárban, a dashboard fájljai mellett.

A tartalmát az [Egyszeri bejelentkezés (SSO)](../../../sso/overview.md) oldal írja le, és ott is van rá szükség: ez tartalmazza a dashboard által kínált bejelentkezési lehetőségeket, valamint többinstanciás telepítéseknél a backend kapcsolatot.

Válaszd ki a webkiszolgálót, és kövesd az alábbi telepítési lépéseket.

#### Telepítés IIS-re

1. **Nyisd meg az IIS Manager-t**
   - Nyomd meg a `Win + R`, írd be `inetmgr`, majd Enter

2. **Hozz létre egy új webhelyet**
   - A bal oldali panelen jobb klikk a **Sites**-ra
   - Válaszd az **Add Website...** opciót

3. **Konfiguráld a webhelyet**
   - **Site Name**: Adj nevet (például "dignaDashboard")
   - **Physical Path**: Kattints a Tallózásra és válaszd ki a `dashboard` mappádat
   - **Binding**: Állítsd be az IP címet és portot (alapértelmezett port HTTP-hez 80, HTTPS-hez 443)

4. **Indítsd el a weboldalt**
   - Kattints az **OK** gombra a webhely létrehozásához
   - Jobb klikk az új webhelyen és válaszd a **Start** opciót

5. **Ellenőrizd a telepítést**
   - Nyisd meg a böngészőt
   - Navigálj a `http://localhost` (vagy a konfigurált URL) címre
   - A digna dashboard bejelentkező oldalának kell megjelennie

#### Telepítés Apache Tomcat-re

1. **Másold a dashboardot a Tomcat-hez**
   - Másold a `dashboard` mappát a Tomcat `webapps` könyvtárába
   - Szükség szerint nevezd át (pl.: `digna`)
   - Példa: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Ellenőrizd a telepítést**
   - Frissítsd vagy töltsd újra a Tomcat kezelőfelületét (http://localhost:8080)
   - Látnod kell a "digna" (vagy a választott név) elemet a telepített alkalmazások között

3. **Elérése**
   - Nyisd meg a böngészőt
   - Navigálj a `http://localhost:8080/digna` címre
   - A digna dashboard bejelentkező oldalának kell megjelennie

---

## digna futtatása Windows szolgáltatásként {: #running-digna-as-a-windows-service }

### Miért érdemes Windows szolgáltatásként futtatni?

A digna backend Windows szolgáltatásként való futtatása biztosítja, hogy a szolgáltatás:
- Automatikusan elinduljon a szerver bootolásakor
- Háttérben fusson anélkül, hogy nyitva kellene tartani egy Parancssort
- Automatikusan újrainduljon, ha összeomlik
- A Windows Szolgáltatások felületen keresztül menedzselhető legyen

### A `windows` parancsok

A szolgáltatást maga a `digna` futtatható állomány kezeli, a `digna windows`
alparancsokon keresztül. Nincs szükség batch fájlok futtatására.

| Parancs | Cél |
|---|---|
| `digna windows install` | digna regisztrálása Windows szolgáltatásként |
| `digna windows start` | a regisztrált szolgáltatás indítása |
| `digna windows stop` | a futó szolgáltatás leállítása |
| `digna windows uninstall` | a szolgáltatás regisztrációjának törlése |

!!! warning "Rendszergazdai jogosultság szükséges"

    Mind a négy parancsot rendszergazdaként megnyitott Parancssorból kell futtatni.

Minden parancs elfogadja a `--name` kapcsolót, amellyel egy nem alapértelmezett néven regisztrált
szolgáltatást címezhetsz meg. A teljes opciólista a [CLI referenciában](../../../cli/Command_Line_Interface_202611.md) található.

### A szolgáltatás telepítése

1. **Nyisd meg a Parancssort rendszergazdaként**
   - Jobb klikk a Parancssorra
   - Válaszd a "Futtatás rendszergazdaként" opciót

2. **Navigálj a digna telepítési könyvtáradba**
   ```bash
   cd C:\path\to\digna
   ```

3. **Regisztráld a szolgáltatást**
   ```bash
   digna windows install
   ```

!!! important "Add meg a címet és a portot, hacsak az alapértékek nem felelnek meg"

    Az `install` rögzíti a címet és a portot a szolgáltatás regisztrációjában, és a szolgáltatás
    pontosan a rögzített értékekhez kötődik. Az alapértékek `127.0.0.1` és `8000`, amelyek csak
    magáról a gépről fogadnak kapcsolatot. Egy másik gépen futó dashboard ezt nem éri el, ezért add
    meg azt a címet, amelyen a backendnek figyelnie kell:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Ezeket az értékeket a rendszer nem a `config.toml` fájlból olvassa. Ha később módosítani
    szeretnéd őket, távolítsd el a szolgáltatást, és telepítsd újra az új értékekkel.

A szolgáltatás **automatikus indítással** van regisztrálva, így a Windows-zal együtt indul. Azonnal
nem indul el — lásd a következő szakaszt.

#### Telepítési opciók

| Opció | Alapérték | Cél |
|---|---|---|
| `--name` | `digna` | A név, amelyen a szolgáltatás regisztrálva lesz |
| `--display-name` | `digna` | A services.msc-ben megjelenő név |
| `--description` | `digna data quality backend` | A services.msc-ben megjelenő leírás |
| `--address` | `127.0.0.1` | A cím, amelyhez a szolgáltatás az API-ját köti |
| `--port` | `8000` | A port, amelyhez a szolgáltatás az API-ját köti |
| `--working-dir` | a `digna` futtatható állomány könyvtára | A `config.toml` és a `license.toml` fájlt tartalmazó könyvtár, amelyet a szolgáltatás munkakönyvtárként használ |
| `--start-type` | `auto` | Az `auto` a Windows-zal együtt indul, a `manual` csak kérésre indul, a `disabled` regisztrálja a szolgáltatást, de nem engedi elindítani |
| `--account` | `LocalSystem` | A fiók, amelynek nevében a szolgáltatás fut, pl. `DOMAIN\user` vagy `.\user` |
| `--password` | | A `--account` fiók jelszava |

!!! tip "Futtatás tartományi fiókkal"

    A `LocalSystem` fióknak nincs hálózati identitása, ezért a SQL Serverrel szembeni Windows-hitelesítés
    és a hálózati megosztások elérése sikertelen lesz. Telepítsd a `--account` és a `--password`
    kapcsolóval, ha a szolgáltatásnak egy adott felhasználóként kell erőforrásokat elérnie.

### A szolgáltatás indítása és leállítása

#### Szolgáltatás indítása

```bash
digna windows start
```

#### Szolgáltatás leállítása

```bash
digna windows stop
```

!!! tip "Tipp"

    Mindig állítsd le a szolgáltatást az alkalmazás fájlok frissítése előtt.

### Áthelyezés új könyvtárba a szolgáltatásnál

Ha át kell helyezned a digna telepítést:

1. **Állítsd le és töröld a jelenlegi szolgáltatás regisztrációját**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Mozgasd az alkalmazás fájlokat**
   - Mozgasd az egész digna telepítési mappát az új helyre

3. **Regisztráld újra a szolgáltatást az új helyről**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Add meg újra az első alkalommal használt `--address`, `--port` vagy `--account` értékeket — a
   korábbi regisztráció már nem létezik.

4. **Indítsd el a szolgáltatást**
   ```bash
   digna windows start
   ```

### A szolgáltatás eltávolítása

1. **Állítsd le a futó szolgáltatást**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Töröld a szolgáltatás regisztrációját**
   ```bash
   digna windows uninstall
   ```

A digna szerver mostantól nincs regisztrálva Windows szolgáltatásként.

---

## Frissítés új kiadásra {: #upgrading-to-a-new-release }

Ez a szakasz egy Release 2026.06 telepítés Release 2026.11-re történő frissítését írja le. Ha a
telepítésed régebbi, először olvasd el a [Frissítés 2026.06-nál régebbi kiadásról](#upgrading-from-a-release-before-2026-06)
című részt.

### Mielőtt frissítenél

**A digna adattár biztonsági mentése kötelező**

A digna frissítése előtt készíts biztonsági mentést az adattárról (PostgreSQL), hogy elkerüld az
adatvesztést. A mentés biztosítja, hogy vissza tudd állítani az adatokat, ha a frissítés során váratlan
probléma lép fel.

**A Release 2026.11 licencfájljának igénylése**

A Release 2026.11 új `license.toml` fájlt igényel. Kérd el a digna csapattól még a kezdés előtt, és
tartsd készenlétben a [7. lépéshez](#step-7-replace-the-license-file).

### Frissítés 2026.06-nál régebbi kiadásról {: #upgrading-from-a-release-before-2026-06 }

A Release 2026.06 három olyan változást hozott, amely akkor is érvényes, ha egy régebbi telepítést
közvetlenül 2026.11-re frissítesz:

- **Csak ODBC.** A digna minden forrástechnológiát ODBC-n keresztül ér el. Minden olyan
  adatbázis-kapcsolatot, amely még nem ODBC-t használ, a frissítés után át kell állítani ODBC-re;
  automatikus átalakítás nincs. Előzetesen telepítsd az ODBC-illesztőprogramokat a digna
  gazdagépre, lásd: [Az ODBC-illesztőprogram telepítése a digna gazdagépre](../../../databases/overview.md#install-the-driver),
  és készítsd elő minden kapcsolat tulajdonságait a
  [technológiai útmutatók](../../../databases/overview.md#technology-guides) alapján. A Databricks Legacy
  csatlakozó már nem létezik; költöztesd át ezeket a kapcsolatokat a
  [Databricks](../../../databases/databricks_connector_guide.md) csatlakozóra.
- **Egyetlen futtatható fájl.** A `dignabackend` és a `dignacli` helyét az egyetlen `digna` futtatható
  fájl veszi át, amely egyesíti a backendet és a CLI-t.
- **config.toml.** Az `[encryption]` szekció kötelező, a `DIGNA_APP_HOST` és a `DIGNA_APP_PORT`
  beállítást pedig a digna már nem olvassa be: a szerver a címét és a portját a `digna serve`
  parancstól kapja. Vesd össze a fájlodat a [Backend konfiguráció](#backend-configuration) résszel.

Az alábbi lépések jelzik, hol igényel egy régebbi telepítés eltérő eljárást. A 8. lépésben
az adattár frissítése bármely korábbi kiadás adattárát közvetlenül 2026.11-re hozza.

### Frissítési folyamat

#### 1. lépés: Állítsd le a digna szolgáltatást {: #step-1-stop-the-digna-service }

Nyiss meg egy Parancssort rendszergazdaként, és állítsd le a szolgáltatást a jelenlegi telepítésed
`digna` futtatható fájljával:

```bash
cd C:\path\to\digna
digna windows stop
```

A szolgáltatás regisztrálva marad. Az új futtatható fájl ugyanabban a könyvtárban veszi át a régi
helyét, így a regisztráció továbbra is a megfelelő fájlra mutat.

Ha a digna előtérben fut, nyomd meg a ++ctrl+c++ billentyűket a Parancssor ablakában.

!!! warning "Frissítés 2026.06-nál régebbi kiadásról"

    A 2026.06-nál régebbi kiadások batch fájlokkal regisztrálták a szolgáltatást. Állítsd le, és töröld
    a regisztrációját a jelenlegi telepítésed batch fájljaival, **mielőtt** a 2. lépésben bármit
    átneveznél:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Jegyezd fel, milyen fiók alatt futott a szolgáltatás, valamint milyen címen és porton szolgált ki.
    A 9. lépésben újra regisztrálni fogod a szolgáltatást.

#### 2. lépés: Mentse a jelenlegi telepítést {: #step-2-backup-current-installation }

A digna telepítési könyvtárában nevezd át a jelenlegi telepítés futtatható fájlját és dashboard
mappáját, hogy az új kiadás melléjük telepíthető legyen:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

A `digna_old.exe` fájlt tartsd meg, amíg nem ellenőrizted a frissítést, a `dashboard_old` mappát
pedig addig, amíg vissza nem állítottad belőle a konfigurációs fájljaidat (lásd a 4. lépést).
Utána mindkettő törölhető.

!!! info "Frissítés 2026.06-nál régebbi kiadásról"

    A futtatható fájl helyett a `dignabackend` és a `dignacli` mappát nevezd át:
    `ren dignabackend dignabackend_old` és `ren dignacli dignacli_old`. A Release 2026.11 egyik mappát sem használja, és a batch fájlokat tartalmazó `bin` mappát sem.

#### 3. lépés: Csomagold ki és telepítsd az új verziót {: #step-3-extract-and-deploy-new-version }

1. Csomagold ki az új digna telepítő ZIP fájlt
2. Másold az új `digna` futtatható fájlt és a `dashboard` mappát a telepítési könyvtárba

!!! warning "Fontos"

    Sem a `config.toml`, sem a `dashboard/dashboard_config.toml` **soha** nem része a
    telepítési ZIP-nek — a digna csapat egyik fájlt sem szállítja. A meglévő konfigurációdat
    ezért a frissítés nem érinti, és az átnevezett `*_old` mappákban lévő példányok az
    egyetlenek, amelyekkel rendelkezel.

#### 4. lépés: Állítsd vissza a konfigurációs fájlokat {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

A Release 2026.11 nem igényel változtatást a `config.toml` fájlban: a Release 2026.06-tal működő fájl
továbbra is működik. Két módosítás opcionális:

- Adj hozzá egy [`[duckdb]` szekciót](#duckdb-section), ha az adatbázis-kapcsolatoknak a digna
  Engine-t kell használniuk, és annak alapértelmezett értékei nem felelnek meg a gazdagépnek.
- Hagyd el az `[app]` szekciót, ha egy fordított proxy egyetlen eredet alatt szolgálja ki a
  dashboardot és a backendet.

!!! warning "Beállítások, amelyeket a digna nem olvas be"

    Az útmutató korábbi változatai olyan beállításokat is tartalmaztak, amelyeket a digna nem olvas
    be. Ezeknek nincs hatásuk, és a `config check` a 6. lépésben az **Unknown keys** alatt sorolja fel
    őket. Távolítsd el vagy javítsd ki őket:

    - A `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` és
      `digna_LOGGING_BACKUP_COUNT` beállítás nem létezik. Távolítsd el őket.
    - A beállítások neve megkülönbözteti a kis- és nagybetűket. A digna a `DIGNA_REPO_HOST` kulcsot
      olvassa be, nem a `digna_REPO_HOST` kulcsot. Minden nevet nagybetűvel írj, ahogy a
      [Backend konfiguráció](#backend-configuration) részben.

!!! warning "Egyszeri bejelentkezés: tartsd meg az [[oidc_clients]] formát"

    A digna az egyszeri bejelentkezés szolgáltatóit `[[oidc_clients]]` bejegyzések listájaként
    olvassa be, mindegyiket saját `DIGNA_OIDC_KEY` kulccsal. Ha a szolgáltatóidat
    `[oidc_clients.<key>]` szekciókra alakítottad át, ahogy az útmutató egy korábbi változata
    mutatta, alakítsd vissza őket. A `config check` mindaddig FAILED állapotúnak jelenti az
    `OIDC config(s)` elemet, amíg ez a forma van érvényben:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Ismételd meg a bejegyzést minden szolgáltatóhoz, és minden `DIGNA_OIDC_KEY` legyen azonos a
    `dashboard_config.toml` fájlban lévő `key` értékkel. Ez csak az egyszeri bejelentkezést használó
    telepítéseket érinti.

#### 5. lépés: Töltsd újra a webkiszolgálót {: #step-5-reload-the-web-server }

A dashboard statikus fájlok összessége, ezért előfordulhat, hogy a webkiszolgáló — és a böngésző —
még az előző verziót szolgálja ki. Töltsd újra vagy indítsd újra azt a webkiszolgálót, amely a
`dashboard` mappát kiszolgálja, majd töltsd be újra az oldalt kényszerített frissítéssel (++ctrl+f5++).

#### 6. lépés: Ellenőrizze a konfigurációt {: #step-6-validate-the-configuration }

Mielőtt az adattárhoz nyúlnál, győződj meg róla, hogy a `config.toml` teljes:

```bash
digna config check
```

Minden szekciónak OK állapotot kell jelentenie. Javíts ki mindent, amit FAILED állapotúként jelent,
távolítsd el az **Unknown keys** alatt felsorolt kulcsokat, és a folytatás előtt futtasd újra
a parancsot.

#### 7. lépés: Cseréld le a licencfájlt {: #step-7-replace-the-license-file }

A licencfájl általában átvihető egyik kiadásról a másikra. A Release 2026.11 kivétel: két
licencköteles modult vezet be, a digna Data Reconciliation-t és a digna Agentic-et, és a 2026.11 előtt
kiállított licenc ezeket nem tartalmazza. Másold a digna csapat által a Release 2026.11-hez
biztosított `license.toml` fájlt a telepítési könyvtárba, felülírva a régit:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Ne tartsd meg a korábbi licencet"

    A korábbi licenccel a digna ugyan elindul, de a digna Data Reconciliation és a digna MCP Server
    kikapcsolva marad. Minden parancs, amely ellenőrzi a licencet — `user`, `inspection`, `repo` —
    megszakad, mielőtt az adattárhoz nyúlna, ha az ellenőrzés sikertelen. Ellenőrizd az új
    licencet, mielőtt továbblépsz:

    ```bash
    digna license check
    ```

#### 8. lépés: Frissítsd az adattár sémáját {: #step-8-upgrade-the-repository-schema }

A digna telepítési könyvtárában futtasd:

```bash
digna repo upgrade
```

A Release 2026.11 verziózott migrációkkal kezeli az adattár sémáját. Egy korábbi kiadásról végzett első
frissítés a sémát az előző rendszer utolsó verziójára hozza, ezt kiindulópontként rögzíti, majd
alkalmazza a Release 2026.11 migrációit. A végén ezt írja ki:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Minden meglévő adat megmarad. Az adattár állapotát bármikor megtekintheted a
`digna repo check` paranccsal: kilistázza a legutóbb alkalmazott migrációt és a még függőben lévőket.

!!! warning "A digna nem indul el elavult adattárral"

    A Release 2026.11-től a szerver nem hajlandó elindulni, amíg az adattár frissítésre szorul, és ezt
    jelzi is, például:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    A szerver vagy a szolgáltatás indítása előtt futtasd a `repo upgrade` parancsot.

#### 9. lépés: Indítsd újra a szolgáltatásokat {: #step-9-restart-services }

Ha a digna Windows-szolgáltatásként fut, indítsd el újra:

```bash
cd C:\path\to\digna
digna windows start
```

Ha 2026.06-nál régebbi kiadásról frissítettél, és az 1. lépésben törölted a szolgáltatás
regisztrációját, előbb regisztráld újra a `digna` futtatható fájllal:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

A `--address` és a `--port` kapcsolónak add meg azokat az értékeket, amelyeken a régi szolgáltatás
kiszolgált, hacsak nem a `127.0.0.1` és `8000` alapértelmezett értékeket szeretnéd. Ha a régi
szolgáltatás tartományi fiók alatt futott, add hozzá a `--account` és `--password` kapcsolót. A teljes
opciólistát lásd: [digna futtatása Windows szolgáltatásként](#running-digna-as-a-windows-service).

Ha manuálisan futtatod, indítsd újra a szervert:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Ha IIS-t vagy Tomcatet használsz, indítsd újra a megfelelő webkiszolgálót.

#### 10. lépés: Ellenőrizd a frissítést {: #step-10-verify-the-upgrade }

1. Ellenőrizd az új futtatható fájl kiadását:

    ```bash
    digna version
    ```

    Az első sornak így kell szólnia: `Release: 2026.11`.

2. Nyisd meg a digna dashboardot, és ellenőrizd, hogy a felület helyesen töltődik-e be.
3. Nézd át a telepítés `logs` könyvtárában lévő fájlokat esetleges hibákért.
4. Teszteld az adatbázis-kapcsolatokat — lásd:
   [Kapcsolat tesztelése](../../../databases/overview.md#testing-a-connection). Egy 2026.06-nál régebbi
   kiadásról végzett frissítés után előbb állítsd át ODBC-re mindazokat a kapcsolatokat, amelyek
   még nem ODBC-t használtak.

Az új modulok használatának megkezdéséhez lásd: [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI-ügynök csatlakoztatása](../../../platform/agentic/connect_ai_agent.md) a digna MCP Serverhez, valamint
[Profilozási hely](../../../platform/profiling/profiling_location.md) a digna Engine-hez.