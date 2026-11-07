# macOS Telepítési útmutató a digna Release 2026.11-hoz

**Kiadás:** 2026.11

**Utoljára frissítve:** 2026. november 7.


---

## Tartalomjegyzék

1. [Bevezetés](#introduction)
2. [Rendszerkövetelmények](#system-requirements)
3. [Előtelepítési beállítások](#pre-installation-setup)
4. [PostgreSQL szerver beállítása](#postgresql-server-setup)
5. [Webszerver konfiguráció](#web-server-configuration)
6. [Első telepítés](#initial-installation)
7. [Backend konfiguráció](#backend-configuration)
8. [Dashboard konfiguráció](#dashboard-configuration)
9. [digna futtatása háttérszolgáltatásként](#running-digna-as-a-background-service)
10. [Frissítés új kiadásra](#upgrading-to-a-new-release)

---

## Bevezetés {: #introduction }

### A dignáról

digna egy átfogó, MI-vezérelt platform, amely az adatok minőségének kezelését optimalizálja különböző adatkörnyezetekben, mint adattárházak, adat-tavak és lakehouse-ok. Nagymértékben skálázható és alkalmazkodó, digna automatizálással, valós idejű figyeléssel és anomáliaészleléssel kezeli a modern adathasználati kihívásokat.

A digna két fő komponensből áll:

- **digna**: az alkalmazás magja, amely az adatok feldolgozásáért és a minőségi ellenőrzések végrehajtásáért felel. Egyetlen futtatható fájlban egyesíti a háttérrendszert és a parancssori felületet, felváltva a korábbi kiadások különálló `dignabackend` és `dignacli` programjait.
- **dignadashboard**: webalapú felület egy webszerveren, amely felhasználóbarát módon teszi lehetővé a digna platform használatát és az adathigiéniai mutatók megjelenítését.

### Mi újság a 2026.11-os kiadásban

Ez a kiadás bevezeti a digna Data Reconciliation-t, a digna Agentic-et a digna MCP Serverrel, valamint a digna Engine-t, amely a dignán belül képes adatokat profilozni, és különböző adatbázis-technológiák között is ellenőrzi a referenciális integritást. A részletekért lásd a [kiadási megjegyzéseket](../../../changelog/Release_202611.md).

A telepítés szempontjából a kiadás új migrációs mechanizmust hoz a tárolóséma kezelésére, egy opcionális `[duckdb]` szekciót a `config.toml` fájlban a digna Engine számára, valamint új licencfájlt. Mindegyikkel a [frissítésről szóló szakasz](#upgrading-to-a-new-release) foglalkozik.

### Windowsot vagy Linuxot keres?

Ez az útmutató macOS-re vonatkozik. Más platformokhoz lásd a [Windows telepítési útmutatót](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) vagy a [Linux telepítési útmutatót](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Rendszerkövetelmények {: #system-requirements }

Mielőtt megkezdené a telepítést, győződjön meg arról, hogy a rendszere megfelel az alábbi minimális követelményeknek:

| Követelmény | Specifikáció |
|---|---|
| **Operációs rendszer** | macOS 13 (Ventura) vagy újabb |
| **Architektúra** | Apple Silicon (arm64) vagy Intel (x86_64) |
| **Memória (minimális telepítéshez)** | 16 GB RAM |
| **Lemezterület** | 10 GB szabad tárhely |
| **Adatbázis** | PostgreSQL Server 12 vagy újabb |
| **Webszerver** | nginx, Apache httpd vagy egyenértékű |
| **Parancssori eszközök** | Xcode Command Line Tools (Homebrew által igényelt) |

!!! info "digna Engine"

    Azokat az adatbázis-kapcsolatokat, amelyek profilozási helyként a digna Engine-t használják,
    magán a digna gazdagépen profilozza a rendszer. Ezekhez további memóriát és lemezterületet kell
    tervezni, lásd: [\[duckdb\] szekció](#duckdb-section).

### Adatbázis telepítési lehetőségek

**Ha PostgreSQL már telepítve van:**
Hozzáadhat egy új adatbázist digna számára a meglévő PostgreSQL szerveréhez.

**Ha PostgreSQL-t a dignával ugyanarra a gépre telepíti:**

!!! info "Ajánlott specifikációk"

    - **Memória**: 32 GB RAM (a 16 GB helyett)
    - **Lemezterület**: 50 GB szabad tárhely (a 10 GB helyett)

    Ezek a magasabb specifikációk lehetővé teszik, hogy a digna és a PostgreSQL adatbázis egyszerre fusson optimálisan.

### Az architektúra ellenőrzése

Több útvonal a leírásban különbözik Apple Silicon és Intel Mac-ek között. Hogy megtudja, melyik van, nyissa meg a **Terminalt** és futtassa:

```bash
uname -m
```

- `arm64` — Apple Silicon. A Homebrew az `/opt/homebrew`-be települ.
- `x86_64` — Intel. A Homebrew a `/usr/local`-ba települ.

!!! tip "Tipp"

    Ahelyett, hogy mereven beégett útvonalakat használna, ez az útmutató a `$(brew --prefix)`-et használja, ami mindkét architektúrán a megfelelő helyre bővül. Másolja a parancsokat karakterről karakterre.

---

## Előtelepítési beállítások {: #pre-installation-setup }

A digna telepítése előtt győződjön meg róla, hogy három kulcsfontosságú előfeltétel rendelkezésre áll:

1. **Homebrew** – a csomagkezelő, amellyel a lenti komponenseket telepítjük
2. **PostgreSQL Server** – a számított metrikák és teljesítményadatok tárolásához
3. **Webszerver** – a digna Dashboard hosztolásához

Ha ezek a komponensek még nincsenek beállítva, kövesse az alábbi részeket a telepítésükhöz és konfigurációjukhoz.

### Homebrew telepítése

A Homebrew a standard csomagkezelő macOS-hez, és ezt használjuk a PostgreSQL és az nginx telepítéséhez.

#### 1. lépés: Ellenőrizze, hogy a Homebrew már telepítve van-e

Nyissa meg a **Terminalt** (nyomja meg a `Cmd + Space`-t, írja be: `Terminal`, nyomjon Entert) és futtassa:

```bash
brew --version
```

Ha verziószám jelenik meg, ugorjon a [PostgreSQL szerver beállítása](#postgresql-server-setup) részre.

#### 2. lépés: Telepítse a Homebrew-t

Ha a fenti parancs nem található, telepítse a Homebrew-t a [hivatalos Homebrew oldal](https://brew.sh) utasításai szerint. Az telepítő telepíti az Xcode Command Line Toolst is, ha még nincsenek jelen.

#### 3. lépés: Adja hozzá a Homebrew-t a PATH-hoz

Apple Silicon esetén a telepítő két parancsot ír ki, amelyeket futtatni kell a Homebrew shell környezetbe illesztéséhez. Futtassa azokat, majd ellenőrizze:

```bash
brew --prefix
```

Ennek `/opt/homebrew`-t kell kiírnia Apple Siliconon vagy `/usr/local`-t Intel esetén.

---

## PostgreSQL szerver beállítása {: #postgresql-server-setup }

### Ha már van PostgreSQL

Ha PostgreSQL már telepítve és fut a helyi gépén, vagy felügyelt távoli PostgreSQL szervert használ, ugorjon a [következő részhez](#web-server-configuration).

### Telepítési lehetőségek

macOS-en két egyszerű módon telepíthető PostgreSQL. Válasszon **egyet**:

- [Homebrew](#postgresql-homebrew) — parancssoros telepítés, ajánlott szerver telepítésekhez
- [Postgres.app](#postgresql-app) — grafikus telepítés, kényelmes helyi értékeléshez

### PostgreSQL telepítése Homebrew-vel {: #postgresql-homebrew }

#### 1. lépés: Telepítse a PostgreSQL formulát

```bash
brew install postgresql@16
```

#### 2. lépés: Adja hozzá a PostgreSQL-t a PATH-hoz

A verziózott PostgreSQL formulák *keg-only* jellegűek, ami azt jelenti, hogy a Homebrew nem linkeli automatikusan a parancsokat a PATH-ba. Adja hozzá kézzel:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Megjegyzés"

    Ez az alapértelmezett `zsh` shellre vonatkozik, amit macOS használ. Ha `bash`-t használ, fűzze ugyanazt a sort a `~/.bash_profile`-hoz.

#### 3. lépés: Indítsa el a PostgreSQL szolgáltatást

```bash
brew services start postgresql@16
```

Ez azonnal elindítja a PostgreSQL-t és beállítja, hogy bejelentkezéskor automatikusan újrainduljon.

#### 4. lépés: Ellenőrizze a telepítést

```bash
psql --version
```

Ha sikeres a telepítés, meg kell jelennie a PostgreSQL verziónak.

#### 5. lépés: Csatlakozás a szerverhez

```bash
psql postgres
```

!!! warning "Fontos — macOS eltér Windows-tól itt"

    A Windows telepítő megkérdezi, hogy hozzon-e létre `postgres` szuperfelhasználót és jelszót. A Homebrew nem teszi ezt. Ehelyett egy, a **macOS fiókjának** megfelelő nevű szuperfelhasználót hoz létre, jelszó nélkül, amely csak a helyi gépről érhető el.

    Ez azt jelenti, hogy egy friss Homebrew telepítésen nincs `postgres` szerep. Használja a saját fióknevét, amikor szuperfelhasználói jogosultságra van szükség, és hozzon létre egy explicit digna felhasználót az [Első telepítés](#initial-installation) leírás szerint.

#### 6. lépés: Ellenőrizze a portot

A PostgreSQL alapértelmezett portja `5432`. A szerver által használt port ellenőrzéséhez:

```bash
psql postgres -c "SHOW port;"
```

Jegyezze fel az értéket — szüksége lesz rá a digna backend konfigurálásakor.

### PostgreSQL telepítése Postgres.app-pal {: #postgresql-app }

Ha grafikus telepítést preferál:

1. Töltse le a [Postgres.app](https://postgresapp.com)-ot és húzza az **Applications** mappába
2. Nyissa meg az alkalmazást és kattintson az **Initialize** gombra egy új szerver létrehozásához
3. Kövesse az alkalmazás utasításait a parancssori eszközök PATH-hoz adásához
4. Ellenőrizze a telepítést:

```bash
psql --version
```

A Postgres.app is létrehoz egy, a macOS fióknevéről elnevezett szuperfelhasználót.

---

## Webszerver konfiguráció {: #web-server-configuration }

A dignának szüksége van egy webszerverre a dashboard hosztolásához. Válasszon az alábbiak közül:

- [nginx](#nginx-setup) — Homebrew-vel telepítve, ajánlott
- [Apache httpd](#apache-setup) — macOS része

Csak **egyiket** kell telepítenie és konfigurálnia.

Mindkét rész a dashboard számára szükséges két beállítást konfigurálja:

- **Single-page-application fallback** (egylapos alkalmazás visszadobás), hogy egy dashboard URL frissítésekor ne kapjon 404-et
- **.md MIME típus** beállítása, hogy a Markdown fájlok helyesen legyenek kiszolgálva

### nginx beállítása {: #nginx-setup }

#### Áttekintés

Az nginx egy könnyű, nagy teljesítményű webszerver, amely jól alkalmas a statikus digna dashboard kiszolgálására.

#### Telepítés

```bash
brew install nginx
```

#### nginx indítása

```bash
brew services start nginx
```

#### Ellenőrizze a telepítést

1. Nyissa meg a böngészőt
2. Navigáljon a `http://localhost:8080` címre
3. Az nginx üdvözlőoldalát kell látnia

!!! note "Megjegyzés — az alapértelmezett port 8080, nem 80"

    A Homebrew úgy konfigurálja az nginx-et, hogy a `8080` porton hallgasson, így admin jogosultság nélkül is futtatható. macOS-en a `80` vagy bármely, 1024 alatti port kötése root jogosultságot igényel.

    Ha a dashboardot a 80-as porton szeretné kiszolgálni, cserélje a konfigurációban a `listen 8080;` sort `listen 80;`-ra, és indítsa el az nginx-et `sudo brew services start nginx` paranccsal.

#### Site konfigurálása a Dashboardhoz

A Homebrew nginx konfigurációja minden fájlt beolvas a `servers` könyvtárból. Hozzon létre egy dedikált konfigurációs fájlt a digna számára:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Illessze be a következőt, kicserélve a `/path/to/digna/dashboard`-ot az Ön kicsomagolt `dashboard` mappájának valódi elérési útjára:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Fontos"

    A `try_files` direktíva nélkül bármely dashboard oldal újratöltése a gyökér URL-en kívül 404-et ad vissza. Ez az nginx megfelelője az IIS URL Rewrite modulnak Windows-on.

#### Alkalmazza a konfigurációt

Tesztelje a konfigurációt szintaktikai hibákra, majd töltse újra az nginx-et:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd beállítása {: #apache-setup }

#### Áttekintés

A macOS tartalmazza az Apache httpd-t, így telepítés nem szükséges. Alapértelmezetten le van tiltva.

#### Apache indítása

```bash
sudo apachectl start
```

#### Ellenőrizze a telepítést

1. Nyissa meg a böngészőt
2. Navigáljon a `http://localhost` címre
3. A "It works!" üzenetet kell látnia

#### Kötelező: mod_rewrite engedélyezése

A dashboard URL átírást igényel. Nyissa meg az Apache konfigurációt:

```bash
sudo nano /etc/apache2/httpd.conf
```

Keresse meg a következő sort és távolítsa el előle a kezdő `#`-t, hogy kicsomagolja:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Kötelező: .htaccess felülbírálások engedélyezése

Ugyanabban a fájlban keresse meg a `<Directory "/Library/WebServer/Documents">` blokkot és változtassa meg:

```apache
AllowOverride None
```

erre:

```apache
AllowOverride All
```

#### Kötelező: MIME típus Markdown fájlokhoz

Még az `httpd.conf`-ban adja hozzá a következő sort, hogy a Markdown fájlok helyesen legyenek kiszolgálva:

```apache
AddType text/markdown .md
```

!!! warning "Fontos"

    E nélkül a beállítás nélkül a `.md` fájlok nem biztos, hogy helyesen lesznek kiszolgálva.

#### Alkalmazza a konfigurációt

Ellenőrizze a konfigurációt szintaktikai hibákra, majd indítsa újra az Apache-ot:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Első telepítés {: #initial-installation }

### 1. lépés: Hozza létre a digna repository-t

A digna repository tárol minden, a digna által kiszámított metrikát. Ez működik, mint a központi adatbázis az analitikai és teljesítményadatok számára.

#### Repository sémája és felhasználó létrehozása

Nyissa meg a PostgreSQL kliensét (psql, pgAdmin vagy hasonló) és futtassa a következő SQL parancsokat:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Cserélje ki az alábbi helykitöltőket:**

- `<digna_repo_schema>` — A kívánt séma neve (pl. `dignarepo`)
- `<digna_repo_user>` — A kívánt felhasználónév (pl. `digna_user`)
- `<digna_repo_password>` — Biztonságos jelszó ehhez a felhasználóhoz

**Példa:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

A parancsok futtatásához a Terminalból egyetlen lépésben:

```bash
psql postgres
```

Majd illessze be a fenti utasításokat a `postgres=#` promptnál, és írja be a kilépéshez: `\q`.

!!! tip "Legjobb gyakorlat"

    Használjon erős, összetett jelszavakat az adatbázis felhasználókhoz. Kerülje az egyszerűen kitalálható hitelesítő adatokat.

---

### 2. lépés: Csomagolja ki a digna telepítési csomagot

1. Keresse meg a digna telepítő ZIP fájlját, amelyet kapott
2. Csomagolja ki a kívánt telepítési helyre — például `/opt/digna` vagy `~/digna`
3. A kicsomagolás után a következő elemeket kell látnia:
   - `dashboard/` — Web dashboard felület
   - `digna` — Fő futtatható állomány (backend + CLI egyben)

!!! info "A konfigurációs és a licencfájl nincs benne a csomagban"

    Sem a `config.toml`, sem a `dashboard/dashboard_config.toml` nem része a telepítésnek — mindkettőt
    Önnek kell létrehoznia, a [Backend konfiguráció](#backend-configuration) és a
    [Dashboard konfiguráció](#dashboard-configuration) szakaszban leírtak szerint. A `license.toml` sem
    része a csomagnak; a digna külön biztosítja, ahogyan a 3. lépés leírja.

A Terminalból történő kicsomagoláshoz:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Tegye futtathatóvá a binárist

Attól függően, hogyan került át a csomag, a futtathatósági bit lehet, hogy nem maradt meg. Állítsa be egyértelműen:

```bash
cd /opt/digna
chmod +x digna
```

#### Ha macOS blokkolja az alkalmazást

A böngészőn vagy levelezőn keresztül letöltött fájlok karantén attribútummal vannak jelölve. Ha macOS azt írja, hogy az alkalmazás *"nem nyitható meg, mert a fejlesztőt nem lehet ellenőrizni"*, távolítsa el az attribútumot a telepítési könyvtárról:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternatívaként nyissa meg a **System Settings → Privacy & Security** menüt, keresse meg a blokkolt elemet az oldal alján, és kattintson az **Open Anyway** gombra.

!!! note "Megjegyzés"

    Erre a lépésre csak akkor van szükség, ha macOS ténylegesen blokkolja a futtatható állományt. SSH-n vagy belső fájlkiszolgálóról átvitt csomagok általában nincsenek karanténnal jelölve.

### 3. lépés: Telepítse a licencfájlt

!!! warning "Fontos"

    A licenc fájl NEM része a telepítési csomagnak és a dignától külön kerül kiszolgálásra.

1. Keresse meg az Önnek biztosított `license.toml` fájlt
2. Másolja be a digna telepítési gyökérkönyvtárába (ahol a `config.toml` és a `digna` futtatható található)

**Miért fontos ez:**
A licenc fájl tartalmazza az ügyféladatokat, a licenc lejárati dátumát és a digitális aláírást. **Ne módosítsa ezt a fájlt** — bármilyen változtatás érvényteleníti azt.

**Könyvtárstruktúra a beállítás után:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend konfiguráció {: #backend-configuration }

### 1. lépés: Hozza létre és szerkessze a konfigurációs fájlt

A `config_template.toml` fájl megtalálható a digna telepítési könyvtárban. Csak át kell neveznie `config.toml`-ra.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Hely:** `/opt/digna/config.toml`

Nyissa meg a `config.toml` fájlt egy szövegszerkesztőben és konfigurálja az alábbi részeket.

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

!!! note "Megjegyzés"

    Ha a dashboardot a Homebrew nginx-en szolgálja ki az alapértelmezett porton, az engedélyezendő origin: `http://localhost:8080`.

!!! info "Az [app] szekció opcionális"

    A Release 2026.11-től mindkét kulcs, sőt a teljes `[app]` szekció is elhagyható. Ez a helyes
    beállítás, ha egy fordított proxy egyetlen eredet alatt szolgálja ki a dashboardot és a
    backendet: a böngésző ilyenkor nem küld eltérő eredetű kéréseket, és alapértelmezés szerint
    egyik sincs engedélyezve.

#### [repo] szekció

Ez a rész a PostgreSQL adatbázishoz való csatlakozást konfigurálja:

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
| `DIGNA_REPO_HOST` | `localhost` vagy IP | PostgreSQL szerver hosztja/IP-je |
| `DIGNA_REPO_PORT` | `5432` (alapértelmezett) | PostgreSQL port |
| `DIGNA_REPO_DB` | `postgres` | Adatbázis neve |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Korábban létrehozott séma |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL-ben létrehozott felhasználó |
| `DIGNA_REPO_PASSWORD` | Az Ön jelszava | A séma létrehozásakor beállított jelszó |
| `DIGNA_REPO_SSLMODE` | `prefer` (alapértelmezett) | Opcionális. PostgreSQL SSL mód: `disable`, `allow`, `prefer`, `require`, `verify-ca` vagy `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (alapértelmezett) | Opcionális. A digna által a repóhoz nyitva tartott kapcsolatok száma |

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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 óra) | Munkamenet lejárati ideje másodpercben |
| `DIGNA_MAX_WORKERS` | CPU magok száma - 1 | Az egyszerre futtatható vizsgálatok száma |
| `DIGNA_FRONTEND_BASEURL` | Dashboard URL | Kötelező. Az értesítő üzenetekben lévő hivatkozásokhoz használatos, ezért olyan URL-nek kell lennie, amelyet a címzettek meg tudnak nyitni |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (alapértelmezett) | Opcionális. Ennyi másodpercig futhat egy forrásadatbázison végrehajtott egyetlen lekérdezés, mielőtt megszakad; a `0` kikapcsolja az időkorlátot |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (alapértelmezett) | Opcionális. Ennyi másodpercig vár a rendszer a forrásadatbázishoz való kapcsolódásra; a `0` korlátlan várakozást jelent |

!!! tip "Tipp"

    A Mac-en rendelkezésre álló CPU-magok számának megkereséséhez futtassa: `sysctl -n hw.ncpu`.

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

Ez a rész a naplózás viselkedését konfigurálja:

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

#### [duckdb] szekció (opcionális) {: #duckdb-section }

Újdonság a Release 2026.11-ben. Ez a szekció a **digna Engine** erőforrásait állítja be. A digna Engine
a dignán belül profilozza az adatokat azoknál az adatbázis-kapcsolatoknál, amelyek profilozási helye
**digna Engine**, és referenciális integritási ellenőrzéseket futtat a különböző adatbázis-kapcsolatokon
lévő adatforrások között. Lásd: [Profilozási hely](../../../platform/profiling/profiling_location.md).

A szekció opcionális. Nélküle az alábbi alapértelmezett értékek érvényesek.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (alapértelmezett) | Egy digna Engine-futás által használható memória MB-ban. Egyszerre legfeljebb `DIGNA_MAX_WORKERS` futás lehet aktív |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Alapértelmezés: a rendszer ideiglenes könyvtára (a dignát futtató fiók `$TMPDIR` könyvtára) | Az ideiglenes fájlok könyvtára arra az esetre, ha az adatok nem férnek el a memóriában |

!!! tip "A digna Engine méretezése"

    A digna gazdagépen a digna saját memóriaigényén felül legfeljebb `DIGNA_MAX_WORKERS` ×
    `DIGNA_DUCKDB_MEMORY_LIMIT_MB` memóriával kell számolni, az ideiglenes könyvtárban pedig annyi
    szabad lemezterülettel, amennyi a digna Engine-t használó adatforrások legnagyobb vizsgált napjának
    adatait befogadja. A `DIGNA_DUCKDB_TEMP_DIRECTORY` beállítást egy ekkora szabad hellyel rendelkező
    lemezre kell irányítani, amelyre a dignát futtató fiók írni tud:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Erre a szekcióra csak akkor van szükség, ha legalább egy adatbázis-kapcsolat a digna Engine-t
    használja, vagy egy referenciális integritási ellenőrzés különböző kapcsolatokon lévő
    adatforrásokat hasonlít össze.

---

### 2. lépés: Ellenőrizze a konfigurációt

A tároló inicializálása előtt ellenőrizze, hogy a `config.toml` teljes és helyesen felépített. A digna telepítési könyvtárában futtassa:

```bash
./digna config check
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

### 3. lépés: Inicializálja a repository-t

1. Nyissa meg a **Terminalt**
2. Navigáljon a digna telepítési könyvtárába (ahol a `config.toml` és a `digna` futtatható található)
3. Futtassa a csatlakozás tesztet:

```bash
cd /opt/digna
./digna repo check
```

Új séma esetén a parancs csatlakozik, majd jelzi, hogy még nincs telepített repó:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Ezen a ponton ez a várt eredmény: megerősíti, hogy a digna eléri a PostgreSQL-t és a sémát. Kapcsolódási vagy hitelesítési hiba esetén viszont a `[repo]` szekcióban vagy a PostgreSQL beállításában van a hiba.

!!! note "Megjegyzés"

    macOS-en a jelenlegi könyvtárban lévő parancsok nincsenek a PATH-on, ezért a futtatható `./digna` formában indítandó. Ha szeretné a rövidebb formát használni mindenhol, adja hozzá a telepítési könyvtárat a PATH-hoz:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 4. lépés: Telepítse a repository sémát

Ugyanabban a könyvtárban futtassa:

```bash
./digna repo upgrade
```

Ez a parancs létrehozza a szükséges táblákat a repó sémájában, és a következő üzenettel zárul:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "A repo upgrade telepít és frissít"

    A Release 2026.11-től a `repo upgrade` új repót telepít, a meglévőt pedig frissíti.
    A `repo install` továbbra is működik, ugyanennek a parancsnak a másik neveként.

### 5. lépés: Hozzon létre egy admin felhasználót

1. Nyisson egy **új** Terminal ablakot
2. Navigáljon a digna telepítési könyvtárába
3. Futtassa a következő parancsot egy admin felhasználó létrehozásához:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Példa:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Ezzel létrejön egy felhasználó `admin@example.com` e-mail-címmel és teljes rendszergazdai jogosultságokkal.

!!! tip "Tipp"

    Tegye idézőjelek közé a jelszót. A `zsh` különlegesként kezeli az olyan karaktereket, mint `!`, `$` és `*`, és egy idézőjelek nélküli jelszó ezeket nem fogja helyesen továbbítani.

!!! tip "Legjobb gyakorlat"

    Használjon erős jelszót, amely tartalmaz nagybetűt, kisbetűt, számokat és speciális karaktereket.

---

### 6. lépés: Indítsa el a digna szervert

A digna telepítési könyvtárban indítsa el a szervert:

```bash
./digna serve --address <host> --port <port>
```

**Paraméterek:**
- `--address` — Szerver hosztneve/IP-je (alapértelmezett: `127.0.0.1`)
- `--port` — Szerver portja (alapértelmezett: `8000`)

Amikor a szerver elindult, kiírja a címet, amelyen figyel:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tipp"

    Amikor a szervert először indítja, macOS megkérdezheti, hogy szeretné-e engedélyezni az alkalmazásnak a bejövő hálózati kapcsolatok elfogadását. Kattintson az **Allow**-ra, különben a dashboard nem fogja elérni a backendet.

!!! note "A kiszolgáló lefoglalja a terminált"

    A `serve` az előtérben fut, és addig működik, amíg le nem állítja a ++ctrl+c++ billentyűkkel. Hagyja futni, amíg befejezi a beállítást; ha inkább rendszerindításkor indulna automatikusan, lásd: [A digna futtatása háttérszolgáltatásként](#running-digna-as-a-background-service).

## Dashboard konfiguráció {: #dashboard-configuration }

### 1. lépés: Telepítse a dashboardot a webszerverre

A digna dashboard a saját konfigurációját a `dashboard/dashboard_config.toml` fájlból olvassa. Ez a fájl nem része a telepítésnek — Önnek kell létrehoznia a `dashboard/` könyvtárban, a dashboard fájljai mellett.

A tartalmát az [Egyszeri bejelentkezés (SSO)](../../../sso/overview.md) oldal írja le, és ott is van rá szükség: ez tartalmazza a dashboard által kínált bejelentkezési lehetőségeket, valamint több példányos telepítéseknél a backend kapcsolatot.

Válassza ki a webszervert és kövesse a megfelelő telepítési lépéseket.

#### Telepítés nginx-re

Ha követte a [nginx beállítás](#nginx-setup) részt, a szerver blokk már a `dashboard` mappájára mutat, így másolás nem szükséges.

1. **Ellenőrizze az elérési utat**
   - Nyissa meg: `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Győződjön meg róla, hogy a `root` a kicsomagolt `dashboard` mappára mutat

2. **Biztosítsa a mappa olvashatóságát**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Töltse újra az nginx-et**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Tesztelje a telepítést**
   - Nyissa meg a böngészőt
   - Navigáljon a `http://localhost:8080` címre (vagy a konfigurált URL-re)
   - A digna dashboard bejelentkező oldalát kell látnia

#### Telepítés Apache httpd-re

1. **Másolja a Dashboardot a Document Root-ba**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Adja hozzá az átírási szabályokat**

   Hozzon létre egy `.htaccess` fájlt a telepített mappában, hogy a dashboard útvonalak túléljék az oldalfrissítést:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Illessze be a következőt:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Indítsa újra az Apache-ot**
   ```bash
   sudo apachectl restart
   ```

4. **Nyissa meg a dashboardot**
   - Nyissa meg a böngészőt
   - Navigáljon a `http://localhost/digna` címre
   - A digna dashboard bejelentkező oldalát kell látnia

---

## digna futtatása háttérszolgáltatásként {: #running-digna-as-a-background-service }

### Miért futtassa a digna-t szolgáltatásként?

A digna backend háttérszolgáltatásként történő futtatása biztosítja, hogy:

- Automatikusan elinduljon a gép bootolásakor
- A háttérben fusson, anélkül, hogy nyitva kellene tartani egy Terminal ablakot
- Automatikusan újrainduljon, ha összeomlik
- `launchctl`-lel, macOS szolgáltatáskezelővel menedzselhető legyen

### Szolgáltatás-kezelő fájlok

Minden szükséges fájl a digna telepítési könyvtár `bin/` almappájában található: `bin/`

Az elérhető shell scriptek:

- `install_service.sh` — digna regisztrálása a launchd-hez
- `uninstall_service.sh` — a szolgáltatás eltávolítása
- `start_service.sh` — a regisztrált szolgáltatás indítása
- `stop_service.sh` — a futó szolgáltatás leállítása

!!! warning "Rendszergazdai jogosultság szükséges"

    Minden scriptet `sudo`-val kell futtatni, mert egy rendszerinduláskor elinduló szolgáltatás regisztrálása a `/Library/LaunchDaemons`-be ír.

### Tegye futtathatóvá a scripteket

A kicsomagoláskor az executable bit eltűnhet. Az első használat előtt:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### A szolgáltatás telepítése

1. **Nyissa meg a Terminalt**

2. **Navigáljon a bin mappába**
   ```bash
   cd /opt/digna/bin
   ```

3. **Futtassa a telepítő scriptet**
   ```bash
   sudo ./install_service.sh
   ```

A digna szerver most regisztrálva van a launchd-ben automatikus indítással. A szolgáltatás nem indul el automatikusan a telepítéskor — lásd a következő szakaszt az indításhoz.

### A szolgáltatás indítása és leállítása

#### A szolgáltatás indítása

1. Nyissa meg a Terminalt
2. Navigáljon a `/opt/digna/bin` könyvtárba
3. Futtassa:
   ```bash
   sudo ./start_service.sh
   ```

#### A szolgáltatás leállítása

1. Nyissa meg a Terminalt
2. Navigáljon a `/opt/digna/bin` könyvtárba
3. Futtassa:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tipp"

    Mindig állítsa le a szolgáltatást az alkalmazásfájlok frissítése előtt.

### A szolgáltatás ellenőrzése

A szolgáltatás regisztráltságának és futásának ellenőrzéséhez:

```bash
sudo launchctl list | grep digna
```

Egy sor, ami folyamatazonosítóval kezdődik, azt jelenti, hogy a szolgáltatás fut. Ha az első oszlopban `-` szerepel, az azt jelenti, hogy regisztrálva van, de leállt.

### A szolgáltatás áthelyezése új könyvtárba

A launchd eltárolja a futtatható abszolút elérési útját, így az áthelyezés újra-regisztrálást igényel:

1. **Távolítsa el a jelenlegi szolgáltatást**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Mozgassa az alkalmazás fájlokat**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Telepítse újra a szolgáltatást**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Indítsa el a szolgáltatást**
   ```bash
   sudo ./start_service.sh
   ```

### A szolgáltatás eltávolítása

1. **Állítsa le a futó szolgáltatást**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Távolítsa el a szolgáltatást**
   ```bash
   sudo ./uninstall_service.sh
   ```

A digna szerver most eltávolításra került a launchd regisztrációból.

---

## Frissítés új kiadásra {: #upgrading-to-a-new-release }

Ez a szakasz egy Release 2026.06 telepítés Release 2026.11-re történő frissítését írja le. Ha a
telepítése régebbi, először olvassa el a [Frissítés 2026.06-nál régebbi kiadásról](#upgrading-from-a-release-before-2026-06)
című részt.

### Mielőtt frissítene

**A digna repó biztonsági mentése kötelező**

A digna frissítése előtt készítsen biztonsági mentést a repóról (PostgreSQL), hogy elkerülje az
adatvesztést. A mentés biztosítja, hogy vissza tudja állítani az adatokat, ha a frissítés során váratlan
probléma lép fel.

Mentés készítése a Terminálból:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**A Release 2026.11 licencfájljának igénylése**

A Release 2026.11 új `license.toml` fájlt igényel. Kérje el a digna csapattól még a kezdés előtt, és
tartsa készenlétben a [7. lépéshez](#step-7-replace-the-license-file).

### Frissítés 2026.06-nál régebbi kiadásról {: #upgrading-from-a-release-before-2026-06 }

A Release 2026.06 három olyan változást hozott, amely akkor is érvényes, ha egy régebbi telepítést
közvetlenül 2026.11-re frissít:

- **Csak ODBC.** A digna minden forrástechnológiát ODBC-n keresztül ér el. Minden olyan
  adatbázis-kapcsolatot, amely még nem ODBC-t használ, a frissítés után át kell állítani ODBC-re;
  automatikus átalakítás nincs. Előzetesen telepítse az ODBC-illesztőprogramokat a digna
  gazdagépre, lásd: [Az ODBC-illesztőprogram telepítése a digna gazdagépre](../../../databases/overview.md#install-the-driver),
  és készítse elő minden kapcsolat tulajdonságait a
  [technológiai útmutatók](../../../databases/overview.md#technology-guides) alapján. A Databricks Legacy
  csatlakozó már nem létezik; költöztesse át ezeket a kapcsolatokat a
  [Databricks](../../../databases/databricks_connector_guide.md) csatlakozóra.
- **Egyetlen futtatható fájl.** A `dignabackend` és a `dignacli` helyét az egyetlen `digna` futtatható
  fájl veszi át, amely egyesíti a backendet és a CLI-t.
- **config.toml.** Az `[encryption]` szekció kötelező, a `DIGNA_APP_HOST` és a `DIGNA_APP_PORT`
  beállítást pedig a digna már nem olvassa be: a szerver a címét és a portját a `digna serve`
  parancstól kapja. Vesse össze a fájlját a [Backend konfiguráció](#backend-configuration) résszel.

Az alábbi lépések jelzik, hol igényel egy régebbi telepítés eltérő eljárást. A 8. lépésben
a repó frissítése bármely korábbi kiadás repóját közvetlenül 2026.11-re hozza.

### Frissítési folyamat

#### 1. lépés: Állítsa le a digna szolgáltatást {: #step-1-stop-the-digna-service }

Ha a digna háttérszolgáltatásként fut, először állítsa le:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Ha a digna előtérben fut, nyomja meg a ++ctrl+c++ billentyűket a Terminál-ablakában.

#### 2. lépés: Mentse a jelenlegi telepítést {: #step-2-backup-current-installation }

A digna telepítési könyvtárában nevezze át a jelenlegi telepítés futtatható fájlját és dashboard
mappáját, hogy az új kiadás melléjük telepíthető legyen:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

A `digna_old` fájlt tartsa meg, amíg nem ellenőrizte a frissítést, a `dashboard_old` mappát
pedig addig, amíg vissza nem állította belőle a konfigurációs fájljait (lásd a 4. lépést).
Utána mindkettő törölhető.

!!! info "Frissítés 2026.06-nál régebbi kiadásról"

    A futtatható fájl helyett a `dignabackend` és a `dignacli` mappát nevezze át:
    `mv dignabackend dignabackend_old` és `mv dignacli dignacli_old`. A Release 2026.11 egyiket sem használja.

#### 3. lépés: Csomagolja ki és telepítse az új verziót {: #step-3-extract-and-deploy-new-version }

1. Csomagolja ki az új digna telepítő ZIP fájlt
2. Másolja az új `digna` futtathatót és a `dashboard` mappát a telepítési könyvtárába
3. Állítsa vissza a futtathatósági bitet és szükség esetén távolítsa el a karantén attribútumot:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Fontos"

    Sem a `config.toml`, sem a `dashboard/dashboard_config.toml` **soha** nem része a
    telepítési ZIP-nek — a digna csapat egyik fájlt sem szállítja. A meglévő konfigurációját
    ezért a frissítés nem érinti, és az átnevezett `*_old` mappákban lévő példányok az
    egyetlenek, amelyekkel rendelkezik.

#### 4. lépés: Állítsa vissza a konfigurációs fájlokat {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

A Release 2026.11 nem igényel változtatást a `config.toml` fájlban: a Release 2026.06-tal működő fájl
továbbra is működik. Két módosítás opcionális:

- Adjon hozzá egy [`[duckdb]` szekciót](#duckdb-section), ha az adatbázis-kapcsolatoknak a digna
  Engine-t kell használniuk, és annak alapértelmezett értékei nem felelnek meg a gazdagépnek.
- Hagyja el az `[app]` szekciót, ha egy fordított proxy egyetlen eredet alatt szolgálja ki a
  dashboardot és a backendet.

!!! warning "Beállítások, amelyeket a digna nem olvas be"

    Az útmutató korábbi változatai olyan beállításokat is tartalmaztak, amelyeket a digna nem olvas
    be. Ezeknek nincs hatásuk, és a `config check` a 6. lépésben az **Unknown keys** alatt sorolja fel
    őket. Távolítsa el vagy javítsa ki őket:

    - A `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` és
      `digna_LOGGING_BACKUP_COUNT` beállítás nem létezik. Távolítsa el őket.
    - A beállítások neve megkülönbözteti a kis- és nagybetűket. A digna a `DIGNA_REPO_HOST` kulcsot
      olvassa be, nem a `digna_REPO_HOST` kulcsot. Minden nevet nagybetűvel írjon, ahogy a
      [Backend konfiguráció](#backend-configuration) részben.

!!! warning "Egyszeri bejelentkezés: tartsa meg az [[oidc_clients]] formát"

    A digna az egyszeri bejelentkezés szolgáltatóit `[[oidc_clients]]` bejegyzések listájaként
    olvassa be, mindegyiket saját `DIGNA_OIDC_KEY` kulccsal. Ha a szolgáltatóit
    `[oidc_clients.<key>]` szekciókra alakította át, ahogy az útmutató egy korábbi változata
    mutatta, alakítsa vissza őket. A `config check` mindaddig FAILED állapotúnak jelenti az
    `OIDC config(s)` elemet, amíg ez a forma van érvényben:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Ismételje meg a bejegyzést minden szolgáltatóhoz, és minden `DIGNA_OIDC_KEY` legyen azonos a
    `dashboard_config.toml` fájlban lévő `key` értékkel. Ez csak az egyszeri bejelentkezést használó
    telepítéseket érinti.

#### 5. lépés: Töltse újra a webszervert {: #step-5-reload-the-web-server }

A dashboard statikus fájlok összessége, ezért előfordulhat, hogy a webszerver — és a böngésző — még
az előző verziót szolgálja ki. Töltse újra vagy indítsa újra azt a webszervert, amely a `dashboard`
mappát kiszolgálja, majd töltse be újra az oldalt kényszerített frissítéssel (++cmd+shift+r++).

#### 6. lépés: Ellenőrizze a konfigurációt {: #step-6-validate-the-configuration }

Mielőtt a repóhoz nyúlna, győződjön meg róla, hogy a `config.toml` teljes:

```bash
./digna config check
```

Minden szekciónak OK állapotot kell jelentenie. Javítson ki mindent, amit FAILED állapotúként jelent,
távolítsa el az **Unknown keys** alatt felsorolt kulcsokat, és a folytatás előtt futtassa újra
a parancsot.

#### 7. lépés: Cserélje le a licencfájlt {: #step-7-replace-the-license-file }

A licencfájl általában átvihető egyik kiadásról a másikra. A Release 2026.11 kivétel: két
licencköteles modult vezet be, a digna Data Reconciliation-t és a digna Agentic-et, és a 2026.11 előtt
kiállított licenc ezeket nem tartalmazza. Másolja a digna csapat által a Release 2026.11-hez
biztosított `license.toml` fájlt a telepítési könyvtárba, felülírva a régit:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ne tartsa meg a korábbi licencet"

    A korábbi licenccel a digna ugyan elindul, de a digna Data Reconciliation és a digna MCP Server
    kikapcsolva marad. Minden parancs, amely ellenőrzi a licencet — `user`, `inspection`, `repo` —
    megszakad, mielőtt a repóhoz nyúlna, ha az ellenőrzés sikertelen. Ellenőrizze az új
    licencet, mielőtt továbblép:

    ```bash
    ./digna license check
    ```

#### 8. lépés: Frissítse a repository sémát {: #step-8-upgrade-the-repository-schema }

A digna telepítési könyvtárában futtassa:

```bash
cd /opt/digna
./digna repo upgrade
```

A Release 2026.11 verziózott migrációkkal kezeli a repó sémáját. Egy korábbi kiadásról végzett első
frissítés a sémát az előző rendszer utolsó verziójára hozza, ezt kiindulópontként rögzíti, majd
alkalmazza a Release 2026.11 migrációit. A végén ezt írja ki:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Minden meglévő adat megmarad. A repó állapotát bármikor megtekintheti a
`./digna repo check` paranccsal: kilistázza a legutóbb alkalmazott migrációt és a még függőben lévőket.

!!! warning "A digna nem indul el elavult repóval"

    A Release 2026.11-től a szerver nem hajlandó elindulni, amíg a repó frissítésre szorul, és ezt
    jelzi is, például:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    A szerver vagy a szolgáltatás indítása előtt futtassa a `repo upgrade` parancsot.

#### 9. lépés: Indítsa újra a szolgáltatásokat {: #step-9-restart-services }

Ha háttérszolgáltatásként fut:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Ha manuálisan futtatja, indítsa újra a szervert:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Ha nginx-et vagy Apache-ot használ, indítsa újra a megfelelő webszervert:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### 10. lépés: Ellenőrizze a frissítést {: #step-10-verify-the-upgrade }

1. Ellenőrizze az új futtatható fájl kiadását:

    ```bash
    ./digna version
    ```

    Az első sornak így kell szólnia: `Release: 2026.11`.

2. Nyissa meg a digna dashboardot, és ellenőrizze, hogy a felület helyesen töltődik-e be.
3. Nézze át a szerver kimenetét és a `logs` könyvtárban lévő fájlokat esetleges hibákért.
4. Tesztelje az adatbázis-kapcsolatokat — lásd:
   [Kapcsolat tesztelése](../../../databases/overview.md#testing-a-connection). Egy 2026.06-nál régebbi
   kiadásról végzett frissítés után előbb állítsa át ODBC-re mindazokat a kapcsolatokat, amelyek
   még nem ODBC-t használtak.

Az új modulok használatának megkezdéséhez lásd: [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI-ügynök csatlakoztatása](../../../platform/agentic/connect_ai_agent.md) a digna MCP Serverhez, valamint
[Profilozási hely](../../../platform/profiling/profiling_location.md) a digna Engine-hez.