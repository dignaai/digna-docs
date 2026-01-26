---
title: digna CLI nuoroda 2026.01 – Komandos ir pavyzdžiai | digna dokumentacija
description: Išsami digna CLI versijos 2026.01 nuoroda. Sužinokite, kaip valdyti vartotojus, saugyklas ir duomenis naudojant komandas, tokias kaip add-user, check-config, check-repo-connection, inspect, inspect-async ir kt.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202601/
image: /assets/logo_square.png
---

# digna CLI nuoroda 2026.01
**2026-01-15**

Šiame puslapyje dokumentuojamas visas komandų rinkinys, prieinamas ***digna*** CLI leidime **2026.01**, įtraukiant naudojimo pavyzdžius ir parinktis.

---

## CLI pagrindai

---

### help
Parinktis `--help` pateikia informaciją apie prieinamas komandas ir jų naudojimą. Yra du pagrindiniai būdai naudoti šią parinktį:

1. **Bendros pagalbos atvaizdavimas:**
   
   Naudokite `--help` iš karto po raktažodžio ***digna***:
   ```bash
   dignacli --help
   ```

2. **Pagalba konkrečiai komandai:**  
  
   Norėdami gauti detalesnę informaciją apie konkrečią komandą, pridėkite `--help` po tos komandos.
   Pavyzdžiui, norėdami gauti pagalbą su komanda `add-user`, vykdykite:
   ```bash
   dignacli add-user --help
   ```

   ### išvestis:
    
   - **Komandos aprašymas:** Išsamiai aprašo, ką atlieka komanda.  
   - **Sintaksė:** Rodo tikslią sintaksę, įskaitant reikiamus ir pasirenkamus argumentus.  
   - **Parinktys:** Išvardija komandai specifines parinktis ir jų paaiškinimus.  
   - **Pavyzdžiai:** Pateikia pavyzdžius, kaip efektyviai vykdyti komandą.

### check-config

Komanda check-config yra įrankis ***digna*** CLI, skirtas patikrinti ***digna*** konfigūraciją. Ši komanda užtikrina, kad ***digna*** komponentai gali rasti reikiamus konfigūracijos elementus faile config.toml.

#### Parinktys

- `--configpath`, `-cp`: Failas arba katalogas, kuriame yra konfigūracija. Jei nenurodoma, bus naudojamas ../config.toml.
      
#### Komandos naudojimas
```bash
dignacli check-config
```

Sėkmingai įvykdžius komandą, bus pateiktas patvirtinimas, kad konfigūracija yra pilna.  
  
Jei konfigūracija atrodo nevisiška, bus išvardyti trūkstami konfigūracijos elementai.

  
### check-repo-connection

Komanda check-repo-connection yra įrankis ***digna*** CLI, skirtas patikrinti ryšį su nurodyta ***digna*** saugykla ir prieigos galimybes. Ši komanda užtikrina, kad CLI gali sąveikauti su saugykla.
      
#### Komandos naudojimas
```bash
dignacli check-repo-connection
```

Sėkmingai įvykdžius komandą, bus pateiktas ryšio patvirtinimas kartu su saugyklos informacija: Repository version, Host, Database ir Schema.  
  
Jei ryšys su saugykla nepavyksta, patikrinkite config.toml failą dėl teisingų konfigūracijos nustatymų.


### version

Norėdami patikrinti įdiegtą *dignacli* versiją, naudokite parinktį --version.  
  
#### Komandos naudojimas
```bash
dignacli --version
```
  
#### Pavyzdinė išvestis
```bash
dignacli version 2026.01
```

### žurnalo parinktys
  
Pagal numatytuosius nustatymus konsolės išvestis iš ***digna*** komandų yra minimalistinė. Dauguma komandų leidžia pateikti papildomą informaciją naudojant šias parinktis:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ir „debug“ nustato išsamumo lygį, o „logfile“ perjungiklis leidžia nukreipti išvestį į failą vietoje konsolės lango.

## Vartotojų valdymas

### add-user
  
Komanda add-user ***digna*** CLI naudojama pridėti naują vartotoją į ***digna*** sistemą.
  
#### Komandos naudojimas
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentai

- **USER_NAME**: Naujo vartotojo vartotojo vardas (privalomas).
- **USER_FULL_NAME**: Naujo vartotojo pilnas vardas (privalomas).
- **USER_PASSWORD**: Naujo vartotojo slaptažodis (privalomas).

#### Parinktys

- `--is_superuser`, `-su`: Žymė skirta paskirti naują vartotoją kaip administratorių.
- `--valid_until`, `-vu`: Nustato vartotojo paskyros galiojimo pabaigos datą formatu `YYYY-MM-DD HH:MI:SS`. Jei nenurodoma, paskyra neturi galiojimo pabaigos.

