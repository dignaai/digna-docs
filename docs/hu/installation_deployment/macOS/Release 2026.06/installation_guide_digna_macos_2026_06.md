---
title: macOS Telepítési útmutató – digna Release 2026.06 | digna Dokumentáció
description: Lépésről lépésre útmutató a digna Release 2026.06 telepítéséhez macOS rendszeren — rendszerkövetelmények, Homebrew és PostgreSQL beállítása, nginx vagy Apache konfiguráció, backend és dashboard konfiguráció, digna futtatása háttérszolgáltatásként, és frissítés új kiadásra.
keywords: digna macos telepítés, digna mac telepítési útmutató, digna backend beállítás, digna dashboard telepítés, postgresql homebrew, nginx macos, digna launchd szolgáltatás, digna frissítési útmutató
image: /assets/logo_square.png
---

# macOS Telepítési útmutató a digna Release 2026.06-hoz

**Kiadás:** 2026.06

**Utoljára frissítve:** 2026. szeptember 5.


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

- **dignabackend**: az alkalmazás magja, amely felelős az adatok feldolgozásáért és a minőségellenőrzések végrehajtásáért.
- **dignadashboard**: webalapú felület egy webszerveren, amely felhasználóbarát módon teszi lehetővé a digna platform használatát és az adathigiéniai mutatók megjelenítését.

### Mi újság a 2026.06-os kiadásban

