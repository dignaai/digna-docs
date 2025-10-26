---
title: digna CLI Reference 2025.09 – Komandos ir Pavyzdžiai | digna Dokumentacija
description: Išsamus digna CLI leidimo 2025.109 nuorodinis vadovas. Sužinokite, kaip valdyti naudotojus, saugyklas ir duomenis naudojant komandas, tokias kaip add-user, check-config, check-repo-connection, inspect, inspect-async ir kt.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Šiame puslapyje dokumentuojamas visas komandų rinkinys, prieinamas ***digna*** CLI leidime **2025.09**, įskaitant naudojimo pavyzdžius ir parinktis.

---

## CLI pagrindai

---

### help
Parinktis `--help` pateikia informaciją apie galimas komandas ir jų naudojimą. Yra du pagrindiniai būdai naudoti šią parinktį:

1. **Bendros pagalbos rodymas:**
   
    Naudokite –help iškart po raktažodžio ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Pagalba konkrečioms komandoms:**  
  
    Norėdami gauti išsamią informaciją apie konkrečią komandą, pridėkite `--help` prie tos komandos.
    Pavyzdžiui, norėdami gauti pagalbą su komanda `add-user`, vykdykite:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Komandos aprašymas:** Išsamiai paaiškina, ką atlieka komanda.  
     - **Sintaksė:** Rodo tikslią sintaksę, įskaitant privalomus ir pasirenkamus argumentus.  
     - **Parinktys:** Išvardija komandos specifines parinktis su paaiškinimais.  
     - **Pavyzdžiai:** Pateikia pavyzdžių, kaip efektyviai vykdyti komandą.

### check-config

Komanda check-config yra įrankis ***digna*** CLI, skirtas patikrinti ***digna*** konfigūraciją. Ši komanda užtikrina, kad ***digna*** komponentai galėtų rasti reikiamus konfigūracijos elementus faile config.toml.

#### Parinktys

- `--configpath`, `-cp`: Failas arba katalogas, kuriame yra konfigūracija. Jei nenurodyta, bus naudojamas ../config.toml.
      
#### Komandos naudojimas
```bash
dignacli check-config
```

Sėkmingai įvykdžius, komanda išveda patvirtinimą apie konfigūracijos pilnumą.  
  
Jei konfigūracija atrodo nepilna, bus išvardinti trūkstami konfigūracijos elementai.

  
### check-repo-connection

Komanda check-repo-connection yra įrankis ***digna*** CLI, skirtas patikrinti ryšį ir prieigą prie nurodytos ***digna*** saugyklos. Ši komanda užtikrina, kad CLI gali bendrauti su saugykla.
      
#### Komandos naudojimas
```bash
dignacli check-repo-connection
```

Sėkmingai įvykdžius, komanda pateiks patvirtinimą apie ryšį ir duomenis apie saugyklą: Repository version, Host, Database and Schema.  
  
Jei ryšys su saugykla nepavyksta, patikrinkite config.toml failą dėl teisingų konfigūracijos nustatymų.


### version

Norėdami patikrinti įdiegtą *dignacli* versiją, naudokite parinktį --version.  
  
#### Komandos naudojimas
```bash
dignacli --version
```
  
#### Pavyzdinė išvestis
```bash
dignacli version 2025.09
```

### registravimo (logging) parinktys
  
Pagal nutylėjimą ***digna*** komandų konsolės išvestis yra minimali. Dauguma komandų leidžia pateikti papildomą informaciją naudojant šias parinktis:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ir „debug“ nustato detalumo lygį, o „logfile“ jungiklis leidžia nukreipti išvestį į failą vietoj konsolės lango.

## Vartotojų valdymas

### add-user
  
Komanda add-user ***digna*** CLI naudojama pridėti naują vartotoją į ***digna*** sistemą.
  
#### Komandos naudojimas
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumentai

- **USER_NAME**: Naujo vartotojo prisijungimo vardas (privalomas).
- **USER_FULL_NAME**: Naujo vartotojo pilnas vardas (privalomas).
- **USER_PASSWORD**: Naujo vartotojo slaptažodis (privalomas).

