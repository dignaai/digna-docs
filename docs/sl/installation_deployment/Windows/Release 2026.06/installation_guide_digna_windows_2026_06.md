---
title: Vodnik za namestitev na Windows – digna Release 2026.06 | digna Dokumentacija
description: Korak-po-korak vodič za namestitev digna Release 2026.06 na Windows — sistemske zahteve, nastavitev PostgreSQL, konfiguracija spletnega strežnika, konfiguracija backenda in nadzorne plošče, poganjanje digna kot Windows storitve in nadgradnja na novo verzijo.
keywords: digna namestitev windows, digna vodnik za uvajanje, digna backend namestitev, digna nadzorna plošča namestitev, postgresql namestitev, digna windows storitev, digna vodnik za nadgradnjo
image: /assets/logo_square.png
---

# Vodnik za namestitev na Windows za digna Release 2026.06

**Release:** 2026.06

**Zadnja posodobitev:** 30. avgusta 2026


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

- **dignabackend**: Jedro aplikacije, odgovorno za obdelavo podatkov in izvajanje kontrol kakovosti.
- **dignadashboard**: Spletni vmesnik gostovan na spletnem strežniku, ki omogoča uporabnikom prijazen način interakcije s platformo digna in vizualizacijo metrik kakovosti podatkov.

### Novosti v izdaji 2026.06

