---
title: Netezza-connector – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till Netezza via ODBC med en DSN-lös anslutningssträng. Omfattar NetezzaSQL-drivrutinen, de ODBC-egenskaper som krävs och anslutningsinställningarna i digna.
image: /assets/logo_square.png
---


# Källconnector för Netezza

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Netezza via **ODBC** med en
**DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Netezza.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera ODBC-drivrutinen **NetezzaSQL** (en del av IBM Netezza-klientverktygen) på maskinen
som kör *digna*-backenden enligt leverantörens officiella installationsguide.

Läs av det exakta registrerade drivrutinsnamnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    NetezzaSQL-drivrutinen, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    klientversioner och plattformar, och en TLS-skyddad appliance behöver fler egenskaper än de som visas
    här. Använd detta som utgångspunkt och läs dokumentationen för den klientversion du har
    installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden. Klammerparenteserna är det vanliga sättet att skriva detta namn |
| `SERVER` | `netezza.example.com` | Servernamn eller IP-adress |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Databasen som sessionen startar i |
| `UID` | `ADMIN` | Databasanvändare |
| `PWD` | `<password>` | Kryssa i **Encrypted** |

Den resulterande anslutningssträngen ser ut så här:

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Beroende på drivrutinsversion, konfiguration och säkerhetskrav kan ytterligare egenskaper
behövas — till exempel `SecurityLevel` och `CaCertFile` för en TLS-skyddad appliance. Alla alternativ
som drivrutinens dialogrutor *Advanced*, *SSL* och *Driver* erbjuder kan läggas till som egenskaper.

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Att tänka på med Netezza {: #4-notes-on-netezza }

- **Både kataloger och scheman används.** *digna* listar de databaser som användaren får se (från
  `_V_DATABASE`) som kataloger och deras scheman (från `_V_SCHEMA`) under dem, så en anslutning
  kan betjäna källor i mer än en databas. `DATABASE` avgör bara var sessionen
  startar.
- **Identifierare skrivs med versaler** om de inte skapades inom citattecken, vilket är anledningen till att exemplen
  ovan använder `TEST` och `ADMIN`.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema**, så användaren behöver
  `CREATE TABLE` där. *Session* använder `CREATE TEMPORARY TABLE` och rör inte
  **Work Schema**. *Standard* kräver endast läsbehörighet.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att drivrutinen och dina inloggningsuppgifter fungerar innan du
anger dem i *digna*.

#### Steg 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Fälten i **DSN Options** motsvarar ett-till-ett egenskaperna i
[avsnitt 2](#2-odbc-properties). Beroende på din Netezza-drivrutin, konfiguration och säkerhetskrav
kan du även behöva ange uppgifter på flikarna **Advanced DSN Options**, **SSL DSN Options** eller
**Driver Options**; för den enklaste konfigurationen räcker **DSN Options**.

Klicka på knappen **Test Connection**.

#### Steg 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

När bekräftelseskärmen visas fungerar drivrutinen och värdena är korrekta.
