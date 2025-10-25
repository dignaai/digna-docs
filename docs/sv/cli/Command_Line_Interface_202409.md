---
title: digna CLI-referens 2024.09 – Kommandon & Exempel | digna-dokumentation
description: Komplett referens för digna CLI-release 2024.09. Lär dig hur du hanterar användare, repositories och data med kommandon som add-user, check-repo-connection, upgrade-repo, inspect, tls-status med mera.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basics

---

###   help

--help-alternativet ger information om tillgängliga kommandon och hur de används. Det finns två huvudsakliga sätt att använda detta alternativ:

1. **Visa allmän hjälp:**
   
    Använd --help direkt efter nyckelordet ***digna***cl  
   bash
   dignacli --help

3.  **Hämta hjälp för specifika kommandon:**  
  
    För detaljerad information om ett specifikt kommando, lägg till --help efter kommandot.
    Till exempel, för att få hjälp med kommandot add-user, kör:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Kommandobeskrivning:** Ger en detaljerad beskrivning av vad kommandot gör.  
     - **Syntax:** Visar exakt syntax, inklusive obligatoriska och valfria argument.  
     - **Alternativ:** Listar eventuella alternativ som är specifika för kommandot, tillsammans med deras förklaringar.  
     - **Exempel:** Ger exempel på hur kommandot kan köras effektivt.

  
###   check-repo-connection

Kommandot check-repo-connection är ett verktyg i ***digna*** CLI som används för att testa anslutning och åtkomst till ett angivet ***digna*** repository. Detta kommando säkerställer att CLI:n kan interagera med repositoryt.
      
##### Command Usage
bash
dignacli check-repo-connection


Vid lyckad körning skriver kommandot ut en bekräftelse på anslutningen, tillsammans med detaljer om repositoryt: Repository version, Host, Database och Schema.  
  
Om anslutningen till repositoryt inte lyckas, kontrollera filen config.toml för korrekta konfigurationsinställningar.

###   version

För att kontrollera vilken version av *dignacli* som är installerad, använd alternativet --version.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


###   logging options
  
Som standard är konsolutdata från ***digna***-kommandon avsedd att vara minimalistiska. De flesta kommandon erbjuder möjligheten att visa mer information genom följande alternativ:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” och ”debug” definierar detaljnivån, medan ”logfile”-omkopplaren låter dig omdirigera utdata så att de skrivs till en fil istället för till konsolfönstret.

## User Management

###   add-user
  
Kommandot add-user i ***digna*** CLI används för att lägga till en ny användare i ***digna***-systemet.
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Användarnamnet för den nya användaren (obligatoriskt).
- **USER_FULL_NAME**: Den nya användarens fullständiga namn (obligatoriskt).
- **USER_PASSWORD**: Lösenordet för den nya användaren (obligatoriskt).

#### Options

- --is_superuser, -su: Flagga för att utse den nya användaren som administratör.
- --valid_until, -vu: Sätter ett utgångsdatum för användarkontot i formatet YYYY-MM-DD HH:MI:SS. Om det inte anges har kontot inget utgångsdatum.

#### Example

För att lägga till en ny användare med användarnamn jdoe, fullständigt namn John Doe och lösenord password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
För att lägga till en ny användare och sätta ett utgångsdatum för kontot:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Kommandot delete-user i ***digna*** CLI används för att ta bort en befintlig användare från ***digna***-systemet.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: Användarnamnet för användaren som ska tas bort (obligatoriskt). Detta är det enda argument som krävs för kommandot.

#### Example
bash
dignacli delete-user jdoe

  
Genom att köra detta kommando tas användaren jdoe bort från ***digna***-systemet, deras åtkomst upphävs och tillhörande data och rättigheter i repositoryt tas bort.

###   modify-user

Kommandot modify-user i ***digna*** CLI används för att uppdatera uppgifter för en befintlig användare i ***digna***-systemet.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: Användarnamnet för användaren som ska ändras (obligatoriskt).
- **USER_FULL_NAME**: Det nya fullständiga namnet för användaren (obligatoriskt).
  
