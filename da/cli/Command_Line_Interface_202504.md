# digna CLI Reference 2025.04
**2025-04-01**

Denne side dokumenterer det fulde sæt af kommandoer, der er tilgængelige i ***digna*** CLI-udgivelsen **2025.04**, inklusive brugs-eksempler og muligheder.

---

## CLI Basics

---

## Brug af `help`-optionen

Optionen `--help` giver information om tilgængelige kommandoer og deres brug. Der er to hovedmåder at bruge denne option på:

1. **Visning af generel hjælp:**
   
    Brug --help umiddelbart efter nøgleordet `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Hjælp for specifikke kommandoer:**  
  
    For detaljeret information om en specifik kommando, tilføj `--help` til den pågældende kommando.  
    For eksempel, for at få hjælp til kommandoen `add-user`, kør:
     ```bash
     dignacli add-user --help
     ```

     ### Output:
      
     - **Command Description:** Giver en detaljeret beskrivelse af, hvad kommandoen gør.  
     - **Syntax:** Viser den nøjagtige syntaks, inklusive krævede og valgfrie argumenter.  
     - **Options:** Liste over eventuelle options specifikke for kommandoen, sammen med deres forklaringer.  
     - **Examples:** Giver eksempler på, hvordan kommandoen kan køres effektivt.

  
## Brug af `check-repo-connection`-kommandoen

Kommandoen check-repo-connection er et værktøj i ***digna*** CLI, der er designet til at teste forbindelsen og adgangen til et specificeret ***digna*** repository. Denne kommando sikrer, at CLI'en kan interagere med repositoryet.
      
#### Kommando brug
```bash
dignacli check-repo-connection
```

Ved vellykket udførelse vil kommandoen vise en bekræftelse af forbindelsen samt detaljer om repositoryet: Repository version, Host, Database og Schema.  
  
Hvis repository-forbindelsen ikke er vellykket, tjek konfigurationsfilen config.toml for korrekte indstillinger.

## Brug af `version`-kommandoen

For at tjekke den installerede version af *dignacli*, brug optionen --version.  
  
#### Kommando brug
```bash
dignacli --version
```
  
#### Eksempel output
```bash
dignacli version 2025.04
```

## Brug af lognings-optioner
  
Som standard er konsoloutputtet fra ***digna***-kommandoerne designet til at være minimalistisk. De fleste kommandoer tilbyder muligheden for at give yderligere information ved at bruge følgende options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” og ”debug” definerer detaljeringsgraden, mens ”logfile”-skiftet tillader at omdirigere outputtet til en fil i stedet for konsolvinduet.

## Brugeradministration

### Brug af `add-user`-kommandoen
  
Kommandoen add-user i ***digna*** CLI bruges til at tilføje en ny bruger til ***digna*** systemet.
  
#### Kommando brug
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenter

- **USER_NAME**: Brugernavnet for den nye bruger (påkrævet).
- **USER_FULL_NAME**: Den nye brugers fulde navn (påkrævet).
- **USER_PASSWORD**: Passwordet for den nye bruger (påkrævet).

#### Options

- `--is_superuser`, `-su`: Flag for at udpege den nye bruger som administrator.
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerens konto i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke sat, har kontoen ingen udløbsdato.

#### Eksempel

For at tilføje en ny bruger med brugernavnet `jdoe`, fulde navn `John Doe` og password `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For at tilføje en ny bruger og sætte en udløbsdato for kontoen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Brug af `delete-user`-kommandoen
  
Kommandoen `delete-user` i ***digna*** CLI bruges til at fjerne en eksisterende bruger fra ***digna*** systemet.
  
#### Kommando brug
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenter
- **USER_NAME**: Brugernavnet for den bruger, der skal slettes (påkrævet). Dette er det eneste argument, som kommandoen kræver.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Udførelse af denne kommando vil fjerne brugeren `jdoe` fra ***digna*** systemet, inddrage deres adgang og slette deres tilknyttede data og rettigheder fra repositoryet.

### Brug af `modify-user`-kommandoen

Kommandoen `modify-user` i ***digna*** CLI bruges til at opdatere oplysningerne for en eksisterende bruger i ***digna*** systemet.

