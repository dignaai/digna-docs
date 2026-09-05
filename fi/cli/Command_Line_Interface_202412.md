# digna CLI Reference 2024.12
**2024-12-09**

Tällä sivulla dokumentoidaan kaikki komentoriviliittymän (CLI) ***digna*** komennot versiossa **2024.12**, mukaan lukien käyttöesimerkit ja valinnat.

---


**2024-12-09**


---

## CLI:n perusasiat

---

## `--help`-vaihtoehdon käyttäminen

`--help`-vaihtoehto näyttää tietoja käytettävissä olevista komennoista ja niiden käytöstä. Tätä vaihtoehtoa voi käyttää kahdella pääasiallisella tavalla:

1. Yleisen ohjeen näyttäminen:
   
   Käytä `--help`-valitsinta heti `dignacli`-komennon jälkeen:
   ```bash
   dignacli --help
   ```

2. Tietyn komennon ohjeen hakeminen:
   
   Saat yksityiskohtaiset tiedot tietystä komennosta lisäämällä `--help` kyseisen komennon perään.
   Esimerkiksi `add-user`-komennon ohjeen saat ajamalla:
   ```bash
   dignacli add-user --help
   ```

   ### Tuloste:
      
   - **Komenton kuvaus:** Kuvaa yksityiskohtaisesti, mitä komento tekee.  
   - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien pakolliset ja valinnaiset argumentit.  
   - **Valinnat:** Luettelee komennolle erityiset valinnat ja niiden selitykset.  
   - **Esimerkit:** Antaa esimerkkejä komennon tehokkaasta suorittamisesta.

  
## `check-repo-connection`-komennon käyttäminen

`check-repo-connection` on ***digna*** CLI -työkalun apukomento, jolla testataan yhteyttä ja pääsyä määritettyyn ***digna***-repoon. Tämä komento varmistaa, että CLI pystyy kommunikoimaan repositorion kanssa.
      
### Komennon käyttö
```bash
dignacli check-repo-connection
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tietoja repositoriosta: Repository version, Host, Database ja Schema.  
  
Jos repositorion yhteys epäonnistuu, tarkista config.toml-tiedosto ja varmista asetusten oikeellisuus.

## `--version`-komennon käyttäminen

Tarkista asennettu *dignacli*-versio käyttämällä `--version`-vaihtoehtoa.  
  
### Komennon käyttö
```bash
dignacli --version
```
  
### Esimerkkituloste
```bash
dignacli version 2024.12
```

## Lokitusvaihtoehtojen käyttäminen
  
Oletuksena ***digna***-komentojen konsolitulosteet ovat minimalistisia. Useimmat komennot tarjoavat kuitenkin mahdollisuuden lisätiedon tulostamiseen seuraavilla valinnoilla:  
  
- `--verbose` (-v)  
- `--debug` (-d)  
- `--logfile` (lf)  
 
”verbose” ja ”debug” määrittävät yksityiskohtaisuustason, kun taas ”logfile”-valinta mahdollistaa tulosteen ohjaamisen tiedostoon konsolin sijaan.

# Käyttäjähallinta

## `add-user`-komennon käyttäminen
  
`add-user`-komentoa käytetään lisäämään uusi käyttäjä ***digna***-järjestelmään.
  
### Komennon käyttö
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentit

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

### Valinnat

- `--is_superuser`, `-su`: Lipuke, jolla käyttäjä merkitään ylläpitäjäksi.
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivämäärän muodossa `YYYY-MM-DD HH:MI:SS`. Jos tätä ei aseteta, tilillä ei ole eräpäivää.

### Esimerkki

Lisätään uusi käyttäjä käyttäjätunnuksella `jdoe`, koko nimellä `John Doe` ja salasanalla `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lisätään käyttäjä ja asetetaan tilin vanhenemispäivä:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user`-komennon käyttäminen
  
`delete-user`-komennolla poistetaan olemassa oleva käyttäjä ***digna***-järjestelmästä.
  
### Komennon käyttö
```bash
dignacli delete-user USER_NAME
```
  
### Argumentit
- **USER_NAME**: Poistettavan käyttäjän käyttäjätunnus (pakollinen). Tämä on ainoa pakollinen argumentti.

### Esimerkki
```bash
dignacli delete-user jdoe
```
  
Tämän komennon suorittaminen poistaa käyttäjän `jdoe` ***digna***-järjestelmästä, peruuttaa pääsyn ja poistaa siihen liittyvät tiedot ja käyttöoikeudet repositoriosta.

## `modify-user`-komennon käyttäminen

`modify-user`-komennolla päivitetään olemassa olevan käyttäjän tietoja ***digna***-järjestelmässä.

### Komennon käyttö
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentit
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Käyttäjän uusi koko nimi (pakollinen).
  
### Valinnat  
  
- `--is_superuser`, `-su`: Asettaa käyttäjän superkäyttäjäksi, mikä antaa korotetut oikeudet. Tämä valinta ei vaadi arvoa.  
- `--valid_until`, `-vu`: Asettaa käyttäjätilin erääntymispäivän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei anneta, tili pysyy voimassa toistaiseksi.  
  
### Esimerkki
  
Muokataan käyttäjän `jdoe` koko nimeksi "Johnathan Doe" ja asetetaan käyttäjä superkäyttäjäksi:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd`-komennon käyttäminen
  
