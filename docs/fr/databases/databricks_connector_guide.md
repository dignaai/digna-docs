---
title: Connecteur Databricks – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à Databricks avec Unity Catalog via ODBC et une chaîne de connexion sans DSN. Couvre le pilote ODBC Databricks, les jetons d'accès personnels, le chemin HTTP et les paramètres de connexion côté digna.
image: /assets/logo_square.png
---

# Connecteur source pour Databricks

Ce guide décrit comment configurer *digna* pour se connecter à Databricks via **ODBC**, à l'aide
d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Databricks.

!!! note "Unity Catalog est requis"

    *digna* lit les catalogues disponibles depuis `system.information_schema.catalogs` ;
    l'espace de travail doit donc avoir Unity Catalog activé. Les versions antérieures de
    *digna* proposaient une technologie distincte « Databricks Legacy » pour les espaces de
    travail sans Unity Catalog ; elle n'est plus disponible.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez le **Databricks ODBC Driver** sur la machine qui exécute le backend *digna*, en
suivant [le guide d'installation de Databricks](https://docs.databricks.com/aws/en/integrations/odbc/).

Selon la version, le pilote s'enregistre sous le nom **Simba Spark ODBC Driver** ou
**Databricks ODBC Driver**. Relevez le nom exact enregistré sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Rassembler les informations de connexion {: #2-gather-the-connection-details }

Toutes les valeurs proviennent de l'entrepôt SQL (ou du cluster) que *digna* doit utiliser.
Ouvrez-le dans l'espace de travail Databricks et allez dans **Connection details** :

| Champ Databricks | Utilisé comme |
|---|---|
| **Server hostname** | `Host` |
| **Port** | `Port`, normalement `443` |
| **HTTP path** | `HTTPPath` |

Pour l'authentification, créez un **jeton d'accès personnel** — voir
[Databricks personal access token authentication](https://docs.databricks.com/aws/en/dev-tools/auth/pat).
Les jetons appartiennent à un utilisateur ou à un principal de service, et ce principal a besoin
de `USE CATALOG`, `USE SCHEMA` et `SELECT` sur les données sources.

---

## 3. Propriétés ODBC {: #3-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote Databricks/Simba, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du pilote — le pilote a été renommé et ses
    options d'authentification étendues plus d'une fois — et selon les plateformes. Prenez ceci
    comme point de départ et consultez la documentation de la version du pilote que vous avez
    installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Driver` | `Simba Spark ODBC Driver` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `Host` | `<workspace>.cloud.databricks.com` | Nom d'hôte du serveur de l'entrepôt, par exemple `adb-1234567890123456.12.azuredatabricks.net` |
| `Port` | `443` | |
| `HTTPPath` | `/sql/1.0/warehouses/<warehouse-id>` | Chemin HTTP de l'entrepôt ou du cluster |
| `SSL` | `1` | Les points de terminaison Databricks sont exclusivement TLS |
| `ThriftTransport` | `2` | Transport HTTP, celui que parlent les points de terminaison SQL |
| `AuthMech` | `3` | Authentification par jeton |
| `UID` | `token` | Le mot littéral `token`, pas un nom d'utilisateur |
| `PWD` | `dapi…` | Le jeton d'accès personnel. Cochez **Encrypted** |
| `UseNativeQuery` | `1` | Transmet le SQL de *digna* sans modification — voir ci-dessous |

La chaîne de connexion obtenue ressemble à ceci :

```
Driver=Simba Spark ODBC Driver;Host=<workspace>.cloud.databricks.com;Port=443;HTTPPath=/sql/1.0/warehouses/<warehouse-id>;SSL=1;ThriftTransport=2;AuthMech=3;UID=token;PWD=dapi…;UseNativeQuery=1
```

!!! important "Conservez `UseNativeQuery=1`"

    Avec `UseNativeQuery=0` — la valeur par défaut du pilote — le pilote réécrit le SQL entrant
    dans ce qu'il estime être une syntaxe ODBC portable. *digna* génère déjà du SQL Databricks ;
    la réécriture peut donc modifier les guillemets obliques inverses et les littéraux de date,
    et le profilage échoue alors sur des instructions pourtant valides telles qu'elles sont
    écrites.

### OAuth au lieu d'un jeton

Pour un principal de service avec authentification OAuth machine à machine, remplacez
`AuthMech`, `UID` et `PWD` par :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `AuthMech` | `11` | OAuth |
| `Auth_Flow` | `1` | Informations d'identification client |
| `Auth_Client_ID` | `<application id>` | Principal de service |
| `Auth_Client_Secret` | `<client secret>` | Cochez **Encrypted** |

---

## 4. Configuration de *digna* {: #4-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Databricks
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 5. Notes sur Databricks {: #5-notes-on-databricks }

- **L'entrepôt doit être en cours d'exécution**, ou capable de démarrer, lorsque *digna* se
  connecte. Un entrepôt qui sort d'un état arrêté peut mettre plus de temps que le délai
  d'expiration de la connexion — si le test échoue à la première tentative après une période
  d'inactivité, réessayez.
- **Les catalogues viennent de l'espace de travail.** Contrairement à la plupart des
  technologies, une connexion Databricks atteint tous les catalogues que le principal est
  autorisé à voir, de sorte qu'une seule connexion peut desservir des sources réparties dans
  plusieurs catalogues.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema**, à
  l'intérieur du catalogue de la source ; le principal a donc besoin de `CREATE TABLE` à cet
  endroit. *Session* utilise `CREATE TEMPORARY TABLE` et ne touche pas à **Work Schema**.
  *Standard* ne nécessite qu'un accès en lecture.
- **Les entrepôts serverless fonctionnent** de la même manière ; seul `HTTPPath` diffère.

---

## 6. Vérifier le pilote (facultatif) {: #6-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le pilote, l'entrepôt et le
jeton fonctionnent avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Étape 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Étape 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Étape 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Étape 5 – Tester la connexion

Cliquez sur le bouton **TEST**. Une connexion réussie doit ressembler à ceci :

![Step 5](images/databricks/create_odbc_data_source_step5.png)

L'hôte, le chemin HTTP et le jeton saisis ici sont exactement les valeurs que prennent les
propriétés de la [section 3](#3-odbc-properties).
