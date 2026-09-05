# digna CLI Reference 2024.11
**2024-11-03**

Šī lapa dokumentē pilnu komandu komplektu, kas pieejams ***digna*** CLI izlaidumā **2024.11**, iekļaujot izmantošanas piemērus un opcijas.


---
## CLI Basics

---

## Using `help` Option

Opcija `--help` sniedz informāciju par pieejamajām komandām un to lietošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārīgas palīdzības parādīšana:**
   
    Izmantojiet --help tūlīt pēc atslēgas vārda dignacli  
   ```bash
   dignacli --help
   ```

2. **Palīdzība konkrētām komandām:**  
  
    Lai iegūtu detalizētu informāciju par konkrētu komandu, pievienojiet `--help` tai komandai.
    Piemēram, lai saņemtu palīdzību par komandu `add-user`, izpildiet:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Komandas apraksts:** Sniedz detalizētu aprakstu par to, ko komanda veic.  
     - **Sintakse:** Parāda precīzu sintaksi, ieskaitot obligātos un izvēles argumentus.  
     - **Opcijas:** Uzskaita komandas specifiskās opcijas ar to skaidrojumiem.  
     - **Piemēri:** Sniedz piemērus, kā efektīvi izsaukt komandu.

  
## Using `check-repo-connection` Command

Komanda check-repo-connection ir rīks ***digna*** CLI ietvaros, kas paredzēts, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repozitorijam. Šī komanda nodrošina, ka CLI var mijiedarboties ar repozitoriju.
      
### Command Usage
```bash
dignacli check-repo-connection
```

Veiksmīgas izpildes gadījumā komanda izvada savienojuma apstiprinājumu kopā ar informāciju par repozitoriju: Repository version, Host, Database and Schema.  
  
Ja repozitorija savienojums nav veiksmīgs, pārbaudiet config.toml failu, lai pārliecinātos par pareiziem konfigurācijas iestatījumiem.

## Using ‘version’ command

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju --version.  
  
### Command Usage
```bash
dignacli --version
```
  
### Example Output
```bash
dignacli version 2024.11
```

## Using logging options
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir paredzēta īsa un kodolīga. Lielākā daļa komandu piedāvā iespēju uzrādīt papildu informāciju, izmantojot šādas opcijas:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” un “debug” nosaka detaļumu līmeni, savukārt “logfile” slēdzis ļauj pāradresēt izvadi uz failu, nevis konsoles logu.

# User Management

## Using ‘add-user’ command
  
Komanda add-user ***digna*** CLI tiek izmantota, lai pievienotu jaunu lietotāju ***digna*** sistēmai.
  
### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Arguments

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāts).
- **USER_FULL_NAME**: Jaunā lietotāja pilnais vārds (obligāts).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāta).

### Options

- `--is_superuser`, `-su`: Pārslēdzis, kas piešķir jaunajam lietotājam administratora tiesības.
- `--valid_until`, `-vu`: Iestata lietotāja konta derīguma termiņu formātā `YYYY-MM-DD HH:MI:SS`. Ja nav iestatīts, kontam nav derīguma termiņa.

### Example

Lai pievienotu jaunu lietotāju ar lietotājvārdu `jdoe`, pilno vārdu `John Doe` un paroli `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lai pievienotu jaunu lietotāju un iestatītu konta derīguma termiņu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Using `delete-user` command
  
Komanda `delete-user` ***digna*** CLI tiek izmantota, lai noņemtu esošu lietotāju no ***digna*** sistēmas.
  
### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
### Arguments
- **USER_NAME**: Dzēšamā lietotāja lietotājvārds (obligāts). Tā ir vienīgā komandas prasītā argumenta vērtība.

### Example
```bash
dignacli delete-user jdoe
```
  
Izpildot šo komandu, lietotājs `jdoe` tiks noņemts no ***digna*** sistēmas, zaudējot piekļuvi un dzēšot ar viņu saistītos datus un atļaujas repozitorijā.

## Using `modify-user` Command

Komanda `modify-user` ***digna*** CLI tiek izmantota, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Arguments
  
- **USER_NAME**: Lietotājvārds lietotājam, kuru jārediģē (obligāts).
- **USER_FULL_NAME**: Jaunais pilnais lietotāja vārds (obligāts).
  
### Options  
  
- `--is_superuser`, `-su`: Iestata lietotāju par superuser, piešķirot paaugstinātas tiesības. Šim slēdzim nav nepieciešama vērtība.  
- `--valid_until`, `-vu`: Iestata lietotāja konta derīguma termiņu formātā YYYY-MM-DD HH:MI:SS. Ja nav norādīts, konts paliek derīgs bez termiņa.  
  
### Example
  
Lai mainītu lietotāja `jdoe` pilno vārdu uz “Johnathan Doe” un iestatītu lietotāju kā superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Using `modify-user-pwd` Command
  
Komanda `modify-user-pwd` ***digna*** CLI tiek izmantota, lai mainītu esoša lietotāja paroli ***digna*** sistēmā.
  
### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Arguments
  
- **USER_NAME**: Lietotājvārds lietotājam, kura parolei jāveic maiņa (obligāts).
- **USER_PWD**: Jaunā paroles vērtība (obligāts).
  
### Example
  
Lai nomainītu lietotāja `jdoe` paroli uz `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Using `list-users` Command

