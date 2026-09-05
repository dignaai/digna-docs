---
title: digna CLI nuoroda 2024.09 – Komandos ir pavyzdžiai | digna dokumentacija
description: Pilnas digna CLI 2024.09 leidimo žinynas. Sužinokite, kaip valdyti vartotojus, saugyklas ir duomenis naudojant komandas, tokias kaip add-user, check-repo-connection, upgrade-repo, inspect, tls-status ir kt.
image: /assets/logo_square.png
---

# digna CLI nuoroda 2024.09
**2024-08-24**

---

## CLI pagrindai

---

###   help

Parinktis --help pateikia informaciją apie prieinamas komandas ir jų naudojimą. Yra du pagrindiniai būdai naudoti šią parinktį:

1. **Bendra pagalba:**
   
    Naudokite --help iškart po raktažodžio dignacli  
   bash
   dignacli --help

2.  **Pagalba konkrečiai komandai:**  
  
    Norėdami gauti išsamesnę informaciją apie konkrečią komandą, pridėkite --help prie tos komandos.
    Pavyzdžiui, kad gauti pagalbą apie komandą add-user, paleiskite:
     bash
     dignacli add-user --help
     

     ### išvestis:
      
     - **Komandos aprašymas:** Išsamiai paaiškina, ką komanda atlieka.  
     - **Sintaksė:** Rodo tikslią sintaksę, įskaitant privalomus ir pasirenkamuosius argumentus.  
     - **Parinktys:** Išvardina komandos specifines parinktis su paaiškinimais.  
     - **Pavyzdžiai:** Pateikia pavyzdžius, kaip efektyviai vykdyti komandą.

  
###   check-repo-connection

check-repo-connection komanda ***digna*** CLI įrankyje skirta patikrinti ryšį ir prieigą prie nurodytos ***digna*** saugyklos. Ši komanda užtikrina, kad CLI gali bendrauti su saugykla.
      
##### Komandos naudojimas
bash
dignacli check-repo-connection


Sėkmingai įvykdžius komandą, ji išveda prisijungimo patvirtinimą kartu su informacija apie saugyklą: saugyklos versija (Repository version), Host, Database ir Schema.  
  
Jei prisijungti prie saugyklos nepavyksta, patikrinkite config.toml failą dėl teisingų konfigūracijos nustatymų.

###   version

Norėdami patikrinti įdiegtą *dignacli* versiją, naudokite parinktį --version.  
  
#### Komandos naudojimas
bash
dignacli --version

  
#### Pavyzdinė išvestis
bash
dignacli version 2024.09


###   logging options
  
Numatytasis ***digna*** komandų konsolės išvestis yra minimalus. Dauguma komandų leidžia pateikti papildomą informaciją naudojant šias parinktis:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
„verbose“ ir „debug“ nurodo išsamumo lygį, tuo tarpu „logfile“ perjungiklis leidžia nukreipti išvestį į failą vietoje konsolės lango.

## Vartotojų valdymas

###   add-user
  
add-user komanda ***digna*** CLI naudojama pridėti naują vartotoją į ***digna*** sistemą.
  
#### Komandos naudojimas
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumentai

- **USER_NAME**: Naujo vartotojo vartotojo vardas (privalomas).
- **USER_FULL_NAME**: Naujo vartotojo pilnas vardas (privalomas).
- **USER_PASSWORD**: Naujo vartotojo slaptažodis (privalomas).

#### Parinktys

- --is_superuser, -su: Žymė, priskirianti naują vartotoją administratoriumi.
- --valid_until, -vu: Nustato vartotojo paskyros galiojimo pabaigos datą formatu YYYY-MM-DD HH:MI:SS. Jei nenustatyta, paskyra neturi galiojimo pabaigos.

#### Pavyzdys

Norint pridėti naują vartotoją su vartotojo vardu jdoe, pilnu vardu John Doe ir slaptažodžiu password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Norint pridėti naują vartotoją ir nustatyti paskyros galiojimo datą:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user komanda ***digna*** CLI naudojama pašalinti esamą vartotoją iš ***digna*** sistemos.
  
##### Komandos naudojimas
bash
dignacli delete-user USER_NAME

  
#### Argumentai
- **USER_NAME**: Vartotojo, kurį reikia pašalinti, vartotojo vardas (privalomas). Tai yra vienintelis komandos reikalingas argumentas.

#### Pavyzdys
bash
dignacli delete-user jdoe

  
Šios komandos vykdymas pašalins vartotoją jdoe iš ***digna*** sistemos, panaikindamas jo prieigą ir ištrindamas susijusius duomenis bei teises iš saugyklos.

###   modify-user

modify-user komanda ***digna*** CLI naudojama atnaujinti esamo vartotojo duomenis ***digna*** sistemoje.

##### Komandos naudojimas
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumentai
  
