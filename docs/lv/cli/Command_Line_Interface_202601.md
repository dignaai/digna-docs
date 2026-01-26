---
title: digna CLI atsauce 2026.01 – Komandas un piemēri | digna dokumentācija
description: Pilna atsauce par digna CLI izlaidumu 2026.01. Uzziniet, kā pārvaldīt lietotājus, repozitorijus un datus ar komandām, piemēram, add-user, check-config, check-repo-connection, inspect, inspect-async un citām.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202601/
image: /assets/logo_square.png
---

# digna CLI atsauce 2026.01
**2026-01-15**

Šajā lapā dokumentēts pilns komandu kopums, kas pieejams ***digna*** CLI izlaidumā **2026.01**, ieskaitot lietošanas piemērus un opcijas.

---

## CLI pamati

---

### help
Opcija `--help` sniedz informāciju par pieejamajām komandām un to lietošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārējā palīdzība:**
   
    Lietojiet --help tūlīt pēc atslēgvārda ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Palīgs konkrētai komandai:**  
  
    Lai saņemtu detalizētu informāciju par konkrētu komandu, pievienojiet tai `--help`.
    Piemēram, lai saņemtu palīdzību par komandu `add-user`, izpildiet:
     ```bash
     dignacli add-user --help
     ```

     ### izvade:
      
     - **Komandas apraksts:** Sniedz detalizētu aprakstu par to, ko komanda dara.  
     - **Sintakse:** Parāda precīzu sintaksi, iekļaujot obligātos un izvēles argumentus.  
     - **Opcijas:** Uzskaita komandas specifiskās opcijas un to skaidrojumus.  
     - **Piemēri:** Sniedz piemērus, kā efektīvi izpildīt komandu.

### check-config

Komanda `check-config` ir utilīta ***digna*** CLI rīkā, paredzēta, lai pārbaudītu ***digna*** konfigurāciju. Šī komanda nodrošina, ka ***digna*** komponentes var atrast nepieciešamos konfigurācijas elementus config.toml failā.

#### Opcijas

- `--configpath`, `-cp`: Fails vai direktorija, kas satur konfigurāciju. Ja nav norādīts, tiks izmantots ../config.toml.
      
#### Komandas lietošana
```bash
dignacli check-config
```

Veiksmīgas izpildes gadījumā komanda izvada apstiprinājumu par konfigurācijas pilnību.  
  
Ja konfigurācija šķiet nepilnīga, tiks uzskaitīti trūkstošie konfigurācijas elementi.

  
### check-repo-connection

Komanda `check-repo-connection` ir utilīta ***digna*** CLI rīkā, paredzēta, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repozitorijam. Šī komanda nodrošina, ka CLI var mijiedarboties ar repozitoriju.
      
#### Komandas lietošana
```bash
dignacli check-repo-connection
```

Veiksmīgas izpildes gadījumā komanda izvada apstiprinājumu par savienojumu, kā arī informāciju par repozitoriju: repozitorija versiju, hostu, datubāzi un shēmu.  
  
Ja repozitorija savienojums nav izdevies, pārbaudiet config.toml failu, lai pārliecinātos par pareiziem konfigurācijas iestatījumiem.


### version

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju --version.  
  
#### Komandas lietošana
```bash
dignacli --version
```
  
#### Piemēra izvade
```bash
dignacli version 2026.01
```

### žurnālošanas opcijas
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir paredzēta minimālistiska. Lielākajai daļai komandu ir iespēja sniegt papildu informāciju, izmantojot šādas opcijas:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” un “debug” nosaka detaļu līmeni, savukārt “logfile” opcija ļauj pāradresēt izvadi uz failu nevis konsoli.

## Lietotāju pārvaldība

### add-user
  
Komanda `add-user` ***digna*** CLI tiek izmantota, lai pievienotu jaunu lietotāju ***digna*** sistēmā.
  
#### Komandas lietošana
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāts).
- **USER_FULL_NAME**: Jaunā lietotāja pilnais vārds (obligāts).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāta).

#### Opcijas

- `--is_superuser`, `-su`: Flagma, kas apzīmē jauno lietotāju kā administratoru.
- `--valid_until`, `-vu`: Nosaka konta derīguma termiņu formātā `YYYY-MM-DD HH:MI:SS`. Ja nav norādīts, kontam nav derīguma termiņa.

#### Piemērs

