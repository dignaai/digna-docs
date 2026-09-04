---
title: Teradata Connector – Databaseintegration | digna-dokumentation
description: Konfigurer digna til at forbinde til Teradata ved hjælp af teradatasql Python-driveren eller Teradata ODBC-driveren. Understøtter adgangskodebaseret autentificering med DSN eller DSN-less opsætninger.
image: /assets/logo_square.png
---


# Source Connector til Teradata

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at forbinde til Teradata ved hjælp af enten den native Python-connector eller ODBC-driveren.

Den henviser til skærmen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `teradatasql`  
**Understøttet autentificering:** Kun adgangskodebaseret autentificering

> For andre autentificeringsmetoder, brug venligst ODBC-driveren.

### *digna*-konfiguration (native driver)

Angiv følgende oplysninger på skærmen **"Create a Database Connection"**:

```
Technology:      Teradata
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1025
Database Name:   Database name
Schema Name:     Database name
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-driver

ODBC-driveren kan understøtte et bredere sæt autentificerings- og forbindelsesmuligheder. Dette afsnit fokuserer på adgangskodebaseret autentificering ved brug af driveren **Teradata Database ODBC Driver 20.00**.

### 1. Installer ODBC-driveren

Installer driveren **Teradata Database ODBC Driver 20.00** (eller en lignende version) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde med adgangskodebaseret autentificering:

#### Trin 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Klik på **Test**-knappen.

#### Trin 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Indtast brugernavn og adgangskode.

Klik på **OK**-knappen.  
Når du får succesbeskeden, er ODBC konfigureret korrekt.

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna*-konfiguration

På skærmen **"Create a Database Connection"** angiv følgende:

```
Technology:      Teradata
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaber

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` skal matche navnet, der er defineret i din ODBC-driverkonfiguration.

---

### B. DSN-fri konfiguration

#### *digna*-konfiguration

På skærmen **"Create a Database Connection"** angiv følgende:

```
Technology:      Teradata
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-egenskaber

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```