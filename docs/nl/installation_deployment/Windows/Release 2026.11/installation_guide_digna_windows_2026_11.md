---
title: Windows Installatiehandleiding – digna Release 2026.11 | digna Documentatie
description: Stapsgewijze handleiding voor het installeren van digna Release 2026.11 op Windows — systeemeisen, PostgreSQL-configuratie, webserverconfiguratie, backend- en dashboardconfiguratie, digna als Windows-service uitvoeren en upgraden vanaf Release 2026.06.
keywords: digna Windows installatie, digna uitrolhandleiding, digna backend installatie, digna dashboard installatie, postgresql installatie, digna Windows-service, digna upgradehandleiding
image: /assets/logo_square.png
---

# Windows Installatiehandleiding voor digna Release 2026.11

**Release:** 2026.11

**Laatst bijgewerkt:** 7 november 2026


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

- **digna**: de kern van de applicatie, verantwoordelijk voor het verwerken van gegevens en het uitvoeren van kwaliteitscontroles. Het combineert de backend en de opdrachtregelinterface in één uitvoerbaar bestand en vervangt daarmee de losse programma's `dignabackend` en `dignacli` uit eerdere releases.
- **dignadashboard**: Een webgebaseerde interface gehost op een webserver, die een gebruiksvriendelijke manier biedt om met het digna-platform te werken en datakwaliteitsmetriek te visualiseren.

### Wat is nieuw in Release 2026.11

Deze release voegt digna Data Reconciliation toe, digna Agentic met de digna MCP Server, en de digna Engine, die data binnen digna kan profileren en referentiële integriteit kan controleren tussen verschillende databasetechnologieën. Zie de [release notes](../../../changelog/Release_202611.md) voor volledige details.

