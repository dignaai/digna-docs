# digna CLI Reference 2026.04
**2026-04-08**

Šiame puslapyje dokumentuojamas pilnas komandų rinkinys, prieinamas ***digna*** CLI leidime **2026.04**, įskaitant naudojimo pavyzdžius ir parinktis.

---

## CLI Basics

---

### help
Parinktis `--help` pateikia informaciją apie prieinamas komandas ir jų naudojimą. Yra du pagrindiniai būdai naudoti šią parinktį:

1. **Bendros pagalbos rodymas:**
   
    Naudokite `--help` iškart po raktažodžio `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Pagalba konkrečioms komandoms:**  
  
    Norėdami gauti išsamią informaciją apie tam tikrą komandą, pridėkite `--help` prie tos komandos.
    Pavyzdžiui, kad gauti pagalbą apie komandą `add-user`, vykdykite:
     ```bash
     dignacli add-user --help
     ```

     ### išvestis:
      
     - **Komandos aprašymas:** Išsamiai paaiškina, ką atlieka komanda.  
     - **Sintaksė:** Rodo tikslią sintaksę, įskaitant privalomus ir pasirenkamus argumentus.  
     - **Parinktys:** Išvardina konkrečias komandos parinktis ir jų paaiškinimus.  
     - **Pavyzdžiai:** Pateikia pavyzdžius, kaip efektyviai vykdyti komandą.

### check-config

Komanda `check-config` yra įrankis ***digna*** CLI, skirtas patikrinti ***digna*** konfigūraciją. Ši komanda užtikrina, kad ***digna*** komponentai gali rasti reikiamus konfigūracijos elementus faile config.toml.

#### Parinktys

- `--configpath`, `-cp`: Failas arba katalogas, kuriame yra konfigūracija. Jei neužduodama, bus naudojamas ../config.toml.
      
#### Komandos naudojimas
```bash
dignacli check-config
```

Sėkmingai įvykdžius komandą, išvedamas patvirtinimas apie konfigūracijos pilnumą.  
  
Jei konfigūracija yra neišsami, bus išvardyti trūkstami konfigūracijos elementai.

  
### check-repo-connection

Komanda `check-repo-connection` yra įrankis ***digna*** CLI, skirtas patikrinti ryšį ir prieigą prie nurodyto ***digna*** repository. Ši komanda užtikrina, kad CLI gali bendrauti su repozitorija.
      
#### Komandos naudojimas
```bash
dignacli check-repo-connection
```

Sėkmingai įvykdžius komandą, išvedamas patvirtinimas apie prisijungimą, kartu su informacija apie repozitoriją: repozitorijos versija, hostas, duomenų bazė ir schema.  
  
Jei ryšys su repozitorija nėra sėkmingas, patikrinkite config.toml faile nurodytus konfigūracijos nustatymus.


### version

Norėdami patikrinti įdiegtą *dignacli* versiją, naudokite parinktį `--version`.  
  
#### Komandos naudojimas
```bash
dignacli --version
```
  
#### Pavyzdinė išvestis
```bash
dignacli version 2026.04
```

### logging options
  
Numatyta, kad konsolės išvestis iš ***digna*** komandų yra minimalistinė. Dauguma komandų leidžia pateikti papildomą informaciją naudojant šias parinktis:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ir „debug“ apibrėžia informacijos detalių lygį, tuo tarpu perjungimas „logfile“ leidžia nukreipti išvestį į failą, o ne į konsolę.

## Vartotojų valdymas

### add-user
  
Komanda `add-user` ***digna*** CLI naudojama pridėti naują vartotoją į ***digna*** sistemą.
  
#### Komandos naudojimas
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentai

- **USER_NAME**: Naujo vartotojo prisijungimo vardas (privalomas).
- **USER_FULL_NAME**: Naujo vartotojo pilnas vardas (privalomas).
- **USER_PASSWORD**: Naujo vartotojo slaptažodis (privalomas).

#### Parinktys

- `--is_superuser`, `-su`: Žymė nurodanti, kad naujas vartotojas yra administratorius.
- `--valid_until`, `-vu`: Nustato vartotojo paskyros galiojimo datą formatu `YYYY-MM-DD HH:MI:SS`. Jei nenurodyta, paskyra neturi galiojimo pabaigos.

#### Pavyzdys

Norint pridėti naują vartotoją su prisijungimo vardu `jdoe`, pilnu vardu `John Doe` ir slaptažodžiu `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Norint pridėti vartotoją ir nustatyti paskyros galiojimo datą:
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
- **USER_NAME**: Vartotojo, kurį reikia pašalinti, prisijungimo vardas (privalomas). Tai vienintelis komandos reikalingas argumentas.

