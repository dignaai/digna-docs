---
title: macOS-asennusopas – digna Release 2026.06 | digna-dokumentaatio
description: Askel-askeleelta -opas digna Release 2026.06:n asentamiseen macOS:ssä — järjestelmävaatimukset, Homebrew- ja PostgreSQL-asennus, nginx- tai Apache-määritys, backend- ja dashboard-asetukset, digna:n ajaminen taustapalveluna ja päivittäminen uuteen julkaisuun.
keywords: digna macos asentaminen, digna macasennusopas, digna backend asennus, digna dashboard asennus, postgresql homebrew, nginx macos, digna launchd palvelu, digna päivitysopas
image: /assets/logo_square.png
---

# macOS-asennusopas digna Release 2026.06:lle

**Julkaisu:** 2026.06

**Viimeksi päivitetty:** 5. syyskuuta 2026


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

- **dignabackend**: Sovelluksen ydinmoottori, joka vastaa datan käsittelystä ja laadun tarkastuksista.
- **dignadashboard**: Verkkopohjainen käyttöliittymä, joka isännöidään web-palvelimella ja tarjoaa käyttäjäystävällisen tavan käyttää digna-alustaa ja visualisoida datalaatumittareita.

### Mitä uutta Release 2026.06:ssa

Tässä julkaisussa datan observabiliteetti tuodaan suoraan koodiin, jolloin kehittäjät voivat seurata datalaatua jo lähteellä. Katso täydelliset tiedot [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Etsitkö Windowsia tai Linuxia?

Tämä opas kattaa macOS:n. Muille alustoille katso [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) tai [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Konfiguraatiotiedosto
   - `license.toml` — Lisenssitiedosto (kopioi omasi tänne)

Pura Terminalista:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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

Tämä osio määrittää digna-backendin sovellusasetukset:

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
| `digna_APP_PORT` | `8082` (oletus) | REST API -pisteiden portti |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendin URL | Jos dashboard on eri palvelimella, lisää sen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vaaditaan CORS-kutsuille, joissa käytetään tunnuksia |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Salli kaikki HTTP-metodit |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Salli kaikki otsikot |

!!! note "Huomio"

    Jos tarjoat dashboardin Homebrew'n nginx:llä sen oletusportissa, sallitun originin arvo on `http://localhost:8080`.

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
| `digna_REPO_PASSWORD` | Salasanasi | Skeeman luonnin yhteydessä asetettu salasana |

#### [base] -osio

Tämä osio sisältää turva- ja evästeasetuksia:

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
| `digna_FERNET_KEY` | Salausavain | Käytetään tokenien ja evästeiden salaamiseen (oletusarvo annettu) |
| `digna_COOKIE_DOMAIN` | `localhost` | Vastaa frontend-domainia |
| `digna_COOKIE_SECURE` | `false` (paikallinen) / `true` (production) | Käytä `true` HTTPS-yhteyksissä |
| `digna_COOKIE_HTTPONLY` | `true` | Aina päällä turvallisuussyistä |
| `digna_COOKIE_SAME_SITE` | `lax` | Estää CSRF-hyökkäyksiä |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon voimassaoloaika sekunteina |
| `digna_MAX_WORKERS` | CPU-ytimien määrä - 1 | Rinnakkaisten tarkastustehtävien määrä |

!!! tip "Vinkki"

    Selvittääksesi käytettävissä olevien CPU-ytimien määrän Macillasi, suorita `sysctl -n hw.ncpu`.

#### [logging] -osio

Tämä osio määrittää lokituksen käyttäytymisen:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametri | Arvo | Huomio |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotantoon, `DEBUG` vianetsintään |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Säilytettävien päivittäisten lokavarmenteiden määrä |

---

### Vaihe 2: Alusta repositorio

1. Avaa **Terminal**
2. Siirry digna-asennushakemistoon (jossa `config.toml` ja `digna`-suoritettava sijaitsevat)
3. Testaa yhteys:

```bash
cd /opt/digna
./digna repo check
```

Saat vahvistuksen, että yhteys on muodostettu (repo ei vielä ole alustettu).

!!! note "Huomio"

    macOS:ssä nykyisen hakemiston komentoja ei ole PATHissa, joten suoritettava kutsutaan muodossa `./digna` eikä `digna`. Käyttääksesi lyhyempää muotoa kaikkialla, lisää asennushakemisto PATHiin:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Vaihe 3: Asenna repositorion skeema

Samaalla hakemistossa suorita:

```bash
./digna repo install
```

Tämä komento asentaa tarvittavat taulut ja skeeman PostgreSQL-tietokantaasi.

### Vaihe 4: Käynnistä digna-palvelin

Digna-asennushakemistossa käynnistä palvelin:

```bash
./digna serve --address <host> --port <port>
```

**Parametrit:**
- `--address` — Palvelimen isäntä/IP
- `--port` — Palvelimen portti

Näet käynnistysviestejä, jotka vahvistavat palvelimen käynnistyneen:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! tip "Vinkki"

    Ensimmäisellä käynnistyskerralla macOS voi kysyä, haluatko sallia sovelluksen vastaanottaa verkoyhteyksiä. Valitse **Allow**, muuten dashboard ei pääse käsiksi backend:iin.

### Vaihe 5: Luo ylläpitäjäkäyttäjä

1. Avaa **uusi** Terminal-ikkuna
2. Siirry digna-asennushakemistoon
3. Luo ylläpitäjäkäyttäjä seuraavalla komennolla:

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Esimerkki:**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Tämä luo käyttäjän nimellä `admin` ja täyden ylläpitäjäoikeuden.

!!! tip "Vinkki"

    Kääri salasana yksinkertaisiin lainausmerkkeihin. `zsh` käsittelee merkkejä kuten `!`, `$` ja `*` erikoismerkeinä, ja ilman lainausmerkkejä sisältävä salasana ei välity oikein.

!!! tip "Parhaat käytännöt"

    Käytä vahvaa salasanaa, jossa on isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä.

---

## Dashboardin määritys {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön web-palvelimella

Digna-dashboardilla on oma `config.toml` -tiedostonsa `dashboard/`-kansiossa. Tämä konfiguraatio toimitetaan valmiina eikä vaadi muutoksia alkuasennuksessa. Tarvitset sen muokkausta vain, jos haluat mukauttaa backend-yhteyttä tai tehdä monisointiasetuksia.

Jos sinun täytyy muokata dashboardin asetuksia, tutustu dashboardin dokumentaatioon.

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

### Ennen päivitystä

**digna-repositorion varmuuskopiointi on pakollinen**

Ennen digna:n päivittämistä, varmuuskopioi repositoriosi (PostgreSQL) estääksesi datan menetyksen.
Varmuuskopio varmistaa palautusmahdollisuuden, jos päivityksessä ilmenee odottamattomia ongelmia.

Luo varmuuskopio Terminalissa:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Päivitysprosessi

#### Vaihe 1: Pysäytä digna-palvelu

Jos digna on käynnissä taustapalveluna, pysäytä se ensin:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jos digna on ajossa etualalla, keskeytä se painamalla `Ctrl + C` sen Terminal-ikkunassa.

#### Vaihe 2: Varmuuskopioi nykyinen backend-asennus

Digna-asennushakemistossasi:

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Vaihe 3: Pura ja ota uusi versio käyttöön

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritettava ja `dashboard`-kansio asennushakemistoosi
3. Palauta suoritusoikeus ja tarvittaessa poista karanteeniattribuutti:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Tärkeää"

    `config.toml`-tiedostoa **ei koskaan** sisällytetä asennuspakettiin. Nykyinen konfiguraatiosi säilyy ennallaan.

### Vaihe 4: Palauta konfiguraatiotiedostosi

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Vaihe 5: Päivitä repositorion skeema

Siirry digna-asennushakemistoon ja suorita:

```bash
cd /opt/digna
./digna repo upgrade
```

Tämä päivittää PostgreSQL-skeeman uusimpaan versioon säilyttäen kaiken olemassa olevan datan.

### Vaihe 6: Käynnistä palvelut uudelleen

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

#### Vaihe 7: Vahvista päivitys

1. Avaa digna-dashboard
2. Varmista, että käyttöliittymä latautuu oikein
3. Tarkista palvelinlokit mahdollisten virheiden varalta