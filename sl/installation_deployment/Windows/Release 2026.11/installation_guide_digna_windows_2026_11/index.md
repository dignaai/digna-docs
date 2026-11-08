# Vodnik za namestitev na Windows za digna Release 2026.11

**Release:** 2026.11

**Zadnja posodobitev:** 7. novembra 2026


---

## Vsebina

1. [Uvod](#introduction)
2. [Sistemske zahteve](#system-requirements)
3. [Predpriprava pred namestitvijo](#pre-installation-setup)
4. [Namestitev PostgreSQL strežnika](#postgresql-server-setup)
5. [Konfiguracija spletnega strežnika](#web-server-configuration)
6. [Začetna namestitev](#initial-installation)
7. [Konfiguracija backenda](#backend-configuration)
8. [Konfiguracija nadzorne plošče](#dashboard-configuration)
9. [Poganjanje digna kot Windows storitve](#running-digna-as-a-windows-service)
10. [Nadgradnja na novo izdajo](#upgrading-to-a-new-release)

---

## Uvod {: #introduction }

### O digna

digna je celovita AI-podprta platforma zasnovana za optimizacijo upravljanja kakovosti podatkov v različnih podatkovnih okoljih, kot so podatkovni skladi, jezera in lakehouse rešitve. Zasnovana je za visoko skalabilnost in prilagodljivost ter rešuje sodobne podatkovne izzive s pomočjo avtomatizacije, spremljanja v realnem času in odkrivanja anomalij.

digna je sestavljena iz dveh glavnih komponent:

- **digna**: jedro aplikacije, odgovorno za obdelavo podatkov in izvajanje preverjanj kakovosti. Združuje zaledni del in vmesnik ukazne vrstice v eno samo izvršljivo datoteko ter nadomešča ločena programa `dignabackend` in `dignacli` iz prejšnjih izdaj.
- **dignadashboard**: Spletni vmesnik gostovan na spletnem strežniku, ki omogoča uporabnikom prijazen način interakcije s platformo digna in vizualizacijo metrik kakovosti podatkov.

### Novosti v izdaji 2026.11

Ta izdaja dodaja digna Data Reconciliation, digna Agentic z digna MCP Server in digna Engine, ki lahko profilira podatke znotraj digna in preverja referenčno integriteto med različnimi tehnologijami podatkovnih baz. Za popolne podrobnosti si oglejte [opombe ob izdaji](../../../changelog/Release_202611.md).

Pri namestitvi izdaja prinaša nov mehanizem migracij repozitorija, izbirno sekcijo `[duckdb]` v `config.toml` za digna Engine in novo licenčno datoteko. Vse to pokriva [razdelek o nadgradnji](#upgrading-to-a-new-release).

### Iščete macOS ali Linux?

Ta vodič zajema Windows. Za druge platforme si oglejte [Vodnik za namestitev na macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) ali [Vodnik za namestitev na Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Sistemske zahteve {: #system-requirements }

Pred začetkom namestitve se prepričajte, da vaš sistem izpolnjuje naslednje minimalne zahteve:

| Zahteva | Specifikacija |
|---|---|
| **Operacijski sistem** | Windows Server ali Windows 10/11 |
| **Pomnilnik (minimalna konfiguracija)** | 16 GB RAM |
| **Prostor na disku** | 10 GB prostega prostora |
| **Baza podatkov** | PostgreSQL Server 12 ali novejši |
| **Spletni strežnik** | IIS, Apache Tomcat ali ekvivalent |

!!! info "digna Engine"

    Podatkovne povezave, ki kot lokacijo profiliranja uporabljajo digna Engine, se profilirajo na samem gostitelju digna. Zanje načrtujte dodaten pomnilnik in prostor na disku, glejte [sekcijo \[duckdb\]](#duckdb-section).

### Možnosti namestitve baze podatkov

**Če je PostgreSQL že nameščen:**
Lahko dodate novo podatkovno bazo za digna na obstoječ PostgreSQL strežnik.

**Če nameščate PostgreSQL na isti stroj kot digna:**

!!! info "Priporočene specifikacije"

    - **Pomnilnik**: 32 GB RAM (namesto 16 GB)
    - **Prostor na disku**: 50 GB prostega prostora (namesto 10 GB)

    Te višje specifikacije omogočajo sočasno delovanje digna in PostgreSQL baze na istem strežniku.

---

## Predpriprava pred namestitvijo {: #pre-installation-setup }

Pred namestitvijo digna se prepričajte, da sta izpolnjeni dve ključni predpogoji:

1. **PostgreSQL Server** – za shranjevanje izračunanih metrik in podatkov o zmogljivosti
2. **Spletni strežnik** – za gostovanje digna Dashboard

Če ti komponenti še nista nameščeni, sledite spodnjim poglavjem za namestitev in konfiguracijo.

---

## Namestitev PostgreSQL strežnika {: #postgresql-server-setup }

### Če že imate PostgreSQL

Če je PostgreSQL že nameščen in teče na vašem lokalnem stroju ali uporabljate upravljan oddaljeni PostgreSQL strežnik, lahko preskočite na [naslednji razdelek](#web-server-configuration).

### Namestitev PostgreSQL

Sledite tem korakom za namestitev PostgreSQL na Windows:

#### Korak 1: Prenesite PostgreSQL

1. Obiščite [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Izberite **Windows**
3. Prenesite najnovejši namestitveni program

#### Korak 2: Zaženite namestitveni program

1. Dvokliknite preneseno namestitveno datoteko
2. Sledite navodilom v čarovniku za namestitev

#### Korak 3: Izberite imenik za namestitev

Izberite imenik, kamor bo PostgreSQL nameščen. Privzeta lokacija je običajno primerna.

#### Korak 4: Izberite komponente

Za standardno namestitev pustite privzete možnosti komponent.

#### Korak 5: Nastavite geslo PostgreSQL superuporabnika

Vnesite in potrdite geslo za PostgreSQL superuporabnika (`postgres`). **Shranjeno geslo varno** — potreben bo pozneje.

#### Korak 6: Konfiguracija številke vrat

Privzeta vrata PostgreSQL so `5432`. Lahko uporabite privzeto ali določite drugačna vrata po potrebi.

!!! tip "Nasvet"

    Če so vrata 5432 že v uporabi, izberite alternativna vrata in si jih zabeležite za kasnejšo konfiguracijo.

#### Korak 7: Izberite jezikovno nastavitev (locale)

Izberite locale za vašo bazo podatkov. Privzeta nastavitev je običajno primerna za večino namestitev.

#### Korak 8: Dokončajte namestitev

Kliknite **Next** skozi preostale korake, nato kliknite **Finish**.

#### Korak 9: Preverite namestitev

Odprite Command Prompt in preverite, ali je PostgreSQL nameščen:

```bash
psql --version
```

Če je namestitev uspešna, boste videli prikaz različice PostgreSQL.

---

## Konfiguracija spletnega strežnika {: #web-server-configuration }

digna zahteva spletni strežnik za gostovanje nadzorne plošče. Izberite eno od naslednjih možnosti:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Potrebno je namestiti in konfigurirati le enega izmed teh strežnikov.

### Nastavitev IIS {: #iis-setup }

#### Pregled

Internet Information Services (IIS) je Microsoftov spletni strežnik za gostovanje spletnih mest in spletnih aplikacij.

#### Omogočanje IIS

1. **Odprite Nadzorno ploščo**
   - Pritisnite `Win + R`
   - Vnesite `control` in pritisnite Enter

2. **Pojdite na Windows Features**
   - Kliknite **Programs**
   - Izberite **Turn Windows features on or off**

3. **Omogočite Internet Information Services**
   - Pomaknite se navzdol in poiščite **Internet Information Services (IIS)**
   - Označite polje za omogočanje
   - Kliknite na **+**, da razširite in preverite, da so izbrane te podkomponente:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Kliknite OK** za uporabo sprememb

5. **Preverite namestitev IIS**
   - Odprite brskalnik
   - Pojdite na `http://localhost`
   - Morali bi videti IIS Welcome stran

#### Obvezno: URL Rewrite modul

IIS zahteva komponento URL Rewrite. Prenesite in namestite jo s [uradne Microsoft strani](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Obvezno: MIME tip za Markdown datoteke

Da se Markdown datoteke (`.md`) pravilno servirajo prek IIS:

1. Odprite **IIS Manager** (pritisnite `Win + R`, vnesite `inetmgr`, pritisnite Enter)
2. Pomaknite se do **Your Site > MIME Types**
3. Kliknite **Add...**
4. Konfigurirajte:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Pomembno"

    Brez te nastavitve se datoteke `.md` morda ne bodo pravilno servirale.

---

### Nastavitev Apache Tomcat {: #apache-tomcat-setup }

#### Pregled

Apache Tomcat je odprtokodni Java servlet container in spletni strežnik.

#### Namestitev

1. **Prenesite Apache Tomcat**
   - Obiščite [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Prenesite Windows ZIP distribucijo

2. **Razpakirajte arhiv**
   - Razpakirajte ZIP datoteko v imenik na vašem sistemu
   - Primer: `C:\Program Files\Apache Tomcat`

3. **Preverite, ali Tomcat teče**
   - Odprite brskalnik
   - Pojdite na `http://localhost:8080`
   - Videti bi morali Apache Tomcat welcome stran

!!! tip "Nasvet"

    Apache Tomcat se običajno samodejno zažene po namestitvi. Če se ne zažene, pojdite v mapo `bin` in zaženite `startup.bat`.

---

## Začetna namestitev {: #initial-installation }

### Korak 1: Nastavite digna repozitorij

Digna repozitorij shranjuje vse metrike, ki jih izračuna digna. Deluje kot centralna baza za analitične in podatke o zmogljivosti.

#### Ustvarite shemo repozitorija in uporabnika

Odprite svoj PostgreSQL klient (pgAdmin, psql ali podoben) in izvedite naslednje SQL ukaze:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Zamenjajte naslednje nadomestke:**

- `<digna_repo_schema>` — Ime sheme po vaši želji (npr. `dignarepo`)
- `<digna_repo_user>` — Želeno uporabniško ime (npr. `digna_user`)
- `<digna_repo_password>` — Varno geslo za tega uporabnika

**Primer:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Najboljša praksa"

    Uporabljajte močna, kompleksna gesla za uporabnike baze podatkov. Izogibajte se lahko ugotovljivim poverilnicam.

---

### Korak 2: Razpakirajte namestitveni paket digna

1. Poiščite ZIP datoteko z namestitvijo digna, ki vam je bila posredovana
2. Razpakirajte jo na želeno lokacijo za namestitev
3. Po razpakiranju bi morali videti naslednje elemente:
   - `dashboard/` — Spletni vmesnik nadzorne plošče
   - `digna` — Glavna izvršljiva datoteka (backend + CLI skupaj)

!!! info "Konfiguracijskih in licenčnih datotek ni v paketu"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista priložena namestitvi — obe
    ustvarite sami, v razdelkih [Konfiguracija backenda](#backend-configuration) in
    [Konfiguracija nadzorne plošče](#dashboard-configuration). Tudi `license.toml` ni priložena;
    digna jo posreduje ločeno, kot opisuje Korak 3.

### Korak 3: Namestite licenčno datoteko

!!! warning "Pomembno"

    Licenčna datoteka ni vključena v namestitveni paket in vam bo posredovana ločeno s strani digna.

1. Poiščite datoteko `license.toml`, ki vam je bila posredovana
2. Kopirajte jo v root imenik namestitve digna (kjer se nahajata `config.toml` in izvršljiva datoteka `digna`)

**Zakaj je to pomembno:**
Licenčna datoteka vsebuje vaše podatke o stranki, datum poteka licence in digitalni podpis. **Ne spreminjajte te datoteke** — sprememba bo veljavnost licenčne datoteke razveljavila.

**Struktura imenikov po nastavitvi:**

```
digna_installation/
├── config.toml         (konfiguracijska datoteka)
├── license.toml        (VAŠA LICENČNA DATOTEKA - kopirajte sem)
├── digna               (glavna izvršljiva datoteka)
└── dashboard/          (spletni vmesnik)
    └── (datoteke nadzorne plošče)
```

---

## Konfiguracija backenda {: #backend-configuration }

### Korak 1: Ustvarite in uredite konfiguracijsko datoteko

Datoteka `config_template.toml` je priložena v vaši namestitveni mapi digna. Potrebno jo je le preimenovati v `config.toml`.

**Lokacija:** `digna_installation/config.toml`

Odprite `config.toml` v besedilnem urejevalniku in konfigurirajte spodnje razdelke.

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

!!! info "Sekcija [app] je izbirna"

    Od izdaje 2026.11 lahko oba ključa in celotno sekcijo `[app]` izpustite. To je prava nastavitev, kadar obratni posrednik (reverse proxy) streže nadzorno ploščo in backend pod enim izvorom: brskalnik takrat ne pošilja zahtev med izvori, privzeto pa nobena ni dovoljena.

#### Sekcija [repo]

Ta sekcija konfigurira povezavo na PostgreSQL bazo:

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

Ta sekcija konfigurira vedenje beleženja (logging):

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

!!! warning "Pri zagonu kot storitev ohranite imenik dnevnikov"

    Storitev Windows nima konzole, zato so dnevniške datoteke edini zapis o tem, kaj storitev počne. `DIGNA_LOGGING_DIR` ne nastavite na prazen niz, saj to izklopi dnevniške datoteke.

#### Sekcija [duckdb] (izbirno) {: #duckdb-section }

Novo v izdaji 2026.11. Ta sekcija določa vire za **digna Engine**, ki profilira podatke znotraj digna za podatkovne povezave, katerih lokacija profiliranja je **digna Engine**, in izvaja preverjanja referenčne integritete med viri podatkov na različnih podatkovnih povezavah. Glejte [Lokacija profiliranja](../../../platform/profiling/profiling_location.md).

Sekcija je izbirna. Brez nje veljajo spodnje privzete vrednosti.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (privzeto) | Pomnilnik v MB, ki ga sme porabiti en zagon digna Engine. Hkrati je lahko aktivnih do `DIGNA_MAX_WORKERS` zagonov |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Privzeto: začasni imenik računa, pod katerim teče digna (`%TEMP%`) | Imenik za začasne datoteke, kadar podatki ne gredo v pomnilnik |

!!! tip "Dimenzioniranje digna Engine"

    Načrtujte do `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` pomnilnika na gostitelju digna, poleg tega, kar porabi digna sama, ter dovolj prostega prostora na disku v začasnem imeniku za največji pregledani datum virov podatkov, ki uporabljajo digna Engine. `DIGNA_DUCKDB_TEMP_DIRECTORY` usmerite na disk s tem prostorom, v katerega lahko piše račun, pod katerim teče digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    To sekcijo potrebujete le, če vsaj ena podatkovna povezava uporablja digna Engine ali če preverjanje referenčne integritete primerja vire podatkov na različnih povezavah.

---

### Korak 2: Preverjanje Konfiguracije

Pred inicializacijo repozitorija preverite, ali je `config.toml` popoln in pravilno sestavljen. V namestitvenem imeniku digna zaženite:

```bash
digna config check
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

1. Odprite Command Prompt
2. Pomaknite se v imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)
3. Zaženite test povezave:

```bash
digna repo check
```

Na novi shemi se ukaz poveže in nato javi, da repozitorij še ni nameščen:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Na tej točki je to pričakovani rezultat: potrjuje, da digna doseže PostgreSQL in shemo. Napaka pri povezavi ali preverjanju pristnosti pa kaže na sekcijo `[repo]` ali na nastavitev PostgreSQL.

### Korak 4: Namestite shemo repozitorija

V istem imeniku zaženite:

```bash
digna repo upgrade
```

Ta ukaz namesti potrebne tabele v shemo repozitorija in se konča z:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade namešča in nadgrajuje"

    Od izdaje 2026.11 `repo upgrade` namesti nov repozitorij in nadgradi obstoječega. `repo install` še vedno deluje kot drugo ime za isti ukaz.

### Korak 5: Ustvarite administratorskega uporabnika

Skrbniški uporabnik se ustvari neposredno v shemi repozitorija, zato strežniku še ni treba teči. V imeniku namestitve digna zaženite:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Primer:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

S tem ustvarite uporabnika s polnimi administracijskimi pravicami.

!!! tip "Najboljša praksa"

    Uporabite močno geslo z mešanico velikih in malih črk, številk in posebnih znakov.

---

### Korak 6: Zaženite digna strežnik

V imeniku namestitve digna zaženite strežnik z:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — ime gostitelja/IP strežnika (privzeto `127.0.0.1`)
- `--port` — vrata strežnika (privzeto `8000`)

Ko strežnik teče, izpiše naslov, na katerem posluša:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Strežnik zaseda terminal"

    `serve` teče v ospredju in deluje, dokler ga ne ustavite s ++ctrl+c++. Pustite ga teči, dokler ne dokončate namestitve; če naj se namesto tega samodejno zaganja ob zagonu sistema, glejte [Zagon digna kot Storitve Windows](#running-digna-as-a-windows-service).

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Korak 1: Namestite nadzorno ploščo na spletni strežnik

Nadzorna plošča digna prebere svojo konfiguracijo iz datoteke `dashboard/dashboard_config.toml`. Ta datoteka ni priložena namestitvi — ustvarite jo v mapi `dashboard/` poleg datotek nadzorne plošče.

Njena vsebina je opisana v razdelku [Enotna prijava (SSO)](../../../sso/overview.md), kjer je datoteka tudi potrebna: vsebuje možnosti prijave, ki jih ponuja nadzorna plošča, in pri večinstančnih namestitvah povezavo na backend.

Izberite spletni strežnik in sledite ustreznim korakom namestitve.

#### Namestitev na IIS

1. **Odprite IIS Manager**
   - Pritisnite `Win + R`, vnesite `inetmgr`, pritisnite Enter

2. **Ustvarite novo spletno mesto**
   - V levem panelu desni klik na **Sites**
   - Izberite **Add Website...**

3. **Konfigurirajte spletno mesto**
   - **Site Name**: Vnesite ime (npr. "dignaDashboard")
   - **Physical Path**: Kliknite Browse in izberite mapo `dashboard`
   - **Binding**: Nastavite IP naslov in vrata (privzeta vrata 80 za HTTP, 443 za HTTPS)

4. **Zaženite spletno mesto**
   - Kliknite **OK**, da ustvarite spletno mesto
   - Desni klik na novo spletno mesto in izberite **Start**

5. **Preizkusite namestitev**
   - Odprite brskalnik
   - Pojdite na `http://localhost` (ali na vaš konfiguriran URL)
   - Prikazati bi se morala prijavna stran digna nadzorne plošče

#### Namestitev na Apache Tomcat

1. **Kopirajte nadzorno ploščo v Tomcat**
   - Kopirajte mapo `dashboard` v Tomcatovo mapo `webapps`
   - Po potrebi jo preimenujte (npr. v `digna`)
   - Primer: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Preverite namestitev**
   - Osvežite ali ponovno naložite Tomcat upravljalno stran (http://localhost:8080)
   - Morali bi videti "digna" (ali izbrano ime) na seznamu nameščenih aplikacij

3. **Dostop do nadzorne plošče**
   - Odprite brskalnik
   - Pojdite na `http://localhost:8080/digna`
   - Prikazati bi se morala prijavna stran digna nadzorne plošče

---

## Poganjanje digna kot Windows storitve {: #running-digna-as-a-windows-service }

### Zakaj uporabljati Windows storitev?

Poganjanje digna backenda kot Windows storitve zagotavlja:
- Samodejni zagon ob zagonu strežnika
- Delovanje v ozadju brez odprtega Command Prompt
- Samodejno ponovni zagon v primeru izpada
- Upravljanje preko Windows Services

### Ukazi `windows`

Storitev upravlja sama izvršljiva datoteka `digna`, s podukazi `digna windows`.
Batch datotek za zagon ni.

| Ukaz | Namen |
|---|---|
| `digna windows install` | Registrira digna kot Windows storitev |
| `digna windows start` | Zažene registrirano storitev |
| `digna windows stop` | Ustavi delujočo storitev |
| `digna windows uninstall` | Odstrani registracijo storitve |

!!! warning "Potrebne so administratorske pravice"

    Vse štiri ukaze je treba zagnati iz Command Prompt, odprtega kot administrator.

Vsak ukaz sprejme `--name`, s katerim naslovite storitev, registrirano pod imenom, ki ni privzeto. Celoten
seznam možnosti je v [referenci CLI](../../../cli/Command_Line_Interface_202611.md).

### Namestitev storitve

1. **Odprite Command Prompt kot administrator**
   - Desni klik na Command Prompt
   - Izberite "Run as Administrator"

2. **Pomaknite se v imenik namestitve digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Registrirajte storitev**
   ```bash
   digna windows install
   ```

!!! important "Navedite naslov in vrata, razen če vam ustrezajo privzete vrednosti"

    `install` zabeleži naslov in vrata v registraciji storitve, storitev pa se veže natanko na
    zabeleženo. Privzeti vrednosti sta `127.0.0.1` in `8000`, ki sprejemata povezave
    samo z istega računalnika. Nadzorna plošča na drugem gostitelju tja ne more dostopati, zato navedite
    naslov, na katerem naj backend posluša:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Te vrednosti se ne preberejo iz `config.toml`. Če jih želite pozneje spremeniti, storitev odstranite in
    jo znova namestite z novimi vrednostmi.

Storitev je registrirana s **samodejnim zagonom**, zato se bo zagnala skupaj z Windows. Takoj se
ne zažene — glejte naslednji razdelek.

#### Možnosti namestitve

| Možnost | Privzeto | Namen |
|---|---|---|
| `--name` | `digna` | Ime, pod katerim naj se registrira storitev |
| `--display-name` | `digna` | Ime, prikazano v services.msc |
| `--description` | `digna data quality backend` | Opis, prikazan v services.msc |
| `--address` | `127.0.0.1` | Naslov, na katerega storitev veže svoj API |
| `--port` | `8000` | Vrata, na katera storitev veže svoj API |
| `--working-dir` | imenik izvršljive datoteke `digna` | Imenik z datotekama `config.toml` in `license.toml`, ki ga storitev uporabi kot svoj delovni imenik |
| `--start-type` | `auto` | `auto` se zažene skupaj z Windows, `manual` se zažene samo na zahtevo, `disabled` registrira storitev, vendar je ne dovoli zagnati |
| `--account` | `LocalSystem` | Račun, pod katerim teče, npr. `DOMAIN\user` ali `.\user` |
| `--password` | | Geslo računa `--account` |

!!! tip "Izvajanje pod domenskim računom"

    `LocalSystem` nima omrežne identitete, zato preverjanje pristnosti Windows proti SQL Server in vsak
    dostop do omrežne mape ne bosta uspela. Kadar mora storitev dostopati do virov kot določen uporabnik,
    jo namestite z `--account` in `--password`.

### Zagon in ustavitev storitve

#### Za zagon storitve

```bash
digna windows start
```

#### Za ustavitev storitve

```bash
digna windows stop
```

!!! tip "Nasvet"

    Pred posodobitvijo datotek aplikacije vedno ustavite storitev.

### Premik storitve v nov imenik

Če potrebujete premestitev namestitve digna:

1. **Ustavite trenutno storitev in odstranite njeno registracijo**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Premaknite datoteke aplikacije**
   - Premaknite celotno mapo namestitve digna na novo lokacijo

3. **Storitev znova registrirajte z nove lokacije**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Ponovite vse vrednosti `--address`, `--port` ali `--account`, ki ste jih uporabili prvič — prejšnje
   registracije ni več.

4. **Zaženite storitev**
   ```bash
   digna windows start
   ```

### Odstranitev storitve

1. **Ustavite tekočo storitev**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Odstranite registracijo storitve**
   ```bash
   digna windows uninstall
   ```

Digna strežnik je zdaj odregistriran kot Windows storitev.

---

## Nadgradnja na novo izdajo {: #upgrading-to-a-new-release }

Ta razdelek opisuje nadgradnjo namestitve izdaje 2026.06 na izdajo 2026.11.

!!! warning "Nadgradnja z izdaje, starejše od 2026.06"

    Najprej izvedite korake nadgradnje izdaje 2026.06: [Nadgradnja na novo izdajo](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Nato nadaljujte s spodnjimi koraki.

### Pred nadgradnjo

**Varnostna kopija repozitorija digna je obvezna**

Pred nadgradnjo digna varnostno kopirajte svoj repozitorij (PostgreSQL), da se zaščitite pred izgubo podatkov. Varnostna kopija omogoča obnovitev, če pri nadgradnji pride do nepričakovanih težav.

**Pridobitev licenčne datoteke za izdajo 2026.11**

Izdaja 2026.11 potrebuje novo datoteko `license.toml`. Pred začetkom jo zahtevajte od ekipe digna in jo imejte pripravljeno za [korak 7](#step-7-replace-the-license-file).

### Postopek nadgradnje

#### Korak 1: Ustavite storitev digna {: #step-1-stop-the-digna-service }

Odprite Command Prompt kot skrbnik in storitev ustavite z izvršljivo datoteko `digna` svoje trenutne namestitve:

```bash
cd C:\path\to\digna
digna windows stop
```

Storitev ostane registrirana. Nova izvršljiva datoteka zavzame mesto stare v istem imeniku, zato registracija še naprej kaže na pravo datoteko.

Če digna teče v ospredju, v njegovem oknu Command Prompt pritisnite ++ctrl+c++.

#### Korak 2: Varnostno kopirajte trenutno namestitev {: #step-2-backup-current-installation }

V namestitvenem imeniku digna preimenujte izvršljivo datoteko in mapo nadzorne plošče trenutne namestitve, da bo novo izdajo mogoče namestiti ob njih:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

`digna_old.exe` obdržite, dokler ne preverite nadgradnje, `dashboard_old` pa, dokler iz nje ne obnovite svojih konfiguracijskih datotek (glejte korak 4). Nato lahko oboje izbrišete.

#### Korak 3: Razpakirajte in razmestite novo različico {: #step-3-extract-and-deploy-new-version }

1. Razpakirajte novo ZIP datoteko namestitve digna
2. Novo izvršljivo datoteko `digna` in mapo `dashboard` kopirajte v svoj namestitveni imenik

!!! warning "Pomembno"

    Niti `config.toml` niti `dashboard/dashboard_config.toml` nista nikoli vključena v namestitveni ZIP — ekipa digna nobene od teh datotek nikoli ne dostavi. Nadgradnja vaše obstoječe konfiguracije zato ne spremeni, kopije v preimenovanih mapah `*_old` pa so edine, ki jih imate.

#### Korak 4: Obnovite konfiguracijske datoteke {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
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
digna config check
```

Vsaka sekcija mora javiti OK. Odpravite vse, kar je javljeno kot FAILED, odstranite ključe, navedene pod **Unknown keys**, in pred nadaljevanjem ukaz zaženite znova.

#### Korak 7: Zamenjajte licenčno datoteko {: #step-7-replace-the-license-file }

Licenčna datoteka, izdana za prejšnjo izdajo, z izdajo 2026.11 ne deluje. Datoteko `license.toml`, ki vam jo je ekipa digna posredovala za izdajo 2026.11, kopirajte v imenik namestitve in z njo zamenjajte staro:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Ne obdržite prejšnje licence"

    S prejšnjo licenco vsak ukaz, ki preverja licenco — `serve`, `user`, `inspection`, `repo` — ne uspe, zato se digna ne zažene in repozitorija ni mogoče nadgraditi. Preden nadaljujete, preverite novo licenco:

    ```bash
    digna license check
    ```

#### Korak 8: Nadgradite shemo repozitorija {: #step-8-upgrade-the-repository-schema }

V imeniku namestitve digna zaženite:

```bash
digna repo upgrade
```

Izdaja 2026.11 shemo repozitorija upravlja z verzioniranimi migracijami. Prva nadgradnja s prejšnje izdaje shemo pripelje na zadnjo različico prejšnjega sistema, to zabeleži kot izhodišče in nato uporabi migracije izdaje 2026.11. Konča se z:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Vsi obstoječi podatki se ohranijo. Stanje repozitorija lahko kadar koli preverite z ukazom `digna repo check`: navede zadnjo uporabljeno migracijo in morebitne čakajoče.

!!! warning "digna se ne zažene na zastarelem repozitoriju"

    Od izdaje 2026.11 se strežnik ne zažene, dokler repozitorij potrebuje nadgradnjo, in to tudi sporoči, na primer:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Pred zagonom strežnika ali storitve zaženite `repo upgrade`.

#### Korak 9: Znova zaženite storitve {: #step-9-restart-services }

Če digna teče kot storitev Windows, jo znova zaženite:

```bash
cd C:\path\to\digna
digna windows start
```

Če digna poganjate ročno, znova zaženite strežnik:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Če uporabljate IIS ali Tomcat, znova zaženite ustrezni spletni strežnik.

#### Korak 10: Preverite nadgradnjo {: #step-10-verify-the-upgrade }

1. Preverite izdajo nove izvršljive datoteke:

    ```bash
    digna version
    ```

    Prva vrstica se mora glasiti `Release: 2026.11`.

2. Odprite nadzorno ploščo digna in preverite, ali se vmesnik pravilno naloži.
3. V datotekah v imeniku `logs` namestitve preverite, ali so se pojavile napake.
4. Preizkusite svoje podatkovne povezave — glejte [Preizkušanje povezave](../../../databases/overview.md#testing-a-connection).

Za začetek dela z novimi moduli glejte [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md), [Povezava agenta AI](../../../platform/agentic/connect_ai_agent.md) za digna MCP Server in [Lokacija profiliranja](../../../platform/profiling/profiling_location.md) za digna Engine.