# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basisprincipes

---

###   help

De --help-optie geeft informatie over beschikbare commando's en hun gebruik. Er zijn twee hoofdmanieren om deze optie te gebruiken:

1. **Algemene help weergeven:**
   
    Gebruik --help direct na het sleutelwoord ***dignacli***  
   bash
   dignacli --help

3.  **Hulp voor specifieke commando's opvragen:**  
  
    Voor gedetailleerde informatie over een specifiek commando, voeg --help toe aan dat commando.  
    Bijvoorbeeld, om hulp te krijgen bij het commando add-user, voer uit:
     bash
     dignacli add-user --help
     

     ### uitvoer:
      
     - **Beschrijving van het commando:** Geeft een gedetailleerde beschrijving van wat het commando doet.  
     - **Syntax:** Toont de exacte syntax, inclusief verplichte en optionele argumenten.  
     - **Opties:** Lijst met opties die specifiek zijn voor het commando, met uitleg.  
     - **Voorbeelden:** Voorbeelden van hoe het commando effectief uitgevoerd kan worden.

  
###   check-repo-connection

Het commando check-repo-connection is een hulpmiddel binnen de ***digna*** CLI om de connectiviteit en toegang tot een opgegeven ***digna*** repository te testen. Dit commando controleert of de CLI met de repository kan communiceren.
      
##### Gebruik van het commando
bash
dignacli check-repo-connection


Bij succesvolle uitvoering geeft het commando een bevestiging van de verbinding, samen met details over de repository: Repository-versie, Host, Database en Schema.  
  
Als de repository-verbinding niet succesvol is, controleer dan het bestand config.toml op correcte configuratie-instellingen.

###   version

Om de geïnstalleerde versie van *dignacli* te controleren, gebruik de --version optie.  
  
#### Gebruik van het commando
bash
dignacli --version

  
#### Voorbeelduitvoer
bash
dignacli version 2024.09


###   logging options
  
Standaard is de console-uitvoer van de ***digna*** commando's minimaal. De meeste commando's bieden de mogelijkheid om extra informatie te tonen met de volgende opties:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 “verbose” en “debug” bepalen het detailniveau, terwijl de “logfile” schakelaar het mogelijk maakt de uitvoer naar een bestand te sturen in plaats van naar het consolevenster.

## Gebruikersbeheer

###   add-user
  
Het commando add-user in de ***digna*** CLI wordt gebruikt om een nieuwe gebruiker toe te voegen aan het ***digna*** systeem.
  
#### Gebruik van het commando
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenten

- **USER_NAME**: De gebruikersnaam voor de nieuwe gebruiker (vereist).
- **USER_FULL_NAME**: De volledige naam van de nieuwe gebruiker (vereist).
- **USER_PASSWORD**: Het wachtwoord voor de nieuwe gebruiker (vereist).

#### Opties

- --is_superuser, -su: Vlag om de nieuwe gebruiker als beheerder aan te wijzen.
- --valid_until, -vu: Stelt een vervaldatum in voor het gebruikersaccount in het formaat YYYY-MM-DD HH:MI:SS. Als niet ingesteld, heeft het account geen vervaldatum.

#### Voorbeeld

Om een nieuwe gebruiker toe te voegen met gebruikersnaam jdoe, volledige naam John Doe, en wachtwoord password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Om een nieuwe gebruiker toe te voegen en een vervaldatum voor het account in te stellen:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Het commando delete-user in de ***digna*** CLI wordt gebruikt om een bestaande gebruiker uit het ***digna*** systeem te verwijderen.
  
##### Gebruik van het commando
bash
dignacli delete-user USER_NAME

  
#### Argumenten
- **USER_NAME**: De gebruikersnaam van de te verwijderen gebruiker (vereist). Dit is het enige vereiste argument van het commando.

#### Voorbeeld
bash
dignacli delete-user jdoe

  
Het uitvoeren van dit commando verwijdert de gebruiker jdoe uit het ***digna*** systeem, intrekking van hun toegang en het verwijderen van bijbehorende gegevens en permissies uit de repository.

###   modify-user

Het commando modify-user in de ***digna*** CLI wordt gebruikt om de gegevens van een bestaande gebruiker in het ***digna*** systeem bij te werken.

##### Gebruik van het commando
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker die gewijzigd moet worden (vereist).
- **USER_FULL_NAME**: De nieuwe volledige naam voor de gebruiker (vereist).
  
#### Opties  
  
- --is_superuser, -su: Stelt de gebruiker in als superuser, wat verhoogde rechten geeft. Deze vlag heeft geen waarde nodig.  
- --valid_until, -vu: Stelt een vervaldatum in voor het gebruikersaccount in het formaat YYYY-MM-DD HH:MI:SS. Als niet opgegeven, blijft het account onbeperkt geldig.  
  
