# digna CLI Reference 2025.04
**2025-04-01**

Tällä sivulla on dokumentoituna kaikki ***digna*** CLI -julkaisun **2025.04** käytettävissä olevat komennot, sisältäen esimerkit ja asetukset.

---

## CLI:n perusteet

---

## `help`-vaihtoehdon käyttö

`--help`-vaihtoehto antaa tietoa käytettävissä olevista komennoista ja niiden käytöstä. Tätä vaihtoehtoa voi käyttää kahdella pääasiallisella tavalla:

1. **Yleisen ohjeen näyttäminen:**
   
   Käytä --help-vaihtoehtoa heti komentorivin `dignacli`-avaimen jälkeen:
   ```bash
   dignacli --help
   ```

2. **Ohje tietylle komennolle:**  
  
   Jos haluat yksityiskohtaisempaa tietoa tietystä komennosta, lisää kyseisen komennon perään `--help`.  
   Esimerkiksi, saadaksesi ohjeet `add-user`-komennosta, suorita:
   ```bash
   dignacli add-user --help
   ```

   ### Tuloste:
      
   - **Komenton kuvaus:** Kuvaa yksityiskohtaisesti, mitä komento tekee.  
   - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien pakolliset ja valinnaiset argumentit.  
   - **Asetukset (Options):** Listaa komennolle spesifit asetukset ja niiden selitykset.  
   - **Esimerkit:** Antaa esimerkkejä komennon käytöstä.

  
## `check-repo-connection`-komennon käyttö

check-repo-connection on apuohjelma ***digna*** CLI -työkalussa, jolla testataan yhteyttä ja pääsyä määriteltyyn ***digna***-repositorioon. Komento varmistaa, että CLI voi kommunikoida repositorion kanssa.
      
#### Komennon käyttö
```bash
dignacli check-repo-connection
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tiedot repositoriosta: Repository version, Host, Database ja Schema.  
  
Jos repositorioon yhdistäminen epäonnistuu, tarkista config.toml-tiedosto ja varmista asetusten oikeellisuus.

## `version`-komennon käyttö

Tarkista asennettu *dignacli*-versio käyttämällä --version-vaihtoehtoa.  
  
#### Komennon käyttö
```bash
dignacli --version
```
  
#### Esimerkkituloste
```bash
dignacli version 2025.04
```

## Lokitusasetusten käyttö
  
Oletuksena ***digna***-komentojen konsolitulosteet ovat vähäeleisiä. Useimmat komennot tarjoavat mahdollisuuden lisätä tulostuksen määrää seuraavilla vaihtoehdoilla:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” ja ”debug” määrittävät yksityiskohtaisuuden tason, kun taas ”logfile” antaa mahdollisuuden ohjata tulostuksen tiedostoon konsolin sijaan.

## Käyttäjien hallinta

### `add-user`-komennon käyttö
  
add-user-komentoa käytetään uuden käyttäjän lisäämiseen ***digna***-järjestelmään.
  
#### Komennon käyttö
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentit

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

#### Asetukset

- `--is_superuser`, `-su`: Lipuke, jolla uusi käyttäjä merkitään ylläpitäjäksi.
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivämäärän muodossa `YYYY-MM-DD HH:MI:SS`. Jos tätä ei aseteta, tilillä ei ole vanhenemispäivää.

#### Esimerkki

Lisätään uusi käyttäjä käyttäjätunnuksella `jdoe`, koko nimellä `John Doe` ja salasanalla `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lisätäksesi uuden käyttäjän ja asettaaksesi tilin vanhenemispäivän:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### `delete-user`-komennon käyttö
  
`delete-user`-komennolla poistetaan olemassa oleva käyttäjä ***digna***-järjestelmästä.
  
#### Komennon käyttö
```bash
dignacli delete-user USER_NAME
```
  
##### Argumentit
- **USER_NAME**: Poistettavan käyttäjän käyttäjätunnus (pakollinen). Tämä on ainoa komennon vaatima argumentti.

#### Esimerkki
```bash
dignacli delete-user jdoe
```
  
Komennon suorittaminen poistaa käyttäjän `jdoe` ***digna***-järjestelmästä, peruuttaa hänen oikeutensa ja poistaa siihen liittyvät tiedot ja käyttöoikeudet repositoriosta.

### `modify-user`-komennon käyttö