#### Pavyzdys
```bash
dignacli delete-user jdoe
```
  
Vykdant šią komandą vartotojas `jdoe` bus pašalintas iš ***digna*** sistemos, atimant jo prieigą ir ištrinant susijusius duomenis bei teises repozitorijoje.

### modify-user

Komanda `modify-user` ***digna*** CLI naudojama atnaujinti esamo vartotojo informaciją ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumentai
  
- **USER_NAME**: Vartotojo, kurį reikia keisti, prisijungimo vardas (privalomas).
- **USER_FULL_NAME**: Naujas vartotojo pilnas vardas (privalomas).
  
#### Parinktys  
  
- `--is_superuser`, `-su`: Pažymi vartotoją kaip superuserį, suteikiant didesnes teises. Šis ženklas nereikalauja reikšmės.  
- `--valid_until`, `-vu`: Nustato paskyros galiojimo datą formatu YYYY-MM-DD HH:MI:SS. Jei nenurodoma, paskyra lieka galiojanti neribotai.  
  
#### Pavyzdys
  
Norint pakeisti vartotojo `jdoe` pilną vardą į „Johnathan Doe“ ir pažymėti vartotoją kaip superuserį:
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
  
- **USER_NAME**: Vartotojo, kurio slaptažodis keičiamas, prisijungimo vardas (privalomas).
- **USER_PWD**: Naujas vartotojo slaptažodis (privalomas).
  
#### Pavyzdys
  
