---
title: digna CLI-referens 2025.09 – Kommandon & Exempel | digna-dokumentation
description: Komplett referens för digna CLI version 2025.09. Lär dig hur du hanterar användare, repository och data med kommandon som add-user, check-config, check-repo-connection, inspect, inspect-async med flera.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202509/
image: /assets/logo_square.png
---

# digna CLI-referens 2025.09
**2025-09-29**

Denna sida dokumenterar hela uppsättningen kommandon som finns i ***digna*** CLI-utgåvan **2025.09**, inklusive användningsexempel och alternativ.

---

## CLI-grunder

---

### help
Optionen `--help` ger information om tillgängliga kommandon och hur de används. Det finns två huvudsakliga sätt att använda denna option:

1. **Visa generell hjälp:**
   
   Använd --help direkt efter kommandot ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Hjälp för specifika kommandon:**  
  
   För detaljerad information om ett specifikt kommando, lägg till `--help` efter det kommandot.
   Till exempel, för att få hjälp med kommandot `add-user`, kör:
   ```bash
   dignacli add-user --help
   ```

   ### output:
      
   - **Kommando­beskrivning:** Ger en detaljerad beskrivning av vad kommandot gör.  
   - **Syntax:** Visar exakt syntax, inklusive obligatoriska och valfria argument.  
   - **Optioner:** Lista över eventuella optioner specifika för kommandot, tillsammans med förklaringar.  
   - **Exempel:** Ger exempel på hur kommandot kan köras effektivt.

### check-config

Kommandot check-config är ett verktyg i ***digna*** CLI som används för att testa konfigurationen av ***digna***. Detta kommando säkerställer att ***digna***-komponenterna kan hitta nödvändiga konfigurationsdelar i config.toml.

#### Optioner

- `--configpath`, `-cp`: Fil eller katalog som innehåller konfigurationen. Om detta utelämnas används ../config.toml.
      
#### Kommandoanvändning
```bash
dignacli check-config
```

Vid lyckad körning skriver kommandot ut en bekräftelse på att konfigurationen är komplett.  
  
Om konfigurationen verkar ofullständig kommer de saknade konfigurationsdelarna att listas.

  
### check-repo-connection

Kommandot check-repo-connection är ett verktyg i ***digna*** CLI som används för att testa anslutning och åtkomst till ett angivet ***digna***-repository. Detta kommando säkerställer att CLI:n kan interagera med repositoryt.
      
#### Kommandoanvändning
```bash
dignacli check-repo-connection
```

Vid lyckad körning returnerar kommandot en bekräftelse på anslutningen, tillsammans med detaljer om repositoryt: Repository-version, Host, Database och Schema.  
  
Om repository-anslutningen inte lyckas, kontrollera config.toml för korrekta inställningar.


### version

För att kontrollera installerad version av *dignacli* använd optionen --version.  
  
#### Kommandoanvändning
```bash
dignacli --version
```
  
#### Exempelutdata
```bash
dignacli version 2025.09
```

### loggningsoptioner
  
Som standard är konsolutdata från ***digna***-kommandon avsedd att vara minimalistisk. De flesta kommandon erbjuder möjligheten att ge ytterligare information med följande optioner:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
”verbose” och ”debug” definierar detaljnivån, medan ”logfile”-svalet tillåter att omdirigera utdata till en fil istället för till konsolfönstret.

## Användarhantering

### add-user
  
Kommandot add-user i ***digna*** CLI används för att lägga till en ny användare i ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argument

- **USER_NAME**: Användarnamn för den nya användaren (obligatoriskt).
- **USER_FULL_NAME**: Fullständigt namn för den nya användaren (obligatoriskt).
- **USER_PASSWORD**: Lösenord för den nya användaren (obligatoriskt).

#### Optioner

