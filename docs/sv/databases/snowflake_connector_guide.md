---
title: Snowflake-connector – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till Snowflake via ODBC med en DSN-lös anslutningssträng. Omfattar Snowflakes ODBC-drivrutin, programmatic access tokens, val av warehouse och roll samt anslutningsinställningarna i digna.
image: /assets/logo_square.png
---


# Källconnector för Snowflake

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Snowflake via **ODBC** med en
**DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Snowflake.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera **Snowflake ODBC Driver** på maskinen som kör *digna*-backenden enligt
[Snowflakes installationsguide](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Drivrutinen registrerar sig som **SnowflakeDSIIDriver**. Läs av det exakta registrerade namnet på din
värd enligt beskrivningen i [Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

Snowflake nås med en **programmatic access token (PAT)** — den autentiseringsväg som
*digna* verifieras mot, och den som Snowflake kräver för konton där
inloggning med enbart lösenord är blockerad.

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    Snowflakes ODBC-drivrutin, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner och plattformar, och vilka autentiseringsalternativ ditt konto tillåter avgörs av
    kontots säkerhetspolicy. Använd detta som utgångspunkt och läs dokumentationen för
    den drivrutinsversion du har installerat.

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `Server` | `<account>.snowflakecomputing.com` | Kontoidentifierare plus suffixet, t.ex. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Den Snowflake-användare som token tillhör |
| `Database` | `TEST` | Databasen som innehåller källschemana. Det är den enda databas som denna anslutning kan profilera |
| `Schema` | `PUBLIC` | Sessionens standardschema |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Väljer tokenautentisering |
| `token` | `<programmatic access token>` | Kryssa i **Encrypted** |

Den resulterande anslutningssträngen ser ut så här:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse och roll

Frågor behöver ett warehouse. Om *digna*-användaren har ett standard-warehouse och en standardroll
använder sessionen dem och ingenting behöver konfigureras. Annars, lägg till:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse som kör profileringsfrågorna |
| `Role` | `DIGNA_READER` | Roll vars behörigheter sessionen använder |

!!! tip "Ge digna ett eget warehouse"

    Ett separat, litet warehouse som pausas automatiskt håller profileringskostnaden synlig och förhindrar att
    *digna* konkurrerar med interaktiva användare om beräkningskapacitet.

### Lösenordsautentisering

Där kontot fortfarande tillåter det fungerar ett lösenord i stället för token — ta bort `authenticator`
och `token` och lägg till:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `PWD` | `<password>` | Kryssa i **Encrypted** |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Att tänka på med Snowflake {: #4-notes-on-snowflake }

- **Token går ut.** En programmatic access token utfärdas med en livslängd, och profileringen upphör
  den dag den löper ut. Anteckna utgångsdatumet när du skapar den, och ange den nya token i
  egenskapen `token` — krypterade värden kan ersättas men inte läsas tillbaka.
- **En anslutning ser en databas.** *digna* erbjuder schemana i den databas som anges i
  `Database`, eftersom Snowflake bara rapporterar den aktuella databasen som katalog. Källtabeller i
  en annan databas behöver en egen anslutning.
- **Identifierare skrivs med versaler** om de inte skapades inom citattecken. *digna* använder namnen så som
  Snowflake rapporterar dem.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema**, så rollen behöver
  `CREATE TABLE` där. *Session* använder `CREATE TEMPORARY TABLE` och rör inte
  **Work Schema**. *Standard* kräver endast läsbehörighet — och inga skrivbehörigheter alls.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att drivrutinen, konto-URL:en och dina
inloggningsuppgifter fungerar innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Noteringar:

- Värdet för **Server** består av din Snowflake-kontoidentifierare följd av
  `.snowflakecomputing.com`.
- **Database**, **Schema** och **Warehouse** som anges här motsvarar egenskaperna `Database`,
  `Schema` och `Warehouse` i [avsnitt 2](#2-odbc-properties).

#### Steg 2 – Testa anslutningen

Klicka på knappen **TEST**. En lyckad anslutning ska se ut så här:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
