# Lähtekonnektor MS SQL Serveri jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Microsoft SQL Serveriga **ODBC**
kaudu, kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb SQL Serveri eripärasid.

!!! note "Azure Synapse Analytics"

    Ka Synapse konfigureeritakse SQL Serveri ühendusena, erineva hostinime ja mõne lisakaalutlusega
    — vt [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage **ODBC Driver 18 for SQL Server** masinale, kus töötab *digna* backend, järgides
[Microsofti paigaldusjuhendit](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Windowsiga kaasas olev draiver lihtsa nimega **SQL Server** töötab samuti, kuid see on ammu
aegunud ega toeta ei kaasaegseid TLS-i sätteid ega Azure'i autentimist. Kasutage seda ainult
siis, kui praeguse draiveri paigaldamine pole võimalik.

Lugege oma hostist välja täpne registreeritud draiveri nimi, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Microsofti ODBC draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused draiveri versioonide vahel — näiteks Driver 18 krüpteerib vaikimisi, Driver 17
    mitte — ning platvormide vahel. Kasutage seda lähtepunktina ja kontrollige paigaldatud
    draiveriversiooni dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `SERVER` | `sql.example.com` | Serveri nimi või IP-aadress. Nimega eksemplarid: `host\instance`; mittevaikimisi port: `host,1433` |
| `PORT` | `1433` | Jätke ära, kui port on juba osa väärtusest `SERVER` |
| `DATABASE` | `digna_source_db` | Andmebaas, mis sisaldab lähteskeeme. See on ainus andmebaas, mida see ühendus saab profileerida |
| `UID` | `digna_source_user` | Andmebaasi kasutaja |
| `PWD` | `<password>` | Märkige **Encrypted** |

Tulemuseks olev ühendusstring näeb välja selline:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Krüpteerimine draiveriga ODBC Driver 18

Driver 18 krüpteerib ühendused vaikimisi ja valideerib serveri sertifikaadi. Serveri puhul,
mille sertifikaati teie *digna* host ei usalda — tavaliselt iseallkirjastatud sertifikaat —,
ebaõnnestub ühendumine sertifikaadiahela veaga. Lisage:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Encrypt` | `yes` | Driver 18 vaikeväärtus; määrake `no` ainult siis, kui server ei toeta TLS-i |
| `TrustServerCertificate` | `yes` | Jätab sertifikaadi valideerimise vahele. Mugav testkeskkondades; tootmises eelistage sertifikaadi paigaldamist |

### Windowsi autentimine

Et ühenduda SQL-sisselogimise asemel kontona, mis käitab *digna* teenust, eemaldage `UID` ja
`PWD` ning lisage:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Trusted_Connection` | `yes` | *digna* teenusekontol peavad olema andmebaasiõigused |

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Märkused MS SQL Serveri kohta {: #4-notes-on-ms-sql-server }

- **Üks ühendus näeb üht andmebaasi.** *digna* pakub atribuudis `DATABASE` nimetatud
  andmebaasi skeeme, sest SQL Server teatab kataloogina ainult praegusest andmebaasist. Teises
  andmebaasis olevad lähtetabelid vajavad oma ühendust.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema**, seega vajab
  kasutaja seal õigust `CREATE TABLE`. *Session* kasutab kohalikke ajutisi tabeleid (`#wt_…`)
  andmebaasis `tempdb` ega puuduta skeemi **Work Schema**. *Standard* vajab ainult
  lugemisõigust.
- **`SERVER` sisaldab eksemplari ja porti.** Nimega eksemplari puhul (`host\instance`) peab
  teenus SQL Server Browser olema kättesaadav; `host,port` väldib seda.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
viisard on mugav viis veenduda, et draiver töötab ja server aktsepteerib teie mandaate, enne
kui need *dignasse* sisestate.

#### Samm 1
![Samm 1](images/sqlserver/create_odbc_data_source_step1.png)

Klõpsake nuppu **Next >**.

#### Samm 2
![Samm 2](images/sqlserver/create_odbc_data_source_step2.png)

Valige autentimismeetod (nt kasutajanimi ja parool)
ja sisestage vajalikud andmed.

Klõpsake nuppu **Next >**.

#### Samm 3
![Samm 3](images/sqlserver/create_odbc_data_source_step3.png)

Valige ANSI-ühilduvad sätted ja klõpsake seejärel nuppu **Next >**.

#### Samm 4
![Samm 4](images/sqlserver/create_odbc_data_source_step4.png)

Võite jätta vaikesätted või valida vajalikud logimisvalikud
ja klõpsata nuppu **Finish**.

#### Samm 5
![Samm 5](images/sqlserver/create_odbc_data_source_step5.png)

Nüüd klõpsake nuppu **Test datasource**.

#### Samm 6
![Samm 6](images/sqlserver/create_odbc_data_source_step6.png)

Eduekraan kinnitab, et draiver ja mandaadid töötavad. Sisestatud väärtused on täpselt need
väärtused, mida võtavad [jaotise 2](#2-odbc-properties) atribuudid.