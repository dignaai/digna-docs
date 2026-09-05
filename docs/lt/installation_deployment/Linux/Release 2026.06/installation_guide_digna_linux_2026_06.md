---
title: Linux diegimo vadovas – digna leidimas 2026.06 | digna dokumentacija
description: Žingsnis po žingsnio vadovas, kaip įdiegti digna leidimą 2026.06 Linux — sistemos reikalavimai, PostgreSQL nustatymas, nginx arba Apache konfigūracija, backend ir dashboard konfigūracija, digna paleidimas kaip systemd paslauga ir atnaujinimas į naują leidimą.
keywords: digna linux diegimas, digna diegimo vadovas, digna backend nustatymas, digna dashboard diegimas, postgresql linux, nginx linux, digna systemd paslauga, digna atnaujinimo vadovas
image: /assets/logo_square.png
---

# Linux diegimo vadovas digna leidimui 2026.06

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
9. [digna paleidimas kaip systemd paslauga](#running-digna-as-a-systemd-service)
10. [Atnaujinimas į naują leidimą](#upgrading-to-a-new-release)

---

## Įvadas {: #introduction }

### Apie digna

digna yra visapusiška, dirbtiniu intelektu paremta platforma, skirta optimizuoti duomenų kokybės valdymą įvairiose duomenų aplinkose, tokiose kaip duomenų sandėliai, ežerai ir lakehouse sprendimai. Sukurta būti itin mastelijama ir pritaikoma, digna sprendžia šiuolaikines duomenų problemas per automatizavimą, realaus laiko stebėjimą ir anomalijų aptikimą.

digna susideda iš dviejų pagrindinių komponentų:

- **dignabackend**: programos branduolinis variklis, atsakingas už duomenų apdorojimą ir kokybės patikras.
- **dignadashboard**: web sąsaja, talpinama tinklapio serveryje, suteikianti patogią prieigą prie digna platformos ir duomenų kokybės metrikų vizualizacijos.

### Kas naujo leidime 2026.06

Šis leidimas įtraukia duomenų stebėjimo galimybes tiesiai į jūsų kodą, leidžiant kūrėjams stebėti duomenų kokybę ties šaltiniu. Išsamią informaciją rasite [išleidimo pastabose](http://docs.digna.ai/changelog/Release_202606/).

### Ieškote Windows arba macOS instrukcijų?

Šis vadovas apima Linux. Kitiems platformoms žiūrėkite [Windows diegimo vadovą](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) arba [macOS diegimo vadovą](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Kurioms distribucijoms skirtas šis vadovas?

Instrukcijos parašytos dviem dažniausiai naudojamoms serverinių šeimoms. Kur jos skiriasi, pateikiami abu komandų variantai:

- **Debian šeima** — Debian, Ubuntu. Paketų tvarkyklė: `apt`.
- **RHEL šeima** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Paketų tvarkyklė: `dnf`.

Bet kuri moderni distribucija su `systemd` tiks; keičiasi tik paketų pavadinimai ir keli konfigūracijos keliai.

---

## Sistemos reikalavimai {: #system-requirements }

Prieš pradėdami diegimą, įsitikinkite, kad jūsų sistema atitinka šiuos minimalus reikalavimus:

| Reikalavimas | Specifikacija |
|---|---|
| **Operacinė sistema** | Ubuntu 22.04 LTS arba naujesnė, Debian 12 arba naujesnė, RHEL 9 / Rocky 9 / AlmaLinux 9 arba naujesnė |
| **Architektūra** | x86_64 (amd64) arba arm64 |
| **Init sistema** | systemd |
| **Atmintis (minimalus diegimas)** | 16 GB RAM |
| **Disko vieta** | 10 GB laisvos vietos |
| **Duomenų bazė** | PostgreSQL Server 12 arba naujesnė |
| **Tinklapio serveris** | nginx, Apache httpd arba panašus |

### Duomenų bazės diegimo parinktys

**Jei PostgreSQL jau įdiegta:**
Galite pridėti naują duomenų bazę digna prie esamo PostgreSQL serverio.

**Jei diegiate PostgreSQL tame pačiame kompiuteryje kaip digna:**

!!! info "Rekomenduojamos specifikacijos"

    - **Atmintis**: 32 GB RAM (vietoje 16 GB)
    - **Disko vieta**: 50 GB laisvos vietos (vietoje 10 GB)

    Šios didesnės specifikacijos užtikrina, kad tiek digna, tiek PostgreSQL veiktų vienu metu.

### Kaip patikrinti distribuciją ir architektūrą

Kelios šio vadovo komandos skiriasi tarp Debian ir RHEL šeimų. Norėdami patikrinti, kuriai priklausote, vykdykite:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` arba `ID=debian` — naudokite `apt` komandas.
- `ID=rhel`, `rocky`, `almalinux` arba `fedora` — naudokite `dnf` komandas.
- `x86_64` arba `aarch64` — tai diegimo paketo architektūra, kurios jums reikia.

---

## Prieš diegiant {: #pre-installation-setup }

Prieš diegdami digna, įsitikinkite, kad įvykdyti du pagrindiniai reikalavimai:

1. **PostgreSQL serveris** – saugoti apskaičiuotas metrikas ir našumo duomenis
2. **Tinklapio serveris** – talpinti digna Dashboard

Jei šie komponentai dar nėra sukonfigūruoti, vadovaukitės žemiau pateiktomis sekcijomis, kad juos įdiegtumėte ir sukonfigūruotumėte.

### Atnaujinti paketų indeksą

Atnaujinkite paketų sąrašą prieš diegimą:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Pastaba"

    Visame šitame vadove pirmoji komanda poroje skirta **Debian šeimai**, o antroji — **RHEL šeimai**. Vykdykite tik tą komandą, kuri atitinka jūsų sistemą.

---

## PostgreSQL serverio nustatymas {: #postgresql-server-setup }

### Jei PostgreSQL jau yra

Jei PostgreSQL jau įdiegta ir veikia jūsų vietiniame kompiuteryje arba naudojate valdomą nuotolinį PostgreSQL serverį, galite pereiti prie [kitos skilties](#web-server-configuration).

### PostgreSQL diegimas

#### 1 žingsnis: įdiekite serverio paketą

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Patarimas"

    Distribucijų paketai gali atsilikti nuo naujausių PostgreSQL leidimų. Jei reikia konkrečios naujesnės versijos, naudokite oficialų [PostgreSQL apt arba yum saugyklą](https://www.postgresql.org/download/linux/).

#### 2 žingsnis: inicializuokite duomenų klasterį

Debian šeimoje paketas sukuria ir paleidžia klasterį automatiškai — pereikite prie kito žingsnio.

RHEL šeimoje klasteris turi būti sukurtas eksplicitiai:

```bash
sudo postgresql-setup --initdb
```

#### 3 žingsnis: paleiskite ir įgalinkite paslaugą

```bash
sudo systemctl enable --now postgresql
```

Tai paleidžia PostgreSQL iš karto ir sukonfigūruoja, kad jis būtų paleidžiamas automatiškai įkrovos metu.

#### 4 žingsnis: patikrinkite įdiegimą

```bash
psql --version
sudo systemctl status postgresql
```

Turėtumėte matyti PostgreSQL versiją ir `active (running)` būsenos paslaugą.

#### 5 žingsnis: prisijunkite prie serverio

Linux PostgreSQL paketas sukuria `postgres` sistemos paskyrą, kuri valdo klasterį. Prisijunkite per ją:

```bash
sudo -u postgres psql
```

!!! note "Pastaba — Linux čia skiriasi nuo Windows"

    Windows diegimo programa leidžia nustatyti slaptažodį `postgres` supervartotojui diegimo metu. Linux paketai to nedaro. Vietiniai ryšiai autentifikuojami per **peer authentication**: operacinės sistemos vartotojas `postgres` gali prisijungti kaip duomenų bazės vartotojas `postgres` be slaptažodžio.

    Todėl aukščiau pateikta komanda naudoja `sudo -u postgres`. digna backend jungiasi per TCP su naudotojo vardu ir slaptažodžiu, todėl jūs sukursite aiškų digna vartotoją [Pradiniame diegime](#initial-installation).

#### 6 žingsnis: patikrinkite prievadą

Numatytasis PostgreSQL prievadas yra `5432`. Norėdami patikrinti, kokį prievadą serveris naudoja:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Užsirašykite reikšmę — jos prireiks konfigūruojant digna backend.

#### 7 žingsnis: įgalinkite slaptažodžio autentifikavimą digna vartotojui

digna jungiasi prie PostgreSQL per TCP kaip `digna_user`, todėl reikalingas slaptažodinis autentifikavimas, o ne peer autentifikacija. Patikrinkite, ar jūsų `pg_hba.conf` tai leidžia.

Raskite failą:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Atidarykite jį redaktoriuje ir įsitikinkite, kad vietiniai TCP įrašai naudoja `scram-sha-256` (arba `md5` senesniuose serveriuose), o ne `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Persikraukite PostgreSQL po bet kokio pakeitimo:

```bash
sudo systemctl reload postgresql
```

!!! warning "Svarbu"

    Jei digna praneša apie `FATAL: Ident authentication failed for user "digna_user"`, tai būtent šios nustatymo pasekmė.

#### 8 žingsnis: jei PostgreSQL veikia kitoje mašinoje

Norėdami priimti jungtis iš kito hosto, nustatykite `listen_addresses` faile `postgresql.conf` ir pridėkite atitinkamą `host` eilutę savo tinkle `pg_hba.conf`:

```
listen_addresses = '*'
```

Tada atverkite prievadą ugniasienėje ir paleiskite paslaugą iš naujo:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Tinklapio serverio konfigūracija {: #web-server-configuration }

digna reikalauja tinklapio serverio dashboard talpinimui. Pasirinkite vieną iš šių variantų:

- [nginx](#nginx-setup) — lengvas ir rekomenduojamas
- [Apache httpd](#apache-setup) — plačiai naudojama alternatyva

Jums reikės įdiegti ir sukonfigūruoti tik **vieną** iš šių serverių.

Abu skyriai konfigūruoja dvi dashboard reikalaujamas parinktis:

- **Single-page-application fallback**, kad perkrovus dashboard URL negrąžintų 404
- **.md MIME tipą**, kad Markdown failai būtų teisingai pateikiami

### nginx diegimas {: #nginx-setup }

#### Apžvalga

nginx yra lengvas, aukštos veiklos tinklapio serveris, tinkamas talpinti statinį digna dashboard.

#### Diegimas

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx paleidimas

```bash
sudo systemctl enable --now nginx
```

#### Patikrinkite įdiegimą

1. Atidarykite naršyklę
2. Eikite į `http://localhost`
3. Turėtumėte matyti nginx pasveikinimo puslapį

#### Ugniasienės atvėrimas

Jei į serverį jungiamasi iš kitų mašinų, leiskite HTTP srautą:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Svetainės konfigūravimas dashboard

nginx įtraukia kiekvieną failą iš `conf.d` katalogo abiejose distribucijų šeimose. Sukurkite atskirą konfigūracijos failą digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Įklijuokite žemiau pateiktą, pakeisdami `/opt/digna/dashboard` tikru keliu į jūsų išarchyvuotą `dashboard` katalogą:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

    Be `try_files` direktyvos, perkrovus bet kurį dashboard puslapį, išskyrus pagrindinį URL, gausite 404. Tai nginx analogas URL Rewrite modulio, reikalingo IIS Windows aplinkoje.

#### Išjunkite numatytąją svetainę

Tik vienas server blokas gali būti `default_server` prievadui. Debian šeimoje pašalinkite paketais įdiegtą numatytąją svetainę, kad nekiltų konfliktų:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

RHEL šeimoje komentarais arba ištrynimu ištrinkite `server { ... }` bloką faile `/etc/nginx/nginx.conf`.

#### Pritaikykite konfigūraciją

Patikrinkite konfigūraciją sintaksės klaidų atžvilgiu, tada perkraukite nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd diegimas {: #apache-setup }

#### Apžvalga

Apache httpd yra prieinamas numatytųjų saugyklų kiekvienoje palaikomoje distribucijoje. Paketo pavadinimas Debian šeimoje yra `apache2`, o RHEL šeimoje — `httpd`.

#### Diegimas

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache paleidimas

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Patikrinkite įdiegimą

1. Atidarykite naršyklę
2. Eikite į `http://localhost`
3. Turėtumėte matyti distribucijos numatytą Apache puslapį

#### Būtina: įjungti mod_rewrite

Dashboard reikalauja URL perrašymo.

Debian šeimoje įgalinkite modulį ir perkraukite:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

RHEL šeimoje `mod_rewrite` yra įkeltas pagal nutylėjimą. Patikrinkite:

```bash
httpd -M | grep rewrite
```

#### Būtina: leisti .htaccess perrašymus

Atidarykite dokumentų šaknies konfigūracijos failą:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Raskite `<Directory>` bloką, apimantį jūsų dokumentų šaknį (`/var/www/html` abiejose šeimose) ir pakeiskite:

```apache
AllowOverride None
```

į:

```apache
AllowOverride All
```

#### Būtina: MIME tipas Markdown failams

Toje pačioje byloje pridėkite šią eilutę, kad Markdown failai būtų pateikiami teisingai:

```apache
AddType text/markdown .md
```

!!! warning "Svarbu"

    Be šio nustatymo `.md` failai gali būti neteisingai aptarnauti.

#### Pritaikykite konfigūraciją

Patikrinkite konfigūraciją sintaksės klaidų atžvilgiu, tada perkraukite Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Pradinis diegimas {: #initial-installation }

### 1 žingsnis: sukurkite digna saugyklą

digna saugykla saugo visus digna apskaičiuotus rodiklius. Ji veikia kaip centrinė analitinių ir našumo duomenų duomenų bazė.

#### Sukurkite saugyklos schemą ir vartotoją

Atidarykite PostgreSQL klientą (psql, pgAdmin ar panašiai) ir vykdykite šias SQL komandas:

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

Norėdami vykdyti tai iš shell vienu žingsniu:

```bash
sudo -u postgres psql
```

Tada įklijuokite sakinius prie `postgres=#` prompto ir įveskite `\q`, kad išeitumėte.

!!! tip "Geriausia praktika"

    Naudokite stiprius, sudėtingus slaptažodžius duomenų bazės vartotojams. Venkite lengvai atspėjamų kredencialų.

---

### 2 žingsnis: išarchyvuokite digna diegimo paketą

1. Suraskite jums pateiktą digna diegimo ZIP failą
2. Išarchyvuokite jį į pageidaujamą diegimo vietą — pavyzdžiui `/opt/digna`
3. Po išarchyvavimo turėtumėte pamatyti šiuos elementus:
   - `dashboard/` — web dashboard sąsaja
   - `digna` — pagrindinis vykdomasis failas (backend + CLI kartu)
   - `config.toml` — konfigūracijos failas
   - `license.toml` — licencijos failas (įdėkite savo kopiją čia)

Išarchyvavimui iš shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Pastaba"

    Jei `unzip` nėra įdiegtas, pridėkite jį su `sudo apt install -y unzip` arba `sudo dnf install -y unzip`.

#### Paverskite vykdomąjį failą paleidžiamu

Priklausomai nuo to, kaip archyvas buvo perkeltas, vykdomasis bitas gali nebūti išsaugotas. Nustatykite jį aiškiai:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Sukurkite paslaugos paskyrą

Rekomenduojama backend paleisti kaip dedikuotą neprivilegijuotą vartotoją gamybos aplinkoje:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Pastaba"

    RHEL šeimoje ekvivalentinis šliuzas yra `/sbin/nologin`.

### 3 žingsnis: įdiekite licencijos failą

!!! warning "Svarbu"

    Licencijos failas **nėra** įtrauktas į diegimo paketą ir bus pateiktas atskirai iš digna.

1. Suraskite jums pateiktą `license.toml` failą
2. Nukopijuokite jį į pagrindinį digna diegimo katalogą (ten, kur yra `config.toml` ir vykdomasis failas `digna`)

**Kodėl tai svarbu:**
Licencijos failas talpina jūsų kliento informaciją, licencijos galiojimo datą ir skaitmeninį parašą. **Nekeiskite šio failo** — bet koks pakeitimas jį invaliduoja.

**Katalogo struktūra po nustatymo:**

```
/opt/digna/
├── config.toml         (konfigūracijos failas)
├── license.toml        (JŪSŲ LICENCIJOS FAILAS - nukopijuokite čia)
├── digna               (pagrindinis vykdomasis failas)
├── bin/                (paslaugos valdymo skriptai)
└── dashboard/          (web sąsaja)
    └── (dashboard failai)
```

---

## Backend konfigūracija {: #backend-configuration }

### 1 žingsnis: sukurkite ir redaguokite konfigūracijos failą

`config_template.toml` failas pateiktas jūsų digna diegimo kataloge. Jums tereikia pervardyti jį į `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Vieta:** `/opt/digna/config.toml`

Atidarykite `config.toml` teksto redaktoriuje ir sukonfigūruokite kiekvieną žemiau pateiktą skyrių.

#### [app] skyrius

Šis skyrius konfigūruoja digna backend programos nustatymus:

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
| `digna_APP_HOST` | `localhost` arba IP adresas | Host vardas arba IP, kuriame talpinamas dignabackend |
| `digna_APP_PORT` | `8082` (numatytasis) | REST API galinių taškų prievadas |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendo URL | Jei dashboard talpinamas kitur, pridėkite jo URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Reikalinga CORS su kredencialais |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Leidžiami visi HTTP metodai |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Leidžiami visi antraštės laukai |

!!! note "Pastaba"

    Jei dashboard tiekiamas per nginx arba Apache numatytuoju HTTP prievadu, leistinas origin yra `http://localhost` — arba serverio viešasis URL, kai prieiga vyksta iš kitų mašinų.

#### [repo] skyrius

Šis skyrius konfigūruoja jungtį prie PostgreSQL duomenų bazės:

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
| `digna_REPO_HOST` | `localhost` arba IP | PostgreSQL serverio hostas/IP |
| `digna_REPO_PORT` | `5432` (numatytasis) | PostgreSQL prievadas |
| `digna_REPO_DB` | `postgres` | Duomenų bazės pavadinimas |
| `digna_REPO_SCHEMA` | `dignarepo` | Anksčiau sukurta schema |
| `digna_REPO_USER` | `digna_user` | PostgreSQL sukurtas vartotojas |
| `digna_REPO_PASSWORD` | Jūsų slaptažodis | Slaptažodis nustatytas kuriant schemą |

!!! tip "Geriausia praktika"

    `config.toml` talpina duomenų bazės slaptažodį atviru tekstu. Apribokite jo teises, kad tik paslaugos paskyra galėtų jį skaityti:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `digna_FERNET_KEY` | Šifravimo raktas | Naudojamas tokenams ir slapukams šifruoti (numatytasis pateiktas) |
| `digna_COOKIE_DOMAIN` | `localhost` | Sutapti su frontend domenu |
| `digna_COOKIE_SECURE` | `false` (lokaliai) / `true` (gamyboje) | Naudokite `true` HTTPS ryšiams |
| `digna_COOKIE_HTTPONLY` | `true` | Visada įjungta dėl saugumo |
| `digna_COOKIE_SAME_SITE` | `lax` | Apsaugo nuo CSRF atakų |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 val.) | Sesijos galiojimo laikas sekundėmis |
| `digna_MAX_WORKERS` | CPU branduolių skaičius - 1 | Lygiagretinimo užduočių skaičius |

!!! tip "Patarimas"

    Norėdami sužinoti, kiek CPU branduolių yra serveryje, vykdykite `nproc`.

#### [logging] skyrius

Šis skyrius konfigūruoja žurnalo elgseną:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` arba `DEBUG` | `INFO` gamybai, `DEBUG` trikčių šalinimui |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Kiek dieninių žurnalų kopijų saugoti |

---

### 2 žingsnis: inicializuokite saugyklą

1. Atidarykite terminalą
2. Eikite į digna diegimo katalogą (ten, kur yra `config.toml` ir vykdomasis failas `digna`)
3. Patikrinkite ryšį:

```bash
cd /opt/digna
./digna repo check
```

Turėtumėte matyti patvirtinimą, kad ryšys užmegztas (saugykla dar neinicijuota).

!!! note "Pastaba"

    Linux aplinkoje dabartinis katalogas nėra jūsų PATH, todėl vykdomasis failas paleidžiamas kaip `./digna`, o ne `digna`. Norėdami naudoti trumpesnį variantą visur, pridėkite simbolinę nuorodą:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### 3 žingsnis: įdiekite saugyklos schemą

Toje pačioje direktorijoje paleiskite:

```bash
./digna repo install
```

Ši komanda įdiegia reikalingas lenteles ir schemą jūsų PostgreSQL duomenų bazėje.

### 4 žingsnis: paleiskite digna serverį

digna diegimo kataloge paleiskite serverį:

```bash
./digna serve --address <host> --port <port>
```

**Parametrai:**
- `--address` — serverio host vardas/IP
- `--port` — serverio prievadas

Turėtumėte matyti paleidimo pranešimus, patvirtinančius, kad serveris veikia:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Patarimas"

    Jei dashboard tiekiamas iš kitos mašinos nei backend, taip pat atverkite API prievadą ugniasienėje:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### 5 žingsnis: sukurkite administratoriaus paskyrą

1. Atidarykite **naują** terminalo langą
2. Eikite į digna diegimo katalogą
3. Vykdykite šią komandą, kad sukurtumėte administratoriaus paskyrą:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Pavyzdys:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Tai sukuria vartotoją su vardu `admin` ir pilnomis administracinėmis teisėmis.

!!! tip "Patarimas"

    Apvyniokite slaptažodį viengubomis kabutėmis. `bash` ir `zsh` traktuoja simbolius, tokius kaip `!`, `$` ir `*`, specialiai — nepakankamai apibrėžtas slaptažodis su tokiais simboliais nebus perduotas kaip įvestas.

!!! tip "Geriausia praktika"

    Naudokite stiprų slaptažodį, kuriame būtų didžiosios, mažosios raidės, skaičiai ir specialūs simboliai.

---

## Dashboard konfigūracija {: #dashboard-configuration }

### 1 žingsnis: patalpinkite dashboard tinklapio serveryje

digna dashboard turi atskirą `config.toml` failą, esantį `dashboard/` kataloge. Ši konfigūracija jau pateikta ir pradiniam nustatymui ją keisti nereikia. Ją reikės keisti tik tuo atveju, jei norite pritaikyti backend ryšį arba atlikti sudėtingesnes diegimo konfigūracijas.

Jei reikia modifikuoti dashboard konfigūraciją (pvz., daugiaserveriniams diegimams), žiūrėkite dashboard dokumentaciją.

Pasirinkite tinklapio serverį ir vykdykite atitinkamus diegimo veiksmus.

#### Diegimas su nginx

Jei vykdėte [nginx diegimą](#nginx-setup), serverio blokas jau nurodo į jūsų `dashboard` katalogą ir kopijuoti nieko nereikia.

1. **Patvirtinkite kelią**
   - Atidarykite `/etc/nginx/conf.d/digna.conf`
   - Patikrinkite, ar `root` nurodo į jūsų išarchyvuotą `dashboard` katalogą

2. **Užtikrinkite, kad katalogas būtų skaitomas**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Perkraukite nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Patikrinkite diegimą**
   - Atidarykite naršyklę
   - Eikite į `http://localhost` (arba jūsų konfigūruotą URL)
   - Turėtumėte matyti digna dashboard prisijungimo puslapį

#### Diegimas su Apache httpd

1. **Kopijuokite dashboard į dokumentų šaknį**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Pridėkite perrašymo taisykles**

   Sukurkite `.htaccess` failą įdiegtoje direktorijoje, kad dashboard maršrutai išliktų po puslapio perkrovimo:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Įklijuokite žemiau pateiktą:

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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Prisijunkite prie dashboard**
   - Atidarykite naršyklę
   - Eikite į `http://localhost/digna`
   - Turėtumėte matyti digna dashboard prisijungimo puslapį

### 2 žingsnis: SELinux (tik RHEL šeimai)

RHEL, Rocky, AlmaLinux ir Fedora pagal nutylėjimą paleidžia SELinux ir jis gali užblokuoti tinklapio serverį skaitant failus iš neįprastų vietų. Patikrinkite, ar jis aktyvus:

```bash
getenforce
```

Jei rezultatas yra `Enforcing` ir jūs tiekiate dashboard iš `/opt/digna/dashboard`, pažymėkite katalogą tinkamu kontekstu, kad tinklapio serveris galėtų jį perskaityti:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Pastaba"

    Jei `semanage` neaptinkamas, įdiekite jį su `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Svarbu"

    Jei dashboard nuo naujai sukonfigūruotos RHEL sistemos grąžina **403 Forbidden**, paprastai tai SELinux žymėjimo problema, o ne failų teisių. Patikrinkite su `sudo ausearch -m avc -ts recent`.

---

## digna paleidimas kaip systemd paslauga {: #running-digna-as-a-systemd-service }

### Kodėl paleisti digna kaip paslaugą?

digna backend paleidimas kaip systemd paslauga užtikrina, kad jis:

- Automatiškai paleidžiamas kompiuteriui įsijungus
- Veikia fone be atviro terminalo lango
- Automatiškai persikrauna, jei sugesti
- Gali būti valdoma per `systemctl`, standartinį Linux paslaugų valdytoją

### Paslaugos valdymo failai

Visi reikalingi failai yra digna diegimo kataloge po: `bin/`

Galimi šie shell skriptai:

- `install_service.sh` — registruoja digna su systemd
- `uninstall_service.sh` — pašalina registraciją
- `start_service.sh` — paleidžia registruotą paslaugą
- `stop_service.sh` — sustabdo veikiančią paslaugą

!!! warning "Reikalingos root teisės"

    Visi skriptai turi būti vykdomi su `sudo`, nes registruojant paslaugą, kuri paleidžiama įkrovos metu, įrašomas unit failas į `/etc/systemd/system`.

### Paverskite skriptus vykdomais

Išarchyvavimas gali neišsaugoti vykdomojo bito. Prieš pirmą naudojimą:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Paslaugos įdiegimas

1. **Atidarykite terminalą**

2. **Eikite į bin katalogą**
   ```bash
   cd /opt/digna/bin
   ```

3. **Vykdykite diegimo skriptą**
   ```bash
   sudo ./install_service.sh
   ```

digna serveris dabar registruotas systemd su **automatiniu paleidimu**. Paslauga nėra paleidžiama iš karto — žr. kitą skyrių, kaip ją paleisti.

### Paslaugos paleidimas ir sustabdymas

#### Paslaugos paleidimas

1. Atidarykite terminalą
2. Eikite į `/opt/digna/bin`
3. Vykdykite:
   ```bash
   sudo ./start_service.sh
   ```

#### Paslaugos stabdymas

1. Atidarykite terminalą
2. Eikite į `/opt/digna/bin`
3. Vykdykite:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Patarimas"

    Visada sustabdykite paslaugą prieš atnaujinant programos failus.

### Paslaugos valdymas su systemctl

Užregistravus, paslauga gali būti valdoma standartinėmis systemd komandomis iš bet kurio katalogo:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Patikrinkite paslaugą

Norėdami patvirtinti, kad paslauga užregistruota ir veikia:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` reiškia, kad paslauga paleidžiama įkrovos metu; `active` reiškia, kad ji dabar veikia.

### Peržiūrėkite paslaugos žurnalus

systemd perima visą tai, ką backend rašo į konsolę. Skaityti žurnalą:

```bash
sudo journalctl -u digna -n 100
```

Norėdami sekti žurnalą gyvai atkuriant problemą:

```bash
sudo journalctl -u digna -f
```

!!! tip "Patarimas"

    Tai greičiausias būdas diagnozuoti paslaugą, kuri paleidžiama ir iš karto sustoja. Ryšio su saugykla klaidos arba trūkstamas `license.toml` pranešimas bus čia matomas.

### Perkelti paslaugą į naują katalogą

Unit failas saugo absoliutų kelią iki vykdomojo failo, todėl perkėlus diegimą reikia iš naujo registruoti paslaugą:

1. **Pašalinkite esamą paslaugą**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Perkelkite programos failus**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Iš naujo įdiekite paslaugą**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Paleiskite paslaugą**
   ```bash
   sudo ./start_service.sh
   ```

### Pašalinti paslaugą

1. **Sustabdykite veikiančią paslaugą**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Pašalinkite paslaugą**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna serveris dabar neberegistruotas systemd.

---

## Atnaujinimas į naują leidimą {: #upgrading-to-a-new-release }

### Prieš atnaujinant

**Digna saugyklos atsarginė kopija yra privaloma**

Prieš atnaujinant digna, sukurkite atsarginę savo saugyklos (PostgreSQL) kopiją, kad apsisaugotumėte nuo duomenų praradimo.
Atsarginė kopija leis atstatyti, jei atnaujinimas susidurs su netikėtomis problemomis.

Atsarginę kopiją sukurti iš shell:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Atnaujinimo procesas

#### 1 žingsnis: sustabdykite digna paslaugą

Jei digna veikia kaip systemd paslauga, pirmiausia ją sustabdykite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jei digna veikia pirmame plane, paspauskite `Ctrl + C` to terminalo lange.

#### 2 žingsnis: atsarginė dabartinio backend kopija

digna diegimo kataloge:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### 3 žingsnis: išarchyvuokite ir įdiekite naują versiją

1. Išarchyvuokite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į diegimo katalogą
3. Atstatykite vykdomąjį bitą ir paslaugos paskyros nuosavybę:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Svarbu"

    `config.toml` failas **niekada** nėra įtrauktas į diegimo ZIP. Jūsų esama konfigūracija lieka nepažeista.

### 4 žingsnis: atstatykite konfigūracijos failus

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### 5 žingsnis: atnaujinkite saugyklos schemą

Eikite į digna diegimo katalogą ir vykdykite:

```bash
cd /opt/digna
./digna repo upgrade
```

Tai atnaujins PostgreSQL schemą į naujausią versiją, išsaugant visus esamus duomenis.

### 6 žingsnis: paleiskite paslaugas iš naujo

Jei naudojate systemd paslaugą:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Jei paleidžiate rankiniu būdu, paleiskite serverį iš naujo:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Jei naudojate nginx arba Apache, perkraukite atitinkamą tinklapio serverį:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL šeimoje, jei pakeitėte `dashboard` katalogą, iš naujo pritaikykite SELinux žymėjimą:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### 7 žingsnis: patikrinkite atnaujinimą

1. Prisijunkite prie digna dashboard
2. Patikrinkite, ar sąsaja užsikrauna teisingai
3. Patikrinkite serverio žurnalus dėl klaidų:

```bash
sudo journalctl -u digna -n 100
```