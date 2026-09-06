---
title: Referenca CLI digna 2026.06 – Ukazi in primeri | Dokumentacija digna
description: Popolna referenca za izdajo digna CLI 2026.06
image: /assets/logo_square.png
---

# Referenca CLI digna 2026.06
**2026-09-05**

Ta stran dokumentira celoten nabor ukazov, ki so na voljo v izdaji **2026.06** vmesnika CLI ***digna***, vključno s primeri uporabe in možnostmi.

Izvršljiva datoteka se imenuje `digna`.

---

## Osnove CLI

---

### Pregled in sintaksa

CLI izdaje **2026.06** uporablja strukturirano hierarhijo ukazov, urejeno po kategorijah:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` in `serve` sta samostojna ukaza brez podukaza:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globalne možnosti

Naslednje globalne možnosti veljajo za vse ukaze:

- `--help`, `-h`: Prikaže pomoč za CLI ali za določeno kategorijo ukazov oziroma podukaz.
- `--stacktrace`: Ob napaki prikaže celotno verigo napak namesto zgolj sporočila najvišje ravni.

`--stacktrace` je globalna možnost v strogem pomenu besede: navesti jo je treba **pred** kategorijo ukaza, ne za njo.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Zastavice `--version` ni. Namesto nje uporabite ukaz [`version`](#version).

### Predpogoji

Večina ukazov potrebuje berljivo in veljavno datoteko `config.toml`; nekateri poleg tega zahtevajo veljavno licenco.
Naslednja tabela beleži, kaj vsaka kategorija ukazov naloži, preden sploh kaj stori:

| Kategorija ukazov | Potrebuje `config.toml` | Potrebuje veljavno licenco |
|---|---|---|
| `version` | ne | ne |
| `config check` | ne (prav o tem ukaz poroča) | ne |
| `license check` | ne | to *je* preverjanje |
| `crypt` | da | ne |
| `serve` | da | ne |
| `project` | da | ne |
| `user` | da | da |
| `inspection` | da | da |
| `repo` | da | da |

Kjer je licenca zahtevana, se preverita tako njen podpis kot datum poteka, in če katero koli od tega ne uspe, se ukaz prekine, še preden se dotakne repozitorija.

### Izhodne kode

- `0`: ukaz je uspel.
- `1`: ukaz ni uspel. Sporočilo o napaki se izpiše na stderr s predpono `Error: `.

### help

Možnost `--help` ponuja informacije o razpoložljivih kategorijah ukazov, podukazih in možnostih:

1. **Prikaz splošne pomoči:**
   ```bash
   digna --help
   ```

2. **Pridobivanje pomoči za določene kategorije in ukaze:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Izpis vključuje:**
   - **Opis ukaza:** Povzetek namena ukaza.
   - **Sintakso:** Obvezne in neobvezne argumente.
   - **Možnosti:** Zastavice in parametre, značilne za ukaz.

### version

Ukaz `version` izpiše nameščeno izdajo ***digna***. Ne bere nobene konfiguracije in ne preverja licence, zato deluje tudi v namestitvi, v kateri datoteka `config.toml` ali licenca manjka oziroma je neveljavna.

Različica izdaje je neodvisna od različice sheme repozitorija, ki jo javi [`repo check`](#repo-check).

#### Uporaba ukaza
```bash
digna version
```

#### Primer izpisa
```text
2026.06
```

---

## Upravljanje konfiguracije

---

### config check

Ukaz `config check` preveri konfiguracijsko datoteko (`config.toml`) in ugotovi, ali so vsi obvezni razdelki in nastavitve prisotni ter pravilno oblikovani. Vsak razdelek se preveri zase, tako da pokvarjen razdelek `[app]` ne prekrije stanja razdelka `[repo]`.

Poročani razdelki so:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — neobvezen; manjkajoč ključ preverjanje prestane, prisoten, a napačno oblikovan seznam pa ne

Ukaz namenoma ne naloži konfiguracije aplikacije tako, kot to storijo drugi ukazi, da lahko diagnosticira datoteko `config.toml`, ki bi ***digna*** sploh preprečila zagon.

#### Uporaba ukaza
```bash
digna config check [OPTIONS]
```

#### Možnosti
- `--configpath`, `-c`: Pot do konfiguracijske datoteke ali do imenika, ki vsebuje `config.toml` (privzeto `./config.toml`).
- `--json`: Izpiše poročilo o preverjanju v obliki JSON. Ima prednost pred `--quiet`.
- `--quiet`, `-q`: Zatre poročilo in se opira izključno na izhodno kodo.

#### Primer
```bash
digna config check
```

Preverjanje določene konfiguracijske datoteke z izpisom v obliki JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Primer izpisa
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

Manjkajoča datoteka ali skladenjska napaka TOML ne pusti ničesar, kar bi bilo mogoče preveriti razdelek za razdelkom, in je sporočena kot ena sama napaka namesto poročila, ne glede na `--quiet` ali `--json`.

---

## Upravljanje repozitorija

---

### repo check

Ukaz `repo check` preizkusi povezavo z zbirko podatkov ter preveri namestitev in različico repozitorija. Ne uspe, če nastavljena shema ne obstaja ali če obstaja, a ne vsebuje repozitorija ***digna***.

Javljena različica je različica sheme repozitorija, ki se različicira ločeno od izdaje ***digna***, ki jo izpiše [`version`](#version).

#### Uporaba ukaza
```bash
digna repo check
```

#### Primer izpisa
```text
Repo version 3.0.0 installed
```

### repo install

Ukaz `repo install` namesti nov repozitorij ***digna*** v shemo, nastavljeno v `config.toml`, in pri tem ustvari vsa potrebna zaporedja, tabele, indekse, omejitve in začetne zapise.

Sheme same ta ukaz **ne** ustvari — obstajati mora že prej. Ukaz se prav tako ne izvede, če je v tej shemi repozitorij že nameščen, in napoti na [`repo upgrade`](#repo-upgrade), če je nameščena različica starejša.

#### Uporaba ukaza
```bash
digna repo install
```

#### Primer izpisa
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Ukaz `repo upgrade` uveljavi migracije sheme zbirke podatkov, da obstoječi repozitorij posodobi na različico, ki jo pričakuje nameščena izdaja. Nadgradnje se uveljavljajo po en preskok različice naenkrat po ustaljeni poti nadgradnje, vsak dokončan preskok pa se zabeleži v repozitoriju.

Če je repozitorij že v pričakovani različici, ukaz sporoči, da nadgradnja ni potrebna, in ne spremeni ničesar.

#### Uporaba ukaza
```bash
digna repo upgrade
```

#### Primer izpisa
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Upravljanje šifriranja

---

### crypt gen-key

Ukaz `crypt gen-key` ustvari nov šifrirni ključ AES-GCM, namenjen uporabi kot šifrirni ključ v `config.toml`. Datoteka `config.toml`, ki jo je mogoče naložiti, mora že obstajati, čeprav ustvarjeni ključ od nje ni odvisen.

#### Uporaba ukaza
```bash
digna crypt gen-key
```

#### Primer izpisa
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Ukaz `crypt encrypt` šifrira niz (na primer geslo za zbirko podatkov) s ključem AES-GCM, nastavljenim v `config.toml`, in izpiše šifrirano besedilo.

#### Uporaba ukaza
```bash
digna crypt encrypt <VALUE>
```

#### Argumenti
- **VALUE**: Nešifriran niz, ki naj se šifrira (obvezno).

#### Primer
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Ukaz `crypt decrypt` dešifrira niz, šifriran z AES-GCM, s ključem, nastavljenim v `config.toml`, in izpiše nešifrirano besedilo.

#### Uporaba ukaza
```bash
digna crypt decrypt <VALUE>
```

#### Argumenti
- **VALUE**: Šifrirani niz, ki naj se dešifrira (obvezno).

#### Primer
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Upravljanje uporabnikov

---

### user add

Ukaz `user add` ustvari nov uporabniški račun v repozitoriju ***digna***. Ukaz ne uspe, če uporabnik z navedenim e-poštnim naslovom že obstaja.

#### Uporaba ukaza
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenti
- **EMAIL**: E-poštni naslov uporabnika (obvezno).
- **PASSWORD**: Začetno geslo uporabnika (obvezno).
- **DISPLAY_NAME**: Polno prikazno ime uporabnika (obvezno).

#### Možnosti
- `--admin`, `-a`: Ustvari uporabnika s skrbniškimi pravicami (superuporabnik).

#### Primer
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Za ustvarjanje skrbniškega računa:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Primer izpisa
```text
User created with ID: 42
```

### user list

Ukaz `user list` v obliki tabele izpiše vse registrirane uporabnike z ID-jem, e-poštnim naslovom, prikaznim imenom in skrbniško zastavico.

#### Uporaba ukaza
```bash
digna user list
```

#### Primer izpisa
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Ukaz `user modify` posodobi prikazno ime in skrbniške pravice obstoječega uporabniškega računa, določenega z e-poštnim naslovom.

Tako prikazno ime kot skrbniška zastavica se zapišeta vsakič. `--admin` je stikalo in ne vrednost: **če ga izpustite, se skrbniške pravice odvzamejo**, zato ga navedite vsakič, ko naj jih uporabnik obdrži ali pridobi.

#### Uporaba ukaza
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenti
- **EMAIL**: E-poštni naslov uporabnika, ki ga želite spremeniti (obvezno).
- **DISPLAY_NAME**: Posodobljeno prikazno ime (obvezno).

#### Možnosti
- `--admin`, `-a`: Dodeli skrbniške pravice. Izpustite, da jih odvzamete.
- `--valid-until`, `-v`: Sprejeto zaradi združljivosti, vendar se **trenutno ne uporablja**. Če ga navedete, se izpiše opozorilo in ne spremeni se nič.

#### Primer
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Primer izpisa
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Ukaz `user modify-pwd` posodobi geslo obstoječega uporabniškega računa.

#### Uporaba ukaza
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenti
- **EMAIL**: E-poštni naslov uporabnika, čigar geslo naj se posodobi (obvezno).
- **PASSWORD**: Novo geslo (obvezno).

#### Primer
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Ukaz `user delete` odstrani uporabniški račun iz sistema.

#### Uporaba ukaza
```bash
digna user delete <EMAIL>
```

#### Argumenti
- **EMAIL**: E-poštni naslov uporabnika, ki naj se izbriše (obvezno).

#### Primer
```bash
digna user delete jdoe@example.com
```

---

## Upravljanje projektov in podatkovnih virov

---

### project list

Ukaz `project list` izpiše vse projekte, ki so na voljo v repozitoriju, skupaj z njihovim ID-jem, imenom in opisom.

#### Uporaba ukaza
```bash
digna project list
```

#### Primer izpisa
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Ukaz `project list-ds` izpiše vse podatkovne vire, povezane z danim projektom, in prikaže njihov ID, ime, vrsto, shemo in ime tabele.

#### Uporaba ukaza
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, katerega podatkovne vire je treba izpisati (obvezno). Ime se mora ujemati natanko.

#### Primer
```bash
digna project list-ds ProjectA
```

#### Primer izpisa
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Ukaz `project export-ds` izvozi podatkovne vire projekta v dokument JSON.

Če nista navedena ne `--table-name` ne `--table-id`, se izvozijo vsi podatkovni viri projekta.

#### Uporaba ukaza
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Ime projekta, iz katerega naj se izvozijo podatkovni viri (obvezno).

#### Možnosti
- `--table-name`, `-n`: Imena podatkovnih virov za izvoz. Navedete lahko več imen, ločenih s presledki.
- `--table-id`, `-i`: ID-ji podatkovnih virov za izvoz. Navedete lahko več ID-jev, ločenih s presledki.
- `--exportfile`, `-f`: Pot, na katero naj se shranijo izvoženi podatkovni viri (privzeto: `data_sources_export.json`).

#### Primer
Za izvoz vseh podatkovnih virov iz projekta `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Za izvoz določenih tabel:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Primer izpisa
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Ukaz `project import-ds` uvozi podatkovne vire iz izvozne datoteke v ciljni projekt in za vsak objekt sporoči, kaj je bilo ustvarjeno, posodobljeno ali preskočeno.

