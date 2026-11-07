# Linux-asennusopas digna Release 2026.11:lle

**Julkaisu:** 2026.11

**Viimeksi päivitetty:** 7. marraskuuta 2026


---

## Sisällysluettelo

1. [Johdanto](#introduction)
2. [Järjestelmävaatimukset](#system-requirements)
3. [Ennen asennusta](#pre-installation-setup)
4. [PostgreSQL-palvelimen asennus](#postgresql-server-setup)
5. [Web-palvelimen konfiguraatio](#web-server-configuration)
6. [Alustava asennus](#initial-installation)
7. [Backendin määritys](#backend-configuration)
8. [Dashboardin määritys](#dashboard-configuration)
9. [dignan ajaminen systemd-palveluna](#running-digna-as-a-systemd-service)
10. [Päivitys uuteen julkaisuun](#upgrading-to-a-new-release)

---

## Johdanto {: #introduction }

### Tietoa dignasta

digna on kattava tekoälyä hyödyntävä alusta, joka on suunniteltu optimoimaan datalaadun hallintaa erilaisissa data-ympäristöissä, kuten varastoissa, lammissa ja lakehouse-ympäristöissä. Suunniteltu erittäin skaalautuvaksi ja mukautuvaksi, digna vastaa moderneihin datahaasteisiin automaation, reaaliaikaisen valvonnan ja poikkeamien havaitsemisen avulla.

digna koostuu kahdesta pääosasta:

- **digna**: sovelluksen ydin, joka vastaa tietojen käsittelystä ja laatutarkistusten suorittamisesta. Se yhdistää taustajärjestelmän ja komentorivikäyttöliittymän yhteen suoritettavaan tiedostoon ja korvaa aiempien julkaisujen erilliset ohjelmat `dignabackend` ja `dignacli`.
- **dignadashboard**: Web-pohjainen käyttöliittymä, joka isännöidään web-palvelimella ja tarjoaa käyttäjäystävällisen tavan käyttää digna-alustaa ja visualisoida datalaatumittareita.

### Mitä uutta julkaisussa 2026.11

Tämä julkaisu tuo mukanaan digna Data Reconciliationin, digna Agenticin ja digna MCP Serverin sekä digna Enginen, joka voi profiloida dataa dignan sisällä ja tarkistaa viite-eheyden eri tietokantateknologioiden välillä. Katso täydet tiedot [release notes](../../../changelog/Release_202611.md).

Asennuksen kannalta julkaisu tuo uuden repositorion migraatiomekanismin, valinnaisen `[duckdb]`-osion `config.toml`-tiedostoon digna Engineä varten sekä uuden lisenssitiedoston. [Päivitysosio](#upgrading-to-a-new-release) käsittelee jokaisen niistä.

### Etsitkö Windows- tai macOS-ohjeita?

Tämä opas käsittelee Linuxia. Muille alustoille katso [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) tai [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md).

### Mitä jakelua tämä opas kattaa?

Ohjeet on kirjoitettu kahta yleisintä palvelinjakeluperhettä varten. Jos komennot eroavat, molemmat annetaan:

- **Debian-perhe** — Debian, Ubuntu. Paketinhallinta: `apt`.
- **RHEL-perhe** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Paketinhallinta: `dnf`.

Mikä tahansa nykyaikainen jakelu, jossa on `systemd`, toimii; ainoastaan pakettien nimet ja muutama konfiguraatiopolku vaihtelevat.

---

## Järjestelmävaatimukset {: #system-requirements }

Ennen asennuksen aloittamista varmista, että järjestelmäsi täyttää seuraavat vähimmäisvaatimukset:

| Vaatimus | Määrittely |
|---|---|
| **Käyttöjärjestelmä** | Ubuntu 22.04 LTS tai uudempi, Debian 12 tai uudempi, RHEL 9 / Rocky 9 / AlmaLinux 9 tai uudempi |
| **Arkkitehtuuri** | x86_64 (amd64) tai arm64 |
| **Init-järjestelmä** | systemd |
| **Muisti (minimi)** | 16 GB RAM |
| **Levytila** | 10 GB vapaata tallennustilaa |
| **Tietokanta** | PostgreSQL Server 12 tai uudempi |
| **Web-palvelin** | nginx, Apache httpd tai vastaava |

!!! info "digna Engine"

    Tietokantayhteydet, joiden profilointisijaintina on digna Engine, profiloidaan itse
    digna-isännällä. Varaa niille lisää muistia ja levytilaa, katso
    [\[duckdb\]-osio](#duckdb-section).

### Tietokannan asennusvaihtoehdot

**Jos PostgreSQL on jo asennettu:**
Voit lisätä uuden tietokannan dignalle olemassa olevaan PostgreSQL-palvelimeen.

**Jos asennat PostgreSQL:n samalle koneelle kuin digna:**

!!! info "Suositellut määritykset"

    - **Muisti**: 32 GB RAM (16 GB sijaan)
    - **Levytila**: 50 GB vapaata tallennustilaa (10 GB sijaan)

    Nämä suuremmat resurssit mahdollistavat sekä dignan että PostgreSQL-tietokannan samanaikaisen ajon.

### Jakelun ja arkkitehtuurin tarkistus

Tämän oppaan useat komennot eroavat Debian- ja RHEL-perheiden välillä. Tarkista jakelusi ja arkkitehtuuri ajamalla:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` tai `ID=debian` — käytä `apt`-komentoja.
- `ID=rhel`, `rocky`, `almalinux` tai `fedora` — käytä `dnf`-komentoja.
- `x86_64` tai `aarch64` — asennuspaketin tarvitsemasi arkkitehtuuri.

---

## Ennen asennusta {: #pre-installation-setup }

Ennen dignan asentamista varmista, että kaksi keskeistä edellytystä ovat kunnossa:

1. **PostgreSQL-palvelin** – lasketun mittariston ja suorituskykytietojen tallennusta varten
2. **Web-palvelin** – digna Dashboardin isännöintiä varten

Jos nämä komponentit eivät ole vielä valmiina, seuraa alla olevia osioita asentaaksesi ja konfiguroidaksesi ne.

### Pakettilistan päivittäminen

Päivitä pakettien listat ennen asennusta:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Huomautus"

    Tässä oppaassa ensimmäinen komento parissa on **Debian-perheelle** ja toinen **RHEL-perheelle**. Suorita vain järjestelmääsi vastaava komento.

---

## PostgreSQL-palvelimen asennus {: #postgresql-server-setup }

### Jos sinulla on jo PostgreSQL

Jos PostgreSQL on jo asennettu ja käynnissä paikallisella koneella tai käytät hallittua etä-PostgreSQL-palvelinta, voit siirtyä [seuraavaan osioon](#web-server-configuration).

### PostgreSQL:n asennus

#### Vaihe 1: Asenna palvelinpaketti

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Vinkki"

    Jakelupakettien versiot voivat olla jäljessä PostgreSQL:n uusimmasta julkaisusta. Jos tarvitset tiettyä uudempaa versiota, käytä virallista [PostgreSQL apt- tai yum-repositoryä](https://www.postgresql.org/download/linux/).

#### Vaihe 2: Alusta tietokantaklusteri

Debian-perheessä paketti luo ja käynnistää klusterin automaattisesti — siirry seuraavaan vaiheeseen.

RHEL-perheessä klusteri täytyy luoda eksplicitisti:

```bash
sudo postgresql-setup --initdb
```

#### Vaihe 3: Käynnistä ja ota palvelu käyttöön

```bash
sudo systemctl enable --now postgresql
```

Tämä käynnistää PostgreSQL:n välittömästi ja konfiguroi sen käynnistymään automaattisesti uudelleenkäynnistyksen yhteydessä.

#### Vaihe 4: Varmista asennus

```bash
psql --version
sudo systemctl status postgresql
```

Näet PostgreSQL-version ja `active (running)` -palvelun tilan.

#### Vaihe 5: Yhdistä palvelimeen

Linuxin PostgreSQL-paketti luo `postgres`-järjestelmätilin, joka omistaa klusterin. Yhdistä sen kautta:

```bash
sudo -u postgres psql
```

!!! note "Huomautus — Linux eroaa Windowsista tässä"

    Windowsin asennusohjelma pyytää salasanaa `postgres`-superkäyttäjälle asennuksen aikana. Linux-paketit eivät tee tätä. Sen sijaan paikalliset yhteydet todennetaan **peer authentication** -menetelmällä: `postgres`-käyttäjä käyttöjärjestelmässä saa yhdistää `postgres`-tietokantakäyttäjänä ilman salasanaa.

    Tästä syystä komento käyttää `sudo -u postgres`. digna-backend yhdistää TCP:n yli käyttäen käyttäjätunnusta ja salasanaa, joten luot erillisen digna-käyttäjän [Alustavassa asennuksessa](#initial-installation).

#### Vaihe 6: Vahvista portti

Oletus PostgreSQL-portti on `5432`. Varmista, mille portille palvelimesi kuuntelee:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Muista arvo — tarvitset sen digna-backendin konfiguroinnissa.

#### Vaihe 7: Ota salasana-autentikointi käyttöön digna-käyttäjälle

digna yhdistää PostgreSQL:ään TCP:n yli käyttäjänä `digna_user`, joka edellyttää salasana-autentikointia sen sijaan, että käytettäisiin peer/ident-autentikointia. Tarkista, että `pg_hba.conf` sallii sen.

Etsi tiedosto:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Avaa se editorissa ja varmista, että paikalliset TCP-rivit käyttävät `scram-sha-256` (tai vanhemmissa palvelimissa `md5`) `ident`-menetelmän sijaan:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Lataa PostgreSQL uudelleen muutoksen jälkeen:

```bash
sudo systemctl reload postgresql
```

!!! warning "Tärkeää"

    Jos digna raportoi `FATAL: Ident authentication failed for user "digna_user"`, tämä asetus on todennäköinen syy.

#### Vaihe 8: Jos PostgreSQL sijaitsee eri koneessa

Hyväksyäksesi yhteydet toisesta isännästä, aseta `listen_addresses` `postgresql.conf`-tiedostossa ja lisää vastaava `host`-rivi verkollesi `pg_hba.conf`-tiedostoon:

```
listen_addresses = '*'
```

Avaa sitten portti palomuurissa ja käynnistä palvelu uudelleen:

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

## Web-palvelimen konfiguraatio {: #web-server-configuration }

digna tarvitsee web-palvelimen dashboardin isännöintiin. Valitse yksi seuraavista vaihtoehdoista:

- [nginx](#nginx-setup) — kevyt ja suositeltava
- [Apache httpd](#apache-setup) — laajalti käytetty vaihtoehto

Tarvitset vain yhden näistä palvelimista.

Molemmat osiot konfiguroivat kaksi dashboardin tarvitsemaa asiaa:

- **Single-page application -varmistus**, jotta dashboardin URL:n uudelleenlataus ei palauta 404-virhettä
- **`.md` MIME-tyyppi**, jotta Markdown-tiedostot palvellaan oikein

### nginxin asennus {: #nginx-setup }

#### Yleiskatsaus

nginx on kevyt, suorituskykyinen web-palvelin, joka sopii hyvin staattisen digna-dashboardin tarjoamiseen.

#### Asennus

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### nginxin käynnistäminen

```bash
sudo systemctl enable --now nginx
```

#### Asennuksen tarkistus

1. Avaa selain
2. Mene osoitteeseen `http://localhost`
3. Näet nginx-tervetuliasivun

#### Palomuurin avaaminen

Jos palvelimeen tavoitellaan muilta koneilta, salli HTTP-liikenne:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Sivuston konfigurointi dashboardille

nginx lukee kaikki tiedostot `conf.d`-hakemistostaan molemmilla jakeluperheillä. Luo oma konfiguraatiotiedosto dignalle sinne:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Liitä seuraava, korvaten `/opt/digna/dashboard` todellisella polulla purettuun `dashboard`-kansioon:

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

!!! warning "Tärkeää"

    Ilman `try_files`-direktiiviä minkä tahansa muun dashboard-sivun kuin juuriosoite uudelleenlataus palauttaa 404-virheen. Tämä on nginxin vastaava toiminnallisuus URL Rewrite -moduulille, joka IIS:llä vaaditaan Windowsilla.

#### Poista oletussivusto käytöstä

Vain yksi server-lohko voi olla `default_server` portissa. Debian-perheessä poista paketoitu oletus, jotta se ei aiheuta ristiriitaa:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

RHEL-perheessä kommentoi tai poista `server { ... }` -lohko tiedostosta `/etc/nginx/nginx.conf`.

#### Ota konfiguraatio käyttöön

Tarkista syntaksi ja lataa nginx uudelleen:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Apache httpd:n asennus {: #apache-setup }

#### Yleiskatsaus

Apache httpd on saatavilla oletusarkistoista kaikissa tuetuissa jakeluissa. Paketin nimi on `apache2` Debian-perheessä ja `httpd` RHEL-perheessä.

#### Asennus

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Apachen käynnistäminen

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Asennuksen tarkistus

1. Avaa selain
2. Mene osoitteeseen `http://localhost`
3. Näet jakelun oletus Apachen sivun

#### Pakollinen: mod_rewritein ottaminen käyttöön

Dashboard vaatii URL-osoitteiden uudelleenkirjoituksen.

Debian-perheessä ota moduuli käyttöön ja käynnistä uudelleen:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

RHEL-perheessä `mod_rewrite` on yleensä ladattu oletuksena. Varmista se:

```bash
httpd -M | grep rewrite
```

#### Pakollinen: Salli .htaccess-ylikirjoitukset

Avaa dokumenttijuuren konfiguraatiotiedosto:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Etsi `<Directory>`-lohko, joka kattaa dokumenttijuuren (`/var/www/html` molemmilla perheillä) ja muuta:

```apache
AllowOverride None
```

muotoon:

```apache
AllowOverride All
```

#### Pakollinen: MIME-tyyppi Markdown-tiedostoille

Lisää samaan tiedostoon seuraava rivi, jotta Markdown-tiedostot palvellaan oikein:

```apache
AddType text/markdown .md
```

!!! warning "Tärkeää"

    Ilman tätä asetusta `.md`-tiedostoja ei välttämättä palvellakaan oikein.

#### Ota konfiguraatio käyttöön

Tarkista syntaksi ja käynnistä Apache uudelleen:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Alustava asennus {: #initial-installation }

### Vaihe 1: Luo dignan repositorio

digna-repositorio tallentaa kaikki dignan laskemat mittarit. Se toimii keskitettynä tietokantana analytiikka- ja suorituskykytiedoille.

#### Luo skeema ja käyttäjä

Avaa PostgreSQL-asiakas (psql, pgAdmin tai vastaava) ja suorita seuraavat SQL-komennot:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Korvaa seuraavat paikkamerkit:**

- `<digna_repo_schema>` — Haluttu skeeman nimi (esim. `dignarepo`)
- `<digna_repo_user>` — Haluttu käyttäjänimi (esim. `digna_user`)
- `<digna_repo_password>` — Turvallinen salasana tälle käyttäjälle

**Esimerkki:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Yhdellä komennolla kuoren kautta:

```bash
sudo -u postgres psql
```

Liitä sitten yllä olevat lauseet `postgres=#` -kehotteeseen ja kirjoita `\q` poistuaksesi.

!!! tip "Parhaat käytännöt"

    Käytä vahvoja, monimutkaisia salasanoja tietokantakäyttäjille. Vältä helposti arvattavia tunnuksia.

---

### Vaihe 2: Pura digna-asennuspaketti

1. Etsi sinulle toimitettu digna-asennus ZIP-tiedosto
2. Pura se haluamaasi asennushakemistoon — esimerkiksi `/opt/digna`
3. Purkamisen jälkeen sinun pitäisi nähdä seuraavat kohteet:
   - `dashboard/` — Web-dashboardin käyttöliittymä
   - `digna` — Pääsuoritettava tiedosto (backend + CLI yhdessä)

!!! info "Konfiguraatio- ja lisenssitiedostot eivät sisälly pakettiin"

    Asennuksen mukana ei toimiteta `config.toml`- eikä `dashboard/dashboard_config.toml`-tiedostoa — luot
    molemmat itse kohdissa [Backendin määritys](#backend-configuration) ja
    [Dashboardin määritys](#dashboard-configuration). Myöskään `license.toml` ei sisälly pakettiin;
    digna toimittaa sen erikseen, kuten vaiheessa 3 kuvataan.

Kuoren kautta purkaminen:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.11-linux-x86_64.zip -d /opt/digna
```

!!! note "Huomautus"

    Jos `unzip` ei ole asennettuna, lisää se komennolla `sudo apt install -y unzip` tai `sudo dnf install -y unzip`.

#### Tee suoritustiedostosta suoritettava

Riippuen siitä, miten arkisto on siirretty, suoritusoikeus ei ehkä säily purkamisen yhteydessä. Aseta se eksplisiittisesti:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Luo palvelutili

On suositeltavaa ajaa backend erillisenä ei-privilegioituna käyttäjänä tuotantoympäristöissä:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Huomautus"

    RHEL-perheessä vastaava shell-polku on `/sbin/nologin`.

### Vaihe 3: Asenna lisenssitiedosto

!!! warning "Tärkeää"

    Lisenssitiedostoa **ei** sisälly asennuspakettiin, vaan se toimitetaan erikseen dignalta.

1. Etsi sinulle toimitettu `license.toml`-tiedosto
2. Kopioi se dignan asennushakemiston juureen (kohtaan, jossa `config.toml` ja `digna`-suoritustiedosto sijaitsevat)

**Miksi tämä on tärkeää:**
Lisenssitiedosto sisältää asiakastietosi, lisenssin vanhenemispäivän ja digitaalisen allekirjoituksen. **Älä muokkaa tätä tiedostoa** — muutokset mitätöivät sen.

**Hakemistorakenne asennuksen jälkeen:**

```
/opt/digna/
├── config.toml         (konfiguraatiotiedosto)
├── license.toml        (OMA LISENSSITIEDOSTOSI - kopioi tänne)
├── digna               (pääsuoritettava)
├── bin/                (palvelunhallintaskriptit)
└── dashboard/          (web-käyttöliittymä)
    └── (dashboard-tiedostot)
```

---

## Backendin määritys {: #backend-configuration }

### Vaihe 1: Luo ja muokkaa konfiguraatiotiedostoa

`config_template.toml` -tiedosto toimitetaan dignan asennushakemistossa. Tarvitsee vain nimetä se `config.toml`-tiedostoksi.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Sijainti:** `/opt/digna/config.toml`

Avaa `config.toml` tekstieditorissa ja konfiguroi alla olevat osiot.

#### [app] -osio

Tässä osiossa määritetään dashboardin ja backendin välinen cross-origin resource sharing (CORS):

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboardin URL-osoitteet | URL-osoitteet, joista dashboard tarjoillaan. Selaimen pyynnöt mistä tahansa muusta originista hylätään |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Pakollinen, jotta selain lähettää istuntoevästeen jokaisen pyynnön mukana |

!!! note "Huomautus"

    Jos tarjoat dashboardin nginxin tai Apachen kautta oletus-HTTP-portissa, sallitun originin tulee olla `http://localhost` — tai palvelimen julkinen URL, jos dashboardiin pääsee muilta koneilta.

!!! info "[app]-osio on valinnainen"

    Release 2026.11:stä alkaen molemmat avaimet ja koko `[app]`-osio voidaan jättää pois. Tämä on
    oikea asetus, kun käänteinen välityspalvelin tarjoaa dashboardin ja backendin saman originin alla:
    selain ei silloin tee cross-origin-pyyntöjä, eikä niitä oletusarvoisesti sallita.

#### [repo] -osio

Tämä osio määrittää yhteyden PostgreSQL-tietokantaan:

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

| Parametri | Arvo | Huomio |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` tai IP | PostgreSQL-palvelimen isäntä/IP |
| `DIGNA_REPO_PORT` | `5432` (oletus) | PostgreSQL-portti |
| `DIGNA_REPO_DB` | `postgres` | Tietokannan nimi |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Aiemmin luotu skeema |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQL:ssä luotu käyttäjä |
| `DIGNA_REPO_PASSWORD` | Salasanasi | Skeeman luomisessa asetettu salasana |
| `DIGNA_REPO_SSLMODE` | `prefer` (oletus) | Valinnainen. PostgreSQL:n SSL-tila: `disable`, `allow`, `prefer`, `require`, `verify-ca` tai `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (oletus) | Valinnainen. Yhteyksien määrä, jonka digna pitää avoinna repositorioon |

!!! tip "Parhaat käytännöt"

    `config.toml` sisältää tietokantasalasanan selväkielisenä. Rajoita tiedoston lukuoikeudet niin, että vain palvelutili voi lukea sen:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] -osio

Tämä osio sisältää suojaus-, eväste- ja tarkastusasetukset:

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

| Parametri | Arvo | Huomio |
|---|---|---|
| `DIGNA_FERNET_KEY` | Yllä näytetty arvo | Aiempien julkaisujen käyttämän salauksen avain. Sen on oltava mukana; säilytä näytetty arvo |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Isäntä, jonka kautta dashboardia käytetään. `""` ei aseta domainia, mikä on oikein välityspalvelimen takana, joka tarjoaa dashboardin ja backendin saman originin alla |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Oltava `true` aina, kun dignaa tarjoillaan HTTPS:n kautta |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Pitää istuntoevästeen skriptien ulottumattomissa |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon vanhenemisaika sekunteina |
| `DIGNA_MAX_WORKERS` | CPU-ydinten määrä - 1 | Samanaikaisesti ajettavien tarkastusten enimmäismäärä |
| `DIGNA_FRONTEND_BASEURL` | Dashboardin URL | Pakollinen. Käytetään ilmoitusviestien linkeissä, joten sen on oltava URL, jonka vastaanottajat voivat avata |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (oletus) | Valinnainen. Sekunnit, joiden ajan yksittäinen lähdetietokantaan kohdistuva kysely saa olla käynnissä ennen keskeytystä; `0` poistaa aikakatkaisun käytöstä |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (oletus) | Valinnainen. Sekunnit, joiden ajan lähdetietokantayhteyttä odotetaan; `0` odottaa rajattomasti |

!!! tip "Vinkki"

    Selvittääksesi palvelimen CPU-ytimet aja `nproc`.

#### [encryption] -osio

Tämä osio sisältää avaimen, jolla arkiston arkaluontoiset arvot salataan. Se on **pakollinen** — `config check` raportoi osion `[encryption]` tilassa FAILED, jos avain puuttuu.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Base64-koodattu avain | Salaa digna-arkistoon tallennetut arkaluontoiset arvot |

!!! warning "Suojaa config.toml"

    Tämä avain on kiinteä arvo, joka on sama kaikissa digna-asennuksissa, ja juuri se purkaa arkistosi arkaluontoisten arvojen salauksen. Rajaa `config.toml` sille tilille, jolla digna toimii, pidä tiedosto poissa versionhallinnasta ja jaetuilta levyiltä, ja jätä se pois jokaisesta varmuuskopiosta, jota säilytetään vähemmän turvallisesti kuin itse arkistoa.

#### [logging] -osio

Tämä osio määrittää lokituksen käyttäytymisen:

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotannolle, `DEBUG` vianetsintään. Myös `TRACE`, `WARN` ja `ERROR` hyväksytään |
| `DIGNA_LOGGING_DIR` | `logs` (oletus) | Valinnainen. Kiertävien lokitiedostojen hakemisto suhteessa työhakemistoon |
| `DIGNA_LOGGING_MAX_FILES` | `30` (oletus) | Valinnainen. Säilytettävien kierrätettyjen lokitiedostojen määrä |

#### [duckdb] -osio (valinnainen) {: #duckdb-section }

Uutta Release 2026.11:ssä. Tämä osio määrittää **digna Enginen** resurssit. digna Engine profiloi
dataa dignan sisällä niille tietokantayhteyksille, joiden profilointisijainti on **digna Engine**, ja
suorittaa viite-eheystarkistuksia eri tietokantayhteyksien tietolähteiden välillä. Katso
[Profilointisijainti](../../../platform/profiling/profiling_location.md).

Osio on valinnainen. Ilman sitä käytetään alla olevia oletusarvoja.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (oletus) | Muisti megatavuina, jota yksi digna Engine -ajo saa käyttää. Enintään `DIGNA_MAX_WORKERS` ajoa voi olla käynnissä samanaikaisesti |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Oletus: järjestelmän väliaikaishakemisto (`$TMPDIR`, tai `/tmp`, jos sitä ei ole asetettu) | Väliaikaistiedostojen hakemisto, kun data ei mahdu muistiin |

!!! tip "digna Enginen mitoitus"

    Varaa digna-isännälle enintään `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` muistia
    dignan oman muistinkäytön lisäksi, ja väliaikaishakemistoon riittävästi vapaata levytilaa
    suurimmalle tarkastetulle päivämäärälle niistä tietolähteistä, jotka käyttävät digna Engineä.
    Osoita `DIGNA_DUCKDB_TEMP_DIRECTORY` levylle, jolla on tämä tila ja johon dignaa ajava tili
    voi kirjoittaa:

    ```bash
    sudo mkdir -p /opt/digna/tmp
    sudo chown digna:digna /opt/digna/tmp
    ```

    Tarvitset tätä osiota vain, jos vähintään yksi tietokantayhteys käyttää digna Engineä tai
    viite-eheystarkistus vertaa eri yhteyksien tietolähteitä.

---

### Vaihe 2: Tarkista konfiguraatio

Varmista ennen arkiston alustusta, että `config.toml` on täydellinen ja oikein muodostettu. Suorita digna-asennushakemistossasi:

```bash
./digna config check
```

Jokainen osio tarkistetaan erikseen, joten yksittäinen virhe ei peitä muiden tilaa:

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

Korjaa kaikki, mikä raportoidaan tilassa FAILED, ja suorita komento uudelleen ennen jatkamista. Kohdan **Unknown keys** alla oleva WARNING luettelee `config.toml`-tiedoston avaimet, joita digna ei lue; niillä ei ole vaikutusta, joten poista ne tai korjaa niiden kirjoitusasu. Täydellinen luettelo valinnoista on [CLI-viitteessä](../../../cli/Command_Line_Interface_202611.md).

### Vaihe 3: Alusta repositorioyhteys

1. Avaa terminaali
2. Siirry dignan asennushakemistoon (jossa `config.toml` ja `digna`-suoritustiedosto sijaitsevat)
3. Suorita yhteystarkistus:

```bash
cd /opt/digna
./digna repo check
```

Uudessa skeemassa komento muodostaa yhteyden ja ilmoittaa sitten, ettei repositoriota ole vielä asennettu:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Tässä vaiheessa tämä on odotettu tulos: se vahvistaa, että digna tavoittaa PostgreSQL:n ja skeeman. Yhteys- tai todennusvirhe sen sijaan viittaa `[repo]`-osioon tai PostgreSQL-asetuksiin.

!!! note "Huomautus"

    Linuxissa nykyinen hakemisto ei ole PATH:ssa, joten suoritettava tiedosto käynnistetään muodossa `./digna` eikä `digna`. Lyhyemmän muodon käyttämiseksi kaikkialta voit tehdä symbolisen linkin:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Vaihe 4: Asenna repositorion skeema

Sama hakemisto auki, suorita:

```bash
./digna repo upgrade
```

Tämä komento asentaa tarvittavat taulut repositorion skeemaan ja päättyy ilmoitukseen:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade asentaa ja päivittää"

    Release 2026.11:stä alkaen `repo upgrade` asentaa uuden repositorion ja päivittää olemassa olevan.
    `repo install` toimii edelleen saman komennon toisena nimenä.

### Vaihe 5: Luo ylläpitäjäkäyttäjä

1. Avaa **uusi** terminaali-ikkuna
2. Siirry dignan asennushakemistoon
3. Suorita seuraava komento luodaksesi ylläpitäjäkäyttäjän:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Esimerkki:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Tämä luo käyttäjän sähköpostiosoitteella `admin@example.com` ja täysillä järjestelmänvalvojan oikeuksilla.

!!! tip "Vinkki"

    Lisää salasana yksinkertaisesti yksinkertaisiin lainausmerkkeihin. `bash` ja `zsh` käsittelevät merkkejä kuten `!`, `$` ja `*` erikoismerkkeinä, joten lainausmerkit varmistavat, että salasana välittyy oikein.

!!! tip "Parhaat käytännöt"

    Käytä vahvaa salasanaa, jossa on isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä.

---

### Vaihe 6: Käynnistä digna-palvelin

Dignan asennushakemistossa käynnistä palvelin komennolla:

```bash
./digna serve --address <host> --port <port>
```

**Parametrit:**
- `--address` — Palvelimen hostname/IP (oletus `127.0.0.1`)
- `--port` — Palvelimen portti (oletus `8000`)

Kun palvelin on käynnissä, se tulostaa osoitteen, jota se kuuntelee:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Vinkki"

    Jos dashboard tarjotaan eri koneelta kuin backend, avaa myös API-portti palomuurissa:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Palvelin varaa päätteen"

    `serve` toimii edustalla ja jatkaa, kunnes pysäytät sen näppäinyhdistelmällä ++ctrl+c++. Anna sen olla käynnissä, kun viimeistelet asennuksen; automaattisen käynnistyksen osalta katso [dignan suorittaminen systemd-palveluna](#running-digna-as-a-systemd-service).

## Dashboardin määritys {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön web-palvelimella

digna-dashboard lukee oman konfiguraationsa tiedostosta `dashboard/dashboard_config.toml`. Tätä tiedostoa ei toimiteta asennuksen mukana — luot sen `dashboard/`-hakemistoon dashboardin tiedostojen rinnalle.

Sen sisältö on kuvattu kohdassa [Yhden kirjautumisen (SSO) yleiskatsaus](../../../sso/overview.md), jossa tiedostoa myös tarvitaan: se sisältää dashboardin tarjoamat kirjautumisvaihtoehdot ja monen instanssin käyttöönotoissa backend-yhteyden.

Valitse web-palvelimesi ja seuraa vastaavia käyttöönotto-ohjeita.

#### Käyttöönotto nginxillä

Jos seurasit [nginxin asennusta](#nginx-setup), server-lohko osoittaa jo `dashboard`-kansioosi eikä kopiointia tarvita.

1. **Varmista polku**
   - Avaa `/etc/nginx/conf.d/digna.conf`
   - Varmista, että `root` osoittaa purettuun `dashboard`-kansioon

2. **Varmista, että kansio on luettavissa**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Lataa nginx uudelleen**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Testaa asennus**
   - Avaa selain
   - Mene osoitteeseen `http://localhost` (tai konfiguroituun URL:iin)
   - Näet digna-dashboardin kirjautumissivun

#### Käyttöönotto Apachella

1. **Kopioi dashboard dokumenttijuureen**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Lisää uudelleenkirjoitussäännöt**

   Luo `.htaccess`-tiedosto asennettuun kansioon, jotta dashboardin reitit säilyvät sivun uudelleenlatauksen aikana:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Liitä seuraava sisältö:

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

3. **Käynnistä Apache uudelleen**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Avaa dashboard**
   - Avaa selain
   - Mene osoitteeseen `http://localhost/digna`
   - Näet digna-dashboardin kirjautumissivun

### Vaihe 2: SELinux (vain RHEL-perhe)

RHEL:ssä, Rockyssä, AlmaLinuxissa ja Fedoressa SELinux on oletuksena päällä (enforcing) ja estää web-palvelinta lukemasta tiedostoja odotetuista sijainneista. Tarkista onko se aktiivinen:

```bash
getenforce
```

Jos tulos on `Enforcing` ja tarjoat dashboardia `/opt/digna/dashboard` -kansiosta, leimaa hakemisto jotta web-palvelin voi lukea sitä:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Huomautus"

    Jos `semanage` ei löydy, asenna se komennolla `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Tärkeää"

    Jos dashboard palauttaa **403 Forbidden** vastauksena täysin juuri konfiguroidulla RHEL-palvelimella, se on lähes aina SELinux-leimauksen ongelma eikä tiedostojen käyttöoikeusongelma. Varmista tilanne komennolla `sudo ausearch -m avc -ts recent`.

---

## dignan ajaminen systemd-palveluna {: #running-digna-as-a-systemd-service }

### Miksi ajaa digna palveluna?

digna-backendin ajaminen systemd-palveluna varmistaa, että se:

- Käynnistyy automaattisesti koneen käynnistyessä
- Ajetaan taustalla ilman avointa terminaali-ikkunaa
- Käynnistyy automaattisesti uudelleen kaatumisen jälkeen
- On hallittavissa `systemctl`-komennolla, joka on standardi Linux-palvelunhallinta

### Palvelunhallintatiedostot

Kaikki tarvittavat tiedostot löytyvät dignan asennushakemistosta kansiosta: `bin/`

Seuraavat shell-skriptit ovat käytettävissä:

- `install_service.sh` — Rekisteröi dignan systemd:hen
- `uninstall_service.sh` — Poistaa rekisteröinnin
- `start_service.sh` — Käynnistää rekisteröidyn palvelun
- `stop_service.sh` — Pysäyttää käynnissä olevan palvelun

!!! warning "Vaaditaan root-oikeudet"

    Kaikki skriptit on suoritettava `sudo`-oikeuksin, koska palvelun rekisteröinti, joka käynnistyy bootissa, kirjoittaa yksikkötiedoston kansioon `/etc/systemd/system`.

### Tee skripteistä suoritettavia

Purkaminen ei välttämättä säilytä suoritusoikeuksia. Ennen ensimmäistä käyttökertaa:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Palvelun asennus

1. **Avaa terminaali**

2. **Siirry bin-kansioon**
   ```bash
   cd /opt/digna/bin
   ```

3. **Suorita asennusskripti**
   ```bash
   sudo ./install_service.sh
   ```

digna-palvelin on nyt rekisteröity systemd:hen automaattisella käynnistyksellä. Palvelu ei välttämättä käynnisty heti — katso seuraavaa osiota käynnistystä varten.

### Palvelun käynnistäminen ja pysäyttäminen

#### Palvelun käynnistäminen

1. Avaa terminaali
2. Siirry `/opt/digna/bin`-hakemistoon
3. Suorita:
   ```bash
   sudo ./start_service.sh
   ```

#### Palvelun pysäyttäminen

1. Avaa terminaali
2. Siirry `/opt/digna/bin`-hakemistoon
3. Suorita:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Vinkki"

    Pysäytä aina palvelu ennen sovellustiedostojen päivittämistä.

### Palvelun hallinta systemctl:llä

Kun palvelu on rekisteröity, sitä voi hallita myös standardeilla systemd-komennoilla mistä tahansa hakemistosta:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Palvelun vahvistus

Varmista, että palvelu on rekisteröity ja käynnissä:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` tarkoittaa, että palvelu käynnistyy bootissa; `active` tarkoittaa, että se on käynnissä juuri nyt.

### Palvelulokit

systemd tallentaa kaiken, mitä backend kirjoittaa konsoliin. Lue lokit:

```bash
sudo journalctl -u digna -n 100
```

Seuraa lokia reaaliaikaisesti toistaen ongelman:

```bash
sudo journalctl -u digna -f
```

!!! tip "Vinkki"

    Tämä on nopein tapa diagnosoida palvelua, joka käynnistyy ja sammuu välittömästi. Repositorion yhteysvirhe tai puuttuva `license.toml` raportoidaan täällä.

### Siirto uuteen hakemistoon

Yksikkötiedosto tallentaa absoluuttisen polun suoritettavaan tiedostoon, joten asennuksen siirto edellyttää palvelun uudelleenrekisteröintiä:

1. **Poista nykyinen palvelu**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Siirrä sovellustiedostot**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Asenna palvelu uudelleen**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Käynnistä palvelu**
   ```bash
   sudo ./start_service.sh
   ```

### Palvelun poistaminen

1. **Pysäytä käynnissä oleva palvelu**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Poista palvelu**
   ```bash
   sudo ./uninstall_service.sh
   ```

digna-palvelin on nyt poistettu systemd:stä.

---

## Päivitys uuteen julkaisuun {: #upgrading-to-a-new-release }

Tämä osio päivittää Release 2026.06 -asennuksen versioon Release 2026.11. Jos asennuksesi on
vanhempi, lue ensin [Päivitys julkaisua 2026.06 vanhemmasta versiosta](#upgrading-from-a-release-before-2026-06).

### Ennen päivitystä

**digna-repositorion varmuuskopiointi on pakollista**

Ennen dignan päivittämistä, varmuuskopioi repositoriosi (PostgreSQL) datan menetyksen varalta.
Varmuuskopio mahdollistaa palautuksen, jos päivityksessä ilmenee odottamattomia ongelmia.

Luo varmuuskopio kuoren kautta:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Lisenssitiedoston pyytäminen Release 2026.11:tä varten**

Release 2026.11 vaatii uuden `license.toml`-tiedoston. Pyydä se digna-tiimiltä ennen aloittamista ja
pidä se valmiina [vaihetta 7](#step-7-replace-the-license-file) varten.

### Päivitys julkaisua 2026.06 vanhemmasta versiosta {: #upgrading-from-a-release-before-2026-06 }

Release 2026.06 toi kolme muutosta, jotka ovat yhä voimassa, kun päivität vanhemman asennuksen
suoraan versioon 2026.11:

- **Vain ODBC.** digna tavoittaa jokaisen lähdeteknologian ODBC:n kautta. Jokainen tietokantayhteys, joka
  ei vielä käytä ODBC:tä, on muutettava ODBC:ksi päivityksen jälkeen; automaattista
  muunnosta ei ole. Asenna ODBC-ajurit digna-isäntään etukäteen, katso
  [ODBC-ajurin asentaminen digna-isäntään](../../../databases/overview.md#install-the-driver),
  ja pidä kunkin yhteyden ominaisuudet valmiina
  [teknologiaoppaista](../../../databases/overview.md#technology-guides). Databricks Legacy -liitintä
  ei enää ole; siirrä nämä yhteydet
  [Databricks](../../../databases/databricks_connector_guide.md)-liittimeen.
- **Yksi suoritettava tiedosto.** `dignabackend` ja `dignacli` on korvattu yhdellä suoritettavalla tiedostolla `digna`,
  joka yhdistää backendin ja CLI:n.
- **config.toml.** `[encryption]`-osio on pakollinen, eikä `DIGNA_APP_HOST`- ja
  `DIGNA_APP_PORT`-asetuksia enää lueta: palvelin saa osoitteensa ja porttinsa komennolta `digna serve`.
  Vertaa tiedostoasi kohtaan [Backendin määritys](#backend-configuration).

Alla olevat vaiheet kertovat, missä vanhempi asennus vaatii jotain muuta. Vaiheen 8 repositorion
päivitys tuo minkä tahansa aiemman julkaisun repositorion suoraan versioon 2026.11.

### Päivitysprosessi

#### Vaihe 1: Pysäytä digna-palvelu {: #step-1-stop-the-digna-service }

Jos digna ajetaan systemd-palveluna, pysäytä se ensin:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jos digna ajetaan etualalla, paina ++ctrl+c++ sen terminaali-ikkunassa.

#### Vaihe 2: Varmuuskopioi nykyinen asennus {: #step-2-backup-current-installation }

Nimeä digna-asennushakemistossa nykyisen asennuksen suoritettava tiedosto ja dashboard-kansio uudelleen,
jotta uusi julkaisu voidaan ottaa käyttöön niiden rinnalle:

```bash
cd /opt/digna
sudo mv digna digna_old
sudo mv dashboard dashboard_old
```

Säilytä `digna_old`, kunnes olet varmistanut päivityksen, ja `dashboard_old`, kunnes olet palauttanut
siitä konfiguraatiotiedostosi (katso vaihe 4). Sen jälkeen voit poistaa molemmat.

!!! info "Päivitys julkaisua 2026.06 vanhemmasta versiosta"

    Nimeä suoritettavan tiedoston sijaan uudelleen kansiot `dignabackend` ja `dignacli`:
    `sudo mv dignabackend dignabackend_old` ja `sudo mv dignacli dignacli_old`. Release 2026.11 ei käytä kumpaakaan.

#### Vaihe 3: Pura ja ota uusi versio käyttöön {: #step-3-extract-and-deploy-new-version }

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritustiedosto ja `dashboard`-kansio asennushakemistoon
3. Palauta suoritusoikeus ja palvelutilin omistus:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Tärkeää"

    Asennuksen ZIP-tiedostoon ei koskaan sisällytetä `config.toml`- eikä `dashboard/dashboard_config.toml`-tiedostoa
    — digna-tiimi ei koskaan toimita kumpaakaan tiedostoa. Päivitys ei siksi koske olemassa olevaan
    konfiguraatioosi, ja uudelleennimetyissä `*_old`-kansioissa olevat kopiot ovat ainoat, jotka sinulla on.

#### Vaihe 4: Palauta konfiguraatiotiedostosi {: #step-4-restore-your-configuration-files }

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

Release 2026.11 ei vaadi muutoksia `config.toml`-tiedostoon: tiedosto, joka toimii Release 2026.06:n kanssa,
toimii edelleen. Kaksi muutosta on valinnaisia:

- Lisää [`[duckdb]`-osio](#duckdb-section), jos tietokantayhteyksien on määrä käyttää digna Engineä
  eivätkä sen oletusarvot sovi isännällesi.
- Jätä `[app]`-osio pois, jos käänteinen välityspalvelin tarjoaa dashboardin ja backendin saman
  originin alla.

!!! warning "Asetukset, joita digna ei lue"

    Tämän oppaan aiemmissa versioissa näytettiin joitakin asetuksia, joita digna ei lue. Niillä ei ole
    vaikutusta, ja `config check` luettelee ne kohdan **Unknown keys** alla vaiheessa 6. Poista tai korjaa
    ne:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` ja
      `digna_LOGGING_BACKUP_COUNT` eivät ole olemassa. Poista ne.
    - Asetusten nimissä isot ja pienet kirjaimet erotetaan. digna lukee `DIGNA_REPO_HOST`, ei `digna_REPO_HOST`.
      Kirjoita jokainen nimi isoin kirjaimin, kuten kohdassa [Backendin määritys](#backend-configuration).

!!! warning "Kertakirjautuminen: säilytä [[oidc_clients]]"

    digna lukee kertakirjautumisen palveluntarjoajat `[[oidc_clients]]`-merkintöjen luettelona, jossa jokaisella
    on oma `DIGNA_OIDC_KEY`. Jos muutit palveluntarjoajasi `[oidc_clients.<key>]`-osioiksi, kuten tämän
    oppaan aiempi versio näytti, muuta ne takaisin. `config check` raportoi
    `OIDC config(s)` tilassa FAILED niin kauan kuin tämä muoto on paikallaan:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Toista merkintä jokaiselle palveluntarjoajalle ja pidä jokainen `DIGNA_OIDC_KEY` samana kuin `key`
    tiedostossa `dashboard_config.toml`. Tämä koskee vain asennuksia, jotka käyttävät kertakirjautumista.

#### Vaihe 5: Lataa web-palvelin uudelleen {: #step-5-reload-the-web-server }

Dashboard koostuu staattisista tiedostoista, joten web-palvelimesi — ja selain — saattaa yhä
tarjoilla edellistä versiota. Lataa uudelleen tai käynnistä uudelleen se web-palvelin, joka isännöi `dashboard`-kansiota,
ja lataa sitten sivu uudelleen pakotetulla päivityksellä (++ctrl+f5++).

#### Vaihe 6: Tarkista konfiguraatio {: #step-6-validate-the-configuration }

Varmista, että `config.toml` on täydellinen ennen kuin kosket arkistoon:

```bash
./digna config check
```

Jokaisen osion on raportoitava OK. Korjaa kaikki, mikä raportoidaan tilassa FAILED, poista kohdan
**Unknown keys** alla luetellut avaimet ja suorita komento uudelleen ennen jatkamista.

#### Vaihe 7: Vaihda lisenssitiedosto {: #step-7-replace-the-license-file }

Lisenssitiedosto siirtyy yleensä julkaisusta seuraavaan. Release 2026.11 on
poikkeus: se lisää kaksi lisensoitua moduulia, digna Data Reconciliationin ja digna Agenticin, eikä
ennen versiota 2026.11 myönnetty lisenssi sisällä niitä. Kopioi digna-tiimin Release 2026.11:tä varten
toimittama `license.toml` asennushakemistoon vanhan tiedoston tilalle:

```bash
sudo cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Älä säilytä edellistä lisenssiä"

    Edellisellä lisenssillä digna käynnistyy yhä, mutta digna Data Reconciliation ja digna
    MCP Server pysyvät pois päältä. Jokainen komento, joka tarkistaa lisenssin — `user`,
    `inspection`, `repo` — keskeytyy ennen repositorion koskettamista, jos tarkistus epäonnistuu. Tarkista
    uusi lisenssi ennen kuin jatkat:

    ```bash
    ./digna license check
    ```

#### Vaihe 8: Päivitä repositorion skeema {: #step-8-upgrade-the-repository-schema }

Suorita dignan asennushakemistossa:

```bash
cd /opt/digna
./digna repo upgrade
```

Release 2026.11 hallitsee repositorion skeemaa versioitujen migraatioiden avulla. Ensimmäinen päivitys
aiemmasta julkaisusta tuo skeeman edellisen järjestelmän viimeiseen versioon, kirjaa sen
lähtökohdakseen ja soveltaa sitten Release 2026.11:n migraatiot. Se päättyy ilmoituksiin:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Kaikki olemassa olevat tiedot säilyvät. Näet repositorion tilan milloin tahansa komennolla
`./digna repo check`: se luettelee viimeisimmän sovelletun migraation ja mahdolliset odottavat migraatiot.

!!! warning "digna ei käynnisty vanhentuneella repositoriolla"

    Release 2026.11:stä alkaen palvelin kieltäytyy käynnistymästä niin kauan kuin repositorio vaatii päivityksen, ja
    ilmoittaa siitä, esimerkiksi:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Suorita `repo upgrade` ennen kuin käynnistät palvelimen tai palvelun.

#### Vaihe 9: Käynnistä palvelut uudelleen {: #step-9-restart-services }

Jos ajetaan systemd-palveluna:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Jos ajettiin manuaalisesti, käynnistä palvelin uudelleen:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Jos käytät nginx:iä tai Apachea, lataa vastaava web-palvelin uudelleen:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

RHEL-perheessä, jos `dashboard`-hakemisto korvattiin, aseta SELinux-leimat uudelleen:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Vaihe 10: Vahvista päivitys {: #step-10-verify-the-upgrade }

1. Vahvista uuden suoritettavan tiedoston julkaisu:

    ```bash
    ./digna version
    ```

    Ensimmäisen rivin on oltava `Release: 2026.11`.

2. Avaa digna-dashboard ja varmista, että käyttöliittymä latautuu oikein.
3. Tarkista palvelinlokit virheiden varalta:

    ```bash
    sudo journalctl -u digna -n 100
    ```

4. Testaa tietokantayhteytesi — katso
   [Yhteyden testaaminen](../../../databases/overview.md#testing-a-connection). Jos päivitit
   julkaisua 2026.06 vanhemmasta versiosta, muuta ensin jokainen yhteys, joka ei vielä käyttänyt ODBC:tä,
   ODBC:ksi.

Uusien moduulien käytön aloittamiseen katso [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI-agentin yhdistäminen](../../../platform/agentic/connect_ai_agent.md) digna MCP Serveriä varten ja
[Profilointisijainti](../../../platform/profiling/profiling_location.md) digna Engineä varten.