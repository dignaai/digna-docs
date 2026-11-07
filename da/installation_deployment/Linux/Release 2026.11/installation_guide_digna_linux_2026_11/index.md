# Linux-installationsvejledning for digna Release 2026.11

**Release:** 2026.11

**Sidst opdateret:** 7. november 2026


---

## Indholdsfortegnelse

1. [Introduktion](#introduction)
2. [Systemkrav](#system-requirements)
3. [Forberedende opsætning](#pre-installation-setup)
4. [PostgreSQL-serveropsætning](#postgresql-server-setup)
5. [Webserverkonfiguration](#web-server-configuration)
6. [Initial installation](#initial-installation)
7. [Backend-konfiguration](#backend-configuration)
8. [Dashboard-konfiguration](#dashboard-configuration)
9. [Kørsel af digna som systemd-service](#running-digna-as-a-systemd-service)
10. [Opgradering til en ny release](#upgrading-to-a-new-release)

---

## Introduktion {: #introduction }

### Om digna

digna er en omfattende AI-drevet platform designet til at optimere datakvalitetsstyring på tværs af forskellige data­miljøer som warehouses, lakes og lakehouses. Bygget til høj skalerbarhed og fleksibilitet adresserer digna moderne dataudfordringer gennem automatisering, realtids­overvågning og anomali­detektion.

digna består af to hovedkomponenter:

- **digna**: applikationens kerne, ansvarlig for at behandle data og udføre kvalitetskontroller. Den samler backend og kommandolinjegrænsefladen i én eksekverbar fil og erstatter dermed de separate programmer `dignabackend` og `dignacli` fra tidligere releases.
- **dignadashboard**: Et webbaseret interface hostet på en webserver, som giver en brugervenlig måde at interagere med digna-platformen og visualisere datakvalitetsmålinger.

### Nyheder i Release 2026.11

Denne release tilføjer digna Data Reconciliation, digna Agentic med digna MCP Server samt digna Engine, som kan profilere data inde i digna og kontrollere referentiel integritet mellem forskellige databaseteknologier. Se [release notes](../../../changelog/Release_202611.md) for fulde detaljer.

For en installation bringer releasen en ny migreringsmekanisme for repositoriet, en valgfri `[duckdb]`-sektion i `config.toml` til digna Engine og en ny licensfil. [Opgraderingsafsnittet](#upgrading-to-a-new-release) gennemgår hver af dem.

### Leder du efter Windows eller macOS?

Denne vejledning dækker Linux. For andre platforme, se [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) eller [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Hvilken distribution dækker denne vejledning?

Instruktionerne er skrevet for de to mest almindelige serverfamilier. Hvor de to adskiller sig, er begge kommandoer angivet:

- **Debian-familien** — Debian, Ubuntu. Pakkestyring: `apt`.
- **RHEL-familien** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Pakkestyring: `dnf`.

Enhver moderne distribution med `systemd` vil fungere; kun pakkenavne og nogle få konfigurationsstier ændrer sig.

---

## Systemkrav {: #system-requirements }

Før du begynder installationen, sørg for at dit system opfylder følgende minimumskrav:

| Krav | Specifikation |
|---|---|
| **Operativsystem** | Ubuntu 22.04 LTS eller nyere, Debian 12 eller nyere, RHEL 9 / Rocky 9 / AlmaLinux 9 eller nyere |
| **Arkitektur** | x86_64 (amd64) eller arm64 |
| **Init-system** | systemd |
| **Hukommelse (minimal opsætning)** | 16 GB RAM |
| **Diskplads** | 10 GB ledig lagerplads |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Webserver** | nginx, Apache httpd eller tilsvarende |

!!! info "digna Engine"

    Databaseforbindelser, der bruger digna Engine som profileringssted, profileres på selve
    digna-værten. Planlæg ekstra hukommelse og diskplads til dem, se
    [\[duckdb\]-sektionen](#duckdb-section).

### Databaseinstallationsmuligheder

**Hvis PostgreSQL allerede er installeret:**
Du kan tilføje en ny database til digna i din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskine som digna:**

!!! info "Anbefalede specifikationer"

    - **Hukommelse**: 32 GB RAM (i stedet for 16 GB)
    - **Diskplads**: 50 GB ledig lagerplads (i stedet for 10 GB)

    Disse højere specifikationer tilgodeser både digna og PostgreSQL-databasen, når de kører samtidigt.

### Kontrol af distribution og arkitektur

Flere kommandoer i denne vejledning adskiller sig mellem Debian- og RHEL-familierne. For at kontrollere hvilken du kører, kør:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` eller `ID=debian` — brug `apt`-kommandoerne.
- `ID=rhel`, `rocky`, `almalinux` eller `fedora` — brug `dnf`-kommandoerne.
- `x86_64` eller `aarch64` — arkitekturen til installationspakken, du skal bruge.

---

## Forberedende opsætning {: #pre-installation-setup }

Før du installerer digna, skal du sikre dig, at to nøgleforudsætninger er på plads:

1. **PostgreSQL-server** – til lagring af beregnede målinger og performance-data
2. **Webserver** – til hosting af digna Dashboard

Hvis disse komponenter ikke allerede er opsat, følg nedenstående afsnit for at installere og konfigurere dem.

### Opdatering af pakkelisten

Opdater dine pakkelister, før du installerer noget:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Bemærk"

    I hele denne vejledning er den første kommando i et par for **Debian-familien** og den anden for **RHEL-familien**. Kør kun den, der passer til dit system.

---

## PostgreSQL-serveropsætning {: #postgresql-server-setup }

### Hvis du allerede har PostgreSQL

Hvis PostgreSQL allerede er installeret og kører lokalt eller hvis du bruger en administreret fjern-PostgreSQL-server, kan du springe til [næste afsnit](#web-server-configuration).

### Installation af PostgreSQL

#### Trin 1: Installer serverpakken

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tip"

    Distributionernes pakker kan være bagud i forhold til den nyeste PostgreSQL-version. Hvis du har brug for en nyere version, brug den officielle [PostgreSQL apt- eller yum-repositorium](https://www.postgresql.org/download/linux/) i stedet.

#### Trin 2: Initialiser databaseklustret

På **Debian-familien** opretter og starter pakken et cluster automatisk — spring til næste trin.

På **RHEL-familien** skal clustret oprettes eksplicit:

```bash
sudo postgresql-setup --initdb
```

#### Trin 3: Start og aktiver servicen

```bash
sudo systemctl enable --now postgresql
```

Dette starter PostgreSQL med det samme og konfigurerer det til automatisk start ved boot.

#### Trin 4: Bekræft installationen

```bash
psql --version
sudo systemctl status postgresql
```

Du bør se PostgreSQL-versionen og en `active (running)` service.

#### Trin 5: Forbind til serveren

En Linux PostgreSQL-pakke opretter en `postgres` systemkonto, som ejer clustret. Forbind via denne konto:

```bash
sudo -u postgres psql
```

!!! note "Bemærk — Linux adskiller sig fra Windows her"

    Windows-installationsprogrammet beder dig om at sætte en adgangskode for `postgres` superbrugeren under installationen. Linux-pakker gør ikke det. I stedet autentificeres lokale forbindelser via **peer authentication**: det `postgres` operativsystembrugernavn må forbinde som `postgres` databasebrugeren uden adgangskode.

    Derfor bruger kommandoen ovenfor `sudo -u postgres`. digna-backend forbinder via TCP med brugernavn og adgangskode, så du vil oprette en eksplicit digna-bruger i [Initial installation](#initial-installation).

#### Trin 6: Bekræft porten

Standard PostgreSQL-porten er `5432`. For at bekræfte hvilken port din server lytter på:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Notér værdien — du får brug for den, når du konfigurerer digna-backend.

#### Trin 7: Aktivér adgangskodeautentifikation for digna-brugeren

digna forbinder til PostgreSQL over TCP som `digna_user`, hvilket kræver adgangskodeautentifikation fremfor peer. Kontroller, at din `pg_hba.conf` tillader det.

Find filen:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Åbn den i en editor og bekræft, at de lokale TCP-linjer bruger `scram-sha-256` (eller `md5` på ældre servere) i stedet for `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Genindlæs PostgreSQL efter enhver ændring:

```bash
sudo systemctl reload postgresql
```

!!! warning "Vigtigt"

    Hvis digna rapporterer `FATAL: Ident authentication failed for user "digna_user"`, er denne indstilling årsagen.

#### Trin 8: Hvis PostgreSQL kører på en anden maskine

For at acceptere forbindelser fra en anden vært, sæt `listen_addresses` i `postgresql.conf` og tilføj en matchende `host`-linje for dit netværk i `pg_hba.conf`:

```
listen_addresses = '*'
```

Åbn derefter porten i firewall'en og genstart servicen:

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

## Webserverkonfiguration {: #web-server-configuration }

digna kræver en webserver til at hoste dashboardet. Vælg en af følgende muligheder:

- [nginx](#nginx-setup) — letvægt og anbefalet
- [Apache httpd](#apache-setup) — bredt udbredt alternativ

Du behøver kun at installere og konfigurere **én** af disse servere.

Begge sektioner konfigurerer to ting, som dashboardet afhænger af:

- **En single-page-application-fallback**, så genindlæsning af en dashboard-URL ikke giver 404
- **En `.md` MIME-type**, så Markdown-filer serveres korrekt

### nginx-opsætning {: #nginx-setup }

#### Oversigt

nginx er en let, højtydende webserver, velegnet til at serve det statiske digna-dashboard.

#### Installation

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Start af nginx

```bash
sudo systemctl enable --now nginx
```

#### Bekræft installationen

1. Åbn din browser
2. Gå til `http://localhost`
3. Du bør se nginx-velkomstsiden

#### Åbning af firewall

Hvis serveren tilgås fra andre maskiner, tillad HTTP-trafik:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Konfigurering af et site til dashboardet

nginx inkluderer alle filer i `conf.d`-mappen på begge distributionsfamilier. Opret en dedikeret konfigurationsfil til digna dér:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Indsæt følgende, og erstat `/opt/digna/dashboard` med den faktiske sti til din udpakkede `dashboard`-mappe:

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

!!! warning "Vigtigt"

    Uden `try_files`-direktivet vil en genindlæsning af enhver dashboard-side bortset fra rod-URL'en give en 404. Dette er nginx-ækvivalenten til URL Rewrite-modulet, som kræves af IIS på Windows.

#### Deaktiver standardsitet

Kun én serverblok kan være `default_server` for en port. På **Debian-familien** fjern den pakkede default, så den ikke konflikter:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

På **RHEL-familien** kommentér eller slet `server { ... }`-blokken inde i `/etc/nginx/nginx.conf`.

#### Anvend konfigurationen

Test konfigurationen for syntaksfejl, og genindlæs nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd-opsætning {: #apache-setup }

#### Oversigt

Apache httpd findes i standardlageret for alle understøttede distributioner. Pakken hedder `apache2` på Debian-familien og `httpd` på RHEL-familien.

#### Installation

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Start af Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Bekræft installationen

1. Åbn din browser
2. Gå til `http://localhost`
3. Du bør se distributionens standard Apache-side

#### Krævet: Aktivér mod_rewrite

Dashboardet kræver URL-omskrivning.

På **Debian-familien**, aktivér modulet og genstart:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

På **RHEL-familien** er `mod_rewrite` indlæst som standard. Bekræft det:

```bash
httpd -M | grep rewrite
```

#### Krævet: Tillad .htaccess-overrides

Åbn konfigurationsfilen for din dokumentrod:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Find `<Directory>`-blokken, der dækker din dokumentrod (`/var/www/html` på begge familier) og ændr:

```apache
AllowOverride None
```

til:

```apache
AllowOverride All
```

#### Krævet: MIME-type for Markdown-filer

I samme fil, tilføj følgende linje, så Markdown-filer serveres korrekt:

```apache
AddType text/markdown .md
```

!!! warning "Vigtigt"

    Uden denne indstilling kan `.md`-filer muligvis ikke serveres korrekt.

#### Anvend konfigurationen

Tjek konfigurationen for syntaksfejl, og genstart Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Initial installation {: #initial-installation }

### Trin 1: Opret digna-repositoriet

digna-repositoriet lagrer alle målinger, som digna beregner. Det fungerer som den centrale database for analytiske- og performance-data.

#### Opret repository-schema og bruger

Åbn din PostgreSQL-klient (psql, pgAdmin eller lignende) og udfør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstat følgende pladsholdere:**

- `<digna_repo_schema>` — Dit ønskede schema-navn (fx `dignarepo`)
- `<digna_repo_user>` — Dit ønskede brugernavn (fx `digna_user`)
- `<digna_repo_password>` — En sikker adgangskode til denne bruger

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

For at køre disse fra shell i ét trin:

```bash
sudo -u postgres psql
```

Indsæt derefter udsagnene ved `postgres=#` prompten og skriv `\q` for at afslutte.

!!! tip "Bedste praksis"

    Brug stærke, komplekse adgangskoder til databasebrugere. Undgå let gættelige legitimationsoplysninger.

---

### Trin 2: Pak digna-installationspakken ud

1. Find digna-installations-ZIP-filen, som er leveret til dig
2. Pak den ud til din ønskede installationssti — for eksempel `/opt/digna`
3. Efter udpakning bør du se følgende elementer:
   - `dashboard/` — Webdashboard-interface
   - `digna` — Hovedkørbar fil (backend + CLI kombineret)

!!! info "Konfigurations- og licensfilerne er ikke med i pakken"

    Hverken `config.toml` eller `dashboard/dashboard_config.toml` følger med installationen — du
    opretter begge selv, i [Backend-konfiguration](#backend-configuration) og
    [Dashboard-konfiguration](#dashboard-configuration). `license.toml` følger heller ikke med;
    digna leverer den separat, som beskrevet i Trin 3.

For at udpakke fra shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Bemærk"

    Hvis `unzip` ikke er installeret, tilføj det med `sudo apt install -y unzip` eller `sudo dnf install -y unzip`.

#### Gør den eksekverbare fil kørbar

Afhængigt af hvordan arkivet blev overført, kan den eksekverbare bit være tabt under udpakning. Sæt den eksplicit:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Opret en servicekonto

Det anbefales at køre backend som en dedikeret uprivilegeret bruger i produktionsmiljøer:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Bemærk"

    På RHEL-familien er den tilsvarende shellsti `/sbin/nologin`.

### Trin 3: Installer licensfilen

!!! warning "Vigtigt"

    Licensfilen er **ikke** inkluderet i installationspakken og leveres separat af digna.

1. Find den `license.toml`-fil, som er leveret til dig
2. Kopiér den ind i rodinstallationsmappen for digna (hvor `config.toml` og den eksekverbare `digna` ligger)

**Hvorfor det er vigtigt:**
Licensfilen indeholder dine kundeoplysninger, licensens udløbsdato og det digitale signatur. **Ændr ikke denne fil** — enhver ændring vil ugyldiggøre den.

**Mappe­struktur efter opsætning:**

```
/opt/digna/
├── config.toml         (konfigurationsfil)
├── license.toml        (DIN LICENSFIL - kopier her)
├── digna               (hovedkørbar fil)
├── bin/                (servicehåndteringsscripts)
└── dashboard/          (webinterface)
    └── (dashboard-filer)
```

---

## Backend-konfiguration {: #backend-configuration }

### Trin 1: Opret og rediger konfigurationsfilen

Filen `config_template.toml` medfølger i din digna-installationsmappe. Du skal blot omdøbe den til `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Placering:** `/opt/digna/config.toml`

Åbn `config.toml` i en teksteditor og konfigurer hver sektion nedenfor.

#### [app] Sektion

Denne sektion konfigurerer cross-origin resource sharing (CORS) mellem dashboardet og backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL'er | De URL'er, dashboardet leveres fra. Browseranmodninger fra enhver anden origin afvises |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrævet, så browseren sender sessionscookien med hver anmodning |

!!! note "Bemærk"

    Hvis du servicerer dashboardet fra nginx eller Apache på standard HTTP-porten, er origin, der skal tillades, `http://localhost` — eller serverens offentlige URL, når dashboardet tilgås fra andre maskiner.

!!! info "Sektionen [app] er valgfri"

    Fra Release 2026.11 kan begge nøgler, og hele sektionen `[app]`, udelades. Det er den
    rigtige opsætning, når en reverse proxy leverer dashboardet og backend under én origin:
    browseren foretager så ingen cross-origin-anmodninger, og som standard tillades ingen.

#### [repo] Sektion

Denne sektion konfigurerer forbindelsen til PostgreSQL-databasen:

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

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasenavn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema oprettet tidligere |
| `DIGNA_REPO_USER` | `digna_user` | Bruger oprettet i PostgreSQL-opsætningen |
| `DIGNA_REPO_PASSWORD` | Din adgangskode | Adgangskode angivet ved schema-oprettelsen |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valgfri. PostgreSQL SSL-tilstand: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valgfri. Antal forbindelser, digna holder åbne til repositoriet |

!!! tip "Bedste praksis"

    `config.toml` indeholder en databaseadgangskode i klartekst. Begræns dets tilladelser, så kun servicekontoen kan læse det:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] Sektion

Denne sektion indeholder indstillinger for sikkerhed, cookies og inspektioner:

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

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_FERNET_KEY` | Værdien vist ovenfor | Nøgle til den kryptering, som tidligere releases brugte. Den skal være til stede; behold den viste værdi |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Den vært, dashboardet tilgås under. `""` angiver intet domæne, hvilket er rigtigt bag en proxy, der leverer dashboardet og backend under én origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Skal være `true`, når digna leveres over HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Holder sessionscookien uden for scripts' rækkevidde |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `DIGNA_MAX_WORKERS` | Antal CPU-kerner - 1 | Antal inspektioner, der må køre samtidig |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Påkrævet. Bruges til linkene i notifikationsbeskeder, så det skal være en URL, modtagerne kan åbne |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valgfri. Antal sekunder, en enkelt forespørgsel mod en kildedatabase må køre, før den afbrydes; `0` deaktiverer timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valgfri. Antal sekunder, der ventes på en forbindelse til en kildedatabase; `0` venter ubegrænset |

!!! tip "Tip"

    For at finde antallet af CPU-kerner på din server, kør `nproc`.

#### [encryption] Sektion

Denne sektion indeholder nøglen, der bruges til at kryptere følsomme værdier i repositoryet. Den er **påkrævet** — `config check` rapporterer sektionen `[encryption]` som FAILED, hvis nøglen mangler.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodet nøgle | Krypterer følsomme værdier, der er gemt i digna-repositoryet |

!!! warning "Beskyt config.toml"

    Denne nøgle er en fast værdi, der er identisk i alle digna-installationer, og det er den, der dekrypterer de følsomme værdier i dit repository. Begræns `config.toml` til den konto, der kører digna, hold filen uden for versionsstyring og delte drev, og udelad den fra enhver sikkerhedskopi, der opbevares mindre sikkert end selve repositoryet.

#### [logging] Sektion

Denne sektion konfigurerer logningsadfærd:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` til produktion, `DEBUG` til fejlsøgning. `TRACE`, `WARN` og `ERROR` accepteres også |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valgfri. Mappe til de roterende logfiler, relativt til arbejdsmappen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valgfri. Antal roterede logfiler, der beholdes |

#### [duckdb] Sektion (valgfri) {: #duckdb-section }

Nyt i Release 2026.11. Denne sektion fastlægger ressourcerne for **digna Engine**, som profilerer
data inde i digna for databaseforbindelser, hvis profileringssted er **digna Engine**, og
kører kontroller af referentiel integritet mellem datakilder på forskellige databaseforbindelser. Se
[Profileringssted](../../../platform/profiling/profiling_location.md).

Sektionen er valgfri. Uden den gælder standardværdierne nedenfor.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Hukommelse i MB, som én kørsel af digna Engine må bruge. Op til `DIGNA_MAX_WORKERS` kørsler kan være aktive samtidig |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: systemets midlertidige mappe (`$TMPDIR`, eller `/tmp` når den ikke er sat) | Mappe til midlertidige filer, når data ikke kan være i hukommelsen |

!!! tip "Dimensionering af digna Engine"

    Planlæg op til `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` hukommelse på digna-værten
    ud over det, digna selv bruger, og nok ledig diskplads i den midlertidige mappe til at rumme
    den største inspicerede dato blandt de datakilder, der bruger digna Engine.
    Lad `DIGNA_DUCKDB_TEMP_DIRECTORY` pege på en disk med den plads, som den konto, der kører
    digna, kan skrive til:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    Du har kun brug for denne sektion, hvis mindst én databaseforbindelse bruger digna Engine, eller
    hvis en kontrol af referentiel integritet sammenligner datakilder på forskellige forbindelser.

---

### Trin 2: Validér konfigurationen

Kontrollér, at `config.toml` er fuldstændig og korrekt opbygget, før du initialiserer repositoryet. Kør i din digna-installationsmappe:

```bash
./digna config check
```

Hver sektion valideres for sig, så en enkelt fejl ikke skjuler tilstanden af de øvrige:

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

Ret alt, der rapporteres som FAILED, og kør kommandoen igen, før du fortsætter. En WARNING under **Unknown keys** viser nøgler i `config.toml`, som digna ikke læser; de har ingen effekt, så fjern dem eller ret deres stavemåde. Den fulde liste over muligheder findes i [CLI-referencen](../../../cli/Command_Line_Interface_202611.md).

### Trin 3: Initialiser repositoriet

1. Åbn en terminal
2. Gå til din digna-installationsmappe (hvor `config.toml` og den eksekverbare `digna` er placeret)
3. Kør forbindelsestesten:

```bash
cd /opt/digna
./digna repo check
```

På et nyt schema opretter kommandoen forbindelse og melder derefter, at der endnu ikke er installeret noget repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

På dette tidspunkt er det det forventede resultat: det bekræfter, at digna når PostgreSQL og schemaet. En forbindelses- eller godkendelsesfejl peger i stedet på sektionen `[repo]` eller på PostgreSQL-opsætningen.

!!! note "Bemærk"

    På Linux er den aktuelle mappe ikke på din PATH, så den eksekverbare fil kaldes som `./digna` i stedet for `digna`. For at bruge den kortere form overalt, tilføj et symbolsk link:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Trin 4: Installer repository-schemaet

I samme mappe, kør:

```bash
./digna repo upgrade
```

Denne kommando installerer de nødvendige tabeller i repository-schemaet og afslutter med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerer og opgraderer"

    Fra Release 2026.11 installerer `repo upgrade` et nyt repository og opgraderer et eksisterende.
    `repo install` virker stadig som et andet navn for den samme kommando.

### Trin 5: Opret en adminbruger

1. Åbn et **nyt** terminalvindue
2. Gå til din digna-installationsmappe
3. Kør følgende kommando for at oprette en adminbruger:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Eksempel:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Dette opretter en bruger med e-mailadressen `admin@example.com` og fulde administratorrettigheder.

!!! tip "Tip"

    Indram adgangskoden i enkelte citationstegn. `bash` og `zsh` behandler tegn som `!`, `$` og `*` specielt, og en ikke-indrammet adgangskode med disse tegn vil ikke blive sendt igennem som tastet.

!!! tip "Bedste praksis"

    Brug en stærk adgangskode med blanding af store og små bogstaver, tal og specialtegn.

---

### Trin 6: Start digna-serveren

I digna-installationsmappen, start serveren med:

```bash
./digna serve --address <host> --port <port>
```

**Parametre:**
- `--address` — Serverens hostname/IP (standard `127.0.0.1`)
- `--port` — Serverport (standard `8000`)

Når serveren er oppe, udskriver den den adresse, den lytter på:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tip"

    Hvis dashboardet serviceres fra en anden maskine end backend, åbn også API-porten i firewall'en:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Serveren optager terminalen"

    `serve` kører i forgrunden og fortsætter, indtil du stopper den med ++ctrl+c++. Lad den køre, mens du færdiggør opsætningen; for at starte den automatisk ved opstart, se [Kør digna som systemd-tjeneste](#running-digna-as-a-systemd-service).

## Dashboard-konfiguration {: #dashboard-configuration }

### Trin 1: Deploy dashboard til webserver

digna-dashboardet læser sin egen konfiguration fra `dashboard/dashboard_config.toml`. Den fil følger ikke med installationen — du opretter den i `dashboard/`-mappen sammen med dashboardfilerne.

Dens indhold er beskrevet under [Single Sign-On](../../../sso/overview.md), som også er der, hvor filen er nødvendig: den indeholder de login-muligheder, dashboardet tilbyder, og ved multi-instance deployment backend-forbindelsen.

Vælg din webserver og følg de tilsvarende deploy-trin.

#### Deploy til nginx

Hvis du fulgte [nginx-opsætningen](#nginx-setup), peger serverblokken allerede på din `dashboard`-mappe, og ingen kopiering er nødvendig.

1. **Bekræft stien**
   - Åbn `/etc/nginx/conf.d/digna.conf`
   - Bekræft, at `root` peger på din udpakkede `dashboard`-mappe

2. **Sørg for at mappen er læsbar**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Genindlæs nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Test installationen**
   - Åbn din browser
   - Gå til `http://localhost` (eller din konfigurerede URL)
   - Du bør se digna-dashboardets login-side

#### Deploy til Apache httpd

1. **Kopier dashboardet til dokumentroden**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Tilføj omskrivningsreglerne**

   Opret en `.htaccess`-fil inde i den deployerede mappe, så dashboard-ruter overlever en browser-genindlæsning:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Indsæt følgende:

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

3. **Genstart Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Tilgå dashboardet**
   - Åbn din browser
   - Gå til `http://localhost/digna`
   - Du bør se digna-dashboardets login-side

### Trin 2: SELinux (kun RHEL-familien)

På RHEL, Rocky, AlmaLinux og Fedora er SELinux som standard i enforcing-tilstand og vil blokere webserveren fra at læse filer uden for forventede placeringer. Kontroller om den er aktiv:

```bash
getenforce
```

Hvis resultatet er `Enforcing` og du servicerer dashboardet fra `/opt/digna/dashboard`, label mappen, så webserveren kan læse den:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Bemærk"

    Hvis `semanage` ikke findes, installer det med `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Vigtigt"

    Et dashboard, der returnerer **403 Forbidden** på en nykonfigureret RHEL-server, skyldes næsten altid et SELinux-labelingsproblem fremfor et fil-tilladelsesproblem. Bekræft med `sudo ausearch -m avc -ts recent`.

---

## Kørsel af digna som en systemd-service {: #running-digna-as-a-systemd-service }

### Hvorfor køre digna som en service?

At køre digna-backend som en systemd-service sikrer, at den:

- Starter automatisk, når maskinen booter
- Kører i baggrunden uden et åbent terminalvindue
- Genstarter automatisk, hvis den crasher
- Kan administreres via `systemctl`, standard Linux service‑manager

### Filer til servicehåndtering

Alle nødvendige filer findes i digna-installationsmappen under: `bin/`

Følgende shell-scripts er tilgængelige:

- `install_service.sh` — registrerer digna hos systemd
- `uninstall_service.sh` — afregistrerer servicen
- `start_service.sh` — starter den registrerede service
- `stop_service.sh` — stopper den kørende service

!!! warning "Root-adgang påkrævet"

    Alle scripts skal køres med `sudo`, fordi registrering af en service, der starter ved boot, skriver en unit-fil til `/etc/systemd/system`.

### Gør scripts eksekverbare

Udpakning bevarer muligvis ikke eksekveringsrettigheder. Før første brug:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Installer servicen

1. **Åbn en terminal**

2. **Gå til bin-mappen**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kør installationsscriptet**
   ```bash
   sudo ./install_service.sh
   ```

Digna-serveren er nu registreret hos systemd med **automatisk opstart** aktiveret. Servicen starter ikke nødvendigvis med det samme — se næste sektion for at starte den.

### Start og stop servicen

#### For at starte servicen

1. Åbn en terminal
2. Gå til `/opt/digna/bin`
3. Kør:
   ```bash
   sudo ./start_service.sh
   ```

#### For at stoppe servicen

1. Åbn en terminal
2. Gå til `/opt/digna/bin`
3. Kør:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Stop altid servicen før opdatering af applikationsfiler.

### Administrer servicen med systemctl

Når den er registreret, kan servicen også kontrolleres med standard systemd-kommandoer fra enhver mappe:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Bekræft servicen

For at bekræfte at servicen er registreret og kørende:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` betyder, at servicen starter ved boot; `active` betyder, at den kører nu.

### Vis serviceloggen

systemd fanger alt, backend skriver til konsollen. For at læse den:

```bash
sudo journalctl -u digna -n 100
```

For at følge loggen live mens du reproducerer et problem:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tip"

    Dette er den hurtigste måde at diagnosticere en service, der starter og straks stopper. En forbindelsesfejl til repositoriet eller en manglende `license.toml` rapporteres her.

### Flyt servicen til en ny mappe

Unit-filen gemmer den absolutte sti til den eksekverbare fil, så flytning af installationen kræver re-registrering af servicen:

1. **Afinstaller den nuværende service**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Flyt applikationsfilerne**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Geninstaller servicen**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Start servicen**
   ```bash
   sudo ./start_service.sh
   ```

### Afinstallation af servicen

1. **Stop den kørende service**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Afinstaller servicen**
   ```bash
   sudo ./uninstall_service.sh
   ```

Digna-serveren er nu afregistreret fra systemd.

---

## Opgradering til en ny release {: #upgrading-to-a-new-release }

Dette afsnit opgraderer en installation af Release 2026.06 til Release 2026.11. Hvis din
installation er ældre, så læs først [Opgradering fra en release før 2026.06](#upgrading-from-a-release-before-2026-06).

### Før du opgraderer

**Oprettelse af backup af digna-repositoriet er obligatorisk**

Før du opgraderer digna, tag en backup af dit repositorium (PostgreSQL) for at beskytte mod datatab.
En backup sikrer, at du kan gendanne, hvis opgraderingen støder på uventede problemer.

For at skabe en backup fra shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Anmod om licensfilen til Release 2026.11**

Release 2026.11 kræver en ny `license.toml`. Anmod digna-teamet om den, før du starter, og hav
den klar til [Trin 7](#step-7-replace-the-license-file).

### Opgradering fra en release før 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 bragte tre ændringer, som stadig gælder, når du opgraderer en ældre installation
direkte til 2026.11:

- **Kun ODBC.** digna når hver kildeteknologi via ODBC. Hver databaseforbindelse, der endnu ikke
  bruger ODBC, skal lægges om til ODBC efter opgraderingen; der er ingen automatisk
  konvertering. Installér ODBC-driverne på digna-værten på forhånd, se
  [Installér ODBC-driveren på digna-værten](../../../databases/overview.md#install-the-driver),
  og hav egenskaberne for hver forbindelse klar fra
  [teknologivejledningerne](../../../databases/overview.md#technology-guides). Databricks Legacy-connectoren
  findes ikke længere; flyt disse forbindelser til
  [Databricks](../../../databases/databricks_connector_guide.md)-connectoren.
- **Én eksekverbar fil.** `dignabackend` og `dignacli` er erstattet af den enkelte eksekverbare fil `digna`,
  som samler backend og CLI.
- **config.toml.** Sektionen `[encryption]` er påkrævet, og `DIGNA_APP_HOST` og
  `DIGNA_APP_PORT` læses ikke længere: serveren henter sin adresse og port fra `digna serve`.
  Sammenlign din fil med [Backend-konfiguration](#backend-configuration).

Trinene nedenfor angiver, hvor en ældre installation kræver noget andet. Opgraderingen af
repositoriet i Trin 8 bringer et repository fra enhver tidligere release direkte til 2026.11.

### Opgraderingsproces

#### Trin 1: Stop digna-servicen {: #step-1-stop-the-digna-service }

Hvis digna kører som en systemd-service, stop den først:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Hvis digna kører i forgrunden, tryk ++ctrl+c++ i terminalvinduet.

#### Trin 2: Sikkerhedskopiér nuværende installation {: #step-2-backup-current-installation }

Omdøb den eksekverbare fil og dashboard-mappen i din nuværende installation i digna-installationsmappen,
så den nye release kan udrulles ved siden af dem:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Behold `digna_old`, indtil du har verificeret opgraderingen, og `dashboard_old`, indtil du har gendannet
dine konfigurationsfiler fra den (se Trin 4). Derefter kan du slette begge.

!!! info "Opgradering fra en release før 2026.06"

    Omdøb mapperne `dignabackend` og `dignacli` i stedet for den eksekverbare fil:
    `sudo mv dignabackend dignabackend_old` og `sudo mv dignacli dignacli_old`. Ingen af dem bruges af Release 2026.11.

#### Trin 3: Udpak og deploy ny version {: #step-3-extract-and-deploy-new-version }

1. Pak den nye digna-installations-ZIP-fil ud
2. Kopiér den nye `digna`-eksekverbare og `dashboard`-mappen til din installationsmappe
3. Genskab den eksekverbare bit og ejerskab til servicekontoen:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Vigtigt"

    Hverken `config.toml` eller `dashboard/dashboard_config.toml` er nogensinde inkluderet i
    installations-ZIP'en — digna-teamet leverer aldrig nogen af filerne. Din eksisterende konfiguration
    berøres derfor ikke af opgraderingen, og kopierne i de omdøbte `*_old`-mapper er de
    eneste, du har.

#### Trin 4: Gendan dine konfigurationsfiler {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 kræver ingen ændring af `config.toml`: en fil, der virker med Release 2026.06,
virker fortsat. To ændringer er valgfrie:

- Tilføj en [`[duckdb]`-sektion](#duckdb-section), hvis databaseforbindelser skal bruge digna Engine,
  og dens standardværdier ikke passer til din vært.
- Udelad sektionen `[app]`, hvis en reverse proxy leverer dashboardet og backend under én
  origin.

!!! warning "Indstillinger, som digna ikke læser"

    Tidligere versioner af denne vejledning viste nogle indstillinger, som digna ikke læser. De har ingen
    effekt, og `config check` viser dem under **Unknown keys** i Trin 6. Fjern eller ret
    dem:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` og
      `digna_LOGGING_BACKUP_COUNT` findes ikke. Fjern dem.
    - Der skelnes mellem store og små bogstaver i indstillingsnavne. digna læser `DIGNA_REPO_HOST`, ikke `digna_REPO_HOST`.
      Skriv alle navne med store bogstaver som i [Backend-konfiguration](#backend-configuration).

!!! warning "Single sign-on: behold [[oidc_clients]]"

    digna læser single sign-on-udbydere som en liste af `[[oidc_clients]]`-poster, hver med sin egen
    `DIGNA_OIDC_KEY`. Hvis du har ændret dine udbydere til `[oidc_clients.<key>]`-sektioner, som en
    tidligere version af denne vejledning viste, så ændr dem tilbage. `config check` rapporterer
    `OIDC config(s)` som FAILED, så længe den form findes:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Gentag posten for hver udbyder, og hold hver `DIGNA_OIDC_KEY` identisk med `key` i
    `dashboard_config.toml`. Kun installationer, der bruger single sign-on, er berørt.

#### Trin 5: Genindlæs webserveren {: #step-5-reload-the-web-server }

Dashboardet er et sæt statiske filer, så din webserver — og browseren — kan stadig
levere den tidligere version. Genindlæs eller genstart den webserver, der hoster `dashboard`-
mappen, og genindlæs derefter siden med en hård opdatering (++ctrl+f5++).

#### Trin 6: Validér konfigurationen {: #step-6-validate-the-configuration }

Bekræft, at `config.toml` er fuldstændig, før du rører repositoryet:

```bash
./digna config check
```

Hver sektion skal rapportere OK. Ret alt, der rapporteres som FAILED, fjern de nøgler, der vises under
**Unknown keys**, og kør kommandoen igen, før du fortsætter.

#### Trin 7: Udskift licensfilen {: #step-7-replace-the-license-file }

En licensfil overføres normalt fra én release til den næste. Release 2026.11 er en
undtagelse: den tilføjer to licenserede moduler, digna Data Reconciliation og digna Agentic, og en
licens udstedt før 2026.11 indeholder dem ikke. Kopiér den `license.toml`, som digna-teamet har
leveret til Release 2026.11, til installationsmappen, så den erstatter den gamle:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Behold ikke den tidligere licens"

    Med den tidligere licens starter digna stadig, men digna Data Reconciliation og digna
    MCP Server forbliver slået fra. Alle kommandoer, der kontrollerer licensen — `user`,
    `inspection`, `repo` — afbrydes, før de rører repositoryet, når kontrollen fejler. Bekræft
    den nye licens, før du går videre:

    ```bash
    ./digna license check
    ```

#### Trin 8: Opgrader repository-schemaet {: #step-8-upgrade-the-repository-schema }

Kør i din digna-installationsmappe:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 styrer repository-schemaet med versionerede migreringer. Den første opgradering fra
en tidligere release bringer schemaet til den sidste version i den tidligere ordning, registrerer den som
sit udgangspunkt og anvender derefter migreringerne fra Release 2026.11. Den afslutter med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle eksisterende data bevares. For at se repositoriets tilstand når som helst, kør
`./digna repo check`: den viser den senest anvendte migrering og eventuelle ventende.

!!! warning "digna starter ikke på et forældet repository"

    Fra Release 2026.11 nægter serveren at starte, så længe repositoriet kræver en opgradering, og
    siger det, for eksempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kør `repo upgrade`, før du starter serveren eller servicen.

#### Trin 9: Genstart services {: #step-9-restart-services }

Hvis du kører som systemd-service:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Hvis du kører manuelt, genstart serveren:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Hvis du bruger nginx eller Apache, genindlæs den respektive webserver:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

På RHEL-familien, genanvend SELinux-labeling, hvis `dashboard`-mappen blev udskiftet:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Trin 10: Bekræft opgraderingen {: #step-10-verify-the-upgrade }

1. Bekræft releasen af den nye eksekverbare fil:

    ```bash
    ./digna version
    ```

    Den første linje skal lyde `Release: 2026.11`.

2. Tilgå digna-dashboardet, og bekræft, at interfacet indlæses korrekt.
3. Tjek serverloggene for fejl:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Test dine databaseforbindelser — se
   [Test en forbindelse](../../../databases/overview.md#testing-a-connection). Efter en opgradering
   fra en release før 2026.06 skal du først lægge hver forbindelse, der ikke allerede brugte ODBC, om til
   ODBC.

For at komme i gang med de nye moduler, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Forbind en AI-agent](../../../platform/agentic/connect_ai_agent.md) for digna MCP Server og
[Profileringssted](../../../platform/profiling/profiling_location.md) for digna Engine.