# Lähtekonnektor Netezza jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Netezzaga **ODBC** kaudu,
kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Netezza eripärasid.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage ODBC draiver **NetezzaSQL** (osa IBM Netezza klienditööriistadest) masinale, kus
töötab *digna* backend, järgides tootja ametlikku paigaldusjuhendit.

Lugege oma hostist välja täpne registreeritud draiveri nimi, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    NetezzaSQL draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused kliendi versioonide ja platvormide vahel ning TLS-iga turvatud seade vajab
    rohkem kui siin näidatud atribuudid. Kasutage seda lähtepunktina ja kontrollige paigaldatud
    kliendiversiooni dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Peab vastama *digna* hostis registreeritud draiveri nimele. Loogelised sulud on selle nime tavapärane kirjutusviis |
| `SERVER` | `netezza.example.com` | Serveri nimi või IP-aadress |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Andmebaas, milles seanss algab |
| `UID` | `ADMIN` | Andmebaasi kasutaja |
| `PWD` | `<password>` | Märkige **Encrypted** |

Tulemuseks olev ühendusstring näeb välja selline:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Olenevalt draiveri versioonist, seadistusest ja turvanõuetest võib vaja minna täiendavaid
atribuute — näiteks `SecurityLevel` ja `CaCertFile` TLS-iga turvatud seadme puhul. Iga valiku,
mida pakuvad draiveri dialoogid *Advanced*, *SSL* ja *Driver*, saab lisada atribuudina.

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Märkused Netezza kohta {: #4-notes-on-netezza }

- **Kehtivad nii kataloogid kui ka skeemid.** *digna* loetleb andmebaasid, mida kasutaja
  tohib näha (vaatest `_V_DATABASE`), kataloogidena ja nende skeemid (vaatest `_V_SCHEMA`)
  nende all, seega saab üks ühendus teenindada allikaid mitmes andmebaasis. `DATABASE` määrab
  ainult selle, kus seanss algab.
- **Identifikaatorid on suurtähtedega**, välja arvatud juhul, kui need loodi jutumärkides,
  mistõttu kasutavad ülaltoodud näited väärtusi `TEST` ja `ADMIN`.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema**, seega vajab
  kasutaja seal õigust `CREATE TABLE`. *Session* kasutab `CREATE TEMPORARY TABLE` ega puuduta
  skeemi **Work Schema**. *Standard* vajab ainult lugemisõigust.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et draiver ja teie mandaadid töötavad, enne kui need
*dignasse* sisestate.

#### Samm 1
![Samm 1](images/netezza/create_odbc_data_source_step1.png)

Vahekaardi **DSN Options** väljad vastavad üks-ühele [jaotise 2](#2-odbc-properties)
atribuutidele. Olenevalt teie Netezza draiverist, seadistusest ja turvanõuetest võib vaja
minna andmeid ka vahekaartidel **Advanced DSN Options**, **SSL DSN Options** või
**Driver Options**; kõige lihtsama seadistuse jaoks piisab vahekaardist **DSN Options**.

Klõpsake nuppu **Test Connection**.

#### Samm 2
![Samm 2](images/netezza/create_odbc_data_source_step2.png)

Kui kuvatakse eduekraan, draiver töötab ja väärtused on õiged.