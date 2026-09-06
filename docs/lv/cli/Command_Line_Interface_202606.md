---
title: digna CLI rokasgrāmata 2026.06 – komandas un piemēri | digna dokumentācija
description: Pilnīga digna CLI 2026.06 laidiena rokasgrāmata
image: /assets/logo_square.png
---

# digna CLI rokasgrāmata 2026.06
**2026-09-05**

Šajā lapā ir dokumentēts pilns komandu kopums, kas pieejams ***digna*** CLI **2026.06** laidienā, tostarp lietošanas piemēri un opcijas.

Izpildāmais fails saucas `digna`.

---

## CLI pamati

---

### Pārskats un sintakse

**2026.06** laidiena CLI izmanto strukturētu, uz kategorijām balstītu komandu hierarhiju:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` un `serve` ir atsevišķas komandas bez apakškomandas:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globālās opcijas

Turpmāk minētās globālās opcijas attiecas uz visām komandām:

- `--help`, `-h`: Parāda palīdzības informāciju par CLI vai par konkrētu komandu kategoriju vai apakškomandu.
- `--stacktrace`: Kļūmes gadījumā parāda visu kļūdu ķēdi, nevis tikai augšējā līmeņa ziņojumu.

`--stacktrace` ir globāla opcija šaurā nozīmē: tā jānorāda **pirms** komandu kategorijas, nevis pēc tās.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Karodziņa `--version` nav. Tā vietā izmantojiet komandu [`version`](#version).

### Priekšnosacījumi

Lielākajai daļai komandu ir nepieciešams nolasāms, derīgs `config.toml`; dažām papildus nepieciešama derīga licence.
Nākamajā tabulā ir atspoguļots, ko katra komandu kategorija ielādē, pirms tā vispār kaut ko dara:

| Komandu kategorija | Nepieciešams `config.toml` | Nepieciešama derīga licence |
|---|---|---|
| `version` | nē | nē |
| `config check` | nē (tieši par to komanda arī ziņo) | nē |
| `license check` | nē | tā *ir* pati pārbaude |
| `crypt` | jā | nē |
| `serve` | jā | nē |
| `project` | jā | nē |
| `user` | jā | jā |
| `inspection` | jā | jā |
| `repo` | jā | jā |

Kur licence ir nepieciešama, tiek pārbaudīts gan tās paraksts, gan derīguma termiņš, un komanda tiek pārtraukta pirms pieskaršanās repozitorijam, ja kāda no pārbaudēm neizdodas.

### Iziešanas kodi

- `0`: komanda izdevās.
- `1`: komanda neizdevās. Kļūdas ziņojums tiek ierakstīts stderr plūsmā ar priedēkli `Error: `.

### help

Opcija `--help` sniedz informāciju par pieejamajām komandu kategorijām, apakškomandām un opcijām:

1. **Vispārīgās palīdzības parādīšana:**
   ```bash
   digna --help
   ```

2. **Palīdzības iegūšana par konkrētām kategorijām un komandām:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Izvadē ietilpst:**
   - **Komandas apraksts:** Komandas mērķa kopsavilkums.
   - **Sintakse:** Obligātie un neobligātie argumenti.
   - **Opcijas:** Konkrētajai komandai raksturīgie karodziņi un parametri.

### version

Komanda `version` izvada instalēto ***digna*** laidienu. Tā nelasa nekādu konfigurāciju un nepārbauda licenci, tāpēc darbojas arī tādā instalācijā, kurai `config.toml` vai licence trūkst vai ir nederīga.

Laidiena versija ir neatkarīga no repozitorija shēmas versijas, par kuru ziņo [`repo check`](#repo-check).

#### Komandas lietojums
```bash
digna version
```

#### Izvades piemērs
```text
2026.06
```

---

## Konfigurācijas pārvaldība

---

### config check

Komanda `config check` pārbauda konfigurācijas failu (`config.toml`), pārliecinoties, ka visas obligātās sadaļas un iestatījumi ir klāt un pareizi formatēti. Katra sadaļa tiek pārbaudīta atsevišķi, tāpēc bojāta sadaļa `[app]` neaizsedz sadaļas `[repo]` stāvokli.

Pārskatā iekļautās sadaļas ir:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — neobligāta; trūkstoša atslēga pārbaudi iztur, bet esošs, taču nepareizi veidots saraksts to neiztur

Komanda apzināti neielādē lietojumprogrammas konfigurāciju tāpat kā pārējās komandas, lai tā spētu diagnosticēt `config.toml`, kas ***digna*** vispār neļautu startēt.

#### Komandas lietojums
```bash
digna config check [OPTIONS]
```

#### Opcijas
- `--configpath`, `-c`: Ceļš līdz konfigurācijas failam vai līdz mapei, kurā atrodas `config.toml` (noklusējums `./config.toml`).
- `--json`: Izvada pārbaudes pārskatu JSON formātā. Tai ir priekšroka pār `--quiet`.
- `--quiet`, `-q`: Slēpj pārskatu un paļaujas vienīgi uz iziešanas kodu.

#### Piemērs
```bash
digna config check
```

Pārbaudīt konkrētu konfigurācijas failu un formatēt izvadi kā JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Izvades piemērs
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

Trūkstošs fails vai TOML sintakses kļūda neatstāj neko, ko pārbaudīt pa sadaļām, un par to tiek ziņots kā par vienu kļūdu, nevis pārskatu, neatkarīgi no `--quiet` vai `--json`.

---

## Repozitorija pārvaldība

---

### repo check

Komanda `repo check` pārbauda datubāzes savienojumu un apstiprina repozitorija instalāciju un versiju. Tā neizdodas, ja konfigurētā shēma neeksistē vai ja tā eksistē, bet nesatur ***digna*** repozitoriju.

Ziņotā versija ir repozitorija shēmas versija, kas tiek versionēta atsevišķi no ***digna*** laidiena, kuru izvada [`version`](#version).

#### Komandas lietojums
```bash
digna repo check
```

#### Izvades piemērs
```text
Repo version 3.0.0 installed
```

### repo install

Komanda `repo install` instalē jaunu ***digna*** repozitoriju `config.toml` failā konfigurētajā shēmā, izveidojot visas nepieciešamās sekvences, tabulas, indeksus, ierobežojumus un sākotnējos ierakstus.

Pašu shēmu šī komanda **neizveido** — tai jāpastāv iepriekš. Komanda arī atsakās darboties, ja šajā shēmā jau ir instalēts repozitorijs, un norāda uz [`repo upgrade`](#repo-upgrade), ja instalētā versija ir vecāka.

#### Komandas lietojums
```bash
digna repo install
```

#### Izvades piemērs
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Komanda `repo upgrade` piemēro datubāzes shēmas migrācijas, lai esošu repozitoriju paceltu līdz versijai, ko sagaida instalētais laidiens. Jauninājumi tiek piemēroti pa vienam versijas solim pa noteiktu jaunināšanas ceļu, un katrs pabeigtais solis tiek reģistrēts repozitorijā.

Ja repozitorijs jau ir sagaidāmajā versijā, komanda ziņo, ka jauninājums nav vajadzīgs, un neveic nekādas izmaiņas.

#### Komandas lietojums
```bash
digna repo upgrade
```

#### Izvades piemērs
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Šifrēšanas pārvaldība

---

### crypt gen-key

Komanda `crypt gen-key` ģenerē jaunu AES-GCM šifrēšanas atslēgu, ko izmantot kā šifrēšanas atslēgu failā `config.toml`. Ielādējamam `config.toml` jau jāpastāv, kaut arī ģenerētā atslēga no tā nav atkarīga.

#### Komandas lietojums
```bash
digna crypt gen-key
```

#### Izvades piemērs
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Komanda `crypt encrypt` šifrē virkni (piemēram, datubāzes paroli), izmantojot failā `config.toml` konfigurēto AES-GCM atslēgu, un izvada šifrēto tekstu.

#### Komandas lietojums
```bash
digna crypt encrypt <VALUE>
```

#### Argumenti
- **VALUE**: Šifrējamā atklātā teksta virkne (obligāts).

#### Piemērs
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Komanda `crypt decrypt` atšifrē ar AES-GCM šifrētu virkni, izmantojot failā `config.toml` konfigurēto atslēgu, un izvada atklāto tekstu.

#### Komandas lietojums
```bash
digna crypt decrypt <VALUE>
```

#### Argumenti
- **VALUE**: Atšifrējamā šifrētā teksta virkne (obligāts).

#### Piemērs
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Lietotāju pārvaldība

---

### user add

Komanda `user add` izveido jaunu lietotāja kontu ***digna*** repozitorijā. Komanda neizdodas, ja lietotājs ar norādīto e-pasta adresi jau pastāv.

#### Komandas lietojums
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenti
- **EMAIL**: Lietotāja e-pasta adrese (obligāts).
- **PASSWORD**: Lietotāja sākotnējā parole (obligāts).
- **DISPLAY_NAME**: Pilnais lietotāja attēlojamais vārds (obligāts).

#### Opcijas
- `--admin`, `-a`: Izveido lietotāju ar administratora (superlietotāja) tiesībām.

#### Piemērs
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Lai izveidotu administratora kontu:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Izvades piemērs
```text
User created with ID: 42
```

### user list

Komanda `user list` tabulas veidā uzskaita visus reģistrētos lietotājus ar ID, e-pastu, attēlojamo vārdu un administratora karogu.

#### Komandas lietojums
```bash
digna user list
```

#### Izvades piemērs
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Komanda `user modify` atjaunina esoša lietotāja konta, kas identificēts pēc e-pasta adreses, attēlojamo vārdu un administratora tiesības.

Gan attēlojamais vārds, gan administratora karogs vienmēr tiek ierakstīti. `--admin` ir slēdzis, nevis vērtība: **tās izlaišana atsauc administratora tiesības**, tāpēc norādiet to ikreiz, kad lietotājam tās jāpatur vai jāiegūst.

#### Komandas lietojums
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenti
- **EMAIL**: Maināmā lietotāja e-pasts (obligāts).
- **DISPLAY_NAME**: Atjauninātais attēlojamais vārds (obligāts).

#### Opcijas
- `--admin`, `-a`: Piešķir administratora tiesības. Izlaidiet, lai tās atsauktu.
- `--valid-until`, `-v`: Tiek pieņemta saderības dēļ, taču **pašlaik netiek piemērota**. Tās norādīšana izvada brīdinājumu un neko nemaina.

#### Piemērs
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Izvades piemērs
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Komanda `user modify-pwd` atjaunina esoša lietotāja konta paroli.

#### Komandas lietojums
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenti
- **EMAIL**: Tā lietotāja e-pasts, kura parole jāatjaunina (obligāts).
- **PASSWORD**: Jaunā parole (obligāts).

#### Piemērs
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Komanda `user delete` noņem lietotāja kontu no sistēmas.

#### Komandas lietojums
```bash
digna user delete <EMAIL>
```

#### Argumenti
- **EMAIL**: Dzēšamā lietotāja e-pasts (obligāts).

#### Piemērs
```bash
digna user delete jdoe@example.com
```

---

## Projektu un datu avotu pārvaldība

---

### project list

Komanda `project list` uzskaita visus repozitorijā pieejamos projektus, parādot to ID, nosaukumu un aprakstu.

#### Komandas lietojums
```bash
digna project list
```

#### Izvades piemērs
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Komanda `project list-ds` uzskaita visus ar konkrētu projektu saistītos datu avotus, parādot to ID, nosaukumu, veidu, shēmu un tabulas nosaukumu.

#### Komandas lietojums
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Tā projekta nosaukums, kura datu avoti jāuzskaita (obligāts). Nosaukumam jāsakrīt precīzi.

#### Piemērs
```bash
digna project list-ds ProjectA
```

#### Izvades piemērs
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Komanda `project export-ds` eksportē projekta datu avotus JSON dokumentā.

Ja nav norādīts ne `--table-name`, ne `--table-id`, tiek eksportēti visi projekta datu avoti.

#### Komandas lietojums
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Tā projekta nosaukums, no kura eksportēt datu avotus (obligāts).

#### Opcijas
- `--table-name`, `-n`: Eksportējamo datu avotu nosaukumi. Vairākus nosaukumus var norādīt, atdalot ar atstarpēm.
- `--table-id`, `-i`: Eksportējamo datu avotu ID. Vairākus ID var norādīt, atdalot ar atstarpēm.
- `--exportfile`, `-f`: Ceļš, kurā saglabāt eksportētos datu avotus (noklusējums: `data_sources_export.json`).

#### Piemērs
Lai eksportētu visus datu avotus no `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Lai eksportētu konkrētas tabulas:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Izvades piemērs
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Komanda `project import-ds` importē datu avotus no eksporta faila mērķa projektā un par katru objektu ziņo, kas tika izveidots, atjaunināts vai izlaists.

