# digna CLI -viite 2026.04
**2026-04-08**

Tämä sivu dokumentoi kaikki ***digna*** CLI -julkaisun **2026.04** käytettävissä olevat komennot, sisältäen käyttöesimerkkejä ja valintoja.

---

## CLI:n perusteet

---

### help
`--help`-valinta tarjoaa tietoa käytettävissä olevista komennoista ja niiden käytöstä. Tämän valinnan käyttöön on kaksi päätapaa:

1. **Yleisen ohjeen näyttäminen:**
   
    Käytä `--help`-valintaa heti komentoa `dignacli` seuraavana.  
   ```bash
   dignacli --help
   ```

2. **Ohje tietylle komennolle:**  
  
    Saadaksesi yksityiskohtaisia tietoja tietystä komennosta, lisää `--help` kyseisen komennon perään.
    Esimerkiksi saadaksesi ohjeet `add-user`-komennosta, aja:
     ```bash
     dignacli add-user --help
     ```

     ### tuloste:
      
     - **Komenton kuvaus:** Tarjoaa yksityiskohtaisen kuvauksen siitä, mitä komento tekee.  
     - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien pakolliset ja valinnaiset argumentit.  
     - **Valinnat:** Listaa komennon erityiset valinnat ja niiden selitykset.  
     - **Esimerkit:** Antaa esimerkkejä komennon tehokkaasta suorittamisesta.

### check-config

`check-config`-komento on apuohjelma ***digna*** CLI -työkalussa, jonka tarkoituksena on testata ***digna***-konfiguraatiota. Tämä komento varmistaa, että ***digna***-komponentit löytävät tarvittavat konfiguraatioelementit tiedostosta `config.toml`.

#### Valinnat

- `--configpath`, `-cp`: Tiedosto tai hakemisto, joka sisältää konfiguraation. Jos tätä ei anneta, käytetään `../config.toml`.
      
#### Komennon käyttö
```bash
dignacli check-config
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen konfiguraation täydellisyydestä.  
  
Jos konfiguraatio näyttää puutteelliselta, puuttuvat konfiguraatioelementit listataan.

  
### check-repo-connection

`check-repo-connection`-komento on apuohjelma ***digna*** CLI -työkalussa, jonka tarkoituksena on testata yhteyttä ja pääsyä määriteltyyn ***digna***-repositoryyn. Tämä komento varmistaa, että CLI pystyy kommunikoimaan repositoryn kanssa.
      
#### Komennon käyttö
```bash
dignacli check-repo-connection
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tietoja repositorysta: Repository-versio, Isäntä, Tietokanta ja Schema.  
  
Jos repository-yhteys epäonnistuu, tarkista `config.toml`-tiedoston asetukset.

### version

Tarkista asennettu *dignacli*-versio käyttämällä `--version`-valintaa.  
  
#### Komennon käyttö
```bash
dignacli --version
```
  
#### Esimerkkituloste
```bash
dignacli version 2026.04
```

### lokitusvalinnat
  
Oletuksena ***digna***-komentojen konsolituloste on minimalistinen. Useimmissa komennoissa on mahdollisuus näyttää lisätietoa käyttämällä seuraavia valintoja:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” ja ”debug” määrittelevät yksityiskohtaisuustason, kun taas ”logfile”-kytkin mahdollistaa tulosteen uudelleenohjauksen tiedostoon konsolin sijaan.

## Käyttäjähallinta

### add-user
  
`add-user`-komentoa ***digna*** CLI:ssä käytetään uuden käyttäjän lisäämiseen ***digna***-järjestelmään.
  
#### Komennon käyttö
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentit

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

#### Valinnat

- `--is_superuser`, `-su`: Lipuke uuden käyttäjän merkitsemiseksi ylläpitäjäksi.
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivän muodossa `YYYY-MM-DD HH:MI:SS`. Jos tätä ei aseteta, tilillä ei ole vanhenemispäivää.

#### Esimerkki

Lisätäksesi uuden käyttäjän käyttäjätunnuksella `jdoe`, koko nimellä `John Doe` ja salasanalla `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lisätäksesi uuden käyttäjän ja asettaaksesi tilin vanhenemispäivän:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user`-komentoa ***digna*** CLI:ssä käytetään olemassa olevan käyttäjän poistamiseen ***digna***-järjestelmästä.
  
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
  
Tämän komennon suorittaminen poistaa käyttäjän `jdoe` ***digna***-järjestelmästä, peruuttaa tämän pääsyn ja poistaa siihen liittyvät tiedot ja oikeudet repositorysta.

