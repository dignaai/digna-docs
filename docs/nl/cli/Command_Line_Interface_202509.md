---
title: digna CLI Reference 2025.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2025.109 Learn how to manage users, repositories, and data with commands such as add-user, check-config, check-repo-connection, inspect, inspect-async, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Deze pagina documenteert de volledige set commando's die beschikbaar zijn in de ***digna*** CLI release **2025.09**, inclusief gebruiksvoorbeelden en opties.

---

## CLI Basics

---

### help
De `--help` optie geeft informatie over beschikbare commando's en hun gebruik. Er zijn twee hoofdmanieren om deze optie te gebruiken:

1. **Algemene help weergeven:**
   
    Gebruik --help direct na het sleutelwoord ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Help voor specifieke commando's opvragen:**  
  
    Voor gedetailleerde informatie over een specifiek commando, voeg `--help` toe aan dat commando.
    Bijvoorbeeld, om hulp te krijgen bij het commando `add-user`, voer uit:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Command Description:** Biedt een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntax:** Toont de exacte syntax, inclusief vereiste en optionele argumenten.  
     - **Options:** Geeft een overzicht van opties specifiek voor het commando, met uitleg.  
     - **Examples:** Voorbeelden van hoe het commando effectief uitgevoerd kan worden.

### check-config

Het check-config commando is een hulpmiddel binnen de ***digna*** CLI om de configuratie van ***digna*** te testen. Dit commando controleert of de ***digna***-componenten de benodigde configuratie-elementen kunnen vinden in config.toml.

#### Options

- `--configpath`, `-cp`: Bestand of directory die de configuratie bevat. Indien weggelaten, wordt ../config.toml gebruikt.
      
#### Command Usage
```bash
dignacli check-config
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de volledigheid van de configuratie.  
  
Als de configuratie incompleet lijkt, worden de ontbrekende configuratie-elementen opgesomd.

  
### check-repo-connection

Het check-repo-connection commando is een hulpmiddel binnen de ***digna*** CLI om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando controleert of de CLI met de repository kan communiceren.
      
#### Command Usage
```bash
dignacli check-repo-connection
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repository version, Host, Database en Schema.  
  
Als de verbinding met de repository niet succesvol is, controleer dan het config.toml bestand op correcte configuratie-instellingen.


### version

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik de --version optie.  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2025.09
```

### logging options
  
Standaard is de console-uitvoer van de ***digna*** commando's minimaal. De meeste commando's bieden de mogelijkheid om extra informatie te tonen, via de volgende opties:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” en “debug” bepalen het detailniveau, terwijl de “logfile” switch het mogelijk maakt de uitvoer naar een bestand te streamen in plaats van naar het consolevenster.

## User Management

### add-user
  
Het add-user commando in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem.
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Arguments

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (verplicht).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (verplicht).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (verplicht).

#### Options

- `--is_superuser`, `-su`: Vlag om de nieuwe gebruiker als admin aan te wijzen.
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat `YYYY-MM-DD HH:MI:SS`. Als dit niet wordt ingesteld, heeft het account geen vervaldatum.

#### Example

Om een nieuwe gebruiker toe te voegen met gebruikersnaam `jdoe`, volledige naam `John Doe` en wachtwoord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Om een nieuwe gebruiker toe te voegen en een vervaldatum voor het account in te stellen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Het `delete-user` commando in de ***digna*** CLI wordt gebruikt om een bestaande gebruiker te verwijderen uit het ***digna*** systeem.
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
#### Arguments
- **USER_NAME**: De gebruikersnaam van de gebruiker die verwijderd moet worden (verplicht). Dit is het enige verplicht argument voor het commando.

#### Example
```bash
dignacli delete-user jdoe
```
  
Het uitvoeren van dit commando verwijdert de gebruiker `jdoe` uit het ***digna*** systeem, intrekking van toegang en het verwijderen van bijbehorende gegevens en permissies uit de repository.

### modify-user

Het `modify-user` commando in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker in het ***digna*** systeem bij te werken.

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Arguments
  
- **USER_NAME**: De gebruikersnaam van de gebruiker die aangepast moet worden (verplicht).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (verplicht).
  
#### Options  
  
- `--is_superuser`, `-su`: Stelt de gebruiker in als superuser, wat verhoogde privileges geeft. Deze vlag vereist geen waarde.  
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat YYYY-MM-DD HH:MI:SS. Als niet opgegeven, blijft het account onbeperkt geldig.  
  
#### Example
  
Om de volledige naam van gebruiker `jdoe` te wijzigen naar “Johnathan Doe” en de gebruiker als superuser in te stellen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Het `modify-user-pwd` commando in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker in het ***digna*** systeem te wijzigen.
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Arguments
  
- **USER_NAME**: De gebruikersnaam van de gebruiker van wie het wachtwoord gewijzigd moet worden (verplicht).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (verplicht).
  
#### Example
  
Om het wachtwoord van gebruiker `jdoe` te wijzigen naar `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Het `list-users` commando in de ***digna*** CLI toont een lijst van alle gebruikers die in het ***digna*** systeem zijn geregistreerd.