#### Kommando brug
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenter
  
- **USER_NAME**: Brugernavnet for den bruger, der skal ændres (påkrævet).
- **USER_FULL_NAME**: Det nye fulde navn for brugeren (påkrævet).
  
#### Options  
  
- `--is_superuser`, `-su`: Sætter brugeren som superuser og giver forhøjede rettigheder. Dette flag kræver ikke en værdi.  
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerens konto i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angivet, forbliver kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For at ændre fulde navn for brugeren `jdoe` til ”Johnathan Doe” og sætte brugeren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Brug af `modify-user-pwd`-kommandoen
  
Kommandoen `modify-user-pwd` i ***digna*** CLI bruges til at ændre passwordet for en eksisterende bruger i ***digna*** systemet.
  
#### Kommando brug
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenter
  
- **USER_NAME**: Brugernavnet for den bruger, hvis password skal ændres (påkrævet).
- **USER_PWD**: Det nye password for brugeren (påkrævet).
  
#### Eksempel
  
For at ændre passwordet for brugeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Brug af `list-users`-kommandoen

Kommandoen `list-users` i ***digna*** CLI viser en liste over alle brugere registreret i ***digna*** systemet.

#### Kommando brug

```bash
dignacli list-users
```

Udførelse af denne kommando i ***digna*** CLI vil forbinde til ***digna*** repositoryet og liste alle brugere, vise deres ID, brugernavn, fulde navn, superuser-status og udløbstidspunkter.

## Repository-administration

### Brug af `upgrade-repo`-kommandoen
  
Kommandoen `upgrade-repo` i ***digna*** CLI bruges til at opgradere eller initialisere ***digna*** repositoryet. Denne kommando er essentiel for at anvende opdateringer eller opsætte repository-infrastrukturen for første gang.
  
#### Kommando brug

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Når aktiveret kører denne option kommandoen i simulerings-tilstand, hvilket udskriver de SQL-udtryk, der ville blive kørt, men udfører dem ikke. Dette er nyttigt til at få en forhåndsvisning af ændringer uden at foretage nogen modifikationer i repositoryet.  

  
#### Eksempel
  
For at opgradere ***digna*** repositoryet kan du køre kommandoen uden nogen options:
  
