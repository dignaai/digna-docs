# Kildeconnector for Oracle

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Oracle Database over **ODBC**,
med en **DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Oracle.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Oracle ODBC-driveren er en del av **Oracle Client** (Instant Client-pakken "ODBC" er
nok). Installer den på maskinen som kjører *digna*-backend, i henhold til leverandørens
offisielle installasjonsveiledning.

Driveren registrerer seg som **Oracle in `<OracleHomeName>`** — for eksempel
`Oracle in OraDB21Home1` eller `Oracle in instantclient_21_13`. Home-navnet varierer fra
installasjon til installasjon, så les av det nøyaktige navnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører Oracles
    ODBC-driver, så navnene, standardverdiene og de godtatte verdiene varierer mellom klientversjoner,
    og særlig drivernavnet avhenger av Oracle home på verten din. Bruk dette som et
    utgangspunkt og sjekk dokumentasjonen for klientversjonen du har installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Databasen det skal kobles til — se nedenfor |
| `UID` | `DIGNA_SOURCE_USER` | Databasebruker |
| `PWD` | `<password>` | Kryss av for **Encrypted** |

Den resulterende tilkoblingsstrengen ser slik ut:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Verdien for `DBQ`

`DBQ` godtar tre former. De er likeverdige for *digna*; forskjellen er hva som må
konfigureres på *digna*-verten:

| Form | Eksempel | Krever |
|---|---|---|
| **Fullstendig connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Ingenting — alt står i egenskapen. Anbefalt |
| **TNS-alias** | `DIGNA_SOURCE` | Aliaset må finnes i `tnsnames.ora` for Oracle Client på *digna*-verten |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | En Oracle Client som støtter Easy Connect (12c og nyere) |

!!! tip "Foretrekk den fullstendige descriptoren"

    Et TNS-alias flytter halve tilkoblingsdefinisjonen inn i en fil på *digna*-verten, der
    den er lett å glemme når verten bygges opp på nytt eller *digna* flyttes. Den fullstendige descriptoren holder
    tilkoblingen selvstendig — som er hele poenget med et DSN-løst oppsett.

Merk at parentesene i en descriptor er uproblematiske i en tilkoblingsstreng, men hvis passordet ditt
inneholder `;`, må du sette det i krøllparenteser: `PWD={p@ss;word}`.

---

## 3. *digna*-konfigurasjon {: #3-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Merknader om Oracle {: #4-notes-on-oracle }

- **Skjemaer er brukere.** *digna* viser Oracle-brukere som skjemaer, så kildeskjemaet er
  eieren av tabellene — `DIGNA_SOURCE_USER` i eksemplet ovenfor. Tilkoblingsbrukeren trenger
  `SELECT` på disse tabellene, enten direkte eller via en rolle.
- **Én tilkobling ser én database.** Katalogen *digna* tilbyr, er databasen
  tilkoblingen er knyttet til, så `DBQ` avgjør hvilken tjeneste, og dermed hvilken database, som
  profileres.
- **Identifikatorer skiller mellom store og små bokstaver når de settes i anførselstegn.** *digna* setter anførselstegn rundt navnene den leser fra
  datakatalogen (data dictionary), som er det Oracle lagrer — store bokstaver for objekter uten anførselstegn.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema**, så brukeren
  trenger `CREATE TABLE` der og en kvote på tablespacet. *Session* bruker en privat midlertidig
  tabell (`ORA$PTT_…`, Oracle 18c og nyere) og rører ikke **Work Schema**. *Standard*
  trenger bare lesetilgang.

---

## 5. Verifisere driveren (valgfritt) {: #5-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at Oracle Client, tjenestenavnet og
legitimasjonen din fungerer, før du legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/oracle/create_odbc_data_source_step1.png)

**TNS Service Name** som tilbys her, kommer fra `tnsnames.ora` i Oracle Client-installasjonen
din — det er der aliaset, og med det verten, porten og tjenestenavnet, er
definert. I *digna* kan du bruke aliaset som `DBQ`, eller den fullstendige descriptoren i stedet.

#### Trinn 2 – Test tilkoblingen

Klikk på knappen **Test Connection**.

![Trinn 2](images/oracle/create_odbc_data_source_step2.png)

Oppgi passordet og klikk på knappen **OK**.

![Trinn 3](images/oracle/create_odbc_data_source_step3.png)

En bekreftelsesmelding viser at driveren og legitimasjonen fungerer.