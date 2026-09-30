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

- **digna**: rakenduse tuum, mis vastutab andmete töötlemise ja kvaliteedikontrollide läbiviimise eest. See ühendab taustasüsteemi ja käsurealiidese üheks käivitatavaks failiks ning asendab varasemate väljalasete eraldi programmid `dignabackend` ja `dignacli`.
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

!!! info "Konfiguratsiooni- ja litsentsifailid ei ole paketis"

    Paigaldusega ei kaasne ei `config.toml` ega `dashboard/dashboard_config.toml` — mõlemad
    loote ise, jaotistes [Taustasüsteemi konfigureerimine](#backend-configuration) ja
    [Juhtpaneeli konfiguratsioon](#dashboard-configuration). Ka `license.toml` ei ole kaasas;
    digna tarnib selle eraldi, nagu kirjeldab samm 3.

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
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
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

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Vastab teie frontendi domeenile |
| `digna_COOKIE_SECURE` | `false` (lokaalne) / `true` (tootmises) | Kasutage `true` HTTPS-ühenduse korral |
| `digna_COOKIE_HTTPONLY` | `true` | Alati lubatud turvalisuse huvides |
| `digna_COOKIE_SAME_SITE` | `lax` | Aitab vältida CSRF-rünnakuid |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumisaeg sekundites |
| `digna_MAX_WORKERS` | CPU tuumade arv - 1 | Paralleelsete kontrollitööde arv |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maksimaalne viivitus sekundites, mille ajastaja võib lisada enne tähtajalise töö käivitamist |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Kellaaeg (24 tunni vorming `HH:MM`), mil algab igapäevane puhastus |

#### [encryption] sektsioon

See sektsioon sisaldab võtit, millega krüpteeritakse hoidlas talletatud tundlikud väärtused. See on **kohustuslik** — `config check` teatab sektsioonist `[encryption]` FAILED, kui võti puudub.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-kodeeritud võti | Krüpteerib digna hoidlas talletatud tundlikud väärtused |

!!! warning "Kaitske faili config.toml"

    See võti on fikseeritud väärtus, mis on kõigis digna paigaldustes ühesugune, ja just see dekrüpteerib teie hoidla tundlikud väärtused. Piirake `config.toml` juurdepääs kontoga, mille all digna töötab, hoidke fail versioonihaldusest ja jagatud ketastest eemal ning jätke see välja igast varukoopiast, mida hoitakse vähem turvaliselt kui hoidlat ennast.

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

### Samm 2: Kontrollige konfiguratsiooni

Enne hoidla lähtestamist kontrollige, kas `config.toml` on täielik ja korrektselt üles ehitatud. Käivitage oma digna paigalduskataloogis:

```bash
digna config check
```

Iga sektsiooni kontrollitakse eraldi, nii et üks viga ei varja teiste olekut:

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

Parandage kõik, millest teatatakse FAILED, ja käivitage käsk enne jätkamist uuesti. Täielik valikute loend on [CLI viites](../../../cli/Command_Line_Interface_202606.md).

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

### Samm 5: Looge administraatorkasutaja

1. Avage **uus** käsuviip
2. Minge oma digna paigalduskausta
3. Käivitage järgmine käsk administraatori kasutaja loomiseks:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Näide:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

See loob kasutaja täisadministratiivsete õigustega.

!!! tip "Parim praktika"

    Kasutage tugevat parooli, mis sisaldab suur- ja väiketähti, numbreid ja erimärke.

---

### Samm 6: Käivitage digna server

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

!!! note "Server hoiab terminali hõivatuna"

    `serve` töötab esiplaanil ja jätkab, kuni peatate selle klahvidega ++ctrl+c++. Jätke see tööle, kuni seadistuse lõpetate; automaatseks käivitamiseks alglaadimisel vaadake [digna käitamine Windowsi teenusena](#running-digna-as-a-windows-service).

## Juhtpaneeli konfiguratsioon {: #dashboard-configuration }

### Samm 1: Paigutage juhtpaneel veebiserverisse

digna juhtpaneel loeb oma konfiguratsiooni failist `dashboard/dashboard_config.toml`. See fail ei ole paigaldusega kaasas — loote selle kataloogi `dashboard/` juhtpaneeli failide kõrvale.

Selle sisu on kirjeldatud jaotises [Ühekordne sisselogimine (SSO)](../../../sso/overview.md), kus faili ka vaja läheb: see sisaldab juhtpaneeli pakutavaid sisselogimisvalikuid ning mitme instantsi juurutuste puhul ühendust backendiga.

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

### Käsud `windows`

Teenust haldab käivitatav fail `digna` ise, alamkäskude `digna windows` kaudu. Käivitatavaid
batch-faile ei ole.

| Käsk | Otstarve |
|---|---|
| `digna windows install` | Registreerib digna Windowsi teenusena |
| `digna windows start` | Käivitab registreeritud teenuse |
| `digna windows stop` | Peatab töötava teenuse |
| `digna windows uninstall` | Eemaldab teenuse registreeringu |

!!! warning "Nõutud administraatoriõigused"

    Kõik neli käsku tuleb käivitada administraatorina avatud käsuviibas.

Iga käsk aktsepteerib valikut `--name`, et pöörduda teenuse poole, mis on registreeritud vaikimisi
nimest erineva nime all. Valikute täielik loend on [CLI teatmikus](../../../cli/Command_Line_Interface_202606.md).

### Teenuse paigaldamine

1. **Avage käsuviip administraatorina**
   - Paremklõpsake Command Prompt
   - Valige "Run as Administrator"

2. **Minge oma digna paigalduskausta**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registreerige teenus**
   ```bash
   digna windows install
   ```

!!! important "Määrake aadress ja port, kui vaikeväärtused teile ei sobi"

    `install` salvestab aadressi ja pordi teenuse registreeringusse ning teenus seotakse
    täpselt salvestatud väärtustega. Vaikeväärtused on `127.0.0.1` ja `8000`, mis võtavad
    ühendusi vastu ainult masinalt endalt. Teises hostis asuv juhtpaneel sinna ei ulatu, seega
    andke aadress, mida backend peab kuulama:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Neid väärtusi ei loeta failist `config.toml`. Nende hilisemaks muutmiseks eemaldage teenus
    ja paigaldage see uute väärtustega uuesti.

Teenus registreeritakse **automaatse käivitusega**, seega käivitub see koos Windowsiga. Kohe see
ei käivitu — vaadake järgmist jaotist.

#### Paigaldusvalikud

| Valik | Vaikeväärtus | Otstarve |
|---|---|---|
| `--name` | `digna` | Nimi, mille all teenus registreeritakse |
| `--display-name` | `digna` | Nimi, mida kuvatakse services.msc-s |
| `--description` | `digna data quality backend` | Kirjeldus, mida kuvatakse services.msc-s |
| `--address` | `127.0.0.1` | Aadress, millega teenus oma API seob |
| `--port` | `8000` | Port, millega teenus oma API seob |
| `--working-dir` | käivitatava faili `digna` kataloog | Kataloog, milles asuvad `config.toml` ja `license.toml` ning mille teenus teeb oma töökataloogiks |
| `--start-type` | `auto` | `auto` käivitub koos Windowsiga, `manual` käivitub ainult nõudmisel, `disabled` registreerib teenuse, kuid keeldub seda käivitamast |
| `--account` | `LocalSystem` | Konto, mille all teenus töötab, nt `DOMAIN\user` või `.\user` |
| `--password` | | Konto `--account` parool |

!!! tip "Käitamine domeenikonto all"

    Kontol `LocalSystem` puudub võrguidentiteet, seega ebaõnnestuvad Windowsi autentimine SQL
    Serveris ja igasugune juurdepääs võrgukaustale. Kui teenus peab ressurssidele juurde pääsema
    kindla kasutajana, paigaldage see valikutega `--account` ja `--password`.

### Teenuse käivitamine ja peatamine

#### Teenuse käivitamiseks

```bash
digna windows start
```

#### Teenuse peatamiseks

```bash
digna windows stop
```

!!! tip "Vihje"

    Enne rakenduse failide uuendamist peatage teenus alati.

### Teenuse liigutamine uude kataloogi

Kui peate digna paigalduskausta teisaldama:

1. **Peatage praegune teenus ja eemaldage selle registreering**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Liigutage rakenduse failid**
   - Liigutage kogu digna paigalduskaust uude asukohta

3. **Registreerige teenus uuest asukohast uuesti**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Korrake kõiki `--address`, `--port` või `--account` väärtusi, mida esimesel korral kasutasite —
   eelmine registreering on kadunud.

4. **Käivitage teenus**
   ```bash
   digna windows start
   ```

### Teenuse eemaldamine

1. **Peatage jooksvalt olev teenus**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Eemaldage teenuse registreering**
   ```bash
   digna windows uninstall
   ```

Digna server on nüüd registrist eemaldatud.

---

## Uuendamine uuele versioonile {: #upgrading-to-a-new-release }

### Enne uuendamist

**Kontrollige esmalt kõiki andmebreaühendusi**

Alates väljalaskest 2026.06 jõuab digna iga lähtetehnoloogiani **ODBC** kaudu. Varasemad väljalasked pakkusid valikut tehnoloogiapõhise draiveri ja ODBC vahel, mille valis lüliti **Use ODBC**. digna meeskond otsustas toetuda ainult ODBC-le, sest üks standardne liides annab rohkem kui hulk eritellimusel draivereid:

- **Autentimine** — autentimine on osa ODBC-st, seega saab ühendus kasutada kõike, mida tema draiver toetab: paroole, lubasid ja PAT-e, Kerberost ja Active Directoryt, MFA-d ja brauseripõhist ühekordset sisselogimist, pilveidentiteete, kliendisertifikaate ja TLS-i. Uued meetodid saabuvad koos draiveri uuendusega, mitte digna väljalaset oodates.
- **Andmebaasitootjate hooldatavad draiverid** — tootja enda draiver järgib uusi serveriversioone ja turvaparandusi ning te saate seda uuendada oma ajakava järgi, dignast sõltumatult.
- **Üks viis kõike seadistada** — iga tehnoloogia on võti-väärtus omaduste loend, sama liidese, sama tundlike väärtuste krüpteerimise ja sama tõrkeotsinguga, mitte erineva väljade komplektiga iga allika kohta.
- **Häälestus ja ulatus** — draiveri valikud nagu ajalõpud, TLS-i seaded, puhverserverid ja lugemismahud on saadaval iga allika jaoks ning ühendada saab iga tehnoloogia, millel on nõuetekohane ODBC draiver, sealhulgas need, mille kohta digna eraldi juhendit ei avalda.

Praktikas tähendab see, et lülitit **Use ODBC** ning eraldi hosti, pordi, andmebaasi, kasutaja ja parooli välju enam ei ole. **Iga ühendus, mis veel ODBC-d ei kasuta, tuleb viia üle ODBC-le** — automaatset teisendust ei ole, seega planeerige see enne uuendamist:

1. Vaadake läbi iga teie paigalduses määratud andmebaasiühendus ja märkige üles need, mis veel ODBC-d ei kasuta — igaüks neist tuleb uuesti seadistada.
2. Paigaldage vastav ODBC draiver digna hostile — ühendused avatakse serverist, kus töötab digna taustasüsteem, mitte brauserist. Vaadake [ODBC draiveri paigaldamine digna hostile](../../../databases/overview.md#install-the-driver).
3. Hoidke ODBC omadused iga puudutatud ühenduse jaoks valmis. [Tehnoloogiajuhendid](../../../databases/overview.md#technology-guides) loetlevad iga allika kohta läbi proovitud omaduste komplekti.

Pärast uuendamist viige iga puudutatud ühendus üle ODBC-le ja testige seda ttöölaualt — vaadake [Andmebaasiühenduse loomine](../../../databases/overview.md#create-a-database-connection) ja [Ühenduse testimine](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy ühendused"

    Databricks Legacy konnektor on selles väljalaskes eemaldatud. Viige need ühendused üle [Databricks](../../../databases/databricks_connector_guide.md) konnektorile.

**digna andmehoidla varundamine on kohustuslik**

Enne digna uuendamist varundage oma andmehoidla (PostgreSQL), et kaitsta andmete kaotsimineku eest.
Varukoopia tagab taastumise juhuks, kui uuendamisel tekib ootamatuid probleeme.

### Uuendusprotsess

#### Samm 1: Peatage vana teenus ja eemaldage selle registreering

Kui digna töötab Windowsi teenusena, peatage see **praeguse paigalduse batch-failidega**
— käsud `digna windows` kuuluvad uude väljalaskesse ega ole veel saadaval:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Seejärel eemaldage teenuse registreering, samuti vana batch-failiga. Registreering osutab vanale
käivitatavale failile ja selle skriptidele, mille see uuendus mõlemad asendab, seega ei saa seda
uuesti kasutada:

```bash
uninstall_service.bat
```

!!! warning "Eemaldage registreering enne, kui midagi ümber nimetate"

    `uninstall_service.bat` asub kaustas `bin`, mille kohe ümber nimetate, ja see on ainus, mis
    suudab eemaldada enda loodud registreeringu. Käivitage see siis, kui vana paigaldus on veel
    paigas. Kui kaust on juba ümber nimetatud, nimetage see tagasi, eemaldage registreering ja
    jätkake seejärel.

    Pange kirja konto, mille all teenus töötas, ning aadress ja port, millel see teenindas — neid
    läheb vaja sammus 9.

#### Samm 2: Varundage praegune paigaldus

Nimetage oma digna paigalduskataloogis praeguse paigalduse kaustad ümber, et uut väljalaset saaks nende kõrvale paigaldada:

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

!!! info "dignabackend ja dignacli ei ole enam kasutusel"

    Alates väljalaskest 2026.06 asendab `dignabackend` ja `dignacli` üksainus käivitatav fail `digna`, mis ühendab taustasüsteemi ja CLI. Hoidke `dignabackend_old` ja `dignacli_old` alles vaid seni, kuni olete uuenduse kontrollinud — seejärel võite mõlemad kaustad kustutada. Hoidke `dashboard_old` alles, kuni olete sellest oma konfiguratsioonifailid taastanud (vt samm 4). Ka kaust `bin` läheb: selle batch-failid juhtisid vana teenust ja 2026.06 neid enam ei tarni, seega pärast teenuse registreeringu eemaldamist sammus 1 on neist ainult segadust.

#### Samm 3: Pakkige ja paigutage uus versioon

1. Pakkige uus digna paigaldus ZIP-fail lahti
2. Kopeerige uus `digna` täitmisfail ja `dashboard` kaust oma paigalduskausta

!!! warning "Tähtis"

    Paigaldus-ZIP ei sisalda kunagi ei faili `config.toml` ega `dashboard/dashboard_config.toml`
    — digna meeskond ei tarni kumbagi faili. Seetõttu ei puuduta uuendus teie olemasolevat
    konfiguratsiooni ning ümbernimetatud `*_old` kaustades olevad koopiad on ainsad, mis teil on.

#### Samm 4: Taastage oma konfiguratsioonifailid

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Väljalase 2026.06 muudab faili config.toml"

    Kolm sätet on uued ja kohustuslikud, kolm ei ole enam kasutusel. Varasemast väljalaskest üle võetud `config.toml` uusi sätteid ei sisalda ja digna ei käivitu, kuni need puuduvad. Lisage oma olemasolevasse `config.toml` faili järgmine:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Lisage kaks `[base]` võtit oma olemasolevasse `[base]` sektsiooni ja lisage `[encryption]` uue sektsioonina. Seejärel eemaldage sätted, mida enam ei kasutata: **`digna_FERNET_KEY`** sektsioonist `[base]` ning **`digna_APP_HOST`** ja **`digna_APP_PORT`** sektsioonist `[app]` — aadressi ja pordi saab server nüüd käsult `digna serve`.

    Mida iga säte teeb, on kirjeldatud jaotises [Taustasüsteemi konfigureerimine](#backend-configuration).

!!! warning "Ühekordne sisselogimine: [oidc_clients] vorming on muutunud"

    Väljalase 2026.06 asendab tabelimassiivi ühe tabeliga iga pakkuja kohta, mis on nimetatud pakkuja võtme järgi. `DIGNA_OIDC_KEY` kaob — võti on nüüd sektsiooni päise osa.

    Enne:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Pärast:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Korrake sektsiooni iga pakkuja jaoks ja hoidke iga võti samana nagu `key` failis `dashboard_config.toml`. `digna config check` teatab `oidc_clients` sektsioonist FAILED, kuni vana vorm on veel alles. See puudutab ainult paigaldusi, mis kasutavad ühekordset sisselogimist.

#### Samm 5: Laadige veebiserver uuesti

Juhtpaneel koosneb staatilistest failidest, seega võivad teie veebiserver — ja brauser — ikka veel
serveerida eelmist versiooni. Laadige uuesti või taaskäivitage veebiserver, mis majutab kausta
`dashboard`, ning seejärel laadige leht sundvärskendusega uuesti (++ctrl+f5++).

#### Samm 6: Kontrollige konfiguratsiooni

Veenduge, et uuendatud `config.toml` on täielik, enne kui hoidlat puudutate:

```bash
digna config check
```

Iga sektsioon peab teatama OK. Parandage kõik, millest teatatakse FAILED, ja käivitage käsk enne jätkamist uuesti.

#### Samm 7: Asendage litsentsifail

Iga väljalase litsentsitakse eraldi. Kopeerige digna meeskonna poolt selle väljalaske jaoks
antud `license.toml` paigalduskausta, asendades vana faili:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Ärge jätke alles eelmist litsentsi"

    Varasema väljalaske jaoks väljastatud `license.toml` ei kehti selle väljalaske kohta ning iga
    käsk, mis litsentsi kontrollib — `user`, `inspection`, `repo` — katkeb enne hoidla
    puudutamist, kui kontroll ebaõnnestub. Kontrollige litsentsi enne jätkamist:

    ```bash
    digna license check
    ```

#### Samm 8: Uuendage andmehoidla skeemi

Minge oma digna paigalduskausta ja käivitage:

```bash
digna repo upgrade
```

See uuendab PostgreSQL skeemi uusimale versioonile, säilitades kõik olemasolevad andmed.

#### Samm 9: Registreerige ja käivitage teenus

Vana registreering eemaldati sammus 1, seega registreeritakse teenus uuesti — seekord
käivitatava failiga `digna`, millel batch-faile ei ole:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Andke valikutele `--address` ja `--port` väärtused, millel vana teenus teenindas, kui te ei soovi
uusi vaikeväärtusi `127.0.0.1` ja `8000`; need salvestatakse registreeringusse ja neid ei loeta
enam failist `config.toml`. Lisage `--account` ja `--password`, kui vana teenus töötas domeenikonto
all. Valikute täieliku loendi leiate jaotisest
[digna käitamine Windowsi teenusena](#running-digna-as-a-windows-service).

Kui käivitate käsitsi, taaskäivitage server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Kui kasutate IIS-i või Tomcati, taaskäivitage vastav veebiserver.

#### Samm 10: Kinnitage uuendus

1. Avage digna juhtpaneel
2. Veenduge, et liides laeb korralikult
3. Kontrollige serverilogisid võimalike vigade osas
4. Viige üle ODBC-le iga ühendus, mis seda veel ei kasutanud, ja testige seejärel kõiki ühendusi — vaadake [Ühenduse testimine](../../../databases/overview.md#testing-a-connection)