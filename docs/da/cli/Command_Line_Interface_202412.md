---
title: digna CLI Reference 2024.12 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.12. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, and more.
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Denne side dokumenterer det fulde sæt kommandoer, der er tilgængelige i ***digna*** CLI-udgivelsen **2024.12**, inklusive brugseksempler og muligheder.

---


**2024-12-09**


---

## CLI-grundlæggende

---

## Brug af `help`-optionen

`--help`-optionen giver information om tilgængelige kommandoer og deres anvendelse. Der er to hovedmåder at bruge denne option på:

1. **Visning af generel hjælp:**
   
    Brug --help umiddelbart efter nøgleordet ***digna***cl  
   ```bash
   dignacli --help
   ```

3.  **Hjælp til specifikke kommandoer:**  
  
    For detaljeret information om en specifik kommando, tilføj `--help` til den pågældende kommando.
    For eksempel, for at få hjælp til `add-user`-kommandoen, kør:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommando beskrivelse:** Giver en detaljeret beskrivelse af, hvad kommandoen gør.  
     - **Syntax:** Viser den præcise syntax, inklusive påkrævede og valgfrie argumenter.  
     - **Options:** Angiver eventuelle options specifikke for kommandoen, sammen med deres forklaringer.  
     - **Eksempler:** Viser eksempler på, hvordan kommandoen kan udføres effektivt.

  
## Brug af `check-repo-connection`-kommandoen

`check-repo-connection`-kommandoen er et værktøj i ***digna*** CLI, designet til at teste forbindelsen og adgangen til et angivet ***digna***-repository. Denne kommando sikrer, at CLI'en kan interagere med repository'et.
      
### Kommando anvendelse
```bash
dignacli check-repo-connection
```

Ved succesfuld udførelse giver kommandoen en bekræftelse af forbindelsen samt detaljer om repository'et: Repository-version, Host, Database og Schema.  
  
Hvis repository-forbindelsen ikke lykkes, kontroller da config.toml-filen for korrekt konfiguration.

## Brug af `version`-kommandoen

For at kontrollere den installerede version af *dignacli*, brug --version-optionen.  
  
### Kommando anvendelse
```bash
dignacli --version
```
  
### Eksempeloutput
```bash
dignacli version 2024.12
```

## Brug af logningsmuligheder
  
Som standard er konsoloutputtet fra ***digna***-kommandoer designet til at være minimalistisk. De fleste kommandoer tilbyder mulighed for at give yderligere information ved hjælp af følgende options:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” og ”debug” definerer detaljeringsgraden, mens ”logfile”-skiftet tillader at omdirigere outputtet til en fil i stedet for konsolvinduet.

# Brugeradministration

## Brug af `add-user`-kommandoen
  
`add-user`-kommandoen i ***digna*** CLI bruges til at tilføje en ny bruger til ***digna***-systemet.
  
### Kommando anvendelse
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenter

- **USER_NAME**: Brugernavnet for den nye bruger (påkrævet).
- **USER_FULL_NAME**: Den nye brugers fulde navn (påkrævet).
- **USER_PASSWORD**: Adgangskoden for den nye bruger (påkrævet).

### Options

- `--is_superuser`, `-su`: Flag for at angive, at den nye bruger er administrator.
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerkontoen i formatet `YYYY-MM-DD HH:MI:SS`. Hvis ikke angivet, har kontoen ingen udløbsdato.

### Eksempel

