---
title: Connecteur Snowflake – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à Snowflake via ODBC avec une chaîne de connexion sans DSN. Couvre le pilote ODBC Snowflake, les jetons d'accès programmatique, le choix de l'entrepôt et du rôle, et les paramètres de connexion côté digna.
image: /assets/logo_square.png
---


# Connecteur source pour Snowflake

Ce guide décrit comment configurer *digna* pour se connecter à Snowflake via **ODBC**, à l'aide
d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Snowflake.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez le **Snowflake ODBC Driver** sur la machine qui exécute le backend *digna*, en suivant
[le guide d'installation de Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Le pilote s'enregistre sous le nom **SnowflakeDSIIDriver**. Relevez le nom exact enregistré sur
votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

Snowflake est atteint au moyen d'un **jeton d'accès programmatique (PAT)** — la méthode
d'authentification sur laquelle *digna* est validé, et celle qu'exige Snowflake pour les comptes
où la connexion par mot de passe seul est bloquée.

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote ODBC Snowflake, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du pilote et les plateformes, et les options
    d'authentification autorisées par votre compte sont déterminées par la politique de sécurité
    de ce compte. Prenez ceci comme point de départ et consultez la documentation de la version
    du pilote que vous avez installée.

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identifiant du compte suivi du suffixe, par exemple `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Utilisateur Snowflake auquel appartient le jeton |
| `Database` | `TEST` | Base de données contenant les schémas sources. C'est la seule base que cette connexion peut profiler |
| `Schema` | `PUBLIC` | Schéma par défaut de la session |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Sélectionne l'authentification par jeton |
| `token` | `<programmatic access token>` | Cochez **Encrypted** |

La chaîne de connexion obtenue ressemble à ceci :

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Entrepôt et rôle

Les requêtes ont besoin d'un entrepôt. Si l'utilisateur *digna* dispose d'un entrepôt par défaut
et d'un rôle par défaut, la session les reprend et rien n'a besoin d'être configuré. Sinon,
ajoutez :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Entrepôt qui exécute les requêtes de profilage |
| `Role` | `DIGNA_READER` | Rôle dont la session utilise les privilèges |

!!! tip "Donnez à digna son propre entrepôt"

    Un entrepôt distinct, de petite taille et à suspension automatique garde le coût du
    profilage visible et empêche *digna* de concurrencer les utilisateurs interactifs pour les
    ressources de calcul.

### Authentification par mot de passe

Lorsque le compte l'autorise encore, un mot de passe fonctionne à la place du jeton —
supprimez `authenticator` et `token` et ajoutez :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `PWD` | `<password>` | Cochez **Encrypted** |

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Notes sur Snowflake {: #4-notes-on-snowflake }

- **Les jetons expirent.** Un jeton d'accès programmatique est émis avec une durée de vie, et le
  profilage s'arrête le jour où elle expire. Notez la date d'expiration au moment de la création
  et saisissez le nouveau jeton dans la propriété `token` — les valeurs chiffrées peuvent être
  remplacées mais pas relues.
- **Une connexion voit une base de données.** *digna* propose les schémas de la base nommée dans
  `Database`, car Snowflake ne signale que la base courante comme catalogue. Les tables sources
  situées dans une autre base nécessitent leur propre connexion.
- **Les identifiants sont en majuscules**, sauf s'ils ont été créés entre guillemets. *digna*
  utilise les noms tels que Snowflake les signale.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema** ; le rôle
  a donc besoin de `CREATE TABLE` à cet endroit. *Session* utilise `CREATE TEMPORARY TABLE` et
  ne touche pas à **Work Schema**. *Standard* ne nécessite qu'un accès en lecture — et aucun
  privilège d'écriture.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le pilote, l'URL du compte et
vos identifiants fonctionnent avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Remarques :

- La valeur de **Server** se compose de l'identifiant de votre compte Snowflake suivi de
  `.snowflakecomputing.com`.
- Les champs **Database**, **Schema** et **Warehouse** saisis ici correspondent aux propriétés
  `Database`, `Schema` et `Warehouse` de la [section 2](#2-odbc-properties).

#### Étape 2 – Tester la connexion

Cliquez sur le bouton **TEST**. Une connexion réussie doit ressembler à ceci :

![Step 2](images/snowflake/create_odbc_data_source_step2.png)