### modify-user

`modify-user`-komentoa ***digna*** CLI:ssä käytetään olemassa olevan käyttäjän tietojen päivittämiseen ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentit
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Käyttäjän uusi koko nimi (pakollinen).
  
#### Valinnat  
  
- `--is_superuser`, `-su`: Asettaa käyttäjän superkäyttäjäksi, antaen laajennetut oikeudet. Tämä lipuke ei vaadi arvoa.  
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei anneta, tili pysyy voimassa toistaiseksi.  
  
#### Esimerkki
  
Muokataksesi käyttäjän `jdoe` koko nimeä muotoon “Johnathan Doe” ja asettaaksesi käyttäjän superkäyttäjäksi:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd`-komentoa ***digna*** CLI:ssä käytetään olemassa olevan käyttäjän salasanan muuttamiseen.
  
#### Komennon käyttö
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentit
  
- **USER_NAME**: Käyttäjän käyttäjätunnus, jonka salasana muutetaan (pakollinen).
- **USER_PWD**: Uusi salasana käyttäjälle (pakollinen).
  
#### Esimerkki
  
Muuttaaksesi käyttäjän `jdoe` salasanan arvoksi `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users`-komento ***digna*** CLI:ssä näyttää listan kaikista järjestelmään rekisteröidyistä käyttäjistä.

#### Komennon käyttö

```bash
dignacli list-users
```

Tämän komennon suorittaminen yhdistää ***digna***-repositoryyn ja listaa kaikki käyttäjät näyttäen niiden ID:n, käyttäjätunnuksen, koko nimen, superkäyttäjästatuksen ja vanhenemisajat.

## Repositoryn hallinta

### upgrade-repo
  
`upgrade-repo`-komentoa ***digna*** CLI:ssä käytetään ***digna***-repositoryn päivittämiseen tai alustamiseen. Tämä komento on tarpeen päivitysten soveltamiseen tai repository-infrastruktuurin ensiasennukseen.
  
#### Komennon käyttö

```bash
dignacli upgrade-repo [options]
```
  
#### Valinnat
  
- `--simulation-mode`, `-s`: Kun tämä valinta on käytössä, komento suoritetaan simulaatiotilassa, joka tulostaa SQL-lauseet, jotka olisi suoritettu, mutta ei itse suoritakaan niitä. Tämä on hyödyllistä muutosten esikatseluun ilman repositoryn muuttamista.  

  
#### Esimerkki
  
Päivittääksesi ***digna***-repositoryn voit ajaa komennon ilman valintoja:
  
```bash
dignacli upgrade-repo
```  
Ajaaksesi päivityksen simulaatiotilassa (näyttää SQL-lauseet ilman niiden suorittamista):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tämä komento on keskeinen ***digna***-järjestelmän ylläpidossa, varmistaen että tietokannan skeema ja muut repositoryn komponentit ovat ajan tasalla ohjelmiston uusimman version kanssa.

### encrypt
  
`encrypt`-komentoa ***digna*** CLI:ssä käytetään salasanan salaamiseen.
  
#### Komennon käyttö
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentit
- **PASSWORD**: Salasana, joka halutaan salata (pakollinen).
  
#### Esimerkki
  
Salataksesi salasanan, anna salasana argumenttina.   
Esimerkiksi salataksesi salasanan `mypassword123`, käyttäisit:
```bash
dignacli encrypt mypassword123
```
Tämä komento palauttaa annettua salasanaa vastaavan salatun merkkijonon, jota voidaan käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI näyttää virheilmoituksen puuttuvasta argumentista.

### generate-key
  
`generate-key`-komentoa käytetään Fernet-avaimen luomiseen, joka on välttämätön säilytettävien salasanojen suojaamiseksi ***digna***-repositoryssa.
  
#### Komennon käyttö
```bash
dignacli generate-key
```
  
## Datan hallinta

### clean-up

`clean-up`-komentoa ***digna*** CLI:ssä käytetään profiilien, ennusteiden ja vilkkuvalo-järjestelmän tietojen poistamiseen yhdeltä tai useammalta tietolähteeltä määritellyssä projektissa. Tämä komento on tärkeä datan elinkaaren hallinnassa ja auttaa pitämään ympäristön järjestettynä poistamalla vanhentuneita tai tarpeettomia tietoja.

#### Komennon käyttö

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, josta data poistetaan (pakollinen). Käytettäessä avainsanaa `all-projects` tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja soveltaa komentoa niihin.
- **FROM_DATE**: Datan poistamisen aloituspäivä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan poistamisen lopetuspäivä ja -aika, samaa formaattia kuin FROM_DATE (pakollinen).
  
#### Valinnat
  
- `--table-name`, `-tn`: Rajaa clean-up-toiminnon koskemaan tiettyä taulukkoa projektissa.
- `--table-filter`, `-tf`: Suodattaa, jotta clean-up kohdistuu vain tauluihin, joiden nimissä on annettu alimerkkijono.
- `--timing`, `-tm`: Näyttää clean-up-prosessin keston suorituksen jälkeen.
- `--help`: Näyttää help-tiedot clean-up-komennosta ja poistuu.
  
#### Esimerkki
  
Poistaaksesi dataa projektista `ProjectA` ajalta 1. tammikuuta 2023 – 30. kesäkuuta 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Poistaaksesi dataa vain tietystä taulusta nimeltä `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tämä komento auttaa hallitsemaan tallennustilaa ja varmistamaan, että repository sisältää vain relevanttia tietoa.

