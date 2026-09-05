# digna CLI Reference 2026.01
**2026-01-15**

Tällä sivulla dokumentoidaan kaikki komennot, jotka ovat käytettävissä ***digna*** CLI -julkaisussa **2026.01**, sisältäen käyttöesimerkkejä ja valinnat.

---

## CLI:n perusteet

---

### help
`--help`-valinnolla saa tietoa saatavilla olevista komennoista ja niiden käytöstä. Tämän valinnan käyttämiseen on kaksi päätapaa:

1. **Yleisen ohjeen näyttäminen:**
   
    Käytä --help välittömästi avainsanan `dignacli` jälkeen.  
   ```bash
   dignacli --help
   ```

2. **Ohje tietylle komennolle:**  
  
    Saat yksityiskohtaiset tiedot tietystä komennosta lisäämällä `--help` kyseisen komennon perään.  
    Esimerkiksi saadaksesi ohjeet `add-user`-komentoon, suorita:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Komenton kuvaus:** Kuvaa yksityiskohtaisesti, mitä komento tekee.  
     - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien vaaditut ja valinnaiset argumentit.  
     - **Valinnat:** Listaa komennolle spesifit valinnat ja niiden selitykset.  
     - **Esimerkit:** Antaa esimerkkejä komennon tehokkaasta käytöstä.

### check-config

`check-config`-komento on työkalu ***digna*** CLI:ssa, joka testaa ***digna***-asetuksen oikeellisuutta. Tämä komento varmistaa, että ***digna***-komponentit löytävät tarvittavat konfiguraatioelementit tiedostosta config.toml.

#### Valinnat

- `--configpath`, `-cp`: Tiedosto tai hakemisto, joka sisältää konfiguraation. Jos valintaa ei anneta, käytetään ../config.toml:ia.
      
#### Komennon käyttö
```bash
dignacli check-config
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen konfiguraation täydellisyydestä.  
  
Jos konfiguraatio näyttää puutteelliselta, puuttuvat konfiguraatioelementit listataan.

  
### check-repo-connection

`check-repo-connection`-komento on työkalu ***digna*** CLI:ssa, jolla testataan yhteyttä ja pääsyä määritettyyn ***digna***-repositorioon. Tämä komento varmistaa, että CLI pystyy kommunikoimaan repositorion kanssa.
      
#### Komennon käyttö
```bash
dignacli check-repo-connection
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tietoja repositoriosta: Repository version, Host, Database ja Schema.  
  
Jos repositorioon muodostuva yhteys ei ole onnistunut, tarkista config.toml-tiedosto ja varmista asetusten oikeellisuus.


### version

Asennetun *dignacli*-version tarkistamiseksi käytä --version-valintaa.  
  
#### Komennon käyttö
```bash
dignacli --version
```
  
#### Esimerkkituloste
```bash
dignacli version 2026.01
```

### lokitusvalinnat
  
Oletuksena ***digna***-komentojen konsolitulostus on minimalistinen. Useimmissa komennoissa on kuitenkin mahdollisuus saada lisätietoa seuraavilla valinnoilla:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” ja ”debug” määrittävät yksityiskohtaisuustason, kun taas ”logfile”-kytkin mahdollistaa tulostuksen uudelleenohjauksen tiedostoon konsolin sijaan.

## Käyttäjien hallinta

### add-user
  
`add-user`-komennolla lisätään uusi käyttäjä ***digna***-järjestelmään.
  
#### Komennon käyttö
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentit

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

#### Valinnat

- `--is_superuser`, `-su`: Lipuke, jolla uusi käyttäjä asetetaan ylläpitäjäksi.
- `--valid_until`, `-vu`: Asettaa käyttäjätilille vanhenemispäivän muodossa `YYYY-MM-DD HH:MI:SS`. Jos tätä ei aseteta, tilillä ei ole vanhenemispäivää.

#### Esimerkki

Lisätäksesi uuden käyttäjän käyttäjätunnuksella `jdoe`, koko nimellä `John Doe` ja salasanalla `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lisätäksesi käyttäjän ja asettaaksesi tilille vanhenemispäivän:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user`-komennolla poistetaan olemassa oleva käyttäjä ***digna***-järjestelmästä.
  
