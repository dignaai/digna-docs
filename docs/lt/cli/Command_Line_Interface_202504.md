---
title: digna CLI referencija 2025.04 – komandos ir pavyzdžiai | digna dokumentacija
description: Išsami digna CLI versijos 2025.04 referencija. Sužinokite, kaip valdyti vartotojus, saugyklas ir duomenis naudojant komandas, tokias kaip add-user, check-repo-connection, upgrade-repo, inspect ir kt.
image: /assets/logo_square.png
---

# digna CLI referencija 2025.04
**2025-04-01**

Šiame puslapyje aprašytas visas komandų rinkinys, prieinamas ***digna*** CLI leidime **2025.04**, įskaitant naudojimo pavyzdžius ir parinktis.

---

## CLI pagrindai

---

## Naudojimasis parinktimi `help`

Parinktis `--help` pateikia informaciją apie prieinamas komandas ir jų naudojimą. Yra du pagrindiniai būdai naudoti šią parinktį:

1. **Bendros pagalbos atvaizdavimas:**
   
    Naudokite --help iškart po komandos raktažodžio dignacli  
   ```bash
   dignacli --help
   ```

2. **Pagalbos gavimas konkrečioms komandoms:**  
  
    Norėdami gauti detalesnės informacijos apie konkrečią komandą, pridėkite `--help` prie tos komandos.
    Pavyzdžiui, norėdami gauti pagalbą su komanda `add-user`, vykdykite:
     ```bash
     dignacli add-user --help
     ```

     ### išvestis:
      
     - **Komandos aprašymas:** Išsamiai paaiškinama, ką komanda atlieka.  
     - **Sintaksė:** Rodo tikslią sintaksę, įskaitant privalomus ir pasirenkamus argumentus.  
     - **Parinktys:** Išvardijamos komandos specifiškos parinktys su paaiškinimais.  
     - **Pavyzdžiai:** Pateikiami pavyzdžiai, kaip efektyviai vykdyti komandą.

  
## Naudojimasis komanda `check-repo-connection`

Komanda check-repo-connection yra įrankis ***digna*** CLI, skirtas patikrinti ryšį ir prieigą prie nurodytos ***digna*** saugyklos. Ši komanda užtikrina, kad CLI gali bendrauti su saugykla.
      
#### Komandos naudojimas
```bash
dignacli check-repo-connection
```

Sėkmingai įvykdžius, komanda pateiks ryšio patvirtinimą ir saugyklos informaciją: saugyklos versiją, Host, Database ir Schema.  
  
Jei ryšys su saugykla nepavyksta, patikrinkite config.toml failą dėl teisingų konfigūracijos nustatymų.

## Naudojimasis komanda ‘version’

Norėdami patikrinti įdiegtą *dignacli* versiją, naudokite parinktį --version.  
  
#### Komandos naudojimas
```bash
dignacli --version
```
  
#### Pavyzdinė išvestis
```bash
dignacli version 2025.04
```

## Naudojimasis registravimo (logging) parinktimis
  
Pagal nutylėjimą konsolės išvestis iš ***digna*** komandų yra minimalistiška. Dauguma komandų leidžia pateikti papildomą informaciją naudojant šias parinktis:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ir „debug“ nurodo detalumo lygį, o perjungiklis „logfile“ leidžia nukreipti išvestį į failą vietoje konsolės lango.

## Vartotojų valdymas

### Naudojimasis komanda ‘add-user’
  
Komanda add-user ***digna*** CLI naudojama pridėti naują vartotoją į ***digna*** sistemą.
  
#### Komandos naudojimas
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumentai

- **USER_NAME**: Naujo vartotojo vardas (privalomas).
- **USER_FULL_NAME**: Naujo vartotojo pilnas vardas (privalomas).
- **USER_PASSWORD**: Naujo vartotojo slaptažodis (privalomas).

#### Parinktys

- `--is_superuser`, `-su`: Žymė, skirianti naują vartotoją kaip administratorių.
- `--valid_until`, `-vu`: Nustato vartotojo paskyros galiojimo pabaigos datą formatu `YYYY-MM-DD HH:MI:SS`. Jei nenustatyta, paskyra galioja neribotai.

