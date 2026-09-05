---
title: Azure Synapse Connector – Databaseintegration | digna Dokumentation
description: Konfigurer digna til at oprette forbindelse til Azure Synapse Analytics enten ved hjælp af den native Python-driver eller ODBC-driveren. Understøtter både serverløse og dedikerede SQL-pools.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Azure Synapse Analytics enten ved hjælp af den native Python-connector eller ODBC-driveren.
Den understøtter både serverløse og dedikerede SQL-pools.

Den refererer til skærmen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Password-based authentication only

> For andre godkendelsesmetoder, brug venligst ODBC-driveren.

### *digna* Configuration (Native Driver)

Angiv følgende oplysninger i skærmen **"Create a Database Connection"**:

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

ODBC-driveren kan understøtte en bredere vifte af godkendelses- og forbindelsesmuligheder. Dette afsnit fokuserer på adgangskodebaseret godkendelse ved brug af driveren **ODBC Driver 18 for SQL Server**.

### 1. Installér ODBC-driveren

Installér driveren **ODBC Driver 18 for SQL Server** (eller tilsvarende) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved brug af adgangskodebaseret godkendelse:

#### Trin 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Udfyld feltet "Server".
Brug navnet på Synapse-workspacet og udvid det med ".sql.azuresynapse.net".   
**Bemærk**, hvis du vil oprette forbindelse ved hjælp af et serverløst SQL-pool, skal du sørge for at inkludere "-ondemand", som vist i skærmbilledet nedenfor.

Klik på knappen **Next >**.

#### Trin 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Vælg godkendelsesmetode (f.eks. brugernavn og adgangskode)
og angiv de krævede oplysninger.

Klik på knappen **Next >**.

#### Trin 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Vælg ANSI-kompatible indstillinger, og klik derefter på knappen **Next >**.

#### Trin 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Du kan lade standardindstillingerne være eller vælge indstillinger efter behov 
og klikke på knappen **Finish**. 

#### Trin 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klik nu på knappen **Test datasource**.

#### Trin 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Når du modtager succes-skærmen, er ODBC konfigureret korrekt.

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* Configuration

I skærmen **"Create a Database Connection"**, angiv følgende:

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

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

I skærmen **"Create a Database Connection"**, angiv følgende:

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

**Bemærk** angående SERVER-egenskaben:  
Brug navnet på Synapse-workspacet og udvid det med ".sql.azuresynapse.net". Hvis du vil oprette forbindelse ved hjælp af et serverløst SQL-pool, skal du sørge for at inkludere "-ondemand", som vist i skærmbilledet nedenfor.