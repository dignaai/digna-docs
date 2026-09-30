# Kildeconnector til Snowflake

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til
Snowflake over **ODBC** med en **DSN-løs** forbindelsesstreng.

*digna*-delen af opsætningen er den samme for alle teknologier — hvor forbindelser oprettes,
hvordan egenskabsværdier krypteres, hvordan en forbindelse testes, og hvad profileringstilstandene
betyder. Den er beskrevet i [Oversigt over databaseforbindelser](overview.md). Denne side dækker
det, der er specifikt for Snowflake.

---

## 1. Installer ODBC-driveren {: #1-install-the-odbc-driver }

Installer **Snowflake ODBC Driver** på den maskine, der kører *digna*-backend, efter
[Snowflakes installationsvejledning](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Driveren registrerer sig som **SnowflakeDSIIDriver**. Aflæs det nøjagtige registrerede navn på
din vært som beskrevet i [Installer ODBC-driveren på digna-værten](overview.md#install-the-driver).

---

## 2. ODBC-egenskaber {: #2-odbc-properties }

Snowflake nås med et **programmatic access token (PAT)** — den autentificeringsmetode, *digna*
er verificeret med, og den, Snowflake kræver for konti, hvor login kun med adgangskode er
blokeret.

!!! important "Et eksempel, ikke en specifikation"

    Sættet nedenfor er én kombination, der vides at virke. Egenskaberne tilhører Snowflake
    ODBC-driveren, så deres navne, standardværdier og accepterede værdier varierer mellem
    driverversioner og platforme, og hvilke autentificeringsmuligheder din konto tillader,
    afgøres af kontoens sikkerhedspolitik. Brug dette som udgangspunkt, og tjek dokumentationen
    for den driverversion, du har installeret.

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Skal matche det drivernavn, der er registreret på *digna*-værten |
| `Server` | `<account>.snowflakecomputing.com` | Konto-identifikator plus suffikset, f.eks. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Den Snowflake-bruger, som tokenet tilhører |
| `Database` | `TEST` | Databasen, der indeholder kildeskemaerne. Det er den eneste database, denne forbindelse kan profilere |
| `Schema` | `PUBLIC` | Sessionens standardskema |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Vælger token-autentificering |
| `token` | `<programmatic access token>` | Sæt flueben i **Encrypted** |

Den resulterende forbindelsesstreng ser sådan ud:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse og rolle

Forespørgsler kræver et warehouse. Hvis *digna*-brugeren har et standard-warehouse og en
standardrolle, bruger sessionen dem, og der skal ikke konfigureres noget. Ellers skal du tilføje:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse, der kører profileringsforespørgslerne |
| `Role` | `DIGNA_READER` | Rolle, hvis rettigheder sessionen bruger |

!!! tip "Giv digna sit eget warehouse"

    Et separat, lille warehouse med automatisk suspendering holder profileringsomkostningerne
    synlige og forhindrer, at *digna* konkurrerer med interaktive brugere om computerkraft.

### Autentificering med adgangskode

Hvor kontoen stadig tillader det, kan en adgangskode bruges i stedet for tokenet — fjern
`authenticator` og `token`, og tilføj:

| Nøgle | Eksempelværdi | Bemærkninger |
|---|---|---|
| `PWD` | `<password>` | Sæt flueben i **Encrypted** |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

Angiv følgende på skærmen **Add DB Connection**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Bemærkninger om Snowflake {: #4-notes-on-snowflake }

- **Tokens udløber.** Et programmatic access token udstedes med en levetid, og profileringen
  stopper den dag, det udløber. Notér udløbsdatoen, når du opretter det, og indtast det nye token
  i egenskaben `token` — krypterede værdier kan erstattes, men ikke læses igen.
- **Én forbindelse ser én database.** *digna* tilbyder skemaerne i den database, der er angivet i
  `Database`, fordi Snowflake kun rapporterer den aktuelle database som katalog. Kildetabeller i
  en anden database kræver deres egen forbindelse.
- **Identifikatorer skrives med store bogstaver**, medmindre de er oprettet i anførselstegn.
  *digna* bruger navnene, som Snowflake rapporterer dem.
- **Profileringstilstande.** *Permanent* opretter arbejdstabellerne i **Work Schema**, så rollen
  skal have `CREATE TABLE` der. *Session* bruger `CREATE TEMPORARY TABLE` og rører ikke
  **Work Schema**. *Standard* kræver kun læseadgang — og slet ingen skriverettigheder.

---

## 5. Verificering af driveren (valgfrit) {: #5-verifying-the-driver-optional }

Det er ikke nødvendigt at konfigurere en ODBC-datakilde for en DSN-løs forbindelse, men
driverens egen dialog er en bekvem måde at bekræfte, at driveren, konto-URL'en og dine
legitimationsoplysninger virker, før du indtaster dem i *digna*.

#### Trin 1
![Trin 1](images/snowflake/create_odbc_data_source_step1.png)

Bemærkninger:

- Værdien for **Server** består af din Snowflake-konto-identifikator efterfulgt af
  `.snowflakecomputing.com`.
- **Database**, **Schema** og **Warehouse**, der indtastes her, svarer til egenskaberne
  `Database`, `Schema` og `Warehouse` i [afsnit 2](#2-odbc-properties).

#### Trin 2 – Test forbindelsen

Klik på knappen **TEST**. En vellykket forbindelse skal se sådan ud:

![Trin 2](images/snowflake/create_odbc_data_source_step2.png)