- `--is_superuser`, `-su`: Flagga för att ange att den nya användaren är administratör.
- `--valid_until`, `-vu`: Sätter ett utgångsdatum för användarkontot i formatet `YYYY-MM-DD HH:MI:SS`. Om detta ej anges har kontot inget utgångsdatum.

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
- **USER_NAME**: Användarnamnet för den användare som ska tas bort (obligatoriskt). Detta är det enda argumentet som krävs för kommandot.

#### Exempel
```bash
dignacli delete-user jdoe
```
  
Att köra detta kommando tar bort användaren `jdoe` från ***digna***-systemet, återkallar deras åtkomst och tar bort associerade data och behörigheter från repositoryt.

### modify-user

Kommandot `modify-user` i ***digna*** CLI används för att uppdatera detaljerna för en befintlig användare i ***digna***-systemet.

#### Kommandoanvändning
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argument
  
- **USER_NAME**: Användarnamnet för den användare som ska ändras (obligatoriskt).
- **USER_FULL_NAME**: Det nya fullständiga namnet för användaren (obligatoriskt).
  
#### Optioner  
  
- `--is_superuser`, `-su`: Sätter användaren som superuser och ger förhöjda rättigheter. Denna flagga kräver inget värde.  
- `--valid_until`, `-vu`: Sätter ett utgångsdatum för användarkontot i formatet YYYY-MM-DD HH:MI:SS. Om detta inte anges förblir kontot giltigt på obestämd tid.  
  
#### Exempel
  
För att ändra fullständigt namn för användaren `jdoe` till “Johnathan Doe” och göra användaren till superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Kommandot `modify-user-pwd` i ***digna*** CLI används för att byta lösenord för en befintlig användare i ***digna***-systemet.
  
#### Kommandoanvändning
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argument
  
- **USER_NAME**: Användarnamnet för den användare vars lösenord ska ändras (obligatoriskt).
- **USER_PWD**: Det nya lösenordet för användaren (obligatoriskt).
  
#### Exempel
  
För att byta lösenord för användaren `jdoe` till `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Kommandot `list-users` i ***digna*** CLI visar en lista över alla användare registrerade i ***digna***-systemet.

#### Kommandoanvändning

```bash
dignacli list-users
```

När detta kommando körs ansluter det till ***digna***-repositoryt och listar alla användare, visar deras ID, användarnamn, fullständiga namn, superuser-status och utgångstidsstämplar.

## Repository-hantering

### upgrade-repo
  
Kommandot `upgrade-repo` i ***digna*** CLI används för att uppgradera eller initiera ***digna***-repositoryt. Detta kommando är nödvändigt för att applicera uppdateringar eller för att sätta upp repository-infrastrukturen första gången.
  
#### Kommandoanvändning

```bash
dignacli upgrade-repo [options]
```
  
#### Optioner
  
- `--simulation-mode`, `-s`: När denna är aktiverad körs kommandot i simuleringsläge, vilket skriver ut SQL-satserna som skulle köras men utför dem inte. Detta är användbart för att förhandsgranska ändringar utan att göra modifieringar i repositoryt.  

  
#### Exempel
  
För att uppgradera ***digna***-repositoryt kan du köra kommandot utan optioner:
  
```bash
dignacli upgrade-repo
```  
För att köra uppgraderingen i simuleringsläge (för att se SQL-satserna utan att tillämpa dem):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Detta kommando är avgörande för att underhålla ***digna***-systemet och säkerställa att databasschemat och andra repository-komponenter är uppdaterade till den senaste versionen av mjukvaran.

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
Detta kommando returnerar den krypterade versionen av det angivna lösenordet, vilket sedan kan användas i säkra sammanhang. Om lösenordsargumentet inte tillhandahålls visar CLI:n ett fel som indikerar det saknade argumentet.

### generate-key
  
Kommandot `generate-key` används för att generera en Fernet-nyckel, vilket är viktigt för att säkra lösenord som lagras i ***digna***-repositoryt.
  
#### Kommandoanvändning
```bash
dignacli generate-key
```
  
## Datahantering

### clean-up

Kommandot `clean-up` i ***digna*** CLI används för att ta bort profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando är viktigt för hantering av datalivscykeln och hjälper till att hålla en organiserad och effektiv datamiljö genom att rensa bort inaktuella eller onödiga data.

#### Kommandoanvändning

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet som data ska tas bort från (obligatoriskt). Att använda nyckelordet all-projects i detta argument instruerar ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för raderingen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för raderingen, enligt samma format som FROM_DATE (obligatoriskt).
  
#### Optioner
  
- `--table-name`, `-tn`: Begränsar clean-up-operationen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar så att clean-up endast gäller tabeller som innehåller den angivna substrängen i sina namn.
- `--timing`, `-tm`: Visar tidsåtgången för clean-up-processen efter avslutad körning.
- `--help`: Visar hjälpinformation för clean-up-kommandot och avslutar.
  
#### Exempel
  
För att ta bort data från projektet ProjectA mellan 1 januari 2023 och 30 juni 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
För att rensa data endast från en specifik tabell kallad `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Detta kommando hjälper till att hantera datalagring och säkerställa att repositoryt endast innehåller relevant information.

