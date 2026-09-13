---
title: Connecteur PostgreSQL – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à PostgreSQL via ODBC avec une chaîne de connexion sans DSN. Couvre le pilote psqlODBC, les propriétés ODBC requises, les modes SSL et les paramètres de connexion côté digna.
image: /assets/logo_square.png
---


# Connecteur source pour PostgreSQL

Ce guide décrit comment configurer *digna* pour se connecter à PostgreSQL via **ODBC**, à l'aide
d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à PostgreSQL.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez le pilote ODBC PostgreSQL (**psqlODBC**) sur la machine qui exécute le backend
*digna*, en suivant le guide d'installation officiel de l'éditeur.

Le pilote s'enregistre sous un nom qui diffère selon la plateforme et le paquet — le plus
souvent **PostgreSQL Unicode(x64)** sous Windows et **PostgreSQL ODBC Driver(UNICODE)** sous
Linux. Relevez le nom exact sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver), et utilisez ce nom
pour la propriété `DRIVER` ci-dessous.

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote psqlODBC, donc leurs noms, leurs valeurs par défaut et les valeurs
    acceptées diffèrent selon les versions du pilote et les plateformes, et ce que votre serveur
    exige — SSL en particulier — peut différer également. Prenez ceci comme point de départ et
    consultez la documentation de la version du pilote que vous avez installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `SERVER` | `db.example.com` | Nom du serveur ou adresse IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Base de données contenant les schémas sources. C'est la seule base que cette connexion peut profiler |
| `UID` | `digna_source_user` | Utilisateur de la base de données |
| `PWD` | `<password>` | Cochez **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` ou `verify-full` — doit être accepté par le serveur |

La chaîne de connexion obtenue ressemble à ceci :

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Toute autre option psqlODBC peut être ajoutée comme propriété supplémentaire — par exemple
`ReadOnly=1` pour une session en lecture seule, ou `ConnSettings` pour exécuter des instructions
`SET` à la connexion.

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notes sur PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` doit correspondre au serveur.** Un serveur configuré avec `hostssl` rejette
  `SSLMode=disable`, et `verify-ca` ou `verify-full` exigent en outre que le certificat racine
  soit accessible au pilote sur l'hôte *digna*. Si vous avez dû choisir un mode particulier lors
  du test du pilote, utilisez le même ici.
- **Une connexion voit une base de données.** *digna* propose les schémas de la base nommée dans
  `DATABASE`, car PostgreSQL ne signale que la base courante comme catalogue. Les tables sources
  situées dans une autre base nécessitent leur propre connexion.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema**,
  l'utilisateur a donc besoin de `CREATE` sur ce schéma. *Session* utilise
  `CREATE TEMPORARY TABLE` et ne touche pas à **Work Schema**. *Standard* ne nécessite qu'un
  accès en lecture.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le pilote fonctionne et que
le serveur accepte vos identifiants et votre mode SSL avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Étape 2 – Tester la connexion

Cliquez sur le bouton **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Les valeurs que vous avez saisies ici sont exactement celles que prennent les propriétés de la
[section 2](#2-odbc-properties).
