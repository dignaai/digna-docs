---
title: macOS diegimo vadovas – digna leidimas 2026.11 | digna dokumentacija
description: Žingsnis po žingsnio gidas, kaip įdiegti digna leidimą 2026.11 macOS — sistemos reikalavimai, Homebrew ir PostgreSQL nustatymas, nginx arba Apache konfigūracija, backend ir dashboard konfigūracija, digna paleidimas kaip foninė paslauga ir atnaujinimas iš Release 2026.06.
keywords: digna macos diegimas, digna mac diegimo gidas, digna backend nustatymas, digna dashboard diegimas, postgresql homebrew, nginx macos, digna launchd paslauga, digna atnaujinimo gidas
image: /assets/logo_square.png
---

# macOS diegimo vadovas digna leidimui 2026.11

**Leidimas:** 2026.11

**Paskutinį kartą atnaujinta:** 2026 m. lapkričio 7 d.


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

- **digna**: programos branduolys, atsakingas už duomenų apdorojimą ir kokybės patikras. Jis sujungia užkulisinę dalį ir komandinęs eilutės sąsają į vieną vykdomąjį failą ir pakeičia atskiras ankstesnių leidimų programas `dignabackend` ir `dignacli`.
- **dignadashboard**: internetinė sąsaja, talpinama tinklapio serveryje, leidžianti vartotojams patogiai sąveikauti su digna platforma ir vizualizuoti duomenų kokybės metrikas.

### Kas naujo leidime 2026.11

Šis leidimas prideda digna Data Reconciliation, digna Agentic su digna MCP Server ir digna Engine, kuris gali profiliuoti duomenis pačioje digna ir tikrinti nuorodų vientisumą tarp skirtingų duomenų bazių technologijų. Išsamią informaciją rasite [leidimo pastabose](../../../changelog/Release_202611.md).