### remove-orphans
  
Kommandot `remove-orphans` i ***digna*** CLI används för städning i ***digna***-repositoryt.  
När en användare tar bort projekt eller datakällor kvarstår profiler och prediktioner i repositoryt. Med detta kommando tas sådana föräldralösa (orphaned) rader bort från repositoryt.
  
#### Kommandoanvändning
  
```bash
dignacli list-projects
```

### list-projects
  
Kommandot `list-projects` i ***digna*** CLI används för att visa en lista över alla tillgängliga projekt i ***digna***-systemet.
  
#### Kommandoanvändning
  
```bash
dignacli list-projects
```

Detta kommando är särskilt användbart för administratörer och användare som hanterar flera projekt, och ger en snabb översikt över de projekt som finns i ***digna***-repositoryt.

### list-ds

Kommandot `list-ds` i ***digna*** CLI används för att visa en lista över alla tillgängliga datakällor inom ett angivet projekt. Detta kommando är användbart för att få en överblick över de dataresurser som finns tillgängliga för analys och hantering i ***digna***-systemet.

#### Kommandoanvändning
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet för vilket datakällorna listas (obligatoriskt).
  
#### Exempel
  
För att lista alla datakällor i projektet som heter `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Detta kommando ger användare en översikt över datakällorna i ett projekt och hjälper dem att navigera och hantera datalandskapet mer effektivt.


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
  
- **PROJECT_NAME**: Namnet på projektet som ska inspekteras (obligatoriskt). Att använda nyckelordet all-projects i detta argument instruerar ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för inspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för inspektionen, enligt samma format som FROM_DATE (obligatoriskt).
  
#### Optioner

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar så att endast tabeller som innehåller den angivna substrängen i sina namn inspekteras.
- `--enable_notification`, `-en`: Aktiverar utskick av notifikationer vid larm.
- `--bypass-backend`, `-bb`: Bypassar backend och kör inspektionen direkt från CLI (endast för teständamål!).

  
#### Exempel
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
För att inspektera endast en specifik tabell och tvinga omberäkning av prediktioner:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Detta kommando är användbart för att generera uppdaterade profiler och prediktioner, övervaka dataintegritet och hantera larmssystem inom en angiven projekttidsram.

### inspect-async

Kommandot `inspect-async` i ***digna*** CLI används för att skapa profiler, prediktioner och trafikljussystemdata för en eller flera datakällor inom ett angivet projekt. Detta kommando hjälper till att analysera och övervaka data över en definierad period. I motsats till kommandot `inspect` väntar detta inte på att inspektionen ska slutföras.
Istället returnerar det request-id för den inskickade inspektionsförfrågan. För att fråga om status för inspektionsprocessen, använd kommandot `inspect-status`.

#### Kommandoanvändning

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argument
  
- **PROJECT_NAME**: Namnet på projektet som ska inspekteras (obligatoriskt). Att använda nyckelordet all-projects i detta argument instruerar ***digna*** att iterera över alla befintliga projekt och tillämpa kommandot.
- **FROM_DATE**: Startdatum och tid för inspektionen. Acceptabla format inkluderar %Y-%m-%d, %Y-%m-%dT%H:%M:%S eller %Y-%m-%d %H:%M:%S (obligatoriskt).
- **TO_DATE**: Slutdatum och tid för inspektionen, enligt samma format som FROM_DATE (obligatoriskt).
  
#### Optioner

- `--table-name`, `-tn`: Begränsar inspektionen till en specifik tabell inom projektet.
- `--table-filter`, `-tf`: Filtrerar så att endast tabeller som innehåller den angivna substrängen i sina namn inspekteras.
- `--enable_notification`, `-en`: Aktiverar utskick av notifikationer vid larm.

  
#### Exempel
  
För att inspektera data för projektet `ProjectA` från 1 januari 2024 till 31 januari 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Kommandot `inspect-status` i ***digna*** CLI används för att kontrollera status för en asynkron inspektion baserat på request-id.

#### Kommandoanvändning

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argument
  
- **REQUEST_ID**: Request-id som returnerades av kommandot `inspect-async` 
  
#### Exempel
  
För att kontrollera status för en inspektion med request-id 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Kommandot `inspect-cancel` i ***digna*** CLI används för att avbryta inspektioner baserat på request-id eller för att avbryta alla pågående förfrågningar.

#### Kommandoanvändning

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argument
  
- **REQUEST_ID**: Request-id som returnerades av kommandot `inspect-async` 
  
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

Kommandot `export-ds` i ***digna*** CLI används för att skapa en export av datakällor från ***digna***-repositoryt. Som standard exporteras alla datakällor från ett givet projekt.

#### Kommandoanvändning
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet som datakällorna kommer att exporteras från.

#### Optioner

- `--table_name`, `-tn`: Exportera en särskild datakälla från ett projekt.
- `--exportfile`, `-ef`: Ange filnamn för exporten.
    
#### Exempel
  
För att exportera alla datakällor från projektet `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Detta kommando exporterar alla datakällor från `ProjectA` som ett JSON-dokument som kan importeras till ett annat projekt eller ***digna***-repository.

