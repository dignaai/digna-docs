---
title: Duomenų bazių ryšių apžvalga – ODBC nustatymas be DSN | digna dokumentacija
description: Kaip veikia duomenų bazių ryšiai digna. Kiekviena šaltinio technologija pasiekiama per ODBC naudojant ryšio eilutę be DSN, sudarytą iš ODBC savybių. Apima tvarkyklės diegimą digna serveryje, ekraną Add DB Connection, savybių šifravimą, ryšio testavimą, trikčių šalinimą ir nuorodas į atskirų technologijų vadovus.
image: /assets/logo_square.png
keywords:
  - digna duomenų bazės ryšys
  - dsn-less odbc
  - odbc be DSN
  - odbc ryšio eilutė
  - odbc tvarkyklės nustatymas
  - unixodbc
  - odbc savybės
  - duomenų šaltinio konfigūracija
lang: lt
robots: index, follow
og_title: digna duomenų bazių ryšiai – ODBC nustatymas be DSN
og_description: Sukonfigūruokite digna šaltinio ryšį per ODBC be DSN. Tvarkyklės diegimas, ODBC savybės, šifravimas, testavimas ir trikčių šalinimas.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Duomenų bazių ryšių apžvalga

---

## Turinys

1. [Kaip veikia ryšiai](#how-connections-work)
2. [Technologijų vadovai](#technology-guides)
3. [Būtina sąlyga: įdiekite ODBC tvarkyklę digna serveryje](#install-the-driver)
4. [Duomenų bazės ryšio sukūrimas](#create-a-database-connection)
5. [ODBC savybės](#odbc-properties)
6. [Savybių reikšmių šifravimas](#encrypting-property-values)
7. [Ryšio testavimas](#testing-a-connection)
8. [Kurią duomenų bazę mato ryšys](#which-database-the-connection-sees)
9. [Profiliavimo režimas ir Work Schema](#profiling-mode-and-work-schema)
10. [DSN naudojimas](#using-a-dsn-instead)
11. [Trikčių šalinimas](#troubleshooting)

---

## Kaip veikia ryšiai {: #how-connections-work }

*digna* kiekvieną šaltinio technologiją pasiekia per **ODBC**. Ryšys yra ODBC savybių sąrašas,
kurį įvedate kaip raktų ir reikšmių poras. Kai *digna* atidaro ryšį, ji sujungia šias poras į
ryšio eilutę — `Key=Value`, atskirtas `;`, ta tvarka, kuria jas surašėte — ir perduoda ją
ODBC tvarkyklių tvarkytuvei (driver manager) *digna* serveryje.

Būtent tai, kad savybes įvedate patys, daro nustatymą **be DSN** (DSN-less): ryšys turi viską,
ko reikia tvarkyklei, todėl serveryje nereikia registruoti jokio ODBC duomenų šaltinio (DSN).
Tai rekomenduojamas *digna* konfigūravimo būdas, nes ryšio apibrėžimas visas saugomas *digna*
ir keliauja kartu su ja.

### Kodėl ODBC {: #why-odbc }

Ankstesnėse versijose buvo galima rinktis tarp konkrečiai technologijai skirtos tvarkyklės ir
ODBC — tai buvo pasirenkama jungikliu **Use ODBC**. Nuo Release 2026.06 *digna* remiasi tik
ODBC. Viena standartinė sąsaja suteikia daugiau, nei gali pasiūlyti atskirų specialių tvarkyklių
rinkinys:

- **Autentifikacija** — autentifikacija yra ODBC dalis, todėl ryšys gali naudoti bet ką, ką
  palaiko jo tvarkyklė: slaptažodžius, žetonus ir PAT, Kerberos ir Active Directory, MFA ir
  naršyklėje vykdomą vienkartinį prisijungimą (SSO), debesijos tapatybę, kliento sertifikatus ir
  TLS. Nauji metodai atsiranda atnaujinus tvarkyklę, o ne laukiant naujos *digna* versijos.
- **Tvarkyklės, kurias prižiūri duomenų bazių gamintojai** — gamintojo tvarkyklė seka naujas
  serverio versijas ir saugumo pataisas, o jūs galite ją atnaujinti savo pasirinktu laiku,
  nepriklausomai nuo *digna*.
- **Vienas būdas viskam konfigūruoti** — kiekviena technologija yra raktų ir reikšmių savybių
  sąrašas su ta pačia sąsaja, tuo pačiu jautrių reikšmių šifravimu ir tuo pačiu trikčių
  šalinimu, o ne atskiru laukų rinkiniu kiekvienam šaltiniui.
- **Derinimas ir aprėptis** — tvarkyklės lygmens parinktys, tokios kaip laiko limitai, TLS
  nustatymai, tarpiniai serveriai (proxy) ir gavimo dydžiai (fetch size), prieinamos kiekvienam
  šaltiniui, o prijungti galima bet kurią technologiją, turinčią standartą atitinkančią ODBC
  tvarkyklę, įskaitant tas, kurioms *digna* neskelbia atskiro vadovo.

!!! note "Kas pasikeitė sąsajoje"

    Jungiklio **Use ODBC** ir atskirų serverio, prievado, duomenų bazės, vartotojo ir
    slaptažodžio laukų nebėra. Ryšiui, kuris dar nenaudoja ODBC, reikia įvesti ODBC savybes,
    kad jis vėl veiktų — žr.
    [Duomenų bazės ryšio sukūrimas](#create-a-database-connection).

---

## Technologijų vadovai {: #technology-guides }

Savybių pavadinimai skiriasi priklausomai nuo tvarkyklės, ir kiekviena technologija turi vieną
ar dvi ypatybes, kurių neturi kitos. Toliau pateikti vadovai aprašo būtent tą dalį; šis
puslapis aprašo *digna* pusę, kuri visoms jiems yra vienoda.

!!! important "Vadovuose pateikti savybių rinkiniai yra pavyzdžiai"

    Kiekviename vadove parodytas vienas žinomai veikiantis derinys — tas, su kuriuo *digna*
    testuojama. Tai atspirties taškas, o ne specifikacija: savybės priklauso ODBC tvarkyklei, o
    tai, kokios jų yra, kaip jos vadinasi ir kokias reikšmes priima, skiriasi tarp tvarkyklių
    versijų ir gamintojų, tarp Windows, Linux ir macOS bei priklauso nuo to, kaip sukonfigūruotas
    šaltinio serveris — autentifikacijos metodo, TLS, šliuzo, prievado. Tikėkitės, kad teks
    pakoreguoti vieną ar dvi reikšmes, ir laikykite įdiegtos tvarkyklės versijos dokumentaciją
    lemiamu šaltiniu.

| Technologija | Vadovas | Verta žinoti |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless telkiniams serverio pavadinime reikia `-ondemand`, ir jie palaiko tik *Standard* profiliavimą |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Autentifikacija žetonu: `UID=token`, PAT lauke `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Katalogus pateikia tvarkyklė, o ne užklausa |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Tvarkyklės pavadinimas rašomas riestiniuose skliaustuose: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` priima pilną prisijungimo aprašą (connect descriptor) arba `tnsnames.ora` pseudonimą |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` turi atitikti tai, ko reikalauja serveris |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Programinės prieigos žetonas (programmatic access token) yra testuotas autentifikacijos būdas |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` nulemia, kurias schemas *digna* gali matyti |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Serveris nurodomas `DBCNAME`; duomenų bazės veikia kaip schemos |

---

## Būtina sąlyga: įdiekite ODBC tvarkyklę digna serveryje {: #install-the-driver }

*digna* atidaro šaltinių ryšius iš **serverio, kuriame veikia digna backend**, o ne iš
naršyklės. Todėl ODBC tvarkyklė turi būti įdiegta tame kompiuteryje, o jos pavadinimas turi būti
užregistruotas vietinėje tvarkyklių tvarkytuvėje.

=== "Windows"

    Įdiekite gamintojo 64 bitų tvarkyklę, tada atidarykite **ODBC Data Source Administrator (64-bit)**
    ir pereikite į skirtuką **Drivers**. Ten išvardyti pavadinimai yra būtent tos reikšmės, kurias
    galite naudoti savybei `Driver`.

=== "Linux"

    Įdiekite **unixODBC** ir gamintojo tvarkyklę, tada išveskite užregistruotų tvarkyklių pavadinimus:

    ```bash
    odbcinst -q -d
    ```

    Laužtiniuose skliaustuose išvesti pavadinimai yra reikšmės, kurias galite naudoti savybei
    `Driver`. Jie paimami iš `/etc/odbcinst.ini` (arba iš failo, kurį nurodo `odbcinst -j`).

=== "macOS"

    Įdiekite **unixODBC** (pavyzdžiui, su `brew install unixodbc`) ir gamintojo tvarkyklę,
    tada išveskite užregistruotų tvarkyklių pavadinimus:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Tvarkyklės pavadinimas turi sutapti simbolis į simbolį"

    `Driver` perduodamas tvarkyklių tvarkytuvei nepakeistas. `Simba Spark ODBC Driver` ir
    `Simba Spark ODBC Driver 64` tvarkyklių tvarkytuvei yra skirtingos tvarkyklės, o
    neužregistruotas pavadinimas sukelia klaidą *data source name not found*, nors jokio DSN
    nenaudojama.

Vietoje užregistruoto pavadinimo visos įprastos tvarkyklių tvarkytuvės priima ir pilną kelią iki
tvarkyklės bibliotekos, pavyzdžiui, `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. Tai
naudinga, kai tvarkyklė įdiegta, bet neužregistruota.

---

## Duomenų bazės ryšio sukūrimas {: #create-a-database-connection }

Atidarykite **Admin Panel**, eikite į skirtuką **Database Connections** ir spustelėkite
**Add DB Connection**. Ekrane prašoma nurodyti penkis dalykus:

| Laukas | Aprašymas |
|---|---|
| **Name** | Ryšio pavadinimas. Juo ryšys nurodomas kituose ekranuose. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake arba Hive. Nuo jo priklauso SQL dialektas, kurį generuoja *digna*, todėl jis turi atitikti šaltinį, o ne tvarkyklę. Azure Synapse Analytics yra **SQL Server** ryšys. |
| **ODBC Properties** | Raktų ir reikšmių poros, aprašytos skyriuje [ODBC savybės](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* arba *Session* — žr. [Profiliavimo režimas ir Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schema, kurioje laikomos darbinės lentelės *Permanent* profiliavimui. |

Ryšys administruojamas centralizuotai ir tada priskiriamas vienam ar keliems projektams, todėl
tas pats ryšys gali aptarnauti kelis projektus.

---

## ODBC savybės {: #odbc-properties }

Kiekvienai savybei spustelėkite **Add Property** ir užpildykite **Key**, **Value**, o
slaptoms reikšmėms pažymėkite žymimąjį langelį **Encrypted**. Kiekvieno technologijos vadove
pateiktas tos technologijos pavyzdinis rinkinys, kurį pritaikote savo tvarkyklės versijai ir
serveriui — žr. [pastabą aukščiau](#technology-guides).

Nepriklausomai nuo tvarkyklės, savybių rinkinys apima tuos pačius keturis dalykus:

- **`Driver`** — užregistruotas tvarkyklės pavadinimas, kaip aprašyta [aukščiau](#install-the-driver).
- **Serverio adresas** — raktas skiriasi priklausomai nuo tvarkyklės: `SERVER`, `HOST`, `DBCNAME`,
  `Server` arba, Oracle atveju, prisijungimo aprašas `DBQ`.
- **Prisijungimo duomenys** — paprastai `UID` ir `PWD`; Snowflake naudoja `UID` ir `token`, o
  Databricks naudoja pažodinį vartotoją `token` ir asmeninį prieigos žetoną lauke `PWD`.
- **Duomenų bazė arba katalogas, kuriame dirbama**, jei technologija tokį turi — žr.
  [Kurią duomenų bazę mato ryšys](#which-database-the-connection-sees).

Bet ką kita, kas aprašyta tvarkyklės dokumentacijoje, galima pridėti tokiu pat būdu — ryšių
telkimą (connection pooling), lizdų laiko limitus, Kerberos nustatymus, tarpinio serverio
nustatymus. *digna* savybių neinterpretuoja; ji tik jas perduoda.

!!! warning "Reikšmės neišvengiamos (escape) — reikšmes su kabliataškiu rašykite riestiniuose skliaustuose"

    Kadangi savybės sujungiamos su `;`, reikšmė, kurioje pačioje yra `;`, perskeltų ryšio
    eilutę netinkamoje vietoje. Tokias reikšmes apgaubkite riestiniais skliaustais: `PWD={p@ss;word}`.
    Tas pats taikoma reikšmėms su `=` arba pradiniais tarpais. Dėl tos pačios priežasties kai
    kurių tvarkyklių pavadinimai įprastai rašomi riestiniuose skliaustuose, pvz., `{NetezzaSQL}`
    arba `{SnowflakeDSIIDriver}`.

---

## Savybių reikšmių šifravimas {: #encrypting-property-values }

Pažymėkite **Encrypted** kiekvienai savybei, kurioje saugoma paslaptis — `PWD`, `token`,
kliento slaptumo raktas. Tada reikšmė užšifruojama prieš ją išsaugant *digna* saugykloje,
ekrane ji paslepiama ir iššifruojama tik tada, kai sudaroma ryšio eilutė.

!!! tip "Patarimas"

    Užšifruotos reikšmės negalima perskaityti atgal nei vartotojo sąsajoje, nei per API — ją
    galima tik pakeisti. Paslaptis saugokite ir savo slaptažodžių tvarkyklėje.

Neslaptas savybes — tvarkyklės pavadinimą, serverį, prievadą, duomenų bazę — geriau palikti
neužšifruotas, kad jas galėtų perskaityti tas, kas vėliau prižiūrės ryšį.

---

## Ryšio testavimas {: #testing-a-connection }

Dialogo lange *Add DB Connection* spustelėkite **Test** **prieš** išsaugodami. Testas naudoja
formoje esamas reikšmes ir atlieka tikrą prisijungimą, todėl praneša būtent tai, su kuo
susidurtų inspekcija — neteisingą tvarkyklės pavadinimą, atmestą slaptažodį, nepasiekiamą
serverį. Niekas neišsaugoma: bandomasis ryšys atšaukiamas nepriklausomai nuo to, ar jis pavyko.

Jau esamą ryšį galite patikrinti iš naujo užvedę pelę ant jo eilutės skirtuke
**Database Connections** ir spustelėję **kištuko** piktogramą. Tai greičiausias būdas
patikrinti, ar šaltinis pasiekiamas po slaptažodžio pakeitimo ar ugniasienės pakeitimų.

---

## Kurią duomenų bazę mato ryšys {: #which-database-the-connection-sees }

Kai pridedate duomenų šaltinį, *digna* pasiūlo katalogus, schemas ir lenteles, kuriuos ryšys
gali pasiekti. Kiek toli tai siekia, priklauso nuo technologijos:

| Technologija | Siūlomi katalogai |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Tik ryšio **dabartinė** duomenų bazė |
| **Teradata**, **Netezza**, **Databricks** | Visos duomenų bazės ar katalogai, kuriuos vartotojui leidžiama matyti |
| **Hive**, **Impala** | Pateikia tvarkyklė |

!!! important "Vienas ryšys – viena duomenų bazė"

    PostgreSQL, SQL Server, Oracle ir Snowflake atveju savybės turi rodyti į duomenų bazę,
    kurioje yra šaltinio schemos — `DATABASE=…`, `Database=…` arba paslaugos pavadinimą
    Oracle `DBQ` viduje. Kitos duomenų bazės lentelės per tą ryšį nepasiekiamos; jai pridėkite
    antrą ryšį.

---

## Profiliavimo režimas ir Work Schema {: #profiling-mode-and-work-schema }

Profiliavimo režimas nulemia, kaip *digna* apdoroja duomenis ir skaičiuoja metrikas:

- **Standard:** metrikos skaičiuojamos tiesiogiai šaltinio lentelėse, nekopijuojant duomenų.
- **Permanent:** tikrinamos dienos duomenys nukopijuojami į nuolatinę lentelę, o metrikos
  skaičiuojamos pagal nukopijuotus duomenis.
- **Session:** duomenys nukopijuojami į seanso arba laikinąją lentelę, o metrikos
  skaičiuojamos pagal šiuos laikinus duomenis.

Režimas nulemia, ką turi būti leidžiama daryti ryšio vartotojui:

| Režimas | Ką rašo | Ryšio vartotojui reikalingos teisės |
|---|---|---|
| **Standard** | nieko | Skaityti šaltinio lenteles |
| **Permanent** | po lentelę kiekvienam duomenų šaltiniui schemoje **Work Schema** | Kurti ir šalinti lenteles schemoje **Work Schema** |
| **Session** | laikinąją lentelę, kurią duomenų bazė pašalina kartu su seansu | Kurti laikinąsias lenteles — **Work Schema** nenaudojama |

*Standard* tik skaito, todėl šį režimą verta rinktis, kai *digna* suteikiama tik skaitymo
prieiga. **Work Schema** skaitoma tik *Permanent* režimu, tačiau ją vis tiek verta užpildyti,
kad ryšys ir toliau veiktų, jei režimas vėliau būtų pakeistas.

---

## DSN naudojimas {: #using-a-dsn-instead }

DSN vis dar veikia — `DSN` yra tiesiog dar viena savybė:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN turi būti užregistruotas *digna* serveryje tai pačiai vartotojo paskyrai, kuria veikia
*digna* backend, o kai *digna* veikia kaip paslauga — kaip **System DSN**. Viską, kas
sukonfigūruota DSN, galima perrašyti pridedant tai ir kaip savybę.

Nustatymas be DSN yra dokumentuotas numatytasis būdas, nes jis išvengia šios serverio pusės
būsenos: ryšys visiškai aprašytas *digna*, o naujame *digna* serveryje reikia įdiegti tvarkyklę,
bet nieko konfigūruoti nereikia.

---

## Trikčių šalinimas {: #troubleshooting }

### Data source name not found / no default driver specified

**Požymiai:**
- Mygtukas **Test** praneša apie klaidą, kurioje minima *data source name not found*, nors
  nustatymas yra be DSN

**Priežastys ir sprendimai:**
1. Reikšmė `Driver` nesutampa su užregistruotu tvarkyklės pavadinimu — palyginkite ją su
   *ODBC Data Source Administrator (64-bit)* skirtuku **Drivers** arba su `odbcinst -q -d`
2. Tvarkyklė įdiegta jūsų darbo stotyje, bet ne *digna* serveryje
3. Tvarkyklė yra 32 bitų, o *digna* – 64 bitų — įdiekite 64 bitų tvarkyklę
4. Savybės `Driver` visai nėra, ir nenurodytas ir `DSN`
5. Linux ir macOS sistemose tvarkyklė įdiegta, bet neužregistruota — vietoje pavadinimo
   nurodykite pilną kelią iki tvarkyklės bibliotekos arba užregistruokite ją `odbcinst.ini`

---

### Ryšio testui baigiasi laikas

**Požymiai:**
- **Test** pakimba ir maždaug po pusės minutės nepavyksta

**Priežastys ir sprendimai:**
1. Serveris ar prievadas nepasiekiamas iš *digna* serverio — patikrinkite ugniasienę, o
   debesijos šaltinių atveju — leidžiamų IP adresų sąrašą
2. Serverio pavadinimas teisingas, bet prievadas priklauso kitai paslaugai
3. Šaltiniui priimti ryšį reikia daugiau nei numatytųjų 30 sekundžių — padidinkite
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` faile `config.toml` skiltyje `[base]` (`0` laukia
   neribotai) ir perkraukite backend
4. Serverless galinis taškas atsibunda po neveiklumo — bandykite dar kartą, o jei tai nutinka
   reguliariai, padidinkite prisijungimo laiko limitą, kaip nurodyta aukščiau

---

### Autentifikacija nepavyksta, nors prisijungimo duomenys teisingi

**Požymiai:**
- Tvarkyklė praneša apie netinkamus prisijungimo duomenis, bet tas pats vartotojas veikia kitame SQL kliente

**Priežastys ir sprendimai:**
1. Slaptažodyje yra `;` — apgaubkite reikšmę riestiniais skliaustais: `{p@ss;word}`
2. Į reikšmę buvo nukopijuotas galinis tarpas
3. Tvarkyklė tikisi konkretaus autentifikacijos mechanizmo — pavyzdžiui, `AuthMech` Hive ir
   Databricks tvarkyklėms arba `authenticator` Snowflake atveju
4. Reikšmė buvo išsaugota užšifruota ir paskui redaguota — užšifruotų reikšmių negalima
   perskaityti atgal, todėl įveskite paslaptį visą iš naujo
5. Baigėsi žetono galiojimas — asmeniniai prieigos žetonai ir programinės prieigos žetonai
   išduodami su galiojimo pabaigos data

---

### Duomenų šaltinio ekrane nesiūloma laukiama duomenų bazė ar schema

**Požymiai:**
- Pridedant duomenų šaltinį trūksta katalogų, schemų ar lentelių

**Priežastys ir sprendimai:**
1. Ryšys rodo į kitą duomenų bazę — žr.
   [Kurią duomenų bazę mato ryšys](#which-database-the-connection-sees)
2. Ryšio vartotojas neturi skaitymo teisių schemai arba duomenų žodynui
3. **Technology** neatitinka šaltinio, todėl *digna* užklausia netinkamo duomenų žodyno
4. Snowflake atveju vartotojui nepriskirtas numatytasis warehouse ir nenurodyta savybė
   `Warehouse`, todėl metaduomenų užklausos negali būti vykdomos

---

### Profiliavimas nepavyksta, nors ryšio testas sėkmingas

**Požymiai:**
- **Test** pavyksta, bet inspekcija nepavyksta kuriant darbines lenteles

**Priežastys ir sprendimai:**
1. Pasirinktas *Permanent* profiliavimas, o ryšio vartotojas negali kurti lentelių schemoje
   **Work Schema** — suteikite teises arba perjunkite į *Session* ar *Standard*
2. **Work Schema** tuščia arba nurodo neegzistuojančią schemą, kai pasirinktas *Permanent*
   profiliavimas
3. Pasirinktas *Session* profiliavimas, o ryšio vartotojui neleidžiama kurti laikinųjų lentelių
4. Ilgai trunkanti profiliavimo užklausa viršija užklausos laiko limitą — padidinkite
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` faile `config.toml` skiltyje `[base]` (numatytoji reikšmė
   3600 sekundžių, `0` išjungia laiko limitą)

---

## Geroji praktika

**DARYKITE:**

- Įdiekite ir užregistruokite tvarkyklę *digna* serveryje prieš konfigūruodami ryšį
- Pažymėkite **Encrypted** kiekvienam slaptažodžiui ir žetonui
- Prieš išsaugodami spustelėkite **Test**, o pakeitę slaptažodį patikrinkite iš naujo
- Ryšius pavadinkite pagal šaltinį ir aplinką, pavyzdžiui, `sales_dwh_prod`
- Suteikite *digna* atskirą duomenų bazės vartotoją, tik skaitymo teisėmis, kai pakanka *Standard* profiliavimo
- Kiekvienai šaltinio duomenų bazei laikykite po vieną ryšį ir verčiau pridėkite antrą, nei perjunginėkite pirmąjį

**NEDARYKITE:**

- Nesaugokite paslapčių neužšifruotų ir nenaudokite vieno duomenų bazės vartotojo *digna* ir kitiems įrankiams
- Nenaudokite 32 bitų tvarkyklės su 64 bitų *digna* diegimu
- Nesiremkite User DSN, kai *digna* veikia kaip paslauga — jis nebus matomas
- Nerašykite reikšmės su `;` į savybę be riestinių skliaustų
- Nenukreipkite **Work Schema** į schemą, kurioje laikomi šaltinio duomenys

---

## Pagalba

Reikia pagalbos dėl duomenų bazės ryšio?

- **El. paštas:** support@digna.ai
- **Dokumentacija:** https://docs.digna.ai
- **Svetainė:** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
