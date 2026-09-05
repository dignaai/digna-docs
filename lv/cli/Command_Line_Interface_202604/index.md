# digna CLI Reference 2026.04
**2026-04-08**

Šī lapa dokumentē pilnu komandu kopu, kas pieejama ***digna*** CLI laidienā **2026.04**, ieskaitot izmantošanas piemērus un opcijas.

---

## CLI pamati

---

### help
Opcija `--help` sniedz informāciju par pieejamajām komandām un to izmantošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārīgās palīdzības attēlošana:**
   
   Izmantojiet `--help` uzreiz pēc atslēgvārda ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Palīdzība konkrētām komandām:**  
  
   Lai iegūtu detalizētu informāciju par konkrētu komandu, pievienojiet `--help` tai komandai.
   Piemēram, lai iegūtu palīdzību par komandu `add-user`, palaidiet:
   ```bash
   dignacli add-user --help
   ```

   ### izvade:
      
   - **Komandas apraksts:** Piedāvā detalizētu aprakstu par to, ko komanda veic.  
   - **Sintakse:** Rāda precīzu sintaksi, ieskaitot obligātos un izvēles argumentus.  
   - **Opcijas:** Uzskaita komandas specifiskās opcijas ar to skaidrojumiem.  
   - **Piemēri:** Sniedz piemērus, kā komandu efektīvi izpildīt.

### check-config

Komanda `check-config` ir rīks ***digna*** CLI rīkā, kas paredzēts, lai pārbaudītu ***digna*** konfigurāciju. Šī komanda nodrošina, ka ***digna*** komponenti spēj atrast nepieciešamās konfigurācijas vienības config.toml.

#### Opcijas

- `--configpath`, `-cp`: Fails vai direktorijs, kas satur konfigurāciju. Ja nav norādīts, tiks izmantots ../config.toml.
      
#### Komandas izmantošana
```bash
dignacli check-config
```

Veiksmīgas izpildes gadījumā komanda izvada apstiprinājumu par konfigurācijas pilnību.  
  
Ja konfigurācija šķiet nepilnīga, tiks uzskaitītas trūkstošās konfigurācijas vienības.

  
### check-repo-connection

Komanda `check-repo-connection` ir rīks ***digna*** CLI rīkā, kas paredzēts, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repozitorijam. Šī komanda nodrošina, ka CLI spēj mijiedarboties ar repozitoriju.
      
#### Komandas izmantošana
```bash
dignacli check-repo-connection
```

Veiksmīgas izpildes gadījumā komanda izvada apstiprinājumu par savienojumu, kā arī detaļas par repozitoriju: repozitorija versiju, hostu, datubāzi un shēmu.  
  
Ja repozitorija savienojums nav veiksmīgs, pārbaudiet config.toml failu, vai konfigurācijas iestatījumi ir pareizi.

### version

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju `--version`.  
  
#### Komandas izmantošana
```bash
dignacli --version
```
  
#### Piemēra izvade
```bash
dignacli version 2026.04
```

### žurnālošanas opcijas
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir izstrādāta minimālistiska. Lielākajai daļai komandu ir iespēja sniegt papildus informāciju, izmantojot sekojošas opcijas:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” un “debug” nosaka detaļu līmeni, savukārt “logfile” pārslēgs ļauj pārsūtīt izvadi uz failu, nevis konsoles logu.

## Lietotāju pārvaldība

### add-user
  
Komanda `add-user` ***digna*** CLI tiek izmantota, lai pievienotu jaunu lietotāju ***digna*** sistēmai.
  
#### Komandas izmantošana
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenti

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāts).
- **USER_FULL_NAME**: Jaunā lietotāja pilns vārds (obligāts).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāta).

#### Opcijas

- `--is_superuser`, `-su`: Slēdzis, lai apzīmētu jauno lietotāju kā administratoru.
- `--valid_until`, `-vu`: Uzstāda konta derīguma termiņu formātā `YYYY-MM-DD HH:MI:SS`. Ja netiek uzstādīts, kontam nav derīguma termiņa.

#### Piemērs