Ta izdaja vnaša zmožnosti opazovanja podatkov neposredno v vašo kodo, kar razvijalcem omogoča spremljanje kakovosti podatkov pri izvoru. Za popolne podrobnosti glejte [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Iščete macOS ali Linux?

Ta vodič zajema Windows. Za druge platforme si oglejte [Vodnik za namestitev na macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) ali [Vodnik za namestitev na Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Konfiguracijska datoteka
   - `license.toml` — Licenčna datoteka (sem kopirajte vašo)

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
| `digna_APP_HOST` | `localhost` ali IP naslov | Gostitelj ali IP, kjer je gostovan dignabackend |
| `digna_APP_PORT` | `8082` (privzeto) | Vrata za REST API endpoints |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontenda | Če je nadzorna plošča na drugem strežniku, vključite njen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Zahtevano za CORS s poverilnicami |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Dovoli vse HTTP metode |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Dovoli vse glave |

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
| `digna_REPO_HOST` | `localhost` ali IP | Ime gostitelja/IP PostgreSQL strežnika |
| `digna_REPO_PORT` | `5432` (privzeto) | PostgreSQL vrata |
| `digna_REPO_DB` | `postgres` | Ime podatkovne baze |
| `digna_REPO_SCHEMA` | `dignarepo` | Shema ustvarjena prej |
| `digna_REPO_USER` | `digna_user` | Uporabnik ustvarjen v nastavitvi PostgreSQL |
| `digna_REPO_PASSWORD` | Vaše geslo | Geslo, nastavljeno med ustvarjanjem sheme |

#### Sekcija [base]

Ta sekcija vsebuje varnostne in piškotne nastavitve:

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
| `digna_FERNET_KEY` | Ključ za šifriranje | Uporablja se za šifriranje tokenov in piškotkov (privzeto priložen) |
| `digna_COOKIE_DOMAIN` | `localhost` | Ujemajte z domeno frontenda |
| `digna_COOKIE_SECURE` | `false` (lokalno) / `true` (produkcija) | Uporabite `true` za HTTPS povezave |
| `digna_COOKIE_HTTPONLY` | `true` | Vedno omogočeno zaradi varnosti |
| `digna_COOKIE_SAME_SITE` | `lax` | Preprečuje CSRF napade |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 ur) | Potek seje v sekundah |
| `digna_MAX_WORKERS` | Število CPU jeder - 1 | Število paralelnih nalog inšpekcij |

#### Sekcija [logging]

Ta sekcija konfigurira vedenje beleženja (logging):

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Vrednost | Opombe |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ali `DEBUG` | `INFO` za produkcijo, `DEBUG` za odpravljanje napak |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Število dnevnih kopij dnevnikov, ki jih obdržimo |

---

### Korak 3: Inicializirajte repozitorij

1. Odprite Command Prompt
2. Pomaknite se v imenik namestitve digna (kjer sta `config.toml` in izvršljiva datoteka `digna`)
3. Zaženite test povezave:

```bash
digna repo check
```

Videti bi morali potrditev, da je povezava vzpostavljena (samo repozitorij še ni inicializiran).

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
- `--address` — Ime gostitelja/IP strežnika
- `--port` — Vrata strežnika

Videti bi morali zagonska sporočila, ki potrjujejo zagon strežnika:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Korak 6: Ustvarite administratorskega uporabnika

1. Odprite **novo** okno Command Prompt
2. Pomaknite se v imenik namestitve digna
3. Zaženite naslednji ukaz za ustvarjanje administratorskega uporabnika:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Primer:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

S tem ustvarite uporabnika s polnimi administracijskimi pravicami.

!!! tip "Najboljša praksa"

    Uporabite močno geslo z mešanico velikih in malih črk, številk in posebnih znakov.

---

## Konfiguracija nadzorne plošče {: #dashboard-configuration }

### Korak 1: Namestite nadzorno ploščo na spletni strežnik

Nadzorna plošča digna ima svojo ločeno datoteko `config.toml`, ki se nahaja v mapi `dashboard/`. Ta konfiguracija je že priložena in običajno ne zahteva sprememb med začetno namestitvijo. Spremenite jo le, če želite prilagoditi povezavo na backend.

Če potrebujete spremembe konfiguracije nadzorne plošče (npr. za večinstančne namestitve), se obrnite na dokumentacijo nadzorne plošče.

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

### Datoteke za upravljanje storitve

Vse potrebne datoteke se nahajajo v imeniku namestitve digna pod: `bin/`

Na voljo so naslednje batch datoteke:
- `install_service.bat` — Registrira digna kot Windows storitev
- `uninstall_service.bat` — Odstrani registracijo storitve
- `start_service.bat` — Zažene storitev
- `stop_service.bat` — Ustavi storitev

!!! warning "Administrator Required"

    Vse batch datoteke je potrebno zagnati z administratorskimi privilegiji.

### Namestitev storitve

1. **Odprite Command Prompt kot administrator**
   - Desni klik na Command Prompt
   - Izberite "Run as Administrator"

2. **Pomaknite se v mapo bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Zaženite namestitveni skript**
   ```bash
   install_service.bat
   ```

Digna strežnik je zdaj registriran kot Windows storitev z omogočenim samodejnim zagonom. Storitev se ne zažene takoj — glejte naslednji razdelek za zagon.

### Zagon in ustavitev storitve

#### Za zagon storitve

1. Odprite Command Prompt kot administrator
2. Pomaknite se v `digna\bin`
3. Zaženite:
   ```bash
   start_service.bat
   ```

#### Za ustavitev storitve

1. Odprite Command Prompt kot administrator
2. Pomaknite se v `digna\bin`
3. Zaženite:
   ```bash
   stop_service.bat
   ```

!!! tip "Nasvet"

    Pred posodobitvijo datotek aplikacije vedno ustavite storitev.

### Premik storitve v nov imenik

Če potrebujete premestitev namestitve digna:

1. **Odstranite trenutno storitev**
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

## Nadgradnja na novo izdajo {: #upgrading-to-a-new-release }

### Pred nadgradnjo

**Obvezno je ustvariti varnostno kopijo digna repozitorija**

Pred nadgradnjo digna varnostno kopirajte svoj repozitorij (PostgreSQL), da se zaščitite pred izgubo podatkov.
Varnostna kopija omogoča obnovitev, če pride do nepričakovanih težav med nadgradnjo.

### Postopek nadgradnje

#### Korak 1: Ustavite digna storitev

Če digna teče kot Windows storitev, jo najprej ustavite:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Korak 2: Varno shranite trenutno namestitev backenda

V imeniku namestitve digna:

```bash
# Preimenujte mapo, ki vsebuje dignabackend
ren dignabackend dignabackend_old
```
```bash
# Preimenujte dashboard
ren dashboard dashboard_old
```

#### Korak 3: Razpakirajte in namestite novo verzijo

1. Razpakirajte nov ZIP paket z namestitvijo digna
2. Kopirajte novo izvršljivo datoteko `digna` in mapo `dashboard` v vaš namestitveni imenik


!!! warning "Pomembno"

    Datoteka `config.toml` NI nikoli vključena v namestitveni ZIP. Vaša obstoječa konfiguracija ostane varna.

### Korak 4: Obnovite konfiguracijske datoteke

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Korak 5: Nadgradite shemo repozitorija

Pomaknite se v imenik namestitve digna in zaženite:

```bash
digna repo upgrade
```

To posodobi PostgreSQL shemo na najnovejšo različico, pri tem pa ohrani vse obstoječe podatke.

### Korak 6: Ponovni zagon storitev

Če poganjate kot Windows storitev:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Če poganjate ročno, ponovno zaženite strežnik:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Če uporabljate IIS ali Tomcat, ponovno zaženite ustrezen spletni strežnik.

#### Korak 7: Preverite nadgradnjo

1. Dostopajte do digna nadzorne plošče
2. Preverite, ali se vmesnik nalaga pravilno
3. Preverite strežniške zapise za morebitne napake