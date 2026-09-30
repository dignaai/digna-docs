---
title: PostgreSQL-connector – Database-integratie | digna Documentatie
description: Configureer digna om via ODBC met een DSN-loze connection string verbinding te maken met PostgreSQL. Behandelt de psqlODBC-driver, de vereiste ODBC-properties, SSL-modi en de verbindingsinstellingen aan de kant van digna.
image: /assets/logo_square.png
---


# Bronconnector voor PostgreSQL

Deze gids beschrijft hoe je *digna* configureert om via **ODBC** verbinding te maken met
PostgreSQL, met een **DSN-loze** connection string.

De *digna*-kant van de configuratie is voor elke technologie hetzelfde — waar verbindingen worden
aangemaakt, hoe property-waarden worden versleuteld, hoe een verbinding wordt getest en wat de
profiling modes betekenen. Dat wordt beschreven in het
[Overzicht databaseverbindingen](overview.md). Deze pagina behandelt wat specifiek is voor
PostgreSQL.

---

## 1. Installeer de ODBC-driver {: #1-install-the-odbc-driver }

Installeer de PostgreSQL ODBC-driver (**psqlODBC**) op de machine waarop de *digna*-backend
draait, volgens de officiële installatiegids van de leverancier.

De driver registreert zich onder een naam die per platform en pakket verschilt — gewoonlijk
**PostgreSQL Unicode(x64)** op Windows en **PostgreSQL ODBC Driver(UNICODE)** op Linux. Lees de
exacte naam op je host af zoals beschreven in
[Installeer de ODBC-driver op de digna-host](overview.md#install-the-driver), en gebruik die naam
voor de property `DRIVER` hieronder.

---

## 2. ODBC-properties {: #2-odbc-properties }

!!! important "Een voorbeeld, geen specificatie"

    De onderstaande set is één combinatie waarvan bekend is dat ze werkt. De properties horen bij
    de psqlODBC-driver, dus hun namen, standaardwaarden en toegestane waarden verschillen per
    driverversie en platform, en ook wat je server eist — vooral SSL — kan afwijken. Gebruik dit
    als startpunt en raadpleeg de documentatie van de geïnstalleerde driverversie.

Voeg de volgende properties toe in het scherm **Add DB Connection**:

| Key | Voorbeeldwaarde | Opmerkingen |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Moet overeenkomen met de drivernaam die op de *digna*-host is geregistreerd |
| `SERVER` | `db.example.com` | Servernaam of IP-adres |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Database die de bronschema's bevat. Het is de enige database die deze verbinding kan profilen |
| `UID` | `digna_source_user` | Databasegebruiker |
| `PWD` | `<password>` | Vink **Encrypted** aan |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` of `verify-full` — moet door de server worden geaccepteerd |

De resulterende connection string ziet er zo uit:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Elke andere psqlODBC-optie kan als extra property worden toegevoegd — bijvoorbeeld `ReadOnly=1`
voor een alleen-lezen sessie, of `ConnSettings` om bij het verbinden `SET`-statements uit te
voeren.

---

## 3. *digna*-configuratie {: #3-digna-configuration }

Geef in het scherm **Add DB Connection** het volgende op:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Opmerkingen over PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` moet overeenkomen met de server.** Een server die met `hostssl` is geconfigureerd,
  weigert `SSLMode=disable`, en `verify-ca` of `verify-full` vereisen bovendien dat het
  rootcertificaat voor de driver op de *digna*-host beschikbaar is. Als je bij het testen van de
  driver een specifieke modus moest kiezen, gebruik die dan ook hier.
- **Eén verbinding ziet één database.** *digna* biedt de schema's aan van de database die in
  `DATABASE` is opgegeven, omdat PostgreSQL alleen de huidige database als catalog meldt.
  Brontabellen in een andere database hebben een eigen verbinding nodig.
- **Profiling modes.** *Permanent* maakt de werktabellen aan in **Work Schema**, dus de gebruiker
  heeft `CREATE` op dat schema nodig. *Session* gebruikt `CREATE TEMPORARY TABLE` en raakt
  **Work Schema** niet aan. *Standard* heeft alleen leesrechten nodig.

---

## 5. De driver controleren (optioneel) {: #5-verifying-the-driver-optional }

Voor een DSN-loze verbinding hoef je geen ODBC-databron te configureren, maar het eigen
dialoogvenster van de driver is een handige manier om te bevestigen dat de driver werkt en dat de
server je inloggegevens en SSL-modus accepteert, voordat je ze in *digna* invoert.

#### Stap 1
![Stap 1](images/postgres/create_odbc_data_source_step1.png)

#### Stap 2 – Test de verbinding

Klik op de knop **Test Connection**.

![Stap 2](images/postgres/create_odbc_data_source_step2.png)

De waarden die je hier hebt ingevoerd, zijn precies de waarden die de properties in
[sectie 2](#2-odbc-properties) krijgen.