Ez a kiadás az adathatékonysági (observability) képességeket közvetlenül a kódba hozza, lehetővé téve a fejlesztők számára, hogy az adatok forrásánál figyeljék az adatmimőséget. Részletekért lásd a [release notes](http://docs.digna.ai/changelog/Release_202606/)-t.

### Windowsot vagy Linuxot keres?

Ez az útmutató macOS-re vonatkozik. Más platformokhoz lásd a [Windows telepítési útmutatót](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) vagy a [Linux telepítési útmutatót](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Konfigurációs fájl
   - `license.toml` — Licenc fájl (másolja ide a sajátját)

A Terminalból történő kicsomagoláshoz:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Ha a dashboard másik szerveren van, adja hozzá annak URL-jét |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Szükséges, ha CORS hitelesítő adatokat is engedélyez |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Minden HTTP metódus engedélyezése |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Minden fejléc engedélyezése |

!!! note "Megjegyzés"

    Ha a dashboardot a Homebrew nginx-en szolgálja ki az alapértelmezett porton, az engedélyezendő origin: `http://localhost:8080`.

#### [repo] szekció

Ez a rész a PostgreSQL adatbázishoz való csatlakozást konfigurálja:

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
| `digna_REPO_HOST` | `localhost` vagy IP | PostgreSQL szerver hosztja/IP-je |
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
| `digna_FERNET_KEY` | Titkosítási kulcs | Tokenek és cookie-k titkosításához (alapértelmezett érkezik) |
| `digna_COOKIE_DOMAIN` | `localhost` | Illeszkedjen a frontend domainhez |
| `digna_COOKIE_SECURE` | `false` (helyi) / `true` (éles) | Használja a `true`-t HTTPS kapcsolatoknál |
| `digna_COOKIE_HTTPONLY` | `true` | Mindig engedélyezze a biztonság érdekében |
| `digna_COOKIE_SAME_SITE` | `lax` | CSRF támadások megelőzésére |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 óra) | Munkamenet lejárati ideje másodpercben |
| `digna_MAX_WORKERS` | CPU magok száma - 1 | Párhuzamos ellenőrzési feladatok száma |

!!! tip "Tipp"

    A Mac-en rendelkezésre álló CPU-magok számának megkereséséhez futtassa: `sysctl -n hw.ncpu`.

#### [logging] szekció

Ez a rész a naplózás viselkedését konfigurálja:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Paraméter | Érték | Megjegyzés |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` vagy `DEBUG` | `INFO` éles környezethez, `DEBUG` hibakereséshez |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Megőrzendő napi naplómentések száma |

---

### 2. lépés: Inicializálja a repository-t

1. Nyissa meg a **Terminalt**
2. Navigáljon a digna telepítési könyvtárába (ahol a `config.toml` és a `digna` futtatható található)
3. Futtassa a csatlakozás tesztet:

```bash
cd /opt/digna
./digna repo check
```

Vissza kell kapnia egy megerősítést, hogy a csatlakozás sikeres (magát a repository-t még nem inicializálta).

!!! note "Megjegyzés"

    macOS-en a jelenlegi könyvtárban lévő parancsok nincsenek a PATH-on, ezért a futtatható `./digna` formában indítandó. Ha szeretné a rövidebb formát használni mindenhol, adja hozzá a telepítési könyvtárat a PATH-hoz:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 3. lépés: Telepítse a repository sémát

Ugyanabban a könyvtárban futtassa:

```bash
./digna repo install
```

Ez a parancs telepíti a szükséges táblákat és sémát a PostgreSQL adatbázisba.

### 4. lépés: Indítsa el a digna szervert

A digna telepítési könyvtárban indítsa el a szervert:

```bash
./digna serve --address <host> --port <port>
```

**Paraméterek:**
- `--address` — Szerver hosztneve/IP-je
- `--port` — Szerver portja

Induláskor a következő üzeneteket kell látnia:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tipp"

    Amikor a szervert először indítja, macOS megkérdezheti, hogy szeretné-e engedélyezni az alkalmazásnak a bejövő hálózati kapcsolatok elfogadását. Kattintson az **Allow**-ra, különben a dashboard nem fogja elérni a backendet.

### 5. lépés: Hozzon létre egy admin felhasználót

1. Nyisson egy **új** Terminal ablakot
2. Navigáljon a digna telepítési könyvtárába
3. Futtassa a következő parancsot egy admin felhasználó létrehozásához:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Példa:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Ez létrehoz egy `admin` felhasználót teljes adminisztrátori jogosultsággal.

!!! tip "Tipp"

    Tegye idézőjelek közé a jelszót. A `zsh` különlegesként kezeli az olyan karaktereket, mint `!`, `$` és `*`, és egy idézőjelek nélküli jelszó ezeket nem fogja helyesen továbbítani.

!!! tip "Legjobb gyakorlat"

    Használjon erős jelszót, amely tartalmaz nagybetűt, kisbetűt, számokat és speciális karaktereket.

---

## Dashboard konfiguráció {: #dashboard-configuration }

### 1. lépés: Telepítse a dashboardot a webszerverre

A digna dashboardnak van egy külön `config.toml` fájlja a `dashboard/` könyvtárban. Ez a konfiguráció már biztosítva van, és az első beállításkor általában nem kell módosítani. Csak akkor kell szerkesztenie, ha testreszabni szeretné a backend kapcsolódást.

Ha módosítania kell a dashboard konfigurációját (pl. több példányos telepítésekhez), kövesse a dashboard dokumentációját.

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

### Mielőtt frissítene

**A digna repository biztonsági mentése kötelező**

A frissítés előtt készítsen biztonsági mentést a repository-ról (PostgreSQL), hogy védje az adatvesztéstől. A mentés biztosítja a visszaállítást, ha a frissítés közben váratlan problémák merülnek fel.

A biztonsági mentés készítése a Terminalból:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Frissítési folyamat

#### 1. lépés: Állítsa le a digna szolgáltatást

Ha a digna háttérszolgáltatásként fut, először állítsa le:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Ha a digna előtérben fut, nyomja meg a terminálablakában a `Ctrl + C`-t.

#### 2. lépés: Biztonsági mentés a jelenlegi backend telepítésről

A digna telepítési könyvtárában:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### 3. lépés: Csomagolja ki és telepítse az új verziót

1. Csomagolja ki az új digna telepítő ZIP fájlt
2. Másolja az új `digna` futtathatót és a `dashboard` mappát a telepítési könyvtárába
3. Állítsa vissza a futtathatósági bitet és szükség esetén távolítsa el a karantén attribútumot:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Fontos"

    A `config.toml` fájl SOHA nem része a telepítési ZIP-nek. A meglévő konfigurációja biztonságban marad.

### 4. lépés: Állítsa vissza a konfigurációs fájlokat

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### 5. lépés: Frissítse a repository sémát

Navigáljon a digna telepítési könyvtárába és futtassa:

```bash
cd /opt/digna
./digna repo upgrade
```

Ez frissíti a PostgreSQL sémát a legújabb verzióra, miközben megőrzi a meglévő adatokat.

### 6. lépés: Indítsa újra a szolgáltatásokat

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

#### 7. lépés: Ellenőrizze a frissítést

1. Nyissa meg a digna dashboardot
2. Ellenőrizze, hogy a felület helyesen töltődik-e
3. Nézze át a szerver naplóit esetleges hibákért