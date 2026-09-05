# digna CLI Reference 2026.01
**2026-01-15**

Denne side dokumenterer det fulde sæt af kommandoer, der er tilgængelige i ***digna*** CLI-udgivelsen **2026.01**, inklusive brugseksempler og muligheder.

---

## CLI - Grundlæggende

---

### help
Optionen `--help` giver information om tilgængelige kommandoer og deres brug. Der er to hovedmåder at anvende denne option på:

1. **Visning af generel hjælp:**
   
    Brug --help umiddelbart efter nøgleordet ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Hjælp til specifikke kommandoer:**  
  
    For detaljeret information om en specifik kommando, tilføj `--help` til den pågældende kommando.
    For eksempel, for at få hjælp til kommandoen `add-user`, kør:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommando beskrivelse:** Giver en detaljeret beskrivelse af, hvad kommandoen gør.  
     - **Syntax:** Viser den præcise syntaks, inklusive krævede og valgfrie argumenter.  
     - **Options:** Lister eventuelle options specifikke for kommandoen, sammen med deres forklaringer.  
     - **Eksempler:** Giver eksempler på, hvordan kommandoen udføres effektivt.

### check-config

check-config-kommandoen er et værktøj i ***digna*** CLI, designet til at teste konfigurationen af ***digna***. Denne kommando sikrer, at ***digna***-komponenterne kan finde de nødvendige konfigurationselementer i config.toml.

#### Options

- `--configpath`, `-cp`: Fil eller mappe, der indeholder konfigurationen. Hvis denne udelades, bruges ../config.toml.
      
#### Kommando brug
```bash
dignacli check-config
```

Ved succesfuld udførelse udskriver kommandoen en bekræftelse på, at konfigurationen er komplet.  
  
Hvis konfigurationen ser ud til at være ufuldstændig, vil de manglende konfigurationselementer blive listet.

  
### check-repo-connection

check-repo-connection-kommandoen er et værktøj i ***digna*** CLI, designet til at teste forbindelsen og adgangen til et specificeret ***digna*** repository. Denne kommando sikrer, at CLI’en kan interagere med repositoryet.
      
#### Kommando brug
```bash
dignacli check-repo-connection
```

Ved succesfuld udførelse returnerer kommandoen en bekræftelse af forbindelsen, sammen med detaljer om repositoryet: Repository version, Host, Database og Schema.  
  
Hvis repository-forbindelsen ikke er succesfuld, kontroller da config.toml-filen for korrekte konfigurationsindstillinger.


### version

For at tjekke den installerede version af *dignacli*, brug optionen --version.  
  
#### Kommando brug
```bash
dignacli --version
```
  
#### Eksempel på output
```bash
dignacli version 2026.01
```

### logningsmuligheder
  
Som standard er konsoloutputtet fra ***digna***-kommandoerne designet til at være minimalistisk. De fleste kommandoer tilbyder mulighed for at give yderligere information ved at bruge følgende options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” og ”debug” angiver niveauet af detaljer, mens ”logfile”-switch’en tillader at omdirigere outputtet til at blive skrevet til en fil i stedet for konsolvinduet.

## Brugerstyring

### add-user
  
add-user-kommandoen i ***digna*** CLI bruges til at tilføje en ny bruger til ***digna***-systemet.
  
#### Kommando brug
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenter

- **USER_NAME**: Brugernavnet for den nye bruger (krævet).
- **USER_FULL_NAME**: Den fulde navn på den nye bruger (krævet).
- **USER_PASSWORD**: Adgangskoden for den nye bruger (krævet).

#### Options

- `--is_superuser`, `-su`: Flag for at udpege den nye bruger som admin.
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke angivet, har kontoen ingen udløbsdato.

#### Eksempel

