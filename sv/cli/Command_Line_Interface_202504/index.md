# digna CLI Reference 2025.04
**2025-04-01**

Denna sida dokumenterar den fullständiga uppsättningen kommandon som finns tillgängliga i ***digna*** CLI-version **2025.04**, inklusive användningsexempel och alternativ.

---

## CLI-grunder

---

## Använda `help`-alternativet

Alternativet `--help` ger information om tillgängliga kommandon och deras användning. Det finns två huvudsakliga sätt att använda detta alternativ:

1. **Visa allmän hjälp:**
   
    Använd --help direkt efter nyckelordet ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Få hjälp för specifika kommandon:**  
  
    För detaljerad information om ett specifikt kommando, lägg till `--help` efter det kommandot.
    Till exempel, för att få hjälp med kommandot `add-user`, kör:
     ```bash
     dignacli add-user --help
     ```

     ### Utmatning:
      
     - **Kommandobeskrivning:** Ger en detaljerad beskrivning av vad kommandot gör.  
     - **Syntax:** Visar exakt syntax, inklusive obligatoriska och valfria argument.  
     - **Alternativ:** Lista över eventuella alternativ som är specifika för kommandot, tillsammans med deras förklaringar.  
     - **Exempel:** Ger exempel på hur man effektivt kör kommandot.  

  
## Använda kommandot `check-repo-connection`

Kommandot check-repo-connection är ett verktyg inom ***digna*** CLI som är utformat för att testa anslutningen och åtkomsten till ett angivet ***digna***-repository. Detta kommando säkerställer att CLI kan interagera med repositoryt.
      
#### Kommandoanvändning
```bash
dignacli check-repo-connection
```

Vid lyckad körning visar kommandot en bekräftelse av anslutningen, tillsammans med detaljer om repositoryt: Repository version, Host, Database och Schema.  
  
Om repository-anslutningen inte lyckas, kontrollera filen config.toml för korrekta konfigurationsinställningar.

## Använda kommandot `version`

För att kontrollera installerad version av *dignacli*, använd alternativet --version.  
  
#### Kommandoanvändning
```bash
dignacli --version
```
  
#### Exempelutmatning
```bash
dignacli version 2025.04
```

## Använda loggningsalternativ
  
Som standard är konsolutmatningen från ***digna***-kommandon avsedd att vara minimalistisk. De flesta kommandon erbjuder möjligheten att visa ytterligare information med följande alternativ:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
”verbose” och ”debug” definierar detaljnivån, medan ”logfile”-växeln tillåter att omdirigera utmatningen så att den strömmas till en fil istället för till konsolfönstret.

## Användarhantering

### Använda kommandot `add-user`
  
Kommandot add-user i ***digna*** CLI används för att lägga till en ny användare i ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argument

- **USER_NAME**: Användarnamnet för den nya användaren (obligatoriskt).
- **USER_FULL_NAME**: Den nya användarens fullständiga namn (obligatoriskt).
- **USER_PASSWORD**: Lösenordet för den nya användaren (obligatoriskt).

#### Alternativ

- `--is_superuser`, `-su`: Flagga för att ange att den nya användaren är administratör.
- `--valid_until`, `-vu`: Sätter ett utgångsdatum för användarkontot i formatet `YYYY-MM-DD HH:MI:SS`. Om det inte anges har kontot inget utgångsdatum.

#### Exempel

För att lägga till en ny användare med användarnamnet `jdoe`, fullständigt namn `John Doe` och lösenord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
För att lägga till en ny användare och sätta ett utgångsdatum för kontot:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Använda kommandot `delete-user`
  