#### Pavyzdys

Norint pridėti naują vartotoją su vartotojo vardu `jdoe`, pilnu vardu `John Doe` ir slaptažodžiu `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Norint pridėti naują vartotoją ir nustatyti paskyros galiojimo datą:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Komanda `delete-user` ***digna*** CLI naudojama pašalinti esamą vartotoją iš ***digna*** sistemos.
  
#### Komandos naudojimas
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentai
- **USER_NAME**: Vartotojo, kurį reikia ištrinti, vartotojo vardas (privalomas). Tai yra vienintelis komandos reikalaujamas argumentas.

#### Pavyzdys
```bash
dignacli delete-user jdoe
```
  
Vykdant šią komandą, vartotojas `jdoe` bus pašalintas iš ***digna*** sistemos, atšaukiant jo prieigą ir ištrynus susijusius duomenis bei teises iš saugyklos.

### modify-user

Komanda `modify-user` ***digna*** CLI naudojama atnaujinti esamo vartotojo duomenis ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentai
  
- **USER_NAME**: Vartotojo, kurį reikia modifikuoti, vartotojo vardas (privalomas).
- **USER_FULL_NAME**: Naujas vartotojo pilnas vardas (privalomas).
  
#### Parinktys  
  
- `--is_superuser`, `-su`: Nustato vartotoją kaip supervartotoją, suteikiant aukštesnes teises. Ši žymė nereikalauja reikšmės.  
- `--valid_until`, `-vu`: Nustato paskyros galiojimo pabaigos datą formatu YYYY-MM-DD HH:MI:SS. Jei nenurodoma, paskyra lieka galiojanti neribotai.  
  
#### Pavyzdys
  
Norint pakeisti vartotojo `jdoe` pilną vardą į „Johnathan Doe“ ir paskirti vartotoją supervartotoju:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Komanda `modify-user-pwd` ***digna*** CLI naudojama pakeisti esamo vartotojo slaptažodį ***digna*** sistemoje.
  
#### Komandos naudojimas
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumentai
  
- **USER_NAME**: Vartotojo, kurio slaptažodis keičiant, vartotojo vardas (privalomas).
- **USER_PWD**: Naujas vartotojo slaptažodis (privalomas).
  
#### Pavyzdys
  
Norint pakeisti vartotojo `jdoe` slaptažodį į `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Komanda `list-users` ***digna*** CLI parodo visų registruotų vartotojų sąrašą ***digna*** sistemoje.

#### Komandos naudojimas

```bash
dignacli list-users
```

Vykdant šią komandą ***digna*** CLI prisijungs prie ***digna*** saugyklos ir išves visų vartotojų sąrašą, rodydama jų ID, vartotojo vardą, pilną vardą, supervartotojo statusą ir galiojimo laiko žymes.

## Saugyklos valdymas

### upgrade-repo
  
Komanda `upgrade-repo` ***digna*** CLI naudojama atnaujinti arba inicializuoti ***digna*** saugyklą. Ši komanda yra būtina taikant atnaujinimus arba nustatant saugyklos infrastruktūrą pirmą kartą.
  
#### Komandos naudojimas

```bash
dignacli upgrade-repo [options]
```
  
#### Parinktys
  
- `--simulation-mode`, `-s`: Įjungus, komanda veikia simuliacijos režimu — spausdina SQL užklausas, kurios būtų vykdomos, bet jų realiai nevykdo. Tai naudinga peržiūrėti pokyčius nekeičiant saugyklos.  

  
#### Pavyzdys
  
Norint atnaujinti ***digna*** saugyklą, galite vykdyti komandą be jokių parinkčių:
  
```bash
dignacli upgrade-repo
```  
Norint paleisti atnaujinimą simuliacijos režimu (pamatyti SQL užklausas be jų taikymo):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ši komanda yra svarbi ***digna*** sistemos priežiūrai, užtikrinant, kad duomenų bazės schema ir kiti saugyklos komponentai atitiktų naujausią programinės įrangos versiją.

### encrypt
  
Komanda `encrypt` ***digna*** CLI naudojama užšifruoti slaptažodį.
  
#### Komandos naudojimas
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentai
- **PASSWORD**: Slaptažodis, kurį reikia užšifruoti (privalomas).
  
#### Pavyzdys
  
Norint užšifruoti slaptažodį, jį reikia pateikti kaip argumentą.   
Pavyzdžiui, norint užšifruoti slaptažodį `mypassword123`, naudokite:
```bash
dignacli encrypt mypassword123
```
Ši komanda išves pateikto slaptažodžio užšifruotą versiją, kuri vėliau gali būti naudojama saugiose vietose. Jei slaptažodžio argumentas nepateikiamas, CLI parodys klaidą, nurodančią trūkstamą argumentą.

