---
title: Windows instalācijas ceļvedis – digna Release 2026.06 | digna dokumentācija
description: Soli pa solim ceļvedis par digna Release 2026.06 uzstādīšanu Windows — sistēmas prasības, PostgreSQL iestatīšana, tīmekļa servera konfigurācija, backend un paneļa konfigurācija, digna darbība kā Windows serviss un jaunināšana uz jaunu izlaidumu.
keywords: digna Windows instalācija, digna izvietošanas ceļvedis, digna backend iestatīšana, digna paneļa instalācija, postgresql iestatīšana, digna Windows serviss, digna jaunināšanas ceļvedis
image: /assets/logo_square.png
---

# Windows instalācijas ceļvedis digna Release 2026.06

**Izlaidums:** 2026.06

**Pēdējais atjauninājums:** 2026. gada 30. augusts


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

- **dignabackend**: lietojumprogrammas kodols, kas atbild par datu apstrādi un kvalitātes pārbaudēm.
- **dignadashboard**: tīmekļa saskarne, kas izvietota uz tīmekļa servera un nodrošina lietotājam draudzīgu veidu, kā mijiedarboties ar digna platformu un vizualizēt datu kvalitātes metrikas.

### Kas jauns izlaidumā 2026.06

Šajā izlaidumā datu novērošanas iespējas ir integrētas tieši jūsu kodā, ļaujot izstrādātājiem uzraudzīt datu kvalitāti pie avota. Pilnas detaļas skatiet [izlaiduma piezīmēs](http://docs.digna.ai/changelog/Release_202606/).

### Meklējat macOS vai Linux?

Šis ceļvedis attiecas uz Windows. Citu platformu instalācijas skaidrojumu skatiet [macOS instalācijas ceļvedī](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) vai [Linux instalācijas ceļvedī](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — konfigurācijas fails
   - `license.toml` — licences fails (ielīmējiet savu šeit)

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

Šī sadaļa konfigurē digna backend lietojumprogrammas iestatījumus:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_APP_HOST` | `localhost` vai IP adrese | Hostname vai IP, kur tiek mitināts dignabackend |
| `digna_APP_PORT` | `8082` (noklusējums) | Ports REST API galapunktiem |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontenda URL | Ja panelis atrodas citā serverī, iekļaujiet tā URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nepieciešams CORS ar akreditācijas datiem |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Atļaut visus HTTP metodus |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Atļaut visus header laukus |

#### [repo] sadaļa

Šī sadaļa konfigurē savienojumu ar PostgreSQL datubāzi:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` vai IP | PostgreSQL servera hostname/IP |
| `digna_REPO_PORT` | `5432` (noklusējums) | PostgreSQL ports |
| `digna_REPO_DB` | `postgres` | Datubāzes nosaukums |
| `digna_REPO_SCHEMA` | `dignarepo` | Iepriekš izveidotā shēma |
| `digna_REPO_USER` | `digna_user` | Lietotājs izveidots PostgreSQL iestatīšanā |
| `digna_REPO_PASSWORD` | Jūsu parole | Parole, iestatīta shēmas izveidē |

#### [base] sadaļa

Šī sadaļa satur drošības un sīkfailu iestatījumus:

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

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_FERNET_KEY` | Šifrēšanas atslēga | Izmanto, lai šifrētu tokenus un sīkfailus (noklusējums iekļauts) |
| `digna_COOKIE_DOMAIN` | `localhost` | Atbilst jūsu frontenda domēnam |
| `digna_COOKIE_SECURE` | `false` (lokāli) / `true` (produkcijā) | Lietojiet `true` HTTPS savienojumiem |
| `digna_COOKIE_HTTPONLY` | `true` | Vienmēr iespējots drošībai |
| `digna_COOKIE_SAME_SITE` | `lax` | Novērš CSRF uzbrukumus |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 stundas) | Sesijas derīguma laiks sekundēs |
| `digna_MAX_WORKERS` | Skaitlis: CPU kodolu skaits - 1 | Paralēlo inspekciju uzdevumu skaits |

#### [logging] sadaļa

Šī sadaļa konfigurē žurnālu (logu) uzvedību:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` vai `DEBUG` | `INFO` produkcijai, `DEBUG` problēmu novēršanai |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Cik dienu žurnālu dublējumu saglabāt |

---

### 3. solis: Inicializēt repozitoriju

1. Atveriet Command Prompt
2. Pārejiet uz jūsu digna instalācijas direktoriju (tur, kur atrodas `config.toml` un izpildāmais `digna`)
3. Palaidiet savienojuma pārbaudi:

```bash
digna repo check
```

Jums jāsaņem apstiprinājums, ka savienojums ir izveidots (repozitārijs pats par sevi vēl nav inicializēts).

### 4. solis: Instalēt repozitorija shēmu

Tajā pašā direktorijā palaidiet:

```bash
digna repo install
```

Šī komanda instalē nepieciešamās tabulas un shēmu jūsu PostgreSQL datubāzē.

### 5. solis: Palaist digna serveri

Digna instalācijas direktorijā palaidiet serveri ar:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — servera hostname/IP
- `--port` — servera ports 

Jums jāredz startēšanas ziņas, kas apstiprina, ka serveris darbojas:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### 6. solis: Izveidot administratora lietotāju

1. Atveriet **jaunu** Command Prompt logu
2. Pārejiet uz jūsu digna instalācijas direktoriju
3. Palaidiet šādu komandu, lai izveidotu administratora lietotāju:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Piemērs:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Šī komanda izveido lietotāju ar pilnām administratīvām tiesībām.

!!! tip "Laba prakse"

    Izmantojiet stipru paroli ar lielajiem un maziem burtiem, cipariem un speciālajām zīmēm.

---

## Paneļa konfigurācija {: #dashboard-configuration }

### 1. solis: Izvietot paneli uz tīmekļa servera

digna panelim ir atsevišķs `config.toml` fails, kas atrodas `dashboard/` direktorijā. Šī konfigurācija parasti jau ir nodrošināta un sākotnējā iestatīšanā nav jāmaina. Jāveic izmaiņas tikai tad, ja nepieciešams pielāgot backend savienojumu.

Ja nepieciešams modificēt paneļa konfigurāciju (piem., daudzinstanču izvietošanai), skatiet paneļa dokumentāciju.

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

### Servisa pārvaldības faili

Visi nepieciešamie faili atrodas digna instalācijas direktorijā zem: `bin/`

Sekojošas batch skripti ir pieejami:
- `install_service.bat` — reģistrē digna kā Windows servisu
- `uninstall_service.bat` — atreģistrē servisu
- `start_service.bat` — palaiž servisu
- `stop_service.bat` — aptur servisu

!!! warning "Nepieciešamas administratīvās tiesības"

    Visus batch failus jāizpilda ar Administratora tiesībām.

### Servisa instalēšana

1. **Atveriet Command Prompt kā administrators**
   - Ar peles labo pogu klikšķiniet uz Command Prompt
   - Izvēlieties "Run as Administrator"

2. **Pārejiet uz bin mapi**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Palaidiet instalācijas skriptu**
   ```bash
   install_service.bat
   ```

digna serveris tagad ir reģistrēts kā Windows serviss ar **automātisku startēšanu**. Serviss netiek sāknēts uzreiz — skatiet nākamo sadaļu, lai to palaistu.

### Servisa palaišana un apturēšana

#### Lai palaistu servisu

1. Atveriet Command Prompt kā administrators
2. Pārejiet uz `digna\bin`
3. Palaidiet:
   ```bash
   start_service.bat
   ```

#### Lai apturētu servisu

1. Atveriet Command Prompt kā administrators
2. Pārejiet uz `digna\bin`
3. Palaidiet:
   ```bash
   stop_service.bat
   ```

!!! tip "Padoms"

    Vienmēr apturiet servisu, pirms atjaunināt lietojumprogrammas failus.

### Pārvietot servisu uz jaunu direktoriju

Ja nepieciešams pārvietot digna instalāciju:

1. **Atinstalēt esošo servisu**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Pārvietot aplikācijas failus**
   - Pārvietojiet visu digna instalācijas mapi uz jauno atrašanās vietu

3. **Pārinstalēt servisu**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Palaist servisu**
   ```bash
   start_service.bat
   ```

### Servisa atinstalēšana

1. **Apturēt darbojošos servisu**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Atinstalēt servisu**
   ```bash
   uninstall_service.bat
   ```

digna serveris tagad vairs nav reģistrēts kā Windows serviss.

---

## Jaunināšana uz jaunu izlaidumu {: #upgrading-to-a-new-release }

### Pirms jaunināšanas

**Repozitārija (PostgreSQL) rezerves kopijas izveide ir obligāta**

Pirms digna jaunināšanas veiciet rezerves kopiju sava repozitorija (PostgreSQL), lai izvairītos no datu zuduma. Rezerves kopija nodrošina atjaunošanas iespēju, ja jaunināšanas laikā rodas neparedzētas problēmas.

### Jaunināšanas process

#### 1. solis: Apturēt digna servisu

Ja digna darbojas kā Windows serviss, vispirms to apturiet:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2. solis: Rezerves kopija esošajai backend instalācijai

Jūsu digna instalācijas direktorijā:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### 3. solis: Izpakot un izvietot jauno versiju

1. Izpakojiet jauno digna instalācijas ZIP failu
2. Kopējiet jauno `digna` izpildāmo failu un `dashboard` mapi uz jūsu instalācijas direktoriju


!!! warning "Svarīgi"

    `config.toml` fails **nekad** netiek iekļauts instalācijas ZIP. Jūsu esošā konfigurācija paliek droša.

### 4. solis: Atjaunot jūsu konfigurācijas failus

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### 5. solis: Jaunināt repozitorija shēmu

Pārejiet uz jūsu digna instalācijas direktoriju un palaidiet:

```bash
digna repo upgrade
```

Tas atjauninās PostgreSQL shēmu uz jaunāko versiju, saglabājot visu esošo datu integritāti.

### 6. solis: Restartēt servisus

Ja darbināt kā Windows servisu:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Ja darbināt manuāli, restartējiet serveri:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Ja izmantojat IIS vai Tomcat, restartējiet attiecīgo tīmekļa serveri.

#### 7. solis: Pārbaudīt jaunināšanu

1. Piekļūstiet digna panelim
2. Pārbaudiet, vai saskarne ielādējas pareizi
3. Pārskatiet servera žurnālus, vai nav kļūdu