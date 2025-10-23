---
title: Connecteur Databricks (Legacy, sans Unity Catalog) | digna Documentation
description: Configurez digna pour se connecter à Databricks sans Unity Catalog en utilisant le connecteur Python natif ou le pilote ODBC Simba Spark. Prend en charge l’authentification par token et une connectivité flexible.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Ce guide décrit comment configurer *digna* pour se connecter à Databricks en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il fait référence à l’écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Pour d’autres méthodes d’authentification, veuillez utiliser le pilote ODBC.

### Personal Access Token (PAT)

Pour vous authentifier en utilisant un Personal Access Token, référez-vous à la documentation officielle de Databricks :  
👉 [Comment obtenir un PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Fournissez les informations suivantes dans l’écran **"Create a Database Connection"** :

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Le pilote ODBC prend en charge une gamme plus large d’options d’authentification et de connectivité. Cette section se concentre sur l’authentification par token en utilisant le **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Installez le **Simba Spark ODBC Driver** en suivant le guide d’installation officiel du fournisseur.

### 2. Configure the ODBC Data Source

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant un Personal Access Token :

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Cliquez sur le bouton **TEST**. Une connexion réussie doit ressembler à ceci :

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit en configuration **sans DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

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