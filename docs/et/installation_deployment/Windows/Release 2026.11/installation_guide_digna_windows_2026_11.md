---
title: Windowsi paigaldusjuhend – digna väljalase 2026.11 | digna dokumentatsioon
description: Samm-sammuline juhend digna väljalaske 2026.11 installimiseks Windowsis — süsteeminõuded, PostgreSQL seadistus, veebiserveri konfiguratsioon, backendi ja juhtpaneeli konfiguratsioon, digna käivitamine Windowsi teenusena ja uuendamine versioonilt Release 2026.06.
keywords: digna windows paigaldus, digna juurutusjuhend, digna backendi seadistus, digna juhtpaneeli paigaldus, postgresql seadistus, digna windows teenus, digna uuendamisjuhend
image: /assets/logo_square.png
---

# Windowsi paigaldusjuhend digna väljalaske 2026.11 jaoks

**Väljalase:** 2026.11

**Viimati uuendatud:** 7. november 2026


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

### Mis on uut väljalaskes 2026.11

See väljalase toob kaasa uued moodulid digna Data Reconciliation ja digna Agentic (koos serveriga digna MCP Server) ning komponendi digna Engine, mis suudab andmeid profileerida digna sees ja kontrollida viidete terviklikkust eri andmebaasitehnoloogiate vahel. Täielikud andmed leiate [väljalaske märkmetest](../../../changelog/Release_202611.md).

