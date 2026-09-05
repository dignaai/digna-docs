---
title: Windows Installation Guide – digna Release 2026.06 | digna Documentation
description: Step-by-step guide to installing digna Release 2026.06 on Windows — system requirements, PostgreSQL setup, web server configuration, backend and dashboard configuration, running digna as a Windows service, and upgrading to a new release.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windowsi paigaldusjuhend digna Release 2026.06 jaoks

**Release:** 2026.06

**Viimati uuendatud:** 30. august 2026


---

## Sisukord

1. [Sissejuhatus](#introduction)
2. [Süsteeminõuded](#system-requirements)
3. [Eelpaigaldus](#pre-installation-setup)
4. [PostgreSQL serveri seadistus](#postgresql-server-setup)
5. [Veebiserveri konfiguratsioon](#web-server-configuration)
6. [Esmane paigaldus](#initial-installation)
7. [Backendi konfiguratsioon](#backend-configuration)
8. [Dashboardi konfiguratsioon](#dashboard-configuration)
9. [digna käivitamine Windowsi teenusena](#running-digna-as-a-windows-service)
10. [Uuendamine uuele versioonile](#upgrading-to-a-new-release)

---

## Sissejuhatus {: #introduction }

### digna kohta

digna on terviklik AI-põhine platvorm, mis on loodud andmekvaliteedi haldamise optimeerimiseks erinevates andmekeskkondades nagu andmehoidlad, andmeladestikud ja lakehoused. Skaleeritavuse ja kohandatavuse eesmärgil lahendab digna kaasaegseid andmeprobleeme automatiseerimise, reaalajas jälgimise ja anomaaliate tuvastamise kaudu.

digna koosneb kahest põhikomponendist:

- **dignabackend**: rakenduse südamik, mis vastutab andmete töötlemise ja kvaliteedikontrollide eest.
- **dignadashboard**: veebipõhine liides, mis majutatakse veebiserveris ja pakub kasutajasõbralikku viisi digna platvormiga suhtlemiseks ning andmekvaliteedi mõõdikute visualiseerimiseks.

### Mis on uut Release 2026.06 versioonis

Selles versioonis on andmeobservability võimekus viidud otse teie koodi, võimaldades arendajatel jälgida andmekvaliteeti juba allikas. Täielike üksikasjade jaoks vaadake [release notes](http://docs.digna.ai/changelog/Release_202606/).

---

## Süsteeminõuded {: #system-requirements }

Enne paigalduse alustamist veenduge, et teie süsteem vastab järgmistele miinimumnõuetele:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server või Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB vaba kettaruumi |
| **Database** | PostgreSQL Server 12 või uuem |
| **Web Server** | IIS, Apache Tomcat või samaväärne |

### Andmebaasi paigaldusvalikud

**Kui PostgreSQL on juba installitud:**
Võite lisada digna jaoks uue andmebaasi olemasolevasse PostgreSQL serverisse.

**Kui paigaldate PostgreSQL-i samasse masinasse, kus jookseb digna:**

!!! info "Soovitatud spetsifikatsioonid"

    - **Mälu**: 32 GB RAM (16 GB asemel)
    - **Kettaruum**: 50 GB vaba salvestusruumi (10 GB asemel)

    Need kõrgemad nõuded arvestavad nii digna kui ka PostgreSQL-i samaaegset käivitamist.

---

## Eelpaigaldus {: #pre-installation-setup }

Enne digna paigaldamist veenduge, et kaks põhitingimust on täidetud:

1. **PostgreSQL Server** – salvestamaks arvutatud mõõdikuid ja jõudlusandmeid
2. **Veebiserver** – digna Dashboardi majutamiseks

Kui need komponendid pole veel seadistatud, järgige alljärgnevaid sektsioone nende paigaldamiseks ja konfiguratsiooniks.

---

## PostgreSQL serveri seadistus {: #postgresql-server-setup }

### Kui teil on juba PostgreSQL

Kui PostgreSQL on juba installitud ja töötab kas lokaalses masinas või kasutate hallatud kaug-PG serverit, võite liikuda järgmisesse sektsiooni [veebiserveri konfiguratsioon](#web-server-configuration).

### PostgreSQL paigaldamine

Järgige neid samme PostgreSQL-i paigaldamiseks Windowsile:

#### 1. samm: Laadige alla PostgreSQL

1. Külastage [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Valige **Windows**
3. Laadige alla uusim installer

#### 2. samm: Käivitage installeerija

1. Topeltklõpsake alla laaditud installerfailil
2. Järgige seadistusviisa juhiseid

#### 3. samm: Valige paigalduskataloog

Valige kataloog, kuhu PostgreSQL paigaldatakse. Vaiketee on tavaliselt sobiv.

#### 4. samm: Valige komponendid

Tavalise paigalduse jaoks jätke vaikimisi valitud komponendid.

#### 5. samm: Määrake PostgreSQL superkasutaja parool

Sisestage ja kinnitage parool PostgreSQL superkasutajale (`postgres`). **Salvestage see parool turvaliselt** — vajate seda hiljem.

#### 6. samm: Konfigureerige pordi number

Vaikeport PostgreSQL-ile on `5432`. Võite kasutada vaikeseadet või määrata vajadusel teise pordi.

!!! tip "Näpunäide"

    Kui port 5432 on juba kasutusel, valige alternatiivne port ja pidage seda meeles edasiseks konfiguratsiooniks.

#### 7. samm: Valige lokaal

Valige andmebaasi lokaal. Vaikevalik sobib enamikele paigaldustele.

#### 8. samm: Lõpetage paigaldus

Klõpsake ülejäänud sammudes **Next** ning seejärel **Finish**.

#### 9. samm: Kontrollige paigaldust

Avage käsurida ja kontrollige PostgreSQL-i olemasolu:

```bash
psql --version
```

Kui paigaldus õnnestus, kuvatakse PostgreSQL versioon.

---

## Veebiserveri konfiguratsioon {: #web-server-configuration }

digna vajab veebiserverit, et majutada dashboardi. Valige üks järgmistest:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Teil on vaja paigaldada ja konfigureerida ainult üks neist.

### IIS seadistus {: #iis-setup }

#### Ülevaade

Internet Information Services (IIS) on Microsofti veebiserver veebilehtede ja veebirakenduste majutamiseks.

#### IIS-i lubamine

1. **Avage juhtpaneel**
   - Vajutage `Win + R`
   - Tippige `control` ja vajutage Enter

2. **Navigeerige Windowsi funktsioonide juurde**
   - Klõpsake **Programs**
   - Valige **Turn Windows features on or off**

3. **Luba Internet Information Services**
   - Kerige alla ja leidke **Internet Information Services (IIS)**
   - Märkige ruut selle lubamiseks
   - Klõpsake **+**, et laiendada ja veenduda, et järgmised alamkomponendid on valitud:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klõpsake OK**, et muudatused rakendada

5. **Kontrollige IIS-i paigaldust**
   - Avage brauser
   - Navigeerige aadressile `http://localhost`
   - Peaksite nägema IIS-i tervitussaiti

#### Nõutav: URL Rewrite moodul

IIS vajab URL Rewrite komponenti. Laadige see alla ja paigaldage [ametlikult Microsofti lehelt](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Nõutav: MIME-tüüp Markdown-failidele

Et tagada Markdown-failide (`.md`) korrektne serveerimine IIS-is:

1. Avage **IIS Manager** (vajutage `Win + R`, tippige `inetmgr`, vajutage Enter)
2. Navigeerige **Your Site > MIME Types**
3. Klõpsake **Add...**
4. Konfigureerige:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Oluline"

    Ilma selle seadeteta ei pruugi `.md` failid korralikult teenindatavad olla.

---

### Apache Tomcat seadistus {: #apache-tomcat-setup }

#### Ülevaade

Apache Tomcat on avatud lähtekoodiga Java servlet konteiner ja veebiserver.

#### Paigaldamine

1. **Laadige alla Apache Tomcat**
   - Külastage [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Laadige alla Windows ZIP distributsioon

2. **Pakkige arhiiv lahti**
   - Ekstraktige ZIP-fail süsteemi kataloogi
   - Näide: `C:\Program Files\Apache Tomcat`

3. **Kontrollige, et Tomcat töötab**
   - Avage brauser
   - Navigeerige `http://localhost:8080`
   - Peaksite nägema Apache Tomcat tervitussaiti

!!! tip "Näpunäide"

    Apache Tomcat tavaliselt käivitub automaatselt pärast paigaldust. Kui see ei käivitu, minge `bin` kausta ja käivitage `startup.bat`.

---

## Esmane paigaldus {: #initial-installation }

### 1. samm: Looge digna reposiitiorium

digna reposiitiorium salvestab kõik digna poolt arvutatud mõõdikud. See toimib keskse andmebaasina analüütilistele ja jõudlusandmetele.

#### Looge skeem ja kasutaja

Avage oma PostgreSQL klient (pgAdmin, psql või sarnane) ja käivitage järgmised SQL-käsud:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Asendage järgmised kohatäitjad:**

- `<digna_repo_schema>` — soovitud skeemi nimi (nt `dignarepo`)
- `<digna_repo_user>` — soovitud kasutajanimi (nt `digna_user`)
- `<digna_repo_password>` — turvaline parool sellele kasutajale

**Näide:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Parim tava"

    Kasutage tugevaid, keerukaid paroole andmebaasi kasutajatele. Vältige kergesti äraarvatavaid mandaate.

---

### 2. samm: Ekstraktige digna paigalduspakett

1. Leidke teile antud digna paigaldus ZIP-fail
2. Pakkige see soovitud paigalduskataloogi
3. Pärast ekstraktimist peaksite nägema järgmisi elemente:
   - `dashboard/` — veebidashboardi liides
   - `digna` — põhiühildatav käivitatav fail (backend + CLI)
   - `config.toml` — konfiguratsioonifail
   - `license.toml` — litsentsifail (paigaldage oma fail siia)

### 3. samm: Paigaldage litsentsifail

!!! warning "Oluline"

    Litsentsifail ei ole paigalduspaketis kaasas ja seda antakse eraldi digna poolt.

1. Leidke teile antud `license.toml` fail
2. Kopeerige see digna paigalduskataloogi (samasse kohta, kus asuvad `config.toml` ja `digna` käivitatav fail)

**Miks see oluline on:**
Litsentsifail sisaldab kliendiinfot, litsentsi aegumiskuupäeva ja digiallkirja. **Ärge muutke seda faili** — mis tahes muudatused tühistavad selle.

**Kataloogistruktuur pärast seadistust:**

```
digna_installation/
├── config.toml         (konfiguratsioonifail)
├── license.toml        (TEIE LITSENTSFALL - kopeerige siia)
├── digna               (põhi käivitatav fail)
└── dashboard/          (veebiliides)
    └── (dashboard failid)
```

---

## Backendi konfiguratsioon {: #backend-configuration }

### 1. samm: Looge ja redigeerige konfiguratsioonifaili

Teie digna paigalduskataloogis on olemas `config_template.toml` fail. Vajalik on selle ümbernimetamine `config.toml`-iks.

**Asukoht:** `digna_installation/config.toml`

Avage `config.toml` tekstiredaktoris ja konfigureerige alljärgnevad sektsioonid.

#### [app] sektsioon

See sektsioon seadistab digna backend rakenduse seaded:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Value | Märkused |
|---|---|---|
| `digna_APP_HOST` | `localhost` või IP-aadress | Hostinimi või IP, kus dignabackend majutatakse |
| `digna_APP_PORT` | `8082` (vaikimisi) | Port REST API endpointide jaoks |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendi URL | Kui dashboard on teisel serveril, lisage selle URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutav CORS-i puhul koos mandaadiga |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Lubab kõiki HTTP meetodeid |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Lubab kõiki päiseid |

#### [repo] sektsioon

See sektsioon seadistab ühenduse PostgreSQL andmebaasiga:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Value | Märkused |
|---|---|---|
| `digna_REPO_HOST` | `localhost` või IP | PostgreSQL serveri hostinimi/IP |
| `digna_REPO_PORT` | `5432` (vaikimisi) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Andmebaasi nimi |
| `digna_REPO_SCHEMA` | `dignarepo` | Varem loodud skeem |
| `digna_REPO_USER` | `digna_user` | PostgreSQL-is loodud kasutaja |
| `digna_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |

#### [base] sektsioon

See sektsioon sisaldab turbe- ja küpsiste seadeid:

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

| Parameter | Value | Märkused |
|---|---|---|
| `digna_FERNET_KEY` | Krüpteerimisvõti | Kasutatakse tokenite ja küpsiste krüpteerimiseks (vaikeväärtus võimalik) |
| `digna_COOKIE_DOMAIN` | `localhost` | Peaks vastama teie frontendi domeenile |
| `digna_COOKIE_SECURE` | `false` (lokaalne) / `true` (tootmine) | Kasutage `true` HTTPS ühenduste puhul |
| `digna_COOKIE_HTTPONLY` | `true` | Alati lubatud turvalisuse huvides |
| `digna_COOKIE_SAME_SITE` | `lax` | Aitab vältida CSRF rünnakuid |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Seansi aegumisaeg sekundites |
| `digna_MAX_WORKERS` | CPU tuumade arv - 1 | Paralellsete inspekteerimistöötajate arv |

#### [logging] sektsioon

See sektsioon seadistab logimise käitumist:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Value | Märkused |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` tootmises, `DEBUG` tõrkeotsinguks |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Säilitavate päevade arvu logivarundustes |

---

### 3. samm: Reposiitioriumi initsialiseerimine

1. Avage käsurida
2. Liikuge digna paigalduskataloogi (kus asuvad `config.toml` ja `digna` käivitatav fail)
3. Käivitage ühenduse test:

```bash
digna repo check
```

Te peaksite nägema kinnitust, et ühendus on loodud (repositoorium ise ei ole veel initsialiseeritud).

### 4. samm: Reposiitioriumi skeemi install

Samas kaustas käivitage:

```bash
digna repo install
```

See käsk loob vajalikud tabelid ja skeemi teie PostgreSQL andmebaasis.

### 5. samm: digna serveri käivitamine

digna paigalduskataloogis käivitage server:

```bash
digna serve --address <host> --port <port>
```

**Parameetrid:**
- `--address` — serveri hostinimi/IP
- `--port` — serveri port

Peaksite nägema käivitussõnumeid, mis kinnitavad serveri tööd:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### 6. samm: Admin-kasutaja loomine

1. Avage **uus** käsurida
2. Liikuge digna paigalduskataloogi
3. Käivitage järgmine käsk admin-kasutaja loomiseks:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Näide:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

See loob kasutaja täielike administraatoriõigustega.

!!! tip "Parim tava"

    Kasutage tugevat parooli, mis sisaldab suuri ja väikesi tähti, numbreid ja erimärke.

---

## Dashboardi konfiguratsioon {: #dashboard-configuration }

### 1. samm: Dashboardi juurutamine veebiserverisse

digna dashboardil on eraldi `config.toml` fail, mis asub `dashboard/` kataloogis. See konfiguratsioon on paigaldusel juba olemas ja seda ei pea esialgsel seadistusel muutma. Vajadusel kohandamiseks (nt multi-instances) muutke seda vastavalt dokumentatsioonile.

Valige veebiserver ja järgige vastavaid juurutusjuhiseid.

#### IIS-i paigaldamine

1. **Avage IIS Manager**
   - Vajutage `Win + R`, tippige `inetmgr`, vajutage Enter

2. **Looge uus veebisait**
   - Vasakul paanil paremklõpsake **Sites**
   - Valige **Add Website...**

3. **Konfigureerige veebisait**
   - **Site Name**: Sisestage nimi (nt "dignaDashboard")
   - **Physical Path**: Klõpsake Browse ja valige oma `dashboard` kaust
   - **Binding**: Määrake IP-aadress ja port (vaikeport HTTP jaoks 80, HTTPS jaoks 443)

4. **Käivitage veebisait**
   - Klõpsake **OK**, et saidi luua
   - Paremklõpsake äsja loodud saidil ja valige **Start**

5. **Testige paigaldust**
   - Avage brauser
   - Navigeerige aadressile `http://localhost` (või teie konfigureeritud URL)
   - Peaksite nägema digna dashboardi sisselogimislehte

#### Apache Tomcat juurutamine

1. **Kopeerige dashboard Tomcati**
   - Kopeerige `dashboard` kaust Tomcati `webapps` kataloogi
   - Nimetage vajadusel ümber (nt `digna`)
   - Näide: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Kontrollige juurutust**
   - Värskendage või laadige uuesti Tomcati halduslehte (http://localhost:8080)
   - Peaksite nägema loendis "digna" (või valitud nime) rakenduste hulgas

3. **Juurdepääs dashboardile**
   - Avage brauser
   - Navigeerige aadressile `http://localhost:8080/digna`
   - Peaksite nägema digna dashboardi sisselogimislehte

---

## digna käivitamine Windowsi teenusena {: #running-digna-as-a-windows-service }

### Miks kasutada Windowsi teenust?

digna backendi käivitamine Windowsi teenusena tagab, et see:
- Käivitub automaatselt serveri buutimisel
- Jookseb taustal ilma avatud käsurida aknata
- Taaskäivitub automaatselt, kui see jookseb kokku
- On hallatav läbi Windows Services halduri

### Teenuse haldusfailid

Kõik vajalikud failid asuvad digna paigalduskataloogis allosas: `bin/`

Järgnevad batch-failid on saadaval:
- `install_service.bat` — registreerib digna Windowsi teenusena
- `uninstall_service.bat` — eemaldab registreeritud teenuse
- `start_service.bat` — käivitab teenuse
- `stop_service.bat` — peatab teenuse

!!! warning "Administraatori õigused vajalikud"

    Kõiki batch-faile tuleb käivitada administraatori õigustes.

### Teenuse paigaldamine

1. **Avage käsurida administraatorina**
   - Paremklõpsake käsurida
   - Valige "Run as Administrator" (Käivita administraatorina)

2. **Liikuge bin kausta**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Käivitage paigaldusskript**
   ```bash
   install_service.bat
   ```

digna server on nüüd registreeritud Windowsi teenusena automaatse käivitusega. Teenus ei pruugi alustada koheselt — vaadake järgmist jaotist teenuse käivitamiseks.

### Teenuse käivitamine ja peatamine

#### Teenuse käivitamiseks

1. Avage käsurida administraatorina
2. Liikuge `digna\bin` kausta
3. Käivitage:
   ```bash
   start_service.bat
   ```

#### Teenuse peatamiseks

1. Avage käsurida administraatorina
2. Liikuge `digna\bin` kausta
3. Käivitage:
   ```bash
   stop_service.bat
   ```

!!! tip "Näpunäide"

    Enne rakenduse failide uuendamist peatage teenus alati.

### Teenuse liigutamine uude kataloogi

Kui peate digna paigalduskataloogi teisaldama:

1. **Desinstallige praegune teenus**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Liigutage rakenduse failid**
   - Liigutage kogu digna paigalduskataloog uude asukohta

3. **Installige teenus uuesti**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Käivitage teenus**
   ```bash
   start_service.bat
   ```

### Teenuse eemaldamine

1. **Peatage töötav teenus**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Eemaldage teenus**
   ```bash
   uninstall_service.bat
   ```

digna server on nüüd Windowsi teenustena registreerimisest eemaldatud.

---

## Uuendamine uuele versioonile {: #upgrading-to-a-new-release }

### Enne uuendamist

**digna reposiitioriumi varundamine on kohustuslik**

Enne digna uuendamist varundage kindlasti oma reposiitiorium (PostgreSQL), et vältida andmekadu. Varukoopia võimaldab taastada andmed, kui uuendamisel tekib ootamatuid probleeme.

### Uuendusprotsess

#### 1. samm: Peatage digna teenus

Kui digna töötab Windowsi teenusena, peatage see esmalt:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2. samm: Varundage praegune backend paigaldus

digna paigalduskataloogis:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### 3. samm: Ekstraktige ja juurutage uus versioon

1. Ekstraktige uus digna paigaldus ZIP-fail
2. Kopeerige uus `digna` käivitatav fail ja `dashboard` kaust oma paigalduskataloogi

!!! warning "Oluline"

    `config.toml` faili EI OLE kunagi kaasas paigaldus-ZIP-is. Teie olemasolev konfiguratsioon jääb samaks.

### 4. samm: Taastage konfiguratsioonifailid

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### 5. samm: Reposiitioriumi skeemi uuendamine

Liikuge digna paigalduskataloogi ja käivitage:

```bash
digna repo upgrade
```

See värskendab PostgreSQL skeemi uusimale versioonile, säilitades kogu olemasoleva andmebaasi sisu.

### 6. samm: Teenuste taaskäivitamine

Kui kasutate Windowsi teenust:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Kui käivitate käsitsi, taaskäivitage server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Kui kasutate IIS-i või Tomcatit, taaskäivitage vastav veebiserver.

#### 7. samm: Uuenduse kontrollimine

1. Avage digna dashboard
2. Kontrollige, et liides laaditakse korrektselt
3. Vaadake serverilogisid võimalike vigade osas
