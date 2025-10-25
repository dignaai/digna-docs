---
title: Povezava MS SQL Server – Integracija podatkov | digna-dokumentacija
description: Konfigurirajte digna za povezavo z Microsoft SQL Server z uporabo Python-driverja pymssql ali SQL Server ODBC-driverja. Podprta je avtentikacija z geslom z DSN ali konfiguracijo brez DSN.
image: /assets/logo_square.png
---


# Povezava podatkovnega vira za MS SQL Server

Ta vodič pojasnjuje, kako konfigurirati *digna* za povezavo z SQL Server bodisi z uporabo izvornega Python-driverja ali ODBC-driverja.

Navaja zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativni Python-driver

**Library:** `pymssql`  
**Podprta avtentikacija:** Le avtentikacija z geslom

> ⚠️ Za druge metode avtentikacije uporabite ODBC-driver.

### *digna*-konfiguracija (nativni driver)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

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

ODBC-driver podpira širši nabor možnosti avtentikacije in povezovanja. Ta razdelek se osredotoča na avtentikacijo z geslom z driverjem **SQL Server**.

### 1. Namestite ODBC-driver

Namestite driver **SQL Server** (ali ustreznega) tako, da sledite uradnim navodilom ponudnika.

### 2. Konfigurirajte ODBC-podatkovni vir

Sledite tem korakom za nastavitev novega ODBC-podatkovnega vira z avtentikacijo z geslom:

#### Step 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknite gumb **Next >**.

#### Step 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Izberite metodo avtentikacije (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### Step 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Izberite nastavitve združljive z ANSI in kliknite gumb **Next >**.

#### Step 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Lahko obdržite privzete nastavitve ali po potrebi izberete možnosti beleženja
in nato kliknite gumb **Finish**. 

#### Step 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Zdaj kliknite gumb ** Test datasource **.

#### Step 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Ko se prikaže zaslon s potrdilom o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC-povezavo, bodisi z **DSN (Data Source Name)** ali z nastavitvijo **brez DSN (DSN-less)**.

---

### A. DSN-podprta konfiguracija

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

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

> 🔹 `DSN` mora sovpadati z imenom, definiranem v vaši ODBC-driver konfiguraciji.

---

### B. Konfiguracija brez DSN (DSN-less)

#### *digna*-konfiguracija

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

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