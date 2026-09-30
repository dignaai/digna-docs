---
title: macOS-installatiehandleiding – digna Release 2026.06 | digna Documentatie
description: Stapsgewijze handleiding voor het installeren van digna Release 2026.06 op macOS — systeemvereisten, Homebrew- en PostgreSQL-configuratie, nginx- of Apache-configuratie, backend- en dashboardconfiguratie, digna als achtergrondservice uitvoeren en upgraden naar een nieuwe release.
keywords: digna macos installatie, digna mac implementatiehandleiding, digna backend configuratie, digna dashboard installatie, postgresql homebrew, nginx macos, digna launchd service, digna upgrade handleiding
image: /assets/logo_square.png
---

# macOS-installatiehandleiding voor digna Release 2026.06

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
9. [digna als achtergrondservice draaien](#running-digna-as-a-background-service)
10. [Upgraden naar een nieuwe release](#upgrading-to-a-new-release)

---

## Introductie {: #introduction }

### Over digna

digna is een uitgebreid AI-gestuurd platform dat is ontworpen om het beheer van datakwaliteit te optimaliseren in uiteenlopende dataomgevingen zoals warehouses, lakes en lakehouses. Het is gebouwd om zeer schaalbaar en aanpasbaar te zijn en pakt moderne data-uitdagingen aan via automatisering, realtime monitoring en anomaliedetectie.

digna bestaat uit twee hoofdcomponenten:

- **digna**: de kern van de applicatie, verantwoordelijk voor het verwerken van gegevens en het uitvoeren van kwaliteitscontroles. Het combineert de backend en de opdrachtregelinterface in één uitvoerbaar bestand en vervangt daarmee de losse programma's `dignabackend` en `dignacli` uit eerdere releases.
- **dignadashboard**: Een webgebaseerde interface gehost op een webserver, die een gebruiksvriendelijke manier biedt om met het digna-platform te werken en datakwaliteitsstatistieken te visualiseren.

### Wat is nieuw in Release 2026.06

Deze release brengt data-observability-mogelijkheden rechtstreeks in uw code, zodat ontwikkelaars datakwaliteit aan de bron kunnen monitoren. Zie de [release notes](http://docs.digna.ai/changelog/Release_202606/) voor volledige details.

### Op zoek naar Windows of Linux?

Deze handleiding behandelt macOS. Voor andere platforms, zie de [Windows-installatiehandleiding](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) of de [Linux-installatiehandleiding](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
unzip digna-2026.06-macos.zip -d /opt/digna
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

Deze sectie configureert de applicatie-instellingen van de digna-backend:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Als het dashboard op een andere server staat, voeg die URL toe |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vereist voor CORS met credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Sta alle HTTP-methoden toe |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Sta alle headers toe |

!!! note "Opmerking"

    Als u het dashboard serveert vanaf de nginx van Homebrew op de standaardpoort, is de origin die u moet toestaan `http://localhost:8080`.

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

#### [base] Sectie

Deze sectie bevat beveiligings- en cookie-instellingen:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Komt overeen met uw frontend-domein |
| `digna_COOKIE_SECURE` | `false` (lokaal) / `true` (productie) | Gebruik `true` voor HTTPS-verbindingen |
| `digna_COOKIE_HTTPONLY` | `true` | Altijd ingeschakeld voor beveiliging |
| `digna_COOKIE_SAME_SITE` | `lax` | Voorkomt CSRF-aanvallen |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 uur) | Sessietimeout in seconden |
| `digna_MAX_WORKERS` | Aantal CPU-cores - 1 | Aantal parallelle inspectietaken |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximale vertraging, in seconden, die de scheduler mag toevoegen voordat een openstaande taak start |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Tijdstip (24-uursnotatie `HH:MM`) waarop de dagelijkse opschoning begint |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Waarde | Opmerkingen |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` of `DEBUG` | `INFO` voor productie, `DEBUG` voor probleemoplossing |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Aantal dagelijkse logbackups om te bewaren |

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

Overall: OK
```

Los alles op wat als FAILED wordt gemeld en voer het commando opnieuw uit voordat u verdergaat. De volledige lijst met opties staat in de [CLI-referentie](../../../cli/Command_Line_Interface_202606.md).

### Stap 3: Initialiseer de repository

1. Open **Terminal**
2. Navigeer naar uw digna-installatiemap (waar `config.toml` en het `digna`-uitvoerbare bestand zich bevinden)
3. Voer de verbindingscontrole uit:

```bash
cd /opt/digna
./digna repo check
```

U zou een bevestiging moeten zien dat de verbinding tot stand is gebracht (de repository zelf is nog niet geïnitialiseerd).

!!! note "Opmerking"

    Op macOS staan commando's in de huidige map niet in uw PATH, dus het uitvoerbare bestand wordt aangeroepen als `./digna` in plaats van `digna`. Om overal de korte vorm te gebruiken, voegt u de installatiemap toe aan uw PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Stap 4: Installeer het repository-schema

Voer in dezelfde map uit:

```bash
./digna repo install
```

Dit commando installeert de benodigde tabellen en het schema in uw PostgreSQL-database.

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

### Voordat u gaat upgraden

**Controleer eerst alle databaseverbindingen**

Vanaf Release 2026.06 benadert digna elke brontechnologie via **ODBC**. Eerdere releases boden de keuze tussen een stuurprogramma per technologie en ODBC, te kiezen met de schakelaar **Use ODBC**. Het digna-team heeft besloten alleen op ODBC te bouwen, omdat één standaardinterface meer biedt dan een verzameling maatwerkstuurprogramma's:

- **Authenticatie** — authenticatie maakt deel uit van ODBC, dus een verbinding kan alles gebruiken wat het stuurprogramma ondersteunt: wachtwoorden, tokens en PAT's, Kerberos en Active Directory, MFA en single sign-on via de browser, cloudidentiteiten, clientcertificaten en TLS. Nieuwe methoden komen met een update van het stuurprogramma, in plaats van te wachten op een digna-release.
- **Stuurprogramma's die door de databaseleveranciers worden onderhouden** — het stuurprogramma van de leverancier volgt nieuwe serverversies en beveiligingsfixes, en u kunt het op uw eigen moment bijwerken, los van digna.
- **Eén manier om alles te configureren** — elke technologie is een lijst met sleutel-waardeparen, met dezelfde interface, dezelfde versleuteling van gevoelige waarden en dezelfde probleemoplossing, in plaats van een andere set velden per bron.
- **Afstemming en bereik** — stuurprogramma-opties zoals time-outs, TLS-instellingen, proxy's en fetch-groottes zijn voor elke bron beschikbaar, en elke technologie met een conform ODBC-stuurprogramma kan worden aangesloten, ook technologieën waarvoor digna geen aparte handleiding publiceert.

In de praktijk betekent dit dat de schakelaar **Use ODBC** en de afzonderlijke velden host, poort, database, gebruiker en wachtwoord niet meer bestaan. **Elke verbinding die nog geen ODBC gebruikt, moet naar ODBC worden omgezet** — er is geen automatische conversie, plan dit dus vóór de upgrade:

1. Loop elke in uw installatie gedefinieerde databaseverbinding na en noteer welke nog geen ODBC gebruiken — elk daarvan moet opnieuw worden geconfigureerd.
2. Installeer het bijbehorende ODBC-stuurprogramma op de digna-host — verbindingen worden geopend vanaf de server waarop de digna-backend draait, niet vanuit de browser. Zie [Het ODBC-stuurprogramma op de digna-host installeren](../../../databases/overview.md#install-the-driver).
3. Zorg dat u de ODBC-eigenschappen van elke betrokken verbinding bij de hand hebt. De [technologiehandleidingen](../../../databases/overview.md#technology-guides) geven per bron een beproefde set eigenschappen.

Zet na de upgrade elke betrokken verbinding om naar ODBC en test ze vanuit het dashboard — zie [Een databaseverbinding maken](../../../databases/overview.md#create-a-database-connection) en [Een verbinding testen](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy-verbindingen"

    De Databricks Legacy-connector is in deze release verwijderd. Migreer die verbindingen naar de [Databricks](../../../databases/databricks_connector_guide.md)-connector.

**Het aanmaken van een backup van de digna-repository is verplicht**

Maak vóór het upgraden een backup van uw repository (PostgreSQL) om gegevensverlies te voorkomen.
Een backup zorgt ervoor dat u kunt herstellen als de upgrade onverwachte problemen veroorzaakt.

Om een backup vanuit de Terminal te maken:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Upgradeproces

#### Stap 1: Stop de digna-service

Als digna als achtergrondservice draait, stop deze dan eerst:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Als digna op de voorgrond draait, druk dan op `Ctrl + C` in het bijbehorende Terminal-venster.

#### Stap 2: Huidige installatie veiligstellen

Hernoem in uw digna-installatiemap de mappen van uw huidige installatie, zodat de nieuwe release ernaast kan worden uitgerold:

```bash
cd /opt/digna
mv dignabackend dignabackend_old
```
```bash
mv dignacli dignacli_old
```
```bash
mv dashboard dashboard_old
```

!!! info "dignabackend en dignacli worden niet meer gebruikt"

    Vanaf Release 2026.06 worden `dignabackend` en `dignacli` vervangen door het enkele uitvoerbare bestand `digna`, dat backend en CLI combineert. Bewaar `dignabackend_old` en `dignacli_old` alleen totdat u de upgrade hebt geverifieerd — daarna kunt u beide mappen verwijderen. Bewaar `dashboard_old` totdat u uw configuratiebestanden eruit hebt teruggezet (zie stap 4).

#### Stap 3: Pak de nieuwe versie uit en deploy

1. Pak het nieuwe digna-installatie-ZIP-bestand uit
2. Kopieer het nieuwe `digna`-uitvoerbare bestand en de `dashboard`-map naar uw installatiemap
3. Herstel het uitvoerbaar-bit en verwijder zo nodig het quarantaine-attribuut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Belangrijk"

    Noch `config.toml` noch `dashboard/dashboard_config.toml` wordt ooit in het
    installatie-ZIP opgenomen — het digna-team levert geen van beide bestanden mee. Uw bestaande
    configuratie blijft bij de upgrade dus onaangeroerd, en de kopieën in de hernoemde
    `*_old`-mappen zijn de enige die u hebt.

#### Stap 4: Herstel uw configuratiebestanden

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Release 2026.06 wijzigt config.toml"

    Drie instellingen zijn nieuw en verplicht, drie worden niet meer gebruikt. Een `config.toml` die uit een eerdere release is overgenomen, bevat de nieuwe instellingen niet, en digna start niet zolang ze ontbreken. Voeg het volgende toe aan uw bestaande `config.toml`:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Voeg de twee `[base]`-sleutels toe aan uw bestaande `[base]`-sectie en voeg `[encryption]` toe als nieuwe sectie. Verwijder daarna de instellingen die niet meer worden gebruikt: **`digna_FERNET_KEY`** uit `[base]`, en **`digna_APP_HOST`** en **`digna_APP_PORT`** uit `[app]` — de server haalt zijn adres en poort nu uit `digna serve`.

    Wat elke instelling doet, staat in [Backendconfiguratie](#backend-configuration).

!!! warning "Eenmalige aanmelding: de indeling van [oidc_clients] is gewijzigd"

    Release 2026.06 vervangt de array van tabellen door één tabel per provider, genoemd naar de providersleutel. `DIGNA_OIDC_KEY` verdwijnt — de sleutel maakt nu deel uit van de sectiekop.

    Voor:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Na:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Herhaal de sectie voor elke provider en houd elke sleutel gelijk aan de `key` in `dashboard_config.toml`. `digna config check` meldt `oidc_clients` als FAILED zolang de oude vorm nog aanwezig is. Alleen installaties die eenmalige aanmelding gebruiken zijn betroffen.

#### Stap 5: Herlaad de webserver

Het dashboard bestaat uit statische bestanden, dus uw webserver — en de browser — kan nog
steeds de vorige versie serveren. Herlaad of herstart de webserver die de `dashboard`-map
host, en herlaad de pagina daarna met een harde vernieuwing (++cmd+shift+r++).

#### Stap 6: Configuratie valideren

Controleer of de bijgewerkte `config.toml` volledig is voordat u de repository aanraakt:

```bash
./digna config check
```

Elke sectie moet OK melden. Los alles op wat als FAILED wordt gemeld en voer het commando opnieuw uit voordat u verdergaat.

#### Stap 7: Vervang het licentiebestand

Elke release krijgt een eigen licentie. Kopieer het `license.toml` dat het digna-team voor
deze release heeft geleverd naar de installatiemap, ter vervanging van het oude:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Behoud de vorige licentie niet"

    Een `license.toml` die voor een eerdere release is uitgegeven, dekt deze release niet, en elk
    commando dat de licentie controleert — `user`, `inspection`, `repo` — breekt af voordat het
    de repository aanraakt wanneer de controle mislukt. Controleer de licentie voordat u verdergaat:

    ```bash
    ./digna license check
    ```

#### Stap 8: Upgrade het repository-schema

Navigeer naar uw digna-installatiemap en voer uit:

```bash
cd /opt/digna
./digna repo upgrade
```

Dit werkt het PostgreSQL-schema bij naar de nieuwste versie terwijl alle bestaande gegevens behouden blijven.

#### Stap 9: Herstart services

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

#### Stap 10: Verifieer de upgrade

1. Open het digna-dashboard
2. Controleer of de interface correct laadt
3. Controleer de serverlogs op eventuele fouten
4. Zet elke verbinding die nog geen ODBC gebruikte om naar ODBC en test daarna alle verbindingen
   — zie [Een verbinding testen](../../../databases/overview.md#testing-a-connection)