`modify-user-pwd`-komennolla vaihdetaan olemassa olevan käyttäjän salasana ***digna***-järjestelmässä.
  
### Komennon käyttö
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentit
  
- **USER_NAME**: Käyttäjän käyttäjätunnus, jonka salasana vaihdetaan (pakollinen).
- **USER_PWD**: Uusi salasana (pakollinen).
  
### Esimerkki
  
Vaihdetaan käyttäjän `jdoe` salasana muotoon `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users`-komennon käyttäminen

`list-users`-komento näyttää luettelon kaikista ***digna***-järjestelmään rekisteröidyistä käyttäjistä.

### Komennon käyttö

```bash
dignacli list-users
```

Tämä komento yhdistää ***digna***-repositorioon ja listaa kaikki käyttäjät, näyttäen niiden ID:n, käyttäjätunnuksen, koko nimen, superkäyttäjästatuksen ja vanhenemisajat.

# Repositorion hallinta

### `upgrade-repo`-komennon käyttäminen
  
`upgrade-repo`-komennolla päivitetään tai alustetaan ***digna***-reposti. Tämä komento on välttämätön päivitysten soveltamiseen tai repositorion alustan ensimmäiseen käyttöönottoon.
  
### Komennon käyttö

```bash
dignacli upgrade-repo [options]
```
  
### Valinnat
  
- `--simulation-mode`, `-s`: Kun tämä valinta on päällä, komento suoritetaan simulointitilassa, mikä tulostaa suoritettavat SQL-lauseet mutta ei itse ajetta niitä. Tämä on hyödyllistä muutosten esikatseluun ilman, että varsinaista repositoriota muokataan.  

  
### Esimerkki
  
Päivitetään ***digna***-repositorio ilman lisävalintoja:
  
```bash
dignacli upgrade-repo
```  
Suoritetaan päivitys simulointitilassa (näytetään SQL-lauseet soveltamatta muutoksia):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tämä komento on keskeinen ***digna***-järjestelmän ylläpidossa ja varmistaa, että tietokantakaavio ja muut repositorion osat ovat ajan tasalla ohjelmiston uusimman version kanssa.

## `encrypt`-komennon käyttäminen
  
`encrypt`-komennolla salataan salasana ***digna***-CLI:ssä.
  
### Komennon käyttö
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentit
- **PASSWORD**: Salasana, joka halutaan salata (pakollinen).
  
### Esimerkki
  
Salasanan salaaminen onnistuu antamalla salasana argumenttina.   
Esimerkiksi salattaessa salasana `mypassword123`:
```bash
dignacli encrypt mypassword123
```
Komento tulostaa annetun salasanan salatun version, jota voidaan käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI ilmoittaa puuttuvasta argumentista.

## `generate-key`-komennon käyttäminen
  
`generate-key`-komennolla luodaan Fernet-avain, joka on tarpeen salasanojen suojaamiseksi ***digna***-repositoriossa.
  
### Komennon käyttö
```bash
dignacli generate-key
```
  
# Datan hallinta

## `clean-up`-komennon käyttäminen

`clean-up`-komennolla poistetaan profiileja, ennusteita ja liikennevalojärjestelmän (Traffic Light System) tietoja yhdeltä tai useammalta tietolähteeltä määritellyssä projektissa. Tämä komento on tärkeä datan elinkaaren hallinnassa ja auttaa pitämään ympäristön järjestettynä ja tehokkaana poistamalla vanhentunutta tai tarpeetonta dataa.

### Komennon käyttö

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, josta data poistetaan (pakollinen). Argumenttina voi käyttää avainsanaa `all-projects`, jolloin ***digna*** toistaa komennon kaikille olemassa oleville projekteille.
- **FROM_DATE**: Datapoiston aloituspäivämäärä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datapoiston loppupäivämäärä ja -aika, samaa muotoa käyttäen kuin FROM_DATE (pakollinen).
  
### Valinnat
  
- `--table-name`, `-tn`: Rajaa clean-up-toiminnon tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa siten, että clean-up koskee vain tauluja, joiden nimessä on annettu alimerkkijono.
- `--timing`, `-tm`: Näyttää clean-up-prosessin kestoajan suorituksen jälkeen.
- `--help`: Näyttää clean-up-komennon ohjeet ja poistuu.
  
