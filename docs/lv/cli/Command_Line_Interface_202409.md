---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI atsauce 2024.09
**2024-08-24**

---

## CLI pamati

---

###   help

Opcija --help sniedz informāciju par pieejamajām komandām un to lietošanu. Ir divi galvenie veidi, kā izmantot šo opciju:

1. **Vispārīgas palīdzības rādīšana:**
   
    Izmantojiet --help uzreiz pēc atslēgvārda ***dignacli***  
   bash
   dignacli --help

3.  **Palīdzība konkrētām komandām:**  
  
    Lai iegūtu detalizētu informāciju par konkrētu komandu, pievienojiet tai --help.
    Piemēram, lai saņemtu palīdzību par komandu add-user, izpildiet:
     bash
     dignacli add-user --help
     

     ### izvade:
      
     - **Komandas apraksts:** Sniedz detalizētu aprakstu par to, ko komanda dara.  
     - **Sintakse:** Rāda precīzu sintaksi, ieskaitot obligātos un izvēles argumentus.  
     - **Opcijas:** Uzskaita komandas specifiskās opcijas ar to skaidrojumiem.  
     - **Piemēri:** Sniedz piemērus, kā efektīvi izpildīt komandu.

  
###   check-repo-connection

check-repo-connection komanda ir utilīta ***dignacli*** rīkā, kas paredzēta, lai pārbaudītu savienojamību un piekļuvi norādītajam ***digna*** repository. Šī komanda nodrošina, ka CLI var sazināties ar repository.
      
##### Komandas lietošana
bash
dignacli check-repo-connection


Pēc veiksmīgas izpildes komanda izvada savienojuma apstiprinājumu, kā arī informāciju par repository: Repository versiju, Host, Database un Schema.  
  
Ja savienojums ar repository neizdodas, pārbaudiet config.toml failu, vai konfigurācijas iestatījumi ir pareizi.

###   version

Lai pārbaudītu instalēto *dignacli* versiju, izmantojiet opciju --version.  
  
#### Komandas lietošana
bash
dignacli --version

  
#### Piemēra izvade
bash
dignacli version 2024.09


###   žurnālu opcijas
  
Pēc noklusējuma konsoles izvade no ***digna*** komandām ir veidota minimālistiska. Lielākā daļa komandu piedāvā iespēju sniegt papildus informāciju, izmantojot šādas opcijas:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
“verbose” un “debug” nosaka detaļu līmeni, savukārt pārslēgs “logfile” ļauj pāradresēt izvadi uz failu, nevis konsoles logu.

## Lietotāju pārvaldība

###   add-user
  
add-user komanda ***dignacli*** CLI tiek izmantota, lai pievienotu jaunu lietotāju ***digna*** sistēmai.
  
#### Komandas lietošana
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Argumenti

- **USER_NAME**: Jaunā lietotāja lietotājvārds (obligāts).
- **USER_FULL_NAME**: Jaunā lietotāja pilnais vārds (obligāts).
- **USER_PASSWORD**: Jaunā lietotāja parole (obligāts).

#### Opcijas

- --is_superuser, -su: Karogs, lai piešķirtu jaunajam lietotājam administratīvās tiesības.
- --valid_until, -vu: Uzstāda konta derīguma termiņu formātā YYYY-MM-DD HH:MI:SS. Ja netiek norādīts, kontam nav derīguma termiņa.

#### Piemērs

Lai pievienotu jaunu lietotāju ar lietotājvārdu jdoe, pilno vārdu John Doe un paroli password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Lai pievienotu jaunu lietotāju un uzstādītu konta derīguma datumu:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
delete-user komanda ***dignacli*** CLI tiek izmantota, lai noņemtu esošu lietotāju no ***digna*** sistēmas.
  
##### Komandas lietošana
bash
dignacli delete-user USER_NAME

  
#### Argumenti
- **USER_NAME**: Lietotājvārds lietotājam, kuru nepieciešams izdzēst (obligāts). Tas ir vienīgais komandas arguments.

#### Piemērs
bash
dignacli delete-user jdoe

  
Izpildot šo komandu, lietotājs jdoe tiks noņemts no ***digna*** sistēmas, tiks atsauktas viņa piekļuves tiesības un izdzēsti saistītie dati un atļaujas no repository.

###   modify-user

modify-user komanda ***dignacli*** CLI tiek izmantota, lai atjauninātu esoša lietotāja datus ***digna*** sistēmā.

##### Komandas lietošana
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotājam, kuru nepieciešams modificēt (obligāts).
- **USER_FULL_NAME**: Lietotāja jaunais pilnais vārds (obligāts).
  
#### Opcijas  
  
- --is_superuser, -su: Uzstāda lietotāju kā superuser, piešķirot paaugstinātas privilēģijas. Šim karogam nav nepieciešama vērtība.  
- --valid_until, -vu: Uzstāda konta derīguma datumu formātā YYYY-MM-DD HH:MI:SS. Ja netiek norādīts, konts paliek derīgs beztermiņa.  
  
