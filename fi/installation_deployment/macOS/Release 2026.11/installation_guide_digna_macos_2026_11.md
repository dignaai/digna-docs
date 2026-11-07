# macOS-asennusopas digna Release 2026.11:lle

**Julkaisu:** 2026.11

**Viimeksi päivitetty:** 7. marraskuuta 2026


---

## Sisällysluettelo

1. [Johdanto](#introduction)
2. [Järjestelmävaatimukset](#system-requirements)
3. [Esiasennuksen valmistelut](#pre-installation-setup)
4. [PostgreSQL-palvelimen asennus](#postgresql-server-setup)
5. [Web-palvelimen määritys](#web-server-configuration)
6. [Alkuasennus](#initial-installation)
7. [Backendin määritys](#backend-configuration)
8. [Dashboardin määritys](#dashboard-configuration)
9. [digna:n ajaminen taustapalveluna](#running-digna-as-a-background-service)
10. [Päivitys uuteen julkaisuun](#upgrading-to-a-new-release)

---

## Johdanto {: #introduction }

### Tietoa digna:sta

digna on kattava tekoälypohjainen alusta, joka on suunniteltu optimoimaan datalaadun hallintaa erilaisissa dataympäristöissä, kuten varastoissa, järvissä ja lakehouse-ratkaisuissa. Skalautuvuutensa ja mukautettavuutensa ansiosta digna vastaa nykyaikaisiin datahaasteisiin automaation, reaaliaikaisen seurannan ja poikkeamien tunnistuksen avulla.

digna koostuu kahdesta pääkomponentista:

- **digna**: sovelluksen ydin, joka vastaa tietojen käsittelystä ja laatutarkistusten suorittamisesta. Se yhdistää taustajärjestelmän ja komentorivikäyttöliittymän yhteen suoritettavaan tiedostoon ja korvaa aiempien julkaisujen erilliset ohjelmat `dignabackend` ja `dignacli`.
- **dignadashboard**: Verkkopohjainen käyttöliittymä, joka isännöidään web-palvelimella ja tarjoaa käyttäjäystävällisen tavan käyttää digna-alustaa ja visualisoida datalaatumittareita.

### Mitä uutta Release 2026.11:ssä

Tämä julkaisu tuo mukanaan digna Data Reconciliationin, digna Agenticin ja digna MCP Serverin sekä digna Enginen, joka voi profiloida dataa dignan sisällä ja tarkistaa viite-eheyden eri tietokantateknologioiden välillä. Katso täydet tiedot [release notes](../../../changelog/Release_202611.md).

Asennuksen kannalta julkaisu tuo uuden repositorion migraatiomekanismin, valinnaisen `[duckdb]`-osion `config.toml`-tiedostoon digna Engineä varten sekä uuden lisenssitiedoston. [Päivitysosio](#upgrading-to-a-new-release) käsittelee jokaisen niistä.

### Etsitkö Windowsia tai Linuxia?

Tämä opas kattaa macOS:n. Muille alustoille katso [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) tai [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Järjestelmävaatimukset {: #system-requirements }

Ennen asennuksen aloittamista varmista, että järjestelmäsi täyttää seuraavat vähimmäisvaatimukset:

| Vaatimus | Määrittely |
|---|---|
| **Käyttöjärjestelmä** | macOS 13 (Ventura) tai uudempi |
| **Arkkitehtuuri** | Apple Silicon (arm64) tai Intel (x86_64) |
| **Muisti (minimi)** | 16 GB RAM |
| **Levyn tila** | 10 GB vapaata tallennustilaa |
| **Tietokanta** | PostgreSQL Server 12 tai uudempi |
| **Web-palvelin** | nginx, Apache httpd tai vastaava |
| **Komentorivityökalut** | Xcode Command Line Tools (vaaditaan Homebrew'lle) |

!!! info "digna Engine"

    Tietokantayhteydet, joiden profilointisijaintina on digna Engine, profiloidaan itse
    digna-isännällä. Varaa niille lisää muistia ja levytilaa, katso
    [\[duckdb\]-osio](#duckdb-section).

### Tietokannan asennusvaihtoehdot

**Jos PostgreSQL on jo asennettu:**
Voit lisätä uuden tietokannan digna:lle olemassa olevaan PostgreSQL-palvelimeesi.

**Jos asennat PostgreSQL:n samalle koneelle kuin digna:**

!!! info "Suositellut määritykset"

    - **Muisti**: 32 GB RAM (16 GB sijaan)
    - **Levyn tila**: 50 GB vapaata tallennustilaa (10 GB sijaan)

    Nämä suuremmat resurssivaatimukset huomioivat sekä digna:n että PostgreSQL-tietokannan ajamisen samanaikaisesti.

### Arkkitehtuurin tarkistus

Monet tämän oppaan polut eroavat Apple Silicon- ja Intel-masien välillä. Tarkista laitteesi arkkitehtuuri avaamalla **Terminal** ja suorittamalla:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew asentuu polkuun `/opt/homebrew`.
- `x86_64` — Intel. Homebrew asentuu polkuun `/usr/local`.

!!! tip "Vinkki"

    Kiinteän polun sijaan tämä opas käyttää `$(brew --prefix)`, joka laajenee oikeaan sijaintiin kummallakin arkkitehtuurilla. Voit kopioida komennot muuttumattomina.

---

## Esiasennuksen valmistelut {: #pre-installation-setup }

Ennen digna:n asentamista varmista, että kolme keskeistä edellytystä on paikallaan:

1. **Homebrew** – pakettienhallinta, jolla asennetaan alla olevat komponentit
2. **PostgreSQL Server** – laskettujen mittareiden ja suorituskykytiedon tallennukseen
3. **Web-palvelin** – digna Dashboardin isännöintiin

Jos näitä komponentteja ei ole vielä asennettu, seuraa alla olevia osioita asentaaksesi ja konfiguroidaksesi ne.

### Homebrew'n asennus

Homebrew on macOS:n yleinen pakettienhallinta ja sitä käytetään tässä oppaassa PostgreSQL:n ja nginx:n asentamiseen.

#### Vaihe 1: Tarkista, onko Homebrew jo asennettu

Avaa **Terminal** (paina `Cmd + Space`, kirjoita `Terminal`, paina Enter) ja suorita:

```bash
brew --version
```

Jos komentoon palautuu versiopäivämäärä, siirry kohtaan [PostgreSQL-palvelimen asennus](#postgresql-server-setup).

#### Vaihe 2: Asenna Homebrew

Jos komentoa ei löydy, asenna Homebrew seuraamalla ohjeita [virallisella Homebrew-sivustolla](https://brew.sh). Asentaja asentaa myös Xcode Command Line Tools -paketin, jos sitä ei ole jo asennettu.

#### Vaihe 3: Lisää Homebrew PATHiin

Apple Siliconilla asennusohjelma tulostaa kaksi komentoa Homebrew'n lisäämiseksi shell-ympäristöön. Suorita ne ohjeiden mukaisesti ja vahvista:

```bash
brew --prefix
```

Tämän pitäisi tulostaa `/opt/homebrew` Apple Siliconilla tai `/usr/local` Intelillä.

---

## PostgreSQL-palvelimen asennus {: #postgresql-server-setup }

### Jos sinulla on jo PostgreSQL

Jos PostgreSQL on jo asennettu ja käynnissä paikallisella koneellasi tai käytät hallinnoitua etä-PG-palvelinta, voit siirtyä seuraavaan osioon: [Web-palvelimen määritys](#web-server-configuration).

### Asennusvaihtoehdot

macOS tarjoaa kaksi suoraviivaista tapaa asentaa PostgreSQL. Valitse **yksi**:

- [Homebrew](#postgresql-homebrew) — komentorivityökalu, suositeltu palvelinympäristöihin
- [Postgres.app](#postgresql-app) — graafinen asennus, kätevä paikalliseen arviointiin

### PostgreSQL:n asennus Homebrew'lla {: #postgresql-homebrew }

#### Vaihe 1: Asenna PostgreSQL-formula

```bash
brew install postgresql@16
```

#### Vaihe 2: Lisää PostgreSQL PATHiin

Versioidut PostgreSQL-formulat ovat *keg-only*, joten Homebrew ei linkitä niiden komentoja PATHiin automaattisesti. Lisää ne itse:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Huomio"

    Tämä olettaa macOS:n oletusshellin `zsh`:n. Jos käytät `bash`-shelliä, lisää sama rivi tiedostoon `~/.bash_profile`.

#### Vaihe 3: Käynnistä PostgreSQL-palvelu

```bash
brew services start postgresql@16
```

Tämä käynnistää PostgreSQL:n välittömästi ja asettaa sen käynnistymään automaattisesti kirjautuessasi sisään.

#### Vaihe 4: Vahvista asennus

```bash
psql --version
```

Näet PostgreSQL-version, jos asennus onnistui.

#### Vaihe 5: Yhdistä palvelimeen

```bash
psql postgres
```

!!! warning "Tärkeää — macOS eroaa Windowsista tässä"

    Windowsin asennusohjelma ohjaa luomaan `postgres`-superkäyttäjän ja salasanan. Homebrew ei tee näin. Sen sijaan se luo superkäyttäjän, jonka nimi vastaa sinun **macOS-käyttäjätiliäsi**, ilman salasanaa, ja se on saavutettavissa vain paikalliselta koneelta.

    Tämä tarkoittaa, että puhtaassa Homebrew-asennuksessa ei ole `postgres`-roolia. Käytä omaa käyttäjänimeäsi, kun tarvitset superkäyttäjää, ja luo erillinen digna-käyttäjä kuten kuvattu [Alkuasennus](#initial-installation) -kohdassa.

#### Vaihe 6: Vahvista portti

Oletusportti PostgreSQL:lle on `5432`. Varmista palvelimen kuuntelema portti:

```bash
psql postgres -c "SHOW port;"
```

Muista tämän arvo myöhempiä digna-backendin asetuksia varten.

### PostgreSQL:n asennus Postgres.app:illa {: #postgresql-app }

Jos haluat graafisen asennuksen:

1. Lataa [Postgres.app](https://postgresapp.com) ja raahaa se **Applications**-kansioon
2. Avaa sovellus ja klikkaa **Initialize** luodaksesi uuden palvelimen
3. Seuraa sovelluksen ohjeita lisätäksesi komentorivityökalut PATHiin
4. Vahvista asennus:

```bash
psql --version
```

Postgres.app luo myös superkäyttäjän, jonka nimi vastaa macOS-käyttäjätiliäsi.

---

## Web-palvelimen määritys {: #web-server-configuration }

digna tarvitsee web-palvelimen dashboardin isännöintiin. Valitse yksi seuraavista vaihtoehdoista:

- [nginx](#nginx-setup) — asennetaan Homebrew'lla, suositeltu
- [Apache httpd](#apache-setup) — sisältyy macOS:ään

Tarvitset vain yhden näistä palvelimista ja konfiguroit sen seuraavien riippuvuuksien mukaisesti:

- **Single-page-application fallback**, jotta dashboard-URL:n uudelleenlataus ei aiheuta 404-virhettä
- **`.md`-MIME-tyyppi**, jotta Markdown-tiedostot toimitetaan oikealla tyypillä

### nginx-määritys {: #nginx-setup }

#### Yleiskatsaus

nginx on kevyt, korkean suorituskyvyn web-palvelin, joka sopii hyvin staattisen digna-dashboardin tarjoamiseen.

#### Asennus

```bash
brew install nginx
```

#### nginx:n käynnistäminen

```bash
brew services start nginx
```

#### Vahvista asennus

1. Avaa selaimesi
2. Siirry osoitteeseen `http://localhost:8080`
3. Näet nginxin tervetulosivun

!!! note "Huomio — oletusportti on 8080, ei 80"

    Homebrew konfiguroi nginxin kuuntelemaan porttia `8080`, jotta se voi toimia ilman administraattorioikeuksia. macOS:ssä porttiin `80` tai muihin alle 1024 kuuluvien porttien sitominen vaatii root-oikeudet.

    Jos haluat tarjota dashboardin portissa 80, vaihda `listen 8080;` -> `listen 80;` alla olevassa konfiguraatiossa ja käynnistä nginx komennolla `sudo brew services start nginx`.

#### Sivuston konfigurointi dashboardille

Homebrew'n nginx-konfiguraatio lataa kaikki tiedostot `servers`-hakemistostaan. Luo oma konfiguraatiotiedosto digna:lle sinne:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Liitä seuraava, korvaten `/path/to/digna/dashboard` todellisella polulla purettuun `dashboard`-kansioon:

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

!!! warning "Tärkeää"

    Ilman `try_files`-direktiiviä, dashboardin muu kuin juuripolun uudelleenlataus palauttaa 404-virheen. Tämä on nginxin vastine IIS:n URL Rewrite -moduulille Windowsissa.

#### Ota konfiguraatio käyttöön

Testaa syntaksivirheet ja lataa nginx uudelleen:

```bash
nginx -t
brew services restart nginx
```

---

### Apache httpd -määritys {: #apache-setup }

#### Yleiskatsaus

macOS sisältää Apache httpd:n, joten asennusta ei tarvita. Se on oletuksena pois päältä.

#### Apachen käynnistäminen

```bash
sudo apachectl start
```

#### Vahvista asennus

1. Avaa selain
2. Siirry osoitteeseen `http://localhost`
3. Näet viestin "It works!"

#### Pakollinen: mod_rewritein ottaminen käyttöön

Dashboard vaatii URL-uudelleenkirjoituksen. Avaa Apache-konfiguraatio:

```bash
sudo nano /etc/apache2/httpd.conf
```

Etsi seuraava rivi ja poista edestä `#` niin että se on kommentoimaton:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Pakollinen: salli .htaccess-ylikirjoitukset

Saman tiedoston sisällä etsi `<Directory "/Library/WebServer/Documents">` -lohko ja vaihda:

```apache
AllowOverride None
```

muotoon:

```apache
AllowOverride All
```

#### Pakollinen: MIME-tyyppi Markdown-tiedostoille

Lisää `httpd.conf`-tiedostoon seuraava rivi, jotta Markdown-tiedostot toimitetaan oikein:

```apache
AddType text/markdown .md
```

!!! warning "Tärkeää"

    Ilman tätä asetusta `.md`-tiedostot eivät välttämättä toimitu oikein.

#### Ota konfiguraatio käyttöön

Tarkista syntaksivirheet ja käynnistä Apache uudelleen:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Alkuasennus {: #initial-installation }

### Vaihe 1: Luo digna-repositorio ja käyttäjä

digna-repositorio tallentaa kaikki digna:n laskemat mittarit. Se toimii keskitettynä tietokantana analytiikka- ja suorituskykytiedolle.

#### Luo skeema ja käyttäjä

Avaa PostgreSQL-asiakasohjelma (psql, pgAdmin tai muu) ja suorita seuraavat SQL-komennot:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Korvaa seuraavat paikkamerkit:**

- `<digna_repo_schema>` — haluamasi skeeman nimi (esim. `dignarepo`)
- `<digna_repo_user>` — haluamasi käyttäjänimi (esim. `digna_user`)
- `<digna_repo_password>` — turvallinen salasana tälle käyttäjälle

**Esimerkki:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Suorittaaksesi nämä Terminalissa yhdessä vaiheessa:

```bash
psql postgres
```

Liitä sitten lauseet `postgres=#` -kehotteessa ja poistu kirjoittamalla `\q`.

!!! tip "Parhaat käytännöt"

    Käytä vahvoja, monimutkaisia salasanoja tietokantakäyttäjille. Vältä helposti arvattavia tunnuksia.

---

### Vaihe 2: Pura digna-asennuspaketti

1. Etsi sinulle toimitettu digna-asennus ZIP-tiedosto
2. Pura se haluamaasi asennushakemistoon — esimerkiksi `/opt/digna` tai `~/digna`
3. Purkamisen jälkeen sinun pitäisi nähdä seuraavat kohteet:
   - `dashboard/` — Web-dashboardin käyttöliittymä
   - `digna` — Pääsuoritettava tiedosto (backend + CLI yhdessä)

!!! info "Konfiguraatio- ja lisenssitiedostot eivät sisälly pakettiin"

    Asennuksen mukana ei toimiteta `config.toml`- eikä `dashboard/dashboard_config.toml`-tiedostoa — luot
    molemmat itse kohdissa [Backendin määritys](#backend-configuration) ja
    [Dashboardin määritys](#dashboard-configuration). Myöskään `license.toml` ei sisälly pakettiin;
    digna toimittaa sen erikseen, kuten vaiheessa 3 kuvataan.

Pura Terminalista:

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Tee suoritettavasta tiedostosta ajettava

Riippuen siitä, miten arkisto on siirretty, suoritusoikeus ei välttämättä säily purkamisen yhteydessä. Aseta se manuaalisesti:

```bash
cd /opt/digna
chmod +x digna
```

#### Jos macOS estää sovelluksen käynnistämisen

Selain- tai sähköpostilataukset merkitään usein karanteeniattribuutilla. Jos macOS ilmoittaa, että sovellusta *"ei voi avata, koska kehittäjää ei voida varmentaa"*, poista attribuutti asennushakemistosta:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Vaihtoehtoisesti avaa **System Settings → Privacy & Security**, etsi estetty kohde sivun alaosasta ja valitse **Open Anyway**.

!!! note "Huomio"

    Tämä vaihe on tarpeen vain, jos macOS todella estää suoritettavan tiedoston. SSH:lla tai sisäisiltä tiedostojakoilta siirretyt paketit eivät yleensä joudu karanteeniin.

### Vaihe 3: Asenna lisenssitiedosto

!!! warning "Tärkeää"

    Lisenssitiedostoa ei sisälly asennuspakettiin ja se toimitetaan erikseen digna:lta.

1. Etsi sinulle toimitettu `license.toml`-tiedosto
2. Kopioi se digna-asennuksen juurihakemistoon (samaan hakemistoon jossa `config.toml` ja `digna`-suoritettava ovat)

**Miksi tämä on tärkeää:**
Lisenssitiedosto sisältää asiakastiedot, lisenssin vanhenemispäivän ja digitaaliset allekirjoitukset. **Älä muokkaa tätä tiedostoa** — kaikki muutokset mitätöivät sen.

**Hakemistorakenne asennuksen jälkeen:**

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

## Backendin määritys {: #backend-configuration }

### Vaihe 1: Luo ja muokkaa konfiguraatiotiedostoa

`config_template.toml` -tiedosto toimitetaan digna-asennushakemistossasi. Sinun tarvitsee vain nimetä se `config.toml` -tiedostoksi.

```bash
cd /opt/digna
mv config_template.toml config.toml
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

!!! note "Huomio"

    Jos tarjoat dashboardin Homebrew'n nginx:llä sen oletusportissa, sallitun originin arvo on `http://localhost:8080`.

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
| `DIGNA_REPO_PASSWORD` | Salasanasi | Skeeman luonnin yhteydessä asetettu salasana |
| `DIGNA_REPO_SSLMODE` | `prefer` (oletus) | Valinnainen. PostgreSQL:n SSL-tila: `disable`, `allow`, `prefer`, `require`, `verify-ca` tai `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (oletus) | Valinnainen. Yhteyksien määrä, jonka digna pitää avoinna repositorioon |

#### [base] -osio

Tämä osio sisältää turva-, eväste- ja tarkastusasetuksia:

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
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon voimassaoloaika sekunteina |
| `DIGNA_MAX_WORKERS` | CPU-ytimien määrä - 1 | Samanaikaisesti ajettavien tarkastusten enimmäismäärä |
| `DIGNA_FRONTEND_BASEURL` | Dashboardin URL | Pakollinen. Käytetään ilmoitusviestien linkeissä, joten sen on oltava URL, jonka vastaanottajat voivat avata |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (oletus) | Valinnainen. Sekunnit, joiden ajan yksittäinen lähdetietokantaan kohdistuva kysely saa olla käynnissä ennen keskeytystä; `0` poistaa aikakatkaisun käytöstä |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (oletus) | Valinnainen. Sekunnit, joiden ajan lähdetietokantayhteyttä odotetaan; `0` odottaa rajattomasti |

!!! tip "Vinkki"

    Selvittääksesi käytettävissä olevien CPU-ytimien määrän Macillasi, suorita `sysctl -n hw.ncpu`.

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
| `DIGNA_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotantoon, `DEBUG` vianetsintään. Myös `TRACE`, `WARN` ja `ERROR` hyväksytään |
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
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Oletus: järjestelmän väliaikaishakemisto (dignaa ajavan tilin `$TMPDIR`) | Väliaikaistiedostojen hakemisto, kun data ei mahdu muistiin |

!!! tip "digna Enginen mitoitus"

    Varaa digna-isännälle enintään `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` muistia
    dignan oman muistinkäytön lisäksi, ja väliaikaishakemistoon riittävästi vapaata levytilaa
    suurimmalle tarkastetulle päivämäärälle niistä tietolähteistä, jotka käyttävät digna Engineä.
    Osoita `DIGNA_DUCKDB_TEMP_DIRECTORY` levylle, jolla on tämä tila ja johon dignaa ajava tili
    voi kirjoittaa:

    ```bash
    mkdir -p /opt/digna/tmp
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

### Vaihe 3: Alusta repositorio

1. Avaa **Terminal**
2. Siirry digna-asennushakemistoon (jossa `config.toml` ja `digna`-suoritettava sijaitsevat)
3. Testaa yhteys:

```bash
cd /opt/digna
./digna repo check
```

Uudessa skeemassa komento muodostaa yhteyden ja ilmoittaa sitten, ettei repositoriota ole vielä asennettu:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Tässä vaiheessa tämä on odotettu tulos: se vahvistaa, että digna tavoittaa PostgreSQL:n ja skeeman. Yhteys- tai todennusvirhe sen sijaan viittaa `[repo]`-osioon tai PostgreSQL-asetuksiin.

!!! note "Huomio"

    macOS:ssä nykyisen hakemiston komentoja ei ole PATHissa, joten suoritettava kutsutaan muodossa `./digna` eikä `digna`. Käyttääksesi lyhyempää muotoa kaikkialla, lisää asennushakemisto PATHiin:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Vaihe 4: Asenna repositorion skeema

Samassa hakemistossa suorita:

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

1. Avaa **uusi** Terminal-ikkuna
2. Siirry digna-asennushakemistoon
3. Luo ylläpitäjäkäyttäjä seuraavalla komennolla:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Esimerkki:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Tämä luo käyttäjän sähköpostiosoitteella `admin@example.com` ja täysillä järjestelmänvalvojan oikeuksilla.

!!! tip "Vinkki"

    Kääri salasana yksinkertaisiin lainausmerkkeihin. `zsh` käsittelee merkkejä kuten `!`, `$` ja `*` erikoismerkeinä, ja ilman lainausmerkkejä sisältävä salasana ei välity oikein.

!!! tip "Parhaat käytännöt"

    Käytä vahvaa salasanaa, jossa on isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä.

---

### Vaihe 6: Käynnistä digna-palvelin

Digna-asennushakemistossa käynnistä palvelin:

```bash
./digna serve --address <host> --port <port>
```

**Parametrit:**
- `--address` — Palvelimen isäntä/IP (oletus `127.0.0.1`)
- `--port` — Palvelimen portti (oletus `8000`)

Kun palvelin on käynnissä, se tulostaa osoitteen, jota se kuuntelee:

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Vinkki"

    Ensimmäisellä käynnistyskerralla macOS voi kysyä, haluatko sallia sovelluksen vastaanottaa verkoyhteyksiä. Valitse **Allow**, muuten dashboard ei pääse käsiksi backend:iin.

!!! note "Palvelin varaa päätteen"

    `serve` toimii edustalla ja jatkaa, kunnes pysäytät sen näppäinyhdistelmällä ++ctrl+c++. Anna sen olla käynnissä, kun viimeistelet asennuksen; automaattisen käynnistyksen osalta katso [dignan suorittaminen taustapalveluna](#running-digna-as-a-background-service).

## Dashboardin määritys {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön web-palvelimella

digna-dashboard lukee oman konfiguraationsa tiedostosta `dashboard/dashboard_config.toml`. Tätä tiedostoa ei toimiteta asennuksen mukana — luot sen `dashboard/`-hakemistoon dashboardin tiedostojen rinnalle.

Sen sisältö on kuvattu kohdassa [Yhden kirjautumisen (SSO) yleiskatsaus](../../../sso/overview.md), jossa tiedostoa myös tarvitaan: se sisältää dashboardin tarjoamat kirjautumisvaihtoehdot ja monen instanssin käyttöönotoissa backend-yhteyden.

Valitse web-palvelimesi ja seuraa vastaavia käyttöönotto-ohjeita.

#### Käyttöönotto nginx:llä

Jos noudatit [nginx-määritystä](#nginx-setup), server-lohko osoittaa jo dashboard-kansioosi eikä tiedoston kopiointia tarvita.

1. **Vahvista polku**
   - Avaa `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Varmista, että `root` osoittaa purettuun `dashboard`-kansioon

2. **Varmista, että kansio on luettavissa**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Lataa nginx uudelleen**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Testaa asennus**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost:8080` (tai konfiguroituun URL-osoitteeseen)
   - Näet digna-dashboardin kirjautumissivun

#### Käyttöönotto Apache httpd:llä

1. **Kopioi dashboard dokumenttihakemistoon**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Lisää uudelleenkirjoitussäännöt**

   Luo `.htaccess`-tiedosto asennetun kansion sisälle, jotta dashboard-reitit säilyvät selainuudelleenlatauksissa:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Liitä seuraava:

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
   sudo apachectl restart
   ```

4. **Avaa dashboard**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost/digna`
   - Näet digna-dashboardin kirjautumissivun

---

## digna:n ajaminen taustapalveluna {: #running-digna-as-a-background-service }

### Miksi ajaa digna palveluna?

digna-backendin ajaminen taustapalveluna varmistaa, että se:

- Käynnistyy automaattisesti koneen käynnistyessä
- Ajaa taustalla ilman auki olevaa Terminal-ikkunaa
- Käynnistyy uudelleen automaattisesti virheen sattuessa
- On hallittavissa `launchctl`-työkalulla, joka on macOS:n palvelunhallinta

### Palvelunhallintatiedostot

Kaikki tarvittavat tiedostot sijaitsevat digna-asennushakemistossa polussa: `bin/`

Seuraavat shell-skriptit ovat käytettävissä:

- `install_service.sh` — rekisteröi digna:n launchd:iin
- `uninstall_service.sh` — poistaa rekisteröinnin
- `start_service.sh` — käynnistää rekisteröidyn palvelun
- `stop_service.sh` — pysäyttää käynnissä olevan palvelun

!!! warning "Ylläpitäjän oikeudet vaaditaan"

    Kaikki skriptit on suoritettava `sudo`-oikeuksin, sillä käynnistyksen yhteydessä rekisteröitävät palvelut kirjoittavat `/Library/LaunchDaemons`-hakemistoon.

### Tee skripteistä suoritettavia

Purkaminen ei välttämättä säilytä suoritusoikeuksia. Ennen ensimmäistä käyttökertaa:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Palvelun asennus

1. **Avaa Terminal**

2. **Siirry bin-hakemistoon**
   ```bash
   cd /opt/digna/bin
   ```

3. **Suorita asennusskripti**
   ```bash
   sudo ./install_service.sh
   ```

Digna-palvelu on nyt rekisteröity launchd:iin automaattisen käynnistyksen kanssa. Palvelu ei välttämättä käynnisty heti — katso seuraava osio sen käynnistämiseksi.

### Palvelun käynnistäminen ja pysäyttäminen

#### Palvelun käynnistäminen

1. Avaa Terminal
2. Siirry `/opt/digna/bin`
3. Suorita:
   ```bash
   sudo ./start_service.sh
   ```

#### Palvelun pysäyttäminen

1. Avaa Terminal
2. Siirry `/opt/digna/bin`
3. Suorita:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Vinkki"

    Pysäytä aina palvelu ennen sovellustiedostojen päivittämistä.

### Palvelun tarkistus

Varmista, että palvelu on rekisteröity ja käynnissä:

```bash
sudo launchctl list | grep digna
```

Rivi, joka alkaa prosessi-ID:llä, tarkoittaa että palvelu on käynnissä. `-` ensimmäisessä sarakkeessa tarkoittaa, että se on rekisteröity mutta pysäytetty.

### Palvelun siirtäminen uuteen hakemistoon

launchd tallentaa suoritettavan tiedoston absoluuttisen polun, joten asennuksen siirto vaatii palvelun uudelleenrekisteröinnin:

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

Digna-palvelu on nyt poistettu launchd:stä.

---

## Päivittäminen uuteen julkaisuun {: #upgrading-to-a-new-release }

Tämä osio päivittää Release 2026.06 -asennuksen versioon Release 2026.11. Jos asennuksesi on
vanhempi, lue ensin [Päivitys julkaisua 2026.06 vanhemmasta versiosta](#upgrading-from-a-release-before-2026-06).

### Ennen päivitystä

**digna-repositorion varmuuskopiointi on pakollinen**

Ennen digna:n päivittämistä, varmuuskopioi repositoriosi (PostgreSQL) estääksesi datan menetyksen.
Varmuuskopio varmistaa palautusmahdollisuuden, jos päivityksessä ilmenee odottamattomia ongelmia.

Luo varmuuskopio Terminalissa:

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

Jos digna on käynnissä taustapalveluna, pysäytä se ensin:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jos digna on ajossa etualalla, keskeytä se painamalla ++ctrl+c++ sen Terminal-ikkunassa.

#### Vaihe 2: Varmuuskopioi nykyinen asennus {: #step-2-backup-current-installation }

Nimeä digna-asennushakemistossa nykyisen asennuksen suoritettava tiedosto ja dashboard-kansio uudelleen,
jotta uusi julkaisu voidaan ottaa käyttöön niiden rinnalle:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Säilytä `digna_old`, kunnes olet varmistanut päivityksen, ja `dashboard_old`, kunnes olet palauttanut
siitä konfiguraatiotiedostosi (katso vaihe 4). Sen jälkeen voit poistaa molemmat.

!!! info "Päivitys julkaisua 2026.06 vanhemmasta versiosta"

    Nimeä suoritettavan tiedoston sijaan uudelleen kansiot `dignabackend` ja `dignacli`:
    `mv dignabackend dignabackend_old` ja `mv dignacli dignacli_old`. Release 2026.11 ei käytä kumpaakaan.

#### Vaihe 3: Pura ja ota uusi versio käyttöön {: #step-3-extract-and-deploy-new-version }

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritettava ja `dashboard`-kansio asennushakemistoosi
3. Palauta suoritusoikeus ja tarvittaessa poista karanteeniattribuutti:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Tärkeää"

    Asennuksen ZIP-tiedostoon ei koskaan sisällytetä `config.toml`- eikä `dashboard/dashboard_config.toml`-tiedostoa
    — digna-tiimi ei koskaan toimita kumpaakaan tiedostoa. Päivitys ei siksi koske olemassa olevaan
    konfiguraatioosi, ja uudelleennimetyissä `*_old`-kansioissa olevat kopiot ovat ainoat, jotka sinulla on.

#### Vaihe 4: Palauta konfiguraatiotiedostosi {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
ja lataa sitten sivu uudelleen pakotetulla päivityksellä (++cmd+shift+r++).

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
cp /path/to/new/license.toml /opt/digna/license.toml
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

Jos ajetaan taustapalveluna:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Jos ajetaan manuaalisesti, käynnistä palvelin uudelleen:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Jos käytät nginx:iä tai Apachea, käynnistä vastaava web-palvelin uudelleen:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Vaihe 10: Vahvista päivitys {: #step-10-verify-the-upgrade }

1. Vahvista uuden suoritettavan tiedoston julkaisu:

    ```bash
    ./digna version
    ```

    Ensimmäisen rivin on oltava `Release: 2026.11`.

2. Avaa digna-dashboard ja varmista, että käyttöliittymä latautuu oikein.
3. Tarkista palvelimen tuloste ja `logs`-hakemiston tiedostot virheiden varalta.
4. Testaa tietokantayhteytesi — katso
   [Yhteyden testaaminen](../../../databases/overview.md#testing-a-connection). Jos päivitit
   julkaisua 2026.06 vanhemmasta versiosta, muuta ensin jokainen yhteys, joka ei vielä käyttänyt ODBC:tä,
   ODBC:ksi.

Uusien moduulien käytön aloittamiseen katso [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI-agentin yhdistäminen](../../../platform/agentic/connect_ai_agent.md) digna MCP Serveriä varten ja
[Profilointisijainti](../../../platform/profiling/profiling_location.md) digna Engineä varten.