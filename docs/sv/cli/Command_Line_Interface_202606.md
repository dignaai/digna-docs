---
title: digna CLI-referens 2026.06 – Kommandon & exempel | digna Dokumentation
description: Fullständig referens för digna CLI-release 2026.06
image: /assets/logo_square.png
---

# digna CLI-referens 2026.06
**2026-09-05**

Den här sidan dokumenterar hela uppsättningen kommandon som finns i ***digna*** CLI-release **2026.06**, inklusive användningsexempel och alternativ.

Den körbara filen heter `digna`.

---

## CLI-grunder

---

### Översikt & syntax

CLI:t i release **2026.06** använder en strukturerad, kategoribaserad kommandohierarki:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` och `serve` är fristående kommandon utan underkommando:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globala alternativ

Följande globala alternativ gäller för samtliga kommandon:

- `--help`, `-h`: Visar hjälpinformation för CLI:t eller för en specifik kommandokategori eller ett underkommando.
- `--stacktrace`: Visar hela felkedjan vid fel i stället för enbart meddelandet på översta nivån.

`--stacktrace` är ett globalt alternativ i strikt mening: det måste anges **före** kommandokategorin, inte efter den.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Det finns ingen flagga `--version`. Använd kommandot [`version`](#version) i stället.

### Förutsättningar

De flesta kommandon behöver en läsbar, giltig `config.toml`; vissa kräver dessutom en giltig licens.
Följande tabell visar vad varje kommandokategori läser in innan den gör något över huvud taget:

| Kommandokategori | Behöver `config.toml` | Behöver giltig licens |
|---|---|---|
| `version` | nej | nej |
| `config check` | nej (det är just den kommandot rapporterar om) | nej |
| `license check` | nej | det *är* kontrollen |
| `crypt` | ja | nej |
| `serve` | ja | nej |
| `project` | ja | nej |
| `user` | ja | ja |
| `inspection` | ja | ja |
| `repo` | ja | ja |

Där en licens krävs kontrolleras både dess signatur och dess utgångsdatum, och kommandot avbryts innan det rör repositoryt om någon av dem underkänns.

### Slutkoder

- `0`: kommandot lyckades.
- `1`: kommandot misslyckades. Felmeddelandet skrivs till stderr, med prefixet `Error: `.

### help

Alternativet `--help` ger information om tillgängliga kommandokategorier, underkommandon och alternativ:

1. **Visa allmän hjälp:**
   ```bash
   digna --help
   ```

2. **Hämta hjälp för specifika kategorier och kommandon:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Utdata omfattar:**
   - **Kommandobeskrivning:** Sammanfattning av kommandots syfte.
   - **Syntax:** Obligatoriska och valfria argument.
   - **Alternativ:** Flaggor och parametrar som är specifika för kommandot.

### version

Kommandot `version` skriver ut den installerade ***digna***-releasen. Det läser ingen konfiguration och validerar ingen licens, så det fungerar även på en installation vars `config.toml` eller licens saknas eller är ogiltig.

Releaseversionen är oberoende av den version av repositoryschemat som rapporteras av [`repo check`](#repo-check).

#### Kommandoanvändning
```bash
digna version
```

#### Exempelutdata
```text
2026.06
```

---

## Konfigurationshantering

---

### config check

Kommandot `config check` validerar konfigurationsfilen (`config.toml`) och kontrollerar att alla obligatoriska sektioner och inställningar finns och är korrekt formaterade. Varje sektion valideras för sig, så att en trasig `[app]`-sektion inte döljer tillståndet för `[repo]`.

De sektioner som rapporteras är:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — valfri; en nyckel som saknas godkänns, medan en lista som finns men är felformad underkänns

Kommandot läser medvetet inte in applikationskonfigurationen på det sätt som de andra kommandona gör, så att det kan diagnostisera en `config.toml` som skulle hindra ***digna*** från att starta över huvud taget.

#### Kommandoanvändning
```bash
digna config check [OPTIONS]
```

#### Alternativ
- `--configpath`, `-c`: Sökväg till konfigurationsfilen, eller till en katalog som innehåller `config.toml` (standard är `./config.toml`).
- `--json`: Skriver ut valideringsrapporten som JSON. Har företräde framför `--quiet`.
- `--quiet`, `-q`: Undertrycker rapporten och förlitar sig enbart på slutkoden.

#### Exempel
```bash
digna config check
```

Validera en specifik konfigurationsfil och formatera utdata som JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Exempelutdata
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

En fil som saknas eller ett TOML-syntaxfel lämnar ingenting att validera sektion för sektion och rapporteras som ett enda fel i stället för som en rapport, oavsett `--quiet` eller `--json`.

---

## Repositoryhantering

---

### repo check

Kommandot `repo check` testar databasanslutningen och verifierar repositoryts installation och version. Det misslyckas om det konfigurerade schemat inte finns, eller om det finns men inte innehåller något ***digna***-repository.

Den version som rapporteras är versionen av repositoryschemat, som versionshanteras separat från den ***digna***-release som skrivs ut av [`version`](#version).

#### Kommandoanvändning
```bash
digna repo check
```

#### Exempelutdata
```text
Repo version 3.0.0 installed
```

### repo install

Kommandot `repo install` installerar ett nytt ***digna***-repository i det schema som konfigurerats i `config.toml` och skapar alla sekvenser, tabeller, index, villkor och initiala poster som krävs.

Själva schemat skapas **inte** av det här kommandot — det måste finnas i förväg. Kommandot vägrar också köra om ett repository redan är installerat i det schemat, och hänvisar till [`repo upgrade`](#repo-upgrade) om den installerade versionen är äldre.

#### Kommandoanvändning
```bash
digna repo install
```

#### Exempelutdata
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Kommandot `repo upgrade` tillämpar migreringar av databasschemat för att lyfta ett befintligt repository till den version som den installerade releasen förväntar sig. Uppgraderingar tillämpas ett versionssteg i taget längs en fast uppgraderingsväg, och varje avslutat steg registreras i repositoryt.

Om repositoryt redan har den förväntade versionen rapporterar kommandot att ingen uppgradering behövs och gör inga ändringar.

#### Kommandoanvändning
```bash
digna repo upgrade
```

#### Exempelutdata
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Krypteringshantering

---

### crypt gen-key

Kommandot `crypt gen-key` genererar en ny AES-GCM-krypteringsnyckel, avsedd att användas som krypteringsnyckel i `config.toml`. En läsbar `config.toml` måste redan finnas, även om den genererade nyckeln inte är beroende av den.

#### Kommandoanvändning
```bash
digna crypt gen-key
```

#### Exempelutdata
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Kommandot `crypt encrypt` krypterar en sträng (till exempel ett databaslösenord) med den AES-GCM-nyckel som konfigurerats i `config.toml` och skriver ut chiffertexten.

#### Kommandoanvändning
```bash
digna crypt encrypt <VALUE>
```

#### Argument
- **VALUE**: Klartextsträngen som ska krypteras (obligatoriskt).

#### Exempel
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Kommandot `crypt decrypt` dekrypterar en AES-GCM-krypterad sträng med den nyckel som konfigurerats i `config.toml` och skriver ut klartexten.

#### Kommandoanvändning
```bash
digna crypt decrypt <VALUE>
```

#### Argument
- **VALUE**: Den krypterade chiffertextsträng som ska dekrypteras (obligatoriskt).

#### Exempel
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Användarhantering

---

### user add

Kommandot `user add` skapar ett nytt användarkonto i ***digna***-repositoryt. Kommandot misslyckas om en användare med den angivna e-postadressen redan finns.

#### Kommandoanvändning
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argument
- **EMAIL**: Användarens e-postadress (obligatoriskt).
- **PASSWORD**: Användarens initiala lösenord (obligatoriskt).
- **DISPLAY_NAME**: Användarens fullständiga visningsnamn (obligatoriskt).

#### Alternativ
- `--admin`, `-a`: Skapar användaren med administratörsbehörighet (superanvändare).

#### Exempel
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Så här skapar du ett administratörskonto:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Exempelutdata
```text
User created with ID: 42
```

### user list

Kommandot `user list` listar alla registrerade användare i tabellform med ID, e-postadress, visningsnamn och administratörsflagga.

#### Kommandoanvändning
```bash
digna user list
```

#### Exempelutdata
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Kommandot `user modify` uppdaterar visningsnamn och administratörsbehörighet för ett befintligt användarkonto, identifierat via e-postadress.

Både visningsnamnet och administratörsflaggan skrivs alltid. `--admin` är en brytare, inte ett värde: **att utelämna den återkallar administratörsbehörigheten**, så ange den varje gång användaren ska behålla eller få den.

#### Kommandoanvändning
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argument
- **EMAIL**: E-postadressen för den användare som ska ändras (obligatoriskt).
- **DISPLAY_NAME**: Det uppdaterade visningsnamnet (obligatoriskt).

#### Alternativ
- `--admin`, `-a`: Ger administratörsbehörighet. Utelämna den för att återkalla den.
- `--valid-until`, `-v`: Accepteras av kompatibilitetsskäl men **tillämpas för närvarande inte**. Om den anges skrivs en varning ut och ingenting ändras.

#### Exempel
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Exempelutdata
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Kommandot `user modify-pwd` uppdaterar lösenordet för ett befintligt användarkonto.

#### Kommandoanvändning
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argument
- **EMAIL**: E-postadressen för den användare vars lösenord ska uppdateras (obligatoriskt).
- **PASSWORD**: Det nya lösenordet (obligatoriskt).

#### Exempel
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Kommandot `user delete` tar bort ett användarkonto från systemet.

#### Kommandoanvändning
```bash
digna user delete <EMAIL>
```

#### Argument
- **EMAIL**: E-postadressen för den användare som ska tas bort (obligatoriskt).

#### Exempel
```bash
digna user delete jdoe@example.com
```

---

## Projekt- och datakällhantering

---

### project list

Kommandot `project list` listar alla tillgängliga projekt i repositoryt och visar deras ID, namn och beskrivning.

#### Kommandoanvändning
```bash
digna project list
```

#### Exempelutdata
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Kommandot `project list-ds` listar alla datakällor som hör till ett visst projekt och visar deras ID, namn, typ, schema och tabellnamn.

#### Kommandoanvändning
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argument
- **PROJECT_NAME**: Namnet på det projekt vars datakällor ska listas (obligatoriskt). Namnet måste stämma exakt.

#### Exempel
```bash
digna project list-ds ProjectA
```

#### Exempelutdata
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Kommandot `project export-ds` exporterar datakällor från ett projekt till ett JSON-dokument.

Om varken `--table-name` eller `--table-id` anges exporteras alla datakällor i projektet.

#### Kommandoanvändning
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argument
- **PROJECT_NAME**: Namnet på det projekt vars datakällor ska exporteras (obligatoriskt).

#### Alternativ
- `--table-name`, `-n`: Namn på de datakällor som ska exporteras. Flera namn kan anges åtskilda med mellanslag.
- `--table-id`, `-i`: ID:n för de datakällor som ska exporteras. Flera ID:n kan anges åtskilda med mellanslag.
- `--exportfile`, `-f`: Sökväg där de exporterade datakällorna ska sparas (standard: `data_sources_export.json`).

#### Exempel
Så här exporterar du alla datakällor från `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Så här exporterar du specifika tabeller:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Exempelutdata
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Kommandot `project import-ds` importerar datakällor från en exportfil till ett målprojekt och rapporterar per objekt vad som skapades, uppdaterades eller hoppades över.

