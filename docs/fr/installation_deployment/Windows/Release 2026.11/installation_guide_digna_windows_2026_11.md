---
title: Guide d'installation Windows – digna Release 2026.11 | digna Documentation
description: Guide pas à pas pour installer digna Release 2026.11 sur Windows — exigences système, configuration de PostgreSQL, configuration du serveur web, configuration du backend et du tableau de bord, exécution de digna en tant que service Windows et mise à niveau depuis la Release 2026.06.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Guide d'installation Windows pour digna Release 2026.11

**Release :** 2026.11

**Dernière mise à jour :** 7 novembre 2026


---

## Table des matières

1. [Introduction](#introduction)
2. [Exigences système](#system-requirements)
3. [Préparation avant l'installation](#pre-installation-setup)
4. [Configuration du serveur PostgreSQL](#postgresql-server-setup)
5. [Configuration du serveur Web](#web-server-configuration)
6. [Installation initiale](#initial-installation)
7. [Configuration du backend](#backend-configuration)
8. [Configuration du tableau de bord](#dashboard-configuration)
9. [Exécuter digna en tant que service Windows](#running-digna-as-a-windows-service)
10. [Mise à niveau vers une nouvelle version](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### À propos de digna

digna est une plateforme complète pilotée par l'IA conçue pour optimiser la gestion de la qualité des données dans divers environnements de données tels que les entrepôts, les data lakes et les lakehouses. Conçue pour être hautement évolutive et adaptable, digna répond aux défis modernes des données grâce à l'automatisation, la surveillance en temps réel et la détection d'anomalies.

digna se compose de deux composants principaux :

- **digna** : le cœur de l'application, chargé du traitement des données et de l'exécution des contrôles de qualité. Il réunit le backend et l'interface en ligne de commande dans un seul exécutable, remplaçant les programmes distincts `dignabackend` et `dignacli` des versions précédentes.
- **dignadashboard** : Une interface web hébergée sur un serveur web, offrant un moyen convivial d'interagir avec la plateforme digna et de visualiser les métriques de qualité des données.

### Nouveautés de la Release 2026.11

Cette version ajoute digna Data Reconciliation, digna Agentic avec le digna MCP Server, et le digna Engine, qui peut profiler les données au sein de digna et contrôler l'intégrité référentielle entre différentes technologies de bases de données. Consultez les [notes de version](../../../changelog/Release_202611.md) pour tous les détails.

Pour une installation, cette version apporte un nouveau mécanisme de migration du référentiel, une section `[duckdb]` facultative dans `config.toml` pour le digna Engine, et un nouveau fichier de licence. La [section sur la mise à niveau](#upgrading-to-a-new-release) traite chacun de ces points.

### Vous cherchez macOS ou Linux ?

Ce guide couvre Windows. Pour d'autres plateformes, consultez le [Guide d'installation macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) ou le [Guide d'installation Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Exigences système {: #system-requirements }

Avant de commencer l'installation, assurez-vous que votre système répond aux exigences minimales suivantes :

| Exigence | Spécification |
|---|---|
| **Système d'exploitation** | Windows Server ou Windows 10/11 |
| **Mémoire (Configuration minimale)** | 16 Go de RAM |
| **Espace disque** | 10 Go d'espace disponible |
| **Base de données** | PostgreSQL Server 12 ou supérieur |
| **Serveur Web** | IIS, Apache Tomcat, ou équivalent |

!!! info "digna Engine"

    Les connexions de base de données qui utilisent le digna Engine comme emplacement de profilage
    sont profilées sur l'hôte digna lui-même. Prévoyez pour elles de la mémoire et de l'espace
    disque supplémentaires, voir la [section \[duckdb\]](#duckdb-section).

### Options d'installation de la base de données

**Si PostgreSQL est déjà installé :**
Vous pouvez ajouter une nouvelle base de données pour digna à votre serveur PostgreSQL existant.

**Si vous installez PostgreSQL sur la même machine que digna :**

!!! info "Spécifications recommandées"

    - **Mémoire** : 32 Go de RAM (au lieu de 16 Go)
    - **Espace disque** : 50 Go d'espace disponible (au lieu de 10 Go)

    Ces spécifications supérieures permettent d'héberger à la fois digna et la base de données PostgreSQL simultanément.

---

## Préparation avant l'installation {: #pre-installation-setup }

Avant d'installer digna, assurez-vous que deux prérequis clés sont en place :

1. **Serveur PostgreSQL** – pour stocker les métriques calculées et les données de performance
2. **Serveur Web** – pour héberger le Dashboard digna

Si ces composants ne sont pas encore configurés, suivez les sections ci-dessous pour les installer et les configurer.

---

## Configuration du serveur PostgreSQL {: #postgresql-server-setup }

### Si PostgreSQL est déjà présent

Si PostgreSQL est déjà installé et en cours d'exécution sur votre machine locale ou si vous utilisez un serveur PostgreSQL distant géré, vous pouvez passer à la [section suivante](#web-server-configuration).

### Installation de PostgreSQL

Suivez ces étapes pour installer PostgreSQL sur Windows :

#### Étape 1 : Télécharger PostgreSQL

1. Visitez la [page de téléchargements PostgreSQL](https://www.postgresql.org/download/)
2. Sélectionnez **Windows**
3. Téléchargez le dernier installateur

#### Étape 2 : Exécuter l'installateur

1. Double-cliquez sur le fichier d'installation téléchargé
2. Suivez les invites de l'assistant d'installation

#### Étape 3 : Choisir le répertoire d'installation

Sélectionnez le répertoire où PostgreSQL sera installé. L'emplacement par défaut est généralement approprié.

#### Étape 4 : Sélectionner les composants

Pour une installation standard, conservez les options de composants par défaut.

#### Étape 5 : Définir le mot de passe du superutilisateur PostgreSQL

Saisissez et confirmez un mot de passe pour le superutilisateur PostgreSQL (`postgres`). **Conservez ce mot de passe en lieu sûr** — vous en aurez besoin plus tard.

#### Étape 6 : Configurer le numéro de port

Le port PostgreSQL par défaut est `5432`. Vous pouvez utiliser le port par défaut ou spécifier un port différent si nécessaire.

!!! tip "Astuce"

    Si le port 5432 est déjà utilisé, choisissez un port alternatif et notez-le pour la configuration ultérieure.

#### Étape 7 : Choisir la locale

Sélectionnez la locale pour votre base de données. Le paramètre par défaut convient généralement à la plupart des installations.

#### Étape 8 : Terminer l'installation

Cliquez sur **Suivant** pour les étapes restantes, puis cliquez sur **Terminer**.

#### Étape 9 : Vérifier l'installation

Ouvrez l'Invite de commandes et vérifiez que PostgreSQL est installé :

```bash
psql --version
```

Vous devriez voir la version de PostgreSQL si l'installation a réussi.

---

## Configuration du serveur Web {: #web-server-configuration }

digna nécessite un serveur web pour héberger le tableau de bord. Choisissez l'une des options suivantes :

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Vous n'avez besoin d'installer et de configurer **qu'un seul** de ces serveurs.

### Configuration IIS {: #iis-setup }

#### Présentation

Internet Information Services (IIS) est le serveur web de Microsoft pour héberger des sites web et des applications web.

#### Activation d'IIS

1. **Ouvrir le Panneau de configuration**
   - Appuyez sur `Win + R`
   - Tapez `control` et appuyez sur Entrée

2. **Accéder aux fonctionnalités Windows**
   - Cliquez sur **Programmes**
   - Sélectionnez **Activer ou désactiver des fonctionnalités Windows**

3. **Activer Internet Information Services**
   - Faites défiler et trouvez **Internet Information Services (IIS)**
   - Cochez la case pour l'activer
   - Cliquez sur le **+** pour développer et vérifiez que ces sous-composants sont sélectionnés :
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Cliquez sur OK** pour appliquer les modifications

5. **Vérifier l'installation d'IIS**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost`
   - Vous devriez voir la page de bienvenue IIS

#### Requis : Module URL Rewrite

IIS nécessite le composant URL Rewrite. Téléchargez et installez-le depuis la [page officielle Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Requis : Type MIME pour les fichiers Markdown

Pour que les fichiers Markdown (`.md`) soient servis correctement par IIS :

1. Ouvrez **IIS Manager** (appuyez sur `Win + R`, tapez `inetmgr`, appuyez sur Entrée)
2. Naviguez vers **Votre site > MIME Types**
3. Cliquez sur **Add...**
4. Configurez :
   - **File name extension** : `.md`
   - **MIME type** : `text/markdown`

!!! warning "Important"

    Sans ce paramétrage, les fichiers `.md` peuvent ne pas être servis correctement.

---

### Configuration Apache Tomcat {: #apache-tomcat-setup }

#### Présentation

Apache Tomcat est un conteneur de servlets Java open-source et un serveur web.

#### Installation

1. **Télécharger Apache Tomcat**
   - Visitez [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Téléchargez la distribution ZIP pour Windows

2. **Extraire l'archive**
   - Extrayez le fichier ZIP dans un répertoire sur votre système
   - Exemple : `C:\Program Files\Apache Tomcat`

3. **Vérifier que Tomcat fonctionne**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost:8080`
   - Vous devriez voir la page de bienvenue Apache Tomcat

!!! tip "Astuce"

    Apache Tomcat démarre généralement automatiquement après l'installation. S'il ne démarre pas, naviguez vers le dossier `bin` et exécutez `startup.bat`.

---

## Installation initiale {: #initial-installation }

### Étape 1 : Préparer le repository digna

Le repository digna stocke toutes les métriques calculées par digna. Il sert de base centrale pour les données analytiques et de performance.

#### Créer le schéma du repository et l'utilisateur

Ouvrez votre client PostgreSQL (pgAdmin, psql ou similaire) et exécutez les commandes SQL suivantes :

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Remplacez les espaces réservés suivants :**

- `<digna_repo_schema>` — Le nom de schéma souhaité (par ex., `dignarepo`)
- `<digna_repo_user>` — Le nom d'utilisateur souhaité (par ex., `digna_user`)
- `<digna_repo_password>` — Un mot de passe sécurisé pour cet utilisateur

**Exemple :**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Bonne pratique"

    Utilisez des mots de passe forts et complexes pour les utilisateurs de la base de données. Évitez les identifiants faciles à deviner.

---

### Étape 2 : Extraire le paquet d'installation digna

1. Localisez le fichier ZIP d'installation de digna qui vous a été fourni
2. Extrayez-le à l'emplacement d'installation souhaité
3. Après extraction, vous devriez voir les éléments suivants :
   - `dashboard/` — Interface web du tableau de bord
   - `digna` — Exécutable principal (backend + CLI combinés)

!!! info "Les fichiers de configuration et de licence ne font pas partie du paquet"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` ne sont livrés avec l'installation — vous créez les deux vous-même, dans [Configuration du backend](#backend-configuration) et [Configuration du tableau de bord](#dashboard-configuration). `license.toml` n'est pas livré non plus ; digna le fournit séparément, comme le décrit l'étape 3.

### Étape 3 : Installer le fichier de licence

!!! warning "Important"

    Le fichier de licence n'est **pas** inclus dans le paquet d'installation et vous sera fourni séparément par digna.

1. Localisez le fichier `license.toml` qui vous a été fourni
2. Copiez-le dans le répertoire racine d'installation de digna (là où se trouvent `config.toml` et l'exécutable `digna`)

**Pourquoi c'est important :**
Le fichier de licence contient vos informations client, la date d'expiration de la licence et la signature numérique. **Ne modifiez pas ce fichier** — toute modification l'invalidera.

**Structure du répertoire après la configuration :**

```
digna_installation/
├── config.toml         (fichier de configuration)
├── license.toml        (VOTRE FICHIER DE LICENCE - copiez-le ici)
├── digna               (exécutable principal)
└── dashboard/          (interface web)
    └── (fichiers du dashboard)
```

---

## Configuration du backend {: #backend-configuration }

### Étape 1 : Créer et éditer le fichier de configuration

Le fichier `config_template.toml` est fourni dans votre répertoire d'installation digna. Vous devez simplement le renommer en `config.toml`.

**Emplacement :** `digna_installation/config.toml`

Ouvrez `config.toml` dans un éditeur de texte et configurez chaque section ci-dessous.

#### Section [app]

Cette section configure le partage de ressources entre origines (CORS) entre le tableau de bord et le backend :

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | URL du tableau de bord | Les URL depuis lesquelles le tableau de bord est servi. Les requêtes du navigateur provenant de toute autre origine sont rejetées |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requis, pour que le navigateur envoie le cookie de session avec chaque requête |

!!! info "La section [app] est facultative"

    À partir de la Release 2026.11, les deux clés, et toute la section `[app]`, peuvent être
    omises. C'est la configuration adaptée lorsqu'un reverse proxy sert le tableau de bord et le
    backend sous une même origine : le navigateur n'effectue alors aucune requête cross-origin, et
    aucune n'est autorisée par défaut.

#### Section [repo]

Cette section configure la connexion à la base de données PostgreSQL :

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` ou IP | Nom d'hôte/IP du serveur PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (par défaut) | Port PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nom de la base de données |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schéma créé précédemment |
| `DIGNA_REPO_USER` | `digna_user` | Utilisateur créé lors de la configuration PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Votre mot de passe | Mot de passe défini lors de la création du schéma |
| `DIGNA_REPO_SSLMODE` | `prefer` (par défaut) | Facultatif. Mode SSL de PostgreSQL : `disable`, `allow`, `prefer`, `require`, `verify-ca` ou `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (par défaut) | Facultatif. Nombre de connexions que digna maintient ouvertes vers le référentiel |

#### Section [base]

Cette section contient les paramètres de sécurité, des cookies et des inspections :

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `DIGNA_FERNET_KEY` | Valeur indiquée ci-dessus | Clé du chiffrement utilisé par les versions précédentes. Elle doit être présente ; conservez la valeur indiquée |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Hôte sous lequel le tableau de bord est atteint. `""` ne définit aucun domaine, ce qui convient derrière un proxy qui sert le tableau de bord et le backend sous une même origine |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Doit valoir `true` dès que digna est servi en HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Met le cookie de session hors de portée des scripts |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 heures) | Durée de session en secondes |
| `DIGNA_MAX_WORKERS` | Nombre de coeurs CPU - 1 | Nombre d'inspections pouvant s'exécuter en même temps |
| `DIGNA_FRONTEND_BASEURL` | URL du tableau de bord | Obligatoire. Utilisée pour les liens des messages de notification ; ce doit donc être une URL que les destinataires peuvent ouvrir |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (par défaut) | Facultatif. Nombre de secondes pendant lesquelles une requête sur une base de données source peut s'exécuter avant d'être interrompue ; `0` désactive le délai |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (par défaut) | Facultatif. Nombre de secondes d'attente d'une connexion à une base de données source ; `0` attend indéfiniment |

#### Section [encryption]

Cette section contient la clé utilisée pour chiffrer les valeurs sensibles stockées dans le référentiel. Elle est **obligatoire** — `config check` signale la section `[encryption]` comme FAILED si la clé est absente.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Paramètre | Valeur | Notes |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Clé encodée en Base64 | Chiffre les valeurs sensibles stockées dans le référentiel digna |

!!! warning "Protéger config.toml"

    Cette clé est une valeur fixe, identique dans toutes les installations digna, et c'est elle qui déchiffre les valeurs sensibles de votre référentiel. Limitez l'accès à `config.toml` au compte qui exécute digna, gardez le fichier hors du gestionnaire de versions et des lecteurs partagés, et excluez-le de toute sauvegarde conservée de manière moins sûre que le référentiel lui-même.

#### Section [logging]

Cette section configure le comportement des logs :

```toml
[logging]
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` ou `DEBUG` | `INFO` pour la production, `DEBUG` pour le dépannage. `TRACE`, `WARN` et `ERROR` sont également acceptés |
| `DIGNA_LOGGING_DIR` | `logs` (par défaut) | Facultatif. Répertoire des fichiers journaux rotatifs, relatif au répertoire de travail |
| `DIGNA_LOGGING_MAX_FILES` | `30` (par défaut) | Facultatif. Nombre de fichiers journaux archivés à conserver |

!!! warning "Conserver le répertoire des journaux en mode service"

    Un service Windows n'a pas de console : les fichiers journaux sont donc la seule trace de ce
    que fait le service. Ne définissez pas `DIGNA_LOGGING_DIR` sur une chaîne vide, ce qui
    désactive les fichiers journaux.

#### Section [duckdb] (facultative) {: #duckdb-section }

Nouveauté de la Release 2026.11. Cette section définit les ressources du **digna Engine**, qui
profile les données au sein de digna pour les connexions de base de données dont l'emplacement de
profilage est **digna Engine**, et exécute les contrôles d'intégrité référentielle entre des
sources de données situées sur des connexions de base de données différentes. Voir
[Emplacement de profilage](../../../platform/profiling/profiling_location.md).

La section est facultative. Sans elle, les valeurs par défaut ci-dessous s'appliquent.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Paramètre | Valeur | Notes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (par défaut) | Mémoire, en MB, qu'une exécution du digna Engine peut utiliser. Jusqu'à `DIGNA_MAX_WORKERS` exécutions peuvent être actives en même temps |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Par défaut : le répertoire temporaire du compte qui exécute digna (`%TEMP%`) | Répertoire des fichiers temporaires lorsque les données ne tiennent pas en mémoire |

!!! tip "Dimensionner le digna Engine"

    Prévoyez jusqu'à `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de mémoire sur l'hôte
    digna, en plus de ce que digna utilise lui-même, ainsi que suffisamment d'espace disque libre
    dans le répertoire temporaire pour contenir le jour inspecté le plus volumineux des sources de
    données qui utilisent le digna Engine. Faites pointer `DIGNA_DUCKDB_TEMP_DIRECTORY` vers un
    disque disposant de cet espace, accessible en écriture au compte qui exécute digna :

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Cette section n'est nécessaire que si au moins une connexion de base de données utilise le
    digna Engine, ou si un contrôle d'intégrité référentielle compare des sources de données situées
    sur des connexions différentes.

---

### Étape 2 : Vérifier la configuration

Avant d'initialiser le référentiel, vérifiez que `config.toml` est complet et correctement formé. Depuis votre répertoire d'installation digna, exécutez :

```bash
digna config check
```

Chaque section est validée séparément, de sorte qu'une seule erreur ne masque pas l'état des autres :

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Corrigez tout ce qui est signalé comme FAILED et relancez la commande avant de continuer. Un WARNING sous **Unknown keys** liste les clés de `config.toml` que digna ne lit pas ; elles n'ont aucun effet, supprimez-les donc ou corrigez leur orthographe. La liste complète des options figure dans la [référence CLI](../../../cli/Command_Line_Interface_202611.md).

### Étape 3 : Initialiser le repository

1. Ouvrez l'Invite de commandes
2. Placez-vous dans le répertoire d'installation de digna (là où se trouvent `config.toml` et l'exécutable `digna`)
3. Exécutez le test de connexion :

```bash
digna repo check
```

Sur un nouveau schéma, la commande se connecte puis signale qu'aucun référentiel n'est encore installé :

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

À ce stade, c'est le résultat attendu : il confirme que digna atteint PostgreSQL et le schéma. Une erreur de connexion ou d'authentification indique au contraire un problème dans la section `[repo]` ou dans la configuration de PostgreSQL.

### Étape 4 : Installer le schéma du repository

Dans le même répertoire, exécutez :

```bash
digna repo upgrade
```

Cette commande installe les tables nécessaires dans le schéma du référentiel et se termine par :

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installe et met à niveau"

    À partir de la Release 2026.11, `repo upgrade` installe un nouveau référentiel et met à niveau
    un référentiel existant. `repo install` fonctionne toujours comme autre nom de la même commande.

### Étape 5 : Créer un utilisateur administrateur

1. Ouvrez une fenêtre Invite de commandes **nouvelle**
2. Placez-vous dans le répertoire d'installation de digna
3. Exécutez la commande suivante pour créer un utilisateur administrateur :

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Exemple :**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

Cela crée un utilisateur avec les privilèges administratifs complets.

!!! tip "Bonne pratique"

    Utilisez un mot de passe fort contenant un mélange de majuscules, minuscules, chiffres et caractères spéciaux.

---

### Étape 6 : Démarrer le serveur digna

Dans le répertoire d'installation de digna, démarrez le serveur avec :

```bash
digna serve --address <host> --port <port>
```

**Paramètres :**
- `--address` — Nom d'hôte/IP du serveur (par défaut `127.0.0.1`)
- `--port` — Port du serveur (par défaut `8000`)

Une fois le serveur démarré, il affiche l'adresse sur laquelle il écoute :

```text
Server running on http://127.0.0.1:8082
```

!!! note "Le serveur occupe le terminal"

    `serve` s'exécute au premier plan et continue de tourner jusqu'à ce que vous l'arrêtiez avec ++ctrl+c++. Laissez-le tourner pendant que vous terminez la configuration ; pour le démarrer automatiquement au démarrage, voir [Exécuter digna en tant que service Windows](#running-digna-as-a-windows-service).

## Configuration du tableau de bord {: #dashboard-configuration }

### Étape 1 : Déployer le dashboard sur le serveur web

Le dashboard digna lit sa propre configuration dans `dashboard/dashboard_config.toml`. Ce fichier n'est pas livré avec l'installation — vous le créez dans le répertoire `dashboard/`, à côté des fichiers du dashboard.

Son contenu est décrit sous [Authentification unique (SSO)](../../../sso/overview.md), là où le fichier est également nécessaire : il contient les options de connexion proposées par le dashboard et, pour les déploiements multi-instance, la connexion au backend.

Choisissez votre serveur web et suivez les étapes de déploiement correspondantes.

#### Déploiement sur IIS

1. **Ouvrir IIS Manager**
   - Appuyez sur `Win + R`, tapez `inetmgr`, appuyez sur Entrée

2. **Créer un nouveau site Web**
   - Dans le panneau de gauche, faites un clic droit sur **Sites**
   - Sélectionnez **Add Website...**

3. **Configurer le site Web**
   - **Site Name** : Entrez un nom (par ex., "dignaDashboard")
   - **Physical Path** : Cliquez sur Parcourir et sélectionnez votre dossier `dashboard`
   - **Binding** : Définissez l'adresse IP et le port (port 80 par défaut pour HTTP, 443 pour HTTPS)

4. **Démarrer le site**
   - Cliquez sur **OK** pour créer le site
   - Faites un clic droit sur le nouveau site et sélectionnez **Start**

5. **Tester l'installation**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost` (ou l'URL configurée)
   - Vous devriez voir la page de connexion du dashboard digna

#### Déploiement sur Apache Tomcat

1. **Copier le dashboard dans Tomcat**
   - Copiez le dossier `dashboard` dans le répertoire `webapps` de Tomcat
   - Renommez-le si nécessaire (par ex., en `digna`)
   - Exemple : `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Vérifier le déploiement**
   - Actualisez ou rechargez la page de gestion Tomcat (http://localhost:8080)
   - Vous devriez voir "digna" (ou le nom choisi) listé parmi les applications déployées

3. **Accéder au dashboard**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost:8080/digna`
   - Vous devriez voir la page de connexion du dashboard digna

---

## Exécuter digna en tant que service Windows {: #running-digna-as-a-windows-service }

### Pourquoi utiliser un service Windows ?

Exécuter le backend digna en tant que service Windows garantit qu'il :
- Démarre automatiquement au démarrage du serveur
- S'exécute en arrière-plan sans fenêtre Invite de commandes ouverte
- Redémarre automatiquement en cas de crash
- Peut être géré via les Services Windows

### Les commandes `windows`

Le service est géré par l'exécutable `digna` lui-même, au moyen des sous-commandes `digna windows`. Il n'y a aucun fichier batch à exécuter.

| Commande | Rôle |
|---|---|
| `digna windows install` | Enregistre digna en tant que service Windows |
| `digna windows start` | Démarre le service enregistré |
| `digna windows stop` | Arrête le service en cours d'exécution |
| `digna windows uninstall` | Désenregistre le service |

!!! warning "Administrateur requis"

    Les quatre commandes doivent être exécutées depuis une Invite de commandes ouverte en tant qu'administrateur.

Chaque commande accepte `--name` pour cibler un service enregistré sous un nom autre que celui par défaut. La liste complète des options figure dans la [référence CLI](../../../cli/Command_Line_Interface_202611.md).

### Installation du service

1. **Ouvrir l'Invite de commandes en tant qu'administrateur**
   - Clic droit sur Invite de commandes
   - Sélectionnez "Exécuter en tant qu'administrateur"

2. **Se placer dans votre répertoire d'installation digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Enregistrer le service**
   ```bash
   digna windows install
   ```

!!! important "Indiquez l'adresse et le port, sauf si les valeurs par défaut vous conviennent"

    `install` inscrit l'adresse et le port dans l'enregistrement du service, et le service se lie exactement à ce qui a été inscrit. Les valeurs par défaut sont `127.0.0.1` et `8000`, qui n'acceptent que les connexions provenant de la machine elle-même. Un dashboard situé sur un autre hôte ne peut pas l'atteindre ; indiquez donc l'adresse sur laquelle le backend doit écouter :

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Ces valeurs ne sont pas lues depuis `config.toml`. Pour les modifier ultérieurement, désinstallez le service puis réinstallez-le avec les nouvelles valeurs.

Le service est enregistré avec démarrage **automatique** ; il démarrera donc avec Windows. Il ne démarre pas immédiatement — voir la section suivante.

#### Options d'installation

| Option | Valeur par défaut | Rôle |
|---|---|---|
| `--name` | `digna` | Nom sous lequel enregistrer le service |
| `--display-name` | `digna` | Nom affiché dans services.msc |
| `--description` | `digna data quality backend` | Description affichée dans services.msc |
| `--address` | `127.0.0.1` | Adresse sur laquelle le service lie son API |
| `--port` | `8000` | Port sur lequel le service lie son API |
| `--working-dir` | le répertoire de l'exécutable `digna` | Répertoire contenant `config.toml` et `license.toml`, dont le service fait son répertoire de travail |
| `--start-type` | `auto` | `auto` démarre avec Windows, `manual` démarre uniquement sur demande, `disabled` enregistre le service mais refuse de le démarrer |
| `--account` | `LocalSystem` | Compte sous lequel exécuter le service, par exemple `DOMAIN\user` ou `.\user` |
| `--password` | | Mot de passe du compte indiqué par `--account` |

!!! tip "Exécution sous un compte de domaine"

    `LocalSystem` n'a pas d'identité réseau : l'authentification Windows auprès de SQL Server et tout accès à un partage réseau échoueront donc. Installez le service avec `--account` et `--password` lorsqu'il doit accéder à des ressources en tant qu'utilisateur spécifique.

### Démarrer et arrêter le service

#### Pour démarrer le service

```bash
digna windows start
```

#### Pour arrêter le service

```bash
digna windows stop
```

!!! tip "Astuce"

    Arrêtez toujours le service avant de mettre à jour les fichiers de l'application.

### Déplacer le service vers un nouveau répertoire

Si vous devez déplacer l'installation digna :

1. **Arrêter et désenregistrer le service actuel**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Déplacer les fichiers de l'application**
   - Déplacez l'ensemble du dossier d'installation digna vers le nouvel emplacement

3. **Enregistrer à nouveau le service depuis le nouvel emplacement**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Reprenez les valeurs `--address`, `--port` ou `--account` que vous aviez utilisées la première fois — l'enregistrement précédent n'existe plus.

4. **Démarrer le service**
   ```bash
   digna windows start
   ```

### Désinstaller le service

1. **Arrêter le service en cours d'exécution**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Désenregistrer le service**
   ```bash
   digna windows uninstall
   ```

Le serveur digna est maintenant désenregistré en tant que service Windows.

---

## Mise à niveau vers une nouvelle version {: #upgrading-to-a-new-release }

Cette section met à niveau une installation de la Release 2026.06 vers la Release 2026.11.

!!! warning "Mise à niveau depuis une release antérieure à 2026.06"

    Effectuez d'abord les étapes de mise à niveau de la Release 2026.06 : [Mise à niveau vers une nouvelle version](../Release%202026.06/installation_guide_digna_windows_2026_06.md#upgrading-to-a-new-release). Poursuivez ensuite avec les étapes ci-dessous.

### Avant de mettre à niveau

**La création d'une sauvegarde du référentiel digna est obligatoire**

Avant de mettre à niveau digna, sauvegardez votre référentiel (PostgreSQL) pour vous protéger contre la perte de données.
Une sauvegarde vous permet de restaurer en cas de problème inattendu pendant la mise à niveau.

**Demander le fichier de licence de la Release 2026.11**

La Release 2026.11 nécessite un nouveau `license.toml`. Demandez-le à l'équipe digna avant de
commencer, et gardez-le à portée de main pour l'[étape 7](#step-7-replace-the-license-file).

### Processus de mise à niveau

#### Étape 1 : Arrêter le service digna {: #step-1-stop-the-digna-service }

Ouvrez une Invite de commandes en tant qu'administrateur et arrêtez le service avec l'exécutable
`digna` de votre installation actuelle :

```bash
cd C:\path\to\digna
digna windows stop
```

Le service reste enregistré. Le nouvel exécutable prend la place de l'ancien dans le même
répertoire, de sorte que l'enregistrement continue de pointer vers le bon fichier.

Si digna s'exécute au premier plan, appuyez sur ++ctrl+c++ dans sa fenêtre Invite de commandes.

#### Étape 2 : Sauvegarder l'installation actuelle {: #step-2-backup-current-installation }

Dans votre répertoire d'installation digna, renommez l'exécutable et le dossier du tableau de bord
de votre installation actuelle, afin que la nouvelle version puisse être déployée à côté :

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Conservez `digna_old.exe` jusqu'à ce que vous ayez vérifié la mise à niveau, et `dashboard_old` jusqu'à
ce que vous en ayez restauré vos fichiers de configuration (voir l'étape 4). Vous pourrez ensuite
supprimer les deux.

#### Étape 3 : Extraire et déployer la nouvelle version {: #step-3-extract-and-deploy-new-version }

1. Extrayez le nouveau fichier ZIP d'installation digna
2. Copiez le nouvel exécutable `digna` et le dossier `dashboard` vers votre répertoire d'installation

!!! warning "Important"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` ne sont jamais inclus dans le ZIP
    d'installation — l'équipe digna ne livre jamais aucun de ces deux fichiers. Votre configuration
    existante n'est donc pas touchée par la mise à niveau, et les copies se trouvant dans les
    dossiers renommés `*_old` sont les seules dont vous disposez.

#### Étape 4 : Restaurer vos fichiers de configuration {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

La Release 2026.11 ne nécessite aucune modification de `config.toml` : un fichier qui fonctionne
avec la Release 2026.06 continue de fonctionner. Deux modifications sont facultatives :

- Ajoutez une [section `[duckdb]`](#duckdb-section) si des connexions de base de données doivent
  utiliser le digna Engine et que ses valeurs par défaut ne conviennent pas à votre hôte.
- Omettez la section `[app]` si un reverse proxy sert le tableau de bord et le backend sous une
  même origine.

!!! warning "Paramètres que digna ne lit pas"

    Des versions antérieures de ce guide présentaient certains paramètres que digna ne lit pas. Ils
    n'ont aucun effet, et `config check` les liste sous **Unknown keys** à l'étape 6. Supprimez-les
    ou corrigez-les :

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` et
      `digna_LOGGING_BACKUP_COUNT` n'existent pas. Supprimez-les.
    - Les noms des paramètres sont sensibles à la casse. digna lit `DIGNA_REPO_HOST`, et non
      `digna_REPO_HOST`. Écrivez chaque nom en majuscules, comme dans
      [Configuration du backend](#backend-configuration).

!!! warning "Authentification unique : conservez [[oidc_clients]]"

    digna lit les fournisseurs d'authentification unique sous forme de liste d'entrées
    `[[oidc_clients]]`, chacune avec son propre `DIGNA_OIDC_KEY`. Si vous avez converti vos
    fournisseurs en sections `[oidc_clients.<key>]`, comme le montrait une version antérieure de
    ce guide, rétablissez-les. `config check` signale `OIDC config(s)` comme FAILED tant que cette
    forme est en place :

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Répétez l'entrée pour chaque fournisseur, et gardez chaque `DIGNA_OIDC_KEY` identique au `key`
    défini dans `dashboard_config.toml`. Seules les installations qui utilisent l'authentification
    unique sont concernées.

#### Étape 5 : Recharger le serveur Web {: #step-5-reload-the-web-server }

Le tableau de bord est un ensemble de fichiers statiques ; votre serveur Web — ainsi que le
navigateur — peut donc encore servir la version précédente. Rechargez ou redémarrez le serveur Web
qui héberge le dossier `dashboard`, puis rechargez la page en forçant l'actualisation
(++ctrl+f5++).

#### Étape 6 : Vérifier la configuration {: #step-6-validate-the-configuration }

Assurez-vous que `config.toml` est complet avant de toucher au référentiel :

```bash
digna config check
```

Chaque section doit être signalée OK. Corrigez tout ce qui est signalé comme FAILED, supprimez les
clés listées sous **Unknown keys**, et relancez la commande avant de continuer.

#### Étape 7 : Remplacer le fichier de licence {: #step-7-replace-the-license-file }

Un fichier de licence est normalement repris d'une release à la suivante. La Release 2026.11 fait
exception : elle ajoute deux modules sous licence, digna Data Reconciliation et digna Agentic, et
une licence émise avant la 2026.11 ne les contient pas. Copiez le `license.toml` fourni par
l'équipe digna pour la Release 2026.11 dans le répertoire d'installation, en remplaçant l'ancien :

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Ne conservez pas la licence précédente"

    Avec la licence précédente, digna démarre toujours, mais digna Data Reconciliation et le digna
    MCP Server restent désactivés. Chaque commande qui vérifie la licence — `user`, `inspection`,
    `repo` — s'interrompt avant de toucher au référentiel lorsque la vérification échoue. Vérifiez
    la nouvelle licence avant d'aller plus loin :

    ```bash
    digna license check
    ```

#### Étape 8 : Mettre à niveau le schéma du référentiel {: #step-8-upgrade-the-repository-schema }

Dans votre répertoire d'installation digna, exécutez :

```bash
digna repo upgrade
```

La Release 2026.11 gère le schéma du référentiel au moyen de migrations versionnées. La première
mise à niveau depuis une release antérieure amène le schéma à la dernière version de l'ancien
mécanisme, enregistre cet état comme point de départ, puis applique les migrations de la Release
2026.11. Elle se termine par :

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Toutes les données existantes sont préservées. Pour connaître l'état du référentiel à tout moment,
exécutez `digna repo check` : la commande liste la dernière migration appliquée et celles qui sont
encore en attente.

!!! warning "digna ne démarre pas sur un référentiel obsolète"

    À partir de la Release 2026.11, le serveur refuse de démarrer tant que le référentiel nécessite
    une mise à niveau, et l'indique, par exemple :

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Exécutez `repo upgrade` avant de démarrer le serveur ou le service.

#### Étape 9 : Redémarrer les services {: #step-9-restart-services }

Si digna s'exécute en tant que service Windows, redémarrez-le :

```bash
cd C:\path\to\digna
digna windows start
```

Si vous l'exécutez manuellement, redémarrez le serveur :

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Si vous utilisez IIS ou Tomcat, redémarrez le serveur web correspondant.

#### Étape 10 : Vérifier la mise à niveau {: #step-10-verify-the-upgrade }

1. Vérifiez la release du nouvel exécutable :

    ```bash
    digna version
    ```

    La première ligne doit indiquer `Release: 2026.11`.

2. Accédez au tableau de bord digna et vérifiez que l'interface se charge correctement.
3. Consultez les fichiers du répertoire `logs` de l'installation pour détecter des erreurs.
4. Testez vos connexions de base de données — voir
   [Tester une connexion](../../../databases/overview.md#testing-a-connection). Après une mise à
   niveau depuis une release antérieure à 2026.06, convertissez d'abord à ODBC chaque connexion
   qui ne l'utilisait pas encore.

Pour commencer avec les nouveaux modules, voir [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Connecter un agent IA](../../../platform/agentic/connect_ai_agent.md) pour le digna MCP Server, et
[Emplacement de profilage](../../../platform/profiling/profiling_location.md) pour le digna Engine.