Lai pievienotu jaunu lietotāju ar lietotājvārdu `jdoe`, pilnu vārdu `John Doe` un paroli `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Lai pievienotu jaunu lietotāju un uzstādītu konta beigu datumu:
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
- **USER_NAME**: Lietotājvārds lietotājam, kas jāizdzēš (obligāts). Tas ir vienīgais komandas prasītais arguments.

#### Piemērs
```bash
dignacli delete-user jdoe
```
  
Šīs komandas izpilde noņems lietotāju `jdoe` no ***digna*** sistēmas, anulējot viņa piekļuvi un dzēšot saistītos datus un atļaujas no repozitorija.

### modify-user

Komanda `modify-user` ***digna*** CLI tiek izmantota, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

#### Komandas izmantošana
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotājam, kuru jāmaina (obligāts).
- **USER_FULL_NAME**: Jaunais pilnais vārds lietotājam (obligāts).
  
#### Opcijas  
  
- `--is_superuser`, `-su`: Uzstāda lietotāju kā superlietotāju, piešķirot paaugstinātas tiesības. Šim slēdzim nav nepieciešama vērtība.  
- `--valid_until`, `-vu`: Uzstāda konta derīguma termiņu formātā YYYY-MM-DD HH:MI:SS. Ja netiek sniegts, konts paliek derīgs bez ierobežojuma.  
  
#### Piemērs
  
Lai mainītu lietotāja `jdoe` pilnu vārdu uz “Johnathan Doe” un uzstādītu lietotāju kā superlietotāju:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Komanda `modify-user-pwd` ***digna*** CLI tiek izmantota, lai mainītu esoša lietotāja paroli ***digna*** sistēmā.
  
#### Komandas izmantošana
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotājam, kura parole jāmaina (obligāts).
- **USER_PWD**: Jaunā parole lietotājam (obligāta).
  
#### Piemērs
  
Lai nomainītu lietotāja `jdoe` paroli uz `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Komanda `list-users` ***digna*** CLI parāda sarakstu ar visiem lietotājiem, kas reģistrēti ***digna*** sistēmā.

#### Komandas izmantošana

```bash
dignacli list-users
```

Šīs komandas izpilde ***digna*** CLI pieslēgsies ***digna*** repozitorijam un uzskaitīs visus lietotājus, rādīsot to ID, lietotājvārdus, pilnos vārdus, superlietotāja statusu un derīguma laika zīmogu.

## Repozitorija pārvaldība

### upgrade-repo
  
Komanda `upgrade-repo` ***digna*** CLI tiek izmantota, lai atjauninātu vai inicializētu ***digna*** repozitoriju. Šī komanda ir būtiska, lai pielietotu atjauninājumus vai pirmo reizi izveidotu repozitorija infrastruktūru.
  
#### Komandas izmantošana

```bash
dignacli upgrade-repo [options]
```
  
#### Opcijas
  
- `--simulation-mode`, `-s`: Ja ieslēgts, šī opcija palaidīs komandu simulācijas režīmā, kas izdrukā SQL vaicājumus, kas tiktu izpildīti, bet tos neizpilda. Tas noder, lai priekšskatītu izmaiņas, neveicot reālas modifikācijas repozitorijā.  

  
#### Piemērs
  
Lai atjauninātu ***digna*** repozitoriju, var palaist komandu bez papildus opcijām:
  
```bash
dignacli upgrade-repo
```  
Lai palaistu atjaunināšanu simulācijas režīmā (skatīt SQL vaicājumus bez to pielietošanas):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Šī komanda ir svarīga ***digna*** sistēmas uzturēšanai, nodrošinot, ka datubāzes shēma un citi repozitorija komponenti ir saskaņā ar programmatūras jaunāko versiju.

### encrypt
  
Komanda `encrypt` ***digna*** CLI tiek izmantota, lai šifrētu paroli.
  
#### Komandas izmantošana
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenti
- **PASSWORD**: Parole, kas jāšifrē (obligāta).
  
#### Piemērs
  
Lai šifrētu paroli, nepieciešams norādīt paroli kā argumentu.  
Piemēram, lai šifrētu paroli `mypassword123`, izmantojiet:
```bash
dignacli encrypt mypassword123
```
Šī komanda izvada norādītās paroles šifrēto versiju, kuru pēc tam var izmantot drošos kontekstos. Ja paroles arguments nav norādīts, CLI parādīs kļūdu, norādot uz trūkstošo argumentu.

### generate-key
  
Komanda `generate-key` tiek izmantota Fernet atslēgas ģenerēšanai, kas ir nepieciešama, lai nodrošinātu paroles, kas tiek glabātas ***digna*** repozitorijā.
  
#### Komandas izmantošana
```bash
dignacli generate-key
```
  
