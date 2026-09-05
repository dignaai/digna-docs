# digna CLI Referentie 2025.04
**2025-04-01**

Deze pagina documenteert de volledige set commando's die beschikbaar zijn in de ***digna*** CLI release **2025.04**, inclusief gebruiksvoorbeelden en opties.

---

## CLI Basis

---

## Gebruik van de `--help` Optie

De `--help` optie geeft informatie over beschikbare commando's en hun gebruik. Er zijn twee hoofdmanieren om deze optie te gebruiken:

1. **Algemene hulp weergeven:**
   
    Gebruik --help direct na het commando ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hulp voor specifieke commando's opvragen:**  
  
    Voor gedetailleerde informatie over een specifiek commando, voeg `--help` toe aan dat commando.  
    Bijvoorbeeld, om hulp te krijgen bij het `add-user` commando, voer uit:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Beschrijving van het commando:** Geeft een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntax:** Toont de exacte syntax, inclusief vereiste en optionele argumenten.  
     - **Opties:** Lijst van opties specifiek voor het commando, met hun toelichting.  
     - **Voorbeelden:** Biedt voorbeelden van hoe het commando effectief uitgevoerd kan worden.

  
## Gebruik van het `check-repo-connection` Commando

Het check-repo-connection commando is een hulpprogramma binnen de ***digna*** CLI om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando controleert of de CLI met de repository kan communiceren.
      
#### Gebruik van het commando
```bash
dignacli check-repo-connection
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repositoryversie, Host, Database en Schema.  
  
Als de repositoryverbinding niet succesvol is, controleer dan het bestand config.toml voor correcte configuratie-instellingen.

## Gebruik van het ‘version’ commando

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik de --version optie.  
  
#### Gebruik van het commando
```bash
dignacli --version
```
  
#### Voorbeelduitvoer
```bash
dignacli version 2025.04
```

## Gebruik van logging opties
  
Standaard is de console-uitvoer van de ***digna*** commando's minimalistisch. De meeste commando's bieden de mogelijkheid extra informatie te tonen met de volgende opties:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
"verbose" en "debug" bepalen het detailniveau, terwijl de "logfile" schakelaar toestaat de uitvoer naar een bestand te streamen in plaats van naar het consolevenster.

## Gebruikersbeheer

### Gebruik van het ‘add-user’ commando
  
Het add-user commando in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem
  
#### Gebruik van het commando
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenten

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (verplicht).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (verplicht).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (verplicht).

#### Opties

- `--is_superuser`, `-su`: Vlag om de nieuwe gebruiker als admin aan te wijzen.
- `--valid_until`, `-vu`: Stelt een vervaldatum voor het gebruikersaccount in in het formaat `YYYY-MM-DD HH:MI:SS`. Als niet ingesteld, heeft het account geen vervaldatum.

#### Voorbeeld

Om een nieuwe gebruiker toe te voegen met gebruikersnaam `jdoe`, volledige naam `John Doe`, en wachtwoord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Om een nieuwe gebruiker toe te voegen en een vervaldatum voor het account in te stellen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Gebruik van het `delete-user` commando
  
Het `delete-user` commando in de ***digna*** CLI wordt gebruikt om een bestaande gebruiker te verwijderen uit het ***digna*** systeem.
  
#### Gebruik van het commando
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenten
- **USER_NAME**: De gebruikersnaam van de te verwijderen gebruiker (verplicht). Dit is het enige vereiste argument voor het commando.

#### Voorbeeld
```bash
dignacli delete-user jdoe
```
  
Het uitvoeren van dit commando verwijdert de gebruiker `jdoe` uit het ***digna*** systeem, intrekt zijn/haar toegang en verwijdert de bijbehorende data en permissies uit de repository.

### Gebruik van het `modify-user` Commando

Het `modify-user` commando in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker bij te werken in het ***digna*** systeem.

#### Gebruik van het commando
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker die gewijzigd moet worden (verplicht).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (verplicht).
  
#### Opties  
  
- `--is_superuser`, `-su`: Maakt de gebruiker superuser en verleent verhoogde privileges. Deze vlag vereist geen waarde.  
- `--valid_until`, `-vu`: Stelt een vervaldatum voor het account in het formaat YYYY-MM-DD HH:MI:SS. Als niet opgegeven, blijft het account onbeperkt geldig.  
  
#### Voorbeeld
  
Om de volledige naam van de gebruiker `jdoe` te wijzigen naar “Johnathan Doe” en de gebruiker als superuser in te stellen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Gebruik van het `modify-user-pwd` Commando
  
Het `modify-user-pwd` commando in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker te wijzigen in het ***digna*** systeem.
  
#### Gebruik van het commando
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker wiens wachtwoord gewijzigd moet worden (verplicht).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (verplicht).
  
#### Voorbeeld
  
Om het wachtwoord van de gebruiker `jdoe` te wijzigen naar `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Gebruik van het `list-users` Commando