Lai pievienotu jaunu lietotāju ar lietotājvārdu `jdoe`, pilnu vārdu `John Doe` un paroli `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lai pievienotu jaunu lietotāju un iestatītu konta derīguma termiņu:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Komanda `delete-user` ***digna*** CLI tiek izmantota, lai noņemtu esošu lietotāju no ***digna*** sistēmas.
  
#### Komandas lietošana
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenti
- **USER_NAME**: Lietotājvārds lietotāja, kuru vēlaties dzēst (obligāts). Tas ir vienīgais komandas prasītais arguments.

#### Piemērs
```bash
dignacli delete-user jdoe
```
  
Izpildot šo komandu, lietotājs `jdoe` tiks noņemts no ***digna*** sistēmas, atņemot piekļuvi un dzēšot ar viņu saistītos datus un atļaujas no repozitorija.

### modify-user

Komanda `modify-user` ***digna*** CLI tiek izmantota, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

#### Komandas lietošana
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotāja, kuru jāmaina (obligāts).
- **USER_FULL_NAME**: Jaunais pilnais vārds lietotājam (obligāts).
  
#### Opcijas  
  
- `--is_superuser`, `-su`: Iestata lietotāju par superuser, piešķirot paaugstinātas tiesības. Šai karodziņai nav nepieciešama vērtība.  
- `--valid_until`, `-vu`: Nosaka konta derīguma termiņu formātā YYYY-MM-DD HH:MI:SS. Ja nav norādīts, konts paliek derīgs beztermiņa.  
  
#### Piemērs
  
Lai mainītu lietotāja `jdoe` pilno vārdu uz “Johnathan Doe” un iestatītu lietotāju kā superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Komanda `modify-user-pwd` ***digna*** CLI tiek izmantota, lai nomainītu esoša lietotāja paroli ***digna*** sistēmā.
  
#### Komandas lietošana
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotāja, kura paroli jāmaina (obligāts).
- **USER_PWD**: Jaunā parole lietotājam (obligāta).
  
#### Piemērs
  
Lai nomainītu lietotāja `jdoe` paroli uz `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Komanda `list-users` ***digna*** CLI parāda visu lietotāju sarakstu, kas reģistrēti ***digna*** sistēmā.

#### Komandas lietošana

```bash
dignacli list-users
```

Izpildot šo komandu ***digna*** CLI pieslēgsies pie ***digna*** repozitorija un uzrādīs visus lietotājus, parādot to ID, lietotājvārdu, pilnu vārdu, superuser statusu un derīguma laika zīmogus.

## Repozitorija pārvaldība

### upgrade-repo
  
Komanda `upgrade-repo` ***digna*** CLI tiek izmantota, lai jauninātu vai inicializētu ***digna*** repozitoriju. Šī komanda ir būtiska, lai piemērotu atjauninājumus vai uzstādītu repozitorija infrastruktūru pirmo reizi.
  
#### Komandas lietošana

```bash
dignacli upgrade-repo [options]
```
  
#### Opcijas
  
- `--simulation-mode`, `-s`: Ja ieslēgta, komanda darbojas simulācijas režīmā, izdrukājot SQL vaicājumus, kas tiktu izpildīti, bet tos faktiski neizpilda. Tas ir noderīgi, lai priekšskatītu izmaiņas, neveicot modifikācijas repozitorijā.  

  
#### Piemērs
  
Lai jauninātu ***digna*** repozitoriju, varat izpildīt komandu bez papildopcijām:
  
