---
title: Windows installasjonsveiledning – digna Release 2026.06 | digna dokumentasjon
description: Trinnvis veiledning for å installere digna Release 2026.06 på Windows — systemkrav, PostgreSQL-oppsett, webserver-konfigurasjon, backend- og dashboard-konfigurasjon, kjøring av digna som Windows-tjeneste og oppgradering til ny utgave.
keywords: digna windows installasjon, digna deploy-veiledning, digna backend oppsett, digna dashboard installasjon, postgresql oppsett, digna windows service, digna oppgraderingsveiledning
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### About digna

digna er en omfattende AI-drevet plattform designet for å optimalisere styring av datakvalitet på tvers av ulike data-miljøer som warehouses, lakes og lakehouses. Bygget for høy skalerbarhet og fleksibilitet, adresserer digna moderne datautfordringer gjennom automatisering, sanntidsovervåking og anomalioppdagelse.

digna består av to hovedkomponenter:

- **dignabackend**: Applikasjonens kjerne, ansvarlig for databehandling og utføring av kvalitetskontroller.
- **dignadashboard**: Et nettbasert grensesnitt hostet på en webserver, som gir en brukervennlig måte å samhandle med digna-plattformen og visualisere datakvalitetsmetrikker.

### What's New in Release 2026.06

Denne utgivelsen bringer data-observability-funksjoner direkte inn i koden din, slik at utviklere kan overvåke datakvalitet ved kilden. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) for fullstendige detaljer.

---

## System Requirements {: #system-requirements }

Før du begynner installasjonen, sørg for at systemet ditt oppfyller følgende minimumskrav:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server eller Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB tilgjengelig lagringsplass |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Web Server** | IIS, Apache Tomcat, eller tilsvarende |

### Database Installation Options

**If PostgreSQL is already installed:**
Du kan legge til en ny database for digna i din eksisterende PostgreSQL-server.

**If installing PostgreSQL on the same machine as digna:**

> **⚠️ Recommended Specifications**
>
> - **Memory**: 32 GB RAM (i stedet for 16 GB)
> - **Disk Space**: 50 GB tilgjengelig lagringsplass (i stedet for 10 GB)
>
> Disse høyere spesifikasjonene gir rom for både digna og PostgreSQL-databasen som kjører samtidig.

---

## Pre-Installation Setup {: #pre-installation-setup }

Før du installerer digna, sørg for at to viktige forutsetninger er på plass:

1. **PostgreSQL Server** – for lagring av beregnede metrikker og ytelsesdata
2. **Web Server** – for hosting av digna Dashboard

