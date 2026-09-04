---
title: Windows uzstādīšanas ceļvedis – digna Release 2026.06 | digna Dokumentācija
description: Soli pa solim ceļvedis digna Release 2026.06 instalēšanai uz Windows — sistēmas prasības, PostgreSQL iestatīšana, tīmekļa servera konfigurācija, backend un dashboard konfigurācija, digna palaišana kā Windows serviss un pāreja uz jaunu izlaidumu.
keywords: digna windows instalācija, digna izvietošanas ceļvedis, digna backend iestatīšana, digna dashboard instalācija, postgresql uzstādīšana, digna windows serviss, digna atjaunināšanas ceļvedis
image: /assets/logo_square.png
---

# Windows uzstādīšanas ceļvedis digna Release 2026.06

**Release:** 2026.06

**Pēdējā atjaunināšana:** 2026. gada 30. augusts


---

## Saturu rādītājs

1. [Ievads](#introduction)
2. [Sistēmas prasības](#system-requirements)
3. [Priekšuzstādīšanas sagatavošana](#pre-installation-setup)
4. [PostgreSQL servera iestatīšana](#postgresql-server-setup)
5. [Tīmekļa servera konfigurācija](#web-server-configuration)
6. [Sākotnējā instalēšana](#initial-installation)
7. [Backend konfigurācija](#backend-configuration)
8. [Dashboard konfigurācija](#dashboard-configuration)
9. [digna palaide kā Windows serviss](#running-digna-as-a-windows-service)
10. [Pāreja uz jaunu izlaidumu](#upgrading-to-a-new-release)

---

## Ievads {: #introduction }

### Par digna

digna ir visaptveroša ar mākslīgo intelektu darbināta platforma, kas paredzēta datu kvalitātes pārvaldības optimizācijai dažādās datu vidēs, piemēram, datu noliktavās, datu ezeros un lakehouse risinājumos. Izstrādāta, lai būtu ļoti mērogojama un pielāgojama, digna risina mūsdienu datu izaicinājumus, izmantojot automatizāciju, reāllaika uzraudzību un anomaliju noteikšanu.

digna sastāv no divām galvenajām komponentēm:

- **dignabackend**: lietotnes kodols, atbildīgs par datu apstrādi un kvalitātes pārbaudēm.
- **dignadashboard**: tīmekļa saskarne, kas hostēta tīmekļa serverī, nodrošinot lietotājam draudzīgu veidu, kā mijiedarboties ar digna platformu un vizualizēt datu kvalitātes metrikas.

### Kas jauns Release 2026.06

Šajā izlaidumā datu novērojamības iespējas tiek ieviestas tieši jūsu kodā, ļaujot izstrādātājiem uzraudzīt datu kvalitāti pie avota. Pilnu informāciju skatiet [release notes](http://docs.digna.ai/changelog/Release_202606/).

---

## Sistēmas prasības {: #system-requirements }

Pirms sākat instalāciju, pārliecinieties, ka jūsu sistēma atbilst šādām minimālajām prasībām:

| Prasība | Specifikācija |
|---|---|
| **Operētājsistēma** | Windows Server vai Windows 10/11 |
| **Atmiņa (minimāli)** | 16 GB RAM |
| **Diska vieta** | 10 GB brīvas atmiņas |
| **Datubāze** | PostgreSQL Server 12 vai jaunāks |
| **Tīmekļa serveris** | IIS, Apache Tomcat vai līdzvērtīgs |

### Datubāzes uzstādīšanas iespējas

**Ja PostgreSQL jau ir instalēts:**
Jūs varat pievienot jaunu datubāzi digna savam esošajam PostgreSQL serverim.

**Ja instalējat PostgreSQL uz tā paša datora kā digna:**

> **⚠️ Ieteicamās specifikācijas**
>
> - **Atmiņa**: 32 GB RAM (nevis 16 GB)
> - **Diska vieta**: 50 GB brīvas atmiņas (nevis 10 GB)
>
> Šīs palielinātās specifikācijas nodrošina pietiekamus resursus gan digna, gan PostgreSQL darbināšanai vienlaikus.

---

## Priekšuzstādīšanas sagatavošana {: #pre-installation-setup }

Pirms instalēt digna, pārliecinieties, ka ir nodrošinātas divas galvenās priekšnosacījumu komponentes:

1. **PostgreSQL Server** – aprēķināto metrikas un veiktspējas datu glabāšanai
2. **Tīmekļa serveris** – digna Dashboard hostēšanai

Ja šīs komponentes vēl nav uzstādītas, sekojiet zemāk norādītajiem norādījumiem, lai tās instalētu un konfigurētu.

---

## PostgreSQL servera iestatīšana {: #postgresql-server-setup }

### Ja PostgreSQL jau ir pieejams

Ja PostgreSQL jau darbojas uz jūsu lokālā datora vai izmantojat pārvaldītu attālo PostgreSQL serveri, varat pāriet uz [nākamo sadaļu](#web-server-configuration).

### PostgreSQL instalēšana

Izpildiet šīs darbības, lai instalētu PostgreSQL uz Windows:

#### 1. solis: Lejupielādējiet PostgreSQL

1. Apmeklējiet [PostgreSQL Downloads lapu](https://www.postgresql.org/download/)
2. Izvēlieties **Windows**
3. Lejupielādējiet jaunāko instalētāju

#### 2. solis: Palaidiet instalētāju

1. Veiciet dubultklikšķi uz lejupielādētā instalētāja faila
2. Sekojiet vedņa norādījumiem

#### 3. solis: Izvēlieties instalācijas direktoriju

Izvēlieties direktoriju, kur PostgreSQL tiks instalēts. Parasti noklusējuma vieta ir piemērota.

#### 4. solis: Izvēlieties komponentes

Standarta uzstādīšanai atstājiet noklusējuma komponentes izvēlētas.

#### 5. solis: Iestatiet PostgreSQL superlietotāja paroli

Ievadiet un apstipriniet paroli PostgreSQL superlietotājam (`postgres`). **Saglabājiet šo paroli drošā vietā** — tā būs nepieciešama vēlāk.

#### 6. solis: Konfigurējiet porta numuru

Noklusējuma PostgreSQL ports ir `5432`. Varat izmantot noklusējumu vai norādīt citu portu, ja nepieciešams.

> **💡 Padoms**
>
> Ja ports 5432 jau tiek izmantots, izvēlieties alternatīvu portu un pierakstiet to vēlākai konfigurācijai.

#### 7. solis: Izvēlieties lokalizāciju

Izvēlieties datubāzes lokalizāciju. Noklusējums parasti ir piemērots lielākajai daļai instalāciju.

#### 8. solis: Pabeidziet instalāciju

Noklikšķiniet **Next** cauri atliekošajiem soļiem, pēc tam noklikšķiniet **Finish**.

#### 9. solis: Pārbaudiet instalāciju

Atveriet Command Prompt un pārbaudiet, vai PostgreSQL ir uzstādīts:

```bash
psql --version
```

Ja instalācija bija veiksmīga, tiks parādīta PostgreSQL versija.

---

## Tīmekļa servera konfigurācija {: #web-server-configuration }

digna nepieciešams tīmekļa serveris dashboard hostēšanai. Izvēlieties vienu no šīm opcijām:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Jums nepieciešams uzstādīt un konfigurēt tikai vienu no šiem serveriem.

### IIS uzstādīšana {: #iis-setup }

#### Pārskats

Internet Information Services (IIS) ir Microsoft tīmekļa serveris vietņu un tīmekļa lietotņu hostēšanai.

#### IIS ieslēgšana

1. **Atveriet Vadības paneli**
   - Nospiediet `Win + R`
   - Ierakstiet `control` un nospiediet Enter

2. **Dodieties uz Windows funkcijām**
   - Klikšķiniet uz **Programs**
   - Izvēlieties **Turn Windows features on or off**

3. **Ieslēdziet Internet Information Services**
   - Ritiniet sarakstu un atrodiet **Internet Information Services (IIS)**
   - Atzīmējiet izvēles rūtiņu, lai to ieslēgtu
   - Noklikšķiniet uz **+**, lai izvērstu un pārliecinātos, ka ir atlasītas šādas apakškomponentes:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Noklikšķiniet OK**, lai piemērotu izmaiņas

5. **Pārbaudiet IIS instalāciju**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost`
   - Jums jāredz IIS sveiciena lapa

#### Nepieciešams: URL Rewrite modulis

IIS prasa URL Rewrite komponenti. Lejupielādējiet un instalējiet to no [oficiālās Microsoft lapas](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Nepieciešams: MIME tips Markdown failiem

Lai nodrošinātu, ka Markdown faili (`.md`) tiek apkalpoti pareizi ar IIS:

1. Atveriet **IIS Manager** (nospiediet `Win + R`, ierakstiet `inetmgr`, nospiediet Enter)
2. Dodieties uz **Your Site > MIME Types**
3. Klikšķiniet **Add...**
4. Konfigurējiet:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

> **⚠️ Svarīgi**
>
> Bez šī iestatījuma `.md` faili var netikt apkalpoti pareizi.

---

### Apache Tomcat uzstādīšana {: #apache-tomcat-setup }

#### Pārskats

Apache Tomcat ir atvērtā koda Java servlet konteiners un tīmekļa serveris.

#### Instalēšana

1. **Lejupielādējiet Apache Tomcat**
   - Apmeklējiet [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Lejupielādējiet Windows ZIP izplatījumu

2. **Izpakot arhīvu**
   - Izpakojiet ZIP failu izvēlētā direktorijā
   - Piemērs: `C:\Program Files\Apache Tomcat`

3. **Pārbaudiet, vai Tomcat darbojas**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost:8080`
   - Jums jāredz Apache Tomcat sveiciena lapa

> **💡 Padoms**
>
> Apache Tomcat parasti tiek startēts automātiski pēc instalācijas. Ja tas netiek startēts, dodieties uz `bin` mapi un palaidiet `startup.bat`.

---

## Sākotnējā instalēšana {: #initial-installation }

### 1. solis: Izveidojiet digna repositāriju

digna repositārijs glabā visas digna aprēķinātās metrikas. Tas darbojas kā centrālā datubāze analītiskajiem un veiktspējas datiem.

#### Izveidojiet shēmu un lietotāju repositārijam

Atveriet savu PostgreSQL klientu (pgAdmin, psql vai līdzīgu) un izpildiet šādas SQL komandas:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Aizstājiet šādus vietturi:**

- `<digna_repo_schema>` — Jūsu izvēlētais shēmas nosaukums (piem., `dignarepo`)
- `<digna_repo_user>` — Jūsu izvēlētais lietotājvārds (piem., `digna_user`)
- `<digna_repo_password>` — Droša parole šim lietotājam

**Piemērs:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

> **✅ Labā prakse**
>
> Izmantojiet spēcīgas, sarežģītas paroles datubāzes lietotājiem. Izvairieties no viegli uzminamām akreditācijām.

---

### 2. solis: Izpakot digna instalācijas pakotni

1. Atrodiet jums nodoto digna instalācijas ZIP failu
2. Izpakojiet to uz vēlamo instalācijas direktoriju
3. Pēc izpakotnes vajadzētu redzēt šādas vienības:
   - `dashboard/` — tīmekļa dashboard saskarne
   - `digna` — galvenais izpildāmais fails (backend + CLI apvienots)
   - `config.toml` — konfigurācijas fails
   - `license.toml` — licences fails (kopējiet savu šeit)

### 3. solis: Instalējiet licences failu

> **⚠️ Svarīgi**
>
> Licences fails **NAV** iekļauts instalācijas paketē un tiks nodrošināts atsevišķi no digna.

1. Atrodiet jums piegādāto `license.toml` failu
2. Kopējiet to uz digna instalācijas saknes direktoriju (tur, kur atrodas `config.toml` un `digna` izpildāmais fails)

**Kāpēc tas ir svarīgi:**
Licences fails satur jūsu klienta informāciju, licences derīguma termiņu un digitālo parakstu. **Nemodificējiet šo failu** — jebkuras izmaiņas to padarīs nederīgu.

**Direktorijas struktūra pēc uzstādīšanas:**

```
digna_installation/
├── config.toml         (konfigurācijas fails)
├── license.toml        (JŪSU LICENCES FAILS - kopējiet šeit)
├── digna               (galvenais izpildāmais fails)
└── dashboard/          (tīmekļa saskarne)
    └── (dashboard faili)
```

---

## Backend konfigurācija {: #backend-configuration }

### 1. solis: Izveidojiet un rediģējiet konfigurācijas failu

`config_template.toml` fails tiek piegādāts jūsu digna instalācijas direktorijā. Jums tas vienkārši jāpārdēvē uz `config.toml`.

**Atrašanās vieta:** `digna_installation/config.toml`

Atveriet `config.toml` teksta redaktorā un konfigurējiet katru zemāk norādīto sadaļu.

#### [app] sadaļa

Šī sadaļa konfigurē dignabackend lietotnes iestatījumus:

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
| `digna_APP_HOST` | `localhost` vai IP adrese | Hostname vai IP, kur tiek hostēts dignabackend |
| `digna_APP_PORT` | `8082` (noklusējums) | Ports REST API endpointiem |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontend URL | Ja dashboard atrodas citā serverī, iekļaujiet tā URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nepieciešams CORS ar akreditācijām |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Atļauj visus HTTP metodus |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Atļauj visus header laukus |

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
| `digna_REPO_USER` | `digna_user` | Lietotājs, izveidots PostgreSQL iestatīšanā |
| `digna_REPO_PASSWORD` | Jūsu parole | Parole, kas iestatīta shēmas izveidē |

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
| `digna_FERNET_KEY` | Šifrēšanas atslēga | Tiek izmantota tokenu un sīkfailu šifrēšanai (noklusējuma atslēga tiek nodrošināta) |
| `digna_COOKIE_DOMAIN` | `localhost` | Atbilst jūsu frontend domēnam |
| `digna_COOKIE_SECURE` | `false` (lokāli) / `true` (produkcija) | Lietojiet `true` HTTPS savienojumiem |
| `digna_COOKIE_HTTPONLY` | `true` | Vienmēr ieslēgts drošībai |
| `digna_COOKIE_SAME_SITE` | `lax` | Aizsargā pret CSRF uzbrukumiem |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 stundas) | Sesijas derīguma termiņš sekundēs |
| `digna_MAX_WORKERS` | CPU kodoli - 1 | Paralēlo pārbaudes uzdevumu skaits |

#### [logging] sadaļa

Šī sadaļa konfigurē žurnālu (logging) uzvedību:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametrs | Vērtība | Piezīmes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` vai `DEBUG` | `INFO` produkcijai, `DEBUG` problēmu novēršanai |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Saglabājamo dienas žurnālu rezerves kopiju skaits |

---

### 3. solis: Inicializējiet repositāriju

1. Atveriet Command Prompt
2. Pārejiet uz savu digna instalācijas direktoriju (tur, kur atrodas `config.toml` un `digna` izpildāmais fails)
3. Palaidiet savienojuma pārbaudi:

```bash
digna repo check
```

Jums jāredz apstiprinājums, ka savienojums ir izveidots (repositārijs pats par sevi vēl nav instalēts).

### 4. solis: Instalējiet repositārija shēmu

Tajā pašā direktorijā palaidiet:

```bash
digna repo install
```

Šī komanda instalē nepieciešamās tabulas un shēmu jūsu PostgreSQL datubāzē.

### 5. solis: Startējiet digna serveri

digna instalācijas direktorijā startējiet serveri ar:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — Servera hostname/IP
- `--port` — Servera ports

Jums jāredz startēšanas ziņojumi, kas apstiprina servera darbību:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### 6. solis: Izveidojiet administratīvo lietotāju

1. Atveriet **jaunu** Command Prompt logu
2. Pārejiet uz savu digna instalācijas direktoriju
3. Palaidiet šādu komandu, lai izveidotu admin lietotāju:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Piemērs:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Šī komanda izveido lietotāju ar pilnīgām administratīvām tiesībām.

> **✅ Labā prakse**
>
> Izmantojiet spēcīgu paroli ar lielajiem un mazajiem burtiem, cipariem un speciālajiem simboliem.

---

## Dashboard konfigurācija {: #dashboard-configuration }

### 1. solis: Ievietojiet dashboard tīmekļa serverī

digna dashboard satur savu atsevišķu `config.toml` failu, kas atrodas `dashboard/` direktorijā. Šī konfigurācija tiek nodrošināta un parasti nav jāmaina sākotnējā uzstādīšanas laikā. Jāmaina tikai tad, ja nepieciešams pielāgot backend savienojumu vai konfigurēt daudzinstanču izvietojumu.

Ja nepieciešams modificēt dashboard konfigurāciju, skatiet dashboard dokumentāciju.

Izvēlieties tīmekļa serveri un sekojiet attiecīgajām izvietošanas darbībām.

#### Izvietošana IIS

1. **Atveriet IIS Manager**
   - Nospiediet `Win + R`, ierakstiet `inetmgr`, nospiediet Enter

2. **Izveidojiet jaunu vietni**
   - Kreisajā rūtī ar peles labo pogu klikšķiniet uz **Sites**
   - Izvēlieties **Add Website...**

3. **Konfigurējiet vietni**
   - **Site Name**: Ievadiet nosaukumu (piem., "dignaDashboard")
   - **Physical Path**: Noklikšķiniet Browse un izvēlieties jūsu `dashboard` mapi
   - **Binding**: Iestatiet IP adresi un portu (noklusējuma ports HTTP — 80, HTTPS — 443)

4. **Startējiet vietni**
   - Noklikšķiniet **OK**, lai izveidotu vietni
   - Ar peles labo pogu klikšķiniet uz jaunās vietnes un izvēlieties **Start**

5. **Pārbaudiet instalāciju**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost` (vai jūsu konfigurēto URL)
   - Jums jāredz digna dashboard pieslēgšanās lapa

#### Izvietošana Apache Tomcat

1. **Kopējiet dashboard uz Tomcat**
   - Kopējiet `dashboard` mapi uz jūsu Tomcat `webapps` direktoriju
   - Pārdēvējiet to pēc vajadzības (piem., uz `digna`)
   - Piemērs: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Pārbaudiet izvietojumu**
   - Atsvaidziniet vai pārlādējiet Tomcat pārvaldības lapu (http://localhost:8080)
   - Jums jāredz "digna" (vai jūsu izvēlētais nosaukums) sarakstā ar izvietotajām lietotnēm

3. **Piekļūstiet dashboard**
   - Atveriet pārlūkprogrammu
   - Dodieties uz `http://localhost:8080/digna`
   - Jums jāredz digna dashboard pieslēgšanās lapa

---

## digna palaišana kā Windows serviss {: #running-digna-as-a-windows-service }

### Kāpēc izmantot Windows servisu?

dignabackend palaišana kā Windows serviss nodrošina:
- Automātisku startēšanu servera iedarbināšanas brīdī
- Darbību fonā bez atvērtas Command Prompt loga
- Automātisku restartēšanu avārijas gadījumā
- Pārvaldību caur Windows Services

### Servisa pārvaldības faili

Visi nepieciešamie faili atrodas digna instalācijas direktorijā zem: `bin/`

Pieejamie batch faili:
- `install_service.bat` — reģistrē digna kā Windows servisu
- `uninstall_service.bat` — noņem servisu no reģistra
- `start_service.bat` — palaiž servisu
- `stop_service.bat` — apstādināt servisu

> **⚠️ Nepieciešamas administratora tiesības**
>
> Visus batch failus jāizpilda ar Administratora tiesībām.

### Servisa instalēšana

1. **Atveriet Command Prompt kā administrators**
   - Ar peles labo pogu klikšķiniet Command Prompt
   - Izvēlieties "Run as Administrator"

2. **Pārejiet uz bin mapi**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Palaidiet instalācijas skriptu**
   ```bash
   install_service.bat
   ```

digna serveris tagad reģistrēts kā Windows serviss ar **automātisku startēšanu**. Serviss nekavējoties nesāk darboties — skatiet nākamo sadaļu, lai to palaistu.

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

> **💡 Padoms**
>
> Vienmēr apturiet servisu pirms lietotnes failu atjaunināšanas.

### Pārvietošana uz jaunu direktoriju

Ja nepieciešams pārvietot digna instalāciju:

1. **Atinstalējiet esošo servisu**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Pārvietojiet lietotnes failus**
   - Pārvietojiet visu digna instalācijas mapes saturu uz jauno atrašanās vietu

3. **Pārliecinieties, ka serviss atkal ir instalēts**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Palaidiet servisu**
   ```bash
   start_service.bat
   ```

### Servisa atinstalēšana

1. **Apturiet darbojošo servisu**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Atinstalējiet servisu**
   ```bash
   uninstall_service.bat
   ```

digna serveris tagad ir noņemts no Windows servisu reģistra.

---

## Pāreja uz jaunu izlaidumu {: #upgrading-to-a-new-release }

### Pirms pārejas

**digna repositārija rezerves kopijas izveide ir obligāta**

Pirms digna atjaunināšanas, izveidojiet rezerves kopiju savam repositārijam (PostgreSQL), lai aizsargātu pret datu zudumu. Rezerves kopija nodrošina atjaunošanu, ja atjaunināšanas laikā rodas negaidītas problēmas.

### Atjaunināšanas process

#### 1. solis: Apturiet digna servisu

Ja digna darbojas kā Windows serviss, vispirms to apturiet:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2. solis: Rezervējiet pašreizējo backend instalāciju

Jūsu digna instalācijas direktorijā:

```bash
# Pārdēvējiet mapi, kas satur dignabackend
ren dignabackend dignabackend_old
```
```bash
# Pārdēvējiet dashboard
ren dashboard dashboard_old
```

#### 3. solis: Izpakot un izvietot jauno versiju

1. Izpakojiet jauno digna instalācijas ZIP failu
2. Kopējiet jauno `digna` izpildāmo failu un `dashboard` mapi uz savu instalācijas direktoriju

> **✅ Svarīgi**
>
> `config.toml` fails **nekad** netiek iekļauts instalācijas ZIP. Jūsu esošā konfigurācija paliek neskarta.

### 4. solis: Atjaunojiet konfigurācijas failus

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

### 5. solis: Atjauniniet repositārija shēmu

Pārejiet uz savu digna instalācijas direktoriju un palaidiet:

```bash
digna repo upgrade
```

Šī komanda atjauninās PostgreSQL shēmu uz jaunāko versiju, saglabājot visus esošos datus.

### 6. solis: Restartējiet servisus

Ja tiek izmantots Windows serviss:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Ja serveris tiek palaists manuāli, restartējiet to:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Ja izmantojat IIS vai Tomcat, restartējiet attiecīgo tīmekļa serveri.

#### 7. solis: Pārbaudiet atjaunināšanu

1. Piekļūstiet digna dashboard
2. Pārliecinieties, ka saskarne ielādējas pareizi
3. Pārbaudiet servera žurnālus, vai nav kļūdu