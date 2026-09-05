# digna CLI Referentie 2026.01
**2026-01-15**

Deze pagina documenteert de volledige set commando's die beschikbaar zijn in de ***digna*** CLI release **2026.01**, inclusief gebruiksvoorbeelden en opties.

---

## CLI Basis

---

### help
De optie `--help` geeft informatie over beschikbare commando's en hun gebruik. Er zijn twee hoofdmanieren om deze optie te gebruiken:

1. **Algemene hulp weergeven:**
   
    Gebruik --help direct achter het woord ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hulp voor specifieke commando's ophalen:**  
  
    Voor gedetailleerde informatie over een specifiek commando voeg je `--help` toe aan dat commando.
    Bijvoorbeeld, om hulp te krijgen bij het commando `add-user`, voer je uit:
     ```bash
     dignacli add-user --help
     ```

     ### uitvoer:
      
     - **Commanodobeschrijving:** Geeft een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntaxis:** Toont de exacte syntaxis, inclusief verplichte en optionele argumenten.  
     - **Opties:** Lijst met opties specifiek voor het commando, met hun uitleg.  
     - **Voorbeelden:** Voorbeelden van hoe het commando effectief uitgevoerd kan worden.

### check-config

Het commando check-config is een hulpprogramma binnen de ***digna*** CLI dat is ontworpen om de configuratie van ***digna*** te testen. Dit commando controleert of de ***digna*** componenten de benodigde configuratie-elementen in de config.toml kunnen vinden.

#### Opties

- `--configpath`, `-cp`: Bestand of directory die de configuratie bevat. Als dit niet is opgegeven, wordt ../config.toml gebruikt.
      
#### Commaando Gebruik
```bash
dignacli check-config
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de volledigheid van de configuratie.  
  
Als de configuratie incompleet lijkt te zijn, worden de ontbrekende configuratie-elementen weergegeven.

  
### check-repo-connection

Het commando check-repo-connection is een hulpprogramma binnen de ***digna*** CLI dat is ontworpen om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando controleert of de CLI met de repository kan communiceren.
      
#### Commaando Gebruik
```bash
dignacli check-repo-connection
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repository versie, Host, Database en Schema.  
  
Als de verbinding met de repository niet succesvol is, controleer dan het config.toml bestand op correcte configuratie-instellingen.


### version

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik je de optie --version.  
  
#### Commaando Gebruik
```bash
dignacli --version
```
  
#### Voorbeeld uitvoer
```bash
dignacli version 2026.01
```

### logging opties
  
Standaard is de console-uitvoer van de ***digna*** commando's minimaal. De meeste commando's bieden de mogelijkheid extra informatie te tonen met de volgende opties:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” en “debug” bepalen het detailniveau, terwijl de “logfile” switch het mogelijk maakt de uitvoer naar een bestand te streamen in plaats van naar het consolevenster.

## Gebruikersbeheer

### add-user
  
Het commando add-user in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem.
  
#### Commaando Gebruik
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenten

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (verplicht).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (verplicht).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (verplicht).

#### Opties

- `--is_superuser`, `-su`: Vlag om de nieuwe gebruiker als beheerder aan te wijzen.
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat `YYYY-MM-DD HH:MI:SS`. Als dit niet wordt ingesteld, heeft het account geen vervaldatum.

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
  
Het commando `delete-user` in de ***digna*** CLI wordt gebruikt om een bestaande gebruiker uit het ***digna*** systeem te verwijderen.
  
#### Commaando Gebruik
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenten
- **USER_NAME**: De gebruikersnaam van de gebruiker die verwijderd moet worden (verplicht). Dit is het enige vereiste argument voor het commando.

#### Voorbeeld
```bash
dignacli delete-user jdoe
```
  
Het uitvoeren van dit commando verwijdert de gebruiker `jdoe` uit het ***digna*** systeem, waarbij hun toegang wordt ingetrokken en de bijbehorende data en machtigingen uit de repository worden verwijderd.

### modify-user

Het commando `modify-user` in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker in het ***digna*** systeem bij te werken.

#### Commaando Gebruik
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker die gewijzigd moet worden (verplicht).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (verplicht).
  
#### Opties  
  
- `--is_superuser`, `-su`: Zet de gebruiker als superuser en geeft verhoogde bevoegdheden. Deze vlag vereist geen waarde.  
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat YYYY-MM-DD HH:MI:SS. Als dit niet wordt opgegeven, blijft het account onbepaald geldig.  
  
#### Voorbeeld
  
Om de volledige naam van de gebruiker `jdoe` te wijzigen in “Johnathan Doe” en de gebruiker als superuser in te stellen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Het commando `modify-user-pwd` in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker in het ***digna*** systeem te wijzigen.
  
#### Commaando Gebruik
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker van wie het wachtwoord gewijzigd moet worden (verplicht).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (verplicht).
  
#### Voorbeeld
  
