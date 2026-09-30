---
title: Azure Synapse-connector – Database-integratie | digna Documentatie
description: Configureer digna om via ODBC met een DSN-loze connection string verbinding te maken met Azure Synapse Analytics. Ondersteunt serverless en dedicated SQL pools, met de vereiste ODBC-properties en de verbindingsinstellingen aan de kant van digna.
image: /assets/logo_square.png
---


# Bronconnector voor Azure Synapse Analytics

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met Azure
Synapse Analytics, met een **DSN-loze** connection string. Zowel serverless als dedicated SQL
pools worden ondersteund.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor Azure
Synapse.

!!! note "Technologie"

    Synapse spreekt het SQL Server-dialect, dus de verbinding wordt aangemaakt met **Technology:
    SQL Server**. Zie [MS SQL Server](sqlserver_connector_guide.md) voor een on-premises server.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer **ODBC Driver 18 for SQL Server** op de machine waarop de *digna*-backend draait,
volgens de [installatiegids van Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
en lees de exacte geregistreerde drivernaam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de ODBC-driver van Microsoft, dus hun namen, standaardwaarden en toegestane waarden verschillen
    per driverversie en platform, en wat de workspace vereist, hangt af van hoe die is
    geconfigureerd — pooltype, authenticatiemethode, firewall. Gebruik dit als startpunt en
    raadpleeg de documentatie van de geïnstalleerde driverversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Workspacenaam plus het endpoint-achtervoegsel — zie hieronder |
| `DATABASE` | `dignadata` | Database die de bronschema's bevat. Het is de enige database die deze verbinding kan profilen |
| `UID` | `sqladminuser` | SQL-login |
| `PWD` | `<password>` | Vink **Encrypted** aan |

De resulterende connection string ziet er zo uit:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### De waarde van `SERVER`

Neem de naam van de Synapse-workspace en voeg het endpoint-achtervoegsel toe:

| Pool | `SERVER` |
|---|---|
| **Serverless SQL pool** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedicated SQL pool** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Het deel `-ondemand` wordt snel over het hoofd gezien"

    Zonder dit deel verwijst de naam naar het dedicated endpoint, en mislukt de verbinding of
    bereikt ze ongemerkt een andere pool dan bedoeld. Beide endpoints staan op de overzichtspagina
    van de workspace in de Azure-portal.

### Firewall

De firewall van de Synapse-workspace moet het uitgaande adres van de *digna*-host toestaan. Voeg
het toe onder **Networking** in de workspace voordat je de verbinding test — een geblokkeerd adres
verschijnt als een verbindingstime-out in plaats van een authenticatiefout.

### Authenticatie met Microsoft Entra ID

In plaats van een SQL-login kan de driver zich authenticeren tegen Entra ID. Vervang `UID`/`PWD`
door de authenticatiemethode die je workspace verwacht, bijvoorbeeld:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` bevat dan de application (client) ID en `PWD` het client secret |
| `Authentication` | `ActiveDirectoryMSI` | Managed identity van de *digna*-host, geen inloggegevens nodig |

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opmerkingen over Azure Synapse {: #4-notes-on-azure-synapse }

- **Serverless pools ondersteunen alleen *Standard* profiling.** Een serverless SQL pool kan geen
  tabellen in een database aanmaken, dus zowel *Permanent* als *Session* profiling kunnen niet
  draaien. *Standard* berekent de metrics direct op de bron, wat ook de goedkopere optie is,
  omdat serverless per verwerkte hoeveelheid data wordt gefactureerd.
- **Eén verbinding ziet één database.** *digna* biedt de schema's aan van de database die in
  `DATABASE` is opgegeven, omdat Synapse, net als SQL Server, alleen de huidige database als
  catalog meldt.
- **Versleuteling staat standaard aan** in Driver 18, en Synapse-endpoints presenteren geldige
  publieke certificaten, dus er is geen property `Encrypt` of `TrustServerCertificate` nodig.
- **Een serverless endpoint kan bij de eerste verbinding uit inactiviteit ontwaken.** Als de
  verbindingstest een time-out geeft op een pool die een tijd niet is gebruikt, probeer het dan
  opnieuw.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar de eigen wizard van
de driver is een handige manier om te bevestigen dat de driver werkt en dat de workspace je
inloggegevens accepteert, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/azure_synapse/create_odbc_data_source_step1.png)

Vul het veld "Server" in.
Gebruik de naam van de Synapse-workspace en vul die aan met ".sql.azuresynapse.net".  
**Let op**: als je verbinding wilt maken met een serverless SQL pool, zorg er dan voor dat je
"-ondemand" toevoegt, zoals in de schermafbeelding hierboven.

Klik op de knop **Next >**.

#### Stap 2
![Stap 2](images/azure_synapse/create_odbc_data_source_step2.png)

Kies de authenticatiemethode (bijv. gebruikersnaam en wachtwoord)
en geef de vereiste gegevens op.

Klik op de knop **Next >**.

#### Stap 3
![Stap 3](images/azure_synapse/create_odbc_data_source_step3.png)

Kies de ANSI-conforme instellingen en klik daarna op de knop **Next >**.

#### Stap 4
![Stap 4](images/azure_synapse/create_odbc_data_source_step4.png)

Je kunt de standaardinstellingen laten staan of naar behoefte opties kiezen,
en klik daarna op de knop **Finish**.

#### Stap 5
![Stap 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klik nu op de knop **Test datasource**.

#### Stap 6
![Stap 6](images/azure_synapse/create_odbc_data_source_step6.png)

Een succesmelding bevestigt dat de driver, het endpoint en de inloggegevens werken. De waarden
die je hebt ingevoerd, zijn precies de waarden die de properties in [sectie 2](#2-odbc-properties)
krijgen.
