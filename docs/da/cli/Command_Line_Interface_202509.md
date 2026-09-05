---
title: digna CLI Reference 2025.09 – Kommandoer & Eksempler | digna Dokumentation
description: Fuld reference for digna CLI-udgivelse 2025.109. Lær, hvordan du administrerer brugere, repositories og data med kommandoer som add-user, check-config, check-repo-connection, inspect, inspect-async og flere.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Denne side dokumenterer det komplette sæt af kommandoer, der er tilgængelige i ***digna*** CLI-udgivelsen **2025.09**, inklusive brugseksempler og muligheder.

---

## CLI-grundlæggende

---

### help
Optionen `--help` giver information om tilgængelige kommandoer og deres brug. Der er to hovedmåder at bruge denne option på:

1. **Visning af generel hjælp:**
   
    Brug --help umiddelbart efter nøgleordet `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Hent hjælp til specifikke kommandoer:**  
  
    For detaljeret information om en bestemt kommando, tilføj `--help` til den kommando.
    For eksempel, for at få hjælp til kommandoen `add-user`, kør:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommando beskrivelse:** Giver en detaljeret beskrivelse af, hvad kommandoen gør.  
     - **Syntax:** Viser den nøjagtige syntaks, inklusive krævede og valgfrie argumenter.  
     - **Options:** Lister eventuelle options specifikke for kommandoen sammen med deres forklaringer.  
     - **Eksempler:** Giver eksempler på, hvordan kommandoen kan køres effektivt.

### check-config

Kommandoen check-config er et værktøj i ***digna*** CLI, designet til at teste konfigurationen af ***digna***. Denne kommando sikrer, at ***digna*** komponenterne kan finde de nødvendige konfigurationselementer i config.toml.

#### Options

- `--configpath`, `-cp`: Fil eller bibliotek, der indeholder konfigurationen. Hvis den udelades, vil ../config.toml blive brugt.
      
#### Kommando brug
```bash
dignacli check-config
```

Ved succesfuld eksekvering vil kommandoen udskrive en bekræftelse af, at konfigurationen er komplet.  
  
Hvis konfigurationen ser ud til at være ufuldstændig, vil de manglende konfigurationselementer blive listet.

  
### check-repo-connection

Kommandoen check-repo-connection er et værktøj i ***digna*** CLI designet til at teste forbindelsen og adgangen til et specificeret ***digna*** repository. Denne kommando sikrer, at CLI'en kan interagere med repositoryet.
      
#### Kommando brug
```bash
dignacli check-repo-connection
```

Ved succesfuld eksekvering vil kommandoen udskrive en bekræftelse af forbindelsen samt detaljer om repositoryet: Repository-version, Host, Database og Schema.  
  
Hvis repository-forbindelsen ikke er succesfuld, så tjek config.toml-filen for korrekte konfigurationsindstillinger.


### version

For at tjekke den installerede version af *dignacli*, brug optionen --version.  
  
#### Kommando brug
```bash
dignacli --version
```
  
#### Eksempeloutput
```bash
dignacli version 2025.09
```

### logningsmuligheder
  
Som standard er konsoloutputtet fra ***digna*** kommandoerne designet til at være minimalistisk. De fleste kommandoer tilbyder muligheden for at give yderligere information ved hjælp af følgende options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 “verbose” og “debug” definerer detaljeringsgraden, mens “logfile”-switch’en tillader at omdirigere outputtet til en fil i stedet for konsolvinduet.

## Brugerstyring

### add-user
  
Kommandoen add-user i ***digna*** CLI bruges til at tilføje en ny bruger til ***digna*** systemet.
  
#### Kommando brug
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenter

- **USER_NAME**: Brugernavnet for den nye bruger (påkrævet).
- **USER_FULL_NAME**: Fulde navn på den nye bruger (påkrævet).
- **USER_PASSWORD**: Adgangskoden for den nye bruger (påkrævet).

#### Options

- `--is_superuser`, `-su`: Flag for at udpege den nye bruger som administrator.
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke sat, har kontoen ingen udløbsdato.

#### Eksempel

For at tilføje en ny bruger med brugernavn `jdoe`, fulde navn `John Doe` og adgangskode `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For at tilføje en ny bruger og sætte en konto-udløbsdato:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Kommandoen `delete-user` i ***digna*** CLI bruges til at fjerne en eksisterende bruger fra ***digna*** systemet.
  
