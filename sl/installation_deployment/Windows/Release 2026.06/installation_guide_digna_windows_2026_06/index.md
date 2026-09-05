# Navodila za namestitev na Windows za digna Release 2026.06

**Release:** 2026.06

**Zadnja posodobitev:** 30. avgust 2026


---

## Vsebina

1. [Uvod](#introduction)
2. [Sistemske zahteve](#system-requirements)
3. [Prednamestitvena priprava](#pre-installation-setup)
4. [Nastavitev PostgreSQL strežnika](#postgresql-server-setup)
5. [Konfiguracija spletnega strežnika](#web-server-configuration)
6. [Prva namestitev](#initial-installation)
7. [Konfiguracija backend-a](#backend-configuration)
8. [Konfiguracija nadzorne plošče](#dashboard-configuration)
9. [Poganjanje digna kot Windows storitve](#running-digna-as-a-windows-service)
10. [Nadgradnja na novo različico](#upgrading-to-a-new-release)

---

## Uvod {: #introduction }

### O digna

digna je celovita platforma, ki temelji na AI in je zasnovana za optimizacijo upravljanja kakovosti podatkov v različnih podatkovnih okoljih, kot so podatkovni skladi, lakes in lakehousi. Zgrajena za visoko skalabilnost in prilagodljivost, digna naslavlja sodobne podatkovne izzive preko avtomatizacije, spremljanja v realnem času in zaznavanja anomalij.

digna sestavljata dve glavni komponenti:

- **dignabackend**: jedro aplikacije, odgovorno za obdelavo podatkov in izvajanje preverjanj kakovosti.
- **dignadashboard**: spletni vmesnik gostovan na spletnem strežniku, ki ponuja uporabniku prijazen način za interakcijo s platformo digna in vizualizacijo metrik kakovosti podatkov.

### Novosti v izdaji 2026.06

Ta izdaja prinaša zmožnosti opazovanja podatkov neposredno v vašo kodo, kar omogoča razvijalcem spremljanje kakovosti podatkov pri viru. Celoten seznam sprememb najdete v [release notes](http://docs.digna.ai/changelog/Release_202606/).

---

## Sistemske zahteve {: #system-requirements }

Pred začetkom namestitve se prepričajte, da vaš sistem izpolnjuje naslednje minimalne zahteve:

| Zahteva | Specifikacija |
|---|---|
| **Operacijski sistem** | Windows Server ali Windows 10/11 |
| **Pomnilnik (minimalno)** | 16 GB RAM |
| **Prostor na disku** | 10 GB prostega prostora |
| **Baza podatkov** | PostgreSQL Server 12 ali novejši |
| **Spletni strežnik** | IIS, Apache Tomcat ali ekvivalent |

### Možnosti namestitve baze podatkov

**Če je PostgreSQL že nameščen:**
V obstoječi PostgreSQL strežnik lahko dodate novo bazo za digna.

**Če nameščate PostgreSQL na isti stroj kot digna:**

!!! info "Priporočene specifikacije"

    - **Pomnilnik**: 32 GB RAM (namesto 16 GB)
    - **Prostor na disku**: 50 GB prostega prostora (namesto 10 GB)

    Te višje specifikacije omogočajo sočasno delovanje digna in PostgreSQL baze.

---

## Prednamestitvena priprava {: #pre-installation-setup }

Pred namestitvijo digna poskrbite za naslednji dve ključni predpogoj:

1. **PostgreSQL Server** – za shranjevanje izračunanih metrik in podatkov o zmogljivosti
2. **Spletni strežnik** – za gostovanje digna Dashboarda

Če ti komponenti še nista nameščeni, sledite spodnjim razdelkom za namestitev in konfiguracijo.

---

## Nastavitev PostgreSQL strežnika {: #postgresql-server-setup }

### Če že imate PostgreSQL

Če je PostgreSQL že nameščen in teče na vašem lokalnem stroju ali uporabljate upravljan oddaljen PostgreSQL strežnik, lahko preskočite na [naslednji razdelek](#web-server-configuration).

### Namestitev PostgreSQL

Sledite tem korakom za namestitev PostgreSQL na Windows:

#### Korak 1: Prenesite PostgreSQL

1. Obiščite [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Izberite **Windows**
3. Prenesite najnovejši installer

#### Korak 2: Zaženite namestitveni program

1. Dvokliknite preneseno datoteko installer
2. Sledite navodilom v čarovniku za namestitev

#### Korak 3: Izberite namestitveni imenik

Izberite imenik, kamor bo PostgreSQL nameščen. Privzeta lokacija je običajno primerna.

#### Korak 4: Izberite komponente

Za standardno namestitev pustite privzete komponente izbrane.

#### Korak 5: Nastavite geslo superuporabnika PostgreSQL

Vnesite in potrdite geslo za PostgreSQL superuporabnika (`postgres`). **Shranjeno geslo varno** — potrebovali ga boste kasneje.

#### Korak 6: Konfigurirajte številko porta

Privzeti PostgreSQL port je `5432`. Uporabite privzeto ali določite drug port po potrebi.

!!! tip "Namig"

    Če je port 5432 že v uporabi, izberite alternativni port in si ga zabeležite za kasnejšo konfiguracijo.

#### Korak 7: Izberite lokalizacijo

Izberite locale za vašo bazo. Privzeta nastavitev je običajno ustrezna.

#### Korak 8: Dokončajte namestitev

Kliknite **Next** skozi preostale korake, nato kliknite **Finish**.

#### Korak 9: Preverite namestitev

Odprite Command Prompt in preverite, da je PostgreSQL nameščen:

```bash
psql --version
```

Če je namestitev uspešna, bi morali videti različico PostgreSQL.

---

## Konfiguracija spletnega strežnika {: #web-server-configuration }

digna zahteva spletni strežnik za gostovanje nadzorne plošče. Izberite eno od naslednjih možnosti:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Potrebno je namestiti in konfigurirati samo enega izmed teh strežnikov.

### Nastavitev IIS {: #iis-setup }

#### Pregled

Internet Information Services (IIS) je Microsoftov spletni strežnik za gostovanje spletnih strani in spletnih aplikacij.

#### Vključitev IIS

1. **Odprite Control Panel**
   - Pritisnite `Win + R`
   - Vnesite `control` in pritisnite Enter

2. **Pojdite na Windows Features**
   - Kliknite **Programs**
   - Izberite **Turn Windows features on or off**

3. **Vključite Internet Information Services**
   - Pomaknite se navzdol in poiščite **Internet Information Services (IIS)**
   - Označite polje za omogočanje
   - Kliknite **+** za razširitev in preverite, da so izbrane naslednje podkomponente:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Kliknite OK** za uveljavitev sprememb

5. **Preverite namestitev IIS**
   - Odprite brskalnik
   - Pojdite na `http://localhost`
   - Videti bi morali IIS Welcome stran

#### Zahtevano: URL Rewrite modul

IIS zahteva komponento URL Rewrite. Prenesite in namestite jo z [uradne Microsoft strani](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Zahtevano: MIME tip za Markdown datoteke

Da se zagotovI pravilno serviranje Markdown datotek (`.md`) v IIS:

1. Odprite **IIS Manager** (pritisnite `Win + R`, vnesite `inetmgr`, pritisnite Enter)
2. Pomaknite se do **Your Site > MIME Types**
3. Kliknite **Add...**
4. Konfigurirajte:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Pomembno"

    Brez te nastavitve se `.md` datoteke morda ne bodo servisirale pravilno.

---

### Nastavitev Apache Tomcat {: #apache-tomcat-setup }

#### Pregled

Apache Tomcat je odprtokodni Java servlet container in spletni strežnik.

#### Namestitev

1. **Prenesite Apache Tomcat**
   - Obiščite [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Prenesite Windows ZIP distribucijo

2. **Razširite arhiv**
   - Razširite ZIP datoteko v imenik na vašem sistemu
   - Primer: `C:\Program Files\Apache Tomcat`

3. **Preverite, da Tomcat teče**
   - Odprite brskalnik
   - Pojdite na `http://localhost:8080`
   - Videti bi morali Apache Tomcat welcome stran

!!! tip "Namig"

    Apache Tomcat se običajno zažene samodejno po namestitvi. Če se ne zažene, pojdite v mapo `bin` in zaženite `startup.bat`.

---

## Prva namestitev {: #initial-installation }

### Korak 1: Nastavite digna repozitorij

Digna repozitorij hrani vse metrike, ki jih izračuna digna. Deluje kot centralna baza za analitične in zmogljivostne podatke.

#### Ustvarite shemo repozitorija in uporabnika

Odprite svoj PostgreSQL klient (pgAdmin, psql ali podoben) in izvedite naslednje SQL ukaze:

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

!!! tip "Najboljša praksa"

    Uporabljajte močna, kompleksna gesla za uporabnike baze podatkov. Izogibajte se enostavnim in lahko ugibljivim poverilnicam.

---

### Korak 2: Razširite namestitveni paket digna

1. Poiščite ZIP datoteko z namestitvijo digna, ki vam je bila posredovana
2. Razširite jo na želeno lokacijo za namestitev
3. Po razširitvi bi morali videti naslednje elemente:
   - `dashboard/` — spletni vmesnik nadzorne plošče
   - `digna` — glavni izvršljivi program (backend + CLI v enem)
   - `config.toml` — konfiguracijska datoteka
   - `license.toml` — licenčna datoteka (sem kopirajte svojo)

### Korak 3: Namestite licenčno datoteko

!!! warning "Pomembno"

    Licenčna datoteka **ni** vključena v namestitveni paket in vam bo posredovana ločeno s strani digna.

1. Poiščite datoteko `license.toml`, ki vam je bila posredovana
2. Kopirajte jo v korenski imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)

**Zakaj je to pomembno:**
Licenčna datoteka vsebuje podatke o stranki, datum poteka licence in digitalni podpis. **Ne spreminjajte te datoteke** — kakršne koli spremembe jo bodo razveljavile.

**Struktura imenika po namestitvi:**

```
digna_installation/
├── config.toml         (configuration file)
├── license.toml        (YOUR LICENSE FILE - copy here)
├── digna               (main executable)
└── dashboard/          (web interface)
    └── (dashboard files)
```

---

## Konfiguracija backend-a {: #backend-configuration }

### Korak 1: Ustvarite in uredite konfiguracijsko datoteko

Datoteka `config_template.toml` je priložena v vašem imeniku za namestitev digna. Preimenujte jo v `config.toml`.

**Lokacija:** `digna_installation/config.toml`

Odprite `config.toml` v urejevalniku besedila in konfigurirajte spodnje odseke.

#### Sekcija [app]

Ta sekcija konfigurira nastavitve aplikacije digna backend:

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
| `digna_APP_HOST` | `localhost` ali IP naslov | Gostitelj, kjer teče dignabackend |
| `digna_APP_PORT` | `8082` (privzeto) | Port za REST API endpoint-e |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontenda | Če je dashboard na drugem strežniku, vključite njegov URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Zahtevano za CORS z poverilnicami |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Dovoli vse HTTP metode |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Dovoli vse headerje |

#### Sekcija [repo]

Ta sekcija konfigurira povezavo na PostgreSQL bazo:

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
| `digna_REPO_HOST` | `localhost` ali IP | Hostname/IP PostgreSQL strežnika |
| `digna_REPO_PORT` | `5432` (privzeto) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Ime baze podatkov |
| `digna_REPO_SCHEMA` | `dignarepo` | Shema ustvarjena prej |
| `digna_REPO_USER` | `digna_user` | Uporabnik ustvarjen v PostgreSQL nastavitvi |
| `digna_REPO_PASSWORD` | Vaše geslo | Geslo nastavljeno ob ustvarjanju sheme |

#### Sekcija [base]

Ta sekcija vsebuje varnostne in cookie nastavitve:

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
| `digna_FERNET_KEY` | Šifrirni ključ | Uporablja se za šifriranje tokenov in cookie-jev (privzeto je zagotovljen) |
| `digna_COOKIE_DOMAIN` | `localhost` | Naj se ujema z vašim frontend domeno |
| `digna_COOKIE_SECURE` | `false` (lokalno) / `true` (produkcija) | Uporabite `true` za HTTPS povezave |
| `digna_COOKIE_HTTPONLY` | `true` | Vedno omogočeno zaradi varnosti |
| `digna_COOKIE_SAME_SITE` | `lax` | Preprečuje CSRF napade |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ure) | Čas poteka seje v sekundah |
| `digna_MAX_WORKERS` | Število CPU jeder - 1 | Število vzporednih nalog inšpekcij |

#### Sekcija [logging]

Ta sekcija konfigurira vedenje beleženja:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ali `DEBUG` | `INFO` za produkcijo, `DEBUG` za odpravljanje napak |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Število dnevnih kopij log datotek, ki jih obdržimo |

---

### Korak 3: Inicializirajte repozitorij

1. Odprite Command Prompt
2. Pomaknite se v imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)
3. Zaženite test povezave:

```bash
digna repo check
```

Videti bi morali potrditev, da je povezava vzpostavljena (sama shema repozitorija še ni nameščena).

### Korak 4: Namestite shemo repozitorija

V istem imeniku zaženite:

```bash
digna repo install
```

Ta ukaz namesti potrebne tabele in shemo v vašo PostgreSQL bazo.

### Korak 5: Zaženite digna strežnik

V imeniku namestitve digna zaženite strežnik z:

```bash
digna serve --address <host> --port <port>
```

**Parametri:**
- `--address` — hostname/IP strežnika
- `--port` — port strežnika

Videti bi morali zagonska sporočila, ki potrjujejo, da strežnik teče:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Korak 6: Ustvarite skrbniškega uporabnika

1. Odprite **novo** okno Command Prompt
2. Pomaknite se v imenik namestitve digna
3. Zaženite naslednji ukaz za ustvarjanje skrbniškega uporabnika:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Primer:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Ta ukaz ustvari uporabnika s polnimi administratorskimi pravicami.

!!! tip "Najboljša praksa"

    Uporabljajte močno geslo z mešanico velikih/malih črk, številk in posebnih znakov.

---

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Korak 1: Namestite dashboard na spletni strežnik

Digna dashboard ima svojo ločeno datoteko `config.toml` v mapi `dashboard/`. Ta konfiguracija je že priložena in običajno ne zahteva sprememb pri začetni namestitvi. Spremeniti jo je potrebno le, če želite prilagoditi povezavo na backend ali za multi-instance postavitve.

Če morate prilagoditi konfiguracijo dashboarda, glejte dokumentacijo dashboarda.

Izberite vaš spletni strežnik in sledite ustreznim korakom za namestitev.

#### Namestitev na IIS

1. **Odprite IIS Manager**
   - Pritisnite `Win + R`, vnesite `inetmgr`, pritisnite Enter

2. **Ustvarite novo spletno mesto**
   - V levem panelu z desnim klikom izberite **Sites**
   - Izberite **Add Website...**

3. **Konfigurirajte spletno mesto**
   - **Site Name**: Vnesite ime (npr. "dignaDashboard")
   - **Physical Path**: Kliknite Browse in izberite vašo mapo `dashboard`
   - **Binding**: Nastavite IP naslov in port (privzeti port 80 za HTTP, 443 za HTTPS)

4. **Zaženite spletno mesto**
   - Kliknite **OK** za ustvarjanje mesta
   - Z desnim klikom na novo mesto izberite **Start**

5. **Preizkusite namestitev**
   - Odprite brskalnik
   - Pojdite na `http://localhost` (ali vaš konfigurirani URL)
   - Videti bi morali stran za prijavo digna dashboarda

#### Namestitev na Apache Tomcat

1. **Kopirajte dashboard v Tomcat**
   - Kopirajte mapo `dashboard` v Tomcat `webapps` imenik
   - Po potrebi jo preimenujte (npr. v `digna`)
   - Primer: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Preverite namestitev**
   - Osvežite ali ponovno naložite Tomcat upravljalno stran (http://localhost:8080)
   - Videti bi morali "digna" (ali izbrano ime) na seznamu nameščenih aplikacij

3. **Dostop do dashboarda**
   - Odprite brskalnik
   - Pojdite na `http://localhost:8080/digna`
   - Videti bi morali stran za prijavo digna dashboarda

---

## Poganjanje digna kot Windows storitve {: #running-digna-as-a-windows-service }

### Zakaj uporabiti Windows storitev?

Poganjanje digna backend-a kot Windows storitve zagotavlja, da se:
- Zažene samodejno ob zagonu strežnika
- Teče v ozadju brez odprtega Command Prompt okna
- Samodejno ponovno zažene ob morebitnem zrušitvi
- Lahko upravljate preko Windows Services

### Datoteke za upravljanje storitve

Vse potrebne datoteke so v imeniku namestitve digna v: `bin/`

Na voljo so naslednje batch datoteke:
- `install_service.bat` — registrira digna kot Windows storitev
- `uninstall_service.bat` — odstrani registracijo storitve
- `start_service.bat` — zažene storitev
- `stop_service.bat` — ustavi storitev

!!! warning "Potrebne so administratorske pravice"

    Vse batch datoteke je treba zagnati z administratorskimi privilegiji.

### Namestitev storitve

1. **Odprite Command Prompt kot Administrator**
   - Z desnim klikom na Command Prompt
   - Izberite "Run as Administrator"

2. **Pomaknite se v mapo bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Zaženite namestitveni skript**
   ```bash
   install_service.bat
   ```

Digna strežnik je sedaj registriran kot Windows storitev z nastavljeno **samodejno zagon**. Storitev se ne zažene takoj — zaženite jo v naslednjem razdelku.

### Zagon in zaustavitev storitve

#### Za zagon storitve

1. Odprite Command Prompt kot Administrator
2. Pomaknite se v `digna\bin`
3. Zaženite:
   ```bash
   start_service.bat
   ```

#### Za zaustavitev storitve

1. Odprite Command Prompt kot Administrator
2. Pomaknite se v `digna\bin`
3. Zaženite:
   ```bash
   stop_service.bat
   ```

!!! tip "Namig"

    Pred posodobitvijo datotek aplikacije storitev vedno zaustavite.

### Premestitev storitve v nov imenik

Če morate premakniti namestitev digna:

1. **Odstranite obstoječo storitev**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Premaknite datoteke aplikacije**
   - Premaknite celotno mapo namestitve digna na novo lokacijo

3. **Ponovno namestite storitev**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Zaženite storitev**
   ```bash
   start_service.bat
   ```

### Odstranitev storitve

1. **Ustavite tekočo storitev**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Odstranite storitev**
   ```bash
   uninstall_service.bat
   ```

Digna strežnik je zdaj odregistriran kot Windows storitev.

---

## Nadgradnja na novo različico {: #upgrading-to-a-new-release }

### Preden nadgradite

**Obvezno ustvarite varnostno kopijo digna repozitorija**

Pred nadgradnjo digna obvezno naredite varnostno kopijo vašega repozitorija (PostgreSQL), da se zaščitite pred izgubo podatkov.
Varnostna kopija omogoča obnovitev, če bi nadgradnja naletela na nepričakovane težave.

### Postopek nadgradnje

#### Korak 1: Ustavite digna storitev

Če digna teče kot Windows storitev, jo najprej ustavite:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Korak 2: Varnostno kopirajte trenutno backend namestitev

V imeniku namestitve digna:

```bash
# Preimenujte mapo, ki vsebuje dignabackend
ren dignabackend dignabackend_old
```
```bash
# Preimenujte dashboard
ren dashboard dashboard_old
```

#### Korak 3: Razširite in namestite novo različico

1. Razširite nov ZIP paket z namestitvijo digna
2. Kopirajte novo izvršljivo datoteko `digna` in mapo `dashboard` v vaš imenik namestitve

!!! warning "Pomembno"

    Datoteka `config.toml` **nikoli** ni vključena v namestitveni ZIP. Vaša obstoječa konfiguracija ostane varna.

### Korak 4: Obnovite konfiguracijske datoteke

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Korak 5: Nadgradite shemo repozitorija

Pomaknite se v imenik namestitve digna in zaženite:

```bash
digna repo upgrade
```

To posodobi PostgreSQL shemo na najnovejšo različico in hkrati ohrani vse obstoječe podatke.

### Korak 6: Ponovni zagon storitev

Če tečeta kot Windows storitev:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Če poganjate ročno, znova zaženite strežnik:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Če uporabljate IIS ali Tomcat, ponovno zaženite ustrezen spletni strežnik.

#### Korak 7: Preverite nadgradnjo

1. Dostopajte do digna dashboarda
2. Preverite, ali se vmesnik pravilno naloži
3. Preverite strežniške zapise za morebitne napake