---
title: digna CLI-referentie 2024.11 – Commands & Examples | digna Documentatie
description: Volledige referentie voor digna CLI release 2024.11. Leer hoe u gebruikers, repositories en data beheert met commando's zoals add-user, check-repo-connection, upgrade-repo, inspect, tls-status en meer.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Deze pagina documenteert de volledige set commando's beschikbaar in de ***digna*** CLI release **2024.11**, inclusief gebruiksvoorbeelden en opties.


---
## CLI Basis

---

## Gebruik van de `help`-optie

De `--help`-optie geeft informatie over beschikbare commando's en hun gebruik. Er zijn twee hoofdmanieren om deze optie te gebruiken:

1. **Algemene help weergeven:**
   
    Gebruik `--help` direct na het sleutelwoord `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Help voor specifieke commando's opvragen:**
  
    Voor gedetailleerde informatie over een specifiek commando, voeg `--help` toe aan dat commando.
    Bijvoorbeeld, om hulp te krijgen voor het `add-user`-commando, voer uit:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Commando Beschrijving:** Biedt een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntax:** Toont de exacte syntaxis, inclusief verplichte en optionele argumenten.  
     - **Opties:** Vermeldt eventuele opties specifiek voor het commando, samen met hun uitleg.  
     - **Voorbeelden:** Geeft voorbeelden van hoe het commando effectief kan worden uitgevoerd.

  
## Gebruik van het `check-repo-connection`-commando

Het `check-repo-connection`-commando is een hulpprogramma binnen de ***digna*** CLI bedoeld om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando controleert of de CLI met de repository kan communiceren.
      
### Commando Gebruik
```bash
dignacli check-repo-connection
```

Bij succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repository-versie, Host, Database en Schema.  
  
Als de repository-verbinding niet succesvol is, controleer dan het config.toml-bestand op correcte configuratie-instellingen.

## Gebruik van het ‘version’-commando

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik de --version-optie.  
  
### Commando Gebruik
```bash
dignacli --version
```
  
### Voorbeeldoutput
```bash
dignacli version 2024.11
```

## Gebruik van logging-opties
  
Standaard is de console-uitvoer van de ***digna*** commando's minimalistisch. De meeste commando's bieden de mogelijkheid om extra informatie te tonen met de volgende opties:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” en “debug” bepalen het detailniveau, terwijl de “logfile”-schakelaar het mogelijk maakt om de uitvoer naar een bestand te laten schrijven in plaats van naar het terminalvenster.

# Gebruikersbeheer

## Gebruik van het ‘add-user’-commando
  
Het `add-user`-commando in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem.
  
### Commando Gebruik
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenten

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (vereist).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (vereist).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (vereist).

### Opties

- `--is_superuser`, `-su`: Vlag om de nieuwe gebruiker als beheerder aan te wijzen.
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat `YYYY-MM-DD HH:MI:SS`. Als niet ingesteld, heeft het account geen vervaldatum.

### Voorbeeld

Om een nieuwe gebruiker toe te voegen met gebruikersnaam `jdoe`, volledige naam `John Doe` en wachtwoord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Om een nieuwe gebruiker toe te voegen en een vervaldatum voor het account in te stellen:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Gebruik van het `delete-user`-commando
  
Het `delete-user`-commando in de ***digna*** CLI wordt gebruikt om een bestaande gebruiker te verwijderen uit het ***digna*** systeem.
  
### Commando Gebruik
```bash
dignacli delete-user USER_NAME
```
  
### Argumenten
- **USER_NAME**: De gebruikersnaam van de te verwijderen gebruiker (vereist). Dit is het enige argument dat door het commando vereist wordt.

### Voorbeeld
```bash
dignacli delete-user jdoe
```
  
Het uitvoeren van dit commando verwijdert de gebruiker `jdoe` uit het ***digna*** systeem, intrekkend hun toegang en verwijderend hun gerelateerde gegevens en permissies uit de repository.

## Gebruik van het `modify-user`-commando

Het `modify-user`-commando in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker in het ***digna*** systeem bij te werken.

### Commando Gebruik
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de te wijzigen gebruiker (vereist).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (vereist).
  
### Opties  
  
- `--is_superuser`, `-su`: Zet de gebruiker als superuser en geeft verhoogde privileges. Deze vlag vereist geen waarde.  
- `--valid_until`, `-vu`: Stelt een vervaldatum in voor het gebruikersaccount in het formaat YYYY-MM-DD HH:MI:SS. Als niet opgegeven, blijft het account onbeperkt geldig.  
  
### Voorbeeld
  
Om de volledige naam van de gebruiker `jdoe` te wijzigen naar “Johnathan Doe” en de gebruiker als superuser in te stellen:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Gebruik van het `modify-user-pwd`-commando
  
Het `modify-user-pwd`-commando in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker in het ***digna*** systeem te wijzigen.
  
### Commando Gebruik
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker waarvan het wachtwoord gewijzigd moet worden (vereist).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (vereist).
  
### Voorbeeld
  
Om het wachtwoord van de gebruiker `jdoe` te wijzigen naar `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Gebruik van het `list-users`-commando

