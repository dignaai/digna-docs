# Linux diegimo vadovas digna leidimui 2026.11

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
9. [digna paleidimas kaip systemd paslauga](#running-digna-as-a-systemd-service)
10. [Atnaujinimas į naują leidimą](#upgrading-to-a-new-release)

---

## Įvadas {: #introduction }

### Apie digna

digna yra visapusiška, dirbtiniu intelektu paremta platforma, skirta optimizuoti duomenų kokybės valdymą įvairiose duomenų aplinkose, tokiose kaip duomenų sandėliai, ežerai ir lakehouse sprendimai. Sukurta būti itin mastelijama ir pritaikoma, digna sprendžia šiuolaikines duomenų problemas per automatizavimą, realaus laiko stebėjimą ir anomalijų aptikimą.

digna susideda iš dviejų pagrindinių komponentų:

- **digna**: programos branduolys, atsakingas už duomenų apdorojimą ir kokybės patikras. Jis sujungia užkulisinę dalį ir komandinęs eilutės sąsają į vieną vykdomąjį failą ir pakeičia atskiras ankstesnių leidimų programas `dignabackend` ir `dignacli`.
- **dignadashboard**: web sąsaja, talpinama tinklapio serveryje, suteikianti patogią prieigą prie digna platformos ir duomenų kokybės metrikų vizualizacijos.

### Kas naujo leidime 2026.11

Šis leidimas prideda digna Data Reconciliation, digna Agentic su digna MCP Server ir digna Engine, kuris gali profiliuoti duomenis pačioje digna ir tikrinti nuorodų vientisumą tarp skirtingų duomenų bazių technologijų. Išsamią informaciją rasite [leidimo pastabose](../../../changelog/Release_202611.md).

Diegimui leidimas atneša naują saugyklos migracijų mechanizmą, neprivalomą `[duckdb]` skyrių faile `config.toml`, skirtą digna Engine, ir naują licencijos failą. Kiekvieną iš jų aptaria [atnaujinimo skyrius](#upgrading-to-a-new-release).

### Ieškote Windows arba macOS instrukcijų?

Šis vadovas apima Linux. Kitiems platformoms žiūrėkite [Windows diegimo vadovą](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) arba [macOS diegimo vadovą](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

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

!!! info "digna Engine"

    Duomenų bazės ryšiai, kurių profiliavimo vieta yra digna Engine, profiliuojami pačiame digna
    pagrindiniame kompiuteryje. Numatykite jiems papildomos atminties ir disko vietos, žr.
    [\[duckdb\] skyrių](#duckdb-section).

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

!!! info "Konfigūracijos ir licencijos failų pakete nėra"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` diegimo pakete nepateikiami — abu
    failus sukuriate patys, skyriuose [Backend konfigūracija](#backend-configuration) ir
    [Dashboard konfigūracija](#dashboard-configuration). `license.toml` taip pat nepateikiamas;
    digna jį pateikia atskirai, kaip aprašyta 3 žingsnyje.

Išarchyvavimui iš shell:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
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

    Jei dashboard tiekiamas per nginx arba Apache numatytuoju HTTP prievadu, leistinas origin yra `http://localhost` — arba serverio viešasis URL, kai prieiga vyksta iš kitų mašinų.

!!! info "[app] skyrius yra neprivalomas"

    Nuo Release 2026.11 abu raktus ir visą `[app]` skyrių galima praleisti. Tai tinkama sąranka, kai
    atvirkštinis tarpinis serveris (reverse proxy) pateikia dashboard ir backend su ta pačia kilme
    (origin): tada naršyklė nesiunčia kryžminės kilmės užklausų, o pagal numatytuosius nustatymus nė
    viena neleidžiama.

#### [repo] skyrius

Šis skyrius konfigūruoja jungtį prie PostgreSQL duomenų bazės:

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
| `DIGNA_REPO_HOST` | `localhost` arba IP | PostgreSQL serverio hostas/IP |
| `DIGNA_REPO_PORT` | `5432` (numatytasis) | PostgreSQL prievadas |
| `DIGNA_REPO_DB` | `postgres` | Duomenų bazės pavadinimas |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Anksčiau sukurta schema |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL sukurtas vartotojas |
| `DIGNA_REPO_PASSWORD` | Jūsų slaptažodis | Slaptažodis nustatytas kuriant schemą |
| `DIGNA_REPO_SSLMODE` | `prefer` (numatytasis) | Neprivaloma. PostgreSQL SSL režimas: `disable`, `allow`, `prefer`, `require`, `verify-ca` arba `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (numatytasis) | Neprivaloma. Kiek ryšių su saugykla digna laiko atvirų |

!!! tip "Geriausia praktika"

    `config.toml` talpina duomenų bazės slaptažodį atviru tekstu. Apribokite jo teises, kad tik paslaugos paskyra galėtų jį skaityti:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    Norėdami sužinoti, kiek CPU branduolių yra serveryje, vykdykite `nproc`.

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

Šis skyrius konfigūruoja žurnalo elgseną:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametras | Reikšmė | Pastabos |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` arba `DEBUG` | `INFO` gamybai, `DEBUG` trikčių šalinimui. Taip pat priimami `TRACE`, `WARN` ir `ERROR` |
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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Numatytoji: sistemos laikinasis katalogas (`$TMPDIR` arba `/tmp`, kai jis nenustatytas) | Laikinųjų failų katalogas, kai duomenys netelpa į atmintį |

!!! tip "digna Engine išteklių planavimas"

    digna pagrindiniame kompiuteryje, be atminties, kurią naudoja pati digna, numatykite iki
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` atminties, o laikinajame kataloge –
    pakankamai laisvos disko vietos, kad tilptų didžiausios tikrinamos datos duomenys iš duomenų
    šaltinių, naudojančių digna Engine. Nukreipkite `DIGNA_DUCKDB_TEMP_DIRECTORY` į diską su tokia
    vieta, į kurį gali rašyti digna paleidžianti paskyra:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

### 3 žingsnis: inicializuokite saugyklą

1. Atidarykite terminalą
2. Eikite į digna diegimo katalogą (ten, kur yra `config.toml` ir vykdomasis failas `digna`)
3. Patikrinkite ryšį:

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

    Linux aplinkoje dabartinis katalogas nėra jūsų PATH, todėl vykdomasis failas paleidžiamas kaip `./digna`, o ne `digna`. Norėdami naudoti trumpesnį variantą visur, pridėkite simbolinę nuorodą:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### 4 žingsnis: įdiekite saugyklos schemą

Toje pačioje direktorijoje paleiskite:

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

### 5 žingsnis: sukurkite administratoriaus paskyrą

1. Atidarykite **naują** terminalo langą
2. Eikite į digna diegimo katalogą
3. Vykdykite šią komandą, kad sukurtumėte administratoriaus paskyrą:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Pavyzdys:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Taip sukuriamas naudotojas su el. pašto adresu `admin@example.com` ir visomis administratoriaus teisėmis.

!!! tip "Patarimas"

    Apvyniokite slaptažodį viengubomis kabutėmis. `bash` ir `zsh` traktuoja simbolius, tokius kaip `!`, `$` ir `*`, specialiai — nepakankamai apibrėžtas slaptažodis su tokiais simboliais nebus perduotas kaip įvestas.

!!! tip "Geriausia praktika"

    Naudokite stiprų slaptažodį, kuriame būtų didžiosios, mažosios raidės, skaičiai ir specialūs simboliai.

---

### 6 žingsnis: paleiskite digna serverį

digna diegimo kataloge paleiskite serverį:

```bash
./digna serve --address <host> --port <port>
```

**Parametrai:**
- `--address` — serverio host vardas/IP (numatytasis `127.0.0.1`)
- `--port` — serverio prievadas (numatytasis `8000`)

Kai serveris pasileidžia, jis išveda adresą, kuriuo klausosi:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Patarimas"

    Jei dashboard tiekiamas iš kitos mašinos nei backend, taip pat atverkite API prievadą ugniasienėje:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Serveris užima terminalą"

    `serve` veikia priekiniame plane ir tęsiasi, kol jį sustabdysite ++ctrl+c++. Palikite jį veikti, kol užbaigsite sąranką; kad jis būtų paleidžiamas automatiškai paleidus sistemą, žiūrėkite [digna paleidimas kaip systemd tarnybos](#running-digna-as-a-systemd-service).

## Dashboard konfigūracija {: #dashboard-configuration }

### 1 žingsnis: patalpinkite dashboard tinklapio serveryje

digna dashboard savo konfigūraciją skaito iš `dashboard/dashboard_config.toml`. Šis failas diegimo pakete nepateikiamas — jį sukuriate `dashboard/` kataloge šalia dashboard failų.

Jo turinys aprašytas skyriuje [Vienkartinis prisijungimas (SSO)](../../../sso/overview.md), kur šis failas ir reikalingas: jame nurodomos dashboard siūlomos prisijungimo parinktys, o daugiainstanciniams diegimams — ir ryšys su backend.

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

Šiame skyriuje aprašoma, kaip atnaujinti Release 2026.06 diegimą į Release 2026.11. Jei jūsų
diegimas senesnis, pirmiausia perskaitykite [Atnaujinimas iš senesnio nei 2026.06 leidimo](#upgrading-from-a-release-before-2026-06).

### Prieš atnaujinant

**Digna saugyklos atsarginė kopija yra privaloma**

Prieš atnaujinant digna, sukurkite atsarginę savo saugyklos (PostgreSQL) kopiją, kad apsisaugotumėte nuo duomenų praradimo.
Atsarginė kopija leis atstatyti, jei atnaujinimas susidurs su netikėtomis problemomis.

Atsarginę kopiją sukurti iš shell:

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

### Atnaujinimo procesas

#### 1 žingsnis: sustabdykite digna paslaugą {: #step-1-stop-the-digna-service }

Jei digna veikia kaip systemd paslauga, pirmiausia ją sustabdykite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jei digna veikia pirmame plane, paspauskite ++ctrl+c++ to terminalo lange.

#### 2 žingsnis: Sukurkite dabartinio diegimo atsarginę kopiją {: #step-2-backup-current-installation }

Savo digna diegimo kataloge pervadinkite dabartinio diegimo vykdomąjį failą ir `dashboard` aplanką,
kad naują leidimą būtų galima įdiegti šalia jų:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

`digna_old` laikykite, kol patikrinsite atnaujinimą, o `dashboard_old` – kol iš jo atkursite savo
konfigūracijos failus (žr. 4 žingsnį). Po to abu galite ištrinti.

!!! info "Atnaujinimas iš senesnio nei 2026.06 leidimo"

    Vietoj vykdomojo failo pervadinkite aplankus `dignabackend` ir `dignacli`:
    `sudo mv dignabackend dignabackend_old` ir `sudo mv dignacli dignacli_old`. Release 2026.11 nė vieno iš jų nenaudoja.

#### 3 žingsnis: išarchyvuokite ir įdiekite naują versiją {: #step-3-extract-and-deploy-new-version }

1. Išarchyvuokite naują digna diegimo ZIP failą
2. Nukopijuokite naują `digna` vykdomąjį failą ir `dashboard` katalogą į diegimo katalogą
3. Atstatykite vykdomąjį bitą ir paslaugos paskyros nuosavybę:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Svarbu"

    Nei `config.toml`, nei `dashboard/dashboard_config.toml` niekada nėra įtraukti į
    diegimo ZIP — digna komanda niekada nepateikia nė vieno iš šių failų. Todėl atnaujinimas jūsų
    esamos konfigūracijos nepaliečia, o kopijos pervadintuose `*_old` aplankuose yra
    vienintelės, kurias turite.

#### 4 žingsnis: atstatykite konfigūracijos failus {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
aplankas, tada iš naujo įkelkite puslapį priverstiniu atnaujinimu (++ctrl+f5++).

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
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nepalikite ankstesnės licencijos"

    Su ankstesne licencija digna vis tiek pasileidžia, tačiau digna Data Reconciliation ir
    digna MCP Server lieka išjungti. Kiekviena komanda, tikrinanti licenciją — `user`,
    `inspection`, `repo` — nepavykus patikrinimui nutraukiama dar prieš paliečiant saugyklą. Prieš
    tęsdami patikrinkite naująją licenciją:

    ```bash
    ./digna license check
    ```

#### 8 žingsnis: atnaujinkite saugyklos schemą {: #step-8-upgrade-the-repository-schema }

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

#### 9 žingsnis: paleiskite paslaugas iš naujo {: #step-9-restart-services }

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

#### 10 žingsnis: patikrinkite atnaujinimą {: #step-10-verify-the-upgrade }

1. Patikrinkite naujojo vykdomojo failo leidimą:

    ```bash
    ./digna version
    ```

    Pirmoji eilutė turi būti `Release: 2026.11`.

2. Atidarykite digna dashboard ir patikrinkite, ar sąsaja įkeliama teisingai.
3. Patikrinkite serverio žurnalus, ar nėra klaidų:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Išbandykite savo duomenų bazės ryšius — žr.
   [Ryšio tikrinimas](../../../databases/overview.md#testing-a-connection). Po atnaujinimo iš
   senesnio nei 2026.06 leidimo pirmiausia perkelkite į ODBC kiekvieną ryšį, kuris dar nenaudojo ODBC.

Norėdami pradėti dirbti su naujais moduliais, žr. [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI agento prijungimas](../../../platform/agentic/connect_ai_agent.md) – apie digna MCP Server, ir
[Profiliavimo vieta](../../../platform/profiling/profiling_location.md) – apie digna Engine.