#### Pavyzdys

Norint pridėti naują vartotoją su vartotojo vardu `jdoe`, pilnu vardu `John Doe` ir slaptažodžiu `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Norėdami pridėti naują vartotoją ir nustatyti paskyros galiojimo datą:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Naudojimasis komanda `delete-user`
  
Komanda `delete-user` ***digna*** CLI naudojama pašalinti esamą vartotoją iš ***digna*** sistemos.
  
#### Komandos naudojimas
```bash
dignacli delete-user USER_NAME
```
  
##### Argumentai
- **USER_NAME**: Vartotojo vardas, kurį reikia pašalinti (privalomas). Tai yra vienintelis komandos reikalaujamas argumentas.

#### Pavyzdys
```bash
dignacli delete-user jdoe
```
  
Vykdant šią komandą, vartotojas `jdoe` bus pašalintas iš ***digna*** sistemos, jam bus atšaukta prieiga ir iš saugyklos bus ištrinti susiję duomenys bei teisės.

### Naudojimasis komanda `modify-user`

Komanda `modify-user` ***digna*** CLI naudojama atnaujinti esamo vartotojo duomenis ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumentai
  
- **USER_NAME**: Vartotojo vardas, kurį reikia pakeisti (privalomas).
- **USER_FULL_NAME**: Naujas vartotojo pilnas vardas (privalomas).
  
#### Parinktys  
  
- `--is_superuser`, `-su`: Nustato vartotoją kaip superuser'į, suteikiant aukštesnes privilegijas. Šis žymeklis nereikalauja reikšmės.  
- `--valid_until`, `-vu`: Nustato vartotojo paskyros galiojimo pabaigos datą formatu YYYY-MM-DD HH:MI:SS. Jei nepateikta, paskyra galioja neribotai.  
  
#### Pavyzdys
  
Norėdami pakeisti vartotojo `jdoe` pilną vardą į „Johnathan Doe“ ir nustatyti vartotoją kaip superuser'į:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Naudojimasis komanda `modify-user-pwd`
  
Komanda `modify-user-pwd` ***digna*** CLI naudojama keisti slaptažodį esamam vartotojui ***digna*** sistemoje.
  
#### Komandos naudojimas
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumentai
  
- **USER_NAME**: Vartotojo vardas, kurio slaptažodis keičiamas (privalomas).
- **USER_PWD**: Naujas vartotojo slaptažodis (privalomas).
  
#### Pavyzdys
  
Norint pakeisti vartotojo `jdoe` slaptažodį į `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Naudojimasis komanda `list-users`

Komanda `list-users` ***digna*** CLI atvaizduoja visų vartotojų, užregistruotų ***digna*** sistemoje, sąrašą.

#### Komandos naudojimas

```bash
dignacli list-users
```

Vykdant šią komandą ***digna*** CLI prisijungs prie ***digna*** saugyklos ir parodys visus vartotojus, nurodydama jų ID, vartotojo vardą, pilną vardą, superuser statusą ir galiojimo laiko žymes.

## Saugyklos (Repository) valdymas

### Naudojimasis komanda `upgrade-repo`
  
Komanda `upgrade-repo` ***digna*** CLI naudojama atnaujinti arba inicijuoti ***digna*** saugyklą. Ši komanda yra būtina taikant atnaujinimus arba nustatant saugyklos infrastruktūrą pirmą kartą.
  
#### Komandos naudojimas

```bash
dignacli upgrade-repo [options]
```
  
#### Parinktys
  
- `--simulation-mode`, `-s`: Įjungus, komanda veikia simuliacijos režimu — išspausdina SQL užklausas, kurios būtų vykdomos, bet jų faktiškai neįvykdo. Tai naudinga peržiūrint pakeitimus be realių modifikacijų saugykloje.  

  
#### Pavyzdys
  
Norėdami atnaujinti ***digna*** saugyklą, galite vykdyti komandą be parinkčių:
  
