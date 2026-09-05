# digna CLI viide 2024.09
**2024-08-24**

---

## CLI põhialused

---

###   help

Valiku --help abil kuvatakse teavet saadaolevate käskude ja nende kasutuse kohta. Selle valiku kasutamiseks on kaks peamist viisi:

1. **Üldise abi kuvamine:**
   
    Kasuta --help otse peale märksõna ***digna***cl  
   bash
   dignacli --help

3.  **Abi konkreetse käsu kohta:**  
  
    Konkreetse käsu üksikasjaliku teabe saamiseks lisa sellele käsule --help.
    Näiteks, et saada abi käsuga add-user, käivita:
     bash
     dignacli add-user --help
     

     ### väljund:
      
     - **Käsu kirjeldus:** Pakub üksikasjalikku kirjeldust, mida käsk teeb.  
     - **Süntaks:** Näitab täpset süntaksit, sealhulgas nõutud ja valikulisi argumendid.  
     - **Valikud:** Loetleb käsule spetsiifilised valikud koos nende selgitustega.  
     - **Näited:** Annavad näiteid, kuidas käsku tõhusalt käivitada.

  
###   check-repo-connection

check-repo-connection käsk on ***digna*** CLI tööriistas utiliit, mis on mõeldud ühenduvuse ja ligipääsu testimiseks antud ***digna*** repositooriumile. See käsk kontrollib, et CLI suudab repositooriumiga suhelda.
      
##### Käsu kasutamine
bash
dignacli check-repo-connection


Õnnestunud täitmise korral väljastab käsk ühenduse kinnituse ning repositooriumi üksikasjad: Repository version, Host, Database and Schema.  
  
Kui repositooriumiga ühendus ei õnnestu, kontrolli config.toml faili, et konfiguratsiooniseaded oleksid õiged.

###   version

Paigaldatud *dignacli* versiooni kontrollimiseks kasuta valikut --version.  
  
#### Käsu kasutamine
bash
dignacli --version

  
#### Näiteväljund
bash
dignacli version 2024.09


###   logimise valikud
  
Vaikimisi on ***digna*** käskude konsooliväljund minimalistlik. Enamik käske võimaldavad täiendava teabe kuvamist järgmiste valikute abil:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ja „debug“ määravad detailide taset, samas kui „logfile“ lüliti võimaldab suunata väljundi faili voogu, mitte konsooli aknasse.

## Kasutajate haldus

###   add-user
  
add-user käsk ***digna*** CLI-s kasutatakse uue kasutaja lisamiseks ***digna*** süsteemi.
  
#### Käsu kasutamine
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumendid

- **USER_NAME**: Uue kasutaja kasutajanimi (nõutav).
- **USER_FULL_NAME**: Uue kasutaja täielik nimi (nõutav).
- **USER_PASSWORD**: Uue kasutaja parool (nõutav).

#### Valikud

- --is_superuser, -su: Lipp, mis tähistab uut kasutajat administraatorina.
- --valid_until, -vu: Määrab kasutajakonto aegumiskuupäeva vormingus YYYY-MM-DD HH:MI:SS. Kui seda ei määrata, ei ole kontol aegumiskuupäeva.

#### Näide

Uue kasutaja lisamiseks kasutajanimega jdoe, täieliku nimega John Doe ja parooliga password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Uue kasutaja lisamiseks ja konto aegumiskuupäeva määramiseks:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user käsk ***digna*** CLI-s kasutatakse olemasoleva kasutaja eemaldamiseks ***digna*** süsteemist.
  
##### Käsu kasutamine
bash
dignacli delete-user USER_NAME

  
#### Argumendid
- **USER_NAME**: Kustutatava kasutaja kasutajanimi (nõutav). See on käsu ainus kohustuslik argument.

#### Näide
bash
dignacli delete-user jdoe

  
Selle käsu täitmine eemaldab kasutaja jdoe ***digna*** süsteemist, tühistades tema juurdepääsu ja kustutades tema seotud andmed ja õigused repositooriumist.

###   modify-user

modify-user käsk ***digna*** CLI-s kasutatakse olemasoleva kasutaja andmete uuendamiseks ***digna*** süsteemis.

##### Käsu kasutamine
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumendid
  
- **USER_NAME**: Muudetava kasutaja kasutajanimi (nõutav).
- **USER_FULL_NAME**: Uus täielik nimi kasutaja jaoks (nõutav).
  
#### Valikud  
  
- --is_superuser, -su: Määrab kasutaja superkasutajaks, andes kõrgendatud õigused. Selle lipu kasutamisel väärtust ei nõuta.  
- --valid_until, -vu: Määrab kasutajakonto aegumiskuupäeva vormingus YYYY-MM-DD HH:MI:SS. Kui seda ei anta, jääb konto kehtima piiramatu ajani.  
  
#### Näide
  
