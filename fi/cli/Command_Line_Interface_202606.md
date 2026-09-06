# digna CLI -referenssi 2026.06
**2026-09-05**

Tämä sivu dokumentoi kaikki komennot, jotka ovat käytettävissä ***digna*** CLI -julkaisussa **2026.06**, mukaan lukien käyttöesimerkit ja valitsimet.

Suoritettavan tiedoston nimi on `digna`.

---

## CLI:n perusteet

---

### Yleiskatsaus ja syntaksi

Julkaisun **2026.06** CLI käyttää jäsenneltyä, luokkiin perustuvaa komentohierarkiaa:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` ja `serve` ovat yksittäisiä komentoja ilman alikomentoa:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Yleiset valitsimet

Seuraavat yleiset valitsimet koskevat kaikkia komentoja:

- `--help`, `-h`: Näyttää ohjetiedot CLI:stä tai tietystä komentoluokasta tai alikomennosta.
- `--stacktrace`: Näyttää virhetilanteessa koko virheketjun pelkän ylimmän tason viestin sijaan.

`--stacktrace` on yleinen valitsin varsinaisessa merkityksessä: se on annettava **ennen** komentoluokkaa, ei sen jälkeen.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

`--version`-lippua ei ole. Käytä sen sijaan komentoa [`version`](#version).

### Edellytykset

Useimmat komennot tarvitsevat luettavan ja kelvollisen `config.toml`-tiedoston; jotkin vaativat lisäksi voimassa olevan lisenssin.
Seuraava taulukko kertoo, mitä kukin komentoluokka lataa ennen kuin se tekee mitään:

| Komentoluokka | Tarvitsee `config.toml`-tiedoston | Tarvitsee voimassa olevan lisenssin |
|---|---|---|
| `version` | ei | ei |
| `config check` | ei (se on juuri se, mistä komento raportoi) | ei |
| `license check` | ei | se *on* itse tarkistus |
| `crypt` | kyllä | ei |
| `serve` | kyllä | ei |
| `project` | kyllä | ei |
| `user` | kyllä | kyllä |
| `inspection` | kyllä | kyllä |
| `repo` | kyllä | kyllä |

Kun lisenssi vaaditaan, tarkistetaan sekä sen allekirjoitus että voimassaolon päättymispäivä, ja komento keskeytyy ennen tietovaraston koskettamista, jos jompikumpi epäonnistuu.

### Paluukoodit

- `0`: komento onnistui.
- `1`: komento epäonnistui. Virheilmoitus kirjoitetaan stderr-virtaan etuliitteellä `Error: `.

### help

Valitsin `--help` antaa tietoa käytettävissä olevista komentoluokista, alikomennoista ja valitsimista:

1. **Yleisen ohjeen näyttäminen:**
   ```bash
   digna --help
   ```

2. **Ohjeen hakeminen tietyille luokille ja komennoille:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Tuloste sisältää:**
   - **Komennon kuvauksen:** Yhteenvedon komennon tarkoituksesta.
   - **Syntaksin:** Pakolliset ja valinnaiset argumentit.
   - **Valitsimet:** Komennolle ominaiset liput ja parametrit.

### version

Komento `version` tulostaa asennetun ***digna***-julkaisun. Se ei lue mitään asetuksia eikä vahvista lisenssiä, joten se toimii myös asennuksessa, jonka `config.toml` tai lisenssi puuttuu tai on virheellinen.

Julkaisun versio on riippumaton tietovaraston skeeman versiosta, jonka [`repo check`](#repo-check) raportoi.

#### Komennon käyttö
```bash
digna version
```

#### Esimerkkituloste
```text
2026.06
```

---

## Asetusten hallinta

---

### config check

Komento `config check` vahvistaa asetustiedoston (`config.toml`) tarkistamalla, että kaikki pakolliset osiot ja asetukset ovat olemassa ja oikein muotoiltuja. Kukin osio vahvistetaan erikseen, joten rikkinäinen `[app]`-osio ei peitä `[repo]`-osion tilaa.

Raportoitavat osiot ovat:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — valinnainen; puuttuva avain läpäisee tarkistuksen, mutta olemassa oleva mutta virheellisesti muotoiltu luettelo epäonnistuu

Komento ei tarkoituksella lataa sovelluksen asetuksia samalla tavalla kuin muut komennot, jotta se voi diagnosoida `config.toml`-tiedoston, joka estäisi ***digna***-ohjelmistoa käynnistymästä lainkaan.

#### Komennon käyttö
```bash
digna config check [OPTIONS]
```

#### Valitsimet
- `--configpath`, `-c`: Polku asetustiedostoon tai hakemistoon, joka sisältää `config.toml`-tiedoston (oletus `./config.toml`).
- `--json`: Tulostaa vahvistusraportin JSON-muodossa. Ohittaa valitsimen `--quiet`.
- `--quiet`, `-q`: Piilottaa raportin ja luottaa yksinomaan paluukoodiin.

#### Esimerkki
```bash
digna config check
```

Tietyn asetustiedoston vahvistaminen ja tulosteen muotoilu JSON-muotoon:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Esimerkkituloste
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Puuttuva tiedosto tai TOML-syntaksivirhe ei jätä mitään osioittain vahvistettavaa, ja siitä raportoidaan yhtenä virheenä raportin sijaan riippumatta valitsimista `--quiet` tai `--json`.

---

## Tietovaraston hallinta

---

### repo check

Komento `repo check` testaa tietokantayhteyden ja varmistaa tietovaraston asennuksen ja version. Se epäonnistuu, jos määritettyä skeemaa ei ole olemassa tai jos se on olemassa mutta ei sisällä ***digna***-tietovarastoa.

Raportoitava versio on tietovaraston skeeman versio, jonka versiointi on erillinen [`version`](#version)-komennon tulostamasta ***digna***-julkaisusta.

#### Komennon käyttö
```bash
digna repo check
```

#### Esimerkkituloste
```text
Repo version 3.0.0 installed
```

### repo install

Komento `repo install` asentaa uuden ***digna***-tietovaraston `config.toml`-tiedostossa määritettyyn skeemaan luoden kaikki tarvittavat sekvenssit, taulut, indeksit, rajoitteet ja alkutietueet.

Tämä komento **ei** luo itse skeemaa — sen on oltava olemassa etukäteen. Komento myös kieltäytyy suorittumasta, jos kyseiseen skeemaan on jo asennettu tietovarasto, ja ohjaa komentoon [`repo upgrade`](#repo-upgrade), jos asennettu versio on vanhempi.

#### Komennon käyttö
```bash
digna repo install
```

#### Esimerkkituloste
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Komento `repo upgrade` soveltaa tietokantaskeeman migraatioita nostaakseen olemassa olevan tietovaraston versioon, jota asennettu julkaisu odottaa. Päivitykset sovelletaan yksi versioaskel kerrallaan kiinteää päivityspolkua pitkin, ja jokainen valmistunut askel kirjataan tietovarastoon.

Jos tietovarasto on jo odotetussa versiossa, komento ilmoittaa, ettei päivitystä tarvita, eikä tee muutoksia.

#### Komennon käyttö
```bash
digna repo upgrade
```

#### Esimerkkituloste
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Salauksen hallinta

---

### crypt gen-key

Komento `crypt gen-key` luo uuden AES-GCM-salausavaimen käytettäväksi salausavaimena `config.toml`-tiedostossa. Ladattavan `config.toml`-tiedoston on oltava jo olemassa, vaikka luotu avain ei riipu siitä.

#### Komennon käyttö
```bash
digna crypt gen-key
```

#### Esimerkkituloste
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Komento `crypt encrypt` salaa merkkijonon (kuten tietokannan salasanan) `config.toml`-tiedostossa määritetyllä AES-GCM-avaimella ja tulostaa salatun tekstin.

#### Komennon käyttö
```bash
digna crypt encrypt <VALUE>
```

#### Argumentit
- **VALUE**: Salattava selkokielinen merkkijono (pakollinen).

#### Esimerkki
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Komento `crypt decrypt` purkaa AES-GCM-salatun merkkijonon `config.toml`-tiedostossa määritetyllä avaimella ja tulostaa selkokielisen tekstin.

#### Komennon käyttö
```bash
digna crypt decrypt <VALUE>
```

#### Argumentit
- **VALUE**: Purettava salattu merkkijono (pakollinen).

#### Esimerkki
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Käyttäjien hallinta

---

### user add

Komento `user add` luo uuden käyttäjätilin ***digna***-tietovarastoon. Komento epäonnistuu, jos annetulla sähköpostiosoitteella on jo käyttäjä.

#### Komennon käyttö
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentit
- **EMAIL**: Käyttäjän sähköpostiosoite (pakollinen).
- **PASSWORD**: Käyttäjän alkuperäinen salasana (pakollinen).
- **DISPLAY_NAME**: Käyttäjän täydellinen näyttönimi (pakollinen).

#### Valitsimet
- `--admin`, `-a`: Luo käyttäjän pääkäyttäjän (superuser) oikeuksin.

#### Esimerkki
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Pääkäyttäjätilin luominen:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Esimerkkituloste
```text
User created with ID: 42
```

### user list

Komento `user list` luettelee kaikki rekisteröidyt käyttäjät taulukkomuodossa tunnisteen, sähköpostiosoitteen, näyttönimen ja pääkäyttäjälipun kera.

#### Komennon käyttö
```bash
digna user list
```

#### Esimerkkituloste
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Komento `user modify` päivittää olemassa olevan, sähköpostiosoitteella yksilöidyn käyttäjätilin näyttönimen ja pääkäyttäjäoikeudet.

Sekä näyttönimi että pääkäyttäjälippu kirjoitetaan aina. `--admin` on kytkin, ei arvo: **sen pois jättäminen poistaa pääkäyttäjäoikeudet**, joten anna se aina, kun käyttäjän on säilytettävä ne tai saatava ne.

#### Komennon käyttö
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentit
- **EMAIL**: Muokattavan käyttäjän sähköpostiosoite (pakollinen).
- **DISPLAY_NAME**: Päivitetty näyttönimi (pakollinen).

#### Valitsimet
- `--admin`, `-a`: Myöntää pääkäyttäjäoikeudet. Jätä pois poistaaksesi ne.
- `--valid-until`, `-v`: Hyväksytään yhteensopivuuden vuoksi, mutta **sitä ei tällä hetkellä sovelleta**. Sen antaminen tulostaa varoituksen eikä muuta mitään.

#### Esimerkki
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Esimerkkituloste
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Komento `user modify-pwd` päivittää olemassa olevan käyttäjätilin salasanan.

#### Komennon käyttö
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumentit
- **EMAIL**: Sen käyttäjän sähköpostiosoite, jonka salasana päivitetään (pakollinen).
- **PASSWORD**: Uusi salasana (pakollinen).

#### Esimerkki
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Komento `user delete` poistaa käyttäjätilin järjestelmästä.

#### Komennon käyttö
```bash
digna user delete <EMAIL>
```

#### Argumentit
- **EMAIL**: Poistettavan käyttäjän sähköpostiosoite (pakollinen).

#### Esimerkki
```bash
digna user delete jdoe@example.com
```

---

## Projektien ja tietolähteiden hallinta

---

### project list

Komento `project list` luettelee kaikki tietovarastossa saatavilla olevat projektit näyttäen niiden tunnisteen, nimen ja kuvauksen.

#### Komennon käyttö
```bash
digna project list
```

#### Esimerkkituloste
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Komento `project list-ds` luettelee kaikki tiettyyn projektiin liitetyt tietolähteet näyttäen niiden tunnisteen, nimen, tyypin, skeeman ja taulun nimen.

#### Komennon käyttö
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumentit
- **PROJECT_NAME**: Sen projektin nimi, jonka tietolähteet luetellaan (pakollinen). Nimen on täsmättävä täsmälleen.

#### Esimerkki
```bash
digna project list-ds ProjectA
```

#### Esimerkkituloste
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Komento `project export-ds` vie projektin tietolähteet JSON-dokumenttiin.

Jos kumpaakaan valitsinta `--table-name` tai `--table-id` ei anneta, viedään kaikki projektin tietolähteet.

#### Komennon käyttö
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumentit
- **PROJECT_NAME**: Sen projektin nimi, josta tietolähteet viedään (pakollinen).

#### Valitsimet
- `--table-name`, `-n`: Vietävien tietolähteiden nimet. Useita nimiä voi antaa välilyönnein eroteltuina.
- `--table-id`, `-i`: Vietävien tietolähteiden tunnisteet. Useita tunnisteita voi antaa välilyönnein eroteltuina.
- `--exportfile`, `-f`: Polku, johon viedyt tietolähteet tallennetaan (oletus: `data_sources_export.json`).

#### Esimerkki
Kaikkien tietolähteiden vieminen projektista `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Tiettyjen taulujen vieminen:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Esimerkkituloste
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Komento `project import-ds` tuo tietolähteet vientitiedostosta kohdeprojektiin ja raportoi objektikohtaisesti, mitä luotiin, päivitettiin tai ohitettiin.