#### Komandas lietojums
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Mērķa projekta nosaukums, kurā importēt (obligāts).
- **EXPORT_FILE**: Ceļš līdz JSON eksporta failam (obligāts).

#### Opcijas
- `--output-file`, `-o`: Fails, kurā ierakstīt importa pārskatu. Bez tā pārskats tiek novirzīts uz stdout.
- `--output-format`, `-f`: Importa pārskata formāts — `table`, `json` vai `csv` (noklusējums: `table`).

#### Piemērs
```bash
digna project import-ds ProjectB my_export.json
```

Lai iegūtu mašīnlasāmu pārskatu:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Pārskats aptver četrus objektu līmeņus — datu avotu, datu kopas definīciju, atribūtu un validācijas noteikumu — katru ar tā importa darbību, rezultātu, iegūtā objekta ID un jebkādu papildu informāciju.

### project plan-import-ds

Komanda `project plan-import-ds` parāda datu avotu importa priekšskatījumu mērķa projektā, norādot, kuri objekti tiktu izveidoti, atjaunināti vai izlaisti, neko nemainot. Tā pieņem to pašu eksporta failu un tās pašas pārskata opcijas kā [`project import-ds`](#project-import-ds) un katram plānotajam objektam pievieno soļa numuru.

#### Komandas lietojums
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Mērķa projekta nosaukums (obligāts).
- **EXPORT_FILE**: Ceļš līdz eksporta failam (obligāts).

#### Opcijas
- `--output-file`, `-o`: Fails, kurā ierakstīt importa plānu. Bez tā plāns tiek novirzīts uz stdout.
- `--output-format`, `-f`: Importa plāna formāts — `table`, `json` vai `csv` (noklusējums: `table`).

#### Piemērs
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Pārbaužu pārvaldība

---

### inspection run

Komanda `inspection run` izveido pārbaudes pieprasījumu projektam un datumu diapazonam un pēc tam — atkarībā no norādītajām opcijām — vai nu gaida to, vai atgriežas nekavējoties, vai izpilda to savā procesā.

Trīs izpildes režīmi ir:

- **Noklusējums (bez karodziņa)**: pieprasījums tiek ievietots aizmugursistēmas rindā, un CLI to aptaujā ik pēc divām sekundēm, izvadot uzdevumu norisi, līdz pārbaude sasniedz galīgo stāvokli. Nepieciešams darbojošs `digna serve`, citādi pieprasījumu neviens nepaņem.
- **`--async-mode`**: pieprasījums tiek ievietots rindā, un tā ID tiek izvadīts nekavējoties. Lai to izsekotu, izmantojiet [`inspection status`](#inspection-status).
- **`--bypass-backend`**: pārbaudi izpilda pats CLI process, un tā netiek ievietota rindā, tāpēc darbojošs serveris nav nepieciešams.

`--async-mode` un `--bypass-backend` viena otru izslēdz.

Ikvienā režīmā komanda beidzas ar iziešanas kodu, kas nav nulle, ja pārbaude netika sekmīgi pabeigta.

#### Komandas lietojums
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenti
- **PROJECT_NAME**: Mērķa projekta nosaukums (obligāts). Nosaukumam jāsakrīt precīzi.
- **START_DATE**: Datumu diapazona sākuma datums formātā `YYYY-MM-DD` (obligāts).
- **END_DATE**: Datumu diapazona beigu datums formātā `YYYY-MM-DD` (obligāts).

#### Opcijas
- `--table-name`: Ierobežo pārbaudi ar vienu projekta datu avotu, kas norādīts pēc datu avota nosaukuma. Bez tās tiek pārbaudīti visi projekta datu avoti.
- `--async-mode`: Ievieto pārbaudi rindā un izvada pieprasījuma ID, nevis gaida tās pabeigšanu. Nevar apvienot ar `--bypass-backend`.
- `--bypass-backend`: Izpilda pārbaudi tieši CLI procesā, nevis ievieto to aizmugursistēmas rindā. Nevar apvienot ar `--async-mode`.

#### Piemērs
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Lai iesniegtu asinhronu pārbaudi:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Lai pārbaudītu vienu datu avotu:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Izvades piemērs
Noklusējuma režīms:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asinhronais režīms:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Komanda `inspection status` pēc pieprasījuma ID noskaidro pārbaudes pieprasījuma stāvokli un uzdevumu norisi.

#### Komandas lietojums
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenti
- **INSPECTION_REQUEST_ID**: Pārbaudes pieprasījuma skaitliskais ID (obligāts).

#### Piemērs
```bash
digna inspection status 1024
```

#### Izvades piemērs
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Komanda `inspection abort` pieprasa atcelt notiekošos vai gaidošos pārbaudes pieprasījumus. Tā katram skartajam pieprasījumam reģistrē apturēšanas notikumu; pēc tā rīkojas aizmugursistēma, tāpēc pārtraukšana ir lūgums apstāties, nevis tūlītēja izbeigšana.

#### Komandas lietojums
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenti
- **INSPECTION_REQUEST_ID**: Pārtraucamā pārbaudes pieprasījuma ID. Obligāts, ja vien nav norādīts `--killall`.

#### Opcijas
- `--killall`: Pārtrauc visus pašlaik notiekošos un gaidošos pārbaudes pieprasījumus. Tai ir priekšroka pār līdzās norādītu pieprasījuma ID.

#### Piemērs
Lai pārtrauktu konkrētu pieprasījumu:
```bash
digna inspection abort 1024
```

Lai pārtrauktu visas aktīvās un rindā esošās pārbaudes:
```bash
digna inspection abort --killall
```

#### Izvades piemērs
`--killall` ziņo par paveikto; atsevišķa pieprasījuma pārtraukšana izvadi nerada un par sekmēm ziņo ar savu iziešanas kodu.
```text
All running and pending inspections have been aborted.
```

---

## Licenču pārvaldība

---

### license check

Komanda `license check` pārbauda failu `license.toml`, salīdzinot tā parakstu ar instalācijai pievienoto publisko atslēgu un pārliecinoties, ka tas nav beidzies. Tā nelasa nekādu lietojumprogrammas konfigurāciju, tāpēc darbojas arī pirms `config.toml` iestatīšanas.

#### Komandas lietojums
```bash
digna license check
```

#### Izvades piemērs
```text
License is valid
```

Par nederīgu parakstu un par beigušos licenci tiek ziņots kā par atsevišķām kļūdām, abos gadījumos ar iziešanas kodu 1.

---

## Servera un fona pakalpojumi

---

### serve

Komanda `serve` palaiž ***digna*** REST API serveri kopā ar fona pārbaužu plānotāju un pārbaužu pārvaldnieku. Startējot tā arī atzīmē par neizdevušos ikvienu pārbaudi, kuru repozitorijs joprojām reģistrē kā notiekošu, jo no agrāka procesa nekas nav varējis saglabāties.

Komanda darbojas priekšplānā, līdz tā tiek apturēta.

#### Komandas lietojums
```bash
digna serve [OPTIONS]
```

#### Opcijas
- `--address`: Tīkla adrese, kurai piesaistīt API serveri (noklusējums: `127.0.0.1`).
- `--port`: Porta numurs, kurā klausīties (noklusējums: `8000`).

#### Piemērs
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Izvades piemērs
```text
Server running on http://0.0.0.0:8000
```
