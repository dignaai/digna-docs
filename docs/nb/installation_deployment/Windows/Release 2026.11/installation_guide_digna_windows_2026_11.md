---
title: Windows installasjonsveiledning – digna Release 2026.11 | digna Dokumentasjon
description: Trinnvis veiledning for å installere digna Release 2026.11 på Windows — systemkrav, PostgreSQL-oppsett, webserverkonfigurasjon, backend- og dashboard-konfigurasjon, kjøring av digna som Windows-tjeneste og oppgradering fra Release 2026.06.
keywords: digna windows installasjon, digna distribusjonsveiledning, digna backend-oppsett, digna dashboard installasjon, postgresql oppsett, digna windows-tjeneste, digna oppgraderingsveiledning
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.11

**Release:** 2026.11

**Sist oppdatert:** 7. november 2026


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

- **digna**: kjernen i applikasjonen, ansvarlig for å behandle data og utføre kvalitetskontroller. Den samler backend og kommandolinjegrensesnittet i én kjørbar fil og erstatter dermed de separate programmene `dignabackend` og `dignacli` fra tidligere utgivelser.
- **dignadashboard**: Et web-basert grensesnitt hostet på en webserver, som gir en brukervennlig måte å interagere med digna-plattformen og visualisere datakvalitetsmålinger.

### Hva er nytt i Release 2026.11

Denne utgivelsen legger til digna Data Reconciliation, digna Agentic med digna MCP Server, og digna Engine, som kan profilere data inne i digna og kontrollere referanseintegritet mellom ulike databaseteknologier. Se [utgivelsesnotatene](../../../changelog/Release_202611.md) for fullstendige detaljer.

