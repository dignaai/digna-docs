---
title: Windows Installatiehandleiding – digna Release 2026.06 | digna Documentatie
description: Stapsgewijze handleiding voor het installeren van digna Release 2026.06 op Windows — systeemeisen, PostgreSQL-configuratie, webserverconfiguratie, backend- en dashboardconfiguratie, digna als Windows-service uitvoeren en upgraden naar een nieuwe release.
keywords: digna Windows installatie, digna uitrolhandleiding, digna backend installatie, digna dashboard installatie, postgresql installatie, digna Windows-service, digna upgradehandleiding
image: /assets/logo_square.png
---

# Windows Installatiehandleiding voor digna Release 2026.06

**Release:** 2026.06

**Laatst bijgewerkt:** 30 augustus 2026


---

## Inhoudsopgave

1. [Inleiding](#introduction)
2. [Systeemeisen](#system-requirements)
3. [Voorbereiding vóór installatie](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Webserverconfiguratie](#web-server-configuration)
6. [Initiële installatie](#initial-installation)
7. [Backendconfiguratie](#backend-configuration)
8. [Dashboardconfiguratie](#dashboard-configuration)
9. [digna als Windows-service uitvoeren](#running-digna-as-a-windows-service)
10. [Upgraden naar een nieuwe release](#upgrading-to-a-new-release)

---

## Inleiding {: #introduction }

### Over digna

digna is een uitgebreid AI-gestuurd platform ontworpen om het beheer van datakwaliteit te optimaliseren in verschillende dataomgevingen zoals warehouses, lakes en lakehouses. Ontworpen voor hoge schaalbaarheid en aanpasbaarheid, lost digna moderne dataproblemen op via automatisering, realtime monitoring en anomaliedetectie.

digna bestaat uit twee hoofcomponenten:

- **dignabackend**: De kernengine van de applicatie, verantwoordelijk voor het verwerken van data en het uitvoeren van kwaliteitscontroles.
- **dignadashboard**: Een webgebaseerde interface gehost op een webserver, die een gebruiksvriendelijke manier biedt om met het digna-platform te werken en datakwaliteitsmetriek te visualiseren.

### Wat is nieuw in Release 2026.06

Deze release brengt data-observability mogelijkheden direct in je code, waarmee ontwikkelaars datakwaliteit bij de bron kunnen monitoren. Zie de [release notes](http://docs.digna.ai/changelog/Release_202606/) voor volledige details.

### Op zoek naar macOS of Linux?

Deze handleiding behandelt Windows. Voor andere platforms, zie de [macOS Installatiehandleiding](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) of de [Linux Installatiehandleiding](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systeemeisen {: #system-requirements }

Voordat je met de installatie begint, zorg dat je systeem voldoet aan de volgende minimale vereisten:

| Vereiste | Specificatie |
|---|---|
| **Besturingssysteem** | Windows Server of Windows 10/11 |
| **Geheugen (Minimale setup)** | 16 GB RAM |
| **Schijfruimte** | 10 GB beschikbare opslag |
| **Database** | PostgreSQL Server 12 of hoger |
| **Webserver** | IIS, Apache Tomcat of equivalent |

### Opties voor database-installatie

**Als PostgreSQL al geïnstalleerd is:**
Je kunt een nieuwe database voor digna toevoegen aan je bestaande PostgreSQL Server.

**Als je PostgreSQL op dezelfde machine als digna installeert:**

!!! info "Aanbevolen specificaties"

    - **Geheugen**: 32 GB RAM (in plaats van 16 GB)
    - **Schijfruimte**: 50 GB beschikbare opslag (in plaats van 10 GB)

    Deze hogere specificaties accommoderen zowel digna als de PostgreSQL-database die gelijktijdig draaien.

---

## Voorbereiding vóór installatie {: #pre-installation-setup }

Voordat je digna installeert, zorg dat twee belangrijke vereisten aanwezig zijn:

1. **PostgreSQL Server** – voor het opslaan van berekende metriek en prestatiegegevens
2. **Webserver** – voor het hosten van het digna Dashboard

Als deze componenten nog niet zijn ingesteld, volg dan de onderstaande secties om ze te installeren en te configureren.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### Als je al PostgreSQL hebt

Als PostgreSQL al is geïnstalleerd en draait op je lokale machine of als je een beheerde externe PostgreSQL-server gebruikt, kun je doorgaan naar de [volgende sectie](#web-server-configuration).

### PostgreSQL installeren

Volg deze stappen om PostgreSQL op Windows te installeren:

#### Stap 1: Download PostgreSQL

1. Bezoek de [PostgreSQL-downloadpagina](https://www.postgresql.org/download/)
2. Selecteer **Windows**
3. Download de meest recente installer

#### Stap 2: Start de installer

1. Dubbelklik op het gedownloade installerbestand
2. Volg de aanwijzingen in de setup-wizard

#### Stap 3: Kies installatiefolder

Selecteer de map waar PostgreSQL wordt geïnstalleerd. De standaardlocatie is meestal geschikt.

#### Stap 4: Selecteer componenten

Voor een standaardopstelling kun je de standaardcomponentopties behouden.

#### Stap 5: Stel het PostgreSQL superuser-wachtwoord in

Voer een wachtwoord in en bevestig dit voor de PostgreSQL superuser (`postgres`). **Bewaar dit wachtwoord veilig** — je hebt het later nodig.

#### Stap 6: Configureer poortnummer

De standaard PostgreSQL-poort is `5432`. Je kunt de standaard gebruiken of een andere poort opgeven indien nodig.

!!! tip "Tip"

    Als poort 5432 al in gebruik is, kies een alternatieve poort en noteer deze voor latere configuratie.

#### Stap 7: Kies locale

Selecteer de locale voor je database. De standaardinstelling is meestal geschikt voor de meeste installaties.

#### Stap 8: Voltooi de installatie

Klik **Volgende** door de resterende stappen en klik vervolgens op **Voltooien**.

#### Stap 9: Verifieer installatie

Open Opdrachtprompt en controleer of PostgreSQL is geïnstalleerd:

```bash
psql --version
```

Je zou de PostgreSQL-versie moeten zien als de installatie succesvol was.

---

## Webserverconfiguratie {: #web-server-configuration }

digna vereist een webserver om het dashboard te hosten. Kies een van de volgende opties:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Je hoeft maar één van deze servers te installeren en te configureren.

### IIS Setup {: #iis-setup }

#### Overzicht

Internet Information Services (IIS) is Microsofts webserver voor het hosten van websites en webapplicaties.

#### IIS inschakelen

1. **Open Configuratiescherm**
   - Druk `Win + R`
   - Typ `control` en druk op Enter

2. **Navigeer naar Windows-onderdelen**
   - Klik **Programma's**
   - Selecteer **Windows-onderdelen in- of uitschakelen**

3. **Schakel Internet Information Services in**
   - Scroll naar beneden en vind **Internet Information Services (IIS)**
   - Vink het selectievakje aan om het in te schakelen
   - Klik op het **+** om uit te vouwen en controleer of de volgende subcomponenten zijn geselecteerd:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klik OK** om de wijzigingen toe te passen

5. **Verifieer IIS-installatie**
   - Open je browser
   - Navigeer naar `http://localhost`
   - Je zou de IIS-welkomstpagina moeten zien

#### Verplicht: URL Rewrite-module

IIS vereist de URL Rewrite-component. Download en installeer deze vanaf de [officiële Microsoft-pagina](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Verplicht: MIME-type voor Markdown-bestanden

Om ervoor te zorgen dat Markdown-bestanden (`.md`) correct door IIS worden geserveerd:

1. Open **IIS Manager** (druk `Win + R`, typ `inetmgr`, druk Enter)
2. Navigeer naar **Uw Site > MIME Types**
3. Klik **Toevoegen...**
4. Configureer:
   - **Bestandsextensie**: `.md`
   - **MIME-type**: `text/markdown`

!!! warning "Belangrijk"

    Zonder deze instelling kunnen `.md`-bestanden mogelijk niet correct worden geserveerd.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Overzicht

Apache Tomcat is een open-source Java servlet-container en webserver.

#### Installatie

1. **Download Apache Tomcat**
   - Bezoek [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Download de Windows ZIP-distributie

2. **Pak het archief uit**
   - Pak het ZIP-bestand uit naar een map op je systeem
   - Voorbeeld: `C:\Program Files\Apache Tomcat`

3. **Verifieer dat Tomcat draait**
   - Open je browser
   - Navigeer naar `http://localhost:8080`
   - Je zou de Apache Tomcat-welkomstpagina moeten zien

!!! tip "Tip"

    Apache Tomcat start normaal gesproken automatisch na installatie. Als dat niet het geval is, navigeer dan naar de `bin`-map en voer `startup.bat` uit.

---

## Initiële installatie {: #initial-installation }

### Stap 1: Richt de digna-repository in

De digna-repository slaat alle door digna berekende metriek op. Het fungeert als de centrale database voor analytische- en prestatiegegevens.

#### Maak repository-schema en gebruiker aan

Open je PostgreSQL-client (pgAdmin, psql of vergelijkbaar) en voer de volgende SQL-commando's uit:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Vervang de volgende placeholders:**

- `<digna_repo_schema>` — De gewenste schemanaam (bijv. `dignarepo`)
- `<digna_repo_user>` — De gewenste gebruikersnaam (bijv. `digna_user`)
- `<digna_repo_password>` — Een veilig wachtwoord voor deze gebruiker

**Voorbeeld:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Beste werkwijze"

    Gebruik sterke, complexe wachtwoorden voor databasegebruikers. Vermijd gemakkelijk te raden inloggegevens.

---

### Stap 2: Pak het digna-installatiepakket uit

1. Zoek het aan jou geleverde digna-installatie-ZIP-bestand
2. Pak het uit naar de gewenste installatieplek
3. Na het uitpakken zou je de volgende items moeten zien:
   - `dashboard/` — Webdashboard-interface
   - `digna` — Hoofduitvoerbaar bestand (backend + CLI gecombineerd)
   - `config.toml` — Configuratiebestand
   - `license.toml` — Licentiebestand (kopieer jouw bestand hierheen)

### Stap 3: Installeer het licentiebestand

!!! warning "Belangrijk"

    Het licentiebestand is **niet** opgenomen in het installatiepakket en wordt afzonderlijk door digna geleverd.

1. Zoek het `license.toml`-bestand dat aan jou is geleverd
2. Kopieer het naar de root van de digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)

**Waarom dit belangrijk is:**
Het licentiebestand bevat je klantgegevens, vervaldatum van de licentie en digitale handtekening. **Wijzig dit bestand niet** — elke wijziging ongeldigt de licentie.

**Mapstructuur na installatie:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backendconfiguratie {: #backend-configuration }

### Stap 1: Maak en bewerk het configuratiebestand

Het bestand `config_template.toml` wordt meegeleverd in je digna-installatiemap. Je hoeft het alleen te hernoemen naar `config.toml`.

**Locatie:** `digna_installation/config.toml`

Open `config.toml` in een teksteditor en configureer elke sectie hieronder.

#### [app] Sectie

Deze sectie configureert de digna-backend applicatie-instellingen:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_APP_HOST` | `localhost` of IP-adres | Hostnaam of IP waar dignabackend gehost wordt |
| `digna_APP_PORT` | `8082` (standaard) | Poort voor REST API-eindpunten |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Als het dashboard op een andere server staat, voeg dan de URL toe |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vereist voor CORS met credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Sta alle HTTP-methodes toe |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Sta alle headers toe |

#### [repo] Sectie

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

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_REPO_HOST` | `localhost` of IP | PostgreSQL-server hostnaam/IP |
| `digna_REPO_PORT` | `5432` (standaard) | PostgreSQL-poort |
| `digna_REPO_DB` | `postgres` | Databasenaam |
| `digna_REPO_SCHEMA` | `dignarepo` | Eerder aangemaakt schema |
| `digna_REPO_USER` | `digna_user` | Gebruiker aangemaakt in PostgreSQL-setup |
| `digna_REPO_PASSWORD` | Je wachtwoord | Wachtwoord ingesteld tijdens schema-creatie |

#### [base] Sectie

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

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_FERNET_KEY` | Encryptiesleutel | Gebruikt om tokens en cookies te versleutelen (standaard meegeleverd) |
| `digna_COOKIE_DOMAIN` | `localhost` | Komt overeen met je frontend-domein |
| `digna_COOKIE_SECURE` | `false` (lokaal) / `true` (productie) | Gebruik `true` voor HTTPS-verbindingen |
| `digna_COOKIE_HTTPONLY` | `true` | Altijd ingeschakeld voor veiligheid |
| `digna_COOKIE_SAME_SITE` | `lax` | Voorkomt CSRF-aanvallen |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 uur) | Sessie-timeout in seconden |
| `digna_MAX_WORKERS` | Aantal CPU-cores - 1 | Aantal parallelle inspectietaken |

#### [logging] Sectie

Deze sectie configureert het loggedrag:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` of `DEBUG` | `INFO` voor productie, `DEBUG` voor probleemoplossing |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Aantal dagelijkse logbackups om te bewaren |

---

### Stap 3: Initialiseer de repository

1. Open Opdrachtprompt
2. Navigeer naar je digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)
3. Voer de verbindingscontrole uit:

```bash
digna repo check
```

Je zou een bevestiging moeten zien dat de verbinding tot stand is gebracht (de repository zelf is nog niet geïnitialiseerd).

### Stap 4: Installeer het repository-schema

Voer in dezelfde map uit:

```bash
digna repo install
```

Dit commando installeert de benodigde tabellen en het schema in je PostgreSQL-database.

### Stap 5: Start de digna-server

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

### Stap 6: Maak een admin-gebruiker aan

1. Open een **nieuw** Opdrachtprompt-venster
2. Navigeer naar je digna-installatiemap
3. Voer het volgende commando uit om een admin-gebruiker aan te maken:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Voorbeeld:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Dit maakt een gebruiker aan met volledige beheerdersrechten.

!!! tip "Beste werkwijze"

    Gebruik een sterk wachtwoord met een mix van hoofdletters, kleine letters, cijfers en speciale tekens.

---

## Dashboardconfiguratie {: #dashboard-configuration }

### Stap 1: Zet het dashboard uit naar de webserver

Het digna-dashboard heeft een eigen separaat `config.toml`-bestand in de `dashboard/`-map. Deze configuratie wordt al meegeleverd en vereist geen wijzigingen tijdens de initiële setup. Je hoeft dit alleen te wijzigen als je de backendverbinding wilt aanpassen.

Als je de dashboardconfiguratie wilt aanpassen (bijv. bij multi-instance deployments), raadpleeg dan de documentatie van het dashboard.

Kies je webserver en volg de bijbehorende deploymentstappen.

#### Deployen naar IIS

1. **Open IIS Manager**
   - Druk `Win + R`, typ `inetmgr`, druk Enter

2. **Maak een nieuwe website**
   - Klik met de rechtermuisknop op **Sites** in het linkerpaneel
   - Selecteer **Website toevoegen...**

3. **Configureer de website**
   - **Sitenaam**: Voer een naam in (bijv. "dignaDashboard")
   - **Fysiek pad**: Klik Bladeren en selecteer je `dashboard`-map
   - **Binding**: Stel IP-adres en poort in (standaard poort 80 voor HTTP, 443 voor HTTPS)

4. **Start de website**
   - Klik **OK** om de site te maken
   - Klik met de rechtermuisknop op de nieuwe site en selecteer **Start**

5. **Test de installatie**
   - Open je browser
   - Navigeer naar `http://localhost` (of je geconfigureerde URL)
   - Je zou de inlogpagina van het digna-dashboard moeten zien

#### Deployen naar Apache Tomcat

1. **Kopieer Dashboard naar Tomcat**
   - Kopieer de `dashboard`-map naar de `webapps`-directory van Tomcat
   - Hernoem indien nodig (bijv. naar `digna`)
   - Voorbeeld: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifieer deployment**
   - Ververs of herlaad de Tomcat-beheerpagina (http://localhost:8080)
   - Je zou "digna" (of de door jou gekozen naam) moeten zien in de lijst met gedeployde applicaties

3. **Toegang tot het dashboard**
   - Open je browser
   - Navigeer naar `http://localhost:8080/digna`
   - Je zou de inlogpagina van het digna-dashboard moeten zien

---

## digna als Windows-service uitvoeren {: #running-digna-as-a-windows-service }

### Waarom een Windows-service gebruiken?

Het draaien van de digna-backend als een Windows-service zorgt ervoor dat deze:
- Automatisch start wanneer de server opstart
- Op de achtergrond draait zonder een open Opdrachtprompt
- Automatisch opnieuw start als deze crasht
- Beheerd kan worden via Windows Services

### Bestanden voor servicemanagement

Alle benodigde bestanden bevinden zich in de digna-installatiemap onder: `bin/`

De volgende batchbestanden zijn beschikbaar:
- `install_service.bat` — Registreert digna als een Windows-service
- `uninstall_service.bat` — Deregistreert de service
- `start_service.bat` — Start de service
- `stop_service.bat` — Stopt de service

!!! warning "Beheerdersrechten vereist"

    Alle batchbestanden moeten worden uitgevoerd met Administrator-rechten.

### De service installeren

1. **Open Opdrachtprompt als Administrator**
   - Klik met de rechtermuisknop op Opdrachtprompt
   - Kies "Als administrator uitvoeren"

2. **Navigeer naar de bin-map**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Voer het installatiescript uit**
   ```bash
   install_service.bat
   ```

De digna-server is nu geregistreerd als een Windows-service met **automatische opstart** ingeschakeld. De service start niet direct — zie de volgende sectie om deze te starten.

### De service starten en stoppen

#### Om de service te starten

1. Open Opdrachtprompt als Administrator
2. Navigeer naar `digna\bin`
3. Voer uit:
   ```bash
   start_service.bat
   ```

#### Om de service te stoppen

1. Open Opdrachtprompt als Administrator
2. Navigeer naar `digna\bin`
3. Voer uit:
   ```bash
   stop_service.bat
   ```

!!! tip "Tip"

    Stop de service altijd voordat je applicatiebestanden bijwerkt.

### De service naar een nieuwe map verplaatsen

Als je de digna-installatie wilt verplaatsen:

1. **De huidige service deïnstalleren**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Verplaats de applicatiebestanden**
   - Verplaats de volledige digna-installatiemap naar de nieuwe locatie

3. **Installeer de service opnieuw**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Start de service**
   ```bash
   start_service.bat
   ```

### De service verwijderen

1. **Stop de draaiende service**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Deïnstalleer de service**
   ```bash
   uninstall_service.bat
   ```

De digna-server is nu afgehandeld als Windows-service.

---

## Upgraden naar een nieuwe release {: #upgrading-to-a-new-release }

### Voordat je upgrade

**Het maken van een digna-repositorybackup is verplicht**

Maak vóór het upgraden van digna een back-up van je repository (PostgreSQL) om gegevensverlies te voorkomen.
Een back-up zorgt dat je kunt herstellen als de upgrade onverwachte problemen tegenkomt.

### Upgradeproces

#### Stap 1: Stop de digna-service

Als digna als Windows-service draait, stop deze dan eerst:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Stap 2: Backup van de huidige backend-installatie

In je digna-installatiemap:

```bash
# Hernoem map met dignabackend
ren dignabackend dignabackend_old
```
```bash
# Hernoem dashboard
ren dashboard dashboard_old
```

#### Stap 3: Pak de nieuwe versie uit en deploy

1. Pak het nieuwe digna-installatie-ZIP-bestand uit
2. Kopieer het nieuwe `digna`-uitvoerbare bestand en de `dashboard`-map naar je installatiemap


!!! warning "Belangrijk"

    Het `config.toml`-bestand is **nooit** inbegrepen in het installatie-ZIP. Je bestaande configuratie blijft veilig.

### Stap 4: Herstel je configuratiebestanden

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Stap 5: Upgrade het repository-schema

Navigeer naar je digna-installatiemap en voer uit:

```bash
digna repo upgrade
```

Dit werkt het PostgreSQL-schema bij naar de nieuwste versie terwijl alle bestaande data behouden blijven.

### Stap 6: Herstart services

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

Als je IIS of Tomcat gebruikt, herstart dan de betreffende webserver.

#### Stap 7: Verifieer de upgrade

1. Open het digna-dashboard
2. Controleer of de interface correct laadt
3. Controleer de serverlogs op eventuele fouten