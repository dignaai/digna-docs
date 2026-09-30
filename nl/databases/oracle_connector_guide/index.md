# Bronconnector voor Oracle

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met Oracle
Database, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor
Oracle.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

De Oracle ODBC-driver maakt deel uit van de **Oracle Client** (het Instant Client-pakket "ODBC"
volstaat). Installeer die op de machine waarop de *digna*-backend draait, volgens de officiële
installatiegids van de leverancier.

De driver registreert zich als **Oracle in `<OracleHomeName>`** — bijvoorbeeld
`Oracle in OraDB21Home1` of `Oracle in instantclient_21_13`. De naam van de home verschilt per
installatie, dus lees de exacte naam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de Oracle ODBC-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen per
    clientversie, en vooral de drivernaam hangt af van de Oracle home op je host. Gebruik dit als
    startpunt en raadpleeg de documentatie van de geïnstalleerde clientversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | De database waarmee verbinding wordt gemaakt — zie hieronder |
| `UID` | `DIGNA_SOURCE_USER` | Databasegebruiker |
| `PWD` | `<password>` | Vink **Encrypted** aan |

De resulterende connection string ziet er zo uit:

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### De waarde van `DBQ`

`DBQ` accepteert drie vormen. Voor *digna* zijn ze gelijkwaardig; ze verschillen in wat er op de
*digna*-host moet worden geconfigureerd:

| Vorm | Voorbeeld | Vereist |
|---|---|---|
| **Volledige connect descriptor** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Niets — alles staat in de property. Aanbevolen |
| **TNS-alias** | `DIGNA_SOURCE` | De alias moet bestaan in de `tnsnames.ora` van de Oracle Client op de *digna*-host |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Een Oracle Client die Easy Connect ondersteunt (12c en later) |

!!! tip "Geef de voorkeur aan de volledige descriptor"

    Een TNS-alias verplaatst de helft van de verbindingsdefinitie naar een bestand op de
    *digna*-host, waar het makkelijk wordt vergeten wanneer de host opnieuw wordt opgebouwd of
    *digna* wordt verhuisd. De volledige descriptor houdt de verbinding op zichzelf staand — en
    dat is precies het doel van een DSN-loze configuratie.

De haakjes in een descriptor zijn geen probleem binnen een connection string, maar als je
wachtwoord `;` bevat, zet het dan tussen accolades: `PWD={p@ss;word}`.

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Opmerkingen over Oracle {: #4-notes-on-oracle }

- **Schema's zijn gebruikers.** *digna* toont Oracle-gebruikers als schema's, dus het bronschema
  is de eigenaar van de tabellen — `DIGNA_SOURCE_USER` in het voorbeeld hierboven. De
  verbindingsgebruiker heeft `SELECT` op die tabellen nodig, direct of via een rol.
- **Eén verbinding ziet één database.** De catalog die *digna* aanbiedt, is de database waaraan de
  verbinding is gekoppeld, dus `DBQ` bepaalt welke service, en daarmee welke database, wordt
  geprofiled.
- **Identifiers zijn hoofdlettergevoelig zodra ze tussen aanhalingstekens staan.** *digna* zet de
  namen die het uit de data dictionary leest tussen aanhalingstekens, en dat is wat Oracle opslaat
  — hoofdletters voor objecten zonder aanhalingstekens.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema**, dus de gebruiker
  heeft daar `CREATE TABLE` nodig en een quota op de tablespace. *Session* gebruikt een private
  temporary table (`ORA$PTT_…`, Oracle 18c en later) en raakt **Work Schema** niet aan.
  *Standard* heeft alleen leesrechten nodig.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de Oracle Client, de
servicenaam en je inloggegevens werken, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/oracle/create_odbc_data_source_step1.png)

De **TNS Service Name** die hier wordt aangeboden, komt uit de `tnsnames.ora` van je Oracle
Client-installatie — daar zijn de alias, en daarmee de host, poort en servicenaam, gedefinieerd.
In *digna* kun je de alias als `DBQ` gebruiken, of in plaats daarvan de volledige descriptor.

#### Stap 2 – Test de verbinding

Klik op de knop **Test Connection**.

![Stap 2](images/oracle/create_odbc_data_source_step2.png)

Geef het wachtwoord op en klik op de knop **OK**.

![Stap 3](images/oracle/create_odbc_data_source_step3.png)

Een succesmelding bevestigt dat de driver en de inloggegevens werken.