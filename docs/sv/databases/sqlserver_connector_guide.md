---
title: MS SQL Server-anslutning – Databasintegration | digna-dokumentation
description: Konfigurera digna för att ansluta till Microsoft SQL Server med Python-drivrutinen pymssql eller SQL Server ODBC-drivrutinen. Stöder lösenordsbaserad autentisering med DSN eller utan DSN.
image: /assets/logo_square.png
---


# Källanslutning för MS SQL Server

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till SQL Server med antingen den inbyggda Python-connectorn eller ODBC-drivrutinen.

Den hänvisar till skärmen **"Create a Database Connection"**.

![Skapa en databasanslutning](images/data_source_config_input_mask.png)

---

## Inbyggd Python-drivrutin

**Library:** `pymssql`  
**Stödd autentisering:** Endast lösenordsbaserad autentisering

> För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna*-konfiguration (inbyggd drivrutin)

Ange följande information i skärmen **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Servernamn eller IP-adress
Host Port:       Portnummer, t.ex. 1433
Database Name:   Databasnamn
Schema Name:     Schema som innehåller källdata
User Name:       Databasens användarnamn
User Password:   Lösenord för användaren
Use ODBC:        Disabled (default)
```

---

## ODBC-drivrutin

ODBC-drivrutinen kan stödja ett bredare utbud av autentiserings- och anslutningsalternativ. Denna sektion fokuserar på lösenordsbaserad autentisering med drivrutinen **SQL Server**.

### 1. Installera ODBC-drivrutinen

Installera drivrutinen **SQL Server** (eller liknande) genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Steg 1
![Steg 1](images/sqlserver/create_odbc_data_source_step1.png)

Klicka på knappen **Next >**.

#### Steg 2
![Steg 2](images/sqlserver/create_odbc_data_source_step2.png)

Välj autentiseringsmetod (t.ex. användarnamn och lösenord)
och ange nödvändig information.

Klicka på knappen **Next >**.

#### Steg 3
![Steg 3](images/sqlserver/create_odbc_data_source_step3.png)

Välj ANSI-kompatibla inställningar och klicka sedan på knappen **Next >**.

#### Steg 4
![Steg 4](images/sqlserver/create_odbc_data_source_step4.png)

Du kan lämna standardinställningarna eller välja loggalternativ vid behov 
och klicka på knappen **Finish**. 

#### Steg 5
![Steg 5](images/sqlserver/create_odbc_data_source_step5.png)

Klicka nu på knappen **Test datasource**.

#### Steg 6
![Steg 1](images/sqlserver/create_odbc_data_source_step6.png)

När du får framgångsskärmen är ODBC korrekt konfigurerat.

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **konfiguration utan DSN**.

---

### A. DSN-baserad konfiguration

#### *digna*-konfiguration

I skärmen **"Create a Database Connection"** ange följande:

```
Technology:      MS SQL Server
Database Name:   Databas som innehåller källschemat
Schema Name:     Schema som innehåller källdata
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Konfiguration utan DSN

#### *digna*-konfiguration

I skärmen **"Create a Database Connection"** ange följande:

```
Technology:      MS SQL Server
Database Name:   Schema som innehåller källdata (samma som Schema Name)
Schema Name:     Schema som innehåller källdata
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```