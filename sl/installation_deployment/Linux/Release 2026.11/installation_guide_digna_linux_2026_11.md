# Navodila za namestitev na Linux za digna izdajo 2026.11

**Izdaja:** 2026.11

**Zadnja posodobitev:** 7. november 2026


---

## Kazalo

1. [Uvod](#introduction)
2. [Sistemske zahteve](#system-requirements)
3. [Prednamestitvena priprava](#pre-installation-setup)
4. [Nastavitev PostgreSQL strežnika](#postgresql-server-setup)
5. [Konfiguracija spletnega strežnika](#web-server-configuration)
6. [Začetna namestitev](#initial-installation)
7. [Konfiguracija backend‑a](#backend-configuration)
8. [Konfiguracija nadzorne plošče](#dashboard-configuration)
9. [Zagon digna kot storitve systemd](#running-digna-as-a-systemd-service)
10. [Nadgradnja na novo izdajo](#upgrading-to-a-new-release)

---

## Uvod {: #introduction }

### O digna

digna je celovita platforma, vodena z umetno inteligenco, namenjena optimizaciji upravljanja kakovosti podatkov v različnih podatkovnih okoljih, kot so podatkovna skladišča, podatkovna jezera in lakehouse‑i. Zasnovana je za visoko skalabilnost in prilagodljivost ter rešuje sodobne izzive podatkov s pomočjo avtomatizacije, spremljanja v realnem času in odkrivanja anomalij.

digna sestavljata dve glavni komponenti:

- **digna**: jedro aplikacije, odgovorno za obdelavo podatkov in izvajanje preverjanj kakovosti. Združuje backend in vmesnik ukazne vrstice v eno samo izvršljivo datoteko ter nadomešča ločena programa `dignabackend` in `dignacli` iz prejšnjih izdaj.
- **dignadashboard**: spletni vmesnik, gostovan na spletnem strežniku, ki omogoča enostavno interakcijo s platformo digna in vizualizacijo meritev kakovosti podatkov.

### Novosti v izdaji 2026.11

Ta izdaja dodaja digna Data Reconciliation, digna Agentic z digna MCP Server in digna Engine, ki lahko profilira podatke znotraj digna in preverja referenčno integriteto med različnimi tehnologijami podatkovnih baz. Za popolne podrobnosti si oglejte [opombe ob izdaji](../../../changelog/Release_202611.md).

Pri namestitvi izdaja prinaša nov mehanizem migracij repozitorija, izbirno sekcijo `[duckdb]` v `config.toml` za digna Engine in novo licenčno datoteko. Vse to pokriva [razdelek o nadgradnji](#upgrading-to-a-new-release).

### Iščete Windows ali macOS?

Ta vodič pokriva Linux. Za druge platforme si oglejte [navodila za namestitev na Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) ali [navodila za namestitev na macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Katere distribucije pokriva ta vodič?

Navodila so napisana za dve najpogostejši družini strežniških distribucij. Kjer se razlikujeta, sta navedena oba ukaza:

- **Družina Debian** — Debian, Ubuntu. Upravljalnik paketov: `apt`.
- **Družina RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Upravljalnik paketov: `dnf`.

Deluje vsaka sodobna distribucija s `systemd`; spremenijo se le imena paketov in nekatere konfiguracijske poti.

---

## Sistemske zahteve {: #system-requirements }

Preden začnete z namestitvijo, se prepričajte, da vaš sistem izpolnjuje naslednje minimalne zahteve:

| Zahteva | Specifikacija |
|---|---|
| **Operacijski sistem** | Ubuntu 22.04 LTS ali novejši, Debian 12 ali novejši, RHEL 9 / Rocky 9 / AlmaLinux 9 ali novejši |
| **Arhitektura** | x86_64 (amd64) ali arm64 |
| **Sistem init** | systemd |
| **Pomnilnik (minimalna namestitev)** | 16 GB RAM |
| **Prostor na disku** | 10 GB razpoložljivega prostora |
| **Baza podatkov** | PostgreSQL Server 12 ali novejši |
| **Spletni strežnik** | nginx, Apache httpd ali ekvivalent |

!!! info "digna Engine"

    Podatkovne povezave, ki kot lokacijo profiliranja uporabljajo digna Engine, se profilirajo na samem gostitelju digna. Zanje načrtujte dodaten pomnilnik in prostor na disku, glejte [sekcijo \[duckdb\]](#duckdb-section).

### Možnosti namestitve baze podatkov

**Če je PostgreSQL že nameščen:**
V obstoječi PostgreSQL strežnik lahko dodate novo bazo podatkov za digna.

**Če nameščate PostgreSQL na isti stroj kot digna:**

!!! info "Priporočene specifikacije"

    - **Pomnilnik**: 32 GB RAM (namesto 16 GB)
    - **Prostor na disku**: 50 GB razpoložljivega prostora (namesto 10 GB)

    Te višje specifikacije omogočajo hkratno delovanje digna in PostgreSQL baze podatkov.

### Preverjanje distribucije in arhitekture

Nekateri ukazi v tem vodiču se razlikujejo med družinama Debian in RHEL. Da preverite, katero uporabljate, zaženite:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` ali `ID=debian` — uporabite ukaze `apt`.
- `ID=rhel`, `rocky`, `almalinux` ali `fedora` — uporabite ukaze `dnf`.
- `x86_64` ali `aarch64` — arhitektura namestitvenega paketa, ki ga potrebujete.

---

## Prednamestitvena priprava {: #pre-installation-setup }

Pred namestitvijo digna poskrbite, da sta izpolnjena dva ključna predpogoja:

1. **PostgreSQL Server** – za shranjevanje izračunanih metrik in podatkov o zmogljivosti
2. **Spletni strežnik** – za gostovanje nadzorne plošče digna

Če ti komponenti še nista nastavljeni, sledite spodnjim razdelkom za namestitev in konfiguracijo.

### Osvežitev indeksa paketov

Pred kakršno koli namestitvijo posodobite sezname paketov:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Opomba"

    V celotnem vodiču je prvi ukaz v paru namenjen **družini Debian**, drugi pa **družini RHEL**. Zaženite samo tistega, ki ustreza vašemu sistemu.

---

## Nastavitev PostgreSQL strežnika {: #postgresql-server-setup }

### Če že imate PostgreSQL

Če je PostgreSQL že nameščen in teče na lokalnem stroju ali če uporabljate upravljan oddaljeni PostgreSQL strežnik, lahko preskočite na [naslednji razdelek](#web-server-configuration).

### Namestitev PostgreSQL

#### Korak 1: Namestite strežniški paket

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Namig"

    Paketi distribucij lahko zaostajajo za trenutno izdajo PostgreSQL. Če potrebujete določeno novejšo različico, namesto tega uporabite uradni [repozitorij PostgreSQL apt ali yum](https://www.postgresql.org/download/linux/).

#### Korak 2: Inicializirajte gručo baze podatkov

Pri **družini Debian** paket gručo ustvari in zažene samodejno — preskočite na naslednji korak.

Pri **družini RHEL** je treba gručo ustvariti izrecno:

```bash
sudo postgresql-setup --initdb
```

#### Korak 3: Zaženite in omogočite storitev

```bash
sudo systemctl enable --now postgresql
```

To takoj zažene PostgreSQL in ga nastavi, da se ob zagonu sistema znova samodejno zažene.

#### Korak 4: Preverite namestitev

```bash
psql --version
sudo systemctl status postgresql
```

Videti bi morali različico PostgreSQL in storitev v stanju `active (running)`.

#### Korak 5: Povežite se s strežnikom

Paket PostgreSQL za Linux ustvari sistemski račun `postgres`, ki je lastnik gruče. Povežite se prek njega:

```bash
sudo -u postgres psql
```

!!! note "Opomba — Linux se tu razlikuje od Windows"

    Namestitveni program za Windows vas med namestitvijo pozove, da nastavite geslo za superuporabnika `postgres`. Paketi za Linux tega ne storijo. Namesto tega se lokalne povezave preverjajo s **peer authentication**: uporabnik operacijskega sistema `postgres` se lahko brez gesla poveže kot uporabnik baze podatkov `postgres`.

    Zato zgornji ukaz uporablja `sudo -u postgres`. Backend digna se povezuje prek TCP z uporabniškim imenom in geslom, zato boste v razdelku [Začetna namestitev](#initial-installation) ustvarili izrecnega uporabnika za digna.

#### Korak 6: Potrdite vrata

Privzeta vrata PostgreSQL so `5432`. Za potrditev, na katerih vratih posluša vaš strežnik:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Zabeležite vrednost — potrebovali jo boste pri konfiguraciji backend‑a digna.

#### Korak 7: Omogočite preverjanje z geslom za uporabnika digna

digna se s PostgreSQL povezuje prek TCP kot `digna_user`, kar zahteva preverjanje z geslom namesto peer authentication. Preverite, ali to vaša datoteka `pg_hba.conf` dovoljuje.

Poiščite datoteko:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Odprite jo v urejevalniku in potrdite, da lokalne vrstice TCP uporabljajo `scram-sha-256` (ali `md5` na starejših strežnikih) namesto `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Po vsaki spremembi ponovno naložite PostgreSQL:

```bash
sudo systemctl reload postgresql
```

!!! warning "Pomembno"

    Če digna javi `FATAL: Ident authentication failed for user "digna_user"`, je vzrok ta nastavitev.

#### Korak 8: Če PostgreSQL teče na drugem stroju

Za sprejemanje povezav z drugega gostitelja nastavite `listen_addresses` v `postgresql.conf` in v `pg_hba.conf` dodajte ustrezno vrstico `host` za vaše omrežje:

```
listen_addresses = '*'
```

Nato odprite vrata v požarnem zidu in znova zaženite storitev:

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

## Konfiguracija spletnega strežnika {: #web-server-configuration }

digna zahteva spletni strežnik za gostovanje nadzorne plošče. Izberite eno od naslednjih možnosti:

- [nginx](#nginx-setup) — lahek in priporočen
- [Apache httpd](#apache-setup) — široko razširjena alternativa

Namestiti in konfigurirati morate le **enega** od teh strežnikov.

Oba razdelka konfigurirata dve stvari, od katerih je odvisna nadzorna plošča:

- **Nadomestno pot za enostransko aplikacijo (SPA fallback)**, tako da osvežitev URL‑ja nadzorne plošče ne vrne 404
- **MIME tip za `.md`**, da se Markdown datoteke strežejo pravilno

### Nastavitev nginx {: #nginx-setup }

#### Pregled

nginx je lahek, zmogljiv spletni strežnik, ki je primeren za streženje statične nadzorne plošče digna.

#### Namestitev

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Zagon nginx

```bash
sudo systemctl enable --now nginx
```

#### Preverjanje namestitve

1. Odprite brskalnik
2. Pojdite na `http://localhost`
3. Videti bi morali pozdravno stran nginx

#### Odpiranje požarnega zidu

Če do strežnika dostopajo drugi stroji, dovolite promet HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Konfiguracija mesta za nadzorno ploščo

nginx v obeh družinah distribucij vključi vse datoteke v svojem imeniku `conf.d`. Tam ustvarite namensko konfiguracijsko datoteko za digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Prilepite naslednje in zamenjajte `/opt/digna/dashboard` z dejansko potjo do razpakirane mape `dashboard`:

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

!!! warning "Pomembno"

    Brez direktive `try_files` osvežitev katere koli strani nadzorne plošče, razen korenskega URL‑ja, vrne 404. To je ekvivalent modula URL Rewrite, ki ga zahteva IIS v sistemu Windows.

#### Onemogočite privzeto mesto

Za posamezna vrata je lahko `default_server` le en strežniški blok. Pri **družini Debian** odstranite privzeto mesto iz paketa, da ne pride do konflikta:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Pri **družini RHEL** zakomentirajte ali izbrišite blok `server { ... }` v datoteki `/etc/nginx/nginx.conf`.

#### Uveljavitev konfiguracije

Preverite konfiguracijo za sintaktične napake, nato ponovno naložite nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Nastavitev Apache httpd {: #apache-setup }

#### Pregled

Apache httpd je na voljo v privzetih repozitorijih vseh podprtih distribucij. Paket se v družini Debian imenuje `apache2`, v družini RHEL pa `httpd`.

#### Namestitev

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Zagon Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Preverjanje namestitve

1. Odprite brskalnik
2. Pojdite na `http://localhost`
3. Videti bi morali privzeto stran Apache vaše distribucije

#### Obvezno: omogočite mod_rewrite

Nadzorna plošča zahteva prepisovanje URL‑jev.

Pri **družini Debian** omogočite modul in znova zaženite strežnik:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Pri **družini RHEL** je `mod_rewrite` naložen privzeto. Potrdite to:

```bash
httpd -M | grep rewrite
```

#### Obvezno: dovolite preglasitve .htaccess

Odprite konfiguracijsko datoteko za svoj korenski imenik dokumentov:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Poiščite blok `<Directory>`, ki pokriva vaš korenski imenik dokumentov (`/var/www/html` v obeh družinah), in spremenite:

```apache
AllowOverride None
```

v:

```apache
AllowOverride All
```

#### Obvezno: MIME tip za Markdown datoteke

V isto datoteko dodajte naslednjo vrstico, da se Markdown datoteke strežejo pravilno:

```apache
AddType text/markdown .md
```

!!! warning "Pomembno"

    Brez te nastavitve se datoteke `.md` morda ne bodo stregle pravilno.

#### Uveljavitev konfiguracije

Preverite konfiguracijo za sintaktične napake, nato znova zaženite Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Začetna namestitev {: #initial-installation }

### Korak 1: Nastavite repozitorij digna

Repozitorij digna hrani vse metrike, ki jih izračuna digna. Deluje kot osrednja baza podatkov za analitične podatke in podatke o zmogljivosti.

#### Ustvarite shemo repozitorija in uporabnika

Odprite svoj PostgreSQL odjemalec (psql, pgAdmin ali podoben) in izvedite naslednje ukaze SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Zamenjajte naslednje nadomestne vrednosti:**

- `<digna_repo_schema>` — želeno ime sheme (npr. `dignarepo`)
- `<digna_repo_user>` — želeno uporabniško ime (npr. `digna_user`)
- `<digna_repo_password>` — varno geslo za tega uporabnika

**Primer:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Za izvedbo teh ukazov iz lupine v enem koraku:

```bash
sudo -u postgres psql
```

Nato prilepite stavke na poziv `postgres=#` in vtipkajte `\q`, da zapustite program.

!!! tip "Najboljša praksa"

    Za uporabnike baze podatkov uporabljajte močna, kompleksna gesla. Izogibajte se poverilnicam, ki jih je lahko uganiti.

---

### Korak 2: Razpakirajte namestitveni paket digna

1. Poiščite ZIP datoteko namestitvenega paketa digna, ki vam je bila posredovana
2. Razpakirajte jo na želeno lokacijo namestitve — na primer `/opt/digna`
3. Po razpakiranju bi morali videti naslednje elemente:
   - `dashboard/` — spletni vmesnik nadzorne plošče
   - `digna` — glavna izvršljiva datoteka (backend + CLI skupaj)

!!! info "Konfiguracijskih in licenčnih datotek ni v paketu"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista priložena namestitvi — obe
    ustvarite sami, v razdelkih [Konfiguracija backend‑a](#backend-configuration) in
    [Konfiguracija nadzorne plošče](#dashboard-configuration). Tudi `license.toml` ni priložena;
    digna jo posreduje ločeno, kot opisuje Korak 3.

Za razpakiranje iz lupine:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Opomba"

    Če `unzip` ni nameščen, ga dodajte z `sudo apt install -y unzip` ali `sudo dnf install -y unzip`.

#### Omogočite zagon izvršljive datoteke

Glede na način prenosa arhiva se bit za izvajanje ob razpakiranju morda ne ohrani. Nastavite ga izrecno:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Ustvarite storitveni račun

Za produkcijske namestitve je priporočljivo, da backend teče pod namenskim uporabnikom brez posebnih pravic:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Opomba"

    V družini RHEL je ustrezna pot lupine `/sbin/nologin`.

### Korak 3: Namestite licenčno datoteko

!!! warning "Pomembno"

    Licenčna datoteka **ni** vključena v namestitveni paket in vam jo bo digna posredovala ločeno.

1. Poiščite datoteko `license.toml`, ki vam je bila posredovana
2. Kopirajte jo v korenski imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)

**Zakaj je to pomembno:**
Licenčna datoteka vsebuje podatke o stranki, datum poteka licence in digitalni podpis. **Ne spreminjajte te datoteke** — vsaka sprememba jo razveljavi.

**Struktura imenika po nastavitvi:**

```
/opt/digna/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
├── bin/                (service management scripts)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Konfiguracija backend‑a {: #backend-configuration }

### Korak 1: Ustvarite in uredite konfiguracijsko datoteko

V namestitvenem imeniku digna je priložena datoteka `config_template.toml`. Preimenovati jo morate le v `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Lokacija:** `/opt/digna/config.toml`

Odprite `config.toml` v urejevalniku besedil in konfigurirajte vsako od spodnjih sekcij.

#### Sekcija [app]

Ta sekcija konfigurira deljenje virov med izvori (CORS) med nadzorno ploščo in backendom:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL-ji nadzorne plošče | URL-ji, s katerih se streže nadzorna plošča. Zahteve brskalnika s katerega koli drugega izvora so zavrnjene |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Obvezno, da brskalnik z vsako zahtevo pošlje sejni piškotek |

!!! note "Opomba"

    Če nadzorno ploščo strežete prek nginx ali Apache na privzetih vratih HTTP, je izvor, ki ga je treba dovoliti, `http://localhost` — ali javni URL strežnika, kadar do nadzorne plošče dostopajo drugi stroji.

!!! info "Sekcija [app] je izbirna"

    Od izdaje 2026.11 lahko oba ključa in celotno sekcijo `[app]` izpustite. To je prava nastavitev, kadar obratni posrednik (reverse proxy) streže nadzorno ploščo in backend pod enim izvorom: brskalnik takrat ne pošilja zahtev med izvori, privzeto pa nobena ni dovoljena.

#### Sekcija [repo]

Ta sekcija konfigurira povezavo s PostgreSQL bazo podatkov:

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

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` ali IP | Ime gostitelja/IP PostgreSQL strežnika |
| `DIGNA_REPO_PORT` | `5432` (privzeto) | Vrata PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Ime baze podatkov |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Prej ustvarjena shema |
| `DIGNA_REPO_USER` | `digna_user` | Uporabnik, ustvarjen pri nastavitvi PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Vaše geslo | Geslo, nastavljeno ob ustvarjanju sheme |
| `DIGNA_REPO_SSLMODE` | `prefer` (privzeto) | Izbirno. Način SSL za PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` ali `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (privzeto) | Izbirno. Število povezav, ki jih digna ohranja odprte do repozitorija |

!!! tip "Najboljša praksa"

    `config.toml` vsebuje geslo baze podatkov v navadnem besedilu. Omejite njegova dovoljenja, tako da ga lahko bere le storitveni račun:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Sekcija [base]

Ta sekcija vsebuje nastavitve varnosti, piškotkov in pregledov:

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

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_FERNET_KEY` | Zgoraj prikazana vrednost | Ključ šifriranja, ki so ga uporabljale prejšnje izdaje. Biti mora prisoten; ohranite prikazano vrednost |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Gostitelj, prek katerega je dosegljiva nadzorna plošča. `""` ne nastavi domene, kar je pravilno za posrednikom, ki nadzorno ploščo in backend streže pod enim izvorom |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Mora biti `true`, kadar koli se digna streže prek HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Sejni piškotek ohranja nedosegljiv za skripte |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 ur) | Čas poteka seje v sekundah |
| `DIGNA_MAX_WORKERS` | Število jeder CPU - 1 | Število pregledov, ki se lahko izvajajo hkrati |
| `DIGNA_FRONTEND_BASEURL` | URL nadzorne plošče | Obvezno. Uporablja se za povezave v sporočilih obvestil, zato mora biti URL, ki ga prejemniki lahko odprejo |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (privzeto) | Izbirno. Število sekund, kolikor sme posamezna poizvedba v izvorni bazi podatkov teči, preden se prekine; `0` onemogoči časovno omejitev |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (privzeto) | Izbirno. Število sekund čakanja na povezavo z izvorno bazo podatkov; `0` čaka neomejeno dolgo |

!!! tip "Namig"

    Za ugotovitev števila jeder CPU, ki so na voljo na vašem strežniku, zaženite `nproc`.

#### Sekcija [encryption]

Ta sekcija vsebuje ključ, s katerim se šifrirajo občutljive vrednosti, shranjene v repozitoriju. Je **obvezna** — `config check` sekcijo `[encryption]` javi kot FAILED, če ključ manjka.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Ključ, kodiran v Base64 | Šifrira občutljive vrednosti, shranjene v repozitoriju digna |

!!! warning "Zaščitite config.toml"

    Ta ključ je fiksna vrednost, enaka v vseh namestitvah digna, in prav on dešifrira
    občutljive vrednosti v vašem repozitoriju. Dostop do `config.toml` omejite na račun, pod katerim teče
    digna, datoteko hranite zunaj sistema za nadzor različic in deljenih diskov ter jo izključite iz vsake varnostne kopije,
    ki je shranjena manj varno kot repozitorij sam.

#### Sekcija [logging]

Ta sekcija konfigurira beleženje:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` ali `DEBUG` | `INFO` za produkcijo, `DEBUG` za odpravljanje težav. Sprejeti so tudi `TRACE`, `WARN` in `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (privzeto) | Izbirno. Imenik za rotirajoče dnevniške datoteke, relativno glede na delovni imenik |
| `DIGNA_LOGGING_MAX_FILES` | `30` (privzeto) | Izbirno. Število rotiranih dnevniških datotek, ki se hranijo |

#### Sekcija [duckdb] (izbirno) {: #duckdb-section }

Novo v izdaji 2026.11. Ta sekcija določa vire za **digna Engine**, ki profilira podatke znotraj digna za podatkovne povezave, katerih lokacija profiliranja je **digna Engine**, in izvaja preverjanja referenčne integritete med viri podatkov na različnih podatkovnih povezavah. Glejte [Lokacija profiliranja](../../../platform/profiling/profiling_location.md).

Sekcija je izbirna. Brez nje veljajo spodnje privzete vrednosti.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (privzeto) | Pomnilnik v MB, ki ga sme porabiti en zagon digna Engine. Hkrati je lahko aktivnih do `DIGNA_MAX_WORKERS` zagonov |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Privzeto: sistemski začasni imenik (`$TMPDIR` ali `/tmp`, če ta ni nastavljen) | Imenik za začasne datoteke, kadar podatki ne gredo v pomnilnik |

!!! tip "Dimenzioniranje digna Engine"

    Načrtujte do `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` pomnilnika na gostitelju digna, poleg tega, kar porabi digna sama, ter dovolj prostega prostora na disku v začasnem imeniku za največji pregledani datum virov podatkov, ki uporabljajo digna Engine. `DIGNA_DUCKDB_TEMP_DIRECTORY` usmerite na disk s tem prostorom, v katerega lahko piše račun, pod katerim teče digna:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    To sekcijo potrebujete le, če vsaj ena podatkovna povezava uporablja digna Engine ali če preverjanje referenčne integritete primerja vire podatkov na različnih povezavah.

---

### Korak 2: Preverite konfiguracijo

Pred inicializacijo repozitorija preverite, ali je `config.toml` popoln in pravilno sestavljen. V namestitvenem imeniku digna zaženite:

```bash
./digna config check
```

Vsaka sekcija se preveri posebej, tako da posamezna napaka ne prikrije stanja ostalih:

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

Odpravite vse, kar je javljeno kot FAILED, in pred nadaljevanjem ukaz zaženite znova. WARNING pod **Unknown keys** navaja ključe v `config.toml`, ki jih digna ne bere; nimajo nobenega učinka, zato jih odstranite ali popravite njihov zapis. Celoten seznam možnosti najdete v [referenci CLI](../../../cli/Command_Line_Interface_202611.md).

### Korak 3: Inicializirajte repozitorij

1. Odprite terminal
2. Pojdite v imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)
3. Zaženite test povezave:

```bash
cd /opt/digna
./digna repo check
```

Na novi shemi se ukaz poveže in nato javi, da repozitorij še ni nameščen:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Na tej točki je to pričakovani rezultat: potrjuje, da digna doseže PostgreSQL in shemo. Napaka pri povezavi ali preverjanju pristnosti pa kaže na sekcijo `[repo]` ali na nastavitev PostgreSQL.

!!! note "Opomba"

    V sistemu Linux trenutni imenik ni v vašem PATH, zato se izvršljiva datoteka kliče kot `./digna` namesto `digna`. Če želite krajšo obliko uporabljati povsod, dodajte simbolno povezavo:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Korak 4: Namestite shemo repozitorija

V istem imeniku zaženite:

```bash
./digna repo upgrade
```

Ta ukaz namesti potrebne tabele v shemo repozitorija in se konča z:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade namešča in nadgrajuje"

    Od izdaje 2026.11 `repo upgrade` namesti nov repozitorij in nadgradi obstoječega. `repo install` še vedno deluje kot drugo ime za isti ukaz.

### Korak 5: Ustvarite skrbniškega uporabnika

Skrbniški uporabnik se ustvari neposredno v shemi repozitorija, zato strežniku še ni treba teči. V imeniku namestitve digna zaženite:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Primer:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

S tem se ustvari uporabnik z e-poštnim naslovom `admin@example.com` in polnimi skrbniškimi pravicami.

!!! tip "Namig"

    Geslo zapišite v enojnih narekovajih. `bash` in `zsh` znake, kot so `!`, `$` in `*`, obravnavata posebej, zato geslo brez narekovajev, ki jih vsebuje, ne bo posredovano tako, kot ste ga vnesli.

!!! tip "Najboljša praksa"

    Uporabite močno geslo z mešanico velikih in malih črk, številk in posebnih znakov.

### Korak 6: Zaženite strežnik digna

V imeniku namestitve digna zaženite strežnik z ukazom:

```bash
./digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — ime gostitelja/IP strežnika (privzeto `127.0.0.1`)
- `--port` — vrata strežnika (privzeto `8000`)

Ko strežnik teče, izpiše naslov, na katerem posluša:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Namig"

    Če se nadzorna plošča streže z drugega stroja kot backend, v požarnem zidu odprite tudi vrata API:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Strežnik zaseda terminal"

    `serve` teče v ospredju in deluje, dokler ga ne ustavite s ++ctrl+c++. Pustite ga teči, dokler ne dokončate namestitve; če naj se namesto tega samodejno zaganja ob zagonu sistema, glejte [Zagon digna kot storitve systemd](#running-digna-as-a-systemd-service).

---

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Korak 1: Razmestite nadzorno ploščo na spletni strežnik

Nadzorna plošča digna prebere svojo konfiguracijo iz datoteke `dashboard/dashboard_config.toml`. Ta datoteka ni priložena namestitvi — ustvarite jo v imeniku `dashboard/` poleg datotek nadzorne plošče.

Njena vsebina je opisana v razdelku [Enotna prijava (SSO)](../../../sso/overview.md), kjer je datoteka tudi potrebna: vsebuje možnosti prijave, ki jih ponuja nadzorna plošča, in pri večinstančnih namestitvah povezavo na backend.

Izberite spletni strežnik in sledite ustreznim korakom za razmestitev.

#### Razmestitev na nginx

Če ste sledili razdelku [Nastavitev nginx](#nginx-setup), strežniški blok že kaže na vašo mapo `dashboard` in kopiranje ni potrebno.

1. **Potrdite pot**
   - Odprite `/etc/nginx/conf.d/digna.conf`
   - Preverite, ali `root` kaže na vašo razpakirano mapo `dashboard`

2. **Poskrbite, da je mapa berljiva**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Ponovno naložite nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Preizkusite namestitev**
   - Odprite brskalnik
   - Pojdite na `http://localhost` (ali vaš konfigurirani URL)
   - Videti bi morali prijavno stran nadzorne plošče digna

#### Razmestitev na Apache httpd

1. **Kopirajte nadzorno ploščo v korenski imenik dokumentov**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Dodajte pravila za prepisovanje**

   V razmeščeni mapi ustvarite datoteko `.htaccess`, da poti nadzorne plošče preživijo osvežitev brskalnika:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Prilepite naslednje:

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

3. **Znova zaženite Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Dostopite do nadzorne plošče**
   - Odprite brskalnik
   - Pojdite na `http://localhost/digna`
   - Videti bi morali prijavno stran nadzorne plošče digna

### Korak 2: SELinux (samo družina RHEL)

V sistemih RHEL, Rocky, AlmaLinux in Fedora je SELinux privzeto v načinu enforcing in spletnemu strežniku prepreči branje datotek zunaj pričakovanih lokacij. Preverite, ali je aktiven:

```bash
getenforce
```

Če je rezultat `Enforcing` in nadzorno ploščo strežete iz `/opt/digna/dashboard`, imenik označite tako, da ga spletni strežnik sme brati:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Opomba"

    Če `semanage` ni najden, ga namestite z `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Pomembno"

    Če nadzorna plošča na sveže konfiguriranem strežniku RHEL vrne **403 Forbidden**, gre skoraj vedno za težavo z oznakami SELinux in ne z dovoljenji datotek. Potrdite to z `sudo ausearch -m avc -ts recent`.

---

## Zagon digna kot storitve systemd {: #running-digna-as-a-systemd-service }

### Zakaj zagnati digna kot storitev?

Zagon backend‑a digna kot storitve systemd zagotavlja, da se:

- samodejno zažene ob zagonu stroja
- izvaja v ozadju brez odprtega okna terminala
- samodejno znova zažene v primeru zrušitve
- upravlja prek `systemctl`, standardnega upravitelja storitev v sistemu Linux

### Datoteke za upravljanje storitve

Vse potrebne datoteke so v imeniku namestitve digna v: `bin/`

Na voljo so naslednji skripti lupine:

- `install_service.sh` — registrira digna pri systemd
- `uninstall_service.sh` — odstrani registracijo storitve
- `start_service.sh` — zažene registrirano storitev
- `stop_service.sh` — ustavi delujočo storitev

!!! warning "Zahtevane so pravice root"

    Vse skripte je treba izvajati s `sudo`, ker registracija storitve, ki se zažene ob zagonu sistema, zapiše datoteko enote v `/etc/systemd/system`.

### Naredite skripte izvršljive

Razpakiranje morda ne ohrani bita za izvajanje. Pred prvo uporabo:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Namestitev storitve

1. **Odprite terminal**

2. **Pojdite v mapo bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Zaženite namestitveni skript**
   ```bash
   sudo ./install_service.sh
   ```

Strežnik digna je zdaj registriran pri systemd z omogočenim **samodejnim zagonom**. Storitev se ne zažene takoj — kako jo zaženete, prikazuje naslednji razdelek.

### Zagon in ustavitev storitve

#### Za zagon storitve

1. Odprite terminal
2. Pojdite v `/opt/digna/bin`
3. Zaženite:
   ```bash
   sudo ./start_service.sh
   ```

#### Za ustavitev storitve

1. Odprite terminal
2. Pojdite v `/opt/digna/bin`
3. Zaženite:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Namig"

    Pred posodobitvijo datotek aplikacije storitev vedno ustavite.

### Upravljanje storitve s systemctl

Ko je storitev registrirana, jo lahko iz katerega koli imenika upravljate tudi s standardnimi ukazi systemd:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Preverjanje storitve

Za potrditev, da je storitev registrirana in teče:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` pomeni, da se storitev zažene ob zagonu sistema; `active` pomeni, da trenutno teče.

### Pregledovanje dnevnikov storitve

systemd zajame vse, kar backend izpiše v konzolo. Za branje:

```bash
sudo journalctl -u digna -n 100
```

Za sprotno spremljanje dnevnika med ponavljanjem težave:

```bash
sudo journalctl -u digna -f
```

!!! tip "Namig"

    To je najhitrejši način za diagnosticiranje storitve, ki se zažene in takoj ustavi. Tu je javljena napaka pri povezavi z repozitorijem ali manjkajoča datoteka `license.toml`.

### Premik storitve v nov imenik

Datoteka enote hrani absolutno pot do izvršljive datoteke, zato premestitev namestitve zahteva ponovno registracijo storitve:

1. **Odstranite trenutno storitev**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Premaknite datoteke aplikacije**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Znova namestite storitev**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Zaženite storitev**
   ```bash
   sudo ./start_service.sh
   ```

### Odstranitev storitve

1. **Ustavite delujočo storitev**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Odstranite storitev**
   ```bash
   sudo ./uninstall_service.sh
   ```

Strežnik digna zdaj ni več registriran pri systemd.

---

## Nadgradnja na novo izdajo {: #upgrading-to-a-new-release }

Ta razdelek opisuje nadgradnjo namestitve izdaje 2026.06 na izdajo 2026.11.

!!! warning "Nadgradnja z izdaje, starejše od 2026.06"

    Najprej izvedite korake nadgradnje izdaje 2026.06: [Nadgradnja na novo izdajo](../Release%202026.06/installation_guide_digna_linux_2026_06.md#upgrading-to-a-new-release). Nato nadaljujte s spodnjimi koraki.

### Pred nadgradnjo

**Varnostna kopija repozitorija digna je obvezna**

Pred nadgradnjo digna varnostno kopirajte svoj repozitorij (PostgreSQL), da se zaščitite pred izgubo podatkov. Varnostna kopija omogoča obnovitev, če pri nadgradnji pride do nepričakovanih težav.

Za ustvarjanje varnostne kopije iz lupine:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Pridobitev licenčne datoteke za izdajo 2026.11**

Izdaja 2026.11 potrebuje novo datoteko `license.toml`. Pred začetkom jo zahtevajte od ekipe digna in jo imejte pripravljeno za [korak 7](#step-7-replace-the-license-file).

### Postopek nadgradnje

#### Korak 1: Ustavite storitev digna {: #step-1-stop-the-digna-service }

Če digna teče kot storitev systemd, jo najprej ustavite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Če digna teče v ospredju, v njegovem oknu terminala pritisnite ++ctrl+c++.

#### Korak 2: Varnostno kopirajte trenutno namestitev {: #step-2-backup-current-installation }

V namestitvenem imeniku digna preimenujte izvršljivo datoteko in mapo nadzorne plošče trenutne namestitve, da bo novo izdajo mogoče namestiti ob njih:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

`digna_old` obdržite, dokler ne preverite nadgradnje, `dashboard_old` pa, dokler iz nje ne obnovite svojih konfiguracijskih datotek (glejte korak 4). Nato lahko oboje izbrišete.

#### Korak 3: Razpakirajte in razmestite novo različico {: #step-3-extract-and-deploy-new-version }

1. Razpakirajte novo ZIP datoteko namestitve digna
2. Novo izvršljivo datoteko `digna` in mapo `dashboard` kopirajte v svoj namestitveni imenik
3. Obnovite bit za izvajanje in lastništvo storitvenega računa:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Pomembno"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista nikoli vključena v namestitveni ZIP — ekipa digna nobene od teh datotek nikoli ne dostavi. Nadgradnja vaše obstoječe konfiguracije zato ne spremeni, kopije v preimenovanih mapah `*_old` pa so edine, ki jih imate.

#### Korak 4: Obnovite konfiguracijske datoteke {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Izdaja 2026.11 ne zahteva nobene spremembe datoteke `config.toml`: datoteka, ki deluje z izdajo 2026.06, deluje še naprej. Dve spremembi sta izbirni:

- Dodajte [sekcijo `[duckdb]`](#duckdb-section), če naj podatkovne povezave uporabljajo digna Engine in njegove privzete vrednosti ne ustrezajo vašemu gostitelju.
- Sekcijo `[app]` izpustite, če obratni posrednik streže nadzorno ploščo in backend pod enim izvorom.

!!! warning "Nastavitve, ki jih digna ne bere"

    Prejšnje različice tega vodiča so prikazovale nekatere nastavitve, ki jih digna ne bere. Nimajo nobenega učinka, `config check` pa jih v koraku 6 navede pod **Unknown keys**. Odstranite ali popravite jih:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`, `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` in `digna_LOGGING_BACKUP_COUNT` ne obstajajo. Odstranite jih.
    - Imena nastavitev razlikujejo med velikimi in malimi črkami. digna bere `DIGNA_REPO_HOST`, ne `digna_REPO_HOST`. Vsa imena zapišite z velikimi črkami, kot v razdelku [Konfiguracija backend‑a](#backend-configuration).

!!! warning "Enotna prijava: ohranite [[oidc_clients]]"

    digna ponudnike enotne prijave bere kot seznam vnosov `[[oidc_clients]]`, vsakega s svojim `DIGNA_OIDC_KEY`. Če ste svoje ponudnike spremenili v sekcije `[oidc_clients.<key>]`, kot je prikazovala prejšnja različica tega vodiča, jih spremenite nazaj. `config check` javi `OIDC config(s)` kot FAILED, dokler je v uporabi ta oblika:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Vnos ponovite za vsakega ponudnika in vsak `DIGNA_OIDC_KEY` ohranite enak vrednosti `key` v datoteki `dashboard_config.toml`. Prizadete so le namestitve, ki uporabljajo enotno prijavo.

#### Korak 5: Ponovno naložite spletni strežnik {: #step-5-reload-the-web-server }

Nadzorna plošča je nabor statičnih datotek, zato vaš spletni strežnik — in brskalnik — morda še vedno streže prejšnjo različico. Ponovno naložite ali znova zaženite spletni strežnik, ki gosti mapo `dashboard`, nato pa stran osvežite s trdim osveževanjem (++ctrl+f5++).

#### Korak 6: Preverite konfiguracijo {: #step-6-validate-the-configuration }

Preden se dotaknete repozitorija, potrdite, da je `config.toml` popoln:

```bash
./digna config check
```

Vsaka sekcija mora javiti OK. Odpravite vse, kar je javljeno kot FAILED, odstranite ključe, navedene pod **Unknown keys**, in pred nadaljevanjem ukaz zaženite znova.

#### Korak 7: Zamenjajte licenčno datoteko {: #step-7-replace-the-license-file }

Licenčna datoteka, izdana za prejšnjo izdajo, z izdajo 2026.11 ne deluje. Datoteko `license.toml`, ki vam jo je ekipa digna posredovala za izdajo 2026.11, kopirajte v imenik namestitve in z njo zamenjajte staro:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ne obdržite prejšnje licence"

    S prejšnjo licenco vsak ukaz, ki preverja licenco — `serve`, `user`, `inspection`, `repo` — ne uspe, zato se digna ne zažene in repozitorija ni mogoče nadgraditi. Preden nadaljujete, preverite novo licenco:

    ```bash
    ./digna license check
    ```

#### Korak 8: Nadgradite shemo repozitorija {: #step-8-upgrade-the-repository-schema }

V imeniku namestitve digna zaženite:

```bash
cd /opt/digna
./digna repo upgrade
```

Izdaja 2026.11 shemo repozitorija upravlja z verzioniranimi migracijami. Prva nadgradnja s prejšnje izdaje shemo pripelje na zadnjo različico prejšnjega sistema, to zabeleži kot izhodišče in nato uporabi migracije izdaje 2026.11. Konča se z:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Vsi obstoječi podatki se ohranijo. Stanje repozitorija lahko kadar koli preverite z ukazom `./digna repo check`: navede zadnjo uporabljeno migracijo in morebitne čakajoče.

!!! warning "digna se ne zažene na zastarelem repozitoriju"

    Od izdaje 2026.11 se strežnik ne zažene, dokler repozitorij potrebuje nadgradnjo, in to tudi sporoči, na primer:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Pred zagonom strežnika ali storitve zaženite `repo upgrade`.

#### Korak 9: Znova zaženite storitve {: #step-9-restart-services }

Če digna teče kot storitev systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Če digna poganjate ročno, znova zaženite strežnik:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Če uporabljate nginx ali Apache, ponovno naložite ustrezni spletni strežnik:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

V družini RHEL znova uveljavite oznake SELinux, če je bil imenik `dashboard` zamenjan:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Korak 10: Preverite nadgradnjo {: #step-10-verify-the-upgrade }

1. Preverite izdajo nove izvršljive datoteke:

    ```bash
    ./digna version
    ```

    Prva vrstica se mora glasiti `Release: 2026.11`.

2. Odprite nadzorno ploščo digna in preverite, ali se vmesnik pravilno naloži.
3. V dnevnikih strežnika preverite, ali so se pojavile napake:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Preizkusite svoje podatkovne povezave — glejte [Preizkušanje povezave](../../../databases/overview.md#testing-a-connection).

Za začetek dela z novimi moduli glejte [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Povezava agenta AI](../../../platform/agentic/connect_ai_agent.md) za digna MCP Server in [Lokacija profiliranja](../../../platform/profiling/profiling_location.md) za digna Engine.