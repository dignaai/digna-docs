---
title: macOS installasjonsveiledning – digna Release 2026.06 | digna dokumentasjon
description: Trinnvis veiledning for å installere digna Release 2026.06 på macOS — systemkrav, Homebrew- og PostgreSQL-oppsett, nginx eller Apache-konfigurasjon, backend- og dashboard-konfigurasjon, kjøre digna som en bakgrunnstjeneste og oppgradere til en ny utgivelse.
keywords: digna macos installasjon, digna mac distribusjonsveiledning, digna backend oppsett, digna dashboard installasjon, postgresql homebrew, nginx macos, digna launchd tjeneste, digna oppgraderingsveiledning
image: /assets/logo_square.png
---

# macOS installasjonsveiledning for digna Release 2026.06

**Release:** 2026.06

**Sist oppdatert:** 5. september 2026


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

- **dignabackend**: Kjernen i applikasjonen, ansvarlig for å prosessere data og utføre kvalitetskontroller.
- **dignadashboard**: Et nettbasert grensesnitt hostet på en webserver, som gir en brukervennlig måte å samhandle med digna-plattformen og visualisere datakvalitetsmetrikker.

### Hva er nytt i Release 2026.06

Denne releasen bringer dataobservability-funksjonalitet direkte inn i koden din, slik at utviklere kan overvåke datakvalitet ved kilden. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) for fullstendige detaljer.

### Ser du etter Windows eller Linux?

Denne veiledningen dekker macOS. For andre plattformer, se [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) eller [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Konfigurasjonsfil
   - `license.toml` — Lisensfil (kopier din fil her)

For å pakke ut fra Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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

| Parameter | Verdi | Notater |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adresse | Vertnavn eller IP hvor dignabackend hostes |
| `digna_APP_PORT` | `8082` (standard) | Port for REST API-endepunkter |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Hvis dashboardet ligger på en annen server, inkluder dens URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Påkrevd for CORS med legimitasjon |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillat alle HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillat alle headers |

!!! note "Merk"

    Hvis du serverer dashboardet fra Homebrews nginx på standardporten, er origin som må tillates `http://localhost:8080`.

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

| Parameter | Verdi | Notater |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens vertnavn/IP |
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

| Parameter | Verdi | Notater |
|---|---|---|
| `digna_FERNET_KEY` | Krypteringsnøkkel | Brukes til å kryptere tokens og cookies (standard gitt) |
| `digna_COOKIE_DOMAIN` | `localhost` | Matche ditt frontend-domene |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produksjon) | Bruk `true` for HTTPS-tilkoblinger |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktivert for sikkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Forebygger CSRF-angrep |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Sesjonsutløp i sekunder |
| `digna_MAX_WORKERS` | Antall CPU-kjerner - 1 | Antall parallelle inspeksjonsoppgaver |

!!! tip "Tips"

    For å finne antall CPU-kjerner tilgjengelig på din Mac, kjør `sysctl -n hw.ncpu`.

#### [logging] Seksjonen