For at tilføje en ny bruger med brugernavn `jdoe`, fuldt navn `John Doe` og adgangskode `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
For at tilføje en ny bruger og sætte en udløbsdato for kontoen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Brug af `delete-user`-kommandoen
  
`delete-user`-kommandoen i ***digna*** CLI bruges til at fjerne en eksisterende bruger fra ***digna***-systemet.
  
### Kommando anvendelse
```bash
dignacli delete-user USER_NAME
```
  
### Argumenter
- **USER_NAME**: Brugernavnet på den bruger, der skal slettes (påkrævet). Dette er det eneste argument, som kommandoen kræver.

### Eksempel
```bash
dignacli delete-user jdoe
```
  
Udførelse af denne kommando fjerner brugeren `jdoe` fra ***digna***-systemet, inddrager deres adgang og sletter deres tilknyttede data og tilladelser fra repository'et.

## Brug af `modify-user`-kommandoen

`modify-user`-kommandoen i ***digna*** CLI bruges til at opdatere oplysningerne for en eksisterende bruger i ***digna***-systemet.

### Kommando anvendelse
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenter
  
- **USER_NAME**: Brugernavnet på den bruger, der skal ændres (påkrævet).
- **USER_FULL_NAME**: Det nye fulde navn for brugeren (påkrævet).
  
### Options  
  
- `--is_superuser`, `-su`: Sætter brugeren som superbruger og giver forhøjede privilegier. Dette flag kræver ikke en værdi.  
- `--valid_until`, `-vu`: Sætter en udløbsdato for brugerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angivet, forbliver kontoen gyldig på ubestemt tid.  
  
### Eksempel
  
For at ændre fulde navn for brugeren `jdoe` til “Johnathan Doe” og sætte brugeren som superbruger:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Brug af `modify-user-pwd`-kommandoen
  
`modify-user-pwd`-kommandoen i ***digna*** CLI bruges til at ændre adgangskoden for en eksisterende bruger i ***digna***-systemet.
  
### Kommando anvendelse
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenter
  
- **USER_NAME**: Brugernavnet for den bruger, hvis adgangskode skal ændres (påkrævet).
- **USER_PWD**: Den nye adgangskode for brugeren (påkrævet).
  
### Eksempel
  
For at ændre adgangskoden for brugeren `jdoe` til `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Brug af `list-users`-kommandoen

`list-users`-kommandoen i ***digna*** CLI viser en liste over alle brugere registreret i ***digna***-systemet.

### Kommando anvendelse

```bash
dignacli list-users
```

Udførelse af denne kommando i ***digna*** CLI vil forbinde til ***digna***-repository'et og liste alle brugere med deres ID, brugernavn, fulde navn, superbruger-status og udløbstidsstempler.

# Repository-administration

### Brug af `upgrade-repo`-kommandoen
  
`upgrade-repo`-kommandoen i ***digna*** CLI bruges til at opgradere eller initialisere ***digna***-repository'et. Denne kommando er essentiel for at anvende opdateringer eller opsætte repository-infrastrukturen første gang.
  
### Kommando anvendelse

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s`: Når denne er aktiveret, kører kommandoen i simuleringsmode, som udskriver de SQL-kommandoer, der ville blive udført, men som ikke rent faktisk udfører dem. Dette er nyttigt for at få et preview af ændringer uden at foretage ændringer i repository'et.  

  
### Eksempel
  
For at opgradere ***digna***-repository'et kan du køre kommandoen uden nogen options:
  
```bash
dignacli upgrade-repo
```  
For at køre opgraderingen i simuleringsmode (for at se SQL-kommandoerne uden at anvende dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Denne kommando er afgørende for at vedligeholde ***digna***-systemet og sikre, at databaseskemaet og andre repository-komponenter er opdaterede med den nyeste softwareversion.

## Brug af `encrypt`-kommandoen
  
`encrypt`-kommandoen i ***digna*** CLI bruges til at kryptere en adgangskode.
  
### Kommando anvendelse
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenter
- **PASSWORD**: Den adgangskode, der skal krypteres (påkrævet).
  
### Eksempel
  
For at kryptere en adgangskode skal du angive adgangskoden som et argument.   
For eksempel, for at kryptere adgangskoden `mypassword123`, ville du bruge:
```bash
dignacli encrypt mypassword123
```
Denne kommando udskriver den krypterede version af den angivne adgangskode, som derefter kan bruges i sikre sammenhænge. Hvis adgangskodeargumentet ikke angives, vil CLI'en vise en fejl, der angiver det manglende argument.

## Brug af `generate-key`-kommandoen
  
`generate-key`-kommandoen bruges til at generere en Fernet-nøgle, som er nødvendig for at sikre adgangskoder, der gemmes i ***digna***-repository'et.
  
### Kommando anvendelse
```bash
dignacli generate-key
```
  
# Datahåndtering

## Brug af `clean-up`-kommandoen

`clean-up`-kommandoen i ***digna*** CLI bruges til at fjerne profiler, predictioner og data fra Traffic Light System for en eller flere datakilder inden for et angivet projekt. Denne kommando er essentiel for data lifecycle-håndtering og hjælper med at opretholde et organiseret og effektivt data-miljø ved at rydde forældede eller unødvendige data.

### Kommando anvendelse

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, hvorfra data skal fjernes (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tidspunkt for datarensningen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tidspunkt for datarensningen, med samme formater som FROM_DATE (påkrævet).
  
### Options
  
- `--table-name`, `-tn`: Begrænser clean-up-operationen til en specifik tabel inden for projektet.
- `--table-filter`, `-tf`: Filtrerer for kun at begrænse clean-up til tabeller, der indeholder den angivne delstreng i deres navne.
- `--timing`, `-tm`: Viser varigheden af clean-up-processen efter fuldførelse.
- `--help`: Viser hjælpeinformation for clean-up-kommandoen og afslutter.
  
### Eksempel
  
For at fjerne data fra projektet ProjectA mellem 1. januar 2023 og 30. juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
For kun at fjerne data fra en specifik tabel ved navn `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Denne kommando hjælper med at styre datalagring og sikre, at repository'et kun indeholder relevant information.