#### Options  
  
- --is_superuser, -su: Sätter användaren som superuser och ger utökade rättigheter. Denna flagga kräver inget värde.  
- --valid_until, -vu: Sätter ett utgångsdatum för användarkontot i formatet YYYY-MM-DD HH:MI:SS. Om det inte anges förblir kontot giltigt på obestämd tid.  
  
#### Example
  
För att ändra fullständigt namn för användaren jdoe till ”Johnathan Doe” och sätta användaren som superuser:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Kommandot modify-user-pwd i ***digna*** CLI används för att byta lösenord för en befintlig användare i ***digna***-systemet.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: Användarnamnet för användaren vars lösenord ska ändras (obligatoriskt).
- **USER_PWD**: Det nya lösenordet för användaren (obligatoriskt).
  
#### Example
  
För att byta lösenord för användaren jdoe till newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Kommandot list-users i ***digna*** CLI visar en lista över alla användare registrerade i ***digna***-systemet.

##### Command Usage

bash
dignacli list-users


Genom att köra detta kommando ansluter ***digna*** CLI till ***digna***-repositoryt och listar alla användare, visar deras ID, användarnamn, fullständiga namn, superuser-status och utgångstider.

# Repository Management

###   upgrade-repo
  
Kommandot upgrade-repo i ***digna*** CLI används för att uppgradera eller initiera ***digna***-repositoryt. Detta kommando är nödvändigt för att tillämpa uppdateringar eller sätta upp repositoryinfrastrukturen för första gången.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: När detta är aktiverat körs kommandot i simuleringsläge, vilket skriver ut de SQL-satser som skulle köras men faktiskt inte exekverar dem. Detta är användbart för att förhandsgranska ändringar utan att göra modifieringar i repositoryt.  

  
#### Example
  
För att uppgradera ***digna***-repositoryt kan du köra kommandot utan några alternativ:
  
bash
dignacli upgrade-repo
  
För att köra uppgraderingen i simuleringsläge (för att se SQL-satserna utan att tillämpa dem):
  
bash
dignacli upgrade-repo --simulation-mode

  
Detta kommando är viktigt för underhållet av ***digna***-systemet och säkerställer att databasens schema och andra repositorykomponenter är uppdaterade med den senaste programvaruversionen.

###   encrypt
  
Kommandot encrypt i ***digna*** CLI används för att kryptera ett lösenord.
  
#### Command Usage
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD**: Lösenordet som ska krypteras (obligatoriskt).
  
#### Example
  
För att kryptera ett lösenord måste du ange lösenordet som ett argument.   
Till exempel, för att kryptera lösenordet mypassword123, skulle du använda:
bash
dignacli encrypt mypassword123

Detta kommando skriver ut den krypterade versionen av det angivna lösenordet, som sedan kan användas i säkra sammanhang. Om lösenordsargumentet inte anges kommer CLI:n att visa ett fel som indikerar det saknade argumentet.

###   generate-key
  
Kommandot generate-key används för att generera en Fernet-nyckel, vilket är nödvändigt för att säkra lösenord som lagras i ***digna***-repositoryt.
  
#### Command Usage
bash
dignacli generate-key

  
## Data Management

###   clean-up

Kommandot clean-up i ***digna*** CLI används för att ta bort profiler, prediktioner och Traffic Light System-data för en eller flera datakällor inom ett angivet projekt. Detta kommando är viktigt för livscykelhantering av data och hjälper till att hålla en organiserad och effektiv data-miljö genom att rensa bort föråldrade eller onödiga data.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Namnet på projektet från vilket data ska tas bort (obligatoriskt). Om du använder nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för datarensningen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datarensningen, i samma format som FROM_DATE (obligatoriskt).
  
#### Options
  
- --table-name, -tn: Begränsar clean-up-operationen till en specifik tabell inom projektet.
- --table-filter, -tf: Filtrerar så att clean-up endast gäller tabeller som innehåller den angivna substrängen i sina namn.
- --timing, -tm: Visar tidsåtgången för clean-up-processen efter avslutad körning.
- --help: Visar hjälp för clean-up-kommandot och avslutar.
  
