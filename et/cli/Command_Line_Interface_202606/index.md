# digna CLI teatmik 2026.06
**2026-09-05**

Sellel lehel on dokumenteeritud kõik käsud, mis on saadaval ***digna*** CLI versioonis **2026.06**, koos kasutusnäidete ja valikutega.

Käivitatav fail kannab nime `digna`.

---

## CLI põhitõed

---

### Ülevaade ja süntaks

Versiooni **2026.06** CLI kasutab struktureeritud, kategooriapõhist käsuhierarhiat:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` ja `serve` on üksikkäsud ilma alamkäsuta:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Üldised valikud

Järgmised üldised valikud kehtivad kõigi käskude puhul:

- `--help`, `-h`: Kuvab abiteavet CLI või konkreetse käsukategooria või alamkäsu kohta.
- `--stacktrace`: Kuvab tõrke korral kogu vigade ahela, mitte üksnes ülemise taseme teate.

`--stacktrace` on üldine valik kitsas tähenduses: see tuleb anda **enne** käsukategooriat, mitte selle järel.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Lippu `--version` ei ole olemas. Kasutage selle asemel käsku [`version`](#version).

### Eeldused

Enamik käske vajab loetavat ja kehtivat faili `config.toml`; mõned nõuavad lisaks kehtivat litsentsi.
Järgmine tabel näitab, mida iga käsukategooria enne mis tahes tegevust laadib:

| Käsukategooria | Vajab faili `config.toml` | Vajab kehtivat litsentsi |
|---|---|---|
| `version` | ei | ei |
| `config check` | ei (see ongi see, mille kohta käsk aru annab) | ei |
| `license check` | ei | see *ongi* kontroll |
| `crypt` | jah | ei |
| `serve` | jah | ei |
| `project` | jah | ei |
| `user` | jah | jah |
| `inspection` | jah | jah |
| `repo` | jah | jah |

Kui litsents on nõutav, kontrollitakse nii selle allkirja kui ka aegumiskuupäeva, ning käsk katkeb enne hoidla puudutamist, kui kumbki neist ebaõnnestub.

### Väljumiskoodid

- `0`: käsk õnnestus.
- `1`: käsk ebaõnnestus. Veateade kirjutatakse standardveavoogu (stderr) eesliitega `Error: `.

### help

Valik `--help` annab teavet saadaolevate käsukategooriate, alamkäskude ja valikute kohta:

1. **Üldise abi kuvamine:**
   ```bash
   digna --help
   ```

2. **Abi saamine kindlate kategooriate ja käskude kohta:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Väljund sisaldab:**
   - **Käsu kirjeldust:** Kokkuvõtet käsu otstarbest.
   - **Süntaksit:** Kohustuslikke ja valikulisi argumente.
   - **Valikuid:** Käsule omaseid lippe ja parameetreid.

### version

Käsk `version` väljastab paigaldatud ***digna*** versiooni. See ei loe ühtki seadistust ega valideeri litsentsi, seega töötab ka paigalduses, mille `config.toml` või litsents puudub või on kehtetu.

Väljalaske versioon on sõltumatu hoidla skeemi versioonist, mille kohta annab teada [`repo check`](#repo-check).

#### Käsu kasutamine
```bash
digna version
```

#### Näidisväljund
```text
2026.06
```

---

## Seadistuste haldus

---

### config check

Käsk `config check` valideerib seadistusfaili (`config.toml`), kontrollides, et kõik kohustuslikud sektsioonid ja seaded on olemas ning korrektselt vormindatud. Iga sektsiooni valideeritakse eraldi, nii et katkine sektsioon `[app]` ei varja sektsiooni `[repo]` seisundit.

Aruandes käsitletavad sektsioonid on:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — valikuline; puuduv võti läbib kontrolli, olemasolev kuid vigane loend aga ebaõnnestub

Käsk ei laadi meelega rakenduse seadistust nii, nagu teevad teised käsud, et suuta diagnoosida faili `config.toml`, mis takistaks ***digna*** üldse käivitumast.

#### Käsu kasutamine
```bash
digna config check [OPTIONS]
```

#### Valikud
- `--configpath`, `-c`: Tee seadistusfailini või kataloogini, mis sisaldab faili `config.toml` (vaikimisi `./config.toml`).
- `--json`: Väljastab valideerimisaruande JSON-vormingus. On ülimuslik valiku `--quiet` suhtes.
- `--quiet`, `-q`: Peidab aruande ja tugineb üksnes väljumiskoodile.

#### Näide
```bash
digna config check
```

Kindla seadistusfaili valideerimine ja väljundi vormindamine JSON-ina:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Näidisväljund
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

Puuduv fail või TOML-i süntaksiviga ei jäta midagi sektsioonide kaupa valideerida ning sellest teatatakse ühe veana aruande asemel, sõltumata valikutest `--quiet` või `--json`.

---

## Hoidla haldus

---

### repo check

Käsk `repo check` katsetab andmebaasiühendust ning kontrollib hoidla paigaldust ja versiooni. See ebaõnnestub, kui seadistatud skeemi ei ole olemas või kui see on olemas, kuid ei sisalda ***digna*** hoidlat.

Teatatav versioon on hoidla skeemi versioon, mida versioonitakse eraldi ***digna*** väljalaskest, mille väljastab [`version`](#version).

#### Käsu kasutamine
```bash
digna repo check
```

#### Näidisväljund
```text
Repo version 3.0.0 installed
```

### repo install

Käsk `repo install` paigaldab uue ***digna*** hoidla failis `config.toml` seadistatud skeemi, luues kõik vajalikud jadad, tabelid, indeksid, kitsendused ja algkirjed.

Skeemi ennast see käsk **ei** loo — see peab olema eelnevalt olemas. Samuti keeldub käsk töötamast, kui selles skeemis on hoidla juba paigaldatud, ning viitab käsule [`repo upgrade`](#repo-upgrade), kui paigaldatud versioon on vanem.

#### Käsu kasutamine
```bash
digna repo install
```

#### Näidisväljund
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Käsk `repo upgrade` rakendab andmebaasi skeemi migratsioone, et viia olemasolev hoidla versioonile, mida paigaldatud väljalase eeldab. Uuendusi rakendatakse ühe versioonisammu kaupa mööda kindlaksmääratud uuendusteed ning iga lõpetatud samm jäädvustatakse hoidlas.

Kui hoidla on juba eeldataval versioonil, teatab käsk, et uuendamist pole vaja, ega tee muudatusi.

#### Käsu kasutamine
```bash
digna repo upgrade
```

#### Näidisväljund
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Krüpteerimise haldus

---

### crypt gen-key

Käsk `crypt gen-key` loob uue AES-GCM krüpteerimisvõtme, mida kasutatakse krüpteerimisvõtmena failis `config.toml`. Laaditav `config.toml` peab juba olemas olema, kuigi loodav võti sellest ei sõltu.

#### Käsu kasutamine
```bash
digna crypt gen-key
```

#### Näidisväljund
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Käsk `crypt encrypt` krüpteerib sõne (näiteks andmebaasi parooli) failis `config.toml` seadistatud AES-GCM võtmega ja väljastab krüptogrammi.

#### Käsu kasutamine
```bash
digna crypt encrypt <VALUE>
```

#### Argumendid
- **VALUE**: Krüpteeritav avatekstiline sõne (kohustuslik).

#### Näide
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Käsk `crypt decrypt` dekrüpteerib AES-GCM-iga krüpteeritud sõne failis `config.toml` seadistatud võtmega ja väljastab avateksti.

#### Käsu kasutamine
```bash
digna crypt decrypt <VALUE>
```

#### Argumendid
- **VALUE**: Dekrüpteeritav krüpteeritud sõne (kohustuslik).

#### Näide
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Kasutajahaldus

---

### user add

Käsk `user add` loob ***digna*** hoidlas uue kasutajakonto. Käsk ebaõnnestub, kui antud e-posti aadressiga kasutaja on juba olemas.

#### Käsu kasutamine
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumendid
- **EMAIL**: Kasutaja e-posti aadress (kohustuslik).
- **PASSWORD**: Kasutaja esialgne parool (kohustuslik).
- **DISPLAY_NAME**: Kasutaja täielik kuvatav nimi (kohustuslik).

#### Valikud
- `--admin`, `-a`: Loob kasutaja administraatori (superkasutaja) õigustega.

#### Näide
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Administraatorikonto loomiseks:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Näidisväljund
```text
User created with ID: 42
```

### user list

Käsk `user list` loetleb kõik registreeritud kasutajad tabelina koos ID, e-posti aadressi, kuvatava nime ja administraatorilipuga.

#### Käsu kasutamine
```bash
digna user list
```

#### Näidisväljund
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Käsk `user modify` uuendab olemasoleva kasutajakonto kuvatavat nime ja administraatoriõigusi; konto tuvastatakse e-posti aadressi järgi.

Nii kuvatav nimi kui ka administraatorilipp kirjutatakse alati. `--admin` on lüliti, mitte väärtus: **selle ärajätmine võtab administraatoriõigused ära**, seega andke see alati, kui kasutaja peab need säilitama või saama.

#### Käsu kasutamine
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumendid
- **EMAIL**: Muudetava kasutaja e-posti aadress (kohustuslik).
- **DISPLAY_NAME**: Uuendatud kuvatav nimi (kohustuslik).

#### Valikud
- `--admin`, `-a`: Annab administraatoriõigused. Jätke ära nende äravõtmiseks.
- `--valid-until`, `-v`: Aktsepteeritakse ühilduvuse huvides, kuid **praegu ei rakendata**. Selle andmine väljastab hoiatuse ega muuda midagi.

#### Näide
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Näidisväljund
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Käsk `user modify-pwd` uuendab olemasoleva kasutajakonto parooli.

#### Käsu kasutamine
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumendid
- **EMAIL**: Selle kasutaja e-posti aadress, kelle parooli uuendatakse (kohustuslik).
- **PASSWORD**: Uus parool (kohustuslik).

#### Näide
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Käsk `user delete` eemaldab kasutajakonto süsteemist.

#### Käsu kasutamine
```bash
digna user delete <EMAIL>
```

#### Argumendid
- **EMAIL**: Kustutatava kasutaja e-posti aadress (kohustuslik).

#### Näide
```bash
digna user delete jdoe@example.com
```

---

## Projektide ja andmeallikate haldus

---

### project list

Käsk `project list` loetleb kõik hoidlas saadaolevad projektid, näidates nende ID-d, nime ja kirjeldust.

#### Käsu kasutamine
```bash
digna project list
```

#### Näidisväljund
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Käsk `project list-ds` loetleb kõik antud projektiga seotud andmeallikad, kuvades nende ID, nime, liigi, skeemi ja tabeli nime.

#### Käsu kasutamine
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumendid
- **PROJECT_NAME**: Selle projekti nimi, mille andmeallikad loetletakse (kohustuslik). Nimi peab täpselt kattuma.

#### Näide
```bash
digna project list-ds ProjectA
```

#### Näidisväljund
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Käsk `project export-ds` ekspordib projekti andmeallikad JSON-dokumenti.

Kui ei anta ei `--table-name` ega `--table-id`, eksporditakse kõik projekti andmeallikad.

#### Käsu kasutamine
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumendid
- **PROJECT_NAME**: Selle projekti nimi, millest andmeallikad eksporditakse (kohustuslik).

#### Valikud
- `--table-name`, `-n`: Eksporditavate andmeallikate nimed. Mitu nime saab anda tühikutega eraldatult.
- `--table-id`, `-i`: Eksporditavate andmeallikate ID-d. Mitu ID-d saab anda tühikutega eraldatult.
- `--exportfile`, `-f`: Tee, kuhu eksporditud andmeallikad salvestatakse (vaikimisi: `data_sources_export.json`).

#### Näide
Kõigi andmeallikate eksportimiseks projektist `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Kindlate tabelite eksportimiseks:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Näidisväljund
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Käsk `project import-ds` impordib andmeallikad ekspordifailist sihtprojekti ja teatab objektide kaupa, mis loodi, mida uuendati ja mis jäeti vahele.

