---
title: Windows-installationsvejledning – digna Release 2026.11 | digna-dokumentation
description: Trin-for-trin vejledning til installation af digna Release 2026.11 på Windows — systemkrav, PostgreSQL-opsætning, webserverkonfiguration, backend- og dashboard-konfiguration, kørsel af digna som Windows-service og opgradering fra Release 2026.06.
keywords: digna Windows-installation, digna udrulningsvejledning, digna backend-opsætning, digna dashboard-installation, postgresql-opsætning, digna Windows-service, digna opgraderingsvejledning
image: /assets/logo_square.png
---

# Windows-installationsvejledning for digna Release 2026.11

**Release:** 2026.11

**Senest opdateret:** 7. november 2026


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

- **digna**: applikationens kerne, ansvarlig for at behandle data og udføre kvalitetskontroller. Den samler backend og kommandolinjegrænsefladen i én eksekverbar fil og erstatter dermed de separate programmer `dignabackend` og `dignacli` fra tidligere releases.
- **dignadashboard**: Et webbaseret interface hostet på en webserver, som giver en brugervenlig måde at interagere med digna-platformen og visualisere datakvalitetsmålinger.

### Hvad er nyt i Release 2026.11

Denne release tilføjer digna Data Reconciliation, digna Agentic med digna MCP Server samt digna Engine, som kan profilere data inde i digna og kontrollere referentiel integritet mellem forskellige databaseteknologier. Se [release notes](../../../changelog/Release_202611.md) for fulde detaljer.

