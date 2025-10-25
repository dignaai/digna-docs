---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.11. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Denna sida dokumenterar hela uppsättningen kommandon som finns tillgängliga i ***digna*** CLI-release **2024.11**, inklusive användningsexempel och alternativ.


---
## CLI Basics

---

## Using `help` Option

Alternativet `--help` ger information om tillgängliga kommandon och deras användning. Det finns två huvud sätt att använda detta alternativ:

1. **Visa generell hjälp:**
   
    Använd --help omedelbart efter nyckelordet ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Hjälp för specifika kommandon:**  
  
    För detaljerad information om ett specifikt kommando, lägg till `--help` efter det kommandot.
    Till exempel, för att få hjälp med kommandot `add-user`, kör:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Command Description:** Ger en detaljerad beskrivning av vad kommandot gör.  
     - **Syntax:** Visar exakt syntax, inklusive obligatoriska och valfria argument.  
     - **Options:** Lista på eventuella alternativ som är specifika för kommandot, tillsammans med deras förklaringar.  
     - **Examples:** Ger exempel på hur kommandot kan köras på ett effektivt sätt.

  
## Using `check-repo-connection` Command

Kommandot check-repo-connection är ett verktyg i ***digna*** CLI som är utformat för att testa anslutning och åtkomst till ett angivet ***digna*** repository. Detta kommando säkerställer att CLI kan interagera med repositoryt.
      
### Command Usage
```bash
dignacli check-repo-connection
```

Vid lyckad körning returnerar kommandot en bekräftelse på anslutningen, tillsammans med detaljer om repositoryt: Repository version, Host, Database och Schema.  
  
Om repository-anslutningen inte lyckas, kontrollera filen config.toml för korrekta konfigurationsinställningar.

## Using ‘version’ command

För att kontrollera installerad version av *dignacli*, använd alternativet --version.  
  
### Command Usage
```bash
dignacli --version
```
  
### Example Output
```bash
dignacli version 2024.11
```

## Using logging options
  
Som standard är konsolutmatningen från ***digna***-kommandon avsedd att vara minimalistisk. De flesta kommandon erbjuder möjligheten att visa ytterligare information med följande alternativ:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” och ”debug” anger detaljnivån, medan alternativet ”logfile” tillåter att omdirigera utdata så att det strömmas till en fil istället för till konsolfönstret.

# User Management

## Using ‘add-user’ command
  
Kommandot add-user i ***digna*** CLI används för att lägga till en ny användare i ***digna***-systemet
  
### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Arguments

- **USER_NAME**: Användarnamnet för den nya användaren (obligatoriskt).
- **USER_FULL_NAME**: Den fullständiga namn för den nya användaren (obligatoriskt).
- **USER_PASSWORD**: Lösenordet för den nya användaren (obligatoriskt).

### Options

- `--is_superuser`, `-su`: Flagga för att beteckna den nya användaren som administratör.
- `--valid_until`, `-vu`: Anger ett utgångsdatum för användarkontot i formatet `YYYY-MM-DD HH:MI:SS`. Om det inte anges har kontot inget utgångsdatum.

### Example

För att lägga till en ny användare med användarnamn `jdoe`, fullständigt namn `John Doe` och lösenord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
För att lägga till en ny användare och sätta ett utgångsdatum för kontot:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Using `delete-user` command
  
Kommandot `delete-user` i ***digna*** CLI används för att ta bort en befintlig användare från ***digna***-systemet.
  
### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
### Arguments
- **USER_NAME**: Användarnamnet för den användare som ska tas bort (obligatoriskt). Detta är det enda argument som krävs av kommandot.

### Example
```bash
dignacli delete-user jdoe
```
  
Genom att köra detta kommando tas användaren `jdoe` bort från ***digna***-systemet, deras åtkomst återkallas och deras associerade data och behörigheter tas bort från repositoryt.

## Using `modify-user` Command

Kommandot `modify-user` i ***digna*** CLI används för att uppdatera uppgifterna för en befintlig användare i ***digna***-systemet.

### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Arguments
  
