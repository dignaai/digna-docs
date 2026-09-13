# Connecteur source pour MS SQL Server

Ce guide décrit comment configurer *digna* pour se connecter à Microsoft SQL Server via
**ODBC**, à l'aide d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse se configure également comme une connexion SQL Server, avec un nom d'hôte différent
    et quelques considérations supplémentaires — voir
    [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez **ODBC Driver 18 for SQL Server** sur la machine qui exécute le backend *digna*, en
suivant [le guide d'installation de Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Le pilote livré avec Windows sous le nom simple **SQL Server** fonctionne également, mais il est
depuis longtemps dépassé et ne prend en charge ni les paramètres TLS modernes ni
l'authentification Azure. Ne l'utilisez que là où l'installation du pilote actuel n'est pas
envisageable.

Relevez le nom exact du pilote enregistré sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote ODBC Microsoft, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du pilote — Driver 18 chiffre par défaut, ce
    que ne faisait pas Driver 17 — et selon les plateformes. Prenez ceci comme point de départ
    et consultez la documentation de la version du pilote que vous avez installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `SERVER` | `sql.example.com` | Nom du serveur ou adresse IP. Instances nommées : `host\instance` ; port non standard : `host,1433` |
| `PORT` | `1433` | À omettre lorsque le port fait déjà partie de `SERVER` |
| `DATABASE` | `digna_source_db` | Base de données contenant les schémas sources. C'est la seule base que cette connexion peut profiler |
| `UID` | `digna_source_user` | Utilisateur de la base de données |
| `PWD` | `<password>` | Cochez **Encrypted** |

La chaîne de connexion obtenue ressemble à ceci :

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Chiffrement avec ODBC Driver 18

Driver 18 chiffre les connexions par défaut et valide le certificat du serveur. Face à un
serveur dont le certificat n'est pas approuvé par votre hôte *digna* — un certificat
auto-signé, typiquement — la connexion échoue avec une erreur de chaîne de certification.
Ajoutez :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Encrypt` | `yes` | Valeur par défaut dans Driver 18 ; ne mettez `no` que si le serveur ne sait pas faire de TLS |
| `TrustServerCertificate` | `yes` | Ignore la validation du certificat. Pratique en environnement de test ; préférez installer le certificat en production |

### Authentification Windows

Pour vous connecter avec le compte qui exécute le service *digna* plutôt qu'avec un identifiant
SQL, supprimez `UID` et `PWD` et ajoutez :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Trusted_Connection` | `yes` | Le compte de service *digna* doit disposer des droits sur la base |

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notes sur MS SQL Server {: #4-notes-on-ms-sql-server }

- **Une connexion voit une base de données.** *digna* propose les schémas de la base nommée dans
  `DATABASE`, car SQL Server ne signale que la base courante comme catalogue. Les tables sources
  situées dans une autre base nécessitent leur propre connexion.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema** ;
  l'utilisateur a donc besoin de `CREATE TABLE` à cet endroit. *Session* utilise des tables
  temporaires locales (`#wt_…`) dans `tempdb` et ne touche pas à **Work Schema**. *Standard* ne
  nécessite qu'un accès en lecture.
- **`SERVER` porte l'instance et le port.** Avec une instance nommée, `host\instance` exige que
  le service SQL Server Browser soit joignable ; `host,port` évite cela.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais
l'assistant du pilote est un moyen pratique de confirmer que le pilote fonctionne et que le
serveur accepte vos identifiants avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Cliquez sur le bouton **Next >**.

#### Étape 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Choisissez la méthode d'authentification (par exemple nom d'utilisateur et mot de passe)
et fournissez les données requises.

Cliquez sur le bouton **Next >**.

#### Étape 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Choisissez les paramètres conformes à ANSI puis cliquez sur le bouton **Next >**.

#### Étape 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Vous pouvez conserver les paramètres par défaut ou choisir des options de journalisation selon
vos besoins, puis cliquer sur le bouton **Finish**.

#### Étape 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Cliquez maintenant sur le bouton **Test datasource**.

#### Étape 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Un écran de réussite confirme que le pilote et les identifiants fonctionnent. Les valeurs que
vous avez saisies sont exactement celles que prennent les propriétés de la
[section 2](#2-odbc-properties).