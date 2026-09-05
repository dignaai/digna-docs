---
title: digna CLI Referentie 2024.12 – Commando's & Voorbeelden | digna Documentatie
description: Volledige referentie voor digna CLI release 2024.12. Leer hoe je gebruikers, repositories en gegevens beheert met commando's zoals add-user, check-repo-connection, upgrade-repo, inspect en meer.
image: /assets/logo_square.png
---


# digna CLI Referentie 2024.12
**2024-12-09**

Deze pagina documenteert de volledige set commando's die beschikbaar zijn in de ***digna*** CLI release **2024.12**, inclusief gebruiksvoorbeelden en opties.

---


**2024-12-09**


---

## CLI Basisprincipes

---

## Het gebruik van de `help` optie

De `--help` optie geeft informatie over beschikbare commando's en hun gebruik. Er zijn twee hoofdmanieren om deze optie te gebruiken:

1. **Algemene help weergeven:**
   
    Gebruik –help direct na het trefwoord ***digna***cl  
   ```bash
   dignacli --help
   ```

3.  **Hulp voor specifieke commando's krijgen:**  
  
    Voor gedetailleerde informatie over een specifiek commando, voeg `--help` toe aan dat commando.
    Bijvoorbeeld, om hulp bij het `add-user` commando te krijgen, voer uit:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Commando Beschrijving:** Geeft een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntaxis:** Toont de exacte syntaxis, inclusief verplichte en optionele argumenten.  
     - **Opties:** Geeft een lijst van opties specifiek voor het commando, met bijbehorende uitleg.  
     - **Voorbeelden:** Biedt voorbeelden van hoe het commando effectief uitgevoerd kan worden.

  
## Het gebruik van het `check-repo-connection` Commando

Het check-repo-connection commando is een hulpmiddel binnen de ***digna*** CLI om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando zorgt ervoor dat de CLI met de repository kan communiceren.
      
### Commando Gebruik
```bash
dignacli check-repo-connection
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repository versie, Host, Database en Schema.  
  
Als de repository-verbinding niet succesvol is, controleer dan het config.toml bestand op correcte configuratie-instellingen.

## Het gebruik van het ‘version’ commando

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik je de --version optie.  
  
### Commando Gebruik
```bash
dignacli --version
```
  
### Voorbeeldoutput
```bash
dignacli version 2024.12
```

## Logging opties gebruiken
  
Standaard is de console-uitvoer van de ***digna*** commando's minimalistisch. De meeste commando's bieden de mogelijkheid om extra informatie te geven met de volgende opties:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” en “debug” bepalen het detailniveau, terwijl de “logfile” schakelaar het mogelijk maakt om de uitvoer naar een bestand te streamen in plaats van naar het consolevenster.

# Gebruikersbeheer

## Het gebruik van het ‘add-user’ commando
  
Het add-user commando in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem.
  
### Commando Gebruik
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenten

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (verplicht).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (verplicht).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (verplicht).

### Opties

- `--is_superuser`, `-su`: Vlag om de nieuwe gebruiker als admin aan te wijzen.
- `--valid_until`, `-vu`: Stelt een vervaldatum voor het gebruikersaccount in in het formaat `YYYY-MM-DD HH:MI:SS`. Als dit niet wordt ingesteld, heeft het account geen vervaldatum.

### Voorbeeld

Om een nieuwe gebruiker toe te voegen met gebruikersnaam `jdoe`, volledige naam `John Doe`, en wachtwoord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Om een nieuwe gebruiker toe te voegen en een vervaldatum voor het account in te stellen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Het gebruik van het `delete-user` commando
  
Het `delete-user` commando in de ***digna*** CLI wordt gebruikt om een bestaande gebruiker te verwijderen uit het ***digna*** systeem.
  
### Commando Gebruik
```bash
dignacli delete-user USER_NAME
```
  
### Argumenten
- **USER_NAME**: De gebruikersnaam van de te verwijderen gebruiker (verplicht). Dit is het enige vereiste argument van het commando.

### Voorbeeld
```bash
dignacli delete-user jdoe
```
  
Het uitvoeren van dit commando verwijdert de gebruiker `jdoe` uit het ***digna*** systeem, intrekkend hun toegang en verwijderend hun gerelateerde gegevens en permissies uit de repository.

## Het gebruik van het `modify-user` Commando

Het `modify-user` commando in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker in het ***digna*** systeem bij te werken.

### Commando Gebruik
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de te wijzigen gebruiker (verplicht).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (verplicht).
  
### Opties  
  
- `--is_superuser`, `-su`: Zet de gebruiker als superuser en geeft verhoogde privileges. Deze vlag vereist geen waarde.  
- `--valid_until`, `-vu`: Stelt een vervaldatum voor het gebruikersaccount in in het formaat YYYY-MM-DD HH:MI:SS. Als dit niet wordt opgegeven, blijft het account onbeperkt geldig.  
  
### Voorbeeld
  
Om de volledige naam van de gebruiker `jdoe` te wijzigen naar “Johnathan Doe” en de gebruiker als superuser in te stellen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Het gebruik van het `modify-user-pwd` Commando
  
Het `modify-user-pwd` commando in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker in het ***digna*** systeem te wijzigen.
  
### Commando Gebruik
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker waarvan het wachtwoord gewijzigd moet worden (verplicht).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (verplicht).
  
### Voorbeeld
  
Om het wachtwoord van de gebruiker `jdoe` te wijzigen naar `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Het gebruik van het `list-users` Commando