#### Käsu kasutamine
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumendid
- **PROJECT_NAME**: Sihtprojekti nimi, kuhu imporditakse (kohustuslik).
- **EXPORT_FILE**: Tee JSON-ekspordifailini (kohustuslik).

#### Valikud
- `--output-file`, `-o`: Fail, kuhu impordiaruanne kirjutatakse. Ilma selleta läheb aruanne standardväljundisse (stdout).
- `--output-format`, `-f`: Impordiaruande vorming — `table`, `json` või `csv` (vaikimisi: `table`).

#### Näide
```bash
digna project import-ds ProjectB my_export.json
```

Masinloetava aruande saamiseks:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Aruanne hõlmab nelja objektitasandit — andmeallikas, andmekogumi definitsioon, atribuut ja valideerimisreegel — igaüks koos impordi toimingu, tulemuse, saadud objekti ID ja võimaliku lisateabega.

### project plan-import-ds

Käsk `project plan-import-ds` kuvab andmeallikate impordi eelvaate sihtprojekti, näidates, millised objektid loodaks, uuendataks või jäetaks vahele, ilma midagi muutmata. See võtab sama ekspordifaili ja samad aruandevalikud nagu [`project import-ds`](#project-import-ds) ning lisab iga kavandatud objekti kohta sammu numbri.

#### Käsu kasutamine
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumendid
- **PROJECT_NAME**: Sihtprojekti nimi (kohustuslik).
- **EXPORT_FILE**: Tee ekspordifailini (kohustuslik).

#### Valikud
- `--output-file`, `-o`: Fail, kuhu impordiplaan kirjutatakse. Ilma selleta läheb plaan standardväljundisse (stdout).
- `--output-format`, `-f`: Impordiplaani vorming — `table`, `json` või `csv` (vaikimisi: `table`).

#### Näide
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Kontrollide haldus

---

### inspection run

Käsk `inspection run` loob projekti ja kuupäevavahemiku kohta kontrollipäringu ning seejärel — olenevalt antud valikutest — kas ootab selle lõppu, naaseb kohe või käivitab selle omaenda protsessis.

Kolm täitmisrežiimi on:

- **Vaikimisi (liputa)**: päring pannakse taustsüsteemi järjekorda ning CLI pärib selle olekut iga kahe sekundi järel, väljastades ülesannete edenemist, kuni kontroll jõuab lõppseisundisse. Vajalik on töötav `digna serve`, muidu ei võta keegi päringut vastu.
- **`--async-mode`**: päring pannakse järjekorda ja selle ID väljastatakse kohe. Selle jälgimiseks kasutage käsku [`inspection status`](#inspection-status).
- **`--bypass-backend`**: kontrolli täidab CLI protsess ise ja seda ei panda järjekorda, seega ei ole töötavat serverit vaja.

`--async-mode` ja `--bypass-backend` välistavad teineteist.

Igas režiimis lõpeb käsk nullist erineva väljumiskoodiga, kui kontroll ei lõppenud edukalt.

#### Käsu kasutamine
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumendid
- **PROJECT_NAME**: Sihtprojekti nimi (kohustuslik). Nimi peab täpselt kattuma.
- **START_DATE**: Kuupäevavahemiku alguskuupäev vormingus `YYYY-MM-DD` (kohustuslik).
- **END_DATE**: Kuupäevavahemiku lõppkuupäev vormingus `YYYY-MM-DD` (kohustuslik).

#### Valikud
- `--table-name`: Piirab kontrolli projekti ühe andmeallikaga, mis antakse andmeallika nime järgi. Ilma selleta kontrollitakse kõiki projekti andmeallikaid.
- `--async-mode`: Paneb kontrolli järjekorda ja väljastab päringu ID selle ootamise asemel. Ei saa kombineerida valikuga `--bypass-backend`.
- `--bypass-backend`: Käivitab kontrolli otse CLI protsessis, selle asemel et panna see taustsüsteemi järjekorda. Ei saa kombineerida valikuga `--async-mode`.

#### Näide
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Asünkroonse kontrolli esitamiseks:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Ühe andmeallika kontrollimiseks:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Näidisväljund
Vaikerežiim:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asünkroonne režiim:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Käsk `inspection status` pärib kontrollipäringu olekut ja ülesannete edenemist päringu ID järgi.

#### Käsu kasutamine
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumendid
- **INSPECTION_REQUEST_ID**: Kontrollipäringu numbriline ID (kohustuslik).

#### Näide
```bash
digna inspection status 1024
```

#### Näidisväljund
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Käsk `inspection abort` taotleb töötavate või ootel kontrollipäringute tühistamist. See salvestab iga mõjutatud päringu kohta peatamissündmuse; taustsüsteem tegutseb selle alusel, seega on katkestamine peatamistaotlus, mitte kohene lõpetamine.

#### Käsu kasutamine
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumendid
- **INSPECTION_REQUEST_ID**: Katkestatava kontrollipäringu ID. Kohustuslik, kui ei anta valikut `--killall`.

#### Valikud
- `--killall`: Katkestab kõik parajasti töötavad ja ootel kontrollipäringud. On ülimuslik samal ajal antud päringu ID suhtes.

#### Näide
Kindla päringu katkestamiseks:
```bash
digna inspection abort 1024
```

Kõigi aktiivsete ja järjekorras olevate kontrollide katkestamiseks:
```bash
digna inspection abort --killall
```

#### Näidisväljund
`--killall` teatab, mida ta tegi; üksiku päringu katkestamine ei anna väljundit ja teatab õnnestumisest väljumiskoodi kaudu.
```text
All running and pending inspections have been aborted.
```

---

## Litsentside haldus

---

### license check

Käsk `license check` valideerib faili `license.toml`, kontrollides selle allkirja paigaldusega kaasas oleva avaliku võtme vastu ja veendudes, et see ei ole aegunud. See ei loe rakenduse seadistust, seega töötab ka enne faili `config.toml` seadistamist.

#### Käsu kasutamine
```bash
digna license check
```

#### Näidisväljund
```text
License is valid
```

Kehtetust allkirjast ja aegunud litsentsist teatatakse eraldiseisvate vigadena, mõlemad väljumiskoodiga 1.

---

## Server ja taustateenused

---

### serve

Käsk `serve` käivitab ***digna*** REST API serveri koos tausta kontrolliajastaja ja kontrollihalduriga. Käivitumisel märgib see ka ebaõnnestunuks iga kontrolli, mida hoidla endiselt töötavana kajastab, kuna varasemast protsessist ei saa miski olla ellu jäänud.

Käsk töötab esiplaanil, kuni see peatatakse.

#### Käsu kasutamine
```bash
digna serve [OPTIONS]
```

#### Valikud
- `--address`: Võrguaadress, millega API server seotakse (vaikimisi: `127.0.0.1`).
- `--port`: Pordi number, mida kuulatakse (vaikimisi: `8000`).

#### Näide
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Näidisväljund
```text
Server running on http://0.0.0.0:8000
```