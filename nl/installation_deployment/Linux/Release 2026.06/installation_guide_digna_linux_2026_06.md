# Linux-installatiehandleiding voor digna Release 2026.06

**Release:** 2026.06

**Laatst bijgewerkt:** 5 september 2026


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
9. [digna als systemd-service draaien](#running-digna-as-a-systemd-service)
10. [Upgraden naar een nieuwe release](#upgrading-to-a-new-release)

---

## Introductie {: #introduction }

### Over digna

digna is een uitgebreid AI-gestuurd platform dat is ontworpen om het beheer van datakwaliteit te optimaliseren in uiteenlopende dataomgevingen zoals warehouses, lakes en lakehouses. Het is gebouwd om zeer schaalbaar en aanpasbaar te zijn en pakt moderne data-uitdagingen aan via automatisering, realtime monitoring en anomaliedetectie.

digna bestaat uit twee hoofdcomponenten:

- **dignabackend**: De kernmotor van de applicatie, verantwoordelijk voor het verwerken van data en het uitvoeren van kwaliteitscontroles.
- **dignadashboard**: Een webgebaseerde interface gehost op een webserver, die een gebruiksvriendelijke manier biedt om met het digna-platform te werken en datakwaliteitsstatistieken te visualiseren.

### Wat is nieuw in Release 2026.06

Deze release brengt data-observability-mogelijkheden rechtstreeks in je code, zodat ontwikkelaars datakwaliteit aan de bron kunnen monitoren. Zie de [release notes](http://docs.digna.ai/changelog/Release_202606/) voor volledige details.

### Op zoek naar Windows of macOS?

Deze handleiding behandelt Linux. Voor andere platforms, zie de [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) of de [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Voor welke distributie geldt deze handleiding?

De instructies zijn geschreven voor de twee meest voorkomende serverfamilies. Waar ze verschillen, worden beide commando's gegeven:

- **Debian-familie** — Debian, Ubuntu. Pakketbeheerder: `apt`.
- **RHEL-familie** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Pakketbeheerder: `dnf`.

Elke moderne distributie met `systemd` werkt; alleen de pakketnamen en enkele configuratiepaden verschillen.

---

## Systeemvereisten {: #system-requirements }

Voordat u met de installatie begint, zorgt u ervoor dat uw systeem aan de volgende minimale vereisten voldoet:

| Vereiste | Specificatie |
|---|---|
| **Besturingssysteem** | Ubuntu 22.04 LTS of later, Debian 12 of later, RHEL 9 / Rocky 9 / AlmaLinux 9 of later |
| **Architectuur** | x86_64 (amd64) of arm64 |
| **Init-systeem** | systemd |
| **Geheugen (minimale opzet)** | 16 GB RAM |
| **Schijfruimte** | 10 GB beschikbare opslag |
| **Database** | PostgreSQL Server 12 of hoger |
| **Webserver** | nginx, Apache httpd, of gelijkwaardig |

### Opties voor database-installatie

**Als PostgreSQL al is geïnstalleerd:**
Je kunt een nieuwe database voor digna toevoegen aan je bestaande PostgreSQL-server.

**Als je PostgreSQL op dezelfde machine als digna installeert:**

!!! info "Aanbevolen specificaties"

    - **Geheugen**: 32 GB RAM (in plaats van 16 GB)
    - **Schijfruimte**: 50 GB beschikbare opslag (in plaats van 10 GB)

    Deze hogere specificaties bieden ruimte voor zowel digna als de PostgreSQL-database die tegelijk draaien.

### Controleren van distributie en architectuur

Verschillende commando's in deze handleiding verschillen tussen de Debian- en RHEL-families. Om te controleren welke u gebruikt, voer uit:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` of `ID=debian` — gebruik de `apt`-commando's.
- `ID=rhel`, `rocky`, `almalinux` of `fedora` — gebruik de `dnf`-commando's.
- `x86_64` of `aarch64` — de architectuur van het installatiepakket dat u nodig hebt.

---

## Voorbereiding vóór installatie {: #pre-installation-setup }

Voordat u digna installeert, zorgt u dat twee belangrijke vereisten aanwezig zijn:

1. **PostgreSQL-server** – voor het opslaan van berekende metrics en prestatiegegevens
2. **Webserver** – voor het hosten van het digna-dashboard

Als deze componenten nog niet zijn ingesteld, volg dan de onderstaande secties om ze te installeren en te configureren.

### Vernieuwen van de pakketindex

Werk uw pakketlijsten bij voordat u iets installeert:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Opmerking"

    Door de hele handleiding geldt: het eerste commando in een paar is voor de **Debian-familie** en het tweede voor de **RHEL-familie**. Voer alleen degene uit die bij uw systeem hoort.

---

## PostgreSQL-serverconfiguratie {: #postgresql-server-setup }

### Als u al PostgreSQL heeft

Als PostgreSQL al is geïnstalleerd en actief op uw lokale machine of als u een beheerde externe PostgreSQL-server gebruikt, kunt u doorgaan naar de [volgende sectie](#web-server-configuration).

### PostgreSQL installeren

#### Stap 1: Installeer het serverpakket

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Tip"

    Distributiepakketten kunnen achterlopen op de actuele PostgreSQL-release. Als u een specifieke nieuwere versie nodig hebt, gebruik dan de officiële [PostgreSQL apt- of yum-repository](https://www.postgresql.org/download/linux/).

#### Stap 2: Initialiseer de databasecluster

Bij de **Debian-familie** maakt en start het pakket automatisch een cluster — sla deze stap dan over.

Bij de **RHEL-familie** moet de cluster expliciet worden aangemaakt:

```bash
sudo postgresql-setup --initdb
```

#### Stap 3: Start en zet de service aan

```bash
sudo systemctl enable --now postgresql
```

Dit start PostgreSQL onmiddellijk en zorgt ervoor dat het ook automatisch start bij het opstarten.

#### Stap 4: Verifieer de installatie

```bash
psql --version
sudo systemctl status postgresql
```

U zou de PostgreSQL-versie en een `active (running)` service moeten zien.

#### Stap 5: Verbinden met de server

Een Linux PostgreSQL-pakket maakt een `postgres` systeemaccount dat de cluster bezit. Verbind hiermee:

```bash
sudo -u postgres psql
```

!!! note "Opmerking — Linux verschilt hier van Windows"

    De Windows-installer vraagt tijdens de installatie om een wachtwoord voor de `postgres` superuser. Linux-pakketten doen dat niet. In plaats daarvan worden lokale verbindingen geverifieerd via **peer authentication**: de `postgres` OS-gebruiker mag zonder wachtwoord verbinden als de `postgres` databasegebruiker.

    Daarom gebruikt het bovenstaande commando `sudo -u postgres`. De digna-backend maakt verbinding via TCP met een gebruikersnaam en wachtwoord, dus u maakt een expliciete digna-gebruiker aan in [Initiële installatie](#initial-installation).

#### Stap 6: Bevestig de poort

De standaard PostgreSQL-poort is `5432`. Om te bevestigen op welke poort uw server luistert:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Noteer de waarde — u heeft deze nodig bij het configureren van de digna-backend.

#### Stap 7: Schakel wachtwoordverificatie in voor de digna-gebruiker

digna maakt verbinding met PostgreSQL via TCP als `digna_user`, wat wachtwoordverificatie vereist in plaats van peer authentication. Controleer dat uw `pg_hba.conf` dit toestaat.

Vind het bestand:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Open het in een editor en controleer of de lokale TCP-regels `scram-sha-256` (of `md5` op oudere servers) gebruiken in plaats van `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Herlaad PostgreSQL na elke wijziging:

```bash
sudo systemctl reload postgresql
```

!!! warning "Belangrijk"

    Als digna `FATAL: Ident authentication failed for user "digna_user"` meldt, is deze instelling de oorzaak.

#### Stap 8: Als PostgreSQL op een andere machine draait

Om verbindingen van een andere host te accepteren, stel `listen_addresses` in `postgresql.conf` in en voeg een bijpassende `host`-regel toe voor uw netwerk in `pg_hba.conf`:

```
listen_addresses = '*'
```

Open vervolgens de poort in de firewall en start de service opnieuw:

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

## Webserverconfiguratie {: #web-server-configuration }

digna heeft een webserver nodig om het dashboard te hosten. Kies een van de volgende opties:

- [nginx](#nginx-setup) — lichtgewicht en aanbevolen
- [Apache httpd](#apache-setup) — veelgebruikte alternatieve

U hoeft slechts **één** van deze servers te installeren en te configureren.

Beide secties configureren twee zaken waarvan het dashboard afhankelijk is:

- **Een single-page-application fallback**, zodat het vernieuwen van een dashboard-URL geen 404 geeft
- **Een `.md` MIME-type**, zodat Markdown-bestanden correct worden geserveerd

### nginx-configuratie {: #nginx-setup }

#### Overzicht

nginx is een lichtgewicht, hoogpresterende webserver, goed geschikt voor het serveren van het statische digna-dashboard.

#### Installatie

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx starten

```bash
sudo systemctl enable --now nginx
```

#### Verifieer de installatie

1. Open uw browser
2. Navigeer naar `http://localhost`
3. U zou de nginx-welkomstpagina moeten zien

#### Firewall openen

Als de server vanaf andere machines bereikbaar is, sta HTTP-verkeer toe:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Een site configureren voor het dashboard

nginx include elke file in zijn `conf.d`-map op beide distributiefamilies. Maak daar een dedicated configuratiebestand voor digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Plak het volgende en vervang `/opt/digna/dashboard` door het werkelijke pad naar uw uitgepakte `dashboard`-map:

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

!!! warning "Belangrijk"

    Zonder de `try_files`-directive geeft het herladen van een dashboardpagina anders dan de root-URL een 404. Dit is het nginx-equivalent van de URL Rewrite-module die op IIS onder Windows vereist is.

#### De standaardsite uitschakelen

Slechts één serverblok kan `default_server` voor een poort zijn. Bij de **Debian-familie**, verwijder de meegeleverde default zodat deze niet in conflict komt:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Bij de **RHEL-familie**, zet het `server { ... }`-blok in `/etc/nginx/nginx.conf` uit door het te commentariëren of te verwijderen.

#### Pas de configuratie toe

Test de configuratie op syntaxisfouten en herlaad nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd-configuratie {: #apache-setup }

#### Overzicht

Apache httpd is beschikbaar in de standaardrepositories van alle ondersteunde distributies. Het pakket heet `apache2` op de Debian-familie en `httpd` op de RHEL-familie.

#### Installatie

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache starten

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Verifieer de installatie

1. Open uw browser
2. Navigeer naar `http://localhost`
3. U zou de standaard Apache-pagina van de distributie moeten zien

#### Vereist: mod_rewrite inschakelen

Het dashboard vereist URL-rewriting.

Bij de **Debian-familie**, schakel de module in en herstart:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Bij de **RHEL-familie** wordt `mod_rewrite` standaard geladen. Controleer dit:

```bash
httpd -M | grep rewrite
```

#### Vereist: .htaccess-overrides toestaan

Open het configuratiebestand voor uw documentroot:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Zoek het `<Directory>`-blok dat uw documentroot dekt (`/var/www/html` op beide families) en wijzig:

```apache
AllowOverride None
```

naar:

```apache
AllowOverride All
```

#### Vereist: MIME-type voor Markdown-bestanden

Voeg in hetzelfde bestand de volgende regel toe zodat Markdown-bestanden correct worden geserveerd:

```apache
AddType text/markdown .md
```

!!! warning "Belangrijk"

    Zonder deze instelling worden `.md`-bestanden mogelijk niet correct geserveerd.

#### Pas de configuratie toe

Controleer de configuratie op syntaxisfouten en herstart Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Initiële installatie {: #initial-installation }

### Stap 1: Zet de digna-repository op

De digna-repository slaat alle door digna berekende metrics op. Het fungeert als de centrale database voor analytische en prestatiegegevens.

#### Maak de repository-schema en gebruiker aan

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

Om deze vanuit de shell in één stap uit te voeren:

```bash
sudo -u postgres psql
```

Plak vervolgens de statements op de `postgres=#` prompt en typ `\q` om af te sluiten.

!!! tip "Best Practice"

    Gebruik sterke, complexe wachtwoorden voor databasegebruikers. Vermijd gemakkelijk te raden inloggegevens.

---

### Stap 2: Pak het digna-installatiepakket uit

1. Zoek het digna-installatie-ZIP-bestand dat aan u is geleverd
2. Pak het uit naar uw gewenste installatieplek — bijvoorbeeld `/opt/digna`
3. Na uitpakken zou u de volgende items moeten zien:
   - `dashboard/` — Webdashboard-interface
   - `digna` — Hoofdprogramma (backend + CLI gecombineerd)
   - `config.toml` — Configuratiebestand
   - `license.toml` — Licentiebestand (kopieer uw licentie hierheen)

Om vanuit de shell uit te pakken:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Opmerking"

    Als `unzip` niet is geïnstalleerd, voeg het toe met `sudo apt install -y unzip` of `sudo dnf install -y unzip`.

#### Maak het uitvoerbare bestand uitvoerbaar

Afhankelijk van hoe het archief is overgezet, kan het uitvoerbit verloren zijn gegaan. Stel het expliciet in:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Maak een serviceaccount aan

Het is aanbevolen om de backend als een dedicated niet-geprivilegieerde gebruiker te draaien voor productie-omgevingen:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Opmerking"

    Op de RHEL-familie is het equivalente shell-pad `/sbin/nologin`.

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
sudo mv config_template.toml config.toml
```

**Locatie:** `/opt/digna/config.toml`

Open `config.toml` in een teksteditor en configureer elke sectie hieronder.

#### [app] Sectie

Deze sectie configureert de applicatie-instellingen van de digna-backend:

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
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Als het dashboard op een andere server staat, voeg die URL toe |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vereist voor CORS met credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Sta alle HTTP-methoden toe |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Sta alle headers toe |

!!! note "Opmerking"

    Als u het dashboard vanaf nginx of Apache op de standaard HTTP-poort serveert, is de origin die u moet toestaan `http://localhost` — of de publieke URL van de server wanneer het dashboard vanaf andere machines bereikbaar is.

#### [repo] Sectie

Deze sectie configureert de verbinding met de PostgreSQL-database:

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
| `digna_REPO_PASSWORD` | Uw wachtwoord | Wachtwoord ingesteld tijdens het aanmaken van het schema |

!!! tip "Best Practice"

    `config.toml` bevat een databasewachtwoord in platte tekst. Beperk de permissies zodat alleen het serviceaccount het kan lezen:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `digna_COOKIE_DOMAIN` | `localhost` | Komt overeen met uw frontend-domein |
| `digna_COOKIE_SECURE` | `false` (lokaal) / `true` (productie) | Gebruik `true` voor HTTPS-verbindingen |
| `digna_COOKIE_HTTPONLY` | `true` | Altijd ingeschakeld voor beveiliging |
| `digna_COOKIE_SAME_SITE` | `lax` | Voorkomt CSRF-aanvallen |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 uur) | Sessietimeout in seconden |
| `digna_MAX_WORKERS` | Aantal CPU-cores - 1 | Aantal parallelle inspectietaken |

!!! tip "Tip"

    Om het aantal beschikbare CPU-cores op uw server te vinden, voert u `nproc` uit.

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

### Stap 2: Initialiseer de repository

1. Open een terminal
2. Navigeer naar uw digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)
3. Voer de verbindingscontrole uit:

```bash
cd /opt/digna
./digna repo check
```

U zou een bevestiging moeten zien dat de verbinding tot stand is gebracht (de repository zelf is nog niet geïnitieerd).

!!! note "Opmerking"

    Op Linux staat de huidige map niet in uw PATH, dus het uitvoerbare bestand wordt aangeroepen als `./digna` in plaats van `digna`. Om overal de korte vorm te gebruiken, maak een symbolische link:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Stap 3: Installeer het repository-schema

Voer in dezelfde map uit:

```bash
./digna repo install
```

Dit commando installeert de benodigde tabellen en het schema in uw PostgreSQL-database.

### Stap 4: Start de digna-server

In de digna-installatiemap start u de server met:

```bash
./digna serve --address <host> --port <port>
```

**Parameters:**
- `--address` — Server hostname/IP
- `--port` — Serverpoort

U zou opstartberichten moeten zien die bevestigen dat de server draait:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tip"

    Als het dashboard vanaf een andere machine wordt geserveerd dan de backend, open dan ook de API-poort in de firewall:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Stap 5: Maak een admin-gebruiker aan

1. Open een **nieuw** terminalvenster
2. Navigeer naar uw digna-installatiemap
3. Voer het volgende commando uit om een admin-gebruiker aan te maken:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Voorbeeld:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Dit maakt een gebruiker aan met gebruikersnaam `admin` en volledige administratieve rechten.

!!! tip "Tip"

    Zet het wachtwoord tussen enkele aanhalingstekens. `bash` en `zsh` behandelen tekens zoals `!`, `$` en `*` speciaal; een niet-geciteerd wachtwoord met deze tekens wordt mogelijk niet correct doorgegeven.

!!! tip "Best Practice"

    Gebruik een sterk wachtwoord met een mix van hoofdletters, kleine letters, cijfers en speciale tekens.

---

## Dashboardconfiguratie {: #dashboard-configuration }

### Stap 1: Zet het dashboard uit op de webserver

Het digna-dashboard heeft een eigen `config.toml`-bestand in de `dashboard/`-map. Deze configuratie wordt al geleverd en vereist geen wijzigingen tijdens de initiële installatie. U hoeft het alleen te configureren als u de backend-verbinding wilt aanpassen.

Als u de dashboardconfiguratie moet wijzigen (bijv. voor multi-instance-implementaties), raadpleeg dan de documentatie van het dashboard.

Kies uw webserver en volg de bijbehorende deployment-stappen.

#### Deployen naar nginx

Als u de [nginx Setup](#nginx-setup) heeft gevolgd, wijst het serverblok al naar uw `dashboard`-map en is er geen kopiëren nodig.

1. **Bevestig het pad**
   - Open `/etc/nginx/conf.d/digna.conf`
   - Controleer of `root` naar uw uitgepakte `dashboard`-map wijst

2. **Zorg dat de map leesbaar is**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Herlaad nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Test de installatie**
   - Open uw browser
   - Navigeer naar `http://localhost` (of uw geconfigureerde URL)
   - U zou de inlogpagina van het digna-dashboard moeten zien

#### Deployen naar Apache httpd

1. **Kopieer het dashboard naar de documentroot**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Voeg de rewrite-regels toe**

   Maak een `.htaccess`-bestand in de gedeployde map zodat dashboard-routes een browserrefresh overleven:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Toegang tot het dashboard**
   - Open uw browser
   - Navigeer naar `http://localhost/digna`
   - U zou de inlogpagina van het digna-dashboard moeten zien

### Stap 2: SELinux (alleen RHEL-familie)

Op RHEL, Rocky, AlmaLinux en Fedora staat SELinux standaard in enforcing en zal de webserver blokkeren om bestanden buiten de verwachte locaties te lezen. Controleer of het actief is:

```bash
getenforce
```

Als het resultaat `Enforcing` is en u serveert het dashboard vanaf `/opt/digna/dashboard`, label dan de map zodat de webserver deze kan lezen:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Opmerking"

    Als `semanage` niet gevonden wordt, installeer het dan met `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Belangrijk"

    Een dashboard dat **403 Forbidden** retourneert op een vers geconfigureerde RHEL-server is vrijwel altijd een SELinux-labellingprobleem in plaats van een bestandspermissieprobleem. Controleer met `sudo ausearch -m avc -ts recent`.

---

## digna als systemd-service draaien {: #running-digna-as-a-systemd-service }

### Waarom digna als service draaien?

Het draaien van de digna-backend als systemd-service zorgt ervoor dat deze:

- Automatisch start bij het opstarten van de machine
- Op de achtergrond draait zonder een geopend terminalvenster
- Automatisch opnieuw start als het crasht
- Beheerd kan worden via `systemctl`, de standaard Linux-servicemanager

### Servicebeheerbestanden

Alle benodigde bestanden bevinden zich in de digna-installatiemap onder: `bin/`

De volgende shellscripts zijn beschikbaar:

- `install_service.sh` — Registreert digna bij systemd
- `uninstall_service.sh` — Deregistreert de service
- `start_service.sh` — Start de geregistreerde service
- `stop_service.sh` — Stopt de draaiende service

!!! warning "Rootrechten vereist"

    Alle scripts moeten met `sudo` worden uitgevoerd, omdat het registreren van een service die bij het opstarten start een unit-file naar `/etc/systemd/system` schrijft.

### Maak de scripts uitvoerbaar

Bij extractie kan het uitvoerbit verloren zijn gegaan. Voor eerste gebruik:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### De service installeren

1. **Open een terminal**

2. **Navigeer naar de bin-map**
   ```bash
   cd /opt/digna/bin
   ```

3. **Voer het installatiescript uit**
   ```bash
   sudo ./install_service.sh
   ```

De digna-server is nu geregistreerd bij systemd met **automatisch opstarten** ingeschakeld. De service start niet onmiddellijk — zie de volgende sectie om deze te starten.

### De service starten en stoppen

#### Om de service te starten

1. Open een terminal
2. Navigeer naar `/opt/digna/bin`
3. Voer uit:
   ```bash
   sudo ./start_service.sh
   ```

#### Om de service te stoppen

1. Open een terminal
2. Navigeer naar `/opt/digna/bin`
3. Voer uit:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tip"

    Stop de service altijd voordat u applicatiebestanden bijwerkt.

### Beheren van de service met systemctl

Zodra geregistreerd, kan de service ook gecontroleerd worden met de standaard systemd-commando's vanuit elke map:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Verifiëren van de service

Om te bevestigen dat de service geregistreerd is en draait:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` betekent dat de service bij het opstarten start; `active` betekent dat deze nu draait.

### Bekijk de servicelogboeken

systemd captureert alles wat de backend naar de console schrijft. Om het te lezen:

```bash
sudo journalctl -u digna -n 100
```

Om de log realtime te volgen terwijl u een probleem reproduceert:

```bash
sudo journalctl -u digna -f
```

!!! tip "Tip"

    Dit is de snelste manier om een service te diagnosticeren die start en onmiddellijk weer stopt. Een repository-verbindingfout of een ontbrekend `license.toml` wordt hier gerapporteerd.

### De service naar een nieuwe map verplaatsen

De unit-file slaat het absolute pad naar het uitvoerbare bestand op, dus het verplaatsen van de installatie vereist het opnieuw registreren van de service:

1. **Verwijder de huidige service**
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

2. **Verwijder de service**
   ```bash
   sudo ./uninstall_service.sh
   ```

De digna-server is nu van systemd losgekoppeld.

---

## Upgraden naar een nieuwe release {: #upgrading-to-a-new-release }

### Voordat u gaat upgraden

**Het aanmaken van een backup van de digna-repository is verplicht**

Maak vóór het upgraden een backup van uw repository (PostgreSQL) om gegevensverlies te voorkomen.
Een backup zorgt ervoor dat u kunt herstellen als de upgrade onverwachte problemen veroorzaakt.

Om een backup vanaf de shell te maken:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgradeproces

#### Stap 1: Stop de digna-service

Als digna als systemd-service draait, stop deze dan eerst:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Als digna in de voorgrond draait, druk dan op `Ctrl + C` in het terminalvenster.

#### Stap 2: Backup van de huidige backend-installatie

In uw digna-installatiemap:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Stap 3: Pak de nieuwe versie uit en deploy

1. Pak het nieuwe digna-installatie-ZIP-bestand uit
2. Kopieer het nieuwe `digna`-uitvoerbare bestand en de `dashboard`-map naar uw installatiemap
3. Herstel het uitvoerbit en de eigendom voor het serviceaccount:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Belangrijk"

    Het `config.toml`-bestand wordt **nooit** in het installatie-ZIP opgenomen. Uw bestaande configuratie blijft onaangeroerd.

### Stap 4: Herstel uw configuratiebestanden

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Stap 5: Upgrade het repository-schema

Navigeer naar uw digna-installatiemap en voer uit:

```bash
cd /opt/digna
./digna repo upgrade
```

Dit werkt het PostgreSQL-schema bij naar de nieuwste versie terwijl alle bestaande gegevens behouden blijven.

### Stap 6: Herstart services

Als u als systemd-service draait:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Als u handmatig draait, start de server opnieuw:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Als u nginx of Apache gebruikt, herlaad dan de betreffende webserver:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Op de RHEL-familie, breng de SELinux-labels opnieuw aan als de `dashboard`-map is vervangen:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Stap 7: Verifieer de upgrade

1. Ga naar het digna-dashboard
2. Controleer of de interface correct laadt
3. Controleer de serverlogs op eventuele fouten:

```bash
sudo journalctl -u digna -n 100
```