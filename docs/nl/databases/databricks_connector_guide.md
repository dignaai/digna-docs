---
title: Databricks-connector – Database-integratie | digna Documentatie
description: Configureer digna om via ODBC met een DSN-loze connection string verbinding te maken met Databricks met Unity Catalog. Behandelt de Databricks ODBC-driver, personal access tokens, het HTTP-pad en de verbindingsinstellingen aan de kant van digna.
image: /assets/logo_square.png
---

# Bronconnector voor Databricks

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met
Databricks, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor
Databricks.

!!! note "Unity Catalog is vereist"

    *digna* leest de beschikbare catalogs uit `system.information_schema.catalogs`, dus de
    workspace moet Unity Catalog ingeschakeld hebben. Eerdere *digna*-releases boden een aparte
    technologie "Databricks Legacy" voor workspaces zonder Unity Catalog; die is niet meer
    beschikbaar.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer de **Databricks ODBC Driver** op de machine waarop de *digna*-backend draait, volgens
de [installatiegids van Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Afhankelijk van de versie registreert de driver zich als **Simba Spark ODBC Driver** of als
**Databricks ODBC Driver**. Lees de exacte geregistreerde naam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. Verzamel de verbindingsgegevens {: #2-gather-the-connection-details }

Alle waarden komen van het SQL warehouse (of cluster) dat *digna* moet gebruiken. Open het in de
Databricks-workspace en ga naar **Connection details**:

| Databricks-veld | Gebruikt als |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normaal `443` |
| **HTTP path** | `HTTPPath` |

Maak voor de authenticatie een **personal access token** aan — zie
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Tokens horen bij een gebruiker of service principal, en die principal heeft `USE CATALOG`,
`USE SCHEMA` en `SELECT` op de brondata nodig.

---

## 3. ODBC-properties {: #3-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de Databricks/Simba-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen
    per driverversie — de driver is meer dan eens hernoemd en de authenticatieopties zijn
    uitgebreid — en per platform. Gebruik dit als startpunt en raadpleeg de documentatie van de
    geïnstalleerde driverversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `Host` | `<workspace>.cloud.databricks.com` | Server hostname van het warehouse, bijv. `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | HTTP-pad van het warehouse of cluster |
| `SSL` | `1` | Databricks-endpoints werken alleen met TLS |
| `ThriftTransport` | `2` | HTTP-transport, dat is wat de SQL-endpoints spreken |
| `AuthMech` | `3` | Tokenauthenticatie |
| `UID` | `token` | Het letterlijke woord `token`, geen gebruikersnaam |
| `PWD` | `dapi…` | Het personal access token. Vink **Encrypted** aan |
| `UseNativeQuery` | `1` | Geeft de SQL van *digna* ongewijzigd door — zie hieronder |

De resulterende connection string ziet er zo uit:

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Houd `UseNativeQuery=1` aan"

    Met `UseNativeQuery=0` — de standaardinstelling van de driver — herschrijft de driver
    binnenkomende SQL naar wat hij als portabele ODBC-syntaxis beschouwt. *digna* genereert al
    Databricks-SQL, dus het herschrijven kan de quoting met backticks en datumliteralen
    veranderen, waarna profiling mislukt op statements die zoals geschreven geldig zijn.

### OAuth in plaats van een token

Voor een service principal met OAuth machine-to-machine-authenticatie vervang je `AuthMech`,
`UID` en `PWD` door:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Client credentials |
| `Auth_Client_ID` | `<application id>` | Service principal |
| `Auth_Client_Secret` | `<client secret>` | Vink **Encrypted** aan |

---

## 4. *digna*-configuratie {: #4-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Opmerkingen over Databricks {: #5-notes-on-databricks }

- **Het warehouse moet draaien**, of kunnen starten, wanneer *digna* verbinding maakt. Een
  warehouse dat vanuit een gestopte toestand opstart, kan langer nodig hebben dan de
  verbindingstime-out — als de test bij de eerste poging na een periode van inactiviteit mislukt,
  probeer het dan opnieuw.
- **Catalogs komen uit de workspace.** Anders dan bij de meeste technologieën bereikt één
  Databricks-verbinding elke catalog die de principal mag zien, dus één verbinding kan bronnen in
  meerdere catalogs bedienen.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema** binnen de catalog
  van de bron, dus de principal heeft daar `CREATE TABLE` nodig. *Session* gebruikt
  `CREATE TEMPORARY TABLE` en raakt **Work Schema** niet aan. *Standard* heeft alleen leesrechten
  nodig.
- **Serverless warehouses werken** op dezelfde manier; alleen `HTTPPath` verschilt.

---

## 6. De driver controleren (optioneel) {: #6-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de driver, het warehouse
en het token werken, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/databricks/create_odbc_data_source_step1.png)

#### Stap 2
![Stap 2](images/databricks/create_odbc_data_source_step2.png)

#### Stap 3
![Stap 3](images/databricks/create_odbc_data_source_step3.png)

#### Stap 4
![Stap 4](images/databricks/create_odbc_data_source_step4.png)

#### Stap 5 – Test de verbinding

Klik op de knop **TEST**. Een geslaagde verbinding ziet er zo uit:

![Stap 5](images/databricks/create_odbc_data_source_step5.png)

De host, het HTTP-pad en het token die je hier invoert, zijn precies de waarden die de properties
in [sectie 3](#3-odbc-properties) krijgen.
