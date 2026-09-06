# Linux-asennusopas digna Release 2026.06:lle

**Julkaisu:** 2026.06

**Viimeksi päivitetty:** 5. syyskuuta 2026


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

- **dignabackend**: Sovelluksen ydinmoottori, joka vastaa datan käsittelystä ja laadun tarkistuksista.
- **dignadashboard**: Web-pohjainen käyttöliittymä, joka isännöidään web-palvelimella ja tarjoaa käyttäjäystävällisen tavan käyttää digna-alustaa ja visualisoida datalaatumittareita.

### Mitä uutta julkaisussa 2026.06

Tässä julkaisussa datan observoitavuusominaisuudet tuodaan suoraan koodiin, jolloin kehittäjät voivat valvoa datan laatua lähteellä. Katso täydet tiedot [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Etsitkö Windows- tai macOS-ohjeita?

Tämä opas käsittelee Linuxia. Muille alustoille katso [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) tai [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

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
   - `config.toml` — Konfiguraatiotiedosto
   - `license.toml` — Lisenssitiedosto (kopioi oma tiedostosi tähän)

Kuoren kautta purkaminen:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
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

Tässä osiossa määritetään digna-backendin sovellusasetukset:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `digna_APP_HOST` | `localhost` tai IP-osoite | Isäntä, jossa dignabackend ajetaan |
| `digna_APP_PORT` | `8082` (oletus) | REST API:n portti |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendin URL | Jos dashboard on eri palvelimella, lisää sen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vaaditaan CORS:lle kun käytetään tunnisteita |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Salli kaikki HTTP-metodit |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Salli kaikki otsikot |

!!! note "Huomautus"

    Jos tarjoat dashboardin nginxin tai Apachen kautta oletus-HTTP-portissa, sallitun originin tulee olla `http://localhost` — tai palvelimen julkinen URL, jos dashboardiin pääsee muilta koneilta.

#### [repo] -osio

Tämä osio määrittää yhteyden PostgreSQL-tietokantaan:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `digna_REPO_HOST` | `localhost` tai IP | PostgreSQL-palvelimen isäntä/IP |
| `digna_REPO_PORT` | `5432` (oletus) | PostgreSQL-portti |
| `digna_REPO_DB` | `postgres` | Tietokannan nimi |
| `digna_REPO_SCHEMA` | `dignarepo` | Aiemmin luotu skeema |
| `digna_REPO_USER` | `digna_user` | PostgreSQL:ssä luotu käyttäjä |
| `digna_REPO_PASSWORD` | Salasanasi | Skeeman luomisessa asetettu salasana |

!!! tip "Parhaat käytännöt"

    `config.toml` sisältää tietokantasalasanan selväkielisenä. Rajoita tiedoston lukuoikeudet niin, että vain palvelutili voi lukea sen:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

#### [base] -osio

Tämä osio sisältää suojaus- ja evästeasetukset:

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

| Parametri | Arvo | Huomio |
|---|---|---|
| `digna_FERNET_KEY` | Salausavain | Käytetään tokenien ja evästeiden salaamiseen (oletusarvo saatavilla) |
| `digna_COOKIE_DOMAIN` | `localhost` | Vastaa frontendin domainia |
| `digna_COOKIE_SECURE` | `false` (paikallinen) / `true` (tuotanto) | Käytä `true` HTTPS-yhteyksissä |
| `digna_COOKIE_HTTPONLY` | `true` | Aina päällä turvallisuuden takia |
| `digna_COOKIE_SAME_SITE` | `lax` | Estää CSRF-hyökkäyksiä |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon vanhenemisaika sekunteina |
| `digna_MAX_WORKERS` | CPU-ydinten määrä - 1 | Samanaikaisten tarkastustehtävien määrä |

!!! tip "Vinkki"

    Selvittääksesi palvelimen CPU-ytimet aja `nproc`.

#### [logging] -osio

Tämä osio määrittää lokituksen käyttäytymisen:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotannolle, `DEBUG` vianetsintään |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Säilytettävien päivittäisten lokavarotoimintojen määrä |

---

### Vaihe 2: Alusta repositorioyhteys

1. Avaa terminaali
2. Siirry dignan asennushakemistoon (jossa `config.toml` ja `digna`-suoritustiedosto sijaitsevat)
3. Suorita yhteystarkistus:

```bash
cd /opt/digna
./digna repo check
```

Saat vahvistuksen, että yhteys on muodostettu (varsinainen repositorio ei ole vielä alustettu).

!!! note "Huomautus"

    Linuxissa nykyinen hakemisto ei ole PATH:ssa, joten suoritettava tiedosto käynnistetään muodossa `./digna` eikä `digna`. Lyhyemmän muodon käyttämiseksi kaikkialta voit tehdä symbolisen linkin:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Vaihe 3: Asenna repositorion skeema

Sama hakemisto auki, suorita:

```bash
./digna repo install
```

Tämä komento asentaa tarvittavat taulut ja skeeman PostgreSQL-tietokantaan.

### Vaihe 4: Käynnistä digna-palvelin

Dignan asennushakemistossa käynnistä palvelin komennolla:

```bash
./digna serve --address <host> --port <port>
```

**Parametrit:**
- `--address` — Palvelimen hostname/IP
- `--port` — Palvelimen portti

Näet käynnistysviestit, jotka vahvistavat palvelimen olevan käynnissä:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Vinkki"

    Jos dashboard tarjotaan eri koneelta kuin backend, avaa myös API-portti palomuurissa:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Vaihe 5: Luo ylläpitäjäkäyttäjä

1. Avaa **uusi** terminaali-ikkuna
2. Siirry dignan asennushakemistoon
3. Suorita seuraava komento luodaksesi ylläpitäjäkäyttäjän:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Esimerkki:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Tämä luo käyttäjän nimellä `admin`, jolla on täydet hallinnolliset oikeudet.

!!! tip "Vinkki"

    Lisää salasana yksinkertaisesti yksinkertaisiin lainausmerkkeihin. `bash` ja `zsh` käsittelevät merkkejä kuten `!`, `$` ja `*` erikoismerkkeinä, joten lainausmerkit varmistavat, että salasana välittyy oikein.

!!! tip "Parhaat käytännöt"

    Käytä vahvaa salasanaa, jossa on isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä.

---

## Dashboardin määritys {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön web-palvelimella

Digna-dashboardilla on oma erillinen `config.toml` -tiedosto, joka sijaitsee `dashboard/`-hakemistossa. Tämä konfiguraatio toimitetaan valmiina eikä vaadi muutoksia alustavassa asennuksessa. Muokkaa sitä vain, jos tarvitset mukautuksia backend-yhteyteen.

Jos sinun täytyy muokata dashboardin asetuksia (esim. monisoluisten käyttöönottojen vuoksi), katso dashboardin dokumentaatiota.

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

### Ennen päivitystä

**digna-repositorion varmuuskopiointi on pakollista**

Ennen dignan päivittämistä, varmuuskopioi repositoriosi (PostgreSQL) datan menetyksen varalta.
Varmuuskopio mahdollistaa palautuksen, jos päivityksessä ilmenee odottamattomia ongelmia.

Luo varmuuskopio kuoren kautta:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Päivitysprosessi

#### Vaihe 1: Pysäytä digna-palvelu

Jos digna ajetaan systemd-palveluna, pysäytä se ensin:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jos digna ajetaan etualalla, paina `Ctrl + C` sen terminaali-ikkunassa.

#### Vaihe 2: Varmuuskopioi nykyinen backend-asennus

dignan asennushakemistossa:

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Vaihe 3: Pura ja ota uusi versio käyttöön

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritustiedosto ja `dashboard`-kansio asennushakemistoon
3. Palauta suoritusoikeus ja palvelutilin omistus:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Tärkeää"

    `config.toml`-tiedostoa **ei koskaan** sisällytetä asennuspakettiin. Olemassa oleva konfiguraatiosi pysyy ennallaan.

### Vaihe 4: Palauta konfiguraatiotiedostosi

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Vaihe 5: Päivitä repositorion skeema

Siirry dignan asennushakemistoon ja suorita:

```bash
cd /opt/digna
./digna repo upgrade
```

Tämä päivittää PostgreSQL-skeeman uusimpaan versioon säilyttäen kaikki olemassa olevat tiedot.

### Vaihe 6: Käynnistä palvelut uudelleen

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

#### Vaihe 7: Vahvista päivitys

1. Avaa digna-dashboard
2. Varmista, että käyttöliittymä latautuu oikein
3. Tarkista palvelinlokit virheiden varalta:

```bash
sudo journalctl -u digna -n 100
```