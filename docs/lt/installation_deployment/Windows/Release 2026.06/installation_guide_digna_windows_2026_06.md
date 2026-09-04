---
title: „Windows diegimo vadovas – digna Release 2026.06“ | digna Dokumentacija
description: Žingsnis po žingsnio vadovas, kaip įdiegti digna Release 2026.06 sistemoje Windows — sistemos reikalavimai, PostgreSQL nustatymai, žiniatinklio serverio konfigūracija, backend ir dashboard konfigūracija, digna paleidimas kaip Windows paslauga ir atnaujinimas į naują leidimą.
keywords: digna windows diegimas, digna diegimo vadovas, digna backend nustatymas, digna dashboard diegimas, postgresql nustatymas, digna windows paslauga, digna atnaujinimo vadovas
image: /assets/logo_square.png
---

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

- **dignabackend**: pagrindinis programos variklis, atsakingas už duomenų apdorojimą ir kokybės patikrinimus.
- **dignadashboard**: žiniatinklio sąsaja, talpinama ant web serverio, suteikianti patogią sąveiką su digna platforma ir duomenų kokybės metrikų vizualizavimą.

### Kas naujo leidime 2026.06

Šis leidimas prideda duomenų stebėjimo (data observability) galimybes tiesiai į jūsų kodą, leidžiant programuotojams stebėti duomenų kokybę ties šaltiniu. Pilną informaciją rasite [išleidimo pastabose](http://docs.digna.ai/changelog/Release_202606/).

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

> **⚠️ Rekomenduojama specifikacija**
>
> - **Atmintis**: 32 GB RAM (vietoje 16 GB)
> - **Disko vieta**: 50 GB laisvos vietos (vietoje 10 GB)
>
> Šios didesnės specifikacijos leidžia sklandžiai veikti tiek digna, tiek PostgreSQL duomenų bazei vienu metu.

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

> **💡 Patarimas**
>
> Jei prievadas 5432 jau užimtas, pasirinkite alternatyvų prievadą ir užsirašykite jį vėlesnei konfigūracijai.

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

> **⚠️ Svarbu**
>
> Be šio nustatymo `.md` failai gali būti netinkamai aptarnaujami.

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

> **💡 Patarimas**
>
> Apache Tomcat paprastai paleidžiamas automatiškai po diegimo. Jei ne, eikite į `bin` katalogą ir paleiskite `startup.bat`.

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

> **✅ Gera praktika**
>
> Naudokite stiprius, sudėtingus slaptažodžius duomenų bazės vartotojams. Venkite lengvai atspėjamų kredencialų.

---

### 2 žingsnis: Ištraukite digna diegimo paketą

1. Raskite jums pateiktą digna diegimo ZIP failą
2. Išskleiskite jį į pageidaujamą diegimo vietą
3. Po išskleidimo turėtumėte matyti šiuos elementus:
   - `dashboard/` — web dashboard sąsaja
   - `digna` — pagrindinis vykdomasis failas (backend + CLI kartu)
   - `config.toml` — konfigūracijos failas
   - `license.toml` — licencijos failas (kopijuokite čia savo licenciją)

### 3 žingsnis: Įdiekite licencijos failą

> **⚠️ Svarbu**
>
> Licencijos failas **neįtrauktas** į diegimo paketą ir bus pateiktas atskirai iš digna.

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
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_APP_HOST` | `localhost` arba IP adresas | Hostname arba IP, kur talpinamas dignabackend |
| `digna_APP_PORT` | `8082` (numatytasis) | REST API galinių taškų prievadas |
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
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_FERNET_KEY` | Šifravimo raktas | Naudojamas tokenams ir slapukams šifruoti (numatytas pateiktas) |
| `digna_COOKIE_DOMAIN` | `localhost` | Atitinka jūsų frontendo domeną |
| `digna_COOKIE_SECURE` | `false` (lokaliai) / `true` (produkcijoje) | Naudokite `true` HTTPS ryšiams |
| `digna_COOKIE_HTTPONLY` | `true` | Visada įjungta dėl saugumo |
| `digna_COOKIE_SAME_SITE` | `lax` | Apsaugo nuo CSRF atakų |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 val.) | Sesijos laikas sekundėmis |
| `digna_MAX_WORKERS` | CPU branduolių skaičius - 1 | Lygų paralelinių tikrinimų užduočių skaičius |

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

### 5 žingsnis: Paleiskite digna serverį

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

### 6 žingsnis: Sukurkite administratoriaus vartotoją

1. Atidarykite **naują** Command Prompt langą
2. Nueikite į digna diegimo katalogą
3. Paleiskite šią komandą, kad sukurtumėte administratorių:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Pavyzdys:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

Tai sukurs vartotoją su pilnomis administravimo teisėmis.

> **✅ Gera praktika**
>
> Naudokite stiprų slaptažodį su didžiosiomis, mažosiomis raidėmis, skaičiais ir specialiaisiais simboliais.

---