Het `list-users`-commando in de ***digna*** CLI toont een lijst van alle gebruikers die in het ***digna*** systeem geregistreerd zijn.

### Commando Gebruik

```bash
dignacli list-users
```

Het uitvoeren van dit commando in de ***digna*** CLI verbindt met de ***digna*** repository en toont alle gebruikers, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaltijdstempels.

# Repositorybeheer

### Gebruik van het `upgrade-repo`-commando
  
Het `upgrade-repo`-commando in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel voor het toepassen van updates of het opzetten van de repository-infrastructuur voor de eerste keer.
  
### Commando Gebruik

```bash
dignacli upgrade-repo [options]
```
  
### Opties
  
- `--simulation-mode`, `-s`: Wanneer ingeschakeld, voert deze optie het commando uit in simulatiemodus, waarbij de SQL-verklaringen die uitgevoerd zouden worden worden afgedrukt maar niet daadwerkelijk worden uitgevoerd. Dit is handig om wijzigingen vooraf te bekijken zonder iets aan de repository te wijzigen.  

  
### Voorbeeld
  
Om de ***digna*** repository te upgraden, kunt u het commando zonder opties uitvoeren:
  
```bash
dignacli upgrade-repo
```  
Om de upgrade in simulatiemodus uit te voeren (om de SQL-verklaringen te zien zonder ze toe te passen):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Dit commando is cruciaal voor het onderhoud van het ***digna*** systeem, en zorgt ervoor dat het databaseschema en andere repositorycomponenten up-to-date zijn met de nieuwste versie van de software.

## Gebruik van het `encrypt`-commando
  
Het `encrypt`-commando in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
### Commando Gebruik
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenten
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (vereist).
  
### Voorbeeld
  
Om een wachtwoord te versleutelen, moet u het wachtwoord als argument opgeven.   
Bijvoorbeeld, om het wachtwoord `mypassword123` te versleutelen, zou u het volgende gebruiken:
```bash
dignacli encrypt mypassword123
```
Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die daarna in beveiligde contexten gebruikt kan worden. Als het wachtwoordargument niet wordt opgegeven, toont de CLI een foutmelding die aangeeft dat het argument ontbreekt.

## Gebruik van het `generate-key`-commando
  
Het `generate-key`-commando wordt gebruikt om een Fernet-sleutel te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
### Commando Gebruik
```bash
dignacli generate-key
```
  
# Data Management

## Gebruik van het `clean-up`-commando

Het `clean-up`-commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het Traffic Light System te verwijderen voor één of meer databronnen binnen een opgegeven project. Dit commando is essentieel voor het beheer van de levenscyclus van data en helpt bij het behouden van een georganiseerde en efficiënte dataomgeving door verouderde of onnodige gegevens op te schonen.

### Commando Gebruik

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan data verwijderd moet worden (vereist). Het gebruik van het sleutelwoord `all-projects` in dit argument geeft instructie aan ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van data. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van data, volgens dezelfde formaten als FROM_DATE (vereist).
  
### Opties
  
- `--table-name`, `-tn`: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om de clean-up te beperken tot tabellen die de opgegeven substring in hun namen bevatten.
- `--timing`, `-tm`: Toont de tijdsduur van het clean-up proces na voltooiing.
- `--help`: Toont helpinformatie voor het clean-up-commando en beëindigt.
  