#### Voorbeeld
  
Om de volledige naam van gebruiker jdoe te wijzigen naar “Johnathan Doe” en de gebruiker als superuser in te stellen:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Het commando modify-user-pwd in de ***digna*** CLI wordt gebruikt om het wachtwoord van een bestaande gebruiker in het ***digna*** systeem te wijzigen.
  
##### Gebruik van het commando
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenten
  
- **USER_NAME**: De gebruikersnaam van de gebruiker wiens wachtwoord gewijzigd moet worden (vereist).
- **USER_PWD**: Het nieuwe wachtwoord voor de gebruiker (vereist).
  
#### Voorbeeld
  
Om het wachtwoord van gebruiker jdoe te wijzigen naar newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Het commando list-users in de ***digna*** CLI toont een lijst van alle gebruikers die in het ***digna*** systeem geregistreerd zijn.

##### Gebruik van het commando

bash
dignacli list-users


Het uitvoeren van dit commando in de ***digna*** CLI maakt verbinding met de ***digna*** repository en toont alle gebruikers, inclusief hun ID, gebruikersnaam, volledige naam, superuser-status en vervaltijdstempels.

# Repositorybeheer

###   upgrade-repo
  
Het commando upgrade-repo in de ***digna*** CLI wordt gebruikt om de ***digna*** repository te upgraden of te initialiseren. Dit commando is essentieel voor het toepassen van updates of het voor het eerst opzetten van de repository-infrastructuur.
  
#### Gebruik van het commando

bash
dignacli upgrade-repo [options]

  
#### Opties
  
- --simulation-mode, -s: Wanneer ingeschakeld voert deze optie het commando uit in simulatiemodus, waarbij de SQL-instructies die uitgevoerd zouden worden worden weergegeven, maar niet daadwerkelijk worden uitgevoerd. Dit is handig om wijzigingen te bekijken zonder de repository aan te passen.  

  
#### Voorbeeld
  
Om de ***digna*** repository te upgraden, kunt u het commando zonder opties uitvoeren:
  
bash
dignacli upgrade-repo
  
Om de upgrade in simulatiemodus uit te voeren (om de SQL-instructies te zien zonder ze toe te passen):
  
bash
dignacli upgrade-repo --simulation-mode

  
Dit commando is cruciaal voor het onderhouden van het ***digna*** systeem en zorgt ervoor dat het databaseschema en andere repositorycomponenten up-to-date zijn met de nieuwste versie van de software.

###   encrypt
  
Het commando encrypt in de ***digna*** CLI wordt gebruikt om een wachtwoord te versleutelen.
  
#### Gebruik van het commando
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenten
- **PASSWORD**: Het wachtwoord dat versleuteld moet worden (vereist).
  
#### Voorbeeld
  
Om een wachtwoord te versleutelen, moet u het wachtwoord als argument meegeven.  
Bijvoorbeeld, om het wachtwoord mypassword123 te versleutelen, gebruikt u:
bash
dignacli encrypt mypassword123

Dit commando geeft de versleutelde versie van het opgegeven wachtwoord terug, die daarna in beveiligde contexten gebruikt kan worden. Als het wachtwoordargument niet wordt opgegeven, zal de CLI een fout weergeven die het ontbrekende argument aangeeft.

###   generate-key
  
Het commando generate-key wordt gebruikt om een Fernet-sleutel te genereren, die essentieel is voor het beveiligen van wachtwoorden die in de ***digna*** repository worden opgeslagen.
  
#### Gebruik van het commando
bash
dignacli generate-key

  
## Data Management

###   clean-up

Het commando clean-up in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens van het Traffic Light System voor één of meer gegevensbronnen binnen een opgegeven project te verwijderen. Dit commando is essentieel voor data lifecycle-beheer en helpt een georganiseerde en efficiënte dataomgeving te behouden door verouderde of overbodige gegevens te verwijderen.

#### Gebruik van het commando

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvan gegevens verwijderd moeten worden (vereist). Het gebruik van het sleutelwoord all-projects in dit argument instrueert ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor het verwijderen van gegevens. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor het verwijderen van gegevens, met dezelfde formaten als FROM_DATE (vereist).
  
#### Opties
  
- --table-name, -tn: Beperkt de clean-up operatie tot een specifieke tabel binnen het project.
- --table-filter, -tf: Filter om de clean-up te beperken tot tabellen die de opgegeven substring in hun naam bevatten.
- --timing, -tm: Toont de duur van het clean-up proces na voltooiing.
- --help: Toont helpinformatie voor het clean-up commando en sluit af.
  
#### Voorbeeld
  
Om gegevens te verwijderen uit het project ProjectA tussen 1 januari 2023 en 30 juni 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Om gegevens alleen uit een specifieke tabel met de naam Table1 te verwijderen:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Dit commando helpt bij het beheren van datavolume en zorgt ervoor dat de repository alleen relevante informatie bevat.

