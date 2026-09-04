---
title: Apache Hive Connector – Databaseintegration | digna-dokumentation
description: Konfigurer *digna* til at oprette forbindelse til Apache Hive ved hjælp af den native PyHive-driver eller Cloudera ODBC-driveren. Understøtter adgangskodebaseret autentificering samt DSN og DSN-less konfigurationer.
image: /assets/logo_square.png
---


# Kildeconnector til Hive

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Hive ved hjælp af enten den native Python-connector eller ODBC-driveren.

Den henviser til skærmen **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `PyHive`  
**Supported Authentication:** Kun adgangskodebaseret autentificering

> For andre autentificeringsmetoder, brug venligst ODBC-driveren.

### *digna* Konfiguration (Native Driver)

Angiv følgende oplysninger i skærmen **"Create a Database Connection"**:

```
Technology:      Apache Hive
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 10000
Database Name:   Schema that contains the source data
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-driveren kan understøtte et bredere udvalg af autentificerings- og tilslutningsmuligheder. Dette afsnit fokuserer på adgangskodebaseret autentificering ved brug af driveren **Cloudera ODBC Driver for Apache Hive**.

### 1. Installer ODBC-driveren

Installer **Cloudera ODBC Driver for Apache Hive** (eller en tilsvarende) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved hjælp af adgangskodebaseret autentificering:

#### Trin 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Trin 2 – Test forbindelsen

Angiv adgangskoden og klik på **Test**-knappen.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Efter en succesfuld test, klik på **OK**-knappen.

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* Konfiguration

I skærmen **"Create a Database Connection"**, angiv følgende:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> `DSN` skal matche navnet, der er defineret i din ODBC-driverkonfiguration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

I skærmen **"Create a Database Connection"**, angiv følgende:

```
Technology:      Apache Hive
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 10000"
name: "Schema",     value: "Schema that contains the source data"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```