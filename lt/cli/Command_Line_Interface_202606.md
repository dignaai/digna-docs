# digna CLI žinynas 2026.06
**2026-09-05**

Šiame puslapyje aprašomas visas komandų rinkinys, prieinamas ***digna*** CLI **2026.06** laidoje, kartu su naudojimo pavyzdžiais ir parinktimis.

Vykdomasis failas vadinasi `digna`.

---

## CLI pagrindai

---

### Apžvalga ir sintaksė

**2026.06** laidos CLI naudoja struktūrizuotą, kategorijomis pagrįstą komandų hierarchiją:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` ir `serve` yra pavienės komandos be subkomandos:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Bendrosios parinktys

Toliau nurodytos bendrosios parinktys taikomos visoms komandoms:

- `--help`, `-h`: Parodo žinyno informaciją apie CLI arba apie konkrečią komandų kategoriją ar subkomandą.
- `--stacktrace`: Įvykus klaidai parodo visą klaidų grandinę, o ne vien aukščiausio lygio pranešimą.

`--stacktrace` yra bendroji parinktis griežtąja prasme: ją reikia nurodyti **prieš** komandų kategoriją, o ne po jos.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Vėliavėlės `--version` nėra. Vietoj jos naudokite komandą [`version`](#version).

### Būtinos sąlygos

Daugumai komandų reikia perskaitomo, galiojančio `config.toml` failo; kai kurioms papildomai reikia galiojančios licencijos.
Toliau pateiktoje lentelėje užfiksuota, ką kiekviena komandų kategorija įkelia prieš imdamasi bet kokio veiksmo:

| Komandų kategorija | Reikia `config.toml` | Reikia galiojančios licencijos |
|---|---|---|
| `version` | ne | ne |
| `config check` | ne (kaip tik apie tai komanda ir praneša) | ne |
| `license check` | ne | tai *ir yra* patikrinimas |
| `crypt` | taip | ne |
| `serve` | taip | ne |
| `project` | taip | ne |
| `user` | taip | taip |
| `inspection` | taip | taip |
| `repo` | taip | taip |

Kai reikia licencijos, tikrinamas ir jos parašas, ir galiojimo pabaigos data, o komanda nutraukiama dar prieš paliečiant saugyklą, jei bent vienas patikrinimas nepavyksta.

### Išėjimo kodai

- `0`: komanda pavyko.
- `1`: komanda nepavyko. Klaidos pranešimas rašomas į stderr su priešdėliu `Error: `.

### help

Parinktis `--help` teikia informaciją apie galimas komandų kategorijas, subkomandas ir parinktis:

1. **Bendrojo žinyno rodymas:**
   ```bash
   digna --help
   ```

2. **Žinyno gavimas apie konkrečias kategorijas ir komandas:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Išvestyje pateikiama:**
   - **Komandos aprašas:** Komandos paskirties santrauka.
   - **Sintaksė:** Privalomi ir neprivalomi argumentai.
   - **Parinktys:** Komandai būdingos vėliavėlės ir parametrai.

### version

Komanda `version` išveda įdiegtą ***digna*** laidą. Ji neskaito jokios konfigūracijos ir netikrina licencijos, todėl veikia ir tokioje diegtyje, kurios `config.toml` ar licencija trūksta arba yra negaliojanti.

Laidos versija nepriklauso nuo saugyklos schemos versijos, apie kurią praneša [`repo check`](#repo-check).

#### Komandos naudojimas
```bash
digna version
```

#### Išvesties pavyzdys
```text
2026.06
```

---

## Konfigūracijos valdymas

---

### config check

Komanda `config check` patikrina konfigūracijos failą (`config.toml`) ir įsitikina, kad visi privalomi skyriai bei nuostatos yra ir tinkamai suformatuoti. Kiekvienas skyrius tikrinamas atskirai, todėl sugadintas skyrius `[app]` neužgožia skyriaus `[repo]` būsenos.

Pateikiami šie skyriai:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — neprivaloma; trūkstamas raktas patikrinimą praeina, o esantis, bet netaisyklingas sąrašas – ne

Komanda sąmoningai neįkelia programos konfigūracijos taip, kaip tai daro kitos komandos, kad galėtų diagnozuoti `config.toml`, dėl kurio ***digna*** apskritai nepasileistų.

#### Komandos naudojimas
```bash
digna config check [OPTIONS]
```

#### Parinktys
- `--configpath`, `-c`: Kelias iki konfigūracijos failo arba iki katalogo, kuriame yra `config.toml` (numatytoji reikšmė `./config.toml`).
- `--json`: Išveda patikrinimo ataskaitą JSON formatu. Turi pirmenybę prieš `--quiet`.
- `--quiet`, `-q`: Slepia ataskaitą ir remiasi vien išėjimo kodu.

#### Pavyzdys
```bash
digna config check
```

Patikrinti konkretų konfigūracijos failą ir išvestį pateikti JSON formatu:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Išvesties pavyzdys
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Trūkstamas failas arba TOML sintaksės klaida nepalieka nieko, ką būtų galima tikrinti skyrius po skyriaus, todėl apie tai pranešama kaip apie vieną klaidą, o ne ataskaitą, nepriklausomai nuo `--quiet` ar `--json`.

---

## Saugyklos valdymas

---

### repo check

Komanda `repo check` patikrina duomenų bazės ryšį bei saugyklos įdiegimą ir versiją. Ji nepavyksta, jei sukonfigūruotos schemos nėra arba jei ji yra, bet joje nėra ***digna*** saugyklos.

Pateikiama versija yra saugyklos schemos versija, kurios numeracija tvarkoma atskirai nuo ***digna*** laidos, kurią išveda [`version`](#version).

#### Komandos naudojimas
```bash
digna repo check
```

#### Išvesties pavyzdys
```text
Repo version 3.0.0 installed
```

### repo install

Komanda `repo install` įdiegia naują ***digna*** saugyklą į `config.toml` faile sukonfigūruotą schemą, sukurdama visas reikiamas sekas, lenteles, indeksus, apribojimus ir pradinius įrašus.

Pačios schemos ši komanda **nesukuria** — ji turi egzistuoti iš anksto. Komanda taip pat atsisako veikti, jei toje schemoje saugykla jau įdiegta, ir nurodo [`repo upgrade`](#repo-upgrade), jei įdiegta versija yra senesnė.

#### Komandos naudojimas
```bash
digna repo install
```

#### Išvesties pavyzdys
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Komanda `repo upgrade` pritaiko duomenų bazės schemos migracijas, kad esama saugykla būtų pakelta iki versijos, kurios tikisi įdiegta laida. Naujinimai taikomi po vieną versijos žingsnį nustatytu naujinimo keliu, o kiekvienas užbaigtas žingsnis įrašomas saugykloje.

Jei saugykla jau yra laukiamos versijos, komanda praneša, kad naujinti nereikia, ir jokių pakeitimų neatlieka.

#### Komandos naudojimas
```bash
digna repo upgrade
```

#### Išvesties pavyzdys
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Šifravimo valdymas

---

### crypt gen-key

Komanda `crypt gen-key` sugeneruoja naują AES-GCM šifravimo raktą, skirtą naudoti kaip šifravimo raktą faile `config.toml`. Įkeliamas `config.toml` jau turi būti, nors sugeneruotas raktas nuo jo ir nepriklauso.

#### Komandos naudojimas
```bash
digna crypt gen-key
```

#### Išvesties pavyzdys
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Komanda `crypt encrypt` užšifruoja eilutę (pavyzdžiui, duomenų bazės slaptažodį) naudodama faile `config.toml` sukonfigūruotą AES-GCM raktą ir išveda šifruotą tekstą.

#### Komandos naudojimas
```bash
digna crypt encrypt <VALUE>
```

#### Argumentai
- **VALUE**: Šifruotina atvirojo teksto eilutė (privaloma).

#### Pavyzdys
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Komanda `crypt decrypt` iššifruoja AES-GCM užšifruotą eilutę naudodama faile `config.toml` sukonfigūruotą raktą ir išveda atvirąjį tekstą.

#### Komandos naudojimas
```bash
digna crypt decrypt <VALUE>
```

#### Argumentai
- **VALUE**: Iššifruotina šifruoto teksto eilutė (privaloma).

#### Pavyzdys
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Naudotojų valdymas

---

### user add

Komanda `user add` sukuria naują naudotojo paskyrą ***digna*** saugykloje. Komanda nepavyksta, jei naudotojas nurodytu el. pašto adresu jau yra.

#### Komandos naudojimas
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentai
- **EMAIL**: Naudotojo el. pašto adresas (privaloma).
- **PASSWORD**: Pradinis naudotojo slaptažodis (privaloma).
- **DISPLAY_NAME**: Visas rodomas naudotojo vardas (privaloma).

#### Parinktys
- `--admin`, `-a`: Sukuria naudotoją su administratoriaus (supernaudotojo) teisėmis.

#### Pavyzdys
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Norint sukurti administratoriaus paskyrą:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Išvesties pavyzdys
```text
User created with ID: 42
```

### user list

Komanda `user list` lentelės pavidalu išvardija visus registruotus naudotojus su ID, el. paštu, rodomu vardu ir administratoriaus žyme.

#### Komandos naudojimas
```bash
digna user list
```

#### Išvesties pavyzdys
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Komanda `user modify` atnaujina esamos naudotojo paskyros, atpažįstamos pagal el. pašto adresą, rodomą vardą ir administratoriaus teises.

Ir rodomas vardas, ir administratoriaus žymė visada įrašomi. `--admin` yra jungiklis, o ne reikšmė: **jos praleidimas atšaukia administratoriaus teises**, todėl nurodykite ją visada, kai naudotojas turi jas išlaikyti arba gauti.

#### Komandos naudojimas
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumentai
- **EMAIL**: Keistino naudotojo el. paštas (privaloma).
- **DISPLAY_NAME**: Atnaujintas rodomas vardas (privaloma).

#### Parinktys
- `--admin`, `-a`: Suteikia administratoriaus teises. Praleiskite, kad jas atšauktumėte.
- `--valid-until`, `-v`: Priimama dėl suderinamumo, tačiau **šiuo metu netaikoma**. Ją nurodžius išvedamas įspėjimas ir niekas nepakeičiama.

#### Pavyzdys
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Išvesties pavyzdys
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Komanda `user modify-pwd` atnaujina esamos naudotojo paskyros slaptažodį.

#### Komandos naudojimas
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumentai
- **EMAIL**: Naudotojo, kurio slaptažodis atnaujinamas, el. paštas (privaloma).
- **PASSWORD**: Naujas slaptažodis (privaloma).

#### Pavyzdys
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Komanda `user delete` pašalina naudotojo paskyrą iš sistemos.

#### Komandos naudojimas
```bash
digna user delete <EMAIL>
```

#### Argumentai
- **EMAIL**: Šalintino naudotojo el. paštas (privaloma).

#### Pavyzdys
```bash
digna user delete jdoe@example.com
```

---

## Projektų ir duomenų šaltinių valdymas

---

### project list

Komanda `project list` išvardija visus saugykloje esančius projektus, parodydama jų ID, pavadinimą ir aprašą.

#### Komandos naudojimas
```bash
digna project list
```

#### Išvesties pavyzdys
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Komanda `project list-ds` išvardija visus su nurodytu projektu susietus duomenų šaltinius, parodydama jų ID, pavadinimą, rūšį, schemą ir lentelės pavadinimą.

#### Komandos naudojimas
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumentai
- **PROJECT_NAME**: Projekto, kurio duomenų šaltinius reikia išvardyti, pavadinimas (privaloma). Pavadinimas turi sutapti tiksliai.

#### Pavyzdys
```bash
digna project list-ds ProjectA
```

#### Išvesties pavyzdys
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Komanda `project export-ds` eksportuoja projekto duomenų šaltinius į JSON dokumentą.

Jei nenurodoma nei `--table-name`, nei `--table-id`, eksportuojami visi projekto duomenų šaltiniai.

#### Komandos naudojimas
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumentai
- **PROJECT_NAME**: Projekto, iš kurio eksportuojami duomenų šaltiniai, pavadinimas (privaloma).

#### Parinktys
- `--table-name`, `-n`: Eksportuotinų duomenų šaltinių pavadinimai. Kelis pavadinimus galima nurodyti atskiriant tarpais.
- `--table-id`, `-i`: Eksportuotinų duomenų šaltinių ID. Kelis ID galima nurodyti atskiriant tarpais.
- `--exportfile`, `-f`: Kelias, kuriuo įrašomi eksportuoti duomenų šaltiniai (numatytoji reikšmė: `data_sources_export.json`).

#### Pavyzdys
Norint eksportuoti visus duomenų šaltinius iš `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Norint eksportuoti konkrečias lenteles:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Išvesties pavyzdys
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Komanda `project import-ds` importuoja duomenų šaltinius iš eksporto failo į paskirties projektą ir kiekvieno objekto atžvilgiu praneša, kas buvo sukurta, atnaujinta ar praleista.

