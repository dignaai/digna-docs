---
title: digna CLI atsauce 2024.12 – Komandas un piemēri | digna dokumentācija
description: Pilna digna CLI izlaiduma 2024.12 atsauce. Uzziniet, kā pārvaldīt lietotājus, repozitorijus un datus ar komandām, piemēram, add-user, check-repo-connection, upgrade-repo, inspect u.c.
image: /assets/logo_square.png
---


# digna CLI atsauce 2024.12
**2024-12-09**

Šī lapa dokumentē pilnu komandu kopumu, kas pieejams ***digna*** CLI izlaidumā **2024.12**, tostarp lietošanas piemērus un opcijas.

---


**2024-12-09**


---

## CLI pamati

---

## `help` opcijas izmantošana

Opcija `--help` sniedz informāciju par pieejamajām komandām un to lietošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārīgās palīdzības attēlošana:**
   
   Izmantojiet `--help` tieši pēc komandvārda ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Palīdzība konkrētām komandām:**  
  
    Lai iegūtu detalizētu informāciju par konkrētu komandu, pievienojiet `--help` pie tās.
    Piemēram, lai saņemtu palīdzību par komandu `add-user`, izpildiet:
     ```bash
     dignacli add-user --help
     ```

     ### izvade:
      
     - **Komandas apraksts:** Sniedz detalizētu aprakstu par to, ko komanda dara.  
     - **Sintakse:** Rāda precīzu sintaksi, ieskaitot obligātos un izvēles argumentus.  
     - **Opcijas:** Uzrāda komandas specifiskās opcijas kopā ar to skaidrojumiem.  
     - **Piemēri:** Sniedz piemērus, kā efektīvi izpildīt komandu.

  
## `check-repo-connection` komandas izmantošana

Komanda check-repo-connection ir utilīta ***digna*** CLI rīkā, kas paredzēta, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repozitorijam. Šī komanda nodrošina, ka CLI var sadarboties ar repozitoriju.
      
### Komandas lietošana
```bash
dignacli check-repo-connection
```

Veiksmīgas izpildes gadījumā komanda izvada savienojuma apstiprinājumu, kā arī informāciju par repozitoriju: repozitorija versiju, hostu, datubāzi un shēmu.  
  
Ja repozitorija savienojums nav veiksmīgs, pārbaudiet config.toml failu, vai konfigurācijas iestatījumi ir pareizi.

## ‘version’ komandas izmantošana

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju `--version`.  
  
### Komandas lietošana
```bash
dignacli --version
```
  
### Piemēra izvade
```bash
dignacli version 2024.12
```

## Žurnālu (logging) opciju izmantošana
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir ieplānota kā minimālistiska. Lielākā daļa komandu piedāvā iespēju iegūt papildus informāciju, izmantojot šādas opcijas:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” un “debug” nosaka detalizētības līmeni, savukārt “logfile” slēdzis ļauj pāradresēt izvadi uz failu, nevis konsoles logu.

# Lietotāju pārvaldība

## ‘add-user’ komandas izmantošana
  
Komanda add-user ***digna*** CLI tiek izmantota, lai pievienotu jaunu lietotāju ***digna*** sistēmai.
  
### Komandas lietošana
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenti

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāti).
- **USER_FULL_NAME**: Jaunā lietotāja pilns vārds (obligāti).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāti).

### Opcijas

- `--is_superuser`, `-su`: Režģis, lai piešķirtu jaunajam lietotājam administratora tiesības.
- `--valid_until`, `-vu`: Uzstāda konta derīguma termiņu formātā `YYYY-MM-DD HH:MI:SS`. Ja nav uzstādīts, kontam nav derīguma termiņa.

### Piemērs

