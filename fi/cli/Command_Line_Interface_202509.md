# digna CLI Reference 2025.09
**2025-09-29**

Tällä sivulla on dokumentoitu kaikki ***digna*** CLI -version **2025.09** komennot, mukaan lukien käyttöesimerkit ja valinnat.

---

## CLI:n perusteet

---

### help
`--help`-valinta antaa tietoa saatavilla olevista komennoista ja niiden käytöstä. On kaksi päätapaa käyttää tätä valintaa:

1. **Yleisen ohjeen näyttäminen:**
   
    Käytä `--help` heti komennon `dignacli` jälkeen:  
   ```bash
   dignacli --help
   ```

2. **Ohje tietylle komennolle:**  
  
    Saat yksityiskohtaiset tiedot tietystä komennosta lisäämällä `--help` kyseisen komennon perään.  
    Esimerkiksi saadaksesi ohjeen `add-user`-komennosta, suorita:
     ```bash
     dignacli add-user --help
     ```

     ### tuloste:
      
     - **Komenton kuvaus:** Tarjoaa yksityiskohtaisen kuvauksen komentojen toiminnasta.  
     - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien pakolliset ja valinnaiset argumentit.  
     - **Valinnat:** Listaa komentokohtaiset valinnat ja niiden selitykset.  
     - **Esimerkit:** Antaa esimerkkejä komennon tehokkaasta käytöstä.

### check-config

`check-config`-komento on työkalu ***digna*** CLI -työkalussa, joka testaa ***digna***-konfiguraatiota. Tämä komento varmistaa, että ***digna***-komponentit löytävät tarvittavat konfiguraatioelementit tiedostosta config.toml.

#### Valinnat

- `--configpath`, `-cp`: Konfiguraation sisältävä tiedosto tai hakemisto. Jos jätetään pois, käytetään ../config.toml:ia.
      
#### Komennon käyttö
```bash
dignacli check-config
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen konfiguraation täydellisyydestä.  
  
Jos konfiguraatio vaikuttaa puutteelliselta, puuttuvat konfiguraatioelementit listataan.

  
### check-repo-connection

`check-repo-connection`-komento on työkalu ***digna*** CLI -työkalussa, joka testaa yhteyden ja pääsyn määritettyyn ***digna***-repositorioon. Tämä komento varmistaa, että CLI pystyy kommunikoimaan repositorion kanssa.
      
#### Komennon käyttö
```bash
dignacli check-repo-connection
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tietoja repositoriosta: Repository version, Host, Database ja Schema.  
  
Jos repositorion yhteys ei ole onnistunut, tarkista config.toml-tiedosto oikeiden asetusten varmistamiseksi.


### version

Asennetun *dignacli*-version tarkistamiseen käytä `--version`-valintaa.  
  
#### Komennon käyttö
```bash
dignacli --version
```
  
#### Esimerkkituloste
```bash
dignacli version 2025.09
```

### lokitusvaihtoehdot
  
Oletuksena ***digna***-komentojen konsolitulosteet ovat minimalistisia. Useimmissa komennoissa on kuitenkin mahdollisuus näyttää lisätietoja seuraavilla valinnoilla:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” ja ”debug” määrittävät yksityiskohtaisuustason, kun taas ”logfile”-vaihtoehto mahdollistaa tulosteen ohjaamisen tiedostoon konsolin sijaan.

## Käyttäjähallinta

### add-user
  
`add-user`-komentoa käytetään lisäämään uusi käyttäjä ***digna***-järjestelmään.
  
#### Komennon käyttö
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentit

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

#### Valinnat

- `--is_superuser`, `-su`: Lipuke, jolla uusi käyttäjä merkitään ylläpitäjäksi.
- `--valid_until`, `-vu`: Asettaa käyttäjätilille voimassaoloajan muodossa `YYYY-MM-DD HH:MI:SS`. Jos ei aseteta, tilillä ei ole vanhenemispäivää.

#### Esimerkki