#### Parinktys

- `--is_superuser`, `-su`: Žymė, skirianti naują vartotoją kaip administratorių.
- `--valid_until`, `-vu`: Nustato vartotojo paskyros galiojimo pabaigos datą formatu `YYYY-MM-DD HH:MI:SS`. Jei nenurodyta, paskyra neturi galiojimo termino.

#### Pavyzdys

Norėdami pridėti naują vartotoją su prisijungimo vardu `jdoe`, pilnu vardu `John Doe` ir slaptažodžiu `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Norėdami pridėti naują vartotoją ir nustatyti paskyros galiojimo pabaigos datą:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Komanda `delete-user` ***digna*** CLI naudojama pašalinti esantį vartotoją iš ***digna*** sistemos.
  
#### Komandos naudojimas
```bash
dignacli delete-user USER_NAME
```
  
#### Argumentai
- **USER_NAME**: Vartotojo, kurį reikia ištrinti, prisijungimo vardas (privalomas). Tai vienintelis komandos reikalaujamas argumentas.

#### Pavyzdys
```bash
dignacli delete-user jdoe
```
  
Vykdant šią komandą vartotojas `jdoe` bus pašalintas iš ***digna*** sistemos, atimant prieigą ir ištrinant susijusius duomenis bei leidimus iš saugyklos.

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
  
- `--is_superuser`, `-su`: Nustato vartotoją kaip superuser’į, suteikiant aukštesnius privilegijų lygius. Ši žymė nereikalauja reikšmės.  
- `--valid_until`, `-vu`: Nustato paskyros galiojimo pabaigos datą formatu YYYY-MM-DD HH:MI:SS. Jei nenurodyta, paskyra lieka galiojanti neribotą laiką.  
  
#### Pavyzdys
  
Norėdami pakeisti vartotojo `jdoe` pilną vardą į „Johnathan Doe“ ir nustatyti vartotoją kaip superuser’į:
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
  
Norėdami pakeisti vartotojo `jdoe` slaptažodį į `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Komanda `list-users` ***digna*** CLI rodo visų registruotų vartotojų sąrašą ***digna*** sistemoje.

#### Komandos naudojimas

```bash
dignacli list-users
```

Vykdant šią komandą ***digna*** CLI prisijungs prie ***digna*** saugyklos ir išves visų vartotojų sąrašą, rodydama jų ID, prisijungimo vardą, pilną vardą, superuser statusą ir galiojimo laikus.

## Saugyklos valdymas

### upgrade-repo
  
Komanda `upgrade-repo` ***digna*** CLI naudojama atnaujinti arba inicializuoti ***digna*** saugyklą. Ši komanda yra būtina taikant atnaujinimus arba pirmą kartą nustatant saugyklos infrastruktūrą.
  
#### Komandos naudojimas

```bash
dignacli upgrade-repo [options]
```
  
#### Parinktys
  
- `--simulation-mode`, `-s`: Įjungus, komanda veikia simuliacijos režimu – išspausdina SQL užklausas, kurios būtų vykdomos, bet jų faktiškai nevykdo. Tai naudinga peržiūrėti pakeitimus nekeičiant saugyklos.  

  
#### Pavyzdys
  
Norėdami atnaujinti ***digna*** saugyklą, galite vykdyti komandą be parinkčių:
  
```bash
dignacli upgrade-repo
```  
Norėdami paleisti atnaujinimą simuliacijos režimu (pamatyti SQL užklausas neįvedant pakeitimų):
  
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
  
Norėdami užšifruoti slaptažodį, turite pateikti slaptažodį kaip argumentą.   
Pavyzdžiui, norėdami užšifruoti slaptažodį `mypassword123`, naudokite:
```bash
dignacli encrypt mypassword123
```
Ši komanda išves pateikto slaptažodžio užšifruotą versiją, kurią galima naudoti saugiose kontekstuose. Jei slaptažodžio argumentas nepateiktas, CLI pateiks klaidą apie trūkstamą argumentą.

### generate-key
  
Komanda `generate-key` naudojama sugeneruoti Fernet raktą, kuris yra būtinas saugoti slaptažodžius ***digna*** saugykloje.
  
