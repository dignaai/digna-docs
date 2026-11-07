# Windows instalācijas ceļvedis digna Release 2026.11

**Izlaidums:** 2026.11

**Pēdējais atjauninājums:** 2026. gada 7. novembris


---

## Saturs

1. [Ievads](#introduction)
2. [Sistēmas prasības](#system-requirements)
3. [Priekšinstalācijas sagatavošana](#pre-installation-setup)
4. [PostgreSQL servera iestatīšana](#postgresql-server-setup)
5. [Tīmekļa servera konfigurācija](#web-server-configuration)
6. [Sākotnējā instalācija](#initial-installation)
7. [Backend konfigurācija](#backend-configuration)
8. [Paneļa konfigurācija](#dashboard-configuration)
9. [digna palaide kā Windows serviss](#running-digna-as-a-windows-service)
10. [Jaunināšana uz jaunu izlaidumu](#upgrading-to-a-new-release)

---

## Ievads {: #introduction }

### Par digna

digna ir visaptveroša ar mākslīgo intelektu balstīta platforma, kas paredzēta datu kvalitātes pārvaldības optimizēšanai dažādās datu vidēs, piemēram, noliktavās, ezeros un lakehouse risinājumos. Izstrādāta kā mērogojama un pielāgojama sistēma, digna risina mūsdienu datu izaicinājumus, izmantojot automatizāciju, reāllaika uzraudzību un anomāliju atklāšanu.

digna sastāv no divām galvenajām komponentēm:

- **digna**: lietojumprogrammas kodols, kas atbild par datu apstrādi un kvalitātes pārbaužu veikšanu. Tas apvieno aizmuguri un komandrindas saskarni vienā izpildāmajā failā un aizstāj iepriekšējo laidienu atsevišķās programmas `dignabackend` un `dignacli`.
- **dignadashboard**: tīmekļa saskarne, kas izvietota uz tīmekļa servera un nodrošina lietotājam draudzīgu veidu, kā mijiedarboties ar digna platformu un vizualizēt datu kvalitātes metrikas.

### Kas jauns izlaidumā 2026.11

Šis izlaidums pievieno digna Data Reconciliation, digna Agentic ar digna MCP Server un digna Engine, kas var profilēt datus pašā digna un pārbaudīt referenciālo integritāti starp dažādām datubāzu tehnoloģijām. Pilnas detaļas skatiet [izlaiduma piezīmēs](../../../changelog/Release_202611.md).

Instalācijai šis izlaidums ievieš jaunu repozitorija migrāciju mehānismu, neobligātu `[duckdb]` sadaļu failā `config.toml` digna Engine vajadzībām un jaunu licences failu. Katrs no tiem ir aprakstīts [jaunināšanas sadaļā](#upgrading-to-a-new-release).

### Meklējat macOS vai Linux?

Šis ceļvedis attiecas uz Windows. Citu platformu instalācijas skaidrojumu skatiet [macOS instalācijas ceļvedī](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) vai [Linux instalācijas ceļvedī](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Sistēmas prasības {: #system-requirements }

Pirms instalācijas pārliecinieties, ka jūsu sistēma atbilst šādām minimālajām prasībām:

| Prasība | Specifikācija |
|---|---|
| **Operētājsistēma** | Windows Server vai Windows 10/11 |
| **Atmiņa (minimālā konfigurācija)** | 16 GB RAM |
| **Diskā nepieciešamā vieta** | 10 GB brīvas vietas |
| **Datubāze** | PostgreSQL Server 12 vai jaunāks |
| **Tīmekļa serveris** | IIS, Apache Tomcat vai ekvivalents |

!!! info "digna Engine"

    Datubāzes savienojumi, kuru profilēšanas vieta ir digna Engine, tiek profilēti pašā digna resursdatorā. Paredziet tiem papildu atmiņu un diska vietu, skatiet [\[duckdb\] sadaļu](#duckdb-section).

### Datubāzes instalācijas iespējas

**Ja PostgreSQL jau ir instalēts:**
Jūs varat pievienot jaunu datubāzi digna esošajam PostgreSQL serverim.

**Ja instalējat PostgreSQL uz tā paša datora kā digna:**

!!! info "Ieteicamās specifikācijas"

    - **Atmiņa**: 32 GB RAM (nevis 16 GB)
    - **Diskā nepieciešamā vieta**: 50 GB brīvas vietas (nevis 10 GB)

    Šīs augstākās specifikācijas nodrošina pietiekamus resursus vienlaicīgai digna un PostgreSQL datubāzes darbībai.

---

## Priekšinstalācijas sagatavošana {: #pre-installation-setup }

Pirms digna instalēšanas pārliecinieties, ka ir izpildīti divi galvenie priekšnosacījumi:

1. **PostgreSQL Server** – aprēķināto metrikas un veiktspējas datu glabāšanai
2. **Tīmekļa serveris** – digna paneļa izvietošanai

Ja šīs sastāvdaļas vēl nav iestatītas, izpildiet tālāk norādītās sadaļas, lai tās instalētu un konfigurētu.

---

## PostgreSQL servera iestatīšana {: #postgresql-server-setup }

### Ja PostgreSQL jau ir pieejams

Ja PostgreSQL jau ir instalēts un darbojas uz jūsu lokālā datora vai ja izmantojat pārvaldītu attālo PostgreSQL serveri, varat pāriet uz [nākamo sadaļu](#web-server-configuration).

### PostgreSQL instalēšana

Izpildiet šos soļus, lai instalētu PostgreSQL uz Windows:

#### 1. solis: Lejupielādēt PostgreSQL

1. Apmeklējiet [PostgreSQL lejupielādes lapu](https://www.postgresql.org/download/)
2. Izvēlieties **Windows**
3. Lejupielādējiet jaunāko instalatoru

#### 2. solis: Palaist instalatoru

1. Veiciet dubultklikšķi uz lejupielādētā instalatora faila
2. Sekojiet norādījumiem instalācijas vednī

#### 3. solis: Izvēlēties instalācijas direktoriju

Izvēlieties mapi, kur PostgreSQL tiks instalēts. Parasti noklusējuma atrašanās vieta ir piemērota.

#### 4. solis: Izvēlēties komponentes

Standarta uzstādīšanai atstājiet noklusējuma komponentes atlasītas.

#### 5. solis: Iestatīt PostgreSQL superlietotāja paroli

Ievadiet un apstipriniet paroli PostgreSQL superlietotājam (`postgres`). **Saglabājiet šo paroli drošā vietā** — tā būs nepieciešama vēlāk.

#### 6. solis: Konfigurēt porta numuru

Noklusējuma PostgreSQL ports ir `5432`. Varat izmantot noklusējumu vai norādīt citu portu pēc vajadzības.

!!! tip "Padoms"

    Ja ports 5432 jau ir aizņemts, izvēlieties citu portu un atcerieties to turpmākajai konfigurācijai.

#### 7. solis: Izvēlēties lokalizāciju

Izvēlieties datubāzes lokalizāciju. Parasti noklusējums ir piemērots lielākajai daļai instalāciju.

#### 8. solis: Pabeigt instalāciju

Noklikšķiniet **Next** cauri atlikušajiem soļiem, pēc tam noklikšķiniet **Finish**.

#### 9. solis: Pārbaudīt instalāciju

Atveriet Command Prompt un pārbaudiet, vai PostgreSQL ir instalēts:

```bash
psql --version
```

Ja instalācija bija veiksmīga, tiks parādīta PostgreSQL versija.

---

## Tīmekļa servera konfigurācija {: #web-server-configuration }

digna prasa tīmekļa serveri paneļa izvietošanai. Izvēlieties vienu no šīm iespējām:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Nepieciešams instalēt un konfigurēt tikai vienu no šiem serveriem.

### IIS iestatīšana {: #iis-setup }

#### Pārskats

Internet Information Services (IIS) ir Microsoft tīmekļa serveris vietņu un tīmekļa lietotņu mitināšanai.

#### IIS ieslēgšana

1. **Atveriet Vadības paneli**
   - Nospiediet `Win + R`
   - Ierakstiet `control` un nospiediet Enter

2. **Pārejiet uz Windows funkcijām**
   - Noklikšķiniet **Programs**
   - Izvēlieties **Turn Windows features on or off**

3. **Ieslēdziet Internet Information Services**
   - Ritiniet un atrodiet **Internet Information Services (IIS)**
   - Atzīmējiet izvēles rūtiņu, lai to ieslēgtu
   - Noklikšķiniet uz **+**, lai izvērstu un pārbaudītu, vai ir atlasītas šādas apakškomponentes:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Noklikšķiniet OK**, lai piemērotu izmaiņas

5. **Pārbaudīt IIS instalāciju**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost`
   - Jums jāredz IIS sveiciena lapa

#### Obligāti: URL Rewrite modulis

IIS prasa URL Rewrite komponenti. Lejupielādējiet un instalējiet to no [oficiālās Microsoft lapas](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obligāti: MIME tips Markdown failiem

Lai nodrošinātu, ka Markdown faili (`.md`) tiek pareizi servēti ar IIS:

1. Atveriet **IIS Manager** (nospiediet `Win + R`, ierakstiet `inetmgr`, nospiediet Enter)
2. Pārejiet uz **Your Site > MIME Types**
3. Noklikšķiniet **Add...**
4. Konfigurējiet:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Svarīgi"

    Bez šī iestatījuma `.md` faili var netikt pareizi servēti.

---

### Apache Tomcat iestatīšana {: #apache-tomcat-setup }

#### Pārskats

Apache Tomcat ir atvērtā koda Java servleta konteiners un tīmekļa serveris.

#### Instalēšana

1. **Lejupielādēt Apache Tomcat**
   - Apmeklējiet [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Lejupielādējiet Windows ZIP izplatījumu

2. **Izpakot arhīvu**
   - Izpakojiet ZIP failu direktorijā uz jūsu sistēmas
   - Piemērs: `C:\Program Files\Apache Tomcat`

3. **Pārbaudīt, vai Tomcat darbojas**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost:8080`
   - Jums jāredz Apache Tomcat sveiciena lapa

!!! tip "Padoms"

    Apache Tomcat parasti sāk darboties automātiski pēc instalācijas. Ja tas nenotiek, atveriet `bin` mapi un palaidiet `startup.bat`.

---

## Sākotnējā instalācija {: #initial-installation }

### 1. solis: Iestatīt digna repozitoriju

digna repozitorijs glabā visas ar digna aprēķinātās metrikas. Tas darbojas kā centrālā datubāze analītiskajiem un veiktspējas datiem.

#### Izveidot repozitorija shēmu un lietotāju

Atveriet savu PostgreSQL klientu (pgAdmin, psql vai līdzīgu) un izpildiet šādas SQL komandas:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Aizvietojiet šādus aizstājējvārdus:**

- `<digna_repo_schema>` — Vēlamais shēmas nosaukums (piem., `dignarepo`)
- `<digna_repo_user>` — Vēlamais lietotājvārds (piem., `digna_user`)
- `<digna_repo_password>` — Droša parole šim lietotājam

**Piemērs:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Laba prakse"

    Lietojiet stipras, sarežģītas paroles datubāzes lietotājiem. Izvairieties no viegli uzminamiem akreditācijas datiem.

---

### 2. solis: Izpakot digna instalācijas pakotni

1. Atrodiet jums nodoto digna instalācijas ZIP failu
2. Izpakojiet to vēlamajā instalācijas vietā
3. Pēc izpakošanas jums jāredz sekojošas vienības:
   - `dashboard/` — tīmekļa paneļa saskarne
   - `digna` — galvenais izpildāmais fails (backend + CLI apvienots)

!!! info "Konfigurācijas un licences faili pakotnē nav iekļauti"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` instalācijā nav iekļauts — abus jūs
    izveidojat paši sadaļās [Backend konfigurācija](#backend-configuration) un
    [Paneļa konfigurācija](#dashboard-configuration). Arī `license.toml` nav iekļauts;
    digna to nodrošina atsevišķi, kā aprakstīts 3. solī.

### 3. solis: Instalēt licences failu

!!! warning "Svarīgi"

    Licences fails **nav** iekļauts instalācijas paketē un tiks nodrošināts atsevišķi no digna.

1. Atrodiet jums nodoto `license.toml` failu
2. Kopējiet to uz digna instalācijas saknes direktoriju (tur, kur atrodas `config.toml` un izpildāmais `digna`)

**Kāpēc tas ir svarīgi:**
Licences fails satur jūsu klienta informāciju, licences derīguma termiņu un digitālo parakstu. **Nemainiet šo failu** — jebkuras izmaiņas to inaktivizēs.

**Direktorijas struktūra pēc iestatīšanas:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend konfigurācija {: #backend-configuration }

### 1. solis: Izveidot un rediģēt konfigurācijas failu

`config_template.toml` fails ir iekļauts jūsu digna instalācijas direktorijā. Pietiek to pārdēvēt par `config.toml`.

**Atrašanās vieta:** `digna_installation/config.toml`

Atveriet `config.toml` teksta redaktorā un konfigurējiet katru sadaļu zemāk.

#### [app] sadaļa

Šī sadaļa konfigurē starpizcelsmju resursu koplietošanu (CORS) starp paneli un backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Paneļa URL | URL, no kuriem tiek pasniegts panelis. Pārlūkprogrammas pieprasījumi no jebkuras citas izcelsmes tiek noraidīti |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obligāts, lai pārlūkprogramma ar katru pieprasījumu nosūtītu sesijas sīkfailu |

!!! info "[app] sadaļa nav obligāta"

    Sākot ar Release 2026.11, abas atslēgas un visu `[app]` sadaļu var izlaist. Tas ir pareizais iestatījums, ja apgrieztais starpniekserveris (reverse proxy) pasniedz paneli un backend ar vienu izcelsmi: tad pārlūkprogramma neveic starpizcelsmju pieprasījumus, un pēc noklusējuma neviens netiek atļauts.

#### [repo] sadaļa

Šī sadaļa konfigurē savienojumu ar PostgreSQL datubāzi:

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

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` vai IP | PostgreSQL servera hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (noklusējums) | PostgreSQL ports |
| `DIGNA_REPO_DB` | `postgres` | Datubāzes nosaukums |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Iepriekš izveidotā shēma |
| `DIGNA_REPO_USER` | `digna_user` | Lietotājs izveidots PostgreSQL iestatīšanā |
| `DIGNA_REPO_PASSWORD` | Jūsu parole | Parole, iestatīta shēmas izveidē |
| `DIGNA_REPO_SSLMODE` | `prefer` (noklusējums) | Neobligāts. PostgreSQL SSL režīms: `disable`, `allow`, `prefer`, `require`, `verify-ca` vai `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (noklusējums) | Neobligāts. Savienojumu skaits, ko digna uztur atvērtus ar repozitoriju |

#### [base] sadaļa

Šī sadaļa satur drošības, sīkfailu un inspekciju iestatījumus:

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

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_FERNET_KEY` | Iepriekš parādītā vērtība | Iepriekšējo laidienu izmantotās šifrēšanas atslēga. Tai jābūt norādītai; saglabājiet parādīto vērtību |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Resursdators, kurā panelis ir sasniedzams. `""` neiestata domēnu, kas ir pareizi aiz starpniekservera, kurš pasniedz paneli un backend ar vienu izcelsmi |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Jābūt `true` vienmēr, kad digna tiek pasniegta caur HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Neļauj skriptiem piekļūt sesijas sīkfailam |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 stundas) | Sesijas derīguma laiks sekundēs |
| `DIGNA_MAX_WORKERS` | Skaitlis: CPU kodolu skaits - 1 | Inspekciju skaits, kas drīkst darboties vienlaikus |
| `DIGNA_FRONTEND_BASEURL` | Paneļa URL | Obligāts. Tiek izmantots saitēm paziņojumu ziņojumos, tāpēc tam jābūt URL, ko adresāti var atvērt |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (noklusējums) | Neobligāts. Sekundes, cik ilgi viens vaicājums avota datubāzē drīkst darboties, pirms tas tiek pārtraukts; `0` atslēdz noildzi |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (noklusējums) | Neobligāts. Sekundes, cik ilgi gaidīt savienojumu ar avota datubāzi; `0` gaida bez ierobežojuma |

#### [encryption] sadaļa

Šajā sadaļā ir atslēga, ar kuru tiek šifrētas repozitorijā glabātās sensitīvās vērtības. Tā ir **obligāta** — `config check` ziņo par sadaļu `[encryption]` kā FAILED, ja atslēgas trūkst.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 kodēta atslēga | Šifrē sensitīvās vērtības, kas glabājas digna repozitorijā |

!!! warning "Aizsargājiet config.toml"

    Šī atslēga ir fiksēta vērtība, kas ir vienāda visās digna instalācijās, un tieši tā atkodē jūsu repozitorija sensitīvās vērtības. Ierobežojiet piekļuvi `config.toml` līdz kontam, ar kuru darbojas digna, glabājiet failu ārpus versiju kontroles un koplietojamiem diskiem un izslēdziet to no jebkuras dublējuma kopijas, kas tiek glabāta mazāk droši nekā pats repozitorijs.

#### [logging] sadaļa

Šī sadaļa konfigurē žurnālu (logu) uzvedību:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` vai `DEBUG` | `INFO` produkcijai, `DEBUG` problēmu novēršanai. Tiek pieņemti arī `TRACE`, `WARN` un `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (noklusējums) | Neobligāts. Direktorija rotējošajiem žurnālfailiem, relatīvi pret darba direktoriju |
| `DIGNA_LOGGING_MAX_FILES` | `30` (noklusējums) | Neobligāts. Saglabājamo rotēto žurnālfailu skaits |

!!! warning "Saglabājiet žurnālu direktoriju, ja digna darbojas kā serviss"

    Windows servisam nav konsoles, tāpēc žurnālfaili ir vienīgais pieraksts par to, ko serviss dara. Neiestatiet `DIGNA_LOGGING_DIR` uz tukšu virkni, jo tas izslēdz žurnālfailus.

#### [duckdb] sadaļa (neobligāta) {: #duckdb-section }

Jaunums Release 2026.11. Šī sadaļa nosaka **digna Engine** resursus. digna Engine profilē datus pašā digna tiem datubāzes savienojumiem, kuru profilēšanas vieta ir **digna Engine**, un veic referenciālās integritātes pārbaudes starp datu avotiem dažādos datubāzes savienojumos. Skatiet [Profilēšanas vieta](../../../platform/profiling/profiling_location.md).

Sadaļa nav obligāta. Bez tās tiek lietotas tālāk norādītās noklusējuma vērtības.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (noklusējums) | Atmiņa MB, ko drīkst izmantot viena digna Engine izpilde. Vienlaikus var būt aktīvas līdz `DIGNA_MAX_WORKERS` izpildēm |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Noklusējums: tā konta pagaidu direktorija, ar kuru darbojas digna (`%TEMP%`) | Direktorija pagaidu failiem, ja dati neietilpst atmiņā |

!!! tip "digna Engine izmēra plānošana"

    Paredziet digna resursdatorā līdz `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` atmiņas papildus tai, ko izmanto pati digna, un pagaidu direktorijā pietiekami daudz brīvas diska vietas, lai tajā ietilptu lielākais inspicētais datums no datu avotiem, kas izmanto digna Engine. Norādiet `DIGNA_DUCKDB_TEMP_DIRECTORY` uz disku ar šādu brīvu vietu, kurā var rakstīt konts, ar kuru darbojas digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Šī sadaļa jums ir vajadzīga tikai tad, ja vismaz viens datubāzes savienojums izmanto digna Engine vai ja referenciālās integritātes pārbaude salīdzina datu avotus dažādos savienojumos.

---

### 2. solis: Parbaudiet konfigurāciju

Pirms repozitorija inicializēšanas pārbaudiet, vai `config.toml` ir pilnīgs un pareizi veidots. Savā digna instalācijas direktorijā palaidiet:

```bash
digna config check
```

Katra sadaļa tiek pārbaudīta atsevišķi, tāpēc viena kļūda neaizsedz pārējo stāvokli:

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

Izlabojiet visu, kas ziņots kā FAILED, un pirms turpināšanas palaidiet komandu vēlreiz. WARNING sadaļā **Unknown keys** uzskaita atslēgas failā `config.toml`, kuras digna nenolasa; tām nav nekādas ietekmes, tāpēc noņemiet tās vai izlabojiet to rakstību. Pilns opciju saraksts ir [CLI atsaucē](../../../cli/Command_Line_Interface_202611.md).

### 3. solis: Inicializēt repozitoriju

1. Atveriet Command Prompt
2. Pārejiet uz jūsu digna instalācijas direktoriju (tur, kur atrodas `config.toml` un izpildāmais `digna`)
3. Palaidiet savienojuma pārbaudi:

```bash
digna repo check
```

Jaunā shēmā komanda izveido savienojumu un pēc tam ziņo, ka repozitorijs vēl nav instalēts:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Šajā brīdī tas ir sagaidāmais rezultāts: tas apstiprina, ka digna sasniedz PostgreSQL un shēmu. Savukārt savienojuma vai autentifikācijas kļūda norāda uz `[repo]` sadaļu vai PostgreSQL iestatīšanu.

### 4. solis: Instalēt repozitorija shēmu

Tajā pašā direktorijā palaidiet:

```bash
digna repo upgrade
```

Šī komanda instalē nepieciešamās tabulas repozitorija shēmā un beidzas ar:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instalē un jaunina"

    Sākot ar Release 2026.11, `repo upgrade` instalē jaunu repozitoriju un jaunina esošu. `repo install` joprojām darbojas kā tās pašas komandas cits nosaukums.

### 5. solis: Izveidot administratora lietotāju

1. Atveriet **jaunu** Command Prompt logu
2. Pārejiet uz jūsu digna instalācijas direktoriju
3. Palaidiet šādu komandu, lai izveidotu administratora lietotāju:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Piemērs:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Šī komanda izveido lietotāju ar pilnām administratīvām tiesībām.

!!! tip "Laba prakse"

    Izmantojiet stipru paroli ar lielajiem un maziem burtiem, cipariem un speciālajām zīmēm.

---

### 6. solis: Palaist digna serveri

Digna instalācijas direktorijā palaidiet serveri ar:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — servera hostname/IP (noklusējums `127.0.0.1`)
- `--port` — servera ports (noklusējums `8000`)

Kad serveris ir palaists, tas izvada adresi, kurā tas klausās:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Serveris aizņem termināli"

    `serve` darbojas priekšplānā un turpina, līdz to apturat ar ++ctrl+c++. Atstājiet to darbojamies, kamēr pabeidzat iestatīšanu; lai to automātiski palaistu sistēmas startēšanas laikā, skatiet [digna palaišana kā Windows pakalpojuma](#running-digna-as-a-windows-service).

---

## Paneļa konfigurācija {: #dashboard-configuration }

### 1. solis: Izvietot paneli uz tīmekļa servera

digna panelis savu konfigurāciju nolasa no faila `dashboard/dashboard_config.toml`. Šis fails instalācijā nav iekļauts — jūs to izveidojat `dashboard/` direktorijā līdzās paneļa failiem.

Tā saturs ir aprakstīts sadaļā [Vienotā pieteikšanās (SSO)](../../../sso/overview.md), kur šis fails arī ir nepieciešams: tajā ir panelī piedāvātās pieteikšanās iespējas un, daudzinstanču izvietošanai, backend savienojums.

Izvēlieties jūsu tīmekļa serveri un izpildiet atbilstošos izvietošanas soļus.

#### Izvietošana uz IIS

1. **Atveriet IIS Manager**
   - Nospiediet `Win + R`, ierakstiet `inetmgr`, nospiediet Enter

2. **Izveidot jaunu vietni**
   - Kreisajā panelī ar peles labo pogu klikšķiniet uz **Sites**
   - Izvēlieties **Add Website...**

3. **Konfigurēt vietni**
   - **Site Name**: Ievadiet nosaukumu (piem., "dignaDashboard")
   - **Physical Path**: Noklikšķiniet Browse un izvēlieties jūsu `dashboard` mapi
   - **Binding**: Iestatiet IP adresi un portu (noklusējuma ports HTTP — 80, HTTPS — 443)

4. **Startēt vietni**
   - Noklikšķiniet **OK**, lai izveidotu vietni
   - Ar peles labo pogu klikšķiniet uz jaunizveidotās vietnes un izvēlieties **Start**

5. **Pārbaudīt instalāciju**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost` (vai jūsu konfigurēto URL)
   - Jums jāredz digna paneļa pieteikšanās lapa

#### Izvietošana uz Apache Tomcat

1. **Kopēt paneli uz Tomcat**
   - Nokopējiet `dashboard` mapi uz jūsu Tomcat `webapps` direktoriju
   - Pārdēvējiet to pēc vajadzības (piem., uz `digna`)
   - Piemērs: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Pārbaudīt izvietojumu**
   - Atsvaidziniet vai ielādējiet Tomcat pārvaldības lapu (http://localhost:8080)
   - Jums jāredz "digna" (vai jūsu izvēlētais nosaukums) sarakstā ar izvietotajām lietotnēm

3. **Piekļūt panelim**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost:8080/digna`
   - Jums jāredz digna paneļa pieteikšanās lapa

---

## digna palaide kā Windows serviss {: #running-digna-as-a-windows-service }

### Kāpēc izmantot Windows servisu?

digna backend darbināšana kā Windows serviss nodrošina, ka tas:
- Automātiski startējas sistēmas boot laikā
- Darbojas fonā bez atvērtas Command Prompt loga
- Automātiski restartējas, ja notiek avārija
- To var pārvaldīt caur Windows Services rīku

### Komandas `windows`

Servisu pārvalda pats izpildāmais fails `digna`, izmantojot apakškomandas `digna windows`.
Nekādi batch faili nav jāpalaiž.

| Komanda | Mērķis |
|---|---|
| `digna windows install` | Reģistrē digna kā Windows servisu |
| `digna windows start` | Palaiž reģistrēto servisu |
| `digna windows stop` | Aptur darbojošos servisu |
| `digna windows uninstall` | Atreģistrē servisu |

!!! warning "Nepieciešamas administratīvās tiesības"

    Visas četras komandas jāpalaiž no Command Prompt, kas atvērts kā administrators.

Katra komanda pieņem `--name`, lai vērstos pie servisa, kas reģistrēts ar nenoklusējuma nosaukumu. Pilns
opciju saraksts ir [CLI rokasgrāmatā](../../../cli/Command_Line_Interface_202611.md).

### Servisa instalēšana

1. **Atveriet Command Prompt kā administrators**
   - Ar peles labo pogu klikšķiniet uz Command Prompt
   - Izvēlieties "Run as Administrator"

2. **Pārejiet uz savu digna instalācijas direktoriju**
   ```bash
   cd C:\path\to\digna
   ```

3. **Reģistrējiet servisu**
   ```bash
   digna windows install
   ```

!!! important "Norādiet adresi un portu, ja vien noklusējuma vērtības jums neder"

    `install` ieraksta adresi un portu servisa reģistrācijā, un serviss piesaistās tieši
    ierakstītajām vērtībām. Noklusējuma vērtības ir `127.0.0.1` un `8000`, kas pieņem savienojumus
    tikai no pašas mašīnas. Panelis citā resursdatorā tām nevar piekļūt, tāpēc norādiet adresi,
    kurā backend jāklausās:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Šīs vērtības netiek nolasītas no `config.toml`. Lai tās vēlāk mainītu, atinstalējiet servisu un
    instalējiet to vēlreiz ar jaunajām vērtībām.

Serviss tiek reģistrēts ar **automātisku startēšanu**, tāpēc tas startēsies kopā ar Windows. Tas
netiek palaists uzreiz — skatiet nākamo sadaļu.

#### Instalēšanas opcijas

| Opcija | Noklusējums | Mērķis |
|---|---|---|
| `--name` | `digna` | Nosaukums, ar kādu reģistrēt servisu |
| `--display-name` | `digna` | Nosaukums, kas tiek rādīts services.msc |
| `--description` | `digna data quality backend` | Apraksts, kas tiek rādīts services.msc |
| `--address` | `127.0.0.1` | Adrese, kurai serviss piesaista savu API |
| `--port` | `8000` | Ports, kuram serviss piesaista savu API |
| `--working-dir` | izpildāmā faila `digna` direktorija | Direktorija, kurā atrodas `config.toml` un `license.toml` un kuru serviss izmanto kā darba direktoriju |
| `--start-type` | `auto` | `auto` startējas kopā ar Windows, `manual` startējas tikai pēc pieprasījuma, `disabled` reģistrē servisu, taču atsakās to startēt |
| `--account` | `LocalSystem` | Konts, ar kuru darbināt servisu, piem., `DOMAIN\user` vai `.\user` |
| `--password` | | `--account` parole |

!!! tip "Darbināšana ar domēna kontu"

    `LocalSystem` nav tīkla identitātes, tāpēc Windows autentifikācija pret SQL Server un jebkāda
    piekļuve tīkla koplietojumam neizdosies. Instalējiet ar `--account` un `--password`, ja servisam
    resursiem jāpiekļūst kā konkrētam lietotājam.

### Servisa palaišana un apturēšana

#### Lai palaistu servisu

```bash
digna windows start
```

#### Lai apturētu servisu

```bash
digna windows stop
```

!!! tip "Padoms"

    Vienmēr apturiet servisu, pirms atjaunināt lietojumprogrammas failus.

### Pārvietot servisu uz jaunu direktoriju

Ja nepieciešams pārvietot digna instalāciju:

1. **Apturēt un atreģistrēt esošo servisu**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Pārvietot aplikācijas failus**
   - Pārvietojiet visu digna instalācijas mapi uz jauno atrašanās vietu

3. **Reģistrēt servisu no jauna no jaunās atrašanās vietas**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Atkārtojiet visas `--address`, `--port` vai `--account` vērtības, ko izmantojāt pirmajā reizē — iepriekšējā
   reģistrācija vairs nepastāv.

4. **Palaist servisu**
   ```bash
   digna windows start
   ```

### Servisa atinstalēšana

1. **Apturēt darbojošos servisu**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Atreģistrēt servisu**
   ```bash
   digna windows uninstall
   ```

digna serveris tagad vairs nav reģistrēts kā Windows serviss.

---

## Jaunināšana uz jaunu izlaidumu {: #upgrading-to-a-new-release }

Šajā sadaļā aprakstīta Release 2026.06 instalācijas jaunināšana uz Release 2026.11. Ja jūsu instalācija ir vecāka, vispirms izlasiet [Jaunināšana no laidiena, kas vecāks par 2026.06](#upgrading-from-a-release-before-2026-06).

### Pirms jaunināšanas

**Repozitārija (PostgreSQL) rezerves kopijas izveide ir obligāta**

Pirms digna jaunināšanas veiciet rezerves kopiju sava repozitorija (PostgreSQL), lai izvairītos no datu zuduma. Rezerves kopija nodrošina atjaunošanas iespēju, ja jaunināšanas laikā rodas neparedzētas problēmas.

**Licences faila pieprasīšana Release 2026.11**

Release 2026.11 nepieciešams jauns `license.toml`. Pieprasiet to digna komandai pirms darba sākšanas un sagatavojiet to [7. solim](#step-7-replace-the-license-file).

### Jaunināšana no laidiena, kas vecāks par 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 ieviesa trīs izmaiņas, kas joprojām ir spēkā, ja vecāku instalāciju jaunina tieši uz 2026.11:

- **Tikai ODBC.** digna katru avota tehnoloģiju sasniedz caur ODBC. Katrs datubāzes savienojums, kas vēl neizmanto ODBC, pēc jaunināšanas jāpārceļ uz ODBC; automātiskas konvertēšanas nav. Iepriekš instalējiet ODBC draiverus digna resursdatorā, skatiet [ODBC draivera instalēšana digna resursdatorā](../../../databases/overview.md#install-the-driver), un sagatavojiet katra savienojuma īpašības no [tehnoloģiju rokasgrāmatām](../../../databases/overview.md#technology-guides). Databricks Legacy savienotājs vairs nepastāv; pārceliet šos savienojumus uz [Databricks](../../../databases/databricks_connector_guide.md) savienotāju.
- **Viens izpildāmais fails.** `dignabackend` un `dignacli` aizstāj viens izpildāmais fails `digna`, kas apvieno backend un CLI.
- **config.toml.** Sadaļa `[encryption]` ir obligāta, un `DIGNA_APP_HOST` un `DIGNA_APP_PORT` vairs netiek nolasīti: adresi un portu serveris iegūst no `digna serve`. Salīdziniet savu failu ar sadaļu [Backend konfigurācija](#backend-configuration).

Tālāk aprakstītajos soļos ir norādīts, kur vecākai instalācijai jārīkojas citādi. Repozitorija jaunināšana 8. solī jebkura agrāka laidiena repozitoriju jaunina tieši uz 2026.11.

### Jaunināšanas process

#### 1. solis: Apturēt digna servisu {: #step-1-stop-the-digna-service }

Atveriet Command Prompt kā administrators un apturiet servisu ar pašreizējās instalācijas izpildāmo failu `digna`:

```bash
cd C:\path\to\digna
digna windows stop
```

Serviss paliek reģistrēts. Jaunais izpildāmais fails aizstāj veco tajā pašā direktorijā, tāpēc reģistrācija joprojām norāda uz pareizo failu.

Ja digna darbojas priekšplānā, tā Command Prompt logā nospiediet ++ctrl+c++.

!!! warning "Jaunināšana no laidiena, kas vecāks par 2026.06"

    Laidieni pirms 2026.06 reģistrēja servisu ar batch failiem. Apturiet un atreģistrējiet to ar pašreizējās instalācijas batch failiem, **pirms** 2. solī kaut ko pārdēvējat:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Pierakstiet kontu, ar kuru serviss darbojās, kā arī adresi un portu, kurā tas apkalpoja. Servisu jūs no jauna reģistrēsiet 9. solī.

#### 2. solis: Izveidojiet pašreizējās instalācijas dublējumu {: #step-2-backup-current-installation }

Savā digna instalācijas direktorijā pārdēvējiet pašreizējās instalācijas izpildāmo failu un paneļa mapi, lai jauno laidienu varētu izvietot tiem līdzās:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Saglabājiet `digna_old.exe`, līdz esat pārbaudījis jaunināšanu, un `dashboard_old`, līdz esat no tās atjaunojis savus konfigurācijas failus (skatiet 4. soli). Pēc tam abus varat izdzēst.

!!! info "Jaunināšana no laidiena, kas vecāks par 2026.06"

    Izpildāmā faila vietā pārdēvējiet mapes `dignabackend` un `dignacli`: `ren dignabackend dignabackend_old` un `ren dignacli dignacli_old`. Release 2026.11 neizmanto ne vienu, ne otru mapi, nedz arī batch failu mapi `bin`.

#### 3. solis: Izpakot un izvietot jauno versiju {: #step-3-extract-and-deploy-new-version }

1. Izpakojiet jauno digna instalācijas ZIP failu
2. Kopējiet jauno `digna` izpildāmo failu un `dashboard` mapi uz jūsu instalācijas direktoriju

!!! warning "Svarīgi"

    Ne `config.toml`, ne `dashboard/dashboard_config.toml` nekad netiek iekļauts instalācijas ZIP — digna komanda nekad nepiegādā nevienu no šiem failiem. Tāpēc jaunināšana jūsu esošo konfigurāciju neskar, un kopijas pārdēvētajās `*_old` mapēs ir vienīgās, kas jums ir.

#### 4. solis: Atjaunot jūsu konfigurācijas failus {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 neprasa izmaiņas failā `config.toml`: fails, kas darbojas ar Release 2026.06, turpina darboties. Divas izmaiņas nav obligātas:

- Pievienojiet [`[duckdb]` sadaļu](#duckdb-section), ja datubāzes savienojumiem jāizmanto digna Engine un tās noklusējuma vērtības neder jūsu resursdatoram.
- Izlaidiet `[app]` sadaļu, ja apgrieztais starpniekserveris pasniedz paneli un backend ar vienu izcelsmi.

!!! warning "Iestatījumi, kurus digna nenolasa"

    Agrākās šī ceļveža versijās bija parādīti daži iestatījumi, kurus digna nenolasa. Tiem nav nekādas ietekmes, un `config check` 6. solī tos uzskaita sadaļā **Unknown keys**. Noņemiet vai izlabojiet tos:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`, `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` un `digna_LOGGING_BACKUP_COUNT` nepastāv. Noņemiet tos.
    - Iestatījumu nosaukumi ir reģistrjutīgi. digna nolasa `DIGNA_REPO_HOST`, nevis `digna_REPO_HOST`. Rakstiet katru nosaukumu ar lielajiem burtiem, kā sadaļā [Backend konfigurācija](#backend-configuration).

!!! warning "Vienotā pieteikšanās: saglabājiet [[oidc_clients]]"

    digna nolasa vienotās pieteikšanās nodrošinātājus kā `[[oidc_clients]]` ierakstu sarakstu, katru ar savu `DIGNA_OIDC_KEY`. Ja esat pārveidojis savus nodrošinātājus par `[oidc_clients.<key>]` sadaļām, kā bija parādīts agrākā šī ceļveža versijā, mainiet tos atpakaļ. Kamēr šī forma ir spēkā, `config check` ziņo par `OIDC config(s)` kā FAILED:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Atkārtojiet ierakstu katram nodrošinātājam un saglabājiet katru `DIGNA_OIDC_KEY` tādu pašu kā `key` failā `dashboard_config.toml`. Tas skar tikai instalācijas, kas izmanto vienoto pieteikšanos.

#### 5. solis: Pārlādēt tīmekļa serveri {: #step-5-reload-the-web-server }

Panelis ir statisku failu kopums, tāpēc jūsu tīmekļa serveris — un pārlūkprogramma — joprojām var pasniegt iepriekšējo versiju. Pārlādējiet vai restartējiet tīmekļa serveri, kurā mitināta mape `dashboard`, un pēc tam pārlādējiet lapu ar pilnu atsvaidzināšanu (++ctrl+f5++).

#### 6. solis: Pārbaudiet konfigurāciju {: #step-6-validate-the-configuration }

Pirms pieskarties repozitorijam, pārliecinieties, ka `config.toml` ir pilnīgs:

```bash
digna config check
```

Katrai sadaļai jāziņo OK. Izlabojiet visu, kas ziņots kā FAILED, noņemiet atslēgas, kas uzskaitītas sadaļā **Unknown keys**, un pirms turpināšanas palaidiet komandu vēlreiz.

#### 7. solis: Aizstāt licences failu {: #step-7-replace-the-license-file }

Licences fails parasti tiek pārnests no viena laidiena uz nākamo. Release 2026.11 ir izņēmums: tas pievieno divus licencējamus moduļus, digna Data Reconciliation un digna Agentic, un licence, kas izsniegta pirms 2026.11, tos nesatur. Nokopējiet `license.toml`, ko digna komanda nodrošināja Release 2026.11, instalācijas direktorijā, aizstājot veco:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nepaturiet iepriekšējo licenci"

    Ar iepriekšējo licenci digna joprojām startē, bet digna Data Reconciliation un digna MCP Server paliek izslēgti. Katra komanda, kas pārbauda licenci — `user`, `inspection`, `repo` —, tiek pārtraukta pirms pieskaršanās repozitorijam, ja pārbaude neizdodas. Pirms turpināt, pārbaudiet jauno licenci:

    ```bash
    digna license check
    ```

#### 8. solis: Jaunināt repozitorija shēmu {: #step-8-upgrade-the-repository-schema }

Savā digna instalācijas direktorijā palaidiet:

```bash
digna repo upgrade
```

Release 2026.11 pārvalda repozitorija shēmu ar versionētām migrācijām. Pirmā jaunināšana no agrāka laidiena atjaunina shēmu līdz iepriekšējā versiju mehānisma pēdējai versijai, reģistrē to kā sākumpunktu un pēc tam piemēro Release 2026.11 migrācijas. Tā beidzas ar:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Visi esošie dati tiek saglabāti. Lai jebkurā brīdī redzētu repozitorija stāvokli, palaidiet `digna repo check`: tā parāda pēdējo piemēroto migrāciju un visas vēl nepiemērotās migrācijas.

!!! warning "digna nestartē ar novecojušu repozitoriju"

    Sākot ar Release 2026.11, serveris atsakās startēt, kamēr repozitorijs ir jājaunina, un par to ziņo, piemēram:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Pirms servera vai servisa palaišanas palaidiet `repo upgrade`.

#### 9. solis: Restartēt servisus {: #step-9-restart-services }

Ja digna darbojas kā Windows serviss, palaidiet to vēlreiz:

```bash
cd C:\path\to\digna
digna windows start
```

Ja jauninājāt no laidiena, kas vecāks par 2026.06, un 1. solī atreģistrējāt servisu, vispirms reģistrējiet to no jauna ar izpildāmo failu `digna`:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Norādiet `--address` un `--port` vērtības, kurās apkalpoja vecais serviss, ja vien nevēlaties noklusējuma vērtības `127.0.0.1` un `8000`. Pievienojiet `--account` un `--password`, ja vecais serviss darbojās ar domēna kontu. Pilnu opciju sarakstu skatiet sadaļā [digna palaide kā Windows serviss](#running-digna-as-a-windows-service).

Ja darbināt manuāli, restartējiet serveri:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Ja izmantojat IIS vai Tomcat, restartējiet attiecīgo tīmekļa serveri.

#### 10. solis: Pārbaudīt jaunināšanu {: #step-10-verify-the-upgrade }

1. Pārbaudiet jaunā izpildāmā faila laidienu:

    ```bash
    digna version
    ```

    Pirmajai rindai jābūt `Release: 2026.11`.

2. Piekļūstiet digna panelim un pārbaudiet, vai saskarne ielādējas pareizi.
3. Pārskatiet failus instalācijas direktorijā `logs`, vai nav kļūdu.
4. Pārbaudiet savus datubāzes savienojumus — skatiet [Savienojuma pārbaude](../../../databases/overview.md#testing-a-connection). Pēc jaunināšanas no laidiena, kas vecāks par 2026.06, vispirms pārceliet uz ODBC katru savienojumu, kas vēl neizmantoja ODBC.

Lai sāktu darbu ar jaunajiem moduļiem, skatiet [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [AI aģenta pievienošana](../../../platform/agentic/connect_ai_agent.md) par digna MCP Server un [Profilēšanas vieta](../../../platform/profiling/profiling_location.md) par digna Engine.