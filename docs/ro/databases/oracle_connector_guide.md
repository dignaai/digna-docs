---
title: Conector Oracle – Integrare baze de date | Documentație digna
description: Configurează digna pentru a se conecta la Oracle folosind driverul python-oracledb sau driverul Oracle ODBC. Suportă autentificare pe bază de parolă cu configurații DSN sau fără DSN.
image: /assets/logo_square.png
---


# Conector sursă pentru Oracle

Acest ghid descrie cum să configurezi *digna* pentru a se conecta la Oracle DB folosind fie conectorul Python nativ, fie driverul ODBC.

Se referă la ecranul **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver Python nativ

**Library:** `python-oracledb`  
**Autentificare acceptată:** Doar autentificare pe bază de parolă

> ⚠️ Pentru alte metode de autentificare, te rugăm să folosești driverul ODBC.

### Configurarea *digna* (Driver nativ)

Furnizează următoarele informații în ecranul **"Create a Database Connection"**:

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

## Driver ODBC

Driverul ODBC poate oferi o gamă mai largă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă folosind driverul **Oracle in OraDB21Home1**.

### 1. Instalarea driverului ODBC

Instalează **Oracle in OraDB21Home1** (sau echivalent) urmând ghidul oficial de instalare al furnizorului.

### 2. Configurează sursa de date ODBC

Urmărește pașii de mai jos pentru a configura o nouă sursă de date ODBC folosind autentificare pe bază de parolă:

#### Pasul 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Notă:
Numele serviciului TNS trebuie configurat în fișierul tnsnames.ora din instalarea clientului Oracle. Aici furnizezi descriptorul de conectare (host, port, service name).

#### Pasul 2 – Testează conexiunea

Apasă butonul **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Introdu parola și apasă butonul **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Acum poți configura *digna* să folosească conexiunea ODBC, fie cu un **DSN (Data Source Name)**, fie cu o configurație **fără DSN**.

---

### A. Configurare bazată pe DSN

#### Configurarea *digna*

În ecranul **"Create a Database Connection"**, furnizează următoarele:

```
Technology:      Oracle
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Proprietăți ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN` trebuie să corespundă numelui definit în configurația driverului ODBC.

---

### B. Configurare fără DSN

#### Configurarea *digna*

În ecranul **"Create a Database Connection"**, furnizează următoarele:

```
Technology:      Oracle
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Proprietăți ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```