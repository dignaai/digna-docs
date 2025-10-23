---
title: Conector PostgreSQL – Integrare Bază de Date | digna Documentation
description: Configurați digna pentru a se conecta la PostgreSQL folosind driverul Python psycopg sau driverul ODBC pentru PostgreSQL. Suportă autentificare pe bază de parolă cu configurații DSN sau fără DSN.
image: /assets/logo_square.png
---


# Source Connector for PostgreSQL

Acest ghid descrie cum să configurați *digna* pentru a se conecta la Postgres folosind fie conectorul nativ Python, fie driverul ODBC.

Se face referire la ecranul **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Doar autentificare pe bază de parolă

> ⚠️ Pentru alte metode de autentificare, vă rugăm să folosiți driverul ODBC.

### *digna* Configuration (Native Driver)

Furnizați următoarele informații în ecranul **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Driverul ODBC poate oferi un set mai larg de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă utilizând driverul **PostgreSQL Unicode(x64)**.

### 1. Instalarea driverului ODBC

Instalați **PostgreSQL Unicode(x64)** (sau unul similar) urmând ghidul oficial de instalare al vendorului.

### 2. Configurarea sursei de date ODBC

Urmați pașii de mai jos pentru a configura o nouă sursă de date ODBC folosind autentificare pe bază de parolă:

#### Pasul 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Notă: Dacă configurația bazei de date necesită selectarea unui anumit "SSLMode", asigurați-vă că utilizați aceeași setare și când definiți o configurație DSN-less.

#### Pasul 2 – Testați conexiunea

Faceți clic pe butonul **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Acum puteți configura *digna* să folosească conexiunea ODBC, fie cu o configurație **DSN (Data Source Name)**, fie una **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

În ecranul **"Create a Database Connection"**, furnizați următoarele:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

În ecranul **"Create a Database Connection"**, furnizați următoarele:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```