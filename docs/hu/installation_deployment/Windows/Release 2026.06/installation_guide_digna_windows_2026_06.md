---
title: Windows telepítési útmutató – digna Release 2026.06 | digna dokumentáció
description: Lépésről lépésre útmutató a digna Release 2026.06 Windows rendszeren történő telepítéséhez — rendszerkövetelmények, PostgreSQL beállítása, webkiszolgáló konfigurálása, backend és dashboard konfiguráció, digna futtatása Windows szolgáltatásként és frissítés új kiadásra.
keywords: digna windows telepítés, digna telepítési útmutató, digna backend beállítás, digna dashboard telepítés, postgresql beállítás, digna windows szolgáltatás, digna frissítési útmutató
image: /assets/logo_square.png
---

# digna Release 2026.06 Windows telepítési útmutató

**Kiadás:** 2026.06

**Utoljára frissítve:** 2026. augusztus 30.


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

### Mi újság a 2026.06-os kiadásban

Ez a kiadás az adatmegfigyelhetőségi képességeket közvetlenül a kódban hozza el, lehetővé téve a fejlesztők számára az adatok minőségének forrásnál történő monitorozását. A teljes részletekért lásd a [release notes](http://docs.digna.ai/changelog/Release_202606/)-t.

### macOS vagy Linux telepítést keresel?

Ez az útmutató Windowsra vonatkozik. Más platformokhoz lásd a [macOS telepítési útmutatót](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) vagy a [Linux telepítési útmutatót](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — konfigurációs fájl
   - `license.toml` — licenc fájl (másold ide a sajátodat)

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

Ez a rész a digna backend alkalmazás beállításait tartalmazza:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_APP_HOST` | `localhost` vagy IP cím | A hoszt vagy IP, ahol a dignabackend fut |
| `digna_APP_PORT` | `8082` (alapértelmezett) | A REST API végpontok portja |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Ha a dashboard másik szerveren fut, add meg annak URL-jét |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Szükséges CORS-hoz hitelesítő adatokkal |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Minden HTTP metódus engedélyezése |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Minden fejléc engedélyezése |

#### [repo] szekció

Ez a rész a PostgreSQL adatbázishoz való kapcsolódást konfigurálja:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_REPO_HOST` | `localhost` vagy IP | A PostgreSQL szerver hosztneve/IP-je |
| `digna_REPO_PORT` | `5432` (alapértelmezett) | A PostgreSQL portja |
| `digna_REPO_DB` | `postgres` | Adatbázis neve |
| `digna_REPO_SCHEMA` | `dignarepo` | A korábban létrehozott séma |
| `digna_REPO_USER` | `digna_user` | A PostgreSQL-ben létrehozott felhasználó |
| `digna_REPO_PASSWORD` | A jelszavad | A séma létrehozásakor beállított jelszó |

#### [base] szekció

Ez a rész a biztonsági és cookie beállításokat tartalmazza:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Illeszkedjen a frontend domainhez |
| `digna_COOKIE_SECURE` | `false` (lokális) / `true` (éles) | Éles környezetben HTTPS esetén állítsd `true`-ra |
| `digna_COOKIE_HTTPONLY` | `true` | Biztonsági okokból mindig engedélyezett |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF elleni védelem |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 óra) | Munkamenet lejárata másodpercben |
| `digna_MAX_WORKERS` | CPU magok száma - 1 | Párhuzamos ellenőrzési feladatok száma |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximális késleltetés másodpercben, amelyet az ütemező hozzáadhat egy esedékes feladat indítása előtt |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Napszak (24 órás `HH:MM` formátum), amikor a napi takarítás indul |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` vagy `DEBUG` | `INFO` éles környezethez, `DEBUG` hibakereséshez |
| `digna_LOGGING_BACKUP_COUNT` | `10` | A megtartott napi naplómentések száma |

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

Overall: OK
```

Javítson ki mindent, amit FAILED állapotúként jelent, és a folytatás előtt futtassa újra a parancsot. A beállítások teljes listája a [CLI-referenciában](../../../cli/Command_Line_Interface_202606.md) található.

### 3. lépés: Inicializáld az adattárat (repository)

1. Nyisd meg a Parancssort
2. Navigálj a digna telepítési könyvtárába (ahol a `config.toml` és a `digna` futtatható található)
3. Futtasd a kapcsolat tesztet:

```bash
digna repo check
```

Meg kell jelennie egy megerősítésnek, hogy a kapcsolat létrejött (magát az adattárat még nem inicializáltuk).

### 4. lépés: Telepítsd a séma tábláit az adattárba

Ugyanebben a könyvtárban futtasd:

```bash
digna repo install
```

Ez a parancs létrehozza a szükséges táblákat és sémát a PostgreSQL adatbázisban.

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
- `--address` — szerver hosztneve/IP-je
- `--port` — szerver portja 

Induláskor a következő típusú üzeneteket kell látnod:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "A kiszolgáló lefoglalja a terminált"

    A `serve` az előtérben fut, és addig működik, amíg le nem állítja a ++ctrl+c++ billentyűkkel. Hagyja futni, amíg befejezi a beállítást; ha inkább rendszerindításkor indulna automatikusan, lásd: [A digna futtatása Windows-szolgáltatásként](#running-digna-as-a-windows-service).

## Dashboard konfiguráció {: #dashboard-configuration }

### 1. lépés: Telepítsd a dashboardot a webkiszolgálóra

A digna dashboard saját `config.toml` fájllal rendelkezik a `dashboard/` könyvtárban. Ez a konfiguráció alapértelmezetten biztosítva van, és kezdeti telepítéskor általában nincs szükség módosításra. Csak akkor kell módosítanod, ha a backend kapcsolatot testre szeretnéd szabni.

Ha módosítani szeretnéd a dashboard konfigurációját (például többinstanciás telepítésnél), kövesd a dashboard dokumentációját.

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

### Szolgáltatás-kezelő fájlok

Minden szükséges fájl a digna telepítési könyvtárában található: `bin/`

A következő batch fájlok állnak rendelkezésre:
- `install_service.bat` — digna regisztrálása Windows szolgáltatásként
- `uninstall_service.bat` — a szolgáltatás eltávolítása
- `start_service.bat` — a szolgáltatás indítása
- `stop_service.bat` — a szolgáltatás leállítása

!!! warning "Rendszergazdai jogosultság szükséges"

    Minden batch fájlt rendszergazdai jogosultságokkal kell futtatni.

### A szolgáltatás telepítése

1. **Nyisd meg a Parancssort rendszergazdaként**
   - Jobb klikk a Parancssorra
   - Válaszd a "Futtatás rendszergazdaként" opciót

2. **Navigálj a bin mappába**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Futtasd a telepítő scriptet**
   ```bash
   install_service.bat
   ```

A digna szerver mostantól regisztrálva van Windows szolgáltatásként automatikus indítással engedélyezve. Maga a szolgáltatás még nem indul el — a következő szakaszban indíthatod el.

### A szolgáltatás indítása és leállítása

#### Szolgáltatás indítása

1. Nyisd meg a Parancssort rendszergazdaként
2. Navigálj a `digna\bin` mappába
3. Futtasd:
   ```bash
   start_service.bat
   ```

#### Szolgáltatás leállítása

1. Nyisd meg a Parancssort rendszergazdaként
2. Navigálj a `digna\bin` mappába
3. Futtasd:
   ```bash
   stop_service.bat
   ```

!!! tip "Tipp"

    Mindig állítsd le a szolgáltatást az alkalmazás fájlok frissítése előtt.

### Áthelyezés új könyvtárba a szolgáltatásnál

Ha át kell helyezned a digna telepítést:

1. **Távolítsd el a jelenlegi szolgáltatást**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Mozgasd az alkalmazás fájlokat**
   - Mozgasd az egész digna telepítési mappát az új helyre

3. **Telepítsd újra a szolgáltatást**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Indítsd el a szolgáltatást**
   ```bash
   start_service.bat
   ```

### A szolgáltatás eltávolítása

1. **Állítsd le a futó szolgáltatást**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Távolítsd el a szolgáltatást**
   ```bash
   uninstall_service.bat
   ```

A digna szerver mostantól nincs regisztrálva Windows szolgáltatásként.

---

## Frissítés új kiadásra {: #upgrading-to-a-new-release }

### Mielőtt frissítenél

**Először ellenőrizze az összes adatbázis-kapcsolatot**

A 2026.06 kiadástól a digna minden forrástechnológiát **ODBC**-n keresztül ér el. A korábbi kiadások választást kínáltak a technológiánkénti illesztőprogram és az ODBC között, a **Use ODBC** kapcsolóval. A digna csapata úgy döntött, hogy kizárólag az ODBC-re épít, mert egyetlen szabványos felület többet ad, mint egy sor testreszabott illesztőprogram:

- **Hitelesítés** — a hitelesítés az ODBC része, így egy kapcsolat mindent használhat, amit az illesztőprogramja támogat: jelszavakat, tokeneket és PAT-okat, Kerberost és Active Directoryt, MFA-t és böngészőalapú egyszeri bejelentkezést, felhőidentitásokat, ügyféltanúsítványokat és TLS-t. Az új módszerek az illesztőprogram frissítésével érkeznek, nem pedig egy digna kiadásra várva.
- **Az adatbázis-gyártók által karbantartott illesztőprogramok** — a gyártó saját illesztőprogramja követi az új kiszolgálóverziókat és a biztonsági javításokat, és Ön a saját ütemezése szerint frissítheti, a dignától függetlenül.
- **Egyetlen mód mindent beállítani** — minden technológia kulcs-érték tulajdonságok listája, ugyanazzal a felülettel, az érzékeny értékek ugyanolyan titkosításával és ugyanazzal a hibakereséssel, ahelyett hogy forrásonként más mezőkészlet lenne.
- **Hangolás és lefedettség** — az illesztőprogram-szintű beállítások, mint az időtúllépések, a TLS-beállítások, a proxyk és a lekérési méretek minden forráshoz elérhetők, és bármely technológia csatlakoztatható, amelyhez szabványos ODBC-illesztőprogram létezik, azok is, amelyekhez a digna nem ad ki külön útmutatót.

A gyakorlatban ez azt jelenti, hogy a **Use ODBC** kapcsoló, valamint a külön gazdagép-, port-, adatbázis-, felhasználó- és jelszómezők már nem léteznek. **Minden olyan kapcsolatot, amely még nem ODBC-t használ, át kell állítani ODBC-re** — automatikus átalakítás nincs, ezért tervezze ezt a frissítés előtt:

1. Tekintse át a telepítésében meghatározott valamennyi adatbázis-kapcsolatot, és jegyezze fel azokat, amelyek még nem ODBC-t használnak — mindegyiket újra kell konfigurálni.
2. Telepítse a megfelelő ODBC-illesztőprogramot a digna gazdagépre — a kapcsolatokat az a kiszolgáló nyitja meg, amelyen a digna háttérrendszer fut, nem a böngésző. Lásd: [Az ODBC-illesztőprogram telepítése a digna gazdagépre](../../../databases/overview.md#install-the-driver).
3. Készítse elő az ODBC-tulajdonságokat minden érintett kapcsolathoz. A [technológiai útmutatók](../../../databases/overview.md#technology-guides) forrásonként egy bevált tulajdonságkészletet sorolnak fel.

A frissítés után állítsa át ODBC-re minden érintett kapcsolatot, és tesztelje az irányítópultról — lásd: [Adatbázis-kapcsolat létrehozása](../../../databases/overview.md#create-a-database-connection) és [Kapcsolat tesztelése](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy kapcsolatok"

    A Databricks Legacy csatlakozót ebben a kiadásban eltávolítottuk. Költöztesse át ezeket a kapcsolatokat a [Databricks](../../../databases/databricks_connector_guide.md) csatlakozóra.

**A digna adattár biztonsági mentése kötelező**

A frissítés előtt készíts biztonsági mentést az adattárról (PostgreSQL), hogy védve legyél az adatvesztés ellen. A mentés biztosítja, hogy vissza tudod állítani az állapotot, ha a frissítés közben váratlan problémák merülnének fel.

### Frissítési folyamat

#### 1. lépés: Állítsd le a digna szolgáltatást

Ha a digna Windows szolgáltatásként fut, először állítsd le:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2. lépés: Mentse a jelenlegi telepítést

A digna telepítési könyvtárában nevezze át a jelenlegi telepítés mappáit, hogy az új kiadás melléjük telepíthető legyen:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "a dignabackend és a dignacli már nem használatos"

    A 2026.06 kiadástól a `dignabackend` és a `dignacli` helyét az egyetlen `digna` futtatható fájl veszi át, amely egyesíti a háttérrendszert és a CLI-t. A `dignabackend_old` és a `dignacli_old` mappát csak addig tartsa meg, amíg a frissítést ellenőrizte — utána mindkettőt törölheti. A `dashboard_old` mappát tartsa meg, amíg vissza nem állította belőle a konfigurációs fájljait (lásd a 4. lépést).

#### 3. lépés: Csomagold ki és telepítsd az új verziót

1. Csomagold ki az új digna telepítési ZIP fájlt
2. Másold át az új `digna` futtathatót és a `dashboard` mappát a telepítési könyvtáradba


!!! warning "Fontos"

    A `config.toml` fájl **soha** nincs benne a telepítési ZIP-ben. A meglévő konfigurációd biztonságban marad.

#### 4. lépés: Állítsd vissza a konfigurációs fájlokat

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "A 2026.06 kiadás módosítja a config.toml fájlt"

    Három beállítás új és kötelező, egy pedig már nem használatos. A korábbi kiadásból átvett `config.toml` nem tartalmazza az új beállításokat, és a digna nem indul el, amíg hiányoznak. Egészítse ki a meglévő `config.toml` fájlját a következőkkel:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Adja hozzá a két `[base]` kulcsot a meglévő `[base]` szekcióhoz, és vegye fel az `[encryption]` szekciót újként. Ezután **távolítsa el a `digna_FERNET_KEY` kulcsot** a `[base]` szekcióból — már nem használatos.

    Az egyes beállítások jelentését lásd: [Háttérrendszer konfigurálása](#backend-configuration).

!!! warning "Egyszeri bejelentkezés: az [oidc_clients] formátuma megváltozott"

    A 2026.06 kiadás a táblatömböt szolgáltatónként egy-egy táblára cseréli, amelyet a szolgáltató kulcsáról neveznek el. A `DIGNA_OIDC_KEY` megszűnik — a kulcs mostantól a szakaszfejléc része.

    Előtte:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Utána:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Ismételje meg a szakaszt minden szolgáltatóhoz, és tartsa minden kulcsot azonosnak a `dashboard_config.toml` fájlban lévő `key` értékkel. A `digna config check` FAILED állapotúnak jelenti az `oidc_clients` szakaszt mindaddig, amíg a régi forma megmarad. Ez csak az egyszeri bejelentkezést használó telepítéseket érinti.

#### 5. lépés: Ellenőrizze a konfigurációt

Mielőtt hozzányúlna a tárolóhoz, győződjön meg róla, hogy a frissített `config.toml` teljes:

```bash
digna config check
```

Minden szekciónak OK állapotot kell jelentenie. Javítson ki mindent, amit FAILED állapotúként jelent, és a folytatás előtt futtassa újra a parancsot.

#### 6. lépés: Frissítsd az adattár sémáját

Navigálj a digna telepítési könyvtárába és futtasd:

```bash
digna repo upgrade
```

Ez frissíti a PostgreSQL sémát a legújabb verzióra, miközben megőrzi a meglévő adatokat.

#### 7. lépés: Indítsd újra a szolgáltatásokat

Ha Windows szolgáltatásként fut:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Ha kézzel futtattad korábban, indítsd újra a szervert:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Ha IIS-t vagy Tomcat-et használsz, indítsd újra a megfelelő webkiszolgálót.

#### 8. lépés: Ellenőrizd a frissítést

1. Nyisd meg a digna dashboardot
2. Ellenőrizd, hogy a felület betöltődik-e rendesen
3. Nézd át a szerver naplóit hibák után kutatva
4. Állítsa át ODBC-re mindazokat a kapcsolatokat, amelyek még nem használták, majd tesztelje az összes kapcsolatot — lásd: [Kapcsolat tesztelése](../../../databases/overview.md#testing-a-connection)