```bash
dignacli upgrade-repo
```  
Norėdami paleisti atnaujinimą simuliacijos režimu (pamatyti SQL užklausas, jų neįvedant):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ši komanda yra svarbi palaikant ***digna*** sistemą, užtikrinant, kad duomenų bazės schema ir kiti saugyklos komponentai atitiktų naujausią programinės įrangos versiją.

### Naudojimasis komanda `encrypt`
  
Komanda `encrypt` ***digna*** CLI naudojama užšifruoti slaptažodį.
  
#### Komandos naudojimas
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumentai
- **PASSWORD**: Slaptažodis, kurį reikia užšifruoti (privalomas).
  
#### Pavyzdys
  
Norint užšifruoti slaptažodį, reikia pateikti slaptažodį kaip argumentą.   
Pavyzdžiui, užšifruoti slaptažodį `mypassword123`, naudokite:
```bash
dignacli encrypt mypassword123
```
Ši komanda išves užšifruotą pateikto slaptažodžio versiją, kurią vėliau galima naudoti saugiose vietose. Jei slaptažodžio argumentas nepateiktas, CLI nurodys klaidą dėl trūkstamo argumento.

## Naudojimasis komanda `generate-key`
  
Komanda `generate-key` naudojama sugeneruoti Fernet raktą, kuris būtinas slaptažodžiams saugoti ***digna*** saugykloje.
  
#### Komandos naudojimas
```bash
dignacli generate-key
```
  
## Duomenų valdymas

## Naudojimasis komanda `clean-up`

Komanda `clean-up` ***digna*** CLI naudojama pašalinti profilius, prognozes ir Traffic Light System duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda yra svarbi duomenų gyvenimo ciklo valdymui, padedanti palaikyti tvarkingą ir efektyvią duomenų aplinką, ištrinant pasenusius arba nereikalingus duomenis.

#### Komandos naudojimas

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, iš kurio turi būti pašalinti duomenys (privalomas). Naudojant raktinį žodį all-projects šio argumento reikšmė nurodo ***digna*** iteruoti per visus esamus projektus ir taikyti komandą kiekvienam jų.
- **FROM_DATE**: Duomenų šalinimo pradinė data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų šalinimo pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys
  
- `--table-name`, `-tn`: Apriboja clean-up operaciją konkrečiai lentelei projekte.
- `--table-filter`, `-tf`: Filtruoja, apribojant clean-up tik lentelėms, kurių pavadinimuose yra nurodyta potekstė.
- `--timing`, `-tm`: Po užbaigimo parodo clean-up proceso trukmę.
- `--help`: Pateikia pagalbos informaciją apie clean-up komandą ir išeina.
  
#### Pavyzdys
  
Norėdami pašalinti duomenis iš projekto ProjectA laikotarpiu nuo 2023-01-01 iki 2023-06-30:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Norėdami pašalinti duomenis tik iš konkrečios lentelės `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ši komanda padeda valdyti duomenų saugojimą ir užtikrina, kad saugykloje liktų tik aktuali informacija.

## Naudojimasis komanda `list-projects`
  
Komanda `list-projects` ***digna*** CLI naudojama parodyti visų turimų projektų sąrašą ***digna*** sistemoje.
  
#### Komandos naudojimas
  
```bash
dignacli list-projects
```

Ši komanda ypač naudinga administratoriams ir vartotojams, valdantiems kelis projektus — ji suteikia greitą apžvalgą apie prieinamus projektus ***digna*** saugykloje.

## Naudojimasis komanda `list-ds`

Komanda `list-ds` ***digna*** CLI naudojama parodyti visų prieinamų duomenų šaltinių sąrašą nurodytame projekte. Ši komanda padeda suprasti, kokie duomenų ištekliai yra prieinami analizėms ir valdymui ***digna*** sistemoje.

#### Komandos naudojimas
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumentai
- **PROJECT_NAME**: Projekto pavadinimas, kuriam bus išvardyti duomenų šaltiniai (privalomas).
  
#### Pavyzdys
  
Norėdami išvardinti visus duomenų šaltinius projekte `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ši komanda suteikia vartotojams apžvalgą apie projekte prieinamus duomenų šaltinius, padedant geriau naršyti ir valdyti duomenų sritį.


## Naudojimasis komanda `inspect`