Het `list-users` commando in de ***digna*** CLI toont een lijst van alle gebruikers die geregistreerd zijn in het ***digna*** systeem.

### Commando Gebruik

```bash
dignacli list-users
```

Het uitvoeren van dit commando in de ***digna*** CLI maakt verbinding met de ***digna*** repository en toont alle gebruikers, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaltijdstempels.

# Repository Beheer

### Het gebruik van het `upgrade-repo` Commando
  
Het `upgrade-repo` commando in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel voor het toepassen van updates of het voor het eerst opzetten van de repository-infrastructuur.
  
### Commando Gebruik

```bash
dignacli upgrade-repo [options]
```
  
### Opties
  
- `--simulation-mode`, `-s`: Wanneer ingeschakeld draait dit het commando in simulatiemodus, wat de SQL-statements print die uitgevoerd zouden worden maar deze niet daadwerkelijk uitvoert. Dit is handig om wijzigingen vooraf te bekijken zonder iets aan de repository te wijzigen.  

  
### Voorbeeld
  
Om de ***digna*** repository te upgraden, kun je het commando zonder opties uitvoeren:
  
```bash
dignacli upgrade-repo
```  
Om de upgrade in simulatiemodus uit te voeren (om de SQL-statements te zien zonder ze toe te passen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dit commando is van cruciaal belang voor het onderhouden van het ***digna*** systeem en zorgt ervoor dat het databasemodel en andere repository-componenten up-to-date zijn met de nieuwste versie van de software.

## Het gebruik van het `encrypt` Commando
  
Het `encrypt` commando in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
### Commando Gebruik
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenten
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (verplicht).
  
### Voorbeeld
  
Om een wachtwoord te versleutelen moet je het wachtwoord als argument meegeven.   
Bijvoorbeeld, om het wachtwoord `mypassword123` te versleutelen, gebruik je:
```bash
dignacli encrypt mypassword123
```
Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die vervolgens in beveiligde contexten gebruikt kan worden. Als het wachtwoordargument niet wordt opgegeven, geeft de CLI een foutmelding over het ontbrekende argument.

## Het gebruik van het `generate-key` Commando
  
Het `generate-key` commando wordt gebruikt om een Fernet-sleutel te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
### Commando Gebruik
```bash
dignacli generate-key
```
  
# Gegevensbeheer

## Het gebruik van het `clean-up` Commando

Het `clean-up` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het Traffic Light System voor één of meerdere gegevensbronnen binnen een opgegeven project te verwijderen. Dit commando is essentieel voor lifecycle-beheer van data en helpt een georganiseerde en efficiënte dataomgeving te behouden door verouderde of onnodige gegevens op te schonen.

### Commando Gebruik

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan gegevens verwijderd moeten worden (verplicht). Gebruik je het sleutelwoord all-projects in dit argument, dan instrueert dit ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van gegevens. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van gegevens, volgens dezelfde formaten als FROM_DATE (verplicht).
  
### Opties
  
- `--table-name`, `-tn`: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om de clean-up te beperken tot tabellen die de opgegeven substring in hun naam bevatten.
- `--timing`, `-tm`: Toont de duur van het clean-up proces na voltooiing.
- `--help`: Toont helpinformatie voor het clean-up commando en stopt.
  
### Voorbeeld
  
Om gegevens te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Om alleen gegevens uit een specifieke tabel genaamd `Table1` te verwijderen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dit commando helpt bij het beheren van gegevensopslag en zorgt ervoor dat de repository alleen relevante informatie bevat.

## Het gebruik van het `inspect` Commando

Het `inspect` commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en Traffic Light System-gegevens te creëren voor één of meerdere gegevensbronnen binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van gegevens over een gedefinieerde periode.

### Commando Gebruik

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor gegevens geïnspecteerd moeten worden (verplicht). Gebruik je het sleutelwoord all-projects in dit argument, dan instrueert dit ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de inspectie van gegevens. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (verplicht).
- **TO_DATE**: De einddatum en -tijd voor de inspectie van gegevens, volgens dezelfde formaten als FROM_DATE (verplicht).
  
### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun naam bevatten.
- `--do-profile`: Veroorzaakt het opnieuw verzamelen van profielen. Standaard is do-profile ingeschakeld.
- `--no-do-profile`: Voorkomt het opnieuw verzamelen van profielen.
- `--do-prediction`: Veroorzaakt het herberekenen van voorspellingen. Standaard is do-prediction ingeschakeld.
- `--no-do-prediction`: Voorkomt het herberekenen van voorspellingen.
- `--do-alert-status`: Veroorzaakt het herberekenen van alertstatussen. Standaard is do-alert-status ingeschakeld.
- `--no-do-alert-status`: Voorkomt het herberekenen van alertstatussen.
- `--iterative`: Veroorzaakt de inspectie van een periode met dagelijkse iteraties. Standaard is iterative ingeschakeld.
- `--no-iterative`: Veroorzaakt de inspectie van de gehele periode in één keer.
- `--timing`, `-tm`: Toont de duur van het inspectieproces na voltooiing.
  
### Voorbeeld
  
Om gegevens te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Om alleen een specifieke tabel te inspecteren en het herberekenen van voorspellingen af te dwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dit commando is nuttig voor het genereren van bijgewerkte profielen en voorspellingen, het monitoren van dataintegriteit en het beheren van alerts binnen een opgegeven projecttijdvak.

## Het gebruik van het `tls-status` Commando

Het `tls-status` commando in de ***digna*** CLI wordt gebruikt om de status van het Traffic Light System (TLS) op te vragen voor een specifieke tabel binnen een project op een bepaalde datum. Het Traffic Light System biedt inzicht in de gezondheid en kwaliteit van de gegevens en geeft eventuele problemen of waarschuwingen aan die aandacht vereisen.
  
### Commando Gebruik
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor de TLS-status wordt opgevraagd (verplicht).
- **TABLE_NAME**: De specifieke tabel binnen het project waarvoor de TLS-status nodig is (verplicht).
- **DATE**: De datum waarvoor de TLS-status wordt opgevraagd, typisch in het formaat %Y-%m-%d (verplicht).
  
### Voorbeeld
  
Om de TLS-status te controleren voor een tabel genaamd UserData in het project ProjectA op 1 juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dit commando helpt gebruikers bij het monitoren en behouden van datakwaliteit door een duidelijke en bruikbare statusrapportage te bieden op basis van vooraf gedefinieerde criteria.

## Het gebruik van het `list-projects` Commando
  
Het `list-projects` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
### Commando Gebruik
  
```bash
dignacli list-projects
```

Dit commando is vooral nuttig voor beheerders en gebruikers die meerdere projecten beheren, en geeft snel een overzicht van de beschikbare projecten in de ***digna*** repository.

## Het gebruik van het `list-ds` Commando

Het `list-ds` commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare data sources binnen een opgegeven project. Dit commando is nuttig om inzicht te krijgen in de data-assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

### Commando Gebruik
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenten
- **PROJECT_NAME**: De naam van het project waarvoor de data sources worden weergegeven (verplicht).
  
### Voorbeeld
  
Om alle data sources in het project met de naam `ProjectA` te tonen:
  
```bash
dignacli list-ds ProjectA
```
  
Dit commando geeft gebruikers een overzicht van de data sources die in een project beschikbaar zijn en helpt bij het navigeren en beheren van het datalandschap.