#### Command Usage

```bash
dignacli list-users
```

Het uitvoeren van dit commando in de ***digna*** CLI maakt verbinding met de ***digna*** repository en geeft alle gebruikers weer, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaltijdstempels.

## Repository Management

### upgrade-repo
  
Het `upgrade-repo` commando in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel om updates toe te passen of de repository-infrastructuur voor de eerste keer op te zetten.
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Wanneer ingeschakeld draait dit commando in simulatiemodus, waarbij de SQL-statements die uitgevoerd zouden worden worden geprint, maar niet daadwerkelijk uitgevoerd. Dit is handig om wijzigingen te previewen zonder de repository aan te passen.  

  
#### Example
  
Om de ***digna*** repository te upgraden, kan je het commando zonder opties uitvoeren:
  
```bash
dignacli upgrade-repo
```  
Om de upgrade in simulatiemodus uit te voeren (om de SQL-statements te zien zonder ze toe te passen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dit commando is cruciaal voor het onderhoud van het ***digna*** systeem en zorgt ervoor dat het databasemodel en andere repository-componenten up-to-date zijn met de nieuwste versie van de software.

### encrypt
  
Het `encrypt` commando in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (verplicht).
  
#### Example
  
Om een wachtwoord te versleutelen moet je het wachtwoord als argument doorgeven.   
Bijvoorbeeld, om het wachtwoord `mypassword123` te versleutelen, gebruik:
```bash
dignacli encrypt mypassword123
```
Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die vervolgens in veilige contexten gebruikt kan worden. Als het wachtwoordargument niet wordt opgegeven, zal de CLI een foutmelding tonen die het ontbrekende argument aangeeft.

### generate-key
  
Het `generate-key` commando wordt gebruikt om een Fernet key te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Data Management

### clean-up

Het `clean-up` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het traffic light-systeem te verwijderen voor één of meer data sources binnen een opgegeven project. Dit commando is essentieel voor lifecycle management van data en helpt een georganiseerde en efficiënte dataomgeving te behouden door verouderde of onnodige data te verwijderen.

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: De naam van het project waarvan data verwijderd moet worden (verplicht). Het gebruik van het sleutelwoord all-projects in dit argument instrueert ***digna*** om over alle bestaande projecten te itereren en het commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van data. Acceptabele formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van data, volgens dezelfde formaten als FROM_DATE (verplicht).
  
#### Options
  
- `--table-name`, `-tn`: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om de clean-up te beperken tot tabellen die de opgegeven substring in hun naam bevatten.
- `--timing`, `-tm`: Toont de tijdsduur van het clean-up proces na voltooiing.
- `--help`: Toont helpinformatie voor het clean-up commando en stopt.
  
#### Example
  
Om data te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Om alleen data uit een specifieke tabel genaamd `Table1` te verwijderen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dit commando helpt bij het beheren van dataopslag en zorgt ervoor dat de repository alleen relevante informatie bevat.

### remove-orphans
  
Het `remove-orphans` commando in de ***digna*** CLI wordt gebruikt voor onderhoud in de ***digna*** repository.  
Wanneer een gebruiker projecten of data sources verwijdert, blijven de profielen en voorspellingen vaak in de repository achter. Met dit commando worden dergelijke verweesde rijen uit de repository verwijderd.
  
#### Command Usage
  
```bash
dignacli list-projects
```

### list-projects
  
Het `list-projects` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
#### Command Usage
  
```bash
dignacli list-projects
```

Dit commando is vooral nuttig voor beheerders en gebruikers die meerdere projecten beheren en biedt een snel overzicht van de beschikbare projecten in de ***digna*** repository.

### list-ds

Het `list-ds` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare data sources binnen een opgegeven project. Dit commando is nuttig om inzicht te krijgen in de data assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: De naam van het project waarvoor de data sources worden weergegeven (verplicht).
  
#### Example
  
Om alle data sources in het project genaamd `ProjectA` te tonen:
  
```bash
dignacli list-ds ProjectA
```
  
Dit commando geeft gebruikers een overzicht van de data sources die in een project beschikbaar zijn, wat helpt bij het navigeren en beheren van het data-landschap.

### inspect

Het `inspect` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het traffic light-systeem te creëren voor één of meer data sources binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode. Na voltooiing van de inspectie wordt de waarde van het berekende traffic light-systeem geretourneerd:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: De naam van het project dat geïnspecteerd moet worden (verplicht). Het gebruik van het sleutelwoord all-projects in dit argument instrueert ***digna*** om over alle bestaande projecten te itereren en het commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Acceptabele formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, volgens dezelfde formaten als FROM_DATE (verplicht).
  
#### Options

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun naam bevatten.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in bij alerts.
- `--bypass-backend`, `-bb`: Bypass de backend en voer de inspectie direct vanuit de CLI uit (alleen voor testdoeleinden!).

  
#### Example
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Om alleen een specifieke tabel te inspecteren en een herberekening van voorspellingen af te dwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dit commando is nuttig om bijgewerkte profielen en voorspellingen te genereren, de dataintegriteit te monitoren en alerts binnen een opgegeven projectperiode te beheren.

### inspect-async

Het `inspect-async` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het traffic light-systeem te creëren voor één of meer data sources binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode. In tegenstelling tot het `inspect` commando wacht dit niet op voltooiing van de inspectie.  
In plaats daarvan retourneert het de request id voor het ingediende inspectieverzoek. Om de voortgang van het inspectieproces te raadplegen, gebruik je het commando `inspect-status`.

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: De naam van het project dat geïnspecteerd moet worden (verplicht). Het gebruik van het sleutelwoord all-projects in dit argument instrueert ***digna*** om over alle bestaande projecten te itereren en het commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Acceptabele formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, volgens dezelfde formaten als FROM_DATE (verplicht).
  
#### Options

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun naam bevatten.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in bij alerts.

  
#### Example
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Het `inspect-status` commando in de ***digna*** CLI wordt gebruikt om de voortgang van een asynchrone inspectie te controleren op basis van de request ID.

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Arguments
  
- **REQUEST_ID**: De request id die door het `inspect-async` commando is geretourneerd 
  
#### Example
  
Om de voortgang van een inspectie met request ID 12345 te controleren:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Het `inspect-cancel` commando in de ***digna*** CLI wordt gebruikt om inspecties te annuleren op basis van de request ID of om alle huidige verzoeken te annuleren.

#### Command Usage

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Arguments
  
- **REQUEST_ID**: De request id die door het `inspect-async` commando is geretourneerd 
  
#### Example
  
Om de inspectie met request ID 12345 te annuleren:
  
```bash
dignacli inspect-cancel 12345
```

Om alle verzoeken die momenteel draaien of in de wachtrij staan te annuleren:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Het `export-ds` commando in de ***digna*** CLI wordt gebruikt om een export van data sources uit de ***digna*** repository te maken. Standaard worden alle data sources van een opgegeven project geëxporteerd.

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: De naam van het project waarvan de data sources geëxporteerd zullen worden.

#### Options

- `--table_name`, `-tn`: Exporteer een specifieke data source uit een project.
- `--exportfile`, `-ef`: Specificeer de bestandsnaam voor de export.
    
#### Example
  
Om alle data sources van het project met de naam `ProjectA` te exporteren:
  
```bash
dignacli export-ds ProjectA
```
  
Dit commando exporteert alle data sources uit `ProjectA` als een JSON-document dat naar een ander project of ***digna*** repository geïmporteerd kan worden.


### import-ds

Het `import-ds` commando in de ***digna*** CLI wordt gebruikt om data sources te importeren in een doelproject en een importrapport te genereren.

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: De naam van het project waarnaar de data sources geïmporteerd zullen worden.
- **EXPORT_FILE**: De bestandsnaam van de data sources export die geïmporteerd moet worden.

#### Options

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als niet gespecificeerd, wordt het in tabelvorm naar de terminal geschreven).
- `--output-format`, `-f`: Formaat om het importrapport op te slaan (json, csv).
    