## Dashboard konfigūracija {: #dashboard-configuration }

### 1 žingsnis: Patalpinkite dashboard į žiniatinklio serverį

digna dashboard turi atskirą `config.toml` failą, esantį `dashboard/` kataloge. Ši konfigūracija jau pateikta ir pradiniame diegime jos keisti nereikia. Ją reikia keisti tik tuo atveju, jei norite pritaikyti backend prisijungimą.

Jei reikia modifikuoti dashboard konfigūraciją (pvz., daugiaserveriniam diegimui), kreipkitės į dashboard dokumentaciją.

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

### Paslaugos valdymo failai

Visi reikalingi failai yra digna diegimo kataloge, po: `bin/`

Šie batch failai yra prieinami:
- `install_service.bat` — registruoja digna kaip Windows paslaugą
- `uninstall_service.bat` — panaikina paslaugos registraciją
- `start_service.bat` — paleidžia paslaugą
- `stop_service.bat` — sustabdo paslaugą

> **⚠️ Reikalingos administratoriaus teisės**
>
> Visi batch failai turi būti vykdomi su Administrator privilegijomis.

### Paslaugos įdiegimas

1. **Atidarykite Command Prompt kaip administratorius**
   - Dešiniuoju pelės mygtuku spustelėkite Command Prompt
   - Pasirinkite "Run as Administrator"

2. **Nueikite į bin katalogą**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Paleiskite diegimo skriptą**
   ```bash
   install_service.bat
   ```

Digna serveris dabar užregistruotas kaip Windows paslauga su **automatinio paleidimo** nustatymu. Paslauga nebus paleista iš karto — žr. kitą skyrių, kaip ją paleisti.

### Paslaugos paleidimas ir sustabdymas

#### Paslauga paleidimui

1. Atidarykite Command Prompt kaip administratorius
2. Nueikite į `digna\bin`
3. Vykdykite:
   ```bash
   start_service.bat
   ```

#### Paslauga sustabdymui

1. Atidarykite Command Prompt kaip administratorius
2. Nueikite į `digna\bin`
3. Vykdykite:
   ```bash
   stop_service.bat
   ```

> **💡 Patarimas**
>
> Visada sustabdykite paslaugą prieš atnaujinant programos failus.

### Perkėlimas paslaugos į naują katalogą

Jei reikia perkelti digna diegimą:

1. **Išjunkite esamą paslaugą**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Perkelkite aplikacijos failus**
   - Perkelkite visą digna diegimo aplanką į naują vietą

3. **Įdiekite paslaugą iš naujo**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Paleiskite paslaugą**
   ```bash
   start_service.bat
   ```

### Paslaugos pašalinimas

1. **Sustabdykite veikiančią paslaugą**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Pašalinkite paslaugą**
   ```bash
   uninstall_service.bat
   ```

Digna serveris dabar atregistruotas kaip Windows paslauga.

---

## Atnaujinimas į naują leidimą {: #upgrading-to-a-new-release }

### Prieš atnaujinimą

**Būtina sukurti digna repozitorijos atsarginę kopiją**

Prieš atnaujinant digna, atsargiai atsarginę kopiją savo repozitorijos (PostgreSQL), kad apsisaugotumėte nuo duomenų praradimo.
Atsarginė kopija leis atkurti duomenis, jei atnaujinimo metu kils nenumatytų problemų.

### Atnaujinimo procesas

#### 1 žingsnis: Sustabdykite digna paslaugą

Jei digna veikia kaip Windows paslauga, pirmiausia ją sustabdykite:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### 2 žingsnis: Saugokite esamą backend diegimą

Jūsų digna diegimo kataloge:

```bash
# Pervardykite katalogą su dignabackend
ren dignabackend dignabackend_old
```
```bash
# Pervardykite dashboard
ren dashboard dashboard_old
```

#### 3 žingsnis: Išskleiskite ir naudokite naują versiją

1. Išskleiskite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į savo diegimo katalogą


> **✅ Svarbu**
>
> `config.toml` failas **niekada** neįtrauktas į diegimo ZIP. Jūsų esama konfigūracija lieka saugi.

### 4 žingsnis: Atkurkite konfigūracijos failus

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### 5 žingsnis: Atnaujinkite repozitorijos schemą

Nueikite į savo digna diegimo katalogą ir paleiskite:

```bash
digna repo upgrade
```

Tai atnaujins PostgreSQL schemą į naujausią versiją, išsaugant visus esamus duomenis.

### 6 žingsnis: Perkraukite paslaugas

Jei naudojate Windows paslaugą:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Jei paleidžiate rankiniu būdu, paleiskite serverį iš naujo:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jei naudojate IIS arba Tomcat, perkraukite atitinkamą žiniatinklio serverį.

#### 7 žingsnis: Patikrinkite atnaujinimą

1. Atidarykite digna dashboard
2. Patikrinkite, ar sąsaja pakraunama teisingai
3. Peržiūrėkite serverio žurnalus dėl galimų klaidų
