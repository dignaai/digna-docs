---
title: digna CLI Reference 2024.09 – Kommandoer & Eksempler | digna Dokumentation
description: Fuld reference for digna CLI-udgivelsen 2024.09. Lær hvordan man administrerer brugere, repositories og data med kommandoer som add-user, check-repo-connection, upgrade-repo, inspect, tls-status og flere.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basics

---

###   help

Optionen --help giver information om tilgængelige kommandoer og deres brug. Der er to hovedmåder at bruge denne option på:

1. **Visning af generel hjælp:**
   
    Brug –help umiddelbart efter nøgleordet ***digna***cl  
   bash
   dignacli --help

3.  **Få hjælp til specifikke kommandoer:**  
  
    For detaljeret information om en specifik kommando, tilføj --help til den pågældende kommando.
    For eksempel, for at få hjælp til add-user-kommandoen, kør:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Command Description:** Giver en detaljeret beskrivelse af hvad kommandoen gør.  
     - **Syntax:** Viser den præcise syntaks, inklusiv nødvendige og valgfrie argumenter.  
     - **Options:** Lister eventuelle optioner specifikke for kommandoen, sammen med deres forklaringer.  
     - **Examples:** Giver eksempler på hvordan kommandoen kan køres effektivt.

  
###   check-repo-connection

check-repo-connection-kommandoen er et værktøj i ***digna*** CLI-værktøjet designet til at teste forbindelsen og adgangen til et specificeret ***digna*** repository. Denne kommando sikrer, at CLI'en kan interagere med repository'et.
      
##### Command Usage
bash
dignacli check-repo-connection


Ved succesfuld udførelse udskriver kommandoen en bekræftelse af forbindelsen samt detaljer om repository'et: Repository version, Host, Database og Schema.  
  
Hvis repository-forbindelsen ikke lykkes, så tjek config.toml-filen for korrekte konfigurationsindstillinger.

###   version

For at tjekke den installerede version af *dignacli*, brug optionen --version.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


###   logging options
  
Som standard er konsoloutputtet fra ***digna***-kommandoerne designet til at være minimalistisk. De fleste kommandoer tilbyder muligheden for at give yderligere information ved hjælp af følgende optioner:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” og “debug” definerer detaljeniveauet, mens “logfile”-skiftet tillader at omdirigere outputtet til en fil i stedet for konsolvinduet.

## User Management

###   add-user
  
add-user-kommandoen i ***digna*** CLI bruges til at tilføje en ny bruger til ***digna*** systemet
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Brugernavnet for den nye bruger (påkrævet).
- **USER_FULL_NAME**: Den nye brugers fulde navn (påkrævet).
- **USER_PASSWORD**: Adgangskoden for den nye bruger (påkrævet).

#### Options

- --is_superuser, -su: Flag for at udpege den nye bruger som admin.
- --valid_until, -vu: Sætter en udløbsdato for brugerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke sat, har kontoen ingen udløbsdato.

#### Example

For at tilføje en ny bruger med brugernavn jdoe, fulde navn John Doe og adgangskode password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
For at tilføje en ny bruger og sætte en udløbsdato for kontoen:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user-kommandoen i ***digna*** CLI bruges til at fjerne en eksisterende bruger fra ***digna*** systemet.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: Brugernavnet for den bruger, der skal slettes (påkrævet). Dette er det eneste argument, der kræves af kommandoen.

#### Example
bash
dignacli delete-user jdoe

  
Kørslen af denne kommando vil fjerne brugeren jdoe fra ***digna*** systemet, fratage deres adgang og slette deres tilknyttede data og rettigheder i repository'et.

###   modify-user

modify-user-kommandoen i ***digna*** CLI bruges til at opdatere detaljer for en eksisterende bruger i ***digna*** systemet.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: Brugernavnet for den bruger, der skal ændres (påkrævet).
- **USER_FULL_NAME**: Det nye fulde navn for brugeren (påkrævet).
  
#### Options  
  
