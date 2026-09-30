# Lähtekonnektor Oracle'i jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Oracle Database'iga **ODBC**
kaudu, kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Oracle'i eripärasid.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Oracle'i ODBC draiver on osa **Oracle Clientist** (piisab Instant Clienti paketist "ODBC").
Paigaldage see masinale, kus töötab *digna* backend, järgides tootja ametlikku
paigaldusjuhendit.

Draiver registreerib end nime all **Oracle in `<OracleHomeName>`** — näiteks
`Oracle in OraDB21Home1` või `Oracle in instantclient_21_13`. Home'i nimi erineb paigalduste
kaupa, seega lugege täpne nimi oma hostist välja, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Oracle'i ODBC draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused kliendi versioonide vahel ning eriti draiveri nimi sõltub teie hosti Oracle
    home'ist. Kasutage seda lähtepunktina ja kontrollige paigaldatud kliendiversiooni
    dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Andmebaas, millega ühenduda — vt allpool |
| `UID` | `DIGNA_SOURCE_USER` | Andmebaasi kasutaja |
| `PWD` | `<password>` | Märkige **Encrypted** |

Tulemuseks olev ühendusstring näeb välja selline:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Väärtus `DBQ`

`DBQ` aktsepteerib kolme vormi. *digna* jaoks on need samaväärsed; need erinevad selle poolest,
mida tuleb *digna* hostis konfigureerida:

| Vorm | Näide | Nõuab |
|---|---|---|
| **Täielik connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Mitte midagi — kõik on atribuudis. Soovitatav |
| **TNS-alias** | `DIGNA_SOURCE` | Alias peab olema olemas *digna* hosti Oracle Clienti failis `tnsnames.ora` |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Oracle Client, mis toetab Easy Connecti (12c ja uuemad) |

!!! tip "Eelistage täielikku descriptorit"

    TNS-alias viib poole ühenduse määratlusest *digna* hostis olevasse faili, kus see on kerge
    ununema, kui host uuesti üles ehitatakse või *digna* teise kohta viiakse. Täielik descriptor
    hoiab ühenduse iseseisvana — mis ongi DSN-ita seadistuse mõte.

Pange tähele, et descriptori sulud on ühendusstringis korras, kuid kui teie parool sisaldab
märki `;`, pange see loogelistesse sulgudesse: `PWD={p@ss;word}`.

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Märkused Oracle'i kohta {: #4-notes-on-oracle }

- **Skeemid on kasutajad.** *digna* loetleb Oracle'i kasutajad skeemidena, seega on
  lähteskeem tabelite omanik — ülaltoodud näites `DIGNA_SOURCE_USER`. Ühenduse kasutaja vajab
  nendele tabelitele õigust `SELECT` kas otse või rolli kaudu.
- **Üks ühendus näeb üht andmebaasi.** Kataloog, mida *digna* pakub, on andmebaas, millega
  ühendus on seotud, seega määrab `DBQ`, millist teenust ja seega millist andmebaasi
  profileeritakse.
- **Identifikaatorid on jutumärkides tõstutundlikud.** *digna* paneb jutumärkidesse nimed,
  mille ta loeb andmesõnastikust, st need, mida Oracle salvestab — jutumärkideta objektide
  puhul suurtähtedega.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema**, seega vajab
  kasutaja seal õigust `CREATE TABLE` ja kvooti tabeliruumis. *Session* kasutab privaatset
  ajutist tabelit (`ORA$PTT_…`, Oracle 18c ja uuemad) ega puuduta skeemi **Work Schema**.
  *Standard* vajab ainult lugemisõigust.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et Oracle Client, teenuse nimi ja teie mandaadid töötavad, enne
kui need *dignasse* sisestate.

#### Samm 1
![Samm 1](images/oracle/create_odbc_data_source_step1.png)

Siin pakutav **TNS Service Name** pärineb teie Oracle Clienti paigalduse failist
`tnsnames.ora` — seal on alias ja koos sellega host, port ja teenuse nimi määratletud.
*dignas* võite kasutada aliast väärtusena `DBQ` või selle asemel täielikku descriptorit.

#### Samm 2 – ühenduse testimine

Klõpsake nuppu **Test Connection**.

![Samm 2](images/oracle/create_odbc_data_source_step2.png)

Sisestage parool ja klõpsake nuppu **OK**.

![Samm 3](images/oracle/create_odbc_data_source_step3.png)

Eduteade kinnitab, et draiver ja mandaadid töötavad.