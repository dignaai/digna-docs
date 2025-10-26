---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Išsamus digna CLI leidimo 2024.11 komandinės eilutės nuorodų rinkinys. Sužinokite, kaip valdyti naudotojus, saugyklas ir duomenis naudojant komandas add-user, check-repo-connection, upgrade-repo, inspect, tls-status ir kt.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Šiame puslapyje dokumentuojamas pilnas komandų rinkinys, prieinamas ***digna*** CLI leidime **2024.11**, įskaitant naudojimo pavyzdžius ir parinktis.


---
## CLI pagrindai

---

## `help` parinkties naudojimas

Parinktis `--help` pateikia informaciją apie prieinamas komandas ir jų naudojimą. Yra du pagrindiniai būdai naudoti šią parinktį:

1. **Bendrosios pagalbos rodymas:**
   
    Naudokite `--help` iškart po raktažodžio `dignacli`  
   ```bash
   dignacli --help
   ```

3.  **Pagalba konkrečioms komandoms:**  
  
    Norėdami gauti išsamią informaciją apie konkrečią komandą, pridėkite `--help` prie tos komandos.
    Pavyzdžiui, norėdami gauti pagalbą komandai `add-user`, vykdykite:
     ```bash
     dignacli add-user --help
     ```

     ### išvestis:
      
     - **Komandos aprašymas:** Išsamiai paaiškina, ką komanda atlieka.  
     - **Sintaksė:** Rodo tikslią sintaksę, įskaitant būtinus ir pasirenkamus argumentus.  
     - **Parinktys:** Išvardija komandos specifines parinktis su paaiškinimais.  
     - **Pavyzdžiai:** Pateikia pavyzdžių, kaip efektyviai vykdyti komandą.

  
## `check-repo-connection` komandos naudojimas

Komanda `check-repo-connection` yra įrankis ***digna*** CLI skirtas tikrinti ryšį ir prieigą prie nurodytos ***digna*** saugyklos. Ši komanda užtikrina, kad CLI gali bendrauti su saugykla.
      
### Komandos naudojimas
```bash
dignacli check-repo-connection
```

Sėkmingai įvykdžius, komanda pateiks patvirtinimą apie ryšį kartu su informacija apie saugyklą: Repository version, Host, Database ir Schema.  
  
Jei ryšys su saugykla nepavyksta, patikrinkite config.toml failą, ar nustatymai yra teisingi.

## `version` komandos naudojimas

Norėdami patikrinti įdiegtą *dignacli* versiją, naudokite parinktį `--version`.  
  
### Komandos naudojimas
```bash
dignacli --version
```
  
### Pavyzdinė išvestis
```bash
dignacli version 2024.11
```

## Žurnalavimo parinkčių naudojimas
  
Pagal numatytuosius nustatymus konsolės išvestis iš ***digna*** komandų yra minimalistinė. Dauguma komandų leidžia pateikti papildomą informaciją naudojant šias parinktis:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose“ ir „debug“ nurodo informacijos detalumo lygį, o „logfile“ perjungiklis leidžia nukreipti išvestį į failą vietoje konsolės lango.

# Naudotojų valdymas

## `add-user` komandos naudojimas
  
Komanda `add-user` ***digna*** CLI naudojama pridėti naują naudotoją į ***digna*** sistemą.
  
### Komandos naudojimas
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumentai

- **USER_NAME**: Naujo naudotojo vartotojo vardas (privalomas).
- **USER_FULL_NAME**: Naujo naudotojo pilnas vardas (privalomas).
- **USER_PASSWORD**: Naujo naudotojo slaptažodis (privalomas).

### Parinktys

- `--is_superuser`, `-su`: Žymė, skirianti naują naudotoją kaip administratorių.
- `--valid_until`, `-vu`: Nustato naudotojo paskyros galiojimo pabaigos datą formatu `YYYY-MM-DD HH:MI:SS`. Jei nenustatyta, paskyra neturi galiojimo pabaigos.

### Pavyzdys

Pridėti naują naudotoją su vartotojo vardu `jdoe`, pilnu vardu `John Doe` ir slaptažodžiu `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pridėti naują naudotoją ir nustatyti paskyros galiojimo datą:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` komandos naudojimas
  
Komanda `delete-user` ***digna*** CLI naudojama pašalinti esamą naudotoją iš ***digna*** sistemos.
  
### Komandos naudojimas
```bash
dignacli delete-user USER_NAME
```
  
### Argumentai
- **USER_NAME**: Naudotojo vardas, kurį reikia pašalinti (privalomas). Tai yra vienintelis reikalaujamas argumentas komandai.

### Pavyzdys
```bash
dignacli delete-user jdoe
```
  
Vykdant šią komandą, naudotojas `jdoe` bus pašalintas iš ***digna*** sistemos, jam bus atimta prieiga ir ištrinti susiję duomenys bei leidimai saugykloje.

## `modify-user` komandos naudojimas

Komanda `modify-user` ***digna*** CLI naudojama atnaujinti esamo naudotojo duomenis ***digna*** sistemoje.

### Komandos naudojimas
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumentai
  