Om het wachtwoord voor de gebruiker `jdoe` te wijzigen naar `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Het commando `list-users` in de ***digna*** CLI toont een lijst van alle gebruikers die geregistreerd zijn in het ***digna*** systeem.

#### Commaando Gebruik

```bash
dignacli list-users
```

Het uitvoeren van dit commando in de ***digna*** CLI maakt verbinding met de ***digna*** repository en toont alle gebruikers, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaltijdstempels.

## Repositorybeheer

### upgrade-repo
  
Het commando `upgrade-repo` in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel voor het toepassen van updates of het voor het eerst opzetten van de repository-infrastructuur.
  
#### Commaando Gebruik

```bash
dignacli upgrade-repo [options]
```
  
#### Opties
  
- `--simulation-mode`, `-s`: Wanneer ingeschakeld, voert deze optie het commando uit in simulatiemodus, waarbij de SQL-statements die uitgevoerd zouden worden worden afgedrukt, maar niet daadwerkelijk worden uitgevoerd. Dit is nuttig om wijzigingen te bekijken zonder iets aan de repository te wijzigen.  

  
#### Voorbeeld
  
Om de ***digna*** repository te upgraden, kun je het commando zonder opties uitvoeren:
  
```bash
dignacli upgrade-repo
```  
Om de upgrade in simulatiemodus uit te voeren (om de SQL-statements te zien zonder ze toe te passen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dit commando is cruciaal voor het onderhouden van het ***digna*** systeem en zorgt ervoor dat het databaseschema en andere repository-componenten up-to-date zijn met de nieuwste versie van de software.

### encrypt
  
Het commando `encrypt` in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
#### Commaando Gebruik
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenten
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (verplicht).
  
#### Voorbeeld
  
Om een wachtwoord te versleutelen geef je het wachtwoord als argument.   
Bijvoorbeeld, om het wachtwoord `mypassword123` te versleutelen, gebruik je:
```bash
dignacli encrypt mypassword123
```
Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die vervolgens in veilige contexten gebruikt kan worden. Als het wachtwoordargument niet is opgegeven, zal de CLI een foutmelding tonen waarin het ontbrekende argument wordt aangegeven.

### generate-key
  
Het commando `generate-key` wordt gebruikt om een Fernet-sleutel te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
#### Commaando Gebruik
```bash
dignacli generate-key
```
  
## Databeheer

### clean-up

Het commando `clean-up` in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het verkeerslichtsysteem te verwijderen voor één of meerdere datasources binnen een opgegeven project. Dit commando is essentieel voor levenscyclusbeheer van data en helpt een georganiseerde en efficiënte dataomgeving te behouden door verouderde of onnodige gegevens te verwijderen.

#### Commaando Gebruik

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan data verwijderd moet worden (verplicht). Door het trefwoord all-projects te gebruiken in dit argument instrueer je ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van data. Toegestane formaten zijn onder andere %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van data, volgens dezelfde formaten als FROM_DATE (verplicht).
  
#### Opties
  
- `--table-name`, `-tn`: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filters om de clean-up te beperken tot tabellen waarvan de namen de opgegeven substring bevatten.
- `--timing`, `-tm`: Toont de duur van het clean-up proces na voltooiing.
- `--help`: Toont hulpinformatie voor het clean-up commando en stopt.
  
#### Voorbeeld
  
Om data te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Om data alleen uit een specifieke tabel met de naam `Table1` te verwijderen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dit commando helpt bij het beheren van datastorage en zorgt ervoor dat de repository alleen relevante informatie bevat.

### remove-orphans
  
Het commando `remove-orphans` in de ***digna*** CLI wordt gebruikt voor onderhoud in de ***digna*** repository.  
Wanneer een gebruiker projecten of datasources verwijdert, blijven de profielen en voorspellingen mogelijk in de repository achter. Met dit commando worden dergelijke verweesde rijen uit de repository verwijderd.
  
#### Commaando Gebruik
  
```bash
dignacli list-projects
```

### list-projects
  
Het commando `list-projects` in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
#### Commaando Gebruik
  
```bash
dignacli list-projects
```

Dit commando is vooral nuttig voor beheerders en gebruikers die meerdere projecten beheren en biedt een snel overzicht van de beschikbare projecten in de ***digna*** repository.

### list-ds

Het commando `list-ds` in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare datasources binnen een opgegeven project. Dit commando is handig om inzicht te krijgen in de data-assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

#### Commaando Gebruik
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvoor de datasources worden weergegeven (verplicht).
  
#### Voorbeeld
  
Om alle datasources in het project met de naam `ProjectA` weer te geven:
  
```bash
dignacli list-ds ProjectA
```
  
Dit commando geeft gebruikers een overzicht van de binnen een project beschikbare datasources, wat helpt bij het navigeren en beheren van het data-landschap.

### inspect

Het commando `inspect` in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het verkeerslichtsysteem te creëren voor één of meerdere datasources binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode. Na voltooiing van de inspectie wordt de waarde van het berekende verkeerslichtsysteem teruggegeven:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Commaando Gebruik

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project dat geïnspecteerd moet worden (verplicht). Door het trefwoord all-projects te gebruiken in dit argument instrueer je ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Toegestane formaten zijn onder andere %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, volgens dezelfde formaten als FROM_DATE (verplicht).
  
#### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun namen bevatten.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in bij alerts.
- `--bypass-backend`, `-bb`: Omzeil de backend en voer de inspectie direct vanuit de CLI uit (alleen voor testdoeleinden!).

  
#### Voorbeeld
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Om alleen een specifieke tabel te inspecteren en de voorspellingen geforceerd opnieuw te berekenen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dit commando is nuttig voor het genereren van geüpdatete profielen en voorspellingen, het monitoren van data-integriteit en het beheren van alerts binnen een opgegeven projecttijdvak.

### inspect-async

Het commando `inspect-async` in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het verkeerslichtsysteem te creëren voor één of meerdere datasources binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode. In tegenstelling tot het `inspect` commando wacht dit niet op de voltooiing van de inspectie.
In plaats daarvan retourneert het de request id voor het ingediende inspectieverzoek. Om de voortgang van het inspectieproces te controleren, gebruik je het commando `inspect-status`.

#### Commaando Gebruik

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project dat geïnspecteerd moet worden (verplicht). Door het trefwoord all-projects te gebruiken in dit argument instrueer je ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Toegestane formaten zijn onder andere %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, volgens dezelfde formaten als FROM_DATE (verplicht).
  
#### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun namen bevatten.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in bij alerts.

  
#### Voorbeeld
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Het commando `inspect-status` in de ***digna*** CLI wordt gebruikt om de voortgang van een asynchrone inspectie te controleren op basis van de request ID.

#### Commaando Gebruik

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenten
  
- **REQUEST_ID**: De request id die door het `inspect-async` commando is teruggegeven 
  
#### Voorbeeld
  
Om de voortgang van een inspectie met request ID 12345 te controleren:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Het commando `inspect-cancel` in de ***digna*** CLI wordt gebruikt om inspecties te annuleren op basis van de request ID of om alle huidige verzoeken te annuleren.

#### Commaando Gebruik

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenten
  
- **REQUEST_ID**: De request id die door het `inspect-async` commando is teruggegeven 
  
#### Voorbeeld
  
Om de inspectie met request ID 12345 te annuleren:
  
```bash
dignacli inspect-cancel 12345
```

Om alle verzoeken die momenteel draaien of in de wachtrij staan te annuleren:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Het commando `export-ds` in de ***digna*** CLI wordt gebruikt om een export van datasources uit de ***digna*** repository te maken. Standaard worden alle datasources van een gegeven project geëxporteerd.

#### Commaando Gebruik
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvan de datasources geëxporteerd worden.

#### Opties

- `--table_name`, `-tn`: Exporteer een specifieke datasource uit een project.
- `--exportfile`, `-ef`: Geef de bestandsnaam op voor de export.
    
#### Voorbeeld
  
Om alle datasources uit het project met de naam `ProjectA` te exporteren:
  
```bash
dignacli export-ds ProjectA
```
  
Dit commando exporteert alle datasources uit `ProjectA` als een JSON-document dat kan worden geïmporteerd in een ander project of een andere ***digna*** repository.


### import-ds

Het commando `import-ds` in de ***digna*** CLI wordt gebruikt om datasources te importeren in een doeltargetproject en een importrapport te genereren.

#### Commaando Gebruik
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarnaar de datasources geïmporteerd zullen worden.
- **EXPORT_FILE**: De bestandsnaam van de datasources-export die geïmporteerd moet worden.

#### Opties

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als dit niet is opgegeven, wordt er een tabelvormige weergave naar de terminal geprint).
- `--output-format`, `-f`: Formaat om het importrapport in op te slaan (json, csv).
    
#### Voorbeeld
  
Om alle datasources uit het exportbestand `my_export.json` te importeren in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Na de import toont dit commando ook een rapport van geïmporteerde en overgeslagen objecten. Alleen nieuwe datasources worden in `ProjectB` geïmporteerd. Om te achterhalen welke objecten geïmporteerd en overgeslagen zouden worden, kun je het commando `plan-import-ds` gebruiken.

### plan-import-ds

Het commando `plan-import-ds` in de ***digna*** CLI wordt gebruikt om een importplan te maken voor datasources naar een doeltargetproject en een importrapport te genereren zonder daadwerkelijk te importeren.

#### Commaando Gebruik
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarnaar de datasources geïmporteerd zouden worden.
- **EXPORT_FILE**: De bestandsnaam van de datasources-export die geanalyseerd moet worden vóór de import.

#### Opties

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als dit niet is opgegeven, wordt er een tabelvormige weergave naar de terminal geprint).
- `--output-format`, `-f`: Formaat om het importrapport in op te slaan (json, csv).
    
#### Voorbeeld
  
Om te controleren welke datasources geïmporteerd zouden worden en welke overgeslagen zouden worden uit het exportbestand `my_export.json` wanneer dit in `ProjectB` geïmporteerd zou worden:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dit commando toont alleen een importplan van objecten die geïmporteerd en overgeslagen zouden worden.