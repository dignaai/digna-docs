# macOS-i paigaldusjuhend digna väljalase 2026.11

**Väljalase:** 2026.11

**Viimati uuendatud:** 7. november 2026


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

- **digna**: rakenduse tuum, mis vastutab andmete töötlemise ja kvaliteedikontrollide läbiviimise eest. See ühendab taustasüsteemi ja käsurealiidese üheks käivitatavaks failiks ning asendab varasemate väljalasete eraldi programmid `dignabackend` ja `dignacli`.
- **dignadashboard**: veebi-liides, mida majutab veebiserver ja mis pakub kasutajasõbralikku viisi digna platvormiga suhtlemiseks ning andmekvaliteedi mõõdikute visualiseerimiseks.

### Mis on uut versioonis 2026.11

See väljalase toob kaasa uued moodulid digna Data Reconciliation ja digna Agentic (koos serveriga digna MCP Server) ning komponendi digna Engine, mis suudab andmeid profileerida digna sees ja kontrollida viidete terviklikkust eri andmebaasitehnoloogiate vahel. Täielikud andmed leiate [väljalaske märkmetest](../../../changelog/Release_202611.md).

Paigalduse jaoks toob väljalase uue hoidla migratsioonimehhanismi, komponendi digna Engine jaoks valikulise sektsiooni `[duckdb]` failis `config.toml` ning uue litsentsifaili. Neid kõiki käsitleb [uuendamise jaotis](#upgrading-to-a-new-release).

### Otsite Windowsi või Linuxi?

See juhend käsitleb macOS-i. Muude platvormide jaoks vaadake [Windowsi paigaldusjuhendit](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) või [Linuxi paigaldusjuhendit](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Andmebaasiühendusi, mille profileerimise asukoht on digna Engine, profileeritakse digna hostis
    endas. Planeerige nende jaoks lisamälu ja -kettaruumi, vt
    [\[duckdb\] sektsioon](#duckdb-section).

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

!!! info "Konfiguratsiooni- ja litsentsifailid ei ole paketis"

    Paigaldusega ei kaasne ei `config.toml` ega `dashboard/dashboard_config.toml` — mõlemad
    loote ise, jaotistes [Backendi konfiguratsioon](#backend-configuration) ja
    [Armatuurlauai konfiguratsioon](#dashboard-configuration). Ka `license.toml` ei ole kaasas;
    digna tarnib selle eraldi, nagu kirjeldab samm 3.

Terminalist lahtipakkimiseks:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
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

See jaotis seadistab armatuurlaua ja backendi vahelist päritoluülest ressursijagamist (CORS):

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Armatuurlaua URL-id | URL-id, millelt armatuurlaud serveeritakse. Brauseri päringud mis tahes muult päritolult lükatakse tagasi |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Nõutav, et brauser saadaks igas päringus kaasa sessiooniküpsise |

!!! note "Märkus"

    Kui teenindate armatuurlaua Homebrew nginx-i vaikimisi pordi pealt, on lubatav origin `http://localhost:8080`.

!!! info "Jaotis [app] on valikuline"

    Alates Release 2026.11-st võib mõlemad võtmed ja kogu sektsiooni `[app]` ära jätta. See on
    õige seadistus, kui pöördpuhverserver (reverse proxy) serveerib armatuurlaua ja backendi ühe päritolu
    all: brauser ei tee siis päritoluüleseid päringuid ja vaikimisi pole ühtki lubatud.

#### [repo] jaotis

See jaotis seadistab ühenduse PostgreSQL andmebaasiga:

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
| `DIGNA_REPO_HOST` | `localhost` või IP | PostgreSQL serveri host/IP |
| `DIGNA_REPO_PORT` | `5432` (vaikimisi) | PostgreSQL port |
| `DIGNA_REPO_DB` | `postgres` | Andmebaasi nimi |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Varem loodud skeem |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL-is loodud kasutaja |
| `DIGNA_REPO_PASSWORD` | Teie parool | Parool, mis määrati skeemi loomisel |
| `DIGNA_REPO_SSLMODE` | `prefer` (vaikimisi) | Valikuline. PostgreSQL-i SSL-režiim: `disable`, `allow`, `prefer`, `require`, `verify-ca` või `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (vaikimisi) | Valikuline. Ühenduste arv, mida digna hoidlaga avatuna hoiab |

#### [base] jaotis

See jaotis sisaldab turbe-, küpsise- ja inspekteerimisseadeid:

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
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host, mille all armatuurlaud on kättesaadav. `""` ei määra domeeni, mis on õige puhverserveri taga, mis serveerib armatuurlaua ja backendi ühe päritolu all |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Peab olema `true` alati, kui digna serveeritakse üle HTTPS-i |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Hoiab sessiooniküpsise skriptidele kättesaamatuna |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 tundi) | Sessiooni aegumine sekundites |
| `DIGNA_MAX_WORKERS` | CPU tuumade arv - 1 | Samaaegselt töötada võivate inspekteerimiste arv |
| `DIGNA_FRONTEND_BASEURL` | Armatuurlaua URL | Kohustuslik. Kasutatakse teavitussõnumite linkides, seega peab see olema URL, mida adressaadid saavad avada |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (vaikimisi) | Valikuline. Sekundid, mille jooksul võib üks päring lähteandmebaasi vastu töötada, enne kui see katkestatakse; `0` lülitab ajalõpu välja |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (vaikimisi) | Valikuline. Sekundid, mille jooksul oodatakse ühendust lähteandmebaasiga; `0` ootab piiramatult |

!!! tip "Vihje"

    Oma Maci CPU tuumade arvu leidmiseks käivitage `sysctl -n hw.ncpu`.

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

#### [logging] jaotis

See jaotis seadistab logimise käitumise:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` või `DEBUG` | `INFO` produktsiooniks, `DEBUG` tõrkeotsinguks. Aktsepteeritakse ka `TRACE`, `WARN` ja `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (vaikimisi) | Valikuline. Roteeruvate logifailide kataloog, suhteline töökataloogi suhtes |
| `DIGNA_LOGGING_MAX_FILES` | `30` (vaikimisi) | Valikuline. Säilitatavate roteeritud logifailide arv |

#### [duckdb] jaotis (valikuline) {: #duckdb-section }

Uus väljalaskes Release 2026.11. See jaotis määrab ressursid komponendile **digna Engine**, mis
profileerib andmeid digna sees nende andmebaasiühenduste puhul, mille profileerimise asukoht on
**digna Engine**, ning käitab viidete terviklikkuse kontrolle eri andmebaasiühendustel asuvate
andmeallikate vahel. Vaadake [Profileerimise asukoht](../../../platform/profiling/profiling_location.md).

Jaotis on valikuline. Ilma selleta kehtivad allolevad vaikeväärtused.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parameeter | Väärtus | Märkused |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (vaikimisi) | Mälu MB-des, mida üks digna Engine'i käivitus võib kasutada. Korraga võib aktiivne olla kuni `DIGNA_MAX_WORKERS` käivitust |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Vaikimisi: süsteemi ajutine kataloog (digna käitava konto `$TMPDIR`) | Ajutiste failide kataloog, kui andmed mällu ei mahu |

!!! tip "digna Engine'i ressursside planeerimine"

    Planeerige digna hostis lisaks digna enda kasutatavale mälule kuni
    `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` mälu ning ajutises kataloogis piisavalt
    vaba kettaruumi, et sinna mahuksid digna Engine'i kasutavate andmeallikate suurima
    inspekteeritava kuupäeva andmed. Suunake `DIGNA_DUCKDB_TEMP_DIRECTORY` sellise ruumiga kettale,
    kuhu digna käitaval kontol on kirjutusõigus:

    ```bash
    mkdir -p /opt/digna/tmp
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

### Samm 3: Inicialiseerige andmehoidla ühendus

1. Avage **Terminal**
2. Navigeerige digna paigalduskataloogi (kus asuvad `config.toml` ja `digna` käivitatav fail)
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

    macOS-is ei ole käsud jooksva kataloogi suhtes PATH-is, seega käivitatakse käivitatav fail kui `./digna` mitte `digna`. Kui soovite kasutada lühemat vormi kogu aeg, lisage paigalduskataloog PATH-i:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Samm 4: Paigaldage andmehoidla skeem

Samas kataloogis käivitage:

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

### Samm 5: Loo administraatori kasutaja

1. Avage uus Terminali aken
2. Navigeerige digna paigalduskataloogi
3. Käivitage järgmine käsk administraatori lisamiseks:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Näide:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

See loob kasutaja e-posti aadressiga `admin@example.com` ja täielike administraatoriõigustega.

!!! tip "Vihje"

    Pange parool üksikutesse jutumärkidesse. `zsh` käsib tõlgendada märke nagu `!`, `$` ja `*` erimärkidena ning jutumärkideta parool ei pruugi edastuda õigesti.

!!! tip "Parim tava"

    Kasutage tugevat parooli, mis sisaldab suuri ja väikeseid tähti, numbreid ja erimärke.

---

### Samm 6: Käivitage digna server

Digna paigalduskataloogis käivitage serveriga:

```bash
./digna serve --address <host> --port <port>
```

**Parameetrid:**
- `--address` — serveri host/ IP (vaikimisi `127.0.0.1`)
- `--port` — serveri port (vaikimisi `8000`)

Kui server töötab, kuvab see aadressi, millel ta kuulab:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Vihje"

    Esimese käivitamise ajal võib macOS paluda, kas soovite lubada rakendusel sissetulevaid võrguühendusi vastu võtta. Klõpsake **Allow**, muidu ei pääse armatuurlaud backend'i.

!!! note "Server hoiab terminali hõivatuna"

    `serve` töötab esiplaanil ja jätkab, kuni peatate selle klahvidega ++ctrl+c++. Jätke see tööle, kuni seadistuse lõpetate; automaatseks käivitamiseks alglaadimisel vaadake [digna käitamine taustateenusena](#running-digna-as-a-background-service).

## Armatuurlaua konfiguratsioon {: #dashboard-configuration }

### Samm 1: Paigaldage armatuurlaud veebiserverisse

digna armatuurlaud loeb oma konfiguratsiooni failist `dashboard/dashboard_config.toml`. See fail ei ole paigaldusega kaasas — loote selle kataloogi `dashboard/` armatuurlaua failide kõrvale.

Selle sisu on kirjeldatud jaotises [Ühekordne sisselogimine (SSO)](../../../sso/overview.md), kus faili ka vaja läheb: see sisaldab armatuurlaua pakutavaid sisselogimisvalikuid ning mitme instantsiga juurutuste puhul ühendust backendiga.

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

See jaotis uuendab Release 2026.06 paigalduse Release 2026.11-le.

!!! warning "Uuendamine 2026.06-st vanemast väljalaskest"

    Tee esmalt läbi Release 2026.06 uuendamise sammud: [Uuendamine uuele versioonile](../Release%202026.06/installation_guide_digna_macos_2026_06.md#upgrading-to-a-new-release). Seejärel jätka allolevate sammudega.

### Enne uuendamist

**digna andmehoidla varundamine on kohustuslik**

Enne digna uuendamist varundage oma repository (PostgreSQL), et kaitsta andmete kaotsimineku eest.
Varukoopia võimaldab taastada olukorra, kui uuenduse käigus tekib ootamatuid probleeme.

Varukoopia loomiseks Terminalis:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Release 2026.11 litsentsifaili taotlemine**

Release 2026.11 vajab uut faili `license.toml`. Taotlege see digna meeskonnalt enne alustamist ja
hoidke see [sammu 7](#step-7-replace-the-license-file) jaoks valmis.

### Uuenduse protsess

#### Samm 1: Peatage digna teenus {: #step-1-stop-the-digna-service }

Kui digna töötab taustateenusena, peatage see esmalt:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Kui digna töötab esiplaanil, vajutage selle Terminali aknas ++ctrl+c++.

#### Samm 2: Varundage praegune paigaldus {: #step-2-backup-current-installation }

Nimetage oma digna paigalduskataloogis praeguse paigalduse käivitatav fail ja kaust `dashboard`
ümber, et uut väljalaset saaks nende kõrvale paigaldada:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Hoidke `digna_old` alles, kuni olete uuenduse kontrollinud, ja `dashboard_old`, kuni olete sellest
oma konfiguratsioonifailid taastanud (vt samm 4). Seejärel võite mõlemad kustutada.

#### Samm 3: Pakige lahti ja juurutage uus versioon {: #step-3-extract-and-deploy-new-version }

1. Pakkige lahti uus digna paigaldus ZIP-fail
2. Kopeerige uus `digna` käivitatav fail ja `dashboard` kaust oma paigalduskataloogi
3. Taastage käivitusbit ja vajadusel eemaldage karantiini atribuut:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Oluline"

    Paigaldus-ZIP ei sisalda kunagi ei faili `config.toml` ega `dashboard/dashboard_config.toml`
    — digna meeskond ei tarni kumbagi faili. Seetõttu ei puuduta uuendus teie olemasolevat
    konfiguratsiooni ning ümbernimetatud `*_old` kaustades olevad koopiad on ainsad, mis teil on.

#### Samm 4: Taastage konfiguratsioonifailid {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 ei vaja muudatusi failis `config.toml`: fail, mis töötab Release 2026.06-ga,
töötab edasi. Kaks muudatust on valikulised:

- Lisage [`[duckdb]` sektsioon](#duckdb-section), kui andmebaasiühendused peavad kasutama
  komponenti digna Engine ja selle vaikeväärtused teie hostile ei sobi.
- Jätke sektsioon `[app]` ära, kui pöördpuhverserver serveerib armatuurlaua ja backendi ühe päritolu all.

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

Armatuurlaud koosneb staatilistest failidest, seega võivad teie veebiserver — ja brauser — ikka veel
serveerida eelmist versiooni. Laadige uuesti või taaskäivitage veebiserver, mis majutab kausta
`dashboard`, ning seejärel laadige leht sundvärskendusega uuesti (++cmd+shift+r++).

#### Samm 6: Kontrollige konfiguratsiooni {: #step-6-validate-the-configuration }

Veenduge enne hoidla puudutamist, et `config.toml` on täielik:

```bash
./digna config check
```

Iga sektsioon peab teatama OK. Parandage kõik, millest teatatakse FAILED, eemaldage rea
**Unknown keys** all loetletud võtmed ja käivitage käsk enne jätkamist uuesti.

#### Samm 7: Asendage litsentsifail {: #step-7-replace-the-license-file }

Varasema väljalaske jaoks väljastatud litsentsifail ei tööta Release 2026.11-ga. Kopeerige digna
meeskonna poolt Release 2026.11 jaoks antud `license.toml` paigalduskataloogi, asendades vana faili:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ärge jätke alles eelmist litsentsi"

    Eelmise litsentsiga ebaõnnestub iga käsk, mis litsentsi kontrollib — `serve`, `user`,
    `inspection`, `repo` —, seega digna ei käivitu ja hoidlat ei saa uuendada. Kontrollige uut
    litsentsi enne jätkamist:

    ```bash
    ./digna license check
    ```

#### Samm 8: Uuendage andmehoidla skeemi {: #step-8-upgrade-the-repository-schema }

Käivitage oma digna paigalduskataloogis:

```bash
cd /opt/digna
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

#### Samm 9: Taaskäivitage teenused {: #step-9-restart-services }

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

#### Samm 10: Kinnitage uuendus {: #step-10-verify-the-upgrade }

1. Kontrollige uue käivitatava faili väljalaset:

    ```bash
    ./digna version
    ```

    Esimene rida peab olema `Release: 2026.11`.

2. Avage digna armatuurlaud ja veenduge, et liides laadib korrektselt.
3. Kontrollige serveri väljundit ja kataloogi `logs` faile vigade suhtes.
4. Testige oma andmebaasiühendusi — vaadake
   [Ühenduse testimine](../../../databases/overview.md#testing-a-connection).

Uute moodulitega alustamiseks vaadake [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
digna MCP Serveri kohta [AI-agendi ühendamine](../../../platform/agentic/connect_ai_agent.md) ja
digna Engine'i kohta [Profileerimise asukoht](../../../platform/profiling/profiling_location.md).