Hvis disse komponentene ikke allerede er satt opp, følg seksjonene nedenfor for å installere og konfigurere dem.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Hvis PostgreSQL allerede er installert og kjører på din lokale maskin eller hvis du bruker en administrert ekstern PostgreSQL-server, kan du hoppe til [neste seksjon](#web-server-configuration).

### Installing PostgreSQL

Følg disse trinnene for å installere PostgreSQL på Windows:

#### Step 1: Download PostgreSQL

1. Besøk [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Velg **Windows**
3. Last ned nyeste installer

#### Step 2: Run the Installer

1. Dobbeltklikk på den nedlastede installer-filen
2. Følg instruksjonene i oppsettveiviseren

#### Step 3: Choose Installation Directory

Velg katalogen hvor PostgreSQL skal installeres. Standardplasseringen er vanligvis passende.

#### Step 4: Select Components

For en standardoppsett, behold standardvalg for komponenter.

#### Step 5: Set PostgreSQL Superuser Password

Angi og bekreft et passord for PostgreSQL-superbrukeren (`postgres`). **Lagre dette passordet sikkert** — du vil trenge det senere.

#### Step 6: Configure Port Number

Standard PostgreSQL-port er `5432`. Du kan bruke standarden eller spesifisere en annen port ved behov.

> **💡 Tip**
>
> Hvis port 5432 allerede er i bruk, velg en alternativ port og noter den for senere konfigurering.

#### Step 7: Choose Locale

Velg locale for databasen. Standard er vanligvis passende for de fleste installasjoner.

#### Step 8: Complete Installation

Klikk **Next** gjennom de resterende stegene, deretter **Finish**.

#### Step 9: Verify Installation

Åpne Command Prompt og verifiser at PostgreSQL er installert:

```bash
psql --version
```

Du bør se PostgreSQL-versjonen hvis installasjonen var vellykket.

---

## Web Server Configuration {: #web-server-configuration }

digna krever en webserver for å hoste dashboardet. Velg ett av følgende alternativer:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Du trenger kun å installere og konfigurere **én** av disse serverne.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) er Microsofts webserver for hosting av nettsteder og webapplikasjoner.

#### Enabling IIS

1. **Åpne Kontrollpanel**
   - Trykk `Win + R`
   - Skriv `control` og trykk Enter

2. **Gå til Windows-funksjoner**
   - Klikk **Programs**
   - Velg **Turn Windows features on or off**

3. **Aktiver Internet Information Services**
   - Rull ned og finn **Internet Information Services (IIS)**
   - Huk av for å aktivere den
   - Klikk **+** for å utvide og verifiser at disse underkomponentene er valgt:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klikk OK** for å anvende endringene

5. **Verifiser IIS-installasjon**
   - Åpne nettleseren
   - Gå til `http://localhost`
   - Du bør se IIS Welcome-siden

#### Required: URL Rewrite Module

IIS krever URL Rewrite-komponenten. Last den ned og installer fra [offisiell Microsoft-side](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Required: MIME Type for Markdown Files

For å sikre at Markdown-filer (`.md`) blir servert riktig av IIS:

1. Åpne **IIS Manager** (trykk `Win + R`, skriv `inetmgr`, trykk Enter)
2. Naviger til **Your Site > MIME Types**
3. Klikk **Add...**
4. Konfigurer:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **⚠️ Important**
>
> Uten denne innstillingen kan `.md`-filer bli servert feil.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat er en åpen kildekode Java servlet-container og webserver.

#### Installation

1. **Download Apache Tomcat**
   - Besøk [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Last ned Windows ZIP-distribusjonen

2. **Extract the Archive**
   - Pakk ut ZIP-filen til en katalog på systemet ditt
   - Eksempel: `C:\Program Files\Apache Tomcat`

3. **Verify Tomcat is Running**
   - Åpne nettleseren
   - Gå til `http://localhost:8080`
   - Du bør se Apache Tomcat velkomstsiden

> **💡 Tip**
>
> Apache Tomcat starter ofte automatisk etter installasjon. Hvis den ikke gjør det, naviger til `bin`-mappen og kjør `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

Digna-repositoriet lagrer alle metrikker beregnet av digna. Det fungerer som den sentrale databasen for analytiske og ytelsesdata.

#### Create Repository Schema and User

Åpne din PostgreSQL-klient (pgAdmin, psql eller lignende) og kjør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstatt følgende placholdere:**

- `<digna_repo_schema>` — Ønsket schemanavn (f.eks. `dignarepo`)
- `<digna_repo_user>` — Ønsket brukernavn (f.eks. `digna_user`)
- `<digna_repo_password>` — Et sikkert passord for denne brukeren

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **✅ Best Practice**
>
> Bruk sterke, komplekse passord for databasebrukere. Unngå lett gjetnbare legitimasjoner.

---

### Step 2: Extract the digna Installation Package

1. Finn digna-installasjons ZIP-filen som er levert til deg
2. Pakk den ut til ønsket installasjonssted
3. Etter uttrekking bør du se følgende elementer:
   - `dashboard/` — Web dashboard-grensesnitt
   - `digna` — Hovedkjørbar fil (backend + CLI kombinert)
   - `config.toml` — Konfigurasjonsfil
   - `license.toml` — Lisensfil (kopier din fil her)

### Step 3: Install the License File

> **⚠️ Important**
>
> Lisensfilen er **ikke** inkludert i installasjonspakken og vil bli levert separat av digna.

1. Finn `license.toml`-filen som er levert til deg
2. Kopier den til rotmappen for digna-installasjonen (der `config.toml` og kjørbar fil `digna` ligger)

**Hvorfor dette er viktig:**
Lisensfilen inneholder kundeinformasjon, lisensens utløpsdato og digital signatur. **Ikke endre denne filen** — eventuelle endringer vil ugyldiggjøre den.

**Katalogstruktur etter oppsett:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend Configuration {: #backend-configuration }

### Step 1: Create and Edit the Configuration File

Filen `config_template.toml` er levert i din digna-installasjonsmappe. Du trenger kun å gi den nytt navn til `config.toml`.

**Lokasjon:** `digna_installation/config.toml`

Åpne `config.toml` i en teksteditor og konfigurer hver seksjon nedenfor.

#### [app] Section

Denne seksjonen konfigurerer digna backend-applikasjonsinnstillinger:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adresse | Hostnavn eller IP hvor dignabackend er hostet |
| `digna_APP_PORT` | `8082` (default) | Port for REST API-endepunkter |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Hvis dashboardet ligger på en annen server, inkluder dens URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nødvendig for CORS med credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillat alle HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillat alle headere |

#### [repo] Section

Denne seksjonen konfigurerer tilkoblingen til PostgreSQL-databasen:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostnavn/IP |
| `digna_REPO_PORT` | `5432` (default) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasenavn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema opprettet tidligere |
| `digna_REPO_USER` | `digna_user` | Bruker opprettet i PostgreSQL-oppsettet |
| `digna_REPO_PASSWORD` | Ditt passord | Passord satt under schema-opprettelsen |

#### [base] Section

Denne seksjonen inneholder sikkerhets- og cookie-innstillinger:

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Krypteringsnøkkel | Brukes for å kryptere tokens og cookies (standard oppgitt) |
| `digna_COOKIE_DOMAIN` | `localhost` | Match ditt frontend-domene |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produksjon) | Bruk `true` for HTTPS-tilkoblinger |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktivert for sikkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Forhindrer CSRF-angrep |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antall CPU-kjerner - 1 | Antall parallelle inspeksjonsoppgaver |

#### [logging] Section

Denne seksjonen konfigurerer loggoppførsel:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` for produksjon, `DEBUG` for feilsøking |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antall dagsvise loggbackup som beholdes |

---

### Step 3: Initialize the Repository

1. Åpne Command Prompt
2. Naviger til din digna-installasjonskatalog (der `config.toml` og den kjørbare `digna` ligger)
3. Kjør forbindelsestesten:

```bash
digna repo check
```

Du bør se en bekreftelse på at tilkoblingen er etablert (selve repositoriet er ennå ikke initialisert).

### Step 4: Install the Repository Schema

I samme katalog, kjør:

```bash
digna repo install
```

Denne kommandoen installerer nødvendige tabeller og schema i din PostgreSQL-database.

### Step 5: Start the digna Server

I digna-installasjonskatalogen, start serveren med:

```bash
digna serve --address <host> --port <port>
```

**Parametere:**
- `--address` — Serverens hostname/IP
- `--port` — Serverport 

Du bør se oppstarts-meldinger som bekrefter at serveren kjører:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Step 6: Create an Admin User

1. Åpne et **nytt** Command Prompt-vindu
2. Naviger til din digna-installasjonskatalog
3. Kjør følgende kommando for å opprette en admin-bruker:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Eksempel:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Dette oppretter en bruker med full administrative rettigheter.

> **✅ Best Practice**
>
> Bruk et sterkt passord med en blanding av store og små bokstaver, tall og spesialtegn.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

Digna-dashboardet har sin egen separate `config.toml`-fil plassert i `dashboard/`-katalogen. Denne konfigurasjonen er allerede levert og krever vanligvis ikke endringer under initialt oppsett. Du trenger kun å konfigurere den hvis du må tilpasse backend-tilkoblingen.

Hvis du trenger å endre dashboard-konfigurasjonen (f.eks. for multi-instans distribusjoner), se dashboard-dokumentasjonen.

Velg din webserver og følg de tilhørende deploy-trinnene.

#### Deploying to IIS

1. **Åpne IIS Manager**
   - Trykk `Win + R`, skriv `inetmgr`, trykk Enter

2. **Opprett et nytt nettsted**
   - I venstre panel, høyreklikk **Sites**
   - Velg **Add Website...**

3. **Konfigurer nettstedet**
   - **Site Name**: Skriv inn et navn (f.eks. "dignaDashboard")
   - **Physical Path**: Klikk Browse og velg `dashboard`-mappen din
   - **Binding**: Sett IP-adresse og port (standard port 80 for HTTP, 443 for HTTPS)

4. **Start nettstedet**
   - Klikk **OK** for å opprette siden
   - Høyreklikk det nye nettstedet og velg **Start**

5. **Test installasjonen**
   - Åpne nettleseren
   - Gå til `http://localhost` (eller din konfigurerte URL)
   - Du bør se digna dashboard-login-siden

#### Deploying to Apache Tomcat

1. **Kopier dashboard til Tomcat**
   - Kopier `dashboard`-mappen til Tomcat `webapps`-katalogen
   - Gi den nytt navn om nødvendig (f.eks. til `digna`)
   - Eksempel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifiser deploy**
   - Oppdater eller last inn Tomcat management-siden på nytt (http://localhost:8080)
   - Du bør se "digna" (eller det valgte navnet) listet i deployerte applikasjoner

3. **Få tilgang til dashboardet**
   - Åpne nettleseren
   - Gå til `http://localhost:8080/digna`
   - Du bør se digna dashboard-login-siden

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

Å kjøre digna-backend som en Windows-tjeneste sikrer at den:
- Starter automatisk når serveren bootes
- Kjører i bakgrunnen uten et åpent Command Prompt-vindu
- Starter på nytt automatisk hvis den krasjer
- Kan administreres via Windows Services

### Service Management Files

Alle nødvendige filer ligger i digna-installasjonskatalogen under: `bin/`

Følgende batch-filer er tilgjengelige:
- `install_service.bat` — Registrerer digna som en Windows-tjeneste
- `uninstall_service.bat` — Avregistrerer tjenesten
- `start_service.bat` — Starter tjenesten
- `stop_service.bat` — Stopper tjenesten

> **⚠️ Administrator Required**
>
> Alle batch-filer må kjøres med Administrator-rettigheter.

### Installing the Service

1. **Åpne Command Prompt som Administrator**
   - Høyreklikk Command Prompt
   - Velg "Run as Administrator"

2. **Naviger til bin-mappen**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Kjør installasjonsskriptet**
   ```bash
   install_service.bat
   ```

Digna-serveren er nå registrert som en Windows-tjeneste med **automatisk oppstart** aktivert. Tjenesten starter ikke umiddelbart — se neste seksjon for å starte den.

### Starting and Stopping the Service

#### To Start the Service

1. Åpne Command Prompt som Administrator
2. Naviger til `digna\bin`
3. Kjør:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Åpne Command Prompt som Administrator
2. Naviger til `digna\bin`
3. Kjør:
   ```bash
   stop_service.bat
   ```

> **💡 Tip**
>
> Stopp alltid tjenesten før du oppdaterer applikasjonsfiler.

### Moving the Service to a New Directory

Hvis du må flytte digna-installasjonen:

1. **Avinstaller gjeldende tjeneste**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Flytt applikasjonsfilene**
   - Flytt hele digna-installasjonsmappen til det nye stedet

3. **Installer tjenesten på nytt**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start tjenesten**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Stopp den kjørende tjenesten**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Avinstaller tjenesten**
   ```bash
   uninstall_service.bat
   ```

Digna-serveren er nå avregistrert som en Windows-tjeneste.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Før du oppgraderer digna, ta sikkerhetskopi av repositoriet ditt (PostgreSQL) for å beskytte mot datatap.
En backup sikrer at du kan gjenopprette hvis oppgraderingen støter på uventede problemer.

### Upgrade Process

#### Step 1: Stop digna Service

Hvis digna kjører som en Windows-tjeneste, stopp den først:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Backup Current Backend Installation

I din digna-installasjonskatalog:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Pakk ut ny digna-installasjons ZIP-fil
2. Kopier den nye `digna`-kjørbare filen og `dashboard`-mappen til installasjonskatalogen


> **✅ Important**
>
> Filen `config.toml` er **aldri** inkludert i installasjons-ZIP-en. Din eksisterende konfigurasjon forblir trygg.

### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Step 5: Upgrade the Repository Schema

Naviger til din digna-installasjonskatalog og kjør:

```bash
digna repo upgrade
```

Dette oppdaterer PostgreSQL-schemat til siste versjon samtidig som alle eksisterende data bevares.

### Step 6: Restart Services

Hvis du kjører som Windows-tjeneste:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Hvis du kjører manuelt, start serveren på nytt:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Hvis du bruker IIS eller Tomcat, start den respektive webserveren på nytt.

#### Step 7: Verify the Upgrade

1. Gå til digna-dashboardet
2. Verifiser at grensesnittet laster riktig
3. Sjekk serverloggene for eventuelle feil