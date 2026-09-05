# digna CLI Reference 2026.04
**2026-04-08**

Denne side dokumenterer det fulde sæt af kommandoer, der er tilgængelige i ***digna*** CLI-udgivelsen **2026.04**, inklusive brugseksempler og muligheder.

---

## CLI-grundlæggende

---

### help
Optionen `--help` giver information om tilgængelige kommandoer og deres brug. Der er to hovedmåder at bruge denne option på:

1. **Visning af generel hjælp:**
   
    Brug --help straks efter nøgleordet ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Hent hjælp for specifikke kommandoer:**  
  
    For detaljeret information om en specifik kommando, tilføj `--help` til den pågældende kommando.
    For eksempel, for at få hjælp til kommandoen `add-user`, kør:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommando beskrivelse:** Giver en detaljeret forklaring af, hvad kommandoen gør.  
     - **Syntax:** Viser den nøjagtige syntaks, inklusive nødvendige og valgfrie argumenter.  
     - **Options:** Lister eventuelle options, der er specifikke for kommandoen, sammen med deres forklaringer.  
     - **Eksempler:** Giver eksempler på, hvordan kommandoen kan køres effektivt.

### check-config

check-config-kommandoen er et værktøj i ***digna*** CLI-værktøjet designet til at teste konfigurationen af ***digna***. Denne kommando sikrer, at ***digna***-komponenterne kan finde de nødvendige konfigurationselementer i config.toml.

#### Options

- `--configpath`, `-cp`: Fil eller mappe, der indeholder konfigurationen. Hvis den udelades, bruges ../config.toml.
      
#### Kommando brug
```bash
dignacli check-config
```

Ved succesfuld eksekvering udskriver kommandoen en bekræftelse af konfigurationens fuldstændighed.  
  
Hvis konfigurationen forekommer ufuldstændig, vil de manglende konfigurationselementer blive listet.

  
### check-repo-connection

check-repo-connection-kommandoen er et værktøj i ***digna*** CLI designet til at teste forbindelsen og adgangen til et specificeret ***digna***-repository. Denne kommando sikrer, at CLI'en kan interagere med repository'et.
      
#### Kommando brug
```bash
dignacli check-repo-connection
```

Ved succesfuld eksekvering udskriver kommandoen en bekræftelse af forbindelsen samt detaljer om repository'et: Repository version, Host, Database og Schema.  
  
Hvis repository-forbindelsen ikke lykkes, tjek config.toml-filen for korrekte konfigurationsindstillinger.


### version

For at kontrollere den installerede version af *dignacli*, brug optionen --version.  
  
#### Kommando brug
```bash
dignacli --version
```
  
#### Eksempel output
```bash
dignacli version 2026.04
```

### logging options
  
Som standard er konsoloutputtet fra ***digna***-kommandoer designet til at være minimalistisk. De fleste kommandoer tilbyder muligheden for at give yderligere information ved brug af følgende options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” og ”debug” definerer detaljeringsniveauet, mens ”logfile”-switch'en tillader at omdirigere outputtet til en fil i stedet for konsolvinduet.

## Brugerstyring

### add-user
  
add-user-kommandoen i ***digna*** CLI bruges til at tilføje en ny bruger til ***digna***-systemet.
  
#### Kommando brug
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenter

- **USER_NAME**: Brugernavn for den nye bruger (påkrævet).
- **USER_FULL_NAME**: Den nye brugers fulde navn (påkrævet).
- **USER_PASSWORD**: Adgangskoden for den nye bruger (påkrævet).

#### Options

- `--is_superuser`, `-su`: Flag for at betegne den nye bruger som administrator.
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerens konto i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke sat, har kontoen ingen udløbsdato.

#### Eksempel