## Datu pārvaldība

### clean-up

Komanda `clean-up` ***digna*** CLI tiek izmantota, lai noņemtu profilus, prognozes un datus no trafikgaismas sistēmas vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda ir būtiska datu dzīves cikla pārvaldībai, palīdzot uzturēt sakārtotu un efektīvu datu vidi, dzēšot novecojusīsu vai nevajadzīgu informāciju.

#### Komandas izmantošana

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, no kura dati jānoņem (obligāts). Izmantojot atslēgvārdu `all-projects` šajā argumentā, ***digna*** iziet cauri visiem esošajiem projektiem un piemēro komandu.
- **FROM_DATE**: Sākuma datums un laiks datu noņemšanai. Pieņemamie formāti ietver %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Beigu datums un laiks datu noņemšanai, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas
  
- `--table-name`, `-tn`: Ierobežo `clean-up` darbību uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrē, lai tīrīšana attiektos tikai uz tabulām, kuru nosaukumos ir norādītais apakšvirkne.
- `--timing`, `-tm`: Parāda `clean-up` procesa ilgumu pēc tā pabeigšanas.
- `--help`: Parāda palīdzību par `clean-up` komandu un iziet.
  
#### Piemērs
  
Lai noņemtu datus no projekta ProjectA no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Lai noņemtu datus tikai no konkrētas tabulas ar nosaukumu `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Šī komanda palīdz pārvaldīt datu krātuvi un nodrošināt, ka repozitorijā glabājas tikai relevanta informācija.

### remove-orphans
  
Komanda `remove-orphans` ***digna*** CLI tiek izmantota repozitorija uzturēšanai.  
Kad lietotājs izdzēš projektus vai datu avotus, profili un prognozes paliek repozitorijā. Ar šo komandu šādas “bēdīgas” (orphan) rindas tiks noņemtas no repozitorija.
  
#### Komandas izmantošana
  
```bash
dignacli list-projects
```

### list-projects
  
Komanda `list-projects` ***digna*** CLI tiek izmantota, lai parādītu sarakstu ar visiem pieejamiem projektiem ***digna*** sistēmā.
  
#### Komandas izmantošana
  
```bash
dignacli list-projects
```

Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kas pārvalda vairākus projektus, sniedzot ātru pārskatu par pieejamajiem projektiem ***digna*** repozitorijā.

### list-ds

Komanda `list-ds` ***digna*** CLI tiek izmantota, lai parādītu sarakstu ar visiem pieejamiem datu avotiem norādītā projektā. Šī komanda noder, lai saprastu pieejamos datu resursus analīzei un pārvaldībai ***digna*** sistēmā.

#### Komandas izmantošana
  
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
  
Šī komanda sniedz pārskatu par datu avotiem projektā, palīdzot efektīvāk orientēties un pārvaldīt datu ainavu.


### inspect

Komanda `inspect` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un datus trafikgaismas sistēmai vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda palīdz analizēt un uzraudzīt datus noteiktā periodā. Pēc inspekcijas pabeigšanas tiek atgriezta aprēķinātās trafikgaismas sistēmas vērtība:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Komandas izmantošana

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus jāinspektē (obligāts). Izmantojot atslēgvārdu `all-projects` šajā argumentā, ***digna*** izies cauri visiem esošajiem projektiem un piemēros komandu.
- **FROM_DATE**: Sākuma datums un laiks datu inspekcijai. Pieņemamie formāti ietver %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Beigu datums un laiks datu inspekcijai, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrē, lai inspekcija attiektos tikai uz tabulām, kuru nosaukumos ir norādītais apakšvirkne.
- `--enable_notification`, `-en`: Ieslēdz paziņojumu sūtīšanu brīdinājumu gadījumā.
- `--bypass-backend`, `-bb`: Apiet backend un veic inspekciju tieši no CLI (tikai testēšanas nolūkos!).

  
#### Piemērs
  
Lai inspektētu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Lai inspektētu tikai konkrētu tabulu un piespiestu prognožu pārrēķināšanu:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Šī komanda noder, lai ģenerētu atjauninātus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu brīdinājumu sistēmas noteiktā projekta laika posmā.

### inspect-async

Komanda `inspect-async` ***digna*** CLI tiek izmantota, lai izveidotu profilus, prognozes un datus trafikgaismas sistēmai vienam vai vairākiem datu avotiem norādītā projektā. Šī komanda palīdz analizēt un uzraudzīt datus noteiktā periodā. Atšķirībā no sinhronās `inspect` komandas, šī negaida inspekcijas pabeigšanu.
Tā vietā tā atgriež pieprasījuma ID par iesniegto inspekcijas pieprasījumu. Lai vaicātu inspekcijas procesa gaitu, izmantojiet komandu `inspect-status`.

#### Komandas izmantošana

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kura datus jāinspektē (obligāts). Izmantojot atslēgvārdu `all-projects` šajā argumentā, ***digna*** izies cauri visiem esošajiem projektiem un piemēros komandu.
- **FROM_DATE**: Sākuma datums un laiks datu inspekcijai. Pieņemamie formāti ietver %Y-%m-%d, %Y-%m-%dT%H:%M:%S, vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Beigu datums un laiks datu inspekcijai, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas

- `--table-name`, `-tn`: Ierobežo inspekciju uz konkrētu tabulu projektā.
- `--table-filter`, `-tf`: Filtrē, lai inspekcija attiektos tikai uz tabulām, kuru nosaukumos ir norādītais apakšvirkne.
- `--enable_notification`, `-en`: Ieslēdz paziņojumu sūtīšanu brīdinājumu gadījumā.

  
#### Piemērs
  
Lai asinhroni inspektētu datus projektam `ProjectA` no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Komanda `inspect-status` ***digna*** CLI tiek izmantota, lai pārbaudītu asinhronās inspekcijas gaitu, pamatojoties uz pieprasījuma ID.

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

Komanda `inspect-cancel` ***digna*** CLI tiek izmantota, lai atceltu inspekcijas, pamatojoties uz pieprasījuma ID, vai arī lai atceltu visus pašreizējos pieprasījumus.

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

Lai atceltu visus pašlaik darbojošos vai gaidošos pieprasījumus:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Komanda `export-ds` ***digna*** CLI tiek izmantota, lai izveidotu datu avotu eksporta failu no ***digna*** repozitorija. Pēc noklusējuma tiks eksportēti visi datu avoti no norādītā projekta.

#### Komandas izmantošana
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, no kura tiks eksportēti datu avoti.

#### Opcijas

- `--table_name`, `-tn`: Eksportē konkrētu datu avotu no projekta.
- `--exportfile`, `-ef`: Norāda eksporta faila nosaukumu.
    
#### Piemērs
  
Lai eksportētu visus datu avotus no projekta `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
Šī komanda eksportē visus datu avotus no `ProjectA` kā JSON dokumentu, ko var importēt citā projektā vai ***digna*** repozitorijā.