For en installation bringer releasen en ny migreringsmekanisme for repositoriet, en valgfri `[duckdb]`-sektion i `config.toml` til digna Engine og en ny licensfil. [Opgraderingsafsnittet](#upgrading-to-a-new-release) gennemgår hver af dem.

### Leder du efter macOS eller Linux?

Denne vejledning dækker Windows. For andre platforme, se [macOS-installationsvejledningen](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) eller [Linux-installationsvejledningen](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Databaseforbindelser, der bruger digna Engine som profileringssted, profileres på selve
    digna-værten. Planlæg ekstra hukommelse og diskplads til dem, se
    [\[duckdb\]-sektionen](#duckdb-section).

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

!!! info "Konfigurations- og licensfilerne er ikke med i pakken"

    Hverken `config.toml` eller `dashboard/dashboard_config.toml` følger med installationen — du
    opretter begge selv, i [Backend-konfiguration](#backend-configuration) og
    [Dashboard-konfiguration](#dashboard-configuration). `license.toml` følger heller ikke med;
    digna leverer den separat, som beskrevet i Trin 3.

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

Denne sektion konfigurerer cross-origin resource sharing (CORS) mellem dashboardet og backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL'er | De URL'er, dashboardet leveres fra. Browseranmodninger fra enhver anden origin afvises |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrævet, så browseren sender sessionscookien med hver anmodning |

!!! info "Sektionen [app] er valgfri"

    Fra Release 2026.11 kan begge nøgler, og hele sektionen `[app]`, udelades. Det er den
    rigtige opsætning, når en reverse proxy leverer dashboardet og backend under én origin:
    browseren foretager så ingen cross-origin-anmodninger, og som standard tillades ingen.

#### [repo] Sektionen

Denne sektion konfigurerer forbindelsen til PostgreSQL-databasen:

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

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostnavn/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasenavn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema oprettet tidligere |
| `DIGNA_REPO_USER` | `digna_user` | Bruger oprettet i PostgreSQL-opsætningen |
| `DIGNA_REPO_PASSWORD` | Dit password | Password sat under schema-oprettelsen |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valgfri. PostgreSQL SSL-tilstand: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valgfri. Antal forbindelser, digna holder åbne til repositoriet |

#### [base] Sektionen

Denne sektion indeholder indstillinger for sikkerhed, cookies og inspektioner:

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

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_FERNET_KEY` | Værdien vist ovenfor | Nøgle til den kryptering, som tidligere releases brugte. Den skal være til stede; behold den viste værdi |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Den vært, dashboardet tilgås under. `""` angiver intet domæne, hvilket er rigtigt bag en proxy, der leverer dashboardet og backend under én origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Skal være `true`, når digna leveres over HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Holder sessionscookien uden for scripts' rækkevidde |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `DIGNA_MAX_WORKERS` | Antal CPU-kerner - 1 | Antal inspektioner, der må køre samtidig |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Påkrævet. Bruges til linkene i notifikationsbeskeder, så det skal være en URL, modtagerne kan åbne |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valgfri. Antal sekunder, en enkelt forespørgsel mod en kildedatabase må køre, før den afbrydes; `0` deaktiverer timeout |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valgfri. Antal sekunder, der ventes på en forbindelse til en kildedatabase; `0` venter ubegrænset |

#### [encryption] Sektion

Denne sektion indeholder nøglen, der bruges til at kryptere følsomme værdier i repositoryet. Den er **påkrævet** — `config check` rapporterer sektionen `[encryption]` som FAILED, hvis nøglen mangler.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodet nøgle | Krypterer følsomme værdier, der er gemt i digna-repositoryet |

!!! warning "Beskyt config.toml"

    Denne nøgle er en fast værdi, der er identisk i alle digna-installationer, og det er den, der dekrypterer de følsomme værdier i dit repository. Begræns `config.toml` til den konto, der kører digna, hold filen uden for versionsstyring og delte drev, og udelad den fra enhver sikkerhedskopi, der opbevares mindre sikkert end selve repositoryet.

#### [logging] Sektionen

Denne sektion konfigurerer logningsadfærd:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` til produktion, `DEBUG` til fejlfinding. `TRACE`, `WARN` og `ERROR` accepteres også |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valgfri. Mappe til de roterende logfiler, relativt til arbejdsmappen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valgfri. Antal roterede logfiler, der beholdes |

!!! warning "Behold logmappen, når digna kører som service"

    En Windows-service har ingen konsol, så logfilerne er den eneste registrering af, hvad servicen
    gør. Sæt ikke `DIGNA_LOGGING_DIR` til en tom streng, da det slår logfilerne fra.

#### [duckdb] Sektion (valgfri) {: #duckdb-section }

Nyt i Release 2026.11. Denne sektion fastlægger ressourcerne for **digna Engine**, som profilerer
data inde i digna for databaseforbindelser, hvis profileringssted er **digna Engine**, og
kører kontroller af referentiel integritet mellem datakilder på forskellige databaseforbindelser. Se
[Profileringssted](../../../platform/profiling/profiling_location.md).

Sektionen er valgfri. Uden den gælder standardværdierne nedenfor.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Værdi | Noter |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Hukommelse i MB, som én kørsel af digna Engine må bruge. Op til `DIGNA_MAX_WORKERS` kørsler kan være aktive samtidig |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: den midlertidige mappe for den konto, der kører digna (`%TEMP%`) | Mappe til midlertidige filer, når data ikke kan være i hukommelsen |

!!! tip "Dimensionering af digna Engine"

    Planlæg op til `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` hukommelse på digna-værten
    ud over det, digna selv bruger, og nok ledig diskplads i den midlertidige mappe til at rumme
    den største inspicerede dato blandt de datakilder, der bruger digna Engine.
    Lad `DIGNA_DUCKDB_TEMP_DIRECTORY` pege på en disk med den plads, som den konto, der kører
    digna, kan skrive til:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Du har kun brug for denne sektion, hvis mindst én databaseforbindelse bruger digna Engine, eller
    hvis en kontrol af referentiel integritet sammenligner datakilder på forskellige forbindelser.

---

### Trin 2: Validér konfigurationen

Kontrollér, at `config.toml` er fuldstændig og korrekt opbygget, før du initialiserer repositoryet. Kør i din digna-installationsmappe:

```bash
digna config check
```

Hver sektion valideres for sig, så en enkelt fejl ikke skjuler tilstanden af de øvrige:

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

Ret alt, der rapporteres som FAILED, og kør kommandoen igen, før du fortsætter. En WARNING under **Unknown keys** viser nøgler i `config.toml`, som digna ikke læser; de har ingen effekt, så fjern dem eller ret deres stavemåde. Den fulde liste over muligheder findes i [CLI-referencen](../../../cli/Command_Line_Interface_202611.md).

### Trin 3: Initialiser repositoriet

1. Åbn Kommandoprompt
2. Skift til din digna-installationsmappe (hvor `config.toml` og den `digna`-eksekverbare fil ligger)
3. Kør forbindelsestesten:

```bash
digna repo check
```

På et nyt schema opretter kommandoen forbindelse og melder derefter, at der endnu ikke er installeret noget repository:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

På dette tidspunkt er det det forventede resultat: det bekræfter, at digna når PostgreSQL og schemaet. En forbindelses- eller godkendelsesfejl peger i stedet på sektionen `[repo]` eller på PostgreSQL-opsætningen.

### Trin 4: Installer repository-schemaet

I samme mappe, kør:

```bash
digna repo upgrade
```

Denne kommando installerer de nødvendige tabeller i repository-schemaet og afslutter med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerer og opgraderer"

    Fra Release 2026.11 installerer `repo upgrade` et nyt repository og opgraderer et eksisterende.
    `repo install` virker stadig som et andet navn for den samme kommando.

### Trin 5: Opret en admin-bruger

1. Åbn et **nyt** Kommandoprompt-vindue
2. Skift til din digna-installationsmappe
3. Kør følgende kommando for at oprette en admin-bruger:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Eksempel:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Dette opretter en bruger med fulde administrative rettigheder.

!!! tip "Bedste praksis"

    Brug en stærk adgangskode med en blanding af store og små bogstaver, tal og specialtegn.

---

### Trin 6: Start digna-serveren

I digna-installationsmappen, start serveren med:

```bash
digna serve --address <host> --port <port>
```

**Parametre:**
- `--address` — Serverens hostnavn/IP (standard `127.0.0.1`)
- `--port` — Serverens port (standard `8000`)

Når serveren er oppe, udskriver den den adresse, den lytter på:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Serveren optager terminalen"

    `serve` kører i forgrunden og fortsætter, indtil du stopper den med ++ctrl+c++. Lad den køre, mens du færdiggør opsætningen; for at starte den automatisk ved opstart, se [Kør digna som Windows-tjeneste](#running-digna-as-a-windows-service).

## Dashboard-konfiguration {: #dashboard-configuration }

### Trin 1: Deploy dashboardet til webserveren

digna-dashboardet læser sin egen konfiguration fra `dashboard/dashboard_config.toml`. Den fil følger ikke med installationen — du opretter den i `dashboard/`-mappen sammen med dashboardfilerne.

Dens indhold er beskrevet under [Single Sign-On](../../../sso/overview.md), som også er der, hvor filen er nødvendig: den indeholder de login-muligheder, dashboardet tilbyder, og ved multi-instance udrulninger backend-forbindelsen.

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

### `windows`-kommandoerne

Servicen administreres af selve den eksekverbare `digna`-fil via underkommandoerne `digna windows`.
Der er ingen batch-filer at køre.

| Kommando | Formål |
|---|---|
| `digna windows install` | Registrerer digna som en Windows-service |
| `digna windows start` | Starter den registrerede service |
| `digna windows stop` | Stopper den kørende service |
| `digna windows uninstall` | Fjerner service-registreringen |

!!! warning "Administratorrettigheder kræves"

    Alle fire kommandoer skal køres fra en Kommandoprompt, der er åbnet som Administrator.

Hver kommando accepterer `--name` for at adressere en service, der er registreret under et ikke-standardnavn. Den fulde
liste over indstillinger findes i [CLI-referencen](../../../cli/Command_Line_Interface_202611.md).

### Installation af servicen

1. **Åbn Kommandoprompt som Administrator**
   - Højreklik på Kommandoprompt
   - Vælg "Kør som administrator"

2. **Skift til din digna-installationsmappe**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registrer servicen**
   ```bash
   digna windows install
   ```

!!! important "Angiv adresse og port, medmindre standardværdierne passer dig"

    `install` gemmer adressen og porten i service-registreringen, og servicen binder til
    præcis det, der blev gemt. Standardværdierne er `127.0.0.1` og `8000`, som kun accepterer forbindelser
    fra selve maskinen. Et dashboard på en anden vært kan ikke nå det, så angiv den
    adresse, backend'en skal lytte på:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Disse læses ikke fra `config.toml`. For at ændre dem senere skal du afinstallere servicen og
    installere den igen med de nye værdier.

Servicen registreres med **automatisk opstart**, så den starter sammen med Windows. Den starter ikke
umiddelbart — se næste afsnit.

#### Installationsindstillinger

| Indstilling | Standard | Formål |
|---|---|---|
| `--name` | `digna` | Navn, servicen registreres under |
| `--display-name` | `digna` | Navn, der vises i services.msc |
| `--description` | `digna data quality backend` | Beskrivelse, der vises i services.msc |
| `--address` | `127.0.0.1` | Adresse, servicen binder sin API til |
| `--port` | `8000` | Port, servicen binder sin API til |
| `--working-dir` | mappen med den eksekverbare `digna`-fil | Mappe med `config.toml` og `license.toml`, som servicen bruger som arbejdsmappe |
| `--start-type` | `auto` | `auto` starter sammen med Windows, `manual` starter kun på anmodning, `disabled` registrerer servicen, men nægter at starte den |
| `--account` | `LocalSystem` | Konto, servicen kører som, f.eks. `DOMAIN\user` eller `.\user` |
| `--password` | | Adgangskode til `--account` |

!!! tip "Kørsel under en domænekonto"

    `LocalSystem` har ingen netværksidentitet, så Windows-godkendelse mod SQL Server og enhver
    adgang til et netværksshare vil mislykkes. Installer med `--account` og `--password`, hvor
    servicen skal tilgå ressourcer som en bestemt bruger.

### Start og stop af servicen

#### For at starte servicen

```bash
digna windows start
```

#### For at stoppe servicen

```bash
digna windows stop
```

!!! tip "Tip"

    Stop altid servicen før opdatering af applikationsfiler.

### Flytning af servicen til en ny mappe

Hvis du skal flytte digna-installationen:

1. **Stop og afregistrer den nuværende service**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Flyt applikationsfilerne**
   - Flyt hele digna-installationsmappen til den nye placering

3. **Registrer servicen igen fra den nye placering**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Gentag de værdier for `--address`, `--port` eller `--account`, du brugte første gang — den tidligere
   registrering er væk.

4. **Start servicen**
   ```bash
   digna windows start
   ```

### Afinstallation af servicen

1. **Stop den kørende service**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Afregistrer servicen**
   ```bash
   digna windows uninstall
   ```

Digna-serveren er nu fjernet som en Windows-service.

---

## Opgradering til en ny release {: #upgrading-to-a-new-release }

Dette afsnit opgraderer en installation af Release 2026.06 til Release 2026.11. Hvis din
installation er ældre, så læs først [Opgradering fra en release før 2026.06](#upgrading-from-a-release-before-2026-06).

### Før du opgraderer

**Det er obligatorisk at lave en backup af digna-repositoriet**

Før du opgraderer digna, skal du sikkerhedskopiere dit repository (PostgreSQL) for at beskytte imod datatab.
En backup sikrer, at du kan gendanne, hvis opgraderingen støder på uventede problemer.

**Anmod om licensfilen til Release 2026.11**

Release 2026.11 kræver en ny `license.toml`. Anmod digna-teamet om den, før du starter, og hav
den klar til [Trin 7](#step-7-replace-the-license-file).

### Opgradering fra en release før 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 bragte tre ændringer, som stadig gælder, når du opgraderer en ældre installation
direkte til 2026.11:

- **Kun ODBC.** digna når hver kildeteknologi via ODBC. Hver databaseforbindelse, der endnu ikke
  bruger ODBC, skal lægges om til ODBC efter opgraderingen; der er ingen automatisk
  konvertering. Installér ODBC-driverne på digna-værten på forhånd, se
  [Installér ODBC-driveren på digna-værten](../../../databases/overview.md#install-the-driver),
  og hav egenskaberne for hver forbindelse klar fra
  [teknologivejledningerne](../../../databases/overview.md#technology-guides). Databricks Legacy-connectoren
  findes ikke længere; flyt disse forbindelser til
  [Databricks](../../../databases/databricks_connector_guide.md)-connectoren.
- **Én eksekverbar fil.** `dignabackend` og `dignacli` er erstattet af den enkelte eksekverbare fil `digna`,
  som samler backend og CLI.
- **config.toml.** Sektionen `[encryption]` er påkrævet, og `DIGNA_APP_HOST` og
  `DIGNA_APP_PORT` læses ikke længere: serveren henter sin adresse og port fra `digna serve`.
  Sammenlign din fil med [Backend-konfiguration](#backend-configuration).

Trinene nedenfor angiver, hvor en ældre installation kræver noget andet. Opgraderingen af
repositoriet i Trin 8 bringer et repository fra enhver tidligere release direkte til 2026.11.

### Opgraderingsproces

#### Trin 1: Stop digna-servicen {: #step-1-stop-the-digna-service }

Åbn en Kommandoprompt som administrator, og stop servicen med den eksekverbare `digna`-fil fra
din nuværende installation:

```bash
cd C:\path\to\digna
digna windows stop
```

Servicen forbliver registreret. Den nye eksekverbare fil træder i stedet for den gamle i samme
mappe, så registreringen fortsat peger på den rigtige fil.

Hvis digna kører i forgrunden, tryk ++ctrl+c++ i dets Kommandoprompt-vindue.

!!! warning "Opgradering fra en release før 2026.06"

    Releases før 2026.06 registrerede servicen med batch-filer. Stop og afregistrer den med
    batch-filerne fra din nuværende installation, **før** du omdøber noget i Trin 2:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Notér den konto, servicen kørte under, samt den adresse og port, den kørte på. Du
    registrerer servicen igen i Trin 9.

#### Trin 2: Sikkerhedskopiér nuværende installation {: #step-2-backup-current-installation }

Omdøb den eksekverbare fil og dashboard-mappen i din nuværende installation i digna-installationsmappen,
så den nye release kan udrulles ved siden af dem:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Behold `digna_old.exe`, indtil du har verificeret opgraderingen, og `dashboard_old`, indtil du har gendannet
dine konfigurationsfiler fra den (se Trin 4). Derefter kan du slette begge.

!!! info "Opgradering fra en release før 2026.06"

    Omdøb mapperne `dignabackend` og `dignacli` i stedet for den eksekverbare fil:
    `ren dignabackend dignabackend_old` og `ren dignacli dignacli_old`. Release 2026.11 bruger ingen af mapperne og heller ikke mappen `bin` med batch-filer.

#### Trin 3: Udpak og deploy ny version {: #step-3-extract-and-deploy-new-version }

1. Pak den nye digna-installations-ZIP-fil ud
2. Kopiér den nye `digna`-eksekverbare fil og `dashboard`-mappen til din installationsmappe

!!! warning "Vigtigt"

    Hverken `config.toml` eller `dashboard/dashboard_config.toml` er nogensinde inkluderet i
    installations-ZIP'en — digna-teamet leverer aldrig nogen af filerne. Din eksisterende konfiguration
    berøres derfor ikke af opgraderingen, og kopierne i de omdøbte `*_old`-mapper er de
    eneste, du har.

#### Trin 4: Gendan dine konfigurationsfiler {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 kræver ingen ændring af `config.toml`: en fil, der virker med Release 2026.06,
virker fortsat. To ændringer er valgfrie:

- Tilføj en [`[duckdb]`-sektion](#duckdb-section), hvis databaseforbindelser skal bruge digna Engine,
  og dens standardværdier ikke passer til din vært.
- Udelad sektionen `[app]`, hvis en reverse proxy leverer dashboardet og backend under én
  origin.

!!! warning "Indstillinger, som digna ikke læser"

    Tidligere versioner af denne vejledning viste nogle indstillinger, som digna ikke læser. De har ingen
    effekt, og `config check` viser dem under **Unknown keys** i Trin 6. Fjern eller ret
    dem:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` og
      `digna_LOGGING_BACKUP_COUNT` findes ikke. Fjern dem.
    - Der skelnes mellem store og små bogstaver i indstillingsnavne. digna læser `DIGNA_REPO_HOST`, ikke `digna_REPO_HOST`.
      Skriv alle navne med store bogstaver som i [Backend-konfiguration](#backend-configuration).

!!! warning "Single sign-on: behold [[oidc_clients]]"

    digna læser single sign-on-udbydere som en liste af `[[oidc_clients]]`-poster, hver med sin egen
    `DIGNA_OIDC_KEY`. Hvis du har ændret dine udbydere til `[oidc_clients.<key>]`-sektioner, som en
    tidligere version af denne vejledning viste, så ændr dem tilbage. `config check` rapporterer
    `OIDC config(s)` som FAILED, så længe den form findes:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Gentag posten for hver udbyder, og hold hver `DIGNA_OIDC_KEY` identisk med `key` i
    `dashboard_config.toml`. Kun installationer, der bruger single sign-on, er berørt.

#### Trin 5: Genindlæs webserveren {: #step-5-reload-the-web-server }

Dashboardet er et sæt statiske filer, så din webserver — og browseren — kan stadig
levere den tidligere version. Genindlæs eller genstart den webserver, der hoster `dashboard`-
mappen, og genindlæs derefter siden med en hård opdatering (++ctrl+f5++).

#### Trin 6: Validér konfigurationen {: #step-6-validate-the-configuration }

Bekræft, at `config.toml` er fuldstændig, før du rører repositoryet:

```bash
digna config check
```

Hver sektion skal rapportere OK. Ret alt, der rapporteres som FAILED, fjern de nøgler, der vises under
**Unknown keys**, og kør kommandoen igen, før du fortsætter.

#### Trin 7: Udskift licensfilen {: #step-7-replace-the-license-file }

En licensfil overføres normalt fra én release til den næste. Release 2026.11 er en
undtagelse: den tilføjer to licenserede moduler, digna Data Reconciliation og digna Agentic, og en
licens udstedt før 2026.11 indeholder dem ikke. Kopiér den `license.toml`, som digna-teamet har
leveret til Release 2026.11, til installationsmappen, så den erstatter den gamle:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Behold ikke den tidligere licens"

    Med den tidligere licens starter digna stadig, men digna Data Reconciliation og digna
    MCP Server forbliver slået fra. Alle kommandoer, der kontrollerer licensen — `user`,
    `inspection`, `repo` — afbrydes, før de rører repositoryet, når kontrollen fejler. Bekræft
    den nye licens, før du går videre:

    ```bash
    digna license check
    ```

#### Trin 8: Opgrader repository-schemaet {: #step-8-upgrade-the-repository-schema }

Kør i din digna-installationsmappe:

```bash
digna repo upgrade
```

Release 2026.11 styrer repository-schemaet med versionerede migreringer. Den første opgradering fra
en tidligere release bringer schemaet til den sidste version i den tidligere ordning, registrerer den som
sit udgangspunkt og anvender derefter migreringerne fra Release 2026.11. Den afslutter med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle eksisterende data bevares. For at se repositoriets tilstand når som helst, kør
`digna repo check`: den viser den senest anvendte migrering og eventuelle ventende.

!!! warning "digna starter ikke på et forældet repository"

    Fra Release 2026.11 nægter serveren at starte, så længe repositoriet kræver en opgradering, og
    siger det, for eksempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kør `repo upgrade`, før du starter serveren eller servicen.

#### Trin 9: Genstart services {: #step-9-restart-services }

Hvis digna kører som Windows-service, start den igen:

```bash
cd C:\path\to\digna
digna windows start
```

Hvis du opgraderede fra en release før 2026.06 og afregistrerede servicen i Trin 1, så registrer
den først igen med den eksekverbare `digna`-fil:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Giv `--address` og `--port` de værdier, den gamle service kørte på, medmindre du ønsker
standardværdierne `127.0.0.1` og `8000`. Tilføj `--account` og `--password`, hvis den gamle service kørte
under en domænekonto. Se
[Kørsel af digna som en Windows-service](#running-digna-as-a-windows-service) for den fulde liste
over indstillinger.

Hvis du kører manuelt, genstart serveren:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Hvis du bruger IIS eller Tomcat, genstart den pågældende webserver.

#### Trin 10: Bekræft opgraderingen {: #step-10-verify-the-upgrade }

1. Bekræft releasen af den nye eksekverbare fil:

    ```bash
    digna version
    ```

    Den første linje skal lyde `Release: 2026.11`.

2. Tilgå digna-dashboardet, og bekræft, at interfacet indlæses korrekt.
3. Tjek filerne i installationens `logs`-mappe for fejl.
4. Test dine databaseforbindelser — se
   [Test en forbindelse](../../../databases/overview.md#testing-a-connection). Efter en opgradering
   fra en release før 2026.06 skal du først lægge hver forbindelse, der ikke allerede brugte ODBC, om til
   ODBC.

For at komme i gang med de nye moduler, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Forbind en AI-agent](../../../platform/agentic/connect_ai_agent.md) for digna MCP Server og
[Profileringssted](../../../platform/profiling/profiling_location.md) for digna Engine.
