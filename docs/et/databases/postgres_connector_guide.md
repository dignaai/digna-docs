---
title: PostgreSQL konnektor – andmebaasi integratsioon | digna dokumentatsioon
description: Konfigureerige digna ühenduma PostgreSQL-iga ODBC kaudu DSN-ita ühendusstringiga. Käsitleb psqlODBC draiverit, vajalikke ODBC atribuute, SSL-režiime ja digna-poolseid ühenduse sätteid.
image: /assets/logo_square.png
---


# Lähtekonnektor PostgreSQL-i jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma PostgreSQL-iga **ODBC** kaudu,
kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb PostgreSQL-i eripärasid.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage PostgreSQL-i ODBC draiver (**psqlODBC**) masinale, kus töötab *digna* backend,
järgides tootja ametlikku paigaldusjuhendit.

Draiver registreerib end nime all, mis erineb platvormi ja paketi kaupa — tavaliselt
**PostgreSQL Unicode(x64)** Windowsis ja **PostgreSQL ODBC Driver(UNICODE)** Linuxis. Lugege
täpne nimi oma hostist välja, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver), ja kasutage seda
nime allpool atribuudi `DRIVER` jaoks.

---

## 2. ODBC atribuudid {: #2-odbc-properties }

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    psqlODBC draiverile, seega erinevad nende nimed, vaikeväärtused ja aktsepteeritavad
    väärtused draiveri versioonide ja platvormide vahel ning ka see, mida teie server nõuab —
    eriti SSL —, võib erineda. Kasutage seda lähtepunktina ja kontrollige paigaldatud
    draiveriversiooni dokumentatsiooni.

Lisage kuval **Add DB Connection** järgmised atribuudid:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `SERVER` | `db.example.com` | Serveri nimi või IP-aadress |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Andmebaas, mis sisaldab lähteskeeme. See on ainus andmebaas, mida see ühendus saab profileerida |
| `UID` | `digna_source_user` | Andmebaasi kasutaja |
| `PWD` | `<password>` | Märkige **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` või `verify-full` — server peab seda aktsepteerima |

Tulemuseks olev ühendusstring näeb välja selline:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Iga täiendava psqlODBC valiku saab lisada lisaatribuudina — näiteks `ReadOnly=1` ainult
lugemiseks mõeldud seansi jaoks või `ConnSettings`, et käivitada ühendumisel `SET`-lauseid.

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Märkused PostgreSQL-i kohta {: #4-notes-on-postgresql }

- **`SSLMode` peab vastama serverile.** Server, mis on konfigureeritud kirjega `hostssl`,
  lükkab tagasi `SSLMode=disable` ning `verify-ca` või `verify-full` nõuavad lisaks, et
  juursertifikaat oleks *digna* hostis draiverile kättesaadav. Kui pidite draiveri
  testimisel valima kindla režiimi, kasutage siin sama režiimi.
- **Üks ühendus näeb üht andmebaasi.** *digna* pakub atribuudis `DATABASE` nimetatud
  andmebaasi skeeme, sest PostgreSQL teatab kataloogina ainult praegusest andmebaasist. Teises
  andmebaasis olevad lähtetabelid vajavad oma ühendust.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema**, seega vajab
  kasutaja sellele skeemile õigust `CREATE`. *Session* kasutab `CREATE TEMPORARY TABLE` ega
  puuduta skeemi **Work Schema**. *Standard* vajab ainult lugemisõigust.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et draiver töötab ning server aktsepteerib teie mandaate ja
SSL-režiimi, enne kui need *dignasse* sisestate.

#### Samm 1
![Samm 1](images/postgres/create_odbc_data_source_step1.png)

#### Samm 2 – ühenduse testimine

Klõpsake nuppu **Test Connection**.

![Samm 2](images/postgres/create_odbc_data_source_step2.png)

Siin sisestatud väärtused on täpselt need väärtused, mida võtavad
[jaotise 2](#2-odbc-properties) atribuudid.