### import-ds

Komanda `import-ds` ***digna*** CLI tiek izmantota, lai importētu datu avotus mērķprojektā un izveidotu importa atskaiti.

#### Komandas izmantošana
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru tiks importēti datu avoti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kas tiks importēts.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importa atskaiti (ja nav norādīts, izvada terminālī tabulārā formā).
- `--output-format`, `-f`: Formāts, kādā saglabāt importa atskaiti (json, csv).
    
#### Piemērs
  
Lai importētu visus datu avotus no eksporta faila `my_export.json` uz `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Pēc importa šī komanda parādīs arī atskaiti par importētajiem un izlaistajiem objektiem. Tiks importēti tikai jauni datu avoti `ProjectB`. Lai noskaidrotu, kuri objekti tiktu importēti un kuri izlaisti, var izmantot komandu `plan-import-ds`.

### plan-import-ds

Komanda `plan-import-ds` ***digna*** CLI tiek izmantota, lai sagatavotu importa plānu datu avotu importam mērķprojektā un izveidotu importa pārskatu bez reālas importa izpildes.

#### Komandas izmantošana
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, uz kuru datu avoti tiktu importēti.
- **EXPORT_FILE**: Eksporta faila nosaukums, kas tiks analizēts pirms importa.

#### Opcijas

- `--output-file`, `-o`: Fails, kur saglabāt importa atskaiti (ja nav norādīts, izvada terminālī tabulārā formā).
- `--output-format`, `-f`: Formāts, kādā saglabāt importa atskaiti (json, csv).
    
#### Piemērs
  
Lai pārbaudītu, kuri datu avoti tiktu importēti un kuri tiktu izlaisti no eksporta faila `my_export.json`, importējot uz `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Šī komanda tikai parādīs importa plānu par objektiem, kas tiktu importēti un izlaisti.