---
title: Connecteur Azure Synapse – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à Azure Synapse Analytics en utilisant soit le pilote Python natif, soit le pilote ODBC. Prend en charge les pools SQL serverless et dédiés.
image: /assets/logo_square.png
---


# Connecteur source pour Azure Synapse Analytics

Ce guide décrit comment configurer *digna* pour se connecter à Azure Synapse Analytics en utilisant soit le connecteur Python natif, soit le pilote ODBC.
Il prend en charge les pools SQL serverless et dédiés.

Il fait référence à l’écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Bibliothèque :** `pymssql`  
**Authentification prise en charge :** Authentification par mot de passe uniquement

> Pour d’autres méthodes d’authentification, veuillez utiliser le pilote ODBC.

### Configuration *digna* (Pilote natif)

Fournissez les informations suivantes dans l’écran **"Create a Database Connection"** :

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Pilote ODBC

Le pilote ODBC peut prendre en charge une gamme plus large d’options d’authentification et de connectivité. Cette section se concentre sur l’authentification par mot de passe en utilisant le pilote **ODBC Driver 18 for SQL Server**.

### 1. Installer le pilote ODBC

Installez le pilote **ODBC Driver 18 for SQL Server** (ou équivalent) en suivant le guide d’installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l’authentification par mot de passe :

#### Étape 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Remplissez le champ "Server".
Utilisez le nom de l’espace de travail Synapse et ajoutez-y ".sql.azuresynapse.net".  
**Attention**, si vous souhaitez vous connecter en utilisant un pool SQL serverless, assurez-vous d’inclure "-ondemand" comme montré dans la capture d’écran ci‑dessous.

Cliquez sur le bouton **Next >**.

#### Étape 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Choisissez la méthode d’authentification (par exemple nom d’utilisateur et mot de passe)
et fournissez les informations requises.

Cliquez sur le bouton **Next >**.

#### Étape 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Choisissez les paramètres compatibles ANSI puis cliquez sur le bouton **Next >**.

#### Étape 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Vous pouvez laisser les paramètres par défaut ou choisir les options nécessaires 
puis cliquer sur le bouton **Finish**. 

#### Étape 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Cliquez maintenant sur le bouton ** Test datasource **.

#### Étape 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Lorsque vous voyez l’écran de succès, l’ODBC est correctement configuré.

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit sans DSN (DSN-less).

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. Configuration sans DSN (DSN-less)

#### Configuration *digna*

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Remarque** concernant la propriété SERVER :  
Utilisez le nom de l’espace de travail Synapse et ajoutez-y ".sql.azuresynapse.net". Si vous souhaitez vous connecter en utilisant un pool SQL serverless, assurez-vous d’inclure "-ondemand" comme montré dans la capture d’écran ci‑dessous.