- **USER_NAME**: Användarnamnet för den användare som ska ändras (obligatoriskt).
- **USER_FULL_NAME**: Det nya fullständiga namnet för användaren (obligatoriskt).
  
### Options  
  
- `--is_superuser`, `-su`: Sätter användaren som superuser och ger utökade privilegier. Denna flagga kräver inget värde.  
- `--valid_until`, `-vu`: Anger ett utgångsdatum för användarkontot i formatet YYYY-MM-DD HH:MI:SS. Om det inte anges förblir kontot giltigt på obestämd tid.  
  
### Example
  
För att ändra fullständiga namnet för användaren `jdoe` till ”Johnathan Doe” och sätta användaren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Using `modify-user-pwd` Command
  
Kommandot `modify-user-pwd` i ***digna*** CLI används för att byta lösenord för en befintlig användare i ***digna***-systemet.
  
### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Arguments
  
- **USER_NAME**: Användarnamnet för den användare vars lösenord ska ändras (obligatoriskt).
- **USER_PWD**: Det nya lösenordet för användaren (obligatoriskt).
  
### Example
  
För att byta lösenord för användaren `jdoe` till `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Using `list-users` Command

Kommandot `list-users` i ***digna*** CLI visar en lista över alla användare som är registrerade i ***digna***-systemet.

### Command Usage

```bash
dignacli list-users
```

När detta kommando körs i ***digna*** CLI ansluter det till ***digna***-repositoryt och listar alla användare, visar deras ID, användarnamn, fullständiga namn, superuser-status och utgångs-tidsstämplar.

# Repository Management

### Using `upgrade-repo` Command
  
Kommandot `upgrade-repo` i ***digna*** CLI används för att uppgradera eller initiera ***digna***-repositoryt. Detta kommando är viktigt för att tillämpa uppdateringar eller sätta upp repository-infrastrukturen för första gången.
  
### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s`: När detta är aktiverat körs kommandot i simuleringsläge, vilket skriver ut de SQL-satser som skulle köras men utför dem inte. Detta är användbart för att förhandsgranska ändringar utan att göra modifieringar i repositoryt.  

  
### Example
  
För att uppgradera ***digna***-repositoryt kan du köra kommandot utan några alternativ:
  
