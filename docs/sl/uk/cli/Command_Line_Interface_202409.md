---
title: digna CLI Priročnik 2024.09 – Ukazi in primeri | digna Documentation
description: Popoln priročnik za digna CLI izdajo 2024.09. Naučite se upravljati uporabnike, repozitorije in podatke z ukazi, kot so add-user, check-repo-connection, upgrade-repo, inspect, tls-status in drugi.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Priročnik 2024.09
**2024-08-24**

---

## Osnove CLI

---

###   help

Možnost --help prikaže informacije o razpoložljivih ukazih in njihovem načinu uporabe. Obstajata dva glavna načina uporabe te možnosti:

1. **Prikaz splošne pomoči:**
   
    Uporabite --help takoj po ključni besedi ***digna***  
bash
dignacli --help

2.  **Pridobitev pomoči za določen ukaz:**  
  
    Za podrobne informacije o določenem ukazu dodajte --help temu ukazu.
    Na primer, za pomoč pri ukazu add-user zaženite:
bash
dignacli add-user --help
     

     ### izhod:
      
     - **Opis ukaza:** Podroben opis, kaj ukaz opravlja.  
     - **Sintaksa:** Prikaže natančno sintakso, vključno z obveznimi in neobveznimi argumenti.  
     - **Možnosti:** Seznam možnosti, specifičnih za ukaz, z razlagami.  
     - **Primeri:** Primeri, kako pravilno izvesti ukaz.

  
###   check-repo-connection

Ukaz check-repo-connection je pripomoček v orodju ***digna*** CLI, namenjen preverjanju povezave in dostopa do navedenega repozitorija ***digna***. Ta ukaz zagotavlja, da lahko CLI komunicira z repozitorijem.
      
##### Uporaba ukaza
bash
dignacli check-repo-connection


Po uspešni izvedbi ukaz izpiše potrdilo o povezavi skupaj s podatki o repozitoriju: različico repozitorija, gostitelja, bazo podatkov in shemo.  
  
Če povezava z repozitorijem ni uspešna, preverite datoteko config.toml glede pravilnih nastavitev.

###   version

Za preverjanje nameščene različice *dignacli* uporabite možnost --version.  
  
#### Uporaba ukaza
bash
dignacli --version

  
#### Primer izhoda
bash
dignacli version 2024.09


###   parametri beleženja
  
Privzeto je izpis ukazov ***digna*** v konzoli minimalističen. Večina ukazov omogoča pridobitev dodatnih informacij z naslednjimi možnostmi:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
»verbose« in »debug« določata raven podrobnosti, medtem ko možnost »logfile« preusmeri izpis v datoteko namesto na konzolo.

## Upravljanje uporabnikov

###   add-user
  
Ukaz add-user v CLI ***digna*** se uporablja za dodajanje novega uporabnika v sistem ***digna***.
  
#### Uporaba ukaza
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenti

- **USER_NAME**: Ime uporabnika za nov račun (obvezno).
- **USER_FULL_NAME**: Polno ime novega uporabnika (obvezno).
- **USER_PASSWORD**: Geslo za novega uporabnika (obvezno).

#### Možnosti

- --is_superuser, -su: Oznaka, da je novi uporabnik skrbnik.
- --valid_until, -vu: Nastavi datum veljavnosti računa v formatu YYYY-MM-DD HH:MI:SS. Če ni navedeno, veljavnost ni omejena.

#### Primer

Za dodajanje novega uporabnika z imenom jdoe, polnim imenom John Doe in geslom password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Za dodajanje novega uporabnika in nastavitve datuma poteka računa:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Ukaz delete-user v CLI ***digna*** se uporablja za izbris obstoječega uporabnika iz sistema ***digna***.
  
##### Uporaba ukaza
bash
dignacli delete-user USER_NAME

  
#### Argumenti
- **USER_NAME**: Ime uporabnika, ki ga je treba izbrisati (obvezno). To je edini potrebni argument ukaza.

#### Primer
bash
dignacli delete-user jdoe

  
Izvedba tega ukaza bo iz sistema ***digna*** odstranila uporabnika jdoe, preklicala njegov dostop in izbrisala povezane podatke ter dovoljenja iz repozitorija.

###   modify-user

Ukaz modify-user v CLI ***digna*** se uporablja za posodabljanje podatkov obstoječega uporabnika v sistemu ***digna***.

##### Uporaba ukaza
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenti
  
- **USER_NAME**: Ime uporabnika, ki ga je treba spremeniti (obvezno).
- **USER_FULL_NAME**: Novo polno ime uporabnika (obvezno).
  
#### Možnosti  
  