#### Komennon käyttö
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentit
- **USER_NAME**: Poistettavan käyttäjän käyttäjätunnus (pakollinen). Tämä on ainoa komennolle vaadittava argumentti.

#### Esimerkki
```bash
dignacli delete-user jdoe
```
  
Komennon suorittaminen poistaa käyttäjän `jdoe` ***digna***-järjestelmästä, peruu hänen pääsynsä ja poistaa siihen liittyvät tiedot ja oikeudet repositoriosta.

### modify-user

`modify-user`-komennolla päivitetään olemassa olevan käyttäjän tiedot ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentit
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uusi koko nimi käyttäjälle (pakollinen).
  
#### Valinnat  
  
- `--is_superuser`, `-su`: Asettaa käyttäjän superkäyttäjäksi eli antaa korotetut oikeudet. Tämä lipuke ei tarvitse arvoa.  
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei anneta, tili pysyy voimassa toistaiseksi.  
  
#### Esimerkki
  
Muokataksesi käyttäjän `jdoe` koko nimeä muotoon “Johnathan Doe” ja asettaaksesi hänet superkäyttäjäksi:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd`-komennolla vaihdetaan olemassa olevan käyttäjän salasana ***digna***-järjestelmässä.
  
#### Komennon käyttö
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentit
  
- **USER_NAME**: Salasanan vaihtavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_PWD**: Uusi salasana käyttäjälle (pakollinen).
  
#### Esimerkki
  
Vaihtaaksesi käyttäjän `jdoe` salasanan muotoon `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users`-komento näyttää luettelon kaikista ***digna***-järjestelmään rekisteröidyistä käyttäjistä.

#### Komennon käyttö

```bash
dignacli list-users
```

Komennon suorittaminen muodostaa yhteyden ***digna***-repositorioihin ja listaa kaikki käyttäjät, näyttäen heidän ID:nsä, käyttäjätunnuksensa, koko nimensä, superkäyttäjätilan ja vanhenemisaikaleimat.

## Repositorion hallinta

### upgrade-repo
  
`upgrade-repo`-komennolla päivitetään tai alustetaan ***digna***-repositorio. Tämä komento on oleellinen päivitysten soveltamisessa tai repositorion infrastruktuurin ensimmäisessä käyttöönotossa.
  
#### Komennon käyttö

```bash
dignacli upgrade-repo [options]
```
  
#### Valinnat
  
- `--simulation-mode`, `-s`: Kun tämä valinta on käytössä, komento suorittaa simulaation: se tulostaa SQL-lauseet, jotka suoritettaisiin, mutta ei oikeasti suorita muutoksia. Tämä on hyödyllistä muutosten esikatseluun ilman repositorion muokkaamista.  

  
#### Esimerkki
  
Päivityksen suorittamiseksi ilman valintoja:
  
```bash
dignacli upgrade-repo
```  
Suorittaaksesi päivityksen simulaatiotilassa (nähdäkseen SQL-lauseet ilman soveltamista):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tämä komento on tärkeä ***digna***-järjestelmän ylläpidossa, varmistaen että tietokannan skeema ja muut repositorion komponentit ovat ajan tasalla ohjelmiston uusimman version kanssa.

### encrypt
  
`encrypt`-komennolla voi salata salasanan.
  
#### Komennon käyttö
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentit
- **PASSWORD**: Salasana, joka halutaan salata (pakollinen).
  
#### Esimerkki
  
Salataksesi salasanan, anna salasana argumenttina.  
Esimerkiksi salataksesi salasanan `mypassword123`, käytä:
```bash
dignacli encrypt mypassword123
```
Komento tulostaa annettuun salasanaan perustuvan salatun version, jota voi käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI näyttää virheilmoituksen puuttuvasta argumentista.

### generate-key
  
`generate-key`-komennolla luodaan Fernet-avain, joka on tarpeellinen salasanojen suojaamiseen ***digna***-repositoriossa.
  
#### Komennon käyttö
```bash
dignacli generate-key
```
  
## Datan hallinta

### clean-up

`clean-up`-komennolla poistetaan profiileja, ennusteita ja liikennevalojärjestelmän dataa yhdeltä tai useammalta datalähteeltä määritellyssä projektissa. Tämä komento on olennaisen tärkeä datan elinkaaren hallinnassa, auttaen pitämään ympäristön järjestettynä ja tehokkaana poistamalla vanhentunutta tai tarpeetonta tietoa.

#### Komennon käyttö

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, josta data poistetaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja suorittaa komennon niissä.
- **FROM_DATE**: Datan poistamisen aloituspäivämäärä ja -aika. Hyväksytyt muodot sisältävät %Y-%m-%d, %Y-%m-%dT%H:%M:%S, tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan poiston päättymispäivämäärä ja -aika, samaan tapaan kuin FROM_DATE (pakollinen).
  
#### Valinnat
  
- `--table-name`, `-tn`: Rajaa clean-up-operaation tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa, niin että puhdistus kohdistuu vain tauluihin, joiden nimessä on annettu alimerkkijono.
- `--timing`, `-tm`: Näyttää clean-up-prosessin keston suorituksen jälkeen.
- `--help`: Näyttää help-tiedot clean-up-komennolle ja poistuu.
  
#### Esimerkki
  
Poistaaksesi dataa projektista ProjectA ajalta 1. tammikuuta 2023 – 30. kesäkuuta 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Poistaaksesi dataa vain tietystä taulusta nimeltä `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tämä komento auttaa hallitsemaan tallennustilaa ja varmistamaan, että repositorio sisältää vain relevanttia tietoa.

