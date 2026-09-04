---
title: Windows Installation Guide – digna Release 2026.06 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.06 on Windows — system requirements, PostgreSQL setup, web server configuration, backend and dashboard configuration, running digna as a Windows service, and upgrading to a new release.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows-installationsvejledning for digna Release 2026.06

**Release:** 2026.06

**Sidst opdateret:** 30. august 2026


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

digna er en omfattende AI-drevet platform designet til at optimere datakvalitetsstyring på tværs af forskellige data-miljøer som warehouses, lakes og lakehouses. Bygget til at være meget skalerbar og tilpasningsdygtig, håndterer digna moderne dataudfordringer gennem automatisering, realtidsmonitorering og anomalidetektion.

digna består af to hovedkomponenter:

- **dignabackend**: Applikationens kerneengine, ansvarlig for databehandling og udførelse af kvalitetskontroller.
- **dignadashboard**: Et webbaseret interface hostet på en webserver, der giver en brugervenlig måde at interagere med digna-platformen og visualisere datakvalitetsmålinger.

### What's New in Release 2026.06

Denne release bringer dataobservability-muligheder direkte ind i din kode, så udviklere kan overvåge datakvalitet ved kilden. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) for fulde detaljer.

---

## System Requirements {: #system-requirements }

Før du begynder installationen, sørg for at dit system opfylder følgende minimumskrav:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server eller Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB ledig lagerplads |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Web Server** | IIS, Apache Tomcat eller tilsvarende |

### Database Installation Options

**Hvis PostgreSQL allerede er installeret:**
Du kan tilføje en ny database til digna på din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskine som digna:**

> **Anbefalede specifikationer**
>
> - **Memory**: 32 GB RAM (i stedet for 16 GB)
> - **Disk Space**: 50 GB ledig lagerplads (i stedet for 10 GB)
>
> Disse højere specifikationer rummer både digna og PostgreSQL-databasen, når de kører samtidigt.

---

## Pre-Installation Setup {: #pre-installation-setup }

Før du installerer digna, skal du sikre dig, at to vigtige forudsætninger er på plads:

1. **PostgreSQL Server** – til lagring af beregnede målinger og performance-data
2. **Web Server** – til hosting af digna Dashboard

