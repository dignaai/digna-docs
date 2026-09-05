---
title: Azure Synapse Connector – Database Integration | digna Documentation
description: Configure digna to connect to Azure Synapse Analytics using either the native Python driver or the ODBC driver. Supports both serverless and dedicated SQL pools.
image: /assets/logo_square.png
---


# Source Connector for Azure Synapse Analytics

Denne guiden beskriver hvordan du konfigurerer *digna* for å koble til Azure Synapse Analytics ved hjelp av enten den native Python-tilkoblingen eller ODBC-driveren.
Den støtter både serverless og dedikerte SQL-pooler.

Den viser til skjermen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Kun passordbasert autentisering

> For andre autentiseringsmetoder, vennligst bruk ODBC-driveren.

### *digna* konfigurasjon (native driver)

Oppgi følgende informasjon i skjermen **"Create a Database Connection"**:

```
Teknologi:       MS SQL Server
Vertsadresse:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Portnummer:      Portnummer, f.eks. 1433
Databasenavn:    Databasenavn
Skjema:          Skjema som inneholder kilde-dataene
Brukernavn:      Databasens brukernavn
Brukerpassord:   Passord for brukeren
Bruk ODBC:       Deaktivert (standard)
```

---

## ODBC Driver

ODBC-driveren kan støtte et bredere spekter av autentiserings- og tilkoblingsalternativer. Denne seksjonen fokuserer på passordbasert autentisering ved bruk av driveren **ODBC Driver 18 for SQL Server**.

### 1. Installer ODBC-driveren

Installer driveren **ODBC Driver 18 for SQL Server** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsguide.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde med passordbasert autentisering:

#### Trinn 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Fyll ut feltet "Server".
Bruk navnet på Synapse-arbeidsområdet og legg til ".sql.azuresynapse.net".  
**Merk**, hvis du vil koble til ved hjelp av en serverless SQL-pool, må du passe på å inkludere "-ondemand" som vist i skjermbildet under.

Klikk på **Next >**-knappen.

#### Trinn 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Velg autentiseringsmetode (f.eks. brukernavn og passord)
og oppgi nødvendige data.

Klikk på **Next >**-knappen.

#### Trinn 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Velg ANSI-kompatible innstillinger og klikk deretter på **Next >**-knappen.

#### Trinn 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Du kan la standardinnstillingene stå eller velge alternativer etter behov 
og klikke på **Finish**-knappen. 

#### Trinn 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klikk nå på **Test datasource**-knappen.

#### Trinn 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Når du mottar suksessskjermen, er ODBC riktig konfigurert.

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller en **DSN-less**-oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna* konfigurasjon

I skjermen **"Create a Database Connection"** oppgir du følgende:

```
Teknologi:       MS SQL Server
Databasenavn:    Database som inneholder kilde-skjemaet
Skjema:          Skjema som inneholder kilde-dataene
Bruk ODBC:       Aktivert
```

#### ODBC-egenskaper

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-less konfigurasjon

#### *digna* konfigurasjon

I skjermen **"Create a Database Connection"** oppgir du følgende:

```
Teknologi:       MS SQL Server
Databasenavn:    Skjema som inneholder kilde-dataene (samme som Skjema)
Skjema:          Skjema som inneholder kilde-dataene
Bruk ODBC:       Aktivert
```

#### ODBC-egenskaper

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Merk** angående SERVER-egenskapen:  
Bruk navnet på Synapse-arbeidsområdet og legg til ".sql.azuresynapse.net". Hvis du vil koble til ved bruk av en serverless SQL-pool, må du sørge for å inkludere "-ondemand" som vist i skjermbildet under.