### generate-key
  
Komanda `generate-key` naudojama sugeneruoti Fernet raktą, kuris yra būtinas saugant slaptažodžius užšifruotus ***digna*** saugykloje.
  
#### Komandos naudojimas
```bash
dignacli generate-key
```
  
## Duomenų valdymas

### clean-up

Komanda `clean-up` ***digna*** CLI naudojama pašalinti profilius, prognozes ir šviesoforo (traffic light) sistemos duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda yra svarbi duomenų gyvavimo ciklo valdymui, padedant palaikyti tvarkingą ir efektyvią duomenų aplinką bei ištrinti pasenusius ar nereikalingus duomenis.

#### Komandos naudojimas

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto, iš kurio bus pašalinami duomenys, pavadinimas (privalomas). Naudojant raktinį žodį all-projects šiame argumente nurodoma ***digna*** iteruoti per visus egzistuojančius projektus ir pritaikyti komandą visiems.
- **FROM_DATE**: Duomenų pašalinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų pašalinimo pabaigos data ir laikas, naudojant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys
  
- `--table-name`, `-tn`: Apriboja valymą konkrečiai lentelėi projekte.
- `--table-filter`, `-tf`: Filtras, leidžiantis valymą atlikti tik lentelėms, kurių pavadinimuose yra nurodyta potekstė.
- `--timing`, `-tm`: Parodo valymo proceso trukmę po užbaigimo.
- `--help`: Parodo pagalbą apie clean-up komandą ir išeina.
  
#### Pavyzdys
  
Norint pašalinti duomenis iš projekto ProjectA tarp 2023-01-01 ir 2023-06-30:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Norint pašalinti duomenis tik iš konkrečios `Table1` lentelės:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ši komanda padeda valdyti duomenų saugyklą ir užtikrinti, kad saugykloje būtų tik aktuali informacija.

### remove-orphans
  
Komanda `remove-orphans` ***digna*** CLI naudojama saugyklos „tvarkymui“.  
Kai vartotojas ištrina projektus arba duomenų šaltinius, profiliai ir prognozės gali likti saugykloje. Ši komanda pašalins tokius bešeimininkių (orphan) įrašus iš saugyklos.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

### list-projects
  
Komanda `list-projects` ***digna*** CLI naudojama parodyti visų prieinamų projektų sąrašą ***digna*** sistemoje.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

Ši komanda ypač naudinga administratoriams ir vartotojams, valdantiems kelis projektus, suteikiant greitą apžvalgą apie prieinamus projektus ***digna*** saugykloje.

### list-ds

Komanda `list-ds` ***digna*** CLI naudojama parodyti visų prieinamų duomenų šaltinių sąrašą nurodytame projekte. Ši komanda padeda suprasti analizės ir valdymo objektus, prieinamus ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentai
- **PROJECT_NAME**: Projekto, kurio duomenų šaltiniai yra listinami, pavadinimas (privalomas).
  
#### Pavyzdys
  
