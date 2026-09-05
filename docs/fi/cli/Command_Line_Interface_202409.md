---
title: digna CLI - Viite 2024.09 – Komennot & Esimerkit | digna Dokumentaatio
description: Täydellinen viite digna CLI -julkaisulle 2024.09. Opi hallitsemaan käyttäjiä, repositorioita ja dataa komennoilla kuten add-user, check-repo-connection, upgrade-repo, inspect, tls-status ja lisää.
image: /assets/logo_square.png
---

# digna CLI - Viite 2024.09
**2024-08-24**

---

## CLI:n perusteet

---

### help

--help -valinta näyttää tietoa saatavilla olevista komennoista ja niiden käytöstä. Tätä vaihtoehtoa voi käyttää kahdella pääasiallisella tavalla:

1. **Yleisen ohjeen näyttäminen:**
   
    Käytä –help heti avainsanan ***digna***cl jälkeen  
   bash
   dignacli --help

3.  **Ohje tietylle komennolle:**  
  
    Jos haluat yksityiskohtaisia tietoja tietystä komennosta, lisää --help kyseisen komennon perään.
    Esimerkiksi saadaksesi ohjeen add-user-komennosta, suorita:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Komennon kuvaus:** Tarjoaa yksityiskohtaisen kuvauksen siitä, mitä komento tekee.  
     - **Syntaksi:** Näyttää tarkan syntaksin, mukaan lukien pakolliset ja valinnaiset argumentit.  
     - **Valinnat:** Listaa komennolle ominaiset valinnat ja niiden selitykset.  
     - **Esimerkit:** Antaa esimerkkejä, miten komentoa suoritetaan käytännössä.

  
### check-repo-connection

check-repo-connection-komento on apu***digna*** CLI -työkalussa, joka on tarkoitettu testaamaan yhteyttä ja pääsyä määritettyyn ***digna*** repositoryyn. Tämä komento varmistaa, että CLI pystyy kommunikoimaan repositorion kanssa.
      
##### Command Usage
bash
dignacli check-repo-connection


Onnistuneen suorituksen jälkeen komento tulostaa vahvistuksen yhteydestä sekä tietoja repositoriosta: Repository version, Host, Database and Schema.  
  
Jos repositorioon yhdistäminen epäonnistuu, tarkista config.toml -tiedosto oikeiden määritysten varmistamiseksi.

### version

Tarkista asennettu *dignacli*-versio käyttämällä --version -valintaa.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


### logging options
  
Oletusarvoisesti ***digna***-komentojen konsolitulostus on suunniteltu minimalistiseksi. Useimmissa komennoissa on mahdollisuus näyttää lisätietoja seuraavien valintojen avulla:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” ja ”debug” määrittävät yksityiskohtaisuustason, kun taas ”logfile” -kytkin mahdollistaa tulostuksen uudelleenohjauksen tiedostoon konsolin sijaan.

## Käyttäjähallinta

### add-user
  
add-user-komentoa käytetään lisäämään uusi käyttäjä ***digna***-järjestelmään.
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Uuden käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Uuden käyttäjän koko nimi (pakollinen).
- **USER_PASSWORD**: Uuden käyttäjän salasana (pakollinen).

#### Options

- --is_superuser, -su: Lipuke, jolla uusi käyttäjä merkitään ylläpitäjäksi.
- --valid_until, -vu: Asettaa käyttäjätilin vanhenemispäivämäärän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei aseteta, tilillä ei ole vanhenemispäivää.

#### Example

Lisätäksesi uuden käyttäjän käyttäjätunnuksella jdoe, koko nimellä John Doe ja salasanalla password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Lisätäksesi uuden käyttäjän ja asettaaksesi tilin vanhenemispäivän:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


### delete-user
  
delete-user-komentoa käytetään poistamaan olemassa oleva käyttäjä ***digna***-järjestelmästä.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: Poistettavan käyttäjän käyttäjätunnus (pakollinen). Tämä on komennon ainoa vaadittu argumentti.

#### Example
bash
dignacli delete-user jdoe

  
Tämän komennon suorittaminen poistaa käyttäjän jdoe ***digna***-järjestelmästä, peruuttaa tämän käyttöoikeudet ja poistaa siihen liittyvät tiedot ja oikeudet repositoriosta.

### modify-user

modify-user-komentoa käytetään päivittämään olemassa olevan käyttäjän tiedot ***digna***-järjestelmässä.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: Muokattavan käyttäjän käyttäjätunnus (pakollinen).
- **USER_FULL_NAME**: Käyttäjän uusi koko nimi (pakollinen).
  
#### Options  
  
