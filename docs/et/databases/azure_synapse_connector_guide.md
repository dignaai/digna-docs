---
title: Azure Synapse konnektor – andmebaasi integratsioon | digna dokumentatsioon
description: Konfigureerige digna ühenduma Azure Synapse Analyticsiga ODBC kaudu DSN-ita ühendusstringiga. Toetab serverless- ja dedicated SQL-kogumeid, koos vajalike ODBC atribuutide ja digna-poolsete ühenduse sätetega.
image: /assets/logo_square.png
---


# Lähtekonnektor Azure Synapse Analyticsi jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Azure Synapse Analyticsiga
**ODBC** kaudu, kasutades **DSN-ita** ühendusstringi. Toetatud on nii serverless- kui ka
dedicated SQL-kogumid.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Azure Synapse'i eripärasid.

!!! note "Tehnoloogia"

    Synapse kasutab SQL Serveri dialekti, seega luuakse ühendus sättega **Technology:
    SQL Server**. Kohapealse serveri jaoks vt [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage **ODBC Driver 18 for SQL Server** masinale, kus töötab *digna* backend, järgides
[Microsofti paigaldusjuhendit](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
ja lugege oma hostist välja täpne registreeritud draiveri nimi, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Microsofti ODBC draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused draiveri versioonide ja platvormide vahel ning see, mida tööruum nõuab, sõltub
    selle konfiguratsioonist — kogumi tüübist, autentimismeetodist, tulemüürist. Kasutage seda
    lähtepunktina ja kontrollige paigaldatud draiveriversiooni dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Tööruumi nimi pluss lõpp-punkti järelliide — vt allpool |
| `DATABASE` | `dignadata` | Andmebaas, mis sisaldab lähteskeeme. See on ainus andmebaas, mida see ühendus saab profileerida |
| `UID` | `sqladminuser` | SQL-sisselogimine |
| `PWD` | `<password>` | Märkige **Encrypted** |

Tulemuseks olev ühendusstring näeb välja selline:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Väärtus `SERVER`

Võtke Synapse'i tööruumi nimi ja lisage sellele lõpp-punkti järelliide:

| Kogum | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Osa `-ondemand` on kerge märkamata jätta"

    Ilma selleta lahendatakse nimi dedicated-lõpp-punktiks ning ühendus kas ebaõnnestub või
    jõuab vaikselt teise kogumini, kui kavatsetud. Mõlemat lõpp-punkti näidatakse Azure'i
    portaalis tööruumi ülevaatelehel.

### Tulemüür

Synapse'i tööruumi tulemüür peab lubama *digna* hosti väljuva aadressi. Lisage see tööruumis
jaotises **Networking** enne ühenduse testimist — blokeeritud aadress ilmneb ühenduse
ajalõpuna, mitte autentimisveana.

### Microsoft Entra ID autentimine

SQL-sisselogimise asemel saab draiver autentida Entra ID vastu. Asendage `UID`/`PWD`
autentimismeetodiga, mida teie tööruum ootab, näiteks:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` võtab siis rakenduse (kliendi) ID ja `PWD` kliendi saladuse |
| `Authentication` | `ActiveDirectoryMSI` | *digna* hosti hallatud identiteet, mandaate pole vaja |

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Märkused Azure Synapse'i kohta {: #4-notes-on-azure-synapse }

- **Serverless-kogumid toetavad ainult *Standard* profileerimist.** Serverless SQL-kogum ei
  saa andmebaasis tabeleid luua, seega ei saa käivitada ei *Permanent* ega *Session*
  profileerimist. *Standard* arvutab mõõdikud otse allikal, mis on ka odavam valik, sest
  serverless-kogumit arveldatakse töödeldud andmete mahu järgi.
- **Üks ühendus näeb üht andmebaasi.** *digna* pakub atribuudis `DATABASE` nimetatud
  andmebaasi skeeme, sest Synapse, nagu SQL Server, teatab kataloogina ainult praegusest
  andmebaasist.
- **Krüpteerimine on vaikimisi sees** draiveris Driver 18 ja Synapse'i lõpp-punktid esitavad
  kehtivad avalikud sertifikaadid, seega pole atribuute `Encrypt` ega `TrustServerCertificate`
  vaja.
- **Serverless-lõpp-punkt võib esimesel ühendumisel jõudeolekust ärgata.** Kui ühenduse test
  aegub kogumi puhul, mida pole mõnda aega kasutatud, proovige uuesti.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
viisard on mugav viis veenduda, et draiver töötab ja tööruum aktsepteerib teie mandaate, enne
kui need *dignasse* sisestate.

#### Samm 1
![Samm 1](images/azure_synapse/create_odbc_data_source_step1.png)

Täitke väli "Server".
Kasutage Synapse'i tööruumi nime ja lisage sellele ".sql.azuresynapse.net".  
**Tähelepanu**: kui soovite ühenduda serverless SQL-kogumiga, lisage kindlasti
"-ondemand", nagu ülaltoodud ekraanipildil näidatud.

Klõpsake nuppu **Next >**.

#### Samm 2
![Samm 2](images/azure_synapse/create_odbc_data_source_step2.png)

Valige autentimismeetod (nt kasutajanimi ja parool)
ja sisestage vajalikud andmed.

Klõpsake nuppu **Next >**.

#### Samm 3
![Samm 3](images/azure_synapse/create_odbc_data_source_step3.png)

Valige ANSI-ühilduvad sätted ja klõpsake seejärel nuppu **Next >**.

#### Samm 4
![Samm 4](images/azure_synapse/create_odbc_data_source_step4.png)

Võite jätta vaikesätted või valida vajalikud valikud
ja klõpsata nuppu **Finish**.

#### Samm 5
![Samm 5](images/azure_synapse/create_odbc_data_source_step5.png)

Nüüd klõpsake nuppu **Test datasource**.

#### Samm 6
![Samm 6](images/azure_synapse/create_odbc_data_source_step6.png)

Eduekraan kinnitab, et draiver, lõpp-punkt ja mandaadid töötavad. Sisestatud väärtused on
täpselt need väärtused, mida võtavad [jaotise 2](#2-odbc-properties) atribuudid.
