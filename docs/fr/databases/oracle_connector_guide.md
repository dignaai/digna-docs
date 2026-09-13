---
title: Connecteur Oracle – Intégration de base de données | digna Documentation
description: Configurez digna pour se connecter à Oracle via ODBC avec une chaîne de connexion sans DSN. Couvre le pilote ODBC Oracle, le descripteur de connexion DBQ, les alias TNS et les paramètres de connexion côté digna.
image: /assets/logo_square.png
---


# Connecteur source pour Oracle

Ce guide décrit comment configurer *digna* pour se connecter à Oracle Database via **ODBC**, à
l'aide d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Oracle.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Le pilote ODBC Oracle fait partie du **client Oracle** (le paquet « ODBC » d'Instant Client
suffit). Installez-le sur la machine qui exécute le backend *digna*, en suivant le guide
d'installation officiel de l'éditeur.

Le pilote s'enregistre sous le nom **Oracle in `<OracleHomeName>`** — par exemple
`Oracle in OraDB21Home1` ou `Oracle in instantclient_21_13`. Le nom du home diffère d'une
installation à l'autre ; relevez donc le nom exact sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote ODBC Oracle, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du client, et le nom du pilote en particulier
    dépend du home Oracle présent sur votre hôte. Prenez ceci comme point de départ et consultez
    la documentation de la version du client que vous avez installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Driver` | `Oracle in OraDB21Home1` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `DBQ` | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | La base à laquelle se connecter — voir ci-dessous |
| `UID` | `DIGNA_SOURCE_USER` | Utilisateur de la base de données |
| `PWD` | `<password>` | Cochez **Encrypted** |

La chaîne de connexion obtenue ressemble à ceci :

```
Driver=Oracle in OraDB21Home1;DBQ=(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)));UID=DIGNA_SOURCE_USER;PWD=<password>
```

### La valeur de `DBQ`

`DBQ` accepte trois formes. Elles sont équivalentes pour *digna* ; elles diffèrent par ce qui
doit être configuré sur l'hôte *digna* :

| Forme | Exemple | Nécessite |
|---|---|---|
| **Descripteur de connexion complet** | `(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=db.example.com)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=digna_source_db)))` | Rien — tout est dans la propriété. Recommandé |
| **Alias TNS** | `DIGNA_SOURCE` | L'alias doit exister dans le `tnsnames.ora` du client Oracle installé sur l'hôte *digna* |
| **Easy Connect** | `db.example.com:1521/digna_source_db` | Un client Oracle prenant en charge Easy Connect (12c et versions ultérieures) |

!!! tip "Préférez le descripteur complet"

    Un alias TNS déplace la moitié de la définition de la connexion dans un fichier situé sur
    l'hôte *digna*, où il est facile de l'oublier lorsque l'hôte est reconstruit ou que *digna*
    est déplacé. Le descripteur complet garde la connexion autonome — ce qui est précisément
    l'intérêt d'une installation sans DSN.

Notez que les parenthèses d'un descripteur ne posent pas de problème dans une chaîne de
connexion, mais si votre mot de passe contient `;`, encadrez-le d'accolades :
`PWD={p@ss;word}`.

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Oracle
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "DIGNA_WORK"
```

---

## 4. Notes sur Oracle {: #4-notes-on-oracle }

- **Les schémas sont des utilisateurs.** *digna* liste les utilisateurs Oracle comme schémas ;
  le schéma source est donc le propriétaire des tables — `DIGNA_SOURCE_USER` dans l'exemple
  ci-dessus. L'utilisateur de la connexion a besoin de `SELECT` sur ces tables, directement ou
  via un rôle.
- **Une connexion voit une base de données.** Le catalogue proposé par *digna* est la base à
  laquelle la connexion est rattachée ; `DBQ` détermine donc quel service, et donc quelle base,
  est profilé.
- **Les identifiants sont sensibles à la casse une fois entre guillemets.** *digna* met entre
  guillemets les noms qu'il lit dans le dictionnaire de données, c'est-à-dire ce que stocke
  Oracle — en majuscules pour les objets non mis entre guillemets.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema** ;
  l'utilisateur a donc besoin de `CREATE TABLE` à cet endroit et d'un quota sur le tablespace.
  *Session* utilise une table temporaire privée (`ORA$PTT_…`, Oracle 18c et versions
  ultérieures) et ne touche pas à **Work Schema**. *Standard* ne nécessite qu'un accès en
  lecture.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le client Oracle, le nom du
service et vos identifiants fonctionnent avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Le **TNS Service Name** proposé ici provient du `tnsnames.ora` de votre installation cliente
Oracle — c'est là que sont définis l'alias et, avec lui, l'hôte, le port et le nom du service.
Dans *digna*, vous pouvez utiliser l'alias comme `DBQ`, ou bien le descripteur complet.

#### Étape 2 – Tester la connexion

Cliquez sur le bouton **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Indiquez le mot de passe et cliquez sur le bouton **OK**.

![Step 3](images/oracle/create_odbc_data_source_step3.png)

Un message de réussite confirme que le pilote et les identifiants fonctionnent.
