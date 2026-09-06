# digna CLI-reference 2026.06
**2026-09-05**

Denne side dokumenterer det fulde sæt kommandoer, der er tilgængelige i ***digna*** CLI-udgivelse **2026.06**, inklusive anvendelseseksempler og indstillinger.

Den eksekverbare fil hedder `digna`.

---

## CLI-grundbegreber

---

### Overblik og syntaks

CLI'en i udgivelse **2026.06** anvender et struktureret, kategoribaseret kommandohierarki:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` og `serve` er enkeltstående kommandoer uden underkommando:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Globale indstillinger

Følgende globale indstillinger gælder for alle kommandoer:

- `--help`, `-h`: Viser hjælpeoplysninger for CLI'en eller for en bestemt kommandokategori eller underkommando.
- `--stacktrace`: Viser hele fejlkæden ved fejl i stedet for kun beskeden på øverste niveau.

`--stacktrace` er en global indstilling i streng forstand: den skal angives **før** kommandokategorien, ikke efter.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Der findes intet `--version`-flag. Brug kommandoen [`version`](#version) i stedet.

### Forudsætninger

De fleste kommandoer kræver en læsbar, gyldig `config.toml`; nogle kræver desuden en gyldig licens.
Følgende tabel viser, hvad hver kommandokategori indlæser, før den foretager sig noget:

| Kommandokategori | Kræver `config.toml` | Kræver en gyldig licens |
|---|---|---|
| `version` | nej | nej |
| `config check` | nej (det er netop dét, kommandoen rapporterer om) | nej |
| `license check` | nej | den *er* kontrollen |
| `crypt` | ja | nej |
| `serve` | ja | nej |
| `project` | ja | nej |
| `user` | ja | ja |
| `inspection` | ja | ja |
| `repo` | ja | ja |

Hvor en licens er påkrævet, kontrolleres både dens signatur og dens udløbsdato, og kommandoen afbrydes, før den rører ved repositoriet, hvis en af delene fejler.

### Afslutningskoder

- `0`: kommandoen lykkedes.
- `1`: kommandoen mislykkedes. Fejlmeddelelsen skrives til stderr med præfikset `Error: `.

### help

Indstillingen `--help` giver oplysninger om tilgængelige kommandokategorier, underkommandoer og indstillinger:

1. **Visning af generel hjælp:**
   ```bash
   digna --help
   ```

2. **Hjælp til bestemte kategorier og kommandoer:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Output omfatter:**
   - **Kommandobeskrivelse:** Resumé af kommandoens formål.
   - **Syntaks:** Påkrævede og valgfrie argumenter.
   - **Indstillinger:** Flag og parametre, der er specifikke for kommandoen.

### version

Kommandoen `version` udskriver den installerede ***digna***-udgivelse. Den læser ingen konfiguration og validerer ingen licens, så den virker også på en installation, hvor `config.toml` eller licensen mangler eller er ugyldig.

Udgivelsesversionen er uafhængig af den repositorieskemaversion, som [`repo check`](#repo-check) rapporterer.

#### Kommandoanvendelse
```bash
digna version
```

#### Eksempeloutput
```text
2026.06
```

---

## Konfigurationsstyring

---

### config check

Kommandoen `config check` validerer konfigurationsfilen (`config.toml`) og kontrollerer, at alle obligatoriske sektioner og indstillinger er til stede og korrekt formateret. Hver sektion valideres for sig, så en defekt `[app]`-sektion ikke skjuler tilstanden af `[repo]`.

De rapporterede sektioner er:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — valgfri; en manglende nøgle består, mens en tilstedeværende, men fejlformateret liste fejler

Kommandoen indlæser bevidst ikke applikationskonfigurationen på samme måde som de øvrige kommandoer, så den kan diagnosticere en `config.toml`, der ville forhindre ***digna*** i overhovedet at starte.

#### Kommandoanvendelse
```bash
digna config check [OPTIONS]
```

#### Indstillinger
- `--configpath`, `-c`: Sti til konfigurationsfilen eller til en mappe, der indeholder `config.toml` (standard `./config.toml`).
- `--json`: Udskriver valideringsrapporten som JSON. Har forrang for `--quiet`.
- `--quiet`, `-q`: Undertrykker rapporten og forlader sig udelukkende på afslutningskoden.

#### Eksempel
```bash
digna config check
```

Validér en bestemt konfigurationsfil, og formatér output som JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Eksempeloutput
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

En manglende fil eller en TOML-syntaksfejl efterlader intet at validere sektion for sektion og rapporteres som én enkelt fejl i stedet for en rapport, uanset `--quiet` eller `--json`.

---

## Repositoriestyring

---

### repo check

Kommandoen `repo check` tester databaseforbindelsen og verificerer repositoriets installation og version. Den fejler, hvis det konfigurerede skema ikke findes, eller hvis det findes, men ikke indeholder noget ***digna***-repositorie.

Den rapporterede version er versionen af repositorieskemaet, som versioneres uafhængigt af den ***digna***-udgivelse, [`version`](#version) udskriver.

#### Kommandoanvendelse
```bash
digna repo check
```

#### Eksempeloutput
```text
Repo version 3.0.0 installed
```

### repo install

Kommandoen `repo install` installerer et nyt ***digna***-repositorie i det skema, der er konfigureret i `config.toml`, og opretter alle nødvendige sekvenser, tabeller, indeks, begrænsninger og indledende poster.

Selve skemaet oprettes **ikke** af denne kommando — det skal findes på forhånd. Kommandoen nægter desuden at køre, hvis der allerede er installeret et repositorie i det pågældende skema, og henviser til [`repo upgrade`](#repo-upgrade), hvis den installerede version er ældre.

#### Kommandoanvendelse
```bash
digna repo install
```

#### Eksempeloutput
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Kommandoen `repo upgrade` anvender databaseskemamigreringer for at bringe et eksisterende repositorie op på den version, den installerede udgivelse forventer. Opgraderinger anvendes ét versionsspring ad gangen langs en fast opgraderingssti, og hvert gennemført spring registreres i repositoriet.

Hvis repositoriet allerede er på den forventede version, rapporterer kommandoen, at ingen opgradering er nødvendig, og foretager ingen ændringer.

#### Kommandoanvendelse
```bash
digna repo upgrade
```

#### Eksempeloutput
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Krypteringsstyring

---

### crypt gen-key

Kommandoen `crypt gen-key` genererer en ny AES-GCM-krypteringsnøgle til brug som krypteringsnøgle i `config.toml`. En indlæsbar `config.toml` skal allerede være til stede, selvom den genererede nøgle ikke afhænger af den.

#### Kommandoanvendelse
```bash
digna crypt gen-key
```

#### Eksempeloutput
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Kommandoen `crypt encrypt` krypterer en streng (for eksempel en databaseadgangskode) med den AES-GCM-nøgle, der er konfigureret i `config.toml`, og udskriver den krypterede tekst.

#### Kommandoanvendelse
```bash
digna crypt encrypt <VALUE>
```

#### Argumenter
- **VALUE**: Klarteksten, der skal krypteres (påkrævet).

#### Eksempel
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Kommandoen `crypt decrypt` dekrypterer en AES-GCM-krypteret streng med den nøgle, der er konfigureret i `config.toml`, og udskriver klarteksten.

#### Kommandoanvendelse
```bash
digna crypt decrypt <VALUE>
```

#### Argumenter
- **VALUE**: Den krypterede tekststreng, der skal dekrypteres (påkrævet).

#### Eksempel
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Brugerstyring

---

### user add

Kommandoen `user add` opretter en ny brugerkonto i ***digna***-repositoriet. Kommandoen fejler, hvis der allerede findes en bruger med den angivne e-mailadresse.

#### Kommandoanvendelse
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenter
- **EMAIL**: Brugerens e-mailadresse (påkrævet).
- **PASSWORD**: Brugerens indledende adgangskode (påkrævet).
- **DISPLAY_NAME**: Brugerens fulde visningsnavn (påkrævet).

#### Indstillinger
- `--admin`, `-a`: Opretter brugeren med administratorrettigheder (superbruger).

#### Eksempel
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Sådan oprettes en administratorkonto:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Eksempeloutput
```text
User created with ID: 42
```

### user list

Kommandoen `user list` viser alle registrerede brugere i tabelform med ID, e-mail, visningsnavn og administratorflag.

#### Kommandoanvendelse
```bash
digna user list
```

#### Eksempeloutput
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Kommandoen `user modify` opdaterer visningsnavn og administratorrettigheder for en eksisterende brugerkonto, der identificeres ved e-mailadresse.

Både visningsnavnet og administratorflaget skrives altid. `--admin` er en kontakt, ikke en værdi: **udelades den, fratages administratorrettighederne**, så angiv den, hver gang brugeren skal beholde eller opnå dem.

#### Kommandoanvendelse
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenter
- **EMAIL**: E-mailadressen på den bruger, der skal ændres (påkrævet).
- **DISPLAY_NAME**: Det opdaterede visningsnavn (påkrævet).

#### Indstillinger
- `--admin`, `-a`: Tildeler administratorrettigheder. Udelad for at fratage dem.
- `--valid-until`, `-v`: Accepteres af hensyn til kompatibilitet, men **anvendes ikke i øjeblikket**. Angives den, udskrives en advarsel, og intet ændres.

#### Eksempel
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Eksempeloutput
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Kommandoen `user modify-pwd` opdaterer adgangskoden for en eksisterende brugerkonto.

#### Kommandoanvendelse
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenter
- **EMAIL**: E-mailadressen på den bruger, hvis adgangskode skal opdateres (påkrævet).
- **PASSWORD**: Den nye adgangskode (påkrævet).

#### Eksempel
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Kommandoen `user delete` fjerner en brugerkonto fra systemet.

#### Kommandoanvendelse
```bash
digna user delete <EMAIL>
```

#### Argumenter
- **EMAIL**: E-mailadressen på den bruger, der skal slettes (påkrævet).

#### Eksempel
```bash
digna user delete jdoe@example.com
```

---

## Projekt- og datakildestyring

---

### project list

Kommandoen `project list` viser alle tilgængelige projekter i repositoriet med deres ID, navn og beskrivelse.

#### Kommandoanvendelse
```bash
digna project list
```

#### Eksempeloutput
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Kommandoen `project list-ds` viser alle datakilder, der er knyttet til et givent projekt, med deres ID, navn, type, skema og tabelnavn.

#### Kommandoanvendelse
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvis datakilder skal vises (påkrævet). Navnet skal matche præcist.

#### Eksempel
```bash
digna project list-ds ProjectA
```

#### Eksempeloutput
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Kommandoen `project export-ds` eksporterer datakilder fra et projekt til et JSON-dokument.

Angives hverken `--table-name` eller `--table-id`, eksporteres alle projektets datakilder.

#### Kommandoanvendelse
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, datakilderne skal eksporteres fra (påkrævet).

#### Indstillinger
- `--table-name`, `-n`: Navne på de datakilder, der skal eksporteres. Flere navne kan angives adskilt af mellemrum.
- `--table-id`, `-i`: ID'er på de datakilder, der skal eksporteres. Flere ID'er kan angives adskilt af mellemrum.
- `--exportfile`, `-f`: Sti, hvor de eksporterede datakilder gemmes (standard: `data_sources_export.json`).

#### Eksempel
Sådan eksporteres alle datakilder fra `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Sådan eksporteres bestemte tabeller:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Eksempeloutput
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Kommandoen `project import-ds` importerer datakilder fra en eksportfil til et målprojekt og rapporterer for hvert objekt, hvad der blev oprettet, opdateret eller sprunget over.

#### Kommandoanvendelse
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det målprojekt, der importeres til (påkrævet).
- **EXPORT_FILE**: Sti til JSON-eksportfilen (påkrævet).

#### Indstillinger
- `--output-file`, `-o`: Fil, importrapporten skrives til. Uden den går rapporten til stdout.
- `--output-format`, `-f`: Importrapportens format — `table`, `json` eller `csv` (standard: `table`).

#### Eksempel
```bash
digna project import-ds ProjectB my_export.json
```

Sådan opsamles en maskinlæsbar rapport:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Rapporten dækker fire objektniveauer — datakilde, datasætdefinition, attribut og valideringsregel — hvert med sin importhandling, sit resultat, det resulterende objekt-ID og eventuelle yderligere oplysninger.

### project plan-import-ds

Kommandoen `project plan-import-ds` viser en forhåndsvisning af en datakildeimport til et målprojekt og angiver, hvilke objekter der ville blive oprettet, opdateret eller sprunget over, uden at ændre noget. Den tager den samme eksportfil og de samme rapporteringsindstillinger som [`project import-ds`](#project-import-ds) og tilføjer et trinnummer pr. planlagt objekt.

#### Kommandoanvendelse
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på målprojektet (påkrævet).
- **EXPORT_FILE**: Sti til eksportfilen (påkrævet).

#### Indstillinger
- `--output-file`, `-o`: Fil, importplanen skrives til. Uden den går planen til stdout.
- `--output-format`, `-f`: Importplanens format — `table`, `json` eller `csv` (standard: `table`).

#### Eksempel
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Inspektionsstyring

---

### inspection run

Kommandoen `inspection run` opretter en inspektionsanmodning for et projekt og et datointerval og — afhængigt af de angivne indstillinger — venter derefter på den, vender straks tilbage eller kører den i sin egen proces.

De tre udførelsestilstande er:

- **Standard (uden flag)**: anmodningen sættes i kø til backend'en, og CLI'en forespørger den hvert andet sekund og udskriver opgavernes fremdrift, indtil inspektionen når en sluttilstand. En kørende `digna serve` er påkrævet, ellers samler ingen anmodningen op.
- **`--async-mode`**: anmodningen sættes i kø, og dens ID udskrives med det samme. Brug [`inspection status`](#inspection-status) til at følge den.
- **`--bypass-backend`**: inspektionen udføres af selve CLI-processen og sættes ikke i kø, så der kræves ingen kørende server.

`--async-mode` og `--bypass-backend` udelukker hinanden.

I alle tilstande afsluttes kommandoen med en afslutningskode forskellig fra nul, hvis inspektionen ikke blev fuldført korrekt.

#### Kommandoanvendelse
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på målprojektet (påkrævet). Navnet skal matche præcist.
- **START_DATE**: Startdato for datointervallet i formatet `YYYY-MM-DD` (påkrævet).
- **END_DATE**: Slutdato for datointervallet i formatet `YYYY-MM-DD` (påkrævet).

#### Indstillinger
- `--table-name`: Begrænser inspektionen til en enkelt af projektets datakilder, angivet ved dens datakildenavn. Uden den inspiceres alle projektets datakilder.
- `--async-mode`: Sætter inspektionen i kø og udskriver anmodnings-ID'et i stedet for at vente på den. Kan ikke kombineres med `--bypass-backend`.
- `--bypass-backend`: Kører inspektionen direkte i CLI-processen i stedet for at sætte den i kø til backend'en. Kan ikke kombineres med `--async-mode`.

#### Eksempel
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Sådan indsendes en asynkron inspektion:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Sådan inspiceres en enkelt datakilde:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Eksempeloutput
Standardtilstand:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Asynkron tilstand:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Kommandoen `inspection status` forespørger på tilstanden og opgavefremdriften for en inspektionsanmodning ud fra dens anmodnings-ID.

#### Kommandoanvendelse
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenter
- **INSPECTION_REQUEST_ID**: Det numeriske ID for inspektionsanmodningen (påkrævet).

#### Eksempel
```bash
digna inspection status 1024
```

#### Eksempeloutput
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Kommandoen `inspection abort` anmoder om annullering af kørende eller ventende inspektionsanmodninger. Den registrerer en stophændelse for hver berørt anmodning; backend'en handler på den, så en afbrydelse er en anmodning om at standse frem for en øjeblikkelig nedlukning.

#### Kommandoanvendelse
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenter
- **INSPECTION_REQUEST_ID**: ID'et på den inspektionsanmodning, der skal afbrydes. Påkrævet, medmindre `--killall` angives.

#### Indstillinger
- `--killall`: Afbryder alle aktuelt kørende og ventende inspektionsanmodninger. Har forrang for et anmodnings-ID, der angives sammen med den.

#### Eksempel
Sådan afbrydes en bestemt anmodning:
```bash
digna inspection abort 1024
```

Sådan afbrydes alle aktive og køsatte inspektioner:
```bash
digna inspection abort --killall
```

#### Eksempeloutput
`--killall` rapporterer, hvad den gjorde; afbrydelse af en enkelt anmodning giver intet output og melder om succes via sin afslutningskode.
```text
All running and pending inspections have been aborted.
```

---

## Licensstyring

---

### license check

Kommandoen `license check` validerer `license.toml`, verificerer dens signatur mod den offentlige nøgle, der leveres med installationen, og kontrollerer, at den ikke er udløbet. Den læser ingen applikationskonfiguration og virker derfor også, før `config.toml` er sat op.

#### Kommandoanvendelse
```bash
digna license check
```

#### Eksempeloutput
```text
License is valid
```

En ugyldig signatur og en udløbet licens rapporteres som to forskellige fejl, begge med afslutningskode 1.

---

## Server- og baggrundstjenester

---

### serve

Kommandoen `serve` starter ***digna***-REST-API-serveren sammen med baggrundsinspektionsplanlæggeren og inspektionsmanageren. Ved opstart lader den desuden enhver inspektion, som repositoriet stadig registrerer som kørende, fejle, eftersom intet kan have overlevet fra en tidligere proces.

Kommandoen kører i forgrunden, indtil den stoppes.

#### Kommandoanvendelse
```bash
digna serve [OPTIONS]
```

#### Indstillinger
- `--address`: Netværksadresse, API-serveren skal bindes til (standard: `127.0.0.1`).
- `--port`: Portnummer, der lyttes på (standard: `8000`).

#### Eksempel
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Eksempeloutput
```text
Server running on http://0.0.0.0:8000
```