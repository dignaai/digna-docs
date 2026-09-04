---
title: MS SQL Server-tilkobling – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til Microsoft SQL Server ved hjelp av pymssql Python-driveren eller SQL Server ODBC-driveren. Støtter passordbasert autentisering med DSN eller DSN‑løs konfigurasjon.
image: /assets/logo_square.png
---


# Kildekobling for MS SQL Server

Denne veiledningen beskriver hvordan du konfigurerer *digna* for å koble til SQL Server ved enten å bruke den native Python-tilkobleren eller ODBC-driveren.

Den viser til skjermen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `pymssql`  
**Supported Authentication:** Kun passordbasert autentisering

> For andre autentiseringsmetoder, vennligst bruk ODBC-driveren.

### *digna*-konfigurasjon (native driver)

Oppgi følgende informasjon i skjermen **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-driver

ODBC-driveren kan støtte et bredere utvalg av autentiserings- og tilkoblingsalternativer. Dette avsnittet fokuserer på passordbasert autentisering med driveren **SQL Server**.

### 1. Installer ODBC-driveren

Installer driveren **SQL Server** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde med passordbasert autentisering:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Klikk på **Next >**-knappen.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Velg autentiseringsmetode (f.eks. brukernavn og passord)
og oppgi nødvendig informasjon.

Klikk på **Next >**-knappen.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Velg ANSI-kompatible innstillinger og klikk på **Next >**-knappen.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Du kan beholde standardinnstillingene eller velge loggingsalternativer etter behov 
og klikk så på **Finish**-knappen. 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Klikk nå på ** Test datasource **-knappen.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Når du får opp suksessskjermen, er ODBC riktig konfigurert.

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller en **DSN-less** oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-less-konfigurasjon

#### *digna*-konfigurasjon

I skjermen **"Create a Database Connection"**, oppgi følgende:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```