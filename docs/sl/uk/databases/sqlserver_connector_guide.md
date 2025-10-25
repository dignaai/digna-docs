---
title: Povezovalnik MS SQL Server – Integracija baze podatkov | digna Dokumentacija
description: Konfigurirajte digna za povezavo z Microsoft SQL Server z uporabo Python gonilnika pymssql ali SQL Server ODBC gonilnika. Podpira overjanje z geslom z DSN ali brez DSN nastavitev.
image: /assets/logo_square.png
---


# Vir podatkov — povezovalnik za MS SQL Server

Ta vodič opisuje, kako konfigurirati *digna*, da se poveže s SQL Server z uporabo bodisi nativnega Python konektorja bodisi ODBC gonilnika.

Sklicuje se na zaslon **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativni Python gonilnik

**Knjižnica:** `pymssql`  
**Podprto overjanje:** Samo overjanje z geslom

> ⚠️ Za druge metode overjanja uporabite ODBC gonilnik.

### Konfiguracija *digna* (nativni gonilnik)

Vnesite naslednje podatke v zaslon **"Create a Database Connection"**:

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

## ODBC gonilnik

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezljivosti. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **SQL Server**.

### 1. Namestitev ODBC gonilnika

Namestite gonilnik **SQL Server** (ali soroden) tako, da sledite uradnemu vodniku za namestitev ponudnika.

### 2. Konfiguracija ODBC vira podatkov

Sledite tem korakom za konfiguracijo novega ODBC vira podatkov z overjanjem z geslom:

#### Korak 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknite gumb **Next >**.

#### Korak 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Izberite metodo overjanja (npr. uporabniško ime in geslo)
in vnesite zahtevane podatke.

Kliknite gumb **Next >**.

#### Korak 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Izberite ANSI skladne nastavitve in nato kliknite gumb **Next >**.

#### Korak 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Privzete nastavitve lahko pustite ali pa po potrebi izberete možnosti beleženja 
in kliknite gumb **Finish**. 

#### Korak 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Zdaj kliknite gumb ** Test datasource **.

#### Korak 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Ko prejmete zaslon o uspehu, je ODBC pravilno konfiguriran.

---

Zdaj lahko konfigurirate *digna*, da uporablja ODBC povezavo, bodisi z **DSN (Data Source Name)** ali z **DSN-less** nastavitvijo.

---

### A. Konfiguracija na osnovi DSN

#### Konfiguracija *digna*

V zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 Vrednost `DSN` se mora ujemati z imenom, definiranem v vaši konfiguraciji ODBC gonilnika.

---

### B. DSN-less konfiguracija

#### Konfiguracija *digna*

V zaslonu **"Create a Database Connection"** vnesite naslednje:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC lastnosti

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```