Kasutaja jdoe täieliku nime muutmiseks „Johnathan Doe“ ja kasutaja määramiseks superkasutajaks:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd käsk ***digna*** CLI-s kasutatakse olemasoleva kasutaja parooli muutmiseks ***digna*** süsteemis.
  
##### Käsu kasutamine
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumendid
  
- **USER_NAME**: Parooli muutmisele alluv kasutajanimi (nõutav).
- **USER_PWD**: Kasutaja uus parool (nõutav).
  
#### Näide
  
Kasutaja jdoe parooli muutmiseks uueks newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users käsk ***digna*** CLI-s kuvab nimekirja kõigist ***digna*** süsteemi registreeritud kasutajatest.

##### Käsu kasutamine

bash
dignacli list-users


Selle käsu käivitamisel ühendub ***digna*** CLI ***digna*** repositooriumiga ja loetleb kõik kasutajad, näidates nende ID-d, kasutajanime, täielikku nime, superkasutaja staatust ja aegumistähtajaid.

# Repositooriumi haldus

###   upgrade-repo
  
upgrade-repo käsk ***digna*** CLI-s kasutatakse ***digna*** repositooriumi uuendamiseks või initsialiseerimiseks. See käsk on vajalik uuenduste rakendamiseks või repositooriumi infrastruktuuri esmakordseks seadistamiseks.
  
#### Käsu kasutamine

bash
dignacli upgrade-repo [options]

  
#### Valikud
  
- --simulation-mode, -s: Kui lubatud, käivitab käsk simulatsioonirežiimis, mis prindib SQL-lauseid, mida täidetaks, kuid ei käivita neid tegelikult. See on kasulik muudatuste eelvaatamiseks ilma repositooriumi muutmata.  

  
#### Näide
  
***digna*** repositooriumi uuendamiseks võid käivitada käsu ilma valikuteta:
  
bash
dignacli upgrade-repo
  
Uuenduse käivitamiseks simulatsioonirežiimis (et näha SQL-lauseid ilma neid rakendamata):
  
bash
dignacli upgrade-repo --simulation-mode

  
See käsk on oluline ***digna*** süsteemi hoolduseks, tagades, et andmebaasi skeem ja muud repositooriumi komponendid oleksid tarkvara uusima versiooniga sünkroonis.

###   encrypt
  
encrypt käsk ***digna*** CLI-s kasutatakse parooli krüpteerimiseks.
  
#### Käsu kasutamine
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumendid
- **PASSWORD**: Parool, mida on vaja krüpteerida (nõutav).
  
#### Näide
  
Parooli krüpteerimiseks tuleb parool edastada argumendina.   
Näiteks parooli mypassword123 krüpteerimiseks kasuta:
bash
dignacli encrypt mypassword123

See käsk väljastab antud parooli krüpteeritud versiooni, mida saab seejärel kasutada turvalistes kontekstides. Kui parooli argumendi ei anta, kuvab CLI vea, mis näitab puuduvat argumenti.

###   generate-key
  
generate-key käsk genereerib Fernet-võtme, mis on vajalik paroolide turvaliseks säilitamiseks ***digna*** repositooriumis.
  
#### Käsu kasutamine
bash
dignacli generate-key

  
## Andmete haldus

###   clean-up

clean-up käsk ***digna*** CLI-s kasutatakse profiilide, ennustuste ja liiklusmärguandme süsteemi andmete eemaldamiseks ühelt või mitmelt andmeallikalt nimetatud projektis. See käsk on oluline andmete elutsükli haldamiseks, aidates hoida organiseeritud ja tõhusat andmekeskkonda, kustutades aegunud või mittevajalikke andmeid.

#### Käsu kasutamine

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, kust andmeid eemaldatakse (nõutav). Kui selles argumendis kasutatakse märksõna all-projects, käsib see ***digna***-l iteratsiooni üle kõigi olemasolevate projektide ja rakendada käsku neile kõigile.
- **FROM_DATE**: Andmete eemaldamise alguskuupäev ja kellaaeg. Aktsepteeritud vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Andmete eemaldamise lõppkuupäev ja kellaaeg, sama vorminguga nagu FROM_DATE (nõutav).
  
#### Valikud
  
- --table-name, -tn: Piirab clean-up toimingut konkreetsele tabelile projektis.
- --table-filter, -tf: Filtreerib, piirates clean-up operatsiooni tabelitele, mille nimedes on antud alamsõne.
- --timing, -tm: Kuvab clean-up protsessi kestuse pärast lõpetamist.
- --help: Kuvab abiinfo clean-up käsu kohta ja väljub.
  
#### Näide
  
Andmete eemaldamiseks projektist ProjectA perioodil 1. jaanuar 2023 kuni 30. juuni 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Andmete eemaldamiseks ainult konkreetsest tabelist nimega Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
See käsk aitab hallata andmete salvestamist ja tagada, et repositooriumis oleks ainult asjakohane info.

