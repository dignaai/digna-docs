---
title: MS SQL Server Connector – Database Integration | digna Documentation
description: Configure digna to connect to Microsoft SQL Server using the pymssql Python driver or the SQL Server ODBC driver. Supports password-based authentication with DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

Ta vodič opisuje, kako konfigurirati *digna*, da se poveže na SQL Server z uporabo bodisi izvornega Python konektorja bodisi ODBC gonilnika.

Navaja se zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `pymssql`  
**Supported Authentication:** Samo overjanje z geslom

> Za druge metode overjanja uporabite ODBC gonilnik.

### *digna* Configuration (Native Driver)

Vnesite naslednje podatke v zaslonu **"Create a Database Connection"**:

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

## ODBC Driver

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezljivosti. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **SQL Server**.

### 1. Namestite ODBC gonilnik

Namestite gonilnik **SQL Server** (ali podoben) po uradnem navodilu proizvajalca.

### 2. Konfigurirajte ODBC Data Source

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z overjanjem z geslom:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknite gumb **Next >**.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Izberite metodo overjanja (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Izberite nastavitve v skladu z ANSI in nato kliknite gumb **Next >**.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Privzete nastavitve lahko pustite ali po potrebi izberete možnosti beleženja
in kliknite gumb **Finish**. 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Zdaj kliknite gumb **Test datasource**.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Ko prejmete zaslon s potrditvijo uspeha, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. DSN-Based Configuration

#### *digna* Configuration

V zaslonu **"Create a Database Connection"** vnesite naslednje:

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

> `DSN` se mora ujemati z imenom, definiranim v konfiguraciji vašega ODBC gonilnika.

---

### B. DSN-less Configuration

#### *digna* Configuration

V zaslonu **"Create a Database Connection"** vnesite naslednje:

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