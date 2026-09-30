# Lähtekonnektor Hive'i jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Apache Hive'iga **ODBC** kaudu,
kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Hive'i eripärasid.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage **Cloudera ODBC Driver for Apache Hive** masinale, kus töötab *digna* backend,
järgides tootja ametlikku paigaldusjuhendit.

Lugege oma hostist välja täpne registreeritud draiveri nimi, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Cloudera Hive'i draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused draiveri versioonide ja platvormide vahel ning see, mida HiveServer2 aktsepteerib,
    sõltub täielikult klastri turvaseadistusest — autentimismehhanismist, transpordirežiimist,
    TLS-ist, lüüsist. Kasutage seda lähtepunktina ja kontrollige paigaldatud draiveriversiooni
    dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `HOST` | `hive.example.com` | HiveServer2 hostinimi või IP-aadress |
| `PORT` | `10000` | HiveServer2 port; HTTP-transpordi puhul `10001` |

Tulemuseks olev ühendusstring näeb välja selline:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentimine

Turvamata HiveServer2 aktsepteerib ülaltoodud kolme atribuuti sellisel kujul. Kui autentimine
on lubatud, lisage:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `AuthMech` | `3` | `0` autentimiseta, `2` ainult kasutajanimi, `3` kasutajanimi ja parool, `1` Kerberos |
| `UID` | `digna_source_user` | Nõutav `AuthMech` väärtuste `2` ja `3` puhul |
| `PWD` | `<password>` | Nõutav `AuthMech` väärtuse `3` puhul. Märkige **Encrypted** |

Kerberose (`AuthMech=1`) puhul vajab *digna* host lisaks kehtivat piletit või keytabi ning
draiveri dokumentatsioonis kirjeldatud atribuute `KrbHostFQDN`, `KrbServiceName` ja `KrbRealm`.

### Transport ja TLS

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `ThriftTransport` | `2` | `0` binaarne (vaikimisi, port 10000), `1` SASL, `2` HTTP (port 10001, ja see, mida Knoxi lüüs ootab) |
| `HTTPPath` | `cliservice` | Koos `ThriftTransport=2` |
| `SSL` | `1` | Kui HiveServer2 on TLS-iga turvatud |
| `Schema` | `dignadata` | Hive'i andmebaas, milles seanss algab. Valikuline — *digna* kvalifitseerib oma päringud |

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Märkused Hive'i kohta {: #4-notes-on-hive }

- **Kataloogid tulevad draiverilt.** Hive'il pole oma kataloogi, seega võtab *digna* selle,
  mida draiver teatab — tavaliselt ühe kirje nimega `HIVE` — ja loetleb Hive'i andmebaasid
  selle all skeemidena.
- **Work Schema on Hive'i andmebaas.** *Permanent* profileerimise jaoks vajab kasutaja õigust
  selles tabeleid luua ja kustutada ning aluseks olev salvestuskoht peab olema kirjutatav.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema**. *Session*
  kasutab `CREATE TEMPORARY TABLE`, mis vajab ajutisi tabeleid toetavat HiveServer2 ega
  puuduta skeemi **Work Schema**. *Standard* vajab ainult lugemisõigust ja on režiim, mille
  valida klastris, kus *dignal* pole üldse kirjutusõigust.
- **Profileerimine on päringute kogum, mitte skaneerimine.** Iga statistiku arvutab
  HiveServer2, seega peaks järjekorral, kuhu *digna* kasutaja päringuid esitab, olema
  inspekteerimisakna jaoks piisavalt mahtu.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et draiver, transpordirežiim ja teie mandaadid töötavad, enne
kui need *dignasse* sisestate.

#### Samm 1
![Samm 1](images/hive/create_odbc_data_source_step1.png)

Siinsed väljad **Host**, **Port**, **Database**, **Mechanism** ja **Thrift Transport** on
[jaotise 2](#2-odbc-properties) atribuudid `HOST`, `PORT`, `Schema`, `AuthMech` ja
`ThriftTransport`.

#### Samm 2 – ühenduse testimine

Sisestage parool ja klõpsake nuppu **Test**.

![Samm 2](images/hive/create_odbc_data_source_step2.png)

Pärast õnnestunud testi klõpsake nuppu **OK**.