# macOS-installatiehandleiding voor digna Release 2026.11

**Release:** 2026.11

**Laatst bijgewerkt:** 7 november 2026


---

## Inhoudsopgave

1. [Introductie](#introduction)
2. [Systeemvereisten](#system-requirements)
3. [Voorbereiding vóór installatie](#pre-installation-setup)
4. [PostgreSQL-serverconfiguratie](#postgresql-server-setup)
5. [Webserverconfiguratie](#web-server-configuration)
6. [Initiële installatie](#initial-installation)
7. [Backendconfiguratie](#backend-configuration)
8. [Dashboardconfiguratie](#dashboard-configuration)
9. [digna als achtergrondservice draaien](#running-digna-as-a-background-service)
10. [Upgraden naar een nieuwe release](#upgrading-to-a-new-release)

---

## Introductie {: #introduction }

### Over digna

digna is een uitgebreid AI-gestuurd platform dat is ontworpen om het beheer van datakwaliteit te optimaliseren in uiteenlopende dataomgevingen zoals warehouses, lakes en lakehouses. Het is gebouwd om zeer schaalbaar en aanpasbaar te zijn en pakt moderne data-uitdagingen aan via automatisering, realtime monitoring en anomaliedetectie.

digna bestaat uit twee hoofdcomponenten:

- **digna**: de kern van de applicatie, verantwoordelijk voor het verwerken van gegevens en het uitvoeren van kwaliteitscontroles. Het combineert de backend en de opdrachtregelinterface in één uitvoerbaar bestand en vervangt daarmee de losse programma's `dignabackend` en `dignacli` uit eerdere releases.
- **dignadashboard**: Een webgebaseerde interface gehost op een webserver, die een gebruiksvriendelijke manier biedt om met het digna-platform te werken en datakwaliteitsstatistieken te visualiseren.

### Wat is nieuw in Release 2026.11

Deze release voegt digna Data Reconciliation toe, digna Agentic met de digna MCP Server, en de digna Engine, die data binnen digna kan profileren en referentiële integriteit kan controleren tussen verschillende databasetechnologieën. Zie de [release notes](../../../changelog/Release_202611.md) voor volledige details.

Voor een installatie brengt de release een nieuw migratiemechanisme voor de repository, een optionele `[duckdb]`-sectie in `config.toml` voor de digna Engine en een nieuw licentiebestand. De [upgradesectie](#upgrading-to-a-new-release) behandelt elk daarvan.

### Op zoek naar Windows of Linux?

Deze handleiding behandelt macOS. Voor andere platforms, zie de [Windows-installatiehandleiding](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) of de [Linux-installatiehandleiding](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Systeemvereisten {: #system-requirements }

Voordat u met de installatie begint, zorgt u ervoor dat uw systeem aan de volgende minimale vereisten voldoet:

| Vereiste | Specificatie |
|---|---|
| **Besturingssysteem** | macOS 13 (Ventura) of later |
| **Architectuur** | Apple Silicon (arm64) of Intel (x86_64) |
| **Geheugen (minimale opzet)** | 16 GB RAM |
| **Schijfruimte** | 10 GB beschikbare opslag |
| **Database** | PostgreSQL Server 12 of hoger |
| **Webserver** | nginx, Apache httpd, of gelijkwaardig |
| **Opdrachtregelprogramma's** | Xcode Command Line Tools (vereist door Homebrew) |

!!! info "digna Engine"

    Databaseverbindingen die de digna Engine als profileringslocatie gebruiken, worden op de digna-host zelf geprofileerd. Plan daarvoor extra geheugen en schijfruimte in, zie de [\[duckdb\]-sectie](#duckdb-section).

### Opties voor database-installatie

**Als PostgreSQL al is geïnstalleerd:**
U kunt een nieuwe database voor digna toevoegen aan uw bestaande PostgreSQL-server.

**Als u PostgreSQL op dezelfde machine als digna installeert:**

!!! info "Aanbevolen specificaties"

    - **Geheugen**: 32 GB RAM (in plaats van 16 GB)
    - **Schijfruimte**: 50 GB beschikbare opslag (in plaats van 10 GB)

    Deze hogere specificaties bieden ruimte voor zowel digna als de PostgreSQL-database die tegelijk draaien.

### Uw architectuur controleren

Verschillende paden in deze handleiding verschillen tussen Macs met Apple Silicon en Intel. Om te controleren welke u hebt, opent u **Terminal** en voert u uit:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installeert naar `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installeert naar `/usr/local`.

!!! tip "Tip"

    In plaats van een van beide paden vast te coderen, gebruikt deze handleiding `$(brew --prefix)`, dat op beide architecturen naar de juiste locatie wordt uitgebreid. U kunt de commando's letterlijk kopiëren.

---

## Voorbereiding vóór installatie {: #pre-installation-setup }

Voordat u digna installeert, zorgt u dat drie belangrijke vereisten aanwezig zijn:

1. **Homebrew** – de pakketbeheerder waarmee de onderstaande componenten worden geïnstalleerd
2. **PostgreSQL-server** – voor het opslaan van berekende metrics en prestatiegegevens
3. **Webserver** – voor het hosten van het digna-dashboard

Als deze componenten nog niet zijn ingesteld, volg dan de onderstaande secties om ze te installeren en te configureren.

### Homebrew installeren

Homebrew is de standaardpakketbeheerder voor macOS en wordt in deze hele handleiding gebruikt om PostgreSQL en nginx te installeren.

#### Stap 1: Controleer of Homebrew al is geïnstalleerd

Open **Terminal** (druk op `Cmd + Space`, typ `Terminal`, druk op Enter) en voer uit:

```bash
brew --version
```

Als er een versienummer wordt getoond, ga dan direct naar de sectie [PostgreSQL-serverconfiguratie](#postgresql-server-setup).

#### Stap 2: Installeer Homebrew

Als het commando niet werd gevonden, installeer Homebrew dan volgens de instructies op de [officiële Homebrew-site](https://brew.sh). Het installatieprogramma installeert ook de Xcode Command Line Tools als die nog niet aanwezig zijn.

#### Stap 3: Voeg Homebrew toe aan uw PATH

Op Apple Silicon toont het installatieprogramma twee commando's om Homebrew aan uw shell-omgeving toe te voegen. Voer ze uit zoals aangegeven en controleer daarna:

```bash
brew --prefix
```

Dit zou `/opt/homebrew` moeten tonen op Apple Silicon of `/usr/local` op Intel.

---

## PostgreSQL-serverconfiguratie {: #postgresql-server-setup }

### Als u PostgreSQL al hebt

Als PostgreSQL al is geïnstalleerd en draait op uw lokale machine, of als u een beheerde externe PostgreSQL-server gebruikt, kunt u doorgaan naar de [volgende sectie](#web-server-configuration).

### Installatieopties

macOS biedt twee eenvoudige manieren om PostgreSQL te installeren. Kies er **één**:

- [Homebrew](#postgresql-homebrew) — installatie via de opdrachtregel, aanbevolen voor serverimplementaties
- [Postgres.app](#postgresql-app) — grafische installatie, handig voor lokale evaluatie

### PostgreSQL installeren met Homebrew {: #postgresql-homebrew }

#### Stap 1: Installeer de PostgreSQL-formule

```bash
brew install postgresql@16
```

#### Stap 2: Voeg PostgreSQL toe aan uw PATH

Formules van PostgreSQL met een versienummer zijn *keg-only*, wat betekent dat Homebrew hun commando's niet automatisch in uw PATH koppelt. Voeg ze zelf toe:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Opmerking"

    Dit gaat uit van de standaard-`zsh`-shell van macOS. Als u `bash` gebruikt, voeg dezelfde regel dan toe aan `~/.bash_profile`.

#### Stap 3: Start de PostgreSQL-service

```bash
brew services start postgresql@16
```

Dit start PostgreSQL direct en stelt het zo in dat het automatisch opnieuw start wanneer u zich aanmeldt.

#### Stap 4: Verifieer de installatie

```bash
psql --version
```

U zou de PostgreSQL-versie moeten zien als de installatie is geslaagd.

#### Stap 5: Verbinden met de server

```bash
psql postgres
```

!!! warning "Belangrijk — macOS wijkt hier af van Windows"

    Het Windows-installatieprogramma vraagt u een `postgres`-superuser en wachtwoord aan te maken. Homebrew doet dat niet. In plaats daarvan maakt het een superuser aan met de naam van uw **macOS-account**, zonder wachtwoord, alleen bereikbaar vanaf de lokale machine.

    Dit betekent dat er op een nieuwe Homebrew-installatie geen `postgres`-rol bestaat. Gebruik uw eigen accountnaam wanneer u een superuser nodig hebt, en maak een expliciete digna-gebruiker aan zoals beschreven in [Initiële installatie](#initial-installation).

#### Stap 6: Bevestig de poort

De standaardpoort van PostgreSQL is `5432`. Om te bevestigen op welke poort uw server luistert:

```bash
psql postgres -c "SHOW port;"
```

Noteer de waarde — u hebt die nodig bij het configureren van de digna-backend.

### PostgreSQL installeren met Postgres.app {: #postgresql-app }

Als u de voorkeur geeft aan een grafische installatie:

1. Download [Postgres.app](https://postgresapp.com) en sleep het naar uw map **Applications**
2. Open de app en klik op **Initialize** om een nieuwe server aan te maken
3. Volg de instructies van de app om de opdrachtregelprogramma's aan uw PATH toe te voegen
4. Verifieer de installatie:

```bash
psql --version
```

Postgres.app maakt ook een superuser aan met de naam van uw macOS-account.

---

## Webserverconfiguratie {: #web-server-configuration }

digna heeft een webserver nodig om het dashboard te hosten. Kies een van de volgende opties:

- [nginx](#nginx-setup) — geïnstalleerd via Homebrew, aanbevolen
- [Apache httpd](#apache-setup) — meegeleverd met macOS

U hoeft slechts **één** van deze servers te installeren en te configureren.

Beide secties configureren twee zaken waarvan het dashboard afhankelijk is:

- **Een fallback voor single-page-applicaties**, zodat het vernieuwen van een dashboard-URL geen 404 oplevert
- **Een `.md`-MIME-type**, zodat Markdown-bestanden correct worden geserveerd

### nginx-configuratie {: #nginx-setup }

#### Overzicht

nginx is een lichtgewicht, krachtige webserver die zeer geschikt is voor het serveren van het statische digna-dashboard.

#### Installatie

```bash
brew install nginx
```

#### nginx starten

```bash
brew services start nginx
```

#### Verifieer de installatie

1. Open uw browser
2. Navigeer naar `http://localhost:8080`
3. U zou de welkomstpagina van nginx moeten zien

!!! note "Opmerking — de standaardpoort is 8080, niet 80"

    Homebrew configureert nginx om op poort `8080` te luisteren, zodat het zonder beheerdersrechten kan draaien. Op macOS vereist binden aan poort `80` of een andere poort onder 1024 root-rechten.

    Om het dashboard op poort 80 te serveren, wijzigt u `listen 8080;` in `listen 80;` in de onderstaande configuratie en start u nginx in plaats daarvan met `sudo brew services start nginx`.

#### Een site configureren voor het dashboard

De nginx-configuratie van Homebrew neemt elk bestand in de map `servers` op. Maak daar een apart configuratiebestand voor digna aan:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Plak het volgende en vervang `/path/to/digna/dashboard` door het werkelijke pad naar uw uitgepakte `dashboard`-map:

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

!!! warning "Belangrijk"

    Zonder de `try_files`-directive levert het herladen van elke dashboardpagina behalve de root-URL een 404 op. Dit is het nginx-equivalent van de URL Rewrite-module die IIS op Windows vereist.

#### Pas de configuratie toe

Test de configuratie op syntaxfouten en herlaad daarna nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd-configuratie {: #apache-setup }

#### Overzicht

macOS bevat Apache httpd, dus er is geen installatie nodig. Het is standaard uitgeschakeld.

#### Apache starten

```bash
sudo apachectl start
```

#### Verifieer de installatie

1. Open uw browser
2. Navigeer naar `http://localhost`
3. U zou het bericht "It works!" moeten zien

#### Vereist: mod_rewrite inschakelen

Het dashboard vereist URL-herschrijving. Open de Apache-configuratie:

```bash
sudo nano /etc/apache2/httpd.conf
```

Zoek de volgende regel en verwijder het voorloop-`#` om de regel te activeren:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Vereist: .htaccess-overrides toestaan

Zoek in hetzelfde bestand het blok `<Directory "/Library/WebServer/Documents">` en wijzig:

```apache
AllowOverride None
```

in:

```apache
AllowOverride All
```

#### Vereist: MIME-type voor Markdown-bestanden

Voeg, nog steeds in `httpd.conf`, de volgende regel toe zodat Markdown-bestanden correct worden geserveerd:

```apache
AddType text/markdown .md
```

!!! warning "Belangrijk"

    Zonder deze instelling worden `.md`-bestanden mogelijk niet correct geserveerd.

#### Pas de configuratie toe

Controleer de configuratie op syntaxfouten en herstart daarna Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Initiële installatie {: #initial-installation }

### Stap 1: Zet de digna-repository op

De digna-repository slaat alle door digna berekende metrics op. Ze fungeert als centrale database voor analytische en prestatiegegevens.

#### Maak het repository-schema en de gebruiker aan

Open uw PostgreSQL-client (psql, pgAdmin of vergelijkbaar) en voer de volgende SQL-commando's uit:

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

Om deze in één stap vanuit de Terminal uit te voeren:

```bash
psql postgres
```

Plak daarna de statements bij de prompt `postgres=#` en typ `\q` om af te sluiten.

!!! tip "Best Practice"

    Gebruik sterke, complexe wachtwoorden voor databasegebruikers. Vermijd gemakkelijk te raden inloggegevens.

---

### Stap 2: Pak het digna-installatiepakket uit

1. Zoek het digna-installatie-ZIP-bestand dat aan u is geleverd
2. Pak het uit naar uw gewenste installatieplek — bijvoorbeeld `/opt/digna` of `~/digna`
3. Na uitpakken zou u de volgende items moeten zien:
   - `dashboard/` — Webdashboard-interface
   - `digna` — Hoofdprogramma (backend + CLI gecombineerd)

!!! info "Het configuratie- en licentiebestand zitten niet in het pakket"

    Noch `config.toml` noch `dashboard/dashboard_config.toml` wordt met de installatie
    meegeleverd — u maakt beide zelf aan, in [Backendconfiguratie](#backend-configuration) en
    [Dashboardconfiguratie](#dashboard-configuration). Ook `license.toml` wordt niet meegeleverd;
    digna levert het afzonderlijk, zoals Stap 3 beschrijft.

Om vanuit de Terminal uit te pakken:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Maak het uitvoerbare bestand uitvoerbaar

Afhankelijk van hoe het archief is overgedragen, blijft het uitvoerbaar-bit bij het uitpakken mogelijk niet behouden. Stel het expliciet in:

```bash
cd /opt/digna
chmod +x digna
```

#### Als macOS de applicatie blokkeert

Bestanden die via een browser of mailprogramma zijn gedownload, krijgen een quarantaine-attribuut. Als macOS meldt dat de app *"niet kan worden geopend omdat de ontwikkelaar niet kan worden geverifieerd"*, verwijder het attribuut dan uit de installatiemap:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

U kunt ook **System Settings → Privacy & Security** openen, het geblokkeerde item onderaan de pagina zoeken en op **Open Anyway** klikken.

!!! note "Opmerking"

    Deze stap is alleen nodig als macOS het uitvoerbare bestand daadwerkelijk blokkeert. Pakketten die via SSH of vanaf interne netwerkshares zijn overgedragen, worden meestal niet in quarantaine geplaatst.

### Stap 3: Installeer het licentiebestand

!!! warning "Belangrijk"

    Het licentiebestand is **niet** inbegrepen in het installatiepakket en wordt apart door digna verstrekt.

1. Zoek het `license.toml`-bestand dat aan u is geleverd
2. Kopieer het in de root van de digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)

**Waarom dit van belang is:**
Het licentiebestand bevat uw klantgegevens, licentievervaldatum en digitale handtekening. **Wijzig dit bestand niet** — elke aanpassing maakt de licentie ongeldig.

**Mapstructuur na installatie:**

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

## Backendconfiguratie {: #backend-configuration }

### Stap 1: Maak en bewerk het configuratiebestand

Het `config_template.toml`-bestand wordt meegeleverd in uw digna-installatiemap. U hoeft het alleen maar te hernoemen naar `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Locatie:** `/opt/digna/config.toml`

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

!!! note "Opmerking"

    Als u het dashboard serveert vanaf de nginx van Homebrew op de standaardpoort, is de origin die u moet toestaan `http://localhost:8080`.

!!! info "De [app]-sectie is optioneel"

    Vanaf Release 2026.11 mogen beide sleutels, en de hele `[app]`-sectie, worden weggelaten. Dat is de juiste opzet wanneer een reverse proxy het dashboard en de backend onder één origin serveert: de browser doet dan geen cross-origin-verzoeken, en standaard wordt er geen enkele toegestaan.

#### [repo] Sectie

Deze sectie configureert de verbinding met de PostgreSQL-database:

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
| `DIGNA_REPO_PASSWORD` | Uw wachtwoord | Wachtwoord ingesteld tijdens het aanmaken van het schema |
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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 uur) | Sessietimeout in seconden |
| `DIGNA_MAX_WORKERS` | Aantal CPU-cores - 1 | Aantal inspecties dat tegelijk mag draaien |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Vereist. Wordt gebruikt voor de links in meldingsberichten en moet dus een URL zijn die de ontvangers kunnen openen |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standaard) | Optioneel. Aantal seconden dat één query op een brondatabase mag draaien voordat deze wordt afgebroken; `0` schakelt de time-out uit |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standaard) | Optioneel. Aantal seconden dat wordt gewacht op een verbinding met een brondatabase; `0` wacht onbeperkt |

!!! tip "Tip"

    Om het aantal beschikbare CPU-cores op uw Mac te vinden, voert u `sysctl -n hw.ncpu` uit.

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

    Deze sleutel is een vaste waarde, identiek in alle digna-installaties, en het is de sleutel die
    de gevoelige waarden in uw repository ontsleutelt. Beperk `config.toml` tot het account waaronder
    digna draait, houd het bestand buiten versiebeheer en gedeelde schijven, en sluit het uit van elke
    back-up die minder veilig wordt bewaard dan de repository zelf.

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

#### [duckdb] Sectie (optioneel) {: #duckdb-section }

Nieuw in Release 2026.11. Deze sectie bepaalt de resources van de **digna Engine**, die data binnen digna profileert voor databaseverbindingen met **digna Engine** als profileringslocatie, en die controles op referentiële integriteit uitvoert tussen datasources op verschillende databaseverbindingen. Zie [Profileringslocatie](../../../platform/profiling/profiling_location.md).

De sectie is optioneel. Zonder deze sectie gelden de onderstaande standaardwaarden.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standaard) | Geheugen, in MB, dat één run van de digna Engine mag gebruiken. Er kunnen tot `DIGNA_MAX_WORKERS` runs tegelijk actief zijn |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standaard: de tijdelijke map van het systeem (`$TMPDIR` van het account waaronder digna draait) | Map voor tijdelijke bestanden wanneer de data niet in het geheugen past |

!!! tip "De digna Engine dimensioneren"

    Reken op maximaal `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` aan geheugen op de digna-host, bovenop wat digna zelf gebruikt, en op voldoende vrije schijfruimte in de tijdelijke map voor de grootste geïnspecteerde datum van de datasources die de digna Engine gebruiken. Laat `DIGNA_DUCKDB_TEMP_DIRECTORY` verwijzen naar een schijf met die ruimte, beschrijfbaar voor het account waaronder digna draait:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    U hebt deze sectie alleen nodig als ten minste één databaseverbinding de digna Engine gebruikt, of als een controle op referentiële integriteit datasources op verschillende verbindingen vergelijkt.

---

### Stap 2: Configuratie valideren

Controleer voordat u de repository initialiseert of `config.toml` volledig en correct opgebouwd is. Voer in uw digna-installatiemap uit:

```bash
./digna config check
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

1. Open **Terminal**
2. Navigeer naar uw digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)
3. Voer de verbindingscontrole uit:

```bash
cd /opt/digna
./digna repo check
```

Bij een nieuw schema maakt het commando verbinding en meldt het vervolgens dat er nog geen repository is geïnstalleerd:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Op dit punt is dat het verwachte resultaat: het bevestigt dat digna PostgreSQL en het schema bereikt. Een verbindings- of authenticatiefout wijst daarentegen op de `[repo]`-sectie of op de PostgreSQL-installatie.

!!! note "Opmerking"

    Op macOS staan commando's in de huidige map niet in uw PATH, dus het uitvoerbare bestand wordt aangeroepen als `./digna` in plaats van `digna`. Om overal de korte vorm te gebruiken, voegt u de installatiemap toe aan uw PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Stap 4: Installeer het repository-schema

Voer in dezelfde map uit:

```bash
./digna repo upgrade
```

Dit commando installeert de benodigde tabellen in het repository-schema en eindigt met:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installeert en upgradet"

    Vanaf Release 2026.11 installeert `repo upgrade` een nieuwe repository en upgradet het een bestaande. `repo install` werkt nog steeds als andere naam voor hetzelfde commando.

### Stap 5: Maak een admin-gebruiker aan

De admin-gebruiker wordt rechtstreeks in het repository-schema aangemaakt, dus de server hoeft nog niet te draaien. Voer in de digna-installatiemap uit:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Voorbeeld:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Hiermee wordt een gebruiker aangemaakt met het e-mailadres `admin@example.com` en volledige beheerdersrechten.

!!! tip "Tip"

    Zet het wachtwoord tussen enkele aanhalingstekens. `zsh` behandelt tekens zoals `!`, `$` en `*` speciaal, en een niet-geciteerd wachtwoord met deze tekens wordt niet doorgegeven zoals u het hebt getypt.

!!! tip "Best Practice"

    Gebruik een sterk wachtwoord met een mix van hoofdletters, kleine letters, cijfers en speciale tekens.

### Stap 6: Start de digna-server

In de digna-installatiemap start u de server met:

```bash
./digna serve --address <host> --port <port>
```

**Parameters:**
- `--address` — Server hostname/IP (standaard `127.0.0.1`)
- `--port` — Serverpoort (standaard `8000`)

Zodra de server draait, toont hij het adres waarop hij luistert:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tip"

    De eerste keer dat u de server start, kan macOS vragen of de applicatie inkomende netwerkverbindingen mag accepteren. Klik op **Allow**, anders kan het dashboard de backend niet bereiken.

!!! note "De server houdt de terminal bezet"

    `serve` draait op de voorgrond en blijft draaien totdat u het stopt met ++ctrl+c++. Laat het draaien terwijl u de installatie afrondt; zie [digna als achtergrondservice draaien](#running-digna-as-a-background-service) om het in plaats daarvan automatisch bij het opstarten te starten.

---

## Dashboardconfiguratie {: #dashboard-configuration }

### Stap 1: Zet het dashboard uit op de webserver

Het digna-dashboard leest zijn eigen configuratie uit `dashboard/dashboard_config.toml`. Dat bestand wordt niet met de installatie meegeleverd — u maakt het aan in de `dashboard/`-map, naast de dashboardbestanden.

De inhoud ervan wordt beschreven onder [Single Sign-On](../../../sso/overview.md), en daar is het bestand ook nodig: het bevat de aanmeldopties die het dashboard aanbiedt en, voor multi-instance-implementaties, de backend-verbinding.

Kies uw webserver en volg de bijbehorende deployment-stappen.

#### Deployen naar nginx

Als u de sectie [nginx-configuratie](#nginx-setup) hebt gevolgd, verwijst het serverblok al naar uw `dashboard`-map en hoeft er niets te worden gekopieerd.

1. **Bevestig het pad**
   - Open `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Controleer of `root` naar uw uitgepakte `dashboard`-map verwijst

2. **Zorg dat de map leesbaar is**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Herlaad nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Test de installatie**
   - Open uw browser
   - Navigeer naar `http://localhost:8080` (of uw geconfigureerde URL)
   - U zou de aanmeldpagina van het digna-dashboard moeten zien

#### Deployen naar Apache httpd

1. **Kopieer het dashboard naar de document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Voeg de rewrite-regels toe**

   Maak een `.htaccess`-bestand aan in de uitgerolde map, zodat dashboardroutes een browservernieuwing overleven:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Plak het volgende:

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

3. **Herstart Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Open het dashboard**
   - Open uw browser
   - Navigeer naar `http://localhost/digna`
   - U zou de aanmeldpagina van het digna-dashboard moeten zien

---

## digna als achtergrondservice draaien {: #running-digna-as-a-background-service }

### Waarom digna als service draaien?

Door de digna-backend als achtergrondservice te draaien, zorgt u ervoor dat deze:

- Automatisch start wanneer de machine opstart
- Op de achtergrond draait zonder een geopend Terminal-venster
- Automatisch opnieuw start als deze crasht
- Beheerd kan worden via `launchctl`, de servicebeheerder van macOS

### Bestanden voor servicebeheer

Alle benodigde bestanden bevinden zich in de digna-installatiemap onder: `bin/`

De volgende shellscripts zijn beschikbaar:

- `install_service.sh` — Registreert digna bij launchd
- `uninstall_service.sh` — Deregistreert de service
- `start_service.sh` — Start de geregistreerde service
- `stop_service.sh` — Stopt de draaiende service

!!! warning "Beheerdersrechten vereist"

    Alle scripts moeten met `sudo` worden uitgevoerd, omdat het registreren van een service die bij het opstarten start naar `/Library/LaunchDaemons` schrijft.

### De scripts uitvoerbaar maken

Bij het uitpakken blijft het uitvoerbaar-bit mogelijk niet behouden. Vóór het eerste gebruik:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### De service installeren

1. **Open Terminal**

2. **Navigeer naar de bin-map**
   ```bash
   cd /opt/digna/bin
   ```

3. **Voer het installatiescript uit**
   ```bash
   sudo ./install_service.sh
   ```

De digna-server is nu bij launchd geregistreerd met **automatische opstart** ingeschakeld. De service start niet direct — zie de volgende sectie om deze te starten.

### De service starten en stoppen

#### Om de service te starten

1. Open Terminal
2. Navigeer naar `/opt/digna/bin`
3. Voer uit:
   ```bash
   sudo ./start_service.sh
   ```

#### Om de service te stoppen

1. Open Terminal
2. Navigeer naar `/opt/digna/bin`
3. Voer uit:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Stop de service altijd voordat u applicatiebestanden bijwerkt.

### De service verifiëren

Om te bevestigen dat de service geregistreerd is en draait:

```bash
sudo launchctl list | grep digna
```

Een regel die met een proces-ID begint, geeft aan dat de service draait. Een `-` in de eerste kolom betekent dat de service geregistreerd maar gestopt is.

### De service naar een nieuwe map verplaatsen

launchd slaat het absolute pad naar het uitvoerbare bestand op, dus het verplaatsen van de installatie vereist dat de service opnieuw wordt geregistreerd:

1. **Deïnstalleer de huidige service**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Verplaats de applicatiebestanden**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Installeer de service opnieuw**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Start de service**
   ```bash
   sudo ./start_service.sh
   ```

### De service verwijderen

1. **Stop de draaiende service**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Deïnstalleer de service**
   ```bash
   sudo ./uninstall_service.sh
   ```

De digna-server is nu bij launchd gederegistreerd.

---

## Upgraden naar een nieuwe release {: #upgrading-to-a-new-release }

Deze sectie upgradet een installatie van Release 2026.06 naar Release 2026.11.

!!! warning "Upgraden vanaf een release ouder dan 2026.06"

    Voer eerst de upgradestappen van Release 2026.06 uit: [Upgraden naar een nieuwe release](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Ga daarna verder met de stappen hieronder.

### Voordat u gaat upgraden

**Het aanmaken van een backup van de digna-repository is verplicht**

Maak vóór het upgraden een backup van uw repository (PostgreSQL) om gegevensverlies te voorkomen. Een backup zorgt ervoor dat u kunt herstellen als de upgrade onverwachte problemen veroorzaakt.

Om een backup vanuit de Terminal te maken:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Het licentiebestand voor Release 2026.11 aanvragen**

Release 2026.11 heeft een nieuw `license.toml` nodig. Vraag het bij het digna-team aan voordat u begint, en houd het gereed voor [Stap 7](#step-7-replace-the-license-file).

### Upgradeproces

#### Stap 1: Stop de digna-service {: #step-1-stop-the-digna-service }

Als digna als achtergrondservice draait, stop deze dan eerst:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Als digna op de voorgrond draait, druk dan op ++ctrl+c++ in het bijbehorende Terminal-venster.

#### Stap 2: Huidige installatie veiligstellen {: #step-2-backup-current-installation }

Hernoem in uw digna-installatiemap het uitvoerbare bestand en de dashboardmap van uw huidige installatie, zodat de nieuwe release ernaast kan worden uitgerold:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Bewaar `digna_old` totdat u de upgrade hebt geverifieerd, en `dashboard_old` totdat u uw configuratiebestanden eruit hebt teruggezet (zie Stap 4). Daarna kunt u beide verwijderen.

#### Stap 3: Pak de nieuwe versie uit en deploy {: #step-3-extract-and-deploy-new-version }

1. Pak het nieuwe digna-installatie-ZIP-bestand uit
2. Kopieer het nieuwe `digna`-uitvoerbare bestand en de `dashboard`-map naar uw installatiemap
3. Herstel het uitvoerbaar-bit en verwijder zo nodig het quarantaine-attribuut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Belangrijk"

    Noch `config.toml` noch `dashboard/dashboard_config.toml` wordt ooit in het installatie-ZIP opgenomen — het digna-team levert geen van beide bestanden mee. Uw bestaande configuratie blijft bij de upgrade dus onaangeroerd, en de kopieën in de hernoemde `*_old`-mappen zijn de enige die u hebt.

#### Stap 4: Herstel uw configuratiebestanden {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

Het dashboard bestaat uit statische bestanden, dus uw webserver — en de browser — kan nog steeds de vorige versie serveren. Herlaad of herstart de webserver die de `dashboard`-map host, en herlaad de pagina daarna met een harde vernieuwing (++cmd+shift+r++).

#### Stap 6: Configuratie valideren {: #step-6-validate-the-configuration }

Controleer of `config.toml` volledig is voordat u de repository aanraakt:

```bash
./digna config check
```

Elke sectie moet OK melden. Los alles op wat als FAILED wordt gemeld, verwijder de sleutels die onder **Unknown keys** staan, en voer het commando opnieuw uit voordat u verdergaat.

#### Stap 7: Vervang het licentiebestand {: #step-7-replace-the-license-file }

Een licentiebestand gaat normaal gesproken mee van de ene release naar de volgende. Release 2026.11 is een uitzondering: deze release voegt twee gelicentieerde modules toe, digna Data Reconciliation en digna Agentic, en een licentie die vóór 2026.11 is uitgegeven, bevat ze niet. Kopieer het `license.toml` dat het digna-team voor Release 2026.11 heeft geleverd naar de installatiemap, ter vervanging van het oude:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Behoud de vorige licentie niet"

    Met de vorige licentie start digna nog wel, maar digna Data Reconciliation en de digna MCP Server blijven uitgeschakeld. Elk commando dat de licentie controleert — `user`, `inspection`, `repo` — breekt af voordat het de repository aanraakt wanneer de controle mislukt. Controleer de nieuwe licentie voordat u verdergaat:

    ```bash
    ./digna license check
    ```

#### Stap 8: Upgrade het repository-schema {: #step-8-upgrade-the-repository-schema }

Voer in uw digna-installatiemap uit:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 beheert het repository-schema met geversioneerde migraties. De eerste upgrade vanaf een eerdere release brengt het schema naar de laatste versie van het vorige mechanisme, legt dat vast als startpunt en past daarna de migraties van Release 2026.11 toe. De upgrade eindigt met:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Alle bestaande gegevens blijven behouden. Voer op elk moment `./digna repo check` uit om de toestand van de repository te zien: het commando toont de laatst toegepaste migratie en eventuele openstaande migraties.

!!! warning "digna start niet op een verouderde repository"

    Vanaf Release 2026.11 weigert de server te starten zolang de repository een upgrade nodig heeft, en meldt dat, bijvoorbeeld:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Voer `repo upgrade` uit voordat u de server of de service start.

#### Stap 9: Herstart services {: #step-9-restart-services }

Als digna als achtergrondservice draait:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Als u de server handmatig draait, start deze dan opnieuw:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Als u nginx of Apache gebruikt, herstart dan de betreffende webserver:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Stap 10: Verifieer de upgrade {: #step-10-verify-the-upgrade }

1. Controleer de release van het nieuwe uitvoerbare bestand:

    ```bash
    ./digna version
    ```

    De eerste regel moet `Release: 2026.11` luiden.

2. Ga naar het digna-dashboard en controleer of de interface correct laadt.
3. Controleer de serveruitvoer en de bestanden in de map `logs` op fouten.
4. Test uw databaseverbindingen — zie [Een verbinding testen](../../../databases/overview.md#testing-a-connection). Zet na een upgrade vanaf een release vóór 2026.06 eerst elke verbinding die nog geen ODBC gebruikte om naar ODBC.

Om met de nieuwe modules te beginnen, zie [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Een AI-agent verbinden](../../../platform/agentic/connect_ai_agent.md) voor de digna MCP Server, en [Profileringslocatie](../../../platform/profiling/profiling_location.md) voor de digna Engine.