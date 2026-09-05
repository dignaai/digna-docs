# digna CLI Reference 2026.01
**2026-01-15**

Denna sida dokumenterar hela uppsättningen kommandon som finns tillgängliga i ***digna*** CLI-release **2026.01**, inklusive användningsexempel och alternativ.

---

## CLI-grunder

---

### help
`--help`-alternativet ger information om tillgängliga kommandon och hur de används. Det finns två huvudsakliga sätt att använda detta alternativ:

1. **Visa generell hjälp:**
   
    Använd --help omedelbart efter nyckelordet `dignacli`  
   ```bash
   dignacli --help
   ```

2. **Få hjälp för specifika kommandon:**  
  
    För detaljerad information om ett specifikt kommando, lägg till `--help` efter det kommandot.
    Till exempel, för att få hjälp med kommandot `add-user`, kör:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Kommandombeskrivning:** Ger en detaljerad beskrivning av vad kommandot gör.  
     - **Syntax:** Visar den exakta syntaxen, inklusive obligatoriska och valfria argument.  
     - **Alternativ:** Lista över alternativ som är specifika för kommandot, tillsammans med deras förklaringar.  
     - **Exempel:** Ger exempel på hur kommandot kan köras effektivt.

### check-config

Kommandot check-config är ett verktyg i ***digna*** CLI som är utformat för att testa konfigurationen av ***digna***. Detta kommando säkerställer att ***digna***-komponenterna kan hitta nödvändiga konfigurationselement i config.toml.

#### Alternativ

- `--configpath`, `-cp`: Fil eller katalog som innehåller konfigurationen. Om det inte anges används ../config.toml.
      
#### Kommandoanvändning
```bash
dignacli check-config
```

Vid en lyckad körning visar kommandot en bekräftelse på att konfigurationen är komplett.  
  
Om konfigurationen verkar ofullständig kommer de saknade konfigurationselementen att listas.

  
### check-repo-connection

Kommandot check-repo-connection är ett verktyg i ***digna*** CLI som är utformat för att testa uppkoppling och åtkomst till ett angivet ***digna*** repository. Detta kommando säkerställer att CLI:n kan interagera med repositoryt.
      
#### Kommandoanvändning
```bash
dignacli check-repo-connection
```

Vid en lyckad körning visar kommandot en bekräftelse på anslutningen, tillsammans med detaljer om repositoryt: Repository-version, Host, Database och Schema.  
  
Om repository-anslutningen misslyckas, kontrollera config.toml-filen för korrekta konfigurationsinställningar.


### version

För att kontrollera den installerade versionen av *dignacli* använder du alternativet --version.  
  
#### Kommandoanvändning
```bash
dignacli --version
```
  
#### Exempelutskrift
```bash
dignacli version 2026.01
```

### loggningsalternativ
  
Som standard är konsolutskriften från ***digna***-kommandon minimalistisk. De flesta kommandon erbjuder möjlighet att visa ytterligare information genom följande alternativ:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 ”verbose” och ”debug” anger detaljnivån, medan ”logfile”-växeln tillåter omdirigering av utdata till en fil istället för konsolfönstret.

## Användarhantering

### add-user
  
Kommandot add-user i ***digna*** CLI används för att lägga till en ny användare i ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argument

- **USER_NAME**: Användarnamnet för den nya användaren (obligatoriskt).
- **USER_FULL_NAME**: Den nya användarens fullständiga namn (obligatoriskt).
- **USER_PASSWORD**: Lösenordet för den nya användaren (obligatoriskt).

#### Alternativ

- `--is_superuser`, `-su`: Flagga för att ange den nya användaren som administratör.
- `--valid_until`, `-vu`: Sätter ett utgångsdatum för användarkontot i formatet `YYYY-MM-DD HH:MI:SS`. Om det inte anges har kontot inget utgångsdatum.

#### Exempel

