# Connecteur source pour Azure Synapse Analytics

Ce guide décrit comment configurer *digna* pour se connecter à Azure Synapse Analytics via
**ODBC**, à l'aide d'une chaîne de connexion **sans DSN**. Les pools SQL serverless et dédiés
sont tous deux pris en charge.

La partie digna de la configuration est identique pour toutes les technologies — où les
connexions sont créées, comment les valeurs des propriétés sont chiffrées, comment une connexion
est testée et ce que signifient les modes de profilage. Elle est décrite dans
[Vue d'ensemble des connexions aux bases de données](overview.md). Cette page traite de ce qui
est spécifique à Azure Synapse.

!!! note "Technologie"

    Synapse parle le dialecte SQL Server ; la connexion se crée donc avec **Technology:
    SQL Server**. Pour un serveur sur site, voir [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Installer le pilote ODBC {: #1-install-the-odbc-driver }

Installez **ODBC Driver 18 for SQL Server** sur la machine qui exécute le backend *digna*, en
suivant [le guide d'installation de Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
et relevez le nom exact du pilote enregistré sur votre hôte comme décrit dans
[Installer le pilote ODBC sur l'hôte digna](overview.md#install-the-driver).

---

## 2. Propriétés ODBC {: #2-odbc-properties }

!!! important "Un exemple, pas une spécification"

    L'ensemble ci-dessous est une combinaison dont on sait qu'elle fonctionne. Les propriétés
    appartiennent au pilote ODBC Microsoft, donc leurs noms, leurs valeurs par défaut et les
    valeurs acceptées diffèrent selon les versions du pilote et les plateformes, et ce
    qu'exige l'espace de travail dépend de sa configuration — type de pool, méthode
    d'authentification, pare-feu. Prenez ceci comme point de départ et consultez la
    documentation de la version du pilote que vous avez installée.

Ajoutez les propriétés suivantes dans l'écran **Add DB Connection** :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Doit correspondre au nom du pilote enregistré sur l'hôte *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Nom de l'espace de travail suivi du suffixe de point de terminaison — voir ci-dessous |
| `DATABASE` | `dignadata` | Base de données contenant les schémas sources. C'est la seule base que cette connexion peut profiler |
| `UID` | `sqladminuser` | Identifiant SQL |
| `PWD` | `<password>` | Cochez **Encrypted** |

La chaîne de connexion obtenue ressemble à ceci :

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### La valeur de `SERVER`

Prenez le nom de l'espace de travail Synapse et ajoutez-y le suffixe du point de terminaison :

| Pool | `SERVER` |
|---|---|
| **Pool SQL serverless** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Pool SQL dédié** | `<workspace>.sql.azuresynapse.net` |

!!! warning "La partie `-ondemand` est facile à oublier"

    Sans elle, le nom se résout vers le point de terminaison dédié, et la connexion échoue ou
    atteint silencieusement un pool différent de celui prévu. Les deux points de terminaison
    sont affichés sur la page de vue d'ensemble de l'espace de travail dans le portail Azure.

### Pare-feu

Le pare-feu de l'espace de travail Synapse doit autoriser l'adresse sortante de l'hôte *digna*.
Ajoutez-la sous **Networking** dans l'espace de travail avant de tester la connexion — une
adresse bloquée se manifeste par un dépassement de délai plutôt que par une erreur
d'authentification.

### Authentification Microsoft Entra ID

Au lieu d'un identifiant SQL, le pilote peut s'authentifier auprès d'Entra ID. Remplacez
`UID`/`PWD` par la méthode d'authentification attendue par votre espace de travail, par
exemple :

| Clé | Valeur d'exemple | Notes |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` prend alors l'ID d'application (client) et `PWD` le secret client |
| `Authentication` | `ActiveDirectoryMSI` | Identité managée de l'hôte *digna*, aucun identifiant nécessaire |

---

## 3. Configuration de *digna* {: #3-digna-configuration }

Dans l'écran **Add DB Connection**, renseignez les éléments suivants :

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Notes sur Azure Synapse {: #4-notes-on-azure-synapse }

- **Les pools serverless ne prennent en charge que le profilage *Standard*.** Un pool SQL
  serverless ne peut pas créer de tables dans une base de données ; ni le profilage *Permanent*
  ni le profilage *Session* ne peuvent donc s'exécuter. *Standard* calcule les métriques
  directement sur la source, ce qui est aussi l'option la moins coûteuse, le serverless étant
  facturé au volume de données traité.
- **Une connexion voit une base de données.** *digna* propose les schémas de la base nommée dans
  `DATABASE`, car Synapse, comme SQL Server, ne signale que la base courante comme catalogue.
- **Le chiffrement est actif par défaut** dans Driver 18 et les points de terminaison Synapse
  présentent des certificats publics valides ; aucune propriété `Encrypt` ou
  `TrustServerCertificate` n'est donc nécessaire.
- **Un point de terminaison serverless peut sortir de veille** à la première connexion. Si le
  test de connexion expire sur un pool inutilisé depuis un certain temps, réessayez.

---

## 5. Vérifier le pilote (facultatif) {: #5-verifying-the-driver-optional }

Configurer une source de données ODBC n'est pas nécessaire pour une connexion sans DSN, mais
l'assistant du pilote est un moyen pratique de confirmer que le pilote fonctionne et que
l'espace de travail accepte vos identifiants avant de les saisir dans *digna*.

#### Étape 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Remplissez le champ « Server ».
Utilisez le nom de l'espace de travail Synapse et complétez-le par « .sql.azuresynapse.net ».  
**Attention**, si vous souhaitez vous connecter via un pool SQL serverless, veillez à inclure
« -ondemand » comme sur la capture d'écran ci-dessus.

Cliquez sur le bouton **Next >**.

#### Étape 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Choisissez la méthode d'authentification (par exemple nom d'utilisateur et mot de passe)
et fournissez les données requises.

Cliquez sur le bouton **Next >**.

#### Étape 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Choisissez les paramètres conformes à ANSI puis cliquez sur le bouton **Next >**.

#### Étape 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Vous pouvez conserver les paramètres par défaut ou choisir des options selon vos besoins,
puis cliquer sur le bouton **Finish**.

#### Étape 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Cliquez maintenant sur le bouton **Test datasource**.

#### Étape 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Un écran de réussite confirme que le pilote, le point de terminaison et les identifiants
fonctionnent. Les valeurs que vous avez saisies sont exactement celles que prennent les
propriétés de la [section 2](#2-odbc-properties).