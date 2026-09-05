# Source Connector for PostgreSQL

Ce guide explique comment configurer *digna* pour se connecter à Postgres en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il fait référence à l'écran **"Create a Database Connection"**.

![Créer une connexion de base de données](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `psycopg`  
**Supported Authentication:** Password-based authentication only

> Pour d'autres méthodes d'authentification, veuillez utiliser le pilote ODBC.

### *digna* Configuration (Native Driver)

Fournissez les informations suivantes dans l'écran **"Create a Database Connection"** :

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Le pilote ODBC peut offrir une gamme plus large d'options d'authentification et de connectivité. Cette section se concentre sur l'authentification par mot de passe en utilisant le pilote **PostgreSQL Unicode(x64)**.

### 1. Installer le pilote ODBC

Installez **PostgreSQL Unicode(x64)** (ou équivalent) en suivant le guide d'installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l'authentification par mot de passe :

#### Step 1
![Étape 1](images/postgres/create_odbc_data_source_step1.png)

Remarque : si votre configuration de base de données exige de choisir un "SSLMode", assurez-vous de l'utiliser également lors de la définition d'une configuration sans DSN.

#### Step 2 – Test the connection

Cliquez sur le bouton **Test Connection**.

![Étape 2](images/postgres/create_odbc_data_source_step2.png)

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec une **DSN (Data Source Name)** soit avec une configuration **sans DSN**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "PostgreSQL35W"
```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```