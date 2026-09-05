# digna CLI Atsauce 2025.09
**2025-09-29**

Šajā lapā dokumentēts pilns komandu komplekts, kas pieejams ***digna*** CLI izlaidumā **2025.09**, tostarp izmantošanas piemēri un opcijas.

---

## CLI pamati

---

### help
Opcija `--help` sniedz informāciju par pieejamajām komandām un to izmantošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārējās palīgrinas attēlošana:**
   
    Izmantojiet --help uzreiz pēc atslēgvārda ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Palīginformācija par konkrētām komandām:**  
  
    Lai iegūtu detalizētu informāciju par konkrētu komandu, pievienojiet tai `--help`.
    Piemēram, lai iegūtu palīdzību par komandu `add-user`, palaidiet:
     ```bash
     dignacli add-user --help
     ```

     ### izvade:
      
     - **Komandas apraksts:** Sniedz detalizētu aprakstu par to, ko komanda dara.  
     - **Sintakse:** Rāda precīzu sintaksi, ieskaitot obligātos un izvēles argumentus.  
     - **Opcijas:** Uzskaita visas komandas specifiskās opcijas un to paskaidrojumus.  
     - **Piemēri:** Sniedz piemērus, kā efektīvi izpildīt komandu.

### check-config

Komanda check-config ir rīks ***digna*** CLI ietvaros, paredzēts, lai pārbaudītu ***digna*** konfigurāciju. Šī komanda nodrošina, ka ***digna*** komponentes spēj atrast nepieciešamos konfigurācijas elementus config.toml.

#### Opcijas

- `--configpath`, `-cp`: Fails vai direktorija, kas satur konfigurāciju. Ja nav norādīts, tiks izmantots ../config.toml.
      
#### Komandas izmantošana
```bash
dignacli check-config
```

Veiksmīgas izpildes gadījumā komanda izvada apstiprinājumu par konfigurācijas pilnību.  
  
Ja konfigurācija šķiet nepilnīga, tiks uzskaitīti trūkstošie konfigurācijas elementi.

  
### check-repo-connection

Komanda check-repo-connection ir rīks ***digna*** CLI ietvaros, paredzēts, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repozitorijam. Šī komanda nodrošina, ka CLI var mijiedarboties ar repozitoriju.
      
#### Komandas izmantošana
```bash
dignacli check-repo-connection
```

Veiksmīgas izpildes gadījumā komanda izvada apstiprinājumu par savienojumu, kā arī informāciju par repozitoriju: Repository version, Host, Database un Schema.  
  
Ja savienojums ar repozitoriju nav veiksmīgs, pārbaudiet config.toml failu, lai pārliecinātos par pareiziem konfigurācijas iestatījumiem.


### version

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju --version.  
  
#### Komandas izmantošana
```bash
dignacli --version
```
  
#### Piemēra izvade
```bash
dignacli version 2025.09
```

### reģistrēšanas (logging) opcijas
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir veidota minimālistiska. Lielākā daļa komandu piedāvā iespēju sniegt papildinformāciju, izmantojot šādas opcijas:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
“verbose” un “debug” nosaka detalizācijas līmeni, kamēr pārslēgs “logfile” ļauj pāradresēt izvadi uz failu, nevis konsoles logu.

## Lietotāju pārvaldība

### add-user
  
Komanda add-user ***digna*** CLI tiek izmantota, lai pievienotu jaunu lietotāju ***digna*** sistēmai.
  
#### Komandas izmantošana
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāts).
- **USER_FULL_NAME**: Jaunā lietotāja pilnais vārds (obligāts).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāts).

#### Opcijas

- `--is_superuser`, `-su`: Pārslēdzis, lai piešķirtu jaunajam lietotājam administratora tiesības.
- `--valid_until`, `-vu`: Nosaka lietotāja konta derīguma termiņu formātā `YYYY-MM-DD HH:MI:SS`. Ja netiek norādīts, kontam nav derīguma termiņa.

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
  
#### Komandas izmantošana
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenti
- **USER_NAME**: Lietotājvārds lietotājam, kuru vēlaties izdzēst (obligāts). Šis ir vienīgais komandai nepieciešamais arguments.

#### Piemērs
```bash
dignacli delete-user jdoe
```
  