#### Piemērs
  
Lai mainītu lietotāja jdoe pilno vārdu uz “Johnathan Doe” un piešķirtu lietotājam superuser tiesības:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
modify-user-pwd komanda ***dignacli*** CLI tiek izmantota, lai nomainītu paroles esošam lietotājam ***digna*** sistēmā.
  
##### Komandas lietošana
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Argumenti
  
- **USER_NAME**: Lietotājvārds lietotājam, kura paroli nepieciešams mainīt (obligāts).
- **USER_PWD**: Lietotāja jaunā parole (obligāts).
  
#### Piemērs
  
Lai nomainītu lietotāja jdoe paroli uz newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

list-users komanda ***dignacli*** CLI attēlo visu reģistrēto lietotāju sarakstu ***digna*** sistēmā.

##### Komandas lietošana

bash
dignacli list-users


Izpildot šo komandu ***dignacli*** savienosies ar ***digna*** repository un uzskaitīs visus lietotājus, parādot to ID, lietotājvārdu, pilno vārdu, superuser statusu un derīguma laika zīmogus.

# Repository pārvaldība

###   upgrade-repo
  
upgrade-repo komanda ***dignacli*** CLI tiek izmantota, lai atjauninātu vai inicializētu ***digna*** repository. Šī komanda ir būtiska, lai piemērotu atjauninājumus vai uzstādītu repository infrastruktūru pirmo reizi.
  
#### Komandas lietošana

bash
dignacli upgrade-repo [options]

  
#### Opcijas
  
- --simulation-mode, -s: Ja iespējota, šī opcija izpilda komandu simulatīvā režīmā, izdrukājot SQL vaicājumus, kas tiktu izpildīti, bet tos patiesībā neizpilda. Tas ir noderīgi, lai priekšskatītu izmaiņas, neveicot izmaiņas repository.  

  
#### Piemērs
  
Lai atjauninātu ***digna*** repository, komandu var izpildīt bez opcijām:
  
bash
dignacli upgrade-repo
  
Lai palaistu atjaunināšanu simulatīvā režīmā (lai redzētu SQL vaicājumus, tos nepiemērojot):
  
bash
dignacli upgrade-repo --simulation-mode

  
Šī komanda ir svarīga ***digna*** sistēmas uzturēšanai, nodrošinot, ka datubāzes shēma un citi repository komponenti ir saskaņā ar programmatūras jaunāko versiju.

###   encrypt
  
encrypt komanda ***dignacli*** CLI tiek izmantota paroles šifrēšanai.
  
#### Komandas lietošana
  
bash
dignacli encrypt <PASSWORD>

    
#### Argumenti
- **PASSWORD**: Parole, kuru nepieciešams šifrēt (obligāts).
  
#### Piemērs
  
Lai šifrētu paroli, jānorāda parole kā arguments.   
Piemēram, lai šifrētu paroli mypassword123, izmantojiet:
bash
dignacli encrypt mypassword123

Šī komanda izvadīs norādītās paroles šifrēto versiju, ko pēc tam var izmantot drošos kontekstos. Ja paroles arguments netiek norādīts, CLI parādīs kļūdu par trūkstošu argumentu.

###   generate-key
  
generate-key komanda tiek izmantota, lai ģenerētu Fernet atslēgu, kas ir būtiska paroļu drošināšanai, kas glabājas ***digna*** repository.
  
#### Komandas lietošana
bash
dignacli generate-key

  
## Datu pārvaldība

###   clean-up

clean-up komanda ***dignacli*** CLI tiek izmantota, lai noņemtu profilus, prognozes un Traffic Light System datus vienam vai vairākām datu avotu tabulām noteiktā projektā. Šī komanda ir svarīga datu dzīves cikla pārvaldībai, palīdzot uzturēt organizētu un efektīvu datu vidi, iztīrot novecojušus vai liekus datus.