`modify-user`-komennolla päivitetään olemassa olevan käyttäjän tiedot ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumentit
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Käyttäjän uusi koko nimi (pakollinen).
  
#### Asetukset  
  
- `--is_superuser`, `-su`: Asettaa käyttäjän superuseriksi, antaen laajennetut oikeudet. Tämä lipuke ei vaadi arvoa.  
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei anneta, tili pysyy voimassa toistaiseksi.  
  
#### Esimerkki
  
Muuta käyttäjän `jdoe` koko nimeksi “Johnathan Doe” ja aseta käyttäjä superuseriksi:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### `modify-user-pwd`-komennon käyttö
  
`modify-user-pwd`-komennolla vaihdetaan olemassa olevan käyttäjän salasana ***digna***-järjestelmässä.
  
#### Komennon käyttö
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentit
  
- **USER_NAME**: Salasanaa vaihtavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_PWD**: Uusi salasana (pakollinen).
  
#### Esimerkki
  
Vaihdetaan käyttäjän `jdoe` salasana muotoon `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### `list-users`-komennon käyttö

`list-users`-komento näyttää listan kaikista ***digna***-järjestelmään rekisteröidyistä käyttäjistä.

#### Komennon käyttö

```bash
dignacli list-users
```

Komento yhdistää ***digna***-repositorioon ja listaa kaikki käyttäjät, näyttäen heidän ID:nsä, käyttäjätunnuksensa, koko nimensä, superuser-tilan ja vanhenemisaikatunnisteet.

## Repositorion hallinta

### `upgrade-repo`-komennon käyttö
  
`upgrade-repo`-komennolla päivitetään tai alustetaan ***digna***-repositorio. Tämä komento on välttämätön päivitysten soveltamiseksi tai repositorion infrastruktuurin ensimmäistä kertaa luomiseksi.
  
#### Komennon käyttö

```bash
dignacli upgrade-repo [options]
```
  
#### Asetukset
  
- `--simulation-mode`, `-s`: Kun tämä on käytössä, komento ajetaan simulaatiotilassa; siinä tulostetaan SQL-lauseet, jotka suoritettaisiin, mutta niitä ei oikeasti ajeta. Tämä on hyödyllistä muutosten ennakkoarviointiin ilman, että repositoriota muutetaan.  

  
#### Esimerkki
  
Päivitä ***digna***-repositorio ajamalla komento ilman lisäasetuksia:
  
```bash
dignacli upgrade-repo
```  
Aja päivitys simulaatiotilassa (näet SQL-lauseet ilman niiden soveltamista):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tämä komento on keskeinen ***digna***-järjestelmän ylläpidossa, varmistaen että tietokantakaavio ja muut repositorion osat ovat ajan tasalla ohjelmiston uusimman version kanssa.

### `encrypt`-komennon käyttö
  
`encrypt`-komennolla voi salata salasanan.
  
#### Komennon käyttö
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentit
- **PASSWORD**: Salasana, joka halutaan salata (pakollinen).
  
#### Esimerkki
  
Salaaksesi salasanan, anna salasana argumenttina.  
Esimerkiksi salataksesi salasanan `mypassword123`, käytä:
```bash
dignacli encrypt mypassword123
```
Komentorivi tulostaa annetun salasanan salatun version, jota voidaan käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI ilmoittaa puuttuvasta argumentista.

## `generate-key`-komennon käyttö
  
`generate-key`-komennolla luodaan Fernet-avain, joka on olennainen salasanojen suojaamiseen ***digna***-repositoriossa.
  
#### Komennon käyttö
```bash
dignacli generate-key
```
  
## Datan hallinta

## `clean-up`-komennon käyttö

`clean-up`-komentoa käytetään poistamaan profiileja, ennusteita ja Traffic Light System -järjestelmän dataa yhdeltä tai useammalta datalähteeltä määritellyssä projektissa. Tämä komento on tärkeä datan elinkaaren hallinnassa, auttaen pitämään dataympäristön järjestettynä ja tehokkaana poistamalla vanhentunutta tai tarpeetonta tietoa.

#### Komennon käyttö

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, josta data poistetaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja soveltaa komentoa niihin.
- **FROM_DATE**: Datan poiston alkuajankohta. Hyväksyttäviä muotoja ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan poiston loppuajankohta, samaa muotoa noudattaen kuin FROM_DATE (pakollinen).
  
#### Asetukset
  
- `--table-name`, `-tn`: Rajaa clean-up-toiminnon koskemaan vain tiettyä taulua projektissa.
- `--table-filter`, `-tf`: Suodattaa niin, että puhdistus kohdistuu vain tauluihin, joiden nimissä on annettu osajono.
- `--timing`, `-tm`: Näyttää clean-up-prosessin keston suorituksen jälkeen.
- `--help`: Näyttää clean-up-komennon ohjeen ja poistuu.
  
#### Esimerkki
  
Poista data projektista ProjectA ajalta 1. tammikuuta 2023 – 30. kesäkuuta 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Poista data vain tietystä taulusta nimeltä `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tämä komento auttaa hallitsemaan tallennustilaa ja varmistamaan, että repositoriossa säilytetään vain oleellinen informaatio.

