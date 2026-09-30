---
title: Netezza-connector – Database-integratie | digna Documentatie
description: Configureer digna om via ODBC met een DSN-loze connection string verbinding te maken met Netezza. Behandelt de NetezzaSQL-driver, de vereiste ODBC-properties en de verbindingsinstellingen aan de kant van digna.
image: /assets/logo_square.png
---


# Bronconnector voor Netezza

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met Netezza,
met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor
Netezza.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer de ODBC-driver **NetezzaSQL** (onderdeel van de IBM Netezza-clienttools) op de machine
waarop de *digna*-backend draait, volgens de officiële installatiegids van de leverancier.

Lees de exacte geregistreerde drivernaam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver).

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de NetezzaSQL-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen per
    clientversie en platform, en een met TLS beveiligde appliance heeft meer nodig dan de
    properties die hier worden getoond. Gebruik dit als startpunt en raadpleeg de documentatie van
    de geïnstalleerde clientversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd. De accolades zijn de gebruikelijke schrijfwijze voor deze naam |
| `SERVER` | `netezza.example.com` | Servernaam of IP-adres |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Database waarin de sessie start |
| `UID` | `ADMIN` | Databasegebruiker |
| `PWD` | `<password>` | Vink **Encrypted** aan |

De resulterende connection string ziet er zo uit:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Afhankelijk van je driverversie, configuratie en beveiligingseisen kunnen extra properties nodig
zijn — bijvoorbeeld `SecurityLevel` en `CaCertFile` voor een met TLS beveiligde appliance. Elke
optie die de dialoogvensters *Advanced*, *SSL* en *Driver* van de driver bieden, kan als property
worden toegevoegd.

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Opmerkingen over Netezza {: #4-notes-on-netezza }

- **Zowel catalogs als schema's zijn van toepassing.** *digna* toont de databases die de
  gebruiker mag zien (uit `_V_DATABASE`) als catalogs en hun schema's (uit `_V_SCHEMA`)
  daaronder, dus één verbinding kan bronnen in meer dan één database bedienen. `DATABASE` bepaalt
  alleen waar de sessie start.
- **Identifiers zijn in hoofdletters**, tenzij ze tussen aanhalingstekens zijn aangemaakt; daarom
  gebruiken de voorbeelden hierboven `TEST` en `ADMIN`.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema**, dus de gebruiker
  heeft daar `CREATE TABLE` nodig. *Session* gebruikt `CREATE TEMPORARY TABLE` en raakt
  **Work Schema** niet aan. *Standard* heeft alleen leesrechten nodig.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de driver en je
inloggegevens werken, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/netezza/create_odbc_data_source_step1.png)

De velden in **DSN Options** komen één op één overeen met de properties in
[sectie 2](#2-odbc-properties). Afhankelijk van je Netezza-driver, configuratie en
beveiligingseisen heb je mogelijk ook gegevens nodig in de tabbladen **Advanced DSN Options**,
**SSL DSN Options** of **Driver Options**; voor de eenvoudigste configuratie volstaat
**DSN Options**.

Klik op de knop **Test Connection**.

#### Stap 2
![Stap 2](images/netezza/create_odbc_data_source_step2.png)

Wanneer je de succesmelding ziet, werkt de driver en kloppen de waarden.