Komanda `list-users` ***digna*** CLI attēlo visu lietotāju sarakstu, reģistrētu ***digna*** sistēmā.

### Command Usage

```bash
dignacli list-users
```

Izpildot šo komandu ***digna*** CLI savienosies ar ***digna*** repozitoriju un uzrādīs visus lietotājus, rādīdams viņu ID, lietotājvārdus, pilnos vārdus, superuser statusu un derīguma laika zīmogus.

# Repository Management

### Using `upgrade-repo` Command
  
Komanda `upgrade-repo` ***digna*** CLI tiek izmantota, lai atjauninātu vai inicializētu ***digna*** repozitoriju. Šī komanda ir būtiska, lai pielietotu atjauninājumus vai uzstādītu repozitorija infrastruktūru pirmo reizi.
  
### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s`: Kad iespējota, šī opcija izpilda komandu simulācijas režīmā, izdrukājot SQL vaicājumus, kas tiktu izpildīti, bet tos faktiski neizpilda. Tas ir noderīgi, lai apskatītu izmaiņas bez to pielietošanas repozitorijā.  

  
### Example
  
Lai atjauninātu ***digna*** repozitoriju, var izpildīt komandu bez papildu opcijām:
  
```bash
dignacli upgrade-repo
```  
Lai palaistu atjauninājumu simulācijas režīmā (lai redzētu SQL vaicājumus bez to pielietošanas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Šī komanda ir svarīga ***digna*** sistēmas uzturēšanai, nodrošinot, ka datubāzes shēma un citi repozitorija komponenti ir aktuāli ar jaunāko programmatūras versiju.

## Using `encrypt` Command
  
Komanda `encrypt` ***digna*** CLI tiek izmantota, lai šifrētu paroli.
  
### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Arguments
- **PASSWORD**: Parole, kuru nepieciešams šifrēt (obligāts).
  
### Example
  
Lai šifrētu paroli, parole jānorāda kā arguments.   
Piemēram, lai šifrētu paroli `mypassword123`, izmantojiet:
```bash
dignacli encrypt mypassword123
```
Šī komanda izvada norādītās paroles šifrēto versiju, ko pēc tam var izmantot drošās vietās. Ja paroles arguments nav norādīts, CLI parādīs kļūdu par trūkstošo argumentu.

## Using `generate-key` Command
  
Komanda `generate-key` tiek izmantota, lai ģenerētu Fernet atslēgu, kas ir būtiska paroles aizsardzībai ***digna*** repozitorijā.
  
### Command Usage
```bash
dignacli generate-key
```
  
# Data Management

## Using `clean-up` Command

Komanda `clean-up` ***digna*** CLI tiek izmantota, lai noņemtu profilus, prognozes un Traffic Light System datus vienam vai vairākiem datu avotiem noteiktā projektā. Šī komanda ir būtiska datu dzīves cikla pārvaldībā, palīdzot uzturēt kārtīgu un efektīvu datu vidi, iztīrot novecojušos vai nevajadzīgos datus.

### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: Projekta nosaukums, no kura jānoņem dati (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** tiks norīkots iterēt pār visiem esošajiem projektiem un pielietot šo komandu.
- **FROM_DATE**: Datumu un laiku sākumposms datu dzēšanai. Pieņemami formāti: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Datumu un laiku beigu posms datu dzēšanai, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
### Options
  
- `--table-name`, `-tn`: Ierobežo clean-up operāciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtri, kas ierobežo clean-up tikai tām tabulām, kuru nosaukumos ir norādītā apakšvirkne.
- `--timing`, `-tm`: Pēc pabeigšanas parāda clean-up procesa ilgumu.
- `--help`: Parāda palīdzību par clean-up komandu un iziet.
  
### Example
  
Lai noņemtu datus no projekta ProjectA periodā no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Lai noņemtu datus tikai no konkrētas tabulas ar nosaukumu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Šī komanda palīdz pārvaldīt datu glabāšanu un nodrošina, ka repozitorijā saglabājas tikai atbilstoša informācija.

## Using `inspect` Command

Komanda `inspect` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un Traffic Light System datus vienam vai vairākiem datu avotiem noteiktā projektā. Šī komanda palīdz analizēt un uzraudzīt datus noteiktā laika posmā.

### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME**: Projekta nosaukums, kuram jāveic datu pārbaude (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** tiks norīkots iterēt pār visiem esošajiem projektiem un pielietot šo komandu.
- **FROM_DATE**: Sākuma datums un laiks datu pārbaudei. Pieņemami formāti: %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Beigu datums un laiks datu pārbaudei, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
### Options

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrē, lai pārbaudītu tikai tās tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--do-profile`: Aktivizē profilu pārvākšanu/reģenerēšanu. Noklusējums ir do-profile.
- `--no-do-profile`: Neļauj pārvākt/reģenerēt profilus.
- `--do-prediction`: Aktivizē prognožu pārrēķināšanu. Noklusējums ir do-prediction.
- `--no-do-prediction`: Neļauj pārrēķināt prognozes.
- `--do-alert-status`: Aktivizē brīdinājumu statusu pārrēķināšanu. Noklusējums ir do-alert-status.
- `--no-do-alert-status`: Neļauj pārrēķināt brīdinājumu statusus.
- `--timing`, `-tm`: Pēc pabeigšanas parāda inspekcijas procesa ilgumu.
  
### Example
  
Lai inspectētu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Lai inspektētu tikai konkrētu tabulu un piespiestu prognožu pārrēķinu:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Šī komanda ir noderīga, lai ģenerētu atjauninātus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu brīdinājumu sistēmas noteiktā projekta laika periodā.

## Using `tls-status` Command

Komanda `tls-status` ***digna*** CLI tiek izmantota, lai vaicātu Traffic Light System (TLS) statusu konkrētai tabulai projektā dotajā datumā. Traffic Light System sniedz ieskatu par datu veselību un kvalitāti, norādot uz potenciālajām problēmām vai brīdinājumiem, kam jāpievērš uzmanība.
  
### Command Usage
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Arguments
  
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek vaicāts TLS statuss (obligāts).
- **TABLE_NAME**: Konkrētā tabula projektā, kurai nepieciešams TLS statuss (obligāts).
- **DATE**: Datums, par kuru tiek vaicāts TLS statuss, parasti formātā %Y-%m-%d (obligāts).
  
### Example
  
Lai pārbaudītu TLS statusu tabulai UserData projektā ProjectA 2024. gada 1. jūlijā:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Šī komanda palīdz lietotājiem uzraudzīt un uzturēt datu kvalitāti, sniedzot skaidru un lietojamu statusa ziņojumu, pamatojoties uz iepriekš definētiem kritērijiem.

## Using `list-projects` Command
  
Komanda `list-projects` ***digna*** CLI tiek izmantota, lai attēlotu visu pieejamo projektu sarakstu ***digna*** sistēmā.
  
### Command Usage
  
```bash
dignacli list-projects
```

Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kuri pārvalda vairākus projektus, sniedzot ātru pārskatu par pieejamajiem projektiem ***digna*** repozitorijā.

## Using `list-ds` Command

Komanda `list-ds` ***digna*** CLI tiek izmantota, lai attēlotu visu pieejamo datu avotu sarakstu noteiktā projektā. Šī komanda ir noderīga, lai saprastu datu resursus, kas pieejami analīzei un pārvaldībai ***digna*** sistēmā.

### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Arguments
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek uzskaitīti datu avoti (obligāts).
  
### Example
  
Lai uzskaitītu visus datu avotus projektā ar nosaukumu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Šī komanda sniedz lietotājiem pārskatu par projektā pieejamiem datu avotiem, palīdzot efektīvāk pārvietoties un pārvaldīt datu ainavu.