Denne seksjonen konfigurerer loggeadferd:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Verdi | Notater |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` for produksjon, `DEBUG` for feilsøking |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antall daglige logg-backuper som beholdes |

---

### Trinn 2: Initialiser repositoriet

1. Åpne **Terminal**
2. Naviger til din digna-installasjonsmappe (der `config.toml` og den kjørbare `digna`-filen ligger)
3. Kjør tilkoblingstesten:

```bash
cd /opt/digna
./digna repo check
```

Du bør se en bekreftelse på at tilkoblingen er etablert (selve repositoriet er ennå ikke initialisert).

!!! note "Merk"

    På macOS er ikke kommandoer i gjeldende katalog på PATH, så den kjørbare filen påkalles som `./digna` i stedet for `digna`. For å bruke den kortere formen overalt, legg installasjonskatalogen til i PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Trinn 3: Installer repositories-skjemaet

I samme katalog, kjør:

```bash
./digna repo install
```

Denne kommandoen installerer nødvendige tabeller og skjema i din PostgreSQL-database.

### Trinn 4: Start digna-serveren

I digna-installasjonskatalogen, start serveren med:

```bash
./digna serve --address <host> --port <port>
```

**Parametere:**
- `--address` — Serverens vertsnavn/IP
- `--port` — Serverport

Du skal se oppstarts-meldinger som bekrefter at serveren kjører:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tips"

    Første gangen du starter serveren kan macOS spørre om du vil tillate at applikasjonen aksepterer innkommende nettverkstilkoblinger. Klikk **Allow**, ellers vil ikke dashboardet kunne nå backend.

### Trinn 5: Opprett en admin-bruker

1. Åpne et **nytt** Terminal-vindu
2. Naviger til digna-installasjonsmappen
3. Kjør følgende kommando for å opprette en admin-bruker:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Eksempel:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Dette oppretter en bruker med brukernavn `admin` og full administrative rettigheter.

!!! tip "Tips"

    Pakk passordet inn i enkeltanførselstegn. `zsh` behandler tegn som `!`, `$` og `*` spesielt, og et uavsluttet passord som inneholder dem vil ikke bli sendt videre som skrevet.

!!! tip "Beste praksis"

    Bruk et sterkt passord med en blanding av store og små bokstaver, tall og spesialtegn.

---

## Dashboard-konfigurasjon {: #dashboard-configuration }

### Trinn 1: Distribuer dashboardet til webserveren

digna-dashboardet har sin egen `config.toml`-fil plassert i `dashboard/`-katalogen. Denne konfigurasjonen er allerede levert og krever normalt ikke endringer under første oppsett. Du trenger kun å konfigurere den hvis du må tilpasse backend-tilkoblingen.

Hvis du må endre dashboard-konfigurasjonen (f.eks. for multi-instans distribusjoner), se dokumentasjonen for dashboardet.

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

### Før du oppgraderer

**Å lage en backup av digna-repositoriet er obligatorisk**

Før du oppgraderer digna, ta backup av ditt repositorium (PostgreSQL) for å beskytte mot datatap.
En backup sikrer at du kan gjenopprette hvis oppgraderingen støter på uventede problemer.

For å lage en backup fra Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Oppgraderingsprosessen

#### Trinn 1: Stopp digna-tjenesten

Hvis digna kjører som en bakgrunnstjeneste, stopp den først:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Hvis digna kjører i forgrunnen, trykk `Ctrl + C` i Terminal-vinduet hvor den kjører.

#### Trinn 2: Backup av nåværende backend-installasjon

I din digna-installasjonskatalog:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Trinn 3: Pakk ut og distribuer ny versjon

1. Pakk ut den nye digna-installasjons ZIP-filen
2. Kopier den nye `digna`-kjørbare filen og `dashboard`-mappen til installasjonskatalogen din
3. Gjenopprett kjørbar-bit og, hvis nødvendig, fjern karanteneattributtet:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Viktig"

    Filen `config.toml` er **aldri** inkludert i installasjons-ZIPen. Din eksisterende konfigurasjon forblir trygg.

### Trinn 4: Gjenopprett konfigurasjonsfilene dine

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Trinn 5: Oppgrader repository-skjemaet

Naviger til din digna-installasjonskatalog og kjør:

```bash
cd /opt/digna
./digna repo upgrade
```

Dette oppdaterer PostgreSQL-skjemaet til siste versjon samtidig som alle eksisterende data beholdes.

### Trinn 6: Start tjenestene på nytt

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

Hvis du bruker nginx eller Apache, start den respektive webserveren på nytt:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Trinn 7: Verifiser oppgraderingen

1. Åpne digna-dashboardet
2. Bekreft at grensesnittet laster riktig
3. Sjekk serverloggene for eventuelle feil