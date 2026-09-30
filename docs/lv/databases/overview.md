---
title: Datubāzu savienojumu pārskats — ODBC iestatīšana bez DSN | digna dokumentācija
description: Kā datubāzu savienojumi darbojas digna. Katra avota tehnoloģija tiek sasniegta caur ODBC ar savienojuma virkni bez DSN, kas veidota no ODBC rekvizītiem. Aptver draivera instalēšanu digna resursdatorā, ekrānu Add DB Connection, rekvizītu šifrēšanu, savienojuma testēšanu, problēmu novēršanu un saites uz katras tehnoloģijas ceļvedi.
image: /assets/logo_square.png
keywords:
  - digna datubāzes savienojums
  - ODBC bez DSN
  - ODBC savienojuma virkne
  - ODBC draivera iestatīšana
  - unixodbc
  - ODBC rekvizīti
  - datu avota konfigurācija
lang: en
robots: index, follow
og_title: digna Database Connections – DSN-less ODBC Setup
og_description: Configure a digna source connection over ODBC without a DSN. Driver installation, ODBC properties, encryption, testing and troubleshooting.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Datubāzu savienojumu pārskats

---

## Satura rādītājs

1. [Kā darbojas savienojumi](#how-connections-work)
2. [Tehnoloģiju ceļveži](#technology-guides)
3. [Priekšnosacījums: instalēt ODBC draiveri digna resursdatorā](#install-the-driver)
4. [Izveidot datubāzes savienojumu](#create-a-database-connection)
5. [ODBC rekvizīti](#odbc-properties)
6. [Rekvizītu vērtību šifrēšana](#encrypting-property-values)
7. [Savienojuma testēšana](#testing-a-connection)
8. [Kuru datubāzi redz savienojums](#which-database-the-connection-sees)
9. [Profilēšanas režīms un darba shēma](#profiling-mode-and-work-schema)
10. [DSN izmantošana](#using-a-dsn-instead)
11. [Problēmu novēršana](#troubleshooting)

---

## Kā darbojas savienojumi {: #how-connections-work }

*digna* sasniedz katru avota tehnoloģiju caur **ODBC**. Savienojums ir ODBC rekvizītu
saraksts, ko ievadāt kā atslēgas/vērtības pārus. Kad *digna* atver savienojumu, tā apvieno šos
pārus savienojuma virknē — `Key=Value`, atdalītus ar `;`, tādā secībā, kādā tos norādījāt —
un nodod to ODBC draiveru pārvaldniekam *digna* resursdatorā.

Tas, ka rekvizītus ievadāt paši, padara iestatīšanu **bez DSN** (DSN-less): savienojums satur
visu, kas draiverim nepieciešams, tāpēc resursdatorā nav jāreģistrē ODBC datu avots (DSN).
Šis ir ieteicamais veids, kā konfigurēt *digna*, jo savienojuma definīcija pilnībā atrodas
*digna* un pārvietojas kopā ar to.

### Kāpēc ODBC {: #why-odbc }

Iepriekšējos izlaidumos varēja izvēlēties starp tehnoloģijai specifisku draiveri un ODBC,
izmantojot slēdzi **Use ODBC**. Sākot ar Release 2026.06, *digna* balstās tikai uz ODBC.
Viena standarta saskarne sniedz vairāk nekā atsevišķu pielāgotu draiveru kopa:

- **Autentifikācija** — autentifikācija ir daļa no ODBC, tāpēc savienojums var izmantot visu,
  ko atbalsta tā draiveris: paroles, tokenus un PAT, Kerberos un Active Directory, MFA un
  pārlūkā balstītu vienreizējo pieteikšanos, mākoņa identitāti, klienta sertifikātus un TLS.
  Jaunas metodes kļūst pieejamas ar draivera atjauninājumu, negaidot *digna* izlaidumu.
- **Draiveri, ko uztur datubāzu piegādātāji** — piegādātāja paša draiveris seko jaunām servera
  versijām un drošības labojumiem, un jūs varat to atjaunināt pēc sava grafika, neatkarīgi no
  *digna*.
- **Viens veids, kā konfigurēt visu** — katra tehnoloģija ir atslēgas/vērtības rekvizītu
  saraksts ar vienādu saskarni, vienādu sensitīvo vērtību šifrēšanu un vienādu problēmu
  novēršanu, nevis atšķirīgu lauku kopu katram avotam.
- **Pielāgošana un aptvērums** — draivera līmeņa opcijas, piemēram, taimauti, TLS iestatījumi,
  starpniekserveri un ielādes apjomi, ir pieejamas katram avotam, un var pievienot jebkuru
  tehnoloģiju ar atbilstošu ODBC draiveri, ieskaitot tādas, kurām *digna* nepublicē atsevišķu ceļvedi.

!!! note "Kas mainījās saskarnē"

    Slēdzis **Use ODBC** un atsevišķie resursdatora, porta, datubāzes, lietotāja un paroles lauki
    vairs nepastāv. Savienojumam, kas vēl neizmanto ODBC, jāievada ODBC rekvizīti, pirms tas
    atkal darbosies — skatiet
    [Izveidot datubāzes savienojumu](#create-a-database-connection).

---

## Tehnoloģiju ceļveži {: #technology-guides }

Rekvizītu nosaukumi katram draiverim atšķiras, un katrai tehnoloģijai ir viena vai divas
īpatnības, kuru citām nav. Tālāk norādītie ceļveži aptver šo daļu; šī lapa aptver *digna* pusi,
kas visiem ir vienāda.

!!! important "Rekvizītu kopas ceļvežos ir piemēri"

    Katrā ceļvedī parādīta viena kombinācija, par kuru zināms, ka tā darbojas — tā, ar kuru *digna*
    tiek testēta. Tas ir sākumpunkts, nevis specifikācija: rekvizīti pieder ODBC draiverim, un tas,
    kuri no tiem pastāv, kā tie saucas un kādas vērtības pieņem, atšķiras starp draiveru versijām
    un piegādātājiem, starp Windows, Linux un macOS, kā arī atkarībā no avota servera
    konfigurācijas — autentifikācijas metodes, TLS, vārtejas, porta. Rēķinieties, ka vienu vai
    divas vērtības būs jāpielāgo, un par noteicošo uzskatiet jūsu instalētās draivera versijas dokumentāciju.

| Tehnoloģija | Ceļvedis | Vērts zināt |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless pūliem resursdatora nosaukumā nepieciešams `-ondemand`, un tie atbalsta tikai *Standard* profilēšanu |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Tokena autentifikācija: `UID=token`, PAT laukā `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Katalogi nāk no draivera, nevis no vaicājuma |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Draivera nosaukums ir figūriekavās: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` pieņem vai nu pilnu savienojuma deskriptoru, vai `tnsnames.ora` aizstājvārdu |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` jāatbilst servera prasībām |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programmatic access token ir testētais autentifikācijas veids |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` nosaka, kuras shēmas *digna* var redzēt |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Resursdators tiek norādīts `DBCNAME`; datubāzes darbojas kā shēmas |

---

## Priekšnosacījums: instalēt ODBC draiveri digna resursdatorā {: #install-the-driver }

*digna* atver avota savienojumus no **servera, kurā darbojas digna backend**, nevis no
pārlūka. Tāpēc ODBC draiverim jābūt instalētam šajā datorā, un tā nosaukumam jābūt
reģistrētam lokālajā draiveru pārvaldniekā.

=== "Windows"

    Instalējiet piegādātāja 64 bitu draiveri, pēc tam atveriet **ODBC Data Source Administrator (64-bit)**
    un pārslēdzieties uz cilni **Drivers**. Tur norādītie nosaukumi ir tieši tās vērtības, ko
    varat izmantot rekvizītam `Driver`.

=== "Linux"

    Instalējiet **unixODBC** un piegādātāja draiveri, pēc tam izvadiet reģistrēto draiveru nosaukumus:

    ```bash
    odbcinst -q -d
    ```

    Kvadrātiekavās izvadītie nosaukumi ir vērtības, ko varat izmantot rekvizītam `Driver`. Tie
    nāk no `/etc/odbcinst.ini` (vai faila, ko norāda `odbcinst -j`).

=== "macOS"

    Instalējiet **unixODBC** (piemēram, ar `brew install unixodbc`) un piegādātāja draiveri,
    pēc tam izvadiet reģistrēto draiveru nosaukumus:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Draivera nosaukumam jāsakrīt līdz pēdējai rakstzīmei"

    `Driver` tiek nodots draiveru pārvaldniekam nemainītā veidā. Draiveru pārvaldniekam
    `Simba Spark ODBC Driver` un `Simba Spark ODBC Driver 64` ir dažādi draiveri, un
    nereģistrēts nosaukums izraisa kļūdu *data source name not found*, lai gan DSN
    nemaz netiek izmantots.

Reģistrēta nosaukuma vietā visi izplatītie draiveru pārvaldnieki pieņem arī pilnu ceļu uz
draivera bibliotēku, piemēram, `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Tas
noder, ja draiveris ir instalēts, bet nav reģistrēts.

---

## Izveidot datubāzes savienojumu {: #create-a-database-connection }

Atveriet **Admin Panel**, dodieties uz cilni **Database Connections** un noklikšķiniet
**Add DB Connection**. Ekrānā jānorāda pieci elementi:

| Lauks | Apraksts |
|---|---|
| **Name** | Savienojuma nosaukums. Tas tiek izmantots, lai atsauktos uz savienojumu citos ekrānos. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake vai Hive. Tas nosaka SQL dialektu, ko ģenerē *digna*, tāpēc tam jāatbilst avotam, nevis draiverim. Azure Synapse Analytics ir **SQL Server** savienojums. |
| **ODBC Properties** | Atslēgas/vērtības pāri, kas aprakstīti sadaļā [ODBC rekvizīti](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* vai *Session* — skatiet [Profilēšanas režīms un darba shēma](#profiling-mode-and-work-schema). |
| **Work Schema** | Shēma, kurā atrodas darba tabulas *Permanent* profilēšanai. |

Savienojums tiek administrēts centralizēti un pēc tam piešķirts vienam vai vairākiem projektiem,
tāpēc viens un tas pats savienojums var apkalpot vairākus projektus.

---

## ODBC rekvizīti {: #odbc-properties }

Katram rekvizītam noklikšķiniet **Add Property** un aizpildiet **Key**, **Value** un, slepenām
vērtībām, izvēles rūtiņu **Encrypted**. Katras tehnoloģijas ceļvedī ir piemēra kopa šai
tehnoloģijai, ko pielāgojat savai draivera versijai un serverim — skatiet
[piezīmi iepriekš](#technology-guides).

Neatkarīgi no draivera rekvizītu kopa aptver tās pašas četras lietas:

- **`Driver`** — reģistrētais draivera nosaukums, kā aprakstīts [iepriekš](#install-the-driver).
- **Servera adrese** — atslēga katram draiverim atšķiras: `SERVER`, `HOST`, `DBCNAME`,
  `Server` vai, Oracle gadījumā, `DBQ` savienojuma deskriptors.
- **Akreditācijas dati** — parasti `UID` un `PWD`; Snowflake izmanto `UID` kopā ar `token`, un
  Databricks izmanto burtisku lietotāju `token` kopā ar personīgās piekļuves tokenu laukā `PWD`.
- **Datubāze vai katalogs, kurā strādāt**, ja tehnoloģijai tāds ir — skatiet
  [Kuru datubāzi redz savienojums](#which-database-the-connection-sees).

Jebko citu, ko dokumentē draiveris, var pievienot tādā pašā veidā — savienojumu pūlu, soketu
taimautus, Kerberos iestatījumus, starpniekservera iestatījumus. *digna* neinterpretē rekvizītus;
tā tikai nodod tos tālāk.

!!! warning "Vērtības netiek ekranētas — visu ar semikolu ievietojiet figūriekavās"

    Tā kā rekvizīti tiek apvienoti ar `;`, vērtība, kas pati satur `;`, sadalītu savienojuma
    virkni nepareizā vietā. Ietveriet šādas vērtības figūriekavās: `PWD={p@ss;word}`.
    Tas pats attiecas uz vērtībām ar `=` vai atstarpēm sākumā. Tādēļ arī dažus draiverus
    ierasts rakstīt figūriekavās, piemēram, `{NetezzaSQL}` vai `{SnowflakeDSIIDriver}`.

---

## Rekvizītu vērtību šifrēšana {: #encrypting-property-values }

Atzīmējiet **Encrypted** katram rekvizītam, kas satur noslēpumu — `PWD`, `token`, klienta
slepeno atslēgu. Tad vērtība tiek šifrēta, pirms tā tiek saglabāta *digna* repozitorijā,
ekrānā tā ir maskēta un tiek atšifrēta tikai tad, kad tiek veidota savienojuma virkne.

!!! tip "Padoms"

    Šifrētu vērtību nevar nolasīt atpakaļ ne saskarnē, ne caur API — to var tikai aizstāt.
    Glabājiet noslēpumus arī savā paroļu pārvaldniekā.

Rekvizītus, kas nav slepeni — draivera nosaukumu, resursdatoru, portu, datubāzi —, labāk
atstāt nešifrētus, lai tie paliktu salasāmi ikvienam, kurš vēlāk uzturēs savienojumu.

---

## Savienojuma testēšana {: #testing-a-connection }

Dialogā *Add DB Connection* noklikšķiniet **Test** **pirms** saglabāšanas. Tests izmanto
formā pašlaik esošās vērtības un veic reālu savienošanos, tāpēc tas ziņo tieši par to, ar ko
saskartos inspekcija — nepareizu draivera nosaukumu, noraidītu paroli, nesasniedzamu resursdatoru.
Nekas netiek saglabāts: testa savienojums tiek atritināts (rollback) neatkarīgi no tā, vai tas izdodas.

Esošam savienojumam novietojiet kursoru virs tā rindas cilnē **Database Connections** un
noklikšķiniet uz **kontaktdakšas** ikonas, lai to pārbaudītu vēlreiz. Tas ir ātrākais veids,
kā pārbaudīt, vai avots ir sasniedzams pēc paroles maiņas vai ugunsmūra izmaiņām.

---

## Kuru datubāzi redz savienojums {: #which-database-the-connection-sees }

Kad pievienojat datu avotu, *digna* piedāvā katalogus, shēmas un tabulas, ko savienojums var
sasniegt. Cik tālu tas sniedzas, ir atkarīgs no tehnoloģijas:

| Tehnoloģija | Piedāvātie katalogi |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Tikai savienojuma **pašreizējā** datubāze |
| **Teradata**, **Netezza**, **Databricks** | Visas datubāzes vai katalogi, ko lietotājam ir atļauts redzēt |
| **Hive**, **Impala** | Tos norāda draiveris |

!!! important "Viens savienojums, viena datubāze"

    PostgreSQL, SQL Server, Oracle un Snowflake gadījumā rekvizītiem jānorāda uz datubāzi,
    kurā atrodas avota shēmas — `DATABASE=…`, `Database=…` vai pakalpojuma nosaukums Oracle
    `DBQ` iekšpusē. Tabulas citā datubāzē caur šo savienojumu nav sasniedzamas; pievienojiet
    tai otru savienojumu.

---

## Profilēšanas režīms un darba shēma {: #profiling-mode-and-work-schema }

Profilēšanas režīms nosaka, kā *digna* apstrādā datus un aprēķina metrikas:

- **Standard:** Metrikas tiek aprēķinātas tieši avota tabulās, nekopējot datus.
- **Permanent:** Inspicētās dienas dati tiek nokopēti pastāvīgā tabulā, un metrikas tiek
  aprēķinātas nokopētajos datos.
- **Session:** Dati tiek nokopēti sesijas jeb pagaidu tabulā, un metrikas tiek aprēķinātas
  šajos pagaidu datos.

Režīms nosaka, kas savienojuma lietotājam jādrīkst darīt:

| Režīms | Ieraksta | Tiesības, kas nepieciešamas savienojuma lietotājam |
|---|---|---|
| **Standard** | neko | Lasīšana avota tabulās |
| **Permanent** | pa tabulai katram datu avotam shēmā **Work Schema** | Tabulu izveide un dzēšana shēmā **Work Schema** |
| **Session** | pagaidu tabulu, ko datubāze dzēš kopā ar sesiju | Pagaidu tabulu izveide — **Work Schema** netiek izmantota |

*Standard* tikai lasa, tāpēc tas ir režīms, kas jāizvēlas, ja *digna* piešķirta tikai lasīšanas
piekļuve. **Work Schema** tiek nolasīta tikai režīmā *Permanent*, taču to tik un tā vērts
aizpildīt, lai savienojums turpinātu darboties, ja režīms vēlāk tiek mainīts.

---

## DSN izmantošana {: #using-a-dsn-instead }

DSN joprojām darbojas — `DSN` ir vienkārši vēl viens rekvizīts:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN jābūt reģistrētam *digna* resursdatorā tam pašam lietotāja kontam, ar kuru darbojas *digna*
backend, un kā **System DSN**, ja *digna* darbojas kā pakalpojums. Visu, kas konfigurēts
DSN, var pārrakstīt, pievienojot to arī kā rekvizītu.

Iestatīšana bez DSN ir dokumentētais noklusējums, jo tā novērš šo resursdatora puses stāvokli:
savienojums ir pilnībā aprakstīts *digna*, un jaunā *digna* resursdatorā jāinstalē draiveris,
bet nekas nav jākonfigurē.

---

## Problēmu novēršana {: #troubleshooting }

### Data source name not found / no default driver specified

**Simptomi:**
- Poga **Test** ziņo par kļūdu, kurā minēts *data source name not found*, lai gan
  iestatīšana ir bez DSN

**Cēloņi un risinājumi:**
1. `Driver` vērtība neatbilst reģistrētam draivera nosaukumam — salīdziniet to ar cilni **Drivers**
   programmā *ODBC Data Source Administrator (64-bit)* vai ar `odbcinst -q -d`
2. Draiveris ir instalēts jūsu darbstacijā, bet ne *digna* resursdatorā
3. Draiveris ir 32 bitu, bet *digna* ir 64 bitu — instalējiet 64 bitu draiveri
4. Rekvizīta `Driver` vispār nav, un nav norādīts arī `DSN`
5. Linux un macOS draiveris ir instalēts, bet nav reģistrēts — tā vietā norādiet pilnu ceļu uz
   draivera bibliotēku vai reģistrējiet to failā `odbcinst.ini`

---

### Savienojuma testam iestājas taimauts

**Simptomi:**
- **Test** uzkaras un pēc aptuveni pusminūtes neizdodas

**Cēloņi un risinājumi:**
1. Resursdators vai ports nav sasniedzams no *digna* resursdatora — pārbaudiet ugunsmūri un,
   mākoņa avotiem, IP atļauto sarakstu
2. Resursdatora nosaukums ir pareizs, bet ports pieder citam pakalpojumam
3. Avotam nepieciešams vairāk nekā noklusējuma 30 sekundes, lai pieņemtu savienojumu — palieliniet
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` faila `config.toml` sadaļā `[base]` (`0` gaida
   bezgalīgi) un restartējiet backend
4. Serverless gala punkts atsāk darbu pēc dīkstāves — mēģiniet vēlreiz, un, ja tas notiek regulāri,
   palieliniet pieteikšanās taimautu, kā aprakstīts iepriekš

---

### Autentifikācija neizdodas, lai gan akreditācijas dati ir pareizi

**Simptomi:**
- Draiveris ziņo par nederīgiem akreditācijas datiem, bet tas pats lietotājs darbojas citā SQL klientā

**Cēloņi un risinājumi:**
1. Parole satur `;` — ietveriet vērtību figūriekavās: `{p@ss;word}`
2. Vērtībā tika iekopēta atstarpe beigās
3. Draiveris sagaida konkrētu autentifikācijas mehānismu — piemēram, `AuthMech` Hive un
   Databricks draiveriem vai `authenticator` Snowflake
4. Vērtība tika saglabāta šifrēta un pēc tam rediģēta — šifrētas vērtības nevar nolasīt atpakaļ,
   tāpēc ievadiet noslēpumu no jauna pilnībā
5. Tokena derīgums ir beidzies — personīgās piekļuves tokeni un programmatic access tokeni tiek
   izsniegti ar derīguma termiņu

---

### Datu avota ekrānā netiek piedāvāta gaidītā datubāze vai shēma

**Simptomi:**
- Pievienojot datu avotu, trūkst katalogu, shēmu vai tabulu

**Cēloņi un risinājumi:**
1. Savienojums norāda uz citu datubāzi — skatiet
   [Kuru datubāzi redz savienojums](#which-database-the-connection-sees)
2. Savienojuma lietotājam nav lasīšanas tiesību shēmā vai datu vārdnīcā
3. **Technology** neatbilst avotam, tāpēc *digna* vaicā nepareizo datu vārdnīcu
4. Snowflake gadījumā lietotājam nav piešķirta noklusējuma noliktava (warehouse) un nav norādīts
   rekvizīts `Warehouse`, tāpēc metadatu vaicājumus nevar izpildīt

---

### Profilēšana neizdodas, lai gan savienojuma tests ir veiksmīgs

**Simptomi:**
- **Test** ir veiksmīgs, bet inspekcija neizdodas, kad tiek veidotas darba tabulas

**Cēloņi un risinājumi:**
1. Ir izvēlēta *Permanent* profilēšana, un savienojuma lietotājs nevar izveidot tabulas shēmā
   **Work Schema** — piešķiriet tiesības vai pārslēdzieties uz *Session* vai *Standard*
2. **Work Schema** ir tukša vai norāda uz neesošu shēmu, kamēr ir izvēlēta *Permanent*
   profilēšana
3. Ir izvēlēta *Session* profilēšana, un savienojuma lietotājs nedrīkst izveidot pagaidu tabulas
4. Ilgstošs profilēšanas vaicājums sasniedz vaicājuma taimautu — palieliniet
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` faila `config.toml` sadaļā `[base]` (noklusējums 3600
   sekundes, `0` atspējo taimautu)

---

## Labākā prakse

**DARĪT:**

- Instalējiet un reģistrējiet draiveri *digna* resursdatorā pirms savienojuma konfigurēšanas
- Atzīmējiet **Encrypted** katrai parolei un tokenam
- Noklikšķiniet **Test** pirms saglabāšanas un testējiet vēlreiz pēc paroles maiņas
- Nosauciet savienojumus pēc avota un vides, piemēram, `sales_dwh_prod`
- Piešķiriet *digna* atsevišķu datubāzes lietotāju, ar tikai lasīšanas tiesībām, ja pietiek ar *Standard* profilēšanu
- Uzturiet vienu savienojumu katrai avota datubāzei un pievienojiet otru, nevis pārslēdziet pirmo

**NEDARĪT:**

- Glabāt noslēpumus nešifrētus vai koplietot vienu datubāzes lietotāju starp *digna* un citiem rīkiem
- Izmantot 32 bitu draiveri ar 64 bitu *digna* instalāciju
- Paļauties uz User DSN, ja *digna* darbojas kā pakalpojums — tas nebūs redzams
- Ievietot rekvizītā vērtību, kas satur `;`, bez figūriekavām
- Norādīt **Work Schema** uz shēmu, kurā atrodas avota dati

---

## Atbalsts

Nepieciešama palīdzība ar datubāzes savienojumu?

- **E-pasts:** support@digna.ai
- **Dokumentācija:** https://docs.digna.ai
- **Tīmekļa vietne:** https://www.digna.ai

---

**Izlaidums:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