Komanda `inspect` ***digna*** CLI naudojama kurti profilius, prognozes ir Traffic Light System duomenis vienam arba keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis per nurodytą laikotarpį.

#### Komandos naudojimas

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kurio duomenys bus tikrinami (privalomas). Naudojant raktinį žodį all-projects šis argumentas nurodo ***digna*** iteruoti per visus esamus projektus ir taikyti komandą kiekvienam jų.
- **FROM_DATE**: Duomenų tikrinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų tikrinimo pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja inspekciją konkrečiai lentelei projekte.
- `--table-filter`, `-tf`: Filtruoja, inspektuojant tik lenteles, kurių pavadinimuose yra nurodyta potekstė.
- `--do-profile`: Inicijuoja profilių perkalkuliavimą. Numatytoji reikšmė yra do-profile.
- `--no-do-profile`: Neleidžia profilių perkalkuliavimo.
- `--do-prediction`: Inicijuoja prognozių perskaičiavimą. Numatytoji reikšmė yra do-prediction.
- `--no-do-prediction`: Neleidžia prognozių perskaičiavimo.
- `--do-alert-status`: Inicijuoja perspėjimų būsenų perskaičiavimą. Numatytoji reikšmė yra do-alert-status.
- `--no-do-alert-status`: Neleidžia perspėjimų būsenų perskaičiavimo.
- `--iterative`: Vykdo inspekciją periodiškai, kasdienėmis iteracijomis. Numatytoji reikšmė yra iterative.
- `--no-iterative`: Vykdo inspekciją per visą laikotarpį vienu metu.
- `--enable_notification`, `-en`: Įjungia pranešimų siuntimą pastebėjus perspėjimus.
- `--timing`, `-tm`: Po užbaigimo parodo inspekcijos proceso trukmę.
  
#### Pavyzdys
  
Norėdami inspektuoti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Norėdami inspektuoti tik konkrečią lentelę ir priversti prognozių perskaičiavimą:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ši komanda naudinga generuoti atnaujintus profilius ir prognozes, stebėti duomenų vientisumą ir valdyti perspėjimų sistemas nurodytu projekto laikotarpiu.

## Naudojimasis komanda `tls-status`

Komanda `tls-status` ***digna*** CLI naudojama užklausti Traffic Light System (TLS) būsenos konkrečiai lentelei projekte tam tikrai datai. Traffic Light System pateikia informaciją apie duomenų būklę ir kokybę, nurodant galimas problemas arba perspėjimus, kuriems reikia dėmesio.
  
#### Komandos naudojimas
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kuriam vykdoma TLS būsenos užklausa (privalomas).
- **TABLE_NAME**: Konkretus lentelės pavadinimas projekte, kuriai reikalinga TLS būklė (privalomas).
- **DATE**: Data, kuriai tikrinama TLS būsena, paprastai formatu %Y-%m-%d (privalomas).
  
#### Pavyzdys
  
Norėdami patikrinti TLS būseną lentelei UserData projekte ProjectA 2024-07-01 dienai:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ši komanda padeda vartotojams stebėti ir palaikyti duomenų kokybę, pateikiant aiškią ir veiksmingą būsenos ataskaitą pagal iš anksto nustatytus kriterijus.

## Naudojimasis komanda `inspect-async`

Komanda `inspect-async` ***digna*** CLI naudojama nurodyti backendui asinchroniškai atlikti inspekciją vienam arba keliems duomenų šaltiniams nurodytame projekte. Jei project_name nustatytas kaip all-projects, inspekcija iteruos per visus galimus projektus ir atliks inspekciją. Komanda grąžina užklausos ID, kuriuo galima sekti inspekcijos eigą.

#### Komandos naudojimas

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumentai
  
- **PROJECT_NAME**: Projekto pavadinimas, kurio duomenys bus tikrinami (privalomas). Naudojant raktinį žodį all-projects šis argumentas nurodo ***digna*** iteruoti per visus esamus projektus ir taikyti komandą kiekvienam jų.
- **FROM_DATE**: Duomenų tikrinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų tikrinimo pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
#### Parinktys

