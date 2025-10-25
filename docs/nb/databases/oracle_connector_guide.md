---
title: Oracle-tilkobling – Databaseintegrasjon | digna-dokumentasjon
description: Konfigurer digna for å koble til Oracle ved hjelp av python-oracledb-driveren eller Oracle ODBC-driveren. Støtter passordbasert autentisering med DSN- eller DSN-løse oppsett.
image: /assets/logo_square.png
---


# Kildekobler for Oracle

Denne veiledningen beskriver hvordan du konfigurerer *digna* for å koble til Oracle DB ved å bruke enten den native Python-connectoren eller ODBC-driveren.

Den viser til skjermen **"Create a Database Connection"**.

![Opprett en databasetilkobling](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `python-oracledb`  
**Støttet autentisering:** Kun passordbasert autentisering

> ⚠️ For andre autentiseringsmetoder, bruk ODBC-driveren.

### *digna*-konfigurasjon (native driver)

Oppgi følgende informasjon i **"Create a Database Connection"**-skjermen:

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

## ODBC-driver

ODBC-driveren kan støtte et bredere spekter av autentiserings- og tilkoblingsalternativer. Denne seksjonen fokuserer på passordbasert autentisering ved bruk av driveren **Oracle in OraDB21Home1**.

### 1. Installer ODBC-driveren

Installer **Oracle in OraDB21Home1** (eller tilsvarende) ved å følge leverandørens offisielle installasjonsveiledning.

### 2. Konfigurer ODBC-datakilden

Følg disse trinnene for å konfigurere en ny ODBC-datakilde med passordbasert autentisering:

#### Trinn 1
![Trinn 1](images/oracle/create_odbc_data_source_step1.png)

Merk:
TNS Service Name må konfigureres i tnsnames.ora-filen i din Oracle-klientinstallasjon. Her angir du tilkoblingsbeskrivelsen (host, port, service name).

#### Trinn 2 – Test tilkoblingen

Klikk på **Test Connection**-knappen.

![Trinn 2](images/oracle/create_odbc_data_source_step2.png)

Oppgi passordet og klikk på **OK**-knappen.

![Trinn 2](images/oracle/create_odbc_data_source_step3.png)

---

Nå kan du konfigurere *digna* til å bruke ODBC-tilkoblingen, enten med en **DSN (Data Source Name)** eller et **DSN-løst** oppsett.

---

### A. DSN-basert konfigurasjon

#### *digna*-konfigurasjon

I **"Create a Database Connection"**-skjermen, oppgi følgende:

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

> 🔹 `DSN` må samsvare med navnet som er definert i ODBC-driverkonfigurasjonen din.

---

### B. DSN-løst oppsett

#### *digna*-konfigurasjon

I **"Create a Database Connection"**-skjermen, oppgi følgende:

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