Norint išvardinti visus duomenų šaltinius projekte `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ši komanda suteikia vartotojams apžvalgą apie projekte prieinamus duomenų šaltinius, padedant geriau valdyti duomenų kraštovaizdį.


### inspect

Komanda `inspect` ***digna*** CLI naudojama sukurti profilius, prognozes ir šviesoforo sistemos duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis per apibrėžtą laikotarpį. Baigus inspekciją, grąžinama apskaičiuoto šviesoforo sistemos reikšmė:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komandos naudojimas

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto, kurio duomenys bus tikrinami, pavadinimas (privalomas). Naudojant raktinį žodį all-projects šiame argumente nurodoma ***digna*** iteruoti per visus egzistuojančius projektus ir taikyti komandą visiems.
- **FROM_DATE**: Duomenų tikrinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų tikrinimo pabaigos data ir laikas, naudojant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja tikrinimą konkrečiai lentelėi projekte.
- `--table-filter`, `-tf`: Filtras, leidžiantis tikrinti tik lenteles, kurių pavadinimuose yra nurodyta potekstė.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą įspėjimų atveju.
- `--bypass-backend`, `-bb`: Apeiti backendą ir vykdyti inspekciją tiesiogiai iš CLI (tik testavimo tikslais!).

  
#### Pavyzdys
  
Norint patikrinti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Norint tikrinti tik konkrečią lentelę ir priversti prognozių perskaičiavimą:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ši komanda naudinga generuojant atnaujintus profilius ir prognozes, stebint duomenų vientisumą ir valdant įspėjimų sistemas nurodytu projekto laikotarpiu.

### inspect-async

Komanda `inspect-async` ***digna*** CLI naudojama sukurti profilius, prognozes ir šviesoforo sistemos duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis per apibrėžtą laikotarpį. Skirtingai nuo sinchroninės inspekcijos, ši komanda nelaukiama inspekcijos pabaigos — ji grąžina pateikto užklausos ID. Norėdami tikrinti inspekcijos pažangą, naudokite komandą `inspect-status`.

#### Komandos naudojimas

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto, kurio duomenys bus tikrinami, pavadinimas (privalomas). Naudojant raktinį žodį all-projects šiame argumente nurodoma ***digna*** iteruoti per visus egzistuojančius projektus ir taikyti komandą visiems.
- **FROM_DATE**: Duomenų tikrinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų tikrinimo pabaigos data ir laikas, naudojant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja tikrinimą konkrečiai lentelėi projekte.
- `--table-filter`, `-tf`: Filtras, leidžiantis tikrinti tik lenteles, kurių pavadinimuose yra nurodyta potekstė.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą įspėjimų atveju.

  
#### Pavyzdys
  
Norint inicijuoti asimptotinę inspekciją projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Komanda `inspect-status` ***digna*** CLI naudojama patikrinti asinchroninės inspekcijos pažangą pagal užklausos ID.

#### Komandos naudojimas

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentai
  
- **REQUEST_ID**: Užklausos ID, kurį grąžino komanda `inspect-async`.
  
#### Pavyzdys
  
Norint patikrinti inspekcijos pažangą su užklausos ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Komanda `inspect-cancel` ***digna*** CLI naudojama atšaukti inspekcijas pagal užklausos ID arba atšaukti visas esamas užklausas.

#### Komandos naudojimas

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentai
  
- **REQUEST_ID**: Užklausos ID, kurį grąžino komanda `inspect-async`.
  
#### Pavyzdys
  
Norint atšaukti inspekciją su užklausos ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Norint atšaukti visas šiuo metu vykdomas arba laukiančias užklausas:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Komanda `export-ds` ***digna*** CLI naudojama sukurti duomenų šaltinių eksportą iš ***digna*** saugyklos. Pagal numatytuosius nustatymus bus eksportuoti visi duomenų šaltiniai iš nurodyto projekto.

#### Komandos naudojimas
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, iš kurio bus eksportuojami duomenų šaltiniai, pavadinimas.

#### Parinktys

- `--table_name`, `-tn`: Eksportuoti konkretų duomenų šaltinį iš projekto.
- `--exportfile`, `-ef`: Nurodyti eksportui naudojamą failo pavadinimą.
    
#### Pavyzdys
  
Norint eksportuoti visus duomenų šaltinius iš projekto `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ši komanda eksportuoja visus `ProjectA` duomenų šaltinius kaip JSON dokumentą, kurį galima importuoti į kitą projektą arba ***digna*** saugyklą.


### import-ds

Komanda `import-ds` ***digna*** CLI naudojama importuoti duomenų šaltinius į tikslinį projektą ir sukurti importo ataskaitą.

#### Komandos naudojimas
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, į kurį bus importuojami duomenų šaltiniai, pavadinimas.
- **EXPORT_FILE**: Eksporto failo, kurį reikia importuoti, pavadinimas.

#### Parinktys

- `--output-file`, `-o`: Failas, kuriame išsaugoti importo ataskaitą (jei nenurodoma, ataskaita spausdinama terminale lentelės formatu).
- `--output-format`, `-f`: Formatą, kuriuo išsaugoti importo ataskaitą (json, csv).
    
#### Pavyzdys
  
Norint importuoti visus duomenų šaltinius iš eksporto failo `my_export.json` į `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importo ši komanda taip pat parodys ataskaitą apie importuotus ir praleistus objektus. Į `ProjectB` bus importuoti tik nauji duomenų šaltiniai. Norėdami sužinoti, kurie objektai būtų importuoti ir kurie praleisti, galite naudoti komandą `plan-import-ds`.

### plan-import-ds

Komanda `plan-import-ds` ***digna*** CLI naudojama analizuoti duomenų šaltinių eksportą prieš importą ir sukurti importo planą.

#### Komandos naudojimas
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, į kurį būtų importuojami duomenų šaltiniai, pavadinimas.
- **EXPORT_FILE**: Eksporto failo, kuris bus analizuojamas prieš importą, pavadinimas.

#### Parinktys

- `--output-file`, `-o`: Failas, kuriame išsaugoti importo ataskaitą (jei nenurodoma, ataskaita spausdinama terminale lentelės formatu).
- `--output-format`, `-f`: Formatą, kuriuo išsaugoti importo ataskaitą (json, csv).
    
#### Pavyzdys
  
Norint patikrinti, kurie duomenų šaltiniai būtų importuoti ir kurie būtų praleisti iš eksporto failo `my_export.json` importuojant į `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ši komanda tik parodys importo planą su objektais, kurie būtų importuoti arba praleisti.