Het `list-users` commando in de ***digna*** CLI toont een lijst van alle gebruikers die geregistreerd zijn in het ***digna*** systeem.

#### Gebruik van het commando

```bash
dignacli list-users
```

Het uitvoeren van dit commando in de ***digna*** CLI maakt verbinding met de ***digna*** repository en toont alle gebruikers, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaltijdstempels.

## Repositorybeheer

### Gebruik van het `upgrade-repo` Commando
  
Het `upgrade-repo` commando in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel voor het toepassen van updates of het opzetten van de repository-infrastructuur voor de eerste keer.
  
#### Gebruik van het commando

```bash
dignacli upgrade-repo [options]
```
  
#### Opties
  
- `--simulation-mode`, `-s`: Wanneer ingeschakeld, voert dit commando de operatie uit in simulatiemodus, waarbij de SQL-statements worden geprint die uitgevoerd zouden worden, maar deze niet daadwerkelijk worden uitgevoerd. Dit is handig om wijzigingen te bekijken zonder de repository aan te passen.  

  
#### Voorbeeld
  
Om de ***digna*** repository te upgraden, kunt u het commando zonder opties uitvoeren:
  
```bash
dignacli upgrade-repo
```  
Om de upgrade in simulatiemodus uit te voeren (om de SQL-statements te zien zonder ze toe te passen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dit commando is cruciaal voor het onderhoud van het ***digna*** systeem en zorgt ervoor dat de databaseschema's en andere repositorycomponenten up-to-date zijn met de nieuwste versie van de software.

### Gebruik van het `encrypt` Commando
  
Het `encrypt` commando in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
#### Gebruik van het commando
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenten
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (verplicht).
  
#### Voorbeeld
  
Om een wachtwoord te versleutelen, moet u het wachtwoord als argument meegeven.   
Bijvoorbeeld, om het wachtwoord `mypassword123` te versleutelen, gebruikt u:
```bash
dignacli encrypt mypassword123
```
Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die vervolgens gebruikt kan worden in veilige contexten. Als het wachtwoordargument niet wordt opgegeven, zal de CLI een foutmelding tonen dat het argument ontbreekt.

## Gebruik van het `generate-key` Commando
  
Het `generate-key` commando wordt gebruikt om een Fernet-sleutel te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
#### Gebruik van het commando
```bash
dignacli generate-key
```
  
## Gegevensbeheer

## Gebruik van het `clean-up` Commando

Het `clean-up` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en data van het Traffic Light System te verwijderen voor één of meerdere data sources binnen een opgegeven project. Dit commando is essentieel voor lifecycle-management van data en helpt bij het onderhouden van een georganiseerde en efficiënte dataomgeving door verouderde of onnodige data op te schonen.

#### Gebruik van het commando

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan data verwijderd moet worden (verplicht). Als u de sleutelwoord all-projects gebruikt in dit argument, instrueert u ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van data. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van data, met dezelfde formaten als FROM_DATE (verplicht).
  
#### Opties
  
- `--table-name`, `-tn`: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om de clean-up te beperken tot tabellen die de opgegeven substring in hun naam bevatten.
- `--timing`, `-tm`: Toont de duur van het clean-up proces na voltooiing.
- `--help`: Toont helpinformatie voor het clean-up commando en stopt.
  
#### Voorbeeld
  
Om data te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Om alleen data te verwijderen uit een specifieke tabel genaamd `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dit commando helpt bij het beheren van dataopslag en zorgt ervoor dat de repository alleen relevante informatie bevat.

## Gebruik van het `list-projects` Commando
  
Het `list-projects` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
#### Gebruik van het commando
  
```bash
dignacli list-projects
```

Dit commando is vooral nuttig voor beheerders en gebruikers die meerdere projecten beheren en biedt een snel overzicht van de beschikbare projecten in de ***digna*** repository.

## Gebruik van het `list-ds` Commando

Het `list-ds` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare data sources binnen een opgegeven project. Dit commando is nuttig om inzicht te krijgen in de data-assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

#### Gebruik van het commando
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvoor de data sources worden opgelijst (verplicht).
  
#### Voorbeeld
  
Om alle data sources in het project met de naam `ProjectA` op te sommen:
  
```bash
dignacli list-ds ProjectA
```
  
Dit commando geeft gebruikers een overzicht van de beschikbare data sources in een project en helpt hen bij het navigeren en beheren van het datalandschap.

## Gebruik van het `inspect` Commando

Het `inspect` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en data voor het Traffic Light System te creëren voor één of meerdere data sources binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een gedefinieerde periode.

#### Gebruik van het commando

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan data geïnspecteerd moet worden (verplicht). Als u de sleutelwoord all-projects gebruikt in dit argument, instrueert u ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, met dezelfde formaten als FROM_DATE (verplicht).
  
#### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun naam bevatten.
- `--do-profile`: Dwingt het opnieuw verzamelen van profielen. Standaard is do-profile.
- `--no-do-profile`: Voorkomt het opnieuw verzamelen van profielen.
- `--do-prediction`: Dwingt het opnieuw berekenen van voorspellingen. Standaard is do-prediction.
- `--no-do-prediction`: Voorkomt het opnieuw berekenen van voorspellingen.
- `--do-alert-status`: Dwingt het opnieuw berekenen van alert-statussen. Standaard is do-alert-status.
- `--no-do-alert-status`: Voorkomt het opnieuw berekenen van alert-statussen.
- `--iterative`: Voert de inspectie van een periode uit met dagelijkse iteraties. Standaard is iterative.
- `--no-iterative`: Voert de inspectie van de volledige periode in één keer uit.
- `--enable_notification`, `-en`: Schakelt het verzenden van notificaties in in geval van alerts.
- `--timing`, `-tm`: Toont de duur van het inspectieproces na voltooiing.
  
#### Voorbeeld
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Om slechts een specifieke tabel te inspecteren en de voorspellingen opnieuw te berekenen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dit commando is nuttig voor het genereren van bijgewerkte profielen en voorspellingen, het monitoren van dataintegriteit en het beheren van alerts binnen een specifieke projectperiode.

## Gebruik van het `tls-status` Commando

Het `tls-status` commando in de ***digna*** CLI wordt gebruikt om de status van het Traffic Light System (TLS) op te vragen voor een specifieke tabel binnen een project op een bepaalde datum. Het Traffic Light System geeft inzicht in de gezondheid en kwaliteit van de data en wijst op eventuele problemen of alerts die aandacht behoeven.
  
#### Gebruik van het commando
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor de TLS-status wordt opgevraagd (verplicht).
- **TABLE_NAME**: De specifieke tabel binnen het project waarvoor de TLS-status nodig is (verplicht).
- **DATE**: De datum waarvoor de TLS-status wordt opgevraagd, doorgaans in het formaat %Y-%m-%d (verplicht).
  
#### Voorbeeld
  
Om de TLS-status te controleren voor een tabel genaamd UserData in het project ProjectA op 1 juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dit commando helpt gebruikers bij het monitoren en onderhouden van datakwaliteit door een duidelijk en actiegericht statusrapport te bieden op basis van vooraf gedefinieerde criteria.

## Gebruik van het `inspect-async` Commando

Het `inspect-async` commando in de ***digna*** CLI wordt gebruikt om de backend aan te sturen om asynchroon de inspectie uit te voeren voor één of meerdere data sources binnen een gegeven project. Als project_name is ingesteld op all-projects, zal de inspectie over alle beschikbare projecten itereren en de inspectie uitvoeren. Het retourneert een request id die gebruikt kan worden om de voortgang van de inspectie te volgen.

#### Gebruik van het commando

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan data geïnspecteerd moet worden (verplicht). Als u de sleutelwoord all-projects gebruikt in dit argument, instrueert u ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, met dezelfde formaten als FROM_DATE (verplicht).
  
#### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun naam bevatten.

  
#### Voorbeeld
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Gebruik van het `inspect-status` Commando

Het `inspect-status` commando in de ***digna*** CLI wordt gebruikt om de voortgang van een asynchrone inspectie te controleren op basis van de request ID.

#### Gebruik van het commando

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenten
  
- **REQUEST_ID**: De request id die geretourneerd is door het `inspect-async` commando 
  
#### Opties

- `--report_level`, `-rl`: Stel het rapportageniveau in: 'task' of 'step' [default: task]
  
#### Voorbeeld
  
Om de voortgang van een inspectie met request ID 12345 te controleren op gedetailleerd step-niveau:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Gebruik van het `export-ds` Commando

Het `export-ds` commando in de ***digna*** CLI wordt gebruikt om een export van data sources uit de ***digna*** repository te maken. Standaard worden alle data sources van een gegeven project geëxporteerd.

#### Gebruik van het commando
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvan de data sources geëxporteerd zullen worden.

#### Opties

- `--table_name`, `-tn`: Exporteer een specifieke data source uit een project.
- `--exportfile`, `-ef`: Geef de bestandsnaam op voor de export.
    
#### Voorbeeld
  
Om alle data sources uit het project met de naam `ProjectA` te exporteren:
  
```bash
dignacli export-ds ProjectA
```
  
Dit commando exporteert alle data sources van `ProjectA` als een JSON-document dat geïmporteerd kan worden in een ander project of ***digna*** repository.


## Gebruik van het `import-ds` Commando

Het `import-ds` commando in de ***digna*** CLI wordt gebruikt om data sources te importeren in een doeldproject en een importrapport aan te maken.

#### Gebruik van het commando
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarnaar de data sources geïmporteerd zullen worden.
- **EXPORT_FILE**: De bestandsnaam van de geëxporteerde data sources die geïmporteerd moeten worden.

#### Opties

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als niet opgegeven, wordt het in tabulaire vorm naar de terminal geprint).
- `--output-format`, `-f`: Formaat om het importrapport op te slaan (json, csv).
    
#### Voorbeeld
  
Om alle data sources uit exportbestand `my_export.json` te importeren in `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Na de import zal dit commando ook een rapport tonen van geïmporteerde en overgeslagen objecten. Alleen nieuwe data sources worden in `ProjectB` geïmporteerd. Om te achterhalen welke objecten geïmporteerd en overgeslagen zouden worden, kunt u het commando `plan-import-ds` gebruiken.

## Gebruik van het `plan-import-ds` Commando

Het `plan-import-ds` commando in de ***digna*** CLI wordt gebruikt om een importplan te maken voor data sources in een doelproject en een importrapport te genereren zonder daadwerkelijk te importeren.

#### Gebruik van het commando
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenten
- **PROJECT_NAME**: De naam van het project waarnaar de data sources zouden worden geïmporteerd.
- **EXPORT_FILE**: De bestandsnaam van de geëxporteerde data sources die geanalyseerd moeten worden voor de import.

#### Opties

- `--output-file`, `-o`: Bestand om het importrapport in op te slaan (als niet opgegeven, wordt het in tabulaire vorm naar de terminal geprint).
- `--output-format`, `-f`: Formaat om het importrapport op te slaan (json, csv).
    
#### Voorbeeld
  
Om te controleren welke data sources geïmporteerd en welke overgeslagen zouden worden uit exportbestand `my_export.json` bij import in `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Dit commando toont alleen een importplan van objecten die geïmporteerd en overgeslagen zouden worden.