Norint pakeisti vartotojo `jdoe` slaptažodį į `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Komanda `list-users` ***digna*** CLI parodo visų ***digna*** sistemoje užregistruotų vartotojų sąrašą.

#### Komandos naudojimas

```bash
dignacli list-users
```

Vykdant šią komandą ***digna*** CLI prisijungs prie ***digna*** repozitorijos ir išves visų vartotojų sąrašą, rodant jų ID, prisijungimo vardą, pilną vardą, superuser statusą ir galiojimo laikus.

## Repozitorijos valdymas

### upgrade-repo
  
Komanda `upgrade-repo` ***digna*** CLI naudojama atnaujinti arba inicializuoti ***digna*** repozitoriją. Ši komanda yra būtina taikant atnaujinimus arba ruošiant repozitorijos infrastruktūrą pirmą kartą.
  
#### Komandos naudojimas

```bash
dignacli upgrade-repo [options]
```
  
#### Parinktys
  
- `--simulation-mode`, `-s`: Įjungus šią parinktį, komanda vykdoma simuliacijos režimu — spausdinamos SQL užklausos, kurios būtų vykdomos, bet jos faktiškai nevykdomos. Tai naudinga norint peržiūrėti pakeitimus prieš juos taikant.  

  
#### Pavyzdys
  
Norėdami atnaujinti ***digna*** repozitoriją, galite vykdyti komandą be parinkčių:
  
```bash
dignacli upgrade-repo
```  
Norėdami vykdyti atnaujinimą simuliacijos režimu (pamatyti SQL užklausas neTaikant jų):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ši komanda yra svarbi palaikant ***digna*** sistemą, užtikrinant, kad duomenų bazės schema ir kiti repozitorijos komponentai atitiktų programinės įrangos versiją.

### encrypt
  
Komanda `encrypt` ***digna*** CLI naudojama užšifruoti slaptažodį.
  
#### Komandos naudojimas
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentai
- **PASSWORD**: Slaptažodis, kurį reikia užšifruoti (privalomas).
  
#### Pavyzdys
  
Norint užšifruoti slaptažodį, reikia pateikti slaptažodį kaip argumentą.   
Pavyzdžiui, norint užšifruoti slaptažodį `mypassword123`, naudokite:
```bash
dignacli encrypt mypassword123
```
Ši komanda išves pateikto slaptažodžio užšifruotą versiją, kurią vėliau galima naudoti saugioje aplinkoje. Jei slaptažodis nėra pateiktas, CLI parodys klaidos pranešimą apie trūkstamą argumentą.

### generate-key
  
Komanda `generate-key` naudojama sugeneruoti Fernet raktą, kuris yra būtinas saugant slaptažodžius užšifruotus ***digna*** repozitorijoje.
  
#### Komandos naudojimas
```bash
dignacli generate-key
```
  
## Duomenų valdymas

### clean-up

Komanda `clean-up` ***digna*** CLI naudojama šalinti profilius, prognozes ir šviesoforo sistemos duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda yra svarbi duomenų gyvavimo ciklo valdymui, padedant išlaikyti tvarkingą ir efektyvią duomenų aplinką ištrinant pasenusius ar nereikalingus duomenis.

#### Komandos naudojimas

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, iš kurio bus pašalinami duomenys (privalomas). Naudojant raktinį žodį `all-projects` šiame argumente, ***digna*** iteruos per visus esamus projektus ir taikys komandą kiekvienam.
- **FROM_DATE**: Duomenų šalinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų šalinimo pabaigos data ir laikas, pagal tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys
  
- `--table-name`, `-tn`: Apriboja valymą konkrečiai lentelei projekte.
- `--table-filter`, `-tf`: Filtras, leidžiantis valymą riboti lentelėms, kurių pavadinimuose yra nurodytas potekstis.
- `--timing`, `-tm`: Po užbaigimo parodo valymo proceso trukmę.
- `--help`: Parodo pagalbą apie clean-up komandą ir išeina.
  
#### Pavyzdys
  
Norint pašalinti duomenis iš projekto ProjectA nuo 2023-01-01 iki 2023-06-30:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Norint pašalinti duomenis tik iš konkrečios lentelės pavadinimu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ši komanda padeda valdyti saugyklos apimtį ir užtikrina, kad repozitorijoje liktų tik aktuali informacija.

### remove-orphans
  
Komanda `remove-orphans` ***digna*** CLI naudojama repozitorijos tvarkymui.  
Kai vartotojas ištrina projektus ar duomenų šaltinius, profiliai ir prognozės gali likti repozitorijoje. Vykdant šią komandą, tokie „ūkiniai“ (orphan) įrašai bus pašalinti iš repozitorijos.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

### list-projects
  
Komanda `list-projects` ***digna*** CLI naudojama parodyti visų galimų projektų sąrašą ***digna*** sistemoje.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

Ši komanda ypač naudinga administratoriams ir vartotojams valdantiems kelis projektus — suteikia greitą peržiūrą apie prieinamus projektus repozitorijoje.

### list-ds

Komanda `list-ds` ***digna*** CLI naudojama parodyti visų duomenų šaltinių sąrašą nurodytame projekte. Ši komanda naudinga norint suprasti, kokie duomenų ištekliai yra prieinami analizėms ir valdymui ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentai
- **PROJECT_NAME**: Projekto pavadinimas, kurio duomenų šaltiniai yra išvedami (privalomas).
  
#### Pavyzdys
  
Norėdami išvardinti visus duomenų šaltinius projekte `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ši komanda suteikia vartotojams apžvalgą apie projekte prieinamus duomenų šaltinius, palengvindama jų valdymą ir orientaciją duomenų peizaže.


### inspect

Komanda `inspect` ***digna*** CLI naudojama kurti profilius, prognozes ir šviesoforo sistemos duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis per nurodytą laikotarpį. Baigus patikrinimą, grąžinama apskaičiuotos šviesoforo sistemos reikšmė:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komandos naudojimas

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kurio duomenys bus tikrinami (privalomas). Naudojant raktinį žodį `all-projects` šiame argumente, ***digna*** iteruos per visus esamus projektus ir taikys komandą kiekvienam.
- **FROM_DATE**: Pradžios data ir laikas duomenų tikrinimui. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Pabaigos data ir laikas duomenų tikrinimui, pagal tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja tikrinimą konkrečiai lentelei projekte.
- `--table-filter`, `-tf`: Filtras, leidžiantis tikrinti tik tas lenteles, kurių pavadinimuose yra nurodytas potekstis.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą alertų atveju.
- `--bypass-backend`, `-bb`: Apeina backendą ir vykdo tikrinimą tiesiogiai iš CLI (skirta tik testavimui!).

  
#### Pavyzdys
  
Norint patikrinti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Norint patikrinti tik konkrečią lentelę ir priversti prognozių perskaičiavimą:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ši komanda naudinga generuoti atnaujintus profilius ir prognozes, stebėti duomenų vientisumą ir valdyti alertų sistemą nurodytu projekto laiko tarpu.

### inspect-async

