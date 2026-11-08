---
title: Windows-asennusopas – digna Release 2026.11 | digna-dokumentaatio
description: Vaiheittainen opas digna Release 2026.11 -version asentamiseen Windowsille — järjestelmävaatimukset, PostgreSQL-asennus, verkkopalvelimen määritys, backend- ja dashboard-konfiguraatio, dignan ajaminen Windows-palveluna ja päivitys versiosta Release 2026.06.
keywords: digna windows-asennus, digna käyttöönotto-opas, digna backend-asennus, digna dashboard-asennus, postgresql-asennus, digna windows-palvelu, digna päivitysohje
image: /assets/logo_square.png
---

# Windows-asennusopas digna Release 2026.11:lle

**Julkaisu:** 2026.11

**Viimeksi päivitetty:** 7. marraskuuta 2026


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

### Mitä uutta julkaisussa 2026.11

Tämä julkaisu tuo mukanaan digna Data Reconciliationin, digna Agenticin ja digna MCP Serverin sekä digna Enginen, joka voi profiloida dataa dignan sisällä ja tarkistaa viite-eheyden eri tietokantateknologioiden välillä. Katso täydet tiedot [release notes](../../../changelog/Release_202611.md).

Asennuksen kannalta julkaisu tuo uuden repositorion migraatiomekanismin, valinnaisen `[duckdb]`-osion `config.toml`-tiedostoon digna Engineä varten sekä uuden lisenssitiedoston. [Päivitysosio](#upgrading-to-a-new-release) käsittelee jokaisen niistä.

### Etsitkö macOS- tai Linux-opasta?

Tämä opas kattaa Windowsin. Muihin alustoihin liittyen katso [macOS Installation Guide](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) tai [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Tietokantayhteydet, joiden profilointisijaintina on digna Engine, profiloidaan itse
    digna-isännällä. Varaa niille lisää muistia ja levytilaa, katso
    [\[duckdb\]-osio](#duckdb-section).

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

!!! info "Konfiguraatio- ja lisenssitiedostot eivät sisälly pakettiin"

    Asennuksen mukana ei toimiteta `config.toml`- eikä `dashboard/dashboard_config.toml`-tiedostoa — luot
    molemmat itse kohdissa [Backendin määritys](#backend-configuration) ja
    [Dashboardin määritys](#dashboard-configuration). Myöskään `license.toml` ei sisälly pakettiin;
    digna toimittaa sen erikseen, kuten vaiheessa 3 kuvataan.

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

Tässä osiossa määritetään dashboardin ja backendin välinen cross-origin resource sharing (CORS):

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Dashboardin URL-osoitteet | URL-osoitteet, joista dashboard tarjoillaan. Selaimen pyynnöt mistä tahansa muusta originista hylätään |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Pakollinen, jotta selain lähettää istuntoevästeen jokaisen pyynnön mukana |

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

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` tai IP | PostgreSQL-palvelimen isäntä/IP |
| `DIGNA_REPO_PORT` | `5432` (oletus) | PostgreSQL-portti |
| `DIGNA_REPO_DB` | `postgres` | Tietokannan nimi |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Aiemmin luotu skeema |
| `DIGNA_REPO_USER` | `digna_user` | PostgreSQLissä luotu käyttäjä |
| `DIGNA_REPO_PASSWORD` | Salasanasi | Skeeman luomisessa asetettu salasana |
| `DIGNA_REPO_SSLMODE` | `prefer` (oletus) | Valinnainen. PostgreSQL:n SSL-tila: `disable`, `allow`, `prefer`, `require`, `verify-ca` tai `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (oletus) | Valinnainen. Yhteyksien määrä, jonka digna pitää avoinna repositorioon |

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

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `DIGNA_FERNET_KEY` | Yllä näytetty arvo | Aiempien julkaisujen käyttämän salauksen avain. Sen on oltava mukana; säilytä näytetty arvo |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Isäntä, jonka kautta dashboardia käytetään. `""` ei aseta domainia, mikä on oikein välityspalvelimen takana, joka tarjoaa dashboardin ja backendin saman originin alla |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Oltava `true` aina, kun dignaa tarjoillaan HTTPS:n kautta |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Pitää istuntoevästeen skriptien ulottumattomissa |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 tuntia) | Istunnon vanhenemisaika sekunteina |
| `DIGNA_MAX_WORKERS` | CPU-ytimien lukumäärä - 1 | Samanaikaisesti ajettavien tarkastusten enimmäismäärä |
| `DIGNA_FRONTEND_BASEURL` | Dashboardin URL | Pakollinen. Käytetään ilmoitusviestien linkeissä, joten sen on oltava URL, jonka vastaanottajat voivat avata |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (oletus) | Valinnainen. Sekunnit, joiden ajan yksittäinen lähdetietokantaan kohdistuva kysely saa olla käynnissä ennen keskeytystä; `0` poistaa aikakatkaisun käytöstä |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (oletus) | Valinnainen. Sekunnit, joiden ajan lähdetietokantayhteyttä odotetaan; `0` odottaa rajattomasti |

#### [encryption] -osio

Tämä osio sisältää avaimen, jolla arkiston arkaluontoiset arvot salataan. Se on **pakollinen** — `config check` raportoi osion `[encryption]` tilassa FAILED, jos avain puuttuu.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametri | Arvo | Huomautuksia |
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

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` tai `DEBUG` | `INFO` tuotantoon, `DEBUG` vianetsintään. Myös `TRACE`, `WARN` ja `ERROR` hyväksytään |
| `DIGNA_LOGGING_DIR` | `logs` (oletus) | Valinnainen. Kiertävien lokitiedostojen hakemisto suhteessa työhakemistoon |
| `DIGNA_LOGGING_MAX_FILES` | `30` (oletus) | Valinnainen. Säilytettävien kierrätettyjen lokitiedostojen määrä |

!!! warning "Säilytä lokihakemisto, kun digna toimii palveluna"

    Windows-palvelulla ei ole konsolia, joten lokitiedostot ovat ainoa tallenne siitä, mitä palvelu
    tekee. Älä aseta `DIGNA_LOGGING_DIR`-arvoksi tyhjää merkkijonoa, sillä se poistaa lokitiedostot käytöstä.

#### [duckdb] -osio (valinnainen) {: #duckdb-section }

Uutta Release 2026.11:ssä. Tämä osio määrittää **digna Enginen** resurssit. digna Engine profiloi
dataa dignan sisällä niille tietokantayhteyksille, joiden profilointisijainti on **digna Engine**, ja
suorittaa viite-eheystarkistuksia eri tietokantayhteyksien tietolähteiden välillä. Katso
[Profilointisijainti](../../../platform/profiling/profiling_location.md).

Osio on valinnainen. Ilman sitä käytetään alla olevia oletusarvoja.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametri | Arvo | Huomautuksia |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (oletus) | Muisti megatavuina, jota yksi digna Engine -ajo saa käyttää. Enintään `DIGNA_MAX_WORKERS` ajoa voi olla käynnissä samanaikaisesti |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Oletus: dignaa ajavan tilin väliaikaishakemisto (`%TEMP%`) | Väliaikaistiedostojen hakemisto, kun data ei mahdu muistiin |

!!! tip "digna Enginen mitoitus"

    Varaa digna-isännälle enintään `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` muistia
    dignan oman muistinkäytön lisäksi, ja väliaikaishakemistoon riittävästi vapaata levytilaa
    suurimmalle tarkastetulle päivämäärälle niistä tietolähteistä, jotka käyttävät digna Engineä.
    Osoita `DIGNA_DUCKDB_TEMP_DIRECTORY` levylle, jolla on tämä tila ja johon dignaa ajava tili
    voi kirjoittaa:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Tarvitset tätä osiota vain, jos vähintään yksi tietokantayhteys käyttää digna Engineä tai
    viite-eheystarkistus vertaa eri yhteyksien tietolähteitä.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Korjaa kaikki, mikä raportoidaan tilassa FAILED, ja suorita komento uudelleen ennen jatkamista. Kohdan **Unknown keys** alla oleva WARNING luettelee `config.toml`-tiedoston avaimet, joita digna ei lue; niillä ei ole vaikutusta, joten poista ne tai korjaa niiden kirjoitusasu. Täydellinen luettelo valinnoista on [CLI-viitteessä](../../../cli/Command_Line_Interface_202611.md).

### Vaihe 3: Alusta repositorio-yhteys

1. Avaa komentokehote
2. Siirry digna-asennuskansioon (kohtaan, jossa `config.toml` ja suoritettava `digna` sijaitsevat)
3. Suorita yhteystesti:

```bash
digna repo check
```

Uudessa skeemassa komento muodostaa yhteyden ja ilmoittaa sitten, ettei repositoriota ole vielä asennettu:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Tässä vaiheessa tämä on odotettu tulos: se vahvistaa, että digna tavoittaa PostgreSQL:n ja skeeman. Yhteys- tai todennusvirhe sen sijaan viittaa `[repo]`-osioon tai PostgreSQL-asetuksiin.

### Vaihe 4: Asenna repositorion skeema

Samassa hakemistossa suorita:

```bash
digna repo upgrade
```

Tämä komento asentaa tarvittavat taulut repositorion skeemaan ja päättyy ilmoitukseen:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade asentaa ja päivittää"

    Release 2026.11:stä alkaen `repo upgrade` asentaa uuden repositorion ja päivittää olemassa olevan.
    `repo install` toimii edelleen saman komennon toisena nimenä.

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
- `--address` — Palvelimen isäntä tai IP (oletus `127.0.0.1`)
- `--port` — Palvelimen portti (oletus `8000`)

Kun palvelin on käynnissä, se tulostaa osoitteen, jota se kuuntelee:

```text
Server running on http://127.0.0.1:8082
```

!!! note "Palvelin varaa päätteen"

    `serve` toimii edustalla ja jatkaa, kunnes pysäytät sen näppäinyhdistelmällä ++ctrl+c++. Anna sen olla käynnissä, kun viimeistelet asennuksen; automaattisen käynnistyksen osalta katso [dignan suorittaminen Windows-palveluna](#running-digna-as-a-windows-service).

## Dashboardin konfigurointi {: #dashboard-configuration }

### Vaihe 1: Ota dashboard käyttöön verkkopalvelimella

digna-dashboard lukee oman konfiguraationsa tiedostosta `dashboard/dashboard_config.toml`. Tätä tiedostoa ei toimiteta asennuksen mukana — luot sen `dashboard/`-hakemistoon dashboardin tiedostojen rinnalle.

Sen sisältö on kuvattu kohdassa [Yhden kirjautumisen (SSO) yleiskatsaus](../../../sso/overview.md), jossa tiedostoa myös tarvitaan: se sisältää dashboardin tarjoamat kirjautumisvaihtoehdot ja monen instanssin käyttöönotoissa backend-yhteyden.

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

### `windows`-komennot

Palvelua hallitaan itse `digna`-suoritustiedostolla, `digna windows` -alikomentojen avulla.
Suoritettavia bat-tiedostoja ei ole.

| Komento | Tarkoitus |
|---|---|
| `digna windows install` | Rekisteröi dignan Windows-palveluksi |
| `digna windows start` | Käynnistää rekisteröidyn palvelun |
| `digna windows stop` | Pysäyttää käynnissä olevan palvelun |
| `digna windows uninstall` | Poistaa palvelun rekisteröinnin |

!!! warning "Ylläpitäjäoikeudet vaaditaan"

    Kaikki neljä komentoa on suoritettava järjestelmänvalvojana avatusta komentokehotteesta.

Jokainen komento hyväksyy valitsimen `--name`, jolla voidaan viitata muulla kuin oletusnimellä rekisteröityyn palveluun. Täydellinen
valitsinluettelo on [CLI-referenssissä](../../../cli/Command_Line_Interface_202611.md).

### Palvelun asentaminen

1. **Avaa komentokehote järjestelmänvalvojana**
   - Napsauta komentokehote oikealla painikkeella
   - Valitse "Run as Administrator"

2. **Siirry digna-asennushakemistoosi**
   ```bash
   cd C:\path\to\digna
   ```

3. **Rekisteröi palvelu**
   ```bash
   digna windows install
   ```

!!! important "Määritä osoite ja portti, elleivät oletusarvot sovi sinulle"

    `install` tallentaa osoitteen ja portin palvelun rekisteröintiin, ja palvelu sitoutuu
    täsmälleen tallennettuihin arvoihin. Oletusarvot ovat `127.0.0.1` ja `8000`, jotka hyväksyvät yhteyksiä
    vain koneelta itseltään. Toisella isännällä oleva dashboard ei tavoita sitä, joten anna
    osoite, jota backendin tulee kuunnella:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Näitä arvoja ei lueta tiedostosta `config.toml`. Jos haluat muuttaa niitä myöhemmin, poista palvelun rekisteröinti ja
    asenna palvelu uudelleen uusilla arvoilla.

Palvelu rekisteröidään **automaattisella käynnistyksellä**, joten se käynnistyy Windowsin mukana. Se ei
käynnisty välittömästi — katso seuraava osio.

#### Asennuksen valitsimet

| Valitsin | Oletus | Tarkoitus |
|---|---|---|
| `--name` | `digna` | Nimi, jolla palvelu rekisteröidään |
| `--display-name` | `digna` | services.msc-näkymässä näytettävä nimi |
| `--description` | `digna data quality backend` | services.msc-näkymässä näytettävä kuvaus |
| `--address` | `127.0.0.1` | Osoite, johon palvelu sitoo API:nsa |
| `--port` | `8000` | Portti, johon palvelu sitoo API:nsa |
| `--working-dir` | `digna`-suoritustiedoston hakemisto | Hakemisto, jossa `config.toml` ja `license.toml` sijaitsevat ja jonka palvelu asettaa työhakemistokseen |
| `--start-type` | `auto` | `auto` käynnistyy Windowsin mukana, `manual` käynnistyy vain pyydettäessä, `disabled` rekisteröi palvelun mutta estää sen käynnistämisen |
| `--account` | `LocalSystem` | Tili, jolla palvelu suoritetaan, esim. `DOMAIN\user` tai `.\user` |
| `--password` | | Tilin `--account` salasana |

!!! tip "Suorittaminen toimialuetilillä"

    `LocalSystem`-tilillä ei ole verkkoidentiteettiä, joten Windows-todennus SQL Serveriin ja kaikki
    verkkojakojen käyttö epäonnistuvat. Asenna valitsimilla `--account` ja `--password`, jos
    palvelun on käytettävä resursseja tiettynä käyttäjänä.

### Palvelun käynnistäminen ja pysäyttäminen

#### Palvelun käynnistäminen

```bash
digna windows start
```

#### Palvelun pysäyttäminen

```bash
digna windows stop
```

!!! tip "Vinkki"

    Pysäytä aina palvelu ennen sovellustiedostojen päivittämistä.

### Palvelun siirtäminen uuteen hakemistoon

Jos sinun on siirrettävä digna-asennus:

1. **Pysäytä nykyinen palvelu ja poista sen rekisteröinti**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Siirrä sovellustiedostot**
   - Siirrä koko digna-asennushakemisto uuteen sijaintiin

3. **Rekisteröi palvelu uudelleen uudesta sijainnista**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Toista kaikki valitsimien `--address`, `--port` ja `--account` arvot, joita käytit ensimmäisellä kerralla — aiempi
   rekisteröinti on poistettu.

4. **Käynnistä palvelu**
   ```bash
   digna windows start
   ```

### Palvelun poistaminen

1. **Pysäytä käynnissä oleva palvelu**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Poista palvelun rekisteröinti**
   ```bash
   digna windows uninstall
   ```

digna-palvelin on nyt poistettu Windows-palveluna rekisteristä.

---

## Päivitys uuteen julkaisuun {: #upgrading-to-a-new-release }

Tämä osio päivittää Release 2026.06 -asennuksen Release 2026.11 -versioon.

!!! warning "Päivitys 2026.06:ta vanhemmasta julkaisusta"

    Suorita ensin Release 2026.06:n päivitysvaiheet: [Päivitys uuteen julkaisuun](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Jatka sitten alla olevista vaiheista.

### Ennen päivitystä

**digna-repositorion varmuuskopiointi on pakollista**

Ennen dignan päivittämistä tee varmuuskopio repositoriostasi (PostgreSQL) suojautuaksesi datan menetykseltä. Varmuuskopio mahdollistaa toipumisen, jos päivityksessä ilmenee odottamattomia ongelmia.

**Lisenssitiedoston pyytäminen Release 2026.11:tä varten**

Release 2026.11 vaatii uuden `license.toml`-tiedoston. Pyydä se digna-tiimiltä ennen aloittamista ja
pidä se valmiina [vaihetta 7](#step-7-replace-the-license-file) varten.

### Päivitysprosessi

#### Vaihe 1: Pysäytä digna-palvelu {: #step-1-stop-the-digna-service }

Avaa komentokehote järjestelmänvalvojana ja pysäytä palvelu nykyisen asennuksesi
`digna`-suoritustiedostolla:

```bash
cd C:\path\to\digna
digna windows stop
```

Palvelu pysyy rekisteröitynä. Uusi suoritustiedosto korvaa vanhan samassa hakemistossa, joten
rekisteröinti osoittaa edelleen oikeaan tiedostoon.

Jos digna on käynnissä etualalla, paina ++ctrl+c++ sen komentokehoteikkunassa.

#### Vaihe 2: Varmuuskopioi nykyinen asennus {: #step-2-backup-current-installation }

Nimeä digna-asennushakemistossa nykyisen asennuksen suoritettava tiedosto ja dashboard-kansio uudelleen,
jotta uusi julkaisu voidaan ottaa käyttöön niiden rinnalle:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Säilytä `digna_old.exe`, kunnes olet varmistanut päivityksen, ja `dashboard_old`, kunnes olet palauttanut
siitä konfiguraatiotiedostosi (katso vaihe 4). Sen jälkeen voit poistaa molemmat.

#### Vaihe 3: Pura ja ota käyttöön uusi versio {: #step-3-extract-and-deploy-new-version }

1. Pura uusi digna-asennus ZIP-tiedosto
2. Kopioi uusi `digna`-suoritettava ja `dashboard`-kansio asennushakemistoosi

!!! warning "Tärkeää"

    Asennuksen ZIP-tiedostoon ei koskaan sisällytetä `config.toml`- eikä `dashboard/dashboard_config.toml`-tiedostoa
    — digna-tiimi ei koskaan toimita kumpaakaan tiedostoa. Päivitys ei siksi koske olemassa olevaan
    konfiguraatioosi, ja uudelleennimetyissä `*_old`-kansioissa olevat kopiot ovat ainoat, jotka sinulla on.

#### Vaihe 4: Palauta konfiguraatiotiedostosi {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
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
digna config check
```

Jokaisen osion on raportoitava OK. Korjaa kaikki, mikä raportoidaan tilassa FAILED, poista kohdan
**Unknown keys** alla luetellut avaimet ja suorita komento uudelleen ennen jatkamista.

#### Vaihe 7: Vaihda lisenssitiedosto {: #step-7-replace-the-license-file }

Aiempaa julkaisua varten myönnetty lisenssitiedosto ei toimi Release 2026.11:n kanssa. Kopioi
digna-tiimin Release 2026.11:tä varten toimittama `license.toml` asennushakemistoon vanhan tiedoston
tilalle:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Älä säilytä edellistä lisenssiä"

    Edellisellä lisenssillä jokainen komento, joka tarkistaa lisenssin — `serve`, `user`,
    `inspection`, `repo` — epäonnistuu, joten digna ei käynnisty eikä repositoriota voi päivittää.
    Tarkista uusi lisenssi ennen kuin jatkat:

    ```bash
    digna license check
    ```

#### Vaihe 8: Päivitä repositorion skeema {: #step-8-upgrade-the-repository-schema }

Suorita dignan asennushakemistossa:

```bash
digna repo upgrade
```

Release 2026.11 hallitsee repositorion skeemaa versioitujen migraatioiden avulla. Ensimmäinen päivitys
aiemmasta julkaisusta tuo skeeman edellisen järjestelmän viimeiseen versioon, kirjaa sen
lähtökohdakseen ja soveltaa sitten Release 2026.11:n migraatiot. Se päättyy ilmoituksiin:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Kaikki olemassa olevat tiedot säilyvät. Näet repositorion tilan milloin tahansa komennolla
`digna repo check`: se luettelee viimeisimmän sovelletun migraation ja mahdolliset odottavat migraatiot.

!!! warning "digna ei käynnisty vanhentuneella repositoriolla"

    Release 2026.11:stä alkaen palvelin kieltäytyy käynnistymästä niin kauan kuin repositorio vaatii päivityksen, ja
    ilmoittaa siitä, esimerkiksi:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Suorita `repo upgrade` ennen kuin käynnistät palvelimen tai palvelun.

#### Vaihe 9: Käynnistä palvelut uudelleen {: #step-9-restart-services }

Jos digna toimii Windows-palveluna, käynnistä se uudelleen:

```bash
cd C:\path\to\digna
digna windows start
```

Jos ajat palvelinta manuaalisesti, käynnistä se uudelleen:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jos käytät IIS:ää tai Tomcatia, käynnistä vastaava verkkopalvelin uudelleen.

#### Vaihe 10: Vahvista päivitys {: #step-10-verify-the-upgrade }

1. Vahvista uuden suoritettavan tiedoston julkaisu:

    ```bash
    digna version
    ```

    Ensimmäisen rivin on oltava `Release: 2026.11`.

2. Avaa digna-dashboard ja varmista, että käyttöliittymä latautuu oikein.
3. Tarkista asennuksen `logs`-hakemiston tiedostot virheiden varalta.
4. Testaa tietokantayhteytesi — katso
   [Yhteyden testaaminen](../../../databases/overview.md#testing-a-connection).

Uusien moduulien käytön aloittamiseen katso [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[AI-agentin yhdistäminen](../../../platform/agentic/connect_ai_agent.md) digna MCP Serveriä varten ja
[Profilointisijainti](../../../platform/profiling/profiling_location.md) digna Engineä varten.
