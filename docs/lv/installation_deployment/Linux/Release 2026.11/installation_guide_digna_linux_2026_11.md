---
title: Linux instalācijas ceļvedis – digna Release 2026.11 | digna dokumentācija
description: Soli pa solim ceļvedis par digna Release 2026.11 uzstādīšanu Linux — sistēmas prasības, PostgreSQL iestatīšana, nginx vai Apache konfigurācija, backend un paneļa konfigurācija, digna darbība kā systemd serviss un jaunināšana no Release 2026.06.
keywords: digna Linux instalācija, digna izvietošanas ceļvedis, digna backend iestatīšana, digna paneļa instalācija, postgresql linux, nginx linux, digna systemd serviss, digna jaunināšanas ceļvedis
image: /assets/logo_square.png
---

# Linux instalācijas ceļvedis digna Release 2026.11

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
9. [digna palaide kā systemd serviss](#running-digna-as-a-systemd-service)
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

### Meklējat Windows vai macOS?

Šis ceļvedis attiecas uz Linux. Citu platformu instalācijas skaidrojumu skatiet [Windows instalācijas ceļvedī](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) vai [macOS instalācijas ceļvedī](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Kuras distribūcijas aptver šis ceļvedis?

Norādījumi ir sagatavoti divām izplatītākajām serveru saimēm. Kur tās atšķiras, ir dotas abas komandas:

- **Debian saime** — Debian, Ubuntu. Pakotņu pārvaldnieks: `apt`.
- **RHEL saime** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Pakotņu pārvaldnieks: `dnf`.

Darbosies jebkura mūsdienīga distribūcija ar `systemd`; mainās tikai pakotņu nosaukumi un daži konfigurācijas ceļi.

---

## Sistēmas prasības {: #system-requirements }

Pirms instalācijas pārliecinieties, ka jūsu sistēma atbilst šādām minimālajām prasībām:

| Prasība | Specifikācija |
|---|---|
| **Operētājsistēma** | Ubuntu 22.04 LTS vai jaunāka, Debian 12 vai jaunāka, RHEL 9 / Rocky 9 / AlmaLinux 9 vai jaunāka |
| **Arhitektūra** | x86_64 (amd64) vai arm64 |
| **Init sistēma** | systemd |
| **Atmiņa (minimālā konfigurācija)** | 16 GB RAM |
| **Diskā nepieciešamā vieta** | 10 GB brīvas vietas |
| **Datubāze** | PostgreSQL Server 12 vai jaunāks |
| **Tīmekļa serveris** | nginx, Apache httpd vai ekvivalents |

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

### Distribūcijas un arhitektūras noskaidrošana

Vairākas šī ceļveža komandas atšķiras Debian un RHEL saimei. Lai noskaidrotu, kuru izmantojat, palaidiet:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` vai `ID=debian` — izmantojiet `apt` komandas.
- `ID=rhel`, `rocky`, `almalinux` vai `fedora` — izmantojiet `dnf` komandas.
- `x86_64` vai `aarch64` — jums nepieciešamās instalācijas pakotnes arhitektūra.

---

## Priekšinstalācijas sagatavošana {: #pre-installation-setup }

Pirms digna instalēšanas pārliecinieties, ka ir izpildīti divi galvenie priekšnosacījumi:

1. **PostgreSQL Server** – aprēķināto metrikas un veiktspējas datu glabāšanai
2. **Tīmekļa serveris** – digna paneļa izvietošanai

Ja šīs sastāvdaļas vēl nav iestatītas, izpildiet tālāk norādītās sadaļas, lai tās instalētu un konfigurētu.

### Pakotņu indeksa atsvaidzināšana

Pirms jebko instalējat, atjauniniet pakotņu sarakstus:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Piezīme"

    Visā šajā ceļvedī pirmā komanda pārī ir paredzēta **Debian saimei**, bet otrā — **RHEL saimei**. Palaidiet tikai to, kas atbilst jūsu sistēmai.

---

## PostgreSQL servera iestatīšana {: #postgresql-server-setup }

### Ja PostgreSQL jau ir pieejams

Ja PostgreSQL jau ir instalēts un darbojas uz jūsu lokālā datora vai ja izmantojat pārvaldītu attālo PostgreSQL serveri, varat pāriet uz [nākamo sadaļu](#web-server-configuration).

### PostgreSQL instalēšana

#### 1. solis: Instalēt servera pakotni

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Padoms"

    Distribūciju pakotnes var atpalikt no aktuālā PostgreSQL laidiena. Ja jums nepieciešama konkrēta jaunāka versija, tā vietā izmantojiet oficiālo [PostgreSQL apt vai yum repozitoriju](https://www.postgresql.org/download/linux/).

#### 2. solis: Inicializēt datubāzes klasteri

**Debian saimē** pakotne izveido un palaiž klasteri automātiski — pārejiet uz nākamo soli.

**RHEL saimē** klasteris jāizveido skaidri:

```bash
sudo postgresql-setup --initdb
```

#### 3. solis: Palaist un iespējot servisu

```bash
sudo systemctl enable --now postgresql
```

Tas nekavējoties palaiž PostgreSQL un konfigurē to automātiski startēt atkal sistēmas sāknēšanas laikā.

#### 4. solis: Pārbaudīt instalāciju

```bash
psql --version
sudo systemctl status postgresql
```

Jums jāredz PostgreSQL versija un serviss stāvoklī `active (running)`.

#### 5. solis: Pieslēgties serverim

Linux PostgreSQL pakotne izveido sistēmas kontu `postgres`, kam pieder klasteris. Pieslēdzieties caur to:

```bash
sudo -u postgres psql
```

!!! note "Piezīme — šeit Linux atšķiras no Windows"

    Windows instalators iestatīšanas laikā lūdz iestatīt paroli superlietotājam `postgres`. Linux pakotnes to nedara. Tā vietā lokālie savienojumi tiek autentificēti ar **peer autentifikāciju**: operētājsistēmas lietotājam `postgres` ir atļauts pieslēgties kā datubāzes lietotājam `postgres` bez paroles.

    Tāpēc augstāk minētā komanda izmanto `sudo -u postgres`. digna backend pieslēdzas caur TCP ar lietotājvārdu un paroli, tāpēc sadaļā [Sākotnējā instalācija](#initial-installation) jūs izveidosiet atsevišķu digna lietotāju.

#### 6. solis: Pārbaudīt portu

Noklusējuma PostgreSQL ports ir `5432`. Lai pārbaudītu, kurā portā jūsu serveris klausās:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Pierakstiet šo vērtību — tā būs nepieciešama, konfigurējot digna backend.

#### 7. solis: Iespējot paroles autentifikāciju digna lietotājam

digna pieslēdzas PostgreSQL caur TCP kā `digna_user`, kam nepieciešama paroles autentifikācija, nevis peer autentifikācija. Pārbaudiet, vai jūsu `pg_hba.conf` to atļauj.

Atrodiet failu:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Atveriet to redaktorā un pārliecinieties, ka lokālajās TCP rindās tiek izmantots `scram-sha-256` (vai `md5` vecākos serveros), nevis `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Pēc jebkuras izmaiņas pārlādējiet PostgreSQL:

```bash
sudo systemctl reload postgresql
```

!!! warning "Svarīgi"

    Ja digna ziņo `FATAL: Ident authentication failed for user "digna_user"`, cēlonis ir šis iestatījums.

#### 8. solis: Ja PostgreSQL darbojas citā datorā

Lai pieņemtu savienojumus no cita resursdatora, iestatiet `listen_addresses` failā `postgresql.conf` un pievienojiet atbilstošu `host` rindu savam tīklam failā `pg_hba.conf`:

```
listen_addresses = '*'
```

Pēc tam atveriet portu ugunsmūrī un restartējiet servisu:

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

## Tīmekļa servera konfigurācija {: #web-server-configuration }

digna prasa tīmekļa serveri paneļa izvietošanai. Izvēlieties vienu no šīm iespējām:

- [nginx](#nginx-setup) — viegls un ieteicams
- [Apache httpd](#apache-setup) — plaši izmantota alternatīva

Nepieciešams instalēt un konfigurēt tikai **vienu** no šiem serveriem.

Abās sadaļās tiek konfigurētas divas lietas, no kurām panelis ir atkarīgs:

- **Vienas lapas lietotnes (SPA) rezerves maršruts**, lai paneļa URL atsvaidzināšana neatgrieztu 404
- **`.md` MIME tips**, lai Markdown faili tiktu servēti pareizi

### nginx iestatīšana {: #nginx-setup }

#### Pārskats

nginx ir viegls, augstas veiktspējas tīmekļa serveris, kas labi piemērots statiskā digna paneļa servēšanai.

#### Instalēšana

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx palaišana

```bash
sudo systemctl enable --now nginx
```

#### Pārbaudīt instalāciju

1. Atveriet pārlūkprogrammu
2. Dodieties uz `http://localhost`
3. Jums jāredz nginx sveiciena lapa

#### Ugunsmūra atvēršana

Ja serverim piekļūst no citiem datoriem, atļaujiet HTTP datplūsmu:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Vietnes konfigurēšana panelim

Abās distribūciju saimēs nginx iekļauj katru failu no savas `conf.d` direktorijas. Izveidojiet tur atsevišķu konfigurācijas failu digna vajadzībām:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Ielīmējiet tālāk norādīto, aizstājot `/opt/digna/dashboard` ar faktisko ceļu līdz izpakotajai `dashboard` mapei:

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

!!! warning "Svarīgi"

    Bez direktīvas `try_files` jebkuras paneļa lapas, izņemot saknes URL, pārlādēšana atgriež 404. Tas ir nginx ekvivalents URL Rewrite modulim, kas nepieciešams IIS operētājsistēmā Windows.

#### Atspējot noklusējuma vietni

Tikai viens server bloks drīkst būt `default_server` konkrētam portam. **Debian saimē** noņemiet pakotnes noklusējuma vietni, lai tā neradītu konfliktu:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

**RHEL saimē** aizkomentējiet vai izdzēsiet bloku `server { ... }` failā `/etc/nginx/nginx.conf`.

#### Piemērot konfigurāciju

Pārbaudiet, vai konfigurācijā nav sintakses kļūdu, un pēc tam pārlādējiet nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd iestatīšana {: #apache-setup }

#### Pārskats

Apache httpd ir pieejams katras atbalstītās distribūcijas noklusējuma repozitorijos. **Debian saimē** pakotne saucas `apache2`, bet **RHEL saimē** — `httpd`.

#### Instalēšana

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache palaišana

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Pārbaudīt instalāciju

1. Atveriet pārlūkprogrammu
2. Dodieties uz `http://localhost`
3. Jums jāredz distribūcijas noklusējuma Apache lapa

#### Obligāti: iespējot mod_rewrite

Panelim nepieciešama URL pārrakstīšana.

**Debian saimē** iespējojiet moduli un restartējiet:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

**RHEL saimē** `mod_rewrite` tiek ielādēts pēc noklusējuma. Pārliecinieties par to:

```bash
httpd -M | grep rewrite
```

#### Obligāti: atļaut .htaccess pārrakstīšanu

Atveriet savas dokumentu saknes konfigurācijas failu:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Atrodiet bloku `<Directory>`, kas aptver jūsu dokumentu sakni (abās saimēs `/var/www/html`), un nomainiet:

```apache
AllowOverride None
```

uz:

```apache
AllowOverride All
```

#### Obligāti: MIME tips Markdown failiem

Tajā pašā failā pievienojiet šādu rindu, lai Markdown faili tiktu servēti pareizi:

```apache
AddType text/markdown .md
```

!!! warning "Svarīgi"

    Bez šī iestatījuma `.md` faili var netikt pareizi servēti.

#### Piemērot konfigurāciju

Pārbaudiet, vai konfigurācijā nav sintakses kļūdu, un pēc tam restartējiet Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
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

Lai tās palaistu no čaulas vienā solī:

```bash
sudo -u postgres psql
```

Pēc tam ielīmējiet priekšrakstus uzvednē `postgres=#` un ierakstiet `\q`, lai izietu.

!!! tip "Laba prakse"

    Lietojiet stipras, sarežģītas paroles datubāzes lietotājiem. Izvairieties no viegli uzminamiem akreditācijas datiem.

---

### 2. solis: Izpakot digna instalācijas pakotni

1. Atrodiet jums nodoto digna instalācijas ZIP failu
2. Izpakojiet to vēlamajā instalācijas vietā — piemēram, `/opt/digna`
3. Pēc izpakošanas jums jāredz sekojošas vienības:
   - `dashboard/` — tīmekļa paneļa saskarne
   - `digna` — galvenais izpildāmais fails (backend + CLI apvienots)

!!! info "Konfigurācijas un licences faili pakotnē nav iekļauti"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` instalācijā nav iekļauts — abus jūs
    izveidojat paši sadaļās [Backend konfigurācija](#backend-configuration) un
    [Paneļa konfigurācija](#dashboard-configuration). Arī `license.toml` nav iekļauts;
    digna to nodrošina atsevišķi, kā aprakstīts 3. solī.

Lai izpakotu no čaulas:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Piezīme"

    Ja `unzip` nav instalēts, pievienojiet to ar `sudo apt install -y unzip` vai `sudo dnf install -y unzip`.

#### Padarīt failu izpildāmu

Atkarībā no tā, kā arhīvs tika pārsūtīts, izpildes bits izpakošanas laikā var netikt saglabāts. Iestatiet to skaidri:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Izveidot servisa kontu

Produkcijas izvietojumiem ieteicams darbināt backend ar atsevišķu lietotāju bez privilēģijām:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Piezīme"

    RHEL saimē atbilstošais čaulas ceļš ir `/sbin/nologin`.

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
sudo mv config_template.toml config.toml
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

    Ja panelis tiek servēts no nginx vai Apache noklusējuma HTTP portā, atļaujamā izcelsme ir `http://localhost` — vai servera publiskais URL, ja panelim piekļūst no citiem datoriem.

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

!!! tip "Laba prakse"

    `config.toml` satur datubāzes paroli atklātā tekstā. Ierobežojiet tā atļaujas, lai to varētu nolasīt tikai servisa konts:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    Lai uzzinātu, cik CPU kodolu ir pieejami jūsu serverī, palaidiet `nproc`.

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Noklusējums: sistēmas pagaidu direktorija (`$TMPDIR` vai `/tmp`, ja tas nav iestatīts) | Direktorija pagaidu failiem, ja dati neietilpst atmiņā |

!!! tip "digna Engine izmēra plānošana"

    Paredziet digna resursdatorā līdz `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` atmiņas papildus tai, ko izmanto pati digna, un pagaidu direktorijā pietiekami daudz brīvas diska vietas, lai tajā ietilptu lielākais inspicētais datums no datu avotiem, kas izmanto digna Engine. Norādiet `DIGNA_DUCKDB_TEMP_DIRECTORY` uz disku ar šādu brīvu vietu, kurā var rakstīt konts, ar kuru darbojas digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

1. Atveriet termināli
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

    Linux sistēmā pašreizējā direktorija nav iekļauta PATH, tāpēc izpildāmais fails tiek izsaukts kā `./digna`, nevis `digna`. Lai visur izmantotu īsāko formu, pievienojiet simbolisko saiti:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

    Ietveriet paroli vienpēdiņās. `bash` un `zsh` tādas rakstzīmes kā `!`, `$` un `*` apstrādā īpaši, un parole bez pēdiņām, kas tās satur, netiks nodota tieši tā, kā ierakstīta.

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

    Ja panelis tiek servēts no cita datora nekā backend, atveriet ugunsmūrī arī API portu:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Serveris aizņem termināli"

    `serve` darbojas priekšplānā un turpina, līdz to apturat ar ++ctrl+c++. Atstājiet to darbojamies, kamēr pabeidzat iestatīšanu; lai to automātiski palaistu sistēmas sāknēšanas laikā, skatiet [digna palaide kā systemd serviss](#running-digna-as-a-systemd-service).

---

## Paneļa konfigurācija {: #dashboard-configuration }

### 1. solis: Izvietot paneli uz tīmekļa servera

digna panelis savu konfigurāciju nolasa no faila `dashboard/dashboard_config.toml`. Šis fails instalācijā nav iekļauts — jūs to izveidojat `dashboard/` direktorijā līdzās paneļa failiem.

Tā saturs ir aprakstīts sadaļā [Vienotā pieteikšanās (SSO)](../../../sso/overview.md), kur šis fails arī ir nepieciešams: tajā ir panelī piedāvātās pieteikšanās iespējas un, daudzinstanču izvietošanai, backend savienojums.

Izvēlieties jūsu tīmekļa serveri un izpildiet atbilstošos izvietošanas soļus.

#### Izvietošana uz nginx

Ja izpildījāt sadaļu [nginx iestatīšana](#nginx-setup), server bloks jau norāda uz jūsu `dashboard` mapi, un nekas nav jākopē.

1. **Pārbaudiet ceļu**
   - Atveriet `/etc/nginx/conf.d/digna.conf`
   - Pārliecinieties, ka `root` norāda uz jūsu izpakoto `dashboard` mapi

2. **Nodrošiniet, ka mape ir nolasāma**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Pārlādējiet nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Pārbaudiet instalāciju**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost` (vai jūsu konfigurēto URL)
   - Jums jāredz digna paneļa pieteikšanās lapa

#### Izvietošana uz Apache httpd

1. **Kopējiet paneli uz dokumentu sakni**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Pievienojiet pārrakstīšanas noteikumus**

   Izvietotajā mapē izveidojiet failu `.htaccess`, lai paneļa maršruti saglabātos pēc pārlūkprogrammas atsvaidzināšanas:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Piekļūstiet panelim**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost/digna`
   - Jums jāredz digna paneļa pieteikšanās lapa

### 2. solis: SELinux (tikai RHEL saime)

RHEL, Rocky, AlmaLinux un Fedora sistēmās SELinux pēc noklusējuma darbojas režīmā enforcing un bloķē tīmekļa servera piekļuvi failiem ārpus tam paredzētajām vietām. Pārbaudiet, vai tas ir aktīvs:

```bash
getenforce
```

Ja rezultāts ir `Enforcing` un jūs servējat paneli no `/opt/digna/dashboard`, marķējiet direktoriju, lai tīmekļa serveris to drīkstētu nolasīt:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Piezīme"

    Ja `semanage` nav atrodams, instalējiet to ar `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Svarīgi"

    Ja panelis tikko konfigurētā RHEL serverī atgriež **403 Forbidden**, tā gandrīz vienmēr ir SELinux marķēšanas problēma, nevis failu atļauju problēma. Pārliecinieties ar `sudo ausearch -m avc -ts recent`.

---

## digna palaide kā systemd serviss {: #running-digna-as-a-systemd-service }

### Kāpēc darbināt digna kā servisu?

digna backend darbināšana kā systemd serviss nodrošina, ka tas:

- Automātiski startējas, kad dators tiek sāknēts
- Darbojas fonā bez atvērta termināļa loga
- Automātiski restartējas, ja notiek avārija
- To var pārvaldīt ar `systemctl`, standarta Linux servisu pārvaldnieku

### Servisa pārvaldības faili

Visi nepieciešamie faili atrodas digna instalācijas direktorijā zem: `bin/`

Pieejami šādi čaulas skripti:

- `install_service.sh` — reģistrē digna sistēmā systemd
- `uninstall_service.sh` — atreģistrē servisu
- `start_service.sh` — palaiž reģistrēto servisu
- `stop_service.sh` — aptur darbojošos servisu

!!! warning "Nepieciešamas root tiesības"

    Visi skripti jāizpilda ar `sudo`, jo servisa, kas startējas sāknēšanas laikā, reģistrēšana ieraksta unit failu direktorijā `/etc/systemd/system`.

### Skriptu padarīšana izpildāmus

Izpakošana var nesaglabāt izpildes bitu. Pirms pirmās lietošanas:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Servisa instalēšana

1. **Atveriet termināli**

2. **Pārejiet uz bin mapi**
   ```bash
   cd /opt/digna/bin
   ```

3. **Palaidiet instalācijas skriptu**
   ```bash
   sudo ./install_service.sh
   ```

digna serveris tagad ir reģistrēts sistēmā systemd ar **automātisku startēšanu**. Serviss netiek palaists uzreiz — skatiet nākamo sadaļu, lai to palaistu.

### Servisa palaišana un apturēšana

#### Lai palaistu servisu

1. Atveriet termināli
2. Pārejiet uz `/opt/digna/bin`
3. Palaidiet:
   ```bash
   sudo ./start_service.sh
   ```

#### Lai apturētu servisu

1. Atveriet termināli
2. Pārejiet uz `/opt/digna/bin`
3. Palaidiet:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Padoms"

    Vienmēr apturiet servisu, pirms atjaunināt lietojumprogrammas failus.

### Servisa pārvaldība ar systemctl

Pēc reģistrēšanas servisu var vadīt arī ar standarta systemd komandām no jebkuras direktorijas:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Servisa pārbaude

Lai pārliecinātos, ka serviss ir reģistrēts un darbojas:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` nozīmē, ka serviss startējas sāknēšanas laikā; `active` nozīmē, ka tas darbojas pašlaik.

### Servisa žurnālu skatīšana

systemd uztver visu, ko backend izvada konsolē. Lai to izlasītu:

```bash
sudo journalctl -u digna -n 100
```

Lai sekotu žurnālam reāllaikā, atkārtojot problēmu:

```bash
sudo journalctl -u digna -f
```

!!! tip "Padoms"

    Tas ir ātrākais veids, kā diagnosticēt servisu, kas startējas un uzreiz apstājas. Šeit tiek ziņots par repozitorija savienojuma kļūmi vai trūkstošu `license.toml`.

### Pārvietot servisu uz jaunu direktoriju

Unit fails glabā absolūto ceļu līdz izpildāmajam failam, tāpēc instalācijas pārvietošanai serviss ir jāreģistrē no jauna:

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

digna serveris tagad vairs nav reģistrēts sistēmā systemd.

---

## Jaunināšana uz jaunu izlaidumu {: #upgrading-to-a-new-release }

Šajā sadaļā aprakstīta Release 2026.06 instalācijas jaunināšana uz Release 2026.11. Ja jūsu instalācija ir vecāka, vispirms izlasiet [Jaunināšana no laidiena, kas vecāks par 2026.06](#upgrading-from-a-release-before-2026-06).

### Pirms jaunināšanas

**digna repozitorija rezerves kopijas izveide ir obligāta**

Pirms digna jaunināšanas veiciet rezerves kopiju sava repozitorija (PostgreSQL), lai izvairītos no datu zuduma. Rezerves kopija nodrošina atjaunošanas iespēju, ja jaunināšanas laikā rodas neparedzētas problēmas.

Lai izveidotu rezerves kopiju no čaulas:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Licences faila pieprasīšana Release 2026.11**

Release 2026.11 nepieciešams jauns `license.toml`. Pieprasiet to digna komandai pirms darba sākšanas un sagatavojiet to [7. solim](#step-7-replace-the-license-file).

### Jaunināšana no laidiena, kas vecāks par 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 ieviesa trīs izmaiņas, kas joprojām ir spēkā, ja vecāku instalāciju jaunina tieši uz 2026.11:

- **Tikai ODBC.** digna katru avota tehnoloģiju sasniedz caur ODBC. Katrs datubāzes savienojums, kas vēl neizmanto ODBC, pēc jaunināšanas jāpārceļ uz ODBC; automātiskas konvertēšanas nav. Iepriekš instalējiet ODBC draiverus digna resursdatorā, skatiet [ODBC draivera instalēšana digna resursdatorā](../../../databases/overview.md#install-the-driver), un sagatavojiet katra savienojuma īpašības no [tehnoloģiju rokasgrāmatām](../../../databases/overview.md#technology-guides). Databricks Legacy savienotājs vairs nepastāv; pārceliet šos savienojumus uz [Databricks](../../../databases/databricks_connector_guide.md) savienotāju.
- **Viens izpildāmais fails.** `dignabackend` un `dignacli` aizstāj viens izpildāmais fails `digna`, kas apvieno backend un CLI.
- **config.toml.** Sadaļa `[encryption]` ir obligāta, un `DIGNA_APP_HOST` un `DIGNA_APP_PORT` vairs netiek nolasīti: adresi un portu serveris iegūst no `digna serve`. Salīdziniet savu failu ar sadaļu [Backend konfigurācija](#backend-configuration).

Tālāk aprakstītajos soļos ir norādīts, kur vecākai instalācijai jārīkojas citādi. Repozitorija jaunināšana 8. solī jebkura agrāka laidiena repozitoriju jaunina tieši uz 2026.11.

### Jaunināšanas process

#### 1. solis: Apturēt digna servisu {: #step-1-stop-the-digna-service }

Ja digna darbojas kā systemd serviss, vispirms to apturiet:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Ja digna darbojas priekšplānā, tā termināļa logā nospiediet ++ctrl+c++.

#### 2. solis: Izveidojiet pašreizējās instalācijas dublējumu {: #step-2-backup-current-installation }

Savā digna instalācijas direktorijā pārdēvējiet pašreizējās instalācijas izpildāmo failu un paneļa mapi, lai jauno laidienu varētu izvietot tiem līdzās:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Saglabājiet `digna_old`, līdz esat pārbaudījis jaunināšanu, un `dashboard_old`, līdz esat no tās atjaunojis savus konfigurācijas failus (skatiet 4. soli). Pēc tam abus varat izdzēst.

!!! info "Jaunināšana no laidiena, kas vecāks par 2026.06"

    Izpildāmā faila vietā pārdēvējiet mapes `dignabackend` un `dignacli`: `sudo mv dignabackend dignabackend_old` un `sudo mv dignacli dignacli_old`. Release 2026.11 neizmanto nevienu no tām.

#### 3. solis: Izpakot un izvietot jauno versiju {: #step-3-extract-and-deploy-new-version }

1. Izpakojiet jauno digna instalācijas ZIP failu
2. Kopējiet jauno `digna` izpildāmo failu un `dashboard` mapi uz jūsu instalācijas direktoriju
3. Atjaunojiet izpildes bitu un servisa konta īpašumtiesības:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Svarīgi"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` nekad netiek iekļauts instalācijas ZIP — digna komanda nekad nepiegādā nevienu no šiem failiem. Tāpēc jaunināšana jūsu esošo konfigurāciju neskar, un kopijas pārdēvētajās `*_old` mapēs ir vienīgās, kas jums ir.

#### 4. solis: Atjaunot jūsu konfigurācijas failus {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

Panelis ir statisku failu kopums, tāpēc jūsu tīmekļa serveris — un pārlūkprogramma — joprojām var pasniegt iepriekšējo versiju. Pārlādējiet vai restartējiet tīmekļa serveri, kurā mitināta mape `dashboard`, un pēc tam pārlādējiet lapu ar pilnu atsvaidzināšanu (++ctrl+f5++).

#### 6. solis: Pārbaudiet konfigurāciju {: #step-6-validate-the-configuration }

Pirms pieskarties repozitorijam, pārliecinieties, ka `config.toml` ir pilnīgs:

```bash
./digna config check
```

Katrai sadaļai jāziņo OK. Izlabojiet visu, kas ziņots kā FAILED, noņemiet atslēgas, kas uzskaitītas sadaļā **Unknown keys**, un pirms turpināšanas palaidiet komandu vēlreiz.

#### 7. solis: Aizstāt licences failu {: #step-7-replace-the-license-file }

Licences fails parasti tiek pārnests no viena laidiena uz nākamo. Release 2026.11 ir izņēmums: tas pievieno divus licencējamus moduļus, digna Data Reconciliation un digna Agentic, un licence, kas izsniegta pirms 2026.11, tos nesatur. Nokopējiet `license.toml`, ko digna komanda nodrošināja Release 2026.11, instalācijas direktorijā, aizstājot veco:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
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

Ja darbināt kā systemd servisu:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Ja darbināt manuāli, restartējiet serveri:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Ja izmantojat nginx vai Apache, pārlādējiet attiecīgo tīmekļa serveri:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL saimē, ja direktorija `dashboard` tika aizstāta, atkārtoti piemērojiet SELinux marķējumu:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### 10. solis: Pārbaudīt jaunināšanu {: #step-10-verify-the-upgrade }

1. Pārbaudiet jaunā izpildāmā faila laidienu:

    ```bash
    ./digna version
    ```

    Pirmajai rindai jābūt `Release: 2026.11`.

2. Piekļūstiet digna panelim un pārbaudiet, vai saskarne ielādējas pareizi.
3. Pārskatiet servera žurnālus, vai nav kļūdu:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Pārbaudiet savus datubāzes savienojumus — skatiet [Savienojuma pārbaude](../../../databases/overview.md#testing-a-connection). Pēc jaunināšanas no laidiena, kas vecāks par 2026.06, vispirms pārceliet uz ODBC katru savienojumu, kas vēl neizmantoja ODBC.

Lai sāktu darbu ar jaunajiem moduļiem, skatiet [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [AI aģenta pievienošana](../../../platform/agentic/connect_ai_agent.md) par digna MCP Server un [Profilēšanas vieta](../../../platform/profiling/profiling_location.md) par digna Engine.
