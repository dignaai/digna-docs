# Connecteur source pour Hive

Ce guide décrit comment configurer *digna* pour se connecter à Apache Hive via **ODBC**, à
l'aide d'une chaîne de connexion **sans DSN**.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Hive.

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez le **Cloudera ODBC Driver for Apache Hive** sur la machine qui exécute le backend
*digna*, en suivant le guide d'installation officiel de l'éditeur.

Relevez le nom exact du pilote enregistré sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote Cloudera Hive, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du pilote et les plateformes, et ce que
    HiveServer2 accepte dépend entièrement de la manière dont le cluster est sécurisé —
    mécanisme d'authentification, mode de transport, TLS, passerelle. Prenez ceci comme point de
    départ et consultez la documentation de la version du pilote que vous avez installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `DRIVER` | `Cloudera ODBC Driver for Apache Hive` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `HOST` | `hive.example.com` | Nom d'hôte ou adresse IP de HiveServer2 |
| `PORT` | `10000` | Port de HiveServer2 ; `10001` pour le transport HTTP |

La chaîne de connexion obtenue ressemble à ceci :

```
DRIVER=Cloudera ODBC Driver for Apache Hive;HOST=hive.example.com;PORT=10000
```

### Authentification

Un HiveServer2 non sécurisé accepte les trois propriétés ci-dessus telles quelles. Lorsque
l'authentification est activée, ajoutez :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `AuthMech` | `3` | `0` aucune authentification, `2` nom d'utilisateur uniquement, `3` nom d'utilisateur et mot de passe, `1` Kerberos |
| `UID` | `digna_source_user` | Requis pour `AuthMech` `2` et `3` |
| `PWD` | `<password>` | Requis pour `AuthMech` `3`. Cochez **Encrypted** |

Pour Kerberos (`AuthMech=1`), l'hôte *digna* a en outre besoin d'un ticket ou d'un keytab
valide, ainsi que des propriétés `KrbHostFQDN`, `KrbServiceName` et `KrbRealm` documentées par
le pilote.

### Transport et TLS

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `ThriftTransport` | `2` | `0` binaire (valeur par défaut, port 10000), `1` SASL, `2` HTTP (port 10001, et ce qu'attend une passerelle Knox) |
| `HTTPPath` | `cliservice` | Avec `ThriftTransport=2` |
| `SSL` | `1` | Lorsque HiveServer2 est sécurisé par TLS |
| `Schema` | `dignadata` | Base Hive dans laquelle la session démarre. Facultatif — *digna* qualifie ses requêtes |

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Hive
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Hive database for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notes sur Hive {: #4-notes-on-hive }

- **Les catalogues viennent du pilote.** Hive n'a pas de catalogue propre, *digna* reprend donc
  ce que signale le pilote — normalement une seule entrée nommée `HIVE` — et liste les bases
  Hive comme schémas en dessous.
- **Work Schema est une base Hive.** Pour le profilage *Permanent*, l'utilisateur doit y avoir
  le droit de créer et de supprimer des tables, et l'emplacement de stockage sous-jacent doit
  être accessible en écriture.
- **Modes de profilage.** *Permanent* crée les tables de travail dans **Work Schema**. *Session*
  utilise `CREATE TEMPORARY TABLE`, ce qui exige un HiveServer2 prenant en charge les tables
  temporaires, et ne touche pas à **Work Schema**. *Standard* ne nécessite qu'un accès en
  lecture, et c'est le mode à choisir sur un cluster où *digna* n'a aucun accès en écriture.
- **Le profilage est un ensemble de requêtes, pas une analyse séquentielle.** Chaque statistique
  est calculée par HiveServer2 ; la file d'attente dans laquelle l'utilisateur de *digna*
  soumet doit donc disposer d'une capacité suffisante pour la fenêtre d'inspection.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais la
boîte de dialogue du pilote est un moyen pratique de confirmer que le pilote, le mode de
transport et vos identifiants fonctionnent avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/hive/create_odbc_data_source_step1.png)

Les champs **Host**, **Port**, **Database**, **Mechanism** et **Thrift Transport** correspondent
ici aux propriétés `HOST`, `PORT`, `Schema`, `AuthMech` et `ThriftTransport` de la
[section 2](#2-odbc-properties).

#### Étape 2 – Tester la connexion

Indiquez le mot de passe et cliquez sur le bouton **Test**.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Après un test réussi, cliquez sur le bouton **OK**.