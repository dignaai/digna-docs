# macOS-installationsguide för digna Release 2026.11

**Release:** 2026.11

**Senast uppdaterad:** 7 november 2026


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

- **digna**: applikationens kärna, ansvarig för att bearbeta data och utföra kvalitetskontroller. Den förenar backend och kommandoradsgränssnittet i en enda körbar fil och ersätter därmed de separata programmen `dignabackend` och `dignacli` från tidigare releaser.
- **dignadashboard**: Ett webbaserat gränssnitt som körs på en webbserver och ger ett användarvänligt sätt att interagera med digna-plattformen och visualisera datakvalitetsmått.

### Nytt i Release 2026.11

Denna release lägger till digna Data Reconciliation, digna Agentic med digna MCP Server samt digna Engine, som kan profilera data inuti digna och kontrollera referentiell integritet mellan olika databastekniker. Se [versionsanteckningarna](../../../changelog/Release_202611.md) för fullständiga detaljer.

För en installation medför releasen en ny mekanism för repositorymigreringar, en valfri `[duckdb]`-sektion i `config.toml` för digna Engine och en ny licensfil. [Uppgraderingsavsnittet](#upgrading-to-a-new-release) går igenom var och en av dem.

### Letar du efter Windows eller Linux?

Denna guide täcker macOS. För andra plattformar, se [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) eller [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Databasanslutningar som använder digna Engine som profileringsplats profileras på själva
    digna-värden. Planera för extra minne och diskutrymme för dem, se
    [\[duckdb\]-sektionen](#duckdb-section).

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

!!! info "Konfigurations- och licensfilerna ingår inte i paketet"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` medföljer installationen — du
    skapar båda själv, i [Backendkonfiguration](#backend-configuration) och
    [Dashboardkonfiguration](#dashboard-configuration). Inte heller `license.toml` medföljer;
    digna levererar den separat, enligt beskrivningen i steg 3.

För att extrahera från Terminal:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
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

Detta avsnitt konfigurerar cross-origin resource sharing (CORS) mellan dashboarden och backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard-URL:er | De URL:er som dashboarden serveras från. Webbläsarförfrågningar från alla andra origins avvisas |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krävs, så att webbläsaren skickar sessionscookien med varje förfrågan |

!!! note "Notera"

    Om du serverar dashboarden från Homebrews nginx på dess standardport, är origin som ska tillåtas `http://localhost:8080`.

!!! info "Sektionen [app] är valfri"

    Från Release 2026.11 kan båda nycklarna, och hela sektionen `[app]`, utelämnas. Det är rätt
    uppsättning när en omvänd proxy serverar dashboarden och backend under samma origin: webbläsaren
    gör då inga cross-origin-förfrågningar, och inga tillåts som standard.

#### [repo] Avsnittet

Detta avsnitt konfigurerar anslutningen till PostgreSQL-databasen:

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

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns värdnamn/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasnamn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema som skapades tidigare |
| `DIGNA_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-uppsättningen |
| `DIGNA_REPO_PASSWORD` | Ditt lösenord | Lösenord satt vid schema-skapandet |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valfri. SSL-läge för PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valfri. Antal anslutningar som digna håller öppna mot repositoryt |

#### [base] Avsnittet

Detta avsnitt innehåller säkerhets-, cookie- och inspektionsinställningar:

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

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_FERNET_KEY` | Värdet som visas ovan | Nyckel för den kryptering som tidigare releaser använde. Den måste finnas; behåll det visade värdet |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Den värd som dashboarden nås under. `""` anger ingen domän, vilket är rätt bakom en proxy som serverar dashboarden och backend under samma origin |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Måste vara `true` när digna serveras över HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Håller sessionscookien utom räckhåll för skript |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Sessionsutgång i sekunder |
| `DIGNA_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal inspektioner som får köras samtidigt |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Obligatorisk. Används för länkarna i aviseringsmeddelanden, så det måste vara en URL som mottagarna kan öppna |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valfri. Antal sekunder som en enskild fråga mot en källdatabas får köras innan den avbryts; `0` stänger av tidsgränsen |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valfri. Antal sekunder att vänta på en anslutning till en källdatabas; `0` väntar obegränsat |

!!! tip "Tips"

    För att hitta antalet CPU-kärnor på din Mac, kör `sysctl -n hw.ncpu`.

#### [encryption] Sektionen

Denna sektion innehåller nyckeln som används för att kryptera känsliga värden i repositoryt. Den är **obligatorisk** — `config check` rapporterar sektionen `[encryption]` som FAILED om nyckeln saknas.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Värde | Noter |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodad nyckel | Krypterar känsliga värden som lagras i digna-repositoryt |

!!! warning "Skydda config.toml"

    Den här nyckeln är ett fast värde, identiskt i alla digna-installationer, och det är den som dekrypterar de känsliga värdena i ditt repository. Begränsa `config.toml` till det konto som kör digna, håll filen utanför versionshantering och delade enheter, och undanta den från varje säkerhetskopia som förvaras mindre säkert än repositoryt självt.

#### [logging] Avsnittet

Detta avsnitt konfigurerar logghantering:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning. `TRACE`, `WARN` och `ERROR` accepteras också |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valfri. Katalog för de roterande loggfilerna, relativt arbetskatalogen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valfri. Antal roterade loggfiler som behålls |

#### [duckdb] Avsnittet (valfritt) {: #duckdb-section }

Nytt i Release 2026.11. Denna sektion anger resurserna för **digna Engine**, som profilerar
data inuti digna för databasanslutningar vars profileringsplats är **digna Engine**, och som kör
kontroller av referentiell integritet mellan datakällor på olika databasanslutningar. Se
[Profileringsplats](../../../platform/profiling/profiling_location.md).

Sektionen är valfri. Utan den gäller standardvärdena nedan.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Minne, i MB, som en körning av digna Engine får använda. Upp till `DIGNA_MAX_WORKERS` körningar kan vara aktiva samtidigt |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: systemets temporära katalog (`$TMPDIR` för det konto som kör digna) | Katalog för temporära filer när data inte ryms i minnet |

!!! tip "Dimensionera digna Engine"

    Planera för upp till `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` minne på
    digna-värden, utöver det som digna själv använder, och för tillräckligt med ledigt diskutrymme i
    den temporära katalogen för att rymma det största inspekterade datumet bland de datakällor som
    använder digna Engine. Peka `DIGNA_DUCKDB_TEMP_DIRECTORY` mot en disk med det utrymmet, skrivbar
    för det konto som kör digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Du behöver bara denna sektion om minst en databasanslutning använder digna Engine, eller om en
    kontroll av referentiell integritet jämför datakällor på olika anslutningar.

---

### Steg 2: Validera konfigurationen

Kontrollera att `config.toml` är fullständig och korrekt uppbyggd innan du initierar repositoryt. Kör i din digna-installationskatalog:

```bash
./digna config check
```

Varje sektion valideras för sig, så att ett enskilt fel inte döljer tillståndet hos de övriga:

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

Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter. En WARNING under **Unknown keys** listar nycklar i `config.toml` som digna inte läser; de har ingen effekt, så ta bort dem eller rätta stavningen. Den fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202611.md).

### Steg 3: Initiera repositoriet

1. Öppna **Terminal**
2. Navigera till din digna-installationskatalog (där `config.toml` och `digna`-körbara finns)
3. Kör anslutningstestet:

```bash
cd /opt/digna
./digna repo check
```

På ett nytt schema ansluter kommandot och rapporterar sedan att inget repository är installerat ännu:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Vid det här laget är det det förväntade resultatet: det bekräftar att digna når PostgreSQL och schemat. Ett anslutnings- eller autentiseringsfel pekar i stället på sektionen `[repo]` eller på PostgreSQL-uppsättningen.

!!! note "Notera"

    På macOS finns inte kommandon i den aktuella katalogen på din PATH, så den körbara anropas som `./digna` istället för `digna`. För att använda kortformen överallt, lägg till installationskatalogen i din PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Steg 4: Installera repository-schemat

I samma katalog, kör:

```bash
./digna repo upgrade
```

Detta kommando installerar nödvändiga tabeller i repositoryschemat och avslutas med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerar och uppgraderar"

    Från Release 2026.11 installerar `repo upgrade` ett nytt repository och uppgraderar ett befintligt.
    `repo install` fungerar fortfarande som ett annat namn för samma kommando.

### Steg 5: Skapa en administratörsanvändare

Administratörsanvändaren skapas direkt mot repositoryschemat, så servern behöver inte köras ännu. Kör i digna-installationskatalogen:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Exempel:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Detta skapar en användare med e-postadressen `admin@example.com` och fullständiga administratörsrättigheter.

!!! tip "Tips"

    Omge lösenordet med enkla citattecken. `zsh` behandlar tecken som `!`, `$` och `*` särskilt, och ett oavgränsat lösenord som innehåller dem skickas inte som avsett.

!!! tip "Bästa praxis"

    Använd ett starkt lösenord med en blandning av versaler, gemener, siffror och specialtecken.

### Steg 6: Starta digna-servern

I digna-installationskatalogen, starta servern med:

```bash
./digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns värdnamn/IP (standard `127.0.0.1`)
- `--port` — Serverns port (standard `8000`)

När servern är igång skriver den ut adressen som den lyssnar på:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Tips"

    Första gången du startar servern kan macOS fråga om du vill tillåta att applikationen accepterar inkommande nätverksanslutningar. Klicka **Allow**, annars kommer inte dashboarden att kunna nå backend.

!!! note "Servern upptar terminalen"

    `serve` körs i förgrunden och fortsätter tills du stoppar den med ++ctrl+c++. Låt den vara igång medan du slutför installationen; för att i stället starta den automatiskt vid uppstart, se [Köra digna som bakgrundstjänst](#running-digna-as-a-background-service).

---

## Dashboard-konfiguration {: #dashboard-configuration }

### Steg 1: Distribuera dashboarden till webbservern

digna-dashboarden läser sin egen konfiguration från `dashboard/dashboard_config.toml`. Den filen medföljer inte installationen — du skapar den i katalogen `dashboard/` bredvid dashboardfilerna.

Dess innehåll beskrivs under [Enkel inloggning (SSO)](../../../sso/overview.md), som också är där filen behövs: den innehåller de inloggningsalternativ som dashboarden erbjuder och, vid uppsättningar med flera instanser, backend-anslutningen.

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

Detta avsnitt uppgraderar en installation av Release 2026.06 till Release 2026.11. Om din
installation är äldre, läs först [Uppgradera från en release före 2026.06](#upgrading-from-a-release-before-2026-06).

### Innan du uppgraderar

**Det är obligatoriskt att skapa en backup av digna-repositoryt**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

För att skapa en backup från Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Begär licensfilen för Release 2026.11**

Release 2026.11 kräver en ny `license.toml`. Begär den från digna-teamet innan du börjar, och
ha den redo för [steg 7](#step-7-replace-the-license-file).

### Uppgradera från en release före 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 medförde tre ändringar som fortfarande gäller när du uppgraderar en äldre installation
direkt till 2026.11:

- **Endast ODBC.** digna når varje källteknik via ODBC. Varje databasanslutning som ännu
  inte använder ODBC måste läggas om till ODBC efter uppgraderingen; det finns ingen automatisk
  konvertering. Installera ODBC-drivrutinerna på digna-värden i förväg, se
  [Installera ODBC-drivrutinen på digna-värden](../../../databases/overview.md#install-the-driver),
  och ha egenskaperna för varje anslutning redo från
  [teknikguiderna](../../../databases/overview.md#technology-guides). Databricks Legacy-anslutaren
  finns inte längre; flytta de anslutningarna till
  [Databricks](../../../databases/databricks_connector_guide.md)-anslutaren.
- **En körbar fil.** `dignabackend` och `dignacli` ersätts av den enda körbara filen `digna`,
  som förenar backend och CLI.
- **config.toml.** Sektionen `[encryption]` är obligatorisk, och `DIGNA_APP_HOST` och
  `DIGNA_APP_PORT` läses inte längre: servern hämtar sin adress och port från `digna serve`.
  Jämför din fil med [Backendkonfiguration](#backend-configuration).

Stegen nedan anger var en äldre installation behöver något annat. Repositoryuppgraderingen i
steg 8 för ett repository från vilken tidigare release som helst direkt till 2026.11.

### Uppgraderingsprocess

#### Steg 1: Stoppa digna-tjänsten {: #step-1-stop-the-digna-service }

Om digna körs som en bakgrundstjänst, stoppa den först:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Om digna körs i förgrunden, tryck ++ctrl+c++ i dess Terminal-fönster.

#### Steg 2: Säkerhetskopiera nuvarande installation {: #step-2-backup-current-installation }

Byt namn på den körbara filen och dashboard-mappen i din nuvarande installation i
digna-installationskatalogen, så att den nya releasen kan distribueras vid sidan av dem:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Behåll `digna_old` tills du har verifierat uppgraderingen, och `dashboard_old` tills du har återställt
dina konfigurationsfiler från den (se steg 4). Därefter kan du ta bort båda.

!!! info "Uppgradera från en release före 2026.06"

    Byt namn på mapparna `dignabackend` och `dignacli` i stället för den körbara filen:
    `mv dignabackend dignabackend_old` och `mv dignacli dignacli_old`. Ingen av dem används av Release 2026.11.

#### Steg 3: Packa upp och distribuera ny version {: #step-3-extract-and-deploy-new-version }

1. Packa upp den nya digna-installations-ZIP-filen
2. Kopiera den nya körbara filen `digna` och mappen `dashboard` till din installationskatalog
3. Återställ exekveringsbiten och ta vid behov bort karantänattributet:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Varning"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` ingår någonsin i
    installations-ZIP:en — digna-teamet levererar aldrig någon av filerna. Din befintliga konfiguration
    påverkas därför inte av uppgraderingen, och kopiorna i de omdöpta `*_old`-mapparna är de
    enda du har.

#### Steg 4: Återställ dina konfigurationsfiler {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 kräver ingen ändring i `config.toml`: en fil som fungerar med Release 2026.06 fortsätter
att fungera. Två ändringar är valfria:

- Lägg till en [`[duckdb]`-sektion](#duckdb-section) om databasanslutningar ska använda digna Engine
  och dess standardvärden inte passar din värd.
- Utelämna sektionen `[app]` om en omvänd proxy serverar dashboarden och backend under samma
  origin.

!!! warning "Inställningar som digna inte läser"

    Tidigare versioner av denna guide visade några inställningar som digna inte läser. De har ingen
    effekt, och `config check` listar dem under **Unknown keys** i steg 6. Ta bort eller rätta
    dem:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` och
      `digna_LOGGING_BACKUP_COUNT` finns inte. Ta bort dem.
    - Inställningsnamn är skiftlägeskänsliga. digna läser `DIGNA_REPO_HOST`, inte `digna_REPO_HOST`.
      Skriv varje namn med versaler, som i [Backendkonfiguration](#backend-configuration).

!!! warning "Enkel inloggning: behåll [[oidc_clients]]"

    digna läser leverantörer för enkel inloggning som en lista med `[[oidc_clients]]`-poster, var och en
    med sin egen `DIGNA_OIDC_KEY`. Om du har ändrat dina leverantörer till `[oidc_clients.<key>]`-sektioner,
    som en tidigare version av denna guide visade, ändra tillbaka dem. `config check` rapporterar
    `OIDC config(s)` som FAILED så länge den formen används:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Upprepa posten för varje leverantör, och håll varje `DIGNA_OIDC_KEY` identisk med `key` i
    `dashboard_config.toml`. Endast installationer som använder enkel inloggning berörs.

#### Steg 5: Ladda om webbservern {: #step-5-reload-the-web-server }

Dashboarden är en uppsättning statiska filer, så din webbserver — och webbläsaren — kan fortfarande
leverera den tidigare versionen. Ladda om eller starta om den webbserver som är värd för mappen `dashboard`
och ladda sedan om sidan med en hård uppdatering (++cmd+shift+r++).

#### Steg 6: Validera konfigurationen {: #step-6-validate-the-configuration }

Kontrollera att `config.toml` är fullständig innan du rör repositoryt:

```bash
./digna config check
```

Varje sektion måste rapportera OK. Åtgärda allt som rapporteras som FAILED, ta bort nycklarna som listas
under **Unknown keys** och kör kommandot igen innan du fortsätter.

#### Steg 7: Ersätt licensfilen {: #step-7-replace-the-license-file }

En licensfil följer normalt med från en release till nästa. Release 2026.11 är ett
undantag: den lägger till två licensierade moduler, digna Data Reconciliation och digna Agentic, och en
licens som utfärdats före 2026.11 innehåller dem inte. Kopiera den `license.toml` som digna-teamet
tillhandahållit för Release 2026.11 till installationskatalogen och ersätt den gamla:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Behåll inte den tidigare licensen"

    Med den tidigare licensen startar digna fortfarande, men digna Data Reconciliation och digna
    MCP Server förblir avstängda. Varje kommando som kontrollerar licensen — `user`,
    `inspection`, `repo` — avbryts innan det rör repositoryt när kontrollen misslyckas. Verifiera
    den nya licensen innan du går vidare:

    ```bash
    ./digna license check
    ```

#### Steg 8: Uppgradera repositoryschemat {: #step-8-upgrade-the-repository-schema }

Kör i din digna-installationskatalog:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 hanterar repositoryschemat med versionerade migreringar. Den första uppgraderingen från
en tidigare release för schemat till den sista versionen av det tidigare systemet, registrerar den som
utgångspunkt och tillämpar sedan migreringarna i Release 2026.11. Den avslutas med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

All befintlig data bevaras. För att när som helst se repositoryts tillstånd, kör
`./digna repo check`: det listar den senast tillämpade migreringen och eventuella väntande migreringar.

!!! warning "digna startar inte på ett föråldrat repository"

    Från Release 2026.11 vägrar servern att starta så länge repositoryt behöver uppgraderas, och
    säger det, till exempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kör `repo upgrade` innan du startar servern eller tjänsten.

#### Steg 9: Starta om tjänsterna {: #step-9-restart-services }

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

#### Steg 10: Verifiera uppgraderingen {: #step-10-verify-the-upgrade }

1. Bekräfta releasen för den nya körbara filen:

    ```bash
    ./digna version
    ```

    Första raden måste vara `Release: 2026.11`.

2. Öppna digna-dashboarden och kontrollera att gränssnittet laddas korrekt.
3. Kontrollera serverns utdata och filerna i katalogen `logs` efter fel.
4. Testa dina databasanslutningar — se
   [Testa en anslutning](../../../databases/overview.md#testing-a-connection). Efter en uppgradering
   från en release före 2026.06, lägg först om varje anslutning som inte redan använde ODBC till
   ODBC.

För att komma igång med de nya modulerna, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Ansluta en AI-agent](../../../platform/agentic/connect_ai_agent.md) för digna MCP Server och
[Profileringsplats](../../../platform/profiling/profiling_location.md) för digna Engine.