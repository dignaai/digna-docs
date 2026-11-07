# Navodila za namestitev na macOS za digna izdajo 2026.11

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
9. [Zagon digna kot ozadnega servisa](#running-digna-as-a-background-service)
10. [Nadgradnja na novo izdajo](#upgrading-to-a-new-release)

---

## Uvod {: #introduction }

### O digna

digna je celovita platforma, vodena z umetno inteligenco, namenjena optimizaciji upravljanja kakovosti podatkov v različnih podatkovnih okoljih, kot so podatkovni skladi, podatkovna jezera in lakehouse‑i. Zasnovana je za visoko skalabilnost in prilagodljivost ter rešuje sodobne izzive podatkov s pomočjo avtomatizacije, spremljanja v realnem času in odkrivanja anomalij.

digna sestavljata dve glavni komponenti:

- **digna**: jedro aplikacije, odgovorno za obdelavo podatkov in izvajanje preverjanj kakovosti. Združuje zaledni del in vmesnik ukazne vrstice v eno samo izvršljivo datoteko ter nadomešča ločena programa `dignabackend` in `dignacli` iz prejšnjih izdaj.
- **dignadashboard**: spletni vmesnik gostovan na spletnem strežniku, ki omogoča enostavno interakcijo s platformo digna in vizualizacijo meritev kakovosti podatkov.

### Novosti v izdaji 2026.11

Ta izdaja dodaja digna Data Reconciliation, digna Agentic z digna MCP Server in digna Engine, ki lahko profilira podatke znotraj digna in preverja referenčno integriteto med različnimi tehnologijami podatkovnih baz. Za popolne podrobnosti si oglejte [opombe ob izdaji](../../../changelog/Release_202611.md).

Pri namestitvi izdaja prinaša nov mehanizem migracij repozitorija, izbirno sekcijo `[duckdb]` v `config.toml` za digna Engine in novo licenčno datoteko. Vse to pokriva [razdelek o nadgradnji](#upgrading-to-a-new-release).

### Iščete Windows ali Linux?

Ta vodič pokriva macOS. Za druge platforme si oglejte [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) ali [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Podatkovne povezave, ki kot lokacijo profiliranja uporabljajo digna Engine, se profilirajo na samem gostitelju digna. Zanje načrtujte dodaten pomnilnik in prostor na disku, glejte [sekcijo \[duckdb\]](#duckdb-section).

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

!!! info "Konfiguracijskih in licenčnih datotek ni v paketu"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista priložena namestitvi — obe
    ustvarite sami, v razdelkih [Konfiguracija backend‑a](#backend-configuration) in
    [Konfiguracija nadzorne plošče](#dashboard-configuration). Tudi `license.toml` ni priložena;
    digna jo posreduje ločeno, kot opisuje Korak 3.

Za razširitev iz Terminala:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
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

    Če strežete nadzorno ploščo iz Homebrew‑ovega nginx na privzetem priključku, je izvor, ki ga je treba dovoliti, `http://localhost:8080`.

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

    Za ugotovitev števila CPU jeder na vašem Macu zaženite `sysctl -n hw.ncpu`.

#### Sekcija [encryption]

Ta sekcija vsebuje ključ, s katerim so šifrirane občutljive vrednosti v repozitoriju. Je **obvezna** — `config check` sekcijo `[encryption]` javi kot FAILED, če ključ manjka.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Ključ, kodiran v Base64 | Šifrira občutljive vrednosti, shranjene v repozitoriju digna |

!!! warning "Zaščitite config.toml"

    Ta ključ je fiksna vrednost, enaka v vseh namestitvah digna, in prav on dešifrira občutljive vrednosti v vašem repozitoriju. Dostop do `config.toml` omejite na račun, pod katerim teče digna, datoteko hranite zunaj sistema za nadzor različic in deljenih diskov ter jo izključite iz vsake varnostne kopije, ki je shranjena manj varno kot repozitorij sam.

#### Sekcija [logging]

Ta sekcija konfigurira vedenje beleženja:

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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Privzeto: sistemski začasni imenik (`$TMPDIR` računa, pod katerim teče digna) | Imenik za začasne datoteke, kadar podatki ne gredo v pomnilnik |

!!! tip "Dimenzioniranje digna Engine"

    Načrtujte do `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` pomnilnika na gostitelju digna, poleg tega, kar porabi digna sama, ter dovolj prostega prostora na disku v začasnem imeniku za največji pregledani datum virov podatkov, ki uporabljajo digna Engine. `DIGNA_DUCKDB_TEMP_DIRECTORY` usmerite na disk s tem prostorom, v katerega lahko piše račun, pod katerim teče digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    To sekcijo potrebujete le, če vsaj ena podatkovna povezava uporablja digna Engine ali če preverjanje referenčne integritete primerja vire podatkov na različnih povezavah.

---

### Korak 2: Preverjanje Konfiguracije

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

1. Odprite **Terminal**
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

    Na macOS‑u ukazi v trenutnem imeniku niso v vašem PATH, zato se izvršljiva datoteka kliče kot `./digna` namesto `digna`. Če želite krajšo obliko uporabljati povsod, dodajte imenik namestitve v PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
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

    Geslo zavijte v enojne navednice. `zsh` obravnava znake kot `!`, `$` in `*` posebej, zato nezavito geslo, ki jih vsebuje, ne bo poslano tako, kot ste ga vnesli.

!!! tip "Najboljša praksa"

    Uporabite močno geslo z mešanico velikih in malih črk, številk in posebnih znakov.

---

### Korak 6: Zaženite digna strežnik

V imeniku namestitve digna zaženite strežnik z:

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

    Ob prvem zagonu strežnika vas lahko macOS vpraša, ali želite, da aplikacija sprejema dohodne omrežne povezave. Kliknite **Allow**, sicer nadzorna plošča ne bo mogla doseči backend‑a.

!!! note "Strežnik zaseda terminal"

    `serve` teče v ospredju in deluje, dokler ga ne ustavite s ++ctrl+c++. Pustite ga teči, dokler ne dokončate namestitve; če naj se namesto tega samodejno zaganja ob zagonu sistema, glejte [Zagon digna kot Storitve v Ozadju](#running-digna-as-a-background-service).

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Korak 1: Razmestitev nadzorne plošče na spletni strežnik

Nadzorna plošča digna prebere svojo konfiguracijo iz datoteke `dashboard/dashboard_config.toml`. Ta datoteka ni priložena namestitvi — ustvarite jo v imeniku `dashboard/` poleg datotek nadzorne plošče.

Njena vsebina je opisana v razdelku [Enotna prijava (SSO)](../../../sso/overview.md), kjer je datoteka tudi potrebna: vsebuje možnosti prijave, ki jih ponuja nadzorna plošča, in pri večinstančnih nameščanjih povezavo na backend.

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

Ta razdelek nadgradi namestitev izdaje 2026.06 na izdajo 2026.11. Če je vaša namestitev starejša, najprej preberite [Nadgradnja z izdaje pred 2026.06](#upgrading-from-a-release-before-2026-06).

### Pred nadgradnjo

**Varnostna kopija repozitorija digna je obvezna**

Pred nadgradnjo digna varnostno kopirajte svoj repozitorij (PostgreSQL), da se zaščitite pred izgubo podatkov. Varnostna kopija omogoča obnovitev, če pri nadgradnji pride do nepričakovanih težav.

Za ustvarjanje varnostne kopije iz aplikacije Terminal:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Pridobitev licenčne datoteke za izdajo 2026.11**

Izdaja 2026.11 potrebuje novo datoteko `license.toml`. Pred začetkom jo zahtevajte od ekipe digna in jo imejte pripravljeno za [korak 7](#step-7-replace-the-license-file).

### Nadgradnja z izdaje pred 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Izdaja 2026.06 je prinesla tri spremembe, ki še vedno veljajo, kadar starejšo namestitev nadgradite neposredno na 2026.11:

- **Samo ODBC.** digna do vsake izvorne tehnologije dostopa prek ODBC. Vsako podatkovno povezavo, ki še ne uporablja ODBC, je treba po nadgradnji preklopiti na ODBC; samodejne pretvorbe ni. Gonilnike ODBC na gostitelja digna namestite vnaprej, glejte [Namestitev gonilnika ODBC na gostitelja digna](../../../databases/overview.md#install-the-driver), lastnosti vsake povezave pa imejte pripravljene iz [vodnikov po tehnologijah](../../../databases/overview.md#technology-guides). Konektor Databricks Legacy ne obstaja več; te povezave preselite na konektor [Databricks](../../../databases/databricks_connector_guide.md).
- **Ena izvršljiva datoteka.** `dignabackend` in `dignacli` nadomešča ena sama izvršljiva datoteka `digna`, ki združuje backend in CLI.
- **config.toml.** Sekcija `[encryption]` je obvezna, `DIGNA_APP_HOST` in `DIGNA_APP_PORT` pa se ne bereta več: naslov in vrata strežnik dobi iz `digna serve`. Svojo datoteko primerjajte z razdelkom [Konfiguracija backend‑a](#backend-configuration).

Spodnji koraki opozarjajo, kje starejša namestitev potrebuje kaj drugačnega. Nadgradnja repozitorija v koraku 8 repozitorij katere koli prejšnje izdaje pripelje neposredno na 2026.11.

### Postopek nadgradnje

#### Korak 1: Ustavite storitev digna {: #step-1-stop-the-digna-service }

Če digna teče kot storitev v ozadju, jo najprej ustavite:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Če digna teče v ospredju, v njegovem oknu Terminal pritisnite ++ctrl+c++.

#### Korak 2: Varnostno kopirajte trenutno namestitev {: #step-2-backup-current-installation }

V namestitvenem imeniku digna preimenujte izvršljivo datoteko in mapo nadzorne plošče trenutne namestitve, da bo novo izdajo mogoče namestiti ob njih:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

`digna_old` obdržite, dokler ne preverite nadgradnje, `dashboard_old` pa, dokler iz nje ne obnovite svojih konfiguracijskih datotek (glejte korak 4). Nato lahko oboje izbrišete.

!!! info "Nadgradnja z izdaje pred 2026.06"

    Namesto izvršljive datoteke preimenujte mapi `dignabackend` in `dignacli`: `mv dignabackend dignabackend_old` in `mv dignacli dignacli_old`. Izdaja 2026.11 ne uporablja nobene od njiju.

#### Korak 3: Razpakirajte in razmestite novo različico {: #step-3-extract-and-deploy-new-version }

1. Razpakirajte novo ZIP datoteko namestitve digna
2. Novo izvršljivo datoteko `digna` in mapo `dashboard` kopirajte v svoj namestitveni imenik
3. Obnovite bit za izvajanje in po potrebi odstranite atribut karantene:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Pomembno"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista nikoli vključena v namestitveni ZIP — ekipa digna nobene od teh datotek nikoli ne dostavi. Nadgradnja vaše obstoječe konfiguracije zato ne spremeni, kopije v preimenovanih mapah `*_old` pa so edine, ki jih imate.

#### Korak 4: Obnovite konfiguracijske datoteke {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

Nadzorna plošča je nabor statičnih datotek, zato vaš spletni strežnik — in brskalnik — morda še vedno streže prejšnjo različico. Ponovno naložite ali znova zaženite spletni strežnik, ki gosti mapo `dashboard`, nato pa stran osvežite s trdim osveževanjem (++cmd+shift+r++).

#### Korak 6: Preverite konfiguracijo {: #step-6-validate-the-configuration }

Preden se dotaknete repozitorija, potrdite, da je `config.toml` popoln:

```bash
./digna config check
```

Vsaka sekcija mora javiti OK. Odpravite vse, kar je javljeno kot FAILED, odstranite ključe, navedene pod **Unknown keys**, in pred nadaljevanjem ukaz zaženite znova.

#### Korak 7: Zamenjajte licenčno datoteko {: #step-7-replace-the-license-file }

Licenčna datoteka se običajno prenese iz ene izdaje v naslednjo. Izdaja 2026.11 je izjema: dodaja dva licencirana modula, digna Data Reconciliation in digna Agentic, licenca, izdana pred 2026.11, pa ju ne vsebuje. Datoteko `license.toml`, ki vam jo je ekipa digna posredovala za izdajo 2026.11, kopirajte v imenik namestitve in z njo zamenjajte staro:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ne obdržite prejšnje licence"

    S prejšnjo licenco se digna še vedno zažene, vendar digna Data Reconciliation in digna MCP Server ostaneta izklopljena. Vsak ukaz, ki preverja licenco — `user`, `inspection`, `repo` — se prekine, še preden se dotakne repozitorija, če preverjanje ne uspe. Preden nadaljujete, preverite novo licenco:

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

Če digna teče kot storitev v ozadju:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Če digna poganjate ročno, znova zaženite strežnik:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Če uporabljate nginx ali Apache, znova zaženite ustrezni spletni strežnik:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Korak 10: Preverite nadgradnjo {: #step-10-verify-the-upgrade }

1. Preverite izdajo nove izvršljive datoteke:

    ```bash
    ./digna version
    ```

    Prva vrstica se mora glasiti `Release: 2026.11`.

2. Odprite nadzorno ploščo digna in preverite, ali se vmesnik pravilno naloži.
3. V izpisu strežnika in v datotekah v imeniku `logs` preverite, ali so se pojavile napake.
4. Preizkusite svoje podatkovne povezave — glejte [Preizkušanje povezave](../../../databases/overview.md#testing-a-connection). Po nadgradnji z izdaje pred 2026.06 najprej vsako povezavo, ki še ni uporabljala ODBC, preklopite na ODBC.

Za začetek dela z novimi moduli glejte [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Povezava agenta AI](../../../platform/agentic/connect_ai_agent.md) za digna MCP Server in [Lokacija profiliranja](../../../platform/profiling/profiling_location.md) za digna Engine.