Lai pievienotu jaunu lietotāju ar lietotājvārdu `jdoe`, pilnu vārdu `John Doe` un paroli `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lai pievienotu jaunu lietotāju un uzstādītu konta derīguma datumu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## `delete-user` komandas izmantošana
  
Komanda `delete-user` ***digna*** CLI tiek izmantota, lai noņemtu esošu lietotāju no ***digna*** sistēmas.
  
### Komandas lietošana
```bash
dignacli delete-user USER_NAME
```
  
### Argumenti
- **USER_NAME**: Dzēšamā lietotāja lietotājvārds (obligāti). Tā ir vienīgā komandai nepieciešamā argumenta vērtība.

### Piemērs
```bash
dignacli delete-user jdoe
```
  
Izpildot šo komandu, lietotājs `jdoe` tiks noņemts no ***digna*** sistēmas, zaudējot piekļuvi, un tiks izdzēsti viņam saistītie dati un tiesības repozitorijā.

## `modify-user` komandas izmantošana

Komanda `modify-user` ***digna*** CLI tiek izmantota, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

### Komandas lietošana
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenti
  
- **USER_NAME**: Modificējamā lietotāja lietotājvārds (obligāti).
- **USER_FULL_NAME**: Jaunais pilnais vārds lietotājam (obligāti).
  
### Opcijas  
  
- `--is_superuser`, `-su`: Uzstāda lietotāju kā superlietotāju, piešķirot paaugstinātas privilēģijas. Šim slēdzim nav nepieciešama vērtība.  
- `--valid_until`, `-vu`: Uzstāda konta derīguma datumu formātā YYYY-MM-DD HH:MI:SS. Ja nav norādīts, konts paliek derīgs beztermiņa.  
  
### Piemērs
  
Lai mainītu lietotāja `jdoe` pilno vārdu uz “Johnathan Doe” un piešķirtu tam superlietotāja tiesības:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## `modify-user-pwd` komandas izmantošana
  
Komanda `modify-user-pwd` ***digna*** CLI tiek izmantota, lai mainītu esoša lietotāja paroli ***digna*** sistēmā.
  
### Komandas lietošana
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenti
  
- **USER_NAME**: Lietotājvārds, kura parole jāmaina (obligāti).
- **USER_PWD**: Jaunā parole lietotājam (obligāti).
  
### Piemērs
  
Lai nomainītu lietotāja `jdoe` paroli uz `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## `list-users` komandas izmantošana

Komanda `list-users` ***digna*** CLI attēlo visu lietotāju sarakstu, kas reģistrēti ***digna*** sistēmā.

### Komandas lietošana

```bash
dignacli list-users
```

Izpildot šo komandu ***digna*** CLI pieslēgsies ***digna*** repozitorijam un uzrādīs visus lietotājus, rādīdams to ID, lietotājvārdu, pilnu vārdu, superlietotāja statusu un derīguma laika zīmogus.

# Repozitorija pārvaldība

### `upgrade-repo` komandas izmantošana
  
Komanda `upgrade-repo` ***digna*** CLI tiek izmantota, lai atjauninātu vai inicializētu ***digna*** repozitoriju. Šī komanda ir būtiska, lai pielietotu atjauninājumus vai pirmreizēji iestatītu repozitorija infrastruktūru.
  
### Komandas lietošana

```bash
dignacli upgrade-repo [options]
```
  
### Opcijas
  
- `--simulation-mode`, `-s`: Ja iespējota, šī opcija izpilda komandu simulācijas režīmā, kas izdrukā SQL vaicājumus, kas tiktu izpildīti, taču tos faktiski neveic. Tas noderīgi, lai priekšskatītu izmaiņas, neveicot izmaiņas repozitorijā.  

  
### Piemērs
  
Lai atjauninātu ***digna*** repozitoriju, varat izpildīt komandu bez papildus opcijām:
  
```bash
dignacli upgrade-repo
```  
Lai palaistu atjaunināšanu simulācijas režīmā (lai redzētu SQL vaicājumus bez to piemērošanas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Šī komanda ir svarīga, lai uzturētu ***digna*** sistēmu, nodrošinot, ka datubāzes shēma un citi repozitorija komponenti ir atjaunināti atbilstoši jaunākajai programmatūras versijai.

## `encrypt` komandas izmantošana
  
Komanda `encrypt` ***digna*** CLI tiek izmantota, lai šifrētu paroli.
  
### Komandas lietošana
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenti
- **PASSWORD**: Parole, kuru nepieciešams šifrēt (obligāti).
  
### Piemērs
  
Lai šifrētu paroli, parole jānodod kā arguments.   
Piemēram, lai šifrētu paroli `mypassword123`, izmantojiet:
```bash
dignacli encrypt mypassword123
```
Šī komanda izvadīs norādītās paroles šifrēto versiju, kuru pēc tam var izmantot drošos kontekstos. Ja paroles arguments netiek nodots, CLI parādīs kļūdu, norādot uz trūkstošo argumentu.

## `generate-key` komandas izmantošana
  
Komanda `generate-key` tiek izmantota, lai ģenerētu Fernet atslēgu, kas ir būtiska parolu drošināšanai, kas glabātas ***digna*** repozitorijā.
  
### Komandas lietošana
```bash
dignacli generate-key
```
  
# Datu pārvaldība

## `clean-up` komandas izmantošana

Komanda `clean-up` ***digna*** CLI tiek izmantota, lai noņemtu profilus, prognozes un Traffic Light System datus vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda ir būtiska datu cikla pārvaldībai, palīdzot uzturēt organizētu un efektīvu datu vidi, iztīrot novecojušus vai nevajadzīgus datus.

### Komandas lietošana

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, no kura jānoņem dati (obligāti). Ja šajā argumentā izmanto atslēgvārdu all-projects, ***digna*** iterēs pāri visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Sākuma datums un laiks datu dzēšanai. Pieņemamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāti).
- **TO_DATE**: Beigu datums un laiks datu dzēšanai, sekojot tādiem pašiem formātiem kā FROM_DATE (obligāti).
  