Voor een installatie brengt de release een nieuw migratiemechanisme voor de repository, een optionele `[duckdb]`-sectie in `config.toml` voor de digna Engine en een nieuw licentiebestand. De [upgradesectie](#upgrading-to-a-new-release) behandelt elk daarvan.

### Op zoek naar macOS of Linux?

Deze handleiding behandelt Windows. Voor andere platforms, zie de [macOS Installatiehandleiding](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) of de [Linux Installatiehandleiding](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Databaseverbindingen die de digna Engine als profileringslocatie gebruiken, worden op de digna-host zelf geprofileerd. Plan daarvoor extra geheugen en schijfruimte in, zie de [\[duckdb\]-sectie](#duckdb-section).

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

!!! info "Het configuratie- en licentiebestand zitten niet in het pakket"

    Noch `config.toml` noch `dashboard/dashboard_config.toml` wordt met de installatie
    meegeleverd — u maakt beide zelf aan, in [Backendconfiguratie](#backend-configuration) en
    [Dashboardconfiguratie](#dashboard-configuration). Ook `license.toml` wordt niet meegeleverd;
    digna levert het afzonderlijk, zoals Stap 3 beschrijft.

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

Deze sectie configureert cross-origin resource sharing (CORS) tussen het dashboard en de backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL's | De URL's van waaruit het dashboard wordt geserveerd. Browserverzoeken van elke andere origin worden geweigerd |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vereist, zodat de browser bij elk verzoek de sessiecookie meestuurt |

!!! info "De [app]-sectie is optioneel"

    Vanaf Release 2026.11 mogen beide sleutels, en de hele `[app]`-sectie, worden weggelaten. Dat is de juiste opzet wanneer een reverse proxy het dashboard en de backend onder één origin serveert: de browser doet dan geen cross-origin-verzoeken, en standaard wordt er geen enkele toegestaan.

#### [repo] Sectie

Deze sectie configureert de verbinding naar de PostgreSQL-database:

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

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` of IP | PostgreSQL-server hostnaam/IP |
| `DIGNA_REPO_PORT` | `5432` (standaard) | PostgreSQL-poort |
| `DIGNA_REPO_DB` | `postgres` | Databasenaam |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Eerder aangemaakt schema |
| `DIGNA_REPO_USER` | `digna_user` | Gebruiker aangemaakt in PostgreSQL-setup |
| `DIGNA_REPO_PASSWORD` | Je wachtwoord | Wachtwoord ingesteld tijdens schema-creatie |
| `DIGNA_REPO_SSLMODE` | `prefer` (standaard) | Optioneel. PostgreSQL SSL-modus: `disable`, `allow`, `prefer`, `require`, `verify-ca` of `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standaard) | Optioneel. Aantal verbindingen dat digna open houdt naar de repository |

#### [base] Sectie

Deze sectie bevat beveiligings-, cookie- en inspectie-instellingen:

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

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_FERNET_KEY` | Hierboven getoonde waarde | Sleutel van de versleuteling die eerdere releases gebruikten. Deze moet aanwezig zijn; behoud de getoonde waarde |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host waaronder het dashboard bereikbaar is. `""` stelt geen domein in; dat is juist achter een proxy die het dashboard en de backend onder één origin serveert |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Moet `true` zijn zodra digna via HTTPS wordt geserveerd |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Houdt de sessiecookie buiten bereik van scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 uur) | Sessie-timeout in seconden |
| `DIGNA_MAX_WORKERS` | Aantal CPU-cores - 1 | Aantal inspecties dat tegelijk mag draaien |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Vereist. Wordt gebruikt voor de links in meldingsberichten en moet dus een URL zijn die de ontvangers kunnen openen |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standaard) | Optioneel. Aantal seconden dat één query op een brondatabase mag draaien voordat deze wordt afgebroken; `0` schakelt de time-out uit |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standaard) | Optioneel. Aantal seconden dat wordt gewacht op een verbinding met een brondatabase; `0` wacht onbeperkt |

#### [encryption] Sectie

Deze sectie bevat de sleutel waarmee gevoelige waarden in de repository worden versleuteld. Ze is **verplicht** — `config check` meldt de sectie `[encryption]` als FAILED wanneer de sleutel ontbreekt.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-gecodeerde sleutel | Versleutelt gevoelige waarden die in de digna-repository zijn opgeslagen |

!!! warning "Bescherm config.toml"

    Deze sleutel is een vaste waarde, identiek in alle digna-installaties, en het is de sleutel die de gevoelige waarden in uw repository ontsleutelt. Beperk `config.toml` tot het account waaronder digna draait, houd het bestand buiten versiebeheer en gedeelde schijven, en sluit het uit van elke back-up die minder veilig wordt bewaard dan de repository zelf.

#### [logging] Sectie

Deze sectie configureert het loggedrag:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` of `DEBUG` | `INFO` voor productie, `DEBUG` voor probleemoplossing. `TRACE`, `WARN` en `ERROR` worden ook geaccepteerd |
| `DIGNA_LOGGING_DIR` | `logs` (standaard) | Optioneel. Map voor de roterende logbestanden, relatief ten opzichte van de werkmap |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standaard) | Optioneel. Aantal geroteerde logbestanden dat wordt bewaard |

!!! warning "Behoud de logmap wanneer digna als service draait"

    Een Windows-service heeft geen console, dus de logbestanden zijn de enige registratie van wat de service doet. Stel `DIGNA_LOGGING_DIR` niet in op een lege string; daarmee worden de logbestanden uitgeschakeld.

#### [duckdb] Sectie (optioneel) {: #duckdb-section }

Nieuw in Release 2026.11. Deze sectie bepaalt de resources van de **digna Engine**, die data binnen digna profileert voor databaseverbindingen met **digna Engine** als profileringslocatie, en die controles op referentiële integriteit uitvoert tussen datasources op verschillende databaseverbindingen. Zie [Profileringslocatie](../../../platform/profiling/profiling_location.md).

De sectie is optioneel. Zonder deze sectie gelden de onderstaande standaardwaarden.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standaard) | Geheugen, in MB, dat één run van de digna Engine mag gebruiken. Er kunnen tot `DIGNA_MAX_WORKERS` runs tegelijk actief zijn |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standaard: de tijdelijke map van het account waaronder digna draait (`%TEMP%`) | Map voor tijdelijke bestanden wanneer de data niet in het geheugen past |

!!! tip "De digna Engine dimensioneren"

    Reken op maximaal `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` aan geheugen op de digna-host, bovenop wat digna zelf gebruikt, en op voldoende vrije schijfruimte in de tijdelijke map voor de grootste geïnspecteerde datum van de datasources die de digna Engine gebruiken. Laat `DIGNA_DUCKDB_TEMP_DIRECTORY` verwijzen naar een schijf met die ruimte, beschrijfbaar voor het account waaronder digna draait:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    U hebt deze sectie alleen nodig als ten minste één databaseverbinding de digna Engine gebruikt, of als een controle op referentiële integriteit datasources op verschillende verbindingen vergelijkt.

---

### Stap 2: Configuratie valideren

Controleer voordat u de repository initialiseert of `config.toml` volledig en correct opgebouwd is. Voer in uw digna-installatiemap uit:

```bash
digna config check
```

Elke sectie wordt afzonderlijk gevalideerd, zodat één fout de toestand van de rest niet verbergt:

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

Los alles op wat als FAILED wordt gemeld en voer het commando opnieuw uit voordat u verdergaat. Een WARNING onder **Unknown keys** somt sleutels in `config.toml` op die digna niet leest; ze hebben geen effect, dus verwijder ze of corrigeer de spelling. De volledige lijst met opties staat in de [CLI-referentie](../../../cli/Command_Line_Interface_202611.md).

### Stap 3: Initialiseer de repository

1. Open Opdrachtprompt
2. Navigeer naar je digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)
3. Voer de verbindingscontrole uit:

```bash
digna repo check
```

Bij een nieuw schema maakt het commando verbinding en meldt het vervolgens dat er nog geen repository is geïnstalleerd:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Op dit punt is dat het verwachte resultaat: het bevestigt dat digna PostgreSQL en het schema bereikt. Een verbindings- of authenticatiefout wijst daarentegen op de `[repo]`-sectie of op de PostgreSQL-installatie.

### Stap 4: Installeer het repository-schema

Voer in dezelfde map uit:

```bash
digna repo upgrade
```

Dit commando installeert de benodigde tabellen in het repository-schema en eindigt met:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installeert en upgradet"

    Vanaf Release 2026.11 installeert `repo upgrade` een nieuwe repository en upgradet het een bestaande. `repo install` werkt nog steeds als andere naam voor hetzelfde commando.

### Stap 5: Maak een admin-gebruiker aan

1. Open een **nieuw** Opdrachtprompt-venster
2. Navigeer naar je digna-installatiemap
3. Voer het volgende commando uit om een admin-gebruiker aan te maken:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Voorbeeld:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Dit maakt een gebruiker aan met volledige beheerdersrechten.

!!! tip "Beste werkwijze"

    Gebruik een sterk wachtwoord met een mix van hoofdletters, kleine letters, cijfers en speciale tekens.

---

### Stap 6: Start de digna-server

Start in de digna-installatiemap de server met:

```bash
digna serve --address <host> --port <port>
```

**Parameters:**
- `--address` — Server hostname/IP (standaard `127.0.0.1`)
- `--port` — Serverpoort (standaard `8000`)

Zodra de server draait, toont hij het adres waarop hij luistert:

```text
Server running on http://127.0.0.1:8082
```

!!! note "De server houdt de terminal bezet"

    `serve` draait op de voorgrond en blijft draaien totdat u het stopt met ++ctrl+c++. Laat het draaien terwijl u de installatie afrondt; zie voor automatisch starten bij het opstarten [digna als Windows-service uitvoeren](#running-digna-as-a-windows-service).

---

## Dashboardconfiguratie {: #dashboard-configuration }

### Stap 1: Zet het dashboard uit naar de webserver

Het digna-dashboard leest zijn eigen configuratie uit `dashboard/dashboard_config.toml`. Dat bestand wordt niet met de installatie meegeleverd — u maakt het aan in de `dashboard/`-map, naast de dashboardbestanden.

De inhoud ervan wordt beschreven onder [Single Sign-On](../../../sso/overview.md), en daar is het bestand ook nodig: het bevat de aanmeldopties die het dashboard aanbiedt en, voor multi-instance-deployments, de backendverbinding.

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

### De `windows`-commando's

De service wordt beheerd door het `digna`-uitvoerbare bestand zelf, via de subcommando's van
`digna windows`. Er zijn geen batchbestanden meer om uit te voeren.

| Commando | Doel |
|---|---|
| `digna windows install` | Registreert digna als een Windows-service |
| `digna windows start` | Start de geregistreerde service |
| `digna windows stop` | Stopt de draaiende service |
| `digna windows uninstall` | Deregistreert de service |

!!! warning "Beheerdersrechten vereist"

    Alle vier de commando's moeten worden uitgevoerd vanuit een Opdrachtprompt die als Administrator is geopend.

Elk commando accepteert `--name` om een service aan te spreken die onder een andere dan de
standaardnaam is geregistreerd. De volledige lijst met opties staat in de
[CLI-referentie](../../../cli/Command_Line_Interface_202611.md).

### De service installeren

1. **Open Opdrachtprompt als Administrator**
   - Klik met de rechtermuisknop op Opdrachtprompt
   - Kies "Als administrator uitvoeren"

2. **Navigeer naar uw digna-installatiemap**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registreer de service**
   ```bash
   digna windows install
   ```

!!! important "Geef adres en poort op, tenzij de standaardwaarden volstaan"

    `install` legt het adres en de poort vast in de serviceregistratie, en de service bindt zich
    precies aan wat is vastgelegd. De standaardwaarden zijn `127.0.0.1` en `8000`, die alleen
    verbindingen van de machine zelf accepteren. Een dashboard op een andere host kan die niet
    bereiken, dus geef het adres op waarop de backend moet luisteren:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Deze waarden worden niet uit `config.toml` gelezen. Om ze later te wijzigen, verwijdert u de
    service en installeert u deze opnieuw met de nieuwe waarden.

De service wordt geregistreerd met **automatische opstart**, zodat deze met Windows meestart. De
service start niet direct — zie de volgende sectie.

#### Installatieopties

| Optie | Standaard | Doel |
|---|---|---|
| `--name` | `digna` | Naam waaronder de service wordt geregistreerd |
| `--display-name` | `digna` | Naam die in services.msc wordt getoond |
| `--description` | `digna data quality backend` | Beschrijving die in services.msc wordt getoond |
| `--address` | `127.0.0.1` | Adres waaraan de service zijn API bindt |
| `--port` | `8000` | Poort waaraan de service zijn API bindt |
| `--working-dir` | de map van het `digna`-uitvoerbare bestand | Map met `config.toml` en `license.toml`, die de service als werkmap gebruikt |
| `--start-type` | `auto` | `auto` start met Windows, `manual` start alleen op verzoek, `disabled` registreert de service maar weigert deze te starten |
| `--account` | `LocalSystem` | Account waaronder de service draait, bijv. `DOMAIN\user` of `.\user` |
| `--password` | | Wachtwoord van `--account` |

!!! tip "Draaien onder een domeinaccount"

    `LocalSystem` heeft geen netwerkidentiteit, dus Windows-verificatie bij SQL Server en elke
    toegang tot een netwerkshare mislukken. Installeer met `--account` en `--password` wanneer de
    service als een specifieke gebruiker bij resources moet kunnen.

### De service starten en stoppen

#### Om de service te starten

```bash
digna windows start
```

#### Om de service te stoppen

```bash
digna windows stop
```

!!! tip "Tip"

    Stop de service altijd voordat je applicatiebestanden bijwerkt.

### De service naar een nieuwe map verplaatsen

Als je de digna-installatie wilt verplaatsen:

1. **Stop en deregistreer de huidige service**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Verplaats de applicatiebestanden**
   - Verplaats de volledige digna-installatiemap naar de nieuwe locatie

3. **Registreer de service opnieuw vanaf de nieuwe locatie**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Herhaal alle waarden voor `--address`, `--port` of `--account` die u de eerste keer hebt
   gebruikt — de vorige registratie bestaat niet meer.

4. **Start de service**
   ```bash
   digna windows start
   ```

### De service verwijderen

1. **Stop de draaiende service**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Deregistreer de service**
   ```bash
   digna windows uninstall
   ```

De digna-server is nu afgehandeld als Windows-service.

---

## Upgraden naar een nieuwe release {: #upgrading-to-a-new-release }

Deze sectie beschrijft de upgrade van een installatie van Release 2026.06 naar Release 2026.11. Is uw installatie ouder, lees dan eerst [Upgraden vanaf een release vóór 2026.06](#upgrading-from-a-release-before-2026-06).

### Voordat je upgrade

**Het maken van een digna-repositorybackup is verplicht**

Maak vóór het upgraden van digna een back-up van je repository (PostgreSQL) om gegevensverlies te voorkomen. Een back-up zorgt dat je kunt herstellen als de upgrade onverwachte problemen tegenkomt.

**Het licentiebestand voor Release 2026.11 aanvragen**

Release 2026.11 heeft een nieuw `license.toml` nodig. Vraag het bij het digna-team aan voordat u begint, en houd het gereed voor [Stap 7](#step-7-replace-the-license-file).

### Upgraden vanaf een release vóór 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 bracht drie wijzigingen die nog steeds gelden wanneer u een oudere installatie rechtstreeks naar 2026.11 upgradet:

- **Alleen ODBC.** digna benadert elke brontechnologie via ODBC. Elke databaseverbinding die nog geen ODBC gebruikt, moet na de upgrade naar ODBC worden omgezet; er is geen automatische conversie. Installeer vooraf de ODBC-stuurprogramma's op de digna-host, zie [Het ODBC-stuurprogramma op de digna-host installeren](../../../databases/overview.md#install-the-driver), en houd de eigenschappen van elke verbinding gereed aan de hand van de [technologiehandleidingen](../../../databases/overview.md#technology-guides). De Databricks Legacy-connector bestaat niet meer; zet die verbindingen over naar de [Databricks](../../../databases/databricks_connector_guide.md)-connector.
- **Eén uitvoerbaar bestand.** `dignabackend` en `dignacli` zijn vervangen door het enkele uitvoerbare bestand `digna`, dat de backend en de CLI combineert.
- **config.toml.** De sectie `[encryption]` is verplicht, en `DIGNA_APP_HOST` en `DIGNA_APP_PORT` worden niet meer gelezen: de server haalt zijn adres en poort uit `digna serve`. Vergelijk uw bestand met [Backendconfiguratie](#backend-configuration).

De onderstaande stappen geven aan waar een oudere installatie iets anders nodig heeft. De repository-upgrade in Stap 8 brengt een repository van elke eerdere release rechtstreeks naar 2026.11.

### Upgradeproces

#### Stap 1: Stop de digna-service {: #step-1-stop-the-digna-service }

Open een Opdrachtprompt als Administrator en stop de service met het `digna`-uitvoerbare bestand van uw huidige installatie:

```bash
cd C:\path\to\digna
digna windows stop
```

De service blijft geregistreerd. Het nieuwe uitvoerbare bestand neemt in dezelfde map de plaats in van het oude, zodat de registratie naar het juiste bestand blijft verwijzen.

Als digna op de voorgrond draait, druk dan op ++ctrl+c++ in het Opdrachtprompt-venster.

!!! warning "Upgraden vanaf een release vóór 2026.06"

    Releases vóór 2026.06 registreerden de service met batchbestanden. Stop en deregistreer de service met de batchbestanden van uw huidige installatie, **voordat** u in Stap 2 iets hernoemt:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Noteer het account waaronder de service draaide, en het adres en de poort waarop deze bereikbaar was. U registreert de service in Stap 9 opnieuw.

#### Stap 2: Huidige installatie veiligstellen {: #step-2-backup-current-installation }

Hernoem in uw digna-installatiemap het uitvoerbare bestand en de dashboardmap van uw huidige installatie, zodat de nieuwe release ernaast kan worden uitgerold:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Bewaar `digna_old.exe` totdat u de upgrade hebt geverifieerd, en `dashboard_old` totdat u uw configuratiebestanden eruit hebt teruggezet (zie Stap 4). Daarna kunt u beide verwijderen.

!!! info "Upgraden vanaf een release vóór 2026.06"

    Hernoem in plaats van het uitvoerbare bestand de mappen `dignabackend` en `dignacli`: `ren dignabackend dignabackend_old` en `ren dignacli dignacli_old`. Release 2026.11 gebruikt geen van beide mappen, en ook de `bin`-map met batchbestanden niet.

#### Stap 3: Pak de nieuwe versie uit en deploy {: #step-3-extract-and-deploy-new-version }

1. Pak het nieuwe digna-installatie-ZIP-bestand uit
2. Kopieer het nieuwe `digna`-uitvoerbare bestand en de `dashboard`-map naar uw installatiemap

!!! warning "Belangrijk"

    Noch `config.toml` noch `dashboard/dashboard_config.toml` wordt ooit in het installatie-ZIP opgenomen — het digna-team levert geen van beide bestanden mee. Uw bestaande configuratie blijft bij de upgrade dus onaangeroerd, en de kopieën in de hernoemde `*_old`-mappen zijn de enige die u hebt.

#### Stap 4: Herstel je configuratiebestanden {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 vereist geen wijziging in `config.toml`: een bestand dat met Release 2026.06 werkt, blijft werken. Twee wijzigingen zijn optioneel:

- Voeg een [`[duckdb]`-sectie](#duckdb-section) toe als databaseverbindingen de digna Engine moeten gebruiken en de standaardwaarden ervan niet bij uw host passen.
- Laat de `[app]`-sectie weg als een reverse proxy het dashboard en de backend onder één origin serveert.

!!! warning "Instellingen die digna niet leest"

    Eerdere versies van deze handleiding toonden enkele instellingen die digna niet leest. Ze hebben geen effect, en `config check` vermeldt ze in Stap 6 onder **Unknown keys**. Verwijder of corrigeer ze:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`, `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` en `digna_LOGGING_BACKUP_COUNT` bestaan niet. Verwijder ze.
    - Namen van instellingen zijn hoofdlettergevoelig. digna leest `DIGNA_REPO_HOST`, niet `digna_REPO_HOST`. Schrijf elke naam in hoofdletters, zoals in [Backendconfiguratie](#backend-configuration).

!!! warning "Eenmalige aanmelding: behoud [[oidc_clients]]"

    digna leest providers voor eenmalige aanmelding als een lijst van `[[oidc_clients]]`-items, elk met een eigen `DIGNA_OIDC_KEY`. Als u uw providers hebt omgezet naar `[oidc_clients.<key>]`-secties, zoals een eerdere versie van deze handleiding toonde, zet ze dan terug. `config check` meldt `OIDC config(s)` als FAILED zolang die vorm aanwezig is:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Herhaal het item voor elke provider en houd elke `DIGNA_OIDC_KEY` gelijk aan de `key` in `dashboard_config.toml`. Alleen installaties die eenmalige aanmelding gebruiken, worden hierdoor geraakt.

#### Stap 5: Herlaad de webserver {: #step-5-reload-the-web-server }

Het dashboard bestaat uit statische bestanden, dus uw webserver — en de browser — kan nog steeds de vorige versie serveren. Herlaad of herstart de webserver die de `dashboard`-map host, en herlaad de pagina daarna met een harde vernieuwing (++ctrl+f5++).

#### Stap 6: Configuratie valideren {: #step-6-validate-the-configuration }

Controleer of `config.toml` volledig is voordat u de repository aanraakt:

```bash
digna config check
```

Elke sectie moet OK melden. Los alles op wat als FAILED wordt gemeld, verwijder de sleutels die onder **Unknown keys** staan, en voer het commando opnieuw uit voordat u verdergaat.

#### Stap 7: Vervang het licentiebestand {: #step-7-replace-the-license-file }

Een licentiebestand gaat normaal gesproken mee van de ene release naar de volgende. Release 2026.11 is een uitzondering: deze release voegt twee gelicentieerde modules toe, digna Data Reconciliation en digna Agentic, en een licentie die vóór 2026.11 is uitgegeven, bevat ze niet. Kopieer het `license.toml` dat het digna-team voor Release 2026.11 heeft geleverd naar de installatiemap, ter vervanging van het oude:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Behoud de vorige licentie niet"

    Met de vorige licentie start digna nog wel, maar digna Data Reconciliation en de digna MCP Server blijven uitgeschakeld. Elk commando dat de licentie controleert — `user`, `inspection`, `repo` — breekt af voordat het de repository aanraakt wanneer de controle mislukt. Controleer de nieuwe licentie voordat u verdergaat:

    ```bash
    digna license check
    ```

#### Stap 8: Upgrade het repository-schema {: #step-8-upgrade-the-repository-schema }

Voer in uw digna-installatiemap uit:

```bash
digna repo upgrade
```

Release 2026.11 beheert het repository-schema met geversioneerde migraties. De eerste upgrade vanaf een eerdere release brengt het schema naar de laatste versie van het vorige mechanisme, legt dat vast als startpunt en past daarna de migraties van Release 2026.11 toe. De upgrade eindigt met:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle bestaande gegevens blijven behouden. Voer op elk moment `digna repo check` uit om de toestand van de repository te zien: het commando toont de laatst toegepaste migratie en eventuele openstaande migraties.

!!! warning "digna start niet op een verouderde repository"

    Vanaf Release 2026.11 weigert de server te starten zolang de repository een upgrade nodig heeft, en meldt dat, bijvoorbeeld:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Voer `repo upgrade` uit voordat u de server of de service start.

#### Stap 9: Herstart services {: #step-9-restart-services }

Als digna als Windows-service draait, start deze dan opnieuw:

```bash
cd C:\path\to\digna
digna windows start
```

Als u vanaf een release vóór 2026.06 hebt geüpgraded en de service in Stap 1 hebt gederegistreerd, registreer deze dan eerst opnieuw met het `digna`-uitvoerbare bestand:

```bash
digna windows install --address <address> --port <port>
digna windows start
```

Geef `--address` en `--port` de waarden waarop de oude service bereikbaar was, tenzij u de standaardwaarden `127.0.0.1` en `8000` wilt. Voeg `--account` en `--password` toe als de oude service onder een domeinaccount draaide. Zie [digna als Windows-service uitvoeren](#running-digna-as-a-windows-service) voor de volledige lijst met opties.

Als u handmatig draait, start de server dan opnieuw:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Als u IIS of Tomcat gebruikt, herstart dan de betreffende webserver.

#### Stap 10: Verifieer de upgrade {: #step-10-verify-the-upgrade }

1. Controleer de release van het nieuwe uitvoerbare bestand:

    ```bash
    digna version
    ```

    De eerste regel moet `Release: 2026.11` luiden.

2. Ga naar het digna-dashboard en controleer of de interface correct laadt.
3. Controleer de bestanden in de map `logs` van de installatie op fouten.
4. Test uw databaseverbindingen — zie [Een verbinding testen](../../../databases/overview.md#testing-a-connection). Zet na een upgrade vanaf een release vóór 2026.06 eerst elke verbinding die nog geen ODBC gebruikte om naar ODBC.

Om met de nieuwe modules te beginnen, zie [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Een AI-agent verbinden](../../../platform/agentic/connect_ai_agent.md) voor de digna MCP Server, en [Profileringslocatie](../../../platform/profiling/profiling_location.md) voor de digna Engine.
