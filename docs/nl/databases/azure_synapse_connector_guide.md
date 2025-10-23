---
title: Azure Synapse-connector – Database-integratie | digna Documentatie
description: Configureer *digna* om verbinding te maken met Azure Synapse Analytics met behulp van de native Python-driver of de ODBC-driver. Ondersteunt zowel serverless als dedicated SQL-pools.
image: /assets/logo_square.png
---


# Bronconnector voor Azure Synapse Analytics

Deze gids beschrijft hoe je *digna* configureert om verbinding te maken met Azure Synapse Analytics met behulp van de native Python-connector of de ODBC-driver.
Het ondersteunt zowel serverless als dedicated SQL-pools.

Het verwijst naar het scherm **"Create a Database Connection"**.

![Een databaseverbinding maken](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Ondersteunde authenticatie:** Alleen op wachtwoord gebaseerde authenticatie

> ⚠️ Voor andere authenticatiemethoden gebruik je de ODBC-driver.

### *digna* Configuratie (Native Driver)

Vul de volgende gegevens in op het scherm **"Create a Database Connection"**:

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

## ODBC Driver

De ODBC-driver kan een breder scala aan authenticatie- en connectiviteitsopties ondersteunen. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **ODBC Driver 18 for SQL Server**.

### 1. Installeer de ODBC-driver

Installeer de driver **ODBC Driver 18 for SQL Server** (of een vergelijkbare versie) door de officiële installatiehandleiding van de leverancier te volgen.

### 2. Configureer de ODBC-databron

Volg deze stappen om een nieuwe ODBC-databron te configureren met wachtwoordgebaseerde authenticatie:

#### Step 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Vul het veld "Server" in.
Gebruik de naam van de synapse workspace en breid deze uit met ".sql.azuresynapse.net".   
**Let op**, als je wilt verbinden met een serverless SQL-pool, zorg dan dat je "-ondemand" toevoegt zoals te zien in de screenshot hieronder.

Klik op de knop **Next >**.

#### Step 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Kies de authenticatiemethode (bijv. gebruikersnaam en wachtwoord)
en geef de vereiste gegevens op.

Klik op de knop **Next >**.

#### Step 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Kies de ANSI-conforme instellingen en klik vervolgens op de knop **Next >**.

#### Step 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Je kunt de standaardinstellingen behouden of opties kiezen naar behoefte 
en klik op de knop **Finish**. 

#### Step 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klik nu op de knop ** Test datasource **.

#### Step 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Wanneer je het succesvenster ontvangt, is ODBC correct geconfigureerd.

---

Nu kun je *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of met een **DSN-less** setup.

---

### A. DSN-Based Configuration

#### *digna* Configuratie

Vul op het scherm **"Create a Database Connection"** het volgende in:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 De `DSN` moet overeenkomen met de naam die in je ODBC-driverconfiguratie is gedefinieerd.

---

### B. DSN-less Configuratie

#### *digna* Configuratie

Vul op het scherm **"Create a Database Connection"** het volgende in:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Opmerking** met betrekking tot de SERVER-eigenschap:  
Gebruik de naam van de synapse workspace en breid deze uit met ".sql.azuresynapse.net". Als je wilt verbinden met een serverless SQL-pool, zorg er dan voor dat je "-ondemand" toevoegt zoals te zien in de screenshot hieronder.