För att lägga till en ny användare med användarnamn `jdoe`, fullständigt namn `John Doe` och lösenord `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
För att lägga till en ny användare och sätta ett utgångsdatum för kontot:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Kommandot `delete-user` i ***digna*** CLI används för att ta bort en befintlig användare från ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli delete-user USER_NAME
```
  
#### Argument
- **USER_NAME**: Användarnamnet för användaren som ska tas bort (obligatoriskt). Detta är det enda argument som krävs för kommandot.

#### Exempel
```bash
dignacli delete-user jdoe
```
  
Genom att köra detta kommando tas användaren `jdoe` bort från ***digna***-systemet, deras åtkomst återkallas och associerade data och rättigheter i repositoryt tas bort.

### modify-user

Kommandot `modify-user` i ***digna*** CLI används för att uppdatera uppgifterna för en befintlig användare i ***digna***-systemet.

#### Kommandoanvändning
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argument
  
- **USER_NAME**: Användarnamnet för den användare som ska ändras (obligatoriskt).
- **USER_FULL_NAME**: Det nya fullständiga namnet för användaren (obligatoriskt).
  
#### Alternativ  
  
- `--is_superuser`, `-su`: Sätter användaren som superuser, vilket ger upphöjda privilegier. Denna flagga kräver inget värde.  
- `--valid_until`, `-vu`: Sätter ett utgångsdatum för användarkontot i formatet YYYY-MM-DD HH:MI:SS. Om det inte anges förblir kontot giltigt på obestämd tid.  
  
#### Exempel
  
För att ändra fullständigt namn för användaren `jdoe` till “Johnathan Doe” och sätta användaren som superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Kommandot `modify-user-pwd` i ***digna*** CLI används för att ändra lösenordet för en befintlig användare i ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argument
  
- **USER_NAME**: Användarnamnet för den användare vars lösenord ska ändras (obligatoriskt).
- **USER_PWD**: Det nya lösenordet för användaren (obligatoriskt).
  
#### Exempel
  
För att ändra lösenordet för användaren `jdoe` till `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Kommandot `list-users` i ***digna*** CLI visar en lista över alla användare registrerade i ***digna***-systemet.

#### Kommandoanvändning

```bash
dignacli list-users
```

När du kör detta kommando ansluter ***digna*** CLI till ***digna***-repositoryt och listar alla användare, och visar deras ID, användarnamn, fullständiga namn, superuser-status och utgångstidpunkter.

## Repository-hantering

### upgrade-repo
  
Kommandot `upgrade-repo` i ***digna*** CLI används för att uppgradera eller initiera ***digna***-repositoryt. Detta kommando är viktigt för att tillämpa uppdateringar eller ställa in repositoryinfrastrukturen första gången.
  
#### Kommandoanvändning

```bash
dignacli upgrade-repo [options]
```
  
#### Alternativ
  
- `--simulation-mode`, `-s`: När detta är aktiverat körs kommandot i simuleringsläge, vilket skriver ut SQL-satserna som skulle köras men utför dem inte. Detta är användbart för att förhandsgranska ändringar utan att göra faktiska modifieringar i repositoryt.  

  
#### Exempel
  
För att uppgradera ***digna***-repositoryt kan du köra kommandot utan några alternativ:
  
```bash
dignacli upgrade-repo
```  
För att köra uppgraderingen i simuleringsläge (för att se SQL-satser utan att tillämpa dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Detta kommando är avgörande för att underhålla ***digna***-systemet, och säkerställer att databasschemat och andra repository-komponenter är uppdaterade med den senaste versionen av mjukvaran.

### encrypt
  
Kommandot `encrypt` i ***digna*** CLI används för att kryptera ett lösenord.
  
#### Kommandoanvändning
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argument
- **PASSWORD**: Lösenordet som ska krypteras (obligatoriskt).
  
#### Exempel
  
För att kryptera ett lösenord måste du ange lösenordet som ett argument.   
Till exempel, för att kryptera lösenordet `mypassword123`, använder du:
```bash
dignacli encrypt mypassword123
```
Detta kommando skriver ut den krypterade versionen av det angivna lösenordet, som sedan kan användas i säkra sammanhang. Om lösenordsargumentet inte anges kommer CLI:n att visa ett fel som anger det saknade argumentet.

### generate-key
  
Kommandot `generate-key` används för att generera en Fernet-nyckel, vilket är nödvändigt för att säkra lösenord som lagras i ***digna***-repositoryt.
  
#### Kommandoanvändning
```bash
dignacli generate-key
```
  
## Datahantering

### clean-up

Kommandot `clean-up` i ***digna*** CLI används för att ta bort profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando är viktigt för hantering av datas livscykel och hjälper till att hålla en organiserad och effektiv data-miljö genom att rensa föråldrade eller onödiga data.

#### Kommandoanvändning

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet från vilket data ska tas bort (obligatoriskt). Genom att använda nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för datarensningen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datarensningen, med samma format som FROM_DATE (obligatoriskt).
  
#### Alternativ
  
- `--table-name`, `-tn`: Begränsar clean-up-operationen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar för att begränsa clean-up till tabeller som innehåller den angivna substrängen i sina namn.
- `--timing`, `-tm`: Visar tidsåtgången för clean-up-processen efter att den slutförts.
- `--help`: Visar hjälpinformation för clean-up-kommandot och avslutar.
  
#### Exempel
  
För att ta bort data från projektet ProjectA mellan 1 januari 2023 och 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
För att ta bort data endast från en specifik tabell med namn `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Detta kommando hjälper till att hantera datalagring och säkerställer att repositoryt endast innehåller relevant information.