## `list-projects`-komennon käyttö
  
`list-projects`-komento näyttää listan kaikista saatavilla olevista projekteista ***digna***-järjestelmässä.
  
#### Komennon käyttö
  
```bash
dignacli list-projects
```

Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja; se tarjoaa nopean yleiskuvan repositorion saatavilla olevista projekteista.

## `list-ds`-komennon käyttö

`list-ds`-komento näyttää listan kaikista saatavilla olevista datalähteistä määritellyssä projektissa. Tämä komento on hyödyllinen datavarantojen kartoittamiseen analyysi- ja hallintatarkoituksiin ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, jonka datalähteet halutaan listata (pakollinen).
  
#### Esimerkki
  
Listaa kaikki datalähteet projektista nimeltä `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Komento antaa käyttäjille yleiskuvan projektin datalähteistä, helpottaen datanavigointia ja -hallintaa.


## `inspect`-komennon käyttö

`inspect`-komennolla luodaan profiileja, ennusteita ja Traffic Light System -dataa yhdelle tai useammalle datalähteelle määritellyssä projektissa. Tämä komento auttaa datan analysoinnissa ja seurannassa valitulta aikaväliltä.

#### Komennon käyttö

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastellaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja soveltaa komentoa niihin.
- **FROM_DATE**: Tarkastelun aloituspäivä ja -aika. Hyväksyttäviä muotoja ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastelun lopetuspäivä ja -aika, samaa muotoa noudattaen kuin FROM_DATE (pakollinen).
  
#### Asetukset

- `--table-name`, `-tn`: Rajaa tarkastelun tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa niin, että tarkastus kohdistuu vain tauluihin, joiden nimissä on annettu osajono.
- `--do-profile`: Käynnistää profiilien uudelleenkokoamisen. Oletuksena do-profile.
- `--no-do-profile`: Estää profiilien uudelleenkokoamisen.
- `--do-prediction`: Käynnistää ennusteiden uudelleenlaskennan. Oletuksena do-prediction.
- `--no-do-prediction`: Estää ennusteiden uudelleenlaskennan.
- `--do-alert-status`: Käynnistää hälytystilojen uudelleenlaskennan. Oletuksena do-alert-status.
- `--no-do-alert-status`: Estää hälytystilojen uudelleenlaskennan.
- `--iterative`: Suorittaa tarkastelun jaksottaisesti päivittäisin iteroinnin avulla. Oletuksena iterative.
- `--no-iterative`: Suorittaa tarkastelun koko ajanjaksolle kerralla.
- `--enable_notification`, `-en`: Sallii ilmoitusten lähettämisen hälytysten yhteydessä.
- `--timing`, `-tm`: Näyttää tarkasteluprosessin keston suorituksen jälkeen.
  
#### Esimerkki
  
Tarkasta projektin `ProjectA` data ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Tarkasta vain tietty taulu ja pakota ennusteiden uudelleenlaskenta:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden luomiseen, datan eheyden valvontaan ja hälytysjärjestelmien hallintaan määritellyllä aikavälillä.

## `tls-status`-komennon käyttö

`tls-status`-komennolla kysytään Traffic Light Systemin (TLS) tilaa tietylle taululle projektissa tietyllä päivämäärällä. Traffic Light System antaa näkymän datan terveydestä ja laadusta, osoittaen mahdolliset ongelmat tai hälytykset, jotka saattavat vaatia toimenpiteitä.
  
#### Komennon käyttö
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jolle TLS-tilaa kysytään (pakollinen).
- **TABLE_NAME**: Tietty taulu projektissa, jonka TLS-tila halutaan (pakollinen).
- **DATE**: Päivämäärä, jolle TLS-tila kysytään, yleensä muodossa %Y-%m-%d (pakollinen).
  
#### Esimerkki
  
Tarkista TLS-tila taululle UserData projektissa ProjectA päivänä 1. heinäkuuta 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Tämä komento auttaa käyttäjiä valvomaan ja ylläpitämään datan laatua tarjoamalla selkeän, käytännöllisen tilanneraportin ennalta määriteltyjen kriteerien perusteella.

## `inspect-async`-komennon käyttö

`inspect-async`-komennolla annetaan taustapalvelimelle tehtäväksi suorittaa tarkastus asynkronisesti yhdelle tai useammalle datalähteelle tietyssä projektissa. Jos projektiksi on asetettu all-projects, tarkastus käy läpi kaikki saatavilla olevat projektit. Komento palauttaa request-id:n, jota voidaan käyttää tarkastuksen etenemisen seuraamiseen.

#### Komennon käyttö

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastellaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja soveltaa komentoa niihin.
- **FROM_DATE**: Tarkastelun aloituspäivä ja -aika. Hyväksyttäviä muotoja ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastelun lopetuspäivä ja -aika, samaa muotoa noudattaen kuin FROM_DATE (pakollinen).
  
#### Asetukset

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa niin, että asynkroninen tarkastus koskee vain tauluja, joiden nimissä on annettu osajono.

  
#### Esimerkki
  
Tarkasta projektin `ProjectA` data asynkronisesti ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## `inspect-status`-komennon käyttö

`inspect-status`-komennolla tarkistetaan asynkronisen tarkastuksen eteneminen request-id:n perusteella.

#### Komennon käyttö

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama request-id.
  
#### Asetukset

- `--report_level`, `-rl`: Aseta raportin taso: 'task' tai 'step' [oletus: task]
  
#### Esimerkki
  
Tarkista tarkastuksen eteneminen request-id:llä 12345 yksityiskohtaisella step-tasolla:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## `export-ds`-komennon käyttö

`export-ds`-komennolla luodaan vienti datalähteistä ***digna***-repositoriosta. Oletuksena kaikki tietyn projektin datalähteet viedään.

#### Komennon käyttö
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, josta datalähteet viedään.

#### Asetukset

- `--table_name`, `-tn`: Vie tietyn datalähteen projektista.
- `--exportfile`, `-ef`: Määrittele vientitiedoston nimi.
    
#### Esimerkki
  
Vie kaikki datalähteet projektista `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tämä komento vie kaikki `ProjectA`-projektin datalähteet JSON-dokumentiksi, joka voidaan tuoda toiseen projektiin tai ***digna***-repositorioon.

