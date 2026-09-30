# Källconnector för Databricks

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Databricks via **ODBC** med en
**DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Databricks.

!!! note "Unity Catalog krävs"

    *digna* läser de tillgängliga katalogerna från `system.information_schema.catalogs`, så
    arbetsytan måste ha Unity Catalog aktiverat. Tidigare *digna*-releaser erbjöd en separat
    teknik, "Databricks Legacy", för arbetsytor utan Unity Catalog; den är inte längre
    tillgänglig.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera **Databricks ODBC Driver** på maskinen som kör *digna*-backenden enligt
[Databricks installationsguide](https://docs.databricks.com/aws/en/integrations/odbc/).

Beroende på version registrerar drivrutinen sig som **Simba Spark ODBC Driver** eller som
**Databricks ODBC Driver**. Läs av det exakta registrerade namnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. Samla in anslutningsuppgifterna {: #2-gather-the-connection-details }

Alla värden kommer från det SQL-warehouse (eller kluster) som du vill att *digna* ska använda. Öppna det i
Databricks-arbetsytan och gå till **Connection details**:

| Fält i Databricks | Används som |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalt `443` |
| **HTTP path** | `HTTPPath` |

För autentisering, skapa en **personlig åtkomsttoken** (personal access token) — se
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Token tillhör en användare eller ett service principal, och det kontot behöver `USE CATALOG`,
`USE SCHEMA` och `SELECT` på källdata.

---

## 3. ODBC-egenskaper {: #3-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    Databricks/Simba-drivrutinen, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner — drivrutinen har bytt namn och fått utökade autentiseringsalternativ mer än
    en gång — och mellan plattformar. Använd detta som utgångspunkt och läs dokumentationen för
    den drivrutinsversion du har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `Host` | `<workspace>.cloud.databricks.com` | Warehousets server hostname, t.ex. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP-sökvägen för warehouset eller klustret |
| `SSL` | `1` | Databricks-endpoints stöder endast TLS |
| `ThriftTransport` | `2` | HTTP-transport, vilket är vad SQL-endpoints använder |
| `AuthMech` | `3` | Tokenautentisering |
| `UID` | `token` | Det bokstavliga ordet `token`, inte ett användarnamn |
| `PWD` | `dapi…` | Den personliga åtkomsttoken. Kryssa i **Encrypted** |
| `UseNativeQuery` | `1` | Skickar *dignas* SQL oförändrad — se nedan |

Den resulterande anslutningssträngen ser ut så här:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Behåll `UseNativeQuery=1`"

    Med `UseNativeQuery=0` — drivrutinens standardvärde — skriver drivrutinen om inkommande SQL till det
    den anser vara portabel ODBC-syntax. *digna* genererar redan Databricks SQL, så
    omskrivningen kan ändra citering med backticks och datumliteraler, och profileringen misslyckas då på
    satser som är giltiga som de är skrivna.

### OAuth i stället för en token

För ett service principal med OAuth-autentisering maskin-till-maskin, ersätt `AuthMech`,
`UID` och `PWD` med:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Kryssa i **Encrypted** |

---

## 4. *digna*-konfiguration {: #4-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Att tänka på med Databricks {: #5-notes-on-databricks }

- **Warehouset måste vara igång**, eller kunna starta, när *digna* ansluter. Ett warehouse som
  startar från stoppat läge kan ta längre tid än anslutningstimeouten — om testet misslyckas
  vid första försöket efter en period av inaktivitet, försök igen.
- **Katalogerna kommer från arbetsytan.** Till skillnad från de flesta tekniker når en Databricks-anslutning
  alla kataloger som kontot har behörighet att se, så en enda anslutning kan betjäna
  källor i flera kataloger.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema** i
  källans katalog, så kontot behöver `CREATE TABLE` där. *Session* använder
  `CREATE TEMPORARY TABLE` och rör inte **Work Schema**. *Standard* kräver endast läsbehörighet.
- **Serverlösa warehouses fungerar** på samma sätt; endast `HTTPPath` skiljer sig.

---

## 6. Verifiera drivrutinen (valfritt) {: #6-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att drivrutinen, warehouset och token fungerar
innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Steg 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Steg 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Steg 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Steg 5 – Testa anslutningen

Klicka på knappen **TEST**. En lyckad anslutning ska se ut så här:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

Värden, HTTP-sökvägen och token som anges här är exakt de värden som egenskaperna i
[avsnitt 3](#3-odbc-properties) tar.