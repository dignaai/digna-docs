# Navodila za namestitev na Linux za digna izdajo 2026.06

**Izdaja:** 2026.06

**Zadnja posodobitev:** 5. september 2026


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

### Novosti v izdaji 2026.06

Ta izdaja prinaša zmogljivosti opazovanja podatkov neposredno v vašo kodo, kar razvijalcem omogoča spremljanje kakovosti podatkov pri izvoru. Za popolne podrobnosti si oglejte [opombe ob izdaji](http://docs.digna.ai/changelog/Release_202606/).

### Iščete Windows ali macOS?

Ta vodič pokriva Linux. Za druge platforme si oglejte [navodila za namestitev na Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ali [navodila za namestitev na macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

Ta sekcija konfigurira nastavitve aplikacije backend digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontenda | Če je nadzorna plošča na drugem strežniku, vključite njen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Zahtevano za CORS s poverilnicami |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Dovoli vse metode HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Dovoli vse glave |

!!! note "Opomba"

    Če nadzorno ploščo strežete prek nginx ali Apache na privzetih vratih HTTP, je izvor, ki ga je treba dovoliti, `http://localhost` — ali javni URL strežnika, kadar do nadzorne plošče dostopajo drugi stroji.

#### Sekcija [repo]

Ta sekcija konfigurira povezavo s PostgreSQL bazo podatkov:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_REPO_HOST` | `localhost` ali IP | Ime gostitelja/IP PostgreSQL strežnika |
| `digna_REPO_PORT` | `5432` (privzeto) | Vrata PostgreSQL |
| `digna_REPO_DB` | `postgres` | Ime baze podatkov |
| `digna_REPO_SCHEMA` | `dignarepo` | Prej ustvarjena shema |
| `digna_REPO_USER` | `digna_user` | Uporabnik, ustvarjen pri nastavitvi PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše geslo | Geslo, nastavljeno ob ustvarjanju sheme |

!!! tip "Najboljša praksa"

    `config.toml` vsebuje geslo baze podatkov v navadnem besedilu. Omejite njegova dovoljenja, tako da ga lahko bere le storitveni račun:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### Sekcija [base]

Ta sekcija vsebuje varnostne nastavitve in nastavitve piškotkov:

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

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Ujemati se mora z domeno vašega frontenda |
| `digna_COOKIE_SECURE` | `false` (lokalno) / `true` (produkcija) | Za povezave HTTPS uporabite `true` |
| `digna_COOKIE_HTTPONLY` | `true` | Zaradi varnosti vedno omogočeno |
| `digna_COOKIE_SAME_SITE` | `lax` | Preprečuje napade CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ur) | Čas poteka seje v sekundah |
| `digna_MAX_WORKERS` | Število jeder CPU - 1 | Število vzporednih nalog pregledov |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Največja zakasnitev v sekundah, ki jo sme razporejevalnik dodati pred zagonom zapadlega opravila |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Ura dneva (24-urni zapis `HH:MM`), ob kateri se začne dnevno čiščenje |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ali `DEBUG` | `INFO` za produkcijo, `DEBUG` za odpravljanje težav |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Število dnevnih varnostnih kopij dnevnikov, ki se hranijo |

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

Overall: OK
```

Odpravite vse, kar je javljeno kot FAILED, in pred nadaljevanjem ukaz zaženite znova. Celoten seznam možnosti najdete v [referenci CLI](../../../cli/Command_Line_Interface_202606.md).

### Korak 3: Inicializirajte repozitorij

1. Odprite terminal
2. Pojdite v imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)
3. Zaženite test povezave:

```bash
cd /opt/digna
./digna repo check
```

Videti bi morali potrditev, da je povezava vzpostavljena (sam repozitorij še ni inicializiran).

!!! note "Opomba"

    V sistemu Linux trenutni imenik ni v vašem PATH, zato se izvršljiva datoteka kliče kot `./digna` namesto `digna`. Če želite krajšo obliko uporabljati povsod, dodajte simbolno povezavo:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Korak 4: Namestite shemo repozitorija

V istem imeniku zaženite:

```bash
./digna repo install
```

Ta ukaz namesti potrebne tabele in shemo v vašo PostgreSQL bazo podatkov.

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
- `--address` — ime gostitelja/IP strežnika
- `--port` — vrata strežnika

Videti bi morali začetna sporočila, ki potrjujejo, da strežnik teče:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
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

### Pred nadgradnjo

**Najprej preverite vse podatkovne povezave**

Od izdaje 2026.06 digna do vsake izvorne tehnologije dostopa prek **ODBC**. Prejšnje izdaje
so ponujale izbiro med gonilnikom za posamezno tehnologijo in ODBC, izbrano s stikalom **Use ODBC**.
Ekipa digna se je odločila graditi izključno na ODBC, ker en sam standardni vmesnik ponuja
več kot nabor gonilnikov po meri:

- **Preverjanje pristnosti** — preverjanje pristnosti je del ODBC, zato lahko povezava uporabi vse, kar
  podpira njen gonilnik: gesla, žetone in PAT-e, Kerberos in Active Directory, MFA in enotno prijavo
  prek brskalnika, identitete v oblaku, odjemalska potrdila in TLS. Nove metode pridejo s posodobitvijo
  gonilnika, namesto da bi čakali na izdajo digna.
- **Gonilniki, ki jih vzdržujejo proizvajalci podatkovnih baz** — proizvajalčev lastni gonilnik sledi novim
  različicam strežnika in varnostnim popravkom, vi pa ga lahko posodabljate po svojem urniku, neodvisno od digna.
- **En sam način nastavljanja vsega** — vsaka tehnologija je seznam lastnosti ključ/vrednost, z
  istim vmesnikom, istim šifriranjem občutljivih vrednosti in istim odpravljanjem težav,
  namesto drugačnega nabora polj za vsak vir.
- **Nastavljanje in doseg** — možnosti na ravni gonilnika, kot so časovne omejitve, nastavitve TLS, posredniški strežniki in velikosti
  prenosa, so na voljo za vsak vir, priključiti pa je mogoče vsako tehnologijo s skladnim gonilnikom ODBC,
  tudi takšno, za katero digna ne objavlja lastnega vodnika.

V praksi to pomeni, da stikala **Use ODBC** ter ločenih polj za gostitelja, vrata, bazo, uporabnika in
geslo ni več. **Vsako povezavo, ki še ne uporablja ODBC, je treba preklopiti
na ODBC** — samodejne pretvorbe ni, zato to načrtujte pred nadgradnjo:

1. Preglejte vsako podatkovno povezavo, opredeljeno v vaši namestitvi, in si zapišite tiste, ki
   še ne uporabljajo ODBC — vsako od njih bo treba znova nastaviti.
2. Na gostitelja digna namestite ustrezen gonilnik ODBC — povezave se odpirajo s strežnika,
   na katerem teče backend digna, in ne iz brskalnika. Glejte
   [Namestitev gonilnika ODBC na gostitelja digna](../../../databases/overview.md#install-the-driver).
3. Za vsako prizadeto povezavo pripravite lastnosti ODBC.
   [Vodniki po tehnologijah](../../../databases/overview.md#technology-guides) za vsak vir navajajo preizkušen
   nabor lastnosti.

Po nadgradnji vsako prizadeto povezavo preklopite na ODBC in jo preizkusite z nadzorne plošče —
glejte [Ustvarjanje podatkovne povezave](../../../databases/overview.md#create-a-database-connection)
in [Preizkušanje povezave](../../../databases/overview.md#testing-a-connection).

!!! warning "Povezave Databricks Legacy"

    Konektor Databricks Legacy je bil v tej izdaji odstranjen. Te povezave preselite
    na konektor [Databricks](../../../databases/databricks_connector_guide.md).

**Varnostna kopija repozitorija digna je obvezna**

Pred nadgradnjo digna varnostno kopirajte svoj repozitorij (PostgreSQL), da se zaščitite pred izgubo podatkov.
Varnostna kopija omogoča obnovitev, če pri nadgradnji pride do nepričakovanih težav.

Za ustvarjanje varnostne kopije iz lupine:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Postopek nadgradnje

#### Korak 1: Ustavite storitev digna

Če digna teče kot storitev systemd, jo najprej ustavite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Če digna teče v ospredju, v njegovem oknu terminala pritisnite `Ctrl + C`.

#### Korak 2: Varnostno kopirajte trenutno namestitev

V namestitvenem imeniku digna preimenujte mape trenutne namestitve, da bo novo izdajo mogoče namestiti ob njih:

```bash
cd /opt/digna
sudo mv dignabackend dignabackend_old
```
```bash
sudo mv dignacli dignacli_old
```
```bash
sudo mv dashboard dashboard_old
```

!!! info "dignabackend in dignacli nista več v uporabi"

    Od izdaje 2026.06 `dignabackend` in `dignacli` nadomešča ena sama izvršljiva datoteka `digna`, ki združuje backend in CLI. Mapi `dignabackend_old` in `dignacli_old` obdržite le, dokler ne preverite nadgradnje — nato ju lahko obe izbrišete. Mapo `dashboard_old` obdržite, dokler iz nje ne obnovite svojih konfiguracijskih datotek (glejte korak 4).

#### Korak 3: Razpakirajte in razmestite novo različico

1. Razpakirajte novo ZIP datoteko namestitve digna
2. Novo izvršljivo datoteko `digna` in mapo `dashboard` kopirajte v svoj namestitveni imenik
3. Obnovite bit za izvajanje in lastništvo storitvenega računa:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Pomembno"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista **nikoli** vključena v
    namestitveni ZIP — ekipa digna nobene od teh datotek nikoli ne dostavi. Nadgradnja vaše obstoječe
    konfiguracije zato ne spremeni, kopije v preimenovanih mapah `*_old` pa so edine, ki jih imate.

#### Korak 4: Obnovite konfiguracijske datoteke

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

!!! warning "Izdaja 2026.06 spreminja config.toml"

    Tri nastavitve so nove in obvezne, tri pa niso več v uporabi. `config.toml`, prenesen iz prejšnje izdaje, novih nastavitev ne vsebuje in digna se ne bo zagnala, dokler manjkajo. V obstoječi `config.toml` dodajte naslednje:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Dva ključa `[base]` dodajte v svojo obstoječo sekcijo `[base]`, sekcijo `[encryption]` pa dodajte kot novo. Nato odstranite nastavitve, ki niso več v uporabi: **`digna_FERNET_KEY`** iz `[base]` ter **`digna_APP_HOST`** in **`digna_APP_PORT`** iz `[app]` — naslov in vrata strežnik zdaj dobi iz `digna serve`.

    Kaj počne posamezna nastavitev, je opisano v razdelku [Konfiguracija backend‑a](#backend-configuration).

!!! warning "Enotna prijava: oblika [oidc_clients] se je spremenila"

    Izdaja 2026.06 nadomesti polje tabel z eno tabelo na ponudnika, poimenovano po
    ključu ponudnika. `DIGNA_OIDC_KEY` odpade — ključ je zdaj del glave sekcije.

    Prej:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Potem:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Sekcijo ponovite za vsakega ponudnika in vsak ključ ohranite enak vrednosti `key` v
    datoteki `dashboard_config.toml`. `digna config check` javi `oidc_clients` kot FAILED, dokler
    ostaja stara oblika. Prizadete so le namestitve, ki uporabljajo enotno prijavo.

#### Korak 5: Ponovno naložite spletni strežnik

Nadzorna plošča je nabor statičnih datotek, zato vaš spletni strežnik — in brskalnik — morda še vedno
streže prejšnjo različico. Ponovno naložite ali znova zaženite spletni strežnik, ki gosti mapo `dashboard`,
nato pa stran osvežite s trdim osveževanjem (++ctrl+f5++).

#### Korak 6: Preverite konfiguracijo

Preden se dotaknete repozitorija, potrdite, da je posodobljeni `config.toml` popoln:

```bash
./digna config check
```

Vsaka sekcija mora javiti OK. Odpravite vse, kar je javljeno kot FAILED, in pred nadaljevanjem ukaz zaženite znova.

#### Korak 7: Zamenjajte licenčno datoteko

Vsaka izdaja je licencirana ločeno. Datoteko `license.toml`, ki vam jo je ekipa digna posredovala za
to izdajo, kopirajte v imenik namestitve in z njo zamenjajte staro:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ne obdržite prejšnje licence"

    Datoteka `license.toml`, izdana za prejšnjo izdajo, ne velja za to, in vsak ukaz, ki preverja
    licenco — `user`, `inspection`, `repo` — se prekine, še preden se dotakne repozitorija, če
    preverjanje ne uspe. Preden nadaljujete, jo preverite:

    ```bash
    ./digna license check
    ```

#### Korak 8: Nadgradite shemo repozitorija

Pojdite v imenik namestitve digna in zaženite:

```bash
cd /opt/digna
./digna repo upgrade
```

To posodobi PostgreSQL shemo na najnovejšo različico, pri tem pa ohrani vse obstoječe podatke.

#### Korak 9: Znova zaženite storitve

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

#### Korak 10: Preverite nadgradnjo

1. Dostopite do nadzorne plošče digna
2. Preverite, ali se vmesnik pravilno naloži
3. V dnevnikih strežnika preverite, ali so se pojavile napake
4. Vsako povezavo, ki še ni uporabljala ODBC, preklopite na ODBC, nato preizkusite vse povezave
   — glejte [Preizkušanje povezave](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```