For at tilføje en ny bruger med brugernavn `jdoe`, fulde navn `John Doe`, og adgangskode `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For at tilføje en ny bruger og sætte en konto-udløbsdato:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
`delete-user`-kommandoen i ***digna*** CLI bruges til at fjerne en eksisterende bruger fra ***digna***-systemet.
  
#### Kommando brug
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenter
- **USER_NAME**: Brugernavnet for den bruger, der skal slettes (påkrævet). Dette er det eneste argument, som kommandoen kræver.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Når denne kommando køres, fjernes brugeren `jdoe` fra ***digna***-systemet, og deres adgang samt tilknyttede data og rettigheder i repository'et tilbagekaldes.

### modify-user

`modify-user`-kommandoen i ***digna*** CLI bruges til at opdatere oplysninger for en eksisterende bruger i ***digna***-systemet.

#### Kommando brug
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenter
  
- **USER_NAME**: Brugernavnet på den bruger, der skal ændres (påkrævet).
- **USER_FULL_NAME**: Det nye fulde navn for brugeren (påkrævet).
  
#### Options  
  
- `--is_superuser`, `-su`: Sætter brugeren som superuser og giver forhøjede rettigheder. Dette flag kræver ingen værdi.  
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angivet, forbliver kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For at ændre fulde navn for brugeren `jdoe` til ”Johnathan Doe” og sætte brugeren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
`modify-user-pwd`-kommandoen i ***digna*** CLI bruges til at ændre adgangskoden for en eksisterende bruger i ***digna***-systemet.
  
#### Kommando brug
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenter
  
- **USER_NAME**: Brugernavnet for den bruger, hvis adgangskode skal ændres (påkrævet).
- **USER_PWD**: Den nye adgangskode for brugeren (påkrævet).
  
#### Eksempel
  
For at ændre adgangskoden for brugeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

`list-users`-kommandoen i ***digna*** CLI viser en liste over alle brugere registreret i ***digna***-systemet.

#### Kommando brug

```bash
dignacli list-users
```

Når denne kommando køres, opretter ***digna***-CLI'en forbindelse til ***digna***-repository'et og lister alle brugere, viser deres ID, brugernavn, fulde navn, superuser-status og udløbstidsstempler.

## Repository-styring

### upgrade-repo
  
`upgrade-repo`-kommandoen i ***digna*** CLI bruges til at opgradere eller initialisere ***digna***-repository'et. Denne kommando er essentiel for at anvende opdateringer eller opsætte repository-infrastrukturen for første gang.
  
#### Kommando brug

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Når denne er aktiveret, kører kommandoen i simuleringsmode, hvilket udskriver de SQL-sætninger, der ville blive eksekveret, men udfører dem ikke. Dette er nyttigt til at forhåndsvise ændringer uden at foretage modifikationer i repository'et.  

  
#### Eksempel
  
For at opgradere ***digna***-repository'et kan du køre kommandoen uden nogen options:
  
```bash
dignacli upgrade-repo
```  
For at køre opgraderingen i simuleringsmode (for at se SQL-sætningerne uden at anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommando er afgørende for vedligeholdelse af ***digna***-systemet og sikrer, at databaseskemaet og andre repository-komponenter er opdaterede med den seneste softwareversion.

### encrypt
  
`encrypt`-kommandoen i ***digna*** CLI bruges til at kryptere en adgangskode.
  
#### Kommando brug
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenter
- **PASSWORD**: Adgangskoden, der skal krypteres (påkrævet).
  
#### Eksempel
  
For at kryptere en adgangskode skal du angive adgangskoden som et argument.   
For eksempel, for at kryptere adgangskoden `mypassword123`, ville du bruge:
```bash
dignacli encrypt mypassword123
```
Denne kommando udskriver den krypterede version af den angivne adgangskode, som så kan bruges i sikre sammenhænge. Hvis adgangskode-argumentet ikke er angivet, vil CLI'en vise en fejl, der angiver det manglende argument.

### generate-key
  
`generate-key`-kommandoen bruges til at generere en Fernet-nøgle, som er nødvendig for at sikre adgangskoder gemt i ***digna***-repository'et.
  
#### Kommando brug
```bash
dignacli generate-key
```
  
## Datahåndtering

### clean-up

`clean-up`-kommandoen i ***digna*** CLI bruges til at fjerne profiler, predictioner og trafiklyssystemdata for en eller flere datakilder inden for et specificeret projekt. Denne kommando er vigtig for data-lifecycle-styring og hjælper med at holde et organiseret og effektivt data-miljø ved at rydde forældet eller unødvendige data.

#### Kommando brug

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, hvorfra data skal fjernes (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tidspunkt for datafjernelsen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tidspunkt for datafjernelsen, med samme formater som FROM_DATE (påkrævet).
  
#### Options
  
- `--table-name`, `-tn`: Begrænser clean-up-operationen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filtrerer for kun at rydde tabeller, der indeholder den angivne substring i deres navne.
- `--timing`, `-tm`: Viser tidsforbruget for clean-up-processen efter afslutning.
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
  
Denne kommando hjælper med at styre datalagring og sikre, at repository'et kun indeholder relevant information.

### remove-orphans
  
`remove-orphans`-kommandoen i ***digna*** CLI anvendes til housekeeping i ***digna***-repository'et.  
Når en bruger sletter projekter eller datakilder, kan profiler og predictioner blive efterladt i repository'et. Med denne kommando fjernes sådanne forældreløse rækker fra repository'et.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects`-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige projekter i ***digna***-systemet.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

Denne kommando er særligt nyttig for administratorer og brugere, der administrerer flere projekter, da den giver et hurtigt overblik over de tilgængelige projekter i ***digna***-repository'et.

### list-ds

`list-ds`-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige datakilder inden for et specificeret projekt. Denne kommando er nyttig til at få overblik over de dataaktiver, der er tilgængelige til analyse og styring i ***digna***-systemet.

#### Kommando brug
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvis datakilder der listes (påkrævet).
  
#### Eksempel
  
For at liste alle datakilder i projektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommando giver brugerne et overblik over de datakilder, der er tilgængelige i et projekt og hjælper dem med at navigere og administrere datalandskabet mere effektivt.


