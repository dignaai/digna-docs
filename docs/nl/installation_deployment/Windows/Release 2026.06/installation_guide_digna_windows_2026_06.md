---
title: Windows Installatiehandleiding – digna Release 2026.06 | digna Documentatie
description: Stapsgewijze handleiding voor het installeren van digna Release 2026.06 op Windows — systeemeisen, PostgreSQL-instelling, webserverconfiguratie, backend- en dashboardconfiguratie, digna als Windows-service uitvoeren en upgraden naar een nieuwe release.
keywords: digna windows installatie, digna deployment guide, digna backend setup, digna dashboard installatie, postgresql setup, digna windows service, digna upgrade guide
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

digna is een uitgebreide, door AI aangedreven platform dat is ontworpen om datakwaliteitsbeheer te optimaliseren in verschillende dataomgevingen zoals warehouses, lakes en lakehouses. Het is gebouwd om schaalbaar en aanpasbaar te zijn en pakt moderne data-uitdagingen aan via automatisering, realtime monitoring en anomaliedetectie.

digna bestaat uit twee hoofdcomponenten:

- **dignabackend**: De kernengine van de applicatie, verantwoordelijk voor het verwerken van data en het uitvoeren van kwaliteitscontroles.
- **dignadashboard**: Een webgebaseerde interface gehost op een webserver, die een gebruiksvriendelijke manier biedt om met het digna-platform te werken en datakwaliteitsstatistieken te visualiseren.

### What's New in Release 2026.06

