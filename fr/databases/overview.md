# Vue d'ensemble des connexions aux bases de données

---

## Table des matières

1. [Comment fonctionnent les connexions](#how-connections-work)
2. [Guides par technologie](#technology-guides)
3. [Prérequis : installer le pilote ODBC sur l'hôte digna](#install-the-driver)
4. [Créer une connexion à une base de données](#create-a-database-connection)
5. [Propriétés ODBC](#odbc-properties)
6. [Chiffrer les valeurs des propriétés](#encrypting-property-values)
7. [Tester une connexion](#testing-a-connection)
8. [Quelle base de données la connexion voit](#which-database-the-connection-sees)
9. [Mode de profilage et Work Schema](#profiling-mode-and-work-schema)
10. [Utiliser un DSN à la place](#using-a-dsn-instead)
11. [Dépannage](#troubleshooting)

---

## Comment fonctionnent les connexions {: #how-connections-work }

*digna* atteint chaque technologie source via **ODBC**. Une connexion est une liste de
propriétés ODBC que vous saisissez sous forme de paires clé/valeur. Lorsque *digna* ouvre la
connexion, il assemble ces paires en une chaîne de connexion — `Key=Value`, séparées par `;`,
dans l'ordre où vous les avez listées — et la transmet au gestionnaire de pilotes ODBC de
l'hôte *digna*.

C'est le fait de saisir vous-même les propriétés qui rend la configuration **sans DSN** : la
connexion porte tout ce dont le pilote a besoin, de sorte qu'aucune source de données ODBC (DSN)
n'a à être enregistrée sur l'hôte. C'est la manière recommandée de configurer *digna*, car la
définition de la connexion réside entièrement dans *digna* et se déplace avec lui.

### Pourquoi ODBC {: #why-odbc }

Les versions antérieures offraient le choix entre un pilote par technologie et ODBC, sélectionné
au moyen d'un commutateur **Use ODBC**. À partir de la version 2026.06, *digna* s'appuie
uniquement sur ODBC. Une interface unique et standard apporte plus qu'un ensemble de pilotes sur
mesure :

- **Authentification** — l'authentification fait partie d'ODBC ; une connexion peut donc
  utiliser tout ce que son pilote prend en charge : mots de passe, jetons et PAT, Kerberos et
  Active Directory, MFA et authentification unique via navigateur, identités cloud, certificats
  client et TLS. Les nouvelles méthodes arrivent avec une mise à jour du pilote, sans attendre
  une version de *digna*.
- **Pilotes maintenus par les éditeurs de bases de données** — le pilote de l'éditeur suit les
  nouvelles versions du serveur et les correctifs de sécurité, et vous pouvez le mettre à jour à
  votre propre rythme, indépendamment de *digna*.
- **Une seule façon de tout configurer** — chaque technologie est une liste de propriétés
  clé/valeur, avec la même interface, le même chiffrement des valeurs sensibles et le même
  dépannage, au lieu d'un jeu de champs différent par source.
- **Réglage et portée** — les options du pilote telles que les délais d'attente, les paramètres
  TLS, les proxys et la taille des lots sont disponibles pour toutes les sources, et toute
  technologie disposant d'un pilote ODBC conforme peut être connectée, y compris celles pour
  lesquelles *digna* ne publie pas de guide dédié.

!!! note "Ce qui a changé dans l'interface"

    Le commutateur **Use ODBC** et les champs distincts hôte, port, base de données,
    utilisateur et mot de passe n'existent plus. Une connexion qui n'utilise pas déjà ODBC a
    besoin que ses propriétés ODBC soient saisies avant de fonctionner à nouveau — voir
    [Créer une connexion à une base de données](#create-a-database-connection).

---

## Guides par technologie {: #technology-guides }

Les noms des propriétés diffèrent selon le pilote, et chaque technologie présente un ou deux
détails que les autres n'ont pas. Les guides ci-dessous couvrent cette partie ; cette page
couvre la partie *digna*, qui est la même pour toutes.

!!! important "Les jeux de propriétés des guides sont des exemples"

    Chaque guide présente une combinaison dont on sait qu'elle fonctionne — celle sur laquelle
    *digna* est testé. C'est un point de départ, pas une spécification : les propriétés
    appartiennent au pilote ODBC, et lesquelles existent, comment elles s'appellent et quelles
    valeurs elles acceptent diffèrent selon les versions et les éditeurs de pilotes, entre
    Windows, Linux et macOS, et selon la configuration du serveur source — méthode
    d'authentification, TLS, passerelle, port. Attendez-vous à ajuster une valeur ou deux, et
    considérez la documentation de la version du pilote que vous avez installée comme faisant
    autorité.

| Technologie | Guide | À savoir |
|---|---|---|
| **Azure Synapse Analytics** | [Azure Synapse](azure_synapse_connector_guide.md) | Les pools serverless exigent `-ondemand` dans le nom d'hôte et ne prennent en charge que le profilage *Standard* |
| **Databricks** | [Databricks](databricks_connector_guide.md) | Authentification par jeton : `UID=token`, PAT dans `PWD` |
| **Apache Hive** | [Hive](hive_connector_guide.md) | Les catalogues viennent du pilote, pas d'une requête |
| **Netezza** | [Netezza](netezza_connector_guide.md) | Le nom du pilote est entre accolades : `{NetezzaSQL}` |
| **Oracle** | [Oracle](oracle_connector_guide.md) | `DBQ` accepte soit un descripteur de connexion complet, soit un alias `tnsnames.ora` |
| **PostgreSQL** | [PostgreSQL](postgres_connector_guide.md) | `SSLMode` doit correspondre à ce qu'exige le serveur |
| **MS SQL Server** | [MS SQL Server](sqlserver_connector_guide.md) | `DATABASE` détermine quels schémas *digna* peut voir |
| **Snowflake** | [Snowflake](snowflake_connector_guide.md) | Le jeton d'accès programmatique est la méthode d'authentification testée |
| **Teradata** | [Teradata](teradata_connector_guide.md) | L'hôte va dans `DBCNAME` ; les bases font office de schémas |

---

## Prérequis : installer le pilote ODBC sur l'hôte digna {: #install-the-driver }

*digna* ouvre les connexions sources depuis le **serveur qui exécute le backend digna**, pas
depuis le navigateur. Le pilote ODBC doit donc être installé sur cette machine, et son nom
enregistré auprès du gestionnaire de pilotes local.

=== "Windows"

    Installez le pilote 64 bits de l'éditeur, puis ouvrez l'**Administrateur de sources de
    données ODBC (64 bits)** et passez à l'onglet **Drivers**. Les noms qui y figurent sont
    exactement les valeurs que vous pouvez utiliser pour la propriété `Driver`.

=== "Linux"

    Installez **unixODBC** et le pilote de l'éditeur, puis listez les noms de pilotes
    enregistrés :

    ```bash
    odbcinst -q -d
    ```

    Les noms affichés entre crochets sont les valeurs que vous pouvez utiliser pour la propriété
    `Driver`. Ils proviennent de `/etc/odbcinst.ini` (ou du fichier que signale `odbcinst -j`).

=== "macOS"

    Installez **unixODBC** (par exemple avec `brew install unixodbc`) et le pilote de l'éditeur,
    puis listez les noms de pilotes enregistrés :

    ```bash
    odbcinst -q -d
    ```

!!! warning "Le nom du pilote doit correspondre caractère pour caractère"

    `Driver` est transmis tel quel au gestionnaire de pilotes. `Simba Spark ODBC Driver` et
    `Simba Spark ODBC Driver 64` sont des pilotes différents du point de vue du gestionnaire, et
    un nom non enregistré produit une erreur *data source name not found* alors même qu'aucun
    DSN n'est en jeu.

À la place d'un nom enregistré, tous les gestionnaires de pilotes courants acceptent également
le chemin complet vers la bibliothèque du pilote, par exemple
`Driver=/opt/simba/spark/lib/64/libsparkodbc_sb64.so`. C'est utile lorsque le pilote est
installé mais non enregistré.

---

## Créer une connexion à une base de données {: #create-a-database-connection }

Ouvrez l'**Admin Panel**, allez dans l'onglet **Database Connections** et cliquez sur
**Add DB Connection**. L'écran demande cinq éléments :

| Champ | Description |
|---|---|
| **Name** | Nom de la connexion. Il sert à référencer la connexion dans les autres écrans. |
| **Technology** | Postgres, Oracle, SQL Server, Databricks, Teradata, Netezza, Snowflake ou Hive. Sélectionne le dialecte SQL que *digna* génère ; il doit donc correspondre à la source — pas au pilote. Azure Synapse Analytics est une connexion **SQL Server**. |
| **ODBC Properties** | Les paires clé/valeur décrites dans [Propriétés ODBC](#odbc-properties). |
| **Profiling Mode** | *Standard*, *Permanent* ou *Session* — voir [Mode de profilage et Work Schema](#profiling-mode-and-work-schema). |
| **Work Schema** | Schéma qui contient les tables de travail pour le profilage *Permanent*. |

Une connexion est administrée de façon centralisée puis affectée à un ou plusieurs projets, de
sorte que la même connexion peut desservir plusieurs projets.

---

## Propriétés ODBC {: #odbc-properties }

Cliquez sur **Add Property** pour chaque propriété et renseignez **Key**, **Value** et, pour les
secrets, la case **Encrypted**. Chaque guide de technologie liste un jeu d'exemple pour la
technologie concernée, que vous adaptez à votre version de pilote et à votre serveur — voir
[la note ci-dessus](#technology-guides).

Quel que soit le pilote, un jeu de propriétés couvre les mêmes quatre éléments :

- **`Driver`** — le nom du pilote enregistré, comme décrit [ci-dessus](#install-the-driver).
- **L'adresse du serveur** — la clé diffère selon le pilote : `SERVER`, `HOST`, `DBCNAME`,
  `Server` ou, pour Oracle, le descripteur de connexion `DBQ`.
- **Les identifiants** — généralement `UID` et `PWD` ; Snowflake utilise `UID` plus un `token`,
  et Databricks l'utilisateur littéral `token` plus le jeton d'accès personnel dans `PWD`.
- **La base ou le catalogue dans lequel travailler**, lorsque la technologie en possède un —
  voir [Quelle base de données la connexion voit](#which-database-the-connection-sees).

Tout ce que le pilote documente par ailleurs peut être ajouté de la même manière — pool de
connexions, délais d'expiration de socket, paramètres Kerberos, paramètres de proxy. *digna*
n'interprète pas les propriétés ; il ne fait que les transmettre.

!!! warning "Les valeurs ne sont pas échappées — encadrez d'accolades tout ce qui contient un point-virgule"

    Comme les propriétés sont assemblées avec `;`, une valeur contenant elle-même `;` diviserait
    la chaîne de connexion au mauvais endroit. Encadrez ces valeurs d'accolades :
    `PWD={p@ss;word}`. Il en va de même pour les valeurs contenant `=` ou des espaces en tête.
    C'est aussi pourquoi certains pilotes s'écrivent par convention entre accolades, comme
    `{NetezzaSQL}` ou `{SnowflakeDSIIDriver}`.

---

## Chiffrer les valeurs des propriétés {: #encrypting-property-values }

Cochez **Encrypted** pour chaque propriété contenant un secret — `PWD`, `token`, un secret
client. La valeur est alors chiffrée avant d'être stockée dans le référentiel *digna*, masquée à
l'écran, et déchiffrée uniquement au moment de l'assemblage de la chaîne de connexion.

!!! tip "Conseil"

    Une valeur chiffrée ne peut pas être relue, ni dans l'interface ni via l'API — elle peut
    seulement être remplacée. Conservez également les secrets dans votre propre gestionnaire de
    mots de passe.

Les propriétés qui ne sont pas secrètes — nom du pilote, hôte, port, base de données — sont à
laisser de préférence non chiffrées, afin qu'elles restent lisibles pour la personne qui
maintiendra la connexion par la suite.

---

## Tester une connexion {: #testing-a-connection }

Cliquez sur **Test** dans la boîte de dialogue *Add DB Connection* **avant** d'enregistrer. Le
test utilise les valeurs actuellement présentes dans le formulaire et effectue une véritable
connexion ; il signale donc exactement ce qu'une inspection rencontrerait — un nom de pilote
erroné, un mot de passe rejeté, un hôte injoignable. Rien n'est stocké : la connexion de test
est annulée qu'elle réussisse ou échoue.

Pour une connexion déjà existante, survolez sa ligne dans l'onglet **Database Connections** et
cliquez sur l'icône **prise** pour la retester. C'est le moyen le plus rapide de vérifier
qu'une source est joignable après une rotation de mot de passe ou une modification de pare-feu.

---

## Quelle base de données la connexion voit {: #which-database-the-connection-sees }

Lorsque vous ajoutez une source de données, *digna* propose les catalogues, schémas et tables
que la connexion peut atteindre. L'étendue dépend de la technologie :

| Technologie | Catalogues proposés |
|---|---|
| **PostgreSQL**, **MS SQL Server**, **Oracle**, **Snowflake** | Uniquement la base **courante** de la connexion |
| **Teradata**, **Netezza**, **Databricks** | Toutes les bases ou catalogues que l'utilisateur est autorisé à voir |
| **Hive**, **Impala** | Signalés par le pilote |

!!! important "Une connexion, une base de données"

    Pour PostgreSQL, SQL Server, Oracle et Snowflake, les propriétés doivent pointer vers la
    base qui contient les schémas sources — `DATABASE=…`, `Database=…`, ou le nom du service
    dans le `DBQ` d'Oracle. Les tables situées dans une autre base ne sont pas accessibles par
    cette connexion ; ajoutez-en une seconde pour cela.

---

## Mode de profilage et Work Schema {: #profiling-mode-and-work-schema }

Le mode de profilage détermine comment *digna* traite les données et calcule les métriques :

- **Standard :** les métriques sont calculées directement sur les tables sources, sans copier
  les données.
- **Permanent :** les données du jour inspecté sont copiées dans une table permanente, et les
  métriques sont calculées sur les données copiées.
- **Session :** les données sont copiées dans une table de session ou temporaire, et les
  métriques sont calculées sur ces données temporaires.

Le mode détermine ce que l'utilisateur de la connexion doit être autorisé à faire :

| Mode | Écrit | Droits nécessaires à l'utilisateur de la connexion |
|---|---|---|
| **Standard** | rien | Lecture sur les tables sources |
| **Permanent** | une table par source de données dans **Work Schema** | Créer et supprimer des tables dans **Work Schema** |
| **Session** | une table temporaire que la base supprime avec la session | Créer des tables temporaires — **Work Schema** n'est pas utilisé |

*Standard* se contente de lire, ce qui en fait le mode à choisir lorsque *digna* ne dispose que
d'un accès en lecture seule. **Work Schema** n'est lu que pour *Permanent*, mais il vaut la
peine de le renseigner malgré tout afin que la connexion continue de fonctionner si le mode est
modifié par la suite.

---

## Utiliser un DSN à la place {: #using-a-dsn-instead }

Un DSN fonctionne toujours — `DSN` n'est qu'une propriété parmi d'autres :

```
Key: DSN        Value: my_registered_dsn
Key: UID        Value: <user>
Key: PWD        Value: <password>        [Encrypted]
```

Le DSN doit être enregistré sur l'hôte *digna*, pour le compte utilisateur qui exécute le
backend *digna*, et en tant que **System DSN** lorsque *digna* s'exécute comme service. Tout ce
qui est configuré dans le DSN peut être remplacé en l'ajoutant également comme propriété.

Le mode sans DSN est la valeur par défaut documentée parce qu'il évite cet état côté hôte : la
connexion est entièrement décrite dans *digna*, et un nouvel hôte *digna* a besoin du pilote
installé, mais de rien de configuré.

---

## Dépannage {: #troubleshooting }

### Nom de source de données introuvable / aucun pilote par défaut spécifié

**Symptômes :**
- Le bouton **Test** signale une erreur mentionnant *data source name not found*, alors même que
  la configuration est sans DSN

**Causes et solutions :**
1. La valeur de `Driver` ne correspond à aucun nom de pilote enregistré — comparez-la avec
   l'onglet **Drivers** de l'*Administrateur de sources de données ODBC (64 bits)*, ou avec
   `odbcinst -q -d`
2. Le pilote est installé sur votre poste de travail mais pas sur l'hôte *digna*
3. Le pilote est en 32 bits alors que *digna* est en 64 bits — installez le pilote 64 bits
4. La propriété `Driver` est totalement absente, et aucun `DSN` n'a été fourni non plus
5. Sous Linux et macOS, le pilote est installé mais non enregistré — indiquez plutôt le chemin
   complet vers la bibliothèque du pilote, ou enregistrez-le dans `odbcinst.ini`

---

### Le test de connexion expire

**Symptômes :**
- **Test** se bloque puis échoue au bout d'environ une demi-minute

**Causes et solutions :**
1. L'hôte ou le port sont injoignables depuis l'hôte *digna* — vérifiez le pare-feu et, pour les
   sources cloud, la liste d'adresses IP autorisées
2. Le nom d'hôte est correct mais le port appartient à un autre service
3. La source a besoin de plus que les 30 secondes par défaut pour accepter une connexion —
   augmentez `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` dans la section `[base]` de `config.toml` (`0`
   attend indéfiniment) et redémarrez le backend
4. Un point de terminaison serverless sort de veille — réessayez, et si cela se produit
   régulièrement, augmentez le délai de connexion comme ci-dessus

---

### L'authentification échoue alors que les identifiants sont corrects

**Symptômes :**
- Le pilote signale des identifiants non valides, mais le même utilisateur fonctionne dans un
  autre client SQL

**Causes et solutions :**
1. Le mot de passe contient `;` — encadrez la valeur d'accolades : `{p@ss;word}`
2. Un espace en fin de chaîne a été copié dans la valeur
3. Le pilote attend un mécanisme d'authentification précis — par exemple `AuthMech` pour les
   pilotes Hive et Databricks, ou `authenticator` pour Snowflake
4. La valeur a été stockée chiffrée puis modifiée — les valeurs chiffrées ne peuvent pas être
   relues, ressaisissez donc le secret dans son intégralité
5. Un jeton a expiré — les jetons d'accès personnels et les jetons d'accès programmatique sont
   émis avec une date d'expiration

---

### L'écran des sources de données ne propose pas la base ou le schéma attendu

**Symptômes :**
- Des catalogues, schémas ou tables manquent lors de l'ajout d'une source de données

**Causes et solutions :**
1. La connexion pointe vers une autre base — voir
   [Quelle base de données la connexion voit](#which-database-the-connection-sees)
2. L'utilisateur de la connexion n'a pas les droits de lecture sur le schéma ou sur le
   dictionnaire de données
3. **Technology** ne correspond pas à la source, *digna* interroge donc le mauvais dictionnaire
   de données
4. Pour Snowflake, aucun entrepôt par défaut n'est affecté à l'utilisateur et aucune propriété
   `Warehouse` n'a été fournie, de sorte que les requêtes de métadonnées ne peuvent pas
   s'exécuter

---

### Le profilage échoue alors que le test de connexion réussit

**Symptômes :**
- **Test** réussit, mais une inspection échoue au moment de créer les tables de travail

**Causes et solutions :**
1. Le profilage *Permanent* est sélectionné et l'utilisateur de la connexion ne peut pas créer
   de tables dans **Work Schema** — accordez les droits, ou passez à *Session* ou *Standard*
2. **Work Schema** est vide ou nomme un schéma inexistant, alors que le profilage *Permanent*
   est sélectionné
3. Le profilage *Session* est sélectionné et l'utilisateur de la connexion n'a pas le droit de
   créer des tables temporaires
4. Une requête de profilage de longue durée atteint le délai d'expiration des requêtes —
   augmentez `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` dans la section `[base]` de `config.toml` (3600
   secondes par défaut, `0` désactive le délai)

---

## Bonnes pratiques

**À FAIRE :**

- Installer et enregistrer le pilote sur l'hôte *digna* avant de configurer la connexion
- Cocher **Encrypted** pour chaque mot de passe et chaque jeton
- Cliquer sur **Test** avant d'enregistrer, et retester après une rotation de mot de passe
- Nommer les connexions d'après la source et l'environnement, par exemple `sales_dwh_prod`
- Donner à *digna* un utilisateur de base dédié, en lecture seule lorsque le profilage
  *Standard* suffit
- Conserver une connexion par base source, et en ajouter une seconde plutôt que de modifier la
  première

**À NE PAS FAIRE :**

- Stocker des secrets en clair, ou partager un utilisateur de base entre *digna* et d'autres
  outils
- Utiliser un pilote 32 bits avec une installation *digna* 64 bits
- Compter sur un DSN utilisateur lorsque *digna* s'exécute comme service — il ne sera pas
  visible
- Placer une valeur contenant `;` dans une propriété sans accolades
- Faire pointer **Work Schema** vers un schéma qui contient des données sources

---

## Support

Besoin d'aide pour une connexion à une base de données ?

- **E-mail :** support@digna.ai
- **Documentation :** https://docs.digna.ai
- **Site web :** https://www.digna.ai

---

**Release:** 2026.06  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**