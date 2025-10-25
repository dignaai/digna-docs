---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## Osnove CLI

---

###   help

Možnost --help prikazuje informacije o razpoložljivih ukazih in o tem, kako jih uporabljati. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ključnimi besedami ***digna***cl  
   bash
   dignacli --help

3.  **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte --help za tem ukazom.
    Na primer, za pomoč pri ukazu add-user zaženite:
     bash
     dignacli add-user --help
     

     ### izpis:
      
     - **Opis ukaza:** Ponuja podroben opis, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z zahtevanimi in izbirnimi argumenti.  
     - **Možnosti:** Navedeni so morebitni preklopi, ki so specifični za ukaz, skupaj z razlagami.  
     - **Primeri:** Ponuja primere, kako ukaz učinkovito uporabiti.

  
###   check-repo-connection

Ukaz check-repo-connection v CLI-ju ***digna*** je orodje, namenjeno preverjanju povezave in dostopa do določenega ***digna*** repositoryja. Ta ukaz zagotavlja, da lahko CLI komunicira z repositoryjem.
      
##### Uporaba ukaza
bash
dignacli check-repo-connection


Ob uspešnem izvajanju ukaz potrdi povezavo in izpiše podrobnosti o repositoryju: Repository version, Host, Database in Schema.  
  
Če povezava do repositoryja ne uspe, preverite datoteko config.toml za pravilne konfiguracijske nastavitve.

###   version

Za preverjanje, katera različica *dignacli* je nameščena, uporabite možnost --version.  
  
#### Uporaba ukaza
bash
dignacli --version

  
#### Primer izpisa
bash
dignacli version 2024.09


###   logging options
  
Privzeto je izpis v konzolo ukazov ***digna*** zasnovan minimalistično. Večina ukazov omogoča prikaz več informacij z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
«verbose» in «debug» določata raven podrobnosti, medtem ko preklop «logfile» omogoči preusmeritev izhoda v datoteko namesto na konzolo.

## Upravljanje uporabnikov

###   add-user
  
Ukaz add-user v CLI-ju ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenti

- **USER_NAME**: Uporniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- --is_superuser, -su: Preklop za dodelitev administratorskih pravic novemu uporabniku.
- --valid_until, -vu: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni nastavljen, račun nima datuma poteka.

#### Primer

Za dodajanje novega uporabnika z uporabniškim imenom jdoe, polnim imenom John Doe in geslom password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Za dodajanje novega uporabnika in nastavitev datuma poteka računa:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Ukaz delete-user v CLI-ju ***digna*** se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
##### Uporaba ukaza
bash
dignacli delete-user USER_NAME

  
#### Argumenti
- **USER_NAME**: Uporniško ime uporabnika, ki naj bo izbrisan (obvezno). To je edini argument, ki ga ukaz zahteva.

#### Primer
bash
dignacli delete-user jdoe

  
Z izvajanjem tega ukaza se uporabnik jdoe odstrani iz sistema ***digna***, njegova dostopna prava in povezani podatki v repositoryju pa se odstranijo.

###   modify-user

Ukaz modify-user v CLI-ju ***digna*** se uporablja za posodabljanje podatkov obstoječega uporabnika v sistemu ***digna***.

##### Uporaba ukaza
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, ki ga je treba spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- --is_superuser, -su: Nastavi uporabnika kot superuserja in mu dodeli povišane privilegije. Ta preklop ne zahteva vrednosti.  
- --valid_until, -vu: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven za nedoločen čas.  
  
#### Primer
  
Za spremembo polnega imena uporabnika jdoe v «Johnathan Doe» in nastavitev uporabnika kot superuser:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Ukaz modify-user-pwd v CLI-ju ***digna*** se uporablja za spreminjanje gesla obstoječega uporabnika v sistemu ***digna***.
  
##### Uporaba ukaza
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenti
  
- **USER_NAME**: Uporniško ime uporabnika, katerega geslo se spreminja (obvezno).
- **USER_PWD**: Novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika jdoe v newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Ukaz list-users v CLI-ju ***digna*** prikaže seznam vseh uporabnikov registriranih v sistemu ***digna***.

##### Uporaba ukaza

bash
dignacli list-users


Ko zaženete ta ukaz v CLI-ju ***digna***, se poveže z ***digna*** repositoryjem in prikaže vse uporabnike z njihovimi ID-ji, uporabniškimi imeni, polnimi imeni, statusom superuserja in datumi poteka.

# Upravljanje repositoryja

###   upgrade-repo
  
Ukaz upgrade-repo v CLI-ju ***digna*** se uporablja za nadgradnjo ali inicializacijo ***digna*** repositoryja. Ta ukaz je bistven za uporabo posodobitev ali vzpostavitev infrastrukture repositoryja prvič.
  
#### Uporaba ukaza

bash
dignacli upgrade-repo [options]

  
#### Možnosti
  
- --simulation-mode, -s: Ko je vključen, ukaz deluje v načinu simulacije, izpiše SQL poizvedbe, ki bi bile izvedene, vendar jih ne izvede. To je uporabno za predogled sprememb brez dejanskega spreminjanja repositoryja.  

  
#### Primer
  
Za nadgradnjo ***digna*** repositoryja lahko zaženete ukaz brez dodatnih možnosti:
  
bash
dignacli upgrade-repo
  
