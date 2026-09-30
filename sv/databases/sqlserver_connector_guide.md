# Källconnector för MS SQL Server

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Microsoft SQL Server via **ODBC**
med en **DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse konfigureras också som en SQL Server-anslutning, med ett annat värdnamn och
    några ytterligare saker att tänka på — se [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera **ODBC Driver 18 for SQL Server** på maskinen som kör *digna*-backenden
enligt [Microsofts installationsguide](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Drivrutinen som levereras med Windows under det enkla namnet **SQL Server** fungerar också, men den är
sedan länge ersatt och stöder varken moderna TLS-inställningar eller Azure-autentisering. Använd den endast
där det inte är möjligt att installera den aktuella drivrutinen.

Läs av det exakta registrerade drivrutinsnamnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    Microsofts ODBC-drivrutin, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner — Driver 18 krypterar till exempel som standard, vilket Driver 17 inte gjorde — och mellan
    plattformar. Använd detta som utgångspunkt och läs dokumentationen för den drivrutinsversion
    du har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `SERVER` | `sql.example.com` | Servernamn eller IP-adress. Namngivna instanser: `host\instance`; en port som inte är standard: `host,1433` |
| `PORT` | `1433` | Utelämna när porten redan ingår i `SERVER` |
| `DATABASE` | `digna_source_db` | Databasen som innehåller källschemana. Det är den enda databas som denna anslutning kan profilera |
| `UID` | `digna_source_user` | Databasanvändare |
| `PWD` | `<password>` | Kryssa i **Encrypted** |

Den resulterande anslutningssträngen ser ut så här:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Kryptering med ODBC Driver 18

Driver 18 krypterar anslutningar som standard och validerar servercertifikatet. Mot en
server med ett certifikat som din *digna*-värd inte litar på — typiskt ett självsignerat certifikat —
misslyckas anslutningen med ett fel i certifikatkedjan. Lägg till:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Encrypt` | `yes` | Standard i Driver 18; ange `no` endast om servern inte kan hantera TLS |
| `TrustServerCertificate` | `yes` | Hoppar över certifikatvalideringen. Praktiskt i testmiljöer; installera hellre certifikatet i produktion |

### Windows-autentisering

För att ansluta som det konto som kör *digna*-tjänsten i stället för med en SQL-inloggning, ta bort
`UID` och `PWD` och lägg till:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `Trusted_Connection` | `yes` | Tjänstekontot för *digna* behöver databasbehörigheterna |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Att tänka på med MS SQL Server {: #4-notes-on-ms-sql-server }

- **En anslutning ser en databas.** *digna* erbjuder schemana i den databas som anges i
  `DATABASE`, eftersom SQL Server bara rapporterar den aktuella databasen som katalog. Källtabeller
  i en annan databas behöver en egen anslutning.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema**, så användaren
  behöver `CREATE TABLE` där. *Session* använder lokala temporära tabeller (`#wt_…`) i `tempdb` och
  rör inte **Work Schema**. *Standard* kräver endast läsbehörighet.
- **`SERVER` innehåller instans och port.** Med en namngiven instans kräver `host\instance` att
  tjänsten SQL Server Browser kan nås; `host,port` undviker det.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen guide är ett bekvämt sätt att bekräfta att drivrutinen fungerar och att servern accepterar
dina inloggningsuppgifter innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Klicka på knappen **Next >**.

#### Steg 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Välj autentiseringsmetod (t.ex. användarnamn och lösenord)
och ange de uppgifter som krävs.

Klicka på knappen **Next >**.

#### Steg 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Välj de ANSI-kompatibla inställningarna och klicka sedan på knappen **Next >**.

#### Steg 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Du kan behålla standardinställningarna eller välja loggningsalternativ efter behov
och klicka på knappen **Finish**.

#### Steg 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Klicka nu på knappen **Test datasource**.

#### Steg 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

En bekräftelseskärm visar att drivrutinen och inloggningsuppgifterna fungerar. Värdena du angav är
exakt de värden som egenskaperna i [avsnitt 2](#2-odbc-properties) tar.