###   inspect

inspect käsk ***digna*** CLI-s kasutatakse profiilide, ennustuste ja liiklusmärguandme süsteemi andmete loomiseks ühelt või mitmelt andmeallikalt nimetatud projektis. See käsk aitab andmete analüüsimisel ja jälgimisel määratud perioodi jooksul.

#### Käsu kasutamine

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille andmeid inspekteeritakse (nõutav). Kui selles argumendis kasutatakse märksõna all-projects, käsib see ***digna***-l iteratsiooni üle kõigi olemasolevate projektide ja rakendada käsku neile kõigile.
- **FROM_DATE**: Andmete inspekteerimise alguskuupäev ja kellaaeg. Aktsepteeritud vormingud hõlmavad %Y-%m-%d, %Y-%m-%dT%H:%M:%S või %Y-%m-%d %H:%M:%S (nõutav).
- **TO_DATE**: Andmete inspekteerimise lõppkuupäev ja kellaaeg, sama vorminguga nagu FROM_DATE (nõutav).
  
#### Valikud

- --table-name, -tn: Piirab inspekteerimist konkreetsele tabelile projektis.
- --table-filter, -tf: Filtreerib, inspekteerides ainult tabeleid, mille nimedes on antud alamsõne.
- --force-profile: Sunnib profiilide uuesti kogumist. Vaikimisi on force-profile.
- --no-force-profile: Takistab profiilide uuesti kogumist.
- --force-prediction: Sunnib ennustuste ümberarvutamist. Vaikimisi on force-prediction.
- --no-force-prediction: Takistab ennustuste ümberarvutamist.
- --force-alert-status: Sunnib hoiatuse staatuse ümberarvutamist. Vaikimisi on force-alert-status.
- --no-force-alert-status: Takistab hoiatuse staatuse ümberarvutamist.
- --timing, -tm: Kuvab inspekteerimisprotsessi kestuse pärast lõpetamist.
- --alert-notification, -an: Saadab hoiatusteatised tellitud kanalitele.
  
#### Näide
  
Projektis ProjectA andmete inspekteerimiseks ajavahemikus 1. jaanuar 2024 kuni 31. jaanuar 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Ainult konkreetse tabeli inspekteerimiseks ja ennustuste ümberarvutamise sundimiseks:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

See käsk on kasulik uuendatud profiilide ja ennustuste genereerimiseks, andmete terviklikkuse jälgimiseks ning hoiatussüsteemide haldamiseks määratud projekti ajavahemikus.

###   tls-status

tls-status käsk ***digna*** CLI-s kasutatakse Traffic Light Systemi (TLS) oleku pärimiseks konkreetse tabeli kohta projektis antud kuupäeval. Traffic Light System annab ülevaate andmete tervislikkusest ja kvaliteedist, osutades võimalikule probleemidele või hoiatustele, mis vajavad tähelepanu.
  
#### Käsu kasutamine
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumendid
  
- **PROJECT_NAME**: Projekti nimi, mille TLS olekut päritakse (nõutav).
- **TABLE_NAME**: Konkreetselt tabel, mille TLS olekut on vaja (nõutav).
- **DATE**: Kuupäev, mille kohta TLS olekut päritakse, tavaliselt vormingus %Y-%m-%d (nõutav).
  
#### Näide
  
TLS oleku kontrollimiseks tabeli nimega UserData kohta projektis ProjectA kuupäeval 1. juuli 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


See käsk aitab kasutajatel jälgida ja hoida andmete kvaliteeti, pakkudes selget ja tegevusvõimalusi andvat seisundi aruannet eelnevalt määratletud kriteeriumide alusel.

###   list-projects
  
list-projects käsk ***digna*** CLI-s kuvab nimekirja kõigist saadaolevatest projektidest ***digna*** süsteemis.
  
#### Käsu kasutamine
  
bash
dignacli list-projects


See käsk on eriti kasulik administraatoritele ja kasutajatele, kes haldavad mitut projekti, pakkudes kiiret ülevaadet saadaval olevatest projektidest ***digna*** repositooriumis.

###   list-ds

list-ds käsk ***digna*** CLI-s kuvab nimekirja kõigist saadaolevatest andmeallikatest nimetatud projektis. See käsk on kasulik andmevarade mõistmiseks, mida analüüsiks ja halduseks ***digna*** süsteemis kasutada saab.

#### Käsu kasutamine
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumendid
- **PROJECT_NAME**: Projekti nimi, mille andmeallikaid loetletakse (nõutav).
  
#### Näide
  
Kõigi andmeallikate loetlemiseks projektis nimega ProjectA:
  
bash
dignacli list-ds ProjectA

  
See käsk annab kasutajatele ülevaate projekti andmeallikatest, aidates neil andmelansse paremini navigeerida ja hallata.