### remove-orphans
  
`remove-orphans`-komento on tarkoitettu repositorion ylläpitoon.  
Kun käyttäjä poistaa projekteja tai datalähteitä, profiilit ja ennusteet voivat jäädä repositorioon. Tällä komennolla tällaiset orvoksi jääneet rivit poistetaan repositoriosta.
  
#### Komennon käyttö
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects`-komento näyttää luettelon kaikista saatavilla olevista projekteista ***digna***-järjestelmässä.
  
#### Komennon käyttö
  
```bash
dignacli list-projects
```

Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja, tarjoten nopean yleiskuvan repositorion saatavilla olevista projekteista.

### list-ds

`list-ds`-komento näyttää luettelon kaikista saatavilla olevista datalähteistä tietyssä projektissa. Tämä komento on hyödyllinen datavarantojen tunnistamiseen analyysi- ja hallintatyössä ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, jonka datalähteet listataan (pakollinen).
  
#### Esimerkki
  
Listataksesi kaikki datalähteet projektissa nimeltä `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tämä komento antaa yleiskuvan projektin käytettävissä olevista datalähteistä, auttaen navigoinnissa ja datan hallinnassa.


### inspect

`inspect`-komennolla luodaan profiileja, ennusteita ja liikennevalojärjestelmän dataa yhdelle tai useammalle datalähteelle määritellyssä projektissa. Tämä komento auttaa datan analysoinnissa ja monitoroinnissa määritellyn aikavälin sisällä. Tarkastuksen valmistuttua palautetaan laskettuun liikennevalojärjestelmään liittyvä arvo:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komennon käyttö

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastetaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja suorittaa komennon niissä.
- **FROM_DATE**: Tarkastuksen aloituspäivämäärä ja -aika. Hyväksytyt muodot sisältävät %Y-%m-%d, %Y-%m-%dT%H:%M:%S, tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastuksen päättymispäivämäärä ja -aika, samaan tapaan kuin FROM_DATE (pakollinen).
  
#### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa ja tarkastaa vain taulut, joiden nimissä esiintyy annettu alimerkkijono.
- `--enable_notification`, `-en`: Ottaa ilmoitusten lähettämisen käyttöön hälytystilanteissa.
- `--bypass-backend`, `-bb`: Ohittaa backendin ja suorittaa tarkastuksen suoraan CLI:stä (vain testikäyttöön!).

  
#### Esimerkki
  
Tarkastaaksesi ProjectA:n dataa 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Tarkastaaksesi vain tietyn taulun ja pakottaaksesi ennusteiden uudelleenlaskennan:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden luomisessa, datan eheyden seurannassa sekä hälytysjärjestelmien hallinnassa määritetyllä aikavälillä projektissa.

### inspect-async