#### Example
  
Om alle data sources uit het exportbestand `my_export.json` te importeren in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Na de import toont dit commando ook een rapport van geïmporteerde en overgeslagen objecten. Alleen nieuwe data sources worden in `ProjectB` geïmporteerd. Om te achterhalen welke objecten geïmporteerd en welke overgeslagen zouden worden, kun je het commando `plan-import-ds` gebruiken.

### plan-import-ds

Het `plan-import-ds` commando in de ***digna*** CLI wordt gebruikt om te analyseren welke data sources in een doelproject zouden worden geïmporteerd en om een importrapport te maken zonder daadwerkelijk te importeren.

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: De naam van het project waarnaar de data sources zouden worden geïmporteerd.
- **EXPORT_FILE**: De bestandsnaam van de data sources export die geanalyseerd moet worden vóór de import.

#### Options

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als niet gespecificeerd, wordt het in tabelvorm naar de terminal geschreven).
- `--output-format`, `-f`: Formaat om het importrapport op te slaan (json, csv).
    
#### Example
  
Om te controleren welke data sources geïmporteerd zouden worden en welke overgeslagen uit het exportbestand `my_export.json` wanneer deze in `ProjectB` geïmporteerd zou worden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dit commando toont alleen een importplan van objecten die geïmporteerd en overgeslagen zouden worden.