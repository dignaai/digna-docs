---
title: Azure Synapse-anslutning – databasintegration | digna-dokumentation
description: Konfigurera digna för att ansluta till Azure Synapse Analytics med antingen den inbyggda Python-drivrutinen eller ODBC-drivrutinen. Stöder både serverlösa och dedikerade SQL-pooler.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Källanslutning för Azure Synapse Analytics

Denna guide beskriver hur du konfigurerar *digna* för att ansluta till Azure Synapse Analytics med antingen den inbyggda Python-anslutaren eller ODBC-drivrutinen.
Den stöder både serverlösa och dedikerade SQL-pooler.

Den hänvisar till skärmen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Inbyggd Python-drivrutin

**Library:** `pymssql`  
**Stödd autentisering:** Endast lösenordsbaserad autentisering

> ⚠️ För andra autentiseringsmetoder, använd ODBC-drivrutinen.

### *digna* konfiguration (inbyggd drivrutin)

Fyll i följande information i skärmen **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-drivrutin

ODBC-drivrutinen kan stödja ett bredare utbud av autentiserings- och anslutningsalternativ. Denna sektion fokuserar på lösenordsbaserad autentisering med drivrutinen **ODBC Driver 18 for SQL Server**.

### 1. Installera ODBC-drivrutinen

Installera drivrutinen **ODBC Driver 18 for SQL Server** (eller liknande) genom att följa leverantörens officiella installationsguide.

### 2. Konfigurera ODBC-datakällan

Följ dessa steg för att konfigurera en ny ODBC-datakälla med lösenordsbaserad autentisering:

#### Steg 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Fyll i fältet "Server".
Använd namnet på Synapse-arbetsytan och lägg till ".sql.azuresynapse.net".  
**Observera**, om du vill ansluta med en serverlös SQL-pool, se till att inkludera "-ondemand" som visas i skärmbilden nedan.

Klicka på knappen **Next >**.

#### Steg 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Välj autentiseringsmetod (t.ex. användarnamn och lösenord)
och ange nödvändiga uppgifter.

Klicka på knappen **Next >**.

#### Steg 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Välj ANSI-kompatibla inställningar och klicka sedan på knappen **Next >**.

#### Steg 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Du kan behålla standardinställningarna eller välja alternativ vid behov 
och klicka sedan på knappen **Finish**. 

#### Steg 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klicka nu på knappen **Test datasource**.

#### Steg 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

När du får framgångsskärmen är ODBC korrekt konfigurerat.

---

Nu kan du konfigurera *digna* att använda ODBC-anslutningen, antingen med en **DSN (Data Source Name)** eller en **DSN-fri** lösning.

---

### A. DSN-baserad konfiguration

#### *digna* konfiguration

I skärmen **"Create a Database Connection"** ange följande:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "din databasanvändare"
name: "PWD",        value: "ditt databaslösenord"
name: "DATABASE",   value: "namnet på databasen som innehåller källschemat"

```

> 🔹 `DSN` måste matcha namnet som definierats i din ODBC-drivrutinskonfiguration.

---

### B. DSN-fri konfiguration

#### *digna* konfiguration

I skärmen **"Create a Database Connection"** ange följande:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "din databasanvändare"
name: "PWD",        value: "ditt databaslösenord"
name: "DATABASE",   value: "namnet på databasen som innehåller källschemat"
```

**Notera** angående egenskapen SERVER:  
Använd namnet på Synapse-arbetsytan och lägg till ".sql.azuresynapse.net". Om du vill ansluta med en serverlös SQL-pool, se till att inkludera "-ondemand" som visas i skärmbilden nedan.