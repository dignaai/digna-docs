# macOS-installationsguide för digna Release 2026.06

**Release:** 2026.06

**Senast uppdaterad:** 5 september 2026


---

## Innehållsförteckning

1. [Introduktion](#introduction)
2. [Systemkrav](#system-requirements)
3. [Förberedelser före installation](#pre-installation-setup)
4. [Förbered PostgreSQL-servern](#postgresql-server-setup)
5. [Webbserverkonfiguration](#web-server-configuration)
6. [Initial installation](#initial-installation)
7. [Backend-konfiguration](#backend-configuration)
8. [Dashboard-konfiguration](#dashboard-configuration)
9. [Köra digna som bakgrundstjänst](#running-digna-as-a-background-service)
10. [Uppgradera till en ny release](#upgrading-to-a-new-release)

---

## Introduktion {: #introduction }

### Om digna

digna är en omfattande AI-driven plattform utformad för att optimera datakvalitetshantering i olika data-miljöer såsom datalager, datasjöar och lakehouses. Byggd för hög skalbarhet och anpassningsförmåga, digna hanterar moderna datautmaningar genom automatisering, realtidsövervakning och avvikelsedetektion.

digna består av två huvudkomponenter:

- **dignabackend**: Applikationens kärnmotor, ansvarig för databehandling och kvalitetskontroller.
- **dignadashboard**: Ett webbaserat gränssnitt som körs på en webbserver och ger ett användarvänligt sätt att interagera med digna-plattformen och visualisera datakvalitetsmått.

### Nytt i Release 2026.06

Den här releasen för in data-observability-möjligheter direkt i din kod, vilket gör det möjligt för utvecklare att övervaka datakvalitet vid källan. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) för fullständiga detaljer.

### Letar du efter Windows eller Linux?

Denna guide täcker macOS. För andra plattformar, se [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) eller [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemkrav {: #system-requirements }

Innan du påbörjar installationen, se till att ditt system uppfyller följande minimikrav:

| Krav | Specifikation |
|---|---|
| **Operativsystem** | macOS 13 (Ventura) eller senare |
| **Arkitektur** | Apple Silicon (arm64) eller Intel (x86_64) |
| **Minne (minimalkonfiguration)** | 16 GB RAM |
| **Diskutrymme** | 10 GB tillgängligt lagringsutrymme |
| **Databas** | PostgreSQL Server 12 eller senare |
| **Webbserver** | nginx, Apache httpd eller motsvarande |
| **Kommandoradsverktyg** | Xcode Command Line Tools (krävs av Homebrew) |

### Alternativ för databasinstallation

**Om PostgreSQL redan är installerat:**
Du kan lägga till en ny databas för digna i din befintliga PostgreSQL-server.

**Om du installerar PostgreSQL på samma maskin som digna:**

!!! info "Rekommenderade specifikationer"

    - **Minne**: 32 GB RAM (istället för 16 GB)
    - **Diskutrymme**: 50 GB tillgängligt lagringsutrymme (istället för 10 GB)

    Dessa högre specifikationer rymmer både digna och PostgreSQL-databasen som körs samtidigt.

### Kontrollera din arkitektur

Flera sökvägar i denna guide skiljer sig mellan Apple Silicon och Intel-Mac. För att kontrollera vilken arkitektur du har, öppna **Terminal** och kör:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew installeras till `/opt/homebrew`.
- `x86_64` — Intel. Homebrew installeras till `/usr/local`.

!!! tip "Tips"

    Istället för att hårdkoda någon av sökvägarna använder denna guide `$(brew --prefix)`, vilket expanderar till rätt plats på båda arkitekturer. Du kan kopiera kommandona rakt av.

---

## Förberedelser före installation {: #pre-installation-setup }

Innan du installerar digna, säkerställ att tre nyckelförutsättningar är på plats:

1. **Homebrew** – paketchefen som används för att installera komponenterna nedan
2. **PostgreSQL Server** – för att lagra beräknade mått och prestandadata
3. **Webbserver** – för att hosta digna Dashboard

Om dessa komponenter inte redan är uppsatta, följ avsnitten nedan för att installera och konfigurera dem.

### Installera Homebrew

Homebrew är standardpakethanteraren för macOS och används i hela denna guide för att installera PostgreSQL och nginx.

#### Steg 1: Kontrollera om Homebrew redan är installerat

Öppna **Terminal** (tryck `Cmd + Space`, skriv `Terminal`, tryck Enter) och kör:

```bash
brew --version
```

Om ett versionsnummer returneras, hoppa till avsnittet [Förbered PostgreSQL-servern](#postgresql-server-setup).

#### Steg 2: Installera Homebrew

Om kommandot inte hittades, installera Homebrew genom att följa instruktionerna på [officiella Homebrew-sajten](https://brew.sh). Installationsprogrammet installerar även Xcode Command Line Tools om de inte redan finns.

#### Steg 3: Lägg till Homebrew i din PATH

På Apple Silicon skriver installatören ut två kommandon för att lägga till Homebrew i din shell-miljö. Kör dem enligt instruktionerna och bekräfta sedan:

```bash
brew --prefix
```

Detta bör skriva ut `/opt/homebrew` på Apple Silicon eller `/usr/local` på Intel.

---

## Förbered PostgreSQL-servern {: #postgresql-server-setup }

### Om du redan har PostgreSQL

Om PostgreSQL redan är installerat och körs lokalt eller om du använder en hanterad fjärr-PostgreSQL-server kan du hoppa till [nästa avsnitt](#web-server-configuration).

### Installationsalternativ

macOS erbjuder två enkla sätt att installera PostgreSQL. Välj **ett**:

- [Homebrew](#postgresql-homebrew) — kommandoradsinstallation, rekommenderas för serverdistributioner
- [Postgres.app](#postgresql-app) — grafisk installation, bekvämt för lokal utvärdering

### Installera PostgreSQL med Homebrew {: #postgresql-homebrew }

#### Steg 1: Installera PostgreSQL-formeln

```bash
brew install postgresql@16
```

#### Steg 2: Lägg till PostgreSQL i din PATH

Versionerade PostgreSQL-formler är *keg-only*, vilket innebär att Homebrew inte länkar deras kommandon till din PATH automatiskt. Lägg till dem själv:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Notera"

    Detta förutsätter standard-shellet `zsh` som används av macOS. Om du använder `bash`, lägg till samma rad i `~/.bash_profile` istället.

#### Steg 3: Starta PostgreSQL-tjänsten

```bash
brew services start postgresql@16
```

Detta startar PostgreSQL omedelbart och konfigurerar det för att starta automatiskt när du loggar in.

#### Steg 4: Verifiera installationen

```bash
psql --version
```

Du bör se PostgreSQL-versionen om installationen lyckades.

#### Steg 5: Anslut till servern

```bash
psql postgres
```

!!! warning "Varning — macOS skiljer sig från Windows här"

    Windows-installationsprogrammet uppmanar dig att skapa en `postgres`-superuser och lösenord. Homebrew gör inte det. Istället skapas en superuser med namnet efter ditt **macOS-konto**, utan lösenord, åtkomlig endast från den lokala maskinen.

    Detta innebär att det inte finns någon `postgres`-roll på en färsk Homebrew-installation. Använd ditt eget kontonamn när du behöver en superuser, och skapa en uttrycklig digna-användare enligt beskrivningen i [Initial installation](#initial-installation).

#### Steg 6: Bekräfta porten

Standardporten för PostgreSQL är `5432`. För att bekräfta vilken port din server lyssnar på:

```bash
psql postgres -c "SHOW port;"
```

Notera värdet — du kommer att behöva det när du konfigurerar digna-backend.

### Installera PostgreSQL med Postgres.app {: #postgresql-app }

Om du föredrar en grafisk installation:

1. Ladda ner [Postgres.app](https://postgresapp.com) och dra den till din **Applications**-mapp
2. Öppna appen och klicka **Initialize** för att skapa en ny server
3. Följ appens instruktioner för att lägga till dess kommandoradsverktyg i din PATH
4. Verifiera installationen:

```bash
psql --version
```

Postgres.app skapar också en superuser med namnet efter ditt macOS-konto.

---

## Webbserverkonfiguration {: #web-server-configuration }

digna kräver en webbserver för att hosta dashboarden. Välj ett av följande alternativ:

- [nginx](#nginx-setup) — installerat via Homebrew, rekommenderas
- [Apache httpd](#apache-setup) — inkluderat i macOS

Du behöver bara installera och konfigurera **en** av dessa servrar.

Båda avsnitten konfigurerar två saker som dashboarden är beroende av:

- **Fallback för single-page application**, så att uppdatering av en dashboard-URL inte ger 404
- **En `.md` MIME-typ**, så att Markdown-filer serveras korrekt

### nginx-inställning {: #nginx-setup }

#### Översikt

nginx är en lättviktig, högpresterande webbserver väl lämpad för att servera den statiska digna-dashboarden.

#### Installation

```bash
brew install nginx
```

#### Starta nginx

```bash
brew services start nginx
```

#### Verifiera installationen

1. Öppna din webbläsare
2. Navigera till `http://localhost:8080`
3. Du bör se nginx välkomstsida

!!! note "Notera — standardport är 8080, inte 80"

    Homebrew konfigurerar nginx att lyssna på port `8080` så att det kan köras utan administratörsbehörighet. På macOS krävs root för att binda till port `80` eller någon annan port under 1024.

    För att servera dashboarden på port 80, ändra `listen 8080;` till `listen 80;` i konfigurationen nedan och starta nginx med `sudo brew services start nginx` istället.

#### Konfigurera en site för dashboarden

Homebrews nginx-konfiguration inkluderar alla filer i dess `servers`-katalog. Skapa en dedikerad konfigurationsfil för digna där:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Klistra in följande och ersätt `/path/to/digna/dashboard` med den faktiska sökvägen till din extraherade `dashboard`-mapp:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Servera Markdown-filer med korrekt MIME-typ.
    types {
        text/markdown  md;
    }

    # Fallback för single-page-application: okända sökvägar returnerar index.html
    # istället för en 404, så dashboard-rutter överlever en webbläsaruppdatering.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Varning"

    Utan `try_files`-direktivet kommer omladdning av någon dashboard-sida utöver rot-URL:en att ge en 404. Detta är nginx-ekvivalenten till URL Rewrite-modulen som krävs av IIS på Windows.

#### Tillämpa konfigurationen

Testa syntaxen i konfigurationen och ladda om nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd-inställning {: #apache-setup }

#### Översikt

macOS inkluderar Apache httpd, så ingen installation krävs. Den är som standard inaktiverad.

#### Starta Apache

```bash
sudo apachectl start
```

#### Verifiera installationen

1. Öppna din webbläsare
2. Navigera till `http://localhost`
3. Du bör se meddelandet "It works!"

#### Obligatoriskt: Aktivera mod_rewrite

Dashboarden kräver URL-omskrivning. Öppna Apache-konfigurationen:

```bash
sudo nano /etc/apache2/httpd.conf
```

Hitta följande rad och ta bort inledande `#` för att avkommentera den:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obligatoriskt: Tillåt .htaccess-överriding

I samma fil, lokalisera `<Directory "/Library/WebServer/Documents">`-blocket och ändra:

```apache
AllowOverride None
```

till:

```apache
AllowOverride All
```

#### Obligatoriskt: MIME-typ för Markdown-filer

Fortfarande i `httpd.conf`, lägg till följande rad så att Markdown-filer serveras korrekt:

```apache
AddType text/markdown .md
```

!!! warning "Varning"

    Utan denna inställning kan `.md`-filer inte serveras korrekt.

#### Tillämpa konfigurationen

Kontrollera konfigurationen för syntaxfel och starta om Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Initial installation {: #initial-installation }

### Steg 1: Skapa digna-repositoriet

digna-repositoriet lagrar alla mått som beräknas av digna. Det fungerar som den centrala databasen för analytiska och prestandadata.

#### Skapa repository-schema och användare

Öppna din PostgreSQL-klient (psql, pgAdmin eller liknande) och kör följande SQL-kommandon:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersätt följande platshållare:**

- `<digna_repo_schema>` — Ditt önskade schemanamn (t.ex. `dignarepo`)
- `<digna_repo_user>` — Ditt önskade användarnamn (t.ex. `digna_user`)
- `<digna_repo_password>` — Ett säkert lösenord för denna användare

**Exempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

För att köra dessa från Terminal i ett steg:

```bash
psql postgres
```

Klistra sedan in kommandona vid `postgres=#` prompten och skriv `\q` för att avsluta.

!!! tip "Bästa praxis"

    Använd starka, komplexa lösenord för databas-användare. Undvik lättgissade uppgifter.

---

### Steg 2: Extrahera digna-installationspaketet

1. Lokalisera digna-installationsfilen (ZIP) som tillhandahållits
2. Extrahera den till önskad installationsplats — till exempel `/opt/digna` eller `~/digna`
3. Efter extraktion bör du se följande objekt:
   - `dashboard/` — Webbgränssnittet
   - `digna` — Huvudkörbar fil (backend + CLI kombinerat)
   - `config.toml` — Konfigurationsfil
   - `license.toml` — Licensfil (kopiera din här)

För att extrahera från Terminal:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Gör den körbara filen körbar

Beroende på hur arkivet överfördes kan exekveringsbiten ha försvunnit vid extraktion. Sätt den explicit:

```bash
cd /opt/digna
chmod +x digna
```

#### Om macOS blockerar applikationen

Filer som laddats ner via webbläsare eller e-postklienter taggas med ett karantänattribut. Om macOS rapporterar att appen *"cannot be opened because the developer cannot be verified"*, ta bort attributet från installationskatalogen:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativt, öppna **System Settings → Privacy & Security**, hitta det blockerade objektet nära botten av sidan och klicka **Open Anyway**.

!!! note "Notera"

    Detta steg behövs endast om macOS faktiskt blockerar den körbara filen. Paket som överförts över SSH eller från interna filresurser är vanligtvis inte karantänmärka.

### Steg 3: Installera licensfilen

!!! warning "Varning"

    Licensfilen ingår **inte** i installationspaketet och kommer att tillhandahållas separat av digna.

1. Lokalisera `license.toml`-filen som tillhandahållits
2. Kopiera den till rotkatalogen för digna-installationen (där `config.toml` och den körbara `digna` finns)

**Varför detta är viktigt:**
Licensfilen innehåller din kundinformation, licensens utgångsdatum och digital signatur. **Ändra inte denna fil** — alla ändringar gör den ogiltig.

**Katalogstruktur efter installation:**

```
/opt/digna/
├── config.toml         (konfigurationsfil)
├── license.toml        (DIN LICENSFIL - kopiera hit)
├── digna               (huvudkörbar fil)
├── bin/                (skript för tjänstehantering)
└── dashboard/          (webbgränssnitt)
    └── (dashboard-filer)
```

---

## Backend-konfiguration {: #backend-configuration }

### Steg 1: Skapa och redigera konfigurationsfilen

Filen `config_template.toml` medföljer din digna-installation. Du behöver bara byta namn till `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Plats:** `/opt/digna/config.toml`

Öppna `config.toml` i en textredigerare och konfigurera varje avsnitt nedan.

#### [app] Avsnittet

Detta avsnitt konfigurerar digna-backendens applikationsinställningar:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_APP_HOST` | `localhost` eller IP-adress | Värdnamn eller IP där dignabackend körs |
| `digna_APP_PORT` | `8082` (standard) | Port för REST API-endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Om dashboarden ligger på annan server, inkludera dess URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krävs för CORS med referenser |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillåt alla HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillåt alla headers |

!!! note "Notera"

    Om du serverar dashboarden från Homebrews nginx på dess standardport, är origin som ska tillåtas `http://localhost:8080`.

#### [repo] Avsnittet

Detta avsnitt konfigurerar anslutningen till PostgreSQL-databasen:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns värdnamn/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasnamn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema som skapades tidigare |
| `digna_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-uppsättningen |
| `digna_REPO_PASSWORD` | Ditt lösenord | Lösenord satt vid schema-skapandet |

#### [base] Avsnittet

Detta avsnitt innehåller säkerhets- och cookie-inställningar:

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

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_FERNET_KEY` | Krypteringsnyckel | Används för att kryptera tokens och cookies (standard medföljer) |
| `digna_COOKIE_DOMAIN` | `localhost` | Matcha din frontend-domän |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Använd `true` för HTTPS-anslutningar |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktiverat för säkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Förhindrar CSRF-attacker |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Sessionsutgång i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal parallella inspektionsjobb |

!!! tip "Tips"

    För att hitta antalet CPU-kärnor på din Mac, kör `sysctl -n hw.ncpu`.

#### [logging] Avsnittet

Detta avsnitt konfigurerar logghantering:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal dagliga loggbackup som ska behållas |

---

### Steg 2: Initiera repositoriet

1. Öppna **Terminal**
2. Navigera till din digna-installationskatalog (där `config.toml` och `digna`-körbara finns)
3. Kör anslutningstestet:

```bash
cd /opt/digna
./digna repo check
```

Du bör se en bekräftelse på att anslutningen är etablerad (själva repositoriet har ännu inte initialiserats).

!!! note "Notera"

    På macOS finns inte kommandon i den aktuella katalogen på din PATH, så den körbara anropas som `./digna` istället för `digna`. För att använda kortformen överallt, lägg till installationskatalogen i din PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Steg 3: Installera repository-schemat

I samma katalog, kör:

```bash
./digna repo install
```

Detta kommando installerar nödvändiga tabeller och schema i din PostgreSQL-databas.

### Steg 4: Starta digna-servern

I digna-installationskatalogen, starta servern med:

```bash
./digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns värdnamn/IP
- `--port` — Serverns port

Du bör se startmeddelanden som bekräftar att servern körs:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Tips"

    Första gången du startar servern kan macOS fråga om du vill tillåta att applikationen accepterar inkommande nätverksanslutningar. Klicka **Allow**, annars kommer inte dashboarden att kunna nå backend.

### Steg 5: Skapa en administratörsanvändare

1. Öppna ett **nytt** Terminalfönster
2. Navigera till din digna-installationskatalog
3. Kör följande kommando för att skapa en admin-användare:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Exempel:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Detta skapar en användare med användarnamnet `admin` och fullständiga administratörsrättigheter.

!!! tip "Tips"

    Omge lösenordet med enkla citattecken. `zsh` behandlar tecken som `!`, `$` och `*` särskilt, och ett oavgränsat lösenord som innehåller dem skickas inte som avsett.

!!! tip "Bästa praxis"

    Använd ett starkt lösenord med en blandning av versaler, gemener, siffror och specialtecken.

---

## Dashboard-konfiguration {: #dashboard-configuration }

### Steg 1: Distribuera dashboarden till webbservern

Digna-dashboarden har sin egen separata `config.toml`-fil i `dashboard/`-katalogen. Denna konfiguration medföljer och kräver normalt inga ändringar under initial installation. Du behöver endast konfigurera den om du vill anpassa backend-anslutningen.

Om du behöver ändra dashboard-konfigurationen (t.ex. vid multi-instans-distributioner), hänvisa till dashboardens dokumentation.

Välj din webbserver och följ motsvarande distribution steg.

#### Distribuera till nginx

Om du följde avsnittet [nginx-inställning](#nginx-setup), pekar serverblocket redan mot din `dashboard`-mapp och ingen kopiering krävs.

1. **Bekräfta sökvägen**
   - Öppna `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Verifiera att `root` pekar på din extraherade `dashboard`-mapp

2. **Se till att mappen är läsbar**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Ladda om nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Testa installationen**
   - Öppna din webbläsare
   - Navigera till `http://localhost:8080` (eller din konfigurerade URL)
   - Du bör se digna dashboard-inloggningssidan

#### Distribuera till Apache httpd

1. **Kopiera dashboarden till dokumentroten**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Lägg till omskrivningsregler**

   Skapa en `.htaccess`-fil inne i den deployade mappen så att dashboard-rutter överlever en webbläsaruppdatering:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Klistra in följande:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Servera befintliga filer och kataloger som de är.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Allt annat faller tillbaka till single-page-application-entrén.
   RewriteRule ^ index.html [L]
   ```

3. **Starta om Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Nå dashboarden**
   - Öppna din webbläsare
   - Navigera till `http://localhost/digna`
   - Du bör se digna dashboard-inloggningssidan

---

## Köra digna som bakgrundstjänst {: #running-digna-as-a-background-service }

### Varför köra digna som tjänst?

Att köra digna-backenden som en bakgrundstjänst säkerställer att den:

- Startar automatiskt när maskinen bootar
- Körs i bakgrunden utan öppet Terminal-fönster
- Startas om automatiskt om den kraschar
- Kan hanteras via `launchctl`, macOS servicehanterare

### Filer för tjänstehantering

Alla nödvändiga filer finns i digna-installationskatalogen under: `bin/`

Följande shell-skript finns:

- `install_service.sh` — registrerar digna med launchd
- `uninstall_service.sh` — avregistrerar tjänsten
- `start_service.sh` — startar den registrerade tjänsten
- `stop_service.sh` — stoppar den körande tjänsten

!!! warning "Administratör krävs"

    Alla skript måste köras med `sudo`, eftersom registrering av en tjänst som startar vid boot skriver till `/Library/LaunchDaemons`.

### Gör skripten körbara

Extraktion kanske inte bevarar exekveringsbiten. Innan första användning:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installera tjänsten

1. **Öppna Terminal**

2. **Navigera till bin-mappen**
   ```bash
   cd /opt/digna/bin
   ```

3. **Kör installationsskriptet**
   ```bash
   sudo ./install_service.sh
   ```

Digna-servern är nu registrerad i launchd med **automatisk uppstart** aktiverad. Tjänsten startar inte omedelbart — se nästa avsnitt för att starta den.

### Starta och stoppa tjänsten

#### För att starta tjänsten

1. Öppna Terminal
2. Navigera till `/opt/digna/bin`
3. Kör:
   ```bash
   sudo ./start_service.sh
   ```

#### För att stoppa tjänsten

1. Öppna Terminal
2. Navigera till `/opt/digna/bin`
3. Kör:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Tips"

    Stoppa alltid tjänsten innan du uppdaterar applikationsfiler.

### Verifiera tjänsten

För att bekräfta att tjänsten är registrerad och körs:

```bash
sudo launchctl list | grep digna
```

En rad som börjar med ett process-ID indikerar att tjänsten körs. Ett `-` i första kolumnen betyder att den är registrerad men stoppad.

### Flytta tjänsten till en ny katalog

launchd lagrar den absoluta sökvägen till den körbara filen, så att flytta installationen kräver omregistrering av tjänsten:

1. **Avinstallera nuvarande tjänst**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Flytta applikationsfilerna**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Installera tjänsten på nytt**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Starta tjänsten**
   ```bash
   sudo ./start_service.sh
   ```

### Avinstallera tjänsten

1. **Stoppa den körande tjänsten**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Avinstallera tjänsten**
   ```bash
   sudo ./uninstall_service.sh
   ```

Digna-servern är nu avregistrerad från launchd.

---

## Uppgradera till en ny release {: #upgrading-to-a-new-release }

### Innan du uppgraderar

**Att skapa en backup av digna-repositoriet är obligatoriskt**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

För att skapa en backup från Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Uppgraderingsprocess

#### Steg 1: Stoppa digna-tjänsten

Om digna körs som bakgrundstjänst, stoppa den först:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Om digna körs i förgrunden, tryck `Ctrl + C` i dess Terminal-fönster.

#### Steg 2: Säkerhetskopiera nuvarande backend-installation

I din digna-installationskatalog:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Steg 3: Extrahera och distribuera ny version

1. Extrahera den nya digna-installations-ZIP-filen
2. Kopiera den nya `digna`-körbara och `dashboard`-mappen till din installationskatalog
3. Återställ exekveringsbiten och, om nödvändigt, ta bort karantänattributet:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Varning"

    Filen `config.toml` ingår **aldrig** i installations-ZIP:en. Din befintliga konfiguration förblir säker.

### Steg 4: Återställ dina konfigurationsfiler

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Steg 5: Uppgradera repository-schemat

Navigera till din digna-installationskatalog och kör:

```bash
cd /opt/digna
./digna repo upgrade
```

Detta uppdaterar PostgreSQL-schemat till senaste versionen samtidigt som all befintlig data bevaras.

### Steg 6: Starta om tjänsterna

Om du kör som bakgrundstjänst:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Om du kör manuellt, starta servern igen:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Om du använder nginx eller Apache, starta om respektive webbserver:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Steg 7: Verifiera uppgraderingen

1. Gå till digna-dashboarden
2. Verifiera att gränssnittet laddar korrekt
3. Kontrollera serverloggarna efter eventuella fel