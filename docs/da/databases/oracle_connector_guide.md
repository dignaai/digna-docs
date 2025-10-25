---
title: Oracle Connector – Databaseintegration | digna Dokumentation
description: Konfigurer digna til at oprette forbindelse til Oracle ved hjælp af python-oracledb-driveren eller Oracle ODBC-driveren. Understøtter adgangskodebaseret autentificering med DSN eller DSN-less opsætninger.
image: /assets/logo_square.png
---


# Kildeconnector til Oracle

Denne vejledning beskriver, hvordan du konfigurerer *digna* til at oprette forbindelse til Oracle DB ved enten at bruge den native Python-connector eller ODBC-driveren.

Der henvises til skærmbilledet **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Understøttet autentificering:** Kun adgangskodebaseret autentificering

> ⚠️ For andre autentificeringsmetoder, brug venligst ODBC-driveren.

### *digna* Konfiguration (Native Driver)

Angiv følgende oplysninger i skærmbilledet **"Create a Database Connection"**:

```
Technology:      Oracle
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1521
Database Name:   Instance name, service name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

ODBC-driveren kan understøtte et bredere udvalg af autentificerings- og forbindelsesmuligheder. Dette afsnit fokuserer på adgangskodebaseret autentificering ved brug af driveren **Oracle in OraDB21Home1**.

### 1. Installer ODBC-driveren

Installer **Oracle in OraDB21Home1** (eller tilsvarende) ved at følge leverandørens officielle installationsvejledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trin for at konfigurere en ny ODBC-datakilde ved hjælp af adgangskodebaseret autentificering:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Bemærk:
TNS Service Name skal være konfigureret i tnsnames.ora-filen i din Oracle-klientinstallation. Her angiver du forbindelsesbeskrivelsen (host, port, service name).

#### Step 2 – Test forbindelsen

Klik på knappen **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Angiv adgangskoden og klik på **OK**-knappen.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Nu kan du konfigurere *digna* til at bruge ODBC-forbindelsen, enten med en **DSN (Data Source Name)** eller en **DSN-less** opsætning.

---

### A. DSN-baseret konfiguration

#### *digna* Konfiguration

I skærmbilledet **"Create a Database Connection"** angiver du følgende:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less konfiguration

#### *digna* Konfiguration

I skærmbilledet **"Create a Database Connection"** angiver du følgende:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```