#### Komandos naudojimas
```bash
dignacli generate-key
```
  
## Duomenų valdymas

### clean-up

Komanda `clean-up` ***digna*** CLI naudojama pašalinti profilius, prognozes ir šviesoforo (traffic light system) duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda yra svarbi duomenų gyvavimo ciklo valdymui, padedanti palaikyti tvarkingą ir efektyvią duomenų aplinką, išvalant pasenusius ar nereikalingus duomenis.

#### Komandos naudojimas

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto, iš kurio bus pašalinami duomenys, pavadinimas (privalomas). Naudojant raktinį žodį all-projects šiame argumente, ***digna*** iteruos per visus esamus projektus ir taikys komandą visiems.
- **FROM_DATE**: Duomenų šalinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų šalinimo pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys
  
- `--table-name`, `-tn`: Apriboja valymą iki konkrečios lentelės projekte.
- `--table-filter`, `-tf`: Filtruoja, kad valymas būtų taikomas tik lentelėms, kurių pavadinimuose yra nurodytas posakinys.
- `--timing`, `-tm`: Parodo operacijos trukmę po užbaigimo.
- `--help`: Parodo pagalbos informaciją apie komandą clean-up ir išeina.
  
#### Pavyzdys
  
Norėdami pašalinti duomenis iš projekto ProjectA nuo 2023-01-01 iki 2023-06-30:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Norėdami pašalinti duomenis tik iš konkrečios lentelės pavadinimu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ši komanda padeda valdyti duomenų saugyklą ir užtikrinti, kad saugykloje būtų tik aktuali informacija.

### remove-orphans
  
Komanda `remove-orphans` ***digna*** CLI naudojama saugyklos tvarkymui.  
Kai vartotojas ištrina projektus ar duomenų šaltinius, profiliai ir prognozės lieka saugykloje. Naudojant šią komandą, tokie „našlaičiai“ (orphaned rows) bus pašalinti iš saugyklos.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

### list-projects
  
Komanda `list-projects` ***digna*** CLI naudojama visų turimų projektų sąrašui rodyti ***digna*** sistemoje.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

Ši komanda ypač naudinga administratoriams ir vartotojams, valdantiems kelis projektus, suteikiant greitą apžvalgą apie prieinamus projektus ***digna*** saugykloje.

### list-ds

Komanda `list-ds` ***digna*** CLI naudojama visų turimų duomenų šaltinių sąrašui nurodytame projekte rodyti. Ši komanda naudinga norint suprasti, kokie duomenų ištekliai yra prieinami analizėms ir valdymui ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentai
- **PROJECT_NAME**: Projekto, kuriam bus rodomi duomenų šaltiniai, pavadinimas (privalomas).
  
#### Pavyzdys
  
