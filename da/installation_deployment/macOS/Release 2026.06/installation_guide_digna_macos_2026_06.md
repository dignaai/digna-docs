# macOS Installation Guide for digna Release 2026.06

**Release:** 2026.06

**Last Updated:** September 5, 2026


---

## Table of Contents

1. [Introduktion](#introduction)
2. [Systemkrav](#system-requirements)
3. [Forudgående opsætning](#pre-installation-setup)
4. [PostgreSQL-serveropsætning](#postgresql-server-setup)
5. [Webserverkonfiguration](#web-server-configuration)
6. [Initial installation](#initial-installation)
7. [Backend-konfiguration](#backend-configuration)
8. [Dashboard-konfiguration](#dashboard-configuration)
9. [Køre digna som baggrundstjeneste](#running-digna-as-a-background-service)
10. [Opgradering til en ny release](#upgrading-to-a-new-release)

---

## Introduktion {: #introduction }

### Om digna

digna er en omfattende AI-drevet platform designet til at optimere data-kvalitetsstyring på tværs af forskellige data-miljøer som warehouses, lakes og lakehouses. Bygget til at være højt skalerbar og tilpasningsdygtig, adresserer digna moderne dataudfordringer gennem automatisering, realtidsovervågning og anomalidetektion.

digna består af to hovedkomponenter:

- **dignabackend**: Applikationens kerneengine, ansvarlig for at behandle data og udføre kvalitetskontroller.
- **dignadashboard**: Et webbaseret interface hostet på en webserver, som giver en brugervenlig måde at interagere med digna-platformen og visualisere datakvalitetsmålinger.

### Hvad er nyt i Release 2026.06

Denne release bringer data-observability-funktionalitet direkte ind i din kode, så udviklere kan overvåge datakvalitet ved kilden. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) for fulde detaljer.

### Leder du efter Windows eller Linux?

Denne vejledning dækker macOS. For andre platforme, se [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) eller [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemkrav {: #system-requirements }

Før du begynder installationen, sørg for at dit system opfylder følgende minimumskrav:

| Requirement | Specification |
|---|---|
| **Operating System** | macOS 13 (Ventura) or later |
| **Architecture** | Apple Silicon (arm64) or Intel (x86_64) |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB available storage |
| **Database** | PostgreSQL Server 12 or higher |
| **Web Server** | nginx, Apache httpd, or equivalent |
| **Command Line Tools** | Xcode Command Line Tools (required by Homebrew) |

### Database-installationsmuligheder

**Hvis PostgreSQL allerede er installeret:**
Du kan tilføje en ny database til digna på din eksisterende PostgreSQL-server.

**Hvis du installerer PostgreSQL på samme maskine som digna:**

!!! info "Anbefalede specifikationer"

    - **Hukommelse**: 32 GB RAM (i stedet for 16 GB)
    - **Diskplads**: 50 GB ledig lagerplads (i stedet for 10 GB)

    Disse højere specifikationer rummer både digna og PostgreSQL-databasen kørende samtidigt.

### Tjek din arkitektur

Flere stier i denne vejledning adskiller sig mellem Apple Silicon og Intel Macs. For at tjekke hvilken du har, åbn **Terminal** og kør:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installeres til `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installeres til `/usr/local`.

!!! tip "Tip"

    I stedet for at hardkode en af stierne, bruger denne vejledning `$(brew --prefix)`, som udvider til den korrekte placering på begge arkitekturer. Du kan kopiere kommandoerne ordret.

---

## Forudgående opsætning {: #pre-installation-setup }

Før du installerer digna, skal du sikre, at tre nøgleforudsætninger er på plads:

1. **Homebrew** – pakkestyringsværktøjet brugt til at installere komponenterne nedenfor
2. **PostgreSQL Server** – til lagring af beregnede metrikker og performance-data
3. **Web Server** – til hosting af digna Dashboard

Hvis disse komponenter ikke allerede er opsat, følg afsnittene nedenfor for at installere og konfigurere dem.

### Installation af Homebrew

Homebrew er standard pakkestyringsværktøj for macOS og bruges i hele denne vejledning til at installere PostgreSQL og nginx.

#### Trin 1: Tjek om Homebrew allerede er installeret

Åbn **Terminal** (tryk `Cmd + Space`, skriv `Terminal`, tryk Enter) og kør:

```bash
brew --version
```

Hvis der returneres et versionsnummer, spring videre til afsnittet [PostgreSQL-serveropsætning](#postgresql-server-setup).

#### Trin 2: Installer Homebrew

Hvis kommandoen ikke blev fundet, installer Homebrew ved at følge instruktionerne på [den officielle Homebrew-side](https://brew.sh). Installationsprogrammet installerer også Xcode Command Line Tools, hvis de ikke allerede er til stede.

#### Trin 3: Tilføj Homebrew til din PATH

På Apple Silicon printer installatøren to kommandoer til at tilføje Homebrew til dit shell-miljø. Kør dem som instrueret, og bekræft derefter:

```bash
brew --prefix
```

Dette bør udskrive `/opt/homebrew` på Apple Silicon eller `/usr/local` på Intel.

---

## PostgreSQL-serveropsætning {: #postgresql-server-setup }

### Hvis du allerede har PostgreSQL

Hvis PostgreSQL allerede er installeret og kører på din lokale maskine, eller hvis du bruger en administreret fjern-PostgreSQL-server, kan du springe til [næste afsnit](#web-server-configuration).

### Installationsmuligheder

macOS tilbyder to ligetil måder at installere PostgreSQL på. Vælg **én**:

- [Homebrew](#postgresql-homebrew) — kommandolinjeinstallation, anbefalet til serverudrulninger
- [Postgres.app](#postgresql-app) — grafisk installation, praktisk til lokal evaluering

### Installation af PostgreSQL med Homebrew {: #postgresql-homebrew }

#### Trin 1: Installer PostgreSQL-formulaen

```bash
brew install postgresql@16
```

#### Trin 2: Tilføj PostgreSQL til din PATH

Versionerede PostgreSQL-formulaer er *keg-only*, hvilket betyder, at Homebrew ikke linker deres kommandoer ind i din PATH automatisk. Tilføj dem selv:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Bemærk"

    Dette antager standard `zsh`-shellen brugt af macOS. Hvis du bruger `bash`, tilføj den samme linje til `~/.bash_profile` i stedet.

#### Trin 3: Start PostgreSQL-tjenesten

```bash
brew services start postgresql@16
```

Dette starter PostgreSQL med det samme og konfigurerer den til at starte automatisk, når du logger ind.

#### Trin 4: Verificer installationen

```bash
psql --version
```

Du bør se PostgreSQL-versionen, hvis installationen lykkedes.

#### Trin 5: Forbind til serveren

```bash
psql postgres
```

!!! warning "Vigtigt — macOS adskiller sig fra Windows her"

    Windows-installationsprogrammet beder dig om at oprette en `postgres` superuser og et password. Homebrew gør ikke det. I stedet opretter den en superuser med navnet på din **macOS-konto**, uden password, tilgængelig kun fra den lokale maskine.

    Det betyder, at der ikke er en `postgres`-rolle på en frisk Homebrew-installation. Brug dit eget kontonavn, når du har brug for en superuser, og opret en eksplicit digna-bruger som beskrevet i [Initial installation](#initial-installation).

#### Trin 6: Bekræft porten

Standard PostgreSQL-port er `5432`. For at bekræfte hvilken port din server lytter på:

```bash
psql postgres -c "SHOW port;"
```

Notér værdien — du skal bruge den når du konfigurerer digna-backenden.

### Installation af PostgreSQL med Postgres.app {: #postgresql-app }

Hvis du foretrækker en grafisk installation:

1. Download [Postgres.app](https://postgresapp.com) og træk den ind i din **Applications**-mappe
2. Åbn appen og klik **Initialize** for at oprette en ny server
3. Følg appens instruktioner for at tilføje dens kommandolinjeværktøjer til din PATH
4. Verificer installationen:

```bash
psql --version
```

Postgres.app opretter også en superuser med navnet på din macOS-konto.

---

## Webserverkonfiguration {: #web-server-configuration }

digna kræver en webserver til at hoste dashboardet. Vælg én af følgende muligheder:

- [nginx](#nginx-setup) — installeret via Homebrew, anbefalet
- [Apache httpd](#apache-setup) — inkluderet i macOS

Du behøver kun at installere og konfigurere **én** af disse servere.

Begge sektioner konfigurerer to ting, som dashboardet afhænger af:

- **En single-page-application fallback**, så en opdatering af en dashboard-URL ikke returnerer en 404
- **En `.md` MIME-type**, så Markdown-filer serveres korrekt

### nginx-opsætning {: #nginx-setup }

#### Oversigt

nginx er en letvægts, højtydende webserver velegnet til at serve det statiske digna-dashboard.

#### Installation

```bash
brew install nginx
```

#### Start nginx

```bash
brew services start nginx
```

#### Bekræft installationen

1. Åbn din browser
2. Navigér til `http://localhost:8080`
3. Du bør se nginx-velkomstsiden

!!! note "Bemærk — standardport er 8080, ikke 80"

    Homebrew konfigurerer nginx til at lytte på port `8080`, så den kan køre uden administratorrettigheder. På macOS kræver binding til port `80` eller andre porte under 1024 root-adgang.

    For at serve dashboardet på port 80, ændr `listen 8080;` til `listen 80;` i konfigurationen nedenfor og start nginx med `sudo brew services start nginx` i stedet.

#### Konfiguration af et site til dashboardet

Homebrew's nginx-konfiguration inkluderer alle filer i dens `servers`-mappe. Opret en dedikeret konfigurationsfil til digna der:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Indsæt følgende, og erstat `/path/to/digna/dashboard` med den faktiske sti til din udpakkede `dashboard`-mappe:

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

!!! warning "Vigtigt"

    Uden `try_files`-direktivet returnerer genindlæsning af enhver dashboard-side andet end rod-URL'en en 404. Dette er nginx-ekvivalenten til URL Rewrite-modulet, der kræves af IIS på Windows.

#### Anvend konfigurationen

Test konfigurationen for syntaksfejl, og genindlæs derefter nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd-opsætning {: #apache-setup }

#### Oversigt

macOS inkluderer Apache httpd, så ingen installation er påkrævet. Den er deaktiveret som standard.

#### Start Apache

```bash
sudo apachectl start
```

#### Bekræft installationen

1. Åbn din browser
2. Navigér til `http://localhost`
3. Du bør se beskeden "It works!"

#### Påkrævet: Aktivér mod_rewrite

Dashboardet kræver URL-omskrivning. Åbn Apache-konfigurationen:

```bash
sudo nano /etc/apache2/httpd.conf
```

Find følgende linje og fjern den indledende `#` for at gøre den aktiv:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Påkrævet: Tillad .htaccess-overrides

I samme fil, lokaliser `<Directory "/Library/WebServer/Documents">`-blokken og ændr:

```apache
AllowOverride None
```

til:

```apache
AllowOverride All
```

#### Påkrævet: MIME-type for Markdown-filer

Stadig i `httpd.conf`, tilføj følgende linje, så Markdown-filer serveres korrekt:

```apache
AddType text/markdown .md
```

!!! warning "Vigtigt"

    Uden denne indstilling kan `.md`-filer muligvis ikke serveres korrekt.

#### Anvend konfigurationen

Tjek konfigurationen for syntaksfejl, og genstart derefter Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Initial installation {: #initial-installation }

### Trin 1: Opret digna-repositoriet

Digna-repositoriet lagrer alle metrikker beregnet af digna. Det fungerer som den centrale database for analytiske og performance-data.

#### Opret repositorieschema og bruger

Åbn din PostgreSQL-klient (psql, pgAdmin eller lignende) og udfør følgende SQL-kommandoer:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Erstat følgende pladsholdere:**

- `<digna_repo_schema>` — Dit ønskede schema-navn (fx `dignarepo`)
- `<digna_repo_user>` — Dit ønskede brugernavn (fx `digna_user`)
- `<digna_repo_password>` — Et sikkert password til denne bruger

**Eksempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

For at køre disse fra Terminal i ét trin:

```bash
psql postgres
```

Indsæt derefter statements ved prompten `postgres=#` og skriv `\q` for at afslutte.

!!! tip "Bedste praksis"

    Brug stærke, komplekse passwords til databasebrugere. Undgå let gættelige legitimationsoplysninger.

---

### Trin 2: Pak digna-installationspakken ud

1. Find digna-installations-ZIP-filen leveret til dig
2. Pak den ud til din ønskede installationsplacering — for eksempel `/opt/digna` eller `~/digna`
3. Efter udpakning bør du se følgende elementer:
   - `dashboard/` — Web dashboard interface
   - `digna` — Hoved-eksekverbar (backend + CLI kombineret)
   - `config.toml` — Konfigurationsfil
   - `license.toml` — Licensfil (kopiér din hertil)

For at udpakke fra Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Gør den eksekverbare fil kørbar

Afhængig af hvordan arkivet blev overført, overlever den eksekverbare bit måske ikke ved udpakning. Sæt den eksplicit:

```bash
cd /opt/digna
chmod +x digna
```

#### Hvis macOS blokerer applikationen

Filer downloadet gennem en browser eller mailklient er mærket med et quarantine-attribut. Hvis macOS rapporterer, at appen *"cannot be opened because the developer cannot be verified"*, fjern attributten fra installationsmappen:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativt, åbn **System Settings → Privacy & Security**, find det blokerede element nær bunden af siden, og klik **Open Anyway**.

!!! note "Bemærk"

    Dette trin er kun nødvendigt, hvis macOS rent faktisk blokerer den eksekverbare fil. Pakker overført via SSH eller fra interne filshares er normalt ikke quarantined.

### Trin 3: Installér licensfilen

!!! warning "Vigtigt"

    Licensfilen er **ikke** inkluderet i installationspakken og vil blive leveret separat af digna.

1. Find den `license.toml`-fil der er leveret til dig
2. Kopiér den ind i root af digna-installationsmappen (hvor `config.toml` og den eksekverbare `digna` ligger)

**Hvorfor det er vigtigt:**
Licensfilen indeholder dine kundeoplysninger, licensens udløbsdato og et digitalt signatur. **Ændr ikke filen** — enhver ændring vil ugyldiggøre den.

**Mappe-struktur efter opsætning:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend-konfiguration {: #backend-configuration }

### Trin 1: Opret og rediger konfigurationsfilen

Filen `config_template.toml` leveres i din digna-installationsmappe. Du skal blot omdøbe den til `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Placering:** `/opt/digna/config.toml`

Åbn `config.toml` i en teksteditor og konfigurer hver sektion nedenfor.

#### [app] Sektionen

Denne sektion konfigurerer digna-backend applikationsindstillinger:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adresse | Hostnavn eller IP hvor dignabackend hostes |
| `digna_APP_PORT` | `8082` (default) | Port for REST API-endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Hvis dashboardet er på en anden server, inkluder dens URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krævet for CORS med legitimationsoplysninger |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillad alle HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillad alle headers |

!!! note "Bemærk"

    Hvis du serverer dashboardet fra Homebrew's nginx på standardporten, er origin der skal tillades `http://localhost:8080`.

#### [repo] Sektionen

Denne sektion konfigurerer forbindelsen til PostgreSQL-databasen:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverens hostname/IP |
| `digna_REPO_PORT` | `5432` (default) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasenavn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema oprettet tidligere |
| `digna_REPO_USER` | `digna_user` | Bruger oprettet i PostgreSQL-opsætningen |
| `digna_REPO_PASSWORD` | Dit password | Password sat under schema-oprettelsen |

#### [base] Sektionen

Denne sektion indeholder sikkerheds- og cookie-indstillinger:

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

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_FERNET_KEY` | Encryptionsnøgle | Bruges til at kryptere tokens og cookies (standard leveret) |
| `digna_COOKIE_DOMAIN` | `localhost` | Match dit frontend-domæne |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Brug `true` for HTTPS-forbindelser |
| `digna_COOKIE_HTTPONLY` | `true` | Altid aktiveret for sikkerhed |
| `digna_COOKIE_SAME_SITE` | `lax` | Forhindrer CSRF-angreb |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timer) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kerner - 1 | Antal parallelle inspectionsopgaver |

!!! tip "Tip"

    For at finde antal CPU-kerner på din Mac, kør `sysctl -n hw.ncpu`.

#### [logging] Sektionen

Denne sektion konfigurerer logningsadfærden:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Værdi | Noter |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` til produktion, `DEBUG` til fejlsøgning |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal daglige log-backups der bevares |

---

### Trin 2: Initialisér repositoriet

1. Åbn **Terminal**
2. Navigér til din digna-installationsmappe (hvor `config.toml` og den eksekverbare `digna` ligger)
3. Kør forbindelsestesten:

```bash
cd /opt/digna
./digna repo check
```

Du bør se en bekræftelse på, at forbindelsen er etableret (selve repositoriet er endnu ikke initialiseret).

!!! note "Bemærk"

    På macOS er kommandoer i den aktuelle mappe ikke på din PATH, så den eksekverbare fil påkaldes som `./digna` i stedet for `digna`. For at kunne bruge den korte form overalt, tilføj installationsmappen til din PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Trin 3: Installer repositorieschemaet

I samme mappe, kør:

```bash
./digna repo install
```

Denne kommando installerer de nødvendige tabeller og schema i din PostgreSQL-database.

### Trin 4: Start digna-serveren

I digna-installationsmappen, start serveren med:

```bash
./digna serve --address <host> --port <port>
```

**Parametre:**
- `--address` — Server hostname/IP
- `--port` — Serverport

Du bør se opstartsbeskeder, der bekræfter at serveren kører:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tip"

    Første gang du starter serveren, kan macOS spørge om du vil tillade, at applikationen modtager indgående netværksforbindelser. Klik **Allow**, ellers kan dashboardet ikke nå backenden.

### Trin 5: Opret en admin-bruger

1. Åbn et **nyt** Terminal-vindue
2. Navigér til din digna-installationsmappe
3. Kør følgende kommando for at oprette en admin-bruger:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Eksempel:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Dette opretter en bruger med brugernavn `admin` og fulde administrative rettigheder.

!!! tip "Tip"

    Indkapsl passwordet i enkeltanførselstegn. `zsh` behandler tegn som `!`, `$` og `*` særligt, og et uindkapslet password med sådanne tegn vil ikke blive videregivet som skrevet.

!!! tip "Bedste praksis"

    Brug et stærkt password med en blanding af store og små bogstaver, tal og specialtegn.

---

## Dashboard-konfiguration {: #dashboard-configuration }

### Trin 1: Deploy dashboardet til webserveren

Digna-dashboardet har sin egen separate `config.toml`-fil placeret i `dashboard/`-mappen. Denne konfiguration leveres allerede og kræver ikke ændringer under initial opsætning. Du skal kun konfigurere den, hvis du vil tilpasse backend-forbindelsen.

Hvis du har behov for at ændre dashboard-konfigurationen (fx ved multi-instance udrulninger), se dashboardets dokumentation.

Vælg din webserver og følg de tilsvarende deployments-steps.

#### Deploy til nginx

Hvis du fulgte afsnittet [nginx Setup](#nginx-setup), peger server-blokken allerede på din `dashboard`-mappe og der er ingen kopiering nødvendig.

1. **Bekræft stien**
   - Åbn `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Bekræft at `root` peger på din udpakkede `dashboard`-mappe

2. **Sørg for at mappen er læsbar**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Genindlæs nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Test installationen**
   - Åbn din browser
   - Navigér til `http://localhost:8080` (eller din konfigurerede URL)
   - Du bør se digna-dashboardets login-side

#### Deploy til Apache httpd

1. **Kopier dashboardet til document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Tilføj rewrite-reglerne**

   Opret en `.htaccess`-fil inde i den deployerede mappe, så dashboard-routes overlever en browser-refresh:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Indsæt følgende:

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

3. **Genstart Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Adgang til dashboardet**
   - Åbn din browser
   - Navigér til `http://localhost/digna`
   - Du bør se digna-dashboardets login-side

---

## Køre digna som baggrundstjeneste {: #running-digna-as-a-background-service }

### Hvorfor køre digna som en tjeneste?

At køre digna-backenden som en baggrundstjeneste sikrer, at den:

- Starter automatisk når maskinen booter
- Kører i baggrunden uden et åbent Terminal-vindue
- Genstarter automatisk, hvis den crasher
- Kan administreres via `launchctl`, macOS's tjenestestyring

### Tjeneste-styringsfiler

Alle nødvendige filer ligger i digna-installationsmappen under: `bin/`

Følgende shell-scripts er tilgængelige:

- `install_service.sh` — registrerer digna hos launchd
- `uninstall_service.sh` — af-registrerer tjenesten
- `start_service.sh` — starter den registrerede tjeneste
- `stop_service.sh` — stopper den kørende tjeneste

!!! warning "Administrator kræves"

    Alle scripts skal eksekveres med `sudo`, fordi registrering af en tjeneste der starter ved boot skriver til `/Library/LaunchDaemons`.

### Gør scripts kørbare

Udpakning bevarer måske ikke den eksekverbare bit. Før første brug:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installér tjenesten

1. **Åbn Terminal**

2. **Navigér til bin-mappen**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kør installationsscriptet**
   ```bash
   sudo ./install_service.sh
   ```

Digna-serveren er nu registreret hos launchd med **automatisk opstart** aktiveret. Tjenesten starter ikke umiddelbart — se næste afsnit for at starte den.

### Start og stop af tjenesten

#### For at starte tjenesten

1. Åbn Terminal
2. Navigér til `/opt/digna/bin`
3. Kør:
   ```bash
   sudo ./start_service.sh
   ```

#### For at stoppe tjenesten

1. Åbn Terminal
2. Navigér til `/opt/digna/bin`
3. Kør:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Stop altid tjenesten før opdatering af applikationsfiler.

### Verificér tjenesten

For at bekræfte at tjenesten er registreret og kørende:

```bash
sudo launchctl list | grep digna
```

En linje der begynder med et proces-ID indikerer, at tjenesten kører. Et `-` i den første kolonne betyder, at den er registreret men stoppet.

### Flyt tjenesten til en ny mappe

launchd gemmer den absolutte sti til den eksekverbare fil, så flytning af installationen kræver gen-registrering af tjenesten:

1. **Afinstaller den nuværende tjeneste**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Flyt applikationsfilerne**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Geninstalér tjenesten**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Start tjenesten**
   ```bash
   sudo ./start_service.sh
   ```

### Afinstallér tjenesten

1. **Stop den kørende tjeneste**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Afinstallér tjenesten**
   ```bash
   sudo ./uninstall_service.sh
   ```

Digna-serveren er nu af-registreret fra launchd.

---

## Opgradering til en ny release {: #upgrading-to-a-new-release }

### Før du opgraderer

**Det er obligatorisk at lave en backup af digna-repositoriet**

Før du opgraderer digna, sikkerhedskopier dit repositorie (PostgreSQL) for at beskytte imod datatab.
En backup sikrer, at du kan gendanne, hvis opgraderingen støder på uventede problemer.

For at lave en backup fra Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Opgraderingsproces

#### Trin 1: Stop digna-tjenesten

Hvis digna kører som en baggrundstjeneste, stop den først:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Hvis digna kører i forgrunden, tryk `Ctrl + C` i dets Terminal-vindue.

#### Trin 2: Backup af nuværende backend-installation

I din digna-installationsmappe:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Trin 3: Udpak og deploy den nye version

1. Udpak den nye digna-installations-ZIP-fil
2. Kopiér den nye `digna`-eksekverbare og `dashboard`-mappen til din installationsmappe
3. Genskab den eksekverbare bit og, hvis nødvendigt, fjern quarantine-attributten:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Vigtigt"

    Filen `config.toml` medtages **aldrig** i installations-ZIP'en. Din eksisterende konfiguration er derfor sikker.

### Trin 4: Gendan dine konfigurationsfiler

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Trin 5: Opgrader repositorieschemaet

Navigér til din digna-installationsmappe og kør:

```bash
cd /opt/digna
./digna repo upgrade
```

Dette opdaterer PostgreSQL-schemaet til den nyeste version samtidig med, at alle eksisterende data bevares.

### Trin 6: Genstart tjenesterne

Hvis du kører som baggrundstjeneste:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Hvis du kører manuelt, genstart serveren:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Hvis du bruger nginx eller Apache, genstart den respektive webserver:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Trin 7: Verificér opgraderingen

1. Åbn digna-dashboardet
2. Bekræft at interfacet indlæses korrekt
3. Tjek serverens logs for eventuelle fejl