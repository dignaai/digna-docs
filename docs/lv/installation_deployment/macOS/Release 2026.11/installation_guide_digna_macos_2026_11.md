---
title: macOS instalācijas ceļvedis – digna Release 2026.11 | digna dokumentācija
description: Soli pa solim ceļvedis par digna Release 2026.11 uzstādīšanu macOS — sistēmas prasības, Homebrew un PostgreSQL iestatīšana, nginx vai Apache konfigurācija, backend un paneļa konfigurācija, digna darbība kā fona serviss un jaunināšana no Release 2026.06.
keywords: digna macOS instalācija, digna mac izvietošanas ceļvedis, digna backend iestatīšana, digna paneļa instalācija, postgresql homebrew, nginx macos, digna launchd serviss, digna jaunināšanas ceļvedis
image: /assets/logo_square.png
---

# macOS instalācijas ceļvedis digna Release 2026.11

**Izlaidums:** 2026.11

**Pēdējais atjauninājums:** 2026. gada 7. novembris


---

## Saturs

1. [Ievads](#introduction)
2. [Sistēmas prasības](#system-requirements)
3. [Priekšinstalācijas sagatavošana](#pre-installation-setup)
4. [PostgreSQL servera iestatīšana](#postgresql-server-setup)
5. [Tīmekļa servera konfigurācija](#web-server-configuration)
6. [Sākotnējā instalācija](#initial-installation)
7. [Backend konfigurācija](#backend-configuration)
8. [Paneļa konfigurācija](#dashboard-configuration)
9. [digna palaide kā fona serviss](#running-digna-as-a-background-service)
10. [Jaunināšana uz jaunu izlaidumu](#upgrading-to-a-new-release)

---

## Ievads {: #introduction }

### Par digna

digna ir visaptveroša ar mākslīgo intelektu balstīta platforma, kas paredzēta datu kvalitātes pārvaldības optimizēšanai dažādās datu vidēs, piemēram, noliktavās, ezeros un lakehouse risinājumos. Izstrādāta kā mērogojama un pielāgojama sistēma, digna risina mūsdienu datu izaicinājumus, izmantojot automatizāciju, reāllaika uzraudzību un anomāliju atklāšanu.

digna sastāv no divām galvenajām komponentēm:

- **digna**: lietojumprogrammas kodols, kas atbild par datu apstrādi un kvalitātes pārbaužu veikšanu. Tas apvieno backend un komandrindas saskarni vienā izpildāmajā failā un aizstāj iepriekšējo laidienu atsevišķās programmas `dignabackend` un `dignacli`.
- **dignadashboard**: tīmekļa saskarne, kas izvietota uz tīmekļa servera un nodrošina lietotājam draudzīgu veidu, kā mijiedarboties ar digna platformu un vizualizēt datu kvalitātes metrikas.

### Kas jauns izlaidumā 2026.11

Šis izlaidums pievieno digna Data Reconciliation, digna Agentic ar digna MCP Server un digna Engine, kas var profilēt datus pašā digna un pārbaudīt referenciālo integritāti starp dažādām datubāzu tehnoloģijām. Pilnas detaļas skatiet [izlaiduma piezīmēs](../../../changelog/Release_202611.md).

Instalācijai šis izlaidums ievieš jaunu repozitorija migrāciju mehānismu, neobligātu `[duckdb]` sadaļu failā `config.toml` digna Engine vajadzībām un jaunu licences failu. Katrs no tiem ir aprakstīts [jaunināšanas sadaļā](#upgrading-to-a-new-release).

### Meklējat Windows vai Linux?

Šis ceļvedis attiecas uz macOS. Citu platformu instalācijas skaidrojumu skatiet [Windows instalācijas ceļvedī](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) vai [Linux instalācijas ceļvedī](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Sistēmas prasības {: #system-requirements }

Pirms instalācijas pārliecinieties, ka jūsu sistēma atbilst šādām minimālajām prasībām:

| Prasība | Specifikācija |
|---|---|
| **Operētājsistēma** | macOS 13 (Ventura) vai jaunāka |
| **Arhitektūra** | Apple Silicon (arm64) vai Intel (x86_64) |
| **Atmiņa (minimālā konfigurācija)** | 16 GB RAM |
| **Diskā nepieciešamā vieta** | 10 GB brīvas vietas |
| **Datubāze** | PostgreSQL Server 12 vai jaunāks |
| **Tīmekļa serveris** | nginx, Apache httpd vai ekvivalents |
| **Komandrindas rīki** | Xcode Command Line Tools (nepieciešami Homebrew) |

!!! info "digna Engine"

    Datubāzes savienojumi, kuru profilēšanas vieta ir digna Engine, tiek profilēti pašā digna resursdatorā. Paredziet tiem papildu atmiņu un diska vietu, skatiet [\[duckdb\] sadaļu](#duckdb-section).

### Datubāzes instalācijas iespējas

**Ja PostgreSQL jau ir instalēts:**
Jūs varat pievienot jaunu datubāzi digna esošajam PostgreSQL serverim.

**Ja instalējat PostgreSQL uz tā paša datora kā digna:**

!!! info "Ieteicamās specifikācijas"

    - **Atmiņa**: 32 GB RAM (nevis 16 GB)
    - **Diskā nepieciešamā vieta**: 50 GB brīvas vietas (nevis 10 GB)

    Šīs augstākās specifikācijas nodrošina pietiekamus resursus vienlaicīgai digna un PostgreSQL datubāzes darbībai.

### Arhitektūras noskaidrošana

Vairāki šī ceļveža ceļi atšķiras Apple Silicon un Intel Mac datoriem. Lai noskaidrotu, kurš ir jums, atveriet **Terminal** un palaidiet:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew tiek instalēts direktorijā `/opt/homebrew`.
- `x86_64` — Intel. Homebrew tiek instalēts direktorijā `/usr/local`.

!!! tip "Padoms"

    Tā vietā, lai norādītu kādu no ceļiem tieši, šajā ceļvedī tiek izmantots `$(brew --prefix)`, kas abās arhitektūrās izvēršas par pareizo atrašanās vietu. Komandas varat kopēt burtiski.

---

## Priekšinstalācijas sagatavošana {: #pre-installation-setup }

Pirms digna instalēšanas pārliecinieties, ka ir izpildīti trīs galvenie priekšnosacījumi:

1. **Homebrew** – pakotņu pārvaldnieks, ar ko tiek instalētas tālāk minētās sastāvdaļas
2. **PostgreSQL Server** – aprēķināto metrikas un veiktspējas datu glabāšanai
3. **Tīmekļa serveris** – digna paneļa izvietošanai

Ja šīs sastāvdaļas vēl nav iestatītas, izpildiet tālāk norādītās sadaļas, lai tās instalētu un konfigurētu.

### Homebrew instalēšana

Homebrew ir standarta pakotņu pārvaldnieks operētājsistēmai macOS, un visā šajā ceļvedī tas tiek izmantots PostgreSQL un nginx instalēšanai.

#### 1. solis: Pārbaudīt, vai Homebrew jau ir instalēts

Atveriet **Terminal** (nospiediet `Cmd + Space`, ierakstiet `Terminal`, nospiediet Enter) un palaidiet:

```bash
brew --version
```

Ja tiek atgriezts versijas numurs, pārejiet uz sadaļu [PostgreSQL servera iestatīšana](#postgresql-server-setup).

#### 2. solis: Instalēt Homebrew

Ja komanda netika atrasta, instalējiet Homebrew, izpildot norādījumus [oficiālajā Homebrew vietnē](https://brew.sh). Instalators arī instalē Xcode Command Line Tools, ja tie vēl nav pieejami.

#### 3. solis: Pievienot Homebrew savam PATH

Apple Silicon datoros instalators izvada divas komandas, kas pievieno Homebrew jūsu čaulas videi. Palaidiet tās, kā norādīts, un pēc tam pārbaudiet:

```bash
brew --prefix
```

Tam jāizvada `/opt/homebrew` Apple Silicon datorā vai `/usr/local` Intel datorā.

---

## PostgreSQL servera iestatīšana {: #postgresql-server-setup }

### Ja PostgreSQL jau ir pieejams

Ja PostgreSQL jau ir instalēts un darbojas uz jūsu lokālā datora vai ja izmantojat pārvaldītu attālo PostgreSQL serveri, varat pāriet uz [nākamo sadaļu](#web-server-configuration).

### Instalācijas iespējas

macOS piedāvā divus vienkāršus PostgreSQL instalēšanas veidus. Izvēlieties **vienu**:

- [Homebrew](#postgresql-homebrew) — instalēšana no komandrindas, ieteicama servera izvietojumiem
- [Postgres.app](#postgresql-app) — grafiska instalēšana, ērta lokālai izvērtēšanai

### PostgreSQL instalēšana ar Homebrew {: #postgresql-homebrew }

#### 1. solis: Instalēt PostgreSQL formulu

```bash
brew install postgresql@16
```

#### 2. solis: Pievienot PostgreSQL savam PATH

Versionētās PostgreSQL formulas ir *keg-only*, kas nozīmē, ka Homebrew to komandas automātiski nepiesaista jūsu PATH. Pievienojiet tās paši:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Piezīme"

    Tas pieņem, ka izmantojat macOS noklusējuma čaulu `zsh`. Ja izmantojat `bash`, tā vietā pievienojiet to pašu rindu failam `~/.bash_profile`.

#### 3. solis: Palaist PostgreSQL servisu

```bash
brew services start postgresql@16
```

Tas nekavējoties palaiž PostgreSQL un konfigurē to automātiski startēt atkal, kad jūs piesakāties.

#### 4. solis: Pārbaudīt instalāciju

```bash
psql --version
```

Ja instalācija bija veiksmīga, tiks parādīta PostgreSQL versija.

#### 5. solis: Pieslēgties serverim

```bash
psql postgres
```

!!! warning "Svarīgi — šeit macOS atšķiras no Windows"

    Windows instalators lūdz izveidot superlietotāju `postgres` un paroli. Homebrew to nedara. Tā vietā tas izveido superlietotāju, kas nosaukts jūsu **macOS konta** vārdā, bez paroles un pieejamu tikai no lokālā datora.

    Tas nozīmē, ka svaigā Homebrew instalācijā lomas `postgres` nav. Kad nepieciešams superlietotājs, izmantojiet sava konta vārdu, un izveidojiet atsevišķu digna lietotāju, kā aprakstīts sadaļā [Sākotnējā instalācija](#initial-installation).

#### 6. solis: Pārbaudīt portu

Noklusējuma PostgreSQL ports ir `5432`. Lai pārbaudītu, kurā portā jūsu serveris klausās:

```bash
psql postgres -c "SHOW port;"
```

Pierakstiet šo vērtību — tā būs nepieciešama, konfigurējot digna backend.

### PostgreSQL instalēšana ar Postgres.app {: #postgresql-app }

Ja dodat priekšroku grafiskai instalēšanai:

1. Lejupielādējiet [Postgres.app](https://postgresapp.com) un ievelciet to mapē **Applications**
2. Atveriet lietotni un noklikšķiniet **Initialize**, lai izveidotu jaunu serveri
3. Izpildiet lietotnes norādījumus, lai pievienotu tās komandrindas rīkus savam PATH
4. Pārbaudiet instalāciju:

```bash
psql --version
```

Arī Postgres.app izveido superlietotāju, kas nosaukts jūsu macOS konta vārdā.

---

## Tīmekļa servera konfigurācija {: #web-server-configuration }

digna prasa tīmekļa serveri paneļa izvietošanai. Izvēlieties vienu no šīm iespējām:

- [nginx](#nginx-setup) — instalēts ar Homebrew, ieteicams
- [Apache httpd](#apache-setup) — iekļauts macOS

Nepieciešams instalēt un konfigurēt tikai **vienu** no šiem serveriem.

Abās sadaļās tiek konfigurētas divas lietas, no kurām panelis ir atkarīgs:

- **Vienas lapas lietotnes (SPA) rezerves maršruts**, lai paneļa URL atsvaidzināšana neatgrieztu 404
- **`.md` MIME tips**, lai Markdown faili tiktu servēti pareizi

### nginx iestatīšana {: #nginx-setup }

#### Pārskats

nginx ir viegls, augstas veiktspējas tīmekļa serveris, kas labi piemērots statiskā digna paneļa servēšanai.

#### Instalēšana

```bash
brew install nginx
```

#### nginx palaišana

```bash
brew services start nginx
```

#### Pārbaudīt instalāciju

1. Atveriet pārlūkprogrammu
2. Dodieties uz `http://localhost:8080`
3. Jums jāredz nginx sveiciena lapa

!!! note "Piezīme — noklusējuma ports ir 8080, nevis 80"

    Homebrew konfigurē nginx klausīties portā `8080`, lai tas varētu darboties bez administratora tiesībām. macOS sistēmā piesaistei portam `80` vai jebkuram citam portam zem 1024 nepieciešamas root tiesības.

    Lai servētu paneli portā 80, tālāk dotajā konfigurācijā nomainiet `listen 8080;` uz `listen 80;` un palaidiet nginx ar `sudo brew services start nginx`.

#### Vietnes konfigurēšana panelim

Homebrew nginx konfigurācija iekļauj katru failu no savas `servers` direktorijas. Izveidojiet tur atsevišķu konfigurācijas failu digna vajadzībām:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Ielīmējiet tālāk norādīto, aizstājot `/path/to/digna/dashboard` ar faktisko ceļu līdz izpakotajai `dashboard` mapei:

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

!!! warning "Svarīgi"

    Bez direktīvas `try_files` jebkuras paneļa lapas, izņemot saknes URL, pārlādēšana atgriež 404. Tas ir nginx ekvivalents URL Rewrite modulim, kas nepieciešams IIS operētājsistēmā Windows.

#### Piemērot konfigurāciju

Pārbaudiet, vai konfigurācijā nav sintakses kļūdu, un pēc tam pārlādējiet nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd iestatīšana {: #apache-setup }

#### Pārskats

macOS ietver Apache httpd, tāpēc instalēšana nav nepieciešama. Pēc noklusējuma tas ir atspējots.

#### Apache palaišana

```bash
sudo apachectl start
```

#### Pārbaudīt instalāciju

1. Atveriet pārlūkprogrammu
2. Dodieties uz `http://localhost`
3. Jums jāredz ziņojums "It works!"

#### Obligāti: iespējot mod_rewrite

Panelim nepieciešama URL pārrakstīšana. Atveriet Apache konfigurāciju:

```bash
sudo nano /etc/apache2/httpd.conf
```

Atrodiet šo rindu un noņemiet sākumā esošo `#`, lai to atkomentētu:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obligāti: atļaut .htaccess pārrakstīšanu

Tajā pašā failā atrodiet bloku `<Directory "/Library/WebServer/Documents">` un nomainiet:

```apache
AllowOverride None
```

uz:

```apache
AllowOverride All
```

#### Obligāti: MIME tips Markdown failiem

Joprojām failā `httpd.conf` pievienojiet šādu rindu, lai Markdown faili tiktu servēti pareizi:

```apache
AddType text/markdown .md
```

!!! warning "Svarīgi"

    Bez šī iestatījuma `.md` faili var netikt pareizi servēti.

#### Piemērot konfigurāciju

Pārbaudiet, vai konfigurācijā nav sintakses kļūdu, un pēc tam restartējiet Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Sākotnējā instalācija {: #initial-installation }

### 1. solis: Iestatīt digna repozitoriju

digna repozitorijs glabā visas ar digna aprēķinātās metrikas. Tas darbojas kā centrālā datubāze analītiskajiem un veiktspējas datiem.

#### Izveidot repozitorija shēmu un lietotāju

Atveriet savu PostgreSQL klientu (psql, pgAdmin vai līdzīgu) un izpildiet šādas SQL komandas:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Aizvietojiet šādus aizstājējvārdus:**

- `<digna_repo_schema>` — Vēlamais shēmas nosaukums (piem., `dignarepo`)
- `<digna_repo_user>` — Vēlamais lietotājvārds (piem., `digna_user`)
- `<digna_repo_password>` — Droša parole šim lietotājam

**Piemērs:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Lai tās palaistu no Terminal vienā solī:

```bash
psql postgres
```

Pēc tam ielīmējiet priekšrakstus uzvednē `postgres=#` un ierakstiet `\q`, lai izietu.

!!! tip "Laba prakse"

    Lietojiet stipras, sarežģītas paroles datubāzes lietotājiem. Izvairieties no viegli uzminamiem akreditācijas datiem.

---

### 2. solis: Izpakot digna instalācijas pakotni

1. Atrodiet jums nodoto digna instalācijas ZIP failu
2. Izpakojiet to vēlamajā instalācijas vietā — piemēram, `/opt/digna` vai `~/digna`
3. Pēc izpakošanas jums jāredz sekojošas vienības:
   - `dashboard/` — tīmekļa paneļa saskarne
   - `digna` — galvenais izpildāmais fails (backend + CLI apvienots)

!!! info "Konfigurācijas un licences faili pakotnē nav iekļauti"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` instalācijā nav iekļauts — abus jūs
    izveidojat paši sadaļās [Backend konfigurācija](#backend-configuration) un
    [Paneļa konfigurācija](#dashboard-configuration). Arī `license.toml` nav iekļauts;
    digna to nodrošina atsevišķi, kā aprakstīts 3. solī.

Lai izpakotu no Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Padarīt failu izpildāmu

Atkarībā no tā, kā arhīvs tika pārsūtīts, izpildes bits izpakošanas laikā var netikt saglabāts. Iestatiet to skaidri:

```bash
cd /opt/digna
chmod +x digna
```

#### Ja macOS bloķē lietojumprogrammu

Faili, kas lejupielādēti ar pārlūkprogrammu vai e-pasta klientu, tiek marķēti ar karantīnas atribūtu. Ja macOS ziņo, ka lietotni *"cannot be opened because the developer cannot be verified"*, noņemiet atribūtu no instalācijas direktorijas:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Vai arī atveriet **System Settings → Privacy & Security**, atrodiet bloķēto vienumu lapas apakšā un noklikšķiniet **Open Anyway**.

!!! note "Piezīme"

    Šis solis ir nepieciešams tikai tad, ja macOS patiešām bloķē izpildāmo failu. Pakotnes, kas pārsūtītas caur SSH vai no iekšējiem failu koplietojumiem, parasti netiek ievietotas karantīnā.

### 3. solis: Instalēt licences failu

!!! warning "Svarīgi"

    Licences fails **nav** iekļauts instalācijas paketē un tiks nodrošināts atsevišķi no digna.

1. Atrodiet jums nodoto `license.toml` failu
2. Kopējiet to uz digna instalācijas saknes direktoriju (tur, kur atrodas `config.toml` un izpildāmais `digna`)

**Kāpēc tas ir svarīgi:**
Licences fails satur jūsu klienta informāciju, licences derīguma termiņu un digitālo parakstu. **Nemainiet šo failu** — jebkuras izmaiņas to inaktivizēs.

**Direktorijas struktūra pēc iestatīšanas:**

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

## Backend konfigurācija {: #backend-configuration }

### 1. solis: Izveidot un rediģēt konfigurācijas failu

`config_template.toml` fails ir iekļauts jūsu digna instalācijas direktorijā. Pietiek to pārdēvēt par `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Atrašanās vieta:** `/opt/digna/config.toml`

Atveriet `config.toml` teksta redaktorā un konfigurējiet katru sadaļu zemāk.

#### [app] sadaļa

Šī sadaļa konfigurē starpizcelsmju resursu koplietošanu (CORS) starp paneli un backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Paneļa URL | URL, no kuriem tiek pasniegts panelis. Pārlūkprogrammas pieprasījumi no jebkuras citas izcelsmes tiek noraidīti |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obligāts, lai pārlūkprogramma ar katru pieprasījumu nosūtītu sesijas sīkfailu |

!!! note "Piezīme"

    Ja panelis tiek servēts no Homebrew nginx tā noklusējuma portā, atļaujamā izcelsme ir `http://localhost:8080`.

!!! info "[app] sadaļa nav obligāta"

    Sākot ar Release 2026.11, abas atslēgas un visu `[app]` sadaļu var izlaist. Tas ir pareizais iestatījums, ja apgrieztais starpniekserveris (reverse proxy) pasniedz paneli un backend ar vienu izcelsmi: tad pārlūkprogramma neveic starpizcelsmju pieprasījumus, un pēc noklusējuma neviens netiek atļauts.

#### [repo] sadaļa

Šī sadaļa konfigurē savienojumu ar PostgreSQL datubāzi:

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

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` vai IP | PostgreSQL servera hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (noklusējums) | PostgreSQL ports |
| `DIGNA_REPO_DB` | `postgres` | Datubāzes nosaukums |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Iepriekš izveidotā shēma |
| `DIGNA_REPO_USER` | `digna_user` | Lietotājs izveidots PostgreSQL iestatīšanā |
| `DIGNA_REPO_PASSWORD` | Jūsu parole | Parole, iestatīta shēmas izveidē |
| `DIGNA_REPO_SSLMODE` | `prefer` (noklusējums) | Neobligāts. PostgreSQL SSL režīms: `disable`, `allow`, `prefer`, `require`, `verify-ca` vai `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (noklusējums) | Neobligāts. Savienojumu skaits, ko digna uztur atvērtus ar repozitoriju |

#### [base] sadaļa

Šī sadaļa satur drošības, sīkfailu un inspekciju iestatījumus:

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

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_FERNET_KEY` | Iepriekš parādītā vērtība | Iepriekšējo laidienu izmantotās šifrēšanas atslēga. Tai jābūt norādītai; saglabājiet parādīto vērtību |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Resursdators, kurā panelis ir sasniedzams. `""` neiestata domēnu, kas ir pareizi aiz starpniekservera, kurš pasniedz paneli un backend ar vienu izcelsmi |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Jābūt `true` vienmēr, kad digna tiek pasniegta caur HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Neļauj skriptiem piekļūt sesijas sīkfailam |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 stundas) | Sesijas derīguma laiks sekundēs |
| `DIGNA_MAX_WORKERS` | Skaitlis: CPU kodolu skaits - 1 | Inspekciju skaits, kas drīkst darboties vienlaikus |
| `DIGNA_FRONTEND_BASEURL` | Paneļa URL | Obligāts. Tiek izmantots saitēm paziņojumu ziņojumos, tāpēc tam jābūt URL, ko adresāti var atvērt |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (noklusējums) | Neobligāts. Sekundes, cik ilgi viens vaicājums avota datubāzē drīkst darboties, pirms tas tiek pārtraukts; `0` atslēdz noildzi |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (noklusējums) | Neobligāts. Sekundes, cik ilgi gaidīt savienojumu ar avota datubāzi; `0` gaida bez ierobežojuma |

!!! tip "Padoms"

    Lai uzzinātu, cik CPU kodolu ir pieejami jūsu Mac datorā, palaidiet `sysctl -n hw.ncpu`.

#### [encryption] sadaļa

Šajā sadaļā ir atslēga, ar kuru tiek šifrētas repozitorijā glabātās sensitīvās vērtības. Tā ir **obligāta** — `config check` ziņo par sadaļu `[encryption]` kā FAILED, ja atslēgas trūkst.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 kodēta atslēga | Šifrē sensitīvās vērtības, kas glabājas digna repozitorijā |

!!! warning "Aizsargājiet config.toml"

    Šī atslēga ir fiksēta vērtība, kas ir vienāda visās digna instalācijās, un tieši tā atkodē jūsu repozitorija sensitīvās vērtības. Ierobežojiet piekļuvi `config.toml` līdz kontam, ar kuru darbojas digna, glabājiet failu ārpus versiju kontroles un koplietojamiem diskiem un izslēdziet to no jebkuras dublējuma kopijas, kas tiek glabāta mazāk droši nekā pats repozitorijs.

#### [logging] sadaļa

Šī sadaļa konfigurē žurnālu (logu) uzvedību:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` vai `DEBUG` | `INFO` produkcijai, `DEBUG` problēmu novēršanai. Tiek pieņemti arī `TRACE`, `WARN` un `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (noklusējums) | Neobligāts. Direktorija rotējošajiem žurnālfailiem, relatīvi pret darba direktoriju |
| `DIGNA_LOGGING_MAX_FILES` | `30` (noklusējums) | Neobligāts. Saglabājamo rotēto žurnālfailu skaits |

#### [duckdb] sadaļa (neobligāta) {: #duckdb-section }

Jaunums Release 2026.11. Šī sadaļa nosaka **digna Engine** resursus. digna Engine profilē datus pašā digna tiem datubāzes savienojumiem, kuru profilēšanas vieta ir **digna Engine**, un veic referenciālās integritātes pārbaudes starp datu avotiem dažādos datubāzes savienojumos. Skatiet [Profilēšanas vieta](../../../platform/profiling/profiling_location.md).

Sadaļa nav obligāta. Bez tās tiek lietotas tālāk norādītās noklusējuma vērtības.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (noklusējums) | Atmiņa MB, ko drīkst izmantot viena digna Engine izpilde. Vienlaikus var būt aktīvas līdz `DIGNA_MAX_WORKERS` izpildēm |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Noklusējums: sistēmas pagaidu direktorija (tā konta `$TMPDIR`, ar kuru darbojas digna) | Direktorija pagaidu failiem, ja dati neietilpst atmiņā |

!!! tip "digna Engine izmēra plānošana"

    Paredziet digna resursdatorā līdz `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` atmiņas papildus tai, ko izmanto pati digna, un pagaidu direktorijā pietiekami daudz brīvas diska vietas, lai tajā ietilptu lielākais inspicētais datums no datu avotiem, kas izmanto digna Engine. Norādiet `DIGNA_DUCKDB_TEMP_DIRECTORY` uz disku ar šādu brīvu vietu, kurā var rakstīt konts, ar kuru darbojas digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Šī sadaļa jums ir vajadzīga tikai tad, ja vismaz viens datubāzes savienojums izmanto digna Engine vai ja referenciālās integritātes pārbaude salīdzina datu avotus dažādos savienojumos.

---

### 2. solis: Pārbaudiet konfigurāciju

Pirms repozitorija inicializēšanas pārbaudiet, vai `config.toml` ir pilnīgs un pareizi veidots. Savā digna instalācijas direktorijā palaidiet:

```bash
./digna config check
```

Katra sadaļa tiek pārbaudīta atsevišķi, tāpēc viena kļūda neaizsedz pārējo stāvokli:

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

Izlabojiet visu, kas ziņots kā FAILED, un pirms turpināšanas palaidiet komandu vēlreiz. WARNING sadaļā **Unknown keys** uzskaita atslēgas failā `config.toml`, kuras digna nenolasa; tām nav nekādas ietekmes, tāpēc noņemiet tās vai izlabojiet to rakstību. Pilns opciju saraksts ir [CLI atsaucē](../../../cli/Command_Line_Interface_202611.md).

### 3. solis: Inicializēt repozitoriju

1. Atveriet **Terminal**
2. Pārejiet uz jūsu digna instalācijas direktoriju (tur, kur atrodas `config.toml` un izpildāmais `digna`)
3. Palaidiet savienojuma pārbaudi:

```bash
cd /opt/digna
./digna repo check
```

Jaunā shēmā komanda izveido savienojumu un pēc tam ziņo, ka repozitorijs vēl nav instalēts:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Šajā brīdī tas ir sagaidāmais rezultāts: tas apstiprina, ka digna sasniedz PostgreSQL un shēmu. Savukārt savienojuma vai autentifikācijas kļūda norāda uz `[repo]` sadaļu vai PostgreSQL iestatīšanu.

!!! note "Piezīme"

    macOS sistēmā pašreizējās direktorijas komandas nav iekļautas PATH, tāpēc izpildāmais fails tiek izsaukts kā `./digna`, nevis `digna`. Lai visur izmantotu īsāko formu, pievienojiet instalācijas direktoriju savam PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 4. solis: Instalēt repozitorija shēmu

Tajā pašā direktorijā palaidiet:

```bash
./digna repo upgrade
```

Šī komanda instalē nepieciešamās tabulas repozitorija shēmā un beidzas ar:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instalē un jaunina"

    Sākot ar Release 2026.11, `repo upgrade` instalē jaunu repozitoriju un jaunina esošu. `repo install` joprojām darbojas kā tās pašas komandas cits nosaukums.

### 5. solis: Izveidot administratora lietotāju

Administratora lietotājs tiek izveidots tieši repozitorija shēmā, tāpēc serverim vēl nav jādarbojas. digna instalācijas direktorijā palaidiet:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Piemērs:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Šī komanda izveido lietotāju ar e-pasta adresi `admin@example.com` un pilnām administratīvām tiesībām.

!!! tip "Padoms"

    Ietveriet paroli vienpēdiņās. `zsh` tādas rakstzīmes kā `!`, `$` un `*` apstrādā īpaši, un parole bez pēdiņām, kas tās satur, netiks nodota tieši tā, kā ierakstīta.

!!! tip "Laba prakse"

    Izmantojiet stipru paroli ar lielajiem un maziem burtiem, cipariem un speciālajām zīmēm.

### 6. solis: Palaist digna serveri

digna instalācijas direktorijā palaidiet serveri ar:

```bash
./digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — servera hostname/IP (noklusējums `127.0.0.1`)
- `--port` — servera ports (noklusējums `8000`)

Kad serveris ir palaists, tas izvada adresi, kurā tas klausās:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Padoms"

    Pirmo reizi palaižot serveri, macOS var jautāt, vai vēlaties, lai lietojumprogramma pieņemtu ienākošos tīkla savienojumus. Noklikšķiniet **Allow**, citādi panelis nevarēs sasniegt backend.

!!! note "Serveris aizņem termināli"

    `serve` darbojas priekšplānā un turpina, līdz to apturat ar ++ctrl+c++. Atstājiet to darbojamies, kamēr pabeidzat iestatīšanu; lai to automātiski palaistu sistēmas sāknēšanas laikā, skatiet [digna palaide kā fona serviss](#running-digna-as-a-background-service).

---

## Paneļa konfigurācija {: #dashboard-configuration }

### 1. solis: Izvietot paneli uz tīmekļa servera

digna panelis savu konfigurāciju nolasa no faila `dashboard/dashboard_config.toml`. Šis fails instalācijā nav iekļauts — jūs to izveidojat `dashboard/` direktorijā līdzās paneļa failiem.

Tā saturs ir aprakstīts sadaļā [Vienotā pieteikšanās (SSO)](../../../sso/overview.md), kur šis fails arī ir nepieciešams: tajā ir panelī piedāvātās pieteikšanās iespējas un, daudzinstanču izvietošanai, backend savienojums.

Izvēlieties jūsu tīmekļa serveri un izpildiet atbilstošos izvietošanas soļus.

#### Izvietošana uz nginx

Ja izpildījāt sadaļu [nginx iestatīšana](#nginx-setup), server bloks jau norāda uz jūsu `dashboard` mapi, un nekas nav jākopē.

1. **Pārbaudiet ceļu**
   - Atveriet `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Pārliecinieties, ka `root` norāda uz jūsu izpakoto `dashboard` mapi

2. **Nodrošiniet, ka mape ir nolasāma**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Pārlādējiet nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Pārbaudiet instalāciju**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost:8080` (vai jūsu konfigurēto URL)
   - Jums jāredz digna paneļa pieteikšanās lapa

#### Izvietošana uz Apache httpd

1. **Kopējiet paneli uz dokumentu sakni**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Pievienojiet pārrakstīšanas noteikumus**

   Izvietotajā mapē izveidojiet failu `.htaccess`, lai paneļa maršruti saglabātos pēc pārlūkprogrammas atsvaidzināšanas:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Ielīmējiet tālāk norādīto:

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

3. **Restartējiet Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Piekļūstiet panelim**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost/digna`
   - Jums jāredz digna paneļa pieteikšanās lapa

---

## digna palaide kā fona serviss {: #running-digna-as-a-background-service }

### Kāpēc darbināt digna kā servisu?

digna backend darbināšana kā fona serviss nodrošina, ka tas:

- Automātiski startējas, kad dators tiek sāknēts
- Darbojas fonā bez atvērta Terminal loga
- Automātiski restartējas, ja notiek avārija
- To var pārvaldīt ar `launchctl`, macOS servisu pārvaldnieku

### Servisa pārvaldības faili

Visi nepieciešamie faili atrodas digna instalācijas direktorijā zem: `bin/`

Pieejami šādi čaulas skripti:

- `install_service.sh` — reģistrē digna sistēmā launchd
- `uninstall_service.sh` — atreģistrē servisu
- `start_service.sh` — palaiž reģistrēto servisu
- `stop_service.sh` — aptur darbojošos servisu

!!! warning "Nepieciešamas administratīvās tiesības"

    Visi skripti jāizpilda ar `sudo`, jo servisa, kas startējas sāknēšanas laikā, reģistrēšana veic ierakstu direktorijā `/Library/LaunchDaemons`.

### Skriptu padarīšana izpildāmus

Izpakošana var nesaglabāt izpildes bitu. Pirms pirmās lietošanas:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Servisa instalēšana

1. **Atveriet Terminal**

2. **Pārejiet uz bin mapi**
   ```bash
   cd /opt/digna/bin
   ```

3. **Palaidiet instalācijas skriptu**
   ```bash
   sudo ./install_service.sh
   ```

digna serveris tagad ir reģistrēts sistēmā launchd ar **automātisku startēšanu**. Serviss netiek palaists uzreiz — skatiet nākamo sadaļu, lai to palaistu.

### Servisa palaišana un apturēšana

#### Lai palaistu servisu

1. Atveriet Terminal
2. Pārejiet uz `/opt/digna/bin`
3. Palaidiet:
   ```bash
   sudo ./start_service.sh
   ```

#### Lai apturētu servisu

1. Atveriet Terminal
2. Pārejiet uz `/opt/digna/bin`
3. Palaidiet:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Padoms"

    Vienmēr apturiet servisu, pirms atjaunināt lietojumprogrammas failus.

### Servisa pārbaude

Lai pārliecinātos, ka serviss ir reģistrēts un darbojas:

```bash
sudo launchctl list | grep digna
```

Rinda, kas sākas ar procesa ID, norāda, ka serviss darbojas. `-` pirmajā kolonnā nozīmē, ka tas ir reģistrēts, bet apturēts.

### Pārvietot servisu uz jaunu direktoriju

launchd glabā absolūto ceļu līdz izpildāmajam failam, tāpēc instalācijas pārvietošanai serviss ir jāreģistrē no jauna:

1. **Atinstalēt esošo servisu**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Pārvietot aplikācijas failus**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Pārinstalēt servisu**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Palaist servisu**
   ```bash
   sudo ./start_service.sh
   ```

### Servisa atinstalēšana

1. **Apturēt darbojošos servisu**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Atinstalēt servisu**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna serveris tagad vairs nav reģistrēts sistēmā launchd.

---

## Jaunināšana uz jaunu izlaidumu {: #upgrading-to-a-new-release }

Šajā sadaļā aprakstīts, kā atjaunināt Release 2026.06 instalāciju uz Release 2026.11.

!!! warning "Atjaunināšana no versijas, kas vecāka par 2026.06"

    Vispirms izpildiet Release 2026.06 atjaunināšanas darbības: [Jaunināšana uz jaunu izlaidumu](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Pēc tam turpiniet ar tālāk norādītajām darbībām.

### Pirms jaunināšanas

**digna repozitorija rezerves kopijas izveide ir obligāta**

Pirms digna jaunināšanas veiciet rezerves kopiju sava repozitorija (PostgreSQL), lai izvairītos no datu zuduma. Rezerves kopija nodrošina atjaunošanas iespēju, ja jaunināšanas laikā rodas neparedzētas problēmas.

Lai izveidotu rezerves kopiju no Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Licences faila pieprasīšana Release 2026.11**

Release 2026.11 nepieciešams jauns `license.toml`. Pieprasiet to digna komandai pirms darba sākšanas un sagatavojiet to [7. solim](#step-7-replace-the-license-file).

### Jaunināšanas process

#### 1. solis: Apturēt digna servisu {: #step-1-stop-the-digna-service }

Ja digna darbojas kā fona serviss, vispirms to apturiet:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Ja digna darbojas priekšplānā, tā Terminal logā nospiediet ++ctrl+c++.

#### 2. solis: Izveidojiet pašreizējās instalācijas dublējumu {: #step-2-backup-current-installation }

Savā digna instalācijas direktorijā pārdēvējiet pašreizējās instalācijas izpildāmo failu un paneļa mapi, lai jauno laidienu varētu izvietot tiem līdzās:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Saglabājiet `digna_old`, līdz esat pārbaudījis jaunināšanu, un `dashboard_old`, līdz esat no tās atjaunojis savus konfigurācijas failus (skatiet 4. soli). Pēc tam abus varat izdzēst.

#### 3. solis: Izpakot un izvietot jauno versiju {: #step-3-extract-and-deploy-new-version }

1. Izpakojiet jauno digna instalācijas ZIP failu
2. Kopējiet jauno `digna` izpildāmo failu un `dashboard` mapi uz jūsu instalācijas direktoriju
3. Atjaunojiet izpildes bitu un, ja nepieciešams, noņemiet karantīnas atribūtu:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Svarīgi"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` nekad netiek iekļauts instalācijas ZIP — digna komanda nekad nepiegādā nevienu no šiem failiem. Tāpēc jaunināšana jūsu esošo konfigurāciju neskar, un kopijas pārdēvētajās `*_old` mapēs ir vienīgās, kas jums ir.

#### 4. solis: Atjaunot jūsu konfigurācijas failus {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 neprasa izmaiņas failā `config.toml`: fails, kas darbojas ar Release 2026.06, turpina darboties. Divas izmaiņas nav obligātas:

- Pievienojiet [`[duckdb]` sadaļu](#duckdb-section), ja datubāzes savienojumiem jāizmanto digna Engine un tās noklusējuma vērtības neder jūsu resursdatoram.
- Izlaidiet `[app]` sadaļu, ja apgrieztais starpniekserveris pasniedz paneli un backend ar vienu izcelsmi.

!!! warning "Iestatījumi, kurus digna nenolasa"

    Agrākās šī ceļveža versijās bija parādīti daži iestatījumi, kurus digna nenolasa. Tiem nav nekādas ietekmes, un `config check` 6. solī tos uzskaita sadaļā **Unknown keys**. Noņemiet vai izlabojiet tos:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`, `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` un `digna_LOGGING_BACKUP_COUNT` nepastāv. Noņemiet tos.
    - Iestatījumu nosaukumi ir reģistrjutīgi. digna nolasa `DIGNA_REPO_HOST`, nevis `digna_REPO_HOST`. Rakstiet katru nosaukumu ar lielajiem burtiem, kā sadaļā [Backend konfigurācija](#backend-configuration).

!!! warning "Vienotā pieteikšanās: saglabājiet [[oidc_clients]]"

    digna nolasa vienotās pieteikšanās nodrošinātājus kā `[[oidc_clients]]` ierakstu sarakstu, katru ar savu `DIGNA_OIDC_KEY`. Ja esat pārveidojis savus nodrošinātājus par `[oidc_clients.<key>]` sadaļām, kā bija parādīts agrākā šī ceļveža versijā, mainiet tos atpakaļ. Kamēr šī forma ir spēkā, `config check` ziņo par `OIDC config(s)` kā FAILED:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Atkārtojiet ierakstu katram nodrošinātājam un saglabājiet katru `DIGNA_OIDC_KEY` tādu pašu kā `key` failā `dashboard_config.toml`. Tas skar tikai instalācijas, kas izmanto vienoto pieteikšanos.

#### 5. solis: Pārlādēt tīmekļa serveri {: #step-5-reload-the-web-server }

Panelis ir statisku failu kopums, tāpēc jūsu tīmekļa serveris — un pārlūkprogramma — joprojām var pasniegt iepriekšējo versiju. Pārlādējiet vai restartējiet tīmekļa serveri, kurā mitināta mape `dashboard`, un pēc tam pārlādējiet lapu ar pilnu atsvaidzināšanu (++cmd+shift+r++).

#### 6. solis: Pārbaudiet konfigurāciju {: #step-6-validate-the-configuration }

Pirms pieskarties repozitorijam, pārliecinieties, ka `config.toml` ir pilnīgs:

```bash
./digna config check
```

Katrai sadaļai jāziņo OK. Izlabojiet visu, kas ziņots kā FAILED, noņemiet atslēgas, kas uzskaitītas sadaļā **Unknown keys**, un pirms turpināšanas palaidiet komandu vēlreiz.

#### 7. solis: Aizstāt licences failu {: #step-7-replace-the-license-file }

Licences fails parasti tiek pārnests no viena laidiena uz nākamo. Release 2026.11 ir izņēmums: tas pievieno divus licencējamus moduļus, digna Data Reconciliation un digna Agentic, un licence, kas izsniegta pirms 2026.11, tos nesatur. Nokopējiet `license.toml`, ko digna komanda nodrošināja Release 2026.11, instalācijas direktorijā, aizstājot veco:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nepaturiet iepriekšējo licenci"

    Ar iepriekšējo licenci digna joprojām startē, bet digna Data Reconciliation un digna MCP Server paliek izslēgti. Katra komanda, kas pārbauda licenci — `user`, `inspection`, `repo` —, tiek pārtraukta pirms pieskaršanās repozitorijam, ja pārbaude neizdodas. Pirms turpināt, pārbaudiet jauno licenci:

    ```bash
    ./digna license check
    ```

#### 8. solis: Jaunināt repozitorija shēmu {: #step-8-upgrade-the-repository-schema }

Savā digna instalācijas direktorijā palaidiet:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 pārvalda repozitorija shēmu ar versionētām migrācijām. Pirmā jaunināšana no agrāka laidiena atjaunina shēmu līdz iepriekšējā versiju mehānisma pēdējai versijai, reģistrē to kā sākumpunktu un pēc tam piemēro Release 2026.11 migrācijas. Tā beidzas ar:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Visi esošie dati tiek saglabāti. Lai jebkurā brīdī redzētu repozitorija stāvokli, palaidiet `./digna repo check`: tā parāda pēdējo piemēroto migrāciju un visas vēl nepiemērotās migrācijas.

!!! warning "digna nestartē ar novecojušu repozitoriju"

    Sākot ar Release 2026.11, serveris atsakās startēt, kamēr repozitorijs ir jājaunina, un par to ziņo, piemēram:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Pirms servera vai servisa palaišanas palaidiet `repo upgrade`.

#### 9. solis: Restartēt servisus {: #step-9-restart-services }

Ja darbināt kā fona servisu:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Ja darbināt manuāli, restartējiet serveri:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Ja izmantojat nginx vai Apache, restartējiet attiecīgo tīmekļa serveri:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### 10. solis: Pārbaudīt jaunināšanu {: #step-10-verify-the-upgrade }

1. Pārbaudiet jaunā izpildāmā faila laidienu:

    ```bash
    ./digna version
    ```

    Pirmajai rindai jābūt `Release: 2026.11`.

2. Piekļūstiet digna panelim un pārbaudiet, vai saskarne ielādējas pareizi.
3. Pārskatiet servera izvadi un failus direktorijā `logs`, vai nav kļūdu.
4. Pārbaudiet savus datubāzes savienojumus — skatiet [Savienojuma pārbaude](../../../databases/overview.md#testing-a-connection). Pēc jaunināšanas no laidiena, kas vecāks par 2026.06, vispirms pārceliet uz ODBC katru savienojumu, kas vēl neizmantoja ODBC.

Lai sāktu darbu ar jaunajiem moduļiem, skatiet [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [AI aģenta pievienošana](../../../platform/agentic/connect_ai_agent.md) par digna MCP Server un [Profilēšanas vieta](../../../platform/profiling/profiling_location.md) par digna Engine.