- **USER_NAME**: Keičiamo naudotojo vartotojo vardas (privalomas).
- **USER_FULL_NAME**: Naujas pilnas naudotojo vardas (privalomas).
  
### Parinktys  
  
- `--is_superuser`, `-su`: Nustato naudotoją kaip superuserį, suteikiant didesnes teises. Ši žymė nereikalauja vertės.  
- `--valid_until`, `-vu`: Nustato paskyros galiojimo datą formatu YYYY-MM-DD HH:MI:SS. Jei nenurodoma, paskyra galios neribotai.  
  
### Pavyzdys
  
Norint pakeisti naudotojo `jdoe` pilną vardą į „Johnathan Doe“ ir nustatyti jį kaip superuserį:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` komandos naudojimas
  
Komanda `modify-user-pwd` ***digna*** CLI naudojama pakeisti esamo naudotojo slaptažodį ***digna*** sistemoje.
  
### Komandos naudojimas
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumentai
  
- **USER_NAME**: Naudotojo vardas, kurio slaptažodis keičiamas (privalomas).
- **USER_PWD**: Naujas naudotojo slaptažodis (privalomas).
  
### Pavyzdys
  
Norint pakeisti naudotojo `jdoe` slaptažodį į `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` komandos naudojimas

Komanda `list-users` ***digna*** CLI pateikia visų ***digna*** sistemoje užregistruotų naudotojų sąrašą.

### Komandos naudojimas

```bash
dignacli list-users
```

Vykdant šią komandą, ***digna*** CLI prisijungs prie ***digna*** saugyklos ir išves visų naudotojų sąrašą, rodydama jų ID, vartotojo vardą, pilną vardą, superuser būseną ir galiojimo laiko žymes.

# Saugyklos valdymas

### `upgrade-repo` komandos naudojimas
  
Komanda `upgrade-repo` ***digna*** CLI naudojama atnaujinti arba inicijuoti ***digna*** saugyklą. Ši komanda būtina taikant atnaujinimus arba nustatant saugyklos infrastruktūrą pirmą kartą.
  
### Komandos naudojimas

```bash
dignacli upgrade-repo [options]
```
  
### Parinktys
  
- `--simulation-mode`, `-s`: Įjungus, komanda veikia simuliacijos režimu — atspausdina SQL užklausas, kurios būtų vykdomos, bet jų iš tikrųjų neatlieka. Tai naudinga peržiūrėti pakeitimus nekeičiant saugyklos.  

  
### Pavyzdys
  
Norėdami atnaujinti ***digna*** saugyklą, galite paleisti komandą be parinkčių:
  
```bash
dignacli upgrade-repo
```  
Norėdami paleisti atnaujinimą simuliacijos režimu (pamatyti SQL užklausas, nebeišsukant pakeitimų):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Ši komanda yra svarbi palaikant ***digna*** sistemą, užtikrinant, kad duomenų bazės schema ir kiti saugyklos komponentai atitiktų naujausią programinės įrangos versiją.

## `encrypt` komandos naudojimas
  
Komanda `encrypt` ***digna*** CLI naudojama užšifruoti slaptažodį.
  
### Komandos naudojimas
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumentai
- **PASSWORD**: Slaptažodis, kurį reikia užšifruoti (privalomas).
  
### Pavyzdys
  
Norėdami užšifruoti slaptažodį, turite jį pateikti kaip argumentą.   
Pavyzdžiui, užšifruoti slaptažodį `mypassword123`:
```bash
dignacli encrypt mypassword123
```
Ši komanda išves pateikto slaptažodžio užšifruotą versiją, kurią galima naudoti saugiai. Jei slaptažodžio argumentas nepateiktas, CLI parodys klaidą apie trūkstamą argumentą.

## `generate-key` komandos naudojimas
  
Komanda `generate-key` naudojama sugeneruoti Fernet raktą, kuris reikalingas slaptažodžių saugumui saugomiems ***digna*** repo duomenims.
  
### Komandos naudojimas
```bash
dignacli generate-key
```
  
# Duomenų valdymas

## `clean-up` komandos naudojimas

Komanda `clean-up` ***digna*** CLI naudojama pašalinti profilius, prognozes ir Traffic Light System duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda svarbi duomenų gyvavimo ciklo valdymui, padedant išlaikyti tvarkingą ir efektyvią duomenų aplinką, ištrinant pasenusius arba nereikalingus duomenis.

### Komandos naudojimas

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentai
  
- **PROJECT_NAME**: Projekto, iš kurio bus ištrinami duomenys, pavadinimas (privalomas). Naudojant raktinį žodį `all-projects`, ***digna*** iteruos per visus esamus projektus ir pritaikys komandą.
- **FROM_DATE**: Duomenų šalinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų šalinimo pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
### Parinktys
  
- `--table-name`, `-tn`: Apriboja valymą iki konkrečios projekto lentelės.
- `--table-filter`, `-tf`: Filtras, ribojantis valymą iki lentelių, kurių pavadinimuose yra nurodytas potekstis.
- `--timing`, `-tm`: Po užbaigimo rodo valymo proceso trukmę.
- `--help`: Parodo pagalbą apie `clean-up` komandą ir išeina.
  
### Pavyzdys
  
Pašalinti duomenis iš projekto ProjectA nuo 2023-01-01 iki 2023-06-30:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pašalinti duomenis tik iš konkrečios lentelės pavadinimu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Ši komanda padeda valdyti duomenų saugojimą ir užtikrinti, kad saugykloje liktų tik aktuali informacija.

## `inspect` komandos naudojimas

Komanda `inspect` ***digna*** CLI naudojama kurti profilius, prognozes ir Traffic Light System duomenis vienam ar keliems duomenų šaltiniams nurodytame projekte. Ši komanda padeda analizuoti ir stebėti duomenis per nurodytą periodą.

### Komandos naudojimas

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumentai
  
- **PROJECT_NAME**: Projekto, kurio duomenys bus tikrinami, pavadinimas (privalomas). Naudojant raktinį žodį `all-projects`, ***digna*** iteruos per visus esamus projektus ir pritaikys komandą.
- **FROM_DATE**: Duomenų tikrinimo pradžios data ir laikas. Priimtini formatai: %Y-%m-%d, %Y-%m-%dT%H:%M:%S arba %Y-%m-%d %H:%M:%S (privalomas).
- **TO_DATE**: Duomenų tikrinimo pabaigos data ir laikas, taikant tuos pačius formatus kaip FROM_DATE (privalomas).
  
### Parinktys

- `--table-name`, `-tn`: Apriboja tikrinimą iki konkrečios projekto lentelės.
- `--table-filter`, `-tf`: Filtras tikrinti tik tas lenteles, kurių pavadinimuose yra nurodytas potekstis.
- `--do-profile`: Priverčia iš naujo surinkti profilius. Pagal numatytuosius nustatymus įjungta (do-profile).
- `--no-do-profile`: Neleidžia iš naujo surinkti profilių.
- `--do-prediction`: Priverčia perskaičiuoti prognozes. Pagal numatytuosius nustatymus įjungta (do-prediction).
- `--no-do-prediction`: Neleidžia perskaičiuoti prognozių.
- `--do-alert-status`: Priverčia perskaičiuoti įspėjimų (alert) būsenas. Pagal numatytuosius nustatymus įjungta (do-alert-status).
- `--no-do-alert-status`: Neleidžia perskaičiuoti įspėjimų būsenų.
- `--timing`, `-tm`: Po užbaigimo rodo tikrinimo proceso trukmę.
  
### Pavyzdys
  
Patikrinti duomenis projekte `ProjectA` nuo 2024-01-01 iki 2024-01-31:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Patikrinti tik konkrečią lentelę ir priversti perskaičiuoti prognozes:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Ši komanda naudinga generuoti atnaujintus profilius ir prognozes, stebėti duomenų vientisumą ir valdyti įspėjimų sistemas nurodytu projekto laikotarpiu.

## `tls-status` komandos naudojimas

Komanda `tls-status` ***digna*** CLI naudojama užklausai apie Traffic Light System (TLS) būseną konkrečioje projekto lentelėje tam tikrai datai. Traffic Light System suteikia įžvalgas apie duomenų sveikatą ir kokybę, nurodydama galimas problemas ar įspėjimus, reikalaujančius dėmesio.
  
### Komandos naudojimas
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumentai
  
- **PROJECT_NAME**: Projekto, kurio TLS būseną tikriname, pavadinimas (privalomas).
- **TABLE_NAME**: Konkreti lentelė projekte, kurios TLS būsena reikalinga (privalomas).
- **DATE**: Data, kuriai tikrinama TLS būsena, dažniausiai formatu %Y-%m-%d (privalomas).
  
### Pavyzdys
  
Patikrinti TLS būseną lentelėje UserData projekte ProjectA 2024-07-01:
```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Ši komanda padeda vartotojams stebėti ir palaikyti duomenų kokybę, pateikdama aiškią ir veiksmingą būsenos ataskaitą pagal iš anksto apibrėžtus kriterijus.

## `list-projects` komandos naudojimas
  
Komanda `list-projects` ***digna*** CLI naudojama parodyti visų prieinamų projektų sąrašą ***digna*** sistemoje.
  
### Komandos naudojimas
  
```bash
dignacli list-projects
```

Ši komanda ypač naudinga administratorių ir vartotojų, valdančių kelis projektus, suteikiant greitą peržiūrą apie projektus saugykloje.

## `list-ds` komandos naudojimas

Komanda `list-ds` ***digna*** CLI naudojama parodyti visų prieinamų duomenų šaltinių sąrašą nurodytame projekte. Ši komanda naudinga suprasti, kokie duomenų ištekliai yra prieinami analizėms ir valdymui ***digna*** sistemoje.

### Komandos naudojimas
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumentai
- **PROJECT_NAME**: Projekto, kuriam listuojami duomenų šaltiniai, pavadinimas (privalomas).
  
### Pavyzdys
  
Išvardyti visus duomenų šaltinius projekte `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Ši komanda suteikia vartotojams apžvalgą apie projekto duomenų šaltinius, padedant efektyviau naršyti ir valdyti duomenų kraštovaizdį.