#### Komandas lietošana

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, no kura dati jānoņem (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** iterēs pār visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Datu noņemšanas sākuma datums un laiks. Pieņemamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Datu noņemšanas beigu datums un laiks, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas
  
- --table-name, -tn: Ierobežo tīrīšanas darbību uz konkrētu tabulu projektā.
- --table-filter, -tf: Filtrs, kas ierobežo tīrīšanu tikai tabulām, kuru nosaukumos ir norādītais apakšvirknes fragments.
- --timing, -tm: Parāda tīrīšanas procesa laika ilgumu pēc pabeigšanas.
- --help: Rāda palīdzību par clean-up komandu un iziet.
  
#### Piemērs
  
Lai noņemtu datus no projekta ProjectA no 2023. gada 1. janvāra līdz 2023. gada 30. jūnijam:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Lai noņemtu datus tikai no konkrētas tabulas Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Šī komanda palīdz pārvaldīt datu glabāšanu un nodrošināt, ka repository satur tikai aktuālu informāciju.

###   inspect

inspect komanda ***dignacli*** CLI tiek izmantota, lai izveidotu profilus, prognozes un Traffic Light System datus vienam vai vairākām datu avotu tabulām noteiktā projektā. Šī komanda palīdz analizēt un monitorēt datus noteiktā periodā.

#### Komandas lietošana

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kuram dati jāinspektē (obligāts). Izmantojot atslēgvārdu all-projects šajā argumentā, ***digna*** iterēs pār visiem esošajiem projektiem un piemēros šo komandu.
- **FROM_DATE**: Inspekcijas sākuma datums un laiks. Pieņemamie formāti ir %Y-%m-%d, %Y-%m-%dT%H:%M:%S vai %Y-%m-%d %H:%M:%S (obligāts).
- **TO_DATE**: Inspekcijas beigu datums un laiks, sekojot tiem pašiem formātiem kā FROM_DATE (obligāts).
  
#### Opcijas

- --table-name, -tn: Ierobežo inspekciju uz konkrētu tabulu projektā.
- --table-filter, -tf: Filtrs, lai inspektētu tikai tās tabulas, kuru nosaukumos ir norādītā apakšvirkne.
- --force-profile: Piespiež profilu pārvācēšanu. Noklusējums ir force-profile.
- --no-force-profile: Novērš profilu pārvākšanu.
- --force-prediction: Piespiež prognožu pārrēķināšanu. Noklusējums ir force-prediction.
- --no-force-prediction: Novērš prognožu pārrēķināšanu.
- --force-alert-status: Piespiež brīdinājumu statusu pārrēķināšanu. Noklusējums ir force-alert-status.
- --no-force-alert-status: Novērš brīdinājumu statusu pārrēķināšanu.
- --timing, -tm: Parāda inspekcijas procesa ilgumu pēc pabeigšanas.
- --alert-notification, -an: Sūta brīdinājumu paziņojumus uz abonētajiem kanāliem.
  
#### Piemērs
  
Lai izinspektētu datus projektam ProjectA no 2024. gada 1. janvāra līdz 2024. gada 31. janvārim:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Lai inspektētu tikai konkrētu tabulu un piespiestu prognožu pārrēķināšanu:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Šī komanda ir noderīga, lai ģenerētu atjaunotus profilus un prognozes, uzraudzītu datu integritāti un pārvaldītu brīdinājumu sistēmas noteiktā projekta laika intervalā.

###   tls-status

tls-status komanda ***dignacli*** CLI tiek izmantota, lai vaicātu Traffic Light System (TLS) statusu konkrētai tabulai projektā attiecīgajā datumā. Traffic Light System sniedz ieskatu par datu veselību un kvalitāti, norādot iespējamās problēmas vai brīdinājumus, kam jāpievērš uzmanība.
  
#### Komandas lietošana
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Argumenti
  
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek vaicāts TLS statuss (obligāts).
- **TABLE_NAME**: Konkrētā tabula projektā, kurai nepieciešams TLS statuss (obligāts).
- **DATE**: Datums, kuram tiek vaicāts TLS statuss, parasti formātā %Y-%m-%d (obligāts).
  
#### Piemērs
  
Lai pārbaudītu TLS statusu tabulai UserData projektā ProjectA uz 2024. gada 1. jūliju:

bash
dignacli tls-status ProjectA UserData 2024-07-01


Šī komanda palīdz lietotājiem uzraudzīt un uzturēt datu kvalitāti, nodrošinot skaidru un rīcībspējīgu statusa atskaiti, balstoties uz iepriekš definētiem kritērijiem.

###   list-projects
  
list-projects komanda ***dignacli*** CLI tiek izmantota, lai attēlotu visu pieejamo projektu sarakstu ***digna*** sistēmā.
  
#### Komandas lietošana
  
bash
dignacli list-projects


Šī komanda ir īpaši noderīga administratoriem un lietotājiem, kuri pārvalda vairākus projektus, sniedzot ātru pārskatu par pieejamajiem projektiem ***digna*** repository.

###   list-ds

list-ds komanda ***dignacli*** CLI tiek izmantota, lai attēlotu visu pieejamo datu avotu sarakstu noteiktā projektā. Šī komanda ir noderīga, lai saprastu datu resursus, kas pieejami analīzei un pārvaldībai ***digna*** sistēmā.

#### Komandas lietošana
  
bash
dignacli list-ds <PROJECT_NAME>


#### Argumenti
- **PROJECT_NAME**: Projekta nosaukums, kuram tiek uzskaitīti datu avoti (obligāts).
  
#### Piemērs
  
Lai uzskaitītu visus datu avotus projektā ProjectA:
  
bash
dignacli list-ds ProjectA

  
Šī komanda sniedz lietotājiem pārskatu par projektā pieejamajiem datu avotiem, palīdzot efektīvāk orientēties un pārvaldīt datu ainavu.