- `--table-name`, `-tn`: Apriboja inspekciją konkrečiai lentelei projekte.
- `--table-filter`, `-tf`: Filtruoja, inspektuojant tik lenteles, kurių pavadinimuose yra nurodyta potekstė.

  
#### Pavyzdys
  
Norėdami asinchroniškai inspektuoti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Naudojimasis komanda `inspect-status`

Komanda `inspect-status` ***digna*** CLI naudojama patikrinti asinchroninės inspekcijos pažangą pagal užklausos ID.

#### Komandos naudojimas

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumentai
  
- **REQUEST_ID**: Užklausos id, kurį grąžino komanda `inspect-async`. 
  
#### Parinktys

- `--report_level`, `-rl`: Nustato ataskaitos lygį: 'task' arba 'step' [numatytoji: task]
  
#### Pavyzdys
  
Norėdami patikrinti inspekcijos pažangą su užklausos ID 12345 detaliu žingsnių lygiu:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Naudojimasis komanda `export-ds`

Komanda `export-ds` ***digna*** CLI naudojama sukurti duomenų šaltinių eksporto paketą iš ***digna*** saugyklos. Pagal nutylėjimą eksporto metu bus išeksportuoti visi duomenų šaltiniai iš nurodyto projekto.

#### Komandos naudojimas
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto pavadinimas, iš kurio bus eksporto metu paimti duomenų šaltiniai.

#### Parinktys

- `--table_name`, `-tn`: Išeksportuoti konkretų duomenų šaltinį iš projekto.
- `--exportfile`, `-ef`: Nurodyti eksporto failo pavadinimą.
    
#### Pavyzdys
  
Norėdami išeksportuoti visus duomenų šaltinius iš projekto `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Ši komanda eksportuos visus `ProjectA` duomenų šaltinius kaip JSON dokumentą, kurį galima importuoti į kitą projektą arba ***digna*** saugyklą.


## Naudojimasis komanda `import-ds`

Komanda `import-ds` ***digna*** CLI naudojama importuoti duomenų šaltinius į tikslinį projektą bei sugeneruoti importo ataskaitą.

#### Komandos naudojimas
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto pavadinimas, į kurį bus importuojami duomenų šaltiniai.
- **EXPORT_FILE**: Eksporto failo, kurį reikia importuoti, pavadinimas.

#### Parinktys

- `--output-file`, `-o`: Failas, kuriame išsaugoti importo ataskaitą (jei nenurodyta, ataskaita spausdinama terminale lentelės forma).
- `--output-format`, `-f`: Formatas importo ataskaitai išsaugoti (json, csv).
    
#### Pavyzdys
  
Norėdami importuoti visus duomenų šaltinius iš eksporto failo `my_export.json` į `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po importo ši komanda taip pat parodys ataskaitą apie importuotus ir praleistus objektus. Į `ProjectB` bus importuoti tik nauji duomenų šaltiniai. Norėdami sužinoti, kurie objektai būtų importuoti ir kurie praleisti, galite naudoti komandą `plan-import-ds`.

## Naudojimasis komanda `plan-import-ds`

Komanda `plan-import-ds` ***digna*** CLI naudojama suplanuoti duomenų šaltinių importą į tikslinį projektą ir sukurti importo ataskaitą (be faktiško importo — tik planas).

#### Komandos naudojimas
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumentai
- **PROJECT_NAME**: Projekto pavadinimas, į kurį duomenų šaltiniai būtų importuojami.
- **EXPORT_FILE**: Eksporto failo, kurį reikia išanalizuoti prieš importą, pavadinimas.

#### Parinktys

- `--output-file`, `-o`: Failas, kuriame išsaugoti importo ataskaitą (jei nenurodyta, ataskaita spausdinama terminale lentelės forma).
- `--output-format`, `-f`: Formatas importo ataskaitai išsaugoti (json, csv).
    
#### Pavyzdys
  
Norėdami patikrinti, kurie duomenų šaltiniai būtų importuoti ir kurie praleisti iš eksporto failo `my_export.json` importuojant į `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Ši komanda parodys tik objektų importo planą — kurie bus importuoti ir kurie praleisti.