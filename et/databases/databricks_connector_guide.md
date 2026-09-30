# Lähtekonnektor Databricksi jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Databricksiga **ODBC** kaudu,
kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Databricksi eripärasid.

!!! note "Unity Catalog on nõutav"

    *digna* loeb saadaolevad kataloogid tabelist `system.information_schema.catalogs`, seega
    peab tööruumis olema Unity Catalog lubatud. Varasemad *digna* väljaanded pakkusid ilma Unity
    Catalogita tööruumide jaoks eraldi tehnoloogiat "Databricks Legacy"; see pole enam saadaval.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage **Databricks ODBC Driver** masinale, kus töötab *digna* backend, järgides
[Databricksi paigaldusjuhendit](https://docs.databricks.com/aws/en/integrations/odbc/).

Olenevalt versioonist registreerib draiver end nime all **Simba Spark ODBC Driver** või
**Databricks ODBC Driver**. Lugege oma hostist välja täpne registreeritud nimi, nagu on
kirjeldatud jaotises [ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. Ühenduse andmete kogumine {: #2-gather-the-connection-details }

Kõik väärtused pärinevad SQL warehouse'ist (või klastrist), mida soovite, et *digna*
kasutaks. Avage see Databricksi tööruumis ja minge jaotisse **Connection details**:

| Databricksi väli | Kasutatakse kui |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, tavaliselt `443` |
| **HTTP path** | `HTTPPath` |

Autentimiseks looge **isiklik juurdepääsutoken** (personal access token) — vt
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokenid kuuluvad kasutajale või teenuseprintsipaalile ja sellel printsipaalil peavad olema
lähteandmetele õigused `USE CATALOG`, `USE SCHEMA` ja `SELECT`.

---

## 3. ODBC atribuudid {: #3-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Databricksi/Simba draiverile, seega erinevad nende nimed, vaikeväärtused ja
    aktsepteeritavad väärtused draiveri versioonide vahel — draiverit on korduvalt ümber
    nimetatud ja selle autentimisvalikuid laiendatud — ning platvormide vahel. Kasutage seda
    lähtepunktina ja kontrollige paigaldatud draiveriversiooni dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `Host` | `<workspace>.cloud.databricks.com` | Warehouse'i serveri hostinimi, nt `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Warehouse'i või klastri HTTP-tee |
| `SSL` | `1` | Databricksi lõpp-punktid kasutavad ainult TLS-i |
| `ThriftTransport` | `2` | HTTP-transport, mida SQL-lõpp-punktid kasutavad |
| `AuthMech` | `3` | Tokeniga autentimine |
| `UID` | `token` | Sõna-sõnalt `token`, mitte kasutajanimi |
| `PWD` | `dapi…` | Isiklik juurdepääsutoken. Märkige **Encrypted** |
| `UseNativeQuery` | `1` | Edastab *digna* SQL-i muutmata kujul — vt allpool |

Tulemuseks olev ühendusstring näeb välja selline:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Jätke `UseNativeQuery=1`"

    Väärtusega `UseNativeQuery=0` — draiveri vaikeväärtus — kirjutab draiver sissetuleva SQL-i
    ümber sellesse, mida ta peab porditavaks ODBC süntaksiks. *digna* genereerib juba
    Databricksi SQL-i, seega võib ümberkirjutamine muuta tagurpidi ülakomadega tsiteerimist ja
    kuupäevaliteraale ning profileerimine ebaõnnestub siis lausetel, mis on algsel kujul
    kehtivad.

### OAuth tokeni asemel

OAuth masinalt-masinale autentimisega teenuseprintsipaali puhul asendage `AuthMech`,
`UID` ja `PWD` järgmisega:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Kliendi mandaadid |
| `Auth_Client_ID` | `<application id>` | Teenuseprintsipaal |
| `Auth_Client_Secret` | `<client secret>` | Märkige **Encrypted** |

---

## 4. *digna* konfiguratsioon {: #4-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Märkused Databricksi kohta {: #5-notes-on-databricks }

- **Warehouse peab töötama** või suutma käivituda, kui *digna* ühendub. Peatatud olekust
  ärkav warehouse võib vajada rohkem aega kui ühenduse ajalõpp — kui test ebaõnnestub esimesel
  katsel pärast jõudeolekut, proovige uuesti.
- **Kataloogid tulevad tööruumist.** Erinevalt enamikust tehnoloogiatest ulatub üks
  Databricksi ühendus igasse kataloogi, mida printsipaalil on lubatud näha, seega saab üks
  ühendus teenindada allikaid mitmes kataloogis.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema** allika
  kataloogis, seega vajab printsipaal seal õigust `CREATE TABLE`. *Session* kasutab
  `CREATE TEMPORARY TABLE` ega puuduta skeemi **Work Schema**. *Standard* vajab ainult
  lugemisõigust.
- **Serverless-warehouse'id töötavad** samamoodi; erineb ainult `HTTPPath`.

---

## 6. Draiveri kontrollimine (valikuline) {: #6-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et draiver, warehouse ja token töötavad, enne kui need
*dignasse* sisestate.

#### Samm 1
![Samm 1](images/databricks/create_odbc_data_source_step1.png)

#### Samm 2
![Samm 2](images/databricks/create_odbc_data_source_step2.png)

#### Samm 3
![Samm 3](images/databricks/create_odbc_data_source_step3.png)

#### Samm 4
![Samm 4](images/databricks/create_odbc_data_source_step4.png)

#### Samm 5 – ühenduse testimine

Klõpsake nuppu **TEST**. Õnnestunud ühendus peaks välja nägema selline:

![Samm 5](images/databricks/create_odbc_data_source_step5.png)

Siin sisestatud host, HTTP-tee ja token on täpselt need väärtused, mida võtavad
[jaotise 3](#3-odbc-properties) atribuudid.