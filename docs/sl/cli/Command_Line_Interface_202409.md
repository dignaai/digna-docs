---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## Osnove CLI

---

###   help

Možnost --help zagotavlja informacije o razpoložljivih ukazih in njihovem uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite –help takoj za ključnim besedam ***digna***cl  
   bash
   dignacli --help

3.  **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu pripnite --help k temu ukazu.
    Na primer, za pomoč pri ukazu add-user zaženite:
     bash
     dignacli add-user --help
     

     ### izhod:
      
     - **Opis ukaza:** Ponuja podroben opis, kaj ukaz počne.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in izbirnimi argumenti.  
     - **Možnosti:** Navedene so vse možnosti, specifične za ukaz, skupaj z njihovimi pojasnili.  
     - **Primeri:** Ponuja primere, kako učinkovito izvesti ukaz.

  
###   check-repo-connection

Ukaz check-repo-connection je utilita znotraj orodja ***digna*** CLI, namenjena testiranju povezljivosti in dostopa do določenega ***digna*** repozitorija. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
##### Uporaba ukaza
bash
dignacli check-repo-connection


Ob uspešni izvedbi ukaz izpiše potrditev povezave skupaj s podrobnostmi o repozitoriju: različica repozitorija, gostitelj, baza podatkov in shema.  
  
Če povezava do repozitorija ni uspešna, preverite datoteko config.toml glede pravilnih nastavitev konfiguracije.

###   version

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Uporaba ukaza
bash
dignacli --version

  
#### Primer izhoda
bash
dignacli version 2024.09


###   možnosti beleženja (logging)
  
Privzeto je izpis v konzoli pri ukazih ***digna*** zasnovan minimalistično. Večina ukazov ponuja možnost izpisati dodatne informacije z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” in “debug” določata raven podrobnosti, medtem ko omogoča preklop “logfile” preusmeritev izpisa v datoteko namesto v konzolo.

## Upravljanje uporabnikov

###   add-user
  
Ukaz add-user v ***digna*** CLI se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenti

- **USER_NAME**: uporabniško ime za novega uporabnika (obvezno).
- **USER_FULL_NAME**: polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: geslo za novega uporabnika (obvezno).

#### Možnosti

- --is_superuser, -su: Preklop za dodelitev novega uporabnika kot superuporabnika.
- --valid_until, -vu: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni nastavljen, račun nima datuma poteka.

#### Primer

Za dodajanje novega uporabnika z uporabniškim imenom jdoe, polnim imenom John Doe in geslom password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Za dodajanje novega uporabnika in nastavitev datuma poteka računa:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Ukaz delete-user v ***digna*** CLI se uporablja za odstranitev obstoječega uporabnika iz sistema ***digna***.
  
##### Uporaba ukaza
bash
dignacli delete-user USER_NAME

  
#### Argumenti
- **USER_NAME**: uporabniško ime uporabnika, ki naj bo izbrisan (obvezno). To je edini obvezen argument ukaza.

#### Primer
bash
dignacli delete-user jdoe

  
Izvedba tega ukaza bo odstranila uporabnika jdoe iz sistema ***digna***, odvzela njegov dostop in izbrisala pripadajoče podatke ter dovoljenja iz repozitorija.

###   modify-user

Ukaz modify-user v ***digna*** CLI se uporablja za posodobitev podatkov obstoječega uporabnika v sistemu ***digna***.

##### Uporaba ukaza
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenti
  
- **USER_NAME**: uporabniško ime uporabnika, ki ga želimo spremeniti (obvezno).
- **USER_FULL_NAME**: novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- --is_superuser, -su: Nastavi uporabnika kot superuporabnika, s tem podeli povišane pravice. Ta preklop ne zahteva vrednosti.  
- --valid_until, -vu: Nastavi datum poteka uporabniškega računa v formatu YYYY-MM-DD HH:MI:SS. Če ni naveden, račun ostane veljaven neomejeno.  
  
#### Primer
  
Za spremembo polnega imena uporabnika jdoe v “Johnathan Doe” in nastavitev uporabnika kot superuporabnika:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Ukaz modify-user-pwd v ***digna*** CLI se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
##### Uporaba ukaza
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenti
  
- **USER_NAME**: uporabniško ime uporabnika, katerega geslo se spreminja (obvezno).
- **USER_PWD**: novo geslo za uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika jdoe v newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Ukaz list-users v ***digna*** CLI prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

##### Uporaba ukaza

bash
dignacli list-users


Izvedba tega ukaza v ***digna*** CLI se bo povezala z ***digna*** repozitorijem in izpisala vse uporabnike, prikazala njihove ID-je, uporabniška imena, polna imena, status superuporabnika ter časovne žige poteka.

# Upravljanje repozitorija

###   upgrade-repo
  
Ukaz upgrade-repo v ***digna*** CLI se uporablja za nadgradnjo ali inicializacijo ***digna*** repozitorija. Ta ukaz je ključnega pomena za uporabo posodobitev ali prvotno nastavitev repozitorijske infrastrukture.
  
#### Uporaba ukaza

bash
dignacli upgrade-repo [options]

  
#### Možnosti
  
- --simulation-mode, -s: Ko je omogočeno, ta možnost zažene ukaz v simulacijskem načinu, ki izpiše SQL izjave, ki bi bile izvršene, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez dejanskih sprememb v repozitoriju.  

  
#### Primer
  
Za nadgradnjo ***digna*** repozitorija lahko zaženete ukaz brez dodatnih možnosti:
  
bash
dignacli upgrade-repo
  