### Voorbeeld
  
Om data te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Om data alleen uit een specifieke tabel genaamd `Table1` te verwijderen:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Dit commando helpt bij het beheren van dataopslag en zorgt ervoor dat de repository alleen relevante informatie bevat.

## Gebruik van het `inspect`-commando

Het `inspect`-commando in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en Traffic Light System-gegevens te creëren voor één of meer databronnen binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van data over een bepaald tijdsbestek.

### Commando Gebruik

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor data geïnspecteerd moet worden (vereist). Het gebruik van het sleutelwoord `all-projects` in dit argument geeft instructie aan ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De begindatum en -tijd voor de data-inspectie. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor de data-inspectie, volgens dezelfde formaten als FROM_DATE (vereist).
  
### Opties

- `--table-name`, `-tn`: Beperkt de inspectie tot een specifieke tabel binnen het project.
- `--table-filter`, `-tf`: Filtert om alleen tabellen te inspecteren die de opgegeven substring in hun namen bevatten.
- `--do-profile`: Triggert het opnieuw verzamelen van profielen. De standaard is do-profile.
- `--no-do-profile`: Voorkomt het opnieuw verzamelen van profielen.
- `--do-prediction`: Triggert het opnieuw berekenen van voorspellingen. De standaard is do-prediction.
- `--no-do-prediction`: Voorkomt het opnieuw berekenen van voorspellingen.
- `--do-alert-status`: Triggert het opnieuw berekenen van alert-statussen. De standaard is do-alert-status.
- `--no-do-alert-status`: Voorkomt het opnieuw berekenen van alert-statussen.
- `--timing`, `-tm`: Toont de duur van het inspectieproces na voltooiing.
  
### Voorbeeld
  
Om data te inspecteren voor het project `ProjectA` van 1 januari 2024 tot 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Om slechts een specifieke tabel te inspecteren en het opnieuw berekenen van voorspellingen af te dwingen:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Dit commando is nuttig voor het genereren van bijgewerkte profielen en voorspellingen, het monitoren van data-integriteit en het beheren van alerts binnen een opgegeven projecttijdvak.

## Gebruik van het `tls-status`-commando

Het `tls-status`-commando in de ***digna*** CLI wordt gebruikt om de status van het Traffic Light System (TLS) op te vragen voor een specifieke tabel binnen een project op een bepaalde datum. Het Traffic Light System geeft inzicht in de gezondheid en kwaliteit van de data, en geeft eventuele problemen of waarschuwingen aan die aandacht behoeven.
  
### Commando Gebruik
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor de TLS-status wordt opgevraagd (vereist).
- **TABLE_NAME**: De specifieke tabel binnen het project waarvoor de TLS-status nodig is (vereist).
- **DATE**: De datum waarvoor de TLS-status wordt opgevraagd, doorgaans in het formaat %Y-%m-%d (vereist).
  
### Voorbeeld
  
Om de TLS-status te controleren voor een tabel genaamd UserData in het project ProjectA op 1 juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Dit commando helpt gebruikers bij het monitoren en onderhouden van datakwaliteit door een duidelijke en bruikbare statusrapportage te geven op basis van vooraf gedefinieerde criteria.

## Gebruik van het `list-projects`-commando
  
Het `list-projects`-commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
### Commando Gebruik
  
```bash
dignacli list-projects
```

Dit commando is vooral nuttig voor beheerders en gebruikers die meerdere projecten beheren, en biedt een snel overzicht van de beschikbare projecten in de ***digna*** repository.

## Gebruik van het `list-ds`-commando

Het `list-ds`-commando in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare databronnen binnen een opgegeven project. Dit commando is nuttig om inzicht te krijgen in de data-assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

### Commando Gebruik
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenten
- **PROJECT_NAME**: De naam van het project waarvan de databronnen worden weergegeven (vereist).
  
### Voorbeeld
  
Om alle databronnen in het project `ProjectA` te tonen:
  
```bash
dignacli list-ds ProjectA
```
  
Dit commando geeft gebruikers een overzicht van de databronnen die in een project beschikbaar zijn, waardoor zij het datalandschap effectiever kunnen navigeren en beheren.