### Esimerkki
  
Poistetaan data projektista ProjectA ajalta 1. tammikuuta 2023 – 30. kesäkuuta 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Poistetaan data vain tietystä taulusta nimeltä `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tämä komento auttaa hallitsemaan tallennustilaa ja varmistamaan, että repositoriossa säilytetään vain oleellinen tieto.

## `inspect`-komennon käyttäminen

`inspect`-komennolla luodaan profiileja, ennusteita ja liikennevalojärjestelmän tietoja yhdelle tai useammalle tietolähteelle määritellyssä projektissa. Komento auttaa datan analysoinnissa ja seurannassa määritellyltä aikaväliltä.

### Komennon käyttö

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tarkastellaan (pakollinen). Voit käyttää `all-projects`-avainsanaa suorittaaksesi komennon kaikille projekteille.
- **FROM_DATE**: Tarkastelun aloituspäivämäärä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastelun lopetuspäivämäärä ja -aika, samaa formaattia käyttäen kuin FROM_DATE (pakollinen).
  
### Valinnat

- `--table-name`, `-tn`: Rajaa tarkastelun tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa tarkastelun koskemaan vain tauluja, joiden nimessä on annettu alimerkkijono.
- `--do-profile`: Käynnistää profiilien uudelleenkeruun. Oletusarvo on do-profile.
- `--no-do-profile`: Estää profiilien uudelleenkeruun.
- `--do-prediction`: Käynnistää ennusteiden uudelleenlaskennan. Oletusarvo on do-prediction.
- `--no-do-prediction`: Estää ennusteiden uudelleenlaskennan.
- `--do-alert-status`: Käynnistää hälytystilojen uudelleenlaskennan. Oletusarvo on do-alert-status.
- `--no-do-alert-status`: Estää hälytystilojen uudelleenlaskennan.
- `--iterative`: Tarkastelee ajanjaksoa päivittäisten iterointien avulla. Oletusarvo on iterative.
- `--no-iterative`: Suorittaa tarkastelun koko ajanjaksolle yhdellä kertaa.
- `--timing`, `-tm`: Näyttää tarkasteluprosessin keston suorituksen jälkeen.
  
### Esimerkki
  
Tarkastellaan projektin `ProjectA` dataa ajalta 1. tammikuuta 2024 – 31. tammikuuta 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Tarkastellaan vain tiettyä taulua ja pakotetaan ennusteiden uudelleenlaskenta:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden luomiseen, datan eheyden seuraamiseen sekä hälytysjärjestelmän hallintaan määritellyllä aikavälillä.

## `tls-status`-komennon käyttäminen

`tls-status`-komennolla kysytään Traffic Light Systemin (TLS) tilaa tietylle taululle tietyssä projektissa annetulta päivältä. Liikennevalojärjestelmä antaa käsityksen datan kunnosta ja laadusta sekä mahdollisista ongelmista tai hälytyksistä, jotka vaativat huomiota.
  
### Komennon käyttö
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jonka TLS-tilaa kysytään (pakollinen).
- **TABLE_NAME**: Taulu, jonka TLS-tila tarvitaan (pakollinen).
- **DATE**: Päivämäärä, jolta TLS-tila kysytään, yleensä muodossa %Y-%m-%d (pakollinen).
  
### Esimerkki
  
Tarkastetaan TLS-tila taululle UserData projektissa ProjectA päivältä 1. heinäkuuta 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Tämä komento auttaa käyttäjiä seuraamaan ja ylläpitämään datan laatua tarjoamalla selkeän ja toimintaohjeita antavan tilanneraportin ennalta määritettyjen kriteerien perusteella.

## `list-projects`-komennon käyttäminen
  
`list-projects` näyttää luettelon kaikista saatavilla olevista projekteista ***digna***-järjestelmässä.
  
### Komennon käyttö
  
```bash
dignacli list-projects
```

Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja, tarjoten nopean yleiskatsauksen repositorion saatavilla olevista projekteista.

## `list-ds`-komennon käyttäminen

`list-ds`-komento näyttää luettelon kaikista saatavilla olevista tietolähteistä (data sources) määritellyssä projektissa. Tämä komento auttaa ymmärtämään projektiin liittyvät dataresurssit, jotka ovat analysoitavissa ja hallittavissa ***digna***-järjestelmässä.

### Komennon käyttö
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentit
- **PROJECT_NAME**: Projektin nimi, jonka tietolähteet listataan (pakollinen).
  
### Esimerkki
  
Listataan kaikki tietolähteet projektissa `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tämä komento antaa käyttäjille yleiskuvan projektin tietolähteistä ja auttaa heitä navigoimaan sekä hallitsemaan dataympäristöä tehokkaammin.