### inspect

`inspect`-kommandoen i ***digna*** CLI bruges til at oprette profiler, predictioner og trafiklyssystemdata for en eller flere datakilder inden for et specificeret projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode. Efter inspektionen returneres værdien af det beregnede trafiklyssystem:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Kommando brug

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, der skal inspiceres (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tidspunkt for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tidspunkt for datainspektionen, med samme formater som FROM_DATE (påkrævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel i projektet.
- `--table-filter`, `-tf`: Filtrerer for kun at inspicere tabeller, der indeholder den angivne substring i deres navne.
- `--enable_notification`, `-en`: Aktiverer afsendelse af notifikationer i tilfælde af alerts.
- `--bypass-backend`, `-bb`: Omgå backend og kør inspektionen direkte fra CLI'en (kun til testformål!).

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For kun at inspicere en specifik tabel og tvinge genberegning af predictioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommando er nyttig til at generere opdaterede profiler og predictioner, overvåge dataintegritet og styre alarmsystemer inden for en specificeret projekt-tidsramme.

### inspect-async

`inspect-async`-kommandoen i ***digna*** CLI bruges til at oprette profiler, predictioner og trafiklyssystemdata for en eller flere datakilder inden for et specificeret projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode. I modsætning til `inspect`-kommandoen venter denne ikke på, at inspektionen bliver fuldført.
I stedet returnerer den request-id'en for den indsendte inspektionsanmodning. For at forespørge fremdriften af inspektionsprocessen, brug kommandoen `inspect-status`.

#### Kommando brug

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, der skal inspiceres (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tidspunkt for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tidspunkt for datainspektionen, med samme formater som FROM_DATE (påkrævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel i projektet.
- `--table-filter`, `-tf`: Filtrerer for kun at inspicere tabeller, der indeholder den angivne substring i deres navne.
- `--enable_notification`, `-en`: Aktiverer afsendelse af notifikationer i tilfælde af alerts.

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-kommandoen i ***digna*** CLI bruges til at tjekke fremdriften af en asynkron inspektion baseret på request-id.

#### Kommando brug

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id'en returneret af `inspect-async`-kommandoen 
  
#### Eksempel
  
For at tjekke fremdriften af en inspektion med request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-kommandoen i ***digna*** CLI bruges til at annullere inspektioner baseret på request-id eller kan bruges til at annullere alle igangværende anmodninger.

#### Kommando brug

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id'en returneret af `inspect-async`-kommandoen 
  
#### Eksempel
  
For at annullere inspektionen med request-id 12345:
  
```bash
dignacli inspect-cancel 12345
```

For at annullere alle anmodninger, der i øjeblikket kører eller er i kø:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-kommandoen i ***digna*** CLI bruges til at oprette en eksport af datakilder fra ***digna***-repository'et. Som standard eksporteres alle datakilder fra et givent projekt.

#### Kommando brug
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvorfra datakilderne vil blive eksporteret.

#### Options

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et projekt.
- `--exportfile`, `-ef`: Angiv filnavnet for eksporten.
    
#### Eksempel
  
For at eksportere alle datakilder fra projektet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommando eksporterer alle datakilder fra `ProjectA` som et JSON-dokument, der kan importeres til et andet projekt eller ***digna***-repository.


### import-ds

`import-ds`-kommandoen i ***digna*** CLI bruges til at importere datakilder til et målprojekt og oprette en importrapport.

#### Kommando brug
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvortil datakilderne vil blive importeret.
- **EXPORT_FILE**: Filnavnet på den dataeksport, der skal importeres.

#### Options

- `--output-file`, `-o`: Fil til at gemme importrapporten (hvis ikke specificeret, udskrives den til terminalen i tabelformat).
- `--output-format`, `-f`: Format til at gemme importrapporten (json, csv).
    
#### Eksempel
  
For at importere alle datakilder fra eksportfilen `my_export.json` ind i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen viser denne kommando også en rapport over importerede og sprundne objekter. Kun nye datakilder vil blive importeret til `ProjectB`. For at finde ud af, hvilke objekter der ville blive importeret og sprunget over, kan du bruge kommandoen `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-kommandoen i ***digna*** CLI bruges til at analysere en eksport af datakilder i forhold til et målprojekt og skabe en importrapport uden faktisk at importere noget.

#### Kommando brug
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvortil datakilderne ville blive importeret.
- **EXPORT_FILE**: Filnavnet på dataeksporten, der skal analyseres før import.

#### Options

- `--output-file`, `-o`: Fil til at gemme importrapporten (hvis ikke specificeret, udskrives den til terminalen i tabelformat).
- `--output-format`, `-f`: Format til at gemme importrapporten (json, csv).
    
#### Eksempel
  
For at tjekke, hvilke datakilder der ville blive importeret, og hvilke der ville blive sprunget over fra eksportfilen `my_export.json`, når den importeres til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommando viser kun en importplan over objekter, der vil blive importeret og sprunget over.