## `import-ds`-komennon käyttö

`import-ds`-komennolla tuodaan datalähteitä kohdeprojektiin ja luodaan tuontiraportti.

#### Komennon käyttö
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon datalähteet tuodaan.
- **EXPORT_FILE**: Tuotavan vientitiedoston nimi.

#### Asetukset

- `--output-file`, `-o`: Tiedosto, johon import-raportti tallennetaan (jos ei määritetty, tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, johon import-raportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tuo kaikki datalähteet vientitiedostosta `my_export.json` projektiin `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Tuonnin jälkeen komento näyttää raportin tuoduista ja ohitetuista objekteista. Vain uudet datalähteet tuodaan `ProjectB`-projektiin. Selvittääksesi, mitkä objektit tulisi tuoda ja mitkä ohittaa, voit käyttää komentoa `plan-import-ds`.

## `plan-import-ds`-komennon käyttö

`plan-import-ds`-komennolla analysoidaan vientitiedosto ja luodaan suunnitelma siitä, mitä datalähteitä tuodaan kohdeprojektiin ja mitä ohitetaan.

#### Komennon käyttö
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon datalähteet mahdollisesti tuodaan.
- **EXPORT_FILE**: Analysoitavan vientitiedoston nimi.

#### Asetukset

- `--output-file`, `-o`: Tiedosto, johon import-suunnitelma tallennetaan (jos ei määritetty, tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, johon import-suunnitelma tallennetaan (json, csv).
    
#### Esimerkki
  
Tarkista, mitkä datalähteet tuodaan ja mitkä ohitetaan vientitiedostosta `my_export.json` tuotaessa projektiin `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tämä komento näyttää vain suunnitelman objekteista, jotka tuodaan ja jotka ohitetaan.