### remove-orphans
  
`remove-orphans`-komento ***digna*** CLI:ssä on tarkoitettu repositoryn ylläpitoon.  
Kun käyttäjä poistaa projekteja tai tietolähteitä, profiilit ja ennusteet saattavat jäädä repositoryyn. Tällä komennolla tällaiset orpoiksi jääneet rivit poistetaan repositorysta.
  
#### Komennon käyttö
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects`-komento ***digna*** CLI:ssä näyttää listan kaikista saatavilla olevista projekteista ***digna***-järjestelmässä.
  
#### Komennon käyttö
  
```bash
dignacli list-projects
```

Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja, tarjoten nopean yleiskatsauksen repositoryssa olevista projekteista.

### list-ds

`list-ds`-komento ***digna*** CLI:ssä näyttää listan kaikista tietolähteistä tietyn projektin sisällä. Tämä komento on hyödyllinen, kun halutaan ymmärtää analysoitavissa ja hallinnoitavissa olevat dataresurssit ***digna***-järjestelmässä.

#### Komennon käyttö
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, jolle tietolähteet listataan (pakollinen).
  
#### Esimerkki
  
Listataksesi kaikki tietolähteet projektissa `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tämä komento antaa käyttäjille yleiskuvan projektin tietolähteistä, auttaa navigoinnissa ja datan hallinnassa.

### inspect

`inspect`-komentoa ***digna*** CLI:ssä käytetään profiilien, ennusteiden ja vilkkuvalo-järjestelmän tietojen luomiseen yhdelle tai useammalle tietolähteelle määritellyssä projektissa. Tämä komento auttaa datan analysoinnissa ja seurannassa määritellyllä aikavälillä. Tarkastuksen valmistuttua laskettu vilkkuvalo-arvo palautetaan:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komennon käyttö

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastetaan (pakollinen). Käyttämällä avainsanaa `all-projects` tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja soveltaa komentoa niihin.
- **FROM_DATE**: Tarkastuksen aloituspäivä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastuksen lopetuspäivä ja -aika, samaa formaattia kuin FROM_DATE (pakollinen).
  
#### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa, jotta tarkastus tehdään vain tauluihin, joiden nimissä on annettu alimerkkijono.
- `--enable_notification`, `-en`: Mahdollistaa ilmoitusten lähettämisen hälytystilanteissa.
- `--bypass-backend`, `-bb`: Ohittaa backendin ja suorittaa tarkastus suoraan CLI:stä (vain testauskäyttöön!).

  
#### Esimerkki
  
Tarkastaaksesi projektin `ProjectA` dataa ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Tarkastaaksesi vain tietyn taulun ja pakottaaksesi ennusteiden uudelleenlaskennan:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden generointiin, dataintegrieteetin seurantaan ja hälytysjärjestelmien hallintaan määritellyllä projektin aikavälillä.

### inspect-async

`inspect-async`-komento ***digna*** CLI:ssä käytetään profiilien, ennusteiden ja vilkkuvalo-järjestelmän tietojen luomiseen yhdelle tai useammalle tietolähteelle määritellyssä projektissa. Tämä komento auttaa datan analysoinnissa ja seurannassa määritellyllä aikavälillä. Toisin kuin synkroninen `inspect`-komento, tämä ei odota tarkastuksen valmistumista. Sen sijaan se palauttaa pyynnön tunnisteen lähetetylle tarkastuspyynnölle. Tarkastuksen etenemisen kyselyyn käytä komentoa `inspect-status`.

