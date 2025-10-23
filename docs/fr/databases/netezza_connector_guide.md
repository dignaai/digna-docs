---
title: Connecteur Netezza – Intégration de base de données | Documentation digna
description: Configurez digna pour se connecter à Netezza en utilisant le pilote ODBC NetezzaSQL. Prend en charge l’authentification par mot de passe avec des configurations DSN ou sans DSN pour une connectivité flexible.
image: /assets/logo_square.png
---


# Connecteur source pour Netezza

Ce guide décrit comment configurer *digna* pour se connecter à Netezza en utilisant le pilote ODBC.

Il fait référence à l’écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Pilote ODBC

Le pilote ODBC peut prendre en charge une gamme d’options d’authentification et de connectivité. Cette section se concentre sur l’authentification par mot de passe en utilisant le pilote **NetezzaSQL**.

### 1. Installer le pilote ODBC

Installez le pilote **NetezzaSQL** (ou similaire) en suivant le guide d’installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l’authentification par mot de passe :

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Selon votre pilote Netezza, les exigences d’installation et de sécurité, vous devrez peut-être aussi fournir des informations dans les onglets **Advanced DSN Options**, **SSL DSN Options** ou **Driver Options**. Pour la configuration la plus simple, il suffit de renseigner les données dans **DSN Options**.

Cliquez sur le bouton **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Lorsque vous obtenez l’écran de succès, ODBC est correctement configuré.

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)** soit avec une configuration **sans DSN**.

---

### A. Configuration basée sur DSN

#### Configuration de *digna*

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Configuration sans DSN

#### Configuration de *digna*

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```