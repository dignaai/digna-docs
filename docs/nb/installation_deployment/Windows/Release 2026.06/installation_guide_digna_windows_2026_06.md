---
title: Windows installasjonsveiledning – digna Release 2026.06 | digna Dokumentasjon
description: Trinnvis veiledning for å installere digna Release 2026.06 på Windows — systemkrav, PostgreSQL-oppsett, webserverkonfigurasjon, backend- og dashboard-konfigurasjon, kjøring av digna som Windows-tjeneste og oppgradering til ny utgave.
keywords: digna windows installasjon, digna distribusjonsveiledning, digna backend-oppsett, digna dashboard installasjon, postgresql oppsett, digna windows-tjeneste, digna oppgraderingsveiledning
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** August 30, 2026


---

## Table of Contents

1. [Introduksjon](#introduction)
2. [Systemkrav](#system-requirements)
3. [Forberedelser før installasjon](#pre-installation-setup)
4. [PostgreSQL-serveroppsett](#postgresql-server-setup)
5. [Webserverkonfigurasjon](#web-server-configuration)
6. [Initial installasjon](#initial-installation)
7. [Backend-konfigurasjon](#backend-configuration)
8. [Dashboard-konfigurasjon](#dashboard-configuration)
9. [Kjøre digna som en Windows-tjeneste](#running-digna-as-a-windows-service)
10. [Oppgradering til ny utgave](#upgrading-to-a-new-release)

---

## Introduksjon {: #introduction }

### Om digna

digna er en omfattende AI-drevet plattform utviklet for å optimalisere styring av datakvalitet på tvers av ulike data-miljøer som warehouses, lakes og lakehouses. Bygget for høy skalerbarhet og tilpasning, adresserer digna moderne datautfordringer gjennom automatisering, sanntidsovervåking og anomali-deteksjon.

digna består av to hovedkomponenter:

- **dignabackend**: Kjernen i applikasjonen, ansvarlig for databehandling og kvalitetskontroller.
- **dignadashboard**: Et web-basert grensesnitt hostet på en webserver, som gir en brukervennlig måte å interagere med digna-plattformen og visualisere datakvalitetsmålinger.

### Hva er nytt i Release 2026.06

Denne utgaven bringer dataobservability-funksjonalitet direkte inn i koden din, slik at utviklere kan overvåke datakvalitet ved kilden. Se [utgivelsesnotatene](http://docs.digna.ai/changelog/Release_202606/) for fullstendige detaljer.

### Ser du etter macOS eller Linux?

Denne veiledningen dekker Windows. For andre plattformer, se [macOS installasjonsveiledning](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) eller [Linux installasjonsveiledning](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemkrav {: #system-requirements }

Før du begynner installasjonen, sørg for at systemet ditt møter følgende minimumskrav:

| Krav | Spesifikasjon |
|---|---|
| **Operativsystem** | Windows Server eller Windows 10/11 |
| **Minne (Minimal oppsett)** | 16 GB RAM |
| **Diskplass** | 10 GB tilgjengelig lagring |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Webserver** | IIS, Apache Tomcat eller tilsvarende |

### Databaseinstallasjonsvalg

**Hvis PostgreSQL allerede er installert:**
Du kan legge til en ny database for digna på din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskin som digna:**

!!! info "Anbefalte spesifikasjoner"

    - **Minne**: 32 GB RAM (i stedet for 16 GB)
    - **Diskplass**: 50 GB tilgjengelig lagring (i stedet for 10 GB)

    Disse høyere spesifikasjonene tar høyde for at både digna og PostgreSQL-databasen kjører samtidig.

---

## Forberedelser før installasjon {: #pre-installation-setup }

Før du installerer digna, sørg for at to viktige forutsetninger er på plass:

1. **PostgreSQL-server** – for lagring av beregnede målinger og ytelsesdata
2. **Webserver** – for hosting av digna Dashboard

Hvis disse komponentene ikke allerede er satt opp, følg avsnittene nedenfor for å installere og konfigurere dem.

---

## PostgreSQL-serveroppsett {: #postgresql-server-setup }

### Hvis du allerede har PostgreSQL

Hvis PostgreSQL allerede er installert og kjører på din lokale maskin, eller hvis du bruker en administrert fjern-PostgreSQL-server, kan du hoppe videre til [neste avsnitt](#web-server-configuration).

### Installere PostgreSQL

Følg disse trinnene for å installere PostgreSQL på Windows:

#### Trinn 1: Last ned PostgreSQL

1. Besøk [PostgreSQL-nedlastingssiden](https://www.postgresql.org/download/)
2. Velg **Windows**
3. Last ned den nyeste installasjonsfilen

#### Trinn 2: Kjør installasjonsprogrammet

1. Dobbeltklikk på den nedlastede installasjonsfilen
2. Følg instruksjonene i oppsettveiviseren

#### Trinn 3: Velg installasjonsmappe

Velg katalogen hvor PostgreSQL skal installeres. Standardplasseringen er normalt passende.

#### Trinn 4: Velg komponenter

For et standardoppsett, behold standard komponentvalg.

#### Trinn 5: Angi PostgreSQL-superbrukerpassord

Skriv inn og bekreft et passord for PostgreSQL-superbrukeren (`postgres`). **Lagre dette passordet sikkert** — du vil trenge det senere.

#### Trinn 6: Konfigurer portnummer

Standard PostgreSQL-port er `5432`. Du kan bruke standard eller angi en annen port om nødvendig.

!!! tip "Tips"

    Hvis port 5432 allerede er i bruk, velg en alternativ port og noter den for senere konfigurasjon.

#### Trinn 7: Velg locale

Velg locale for databasen. Standard er vanligvis egnet for de fleste installasjoner.

#### Trinn 8: Fullfør installasjonen

Klikk **Next** gjennom de gjenværende trinnene, og klikk deretter **Finish**.

#### Trinn 9: Verifiser installasjonen

Åpne Kommandoprompt og verifiser at PostgreSQL er installert:

```bash
psql --version
```

Du bør se PostgreSQL-versjonen dersom installasjonen var vellykket.

---

## Webserverkonfigurasjon {: #web-server-configuration }

digna krever en webserver for å hoste dashboardet. Velg ett av følgende alternativer:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Du trenger bare å installere og konfigurere **én** av disse serverne.

### IIS-oppsett {: #iis-setup }

#### Oversikt

Internet Information Services (IIS) er Microsofts webserver for hosting av nettsteder og webapplikasjoner.

#### Aktivere IIS

1. **Åpne Kontrollpanel**
   - Trykk `Win + R`
   - Skriv `control` og trykk Enter

2. **Gå til Windows-funksjoner**
   - Klikk **Programs**
   - Velg **Turn Windows features on or off**

3. **Aktiver Internet Information Services**
   - Bla ned og finn **Internet Information Services (IIS)**
   - Kryss av for å aktivere den
   - Klikk på **+** for å utvide og verifiser at disse underkomponentene er valgt:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klikk OK** for å anvende endringene

5. **Verifiser IIS-installasjonen**
   - Åpne nettleseren din
   - Naviger til `http://localhost`
   - Du skal se IIS velkomstside

#### Påkrevd: URL Rewrite-modul

IIS krever URL Rewrite-komponenten. Last ned og installer den fra [Microsofts offisielle side](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Påkrevd: MIME-type for Markdown-filer

For å sikre at Markdown-filer (`.md`) blir servert riktig av IIS:

1. Åpne **IIS Manager** (trykk `Win + R`, skriv `inetmgr`, trykk Enter)
2. Naviger til **Your Site > MIME Types**
3. Klikk **Add...**
4. Konfigurer:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Viktig"

    Uten denne innstillingen kan `.md`-filer bli servert feil.

---

### Apache Tomcat-oppsett {: #apache-tomcat-setup }

#### Oversikt

Apache Tomcat er en åpen kildekode Java servlet-container og webserver.

#### Installasjon

1. **Last ned Apache Tomcat**
   - Besøk [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Last ned Windows ZIP-distribusjonen

2. **Pakk ut arkivet**
   - Pakk ut ZIP-filen til en katalog på systemet ditt
   - Eksempel: `C:\Program Files\Apache Tomcat`

3. **Verifiser at Tomcat kjører**
   - Åpne nettleseren din
   - Naviger til `http://localhost:8080`
   - Du skal se Apache Tomcat velkomstside

!!! tip "Tips"

    Apache Tomcat starter vanligvis automatisk etter installasjon. Hvis den ikke gjør det, gå til `bin`-mappen og kjør `startup.bat`.

---

## Initial installasjon {: #initial-installation }

### Trinn 1: Sett opp digna-repositoriet

digna-repositoriet lagrer alle målinger beregnet av digna. Det fungerer som den sentrale databasen for analytiske og ytelsesrelaterte data.

#### Opprett repositories-skjema og bruker

Åpne din PostgreSQL-klient (pgAdmin, psql eller lignende) og kjør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstatt følgende plassholdere:**

- `<digna_repo_schema>` — Navnet på ønsket skjema (f.eks. `dignarepo`)
- `<digna_repo_user>` — Ønsket brukernavn (f.eks. `digna_user`)
- `<digna_repo_password>` — Et sikkert passord for denne brukeren

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Beste praksis"

    Bruk sterke, komplekse passord for databasebrukere. Unngå lett gjettbare påloggingsopplysninger.

---

### Trinn 2: Pakk ut digna-installasjonspakken

1. Finn digna-installasjons-ZIP-filen som er levert til deg
2. Pakk den ut til ønsket installasjonssted
3. Etter utpakking skal du se følgende elementer:
   - `dashboard/` — Web dashboard-grensesnitt
   - `digna` — Hovedkjørbar fil (backend + CLI kombinert)
   - `config.toml` — Konfigurasjonsfil
   - `license.toml` — Lisensfil (kopier din her)

### Trinn 3: Installer lisensfilen

!!! warning "Viktig"

    Lisensfilen er **ikke** inkludert i installasjonspakken og vil bli levert separat av digna.

1. Finn `license.toml`-filen som er levert til deg
2. Kopier den inn i rotmappen for digna-installasjonen (der `config.toml` og `digna`-kjørbar ligger)

**Hvorfor dette er viktig:**
Lisensfilen inneholder kundeinformasjon, lisensens utløpsdato og digital signatur. **Ikke endre denne filen** — eventuelle endringer vil gjøre den ugyldig.

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

## Backend-konfigurasjon {: #backend-configuration }

### Trinn 1: Opprett og rediger konfigurasjonsfilen

Filen `config_template.toml` leveres i din digna-installasjonsmappe. Du trenger kun å gi den nytt navn til `config.toml`.

**Plassering:** `digna_installation/config.toml`

Åpne `config.toml` i en teksteditor og konfigurer hver seksjon nedenfor.

#### [app] Seksjonen

Denne seksjonen konfigurerer innstillingene for digna-backend-applikasjonen:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Verdi | Merknader |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adresse | Hostnavn eller IP hvor dignabackend er hostet |
| `digna_APP_PORT` | `8082` (standard) | Port for REST API-endepunkter |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Hvis dashboardet er på en annen server, inkluder dens URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrevet for CORS med credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillat alle HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillat alle headere |

#### [repo] Seksjonen

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

| Parameter | Verdi | Merknader |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostnavn/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasenavn |
| `digna_REPO_SCHEMA` | `dignarepo` | Skjema opprettet tidligere |
| `digna_REPO_USER` | `digna_user` | Bruker opprettet i PostgreSQL-oppsettet |
| `digna_REPO_PASSWORD` | Ditt passord | Passord satt under skjemaopprettelsen |

#### [base] Seksjonen

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

| Parameter | Verdi | Merknader |
|---|---|---|
| `digna_FERNET_KEY` | Krypteringsnøkkel | Brukes for å kryptere tokens og cookies (standard levert) |
| `digna_COOKIE_DOMAIN` | `localhost` | Match ditt frontend-domene |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produksjon) | Bruk `true` for HTTPS-tilkoblinger |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktivert for sikkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Forhindrer CSRF-angrep |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antall CPU-kjerner - 1 | Antall parallelle inspeksjonsoppgaver |

#### [logging] Seksjonen

Denne seksjonen konfigurerer loggeadferd:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Verdi | Merknader |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` for produksjon, `DEBUG` for feilsøking |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antall daglige logg-backup som beholdes |

---

### Trinn 3: Initialiser repositoriet

1. Åpne Kommandoprompt
2. Naviger til din digna-installasjonsmappe (der `config.toml` og `digna`-kjørbar ligger)
3. Kjør tilkoblingstesten:

```bash
digna repo check
```

Du skal se en bekreftelse på at tilkoblingen er opprettet (selve repositoriet er ennå ikke initialisert).

### Trinn 4: Installer repositories-skjemaet

I samme mappe, kjør:

```bash
digna repo install
```

Denne kommandoen installerer nødvendige tabeller og skjema i din PostgreSQL-database.

### Trinn 5: Start digna-serveren

I digna-installasjonsmappen, start serveren med:

```bash
digna serve --address <host> --port <port>
```

**Parametere:**
- `--address` — Serverens hostnavn/IP
- `--port` — Serverens port 

Du bør se oppstartsmeldinger som bekrefter at serveren kjører:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Trinn 6: Opprett en adminbruker

1. Åpne et **nytt** Kommandoprompt-vindu
2. Naviger til din digna-installasjonsmappe
3. Kjør følgende kommando for å opprette en adminbruker:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Eksempel:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Dette oppretter en bruker med full administrative rettigheter.

!!! tip "Beste praksis"

    Bruk et sterkt passord med en blanding av store og små bokstaver, tall og spesialtegn.

---

## Dashboard-konfigurasjon {: #dashboard-configuration }

### Trinn 1: Deploy dashboardet til webserveren

digna-dashboardet har sin egen separate `config.toml`-fil plassert i `dashboard/`-katalogen. Denne konfigurasjonen er allerede levert og krever normalt ikke endringer under initialt oppsett. Du trenger bare å konfigurere den hvis du må tilpasse backend-tilkoblingen.

Hvis du trenger å endre dashboard-konfigurasjonen (f.eks. for multi-instans-deployments), se dokumentasjonen for dashboardet.

Velg webserver og følg de tilsvarende deploy-trinnene.

#### Deploy til IIS

1. **Åpne IIS Manager**
   - Trykk `Win + R`, skriv `inetmgr`, trykk Enter

2. **Opprett et nytt nettsted**
   - I venstre panel, høyreklikk **Sites**
   - Velg **Add Website...**

3. **Konfigurer nettstedet**
   - **Site Name**: Skriv inn et navn (f.eks. "dignaDashboard")
   - **Physical Path**: Klikk Browse og velg din `dashboard`-mappe
   - **Binding**: Sett IP-adresse og port (standard port 80 for HTTP, 443 for HTTPS)

4. **Start nettstedet**
   - Klikk **OK** for å opprette siden
   - Høyreklikk det nye nettstedet og velg **Start**

5. **Test installasjonen**
   - Åpne nettleseren din
   - Naviger til `http://localhost` (eller din konfigurerte URL)
   - Du skal se påloggingssiden for digna-dashboardet

#### Deploy til Apache Tomcat

1. **Kopier dashboard til Tomcat**
   - Kopier `dashboard`-mappen til Tomcat sin `webapps`-katalog
   - Gi den nytt navn om nødvendig (f.eks. til `digna`)
   - Eksempel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifiser deploy**
   - Oppdater eller last inn Tomcat-administrasjonssiden på nytt (http://localhost:8080)
   - Du skal se "digna" (eller det navnet du valgte) listet blant deployerte applikasjoner

3. **Tilgang til dashboardet**
   - Åpne nettleseren din
   - Naviger til `http://localhost:8080/digna`
   - Du skal se påloggingssiden for digna-dashboardet

---

## Kjøre digna som en Windows-tjeneste {: #running-digna-as-a-windows-service }

### Hvorfor bruke en Windows-tjeneste?

Å kjøre digna-backend som en Windows-tjeneste sikrer at den:
- Starter automatisk ved serveroppstart
- Kjører i bakgrunnen uten et åpent Kommandoprompt-vindu
- Starter på nytt automatisk hvis den krasjer
- Kan administreres gjennom Windows Services

### Filer for tjenesteadministrasjon

Alle nødvendige filer ligger i digna-installasjonskatalogen under: `bin/`

Følgende batchfiler er tilgjengelige:
- `install_service.bat` — Registrerer digna som en Windows-tjeneste
- `uninstall_service.bat` — Avregistrerer tjenesten
- `start_service.bat` — Starter tjenesten
- `stop_service.bat` — Stopper tjenesten

!!! warning "Administrator påkrevd"

    Alle batchfiler må kjøres med Administrator-rettigheter.

### Installere tjenesten

1. **Åpne Kommandoprompt som administrator**
   - Høyreklikk Kommandoprompt
   - Velg "Run as Administrator"

2. **Naviger til bin-mappen**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Kjør installasjonsskriptet**
   ```bash
   install_service.bat
   ```

digna-serveren er nå registrert som en Windows-tjeneste med **automatisk oppstart** aktivert. Tjenesten starter ikke umiddelbart — se neste seksjon for å starte den.

### Starte og stoppe tjenesten

#### For å starte tjenesten

1. Åpne Kommandoprompt som administrator
2. Naviger til `digna\bin`
3. Kjør:
   ```bash
   start_service.bat
   ```

#### For å stoppe tjenesten

1. Åpne Kommandoprompt som administrator
2. Naviger til `digna\bin`
3. Kjør:
   ```bash
   stop_service.bat
   ```

!!! tip "Tips"

    Stopp alltid tjenesten før du oppdaterer applikasjonsfiler.

### Flytte tjenesten til en ny katalog

Hvis du trenger å flytte digna-installasjonen:

1. **Avinstaller den nåværende tjenesten**
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

### Avinstallere tjenesten

1. **Stopp tjenesten som kjører**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Avinstaller tjenesten**
   ```bash
   uninstall_service.bat
   ```

digna-serveren er nå avregistrert som en Windows-tjeneste.

---

## Oppgradering til ny utgave {: #upgrading-to-a-new-release }

### Før du oppgraderer

**Å ta backup av digna-repositoriet er obligatorisk**

Før du oppgraderer digna, ta sikkerhetskopi av ditt repositorium (PostgreSQL) for å beskytte mot datatap.
En backup sikrer at du kan gjenopprette dersom oppgraderingen støter på uventede problemer.

### Oppgraderingsprosess

#### Trinn 1: Stopp digna-tjenesten

Hvis digna kjører som en Windows-tjeneste, stopp den først:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Trinn 2: Backup av nåværende backend-installasjon

I din digna-installasjonsmappe:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Trinn 3: Pakk ut og deploy ny versjon

1. Pakk ut den nye digna-installasjons-ZIP-filen
2. Kopier den nye `digna`-kjørbare, og `dashboard`-mappen til din installasjonsmappe


!!! warning "Viktig"

    `config.toml`-filen er **aldri** inkludert i installasjons-ZIP-en. Din eksisterende konfigurasjon forblir trygg.

### Trinn 4: Gjenopprett konfigurasjonsfilene dine

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Trinn 5: Oppgrader repositories-skjemaet

Naviger til din digna-installasjonsmappe og kjør:

```bash
digna repo upgrade
```

Dette oppdaterer PostgreSQL-skjemaet til siste versjon samtidig som alle eksisterende data bevares.

### Trinn 6: Start tjenestene på nytt

Hvis du kjører som en Windows-tjeneste:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Hvis du kjører manuelt, start serveren på nytt:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Hvis du bruker IIS eller Tomcat, restart den respektive webserveren.

#### Trinn 7: Verifiser oppgraderingen

1. Åpne digna-dashboardet
2. Verifiser at grensesnittet laster riktig
3. Sjekk serverloggene for eventuelle feil