```bash
dignacli upgrade-repo
```  
Lai palaistu jauninājumu simulācijas režīmā (lai redzētu SQL vaicājumus bez to piemērošanas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Šī komanda ir būtiska, lai uzturētu ***digna*** sistēmu, nodrošinot, ka datubāzes shēma un citi repozitorija komponenti ir atjaunināti uz jaunāko programmatūras versiju.

### encrypt
  
Komanda `encrypt` ***digna*** CLI tiek izmantota, lai šifrētu paroli.
  
#### Komandas lietošana
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Parole, kuru nepieciešams šifrēt (obligāta).
  
#### Piemērs
  
Lai šifrētu paroli, parole jānorāda kā arguments.   
Piemēram, lai šifrētu paroli `mypassword123`, izmantojiet:
```bash
dignacli encrypt mypassword123
```
Šī komanda izvadīs norādītās paroles šifrēto versiju, kuru pēc tam var izmantot drošos kontekstos. Ja paroles arguments netiks norādīts, CLI parādīs kļūdu, norādot uz trūkstošo argumentu.

### generate-key
  
Komanda `generate-key` tiek izmantota, lai ģenerētu Fernet atslēgu, kas ir būtiska paroles glabāšanas drošībai ***digna*** repozitorijā.
  
#### Komandas lietošana
```bash
dignacli generate-key
```
  
## Datu pārvaldība

### clean-up

Komanda `clean-up` ***digna*** CLI tiek izmantota, lai noņemtu profilus, prognozes un satiksmes gaismas sistēmas datus vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda ir būtiska datu dzīves cikla pārvaldībai, palīdzot uzturēt sakārtotu un efektīvu datu vidi, tīrot novecojušus vai nevajadzīgus datus.

#### Komandas lietošana

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, no kura tiks noņemti dati (obligāts). Ja šajā argumentā norādīts atslēgvārds all-projects, ***digna*** iterēs pār visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Datumu un laiku, no kura sākt datu noņemšanu. Pieļaujamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Datumu un laiku, līdz kuram tiks noņemti dati, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas
  
- `--table-name`, `-tn`: Ierobežo clean-up darbību uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtri, kas ierobežo clean-up uz tabulām, kuru nosaukumos ir norādītā apakšvirkne.
- `--timing`, `-tm`: Parāda clean-up procesa ilgumu pēc tā pabeigšanas.
- `--help`: Parāda palīdzību par clean-up komandu un izejiet.
  
#### Piemērs
  
Lai noņemtu datus no projekta ProjectA no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Lai noņemtu datus tikai no konkrētas tabulas ar nosaukumu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Šī komanda palīdz pārvaldīt datu glabāšanu un nodrošina, ka repozitorijā saglabājas tikai relevanti dati.

### remove-orphans
  
Komanda `remove-orphans` ***digna*** CLI tiek izmantota, lai veiktu repozitorija apkopes darbus.  
Kad lietotājs dzēš projektus vai datu avotus, profili un prognozes paliek repozitorijā. Ar šo komandu šādi pamestie ieraksti tiks izņemti no repozitorija.
  
#### Komandas lietošana
  
```bash
dignacli list-projects
```

### list-projects
  
Komanda `list-projects` ***digna*** CLI tiek izmantota, lai attēlotu visu pieejamo projektu sarakstu ***digna*** sistēmā.
  
#### Komandas lietošana
  
```bash
dignacli list-projects
```

Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kas pārvalda vairākus projektus, nodrošinot ātru pārskatu par pieejamajiem projektiem ***digna*** repozitorijā.

### list-ds

Komanda `list-ds` ***digna*** CLI tiek izmantota, lai attēlotu visu pieejamo datu avotu sarakstu norādītā projektā. Šī komanda ir noderīga, lai saprastu analīzei un pārvaldībai pieejamos datu resursus ***digna*** sistēmā.

#### Komandas lietošana
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek uzskaitīti datu avoti (obligāts).
  
#### Piemērs
  
Lai uzskaitītu visus datu avotus projektā ar nosaukumu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Šī komanda sniedz pārskatu par projekta datu avotiem, palīdzot efektīvāk orientēties un pārvaldīt datu ainavu.


### inspect

Komanda `inspect` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un satiksmes gaismas sistēmas datus vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda palīdz analizēt un uzraudzīt datus noteiktā periodā. Pabeidzot inspekciju, tiek atgriezta aprēķinātās satiksmes gaismas sistēmas vērtība:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komandas lietošana

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus jāpārbauda (obligāts). Ja šajā argumentā norādīts atslēgvārds all-projects, ***digna*** iterēs pār visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Inspekcijas sākuma datums un laiks. Pieļaujamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Inspekcijas beigu datums un laiks, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtri, lai inspektētu tikai tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--enable_notification`, `-en`: Iespējo paziņojumu sūtīšanu gadījumos, kad tiek konstatēti trauksmes signāli.
- `--bypass-backend`, `-bb`: Apiet backend un palaist inspekciju tieši no CLI (tikai testēšanas nolūkos!).

  
#### Piemērs
  
Lai pārbaudītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Lai inspektētu tikai konkrētu tabulu un piespiestu prognožu pārrēķinu:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Šī komanda ir noderīga, lai ģenerētu atjauninātus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu trauksmju sistēmas noteiktā projekta laika posmā.

### inspect-async

Komanda `inspect-async` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un satiksmes gaismas sistēmas datus vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda palīdz analizēt un uzraudzīt datus noteiktā periodā. Atšķirībā no `inspect` komandas, tā negaida inspekcijas pabeigšanu.
Tā vietā tiek atgriezts pieprasījuma ID iesniegtajam inspekcijas pieprasījumam. Lai vaicātu inspekcijas procesa progresu, izmantojiet komandu `inspect-status`.

#### Komandas lietošana

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus jāpārbauda (obligāts). Ja šajā argumentā norādīts atslēgvārds all-projects, ***digna*** iterēs pār visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Inspekcijas sākuma datums un laiks. Pieļaujamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Inspekcijas beigu datums un laiks, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtri, lai inspektētu tikai tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--enable_notification`, `-en`: Iespējo paziņojumu sūtīšanu gadījumos, kad tiek konstatēti trauksmes signāli.

  
#### Piemērs
  
Lai asinhroni pārbaudītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Komanda `inspect-status` ***digna*** CLI tiek izmantota, lai pārbaudītu asinhronas inspekcijas progresu pēc pieprasījuma ID.

#### Komandas lietošana

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: Pieprasījuma ID, ko atgrieza komanda `inspect-async` 
  
#### Piemērs
  
Lai pārbaudītu inspekcijas progresu ar pieprasījuma ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Komanda `inspect-cancel` ***digna*** CLI tiek izmantota, lai atceltu inspekcijas, balstoties uz pieprasījuma ID, vai arī to var izmantot, lai atceltu visus pašreizējos pieprasījumus.

#### Komandas lietošana

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: Pieprasījuma ID, ko atgrieza komanda `inspect-async` 
  
#### Piemērs
  
Lai atceltu inspekciju ar pieprasījuma ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Lai atceltu visus pašreizējā laikā darbojošos vai gaidošos pieprasījumus:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Komanda `export-ds` ***digna*** CLI tiek izmantota, lai izveidotu datu avotu eksportu no ***digna*** repozitorija. Pēc noklusējuma tiks eksportēti visi datu avoti no norādītā projekta.

#### Komandas lietošana
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, no kura tiks eksportēti datu avoti.

#### Opcijas

- `--table_name`, `-tn`: Eksportēt konkrētu datu avotu no projekta.
- `--exportfile`, `-ef`: Norādīt eksporta faila nosaukumu.
    
#### Piemērs
  
Lai eksportētu visus datu avotus no projekta ar nosaukumu `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Šī komanda eksportē visus datu avotus no `ProjectA` kā JSON dokumentu, kuru var importēt citā projektā vai ***digna*** repozitorijā.


### import-ds

Komanda `import-ds` ***digna*** CLI tiek izmantota, lai importētu datu avotus mērķprojektā un izveidotu importa atskaiti.

#### Komandas lietošana
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru tiks importēti datu avoti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kuru importēs.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importa atskaiti (ja nav norādīts, izvada terminālī tabulārā formā).
- `--output-format`, `-f`: Formāts importa atskaitei (json, csv).
    
#### Piemērs
  
Lai importētu visus datu avotus no eksporta faila `my_export.json` uz `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pēc importa šī komanda parādīs arī atskaiti par importētajiem un izlaistajiem objektiem. Tikt importēti tikai jauni datu avoti `ProjectB`. Lai noskaidrotu, kuri objekti tiktu importēti un kuri izlaisti, varat izmantot komandu `plan-import-ds`

### plan-import-ds

Komanda `plan-import-ds` ***digna*** CLI tiek izmantota, lai izplānotu datu avotu importu mērķprojektā un izveidotu importa atskaiti (bez faktiskas importa izpildes).

#### Komandas lietošana
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru dati tiktu importēti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kuru analizēs pirms importēšanas.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importa atskaiti (ja nav norādīts, izvada terminālī tabulārā formā).
- `--output-format`, `-f`: Formāts importa atskaitei (json, csv).
    
#### Piemērs
  
Lai pārbaudītu, kuri datu avoti tiktu importēti un kuri izlaisti no eksporta faila `my_export.json`, importējot tos uz `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Šī komanda tikai parādīs importa plānu par objektiem, kas tiktu importēti un izlaisti.