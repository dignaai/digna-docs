---
title: Teradata-connector – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till Teradata via ODBC med en DSN-lös anslutningssträng. Omfattar Teradatas ODBC-drivrutin, egenskapen DBCNAME, inloggningsmekanismer och anslutningsinställningarna i digna.
image: /assets/logo_square.png
---


# Källconnector för Teradata

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Teradata via **ODBC** med en
**DSN-lös** anslutningssträng.

*digna*-delen av konfigurationen är densamma för alla tekniker — var anslutningar skapas,
hur egenskapsvärden krypteras, hur en anslutning testas och vad profileringslägena
innebär. Den beskrivs i [Översikt över databasanslutningar](overview.md). Denna sida täcker det som
är specifikt för Teradata.

---

## 1. Installera ODBC-drivrutinen {: #1-install-the-odbc-driver }

Installera **ODBC Driver for Teradata** på maskinen som kör *digna*-backenden
enligt leverantörens officiella installationsguide.

Drivrutinen registrerar sig med sin version i namnet, till exempel
**Teradata Database ODBC Driver 20.00**. Läs av det exakta registrerade namnet på din värd enligt
beskrivningen i [Installera ODBC-drivrutinen på digna-värden](overview.md#install-the-driver).

---

## 2. ODBC-egenskaper {: #2-odbc-properties }

!!! important "Ett exempel, inte en specifikation"

    Uppsättningen nedan är en kombination som är känd för att fungera. Egenskaperna tillhör
    Teradatas ODBC-drivrutin, så deras namn, standardvärden och tillåtna värden skiljer sig mellan
    drivrutinsversioner — versionen ingår i själva drivrutinsnamnet — och mellan plattformar. Använd detta
    som utgångspunkt och läs dokumentationen för den drivrutinsversion du har installerat.

Lägg till följande egenskaper på skärmen **Add DB Connection**:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Måste matcha drivrutinsnamnet som är registrerat på *digna*-värden |
| `DBCNAME` | `teradata.example.com` | Servernamn eller IP-adress. Teradatas eget namn på värdegenskapen |
| `UID` | `digna_source_user` | Databasanvändare |
| `PWD` | `<password>` | Kryssa i **Encrypted** |

Den resulterande anslutningssträngen ser ut så här:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Användbara ytterligare egenskaper:

| Nyckel | Exempelvärde | Noteringar |
|---|---|---|
| `MechanismName` | `TD2` | Inloggningsmekanism. `TD2` är Teradatas standard; använd `LDAP` för katalogautentisering |
| `DefaultDatabase` | `dad` | Databasen som sessionen startar i |
| `CharacterSet` | `UTF8` | Ange detta där sessionens standardteckenuppsättning skulle förvanska data som inte är ASCII |

---

## 3. *digna*-konfiguration {: #3-digna-configuration }

På skärmen **Add DB Connection**, ange följande:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Att tänka på med Teradata {: #4-notes-on-teradata }

- **En Teradata-databas är en katalog, inte ett schema.** *digna* listar de databaser som användaren får
  se (från `DBC.DatabasesV`) som kataloger, och schemanivån används inte. När du lägger till en
  datakälla, välj databasen som katalog; schemat rapporteras som *not applicable*.
- **En anslutning når alla tillåtna databaser**, så en enda anslutning kan betjäna källor
  i flera databaser — till skillnad från de tekniker där anslutningen är låst till en databas.
- **Work Schema är en databas.** För profileringsläget *Permanent*, ange den Teradata-databas som
  innehåller arbetstabellerna, och ge användaren behörigheten `CREATE TABLE` plus en tilldelning av `PERM`-utrymme
  i den — en databas med noll perm-utrymme kan inte innehålla en tabell.
- **Profileringslägen.** *Permanent* skapar tabeller i **Work Schema**. *Session* använder en
  `VOLATILE`-tabell, som kräver `SPOOL`-utrymme men inget perm-utrymme och inga behörigheter i **Work
  Schema**. *Standard* kräver endast läsbehörighet.

---

## 5. Verifiera drivrutinen (valfritt) {: #5-verifying-the-driver-optional }

Att konfigurera en ODBC-datakälla krävs inte för en DSN-lös anslutning, men drivrutinens
egen dialogruta är ett bekvämt sätt att bekräfta att drivrutinen och dina inloggningsuppgifter fungerar innan du
anger dem i *digna*.

#### Steg 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Fältet **Name or IP address** här motsvarar egenskapen `DBCNAME` i
[avsnitt 2](#2-odbc-properties).

Klicka på knappen **Test**.

#### Steg 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Ange användarnamn och lösenord och klicka sedan på knappen **OK**. En bekräftelseskärm visar att
drivrutinen och inloggningsuppgifterna fungerar.
