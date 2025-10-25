---
title: digna CLI Referenca 2024.09 – Ukazi in primeri | digna Dokumentacija
description: Popolna referenca za digna CLI različico 2024.09. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi kot so add-user, check-repo-connection, upgrade-repo, inspect, tls-status in še več.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Referenca 2024.09
**2024-08-24**

---

## Osnove CLI

---

###   help

Možnost --help zagotavlja informacije o razpoložljivih ukazih in njihovi uporabi. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj za ukazom ***digna***  
   bash
   dignacli --help

3.  **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte --help k temu ukazu.  
    Na primer, za pomoč pri ukazu add-user zaženite:
     bash
     dignacli add-user --help
     

     ### izhod:
      
     - **Opis ukaza:** Podrobno pojasni, kaj ukaz naredi.  
     - **Sintaksa:** Prikaže popolno sintakso, vključno z obveznimi in neobveznimi argumenti.  
     - **Možnosti:** Našteje možnosti, specifične za ukaz, in njihove opise.  
     - **Primeri:** Ponuja primere, kako ukaz učinkovito zagnati.

  
###   check-repo-connection

Ukaz check-repo-connection je pomočnik v digna CLI, zasnovan za testiranje povezave in dostopa do določenega digna repozitorija. Ta ukaz preveri, ali lahko CLI komunicira z repozitorijem.
      
##### Uporaba ukaza
bash
dignacli check-repo-connection


Če je izvajanje uspešno, bo ukaz izpisal potrditev povezave in informacije o repozitoriju: Repository version, Host, Database in Schema.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml za pravilne nastavitve konfiguracije.

###   version

Uporabite možnost --version za preverjanje nameščene različice *dignacli*.  
  
#### Uporaba ukaza
bash
dignacli --version

  
#### Primer izhoda
bash
dignacli version 2024.09


###   logging options
  
Privzeto je izhod ukazov ***digna*** zasnovan minimalistično. Večina ukazov podpira dodatne informacije z uporabo naslednjih možnosti:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
Možnosti “verbose” in “debug” določajo raven podrobnosti, medtem ko ključ “logfile” preusmeri izhod v datoteko namesto na konzolo.

## Upravljanje uporabnikov

###   add-user
  
Ukaz add-user se uporablja za dodajanje novega uporabnika v digna sistem preko digna CLI.
  
#### Uporaba ukaza
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenti

- **USER_NAME**: Uporabniško ime novega uporabnika (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo novega uporabnika (obvezno).

#### Možnosti

- --is_superuser, -su: Preklopnik za označitev novega uporabnika kot upravitelja (superuser).
- --valid_until, -vu: Določi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni nastavljen, račun nima datuma poteka.

#### Primer

Da ustvarite novega uporabnika z uporabniškim imenom jdoe, polnim imenom John Doe in geslom password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Za dodajanje uporabnika in nastavitev datuma poteka računa:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Ukaz delete-user se uporablja za odstranitev obstoječega uporabnika iz digna sistema preko digna CLI.
  
##### Uporaba ukaza
bash
dignacli delete-user USER_NAME

  
#### Argumenti
- **USER_NAME**: Uporabniško ime uporabnika, ki ga je treba izbrisati (obvezno). To je edini zahtevan argument za ta ukaz.

#### Primer
bash
dignacli delete-user jdoe

  
Ob zagonu tega ukaza bo uporabnik jdoe odstranjen iz digna sistema, njegov dostop preklican in pripadajoči podatki ter dovoljenja v repozitoriju izbrisani.

###   modify-user

Ukaz modify-user se uporablja za posodabljanje informacij obstoječega uporabnika v digna CLI.

##### Uporaba ukaza
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, katerega podatke želite spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime za uporabnika (obvezno).
  
#### Možnosti  
  
- --is_superuser, -su: Nastavi uporabnika kot superuser in mu podeli povišane privilegije. Ta stikalo ne zahteva vrednosti.  
- --valid_until, -vu: Določi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni podan, račun ostane veljaven nedoločen čas.  
  
#### Primer
  
Za spremembo polnega imena uporabnika jdoe v “Johnathan Doe” in njegovo povišanje v superuser:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Ukaz modify-user-pwd se uporablja za spreminjanje gesla obstoječega uporabnika v digna CLI.
  
##### Uporaba ukaza
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenti
  
- **USER_NAME**: Uporabniško ime uporabnika, katerega geslo se spreminja (obvezno).
- **USER_PWD**: Novo geslo uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika jdoe v newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Ukaz list-users prikaže seznam vseh uporabnikov, registriranih v digna sistemu preko digna CLI.

##### Uporaba ukaza

bash
dignacli list-users


Zagon tega ukaza v digna CLI se poveže s digna repozitorijem in izpiše vse uporabnike ter prikaže njihove ID-je, uporabniška imena, polna imena, stanje superuser ter časovne žige poteka.

# Upravljanje repozitorija

###   upgrade-repo
  
Ukaz upgrade-repo se uporablja za nadgradnjo ali inicializacijo digna repozitorija preko digna CLI. Ta ukaz je potreben za uporabo posodobitev ali prvo nastavitev repozitorija.
  
#### Uporaba ukaza

bash
dignacli upgrade-repo [options]

  
#### Možnosti
  
- --simulation-mode, -s: Ko je omogočeno, ukaz zažene v načinu simulacije; izpiše SQL izraze, ki bi se izvedli, a jih v resnici ne izvede. To je uporabno za predogled sprememb brez spreminjanja repozitorija.  

  
#### Primer
  
Za nadgradnjo digna repozitorija lahko zaženete ukaz brez možnosti:
  
bash
dignacli upgrade-repo
  
Za zagon nadgradnje v simulacijskem načinu (prikaz SQL izrazov brez njihove izvedbe):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ta ukaz je ključnega pomena za vzdrževanje digna sistema, saj zagotavlja, da je shema baze podatkov in druge komponente repozitorija združljive z najnovejšo različico programske opreme.

###   encrypt
  
Ukaz encrypt se uporablja za šifriranje gesla v digna CLI.
  
#### Uporaba ukaza
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je potrebno šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla morate geslo podati kot argument.   
Na primer, za šifriranje gesla mypassword123:
bash
dignacli encrypt mypassword123

Ta ukaz izpiše šifrirano različico podanega gesla; ta izhod je nato mogoče uporabiti v varnejših kontekstih. Če ni podan argument gesla, bo CLI prikazal napako zaradi manjkajočega argumenta.

###   generate-key
  
Ukaz generate-key ustvari Fernet ključ, potreben za zagotavljanje varnosti gesel, shranjenih v digna repozitoriju.
  
#### Uporaba ukaza
bash
dignacli generate-key

  
## Upravljanje podatkov

###   clean-up

Ukaz clean-up se uporablja za odstranjevanje profilov, napovedi in podatkov Sistema prometnih luči (TLS) za enega ali več virov podatkov v okviru določenega projekta preko digna CLI. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov in pomaga pri čiščenju starih ali nepotrebnih podatkov za urejeno in učinkovito podatkovno okolje.

#### Uporaba ukaza

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega bodo podatki odstranjeni (obvezno). Uporaba ključne besede all-projects v tem argumentu omogoči digna, da iterira čez vse obstoječe projekte in izvede ukaz.
- **FROM_DATE**: Začetni datum in čas za odstranjevanje podatkov. Sprejeti formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za odstranjevanje podatkov; uporablja iste formate kot FROM_DATE (obvezno).
  
#### Možnosti
  
- --table-name, -tn: Omeji čiščenje na določeno tabelo v projektu.
- --table-filter, -tf: Uporabi filter za omejitev na tabele, katerih imena vsebujejo navedeni podniz.
- --timing, -tm: Po zaključku čiščenja prikaže informacije o trajanju.
- --help: Prikaže pomoč za ukaz clean-up in izstopi.
  
#### Primer
  
Za odstranitev podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Za odstranitev podatkov samo iz določene tabele Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ta ukaz pomaga pri upravljanju shranjevanja podatkov in zagotavlja, da repozitorij vsebuje le relevantne informacije.

###   inspect

Ukaz inspect se uporablja za ustvarjanje profilov, napovedi in podatkov Sistema prometnih luči (TLS) za enega ali več virov podatkov v okviru določenega projekta preko digna CLI. Ta ukaz pomaga pri analizi in spremljanju podatkov v določenem obdobju.

#### Uporaba ukaza

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, v katerem bodo podatki analizirani (obvezno). Uporaba ključne besede all-projects omogoči digna, da iterira čez vse obstoječe projekte in izvede ukaz.
- **FROM_DATE**: Začetni datum in čas za pregled podatkov. Sprejeti formati so %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Končni datum in čas za pregled podatkov; uporablja iste formate kot FROM_DATE (obvezno).
  
#### Možnosti

- --table-name, -tn: Omeji pregled na določeno tabelo v projektu.
- --table-filter, -tf: Uporabi filter za pregled tabel, katerih imena vsebujejo navedeni podniz.
- --force-profile: Zahteva ponovno zbiranje profilov. Privzeta nastavitev je force-profile.
- --no-force-profile: Onemogoči ponovno zbiranje profilov.
- --force-prediction: Zahteva ponovno izračunavanje napovedi. Privzeta nastavitev je force-prediction.
- --no-force-prediction: Onemogoči ponovno izračunavanje napovedi.
- --force-alert-status: Zahteva ponovno izračunavanje statusov opozoril. Privzeta nastavitev je force-alert-status.
- --no-force-alert-status: Onemogoči ponovno izračunavanje statusov opozoril.
- --timing, -tm: Po zaključku pregleda prikaže informacije o trajanju.
- --alert-notification, -an: Pošlje obvestila o opozorilih na naročene kanale.
  
#### Primer
  
Za pregled podatkov v projektu ProjectA med 1. januarjem 2024 in 31. januarjem 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Za pregled samo določene tabele in zahtevo po ponovnem izračunu napovedi:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ta ukaz je uporaben za ustvarjanje posodobljenih profilov in napovedi, spremljanje integritete podatkov ter upravljanje sistemov opozoril v izbranem časovnem obdobju projekta.

###   tls-status

Ukaz tls-status se uporablja za poizvedbo o statusu Sistema prometnih luči (TLS) določene tabele znotraj projekta za določen datum preko digna CLI. Sistem prometnih luči prikazuje stanja, ki zahtevajo pozornost ali opozorilo glede zdravja in kakovosti podatkov.
  
#### Uporaba ukaza
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se preverja TLS status (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero se preverja TLS status (obvezno).
- **DATE**: Datum, za katerega se preverja TLS status, običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje TLS stanja tabele UserData v projektu ProjectA za datum 1. julij 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ta ukaz zagotavlja jasen in izvedljiv poročilo o stanju na podlagi vnaprej določenih kriterijev, kar uporabnikom pomaga spremljati in vzdrževati kakovost podatkov.

###   list-projects
  
Ukaz list-projects prikaže seznam vseh obstoječih projektov v digna CLI.
  
#### Uporaba ukaza
  
bash
dignacli list-projects


Ta ukaz je še posebej uporaben za skrbnike in uporabnike, ki upravljajo več projektov; omogoča hiter pregled nad projekti, prisotnimi v digna repozitoriju.

###   list-ds

Ukaz list-ds prikaže vse razpoložljive vire podatkov znotraj določenega projekta v digna CLI. Ta ukaz je koristen za razumevanje obstoječih podatkovnih virov v digna sistemu za potrebe analize in upravljanja.

#### Uporaba ukaza
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenti
- **PROJECT_NAME**: Ime projekta, katerega podatkovni viri bodo navedeni (obvezno).
  
#### Primer
  
Za navedbo vseh podatkovnih virov v projektu ProjectA:
  
bash
dignacli list-ds ProjectA

  
Ta ukaz nudi pregled nad razpoložljivimi podatkovnimi viri v projektu in pomaga uporabnikom učinkoviteje upravljati svoje podatkovno okolje.