```bash
dignacli upgrade-repo
```  
För att köra uppgraderingen i simuleringsläge (för att se SQL-satserna utan att tillämpa dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Detta kommando är avgörande för att underhålla ***digna***-systemet och säkerställa att databasschemat och andra repository-komponenter är uppdaterade med den senaste versionen av mjukvaran.

## Using `encrypt` Command
  
Kommandot `encrypt` i ***digna*** CLI används för att kryptera ett lösenord.
  
### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Arguments
- **PASSWORD**: Lösenordet som ska krypteras (obligatoriskt).
  
### Example
  
För att kryptera ett lösenord behöver du ange lösenordet som ett argument.   
Till exempel, för att kryptera lösenordet `mypassword123`, skulle du använda:
```bash
dignacli encrypt mypassword123
```
Detta kommando returnerar den krypterade versionen av det angivna lösenordet, som sedan kan användas i säkra sammanhang. Om lösenordsargumentet inte anges kommer CLI att visa ett fel som indikerar det saknade argumentet.

## Using `generate-key` Command
  
Kommandot `generate-key` används för att generera en Fernet-nyckel, vilket är nödvändigt för att säkra lösenord som lagras i ***digna***-repositoryt.
  
### Command Usage
```bash
dignacli generate-key
```
  
# Data Management

## Using `clean-up` Command

Kommandot `clean-up` i ***digna*** CLI används för att ta bort profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando är viktigt för hantering av datalivscykeln och hjälper till att hålla en organiserad och effektiv data-miljö genom att rensa föråldrade eller onödiga data.

### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: Namnet på projektet från vilket data ska tas bort (obligatoriskt). Genom att använda nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa detta kommando.
- **FROM_DATE**: Startdatum och tid för datarensningen. Godkända format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datarensningen, med samma format som FROM_DATE (obligatoriskt).
  
### Options
  
- `--table-name`, `-tn`: Begränsar clean-up operationen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar så att clean-up endast gäller tabeller som innehåller den angivna delsträngen i sina namn.
- `--timing`, `-tm`: Visar tidsåtgången för clean-up-processen efter att den slutförts.
- `--help`: Visar hjälpinformation för clean-up-kommandot och avslutar.
  
### Example
  
För att ta bort data från projektet ProjectA mellan 1 januari 2023 och 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
För att endast ta bort data från en specifik tabell med namnet `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Detta kommando hjälper till att hantera datalagring och säkerställa att repositoryt endast innehåller relevant information.

## Using `inspect` Command

Kommandot `inspect` i ***digna*** CLI används för att skapa profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando hjälper till att analysera och övervaka data över en definierad period.

### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: Namnet på projektet för vilket data ska inspekteras (obligatoriskt). Genom att använda nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa detta kommando.
- **FROM_DATE**: Startdatum och tid för datainspektionen. Godkända format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datainspektionen, med samma format som FROM_DATE (obligatoriskt).
  
### Options

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar så att endast tabeller som innehåller den angivna delsträngen i sina namn inspekteras.
- `--do-profile`: Triggar ominsamling av profiler. Standard är do-profile.
- `--no-do-profile`: Förhindrar ominsamling av profiler.
- `--do-prediction`: Triggar omberäkning av prediktioner. Standard är do-prediction.
- `--no-do-prediction`: Förhindrar omberäkning av prediktioner.
- `--do-alert-status`: Triggar omberäkning av alert-status. Standard är do-alert-status.
- `--no-do-alert-status`: Förhindrar omberäkning av alert-status.
- `--timing`, `-tm`: Visar varaktigheten av inspektionsprocessen efter slutförande.
  
### Example
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
För att inspektera endast en specifik tabell och tvinga omberäkning av prediktioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Detta kommando är användbart för att generera uppdaterade profiler och prediktioner, övervaka dataintegritet och hantera larmsystem inom en angiven projektperiod.

## Using `tls-status` Command

Kommandot `tls-status` i ***digna*** CLI används för att fråga status för Traffic Light System (TLS) för en specifik tabell inom ett projekt på ett givet datum. Trafikljussystemet ger insikter om datahälsa och kvalitet och indikerar eventuella problem eller varningar som kan behöva åtgärdas.
  
### Command Usage
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Arguments
  
- **PROJECT_NAME**: Namnet på projektet för vilket TLS-statusen frågas (obligatoriskt).
- **TABLE_NAME**: Den specifika tabellen inom projektet för vilken TLS-status behövs (obligatoriskt).
- **DATE**: Datumet för vilket TLS-statusen efterfrågas, vanligtvis i formatet %Y-%m-%d (obligatoriskt).
  
### Example
  
För att kontrollera TLS-status för en tabell kallad UserData i projektet ProjectA den 1 juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Detta kommando hjälper användare att övervaka och upprätthålla datakvalitet genom att tillhandahålla en tydlig och handlingsbar statusrapport baserad på fördefinierade kriterier.

## Using `list-projects` Command
  
Kommandot `list-projects` i ***digna*** CLI används för att visa en lista över alla tillgängliga projekt inom ***digna***-systemet.
  
### Command Usage
  
```bash
dignacli list-projects
```

Detta kommando är särskilt användbart för administratörer och användare som hanterar flera projekt och ger en snabb översikt över de tillgängliga projekten i ***digna***-repositoryt.

## Using `list-ds` Command

Kommandot `list-ds` i ***digna*** CLI används för att visa en lista över alla tillgängliga datakällor inom ett angivet projekt. Detta kommando är användbart för att förstå de dataresurser som är tillgängliga för analys och hantering i ***digna***-systemet.

### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Arguments
- **PROJECT_NAME**: Namnet på projektet för vilket datakällorna listas (obligatoriskt).
  
### Example
  
För att lista alla datakällor i projektet med namnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Detta kommando ger användare en översikt över de datakällor som finns i ett projekt och hjälper dem att navigera och hantera datalandskapet mer effektivt.