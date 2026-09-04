---
title: Oracle Connector – Database Integration | digna Documentation
description: Configure digna to connect to Oracle using the python-oracledb driver or the Oracle ODBC driver. Supports password-based authentication with DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Avota savienotājs Oracle

Šī rokasgrāmata apraksta, kā konfigurēt *digna*, lai izveidotu savienojumu ar Oracle DB, izmantojot vai nu nativu Python savienotāju, vai ODBC draiveri.

Atsauce uz ekrānu **"Create a Database Connection"**.

![Izveidot datubāzes savienojumu](images/data_source_config_input_mask.png)

---

## Nativais Python draiveris

**Bibliotēka:** `python-oracledb`  
**Atbalstītā autentifikācija:** Tikai parolei balstīta autentifikācija

> Citu autentifikācijas metožu gadījumā izmantojiet ODBC draiveri.

### *digna* konfigurācija (nativais draiveris)

Norādiet sekojošo informāciju ekrānā **"Create a Database Connection"**:

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

## ODBC draiveris

ODBC draiveris var atbalstīt plašāku autentifikācijas un savienojamības iespēju klāstu. Šī sadaļa koncentrējas uz parolei balstītu autentifikāciju, izmantojot draiveri **Oracle in OraDB21Home1**.

### 1. Instalējiet ODBC draiveri

Instalējiet **Oracle in OraDB21Home1** (vai līdzvērtīgu) saskaņā ar piegādātāja oficiālo instalācijas ceļvedi.

### 2. Konfigurējiet ODBC datu avotu

Veiciet šīs darbības, lai konfigurētu jaunu ODBC datu avotu, izmantojot parolei balstītu autentifikāciju:

#### 1. solis
![1. solis](images/oracle/create_odbc_data_source_step1.png)

Piezīme:
TNS Service Name ir jākonfigurē jūsu oracle klienta tnsnames.ora failā. Tur jānorāda savienojuma apraksts (host, port, service name).

#### 2. solis – Pārbaudīt savienojumu

Noklikšķiniet uz pogas Test Connection.

![2. solis](images/oracle/create_odbc_data_source_step2.png)

Ievadiet paroli un noklikšķiniet uz OK.

![2. solis](images/oracle/create_odbc_data_source_step3.png)

---

Tagad varat konfigurēt *digna*, lai izmantotu ODBC savienojumu, vai nu ar **DSN (Data Source Name)**, vai ar **DSN-less** iestatījumu.

---

### A. Konfigurācija ar DSN

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC īpašības

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "jūsu Oracle lietotājs"
name: "PWD",            value: "{jūsu parole figzīmotās iekavās}"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Konfigurācija bez DSN

#### *digna* konfigurācija

Ekrānā **"Create a Database Connection"** norādiet sekojošo:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC īpašības

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "jūsu Oracle lietotājs"
name: "PWD",        value: "jūsu Oracle parole"
```