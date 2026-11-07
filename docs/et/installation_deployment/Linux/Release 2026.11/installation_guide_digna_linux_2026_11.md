---
title: Linuxi paigaldusjuhend – digna väljalase 2026.11 | digna dokumentatsioon
description: Samm-sammuline juhend digna väljalase 2026.11 paigaldamiseks Linuxis — süsteeminõuded, PostgreSQL seadistus, nginx või Apache konfiguratsioon, backendi ja dashboardi seadistamine, digna käivitamine systemd teenusena ning uuendamine versioonilt Release 2026.06.
keywords: digna linux paigaldus, digna juurutusjuhend, digna backend seadistus, digna dashboard paigaldus, postgresql linux, nginx linux, digna systemd teenus, digna uuendamise juhend
image: /assets/logo_square.png
---

# Linuxi paigaldusjuhend digna väljalase 2026.11

**Väljalase:** 2026.11

**Viimati uuendatud:** 7. november 2026


---

## Sisukord

1. [Sissejuhatus](#introduction)
2. [Süsteeminõuded](#system-requirements)
3. [Eelpaigaldus ja ettevalmistus](#pre-installation-setup)
4. [PostgreSQL serveri seadistus](#postgresql-server-setup)
5. [Veebiserveri konfiguratsioon](#web-server-configuration)
6. [Algne paigaldus](#initial-installation)
7. [Backendi konfiguratsioon](#backend-configuration)
8. [Dashboardi konfiguratsioon](#dashboard-configuration)
9. [digna käitamine systemd teenusena](#running-digna-as-a-systemd-service)
10. [Uuendamine uude versiooni](#upgrading-to-a-new-release)

---

## Sissejuhatus {: #introduction }

### Mis on digna

digna on terviklik tehisintellektil põhinev platvorm, mis on loodud optimeerima andmete kvaliteedi haldust mitmesugustes andmekeskkondades nagu andmelaod, andmejärved ja lakehoused. Selle eesmärk on olla kõrge skaleeritavusega ja kohanduv — digna lahendab kaasaegseid andmeprobleeme automatiseerimise, reaalajas monitooringu ja anomaaliate tuvastuse kaudu.

digna koosneb kahest põhikomponendist:

- **digna**: rakenduse tuum, mis vastutab andmete töötlemise ja kvaliteedikontrollide läbiviimise eest. See ühendab taustasüsteemi ja käsurealiidese üheks käivitatavaks failiks ning asendab varasemate väljalasete eraldi programmid `dignabackend` ja `dignacli`.
- **dignadashboard**: Veebipõhine liides, mis majutatakse veebiserveris ja pakub kasutajasõbralikku võimalust digna platvormiga suhelda ning andmete kvaliteeti visualiseerida.

### Mis on uut väljalahes 2026.11

See väljalase toob kaasa uued moodulid digna Data Reconciliation ja digna Agentic (koos serveriga digna MCP Server) ning komponendi digna Engine, mis suudab andmeid profileerida digna sees ja kontrollida viidete terviklikkust eri andmebaasitehnoloogiate vahel. Täielikud andmed leiate [väljalaske märkmetest](../../../changelog/Release_202611.md).

Paigalduse jaoks toob väljalase uue hoidla migratsioonimehhanismi, komponendi digna Engine jaoks valikulise sektsiooni `[duckdb]` failis `config.toml` ning uue litsentsifaili. Neid kõiki käsitleb [uuendamise jaotis](#upgrading-to-a-new-release).

### Otsite Windowsi või macOS-i?

See juhend käsitleb Linuxi. Muude platvormide jaoks vaadake [Windowsi paigaldusjuhendit](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) või [macOS-i paigaldusjuhendit](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Millistele distributsioonidele see juhend kehtib?

Juhised on kirjutatud kahe kõige tavalisema serveripere jaoks. Kui kahe perekonna vahel on erinevusi, on mõlemad käsud toodud:

- **Debian perekond** — Debian, Ubuntu. Paketihaldur: `apt`.
- **RHEL perekond** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Paketihaldur: `dnf`.

Iga kaasaegne distributsioon, millel on `systemd`, töötab; muutuvad vaid paketinimed ja mõned konfiguratsiooniteed.

---

## Süsteeminõuded {: #system-requirements }

Enne paigaldust veenduge, et teie süsteem vastab järgmistele miinimumnõuetele:

| Nõue | Spetsifikatsioon |
|---|---|
| **Operatsioonisüsteem** | Ubuntu 22.04 LTS või uuem, Debian 12 või uuem, RHEL 9 / Rocky 9 / AlmaLinux 9 või uuem |
| **Arhitektuur** | x86_64 (amd64) või arm64 |
| **Init-süsteem** | systemd |
| **Mälu (miinimum)** | 16 GB RAM |
| **Kõvaketta ruum** | 10 GB vaba salvestusruumi |
| **Andmebaas** | PostgreSQL Server 12 või uuem |
| **Veebiserver** | nginx, Apache httpd või ekvivalent |

!!! info "digna Engine"

    Andmebaasiühendusi, mille profileerimise asukoht on digna Engine, profileeritakse digna hostis
    endas. Planeerige nende jaoks lisamälu ja -kettaruumi, vt
    [\[duckdb\] sektsioon](#duckdb-section).

### Andmebaasi paigaldamise valikud

**Kui PostgreSQL on juba paigaldatud:**
Võite lisada digna jaoks uue skeemi ja kasutaja olemasolevale PostgreSQL serverile.

**Kui paigaldate PostgreSQL-i samale masinale kui digna:**

!!! info "Soovitatavad spetsifikatsioonid"

    - **Mälu**: 32 GB RAM (võrreldes 16 GB-ga)
    - **Kõvaketta ruum**: 50 GB vaba salvestusruumi (võrreldes 10 GB-ga)

    Need kõrgemad spetsifikatsioonid arvestavad nii digna kui ka PostgreSQL andmebaasi samaaegset käivitamist.

### Distribuutori ja arhitektuuri kontrollimine

Mitu käsku selles juhendis erinevad Debian ja RHEL perekondade vahel. Et kontrollida, kummal te olete, käivitage:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` või `ID=debian` — kasutage `apt` käske.
- `ID=rhel`, `rocky`, `almalinux` või `fedora` — kasutage `dnf` käske.
- `x86_64` või `aarch64` — paigalduspaki jaoks vajalik arhitektuur.

---

## Eelpaigaldus ja ettevalmistus {: #pre-installation-setup }

Enne digna paigaldamist veenduge, et kaks peamist eeldust on täidetud:

1. **PostgreSQL server** – salvestamaks väljarvutatud mõõdikuid ja jõudluse andmeid
2. **Veebiserver** – digna Dashboardi majutamiseks

Kui need komponendid pole veel seadistatud, järgige allolevaid sektsioone nende paigaldamiseks ja konfigureerimiseks.

### Paketiloendi värskendamine

Uuendage oma paketiloend enne mis tahes paigaldust:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Märkus"

    Selles juhendis on paarikaupa toodud käsud: esimene käsk on **Debian perekonna** jaoks ja teine käsk on **RHEL perekonna** jaoks. Käivitage ainult see, mis vastab teie süsteemile.

---

## PostgreSQL serveri seadistus {: #postgresql-server-setup }

### Kui teil on PostgreSQL juba olemas

Kui PostgreSQL on juba paigaldatud ja töötab teie lokaalsel masinal või kasutate hallatavat kaugrepostgreSQL teenust, võite edasi liikuda [järgmisse sektsiooni](#web-server-configuration).

### PostgreSQL paigaldamine

#### Samm 1: Serverpaketi paigaldamine

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Vihje"

    Distrosõltuvad paketid võivad mõnikord järele jääda PostgreSQL ametlikest versioonidest. Kui vajate konkreetset uuemat versiooni, kasutage ametlikku [PostgreSQL apt- või yum-repositsiooni](https://www.postgresql.org/download/linux/).

#### Samm 2: Andmebaasi klastri algatamine

Debian perekonnas loob ja käivitab pakett klastri automaatselt — jätkake järgmise sammuga.

RHEL perekonnas tuleb klaster luua käsitsi:

```bash
sudo postgresql-setup --initdb
```

#### Samm 3: Teenuse käivitamine ja lubamine

```bash
sudo systemctl enable --now postgresql
```

See käivitab PostgreSQLi kohe ja seab selle automaatselt käivituma taaskäivituse korral.

#### Samm 4: Paigalduse kontrollimine

```bash
psql --version
sudo systemctl status postgresql
```

Peaksite nägema PostgreSQL versiooni ja teenuse olekut `active (running)`.

#### Samm 5: Ühendumine serveriga

Linuxi PostgreSQL-pakett loob süsteemikonto `postgres`, mis omab klastrit. Ühenduge selle kontoga:

```bash
sudo -u postgres psql
```

!!! note "Märkus — Linux erineb siin Windowsist"

    Windowsi paigaldaja küsib seadistuse käigus `postgres` superkasutaja parooli. Linuxi paketid ei tee seda. Selle asemel autentitakse kohalikud ühendused läbi **peer authentication**-i: operatsioonisüsteemi kasutaja `postgres` võib ühenduda andmebaasi kasutajana `postgres` ilma paroolita.

    Sellepärast kasutab ülevaltoodud käsk `sudo -u postgres`. digna backend töötab TCP kaudu kasutajanime ja parooliga, seega loote eraldi digna kasutaja [Algse paigalduse](#initial-installation) sammudes.

#### Samm 6: Pordi kinnitamine

Vaikimisi PostgreSQL kuulab porti `5432`. Et kinnitada, millisel pordil teie server kuulab:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Pange väärtus kirja — seda vajate digna backendit konfigureerides.

#### Samm 7: Paroolipõhise autentimise lubamine digna kasutaja jaoks

digna ühendub PostgreSQL-iga TCP kaudu kasutajana `digna_user`, mis vajab paroolipõhist autentimist peer-auth asemel. Kontrollige, et teie `pg_hba.conf` lubab seda.

Leidke fail:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Avage see redaktoris ja kinnitage, et lokaalsed TCP-ridad kasutavad `scram-sha-256` (või vanematel serveritel `md5`) mitte `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Laadige PostgreSQL uuesti pärast igat muutust:

```bash
sudo systemctl reload postgresql
```

!!! warning "Oluline"

    Kui digna teatab veast `FATAL: Ident authentication failed for user "digna_user"`, on selle põhjuseks ülaltoodud seadistus.

#### Samm 8: Kui PostgreSQL töötab teisel masinal

Et aktsepteerida ühendusi teiselt hostilt, seadistage `listen_addresses` failis `postgresql.conf` ja lisage võrgu jaoks sobiv `host` rida `pg_hba.conf`-i:

```
listen_addresses = '*'
```

Avage seejärel pordi tulemüüris ja taaskäivitage teenus:

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

## Veebiserveri konfiguratsioon {: #web-server-configuration }

digna vajab veebiserverit dashboardi majutamiseks. Valige üks järgmistest:

- [nginx](#nginx-setup) — kerge ja soovitatav
- [Apache httpd](#apache-setup) — laialt kasutatav alternatiiv

Teil on vaja installida ja konfigureerida ainult ÜKS neist serveritest.

Mõlemad sektsioonid seadistavad kaks asja, mis dashboardil vajalikud on:

- **Ühe lehe rakenduse fallback**, nii et dashboardi URL-i värskendamine ei tagasta 404 vea
- **`.md` MIME-tüüp**, et Markdown-failid teenitakse korrektselt

### nginx seadistamine {: #nginx-setup }

#### Ülevaade

nginx on kerge ja kõrge jõudlusega veebiserver, mis sobib hästi staatilise digna dashboardi serveerimiseks.

#### Paigaldamine

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginx käivitamine

```bash
sudo systemctl enable --now nginx
```

#### Paigalduse kontrollimine

1. Avage brauser
2. Minge `http://localhost`
3. Te peaksite nägema nginx tervituslehte

#### Tulemüüri avamine

Kui serverile pääseb ligi teistelt masinatelt, lubage HTTP liiklus:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Veebisaidi konfiguratsioon dashboardi jaoks

nginx laeb distributsioonidel faili iga faili `conf.d` kataloogist. Looge digna jaoks pühendatud konfiguratsioonifail sinna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Kleepige järgmine, asendades `/opt/digna/dashboard` tegeliku teega, kuhu olete `dashboard` kausta lahtipakinud:

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

!!! warning "Oluline"

    Ilma `try_files` direktiivita tagastab mis tahes dashboardi lehe värskendamine peale juur-URL-i 404. See on nginx ekvivalent IIS-is Windowsis nõutavale URL Rewrite moodulile.

#### Vaikimisi saidi keelamine

Porti võib olla ainult üks `default_server`. Debian perekonnas eemaldage pakendatud vaikimisi konfiguratsioon, et see ei segaks:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

RHEL perekonnas kommenteerige või kustutage `server { ... }` plokk failist `/etc/nginx/nginx.conf`.

#### Konfiguratsiooni rakendamine

Testige konfiguratsiooni süntaksi vea suhtes ja seejärel laadige nginx uuesti:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd seadistamine {: #apache-setup }

#### Ülevaade

Apache httpd on saadaval kõikide toetatud distributsioonide vaikerepositooriumites. Paketi nimi on Debian perekonnas `apache2` ja RHEL perekonnas `httpd`.

#### Paigaldamine

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apache käivitamine

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Paigalduse kontrollimine

1. Avage brauser
2. Minge `http://localhost`
3. Te peaksite nägema distributsiooni vaikimisi Apache lehte

#### Nõutav: mod_rewrite lubamine

Dashboard vajab URL-ide ümberkirjutamist.

Debian perekonnas lubage moodul ja taaskäivitage:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

RHEL perekonnas on `mod_rewrite` vaikimisi laetud. Kinnitage see:

```bash
httpd -M | grep rewrite
```

#### Nõutav: .htaccess üle kirjutuste lubamine

Avage dokumentjuure konfiguratsioonifail:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Leidke `<Directory>` plokk, mis katab teie dokumentjuure (`/var/www/html` mõlemas perekonnas) ja muutke:

```apache
AllowOverride None
```

järgmiseks:

```apache
AllowOverride All
```

#### Nõutav: Markdown-failide MIME-tüüp

Lisage samasse faili järgmine rida, et Markdown-failid teenitakse korrektselt:

```apache
AddType text/markdown .md
```

!!! warning "Oluline"

    Ilma selle seadeteta ei pruugi `.md` failid korralikult teeninduda.

#### Konfiguratsiooni rakendamine

Kontrollige konfiguratsiooni süntaksi vea suhtes ja seejärel taaskäivitage Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Algne paigaldus {: #initial-installation }

### Samm 1: digna andmehoidla (repository) seadistamine

digna repository salvestab kõik digna poolt arvutatud mõõdikud. See toimib analüütiliste ja jõudlusandmete keskandmebaasina.

#### Loo repository skeem ja kasutaja

Avage oma PostgreSQL klient (psql, pgAdmin või sarnane) ja käivitage järgmised SQL-käsud:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Asendage järgmised kohatäited:**

- `<digna_repo_schema>` — Teie soovitud skeemi nimi (nt `dignarepo`)
- `<digna_repo_user>` — Teie soovitud kasutajanimi (nt `digna_user`)
- `<digna_repo_password>` — Selle kasutaja jaoks turvaline parool

**Näide:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Shellist ühe sammuna käivitamiseks:

```bash
sudo -u postgres psql
```

Seejärel kleepige laused `postgres=#` prompti ja väljumiseks tippige `\q`.

!!! tip "Parim praktika"

    Kasutage andmebaasi kasutajate jaoks tugevaid, keerukaid paroole. Vältige kergesti äraarvatavaid mandaate.

---

### Samm 2: digna paigalduspaki lahtipakkimine

1. Leidke teile antud digna paigaldus ZIP-fail
2. Pakkige see soovitud paigalduskataloogi — näiteks `/opt/digna`
3. Pärast lahtipakkimist peaksite nägema järgmisi elemente:
   - `dashboard/` — Veebidashboardi liides
   - `digna` — Põhikäivitatav fail (backend + CLI koos)

!!! info "Konfiguratsiooni- ja litsentsifailid ei ole paketis"

    Paigaldusega ei kaasne ei `config.toml` ega `dashboard/dashboard_config.toml` — mõlemad
    loote ise, jaotistes [Backendi konfiguratsioon](#backend-configuration) ja
    [Dashboardii konfiguratsioon](#dashboard-configuration). Ka `license.toml` ei ole kaasas;
    digna tarnib selle eraldi, nagu kirjeldab samm 3.

Lahtipakkimiseks shellis:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Märkus"

    Kui `unzip` pole paigaldatud, lisage see käsuga `sudo apt install -y unzip` või `sudo dnf install -y unzip`.

#### Muutke käivitatav fail käivitatavaks

Sõltuvalt sellest, kuidas arhiiv üle viidi, ei pruugi käivitatav õigus säilida. Seadke see ekspilti:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Looge teenusekonto

Soovitatav on käivitada backend spetsiaalse piiratud õigustega kasutajana tootmiskeskkonnas:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Märkus"

    RHEL perekonnas on ekvivalentne shelli tee `/sbin/nologin`.

### Samm 3: Litsentsifaili paigaldamine

!!! warning "Oluline"

    Litsentsifaili ei sisaldu paigalduspakendis — see antakse teile eraldi digna poolt.

1. Leidke teile antud `license.toml` fail
2. Kopeerige see digna paigalduse juurkataloogi (sinna, kus asuvad `config.toml` ja `digna` käivitatav fail)

**Miks see oluline on:**
Litsentsifail sisaldab teie kliendiinfot, litsentsi aegumist ja digitaalallkirja. **Ärge muutke seda faili** — iga muudatus muudab selle kehtetuks.

**Kaustastruktuur pärast seadistust:**

```
/opt/digna/
├── config.toml         (konfiguratsioonifail)
├── license.toml        (TEIE LITSENTSI FAIL - kopeerige siia)
├── digna               (põhikäivitatav fail)
├── bin/                (teenusehaldusskriptid)
└── dashboard/          (veebiliides)
    └── (dashboard failid)
```

---

## Backendi konfiguratsioon {: #backend-configuration }

### Samm 1: Loo ja muuda konfiguratsioonifaili

Paigalduskaustas on olemas `config_template.toml` fail. Lihtsalt ümbernimetamine `config.toml`-iks piisab.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Asukoht:** `/opt/digna/config.toml`

Avage `config.toml` tekstiredaktoris ja seadistage alljärgnevad sektsioonid.

#### [app] sektsioon

See sektsioon seadistab dashboardi ja backendi vahelist päritoluülest ressursijagamist (CORS):

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboardi URL-id | URL-id, millelt dashboard serveeritakse. Brauseri päringud mis tahes muult päritolult lükatakse tagasi |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutav, et brauser saadaks igas päringus kaasa sessiooniküpsise |

!!! note "Märkus"

    Kui teenite dashboardi nginxi või Apache kaudu vaikimisi HTTP pordil, on lubatav origin `http://localhost` — või serveri avalik URL, kui dashboardile pääseb ligi teistelt masinatelt.

!!! info "Sektsioon [app] on valikuline"

    Alates Release 2026.11-st võib mõlemad võtmed ja kogu sektsiooni `[app]` ära jätta. See on
    õige seadistus, kui pöördpuhverserver (reverse proxy) serveerib dashboardi ja backendi ühe päritolu
    all: brauser ei tee siis päritoluüleseid päringuid ja vaikimisi pole ühtki lubatud.

#### [repo] sektsioon

See sektsioon seadistab ühenduse PostgreSQL andmebaasiga:

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
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Varasemalt loodud skeem |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL-is loodud kasutaja |
| `DIGNA_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |
| `DIGNA_REPO_SSLMODE` | `prefer` (vaikimisi) | Valikuline. PostgreSQL-i SSL-režiim: `disable`, `allow`, `prefer`, `require`, `verify-ca` või `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (vaikimisi) | Valikuline. Ühenduste arv, mida digna hoidlaga avatuna hoiab |

!!! tip "Parim praktika"

    `config.toml` sisaldab andmebaasi parooli selges tekstis. Piirake faili õigusi nii, et ainult teenusekonto seda loeks:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host, mille all dashboard on kättesaadav. `""` ei määra domeeni, mis on õige puhverserveri taga, mis serveerib dashboardi ja backendi ühe päritolu all |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Peab olema `true` alati, kui digna serveeritakse üle HTTPS-i |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Hoiab sessiooniküpsise skriptidele kättesaamatuna |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumisaeg sekundites |
| `DIGNA_MAX_WORKERS` | CPU tuumade arv - 1 | Samaaegselt töötada võivate inspekteerimiste arv |
| `DIGNA_FRONTEND_BASEURL` | Dashboardi URL | Kohustuslik. Kasutatakse teavitussõnumite linkides, seega peab see olema URL, mida adressaadid saavad avada |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (vaikimisi) | Valikuline. Sekundid, mille jooksul võib üks päring lähteandmebaasi vastu töötada, enne kui see katkestatakse; `0` lülitab ajalõpu välja |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (vaikimisi) | Valikuline. Sekundid, mille jooksul oodatakse ühendust lähteandmebaasiga; `0` ootab piiramatult |

!!! tip "Vihje"

    Saate serveri CPU tuumade arvu teada käsuga `nproc`.

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

See sektsioon seadistab logimise käitumist:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` tootmises, `DEBUG` tõrkeotsinguks. Aktsepteeritakse ka `TRACE`, `WARN` ja `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (vaikimisi) | Valikuline. Roteeruvate logifailide kataloog, suhteline töökataloogi suhtes |
| `DIGNA_LOGGING_MAX_FILES` | `30` (vaikimisi) | Valikuline. Säilitatavate roteeritud logifailide arv |

#### [duckdb] sektsioon (valikuline) {: #duckdb-section }

Uus väljalaskes Release 2026.11. See sektsioon määrab ressursid komponendile **digna Engine**, mis
profileerib andmeid digna sees nende andmebaasiühenduste puhul, mille profileerimise asukoht on
**digna Engine**, ning käitab viidete terviklikkuse kontrolle eri andmebaasiühendustel asuvate
andmeallikate vahel. Vaadake [Profileerimise asukoht](../../../platform/profiling/profiling_location.md).

Sektsioon on valikuline. Ilma selleta kehtivad allolevad vaikeväärtused.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (vaikimisi) | Mälu MB-des, mida üks digna Engine'i käivitus võib kasutada. Korraga võib aktiivne olla kuni `DIGNA_MAX_WORKERS` käivitust |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Vaikimisi: süsteemi ajutine kataloog (`$TMPDIR` või `/tmp`, kui see pole määratud) | Ajutiste failide kataloog, kui andmed mällu ei mahu |

!!! tip "digna Engine'i ressursside planeerimine"

    Planeerige digna hostis lisaks digna enda kasutatavale mälule kuni
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` mälu ning ajutises kataloogis piisavalt
    vaba kettaruumi, et sinna mahuksid digna Engine'i kasutavate andmeallikate suurima
    inspekteeritava kuupäeva andmed. Suunake `DIGNA_DUCKDB_TEMP_DIRECTORY` sellise ruumiga kettale,
    kuhu digna käitaval kontol on kirjutusõigus:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
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

### Samm 3: Repository initsialiseerimine

1. Avage terminal
2. Minge digna paigalduskataloogi (kus asuvad `config.toml` ja `digna` käivitatav fail)
3. Käivitage ühenduse test:

```bash
cd /opt/digna
./digna repo check
```

Uue skeemi puhul loob käsk ühenduse ja teatab seejärel, et hoidlat pole veel paigaldatud:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Selles etapis on see oodatud tulemus: see kinnitab, et digna jõuab PostgreSQL-i ja skeemini. Ühenduse- või autentimisviga viitab seevastu sektsioonile `[repo]` või PostgreSQL-i seadistusele.

!!! note "Märkus"

    Linuxis ei ole praegune kataloog PATH-is, seega kutsutakse käivitatavat faili kui `./digna`, mitte lihtsalt `digna`. Lühikese vormi kasutamiseks igal pool lisage sümboolne link:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Samm 4: Repository skeemi paigaldamine

Selles kataloogis käivitage:

```bash
./digna repo upgrade
```

See käsk paigaldab hoidla skeemi vajalikud tabelid ja lõpetab teatega:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade paigaldab ja uuendab"

    Alates Release 2026.11-st paigaldab `repo upgrade` uue hoidla ja uuendab olemasoleva.
    `repo install` töötab endiselt sama käsu teise nimena.

### Samm 5: Admin-kasutaja loomine

1. Avage **uus** terminaliaken
2. Minge digna paigalduskataloogi
3. Käivitage järgmine käsk admin-kasutaja loomiseks:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Näide:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

See loob kasutaja e-posti aadressiga `admin@example.com` ja täielike administraatoriõigustega.

!!! tip "Vihje"

    Pange parool üksikutesse jutumärkidesse. `bash` ja `zsh` käsitlevad märke nagu `!`, `$` ja `*` eriliselt ning kui parool ei ole tsiteeritud, ei pruugi need tähemärgid õigesti läbida.

!!! tip "Parim praktika"

    Kasutage tugevat parooli, mis sisaldab suurtähti, väiketähti, numbreid ja erimärke.

---

### Samm 6: digna serveri käivitamine

digna paigalduskataloogis käivitage server:

```bash
./digna serve --address <host> --port <port>
```

**Parameetrid:**
- `--address` — Serveri hostinimi/IP (vaikimisi `127.0.0.1`)
- `--port` — Serveri port (vaikimisi `8000`)

Kui server töötab, kuvab see aadressi, millel ta kuulab:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Vihje"

    Kui dashboard teenitakse teiselt masinalt kui backend, avage API port ka tulemüüris:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Server hoiab terminali hõivatuna"

    `serve` töötab esiplaanil ja jätkab, kuni peatate selle klahvidega ++ctrl+c++. Jätke see tööle, kuni seadistuse lõpetate; automaatseks käivitamiseks alglaadimisel vaadake [digna käitamine systemd teenusena](#running-digna-as-a-systemd-service).

## Dashboardi konfiguratsioon {: #dashboard-configuration }

### Samm 1: Dashboardi juurutamine veebiserverisse

digna dashboard loeb oma konfiguratsiooni failist `dashboard/dashboard_config.toml`. See fail ei ole paigaldusega kaasas — loote selle kataloogi `dashboard/` dashboardi failide kõrvale.

Selle sisu on kirjeldatud jaotises [Ühekordne sisselogimine (SSO)](../../../sso/overview.md), kus faili ka vaja läheb: see sisaldab dashboardi pakutavaid sisselogimisvalikuid ning mitme instantsiga juurutuste puhul ühendust backendiga.

Valige veebiserver ja järgige vastavaid juurutussamme.

#### Juurutamine nginx-i peale

Kui järgite [nginx seadistamise](#nginx-setup) juhiseid, osutab serveriblokk juba teie `dashboard` kaustale ja kopeerimist ei ole vaja.

1. **Kinnitage tee**
   - Avage `/etc/nginx/conf.d/digna.conf`
   - Kontrollige, et `root` osutab teie lahtipakitud `dashboard` kaustale

2. **Veenduge, et kaust on loetav**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Laadige nginx uuesti**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Testige paigaldust**
   - Avage brauser
   - Minge `http://localhost` (või teie seadistatud URL)
   - Teile peaks avanema digna dashboardi sisselogimisleht

#### Juurutamine Apache httpd peale

1. **Kopeerige dashboard dokumentjuurde**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Lisage ümberkirjutusreeglid**

   Looge `.htaccess` fail paigaldatud kausta nii, et dashboardi teekonnad säiliksid brauseri värskendamisel:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Kleepige järgmine:

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

3. **Taaskäivitage Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Avage dashboard**
   - Avage brauser
   - Minge `http://localhost/digna`
   - Te peaksite nägema digna dashboardi sisselogimislehte

### Samm 2: SELinux (ainult RHEL perekond)

RHEL, Rocky, AlmaLinux ja Fedora kasutavad vaikimisi SELinux-i, mis võib takistada veebiserveril lugemast faile väljaspool tema eeldatavaid asukohti. Kontrollige, kas see on aktiivne:

```bash
getenforce
```

Kui vastuseks on `Enforcing` ja te teenite dashboardi kataloogist `/opt/digna/dashboard`, märgistage kataloog nii, et veebiserver saaks seda lugeda:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Märkus"

    Kui `semanage` ei ole leitud, paigaldage see käsuga `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Oluline"

    Kui RHEL serveris konfigureeritud dashboard tagastab **403 Forbidden**, on tegemist peaaegu alati SELinux-i siltimise probleemiga, mitte faililubadega. Kinnitage see käsuga `sudo ausearch -m avc -ts recent`.

---

## digna käitamine systemd teenusena {: #running-digna-as-a-systemd-service }

### Miks käivitada digna teenusena?

digna backendi käitamine systemd teenusena tagab, et see:

- Käivitub automaatselt masina käivitamisel
- Töötab taustal ilma avatuna terminaliaknata
- Taaskäivitub automaatselt, kui see kukub kokku
- Seda saab hallata standardse Linuxi teenusehalduriga `systemctl`

### Teenusehalduse failid

Kõik vajalikud failid asuvad digna paigalduskataloogis alamkataloogis: `bin/`

Järgnevad shell-skriptid on olemas:

- `install_service.sh` — registreerib digna systemd-ga
- `uninstall_service.sh` — tühistab registreeritud teenuse
- `start_service.sh` — käivitab registreeritud teenuse
- `stop_service.sh` — peatab töötava teenuse

!!! warning "Root õigused vajalikud"

    Kõiki skripte tuleb käivitada `sudo`-ga, sest teenuse registreerimine, mis käivitub boot-il, kirjutab üksuse faili kataloogi `/etc/systemd/system`.

### Tee skriptid käivitatavaks

Arhiivi lahtipakkimine ei pruugi säilitada käivitusõigust. Enne esimest kasutust:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Teenuse paigaldamine

1. **Avage terminal**

2. **Minge bin kataloogi**
   ```bash
   cd /opt/digna/bin
   ```

3. **Käivitage paigaldusskript**
   ```bash
   sudo ./install_service.sh
   ```

digna server on nüüd registreeritud systemd-ga ja automaatne käivitamine on lubatud. Teenus ei pruugi käivituda koheselt — järgige järgmisi samme selle käivitamiseks.

### Teenuse käivitamine ja peatamine

#### Teenuse käivitamiseks

1. Avage terminal
2. Minge `/opt/digna/bin`
3. Käivitage:
   ```bash
   sudo ./start_service.sh
   ```

#### Teenuse peatamiseks

1. Avage terminal
2. Minge `/opt/digna/bin`
3. Käivitage:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Vihje"

    Peatage teenus alati enne rakedefailide uuendamist.

### Teenuse haldamine systemctl abil

Pärast registreerimist saab teenust hallata ka standardsete systemd käskudega igast kataloogist:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Teenuse kontrollimine

Teenuse registreerimise ja töötamise kinnitamiseks:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` tähendab, et teenus käivitub boot-il; `active` tähendab, et see töötab praegu.

### Teenuselogide vaatamine

systemd salvestab kõik, mida backend kirjutab konsoolile. Lugemiseks:

```bash
sudo journalctl -u digna -n 100
```

Reaalajas jälgimiseks ja probleemi reprodutseerimiseks:

```bash
sudo journalctl -u digna -f
```

!!! tip "Vihje"

    See on kõige kiirem viis diagnoosida teenust, mis käivitub ja kohe peatub. Siin teatatakse repositooriumi ühenduse vea või puuduva `license.toml` kohta.

### Teenuse liigutamine uude kataloogi

Üksuse fail sisaldab täispikka teed käivitatavale failile, seega installatsiooni liigutamine nõuab teenuse uuesti registreerimist:

1. **Desinstallige praegune teenus**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Liigutage rakenduse failid**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Paigaldage teenus uuesti**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Käivitage teenus**
   ```bash
   sudo ./start_service.sh
   ```

### Teenuse eemaldamine

1. **Peatage töötav teenus**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Desinstallige teenus**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna server on nüüd süsteemist unregisteritud.

---

## Uuendamine uude versiooni {: #upgrading-to-a-new-release }

See jaotis uuendab Release 2026.06 paigalduse versioonile Release 2026.11. Kui teie paigaldus
on vanem, lugege kõigepealt jaotist [Uuendamine väljalaskest, mis on vanem kui 2026.06](#upgrading-from-a-release-before-2026-06).

### Enne uuendamist

**digna repository varundamine on kohustuslik**

Enne digna uuendamist varundage oma repository (PostgreSQL), et kaitsta andmete kadumise eest.
Varukoopia võimaldab taastada, kui uuendamine peaks kokku jooksma või esinevad ootamatud probleemid.

Varunduse loomiseks shellist:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Release 2026.11 litsentsifaili taotlemine**

Release 2026.11 vajab uut faili `license.toml`. Taotlege see digna meeskonnalt enne alustamist ja
hoidke see [sammu 7](#step-7-replace-the-license-file) jaoks valmis.

### Uuendamine väljalaskest, mis on vanem kui 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 tõi kolm muudatust, mis kehtivad endiselt, kui uuendate vanema paigalduse otse
versioonile 2026.11:

- **Ainult ODBC.** digna jõuab iga lähtetehnoloogiani ODBC kaudu. Iga andmebaasiühendus, mis veel
  ODBC-d ei kasuta, tuleb pärast uuendamist ODBC-le üle viia; automaatset teisendust ei ole.
  Paigaldage ODBC draiverid digna hostile eelnevalt, vt
  [ODBC draiveri paigaldamine digna hostile](../../../databases/overview.md#install-the-driver),
  ning hoidke iga ühenduse omadused
  [tehnoloogiajuhenditest](../../../databases/overview.md#technology-guides) valmis. Databricks Legacy
  konnektorit enam ei ole; viige need ühendused üle
  [Databricks](../../../databases/databricks_connector_guide.md) konnektorile.
- **Üks käivitatav fail.** `dignabackend` ja `dignacli` on asendatud üheainsa käivitatava failiga
  `digna`, mis ühendab backendi ja CLI.
- **config.toml.** Sektsioon `[encryption]` on kohustuslik ning `DIGNA_APP_HOST` ja
  `DIGNA_APP_PORT` enam ei loeta: server võtab oma aadressi ja pordi käsult `digna serve`.
  Võrrelge oma faili jaotisega [Backendi konfiguratsioon](#backend-configuration).

Allolevad sammud toovad välja, kus vanem paigaldus vajab midagi muud. Sammu 8 hoidla uuendus viib
mis tahes varasema väljalaske hoidla otse versioonile 2026.11.

### Uuendamise protsess

#### Samm 1: Peatage digna teenus {: #step-1-stop-the-digna-service }

Kui digna töötab systemd teenusena, peatage see esmalt:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Kui digna töötab esiplaanil, vajutage terminaliaknas ++ctrl+c++.

#### Samm 2: Varundage praegune paigaldus {: #step-2-backup-current-installation }

Nimetage oma digna paigalduskataloogis praeguse paigalduse käivitatav fail ja kaust `dashboard`
ümber, et uut väljalaset saaks nende kõrvale paigaldada:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Hoidke `digna_old` alles, kuni olete uuenduse kontrollinud, ja `dashboard_old`, kuni olete sellest
oma konfiguratsioonifailid taastanud (vt samm 4). Seejärel võite mõlemad kustutada.

!!! info "Uuendamine väljalaskest, mis on vanem kui 2026.06"

    Nimetage käivitatava faili asemel ümber kaustad `dignabackend` ja `dignacli`:
    `sudo mv dignabackend dignabackend_old` ja `sudo mv dignacli dignacli_old`. Release 2026.11 ei kasuta kumbagi.

#### Samm 3: Uue versiooni lahtipakkimine ja juurutamine {: #step-3-extract-and-deploy-new-version }

1. Pakkige lahti uus digna paigaldus ZIP-fail
2. Kopeerige uus `digna` käivitatav fail ja `dashboard` kaust oma paigalduskataloogi
3. Taastage käivitusõigused ja teenuse konto omandiõigus:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Oluline"

    Paigaldus-ZIP ei sisalda kunagi ei faili `config.toml` ega `dashboard/dashboard_config.toml`
    — digna meeskond ei tarni kumbagi faili. Seetõttu ei puuduta uuendus teie olemasolevat
    konfiguratsiooni ning ümbernimetatud `*_old` kaustades olevad koopiad on ainsad, mis teil on.

#### Samm 4: Taastage oma konfiguratsioonifailid {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 ei vaja muudatusi failis `config.toml`: fail, mis töötab Release 2026.06-ga,
töötab edasi. Kaks muudatust on valikulised:

- Lisage [`[duckdb]` sektsioon](#duckdb-section), kui andmebaasiühendused peavad kasutama
  komponenti digna Engine ja selle vaikeväärtused teie hostile ei sobi.
- Jätke sektsioon `[app]` ära, kui pöördpuhverserver serveerib dashboardi ja backendi ühe päritolu all.

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

Dashboard koosneb staatilistest failidest, seega võivad teie veebiserver — ja brauser — ikka veel
serveerida eelmist versiooni. Laadige uuesti või taaskäivitage veebiserver, mis majutab kausta
`dashboard`, ning seejärel laadige leht sundvärskendusega uuesti (++ctrl+f5++).

#### Samm 6: Kontrollige konfiguratsiooni {: #step-6-validate-the-configuration }

Veenduge enne hoidla puudutamist, et `config.toml` on täielik:

```bash
./digna config check
```

Iga sektsioon peab teatama OK. Parandage kõik, millest teatatakse FAILED, eemaldage rea
**Unknown keys** all loetletud võtmed ja käivitage käsk enne jätkamist uuesti.

#### Samm 7: Asendage litsentsifail {: #step-7-replace-the-license-file }

Litsentsifail kandub tavaliselt ühest väljalaskest järgmisse üle. Release 2026.11 on erand: see
lisab kaks litsentsitavat moodulit, digna Data Reconciliation ja digna Agentic, ning enne 2026.11
väljastatud litsents neid ei sisalda. Kopeerige digna meeskonna poolt Release 2026.11 jaoks antud
`license.toml` paigalduskataloogi, asendades vana faili:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ärge jätke alles eelmist litsentsi"

    Eelmise litsentsiga digna küll käivitub, kuid digna Data Reconciliation ja digna MCP Server
    jäävad välja lülitatuks. Iga käsk, mis litsentsi kontrollib — `user`, `inspection`, `repo` —
    katkeb enne hoidla puudutamist, kui kontroll ebaõnnestub. Kontrollige uut litsentsi enne
    jätkamist:

    ```bash
    ./digna license check
    ```

#### Samm 8: Hoidla skeemi uuendamine {: #step-8-upgrade-the-repository-schema }

Käivitage oma digna paigalduskataloogis:

```bash
./digna repo upgrade
```

Release 2026.11 haldab hoidla skeemi versioonitud migratsioonidega. Esimene uuendus varasemast
väljalaskest viib skeemi eelmise versioonimisskeemi viimasele versioonile, salvestab selle
lähtepunktina ja rakendab seejärel Release 2026.11 migratsioonid. See lõpetab teatega:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Kõik olemasolevad andmed säilivad. Hoidla oleku nägemiseks igal ajal käivitage
`./digna repo check`: see loetleb viimase rakendatud migratsiooni ja kõik ootel migratsioonid.

!!! warning "digna ei käivitu aegunud hoidlaga"

    Alates Release 2026.11-st keeldub server käivitumast, kuni hoidla vajab uuendamist, ja teatab
    sellest, näiteks:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Käivitage `repo upgrade` enne serveri või teenuse käivitamist.

#### Samm 9: Teenuste taaskäivitamine {: #step-9-restart-services }

Kui teenus on systemd kaudu:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Kui käivitate käsitsi, käivitage server uuesti:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Kui kasutate nginx-i või Apache-t, laadige vastav veebiserver uuesti:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL perekonnas rakendage SELinux sildistamine uuesti, kui `dashboard` kataloog on asendatud:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Samm 10: Uuenduse kontrollimine {: #step-10-verify-the-upgrade }

1. Kontrollige uue käivitatava faili väljalaset:

    ```bash
    ./digna version
    ```

    Esimene rida peab olema `Release: 2026.11`.

2. Avage digna dashboard ja veenduge, et liides laadib korrektselt.
3. Kontrollige serverilogisid vigade suhtes:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Testige oma andmebaasiühendusi — vaadake
   [Ühenduse testimine](../../../databases/overview.md#testing-a-connection). Pärast uuendamist
   väljalaskest, mis on vanem kui 2026.06, viige esmalt ODBC-le üle iga ühendus, mis seda veel ei kasutanud.

Uute moodulitega alustamiseks vaadake [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Serveri kohta [AI-agendi ühendamine](../../../platform/agentic/connect_ai_agent.md) ja
digna Engine'i kohta [Profileerimise asukoht](../../../platform/profiling/profiling_location.md).
