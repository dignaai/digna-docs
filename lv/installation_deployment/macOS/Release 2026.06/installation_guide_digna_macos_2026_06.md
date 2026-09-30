# macOS instalācijas ceļvedis digna Release 2026.06

**Izlaidums:** 2026.06

**Pēdējais atjauninājums:** 2026. gada 5. septembris


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

### Kas jauns izlaidumā 2026.06

Šajā izlaidumā datu novērošanas iespējas ir integrētas tieši jūsu kodā, ļaujot izstrādātājiem uzraudzīt datu kvalitāti pie avota. Pilnas detaļas skatiet [izlaiduma piezīmēs](http://docs.digna.ai/changelog/Release_202606/).

### Meklējat Windows vai Linux?

Šis ceļvedis attiecas uz macOS. Citu platformu instalācijas skaidrojumu skatiet [Windows instalācijas ceļvedī](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) vai [Linux instalācijas ceļvedī](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
unzip digna-2026.06-macos.zip -d /opt/digna
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

Šī sadaļa konfigurē digna backend lietojumprogrammas iestatījumus:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontenda URL | Ja panelis atrodas citā serverī, iekļaujiet tā URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nepieciešams CORS ar akreditācijas datiem |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Atļaut visus HTTP metodus |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Atļaut visus header laukus |

!!! note "Piezīme"

    Ja panelis tiek servēts no Homebrew nginx tā noklusējuma portā, atļaujamā izcelsme ir `http://localhost:8080`.

#### [repo] sadaļa

Šī sadaļa konfigurē savienojumu ar PostgreSQL datubāzi:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` vai IP | PostgreSQL servera hostname/IP |
| `digna_REPO_PORT` | `5432` (noklusējums) | PostgreSQL ports |
| `digna_REPO_DB` | `postgres` | Datubāzes nosaukums |
| `digna_REPO_SCHEMA` | `dignarepo` | Iepriekš izveidotā shēma |
| `digna_REPO_USER` | `digna_user` | Lietotājs izveidots PostgreSQL iestatīšanā |
| `digna_REPO_PASSWORD` | Jūsu parole | Parole, iestatīta shēmas izveidē |

#### [base] sadaļa

Šī sadaļa satur drošības un sīkfailu iestatījumus:

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

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Atbilst jūsu frontenda domēnam |
| `digna_COOKIE_SECURE` | `false` (lokāli) / `true` (produkcijā) | Lietojiet `true` HTTPS savienojumiem |
| `digna_COOKIE_HTTPONLY` | `true` | Vienmēr iespējots drošībai |
| `digna_COOKIE_SAME_SITE` | `lax` | Novērš CSRF uzbrukumus |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 stundas) | Sesijas derīguma laiks sekundēs |
| `digna_MAX_WORKERS` | Skaitlis: CPU kodolu skaits - 1 | Paralēlo inspekciju uzdevumu skaits |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maksimālā aizture sekundēs, ko plānotājs drīkst pievienot pirms termiņā esoša darba sākšanas |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Diennakts laiks (24 stundu formāts `HH:MM`), kad sākas ikdienas tīrīšana |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` vai `DEBUG` | `INFO` produkcijai, `DEBUG` problēmu novēršanai |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Cik dienu žurnālu dublējumu saglabāt |

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

Overall: OK
```

Izlabojiet visu, kas ziņots kā FAILED, un pirms turpināšanas palaidiet komandu vēlreiz. Pilns opciju saraksts ir [CLI atsaucē](../../../cli/Command_Line_Interface_202606.md).

### 3. solis: Inicializēt repozitoriju

1. Atveriet **Terminal**
2. Pārejiet uz jūsu digna instalācijas direktoriju (tur, kur atrodas `config.toml` un izpildāmais `digna`)
3. Palaidiet savienojuma pārbaudi:

```bash
cd /opt/digna
./digna repo check
```

Jums jāsaņem apstiprinājums, ka savienojums ir izveidots (repozitorijs pats par sevi vēl nav inicializēts).

!!! note "Piezīme"

    macOS sistēmā pašreizējās direktorijas komandas nav iekļautas PATH, tāpēc izpildāmais fails tiek izsaukts kā `./digna`, nevis `digna`. Lai visur izmantotu īsāko formu, pievienojiet instalācijas direktoriju savam PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 4. solis: Instalēt repozitorija shēmu

Tajā pašā direktorijā palaidiet:

```bash
./digna repo install
```

Šī komanda instalē nepieciešamās tabulas un shēmu jūsu PostgreSQL datubāzē.

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
- `--address` — servera hostname/IP
- `--port` — servera ports

Jums jāredz startēšanas ziņas, kas apstiprina, ka serveris darbojas:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
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

### Pirms jaunināšanas

**Vispirms pārbaudiet visus datubāžu savienojumus**

Sākot ar laidienu 2026.06, digna katru avota tehnoloģiju sasniedz caur **ODBC**. Iepriekšējie laidieni piedāvāja izvēli starp katrai tehnoloģijai pašu draiveri un ODBC, ko izvēlējās ar slēdzi **Use ODBC**. digna komanda nolēma balstīties tikai uz ODBC, jo viena standarta saskarne sniedz vairāk nekā pēc pasūtījuma veidotu draiveru kopums:

- **Autentifikācija** — autentifikācija ir daļa no ODBC, tāpēc savienojums var izmantot visu, ko atbalsta tā draiveris: paroles, pilnvaras un PAT, Kerberos un Active Directory, MFA un pārlūkprogrammas vienoto pieteikšanos, mākoņa identitātes, klienta sertifikātus un TLS. Jaunas metodes nāk līdzi draivera atjauninājumam, nevis gaidot digna laidienu.
- **Draiveri, ko uztur datubāžu ražotāji** — ražotāja draiveris seko jaunām servera versijām un drošības labojumiem, un jūs varat to atjaunināt pēc sava grafika, neatkarīgi no digna.
- **Viens veids, kā konfigurēt visu** — katra tehnoloģija ir atslēgu un vērtību īpašību saraksts ar to pašu saskarni, to pašu sensitīvo vērtību šifrēšanu un to pašu problēmu novēršanu, nevis atšķirīgu lauku kopu katram avotam.
- **Pielāgošana un aptvērums** — draivera opcijas, piemēram, noildzes, TLS iestatījumi, starpniekserveri un ielādes izmēri, ir pieejamas katram avotam, un pievienot var jebkuru tehnoloģiju ar atbilstošu ODBC draiveri, arī tādu, kurai digna nepublicē atsevišķu rokasgrāmatu.

Praksē tas nozīmē, ka slēdzis **Use ODBC** un atsevišķie resursdatora, porta, datubāzes, lietotāja un paroles lauki vairs nepastāv. **Katrs savienojums, kas vēl neizmanto ODBC, ir jāpārceļ uz ODBC** — automātiskas konvertēšanas nav, tāpēc ieplānojiet to pirms jaunināšanas:

1. Pārskatiet katru jūsu instalācijā definēto datubāzes savienojumu un atzīmējiet tos, kas vēl neizmanto ODBC — katrs no tiem būs jākonfigurē no jauna.
2. Instalējiet atbilstošo ODBC draiveri digna resursdatorā — savienojumi tiek atvērti no servera, kurā darbojas digna backend, nevis no pārlūkprogrammas. Skatiet
   [ODBC draivera instalēšana digna resursdatorā](../../../databases/overview.md#install-the-driver).
3. Sagatavojiet ODBC īpašības katram skartajam savienojumam.
   [Tehnoloģiju rokasgrāmatas](../../../databases/overview.md#technology-guides) katram avotam norāda pārbaudītu īpašību kopu.

Pēc jaunināšanas katru skarto savienojumu pārceliet uz ODBC un pārbaudiet to no paneļa — skatiet
[Datubāzes savienojuma izveide](../../../databases/overview.md#create-a-database-connection)
un [Savienojuma pārbaude](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy savienojumi"

    Databricks Legacy savienotājs šajā laidienā ir noņemts. Pārceliet šos savienojumus uz [Databricks](../../../databases/databricks_connector_guide.md) savienotāju.

**digna repozitorija rezerves kopijas izveide ir obligāta**

Pirms digna jaunināšanas veiciet rezerves kopiju sava repozitorija (PostgreSQL), lai izvairītos no datu zuduma.
Rezerves kopija nodrošina atjaunošanas iespēju, ja jaunināšanas laikā rodas neparedzētas problēmas.

Lai izveidotu rezerves kopiju no Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Jaunināšanas process

#### 1. solis: Apturēt digna servisu

Ja digna darbojas kā fona serviss, vispirms to apturiet:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Ja digna darbojas priekšplānā, tā Terminal logā nospiediet `Ctrl + C`.

#### 2. solis: Izveidojiet pašreizējās instalācijas dublējumu

Savā digna instalācijas direktorijā pārdēvējiet pašreizējās instalācijas mapes, lai jauno laidienu varētu izvietot tiem līdzās:

```bash
cd /opt/digna
mv dignabackend dignabackend_old
```
```bash
mv dignacli dignacli_old
```
```bash
mv dashboard dashboard_old
```

!!! info "dignabackend un dignacli vairs netiek izmantoti"

    Sākot ar laidienu 2026.06, `dignabackend` un `dignacli` aizstāj viens izpildāmais fails `digna`, kas apvieno backend un CLI. Saglabājiet `dignabackend_old` un `dignacli_old` tikai līdz brīdim, kad esat pārbaudījis jauninājumu — pēc tam varat izdzēst abas mapes. Saglabājiet `dashboard_old`, līdz esat no tās atjaunojis savus konfigurācijas failus (skatiet 4. soli).

#### 3. solis: Izpakot un izvietot jauno versiju

1. Izpakojiet jauno digna instalācijas ZIP failu
2. Kopējiet jauno `digna` izpildāmo failu un `dashboard` mapi uz jūsu instalācijas direktoriju
3. Atjaunojiet izpildes bitu un, ja nepieciešams, noņemiet karantīnas atribūtu:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Svarīgi"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` nekad netiek iekļauts
    instalācijas ZIP — digna komanda nekad nepiegādā nevienu no šiem failiem. Tāpēc jaunināšana jūsu esošo
    konfigurāciju neskar, un kopijas pārdēvētajās `*_old` mapēs ir vienīgās, kas jums ir.

#### 4. solis: Atjaunot jūsu konfigurācijas failus

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Laidiens 2026.06 maina config.toml"

    Trīs iestatījumi ir jauni un obligāti, bet trīs vairs netiek izmantoti. No iepriekšējā laidiena pārņemtā `config.toml` nesatur jaunos iestatījumus, un digna nestartēs, kamēr to trūks. Pievienojiet savam esošajam `config.toml` šādu:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Pievienojiet divas `[base]` atslēgas savai esošajai `[base]` sadaļai un pievienojiet `[encryption]` kā jaunu sadaļu. Pēc tam noņemiet iestatījumus, kas vairs netiek izmantoti: **`digna_FERNET_KEY`** no `[base]`, kā arī **`digna_APP_HOST`** un **`digna_APP_PORT`** no `[app]` — adresi un portu serveris tagad iegūst no `digna serve`.

    Ko dara katrs iestatījums, aprakstīts sadaļā [Backend konfigurācija](#backend-configuration).

!!! warning "Vienotā pieteikšanās: [oidc_clients] formāts ir mainījies"

    Laidiens 2026.06 aizstāj tabulu masīvu ar vienu tabulu katram nodrošinātājam, nosauktu pēc
    nodrošinātāja atslēgas. `DIGNA_OIDC_KEY` vairs nav — atslēga tagad ir sadaļas virsraksta daļa.

    Pirms:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Pēc:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Atkārtojiet sadaļu katram nodrošinātājam un saglabājiet katru atslēgu tādu pašu kā `key` failā
    `dashboard_config.toml`. `digna config check` ziņo par `oidc_clients` kā FAILED, kamēr
    saglabājas vecā forma. Tas skar tikai instalācijas, kas izmanto vienoto pieteikšanos.

#### 5. solis: Pārlādēt tīmekļa serveri

Panelis ir statisku failu kopums, tāpēc jūsu tīmekļa serveris — un pārlūkprogramma — joprojām var
pasniegt iepriekšējo versiju. Pārlādējiet vai restartējiet tīmekļa serveri, kurā mitināta mape `dashboard`,
un pēc tam pārlādējiet lapu ar pilnu atsvaidzināšanu (++cmd+shift+r++).

#### 6. solis: Pārbaudiet konfigurāciju

Pirms pieskarties repozitorijam pārliecinieties, ka atjauninātais `config.toml` ir pilnīgs:

```bash
./digna config check
```

Katrai sadaļai jāziņo OK. Izlabojiet visu, kas ziņots kā FAILED, un pirms turpināšanas palaidiet komandu vēlreiz.

#### 7. solis: Aizstāt licences failu

Katram laidienam ir atsevišķa licence. Nokopējiet `license.toml`, ko digna komanda nodrošināja
šim laidienam, instalācijas direktorijā, aizstājot veco:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nepaturiet iepriekšējo licenci"

    Agrākam laidienam izsniegts `license.toml` neattiecas uz šo laidienu, un katra komanda,
    kas pārbauda licenci — `user`, `inspection`, `repo` —, tiek pārtraukta pirms pieskaršanās
    repozitorijam, ja pārbaude neizdodas. Pārbaudiet licenci, pirms turpināt:

    ```bash
    ./digna license check
    ```

#### 8. solis: Jaunināt repozitorija shēmu

Pārejiet uz jūsu digna instalācijas direktoriju un palaidiet:

```bash
cd /opt/digna
./digna repo upgrade
```

Tas atjauninās PostgreSQL shēmu uz jaunāko versiju, saglabājot visus esošos datus.

#### 9. solis: Restartēt servisus

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

#### 10. solis: Pārbaudīt jaunināšanu

1. Piekļūstiet digna panelim
2. Pārbaudiet, vai saskarne ielādējas pareizi
3. Pārskatiet servera žurnālus, vai nav kļūdu
4. Pārceliet uz ODBC katru savienojumu, kas vēl neizmantoja ODBC, un pēc tam pārbaudiet visus savienojumus
   — skatiet [Savienojuma pārbaude](../../../databases/overview.md#testing-a-connection)