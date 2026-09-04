---
title: Oracle Connector – Integracija podatkovne baze | digna Dokumentacija
description: Konfigurirajte digna za povezavo z Oracle z uporabo gonilnika python-oracledb ali Oracle ODBC gonilnika. Podpira overjanje z geslom za nastavitve z DSN ali brez DSN.
image: /assets/logo_square.png
---


# Source Connector for Oracle

Ta vodnik opisuje, kako konfigurirati *digna* za povezavo z Oracle DB z uporabo bodisi izvornega Python konektorja bodisi ODBC gonilnika.

Navaja zaslon **"Create a Database Connection"**.

![Ustvarite povezavo do baze podatkov](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Supported Authentication:** Samo overjanje z geslom

> Za druge metode overjanja uporabite ODBC gonilnik.

### *digna* Configuration (Native Driver)

Vnesite naslednje podatke na zaslonu **"Create a Database Connection"**:

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

ODBC gonilnik lahko podpira širši nabor možnosti overjanja in povezljivosti. Ta razdelek se osredotoča na overjanje z geslom z uporabo gonilnika **Oracle in OraDB21Home1**.

### 1. Namestite ODBC gonilnik

Namestite **Oracle in OraDB21Home1** (ali podoben) tako, da sledite uradnemu navodilu za namestitev dobavitelja.

### 2. Konfigurirajte ODBC podatkovni vir

Sledite tem korakom za konfiguracijo novega ODBC podatkovnega vira z overjanjem z geslom:

#### Korak 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Opomba:
TNS Service Name mora biti konfiguriran v datoteki tnsnames.ora v vaši namestitvi Oracle odjemalca. Tam določite opis povezave (host, port, service name).

#### Korak 2 – Preizkusite povezavo

Kliknite gumb **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Vnesite geslo in kliknite gumb **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Zdaj lahko konfigurirate *digna*, da uporabi ODBC povezavo, bodisi z **DSN (Data Source Name)** ali s **DSN-less** nastavitvijo.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

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

> `DSN` mora ustrezati imenu, definiranemu v vaši ODBC konfiguraciji gonilnika.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na zaslonu **"Create a Database Connection"** vnesite naslednje:

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