---
title: Netezza-anslutare – Databasintegration | digna Dokumentation
description: Konfigurera digna för att ansluta till Netezza med NetezzaSQL ODBC-drivrutinen. Stöder lösenordsbaserad autentisering med DSN eller DSN-lösa uppsättningar för flexibel anslutning.
image: /assets/logo_square.png
---


# Källanslutning för Netezza

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Netezza med hjälp av ODBC-drivrutinen.

Den hänvisar till skärmen **"Skapa en databasanslutning"**.

![Skapa en databasanslutning](images/data_source_config_input_mask.png)

---

## ODBC-drivrutin

ODBC-drivrutinen kan stödja en rad autentiserings- och anslutningsalternativ. Detta avsnitt fokuserar på lösenordsbaserad autentisering med drivrutinen **NetezzaSQL**.

### 1. Installera ODBC-drivrutinen

Installera drivrutinen **NetezzaSQL** (eller liknande) genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Steg 1
![Steg 1](images/netezza/create_odbc_data_source_step1.png)

Beroende på din Netezza-drivrutin, installations- och säkerhetskrav kan du även behöva ange data i flikarna **Advanced DSN Options**, **SSL DSN Options** eller **Driver Options**. För den enklaste uppsättningen är det tillräckligt att ange data i **DSN Options**.

Klicka på knappen **Testa anslutning**.

#### Steg 2
![Steg 2](images/netezza/create_odbc_data_source_step2.png)

När du får skärmen som visar att testet lyckades är ODBC korrekt konfigurerat.

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-lös** uppsättning.

---

### A. DSN-baserad konfiguration

#### *digna*-konfiguration

På skärmen **"Skapa en databasanslutning"** ange följande:

```
Teknik:          Netezza
Databasnamn:     Databasen som innehåller källschemat
Schemanamn:      Schemat som innehåller källdata
Använd ODBC:     Aktiverad
```

#### ODBC-egenskaper

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "din databasanvändare"
name: "PWD",        value: "ditt databaslösenord"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-lös konfiguration

#### *digna*-konfiguration

På skärmen **"Skapa en databasanslutning"** ange följande:

```
Teknik:          Netezza
Databasnamn:     Schemat som innehåller källdata (samma som Schemanamn)
Schemanamn:      Schemat som innehåller källdata
Använd ODBC:     Aktiverad
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "ditt servernamn eller IP-adress"
name: "PORT",       value: "Portnummer, t.ex. 5480"
name: "DATABASE",   value: "namn på databasen som innehåller källdataschemat"
name: "UID",        value: "din databasanvändare"
name: "PWD",        value: "ditt databaslösenord"
```