Za zagon nadgradnje v simulacijskem načinu (da si ogledate SQL izjave brez njihove uporabe):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ta ukaz je ključnega pomena za vzdrževanje sistema ***digna*** in zagotavlja, da sta shema podatkovne baze in drugi repozitorijski komponenti posodobljeni z najnovejšo različico programske opreme.

###   encrypt
  
Ukaz encrypt v ***digna*** CLI se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenti
- **PASSWORD**: geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate geslo posredovati kot argument.   
Na primer, za šifriranje gesla mypassword123 bi uporabili:
bash
dignacli encrypt mypassword123

Ta ukaz izpiše šifrirano različico posredovanega gesla, ki se nato lahko uporabi v varnih kontekstih. Če argument gesla ni predan, bo CLI prikazal napako o manjkajočem argumentu.

###   generate-key
  
Ukaz generate-key se uporablja za generiranje Fernet ključa, ki je bistven za zaščito gesel, shranjenih v ***digna*** repozitoriju.
  
#### Uporaba ukaza
bash
dignacli generate-key

  
## Upravljanje podatkov

###   clean-up

Ukaz clean-up v ***digna*** CLI se uporablja za odstranjevanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz je bistven za upravljanje življenjskega cikla podatkov in pomaga vzdrževati urejeno in učinkovito podatkovno okolje z brisanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: ime projekta, iz katerega naj bodo podatki odstranjeni (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira preko vseh obstoječih projektov in uporabi ta ukaz.
- **FROM_DATE**: začetni datum in čas za odstranjevanje podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za odstranjevanje podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti
  
- --table-name, -tn: Omeji operacijo čiščenja na določeno tabelo znotraj projekta.
- --table-filter, -tf: Filtrira in omeji čiščenje na tabele, ki v imenu vsebujejo določen podniz.
- --timing, -tm: Po zaključku prikaže trajanje procesa čiščenja.
- --help: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Za odstranitev podatkov samo iz določene tabele z imenom Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ta ukaz pomaga pri upravljanju shrambe podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

###   inspect

Ukaz inspect v ***digna*** CLI se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči za enega ali več virov podatkov znotraj določenega projekta. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem časovnem obdobju.

#### Uporaba ukaza

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: ime projekta, za katerega naj bodo podatki pregledani (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira preko vseh obstoječih projektov in uporabi ta ukaz.
- **FROM_DATE**: začetni datum in čas za pregled podatkov. Sprejemljivi formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: končni datum in čas za pregled podatkov, v enakih formatih kot FROM_DATE (obvezno).
  
#### Možnosti

- --table-name, -tn: Omeji pregled na določeno tabelo znotraj projekta.
- --table-filter, -tf: Filtrira in pregleda le tabele, ki v imenu vsebujejo določen podniz.
- --force-profile: Prisili ponovno zbiranje profilov. Privzeto je force-profile.
- --no-force-profile: Prepreči ponovno zbiranje profilov.
- --force-prediction: Prisili ponovno izračun napovedi. Privzeto je force-prediction.
- --no-force-prediction: Prepreči ponovno izračun napovedi.
- --force-alert-status: Prisili ponovno izračun statusov opozoril. Privzeto je force-alert-status.
- --no-force-alert-status: Prepreči ponovno izračun statusov opozoril.
- --timing, -tm: Po zaključku prikaže trajanje postopka pregledovanja.
- --alert-notification, -an: Pošlje obvestila o opozorilih na naročene kanale.
  
#### Primer
  
Za pregled podatkov za projekt ProjectA od 1. januarja 2024 do 31. januarja 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Za pregled samo določene tabele in prisilni ponovni izračun napovedi:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistema opozoril v določenem časovnem okviru projekta.

###   tls-status

Ukaz tls-status v ***digna*** CLI se uporablja za poizvedbo o stanju Traffic Light System (TLS) za določeno tabelo v projektu na določen datum. Traffic Light System nudi vpogled v zdravje in kakovost podatkov ter označuje morebitne težave ali opozorila, ki potrebujejo pozornost.
  
#### Uporaba ukaza
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenti
  
- **PROJECT_NAME**: ime projekta, za katerega se poizveduje stanje TLS (obvezno).
- **TABLE_NAME**: določena tabela znotraj projekta, za katero je potrebno stanje TLS (obvezno).
- **DATE**: datum, za katerega se poizveduje stanje TLS, običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje stanja TLS za tabelo z imenom UserData v projektu ProjectA na 1. julij 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov z zagotavljanjem jasnega in ukrepnega poročila o stanju na podlagi vnaprej določenih kriterijev.

###   list-projects
  
Ukaz list-projects v ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
bash
dignacli list-projects


Ta ukaz je posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov, saj ponuja hiter pregled razpoložljivih projektov v ***digna*** repozitoriju.

###   list-ds

Ukaz list-ds v ***digna*** CLI se uporablja za prikaz seznama vseh razpoložljivih virov podatkov znotraj določenega projekta. Ta ukaz je koristen za razumevanje podatkovnih sredstev, ki so na voljo za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenti
- **PROJECT_NAME**: ime projekta, za katerega se navajajo viri podatkov (obvezno).
  
#### Primer
  
Za prikaz vseh virov podatkov v projektu z imenom ProjectA:
  
bash
dignacli list-ds ProjectA

  
Ta ukaz uporabnikom nudi pregled virov podatkov, ki so na voljo v projektu, s čimer jim pomaga pri navigaciji in učinkovitejšem upravljanju podatkovnega okolja.