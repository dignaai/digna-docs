# macOS-i paigaldusjuhend digna väljalase 2026.06

**Väljalase:** 2026.06

**Viimati uuendatud:** 5. september 2026


---

## Sisukord

1. [Sissejuhatus](#introduction)
2. [Süsteeminõuded](#system-requirements)
3. [Eelpaigalduse seadistus](#pre-installation-setup)
4. [PostgreSQL serveri seadistus](#postgresql-server-setup)
5. [Veebiserveri konfiguratsioon](#web-server-configuration)
6. [Esialgne paigaldus](#initial-installation)
7. [Backend'i konfiguratsioon](#backend-configuration)
8. [Armatuurlaua konfiguratsioon](#dashboard-configuration)
9. [digna käitamine taustateenusena](#running-digna-as-a-background-service)
10. [Uuendamine uuele versioonile](#upgrading-to-a-new-release)

---

## Sissejuhatus {: #introduction }

### digna kohta

digna on põhjalik AI-põhine platvorm, mis on loodud andmekvaliteedi haldamise optimeerimiseks erinevates andmekeskkondades, nagu andmelaod, andmejärved ja lakehoused. See on üles ehitatud skaleeritavaks ja kohanemisvõimeliseks, pakkudes automatiseerimist, reaalajas jälgimist ja anomaaliate tuvastamist kaasaegsete andmeväljakutsete lahendamiseks.

digna koosneb kahest peamisest komponendist:

- **dignabackend**: rakenduse tuumiku mootor, mis vastutab andmete töötlemise ja kvaliteedikontrollide läbiviimise eest.
- **dignadashboard**: veebi-liides, mida majutab veebiserver ja mis pakub kasutajasõbralikku viisi digna platvormiga suhtlemiseks ning andmekvaliteedi mõõdikute visualiseerimiseks.

### Mis on uut versioonis 2026.06

See versioon toob andmevaatlevuse funktsioonid otse teie koodi, võimaldades arendajatel jälgida andmekvaliteeti allikal. Täpsemate muudatuste ja detailide jaoks vaadake [väljalasete märkmeid](http://docs.digna.ai/changelog/Release_202606/).

### Otsite Windowsi või Linuxi?

See juhend käsitleb macOS-i. Muude platvormide jaoks vaadake [Windowsi paigaldusjuhendit](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) või [Linuxi paigaldusjuhendit](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Süsteeminõuded {: #system-requirements }

Enne paigaldusega alustamist veenduge, et teie süsteem vastab järgmistele miinimumnõuetele:

| Nõue | Spetsifikatsioon |
|---|---|
| **Operatsioonisüsteem** | macOS 13 (Ventura) või uuem |
| **Arhitektuur** | Apple Silicon (arm64) või Intel (x86_64) |
| **Mälu (minimaalne seadistus)** | 16 GB RAM |
| **Ketaspind** | 10 GB vaba salvestusruumi |
| **Andmebaas** | PostgreSQL Server 12 või uuem |
| **Veebiserver** | nginx, Apache httpd või samaväärne |
| **Käsureatööriistad** | Xcode Command Line Tools (vajalik Homebrew jaoks) |

### Andmebaasi paigaldusvalikud

**Kui PostgreSQL on juba paigaldatud:**
Võite lisada uue andmebaasi digna jaoks olemasolevale PostgreSQL serverile.

**Kui paigaldate PostgreSQL sama masinasse, kus jookseb digna:**

!!! info "Soovitatavad spetsifikatsioonid"

    - **Mälu**: 32 GB RAM (16 GB asemel)
    - **Ketaspind**: 50 GB vaba salvestusruumi (10 GB asemel)

    Need kõrgemad spetsifikatsioonid võimaldavad dignal ja PostgreSQL-andmebaasil samaaegselt jookseda.

### Arhitektuuri kontrollimine

Selles juhendis erinevad mõned käsud Apple Silicon ja Intel masinate vahel. Oma masina arhitektuuri kontrollimiseks avage **Terminal** ja käivitage:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew paigaldatakse kataloogi `/opt/homebrew`.
- `x86_64` — Intel. Homebrew paigaldatakse kataloogi `/usr/local`.

!!! tip "Vihje"

    Selle asemel, et mõnda kataloogi kõvasti sisse kirjutada, kasutab see juhend `$(brew --prefix)`, mis laieneb õigeks asukohaks mõlemal arhitektuuril. Saate käske täpselt kopeerida.

---

## Eelpaigalduse seadistus {: #pre-installation-setup }

Enne digna paigaldamist veenduge, et kolm peamist sõltuvust on olemas:

1. **Homebrew** – pakettide haldur, mida kasutatakse allolevate komponentide paigaldamiseks
2. **PostgreSQL Server** – arvutatud mõõdikute ja jõudlusandmete talletamiseks
3. **Veebiserver** – digna armatuurlaua majutamiseks

Kui need komponendid pole veel paigaldatud, järgige alljärgnevaid jaotisi nende paigaldamiseks ja konfigureerimiseks.

### Homebrew paigaldamine

Homebrew on macOS-i standardne pakettide haldur ja seda kasutatakse kogu juhendis PostgreSQL-i ja nginx-i paigaldamiseks.

#### Samm 1: Kontrollige, kas Homebrew on juba paigaldatud

Avage **Terminal** (vajutage `Cmd + Space`, tippige `Terminal`, vajutage Enter) ja käivitage:

```bash
brew --version
```

Kui tagastatakse versiooninumber, jätkake järgmisse jaotisesse [PostgreSQL serveri seadistus](#postgresql-server-setup).

#### Samm 2: Paigaldage Homebrew

Kui käsk ei leidnud Homebrew'd, paigaldage see, järgides [ametliku Homebrew saidi](https://brew.sh) juhiseid. Installer paigaldab ka Xcode Command Line Tools, kui need puuduvad.

#### Samm 3: Lisage Homebrew PATH-i

Apple Siliconil kuvab installer kaks käsku, et lisada Homebrew teie shelli keskkonda. Käivitage need vastavalt juhistele ja kinnitage seejärel:

```bash
brew --prefix
```

See peaks Apple Siliconil kuvama `/opt/homebrew` või Inteli puhul `/usr/local`.

---

## PostgreSQL serveri seadistus {: #postgresql-server-setup }

### Kui teil on PostgreSQL juba olemas

Kui PostgreSQL on juba teie lokaalses masinas paigaldatud ja töötav või kasutate hallatud kaug-PostgreSQL serverit, võite edasi minna järgmisse sektsiooni [Veebiserveri konfiguratsioon](#web-server-configuration).

### Paigaldusvalikud

macOS pakub kahte lihtsat viisi PostgreSQL paigaldamiseks. Valige **üks**:

- [Homebrew](#postgresql-homebrew) — käsurea paigaldus, soovitatav serveri juurutusteks
- [Postgres.app](#postgresql-app) — graafiline paigaldus, mugav kohaliku hindamise jaoks

### PostgreSQL paigaldamine Homebrew abil {: #postgresql-homebrew }

#### Samm 1: Paigaldage PostgreSQL formula

```bash
brew install postgresql@16
```

#### Samm 2: Lisage PostgreSQL PATH-i

Versioneeritud PostgreSQL formulad on *keg-only*, mis tähendab, et Homebrew ei lingi nende käske PATH-i automaatselt. Lisage need ise:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Märkus"

    See eeldab macOS-i vaikimisi `zsh` shelli kasutamist. Kui kasutate `bash`-i, lisage sama rida faili `~/.bash_profile`.

#### Samm 3: Käivitage PostgreSQL teenus

```bash
brew services start postgresql@16
```

See käivitab PostgreSQL kohe ja konfigureerib selle automaatselt käivituma uuesti sisselogimisel.

#### Samm 4: Kontrollige paigaldust

```bash
psql --version
```

Kui paigaldus õnnestus, kuvatakse PostgreSQL versioon.

#### Samm 5: Ühenduge serveriga

```bash
psql postgres
```

!!! warning "Oluline — macOS erineb Windowsist siin"

    Windowsi installer palub teil luua `postgres` superkasutaja ja parooli. Homebrew ei tee seda. Selle asemel loob see superkasutaja, mis vastab teie **macOS konto** nimele, paroolita ja ligipääsetavana vaid kohalikult masinalt.

    See tähendab, et värskel Homebrew paigaldusel puudub roll `postgres`. Kasutage vajadusel oma konto nime superkasutajana ja looge eraldi digna kasutaja nagu kirjeldatud jaotises [Esialgne paigaldus](#initial-installation).

#### Samm 6: Kinnitage port

Vaikimisi PostgreSQL kuulab porti `5432`. Kinnitamiseks:

```bash
psql postgres -c "SHOW port;"
```

Märkige väärtus üles — vajate seda digna backend'i seadistamisel.

### PostgreSQL paigaldamine Postgres.app abil {: #postgresql-app }

Kui eelistate graafilist installi:

1. Laadige alla [Postgres.app](https://postgresapp.com) ja lohistage see kausta **Applications**
2. Avage rakendus ja klõpsake **Initialize**, et luua uus server
3. Järgige rakenduse juhiseid, et lisada selle käsurea tööriistad PATH-i
4. Kontrollige paigaldust:

```bash
psql --version
```

Postgres.app loob samuti superkasutaja, milleks on teie macOS konto nimi.

---

## Veebiserveri konfiguratsioon {: #web-server-configuration }

digna vajab armatuurlaua majutamiseks veebiserverit. Valige üks järgmistest:

- [nginx](#nginx-setup) — paigaldatakse Homebrew kaudu, soovitatav
- [Apache httpd](#apache-setup) — kaasas macOS-iga

Te peate paigaldama ja konfigureerima ainult **ühe** neist serveritest.

Mõlemad jaotised seadistavad kahte asja, millest armatuurlaud sõltub:

- **Ühe-leheküljeline rakenduse fallback**, et lehekülje värskendamine ei tagastaks 404 viga
- **`.md` MIME-tüüp**, et Markdown-failid servedaksid korrektselt

### nginx seadistus {: #nginx-setup }

#### Ülevaade

nginx on kerge ja kõrge jõudlusega veebiserver, sobib hästi digna staatilise armatuurlaua teenindamiseks.

#### Paigaldus

```bash
brew install nginx
```

#### nginx käivitamine

```bash
brew services start nginx
```

#### Paigalduse kontroll

1. Avage brauser
2. Minge aadressile `http://localhost:8080`
3. Peaksite nägema nginx tervituslehte

!!! note "Märkus — vaikimisi port on 8080, mitte 80"

    Homebrew konfigureerib nginx-i kuulama porti `8080`, et see saaks töötada ilma administraatoriõigusteta. macOS-is nõuab porti `80` või mis tahes porti alla 1024 sidumine root-õigusi.

    Kui soovite teenindada armatuurlaua porti 80 pealt, muutke allolevas konfiguratsioonis `listen 8080;` väärtuseks `listen 80;` ja käivitage nginx `sudo brew services start nginx`.

#### Saidi konfigureerimine armatuurlaua jaoks

Homebrew nginx-i konfiguratsioon sisaldab kõiki faile oma `servers` kataloogis. Looge digna jaoks eraldi konfiguratsioonifail sinna:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Kleebi allolev konfiguratsioon, asendades `/path/to/digna/dashboard` tegeliku teega, kuhu olete lahtipakitud `dashboard` kausta pannud:

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

!!! warning "Oluline"

    Ilma `try_files` direktiivita tagastab mis tahes armatuurlaua lehe värskendamine muu URL-i puhul 404. See on nginx-i ekvivalent IIS-i URL Rewrite moodulile Windowsis.

#### Konfiguratsiooni rakendamine

Testige süntaksivigu ja laadige nginx uuesti:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd seadistus {: #apache-setup }

#### Ülevaade

macOS sisaldab Apache httpd-d, seega paigaldust pole vaja. See on vaikimisi keelatud.

#### Apache käivitamine

```bash
sudo apachectl start
```

#### Paigalduse kontroll

1. Avage brauser
2. Minge aadressile `http://localhost`
3. Peaksite nägema teadet "It works!"

#### Nõutav: mod_rewrite lubamine

Armatuurlaud vajab URL-ide ümberkirjutamist. Avage Apache konfiguratsioon:

```bash
sudo nano /etc/apache2/httpd.conf
```

Leidke järgmine rida ja eemaldage juhtiv `#`, et see lahti kommenteerida:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Nõutav: .htaccess üle kirjutuste lubamine

Samas failis otsige `<Directory "/Library/WebServer/Documents">` plokki ja muutke:

```apache
AllowOverride None
```

selleks:

```apache
AllowOverride All
```

#### Nõutav: MIME-tüüp Markdown-failide jaoks

Endiselt failis `httpd.conf` lisage järgmine rida, et Markdown-failid servedaksid õigesti:

```apache
AddType text/markdown .md
```

!!! warning "Oluline"

    Ilma selle säteta ei pruugi `.md` faile korrektselt serveerida.

#### Konfiguratsiooni rakendamine

Kontrollige konfiguratsiooni süntaksivigu, seejärel taaskäivitage Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Esialgne paigaldus {: #initial-installation }

### Samm 1: Loo digna andmehoidla skeem ja kasutaja

digna andmehoidla (repository) salvestab kõik digna poolt arvutatud mõõdikud. See toimib keskse andmebaasina analüütilistele ja jõudlusandmetele.

#### Loo skeem ja kasutaja

Avage oma PostgreSQL klient (psql, pgAdmin või muu) ja täitke järgmised SQL käsud:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Asendage järgnevad kohatäited:**

- `<digna_repo_schema>` — soovitud skeemi nimi (nt `dignarepo`)
- `<digna_repo_user>` — soovitud kasutajanimi (nt `digna_user`)
- `<digna_repo_password>` — selle kasutaja turvaline parool

**Näide:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Terminalis ühe sammuna käivitamiseks:

```bash
psql postgres
```

Seejärel kleepige käsud `postgres=#` prompti ja väljumiseks tippige `\q`.

!!! tip "Parim tava"

    Kasutage andmebaasi kasutajate jaoks tugevaid, keerukaid paroole. Vältige kergesti äraarvatavaid volitusi.

---

### Samm 2: Pakkige digna paigalduspakett lahti

1. Leidke teile antud digna paigaldus ZIP-fail
2. Pakkige see oma soovitud asukohta — näiteks `/opt/digna` või `~/digna`
3. Pärast lahtipakkimist peaksite nägema järgmisi üksusi:
   - `dashboard/` — veebi armatuurlaua liides
   - `digna` — peamine käivitatav fail (backend + CLI kombineeritud)
   - `config.toml` — konfiguratsioonifail
   - `license.toml` — litsentsifail (kopeerige siia oma fail)

Terminalist lahtipakkimiseks:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Muutke käivitatav fail käivitatavaks

Sõltuvalt sellest, kuidas arhiiv edastati, ei pruugi käivitusbit säilida. Määrake see käsitsi:

```bash
cd /opt/digna
chmod +x digna
```

#### Kui macOS blokeerib rakenduse

Lehitsejad või meiliprogrammid märgistavad alla laetud failid karantiinitunnusega. Kui macOS teatab, et rakendust *"ei saa avada, sest arendajat ei saa kinnitada"*, eemaldage karantiin atribuut installikataloogist:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Või avage **System Settings → Privacy & Security**, leidke blokeeritud element lehe allosas ja klõpsake **Open Anyway**.

!!! note "Märkus"

    Seda sammu on vaja ainult siis, kui macOS reaalselt rakendust blokeerib. Pakette, mis edastatakse SSH kaudu või sisemistest failijagamisest, tavaliselt ei karanteenita.

### Samm 3: Paigaldage litsentsifail

!!! warning "Oluline"

    Litsentsifaili ei ole paigalduspaketis kaasas — see edastatakse teile eraldi digna poolt.

1. Leidke teile antud `license.toml` fail
2. Kopeerige see digna paigalduskataloogi (kus asuvad `config.toml` ja `digna` käivitatav fail)

**Miks see tähtis on:**
Litsentsifail sisaldab teie kliendiandmeid, litsentsi aegumiskuupäeva ja digiallkirja. **Ärge muutke seda faili** — mis tahes muudatused kehtetuks muudavad selle.

**Kataloogistruktuur pärast seadistust:**

```
/opt/digna/
├── config.toml         (konfiguratsioonifail)
├── license.toml        (TEIE LITSENTSIFAIL - kopeerige siia)
├── digna               (peamine käivitatav fail)
├── bin/                (teenuse haldusskriptid)
└── dashboard/          (veebi liides)
    └── (dashboard failid)
```

---

## Backend'i konfiguratsioon {: #backend-configuration }

### Samm 1: Loo ja redigeeri konfiguratsioonifaili

`config_template.toml` fail on kaasas teie digna paigalduskataloogis. Vajalik on see ümber nimetada `config.toml`-iks.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Asukoht:** `/opt/digna/config.toml`

Avage `config.toml` tekstiredaktoris ja konfigureerige iga alljärgnevas jaotises kirjeldatud sätet.

#### [app] jaotis

See jaotis seadistab digna backend'i rakenduse sätted:

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
| `digna_APP_HOST` | `localhost` või IP-aadress | Host või IP, kus dignabackend jookseb |
| `digna_APP_PORT` | `8082` (vaikimisi) | REST API lõpp-punktide port |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendi URL | Kui armatuurlaud on teisel serveril, lisage selle URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutav CORS-i puhul koos sisselogimisandmetega |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Lubab kõik HTTP meetodid |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Lubab kõik päised |

!!! note "Märkus"

    Kui teenindate armatuurlaua Homebrew nginx-i vaikimisi pordi pealt, on lubatav origin `http://localhost:8080`.

#### [repo] jaotis

See jaotis seadistab ühenduse PostgreSQL andmebaasiga:

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
| `digna_REPO_HOST` | `localhost` või IP | PostgreSQL serveri host/IP |
| `digna_REPO_PORT` | `5432` (vaikimisi) | PostgreSQL port |
| `digna_REPO_DB` | `postgres` | Andmebaasi nimi |
| `digna_REPO_SCHEMA` | `dignarepo` | Varem loodud skeem |
| `digna_REPO_USER` | `digna_user` | PostgreSQL-is loodud kasutaja |
| `digna_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |

#### [base] jaotis

See jaotis sisaldab turva- ja küpsise seadeid:

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
| `digna_FERNET_KEY` | Krüpteerimisvõti | Kasutatakse tokenite ja küpsiste krüpteerimiseks (vaikimisi on võti olemas) |
| `digna_COOKIE_DOMAIN` | `localhost` | Vastake oma frontend domeenile |
| `digna_COOKIE_SECURE` | `false` (kohalik) / `true` (produksioon) | Kasutage `true` HTTPS-ühenduste puhul |
| `digna_COOKIE_HTTPONLY` | `true` | Alati lubatud turvalisuse huvides |
| `digna_COOKIE_SAME_SITE` | `lax` | Vähendab CSRF-rünnete riski |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumine sekundites |
| `digna_MAX_WORKERS` | CPU tuumade arv - 1 | Paralleelsete inspekteerimistööde arv |

!!! tip "Vihje"

    Oma Maci CPU tuumade arvu leidmiseks käivitage `sysctl -n hw.ncpu`.

#### [logging] jaotis

See jaotis seadistab logimise käitumise:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` produktsiooniks, `DEBUG` tõrkeotsinguks |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Päevaste logivarukoopiate arv, mida hoida |

---

### Samm 2: Inicialiseerige andmehoidla ühendus

1. Avage **Terminal**
2. Navigeerige digna paigalduskataloogi (kus asuvad `config.toml` ja `digna` käivitatav fail)
3. Käivitage ühenduse test:

```bash
cd /opt/digna
./digna repo check
```

Peate nägema kinnitust, et ühendus on loodud (andmehoidla ise pole veel inicialiseeritud).

!!! note "Märkus"

    macOS-is ei ole käsud jooksva kataloogi suhtes PATH-is, seega käivitatakse käivitatav fail kui `./digna` mitte `digna`. Kui soovite kasutada lühemat vormi kogu aeg, lisage paigalduskataloog PATH-i:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Samm 3: Paigaldage andmehoidla skeem

Samas kataloogis käivitage:

```bash
./digna repo install
```

See käsk paigaldab vajalikud tabelid ja skeemi teie PostgreSQL andmebaasi.

### Samm 4: Käivitage digna server

Digna paigalduskataloogis käivitage serveriga:

```bash
./digna serve --address <host> --port <port>
```

**Parameetrid:**
- `--address` — serveri host/ IP
- `--port` — serveri port

Te peaksite nägema käivitussõnumeid, mis kinnitavad serveri tööd:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Vihje"

    Esimese käivitamise ajal võib macOS paluda, kas soovite lubada rakendusel sissetulevaid võrguühendusi vastu võtta. Klõpsake **Allow**, muidu ei pääse armatuurlaud backend'i.

### Samm 5: Loo administraatori kasutaja

1. Avage uus Terminali aken
2. Navigeerige digna paigalduskataloogi
3. Käivitage järgmine käsk administraatori lisamiseks:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Näide:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

See loob kasutaja nimega `admin` ja täielike administraatoriõigustega.

!!! tip "Vihje"

    Pange parool üksikutesse jutumärkidesse. `zsh` käsib tõlgendada märke nagu `!`, `$` ja `*` erimärkidena ning jutumärkideta parool ei pruugi edastuda õigesti.

!!! tip "Parim tava"

    Kasutage tugevat parooli, mis sisaldab suuri ja väikeseid tähti, numbreid ja erimärke.

---

## Armatuurlaua konfiguratsioon {: #dashboard-configuration }

### Samm 1: Paigaldage armatuurlaud veebiserverisse

Digna armatuurlaual on oma eraldi `config.toml` fail, mis asub `dashboard/` kataloogis. See konfiguratsioon on esialgse seadistuse jaoks juba olemas ja tavaliselt pole seda vaja muuta. Muutke seda ainult juhul, kui peate kohandama backend'i ühendust või tegema multi-instantsi juurutust.

Kui peate armatuurlaua konfiguratsiooni muutma, vaadake armatuurlaua dokumentatsiooni.

Valige veebiserver ja järgige vastavat juurutusprotseduuri.

#### Juurutamine nginx-i

Kui järgisite jaotist [nginx seadistus](#nginx-setup), osutab serverblokk juba teie `dashboard` kaustale ja täiendavat kopeerimist ei ole vaja.

1. **Kinnitage tee**
   - Avage `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Veenduge, et `root` osutab õigesse lahtipakitud `dashboard` kausta

2. **Veenduge, et kaust oleks loetav**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Laadige nginx uuesti**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Testige paigaldust**
   - Avage brauser
   - Minge aadressile `http://localhost:8080` (või teie konfigureeritud URL)
   - Peaksite nägema digna armatuurlaua sisselogimislehte

#### Juurutamine Apache httpd-sse

1. **Kopeerige armatuurlaud dokumentide juurkataloogi**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Lisa ümberkirjutusreeglid**

   Looge `.htaccess` fail juurutatud kausta, et armatuurlaua marsruudid säiliksid lehe värskendamisel:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Kleepige järgmine sisu:

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
   sudo apachectl restart
   ```

4. **Ligipääs armatuurlaudadele**
   - Avage brauser
   - Minge aadressile `http://localhost/digna`
   - Peaksite nägema digna armatuurlaua sisselogimislehte

---

## digna käitamine taustateenusena {: #running-digna-as-a-background-service }

### Miks käivitada digna teenusena?

digna backend'i käitamine taustateenusena tagab:

- Automaatse käivituse masina käivitamisel
- Töötamise taustal ilma avatud Terminali aknata
- Teenuse automaatse taaskäivituse krahhi korral
- Halduse läbi `launchctl`-i — macOS-i teenusehalduri

### Teenuse haldusfailid

Kõik vajalikud failid asuvad digna paigalduskataloogis kaustas: `bin/`

Järgnevad shell-skriptid on saadaval:

- `install_service.sh` — registreerib digna launchd-ga
- `uninstall_service.sh` — tühistab teenuse registreerimise
- `start_service.sh` — käivitab registreeritud teenuse
- `stop_service.sh` — peatab jooksva teenuse

!!! warning "Nõuab administraatori õigusi"

    Kõiki skripte tuleb käivitada `sudo` abil, kuna boot-ajal käivituv teenus registreerimine kirjutab kataloogi `/Library/LaunchDaemons`.

### Skriptide käivitatavaks tegemine

Lahtipakkimine ei pruugi säilitada käivitusbitte. Enne esmast kasutust:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Teenuse paigaldamine

1. **Avage Terminal**

2. **Minge bin kausta**
   ```bash
   cd /opt/digna/bin
   ```

3. **Käivitage paigaldusskript**
   ```bash
   sudo ./install_service.sh
   ```

digna server on nüüd registreeritud launchd-sse koos **automaatselt käivitamise** seadega. Teenus ei pruugi kohe alata — vaadake järgmist jaotist, kuidas seda käivitada.

### Teenuse käivitamine ja peatamine

#### Teenuse käivitamiseks

1. Avage Terminal
2. Navigeerige `/opt/digna/bin`
3. Käivitage:
   ```bash
   sudo ./start_service.sh
   ```

#### Teenuse peatamiseks

1. Avage Terminal
2. Navigeerige `/opt/digna/bin`
3. Käivitage:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Vihje"

    Enne rakenduse failide uuendamist peatage teenus alati.

### Teenuse kontrollimine

Kontrollimaks, et teenus on registreeritud ja töötab:

```bash
sudo launchctl list | grep digna
```

Rida, mis algab protsessi ID-ga, tähendab, et teenus töötab. Kui esimeses veerus on `-`, siis on teenus registreeritud, kuid peatatud.

### Teenuse liigutamine uude kataloogi

launchd salvestab käivitatava faili absoluutse tee, seega paigaldise ümberpaigutamine nõuab teenuse uuesti registreerimist:

1. **Eemaldage praegune teenus**
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

### Teenuse desinstallimine

1. **Peatage jooksva teenus**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Desinstallige teenus**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna server on nüüd launchd-st eemaldatud.

---

## Uuendamine uuele versioonile {: #upgrading-to-a-new-release }

### Enne uuendamist

**digna andmehoidla varundamine on kohustuslik**

Enne digna uuendamist varundage oma repository (PostgreSQL), et kaitsta andmete kaotsimineku eest.
Varukoopia võimaldab taastada olukorra, kui uuenduse käigus tekib ootamatuid probleeme.

Varukoopia loomiseks Terminalis:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Uuenduse protsess

#### Samm 1: Peatage digna teenus

Kui digna töötab taustateenusena, peatage see esmalt:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Kui digna töötab esiplaanil, vajutage selle Terminali aknas `Ctrl + C`.

#### Samm 2: Varundage praegune backend paigaldus

Digna paigalduskataloogis:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Samm 3: Pakige lahti ja juurutage uus versioon

1. Pakkige lahti uus digna paigaldus ZIP-fail
2. Kopeerige uus `digna` käivitatav fail ja `dashboard` kaust oma paigalduskataloogi
3. Taastage käivitusbit ja vajadusel eemaldage karantiini atribuut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Oluline"

    Fail `config.toml` EI OLE kunagi kaasa pakitud installatsiooni ZIP-is. Teie olemasolev konfiguratsioon jääb muutmata.

### Samm 4: Taastage konfiguratsioonifailid

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Samm 5: Uuendage andmehoidla skeemi

Navigeerige digna paigalduskataloogi ja käivitage:

```bash
cd /opt/digna
./digna repo upgrade
```

See uuendab PostgreSQL skeemi uusimale versioonile, säilitades kogu olemasoleva andmestiku.

### Samm 6: Taaskäivitage teenused

Kui jooksed taustateenusena:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Kui jooksesid manuaalselt, käivitage server uuesti:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Kui kasutate nginx-i või Apache-t, taaskäivitage vastav veebiserver:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Samm 7: Kinnitage uuendus

1. Avage digna armatuurlaud
2. Veenduge, et liides laeb korrektselt
3. Kontrollige serveri logisid võimalike vigade osas