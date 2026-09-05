---
title: Windows-installationsvejledning – digna Release 2026.06 | digna-dokumentation
description: Trin-for-trin vejledning til installation af digna Release 2026.06 på Windows — systemkrav, PostgreSQL-opsætning, webserverkonfiguration, backend- og dashboard-konfiguration, kørsel af digna som Windows-service og opgradering til ny release.
keywords: digna Windows-installation, digna udrulningsvejledning, digna backend-opsætning, digna dashboard-installation, postgresql-opsætning, digna Windows-service, digna opgraderingsvejledning
image: /assets/logo_square.png
---

# Windows-installationsvejledning for digna Release 2026.06

**Release:** 2026.06

**Senest opdateret:** 30. august 2026


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
9. [Kørsel af digna som Windows-service](#running-digna-as-a-windows-service)
10. [Opgradering til en ny release](#upgrading-to-a-new-release)

---

## Introduktion {: #introduction }

### Om digna

digna er en omfattende AI-drevet platform designet til at optimere datakvalitetsstyring på tværs af forskellige data-miljøer såsom warehouses, lakes og lakehouses. Bygget til at være meget skalerbar og tilpasningsdygtig, adresserer digna moderne dataudfordringer gennem automatisering, realtidsmonitorering og anomalidetektion.

digna består af to hovedkomponenter:

- **dignabackend**: Applikationens kerneengine, ansvarlig for databehandling og udførelse af kvalitetskontroller.
- **dignadashboard**: Et webbaseret interface hostet på en webserver, som giver en brugervenlig måde at interagere med digna-platformen og visualisere datakvalitetsmålinger.

### Hvad er nyt i Release 2026.06

Denne release bringer dataobservabilitet direkte ind i din kode, hvilket gør det muligt for udviklere at overvåge datakvalitet ved kilden. Se [udgivelsesnoterne](http://docs.digna.ai/changelog/Release_202606/) for fulde detaljer.

### Leder du efter macOS eller Linux?

Denne vejledning dækker Windows. For andre platforme, se [macOS-installationsvejledningen](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) eller [Linux-installationsvejledningen](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemkrav {: #system-requirements }

Før du påbegynder installationen, skal du sikre dig, at dit system opfylder følgende minimumskrav:

| Krav | Specifikation |
|---|---|
| **Operativsystem** | Windows Server eller Windows 10/11 |
| **Hukommelse (minimal opsætning)** | 16 GB RAM |
| **Diskplads** | 10 GB ledig lagerplads |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Webserver** | IIS, Apache Tomcat eller tilsvarende |

### Databaseinstallationsmuligheder

**Hvis PostgreSQL allerede er installeret:**
Du kan oprette en ny database til digna på din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskine som digna:**

!!! info "Anbefalede specifikationer"

    - **Hukommelse**: 32 GB RAM (i stedet for 16 GB)
    - **Diskplads**: 50 GB ledig lagerplads (i stedet for 10 GB)

    Disse højere specifikationer tager højde for både digna og PostgreSQL-databasen, der kører samtidigt.

---

## Forberedende opsætning {: #pre-installation-setup }

Før du installerer digna, skal du sikre, at to nøgleforudsætninger er på plads:

1. **PostgreSQL Server** – til lagring af beregnede målinger og ydelsesdata
2. **Webserver** – til hosting af digna Dashboard

Hvis disse komponenter ikke allerede er sat op, følg afsnittene nedenfor for at installere og konfigurere dem.

---

## PostgreSQL-serveropsætning {: #postgresql-server-setup }

### Hvis du allerede har PostgreSQL

Hvis PostgreSQL allerede er installeret og kører på din lokale maskine, eller hvis du bruger en administreret fjern-PostgreSQL-server, kan du springe videre til [næste afsnit](#web-server-configuration).

### Installation af PostgreSQL

Følg disse trin for at installere PostgreSQL på Windows:

#### Trin 1: Download PostgreSQL

1. Besøg [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Vælg **Windows**
3. Download den nyeste installer

#### Trin 2: Kør installatøren

1. Dobbeltklik på den downloadede installerfil
2. Følg anvisningerne i installationsguiden

#### Trin 3: Vælg installationsmappe

Vælg den mappe, hvor PostgreSQL skal installeres. Standardplaceringen er som regel passende.

#### Trin 4: Vælg komponenter

For en standardopsætning beholdes de forvalgte komponenter.

#### Trin 5: Angiv PostgreSQL-superbrugerens adgangskode

Indtast og bekræft en adgangskode for PostgreSQL-superbrugeren (`postgres`). **Gem denne adgangskode sikkert** — du får brug for den senere.

#### Trin 6: Konfigurer portnummer

Standardporten for PostgreSQL er `5432`. Du kan bruge standarden eller angive en anden port efter behov.

!!! tip "Tip"

    Hvis port 5432 allerede er i brug, vælg en alternativ port og noter den til senere konfiguration.

#### Trin 7: Vælg lokalitet (locale)

Vælg lokalitet for din database. Standardindstillingen er som regel passende for de fleste installationer.

#### Trin 8: Afslut installation

Klik **Næste** gennem de resterende trin, og klik derefter **Finish**.

#### Trin 9: Bekræft installation

Åbn Kommandoprompt og verificer, at PostgreSQL er installeret:

```bash
psql --version
```

Du burde se PostgreSQL-versionen, hvis installationen var vellykket.

---

## Webserverkonfiguration {: #web-server-configuration }

digna kræver en webserver til at hoste dashboardet. Vælg en af følgende muligheder:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Du behøver kun at installere og konfigurere **én** af disse servere.

### IIS-opsætning {: #iis-setup }

#### Oversigt

Internet Information Services (IIS) er Microsofts webserver til hosting af websites og webapplikationer.

#### Aktivering af IIS

1. **Åbn Kontrolpanel**
   - Tryk `Win + R`
   - Skriv `control` og tryk Enter

2. **Gå til Windows-funktioner**
   - Klik **Programmer**
   - Vælg **Slå Windows-funktioner til eller fra**

3. **Aktivér Internet Information Services**
   - Rul ned og find **Internet Information Services (IIS)**
   - Sæt flueben for at aktivere det
   - Klik på **+** for at udvide og verificere, at disse underkomponenter er valgt:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klik OK** for at anvende ændringerne

5. **Bekræft IIS-installation**
   - Åbn din browser
   - Naviger til `http://localhost`
   - Du bør se IIS Velkomstsiden

#### Påkrævet: URL Rewrite-modulet

IIS kræver URL Rewrite-komponenten. Download og installer det fra [den officielle Microsoft-side](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Påkrævet: MIME-type for Markdown-filer

For at sikre, at Markdown-filer (`.md`) serveres korrekt af IIS:

1. Åbn **IIS Manager** (tryk `Win + R`, skriv `inetmgr`, tryk Enter)
2. Naviger til **Your Site > MIME Types**
3. Klik **Add...**
4. Konfigurer:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Vigtigt"

    Uden denne indstilling kan `.md`-filer muligvis ikke blive serveret korrekt.

---

### Apache Tomcat-opsætning {: #apache-tomcat-setup }

#### Oversigt

Apache Tomcat er en open-source Java servlet-container og webserver.

#### Installation

1. **Download Apache Tomcat**
   - Besøg [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Download Windows ZIP-distributionen

2. **Udpak arkivet**
   - Udpak ZIP-filen til en mappe på dit system
   - Eksempel: `C:\Program Files\Apache Tomcat`

3. **Bekræft, at Tomcat kører**
   - Åbn din browser
   - Naviger til `http://localhost:8080`
   - Du bør se Apache Tomcat velkomstsiden

!!! tip "Tip"

    Apache Tomcat starter typisk automatisk efter installation. Hvis det ikke gør, naviger til `bin`-mappen og kør `startup.bat`.

---

## Initial installation {: #initial-installation }

### Trin 1: Opret digna-repositoriet

Digna-repositoriet gemmer alle målinger beregnet af digna. Det fungerer som den centrale database for analytiske og ydelsesdata.

#### Opret repositorieschema og bruger

Åbn din PostgreSQL-klient (pgAdmin, psql eller lignende) og udfør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstat følgende pladsholdere:**

- `<digna_repo_schema>` — Dit ønskede schemanavn (f.eks. `dignarepo`)
- `<digna_repo_user>` — Dit ønskede brugernavn (f.eks. `digna_user`)
- `<digna_repo_password>` — Et sikkert password til denne bruger

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Bedste praksis"

    Brug stærke, komplekse adgangskoder til databasebrugere. Undgå let gættelige legitimationsoplysninger.

---

### Trin 2: Udpak digna-installationspakken

1. Find digna-installations-ZIP-filen, der er leveret til dig
2. Udpak den til det ønskede installationssted
3. Efter udpakning bør du se følgende elementer:
   - `dashboard/` — Webdashboard-interface
   - `digna` — Hoved-udførbar fil (backend + CLI kombineret)
   - `config.toml` — Konfigurationsfil
   - `license.toml` — License-fil (kopiér din fil hertil)

### Trin 3: Installer license-filen

!!! warning "Vigtigt"

    License-filen er **ikke** inkluderet i installationspakken og leveres separat af digna.

1. Find den `license.toml`-fil, der er leveret til dig
2. Kopiér den til roden af digna-installationsmappen (hvor `config.toml` og den `digna`-eksekverbare fil ligger)

**Hvorfor det er vigtigt:**
License-filen indeholder dine kundeoplysninger, licensens udløbsdato og digital signatur. **Rediger ikke denne fil** — ændringer vil ugyldiggøre den.

**Mappe struktur efter opsætning:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend-konfiguration {: #backend-configuration }

### Trin 1: Opret og rediger konfigurationsfilen

Filen `config_template.toml` er inkluderet i din digna-installationsmappe. Du skal blot omdøbe den til `config.toml`.

**Placering:** `digna_installation/config.toml`

Åbn `config.toml` i en teksteditor og konfigurer hver sektion nedenfor.

#### [app] Sektionen

Denne sektion konfigurerer digna backend-applikationens indstillinger:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adresse | Hostnavn eller IP hvor dignabackend er hostet |
| `digna_APP_PORT` | `8082` (standard) | Port for REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Hvis dashboardet ligger på en anden server, medtag dets URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrævet for CORS med legitimationsoplysninger |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillad alle HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillad alle headers |

#### [repo] Sektionen

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

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostnavn/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasenavn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema oprettet tidligere |
| `digna_REPO_USER` | `digna_user` | Bruger oprettet i PostgreSQL-opsætningen |
| `digna_REPO_PASSWORD` | Dit password | Password sat under schema-oprettelsen |

#### [base] Sektionen

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

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_FERNET_KEY` | Krypteringsnøgle | Bruges til at kryptere tokens og cookies (standard leveres) |
| `digna_COOKIE_DOMAIN` | `localhost` | Match dit frontend-domæne |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Brug `true` for HTTPS-forbindelser |
| `digna_COOKIE_HTTPONLY` | `true` | Altid aktiveret for sikkerhed |
| `digna_COOKIE_SAME_SITE` | `lax` | Forhindrer CSRF-angreb |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kerner - 1 | Antal parallelle inspektionsopgaver |

#### [logging] Sektionen

Denne sektion konfigurerer logningsadfærd:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` til produktion, `DEBUG` til fejlfinding |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal daglige log-backups, der gemmes |

---

### Trin 3: Initialiser repositoriet

1. Åbn Kommandoprompt
2. Skift til din digna-installationsmappe (hvor `config.toml` og den `digna`-eksekverbare fil ligger)
3. Kør forbindelsestesten:

```bash
digna repo check
```

Du bør se en bekræftelse på, at forbindelsen er etableret (selve repositoriet er endnu ikke initialiseret).

### Trin 4: Installer repository-schemaet

I samme mappe, kør:

```bash
digna repo install
```

Denne kommando installerer de nødvendige tabeller og schema i din PostgreSQL-database.

### Trin 5: Start digna-serveren

I digna-installationsmappen, start serveren med:

```bash
digna serve --address <host> --port <port>
```

**Parametre:**
- `--address` — Serverens hostnavn/IP
- `--port` — Serverens port 

Du bør se opstartsbeskeder, der bekræfter, at serveren kører:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Trin 6: Opret en admin-bruger

1. Åbn et **nyt** Kommandoprompt-vindue
2. Skift til din digna-installationsmappe
3. Kør følgende kommando for at oprette en admin-bruger:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Eksempel:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Dette opretter en bruger med fulde administrative rettigheder.

!!! tip "Bedste praksis"

    Brug en stærk adgangskode med en blanding af store og små bogstaver, tal og specialtegn.

---

## Dashboard-konfiguration {: #dashboard-configuration }

### Trin 1: Deploy dashboardet til webserveren

Digna-dashboardet har sin egen separate `config.toml`-fil placeret i `dashboard/`-mappen. Denne konfiguration er allerede leveret og kræver ikke ændringer under initial opsætning. Du behøver kun at konfigurere den, hvis du vil tilpasse backend-forbindelsen.

Hvis du skal modificere dashboard-konfigurationen (f.eks. ved multi-instance udrulninger), henvises til dashboardets dokumentation.

Vælg din webserver og følg de tilsvarende deployments-trin nedenfor.

#### Deploy til IIS

1. **Åbn IIS Manager**
   - Tryk `Win + R`, skriv `inetmgr`, tryk Enter

2. **Opret et nyt website**
   - I venstre panel, højreklik på **Sites**
   - Vælg **Add Website...**

3. **Konfigurer websitet**
   - **Site Name**: Indtast et navn (f.eks. "dignaDashboard")
   - **Physical Path**: Klik Browse og vælg din `dashboard`-mappe
   - **Binding**: Sæt IP-adresse og port (standard port 80 for HTTP, 443 for HTTPS)

4. **Start websitet**
   - Klik **OK** for at oprette sitet
   - Højreklik på det nye site og vælg **Start**

5. **Test installationen**
   - Åbn din browser
   - Naviger til `http://localhost` (eller din konfigurerede URL)
   - Du bør se digna-dashboardets login-side

#### Deploy til Apache Tomcat

1. **Kopier dashboard til Tomcat**
   - Kopiér `dashboard`-mappen til din Tomcat `webapps`-mappe
   - Omdøb den om nødvendigt (f.eks. til `digna`)
   - Eksempel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Bekræft deployment**
   - Opdater eller genindlæs Tomcat administrationssiden (http://localhost:8080)
   - Du bør se "digna" (eller dit valgte navn) listet under deployerede applikationer

3. **Adgang til dashboardet**
   - Åbn din browser
   - Naviger til `http://localhost:8080/digna`
   - Du bør se digna-dashboardets login-side

---

## Kørsel af digna som en Windows-service {: #running-digna-as-a-windows-service }

### Hvorfor bruge en Windows-service?

At køre digna-backend som en Windows-service sikrer, at den:
- Starter automatisk, når serveren booter
- Kører i baggrunden uden et åbent Kommandoprompt-vindue
- Genstarter automatisk, hvis den crasher
- Kan administreres via Windows Services

### Service-administrationsfiler

Alle nødvendige filer findes i digna-installationsmappens underkatalog: `bin/`

Følgende batch-filer er tilgængelige:
- `install_service.bat` — Registrerer digna som en Windows-service
- `uninstall_service.bat` — Fjerner service-registreringen
- `start_service.bat` — Starter servicen
- `stop_service.bat` — Stopper servicen

!!! warning "Administratorrettigheder kræves"

    Alle batch-filer skal køres med Administrator-privilegier.

### Installation af servicen

1. **Åbn Kommandoprompt som Administrator**
   - Højreklik på Kommandoprompt
   - Vælg "Kør som administrator"

2. **Skift til bin-mappen**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Kør installationsscriptet**
   ```bash
   install_service.bat
   ```

Digna-serveren er nu registreret som en Windows-service med **automatisk opstart** aktiveret. Servicen starter ikke umiddelbart — se næste afsnit for at starte den.

### Start og stop af servicen

#### For at starte servicen

1. Åbn Kommandoprompt som Administrator
2. Skift til `digna\bin`
3. Kør:
   ```bash
   start_service.bat
   ```

#### For at stoppe servicen

1. Åbn Kommandoprompt som Administrator
2. Skift til `digna\bin`
3. Kør:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    Stop altid servicen før opdatering af applikationsfiler.

### Flytning af servicen til en ny mappe

Hvis du skal flytte digna-installationen:

1. **Afinstaller den nuværende service**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Flyt applikationsfilerne**
   - Flyt hele digna-installationsmappen til den nye placering

3. **Geninstaller servicen**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start servicen**
   ```bash
   start_service.bat
   ```

### Afinstallation af servicen

1. **Stop den kørende service**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Afinstaller servicen**
   ```bash
   uninstall_service.bat
   ```

Digna-serveren er nu fjernet som en Windows-service.

---

## Opgradering til en ny release {: #upgrading-to-a-new-release }

### Før du opgraderer

**Det er obligatorisk at lave en backup af digna-repositoriet**

Før du opgraderer digna, skal du sikkerhedskopiere dit repository (PostgreSQL) for at beskytte imod datatab.
En backup sikrer, at du kan gendanne, hvis opgraderingen støder på uventede problemer.

### Opgraderingsproces

#### Trin 1: Stop digna-servicen

Hvis digna kører som Windows-service, stop den først:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Trin 2: Backup af nuværende backend-installation

I din digna-installationsmappe:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Trin 3: Udpak og deploy ny version

1. Udpak den nye digna-installations-ZIP-fil
2. Kopiér den nye `digna`-eksekverbare fil og `dashboard`-mappen til din installationsmappe


!!! warning "Vigtigt"

    `config.toml`-filen er **aldrig** inkluderet i installations-ZIP'en. Din eksisterende konfiguration forbliver bevaret.

### Trin 4: Gendan dine konfigurationsfiler

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Trin 5: Opgrader repository-schemaet

Naviger til din digna-installationsmappe og kør:

```bash
digna repo upgrade
```

Dette opdaterer PostgreSQL-schemaet til den nyeste version samtidig med, at alle eksisterende data bevares.

### Trin 6: Genstart services

Hvis du kører som Windows-service:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Hvis du kører manuelt, genstart serveren:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Hvis du bruger IIS eller Tomcat, genstart den pågældende webserver.

#### Trin 7: Bekræft opgraderingen

1. Åbn digna-dashboardet
2. Bekræft, at interfacet loader korrekt
3. Tjek serverens logfiler for eventuelle fejl