For at tilføje en ny bruger med brugernavn `jdoe`, fulde navn `John Doe`, og adgangskode `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For at tilføje en ny bruger og sætte en kontoudløbsdato:
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
- **USER_NAME**: Brugernavnet på den bruger, der skal slettes (krævet). Dette er det eneste argument, som kommandoen kræver.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Udførelse af denne kommando vil fjerne brugeren `jdoe` fra ***digna***-systemet, tilbagekalde deres adgang og slette deres tilknyttede data og tilladelser fra repositoryet.

### modify-user

`modify-user`-kommandoen i ***digna*** CLI bruges til at opdatere detaljer for en eksisterende bruger i ***digna***-systemet.

#### Kommando brug
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenter
  
- **USER_NAME**: Brugernavnet på den bruger, der skal ændres (krævet).
- **USER_FULL_NAME**: Det nye fulde navn for brugeren (krævet).
  
#### Options  
  
- `--is_superuser`, `-su`: Gør brugeren til superuser og giver forhøjede rettigheder. Dette flag kræver ingen værdi.  
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angivet, forbliver kontoen gyldig på ubestemt tid.  
  
#### Eksempel
  
For at ændre fulde navn for brugeren `jdoe` til “Johnathan Doe” og sætte brugeren som superuser:
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
  
- **USER_NAME**: Brugernavnet på den bruger, hvis adgangskode skal ændres (krævet).
- **USER_PWD**: Den nye adgangskode for brugeren (krævet).
  
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

Udførelse af denne kommando i ***digna*** CLI vil oprette forbindelse til ***digna***-repositoryet og liste alle brugere, vise deres ID, brugernavn, fulde navn, superuser-status og udløbstidsstempler.

## Repository-administration

### upgrade-repo
  
`upgrade-repo`-kommandoen i ***digna*** CLI bruges til at opgradere eller initialisere ***digna***-repositoryet. Denne kommando er nødvendig for at anvende opdateringer eller opsætte repository-infrastrukturen for første gang.
  
#### Kommando brug

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Når denne er aktiveret, kører kommandoen i simuleringsmode, hvilket udskriver de SQL-udtryk, der ville blive eksekveret, men uden faktisk at eksekvere dem. Dette er nyttigt til at få et overblik over ændringer uden at foretage ændringer i repositoryet.  

  
#### Eksempel
  
For at opgradere ***digna***-repositoryet kan du køre kommandoen uden nogen options:
  
```bash
dignacli upgrade-repo
```  
For at køre opgraderingen i simuleringsmode (for at se SQL-udtryk uden at anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommando er afgørende for at vedligeholde ***digna***-systemet og sikre, at databaseskemaet og andre repository-komponenter er opdaterede i forhold til den seneste softwareversion.

### encrypt
  
`encrypt`-kommandoen i ***digna*** CLI bruges til at kryptere en adgangskode.
  
#### Kommando brug
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenter
- **PASSWORD**: Adgangskoden, der skal krypteres (krævet).
  
#### Eksempel
  
For at kryptere en adgangskode, skal du angive adgangskoden som et argument.   
For eksempel, for at kryptere adgangskoden `mypassword123`, ville du bruge:
```bash
dignacli encrypt mypassword123
```
Denne kommando returnerer den krypterede version af den angivne adgangskode, som derefter kan bruges i sikre sammenhænge. Hvis adgangskodeargumentet ikke er angivet, vil CLI’en vise en fejl, der indikerer det manglende argument.

### generate-key
  
`generate-key`-kommandoen bruges til at generere en Fernet-nøgle, som er nødvendig for at sikre adgangskoder, der er lagret i ***digna***-repositoryet.
  
#### Kommando brug
```bash
dignacli generate-key
```
  
## Datastyring

### clean-up

`clean-up`-kommandoen i ***digna*** CLI bruges til at fjerne profiler, forudsigelser (predictions) og trafiklyssystemdata for en eller flere datakilder inden for et angivet projekt. Denne kommando er vigtig for livscyklusstyring af data og hjælper med at opretholde et organiseret og effektivt data-miljø ved at rydde ud i forældet eller unødvendigt data.

#### Kommando brug

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, hvorfra data skal fjernes (krævet). Ved at bruge nøgleordet all-projects i dette argument instrueres ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og -tidspunkt for datafjernelsen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (krævet).
- **TO_DATE**: Slutdato og -tidspunkt for datafjernelsen, i samme formater som FROM_DATE (krævet).
  
#### Options
  
- `--table-name`, `-tn`: Begrænser clean-up-operationen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filtre for at begrænse clean-up til tabeller, der indeholder den angivne delstreng i deres navne.
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
  
Denne kommando hjælper med at styre datalagring og sikre, at repositoryet kun indeholder relevant information.

### remove-orphans
  
`remove-orphans`-kommandoen i ***digna*** CLI bruges til vedligeholdelse i ***digna***-repositoryet.  
Når en bruger sletter projekter eller datakilder, forbliver profiler og forudsigelser i repositoryet. Med denne kommando vil sådanne forældreløse rækker blive fjernet fra repositoryet.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

### list-projects
  
`list-projects`-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige projekter inden for ***digna***-systemet.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

Denne kommando er særligt nyttig for administratorer og brugere, der administrerer flere projekter, idet den giver et hurtigt overblik over de tilgængelige projekter i ***digna***-repositoryet.

### list-ds

`list-ds`-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige datakilder inden for et specificeret projekt. Denne kommando er nyttig for at få overblik over de dataressourcer, der er tilgængelige til analyse og styring i ***digna***-systemet.

#### Kommando brug
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, som datakilderne listes for (krævet).
  
#### Eksempel
  
For at liste alle datakilder i projektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommando giver brugerne et overblik over de datakilder, der er tilgængelige i et projekt, og hjælper dem med at navigere og administrere datalandskabet mere effektivt.


### inspect

`inspect`-kommandoen i ***digna*** CLI bruges til at oprette profiler, forudsigelser og trafiklyssystemdata for en eller flere datakilder inden for et angivet projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode. Efter gennemførelse af inspektionen returneres værdien af det beregnede trafiklyssystem:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Kommando brug

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, der skal inspiceres (krævet). Ved at bruge nøgleordet all-projects i dette argument instrueres ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og -tidspunkt for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (krævet).
- **TO_DATE**: Slutdato og -tidspunkt for datainspektionen, i samme formater som FROM_DATE (krævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filtre for kun at inspicere tabeller, der indeholder den angivne delstreng i deres navne.
- `--enable_notification`, `-en`: Aktiverer afsendelse af notifikationer i tilfælde af alarmer.
- `--bypass-backend`, `-bb`: Omgå backend og kør inspektionen direkte fra CLI (kun til testformål!).

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For kun at inspicere en specifik tabel og tvinge genberegning af forudsigelser:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommando er nyttig til at generere opdaterede profiler og forudsigelser, overvåge dataintegritet og styre alarmsystemer inden for en angiven projekt-tidsramme.

### inspect-async

`inspect-async`-kommandoen i ***digna*** CLI bruges til at oprette profiler, forudsigelser og trafiklyssystemdata for en eller flere datakilder inden for et angivet projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode. I kontrast til `inspect`-kommandoen venter denne ikke på, at inspektionen fuldføres.
I stedet returnerer den anmodnings-id’et for den indsendte inspektionsanmodning. For at forespørge fremskridt i inspektionsprocessen, brug kommandoen `inspect-status`.

#### Kommando brug

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, der skal inspiceres (krævet). Ved at bruge nøgleordet all-projects i dette argument instrueres ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og -tidspunkt for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (krævet).
- **TO_DATE**: Slutdato og -tidspunkt for datainspektionen, i samme formater som FROM_DATE (krævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filtre for kun at inspicere tabeller, der indeholder den angivne delstreng i deres navne.
- `--enable_notification`, `-en`: Aktiverer afsendelse af notifikationer i tilfælde af alarmer.

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

`inspect-status`-kommandoen i ***digna*** CLI bruges til at tjekke fremskridtet for en asynkron inspektion baseret på anmodnings-id.

#### Kommando brug

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenter
  
- **REQUEST_ID**: Anmodnings-id’et returneret af `inspect-async`-kommandoen 
  
#### Eksempel
  
For at tjekke fremskridtet af en inspektion med anmodnings-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

`inspect-cancel`-kommandoen i ***digna*** CLI bruges til at annullere inspektioner baseret på anmodnings-id eller kan bruges til at annullere alle aktuelle anmodninger.

#### Kommando brug

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenter
  
- **REQUEST_ID**: Anmodnings-id’et returneret af `inspect-async`-kommandoen 
  
#### Eksempel
  
For at annullere inspektionen med anmodnings-id 12345:
  
```bash
dignacli inspect-cancel 12345
```

For at annullere alle anmodninger, der i øjeblikket kører eller er i kø:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

`export-ds`-kommandoen i ***digna*** CLI bruges til at skabe en eksport af datakilder fra ***digna***-repositoryet. Som standard eksporteres alle datakilder fra et givet projekt.

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
  
For at eksportere alle datakilder fra projektet med navnet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommando eksporterer alle datakilder fra `ProjectA` som et JSON-dokument, der kan importeres til et andet projekt eller ***digna***-repository.

### import-ds

`import-ds`-kommandoen i ***digna*** CLI bruges til at importere datakilder ind i et målprojekt og skabe en importrapport.

#### Kommando brug
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvortil datakilderne skal importeres.
- **EXPORT_FILE**: Filnavnet for den datakildeeksport, der skal importeres.

#### Options

- `--output-file`, `-o`: Fil til at gemme importrapporten (hvis ikke angivet, udskrives den i terminalen i tabelform).
- `--output-format`, `-f`: Format til at gemme importrapporten (json, csv).
    
#### Eksempel
  
For at importere alle datakilder fra eksportfilen `my_export.json` til `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen viser denne kommando også en rapport over importerede og sprangne objekter. Kun nye datakilder vil blive importeret ind i `ProjectB`. For at se, hvilke objekter der ville blive importeret og sprunget over, kan du bruge kommandoen `plan-import-ds`.

### plan-import-ds

`plan-import-ds`-kommandoen i ***digna*** CLI bruges til at analysere en datakildeeksport og skabe en importplan/rapport uden faktisk at udføre importen.

#### Kommando brug
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, hvortil datakilderne ville blive importeret.
- **EXPORT_FILE**: Filnavnet for den datakildeeksport, der skal analyseres før import.

#### Options

- `--output-file`, `-o`: Fil til at gemme importrapporten (hvis ikke angivet, udskrives den i terminalen i tabelform).
- `--output-format`, `-f`: Format til at gemme importrapporten (json, csv).
    
#### Eksempel
  
For at tjekke, hvilke datakilder der ville blive importeret, og hvilke der ville blive sprunget over fra eksportfilen `my_export.json`, hvis den importeres til `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommando viser kun en importplan over objekter, der ville blive importeret og sprunget over.