# macOS installasjonsveiledning for digna Release 2026.11

**Release:** 2026.11

**Sist oppdatert:** 7. november 2026


---

## Innholdsfortegnelse

1. [Introduksjon](#introduction)
2. [Systemkrav](#system-requirements)
3. [Forberedelser før installasjon](#pre-installation-setup)
4. [PostgreSQL-serveroppsett](#postgresql-server-setup)
5. [Webserverkonfigurasjon](#web-server-configuration)
6. [Første installasjon](#initial-installation)
7. [Backend-konfigurasjon](#backend-configuration)
8. [Dashboard-konfigurasjon](#dashboard-configuration)
9. [Kjøre digna som en bakgrunnstjeneste](#running-digna-as-a-background-service)
10. [Oppgradere til en ny release](#upgrading-to-a-new-release)

---

## Introduksjon {: #introduction }

### Om digna

digna er en omfattende, AI-drevet plattform designet for å optimalisere datakvalitetsstyring på tvers av ulike dataomgivelser som warehouses, lakes og lakehouses. Bygget for høy skalerbarhet og tilpasningsevne, møter digna moderne datautfordringer gjennom automatisering, sanntidsovervåking og anomalideteksjon.

digna består av to hovedkomponenter:

- **digna**: kjernen i applikasjonen, ansvarlig for å behandle data og utføre kvalitetskontroller. Den samler backend og kommandolinjegrensesnittet i én kjørbar fil og erstatter dermed de separate programmene `dignabackend` og `dignacli` fra tidligere utgivelser.
- **dignadashboard**: Et nettbasert grensesnitt hostet på en webserver, som gir en brukervennlig måte å samhandle med digna-plattformen og visualisere datakvalitetsmetrikker.

### Hva er nytt i Release 2026.11

Denne utgivelsen legger til digna Data Reconciliation, digna Agentic med digna MCP Server, og digna Engine, som kan profilere data inne i digna og kontrollere referanseintegritet mellom ulike databaseteknologier. Se [utgivelsesnotatene](../../../changelog/Release_202611.md) for fullstendige detaljer.

For en installasjon bringer utgivelsen en ny mekanisme for repository-migreringer, en valgfri `[duckdb]`-seksjon i `config.toml` for digna Engine, og en ny lisensfil. [Oppgraderingsavsnittet](#upgrading-to-a-new-release) tar for seg hver av dem.

### Ser du etter Windows eller Linux?

Denne veiledningen dekker macOS. For andre plattformer, se [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) eller [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Systemkrav {: #system-requirements }

Før du begynner installasjonen, sørg for at systemet ditt møter følgende minimumskrav:

| Krav | Spesifikasjon |
|---|---|
| **Operativsystem** | macOS 13 (Ventura) eller nyere |
| **Arkitektur** | Apple Silicon (arm64) eller Intel (x86_64) |
| **Minne (Minimalt oppsett)** | 16 GB RAM |
| **Diskplass** | 10 GB tilgjengelig lagring |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Webserver** | nginx, Apache httpd eller tilsvarende |
| **Kommandolinjeverktøy** | Xcode Command Line Tools (kreves av Homebrew) |

!!! info "digna Engine"

    Databasetilkoblinger som bruker digna Engine som profileringssted, profileres på selve
    digna-verten. Planlegg ekstra minne og diskplass for dem, se
    [\[duckdb\]-seksjonen](#duckdb-section).

### Databaseinstallasjonsvalg

**Hvis PostgreSQL allerede er installert:**
Du kan legge til en ny database for digna i din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskin som digna:**

!!! info "Anbefalte spesifikasjoner"

    - **Minne**: 32 GB RAM (i stedet for 16 GB)
    - **Diskplass**: 50 GB tilgjengelig lagring (i stedet for 10 GB)

    Disse høyere spesifikasjonene tar hensyn til både digna og PostgreSQL-databasen som kjører samtidig.

### Sjekke arkitekturen din

Flere stier i denne veiledningen varierer mellom Apple Silicon og Intel-Mac. For å sjekke hvilken du har, åpne **Terminal** og kjør:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installeres til `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installeres til `/usr/local`.

!!! tip "Tips"

    I stedet for å hardkode en av stiene, bruker denne veiledningen `$(brew --prefix)`, som utvides til riktig plassering på begge arkitekturer. Du kan kopiere kommandoene ordrett.

---

## Forberedelser før installasjon {: #pre-installation-setup }

Før du installerer digna, sørg for at tre viktige forutsetninger er på plass:

1. **Homebrew** – pakkebehandleren som brukes til å installere komponentene nedenfor
2. **PostgreSQL Server** – for lagring av beregnede metrikker og ytelsesdata
3. **Webserver** – for hosting av digna Dashboard

Hvis disse komponentene ikke allerede er konfigurert, følg seksjonene nedenfor for å installere og konfigurere dem.

### Installere Homebrew

Homebrew er standard pakkebehandler for macOS og brukes gjennom hele denne veiledningen for å installere PostgreSQL og nginx.

#### Trinn 1: Sjekk om Homebrew allerede er installert

Åpne **Terminal** (trykk `Cmd + Space`, skriv `Terminal`, trykk Enter) og kjør:

```bash
brew --version
```

Hvis et versjonsnummer returneres, hopp til avsnittet om [PostgreSQL-serveroppsett](#postgresql-server-setup).

#### Trinn 2: Installer Homebrew

Hvis kommandoen ikke ble funnet, installer Homebrew ved å følge instruksjonene på [offisielle Homebrew-nettsiden](https://brew.sh). Installeringsprogrammet installerer også Xcode Command Line Tools hvis de ikke allerede er til stede.

#### Trinn 3: Legg Homebrew til i PATH

På Apple Silicon skriver installasjonsprogrammet to kommandoer for å legge Homebrew til ditt shell-miljø. Kjør dem som angitt, og bekreft deretter:

```bash
brew --prefix
```

Dette skal skrive ut `/opt/homebrew` på Apple Silicon eller `/usr/local` på Intel.

---

## PostgreSQL-serveroppsett {: #postgresql-server-setup }

### Hvis du allerede har PostgreSQL

Hvis PostgreSQL allerede er installert og kjører på din lokale maskin, eller hvis du bruker en administrert ekstern PostgreSQL-server, kan du hoppe til neste avsnitt: [Webserverkonfigurasjon](#web-server-configuration).

### Installasjonsalternativer

macOS tilbyr to enkle måter å installere PostgreSQL på. Velg **én**:

- [Homebrew](#postgresql-homebrew) — kommandolinjeinstallasjon, anbefales for serverdistribusjoner
- [Postgres.app](#postgresql-app) — grafisk installasjon, praktisk for lokal evaluering

### Installere PostgreSQL med Homebrew {: #postgresql-homebrew }

#### Trinn 1: Installer PostgreSQL-formelen

```bash
brew install postgresql@16
```

#### Trinn 2: Legg PostgreSQL til i PATH

Versjonsbundne PostgreSQL-formler er *keg-only*, som betyr at Homebrew ikke lenker kommandoene deres inn i PATH automatisk. Legg dem til selv:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Merk"

    Dette antar standard `zsh`-shell brukt av macOS. Hvis du bruker `bash`, legg til samme linje i `~/.bash_profile` i stedet.

#### Trinn 3: Start PostgreSQL-tjenesten

```bash
brew services start postgresql@16
```

Dette starter PostgreSQL umiddelbart og konfigurerer den til å starte automatisk når du logger inn.

#### Trinn 4: Verifiser installasjonen

```bash
psql --version
```

Du skal se PostgreSQL-versjonen hvis installasjonen var vellykket.

#### Trinn 5: Koble til serveren

```bash
psql postgres
```

!!! warning "Viktig — macOS skiller seg fra Windows her"

    Windows-installasjonen ber deg opprette en `postgres` superuser og passord. Homebrew gjør ikke det. I stedet opprettes en superbruker med navnet til din **macOS-konto**, uten passord, tilgjengelig kun fra lokal maskin.

    Dette betyr at det ikke finnes en `postgres`-rolle på en fersk Homebrew-installasjon. Bruk ditt eget kontonavn når du trenger en superbruker, og opprett en eksplisitt digna-bruker som beskrevet i [Første installasjon](#initial-installation).

#### Trinn 6: Bekreft porten

Standard PostgreSQL-port er `5432`. For å bekrefte hvilken port serveren lytter på:

```bash
psql postgres -c "SHOW port;"
```

Noter verdien — du vil trenge den når du konfigurerer digna-backenden.

### Installere PostgreSQL med Postgres.app {: #postgresql-app }

Hvis du foretrekker en grafisk installasjon:

1. Last ned [Postgres.app](https://postgresapp.com) og dra den til **Applications**-mappen
2. Åpne appen og klikk **Initialize** for å opprette en ny server
3. Følg appens instruksjoner for å legge til dens kommandolinjeverktøy i PATH
4. Verifiser installasjonen:

```bash
psql --version
```

Postgres.app oppretter også en superbruker med navnet til din macOS-konto.

---

## Webserverkonfigurasjon {: #web-server-configuration }

digna krever en webserver for å hoste dashboardet. Velg ett av følgende alternativer:

- [nginx](#nginx-setup) — installert via Homebrew, anbefales
- [Apache httpd](#apache-setup) — inkludert i macOS

Du trenger bare å installere og konfigurere **én** av disse serverne.

Begge seksjonene konfigurerer to ting som dashboardet er avhengig av:

- **Fallback for single-page application**, slik at oppdatering av en dashboard-URL ikke gir 404
- **En `.md` MIME-type**, slik at Markdown-filer serveres riktig

### nginx-oppsett {: #nginx-setup }

#### Oversikt

nginx er en lettvekts, høyytelses webserver godt egnet til å servere det statiske digna-dashboardet.

#### Installering

```bash
brew install nginx
```

#### Starte nginx

```bash
brew services start nginx
```

#### Verifiser installasjonen

1. Åpne nettleseren din
2. Naviger til `http://localhost:8080`
3. Du skal se nginx-velkomstsiden

!!! note "Merk — standardport er 8080, ikke 80"

    Homebrew konfigurerer nginx til å lytte på port `8080` slik at den kan kjøre uten administratorrettigheter. På macOS krever binding til port `80` eller andre porter under 1024 root-tilgang.

    For å serve dashboardet på port 80, endre `listen 8080;` til `listen 80;` i konfigurasjonen nedenfor og start nginx med `sudo brew services start nginx` i stedet.

#### Konfigurere et nettsted for dashboardet

Homebrews nginx-konfigurasjon inkluderer alle filer i katalogen `servers`. Opprett en dedikert konfigurasjonsfil for digna der:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Lim inn følgende og erstatt `/path/to/digna/dashboard` med den faktiske banen til din utpakkede `dashboard`-mappe:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Viktig"

    Uten `try_files`-direktivet vil oppdatering av en hvilken som helst dashboard-side annet enn rot-URLen returnere en 404. Dette er nginx-ekvivalenten til URL Rewrite-modulen som kreves av IIS på Windows.

#### Bruk konfigurasjonen

Test konfigurasjonen for syntaksfeil, og last deretter nginx på nytt:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd-oppsett {: #apache-setup }

#### Oversikt

macOS inkluderer Apache httpd, så ingen installasjon er nødvendig. Tjenesten er deaktivert som standard.

#### Starte Apache

```bash
sudo apachectl start
```

#### Verifiser installasjonen

1. Åpne nettleseren din
2. Naviger til `http://localhost`
3. Du skal se meldingen "It works!"

#### Påkrevd: Aktivere mod_rewrite

Dashboardet krever URL-omskriving. Åpne Apache-konfigurasjonen:

```bash
sudo nano /etc/apache2/httpd.conf
```

Finn følgende linje og fjern ledende `#` for å avkommentere den:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Påkrevd: Tillat .htaccess-overstyringer

I samme fil, lokaliser blokken `<Directory "/Library/WebServer/Documents">` og endre:

```apache
AllowOverride None
```

til:

```apache
AllowOverride All
```

#### Påkrevd: MIME-type for Markdown-filer

Fremdeles i `httpd.conf`, legg til følgende linje slik at Markdown-filer serveres riktig:

```apache
AddType text/markdown .md
```

!!! warning "Viktig"

    Uten denne innstillingen kan `.md`-filer kanskje ikke serveres korrekt.

#### Bruk konfigurasjonen

Sjekk konfigurasjonen for syntaksfeil, og start deretter Apache på nytt:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Første installasjon {: #initial-installation }

### Trinn 1: Sett opp digna-repositoriet

digna-repositoriet lagrer alle metrikker som beregnes av digna. Det fungerer som den sentrale databasen for analytiske og ytelsesrelaterte data.

#### Opprett repositories-skjema og bruker

Åpne din PostgreSQL-klient (psql, pgAdmin eller lignende) og utfør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstatt følgende plassholdere:**

- `<digna_repo_schema>` — Ønsket skjema-navn (f.eks. `dignarepo`)
- `<digna_repo_user>` — Ønsket brukernavn (f.eks. `digna_user`)
- `<digna_repo_password>` — Et sikkert passord for denne brukeren

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

For å kjøre disse fra Terminal i ett steg:

```bash
psql postgres
```

Lim deretter inn utsagnene ved `postgres=#` prompten og skriv `\q` for å avslutte.

!!! tip "Beste praksis"

    Bruk sterke, komplekse passord for databasebrukere. Unngå lett gjettbare legitimasjoner.

---

### Trinn 2: Pakk ut digna-installasjonspakken

1. Finn digna-installasjons ZIP-filen du har fått
2. Pakk den ut til ønsket installasjonssted — for eksempel `/opt/digna` eller `~/digna`
3. Etter utpakking bør du se følgende elementer:
   - `dashboard/` — Web dashboard-grensesnitt
   - `digna` — Hovedkjørbar fil (backend + CLI kombinert)

!!! info "Konfigurasjons- og lisensfilene er ikke med i pakken"

    Verken `config.toml` eller `dashboard/dashboard_config.toml` følger med installasjonen — du
    oppretter begge selv, i [Backend-konfigurasjon](#backend-configuration) og
    [Dashboard-konfigurasjon](#dashboard-configuration). `license.toml` følger heller ikke med;
    digna leverer den separat, slik Trinn 3 beskriver.

For å pakke ut fra Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Gjør den kjørbare filen kjørbar

Avhengig av hvordan arkivet ble overført, kan den kjørbare biten mangle etter utpakking. Sett den eksplisitt:

```bash
cd /opt/digna
chmod +x digna
```

#### Hvis macOS blokkerer applikasjonen

Filer lastet ned via en nettleser eller mailklient tagges med et karanteneattributt. Hvis macOS rapporterer at appen *"cannot be opened because the developer cannot be verified"*, fjern attributtet fra installasjonskatalogen:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativt, åpne **System Settings → Privacy & Security**, finn det blokkerte elementet nær bunnen av siden, og klikk **Open Anyway**.

!!! note "Merk"

    Dette steget er kun nødvendig hvis macOS faktisk blokkerer den kjørbare filen. Pakker overført via SSH eller fra interne filandeler er vanligvis ikke i karantene.

### Trinn 3: Installer lisensfilen

!!! warning "Viktig"

    Lisensfilen er **ikke** inkludert i installasjonspakken og vil bli levert separat av digna.

1. Finn `license.toml`-filen som er levert til deg
2. Kopier den inn i rotmappen for digna-installasjonen (der `config.toml` og den kjørbare `digna`-filen ligger)

**Hvorfor dette er viktig:**
Lisensfilen inneholder kundeinformasjon, lisensens utløpsdato og digital signatur. **Endre ikke denne filen** — eventuelle endringer vil ugyldiggjøre den.

**Katalogstruktur etter oppsett:**

```
/opt/digna/
├── config.toml         (konfigurasjonsfil)
├── license.toml        (DIN LISENSFIL - kopier hit)
├── digna               (hovedkjørbar fil)
├── bin/                (skripter for tjenestehåndtering)
└── dashboard/          (webgrensesnitt)
    └── (dashboard-filer)
```

---

## Backend-konfigurasjon {: #backend-configuration }

### Trinn 1: Opprett og rediger konfigurasjonsfilen

Filen `config_template.toml` leveres i digna-installasjonskatalogen. Du trenger bare å gi den nytt navn til `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Plassering:** `/opt/digna/config.toml`

Åpne `config.toml` i en teksteditor og konfigurer hver seksjon nedenfor.

#### [app] Seksjonen

Denne seksjonen konfigurerer cross-origin resource sharing (CORS) mellom dashboardet og backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Verdi | Notater |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL-er | URL-ene som dashboardet serveres fra. Nettleserforespørsler fra alle andre origins avvises |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrevd, slik at nettleseren sender sesjonscookien med hver forespørsel |

!!! note "Merk"

    Hvis du serverer dashboardet fra Homebrews nginx på standardporten, er origin som må tillates `http://localhost:8080`.

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

| Parameter | Verdi | Notater |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens vertnavn/IP |
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

| Parameter | Verdi | Notater |
|---|---|---|
| `DIGNA_FERNET_KEY` | Verdien vist ovenfor | Nøkkel for krypteringen som tidligere utgivelser brukte. Den må være til stede; behold verdien som vises |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Verten dashboardet nås under. `""` angir ikke noe domene, noe som er riktig bak en proxy som serverer dashboardet og backend under samme origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Må være `true` når digna serveres over HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Holder sesjonscookien utenfor rekkevidde for skript |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Sesjonsutløp i sekunder |
| `DIGNA_MAX_WORKERS` | Antall CPU-kjerner - 1 | Antall inspeksjoner som kan kjøre samtidig |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Påkrevd. Brukes for lenkene i varslingsmeldinger, så det må være en URL mottakerne kan åpne |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valgfri. Antall sekunder én enkelt spørring mot en kildedatabase kan kjøre før den avbrytes; `0` slår av tidsavbruddet |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valgfri. Antall sekunder det ventes på en tilkobling til en kildedatabase; `0` venter uten tidsbegrensning |

!!! tip "Tips"

    For å finne antall CPU-kjerner tilgjengelig på din Mac, kjør `sysctl -n hw.ncpu`.

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

| Parameter | Verdi | Notater |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` for produksjon, `DEBUG` for feilsøking. `TRACE`, `WARN` og `ERROR` godtas også |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valgfri. Katalog for de roterende loggfilene, relativt til arbeidskatalogen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valgfri. Antall roterte loggfiler som beholdes |

#### [duckdb] Seksjonen (valgfri) {: #duckdb-section }

Nytt i Release 2026.11. Denne seksjonen angir ressursene til **digna Engine**, som profilerer
data inne i digna for databasetilkoblinger med profileringsstedet **digna Engine**, og som kjører
kontroller av referanseintegritet mellom datakilder på ulike databasetilkoblinger. Se
[Profileringssted](../../../platform/profiling/profiling_location.md).

Seksjonen er valgfri. Uten den gjelder standardverdiene nedenfor.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Verdi | Notater |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Minne, i MB, som én kjøring av digna Engine kan bruke. Opptil `DIGNA_MAX_WORKERS` kjøringer kan være aktive samtidig |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: systemets midlertidige katalog (`$TMPDIR` for kontoen som kjører digna) | Katalog for midlertidige filer når dataene ikke får plass i minnet |

!!! tip "Dimensjonering av digna Engine"

    Planlegg for opptil `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` minne på
    digna-verten, i tillegg til det digna selv bruker, og for nok ledig diskplass i den midlertidige
    katalogen til å romme den største inspiserte datoen for datakildene som bruker digna Engine.
    Pek `DIGNA_DUCKDB_TEMP_DIRECTORY` mot en disk med så mye plass, skrivbar for kontoen som
    kjører digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Du trenger bare denne seksjonen hvis minst én databasetilkobling bruker digna Engine, eller hvis en
    kontroll av referanseintegritet sammenligner datakilder på ulike tilkoblinger.

---

### Trinn 2: Valider konfigurasjonen

Kontroller at `config.toml` er fullstendig og korrekt bygget opp før du initialiserer repositoryet. Kjør i digna-installasjonskatalogen:

```bash
./digna config check
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

1. Åpne **Terminal**
2. Naviger til din digna-installasjonsmappe (der `config.toml` og den kjørbare `digna`-filen ligger)
3. Kjør tilkoblingstesten:

```bash
cd /opt/digna
./digna repo check
```

På et nytt skjema kobler kommandoen til og rapporterer deretter at det ikke er installert noe repository ennå:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

På dette tidspunktet er det det forventede resultatet: det bekrefter at digna når PostgreSQL og skjemaet. En tilkoblings- eller autentiseringsfeil peker i stedet på `[repo]`-seksjonen eller på PostgreSQL-oppsettet.

!!! note "Merk"

    På macOS er ikke kommandoer i gjeldende katalog på PATH, så den kjørbare filen påkalles som `./digna` i stedet for `digna`. For å bruke den kortere formen overalt, legg installasjonskatalogen til i PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Trinn 4: Installer repositories-skjemaet

I samme katalog, kjør:

```bash
./digna repo upgrade
```

Denne kommandoen installerer de nødvendige tabellene i repository-skjemaet og avslutter med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerer og oppgraderer"

    Fra Release 2026.11 installerer `repo upgrade` et nytt repository og oppgraderer et eksisterende.
    `repo install` fungerer fortsatt som et annet navn på den samme kommandoen.

### Trinn 5: Opprett en admin-bruker

Administratorbrukeren opprettes direkte mot repository-skjemaet, så serveren trenger ikke å kjøre ennå. Kjør i digna-installasjonskatalogen:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Eksempel:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Dette oppretter en bruker med e-postadressen `admin@example.com` og fulle administratorrettigheter.

!!! tip "Tips"

    Pakk passordet inn i enkeltanførselstegn. `zsh` behandler tegn som `!`, `$` og `*` spesielt, og et uavsluttet passord som inneholder dem vil ikke bli sendt videre som skrevet.

!!! tip "Beste praksis"

    Bruk et sterkt passord med en blanding av store og små bokstaver, tall og spesialtegn.

### Trinn 6: Start digna-serveren

I digna-installasjonskatalogen, start serveren med:

```bash
./digna serve --address <host> --port <port>
```

**Parametere:**
- `--address` — Serverens vertsnavn/IP (standard `127.0.0.1`)
- `--port` — Serverport (standard `8000`)

Når serveren er oppe, skriver den ut adressen den lytter på:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tips"

    Første gangen du starter serveren kan macOS spørre om du vil tillate at applikasjonen aksepterer innkommende nettverkstilkoblinger. Klikk **Allow**, ellers vil ikke dashboardet kunne nå backend.

!!! note "Serveren opptar terminalen"

    `serve` kjører i forgrunnen og fortsetter til du stopper den med ++ctrl+c++. La den kjøre mens du fullfører oppsettet; for å starte den automatisk ved oppstart, se [Kjøre digna som bakgrunnstjeneste](#running-digna-as-a-background-service).

---

## Dashboard-konfigurasjon {: #dashboard-configuration }

### Trinn 1: Distribuer dashboardet til webserveren

digna-dashboardet leser sin egen konfigurasjon fra `dashboard/dashboard_config.toml`. Den filen følger ikke med installasjonen — du oppretter den i `dashboard/`-katalogen sammen med dashboardfilene.

Innholdet er beskrevet under [Enkel pålogging](../../../sso/overview.md), som også er der filen trengs: den inneholder påloggingsalternativene dashboardet tilbyr og, for distribusjoner med flere instanser, backend-tilkoblingen.

Velg din webserver og følg de tilsvarende distribusjonstrinnene.

#### Distribuere til nginx

Hvis du fulgte [nginx-oppsettet](#nginx-setup) er serverblokken allerede pekt mot din `dashboard`-mappe og ingen kopiering er nødvendig.

1. **Bekreft banen**
   - Åpne `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Bekreft at `root` peker til din utpakkede `dashboard`-mappe

2. **Sørg for at mappen er lesbar**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Last inn nginx på nytt**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Test installasjonen**
   - Åpne nettleseren din
   - Naviger til `http://localhost:8080` (eller din konfigurerte URL)
   - Du skal se innloggingssiden for digna-dashboardet

#### Distribuere til Apache httpd

1. **Kopier dashboardet til dokumentroten**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Legg til omskrivingsreglene**

   Opprett en `.htaccess`-fil inne i den deployerte mappen slik at dashboard-ruter overlever en nettleseroppdatering:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Lim inn følgende:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Start Apache på nytt**
   ```bash
   sudo apachectl restart
   ```

4. **Åpne dashboardet**
   - Åpne nettleseren din
   - Naviger til `http://localhost/digna`
   - Du skal se innloggingssiden for digna-dashboardet

---

## Kjøre digna som en bakgrunnstjeneste {: #running-digna-as-a-background-service }

### Hvorfor kjøre digna som en tjeneste?

Å kjøre digna-backenden som en bakgrunnstjeneste sikrer at den:

- Startes automatisk når maskinen booter
- Kjører i bakgrunnen uten et åpent Terminal-vindu
- Startes på nytt automatisk hvis den krasjer
- Kan administreres via `launchctl`, macOS sin tjenestehåndterer

### Filer for tjenesteadministrasjon

Alle nødvendige filer ligger i digna-installasjonskatalogen under: `bin/`

Følgende shell-skript er tilgjengelige:

- `install_service.sh` — registrerer digna med launchd
- `uninstall_service.sh` — avregistrerer tjenesten
- `start_service.sh` — starter den registrerte tjenesten
- `stop_service.sh` — stopper den kjørende tjenesten

!!! warning "Administrator kreves"

    Alle skriptene må kjøres med `sudo`, fordi registrering av en tjeneste som starter ved boot skriver til `/Library/LaunchDaemons`.

### Gjør skriptene kjørbare

Utpakking kan fjernet kjørbar-bit. Før første bruk:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installere tjenesten

1. **Åpne Terminal**

2. **Gå til bin-mappen**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kjør installasjonsskriptet**
   ```bash
   sudo ./install_service.sh
   ```

digna-serveren er nå registrert hos launchd med **automatisk oppstart** aktivert. Tjenesten starter ikke umiddelbart — se neste seksjon for å starte den.

### Starte og stoppe tjenesten

#### For å starte tjenesten

1. Åpne Terminal
2. Naviger til `/opt/digna/bin`
3. Kjør:
   ```bash
   sudo ./start_service.sh
   ```

#### For å stoppe tjenesten

1. Åpne Terminal
2. Naviger til `/opt/digna/bin`
3. Kjør:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tips"

    Stopp alltid tjenesten før du oppdaterer applikasjonsfiler.

### Verifisere tjenesten

For å bekrefte at tjenesten er registrert og kjører:

```bash
sudo launchctl list | grep digna
```

En linje som begynner med en prosess-ID indikerer at tjenesten kjører. En `-` i den første kolonnen betyr at den er registrert, men stoppet.

### Flytte tjenesten til en ny katalog

launchd lagrer den absolutte banen til den kjørbare filen, så relokering krever re-registrering av tjenesten:

1. **Avinstaller gjeldende tjeneste**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Flytt applikasjonsfilene**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Installer tjenesten på nytt**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Start tjenesten**
   ```bash
   sudo ./start_service.sh
   ```

### Avinstallere tjenesten

1. **Stopp den kjørende tjenesten**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Avinstaller tjenesten**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna-serveren er nå avregistrert fra launchd.

---

## Oppgradere til en ny release {: #upgrading-to-a-new-release }

Denne delen oppgraderer en installasjon av Release 2026.06 til Release 2026.11. Hvis
installasjonen din er eldre, les først [Oppgradere fra en utgivelse før 2026.06](#upgrading-from-a-release-before-2026-06).

### Før du oppgraderer

**Det er obligatorisk å ta backup av digna-repositoriet**

Før du oppgraderer digna, ta backup av repositoriet (PostgreSQL) for å beskytte mot datatap.
En backup sikrer at du kan gjenopprette hvis oppgraderingen møter uventede problemer.

For å lage en backup fra Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

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

Hvis digna kjører som en bakgrunnstjeneste, stopp den først:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Hvis digna kjører i forgrunnen, trykk ++ctrl+c++ i Terminal-vinduet der den kjører.

#### Trinn 2: Sikkerhetskopier gjeldende installasjon {: #step-2-backup-current-installation }

Gi den kjørbare filen og dashboard-mappen i den gjeldende installasjonen nye navn i
digna-installasjonskatalogen, slik at den nye utgivelsen kan distribueres ved siden av dem:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Behold `digna_old` til du har verifisert oppgraderingen, og `dashboard_old` til du har gjenopprettet
konfigurasjonsfilene dine fra den (se trinn 4). Deretter kan du slette begge.

!!! info "Oppgradering fra en utgivelse før 2026.06"

    Gi mappene `dignabackend` og `dignacli` nye navn i stedet for den kjørbare filen:
    `mv dignabackend dignabackend_old` og `mv dignacli dignacli_old`. Ingen av dem brukes av Release 2026.11.

#### Trinn 3: Pakk ut og distribuer ny versjon {: #step-3-extract-and-deploy-new-version }

1. Pakk ut den nye digna-installasjons-ZIP-filen
2. Kopier den nye kjørbare `digna`-filen og `dashboard`-mappen til installasjonskatalogen din
3. Gjenopprett kjørbar-biten og fjern om nødvendig karanteneattributtet:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Viktig"

    Verken `config.toml` eller `dashboard/dashboard_config.toml` er noensinne inkludert i
    installasjons-ZIP-en — digna-teamet leverer aldri noen av filene. Din eksisterende konfigurasjon
    berøres derfor ikke av oppgraderingen, og kopiene i de omdøpte `*_old`-mappene er de
    eneste du har.

#### Trinn 4: Gjenopprett konfigurasjonsfilene {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
og last deretter inn siden på nytt med en hard oppdatering (++cmd+shift+r++).

#### Trinn 6: Valider konfigurasjonen {: #step-6-validate-the-configuration }

Bekreft at `config.toml` er fullstendig før du rører repositoriet:

```bash
./digna config check
```

Hver seksjon må rapportere OK. Rett alt som rapporteres som FAILED, fjern nøklene som vises under
**Unknown keys**, og kjør kommandoen på nytt før du går videre.

#### Trinn 7: Erstatt lisensfilen {: #step-7-replace-the-license-file }

En lisensfil følger normalt med fra én utgivelse til den neste. Release 2026.11 er et
unntak: den legger til to lisensierte moduler, digna Data Reconciliation og digna Agentic, og en
lisens utstedt før 2026.11 inneholder dem ikke. Kopier `license.toml` som digna-teamet har levert
for Release 2026.11, til installasjonskatalogen, slik at den erstatter den gamle:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ikke behold den forrige lisensen"

    Med den forrige lisensen starter digna fortsatt, men digna Data Reconciliation og digna
    MCP Server forblir slått av. Alle kommandoer som kontrollerer lisensen — `user`,
    `inspection`, `repo` — avbrytes før de berører repositoriet når kontrollen feiler. Verifiser
    den nye lisensen før du går videre:

    ```bash
    ./digna license check
    ```

#### Trinn 8: Oppgrader repository-skjemaet {: #step-8-upgrade-the-repository-schema }

Kjør i digna-installasjonskatalogen:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 håndterer repository-skjemaet med versjonerte migreringer. Den første oppgraderingen fra
en tidligere utgivelse bringer skjemaet til siste versjon av den tidligere ordningen, registrerer dette som
utgangspunkt og bruker deretter migreringene i Release 2026.11. Den avslutter med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle eksisterende data bevares. For å se tilstanden til repositoriet når som helst, kjør
`./digna repo check`: den viser den sist anvendte migreringen og eventuelle ventende migreringer.

!!! warning "digna starter ikke på et utdatert repository"

    Fra Release 2026.11 nekter serveren å starte så lenge repositoriet må oppgraderes, og
    sier ifra om det, for eksempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kjør `repo upgrade` før du starter serveren eller tjenesten.

#### Trinn 9: Start tjenestene på nytt {: #step-9-restart-services }

Hvis du kjører som en bakgrunnstjeneste:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Hvis du kjører manuelt, start serveren på nytt:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Hvis du bruker nginx eller Apache, start den aktuelle webserveren på nytt:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Trinn 10: Verifiser oppgraderingen {: #step-10-verify-the-upgrade }

1. Bekreft utgivelsen til den nye kjørbare filen:

    ```bash
    ./digna version
    ```

    Den første linjen må være `Release: 2026.11`.

2. Åpne digna-dashboardet og bekreft at grensesnittet lastes inn riktig.
3. Sjekk serverutdataene og filene i `logs`-katalogen for feil.
4. Test databasetilkoblingene dine — se
   [Teste en tilkobling](../../../databases/overview.md#testing-a-connection). Etter en oppgradering
   fra en utgivelse før 2026.06 legger du først om hver tilkobling som ikke allerede brukte ODBC, til
   ODBC.

For å komme i gang med de nye modulene, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Koble til en AI-agent](../../../platform/agentic/connect_ai_agent.md) for digna MCP Server, og
[Profileringssted](../../../platform/profiling/profiling_location.md) for digna Engine.