Deze release brengt data observability-mogelijkheden rechtstreeks in je code, waardoor ontwikkelaars datakwaliteit bij de bron kunnen monitoren. Zie de [release notes](http://docs.digna.ai/changelog/Release_202606/) voor volledige details.

---

## System Requirements {: #system-requirements }

Voordat je begint met de installatie, zorg dat je systeem voldoet aan de volgende minimale vereisten:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server of Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB beschikbare opslag |
| **Database** | PostgreSQL Server 12 of hoger |
| **Web Server** | IIS, Apache Tomcat of equivalent |

### Database Installation Options

**If PostgreSQL is already installed:**
Je kunt een nieuwe database voor digna toevoegen aan je bestaande PostgreSQL-server.

**If installing PostgreSQL on the same machine as digna:**

> **⚠️ Recommended Specifications**
>
> - **Memory**: 32 GB RAM (in plaats van 16 GB)
> - **Disk Space**: 50 GB beschikbare opslag (in plaats van 10 GB)
>
> Deze hogere specificaties zijn aanbevolen wanneer zowel digna als PostgreSQL tegelijk op dezelfde machine draaien.

---

## Pre-Installation Setup {: #pre-installation-setup }

Voordat je digna installeert, zorg dat twee belangrijke vereisten aanwezig zijn:

1. **PostgreSQL Server** – voor het opslaan van berekende metrics en prestatiegegevens
2. **Web Server** – voor het hosten van het digna Dashboard

Als deze componenten nog niet zijn ingesteld, volg dan de onderstaande secties om ze te installeren en te configureren.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### If You Already Have PostgreSQL

Als PostgreSQL al geïnstalleerd en actief is op je lokale machine of als je een beheerde externe PostgreSQL-server gebruikt, kun je doorgaan naar de [volgende sectie](#web-server-configuration).

### Installing PostgreSQL

Volg deze stappen om PostgreSQL op Windows te installeren:

#### Step 1: Download PostgreSQL

1. Bezoek de [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Selecteer **Windows**
3. Download de nieuwste installer

#### Step 2: Run the Installer

1. Dubbelklik op het gedownloade installatiebestand
2. Volg de aanwijzingen in de setup-wizard

#### Step 3: Choose Installation Directory

Selecteer de map waar PostgreSQL geïnstalleerd wordt. De standaardlocatie is meestal geschikt.

#### Step 4: Select Components

Voor een standaardopstelling laat je de standaardcomponenten geselecteerd.

#### Step 5: Set PostgreSQL Superuser Password

Voer een wachtwoord in en bevestig dit voor de PostgreSQL superuser (`postgres`). **Sla dit wachtwoord veilig op** — je hebt het later nodig.

#### Step 6: Configure Port Number

De standaard PostgreSQL-poort is `5432`. Je kunt de standaardpoort gebruiken of een andere poort opgeven indien nodig.

> **💡 Tip**
>
> Als poort 5432 al in gebruik is, kies dan een alternatieve poort en noteer deze voor latere configuratie.

#### Step 7: Choose Locale

Selecteer de locale voor je database. De standaardinstelling is voor de meeste installaties geschikt.

#### Step 8: Complete Installation

Klik **Next** door de resterende stappen en klik vervolgens **Finish**.

#### Step 9: Verify Installation

Open de Opdrachtprompt en controleer of PostgreSQL is geïnstalleerd:

```bash
psql --version
```

Je zou de PostgreSQL-versie moeten zien als de installatie succesvol was.

---

## Web Server Configuration {: #web-server-configuration }

digna vereist een webserver om het dashboard te hosten. Kies een van de volgende opties:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Je hoeft slechts **één** van deze servers te installeren en configureren.

### IIS Setup {: #iis-setup }

#### Overview

Internet Information Services (IIS) is Microsofts webserver voor het hosten van websites en webapplicaties.

#### Enabling IIS

1. **Open Control Panel**
   - Druk `Win + R`
   - Typ `control` en druk op Enter

2. **Navigate to Windows Features**
   - Klik **Programs**
   - Selecteer **Turn Windows features on or off**

3. **Enable Internet Information Services**
   - Scroll naar beneden en vind **Internet Information Services (IIS)**
   - Vink het selectievakje aan om het in te schakelen
   - Klik op de **+** om uit te vouwen en controleer of de subcomponenten geselecteerd zijn:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klik OK** om de wijzigingen toe te passen

5. **Verify IIS Installation**
   - Open je browser
   - Navigeer naar `http://localhost`
   - Je zou de IIS-welkomstpagina moeten zien

#### Required: URL Rewrite Module

IIS vereist de URL Rewrite-component. Download en installeer deze vanaf de [officiële Microsoft-pagina](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Required: MIME Type for Markdown Files

Om ervoor te zorgen dat Markdown-bestanden (`.md`) correct door IIS worden geserveerd:

1. Open **IIS Manager** (druk `Win + R`, typ `inetmgr`, druk op Enter)
2. Navigeer naar **Your Site > MIME Types**
3. Klik **Add...**
4. Configureer:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **⚠️ Important**
>
> Zonder deze instelling kunnen `.md`-bestanden mogelijk niet correct worden geserveerd.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overview

Apache Tomcat is een open-source Java servletcontainer en webserver.

#### Installation

1. **Download Apache Tomcat**
   - Bezoek [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Download de Windows ZIP-distributie

2. **Extract the Archive**
   - Pak het ZIP-bestand uit naar een map op je systeem
   - Voorbeeld: `C:\Program Files\Apache Tomcat`

3. **Verify Tomcat is Running**
   - Open je browser
   - Navigeer naar `http://localhost:8080`
   - Je zou de Apache Tomcat-welkomstpagina moeten zien

> **💡 Tip**
>
> Apache Tomcat start meestal automatisch na installatie. Als dat niet het geval is, navigeer dan naar de `bin`-map en voer `startup.bat` uit.

---

## Initial Installation {: #initial-installation }

### Step 1: Set Up the digna Repository

De digna repository slaat alle door digna berekende metrics op. Het fungeert als de centrale database voor analyse- en prestatiegegevens.

#### Create Repository Schema and User

Open je PostgreSQL-client (pgAdmin, psql of vergelijkbaar) en voer de volgende SQL-commando's uit:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Vervang de volgende placeholders:**

- `<digna_repo_schema>` — de gewenste schemanaam (bijv. `dignarepo`)
- `<digna_repo_user>` — de gewenste gebruikersnaam (bijv. `digna_user`)
- `<digna_repo_password>` — een veilig wachtwoord voor deze gebruiker

**Voorbeeld:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **✅ Best Practice**
>
> Gebruik sterke, complexe wachtwoorden voor databasegebruikers. Vermijd gemakkelijk te raden inloggegevens.

---

### Step 2: Extract the digna Installation Package

1. Zoek het digna-installatie-ZIP-bestand dat aan je is geleverd
2. Pak het uit naar je gewenste installatieplaats
3. Na het uitpakken zou je de volgende items moeten zien:
   - `dashboard/` — Web dashboard interface
   - `digna` — Hoofdexecutable (backend + CLI gecombineerd)
   - `config.toml` — Configuratiebestand
   - `license.toml` — Licentiebestand (plaats hier jouw licentie)

### Step 3: Install the License File

> **⚠️ Important**
>
> Het licentiebestand is **niet** opgenomen in het installatiepakket en wordt apart door digna verstrekt.

1. Zoek het `license.toml`-bestand dat aan je is geleverd
2. Kopieer het naar de hoofdmap van de digna-installatie (waar `config.toml` en de `digna`-executable zich bevinden)

**Waarom dit belangrijk is:**
Het licentiebestand bevat klantinformatie, de vervaldatum van de licentie en een digitale handtekening. **Wijzig dit bestand niet** — wijzigingen maken de licentie ongeldig.

**Mapstructuur na setup:**

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

Het bestand `config_template.toml` wordt meegeleverd in je digna-installatiemap. Je hoeft het alleen te hernoemen naar `config.toml`.

**Locatie:** `digna_installation/config.toml`

Open `config.toml` in een teksteditor en configureer elk van de onderstaande secties.

#### [app] Section

Deze sectie configureert de instellingen van de digna backend-applicatie:

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
| `digna_APP_HOST` | `localhost` of IP-adres | Hostnaam of IP waar dignabackend gehost wordt |
| `digna_APP_PORT` | `8082` (standaard) | Poort voor REST API-endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Als het dashboard op een andere server staat, voeg dan de URL toe |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vereist voor CORS met credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Sta alle HTTP-methoden toe |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Sta alle headers toe |

#### [repo] Section

Deze sectie configureert de verbinding naar de PostgreSQL-database:

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
| `digna_REPO_HOST` | `localhost` of IP | PostgreSQL-server hostname/IP |
| `digna_REPO_PORT` | `5432` (standaard) | PostgreSQL-poort |
| `digna_REPO_DB` | `postgres` | Databasenaam |
| `digna_REPO_SCHEMA` | `dignarepo` | Eerder aangemaakte schema |
| `digna_REPO_USER` | `digna_user` | Gebruiker aangemaakt in de PostgreSQL-setup |
| `digna_REPO_PASSWORD` | Je wachtwoord | Wachtwoord ingesteld tijdens het aanmaken van de gebruiker |

#### [base] Section

Deze sectie bevat beveiligings- en cookie-instellingen:

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
| `digna_FERNET_KEY` | Encryptiesleutel | Gebruikt om tokens en cookies te versleutelen (standaard meegeleverd) |
| `digna_COOKIE_DOMAIN` | `localhost` | Komt overeen met je frontend-domein |
| `digna_COOKIE_SECURE` | `false` (lokaal) / `true` (productie) | Gebruik `true` voor HTTPS-verbindingen |
| `digna_COOKIE_HTTPONLY` | `true` | Altijd ingeschakeld voor veiligheid |
| `digna_COOKIE_SAME_SITE` | `lax` | Voorkomt CSRF-aanvallen |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 uur) | Sessie-timeout in seconden |
| `digna_MAX_WORKERS` | Aantal CPU-cores - 1 | Aantal parallelle inspectietaken |

#### [logging] Section

Deze sectie configureert het loggedrag:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` of `DEBUG` | `INFO` voor productie, `DEBUG` voor probleemoplossing |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Aantal bewaarde dagelijkse logbackups |

---

### Step 3: Initialize the Repository

1. Open de Opdrachtprompt
2. Navigeer naar je digna-installatiemap (waar `config.toml` en de `digna`-executable staan)
3. Voer de verbindingscontrole uit:

```bash
digna repo check
```

Je zou een bevestiging moeten zien dat de verbinding is gemaakt (de repository zelf is nog niet geïnitialiseerd).

### Step 4: Install the Repository Schema

Voer in dezelfde map het volgende uit:

```bash
digna repo install
```

Dit commando maakt de benodigde tabellen en schema's aan in je PostgreSQL-database.

### Step 5: Start the digna Server

Start in de digna-installatiemap de server met:

```bash
digna serve --address <host> --port <port>
```

**Parameters:**
- `--address` — Server hostname/IP
- `--port` — Serverpoort

Je zou opstartberichten moeten zien die bevestigen dat de server draait:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Step 6: Create an Admin User

1. Open een **nieuw** Opdrachtprompt-venster
2. Navigeer naar je digna-installatiemap
3. Voer het volgende commando uit om een admin-gebruiker aan te maken:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Voorbeeld:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Dit maakt een gebruiker met volledige administratieve rechten.

> **✅ Best Practice**
>
> Gebruik een sterk wachtwoord met een mix van hoofdletters, kleine letters, cijfers en speciale tekens.

---

## Dashboard Configuration {: #dashboard-configuration }

### Step 1: Deploy Dashboard to Web Server

Het digna-dashboard heeft een apart `config.toml`-bestand in de `dashboard/`-map. Deze configuratie wordt al meegeleverd en hoeft tijdens de initiële setup meestal niet te worden aangepast. Je hoeft het alleen te configureren als je de backend-verbinding wilt aanpassen.

Als je de dashboardconfiguratie moet wijzigen (bijv. voor multi-instance deployments), raadpleeg dan de documentatie van het dashboard.

Kies je webserver en volg de bijbehorende deployment-stappen.

#### Deploying to IIS

1. **Open IIS Manager**
   - Druk `Win + R`, typ `inetmgr`, druk op Enter

2. **Create a New Website**
   - Klik in het linkerpaneel met de rechtermuisknop op **Sites**
   - Selecteer **Add Website...**

3. **Configure the Website**
   - **Site Name**: Voer een naam in (bijv. "dignaDashboard")
   - **Physical Path**: Klik op Browse en selecteer je `dashboard`-map
   - **Binding**: Stel IP-adres en poort in (standaard poort 80 voor HTTP, 443 voor HTTPS)

4. **Start the Website**
   - Klik **OK** om de site aan te maken
   - Klik met de rechtermuisknop op de nieuwe site en selecteer **Start**

5. **Test the Installation**
   - Open je browser
   - Navigeer naar `http://localhost` (of je geconfigureerde URL)
   - Je zou de digna-dashboard loginpagina moeten zien

#### Deploying to Apache Tomcat

1. **Copy Dashboard to Tomcat**
   - Kopieer de `dashboard`-map naar de Tomcat `webapps`-map
   - Hernoem indien nodig (bijv. naar `digna`)
   - Voorbeeld: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verify Deployment**
   - Vernieuw of herlaad de Tomcat-beheerpagina (http://localhost:8080)
   - Je zou "digna" (of je gekozen naam) moeten zien in de lijst met gedeployde applicaties

3. **Access the Dashboard**
   - Open je browser
   - Navigeer naar `http://localhost:8080/digna`
   - Je zou de digna-dashboard loginpagina moeten zien

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Why Use a Windows Service?

Het draaien van de digna-backend als Windows-service zorgt ervoor dat deze:
- Automatisch start wanneer de server opstart
- Op de achtergrond draait zonder een open Opdrachtprompt
- Automatisch herstart als deze crasht
- Beheerd kan worden via Windows Services

### Service Management Files

Alle benodigde bestanden bevinden zich in de digna-installatiemap onder: `bin/`

De volgende batchbestanden zijn beschikbaar:
- `install_service.bat` — Registreert digna als Windows-service
- `uninstall_service.bat` — Deïnstalleert de service
- `start_service.bat` — Start de service
- `stop_service.bat` — Stopt de service

> **⚠️ Administrator Required**
>
> Alle batchbestanden moeten met Administrator-rechten worden uitgevoerd.

### Installing the Service

1. **Open Command Prompt as Administrator**
   - Klik met de rechtermuisknop op Opdrachtprompt
   - Selecteer "Run as Administrator"

2. **Navigate to the bin Folder**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Run the Installation Script**
   ```bash
   install_service.bat
   ```

De digna-server is nu geregistreerd als Windows-service met **automatic startup** ingeschakeld. De service start niet direct — zie de volgende sectie om deze te starten.

### Starting and Stopping the Service

#### To Start the Service

1. Open Opdrachtprompt als Administrator
2. Navigeer naar `digna\bin`
3. Voer uit:
   ```bash
   start_service.bat
   ```

#### To Stop the Service

1. Open Opdrachtprompt als Administrator
2. Navigeer naar `digna\bin`
3. Voer uit:
   ```bash
   stop_service.bat
   ```

> **💡 Tip**
>
> Stop altijd de service voordat je applicatiebestanden bijwerkt.

### Moving the Service to a New Directory

Als je de digna-installatie moet verplaatsen:

1. **Uninstall the Current Service**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Move the Application Files**
   - Verplaats de volledige digna-installatiemap naar de nieuwe locatie

3. **Reinstall the Service**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start the Service**
   ```bash
   start_service.bat
   ```

### Uninstalling the Service

1. **Stop the Running Service**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Uninstall the Service**
   ```bash
   uninstall_service.bat
   ```

De digna-server is nu gederegistreerd als Windows-service.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Before You Upgrade

**Creating a digna Repository Backup is Mandatory**

Voordat je digna upgradet, maak een back-up van je repository (PostgreSQL) om dataverlies te voorkomen.
Een back-up zorgt dat je kunt herstellen als de upgrade onverwachte problemen veroorzaakt.

### Upgrade Process

#### Step 1: Stop digna Service

Als digna als Windows-service draait, stop deze dan eerst:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Step 2: Backup Current Backend Installation

In je digna-installatiemap:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Step 3: Extract and Deploy New Version

1. Pak het nieuwe digna-installatie-ZIP-bestand uit
2. Kopieer de nieuwe `digna`-executable en de `dashboard`-map naar je installatiemap


> **✅ Important**
>
> Het `config.toml`-bestand wordt **nooit** opgenomen in het installatie-ZIP. Je bestaande configuratie blijft behouden.

### Step 4: Restore Your Configuration Files

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Step 5: Upgrade the Repository Schema

Navigeer naar je digna-installatiemap en voer uit:

```bash
digna repo upgrade
```

Dit werkt het PostgreSQL-schema bij naar de nieuwste versie en bewaart alle bestaande data.

### Step 6: Restart Services

Als je draait als Windows-service:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Als je handmatig draait, start de server opnieuw:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Als je IIS of Tomcat gebruikt, herstart de betreffende webserver.

#### Step 7: Verify the Upgrade

1. Open het digna-dashboard
2. Controleer dat de interface correct laadt
3. Controleer de serverlogs op eventuele fouten