Šīs komandas izpilde noņems lietotāju `jdoe` no ***digna*** sistēmas, atņemot piekļuvi un dzēšot saistītos datus un atļaujas no repozitorija.

### modify-user

Komanda `modify-user` ***digna*** CLI tiek izmantota, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

#### Komandas izmantošana
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotājam, kuru vēlaties modificēt (obligāts).
- **USER_FULL_NAME**: Jaunais pilnais vārds lietotājam (obligāts).
  
#### Opcijas  
  
- `--is_superuser`, `-su`: Iestata lietotāju par superuser, piešķirot paaugstinātas privilēģijas. Šim pārslēdzim nav nepieciešama vērtība.  
- `--valid_until`, `-vu`: Nosaka lietotāja konta derīguma datumu formātā YYYY-MM-DD HH:MI:SS. Ja nav norādīts, konts paliek derīgs uz nenoteiktu laiku.  
  
#### Piemērs
  
Lai mainītu lietotāja `jdoe` pilno vārdu uz “Johnathan Doe” un iestatītu lietotāju kā superuser:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Komanda `modify-user-pwd` ***digna*** CLI tiek izmantota, lai nomainītu paroles esošam lietotājam ***digna*** sistēmā.
  
#### Komandas izmantošana
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotājam, kura paroli vēlaties mainīt (obligāts).
- **USER_PWD**: Jaunā parole lietotājam (obligāts).
  
#### Piemērs
  