- --is_superuser, -su: Asettaa käyttäjän superkäyttäjäksi, antaen laajennetut oikeudet. Tämä lipuke ei vaadi arvoa.  
- --valid_until, -vu: Asettaa käyttäjätilin vanhenemispäivän muodossa YYYY-MM-DD HH:MI:SS. Jos tätä ei anneta, tili pysyy voimassa toistaiseksi.  
  
#### Example
  
Muokataksesi käyttäjä jdoe:n koko nimeksi ”Johnathan Doe” ja asettaaksesi käyttäjän superkäyttäjäksi:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


### modify-user-pwd
  
modify-user-pwd-komentoa käytetään muuttamaan olemassa olevan käyttäjän salasanaa ***digna***-järjestelmässä.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: Sen käyttäjän käyttäjätunnus, jonka salasana vaihdetaan (pakollinen).
- **USER_PWD**: Uusi salasana käyttäjälle (pakollinen).
  
#### Example
  
Vaihda käyttäjä jdoe:n salasana uudeksi newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


### list-users

list-users-komento näyttää luettelon kaikista ***digna***-järjestelmään rekisteröidyistä käyttäjistä.

##### Command Usage

bash
dignacli list-users


Tämän komennon suorittaminen yhdistää ***digna***-repositorioon ja listaa kaikki käyttäjät, näyttäen niiden ID:n, käyttäjätunnuksen, koko nimen, superkäyttäjästatuksen ja vanhenemisaikapisteet.

# Repositorion hallinta

### upgrade-repo
  
upgrade-repo-komentoa käytetään päivittämään tai alustamaan ***digna*** repository. Tämä komento on olennainen päivitysten soveltamiseksi tai repositorion infrastruktuurin ensimmäistä kertaa perustamiseksi.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Kun tämä on käytössä, komento suoritetaan simulaatiotilassa, joka tulostaa SQL-lauseet, jotka olisi suoritettu, mutta ei oikeasti aja niitä. Tämä on hyödyllistä muutosten esikatseluun ilman, että repositoriota muokataan.  

  
#### Example
  
Päivittääksesi ***digna***-repositorion voit ajaa komennon ilman valintoja:
  
bash
dignacli upgrade-repo
  
Ajaaksesi päivityksen simulaatiotilassa (näyttää SQL-lauseet ilman soveltamista):
  
bash
dignacli upgrade-repo --simulation-mode

  
Tämä komento on keskeinen ***digna***-järjestelmän ylläpidossa varmistaen, että tietokannan skeema ja muut repositorion komponentit ovat ajan tasalla ohjelmiston uusimman version kanssa.

### encrypt
  
encrypt-komentoa käytetään salakirjoittamaan salasana.
  
#### Command Usage
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD**: Salasana, joka halutaan salata (pakollinen).
  
#### Example
  
Salataksesi salasanan, anna salasana argumenttina.   
Esimerkiksi salataksesi salasanan mypassword123, käytä:
bash
dignacli encrypt mypassword123

Tämä komento tulostaa annettuun salasanaan perustuvan salatun version, jota voidaan käyttää turvallisissa yhteyksissä. Jos salasana-argumenttia ei anneta, CLI näyttää virheilmoituksen puuttuvasta argumentista.

### generate-key
  
generate-key-komentoa käytetään Fernet-avaimen luomiseen, joka on olennainen salasanojen suojaamiseksi ***digna***-repositoryssa.
  
#### Command Usage
bash
dignacli generate-key

  
## Datan hallinta

### clean-up

clean-up-komentoa käytetään poistamaan profiileja, ennusteita ja Traffic Light System -järjestelmän dataa yhdeltä tai useammalta tietolähteeltä määritetyssä projektissa. Tämä komento on tärkeä datan elinkaaren hallinnassa ja auttaa pitämään dataympäristön järjestettynä ja tehokkaana poistamalla vanhentunutta tai tarpeetonta dataa.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Projektin nimi, josta dataa poistetaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ohjataan ***digna*** käymään läpi kaikki olemassa olevat projektit ja soveltamaan komentoa niihin.
- **FROM_DATE**: Datan poistamisen aloituspäivämäärä ja -aika. Hyväksytyt muodot sisältävät %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Datan poistamisen lopetuspäivämäärä ja -aika, samaan tapaan kuin FROM_DATE (pakollinen).
  
#### Options
  
- --table-name, -tn: Rajoittaa clean-up-toiminnon tiettyyn tauluun projektin sisällä.
- --table-filter, -tf: Suodattaa siten, että puhdistus kohdistuu vain tauluihin, joiden nimissä esiintyy annettu alimerkkijono.
- --timing, -tm: Näyttää clean-up -prosessin keston suorituksen jälkeen.
- --help: Näyttää clean-up-komennon ohjetiedot ja poistuu.
  
#### Example
  
