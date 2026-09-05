---
title: digna CLI atsauce 2025.04 – komandas un piemēri | digna dokumentācija
description: Pilna digna CLI versijas 2025.04 atsauce. Uzziniet, kā pārvaldīt lietotājus, repozitorijus un datus, izmantojot komandas, piemēram, add-user, check-repo-connection, upgrade-repo, inspect un citas.
image: /assets/logo_square.png
---

# digna CLI atsauce 2025.04
**2025-04-01**

Šajā lapā dokumentēts pilns komandu komplekts, kas pieejams ***digna*** CLI izlaidā **2025.04**, ieskaitot lietošanas piemērus un opcijas.

---

## CLI pamatprincipi

---

## `help` opcijas izmantošana

Opcija `--help` sniedz informāciju par pieejamajām komandām un to lietošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārīgās palīdzības attēlošana:**
   
    Lietojiet --help uzreiz pēc atslēgvārda ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Palīdzības saņemšana par konkrētām komandām:**  
  
    Lai iegūtu detalizētu informāciju par konkrētu komandu, pievienojiet tai `--help`.
    Piemēram, lai iegūtu palīdzību par komandu `add-user`, izpildiet:
     ```bash
     dignacli add-user --help
     ```

     ### izvade:
      
     - **Komandas apraksts:** Sniedz detalizētu informāciju par to, ko komanda dara.  
     - **Sintakse:** Parāda precīzu sintaksi, ieskaitot obligātās un izvēles argumentu pozīcijas.  
     - **Opcijas:** Uzskaita visas komandas specifiskās opcijas ar to paskaidrojumiem.  
     - **Piemēri:** Piedāvā piemērus, kā efektīvi izpildīt komandu.

  
## `check-repo-connection` komandas izmantošana

Komanda check-repo-connection ir utilīta ***digna*** CLI rīkā, kas paredzēta, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repozitorijam. Šī komanda nodrošina, ka CLI var mijiedarboties ar repozitoriju.
      
#### Komandas lietošana
```bash
dignacli check-repo-connection
```

Veiksmīgas izpildes gadījumā komanda izvada savienojuma apstiprinājumu, kā arī informāciju par repozitoriju: Repository version, Host, Database and Schema.  
  
Ja repozitorija savienojums nav veiksmīgs, pārbaudiet config.toml failu, lai nodrošinātu pareizu konfigurāciju.

## ‘version’ komandas izmantošana

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju --version.  
  
#### Komandas lietošana
```bash
dignacli --version
```
  
#### Piemēra izvade
```bash
dignacli version 2025.04
```

## Lietošana ar žurnālfailu opcijām
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir paredzēta minimālistiska. Lielākā daļa komandu piedāvā iespēju nodrošināt papildu informāciju, izmantojot šādas opcijas:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” un “debug” nosaka informācijas detalizācijas līmeni, savukārt “logfile” slēdzis ļauj pāradresēt izvadi uz failu, nevis konsoles logu.

## Lietotāju pārvaldība

### ‘add-user’ komandas izmantošana
  
Komanda add-user ***digna*** CLI lieto, lai pievienotu jaunu lietotāju ***digna*** sistēmai.
  
#### Komandas lietošana
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenti

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāti).
- **USER_FULL_NAME**: Jaunā lietotāja pilnais vārds (obligāti).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāti).

#### Opcijas

- `--is_superuser`, `-su`: Flagma, lai piešķirtu jaunajam lietotājam administratora tiesības.
- `--valid_until`, `-vu`: Uzstāda lietotāja konta derīguma termiņu formātā `YYYY-MM-DD HH:MI:SS`. Ja netiek norādīts, kontam nav derīguma termiņa.

#### Piemērs

