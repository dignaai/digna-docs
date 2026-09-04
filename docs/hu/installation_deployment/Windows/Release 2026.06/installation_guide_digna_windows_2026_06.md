---
title: Windows telepítési útmutató – digna Release 2026.06 | digna Dokumentáció
description: Lépésről lépésre útmutató a digna Release 2026.06 Windowsra történő telepítéséhez — rendszerkövetelmények, PostgreSQL beállítás, webszerver konfiguráció, backend és dashboard konfiguráció, digna futtatása Windows szolgáltatásként és verziófrissítés.
keywords: digna windows telepítés, digna telepítési útmutató, digna backend beállítás, digna dashboard telepítés, postgresql beállítás, digna windows szolgáltatás, digna frissítési útmutató
image: /assets/logo_square.png
---

# Windows telepítési útmutató a digna Release 2026.06 verzióhoz

**Release:** 2026.06

**Utolsó frissítés:** 2026. augusztus 30.


---

## Tartalom

1. [Bevezetés](#introduction)
2. [Rendszerkövetelmények](#system-requirements)
3. [Előtelepítési beállítások](#pre-installation-setup)
4. [PostgreSQL szerver beállítása](#postgresql-server-setup)
5. [Webszerver konfiguráció](#web-server-configuration)
6. [Kezdeti telepítés](#initial-installation)
7. [Backend konfiguráció](#backend-configuration)
8. [Dashboard konfiguráció](#dashboard-configuration)
9. [digna futtatása Windows szolgáltatásként](#running-digna-as-a-windows-service)
10. [Frissítés új verzióra](#upgrading-to-a-new-release)

---

## Bevezetés {: #introduction }

### A dignáról

A digna egy átfogó, MI-vezérelt platform, amely a különböző adatkörnyezetekben (warehousok, lake-ek, lakehouse-ok) optimalizálja az adatminőség-kezelést. Nagy skalázhatóságra és alkalmazkodóképességre tervezve a digna automatizálással, valós idejű monitorozással és anomáliaészleléssel kezeli a modern adathasználati kihívásokat.

A digna két fő komponensből áll:

- **dignabackend**: Az alkalmazás magja, amely a feldolgozásért és az adatminőségi ellenőrzésekért felel.
- **dignadashboard**: Webalapú felület, amely webszerveren fut, és felhasználóbarát módon biztosít hozzáférést a digna platformhoz és az adatminőségi mutatók vizualizációjához.

### Mi újság a Release 2026.06 verzióban

Ez a verzió az adatmegfigyelhetőségi (data observability) képességeket közvetlenül a kódba hozza, lehetővé téve a fejlesztők számára az adatminőség forrásnál történő monitorozását. A teljes részletekért lásd a [release notes](http://docs.digna.ai/changelog/Release_202606/) oldalt.

---

## Rendszerkövetelmények {: #system-requirements }

Mielőtt megkezdené a telepítést, győződjön meg róla, hogy rendszere megfelel az alábbi minimális követelményeknek:

| Követelmény | Specifikáció |
|---|---|
| **Operációs rendszer** | Windows Server vagy Windows 10/11 |
| **Memória (minimális telepítés)** | 16 GB RAM |
| **Lemezterület** | 10 GB szabad tárhely |
| **Adatbázis** | PostgreSQL Server 12 vagy újabb |
| **Webszerver** | IIS, Apache Tomcat, vagy egyenértékű |

### Adatbázis telepítési lehetőségek

**Ha a PostgreSQL már telepítve van:**
Hozzáadhat egy új adatbázist a digna számára a meglévő PostgreSQL szerveréhez.

**Ha a PostgreSQL-t ugyanarra a gépre telepíti, ahol a digna fut:**

> **Ajánlott specifikációk**
>
> - **Memória**: 32 GB RAM (a 16 GB helyett)
> - **Lemezterület**: 50 GB szabad tárhely (a 10 GB helyett)
>
> Ezek a magasabb erőforrásigények biztosítják, hogy a digna és a PostgreSQL adatbázis egyszerre, zökkenőmentesen fusson.

---

## Előtelepítési beállítások {: #pre-installation-setup }

A digna telepítése előtt győződjön meg róla, hogy két kulcsfontosságú előfeltétel rendelkezésre áll:

1. **PostgreSQL szerver** – a kiszámított mutatók és teljesítményadatok tárolásához
2. **Webszerver** – a digna Dashboard hosztolásához

Ha ezek a komponensek még nincsenek beállítva, kövesse az alábbi részeket az installációhoz és konfigurációhoz.

---

## PostgreSQL szerver beállítása {: #postgresql-server-setup }

### Ha már van PostgreSQL

Ha a PostgreSQL telepítve van és fut a helyi gépen, vagy menedzselt távoli PostgreSQL szervert használ, ugorhat a [következő szakaszra](#web-server-configuration).

### PostgreSQL telepítése

Kövesse az alábbi lépéseket a PostgreSQL telepítéséhez Windows alatt:

#### 1. lépés: PostgreSQL letöltése

1. Nyissa meg a [PostgreSQL Downloads oldalt](https://www.postgresql.org/download/)
2. Válassza a **Windows** opciót
3. Töltse le a legfrissebb telepítőt

#### 2. lépés: Futtassa a telepítőt

1. Kattintson duplán a letöltött telepítő fájlra
2. Kövesse a telepítővarázsló utasításait

#### 3. lépés: Telepítési könyvtár kiválasztása

Válassza ki a PostgreSQL telepítési könyvtárát. Az alapértelmezett hely általában megfelelő.

#### 4. lépés: Komponensek kiválasztása

Egy szabványos telepítéshez hagyja meg az alapértelmezett komponensbeállításokat.

#### 5. lépés: PostgreSQL szuperfelhasználó jelszó beállítása

Adja meg és erősítse meg a PostgreSQL szuperfelhasználó (`postgres`) jelszavát. **Mentse biztonságosan ezt a jelszót** — később szüksége lesz rá.

#### 6. lépés: Port szám konfigurálása

Az alapértelmezett PostgreSQL port a `5432`. Használhatja az alapértelmezettet vagy megadhat más portot, ha szükséges.

> **Tipp**
>
> Ha a 5432-es port már foglalt, válasszon alternatív portot és jegyezze fel későbbi konfigurációhoz.

#### 7. lépés: Locale kiválasztása

Válassza ki az adatbázis locale-jét. Az alapértelmezett általában megfelelő a legtöbb telepítéshez.

#### 8. lépés: Telepítés befejezése

Kattintson a **Next** gombra a hátralévő lépéseken, majd a **Finish** gombra.

#### 9. lépés: Telepítés ellenőrzése

Nyissa meg a Parancssort és ellenőrizze, hogy a PostgreSQL telepítve van:

```bash
psql --version
```

Ha a telepítés sikeres volt, a PostgreSQL verzióját látni fogja.

---

## Webszerver konfiguráció {: #web-server-configuration }

A digna dashboard hosztolásához szükség van egy webszerverre. Válasszon az alábbi lehetőségek közül:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Csak az egyik webszervert kell telepítenie és konfigurálnia.

### IIS beállítása {: #iis-setup }

#### Áttekintés

Az Internet Information Services (IIS) a Microsoft webszervere, weboldalak és webalkalmazások hosztolásához.

#### IIS engedélyezése

1. **Nyissa meg a Vezérlőpultot**
   - Nyomja meg a `Win + R` billentyűket
   - Írja be: `control` és nyomjon Entert

2. **Menjen a Windows funkciókhoz**
   - Kattintson a **Programok** menüpontra
   - Válassza a **Windows-szolgáltatások be- vagy kikapcsolása** lehetőséget

3. **Kapcsolja be az Internet Information Services-t**
   - Görgessen le és keresse meg az **Internet Information Services (IIS)** elemet
   - Jelölje be a négyzetet az engedélyezéshez
   - Kattintson a **+** jelre a kibontáshoz és ellenőrizze, hogy a következő alkotóelemek ki vannak-e választva:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Kattintson az OK gombra** a változtatások alkalmazásához

5. **IIS telepítés ellenőrzése**
   - Nyisson meg egy böngészőt
   - Navigáljon a `http://localhost` címre
   - Látnia kell az IIS üdvözlő oldalát

#### Szükséges: URL Rewrite modul

Az IIS-hez szükség van az URL Rewrite komponensre. Töltse le és telepítse az [hivatalos Microsoft oldalról](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Szükséges: MIME típus Markdown fájlokhoz

Annak érdekében, hogy a Markdown fájlok (`.md`) megfelelően legyenek kiszolgálva IIS alatt:

1. Nyissa meg az **IIS Manager**-t (nyomja meg a `Win + R`, írja be `inetmgr`, majd Enter)
2. Navigáljon a **Your Site > MIME Types** részhez
3. Kattintson az **Add...** gombra
4. Állítsa be:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **Fontos**
>
> Ennek a beállításnak hiányában a `.md` fájlok előfordulhat, hogy nem lesznek megfelelően kiszolgálva.

---

### Apache Tomcat beállítása {: #apache-tomcat-setup }

#### Áttekintés

Az Apache Tomcat egy nyílt forráskódú Java servlet-konténer és webszerver.

#### Telepítés

1. **Apache Tomcat letöltése**
   - Látogasson el az [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi) oldalra
   - Töltse le a Windows ZIP csomagot

2. **Kicsomagolás**
   - Csomagolja ki a ZIP fájlt egy tetszőleges könyvtárba a rendszeren
   - Példa: `C:\Program Files\Apache Tomcat`

3. **Tomcat futásának ellenőrzése**
   - Nyisson meg egy böngészőt
   - Navigáljon a `http://localhost:8080` címre
   - Látnia kell az Apache Tomcat üdvözlő oldalát

> **Tipp**
>
> Az Apache Tomcat általában automatikusan elindul a telepítés után. Ha nem indul el, nyissa meg a `bin` mappát és futtassa a `startup.bat` fájlt.

---

## Kezdeti telepítés {: #initial-installation }

### 1. lépés: A digna repository létrehozása

A digna repository tárolja az összes, a digna által kiszámított metrikát. Központi adattárként szolgál analitikai és teljesítményadatok számára.

#### Sémák és felhasználó létrehozása

Nyissa meg PostgreSQL kliensét (pgAdmin, psql vagy hasonló), és hajtsa végre az alábbi SQL parancsokat:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Cserélje ki a következő helyőrzőket:**

- `<digna_repo_schema>` — A kívánt sémanév (pl. `dignarepo`)
- `<digna_repo_user>` — A kívánt felhasználónév (pl. `digna_user`)
- `<digna_repo_password>` — Ennek a felhasználónak a biztonságos jelszava

**Példa:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **Legjobb gyakorlat**
>
> Használjon erős, összetett jelszavakat az adatbázis-felhasználókhoz. Kerülje az könnyen kitalálható hitelesítő adatokat.

---

### 2. lépés: A digna telepítési csomag kicsomagolása

1. Keresse meg a rendelkezésére bocsátott digna telepítő ZIP fájlt
2. Csomagolja ki a kívánt telepítési helyre
3. A kicsomagolás után a következő elemeket kell látnia:
   - `dashboard/` — Web dashboard felület
   - `digna` — Fő futtatható állomány (backend + CLI egyben)
   - `config.toml` — Konfigurációs fájl
   - `license.toml` — Licenc fájl (ide másolja a saját licencét)

### 3. lépés: Licencfájl telepítése

> **Fontos**
>
> A licencfájl **nem** része a telepítési csomagnak; külön kerül Önnek átadásra a digna által.

1. Keresse meg a rendelkezésére bocsátott `license.toml` fájlt
2. Másolja a digna telepítési gyökérkönyvtárába (ahol a `config.toml` és a `digna` futtatható található)

**Miért fontos ez:**
A licencfájl tartalmazza az ügyféladatokat, a licenc lejárati dátumát és a digitális aláírást. **Ne módosítsa ezt a fájlt** — a módosítás érvényteleníti azt.

**Könyvtárstruktúra a beállítás után:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend konfiguráció {: #backend-configuration }

### 1. lépés: Konfigurációs fájl létrehozása és szerkesztése

A `config_template.toml` fájl megtalálható a digna telepítési könyvtárában. Csak nevezze át `config.toml`-ra.

**Elhelyezkedés:** `digna_installation/config.toml`

Nyissa meg a `config.toml` fájlt egy szövegszerkesztőben és konfigurálja a lent felsorolt részeket.

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
| `digna_APP_HOST` | `localhost` vagy IP cím | A gazdagép neve vagy IP, ahol a dignabackend fut |
| `digna_APP_PORT` | `8082` (alapértelmezett) | A REST API végpontok portja |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Ha a dashboard más szerveren van, adja meg annak URL-jét |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Szükséges CORS hitelesített kérésekhez |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Minden HTTP metódus engedélyezése |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Minden header engedélyezése |

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
| `digna_REPO_HOST` | `localhost` vagy IP | PostgreSQL szerver hoszt vagy IP |
| `digna_REPO_PORT` | `5432` (alapértelmezett) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Adatbázis neve |
| `digna_REPO_SCHEMA` | `dignarepo` | Korábban létrehozott séma |
| `digna_REPO_USER` | `digna_user` | PostgreSQL-ben létrehozott felhasználó |
| `digna_REPO_PASSWORD` | Az Ön jelszava | A séma létrehozásakor beállított jelszó |

#### [base] szekció

Ez a rész a biztonsági és cookie beállításokat tartalmazza:

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_FERNET_KEY` | Titkosítási kulcs | Tokenek és cookie-k titkosításához (alapértelmezésként biztosított) |
| `digna_COOKIE_DOMAIN` | `localhost` | Illeszkedjen a frontend domainhez |
| `digna_COOKIE_SECURE` | `false` (lokális) / `true` (production) | HTTPS esetén használja a `true` értéket |
| `digna_COOKIE_HTTPONLY` | `true` | Biztonsági okokból mindig engedélyezett |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF támadások csökkentésére |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 óra) | Munkamenet lejárata másodpercben |
| `digna_MAX_WORKERS` | CPU magok száma - 1 | Párhuzamos ellenőrzési feladatok száma |

#### [logging] szekció

Ez a rész a naplózás viselkedését konfigurálja:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` vagy `DEBUG` | `INFO` productionhoz, `DEBUG` hibakereséshez |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Megőrzendő napi naplómentések száma |

---

### 3. lépés: Repository kapcsolat ellenőrzése

1. Nyisson meg egy Parancssort
2. Navigáljon a digna telepítési könyvtárába (ahol a `config.toml` és a `digna` futtatható található)
3. Futtassa a kapcsolat tesztet:

```bash
digna repo check
```

Meg kell jelennie egy megerősítésnek, hogy a kapcsolat létrejött (magát a repository-t még nem inicializáltuk).

### 4. lépés: Repository séma telepítése

Ugyanabban a könyvtárban futtassa:

```bash
digna repo install
```

Ez a parancs telepíti a szükséges táblákat és sémát a PostgreSQL adatbázisban.

### 5. lépés: digna szerver indítása

A digna telepítési könyvtárában indítsa el a szervert:

```bash
digna serve --address <host> --port <port>
```

**Paraméterek:**
- `--address` — Szerver gazdagép neve/IP
- `--port` — Szerver portja

Indítási üzeneteket kell látnia, amelyek megerősítik a szerver futását:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### 6. lépés: Admin felhasználó létrehozása

1. Nyisson meg egy **új** Parancssort
2. Navigáljon a digna telepítési könyvtárába
3. Futtassa az alábbi parancsot egy admin felhasználó létrehozásához:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Példa:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Ez létrehoz egy teljes adminisztrátori jogosultságokkal rendelkező felhasználót.

> **Legjobb gyakorlat**
>
> Használjon erős jelszót, amely tartalmaz nagy- és kisbetűket, számokat és speciális karaktereket.

---

## Dashboard konfiguráció {: #dashboard-configuration }

### 1. lépés: Dashboard telepítése a webszerverre

A digna dashboard saját `config.toml` fájllal rendelkezik a `dashboard/` könyvtárban. Ez a konfiguráció alapértelmezés szerint biztosítva van, és kezdeti telepítés során általában nincs szükség módosításra. Csak akkor kell szerkesztenie, ha módosítani szeretné a backend kapcsolódást (pl. többpéldányos telepítés esetén).

Ha módosítania kell a dashboard konfigurációját, tekintse át a dashboard dokumentációját.

Válassza ki a webszerverét, és kövesse az alábbi telepítési lépéseket.

#### Telepítés IIS-re

1. **Nyissa meg az IIS Manager-t**
   - Nyomja meg a `Win + R` billentyűket, írja be: `inetmgr`, majd Enter

2. **Új webhely létrehozása**
   - A bal oldali panelen kattintson jobb gombbal a **Sites** elemre
   - Válassza az **Add Website...** lehetőséget

3. **Webhely konfigurálása**
   - **Site Name**: Adjon nevet (pl. "dignaDashboard")
   - **Physical Path**: Tallózással válassza ki a `dashboard` mappát
   - **Binding**: Állítsa be az IP címet és a portot (HTTP alapértelmezett 80, HTTPS 443)

4. **Webhely indítása**
   - Kattintson az **OK** gombra a webhely létrehozásához
   - Jobb klikk az új webhelyen, majd válassza a **Start** opciót

5. **Telepítés tesztelése**
   - Nyissa meg a böngészőt
   - Navigáljon a `http://localhost` (vagy a beállított URL) címre
   - Meg kell jelennie a digna dashboard bejelentkező oldalának

#### Telepítés Apache Tomcat-re

1. **Másolja a dashboard mappát a Tomcat-be**
   - Másolja a `dashboard` mappát a Tomcat `webapps` könyvtárába
   - Szükség szerint nevezze át (pl. `digna`)
   - Példa: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Telepítés ellenőrzése**
   - Frissítse vagy töltse újra a Tomcat kezelőoldalát (http://localhost:8080)
   - Látnia kell a "digna" (vagy a választott név) alkalmazást a telepített alkalmazások között

3. **Dashboard elérése**
   - Nyissa meg a böngészőt
   - Navigáljon a `http://localhost:8080/digna` címre
   - Meg kell jelennie a digna dashboard bejelentkező oldalának

---

## digna futtatása Windows szolgáltatásként {: #running-digna-as-a-windows-service }

### Miért érdemes Windows szolgáltatásként futtatni?

A digna backend Windows szolgáltatásként történő futtatása biztosítja, hogy:
- Automatikusan elinduljon a szerver indításakor
- A háttérben fusson anélkül, hogy nyitva kellene tartani egy Parancssort
- Automatikusan újrainduljon, ha összeomlik
- A Windows Szolgáltatások felületen keresztül kezelhető legyen

### Szolgáltatás-kezelő fájlok

Minden szükséges fájl a digna telepítési könyvtárában található under: `bin/`

A következő batch fájlok állnak rendelkezésre:
- `install_service.bat` — digna regisztrálása Windows szolgáltatásként
- `uninstall_service.bat` — szolgáltatás eltávolítása
- `start_service.bat` — szolgáltatás indítása
- `stop_service.bat` — szolgáltatás leállítása

> **Rendszergazdai jogosultság szükséges**
>
> Minden batch fájlt rendszergazdai jogosultsággal kell futtatni.

### A szolgáltatás telepítése

1. **Nyisson Parancssort rendszergazdaként**
   - Jobb klikk a Parancssorra
   - Válassza a "Run as Administrator" opciót

2. **Navigáljon a bin mappába**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Futtassa a telepítő scriptet**
   ```bash
   install_service.bat
   ```

A digna szerver most regisztrálva lett Windows szolgáltatásként, automatikus indítással. Maga a szolgáltatás nem indul el azonnal — az indítással kapcsolatos lépéseket lásd a következő szakaszban.

### A szolgáltatás indítása és leállítása

#### A szolgáltatás indítása

1. Nyisson Parancssort rendszergazdaként
2. Navigáljon a `digna\bin` mappába
3. Futtassa:
   ```bash
   start_service.bat
   ```

#### A szolgáltatás leállítása

1. Nyisson Parancssort rendszergazdaként
2. Navigáljon a `digna\bin` mappába
3. Futtassa:
   ```bash
   stop_service.bat
   ```

> **Tipp**
>
> Mindig állítsa le a szolgáltatást a programfájlok frissítése előtt.

### Szolgáltatás áthelyezése új könyvtárba

Ha át kell helyeznie a digna telepítést:

1. **Távolítsa el a jelenlegi szolgáltatást**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Mozgassa az alkalmazás fájljait**
   - Helyezze át a teljes digna telepítési mappát az új helyre

3. **Telepítse újra a szolgáltatást**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Indítsa el a szolgáltatást**
   ```bash
   start_service.bat
   ```

### A szolgáltatás eltávolítása

1. **Állítsa le a futó szolgáltatást**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Távolítsa el a szolgáltatást**
   ```bash
   uninstall_service.bat
   ```

A digna szerver most eltávolításra került Windows szolgáltatásként való regisztrációból.

---

## Frissítés új verzióra {: #upgrading-to-a-new-release }

### Mielőtt frissítene

**A digna Repository biztonsági mentés készítése kötelező**

A digna frissítése előtt készítsen biztonsági mentést a repository-ról (PostgreSQL), hogy elkerülje az adatvesztést.
A mentés biztosítja, hogy ha a frissítés közben váratlan problémák merülnének fel, vissza tudja állítani az állapotot.

### Frissítési folyamat

#### 1. lépés: digna szolgáltatás leállítása

Ha a digna Windows szolgáltatásként fut, állítsa le:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2. lépés: Jelenlegi backend mentése

A digna telepítési könyvtárában:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### 3. lépés: Új verzió kicsomagolása és telepítése

1. Csomagolja ki az új digna telepítő ZIP fájlt
2. Másolja az új `digna` futtathatót és a `dashboard` mappát a telepítési könyvtárába

> **Fontos**
>
> A `config.toml` fájl **soha** nincs benne a telepítő ZIP-ben. A meglévő konfigurációja biztonságban marad.

### 4. lépés: Konfigurációs fájlok visszaállítása

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### 5. lépés: Repository séma frissítése

Navigáljon a digna telepítési könyvtárába és futtassa:

```bash
digna repo upgrade
```

Ez frissíti a PostgreSQL sémát a legújabb verzióra, miközben megőrzi a meglévő adatokat.

### 6. lépés: Szolgáltatások újraindítása

Ha Windows szolgáltatásként fut:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Ha kézzel futtatja, indítsa újra a szervert:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Ha IIS-t vagy Tomcat-et használ, indítsa újra a megfelelő webszervert.

#### 7. lépés: A frissítés ellenőrzése

1. Lépjen be a digna dashboardra
2. Ellenőrizze, hogy a felület helyesen betöltődik
3. Nézze át a szerver naplóit esetleges hibákért