Lisätäksesi uuden käyttäjän käyttäjätunnuksella `jdoe`, täydellä nimellä `John Doe` ja salasanalla `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lisätäksesi uuden käyttäjän ja määrittääksesi tilin vanhenemispäivän:
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
- **USER_NAME**: Poistettavan käyttäjän käyttäjätunnus (pakollinen). Tämä on ainoa komennon vaatima argumentti.

#### Esimerkki
```bash
dignacli delete-user jdoe
```
  
Tämän komennon suorittaminen poistaa käyttäjän `jdoe` ***digna***-järjestelmästä, peruuttaa hänen käyttöoikeutensa ja poistaa siihen liittyvät tiedot sekä oikeudet repositoriosta.

### modify-user

`modify-user`-komennolla päivitetään olemassa olevan käyttäjän tietoja ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentit
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Käyttäjän uusi koko nimi (pakollinen).
  
#### Valinnat  
  
- `--is_superuser`, `-su`: Asettaa käyttäjän superkäyttäjäksi, antaen korotetut oikeudet. Tämä lipuke ei vaadi arvoa.  
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivän muodossa YYYY-MM-DD HH:MI:SS. Jos ei anneta, tili pysyy voimassa toistaiseksi.  
  
#### Esimerkki
  
Muokataksesi käyttäjän `jdoe` koko nimeksi “Johnathan Doe” ja asettaaksesi hänet superkäyttäjäksi:
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
  
- **USER_NAME**: Salasanaa vaihdettavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_PWD**: Uusi salasana käyttäjälle (pakollinen).
  
#### Esimerkki
  
Vaihda käyttäjän `jdoe` salasana muotoon `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users`-komento näyttää luettelon kaikista ***digna***-järjestelmään rekisteröidyistä käyttäjistä.

#### Komennon käyttö

```bash
dignacli list-users
```

Tämän komennon suorittaminen yhdistää ***digna***-repositorioosi ja listaa kaikki käyttäjät, näyttäen heidän ID:nsä, käyttäjätunnuksensa, koko nimensä, superkäyttäjästatuksen ja vanhenemisaikaleimat.

## Repositorion hallinta

### upgrade-repo
  
`upgrade-repo`-komennolla päivitetään tai alustetaan ***digna***-repositorio. Tämä komento on välttämätön päivitysten soveltamiseksi tai repositorion ensimmäistä kertaa asennettaessa.
  
#### Komennon käyttö

```bash
dignacli upgrade-repo [options]
```
  
#### Valinnat
  
- `--simulation-mode`, `-s`: Kun käytössä, komento suoritetaan simulaatiotilassa, jolloin se tulostaa SQL-lauseet, jotka olisi suoritettu, mutta ei oikeasti suorita niitä. Tämä on hyödyllistä muutosten esikatseluun ilman repositorion muokkaamista.  

  
#### Esimerkki
  
Päivittääksesi ***digna***-repositorion ilman valintoja:
  
```bash
dignacli upgrade-repo
```  
Suorittaaksesi päivityksen simulaatiotilassa (näyttää SQL-lauseet ilman soveltamista):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tämä komento on tärkeä ***digna***-järjestelmän ylläpidossa, varmistaen että tietokannan skeema ja muut repositorion osat ovat ajan tasalla ohjelmiston uusimman version kanssa.

### encrypt
  
`encrypt`-komennolla salataan salasana.
  
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
Tämä komento tulostaa annetun salasanan salatun version, jota voidaan käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI näyttää virheilmoituksen puuttuvasta argumentista.

### generate-key
  
`generate-key`-komentoa käytetään Fernet keyn generoimiseen, mikä on olennainen salasanojen suojaamiseksi ***digna***-repositoriossa.
  
#### Komennon käyttö
```bash
dignacli generate-key
```
  
## Datan hallinta

### clean-up

`clean-up`-komento poistaa profiileja, ennusteita ja liikennevalojärjestelmän tietoja yhdeltä tai useammalta tietolähteeltä tietyssä projektissa. Tämä komento on oleellinen datan elinkaaren hallinnassa ja auttaa pitämään tietoympäristön järjestettynä ja tehokkaana poistamalla vanhentunutta tai tarpeetonta dataa.

#### Komennon käyttö

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, josta data poistetaan (pakollinen). Jos tässä argumentissa käytetään avainsanaa `all-projects`, ***digna*** käy läpi kaikki olemassa olevat projektit ja suorittaa komennon jokaiselle.
- **FROM_DATE**: Datan poiston alkamispäivämäärä ja -aika. Hyväksytyt muodot: %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan poiston päättymispäivämäärä ja -aika, samaa formaattia kuin FROM_DATE (pakollinen).
  
#### Valinnat
  
- `--table-name`, `-tn`: Rajaa clean-up-toiminnon tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa siten, että clean-up kohdistetaan vain tauluihin, joiden nimissä esiintyy annettu merkkijono.
- `--timing`, `-tm`: Näyttää clean-up-prosessin keston suorituksen jälkeen.
- `--help`: Näyttää clean-up-komennon ohjeet ja poistuu.
  
#### Esimerkki
  
Poista data projektista ProjectA ajalta 1. tammikuuta 2023 – 30. kesäkuuta 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Poista data vain tietystä taulusta nimeltä `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tämä komento auttaa datan säilytystilan hallinnassa ja varmistaa, että repositorio sisältää vain olennaista tietoa.