Poistaaksesi dataa projektista ProjectA ajanjaksolla 1. tammikuuta 2023–30. kesäkuuta 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Poistaaksesi dataa vain tietystä Table1-nimisestä taulusta:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Tämä komento auttaa hallitsemaan datan tallennusta ja varmistamaan, että repositoriossa säilytetään vain olennaista tietoa.

### inspect

inspect-komentoa käytetään luomaan profiileja, ennusteita ja Traffic Light System -dataa yhdelle tai useammalle tietolähteelle määritetyssä projektissa. Tämä komento auttaa analysoimaan ja seuraamaan dataa määritellyllä aikajaksolla.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Projektin nimi, jota varten dataa tarkastellaan (pakollinen). Käyttämällä avainsanaa all-projects tässä argumentissa, ohjataan ***digna*** käymään läpi kaikki olemassa olevat projektit ja soveltamaan komentoa niihin.
- **FROM_DATE**: Tarkastelun aloituspäivämäärä ja -aika. Hyväksytyt muodot sisältävät %Y-%m-%d, %Y-%m-%dT%H:%M:%S tai %Y-%m-%d %H:%M:%S (pakollinen).
- **TO_DATE**: Tarkastelun lopetuspäivämäärä ja -aika, samaan tapaan kuin FROM_DATE (pakollinen).
  
#### Options

- --table-name, -tn: Rajoittaa tarkastelun tiettyyn tauluun projektissa.
- --table-filter, -tf: Suodattaa niin, että tarkastus kohdistuu vain tauluihin, joiden nimissä esiintyy annettu alimerkkijono.
- --force-profile: Pakottaa profiilien uudelleenkokoamisen. Oletus on force-profile.
- --no-force-profile: Estää profiilien uudelleenkokoamisen.
- --force-prediction: Pakottaa ennusteiden uudelleenlaskennan. Oletus on force-prediction.
- --no-force-prediction: Estää ennusteiden uudelleenlaskennan.
- --force-alert-status: Pakottaa hälytystilojen uudelleenlaskennan. Oletus on force-alert-status.
- --no-force-alert-status: Estää hälytystilojen uudelleenlaskennan.
- --timing, -tm: Näyttää tarkastusprosessin keston suorituksen jälkeen.
- --alert-notification, -an: Lähettää hälytysviestit tilattuihin kanaviin.
  
#### Example
  
Tarkastellaksesi ProjectA-projektin dataa 1. tammikuuta 2024–31. tammikuuta 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Tarkastellaksesi vain tiettyä taulua ja pakottaaksesi ennusteiden uudelleenlaskennan:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Tämä komento on hyödyllinen päivitettyjen profiilien ja ennusteiden generoinnissa, datan eheyden seurannassa ja hälytysjärjestelmien hallinnassa määritellyn projektiajan puitteissa.

### tls-status

tls-status-komento kysyy Traffic Light Systemin (TLS) tilaa tietylle taululle projektissa tiettynä päivänä. Traffic Light System antaa näkemyksen datan kunnosta ja laadusta, ilmoittaen mahdollisista ongelmista tai hälytyksistä, jotka tarvitsevat huomiota.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Projektin nimi, jota TLS-tilan kysely koskee (pakollinen).
- **TABLE_NAME**: Tietty taulu projektissa, jonka TLS-tila halutaan (pakollinen).
- **DATE**: Päivä, jota varten TLS-tila kysytään, yleensä muodossa %Y-%m-%d (pakollinen).
  
#### Example
  
Tarkistaaksesi TLS-tilan UserData-nimiselle taululle projektissa ProjectA päivänä 1. heinäkuuta 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Tämä komento auttaa käyttäjiä seuraamaan ja ylläpitämään datalaatua tarjoamalla selkeän ja toimintaohjeiden mukaisen tilaraportin ennalta määriteltyjen kriteerien perusteella.

### list-projects
  
list-projects-komento näyttää luettelon kaikista saatavilla olevista projekteista ***digna***-järjestelmässä.
  
#### Command Usage
  
bash
dignacli list-projects


Tämä komento on erityisen hyödyllinen ylläpitäjille ja käyttäjille, jotka hallinnoivat useita projekteja, tarjoten nopean yleiskuvan repositoriossa olevista projekteista.

### list-ds

list-ds-komento näyttää luettelon kaikista saatavilla olevista tietolähteistä määritetyssä projektissa. Tämä komento on hyödyllinen, kun halutaan ymmärtää analysoitavat ja hallinnoitavat dataresurssit ***digna***-järjestelmässä.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Projektin nimi, jonka tietolähteet listataan (pakollinen).
  
#### Example
  
Listataksesi kaikki tietolähteet ProjectA-projektissa:
  
bash
dignacli list-ds ProjectA

  
Tämä komento antaa käyttäjille yleiskuvan projektin käytettävissä olevista tietolähteistä, auttaen navigoinnissa ja datamaailman hallinnassa.