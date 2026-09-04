---
title: Connecteur Databricks avec Unity Catalog – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à Databricks avec Unity Catalog en utilisant le connecteur Python natif ou le pilote ODBC. Prend en charge l'authentification par jeton et une connectivité flexible.
image: /assets/logo_square.png
---

# Connecteur source pour Databricks - avec Unity Catalog

Ce guide décrit comment configurer *digna* pour se connecter à Databricks en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il se réfère à l'écran **"Create a Database Connection"**.

![Créer une connexion à la base de données](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) uniquement

> Pour les autres méthodes d'authentification, veuillez utiliser le pilote ODBC.

### Jeton d'accès personnel (PAT)

Pour vous authentifier en utilisant un jeton d'accès personnel, référez-vous à la documentation officielle de Databricks :  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Pilote natif)

Fournissez les informations suivantes dans l'écran **"Create a Database Connection"** :

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

## Pilote ODBC

Le pilote ODBC prend en charge un éventail plus large d'options d'authentification et de connectivité. Cette section se concentre sur l'authentification par jeton en utilisant le **Simba Spark ODBC Driver**.

### 1. Installer le pilote ODBC

Installez le **Simba Spark ODBC Driver** en suivant le guide d'installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant un Personal Access Token :

#### Étape 1
![Étape 1](images/databricks/create_odbc_data_source_step1.png)

#### Étape 2
![Étape 2](images/databricks/create_odbc_data_source_step2.png)

#### Étape 3
![Étape 3](images/databricks/create_odbc_data_source_step3.png)

#### Étape 4
![Étape 4](images/databricks/create_odbc_data_source_step4.png)

#### Étape 5 – Tester la connexion

Cliquez sur le bouton **TEST**. Une connexion réussie devrait ressembler à ceci :

![Étape 5](images/databricks/create_odbc_data_source_step5.png)

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit avec une configuration **sans DSN**.

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. Configuration sans DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

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