Lai pievienotu jaunu lietotāju ar lietotājvārdu `jdoe`, pilnu vārdu `John Doe` un paroli `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lai pievienotu jaunu lietotāju un noteiktu konta derīguma datumu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### `delete-user` komandas izmantošana
  
Komanda `delete-user` ***digna*** CLI lieto, lai noņemtu esošu lietotāju no ***digna*** sistēmas.
  
#### Komandas lietošana
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenti
- **USER_NAME**: Dzēšamā lietotāja lietotājvārds (obligāti). Tas ir vienīgais komandai nepieciešamais arguments.

#### Piemērs
```bash
dignacli delete-user jdoe
```
  
Izpildot šo komandu, lietotājs `jdoe` tiks noņemts no ***digna*** sistēmas, zaudējot piekļuvi, un tiks dzēsti ar viņu saistītie dati un atļaujas repozitorijā.

### `modify-user` komandas izmantošana

Komanda `modify-user` ***digna*** CLI lieto, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

#### Komandas lietošana
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenti
  
- **USER_NAME**: Modificējamā lietotāja lietotājvārds (obligāti).
- **USER_FULL_NAME**: Jaunais lietotāja pilnais vārds (obligāti).
  
#### Opcijas  
  
- `--is_superuser`, `-su`: Uzstāda lietotāju kā superlietotāju, piešķirot paaugstinātas privilēģijas. Šim flagem nav nepieciešama vērtība.  
- `--valid_until`, `-vu`: Uzstāda lietotāja konta derīguma datumu formātā YYYY-MM-DD HH:MI:SS. Ja netiek norādīts, konts paliek derīgs beztermiņa.  
  
#### Piemērs
  
Lai mainītu lietotāja `jdoe` pilno vārdu uz “Johnathan Doe” un piešķirtu lietotājam superlietotāja tiesības:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### `modify-user-pwd` komandas izmantošana
  
Komanda `modify-user-pwd` ***digna*** CLI lieto, lai mainītu esoša lietotāja paroli ***digna*** sistēmā.
  
#### Komandas lietošana
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenti
  
- **USER_NAME**: Lietotājvārds, kura parole jāmaina (obligāti).
- **USER_PWD**: Jaunā parole lietotājam (obligāti).
  
#### Piemērs
  
Lai nomainītu lietotāja `jdoe` paroli uz `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### `list-users` komandas izmantošana

Komanda `list-users` ***digna*** CLI attēlo visu reģistrēto lietotāju sarakstu ***digna*** sistēmā.

#### Komandas lietošana

```bash
dignacli list-users
```

Izpildot šo komandu ***digna*** CLI izveidos savienojumu ar ***digna*** repozitoriju un izrādīs visus lietotājus, rādīsim to ID, lietotājvārdu, pilno vārdu, superlietotāja statusu un derīguma laika zīmogus.

## Repozitorija pārvaldība

### `upgrade-repo` komandas izmantošana
  
Komanda `upgrade-repo` ***digna*** CLI lieto, lai atjauninātu vai inicializētu ***digna*** repozitoriju. Šī komanda ir būtiska atjauninājumu piemērošanai vai repozitorija infrastruktūras iestatīšanai pirmo reizi.
  
#### Komandas lietošana

```bash
dignacli upgrade-repo [options]
```
  
#### Opcijas
  
- `--simulation-mode`, `-s`: Ja ieslēgta, šī opcija veic komandas izpildi simulācijas režīmā, izdrukājot SQL vaicājumus, kas tiktu izpildīti, bet faktiski tos neveicot. Tas noder, lai priekšskatītu izmaiņas, neveicot izmaiņas repozitorijā.  

  
#### Piemērs
  
Lai atjauninātu ***digna*** repozitoriju, varat izpildīt komandu bez papildu opcijām:
  