Kommandot `delete-user` i ***digna*** CLI används för att ta bort en befintlig användare från ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli delete-user USER_NAME
```
  
##### Argument
- **USER_NAME**: Användarnamnet för den användare som ska tas bort (obligatoriskt). Detta är det enda argument som krävs för kommandot.

#### Exempel
```bash
dignacli delete-user jdoe
```
  
Att köra detta kommando tar bort användaren `jdoe` från ***digna***-systemet, återkallar deras åtkomst och tar bort tillhörande data och behörigheter från repositoryt.

### Använda kommandot `modify-user`

Kommandot `modify-user` i ***digna*** CLI används för att uppdatera uppgifter för en befintlig användare i ***digna***-systemet.

#### Kommandoanvändning
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argument
  
- **USER_NAME**: Användarnamnet för den användare som ska ändras (obligatoriskt).
- **USER_FULL_NAME**: Det nya fullständiga namnet för användaren (obligatoriskt).
  
#### Alternativ  
  
- `--is_superuser`, `-su`: Sätter användaren som superuser och ger förhöjda rättigheter. Denna flagga kräver inget värde.  
- `--valid_until`, `-vu`: Sätter ett utgångsdatum för användarkontot i formatet YYYY-MM-DD HH:MI:SS. Om det inte anges förblir kontot giltigt utan tidsbegränsning.  
  
#### Exempel
  
För att ändra fullständigt namn för användaren `jdoe` till ”Johnathan Doe” och sätta användaren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Använda kommandot `modify-user-pwd`
  
Kommandot `modify-user-pwd` i ***digna*** CLI används för att ändra lösenordet för en befintlig användare i ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argument
  
- **USER_NAME**: Användarnamnet för den användare vars lösenord ska ändras (obligatoriskt).
- **USER_PWD**: Det nya lösenordet för användaren (obligatoriskt).
  
#### Exempel
  
För att ändra lösenordet för användaren `jdoe` till `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Använda kommandot `list-users`

Kommandot `list-users` i ***digna*** CLI visar en lista över alla användare registrerade i ***digna***-systemet.

#### Kommandoanvändning

```bash
dignacli list-users
```

Att köra detta kommando i ***digna*** CLI kommer att ansluta till ***digna***-repositoryt och lista alla användare, visa deras ID, användarnamn, fullständiga namn, superuser-status och utgångstidpunkter.

## Repository-hantering

### Använda kommandot `upgrade-repo`
  
Kommandot `upgrade-repo` i ***digna*** CLI används för att uppgradera eller initiera ***digna***-repositoryt. Detta kommando är viktigt för att tillämpa uppdateringar eller för att sätta upp repository-infrastrukturen första gången.
  
#### Kommandoanvändning

```bash
dignacli upgrade-repo [options]
```
  
#### Alternativ
  
- `--simulation-mode`, `-s`: När detta aktiveras körs kommandot i simuleringsläge, vilket skriver ut SQL-satserna som skulle köras men utför dem inte faktiskt. Detta är användbart för att förhandsgranska ändringar utan att göra modifieringar i repositoryt.  

  
#### Exempel
  
För att uppgradera ***digna***-repositoryt kan du köra kommandot utan några alternativ:
  