- **USER_NAME**: Vartotojo vardas, kurį reikia pakeisti (privalomas).
- **USER_FULL_NAME**: Naujas vartotojo pilnas vardas (privalomas).
  
#### Parinktys  
  
- --is_superuser, -su: Nustato vartotoją kaip superuserį, suteikdama pakeltas privilegijas. Šis žymeklis nereikalauja reikšmės.  
- --valid_until, -vu: Nustato vartotojo paskyros galiojimo pabaigos datą formatu YYYY-MM-DD HH:MI:SS. Jei nenurodyta, paskyra galios neribotai.  
  
#### Pavyzdys
  
Norint pakeisti vartotojo jdoe pilną vardą į „Johnathan Doe“ ir nustatyti vartotoją kaip superuserį:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd komanda ***digna*** CLI naudojama pakeisti esamo vartotojo slaptažodį ***digna*** sistemoje.
  
##### Komandos naudojimas
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumentai
  
- **USER_NAME**: Vartotojo vardas, kurio slaptažodis keičiamas (privalomas).
- **USER_PWD**: Naujas vartotojo slaptažodis (privalomas).
  
#### Pavyzdys
  
Norint pakeisti vartotojo jdoe slaptažodį į newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users komanda ***digna*** CLI pateikia visų ***digna*** sistemoje užregistruotų vartotojų sąrašą.

##### Komandos naudojimas

bash
dignacli list-users


Vykdant šią komandą ***digna*** CLI prisijungs prie ***digna*** saugyklos ir išves visus vartotojus, rodydama jų ID, vartotojo vardą, pilną vardą, superuser statusą ir galiojimo timestamp'us.

# Saugyklos valdymas

###   upgrade-repo
  
upgrade-repo komanda ***digna*** CLI naudojama atnaujinti arba inicijuoti ***digna*** saugyklą. Ši komanda būtina taikant atnaujinimus arba ruošiant saugyklos infrastruktūrą pirmą kartą.
  
#### Komandos naudojimas

bash
dignacli upgrade-repo [options]

  
#### Parinktys
  
- --simulation-mode, -s: Įjungus, komanda veikia simuliacijos režimu — spausdina SQL užklausas, kurios būtų vykdomos, bet jų faktiškai nevykdo. Tai naudinga peržiūrėti pakeitimus nekeičiant saugyklos.  

  
#### Pavyzdys
  
Norėdami atnaujinti ***digna*** saugyklą, galite paleisti komandą be parinkčių:
  
bash
dignacli upgrade-repo
  
Norėdami paleisti atnaujinimą simuliacijos režimu (pamatyti SQL užklausas be jų taikymo):
  
bash
dignacli upgrade-repo --simulation-mode

  
Ši komanda yra svarbi palaikant ***digna*** sistemą, užtikrinant, kad duomenų bazės schema ir kiti saugyklos komponentai atitiktų programinės įrangos naujausią versiją.

###   encrypt
  
encrypt komanda ***digna*** CLI naudojama užšifruoti slaptažodį.
  
#### Komandos naudojimas
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumentai
- **PASSWORD**: Slaptažodis, kurį reikia užšifruoti (privalomas).
  
#### Pavyzdys
  
Norėdami užšifruoti slaptažodį, turite pateikti slaptažodį kaip argumentą.   
Pavyzdžiui, kad užšifruoti slaptažodį mypassword123, naudokite:
bash
dignacli encrypt mypassword123

Ši komanda išveda pateikto slaptažodžio užšifruotą versiją, kurią vėliau galima naudoti saugiose vietose. Jei slaptažodžio argumentas nepateiktas, CLI parodys klaidą nurodydama trūkstamą argumentą.

###   generate-key
  
generate-key komanda naudojama sukurti Fernet key, kuris yra būtinas saugant slaptažodžius užšifruotame pavidale ***digna*** saugykloje.
  
#### Komandos naudojimas
bash
dignacli generate-key

  
## Duomenų valdymas

###   clean-up

clean-up komanda ***digna*** CLI naudojama pašalinti profilius, prognozes ir Traffic Light System duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda yra svarbi duomenų gyvavimo ciklo valdymui, padedanti palaikyti tvarkingą ir efektyvią duomenų aplinką pašalinant pasenusius ar nereikalingus duomenis.

#### Komandos naudojimas

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, iš kurio bus pašalinami duomenys (privalomas). Naudojant raktažodį all-projects šiame argumente, ***digna*** iteruos per visus esamus projektus ir pritaikys šią komandą juose.
- **FROM_DATE**: Duomenų pašalinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų pašalinimo pabaigos data ir laikas, naudojant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys
  