Lai mainītu lietotāja `jdoe` paroli uz `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Komanda `list-users` ***digna*** CLI attēlo visu reģistrēto lietotāju sarakstu ***digna*** sistēmā.

#### Komandas izmantošana

```bash
dignacli list-users
```

Izpildot šo komandu, ***digna*** CLI pieslēgsies ***digna*** repozitorijam un uzrādīs visus lietotājus, rādīdams to ID, lietotājvārdu, pilno vārdu, superuser statusu un derīguma laikspiedolus.

## Repozitorija pārvaldība

### upgrade-repo
  
Komanda `upgrade-repo` ***digna*** CLI tiek izmantota, lai atjauninātu vai inicializētu ***digna*** repozitoriju. Šī komanda ir būtiska, lai piemērotu atjauninājumus vai iestatītu repozitorija infrastruktūru pirmo reizi.
  
#### Komandas izmantošana

```bash
dignacli upgrade-repo [options]
```
  
#### Opcijas
  
- `--simulation-mode`, `-s`: Ja iespējots, šī opcija palaidīs komandu simulācijas režīmā, izdrukājot SQL vaicājumus, kuri tiktu izpildīti, bet tos faktiski neizpildot. Tas ir noderīgi, lai priekšskatītu izmaiņas bez to piemērošanas repozitorijam.  

  
#### Piemērs
  
Lai atjauninātu ***digna*** repozitoriju, var palaist komandu bez opcijām:
  
```bash
dignacli upgrade-repo
```  
Lai palaistu atjauninājumu simulācijas režīmā (lai redzētu SQL vaicājumus, bez piemērošanas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Šī komanda ir būtiska ***digna*** sistēmas uzturēšanai, nodrošinot, ka datubāzes shēma un citi repozitorija komponenti ir atjaunināti uz programmatūras jaunāko versiju.

### encrypt
  
Komanda `encrypt` ***digna*** CLI tiek izmantota paroles šifrēšanai.
  
#### Komandas izmantošana
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Parole, kuru nepieciešams šifrēt (obligāts).
  
#### Piemērs
  
Lai šifrētu paroli, jānorāda parole kā arguments.  
Piemēram, lai šifrētu paroli `mypassword123`, izmantojiet:
```bash
dignacli encrypt mypassword123
```
Šī komanda izvadīs norādītās paroles šifrēto versiju, kuru pēc tam var izmantot drošos kontekstos. Ja paroles arguments netiks norādīts, CLI parādīs kļūdu, norādot trūkstošo argumentu.

### generate-key
  
Komanda `generate-key` tiek izmantota, lai ģenerētu Fernet atslēgu, kas nepieciešama parolēm, kas tiek glabātas ***digna*** repozitorijā, nodrošināšanai.
  
#### Komandas izmantošana
```bash
dignacli generate-key
```
  
## Datu pārvaldība

### clean-up

Komanda `clean-up` ***digna*** CLI tiek izmantota, lai noņemtu profilus, prognozes un satiksmes gaismas (traffic light) sistēmas datus vienam vai vairākiem datu avotiem norādītajā projektā. Šī komanda ir svarīga datu dzīves cikla pārvaldībai, palīdzot uzturēt sakārtotu un efektīvu datu vidi, iztīrot novecojušos vai nevajadzīgos datus.

#### Komandas izmantošana

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, no kura tiks noņemti dati (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** izies cauri visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Datumu un laiku, no kura sāksies datu noņemšana. Pieņemamie formāti ietver %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Datumu un laiku, līdz kuram tiks noņemti dati, sekojot tam pašam formātu sarakstam kā FROM_DATE (obligāts).
  
#### Opcijas
  
- `--table-name`, `-tn`: Ierobežo clean-up operāciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrs, kas ierobežo clean-up uz tabulām, kuru nosaukumos ir norādītā apakšvirkne.
- `--timing`, `-tm`: Parāda clean-up procesa laika ilgumu pēc tā pabeigšanas.
- `--help`: Parāda palīdzību par clean-up komandu un iziet.
  
#### Piemērs
  
Lai noņemtu datus no projekta ProjectA no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Lai noņemtu datus tikai no konkrētas tabulas ar nosaukumu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Šī komanda palīdz pārvaldīt datu krātuvi un nodrošina, ka repozitorijs satur tikai attiecīgo informāciju.

### remove-orphans
  
Komanda `remove-orphans` ***digna*** CLI tiek izmantota, lai veiktu repozitorija iekšējo sakopšanu.  
Kad lietotājs izdzēš projektus vai datu avotus, profili un prognozes bieži paliek repozitorijā. Ar šo komandu šādas pamestās rindas tiks noņemtas no repozitorija.
  
#### Komandas izmantošana
  
```bash
dignacli list-projects
```

### list-projects
  
Komanda `list-projects` ***digna*** CLI tiek izmantota, lai parādītu visu pieejamo projektu sarakstu ***digna*** sistēmā.
  
#### Komandas izmantošana
  
```bash
dignacli list-projects
```

Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kas pārvalda vairākus projektus, nodrošinot ātru pārskatu par pieejamajiem projektiem ***digna*** repozitorijā.

### list-ds

Komanda `list-ds` ***digna*** CLI tiek izmantota, lai parādītu visu pieejamo datu avotu sarakstu norādītajā projektā. Šī komanda noder, lai saprastu, kādi datu resursi ir pieejami analīzei un pārvaldībai ***digna*** sistēmā.

#### Komandas izmantošana
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, kura datu avoti tiek uzskaitīti (obligāts).
  
#### Piemērs
  
Lai uzskaitītu visus datu avotus projektā ar nosaukumu `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
Šī komanda sniedz lietotājiem pārskatu par projekta datu avotiem, palīdzot efektīvāk orientēties un pārvaldīt datu ainavu.


### inspect