- --is_superuser, -su: Sætter brugeren som superuser og giver forhøjede rettigheder. Dette flag kræver ingen værdi.  
- --valid_until, -vu: Sætter en udløbsdato for brugerkontoen i formatet YYYY-MM-DD HH:MI:SS. Hvis ikke angivet, forbliver kontoen gyldig uden tidsbegrænsning.  
  
#### Example
  
For at ændre det fulde navn for brugeren jdoe til “Johnathan Doe” og sætte brugeren som superuser:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd-kommandoen i ***digna*** CLI bruges til at ændre adgangskoden for en eksisterende bruger i ***digna*** systemet.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: Brugernavnet for den bruger, hvis adgangskode skal ændres (påkrævet).
- **USER_PWD**: Den nye adgangskode for brugeren (påkrævet).
  
#### Example
  
For at ændre adgangskoden for brugeren jdoe til newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users-kommandoen i ***digna*** CLI viser en liste over alle brugere registreret i ***digna*** systemet.

##### Command Usage

bash
dignacli list-users


Kørsel af denne kommando i ***digna*** CLI vil forbinde til ***digna*** repository'et og liste alle brugere, vise deres ID, brugernavn, fulde navn, superuser-status og udløbstidsstempler.

# Repository Management

###   upgrade-repo
  
upgrade-repo-kommandoen i ***digna*** CLI bruges til at opgradere eller initialisere ***digna*** repository'et. Denne kommando er væsentlig for at anvende opdateringer eller sætte repository-infrastrukturen op for første gang.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Når aktiveret, kører denne option kommandoen i simulationsmode, som printer de SQL-udtryk der ville blive kørt, men udfører dem ikke. Dette er nyttigt til at forudse ændringer uden at foretage modifikationer i repository'et.  

  
#### Example
  
For at opgradere ***digna*** repository'et kan du køre kommandoen uden nogen optioner:
  
bash
dignacli upgrade-repo
  
For at køre opgraderingen i simulationsmode (for at se SQL-udtrykkene uden at anvende dem):
  
bash
dignacli upgrade-repo --simulation-mode

  
Denne kommando er afgørende for vedligehold af ***digna*** systemet og sikrer, at databaseskemaet og andre repository-komponenter er opdateret til den nyeste version af softwaren.

###   encrypt
  
encrypt-kommandoen i ***digna*** CLI bruges til at kryptere en adgangskode.
  
#### Command Usage
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD**: Den adgangskode som skal krypteres (påkrævet).
  
#### Example
  
For at kryptere en adgangskode, skal du angive adgangskoden som et argument.   
For eksempel, for at kryptere adgangskoden mypassword123, ville du bruge:
bash
dignacli encrypt mypassword123

Denne kommando udskriver den krypterede version af den angivne adgangskode, som derefter kan bruges i sikre sammenhænge. Hvis adgangskodeargumentet ikke er angivet, vil CLI'en vise en fejl der indikerer det manglende argument.

###   generate-key
  
generate-key-kommandoen bruges til at generere en Fernet-nøgle, som er nødvendig for at sikre adgangskoder gemt i ***digna*** repository'et.
  
#### Command Usage
bash
dignacli generate-key

  
## Data Management

###   clean-up

