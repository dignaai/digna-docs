# Bronconnector voor MS SQL Server

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met
Microsoft SQL Server, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor SQL
Server.

!!! note "Azure Synapse Analytics"

    Synapse wordt ook als SQL Server-verbinding geconfigureerd, met een andere hostnaam en een paar
    extra aandachtspunten — zie [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer **ODBC Driver 18 for SQL Server** op de machine waarop de *digna*-backend draait,
volgens de [installatiegids van Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

De driver die met Windows wordt meegeleverd onder de eenvoudige naam **SQL Server** werkt ook,
maar is al lang achterhaald en ondersteunt geen moderne TLS-instellingen en geen
Azure-authenticatie. Gebruik hem alleen als het installeren van de huidige driver geen optie is.

Lees de exacte geregistreerde drivernaam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de ODBC-driver van Microsoft, dus hun namen, standaardwaarden en toegestane waarden verschillen
    per driverversie — Driver 18 versleutelt bijvoorbeeld standaard, terwijl Driver 17 dat niet
    deed — en per platform. Gebruik dit als startpunt en raadpleeg de documentatie van de
    geïnstalleerde driverversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `SERVER` | `sql.example.com` | Servernaam of IP-adres. Named instances: `host\instance`; een niet-standaardpoort: `host,1433` |
| `PORT` | `1433` | Weglaten als de poort al deel uitmaakt van `SERVER` |
| `DATABASE` | `digna_source_db` | Database die de bronschema's bevat. Het is de enige database die deze verbinding kan profilen |
| `UID` | `digna_source_user` | Databasegebruiker |
| `PWD` | `<password>` | Vink **Encrypted** aan |

De resulterende connection string ziet er zo uit:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Versleuteling met ODBC Driver 18

Driver 18 versleutelt verbindingen standaard en valideert het servercertificaat. Bij een server
met een certificaat dat je *digna*-host niet vertrouwt — meestal een self-signed certificaat —
mislukt het verbinden met een fout in de certificaatketen. Voeg toe:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Encrypt` | `yes` | Standaard in Driver 18; zet het alleen op `no` als de server geen TLS ondersteunt |
| `TrustServerCertificate` | `yes` | Slaat de certificaatvalidatie over. Handig in testomgevingen; installeer in productie bij voorkeur het certificaat |

### Windows-authenticatie

Om verbinding te maken als het account waaronder de *digna*-service draait in plaats van met een
SQL-login, laat je `UID` en `PWD` weg en voeg je toe:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Trusted_Connection` | `yes` | Het serviceaccount van *digna* heeft de databaserechten nodig |

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opmerkingen over MS SQL Server {: #4-notes-on-ms-sql-server }

- **Eén verbinding ziet één database.** *digna* biedt de schema's aan van de database die in
  `DATABASE` is opgegeven, omdat SQL Server alleen de huidige database als catalog meldt.
  Brontabellen in een andere database hebben een eigen verbinding nodig.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema**, dus de gebruiker
  heeft daar `CREATE TABLE` nodig. *Session* gebruikt lokale tijdelijke tabellen (`#wt_…`) in
  `tempdb` en raakt **Work Schema** niet aan. *Standard* heeft alleen leesrechten nodig.
- **`SERVER` bevat de instance en de poort.** Bij een named instance vereist `host\instance` dat
  de SQL Server Browser-service bereikbaar is; `host,port` vermijdt dat.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar de eigen wizard van
de driver is een handige manier om te bevestigen dat de driver werkt en dat de server je
inloggegevens accepteert, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/sqlserver/create_odbc_data_source_step1.png)

Klik op de knop **Next >**.

#### Stap 2
![Stap 2](images/sqlserver/create_odbc_data_source_step2.png)

Kies de authenticatiemethode (bijv. gebruikersnaam en wachtwoord)
en geef de vereiste gegevens op.

Klik op de knop **Next >**.

#### Stap 3
![Stap 3](images/sqlserver/create_odbc_data_source_step3.png)

Kies de ANSI-conforme instellingen en klik daarna op de knop **Next >**.

#### Stap 4
![Stap 4](images/sqlserver/create_odbc_data_source_step4.png)

Je kunt de standaardinstellingen laten staan of naar behoefte logopties kiezen,
en klik daarna op de knop **Finish**.

#### Stap 5
![Stap 5](images/sqlserver/create_odbc_data_source_step5.png)

Klik nu op de knop **Test datasource**.

#### Stap 6
![Stap 6](images/sqlserver/create_odbc_data_source_step6.png)

Een succesmelding bevestigt dat de driver en de inloggegevens werken. De waarden die je hebt
ingevoerd, zijn precies de waarden die de properties in [sectie 2](#2-odbc-properties) krijgen.