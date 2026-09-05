# Connecteur source pour Hive

Ce guide décrit comment configurer *digna* pour se connecter à Hive en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il fait référence à l'écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Library:** `PyHive`  
**Supported Authentication:** authentification par mot de passe uniquement

> Pour les autres méthodes d'authentification, veuillez utiliser le pilote ODBC.

### Configuration *digna* (pilote natif)

Fournissez les informations suivantes dans l'écran **"Create a Database Connection"** :

```
Technology:      Apache Hive
Host Address:    Nom du serveur ou adresse IP
Host Port:       Numéro de port, p.ex. 10000
Database Name:   Schéma contenant les données sources
Schema Name:     Schéma contenant les données sources
User Name:       Nom d'utilisateur de la base de données
User Password:   Mot de passe de l'utilisateur
Use ODBC:        Désactivé (par défaut)
```

---

## Pilote ODBC

Le pilote ODBC peut prendre en charge une gamme plus large d'options d'authentification et de connectivité. Cette section se concentre sur l'authentification par mot de passe en utilisant le pilote **Cloudera ODBC Driver for Apache Hive**.

### 1. Installer le pilote ODBC

Installez le **Cloudera ODBC Driver for Apache Hive** (ou un équivalent) en suivant le guide d'installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l'authentification par mot de passe :

#### Étape 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Étape 2 – Tester la connexion

Saisissez le mot de passe et cliquez sur le bouton **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Après un test réussi, cliquez sur le bouton **OK**.

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit en configuration **sans DSN**.

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Apache Hive
Database Name:   Schéma contenant les données sources (identique à Schema Name)
Schema Name:     Schéma contenant les données sources
Use ODBC:        Activé
```

#### Propriétés ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{votre mot de passe entre accolades}"
```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. Configuration sans DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Apache Hive
Database Name:   Schéma contenant les données sources (identique à Schema Name)
Schema Name:     Schéma contenant les données sources
Use ODBC:        Activé
```

#### Propriétés ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "votre nom de serveur ou adresse IP"
name: "PORT",       value: "Numéro de port, p.ex. 10000"
name: "Schema",     value: "Schéma contenant les données sources"
name: "UID",        value: "votre utilisateur Hive"
name: "PWD",        value: "votre mot de passe Hive"
name: "AuthMech",   value: "3"
```