#### Kommandoanvändning
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argument
- **PROJECT_NAME**: Namnet på det målprojekt som ska importeras till (obligatoriskt).
- **EXPORT_FILE**: Sökväg till JSON-exportfilen (obligatoriskt).

#### Alternativ
- `--output-file`, `-o`: Fil att skriva importrapporten till. Utan den går rapporten till stdout.
- `--output-format`, `-f`: Format på importrapporten — `table`, `json` eller `csv` (standard: `table`).

#### Exempel
```bash
digna project import-ds ProjectB my_export.json
```

Så här fångar du en maskinläsbar rapport:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Rapporten täcker fyra objektnivåer — datakälla, datamängdsdefinition, attribut och valideringsregel — var och en med sin importåtgärd, sitt resultat, det resulterande objektets ID och eventuell ytterligare information.

### project plan-import-ds

Kommandot `project plan-import-ds` förhandsvisar en import av datakällor till ett målprojekt och visar vilka objekt som skulle skapas, uppdateras eller hoppas över, utan att ändra någonting. Det tar samma exportfil och samma rapportalternativ som [`project import-ds`](#project-import-ds), och lägger till ett stegnummer per planerat objekt.

#### Kommandoanvändning
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argument
- **PROJECT_NAME**: Namnet på målprojektet (obligatoriskt).
- **EXPORT_FILE**: Sökväg till exportfilen (obligatoriskt).

#### Alternativ
- `--output-file`, `-o`: Fil att skriva importplanen till. Utan den går planen till stdout.
- `--output-format`, `-f`: Format på importplanen — `table`, `json` eller `csv` (standard: `table`).

#### Exempel
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Inspektionshantering

---

### inspection run

Kommandot `inspection run` skapar en inspektionsbegäran för ett projekt och ett datumintervall och — beroende på vilka alternativ som anges — antingen väntar på den, återvänder omedelbart eller kör den i den egna processen.

De tre körlägena är:

- **Standard (ingen flagga)**: begäran köas för backend, och CLI:t pollar den varannan sekund och skriver ut uppgifternas förlopp tills inspektionen når ett sluttillstånd. Ett körande `digna serve` krävs, annars är det ingenting som plockar upp begäran.
- **`--async-mode`**: begäran köas och dess ID skrivs ut omedelbart. Använd [`inspection status`](#inspection-status) för att följa den.
- **`--bypass-backend`**: inspektionen körs av CLI-processen själv och köas inte, så ingen körande server behövs.

`--async-mode` och `--bypass-backend` utesluter varandra.

I samtliga lägen avslutas kommandot med en slutkod som inte är noll om inspektionen inte slutfördes utan fel.

#### Kommandoanvändning
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argument
- **PROJECT_NAME**: Namnet på målprojektet (obligatoriskt). Namnet måste stämma exakt.
- **START_DATE**: Startdatum för datumintervallet i formatet `YYYY-MM-DD` (obligatoriskt).
- **END_DATE**: Slutdatum för datumintervallet i formatet `YYYY-MM-DD` (obligatoriskt).

#### Alternativ
- `--table-name`: Begränsar inspektionen till en enda datakälla i projektet, angiven med datakällans namn. Utan den inspekteras alla datakällor i projektet.
- `--async-mode`: Köar inspektionen och skriver ut begärans ID i stället för att vänta på den. Kan inte kombineras med `--bypass-backend`.
- `--bypass-backend`: Kör inspektionen direkt i CLI-processen i stället för att köa den för backend. Kan inte kombineras med `--async-mode`.

#### Exempel
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Så här skickar du en asynkron inspektion:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Så här inspekterar du en enda datakälla:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Exempelutdata
Standardläge:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynkront läge:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Kommandot `inspection status` frågar efter tillstånd och uppgiftsförlopp för en inspektionsbegäran med hjälp av dess begäran-ID.

#### Kommandoanvändning
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argument
- **INSPECTION_REQUEST_ID**: Det numeriska ID:t för inspektionsbegäran (obligatoriskt).

#### Exempel
```bash
digna inspection status 1024
```

#### Exempelutdata
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Kommandot `inspection abort` begär att körande eller väntande inspektionsbegäranden avbryts. Det registrerar en stopphändelse för varje berörd begäran; det är backend som agerar på den, så ett avbrott är en begäran om att stoppa snarare än ett omedelbart avslut.

#### Kommandoanvändning
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argument
- **INSPECTION_REQUEST_ID**: ID:t för den inspektionsbegäran som ska avbrytas. Obligatoriskt om inte `--killall` anges.

#### Alternativ
- `--killall`: Avbryter alla inspektionsbegäranden som körs eller väntar. Har företräde framför ett begäran-ID som anges tillsammans med den.

#### Exempel
Så här avbryter du en specifik begäran:
```bash
digna inspection abort 1024
```

Så här avbryter du alla aktiva och köade inspektioner:
```bash
digna inspection abort --killall
```

#### Exempelutdata
`--killall` rapporterar vad den gjorde; att avbryta en enskild begäran ger ingen utdata och signalerar att det gick bra via slutkoden.
```text
All running and pending inspections have been aborted.
```

---

## Licenshantering

---

### license check

Kommandot `license check` validerar `license.toml` genom att verifiera dess signatur mot den publika nyckel som följer med installationen och kontrollera att den inte har gått ut. Det läser ingen applikationskonfiguration, så det fungerar även innan `config.toml` är uppsatt.

#### Kommandoanvändning
```bash
digna license check
```

#### Exempelutdata
```text
License is valid
```

En ogiltig signatur och en utgången licens rapporteras som två skilda fel, båda med slutkod 1.

---

## Server & bakgrundstjänster

---

### serve

Kommandot `serve` startar ***digna*** REST API-servern tillsammans med schemaläggaren för inspektioner och inspektionshanteraren som körs i bakgrunden. Vid uppstart markerar det också varje inspektion som repositoryt fortfarande registrerar som körande som misslyckad, eftersom ingenting kan ha överlevt från en tidigare process.

Kommandot körs i förgrunden tills det stoppas.

#### Kommandoanvändning
```bash
digna serve [OPTIONS]
```

#### Alternativ
- `--address`: Nätverksadress som API-servern ska bindas till (standard: `127.0.0.1`).
- `--port`: Portnummer att lyssna på (standard: `8000`).

#### Exempel
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Exempelutdata
```text
Server running on http://0.0.0.0:8000
```