#### Komandos naudojimas
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentai
- **PROJECT_NAME**: Paskirties projekto, į kurį importuojama, pavadinimas (privaloma).
- **EXPORT_FILE**: Kelias iki JSON eksporto failo (privaloma).

#### Parinktys
- `--output-file`, `-o`: Failas, į kurį rašoma importo ataskaita. Be jo ataskaita siunčiama į stdout.
- `--output-format`, `-f`: Importo ataskaitos formatas — `table`, `json` arba `csv` (numatytoji reikšmė: `table`).

#### Pavyzdys
```bash
digna project import-ds ProjectB my_export.json
```

Norint gauti kompiuterio skaitomą ataskaitą:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Ataskaita apima keturis objektų lygmenis — duomenų šaltinį, duomenų rinkinio apibrėžtį, atributą ir tikrinimo taisyklę — kiekvieną su jo importo veiksmu, rezultatu, gauto objekto ID ir papildoma informacija.

### project plan-import-ds

Komanda `project plan-import-ds` parodo duomenų šaltinių importo į paskirties projektą peržiūrą – kurie objektai būtų sukurti, atnaujinti ar praleisti – nieko nekeisdama. Ji priima tą patį eksporto failą ir tas pačias ataskaitos parinktis kaip [`project import-ds`](#project-import-ds) ir prie kiekvieno suplanuoto objekto prideda žingsnio numerį.

#### Komandos naudojimas
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumentai
- **PROJECT_NAME**: Paskirties projekto pavadinimas (privaloma).
- **EXPORT_FILE**: Kelias iki eksporto failo (privaloma).

#### Parinktys
- `--output-file`, `-o`: Failas, į kurį rašomas importo planas. Be jo planas siunčiamas į stdout.
- `--output-format`, `-f`: Importo plano formatas — `table`, `json` arba `csv` (numatytoji reikšmė: `table`).

#### Pavyzdys
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Patikrų valdymas

---

### inspection run

Komanda `inspection run` sukuria patikros užklausą projektui ir datų intervalui, o paskui – priklausomai nuo nurodytų parinkčių – arba jos laukia, arba iškart grąžina valdymą, arba vykdo ją savo pačios procese.

Trys vykdymo režimai yra šie:

- **Numatytasis (be vėliavėlės)**: užklausa įtraukiama į vidinės posistemės eilę, o CLI kas dvi sekundes tikrina jos būseną ir išveda užduočių eigą, kol patikra pasiekia galutinę būseną. Būtinas veikiantis `digna serve`, kitaip užklausos niekas nepaims.
- **`--async-mode`**: užklausa įtraukiama į eilę, o jos ID išvedamas iškart. Sekimui naudokite [`inspection status`](#inspection-status).
- **`--bypass-backend`**: patikrą vykdo pats CLI procesas ir ji į eilę neįtraukiama, todėl veikiančio serverio nereikia.

`--async-mode` ir `--bypass-backend` viena kitą paneigia.

Visais režimais komanda baigiasi ne nuliniu išėjimo kodu, jei patikra nebuvo sėkmingai užbaigta.

#### Komandos naudojimas
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumentai
- **PROJECT_NAME**: Paskirties projekto pavadinimas (privaloma). Pavadinimas turi sutapti tiksliai.
- **START_DATE**: Datų intervalo pradžios data `YYYY-MM-DD` formatu (privaloma).
- **END_DATE**: Datų intervalo pabaigos data `YYYY-MM-DD` formatu (privaloma).

#### Parinktys
- `--table-name`: Apriboja patikrą vienu projekto duomenų šaltiniu, nurodomu pagal duomenų šaltinio pavadinimą. Be jos tikrinami visi projekto duomenų šaltiniai.
- `--async-mode`: Įtraukia patikrą į eilę ir išveda užklausos ID, užuot jos laukusi. Negalima derinti su `--bypass-backend`.
- `--bypass-backend`: Vykdo patikrą tiesiogiai CLI procese, užuot įtraukusi ją į vidinės posistemės eilę. Negalima derinti su `--async-mode`.

#### Pavyzdys
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Norint pateikti asinchroninę patikrą:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Norint patikrinti vieną duomenų šaltinį:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Išvesties pavyzdys
Numatytasis režimas:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asinchroninis režimas:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Komanda `inspection status` pagal užklausos ID pateikia patikros užklausos būseną ir užduočių eigą.

#### Komandos naudojimas
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumentai
- **INSPECTION_REQUEST_ID**: Skaitinis patikros užklausos ID (privaloma).

#### Pavyzdys
```bash
digna inspection status 1024
```

#### Išvesties pavyzdys
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Komanda `inspection abort` prašo atšaukti vykdomas arba laukiančias patikros užklausas. Kiekvienai paveiktai užklausai ji įrašo stabdymo įvykį; pagal jį veikia vidinė posistemė, todėl nutraukimas yra prašymas sustoti, o ne momentinis nužudymas.

#### Komandos naudojimas
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumentai
- **INSPECTION_REQUEST_ID**: Nutrauktinos patikros užklausos ID. Privaloma, nebent nurodyta `--killall`.

#### Parinktys
- `--killall`: Nutraukia visas šiuo metu vykdomas ir laukiančias patikros užklausas. Turi pirmenybę prieš kartu nurodytą užklausos ID.

#### Pavyzdys
Norint nutraukti konkrečią užklausą:
```bash
digna inspection abort 1024
```

Norint nutraukti visas aktyvias ir eilėje esančias patikras:
```bash
digna inspection abort --killall
```

#### Išvesties pavyzdys
`--killall` praneša, ką atliko; vienos užklausos nutraukimas išvesties nepateikia, o apie sėkmę praneša savo išėjimo kodu.
```text
All running and pending inspections have been aborted.
```

---

## Licencijų valdymas

---

### license check

Komanda `license check` patikrina failą `license.toml`: sutikrina jo parašą su kartu su diegtimi pateiktu viešuoju raktu ir įsitikina, kad licencija nepasibaigusi. Ji neskaito jokios programos konfigūracijos, todėl veikia dar prieš sukonfigūruojant `config.toml`.

#### Komandos naudojimas
```bash
digna license check
```

#### Išvesties pavyzdys
```text
License is valid
```

Apie negaliojantį parašą ir pasibaigusią licenciją pranešama kaip apie skirtingas klaidas, abiem atvejais su išėjimo kodu 1.

---

## Serverio ir foninės tarnybos

---

### serve

Komanda `serve` paleidžia ***digna*** REST API serverį kartu su fonine patikrų planuokle ir patikrų tvarkykle. Paleidimo metu ji taip pat pažymi kaip nepavykusias visas patikras, kurias saugykla vis dar laiko vykdomomis, nes iš ankstesnio proceso niekas negalėjo išlikti.

Komanda veikia priekiniame plane, kol nesustabdoma.

#### Komandos naudojimas
```bash
digna serve [OPTIONS]
```

#### Parinktys
- `--address`: Tinklo adresas, prie kurio susiejamas API serveris (numatytoji reikšmė: `127.0.0.1`).
- `--port`: Prievado numeris, kurio klausomasi (numatytoji reikšmė: `8000`).

#### Pavyzdys
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Išvesties pavyzdys
```text
Server running on http://0.0.0.0:8000
```