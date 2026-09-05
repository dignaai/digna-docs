# Connecteur source pour Teradata

Ce guide explique comment configurer *digna* pour se connecter à Teradata en utilisant soit le connecteur Python natif, soit le pilote ODBC.

Il se réfère à l'écran **"Create a Database Connection"**.

![Créer une connexion à une base de données](images/data_source_config_input_mask.png)

---

## Pilote Python natif

**Bibliothèque :** `teradatasql`  
**Authentification prise en charge :** uniquement l'authentification par mot de passe

> Pour d'autres méthodes d'authentification, veuillez utiliser le pilote ODBC.

### Configuration *digna* (pilote natif)

Fournissez les informations suivantes dans l'écran **"Create a Database Connection"** :

```
Technology:      Teradata
Host Address:    Nom du serveur ou adresse IP
Host Port:       Numéro de port, p. ex. 1025
Database Name:   Nom de la base de données
Schema Name:     Nom de la base de données
User Name:       Nom d'utilisateur de la base de données
User Password:   Mot de passe de l'utilisateur
Use ODBC:        Désactivé (par défaut)
```

---

## Pilote ODBC

Le pilote ODBC peut prendre en charge un plus large éventail d'options d'authentification et de connectivité. Cette section se concentre sur l'authentification par mot de passe en utilisant le pilote **Teradata Database ODBC Driver 20.00**.

### 1. Installer le pilote ODBC

Installez le pilote **Teradata Database ODBC Driver 20.00** (ou similaire) en suivant le guide d'installation officiel du fournisseur.

### 2. Configurer la source de données ODBC

Suivez ces étapes pour configurer une nouvelle source de données ODBC en utilisant l'authentification par mot de passe :

#### Étape 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Cliquez sur le bouton **Test**.

#### Étape 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Saisissez le nom d'utilisateur et le mot de passe.

Cliquez sur le bouton **OK**.  
Lorsque l'écran de réussite s'affiche, ODBC est correctement configuré.

---

Vous pouvez maintenant configurer *digna* pour utiliser la connexion ODBC, soit avec un **DSN (Data Source Name)**, soit avec une configuration **sans DSN (DSN-less)**.

---

### A. Configuration basée sur DSN

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Teradata
Database Name:   Base de données qui contient le schéma source
Schema Name:     Schéma qui contient les données sources
Use ODBC:        Activé
```

#### Propriétés ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "votre utilisateur de base de données"
name: "PWD",        value: "votre mot de passe de base de données"
```

> Le `DSN` doit correspondre au nom défini dans la configuration de votre pilote ODBC.

---

### B. Configuration sans DSN (DSN-less)

#### Configuration *digna*

Dans l'écran **"Create a Database Connection"**, fournissez les éléments suivants :

```
Technology:      Teradata
Database Name:   Schéma qui contient les données sources (identique à Schema Name)
Schema Name:     Schéma qui contient les données sources
Use ODBC:        Activé
```

#### Propriétés ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "nom de votre serveur ou adresse IP"
name: "UID",        value: "votre utilisateur de base de données"
name: "PWD",        value: "votre mot de passe de base de données"
```