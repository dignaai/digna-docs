# Linux-installasjonsveiledning for digna Release 2026.11

**Release:** 2026.11

**Sist oppdatert:** 7. november 2026


---

## Innholdsfortegnelse

1. [Introduksjon](#introduction)
2. [Systemkrav](#system-requirements)
3. [Forberedelser før installasjon](#pre-installation-setup)
4. [Oppsett av PostgreSQL-server](#postgresql-server-setup)
5. [Webserverkonfigurasjon](#web-server-configuration)
6. [Første installasjon](#initial-installation)
7. [Backend-konfigurasjon](#backend-configuration)
8. [Dashboard-konfigurasjon](#dashboard-configuration)
9. [Kjøre digna som en systemd-tjeneste](#running-digna-as-a-systemd-service)
10. [Oppgradere til en ny utgivelse](#upgrading-to-a-new-release)

---

## Introduksjon {: #introduction }

### Om digna

digna er en omfattende, AI-drevet plattform designet for å optimalisere datakvalitetsstyring på tvers av ulike data-miljøer som warehouses, lakes og lakehouses. Bygget for å være svært skalerbar og tilpasningsdyktig, håndterer digna moderne datautfordringer gjennom automatisering, sanntidsovervåking og anomalideteksjon.

digna består av to hovedkomponenter:

- **digna**: kjernen i applikasjonen, ansvarlig for å behandle data og utføre kvalitetskontroller. Den samler backend og kommandolinjegrensesnittet i én kjørbar fil og erstatter dermed de separate programmene `dignabackend` og `dignacli` fra tidligere utgivelser.
- **dignadashboard**: Et nettbasert grensesnitt hostet på en webserver, som gir en brukervennlig måte å samhandle med digna-plattformen og visualisere datakvalitetsmål.

### Hva er nytt i Release 2026.11

Denne utgivelsen legger til digna Data Reconciliation, digna Agentic med digna MCP Server, og digna Engine, som kan profilere data inne i digna og kontrollere referanseintegritet mellom ulike databaseteknologier. Se [utgivelsesnotatene](../../../changelog/Release_202611.md) for fullstendige detaljer.

For en installasjon bringer utgivelsen en ny mekanisme for repository-migreringer, en valgfri `[duckdb]`-seksjon i `config.toml` for digna Engine, og en ny lisensfil. [Oppgraderingsavsnittet](#upgrading-to-a-new-release) tar for seg hver av dem.

### Ser du etter Windows eller macOS?

Denne veiledningen dekker Linux. For andre plattformer, se [Windows installasjonsveiledning](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) eller [macOS installasjonsveiledning](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Hvilken distribusjon dekker denne veiledningen?

Instruksjonene er skrevet for de to mest vanlige serverfamiliene. Der de to avviker, er begge kommandoene oppgitt:

- **Debian-familien** — Debian, Ubuntu. Pakkehåndterer: `apt`.
- **RHEL-familien** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Pakkehåndterer: `dnf`.

Enhver moderne distribusjon med `systemd` vil fungere; det er bare pakkenavn og noen konfigurasjonsstier som endres.

---

## Systemkrav {: #system-requirements }

Før du begynner installasjonen, sørg for at systemet ditt oppfyller følgende minimumskrav:

| Krav | Spesifikasjon |
|---|---|
| **Operativsystem** | Ubuntu 22.04 LTS eller nyere, Debian 12 eller nyere, RHEL 9 / Rocky 9 / AlmaLinux 9 eller nyere |
| **Arkitektur** | x86_64 (amd64) eller arm64 |
| **Init-system** | systemd |
| **Minne (minimalt oppsett)** | 16 GB RAM |
| **Diskplass** | 10 GB tilgjengelig lagring |
| **Database** | PostgreSQL Server 12 eller nyere |
| **Webserver** | nginx, Apache httpd, eller tilsvarende |

!!! info "digna Engine"

    Databasetilkoblinger som bruker digna Engine som profileringssted, profileres på selve
    digna-verten. Planlegg ekstra minne og diskplass for dem, se
    [\[duckdb\]-seksjonen](#duckdb-section).

### Databaseinstallasjonsalternativer

**Hvis PostgreSQL allerede er installert:**
Du kan legge til en ny database for digna i din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskin som digna:**

!!! info "Anbefalte spesifikasjoner"

    - **Minne**: 32 GB RAM (istedenfor 16 GB)
    - **Diskplass**: 50 GB tilgjengelig lagring (istedenfor 10 GB)

    Disse høyere spesifikasjonene tar hensyn til at både digna og PostgreSQL-databasen kjører samtidig.

### Sjekke distribusjon og arkitektur

Flere kommandoer i denne veiledningen skiller seg mellom Debian- og RHEL-familiene. For å sjekke hvilken du bruker, kjør:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` eller `ID=debian` — bruk `apt`-kommandoene.
- `ID=rhel`, `rocky`, `almalinux` eller `fedora` — bruk `dnf`-kommandoene.
- `x86_64` eller `aarch64` — arkitekturen for installasjonspakken du trenger.

---

## Forberedelser før installasjon {: #pre-installation-setup }

Før du installerer digna, sørg for at to viktige forutsetninger er på plass:

1. **PostgreSQL-server** – for å lagre beregnede metrikker og ytelsesdata
2. **Webserver** – for hosting av digna Dashboard

Hvis disse komponentene ikke allerede er satt opp, følg seksjonene nedenfor for å installere og konfigurere dem.

### Oppdatering av pakkelisten

Oppdater pakkelistene før du installerer noe:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Merk"

    Gjennom denne veiledningen er den første kommandoen i et par for **Debian-familien** og den andre for **RHEL-familien**. Kjør kun den som matcher systemet ditt.

---

## Oppsett av PostgreSQL-server {: #postgresql-server-setup }

### Hvis du allerede har PostgreSQL

Hvis PostgreSQL allerede er installert og kjører lokalt eller hvis du bruker en administrert ekstern PostgreSQL-server, kan du hoppe til [neste seksjon](#web-server-configuration).

### Installere PostgreSQL

#### Steg 1: Installer serverpakken

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tips"

    Distribusjonspakkene kan ligge etter i forhold til nyeste PostgreSQL-utgivelse. Hvis du trenger en spesifikk nyere versjon, bruk den offisielle [PostgreSQL apt- eller yum-repositoryen](https://www.postgresql.org/download/linux/) i stedet.

#### Steg 2: Initialiser databaseklyngen

På **Debian-familien** oppretter og starter pakken en klynge automatisk — hopp til neste steg.

På **RHEL-familien** må klyngen opprettes eksplisitt:

```bash
sudo postgresql-setup --initdb
```

#### Steg 3: Start og aktiver tjenesten

```bash
sudo systemctl enable --now postgresql
```

Dette starter PostgreSQL umiddelbart og konfigurerer den til å starte automatisk ved oppstart.

#### Steg 4: Verifiser installasjonen

```bash
psql --version
sudo systemctl status postgresql
```

Du bør se PostgreSQL-versjonen og en `active (running)`-tjeneste.

#### Steg 5: Koble til serveren

En Linux PostgreSQL-pakke oppretter en systemkonto `postgres` som eier klyngen. Koble til via denne kontoen:

```bash
sudo -u postgres psql
```

!!! note "Merk — Linux skiller seg fra Windows her"

    Windows-installasjonen spør etter et passord for `postgres`-superbrukeren under installasjonen. Linux-pakker gjør ikke det. I stedet autentiseres lokale tilkoblinger med **peer authentication**: operativsystembrukeren `postgres` får koble til som databasebrukeren `postgres` uten passord.

    Dette er grunnen til at kommandoen over bruker `sudo -u postgres`. digna-backend kobler over TCP med brukernavn og passord, så du vil opprette en eksplisitt digna-bruker i [Første installasjon](#initial-installation).

#### Steg 6: Bekreft porten

Standard PostgreSQL-port er `5432`. For å bekrefte hvilken port serveren lytter på:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Noter verdien — du vil trenge den når du konfigurerer digna-backend.

#### Steg 7: Aktiver passordautentisering for digna-brukeren

digna kobler til PostgreSQL over TCP som `digna_user`, noe som krever passordautentisering fremfor peer authentication. Sjekk at `pg_hba.conf` tillater dette.

Finn filen:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Åpne den i en editor og bekreft at de lokale TCP-linjene bruker `scram-sha-256` (eller `md5` på eldre servere) i stedet for `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Reload PostgreSQL etter enhver endring:

```bash
sudo systemctl reload postgresql
```

!!! warning "Viktig"

    Hvis digna rapporterer `FATAL: Ident authentication failed for user "digna_user"`, er denne innstillingen årsaken.

#### Steg 8: Hvis PostgreSQL kjører på en annen maskin

For å akseptere tilkoblinger fra en annen vert, sett `listen_addresses` i `postgresql.conf` og legg til en tilsvarende `host`-linje for nettverket ditt i `pg_hba.conf`:

```
listen_addresses = '*'
```

Deretter åpner du porten i brannmuren og starter tjenesten på nytt:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Webserverkonfigurasjon {: #web-server-configuration }

digna krever en webserver for å hoste dashboardet. Velg ett av følgende alternativer:

- [nginx](#nginx-setup) — lettvekts og anbefalt
- [Apache httpd](#apache-setup) — et mye brukt alternativ

Du trenger bare å installere og konfigurere **én** av disse serverne.

Begge seksjonene konfigurerer to ting dashboardet er avhengig av:

- **En single-page-application fallback**, slik at oppfrisking av en dashboard-URL ikke returnerer 404
- **En `.md` MIME-type**, slik at Markdown-filer serveres riktig

### nginx-oppsett {: #nginx-setup }

#### Oversikt

nginx er en lettvekts, høyytelses webserver som egner seg godt til å servere det statiske digna-dashboardet.

#### Installasjon

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Starte nginx

```bash
sudo systemctl enable --now nginx
```

#### Verifiser installasjonen

1. Åpne nettleseren
2. Gå til `http://localhost`
3. Du bør se nginx-velkomstsiden

#### Åpne brannmuren

Hvis serveren nås fra andre maskiner, tillat HTTP-trafikk:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Konfigurere et nettsted for dashboardet

nginx inkluderer alle filer i `conf.d`-katalogen på begge distribusjonsfamilier. Lag en dedikert konfigurasjonsfil for digna der:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Lim inn følgende, og erstatt `/opt/digna/dashboard` med den faktiske stien til din utpakkede `dashboard`-mappe:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

(Kommentarene over er i konfigurasjonen; de kan hjelpe ved feilsøking.)

!!! warning "Viktig"

    Uten `try_files`-direktivet vil oppfrisking av en dashboard-side annet enn rot-URLen gi 404. Dette er nginx-ekvivalenten til URL Rewrite-modulen som kreves av IIS på Windows.

#### Deaktiver standardnettstedet

Kun én serverblokk kan være `default_server` for en port. På **Debian-familien**, fjern den medfølgende standarden slik at den ikke konflikter:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

På **RHEL-familien**, kommenter ut eller slett `server { ... }`-blokken inne i `/etc/nginx/nginx.conf`.

#### Aktiver konfigurasjonen

Test konfigurasjonen for syntaksfeil, og last deretter nginx på nytt:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd-oppsett {: #apache-setup }

#### Oversikt

Apache httpd er tilgjengelig i standardreposene for alle støttede distribusjoner. Pakken heter `apache2` på Debian-familien og `httpd` på RHEL-familien.

#### Installasjon

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Starte Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verifiser installasjonen

1. Åpne nettleseren
2. Gå til `http://localhost`
3. Du bør se distribusjonens standard Apache-side

#### Påkrevd: Aktiver mod_rewrite

Dashboardet krever URL-omskriving.

På **Debian-familien**, aktiver modulen og start på nytt:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

På **RHEL-familien** lastes `mod_rewrite` som regel inn som standard. Bekreft det:

```bash
httpd -M | grep rewrite
```

#### Påkrevd: Tillat .htaccess-overstyringer

Åpne konfigurasjonsfilen for dokumentroten:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Finn `<Directory>`-blokken som dekker dokumentroten din (`/var/www/html` på begge familier) og endre:

```apache
AllowOverride None
```

til:

```apache
AllowOverride All
```

#### Påkrevd: MIME-type for Markdown-filer

I samme fil, legg til følgende linje slik at Markdown-filer serveres riktig:

```apache
AddType text/markdown .md
```

!!! warning "Viktig"

    Uten denne innstillingen kan `.md`-filer ikke bli servert riktig.

#### Aktiver konfigurasjonen

Sjekk konfigurasjonen for syntaksfeil, og start deretter Apache på nytt:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Første installasjon {: #initial-installation }

### Steg 1: Sett opp digna-repositoriet

digna-repositoriet lagrer alle metrikker som beregnes av digna. Det fungerer som den sentrale databasen for analytiske og ytelsesdata.

#### Opprett repositories-skjema og bruker

Åpne din PostgreSQL-klient (psql, pgAdmin eller lignende) og kjør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstatt følgende plassholdere:**

- `<digna_repo_schema>` — ønsket skjema-navn (f.eks. `dignarepo`)
- `<digna_repo_user>` — ønsket brukernavn (f.eks. `digna_user`)
- `<digna_repo_password>` — et sikkert passord for denne brukeren

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

For å kjøre disse fra shell i ett trinn:

```bash
sudo -u postgres psql
```

Lim så inn uttalelsene ved `postgres=#`-prompten og skriv `\q` for å avslutte.

!!! tip "Beste praksis"

    Bruk sterke, komplekse passord for databasebrukere. Unngå lett gjettbare legitimasjoner.

---

### Steg 2: Pakk ut digna-installasjonspakken

1. Finn digna-installasjons ZIP-filen som er levert til deg
2. Pakk den ut til ønsket installasjonssted — for eksempel `/opt/digna`
3. Etter utpakking skal du se følgende elementer:
   - `dashboard/` — web-dashboard grensesnitt
   - `digna` — hovedkjørbar (backend + CLI kombinert)

!!! info "Konfigurasjons- og lisensfilene er ikke med i pakken"

    Verken `config.toml` eller `dashboard/dashboard_config.toml` følger med installasjonen — du
    oppretter begge selv, i [Backend-konfigurasjon](#backend-configuration) og
    [Dashboard-konfigurasjon](#dashboard-configuration). `license.toml` følger heller ikke med;
    digna leverer den separat, slik Steg 3 beskriver.

For å pakke ut fra shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Merk"

    Hvis `unzip` ikke er installert, legg det til med `sudo apt install -y unzip` eller `sudo dnf install -y unzip`.

#### Gjør den kjørbare filen kjørbar

Avhengig av hvordan arkivet ble overført, kan den kjørbare biten mangle etter utpakking. Sett den eksplisitt:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Opprett en tjenestekonto

Det anbefales å kjøre backend som en dedikert, uprivilegert bruker for produksjonsdistribusjoner:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Merk"

    På RHEL-familien er tilsvarende shellsti `/sbin/nologin`.

### Steg 3: Installer lisensfilen

!!! warning "Viktig"

    Lisensfilen er **ikke** inkludert i installasjonspakken og vil bli levert separat av digna.

1. Finn `license.toml`-filen som er levert til deg
2. Kopier den inn i rotmappen for digna-installasjonen (der `config.toml` og den kjørbare `digna` ligger)

**Hvorfor dette er viktig:**
Lisensfilen inneholder kundeinformasjon, lisensutløpsdato og digital signatur. **Ikke endre denne filen** — enhver endring vil ugyldiggjøre den.

**Katalogstruktur etter oppsett:**

```
/opt/digna/
├── config.toml         (konfigurasjonsfil)
├── license.toml        (DIN LISENSFIL - kopier hit)
├── digna               (hovedkjørbar)
├── bin/                (skript for tjenesteadministrasjon)
└── dashboard/          (webgrensesnitt)
    └── (dashboard-filer)
```

---

## Backend-konfigurasjon {: #backend-configuration }

### Steg 1: Opprett og rediger konfigurasjonsfilen

`config_template.toml`-filen leveres i din digna-installasjonsmappe. Du trenger bare å gi den nytt navn til `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Plassering:** `/opt/digna/config.toml`

Åpne `config.toml` i en teksteditor og konfigurer hver seksjon nedenfor.

#### [app]-seksjonen

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

    Hvis du serverer dashboardet fra nginx eller Apache på standard HTTP-port, er origin å tillate `http://localhost` — eller serverens offentlige URL når dashboardet nås fra andre maskiner.

!!! info "[app]-seksjonen er valgfri"

    Fra Release 2026.11 kan begge nøklene, og hele `[app]`-seksjonen, utelates. Dette er riktig
    oppsett når en omvendt proxy serverer dashboardet og backend under samme origin: nettleseren
    gjør da ingen cross-origin-forespørsler, og ingen er tillatt som standard.

#### [repo]-seksjonen

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
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostnavn/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasenavn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Skjema opprettet tidligere |
| `DIGNA_REPO_USER` | `digna_user` | Bruker opprettet i PostgreSQL-oppsettet |
| `DIGNA_REPO_PASSWORD` | Ditt passord | Passord satt ved skjemaopprettelsen |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valgfri. SSL-modus for PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valgfri. Antall tilkoblinger digna holder åpne mot repositoriet |

!!! tip "Beste praksis"

    `config.toml` inneholder et databasepassord i klartekst. Begrens filens tillatelser slik at kun tjenestekontoen kan lese den:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base]-seksjonen

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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `DIGNA_MAX_WORKERS` | Antall CPU-kjerner - 1 | Antall inspeksjoner som kan kjøre samtidig |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Påkrevd. Brukes for lenkene i varslingsmeldinger, så det må være en URL mottakerne kan åpne |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valgfri. Antall sekunder én enkelt spørring mot en kildedatabase kan kjøre før den avbrytes; `0` slår av tidsavbruddet |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valgfri. Antall sekunder det ventes på en tilkobling til en kildedatabase; `0` venter uten tidsbegrensning |

!!! tip "Tips"

    For å finne antall CPU-kjerner tilgjengelig på serveren, kjør `nproc`.

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

#### [logging]-seksjonen

Denne seksjonen konfigurerer loggingsatferd:

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

#### [duckdb]-seksjonen (valgfri) {: #duckdb-section }

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: systemets midlertidige katalog (`$TMPDIR`, eller `/tmp` når den ikke er satt) | Katalog for midlertidige filer når dataene ikke får plass i minnet |

!!! tip "Dimensjonering av digna Engine"

    Planlegg for opptil `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` minne på
    digna-verten, i tillegg til det digna selv bruker, og for nok ledig diskplass i den midlertidige
    katalogen til å romme den største inspiserte datoen for datakildene som bruker digna Engine.
    Pek `DIGNA_DUCKDB_TEMP_DIRECTORY` mot en disk med så mye plass, skrivbar for kontoen som
    kjører digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    Du trenger bare denne seksjonen hvis minst én databasetilkobling bruker digna Engine, eller hvis en
    kontroll av referanseintegritet sammenligner datakilder på ulike tilkoblinger.

---

### Steg 2: Valider konfigurasjonen

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

### Steg 3: Initialiser repositoriet

1. Åpne et terminalvindu
2. Gå til din digna-installasjonsmappe (der `config.toml` og `digna`-kjørbar ligger)
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

    På Linux er ikke gjeldende katalog på din PATH, så den kjørbare filen kjøres som `./digna` i stedet for `digna`. For å bruke kortformen overalt, legg til en symbolsk lenke:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Steg 4: Installer repositories-skjemaet

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

### Steg 5: Opprett en administratorbruker

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

    Pakk passordet i enkle anførselstegn. `bash` og `zsh` behandler tegn som `!`, `$` og `*` spesielt, og et ikke-innrammet passord som inneholder dem vil ikke bli sendt videre som skrevet.

!!! tip "Beste praksis"

    Bruk et sterkt passord med en blanding av store og små bokstaver, tall og spesialtegn.

### Steg 6: Start digna-serveren

I digna-installasjonskatalogen, start serveren med:

```bash
./digna serve --address <host> --port <port>
```

**Parametere:**
- `--address` — Serverens hostnavn/IP (standard `127.0.0.1`)
- `--port` — Serverport (standard `8000`)

Når serveren er oppe, skriver den ut adressen den lytter på:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tips"

    Hvis dashboardet serveres fra en annen maskin enn backend, åpne API-porten i brannmuren også:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Serveren opptar terminalen"

    `serve` kjører i forgrunnen og fortsetter til du stopper den med ++ctrl+c++. La den kjøre mens du fullfører oppsettet; for å starte den automatisk ved oppstart, se [Kjøre digna som systemd-tjeneste](#running-digna-as-a-systemd-service).

---

## Dashboard-konfigurasjon {: #dashboard-configuration }

### Steg 1: Deploy dashboardet til webserveren

digna-dashboardet leser sin egen konfigurasjon fra `dashboard/dashboard_config.toml`. Den filen følger ikke med installasjonen — du oppretter den i `dashboard/`-katalogen sammen med dashboardfilene.

Innholdet er beskrevet under [Enkel pålogging](../../../sso/overview.md), som også er der filen trengs: den inneholder påloggingsalternativene dashboardet tilbyr og, for distribusjoner med flere instanser, backend-tilkoblingen.

Velg webserver og følg tilsvarende distribusjonstrinn.

#### Deploy til nginx

Hvis du fulgte [nginx-oppsettet](#nginx-setup), peker serverblokken allerede på din `dashboard`-mappe og ingen kopiering er nødvendig.

1. **Bekreft stien**
   - Åpne `/etc/nginx/conf.d/digna.conf`
   - Verifiser at `root` peker til din utpakkede `dashboard`-mappe

2. **Sørg for at mappen er lesbar**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Reload nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Test installasjonen**
   - Åpne nettleseren
   - Gå til `http://localhost` (eller din konfigurerte URL)
   - Du skal se digna-dashboardets innloggingsside

#### Deploy til Apache httpd

1. **Kopier dashboardet til dokumentroten**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Legg til omskrivingsreglene**

   Opprett en `.htaccess`-fil inne i den deployerte mappen slik at dashboard-ruter overlever en oppfriskning i nettleseren:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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

3. **Restart Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Åpne dashboardet**
   - Åpne nettleseren
   - Gå til `http://localhost/digna`
   - Du skal se digna-dashboardets innloggingsside

### Steg 2: SELinux (kun RHEL-familien)

På RHEL, Rocky, AlmaLinux og Fedora er SELinux som regel enforcing og vil blokkere webserveren fra å lese filer utenfor forventede steder. Sjekk om det er aktivt:

```bash
getenforce
```

Hvis resultatet er `Enforcing` og du serverer dashboardet fra `/opt/digna/dashboard`, merk katalogen slik at webserveren kan lese den:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Merk"

    Hvis `semanage` ikke finnes, installer det med `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Viktig"

    Et dashboard som returnerer **403 Forbidden** på en nylig konfigurert RHEL-server er nesten alltid et SELinux-label-problem snarere enn et filtillatelsesproblem. Bekreft med `sudo ausearch -m avc -ts recent`.

---

## Kjøre digna som en systemd-tjeneste {: #running-digna-as-a-systemd-service }

### Hvorfor kjøre digna som en tjeneste?

Å kjøre digna-backend som en systemd-tjeneste sikrer at den:

- Starter automatisk når maskinen boot-er
- Kjører i bakgrunnen uten et åpent terminalvindu
- Starter på nytt automatisk hvis den krasjer
- Kan administreres via `systemctl`, standard Linux-tjenestebehandler

### Filer for tjenesteadministrasjon

Alle nødvendige filer ligger i digna-installasjonskatalogen under: `bin/`

Følgende shell-skript er tilgjengelige:

- `install_service.sh` — registrerer digna hos systemd
- `uninstall_service.sh` — fjerner registreringen
- `start_service.sh` — starter den registrerte tjenesten
- `stop_service.sh` — stopper den kjørende tjenesten

!!! warning "Rottilgang påkrevd"

    Alle skriptene må kjøres med `sudo`, fordi registrering av en tjeneste som starter ved boot skriver en enhetsfil til `/etc/systemd/system`.

### Gjøre skriptene kjørbare

Utpakking bevarer kanskje ikke kjørbar-bit. Før første bruk:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Installere tjenesten

1. **Åpne et terminalvindu**

2. **Gå til bin-mappen**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kjør installasjonsskriptet**
   ```bash
   sudo ./install_service.sh
   ```

digna-serveren er nå registrert hos systemd med **automatisk oppstart** aktivert. Tjenesten starter ikke umiddelbart — se neste seksjon for å starte den.

### Starte og stoppe tjenesten

#### For å starte tjenesten

1. Åpne et terminalvindu
2. Gå til `/opt/digna/bin`
3. Kjør:
   ```bash
   sudo ./start_service.sh
   ```

#### For å stoppe tjenesten

1. Åpne et terminalvindu
2. Gå til `/opt/digna/bin`
3. Kjør:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tips"

    Stopp alltid tjenesten før du oppdaterer applikasjonsfiler.

### Administrere tjenesten med systemctl

Når den er registrert, kan tjenesten også kontrolleres med standard systemd-kommandoer fra hvilken som helst katalog:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verifisere tjenesten

For å bekrefte at tjenesten er registrert og kjører:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` betyr at tjenesten starter ved boot; `active` betyr at den kjører nå.

### Vise tjenestelogger

systemd fanger opp alt backend skriver til konsollen. For å lese det:

```bash
sudo journalctl -u digna -n 100
```

For å følge loggen i sanntid mens du reproduserer et problem:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tips"

    Dette er den raskeste måten å feilsøke en tjeneste som starter og umiddelbart stopper. En repository-tilkoblingsfeil eller en manglende `license.toml` rapporteres her.

### Flytte tjenesten til en ny katalog

Enhetsfilen lagrer den absolutte stien til den kjørbare filen, så flytting av installasjonen krever ny registrering av tjenesten:

1. **Avinstaller den nåværende tjenesten**
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

digna-serveren er nå avregistrert fra systemd.

---

## Oppgradere til en ny utgivelse {: #upgrading-to-a-new-release }

Denne delen oppgraderer en installasjon av Release 2026.06 til Release 2026.11.

!!! warning "Oppgradering fra en utgivelse før 2026.06"

    Utfør først oppgraderingstrinnene for Release 2026.06: [Oppgradere til en ny utgivelse](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). Fortsett deretter med trinnene nedenfor.

### Før du oppgraderer

**Det er obligatorisk å ta backup av digna-repositoriet**

Før du oppgraderer digna, ta backup av repositoriet (PostgreSQL) for å beskytte mot datatap.
En backup sikrer at du kan gjenopprette hvis oppgraderingen møter uventede problemer.

For å lage en backup fra shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Be om lisensfilen for Release 2026.11**

Release 2026.11 krever en ny `license.toml`. Be digna-teamet om den før du starter, og
ha den klar til [steg 7](#step-7-replace-the-license-file).

### Oppgraderingsprosess

#### Steg 1: Stopp digna-tjenesten {: #step-1-stop-the-digna-service }

Hvis digna kjører som en systemd-tjeneste, stopp den først:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Hvis digna kjører i forgrunnen, trykk ++ctrl+c++ i terminalvinduet der den kjører.

#### Steg 2: Sikkerhetskopier gjeldende installasjon {: #step-2-backup-current-installation }

Gi den kjørbare filen og dashboard-mappen i den gjeldende installasjonen nye navn i
digna-installasjonskatalogen, slik at den nye utgivelsen kan distribueres ved siden av dem:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Behold `digna_old` til du har verifisert oppgraderingen, og `dashboard_old` til du har gjenopprettet
konfigurasjonsfilene dine fra den (se steg 4). Deretter kan du slette begge.

#### Steg 3: Pakk ut og distribuer ny versjon {: #step-3-extract-and-deploy-new-version }

1. Pakk ut den nye digna-installasjons-ZIP-filen
2. Kopier den nye kjørbare `digna`-filen og `dashboard`-mappen til installasjonskatalogen din
3. Gjenopprett kjørbar-biten og eierskapet til tjenestekontoen:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Viktig"

    Verken `config.toml` eller `dashboard/dashboard_config.toml` er noensinne inkludert i
    installasjons-ZIP-en — digna-teamet leverer aldri noen av filene. Din eksisterende konfigurasjon
    berøres derfor ikke av oppgraderingen, og kopiene i de omdøpte `*_old`-mappene er de
    eneste du har.

#### Steg 4: Gjenopprett konfigurasjonsfilene {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 krever ingen endring i `config.toml`: en fil som fungerer med Release 2026.06, fortsetter
å fungere. To endringer er valgfrie:

- Legg til en [`[duckdb]`-seksjon](#duckdb-section) hvis databasetilkoblinger skal bruke digna Engine
  og standardverdiene ikke passer for verten din.
- Utelat `[app]`-seksjonen hvis en omvendt proxy serverer dashboardet og backend under samme
  origin.

!!! warning "Innstillinger som digna ikke leser"

    Tidligere versjoner av denne veiledningen viste noen innstillinger som digna ikke leser. De har ingen
    effekt, og `config check` viser dem under **Unknown keys** i steg 6. Fjern eller rett
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

#### Steg 5: Last inn webserveren på nytt {: #step-5-reload-the-web-server }

Dashboardet er et sett med statiske filer, så webserveren din — og nettleseren — kan fortsatt
levere den forrige versjonen. Last inn på nytt eller start på nytt den webserveren som er vert for `dashboard`-mappen,
og last deretter inn siden på nytt med en hard oppdatering (++ctrl+f5++).

#### Steg 6: Valider konfigurasjonen {: #step-6-validate-the-configuration }

Bekreft at `config.toml` er fullstendig før du rører repositoriet:

```bash
./digna config check
```

Hver seksjon må rapportere OK. Rett alt som rapporteres som FAILED, fjern nøklene som vises under
**Unknown keys**, og kjør kommandoen på nytt før du går videre.

#### Steg 7: Erstatt lisensfilen {: #step-7-replace-the-license-file }

En lisensfil følger normalt med fra én utgivelse til den neste. Release 2026.11 er et
unntak: den legger til to lisensierte moduler, digna Data Reconciliation og digna Agentic, og en
lisens utstedt før 2026.11 inneholder dem ikke. Kopier `license.toml` som digna-teamet har levert
for Release 2026.11, til installasjonskatalogen, slik at den erstatter den gamle:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ikke behold den forrige lisensen"

    Med den forrige lisensen starter digna fortsatt, men digna Data Reconciliation og digna
    MCP Server forblir slått av. Alle kommandoer som kontrollerer lisensen — `user`,
    `inspection`, `repo` — avbrytes før de berører repositoriet når kontrollen feiler. Verifiser
    den nye lisensen før du går videre:

    ```bash
    ./digna license check
    ```

#### Steg 8: Oppgrader repository-skjemaet {: #step-8-upgrade-the-repository-schema }

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

#### Steg 9: Start tjenestene på nytt {: #step-9-restart-services }

Hvis du kjører som en systemd-tjeneste:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Hvis du kjører manuelt, start serveren på nytt:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Hvis du bruker nginx eller Apache, last inn den aktuelle webserveren på nytt:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

På RHEL-familien bruker du SELinux-merkingen på nytt hvis `dashboard`-katalogen ble erstattet:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Steg 10: Verifiser oppgraderingen {: #step-10-verify-the-upgrade }

1. Bekreft utgivelsen til den nye kjørbare filen:

    ```bash
    ./digna version
    ```

    Den første linjen må være `Release: 2026.11`.

2. Åpne digna-dashboardet og bekreft at grensesnittet lastes inn riktig.
3. Sjekk serverloggene for feil:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Test databasetilkoblingene dine — se
   [Teste en tilkobling](../../../databases/overview.md#testing-a-connection). Etter en oppgradering
   fra en utgivelse før 2026.06 legger du først om hver tilkobling som ikke allerede brukte ODBC, til
   ODBC.

For å komme i gang med de nye modulene, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Koble til en AI-agent](../../../platform/agentic/connect_ai_agent.md) for digna MCP Server, og
[Profileringssted](../../../platform/profiling/profiling_location.md) for digna Engine.