#### Komennon käyttö

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastetaan (pakollinen). Käyttämällä avainsanaa `all-projects` tässä argumentissa, ***digna*** käy läpi kaikki olemassa olevat projektit ja soveltaa komentoa niihin.
- **FROM_DATE**: Tarkastuksen aloituspäivä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastuksen lopetuspäivä ja -aika, samaa formaattia kuin FROM_DATE (pakollinen).
  
#### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastuksen tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa, jotta tarkastus tehdään vain tauluihin, joiden nimissä on annettu alimerkkijono.
- `--enable_notification`, `-en`: Mahdollistaa ilmoitusten lähettämisen hälytystilanteissa.

  
#### Esimerkki
  
Suorittaaksesi asynkronisen tarkastuksen projektissa `ProjectA` ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-komentoa ***digna*** CLI:ssä käytetään tarkastuksen etenemisen tarkistamiseen asynkroniselle tarkastukselle pyynnön tunnisteen perusteella.

#### Komennon käyttö

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama pyynnön tunniste 
  
#### Esimerkki
  
Tarkistaaksesi tarkastuksen eteneminen, jonka pyynnön tunniste on 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-komentoa ***digna*** CLI:ssä käytetään tarkastusten peruuttamiseen pyynnön tunnisteen avulla tai komentoa voidaan käyttää kaikkien nykyisten pyyntöjen peruuttamiseen.

#### Komennon käyttö

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentit
  
- **REQUEST_ID**: `inspect-async`-komennon palauttama pyynnön tunniste 
  
#### Esimerkki
  
Peruuttaaksesi tarkastuksen, jonka pyynnön tunniste on 12345:
  
```bash
dignacli inspect-cancel 12345
```

Peruuttaaksesi kaikki parhaillaan käynnissä tai jonossa olevat pyynnöt:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-komentoa ***digna*** CLI:ssä käytetään tietolähteiden viennin luomiseen ***digna***-repositorysta. Oletuksena kaikki tietolähteet annetusta projektista viedään.

#### Komennon käyttö
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, josta tietolähteet viedään.

#### Valinnat

- `--table_name`, `-tn`: Vie tietyn tietolähteen projektista.
- `--exportfile`, `-ef`: Määrittää viennin tiedostonimen.
    
#### Esimerkki
  
Viedäksesi kaikki tietolähteet projektista `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Tämä komento vie kaikki `ProjectA`-projektin tietolähteet JSON-dokumentiksi, joka voidaan tuoda toiseen projektiin tai ***digna***-repositoryyn.

### import-ds

`import-ds`-komentoa ***digna*** CLI:ssä käytetään tietolähteiden tuomiseen kohdeprojektiin ja tuoteraportin luomiseen.

#### Komennon käyttö
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon tietolähteet tuodaan.
- **EXPORT_FILE**: Tuotavan viennin tiedostonimi.

#### Valinnat

- `--output-file`, `-o`: Tiedosto, johon import-raportti tallennetaan (jos ei määritetty, tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, johon import-raportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tuodaksesi kaikki tietolähteet vientitiedostosta `my_export.json` projektiin `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Tuonnin jälkeen komento näyttää myös raportin tuoduista ja ohitetuista objekteista. Vain uudet tietolähteet tuodaan `ProjectB`-projektiin. Selvittääksesi, mitkä objektit tuodaan ja mitkä ohitetaan, voit käyttää komentoa `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-komentoa ***digna*** CLI:ssä käytetään analysoimaan vientitiedosto ennen tietolähteiden tuontia kohdeprojektiin ja luomaan import-suunnitelman.

#### Komennon käyttö
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentit
- **PROJECT_NAME**: Projektin nimi, johon tietolähteet mahdollisesti tuodaan.
- **EXPORT_FILE**: Viennin tiedostonimi, joka analysoidaan ennen tuontia.

#### Valinnat

- `--output-file`, `-o`: Tiedosto, johon import-raportti tallennetaan (jos ei määritetty, tulostetaan terminaaliin taulukkona).
- `--output-format`, `-f`: Muoto, johon import-raportti tallennetaan (json, csv).
    
#### Esimerkki
  
Tarkistaaksesi, mitkä tietolähteet tuodaan ja mitkä ohitetaan vientitiedostosta `my_export.json` tuotaessa projektiin `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Tämä komento näyttää vain suunnitelman tuoduista ja ohitetuista objekteista.