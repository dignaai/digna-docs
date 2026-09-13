---
title: Connecteur Netezza – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à Netezza via ODBC avec une chaîne de connexion sans DSN. Couvre le pilote NetezzaSQL, les propriétés ODBC requises et les paramètres de connexion côté digna.
image: /assets/logo_square.png
---


# Connecteur source pour Netezza

Ce guide décrit comment configurer *digna* pour se connecter à Netezza via **ODBC**, à l'aide
d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Netezza.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez le pilote ODBC **NetezzaSQL** (fourni avec les outils client IBM Netezza) sur la
machine qui exécute le backend *digna*, en suivant le guide d'installation officiel de
l'éditeur.

Relevez le nom exact du pilote enregistré sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote NetezzaSQL, donc leurs noms, leurs valeurs par défaut et les valeurs
    acceptées diffèrent selon les versions du client et les plateformes, et une appliance
    sécurisée par TLS nécessite davantage que les propriétés présentées ici. Prenez ceci comme
    point de départ et consultez la documentation de la version du client que vous avez
    installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `DRIVER` | `{NetezzaSQL}` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna*. Les accolades sont la manière habituelle d'écrire ce nom |
| `SERVER` | `netezza.example.com` | Nom du serveur ou adresse IP |
| `PORT` | `5480` | |
| `DATABASE` | `TEST` | Base de données dans laquelle la session démarre |
| `UID` | `ADMIN` | Utilisateur de la base de données |
| `PWD` | `<password>` | Cochez **Encrypted** |

La chaîne de connexion obtenue ressemble à ceci :

```
DRIVER={NetezzaSQL};SERVER=netezza.example.com;PORT=5480;DATABASE=TEST;UID=ADMIN;PWD=<password>
```

Selon votre version de pilote, votre installation et vos exigences de sécurité, d'autres
propriétés peuvent être nécessaires — par exemple `SecurityLevel` et `CaCertFile` pour une
appliance sécurisée par TLS. Toute option proposée par les boîtes de dialogue *Advanced*, *SSL*
et *Driver* du pilote peut être ajoutée comme propriété.

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Notes sur Netezza {: #4-notes-on-netezza }

- **Les catalogues et les schémas s'appliquent tous deux.** *digna* liste comme catalogues les
  bases de données que l'utilisateur peut voir (depuis `_V_DATABASE`) et, en dessous, leurs
  schémas (depuis `_V_SCHEMA`), de sorte qu'une connexion peut desservir des sources réparties
  dans plusieurs bases. `DATABASE` détermine uniquement où la session démarre.
- **Les identifiants sont en majuscules**, sauf s'ils ont été créés entre guillemets — c'est
  pourquoi les exemples ci-dessus utilisent `TEST` et `ADMIN`.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema**,
  l'utilisateur a donc besoin de `CREATE TABLE` à cet endroit. *Session* utilise
  `CREATE TEMPORARY TABLE` et ne touche pas à **Work Schema**. *Standard* ne nécessite qu'un
  accès en lecture.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le pilote et vos identifiants
fonctionnent avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

Les champs de **DSN Options** correspondent un à un aux propriétés de la
[section 2](#2-odbc-properties). Selon votre pilote Netezza, votre installation et vos exigences
de sécurité, vous pourriez également avoir besoin de renseigner les onglets
**Advanced DSN Options**, **SSL DSN Options** ou **Driver Options** ; pour l'installation la
plus simple, **DSN Options** suffit.

Cliquez sur le bouton **Test Connection**.

#### Étape 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Lorsque l'écran de réussite s'affiche, le pilote fonctionne et les valeurs sont correctes.