Hvis disse komponenter ikke allerede er sat op, følg sektionerne nedenfor for at installere og konfigurere dem.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Hvis PostgreSQL allerede er installeret og kører på din lokale maskine, eller hvis du bruger en administreret fjern-PostgreSQL-server, kan du springe til [næste afsnit](#web-server-configuration).

### Installing PostgreSQL

Følg disse trin for at installere PostgreSQL på Windows:

#### Step 1: Download PostgreSQL

1. Besøg [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Vælg **Windows**
3. Download den nyeste installer

#### Step 2: Run the Installer

1. Dobbeltklik på den downloadede installationsfil
2. Følg vejledningen i setup-guiden

#### Step 3: Choose Installation Directory

Vælg den mappe, hvor PostgreSQL skal installeres. Standardplaceringen er normalt passende.

#### Step 4: Select Components

For en standardopsætning, behold de forvalgte komponentmuligheder.

#### Step 5: Set PostgreSQL Superuser Password

Indtast og bekræft en adgangskode for PostgreSQL-superbrugeren (`postgres`). **Gem denne adgangskode sikkert** — du får brug for den senere.

#### Step 6: Configure Port Number

Standard PostgreSQL-porten er `5432`. Du kan bruge standarden eller angive en anden port, hvis nødvendigt.

> **Tip**
>
> Hvis port 5432 allerede er i brug, vælg en alternativ port og bemærk den til senere konfiguration.

#### Step 7: Choose Locale

Vælg locale for din database. Standardindstillingen er normalt passende for de fleste installationer.

#### Step 8: Complete Installation

Klik **Next** gennem de resterende trin, og klik derefter **Finish**.

#### Step 9: Verify Installation

Åbn Kommandoprompt og verificer, at PostgreSQL er installeret:

```bash
psql --version
```

Du bør se PostgreSQL-versionen, hvis installationen lykkedes.

---

## Web Server Configuration {: #web-server-configuration }

digna kræver en webserver til at hoste dashboardet. Vælg en af følgende muligheder:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Du behøver kun at installere og konfigurere **én** af disse servere.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) er Microsofts webserver til hosting af websites og webapplikationer.

#### Enabling IIS

1. **Åbn Kontrolpanel**
   - Tryk `Win + R`
   - Skriv `control` og tryk Enter

2. **Gå til Windows-funktioner**
   - Klik **Programs**
   - Vælg **Turn Windows features on or off**

3. **Aktiver Internet Information Services**
   - Rul ned og find **Internet Information Services (IIS)**
   - Marker afkrydsningsfeltet for at aktivere det
   - Klik på **+** for at udvide og verificere, at disse underkomponenter er valgt:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klik OK** for at anvende ændringerne

5. **Verificer IIS-installation**
   - Åbn din browser
   - Naviger til `http://localhost`
   - Du bør se IIS Welcome-siden

#### Påkrævet: URL Rewrite Module

IIS kræver URL Rewrite-komponenten. Download og installer den fra [den officielle Microsoft-side](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Påkrævet: MIME Type for Markdown Files

For at sikre, at Markdown-filer (`.md`) serveres korrekt af IIS:

1. Åbn **IIS Manager** (tryk `Win + R`, skriv `inetmgr`, tryk Enter)
2. Naviger til **Your Site > MIME Types**
3. Klik **Add...**
4. Konfigurer:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **Vigtigt**
>
> Uden denne indstilling kan `.md` filer ikke blive serveret korrekt.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat er en open-source Java servlet-container og webserver.

#### Installation

1. **Download Apache Tomcat**
   - Besøg [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Download Windows ZIP-distributionen

2. **Udpak arkivet**
   - Udpak ZIP-filen til en mappe på dit system
   - Eksempel: `C:\Program Files\Apache Tomcat`

3. **Verificer at Tomcat kører**
   - Åbn din browser
   - Naviger til `http://localhost:8080`
   - Du bør se Apache Tomcat welcome-siden

> **Tip**
>
> Apache Tomcat starter typisk automatisk efter installation. Hvis den ikke gør, gå til `bin`-mappen og kør `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

Digna-repositoriet lagrer alle målinger beregnet af digna. Det fungerer som den centrale database for analytiske og performance-data.

#### Create Repository Schema and User

Åbn din PostgreSQL-klient (pgAdmin, psql eller lignende) og udfør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstat følgende pladsholdere:**

- `<digna_repo_schema>` — Dit ønskede schema-navn (f.eks. `dignarepo`)
- `<digna_repo_user>` — Dit ønskede brugernavn (f.eks. `digna_user`)
- `<digna_repo_password>` — En sikker adgangskode til denne bruger

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **Best Practice**
>
> Brug stærke, komplekse adgangskoder til databasebrugere. Undgå let gættelige legitimationsoplysninger.

---

### Step 2: Extract the digna Installation Package

1. Find den digna-installations ZIP-fil, du har fået
2. Udpak den til din ønskede installationsplacering
3. Efter udpakning bør du se følgende elementer:
   - `dashboard/` — Web dashboard interface
   - `digna` — Hovedeksekverbar (backend + CLI kombineret)
   - `config.toml` — Konfigurationsfil
   - `license.toml` — Licensfil (kopier din hertil)

### Step 3: Install the License File

> **Vigtigt**
>
> Licensfilen er **ikke** inkluderet i installationspakken og vil blive leveret separat af digna.

1. Find den `license.toml`-fil, der er leveret til dig
2. Kopiér den ind i root-mappen for digna-installationen (hvor `config.toml` og `digna`-eksekverbar er placeret)

**Hvorfor dette er vigtigt:**
Licensfilen indeholder dine kundeoplysninger, licensudløbsdato og digital signatur. **Ændr ikke denne fil** — alle ændringer vil ugyldiggøre den.

**Mappestruktur efter opsætning:**

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

Filen `config_template.toml` leveres i din digna-installationsmappe. Du skal kun omdøbe den til `config.toml`.

**Placering:** `digna_installation/config.toml`

Åbn `config.toml` i en teksteditor og konfigurer hver sektion nedenfor.

#### [app] Section

Denne sektion konfigurerer digna-backend applikationsindstillinger:

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
| `digna_APP_PORT` | `8082` (standard) | Port for REST API-endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Hvis dashboard er på en anden server, inkluder dens URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Kræves for CORS med legitimationsoplysninger |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillad alle HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillad alle headers |

#### [repo] Section

Denne sektion konfigurerer forbindelsen til PostgreSQL-databasen:

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
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostname/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasenavn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema oprettet tidligere |
| `digna_REPO_USER` | `digna_user` | Bruger oprettet i PostgreSQL-opsætningen |
| `digna_REPO_PASSWORD` | Din adgangskode | Adgangskode sat under schema-oprettelsen |

#### [base] Section

Denne sektion indeholder sikkerheds- og cookie-indstillinger:

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
| `digna_FERNET_KEY` | Krypteringsnøgle | Bruges til at kryptere tokens og cookies (standard leveret) |
| `digna_COOKIE_DOMAIN` | `localhost` | Skal matche dit frontend-domæne |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Brug `true` for HTTPS-forbindelser |
| `digna_COOKIE_HTTPONLY` | `true` | Altid aktiveret for sikkerhed |
| `digna_COOKIE_SAME_SITE` | `lax` | Forebygger CSRF-angreb |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kerner - 1 | Antal parallelle inspektionsopgaver |

#### [logging] Section

Denne sektion konfigurerer logningsadfærd:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` til produktion, `DEBUG` til fejlfinding |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal daglige log-backups der opbevares |

---

### Step 3: Initialize the Repository

1. Åbn Kommandoprompt
2. Naviger til din digna-installationsmappe (hvor `config.toml` og `digna`-eksekverbar er placeret)
3. Kør forbindelsestesten:

```bash
digna repo check
```

Du bør se en bekræftelse på, at forbindelsen er etableret (selve repositoriet er endnu ikke initialiseret).

### Step 4: Install the Repository Schema

I samme mappe, kør:

```bash
digna repo install
```

Denne kommando installerer de nødvendige tabeller og schema i din PostgreSQL-database.

### Step 5: Start the digna Server

I digna-installationsmappen, start serveren med:

```bash
digna serve --address <host> --port <port>
```

**Parametre:**
- `--address` — Server hostname/IP
- `--port` — Server port 

Du bør se opstartsmeldinger, der bekræfter, at serveren kører:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Step 6: Create an Admin User

1. Åbn et **nyt** Kommandoprompt-vindue
2. Naviger til din digna-installationsmappe
3. Kør følgende kommando for at oprette en admin-bruger:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Eksempel:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Dette opretter en bruger med fulde administrative rettigheder.

> **Best Practice**
>
> Brug en stærk adgangskode med en blanding af store og små bogstaver, tal og specialtegn.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

Digna-dashboardet har sin egen separate `config.toml`-fil placeret i `dashboard/`-mappen. Denne konfiguration leveres allerede og kræver ikke ændringer under den indledende opsætning. Du skal kun konfigurere den, hvis du har behov for at tilpasse backend-forbindelsen.

Hvis du har brug for at ændre dashboard-konfigurationen (f.eks. til multi-instance deployment), henvises til dashboardets dokumentation.

Vælg din webserver og følg de tilsvarende deploy-trin.

#### Deploying to IIS

1. **Åbn IIS Manager**
   - Tryk `Win + R`, skriv `inetmgr`, tryk Enter

2. **Opret et nyt website**
   - Højreklik på **Sites** i venstre panel
   - Vælg **Add Website...**

3. **Konfigurer sitet**
   - **Site Name**: Indtast et navn (f.eks. "dignaDashboard")
   - **Physical Path**: Klik Browse og vælg din `dashboard`-mappe
   - **Binding**: Sæt IP-adresse og port (standardport 80 for HTTP, 443 for HTTPS)

4. **Start sitet**
   - Klik **OK** for at oprette sitet
   - Højreklik på det nye site og vælg **Start**

5. **Test installationen**
   - Åbn din browser
   - Naviger til `http://localhost` (eller din konfigurerede URL)
   - Du bør se digna-dashboardets login-side

#### Deploying to Apache Tomcat

1. **Kopier dashboard til Tomcat**
   - Kopiér `dashboard`-mappen til din Tomcat `webapps`-mappe
   - Omdøb den om nødvendigt (f.eks. til `digna`)
   - Eksempel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verificer deployment**
   - Opdater eller genindlæs Tomcat management-siden (http://localhost:8080)
   - Du bør se "digna" (eller dit valgte navn) opført i de deployede applikationer

3. **Adgang til dashboardet**
   - Åbn din browser
   - Naviger til `http://localhost:8080/digna`
   - Du bør se digna-dashboardets login-side

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

At køre digna-backend som en Windows-tjeneste sikrer, at den:
- Starter automatisk, når serveren booter
- Kører i baggrunden uden et åbent Kommandoprompt-vindue
- Genstarter automatisk, hvis den crasher
- Kan administreres gennem Windows Services

### Service Management Files

Alle nødvendige filer ligger i digna-installationsmappen under: `bin/`

Følgende batch-filer er tilgængelige:
- `install_service.bat` — Registrerer digna som en Windows-tjeneste
- `uninstall_service.bat` — Afregistrerer tjenesten
- `start_service.bat` — Starter den registrerede tjeneste
- `stop_service.bat` — Stopper den registrerede tjeneste

> **Administrator påkrævet**
>
> Alle batch-filer skal køres med Administrator-rettigheder.

### Installing the Service

1. **Åbn Kommandoprompt som Administrator**
   - Højreklik på Kommandoprompt
   - Vælg "Kør som administrator"

2. **Naviger til bin-mappen**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Kør installationsscriptet**
   ```bash
   install_service.bat
   ```

Digna-serveren er nu registreret som en Windows-tjeneste med **automatisk opstart** aktiveret. Tjenesten starter ikke nødvendigvis med det samme — se næste sektion for at starte den.

### Starting and Stopping the Service

#### To Start the Service

1. Åbn Kommandoprompt som Administrator
2. Naviger til `digna\bin`
3. Kør:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Åbn Kommandoprompt som Administrator
2. Naviger til `digna\bin`
3. Kør:
   ```bash
   stop_service.bat
   ```

> **Tip**
>
> Stop altid tjenesten, før du opdaterer applikationsfiler.

### Moving the Service to a New Directory

Hvis du har brug for at flytte digna-installationen:

1. **Afinstaller den nuværende tjeneste**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Flyt applikationsfilerne**
   - Flyt hele digna-installationsmappen til den nye placering

3. **Geninstaller tjenesten**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start tjenesten**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Stop den kørende tjeneste**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Afinstaller tjenesten**
   ```bash
   uninstall_service.bat
   ```

Digna-serveren er nu afregistreret som en Windows-tjeneste.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Det er obligatorisk at lave en backup af digna Repository**

Før du opgraderer digna, sikkerhedskopier dit repository (PostgreSQL) for at beskytte mod datatab.
En backup sikrer, at du kan gendanne, hvis opgraderingen støder på uventede problemer.

### Upgrade Process

#### Step 1: Stop digna Service

Hvis digna kører som en Windows-tjeneste, stop den først:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Backup Current Backend Installation

I din digna-installationsmappe:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Udpak den nye digna-installations ZIP-fil
2. Kopiér den nye `digna`-eksekverbare og `dashboard`-mappen til din installationsmappe


> **Vigtigt**
>
> Filen `config.toml` medtages **aldrig** i installations-ZIP'en. Din eksisterende konfiguration forbliver sikker.

### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Step 5: Upgrade the Repository Schema

Naviger til din digna-installationsmappe og kør:

```bash
digna repo upgrade
```

Dette opdaterer PostgreSQL-schemaet til den nyeste version, samtidig med at alle eksisterende data bevares.

### Step 6: Restart Services

Hvis det kører som en Windows-tjeneste:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Hvis det køres manuelt, genstart serveren:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Hvis du bruger IIS eller Tomcat, genstart den respektive webserver.

#### Step 7: Verify the Upgrade

1. Gå til digna-dashboardet
2. Bekræft, at interfacet indlæses korrekt
3. Tjek serverlogfilerne for eventuelle fejl
