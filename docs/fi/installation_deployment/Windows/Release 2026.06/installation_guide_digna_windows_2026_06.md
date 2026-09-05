---
title: Windowsin asennusopas – digna Julkaisu 2026.06 | digna-dokumentaatio
description: Askel askeleelta -opas digna Julkaisu 2026.06:n asentamiseen Windowsissa — järjestelmävaatimukset, PostgreSQL-asennus, web-palvelimen konfigurointi, backend- ja dashboard-asetukset, dignan ajaminen Windows-palveluna sekä päivitys uuteen julkaisuun.
keywords: digna windows asennus, digna käyttöönotto-opas, digna backend asennus, digna dashboard asennus, postgresql asennus, digna windows -palvelu, digna päivitysohje
image: /assets/logo_square.png
---

# Windowsin asennusopas digna Julkaisu 2026.06:lle

**Julkaisu:** 2026.06

**Viimeksi päivitetty:** 30. elokuuta 2026


---

## Sisällysluettelo

1. [Johdanto](#introduction)
2. [Järjestelmävaatimukset](#system-requirements)
3. [Ennen asennusta](#pre-installation-setup)
4. [PostgreSQL-palvelimen asennus](#postgresql-server-setup)
5. [Web-palvelimen konfigurointi](#web-server-configuration)
6. [Ensiasennus](#initial-installation)
7. [Backendin konfigurointi](#backend-configuration)
8. [Dashboardin konfigurointi](#dashboard-configuration)
9. [digna:n ajaminen Windows-palveluna](#running-digna-as-a-windows-service)
10. [Päivitys uuteen julkaisuun](#upgrading-to-a-new-release)

---

## Johdanto {: #introduction }

### Tietoa dignasta

digna on kattava tekoälypohjainen alusta, joka on suunniteltu optimoimaan datalaadun hallintaa eri data-ympäristöissä, kuten tietovarastoissa, data lakeissä ja lakehouse-ratkaisuissa. Rakennettu skaalautuvaksi ja mukautuvaksi, digna vastaa moderneihin datahaasteisiin automaation, reaaliaikaisen seurannan ja poikkeamien tunnistuksen avulla.

digna koostuu kahdesta pääkomponentista:

- **dignabackend**: Sovelluksen ydinohjain, joka vastaa datan käsittelystä ja laadun tarkastuksista.
- **dignadashboard**: Web-pohjainen käyttöliittymä, joka ajetaan web-palvelimella ja tarjoaa helppokäyttöisen tavan käyttää digna-alustaa ja visualisoida datalaatumittareita.

### Mitä uutta julkaisussa 2026.06

Tässä julkaisussa datan observoitavuusominaisuudet tuodaan suoraan koodiin, jolloin kehittäjät voivat valvoa datalaatua lähteellä. Katso täydelliset tiedot [julkaisutiedoista](http://docs.digna.ai/changelog/Release_202606/).

---

## Järjestelmävaatimukset {: #system-requirements }

Ennen asennusta varmista, että järjestelmäsi täyttää seuraavat vähimmäisvaatimukset:

| Vaatimus | Määrittely |
|---|---|
| **Käyttöjärjestelmä** | Windows Server tai Windows 10/11 |
| **Muisti (minimi)** | 16 GB RAM |
| **Levyn vapaa tila** | 10 GB käytettävissä |
| **Tietokanta** | PostgreSQL Server 12 tai uudempi |
| **Web-palvelin** | IIS, Apache Tomcat tai vastaava |

### Tietokannan asennusvaihtoehdot

**Jos PostgreSQL on jo asennettu:**
Voit lisätä uuden tietokannan dignalle olemassa olevaan PostgreSQL-palvelimeesi.

**Jos asennat PostgreSQL:n samalle koneelle kuin digna:**

!!! info "Suositellut resurssit"

    - **Muisti**: 32 GB RAM (16 GB sijaan)
    - **Levyn vapaa tila**: 50 GB käytettävissä (10 GB sijaan)

    Nämä suuremmat resurssivaatimukset huomioivat sekä dignan että PostgreSQL:n samanaikaisen ajon.

---

## Ennen asennusta {: #pre-installation-setup }

Ennen dignan asentamista varmista, että seuraavat kaksi edellytystä ovat kunnossa:

1. **PostgreSQL-palvelin** – laskettujen mittarien ja suorituskykytiedon tallennusta varten
2. **Web-palvelin** – digna Dashboardin isännöintiä varten

Jos näitä komponentteja ei ole vielä asennettu, seuraa alla olevia osioita asentaaksesi ja konfiguroidaksesi ne.

---

## PostgreSQL-palvelimen asennus {: #postgresql-server-setup }

### Jos PostgreSQL on jo käytössä

Jos PostgreSQL on jo asennettu ja toimii paikallisesti tai käytät hallittua etä-PostgreSQL-palvelua, voit siirtyä suoraan [seuraavaan osioon](#web-server-configuration).

### PostgreSQL:n asentaminen

Noudata näitä vaiheita asentaaksesi PostgreSQL:n Windowsille:

#### Vaihe 1: Lataa PostgreSQL

1. Siirry [PostgreSQL Downloads -sivulle](https://www.postgresql.org/download/)
2. Valitse **Windows**
3. Lataa uusin asennustiedosto

#### Vaihe 2: Suorita asennustiedosto

1. Kaksoisklikkaa ladattua asennustiedostoa
2. Seuraa asennusohjelman kehotteita

#### Vaihe 3: Valitse asennushakemisto

Valitse hakemisto, johon PostgreSQL asennetaan. Oletussijainti on yleensä sopiva.

#### Vaihe 4: Valitse komponentit

Vakioasennusta varten pidä oletuskomponentit valittuina.

#### Vaihe 5: Aseta PostgreSQL-superkäyttäjän salasana

Syötä ja vahvista salasana PostgreSQL-superkäyttäjälle (`postgres`). **Tallenna tämä salasana turvallisesti** — tarvitset sitä myöhemmin.

#### Vaihe 6: Määritä porttinumero

Oletusportti on `5432`. Voit käyttää oletusta tai määrittää toisen portin tarvittaessa.

!!! tip "Vinkki"

    Jos portti 5432 on jo käytössä, valitse vaihtoehtoinen portti ja muista tämä myöhemmin konfiguroitaessa.

#### Vaihe 7: Valitse paikallisasetukset (locale)

Valitse tietokannan lokalisaatio. Oletusasetukset toimivat yleensä useimmissa asennuksissa.

#### Vaihe 8: Viimeistele asennus

Klikkaa **Next** lopuista vaiheista ja sitten **Finish**.

#### Vaihe 9: Varmista asennus

Avaa komentokehote ja tarkista PostgreSQL-asennus:

```bash
psql --version
```

Jos asennus onnistui, näet PostgreSQL-version.

---

## Web-palvelimen konfigurointi {: #web-server-configuration }

digna tarvitsee web-palvelimen dashboardin isännöintiin. Valitse yksi seuraavista vaihtoehdoista:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Tarvitset vain yhden näistä palvelimista asennettavaksi ja konfiguroitavaksi.

### IIS-asennus {: #iis-setup }

#### Yleiskatsaus

Internet Information Services (IIS) on Microsoftin web-palvelin verkkosivustojen ja web-sovellusten isännöintiä varten.

#### IIS:n ottaminen käyttöön

1. **Avaa Ohjauspaneeli**
   - Paina `Win + R`
   - Kirjoita `control` ja paina Enter

2. **Siirry Windowsin ominaisuuksiin**
   - Valitse **Ohjelmat**
   - Klikkaa **Ota Windowsin ominaisuuksia käyttöön tai poista niitä käytöstä**

3. **Ota Internet Information Services käyttöön**
   - Etsi **Internet Information Services (IIS)**
   - Rastita valintaruudun
   - Klikkaa **+** laajentaaksesi ja varmista, että seuraavat alikomponentit ovat valittuina:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klikkaa OK** ottaaksesi muutokset käyttöön

5. **Varmista IIS-asennus**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost`
   - Näet IIS:n tervetulosivun

#### Pakollinen: URL Rewrite -moduuli

IIS vaatii URL Rewrite -komponentin. Lataa ja asenna se [Microsoftin viralliselta sivulta](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Pakollinen: MIME-tyyppi Markdown-tiedostoille

Varmistaaksesi, että Markdown-tiedostot (`.md`) palvelin toimittaa oikein IIS:ssä:

1. Avaa **IIS Manager** (paina `Win + R`, kirjoita `inetmgr`, paina Enter)
2. Siirry **Sivustosi > MIME Types**
3. Klikkaa **Add...**
4. Määritä:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Tärkeää"

    Ilman tätä asetusta `.md`-tiedostot eivät välttämättä palveudu oikein.

---

### Apache Tomcat -asennus {: #apache-tomcat-setup }

#### Yleiskatsaus

Apache Tomcat on avoimen lähdekoodin Java-servlet-kontti ja web-palvelin.

#### Asennus

1. **Lataa Apache Tomcat**
   - Siirry [Apache Tomcat Downloads -sivulle](https://tomcat.apache.org/download-90.cgi)
   - Lataa Windows ZIP -jakelu

2. **Pura arkisto**
   - Pura ZIP-tiedosto haluamaasi hakemistoon
   - Esimerkki: `C:\Program Files\Apache Tomcat`

3. **Varmista, että Tomcat toimii**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost:8080`
   - Näet Apache Tomcatin tervetulosivun

!!! tip "Vinkki"

    Tomcat yleensä käynnistyy automaattisesti asennuksen jälkeen. Jos se ei käynnisty, siirry `bin`-kansioon ja suorita `startup.bat`.

---

## Ensiasennus {: #initial-installation }

### Vaihe 1: Luo digna-repository

digna-repository tallentaa kaikki dignan laskemat mittarit. Se toimii keskeisenä tietokantana analytiikka- ja suorituskykytiedoille.

#### Luo skeema ja käyttäjä

Avaa PostgreSQL-asiakas (pgAdmin, psql tai vastaava) ja suorita seuraavat SQL-komennot:

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

!!! tip "Hyvä käytäntö"

    Käytä vahvoja ja monimutkaisia salasanoja tietokantakäyttäjille. Vältä helposti arvattavia tunnuksia.

---

### Vaihe 2: Pura digna-asennuspaketti

1. Etsi saamasi digna-asennus ZIP-tiedosto
2. Pura se haluamaasi asennushakemistoon
3. Puraamisen jälkeen sinun pitäisi nähdä seuraavat kohteet:
   - `dashboard/` — Web-dashboardin käyttöliittymä
   - `digna` — Pääsuoritettava tiedosto (backend + CLI yhdessä)
   - `config.toml` — Konfiguraatiotiedosto
   - `license.toml` — Lisenssitiedosto (kopioi oma tiedostosi tähän)

### Vaihe 3: Asenna lisenssitiedosto

!!! warning "Tärkeää"

    Lisenssitiedosto **ei** sisälly asennuspakettiin ja toimitetaan erikseen dignalta.

1. Etsi sinulle toimitettu `license.toml`-tiedosto
2. Kopioi se dignan asennuksen juurihakemistoon (kohtaan, jossa `config.toml` ja `digna`-suoritettava sijaitsevat)

**Miksi tämä on tärkeää:**
Lisenssitiedosto sisältää asiakastiedot, lisenssin vanhenemispäivän ja digitaalisen allekirjoituksen. **Älä muokkaa tätä tiedostoa** — muutokset mitätöivät lisenssin.

**Hakemistorakenne asennuksen jälkeen:**

```
digna_installation/
├── config.toml         (konfiguraatiotiedosto)
├── license.toml        (OMA LISENSSITIEDOSTO - kopioi tänne)
├── digna               (pääsuoritettava tiedosto)
└── dashboard/          (web-käyttöliittymä)
    └── (dashboard-tiedostot)
```

---

## Backendin konfigurointi {: #backend-configuration }

### Vaihe 1: Luo ja muokkaa konfiguraatiotiedostoa

`config_template.toml`-tiedosto sisältyy digna-asennushakemistoon. Tarvitsee vain nimetä se `config.toml`:ksi.

**Sijainti:** `digna_installation/config.toml`

Avaa `config.toml` tekstieditorissa ja konfiguroi alla olevat osiot.

#### [app] -osio

Tämä osio määrittää dignabackend-sovelluksen asetukset:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametri | Arvo | Huomautukset |
|---|---|---|
| `digna_APP_HOST` | `localhost` tai IP-osoite | Isäntä tai IP, jossa dignabackend ajetaan |
| `digna_APP_PORT` | `8082` (oletus) | REST API -pisteiden portti |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendin URL | Jos dashboard on eri palvelimella, lisää sen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Tarvitaan CORS:lle, kun käytetään tunnuksia |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Salli kaikki HTTP-metodit |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Salli kaikki otsakkeet |

#### [repo] -osio

Tässä osiossa määritellään yhteys PostgreSQL-tietokantaan:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametri | Arvo | Huomautukset |
|---|---|---|
| `digna_REPO_HOST` | `localhost` tai IP | PostgreSQL-palvelimen hostname/IP |
| `digna_REPO_PORT` | `5432` (oletus) | PostgreSQL-portti |
| `digna_REPO_DB` | `postgres` | Tietokannan nimi |
| `digna_REPO_SCHEMA` | `dignarepo` | Aiemmin luotu skeema |
| `digna_REPO_USER` | `digna_user` | PostgreSQL:ssä luotu käyttäjä |
| `digna_REPO_PASSWORD` | Salasanasi | Salasana, joka asetettiin skeeman luomisessa |

#### [base] -osio

Tässä osiossa on turvallisuus- ja evästekonfiguraatiot:

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

| Parametri | Arvo | Huomautukset |
|---|---|---|
| `digna_FERNET_KEY` | Salausavain | Käytetään tokenien ja evästeiden salaukseen (oletusarvo) |
| `digna_COOKIE_DOMAIN` | `localhost` | Vastaamaan frontendiäsi |
| `digna_COOKIE_SECURE` | `false` (paikallinen) / `true` (tuotanto) | Käytä `true` HTTPS-yhteyksissä |
| `digna_COOKIE_HTTPONLY` | `true` | Aina suositeltu turvallisuuden vuoksi |
| `digna_COOKIE_SAME_SITE` | `lax` | Estää CSRF-hyökkäyksiä |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon aikakatkaisu sekunneissa |
| `digna_MAX_WORKERS` | CPU-ytimien määrä - 1 | Samanaikaisten tarkastustehtävien määrä |

#### [logging] -osio

Tässä osiossa määritellään lokituksen käytös:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametri | Arvo | Huomautukset |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotantoon, `DEBUG` vianmääritykseen |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Säilytettävien päivittäisten lokivarotojen määrä |

---

### Vaihe 3: Alusta repository

1. Avaa komentokehote
2. Siirry dignan asennushakemistoon (kohtaan, jossa `config.toml` ja `digna`-suoritettava sijaitsevat)
3. Suorita yhteystesti:

```bash
digna repo check
```

Näet vahvistuksen, että yhteys on muodostettu (itsessään repositorya ei ole vielä alustettu).

### Vaihe 4: Asenna repository-skeema

Samoissa kansioissa suorita:

```bash
digna repo install
```

Tämä komento asentaa tarvittavat taulut ja skeeman PostgreSQL-tietokantaasi.

### Vaihe 5: Käynnistä digna-palvelin

digna-asennushakemistossa käynnistä palvelin:

```bash
digna serve --address <host> --port <port>
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

### Vaihe 6: Luo ylläpitäjäkäyttäjä

1. Avaa **uusi** komentokehote-ikkuna
2. Siirry dignan asennushakemistoon
3. Suorita seuraava komento luodaksesi ylläpitäjäkäyttäjä:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Esimerkki:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Tämä luo käyttäjän, jolla on täydet hallintaoikeudet.

!!! tip "Hyvä käytäntö"

    Käytä vahvaa salasanaa, joka sisältää isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä.

---

## Dashboardin konfigurointi {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön web-palvelimella

digna-dashboardilla on oma erillinen `config.toml`-tiedosto `dashboard/`-hakemistossa. Tämä konfigurointi toimitetaan valmiina eikä vaadi muutoksia alkuasennuksen yhteydessä. Muokkaa sitä vain, jos haluat muuttaa backend-yhteysasetuksia tai tehdä monikoneselvityksiä.

Jos tarvitset dashboardin lisäkonfiguraatiota (esim. monikanta-asennuksissa), katso dashboardin dokumentaatiota.

Valitse web-palvelimesi ja seuraa vastaavia käyttöönotto-ohjeita.

#### Julkaisu IIS:ään

1. **Avaa IIS Manager**
   - Paina `Win + R`, kirjoita `inetmgr`, paina Enter

2. **Luo uusi verkkosivusto**
   - Vasemmassa paneelissa oikeaklikkaa **Sites**
   - Valitse **Add Website...**

3. **Konfiguroi verkkosivusto**
   - **Site Name**: Anna nimi (esim. "dignaDashboard")
   - **Physical Path**: Klikkaa Selaa ja valitse `dashboard`-kansiosi
   - **Binding**: Määritä IP-osoite ja portti (oletusportti HTTP:lle 80, HTTPS:lle 443)

4. **Käynnistä sivusto**
   - Klikkaa **OK** luodaksesi sivun
   - Oikeaklikkaa uutta sivustoa ja valitse **Start**

5. **Testaa asennus**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost` (tai määrittelemääsi URL:iin)
   - Näet digna-dashboardin kirjautumissivun

#### Julkaisu Apache Tomcat:iin

1. **Kopioi dashboard Tomcatiin**
   - Kopioi `dashboard`-kansio Tomcatin `webapps`-hakemistoon
   - Nimeä tarvittaessa uudelleen (esim. `digna`)
   - Esimerkki: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Varmista julkaisu**
   - Päivitä tai lataa Tomcatin hallintasivu uudelleen (http://localhost:8080)
   - Näet "digna" (tai valitsemasi nimen) listattuna julkaistuissa sovelluksissa

3. **Avaa dashboard**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost:8080/digna`
   - Näet digna-dashboardin kirjautumissivun

---

## digna:n ajaminen Windows-palveluna {: #running-digna-as-a-windows-service }

### Miksi käyttää Windows-palvelua?

digna-backendin ajaminen Windows-palveluna takaa, että se:
- Käynnistyy automaattisesti, kun palvelin boottaa
- Ajetaan taustalla ilman avoinna olevaa komentokehote-ikkunaa
- Käynnistyy uudelleen automaattisesti, jos se kaatuu
- Voidaan hallita Windowsin Palvelut-työkalun kautta

### Palvelun hallintatiedostot

Kaikki tarvittavat tiedostot sijaitsevat digna-asennushakemistossa kansiossa: `bin/`

Seuraavat batch-tiedostot ovat käytettävissä:
- `install_service.bat` — Rekisteröi dignan Windows-palveluksi
- `uninstall_service.bat` — Poistaa palvelun rekisteröinnin
- `start_service.bat` — Käynnistää palvelun
- `stop_service.bat` — Pysäyttää palvelun

!!! warning "Järjestelmänvalvojan oikeudet vaaditaan"

    Kaikki batch-tiedostot on suoritettava järjestelmänvalvojan oikeuksin.

### Palvelun asentaminen

1. **Avaa komentokehote järjestelmänvalvojana**
   - Oikeaklikkaa Komentokehote
   - Valitse "Run as Administrator"

2. **Siirry bin-hakemistoon**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Suorita asennusskripti**
   ```bash
   install_service.bat
   ```

digna-palvelin rekisteröityy nyt Windows-palveluna **automaattisella käynnistyksellä**. Palvelu ei käynnisty heti — katso seuraava osio palvelun käynnistämiseksi.

### Palvelun käynnistäminen ja pysäyttäminen

#### Palvelun käynnistäminen

1. Avaa komentokehote järjestelmänvalvojana
2. Siirry `digna\bin`-kansioon
3. Suorita:
   ```bash
   start_service.bat
   ```

#### Palvelun pysäyttäminen

1. Avaa komentokehote järjestelmänvalvojana
2. Siirry `digna\bin`-kansioon
3. Suorita:
   ```bash
   stop_service.bat
   ```

!!! tip "Vinkki"

    Pysäytä aina palvelu ennen sovellustiedostojen päivittämistä.

### Palvelun siirtäminen uuteen hakemistoon

Jos tarvitsee siirtää digna-asennus:

1. **Poista nykyinen palvelu**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Siirrä sovellustiedostot**
   - Siirrä koko digna-asennuskansio uuteen sijaintiin

3. **Asenna palvelu uudelleen**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Käynnistä palvelu**
   ```bash
   start_service.bat
   ```

### Palvelun poistaminen

1. **Pysäytä käynnissä oleva palvelu**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Poista palvelun rekisteröinti**
   ```bash
   uninstall_service.bat
   ```

digna-palvelin on nyt poistettu Windows-palveluista.

---

## Päivitys uuteen julkaisuun {: #upgrading-to-a-new-release }

### Ennen päivitystä

**digna-repositoryn varmuuskopiointi on pakollinen**

Ennen dignan päivittämistä varmuuskopioi repository (PostgreSQL) datan menettämisen estämiseksi.
Varmuuskopio mahdollistaa palautuksen, jos päivityksessä ilmenee odottamattomia ongelmia.

### Päivitysprosessi

#### Vaihe 1: Pysäytä digna-palvelu

Jos digna ajetaan Windows-palveluna, pysäytä se ensin:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Vaihe 2: Varmuuskopioi nykyinen backend-asennus

digna-asennushakemistossa:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Vaihe 3: Pura ja ota uusi versio käyttöön

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritettava ja `dashboard`-kansio asennushakemistoosi


!!! warning "Tärkeää"

    `config.toml`-tiedostoa EI KOSKAAN sisällytetä asennusZIP:iin. Olemassa oleva konfiguraatiosi säilyy ennallaan.

### Vaihe 4: Palauta konfiguraatiotiedostosi

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Vaihe 5: Päivitä repository-skeema

Siirry digna-asennushakemistoon ja suorita:

```bash
digna repo upgrade
```

Tämä päivittää PostgreSQL-skeeman uusimpaan versioon säilyttäen kaikki olemassa olevat tiedot.

### Vaihe 6: Käynnistä palvelut uudelleen

Jos ajetaan Windows-palveluna:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Jos ajetaan manuaalisesti, käynnistä palvelin uudelleen:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jos käytät IIS:ää tai Tomcatia, käynnistä vastaava web-palvelin uudelleen.

#### Vaihe 7: Varmista päivitys

1. Avaa digna-dashboard
2. Varmista, että käyttöliittymä latautuu oikein
3. Tarkista palvelinlokit mahdollisten virheiden varalta
