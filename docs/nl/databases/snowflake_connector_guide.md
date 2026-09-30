---
title: Snowflake-connector – Database-integratie | digna Documentatie
description: Configureer digna om via ODBC met een DSN-loze connection string verbinding te maken met Snowflake. Behandelt de Snowflake ODBC-driver, programmatic access tokens, de keuze van warehouse en rol en de verbindingsinstellingen aan de kant van digna.
image: /assets/logo_square.png
---


# Bronconnector voor Snowflake

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met
Snowflake, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor
Snowflake.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer de **Snowflake ODBC Driver** op de machine waarop de *digna*-backend draait, volgens de
[installatiegids van Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

De driver registreert zich als **SnowflakeDSIIDriver**. Lees de exacte geregistreerde naam op je
host af zoals beschreven in [Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

Snowflake wordt benaderd met een **programmatic access token (PAT)** — het authenticatiepad
waartegen *digna* is geverifieerd, en het pad dat Snowflake vereist voor accounts waarop inloggen
met alleen een wachtwoord is geblokkeerd.

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de Snowflake ODBC-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen
    per driverversie en platform, en welke authenticatieopties je account toestaat, wordt bepaald
    door het beveiligingsbeleid van het account. Gebruik dit als startpunt en raadpleeg de
    documentatie van de geïnstalleerde driverversie.

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `Server` | `<account>.snowflakecomputing.com` | Account identifier plus het achtervoegsel, bijv. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Snowflake-gebruiker bij wie het token hoort |
| `Database` | `TEST` | Database die de bronschema's bevat. Het is de enige database die deze verbinding kan profilen |
| `Schema` | `PUBLIC` | Standaardschema van de sessie |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Selecteert tokenauthenticatie |
| `token` | `<programmatic access token>` | Vink **Encrypted** aan |

De resulterende connection string ziet er zo uit:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Warehouse en rol

Queries hebben een warehouse nodig. Als de *digna*-gebruiker een standaard-warehouse en een
standaardrol heeft, neemt de sessie die over en hoeft er niets te worden geconfigureerd. Voeg
anders toe:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Warehouse dat de profiling-queries uitvoert |
| `Role` | `DIGNA_READER` | Rol waarvan de sessie de grants gebruikt |

!!! tip "Geef digna een eigen warehouse"

    Een apart, klein warehouse met auto-suspend houdt de profilingkosten zichtbaar en voorkomt
    dat *digna* met interactieve gebruikers om rekenkracht concurreert.

### Authenticatie met wachtwoord

Waar het account dit nog toestaat, werkt een wachtwoord in plaats van het token — laat
`authenticator` en `token` weg en voeg toe:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `PWD` | `<password>` | Vink **Encrypted** aan |

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Opmerkingen over Snowflake {: #4-notes-on-snowflake }

- **Tokens verlopen.** Een programmatic access token wordt met een levensduur uitgegeven, en
  profiling stopt op de dag dat het verloopt. Noteer de vervaldatum wanneer je het aanmaakt, en
  voer het nieuwe token opnieuw in de property `token` in — versleutelde waarden kunnen worden
  vervangen, maar niet worden teruggelezen.
- **Eén verbinding ziet één database.** *digna* biedt de schema's aan van de database die in
  `Database` is opgegeven, omdat Snowflake alleen de huidige database als catalog meldt.
  Brontabellen in een andere database hebben een eigen verbinding nodig.
- **Identifiers zijn in hoofdletters**, tenzij ze tussen aanhalingstekens zijn aangemaakt. *digna*
  gebruikt de namen zoals Snowflake ze meldt.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema**, dus de rol heeft
  daar `CREATE TABLE` nodig. *Session* gebruikt `CREATE TEMPORARY TABLE` en raakt
  **Work Schema** niet aan. *Standard* heeft alleen leesrechten nodig — en helemaal geen
  schrijfrechten.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de driver, de account-URL
en je inloggegevens werken, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/snowflake/create_odbc_data_source_step1.png)

Opmerkingen:

- De waarde voor **Server** bestaat uit je Snowflake-account identifier, gevolgd door
  `.snowflakecomputing.com`.
- **Database**, **Schema** en **Warehouse** die je hier invoert, komen overeen met de properties
  `Database`, `Schema` en `Warehouse` in [sectie 2](#2-odbc-properties).

#### Stap 2 – Test de verbinding

Klik op de knop **TEST**. Een geslaagde verbinding ziet er zo uit:

![Stap 2](images/snowflake/create_odbc_data_source_step2.png)
