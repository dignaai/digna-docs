# Navodila za namestitev na macOS za digna izdajo 2026.06

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
9. [Zagon digna kot ozadnega servisa](#running-digna-as-a-background-service)
10. [Nadgradnja na novo izdajo](#upgrading-to-a-new-release)

---

## Uvod {: #introduction }

### O digna

digna je celovita platforma, vodena z umetno inteligenco, namenjena optimizaciji upravljanja kakovosti podatkov v različnih podatkovnih okoljih, kot so podatkovni skladi, podatkovna jezera in lakehouse‑i. Zasnovana je za visoko skalabilnost in prilagodljivost ter rešuje sodobne izzive podatkov s pomočjo avtomatizacije, spremljanja v realnem času in odkrivanja anomalij.

digna sestavljata dve glavni komponenti:

- **dignabackend**: jedro aplikacije, odgovorno za obdelavo podatkov in izvajanje preverjanj kakovosti.
- **dignadashboard**: spletni vmesnik gostovan na spletnem strežniku, ki omogoča enostavno interakcijo s platformo digna in vizualizacijo meritev kakovosti podatkov.

### Novosti v izdaji 2026.06

Ta izdaja prinaša zmogljivosti opazovanja podatkov neposredno v vašo kodo, kar razvijalcem omogoča spremljanje kakovosti podatkov pri izvoru. Za popolne podrobnosti si oglejte [opombe ob izdaji](http://docs.digna.ai/changelog/Release_202606/).

### Iščete Windows ali Linux?

Ta vodič pokriva macOS. Za druge platforme si oglejte [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ali [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Sistemske zahteve {: #system-requirements }

Preden začnete z namestitvijo, se prepričajte, da vaš sistem izpolnjuje naslednje minimalne zahteve:

| Zahteva | Specifikacija |
|---|---|
| **Operacijski sistem** | macOS 13 (Ventura) ali novejši |
| **Arhitektura** | Apple Silicon (arm64) ali Intel (x86_64) |
| **Pomnilnik (minimalna namestitev)** | 16 GB RAM |
| **Prostor na disku** | 10 GB razpoložljivega prostora |
| **Baza podatkov** | PostgreSQL Server 12 ali novejši |
| **Spletni strežnik** | nginx, Apache httpd ali ekvivalent |
| **Orodja ukazne vrstice** | Xcode Command Line Tools (zahtevano za Homebrew) |

### Možnosti namestitve baze podatkov

**Če je PostgreSQL že nameščen:**
Lahko dodate novo bazo za digna v obstoječi PostgreSQL strežnik.

**Če nameščate PostgreSQL na isti stroj kot digna:**

!!! info "Priporočene specifikacije"

    - **Pomnilnik**: 32 GB RAM (namesto 16 GB)
    - **Prostor na disku**: 50 GB razpoložljivega prostora (namesto 10 GB)

    Te višje specifikacije omogočajo hkratno delovanje digna in PostgreSQL baze na istem stroju.

### Preverjanje arhitekture

Nekateri poti v tem vodiču se razlikujejo za Apple Silicon in Intel Mac‑e. Da preverite, katero imate, odprite **Terminal** in zaženite:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew se namesti v `/opt/homebrew`.
- `x86_64` — Intel. Homebrew se namesti v `/usr/local`.

!!! tip "Namig"

    Namesto trdega kodiranja ene od poti ta vodič uporablja `$(brew --prefix)`, ki se razširi na pravilno lokacijo na obeh arhitekturah. Ukaze lahko kopirate nespremenjene.

---

## Prednamestitvena priprava {: #pre-installation-setup }

Pred namestitvijo digna poskrbite, da so prisotni trije ključni predpogoji:

1. **Homebrew** – paketni upravljalnik, uporabljen za namestitev spodnjih komponent
2. **PostgreSQL Server** – za shranjevanje izračunanih metrik in podatkov o zmogljivosti
3. **Spletni strežnik** – za gostovanje digna Dashboarda

Če ti sestavni delci še niso nastavljeni, sledite spodnjim razdelkom za namestitev in konfiguracijo.

### Namestitev Homebrew

Homebrew je standardni upravljalnik paketov za macOS in se v celotnem vodiču uporablja za namestitev PostgreSQL in nginx.

#### Korak 1: Preverite, ali je Homebrew že nameščen

Odprite **Terminal** (pritisk `Cmd + Space`, vnesite `Terminal`, pritisnite Enter) in zaženite:

```bash
brew --version
```

Če je prikazana številka različice, preskočite na razdelek [Nastavitev PostgreSQL strežnika](#postgresql-server-setup).

#### Korak 2: Namestite Homebrew

Če ukaz ni najden, namestite Homebrew po navodilih na [uradni strani Homebrew](https://brew.sh). Namestitveni program namesti tudi Xcode Command Line Tools, če še niso prisotni.

#### Korak 3: Dodajte Homebrew v svojo PATH

Na Apple Silicon instalator izpiše dva ukaza za dodajanje Homebrew v vaše okolje lupine. Zaženite jih po navodilih, nato potrdite:

```bash
brew --prefix
```

To bi moralo izpisati `/opt/homebrew` na Apple Silicon ali `/usr/local` na Intel.

---

## Nastavitev PostgreSQL strežnika {: #postgresql-server-setup }

### Če že imate PostgreSQL

Če je PostgreSQL že nameščen in teče na lokalnem stroju ali če uporabljate upravljan oddaljen PostgreSQL strežnik, lahko preskočite na [naslednji razdelek](#web-server-configuration).

### Možnosti namestitve

macOS ponuja dva preprosta načina za namestitev PostgreSQL. Izberite **eno**:

- [Homebrew](#postgresql-homebrew) — namestitev prek ukazne vrstice, priporočena za strežniške namestitve
- [Postgres.app](#postgresql-app) — grafična namestitev, priročna za lokalno evalvacijo

### Namestitev PostgreSQL z Homebrew {: #postgresql-homebrew }

#### Korak 1: Namestite formulo PostgreSQL

```bash
brew install postgresql@16
```

#### Korak 2: Dodajte PostgreSQL v svojo PATH

Verzionirane formule PostgreSQL so *keg-only*, kar pomeni, da Homebrew njihovih ukazov samodejno ne poveže v vaš PATH. Dodajte jih sami:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Opomba"

    To predvideva privzeto lupino `zsh`, ki jo uporablja macOS. Če uporabljate `bash`, dodajte isto vrstico v `~/.bash_profile`.

#### Korak 3: Zaženite storitev PostgreSQL

```bash
brew services start postgresql@16
```

To takoj zažene PostgreSQL in ga nastavi, da se ob prijavi samodejno ponovno zažene.

#### Korak 4: Preverite namestitev

```bash
psql --version
```

Če je namestitev uspela, boste videli različico PostgreSQL.

#### Korak 5: Povežite se s strežnikom

```bash
psql postgres
```

!!! warning "Pomembno — macOS se tu razlikuje od Windows"

    Namestitveni program za Windows vas pozove k ustvarjanju superuporabnika `postgres` in gesla. Homebrew tega ne stori. Namesto tega ustvari superuporabnika z imenom vašega **macOS računa**, brez gesla, dostopnega le z lokalnega stroja.

    To pomeni, da na sveži Homebrew namestitvi ni vloge `postgres`. Uporabite svoje uporabniško ime, kadar potrebujete superuporabnika, in ustvarite izrecnega digna uporabnika, kot je opisano v [Začetni namestitvi](#initial-installation).

#### Korak 6: Potrdite vrata

Privzeta pristanišče PostgreSQL je `5432`. Za potrditev, na katerem priključku strežnik posluša:

```bash
psql postgres -c "SHOW port;"
```

Zabeležite vrednost — potrebovali jo boste pri konfiguraciji digna backend‑a.

### Namestitev PostgreSQL z aplikacijo Postgres.app {: #postgresql-app }

Če imate raje grafični vmesnik:

1. Prenesite [Postgres.app](https://postgresapp.com) in ga povlecite v mapo **Applications**
2. Odprite aplikacijo in kliknite **Initialize**, da ustvarite nov strežnik
3. Sledite navodilom aplikacije za dodajanje njenih orodij ukazne vrstice v vaš PATH
4. Preverite namestitev:

```bash
psql --version
```

Postgres.app prav tako ustvari superuporabnika z imenom vašega macOS računa.

---

## Konfiguracija spletnega strežnika {: #web-server-configuration }

digna zahteva spletni strežnik za gostovanje nadzorne plošče. Izberite eno od naslednjih možnosti:

- [nginx](#nginx-setup) — nameščen prek Homebrew, priporočeno
- [Apache httpd](#apache-setup) — vključen v macOS

Potrebujete le namestitev in konfiguracijo **enega** izmed teh strežnikov.

Oba razdelka konfigurirata dve stvari, od katerih je odvisna nadzorna plošča:

- **Počasen fallback za enostransko aplikacijo (SPA)**, tako da osvežitev URL‑ja nadzorne plošče ne povzroči 404
- **MIME tip za `.md`**, da se Markdown datoteke strežejo pravilno

### Nastavitev nginx {: #nginx-setup }

#### Pregled

nginx je lahek, zmogljiv spletni strežnik, primeren za streženje statične digna nadzorne plošče.

#### Namestitev

```bash
brew install nginx
```

#### Zagon nginx

```bash
brew services start nginx
```

#### Preverjanje namestitve

1. Odprite brskalnik
2. Pojdite na `http://localhost:8080`
3. Videzite pozdravno stran nginx

!!! note "Opomba — privzeto priključek je 8080, ne 80"

    Homebrew konfigurira nginx, da posluša na priključku `8080`, da lahko teče brez administratorskih pravic. Na macOS‑u vezanje na priključek `80` ali katerikoli drug priključek pod 1024 zahteva root.

    Če želite streči nadzorno ploščo na priključku 80, spremenite `listen 8080;` v `listen 80;` v spodnji konfiguraciji in zaženite nginx z `sudo brew services start nginx`.

#### Konfiguracija mesta za nadzorno ploščo

Homebrew‑ova konfiguracija nginx vključi vse datoteke v imeniku `servers`. Ustvarite namensko konfiguracijsko datoteko za digna tam:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Prilepite naslednje in zamenjajte `/path/to/digna/dashboard` z dejansko potjo do razširjene mape `dashboard`:

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

!!! warning "Pomembno"

    Brez direktive `try_files` osvežitev katere koli strani nadzorne plošče, razen korenskega URL‑ja, vrne 404. To je ekvivalent URL Rewrite modula, potrebnega za IIS na Windows.

#### Uveljavitev konfiguracije

Preverite konfiguracijo za sintaktične napake, nato ponovno naložite nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Nastavitev Apache httpd {: #apache-setup }

#### Pregled

macOS vključuje Apache httpd, zato namestitev ni potrebna. Privzeto je onemogočen.

#### Zagon Apache

```bash
sudo apachectl start
```

#### Preverjanje namestitve

1. Odprite brskalnik
2. Pojdite na `http://localhost`
3. Videli boste sporočilo "It works!"

#### Obvezno: omogočite mod_rewrite

Nadzorna plošča zahteva prepisovanje URL‑jev. Odprite Apache konfiguracijo:

```bash
sudo nano /etc/apache2/httpd.conf
```

Poiščite naslednjo vrstico in odstranite vodilni `#`, da jo odkomentirate:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Obvezno: dovolite .htaccess preglasitve

V isti datoteki poiščite blok `<Directory "/Library/WebServer/Documents">` in spremenite:

```apache
AllowOverride None
```

v:

```apache
AllowOverride All
```

#### Obvezno: MIME tip za Markdown datoteke

Še v `httpd.conf` dodajte naslednjo vrstico, da se Markdown datoteke strežejo pravilno:

```apache
AddType text/markdown .md
```

!!! warning "Pomembno"

    Brez te nastavitve se `.md` datoteke morda ne bodo strele pravilno.

#### Uveljavitev konfiguracije

Preverite konfiguracijo za sintaktične napake, nato ponovno zaženite Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Začetna namestitev {: #initial-installation }

### Korak 1: Nastavite digna repozitorij

Repozitorij digna hrani vse meritve, izračunane z digna. Deluje kot centralna baza za analitične in zmogljivostne podatke.

#### Ustvarite shemo repozitorija in uporabnika

Odprite svoj PostgreSQL odjemalec (psql, pgAdmin ali podoben) in izvedite naslednje SQL ukaze:

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

Za izvedbo teh ukazov iz Terminala v enem koraku:

```bash
psql postgres
```

Nato prilepite izjave na poziv `postgres=#` in vtipkajte `\q`, da zapustite.

!!! tip "Najboljša praksa"

    Uporabljajte močna, kompleksna gesla za uporabnike baze podatkov. Izogibajte se lahko ugibljivim poverilnicam.

---

### Korak 2: Razširite namestitveni paket digna

1. Poiščite ZIP datoteko namestitvenega paketa digna, ki vam je bila posredovana
2. Razširite jo na želeno lokacijo namestitve — na primer `/opt/digna` ali `~/digna`
3. Po razširitvi bi morali videti naslednje elemente:
   - `dashboard/` — spletni vmesnik nadzorne plošče
   - `digna` — glavni izvršljivi program (backend + CLI skupaj)
   - `config.toml` — konfiguracijska datoteka
   - `license.toml` — licenčna datoteka (kopirajte svojo sem)

Za razširitev iz Terminala:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Dovolite zagon izvršljive datoteke

Glede na način prenosa se izvršljiva bit morda ne ohrani. Nastavite ga izrecno:

```bash
cd /opt/digna
chmod +x digna
```

#### Če macOS blokira aplikacijo

Datoteke, prenesene prek brskalnika ali pošiljatelja, imajo lahko priponko karantene. Če macOS poroča, da aplikacije *"ni mogoče odpreti, ker razvijalca ni mogoče preveriti"*, odstranite atribut iz namestitvenega imenika:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativno odprite **System Settings → Privacy & Security**, poiščite blokirano postavko blizu dna strani in kliknite **Open Anyway**.

!!! note "Opomba"

    Ta korak je potreben le, če macOS dejansko blokira izvršljivo datoteko. Paketi, preneseni preko SSH ali iz notranjih deljenih map, običajno niso v karanteni.

### Korak 3: Namestite licenčno datoteko

!!! warning "Pomembno"

    Licenčna datoteka ni vključena v namestitveni paket in vam bo posredovana ločeno s strani digna.

1. Poiščite `license.toml` datoteko, ki vam je bila posredovana
2. Kopirajte jo v korenski imenik namestitve digna (kjer se nahajata `config.toml` in izvršljiva datoteka `digna`)

**Zakaj je to pomembno:**
Licenčna datoteka vsebuje informacije o stranki, datum poteka licence in digitalni podpis. **Ne spreminjajte te datoteke** — vsaka sprememba jo bo razveljavila.

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

V namestitvenem imeniku digna je priložena datoteka `config_template.toml`. Preimenujete jo v `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Lokacija:** `/opt/digna/config.toml`

Odprite `config.toml` v urejevalniku besedil in konfigurirajte vsak spodnji odsek.

#### Sekcija [app]

Ta sekcija konfigurira nastavitve digna backend aplikacije:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_APP_HOST` | `localhost` ali IP naslov | Ime gostitelja ali IP, kjer je gostovan dignabackend |
| `digna_APP_PORT` | `8082` (privzeto) | Pristanišče za REST API končne točke |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontenda | Če je nadzorna plošča na drugem strežniku, vključite njen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Zahtevano za CORS z poverilnicami |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Dovoli vse HTTP metode |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Dovoli vse glave |

!!! note "Opomba"

    Če strežete nadzorno ploščo iz Homebrew‑ovega nginx na privzetem priključku, je izvor, ki ga je treba dovoliti, `http://localhost:8080`.

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
| `digna_REPO_PORT` | `5432` (privzeto) | Pristanišče PostgreSQL |
| `digna_REPO_DB` | `postgres` | Ime baze podatkov |
| `digna_REPO_SCHEMA` | `dignarepo` | Shema, ustvarjena prej |
| `digna_REPO_USER` | `digna_user` | Uporabnik, ustvarjen v nastavitvi PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše geslo | Geslo nastavljeno med ustvarjanjem sheme |

#### Sekcija [base]

Ta sekcija vsebuje varnostne nastavitve in nastavitve piškotkov:

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

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_FERNET_KEY` | Ključ za šifriranje | Uporablja se za šifriranje žetonov in piškotkov (privzeto priložen) |
| `digna_COOKIE_DOMAIN` | `localhost` | Ujemanje z domeno vašega frontenda |
| `digna_COOKIE_SECURE` | `false` (lokalno) / `true` (produkcija) | Uporabite `true` za HTTPS povezave |
| `digna_COOKIE_HTTPONLY` | `true` | Vedno omogočeno zaradi varnosti |
| `digna_COOKIE_SAME_SITE` | `lax` | Zmanjša tveganje CSRF napadov |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ure) | Čas poteka seje v sekundah |
| `digna_MAX_WORKERS` | Število CPU jeder - 1 | Število vzporednih nalog inšpekcij |

!!! tip "Namig"

    Za ugotovitev števila CPU jeder na vašem Macu zaženite `sysctl -n hw.ncpu`.

#### Sekcija [logging]

Ta sekcija konfigurira vedenje beleženja:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ali `DEBUG` | `INFO` za produkcijo, `DEBUG` za odpravljanje težav |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Število dnevnih varnostnih kopij dnevnikov za hranjenje |

---

### Korak 2: Inicializirajte repozitorij

1. Odprite **Terminal**
2. Pojdite v imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)
3. Zaženite test povezave:

```bash
cd /opt/digna
./digna repo check
```

Videli boste potrditev, da je povezava vzpostavljena (sam repozitorij še ni inicializiran).

!!! note "Opomba"

    Na macOS‑u ukazi v trenutnem imeniku niso v vašem PATH, zato se izvršljiva datoteka kliče kot `./digna` namesto `digna`. Če želite krajšo obliko uporabljati povsod, dodajte imenik namestitve v PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Korak 3: Namestite shemo repozitorija

V istem imeniku zaženite:

```bash
./digna repo install
```

Ta ukaz namesti potrebne tabele in shemo v vašo PostgreSQL bazo podatkov.

### Korak 4: Zaženite digna strežnik

V imeniku namestitve digna zaženite strežnik z:

```bash
./digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — ime gostitelja/IP strežnika
- `--port` — pristanišče strežnika

Videli boste začetna sporočila, ki potrjujejo zagon strežnika:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Namig"

    Ob prvem zagonu strežnika vas lahko macOS vpraša, ali želite, da aplikacija sprejema dohodne omrežne povezave. Kliknite **Allow**, sicer nadzorna plošča ne bo mogla doseči backend‑a.

### Korak 5: Ustvarite skrbniškega uporabnika

1. Odprite **novo** okno Terminala
2. Pojdite v imenik namestitve digna
3. Zaženite naslednji ukaz za ustvarjanje skrbniškega uporabnika:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Primer:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

To ustvari uporabnika z uporabniškim imenom `admin` in polnimi skrbniškimi pravicami.

!!! tip "Namig"

    Geslo zavijte v enojne navednice. `zsh` obravnava znake kot `!`, `$` in `*` posebej, zato nezavito geslo, ki jih vsebuje, ne bo poslano tako, kot ste ga vnesli.

!!! tip "Najboljša praksa"

    Uporabite močno geslo z mešanico velikih in malih črk, številk in posebnih znakov.

---

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Korak 1: Razmestitev nadzorne plošče na spletni strežnik

Nadzorna plošča digna ima svojo ločeno datoteko `config.toml` v imeniku `dashboard/`. Ta konfiguracija je že priložena in med začetno namestitvijo običajno ni potrebna sprememba. Konfigurirate jo le, če želite prilagoditi povezavo na backend ali pri večinstančnih nameščanjih.

Če morate spremeniti konfiguracijo nadzorne plošče, si oglejte dokumentacijo nadzorne plošče.

Izberite spletni strežnik in sledite ustreznim korakom za namestitev.

#### Razmestitev na nginx

Če ste sledili razdelku [nginx Setup](#nginx-setup), strežniški blok že kaže na vašo mapo `dashboard` in kopiranje ni potrebno.

1. **Potrdite pot**
   - Odprite `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Preverite, da `root` kaže na vašo razširjeno mapo `dashboard`

2. **Poskrbite, da je mapa berljiva**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Ponovno naložite nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Preizkus namestitve**
   - Odprite brskalnik
   - Pojdite na `http://localhost:8080` (ali vaš konfigurirani URL)
   - Videti bi morali prijavno stran digna nadzorne plošče

#### Razmestitev na Apache httpd

1. **Kopirajte nadzorno ploščo v Document Root**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Dodajte pravila za prepisovanje**

   Ustvarite `.htaccess` datoteko v razmestjeni mapi, da poti nadzorne plošče preživijo osvežitev brskalnika:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
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

3. **Ponovno zaženite Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Dostop do nadzorne plošče**
   - Odprite brskalnik
   - Pojdite na `http://localhost/digna`
   - Videli bi morali prijavno stran digna nadzorne plošče

---

## Zagon digna kot ozadnega servisa {: #running-digna-as-a-background-service }

### Zakaj zagnati digna kot storitev?

Zagon digna backend‑a kot ozadnega servisa zagotavlja, da se:

- začne samodejno ob zagonu sistema
- teče v ozadju brez odprtega Terminal okna
- samodejno ponovno zažene v primeru zrušitve
- upravlja preko `launchctl`, upravitelja storitev macOS

### Datoteke za upravljanje storitve

Vse potrebne datoteke so v imeniku namestitve digna v: `bin/`

Na voljo so naslednji shell skripti:

- `install_service.sh` — registrira digna pri launchd
- `uninstall_service.sh` — odstrani registracijo storitve
- `start_service.sh` — zažene registrirano storitev
- `stop_service.sh` — ustavi tekočo storitev

!!! warning "Zahteva skrbniške pravice"

    Vse skripte je treba izvajati z `sudo`, ker registracija storitve, ki se zažene ob zagonu, zapisuje v `/Library/LaunchDaemons`.

### Naredite skripte izvršljive

Pri razširitvi morda izvršljiv bit ni ohranjen. Pred prvo uporabo:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Namestitev storitve

1. **Odprite Terminal**

2. **Pojdite v mapo bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Zaženite namestitveni skript**
   ```bash
   sudo ./install_service.sh
   ```

digna strežnik je zdaj registriran pri launchd z omogočenim **samodejnim zagonom**. Storitve se ne zažene neposredno — naslednji razdelek prikazuje, kako jo zagnati.

### Zagon in ustavitev storitve

#### Za zagon storitve

1. Odprite Terminal
2. Pojdite v `/opt/digna/bin`
3. Zaženite:
   ```bash
   sudo ./start_service.sh
   ```

#### Zaustavitev storitve

1. Odprite Terminal
2. Pojdite v `/opt/digna/bin`
3. Zaženite:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Namig"

    Pred posodobitvijo datotek aplikacije vedno ustavite storitev.

### Preverjanje storitve

Za potrditev, da je storitev registrirana in teče:

```bash
sudo launchctl list | grep digna
```

Vrstica, ki se začne s procesnim ID‑jem, pomeni, da storitev teče. `-` v prvem stolpcu pomeni, da je registrirana, a ustavljena.

### Premik storitve v nov imenik

launchd shrani absolutno pot do izvršljive datoteke, zato premestitev namestitve zahteva ponovno registracijo storitve:

1. **Odstranite obstoječo storitev**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Premaknite aplikacijske datoteke**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Ponovno namestite storitev**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Zaženite storitev**
   ```bash
   sudo ./start_service.sh
   ```

### Odstranitev storitve

1. **Ustavite tekočo storitev**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Odstranite storitev**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna strežnik je sedaj odregistriran pri launchd.

---

## Nadgradnja na novo izdajo {: #upgrading-to-a-new-release }

### Pred nadgradnjo

**Obvezno ustvarite varnostno kopijo digna repozitorija**

Pred nadgradnjo digna varnostno kopirajte vaš repozitorij (PostgreSQL), da se zaščitite pred izgubo podatkov.
Varnostna kopija omogoča obnovitev, če pride pri nadgradnji do nepričakovanih težav.

Za ustvarjanje varnostne kopije iz Terminala:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Postopek nadgradnje

#### Korak 1: Ustavite digna storitev

Če digna teče kot ozadna storitev, jo najprej ustavite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Če digna teče v ospredju, pritisnite `Ctrl + C` v Terminal oknu, kjer teče.

#### Korak 2: Varnostno kopirajte trenutno backend namestitev

V imeniku namestitve digna:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Korak 3: Razširite in razmestite novo različico

1. Razširite nov namestitveni ZIP paket digna
2. Kopirajte nov izvršljiv `digna` in mapo `dashboard` v imenik namestitve
3. Obnovite izvršljivi bit in po potrebi odstranite atribut karantene:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Pomembno"

    Datoteka `config.toml` **nikoli** ni vključena v namestitveni ZIP. Vaša obstoječa konfiguracija ostane varna.

### Korak 4: Obnovite konfiguracijske datoteke

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Korak 5: Nadgradite shemo repozitorija

Pojdite v imenik namestitve digna in zaženite:

```bash
cd /opt/digna
./digna repo upgrade
```

To posodobi PostgreSQL shemo na najnovejšo različico ob ohranitvi vseh obstoječih podatkov.

### Korak 6: Ponovni zagon storitev

Če tečete kot ozadna storitev:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Če tečete ročno, ponovno zaženite strežnik:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Če uporabljate nginx ali Apache, ponovno zaženite ustrezen spletni strežnik:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Korak 7: Preverite nadgradnjo

1. Dostopajte do digna nadzorne plošče
2. Preverite, ali se vmesnik naloži pravilno
3. Preverite dnevniške datoteke strežnika za morebitne napake