#### Komennon käyttö
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentit
- **PROJECT_NAME**: Kohdeprojektin nimi, johon tuodaan (pakollinen).
- **EXPORT_FILE**: Polku JSON-vientitiedostoon (pakollinen).

#### Valitsimet
- `--output-file`, `-o`: Tiedosto, johon tuontiraportti kirjoitetaan. Ilman sitä raportti menee stdout-virtaan.
- `--output-format`, `-f`: Tuontiraportin muoto — `table`, `json` tai `csv` (oletus: `table`).

#### Esimerkki
```bash
digna project import-ds ProjectB my_export.json
```

Koneluettavan raportin tallentaminen:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Raportti kattaa neljä objektitasoa — tietolähde, tietojoukon määrittely, attribuutti ja validointisääntö — kunkin osalta tuontitoimenpiteen, tuloksen, syntyneen objektin tunnisteen ja mahdolliset lisätiedot.

### project plan-import-ds

Komento `project plan-import-ds` esikatselee tietolähteiden tuontia kohdeprojektiin näyttäen, mitkä objektit luotaisiin, päivitettäisiin tai ohitettaisiin, muuttamatta mitään. Se ottaa saman vientitiedoston ja samat raportointivalitsimet kuin [`project import-ds`](#project-import-ds) ja lisää askelnumeron kutakin suunniteltua objektia kohti.

#### Komennon käyttö
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentit
- **PROJECT_NAME**: Kohdeprojektin nimi (pakollinen).
- **EXPORT_FILE**: Polku vientitiedostoon (pakollinen).

#### Valitsimet
- `--output-file`, `-o`: Tiedosto, johon tuontisuunnitelma kirjoitetaan. Ilman sitä suunnitelma menee stdout-virtaan.
- `--output-format`, `-f`: Tuontisuunnitelman muoto — `table`, `json` tai `csv` (oletus: `table`).

#### Esimerkki
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Tarkastusten hallinta

---

### inspection run

Komento `inspection run` luo tarkastuspyynnön projektille ja päivämääräväliä varten ja — annettujen valitsimien mukaan — joko odottaa sitä, palaa välittömästi tai suorittaa sen omassa prosessissaan.

Kolme suoritustilaa ovat:

- **Oletus (ei lippua)**: pyyntö asetetaan taustajärjestelmän jonoon, ja CLI kysyy sen tilaa kahden sekunnin välein tulostaen tehtävien edistymisen, kunnes tarkastus saavuttaa lopputilan. Käynnissä oleva `digna serve` vaaditaan, muuten kukaan ei poimi pyyntöä.
- **`--async-mode`**: pyyntö asetetaan jonoon ja sen tunniste tulostetaan välittömästi. Seuraa sitä komennolla [`inspection status`](#inspection-status).
- **`--bypass-backend`**: tarkastuksen suorittaa CLI-prosessi itse eikä sitä aseteta jonoon, joten käynnissä olevaa palvelinta ei tarvita.

`--async-mode` ja `--bypass-backend` sulkevat toisensa pois.

Kaikissa tiloissa komento päättyy nollasta poikkeavaan paluukoodiin, jos tarkastus ei valmistunut onnistuneesti.

#### Komennon käyttö
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumentit
- **PROJECT_NAME**: Kohdeprojektin nimi (pakollinen). Nimen on täsmättävä täsmälleen.
- **START_DATE**: Päivämäärävälin alkupäivä muodossa `YYYY-MM-DD` (pakollinen).
- **END_DATE**: Päivämäärävälin loppupäivä muodossa `YYYY-MM-DD` (pakollinen).

#### Valitsimet
- `--table-name`: Rajaa tarkastuksen projektin yhteen tietolähteeseen, joka annetaan tietolähteen nimellä. Ilman sitä tarkastetaan kaikki projektin tietolähteet.
- `--async-mode`: Asettaa tarkastuksen jonoon ja tulostaa pyynnön tunnisteen sen sijaan, että odottaisi sitä. Ei voi yhdistää valitsimeen `--bypass-backend`.
- `--bypass-backend`: Suorittaa tarkastuksen suoraan CLI-prosessissa sen sijaan, että asettaisi sen taustajärjestelmän jonoon. Ei voi yhdistää valitsimeen `--async-mode`.

#### Esimerkki
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Asynkronisen tarkastuksen lähettäminen:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Yhden tietolähteen tarkastaminen:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Esimerkkituloste
Oletustila:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynkroninen tila:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Komento `inspection status` kysyy tarkastuspyynnön tilaa ja tehtävien edistymistä pyynnön tunnisteen perusteella.

#### Komennon käyttö
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumentit
- **INSPECTION_REQUEST_ID**: Tarkastuspyynnön numeerinen tunniste (pakollinen).

#### Esimerkki
```bash
digna inspection status 1024
```

#### Esimerkkituloste
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Komento `inspection abort` pyytää käynnissä olevien tai odottavien tarkastuspyyntöjen peruuttamista. Se kirjaa pysäytystapahtuman jokaiselle kyseessä olevalle pyynnölle; taustajärjestelmä toimii sen perusteella, joten keskeytys on pysäytyspyyntö eikä välitön lopetus.

#### Komennon käyttö
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumentit
- **INSPECTION_REQUEST_ID**: Keskeytettävän tarkastuspyynnön tunniste. Pakollinen, ellei valitsinta `--killall` anneta.

#### Valitsimet
- `--killall`: Keskeyttää kaikki parhaillaan käynnissä olevat ja odottavat tarkastuspyynnöt. Ohittaa samalla annetun pyyntötunnisteen.

#### Esimerkki
Tietyn pyynnön keskeyttäminen:
```bash
digna inspection abort 1024
```

Kaikkien aktiivisten ja jonossa olevien tarkastusten keskeyttäminen:
```bash
digna inspection abort --killall
```

#### Esimerkkituloste
`--killall` raportoi, mitä se teki; yksittäisen pyynnön keskeyttäminen ei tuota tulostetta ja ilmoittaa onnistumisesta paluukoodillaan.
```text
All running and pending inspections have been aborted.
```

---

## Lisenssien hallinta

---

### license check

Komento `license check` vahvistaa `license.toml`-tiedoston tarkistamalla sen allekirjoituksen asennuksen mukana toimitettua julkista avainta vasten ja varmistamalla, ettei se ole vanhentunut. Se ei lue sovelluksen asetuksia, joten se toimii myös ennen kuin `config.toml` on määritetty.

#### Komennon käyttö
```bash
digna license check
```

#### Esimerkkituloste
```text
License is valid
```

Virheellisestä allekirjoituksesta ja vanhentuneesta lisenssistä raportoidaan erillisinä virheinä, molemmista paluukoodilla 1.

---

## Palvelin- ja taustapalvelut

---

### serve

Komento `serve` käynnistää ***digna***-REST-API-palvelimen sekä taustalla toimivan tarkastusten ajastimen ja tarkastusten hallinnan. Käynnistyessään se myös merkitsee epäonnistuneeksi jokaisen tarkastuksen, jonka tietovarasto edelleen kirjaa käynnissä olevaksi, koska mikään ei ole voinut säilyä aiemmasta prosessista.

Komento toimii edustalla, kunnes se pysäytetään.

#### Komennon käyttö
```bash
digna serve [OPTIONS]
```

#### Valitsimet
- `--address`: Verkko-osoite, johon API-palvelin sidotaan (oletus: `127.0.0.1`).
- `--port`: Portin numero, jota kuunnellaan (oletus: `8000`).

#### Esimerkki
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Esimerkkituloste
```text
Server running on http://0.0.0.0:8000
```