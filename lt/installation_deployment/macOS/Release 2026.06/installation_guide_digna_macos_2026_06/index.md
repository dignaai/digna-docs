# macOS diegimo vadovas digna leidimui 2026.06

**Leidimas:** 2026.06

**Paskutinį kartą atnaujinta:** 2026 m. rugsėjo 5 d.


---

## Turinys

1. [Įvadas](#introduction)
2. [Sistemos reikalavimai](#system-requirements)
3. [Prieš diegiant](#pre-installation-setup)
4. [PostgreSQL serverio nustatymas](#postgresql-server-setup)
5. [Tinklapio serverio konfigūracija](#web-server-configuration)
6. [Pradinis diegimas](#initial-installation)
7. [Backend konfigūracija](#backend-configuration)
8. [Dashboard konfigūracija](#dashboard-configuration)
9. [digna paleidimas kaip foninė paslauga](#running-digna-as-a-background-service)
10. [Atsinaujinimas į naują leidimą](#upgrading-to-a-new-release)

---

## Įvadas {: #introduction }

### Apie digna

digna yra išsami, dirbtiniu intelektu paremta platforma, skirta optimizuoti duomenų kokybės valdymą įvairiose duomenų aplinkose — sandėliuose, ežeruose ir lakehouse tipo sistemose. Sukurta skalabilumui ir pritaikomumui, digna sprendžia šiuolaikines duomenų problemas per automatizavimą, realaus laiko stebėjimą ir anomalijų aptikimą.

digna susideda iš dviejų pagrindinių komponentų:

- **dignabackend**: pagrindinis taikomosios programos variklis, atsakingas už duomenų apdorojimą ir kokybės patikrinimus.
- **dignadashboard**: internetinė sąsaja, talpinama tinklapio serveryje, leidžianti vartotojams patogiai sąveikauti su digna platforma ir vizualizuoti duomenų kokybės metrikas.

### Kas naujo leidime 2026.06

Šis leidimas įterpia duomenų stebėjimo (observability) galimybes tiesiai į jūsų kodą, leidžiant kūrėjams stebėti duomenų kokybę prie pat šaltinio. Pilną informaciją rasite [išleidimo pastabose](http://docs.digna.ai/changelog/Release_202606/).

### Ieškote Windows arba Linux diegimo instrukcijų?

Šis vadovas skirtas macOS. Kitiems platformoms žr. [Windows diegimo vadovą](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) arba [Linux diegimo vadovą](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Sistemos reikalavimai {: #system-requirements }

Prieš pradėdami diegimą, įsitikinkite, kad jūsų sistema atitinka šiuos minimalius reikalavimus:

| Reikalavimas | Specifikacija |
|---|---|
| **Operacinė sistema** | macOS 13 (Ventura) arba naujesnė |
| **Architektūra** | Apple Silicon (arm64) arba Intel (x86_64) |
| **Atmintis (Minimalus rinkinys)** | 16 GB RAM |
| **Disko vieta** | 10 GB laisvos vietos |
| **Duomenų bazė** | PostgreSQL Server 12 arba naujesnė |
| **Tinklapio serveris** | nginx, Apache httpd arba ekvivalentas |
| **Konsolės įrankiai** | Xcode Command Line Tools (reikalinga Homebrew) |

### Duomenų bazės diegimo parinktys

**Jei PostgreSQL jau įdiegtas:**
Galite pridėti naują duomenų bazę digna savo esamam PostgreSQL serveriui.

**Jei diegiate PostgreSQL tame pačiame kompiuteryje kaip digna:**

!!! info "Rekomenduojamos specifikacijos"

    - **Atmintis**: 32 GB RAM (vietoj 16 GB)
    - **Disko vieta**: 50 GB laisvos vietos (vietoj 10 GB)

    Šios didesnės specifikacijos leidžia tuo pačiu metu paleisti tiek digna, tiek PostgreSQL.

### Kaip patikrinti savo architektūrą

Kai kurie keliai šiame vadove skiriasi Apple Silicon ir Intel Mac kompiuteriams. Norėdami sužinoti, kurį turite, atidarykite **Terminal** ir vykdykite:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew įdiegiamas į `/opt/homebrew`.
- `x86_64` — Intel. Homebrew įdiegiamas į `/usr/local`.

!!! tip "Patarimas"

    Vietoj kelių kietai užkoduotų kelių, šiame vadove naudojamas `$(brew --prefix)`, kuris išplečia teisingą vietą abiejose architektūrose. Galite kopijuoti komandas tiesiogiai.

---

## Prieš diegiant {: #pre-installation-setup }

Prieš įdiegdami digna, įsitikinkite, kad yra trys svarbios prielaidos:

1. **Homebrew** – paketų tvarkyklė, naudojama toliau pateiktiems komponentams įdiegti
2. **PostgreSQL Server** – skaičiuotoms metrikoms ir našumo duomenims saugoti
3. **Tinklapio serveris** – digna Dashboard talpinimui

Jei šių komponentų dar nėra, vykdykite žemiau pateiktas instrukcijas juos įdiegti ir sukonfigūruoti.

### Homebrew diegimas

Homebrew yra standartinė paketų tvarkyklė macOS ir naudojama šiame vadove PostgreSQL bei nginx diegimui.

#### 1 žingsnis: patikrinkite, ar Homebrew jau įdiegtas

Atidarykite **Terminal** (paspauskite `Cmd + Space`, įrašykite `Terminal`, paspauskite Enter) ir vykdykite:

```bash
brew --version
```

Jei grąžinamas versijos numeris, pereikite prie skyriaus [PostgreSQL serverio nustatymas](#postgresql-server-setup).

#### 2 žingsnis: Homebrew įdiegimas

Jei komanda nebuvo rasta, įdiekite Homebrew pagal nurodymus oficialiame [Homebrew puslapyje](https://brew.sh). Diegimo programa taip pat įdiegia Xcode Command Line Tools, jei jų dar nėra.

#### 3 žingsnis: pridėti Homebrew į PATH

Apple Silicon įdiegimo programa išspausdina dvi komandas Homebrew pridėjimui prie jūsų shell aplinkos. Vykdykite jas pagal instrukcijas, tada patikrinkite:

```bash
brew --prefix
```

Tai turėtų išvesti `/opt/homebrew` Apple Silicon arba `/usr/local` Intel atveju.

---

## PostgreSQL serverio nustatymas {: #postgresql-server-setup }

### Jei PostgreSQL jau yra

Jei PostgreSQL jau įdiegtas ir veikia jūsų vietiniame kompiuteryje arba naudojate valdomą nuotolinį PostgreSQL serverį, galite pereiti prie kito skyriaus [Tinklapio serverio konfigūracija](#web-server-configuration).

### Diegimo parinktys

macOS siūlo dvi paprastas PostgreSQL diegimo galimybes. Pasirinkite **vieną**:

- [Homebrew](#postgresql-homebrew) — diegimas per komandų eilutę, rekomenduojama serverio diegimams
- [Postgres.app](#postgresql-app) — grafiškas diegimas, patogu vietiniam vertinimui

### PostgreSQL diegimas per Homebrew {: #postgresql-homebrew }

#### 1 žingsnis: įdiekite PostgreSQL formulę

```bash
brew install postgresql@16
```

#### 2 žingsnis: pridėkite PostgreSQL į PATH

Sukonfigūruotos versijuotos PostgreSQL formulės yra *keg-only*, todėl Homebrew automatiškai neįtraukia jų komandų į jūsų PATH. Pridėkite jas patys:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Pastaba"

    Tai daroma prielaidą, kad naudojate numatytąjį `zsh` shell, kurį naudoja macOS. Jei naudojate `bash`, pridėkite tą pačią eilutę į `~/.bash_profile`.

#### 3 žingsnis: paleiskite PostgreSQL paslaugą

```bash
brew services start postgresql@16
```

Tai paleidžia PostgreSQL iš karto ir sukonfigūruoja automatinį paleidimą prisijungiant.

#### 4 žingsnis: patikrinkite diegimą

```bash
psql --version
```

Turėtumėte matyti PostgreSQL versiją, jei diegimas buvo sėkmingas.

#### 5 žingsnis: prisijunkite prie serverio

```bash
psql postgres
```

!!! warning "Svarbu — macOS čia skiriasi nuo Windows"

    Windows diegimo programa prašo sukurti `postgres` supervartotoją ir slaptažodį. Homebrew to nedaro. Vietoje to sukuriamas supervartotojas su jūsų **macOS paskyros** vardu, be slaptažodžio, pasiekiamas tik iš vietinio kompiuterio.

    Tai reiškia, kad šviežio Homebrew diegimo aplinkoje nėra `postgres` rolės. Naudokite savo paskyros vardą, kai reikia supervartotojo, ir sukurkite atskirą digna vartotoją, kaip aprašyta skyriuje [Pradinis diegimas](#initial-installation).

#### 6 žingsnis: patvirtinkite prievadą

Numatytasis PostgreSQL prievadas yra `5432`. Norėdami patikrinti, kokį prievadą serveris naudoja:

```bash
psql postgres -c "SHOW port;"
```

Užsirašykite reikšmę — jos reikės konfigūruojant digna backend.

### PostgreSQL diegimas su Postgres.app {: #postgresql-app }

Jei pageidaujate grafiško sprendimo:

1. Atsisiųskite [Postgres.app](https://postgresapp.com) ir vilkite į **Applications** katalogą
2. Atidarykite aplikaciją ir spustelėkite **Initialize**, kad sukurtumėte naują serverį
3. Sekite programos nurodymus, kaip pridėti jos komandų eilutės įrankius į PATH
4. Patikrinkite diegimą:

```bash
psql --version
```

Postgres.app taip pat sukuria supervartotoją, pavadintą pagal jūsų macOS paskyros vardą.

---

## Tinklapio serverio konfigūracija {: #web-server-configuration }

digna reikalauja tinklapio serverio dashboard talpinimui. Pasirinkite vieną iš pateiktų variantų:

- [nginx](#nginx-setup) — įdiegiamas per Homebrew, rekomenduojama
- [Apache httpd](#apache-setup) — įtrauktas į macOS

Jums reikia įdiegti ir sukonfigūruoti **vieną** iš šių serverių.

Abi parinktys sukonfigūruoja du dalykus, kurių reikalauja dashboard:

- **Vienos puslapio programos fallback**, kad atnaujinus puslapį dashboard URL negrąžintų 404 klaidos
- **.md MIME tipą**, kad Markdown failai būtų teisingai tiekiami

### nginx nustatymas {: #nginx-setup }

#### Apžvalga

nginx yra lengvas, didelio našumo tinklapio serveris, tinkamas statiniam digna dashboard aptarnavimui.

#### Diegimas

```bash
brew install nginx
```

#### nginx paleidimas

```bash
brew services start nginx
```

#### Patikrinkite diegimą

1. Atidarykite naršyklę
2. Nueikite į `http://localhost:8080`
3. Turėtumėte pamatyti nginx pasveikinimo puslapį

!!! note "Pastaba — numatytasis prievadas yra 8080, ne 80"

    Homebrew sukonfigūruoja nginx klausyti prievade `8080`, kad jis galėtų veikti be administratoriaus teisių. macOS, jungiantis prie prievadų žemesnių nei 1024, reikalauja root teisių.

    Jei norite talpinti dashboard prievade 80, pakeiskite `listen 8080;` į `listen 80;` žemiau pateiktoje konfigūracijoje ir paleiskite nginx su `sudo brew services start nginx`.

#### Svetainės konfigūravimas dashboardui

Homebrew nginx konfigūracija įtraukia visus failus iš savo `servers` katalogo. Sukurkite atskirą konfigūracijos failą digna čia:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Įklijuokite žemiau pateiktą bloką, pakeisdami `/path/to/digna/dashboard` tikru keliu iki išarchyvuoto `dashboard` katalogo:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Svarbu"

    Be `try_files` direktyvos, persikrovus bet kuriam dashboard puslapiui, išskyrus šakninį URL, bus grąžinta 404 klaida. Tai nginx ekvivalentas URL Rewrite modulio, reikalingo IIS Windows aplinkoje.

#### Konfigūracijos taikymas

Patikrinkite sintaksę ir perkraukite nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd nustatymas {: #apache-setup }

#### Apžvalga

macOS komplekte yra Apache httpd, todėl diegti jo nereikia. Jis pagal numatytuosius nustatymus išjungtas.

#### Apache paleidimas

```bash
sudo apachectl start
```

#### Patikrinkite diegimą

1. Atidarykite naršyklę
2. Nueikite į `http://localhost`
3. Turėtumėte pamatyti pranešimą "It works!"

#### Privaloma: įjungti mod_rewrite

Dashboard reikalauja URL perrašymo. Atidarykite Apache konfigūraciją:

```bash
sudo nano /etc/apache2/httpd.conf
```

Suraskite šią eilutę ir pašalinkite pradinį `#`, kad ją atkomentuotumėte:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Privaloma: leisti .htaccess perrašymus

Tame pačiame faile suraskite bloką `<Directory "/Library/WebServer/Documents">` ir pakeiskite:

```apache
AllowOverride None
```

į:

```apache
AllowOverride All
```

#### Privaloma: MIME tipas Markdown failams

Vis dar faile `httpd.conf` pridėkite šią eilutę, kad Markdown failai būtų tiekiami teisingai:

```apache
AddType text/markdown .md
```

!!! warning "Svarbu"

    Be šio nustatymo `.md` failai gali būti tiekiami neteisingai.

#### Konfigūracijos taikymas

Patikrinkite konfigūraciją sintaksės klaidoms, tada perkraukite Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Pradinis diegimas {: #initial-installation }

### 1 žingsnis: sukurkite digna repozitoriją

digna repozitorija saugo visas digna apskaičiuotas metrikas. Ji veikia kaip centrinė analitinių ir našumo duomenų duomenų bazė.

#### Sukurkite repozitorijos schemą ir vartotoją

Atidarykite savo PostgreSQL klientą (psql, pgAdmin ar panašų) ir vykdykite šias SQL komandas:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Pakeiskite šiuos vietos laikiklius:**

- `<digna_repo_schema>` — pageidaujamas schemos pavadinimas (pvz., `dignarepo`)
- `<digna_repo_user>` — pageidaujamas vartotojo vardas (pvz., `digna_user`)
- `<digna_repo_password>` — saugus slaptažodis šiam vartotojui

**Pavyzdys:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Norėdami vykdyti tai per Terminalą vienu žingsniu:

```bash
psql postgres
```

Tada įklijuokite šias komandas prie `postgres=#` eilutės ir įveskite `\q`, kad išeitumėte.

!!! tip "Geriausia praktika"

    Naudokite stiprius, sudėtingus slaptažodžius duomenų bazės vartotojams. Venkite lengvai atspėjamų kredencialų.

---

### 2 žingsnis: išarchyvuokite digna diegimo paketą

1. Suraskite jums pateiktą digna diegimo ZIP failą
2. Išarchyvuokite jį į norimą diegimo vietą — pavyzdžiui `/opt/digna` arba `~/digna`
3. Po išarchyvavimo turėtumėte matyti šiuos elementus:
   - `dashboard/` — žiniatinklio dashboard sąsaja
   - `digna` — pagrindinis vykdomasis failas (backend + CLI kartu)
   - `config.toml` — konfigūracijos failas
   - `license.toml` — licencijos failas (kopijuokite savo failą čia)

Norint išarchyvuoti per Terminalą:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Padarykite vykdomąjį failą vykdomu

Priklausomai nuo to, kaip archyvas buvo perduotas, vykdomasis bitas gali būti prarastas. Nustatykite jį aiškiai:

```bash
cd /opt/digna
chmod +x digna
```

#### Jei macOS blokuoja programą

Failai, atsisiųsti per naršyklę ar paštą, gali turėti karantino atributą. Jei macOS praneša, kad programa *"cannot be opened because the developer cannot be verified"*, pašalinkite atributą iš diegimo katalogo:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternatyviai atidarykite **System Settings → Privacy & Security**, raskite užblokuotą elementą puslapio apačioje ir spustelėkite **Open Anyway**.

!!! note "Pastaba"

    Šis žingsnis reikalingas tik jei macOS iš tiesų blokuoja vykdomąjį failą. Paketai, perkelti per SSH ar iš vidinių failų dalijimosi vietų, dažniausiai nėra karantinuojami.

### 3 žingsnis: įdiekite licencijos failą

!!! warning "Svarbu"

    Licencijos failas **ne**įtrauktas į diegimo paketą ir bus pateiktas atskirai iš digna.

1. Suraskite jums pateiktą `license.toml` failą
2. Nukopijuokite jį į pagrindinį digna diegimo katalogą (ten, kur yra `config.toml` ir vykdomasis `digna` failas)

**Kodėl tai svarbu:**
Licencijos faile yra jūsų kliento informacija, licencijos galiojimo data ir skaitmeninis parašas. **Nekoreguokite šio failo** — bet kokie pakeitimai jį sugadins.

**Katalogo struktūra po nustatymo:**

```
/opt/digna/
├── config.toml         (konfigūracijos failas)
├── license.toml        (JŪSŲ LICENCIJOS FAILAS - įdėkite čia)
├── digna               (pagrindinis vykdomasis failas)
├── bin/                (paslaugos valdymo skriptai)
└── dashboard/          (žiniatinklio sąsaja)
    └── (dashboard failai)
```

---

## Backend konfigūracija {: #backend-configuration }

### 1 žingsnis: sukurkite ir redaguokite konfigūracijos failą

Jūsų digna diegimo kataloge yra pateiktas `config_template.toml` failas. Jį tik pervardykite į `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Vieta:** `/opt/digna/config.toml`

Atidarykite `config.toml` tekstų redaktoriumi ir konfigūruokite kiekvieną skyrių žemiau.

#### [app] skyrius

Šis skyrius konfigūruoja dignabackend programos nustatymus:

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
| `digna_APP_HOST` | `localhost` arba IP adresas | Vieta (hostname) arba IP, kur veikia dignabackend |
| `digna_APP_PORT` | `8082` (numatytasis) | REST API galinių taškų prievadas |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendo URL | Jei dashboard yra kitame serveryje, įtraukite jo URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Reikalinga CORS su kredencialais |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Leisti visus HTTP metodus |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Leisti visus antraščių laukus |

!!! note "Pastaba"

    Jei dashboard tiekiamas iš Homebrew nginx numatytuoju prievadu, leistinas origin bus `http://localhost:8080`.

#### [repo] skyrius

Šis skyrius konfigūruoja ryšį su PostgreSQL duomenų baze:

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
| `digna_REPO_USER` | `digna_user` | Vartotojas, sukurtas PostgreSQL nustatyme |
| `digna_REPO_PASSWORD` | Jūsų slaptažodis | Slaptažodis, nustatytas kuriant schemą |

#### [base] skyrius

Šiame skyriuje yra saugumo ir slapukų nustatymai:

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
| `digna_FERNET_KEY` | Šifravimo raktas | Naudojamas tokenams ir slapukams šifruoti (numatytas pateiktas raktas) |
| `digna_COOKIE_DOMAIN` | `localhost` | Sutapti su jūsų frontendo domenu |
| `digna_COOKIE_SECURE` | `false` (lokaliai) / `true` (produkcijoje) | Naudokite `true` HTTPS ryšiams |
| `digna_COOKIE_HTTPONLY` | `true` | Visada įjungta dėl saugumo |
| `digna_COOKIE_SAME_SITE` | `lax` | Apsaugo nuo CSRF atakų |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 val.) | Sesijos galiojimo laikas sekundėmis |
| `digna_MAX_WORKERS` | CPU branduolių skaičius - 1 | Kiek lygiagrečių patikrinimų paleisti |

!!! tip "Patarimas"

    Norėdami sužinoti, kiek CPU branduolių yra jūsų Mac'e, vykdykite `sysctl -n hw.ncpu`.

#### [logging] skyrius

Šis skyrius konfigūruoja žurnalo (logging) elgseną:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` arba `DEBUG` | `INFO` produkcijai, `DEBUG` trikčių šalinimui |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Kiek dienų saugoti žurnalo atsargines kopijas |

---

### 2 žingsnis: inicializuokite repozitoriją

1. Atidarykite **Terminal**
2. Nueikite į digna diegimo katalogą (ten, kur yra `config.toml` ir vykdomasis `digna`)
3. Paleiskite ryšio patikrinimą:

```bash
cd /opt/digna
./digna repo check
```

Turėtumėte matyti patvirtinimą, kad ryšys užmegztas (savęs repozitorija dar nebus inicializuota).

!!! note "Pastaba"

    macOS komandų vykdymas esant esamam katalogui nėra įtrauktas į PATH, todėl vykdomasis failas paleidžiamas kaip `./digna`, o ne `digna`. Jei pageidaujate trumpesnio formato visur, pridėkite diegimo katalogą į PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 3 žingsnis: įdiekite repozitorijos schemą

Tas pačioje direktorijoje vykdykite:

```bash
./digna repo install
```

Ši komanda įdiegs reikiamas lenteles ir schemą jūsų PostgreSQL duomenų bazėje.

### 4 žingsnis: paleiskite digna serverį

digna diegimo kataloge paleiskite serverį:

```bash
./digna serve --address <host> --port <port>
```

**Parametrai:**
- `--address` — serverio hostname/IP
- `--port` — serverio prievadas

Turėtumėte matyti paleidimo žinutes, patvirtinančias, kad serveris veikia:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Patarimas"

    Pirmą kartą paleidžiant serverį, macOS gali paklausti, ar programa gali priimti įeinančius tinklo ryšius. Spustelėkite **Allow**, kitaip dashboard negalės pasiekti backend.

### 5 žingsnis: sukurkite administratoriaus vartotoją

1. Atidarykite **naują** Terminal langą
2. Nueikite į digna diegimo katalogą
3. Vykdykite komandą administratoriaus vartotojui sukurti:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Pavyzdys:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Tai sukurs vartotoją su vardu `admin` ir pilnais administraciniais įgaliojimais.

!!! tip "Patarimas"

    Aptverkite slaptažodį viengubomis kabutėmis arba viengubais apostrofais. `zsh` traktuoja kai kuriuos simbolius, pvz., `!`, `$` ir `*`, specialiai, todėl neaptvertas slaptažodis su tokiais simboliais gali būti perduodamas neteisingai.

!!! tip "Geriausia praktika"

    Naudokite stiprų slaptažodį su didžiosiomis, mažosiomis raidėmis, skaičiais ir specialiais simboliais.

---

## Dashboard konfigūracija {: #dashboard-configuration }

### 1 žingsnis: patalpinkite dashboard į tinklapio serverį

Digna dashboard turi atskirą `config.toml` failą `dashboard/` kataloge. Ši konfigūracija jau pateikta ir pradiniam diegimui keisti jos nereikia. Keiskite tik jei reikia pritaikyti ryšį su backend ar naudoti daugiainstancinį išdėstymą.

Jei reikia pakeisti dashboard konfigūraciją (pvz., daugiaserijiniams diegimams), vadovaukitės dashboard dokumentacija.

Pasirinkite savo tinklapio serverį ir vykdykite atitinkamus diegimo veiksmus.

#### Diegimas į nginx

Jei sekėte [nginx nustatymo](#nginx-setup) skyrių, server blokas jau rodo jūsų `dashboard` katalogą ir kopijuoti failų nereikia.

1. **Patikrinkite kelią**
   - Atidarykite `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Patikrinkite, kad `root` nurodo į jūsų išarchyvuotą `dashboard` katalogą

2. **Užtikrinkite, kad katalogas skaitomas**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Perkraukite nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Patikrinkite diegimą**
   - Atidarykite naršyklę
   - Nueikite į `http://localhost:8080` (arba jūsų sukonfigūruotą URL)
   - Turėtumėte matyti digna dashboard prisijungimo puslapį

#### Diegimas į Apache httpd

1. **Kopijuokite dashboard į dokumentų šaknį**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Pridėkite perrašymo taisykles**

   Sukurkite `.htaccess` failą įdiegtoje aplanke, kad dashboard maršrutai išliktų persikrovus puslapį:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Įklijuokite:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Perkraukite Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Prieiga prie dashboard**
   - Atidarykite naršyklę
   - Nueikite į `http://localhost/digna`
   - Turėtumėte matyti digna dashboard prisijungimo puslapį

---

## digna paleidimas kaip foninė paslauga {: #running-digna-as-a-background-service }

### Kodėl verta paleisti digna kaip paslaugą?

digna backend paleidus kaip foninę paslaugą užtikrina, kad jis:

- Automatiškai paleidžiamas sistemos įkrovos metu
- Veikia fone be atidaryto Terminal lango
- Automatiškai perkraunamas avarijos atveju
- Valdomas per `launchctl`, macOS paslaugų tvarkytuvą

### Paslaugos valdymo failai

Visi reikalingi failai yra digna diegimo kataloge po: `bin/`

Prieinami šie shell skriptai:

- `install_service.sh` — registruoja digna su launchd
- `uninstall_service.sh` — atregistruoja paslaugą
- `start_service.sh` — paleidžia užregistruotą paslaugą
- `stop_service.sh` — sustabdo veikiančią paslaugą

!!! warning "Reikalingas administratoriaus teisių lygis"

    Visi skriptai turi būti vykdomi su `sudo`, nes registruojant paslaugą, kuri paleidžiama įkrovos metu, rašoma į `/Library/LaunchDaemons`.

### Padarykite skriptus vykdomais

Išarchyvavus vykdomasis bitas gali nebūti išsaugotas. Prieš pirmą naudojimą:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Paslaugos įdiegimas

1. **Atidarykite Terminal**

2. **Nueikite į bin katalogą**
   ```bash
   cd /opt/digna/bin
   ```

3. **Paleiskite įdiegimo skriptą**
   ```bash
   sudo ./install_service.sh
   ```

digna serveris dabar užregistruotas su launchd su **automatinio paleidimo** būsena. Paslauga nebus paleista iš karto — žr. kitą skyrių, jei norite ją paleisti.

### Paslaugos paleidimas ir stabdymas

#### Paslaugos paleidimas

1. Atidarykite Terminal
2. Nueikite į `/opt/digna/bin`
3. Vykdykite:
   ```bash
   sudo ./start_service.sh
   ```

#### Paslaugos stabdymas

1. Atidarykite Terminal
2. Nueikite į `/opt/digna/bin`
3. Vykdykite:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Patarimas"

    Visada sustabdykite paslaugą prieš atnaujinant programos failus.

### Paslaugos patikra

Norėdami patvirtinti, ar paslauga užregistruota ir veikia:

```bash
sudo launchctl list | grep digna
```

Eilutė, prasidedanti proceso ID, reiškia, kad paslauga veikia. `-` pirmame stulpelyje reiškia, kad paslauga užregistruota, bet sustabdyta.

### Perkėlimas į naują katalogą

launchd saugo absoliutų kelią iki vykdomojo failo, todėl perkėlimas reikalauja pakartotinio registravimo:

1. **Atregistruokite dabartinę paslaugą**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Perkelkite programos failus**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Įdiekite paslaugą iš naujos vietos**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Paleiskite paslaugą**
   ```bash
   sudo ./start_service.sh
   ```

### Paslaugos pašalinimas

1. **Sustabdykite veikiančią paslaugą**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Pašalinkite paslaugą**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna serveris dabar atregistruotas iš launchd.

---

## Atnaujinimas į naują leidimą {: #upgrading-to-a-new-release }

### Prieš atnaujinimą

**Privaloma sukurti digna repozitorijos atsarginę kopiją**

Prieš atnaujinant digna, sukurkite savo repozitorijos (PostgreSQL) atsarginę kopiją, kad apsaugotumėte duomenis nuo praradimo.
Atsarginė kopija leis atstatyti sistemą, jei atnaujinimo metu kiltų nenumatytų problemų.

Atsarginę kopiją galite sukurti per Terminalą:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Atnaujinimo eiga

#### 1 žingsnis: sustabdykite digna paslaugą

Jei digna veikia kaip foninė paslauga, pirmiausia ją sustabdykite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jei digna paleistas priešakyje (foreground), paspauskite `Ctrl + C` to Terminal lango.

#### 2 žingsnis: sukurkite dabartinio backend atsarginę kopiją

Savo digna diegimo kataloge:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### 3 žingsnis: išarchyvuokite ir išdėstykite naują versiją

1. Išarchyvuokite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į diegimo katalogą
3. Atstatykite vykdomąjį bitą ir, jei reikia, pašalinkite karantino atributą:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Svarbu"

    `config.toml` failas **niekada** neįtrauktas į diegimo ZIP. Jūsų esama konfigūracija lieka saugi.

### 4 žingsnis: atstatykite konfigūracijos failus

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### 5 žingsnis: atnaujinkite repozitorijos schemą

Eikite į digna diegimo katalogą ir vykdykite:

```bash
cd /opt/digna
./digna repo upgrade
```

Tai atnaujins PostgreSQL schemą į naujausią versiją, išsaugant visus esamus duomenis.

### 6 žingsnis: perkraukite paslaugas

Jei naudojate foninę paslaugą:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Jei paleidžiate rankiniu būdu, paleiskite serverį:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Jei naudojate nginx arba Apache, perkraukite atitinkamą tinklapio serverį:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### 7 žingsnis: patikrinkite atnaujinimą

1. Atidarykite digna dashboard
2. Patikrinkite, ar sąsaja užsikrauna teisingai
3. Peržiūrėkite serverio žurnalus dėl klaidų