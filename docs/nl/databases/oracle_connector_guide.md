---
title: Oracle Connector – Database-integratie | digna Documentatie
description: Configureer digna om verbinding te maken met Oracle met de python-oracledb-driver of de Oracle ODBC-driver. Ondersteunt wachtwoordgebaseerde authenticatie met DSN- of DSN-loze configuraties.
image: /assets/logo_square.png
---


# Source Connector for Oracle

Deze gids beschrijft hoe je *digna* configureert om verbinding te maken met Oracle DB met behulp van ofwel de native Python-connector of de ODBC-driver.

Er wordt verwezen naar het scherm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** Alleen wachtwoordgebaseerde authenticatie

> Voor andere authenticatiemethoden, gebruik de ODBC-driver.

### *digna* Configuration (Native Driver)

Geef de volgende informatie op in het scherm **"Create a Database Connection"**:

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

De ODBC-driver kan een breder scala aan authenticatie- en connectiviteitsopties ondersteunen. Deze sectie richt zich op wachtwoordgebaseerde authenticatie met de driver **Oracle in OraDB21Home1**.

### 1. Install the ODBC Driver

Installeer **Oracle in OraDB21Home1** (of een vergelijkbare) volgens de officiële installatiehandleiding van de leverancier.

### 2. Configure the ODBC Data Source

Volg deze stappen om een nieuwe ODBC-datasource te configureren met wachtwoordgebaseerde authenticatie:

#### Step 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Opmerking:
De TNS Service Name moet worden geconfigureerd in het tnsnames.ora-bestand van je Oracle-clientinstallatie. Hier geef je de connection descriptor op (host, poort, service name).

#### Step 2 – Test the connection

Klik op de knop **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Voer het wachtwoord in en klik op de knop **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Nu kun je *digna* configureren om de ODBC-verbinding te gebruiken, met een **DSN (Data Source Name)** of een **DSN-loze** configuratie.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Geef in het scherm **"Create a Database Connection"** het volgende op:

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

> De `DSN` moet overeenkomen met de naam die is opgegeven in je ODBC-driverconfiguratie.

---

### B. DSN-less Configuration

#### *digna* Configuration

Geef in het scherm **"Create a Database Connection"** het volgende op:

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