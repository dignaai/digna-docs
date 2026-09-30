# Källconnector för Hive

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Apache Hive via **ODBC** med en
**DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Hive.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera **Cloudera ODBC Driver for Apache Hive** på maskinen som kör *digna*-backenden
enligt leverantörens officiella installationsguide.

Läs av det exakta registrerade drivrutinsnamnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    Clouderas Hive-drivrutin, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner och plattformar, och vad HiveServer2 accepterar beror helt på hur klustret är
    säkrat — autentiseringsmekanism, transportläge, TLS, gateway. Använd detta som utgångspunkt
    och läs dokumentationen för den drivrutinsversion du har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `HOST` | `hive.example.com` | Värdnamn eller IP-adress för HiveServer2 |
| `PORT` | `10000` | Port för HiveServer2; `10001` för HTTP-transport |

Den resulterande anslutningssträngen ser ut så här:

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Autentisering

En osäkrad HiveServer2 accepterar de tre egenskaperna ovan som de är. Där autentisering
är aktiverad, lägg till:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `AuthMech` | `3` | `0` ingen autentisering, `2` endast användarnamn, `3` användarnamn och lösenord, `1` Kerberos |
| `UID` | `digna_source_user` | Krävs för `AuthMech` `2` och `3` |
| `PWD` | `<password>` | Krävs för `AuthMech` `3`. Kryssa i **Encrypted** |

För Kerberos (`AuthMech=1`) behöver *digna*-värden dessutom en giltig biljett eller keytab, plus
egenskaperna `KrbHostFQDN`, `KrbServiceName` och `KrbRealm` som drivrutinen dokumenterar.

### Transport och TLS

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `ThriftTransport` | `2` | `0` binär (standard, port 10000), `1` SASL, `2` HTTP (port 10001, och det som en Knox-gateway förväntar sig) |
| `HTTPPath` | `cliservice` | Med `ThriftTransport=2` |
| `SSL` | `1` | Där HiveServer2 är skyddad med TLS |
| `Schema` | `dignadata` | Den Hive-databas som sessionen startar i. Valfritt — *digna* kvalificerar sina frågor |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Att tänka på med Hive {: #4-notes-on-hive }

- **Katalogerna kommer från drivrutinen.** Hive har ingen egen katalog, så *digna* använder det som
  drivrutinen rapporterar — normalt en enda post med namnet `HIVE` — och listar Hive-databaserna som
  scheman under den.
- **Work Schema är en Hive-databas.** För profileringsläget *Permanent* behöver användaren behörighet att
  skapa och ta bort tabeller i den, och den underliggande lagringsplatsen måste vara skrivbar.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema**. *Session* använder
  `CREATE TEMPORARY TABLE`, vilket kräver en HiveServer2 som stöder temporära tabeller, och
  rör inte **Work Schema**. *Standard* kräver endast läsbehörighet och är läget att välja
  på ett kluster där *digna* inte har någon skrivbehörighet alls.
- **Profilering är en uppsättning frågor, inte en genomsökning.** Varje statistikvärde beräknas av HiveServer2, så
  den kö som *dignas* användare skickar till bör ha tillräcklig kapacitet för inspektionsfönstret.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att drivrutinen, transportläget och dina
inloggningsuppgifter fungerar innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

Fälten **Host**, **Port**, **Database**, **Mechanism** och **Thrift Transport** här motsvarar
egenskaperna `HOST`, `PORT`, `Schema`, `AuthMech` och `ThriftTransport` i
[avsnitt 2](#2-odbc-properties).

#### Steg 2 – Testa anslutningen

Ange lösenordet och klicka på knappen **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Efter ett lyckat test, klicka på knappen **OK**.