---
title: Windows-asennusopas – digna Release 2026.06 | digna-dokumentaatio
description: Vaiheittainen opas digna Release 2026.06 -version asentamiseen Windowsille — järjestelmävaatimukset, PostgreSQL-asennus, verkkopalvelimen määritys, backend- ja dashboard-konfiguraatio, dignan ajaminen Windows-palveluna ja päivitys uuteen versioon.
keywords: digna windows-asennus, digna käyttöönotto-opas, digna backend-asennus, digna dashboard-asennus, postgresql-asennus, digna windows-palvelu, digna päivitysohje
image: /assets/logo_square.png
---

# Windows-asennusopas digna Release 2026.06:lle

**Julkaisu:** 2026.06

**Viimeksi päivitetty:** 30. elokuuta 2026


---

## Sisällysluettelo

1. [Johdanto](#introduction)
2. [Järjestelmävaatimukset](#system-requirements)
3. [Ennen asennusta](#pre-installation-setup)
4. [PostgreSQL-palvelimen asennus](#postgresql-server-setup)
5. [Verkkopalvelimen määritys](#web-server-configuration)
6. [Alustava asennus](#initial-installation)
7. [Backendin konfigurointi](#backend-configuration)
8. [Dashboardin konfigurointi](#dashboard-configuration)
9. [dignan ajaminen Windows-palveluna](#running-digna-as-a-windows-service)
10. [Päivitys uuteen julkaisuun](#upgrading-to-a-new-release)

---

## Johdanto {: #introduction }

### Tietoa dignasta

digna on kattava tekoälypohjainen alusta, joka on suunniteltu optimoimaan datalaadun hallintaa erilaisissa dataympäristöissä, kuten tietovarastoissa, data-lakeissa ja lakehouse-ratkaisuissa. Skaalautuvuutensa ja mukautuvuutensa ansiosta digna vastaa nykyajan datahaasteisiin automaation, reaaliaikaisen valvonnan ja poikkeamien havaitsemisen avulla.

digna koostuu kahdesta pääkomponentista:

- **digna**: sovelluksen ydin, joka vastaa tietojen käsittelystä ja laatutarkistusten suorittamisesta. Se yhdistää taustajärjestelmän ja komentorivikäyttöliittymän yhteen suoritettavaan tiedostoon ja korvaa aiempien julkaisujen erilliset ohjelmat `dignabackend` ja `dignacli`.
- **dignadashboard**: Verkkopohjainen käyttöliittymä, joka isännöidään verkkopalvelimella ja tarjoaa käyttäjäystävällisen tavan käyttää digna-alustaa ja visualisoida datalaatumittareita.

### Mitä uutta julkaisussa 2026.06

Tässä julkaisussa datan havaittavuusominaisuudet tuodaan suoraan koodiin, jolloin kehittäjät voivat valvoa datan laatua lähteellä. Katso täydelliset tiedot [release notes](http://docs.digna.ai/changelog/Release_202606/).

### Etsitkö macOS- tai Linux-opasta?

Tämä opas kattaa Windowsin. Muihin alustoihin liittyen katso [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) tai [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Järjestelmävaatimukset {: #system-requirements }

Ennen asennuksen aloittamista varmista, että järjestelmäsi täyttää seuraavat vähimmäisvaatimukset:

| Vaatimus | Määrittely |
|---|---|
| **Käyttöjärjestelmä** | Windows Server tai Windows 10/11 |
| **Muisti (minimi)** | 16 GB RAM |
| **Levypinta-ala** | 10 GB vapaata tilaa |
| **Tietokanta** | PostgreSQL Server 12 tai uudempi |
| **Verkkopalvelin** | IIS, Apache Tomcat tai vastaava |

### Tietokannan asennusvaihtoehdot

**Jos PostgreSQL on jo asennettu:**
Voit lisätä uuden tietokannan dignaa varten olemassa olevaan PostgreSQL-palvelimeesi.

**Jos asennat PostgreSQLin samalle koneelle kuin digna:**

!!! info "Suositellut määritykset"

    - **Muisti**: 32 GB RAM (16 GB sijaan)
    - **Levypinta-ala**: 50 GB vapaata tilaa (10 GB sijaan)

    Nämä korkeammat määritykset mahdollistavat sekä dignan että PostgreSQL-tietokannan samanaikaisen ajon.

---

## Ennen asennusta {: #pre-installation-setup }

Ennen dignan asentamista varmista, että kaksi keskeistä edellytystä ovat paikallaan:

1. **PostgreSQL-palvelin** – laskettujen mittareiden ja suorituskykytietojen tallentamista varten
2. **Verkkopalvelin** – digna Dashboardin isännöintiä varten

Jos näitä komponentteja ei ole vielä asennettu, seuraa alla olevia osioita niiden asentamiseksi ja konfiguroimiseksi.

---

## PostgreSQL-palvelimen asetukset {: #postgresql-server-setup }

### Jos sinulla on jo PostgreSQL

Jos PostgreSQL on jo asennettu ja käynnissä paikallisesti tai käytät hallittua etä-PostgreSQL-palvelinta, voit siirtyä suoraan [seuraavaan osioon](#web-server-configuration).

### PostgreSQLin asentaminen

Noudata näitä ohjeita PostgreSQLin asentamiseksi Windowsille:

#### Vaihe 1: Lataa PostgreSQL

1. Siirry [PostgreSQL Downloads -sivulle](https://www.postgresql.org/download/)
2. Valitse **Windows**
3. Lataa uusin asennusohjelma

#### Vaihe 2: Suorita asennusohjelma

1. Kaksoisnapsauta ladattua asennustiedostoa
2. Seuraa asennusohjelman ohjeita

#### Vaihe 3: Valitse asennushakemisto

Valitse hakemisto, johon PostgreSQL asennetaan. Oletussijainti on yleensä sopiva.

#### Vaihe 4: Valitse komponentit

Pidä oletusarvoiset komponenttiasetukset valittuina tavallista asennusta varten.

#### Vaihe 5: Aseta PostgreSQL-superkäyttäjän salasana

Anna ja vahvista salasana PostgreSQLin superkäyttäjälle (`postgres`). **Tallenna tämä salasana turvallisesti** — tarvitset sitä myöhemmin.

#### Vaihe 6: Määritä porttinumero

Oletusportti PostgreSQLille on `5432`. Voit käyttää oletusta tai määrittää toisen portin tarvittaessa.

!!! tip "Vinkki"

    Jos portti 5432 on jo käytössä, valitse vaihtoehtoinen portti ja merkitse se myöhempää konfigurointia varten.

#### Vaihe 7: Valitse paikallisasetukset (Locale)

Valitse tietokannan paikallisasetukset. Oletusasetukset sopivat yleensä useimpiin asennuksiin.

#### Vaihe 8: Viimeistele asennus

Klikkaa **Seuraava** läpi jäljellä olevien vaiheiden ja lopuksi **Valmis**.

#### Vaihe 9: Vahvista asennus

Avaa komentokehote ja varmista, että PostgreSQL on asennettu:

```bash
psql --version
```

Näet PostgreSQL-version, jos asennus onnistui.

---

## Verkkopalvelimen määritys {: #web-server-configuration }

digna tarvitsee verkkopalvelimen dashboardin isännöintiin. Valitse yksi seuraavista vaihtoehdoista:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Tarvitset vain yhden näistä palvelimista asennettavaksi ja konfiguroitavaksi.

### IIS:n käyttöönotto {: #iis-setup }

#### Yleiskatsaus

Internet Information Services (IIS) on Microsoftin verkkopalvelin verkkosivustojen ja web-sovellusten isännöintiin.

#### IIS:n ottaminen käyttöön

1. **Avaa Ohjauspaneeli**
   - Paina `Win + R`
   - Kirjoita `control` ja paina Enter

2. **Siirry Windowsin ominaisuuksiin**
   - Klikkaa **Ohjelmat**
   - Valitse **Ota Windowsin ominaisuuksia käyttöön tai poista niitä käytöstä**

3. **Ota Internet Information Services käyttöön**
   - Selaa alas ja etsi **Internet Information Services (IIS)**
   - Valitse valintaruutu ottaaksesi sen käyttöön
   - Klikkaa **+** laajentaaksesi ja varmista, että nämä alikomponentit ovat valittuna:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Klikkaa OK** hyväksyäksesi muutokset

5. **Vahvista IIS-asennus**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost`
   - Näet IIS:n tervetulosivun

#### Pakollinen: URL Rewrite -moduuli

IIS tarvitsee URL Rewrite -komponentin. Lataa ja asenna se [viralliselta Microsoftin sivulta](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Pakollinen: MIME-tyyppi Markdown-tiedostoille

Varmistaaksesi, että Markdown-tiedostot (`.md`) palvelimella toimitetaan oikein:

1. Avaa **IIS Manager** (paina `Win + R`, kirjoita `inetmgr`, paina Enter)
2. Siirry **Sivustosi > MIME Types**
3. Klikkaa **Add...**
4. Määritä:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Tärkeää"

    Ilman tätä asetusta `.md`-tiedostoja ei välttämättä toimiteta oikein.

---

### Apache Tomcatin asennus {: #apache-tomcat-setup }

#### Yleiskatsaus

Apache Tomcat on avoimen lähdekoodin Java-servlet-kontti ja verkkopalvelin.

#### Asennus

1. **Lataa Apache Tomcat**
   - Siirry kohtaan [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Lataa Windows ZIP-distribuutio

2. **Pura arkisto**
   - Pura ZIP-tiedosto haluamaasi hakemistoon
   - Esimerkki: `C:\Program Files\Apache Tomcat`

3. **Vahvista, että Tomcat on käynnissä**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost:8080`
   - Näet Apache Tomcatin tervetulosivun

!!! tip "Vinkki"

    Apache Tomcat käynnistyy yleensä automaattisesti asennuksen jälkeen. Jos se ei käynnisty, siirry `bin`-kansioon ja suorita `startup.bat`.

---

## Alustava asennus {: #initial-installation }

### Vaihe 1: Aseta digna-repositorio

digna-repositorio tallentaa kaikki dignan laskemat mittarit. Se toimii keskeisenä tietokantana analytiikka- ja suorituskykytiedoille.

#### Luo repositorion skeema ja käyttäjä

Avaa PostgreSQL-asiakasohjelmaasi (pgAdmin, psql tai vastaava) ja suorita seuraavat SQL-komennot:

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

    Käytä vahvoja, monimutkaisia salasanoja tietokantakäyttäjille. Vältä helposti arvattavia tunnuksia.

---

### Vaihe 2: Pura digna-asennuspaketti

1. Etsi sinulle toimitettu digna-asennus ZIP-tiedosto
2. Pura se haluamaasi asennushakemistoon
3. Purkamisen jälkeen näet seuraavat kohteet:
   - `dashboard/` — Web-dashboardin käyttöliittymä
   - `digna` — Pääsuoritettava tiedosto (backend + CLI yhdistettynä)
   - `config.toml` — Konfiguraatiotiedosto
   - `license.toml` — Lisenssitiedosto (kopioi oma lisenssi tähän)

### Vaihe 3: Asenna lisenssitiedosto

!!! warning "Tärkeää"

    Lisenssitiedostoa **ei** sisälly asennuspakettiin, vaan se toimitetaan erikseen dignalta.

1. Etsi sinulle toimitettu `license.toml`-tiedosto
2. Kopioi se dignan asennuksen juurihakemistoon (kohtaan, jossa `config.toml` ja suoritettava `digna` sijaitsevat)

**Miksi tämä on tärkeää:**
Lisenssitiedosto sisältää asiakastietosi, lisenssin vanhenemispäivän ja digitaalisen allekirjoituksen. **Älä muuta tätä tiedostoa** — muutokset mitätöivät sen.

**Hakemistorakenne asennuksen jälkeen:**

```
digna_installation/
├── config.toml         (konfiguraatiotiedosto)
├── license.toml        (SINUN LISENSSITIEDOSTOSI - kopioi tänne)
├── digna               (pääsuoritettava tiedosto)
└── dashboard/          (web-käyttöliittymä)
    └── (dashboard-tiedostot)
```

---

## Backendin konfigurointi {: #backend-configuration }

### Vaihe 1: Luo ja muokkaa konfiguraatiotiedostoa

`config_template.toml`-tiedosto sisältyy digna-asennushakemistoon. Sinun tarvitsee vain nimetä se `config.toml`:ksi.

Sijainti: `digna_installation/config.toml`

Avaa `config.toml` tekstieditorissa ja konfiguroi alla olevat osiot.

#### [app] -osio

Tämä osio määrittelee digna-backend-sovelluksen asetukset:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `digna_APP_HOST` | `localhost` tai IP-osoite | Isäntä tai IP, jossa dignabackend isännöidään |
| `digna_APP_PORT` | `8082` (oletus) | REST-API:en portti |
| `digna_APP_CORS_ALLOW_ORIGINS` | Frontendin URL | Jos dashboard sijaitsee eri palvelimella, lisää sen URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Vaaditaan CORS-kirjautumisten kanssa |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Salli kaikki HTTP-metodit |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Salli kaikki otsikot |

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

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `digna_REPO_HOST` | `localhost` tai IP | PostgreSQL-palvelimen isäntä/IP |
| `digna_REPO_PORT` | `5432` (oletus) | PostgreSQL-portti |
| `digna_REPO_DB` | `postgres` | Tietokannan nimi |
| `digna_REPO_SCHEMA` | `dignarepo` | Aiemmin luotu skeema |
| `digna_REPO_USER` | `digna_user` | PostgreSQLissä luotu käyttäjä |
| `digna_REPO_PASSWORD` | Salasanasi | Skeeman luomisessa asetettu salasana |

#### [base] -osio

Tämä osio sisältää suojaus- ja evästeasetuksia:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Vastaa frontendin domainia |
| `digna_COOKIE_SECURE` | `false` (paikallinen) / `true` (produktiio) | Käytä `true` HTTPS-yhteyksissä |
| `digna_COOKIE_HTTPONLY` | `true` | Aina käytössä turvallisuuden vuoksi |
| `digna_COOKIE_SAME_SITE` | `lax` | Estää CSRF-hyökkäyksiä |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon vanhenemisaika sekunteina |
| `digna_MAX_WORKERS` | CPU-ytimien lukumäärä - 1 | Samanaikaisten tarkastustehtävien määrä |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Enimmäisviive sekunteina, jonka ajastin saa lisätä ennen erääntyneen työn käynnistämistä |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Kellonaika (24 tunnin muoto `HH:MM`), jolloin päivittäinen siivous alkaa |

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
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotantoon, `DEBUG` vianetsintään |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Säilytettävien päivittäisten lokavarmuuskopioiden määrä |

---

### Vaihe 2: Tarkista konfiguraatio

Varmista ennen arkiston alustusta, että `config.toml` on täydellinen ja oikein muodostettu. Suorita digna-asennushakemistossasi:

```bash
digna config check
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

Overall: OK
```

Korjaa kaikki, mikä raportoidaan tilassa FAILED, ja suorita komento uudelleen ennen jatkamista. Täydellinen luettelo valinnoista on [CLI-viitteessä](../../../cli/Command_Line_Interface_202606.md).

### Vaihe 3: Alusta repositorio-yhteys

1. Avaa komentokehote
2. Siirry digna-asennuskansioon (kohtaan, jossa `config.toml` ja suoritettava `digna` sijaitsevat)
3. Suorita yhteystesti:

```bash
digna repo check
```

Sinun pitäisi nähdä vahvistus siitä, että yhteys on muodostettu (repoa ei ole vielä asennettu).

### Vaihe 4: Asenna repositorion skeema

Samassa hakemistossa suorita:

```bash
digna repo install
```

Tämä komento asentaa tarvittavat taulut ja skeeman PostgreSQL-tietokantaasi.

### Vaihe 5: Luo ylläpitäjäkäyttäjä

1. Avaa **uusi** komentokehoteikkuna
2. Siirry digna-asennushakemistoon
3. Suorita seuraava komento luodaksesi ylläpitäjäkäyttäjän:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Esimerkki:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Tämä luo käyttäjän, jolla on täydet järjestelmänvalvojan oikeudet.

!!! tip "Hyvä käytäntö"

    Käytä vahvaa salasanaa, jossa on isoja ja pieniä kirjaimia, numeroita ja erikoismerkkejä.

---

### Vaihe 6: Käynnistä digna-palvelin

digna-asennushakemistossa käynnistä palvelin komennolla:

```bash
digna serve --address <host> --port <port>
```

**Parametrit:**
- `--address` — Palvelimen isäntä tai IP
- `--port` — Palvelimen portti

Näet käynnistysviestit, jotka vahvistavat palvelimen käynnistyksen:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Palvelin varaa päätteen"

    `serve` toimii edustalla ja jatkaa, kunnes pysäytät sen näppäinyhdistelmällä ++ctrl+c++. Anna sen olla käynnissä, kun viimeistelet asennuksen; automaattisen käynnistyksen osalta katso [dignan suorittaminen Windows-palveluna](#running-digna-as-a-windows-service).

## Dashboardin konfigurointi {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön verkkopalvelimella

Digna-dashboardilla on erillinen `config.toml`-tiedosto, joka sijaitsee `dashboard/`-hakemistossa. Tämä konfiguraatio toimitetaan valmiina eikä vaadi muutoksia alkuasennuksessa. Sinun tarvitsee muuttaa sitä vain, jos haluat mukauttaa backend-yhteyttä tai tehdä moninstance-asennuksia.

Jos tarvitset muutoksia dashboardin konfiguraatioon, katso dashboardin dokumentaatiota.

Valitse verkkopalvelimesi ja seuraa vastaavia käyttöönotto-ohjeita.

#### Käyttöönotto IIS:ssä

1. **Avaa IIS Manager**
   - Paina `Win + R`, kirjoita `inetmgr`, paina Enter

2. **Luo uusi verkkosivusto**
   - Vasemmassa paneelissa napsauta hiiren oikealla **Sites**
   - Valitse **Add Website...**

3. **Määritä verkkosivusto**
   - **Site Name**: Anna nimi (esim. "dignaDashboard")
   - **Physical Path**: Selaa ja valitse `dashboard`-kansiosi
   - **Binding**: Aseta IP-osoite ja portti (oletus 80 HTTP:lle, 443 HTTPS:lle)

4. **Käynnistä sivusto**
   - Klikkaa **OK** luodaksesi sivuston
   - Napsauta hiiren oikealla uutta sivustoa ja valitse **Start**

5. **Testaa asennus**
   - Avaa selain
   - Siirry `http://localhost` (tai määrittämääsi URL:iin)
   - Näet digna-dashboardin kirjautumissivun

#### Käyttöönotto Apache Tomcatissa

1. **Kopioi dashboard Tomcatiin**
   - Kopioi `dashboard`-kansio Tomcatin `webapps`-hakemistoon
   - Nimeä se tarvittaessa uudelleen (esim. `digna`)
   - Esimerkki: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Vahvista käyttöönotto**
   - Päivitä tai lataa Tomcatin hallintasivu uudelleen (http://localhost:8080)
   - Näet listauksen asennetuista sovelluksista, josta pitäisi löytyä "digna" (tai valitsemasi nimi)

3. **Pääsy dashboardiin**
   - Avaa selain
   - Siirry osoitteeseen `http://localhost:8080/digna`
   - Näet digna-dashboardin kirjautumissivun

---

## dignan ajaminen Windows-palveluna {: #running-digna-as-a-windows-service }

### Miksi käyttää Windows-palvelua?

digna-backendin ajaminen Windows-palveluna varmistaa, että se:
- Käynnistyy automaattisesti palvelimen käynnistyessä
- Ajaa taustalla ilman avattua komentokehoteikkunaa
- Käynnistyy uudelleen automaattisesti kaatumistapauksissa
- On hallittavissa Windowsin Palvelut-työkalulla

### Palvelun hallintatiedostot

Kaikki tarvittavat tiedostot sijaitsevat digna-asennushakemistossa polussa: `bin/`

Seuraavat bat-tiedostot ovat käytettävissä:
- `install_service.bat` — Rekisteröi dignan Windows-palveluna
- `uninstall_service.bat` — Poistaa palvelun rekisteröinnin
- `start_service.bat` — Käynnistää palvelun
- `stop_service.bat` — Pysäyttää palvelun

!!! warning "Ylläpitäjäoikeudet vaaditaan"

    Kaikki bat-tiedostot on suoritettava järjestelmänvalvojan oikeuksin.

### Palvelun asentaminen

1. **Avaa komentokehote järjestelmänvalvojana**
   - Napsauta komentokehote oikealla painikkeella
   - Valitse "Run as Administrator"

2. **Siirry bin-kansioon**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Suorita asennusskripti**
   ```bash
   install_service.bat
   ```

digna-palvelin on nyt rekisteröity Windows-palveluna automaattisella käynnistyksellä. Palvelu ei käynnisty välittömästi — katso seuraavaa osiota käynnistystä varten.

### Palvelun käynnistäminen ja pysäyttäminen

#### Palvelun käynnistäminen

1. Avaa komentokehote järjestelmänvalvojana
2. Siirry `digna\bin`-hakemistoon
3. Suorita:
   ```bash
   start_service.bat
   ```

#### Palvelun pysäyttäminen

1. Avaa komentokehote järjestelmänvalvojana
2. Siirry `digna\bin`-hakemistoon
3. Suorita:
   ```bash
   stop_service.bat
   ```

!!! tip "Vinkki"

    Pysäytä aina palvelu ennen sovellustiedostojen päivittämistä.

### Palvelun siirtäminen uuteen hakemistoon

Jos sinun on siirrettävä digna-asennus:

1. **Poista nykyinen palvelu**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Siirrä sovellustiedostot**
   - Siirrä koko digna-asennushakemisto uuteen sijaintiin

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

2. **Poista palvelu**
   ```bash
   uninstall_service.bat
   ```

digna-palvelin on nyt poistettu Windows-palveluna rekisteristä.

---

## Päivitys uuteen julkaisuun {: #upgrading-to-a-new-release }

### Ennen päivitystä

**Tarkista ensin kaikki tietokantayhteydet**

Julkaisusta 2026.06 alkaen digna tavoittaa jokaisen lähdeteknologian **ODBC**:n kautta. Aiemmat julkaisut tarjosivat valinnan teknologiakohtaisen ajurin ja ODBC:n välillä kytkimellä **Use ODBC**. digna-tiimi päätti rakentaa pelkästään ODBC:n varaan, koska yksi standardoitu rajapinta antaa enemmän kuin joukko räätälöityjä ajureita:

- **Todennus** — todennus on osa ODBC:tä, joten yhteys voi käyttää kaikkea, mitä sen ajuri tukee: salasanoja, tokeneita ja PAT-tunnisteita, Kerberosta ja Active Directorya, monivaiheista tunnistautumista ja selainpohjaista kertakirjautumista, pilvi-identiteettejä, asiakasvarmenteita ja TLS:ää. Uudet menetelmät tulevat ajuripäivityksen mukana sen sijaan, että odotettaisiin digna-julkaisua.
- **Tietokantatoimittajien ylläpitämät ajurit** — toimittajan oma ajuri seuraa uusia palvelinversioita ja tietoturvakorjauksia, ja voit päivittää sen omassa aikataulussasi dignasta riippumatta.
- **Yksi tapa määrittää kaikki** — jokainen teknologia on avain–arvo-ominaisuuksien luettelo, samalla käyttöliittymällä, samalla arkaluontoisten arvojen salauksella ja samalla vianmäärityksellä, eikä eri kenttäjoukolla lähdettä kohden.
- **Hienosäätö ja kattavuus** — ajuritason valinnat kuten aikakatkaisut, TLS-asetukset, välityspalvelimet ja hakukoot ovat käytettävissä jokaiselle lähteelle, ja mikä tahansa teknologia, jolla on standardin mukainen ODBC-ajuri, voidaan liittää — myös sellaiset, joille digna ei julkaise omaa opasta.

Käytännössä tämä tarkoittaa, ettei kytkintä **Use ODBC** eikä erillisiä isäntä-, portti-, tietokanta-, käyttäjä- ja salasanakenttiä ole enää olemassa. **Jokainen yhteys, joka ei jo käytä ODBC:tä, on muutettava ODBC:ksi** — automaattista muunnosta ei ole, joten suunnittele tämä ennen päivitystä:

1. Käy läpi jokainen asennuksessasi määritelty tietokantayhteys ja merkitse muistiin ne, jotka eivät vielä käytä ODBC:tä — jokainen niistä on määritettävä uudelleen.
2. Asenna vastaava ODBC-ajuri digna-isäntään — yhteydet avataan palvelimelta, jolla digna-taustajärjestelmä toimii, ei selaimesta. Katso [ODBC-ajurin asentaminen digna-isäntään](../../../databases/overview.md#install-the-driver).
3. Pidä ODBC-ominaisuudet valmiina jokaiselle koskevalle yhteydelle. [Teknologiaoppaat](../../../databases/overview.md#technology-guides) luettelevat lähdekohtaisen, koetellun ominaisuusjoukon.

Muuta päivityksen jälkeen jokainen koskeva yhteys ODBC:ksi ja testaa se hallintapaneelista — katso [Tietokantayhteyden luominen](../../../databases/overview.md#create-a-database-connection) ja [Yhteyden testaaminen](../../../databases/overview.md#testing-a-connection).

!!! warning "Databricks Legacy -yhteydet"

    Databricks Legacy -liitin on poistettu tässä julkaisussa. Siirrä nämä yhteydet [Databricks](../../../databases/databricks_connector_guide.md)-liittimeen.

**digna-repositorion varmuuskopiointi on pakollista**

Ennen dignan päivittämistä tee varmuuskopio repositoriostasi (PostgreSQL) suojautuaksesi datan menetykseltä. Varmuuskopio mahdollistaa toipumisen, jos päivityksessä ilmenee odottamattomia ongelmia.

### Päivitysprosessi

#### Vaihe 1: Pysäytä digna-palvelu

Jos digna on käynnissä Windows-palveluna, pysäytä se ensin:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Vaihe 2: Varmuuskopioi nykyinen asennus

Nimeä digna-asennushakemistossa nykyisen asennuksen kansiot uudelleen, jotta uusi julkaisu voidaan ottaa käyttöön niiden rinnalle:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend ja dignacli eivät ole enää käytössä"

    Julkaisusta 2026.06 alkaen `dignabackend` ja `dignacli` korvataan yhdellä suoritettavalla tiedostolla `digna`, joka yhdistää taustajärjestelmän ja CLI:n. Säilytä `dignabackend_old` ja `dignacli_old` vain siihen asti, kunnes olet varmistanut päivityksen — sen jälkeen voit poistaa molemmat kansiot. Säilytä `dashboard_old`, kunnes olet palauttanut siitä konfiguraatiotiedostosi (katso vaihe 4).

#### Vaihe 3: Pura ja ota käyttöön uusi versio

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritettava ja `dashboard`-kansio asennushakemistoosi


!!! warning "Tärkeää"

    `config.toml`-tiedostoa ei **koskaan** sisällytetä asennus-ZIPiin. Olemassa oleva konfiguraatiosi säilyy turvassa.

#### Vaihe 4: Palauta konfiguraatiotiedostosi

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Julkaisu 2026.06 muuttaa config.toml-tiedostoa"

    Kolme asetusta on uusia ja pakollisia, ja yksi ei ole enää käytössä. Aiemmasta julkaisusta peritty `config.toml` ei sisällä uusia asetuksia, eikä digna käynnisty niin kauan kuin ne puuttuvat. Lisää seuraavat olemassa olevaan `config.toml`-tiedostoosi:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Lisää kaksi `[base]`-avainta olemassa olevaan `[base]`-osioosi ja lisää `[encryption]` uutena osiona. Poista sen jälkeen **`digna_FERNET_KEY`** osiosta `[base]` — sitä ei enää käytetä.

    Kunkin asetuksen merkitys on kuvattu kohdassa [Taustajärjestelmän konfigurointi](#backend-configuration).

!!! warning "Kertakirjautuminen: [oidc_clients]-muoto on muuttunut"

    Julkaisu 2026.06 korvaa taulukkotaulukon yhdellä taululla palveluntarjoajaa kohden, nimettynä palveluntarjoajan avaimen mukaan. `DIGNA_OIDC_KEY` poistuu — avain on nyt osa osion otsikkoa.

    Ennen:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Jälkeen:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Toista osio jokaiselle palveluntarjoajalle ja pidä jokainen avain samana kuin `key` tiedostossa `dashboard_config.toml`. `digna config check` raportoi `oidc_clients`-osion tilassa FAILED niin kauan kuin vanha muoto on yhä paikallaan. Tämä koskee vain asennuksia, jotka käyttävät kertakirjautumista.

#### Vaihe 5: Tarkista konfiguraatio

Varmista, että päivitetty `config.toml` on täydellinen ennen kuin kosket arkistoon:

```bash
digna config check
```

Jokaisen osion on raportoitava OK. Korjaa kaikki, mikä raportoidaan tilassa FAILED, ja suorita komento uudelleen ennen jatkamista.

#### Vaihe 6: Päivitä repositorion skeema

Siirry digna-asennushakemistoon ja suorita:

```bash
digna repo upgrade
```

Tämä päivittää PostgreSQL-skeeman uusimpaan versioon säilyttäen kaikki nykyiset tiedot.

#### Vaihe 7: Käynnistä palvelut uudelleen

Jos käytät Windows-palvelua:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Jos ajat palvelinta manuaalisesti, käynnistä se uudelleen:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jos käytät IIS:ää tai Tomcatia, käynnistä vastaava verkkopalvelin uudelleen.

#### Vaihe 8: Vahvista päivitys

1. Avaa digna-dashboard
2. Varmista, että käyttöliittymä latautuu oikein
3. Tarkista palvelinlokit mahdollisten virheiden varalta
4. Muuta jokainen yhteys, joka ei vielä käyttänyt ODBC:tä, ODBC:ksi ja testaa sitten kaikki yhteydet — katso [Yhteyden testaaminen](../../../databases/overview.md#testing-a-connection)