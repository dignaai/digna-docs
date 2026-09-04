---
title: Connecteur MS SQL Server – Intégration de base de données | Documentation digna
description: Configurez digna pour se connecter à Microsoft SQL Server en utilisant le pilote Python pymssql ou le pilote ODBC SQL Server. Prend en charge l'authentification par mot de passe avec des configurations DSN ou sans DSN.
image: /assets/logo_square.png
---


# Connecteur source pour MS SQL Server

Ce guide décrit comment configurer *digna* pour se connecter à SQL Server en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il fait référence à l'écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Library:** `pymssql`  
**Authentification prise en charge :** uniquement l’authentification par mot de passe

> Pour d’autres méthodes d’authentification, veuillez utiliser le pilote ODBC.

### Configuration *digna* (Pilote natif)

Fournissez les informations suivantes dans l'écran **"Create a Database Connection"** :

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Pilote ODBC

Le pilote ODBC peut offrir une gamme plus large d’options d’authentification et de connectivité. Cette section se concentre sur l’authentification par mot de passe en utilisant le pilote **SQL Server**.

### 1. Installer le pilote ODBC

Installez le pilote **SQL Server** (ou équivalent) en suivant le guide d’installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l’authentification par mot de passe :

#### Étape 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Cliquez sur le bouton **Next >**.

#### Étape 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Choisissez la méthode d’authentification (par ex. nom d’utilisateur et mot de passe) et fournissez les données requises.

Cliquez sur le bouton **Next >**.

#### Étape 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Choisissez les paramètres compatibles ANSI puis cliquez sur le bouton **Next >**.

#### Étape 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Vous pouvez laisser les paramètres par défaut ou choisir les options de journalisation selon vos besoins, puis cliquer sur le bouton **Finish**.

#### Étape 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Cliquez maintenant sur le bouton ** Test datasource **.

#### Étape 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Lorsque vous obtenez l’écran de réussite, l’ODBC est correctement configuré.

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit avec une configuration **sans DSN**.

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. Configuration sans DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```