###   inspect

Het commando inspect in de ***digna*** CLI wordt gebruikt om profielen, voorspellingen en gegevens voor het Traffic Light System te creëren voor één of meer gegevensbronnen binnen een opgegeven project. Dit commando helpt bij het analyseren en monitoren van gegevens over een gedefinieerde periode.

#### Gebruik van het commando

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor gegevens geïnspecteerd moeten worden (vereist). Het gebruik van het sleutelwoord all-projects in dit argument instrueert ***digna*** om over alle bestaande projecten te itereren en dit commando toe te passen.
- **FROM_DATE**: De startdatum en -tijd voor de inspectie van gegevens. Toegestane formaten zijn %Y-%m-%d, %Y-%m-%dT%H:%M:%S, of %Y-%m-%d %H:%M:%S (vereist).
- **TO_DATE**: De einddatum en -tijd voor de inspectie van gegevens, met dezelfde formaten als FROM_DATE (vereist).
  
#### Opties

- --table-name, -tn: Beperkt de inspectie tot een specifieke tabel binnen het project.
- --table-filter, -tf: Filter om alleen tabellen te inspecteren die de opgegeven substring in hun naam bevatten.
- --force-profile: Forceert het opnieuw verzamelen van profielen. Standaard is force-profile.
- --no-force-profile: Voorkomt het opnieuw verzamelen van profielen.
- --force-prediction: Forceert het opnieuw berekenen van voorspellingen. Standaard is force-prediction.
- --no-force-prediction: Voorkomt het opnieuw berekenen van voorspellingen.
- --force-alert-status: Forceert het opnieuw berekenen van alert-statussen. Standaard is force-alert-status.
- --no-force-alert-status: Voorkomt het opnieuw berekenen van alert-statussen.
- --timing, -tm: Toont de duur van het inspectieproces na voltooiing.
- --alert-notification, -an: Stuurt alertmeldingen naar geabonneerde kanalen.
  
#### Voorbeeld
  
Om gegevens te inspecteren voor het project ProjectA van 1 januari 2024 tot 31 januari 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Om alleen een specifieke tabel te inspecteren en het opnieuw berekenen van voorspellingen af te dwingen:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Dit commando is nuttig voor het genereren van bijgewerkte profielen en voorspellingen, het monitoren van dataintegriteit en het beheren van alerts binnen een opgegeven projectperiode.

###   tls-status

Het commando tls-status in de ***digna*** CLI wordt gebruikt om de status van het Traffic Light System (TLS) op te vragen voor een specifieke tabel binnen een project op een bepaalde datum. Het Traffic Light System biedt inzicht in de gezondheids- en kwaliteitsstatus van de gegevens en geeft aan of er problemen of alerts zijn die aandacht nodig hebben.
  
#### Gebruik van het commando
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenten
  
- **PROJECT_NAME**: De naam van het project waarvoor de TLS-status wordt opgevraagd (vereist).
- **TABLE_NAME**: De specifieke tabel binnen het project waarvoor de TLS-status nodig is (vereist).
- **DATE**: De datum waarvoor de TLS-status wordt opgevraagd, doorgaans in het formaat %Y-%m-%d (vereist).
  
#### Voorbeeld
  
Om de TLS-status te controleren voor een tabel met de naam UserData in het project ProjectA op 1 juli 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Dit commando helpt gebruikers bij het monitoren en behouden van datakwaliteit door een duidelijke en uitvoerbare statusrapportage te bieden op basis van vooraf gedefinieerde criteria.

###   list-projects
  
Het commando list-projects in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare projecten binnen het ***digna*** systeem.
  
#### Gebruik van het commando
  
bash
dignacli list-projects


Dit commando is vooral handig voor beheerders en gebruikers die meerdere projecten beheren en biedt een snel overzicht van de beschikbare projecten in de ***digna*** repository.

###   list-ds

Het commando list-ds in de ***digna*** CLI wordt gebruikt om een lijst weer te geven van alle beschikbare gegevensbronnen binnen een opgegeven project. Dit commando is nuttig om inzicht te krijgen in de data-assets die beschikbaar zijn voor analyse en beheer in het ***digna*** systeem.

#### Gebruik van het commando
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenten
- **PROJECT_NAME**: De naam van het project waarvoor de gegevensbronnen worden weergegeven (vereist).
  
#### Voorbeeld
  
Om alle gegevensbronnen in het project met de naam ProjectA weer te geven:
  
bash
dignacli list-ds ProjectA

  
Dit commando geeft gebruikers een overzicht van de beschikbare gegevensbronnen in een project en helpt hen bij het navigeren en beheren van het datalandschap.