Komanda `inspect` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un satiksmes gaismas sistēmas datus vienam vai vairākiem datu avotiem norādītajā projektā. Šī komanda palīdz analizēt un uzraudzīt datus norādītajā laika periodā. Pēc inspekcijas pabeigšanas tiek atgriezta aprēķinātās satiksmes gaismas sistēmas vērtība:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komandas izmantošana

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus vēlaties pārbaudīt (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** izies cauri visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Inspekcijas sākuma datums un laiks. Pieņemamie formāti ietver %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Inspekcijas beigu datums un laiks, sekojot tam pašam formātu sarakstam kā FROM_DATE (obligāts).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrs, lai inspektētu tikai tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--enable_notification`, `-en`: Ieslēdz paziņojumu nosūtīšanu brīdinājumu gadījumā.
- `--bypass-backend`, `-bb`: Apiet backend un palaist inspekciju tieši no CLI (tikai testēšanas nolūkos!).

  
#### Piemērs
  
Lai pārbaudītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Lai pārbaudītu tikai konkrētu tabulu un piespiestu prognožu pārrēķināšanu:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Šī komanda noder, lai ģenerētu atjauninātus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu brīdinājumu sistēmas norādītajā projekta laika logā.

### inspect-async

Komanda `inspect-async` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un satiksmes gaismas sistēmas datus vienam vai vairākiem datu avotiem norādītajā projektā. Šī komanda palīdz analizēt un uzraudzīt datus norādītajā laika periodā. Atšķirībā no sinhronās komandas `inspect`, šī komanda negaida inspekcijas pabeigšanu.
Tā vietā tā atgriež pieprasījuma ID iesniegtajam inspekcijas pieprasījumam. Lai pārbaudītu inspekcijas procesa gaitu, izmantojiet komandu `inspect-status`.

#### Komandas izmantošana

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus vēlaties pārbaudīt (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** izies cauri visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Inspekcijas sākuma datums un laiks. Pieņemamie formāti ietver %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Inspekcijas beigu datums un laiks, sekojot tam pašam formātu sarakstam kā FROM_DATE (obligāts).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrs, lai inspektētu tikai tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- `--enable_notification`, `-en`: Ieslēdz paziņojumu nosūtīšanu brīdinājumu gadījumā.

  
#### Piemērs
  
Lai asinhroni pārbaudītu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Komanda `inspect-status` ***digna*** CLI tiek izmantota, lai pārbaudītu asinhronās inspekcijas gaitu, izmantojot pieprasījuma ID.

#### Komandas izmantošana

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenti
  
- **REQUEST_ID**: Pieprasījuma ID, ko atgrieza komanda `inspect-async`.
  
#### Piemērs
  
Lai pārbaudītu inspekcijas gaitu ar pieprasījuma ID 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Komanda `inspect-cancel` ***digna*** CLI tiek izmantota, lai atceltu inspekcijas pēc pieprasījuma ID vai atceltu visus pašreizējos pieprasījumus.

#### Komandas izmantošana

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenti
  
- **REQUEST_ID**: Pieprasījuma ID, ko atgrieza komanda `inspect-async`.
  
#### Piemērs
  
Lai atceltu inspekciju ar pieprasījuma ID 12345:
  
```bash
dignacli inspect-cancel 12345
```

Lai atceltu visus pašlaik darbojošos vai gaidāmos pieprasījumus:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Komanda `export-ds` ***digna*** CLI tiek izmantota, lai izveidotu datu avotu eksportu no ***digna*** repozitorija. Pēc noklusējuma tiks eksportēti visi datu avoti no norādītā projekta.

#### Komandas izmantošana
  
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

Komanda `import-ds` ***digna*** CLI tiek izmantota, lai importētu datu avotus mērķa projektā un izveidotu importēšanas atskaiti.

#### Komandas izmantošana
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru tiks importēti datu avoti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kuru importēt.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importēšanas atskaiti (ja nav norādīts, izvada terminālā tabulas formā).
- `--output-format`, `-f`: Formāts, kādā saglabāt importēšanas atskaiti (json, csv).
    
#### Piemērs
  
Lai importētu visus datu avotus no eksporta faila `my_export.json` uz `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pēc importēšanas šī komanda arī parādīs atskaiti par importētajiem un izlaistajiem objektiem. Tiks importēti tikai jauni datu avoti uz `ProjectB`. Lai uzzinātu, kuri objekti tiktu importēti un kuri izlaisti, varat izmantot komandu `plan-import-ds`.

### plan-import-ds

Komanda `plan-import-ds` ***digna*** CLI tiek izmantota, lai analizētu datu avotu eksporta saturu pirms tā importēšanas mērķa projektā un izveidotu importēšanas plānu.

#### Komandas izmantošana
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru eksports tiktu importēts.
- **EXPORT_FILE**: Eksporta faila nosaukums, kura saturs tiks analizēts pirms importa.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importēšanas atskaiti (ja nav norādīts, izvada terminālā tabulas formā).
- `--output-format`, `-f`: Formāts, kādā saglabāt importēšanas atskaiti (json, csv).
    
#### Piemērs
  
Lai pārbaudītu, kuri datu avoti tiktu importēti un kuri izlaisti no eksporta faila `my_export.json`, importējot uz `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Šī komanda tikai parādīs objektu importēšanas un izlaistīšanas plānu.