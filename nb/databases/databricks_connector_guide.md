# Kildeconnector for Databricks

Denne veiledningen beskriver hvordan du konfigurerer *digna* til å koble til Databricks over **ODBC**, med en
**DSN-løs** tilkoblingsstreng.

*digna*-siden av oppsettet er den samme for alle teknologier — hvor tilkoblinger opprettes,
hvordan egenskapsverdier krypteres, hvordan en tilkobling testes og hva profileringsmodusene
betyr. Den er beskrevet i [Oversikt over databasetilkoblinger](overview.md). Denne siden dekker det
som er spesifikt for Databricks.

!!! note "Unity Catalog er påkrevd"

    *digna* leser de tilgjengelige katalogene fra `system.information_schema.catalogs`, så
    arbeidsområdet må ha Unity Catalog aktivert. Tidligere *digna*-versjoner tilbød en egen
    teknologi, "Databricks Legacy", for arbeidsområder uten Unity Catalog; den er ikke lenger
    tilgjengelig.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **Databricks ODBC Driver** på maskinen som kjører *digna*-backend, i henhold til
[Databricks' installasjonsveiledning](https://docs.databricks.com/aws/en/integrations/odbc/).

Avhengig av versjonen registrerer driveren seg som **Simba Spark ODBC Driver** eller som
**Databricks ODBC Driver**. Les av det nøyaktige registrerte navnet på verten din som beskrevet i
[Installer ODBC-driveren på digna-verten](overview.md#install-the-driver).

---

## 2. Samle inn tilkoblingsdetaljene {: #2-gather-the-connection-details }

Alle verdier kommer fra SQL warehouse (eller clusteret) du vil at *digna* skal bruke. Åpne det i
Databricks-arbeidsområdet og gå til **Connection details**:

| Databricks-felt | Brukes som |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, vanligvis `443` |
| **HTTP path** | `HTTPPath` |

For autentisering oppretter du et **personal access token** — se
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokens tilhører en bruker eller en service principal, og denne principalen trenger `USE CATALOG`,
`USE SCHEMA` og `SELECT` på kildedataene.

---

## 3. ODBC-egenskaper {: #3-odbc-properties }

!!! important "Et eksempel, ikke en spesifikasjon"

    Settet nedenfor er én kombinasjon som er kjent for å fungere. Egenskapene tilhører
    Databricks/Simba-driveren, så navnene, standardverdiene og de godtatte verdiene varierer mellom
    driverversjoner — driveren har skiftet navn og fått utvidede autentiseringsalternativer mer enn
    én gang — og mellom plattformer. Bruk dette som et utgangspunkt og sjekk dokumentasjonen for
    driverversjonen du har installert.

Legg til følgende egenskaper i skjermbildet **Add DB Connection**:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Må samsvare med drivernavnet som er registrert på *digna*-verten |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname for warehouse, f.eks. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP-banen til warehouse eller clusteret |
| `SSL` | `1` | Databricks-endepunkter støtter bare TLS |
| `ThriftTransport` | `2` | HTTP-transport, som er det SQL-endepunktene bruker |
| `AuthMech` | `3` | Token-autentisering |
| `UID` | `token` | Selve ordet `token`, ikke et brukernavn |
| `PWD` | `dapi…` | Personal access token. Kryss av for **Encrypted** |
| `UseNativeQuery` | `1` | Sender *digna*s SQL videre uendret — se nedenfor |

Den resulterende tilkoblingsstrengen ser slik ut:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Behold `UseNativeQuery=1`"

    Med `UseNativeQuery=0` — driverens standard — skriver driveren om innkommende SQL til det
    den mener er portabel ODBC-syntaks. *digna* genererer allerede Databricks SQL, så
    omskrivingen kan endre backtick-sitering og datolitteraler, og profileringen feiler da på
    setninger som er gyldige slik de er skrevet.

### OAuth i stedet for et token

For en service principal med OAuth machine-to-machine-autentisering erstatter du `AuthMech`,
`UID` og `PWD` med:

| Key | Eksempelverdi | Merknader |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Kryss av for **Encrypted** |

---

## 4. *digna*-konfigurasjon {: #4-digna-configuration }

I skjermbildet **Add DB Connection** oppgir du følgende:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Merknader om Databricks {: #5-notes-on-databricks }

- **Warehouse må kjøre**, eller kunne starte, når *digna* kobler til. Et warehouse som
  starter fra stoppet tilstand, kan bruke lenger tid enn tidsavbruddet for tilkoblingen — hvis testen feiler
  på første forsøk etter en periode uten aktivitet, prøv igjen.
- **Kataloger kommer fra arbeidsområdet.** I motsetning til de fleste teknologier når én Databricks-tilkobling
  alle kataloger principalen har lov til å se, så én enkelt tilkobling kan betjene
  kilder på tvers av kataloger.
- **Profileringsmoduser.** *Permanent* oppretter arbeidstabellene i **Work Schema** i
  kildens katalog, så principalen trenger `CREATE TABLE` der. *Session* bruker
  `CREATE TEMPORARY TABLE` og rører ikke **Work Schema**. *Standard* trenger bare
  lesetilgang.
- **Serverless warehouses fungerer** på samme måte; bare `HTTPPath` er forskjellig.

---

## 6. Verifisere driveren (valgfritt) {: #6-verifying-the-driver-optional }

Det er ikke nødvendig å konfigurere en ODBC-datakilde for en DSN-løs tilkobling, men driverens
egen dialogboks er en praktisk måte å bekrefte at driveren, warehouse og tokenet fungerer,
før du legger dem inn i *digna*.

#### Trinn 1
![Trinn 1](images/databricks/create_odbc_data_source_step1.png)

#### Trinn 2
![Trinn 2](images/databricks/create_odbc_data_source_step2.png)

#### Trinn 3
![Trinn 3](images/databricks/create_odbc_data_source_step3.png)

#### Trinn 4
![Trinn 4](images/databricks/create_odbc_data_source_step4.png)

#### Trinn 5 – Test tilkoblingen

Klikk på knappen **TEST**. En vellykket tilkobling skal se slik ut:

![Trinn 5](images/databricks/create_odbc_data_source_step5.png)

Verten, HTTP-banen og tokenet du legger inn her, er nøyaktig de verdiene egenskapene i
[avsnitt 3](#3-odbc-properties) skal ha.