clean-up-kommandoen i ***digna*** CLI bruges til at fjerne profiler, predictioner og Traffic Light System-data for én eller flere datakilder inden for et specificeret projekt. Denne kommando er vigtig for data lifecycle management og hjælper med at holde et organiseret og effektivt data-miljø ved at rydde forældede eller unødvendige data.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Navnet på det projekt, hvorfra data skal fjernes (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og -tid for datafjernelsen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tid for datafjernelsen, i samme formater som FROM_DATE (påkrævet).
  
#### Options
  
- --table-name, -tn: Begrænser clean-up-operationen til en specifik tabel inden for projektet.
- --table-filter, -tf: Filtrerer for at begrænse clean-up til tabeller, der indeholder den angivne substring i deres navne.
- --timing, -tm: Viser tidsforbruget for clean-up-processen efter afslutning.
- --help: Viser hjælpeinformation for clean-up-kommandoen og afslutter.
  
#### Example
  
For at fjerne data fra projektet ProjectA mellem 1. januar 2023 og 30. juni 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
For kun at fjerne data fra en specifik tabel med navnet Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Denne kommando hjælper med at administrere datalagring og sikrer, at repository'et kun indeholder relevant information.

###   inspect

inspect-kommandoen i ***digna*** CLI bruges til at oprette profiler, predictioner og Traffic Light System-data for én eller flere datakilder inden for et specificeret projekt. Denne kommando hjælper med at analysere og overvåge data over en defineret periode.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Navnet på det projekt, der skal inspiceres (påkrævet). Brug af nøgleordet all-projects i dette argument instruerer ***digna*** om at iterere over alle eksisterende projekter og anvende denne kommando.
- **FROM_DATE**: Startdato og -tid for datainspektionen. Acceptable formater inkluderer %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (påkrævet).
- **TO_DATE**: Slutdato og -tid for datainspektionen, i samme formater som FROM_DATE (påkrævet).
  
#### Options

- --table-name, -tn: Begrænser inspektionen til en specifik tabel inden for projektet.
- --table-filter, -tf: Filtrerer for kun at inspicere tabeller, der indeholder den angivne substring i deres navne.
- --force-profile: Tvinger genindsamling af profiler. Standard er force-profile.
- --no-force-profile: Forhindrer genindsamling af profiler.
- --force-prediction: Tvinger genberegning af predictioner. Standard er force-prediction.
- --no-force-prediction: Forhindrer genberegning af predictioner.
- --force-alert-status: Tvinger genberegning af alert-statusser. Standard er force-alert-status.
- --no-force-alert-status: Forhindrer genberegning af alert-statusser.
- --timing, -tm: Viser varigheden af inspektionsprocessen efter afslutning.
- --alert-notification, -an: Sender alert-notifikationer til tilmeldte kanaler.
  
#### Example
  
For at inspicere data for projektet ProjectA fra 1. januar 2024 til 31. januar 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
For kun at inspicere en specifik tabel og tvinge genberegning af predictioner:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Denne kommando er nyttig til at generere opdaterede profiler og predictioner, overvåge dataintegritet og administrere alert-systemet inden for et specificeret projektinterval.

###   tls-status

tls-status-kommandoen i ***digna*** CLI bruges til at forespørge status for Traffic Light System (TLS) for en specifik tabel inden for et projekt på en given dato. Traffic Light System giver indsigt i dataenes sundhed og kvalitet og indikerer eventuelle problemer eller alerts, der kræver opmærksomhed.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Navnet på det projekt, som TLS-status forespørges for (påkrævet).
- **TABLE_NAME**: Den specifikke tabel inden for projektet, som TLS-status ønskes for (påkrævet).
- **DATE**: Datoen, som TLS-status forespørges for, typisk i formatet %Y-%m-%d (påkrævet).
  
#### Example
  
For at tjekke TLS-status for en tabel ved navn UserData i projektet ProjectA den 1. juli 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Denne kommando hjælper brugere med at overvåge og vedligeholde datakvaliteten ved at give en klar og handlekraftig statusrapport baseret på foruddefinerede kriterier.

###   list-projects
  
list-projects-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige projekter i ***digna*** systemet.
  
#### Command Usage
  
bash
dignacli list-projects


Denne kommando er især nyttig for administratorer og brugere, der administrerer flere projekter, da den giver et hurtigt overblik over de tilgængelige projekter i ***digna*** repository'et.

###   list-ds

list-ds-kommandoen i ***digna*** CLI bruges til at vise en liste over alle tilgængelige datakilder inden for et specificeret projekt. Denne kommando er nyttig for at forstå de dataressourcer, der er tilgængelige til analyse og administration i ***digna*** systemet.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Navnet på det projekt, hvis datakilder listes (påkrævet).
  
#### Example
  
For at liste alle datakilder i projektet med navnet ProjectA:
  
bash
dignacli list-ds ProjectA

  
Denne kommando giver brugere et overblik over de datakilder, der er tilgængelige i et projekt, og hjælper dem med bedre at navigere og administrere datalandskabet.