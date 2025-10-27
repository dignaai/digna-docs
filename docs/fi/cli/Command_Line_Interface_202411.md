---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.11. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Tällä sivulla on dokumentoitu kaikki komennot, jotka ovat saatavilla ***digna*** CLI -julkaisussa **2024.11**, mukaan lukien käyttöesimerkit ja vaihtoehdot.


---
## CLI Basics

---

## Käyttö: `help`-vaihtoehto

`--help`-vaihtoehto tarjoaa tietoa käytettävissä olevista komennoista ja niiden käytöstä. On kaksi päätapaa käyttää tätä vaihtoehtoa:

1. **Yleisen ohjeen näyttäminen:**
   
    Käytä --help heti komennon ***dignacli*** jälkeen.  
   ```bash
   dignacli --help
   ```

2. **Ohje tietylle komennolle:**
  
    Saat yksityiskohtaiset ohjeet tiettyä komentoa varten lisäämällä `--help` kyseisen komennon perään.  
    Esimerkiksi saadaksesi ohjeet `add-user`-komennosta, suorita:
     ```bash
     dignacli add-user --help
     ```

     ### Tuloste:
      
     - **Komennon kuvaus:** Antaa yksityiskohtaisen kuvauksen komennon toiminnasta.  
     - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien vaaditut ja valinnaiset argumentit.  
     - **Vaihtoehdot:** Listaa komennon spesifiset vaihtoehdot ja niiden selitykset.  
     - **Esimerkit:** Tarjoaa esimerkkejä komennon tehokkaasta suorittamisesta.

  
## Käyttö: `check-repo-connection`-komento

`check-repo-connection`-komento on työkalu ***digna*** CLI:ssä, jolla testataan yhteyttä ja pääsyä määriteltyyn ***digna***-repositorioonsa. Tämä komento varmistaa, että CLI pystyy kommunikoimaan repositorion kanssa.
      
### Komennon käyttö
```bash
dignacli check-repo-connection
```

Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tietoja repositoriosta: repositoryn version, isännän, tietokannan ja skeeman.  
  
Jos repositorion yhteys epäonnistuu, tarkista config.toml-tiedosto oikeiden asetusten varmistamiseksi.

## Käyttö: `version`-komento

Asennetun *dignacli*-version tarkistamiseen käytä --version-vaihtoehtoa.  
  
### Komennon käyttö
```bash
dignacli --version
```
  
### Esimerkkituloste
```bash
dignacli version 2024.11
```

## Lokitusvaihtoehdot
  
Oletuksena ***digna***-komentojen konsolituloste on minimalistinen. Useimmissa komennoissa on mahdollisuus saada lisätietoja seuraavilla vaihtoehdoilla:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” ja ”debug” määrittävät yksityiskohtaisuustason, kun taas ”logfile”-kytkin mahdollistaa tulosteen uudelleenohjauksen tiedostoon konsolin sijaan.

# Käyttäjien hallinta

## Käyttö: `add-user`-komento
  
`add-user`-komentoa käytetään lisäämään uusi käyttäjä ***digna***-järjestelmään.
  
### Komennon käyttö
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentit

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

### Vaihtoehdot

- `--is_superuser`, `-su`: Valitsin, jolla uusi käyttäjä voidaan merkitä ylläpitäjäksi.
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivämäärän muodossa `YYYY-MM-DD HH:MI:SS`. Jos tätä ei aseteta, tilillä ei ole vanhenemispäivää.

### Esimerkki

Lisätäksesi uuden käyttäjän, jonka käyttäjätunnus on `jdoe`, koko nimi `John Doe` ja salasana `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lisätäksesi uuden käyttäjän ja asettaaksesi tilin vanhenemispäivän:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Käyttö: `delete-user`-komento
  
`delete-user`-komento poistaa olemassa olevan käyttäjän ***digna***-järjestelmästä.
  
### Komennon käyttö
```bash
dignacli delete-user USER_NAME
```
  
### Argumentit
- **USER_NAME**: Poistettavan käyttäjän käyttäjätunnus (pakollinen). Tämä on komennon ainoa vaadittu argumentti.

### Esimerkki
```bash
dignacli delete-user jdoe
```
  
Tämän komennon suorittaminen poistaa käyttäjän `jdoe` ***digna***-järjestelmästä, peruuttaa pääsyn ja poistaa käyttäjän liittyvät tiedot ja oikeudet repositoriosta.

## Käyttö: `modify-user`-komento

`modify-user`-komennolla päivitetään olemassa olevan käyttäjän tiedot ***digna***-järjestelmässä.

### Komennon käyttö
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentit
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Käyttäjän uusi koko nimi (pakollinen).
  
### Vaihtoehdot  
  
- `--is_superuser`, `-su`: Asettaa käyttäjän superkäyttäjäksi, mikä antaa korotetut oikeudet. Tämä lippu ei vaadi arvoa.  
- `--valid_until`, `-vu`: Asettaa käyttäjätilin vanhenemispäivämäärän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei anneta, tili pysyy voimassa toistaiseksi.  
  
### Esimerkki
  
Muokataksesi käyttäjän `jdoe` koko nimeä muotoon ”Johnathan Doe” ja asettaaksesi käyttäjän superkäyttäjäksi:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Käyttö: `modify-user-pwd`-komento
  
`modify-user-pwd`-komennolla vaihdetaan olemassa olevan käyttäjän salasana ***digna***-järjestelmässä.
  
### Komennon käyttö
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentit
  
- **USER_NAME**: Sen käyttäjän käyttäjätunnus, jonka salasana vaihdetaan (pakollinen).
- **USER_PWD**: Uusi salasana käyttäjälle (pakollinen).
  
### Esimerkki
  
Vaihda käyttäjän `jdoe` salasana muotoon `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Käyttö: `list-users`-komento