### remove-orphans
  
Kommandot `remove-orphans` i ***digna*** CLI används för hushållsskötsel i ***digna***-repositoryt.  
När en användare tar bort projekt eller datakällor så kvarstår profiler och prediktioner i repositoryt. Med detta kommando tas sådana föräldralösa rader bort från repositoryt.
  
#### Kommandoanvändning
  
```bash
dignacli list-projects
```

### list-projects
  
Kommandot `list-projects` i ***digna*** CLI används för att visa en lista över alla tillgängliga projekt inom ***digna***-systemet.
  
#### Kommandoanvändning
  
```bash
dignacli list-projects
```

Detta kommando är särskilt användbart för administratörer och användare som hanterar flera projekt, och ger en snabb överblick över tillgängliga projekt i ***digna***-repositoryt.

### list-ds

Kommandot `list-ds` i ***digna*** CLI används för att visa en lista över alla tillgängliga datakällor inom ett angivet projekt. Detta kommando är användbart för att få en överblick över de dataresurser som finns för analys och hantering i ***digna***-systemet.

#### Kommandoanvändning
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet för vilket datakällorna ska listas (obligatoriskt).
  
#### Exempel
  
För att lista alla datakällor i projektet med namn `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Detta kommando ger användare en överblick över de datakällor som finns i ett projekt, vilket hjälper dem att navigera och hantera datalandskapet mer effektivt.


### inspect

Kommandot `inspect` i ***digna*** CLI används för att skapa profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando hjälper till att analysera och övervaka data över en definierad period. Efter slutförd inspektion returneras värdet för det beräknade trafikljussystemet:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Kommandoanvändning

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet som data ska inspekteras för (obligatoriskt). Genom att använda nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för datainspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datainspektionen, med samma format som FROM_DATE (obligatoriskt).
  
#### Alternativ

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar för att inspektera endast tabeller som innehåller den angivna substrängen i sina namn.
- `--enable_notification`, `-en`: Aktiverar utskick av notifikationer vid larm.
- `--bypass-backend`, `-bb`: Hoppa över backend och kör inspektionen direkt från CLI (endast för teständamål!).

  
#### Exempel
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
För att inspektera endast en specifik tabell och tvinga omberäkning av prediktioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Detta kommando är användbart för att generera uppdaterade profiler och prediktioner, övervaka dataintegritet och hantera larmsystem inom en angiven projektperiod.

### inspect-async

Kommandot `inspect-async` i ***digna*** CLI används för att skapa profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando hjälper till att analysera och övervaka data över en definierad period. I kontrast till kommandot `inspect-async` väntar detta inte på att inspektionen ska slutföras.
Istället returneras request id för den inskickade inspektionsförfrågan. För att fråga efter inspektionens framsteg, använd kommandot `inspect-status`

#### Kommandoanvändning

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet som data ska inspekteras för (obligatoriskt). Genom att använda nyckelordet all-projects i detta argument instrueras ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för datainspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för datainspektionen, med samma format som FROM_DATE (obligatoriskt).
  
#### Alternativ

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar för att inspektera endast tabeller som innehåller den angivna substrängen i sina namn.
- `--enable_notification`, `-en`: Aktiverar utskick av notifikationer vid larm.

  
#### Exempel
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Kommandot `inspect-status` i ***digna*** CLI används för att kontrollera framstegen för en asynkron inspektion baserat på request ID.

#### Kommandoanvändning

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argument
  
- **REQUEST_ID**: Request-id:t som returnerades av kommandot `inspect-async` 
  
#### Exempel
  
För att kontrollera framstegen för en inspektion med request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Kommandot `inspect-cancel` i ***digna*** CLI används för att avbryta inspektioner baserat på request-id eller för att avbryta alla aktuella förfrågningar.

#### Kommandoanvändning

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argument
  
- **REQUEST_ID**: Request-id:t som returnerades av kommandot `inspect-async` 
  
#### Exempel
  
För att avbryta inspektionen med request-id 12345:
  
```bash
dignacli inspect-cancel 12345
```

För att avbryta alla förfrågningar som för närvarande körs eller väntar:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Kommandot `export-ds` i ***digna*** CLI används för att skapa en export av datakällor från ***digna***-repositoryt. Som standard exporteras alla datakällor från ett angivet projekt.

#### Kommandoanvändning
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet från vilket datakällorna kommer att exporteras.

#### Alternativ

- `--table_name`, `-tn`: Exportera en specifik datakälla från ett projekt.
- `--exportfile`, `-ef`: Ange filnamnet för exporten.
    
#### Exempel
  
För att exportera alla datakällor från projektet med namn `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Detta kommando exporterar alla datakällor från `ProjectA` som ett JSON-dokument som kan importeras till ett annat projekt eller ***digna***-repository.

