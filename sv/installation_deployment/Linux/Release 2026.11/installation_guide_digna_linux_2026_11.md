# Linux Installation Guide for digna Release 2026.11

**Release:** 2026.11

**Senast uppdaterad:** 7 november 2026


---

## Table of Contents

1. [Introduktion](#introduction)
2. [Systemkrav](#system-requirements)
3. [Förberedelser inför installation](#pre-installation-setup)
4. [PostgreSQL-serverinställning](#postgresql-server-setup)
5. [Webbserverkonfiguration](#web-server-configuration)
6. [Initial installation](#initial-installation)
7. [Backendkonfiguration](#backend-configuration)
8. [Dashboardkonfiguration](#dashboard-configuration)
9. [Köra digna som en systemd-tjänst](#running-digna-as-a-systemd-service)
10. [Uppgradering till en ny release](#upgrading-to-a-new-release)

---

## Introduktion {: #introduction }

### Om digna

digna är en omfattande AI-driven plattform utformad för att optimera hanteringen av datakvalitet i olika data­miljöer såsom warehouses, lakes och lakehouses. Byggd för hög skalbarhet och anpassningsbarhet adresserar digna moderna data­utmaningar genom automation, realtidsövervakning och anomali­detektion.

digna består av två huvudkomponenter:

- **digna**: applikationens kärna, ansvarig för att bearbeta data och utföra kvalitetskontroller. Den förenar backend och kommandoradsgränssnittet i en enda körbar fil och ersätter därmed de separata programmen `dignabackend` och `dignacli` från tidigare releaser.
- **dignadashboard**: Ett webbaserat gränssnitt hostat på en webbserver som ger ett användarvänligt sätt att interagera med digna-plattformen och visualisera datakvalitets­mått.

### Nytt i Release 2026.11

Denna release lägger till digna Data Reconciliation, digna Agentic med digna MCP Server samt digna Engine, som kan profilera data inuti digna och kontrollera referentiell integritet mellan olika databastekniker. Se [versionsanteckningarna](../../../changelog/Release_202611.md) för fullständiga detaljer.

För en installation medför releasen en ny mekanism för repositorymigreringar, en valfri `[duckdb]`-sektion i `config.toml` för digna Engine och en ny licensfil. [Uppgraderingsavsnittet](#upgrading-to-a-new-release) går igenom var och en av dem.

### Letar du efter Windows eller macOS?

Denna guide täcker Linux. För andra plattformar, se [Windows-installationsguide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) eller [macOS-installationsguide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Vilken distribution täcker guiden?

Instruktionerna är skrivna för de två vanligaste serverfamiljerna. Där de skiljer sig anges båda kommandon:

- **Debian-familjen** — Debian, Ubuntu. Paket­hanterare: `apt`.
- **RHEL-familjen** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Paket­hanterare: `dnf`.

Valfri modern distribution med `systemd` fungerar; det är främst paketnamnen och ett fåtal konfigurationsvägar som skiljer.

---

## Systemkrav {: #system-requirements }

Innan du börjar installationen, kontrollera att ditt system möter följande minimikrav:

| Krav | Specifikation |
|---|---|
| **Operativsystem** | Ubuntu 22.04 LTS eller senare, Debian 12 eller senare, RHEL 9 / Rocky 9 / AlmaLinux 9 eller senare |
| **Arkitektur** | x86_64 (amd64) eller arm64 |
| **Init-system** | systemd |
| **Minne (Minimalkonfiguration)** | 16 GB RAM |
| **Diskutrymme** | 10 GB tillgängligt lagringsutrymme |
| **Databas** | PostgreSQL Server 12 eller högre |
| **Webbserver** | nginx, Apache httpd eller motsvarande |

!!! info "digna Engine"

    Databasanslutningar som använder digna Engine som profileringsplats profileras på själva
    digna-värden. Planera för extra minne och diskutrymme för dem, se
    [\[duckdb\]-sektionen](#duckdb-section).

### Alternativ för databasinstallation

**Om PostgreSQL redan är installerat:**
Du kan lägga till en ny databas för digna på din befintliga PostgreSQL-server.

**Om du installerar PostgreSQL på samma maskin som digna:**

!!! info "Rekommenderade specifikationer"

    - **Minne**: 32 GB RAM (istället för 16 GB)
    - **Diskutrymme**: 50 GB tillgängligt lagringsutrymme (istället för 10 GB)

    Dessa högre specifikationer rymmer både digna och PostgreSQL-databasen som körs samtidigt.

### Kontrollera din distribution och arkitektur

Flera kommandon i denna guide skiljer sig mellan Debian- och RHEL-familjerna. För att se vilken du har, kör:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` eller `ID=debian` — använd `apt`-kommandona.
- `ID=rhel`, `rocky`, `almalinux` eller `fedora` — använd `dnf`-kommandona.
- `x86_64` eller `aarch64` — arkitekturen för det installationspaket du behöver.

---

## Förberedelser inför installation {: #pre-installation-setup }

Innan du installerar digna, säkerställ att två viktiga förutsättningar är på plats:

1. **PostgreSQL-server** – för att lagra beräknade mått och prestandadata
2. **Webbserver** – för att hosta digna Dashboard

Om dessa komponenter inte redan är uppsatta, följ avsnitten nedan för att installera och konfigurera dem.

### Uppdatera paketindexet

Uppdatera paketlistorna innan du installerar något:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Obs"

    I hela denna guide är det första kommandot i ett par för **Debian-familjen** och det andra för **RHEL-familjen**. Kör endast det kommando som matchar ditt system.

---

## PostgreSQL-serverinställning {: #postgresql-server-setup }

### Om du redan har PostgreSQL

Om PostgreSQL redan är installerat och körs lokalt eller om du använder en hanterad fjärr-PostgreSQL, kan du hoppa till nästa avsnitt: [Webbserverkonfiguration](#web-server-configuration).

### Installera PostgreSQL

#### Steg 1: Installera serverpaketet

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tips"

    Distributionspaket kan ligga efter i versionsnumret för PostgreSQL. Om du behöver en specifik nyare version, använd den officiella [PostgreSQL apt- eller yum-repositorien](https://www.postgresql.org/download/linux/) istället.

#### Steg 2: Initiera databas-klustret

På **Debian-familjen** skapar och startar paketet ett kluster automatiskt — hoppa till nästa steg.

På **RHEL-familjen** måste klustret skapas explicit:

```bash
sudo postgresql-setup --initdb
```

#### Steg 3: Starta och aktivera tjänsten

```bash
sudo systemctl enable --now postgresql
```

Detta startar PostgreSQL omedelbart och konfigurerar det att starta automatiskt vid uppstart.

#### Steg 4: Verifiera installationen

```bash
psql --version
sudo systemctl status postgresql
```

Du bör se PostgreSQL-versionen och en tjänst i status `active (running)`.

#### Steg 5: Anslut till servern

Ett Linuxpaket för PostgreSQL skapar ett systemkonto `postgres` som äger klustret. Anslut via det kontot:

```bash
sudo -u postgres psql
```

!!! note "Obs — Linux skiljer sig från Windows här"

    Windows-installationen ber dig att ange ett lösenord för superanvändaren `postgres` under installationen. Linuxpaket gör inte det. Istället autentiseras lokala anslutningar med **peer-autentisering**: operativsystemets användare `postgres` får ansluta som databasanvändaren `postgres` utan lösenord.

    Därför används kommandot ovan med `sudo -u postgres`. digna-backenden ansluter över TCP med användarnamn och lösenord, så du kommer att skapa en uttrycklig digna-användare i [Initial installation](#initial-installation).

#### Steg 6: Bekräfta porten

Standardporten för PostgreSQL är `5432`. För att bekräfta vilken port din server lyssnar på:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Notera värdet — du kommer att behöva det när du konfigurerar digna-backend.

#### Steg 7: Aktivera lösenordsautentisering för digna-användaren

digna ansluter till PostgreSQL över TCP som `digna_user`, vilket kräver lösenordsautentisering istället för peer-autentisering. Kontrollera att din `pg_hba.conf` tillåter detta.

Lokalisera filen:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Öppna den i en editor och se till att lokala TCP-rader använder `scram-sha-256` (eller `md5` på äldre servrar) istället för `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Ladda om PostgreSQL efter ändring:

```bash
sudo systemctl reload postgresql
```

!!! warning "Varning"

    Om digna rapporterar `FATAL: Ident authentication failed for user "digna_user"`, är denna inställning orsaken.

#### Steg 8: Om PostgreSQL körs på en annan maskin

För att acceptera anslutningar från en annan host, sätt `listen_addresses` i `postgresql.conf` och lägg till en matchande `host`-rad för ditt nätverk i `pg_hba.conf`:

```
listen_addresses = '*'
```

Öppna sedan porten i brandväggen och starta om tjänsten:

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

## Webbserverkonfiguration {: #web-server-configuration }

digna kräver en webbserver för att hosta dashboarden. Välj ett av följande alternativ:

- [nginx](#nginx-setup) — lättviktigt och rekommenderas
- [Apache httpd](#apache-setup) — ett ofta använt alternativ

Du behöver endast installera och konfigurera **en** av dessa servrar.

Båda avsnitten konfigurerar två saker som dashboarden är beroende av:

- **Fallback för single-page-applikationen**, så att en uppdatering av en dashboard-URL inte ger en 404
- **En `.md` MIME-typ**, så att Markdown-filer serveras korrekt

### nginx-inställning {: #nginx-setup }

#### Översikt

nginx är en lättviktig, högpresterande webbserver väl lämpad för att servera den statiska digna-dashboarden.

#### Installation

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Starta nginx

```bash
sudo systemctl enable --now nginx
```

#### Verifiera installationen

1. Öppna din webbläsare
2. Navigera till `http://localhost`
3. Du bör se nginx välkomstsida

#### Öppna brandväggen

Om servern nås från andra maskiner, tillåt HTTP-trafik:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Konfigurera en site för dashboarden

nginx inkluderar varje fil i sin `conf.d`-katalog på båda distributionsfamiljerna. Skapa en dedikerad konfigurationsfil för digna där:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Klistra in följande och ersätt `/opt/digna/dashboard` med den faktiska sökvägen till din uppackade `dashboard`-mapp:

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

!!! warning "Varning"

    Utan `try_files`-direktivet returnerar en omladdning av vilken dashboard-sida som helst utöver rot-URL:en en 404. Detta är nginx-ekvivalenten till URL Rewrite-modulen som krävs av IIS på Windows.

#### Inaktivera standard­sidan

Endast en serverblock kan vara `default_server` för en port. På **Debian-familjen**, ta bort det paketlevererade standardblocket så att det inte kolliderar:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

På **RHEL-familjen**, kommentera ut eller ta bort `server { ... }`-blocket i `/etc/nginx/nginx.conf`.

#### Tillämpa konfigurationen

Testa konfigurationen för syntaxfel, och ladda sedan om nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd-inställning {: #apache-setup }

#### Översikt

Apache httpd finns i standardförvaren för alla stödda distributioner. Paketet heter `apache2` i Debian-familjen och `httpd` i RHEL-familjen.

#### Installation

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Starta Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verifiera installationen

1. Öppna din webbläsare
2. Navigera till `http://localhost`
3. Du bör se distributionens standard Apache-sida

#### Obligatoriskt: Aktivera mod_rewrite

Dashboarden kräver URL-omskrivning.

På **Debian-familjen**, aktivera modulen och starta om:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

På **RHEL-familjen** laddas `mod_rewrite` som standard. Bekräfta det:

```bash
httpd -M | grep rewrite
```

#### Obligatoriskt: Tillåt .htaccess-överstyrningar

Öppna konfigurationsfilen för ditt dokumentrot:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Leta reda på `<Directory>`-blocket som täcker din dokumentrot (`/var/www/html` på båda familjerna) och ändra:

```apache
AllowOverride None
```

till:

```apache
AllowOverride All
```

#### Obligatoriskt: MIME-typ för Markdown-filer

I samma fil, lägg till följande rad så att Markdown-filer serveras korrekt:

```apache
AddType text/markdown .md
```

!!! warning "Varning"

    Utan denna inställning kanske `.md`-filer inte serveras korrekt.

#### Tillämpa konfigurationen

Kontrollera konfigurationen för syntaxfel, och starta sedan om Apache:

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

### Steg 1: Skapa digna-repositoryt

digna-repositoryt lagrar alla mått som digna beräknar. Det fungerar som central databas för analytiska och prestandamätningar.

#### Skapa schema och användare för repositoryt

Öppna din PostgreSQL-klient (psql, pgAdmin eller liknande) och kör följande SQL-kommandon:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Byt ut följande platshållare:**

- `<digna_repo_schema>` — Ditt önskade schemanamn (t.ex. `dignarepo`)
- `<digna_repo_user>` — Ditt önskade användarnamn (t.ex. `digna_user`)
- `<digna_repo_password>` — Ett säkert lösenord för denna användare

**Exempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

För att köra dessa från shell i ett steg:

```bash
sudo -u postgres psql
```

Klistra sedan in satserna vid prompten `postgres=#` och skriv `\q` för att avsluta.

!!! tip "Bästa praxis"

    Använd starka, komplexa lösenord för databas­användare. Undvik lättgissade inloggningar.

---

### Steg 2: Packa upp digna-installationspaketet

1. Hitta digna-installations-ZIP-filen som du fått
2. Packa upp den till din önskade installationsplats — till exempel `/opt/digna`
3. Efter uppackning bör du se följande objekt:
   - `dashboard/` — Webbgränssnittet
   - `digna` — Huvudkörbar fil (backend + CLI i ett)

!!! info "Konfigurations- och licensfilerna ingår inte i paketet"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` medföljer installationen — du
    skapar båda själv, i [Backendkonfiguration](#backend-configuration) och
    [Dashboardkonfiguration](#dashboard-configuration). Inte heller `license.toml` medföljer;
    digna levererar den separat, enligt beskrivningen i steg 3.

För att packa upp från shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Obs"

    Om `unzip` inte är installerat, lägg till det med `sudo apt install -y unzip` eller `sudo dnf install -y unzip`.

#### Gör den körbara filen körbar

Beroende på hur arkivet överfördes kan den körbara filens rättigheter ha förlorats. Sätt den uttryckligen:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Skapa ett servicekonto

Det rekommenderas att köra backend som en dedikerad oprivilegierad användare i produktionsmiljö:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Obs"

    På RHEL-familjen är motsvarande shellsökväg `/sbin/nologin`.

### Steg 3: Installera licensfilen

!!! warning "Varning"

    Licensfilen ingår **inte** i installationspaketet och kommer att tillhandahållas separat av digna.

1. Hitta `license.toml`-filen som du fått
2. Kopiera den till rotmappen för digna-installationen (där `config.toml` och den körbara `digna` finns)

**Varför detta är viktigt:**
Licensfilen innehåller din kundinformation, licensens utgångsdatum och en digital signatur. **Ändra inte denna fil** — ändringar gör att den ogiltigförklaras.

**Katalogstruktur efter installation:**

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

## Backendkonfiguration {: #backend-configuration }

### Steg 1: Skapa och redigera konfigurationsfilen

Filen `config_template.toml` medföljer din digna-installation. Du behöver bara byta namn på den till `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Plats:** `/opt/digna/config.toml`

Öppna `config.toml` i en texteditor och konfigurera varje sektion nedan.

#### [app] Sektionen

Denna sektion konfigurerar cross-origin resource sharing (CORS) mellan dashboarden och backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL:er | De URL:er som dashboarden serveras från. Webbläsarförfrågningar från alla andra origins avvisas |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krävs, så att webbläsaren skickar sessionscookien med varje förfrågan |

!!! note "Obs"

    Om du serverar dashboarden från nginx eller Apache på standard HTTP-porten är origin att tillåta `http://localhost` — eller serverns publika URL när dashboarden nås från andra maskiner.

!!! info "Sektionen [app] är valfri"

    Från Release 2026.11 kan båda nycklarna, och hela sektionen `[app]`, utelämnas. Det är rätt
    uppsättning när en omvänd proxy serverar dashboarden och backend under samma origin: webbläsaren
    gör då inga cross-origin-förfrågningar, och inga tillåts som standard.

#### [repo] Sektionen

Denna sektion konfigurerar anslutningen till PostgreSQL-databasen:

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

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns host/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasnamn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schemat som skapades tidigare |
| `DIGNA_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-uppsättningen |
| `DIGNA_REPO_PASSWORD` | Ditt lösenord | Lösenord satt vid skapandet av schemat |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valfri. SSL-läge för PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valfri. Antal anslutningar som digna håller öppna mot repositoryt |

!!! tip "Bästa praxis"

    `config.toml` innehåller ett databaslösenord i klartext. Begränsa dess rättigheter så att endast servicekontot kan läsa den:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] Sektionen

Denna sektion innehåller säkerhets-, cookie- och inspektionsinställningar:

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

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_FERNET_KEY` | Värdet som visas ovan | Nyckel för den kryptering som tidigare releaser använde. Den måste finnas; behåll det visade värdet |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Den värd som dashboarden nås under. `""` anger ingen domän, vilket är rätt bakom en proxy som serverar dashboarden och backend under samma origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Måste vara `true` när digna serveras över HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Håller sessionscookien utom räckhåll för skript |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Sessionstimeout i sekunder |
| `DIGNA_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal inspektioner som får köras samtidigt |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Obligatorisk. Används för länkarna i aviseringsmeddelanden, så det måste vara en URL som mottagarna kan öppna |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valfri. Antal sekunder som en enskild fråga mot en källdatabas får köras innan den avbryts; `0` stänger av tidsgränsen |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valfri. Antal sekunder att vänta på en anslutning till en källdatabas; `0` väntar obegränsat |

!!! tip "Tips"

    För att ta reda på antal CPU-kärnor på din server, kör `nproc`.

#### [encryption] Sektionen

Denna sektion innehåller nyckeln som används för att kryptera känsliga värden i repositoryt. Den är **obligatorisk** — `config check` rapporterar sektionen `[encryption]` som FAILED om nyckeln saknas.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodad nyckel | Krypterar känsliga värden som lagras i digna-repositoryt |

!!! warning "Skydda config.toml"

    Den här nyckeln är ett fast värde, identiskt i alla digna-installationer, och det är den som dekrypterar de känsliga värdena i ditt repository. Begränsa `config.toml` till det konto som kör digna, håll filen utanför versionshantering och delade enheter, och undanta den från varje säkerhetskopia som förvaras mindre säkert än repositoryt självt.

#### [logging] Sektionen

Denna sektion konfigurerar loggningsbeteende:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning. `TRACE`, `WARN` och `ERROR` accepteras också |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valfri. Katalog för de roterande loggfilerna, relativt arbetskatalogen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valfri. Antal roterade loggfiler som behålls |

#### [duckdb] Sektionen (valfri) {: #duckdb-section }

Nytt i Release 2026.11. Denna sektion anger resurserna för **digna Engine**, som profilerar
data inuti digna för databasanslutningar vars profileringsplats är **digna Engine**, och som kör
kontroller av referentiell integritet mellan datakällor på olika databasanslutningar. Se
[Profileringsplats](../../../platform/profiling/profiling_location.md).

Sektionen är valfri. Utan den gäller standardvärdena nedan.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Minne, i MB, som en körning av digna Engine får använda. Upp till `DIGNA_MAX_WORKERS` körningar kan vara aktiva samtidigt |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: systemets temporära katalog (`$TMPDIR`, eller `/tmp` om den inte är satt) | Katalog för temporära filer när data inte ryms i minnet |

!!! tip "Dimensionera digna Engine"

    Planera för upp till `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` minne på
    digna-värden, utöver det som digna själv använder, och för tillräckligt med ledigt diskutrymme i
    den temporära katalogen för att rymma det största inspekterade datumet bland de datakällor som
    använder digna Engine. Peka `DIGNA_DUCKDB_TEMP_DIRECTORY` mot en disk med det utrymmet, skrivbar
    för det konto som kör digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    Du behöver bara denna sektion om minst en databasanslutning använder digna Engine, eller om en
    kontroll av referentiell integritet jämför datakällor på olika anslutningar.

---

### Steg 2: Validera konfigurationen

Kontrollera att `config.toml` är fullständig och korrekt uppbyggd innan du initierar repositoryt. Kör i din digna-installationskatalog:

```bash
./digna config check
```

Varje sektion valideras för sig, så att ett enskilt fel inte döljer tillståndet hos de övriga:

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

Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter. En WARNING under **Unknown keys** listar nycklar i `config.toml` som digna inte läser; de har ingen effekt, så ta bort dem eller rätta stavningen. Den fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202611.md).

### Steg 3: Initiera repositoryt

1. Öppna en terminal
2. Navigera till din digna-installationskatalog (där `config.toml` och den körbara `digna` finns)
3. Kör anslutningstestet:

```bash
cd /opt/digna
./digna repo check
```

På ett nytt schema ansluter kommandot och rapporterar sedan att inget repository är installerat ännu:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Vid det här laget är det det förväntade resultatet: det bekräftar att digna når PostgreSQL och schemat. Ett anslutnings- eller autentiseringsfel pekar i stället på sektionen `[repo]` eller på PostgreSQL-uppsättningen.

!!! note "Obs"

    På Linux ingår inte den aktuella katalogen i din PATH, så den körbara anropas som `./digna` istället för `digna`. För att använda den kortare formen överallt, lägg till en symbolisk länk:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Steg 4: Installera repositoryschemat

I samma katalog, kör:

```bash
./digna repo upgrade
```

Detta kommando installerar nödvändiga tabeller i repositoryschemat och avslutas med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerar och uppgraderar"

    Från Release 2026.11 installerar `repo upgrade` ett nytt repository och uppgraderar ett befintligt.
    `repo install` fungerar fortfarande som ett annat namn för samma kommando.

### Steg 5: Skapa en administratörsanvändare

Administratörsanvändaren skapas direkt mot repositoryschemat, så servern behöver inte köras ännu. Kör i digna-installationskatalogen:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Exempel:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Detta skapar en användare med e-postadressen `admin@example.com` och fullständiga administratörsrättigheter.

!!! tip "Tips"

    Sätt lösenordet i enkla citationstecken. `bash` och `zsh` behandlar tecken som `!`, `$` och `*` speciellt, och ett oinramat lösenord som innehåller dem kommer inte att skickas korrekt.

!!! tip "Bästa praxis"

    Använd ett starkt lösenord med en blandning av versaler, gemener, siffror och specialtecken.

### Steg 6: Starta digna-servern

I digna-installationskatalogen, starta servern med:

```bash
./digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns hostnamn/IP (standard `127.0.0.1`)
- `--port` — Serverns port (standard `8000`)

När servern är igång skriver den ut adressen som den lyssnar på:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tips"

    Om dashboarden serveras från en annan maskin än backend, öppna även API-porten i brandväggen:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Servern upptar terminalen"

    `serve` körs i förgrunden och fortsätter tills du stoppar den med ++ctrl+c++. Låt den vara igång medan du slutför installationen; för att i stället starta den automatiskt vid uppstart, se [Köra digna som systemd-tjänst](#running-digna-as-a-systemd-service).

---

## Dashboardkonfiguration {: #dashboard-configuration }

### Steg 1: Distribuera dashboarden till webbservern

digna-dashboarden läser sin egen konfiguration från `dashboard/dashboard_config.toml`. Den filen medföljer inte installationen — du skapar den i katalogen `dashboard/` bredvid dashboardfilerna.

Dess innehåll beskrivs under [Enkel inloggning (SSO)](../../../sso/overview.md), som också är där filen behövs: den innehåller de inloggningsalternativ som dashboarden erbjuder och, vid uppsättningar med flera instanser, backend-anslutningen.

Välj din webbserver och följ motsvarande distributionssteg.

#### Distribuera till nginx

Om du följt [nginx-inställningen](#nginx-setup) pekar serverblocket redan mot din `dashboard`-mapp och ingen kopiering krävs.

1. **Bekräfta sökvägen**
   - Öppna `/etc/nginx/conf.d/digna.conf`
   - Verifiera att `root` pekar mot din uppackade `dashboard`-mapp

2. **Säkerställ att mappen är läsbar**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Ladda om nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Testa installationen**
   - Öppna din webbläsare
   - Navigera till `http://localhost` (eller din konfigurerade URL)
   - Du bör se inloggningssidan för digna-dashboarden

#### Distribuera till Apache httpd

1. **Kopiera dashboarden till dokumentroten**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Lägg till omskrivningsregler**

   Skapa en `.htaccess`-fil i den deployade mappen så att dashboard-routes överlever en webbläsaruppdatering:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Klistra in följande:

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

3. **Starta om Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Åtkomst till dashboarden**
   - Öppna din webbläsare
   - Navigera till `http://localhost/digna`
   - Du bör se inloggningssidan för digna-dashboarden

### Steg 2: SELinux (endast RHEL-familjen)

På RHEL, Rocky, AlmaLinux och Fedora är SELinux som standard i enforcing-läge och kommer att blockera webbservern från att läsa filer utanför förväntade platser. Kontrollera om det är aktivt:

```bash
getenforce
```

Om resultatet är `Enforcing` och du serverar dashboarden från `/opt/digna/dashboard`, märk katalogen så att webbservern får läsa den:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Obs"

    Om `semanage` inte finns, installera det med `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Varning"

    En dashboard som returnerar **403 Forbidden** på en nykonfigurerad RHEL-server är nästan alltid ett SELinux-märkningsproblem snarare än ett problem med filbehörigheter. Bekräfta med `sudo ausearch -m avc -ts recent`.

---

## Köra digna som en systemd-tjänst {: #running-digna-as-a-systemd-service }

### Varför köra digna som en tjänst?

Att köra digna-backenden som en systemd-tjänst säkerställer att den:

- Startar automatiskt när maskinen startas
- Körs i bakgrunden utan ett öppet terminalfönster
- Startas om automatiskt om den kraschar
- Kan hanteras via `systemctl`, standardverktyget för Linux-tjänster

### Tjänsthanteringsfiler

Alla nödvändiga filer finns i digna-installationskatalogen under: `bin/`

Följande shell-skript finns tillgängliga:

- `install_service.sh` — Registrerar digna med systemd
- `uninstall_service.sh` — Avregistrerar tjänsten
- `start_service.sh` — Startar den registrerade tjänsten
- `stop_service.sh` — Stoppar den körande tjänsten

!!! warning "Root-privilegier krävs"

    Alla skript måste köras med `sudo`, eftersom registrering av en tjänst som startar vid boot skriver en enhetsfil till `/etc/systemd/system`.

### Gör skripten körbara

Uppackning bevarar kanske inte exekveringsrättigheterna. Innan första användning:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Installera tjänsten

1. **Öppna en terminal**

2. **Gå till bin-mappen**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kör installationsskriptet**
   ```bash
   sudo ./install_service.sh
   ```

digna-servern är nu registrerad i systemd med **automatisk start** aktiverad. Tjänsten startar dock inte omedelbart — se nästa avsnitt för att starta den.

### Starta och stoppa tjänsten

#### För att starta tjänsten

1. Öppna en terminal
2. Navigera till `/opt/digna/bin`
3. Kör:
   ```bash
   sudo ./start_service.sh
   ```

#### För att stoppa tjänsten

1. Öppna en terminal
2. Navigera till `/opt/digna/bin`
3. Kör:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tips"

    Stoppa alltid tjänsten innan du uppdaterar applikationsfiler.

### Hantera tjänsten med systemctl

När den är registrerad kan tjänsten även kontrolleras med standard systemd-kommandon från valfri katalog:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verifiera tjänsten

För att bekräfta att tjänsten är registrerad och körs:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` betyder att tjänsten startar vid boot; `active` betyder att den körs nu.

### Visa tjänstens loggar

systemd fångar allt som backend skriver till konsolen. För att läsa dem:

```bash
sudo journalctl -u digna -n 100
```

För att följa loggen live medan du reproducerar ett problem:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tips"

    Detta är det snabbaste sättet att diagnostisera en tjänst som startar och omedelbart stannar. En repository-anslutningsfel eller en saknad `license.toml` rapporteras här.

### Flytta tjänsten till en ny katalog

Enhetsfilen lagrar den absoluta sökvägen till den körbara filen, så att flytta installationen kräver att tjänsten registreras om:

1. **Avinstallera den nuvarande tjänsten**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Flytta applikationsfilerna**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Installera om tjänsten**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Starta tjänsten**
   ```bash
   sudo ./start_service.sh
   ```

### Avinstallera tjänsten

1. **Stoppa den körande tjänsten**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Avinstallera tjänsten**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna-servern är nu avregistrerad från systemd.

---

## Uppgradering till en ny release {: #upgrading-to-a-new-release }

Detta avsnitt uppgraderar en installation av Release 2026.06 till Release 2026.11. Om din
installation är äldre, läs först [Uppgradera från en release före 2026.06](#upgrading-from-a-release-before-2026-06).

### Innan du uppgraderar

**Det är obligatoriskt att skapa en backup av digna-repositoryt**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

För att skapa en backup från shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Begär licensfilen för Release 2026.11**

Release 2026.11 kräver en ny `license.toml`. Begär den från digna-teamet innan du börjar, och
ha den redo för [steg 7](#step-7-replace-the-license-file).

### Uppgradera från en release före 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 medförde tre ändringar som fortfarande gäller när du uppgraderar en äldre installation
direkt till 2026.11:

- **Endast ODBC.** digna når varje källteknik via ODBC. Varje databasanslutning som ännu
  inte använder ODBC måste läggas om till ODBC efter uppgraderingen; det finns ingen automatisk
  konvertering. Installera ODBC-drivrutinerna på digna-värden i förväg, se
  [Installera ODBC-drivrutinen på digna-värden](../../../databases/overview.md#install-the-driver),
  och ha egenskaperna för varje anslutning redo från
  [teknikguiderna](../../../databases/overview.md#technology-guides). Databricks Legacy-anslutaren
  finns inte längre; flytta de anslutningarna till
  [Databricks](../../../databases/databricks_connector_guide.md)-anslutaren.
- **En körbar fil.** `dignabackend` och `dignacli` ersätts av den enda körbara filen `digna`,
  som förenar backend och CLI.
- **config.toml.** Sektionen `[encryption]` är obligatorisk, och `DIGNA_APP_HOST` och
  `DIGNA_APP_PORT` läses inte längre: servern hämtar sin adress och port från `digna serve`.
  Jämför din fil med [Backendkonfiguration](#backend-configuration).

Stegen nedan anger var en äldre installation behöver något annat. Repositoryuppgraderingen i
steg 8 för ett repository från vilken tidigare release som helst direkt till 2026.11.

### Uppgraderingsprocess

#### Steg 1: Stoppa digna-tjänsten {: #step-1-stop-the-digna-service }

Om digna körs som en systemd-tjänst, stoppa den först:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Om digna körs i förgrunden, tryck ++ctrl+c++ i dess terminalfönster.

#### Steg 2: Säkerhetskopiera nuvarande installation {: #step-2-backup-current-installation }

Byt namn på den körbara filen och dashboard-mappen i din nuvarande installation i
digna-installationskatalogen, så att den nya releasen kan distribueras vid sidan av dem:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Behåll `digna_old` tills du har verifierat uppgraderingen, och `dashboard_old` tills du har återställt
dina konfigurationsfiler från den (se steg 4). Därefter kan du ta bort båda.

!!! info "Uppgradera från en release före 2026.06"

    Byt namn på mapparna `dignabackend` och `dignacli` i stället för den körbara filen:
    `sudo mv dignabackend dignabackend_old` och `sudo mv dignacli dignacli_old`. Ingen av dem används av Release 2026.11.

#### Steg 3: Packa upp och distribuera ny version {: #step-3-extract-and-deploy-new-version }

1. Packa upp den nya digna-installations-ZIP-filen
2. Kopiera den nya körbara filen `digna` och mappen `dashboard` till din installationskatalog
3. Återställ exekveringsbiten och servicekontots ägarskap:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Varning"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` ingår någonsin i
    installations-ZIP:en — digna-teamet levererar aldrig någon av filerna. Din befintliga konfiguration
    påverkas därför inte av uppgraderingen, och kopiorna i de omdöpta `*_old`-mapparna är de
    enda du har.

#### Steg 4: Återställ dina konfigurationsfiler {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 kräver ingen ändring i `config.toml`: en fil som fungerar med Release 2026.06 fortsätter
att fungera. Två ändringar är valfria:

- Lägg till en [`[duckdb]`-sektion](#duckdb-section) om databasanslutningar ska använda digna Engine
  och dess standardvärden inte passar din värd.
- Utelämna sektionen `[app]` om en omvänd proxy serverar dashboarden och backend under samma
  origin.

!!! warning "Inställningar som digna inte läser"

    Tidigare versioner av denna guide visade några inställningar som digna inte läser. De har ingen
    effekt, och `config check` listar dem under **Unknown keys** i steg 6. Ta bort eller rätta
    dem:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` och
      `digna_LOGGING_BACKUP_COUNT` finns inte. Ta bort dem.
    - Inställningsnamn är skiftlägeskänsliga. digna läser `DIGNA_REPO_HOST`, inte `digna_REPO_HOST`.
      Skriv varje namn med versaler, som i [Backendkonfiguration](#backend-configuration).

!!! warning "Enkel inloggning: behåll [[oidc_clients]]"

    digna läser leverantörer för enkel inloggning som en lista med `[[oidc_clients]]`-poster, var och en
    med sin egen `DIGNA_OIDC_KEY`. Om du har ändrat dina leverantörer till `[oidc_clients.<key>]`-sektioner,
    som en tidigare version av denna guide visade, ändra tillbaka dem. `config check` rapporterar
    `OIDC config(s)` som FAILED så länge den formen används:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Upprepa posten för varje leverantör, och håll varje `DIGNA_OIDC_KEY` identisk med `key` i
    `dashboard_config.toml`. Endast installationer som använder enkel inloggning berörs.

#### Steg 5: Ladda om webbservern {: #step-5-reload-the-web-server }

Dashboarden är en uppsättning statiska filer, så din webbserver — och webbläsaren — kan fortfarande
leverera den tidigare versionen. Ladda om eller starta om den webbserver som är värd för mappen `dashboard`
och ladda sedan om sidan med en hård uppdatering (++ctrl+f5++).

#### Steg 6: Validera konfigurationen {: #step-6-validate-the-configuration }

Kontrollera att `config.toml` är fullständig innan du rör repositoryt:

```bash
./digna config check
```

Varje sektion måste rapportera OK. Åtgärda allt som rapporteras som FAILED, ta bort nycklarna som listas
under **Unknown keys** och kör kommandot igen innan du fortsätter.

#### Steg 7: Ersätt licensfilen {: #step-7-replace-the-license-file }

En licensfil följer normalt med från en release till nästa. Release 2026.11 är ett
undantag: den lägger till två licensierade moduler, digna Data Reconciliation och digna Agentic, och en
licens som utfärdats före 2026.11 innehåller dem inte. Kopiera den `license.toml` som digna-teamet
tillhandahållit för Release 2026.11 till installationskatalogen och ersätt den gamla:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Behåll inte den tidigare licensen"

    Med den tidigare licensen startar digna fortfarande, men digna Data Reconciliation och digna
    MCP Server förblir avstängda. Varje kommando som kontrollerar licensen — `user`,
    `inspection`, `repo` — avbryts innan det rör repositoryt när kontrollen misslyckas. Verifiera
    den nya licensen innan du går vidare:

    ```bash
    ./digna license check
    ```

#### Steg 8: Uppgradera repositoryschemat {: #step-8-upgrade-the-repository-schema }

Kör i din digna-installationskatalog:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 hanterar repositoryschemat med versionerade migreringar. Den första uppgraderingen från
en tidigare release för schemat till den sista versionen av det tidigare systemet, registrerar den som
utgångspunkt och tillämpar sedan migreringarna i Release 2026.11. Den avslutas med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

All befintlig data bevaras. För att när som helst se repositoryts tillstånd, kör
`./digna repo check`: det listar den senast tillämpade migreringen och eventuella väntande migreringar.

!!! warning "digna startar inte på ett föråldrat repository"

    Från Release 2026.11 vägrar servern att starta så länge repositoryt behöver uppgraderas, och
    säger det, till exempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kör `repo upgrade` innan du startar servern eller tjänsten.

#### Steg 9: Starta om tjänsterna {: #step-9-restart-services }

Om du kör som systemd-tjänst:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Om du kör manuellt, starta servern igen:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Om du använder nginx eller Apache, ladda om respektive webbserver:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

På RHEL-familjen, tillämpa SELinux-märkningen på nytt om katalogen `dashboard` ersattes:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Steg 10: Verifiera uppgraderingen {: #step-10-verify-the-upgrade }

1. Bekräfta releasen för den nya körbara filen:

    ```bash
    ./digna version
    ```

    Första raden måste vara `Release: 2026.11`.

2. Öppna digna-dashboarden och kontrollera att gränssnittet laddas korrekt.
3. Kontrollera serverloggarna efter fel:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Testa dina databasanslutningar — se
   [Testa en anslutning](../../../databases/overview.md#testing-a-connection). Efter en uppgradering
   från en release före 2026.06, lägg först om varje anslutning som inte redan använde ODBC till
   ODBC.

För att komma igång med de nya modulerna, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Ansluta en AI-agent](../../../platform/agentic/connect_ai_agent.md) för digna MCP Server och
[Profileringsplats](../../../platform/profiling/profiling_location.md) för digna Engine.