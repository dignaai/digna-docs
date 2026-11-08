---
title: „Windows diegimo vadovas – digna Release 2026.11“ | digna Dokumentacija
description: Žingsnis po žingsnio vadovas, kaip įdiegti digna Release 2026.11 sistemoje Windows — sistemos reikalavimai, PostgreSQL nustatymai, žiniatinklio serverio konfigūracija, backend ir dashboard konfigūracija, digna paleidimas kaip Windows paslauga ir atnaujinimas iš Release 2026.06.
keywords: digna windows diegimas, digna diegimo vadovas, digna backend nustatymas, digna dashboard diegimas, postgresql nustatymas, digna windows paslauga, digna atnaujinimo vadovas
image: /assets/logo_square.png
---

# Windows diegimo vadovas digna Release 2026.11

**Išleidimas:** 2026.11

**Paskutinį kartą atnaujinta:** 2026 m. lapkričio 7 d.


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

### Kas naujo leidime 2026.11

Šis leidimas prideda digna Data Reconciliation, digna Agentic su digna MCP Server ir digna Engine, kuris gali profiliuoti duomenis pačioje digna ir tikrinti nuorodų vientisumą tarp skirtingų duomenų bazių technologijų. Išsamią informaciją rasite [leidimo pastabose](../../../changelog/Release_202611.md).