#### Kommando brug
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenter
- **USER_NAME**: Brugernavnet på den bruger, der skal slettes (påkrævet). Dette er det eneste argument, kommandoen kræver.

#### Eksempel
```bash
dignacli delete-user jdoe
```
  
Når denne kommando køres, vil brugeren `jdoe` blive fjernet fra ***digna*** systemet, deres adgang vil blive inddraget, og deres tilknyttede data og rettigheder i repositoryet vil blive slettet.

### modify-user

Kommandoen `modify-user` i ***digna*** CLI bruges til at opdatere oplysningerne for en eksisterende bruger i ***digna*** systemet.

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
  
For at ændre fulde navnet for brugeren `jdoe` til “Johnathan Doe” og sætte brugeren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Kommandoen `modify-user-pwd` i ***digna*** CLI bruges til at ændre adgangskoden for en eksisterende bruger i ***digna*** systemet.
  
#### Kommando brug
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenter
  
- **USER_NAME**: Brugernavnet på den bruger, hvis adgangskode skal ændres (påkrævet).
- **USER_PWD**: Den nye adgangskode for brugeren (påkrævet).
  
#### Eksempel
  
For at ændre adgangskoden for brugeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Kommandoen `list-users` i ***digna*** CLI viser en liste over alle brugere registreret i ***digna*** systemet.

#### Kommando brug

```bash
dignacli list-users
```

Når denne kommando køres i ***digna*** CLI, vil den forbinde til ***digna*** repositoryet og liste alle brugere, vise deres ID, brugernavn, fulde navn, superuser-status og udløbstidsstempler.

## Repository-administration

### upgrade-repo
  
Kommandoen `upgrade-repo` i ***digna*** CLI bruges til at opgradere eller initialisere ***digna*** repositoryet. Denne kommando er nødvendig for at anvende opdateringer eller opsætte repository-infrastrukturen for første gang.
  
#### Kommando brug

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Når aktiveret, kører denne option kommandoen i simulationsmode, som udskriver de SQL-udtryk, der ville blive kørt, men udfører dem ikke faktisk. Dette er nyttigt til at få et preview af ændringer uden at ændre repositoryet.  

  
#### Eksempel
  
For at opgradere ***digna*** repositoryet kan du køre kommandoen uden nogen options:
  
