---
title: Windows-installationsguide – digna Release 2026.06 | digna Dokumentation
description: Steg-för-steg-guide för att installera digna Release 2026.06 på Windows — systemkrav, PostgreSQL-setup, webbserverkonfiguration, backend- och dashboard-konfiguration, köra digna som Windows-tjänst och uppgradering till ny release.
keywords: digna windows installation, digna deploymentsguide, digna backend-setup, digna dashboard-installation, postgresql-setup, digna windows-tjänst, digna uppgraderingsguide
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

digna är en omfattande AI-driven plattform utformad för att optimera hanteringen av datakvalitet över olika data-miljöer såsom datalager, data lakes och lakehouses. Byggd för att vara mycket skalbar och anpassningsbar, adresserar digna moderna datautmaningar genom automation, realtidsövervakning och anomalidetektion.

digna består av två huvudkomponenter:

- **digna**: applikationens kärna, ansvarig för att bearbeta data och utföra kvalitetskontroller. Den förenar backend och kommandoradsgränssnittet i en enda körbar fil och ersätter därmed de separata programmen `dignabackend` och `dignacli` från tidigare releaser.
- **dignadashboard**: Ett webbaserat gränssnitt hostat på en webbserver, som ger ett användarvänligt sätt att interagera med digna-plattformen och visualisera datakvalitetsmått.

### What's New in Release 2026.06

Denna release för in data-observability-funktioner direkt i din kod, vilket gör det möjligt för utvecklare att övervaka datakvalitet vid källan. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) för fullständiga detaljer.

### Letar du efter macOS eller Linux?