`inspect-async`-komennolla luodaan profiileja, ennusteita ja liikennevalojärjestelmän dataa yhdelle tai useammalle datalähteelle määritellyssä projektissa. Tämä komento auttaa datan analysoinnissa ja monitoroinnissa määritellyn aikavälin sisällä. Toisin kuin `inspect`-komento, tämä ei odota tarkastuksen valmistumista. Sen sijaan se palauttaa lähetetylle tarkastuspyynnölle pyynnön ID:n. Tarkastuksen etenemisen kyselyyn käytä komentoa `inspect-status`.

#### Komennon käyttö

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastetaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja suorittaa komennon niissä.
- **FROM_DATE**: Tarkastuksen aloituspäivämäärä ja -aika. Hyväksytyt muodot sisältävät %Y-%m-%d, %Y-%m-%dT%H:%M:%S, tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastuksen päättymispäivämäärä ja -aika, samaan tapaan kuin FROM_DATE (pakollinen).
  
#### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa ja tarkastaa vain taulut, joiden nimissä esiintyy annettu alimerkkijono.
- `--enable_notification`, `-en`: Ottaa ilmoitusten lähettämisen käyttöön hälytystilanteissa.

  
#### Esimerkki
  
Tarkastaaksesi ProjectA:n dataa 1. tammikuuta 2024 – 31. tammikuuta 2024 asynkronisesti:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-komennolla tarkistat asynkronisen tarkastuksen etenemisen pyynnön ID:n perusteella.

#### Komennon käyttö

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama pyyntö-ID.
  
#### Esimerkki
  
Tarkistaaksesi tarkastuksen eteneminen, jos pyyntö-ID on 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-komennolla peruutetaan tarkastuksia pyynnön ID:n perusteella tai komennolla voi peruuttaa kaikki käynnissä olevat pyynnöt.

#### Komennon käyttö

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama pyyntö-ID.
  
#### Esimerkki
  
Peruaksesi tarkastuksen, jonka pyyntö-ID on 12345:
  
```bash
dignacli inspect-cancel 12345
```

Peruaksesi kaikki tällä hetkellä käynnissä tai jonossa olevat pyynnöt:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-komennolla luodaan eksportti datalähteistä ***digna***-repositoriosta. Oletuksena kaikki annetun projektin datalähteet viedään.

#### Komennon käyttö
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, josta datalähteet viedään.

#### Valinnat

- `--table_name`, `-tn`: Vie tietyn datalähteen projektista.
- `--exportfile`, `-ef`: Määrittää vientitiedoston nimen.
    
#### Esimerkki
  
Viedäksesi kaikki datalähteet projektista `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tämä komento vie `ProjectA`:n datalähteet JSON-dokumenttina, joka voidaan tuoda toiseen projektiin tai toiseen ***digna***-repositorioon.


### import-ds

`import-ds`-komennolla tuodaan datalähteitä kohdeprojektiin ja luodaan tuontiraportti.

#### Komennon käyttö
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon datalähteet tuodaan.
- **EXPORT_FILE**: Tuontiin käytettävän export-tiedoston nimi.

#### Valinnat

- `--output-file`, `-o`: Tiedosto, johon tallennetaan tuontiraportti (jos tätä ei ole määritetty, raportti tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, jossa tuontiraportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tuodaksesi kaikki datalähteet tiedostosta `my_export.json` projektiin `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Tuonnin jälkeen komento näyttää myös raportin tuoduista ja ohitetuista objekteista. Vain uudet datalähteet tuodaan `ProjectB`:hen. Selvittääksesi, mitkä objektit tuodaan ja mitkä ohitetaan, voit käyttää komentoa `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-komento näyttää ennakon siitä, mitä datalähteitä tuonti toisi kohdeprojektiin ja laatii tuontisuunnitelman.

#### Komennon käyttö
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon datalähteet mahdollisesti tuodaan.
- **EXPORT_FILE**: Export-tiedoston nimi, joka analysoidaan ennen tuontia.

#### Valinnat

- `--output-file`, `-o`: Tiedosto, johon tallennetaan tuontiraportti (jos tätä ei ole määritetty, raportti tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, jossa tuontiraportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tarkistaaksesi, mitkä datalähteet tuodaan ja mitkä ohitetaan tiedostosta `my_export.json` tuotaessa projektiin `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tämä komento näyttää vain suunnitelman objekteista, jotka tuodaan ja jotka ohitetaan.