### import-ds

Kommandot `import-ds` i ***digna*** CLI används för att importera datakällor till ett målprojekt och skapa en importrapport.

#### Kommandoanvändning
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet dit datakällorna kommer att importeras.
- **EXPORT_FILE**: Filnamnet för exportfilen som ska importeras.

#### Optioner

- `--output-file`, `-o`: Fil för att spara importrapporten (om ej specificerat skrivs den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format för att spara importrapporten (json, csv).
    
#### Exempel
  
För att importera alla datakällor från exportfilen `my_export.json` till `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Efter importen visar detta kommando även en rapport över importerade och hoppade objekt. Endast nya datakällor kommer att importeras till `ProjectB`. För att ta reda på vilka objekt som skulle importeras och vilka som skulle hoppas över kan du använda kommandot `plan-import-ds`.

### plan-import-ds

Kommandot `plan-import-ds` i ***digna*** CLI används för att analysera en exportfil innan import och skapa en importplan/rapport.

#### Kommandoanvändning
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argument
- **PROJECT_NAME**: Namnet på projektet dit datakällorna skulle importeras.
- **EXPORT_FILE**: Filnamnet för exportfilen som ska analyseras innan import.

#### Optioner

- `--output-file`, `-o`: Fil för att spara importrapporten (om ej specificerat skrivs den ut i terminalen i tabellform).
- `--output-format`, `-f`: Format för att spara importrapporten (json, csv).
    
#### Exempel
  
För att kontrollera vilka datakällor som skulle importeras och vilka som skulle hoppas över från exportfilen `my_export.json` när den importeras till `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Detta kommando visar endast en importplan av objekt som skulle importeras och hoppas över.