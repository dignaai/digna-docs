# Connecteur source pour Oracle

Ce guide décrit comment configurer *digna* pour se connecter à Oracle DB en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il fait référence à l’écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Bibliothèque :** `python-oracledb`  
**Authentification prise en charge :** uniquement l’authentification par mot de passe

> Pour d’autres méthodes d’authentification, veuillez utiliser le pilote ODBC.

### Configuration *digna* (pilote natif)

Fournissez les informations suivantes dans l’écran **"Create a Database Connection"** :

```
Technology:      Oracle
Host Address:    Nom du serveur ou adresse IP
Host Port:       Numéro de port, p.ex. 1521
Database Name:   Nom de l'instance, nom du service
Schema Name:     Schéma contenant les données source
User Name:       Nom d'utilisateur de la base de données
User Password:   Mot de passe de l'utilisateur
Use ODBC:        Disabled (par défaut)
```

---

## Pilote ODBC

Le pilote ODBC peut prendre en charge une gamme plus large d’options d’authentification et de connectivité. Cette section se concentre sur l’authentification par mot de passe en utilisant le pilote **Oracle in OraDB21Home1**.

### 1. Installer le pilote ODBC

Installez **Oracle in OraDB21Home1** (ou un équivalent) en suivant le guide d’installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l’authentification par mot de passe :

#### Étape 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Remarque :
Le TNS Service Name doit être configuré dans le fichier tnsnames.ora de votre installation du client Oracle. C’est là que vous fournissez le descripteur de connexion (hôte, port, nom du service).

#### Étape 2 – Tester la connexion

Cliquez sur le bouton **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Saisissez le mot de passe et cliquez sur le bouton **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit avec une configuration **sans DSN (DSN-less)**.

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Oracle
Database Name:   Base de données contenant le schéma source
Schema Name:     Schéma contenant les données source
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "votre utilisateur oracle"
name: "PWD",            value: "{votre mot de passe entre accolades}"
```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. Configuration sans DSN (DSN-less)

#### Configuration *digna*

Dans l’écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Oracle
Database Name:   Schéma contenant les données source (identique à Schema Name)
Schema Name:     Schéma contenant les données source
Use ODBC:        Enabled
```

#### Propriétés ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "votre utilisateur oracle'
name: "PWD",        value: "votre mot de passe oracle"
```