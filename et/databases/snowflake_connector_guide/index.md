# Lähtekonnektor Snowflake'i jaoks

See juhend kirjeldab, kuidas konfigureerida *digna* ühenduma Snowflake'iga **ODBC** kaudu,
kasutades **DSN-ita** ühendusstringi.

Seadistuse *digna* pool on iga tehnoloogia puhul sama — kus ühendused luuakse, kuidas
atribuutide väärtused krüpteeritakse, kuidas ühendust testitakse ja mida profileerimisrežiimid
tähendavad. Seda kirjeldatakse lehel [Andmebaasiühenduste ülevaade](overview.md). See leht
käsitleb Snowflake'i eripärasid.

---

## 1. ODBC draiveri paigaldamine {: #1-install-the-odbc-driver }

Paigaldage **Snowflake ODBC Driver** masinale, kus töötab *digna* backend, järgides
[Snowflake'i paigaldusjuhendit](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Draiver registreerib end nime all **SnowflakeDSIIDriver**. Lugege täpne registreeritud nimi
oma hostist välja, nagu on kirjeldatud jaotises
[ODBC draiveri paigaldamine digna hostile](overview.md#install-the-driver).

---

## 2. ODBC atribuudid {: #2-odbc-properties }

Snowflake'iga ühendutakse **programmaatilise juurdepääsu tokeniga (PAT)** — see on
autentimisviis, mille vastu *dignat* on kontrollitud, ja see, mida Snowflake nõuab kontodel,
kus ainult parooliga sisselogimine on blokeeritud.

!!! important "Näide, mitte spetsifikatsioon"

    Allolev komplekt on üks kombinatsioon, mis teadaolevalt töötab. Atribuudid kuuluvad
    Snowflake'i ODBC draiverile, seega erinevad nende nimed, vaikeväärtused ja
    aktsepteeritavad väärtused draiveri versioonide ja platvormide vahel ning see, milliseid
    autentimisvalikuid teie konto lubab, määrab konto turvapoliitika. Kasutage seda
    lähtepunktina ja kontrollige paigaldatud draiveriversiooni dokumentatsiooni.

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Peab vastama *digna* hostis registreeritud draiveri nimele |
| `Server` | `<account>.snowflakecomputing.com` | Konto identifikaator pluss järelliide, nt `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake'i kasutaja, kellele token kuulub |
| `Database` | `TEST` | Andmebaas, mis sisaldab lähteskeeme. See on ainus andmebaas, mida see ühendus saab profileerida |
| `Schema` | `PUBLIC` | Seansi vaikeskeem |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Valib tokeniga autentimise |
| `token` | `<programmatic access token>` | Märkige **Encrypted** |

Tulemuseks olev ühendusstring näeb välja selline:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse ja roll

Päringud vajavad warehouse'i. Kui *digna* kasutajal on vaikimisi warehouse ja vaikeroll,
võtab seanss need kasutusele ja midagi pole vaja konfigureerida. Vastasel juhul lisage:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse, mis käitab profileerimispäringuid |
| `Role` | `DIGNA_READER` | Roll, mille õigusi seanss kasutab |

!!! tip "Andke dignale oma warehouse"

    Eraldi väike, automaatselt peatuv warehouse hoiab profileerimise kulud nähtaval ja takistab
    *dignal* interaktiivsete kasutajatega arvutusressursi pärast konkureerimast.

### Parooliga autentimine

Kui konto seda veel lubab, töötab tokeni asemel parool — eemaldage `authenticator` ja `token`
ning lisage:

| Võti | Näidisväärtus | Märkused |
|---|---|---|
| `PWD` | `<password>` | Märkige **Encrypted** |

---

## 3. *digna* konfiguratsioon {: #3-digna-configuration }

Sisestage kuval **Add DB Connection** järgmine:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Märkused Snowflake'i kohta {: #4-notes-on-snowflake }

- **Tokenid aeguvad.** Programmaatilise juurdepääsu token väljastatakse kindla elueaga ja
  profileerimine peatub päeval, mil see aegub. Pange token luues aegumiskuupäev kirja ja
  sisestage uus token atribuuti `token` — krüpteeritud väärtusi saab asendada, kuid mitte
  tagasi lugeda.
- **Üks ühendus näeb üht andmebaasi.** *digna* pakub atribuudis `Database` nimetatud
  andmebaasi skeeme, sest Snowflake teatab kataloogina ainult praegusest andmebaasist. Teises
  andmebaasis olevad lähtetabelid vajavad oma ühendust.
- **Identifikaatorid on suurtähtedega**, välja arvatud juhul, kui need loodi jutumärkides.
  *digna* kasutab nimesid nii, nagu Snowflake neist teatab.
- **Profileerimisrežiimid.** *Permanent* loob töötabelid skeemi **Work Schema**, seega vajab
  roll seal õigust `CREATE TABLE`. *Session* kasutab `CREATE TEMPORARY TABLE` ega puuduta
  skeemi **Work Schema**. *Standard* vajab ainult lugemisõigust — ja üldse mitte
  kirjutusõigusi.

---

## 5. Draiveri kontrollimine (valikuline) {: #5-verifying-the-driver-optional }

DSN-ita ühenduse jaoks pole ODBC andmeallika konfigureerimine vajalik, kuid draiveri enda
dialoog on mugav viis veenduda, et draiver, konto URL ja teie mandaadid töötavad, enne kui need
*dignasse* sisestate.

#### Samm 1
![Samm 1](images/snowflake/create_odbc_data_source_step1.png)

Märkused:

- Välja **Server** väärtus koosneb teie Snowflake'i konto identifikaatorist, millele järgneb
  `.snowflakecomputing.com`.
- Siin sisestatud **Database**, **Schema** ja **Warehouse** vastavad
  [jaotise 2](#2-odbc-properties) atribuutidele `Database`, `Schema` ja `Warehouse`.

#### Samm 2 – ühenduse testimine

Klõpsake nuppu **TEST**. Õnnestunud ühendus peaks välja nägema selline:

![Samm 2](images/snowflake/create_odbc_data_source_step2.png)