Diegimui leidimas atneša naują saugyklos migracijų mechanizmą, neprivalomą `[duckdb]` skyrių faile `config.toml`, skirtą digna Engine, ir naują licencijos failą. Kiekvieną iš jų aptaria [atnaujinimo skyrius](#upgrading-to-a-new-release).

### Ieškote macOS ar Linux?

Šis vadovas skirtas Windows. Kitoms platformoms žiūrėkite [macOS diegimo vadovą](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) arba [Linux diegimo vadovą](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Duomenų bazės ryšiai, kurių profiliavimo vieta yra digna Engine, profiliuojami pačiame digna
    pagrindiniame kompiuteryje. Numatykite jiems papildomos atminties ir disko vietos, žr.
    [\[duckdb\] skyrių](#duckdb-section).

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

Ši skiltis konfigūruoja kryžminės kilmės išteklių bendrinimą (CORS) tarp dashboard ir backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard URL adresai | URL adresai, iš kurių pateikiamas dashboard. Naršyklės užklausos iš bet kurios kitos kilmės atmetamos |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Būtina, kad naršyklė su kiekviena užklausa siųstų sesijos slapuką |

!!! info "[app] skiltis yra neprivaloma"

    Nuo Release 2026.11 abu raktus ir visą `[app]` skyrių galima praleisti. Tai tinkama sąranka, kai
    atvirkštinis tarpinis serveris (reverse proxy) pateikia dashboard ir backend su ta pačia kilme
    (origin): tada naršyklė nesiunčia kryžminės kilmės užklausų, o pagal numatytuosius nustatymus nė
    viena neleidžiama.

#### [repo] skiltis

Ši skiltis konfigūruoja prisijungimą prie PostgreSQL duomenų bazės:

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

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` arba IP | PostgreSQL serverio hostname/IP |
| `DIGNA_REPO_PORT` | `5432` (numatytasis) | PostgreSQL prievadas |
| `DIGNA_REPO_DB` | `postgres` | Duomenų bazės pavadinimas |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Anksčiau sukurta schema |
| `DIGNA_REPO_USER` | `digna_user` | Vartotojas sukurtas PostgreSQL nustatymuose |
| `DIGNA_REPO_PASSWORD` | Jūsų slaptažodis | Slaptažodis nustatytas kuriant schemą |
| `DIGNA_REPO_SSLMODE` | `prefer` (numatytasis) | Neprivaloma. PostgreSQL SSL režimas: `disable`, `allow`, `prefer`, `require`, `verify-ca` arba `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (numatytasis) | Neprivaloma. Kiek ryšių su saugykla digna laiko atvirų |

#### [base] skiltis

Šioje skiltyje yra saugumo, slapukų ir inspekcijų nustatymai:

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

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_FERNET_KEY` | Aukščiau parodyta reikšmė | Ankstesnių leidimų naudoto šifravimo raktas. Jis turi būti nurodytas; palikite parodytą reikšmę |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Pagrindinis kompiuteris (host), kuriuo pasiekiamas dashboard. `""` nenustato jokio domeno – tai tinka už tarpinio serverio, kuris dashboard ir backend pateikia su ta pačia kilme |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Turi būti `true` visada, kai digna pateikiama per HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Sesijos slapukas lieka nepasiekiamas skriptams |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 val.) | Sesijos laikas sekundėmis |
| `DIGNA_MAX_WORKERS` | CPU branduolių skaičius - 1 | Kiek inspekcijų gali vykti vienu metu |
| `DIGNA_FRONTEND_BASEURL` | Dashboard URL | Privaloma. Naudojamas nuorodoms pranešimuose, todėl tai turi būti URL, kurį gavėjai gali atidaryti |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (numatytasis) | Neprivaloma. Kiek sekundžių viena užklausa į šaltinio duomenų bazę gali vykti, kol bus nutraukta; `0` išjungia skirtąjį laiką |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (numatytasis) | Neprivaloma. Kiek sekundžių laukti prisijungimo prie šaltinio duomenų bazės; `0` laukia neribotai |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` arba `DEBUG` | `INFO` produkcijai, `DEBUG` trikčių šalinimui. Taip pat priimami `TRACE`, `WARN` ir `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (numatytasis) | Neprivaloma. Rotuojamų žurnalo failų katalogas, nurodomas darbinio katalogo atžvilgiu |
| `DIGNA_LOGGING_MAX_FILES` | `30` (numatytasis) | Neprivaloma. Kiek rotuotų žurnalo failų saugoti |

!!! warning "Veikiant kaip paslauga, palikite žurnalų katalogą"

    Windows paslauga neturi konsolės, todėl žurnalo failai yra vienintelis įrašas apie tai, ką
    paslauga daro. Nenustatykite `DIGNA_LOGGING_DIR` kaip tuščios eilutės – taip žurnalo failai
    išjungiami.

#### [duckdb] skiltis (neprivaloma) {: #duckdb-section }

Naujiena nuo Release 2026.11. Ši skiltis nustato **digna Engine** išteklius. digna Engine
profiliuoja duomenis pačioje digna tiems duomenų bazės ryšiams, kurių profiliavimo vieta yra
**digna Engine**, ir vykdo nuorodų vientisumo patikras tarp duomenų šaltinių, esančių skirtinguose
duomenų bazės ryšiuose. Žr. [Profiliavimo vieta](../../../platform/profiling/profiling_location.md).

Skiltis yra neprivaloma. Be jos taikomos toliau nurodytos numatytosios reikšmės.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (numatytasis) | Atmintis MB, kurią gali naudoti vienas digna Engine vykdymas. Vienu metu gali būti aktyvūs iki `DIGNA_MAX_WORKERS` vykdymų |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Numatytoji: digna paleidžiančios paskyros laikinasis katalogas (`%TEMP%`) | Laikinųjų failų katalogas, kai duomenys netelpa į atmintį |

!!! tip "digna Engine išteklių planavimas"

    digna pagrindiniame kompiuteryje, be atminties, kurią naudoja pati digna, numatykite iki
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` atminties, o laikinajame kataloge –
    pakankamai laisvos disko vietos, kad tilptų didžiausios tikrinamos datos duomenys iš duomenų
    šaltinių, naudojančių digna Engine. Nukreipkite `DIGNA_DUCKDB_TEMP_DIRECTORY` į diską su tokia
    vieta, į kurį gali rašyti digna paleidžianti paskyra:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Šio skilties reikia tik tada, jei bent vienas duomenų bazės ryšys naudoja digna Engine arba
    nuorodų vientisumo patikra lygina duomenų šaltinius skirtinguose ryšiuose.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Pataisykite viską, kas pranešama kaip FAILED, ir prieš tęsdami paleiskite komandą dar kartą. Įspėjimas WARNING ties **Unknown keys** išvardija `config.toml` raktus, kurių digna neskaito; jie neturi jokio poveikio, todėl juos pašalinkite arba pataisykite jų rašybą. Visas parinkčių sąrašas pateiktas [CLI žinyne](../../../cli/Command_Line_Interface_202611.md).

### 3 žingsnis: Inicializuokite repozitoriją

1. Atidarykite Command Prompt
2. Nueikite į savo digna diegimo katalogą (ten, kur `config.toml` ir `digna` vykdomasis failas)
3. Paleiskite ryšio testą:

```bash
digna repo check
```

Naujoje schemoje komanda prisijungia ir tada praneša, kad saugykla dar neįdiegta:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Šiame etape tai yra laukiamas rezultatas: jis patvirtina, kad digna pasiekia PostgreSQL ir schemą. Prisijungimo ar autentifikavimo klaida, priešingai, rodo į `[repo]` skyrių arba PostgreSQL sąranką.

### 4 žingsnis: Įdiekite repozitorijos schemą

Toje pačioje direktorijoje paleiskite:

```bash
digna repo upgrade
```

Ši komanda įdiegia reikalingas lenteles saugyklos schemoje ir baigiasi pranešimu:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade įdiegia ir atnaujina"

    Nuo Release 2026.11 `repo upgrade` įdiegia naują saugyklą ir atnaujina esamą.
    `repo install` vis dar veikia kaip kitas tos pačios komandos pavadinimas.

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
- `--address` — serverio hostname/IP (numatytasis `127.0.0.1`)
- `--port` — serverio prievadas (numatytasis `8000`)

Kai serveris pasileidžia, jis išveda adresą, kuriuo klausosi:

```text
Server running on http://127.0.0.1:8082
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
parinkčių sąrašas pateiktas [CLI žinyne](../../../cli/Command_Line_Interface_202611.md).

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

Šiame skyriuje aprašomas Release 2026.06 diegimo atnaujinimas į Release 2026.11.

!!! warning "Atnaujinimas iš senesnės nei 2026.06 versijos"

    Pirmiausia atlikite Release 2026.06 atnaujinimo veiksmus: [Atnaujinimas į naują leidimą](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Tada tęskite toliau pateiktais veiksmais.

### Prieš atnaujinimą

**Būtina sukurti digna repozitorijos atsarginę kopiją**

Prieš atnaujinant digna, atsargiai atsarginę kopiją savo repozitorijos (PostgreSQL), kad apsisaugotumėte nuo duomenų praradimo.
Atsarginė kopija leis atkurti duomenis, jei atnaujinimo metu kils nenumatytų problemų.

**Release 2026.11 licencijos failo užsakymas**

Release 2026.11 reikia naujo `license.toml`. Prieš pradėdami paprašykite jo digna komandos ir
turėkite jį paruoštą [7 žingsniui](#step-7-replace-the-license-file).

### Atnaujinimo procesas

#### 1 žingsnis: Sustabdykite digna paslaugą {: #step-1-stop-the-digna-service }

Atidarykite Command Prompt kaip administratorius ir sustabdykite paslaugą dabartinio diegimo
vykdomuoju failu `digna`:

```bash
cd C:\path\to\digna
digna windows stop
```

Paslauga lieka užregistruota. Naujasis vykdomasis failas pakeičia senąjį tame pačiame kataloge,
todėl registracija ir toliau rodo į tinkamą failą.

Jei digna veikia pirmame plane, paspauskite ++ctrl+c++ jos Command Prompt lange.

#### 2 žingsnis: Sukurkite dabartinio diegimo atsarginę kopiją {: #step-2-backup-current-installation }

Savo digna diegimo kataloge pervadinkite dabartinio diegimo vykdomąjį failą ir `dashboard` aplanką,
kad naują leidimą būtų galima įdiegti šalia jų:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

`digna_old.exe` laikykite, kol patikrinsite atnaujinimą, o `dashboard_old` – kol iš jo atkursite savo
konfigūracijos failus (žr. 4 žingsnį). Po to abu galite ištrinti.

#### 3 žingsnis: Išskleiskite ir naudokite naują versiją {: #step-3-extract-and-deploy-new-version }

1. Išskleiskite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į savo diegimo katalogą


!!! warning "Svarbu"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` niekada nėra įtraukti į
    diegimo ZIP — digna komanda niekada nepateikia nė vieno iš šių failų. Todėl atnaujinimas jūsų
    esamos konfigūracijos nepaliečia, o kopijos pervadintuose `*_old` aplankuose yra
    vienintelės, kurias turite.

#### 4 žingsnis: Atkurkite konfigūracijos failus {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Release 2026.11 nereikia keisti `config.toml`: failas, veikiantis su Release 2026.06, veikia ir
toliau. Du pakeitimai yra neprivalomi:

- Pridėkite [`[duckdb]` skyrių](#duckdb-section), jei duomenų bazės ryšiai turi naudoti
  digna Engine, o jo numatytosios reikšmės netinka jūsų pagrindiniam kompiuteriui.
- Praleiskite `[app]` skyrių, jei atvirkštinis tarpinis serveris dashboard ir backend pateikia su
  ta pačia kilme.

!!! warning "Nustatymai, kurių digna neskaito"

    Ankstesnėse šio vadovo versijose buvo parodyta keletas nustatymų, kurių digna neskaito. Jie
    neturi jokio poveikio, o `config check` 6 žingsnyje juos išvardija ties **Unknown keys**.
    Pašalinkite arba pataisykite juos:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` ir
      `digna_LOGGING_BACKUP_COUNT` neegzistuoja. Pašalinkite juos.
    - Nustatymų pavadinimuose skiriamos didžiosios ir mažosios raidės. digna skaito
      `DIGNA_REPO_HOST`, o ne `digna_REPO_HOST`. Kiekvieną pavadinimą rašykite didžiosiomis
      raidėmis, kaip skyriuje [Backend konfigūracija](#backend-configuration).

!!! warning "Vienkartinis prisijungimas: palikite [[oidc_clients]]"

    digna vienkartinio prisijungimo tiekėjus skaito kaip `[[oidc_clients]]` įrašų sąrašą, kurių
    kiekvienas turi savo `DIGNA_OIDC_KEY`. Jei pakeitėte savo tiekėjus į `[oidc_clients.<key>]`
    skyrius, kaip buvo parodyta ankstesnėje šio vadovo versijoje, pakeiskite juos atgal. Kol
    naudojama ta forma, `config check` praneša `OIDC config(s)` kaip FAILED:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Pakartokite įrašą kiekvienam tiekėjui ir kiekvieną `DIGNA_OIDC_KEY` išlaikykite tokį pat kaip
    `key` faile `dashboard_config.toml`. Tai liečia tik diegimus, kurie naudoja vienkartinį
    prisijungimą.

#### 5 žingsnis: Perkraukite žiniatinklio serverį {: #step-5-reload-the-web-server }

Dashboard yra statinių failų rinkinys, todėl jūsų žiniatinklio serveris — ir naršyklė — gali vis dar
pateikti ankstesnę versiją. Perkraukite arba iš naujo paleiskite žiniatinklio serverį, kuriame talpinamas `dashboard`
aplankas, tada iš naujo įkelkite puslapį priverstiniu atnaujinimu (++ctrl+f5++).

#### 6 žingsnis: Patikrinkite konfigūraciją {: #step-6-validate-the-configuration }

Prieš liesdami saugyklą įsitikinkite, kad `config.toml` yra išsamus:

```bash
digna config check
```

Kiekvienas skyrius turi pranešti OK. Pataisykite viską, kas pranešama kaip FAILED, pašalinkite
raktus, išvardytus ties **Unknown keys**, ir prieš tęsdami paleiskite komandą dar kartą.

#### 7 žingsnis: Pakeiskite licencijos failą {: #step-7-replace-the-license-file }

Licencijos failas paprastai pereina iš vieno leidimo į kitą. Release 2026.11 yra išimtis: jis
prideda du licencijuojamus modulius, digna Data Reconciliation ir digna Agentic, o licencijoje,
išduotoje iki 2026.11, jų nėra. Nukopijuokite `license.toml`, kurį digna komanda pateikė
Release 2026.11, į diegimo katalogą, pakeisdami senąjį:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nepalikite ankstesnės licencijos"

    Su ankstesne licencija digna vis tiek pasileidžia, tačiau digna Data Reconciliation ir
    digna MCP Server lieka išjungti. Kiekviena komanda, tikrinanti licenciją — `user`,
    `inspection`, `repo` — nepavykus patikrinimui nutraukiama dar prieš paliečiant saugyklą. Prieš
    tęsdami patikrinkite naująją licenciją:

    ```bash
    digna license check
    ```

#### 8 žingsnis: Atnaujinkite repozitorijos schemą {: #step-8-upgrade-the-repository-schema }

Savo digna diegimo kataloge paleiskite:

```bash
digna repo upgrade
```

Release 2026.11 saugyklos schemą valdo versijuotomis migracijomis. Pirmasis atnaujinimas iš
ankstesnio leidimo perkelia schemą į paskutinę ankstesnės versijavimo schemos versiją, užfiksuoja ją
kaip pradinį tašką ir tada pritaiko Release 2026.11 migracijas. Jis baigiasi pranešimu:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Visi esami duomenys išsaugomi. Norėdami bet kada pamatyti saugyklos būseną, paleiskite
`digna repo check`: komanda išvardija paskutinę pritaikytą migraciją ir visas laukiančias.

!!! warning "digna nepasileidžia su pasenusia saugykla"

    Nuo Release 2026.11 serveris atsisako pasileisti, kol saugyklą reikia atnaujinti, ir apie tai
    praneša, pavyzdžiui:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Prieš paleisdami serverį ar paslaugą, paleiskite `repo upgrade`.

#### 9 žingsnis: Iš naujo paleiskite paslaugas {: #step-9-restart-services }

Jei digna veikia kaip Windows paslauga, vėl ją paleiskite:

```bash
cd C:\path\to\digna
digna windows start
```

Jei paleidžiate rankiniu būdu, iš naujo paleiskite serverį:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jei naudojate IIS arba Tomcat, iš naujo paleiskite atitinkamą žiniatinklio serverį.

#### 10 žingsnis: Patikrinkite atnaujinimą {: #step-10-verify-the-upgrade }

1. Patikrinkite naujojo vykdomojo failo leidimą:

    ```bash
    digna version
    ```

    Pirmoji eilutė turi būti `Release: 2026.11`.

2. Atidarykite digna dashboard ir patikrinkite, ar sąsaja įkeliama teisingai.
3. Patikrinkite diegimo `logs` katalogo failus, ar nėra klaidų.
4. Išbandykite savo duomenų bazės ryšius — žr.
   [Ryšio tikrinimas](../../../databases/overview.md#testing-a-connection). Po atnaujinimo iš
   senesnio nei 2026.06 leidimo pirmiausia perkelkite į ODBC kiekvieną ryšį, kuris dar nenaudojo ODBC.

Norėdami pradėti dirbti su naujais moduliais, žr. [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI agento prijungimas](../../../platform/agentic/connect_ai_agent.md) – apie digna MCP Server, ir
[Profiliavimo vieta](../../../platform/profiling/profiling_location.md) – apie digna Engine.
