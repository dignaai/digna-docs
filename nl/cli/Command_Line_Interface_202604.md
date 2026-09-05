# digna CLI Reference 2026.04
**2026-04-08**

Deze pagina documenteert de volledige set commando's die beschikbaar zijn in de ***digna*** CLI release **2026.04**, inclusief gebruiksvoorbeelden en opties.

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
      
     - **Omschrijving van het commando:** Geeft een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntax:** Toont de exacte syntax, inclusief vereiste en optionele argumenten.  
     - **Opties:** Geeft alle opties specifiek voor het commando weer, met hun uitleg.  
     - **Voorbeelden:** Biedt voorbeelden van hoe het commando effectief uitgevoerd kan worden.

### check-config

Het commando check-config is een hulpprogramma binnen de ***digna*** CLI die is ontworpen om de configuratie van ***digna*** te testen. Dit commando controleert of de ***digna***-componenten de benodigde configuratie-elementen in de config.toml kunnen vinden.

#### Opties

- `--configpath`, `-cp`: Bestand of directory die de configuratie bevat. Als deze wordt weggelaten, wordt ../config.toml gebruikt.
      
#### Gebruik van het commando
```bash
dignacli check-config
```

Na succesvolle uitvoering geeft het commando een bevestiging van de volledigheid van de configuratie.  
  
Als de configuratie incompleet lijkt, worden de ontbrekende configuratie-elementen opgesomd.

  
### check-repo-connection

Het commando check-repo-connection is een hulpprogramma binnen de ***digna*** CLI dat is ontworpen om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando zorgt ervoor dat de CLI met de repository kan communiceren.
      
#### Gebruik van het commando
```bash
dignacli check-repo-connection
```

Na succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repository versie, Host, Database en Schema.  
  
Als de repository-verbinding niet succesvol is, controleer dan het config.toml bestand op correcte configuratie-instellingen.


### version

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik de --version optie.  
  
#### Gebruik van het commando
```bash
dignacli --version
```
  
#### Voorbeeldoutput
```bash
dignacli version 2026.04
```

### logging options
  
Standaard is de console-uitvoer van de ***digna*** commando's minimalistisch. De meeste commando's bieden de mogelijkheid om extra informatie te tonen met de volgende opties:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” en “debug” bepalen het detailniveau, terwijl de “logfile” schakelaar toestaat de uitvoer naar een bestand te sturen in plaats van naar het console-venster.

## Gebruikersbeheer

### add-user
  
Het commando add-user in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem.
  
#### Gebruik van het commando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenten

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (vereist).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (vereist).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (vereist).

#### Opties

- `--is_superuser`, `-su`: Vlag om de nieuwe gebruiker als beheerder aan te wijzen.
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat `YYYY-MM-DD HH:MI:SS`. Als deze niet is ingesteld, heeft het account geen vervaldatum.

#### Voorbeeld

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
  
#### Gebruik van het commando
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenten
- **USER_NAME**: De gebruikersnaam van de gebruiker die verwijderd moet worden (vereist). Dit is het enige vereiste argument voor het commando.

#### Voorbeeld
```bash
dignacli delete-user jdoe
```
  
Door dit commando uit te voeren wordt de gebruiker `jdoe` verwijderd uit het ***digna*** systeem, wordt hun toegang ingetrokken en worden bijbehorende gegevens en rechten uit de repository verwijderd.

### modify-user

Het `modify-user` commando in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker in het ***digna*** systeem bij te werken.

#### Gebruik van het commando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker die gewijzigd moet worden (vereist).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (vereist).
  
#### Opties  
  
- `--is_superuser`, `-su`: Zet de gebruiker als superuser en geeft verhoogde privileges. Deze vlag vereist geen waarde.  
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat YYYY-MM-DD HH:MI:SS. Als deze niet wordt opgegeven, blijft het account onbeperkt geldig.  
  
#### Voorbeeld
  
Om de volledige naam van de gebruiker `jdoe` te wijzigen in “Johnathan Doe” en de gebruiker als superuser in te stellen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Het `modify-user-pwd` commando in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker in het ***digna*** systeem te wijzigen.
  
#### Gebruik van het commando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker van wie het wachtwoord gewijzigd moet worden (vereist).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (vereist).
  
#### Voorbeeld
  
