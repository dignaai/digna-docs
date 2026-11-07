---
title: Windows-installationsguide – digna Release 2026.11 | digna Dokumentation
description: Steg-för-steg-guide för att installera digna Release 2026.11 på Windows — systemkrav, PostgreSQL-setup, webbserverkonfiguration, backend- och dashboard-konfiguration, köra digna som Windows-tjänst och uppgradering från Release 2026.06.
keywords: digna windows installation, digna deploymentsguide, digna backend-setup, digna dashboard-installation, postgresql-setup, digna windows-tjänst, digna uppgraderingsguide
image: /assets/logo_square.png
---

# Windows-installationsguide för digna Release 2026.11

**Release:** 2026.11

**Senast uppdaterad:** 7 november 2026


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

### Nytt i Release 2026.11

Denna release lägger till digna Data Reconciliation, digna Agentic med digna MCP Server samt digna Engine, som kan profilera data inuti digna och kontrollera referentiell integritet mellan olika databastekniker. Se [versionsanteckningarna](../../../changelog/Release_202611.md) för fullständiga detaljer.

För en installation medför releasen en ny mekanism för repositorymigreringar, en valfri `[duckdb]`-sektion i `config.toml` för digna Engine och en ny licensfil. [Uppgraderingsavsnittet](#upgrading-to-a-new-release) går igenom var och en av dem.

### Letar du efter macOS eller Linux?

Denna guide täcker Windows. För andra plattformar, se [macOS-installationsguide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) eller [Linux-installationsguide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Databasanslutningar som använder digna Engine som profileringsplats profileras på själva
    digna-värden. Planera för extra minne och diskutrymme för dem, se
    [\[duckdb\]-sektionen](#duckdb-section).

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

!!! info "Sektionen [app] är valfri"

    Från Release 2026.11 kan båda nycklarna, och hela sektionen `[app]`, utelämnas. Det är rätt
    uppsättning när en omvänd proxy serverar dashboarden och backend under samma origin: webbläsaren
    gör då inga cross-origin-förfrågningar, och inga tillåts som standard.

#### Avsnittet [repo]

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
| `DIGNA_REPO_HOST` | `localhost` eller IP | PostgreSQL-serverns hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (standard) | PostgreSQL-port |
| `DIGNA_REPO_DB` | `postgres` | Databasnamn |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schema som skapades tidigare |
| `DIGNA_REPO_USER` | `digna_user` | Användare skapad i PostgreSQL-setupen |
| `DIGNA_REPO_PASSWORD` | Ditt lösenord | Lösenord som sattes när schemat skapades |
| `DIGNA_REPO_SSLMODE` | `prefer` (standard) | Valfri. SSL-läge för PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (standard) | Valfri. Antal anslutningar som digna håller öppna mot repositoryt |

#### Avsnittet [base]

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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 timmar) | Session timeout i sekunder |
| `DIGNA_MAX_WORKERS` | Antal CPU-kärnor - 1 | Antal inspektioner som får köras samtidigt |
| `DIGNA_FRONTEND_BASEURL` | Dashboard-URL | Obligatorisk. Används för länkarna i aviseringsmeddelanden, så det måste vara en URL som mottagarna kan öppna |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (standard) | Valfri. Antal sekunder som en enskild fråga mot en källdatabas får köras innan den avbryts; `0` stänger av tidsgränsen |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (standard) | Valfri. Antal sekunder att vänta på en anslutning till en källdatabas; `0` väntar obegränsat |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` eller `DEBUG` | `INFO` för produktion, `DEBUG` för felsökning. `TRACE`, `WARN` och `ERROR` accepteras också |
| `DIGNA_LOGGING_DIR` | `logs` (standard) | Valfri. Katalog för de roterande loggfilerna, relativt arbetskatalogen |
| `DIGNA_LOGGING_MAX_FILES` | `30` (standard) | Valfri. Antal roterade loggfiler som behålls |

!!! warning "Behåll loggkatalogen när digna körs som tjänst"

    En Windows-tjänst har ingen konsol, så loggfilerna är det enda som visar vad tjänsten
    gör. Sätt inte `DIGNA_LOGGING_DIR` till en tom sträng, eftersom det stänger av loggfilerna.

#### Avsnittet [duckdb] (valfritt) {: #duckdb-section }

Nytt i Release 2026.11. Denna sektion anger resurserna för **digna Engine**, som profilerar
data inuti digna för databasanslutningar vars profileringsplats är **digna Engine**, och som kör
kontroller av referentiell integritet mellan datakällor på olika databasanslutningar. Se
[Profileringsplats](../../../platform/profiling/profiling_location.md).

Sektionen är valfri. Utan den gäller standardvärdena nedan.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Värde | Anteckningar |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (standard) | Minne, i MB, som en körning av digna Engine får använda. Upp till `DIGNA_MAX_WORKERS` körningar kan vara aktiva samtidigt |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Standard: den temporära katalogen för det konto som kör digna (`%TEMP%`) | Katalog för temporära filer när data inte ryms i minnet |

!!! tip "Dimensionera digna Engine"

    Planera för upp till `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` minne på
    digna-värden, utöver det som digna själv använder, och för tillräckligt med ledigt diskutrymme i
    den temporära katalogen för att rymma det största inspekterade datumet bland de datakällor som
    använder digna Engine. Peka `DIGNA_DUCKDB_TEMP_DIRECTORY` mot en disk med det utrymmet, skrivbar
    för det konto som kör digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Du behöver bara denna sektion om minst en databasanslutning använder digna Engine, eller om en
    kontroll av referentiell integritet jämför datakällor på olika anslutningar.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Åtgärda allt som rapporteras som FAILED och kör kommandot igen innan du fortsätter. En WARNING under **Unknown keys** listar nycklar i `config.toml` som digna inte läser; de har ingen effekt, så ta bort dem eller rätta stavningen. Den fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202611.md).

### Steg 3: Initiera repositoryt

1. Öppna Kommandotolken
2. Navigera till din digna-installationskatalog (där `config.toml` och den körbara `digna`-filen finns)
3. Kör anslutningstestet:

```bash
digna repo check
```

På ett nytt schema ansluter kommandot och rapporterar sedan att inget repository är installerat ännu:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Vid det här laget är det det förväntade resultatet: det bekräftar att digna når PostgreSQL och schemat. Ett anslutnings- eller autentiseringsfel pekar i stället på sektionen `[repo]` eller på PostgreSQL-uppsättningen.

### Steg 4: Installera repositoryschemat

I samma katalog, kör:

```bash
digna repo upgrade
```

Detta kommando installerar nödvändiga tabeller i repositoryschemat och avslutas med:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installerar och uppgraderar"

    Från Release 2026.11 installerar `repo upgrade` ett nytt repository och uppgraderar ett befintligt.
    `repo install` fungerar fortfarande som ett annat namn för samma kommando.

### Steg 5: Skapa en admin-användare

Administratörsanvändaren skapas direkt mot repositoryschemat, så servern behöver inte köras ännu. Kör i digna-installationskatalogen:

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

### Steg 6: Starta digna-servern

I digna-installationskatalogen, starta servern med:

```bash
digna serve --address <host> --port <port>
```

**Parametrar:**
- `--address` — Serverns hostname/IP (standard `127.0.0.1`)
- `--port` — Serverns port (standard `8000`)

När servern är igång skriver den ut adressen som den lyssnar på:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Servern upptar terminalen"

    `serve` körs i förgrunden och fortsätter tills du stoppar den med ++ctrl+c++. Låt den vara igång medan du slutför installationen; för att i stället starta den automatiskt vid uppstart, se [Köra digna som Windows-tjänst](#running-digna-as-a-windows-service).

---

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
fullständiga listan över alternativ finns i [CLI-referensen](../../../cli/Command_Line_Interface_202611.md).

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

Detta avsnitt uppgraderar en installation av Release 2026.06 till Release 2026.11. Om din
installation är äldre, läs först [Uppgradera från en release före 2026.06](#upgrading-from-a-release-before-2026-06).

### Innan du uppgraderar

**Det är obligatoriskt att skapa en backup av digna-repositoryt**

Innan du uppgraderar digna, säkerhetskopiera ditt repository (PostgreSQL) för att skydda mot dataförlust.
En backup säkerställer att du kan återställa om uppgraderingen stöter på oväntade problem.

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

Öppna en Kommandotolk som administratör och stoppa tjänsten med den körbara filen `digna` från
din nuvarande installation:

```bash
cd C:\path\to\digna
digna windows stop
```

Tjänsten förblir registrerad. Den nya körbara filen tar den gamlas plats i samma katalog, så
registreringen pekar fortfarande på rätt fil.

Om digna körs i förgrunden, tryck ++ctrl+c++ i dess Kommandotolksfönster.

!!! warning "Uppgradera från en release före 2026.06"

    Releaser före 2026.06 registrerade tjänsten med batchfiler. Stoppa och avregistrera den med
    batchfilerna från din nuvarande installation, **innan** du byter namn på något i steg 2:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Anteckna vilket konto tjänsten kördes under, samt vilken adress och port den lyssnade på. Du
    registrerar tjänsten igen i steg 9.

#### Steg 2: Säkerhetskopiera nuvarande installation {: #step-2-backup-current-installation }

Byt namn på den körbara filen och dashboard-mappen i din nuvarande installation i
digna-installationskatalogen, så att den nya releasen kan distribueras vid sidan av dem:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Behåll `digna_old.exe` tills du har verifierat uppgraderingen, och `dashboard_old` tills du har återställt
dina konfigurationsfiler från den (se steg 4). Därefter kan du ta bort båda.

!!! info "Uppgradera från en release före 2026.06"

    Byt namn på mapparna `dignabackend` och `dignacli` i stället för den körbara filen:
    `ren dignabackend dignabackend_old` och `ren dignacli dignacli_old`. Release 2026.11 använder ingen av mapparna, och inte heller mappen `bin` med batchfiler.

#### Steg 3: Packa upp och distribuera ny version {: #step-3-extract-and-deploy-new-version }

1. Packa upp den nya digna-installations-ZIP-filen
2. Kopiera den nya körbara filen `digna` och mappen `dashboard` till din installationskatalog

!!! warning "Varning"

    Varken `config.toml` eller `dashboard/dashboard_config.toml` ingår någonsin i
    installations-ZIP:en — digna-teamet levererar aldrig någon av filerna. Din befintliga konfiguration
    påverkas därför inte av uppgraderingen, och kopiorna i de omdöpta `*_old`-mapparna är de
    enda du har.

#### Steg 4: Återställ dina konfigurationsfiler {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
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
och ladda sedan om sidan med en hård uppdatering (++ctrl+f5++).

#### Steg 6: Validera konfigurationen {: #step-6-validate-the-configuration }

Kontrollera att `config.toml` är fullständig innan du rör repositoryt:

```bash
digna config check
```

Varje sektion måste rapportera OK. Åtgärda allt som rapporteras som FAILED, ta bort nycklarna som listas
under **Unknown keys** och kör kommandot igen innan du fortsätter.

#### Steg 7: Ersätt licensfilen {: #step-7-replace-the-license-file }

En licensfil följer normalt med från en release till nästa. Release 2026.11 är ett
undantag: den lägger till två licensierade moduler, digna Data Reconciliation och digna Agentic, och en
licens som utfärdats före 2026.11 innehåller dem inte. Kopiera den `license.toml` som digna-teamet
tillhandahållit för Release 2026.11 till installationskatalogen och ersätt den gamla:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Behåll inte den tidigare licensen"

    Med den tidigare licensen startar digna fortfarande, men digna Data Reconciliation och digna
    MCP Server förblir avstängda. Varje kommando som kontrollerar licensen — `user`,
    `inspection`, `repo` — avbryts innan det rör repositoryt när kontrollen misslyckas. Verifiera
    den nya licensen innan du går vidare:

    ```bash
    digna license check
    ```

#### Steg 8: Uppgradera repositoryschemat {: #step-8-upgrade-the-repository-schema }

Kör i din digna-installationskatalog:

```bash
digna repo upgrade
```

Release 2026.11 hanterar repositoryschemat med versionerade migreringar. Den första uppgraderingen från
en tidigare release för schemat till den sista versionen av det tidigare systemet, registrerar den som
utgångspunkt och tillämpar sedan migreringarna i Release 2026.11. Den avslutas med:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

All befintlig data bevaras. För att när som helst se repositoryts tillstånd, kör
`digna repo check`: det listar den senast tillämpade migreringen och eventuella väntande migreringar.

!!! warning "digna startar inte på ett föråldrat repository"

    Från Release 2026.11 vägrar servern att starta så länge repositoryt behöver uppgraderas, och
    säger det, till exempel:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Kör `repo upgrade` innan du startar servern eller tjänsten.

#### Steg 9: Starta om tjänsterna {: #step-9-restart-services }

Om digna körs som Windows-tjänst, starta den igen:

```bash
cd C:\path\to\digna
digna windows start
```

Om du uppgraderade från en release före 2026.06 och avregistrerade tjänsten i steg 1, registrera
den först igen med den körbara filen `digna`:

```bash
digna windows install --address <address> --port <port>
digna windows start
```

Ge `--address` och `--port` de värden som den gamla tjänsten lyssnade på, om du inte vill använda
standardvärdena `127.0.0.1` och `8000`. Lägg till `--account` och `--password` om den gamla tjänsten
kördes under ett domänkonto. Se
[Köra digna som Windows-tjänst](#running-digna-as-a-windows-service) för den fullständiga listan över
alternativ.

Om du kör manuellt, starta servern igen:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Om du använder IIS eller Tomcat, starta om respektive webbserver.

#### Steg 10: Verifiera uppgraderingen {: #step-10-verify-the-upgrade }

1. Bekräfta releasen för den nya körbara filen:

    ```bash
    digna version
    ```

    Första raden måste vara `Release: 2026.11`.

2. Öppna digna-dashboarden och kontrollera att gränssnittet laddas korrekt.
3. Kontrollera filerna i installationens katalog `logs` efter fel.
4. Testa dina databasanslutningar — se
   [Testa en anslutning](../../../databases/overview.md#testing-a-connection). Efter en uppgradering
   från en release före 2026.06, lägg först om varje anslutning som inte redan använde ODBC till
   ODBC.

För att komma igång med de nya modulerna, se [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Ansluta en AI-agent](../../../platform/agentic/connect_ai_agent.md) för digna MCP Server och
[Profileringsplats](../../../platform/profiling/profiling_location.md) för digna Engine.
