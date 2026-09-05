---
title: Linuxinstallationsguide – digna Release 2026.06 | digna Dokumentation
description: Steg-för-steg-guide för installation av digna Release 2026.06 på Linux — systemkrav, PostgreSQL-inställning, nginx- eller Apache-konfiguration, backend- och dashboardkonfiguration, att köra digna som en systemd-tjänst och uppgradering till en ny release.
keywords: digna linux-installation, digna distributionsguide, digna backendkonfiguration, digna dashboardinstallation, postgresql linux, nginx linux, digna systemd-tjänst, digna uppgraderingsguide
image: /assets/logo_square.png
---

# Linux Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Senast uppdaterad:** 5 september 2026


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

- **dignabackend**: Applikationens kärnmotor, ansvarig för databehandling och kvalitetskontroller.
- **dignadashboard**: Ett webbaserat gränssnitt hostat på en webbserver som ger ett användarvänligt sätt att interagera med digna-plattformen och visualisera datakvalitets­mått.

### Nytt i Release 2026.06

Denna release för in dataobservability-funktioner direkt i din kod, vilket gör det möjligt för utvecklare att övervaka datakvalitet vid källan. Se [versionsanteckningarna](http://docs.digna.ai/changelog/Release_202606/) för fullständiga detaljer.

### Letar du efter Windows eller macOS?

Denna guide täcker Linux. För andra plattformar, se [Windows-installationsguide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) eller [macOS-installationsguide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — Konfigurationsfil
   - `license.toml` — Licensfil (kopiera din fil hit)

För att packa upp från shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

Denna sektion konfigurerar digna-backendens applikationsinställningar:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Värde | Noter |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adress | Värdnamn eller IP där dignabackend hostas |
| `digna_APP_PORT` | `8082` (standard) | Port för REST API-endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Om dashboarden ligger på annan server, lägg till dess URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krävs för CORS med credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillåt alla HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillåt alla headers |

!!! note "Obs"

    Om du serverar dashboarden från nginx eller Apache på standard HTTP-porten är origin att tillåta `http://localhost` — eller serverns publika URL när dashboarden nås från andra maskiner.

#### [repo] Sektionen

Denna sektion konfigurerar anslutningen till PostgreSQL-databasen:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Värde | Noter |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns host/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasnamn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schemat som skapades tidigare |
| `digna_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-uppsättningen |
| `digna_REPO_PASSWORD` | Ditt lösenord | Lösenord satt vid skapandet av schemat |

!!! tip "Bästa praxis"

    `config.toml` innehåller ett databaslösenord i klartext. Begränsa dess rättigheter så att endast servicekontot kan läsa den:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] Sektionen

Denna sektion innehåller säkerhets- och cookie-inställningar:

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

| Parameter | Värde | Noter |
|---|---|---|
| `digna_FERNET_KEY` | Krypteringsnyckel | Används för att kryptera tokens och cookies (standardnyckel medföljer) |
| `digna_COOKIE_DOMAIN` | `localhost` | Matcha din frontend-domän |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Använd `true` för HTTPS-anslutningar |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktiverat för säkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Hindrar CSRF-attacker |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Sessionstimeout i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal parallella inspektionsjobb |

!!! tip "Tips"

    För att ta reda på antal CPU-kärnor på din server, kör `nproc`.

#### [logging] Sektionen

Denna sektion konfigurerar loggningsbeteende:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Värde | Noter |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal dagliga loggbackup att behålla |

---

### Steg 2: Initiera repositoryt

1. Öppna en terminal
2. Navigera till din digna-installationskatalog (där `config.toml` och den körbara `digna` finns)
3. Kör anslutningstestet:

```bash
cd /opt/digna
./digna repo check
```

Du bör se en bekräftelse på att anslutningen upprättats (själva repositoryt har ännu inte initierats).

!!! note "Obs"

    På Linux ingår inte den aktuella katalogen i din PATH, så den körbara anropas som `./digna` istället för `digna`. För att använda den kortare formen överallt, lägg till en symbolisk länk:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Steg 3: Installera repositoryschemat

I samma katalog, kör:

```bash
./digna repo install
```

Detta kommando installerar nödvändiga tabeller och schema i din PostgreSQL-databas.

### Steg 4: Starta digna-servern

I digna-installationskatalogen, starta servern med:

```bash
./digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns hostnamn/IP
- `--port` — Serverns port

Du bör se startmeddelanden som bekräftar att servern körs:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tips"

    Om dashboarden serveras från en annan maskin än backend, öppna även API-porten i brandväggen:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Steg 5: Skapa en administratörsanvändare

1. Öppna ett **nytt** terminalfönster
2. Navigera till din digna-installationskatalog
3. Kör följande kommando för att skapa en administratörsanvändare:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Exempel:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Detta skapar en användare med användarnamn `admin` och fullständiga administrativa rättigheter.

!!! tip "Tips"

    Sätt lösenordet i enkla citationstecken. `bash` och `zsh` behandlar tecken som `!`, `$` och `*` speciellt, och ett oinramat lösenord som innehåller dem kommer inte att skickas korrekt.

!!! tip "Bästa praxis"

    Använd ett starkt lösenord med en blandning av versaler, gemener, siffror och specialtecken.

---

## Dashboardkonfiguration {: #dashboard-configuration }

### Steg 1: Distribuera dashboarden till webbservern

Digna-dashboarden har en separat `config.toml`-fil i `dashboard/`-katalogen. Denna konfiguration medföljer redan och kräver normalt inga ändringar under initial setup. Du behöver bara ändra den om du vill anpassa backend-anslutningen.

Om du behöver modifiera dashboardkonfigurationen (t.ex. för multi-instance-uppsättningar), se dashboardens dokumentation.

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

### Innan du uppgraderar

**Det är obligatoriskt att skapa en backup av digna-repositoryt**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

För att skapa en backup från shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Uppgraderingsprocess

#### Steg 1: Stoppa digna-tjänsten

Om digna körs som en systemd-tjänst, stoppa den först:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Om digna körs i förgrunden, tryck `Ctrl + C` i dess terminalfönster.

#### Steg 2: Backup av nuvarande backend-installation

I din digna-installationskatalog:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Steg 3: Packa upp och distribuera ny version

1. Packa upp den nya digna-installations-ZIP-filen
2. Kopiera den nya `digna`-körbaren och `dashboard`-mappen till din installationskatalog
3. Återställ körbarhetsbit och ägarskap för servicekontot:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Varning"

    Filen `config.toml` ingår **aldrig** i installations-ZIP:en. Din befintliga konfiguration är säker.

### Steg 4: Återställ dina konfigurationsfiler

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Steg 5: Uppgradera repositoryschemat

Navigera till din digna-installationskatalog och kör:

```bash
cd /opt/digna
./digna repo upgrade
```

Detta uppdaterar PostgreSQL-schemat till senaste versionen samtidigt som all befintlig data bevaras.

### Steg 6: Starta om tjänsterna

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

På RHEL-familjen, återapplicera SELinux-märkningen om `dashboard`-katalogen ersattes:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Steg 7: Verifiera uppgraderingen

1. Gå till digna-dashboarden
2. Verifiera att gränssnittet laddar korrekt
3. Kontrollera serverloggarna efter eventuella fel:

```bash
sudo journalctl -u digna -n 100
```