### remove-orphans
  
`remove-orphans`-komento on tarkoitettu repositorion siivoukseen.  
Kun käyttäjä poistaa projekteja tai tietolähteitä, profiilit ja ennusteet voivat jäädä repositorioon orvoiksi. Tällä komennolla tällaiset orvot rivit voidaan poistaa repositoriosta.
  
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

Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja, tarjoten nopean yleiskuvan repositorion projekteista.

### list-ds

`list-ds`-komento näyttää luettelon kaikista tietolähteistä tietyssä projektissa. Komento auttaa hahmottamaan analysoitavissa ja hallittavissa olevia dataresursseja ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, jonka tietolähteet halutaan listata (pakollinen).
  
#### Esimerkki
  
Listataksesi kaikki tietolähteet projektista nimeltä `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tämä komento antaa yleiskatsauksen projektin tietolähteistä, mikä auttaa navigoinnissa ja datan hallinnassa.


### inspect

`inspect`-komennolla luodaan profiileja, ennusteita ja liikennevalojärjestelmän tietoja yhdelle tai useammalle tietolähteelle määritetyssä projektissa. Komento auttaa analysoimaan ja seuraamaan dataa määritellyllä aikavälillä. Tarkastuksen valmistuttua palautetaan laskettujen liikennevalon arvo:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komennon käyttö

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastellaan (pakollinen). Jos tässä argumentissa käytetään avainsanaa `all-projects`, ***digna*** käy läpi kaikki olemassa olevat projektit ja suorittaa komennon jokaiselle.
- **FROM_DATE**: Tarkastuksen aloituspäivämäärä ja -aika. Hyväksytyt muodot: %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastuksen päättymispäivämäärä ja -aika, samaa formaattia kuin FROM_DATE (pakollinen).
  
#### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa siten, että tarkastus tehdään vain tauluihin, joiden nimissä esiintyy annettu merkkijono.
- `--enable_notification`, `-en`: Ottaa käyttöön ilmoitusten lähettämisen hälytystilanteissa.
- `--bypass-backend`, `-bb`: Ohittaa backendin ja suorittaa tarkastuksen suoraan CLI:stä (vain testikäyttöön!).

  
#### Esimerkki
  
Tarkasta projektin `ProjectA` data ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Tarkasta vain tietty taulu ja pakota ennusteiden uudelleenlaskenta:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden luomiseen, dataintegriuden valvontaan ja hälytysjärjestelmien hallintaan määritellyllä aikavälillä.

### inspect-async

`inspect-async`-komennolla luodaan profiileja, ennusteita ja liikennevalojärjestelmän tietoja yhdelle tai useammalle tietolähteelle määritetyssä projektissa. Tämä komento auttaa analysoimaan ja seuraamaan dataa määritellyllä aikavälillä. Toisin kuin synkroninen inspect-komento, tämä ei odota tarkastuksen valmistumista. Sen sijaan se palauttaa pyynnön tunnisteen (request id) lähetetylle tarkastuspyynnölle. Tarkastuksen etenemisen kyselyyn käytä komentoa `inspect-status`.

#### Komennon käyttö

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastellaan (pakollinen). Jos tässä argumentissa käytetään avainsanaa `all-projects`, ***digna*** käy läpi kaikki olemassa olevat projektit ja suorittaa komennon jokaiselle.
- **FROM_DATE**: Tarkastuksen aloituspäivämäärä ja -aika. Hyväksytyt muodot: %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastuksen päättymispäivämäärä ja -aika, samaa formaattia kuin FROM_DATE (pakollinen).
  
#### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa siten, että tarkastus tehdään vain tauluihin, joiden nimissä esiintyy annettu merkkijono.
- `--enable_notification`, `-en`: Ottaa käyttöön ilmoitusten lähettämisen hälytystilanteissa.

  
#### Esimerkki
  
Tarkasta projektin `ProjectA` data ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024 asynkronisesti:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-komennolla tarkistetaan asynkronisen tarkastuksen eteneminen pyynnön tunnisteen perusteella.

#### Komennon käyttö

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama pyyntötunniste 
  
#### Esimerkki
  
Tarkista tarkastuksen eteneminen pyynnöllä, jonka tunniste on 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-komennolla voidaan peruuttaa tarkastuksia pyynnön tunnisteen perusteella tai peruuttaa kaikki käynnissä olevat pyynnöt.

#### Komennon käyttö

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama pyyntötunniste 
  
#### Esimerkki
  
Peruuta tarkastus, jonka pyyntötunniste on 12345:
  
```bash
dignacli inspect-cancel 12345
```

Peruuta kaikki käynnissä tai jonossa olevat pyynnöt:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-komennolla luodaan vienti tietolähteistä ***digna***-repositoriosta. Oletuksena viedään kaikki tietolähteet annetusta projektista.

#### Komennon käyttö
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, josta tietolähteet viedään.

#### Valinnat

- `--table_name`, `-tn`: Vie tietyn tietolähteen projektista.
- `--exportfile`, `-ef`: Määritä vientitiedoston nimi.
    
#### Esimerkki
  
Viedäksesi kaikki tietolähteet projektista `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tämä komento vie kaikki `ProjectA`-projektin tietolähteet JSON-dokumentiksi, joka voidaan tuoda toiseen projektiin tai ***digna***-repositorioon.


