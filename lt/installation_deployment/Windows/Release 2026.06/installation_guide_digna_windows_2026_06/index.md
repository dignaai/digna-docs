# Windows diegimo vadovas digna Release 2026.06

**Išleidimas:** 2026.06

**Paskutinį kartą atnaujinta:** 2026 m. rugpjūčio 30 d.


---

## Turinys

1. [Įvadas](#introduction)
2. [Sistemos reikalavimai](#system-requirements)
3. [Prieš diegiant](#pre-installation-setup)
4. [PostgreSQL serverio nustatymai](#postgresql-server-setup)
5. [Žiniatinklio serverio konfigūracija](#web-server-configuration)
6. [Pradinis diegimas](#initial-installation)
7. [Backend konfigūracija](#backend-configuration)
8. [Dashboard konfigūracija](#dashboard-configuration)
9. [digna paleidimas kaip Windows paslauga](#running-digna-as-a-windows-service)
10. [Atnaujinimas į naują leidimą](#upgrading-to-a-new-release)

---

## Įvadas {: #introduction }

### Apie digna

digna yra visapusiška AI varoma platforma, skirta optimizuoti duomenų kokybės valdymą įvairiose duomenų aplinkose, tokiose kaip duomenų sandėliai (warehouses), lakes ir lakehouses. Sukurta būti labai skalabilia ir pritaikoma, digna sprendžia šiuolaikines duomenų problemas per automatizaciją, realaus laiko stebėjimą ir anomalijų aptikimą.

digna susideda iš dviejų pagrindinių komponentų:

- **digna**: programos branduolys, atsakingas už duomenų apdorojimą ir kokybės patikras. Jis sujungia užkulisinę dalį ir komandinęs eilutės sąsają į vieną vykdomąjį failą ir pakeičia atskiras ankstesnių leidimų programas `dignabackend` ir `dignacli`.
- **dignadashboard**: žiniatinklio sąsaja, talpinama ant web serverio, suteikianti patogią sąveiką su digna platforma ir duomenų kokybės metrikų vizualizavimą.

### Kas naujo leidime 2026.06

Šis leidimas prideda duomenų stebėjimo (data observability) galimybes tiesiai į jūsų kodą, leidžiant programuotojams stebėti duomenų kokybę ties šaltiniu. Pilną informaciją rasite [išleidimo pastabose](http://docs.digna.ai/changelog/Release_202606/).

### Ieškote macOS ar Linux?

Šis vadovas skirtas Windows. Kitoms platformoms žiūrėkite [macOS diegimo vadovą](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) arba [Linux diegimo vadovą](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Sistemos reikalavimai {: #system-requirements }

Prieš pradėdami diegimą, įsitikinkite, kad jūsų sistema atitinka šiuos minimalius reikalavimus:

| Reikalavimas | Specifikacija |
|---|---|
| **Operacinė sistema** | Windows Server arba Windows 10/11 |
| **Atmintis (minimalus diegimas)** | 16 GB RAM |
| **Disko vieta** | 10 GB laisvos vietos |
| **Duomenų bazė** | PostgreSQL Server 12 arba naujesnė |
| **Žiniatinklio serveris** | IIS, Apache Tomcat arba analogiškas |

### Duomenų bazės diegimo parinktys

**Jei PostgreSQL jau įdiegtas:**
Galite pridėti naują duomenų bazę digna prie esančio PostgreSQL serverio.

**Jei diegiate PostgreSQL toje pačioje mašinoje kaip digna:**

!!! info "Rekomenduojama specifikacija"

    - **Atmintis**: 32 GB RAM (vietoje 16 GB)
    - **Disko vieta**: 50 GB laisvos vietos (vietoje 10 GB)

    Šios didesnės specifikacijos leidžia sklandžiai veikti tiek digna, tiek PostgreSQL duomenų bazei vienu metu.

---

## Prieš diegiant {: #pre-installation-setup }

Prieš įdiegdami digna, įsitikinkite, kad yra du pagrindiniai reikalavimai:

1. **PostgreSQL serveris** – skirtas apskaičiuotų metrikų ir veikimo duomenų saugojimui
2. **Žiniatinklio serveris** – skirtas digna Dashboard talpinimui

Jei šie komponentai dar nėra sukonfigūruoti, vadovaukitės žemiau pateiktomis sekcijomis, kad juos įdiegtumėte ir nustatytumėte.

---

## PostgreSQL serverio nustatymai {: #postgresql-server-setup }

### Jei PostgreSQL jau turite

Jei PostgreSQL jau įdiegtas ir veikia jūsų lokaliame kompiuteryje arba naudojate valdomą nuotolinį PostgreSQL serverį, galite pereiti prie [kitos skilties](#web-server-configuration).

### PostgreSQL diegimas

Vadovaukitės šiomis instrukcijomis, kad įdiegtumėte PostgreSQL Windows sistemoje:

#### 1 žingsnis: Atsisiųskite PostgreSQL

1. Apsilankykite [PostgreSQL atsisiuntimų puslapyje](https://www.postgresql.org/download/)
2. Pasirinkite **Windows**
3. Atsisiųskite naujausią diegimo programą

#### 2 žingsnis: Paleiskite diegimo programą

1. Dukart spustelėkite atsisiųstą diegimo failą
2. Sekite nustatymų vedlio nurodymus

#### 3 žingsnis: Pasirinkite diegimo katalogą

Pasirinkite katalogą, į kurį bus įdiegta PostgreSQL. Numatytoji vieta dažniausiai tinka.

#### 4 žingsnis: Pasirinkite komponentus

Standartiniam diegimui palikite numatytus komponentus.

#### 5 žingsnis: Nustatykite PostgreSQL supervartotojo slaptažodį

Įveskite ir patvirtinkite slaptažodį PostgreSQL supervartotojui (`postgres`). **Saugiai išsaugokite šį slaptažodį** — jo prireiks vėliau.

#### 6 žingsnis: Konfigūruokite prievadą

Numatytasis PostgreSQL prievadas yra `5432`. Galite naudoti numatytąjį arba nurodyti kitą prievadą, jei reikia.

!!! tip "Patarimas"

    Jei prievadas 5432 jau užimtas, pasirinkite alternatyvų prievadą ir užsirašykite jį vėlesnei konfigūracijai.

#### 7 žingsnis: Pasirinkite lokalę

Pasirinkite duomenų bazės lokalę. Numatytoji dažniausiai tinka daugumai diegimų.

#### 8 žingsnis: Uždarykite diegimą

Spustelėkite **Next** per likusius žingsnius, tada spustelėkite **Finish**.

#### 9 žingsnis: Patikrinkite diegimą

Atidarykite Command Prompt ir patikrinkite, ar PostgreSQL įdiegtas:

```bash
psql --version
```

Jei diegimas buvo sėkmingas, matysite PostgreSQL versiją.

---

## Žiniatinklio serverio konfigūracija {: #web-server-configuration }

digna reikalauja žiniatinklio serverio dashboard talpinimui. Pasirinkite vieną iš šių parinkčių:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Reikia įdiegti ir sukonfigūruoti **vieną** iš šių serverių.

### IIS nustatymas {: #iis-setup }

#### Apžvalga

Internet Information Services (IIS) yra Microsoft žiniatinklio serveris, skirtas svetainių ir web programėlių talpinimui.

#### IIS įjungimas

1. **Atidarykite Valdymo skydą**
   - Paspauskite `Win + R`
   - Įveskite `control` ir paspauskite Enter

2. **Eikite į Windows funkcijas**
   - Spustelėkite **Programs**
   - Pasirinkite **Turn Windows features on or off**

3. **Įgalinkite Internet Information Services**
   - Slinkite žemyn ir raskite **Internet Information Services (IIS)**
   - Pažymėkite varnelę, kad jį įjungtumėte
   - Spustelėkite **+**, kad išplėstumėte ir patikrinkite, ar pasirinkti šie potekomponentai:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Spustelėkite OK**, kad pritaikytumėte pakeitimus

5. **Patikrinkite IIS diegimą**
   - Atidarykite naršyklę
   - Nueikite į `http://localhost`
   - Turėtumėte matyti IIS pasveikinimo puslapį

#### Privaloma: URL Rewrite modulis

IIS reikalauja URL Rewrite komponento. Atsisiųskite ir įdiekite jį iš [oficialaus Microsoft puslapio](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Privaloma: MIME tipas Markdown failams

Kad Markdown failai (`.md`) būtų teisingai aptarnauti IIS:

1. Atidarykite **IIS Manager** (paspauskite `Win + R`, įveskite `inetmgr`, paspauskite Enter)
2. Eikite į **Your Site > MIME Types**
3. Spustelėkite **Add...**
4. Konfigūruokite:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Svarbu"

    Be šio nustatymo `.md` failai gali būti netinkamai aptarnaujami.

---

### Apache Tomcat nustatymas {: #apache-tomcat-setup }

#### Apžvalga

Apache Tomcat yra atviro kodo Java servlet konteineris ir žiniatinklio serveris.

#### Diegimas

1. **Atsisiųskite Apache Tomcat**
   - Apsilankykite [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Atsisiųskite Windows ZIP distribuciją

2. **Išskleiskite archyvą**
   - Išskleiskite ZIP failą į katalogą savo sistemoje
   - Pavyzdys: `C:\Program Files\Apache Tomcat`

3. **Patikrinkite, ar Tomcat veikia**
   - Atidarykite naršyklę
   - Nueikite į `http://localhost:8080`
   - Turėtumėte matyti Apache Tomcat pasveikinimo puslapį

!!! tip "Patarimas"

    Apache Tomcat paprastai paleidžiamas automatiškai po diegimo. Jei ne, eikite į `bin` katalogą ir paleiskite `startup.bat`.

---

## Pradinis diegimas {: #initial-installation }

### 1 žingsnis: Sukurkite digna repozitoriją

digna repozitorija saugo visas digna apskaičiuotas metrikas. Ji veikia kaip centrinė analizės ir veikimo duomenų duomenų saugykla.

#### Sukurkite schemą ir vartotoją repozitorijai

Atidarykite savo PostgreSQL klientą (pgAdmin, psql ar panašiai) ir vykdykite šias SQL komandas:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Pakeiskite šiuos vietos rezervavimo simbolius:**

- `<digna_repo_schema>` — pageidaujamas schemos pavadinimas (pvz., `dignarepo`)
- `<digna_repo_user>` — pageidaujamas vartotojo vardas (pvz., `digna_user`)
- `<digna_repo_password>` — saugus slaptažodis šiam vartotojui

**Pavyzdys:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Gera praktika"

    Naudokite stiprius, sudėtingus slaptažodžius duomenų bazės vartotojams. Venkite lengvai atspėjamų kredencialų.

---

### 2 žingsnis: Ištraukite digna diegimo paketą

1. Raskite jums pateiktą digna diegimo ZIP failą
2. Išskleiskite jį į pageidaujamą diegimo vietą
3. Po išskleidimo turėtumėte matyti šiuos elementus:
   - `dashboard/` — web dashboard sąsaja
   - `digna` — pagrindinis vykdomasis failas (backend + CLI kartu)

!!! info "Konfigūracijos ir licencijos failų pakete nėra"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` diegimo pakete nepateikiami — abu
    failus sukuriate patys, skyriuose [Backend konfigūracija](#backend-configuration) ir
    [Dashboard konfigūracija](#dashboard-configuration). `license.toml` taip pat nepateikiamas;
    digna jį pateikia atskirai, kaip aprašyta 3 žingsnyje.

### 3 žingsnis: Įdiekite licencijos failą

!!! warning "Svarbu"

    Licencijos failas **neįtrauktas** į diegimo paketą ir bus pateiktas atskirai iš digna.

1. Raskite jums suteiktą `license.toml` failą
2. Nukopijuokite jį į pagrindinį digna diegimo katalogą (ten, kur yra `config.toml` ir `digna` vykdomasis failas)

**Kodėl tai svarbu:**
Licencijos faile yra jūsų klientų informacija, licencijos galiojimo data ir skaitmeninis parašas. **Nekeiskite šio failo** — bet kokie pakeitimai jį sukels nebegaliojantį.

**Katalogų struktūra po nustatymo:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Backend konfigūracija {: #backend-configuration }

### 1 žingsnis: Sukurkite ir redaguokite konfigūracijos failą

`config_template.toml` failas pateiktas jūsų digna diegimo kataloge. Jums tereikia jį pervardyti į `config.toml`.

**Vieta:** `digna_installation/config.toml`

Atidarykite `config.toml` tekstų redaktoriumi ir sukonfigūruokite kiekvieną sekciją žemiau.

#### [app] skiltis

Ši skiltis konfigūruoja digna backend programos nustatymus:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendo URL | Jei dashboard yra kitame serveryje, įtraukite jo URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Reikalinga CORS su kredencialais |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Leidžiami visi HTTP metodai |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Leidžiami visi antraštės laukai |

#### [repo] skiltis

Ši skiltis konfigūruoja prisijungimą prie PostgreSQL duomenų bazės:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_REPO_HOST` | `localhost` arba IP | PostgreSQL serverio hostname/IP |
| `digna_REPO_PORT` | `5432` (numatytasis) | PostgreSQL prievadas |
| `digna_REPO_DB` | `postgres` | Duomenų bazės pavadinimas |
| `digna_REPO_SCHEMA` | `dignarepo` | Anksčiau sukurta schema |
| `digna_REPO_USER` | `digna_user` | Vartotojas sukurtas PostgreSQL nustatymuose |
| `digna_REPO_PASSWORD` | Jūsų slaptažodis | Slaptažodis nustatytas kuriant schemą |

#### [base] skiltis

Ši skiltis turi saugumo ir slapukų nustatymus:

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

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Atitinka jūsų frontendo domeną |
| `digna_COOKIE_SECURE` | `false` (lokaliai) / `true` (produkcijoje) | Naudokite `true` HTTPS ryšiams |
| `digna_COOKIE_HTTPONLY` | `true` | Visada įjungta dėl saugumo |
| `digna_COOKIE_SAME_SITE` | `lax` | Apsaugo nuo CSRF atakų |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 val.) | Sesijos laikas sekundėmis |
| `digna_MAX_WORKERS` | CPU branduolių skaičius - 1 | Lygų paralelinių tikrinimų užduočių skaičius |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Didžiausias vėlavimas sekundėmis, kurį planuoklis gali pridėti prieš paleisdamas terminuotą užduotį |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Paros laikas (24 valandų formatas `HH:MM`), kada prasideda kasdienis valymas |

#### [encryption] skyrius

Šiame skyriuje yra raktas, kuriuo šifruojamos saugykloje laikomos jautrios reikšmės. Jis yra **būtinas** — `config check` praneša skyrių `[encryption]` kaip FAILED, jei rakto trūksta.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64 koduotas raktas | Šifruoja jautrias reikšmes, saugomas digna saugykloje |

!!! warning "Apsaugokite config.toml"

    Šis raktas yra fiksuota reikšmė, vienoda visose digna diegimuose, ir būtent jis iššifruoja jautrias jūsų saugyklos reikšmes. Apribokite `config.toml` prieigą iki paskyros, kuria veikia digna, laikykite failą už versijų kontrolės ir bendrų diskų ribų ir neįtraukite jo į jokias atsargines kopijas, laikomas mažiau saugiai nei pati saugykla.

#### [logging] skiltis

Ši skiltis konfigūruoja žurnalo (logging) elgseną:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` arba `DEBUG` | `INFO` produkcijai, `DEBUG` trikčių šalinimui |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Išsaugomų kasdienių žurnalų atsarginių kopijų skaičius |

---

### 2 žingsnis: Patikrinkite konfigūraciją

Prieš inicijuodami saugyklą patikrinkite, ar `config.toml` yra išsamus ir tinkamai sudarytas. Savo digna diegimo kataloge paleiskite:

```bash
digna config check
```

Kiekvienas skyrius tikrinamas atskirai, todėl viena klaida neuždengia kitų būsenos:

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

Pataisykite viską, kas pranešama kaip FAILED, ir prieš tęsdami paleiskite komandą dar kartą. Visas parinkčių sąrašas pateiktas [CLI žinyne](../../../cli/Command_Line_Interface_202606.md).

### 3 žingsnis: Inicializuokite repozitoriją

1. Atidarykite Command Prompt
2. Nueikite į savo digna diegimo katalogą (ten, kur `config.toml` ir `digna` vykdomasis failas)
3. Paleiskite ryšio testą:

```bash
digna repo check
```

Turėtumėte matyti patvirtinimą, kad ryšys užmegztas (repozitorija pati dar neinicijuota).

### 4 žingsnis: Įdiekite repozitorijos schemą

Toje pačioje direktorijoje paleiskite:

```bash
digna repo install
```

Ši komanda įdiegia reikiamas lenteles ir schemą jūsų PostgreSQL duomenų bazėje.

### 5 žingsnis: Sukurkite administratoriaus vartotoją

1. Atidarykite **naują** Command Prompt langą
2. Nueikite į digna diegimo katalogą
3. Paleiskite šią komandą, kad sukurtumėte administratorių:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Pavyzdys:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Tai sukurs vartotoją su pilnomis administravimo teisėmis.

!!! tip "Gera praktika"

    Naudokite stiprų slaptažodį su didžiosiomis, mažosiomis raidėmis, skaičiais ir specialiaisiais simboliais.

---

### 6 žingsnis: Paleiskite digna serverį

Digno diegimo kataloge paleiskite serverį:

```bash
digna serve --address <host> --port <port>
```

**Parametrai:**
- `--address` — serverio hostname/IP
- `--port` — serverio prievadas 

Turėtumėte matyti paleidimo pranešimus, patvirtinančius, kad serveris veikia:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Serveris užima terminalą"

    `serve` veikia priekiniame plane ir tęsiasi, kol jį sustabdysite ++ctrl+c++. Palikite jį veikti, kol užbaigsite sąranką; kad jis būtų paleidžiamas automatiškai paleidus sistemą, žiūrėkite [digna paleidimas kaip Windows tarnybos](#running-digna-as-a-windows-service).

## Dashboard konfigūracija {: #dashboard-configuration }

### 1 žingsnis: Patalpinkite dashboard į žiniatinklio serverį

digna dashboard savo konfigūraciją skaito iš `dashboard/dashboard_config.toml`. Šis failas diegimo pakete nepateikiamas — jį sukuriate `dashboard/` kataloge šalia dashboard failų.

Jo turinys aprašytas skyriuje [Vienkartinis prisijungimas (SSO)](../../../sso/overview.md), kur šis failas ir reikalingas: jame nurodomos dashboard siūlomos prisijungimo parinktys, o daugiainstanciniams diegimams — ir ryšys su backend.

Pasirinkite žiniatinklio serverį ir atlikite atitinkamus diegimo veiksmus.

#### Diegimas į IIS

1. **Atidarykite IIS Manager**
   - Paspauskite `Win + R`, įveskite `inetmgr`, paspauskite Enter

2. **Sukurkite naują svetainę**
   - Kairėje panelėje dešiniuoju pelės mygtuku spustelėkite **Sites**
   - Pasirinkite **Add Website...**

3. **Sukonfigūruokite svetainę**
   - **Site Name**: Įveskite pavadinimą (pvz., "dignaDashboard")
   - **Physical Path**: Spustelėkite Browse ir pasirinkite savo `dashboard` katalogą
   - **Binding**: Nustatykite IP adresą ir prievadą (numatytas prievadas HTTP — 80, HTTPS — 443)

4. **Paleiskite svetainę**
   - Spustelėkite **OK**, kad sukurtumėte svetainę
   - Dešiniuoju pelės mygtuku spustelėkite naują svetainę ir pasirinkite **Start**

5. **Patikrinkite diegimą**
   - Atidarykite naršyklę
   - Nueikite į `http://localhost` (arba jūsų sukonfigūruotą URL)
   - Turėtumėte matyti digna dashboard prisijungimo puslapį

#### Diegimas į Apache Tomcat

1. **Kopijuokite dashboard į Tomcat**
   - Nukopijuokite `dashboard` katalogą į savo Tomcat `webapps` katalogą
   - Pervardykite, jei reikia (pvz., į `digna`)
   - Pavyzdys: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Patikrinkite diegimą**
   - Atnaujinkite arba perkraukite Tomcat valdymo puslapį (http://localhost:8080)
   - Turėtumėte matyti „digna“ (ar jūsų pasirinktą pavadinimą) tarp išdėstytų aplikacijų

3. **Prieiga prie dashboard**
   - Atidarykite naršyklę
   - Nueikite į `http://localhost:8080/digna`
   - Turėtumėte matyti digna dashboard prisijungimo puslapį

---

## digna paleidimas kaip Windows paslauga {: #running-digna-as-a-windows-service }

### Kodėl naudoti Windows paslaugą?

digna backend paleidus kaip Windows paslaugą užtikrinama, kad jis:
- Paleidžiamas automatiškai serveriui įsijungus
- Veikia fone be atidaryto Command Prompt lango
- Automatiškai paleidžiamas iš naujo, jei sugestų
- Gali būti valdomas per Windows Services

### `windows` komandos

Paslaugą valdo pats `digna` vykdomasis failas, naudodamas `digna windows`
subkomandas. Jokių batch failų vykdyti nereikia.

| Komanda | Paskirtis |
|---|---|
| `digna windows install` | Užregistruoja digna kaip Windows paslaugą |
| `digna windows start` | Paleidžia užregistruotą paslaugą |
| `digna windows stop` | Sustabdo veikiančią paslaugą |
| `digna windows uninstall` | Panaikina paslaugos registraciją |

!!! warning "Reikalingos administratoriaus teisės"

    Visas keturias komandas reikia vykdyti iš Command Prompt, atidaryto kaip administratorius.

Kiekviena komanda priima `--name`, kad būtų galima kreiptis į paslaugą, užregistruotą ne numatytuoju pavadinimu. Visas
parinkčių sąrašas pateiktas [CLI žinyne](../../../cli/Command_Line_Interface_202606.md).

### Paslaugos įdiegimas

1. **Atidarykite Command Prompt kaip administratorius**
   - Dešiniuoju pelės mygtuku spustelėkite Command Prompt
   - Pasirinkite "Run as Administrator"

2. **Nueikite į savo digna diegimo katalogą**
   ```bash
   cd C:\path\to\digna
   ```

3. **Užregistruokite paslaugą**
   ```bash
   digna windows install
   ```

!!! important "Nurodykite adresą ir prievadą, nebent numatytosios reikšmės jums tinka"

    `install` įrašo adresą ir prievadą į paslaugos registraciją, o paslauga susiejama būtent
    su tuo, kas įrašyta. Numatytosios reikšmės yra `127.0.0.1` ir `8000`, kurios priima ryšius
    tik iš pačios mašinos. Kitame kompiuteryje veikiantis dashboard jų nepasieks, todėl nurodykite
    adresą, kuriuo backend turi klausytis:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Šios reikšmės neskaitomos iš `config.toml`. Norėdami jas vėliau pakeisti, pašalinkite paslaugą ir
    įdiekite ją iš naujo su naujomis reikšmėmis.

Paslauga užregistruojama su **automatiniu paleidimu**, todėl ji bus paleidžiama kartu su Windows. Iš karto
ji nepaleidžiama — žr. kitą skyrių.

#### Diegimo parinktys

| Parinktis | Numatytoji reikšmė | Paskirtis |
|---|---|---|
| `--name` | `digna` | Pavadinimas, kuriuo registruojama paslauga |
| `--display-name` | `digna` | Pavadinimas, rodomas services.msc |
| `--description` | `digna data quality backend` | Aprašas, rodomas services.msc |
| `--address` | `127.0.0.1` | Adresas, prie kurio paslauga susieja savo API |
| `--port` | `8000` | Prievadas, prie kurio paslauga susieja savo API |
| `--working-dir` | `digna` vykdomojo failo katalogas | Katalogas su `config.toml` ir `license.toml`, kurį paslauga naudoja kaip darbinį katalogą |
| `--start-type` | `auto` | `auto` paleidžiama kartu su Windows, `manual` paleidžiama tik paprašius, `disabled` užregistruoja paslaugą, bet neleidžia jos paleisti |
| `--account` | `LocalSystem` | Paskyra, kuria vykdoma paslauga, pvz., `DOMAIN\user` arba `.\user` |
| `--password` | | `--account` paskyros slaptažodis |

!!! tip "Vykdymas domeno paskyra"

    `LocalSystem` neturi tinklo tapatybės, todėl Windows Authentication prie SQL Server ir bet kokia
    prieiga prie tinklo bendrinamo aplanko nepavyks. Jei paslaugai reikia pasiekti išteklius kaip konkrečiam naudotojui,
    įdiekite ją su `--account` ir `--password`.

### Paslaugos paleidimas ir sustabdymas

#### Paslauga paleidimui

```bash
digna windows start
```

#### Paslauga sustabdymui

```bash
digna windows stop
```

!!! tip "Patarimas"

    Visada sustabdykite paslaugą prieš atnaujinant programos failus.

### Perkėlimas paslaugos į naują katalogą

Jei reikia perkelti digna diegimą:

1. **Sustabdykite ir išregistruokite esamą paslaugą**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Perkelkite aplikacijos failus**
   - Perkelkite visą digna diegimo aplanką į naują vietą

3. **Vėl užregistruokite paslaugą iš naujos vietos**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Pakartokite visas `--address`, `--port` ar `--account` reikšmes, kurias naudojote pirmą kartą — ankstesnės
   registracijos nebėra.

4. **Paleiskite paslaugą**
   ```bash
   digna windows start
   ```

### Paslaugos pašalinimas

1. **Sustabdykite veikiančią paslaugą**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Išregistruokite paslaugą**
   ```bash
   digna windows uninstall
   ```

Digna serveris dabar atregistruotas kaip Windows paslauga.

---

## Atnaujinimas į naują leidimą {: #upgrading-to-a-new-release }

### Prieš atnaujinimą

**Pirmiausia patikrinkite visus duomenų bazės ryšius**

Nuo leidimo 2026.06 digna kiekvieną šaltinio technologiją pasiekia per **ODBC**. Ankstesni leidimai siūlė pasirinkimą tarp konkrečiai technologijai skirtos tvarkyklės ir ODBC, pažymimą jungikliu **Use ODBC**. digna komanda nusprendė remtis vien ODBC, nes viena standartinė sąsaja duoda daugiau nei pagal užsakymą sukurtų tvarkyklių rinkinys:

- **Tapatybės nustatymas** — tapatybės nustatymas yra ODBC dalis, todėl ryšys gali naudoti viską, ką palaiko jo tvarkyklė: slaptažodžius, prieigos raktus ir PAT, Kerberos ir Active Directory, MFA ir naršyklės vienkartinį prisijungimą, debesijos tapatybes, kliento sertifikatus ir TLS. Nauji metodai atkeliauja su tvarkyklės atnaujinimu, o ne laukiant digna leidimo.
- **Tvarkyklės, kurias prižiūri duomenų bazių gamintojai** — gamintojo tvarkyklė seka naujas serverio versijas ir saugumo pataisas, o jūs galite ją atnaujinti savo tempu, nepriklausomai nuo digna.
- **Vienas būdas viską sukonfigūruoti** — kiekviena technologija yra raktų ir reikšmių savybių sąrašas su ta pačia sąsaja, tuo pačiu jautrių reikšmių šifravimu ir ta pačia trikčių diagnostika, o ne skirtingais laukų rinkiniais kiekvienam šaltiniui.
- **Derinimas ir aprėptis** — tvarkyklės parinktys, tokios kaip skirtieji laikai, TLS nuostatos, tarpiniai serveriai ir nuskaitymo dydžiai, prieinamos kiekvienam šaltiniui, o prijungti galima bet kurią technologiją su atitinkama ODBC tvarkykle, taip pat ir tas, kurioms digna neskelbia atskiro vadovo.

Praktikoje tai reiškia, kad jungiklio **Use ODBC** bei atskirų pagrindinio kompiuterio, prievado, duomenų bazės, naudotojo ir slaptažodžio laukų nebeliko. **Kiekvieną ryšį, kuris dar nenaudoja ODBC, reikia perkelti į ODBC** — automatinio konvertavimo nėra, todėl suplanuokite tai prieš naujinimą:

1. Peržiūrėkite kiekvieną jūsų diegime apibrėžtą duomenų bazės ryšį ir pasižymėkite tuos, kurie dar nenaudoja ODBC — kiekvieną jų reikės sukonfigūruoti iš naujo.
2. Įdiekite atitinkamą ODBC tvarkyklę digna pagrindiniame kompiuteryje — ryšiai atveriami iš serverio, kuriame veikia digna užkulisinė dalis, o ne iš naršyklės. Žiūrėkite [ODBC tvarkyklės diegimas digna pagrindiniame kompiuteryje](../../../databases/overview.md#install-the-driver).
3. Turėkite paruoštas ODBC savybes kiekvienam susijusiam ryšiui. [Technologijų vadovai](../../../databases/overview.md#technology-guides) kiekvienam šaltiniui pateikia išbandytą savybių rinkinį.

Po naujinimo kiekvieną susijusį ryšį perkelkite į ODBC ir išbandykite jį iš skydelio — žiūrėkite [Duomenų bazės ryšio kūrimas](../../../databases/overview.md#create-a-database-connection) ir [Ryšio tikrinimas](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy ryšiai"

    Databricks Legacy jungtis šiame leidime pašalinta. Perkelkite tuos ryšius į [Databricks](../../../databases/databricks_connector_guide.md) jungtį.

**Būtina sukurti digna repozitorijos atsarginę kopiją**

Prieš atnaujinant digna, atsargiai atsarginę kopiją savo repozitorijos (PostgreSQL), kad apsisaugotumėte nuo duomenų praradimo.
Atsarginė kopija leis atkurti duomenis, jei atnaujinimo metu kils nenumatytų problemų.

### Atnaujinimo procesas

#### 1 žingsnis: Sustabdykite ir išregistruokite senąją paslaugą

Jei digna veikia kaip Windows paslauga, sustabdykite ją **dabartinio diegimo batch failais**
— `digna windows` komandos priklauso naujajam leidimui ir dar nėra
prieinamos:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Tada išregistruokite paslaugą, vėl naudodami senąjį batch failą. Registracija nurodo į senąjį
vykdomąjį failą ir jo skriptus, kuriuos abu šis atnaujinimas pakeičia, todėl jos panaudoti pakartotinai negalima:

```bash
uninstall_service.bat
```

!!! warning "Išregistruokite prieš ką nors pervadindami"

    `uninstall_service.bat` yra `bin` aplanke, kurį netrukus pervadinsite, ir tik jis gali
    pašalinti savo sukurtą registraciją. Vykdykite jį, kol senasis diegimas dar yra savo vietoje.
    Jei aplankas jau pervadintas, grąžinkite jam senąjį pavadinimą, išregistruokite paslaugą ir tęskite.

    Užsirašykite paskyrą, kuria veikė paslauga, bei adresą ir prievadą, kuriais ji veikė — jų
    prireiks 9 žingsnyje.

#### 2 žingsnis: Sukurkite dabartinio diegimo atsarginę kopiją

Savo digna diegimo kataloge pervadinkite dabartinio diegimo aplankus, kad naują leidimą būtų galima įdiegti šalia jų:

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

!!! info "dignabackend ir dignacli nebenaudojami"

    Nuo leidimo 2026.06 `dignabackend` ir `dignacli` pakeičia vienas vykdomasis failas `digna`, sujungiantis užkulisinę dalį ir CLI. Aplankus `dignabackend_old` ir `dignacli_old` laikykite tik tol, kol patikrinsite naujinimą — po to abu galite ištrinti. Aplanką `dashboard_old` laikykite, kol iš jo atkursite savo konfigūracijos failus (žiūrėkite 4 žingsnį). Pašalinamas ir `bin` aplankas: jo batch failai valdė senąją paslaugą, o 2026.06 jų nebepateikia, todėl 1 žingsnyje išregistravus paslaugą jie tik klaidintų.

#### 3 žingsnis: Išskleiskite ir naudokite naują versiją

1. Išskleiskite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į savo diegimo katalogą


!!! warning "Svarbu"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` niekada nėra įtraukti į
    diegimo ZIP — digna komanda niekada nepateikia nė vieno iš šių failų. Todėl atnaujinimas jūsų
    esamos konfigūracijos nepaliečia, o kopijos pervadintuose `*_old` aplankuose yra
    vienintelės, kurias turite.

#### 4 žingsnis: Atkurkite konfigūracijos failus

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Leidimas 2026.06 keičia config.toml"

    Trys nuostatos yra naujos ir būtinos, o trys nebenaudojamos. Iš ankstesnio leidimo perkeltame `config.toml` naujų nuostatų nėra, ir digna nepasileis, kol jų trūks. Į esamą `config.toml` įrašykite:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Du `[base]` raktus įrašykite į esamą `[base]` skyrių, o `[encryption]` pridėkite kaip naują skyrių. Tada pašalinkite nuostatas, kurios nebenaudojamos: **`digna_FERNET_KEY`** iš `[base]` bei **`digna_APP_HOST`** ir **`digna_APP_PORT`** iš `[app]` — adresą ir prievadą serveris dabar gauna iš `digna serve`.

    Ką daro kiekviena nuostata, aprašyta skyriuje [Užkulisinės dalies konfigūracija](#backend-configuration).

!!! warning "Vienkartinis prisijungimas: pasikeitė [oidc_clients] formatas"

    Leidime 2026.06 lentelių masyvą pakeičia po vieną lentelę kiekvienam tiekėjui, pavadintą pagal tiekėjo raktą. `DIGNA_OIDC_KEY` nebelieka — raktas dabar yra skyriaus antraštės dalis.

    Prieš:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Po:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Pakartokite skyrių kiekvienam tiekėjui ir kiekvieną raktą išlaikykite tokį pat kaip `key` faile `dashboard_config.toml`. `digna config check` praneša `oidc_clients` kaip FAILED, kol lieka senoji forma. Tai liečia tik diegimus, kurie naudoja vienkartinį prisijungimą.

#### 5 žingsnis: Perkraukite žiniatinklio serverį

Dashboard yra statinių failų rinkinys, todėl jūsų žiniatinklio serveris — ir naršyklė — gali vis dar
pateikti ankstesnę versiją. Perkraukite arba iš naujo paleiskite žiniatinklio serverį, kuriame talpinamas `dashboard`
aplankas, tada iš naujo įkelkite puslapį priverstiniu atnaujinimu (++ctrl+f5++).

#### 6 žingsnis: Patikrinkite konfigūraciją

Prieš liesdami saugyklą įsitikinkite, kad atnaujintas `config.toml` yra išsamus:

```bash
digna config check
```

Kiekvienas skyrius turi pranešti OK. Pataisykite viską, kas pranešama kaip FAILED, ir prieš tęsdami paleiskite komandą dar kartą.

#### 7 žingsnis: Pakeiskite licencijos failą

Kiekvienai laidai licencija išduodama atskirai. Nukopijuokite `license.toml`, kurį digna komanda pateikė
šiai laidai, į diegimo katalogą, pakeisdami senąjį:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nepalikite ankstesnės licencijos"

    Ankstesnei laidai išduotas `license.toml` šios laidos neapima, o kiekviena komanda,
    tikrinanti licenciją — `user`, `inspection`, `repo` — nepavykus patikrinimui nutraukiama dar prieš paliečiant
    saugyklą. Prieš tęsdami ją patikrinkite:

    ```bash
    digna license check
    ```

#### 8 žingsnis: Atnaujinkite repozitorijos schemą

Nueikite į savo digna diegimo katalogą ir paleiskite:

```bash
digna repo upgrade
```

Tai atnaujins PostgreSQL schemą į naujausią versiją, išsaugant visus esamus duomenis.

#### 9 žingsnis: Užregistruokite ir paleiskite paslaugą

Senoji registracija buvo pašalinta 1 žingsnyje, todėl paslauga registruojama iš naujo — šį kartą
naudojant `digna` vykdomąjį failą, kuris neturi batch failų:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Parinktims `--address` ir `--port` nurodykite reikšmes, kuriomis veikė senoji paslauga, nebent norite naujų
numatytųjų reikšmių `127.0.0.1` ir `8000`; jos įrašomos į registraciją ir nebėra skaitomos
iš `config.toml`. Jei senoji paslauga veikė domeno paskyra, pridėkite `--account` ir `--password`.
Visą parinkčių sąrašą rasite skyriuje
[digna paleidimas kaip Windows paslauga](#running-digna-as-a-windows-service).

Jei paleidžiate rankiniu būdu, paleiskite serverį iš naujo:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jei naudojate IIS arba Tomcat, perkraukite atitinkamą žiniatinklio serverį.

#### 10 žingsnis: Patikrinkite atnaujinimą

1. Atidarykite digna dashboard
2. Patikrinkite, ar sąsaja pakraunama teisingai
3. Peržiūrėkite serverio žurnalus dėl galimų klaidų
4. Kiekvieną ryšį, kuris dar nenaudojo ODBC, perkelkite į ODBC, tada išbandykite visus ryšius — žiūrėkite [Ryšio tikrinimas](../../../databases/overview.md#testing-a-connection)