Diegimui leidimas atneša naują saugyklos migracijų mechanizmą, neprivalomą `[duckdb]` skyrių faile `config.toml`, skirtą digna Engine, ir naują licencijos failą. Kiekvieną iš jų aptaria [atnaujinimo skyrius](#upgrading-to-a-new-release).

### Ieškote Windows arba Linux diegimo instrukcijų?

Šis vadovas skirtas macOS. Kitiems platformoms žr. [Windows diegimo vadovą](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) arba [Linux diegimo vadovą](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Duomenų bazės ryšiai, kurių profiliavimo vieta yra digna Engine, profiliuojami pačiame digna
    pagrindiniame kompiuteryje. Numatykite jiems papildomos atminties ir disko vietos, žr.
    [\[duckdb\] skyrių](#duckdb-section).

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

!!! info "Konfigūracijos ir licencijos failų pakete nėra"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` diegimo pakete nepateikiami — abu
    failus sukuriate patys, skyriuose [Backend konfigūracija](#backend-configuration) ir
    [Dashboard konfigūracija](#dashboard-configuration). `license.toml` taip pat nepateikiamas;
    digna jį pateikia atskirai, kaip aprašyta 3 žingsnyje.

Norint išarchyvuoti per Terminalą:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
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

Šis skyrius konfigūruoja kryžminės kilmės išteklių bendrinimą (CORS) tarp dashboard ir backend:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboard URL adresai | URL adresai, iš kurių pateikiamas dashboard. Naršyklės užklausos iš bet kurios kitos kilmės atmetamos |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Būtina, kad naršyklė su kiekviena užklausa siųstų sesijos slapuką |

!!! note "Pastaba"

    Jei dashboard tiekiamas iš Homebrew nginx numatytuoju prievadu, leistinas origin bus `http://localhost:8080`.

!!! info "[app] skyrius yra neprivalomas"

    Nuo Release 2026.11 abu raktus ir visą `[app]` skyrių galima praleisti. Tai tinkama sąranka, kai
    atvirkštinis tarpinis serveris (reverse proxy) pateikia dashboard ir backend su ta pačia kilme
    (origin): tada naršyklė nesiunčia kryžminės kilmės užklausų, o pagal numatytuosius nustatymus nė
    viena neleidžiama.

#### [repo] skyrius

Šis skyrius konfigūruoja ryšį su PostgreSQL duomenų baze:

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
| `DIGNA_REPO_USER` | `digna_user` | Vartotojas, sukurtas PostgreSQL nustatyme |
| `DIGNA_REPO_PASSWORD` | Jūsų slaptažodis | Slaptažodis, nustatytas kuriant schemą |
| `DIGNA_REPO_SSLMODE` | `prefer` (numatytasis) | Neprivaloma. PostgreSQL SSL režimas: `disable`, `allow`, `prefer`, `require`, `verify-ca` arba `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (numatytasis) | Neprivaloma. Kiek ryšių su saugykla digna laiko atvirų |

#### [base] skyrius

Šiame skyriuje yra saugumo, slapukų ir inspekcijų nustatymai:

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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 val.) | Sesijos galiojimo laikas sekundėmis |
| `DIGNA_MAX_WORKERS` | CPU branduolių skaičius - 1 | Kiek inspekcijų gali vykti vienu metu |
| `DIGNA_FRONTEND_BASEURL` | Dashboard URL | Privaloma. Naudojamas nuorodoms pranešimuose, todėl tai turi būti URL, kurį gavėjai gali atidaryti |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (numatytasis) | Neprivaloma. Kiek sekundžių viena užklausa į šaltinio duomenų bazę gali vykti, kol bus nutraukta; `0` išjungia skirtąjį laiką |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (numatytasis) | Neprivaloma. Kiek sekundžių laukti prisijungimo prie šaltinio duomenų bazės; `0` laukia neribotai |

!!! tip "Patarimas"

    Norėdami sužinoti, kiek CPU branduolių yra jūsų Mac'e, vykdykite `sysctl -n hw.ncpu`.

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

#### [logging] skyrius

Šis skyrius konfigūruoja žurnalo (logging) elgseną:

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

#### [duckdb] skyrius (neprivalomas) {: #duckdb-section }

Naujiena nuo Release 2026.11. Šis skyrius nustato **digna Engine** išteklius. digna Engine
profiliuoja duomenis pačioje digna tiems duomenų bazės ryšiams, kurių profiliavimo vieta yra
**digna Engine**, ir vykdo nuorodų vientisumo patikras tarp duomenų šaltinių, esančių skirtinguose
duomenų bazės ryšiuose. Žr. [Profiliavimo vieta](../../../platform/profiling/profiling_location.md).

Skyrius yra neprivalomas. Be jo taikomos toliau nurodytos numatytosios reikšmės.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (numatytasis) | Atmintis MB, kurią gali naudoti vienas digna Engine vykdymas. Vienu metu gali būti aktyvūs iki `DIGNA_MAX_WORKERS` vykdymų |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Numatytoji: sistemos laikinasis katalogas (digna paleidžiančios paskyros `$TMPDIR`) | Laikinųjų failų katalogas, kai duomenys netelpa į atmintį |

!!! tip "digna Engine išteklių planavimas"

    digna pagrindiniame kompiuteryje, be atminties, kurią naudoja pati digna, numatykite iki
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` atminties, o laikinajame kataloge –
    pakankamai laisvos disko vietos, kad tilptų didžiausios tikrinamos datos duomenys iš duomenų
    šaltinių, naudojančių digna Engine. Nukreipkite `DIGNA_DUCKDB_TEMP_DIRECTORY` į diską su tokia
    vieta, į kurį gali rašyti digna paleidžianti paskyra:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Šio skyriaus reikia tik tada, jei bent vienas duomenų bazės ryšys naudoja digna Engine arba
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

### 3 žingsnis: inicializuokite repozitoriją

1. Atidarykite **Terminal**
2. Nueikite į digna diegimo katalogą (ten, kur yra `config.toml` ir vykdomasis `digna`)
3. Paleiskite ryšio patikrinimą:

```bash
cd /opt/digna
./digna repo check
```

Naujoje schemoje komanda prisijungia ir tada praneša, kad saugykla dar neįdiegta:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Šiame etape tai yra laukiamas rezultatas: jis patvirtina, kad digna pasiekia PostgreSQL ir schemą. Prisijungimo ar autentifikavimo klaida, priešingai, rodo į `[repo]` skyrių arba PostgreSQL sąranką.

!!! note "Pastaba"

    macOS komandų vykdymas esant esamam katalogui nėra įtrauktas į PATH, todėl vykdomasis failas paleidžiamas kaip `./digna`, o ne `digna`. Jei pageidaujate trumpesnio formato visur, pridėkite diegimo katalogą į PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### 4 žingsnis: įdiekite repozitorijos schemą

Tas pačioje direktorijoje vykdykite:

```bash
./digna repo upgrade
```

Ši komanda įdiegia reikalingas lenteles saugyklos schemoje ir baigiasi pranešimu:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade įdiegia ir atnaujina"

    Nuo Release 2026.11 `repo upgrade` įdiegia naują saugyklą ir atnaujina esamą.
    `repo install` vis dar veikia kaip kitas tos pačios komandos pavadinimas.

### 5 žingsnis: sukurkite administratoriaus vartotoją

1. Atidarykite **naują** Terminal langą
2. Nueikite į digna diegimo katalogą
3. Vykdykite komandą administratoriaus vartotojui sukurti:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Pavyzdys:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Taip sukuriamas naudotojas su el. pašto adresu `admin@example.com` ir visomis administratoriaus teisėmis.

!!! tip "Patarimas"

    Aptverkite slaptažodį viengubomis kabutėmis arba viengubais apostrofais. `zsh` traktuoja kai kuriuos simbolius, pvz., `!`, `$` ir `*`, specialiai, todėl neaptvertas slaptažodis su tokiais simboliais gali būti perduodamas neteisingai.

!!! tip "Geriausia praktika"

    Naudokite stiprų slaptažodį su didžiosiomis, mažosiomis raidėmis, skaičiais ir specialiais simboliais.

---

### 6 žingsnis: paleiskite digna serverį

digna diegimo kataloge paleiskite serverį:

```bash
./digna serve --address <host> --port <port>
```

**Parametrai:**
- `--address` — serverio hostname/IP (numatytasis `127.0.0.1`)
- `--port` — serverio prievadas (numatytasis `8000`)

Kai serveris pasileidžia, jis išveda adresą, kuriuo klausosi:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Patarimas"

    Pirmą kartą paleidžiant serverį, macOS gali paklausti, ar programa gali priimti įeinančius tinklo ryšius. Spustelėkite **Allow**, kitaip dashboard negalės pasiekti backend.

!!! note "Serveris užima terminalą"

    `serve` veikia priekiniame plane ir tęsiasi, kol jį sustabdysite ++ctrl+c++. Palikite jį veikti, kol užbaigsite sąranką; kad jis būtų paleidžiamas automatiškai paleidus sistemą, žiūrėkite [digna paleidimas kaip foninės tarnybos](#running-digna-as-a-background-service).

## Dashboard konfigūracija {: #dashboard-configuration }

### 1 žingsnis: patalpinkite dashboard į tinklapio serverį

digna dashboard savo konfigūraciją skaito iš `dashboard/dashboard_config.toml`. Šis failas diegimo pakete nepateikiamas — jį sukuriate `dashboard/` kataloge šalia dashboard failų.

Jo turinys aprašytas skyriuje [Vienkartinis prisijungimas (SSO)](../../../sso/overview.md), kur šis failas ir reikalingas: jame nurodomos dashboard siūlomos prisijungimo parinktys, o daugiainstanciniams diegimams — ir ryšys su backend.

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

Šiame skyriuje aprašoma, kaip atnaujinti Release 2026.06 diegimą į Release 2026.11. Jei jūsų
diegimas senesnis, pirmiausia perskaitykite [Atnaujinimas iš senesnio nei 2026.06 leidimo](#upgrading-from-a-release-before-2026-06).

### Prieš atnaujinimą

**Privaloma sukurti digna repozitorijos atsarginę kopiją**

Prieš atnaujinant digna, sukurkite savo repozitorijos (PostgreSQL) atsarginę kopiją, kad apsaugotumėte duomenis nuo praradimo.
Atsarginė kopija leis atstatyti sistemą, jei atnaujinimo metu kiltų nenumatytų problemų.

Atsarginę kopiją galite sukurti per Terminalą:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Release 2026.11 licencijos failo užsakymas**

Release 2026.11 reikia naujo `license.toml`. Prieš pradėdami paprašykite jo digna komandos ir
turėkite jį paruoštą [7 žingsniui](#step-7-replace-the-license-file).

### Atnaujinimas iš senesnio nei 2026.06 leidimo {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 atnešė tris pakeitimus, kurie vis dar galioja, kai senesnį diegimą atnaujinate
tiesiai į 2026.11:

- **Tik ODBC.** digna kiekvieną šaltinio technologiją pasiekia per ODBC. Kiekvieną duomenų bazės
  ryšį, kuris dar nenaudoja ODBC, po atnaujinimo reikia perkelti į ODBC; automatinio konvertavimo
  nėra. Iš anksto įdiekite ODBC tvarkykles digna pagrindiniame kompiuteryje, žr.
  [ODBC tvarkyklės diegimas digna pagrindiniame kompiuteryje](../../../databases/overview.md#install-the-driver),
  ir turėkite paruoštas kiekvieno ryšio savybes iš
  [technologijų vadovų](../../../databases/overview.md#technology-guides). Databricks Legacy
  jungties nebėra; perkelkite tuos ryšius į
  [Databricks](../../../databases/databricks_connector_guide.md) jungtį.
- **Vienas vykdomasis failas.** `dignabackend` ir `dignacli` pakeisti vienu vykdomuoju failu
  `digna`, kuris sujungia backend ir CLI.
- **config.toml.** `[encryption]` skyrius yra privalomas, o `DIGNA_APP_HOST` ir `DIGNA_APP_PORT`
  nebeskaitomi: adresą ir prievadą serveris gauna iš `digna serve`. Palyginkite savo failą su
  skyriumi [Backend konfigūracija](#backend-configuration).

Toliau pateiktuose žingsniuose nurodyta, kur senesniam diegimui reikia ko nors kito. Saugyklos
atnaujinimas 8 žingsnyje bet kurio ankstesnio leidimo saugyklą perkelia tiesiai į 2026.11.

### Atnaujinimo eiga

#### 1 žingsnis: sustabdykite digna paslaugą {: #step-1-stop-the-digna-service }

Jei digna veikia kaip foninė paslauga, pirmiausia ją sustabdykite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jei digna paleistas priešakyje (foreground), paspauskite ++ctrl+c++ to Terminal lango.

#### 2 žingsnis: Sukurkite dabartinio diegimo atsarginę kopiją {: #step-2-backup-current-installation }

Savo digna diegimo kataloge pervadinkite dabartinio diegimo vykdomąjį failą ir `dashboard` aplanką,
kad naują leidimą būtų galima įdiegti šalia jų:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

`digna_old` laikykite, kol patikrinsite atnaujinimą, o `dashboard_old` – kol iš jo atkursite savo
konfigūracijos failus (žr. 4 žingsnį). Po to abu galite ištrinti.

!!! info "Atnaujinimas iš senesnio nei 2026.06 leidimo"

    Vietoj vykdomojo failo pervadinkite aplankus `dignabackend` ir `dignacli`:
    `mv dignabackend dignabackend_old` ir `mv dignacli dignacli_old`. Release 2026.11 nė vieno iš jų nenaudoja.

#### 3 žingsnis: išarchyvuokite ir išdėstykite naują versiją {: #step-3-extract-and-deploy-new-version }

1. Išarchyvuokite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į diegimo katalogą
3. Atstatykite vykdomąjį bitą ir, jei reikia, pašalinkite karantino atributą:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Svarbu"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` niekada nėra įtraukti į
    diegimo ZIP — digna komanda niekada nepateikia nė vieno iš šių failų. Todėl atnaujinimas jūsų
    esamos konfigūracijos nepaliečia, o kopijos pervadintuose `*_old` aplankuose yra
    vienintelės, kurias turite.

#### 4 žingsnis: atstatykite konfigūracijos failus {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

#### 5 žingsnis: perkraukite tinklapio serverį {: #step-5-reload-the-web-server }

Dashboard yra statinių failų rinkinys, todėl jūsų tinklapio serveris — ir naršyklė — gali vis dar
pateikti ankstesnę versiją. Perkraukite arba iš naujo paleiskite tinklapio serverį, kuriame talpinamas `dashboard`
aplankas, tada iš naujo įkelkite puslapį priverstiniu atnaujinimu (++cmd+shift+r++).

#### 6 žingsnis: Patikrinkite konfigūraciją {: #step-6-validate-the-configuration }

Prieš liesdami saugyklą įsitikinkite, kad `config.toml` yra išsamus:

```bash
./digna config check
```

Kiekvienas skyrius turi pranešti OK. Pataisykite viską, kas pranešama kaip FAILED, pašalinkite
raktus, išvardytus ties **Unknown keys**, ir prieš tęsdami paleiskite komandą dar kartą.

#### 7 žingsnis: pakeiskite licencijos failą {: #step-7-replace-the-license-file }

Licencijos failas paprastai pereina iš vieno leidimo į kitą. Release 2026.11 yra išimtis: jis
prideda du licencijuojamus modulius, digna Data Reconciliation ir digna Agentic, o licencijoje,
išduotoje iki 2026.11, jų nėra. Nukopijuokite `license.toml`, kurį digna komanda pateikė
Release 2026.11, į diegimo katalogą, pakeisdami senąjį:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nepalikite ankstesnės licencijos"

    Su ankstesne licencija digna vis tiek pasileidžia, tačiau digna Data Reconciliation ir
    digna MCP Server lieka išjungti. Kiekviena komanda, tikrinanti licenciją — `user`,
    `inspection`, `repo` — nepavykus patikrinimui nutraukiama dar prieš paliečiant saugyklą. Prieš
    tęsdami patikrinkite naująją licenciją:

    ```bash
    ./digna license check
    ```

#### 8 žingsnis: atnaujinkite repozitorijos schemą {: #step-8-upgrade-the-repository-schema }

Savo digna diegimo kataloge paleiskite:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 saugyklos schemą valdo versijuotomis migracijomis. Pirmasis atnaujinimas iš
ankstesnio leidimo perkelia schemą į paskutinę ankstesnės versijavimo schemos versiją, užfiksuoja ją
kaip pradinį tašką ir tada pritaiko Release 2026.11 migracijas. Jis baigiasi pranešimu:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Visi esami duomenys išsaugomi. Norėdami bet kada pamatyti saugyklos būseną, paleiskite
`./digna repo check`: komanda išvardija paskutinę pritaikytą migraciją ir visas laukiančias.

!!! warning "digna nepasileidžia su pasenusia saugykla"

    Nuo Release 2026.11 serveris atsisako pasileisti, kol saugyklą reikia atnaujinti, ir apie tai
    praneša, pavyzdžiui:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Prieš paleisdami serverį ar paslaugą, paleiskite `repo upgrade`.

#### 9 žingsnis: perkraukite paslaugas {: #step-9-restart-services }

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

#### 10 žingsnis: patikrinkite atnaujinimą {: #step-10-verify-the-upgrade }

1. Patikrinkite naujojo vykdomojo failo leidimą:

    ```bash
    ./digna version
    ```

    Pirmoji eilutė turi būti `Release: 2026.11`.

2. Atidarykite digna dashboard ir patikrinkite, ar sąsaja įkeliama teisingai.
3. Patikrinkite serverio išvestį ir `logs` katalogo failus, ar nėra klaidų.
4. Išbandykite savo duomenų bazės ryšius — žr.
   [Ryšio tikrinimas](../../../databases/overview.md#testing-a-connection). Po atnaujinimo iš
   senesnio nei 2026.06 leidimo pirmiausia perkelkite į ODBC kiekvieną ryšį, kuris dar nenaudojo ODBC.

Norėdami pradėti dirbti su naujais moduliais, žr. [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI agento prijungimas](../../../platform/agentic/connect_ai_agent.md) – apie digna MCP Server, ir
[Profiliavimo vieta](../../../platform/profiling/profiling_location.md) – apie digna Engine.
