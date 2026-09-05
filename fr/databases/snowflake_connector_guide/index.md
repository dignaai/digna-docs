# Connecteur source pour Snowflake

Ce guide décrit comment configurer *digna* pour se connecter à Snowflake en utilisant soit le connecteur Python natif, soit le driver ODBC.

Il fait référence à l'écran **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Bibliothèque :** `snowflake-connector-python`  
**Authentification prise en charge :** Authentification par mot de passe uniquement

> Pour d'autres méthodes d'authentification, utilisez le driver ODBC.

### Configuration *digna* (pilote natif)

Fournissez les informations suivantes dans l'écran **"Create a Database Connection"** :

```
Technologie:      Snowflake
Adresse Hôte:     Nom du compte Snowflake
Port Hôte:        Pas nécessaire
Nom Base de Données:   Base de données contenant le schéma source
Nom Schéma:       Schéma contenant les données source
Nom d'Utilisateur: Nom d'utilisateur et warehouse au format "user<@>warehouse"
Mot de Passe Utilisateur:   Mot de passe de l'utilisateur
Utiliser ODBC:        Désactivé (par défaut)
```

---

## Driver ODBC

Le driver ODBC peut prendre en charge un éventail plus large d'options d'authentification et de connectivité. Cette section se concentre sur l'authentification par mot de passe en utilisant le **SnowflakeDSIIDriver**.

### 1. Installer le driver ODBC

Installez le **SnowflakeDSIIDriver** en suivant le guide d'installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l'authentification par mot de passe :

#### Étape 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Remarques : 
- Si vous ne fournissez pas de valeurs pour Database, Schema et Warehouse, vous devrez les fournir comme propriétés ODBC lors de la configuration de la source de données dans *digna*.
- La valeur pour "Server" se compose du nom de votre compte Snowflake suivi de ".snowflakecomputing.com"

#### Étape 2 – Tester la connexion

Cliquez sur le bouton **TEST**. Une connexion réussie devrait ressembler à ceci :

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit avec une configuration sans DSN.

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez ce qui suit :

```
Technologie:      Snowflake
Nom Base de Données:   Base de données contenant le schéma source
Nom Schéma:     Schéma contenant les données source
Utiliser ODBC:        Activé
```

#### Propriétés ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionnellement:
name: "Database",       value: "Base de données contenant le schéma source"
name: "Schema",         value: "Schéma contenant les données source"
name: "Warehouse",      value: "Warehouse à utiliser pour l'exécution des SQLs"
```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre driver ODBC.

---

### B. Configuration sans DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez ce qui suit :

```
Technologie:      Snowflake
Nom Base de Données:   Schéma contenant les données source (identique au Nom Schéma)
Nom Schéma:     Schéma contenant les données source
Utiliser ODBC:        Activé
```

#### Propriétés ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Base de données contenant le schéma source"
name: "Schema",     value: "Schéma contenant les données source"
name: "Warehouse",  value: "Warehouse à utiliser pour l'exécution des SQLs"
```