Om het wachtwoord van de gebruiker `jdoe` te veranderen naar `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Het `list-users` commando in de ***digna*** CLI toont een lijst van alle gebruikers die geregistreerd zijn in het ***digna*** systeem.

#### Gebruik van het commando

```bash
dignacli list-users
```

Bij uitvoering maakt dit commando verbinding met de ***digna*** repository en toont alle gebruikers, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaldatumstempels.

## Repositorybeheer

### upgrade-repo
  
Het `upgrade-repo` commando in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel voor het toepassen van updates of het opzetten van de repository-infrastructuur voor de eerste keer.
  
#### Gebruik van het commando

```bash
dignacli upgrade-repo [options]
```
  
#### Opties
  
- `--simulation-mode`, `-s`: Wanneer ingeschakeld voert dit de opdracht in simulatiemodus uit, waarbij de SQL-statements die uitgevoerd zouden worden worden weergegeven maar niet daadwerkelijk uitgevoerd. Dit is handig om wijzigingen vooraf te kunnen beoordelen zonder iets in de repository te wijzigen.  

  
#### Voorbeeld
  
Om de ***digna*** repository te upgraden, kunt u het commando zonder opties uitvoeren:
  
```bash
dignacli upgrade-repo
```  
Om de upgrade in simulatiemodus uit te voeren (zodat u de SQL-statements ziet zonder ze toe te passen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dit commando is belangrijk voor het onderhoud van het ***digna*** systeem en zorgt ervoor dat het databaseschema en andere repository-componenten up-to-date zijn met de nieuwste versie van de software.

### encrypt
  
Het `encrypt` commando in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
#### Gebruik van het commando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenten
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (vereist).
  
#### Voorbeeld
  
Om een wachtwoord te versleutelen, moet u het wachtwoord als argument meegeven.   
Bijvoorbeeld, om het wachtwoord `mypassword123` te versleutelen, gebruikt u:
```bash
dignacli encrypt mypassword123
```
Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die vervolgens in beveiligde contexten kan worden gebruikt. Als het wachtwoordargument niet wordt opgegeven, zal de CLI een foutmelding tonen over het ontbrekende argument.

### generate-key
  
Het `generate-key` commando wordt gebruikt om een Fernet-sleutel te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
#### Gebruik van het commando
```bash
dignacli generate-key
```
  
## Gegevensbeheer

### clean-up

Het `clean-up` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en data van het traffic light-systeem te verwijderen voor één of meerdere gegevensbronnen binnen een opgegeven project. Dit commando is essentieel voor lifecycle-management van gegevens en helpt een georganiseerde en efficiënte dataomgeving te behouden door verouderde of onnodige data te verwijderen.

#### Gebruik van het commando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waaruit gegevens verwijderd moeten worden (vereist). Als het sleutelwoord all-projects in dit argument wordt gebruikt, instrueert dit ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van gegevens. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van gegevens, met dezelfde formaten als FROM_DATE (vereist).
  
#### Opties
  
- `--table-name`, `-tn`: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert zodat alleen tabellen die de opgegeven substring in hun naam bevatten worden meegenomen.
- `--timing`, `-tm`: Toont de tijdsduur van het clean-up proces na voltooiing.
- `--help`: Toont helpinformatie voor het clean-up commando en stopt.
  
#### Voorbeeld
  
Om gegevens te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Om alleen gegevens uit een specifieke tabel met de naam `Table1` te verwijderen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dit commando helpt bij het beheren van opslag en zorgt ervoor dat de repository alleen relevante informatie bevat.

### remove-orphans
  
Het `remove-orphans` commando in de ***digna*** CLI wordt gebruikt voor onderhoud in de ***digna*** repository.  
Wanneer een gebruiker projecten of gegevensbronnen verwijdert, blijven profielen en voorspellingen soms in de repository achter. Met dit commando worden dergelijke verweesde rijen uit de repository verwijderd.
  
#### Gebruik van het commando
  
```bash
dignacli list-projects
```

### list-projects
  
Het `list-projects` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
#### Gebruik van het commando
  
```bash
dignacli list-projects
```

Dit commando is vooral nuttig voor beheerders en gebruikers die meerdere projecten beheren en biedt een snel overzicht van de beschikbare projecten in de ***digna*** repository.

### list-ds

Het `list-ds` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare gegevensbronnen binnen een opgegeven project. Dit commando is nuttig om inzicht te krijgen in de data-assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

#### Gebruik van het commando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvan de gegevensbronnen worden opgesomd (vereist).
  
#### Voorbeeld
  
Om alle gegevensbronnen in het project met de naam `ProjectA` te tonen:
  
```bash
dignacli list-ds ProjectA
```
  
Dit commando geeft gebruikers een overzicht van de beschikbare gegevensbronnen in een project, wat helpt bij het navigeren en beheren van het data-landschap.

### inspect

Het `inspect` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en data voor het traffic light-systeem te creëren voor één of meerdere gegevensbronnen binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode. Na voltooiing van de inspectie wordt de waarde van het berekende traffic light-systeem geretourneerd:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Gebruik van het commando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project dat geïnspecteerd moet worden (vereist). Als het sleutelwoord all-projects in dit argument wordt gebruikt, instrueert dit ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de inspectie. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor de inspectie, met dezelfde formaten als FROM_DATE (vereist).
  
#### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert zodat alleen tabellen die de opgegeven substring in hun naam bevatten worden geïnspecteerd.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in bij alerts.
- `--bypass-backend`, `-bb`: Omzeilt de backend en voert de inspectie rechtstreeks vanuit de CLI uit (alleen voor testdoeleinden!).

  
#### Voorbeeld
  
Om gegevens te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Om slechts een specifieke tabel te inspecteren en herberekening van voorspellingen af te dwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dit commando is nuttig voor het genereren van bijgewerkte profielen en voorspellingen, het monitoren van data-integriteit en het beheren van alerts binnen een opgegeven projectperiode.

### inspect-async

Het `inspect-async` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en data voor het traffic light-systeem te creëren voor één of meerdere gegevensbronnen binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode. In tegenstelling tot het `inspect` commando wacht dit commando niet op voltooiing van de inspectie. In plaats daarvan retourneert het de request id voor het ingediende inspectieverzoek. Om de voortgang van het inspectieproces te raadplegen, gebruik het commando `inspect-status`.

#### Gebruik van het commando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project dat geïnspecteerd moet worden (vereist). Als het sleutelwoord all-projects in dit argument wordt gebruikt, instrueert dit ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de inspectie. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor de inspectie, met dezelfde formaten als FROM_DATE (vereist).
  
#### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert zodat alleen tabellen die de opgegeven substring in hun naam bevatten worden geïnspecteerd.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in bij alerts.

  
#### Voorbeeld
  
Om gegevens te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Het `inspect-status` commando in de ***digna*** CLI wordt gebruikt om de voortgang van een asynchrone inspectie te controleren op basis van de request ID.

#### Gebruik van het commando

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenten
  
- **REQUEST_ID**: De request id die door het `inspect-async` commando is geretourneerd 
  
#### Voorbeeld
  
Om de voortgang van een inspectie met request ID 12345 te controleren:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Het `inspect-cancel` commando in de ***digna*** CLI wordt gebruikt om inspecties te annuleren op basis van de request ID of om alle huidige verzoeken te annuleren.

#### Gebruik van het commando

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenten
  
- **REQUEST_ID**: De request id die door het `inspect-async` commando is geretourneerd 
  
#### Voorbeeld
  
Om de inspectie met request ID 12345 te annuleren:
  
```bash
dignacli inspect-cancel 12345
```

Om alle verzoeken die momenteel lopen of in de wachtrij staan te annuleren:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Het `export-ds` commando in de ***digna*** CLI wordt gebruikt om een export van gegevensbronnen uit de ***digna*** repository te maken. Standaard worden alle gegevensbronnen van een bepaald project geëxporteerd.

#### Gebruik van het commando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvan de gegevensbronnen geëxporteerd zullen worden.

#### Opties

- `--table_name`, `-tn`: Exporteer een specifieke gegevensbron uit een project.
- `--exportfile`, `-ef`: Specificeer de bestandsnaam voor de export.
    
#### Voorbeeld
  
Om alle gegevensbronnen uit het project met de naam `ProjectA` te exporteren:
  
```bash
dignacli export-ds ProjectA
```
  
Dit commando exporteert alle gegevensbronnen uit `ProjectA` als een JSON-document dat geïmporteerd kan worden in een ander project of ***digna*** repository.


### import-ds

Het `import-ds` commando in de ***digna*** CLI wordt gebruikt om gegevensbronnen te importeren in een doelproject en een importrapport te maken.

#### Gebruik van het commando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarin de gegevensbronnen geïmporteerd zullen worden.
- **EXPORT_FILE**: De bestandsnaam van de gegevensbronnenexport die geïmporteerd moet worden.

#### Opties

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als dit niet is opgegeven, wordt het rapport in tabelvorm naar de terminal geprint).
- `--output-format`, `-f`: Formaat om het importrapport op te slaan (json, csv).
    
#### Voorbeeld
  
Om alle gegevensbronnen uit exportbestand `my_export.json` te importeren in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Na de import zal dit commando ook een rapport tonen van geïmporteerde en overgeslagen objecten. Alleen nieuwe gegevensbronnen worden in `ProjectB` geïmporteerd. Om te zien welke objecten geïmporteerd en welke overgeslagen zouden worden, kunt u het commando `plan-import-ds` gebruiken.

### plan-import-ds

Het `plan-import-ds` commando in de ***digna*** CLI wordt gebruikt om te analyseren welke gegevensbronnen in een doelproject geïmporteerd zouden worden en om een importrapport te maken zonder daadwerkelijk te importeren.

#### Gebruik van het commando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarin de gegevensbronnen geïmporteerd zouden worden.
- **EXPORT_FILE**: De bestandsnaam van de gegevensbronnenexport die geanalyseerd moet worden voorafgaand aan de import.

#### Opties

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als dit niet is opgegeven, wordt het rapport in tabelvorm naar de terminal geprint).
- `--output-format`, `-f`: Formaat om het importrapport op te slaan (json, csv).
    
#### Voorbeeld
  
Om te controleren welke gegevensbronnen geïmporteerd en welke overgeslagen zouden worden uit exportbestand `my_export.json` wanneer dat in `ProjectB` geïmporteerd zou worden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dit commando toont alleen een importplan van objecten die geïmporteerd en overgeslagen zouden worden.