```bash
dignacli upgrade-repo
```  
Lai palaistu atjaunināšanu simulācijas režīmā (lai redzētu SQL vaicājumus bez to pielietošanas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Šī komanda ir izšķiroša, lai uzturētu ***digna*** sistēmu — nodrošinot, ka datubāzes shēma un citi repozitorija komponenti atbilst programmatūras jaunākajai versijai.

### `encrypt` komandas izmantošana
  
Komanda `encrypt` ***digna*** CLI lieto, lai šifrētu paroli.
  
#### Komandas lietošana
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Parole, kas jāšifrē (obligāti).
  
#### Piemērs
  
Lai šifrētu paroli, tai jābūt norādītai kā argumentam.   
Piemēram, lai šifrētu paroli `mypassword123`, izmantojiet:
```bash
dignacli encrypt mypassword123
```
Šī komanda izvadīs norādītās paroles šifrēto versiju, kuru pēc tam var izmantot drošos kontekstos. Ja parole netiek norādīta kā arguments, CLI parādīs kļūdu, norādot uz trūkstošo argumentu.

## `generate-key` komandas izmantošana
  
Komanda `generate-key` tiek izmantota, lai ģenerētu Fernet atslēgu, kas ir būtiska, lai nodrošinātu parolēm glabāšanas drošību ***digna*** repozitorijā.
  
#### Komandas lietošana
```bash
dignacli generate-key
```
  
## Datu pārvaldība

## `clean-up` komandas izmantošana

Komanda `clean-up` ***digna*** CLI lieto, lai noņemtu profilus, prognozes un Traffic Light System datus vienam vai vairākiem datu avotiem specifiskā projektā laika intervālā. Šī komanda ir būtiska datu dzīves cikla pārvaldībai, palīdzot uzturēt organizētu un efektīvu datu vidi, iztīrot novecojušos vai nevajadzīgos datus.

#### Komandas lietošana

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, no kura dati tiek noņemti (obligāti). Ja kā argumentu izmanto atslēgvārdu all-projects, ***digna*** izpildīs šo komandu visos esošajos projektos.
- **FROM_DATE**: Datumu un laiku, no kura sākt datu dzēšanu. Pieņemamie formāti: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vai %Y-%m-%d %H:%M:%S (obligāti).
- **TO_DATE**: Datumu un laiku, līdz kuram veikt datu dzēšanu, izmantojot tos pašus formātus kā FROM_DATE (obligāti).
  
#### Opcijas
  
- `--table-name`, `-tn`: Ierobežo clean-up operāciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtē, lai ierobežotu tīrīšanu tikai tabulām, kuru nosaukumos ir norādītā apakšvirkne.
- `--timing`, `-tm`: Parāda clean-up procesa laika ilgumu pēc tā pabeigšanas.
- `--help`: Parāda help informāciju par clean-up komandu un iziet.
  
#### Piemērs
  
Lai noņemtu datus no projekta ProjectA no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Lai noņemtu datus tikai no konkrētas tabulas ar nosaukumu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Šī komanda palīdz pārvaldīt datu uzglabāšanu un nodrošina, ka repozitorijā paliek tikai aktuāla informācija.

## `list-projects` komandas izmantošana
  
Komanda `list-projects` ***digna*** CLI lieto, lai attēlotu visu pieejamo projektu sarakstu ***digna*** sistēmā.
  
#### Komandas lietošana
  
```bash
dignacli list-projects
```

Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kas pārvalda vairākus projektus, nodrošinot ātru pārskatu par pieejamajiem projektiem ***digna*** repozitorijā.

## `list-ds` komandas izmantošana

Komanda `list-ds` ***digna*** CLI lieto, lai attēlotu visu pieejamo datu avotu sarakstu norādītā projektā. Šī komanda noder, lai saprastu pieejamos datu resursus analīzei un pārvaldībai ***digna*** sistēmā.

#### Komandas lietošana
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, kura datu avoti tiek uzskaitīti (obligāti).
  
#### Piemērs
  
Lai uzskaitītu visus datu avotus projektā ar nosaukumu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Šī komanda sniedz lietotājiem pārskatu par projektā pieejamajiem datu avotiem, palīdzot labāk orientēties un pārvaldīt datu resursus.

## `inspect` komandas izmantošana

Komanda `inspect` ***digna*** CLI lieto, lai izveidotu profilus, prognozes un Traffic Light System datus vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda palīdz analizēt un monitorēt datus noteiktā laika posmā.

#### Komandas lietošana

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kuram dati tiek pārbaudīti (obligāti). Ja kā argumentu izmanto atslēgvārdu all-projects, ***digna*** izpildīs šo komandu visos esošajos projektos.
- **FROM_DATE**: Sākuma datums un laiks datu pārbaudei. Pieņemamie formāti: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vai %Y-%m-%d %H:%M:%S (obligāti).
- **TO_DATE**: Beigu datums un laiks datu pārbaudei, izmantojot tos pašus formātus kā FROM_DATE (obligāti).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspect darbību uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtē, lai pārbaudītu tikai tās tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--do-profile`: Izsauc profilu pārsavākšanu. Noklusējums ir do-profile.
- `--no-do-profile`: Neļauj pārsavākt profilus.
- `--do-prediction`: Izsauc prognožu pārrēķināšanu. Noklusējums ir do-prediction.
- `--no-do-prediction`: Novērš prognožu pārrēķināšanu.
- `--do-alert-status`: Izsauc brīdinājumu statusu pārrēķināšanu. Noklusējums ir do-alert-status.
- `--no-do-alert-status`: Novērš brīdinājumu statusu pārrēķināšanu.
- `--iterative`: Veic perioda pārbaudi, izmantojot dienu iterācijas. Noklusējums ir iterative.
- `--no-iterative`: Veic pārbaudi visam periodam vienlaikus.
- `--enable_notification`, `-en`: Iespējo paziņojumu sūtīšanu brīdinājumu gadījumā.
- `--timing`, `-tm`: Parāda inspect procesa ilgumu pēc tā pabeigšanas.
  
#### Piemērs
  
Lai pārbaudītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Lai pārbaudītu tikai konkrētu tabulu un piespiestu prognožu pārrēķināšanu:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Šī komanda noder, lai ģenerētu atjauninātus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu brīdinājumu sistēmas noteiktā projekta laika posmā.

## `tls-status` komandas izmantošana

Komanda `tls-status` ***digna*** CLI lieto, lai pieprasītu Traffic Light System (TLS) statusu konkrētai tabulai projektā noteiktā datumā. Traffic Light System sniedz ieskatu par datu veselību un kvalitāti, norādot uz problēmām vai brīdinājumiem, kam jāpievērš uzmanība.
  
#### Komandas lietošana
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura TLS statusu pieprasāt (obligāti).
- **TABLE_NAME**: Konkrētā tabula projektā, kurai nepieciešams TLS statuss (obligāti).
- **DATE**: Datums, par kuru tiek pieprasīts TLS statuss, parasti formātā %Y-%m-%d (obligāti).
  
#### Piemērs
  
Lai pārbaudītu TLS statusu tabulai UserData projektā ProjectA 2024. gada 1. jūlijā:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Šī komanda palīdz lietotājiem uzraudzīt un uzturēt datu kvalitāti, sniedzot skaidru un rīcībspējīgu statusa pārskatu, balstoties uz iepriekš definētiem kritērijiem.

## `inspect-async` komandas izmantošana

Komanda `inspect-async` ***digna*** CLI lieto, lai norādītu backend sākt asinhrono pārbaudi vienam vai vairākiem datu avotiem konkrētā projektā. Ja project_name ir iestatīts uz all-projects, pārbaude iterēs pār visiem pieejamiem projektiem un veiks inspect operāciju. Komanda atgriež request id, ko var izmantot, lai izsekotu pārbaudes progresu.

#### Komandas lietošana

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kuram dati tiek pārbaudīti (obligāti). Ja kā argumentu izmanto atslēgvārdu all-projects, ***digna*** izpildīs šo komandu visos esošajos projektos.
- **FROM_DATE**: Sākuma datums un laiks datu pārbaudei. Pieņemamie formāti: %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vai %Y-%m-%d %H:%M:%S (obligāti).
- **TO_DATE**: Beigu datums un laiks datu pārbaudei, izmantojot tos pašus formātus kā FROM_DATE (obligāti).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo pārbaudi uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtē, lai pārbaudītu tikai tabulas, kuru nosaukumos ir norādītā apakšvirkne.

  
#### Piemērs
  
Lai asinhroni pārbaudītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## `inspect-status` komandas izmantošana

Komanda `inspect-status` ***digna*** CLI lieto, lai pārbaudītu asinhronās pārbaudes progresu, pamatojoties uz request ID.

#### Komandas lietošana

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenti
  
- **REQUEST_ID**: pieprasījuma ID, ko atgrieza komanda `inspect-async` 
  
#### Opcijas

- `--report_level`, `-rl`: Uzstāda atskaites līmeni: 'task' vai 'step' [noklusējums: task]
  
#### Piemērs
  
Lai pārbaudītu pārbaudes progresu ar request ID 12345 detalizētā step līmenī:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## `export-ds` komandas izmantošana

Komanda `export-ds` ***digna*** CLI lieto, lai izveidotu datu avotu eksportu no ***digna*** repozitorija. Pēc noklusējuma tiks eksportēti visi datu avoti no norādītā projekta.

#### Komandas lietošana
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, no kura datu avoti tiks eksportēti.

#### Opcijas

- `--table_name`, `-tn`: Eksportē konkrētu datu avotu no projekta.
- `--exportfile`, `-ef`: Norāda eksportējamā faila nosaukumu.
    
#### Piemērs
  
Lai eksportētu visus datu avotus no projekta `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Šī komanda eksportē visus datu avotus no `ProjectA` kā JSON dokumentu, kuru var importēt citā projektā vai ***digna*** repozitorijā.


## `import-ds` komandas izmantošana

Komanda `import-ds` ***digna*** CLI lieto, lai importētu datu avotus mērķa projektā un izveidotu importa pārskatu.

#### Komandas lietošana
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru datu avoti tiks importēti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kuru importēt.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importa pārskatu (ja nav norādīts, izvada terminālī tabulas formātā).
- `--output-format`, `-f`: Formāts, kurā saglabāt importa pārskatu (json, csv).
    
#### Piemērs
  
Lai importētu visus datu avotus no eksportēšanas faila `my_export.json` uz `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pēc importa šī komanda arī parādīs pārskatu par importētajiem un izlaistajiem objektiem. Tiks importēti tikai jauni datu avoti projektā `ProjectB`. Lai uzzinātu, kuri objekti tiktu importēti un kuri izlaisti, varat izmantot komandu `plan-import-ds`.

## `plan-import-ds` komandas izmantošana

Komanda `plan-import-ds` ***digna*** CLI lieto, lai izplānotu datu avotu importu mērķa projektā un izveidotu importa pārskatu pirms faktiskā importa.

#### Komandas lietošana
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru datu avoti tiktu importēti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kuru analizēt pirms importa.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importa pārskatu (ja nav norādīts, izvada terminālī tabulas formātā).
- `--output-format`, `-f`: Formāts, kurā saglabāt importa pārskatu (json, csv).
    
#### Piemērs
  
Lai pārbaudītu, kuri datu avoti tiktu importēti un kuri izlaisti no eksportēšanas faila `my_export.json`, importējot tos uz `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Šī komanda tikai parādīs importa plānu objektu importam un izlaistajiem objektiem.