```bash
dignacli upgrade-repo
```  
For at køre opgraderingen i simulationsmode (for at se SQL-udtryk uden at anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommando er afgørende for vedligeholdelse af ***digna*** systemet og sikrer, at databaseskemaet og andre repository-komponenter er opdateret til den nyeste version af softwaren.

### encrypt
  
Kommandoen `encrypt` i ***digna*** CLI bruges til at kryptere et password.
  
#### Kommando brug
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenter
- **PASSWORD**: Adgangskoden, som skal krypteres (påkrævet).
  
#### Eksempel
  
For at kryptere en adgangskode, skal du angive adgangskoden som et argument.   
For eksempel, for at kryptere adgangskoden `mypassword123`, ville du bruge:
```bash
dignacli encrypt mypassword123
```
Denne kommando udskriver den krypterede version af den angivne adgangskode, som derefter kan bruges i sikre kontekster. Hvis password-argumentet ikke er angivet, vil CLI'en vise en fejl, der indikerer det manglende argument.

### generate-key
  
Kommandoen `generate-key` bruges til at generere en Fernet-nøgle, som er nødvendig for at sikre adgangskoder, der er gemt i ***digna*** repositoryet.
  
#### Kommando brug
```bash
dignacli generate-key
```
  
## Datahåndtering

### clean-up

Kommandoen `clean-up` i ***digna*** CLI bruges til at fjerne profiler, predictioner og trafiklyssystem-data for en eller flere datakilder inden for et specificeret projekt. Denne kommando er essentiel for datalivscyklusstyring og hjælper med at bevare et organiseret og effektivt data-miljø ved at rydde forældet eller unødvendig data.

#### Kommando brug

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på projektet, hvorfra data skal fjernes (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** til at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og tidspunkt for datafjernelsen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og tidspunkt for datafjernelsen, med samme formater som FROM_DATE (påkrævet).
  
#### Options
  
- `--table-name`, `-tn`: Begrænser clean-up operationen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filter for kun at begrænse clean-up til tabeller, der indeholder den angivne substring i deres navne.
- `--timing`, `-tm`: Viser tidsforbruget for clean-up processen efter færdiggørelse.
- `--help`: Viser hjælpeinformation for clean-up kommandoen og afslutter.
  
#### Eksempel
  
For at fjerne data fra projektet ProjectA mellem 1. januar 2023 og 30. juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
For kun at fjerne data fra en specifik tabel med navnet `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Denne kommando hjælper med at styre datalagring og sikre, at repositoryet kun indeholder relevant information.

### remove-orphans
  
Kommandoen `remove-orphans` i ***digna*** CLI bruges til oprydning i ***digna*** repositoryet.  
Når en bruger sletter projekter eller datakilder, kan profiler og predictioner blive efterladt i repositoryet. Med denne kommando vil sådanne forældreløse rækker blive fjernet fra repositoryet.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

### list-projects
  
Kommandoen `list-projects` i ***digna*** CLI bruges til at vise en liste over alle tilgængelige projekter i ***digna*** systemet.
  
#### Kommando brug
  
```bash
dignacli list-projects
```

Denne kommando er især nyttig for administratorer og brugere, der administrerer flere projekter, da den giver et hurtigt overblik over de tilgængelige projekter i ***digna*** repositoryet.

### list-ds

Kommandoen `list-ds` i ***digna*** CLI bruges til at vise en liste over alle tilgængelige datakilder inden for et specificeret projekt. Denne kommando er nyttig for at få overblik over de dataressourcer, der er tilgængelige til analyse og administration i ***digna*** systemet.

#### Kommando brug
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenter
- **PROJECT_NAME**: Navnet på projektet, for hvilket datakilderne listes (påkrævet).
  
#### Eksempel
  
For at liste alle datakilder i projektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommando giver brugerne et overblik over de datakilder, der er tilgængelige i et projekt, og hjælper dem med at navigere og administrere datalandskabet mere effektivt.


### inspect

Kommandoen `inspect` i ***digna*** CLI bruges til at oprette profiler, predictioner og trafiklyssystem-data for en eller flere datakilder inden for et specificeret projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode. Efter inspektionens afslutning returneres værdien af det beregnede trafiklyssystem:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Kommando brug

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på projektet, der skal inspiceres (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** til at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og tidspunkt for data-inspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og tidspunkt for data-inspektionen, med samme formater som FROM_DATE (påkrævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filter for kun at inspicere tabeller, der indeholder den angivne substring i deres navne.
- `--enable_notification`, `-en`: Muliggør afsendelse af notifikationer i tilfælde af alerts.
- `--bypass-backend`, `-bb`: Bypass backend og kør inspektion direkte fra CLI (til testformål kun!).

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For at inspicere kun en specifik tabel og tvinge genberegning af predictioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommando er nyttig til at generere opdaterede profiler og predictioner, overvåge dataintegritet og styre alarmsystemer inden for en specificeret projekttidsramme.

### inspect-async

Kommandoen `inspect-async` i ***digna*** CLI bruges til at oprette profiler, predictioner og trafiklyssystem-data for en eller flere datakilder inden for et specificeret projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode. I modsætning til `inspect` venter denne kommando ikke på inspektionens færdiggørelse.
I stedet returnerer den request-id for den indsendte inspektionsanmodning. For at forespørge inspektionens fremskridt, brug kommandoen `inspect-status`.

#### Kommando brug

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenter
  
- **PROJECT_NAME**: Navnet på projektet, der skal inspiceres (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** til at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og tidspunkt for data-inspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og tidspunkt for data-inspektionen, med samme formater som FROM_DATE (påkrævet).
  
#### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filter for kun at inspicere tabeller, der indeholder den angivne substring i deres navne.
- `--enable_notification`, `-en`: Muliggør afsendelse af notifikationer i tilfælde af alerts.

  
#### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Kommandoen `inspect-status` i ***digna*** CLI bruges til at tjekke fremskridtet for en asynkron inspektion baseret på request-ID.

#### Kommando brug

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id returneret af `inspect-async` kommandoen 
  
#### Eksempel
  
For at tjekke fremskridtet for en inspektion med request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Kommandoen `inspect-cancel` i ***digna*** CLI bruges til at annullere inspektioner baseret på request-id eller kan bruges til at annullere alle aktuelle anmodninger.

#### Kommando brug

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenter
  
- **REQUEST_ID**: Request-id returneret af `inspect-async` kommandoen 
  
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

Kommandoen `export-ds` i ***digna*** CLI bruges til at lave en eksport af datakilder fra ***digna*** repositoryet. Som standard eksporteres alle datakilder fra et givet projekt.

#### Kommando brug
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på projektet, hvorfra datakilderne eksporteres.

#### Options

- `--table_name`, `-tn`: Eksporter en bestemt datakilde fra et projekt.
- `--exportfile`, `-ef`: Angiv filnavnet for eksporten.
    
#### Eksempel
  
For at eksportere alle datakilder fra projektet med navnet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Denne kommando eksporterer alle datakilder fra `ProjectA` som et JSON-dokument, der kan importeres til et andet projekt eller ***digna*** repository.

### import-ds

Kommandoen `import-ds` i ***digna*** CLI bruges til at importere datakilder til et målprojekt og skabe en importrapport.

#### Kommando brug
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på projektet, hvortil datakilderne importeres.
- **EXPORT_FILE**: Filnavnet på datakilde-eksporten, der skal importeres.

#### Options

- `--output-file`, `-o`: Fil til at gemme importrapporten (hvis ikke angivet, udskrives den i terminalen i tabelform).
- `--output-format`, `-f`: Format til at gemme importrapporten (json, csv).
    
#### Eksempel
  
For at importere alle datakilder fra eksportfilen `my_export.json` ind i `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen vil denne kommando også vise en rapport over importerede og sprundne objekter. Kun nye datakilder vil blive importeret til `ProjectB`. For at finde ud af, hvilke objekter der ville blive importeret og sprunget over, kan du bruge kommandoen `plan-import-ds`.

### plan-import-ds

Kommandoen `plan-import-ds` i ***digna*** CLI bruges til at analysere en eksportfil i forhold til et målprojekt og skabe en importplan/rapport over, hvad der ville blive importeret eller sprunget over.

#### Kommando brug
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenter
- **PROJECT_NAME**: Navnet på projektet, hvortil datakilderne ville blive importeret.
- **EXPORT_FILE**: Filnavnet på datakilde-eksporten, der skal analyseres før import.

#### Options

- `--output-file`, `-o`: Fil til at gemme importrapporten (hvis ikke angivet, udskrives den i terminalen i tabelform).
- `--output-format`, `-f`: Format til at gemme importrapporten (json, csv).
    
#### Eksempel
  
For at tjekke, hvilke datakilder der ville blive importeret, og hvilke der ville blive sprunget over fra eksportfilen `my_export.json`, når den importeres ind i `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Denne kommando viser kun en importplan over objekter, der ville blive importeret og sprunget over.