`list-users`-komento näyttää kaikki järjestelmään rekisteröidyt käyttäjät.

### Komennon käyttö

```bash
dignacli list-users
```

Tämän komennon suorittaminen yhdistää ***digna***-repositorioon ja listaa kaikki käyttäjät, näyttäen niiden ID:n, käyttäjätunnuksen, koko nimen, superkäyttäjästatuksen ja vanhenemisaikaleimat.

# Repositorion hallinta

### Käyttö: `upgrade-repo`-komento
  
`upgrade-repo`-komentoa käytetään päivittämään tai alustamaan ***digna***-repositorio. Tämä komento on olennainen päivitysten soveltamiseen tai repositorion infrastruktuurin luomiseen ensimmäistä kertaa.
  
### Komennon käyttö

```bash
dignacli upgrade-repo [options]
```
  
### Vaihtoehdot
  
- `--simulation-mode`, `-s`: Kun käytössä, komento ajetaan simulaatiotilassa, joka tulostaa SQL-lauseet, jotka aiottaisiin suorittaa, mutta ei itse suorita niitä. Tämä on hyödyllinen muutosten esikatseluun ilman repositorion muokkaamista.  

  
### Esimerkki
  
Repositorion päivittämiseksi voi ajaa komennon ilman vaihtoehtoja:
  
```bash
dignacli upgrade-repo
```  
Ajaaksesi päivityksen simulaatiotilassa (näet SQL-lauseet ilman niiden soveltamista):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Tämä komento on tärkeä ***digna***-järjestelmän ylläpidossa, varmistaen, että tietokannan skeema ja muut repositorion komponentit ovat ajan tasalla ohjelmiston uusimman version kanssa.

## Käyttö: `encrypt`-komento
  
`encrypt`-komennolla salataan salasana.
  
### Komennon käyttö
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentit
- **PASSWORD**: Salasana, joka halutaan salata (pakollinen).
  
### Esimerkki
  
Salataksesi salasanan, anna se argumenttina.  
Esimerkiksi salataksesi salasanan `mypassword123`, käytä:
```bash
dignacli encrypt mypassword123
```
Komento tulostaa annetun salasanan salatun version, jota voidaan käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI näyttää virheilmoituksen puuttuvasta argumentista.

## Käyttö: `generate-key`-komento
  
`generate-key`-komennolla luodaan Fernet-avain, joka on välttämätön salasanojen suojaamiseen tallennettaessa niitä ***digna***-repositoriossa.
  
### Komennon käyttö
```bash
dignacli generate-key
```
  
# Datan hallinta

## Käyttö: `clean-up`-komento

`clean-up`-komennolla poistetaan profiileja, ennusteita ja Traffic Light System -dataa yhdeltä tai useammalta tietolähteeltä määritellyssä projektissa. Tämä komento on tärkeä datan elinkaaren hallinnassa ja auttaa ylläpitämään järjestystä ja tehokkuutta poistamalla vanhentunutta tai tarpeetonta dataa.

### Komennon käyttö

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, josta data poistetaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa ***digna*** iteroi kaikkien olemassa olevien projektien läpi ja suorittaa komennon niille.
- **FROM_DATE**: Datan poistamisen aloituspäivä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan poistamisen päättymispäivä ja -aika, samaa muotoa kuin FROM_DATE (pakollinen).
  
### Vaihtoehdot
  
- `--table-name`, `-tn`: Rajoittaa clean-up-operaation tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa clean-upin tauluihin, joiden nimissä esiintyy annettu alimerkkijono.
- `--timing`, `-tm`: Näyttää clean-up-prosessin keston suorituksen jälkeen.
- `--help`: Näyttää clean-up-komennon ohjeet ja poistuu.
  
