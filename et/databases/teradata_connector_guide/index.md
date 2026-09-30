# Lähtekonnektor Teradata jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Teradataga **ODBC** kaudu,
kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Teradata eripärasid.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage **ODBC Driver for Teradata** masinale, kus töötab *digna* backend, järgides tootja
ametlikku paigaldusjuhendit.

Draiver registreerib end nimega, mis sisaldab versiooni, näiteks
**Teradata Database ODBC Driver 20.00**. Lugege täpne registreeritud nimi oma hostist välja,
nagu on kirjeldatud jaotises [ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Teradata ODBC draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused draiveri versioonide vahel — versioon on osa draiveri nimest endast — ning
    platvormide vahel. Kasutage seda lähtepunktina ja kontrollige paigaldatud
    draiveriversiooni dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `DBCNAME` | `teradata.example.com` | Serveri nimi või IP-aadress. Teradata enda nimi hosti atribuudi jaoks |
| `UID` | `digna_source_user` | Andmebaasi kasutaja |
| `PWD` | `<password>` | Märkige **Encrypted** |

Tulemuseks olev ühendusstring näeb välja selline:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Kasulikud lisaatribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `MechanismName` | `TD2` | Sisselogimismehhanism. `TD2` on Teradata vaikeväärtus; kataloogiteenuse autentimiseks kasutage `LDAP` |
| `DefaultDatabase` | `dad` | Andmebaas, milles seanss algab |
| `CharacterSet` | `UTF8` | Määrake see, kui seansi vaikimisi märgistik moonutaks mitte-ASCII andmeid |

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Märkused Teradata kohta {: #4-notes-on-teradata }

- **Teradata andmebaas on kataloog, mitte skeem.** *digna* loetleb andmebaasid, mida kasutaja
  tohib näha (vaatest `DBC.DatabasesV`), kataloogidena ja skeemi tase ei kehti. Andmeallika
  lisamisel valige andmebaas kataloogina; skeemi kohta kuvatakse *not applicable*.
- **Üks ühendus ulatub igasse lubatud andmebaasi**, seega saab üks ühendus teenindada allikaid
  mitmes andmebaasis — erinevalt tehnoloogiatest, kus ühendus on seotud ühe andmebaasiga.
- **Work Schema on andmebaas.** *Permanent* profileerimise jaoks nimetage Teradata andmebaas,
  mis hoiab töötabeleid, ning andke kasutajale selles õigus `CREATE TABLE` ja `PERM`-ruumi
  eraldis — andmebaas, mille perm-ruum on null, ei saa tabelit hoida.
- **Profileerimisrežiimid.** *Permanent* loob tabelid skeemi **Work Schema**. *Session*
  kasutab `VOLATILE` tabelit, mis vajab `SPOOL`-ruumi, kuid mitte perm-ruumi ega õigusi skeemis
  **Work Schema**. *Standard* vajab ainult lugemisõigust.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et draiver ja teie mandaadid töötavad, enne kui need
*dignasse* sisestate.

#### Samm 1
![Samm 1](images/teradata/create_odbc_data_source_step1.png)

Siinne väli **Name or IP address** on [jaotise 2](#2-odbc-properties) atribuut `DBCNAME`.

Klõpsake nuppu **Test**.

#### Samm 2
![Samm 2](images/teradata/create_odbc_data_source_step2.png)

Sisestage kasutajanimi ja parool ning klõpsake seejärel nuppu **OK**. Eduekraan kinnitab, et
draiver ja mandaadid töötavad.