### Opcijas
  
- `--table-name`, `-tn`: Ierobežo clean-up darbību uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrs, kas ierobežo clean-up tikai uz tabulām, kuru nosaukumos ir norādītais apakšvirkne.
- `--timing`, `-tm`: Pēc pabeigšanas parāda clean-up procesa norises laiku.
- `--help`: Parāda palīdzību clean-up komandai un iziet.
  
### Piemērs
  
Lai noņemtu datus no projekta ProjectA no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Lai noņemtu datus tikai no konkrētas tabulas `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Šī komanda palīdz pārvaldīt datu glabāšanu un nodrošina, ka repozitorijā saglabājas tikai aktuāla informācija.

## `inspect` komandas izmantošana

Komanda `inspect` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un Traffic Light System datus vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda palīdz analizēt un uzraudzīt datus norādītajā laika periodā.

### Komandas lietošana

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus jāizpēta (obligāti). Ja šajā argumentā izmanto atslēgvārdu all-projects, ***digna*** iterēs pāri visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Sākuma datums un laiks datu izpētei. Pieņemamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāti).
- **TO_DATE**: Beigu datums un laiks datu izpētei, sekojot tādiem pašiem formātiem kā FROM_DATE (obligāti).
  
### Opcijas

- `--table-name`, `-tn`: Ierobežo izpēti uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrē, lai izpētītu tikai tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--do-profile`: Aktivizē profilu atkārtotu vākšanu. Noklusējums ir do-profile.
- `--no-do-profile`: Novērš profilu atkārtotu vākšanu.
- `--do-prediction`: Aktivizē prognožu pārrēķināšanu. Noklusējums ir do-prediction.
- `--no-do-prediction`: Novērš prognožu pārrēķināšanu.
- `--do-alert-status`: Aktivizē brīdinājumu statusu pārrēķināšanu. Noklusējums ir do-alert-status.
- `--no-do-alert-status`: Novērš brīdinājumu statusu pārrēķināšanu.
- `--iterative`: Aktivizē perioda izpēti, izmantojot dienas iterācijas. Noklusējums ir iterative.
- `--no-iterative`: Veic izpēti par visu periodu vienā reizē.
- `--timing`, `-tm`: Pēc pabeigšanas parāda izpētes procesa ilgumu.
  
### Piemērs
  
Lai izpētītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Lai izpētītu tikai konkrētu tabulu un piespiestu prognožu pārrēķināšanu:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Šī komanda ir noderīga, lai ģenerētu atjauninātus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu brīdinājumu sistēmas norādītajā projekta laika posmā.

## `tls-status` komandas izmantošana

Komanda `tls-status` ***digna*** CLI tiek izmantota, lai uzdotu jautājumu par Traffic Light System (TLS) statusu konkrētai tabulai projektā dotajā datumā. Traffic Light System sniedz ieskatu par datu veselumu un kvalitāti, norādot uz iespējamiem jautājumiem vai brīdinājumiem, kuriem jāpiešķir uzmanība.
  
### Komandas lietošana
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek vaicāts TLS status (obligāti).
- **TABLE_NAME**: Konkrētā tabula projektā, kurai nepieciešams TLS statuss (obligāti).
- **DATE**: Datums, par kuru tiek vaicāts TLS statuss, parasti formātā %Y-%m-%d (obligāti).
  
### Piemērs
  
Lai pārbaudītu TLS statusu tabulai UserData projektā ProjectA 2024. gada 1. jūlijā:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Šī komanda palīdz lietotājiem uzraudzīt un uzturēt datu kvalitāti, sniedzot skaidru un izmantojamu statusa atskaiti, balstoties uz iepriekš definētiem kritērijiem.

## `list-projects` komandas izmantošana
  
Komanda `list-projects` ***digna*** CLI tiek izmantota, lai attēlotu visu pieejamo projektu sarakstu ***digna*** sistēmā.
  
### Komandas lietošana
  
```bash
dignacli list-projects
```

Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kas pārvalda vairākus projektus, sniedzot ātru pārskatu par pieejamajiem projektiem ***digna*** repozitorijā.

## `list-ds` komandas izmantošana

Komanda `list-ds` ***digna*** CLI tiek izmantota, lai attēlotu visu pieejamo datu avotu sarakstu norādītā projektā. Šī komanda noder, lai saprastu datu aktīvus, kas pieejami analīzei un pārvaldībai ***digna*** sistēmā.

### Komandas lietošana
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek uzskaitīti datu avoti (obligāti).
  
### Piemērs
  
Lai uzskaitītu visus datu avotus projektā `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Šī komanda sniedz lietotājiem pārskatu par projekta datu avotiem, palīdzot tiem efektīvāk orientēties un pārvaldīt datu vidi.