Komanda `inspect-async` ***digna*** CLI naudojama kurti profilius, prognozes ir šviesoforo sistemos duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Skirtingai nei sinchroninė `inspect` komanda, ši komandą nepalaukia patikrinimo pabaigos — vietoje to grąžina užklausos ID pateiktam asinchroniniam patikrinimui. Norėdami patikrinti patikrinimo proceso būseną, naudokite komandą `inspect-status`.

#### Komandos naudojimas

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kurio duomenys bus tikrinami (privalomas). Naudojant raktinį žodį `all-projects` šiame argumente, ***digna*** iteruos per visus esamus projektus ir taikys komandą kiekvienam.
- **FROM_DATE**: Pradžios data ir laikas duomenų tikrinimui. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Pabaigos data ir laikas duomenų tikrinimui, pagal tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja tikrinimą konkrečiai lentelei projekte.
- `--table-filter`, `-tf`: Filtras, leidžiantis tikrinti tik tas lenteles, kurių pavadinimuose yra nurodytas potekstis.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą alertų atveju.

  
#### Pavyzdys
  
Norint asinchroniškai patikrinti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Komanda `inspect-status` ***digna*** CLI naudojama patikrinti asinchroninio patikrinimo pažangą, pagal užklausos ID.

#### Komandos naudojimas

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumentai
  
- **REQUEST_ID**: Užklausos ID, kurį grąžino komanda `inspect-async`. 
  
#### Pavyzdys
  
Norint patikrinti patikrinimo pažangą su užklausos ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Komanda `inspect-cancel` ***digna*** CLI naudojama atšaukti patikrinimus pagal užklausos ID arba atšaukti visus einamus ir laukiančius užsakymus.

#### Komandos naudojimas

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumentai
  
- **REQUEST_ID**: Užklausos ID, kurį grąžino komanda `inspect-async`. 
  
#### Pavyzdys
  
Norint atšaukti patikrinimą su užklausos ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Norint atšaukti visus šiuo metu vykdomus arba laukiančius užsakymus:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Komanda `export-ds` ***digna*** CLI naudojama sukurti duomenų šaltinių eksportą iš ***digna*** repozitorijos. Pagal numatytuosius nustatymus bus eksportuoti visi duomenų šaltiniai iš nurodyto projekto.

#### Komandos naudojimas
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, iš kurio bus eksportuojami duomenų šaltiniai, pavadinimas.

#### Parinktys

- `--table_name`, `-tn`: Eksportuoja konkretų duomenų šaltinį iš projekto.
- `--exportfile`, `-ef`: Nustato failo vardą eksportui.
    
#### Pavyzdys
  
Norint eksportuoti visus duomenų šaltinius iš projekto `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ši komanda eksportuos visus `ProjectA` duomenų šaltinius kaip JSON dokumentą, kurį galima importuoti į kitą projektą arba ***digna*** repozitoriją.


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

- `--output-file`, `-o`: Failas importo ataskaitai išsaugoti (jei nenurodoma, ataskaita spausdinama terminale lentelės formatu).
- `--output-format`, `-f`: Formatą ataskaitai išsaugoti (json, csv).
    
#### Pavyzdys
  
Norint importuoti visus duomenų šaltinius iš eksporto failo `my_export.json` į `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importo ši komanda taip pat parodys ataskaitą apie importuotus ir praleistus objektus. Į `ProjectB` bus importuoti tik nauji duomenų šaltiniai. Norint sužinoti, kurie objektai būtų importuojami arba praleidžiami, galite naudoti komandą `plan-import-ds`.

### plan-import-ds

Komanda `plan-import-ds` ***digna*** CLI naudojama suplanuoti duomenų šaltinių importą į tikslinį projektą ir sukurti importo ataskaitą prieš faktinį importą.

#### Komandos naudojimas
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, į kurį būtų importuojami duomenų šaltiniai, pavadinimas.
- **EXPORT_FILE**: Eksporto failo, kurį reikia išanalizuoti prieš importą, pavadinimas.

#### Parinktys

- `--output-file`, `-o`: Failas importo ataskaitai išsaugoti (jei nenurodoma, ataskaita spausdinama terminale lentelės formatu).
- `--output-format`, `-f`: Formatą ataskaitai išsaugoti (json, csv).
    
#### Pavyzdys
  
Norint patikrinti, kurie duomenų šaltiniai būtų importuoti ir kurie praleisti iš eksporto failo `my_export.json` importuojant į `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ši komanda tik parodys importo planą su objektais, kurie būtų importuoti ir praleisti.