---
title: Teradata-connector – Database-integratie | digna Documentatie
description: Configureer digna om via ODBC met een DSN-loze connection string verbinding te maken met Teradata. Behandelt de Teradata ODBC-driver, de property DBCNAME, logonmechanismen en de verbindingsinstellingen aan de kant van digna.
image: /assets/logo_square.png
---


# Bronconnector voor Teradata

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met
Teradata, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor
Teradata.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer de **ODBC Driver for Teradata** op de machine waarop de *digna*-backend draait, volgens
de officiële installatiegids van de leverancier.

De driver registreert zich met zijn versie in de naam, bijvoorbeeld
**Teradata Database ODBC Driver 20.00**. Lees de exacte geregistreerde naam op je host af zoals
beschreven in [Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de Teradata ODBC-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen per
    driverversie — de versie maakt zelfs deel uit van de drivernaam — en per platform. Gebruik dit
    als startpunt en raadpleeg de documentatie van de geïnstalleerde driverversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `DBCNAME` | `teradata.example.com` | Servernaam of IP-adres. De eigen naam van Teradata voor de host-property |
| `UID` | `digna_source_user` | Databasegebruiker |
| `PWD` | `<password>` | Vink **Encrypted** aan |

De resulterende connection string ziet er zo uit:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Nuttige extra properties:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `MechanismName` | `TD2` | Logonmechanisme. `TD2` is de standaard van Teradata; gebruik `LDAP` voor authenticatie via een directory |
| `DefaultDatabase` | `dad` | Database waarin de sessie start |
| `CharacterSet` | `UTF8` | Stel dit in als de standaard tekenset van de sessie niet-ASCII-data zou verminken |

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Opmerkingen over Teradata {: #4-notes-on-teradata }

- **Een Teradata-database is een catalog, geen schema.** *digna* toont de databases die de
  gebruiker mag zien (uit `DBC.DatabasesV`) als catalogs, en het schemaniveau is niet van
  toepassing. Kies bij het toevoegen van een databron de database als catalog; het schema wordt
  gemeld als *not applicable*.
- **Eén verbinding bereikt elke toegestane database**, dus één verbinding kan bronnen in meerdere
  databases bedienen — anders dan bij de technologieën waarbij de verbinding aan één database is
  gekoppeld.
- **Work Schema is een database.** Geef voor *Permanent* profiling de Teradata-database op die de
  werktabellen bevat, en geef de gebruiker daarin `CREATE TABLE`-rechten plus een toewijzing van
  `PERM`-ruimte — een database zonder perm space kan geen tabel bevatten.
- **Profiling modes.** *Permanent* maakt tabellen aan in **Work Schema**. *Session* gebruikt een
  `VOLATILE`-tabel, die `SPOOL`-ruimte nodig heeft, maar geen perm space en geen rechten in
  **Work Schema**. *Standard* heeft alleen leesrechten nodig.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de driver en je
inloggegevens werken, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/teradata/create_odbc_data_source_step1.png)

Het veld **Name or IP address** hier is de property `DBCNAME` in
[sectie 2](#2-odbc-properties).

Klik op de knop **Test**.

#### Stap 2
![Stap 2](images/teradata/create_odbc_data_source_step2.png)

Geef gebruikersnaam en wachtwoord op en klik daarna op de knop **OK**. Een succesmelding bevestigt
dat de driver en de inloggegevens werken.
