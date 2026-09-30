# Kildeconnector til Oracle

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Oracle Database over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Oracle.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Oracle ODBC-driveren er en del af **Oracle Client** (Instant Client-pakken "ODBC" er
tilstrækkelig). Installer den på den maskine, der kører *digna*-backend, efter leverandørens
officielle installationsvejledning.

Driveren registrerer sig som **Oracle in `<OracleHomeName>`** — for eksempel
`Oracle in OraDB21Home1` eller `Oracle in instantclient_21_13`. Home-navnet er forskelligt fra
installation til installation, så aflæs det nøjagtige navn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører Oracle
    ODBC-driveren, så deres navne, standardværdier og accepterede værdier varierer mellem
    klientversioner, og især drivernavnet afhænger af Oracle home på din vært. Brug dette som
    udgangspunkt, og tjek dokumentationen for den klientversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Databasen, der skal oprettes forbindelse til — se nedenfor |
| `UID` | `DIGNA_SOURCE_USER` | Databasebruger |
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |

Den resulterende forbindelsesstreng ser sådan ud:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### `DBQ`-værdien

`DBQ` accepterer tre former. De er ækvivalente for *digna*; de adskiller sig i, hvad der skal
konfigureres på *digna*-værten:

| Form | Eksempel | Kræver |
|---|---|---|
| **Fuld connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Intet — alt står i egenskaben. Anbefales |
| **TNS-alias** | `DIGNA_SOURCE` | Aliasset skal findes i `tnsnames.ora` for Oracle Client på *digna*-værten |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | En Oracle Client, der understøtter Easy Connect (12c og nyere) |

!!! tip "Foretræk den fulde descriptor"

    Et TNS-alias flytter halvdelen af forbindelsesdefinitionen ind i en fil på *digna*-værten,
    hvor den let bliver glemt, når værten genopbygges, eller *digna* flyttes. Den fulde
    descriptor holder forbindelsen selvstændig — hvilket netop er meningen med en DSN-løs
    opsætning.

Bemærk, at parenteserne i en descriptor er uproblematiske i en forbindelsesstreng, men hvis din
adgangskode indeholder `;`, skal du omslutte den med krøllede parenteser: `PWD={p@ss;word}`.

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Bemærkninger om Oracle {: #4-notes-on-oracle }

- **Skemaer er brugere.** *digna* viser Oracle-brugere som skemaer, så kildeskemaet er ejeren af
  tabellerne — `DIGNA_SOURCE_USER` i eksemplet ovenfor. Forbindelsesbrugeren skal have `SELECT`
  på disse tabeller, enten direkte eller via en rolle.
- **Én forbindelse ser én database.** Det katalog, *digna* tilbyder, er den database,
  forbindelsen er tilknyttet, så `DBQ` afgør, hvilken service, og dermed hvilken database, der
  profileres.
- **Identifikatorer skelner mellem store og små bogstaver, når de er citeret.** *digna* citerer
  de navne, den læser fra datakataloget, og det er dem, Oracle gemmer — med store bogstaver for
  objekter uden anførselstegn.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema**, så
  brugeren skal have `CREATE TABLE` der og en kvote på tablespacet. *Session* bruger en privat
  midlertidig tabel (`ORA$PTT_…`, Oracle 18c og nyere) og rører ikke **Work Schema**. *Standard*
  kræver kun læseadgang.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at Oracle Client, servicenavnet og dine
legitimationsoplysninger virker, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/oracle/create_odbc_data_source_step1.png)

Det **TNS Service Name**, der tilbydes her, kommer fra `tnsnames.ora` i din Oracle
Client-installation — det er der, aliasset og dermed vært, port og servicenavn er defineret. I
*digna* kan du bruge aliasset som `DBQ` eller i stedet den fulde descriptor.

#### Trin 2 – Test forbindelsen

Klik på knappen **Test Connection**.

![Trin 2](images/oracle/create_odbc_data_source_step2.png)

Angiv adgangskoden, og klik på knappen **OK**.

![Trin 3](images/oracle/create_odbc_data_source_step3.png)

En bekræftelsesmeddelelse viser, at driveren og legitimationsoplysningerne virker.