Paigalduse jaoks toob väljalase uue hoidla migratsioonimehhanismi, komponendi digna Engine jaoks valikulise sektsiooni `[duckdb]` failis `config.toml` ning uue litsentsifaili. Neid kõiki käsitleb [uuendamise jaotis](#upgrading-to-a-new-release).

### Otsite macOS-i või Linuxi?

See juhend käsitleb Windowsi. Muude platvormide jaoks vaadake [macOS-i paigaldusjuhendit](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) või [Linuxi paigaldusjuhendit](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Andmebaasiühendusi, mille profileerimise asukoht on digna Engine, profileeritakse digna hostis
    endas. Planeerige nende jaoks lisamälu ja -kettaruumi, vt
    [\[duckdb\] sektsioon](#duckdb-section).

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

See sektsioon seadistab juhtpaneeli ja backendi vahelist päritoluülest ressursijagamist (CORS):

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Juhtpaneeli URL-id | URL-id, millelt juhtpaneel serveeritakse. Brauseri päringud mis tahes muult päritolult lükatakse tagasi |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutav, et brauser saadaks igas päringus kaasa sessiooniküpsise |

!!! info "Sektsioon [app] on valikuline"

    Alates Release 2026.11-st võib mõlemad võtmed ja kogu sektsiooni `[app]` ära jätta. See on
    õige seadistus, kui pöördpuhverserver (reverse proxy) serveerib juhtpaneeli ja backendi ühe päritolu
    all: brauser ei tee siis päritoluüleseid päringuid ja vaikimisi pole ühtki lubatud.

#### [repo] sektsioon

See sektsioon konfigureerib ühenduse PostgreSQL andmebaasiga:

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

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` või IP | PostgreSQL serveri hostinimi/IP |
| `DIGNA_REPO_PORT` | `5432` (vaikimisi) | PostgreSQL port |
| `DIGNA_REPO_DB` | `postgres` | Andmebaasi nimi |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Varem loodud skeem |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL seadistuses loodud kasutaja |
| `DIGNA_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |
| `DIGNA_REPO_SSLMODE` | `prefer` (vaikimisi) | Valikuline. PostgreSQL-i SSL-režiim: `disable`, `allow`, `prefer`, `require`, `verify-ca` või `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (vaikimisi) | Valikuline. Ühenduste arv, mida digna hoidlaga avatuna hoiab |

#### [base] sektsioon

See sektsioon sisaldab turbe-, küpsise- ja inspekteerimisseadeid:

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

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_FERNET_KEY` | Ülal näidatud väärtus | Varasemate väljalasete kasutatud krüpteerimise võti. See peab olemas olema; jätke näidatud väärtus |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host, mille all juhtpaneel on kättesaadav. `""` ei määra domeeni, mis on õige puhverserveri taga, mis serveerib juhtpaneeli ja backendi ühe päritolu all |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Peab olema `true` alati, kui digna serveeritakse üle HTTPS-i |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Hoiab sessiooniküpsise skriptidele kättesaamatuna |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumisaeg sekundites |
| `DIGNA_MAX_WORKERS` | CPU tuumade arv - 1 | Samaaegselt töötada võivate inspekteerimiste arv |
| `DIGNA_FRONTEND_BASEURL` | Juhtpaneeli URL | Kohustuslik. Kasutatakse teavitussõnumite linkides, seega peab see olema URL, mida adressaadid saavad avada |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (vaikimisi) | Valikuline. Sekundid, mille jooksul võib üks päring lähteandmebaasi vastu töötada, enne kui see katkestatakse; `0` lülitab ajalõpu välja |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (vaikimisi) | Valikuline. Sekundid, mille jooksul oodatakse ühendust lähteandmebaasiga; `0` ootab piiramatult |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` tootmisse, `DEBUG` tõrkeotsingu jaoks. Aktsepteeritakse ka `TRACE`, `WARN` ja `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (vaikimisi) | Valikuline. Roteeruvate logifailide kataloog, suhteline töökataloogi suhtes |
| `DIGNA_LOGGING_MAX_FILES` | `30` (vaikimisi) | Valikuline. Säilitatavate roteeritud logifailide arv |

!!! warning "Teenusena käitamisel säilitage logikataloog"

    Windowsi teenusel ei ole konsooli, seega on logifailid ainus ülestähendus sellest, mida teenus
    teeb. Ärge seadke `DIGNA_LOGGING_DIR` väärtuseks tühja stringi, sest see lülitab logifailid välja.

#### [duckdb] sektsioon (valikuline) {: #duckdb-section }

Uus väljalaskes Release 2026.11. See sektsioon määrab ressursid komponendile **digna Engine**, mis
profileerib andmeid digna sees nende andmebaasiühenduste puhul, mille profileerimise asukoht on
**digna Engine**, ning käitab viidete terviklikkuse kontrolle eri andmebaasiühendustel asuvate
andmeallikate vahel. Vaadake [Profileerimise asukoht](../../../platform/profiling/profiling_location.md).

Sektsioon on valikuline. Ilma selleta kehtivad allolevad vaikeväärtused.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (vaikimisi) | Mälu MB-des, mida üks digna Engine'i käivitus võib kasutada. Korraga võib aktiivne olla kuni `DIGNA_MAX_WORKERS` käivitust |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Vaikimisi: digna käitava konto ajutine kataloog (`%TEMP%`) | Ajutiste failide kataloog, kui andmed mällu ei mahu |

!!! tip "digna Engine'i ressursside planeerimine"

    Planeerige digna hostis lisaks digna enda kasutatavale mälule kuni
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` mälu ning ajutises kataloogis piisavalt
    vaba kettaruumi, et sinna mahuksid digna Engine'i kasutavate andmeallikate suurima
    inspekteeritava kuupäeva andmed. Suunake `DIGNA_DUCKDB_TEMP_DIRECTORY` sellise ruumiga kettale,
    kuhu digna käitaval kontol on kirjutusõigus:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Seda sektsiooni on vaja ainult siis, kui vähemalt üks andmebaasiühendus kasutab digna Engine'it
    või kui viidete terviklikkuse kontroll võrdleb eri ühendustel asuvaid andmeallikaid.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Parandage kõik, millest teatatakse FAILED, ja käivitage käsk enne jätkamist uuesti. Hoiatus WARNING rea **Unknown keys** all loetleb failis `config.toml` võtmed, mida digna ei loe; neil pole mingit mõju, seega eemaldage need või parandage nende kirjapilt. Täielik valikute loend on [CLI viites](../../../cli/Command_Line_Interface_202611.md).

### Samm 3: Initsialiseeri andmehoidla ühendus

1. Avage käsuviip
2. Minge oma digna paigalduskausta (kus asuvad `config.toml` ja `digna` täitmisfail)
3. Käivitage ühenduse test:

```bash
digna repo check
```

Uue skeemi puhul loob käsk ühenduse ja teatab seejärel, et hoidlat pole veel paigaldatud:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Selles etapis on see oodatud tulemus: see kinnitab, et digna jõuab PostgreSQL-i ja skeemini. Ühenduse- või autentimisviga viitab seevastu sektsioonile `[repo]` või PostgreSQL-i seadistusele.

### Samm 4: Paigaldage andmehoidla skeem

Selles samas kataloogis käivitage:

```bash
digna repo upgrade
```

See käsk paigaldab hoidla skeemi vajalikud tabelid ja lõpetab teatega:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade paigaldab ja uuendab"

    Alates Release 2026.11-st paigaldab `repo upgrade` uue hoidla ja uuendab olemasoleva.
    `repo install` töötab endiselt sama käsu teise nimena.

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
- `--address` — serveri hostinimi/IP (vaikimisi `127.0.0.1`)
- `--port` — serveri port (vaikimisi `8000`)

Kui server töötab, kuvab see aadressi, millel ta kuulab:

```text
Server running on http://127.0.0.1:8082
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
nimest erineva nime all. Valikute täielik loend on [CLI teatmikus](../../../cli/Command_Line_Interface_202611.md).

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

See jaotis uuendab Release 2026.06 paigalduse Release 2026.11-le.

!!! warning "Uuendamine 2026.06-st vanemast väljalaskest"

    Tee esmalt läbi Release 2026.06 uuendamise sammud: [Uuendamine uuele versioonile](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Seejärel jätka allolevate sammudega.

### Enne uuendamist

**digna andmehoidla varundamine on kohustuslik**

Enne digna uuendamist varundage oma andmehoidla (PostgreSQL), et kaitsta andmete kaotsimineku eest.
Varukoopia tagab taastumise juhuks, kui uuendamisel tekib ootamatuid probleeme.

**Release 2026.11 litsentsifaili taotlemine**

Release 2026.11 vajab uut faili `license.toml`. Taotlege see digna meeskonnalt enne alustamist ja
hoidke see [sammu 7](#step-7-replace-the-license-file) jaoks valmis.

### Uuendusprotsess

#### Samm 1: Peatage digna teenus {: #step-1-stop-the-digna-service }

Avage käsuviip administraatorina ja peatage teenus praeguse paigalduse käivitatava failiga
`digna`:

```bash
cd C:\path\to\digna
digna windows stop
```

Teenus jääb registreerituks. Uus käivitatav fail asub samas kataloogis vana asemel, seega osutab
registreering jätkuvalt õigele failile.

Kui digna töötab esiplaanil, vajutage selle käsuviiba aknas ++ctrl+c++.

#### Samm 2: Varundage praegune paigaldus {: #step-2-backup-current-installation }

Nimetage oma digna paigalduskataloogis praeguse paigalduse käivitatav fail ja kaust `dashboard`
ümber, et uut väljalaset saaks nende kõrvale paigaldada:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Hoidke `digna_old.exe` alles, kuni olete uuenduse kontrollinud, ja `dashboard_old`, kuni olete sellest
oma konfiguratsioonifailid taastanud (vt samm 4). Seejärel võite mõlemad kustutada.

#### Samm 3: Pakkige ja paigutage uus versioon {: #step-3-extract-and-deploy-new-version }

1. Pakkige uus digna paigaldus ZIP-fail lahti
2. Kopeerige uus `digna` täitmisfail ja `dashboard` kaust oma paigalduskausta

!!! warning "Tähtis"

    Paigaldus-ZIP ei sisalda kunagi ei faili `config.toml` ega `dashboard/dashboard_config.toml`
    — digna meeskond ei tarni kumbagi faili. Seetõttu ei puuduta uuendus teie olemasolevat
    konfiguratsiooni ning ümbernimetatud `*_old` kaustades olevad koopiad on ainsad, mis teil on.

#### Samm 4: Taastage oma konfiguratsioonifailid {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 ei vaja muudatusi failis `config.toml`: fail, mis töötab Release 2026.06-ga,
töötab edasi. Kaks muudatust on valikulised:

- Lisage [`[duckdb]` sektsioon](#duckdb-section), kui andmebaasiühendused peavad kasutama
  komponenti digna Engine ja selle vaikeväärtused teie hostile ei sobi.
- Jätke sektsioon `[app]` ära, kui pöördpuhverserver serveerib juhtpaneeli ja backendi ühe päritolu all.

!!! warning "Sätted, mida digna ei loe"

    Selle juhendi varasemad versioonid näitasid mõningaid sätteid, mida digna ei loe. Neil pole
    mingit mõju ja `config check` loetleb need sammus 6 rea **Unknown keys** all. Eemaldage või
    parandage need:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` ja
      `digna_LOGGING_BACKUP_COUNT` ei ole olemas. Eemaldage need.
    - Sätete nimed on tõstutundlikud. digna loeb `DIGNA_REPO_HOST`, mitte `digna_REPO_HOST`.
      Kirjutage iga nimi suurtähtedega, nagu jaotises [Backendi konfiguratsioon](#backend-configuration).

!!! warning "Ühekordne sisselogimine: säilitage [[oidc_clients]]"

    digna loeb ühekordse sisselogimise pakkujaid `[[oidc_clients]]` kirjete loendina, millest
    igaühel on oma `DIGNA_OIDC_KEY`. Kui muutsite oma pakkujad `[oidc_clients.<key>]`
    sektsioonideks, nagu selle juhendi varasem versioon näitas, muutke need tagasi. `config check`
    teatab `OIDC config(s)` olekuks FAILED, kuni see vorm on kasutusel:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Korrake kirjet iga pakkuja jaoks ja hoidke iga `DIGNA_OIDC_KEY` samana kui `key` failis
    `dashboard_config.toml`. See puudutab ainult paigaldusi, mis kasutavad ühekordset sisselogimist.

#### Samm 5: Laadige veebiserver uuesti {: #step-5-reload-the-web-server }

Juhtpaneel koosneb staatilistest failidest, seega võivad teie veebiserver — ja brauser — ikka veel
serveerida eelmist versiooni. Laadige uuesti või taaskäivitage veebiserver, mis majutab kausta
`dashboard`, ning seejärel laadige leht sundvärskendusega uuesti (++ctrl+f5++).

#### Samm 6: Kontrollige konfiguratsiooni {: #step-6-validate-the-configuration }

Veenduge enne hoidla puudutamist, et `config.toml` on täielik:

```bash
digna config check
```

Iga sektsioon peab teatama OK. Parandage kõik, millest teatatakse FAILED, eemaldage rea
**Unknown keys** all loetletud võtmed ja käivitage käsk enne jätkamist uuesti.

#### Samm 7: Asendage litsentsifail {: #step-7-replace-the-license-file }

Varasema väljalaske jaoks väljastatud litsentsifail ei tööta Release 2026.11-ga. Kopeerige digna
meeskonna poolt Release 2026.11 jaoks antud `license.toml` paigalduskataloogi, asendades vana faili:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Ärge jätke alles eelmist litsentsi"

    Eelmise litsentsiga ebaõnnestub iga käsk, mis litsentsi kontrollib — `serve`, `user`,
    `inspection`, `repo` —, seega digna ei käivitu ja hoidlat ei saa uuendada. Kontrollige uut
    litsentsi enne jätkamist:

    ```bash
    digna license check
    ```

#### Samm 8: Uuendage andmehoidla skeemi {: #step-8-upgrade-the-repository-schema }

Käivitage oma digna paigalduskataloogis:

```bash
digna repo upgrade
```

Release 2026.11 haldab hoidla skeemi versioonitud migratsioonidega. Esimene uuendus varasemast
väljalaskest viib skeemi eelmise versioonimisskeemi viimasele versioonile, salvestab selle
lähtepunktina ja rakendab seejärel Release 2026.11 migratsioonid. See lõpetab teatega:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Kõik olemasolevad andmed säilivad. Hoidla oleku nägemiseks igal ajal käivitage
`digna repo check`: see loetleb viimase rakendatud migratsiooni ja kõik ootel migratsioonid.

!!! warning "digna ei käivitu aegunud hoidlaga"

    Alates Release 2026.11-st keeldub server käivitumast, kuni hoidla vajab uuendamist, ja teatab
    sellest, näiteks:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Käivitage `repo upgrade` enne serveri või teenuse käivitamist.

#### Samm 9: Teenuste taaskäivitamine {: #step-9-restart-services }

Kui digna töötab Windowsi teenusena, käivitage see uuesti:

```bash
cd C:\path\to\digna
digna windows start
```

Kui käivitate käsitsi, taaskäivitage server:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Kui kasutate IIS-i või Tomcati, taaskäivitage vastav veebiserver.

#### Samm 10: Kinnitage uuendus {: #step-10-verify-the-upgrade }

1. Kontrollige uue käivitatava faili väljalaset:

    ```bash
    digna version
    ```

    Esimene rida peab olema `Release: 2026.11`.

2. Avage digna juhtpaneel ja veenduge, et liides laadib korrektselt.
3. Kontrollige paigalduse kataloogi `logs` faile vigade suhtes.
4. Testige oma andmebaasiühendusi — vaadake
   [Ühenduse testimine](../../../databases/overview.md#testing-a-connection).

Uute moodulitega alustamiseks vaadake [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Serveri kohta [AI-agendi ühendamine](../../../platform/agentic/connect_ai_agent.md) ja
digna Engine'i kohta [Profileerimise asukoht](../../../platform/profiling/profiling_location.md).