Norėdami išvardinti visus duomenų šaltinius projekte `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ši komanda suteikia vartotojams apžvalgą apie projekto duomenų šaltinius, padedant efektyviau naršyti ir valdyti duomenų kraštovaizdį.


### inspect

Komanda `inspect` ***digna*** CLI naudojama sukurti profilius, prognozes ir šviesoforo (traffic light system) duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis nurodytame laikotarpyje. Baigus inspekciją, grąžinama apskaičiuotos šviesoforo sistemos reikšmė:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komandos naudojimas

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto, kurį reikia ištirti, pavadinimas (privalomas). Naudojant raktinį žodį all-projects šiame argumente, ***digna*** iteruos per visus esamus projektus ir taikys komandą visiems.
- **FROM_DATE**: Inspekcijos pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Inspekcijos pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja inspekciją iki konkrečios lentelės projekte.
- `--table-filter`, `-tf`: Filtruoja, kad būtų tikrinamos tik lentelės, kurių pavadinimuose yra nurodytas posakinys.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą įspėjimų atveju.
- `--bypass-backend`, `-bb`: Apeiti backend’ą ir vykdyti inspekciją tiesiogiai iš CLI (skirta tik testavimui!).

  
#### Pavyzdys
  
Norėdami ištirti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Norėdami ištirti tik konkrečią lentelę ir priversti prognozių perskaičiavimą:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ši komanda naudinga generuoti atnaujintus profilius ir prognozes, stebėti duomenų vientisumą ir valdyti įspėjimų sistemas nurodytame projekto laikotarpyje.

### inspect-async

Komanda `inspect-async` ***digna*** CLI naudojama sukurti profilius, prognozes ir šviesoforo (traffic light system) duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis nurodytame laikotarpyje. Skirtingai nei sinchroninė `inspect` komanda, ši komandą nevykdo laukdama užbaigimo.
Vietoje to ji grąžina pateikto užklausos ID. Norėdami patikrinti inspekcijos proceso eigą, naudokite komandą `inspect-status`.

#### Komandos naudojimas

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto, kurį reikia ištirti, pavadinimas (privalomas). Naudojant raktinį žodį all-projects šiame argumente, ***digna*** iteruos per visus esamus projektus ir taikys komandą visiems.
- **FROM_DATE**: Inspekcijos pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Inspekcijos pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja inspekciją iki konkrečios lentelės projekte.
- `--table-filter`, `-tf`: Filtruoja, kad būtų tikrinamos tik lentelės, kurių pavadinimuose yra nurodytas posakinys.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą įspėjimų atveju.

  
#### Pavyzdys
  
Norėdami ištirti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
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
  
Norėdami patikrinti inspekcijos pažangą su užklausos ID 12345:
  
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
  
Norėdami atšaukti inspekciją su užklausos ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Norėdami atšaukti visas šiuo metu vykstančias arba eilėje esančias užklausas:
  
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
- `--exportfile`, `-ef`: Nurodyti failo pavadinimą eksportui.
    
#### Pavyzdys
  
Norėdami eksportuoti visus duomenų šaltinius iš projekto `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ši komanda eksportuoja visus duomenų šaltinius iš `ProjectA` kaip JSON dokumentą, kurį galima importuoti į kitą projektą arba ***digna*** saugyklą.


### import-ds

Komanda `import-ds` ***digna*** CLI naudojama importuoti duomenų šaltinius į tikslinį projektą ir sukurti importo ataskaitą.

#### Komandos naudojimas
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, į kurį bus importuojami duomenų šaltiniai, pavadinimas.
- **EXPORT_FILE**: Failo vardas, kuriame yra duomenų šaltinių eksportas, kurį reikia importuoti.

#### Parinktys

- `--output-file`, `-o`: Failas importo ataskaitai išsaugoti (jei nenurodytas, ataskaita spausdinama terminale lentelės formatu).
- `--output-format`, `-f`: Formatą, kuriuo išsaugoti importo ataskaitą (json, csv).
    
#### Pavyzdys
  
Norėdami importuoti visus duomenų šaltinius iš eksporto failo `my_export.json` į `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importo ši komanda taip pat parodys ataskaitą apie importuotus ir praleistus objektus. Į `ProjectB` bus importuoti tik nauji duomenų šaltiniai. Norėdami sužinoti, kurie objektai būtų importuoti ir praleisti, galite naudoti komandą `plan-import-ds`.

### plan-import-ds

Komanda `plan-import-ds` ***digna*** CLI naudojama išanalizuoti duomenų šaltinių eksportą prieš faktinį importą ir sukurti importo planą bei ataskaitą.

#### Komandos naudojimas
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, į kurį būtų importuojami duomenų šaltiniai, pavadinimas.
- **EXPORT_FILE**: Failo vardas, kuriame yra duomenų šaltinių eksportas, kurį reikia išanalizuoti prieš importą.

#### Parinktys

- `--output-file`, `-o`: Failas importo ataskaitai išsaugoti (jei nenurodytas, ataskaita spausdinama terminale lentelės formatu).
- `--output-format`, `-f`: Formatą, kuriuo išsaugoti importo ataskaitą (json, csv).
    
#### Pavyzdys
  
Norėdami patikrinti, kurie duomenų šaltiniai būtų importuoti ir kurie būtų praleisti iš eksporto failo `my_export.json` importuojant į `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ši komanda parodys tik importo planą – objektus, kurie būtų importuoti ir praleisti.