# Linux telepítési útmutató digna Release 2026.11-hoz

**Kiadás:** 2026.11

**Utoljára frissítve:** 2026. november 7.


---

## Tartalomjegyzék

1. [Bevezetés](#introduction)
2. [Rendszerkövetelmények](#system-requirements)
3. [Telepítés előtti beállítások](#pre-installation-setup)
4. [PostgreSQL szerver beállítása](#postgresql-server-setup)
5. [Webszerver konfiguráció](#web-server-configuration)
6. [Kezdeti telepítés](#initial-installation)
7. [Backend konfiguráció](#backend-configuration)
8. [Dashboard konfiguráció](#dashboard-configuration)
9. [digna futtatása systemd szolgáltatásként](#running-digna-as-a-systemd-service)
10. [Frissítés új kiadásra](#upgrading-to-a-new-release)

---

## Bevezetés {: #introduction }

### A digna-ról

A digna egy átfogó, mesterséges intelligencia által vezérelt platform, amely az adatminőség kezelését optimalizálja különböző adatkörnyezetekben, mint adattárházak, data lake-ek és lakehouse-ok. Nagy fokú skálázhatóságra és alkalmazkodóképességre tervezték; a digna automatizálással, valós idejű monitorozással és anomáliaészleléssel kezeli a modern adatszakmai kihívásokat.

A digna két fő komponensből áll:

- **digna**: az alkalmazás magja, amely az adatok feldolgozásáért és a minőségi ellenőrzések végrehajtásáért felel. Egyetlen futtatható fájlban egyesíti a háttérrendszert és a parancssori felületet, felváltva a korábbi kiadások különálló `dignabackend` és `dignacli` programjait.
- **dignadashboard**: Webes felület, amely egy webszerveren fut, felhasználóbarát módot nyújt a digna platform kezelésére és az adatminőségi metrikák vizualizálására.

### Mi újság a 2026.11 kiadásban

Ez a kiadás bevezeti a digna Data Reconciliation-t, a digna Agentic-et a digna MCP Serverrel, valamint a digna Engine-t, amely a dignán belül képes adatokat profilozni, és különböző adatbázis-technológiák között is ellenőrzi a referenciális integritást. A részletekért lásd a [kiadási megjegyzéseket](../../../changelog/Release_202611.md).

A telepítés szempontjából a kiadás új migrációs mechanizmust hoz a tárolóséma kezelésére, egy opcionális `[duckdb]` szekciót a `config.toml` fájlban a digna Engine számára, valamint új licencfájlt. Mindegyikkel a [frissítésről szóló szakasz](#upgrading-to-a-new-release) foglalkozik.

### Windows vagy macOS útmutatót keres?

Ez az útmutató Linuxra vonatkozik. Más platformokhoz lásd a [Windows telepítési útmutatót](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) vagy a [macOS telepítési útmutatót](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Melyik disztribúcióra vonatkozik az útmutató?

Az utasítások a két leggyakoribb szervercsaládra vannak írva. Ha a két család eltér, mindkét parancs szerepel:

- **Debian család** — Debian, Ubuntu. Csomagkezelő: `apt`.
- **RHEL család** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Csomagkezelő: `dnf`.

Bármely modern, `systemd`-t használó disztribúció működni fog; csak a csomagnevek és néhány konfigurációs útvonal változik.

---

## Rendszerkövetelmények {: #system-requirements }

Mielőtt hozzákezdene a telepítéshez, győződjön meg róla, hogy rendszere megfelel az alábbi minimális követelményeknek:

| Követelmény | Specifikáció |
|---|---|
| **Operációs rendszer** | Ubuntu 22.04 LTS vagy újabb, Debian 12 vagy újabb, RHEL 9 / Rocky 9 / AlmaLinux 9 vagy újabb |
| **Architektúra** | x86_64 (amd64) vagy arm64 |
| **Init rendszer** | systemd |
| **Memória (minimális telepítés)** | 16 GB RAM |
| **Lemezterület** | 10 GB szabad tárhely |
| **Adatbázis** | PostgreSQL Server 12 vagy újabb |
| **Webszerver** | nginx, Apache httpd vagy egyenértékű |

!!! info "digna Engine"

    Azokat az adatbázis-kapcsolatokat, amelyek profilozási helyként a digna Engine-t használják,
    magán a digna gazdagépen profilozza a rendszer. Ezekhez további memóriát és lemezterületet kell
    tervezni, lásd: [\[duckdb\] szekció](#duckdb-section).

### Adatbázis telepítési lehetőségek

**Ha PostgreSQL már telepítve van:**
Új adatbázist adhat hozzá a meglévő PostgreSQL szerverhez a digna tároló számára.

**Ha a PostgreSQL ugyanazon a gépen fut, mint a digna:**

!!! info "Ajánlott specifikációk"

    - **Memória**: 32 GB RAM (a 16 GB helyett)
    - **Lemezterület**: 50 GB szabad tárhely (a 10 GB helyett)

    Ezek a nagyobb erőforrások lehetővé teszik, hogy a digna és a PostgreSQL egyszerre fusson a gépen.

### A disztribúció és az architektúra ellenőrzése

Ebben az útmutatóban néhány parancs eltér a Debian és a RHEL család között. A disztribúció és az architektúra ellenőrzéséhez futtassa:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` vagy `ID=debian` — használja az `apt` parancsokat.
- `ID=rhel`, `rocky`, `almalinux` vagy `fedora` — használja a `dnf` parancsokat.
- `x86_64` vagy `aarch64` — a telepítési csomaghoz szükséges architektúra.

---

## Telepítés előtti beállítások {: #pre-installation-setup }

A digna telepítése előtt győződjön meg arról, hogy két kulcsfontosságú előfeltétel rendelkezésre áll:

1. **PostgreSQL szerver** – a számított metrikák és teljesítményadatok tárolásához
2. **Webszerver** – a digna Dashboard kiszolgálásához

Ha ezek a komponensek még nincsenek beállítva, kövesse az alábbi részeket az installálásukhoz és konfigurálásukhoz.

### A csomagindex frissítése

Frissítse a csomaglistát telepítés előtt:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Megjegyzés"

    Az útmutatóban egy párban az első parancs a **Debian családra**, a második a **RHEL családra** vonatkozik. Futtassa csak azt, amelyik a rendszeréhez illik.

---

## PostgreSQL szerver beállítása {: #postgresql-server-setup }

### Ha már van PostgreSQL

Ha a PostgreSQL már telepítve és fut a helyi gépén, vagy ha kezelt, távoli PostgreSQL szolgáltatást használ, akkor lépjen tovább a [következő szekcióhoz](#web-server-configuration).

### PostgreSQL telepítése

#### 1. lépés: A szerver csomag telepítése

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tipp"

    A disztribúciós csomagok lemaradhatnak a legfrissebb PostgreSQL kiadásoktól. Ha egy konkrét, újabb verzióra van szüksége, használja a hivatalos [PostgreSQL apt vagy yum tárolót](https://www.postgresql.org/download/linux/).

#### 2. lépés: Az adatbázis klaszter inicializálása

A **Debian családon** a csomag automatikusan létrehozza és elindítja a klasztert — lépjen tovább a következő lépésre.

A **RHEL családon** a klasztert kifejezetten létre kell hozni:

```bash
sudo postgresql-setup --initdb
```

#### 3. lépés: A szolgáltatás engedélyezése és indítása

```bash
sudo systemctl enable --now postgresql
```

Ez azonnal elindítja a PostgreSQL-t és beállítja, hogy a rendszerinduláskor automatikusan elinduljon.

#### 4. lépés: A telepítés ellenőrzése

```bash
psql --version
sudo systemctl status postgresql
```

Meg kell látnia a PostgreSQL verziót és azt, hogy a szolgáltatás `active (running)` státuszú.

#### 5. lépés: Kapcsolódás a szerverhez

A Linux PostgreSQL csomag létrehoz egy `postgres` rendszerfiókot, amely a klaszter tulajdonosa. Ezen keresztül csatlakozzon:

```bash
sudo -u postgres psql
```

!!! note "Megjegyzés — Linux itt eltér a Windowstól"

    A Windows telepítő a beállítás során jelszót kér a `postgres` szuperfelhasználóhoz. A Linux csomagok nem így működnek. Helyi kapcsolatok hitelesítése általában **peer authentication**: az operációs rendszer `postgres` felhasználója jelszó nélkül csatlakozhat a `postgres` adatbázisfelhasználóként.

    Ezért használja a fenti `sudo -u postgres` parancsot. A digna backend TCP-n keresztül, felhasználónévvel és jelszóval csatlakozik, ezért az [Kezdeti telepítés](#initial-installation) szakaszban létrehozunk egy explicit digna felhasználót.

#### 6. lépés: A port ellenőrzése

A PostgreSQL alapértelmezett portja `5432`. A szerver által használt port ellenőrzéséhez:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Jegyezze fel az értéket — szüksége lesz rá a digna backend konfigurálásakor.

#### 7. lépés: Jelszavas hitelesítés engedélyezése a digna felhasználó számára

A digna TCP-n keresztül `digna_user` felhasználóként csatlakozik, ami jelszavas hitelesítést igényel a peer/ident helyett. Ellenőrizze, hogy a `pg_hba.conf` engedélyezi-e ezt.

A fájl helyének lekérdezése:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Nyissa meg egy szerkesztővel, és győződjön meg róla, hogy a helyi TCP sorok `scram-sha-256`-et (vagy régebbi szervereken `md5`-öt) használnak `ident` helyett:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Bármilyen változtatás után töltse újra a PostgreSQL-t:

```bash
sudo systemctl reload postgresql
```

!!! warning "Fontos"

    Ha digna a következőt jelenti: `FATAL: Ident authentication failed for user "digna_user"`, akkor ez a beállítás az oka.

#### 8. lépés: Ha a PostgreSQL egy másik gépen fut

Ha másik hostról szeretne csatlakozni, állítsa be a `listen_addresses` értékét a `postgresql.conf`-ban és adjon hozzá egy megfelelő `host` sort a hálózathoz a `pg_hba.conf`-ban:

```
listen_addresses = '*'
```

Ezután nyissa meg a portot a tűzfalon és indítsa újra a szolgáltatást:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Webszerver konfiguráció {: #web-server-configuration }

A digna igényel egy webszervert a dashboard kiszolgálásához. Válasszon az alábbi lehetőségek közül:

- [nginx](#nginx-setup) — könnyű és ajánlott
- [Apache httpd](#apache-setup) — széles körben elterjedt alternatíva

Csak **egy** szervert kell telepítenie és konfigurálnia.

Mindkét szekció két dolgot állít be, amelyekre a dashboardnak szüksége van:

- **Single-page application visszaesés (fallback)**, hogy ha frissíti a dashboard URL-t, ne 404-et kapjon
- **`.md` MIME típus**, hogy a Markdown fájlok megfelelően legyenek kiszolgálva

### nginx beállítása {: #nginx-setup }

#### Áttekintés

Az nginx egy könnyű, nagy teljesítményű webszerver, amely jól alkalmas a statikus digna dashboard kiszolgálására.

#### Telepítés

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx indítása

```bash
sudo systemctl enable --now nginx
```

#### A telepítés ellenőrzése

1. Nyissa meg a böngészőt
2. Navigáljon a `http://localhost` címre
3. Látnia kell az nginx üdvözlőoldalát

#### A tűzfal megnyitása

Ha a szerver más gépek felől is elérhető, engedélyezze a HTTP forgalmat:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Webhely konfigurálása a dashboardhoz

Az nginx betölti a `conf.d` könyvtárban található összes fájlt mindkét disztribúció esetén. Hozzon létre egy dedikált konfigurációs fájlt a digna számára ott:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Illessze be a következőt, cserélje ki a `/opt/digna/dashboard`-ot a tényleges, kicsomagolt `dashboard` mappa elérési útjára:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    A `try_files` direktíva nélkül a dashboard bármely oldalának újratöltése a gyökér URL kivételével 404-et ad vissza. Ez az nginx egyenértéke annak az URL Rewrite modulnak, amely Windows alatt az IIS-hez szükséges.

#### Az alapértelmezett oldal letiltása

Csak egy server block lehet `default_server` egy porton. A **Debian családon** távolítsa el a csomagolt alapértelmezettet, hogy ne ütközzön:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

A **RHEL családon** kommentelje ki vagy törölje a `server { ... }` blokkot a `/etc/nginx/nginx.conf` fájlban.

#### A konfiguráció alkalmazása

Ellenőrizze a konfigurációt szintaktikai hibák után, majd töltse újra az nginx-et:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd beállítása {: #apache-setup }

#### Áttekintés

Az Apache httpd megtalálható a támogatott disztribúciók alapértelmezett tárolóiban. A csomag neve a Debian családon `apache2`, a RHEL családon pedig `httpd`.

#### Telepítés

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache indítása

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### A telepítés ellenőrzése

1. Nyissa meg a böngészőt
2. Navigáljon a `http://localhost` címre
3. Látnia kell a disztribúció alapértelmezett Apache oldalát

#### Kötelező: mod_rewrite engedélyezése

A dashboard URL átírást igényel.

A **Debian családon** engedélyezze a modult és indítsa újra:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

A **RHEL családon** a `mod_rewrite` alapból betöltődik. Ellenőrizze:

```bash
httpd -M | grep rewrite
```

#### Kötelező: .htaccess felülírások engedélyezése

Nyissa meg a dokumentumgyökér konfigurációs fájlját:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Keresse meg azt a `<Directory>` blokkot, amely a dokumentumgyökért lefedi (`/var/www/html` mindkét családon), és módosítsa:

```apache
AllowOverride None
```

erre:

```apache
AllowOverride All
```

#### Kötelező: MIME típus a Markdown fájlokhoz

Ugyanebben a fájlban adja hozzá az alábbi sort, hogy a Markdown fájlok helyesen legyenek kiszolgálva:

```apache
AddType text/markdown .md
```

!!! warning "Fontos"

    Ennek a beállításnak a hiányában a `.md` fájlok nem biztos, hogy megfelelően szolgálódnak ki.

#### A konfiguráció alkalmazása

Ellenőrizze a szintaxist, majd indítsa újra az Apache-ot:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Kezdeti telepítés {: #initial-installation }

### 1. lépés: A digna tároló beállítása

A digna tároló (repository) tárolja a digna által számított összes metrikát. Központi adatbázisként szolgál az analitikai és teljesítményadatok számára.

#### Sémalétrehozás és felhasználó létrehozása a repóhoz

Nyissa meg a PostgreSQL kliensét (psql, pgAdmin vagy hasonló), és futtassa az alábbi SQL parancsokat:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Cserélje ki a következő helykitöltőket:**

- `<digna_repo_schema>` — A kívánt sémanév (pl. `dignarepo`)
- `<digna_repo_user>` — A kívánt felhasználónév (pl. `digna_user`)
- `<digna_repo_password>` — Biztonságos jelszó ehhez a felhasználóhoz

**Példa:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

A parancsok egy lépésben történő futtatásához a shellből:

```bash
sudo -u postgres psql
```

Majd illessze be a kéréseket a `postgres=#` promptnál, és írja be a `\q` parancsot a kilépéshez.

!!! tip "Legjobb gyakorlat"

    Használjon erős, összetett jelszavakat az adatbázis-felhasználókhoz. Kerülje a könnyen kitalálható hitelesítő adatokat.

---

### 2. lépés: A digna telepítési csomag kicsomagolása

1. Keresse meg a Önnek biztosított digna ZIP fájlt
2. Csomagolja ki a kívánt telepítési helyre — például `/opt/digna`
3. A kicsomagolás után a következő elemeket kell látnia:
   - `dashboard/` — Webes dashboard felület
   - `digna` — Fő futtatható állomány (backend + CLI kombinálva)

!!! info "A konfigurációs és a licencfájl nincs benne a csomagban"

    Sem a `config.toml`, sem a `dashboard/dashboard_config.toml` nem része a telepítésnek — mindkettőt
    Önnek kell létrehoznia, a [Backend konfiguráció](#backend-configuration) és a
    [Dashboard konfiguráció](#dashboard-configuration) szakaszban leírtak szerint. A `license.toml` sem
    része a csomagnak; a digna külön biztosítja, ahogyan a 3. lépés leírja.

A kicsomagoláshoz shellből:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Megjegyzés"

    Ha az `unzip` nincs telepítve, telepítse: `sudo apt install -y unzip` vagy `sudo dnf install -y unzip`.

#### Tegye futtathatóvá a binárist

A fájl átvitele során a futtathatóság elveszhet. Állítsa be expliciten:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Szolgáltatási fiók létrehozása

Ajánlott a backend futtatása dedikált, korlátozott jogosultságú felhasználóként:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Megjegyzés"

    A RHEL családon az egyenértékű shell útvonala `/sbin/nologin`.

### 3. lépés: A licence fájl telepítése

!!! warning "Fontos"

    A licence fájl **nem** része a telepítési csomagnak; külön kerül Önnek átadásra a digna-tól.

1. Keresse meg a kapott `license.toml` fájlt
2. Másolja be a digna telepítési könyvtár gyökerébe (ahol a `config.toml` és a `digna` futtatható fájl található)

**Miért fontos ez:**
A license fájl tartalmazza az ügyféladatokat, a licenc lejárati dátumát és a digitális aláírást. **Ne módosítsa ezt a fájlt** — bármilyen változtatás érvényteleníti a licencet.

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

### 1. lépés: A konfigurációs fájl létrehozása és szerkesztése

A `config_template.toml` fájl megtalálható a digna telepítési könyvtárban. Csak át kell neveznie `config.toml`-ra.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Elérési út:** `/opt/digna/config.toml`

Nyissa meg a `config.toml`-t egy szövegszerkesztővel, és állítson be minden alábbi szekciót.

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

    Ha a dashboard-ot nginx vagy Apache szolgálja ki az alapértelmezett HTTP porton, az engedélyezendő origin `http://localhost` — vagy a szerver publikus URL-je, ha a dashboard más gépekről is elérhető.

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
| `DIGNA_REPO_HOST` | `localhost` vagy IP | PostgreSQL szerver hoszt/IP |
| `DIGNA_REPO_PORT` | `5432` (alapértelmezett) | PostgreSQL port |
| `DIGNA_REPO_DB` | `postgres` | Adatbázis neve |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Korábban létrehozott séma |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL-ben létrehozott felhasználó |
| `DIGNA_REPO_PASSWORD` | Az Ön jelszava | A sémalétrehozáskor beállított jelszó |
| `DIGNA_REPO_SSLMODE` | `prefer` (alapértelmezett) | Opcionális. PostgreSQL SSL mód: `disable`, `allow`, `prefer`, `require`, `verify-ca` vagy `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (alapértelmezett) | Opcionális. A digna által a repóhoz nyitva tartott kapcsolatok száma |

!!! tip "Legjobb gyakorlat"

    A `config.toml` jelszót tartalmaz tiszta szövegként. Korlátozza a fájl jogosultságait, hogy csak a szolgáltatási fiók olvashassa:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

!!! tip "Tipp"

    Az elérhető CPU magok számának meghatározásához futtassa: `nproc`.

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
| `DIGNA_LOGGING_MODE` | `INFO` vagy `DEBUG` | `INFO` éles környezethez, `DEBUG` hibaelhárításhoz. A `TRACE`, `WARN` és `ERROR` érték is elfogadott |
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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Alapértelmezés: a rendszer ideiglenes könyvtára (`$TMPDIR`, vagy `/tmp`, ha nincs beállítva) | Az ideiglenes fájlok könyvtára arra az esetre, ha az adatok nem férnek el a memóriában |

!!! tip "A digna Engine méretezése"

    A digna gazdagépen a digna saját memóriaigényén felül legfeljebb `DIGNA_MAX_WORKERS` ×
    `DIGNA_DUCKDB_MEMORY_LIMIT_MB` memóriával kell számolni, az ideiglenes könyvtárban pedig annyi
    szabad lemezterülettel, amennyi a digna Engine-t használó adatforrások legnagyobb vizsgált napjának
    adatait befogadja. A `DIGNA_DUCKDB_TEMP_DIRECTORY` beállítást egy ekkora szabad hellyel rendelkező
    lemezre kell irányítani, amelyre a dignát futtató fiók írni tud:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

### 3. lépés: A repó inicializálása

1. Nyisson meg egy terminált
2. Navigáljon a digna telepítési könyvtárába (ahol a `config.toml` és a `digna` futtatható található)
3. Futtassa a kapcsolat tesztet:

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

    Linuxon az aktuális könyvtár nincs a PATH-on, ezért az futtatható `./digna` formában hívandó, nem csak `digna`. Ha mindenhol rövidebb formát szeretne használni, hozzon létre egy szimbolikus linket:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### 4. lépés: A repó séma telepítése

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

### 5. lépés: Admin felhasználó létrehozása

1. Nyisson meg egy **új** terminált
2. Navigáljon a digna telepítési könyvtárába
3. Futtassa a következő parancsot admin felhasználó létrehozásához:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Példa:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Ezzel létrejön egy felhasználó `admin@example.com` e-mail-címmel és teljes rendszergazdai jogosultságokkal.

!!! tip "Tipp"

    Tegye egyes idézőjelek közé a jelszót. A `bash` és `zsh` speciális karakterként kezel néhány szimbólumot (`!`, `$`, `*`), és ha nincsenek idézőjelek, a jelszó nem lesz megfelelően továbbítva.

!!! tip "Legjobb gyakorlat"

    Használjon erős jelszót, amely nagy- és kisbetűket, számokat és speciális karaktereket is tartalmaz.

---

### 6. lépés: A digna szerver indítása

A digna telepítési könyvtárában indítsa el a szervert:

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

    Ha a dashboard egy másik gépről éri el a backendet, engedélyezze az API portot a tűzfalon:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "A kiszolgáló lefoglalja a terminált"

    A `serve` az előtérben fut, és addig működik, amíg le nem állítja a ++ctrl+c++ billentyűkkel. Hagyja futni, amíg befejezi a beállítást; ha inkább rendszerindításkor indulna automatikusan, lásd: [A digna futtatása systemd-szolgáltatásként](#running-digna-as-a-systemd-service).

## Dashboard konfiguráció {: #dashboard-configuration }

### 1. lépés: A dashboard telepítése a webszerverre

A digna dashboard a saját konfigurációját a `dashboard/dashboard_config.toml` fájlból olvassa. Ez a fájl nem része a telepítésnek — Önnek kell létrehoznia a `dashboard/` könyvtárban, a dashboard fájljai mellett.

A tartalmát az [Egyszeri bejelentkezés (SSO)](../../../sso/overview.md) oldal írja le, és ott is van rá szükség: ez tartalmazza a dashboard által kínált bejelentkezési lehetőségeket, valamint több példányos telepítéseknél a backend kapcsolatot.

Válassza ki a webszervert, és kövesse a hozzá tartozó telepítési lépéseket.

#### Telepítés nginx-re

Ha követte az [nginx beállítást](#nginx-setup), a server block már a `dashboard` mappájára mutat, így másolás nem szükséges.

1. **Ellenőrizze az elérési utat**
   - Nyissa meg a `/etc/nginx/conf.d/digna.conf` fájlt
   - Ellenőrizze, hogy a `root` a kicsomagolt `dashboard` mappára mutat-e

2. **Biztosítsa, hogy a mappa olvasható legyen**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Töltse újra az nginx-et**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Telepítés tesztelése**
   - Nyissa meg a böngészőt
   - Navigáljon a `http://localhost` (vagy a konfigurált URL) címre
   - Látnia kell a digna dashboard bejelentkezési oldalát

#### Telepítés Apache httpd-re

1. **Másolja a dashboardot a dokumentumgyökérbe**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Adja hozzá az átírási szabályokat**

   Hozzon létre egy `.htaccess` fájlt a telepített mappában, hogy a dashboard útvonalai frissítéskor ne törjenek el:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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

3. **Apache újraindítása**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Dashboard elérése**
   - Nyissa meg a böngészőt
   - Navigáljon a `http://localhost/digna` címre
   - Látnia kell a digna dashboard bejelentkezési oldalát

### 2. lépés: SELinux (csak RHEL család)

RHEL, Rocky, AlmaLinux és Fedora rendszereken az SELinux alapértelmezetten enforcing módban fut, és blokkolhatja a webszervert, ha a fájlok nem a várt helyen vannak. Ellenőrizze, hogy aktív-e:

```bash
getenforce
```

Ha a kimenet `Enforcing`, és a dashboard az `/opt/digna/dashboard` alatt van kiszolgálva, címkézze fel a könyvtárat, hogy a webszerver olvasni tudja:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Megjegyzés"

    Ha a `semanage` nem található, telepítse: `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Fontos"

    Egy frissen konfigurált RHEL szerveren a **403 Forbidden** hibát a dashboard esetében szinte mindig SELinux címkézési probléma okozza, nem fájljogosultsági hiba. Ellenőrizze az eseményeket: `sudo ausearch -m avc -ts recent`.

---

## digna futtatása systemd szolgáltatásként {: #running-digna-as-a-systemd-service }

### Miért futtassuk a digna-t szolgáltatásként?

A digna backend systemd szolgáltatásként futtatva biztosítja, hogy:

- Automatikusan elindul a gép indításakor
- Háttérben fusson, terminál nélkül
- Automatikusan újrainduljon, ha összeomlik
- A `systemctl` segítségével kezelhető legyen, az ipari szabvány Linux szolgáltatáskezelő

### Szolgáltatáskezelő fájlok

Minden szükséges fájl a digna telepítési könyvtárában található: `bin/`

A következő shell scriptek állnak rendelkezésre:

- `install_service.sh` — digna regisztrálása systemd-ben
- `uninstall_service.sh` — a szolgáltatás eltávolítása
- `start_service.sh` — a regisztrált szolgáltatás indítása
- `stop_service.sh` — a futó szolgáltatás leállítása

!!! warning "Root jogosultság szükséges"

    Minden scriptet `sudo`-val kell futtatni, mert a rendszerindításkor induló szolgáltatás regisztrálása egységfájlt ír a `/etc/systemd/system`-be.

### A scriptek futtathatóvá tétele

A kicsomagolás során a futtatható bit eltűnhet. Első használat előtt:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### A szolgáltatás telepítése

1. **Nyisson meg egy terminált**

2. **Navigáljon a bin mappába**
   ```bash
   cd /opt/digna/bin
   ```

3. **Futtassa a telepítő scriptet**
   ```bash
   sudo ./install_service.sh
   ```

A digna szerver most regisztrálva van a systemd-ben automatikus indítással. A szolgáltatás nem indul el automatikusan azonnal — a következő szakaszban találja az indítást.

### A szolgáltatás indítása és leállítása

#### A szolgáltatás indításához

1. Nyisson egy terminált
2. Navigáljon a `/opt/digna/bin` könyvtárba
3. Futtassa:
   ```bash
   sudo ./start_service.sh
   ```

#### A szolgáltatás leállításához

1. Nyisson egy terminált
2. Navigáljon a `/opt/digna/bin` könyvtárba
3. Futtassa:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tipp"

    Mindig állítsa le a szolgáltatást a frissítés előtt az alkalmazásfájlok módosítása előtt.

### A szolgáltatás kezelése systemctl-lel

Regisztrálás után a szolgáltatás a standard systemd parancsokkal is vezérelhető bármely könyvtárból:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### A szolgáltatás ellenőrzése

Annak megerősítéséhez, hogy a szolgáltatás regisztrálva és fut:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

Az `enabled` azt jelenti, hogy a szolgáltatás indul a rendszerinduláskor; az `active` azt jelenti, hogy éppen fut.

### A szolgáltatás naplóinak megtekintése

A systemd rögzíti mindazt, amit a backend a konzolra ír. A naplók olvasása:

```bash
sudo journalctl -u digna -n 100
```

Élőben követéshez, például hib reprodukálása közben:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tipp"

    Ez a leggyorsabb mód annak diagnosztizálására, ha a szolgáltatás elindul és azonnal leáll. Itt jelentődik a repókapcsolat hiba vagy a hiányzó `license.toml`.

### Az alkalmazás áthelyezése másik könyvtárba

Az egységfájl abszolút elérési utat tárol a futtathatóhoz, ezért az áthelyezés újra-regisztrálást igényel:

1. **A jelenlegi szolgáltatás eltávolítása**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Az alkalmazás fájljainak áthelyezése**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **A szolgáltatás újratelepítése**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **A szolgáltatás indítása**
   ```bash
   sudo ./start_service.sh
   ```

### A szolgáltatás eltávolítása

1. **A futó szolgáltatás leállítása**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **A szolgáltatás eltávolítása**
   ```bash
   sudo ./uninstall_service.sh
   ```

A digna szerver most eltávolításra került a systemd regisztrációjából.

---

## Frissítés új kiadásra {: #upgrading-to-a-new-release }

Ez a szakasz egy Release 2026.06 telepítés frissítését írja le Release 2026.11-re.

!!! warning "Frissítés 2026.06-nál régebbi kiadásról"

    Először a Release 2026.06 frissítési lépéseit kell végrehajtani: [Frissítés új kiadásra](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). Ezután az alábbi lépésekkel lehet folytatni.

### Mielőtt frissítene

**A digna repó biztonsági mentése kötelező**

A digna frissítése előtt készítsen biztonsági mentést a repóról (PostgreSQL), hogy elkerülje az
adatvesztést. A mentés biztosítja, hogy vissza tudja állítani az adatokat, ha a frissítés során váratlan
probléma lép fel.

Mentés készítése shellből:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**A Release 2026.11 licencfájljának igénylése**

A Release 2026.11 új `license.toml` fájlt igényel. Kérje el a digna csapattól még a kezdés előtt, és
tartsa készenlétben a [7. lépéshez](#step-7-replace-the-license-file).

### Frissítési folyamat

#### 1. lépés: A digna szolgáltatás leállítása {: #step-1-stop-the-digna-service }

Ha a digna systemd szolgáltatásként fut, először állítsa le:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Ha a digna előtérben fut, nyomja meg a ++ctrl+c++ billentyűket a terminálablakában.

#### 2. lépés: Mentse a jelenlegi telepítést {: #step-2-backup-current-installation }

A digna telepítési könyvtárában nevezze át a jelenlegi telepítés futtatható fájlját és dashboard
mappáját, hogy az új kiadás melléjük telepíthető legyen:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

A `digna_old` fájlt tartsa meg, amíg nem ellenőrizte a frissítést, a `dashboard_old` mappát
pedig addig, amíg vissza nem állította belőle a konfigurációs fájljait (lásd a 4. lépést).
Utána mindkettő törölhető.

#### 3. lépés: Az új verzió kicsomagolása és telepítése {: #step-3-extract-and-deploy-new-version }

1. Csomagolja ki az új digna ZIP fájlt
2. Másolja az új `digna` futtathatót és a `dashboard` mappát a telepítési könyvtárba
3. Állítsa vissza a futtathatóságot és a szolgáltatási fiók tulajdonjogát:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Fontos"

    Sem a `config.toml`, sem a `dashboard/dashboard_config.toml` **soha** nem része a
    telepítési ZIP-nek — a digna csapat egyik fájlt sem szállítja. A meglévő konfigurációját
    ezért a frissítés nem érinti, és az átnevezett `*_old` mappákban lévő példányok az
    egyetlenek, amelyekkel rendelkezik.

#### 4. lépés: Konfigurációs fájlok visszaállítása {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

#### 5. lépés: A webszerver újratöltése {: #step-5-reload-the-web-server }

A dashboard statikus fájlok összessége, ezért előfordulhat, hogy a webszerver — és a böngésző — még
az előző verziót szolgálja ki. Töltse újra vagy indítsa újra azt a webszervert, amely a `dashboard`
mappát kiszolgálja, majd töltse be újra az oldalt kényszerített frissítéssel (++ctrl+f5++).

#### 6. lépés: Ellenőrizze a konfigurációt {: #step-6-validate-the-configuration }

Mielőtt a repóhoz nyúlna, győződjön meg róla, hogy a `config.toml` teljes:

```bash
./digna config check
```

Minden szekciónak OK állapotot kell jelentenie. Javítson ki mindent, amit FAILED állapotúként jelent,
távolítsa el az **Unknown keys** alatt felsorolt kulcsokat, és a folytatás előtt futtassa újra
a parancsot.

#### 7. lépés: A licencfájl cseréje {: #step-7-replace-the-license-file }

Egy korábbi kiadáshoz kiállított licencfájl nem működik a Release 2026.11 verzióval. Másolja a
digna csapat által a Release 2026.11-hez biztosított `license.toml` fájlt a telepítési könyvtárba,
felülírva a régit:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ne tartsa meg a korábbi licencet"

    A korábbi licenccel minden parancs, amely ellenőrzi a licencet — `serve`, `user`,
    `inspection`, `repo` — hibával leáll, így a digna nem indul el, és a repó nem frissíthető.
    Ellenőrizze az új licencet, mielőtt továbblép:

    ```bash
    ./digna license check
    ```

#### 8. lépés: A repó sémájának frissítése {: #step-8-upgrade-the-repository-schema }

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

#### 9. lépés: Szolgáltatások újraindítása {: #step-9-restart-services }

Ha systemd szolgáltatásként fut:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Ha kézzel futtatja, indítsa újra a szervert:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Ha nginx-et vagy Apache-ot használ, töltse újra a megfelelő webszervert:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

A RHEL családon alkalmazza újra az SELinux címkézést, ha a `dashboard` könyvtárat kicserélték:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### 10. lépés: A frissítés ellenőrzése {: #step-10-verify-the-upgrade }

1. Ellenőrizze az új futtatható fájl kiadását:

    ```bash
    ./digna version
    ```

    Az első sornak így kell szólnia: `Release: 2026.11`.

2. Nyissa meg a digna dashboardot, és ellenőrizze, hogy a felület helyesen töltődik-e be.
3. Nézze át a szerver naplóit hibák után kutatva:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Tesztelje az adatbázis-kapcsolatokat — lásd:
   [Kapcsolat tesztelése](../../../databases/overview.md#testing-a-connection).

Az új modulok használatának megkezdéséhez lásd: [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI-ügynök csatlakoztatása](../../../platform/agentic/connect_ai_agent.md) a digna MCP Serverhez, valamint
[Profilozási hely](../../../platform/profiling/profiling_location.md) a digna Engine-hez.