- --table-name, -tn: Apriboja clean-up operaciją iki konkrečios projekto lentelės.
- --table-filter, -tf: Filtras, ribojantis clean-up tik toms lentelėms, kurių pavadinime yra nurodytas potekstis.
- --timing, -tm: Parodo clean-up proceso trukmę po jo užbaigimo.
- --help: Parodo pagalbą apie clean-up komandą ir išeina.
  
#### Pavyzdys
  
Norėdami pašalinti duomenis iš projekto ProjectA tarp 2023-01-01 ir 2023-06-30:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Norėdami pašalinti duomenis tik iš konkrečios lentelės Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Ši komanda padeda valdyti duomenų saugyklą ir užtikrina, kad saugykloje liktų tik aktuali informacija.

###   inspect

inspect komanda ***digna*** CLI naudojama sukurti profilius, prognozes ir Traffic Light System duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis per apibrėžtą laikotarpį.

#### Komandos naudojimas

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kuriam bus atliekama duomenų inspekcija (privalomas). Naudojant raktažodį all-projects šiame argumente, ***digna*** iteruos per visus esamus projektus ir pritaikys šią komandą.
- **FROM_DATE**: Duomenų inspekcijos pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų inspekcijos pabaigos data ir laikas, naudojant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- --table-name, -tn: Apriboja inspekciją iki konkrečios projekto lentelės.
- --table-filter, -tf: Filtras, kad būtų inspektuojamos tik tos lentelės, kurių pavadinime yra nurodytas potekstis.
- --force-profile: Priverčia pakartotinai surinkti profilius. Pagal nutylėjimą yra force-profile.
- --no-force-profile: Neleidžia pakartotinai surinkti profilių.
- --force-prediction: Priverčia perskaičiuoti prognozes. Pagal nutylėjimą yra force-prediction.
- --no-force-prediction: Neleidžia perskaičiuoti prognozių.
- --force-alert-status: Priverčia perskaičiuoti perspėjimų (alert) statusus. Pagal nutylėjimą yra force-alert-status.
- --no-force-alert-status: Neleidžia perskaičiuoti perspėjimų statusų.
- --timing, -tm: Parodo inspekcijos proceso trukmę po jo užbaigimo.
- --alert-notification, -an: Siunčia perspėjimų pranešimus prenumeruotais kanalais.
  
#### Pavyzdys
  
Norėdami inspektuoti duomenis projekte ProjectA nuo 2024-01-01 iki 2024-01-31:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Norėdami inspektuoti tik konkrečią lentelę ir priversti prognozių perskaičiavimą:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Ši komanda naudinga generuoti atnaujintus profilius ir prognozes, stebėti duomenų vientisumą ir valdyti perspėjimų sistemas nurodytu projekto laiko tarpu.

###   tls-status

tls-status komanda ***digna*** CLI naudojama užklausai dėl Traffic Light System (TLS) būsenos konkrečioje projekto lentelėje tam tikrą datą. Traffic Light System teikia informaciją apie duomenų sveikatą ir kokybę, nurodant galimas problemas ar perspėjimus, kuriems reikia dėmesio.
  
#### Komandos naudojimas
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kuriam užklausoma TLS būsena (privalomas).
- **TABLE_NAME**: Konkreti projekto lentelė, kurios TLS būsena reikalinga (privalomas).
- **DATE**: Data, kuriai užklausoma TLS būsena, paprastai formatu %Y-%m-%d (privalomas).
  
#### Pavyzdys
  
Norėdami patikrinti TLS būseną lentelėje UserData projekte ProjectA 2024-07-01:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Ši komanda padeda vartotojams stebėti ir palaikyti duomenų kokybę, teikdama aiškią ir veiksmingą būsenos ataskaitą, paremtą iš anksto apibrėžtais kriterijais.

###   list-projects
  
list-projects komanda ***digna*** CLI naudojama parodyti visų prieinamų projektų sąrašą ***digna*** sistemoje.
  
#### Komandos naudojimas
  
bash
dignacli list-projects


Ši komanda ypač naudinga administratoriui ir vartotojams, kurie valdo kelis projektus — ji suteikia greitą apžvalgą apie prieinamus projektus ***digna*** saugykloje.

###   list-ds

list-ds komanda ***digna*** CLI naudojama parodyti visų prieinamų duomenų šaltinių sąrašą nurodytame projekte. Ši komanda naudinga suprasti, kokie duomenų ištekliai yra prieinami analizei ir valdymui ***digna*** sistemoje.

#### Komandos naudojimas
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumentai
- **PROJECT_NAME**: Projekto pavadinimas, kuriam rodomi duomenų šaltiniai (privalomas).
  
#### Pavyzdys
  
Norėdami išvardinti visus duomenų šaltinius projekte ProjectA:
  
bash
dignacli list-ds ProjectA

  
Ši komanda suteikia vartotojams apžvalgą apie projekto turimus duomenų šaltinius, padėdama efektyviau naršyti ir valdyti duomenų kraštovaizdį.