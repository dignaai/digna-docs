# Connecteur source pour Teradata

Ce guide décrit comment configurer *digna* pour se connecter à Teradata via **ODBC**, à l'aide
d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Teradata.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez le **ODBC Driver for Teradata** sur la machine qui exécute le backend *digna*, en
suivant le guide d'installation officiel de l'éditeur.

Le pilote s'enregistre avec sa version dans le nom, par exemple
**Teradata Database ODBC Driver 20.00**. Relevez le nom exact enregistré sur votre hôte comme
décrit dans [Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote ODBC Teradata, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du pilote — la version fait partie du nom du
    pilote lui-même — et selon les plateformes. Prenez ceci comme point de départ et consultez
    la documentation de la version du pilote que vous avez installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `DBCNAME` | `teradata.example.com` | Nom du serveur ou adresse IP. Nom donné par Teradata à la propriété d'hôte |
| `UID` | `digna_source_user` | Utilisateur de la base de données |
| `PWD` | `<password>` | Cochez **Encrypted** |

La chaîne de connexion obtenue ressemble à ceci :

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Propriétés supplémentaires utiles :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `MechanismName` | `TD2` | Mécanisme de connexion. `TD2` est la valeur par défaut de Teradata ; utilisez `LDAP` pour l'authentification par annuaire |
| `DefaultDatabase` | `dad` | Base de données dans laquelle la session démarre |
| `CharacterSet` | `UTF8` | À définir lorsque le jeu de caractères de session par défaut altérerait des données non ASCII |

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Notes sur Teradata {: #4-notes-on-teradata }

- **Une base de données Teradata est un catalogue, pas un schéma.** *digna* liste comme
  catalogues les bases que l'utilisateur peut voir (depuis `DBC.DatabasesV`), et le niveau
  schéma ne s'applique pas. Lorsque vous ajoutez une source de données, choisissez la base comme
  catalogue ; le schéma est signalé comme *non applicable*.
- **Une connexion atteint toutes les bases autorisées**, de sorte qu'une seule connexion peut
  desservir des sources réparties dans plusieurs bases — contrairement aux technologies où la
  connexion est rattachée à une seule base.
- **Work Schema est une base de données.** Pour le profilage *Permanent*, nommez la base
  Teradata qui contient les tables de travail et accordez à l'utilisateur le droit
  `CREATE TABLE` ainsi qu'une allocation d'espace `PERM` — une base sans espace perm ne peut pas
  héberger de table.
- **Modes de profilage.** *Permanent* crée les tables dans **Work Schema**. *Session* utilise
  une table `VOLATILE`, qui nécessite de l'espace `SPOOL` mais aucun espace perm ni aucun droit
  dans **Work Schema**. *Standard* ne nécessite qu'un accès en lecture.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le pilote et vos identifiants
fonctionnent avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Le champ **Name or IP address** correspond ici à la propriété `DBCNAME` de la
[section 2](#2-odbc-properties).

Cliquez sur le bouton **Test**.

#### Étape 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Indiquez le nom d'utilisateur et le mot de passe, puis cliquez sur le bouton **OK**. Un écran de
réussite confirme que le pilote et les identifiants fonctionnent.