---
title: Oracle-connector – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till Oracle via ODBC med en DSN-lös anslutningssträng. Omfattar Oracles ODBC-drivrutin, connect descriptorn i DBQ, TNS-alias och anslutningsinställningarna i digna.
image: /assets/logo_square.png
---


# Källconnector för Oracle

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Oracle Database via **ODBC**
med en **DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Oracle.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Oracles ODBC-drivrutin ingår i **Oracle Client** (Instant Client-paketet "ODBC" räcker).
Installera den på maskinen som kör *digna*-backenden enligt leverantörens
officiella installationsguide.

Drivrutinen registrerar sig som **Oracle in `<OracleHomeName>`** — till exempel
`Oracle in OraDB21Home1` eller `Oracle in instantclient_21_13`. Home-namnet skiljer sig mellan
installationer, så läs av det exakta namnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör Oracles
    ODBC-drivrutin, så deras namn, standardvärden och tillåtna värden skiljer sig mellan klientversioner,
    och särskilt drivrutinsnamnet beror på Oracle home på din värd. Använd detta som
    utgångspunkt och läs dokumentationen för den klientversion du har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Databasen att ansluta till — se nedan |
| `UID` | `DIGNA_SOURCE_USER` | Databasanvändare |
| `PWD` | `<password>` | Kryssa i **Encrypted** |

Den resulterande anslutningssträngen ser ut så här:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### Värdet för `DBQ`

`DBQ` accepterar tre former. De är likvärdiga för *digna*; de skiljer sig i vad som måste
konfigureras på *digna*-värden:

| Form | Exempel | Kräver |
|---|---|---|
| **Fullständig connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Ingenting — allt finns i egenskapen. Rekommenderas |
| **TNS-alias** | `DIGNA_SOURCE` | Aliaset måste finnas i `tnsnames.ora` för Oracle Client på *digna*-värden |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | En Oracle Client som stöder Easy Connect (12c och senare) |

!!! tip "Föredra den fullständiga descriptorn"

    Ett TNS-alias flyttar halva anslutningsdefinitionen till en fil på *digna*-värden, där
    den lätt glöms bort när värden byggs om eller *digna* flyttas. Den fullständiga descriptorn håller
    anslutningen självständig — vilket är hela poängen med en DSN-lös konfiguration.

Observera att parenteserna i en descriptor fungerar bra i en anslutningssträng, men om ditt lösenord
innehåller `;`, omge det med klammerparenteser: `PWD={p@ss;word}`.

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Att tänka på med Oracle {: #4-notes-on-oracle }

- **Scheman är användare.** *digna* listar Oracle-användare som scheman, så källschemat är
  ägaren av tabellerna — `DIGNA_SOURCE_USER` i exemplet ovan. Anslutningens användare behöver
  `SELECT` på dessa tabeller, antingen direkt eller via en roll.
- **En anslutning ser en databas.** Katalogen som *digna* erbjuder är den databas som
  anslutningen är kopplad till, så `DBQ` avgör vilken tjänst, och därmed vilken databas, som
  profileras.
- **Identifierare är skiftlägeskänsliga när de citeras.** *digna* citerar de namn den läser från
  datakatalogen, vilket är det som Oracle lagrar — versaler för objekt som inte skapats inom citattecken.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema**, så användaren
  behöver `CREATE TABLE` där och en kvot på tablespacet. *Session* använder en privat temporär
  tabell (`ORA$PTT_…`, Oracle 18c och senare) och rör inte **Work Schema**. *Standard*
  kräver endast läsbehörighet.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att Oracle Client, tjänstnamnet och dina
inloggningsuppgifter fungerar innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Det **TNS Service Name** som erbjuds här kommer från `tnsnames.ora` i din Oracle Client-installation
— det är där aliaset, och därmed värd, port och tjänstnamn, är
definierat. I *digna* kan du använda aliaset som `DBQ`, eller den fullständiga descriptorn i stället.

#### Steg 2 – Testa anslutningen

Klicka på knappen **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Ange lösenordet och klicka på knappen **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Ett bekräftelsemeddelande visar att drivrutinen och inloggningsuppgifterna fungerar.