Za zagon nadgradnje v načinu simulacije (za ogled SQL poizvedb brez njihove uporabe):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ta ukaz je pomemben za vzdrževanje sistema ***digna*** in zagotavlja, da je shema baze podatkov in druge komponente repositoryja posodobljene v skladu z najnovejšo različico programske opreme.

###   encrypt
  
Ukaz encrypt v CLI-ju ***digna*** se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenti
- **PASSWORD**: Geslo, ki ga želite šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate geslo podati kot argument.   
Na primer, za šifriranje gesla mypassword123 bi uporabili:
bash
dignacli encrypt mypassword123

Ta ukaz vrne šifrirano različico podanega gesla, ki jo lahko nato uporabite v varnih kontekstih. Če argument gesla ni podan, bo CLI izpisal sporočilo o napaki, ki opozarja na manjkajoči argument.

###   generate-key
  
Ukaz generate-key se uporablja za generiranje Fernet-ključa, ki je pomemben za zaščito gesel, shranjenih v ***digna*** repositoryju.
  
#### Uporaba ukaza
bash
dignacli generate-key

  
## Obdelava podatkov

###   clean-up

Ukaz clean-up v CLI-ju ***digna*** se uporablja za odstranjevanje profilov, napovedi in podatkov iz sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga ohranjati organiziran in učinkovit obseg podatkov z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega želite odstraniti podatke (obvezno). Če v tem argumentu uporabite ključni izraz all-projects, ukažete ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas čiščenja podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas čiščenja podatkov, s istimi formati kot FROM_DATE (obvezno).
  
#### Možnosti
  
- --table-name, -tn: Omeji operacijo clean-up na določeno tabelo v projektu.
- --table-filter, -tf: Filtrira tako, da clean-up vključuje le tabele, katerih ime vsebuje podano podniz.
- --timing, -tm: Prikaže trajanje procesa clean-up po zaključku.
- --help: Prikaže pomoč za ukaz clean-up in zapre.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Za odstranitev podatkov samo iz določene tabele z imenom Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ta ukaz pomaga upravljati shranjevanje podatkov in zagotavlja, da repository vsebuje le relevantne informacije.

###   inspect

Ukaz inspect v CLI-ju ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov za sistem prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga analizirati in spremljati podatke v določenem časovnem obdobju.

#### Uporaba ukaza

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega želite izvesti inšpekcijo podatkov (obvezno). Če v tem argumentu uporabite ključni izraz all-projects, ukažete ***digna***, naj iterira skozi vse obstoječe projekte in uporabi ta ukaz.
- **FROM_DATE**: Začetni datum in čas inšpekcije. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas inšpekcije, s istimi formati kot FROM_DATE (obvezno).
  
#### Možnosti

- --table-name, -tn: Omeji inšpekcijo na določeno tabelo v projektu.
- --table-filter, -tf: Filtrira tako, da se inšpektirajo samo tabele, katerih ime vsebuje podano podniz.
- --force-profile: Prisili ponovno zbiranje profilov. Privzeto je force-profile.
- --no-force-profile: Onemogoči ponovno zbiranje profilov.
- --force-prediction: Prisili ponovno izračunavanje napovedi. Privzeto je force-prediction.
- --no-force-prediction: Onemogoči ponovno izračunavanje napovedi.
- --force-alert-status: Prisili ponovno izračunavanje statusa opozoril. Privzeto je force-alert-status.
- --no-force-alert-status: Onemogoči ponovno izračunavanje statusa opozoril.
- --timing, -tm: Prikaže trajanje procesa inšpekcije po zaključku.
- --alert-notification, -an: Pošlje obvestila o opozorilih na prijavljene kanale.
  
#### Primer
  
Za inšpekcijo podatkov za projekt ProjectA od 1. januarja 2024 do 31. januarja 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Za inšpekcijo samo določene tabele in prisilno ponovno izračunavanje napovedi:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje celovitosti podatkov in upravljanje sistema opozoril v določenem časovnem okviru projekta.

###   tls-status

Ukaz tls-status v CLI-ju ***digna*** se uporablja za poizvedbo o stanju sistema prometnih luči (TLS) za določeno tabelo v projektu na določen datum. Sistem prometnih luči daje vpogled v kakovost in zdravje podatkov ter označuje morebitne težave ali opozorila, ki zahtevajo pozornost.
  
#### Uporaba ukaza
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se zahteva status TLS (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero se zahteva status TLS (obvezno).
- **DATE**: Datum, za katerega se poizveduje status TLS, običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje TLS-statusa tabele z imenom UserData v projektu ProjectA na 1. julij 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z zagotavljanjem jasnega in ukrepanja vrednega poročila o stanju na podlagi vnaprej definiranih kriterijev.

###   list-projects
  
Ukaz list-projects v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
bash
dignacli list-projects


Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj nudi hiter pregled razpoložljivih projektov v ***digna*** repositoryju.

###   list-ds

Ukaz list-ds v CLI-ju ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov znotraj določenega projekta. Ta ukaz je koristen za pregled virov podatkov, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega se izpišejo viri podatkov (obvezno).
  
#### Primer
  
Za izpis vseh virov podatkov v projektu z imenom ProjectA:
  
bash
dignacli list-ds ProjectA

  
Ta ukaz uporabnikom nudi pregled virov podatkov, ki so na voljo v projektu, in jim pomaga učinkoviteje navigirati ter upravljati podatkovno okolje.