Denna guide täcker Windows. För andra plattformar, se [macOS-installationsguide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) eller [Linux-installationsguide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## System Requirements {: #system-requirements }

Innan du påbörjar installationen, se till att ditt system uppfyller följande minimikrav:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server eller Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB ledigt lagringsutrymme |
| **Database** | PostgreSQL Server 12 eller senare |
| **Web Server** | IIS, Apache Tomcat eller motsvarande |

### Database Installation Options

**If PostgreSQL is already installed:**
Du kan lägga till en ny databas för digna i din befintliga PostgreSQL-server.

**If installing PostgreSQL on the same machine as digna:**

!!! info "Recommended Specifications"

    - **Memory**: 32 GB RAM (istället för 16 GB)
    - **Disk Space**: 50 GB ledigt lagringsutrymme (istället för 10 GB)

    Dessa högre specifikationer rymmer både digna och PostgreSQL-databasen som körs samtidigt.

---

## Pre-Installation Setup {: #pre-installation-setup }

Innan du installerar digna, se till att två viktiga förutsättningar är på plats:

1. **PostgreSQL Server** – för att lagra beräknade mått och prestandadata
2. **Web Server** – för att hosta digna Dashboard

Om dessa komponenter inte redan är uppsatta, följ avsnitten nedan för att installera och konfigurera dem.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Om PostgreSQL redan är installerat och körs på din lokala maskin eller om du använder en hanterad fjärr-PostgreSQL-server, kan du hoppa till [nästa avsnitt](#web-server-configuration).

### Installing PostgreSQL

Följ dessa steg för att installera PostgreSQL på Windows:

#### Step 1: Download PostgreSQL

1. Besök [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Välj **Windows**
3. Ladda ner den senaste installatören

#### Step 2: Run the Installer

1. Dubbelklicka på den nedladdade installatörsfilen
2. Följ anvisningarna i installationsguiden

#### Step 3: Choose Installation Directory

Välj katalog där PostgreSQL ska installeras. Standardplatsen är vanligtvis lämplig.

#### Step 4: Select Components

För en standardinstallation, behåll standardvalen av komponenter.

#### Step 5: Set PostgreSQL Superuser Password

Ange och bekräfta ett lösenord för PostgreSQL-superanvändaren (`postgres`). **Spara detta lösenord säkert** — du kommer att behöva det senare.

#### Step 6: Configure Port Number

Standardporten för PostgreSQL är `5432`. Du kan använda standardporten eller ange en annan port vid behov.

!!! tip "Tip"

    Om port 5432 redan används, välj en alternativ port och notera den för senare konfiguration.

#### Step 7: Choose Locale

Välj locale för din databas. Standardinställningen är vanligtvis lämplig för de flesta installationer.

#### Step 8: Complete Installation

Klicka **Next** genom återstående steg och sedan **Finish**.

#### Step 9: Verify Installation

Öppna Kommandotolken och verifiera att PostgreSQL är installerat:

```bash
psql --version
```

Du bör se PostgreSQL-versionen om installationen lyckades.

---

## Web Server Configuration {: #web-server-configuration }

digna kräver en webbserver för att hosta dashboarden. Välj ett av följande alternativ:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Du behöver endast installera och konfigurera **en** av dessa servrar.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) är Microsofts webbserver för att hosta webbplatser och webbaserade applikationer.

#### Enabling IIS

1. **Öppna Kontrollpanelen**
   - Tryck `Win + R`
   - Skriv `control` och tryck Enter

2. **Gå till Windows-funktioner**
   - Klicka **Programs**
   - Välj **Turn Windows features on or off**

3. **Aktivera Internet Information Services**
   - Scrolla ner och hitta **Internet Information Services (IIS)**
   - Markera kryssrutan för att aktivera den
   - Klicka på **+** för att expandera och verifiera att dessa underkomponenter är valda:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klicka OK** för att tillämpa ändringarna

5. **Verifiera IIS-installationen**
   - Öppna din webbläsare
   - Navigera till `http://localhost`
   - Du bör se IIS välkomstsida

#### Required: URL Rewrite Module

IIS kräver URL Rewrite-komponenten. Ladda ner och installera den från [officiella Microsoft-sidan](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Required: MIME Type for Markdown Files

För att säkerställa att Markdown-filer (`.md`) serveras korrekt av IIS:

1. Öppna **IIS Manager** (tryck `Win + R`, skriv `inetmgr`, tryck Enter)
2. Navigera till **Din webbplats > MIME Types**
3. Klicka **Add...**
4. Konfigurera:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Important"

    Utan denna inställning kan `.md`-filerna inte serveras korrekt.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat är en öppen källkods Java-servlet-container och webbserver.

#### Installation

1. **Download Apache Tomcat**
   - Besök [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Ladda ner Windows ZIP-distributionen

2. **Extract the Archive**
   - Packa upp ZIP-filen till en katalog på din maskin
   - Exempel: `C:\Program Files\Apache Tomcat`

3. **Verify Tomcat is Running**
   - Öppna din webbläsare
   - Navigera till `http://localhost:8080`
   - Du bör se Apache Tomcat välkomstsida

!!! tip "Tip"

    Apache Tomcat startar vanligtvis automatiskt efter installation. Om det inte gör det, gå till `bin`-mappen och kör `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

Digna-repositoryt lagrar alla mått som beräknas av digna. Det fungerar som den centrala databasen för analytiska och prestandadata.

#### Create Repository Schema and User

Öppna din PostgreSQL-klient (pgAdmin, psql eller liknande) och kör följande SQL-kommandon:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersätt följande platshållare:**

- `<digna_repo_schema>` — Ditt önskade schema-namn (t.ex. `dignarepo`)
- `<digna_repo_user>` — Ditt önskade användarnamn (t.ex. `digna_user`)
- `<digna_repo_password>` — Ett säkert lösenord för denna användare

**Exempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Best Practice"

    Använd starka, komplexa lösenord för databas-användare. Undvik lätta att gissa-credentialer.

---

### Step 2: Extract the digna Installation Package

1. Lokalisera digna-installations-ZIP-filen som tillhandahållits till dig
2. Packa upp den till önskad installationsplats
3. Efter uppackning bör du se följande objekt:
   - `dashboard/` — Webbgränssnittet
   - `digna` — Huvudexekverbara filen (backend + CLI kombinerat)
   - `config.toml` — Konfigurationsfil
   - `license.toml` — Licensfil (kopiera din här)

### Step 3: Install the License File

!!! warning "Important"

    Licensfilen ingår **inte** i installationspaketet och kommer att tillhandahållas separat av digna.

1. Lokalisera `license.toml`-filen som tillhandahållits till dig
2. Kopiera den till root i digna-installationskatalogen (där `config.toml` och den körbara `digna`-filen finns)

**Varför detta är viktigt:**
Licensfilen innehåller din kundinformation, licensens utgångsdatum och digital signatur. **Ändra inte filen** — eventuella ändringar gör den ogiltig.

**Katalogstruktur efter setup:**

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

Filen `config_template.toml` levereras i din digna-installationskatalog. Du behöver bara byta namn på den till `config.toml`.

**Plats:** `digna_installation/config.toml`

Öppna `config.toml` i en textredigerare och konfigurera varje avsnitt nedan.

#### [app] Section

Detta avsnitt konfigurerar digna-backendens applikationsinställningar:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Om dashboarden ligger på annan server, inkludera dess URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krävs för CORS med credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillåt alla HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillåt alla headers |

#### [repo] Section

Detta avsnitt konfigurerar anslutningen till PostgreSQL-databasen:

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
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns hostname/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasnamn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema som skapades tidigare |
| `digna_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-setupen |
| `digna_REPO_PASSWORD` | Ditt lösenord | Lösenord som sattes vid schema-creation |

#### [base] Section

Detta avsnitt innehåller säkerhets- och cookie-inställningar:

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

| Parameter | Value | Notes |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Matcha ditt frontend-domän |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Använd `true` för HTTPS-anslutningar |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktiverat för säkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Förhindrar CSRF-attacker |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal parallella inspections-jobb |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximal fördröjning, i sekunder, som schemaläggaren får lägga till innan ett förfallet jobb startar |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Tidpunkt (24-timmarsformat `HH:MM`) då den dagliga rensningen startar |

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

#### [logging] Section

Detta avsnitt konfigurerar loggningen:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal dagliga logg-backuper att behålla |

---

### Step 2: Validera konfigurationen

Kontrollera att `config.toml` är fullständig och korrekt uppbyggd innan du initierar repositoryt. Kör i din digna-installationskatalog:

```bash
digna config check
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

Overall: OK
```

Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter. Den fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202606.md).

### Step 3: Initialize the Repository

1. Öppna Kommandotolken
2. Navigera till din digna-installationskatalog (där `config.toml` och den körbara `digna`-filen finns)
3. Kör anslutningstestet:

```bash
digna repo check
```

Du bör se en bekräftelse på att anslutningen upprättats (själva repositoryt har ännu inte initialiserats).

### Step 4: Install the Repository Schema

I samma katalog, kör:

```bash
digna repo install
```

Detta kommando installerar nödvändiga tabeller och schema i din PostgreSQL-databas.

### Step 5: Create an Admin User

1. Öppna ett **nytt** Kommandotolksfönster
2. Navigera till din digna-installationskatalog
3. Kör följande kommando för att skapa en admin-användare:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Exempel:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Detta skapar en användare med fullständiga administrativa privilegier.

!!! tip "Best Practice"

    Använd ett starkt lösenord med en mix av versaler, gemener, siffror och specialtecken.

---

### Step 6: Start the digna Server

I digna-installationskatalogen, starta servern med:

```bash
digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns hostname/IP
- `--port` — Serverns port 

Du bör se startmeddelanden som bekräftar att servern körs:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Servern upptar terminalen"

    `serve` körs i förgrunden och fortsätter tills du stoppar den med ++ctrl+c++. Låt den vara igång medan du slutför installationen; för att i stället starta den automatiskt vid uppstart, se [Köra digna som Windows-tjänst](#running-digna-as-a-windows-service).

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

Digna-dashboarden har sin egen separata `config.toml`-fil i `dashboard/`-katalogen. Denna konfiguration levereras färdig och kräver normalt inga ändringar under initial installation. Du behöver endast konfigurera den om du vill anpassa backend-anslutningen.

Om du behöver ändra dashboard-konfigurationen (t.ex. för multi-instance-distributioner), se dashboardens dokumentation.

Välj din webbserver och följ motsvarande deploy-steg.

#### Deploying to IIS

1. **Öppna IIS Manager**
   - Tryck `Win + R`, skriv `inetmgr`, tryck Enter

2. **Skapa en ny webbplats**
   - I vänster panel, högerklicka på **Sites**
   - Välj **Add Website...**

3. **Konfigurera webbplatsen**
   - **Site Name**: Ange ett namn (t.ex. "dignaDashboard")
   - **Physical Path**: Klicka Browse och välj din `dashboard`-mapp
   - **Binding**: Ställ in IP-adress och port (standardport 80 för HTTP, 443 för HTTPS)

4. **Starta webbplatsen**
   - Klicka **OK** för att skapa webbplatsen
   - Högerklicka på den nya webbplatsen och välj **Start**

5. **Testa installationen**
   - Öppna din webbläsare
   - Navigera till `http://localhost` (eller din konfigurerade URL)
   - Du bör se digna-dashboardens inloggningssida

#### Deploying to Apache Tomcat

1. **Kopiera dashboard till Tomcat**
   - Kopiera `dashboard`-mappen till din Tomcat `webapps`-katalog
   - Byt namn vid behov (t.ex. till `digna`)
   - Exempel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifiera deployment**
   - Uppdatera eller ladda om Tomcat-hanteringssidan (http://localhost:8080)
   - Du bör se "digna" (eller ditt valda namn) listad bland deployade applikationer

3. **Åtkomst till dashboard**
   - Öppna din webbläsare
   - Navigera till `http://localhost:8080/digna`
   - Du bör se digna-dashboardens inloggningssida

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

Att köra digna-backend som en Windows-tjänst säkerställer att den:
- Startar automatiskt när servern bootar
- Körs i bakgrunden utan öppen Kommandotolk
- Startar om automatiskt om den kraschar
- Kan hanteras via Windows Services

### Service Management Files

Alla nödvändiga filer finns i digna-installationskatalogen under: `bin/`

Följande batch-filer finns tillgängliga:
- `install_service.bat` — Registrerar digna som en Windows-tjänst
- `uninstall_service.bat` — Avregistrerar tjänsten
- `start_service.bat` — Startar den registrerade tjänsten
- `stop_service.bat` — Stoppar den registrerade tjänsten

!!! warning "Administrator Required"

    Alla batch-filer måste köras med Administratörsrättigheter.

### Installing the Service

1. **Öppna Kommandotolken som administratör**
   - Högerklicka på Kommandotolken
   - Välj "Run as Administrator"

2. **Navigera till bin-mappen**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Kör installationsskriptet**
   ```bash
   install_service.bat
   ```

Digna-servern är nu registrerad som en Windows-tjänst med **automatisk start** aktiverad. Tjänsten startar inte omedelbart — se nästa avsnitt för att starta den.

### Starting and Stopping the Service

#### To Start the Service

1. Öppna Kommandotolken som administratör
2. Navigera till `digna\bin`
3. Kör:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Öppna Kommandotolken som administratör
2. Navigera till `digna\bin`
3. Kör:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    Stoppa alltid tjänsten innan du uppdaterar applikationsfiler.

### Moving the Service to a New Directory

Om du behöver flytta digna-installationen:

1. **Avinstallera den nuvarande tjänsten**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Flytta applikationsfilerna**
   - Flytta hela digna-installationsmappen till den nya platsen

3. **Installera om tjänsten**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Starta tjänsten**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Stoppa den körande tjänsten**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Avinstallera tjänsten**
   ```bash
   uninstall_service.bat
   ```

Digna-servern är nu avregistrerad som en Windows-tjänst.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Verifiera alla databasanslutningar först**

Från Release 2026.06 når digna varje källteknologi via **ODBC**. Tidigare releaser erbjöd ett val mellan en teknikspecifik drivrutin och ODBC, via omkopplaren **Use ODBC**. digna-teamet har valt att bygga enbart på ODBC, eftersom ett enda standardiserat gränssnitt ger mer än en uppsättning skräddarsydda drivrutiner:

- **Autentisering** — autentisering är en del av ODBC, så en anslutning kan använda allt som dess drivrutin stöder: lösenord, tokens och PAT:ar, Kerberos och Active Directory, MFA och webbläsarbaserad enkel inloggning, molnidentiteter, klientcertifikat och TLS. Nya metoder kommer med en uppdatering av drivrutinen i stället för att vänta på en digna-release.
- **Drivrutiner som underhålls av databasleverantörerna** — leverantörens egen drivrutin följer nya serverversioner och säkerhetsfixar, och du kan uppdatera den enligt ditt eget schema, oberoende av digna.
- **Ett enda sätt att konfigurera allt** — varje teknik är en lista med nyckel/värde-egenskaper, med samma gränssnitt, samma kryptering av känsliga värden och samma felsökning, i stället för olika fält per källa.
- **Finjustering och räckvidd** — drivrutinsalternativ som timeouts, TLS-inställningar, proxyservrar och hämtningsstorlekar är tillgängliga för varje källa, och varje teknik med en kompatibel ODBC-drivrutin kan anslutas, även sådana som digna inte publicerar någon egen guide för.

I praktiken innebär detta att omkopplaren **Use ODBC** och de separata fälten för värd, port, databas, användare och lösenord inte längre finns. **Varje anslutning som inte redan använder ODBC måste läggas om till ODBC** — det finns ingen automatisk konvertering, så planera för detta före uppgraderingen:

1. Gå igenom varje databasanslutning som är definierad i din installation och notera vilka som ännu inte använder ODBC — var och en av dem måste konfigureras om.
2. Installera motsvarande ODBC-drivrutin på digna-värden — anslutningar öppnas från den server som kör digna-backend, inte från webbläsaren. Se [Installera ODBC-drivrutinen på digna-värden](../../../databases/overview.md#install-the-driver).
3. Ha ODBC-egenskaperna redo för varje berörd anslutning. [Teknikguiderna](../../../databases/overview.md#technology-guides) listar en beprövad uppsättning egenskaper per källa.

Efter uppgraderingen lägger du om varje berörd anslutning till ODBC och testar den från dashboarden — se [Skapa en databasanslutning](../../../databases/overview.md#create-a-database-connection) och [Testa en anslutning](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy-anslutningar"

    Databricks Legacy-anslutaren har tagits bort i denna release. Migrera dessa anslutningar till [Databricks](../../../databases/databricks_connector_guide.md)-anslutaren.

**Creating a digna Repository Backup is Mandatory**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

### Upgrade Process

#### Step 1: Stop digna Service

Om digna körs som en Windows-tjänst, stoppa den först:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Säkerhetskopiera nuvarande installation

Byt namn på mapparna i din nuvarande installation i digna-installationskatalogen, så att den nya releasen kan distribueras vid sidan av dem:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend och dignacli används inte längre"

    Från Release 2026.06 ersätts `dignabackend` och `dignacli` av den enda körbara filen `digna`, som förenar backend och CLI. Behåll `dignabackend_old` och `dignacli_old` bara tills du har verifierat uppgraderingen — därefter kan du ta bort båda mapparna. Behåll `dashboard_old` tills du har återställt dina konfigurationsfiler från den (se steg 4).

#### Step 3: Extract and Deploy New Version

1. Packa upp den nya digna-installations-ZIP-filen
2. Kopiera den nya `digna`-exekverbara filen och `dashboard`-mappen till din installationskatalog


!!! warning "Important"

    Filen `config.toml` ingår **aldrig** i installations-ZIP:en. Din befintliga konfiguration förblir säker.

#### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Release 2026.06 ändrar config.toml"

    Tre inställningar är nya och obligatoriska, och tre används inte längre. En `config.toml` som har följt med från en tidigare release saknar de nya inställningarna, och digna startar inte så länge de saknas. Lägg till följande i din befintliga `config.toml`:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Lägg till de två `[base]`-nycklarna i din befintliga `[base]`-sektion och lägg till `[encryption]` som ny sektion. Ta sedan bort de inställningar som inte längre används: **`digna_FERNET_KEY`** från `[base]`, samt **`digna_APP_HOST`** och **`digna_APP_PORT`** från `[app]` — servern hämtar nu adress och port från `digna serve`.

    Vad varje inställning gör beskrivs i [Backend-konfiguration](#backend-configuration).

!!! warning "Enkel inloggning: formatet för [oidc_clients] har ändrats"

    Release 2026.06 ersätter arrayen av tabeller med en tabell per leverantör, namngiven efter leverantörsnyckeln. `DIGNA_OIDC_KEY` är borta — nyckeln ingår nu i sektionsrubriken.

    Före:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Efter:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Upprepa sektionen för varje leverantör och håll varje nyckel identisk med `key` i `dashboard_config.toml`. `digna config check` rapporterar `oidc_clients` som FAILED så länge den gamla formen finns kvar. Endast installationer som använder enkel inloggning berörs.

#### Step 5: Validera konfigurationen

Kontrollera att den uppdaterade `config.toml` är fullständig innan du rör repositoryt:

```bash
digna config check
```

Varje sektion måste rapportera OK. Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter.

#### Step 6: Upgrade the Repository Schema

Navigera till din digna-installationskatalog och kör:

```bash
digna repo upgrade
```

Detta uppdaterar PostgreSQL-schemat till senaste versionen samtidigt som all befintlig data bevaras.

#### Step 7: Restart Services

Om du kör som Windows-tjänst:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Om du kör manuellt, starta om servern:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Om du använder IIS eller Tomcat, starta om respektive webbserver.

#### Step 8: Verify the Upgrade

1. Öppna digna-dashboarden
2. Verifiera att gränssnittet laddar korrekt
3. Kontrollera serverloggarna efter eventuella fel
4. Lägg om varje anslutning som ännu inte använde ODBC till ODBC och testa sedan alla anslutningar — se [Testa en anslutning](../../../databases/overview.md#testing-a-connection)