### import-ds

Kommandot `import-ds` i ***digna*** CLI används för att importera datakällor till ett målsprojekt och skapa en importrapport.

#### Kommandoanvändning
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet till vilket datakällorna kommer att importeras.
- **EXPORT_FILE**: Filnamnet på exportfilen med datakällor som ska importeras.

#### Alternativ

- `--output-file`, `-o`: Fil för att spara importrapporten (om det inte anges skrivs den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format för att spara importrapporten (json, csv).
    
#### Exempel
  
För att importera alla datakällor från exportfilen `my_export.json` till `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen visar detta kommando även en rapport över importerade och hoppade objekt. Endast nya datakällor kommer att importeras till `ProjectB`. För att ta reda på vilka objekt som skulle importeras och hoppas över kan du använda kommandot `plan-import-ds`

### plan-import-ds

Kommandot `plan-import-ds` i ***digna*** CLI används för att analysera en exportfil innan import och skapa en plan/rapport över vad som skulle importeras.

#### Kommandoanvändning
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet till vilket datakällorna skulle importeras.
- **EXPORT_FILE**: Filnamnet på exportfilen med datakällor som ska analyseras innan import.

#### Alternativ

- `--output-file`, `-o`: Fil för att spara rapporten (om det inte anges skrivs den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format för att spara rapporten (json, csv).
    
#### Exempel
  
För att kontrollera vilka datakällor som skulle importeras och vilka som skulle hoppas över från exportfilen `my_export.json` när de importeras till `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Detta kommando visar endast en importplan över objekt som skulle importeras och hoppas över.