#### Uporaba ukaza
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Ime ciljnega projekta, v katerega naj se uvozi (obvezno).
- **EXPORT_FILE**: Pot do izvozne datoteke JSON (obvezno).

#### Možnosti
- `--output-file`, `-o`: Datoteka, v katero naj se zapiše poročilo o uvozu. Brez nje gre poročilo na stdout.
- `--output-format`, `-f`: Oblika poročila o uvozu — `table`, `json` ali `csv` (privzeto: `table`).

#### Primer
```bash
digna project import-ds ProjectB my_export.json
```

Za strojno berljivo poročilo:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Poročilo zajema štiri ravni objektov — podatkovni vir, definicijo podatkovnega niza, atribut in pravilo preverjanja — vsako z njeno uvozno akcijo, rezultatom, ID-jem nastalega objekta in morebitnimi dodatnimi informacijami.

### project plan-import-ds

Ukaz `project plan-import-ds` predogleda uvoz podatkovnih virov v ciljni projekt in pokaže, kateri objekti bi bili ustvarjeni, posodobljeni ali preskočeni, ne da bi kar koli spremenil. Sprejme isto izvozno datoteko in iste možnosti poročanja kot [`project import-ds`](#project-import-ds), poleg tega pa doda še številko koraka za vsak načrtovani objekt.

#### Uporaba ukaza
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Ime ciljnega projekta (obvezno).
- **EXPORT_FILE**: Pot do izvozne datoteke (obvezno).

#### Možnosti
- `--output-file`, `-o`: Datoteka, v katero naj se zapiše načrt uvoza. Brez nje gre načrt na stdout.
- `--output-format`, `-f`: Oblika načrta uvoza — `table`, `json` ali `csv` (privzeto: `table`).

#### Primer
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Upravljanje pregledov

---

### inspection run

Ukaz `inspection run` ustvari zahtevo za pregled za projekt in datumski razpon, nato pa — odvisno od navedenih možnosti — bodisi počaka nanjo, se takoj vrne ali jo izvede v lastnem procesu.

Trije načini izvajanja so:

- **Privzeti (brez zastavice)**: zahteva se uvrsti v čakalno vrsto za zaledje, CLI pa jo vsaki dve sekundi poizveduje in izpisuje napredek opravil, dokler pregled ne doseže končnega stanja. Potreben je zagnan `digna serve`, sicer zahteve ne prevzame nič.
- **`--async-mode`**: zahteva se uvrsti v čakalno vrsto, njen ID pa se izpiše takoj. Za spremljanje uporabite [`inspection status`](#inspection-status).
- **`--bypass-backend`**: pregled izvede sam proces CLI in se ne uvrsti v čakalno vrsto, zato zagnan strežnik ni potreben.

`--async-mode` in `--bypass-backend` se medsebojno izključujeta.

V vseh načinih se ukaz konča z izhodno kodo, različno od nič, če se pregled ni uspešno zaključil.

#### Uporaba ukaza
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Ime ciljnega projekta (obvezno). Ime se mora ujemati natanko.
- **START_DATE**: Začetni datum razpona v obliki `YYYY-MM-DD` (obvezno).
- **END_DATE**: Končni datum razpona v obliki `YYYY-MM-DD` (obvezno).

#### Možnosti
- `--table-name`: Omeji pregled na en sam podatkovni vir projekta, določen z imenom tega podatkovnega vira. Brez nje se pregledajo vsi podatkovni viri projekta.
- `--async-mode`: Uvrsti pregled v čakalno vrsto in izpiše ID zahteve, namesto da bi čakal nanjo. Ni ga mogoče kombinirati z `--bypass-backend`.
- `--bypass-backend`: Izvede pregled neposredno v procesu CLI, namesto da bi ga uvrstil v čakalno vrsto za zaledje. Ni ga mogoče kombinirati z `--async-mode`.

#### Primer
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Za oddajo asinhronega pregleda:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Za pregled enega samega podatkovnega vira:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Primer izpisa
Privzeti način:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asinhroni način:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Ukaz `inspection status` po ID-ju zahteve poizve o stanju in napredku opravil zahteve za pregled.

#### Uporaba ukaza
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenti
- **INSPECTION_REQUEST_ID**: Številčni ID zahteve za pregled (obvezno).

#### Primer
```bash
digna inspection status 1024
```

#### Primer izpisa
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Ukaz `inspection abort` zahteva preklic pregledov, ki se izvajajo ali čakajo. Za vsako prizadeto zahtevo zabeleži dogodek ustavitve; nanj se odzove zaledje, zato je prekinitev prošnja za ustavitev in ne takojšnja prekinitev procesa.

#### Uporaba ukaza
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenti
- **INSPECTION_REQUEST_ID**: ID zahteve za pregled, ki naj se prekine. Obvezen, razen če je naveden `--killall`.

#### Možnosti
- `--killall`: Prekine vse trenutno izvajane in čakajoče zahteve za pregled. Ima prednost pred ID-jem zahteve, navedenim skupaj z njim.

#### Primer
Za prekinitev določene zahteve:
```bash
digna inspection abort 1024
```

Za prekinitev vseh dejavnih in čakajočih pregledov:
```bash
digna inspection abort --killall
```

#### Primer izpisa
`--killall` sporoči, kaj je storil; prekinitev ene same zahteve ne izpiše ničesar in o uspehu poroča z izhodno kodo.
```text
All running and pending inspections have been aborted.
```

---

## Upravljanje licenc

---

### license check

Ukaz `license check` preveri datoteko `license.toml`: njen podpis preveri z javnim ključem, priloženim namestitvi, in ugotovi, ali ni potekla. Ne bere nobene konfiguracije aplikacije, zato deluje tudi, preden je `config.toml` nastavljen.

#### Uporaba ukaza
```bash
digna license check
```

#### Primer izpisa
```text
License is valid
```

Neveljaven podpis in potekla licenca sta sporočena kot ločeni napaki, obe z izhodno kodo 1.

---

## Strežnik in storitve v ozadju

---

### serve

Ukaz `serve` zažene strežnik REST API ***digna*** skupaj z razporejevalnikom pregledov in upravljalnikom pregledov, ki tečeta v ozadju. Ob zagonu tudi označi kot neuspešen vsak pregled, ki ga repozitorij še vedno beleži kot izvajan, saj iz prejšnjega procesa ni moglo nič preživeti.

Ukaz teče v ospredju, dokler ga ne ustavite.

#### Uporaba ukaza
```bash
digna serve [OPTIONS]
```

#### Možnosti
- `--address`: Omrežni naslov, na katerega naj se veže strežnik API (privzeto: `127.0.0.1`).
- `--port`: Številka vrat, na katerih posluša (privzeto: `8000`).

#### Primer
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Primer izpisa
```text
Server running on http://0.0.0.0:8000
```