```bash
dignacli upgrade-repo
```  
For at køre opgraderingen i simulerings-tilstand (for at se SQL-udtryk uden at anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommando er afgørende for vedligeholdelse af ***digna*** systemet og sikrer, at databaseskemaet og andre repository-komponenter er opdaterede i forhold til den nyeste softwareversion.

### Brug af `encrypt`-kommandoen
  
Kommandoen `encrypt` i ***digna*** CLI bruges til at kryptere et password.
  
#### Kommando brug
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenter
- **PASSWORD**: Det password, der skal krypteres (påkrævet).
  
#### Eksempel
  
For at kryptere et password skal du angive passwordet som et argument.   
For eksempel, for at kryptere passwordet `mypassword123`, ville du bruge:
```bash
dignacli encrypt mypassword123
```
Denne kommando returnerer den krypterede version af det angivne password, som derefter kan anvendes i sikre sammenhænge. Hvis password-argumentet ikke er angivet, vil CLI'en vise en fejl, der angiver det manglende argument.

## Brug af `generate-key`-kommandoen
  
Kommandoen `generate-key` bruges til at generere en Fernet-nøgle, som er essentiel til at sikre passwords, der gemmes i ***digna*** repositoryet.
  
#### Kommando brug
```bash
dignacli generate-key
```
  
## Datahåndtering

## Brug af `clean-up`-kommandoen

Kommandoen `clean-up` i ***digna*** CLI bruges til at fjerne profiler, predictioner og Traffic Light System-data for en eller flere datakilder inden for et specificeret projekt. Denne kommando er vigtig for data-lifecycle management og hjælper med at holde et organiseret og effektivt data-miljø ved at rydde forældede eller unødvendige data.

#### Kommando brug

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, hvorfra data skal fjernes (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdatoen og -tidspunktet for datafjernelsen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdatoen og -tidspunktet for datafjernelsen, med samme formater som FROM_DATE (påkrævet).
  
#### Options
  
- `--table-name`, `-tn`: Begrænser clean-up-operationen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filtre til at begrænse clean-up til tabeller, der indeholder den angivne substring i deres navne.
- `--timing`, `-tm`: Viser tidsforbruget for clean-up-processen efter færdiggørelse.
- `--help`: Viser hjælpeinformation for clean-up-kommandoen og afslutter.
  
#### Eksempel
  
For at fjerne data fra projektet ProjectA mellem 1. januar 2023 og 30. juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
For kun at fjerne data fra en specifik tabel ved navn `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Denne kommando hjælper med at styre datalagring og sikrer, at repositoryet kun indeholder relevant information.

## Brug af `list-projects`-kommandoen
  
Kommandoen `list-projects` i ***digna*** CLI bruges til at vise en liste over alle tilgængelige projekter i ***digna*** systemet.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

Denne kommando er især nyttig for administratorer og brugere, der administrerer flere projekter, da den giver et hurtigt overblik over de tilgængelige projekter i ***digna*** repositoryet.

## Brug af `list-ds`-kommandoen

Kommandoen `list-ds` i ***digna*** CLI bruges til at vise en liste over alle tilgængelige datakilder inden for et specificeret projekt. Denne kommando er nyttig for at få overblik over de dataressourcer, der er tilgængelige for analyse og administration i ***digna*** systemet.

#### Kommando brug
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, som datakilderne listes for (påkrævet).
  
#### Eksempel
  
For at liste alle datakilder i projektet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommando giver brugerne et overblik over de datakilder, der er tilgængelige i et projekt, og hjælper dem med at navigere og administrere datalandskabet mere effektivt.


## Brug af `inspect`-kommandoen

Kommandoen `inspect` i ***digna*** CLI bruges til at oprette profiler, predictioner og Traffic Light System-data for en eller flere datakilder inden for et specificeret projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode.

#### Kommando brug

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, som data skal inspiceres for (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdatoen og -tidspunktet for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdatoen og -tidspunktet for datainspektionen, med samme formater som FROM_DATE (påkrævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel i projektet.
- `--table-filter`, `-tf`: Filtre til kun at inspicere tabeller, der indeholder den angivne substring i deres navne.
- `--do-profile`: Trigger genindsamling af profiler. Standard er do-profile.
- `--no-do-profile`: Forhindrer genindsamling af profiler.
- `--do-prediction`: Trigger genberegning af predictioner. Standard er do-prediction.
- `--no-do-prediction`: Forhindrer genberegning af predictioner.
- `--do-alert-status`: Trigger genberegning af alarmstatusser. Standard er do-alert-status.
- `--no-do-alert-status`: Forhindrer genberegning af alarmstatusser.
- `--iterative`: Trigger inspektion af en periode ved hjælp af daglige iterationer. Standard er iterative.
- `--no-iterative`: Trigger inspektion af hele perioden på én gang.
- `--enable_notification`, `-en`: Aktiverer afsendelse af notifikationer i tilfælde af alarmer.
- `--timing`, `-tm`: Viser varigheden af inspektionsprocessen efter færdiggørelse.
  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For kun at inspicere en specifik tabel og tvinge genberegning af predictioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommando er nyttig til at generere opdaterede profiler og predictioner, overvåge dataintegritet og administrere alarm-systemer inden for et specificeret projekt-tidsrum.

## Brug af `tls-status`-kommandoen

Kommandoen `tls-status` i ***digna*** CLI bruges til at forespørge status for Traffic Light System (TLS) for en specifik tabel i et projekt på en given dato. Traffic Light Systemet giver indsigt i datakvalitet og -sundhed og indikerer eventuelle problemer eller alarmer, der kræver opmærksomhed.
  
#### Kommando brug
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, som TLS-status forespørges for (påkrævet).
- **TABLE_NAME**: Den specifikke tabel inden for projektet, som TLS-status er nødvendig for (påkrævet).
- **DATE**: Datoen, som TLS-status forespørges for, typisk i formatet %Y-%m-%d (påkrævet).
  
#### Eksempel
  
For at tjekke TLS-status for en tabel ved navn UserData i projektet ProjectA den 1. juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Denne kommando hjælper brugere med at overvåge og vedligeholde datakvalitet ved at levere en klar og handlingsrettet statusrapport baseret på foruddefinerede kriterier.

## Brug af `inspect-async`-kommandoen

Kommandoen `inspect-async` i ***digna*** CLI bruges til at instruere backend om asynkront at udføre inspektionen for en eller flere datakilder for et givet projekt. Hvis project_name er sat til all-projects, vil inspektionen iterere over alle tilgængelige projekter og udføre inspektionen. Den returnerer et request id, som kan bruges til at spore inspektionens fremdrift.

#### Kommando brug

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, som data skal inspiceres for (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdatoen og -tidspunktet for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdatoen og -tidspunktet for datainspektionen, med samme formater som FROM_DATE (påkrævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel i projektet.
- `--table-filter`, `-tf`: Filtre til kun at inspicere tabeller, der indeholder den angivne substring i deres navne.

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Brug af `inspect-status`-kommandoen

Kommandoen `inspect-status` i ***digna*** CLI bruges til at tjekke fremdriften af en asynkron inspektion baseret på request ID.

#### Kommando brug

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenter
  
- **REQUEST_ID**: Request id returneret af `inspect-async`-kommandoen 
  
#### Options

- `--report_level`, `-rl`: Sæt rapportniveau: 'task' eller 'step' [default: task]
  
#### Eksempel
  
For at tjekke fremdriften af en inspektion med request ID 12345 på detaljeret step-niveau:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Brug af `export-ds`-kommandoen

Kommandoen `export-ds` i ***digna*** CLI bruges til at lave en eksport af datakilder fra ***digna*** repositoryet. Som standard eksporteres alle datakilder fra et givent projekt.

#### Kommando brug
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvorfra datakilderne eksporteres.

#### Options

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et projekt.
- `--exportfile`, `-ef`: Angiv filnavnet for eksporten.
    
#### Eksempel
  
For at eksportere alle datakilder fra projektet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommando eksporterer alle datakilder fra `ProjectA` som et JSON-dokument, der kan importeres til et andet projekt eller et andet ***digna*** repository.


## Brug af `import-ds`-kommandoen

Kommandoen `import-ds` i ***digna*** CLI bruges til at importere datakilder ind i et målprojekt og oprette en import-rapport.

#### Kommando brug
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, som datakilderne importeres til.
- **EXPORT_FILE**: Filnavnet på datakilde-eksporten, der skal importeres.

#### Options

- `--output-file`, `-o`: Fil til at gemme import-rapporten (hvis ikke angivet, udskrives den i terminalen i tabelform).
- `--output-format`, `-f`: Format til at gemme import-rapporten (json, csv).
    
#### Eksempel
  
For at importere alle datakilder fra eksportfilen `my_export.json` ind i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen vil denne kommando også vise en rapport over importerede og springede objekter. Kun nye datakilder vil blive importeret til `ProjectB`. For at finde ud af, hvilke objekter der ville blive importeret og sprunget over, kan du bruge kommandoen `plan-import-ds`.

## Brug af `plan-import-ds`-kommandoen

Kommandoen `plan-import-ds` i ***digna*** CLI bruges til at analysere en datakilde-eksport og vise en importplan for et målprojekt.

#### Kommando brug
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, som datakilderne ville blive importeret til.
- **EXPORT_FILE**: Filnavnet på datakilde-eksporten, der skal analyseres før import.

#### Options

- `--output-file`, `-o`: Fil til at gemme import-rapporten (hvis ikke angivet, udskrives den i terminalen i tabelform).
- `--output-format`, `-f`: Format til at gemme import-rapporten (json, csv).
    
#### Eksempel
  
For at tjekke hvilke datakilder der ville blive importeret og hvilke der ville blive sprunget over fra eksportfilen `my_export.json`, når de importeres til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommando vil kun vise en importplan over objekter, der vil blive importeret og sprunget over.