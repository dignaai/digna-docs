---
title: Linuxi paigaldusjuhend – digna väljalase 2026.06 | digna dokumentatsioon
description: Samm-sammuline juhend digna väljalase 2026.06 paigaldamiseks Linuxis — süsteeminõuded, PostgreSQL seadistus, nginx või Apache konfiguratsioon, backendi ja dashboardi seadistamine, digna käivitamine systemd teenusena ning uuendamine uude versiooni.
keywords: digna linux paigaldus, digna juurutusjuhend, digna backend seadistus, digna dashboard paigaldus, postgresql linux, nginx linux, digna systemd teenus, digna uuendamise juhend
image: /assets/logo_square.png
---

# Linuxi paigaldusjuhend digna väljalase 2026.06

**Väljalase:** 2026.06

**Viimati uuendatud:** 5. september 2026


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

- **dignabackend**: Rakenduse tuum, mis vastutab andmete töötlemise ja kvaliteedikontrollide eest.
- **dignadashboard**: Veebipõhine liides, mis majutatakse veebiserveris ja pakub kasutajasõbralikku võimalust digna platvormiga suhelda ning andmete kvaliteeti visualiseerida.

### Mis on uut väljalahes 2026.06

See versioon toob andmevaatlikkuse (data observability) võimalused otse teie koodi, võimaldades arendajatel jälgida andmete kvaliteeti juba allikal. Täielikud andmed leiate [väljalaseteatmikust](http://docs.digna.ai/changelog/Release_202606/).

### Otsite Windowsi või macOS-i?

See juhend käsitleb Linuxi. Muude platvormide jaoks vaadake [Windowsi paigaldusjuhendit](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) või [macOS-i paigaldusjuhendit](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — Konfiguratsioonifail
   - `license.toml` — Litsentsifail (kopeerige siia oma fail)

Lahtipakkimiseks shellis:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

See sektsioon seadistab digna backendi rakenduse seadeid:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_APP_HOST` | `localhost` või IP-aadress | Hostinimi või IP, kus dignabackend jookseb |
| `digna_APP_PORT` | `8082` (vaikimisi) | REST API endpointide port |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendi URL | Kui dashboard asub teisel serveril, lisage selle URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutav CORS-i puhul koos tunnustega |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Lubab kõiki HTTP meetodeid |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Lubab kõiki päiseid |

!!! note "Märkus"

    Kui teenite dashboardi nginxi või Apache kaudu vaikimisi HTTP pordil, on lubatav origin `http://localhost` — või serveri avalik URL, kui dashboardile pääseb ligi teistelt masinatelt.

#### [repo] sektsioon

See sektsioon seadistab ühenduse PostgreSQL andmebaasiga:

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
| `digna_REPO_SCHEMA` | `dignarepo` | Varasemalt loodud skeem |
| `digna_REPO_USER` | `digna_user` | PostgreSQL-is loodud kasutaja |
| `digna_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |

!!! tip "Parim praktika"

    `config.toml` sisaldab andmebaasi parooli selges tekstis. Piirake faili õigusi nii, et ainult teenusekonto seda loeks:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] sektsioon

See sektsioon sisaldab turbe- ja küpsise seadeid:

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

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_FERNET_KEY` | Krüpteerimisvõti | Kasutatakse tokenite ja küpsiste krüpteerimiseks (vaikesäte olemas) |
| `digna_COOKIE_DOMAIN` | `localhost` | Vastab teie frontendi domeenile |
| `digna_COOKIE_SECURE` | `false` (lokalis) / `true` (tootmises) | Kasutage `true` HTTPS-i puhul |
| `digna_COOKIE_HTTPONLY` | `true` | Alati lubatud turvalisuse tõttu |
| `digna_COOKIE_SAME_SITE` | `lax` | Aitab ära hoida CSRF-rünnakuid |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumisaeg sekundites |
| `digna_MAX_WORKERS` | CPU tuumade arv - 1 | Paralleelsete inspekteerimiste ülesannete arv |

!!! tip "Vihje"

    Saate serveri CPU tuumade arvu teada käsuga `nproc`.

#### [logging] sektsioon

See sektsioon seadistab logimise käitumist:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` tootmises, `DEBUG` tõrkeotsinguks |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Päevaste logivarude hoidmise arv |

---

### Samm 2: Repository initsialiseerimine

1. Avage terminal
2. Minge digna paigalduskataloogi (kus asuvad `config.toml` ja `digna` käivitatav fail)
3. Käivitage ühenduse test:

```bash
cd /opt/digna
./digna repo check
```

Te peaksite nägema kinnitust, et ühendus on loodud (repository ise ei ole veel initsialiseeritud).

!!! note "Märkus"

    Linuxis ei ole praegune kataloog PATH-is, seega kutsutakse käivitatavat faili kui `./digna`, mitte lihtsalt `digna`. Lühikese vormi kasutamiseks igal pool lisage sümboolne link:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Samm 3: Repository skeemi paigaldamine

Selles kataloogis käivitage:

```bash
./digna repo install
```

See käsk paigaldab vajalikud tabelid ja skeemi teie PostgreSQL andmebaasi.

### Samm 4: digna serveri käivitamine

digna paigalduskataloogis käivitage server:

```bash
./digna serve --address <host> --port <port>
```

**Parameetrid:**
- `--address` — Serveri hostinimi/IP
- `--port` — Serveri port

Te peaksite nägema käivitussõnumeid, mis kinnitavad serveri tööd:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Vihje"

    Kui dashboard teenitakse teiselt masinalt kui backend, avage API port ka tulemüüris:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Samm 5: Admin-kasutaja loomine

1. Avage **uus** terminaliaken
2. Minge digna paigalduskataloogi
3. Käivitage järgmine käsk admin-kasutaja loomiseks:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Näide:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

See loob kasutaja nimega `admin` täielike administraatoriõigustega.

!!! tip "Vihje"

    Pange parool üksikutesse jutumärkidesse. `bash` ja `zsh` käsitlevad märke nagu `!`, `$` ja `*` eriliselt ning kui parool ei ole tsiteeritud, ei pruugi need tähemärgid õigesti läbida.

!!! tip "Parim praktika"

    Kasutage tugevat parooli, mis sisaldab suurtähti, väiketähti, numbreid ja erimärke.

---

## Dashboardi konfiguratsioon {: #dashboard-configuration }

### Samm 1: Dashboardi juurutamine veebiserverisse

digna dashboardil on eraldi `config.toml` fail asukohaga `dashboard/` kataloogis. See konfiguratsioon on juba kaasas ega vaja algseadistuse ajal muutmist. Muutke seda vaid juhul, kui peate kohandama backendiga ühenduse seadeid.

Kui peate dashboardi konfiguratsiooni muutma (nt multi-instance juurutuse puhul), vaadake dashboardi dokumentatsiooni.

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

### Enne uuendamist

**digna repository varundamine on kohustuslik**

Enne digna uuendamist varundage oma repository (PostgreSQL), et kaitsta andmete kadumise eest.
Varukoopia võimaldab taastada, kui uuendamine peaks kokku jooksma või esinevad ootamatud probleemid.

Varunduse loomiseks shellist:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Uuendamise protsess

#### Samm 1: Peatage digna teenus

Kui digna töötab systemd teenusena, peatage see esmalt:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Kui digna töötab esiplaanil, vajutage terminaliaknas `Ctrl + C`.

#### Samm 2: Varundage praegune backend paigaldus

digna paigalduskataloogis:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Samm 3: Uue versiooni lahtipakkimine ja juurutamine

1. Pakkige lahti uus digna paigaldus ZIP-fail
2. Kopeerige uus `digna` käivitatav fail ja `dashboard` kaust oma paigalduskataloogi
3. Taastage käivitusõigused ja teenuse konto omandiõigus:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Oluline"

    Faili `config.toml` EI SISALDATA kunagi paigaldusZIP. Teie olemasolev konfiguratsioon jääb alles.

### Samm 4: Taastage oma konfiguratsioonifailid

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Samm 5: Repository skeemi uuendamine

Minge digna paigalduskataloogi ja käivitage:

```bash
cd /opt/digna
./digna repo upgrade
```

See uuendab PostgreSQL skeemi uusimale versioonile, säilitades kogu olemasoleva andmebaasi sisu.

### Samm 6: Teenuste taaskäivitamine

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

#### Samm 7: Uuenduse kontrollimine

1. Avage digna dashboard
2. Kinnitage, et liides laadib korrektselt
3. Kontrollige serverilogi vigade osas:

```bash
sudo journalctl -u digna -n 100
```