```bash
dignacli upgrade-repo
```  
För att köra uppgraderingen i simuleringsläge (för att se SQL-satserna utan att tillämpa dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Detta kommando är avgörande för att underhålla ***digna***-systemet och säkerställa att databasens schema och andra repository-komponenter är uppdaterade med den senaste versionen av programvaran.

### Använda kommandot `encrypt`
  
Kommandot `encrypt` i ***digna*** CLI används för att kryptera ett lösenord.
  
#### Kommandoanvändning
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argument
- **PASSWORD**: Lösenordet som ska krypteras (obligatoriskt).
  
#### Exempel
  
För att kryptera ett lösenord måste du ange lösenordet som ett argument.   
Till exempel, för att kryptera lösenordet `mypassword123`, skulle du använda:
```bash
dignacli encrypt mypassword123
```
Detta kommando skriver ut den krypterade versionen av det angivna lösenordet, som sedan kan användas i säkra sammanhang. Om lösenordsargumentet inte ges kommer CLI att visa ett fel som indikerar det saknade argumentet.

## Använda kommandot `generate-key`
  
Kommandot `generate-key` används för att generera en Fernet-nyckel, vilket är viktigt för att säkra lösenord som lagras i ***digna***-repositoryt.
  
#### Kommandoanvändning
```bash
dignacli generate-key
```
  
## Dat hantering

## Använda kommandot `clean-up`

Kommandot `clean-up` i ***digna*** CLI används för att ta bort profiler, prediktioner och data från trafikljussystemet för en eller flera datakällor inom ett angivet projekt. Detta kommando är viktigt för livscykelhantering av data och hjälper till att hålla en organiserad och effektiv data-miljö genom att rensa utdaterade eller onödiga data.

#### Kommandoanvändning

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet från vilket data ska tas bort (obligatoriskt). Att använda nyckelordet all-projects i detta argument instruerar ***digna*** att iterera över alla befintliga projekt och tillämpa detta kommando.
- **FROM_DATE**: Startdatum och tid för datasraderingen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datasraderingen, med samma format som FROM_DATE (obligatoriskt).
  
#### Alternativ
  
- `--table-name`, `-tn`: Begränsar clean-up-operationen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filter för att begränsa clean-up till tabeller som innehåller den angivna delsträngen i sina namn.
- `--timing`, `-tm`: Visar tidsåtgången för clean-up-processen efter slutförande.
- `--help`: Visar hjälpinformation för clean-up-kommandot och avslutar.
  
#### Exempel
  
För att ta bort data från projektet ProjectA mellan 1 januari 2023 och 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
För att endast ta bort data från en specifik tabell med namnet `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Detta kommando hjälper till att hantera datalagring och säkerställa att repositoryt endast innehåller relevant information.

## Använda kommandot `list-projects`
  
Kommandot `list-projects` i ***digna*** CLI används för att visa en lista över alla tillgängliga projekt inom ***digna***-systemet.
  
#### Kommandoanvändning
  
```bash
dignacli list-projects
```

Detta kommando är särskilt användbart för administratörer och användare som hanterar flera projekt och ger en snabb översikt över de tillgängliga projekten i ***digna***-repositoryt.

## Använda kommandot `list-ds`

Kommandot `list-ds` i ***digna*** CLI används för att visa en lista över alla tillgängliga datakällor inom ett angivet projekt. Detta kommando är användbart för att förstå vilka dataresurser som är tillgängliga för analys och hantering i ***digna***-systemet.

#### Kommandoanvändning
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet för vilket datakällorna listas (obligatoriskt).
  
#### Exempel
  
För att lista alla datakällor i projektet med namnet `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Detta kommando ger användare en översikt över de datakällor som finns i ett projekt, vilket hjälper dem att navigera och hantera datalandskapet mer effektivt.


## Använda kommandot `inspect`

Kommandot `inspect` i ***digna*** CLI används för att skapa profiler, prediktioner och data för trafikljussystemet för en eller flera datakällor inom ett angivet projekt. Detta kommando hjälper till att analysera och övervaka data över en definierad period.

#### Kommandoanvändning

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet som ska inspekteras (obligatoriskt). Att använda nyckelordet all-projects i detta argument instruerar ***digna*** att iterera över alla befintliga projekt och tillämpa detta kommando.
- **FROM_DATE**: Startdatum och tid för datainspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datainspektionen, med samma format som FROM_DATE (obligatoriskt).
  
#### Alternativ

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filter för att inspektera endast tabeller som innehåller den angivna delsträngen i sina namn.
- `--do-profile`: Triggar återinsamling av profiler. Standard är do-profile.
- `--no-do-profile`: Förhindrar återinsamling av profiler.
- `--do-prediction`: Triggar omberäkning av prediktioner. Standard är do-prediction.
- `--no-do-prediction`: Förhindrar omberäkning av prediktioner.
- `--do-alert-status`: Triggar omberäkning av alert-status. Standard är do-alert-status.
- `--no-do-alert-status`: Förhindrar omberäkning av alert-status.
- `--iterative`: Triggar inspektion av en period med dagliga iterationer. Standard är iterative.
- `--no-iterative`: Triggar inspektion av hela perioden i ett svep.
- `--enable_notification`, `-en`: Aktiverar utskick av notifikationer vid larm.
- `--timing`, `-tm`: Visar tidsåtgången för inspektionsprocessen efter slutförande.
  
#### Exempel
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
För att inspektera endast en specifik tabell och tvinga omberäkning av prediktioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Detta kommando är användbart för att generera uppdaterade profiler och prediktioner, övervaka dataintegritet och hantera larmsystem inom en angiven projekttidsram.

## Använda kommandot `tls-status`

Kommandot `tls-status` i ***digna*** CLI används för att fråga status för Trafikljussystemet (TLS) för en specifik tabell inom ett projekt på ett givet datum. Trafikljussystemet ger insikter i datans hälsa och kvalitet och indikerar eventuella problem eller larm som kan behöva åtgärdas.
  
#### Kommandoanvändning
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet för vilket TLS-statusen efterfrågas (obligatoriskt).
- **TABLE_NAME**: Den specifika tabellen inom projektet för vilken TLS-status behövs (obligatoriskt).
- **DATE**: Datumet för vilket TLS-statusen efterfrågas, vanligtvis i formatet %Y-%m-%d (obligatoriskt).
  
#### Exempel
  
För att kontrollera TLS-statusen för en tabell med namnet UserData i projektet ProjectA den 1 juli 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Detta kommando hjälper användare att övervaka och upprätthålla datakvalitet genom att tillhandahålla en tydlig och åtgärdsbar statusrapport baserad på fördefinierade kriterier.

## Använda kommandot `inspect-async`

Kommandot `inspect-async` i ***digna*** CLI används för att instruera backend att asynkront utföra inspektionen för en eller flera datakällor för ett givet projekt. Om project_name är satt till all-projects kommer inspektionen att iterera över alla tillgängliga projekt och utföra inspektionen. Det returnerar ett request id som kan användas för att spåra inspektionens framsteg.

#### Kommandoanvändning

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet som ska inspekteras (obligatoriskt). Att använda nyckelordet all-projects i detta argument instruerar ***digna*** att iterera över alla befintliga projekt och tillämpa detta kommando.
- **FROM_DATE**: Startdatum och tid för datainspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datainspektionen, med samma format som FROM_DATE (obligatoriskt).
  
#### Alternativ

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filter för att inspektera endast tabeller som innehåller den angivna delsträngen i sina namn.

  
#### Exempel
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Använda kommandot `inspect-status`

Kommandot `inspect-status` i ***digna*** CLI används för att kontrollera framstegen för en asynkron inspektion baserat på request ID.

#### Kommandoanvändning

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argument
  
- **REQUEST_ID**: Request-id som returnerades av kommandot `inspect-async` 
  
#### Alternativ

- `--report_level`, `-rl`: Sätter rapportnivå: 'task' eller 'step' [default: task]
  
#### Exempel
  
För att kontrollera framstegen för en inspektion med request-id 12345 på detaljerad stegnivå:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Använda kommandot `export-ds`

Kommandot `export-ds` i ***digna*** CLI används för att skapa en export av datakällor från ***digna***-repositoryt. Som standard exporteras alla datakällor från ett angivet projekt.

#### Kommandoanvändning
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet från vilket datakällorna kommer att exporteras.

#### Alternativ

- `--table_name`, `-tn`: Exportera en viss datakälla från ett projekt.
- `--exportfile`, `-ef`: Ange filnamnet för exporten.
    
#### Exempel
  
För att exportera alla datakällor från projektet med namnet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Detta kommando exporterar alla datakällor från `ProjectA` som ett JSON-dokument som kan importeras till ett annat projekt eller ***digna***-repository.

## Använda kommandot `import-ds`

Kommandot `import-ds` i ***digna*** CLI används för att importera datakällor till ett målsprojekt och skapa en importrapport.

#### Kommandoanvändning
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet till vilket datakällorna kommer att importeras.
- **EXPORT_FILE**: Filnamnet för exportfilen som ska importeras.

#### Alternativ

- `--output-file`, `-o`: Fil för att spara importrapporten (om inte angiven skrivs den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format för att spara importrapporten (json, csv).
    
#### Exempel
  
För att importera alla datakällor från exportfilen `my_export.json` till `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen visar detta kommando även en rapport över importerade och hoppade objekt. Endast nya datakällor kommer att importeras till `ProjectB`. För att ta reda på vilka objekt som skulle importeras och hoppas över kan du använda kommandot `plan-import-ds`

## Använda kommandot `plan-import-ds`

Kommandot `plan-import-ds` i ***digna*** CLI används för att planera import av datakällor till ett målsprojekt och skapa en importrapport (utan att faktiskt importera).

#### Kommandoanvändning
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet till vilket datakällorna skulle importeras.
- **EXPORT_FILE**: Filnamnet för exportfilen som ska analyseras före import.

#### Alternativ

- `--output-file`, `-o`: Fil för att spara importrapporten (om inte angiven skrivs den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format för att spara importrapporten (json, csv).
    
#### Exempel
  
För att kontrollera vilka datakällor som skulle importeras och vilka som skulle hoppas över från exportfilen `my_export.json` vid import till `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Detta kommando visar endast en importplan över objekt som skulle importeras och hoppas över.