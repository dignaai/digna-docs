# Kildeconnector til Databricks

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Databricks over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Databricks.

!!! note "Unity Catalog er påkrævet"

    *digna* læser de tilgængelige kataloger fra `system.information_schema.catalogs`, så
    workspacet skal have Unity Catalog aktiveret. Tidligere *digna*-versioner tilbød en separat
    teknologi, "Databricks Legacy", til workspaces uden Unity Catalog; den findes ikke længere.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **Databricks ODBC Driver** på den maskine, der kører *digna*-backend, efter
[Databricks' installationsvejledning](https://docs.databricks.com/aws/en/integrations/odbc/).

Afhængigt af versionen registrerer driveren sig som **Simba Spark ODBC Driver** eller som
**Databricks ODBC Driver**. Aflæs det nøjagtige registrerede navn på din vært som beskrevet i
[Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. Indsaml forbindelsesoplysningerne {: #2-gather-the-connection-details }

Alle værdier kommer fra det SQL warehouse (eller den cluster), som *digna* skal bruge. Åbn det i
Databricks-workspacet, og gå til **Connection details**:

| Databricks-felt | Bruges som |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalt `443` |
| **HTTP path** | `HTTPPath` |

Til autentificering skal du oprette et **personal access token** — se
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokens tilhører en bruger eller en service principal, og den principal skal have `USE CATALOG`,
`USE SCHEMA` og `SELECT` på kildedataene.

---

## 3. ODBC-egenskaber {: #3-odbc-properties }

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører
    Databricks/Simba-driveren, så deres navne, standardværdier og accepterede værdier varierer
    mellem driverversioner — driveren er blevet omdøbt, og dens autentificeringsmuligheder er
    udvidet mere end én gang — og mellem platforme. Brug dette som udgangspunkt, og tjek
    dokumentationen for den driverversion, du har installeret.

Tilføj følgende egenskaber på skærmen **Add DB Connection**:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `Host` | `<workspace>.cloud.databricks.com` | Warehousets server hostname, f.eks. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP path for warehouset eller clusteren |
| `SSL` | `1` | Databricks-endpoints understøtter kun TLS |
| `ThriftTransport` | `2` | HTTP-transport, som er det, SQL-endpoints taler |
| `AuthMech` | `3` | Token-autentificering |
| `UID` | `token` | Det bogstavelige ord `token`, ikke et brugernavn |
| `PWD` | `dapi…` | Personal access token. Sæt flueben i **Encrypted** |
| `UseNativeQuery` | `1` | Sender *digna*s SQL uændret videre — se nedenfor |

Den resulterende forbindelsesstreng ser sådan ud:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Behold `UseNativeQuery=1`"

    Med `UseNativeQuery=0` — driverens standard — omskriver driveren indgående SQL til det, den
    mener er portabel ODBC-syntaks. *digna* genererer allerede Databricks SQL, så omskrivningen
    kan ændre citering med backticks og datoliteraler, og profileringen fejler derefter på
    sætninger, der er gyldige, som de er skrevet.

### OAuth i stedet for et token

For en service principal med OAuth machine-to-machine-autentificering skal `AuthMech`, `UID` og
`PWD` erstattes med:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Sæt flueben i **Encrypted** |

---

## 4. *digna*-konfiguration {: #4-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Bemærkninger om Databricks {: #5-notes-on-databricks }

- **Warehouset skal køre** eller kunne starte, når *digna* opretter forbindelse. Et warehouse,
  der startes fra stoppet tilstand, kan tage længere tid end forbindelsestimeouten — hvis testen
  fejler ved første forsøg efter en inaktiv periode, så prøv igen.
- **Kataloger kommer fra workspacet.** I modsætning til de fleste teknologier når én
  Databricks-forbindelse alle kataloger, som principalen har lov til at se, så én forbindelse kan
  betjene kilder på tværs af kataloger.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema** i kildens
  katalog, så principalen skal have `CREATE TABLE` der. *Session* bruger
  `CREATE TEMPORARY TABLE` og rører ikke **Work Schema**. *Standard* kræver kun læseadgang.
- **Serverless warehouses virker** på samme måde; kun `HTTPPath` er anderledes.

---

## 6. Verificering af driveren (valgfrit) {: #6-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at driveren, warehouset og tokenet virker,
før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/databricks/create_odbc_data_source_step1.png)

#### Trin 2
![Trin 2](images/databricks/create_odbc_data_source_step2.png)

#### Trin 3
![Trin 3](images/databricks/create_odbc_data_source_step3.png)

#### Trin 4
![Trin 4](images/databricks/create_odbc_data_source_step4.png)

#### Trin 5 – Test forbindelsen

Klik på knappen **TEST**. En vellykket forbindelse skal se sådan ud:

![Trin 5](images/databricks/create_odbc_data_source_step5.png)

Den vært, HTTP path og det token, der indtastes her, er præcis de værdier, egenskaberne i
[afsnit 3](#3-odbc-properties) skal have.