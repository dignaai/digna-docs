# Windows-installationsguide för digna Release 2026.06

**Release:** 2026.06

**Senast uppdaterad:** 30 augusti 2026


---

## Innehållsförteckning

1. [Introduktion](#introduction)
2. [Systemkrav](#system-requirements)
3. [Förberedelser inför installation](#pre-installation-setup)
4. [PostgreSQL-serverinställning](#postgresql-server-setup)
5. [Webbserverkonfiguration](#web-server-configuration)
6. [Första installationen](#initial-installation)
7. [Backendkonfiguration](#backend-configuration)
8. [Dashboardkonfiguration](#dashboard-configuration)
9. [Köra digna som Windows-tjänst](#running-digna-as-a-windows-service)
10. [Uppgradera till en ny release](#upgrading-to-a-new-release)

---

## Introduktion {: #introduction }

### Om digna

digna är en omfattande AI-driven plattform utformad för att optimera hanteringen av datakvalitet över olika data-miljöer såsom datalager, data lakes och lakehouses. Byggd för att vara mycket skalbar och anpassningsbar, adresserar digna moderna datautmaningar genom automation, realtidsövervakning och anomalidetektion.

digna består av två huvudkomponenter:

- **digna**: applikationens kärna, ansvarig för att bearbeta data och utföra kvalitetskontroller. Den förenar backend och kommandoradsgränssnittet i en enda körbar fil och ersätter därmed de separata programmen `dignabackend` och `dignacli` från tidigare releaser.
- **dignadashboard**: Ett webbaserat gränssnitt hostat på en webbserver, som ger ett användarvänligt sätt att interagera med digna-plattformen och visualisera datakvalitetsmått.

### Nytt i Release 2026.06

Denna release för in data-observability-funktioner direkt i din kod, vilket gör det möjligt för utvecklare att övervaka datakvalitet vid källan. Se [release notes](http://docs.digna.ai/changelog/Release_202606/) för fullständiga detaljer.

### Letar du efter macOS eller Linux?

Denna guide täcker Windows. För andra plattformar, se [macOS-installationsguide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) eller [Linux-installationsguide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Systemkrav {: #system-requirements }

Innan du påbörjar installationen, se till att ditt system uppfyller följande minimikrav:

| Krav | Specifikation |
|---|---|
| **Operativsystem** | Windows Server eller Windows 10/11 |
| **Minne (minimal installation)** | 16 GB RAM |
| **Diskutrymme** | 10 GB ledigt lagringsutrymme |
| **Databas** | PostgreSQL Server 12 eller senare |
| **Webbserver** | IIS, Apache Tomcat eller motsvarande |

### Alternativ för databasinstallation

**Om PostgreSQL redan är installerat:**
Du kan lägga till en ny databas för digna i din befintliga PostgreSQL-server.

**Om PostgreSQL installeras på samma maskin som digna:**

!!! info "Rekommenderade specifikationer"

    - **Minne**: 32 GB RAM (istället för 16 GB)
    - **Diskutrymme**: 50 GB ledigt lagringsutrymme (istället för 10 GB)

    Dessa högre specifikationer rymmer både digna och PostgreSQL-databasen som körs samtidigt.

---

## Förberedelser inför installation {: #pre-installation-setup }

Innan du installerar digna, se till att två viktiga förutsättningar är på plats:

1. **PostgreSQL Server** – för att lagra beräknade mått och prestandadata
2. **Webbserver** – för att hosta digna Dashboard

Om dessa komponenter inte redan är uppsatta, följ avsnitten nedan för att installera och konfigurera dem.

---

## PostgreSQL-serverinställning {: #postgresql-server-setup }

### Om du redan har PostgreSQL

Om PostgreSQL redan är installerat och körs på din lokala maskin eller om du använder en hanterad fjärr-PostgreSQL-server, kan du hoppa till [nästa avsnitt](#web-server-configuration).

### Installera PostgreSQL

Följ dessa steg för att installera PostgreSQL på Windows:

#### Steg 1: Ladda ner PostgreSQL

1. Besök [PostgreSQL:s nedladdningssida](https://www.postgresql.org/download/)
2. Välj **Windows**
3. Ladda ner den senaste installatören

#### Steg 2: Kör installatören

1. Dubbelklicka på den nedladdade installatörsfilen
2. Följ anvisningarna i installationsguiden

#### Steg 3: Välj installationskatalog

Välj katalog där PostgreSQL ska installeras. Standardplatsen är vanligtvis lämplig.

#### Steg 4: Välj komponenter

För en standardinstallation, behåll standardvalen av komponenter.

#### Steg 5: Ange lösenord för PostgreSQL-superanvändaren

Ange och bekräfta ett lösenord för PostgreSQL-superanvändaren (`postgres`). **Spara detta lösenord säkert** — du kommer att behöva det senare.

#### Steg 6: Konfigurera portnummer

Standardporten för PostgreSQL är `5432`. Du kan använda standardporten eller ange en annan port vid behov.

!!! tip "Tips"

    Om port 5432 redan används, välj en alternativ port och notera den för senare konfiguration.

#### Steg 7: Välj locale

Välj locale för din databas. Standardinställningen är vanligtvis lämplig för de flesta installationer.

#### Steg 8: Slutför installationen

Klicka **Next** genom återstående steg och sedan **Finish**.

#### Steg 9: Verifiera installationen

Öppna Kommandotolken och verifiera att PostgreSQL är installerat:

```bash
psql --version
```

Du bör se PostgreSQL-versionen om installationen lyckades.

---

## Webbserverkonfiguration {: #web-server-configuration }

digna kräver en webbserver för att hosta dashboarden. Välj ett av följande alternativ:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Du behöver endast installera och konfigurera **en** av dessa servrar.

### IIS-inställning {: #iis-setup }

#### Översikt

Internet Information Services (IIS) är Microsofts webbserver för att hosta webbplatser och webbaserade applikationer.

#### Aktivera IIS

1. **Öppna Kontrollpanelen**
   - Tryck `Win + R`
   - Skriv `control` och tryck Enter

2. **Gå till Windows-funktioner**
   - Klicka **Programs**
   - Välj **Turn Windows features on or off**

3. **Aktivera Internet Information Services**
   - Scrolla ner och hitta **Internet Information Services (IIS)**
   - Markera kryssrutan för att aktivera den
   - Klicka på **+** för att expandera och verifiera att dessa underkomponenter är valda:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klicka OK** för att tillämpa ändringarna

5. **Verifiera IIS-installationen**
   - Öppna din webbläsare
   - Navigera till `http://localhost`
   - Du bör se IIS välkomstsida

#### Krävs: URL Rewrite-modulen

IIS kräver URL Rewrite-komponenten. Ladda ner och installera den från [officiella Microsoft-sidan](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Krävs: MIME-typ för Markdown-filer

För att säkerställa att Markdown-filer (`.md`) serveras korrekt av IIS:

1. Öppna **IIS Manager** (tryck `Win + R`, skriv `inetmgr`, tryck Enter)
2. Navigera till **Din webbplats > MIME Types**
3. Klicka **Add...**
4. Konfigurera:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Viktigt"

    Utan denna inställning kan `.md`-filerna inte serveras korrekt.

---

### Apache Tomcat-inställning {: #apache-tomcat-setup }

#### Översikt

Apache Tomcat är en öppen källkods Java-servlet-container och webbserver.

#### Installation

1. **Ladda ner Apache Tomcat**
   - Besök [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Ladda ner Windows ZIP-distributionen

2. **Packa upp arkivet**
   - Packa upp ZIP-filen till en katalog på din maskin
   - Exempel: `C:\Program Files\Apache Tomcat`

3. **Verifiera att Tomcat körs**
   - Öppna din webbläsare
   - Navigera till `http://localhost:8080`
   - Du bör se Apache Tomcat välkomstsida

!!! tip "Tips"

    Apache Tomcat startar vanligtvis automatiskt efter installation. Om det inte gör det, gå till `bin`-mappen och kör `startup.bat`.

---

## Första installationen {: #initial-installation }

### Steg 1: Konfigurera digna-repositoryt

digna-repositoryt lagrar alla mått som beräknas av digna. Det fungerar som den centrala databasen för analytiska och prestandadata.

#### Skapa schema och användare för repositoryt

Öppna din PostgreSQL-klient (pgAdmin, psql eller liknande) och kör följande SQL-kommandon:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Ersätt följande platshållare:**

- `<digna_repo_schema>` — Ditt önskade schema-namn (t.ex. `dignarepo`)
- `<digna_repo_user>` — Ditt önskade användarnamn (t.ex. `digna_user`)
- `<digna_repo_password>` — Ett säkert lösenord för denna användare

**Exempel:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Bästa praxis"

    Använd starka, komplexa lösenord för databas-användare. Undvik inloggningsuppgifter som är lätta att gissa.

---

### Steg 2: Packa upp digna-installationspaketet

1. Lokalisera digna-installations-ZIP-filen som tillhandahållits till dig
2. Packa upp den till önskad installationsplats
3. Efter uppackning bör du se följande objekt:
   - `dashboard/` — Webbgränssnittet
   - `digna` — Huvudexekverbara filen (backend + CLI kombinerat)

!!! info "Konfigurations- och licensfilerna ingår inte i paketet"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` medföljer installationen — du
    skapar båda själv, i [Backendkonfiguration](#backend-configuration) och
    [Dashboardkonfiguration](#dashboard-configuration). Inte heller `license.toml` medföljer;
    digna levererar den separat, enligt beskrivningen i steg 3.

### Steg 3: Installera licensfilen

!!! warning "Viktigt"

    Licensfilen ingår **inte** i installationspaketet och kommer att tillhandahållas separat av digna.

1. Lokalisera `license.toml`-filen som tillhandahållits till dig
2. Kopiera den till root i digna-installationskatalogen (där `config.toml` och den körbara `digna`-filen finns)

**Varför detta är viktigt:**
Licensfilen innehåller din kundinformation, licensens utgångsdatum och digital signatur. **Ändra inte filen** — eventuella ändringar gör den ogiltig.

**Katalogstruktur efter setup:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backendkonfiguration {: #backend-configuration }

### Steg 1: Skapa och redigera konfigurationsfilen

Filen `config_template.toml` levereras i din digna-installationskatalog. Du behöver bara byta namn på den till `config.toml`.

**Plats:** `digna_installation/config.toml`

Öppna `config.toml` i en textredigerare och konfigurera varje avsnitt nedan.

#### Avsnittet [app]

Detta avsnitt konfigurerar digna-backendens applikationsinställningar:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend-URL | Om dashboarden ligger på annan server, inkludera dess URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Krävs för CORS med credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Tillåt alla HTTP-metoder |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Tillåt alla headers |

#### Avsnittet [repo]

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
| `digna_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns hostname/IP |
| `digna_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `digna_REPO_DB` | `postgres` | Databasnamn |
| `digna_REPO_SCHEMA` | `dignarepo` | Schema som skapades tidigare |
| `digna_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-setupen |
| `digna_REPO_PASSWORD` | Ditt lösenord | Lösenord som sattes när schemat skapades |

#### Avsnittet [base]

Detta avsnitt innehåller säkerhets- och cookie-inställningar:

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

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Matcha din frontend-domän |
| `digna_COOKIE_SECURE` | `false` (lokalt) / `true` (produktion) | Använd `true` för HTTPS-anslutningar |
| `digna_COOKIE_HTTPONLY` | `true` | Alltid aktiverat för säkerhet |
| `digna_COOKIE_SAME_SITE` | `lax` | Förhindrar CSRF-attacker |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Session timeout i sekunder |
| `digna_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal parallella inspektionsjobb |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maximal fördröjning, i sekunder, som schemaläggaren får lägga till innan ett förfallet jobb startar |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Tidpunkt (24-timmarsformat `HH:MM`) då den dagliga rensningen startar |

#### Avsnittet [encryption]

Detta avsnitt innehåller nyckeln som används för att kryptera känsliga värden i repositoryt. Det är **obligatoriskt** — `config check` rapporterar sektionen `[encryption]` som FAILED om nyckeln saknas.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodad nyckel | Krypterar känsliga värden som lagras i digna-repositoryt |

!!! warning "Skydda config.toml"

    Den här nyckeln är ett fast värde, identiskt i alla digna-installationer, och det är den som dekrypterar de känsliga värdena i ditt repository. Begränsa `config.toml` till det konto som kör digna, håll filen utanför versionshantering och delade enheter, och undanta den från varje säkerhetskopia som förvaras mindre säkert än repositoryt självt.

#### Avsnittet [logging]

Detta avsnitt konfigurerar loggningen:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Antal dagliga logg-backuper att behålla |

---

### Steg 2: Validera konfigurationen

Kontrollera att `config.toml` är fullständig och korrekt uppbyggd innan du initierar repositoryt. Kör i din digna-installationskatalog:

```bash
digna config check
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

Overall: OK
```

Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter. Den fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202606.md).

### Steg 3: Initiera repositoryt

1. Öppna Kommandotolken
2. Navigera till din digna-installationskatalog (där `config.toml` och den körbara `digna`-filen finns)
3. Kör anslutningstestet:

```bash
digna repo check
```

Du bör se en bekräftelse på att anslutningen upprättats (själva repositoryt har ännu inte initialiserats).

### Steg 4: Installera repositoryschemat

I samma katalog, kör:

```bash
digna repo install
```

Detta kommando installerar nödvändiga tabeller och schema i din PostgreSQL-databas.

### Steg 5: Skapa en admin-användare

1. Öppna ett **nytt** Kommandotolksfönster
2. Navigera till din digna-installationskatalog
3. Kör följande kommando för att skapa en admin-användare:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Exempel:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Detta skapar en användare med fullständiga administrativa privilegier.

!!! tip "Bästa praxis"

    Använd ett starkt lösenord med en mix av versaler, gemener, siffror och specialtecken.

---

### Steg 6: Starta digna-servern

I digna-installationskatalogen, starta servern med:

```bash
digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns hostname/IP
- `--port` — Serverns port 

Du bör se startmeddelanden som bekräftar att servern körs:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Servern upptar terminalen"

    `serve` körs i förgrunden och fortsätter tills du stoppar den med ++ctrl+c++. Låt den vara igång medan du slutför installationen; för att i stället starta den automatiskt vid uppstart, se [Köra digna som Windows-tjänst](#running-digna-as-a-windows-service).

## Dashboardkonfiguration {: #dashboard-configuration }

### Steg 1: Distribuera dashboarden till webbservern

digna-dashboarden läser sin egen konfiguration från `dashboard/dashboard_config.toml`. Den filen medföljer inte installationen — du skapar den i katalogen `dashboard/` bredvid dashboardfilerna.

Dess innehåll beskrivs under [Enkel inloggning (SSO)](../../../sso/overview.md), som också är där filen behövs: den innehåller de inloggningsalternativ som dashboarden erbjuder och, vid uppsättningar med flera instanser, backend-anslutningen.

Välj din webbserver och följ motsvarande deploy-steg.

#### Distribuera till IIS

1. **Öppna IIS Manager**
   - Tryck `Win + R`, skriv `inetmgr`, tryck Enter

2. **Skapa en ny webbplats**
   - I vänster panel, högerklicka på **Sites**
   - Välj **Add Website...**

3. **Konfigurera webbplatsen**
   - **Site Name**: Ange ett namn (t.ex. "dignaDashboard")
   - **Physical Path**: Klicka Browse och välj din `dashboard`-mapp
   - **Binding**: Ställ in IP-adress och port (standardport 80 för HTTP, 443 för HTTPS)

4. **Starta webbplatsen**
   - Klicka **OK** för att skapa webbplatsen
   - Högerklicka på den nya webbplatsen och välj **Start**

5. **Testa installationen**
   - Öppna din webbläsare
   - Navigera till `http://localhost` (eller din konfigurerade URL)
   - Du bör se digna-dashboardens inloggningssida

#### Distribuera till Apache Tomcat

1. **Kopiera dashboard till Tomcat**
   - Kopiera `dashboard`-mappen till din Tomcat `webapps`-katalog
   - Byt namn vid behov (t.ex. till `digna`)
   - Exempel: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Verifiera distributionen**
   - Uppdatera eller ladda om Tomcat-hanteringssidan (http://localhost:8080)
   - Du bör se "digna" (eller ditt valda namn) listad bland distribuerade applikationer

3. **Öppna dashboarden**
   - Öppna din webbläsare
   - Navigera till `http://localhost:8080/digna`
   - Du bör se digna-dashboardens inloggningssida

---

## Köra digna som Windows-tjänst {: #running-digna-as-a-windows-service }

### Varför använda en Windows-tjänst?

Att köra digna-backend som en Windows-tjänst säkerställer att den:
- Startar automatiskt när servern bootar
- Körs i bakgrunden utan öppen Kommandotolk
- Startar om automatiskt om den kraschar
- Kan hanteras via Windows Services

### Kommandona `windows`

Tjänsten hanteras av den körbara filen `digna` själv, via underkommandona `digna windows`.
Det finns inga batch-filer att köra.

| Kommando | Syfte |
|---|---|
| `digna windows install` | Registrerar digna som en Windows-tjänst |
| `digna windows start` | Startar den registrerade tjänsten |
| `digna windows stop` | Stoppar den körande tjänsten |
| `digna windows uninstall` | Avregistrerar tjänsten |

!!! warning "Administratörsrättigheter krävs"

    Alla fyra kommandona måste köras från en Kommandotolk som öppnats som administratör.

Varje kommando accepterar `--name` för att adressera en tjänst som registrerats under ett annat namn än standardnamnet. Den
fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202606.md).

### Installera tjänsten

1. **Öppna Kommandotolken som administratör**
   - Högerklicka på Kommandotolken
   - Välj "Run as Administrator"

2. **Navigera till din digna-installationskatalog**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registrera tjänsten**
   ```bash
   digna windows install
   ```

!!! important "Ange adress och port om inte standardvärdena passar dig"

    `install` sparar adressen och porten i tjänstregistreringen, och tjänsten binder till
    exakt det som sparades. Standardvärdena är `127.0.0.1` och `8000`, som bara accepterar anslutningar
    från maskinen själv. En dashboard på en annan värd kan inte nå den, så ange den
    adress som backend ska lyssna på:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Dessa läses inte från `config.toml`. För att ändra dem senare avinstallerar du tjänsten och
    installerar den igen med de nya värdena.

Tjänsten registreras med **automatisk start**, så den startar tillsammans med Windows. Den startar inte
omedelbart — se nästa avsnitt.

#### Installationsalternativ

| Alternativ | Standard | Syfte |
|---|---|---|
| `--name` | `digna` | Namn som tjänsten ska registreras under |
| `--display-name` | `digna` | Namn som visas i services.msc |
| `--description` | `digna data quality backend` | Beskrivning som visas i services.msc |
| `--address` | `127.0.0.1` | Adress som tjänsten binder sitt API till |
| `--port` | `8000` | Port som tjänsten binder sitt API till |
| `--working-dir` | katalogen där den körbara filen `digna` ligger | Katalog som innehåller `config.toml` och `license.toml`, och som tjänsten gör till sin arbetskatalog |
| `--start-type` | `auto` | `auto` startar med Windows, `manual` startar bara när det begärs, `disabled` registrerar tjänsten men vägrar starta den |
| `--account` | `LocalSystem` | Konto att köra som, t.ex. `DOMAIN\user` eller `.\user` |
| `--password` | | Lösenord för `--account` |

!!! tip "Köra under ett domänkonto"

    `LocalSystem` saknar nätverksidentitet, så Windows-autentisering mot SQL Server och all
    åtkomst till en nätverksresurs misslyckas. Installera med `--account` och `--password` när
    tjänsten behöver nå resurser som en viss användare.

### Starta och stoppa tjänsten

#### Starta tjänsten

```bash
digna windows start
```

#### Stoppa tjänsten

```bash
digna windows stop
```

!!! tip "Tips"

    Stoppa alltid tjänsten innan du uppdaterar applikationsfiler.

### Flytta tjänsten till en ny katalog

Om du behöver flytta digna-installationen:

1. **Stoppa och avregistrera den nuvarande tjänsten**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Flytta applikationsfilerna**
   - Flytta hela digna-installationsmappen till den nya platsen

3. **Registrera tjänsten igen från den nya platsen**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Upprepa de värden för `--address`, `--port` eller `--account` som du använde första gången — den tidigare
   registreringen är borta.

4. **Starta tjänsten**
   ```bash
   digna windows start
   ```

### Avinstallera tjänsten

1. **Stoppa den körande tjänsten**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Avregistrera tjänsten**
   ```bash
   digna windows uninstall
   ```

digna-servern är nu avregistrerad som en Windows-tjänst.

---

## Uppgradera till en ny release {: #upgrading-to-a-new-release }

### Innan du uppgraderar

**Verifiera alla databasanslutningar först**

Från Release 2026.06 når digna varje källteknologi via **ODBC**. Tidigare releaser erbjöd ett val mellan en teknikspecifik drivrutin och ODBC, via omkopplaren **Use ODBC**. digna-teamet har valt att bygga enbart på ODBC, eftersom ett enda standardiserat gränssnitt ger mer än en uppsättning skräddarsydda drivrutiner:

- **Autentisering** — autentisering är en del av ODBC, så en anslutning kan använda allt som dess drivrutin stöder: lösenord, tokens och PAT:ar, Kerberos och Active Directory, MFA och webbläsarbaserad enkel inloggning, molnidentiteter, klientcertifikat och TLS. Nya metoder kommer med en uppdatering av drivrutinen i stället för att vänta på en digna-release.
- **Drivrutiner som underhålls av databasleverantörerna** — leverantörens egen drivrutin följer nya serverversioner och säkerhetsfixar, och du kan uppdatera den enligt ditt eget schema, oberoende av digna.
- **Ett enda sätt att konfigurera allt** — varje teknik är en lista med nyckel/värde-egenskaper, med samma gränssnitt, samma kryptering av känsliga värden och samma felsökning, i stället för olika fält per källa.
- **Finjustering och räckvidd** — drivrutinsalternativ som timeouts, TLS-inställningar, proxyservrar och hämtningsstorlekar är tillgängliga för varje källa, och varje teknik med en kompatibel ODBC-drivrutin kan anslutas, även sådana som digna inte publicerar någon egen guide för.

I praktiken innebär detta att omkopplaren **Use ODBC** och de separata fälten för värd, port, databas, användare och lösenord inte längre finns. **Varje anslutning som inte redan använder ODBC måste läggas om till ODBC** — det finns ingen automatisk konvertering, så planera för detta före uppgraderingen:

1. Gå igenom varje databasanslutning som är definierad i din installation och notera vilka som ännu inte använder ODBC — var och en av dem måste konfigureras om.
2. Installera motsvarande ODBC-drivrutin på digna-värden — anslutningar öppnas från den server som kör digna-backend, inte från webbläsaren. Se [Installera ODBC-drivrutinen på digna-värden](../../../databases/overview.md#install-the-driver).
3. Ha ODBC-egenskaperna redo för varje berörd anslutning. [Teknikguiderna](../../../databases/overview.md#technology-guides) listar en beprövad uppsättning egenskaper per källa.

Efter uppgraderingen lägger du om varje berörd anslutning till ODBC och testar den från dashboarden — se [Skapa en databasanslutning](../../../databases/overview.md#create-a-database-connection) och [Testa en anslutning](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy-anslutningar"

    Databricks Legacy-anslutaren har tagits bort i denna release. Migrera dessa anslutningar till [Databricks](../../../databases/databricks_connector_guide.md)-anslutaren.

**Det är obligatoriskt att säkerhetskopiera digna-repositoryt**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

### Uppgraderingsprocess

#### Steg 1: Stoppa och avregistrera den gamla tjänsten

Om digna körs som en Windows-tjänst, stoppa den med **batch-filerna i din nuvarande
installation** — kommandona `digna windows` hör till den nya releasen och är ännu inte
tillgängliga:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Avregistrera sedan tjänsten, även här med den gamla batch-filen. Registreringen pekar på den gamla
körbara filen och dess skript, som båda ersätts av den här uppgraderingen, så den kan inte återanvändas:

```bash
uninstall_service.bat
```

!!! warning "Avregistrera innan du byter namn på något"

    `uninstall_service.bat` ligger i mappen `bin` som du strax ska byta namn på, och det är det enda
    som kan ta bort den registrering det skapade. Kör det medan den gamla installationen fortfarande
    finns på plats. Om mappen redan har bytt namn, byt tillbaka namnet, avregistrera och fortsätt sedan.

    Anteckna vilket konto tjänsten kördes under samt vilken adress och port den lyssnade på — du kommer att
    behöva dem i steg 9.

#### Steg 2: Säkerhetskopiera nuvarande installation

Byt namn på mapparna i din nuvarande installation i digna-installationskatalogen, så att den nya releasen kan distribueras vid sidan av dem:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend och dignacli används inte längre"

    Från Release 2026.06 ersätts `dignabackend` och `dignacli` av den enda körbara filen `digna`, som förenar backend och CLI. Behåll `dignabackend_old` och `dignacli_old` bara tills du har verifierat uppgraderingen — därefter kan du ta bort båda mapparna. Behåll `dashboard_old` tills du har återställt dina konfigurationsfiler från den (se steg 4). Mappen `bin` försvinner också: dess batch-filer styrde den gamla tjänsten och 2026.06 levererar dem inte, så när tjänsten väl har avregistrerats i steg 1 gör de inget annat än att vilseleda.

#### Steg 3: Packa upp och distribuera den nya versionen

1. Packa upp den nya digna-installations-ZIP-filen
2. Kopiera den nya `digna`-exekverbara filen och `dashboard`-mappen till din installationskatalog


!!! warning "Viktigt"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` ingår någonsin i
    installations-ZIP:en — digna-teamet levererar aldrig någon av filerna. Din befintliga konfiguration
    påverkas därför inte av uppgraderingen, och kopiorna i de omdöpta `*_old`-mapparna är de
    enda du har.

#### Steg 4: Återställ dina konfigurationsfiler

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Release 2026.06 ändrar config.toml"

    Tre inställningar är nya och obligatoriska, och tre används inte längre. En `config.toml` som har följt med från en tidigare release saknar de nya inställningarna, och digna startar inte så länge de saknas. Lägg till följande i din befintliga `config.toml`:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Lägg till de två `[base]`-nycklarna i din befintliga `[base]`-sektion och lägg till `[encryption]` som ny sektion. Ta sedan bort de inställningar som inte längre används: **`digna_FERNET_KEY`** från `[base]`, samt **`digna_APP_HOST`** och **`digna_APP_PORT`** från `[app]` — servern hämtar nu adress och port från `digna serve`.

    Vad varje inställning gör beskrivs i [Backendkonfiguration](#backend-configuration).

!!! warning "Enkel inloggning: formatet för [oidc_clients] har ändrats"

    Release 2026.06 ersätter arrayen av tabeller med en tabell per leverantör, namngiven efter leverantörsnyckeln. `DIGNA_OIDC_KEY` är borta — nyckeln ingår nu i sektionsrubriken.

    Före:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Efter:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Upprepa sektionen för varje leverantör och håll varje nyckel identisk med `key` i `dashboard_config.toml`. `digna config check` rapporterar `oidc_clients` som FAILED så länge den gamla formen finns kvar. Endast installationer som använder enkel inloggning berörs.

#### Steg 5: Ladda om webbservern

Dashboarden är en uppsättning statiska filer, så din webbserver — och webbläsaren — kan fortfarande
leverera den tidigare versionen. Ladda om eller starta om den webbserver som är värd för mappen `dashboard`
och ladda sedan om sidan med en hård uppdatering (++ctrl+f5++).

#### Steg 6: Validera konfigurationen

Kontrollera att den uppdaterade `config.toml` är fullständig innan du rör repositoryt:

```bash
digna config check
```

Varje sektion måste rapportera OK. Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter.

#### Steg 7: Ersätt licensfilen

Varje release licensieras separat. Kopiera den `license.toml` som digna-teamet tillhandahållit för
denna release till installationskatalogen och ersätt den gamla:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Behåll inte den tidigare licensen"

    En `license.toml` som utfärdats för en tidigare release täcker inte den här, och varje kommando
    som kontrollerar licensen — `user`, `inspection`, `repo` — avbryts innan det rör
    repositoryt när kontrollen misslyckas. Verifiera den innan du går vidare:

    ```bash
    digna license check
    ```

#### Steg 8: Uppgradera repositoryschemat

Navigera till din digna-installationskatalog och kör:

```bash
digna repo upgrade
```

Detta uppdaterar PostgreSQL-schemat till senaste versionen samtidigt som all befintlig data bevaras.

#### Steg 9: Registrera och starta tjänsten

Den gamla registreringen togs bort i steg 1, så tjänsten registreras på nytt — den här gången med
den körbara filen `digna`, som inte har några batch-filer:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Ge `--address` och `--port` de värden som den gamla tjänsten lyssnade på, om du inte vill ha de nya
standardvärdena `127.0.0.1` och `8000`; de sparas i registreringen och läses inte längre
från `config.toml`. Lägg till `--account` och `--password` om den gamla tjänsten kördes under ett
domänkonto. Se
[Köra digna som Windows-tjänst](#running-digna-as-a-windows-service) för den fullständiga listan
över alternativ.

Om du kör manuellt, starta om servern:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Om du använder IIS eller Tomcat, starta om respektive webbserver.

#### Steg 10: Verifiera uppgraderingen

1. Öppna digna-dashboarden
2. Verifiera att gränssnittet laddar korrekt
3. Kontrollera serverloggarna efter eventuella fel
4. Lägg om varje anslutning som ännu inte använde ODBC till ODBC och testa sedan alla anslutningar
   — se [Testa en anslutning](../../../databases/overview.md#testing-a-connection)