### import-ds

`import-ds`-komennolla tuodaan tietolähteitä kohdeprojektiin ja luodaan tuontiraportti.

#### Komennon käyttö
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon tietolähteet tuodaan.
- **EXPORT_FILE**: Tuotavan vientitiedoston tiedostonimi.

#### Valinnat

- `--output-file`, `-o`: Tiedosto, johon tallennetaan tuontiraportti (jos ei määritetä, tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, johon tuontiraportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tuo kaikki tietolähteet vientitiedostosta `my_export.json` kohteeseen `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Tuonnin jälkeen komento näyttää raportin tuoduista ja ohitetuista objekteista. Vain uudet tietolähteet tuodaan `ProjectB`:hen. Selvittääksesi, mitkä objektit tuodaan tai ohitetaan, voit käyttää komentoa `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-komento analysoi vientitiedoston ja näyttää tuontisuunnitelman, eli mitkä tietolähteet tuodaan ja mitkä ohitetaan.

#### Komennon käyttö
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon tietolähteet mahdollisesti tuodaan.
- **EXPORT_FILE**: Vientitiedoston tiedostonimi, joka analysoidaan ennen tuontia.

#### Valinnat

- `--output-file`, `-o`: Tiedosto, johon tallennetaan tuontiraportti (jos ei määritetä, tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, johon tuontiraportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tarkista mitkä tietolähteet tuodaan ja mitkä ohitetaan vientitiedostosta `my_export.json` tuotaessa ne `ProjectB`-projektiin:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tämä komento näyttää vain suunnitelman objekteista, jotka tuodaan ja ohitetaan.