- --is_superuser, -su: Nastavi uporabnika kot superuporabnika in mu dodeli povišane pravice. Ta preklop ne zahteva vrednosti.  
- --valid_until, -vu: Nastavi datum poteka računa v formatu YYYY-MM-DD HH:MI:SS. Če ni navedeno, račun ostane veljaven za nedoločen čas.  
  
#### Primer
  
Za spremembo polnega imena uporabnika jdoe v “Johnathan Doe” in za njegovo nastavitve kot superuporabnika:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Ukaz modify-user-pwd v CLI ***digna*** se uporablja za spremembo gesla obstoječega uporabnika v sistemu ***digna***.
  
##### Uporaba ukaza
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenti
  
- **USER_NAME**: Ime uporabnika, katerega geslo je treba spremeniti (obvezno).
- **USER_PWD**: Novo geslo uporabnika (obvezno).
  
#### Primer
  
Za spremembo gesla uporabnika jdoe v newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Ukaz list-users v CLI ***digna*** prikaže seznam vseh uporabnikov, registriranih v sistemu ***digna***.

##### Uporaba ukaza

bash
dignacli list-users


Izvedba tega ukaza v CLI ***digna*** se poveže z repozitorijem ***digna*** in izpiše seznam vseh uporabnikov ter prikaže njihov ID, uporabniško ime, polno ime, status superuporabnika in časovne žige poteka veljavnosti.

# Upravljanje repozitorija

###   upgrade-repo
  
Ukaz upgrade-repo v CLI ***digna*** se uporablja za nadgradnjo ali inicializacijo repozitorija ***digna***. Ta ukaz je potreben za uporabo posodobitev ali za prvo nastavitev infrastrukture repozitorija.
  
#### Uporaba ukaza

bash
dignacli upgrade-repo [options]

  
#### Možnosti
  
- --simulation-mode, -s: Če je omogočeno, ukaz deluje v načinu simulacije — izpiše SQL ukaze, ki bi bili izvedeni, vendar jih dejansko ne izvede. To je uporabno za predogled sprememb brez vpliva na repozitorij.  

  
#### Primer
  
Za nadgradnjo repozitorija ***digna*** lahko zaženete ukaz brez možnosti:
  
bash
dignacli upgrade-repo
  
Za zagon nadgradnje v načinu simulacije (da vidite SQL ukaze brez njihove uporabe):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ta ukaz je pomemben za vzdrževanje sistema ***digna***, saj zagotavlja skladnost sheme baze podatkov in drugih komponent repozitorija z najnovejšo različico programske opreme.

###   encrypt
  
Ukaz encrypt v CLI ***digna*** se uporablja za šifriranje gesla.
  
#### Uporaba ukaza
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenti
- **PASSWORD**: Geslo, ki ga je treba šifrirati (obvezno).
  
#### Primer
  
Za šifriranje gesla ga podajte kot argument.   
Na primer, za šifriranje gesla mypassword123 uporabite:
bash
dignacli encrypt mypassword123

Ta ukaz izpiše šifrirano različico podanega gesla, ki jo nato lahko uporabite v varnih kontekstih. Če argument gesla ni podan, bo CLI prikazal napako o manjkajočem argumentu.

###   generate-key
  
Ukaz generate-key se uporablja za generiranje Fernet-ključa, ki je potreben za zaščito gesel, shranjenih v repozitoriju ***digna***.
  
#### Uporaba ukaza
bash
dignacli generate-key

  
## Upravljanje podatkov

###   clean-up

Ukaz clean-up v CLI ***digna*** se uporablja za brisanje profilov, napovedi in podatkov sistema prometnih luči (traffic light system) za enega ali več virov podatkov v navedenem projektu. Ta ukaz je pomemben za upravljanje življenjskega cikla podatkov, saj pomaga vzdrževati organizirano in učinkovito okolje z odstranjevanjem zastarelih ali nepotrebnih podatkov.

