---
title: Conector Netezza – Integrare Bază de Date | Documentație digna
description: Configurează digna pentru a se conecta la Netezza folosind driverul ODBC NetezzaSQL. Suportă autentificare pe bază de parolă cu configurări DSN sau DSN-less pentru conectivitate flexibilă.
image: /assets/logo_square.png
---


# Conector sursă pentru Netezza

Acest ghid descrie cum să configurezi *digna* pentru a se conecta la Netezza folosind driverul ODBC.

Se referă la ecranul **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Driver ODBC

Driverul ODBC poate suporta o gamă de opțiuni de autentificare și conectivitate. Această secțiune se concentrează pe autentificarea pe bază de parolă folosind driverul **NetezzaSQL**.

### 1. Instalarea driverului ODBC

Instalează driverul **NetezzaSQL** (sau un driver similar) urmând ghidul oficial de instalare al furnizorului.

### 2. Configurarea sursei de date ODBC

Urmează pașii de mai jos pentru a configura o nouă sursă de date ODBC folosind autentificare pe bază de parolă:

#### Pasul 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

În funcție de driverul Netezza, de configurația și de cerințele de securitate, este posibil să trebuiască să furnizezi date și în filele **Advanced DSN Options**, **SSL DSN Options** sau **Driver Options**. Pentru cea mai simplă configurare este suficient să introduci informațiile în **DSN Options**.

Apasă butonul **Test Connection**.

#### Pasul 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Când primești ecranul de succes, ODBC este configurat corespunzător.

---

Acum poți configura *digna* să folosească conexiunea ODBC, fie cu un **DSN (Data Source Name)**, fie într-o configurație **DSN-less**.

---

### A. Configurare bazată pe DSN

#### Configurarea *digna*

În ecranul **"Create a Database Connection"**, completează următoarele:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Proprietăți ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> `DSN` trebuie să corespundă numelui definit în configurația driverului ODBC.

---

### B. Configurare fără DSN

#### Configurarea *digna*

În ecranul **"Create a Database Connection"**, completează următoarele:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Proprietăți ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```