## Brug af `inspect`-kommandoen

`inspect`-kommandoen i ***digna*** CLI bruges til at oprette profiler, predictioner og Traffic Light System-data for en eller flere datakilder inden for et angivet projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode.

### Kommando anvendelse

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, som data skal inspiceres for (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende kommandoen.
- **FROM_DATE**: Startdato og -tidspunkt for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S, eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tidspunkt for datainspektionen, med samme formater som FROM_DATE (påkrævet).
  
### Options

- `--table-name`, `-tn`: Begrænser inspektionen til en specifik tabel i projektet.
- `--table-filter`, `-tf`: Filtrerer for kun at inspicere tabeller, der indeholder den angivne delstreng i deres navne.
- `--do-profile`: Tvinger genindsamling af profiler. Standard er do-profile.
- `--no-do-profile`: Forhindrer genindsamling af profiler.
- `--do-prediction`: Tvinger genberegning af predictioner. Standard er do-prediction.
- `--no-do-prediction`: Forhindrer genberegning af predictioner.
- `--do-alert-status`: Tvinger genberegning af alarmstatusser. Standard er do-alert-status.
- `--no-do-alert-status`: Forhindrer genberegning af alarmstatusser.
- `--iterative`: Tvinger inspektion af en periode ved hjælp af daglige iterationer. Standard er iterative.
- `--no-iterative`: Tvinger inspektion af hele perioden på én gang.
- `--timing`, `-tm`: Viser varigheden af inspektionsprocessen efter fuldførelse.
  
### Eksempel
  
For at inspicere data for projektet `ProjectA` fra 1. januar 2024 til 31. januar 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
For kun at inspicere en specifik tabel og tvinge genberegning af predictioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Denne kommando er nyttig til at generere opdaterede profiler og predictioner, overvåge dataintegritet og administrere alarmsystemer inden for en specificeret projekt-tidsramme.

## Brug af `tls-status`-kommandoen

`tls-status`-kommandoen i ***digna*** CLI bruges til at forespørge status for Traffic Light System (TLS) for en specifik tabel inden for et projekt på en given dato. Traffic Light System giver indsigt i dataens sundhed og kvalitet og angiver eventuelle problemer eller alarmer, der kan kræve opmærksomhed.
  
### Kommando anvendelse
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenter
  
- **PROJECT_NAME**: Navnet på det projekt, som TLS-status forespørges for (påkrævet).
- **TABLE_NAME**: Den specifikke tabel i projektet, som TLS-status ønskes for (påkrævet).
- **DATE**: Datoen, som TLS-status forespørges for, typisk i formatet %Y-%m-%d (påkrævet).
  
### Eksempel
  
For at tjekke TLS-status for en tabel ved navn UserData i projektet ProjectA den 1. juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Denne kommando hjælper brugere med at overvåge og vedligeholde datakvalitet ved at levere en klar og handlingsorienteret statusrapport baseret på foruddefinerede kriterier.

## Brug af `list-projects`-kommandoen
  
`list-projects`-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige projekter i ***digna***-systemet.
  
### Kommando anvendelse
  
```bash
dignacli list-projects
```

Denne kommando er særlig nyttig for administratorer og brugere, der administrerer flere projekter, da den giver et hurtigt overblik over de tilgængelige projekter i ***digna***-repository'et.

## Brug af `list-ds`-kommandoen

`list-ds`-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige datakilder inden for et angivet projekt. Denne kommando er nyttig for at få overblik over de dataressourcer, der er tilgængelige til analyse og administration i ***digna***-systemet.

### Kommando anvendelse
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenter
- **PROJECT_NAME**: Navnet på det projekt, som datakilderne listes for (påkrævet).
  
### Eksempel
  
For at liste alle datakilder i projektet med navnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Denne kommando giver brugerne et overblik over de datakilder, der er tilgængelige i et projekt, og hjælper dem med bedre at navigere og administrere datalandskabet.