For en installasjon bringer utgivelsen en ny mekanisme for repository-migreringer, en valgfri `[duckdb]`-seksjon i `config.toml` for digna Engine, og en ny lisensfil. [Oppgraderingsavsnittet](#upgrading-to-a-new-release) tar for seg hver av dem.

### Ser du etter macOS eller Linux?

Denne veiledningen dekker Windows. For andre plattformer, se [macOS installasjonsveiledning](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) eller [Linux installasjonsveiledning](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Databasetilkoblinger som bruker digna Engine som profileringssted, profileres på selve
    digna-verten. Planlegg ekstra minne og diskplass for dem, se
    [\[duckdb\]-seksjonen](#duckdb-section).

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

!!! info "Konfigurasjons- og lisensfilene er ikke med i pakken"

    Verken `config.toml` eller `dashboard/dashboard_config.toml` følger med installasjonen — du
    oppretter begge selv, i [Backend-konfigurasjon](#backend-configuration) og
    [Dashboard-konfigurasjon](#dashboard-configuration). `license.toml` følger heller ikke med;
    digna leverer den separat, slik Trinn 3 beskriver.

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

Denne seksjonen konfigurerer cross-origin resource sharing (CORS) mellom dashboardet og backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Verdi | Merknader |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL-er | URL-ene som dashboardet serveres fra. Nettleserforespørsler fra alle andre origins avvises |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrevd, slik at nettleseren sender sesjonscookien med hver forespørsel |

!!! info "[app]-seksjonen er valgfri"

    Fra Release 2026.11 kan begge nøklene, og hele `[app]`-seksjonen, utelates. Dette er riktig
    oppsett når en omvendt proxy serverer dashboardet og backend under samme origin: nettleseren
    gjør da ingen cross-origin-forespørsler, og ingen er tillatt som standard.

#### [repo] Seksjonen

Denne seksjonen konfigurerer tilkoblingen til PostgreSQL-databasen:

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

| Parameter | Verdi | Merknader |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostnavn/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasenavn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Skjema opprettet tidligere |
| `DIGNA_REPO_USER` | `digna_user` | Bruker opprettet i PostgreSQL-oppsettet |
| `DIGNA_REPO_PASSWORD` | Ditt passord | Passord satt under skjemaopprettelsen |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valgfri. SSL-modus for PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valgfri. Antall tilkoblinger digna holder åpne mot repositoriet |

#### [base] Seksjonen

Denne seksjonen inneholder sikkerhets-, cookie- og inspeksjonsinnstillinger:

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

| Parameter | Verdi | Merknader |
|---|---|---|
| `DIGNA_FERNET_KEY` | Verdien vist ovenfor | Nøkkel for krypteringen som tidligere utgivelser brukte. Den må være til stede; behold verdien som vises |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Verten dashboardet nås under. `""` angir ikke noe domene, noe som er riktig bak en proxy som serverer dashboardet og backend under samme origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Må være `true` når digna serveres over HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Holder sesjonscookien utenfor rekkevidde for skript |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `DIGNA_MAX_WORKERS` | Antall CPU-kjerner - 1 | Antall inspeksjoner som kan kjøre samtidig |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Påkrevd. Brukes for lenkene i varslingsmeldinger, så det må være en URL mottakerne kan åpne |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valgfri. Antall sekunder én enkelt spørring mot en kildedatabase kan kjøre før den avbrytes; `0` slår av tidsavbruddet |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valgfri. Antall sekunder det ventes på en tilkobling til en kildedatabase; `0` venter uten tidsbegrensning |

#### [encryption]-seksjonen

Denne seksjonen inneholder nøkkelen som brukes til å kryptere sensitive verdier i repositoryet. Den er **påkrevd** — `config check` rapporterer seksjonen `[encryption]` som FAILED hvis nøkkelen mangler.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Verdi | Notater |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodet nøkkel | Krypterer sensitive verdier som er lagret i digna-repositoryet |

!!! warning "Beskytt config.toml"

    Denne nøkkelen er en fast verdi som er identisk i alle digna-installasjoner, og det er den som dekrypterer de sensitive verdiene i repositoryet ditt. Begrens `config.toml` til kontoen som kjører digna, hold filen utenfor versjonskontroll og delte disker, og utelat den fra enhver sikkerhetskopi som oppbevares mindre sikkert enn selve repositoryet.

#### [logging] Seksjonen

Denne seksjonen konfigurerer loggeadferd:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Verdi | Merknader |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` for produksjon, `DEBUG` for feilsøking. `TRACE`, `WARN` og `ERROR` godtas også |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valgfri. Katalog for de roterende loggfilene, relativt til arbeidskatalogen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valgfri. Antall roterte loggfiler som beholdes |

!!! warning "Behold loggkatalogen når digna kjører som tjeneste"

    En Windows-tjeneste har ingen konsoll, så loggfilene er det eneste som viser hva tjenesten
    gjør. Ikke sett `DIGNA_LOGGING_DIR` til en tom streng, for det slår av loggfilene.

#### [duckdb] Seksjonen (valgfri) {: #duckdb-section }

Nytt i Release 2026.11. Denne seksjonen angir ressursene til **digna Engine**, som profilerer
data inne i digna for databasetilkoblinger med profileringsstedet **digna Engine**, og som kjører
kontroller av referanseintegritet mellom datakilder på ulike databasetilkoblinger. Se
[Profileringssted](../../../platform/profiling/profiling_location.md).

Seksjonen er valgfri. Uten den gjelder standardverdiene nedenfor.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Verdi | Merknader |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Minne, i MB, som én kjøring av digna Engine kan bruke. Opptil `DIGNA_MAX_WORKERS` kjøringer kan være aktive samtidig |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: den midlertidige katalogen til kontoen som kjører digna (`%TEMP%`) | Katalog for midlertidige filer når dataene ikke får plass i minnet |

!!! tip "Dimensjonering av digna Engine"

    Planlegg for opptil `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` minne på
    digna-verten, i tillegg til det digna selv bruker, og for nok ledig diskplass i den midlertidige
    katalogen til å romme den største inspiserte datoen for datakildene som bruker digna Engine.
    Pek `DIGNA_DUCKDB_TEMP_DIRECTORY` mot en disk med så mye plass, skrivbar for kontoen som
    kjører digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Du trenger bare denne seksjonen hvis minst én databasetilkobling bruker digna Engine, eller hvis en
    kontroll av referanseintegritet sammenligner datakilder på ulike tilkoblinger.

---

### Trinn 2: Valider konfigurasjonen

Kontroller at `config.toml` er fullstendig og korrekt bygget opp før du initialiserer repositoryet. Kjør i digna-installasjonskatalogen:

```bash
digna config check
```

Hver seksjon valideres for seg, slik at én enkelt feil ikke skjuler tilstanden til de andre:

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

Rett alt som rapporteres som FAILED, og kjør kommandoen på nytt før du går videre. En WARNING under **Unknown keys** viser nøkler i `config.toml` som digna ikke leser; de har ingen effekt, så fjern dem eller rett stavemåten. Den fullstendige listen over valg finnes i [CLI-referansen](../../../cli/Command_Line_Interface_202611.md).

### Trinn 3: Initialiser repositoriet

1. Åpne Kommandoprompt
2. Naviger til din digna-installasjonsmappe (der `config.toml` og `digna`-kjørbar ligger)
3. Kjør tilkoblingstesten:

```bash
digna repo check
```

På et nytt skjema kobler kommandoen til og rapporterer deretter at det ikke er installert noe repository ennå:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

På dette tidspunktet er det det forventede resultatet: det bekrefter at digna når PostgreSQL og skjemaet. En tilkoblings- eller autentiseringsfeil peker i stedet på `[repo]`-seksjonen eller på PostgreSQL-oppsettet.

### Trinn 4: Installer repositories-skjemaet

I samme mappe, kjør:

```bash
digna repo upgrade
```

Denne kommandoen installerer de nødvendige tabellene i repository-skjemaet og avslutter med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerer og oppgraderer"

    Fra Release 2026.11 installerer `repo upgrade` et nytt repository og oppgraderer et eksisterende.
    `repo install` fungerer fortsatt som et annet navn på den samme kommandoen.

### Trinn 5: Opprett en adminbruker

Administratorbrukeren opprettes direkte mot repository-skjemaet, så serveren trenger ikke å kjøre ennå. Kjør i digna-installasjonskatalogen:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Eksempel:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Dette oppretter en bruker med full administrative rettigheter.

!!! tip "Beste praksis"

    Bruk et sterkt passord med en blanding av store og små bokstaver, tall og spesialtegn.

### Trinn 6: Start digna-serveren

I digna-installasjonsmappen, start serveren med:

```bash
digna serve --address <host> --port <port>
```

**Parametere:**
- `--address` — Serverens hostnavn/IP (standard `127.0.0.1`)
- `--port` — Serverens port (standard `8000`)

Når serveren er oppe, skriver den ut adressen den lytter på:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Serveren opptar terminalen"

    `serve` kjører i forgrunnen og fortsetter til du stopper den med ++ctrl+c++. La den kjøre mens du fullfører oppsettet; for å starte den automatisk ved oppstart, se [Kjøre digna som Windows-tjeneste](#running-digna-as-a-windows-service).

---

## Dashboard-konfigurasjon {: #dashboard-configuration }

### Trinn 1: Deploy dashboardet til webserveren

digna-dashboardet leser sin egen konfigurasjon fra `dashboard/dashboard_config.toml`. Den filen følger ikke med installasjonen — du oppretter den i `dashboard/`-katalogen sammen med dashboardfilene.

Innholdet er beskrevet under [Enkel pålogging](../../../sso/overview.md), som også er der filen trengs: den inneholder påloggingsalternativene dashboardet tilbyr og, for distribusjoner med flere instanser, backend-tilkoblingen.

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

### `windows`-kommandoene

Tjenesten administreres av selve den kjørbare filen `digna`, gjennom underkommandoene `digna windows`.
Det finnes ingen batchfiler å kjøre.

| Kommando | Formål |
|---|---|
| `digna windows install` | Registrerer digna som en Windows-tjeneste |
| `digna windows start` | Starter den registrerte tjenesten |
| `digna windows stop` | Stopper tjenesten som kjører |
| `digna windows uninstall` | Avregistrerer tjenesten |

!!! warning "Administrator påkrevd"

    Alle fire kommandoene må kjøres fra en Kommandoprompt som er åpnet som administrator.

Hver kommando godtar `--name` for å adressere en tjeneste som er registrert under et annet navn enn standardnavnet. Den
fullstendige listen over alternativer finnes i [CLI-referansen](../../../cli/Command_Line_Interface_202611.md).

### Installere tjenesten

1. **Åpne Kommandoprompt som administrator**
   - Høyreklikk Kommandoprompt
   - Velg "Run as Administrator"

2. **Naviger til digna-installasjonskatalogen din**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registrer tjenesten**
   ```bash
   digna windows install
   ```

!!! important "Angi adresse og port med mindre standardverdiene passer for deg"

    `install` lagrer adressen og porten i tjenesteregistreringen, og tjenesten binder seg til
    nøyaktig det som ble lagret. Standardverdiene er `127.0.0.1` og `8000`, som bare godtar tilkoblinger
    fra selve maskinen. Et dashboard på en annen vert kan ikke nå dette, så angi
    adressen backend skal lytte på:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Disse leses ikke fra `config.toml`. For å endre dem senere må du avinstallere tjenesten og
    installere den på nytt med de nye verdiene.

Tjenesten registreres med **automatisk oppstart**, så den starter sammen med Windows. Den starter
ikke umiddelbart — se neste seksjon.

#### Installasjonsalternativer

| Alternativ | Standard | Formål |
|---|---|---|
| `--name` | `digna` | Navnet tjenesten registreres under |
| `--display-name` | `digna` | Navnet som vises i services.msc |
| `--description` | `digna data quality backend` | Beskrivelsen som vises i services.msc |
| `--address` | `127.0.0.1` | Adressen tjenesten binder API-et sitt til |
| `--port` | `8000` | Porten tjenesten binder API-et sitt til |
| `--working-dir` | katalogen til den kjørbare filen `digna` | Katalogen som inneholder `config.toml` og `license.toml`, og som tjenesten bruker som arbeidskatalog |
| `--start-type` | `auto` | `auto` starter sammen med Windows, `manual` starter bare på forespørsel, `disabled` registrerer tjenesten, men nekter å starte den |
| `--account` | `LocalSystem` | Kontoen tjenesten kjører som, f.eks. `DOMAIN\user` eller `.\user` |
| `--password` | | Passordet til `--account` |

!!! tip "Kjøre under en domenekonto"

    `LocalSystem` har ingen nettverksidentitet, så Windows-autentisering mot SQL Server og all
    tilgang til en nettverksressurs vil mislykkes. Installer med `--account` og `--password` der
    tjenesten må nå ressurser som en bestemt bruker.

### Starte og stoppe tjenesten

#### For å starte tjenesten

```bash
digna windows start
```

#### For å stoppe tjenesten

```bash
digna windows stop
```

!!! tip "Tips"

    Stopp alltid tjenesten før du oppdaterer applikasjonsfiler.

### Flytte tjenesten til en ny katalog

Hvis du trenger å flytte digna-installasjonen:

1. **Stopp og avregistrer den nåværende tjenesten**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Flytt applikasjonsfilene**
   - Flytt hele digna-installasjonsmappen til det nye stedet

3. **Registrer tjenesten på nytt fra det nye stedet**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Gjenta eventuelle verdier for `--address`, `--port` eller `--account` som du brukte første gang — den forrige
   registreringen er borte.

4. **Start tjenesten**
   ```bash
   digna windows start
   ```

### Avinstallere tjenesten

1. **Stopp tjenesten som kjører**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Avregistrer tjenesten**
   ```bash
   digna windows uninstall
   ```

digna-serveren er nå avregistrert som en Windows-tjeneste.

---

## Oppgradering til ny utgave {: #upgrading-to-a-new-release }

Denne delen oppgraderer en installasjon av Release 2026.06 til Release 2026.11. Hvis
installasjonen din er eldre, les først [Oppgradere fra en utgivelse før 2026.06](#upgrading-from-a-release-before-2026-06).

### Før du oppgraderer

**Det er obligatorisk å ta backup av digna-repositoriet**

Før du oppgraderer digna, ta backup av repositoriet (PostgreSQL) for å beskytte mot datatap.
En backup sikrer at du kan gjenopprette hvis oppgraderingen møter uventede problemer.

**Be om lisensfilen for Release 2026.11**

Release 2026.11 krever en ny `license.toml`. Be digna-teamet om den før du starter, og
ha den klar til [trinn 7](#step-7-replace-the-license-file).

### Oppgradere fra en utgivelse før 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 innførte tre endringer som fortsatt gjelder når du oppgraderer en eldre installasjon
direkte til 2026.11:

- **Kun ODBC.** digna når hver kildeteknologi via ODBC. Hver databasetilkobling som ennå ikke
  bruker ODBC, må legges om til ODBC etter oppgraderingen; det finnes ingen automatisk
  konvertering. Installer ODBC-driverne på digna-verten på forhånd, se
  [Installer ODBC-driveren på digna-verten](../../../databases/overview.md#install-the-driver),
  og ha egenskapene for hver tilkobling klare fra
  [teknologiveiledningene](../../../databases/overview.md#technology-guides). Databricks Legacy-koblingen
  finnes ikke lenger; flytt disse tilkoblingene til
  [Databricks](../../../databases/databricks_connector_guide.md)-koblingen.
- **Én kjørbar fil.** `dignabackend` og `dignacli` erstattes av den ene kjørbare filen `digna`,
  som samler backend og CLI.
- **config.toml.** `[encryption]`-seksjonen er påkrevd, og `DIGNA_APP_HOST` og
  `DIGNA_APP_PORT` leses ikke lenger: serveren henter adresse og port fra `digna serve`.
  Sammenlign filen din med [Backend-konfigurasjon](#backend-configuration).

Trinnene nedenfor viser hvor en eldre installasjon trenger noe annet. Repository-oppgraderingen i
trinn 8 bringer et repository fra en hvilken som helst tidligere utgivelse direkte til 2026.11.

### Oppgraderingsprosess

#### Trinn 1: Stopp digna-tjenesten {: #step-1-stop-the-digna-service }

Åpne Kommandoprompt som administrator og stopp tjenesten med den kjørbare `digna`-filen fra
den gjeldende installasjonen din:

```bash
cd C:\path\to\digna
digna windows stop
```

Tjenesten forblir registrert. Den nye kjørbare filen tar den gamles plass i samme katalog, så
registreringen peker fortsatt på riktig fil.

Hvis digna kjører i forgrunnen, trykk ++ctrl+c++ i Kommandoprompt-vinduet der den kjører.

!!! warning "Oppgradering fra en utgivelse før 2026.06"

    Utgivelser før 2026.06 registrerte tjenesten med batchfiler. Stopp og avregistrer den med
    batchfilene fra den gjeldende installasjonen, **før** du gir nytt navn til noe i trinn 2:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Noter hvilken konto tjenesten kjørte under, og hvilken adresse og port den lyttet på. Du
    registrerer tjenesten på nytt i trinn 9.

#### Trinn 2: Sikkerhetskopier gjeldende installasjon {: #step-2-backup-current-installation }

Gi den kjørbare filen og dashboard-mappen i den gjeldende installasjonen nye navn i
digna-installasjonskatalogen, slik at den nye utgivelsen kan distribueres ved siden av dem:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Behold `digna_old.exe` til du har verifisert oppgraderingen, og `dashboard_old` til du har gjenopprettet
konfigurasjonsfilene dine fra den (se trinn 4). Deretter kan du slette begge.

!!! info "Oppgradering fra en utgivelse før 2026.06"

    Gi mappene `dignabackend` og `dignacli` nye navn i stedet for den kjørbare filen:
    `ren dignabackend dignabackend_old` og `ren dignacli dignacli_old`. Release 2026.11 bruker ingen av mappene, og heller ikke `bin`-mappen med batchfiler.

#### Trinn 3: Pakk ut og distribuer ny versjon {: #step-3-extract-and-deploy-new-version }

1. Pakk ut den nye digna-installasjons-ZIP-filen
2. Kopier den nye kjørbare `digna`-filen og `dashboard`-mappen til installasjonskatalogen din

!!! warning "Viktig"

    Verken `config.toml` eller `dashboard/dashboard_config.toml` er noensinne inkludert i
    installasjons-ZIP-en — digna-teamet leverer aldri noen av filene. Din eksisterende konfigurasjon
    berøres derfor ikke av oppgraderingen, og kopiene i de omdøpte `*_old`-mappene er de
    eneste du har.

#### Trinn 4: Gjenopprett konfigurasjonsfilene {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 krever ingen endring i `config.toml`: en fil som fungerer med Release 2026.06, fortsetter
å fungere. To endringer er valgfrie:

- Legg til en [`[duckdb]`-seksjon](#duckdb-section) hvis databasetilkoblinger skal bruke digna Engine
  og standardverdiene ikke passer for verten din.
- Utelat `[app]`-seksjonen hvis en omvendt proxy serverer dashboardet og backend under samme
  origin.

!!! warning "Innstillinger som digna ikke leser"

    Tidligere versjoner av denne veiledningen viste noen innstillinger som digna ikke leser. De har ingen
    effekt, og `config check` viser dem under **Unknown keys** i trinn 6. Fjern eller rett
    dem:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` og
      `digna_LOGGING_BACKUP_COUNT` finnes ikke. Fjern dem.
    - Innstillingsnavn skiller mellom store og små bokstaver. digna leser `DIGNA_REPO_HOST`, ikke `digna_REPO_HOST`.
      Skriv hvert navn med store bokstaver, som i [Backend-konfigurasjon](#backend-configuration).

!!! warning "Enkel pålogging: behold [[oidc_clients]]"

    digna leser leverandører for enkel pålogging som en liste med `[[oidc_clients]]`-oppføringer, hver
    med sin egen `DIGNA_OIDC_KEY`. Hvis du har endret leverandørene dine til `[oidc_clients.<key>]`-seksjoner,
    slik en tidligere versjon av denne veiledningen viste, må du endre dem tilbake. `config check`
    rapporterer `OIDC config(s)` som FAILED så lenge den formen er i bruk:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Gjenta oppføringen for hver leverandør, og hold hver `DIGNA_OIDC_KEY` lik `key` i
    `dashboard_config.toml`. Bare installasjoner som bruker enkel pålogging, er berørt.

#### Trinn 5: Last inn webserveren på nytt {: #step-5-reload-the-web-server }

Dashboardet er et sett med statiske filer, så webserveren din — og nettleseren — kan fortsatt
levere den forrige versjonen. Last inn på nytt eller start på nytt den webserveren som er vert for `dashboard`-mappen,
og last deretter inn siden på nytt med en hard oppdatering (++ctrl+f5++).

#### Trinn 6: Valider konfigurasjonen {: #step-6-validate-the-configuration }

Bekreft at `config.toml` er fullstendig før du rører repositoriet:

```bash
digna config check
```

Hver seksjon må rapportere OK. Rett alt som rapporteres som FAILED, fjern nøklene som vises under
**Unknown keys**, og kjør kommandoen på nytt før du går videre.

#### Trinn 7: Erstatt lisensfilen {: #step-7-replace-the-license-file }

En lisensfil følger normalt med fra én utgivelse til den neste. Release 2026.11 er et
unntak: den legger til to lisensierte moduler, digna Data Reconciliation og digna Agentic, og en
lisens utstedt før 2026.11 inneholder dem ikke. Kopier `license.toml` som digna-teamet har levert
for Release 2026.11, til installasjonskatalogen, slik at den erstatter den gamle:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Ikke behold den forrige lisensen"

    Med den forrige lisensen starter digna fortsatt, men digna Data Reconciliation og digna
    MCP Server forblir slått av. Alle kommandoer som kontrollerer lisensen — `user`,
    `inspection`, `repo` — avbrytes før de berører repositoriet når kontrollen feiler. Verifiser
    den nye lisensen før du går videre:

    ```bash
    digna license check
    ```

#### Trinn 8: Oppgrader repository-skjemaet {: #step-8-upgrade-the-repository-schema }

Kjør i digna-installasjonskatalogen:

```bash
digna repo upgrade
```

Release 2026.11 håndterer repository-skjemaet med versjonerte migreringer. Den første oppgraderingen fra
en tidligere utgivelse bringer skjemaet til siste versjon av den tidligere ordningen, registrerer dette som
utgangspunkt og bruker deretter migreringene i Release 2026.11. Den avslutter med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle eksisterende data bevares. For å se tilstanden til repositoriet når som helst, kjør
`digna repo check`: den viser den sist anvendte migreringen og eventuelle ventende migreringer.

!!! warning "digna starter ikke på et utdatert repository"

    Fra Release 2026.11 nekter serveren å starte så lenge repositoriet må oppgraderes, og
    sier ifra om det, for eksempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kjør `repo upgrade` før du starter serveren eller tjenesten.

#### Trinn 9: Start tjenestene på nytt {: #step-9-restart-services }

Hvis digna kjører som en Windows-tjeneste, start den igjen:

```bash
cd C:\path\to\digna
digna windows start
```

Hvis du oppgraderte fra en utgivelse før 2026.06 og avregistrerte tjenesten i trinn 1, må du først
registrere den på nytt med den kjørbare `digna`-filen:

```bash
digna windows install --address <address> --port <port>
digna windows start
```

Gi `--address` og `--port` verdiene den gamle tjenesten lyttet på, med mindre du vil bruke
standardverdiene `127.0.0.1` og `8000`. Legg til `--account` og `--password` hvis den gamle tjenesten
kjørte under en domenekonto. Se
[Kjøre digna som en Windows-tjeneste](#running-digna-as-a-windows-service) for den fullstendige listen over
alternativer.

Hvis du kjører manuelt, start serveren på nytt:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Hvis du bruker IIS eller Tomcat, start den aktuelle webserveren på nytt.

#### Trinn 10: Verifiser oppgraderingen {: #step-10-verify-the-upgrade }

1. Bekreft utgivelsen til den nye kjørbare filen:

    ```bash
    digna version
    ```

    Den første linjen må være `Release: 2026.11`.

2. Åpne digna-dashboardet og bekreft at grensesnittet lastes inn riktig.
3. Sjekk filene i installasjonens `logs`-katalog for feil.
4. Test databasetilkoblingene dine — se
   [Teste en tilkobling](../../../databases/overview.md#testing-a-connection). Etter en oppgradering
   fra en utgivelse før 2026.06 legger du først om hver tilkobling som ikke allerede brukte ODBC, til
   ODBC.

For å komme i gang med de nye modulene, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Koble til en AI-agent](../../../platform/agentic/connect_ai_agent.md) for digna MCP Server, og
[Profileringssted](../../../platform/profiling/profiling_location.md) for digna Engine.