### Esimerkki
  
Poistaaksesi dataa projektista ProjectA ajalta 1. tammikuuta 2023 — 30. kesäkuuta 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Poistaaksesi dataa vain tietystä taulusta nimeltä `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Tämä komento auttaa hallitsemaan tallennustilaa ja varmistamaan, että repositoriossa säilytetään vain relevanttia tietoa.

## Käyttö: `inspect`-komento

`inspect`-komennolla luodaan profiileja, ennusteita ja Traffic Light System -dataa yhdeltä tai useammalta tietolähteeltä määritellyssä projektissa. Tämä komento auttaa analysoimaan ja seuraamaan dataa määritellyn ajanjakson aikana.

### Komennon käyttö

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jota tutkitaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa ***digna*** iteroi kaikkien olemassa olevien projektien läpi ja suorittaa komennon niille.
- **FROM_DATE**: Datan tarkastelun aloituspäivä ja -aika. Hyväksytyt muodot ovat %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan tarkastelun päättymispäivä ja -aika, samaa muotoa kuin FROM_DATE (pakollinen).
  
### Vaihtoehdot

- `--table-name`, `-tn`: Rajoittaa tarkastelun tiettyyn tauluun projektissa.
- `--table-filter`, `-tf`: Suodattaa tarkastelun tauluihin, joiden nimissä esiintyy annettu alimerkkijono.
- `--do-profile`: Käynnistää profiilien uudelleenkokoelun. Oletusarvo on do-profile.
- `--no-do-profile`: Estää profiilien uudelleenkokoelun.
- `--do-prediction`: Käynnistää ennusteiden uudelleenlaskennan. Oletusarvo on do-prediction.
- `--no-do-prediction`: Estää ennusteiden uudelleenlaskennan.
- `--do-alert-status`: Käynnistää hälytystilojen uudelleenlaskennan. Oletusarvo on do-alert-status.
- `--no-do-alert-status`: Estää hälytystilojen uudelleenlaskennan.
- `--timing`, `-tm`: Näyttää tarkasteluprosessin keston suorituksen jälkeen.
  
### Esimerkki
  
Tarkasta dataa projektista `ProjectA` ajalta 1. tammikuuta 2024 — 31. tammikuuta 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Tarkasta vain tietty taulu ja pakota ennusteiden uudelleenlaskenta:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden luomiseen, datan eheyden valvontaan ja hälytysjärjestelmän hallintaan määritellyllä aikavälillä.

## Käyttö: `tls-status`-komento

`tls-status`-komennolla kysytään Traffic Light Systemin (TLS) tila tietylle taululle projektissa tiettynä päivänä. Traffic Light System tarjoaa näkymän datan kunnosta ja laadusta, ja osoittaa mahdolliset ongelmat tai hälytykset, jotka vaativat toimenpiteitä.
  
### Komennon käyttö
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentit
  
- **PROJECT_NAME**: Projektin nimi, jolle TLS-tila kysytään (pakollinen).
- **TABLE_NAME**: Tietty taulu projektissa, jota tilatarkastus koskee (pakollinen).
- **DATE**: Päivä, jolle TLS-tila kysytään, yleensä muodossa %Y-%m-%d (pakollinen).
  
### Esimerkki
  
Tarkista TLS-tila taululle UserData projektissa ProjectA päivälle 1. heinäkuuta 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Tämä komento auttaa käyttäjiä seuraamaan ja ylläpitämään datan laatua tarjoamalla selkeän ja toimintakelpoisen tilaraportin ennalta määriteltyjen kriteerien perusteella.

## Käyttö: `list-projects`-komento
  
`list-projects`-komento näyttää listan kaikista saatavilla olevista projekteista ***digna***-järjestelmässä.
  
### Komennon käyttö
  
```bash
dignacli list-projects
```

Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja, tarjoten nopean yleiskuvan repositorion saatavilla olevista projekteista.

## Käyttö: `list-ds`-komento

`list-ds`-komennolla listataan kaikki tietolähteet tietyssä projektissa. Tämä komento on hyödyllinen, kun halutaan ymmärtää analysoitavissa ja hallittavissa olevia dataresursseja ***digna***-järjestelmässä.

### Komennon käyttö
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentit
- **PROJECT_NAME**: Projektin nimi, jolle tietolähteet listataan (pakollinen).
  
### Esimerkki
  
Listataksesi kaikki tietolähteet projektista `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Tämä komento antaa käyttäjille yleiskuvan projektin saatavilla olevista tietolähteistä ja auttaa navigoimaan ja hallitsemaan data-arkkitehtuuria tehokkaammin.