---
title: PostgreSQL-connector – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till PostgreSQL via ODBC med en DSN-lös anslutningssträng. Omfattar psqlODBC-drivrutinen, de ODBC-egenskaper som krävs, SSL-lägen och anslutningsinställningarna i digna.
image: /assets/logo_square.png
---


# Källconnector för PostgreSQL

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till PostgreSQL via **ODBC** med en
**DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för PostgreSQL.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera PostgreSQL:s ODBC-drivrutin (**psqlODBC**) på maskinen som kör *digna*-backenden
enligt leverantörens officiella installationsguide.

Drivrutinen registrerar sig under ett namn som skiljer sig mellan plattformar och paket — vanligtvis
**PostgreSQL Unicode(x64)** på Windows och **PostgreSQL ODBC Driver(UNICODE)** på Linux. Läs av
det exakta namnet på din värd enligt beskrivningen i
[Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver), och använd det namnet
för egenskapen `DRIVER` nedan.

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    psqlODBC-drivrutinen, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner och plattformar, och det din server kräver — särskilt SSL — kan också skilja sig.
    Använd detta som utgångspunkt och läs dokumentationen för den drivrutinsversion du
    har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `SERVER` | `db.example.com` | Servernamn eller IP-adress |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Databasen som innehåller källschemana. Det är den enda databas som denna anslutning kan profilera |
| `UID` | `digna_source_user` | Databasanvändare |
| `PWD` | `<password>` | Kryssa i **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` eller `verify-full` — måste accepteras av servern |

Den resulterande anslutningssträngen ser ut så här:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Alla andra psqlODBC-alternativ kan läggas till som ytterligare egenskaper — till exempel
`ReadOnly=1` för en skrivskyddad session, eller `ConnSettings` för att köra `SET`-satser när
anslutningen upprättas.

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Att tänka på med PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` måste matcha servern.** En server som är konfigurerad med `hostssl` avvisar
  `SSLMode=disable`, och `verify-ca` eller `verify-full` kräver dessutom att rotcertifikatet
  är tillgängligt för drivrutinen på *digna*-värden. Om du var tvungen att välja ett visst läge när
  du testade drivrutinen, använd samma här.
- **En anslutning ser en databas.** *digna* erbjuder schemana i den databas som anges i
  `DATABASE`, eftersom PostgreSQL bara rapporterar den aktuella databasen som katalog. Källtabeller
  i en annan databas behöver en egen anslutning.
- **Profileringslägen.** *Permanent* skapar arbetstabellerna i **Work Schema**, så användaren
  behöver `CREATE` på det schemat. *Session* använder `CREATE TEMPORARY TABLE` och rör inte
  **Work Schema**. *Standard* kräver endast läsbehörighet.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att drivrutinen fungerar och att servern accepterar
dina inloggningsuppgifter och ditt SSL-läge innan du anger dem i *digna*.

#### Steg 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Steg 2 – Testa anslutningen

Klicka på knappen **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Värdena du angav här är exakt de värden som egenskaperna i
[avsnitt 2](#2-odbc-properties) tar.