#### Uporaba ukaza

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, iz katerega je treba izbrisati podatke (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse razpoložljive projekte in izvede ukaz za vsakega.
- **FROM_DATE**: Datum in čas začetka brisanja podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca brisanja podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
#### Možnosti
  
- --table-name, -tn: Omeji operacijo čiščenja na določeno tabelo v projektu.
- --table-filter, -tf: Filtrira tabele in omeji čiščenje na tiste, katerih ime vsebuje navedeni podniz.
- --timing, -tm: Prikaže trajanje procesa čiščenja po končanju.
- --help: Prikaže referenčne informacije za ukaz clean-up in izstopi.
  
#### Primer
  
Za brisanje podatkov iz projekta ProjectA med 1. januarjem 2023 in 30. junijem 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Za brisanje podatkov samo iz določene tabele z imenom Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ta ukaz pomaga upravljati hrambo podatkov in zagotavlja, da v repozitoriju ostanejo le relevantne informacije.

###   inspect

Ukaz inspect v CLI ***digna*** se uporablja za ustvarjanje profilov, napovedi in podatkov sistema prometnih luči (traffic light system) za enega ali več virov podatkov v navedenem projektu. Ta ukaz pomaga analizirati in spremljati podatke v določenem obdobju.

#### Uporaba ukaza

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega je treba izvesti inšpekcijo podatkov (obvezno). Uporaba ključne besede all-projects v tem argumentu ukaže ***digna***, naj iterira skozi vse razpoložljive projekte in izvede ukaz za vsakega.
- **FROM_DATE**: Datum in čas začetka inšpekcije podatkov. Dovoljeni formati vključujejo %Y-%m-%d, %Y-%m-%dT%H:%M:%S ali %Y-%m-%d %H:%M:%S (obvezno).
- **TO_DATE**: Datum in čas konca inšpekcije podatkov, z enakimi formati kot FROM_DATE (obvezno).
  
#### Možnosti

- --table-name, -tn: Omeji inšpekcijo na določeno tabelo v projektu.
- --table-filter, -tf: Filtrira tabele in inšpektira le tiste, katerih ime vsebuje navedeni podniz.
- --force-profile: Prisili ponovni zagon zbiranja profilov. Privzeto je force-profile omogočen.
- --no-force-profile: Prepreči ponovni zagon zbiranja profilov.
- --force-prediction: Prisili ponovni izračun napovedi. Privzeto je force-prediction omogočen.
- --no-force-prediction: Prepreči ponovni izračun napovedi.
- --force-alert-status: Prisili ponovni izračun stanj alarmov. Privzeto je force-alert-status omogočen.
- --no-force-alert-status: Prepreči ponovni izračun stanj alarmov.
- --timing, -tm: Prikaže trajanje procesa inšpekcije po končanju.
- --alert-notification, -an: Pošlje obvestila o alarmih na prijavljene kanale.
  
#### Primer
  
Za pregled podatkov projekta ProjectA od 1. januarja 2024 do 31. januarja 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Za inšpekcijo le določene tabele in prisilen ponovni izračun napovedi:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ta ukaz je uporaben za generiranje posodobljenih profilov in napovedi, spremljanje celovitosti podatkov ter upravljanje sistema obveščanja v navedenem časovnem obdobju projekta.

###   tls-status

Ukaz tls-status v CLI ***digna*** se uporablja za pridobitev stanja sistema prometnih luči (TLS) za določeno tabelo v projektu na izbrani datum. Sistem prometnih luči daje vpogled v stanje in kakovost podatkov ter opozarja na težave ali alarme, ki zahtevajo pozornost.
  
#### Uporaba ukaza
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenti
  
- **PROJECT_NAME**: Ime projekta, za katerega se zahteva stanje TLS (obvezno).
- **TABLE_NAME**: Določena tabela v projektu, za katero potrebujete stanje TLS (obvezno).
- **DATE**: Datum, za katerega se zahteva stanje TLS, običajno v formatu %Y-%m-%d (obvezno).
  
#### Primer
  
Za preverjanje stanja TLS za tabelo UserData v projektu ProjectA na 1. julij 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ta ukaz pomaga uporabnikom spremljati in vzdrževati kakovost podatkov ter zagotavlja jasna in praktična poročila o stanju na podlagi vnaprej določenih kriterijev.

###   list-projects
  
Ukaz list-projects v CLI ***digna*** se uporablja za prikaz seznama vseh razpoložljivih projektov v sistemu ***digna***.
  
#### Uporaba ukaza
  
bash
dignacli list-projects


Ta ukaz je še posebej koristen za skrbnike in uporabnike, ki upravljajo več projektov, saj nudi hiter pregled razpoložljivih projektov v repozitoriju ***digna***.

###   list-ds

Ukaz list-ds v CLI ***digna*** se uporablja za prikaz seznama vseh razpoložljivih virov podatkov v navedenem projektu. Ta ukaz je uporaben za razumevanje podatkov, razpoložljivih za analizo in upravljanje v sistemu ***digna***.

#### Uporaba ukaza
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenti
- **PROJECT_NAME**: Ime projekta, za katerega so navedeni viri podatkov (obvezno).
  
#### Primer
  
Za izpis vseh virov podatkov v projektu z imenom ProjectA:
  
bash
dignacli list-ds ProjectA

  
Ta ukaz uporabnikom nudi pregled virov podatkov, ki so na voljo v projektu, in pomaga pri orientaciji ter učinkovitejšem upravljanju podatkovnega okolja.