---
title: Databricks-connector met Unity Catalog – Database-integratie | digna Documentatie
description: Configureer *digna* om verbinding te maken met Databricks en Unity Catalog met behulp van de native Python-connector of de ODBC-driver. Ondersteunt token-gebaseerde authenticatie en flexibele connectiviteit.
image: /assets/logo_square.png
---

# Bronconnector voor Databricks - met Unity Catalog

Deze handleiding beschrijft hoe je *digna* configureert om verbinding te maken met Databricks met behulp van de native Python-connector of de ODBC-driver.

Het verwijst naar het scherm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python-driver

**Library:** `databricks-sql-connector`  
**Ondersteunde authenticatie:** alleen Personal Access Token (PAT)

> Voor andere authenticatiemethoden, gebruik de ODBC-driver.

### Personal Access Token (PAT)

Om te authenticeren met een Personal Access Token, raadpleeg de officiële Databricks-documentatie:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuratie (Native Driver)

Geef de volgende informatie op in het scherm **"Create a Database Connection"**:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC-driver

De ODBC-driver ondersteunt een breder scala aan authenticatie- en connectiviteitsopties. Deze sectie richt zich op token-gebaseerde authenticatie met behulp van de **Simba Spark ODBC Driver**.

### 1. Installeer de ODBC-driver

Installeer de **Simba Spark ODBC Driver** door de officiële installatiehandleiding van de leverancier te volgen.

### 2. Configureer de ODBC-data source

Volg deze stappen om een nieuwe ODBC-data source te configureren met een Personal Access Token:

#### Stap 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Stap 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Stap 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Stap 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Stap 5 – Test de verbinding

Klik op de **TEST** knop. Een succesvolle verbinding ziet er zo uit:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nu kun je *digna* configureren om de ODBC-verbinding te gebruiken, ofwel met een **DSN (Data Source Name)** of een **DSN-less** setup.

---

### A. DSN-gebaseerde configuratie

#### *digna* Configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name: "DSN",    value: "*digna*data_databricks"
```

> De `DSN` moet overeenkomen met de naam die is gedefinieerd in je ODBC-driverconfiguratie.

---

### B. DSN-less configuratie

#### *digna* Configuratie

Geef in het scherm **"Create a Database Connection"** het volgende op:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-eigenschappen

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```