#### Example
  
För att ta bort data från projektet ProjectA mellan 1 januari 2023 och 30 juni 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
För att endast ta bort data från en specifik tabell som heter Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Detta kommando hjälper till att hantera lagring av data och säkerställer att repositoryt endast innehåller relevant information.

###   inspect

Kommandot inspect i ***digna*** CLI används för att skapa profiler, prediktioner och Traffic Light System-data för en eller flera datakällor inom ett angivet projekt. Detta kommando hjälper till att analysera och övervaka data över en definierad period.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Namnet på projektet som ska inspekteras (obligatoriskt). Om du använder nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för datainspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datainspektionen, i samma format som FROM_DATE (obligatoriskt).
  
#### Options

- --table-name, -tn: Begränsar inspektionen till en specifik tabell inom projektet.
- --table-filter, -tf: Filtrerar så att endast tabeller som innehåller den angivna substrängen i sina namn inspekteras.
- --force-profile: Tvingar ominsamling av profiler. Standard är force-profile.
- --no-force-profile: Förhindrar ominsamling av profiler.
- --force-prediction: Tvingar omberäkning av prediktioner. Standard är force-prediction.
- --no-force-prediction: Förhindrar omberäkning av prediktioner.
- --force-alert-status: Tvingar omberäkning av larmstatus. Standard är force-alert-status.
- --no-force-alert-status: Förhindrar omberäkning av larmstatus.
- --timing, -tm: Visar hur lång tid inspektionsprocessen tog efter avslutad körning.
- --alert-notification, -an: Skickar larmnotifikationer till prenumererade kanaler.
  
#### Example
  
För att inspektera data för projektet ProjectA från 1 januari 2024 till 31 januari 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
För att inspektera endast en specifik tabell och tvinga omberäkning av prediktioner:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Detta kommando är användbart för att generera uppdaterade profiler och prediktioner, övervaka dataintegritet och hantera larmsystem inom en angiven projektperiod.

###   tls-status

Kommandot tls-status i ***digna*** CLI används för att fråga statusen för Traffic Light System (TLS) för en specifik tabell inom ett projekt på ett angivet datum. Traffic Light System ger insikter om datans hälsa och kvalitet och indikerar eventuella problem eller larm som kan behöva åtgärdas.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Namnet på projektet för vilket TLS-statusen frågas (obligatoriskt).
- **TABLE_NAME**: Den specifika tabellen inom projektet som TLS-statusen gäller för (obligatoriskt).
- **DATE**: Datumet för vilket TLS-statusen frågas, vanligtvis i formatet %Y-%m-%d (obligatoriskt).
  
#### Example
  
För att kontrollera TLS-statusen för en tabell som heter UserData i projektet ProjectA den 1 juli 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Detta kommando hjälper användare att övervaka och upprätthålla datakvaliteten genom att tillhandahålla en tydlig och handlingsbar statusrapport baserad på fördefinierade kriterier.

###   list-projects
  
Kommandot list-projects i ***digna*** CLI används för att visa en lista över alla tillgängliga projekt i ***digna***-systemet.
  
#### Command Usage
  
bash
dignacli list-projects


Detta kommando är särskilt användbart för administratörer och användare som hanterar flera projekt och ger en snabb överblick över de projekt som finns i ***digna***-repositoryt.

###   list-ds

Kommandot list-ds i ***digna*** CLI används för att visa en lista över alla tillgängliga datakällor inom ett angivet projekt. Detta kommando är användbart för att få överblick över de dataresurser som finns för analys och hantering i ***digna***-systemet.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Namnet på projektet för vilket datakällorna listas (obligatoriskt).
  
#### Example
  
För att lista alla datakällor i projektet som heter ProjectA:
  
bash
dignacli list-ds ProjectA

  
Detta kommando ger användare en överblick över datakällorna som finns i ett projekt och hjälper dem att navigera och hantera datalandskapet mer effektivt.