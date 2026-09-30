---
title: Azure Synapse-connector – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till Azure Synapse Analytics via ODBC med en DSN-lös anslutningssträng. Stöder serverlösa och dedikerade SQL-pooler, med de ODBC-egenskaper som krävs och anslutningsinställningarna i digna.
image: /assets/logo_square.png
---


# Källconnector för Azure Synapse Analytics

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Azure Synapse Analytics via
**ODBC** med en **DSN-lös** anslutningssträng. Både serverlösa och dedikerade SQL-pooler
stöds.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Azure Synapse.

!!! note "Teknik"

    Synapse använder SQL Server-dialekten, så anslutningen skapas med **Technology:
    SQL Server**. Se [MS SQL Server](sqlserver_connector_guide.md) för en lokal server.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera **ODBC Driver 18 for SQL Server** på maskinen som kör *digna*-backenden
enligt [Microsofts installationsguide](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
och läs av det exakta registrerade drivrutinsnamnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    Microsofts ODBC-drivrutin, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner och plattformar, och vad arbetsytan kräver beror på hur den är konfigurerad —
    pooltyp, autentiseringsmetod, brandvägg. Använd detta som utgångspunkt och läs
    dokumentationen för den drivrutinsversion du har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Arbetsytans namn plus endpoint-suffixet — se nedan |
| `DATABASE` | `dignadata` | Databasen som innehåller källschemana. Det är den enda databas som denna anslutning kan profilera |
| `UID` | `sqladminuser` | SQL-inloggning |
| `PWD` | `<password>` | Kryssa i **Encrypted** |

Den resulterande anslutningssträngen ser ut så här:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Värdet för `SERVER`

Ta namnet på Synapse-arbetsytan och lägg till endpoint-suffixet:

| Pool | `SERVER` |
|---|---|
| **Serverlös SQL-pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedikerad SQL-pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Delen `-ondemand` är lätt att missa"

    Utan den pekar namnet på den dedikerade endpointen, och anslutningen misslyckas antingen eller
    når i tysthet en annan pool än avsett. Båda endpoints visas på arbetsytans
    översiktssida i Azure-portalen.

### Brandvägg

Brandväggen för Synapse-arbetsytan måste tillåta den utgående adressen för *digna*-värden. Lägg till den
under **Networking** i arbetsytan innan du testar anslutningen — en blockerad adress visar sig
som en anslutningstimeout snarare än ett autentiseringsfel.

### Autentisering med Microsoft Entra ID

I stället för en SQL-inloggning kan drivrutinen autentisera mot Entra ID. Ersätt `UID`/`PWD` med
den autentiseringsmetod som din arbetsyta förväntar sig, till exempel:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` tar då applikationens (klientens) ID och `PWD` klienthemligheten |
| `Authentication` | `ActiveDirectoryMSI` | Hanterad identitet för *digna*-värden, inga inloggningsuppgifter behövs |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Att tänka på med Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverlösa pooler stöder endast profileringsläget *Standard*.** En serverlös SQL-pool kan inte skapa
  tabeller i en databas, så varken *Permanent* eller *Session* kan köras. *Standard*
  beräknar mätvärdena direkt på källan, vilket också är det billigare alternativet, eftersom
  serverlöst debiteras per mängd bearbetade data.
- **En anslutning ser en databas.** *digna* erbjuder schemana i den databas som anges i
  `DATABASE`, eftersom Synapse, liksom SQL Server, bara rapporterar den aktuella databasen som katalog.
- **Kryptering är på som standard** i Driver 18, och Synapse-endpoints har giltiga publika
  certifikat, så ingen egenskap `Encrypt` eller `TrustServerCertificate` behövs.
- **En serverlös endpoint kan behöva vakna från viloläge** vid första anslutningen. Om anslutningstestet
  får timeout mot en pool som inte har använts på ett tag, försök igen.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen guide är ett bekvämt sätt att bekräfta att drivrutinen fungerar och att arbetsytan accepterar
dina inloggningsuppgifter innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Fyll i fältet "Server".
Använd namnet på Synapse-arbetsytan och lägg till ".sql.azuresynapse.net".  
**Observera**: om du vill ansluta via en serverlös SQL-pool, se till att inkludera
"-ondemand" som i skärmbilden ovan.

Klicka på knappen **Next >**.

#### Steg 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Välj autentiseringsmetod (t.ex. användarnamn och lösenord)
och ange de uppgifter som krävs.

Klicka på knappen **Next >**.

#### Steg 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Välj de ANSI-kompatibla inställningarna och klicka sedan på knappen **Next >**.

#### Steg 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Du kan behålla standardinställningarna eller välja alternativ efter behov
och klicka på knappen **Finish**.

#### Steg 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klicka nu på knappen **Test datasource**.

#### Steg 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

En bekräftelseskärm visar att drivrutinen, endpointen och inloggningsuppgifterna fungerar. Värdena
du angav är exakt de värden som egenskaperna i [avsnitt 2](#2-odbc-properties) tar.
