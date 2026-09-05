---
title: Windowsi paigaldusjuhend – digna väljalase 2026.06 | digna dokumentatsioon
description: Samm-sammuline juhend digna väljalaske 2026.06 installimiseks Windowsis — süsteeminõuded, PostgreSQL seadistus, veebiserveri konfiguratsioon, backendi ja juhtpaneeli konfiguratsioon, digna käivitamine Windowsi teenusena ja uuendamine uuele versioonile.
keywords: digna windows paigaldus, digna juurutusjuhend, digna backendi seadistus, digna juhtpaneeli paigaldus, postgresql seadistus, digna windows teenus, digna uuendamisjuhend
image: /assets/logo_square.png
---

# Windowsi paigaldusjuhend digna väljalaske 2026.06 jaoks

**Väljalase:** 2026.06

**Viimati uuendatud:** 30. august 2026


---

## Sisu

1. [Sissejuhatus](#introduction)
2. [Süsteeminõuded](#system-requirements)
3. [Enne paigaldust tehtavad toimingud](#pre-installation-setup)
4. [PostgreSQL serveri seadistus](#postgresql-server-setup)
5. [Veebiserveri konfiguratsioon](#web-server-configuration)
6. [Esmane paigaldus](#initial-installation)
7. [Backendi konfiguratsioon](#backend-configuration)
8. [Juhtpaneeli konfiguratsioon](#dashboard-configuration)
9. [digna käitamine Windowsi teenusena](#running-digna-as-a-windows-service)
10. [Uuendamine uuele versioonile](#upgrading-to-a-new-release)

---

## Sissejuhatus {: #introduction }

### Teave digna kohta

digna on kõikehõlmav AI-käitusel põhinev platvorm, mis on loodud andmekvaliteedi haldamise optimeerimiseks erinevates andmekeskkondades nagu andmelaod, andmejärved ja lakehoused. Suure skaleeritavuse ja kohandatavusega digna tegeleb kaasaegsete andmeprobleemidega automatiseerimise, reaalajas monitooringu ja anomaaliate tuvastuse kaudu.

digna koosneb kahest põhilisest komponendist:

- **dignabackend**: rakenduse tuum, mis vastutab andmete töötlemise ja kvaliteedikontrollide eest.
- **dignadashboard**: veebipõhine liides, mis majutatakse veebiserveris ja pakub kasutajasõbralikku viisi digna platvormiga suhtlemiseks ning andmekvaliteedi mõõdikute visualiseerimiseks.

### Mis on uut väljalaskes 2026.06

See väljalase toob andmete jälgitavuse võimekused otse teie koodi, võimaldades arendajatel jälgida andmekvaliteeti allikas. Täielike üksikasjade jaoks vaadake [väljalasete märkmeid](http://docs.digna.ai/changelog/Release_202606/).

### Otsite macOS-i või Linuxi?

See juhend käsitleb Windowsi. Muude platvormide jaoks vaadake [macOS-i paigaldusjuhendit](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) või [Linuxi paigaldusjuhendit](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Süsteeminõuded {: #system-requirements }

Enne paigalduse alustamist veenduge, et teie süsteem vastab järgmistele miinimumnõuetele:

| Nõue | Spetsifikatsioon |
|---|---|
| **Operatsioonisüsteem** | Windows Server või Windows 10/11 |
| **Mälu (minimaalne paigaldus)** | 16 GB RAM |
| **Kettaruumi** | 10 GB vaba salvestusruumi |
| **Andmebaas** | PostgreSQL Server 12 või uuem |
| **Veebiserver** | IIS, Apache Tomcat või ekvivalent |

### Andmebaasi paigaldusvalikud

**Kui PostgreSQL on juba paigaldatud:**
Võite oma olemasolevale PostgreSQL-serverile lisada uue andmebaasi digna jaoks.

**Kui paigaldate PostgreSQL-i samasse masinasse, kus töötab digna:**

!!! info "Soovitatavad spetsifikatsioonid"

    - **Mälu**: 32 GB RAM (16 GB asemel)
    - **Kettaruumi**: 50 GB vaba salvestusruumi (10 GB asemel)

    Need kõrgemad spetsifikatsioonid võimaldavad dignal ja PostgreSQL-il samaaegselt tõhusalt töötada.

---

## Enne paigaldust tehtavad toimingud {: #pre-installation-setup }

Enne digna paigaldamist veenduge, et kaks peamist eeltingimust on täidetud:

1. **PostgreSQL Server** – arvutatud mõõdikute ja jõudlusandmete salvestamiseks
2. **Veebiserver** – digna juhtpaneeli majutamiseks

Kui need komponendid pole veel seadistatud, järgige allolevaid lõike nende paigaldamiseks ja konfiguratsiooniks.

---

## PostgreSQL serveri seadistus {: #postgresql-server-setup }

### Kui teil on PostgreSQL juba olemas

Kui PostgreSQL on juba paigaldatud ja töötab teie lokaalses masinas või kasutate hallatavat kaug-PostgreSQL-serverit, võite liikuda otse järgmisse jaotisse: [veebiserveri konfiguratsioon](#web-server-configuration).

### PostgreSQL-i paigaldamine

Järgige neid samme PostgreSQL-i paigaldamiseks Windowsi:

#### Samm 1: Laadige alla PostgreSQL

1. Minge lehele [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Valige **Windows**
3. Laadige alla viimane installeerija

#### Samm 2: Käivitage installeerija

1. Topeltklõpsake alla laaditud installeerijafailil
2. Järgige seadistusviisardi juhiseid

#### Samm 3: Valige paigalduse kataloog

Valige kataloog, kuhu PostgreSQL paigaldatakse. Vaikekoht on tavaliselt sobiv.

#### Samm 4: Valige komponendid

Tavalise paigalduse jaoks jätke vaikimisi valitud komponendid.

#### Samm 5: Määrake PostgreSQL-i superkasutaja parool

Sisestage ja kinnitage parool PostgreSQL-i superkasutajale (`postgres`). **Salvestage see parool turvaliselt** — teil on seda hiljem vaja.

#### Samm 6: Konfigureerige pordinumber

Vaikeport PostgreSQL-ile on `5432`. Võite kasutada vaikimisi või määrata vajadusel teise pordi.

!!! tip "Vihje"

    Kui port 5432 on juba kasutusel, valige alternatiivne port ja märkige see hilisemaks konfiguratsiooniks üles.

#### Samm 7: Valige lokaliseerimine

Valige andmebaasi lokaliseerimine. Vaikeväärtus sobib tavaliselt enamiku paigalduste jaoks.

#### Samm 8: Lõpetage paigaldus

Klõpsake ülejäänud sammudes **Next**, seejärel **Finish**.

#### Samm 9: Kontrollige paigaldust

Avage käsuviip ja kontrollige, kas PostgreSQL on paigaldatud:

```bash
psql --version
```

Kui paigaldus õnnestus, kuvatakse PostgreSQL-i versioon.

---

## Veebiserveri konfiguratsioon {: #web-server-configuration }

digna vajab veebiserverit juhtpaneeli majutamiseks. Valige üks järgmistest võimalustest:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Vajate ainult ühe neist serveritest paigaldamist ja konfiguratsiooni.

### IIS-i seadistus {: #iis-setup }

#### Ülevaade

Internet Information Services (IIS) on Microsofti veebiserver veebisaitide ja veebirakenduste majutamiseks.

#### IIS-i lubamine

1. **Avage juhtpaneel**
   - Vajutage `Win + R`
   - Tippige `control` ja vajutage Enter

2. **Minge Windowsi funktsioonide juurde**
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
   - Minge aadressile `http://localhost`
   - Te peaksite nägema IIS-i tervituse lehte

#### Nõutav: URL Rewrite moodul

IIS nõuab URL Rewrite komponenti. Laadige see alla ja paigaldage sellelt [official Microsoft page](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Nõutav: MIME-tüüp Markdown-failide jaoks

Et tagada Markdown-failide (`.md`) korrektne teenindamine IIS-is:

1. Avage **IIS Manager** (vajutage `Win + R`, tippige `inetmgr`, vajutage Enter)
2. Minge **Your Site > MIME Types**
3. Klõpsake **Add...**
4. Konfigureerige:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Tähtis"

    Ilma selle säteta ei pruugi `.md` faile õigesti teenindada.

---

### Apache Tomcati seadistus {: #apache-tomcat-setup }

#### Ülevaade

Apache Tomcat on avatud lähtekoodiga Java servlet-konteiner ja veebiserver.

#### Paigaldamine

1. **Laadige alla Apache Tomcat**
   - Minge lehele [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Laadige alla Windowsi ZIP-versioon

2. **Pakkige arhiiv lahti**
   - Pakkige ZIP-fail lahti sobivasse kataloogi
   - Näide: `C:\Program Files\Apache Tomcat`

3. **Kontrollige, et Tomcat töötab**
   - Avage brauser
   - Minge aadressile `http://localhost:8080`
   - Te peaksite nägema Apache Tomcati tervituslehte

!!! tip "Vihje"

    Apache Tomcat peaks enamasti käivituma automaatselt pärast paigaldust. Kui see ei käivitu, minge `bin` kausta ja käivitage `startup.bat`.

---

## Esmane paigaldus {: #initial-installation }

### Samm 1: Looge digna andmehoidla skeem

digna andmehoidla salvestab kõik digna poolt arvutatud mõõdikud. See toimib analüütilise ja jõudlusandmete keskse andmebaasina.

#### Looge skeem ja kasutaja

Avage oma PostgreSQL klient (pgAdmin, psql või sarnane) ja täitke järgmised SQL-käsud:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Asendage järgmised kohatäitjad:**

- `<digna_repo_schema>` — Teie soovitud skeemi nimi (näiteks `dignarepo`)
- `<digna_repo_user>` — Teie soovitud kasutajanimi (näiteks `digna_user`)
- `<digna_repo_password>` — Turvaline parool selle kasutaja jaoks

**Näide:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Parim praktika"

    Kasutage andmebaasi kasutajate jaoks tugevaid, keerukaid paroole. Vältige lihtsalt äraarvatavaid tunnuseid.

---

### Samm 2: Pakkige digna paigalduspakett lahti

1. Leidke teile antud digna paigaldamise ZIP-fail
2. Pakkige see soovitud paigalduskataloogi
3. Pärast lahtipakkimist peaksite nägema järgmisi üksusi:
   - `dashboard/` — Veebijuhtpaneeli liides
   - `digna` — Peamine täitmisfail (backend + CLI kombineeritud)
   - `config.toml` — Konfiguratsioonifail
   - `license.toml` — Litsentsifail (kopeerige oma fail siia)

### Samm 3: Paigaldage litsentsifail

!!! warning "Tähtis"

    Litsentsifail EI OLE paigalduspaketis ja see antakse teile eraldi digna poolt.

1. Leidke teile antud `license.toml` fail
2. Kopeerige see digna paigalduskausta juurkausta (kuhu on paigaldatud `config.toml` ja `digna` täitmisfail)

**Miks see oluline on:**
Litsentsifail sisaldab teie kliendiandmeid, litsentsi aegumiskuupäeva ja digitaalset allkirja. **Ärge muutke seda faili** — kõik muudatused annuleerivad selle.

**Kataloogistruktuur pärast seadistust:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backendi konfiguratsioon {: #backend-configuration }

### Samm 1: Looge ja redigeerige konfiguratsioonifaili

Kaustas on teile antud `config_template.toml` fail. Te peate selle ümber nimetama `config.toml`-ks.

**Asukoht:** `digna_installation/config.toml`

Avage `config.toml` tekstiredaktoris ja kohandage allpool toodud sektsioone.

#### [app] sektsioon

See sektsioon konfigureerib digna backendi rakenduse seadeid:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_APP_HOST` | `localhost` või IP-aadress | Hostinimi või IP, kus dignabackend jookseb |
| `digna_APP_PORT` | `8082` (vaikimisi) | Port REST API lõpp-punktide jaoks |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendi URL | Kui juhtpaneel on teisel serveril, lisage selle URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutud CORS-i jaoks koos tunnustega |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Lubab kõik HTTP meetodid |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Lubab kõik päised |

#### [repo] sektsioon

See sektsioon konfigureerib ühenduse PostgreSQL andmebaasiga:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_REPO_HOST` | `localhost` või IP | PostgreSQL serveri hostinimi/IP |
| `digna_REPO_PORT` | `5432` (vaikimisi) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Andmebaasi nimi |
| `digna_REPO_SCHEMA` | `dignarepo` | Varem loodud skeem |
| `digna_REPO_USER` | `digna_user` | PostgreSQL seadistuses loodud kasutaja |
| `digna_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |

#### [base] sektsioon

See sektsioon sisaldab turva- ja küpsise seadeid:

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

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_FERNET_KEY` | Krüpteerimisvõti | Kasutatakse tokenite ja küpsiste krüpteerimiseks (vaikeväärtus olemas) |
| `digna_COOKIE_DOMAIN` | `localhost` | Vastab teie frontendi domeenile |
| `digna_COOKIE_SECURE` | `false` (lokaalne) / `true` (tootmises) | Kasutage `true` HTTPS-ühenduse korral |
| `digna_COOKIE_HTTPONLY` | `true` | Alati lubatud turvalisuse huvides |
| `digna_COOKIE_SAME_SITE` | `lax` | Aitab vältida CSRF-rünnakuid |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumisaeg sekundites |
| `digna_MAX_WORKERS` | CPU tuumade arv - 1 | Paralleelsete kontrollitööde arv |

#### [logging] sektsioon

See sektsioon konfigureerib logimise käitumist:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` tootmisse, `DEBUG` tõrkeotsingu jaoks |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Päevaste logivarukoopiate arv, mida säilitatakse |

---

### Samm 3: Initsialiseeri andmehoidla ühendus

1. Avage käsuviip
2. Minge oma digna paigalduskausta (kus asuvad `config.toml` ja `digna` täitmisfail)
3. Käivitage ühenduse test:

```bash
digna repo check
```

Te peaksite nägema kinnitust, et ühendus on loodud (andmehoidla ennast pole veel initsialiseeritud).

### Samm 4: Paigaldage andmehoidla skeem

Selles samas kataloogis käivitage:

```bash
digna repo install
```

See käsk installib vajalikud tabelid ja skeemi teie PostgreSQL andmebaasi.

### Samm 5: Käivitage digna server

Digna paigalduskaustas käivitage server:

```bash
digna serve --address <host> --port <port>
```

**Parameetrid:**
- `--address` — serveri hostinimi/IP
- `--port` — serveri port 

Peaksite nägema käivituse sõnumeid, mis kinnitavad serveri tööle hakkamist:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Samm 6: Looge administraatorkasutaja

1. Avage **uus** käsuviip
2. Minge oma digna paigalduskausta
3. Käivitage järgmine käsk administraatori kasutaja loomiseks:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Näide:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

See loob kasutaja täisadministratiivsete õigustega.

!!! tip "Parim praktika"

    Kasutage tugevat parooli, mis sisaldab suur- ja väiketähti, numbreid ja erimärke.

---

## Juhtpaneeli konfiguratsioon {: #dashboard-configuration }

### Samm 1: Paigutage juhtpaneel veebiserverisse

digna juhtpaneelil on oma eraldi `config.toml` fail, mis asub `dashboard/` kataloogis. See konfiguratsioon on juba kaasas ega vaja esialgsel seadistusel muutmist. Vajadusel kohandage seda ainult siis, kui peate muutma backendi ühenduse sätteid.

Kui peate juhtpaneeli konfiguratsiooni muutma (nt mitme instantsi juurutamisel), vaadake vastavat dokumentatsiooni.

Valige veebiserver ja järgige vastavaid juurutusjuhiseid.

#### Paigutamine IIS-i

1. **Avage IIS Manager**
   - Vajutage `Win + R`, tippige `inetmgr`, vajutage Enter

2. **Looge uus veebisait**
   - Vasakul paneelil paremklõpsake **Sites**
   - Valige **Add Website...**

3. **Konfigureerige veebisait**
   - **Site Name**: Sisestage nimi (nt "dignaDashboard")
   - **Physical Path**: Klõpsake Browse ja valige `dashboard` kaust
   - **Binding**: Määrake IP-aadress ja port (vaikeport HTTP jaoks on 80, HTTPS jaoks 443)

4. **Käivitage veebisait**
   - Klõpsake **OK**, et saiti luua
   - Paremklõpsake uuel saidil ja valige **Start**

5. **Testige paigaldust**
   - Avage brauser
   - Minge aadressile `http://localhost` (või teie konfigureeritud URL)
   - Te peaksite nägema digna juhtpaneeli sisselogimislehte

#### Paigutamine Apache Tomcati

1. **Kopeerige juhtpaneel Tomcati**
   - Kopeerige `dashboard` kaust Tomcati `webapps` kataloogi
   - Nimetage see vajadusel ümber (nt `digna`)
   - Näide: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Kontrollige juurutust**
   - Värskendage või laadige uuesti Tomcati halduslehte (http://localhost:8080)
   - Te peaksite nägema loendis "digna" (või valitud nime)

3. **Juurdepääs juhtpaneelile**
   - Avage brauser
   - Minge aadressile `http://localhost:8080/digna`
   - Te peaksite nägema digna juhtpaneeli sisselogimislehte

---

## digna käitamine Windowsi teenusena {: #running-digna-as-a-windows-service }

### Miks kasutada Windowsi teenust?

digna backendi käitamine Windowsi teenusena tagab:
- Teenuse automaatse käivitumise serveri buutimisel
- Taustal töötamise ilma avatud käsuviibata
- Automaatse taaskäivituse jooksmisel
- Halduse võimaluse Windows Services kaudu

### Teenuse haldusfailid

Kõik vajalikud failid asuvad digna paigalduskaustas alamkaustas: `bin/`

Järgnevad batch-failid on saadaval:
- `install_service.bat` — registrib digna Windowsi teenusena
- `uninstall_service.bat` — eemaldab teenuse registrist
- `start_service.bat` — käivitab teenuse
- `stop_service.bat` — peatab teenuse

!!! warning "Nõutud administraatoriõigused"

    Kõik batch-failid tuleb käivitada administraatoriõigustega.

### Teenuse paigaldamine

1. **Avage käsuviip administraatorina**
   - Paremklõpsake Command Prompt
   - Valige "Run as Administrator"

2. **Minge bin kausta**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Käivitage paigaldusskript**
   ```bash
   install_service.bat
   ```

Digna server on nüüd registreeritud Windowsi teenusena, mille põhikäivituse tüübiks on seatud automaatne. Teenus ei pruugi käivituda kohe — vaadake järgmist jaotist teenuse käivitamiseks.

### Teenuse käivitamine ja peatamine

#### Teenuse käivitamiseks

1. Avage käsuviip administraatorina
2. Minge `digna\bin`
3. Käivitage:
   ```bash
   start_service.bat
   ```

#### Teenuse peatamiseks

1. Avage käsuviip administraatorina
2. Minge `digna\bin`
3. Käivitage:
   ```bash
   stop_service.bat
   ```

!!! tip "Vihje"

    Enne rakenduse failide uuendamist peatage teenus alati.

### Teenuse liigutamine uude kataloogi

Kui peate digna paigalduskausta teisaldama:

1. **Desinstallige praegune teenus**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Liigutage rakenduse failid**
   - Liigutage kogu digna paigalduskaust uude asukohta

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

1. **Peatage jooksvalt olev teenus**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Desinstallige teenus**
   ```bash
   uninstall_service.bat
   ```

Digna server on nüüd registrist eemaldatud.

---

## Uuendamine uuele versioonile {: #upgrading-to-a-new-release }

### Enne uuendamist

**digna andmehoidla varundamine on kohustuslik**

Enne digna uuendamist varundage oma andmehoidla (PostgreSQL), et kaitsta andmete kaotsimineku eest.
Varukoopia tagab taastumise juhuks, kui uuendamisel tekib ootamatuid probleeme.

### Uuendusprotsess

#### Samm 1: Peatage digna teenus

Kui digna töötab Windowsi teenusena, peatage see esmalt:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Samm 2: Varundage praegune backendi paigaldus

Teie digna paigalduskaustas:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Samm 3: Pakkige ja paigutage uus versioon

1. Pakkige uus digna paigaldus ZIP-fail lahti
2. Kopeerige uus `digna` täitmisfail ja `dashboard` kaust oma paigalduskausta

!!! warning "Tähtis"

    `config.toml` fail EI OLE kunagi kaasatud paigaldus-ZIP-is. Teie olemasolev konfiguratsioon jääb puutumatuks.

### Samm 4: Taastage oma konfiguratsioonifailid

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Samm 5: Uuendage andmehoidla skeemi

Minge oma digna paigalduskausta ja käivitage:

```bash
digna repo upgrade
```

See uuendab PostgreSQL skeemi uusimale versioonile, säilitades kõik olemasolevad andmed.

### Samm 6: Taaskäivitage teenused

Kui käivitate teenust Windowsi teenusena:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Kui käivitate käsitsi, taaskäivitage server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Kui kasutate IIS-i või Tomcati, taaskäivitage vastav veebiserver.

#### Samm 7: Kinnitage uuendus

1. Avage digna juhtpaneel
2. Veenduge, et liides laeb korralikult
3. Kontrollige serverilogisid võimalike vigade osas