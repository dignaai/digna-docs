# Andmebaasiühenduste ülevaade

---

## Sisukord

1. [Kuidas ühendused töötavad](#how-connections-work)
2. [Tehnoloogiate juhendid](#technology-guides)
3. [Eeltingimus: ODBC draiveri paigaldamine digna hostile](#install-the-driver)
4. [Andmebaasiühenduse loomine](#create-a-database-connection)
5. [ODBC atribuudid](#odbc-properties)
6. [Atribuutide väärtuste krüpteerimine](#encrypting-property-values)
7. [Ühenduse testimine](#testing-a-connection)
8. [Millist andmebaasi ühendus näeb](#which-database-the-connection-sees)
9. [Profileerimisrežiim ja tööskeem](#profiling-mode-and-work-schema)
10. [DSN-i kasutamine](#using-a-dsn-instead)
11. [Tõrkeotsing](#troubleshooting)

---

## Kuidas ühendused töötavad {: #how-connections-work }

*digna* ühendub iga lähtetehnoloogiaga **ODBC** kaudu. Ühendus on ODBC atribuutide loend,
mille sisestate võti/väärtus-paaridena. Kui *digna* ühenduse avab, liidab ta need paarid
ühendusstringiks — `Key=Value`, eraldatud märgiga `;`, teie loetletud järjekorras — ja annab
selle *digna* hosti ODBC draiverihaldurile.

Just atribuutide ise sisestamine muudab seadistuse **DSN-ita** lahenduseks: ühendus sisaldab
kõike, mida draiver vajab, seega ei pea hostis registreerima ühtegi ODBC andmeallikat (DSN).
See on *digna* soovitatav konfigureerimisviis, sest ühenduse määratlus asub täielikult
*dignas* ja liigub koos sellega.

### Miks ODBC {: #why-odbc }

Varasemad väljaanded pakkusid valikut tehnoloogiapõhise draiveri ja ODBC vahel, mis valiti
lülitiga **Use ODBC**. Alates Release 2026.06 tugineb *digna* ainult ODBC-le. Üks
standardne liides annab rohkem, kui suudab hulk eraldi draivereid:

- **Autentimine** — autentimine on ODBC osa, seega saab ühendus kasutada kõike, mida selle
  draiver toetab: paroole, tokeneid ja PAT-e, Kerberost ja Active Directoryt, MFA-d ja
  brauseripõhist ühekordset sisselogimist, pilveidentiteeti, kliendisertifikaate ja TLS-i. Uued
  meetodid tulevad draiveri uuendusega, mitte *digna* väljaande ootamisega.
- **Andmebaasitootjate hallatavad draiverid** — tootja enda draiver järgib uusi serveriversioone
  ja turvaparandusi ning saate seda uuendada oma ajakava järgi, *dignast* sõltumatult.
- **Üks viis kõige konfigureerimiseks** — iga tehnoloogia on võti/väärtus-atribuutide loend,
  sama liidese, tundlike väärtuste sama krüpteerimise ja sama tõrkeotsinguga, mitte iga allika
  jaoks erinev väljade komplekt.
- **Häälestus ja ulatus** — draiveri tasemel valikud, nagu ajalõpud, TLS-i sätted, puhverserverid
  ja päringu tõmbemahud, on saadaval iga allika jaoks ning ühendada saab mis tahes tehnoloogia,
  millel on nõuetele vastav ODBC draiver, sealhulgas need, mille jaoks *digna* eraldi juhendit ei
  avalda.

!!! note "Mis liideses muutus"

    Lüliti **Use ODBC** ning eraldi hosti, pordi, andmebaasi, kasutaja ja parooli väljad on
    eemaldatud. Ühendus, mis veel ODBC-d ei kasuta, vajab enne uuesti töötamist ODBC atribuutide
    sisestamist — vt
    [Andmebaasiühenduse loomine](#create-a-database-connection).

---

## Tehnoloogiate juhendid {: #technology-guides }

Atribuutide nimed erinevad draiverite kaupa ja igal tehnoloogial on üks-kaks eripära, mida
teistel pole. Allolevad juhendid käsitlevad seda osa; see leht käsitleb *digna* poolt, mis on
kõigi jaoks sama.

!!! important "Juhendites toodud atribuutide komplektid on näited"

    Iga juhend näitab üht kombinatsiooni, mis teadaolevalt töötab — seda, mille vastu *dignat*
    testitakse. See on lähtepunkt, mitte spetsifikatsioon: atribuudid kuuluvad ODBC draiverile
    ning see, millised neist on olemas, kuidas neid nimetatakse ja milliseid väärtusi need
    aktsepteerivad, erineb draiveri versioonide ja tootjate vahel, Windowsi, Linuxi ja macOS-i
    vahel ning sõltub lähteserveri konfiguratsioonist — autentimismeetodist, TLS-ist, lüüsist,
    pordist. Arvestage, et mõnda väärtust tuleb kohandada, ja pidage autoriteetseks allikaks
    paigaldatud draiveriversiooni dokumentatsiooni.

| Tehnoloogia | Juhend | Tasub teada |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Serverless-kogumid vajavad hostinimes `-ondemand` ja toetavad ainult *Standard* profileerimist |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Tokeniga autentimine: `UID=token`, PAT väljal `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Kataloogid tulevad draiverilt, mitte päringust |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Draiveri nimi on loogelistes sulgudes: `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` võtab kas täieliku connect descriptori või `tnsnames.ora` aliase |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` peab vastama sellele, mida server nõuab |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Testitud autentimisviis on programmaatilise juurdepääsu token |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` määrab, milliseid skeeme *digna* näeb |
| **Teradata** | [Teradata](teradata_connector_guide.md) | Host läheb atribuuti `DBCNAME`; andmebaasid toimivad skeemidena |

---

## Eeltingimus: ODBC draiveri paigaldamine digna hostile {: #install-the-driver }

*digna* avab lähteühendused **serverist, kus töötab digna backend**, mitte brauserist. Seetõttu
peab ODBC draiver olema paigaldatud sellele masinale ja selle nimi peab olema registreeritud
kohalikus draiverihalduris.

=== "Windows"

    Paigaldage tootja 64-bitine draiver, seejärel avage **ODBC Data Source Administrator (64-bit)**
    ja lülituge vahekaardile **Drivers**. Seal loetletud nimed on täpselt need väärtused, mida
    võite kasutada atribuudi `Driver` jaoks.

=== "Linux"

    Paigaldage **unixODBC** ja tootja draiver, seejärel kuvage registreeritud draiverite nimed:

    ```bash
    odbcinst -q -d
    ```

    Nurksulgudes kuvatud nimed on väärtused, mida võite kasutada atribuudi `Driver` jaoks. Need
    pärinevad failist `/etc/odbcinst.ini` (või failist, millest teatab `odbcinst -j`).

=== "macOS"

    Paigaldage **unixODBC** (näiteks käsuga `brew install unixodbc`) ja tootja draiver,
    seejärel kuvage registreeritud draiverite nimed:

    ```bash
    odbcinst -q -d
    ```

!!! warning "Draiveri nimi peab kattuma täht-tähelt"

    `Driver` edastatakse draiverihaldurile muutmata kujul. `Simba Spark ODBC Driver` ja
    `Simba Spark ODBC Driver 64` on draiverihalduri jaoks erinevad draiverid ning
    registreerimata nimi põhjustab vea *data source name not found*, kuigi DSN-i üldse ei
    kasutata.

Registreeritud nime asemel aktsepteerivad kõik levinud draiverihaldurid ka draiveri teegi
täielikku teed, näiteks `Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. See on kasulik,
kui draiver on paigaldatud, kuid registreerimata.

---

## Andmebaasiühenduse loomine {: #create-a-database-connection }

Avage **Admin Panel**, minge vahekaardile **Database Connections** ja klõpsake
**Add DB Connection**. Kuva küsib viit asja:

| Väli | Kirjeldus |
|---|---|
| **Name** | Ühenduse nimi. Seda kasutatakse ühendusele viitamiseks teistes kuvades. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake või Hive. See valib SQL-dialekti, mida *digna* genereerib, seega peab see vastama allikale — mitte draiverile. Azure Synapse Analytics on **SQL Server** ühendus. |
| **ODBC Properties** | Võti/väärtus-paarid, mida on kirjeldatud jaotises [ODBC atribuudid](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* või *Session* — vt [Profileerimisrežiim ja tööskeem](#profiling-mode-and-work-schema). |
| **Work Schema** | Skeem, mis hoiab *Permanent* profileerimise töötabeleid. |

Ühendust hallatakse tsentraalselt ja seejärel määratakse see ühele või mitmele projektile, nii
et sama ühendus saab teenindada mitut projekti.

---

## ODBC atribuudid {: #odbc-properties }

Klõpsake iga atribuudi jaoks **Add Property** ja täitke **Key**, **Value** ning saladuste puhul
märkeruut **Encrypted**. Iga tehnoloogia juhend loetleb selle tehnoloogia näidiskomplekti,
mille kohandate oma draiveriversiooni ja serveri järgi — vt
[ülaltoodud märkust](#technology-guides).

Olenemata draiverist katab atribuutide komplekt samad neli asja:

- **`Driver`** — registreeritud draiveri nimi, nagu on kirjeldatud [eespool](#install-the-driver).
- **Serveri aadress** — võti erineb draiverite kaupa: `SERVER`, `HOST`, `DBCNAME`,
  `Server` või Oracle'i puhul `DBQ` connect descriptor.
- **Mandaadid** — tavaliselt `UID` ja `PWD`; Snowflake kasutab `UID` pluss `token` ning
  Databricks kasutab sõna-sõnalt kasutajat `token` pluss isiklikku juurdepääsutokenit väljal `PWD`.
- **Andmebaas või kataloog, milles töötada**, kui tehnoloogial see on — vt
  [Millist andmebaasi ühendus näeb](#which-database-the-connection-sees).

Kõike muud, mida draiveri dokumentatsioon kirjeldab, saab lisada samal viisil — ühenduste
koondamine, sokli ajalõpud, Kerberose sätted, puhverserveri sätted. *digna* atribuute ei
tõlgenda; ta ainult edastab need.

!!! warning "Väärtusi ei paojärjestata — pange semikooloniga väärtused loogelistesse sulgudesse"

    Kuna atribuudid liidetakse märgiga `;`, jagaks väärtus, mis ise sisaldab märki `;`,
    ühendusstringi vales kohas. Pange sellised väärtused loogelistesse sulgudesse: `PWD={p@ss;word}`.
    Sama kehtib väärtuste kohta, mis sisaldavad märki `=` või algavad tühikutega. Seetõttu
    kirjutatakse mõned draiverid tavapäraselt loogelistes sulgudes, näiteks `{NetezzaSQL}` või
    `{SnowflakeDSIIDriver}`.

---

## Atribuutide väärtuste krüpteerimine {: #encrypting-property-values }

Märkige **Encrypted** iga atribuudi puhul, mis sisaldab saladust — `PWD`, `token`, kliendi
saladus. Väärtus krüpteeritakse enne selle salvestamist *digna* repositooriumisse, maskeeritakse
kuval ja dekrüpteeritakse alles ühendusstringi koostamisel.

!!! tip "Vihje"

    Krüpteeritud väärtust ei saa tagasi lugeda, ei kasutajaliideses ega API kaudu — seda saab
    ainult asendada. Hoidke saladusi ka oma paroolihalduris.

Atribuudid, mis pole salajased — draiveri nimi, host, port, andmebaas —, on parem jätta
krüpteerimata, et need jääksid loetavaks sellele, kes ühendust hiljem hooldab.

---

## Ühenduse testimine {: #testing-a-connection }

Klõpsake dialoogis *Add DB Connection* **enne** salvestamist nuppu **Test**. Test kasutab
vormis parajasti olevaid väärtusi ja teeb päris ühenduse, seega teatab see täpselt sellest,
millega inspekteerimine kokku puutuks — vale draiveri nimi, tagasi lükatud parool, kättesaamatu
host. Midagi ei salvestata: testühendus rullitakse tagasi nii õnnestumise kui ka ebaõnnestumise
korral.

Olemasoleva ühenduse uuesti testimiseks viige kursor selle reale vahekaardil
**Database Connections** ja klõpsake ikooni **plug**. See on kiireim viis kontrollida, kas
allikas on pärast parooli vahetamist või tulemüüri muudatust kättesaadav.

---

## Millist andmebaasi ühendus näeb {: #which-database-the-connection-sees }

Andmeallika lisamisel pakub *digna* katalooge, skeeme ja tabeleid, milleni ühendus ulatub.
Kui kaugele see ulatub, sõltub tehnoloogiast:

| Tehnoloogia | Pakutavad kataloogid |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Ainult ühenduse **praegune** andmebaas |
| **Teradata**, **Netezza**, **Databricks** | Kõik andmebaasid või kataloogid, mida kasutajal on lubatud näha |
| **Hive**, **Impala** | Teatab draiver |

!!! important "Üks ühendus, üks andmebaas"

    PostgreSQL-i, SQL Serveri, Oracle'i ja Snowflake'i puhul peavad atribuudid osutama
    andmebaasile, mis sisaldab lähteskeeme — `DATABASE=…`, `Database=…` või teenuse nimi
    Oracle'i `DBQ` sees. Teise andmebaasi tabelid pole selle ühenduse kaudu kättesaadavad;
    lisage selle jaoks teine ühendus.

---

## Profileerimisrežiim ja tööskeem {: #profiling-mode-and-work-schema }

Profileerimisrežiim määrab, kuidas *digna* andmeid töötleb ja mõõdikuid arvutab:

- **Standard:** mõõdikud arvutatakse otse lähtetabelitel ilma andmeid kopeerimata.
- **Permanent:** inspekteeritava päeva andmed kopeeritakse püsivasse tabelisse ja mõõdikud
  arvutatakse kopeeritud andmetel.
- **Session:** andmed kopeeritakse seansi- või ajutisse tabelisse ja mõõdikud arvutatakse
  nendel ajutistel andmetel.

Režiim määrab, mida ühenduse kasutajal peab olema lubatud teha:

| Režiim | Kirjutab | Ühenduse kasutaja vajalikud õigused |
|---|---|---|
| **Standard** | mitte midagi | Lugemisõigus lähtetabelitele |
| **Permanent** | iga andmeallika kohta ühe tabeli skeemi **Work Schema** | Tabelite loomine ja kustutamine skeemis **Work Schema** |
| **Session** | ajutise tabeli, mille andmebaas seansi lõppedes kustutab | Ajutiste tabelite loomine — **Work Schema** ei kasutata |

*Standard* ainult loeb, mistõttu on see režiim, mille valida, kui *dignale* antakse ainult
lugemisõigus. **Work Schema** loetakse ainult režiimis *Permanent*, kuid selle täitmine tasub
end ikkagi ära, et ühendus töötaks edasi, kui režiimi hiljem muudetakse.

---

## DSN-i kasutamine {: #using-a-dsn-instead }

DSN töötab endiselt — `DSN` on lihtsalt üks atribuut:

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

DSN peab olema registreeritud *digna* hostis sama kasutajakonto jaoks, mis käitab *digna*
backendi, ning **System DSN**-ina, kui *digna* töötab teenusena. Kõik, mis on DSN-is
konfigureeritud, saab üle kirjutada, lisades selle ka atribuudina.

DSN-ita on dokumenteeritud vaikeviis, sest see väldib hostipoolset olekut: ühendus on täielikult
kirjeldatud *dignas* ja uuel *digna* hostil peab olema paigaldatud draiver, kuid midagi pole vaja
konfigureerida.

---

## Tõrkeotsing {: #troubleshooting }

### Data source name not found / no default driver specified

**Sümptomid:**
- Nupp **Test** teatab veast, mis mainib *data source name not found*, kuigi seadistus on
  DSN-ita

**Põhjused ja lahendused:**
1. Väärtus `Driver` ei vasta ühelegi registreeritud draiveri nimele — võrrelge seda
   *ODBC Data Source Administrator (64-bit)* vahekaardiga **Drivers** või käsu `odbcinst -q -d`
   väljundiga
2. Draiver on paigaldatud teie tööjaamale, kuid mitte *digna* hostile
3. Draiver on 32-bitine, samas kui *digna* on 64-bitine — paigaldage 64-bitine draiver
4. Atribuut `Driver` puudub täielikult ja ka `DSN` pole antud
5. Linuxis ja macOS-is on draiver paigaldatud, kuid registreerimata — andke selle asemel
   draiveri teegi täielik tee või registreerige see failis `odbcinst.ini`

---

### Ühenduse test aegub

**Sümptomid:**
- **Test** hangub ja ebaõnnestub umbes poole minuti pärast

**Põhjused ja lahendused:**
1. Host või port pole *digna* hostist kättesaadav — kontrollige tulemüüri ja pilveallikate puhul
   IP-lubade loendit
2. Hostinimi on õige, kuid port kuulub teisele teenusele
3. Allikas vajab ühenduse vastuvõtmiseks vaikimisi 30 sekundist rohkem aega — suurendage väärtust
   `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` faili `config.toml` jaotises `[base]` (`0` ootab
   lõpmatult) ja taaskäivitage backend
4. Serverless-lõpp-punkt ärkab jõudeolekust — proovige uuesti ja kui see juhtub regulaarselt,
   suurendage sisselogimise ajalõppu nagu eespool

---

### Autentimine ebaõnnestub, kuigi mandaadid on õiged

**Sümptomid:**
- Draiver teatab kehtetutest mandaatidest, kuid sama kasutaja töötab teises SQL-kliendis

**Põhjused ja lahendused:**
1. Parool sisaldab märki `;` — pange väärtus loogelistesse sulgudesse: `{p@ss;word}`
2. Väärtusesse kopeeriti lõpptühik
3. Draiver ootab kindlat autentimismehhanismi — näiteks `AuthMech` Hive'i ja Databricksi
   draiverite puhul või `authenticator` Snowflake'i puhul
4. Väärtus salvestati krüpteerituna ja seejärel muudeti — krüpteeritud väärtusi ei saa tagasi
   lugeda, seega sisestage saladus uuesti täies ulatuses
5. Token on aegunud — isiklikud juurdepääsutokenid ja programmaatilise juurdepääsu tokenid
   väljastatakse aegumiskuupäevaga

---

### Andmeallika kuva ei paku oodatud andmebaasi või skeemi

**Sümptomid:**
- Andmeallika lisamisel puuduvad kataloogid, skeemid või tabelid

**Põhjused ja lahendused:**
1. Ühendus osutab teisele andmebaasile — vt
   [Millist andmebaasi ühendus näeb](#which-database-the-connection-sees)
2. Ühenduse kasutajal puudub lugemisõigus skeemile või andmesõnastikule
3. **Technology** ei vasta allikale, seega pärib *digna* valet andmesõnastikku
4. Snowflake'i puhul pole kasutajale määratud vaikimisi warehouse'i ega antud atribuuti
   `Warehouse`, seega metaandmete päringuid ei saa käivitada

---

### Profileerimine ebaõnnestub, kuigi ühenduse test õnnestub

**Sümptomid:**
- **Test** läbib, kuid inspekteerimine ebaõnnestub töötabelite loomisel

**Põhjused ja lahendused:**
1. Valitud on *Permanent* profileerimine ja ühenduse kasutaja ei saa luua tabeleid skeemis
   **Work Schema** — andke õigused või lülituge režiimile *Session* või *Standard*
2. **Work Schema** on tühi või nimetab skeemi, mida pole olemas, samal ajal kui valitud on
   *Permanent* profileerimine
3. Valitud on *Session* profileerimine ja ühenduse kasutaja ei tohi luua ajutisi tabeleid
4. Pikalt kestev profileerimispäring jõuab päringu ajalõpuni — suurendage väärtust
   `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` faili `config.toml` jaotises `[base]` (vaikimisi 3600
   sekundit, `0` lülitab ajalõpu välja)

---

## Parimad tavad

**TEHKE:**

- Paigaldage ja registreerige draiver *digna* hostis enne ühenduse konfigureerimist
- Märkige **Encrypted** iga parooli ja tokeni puhul
- Klõpsake enne salvestamist **Test** ja testige uuesti pärast parooli vahetamist
- Nimetage ühendused allika ja keskkonna järgi, näiteks `sales_dwh_prod`
- Andke *dignale* eraldi andmebaasikasutaja, ainult lugemisõigusega, kui *Standard* profileerimisest piisab
- Hoidke iga lähteandmebaasi jaoks üks ühendus ja lisage pigem teine, kui muutke esimest

**ÄRGE:**

- Salvestage saladusi krüpteerimata ega jagage üht andmebaasikasutajat *digna* ja teiste tööriistade vahel
- Kasutage 32-bitist draiverit 64-bitise *digna* paigaldusega
- Lootke User DSN-ile, kui *digna* töötab teenusena — see pole nähtav
- Pange märki `;` sisaldavat väärtust atribuuti ilma loogeliste sulgudeta
- Suunake **Work Schema** skeemile, mis sisaldab lähteandmeid

---

## Tugi

Vajate abi andmebaasiühendusega?

- **E-post:** support@digna.ai
- **Dokumentatsioon:** https://docs.digna.ai
- **Veebileht:** https://www.digna.ai

---

**Väljaanne:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**