# Guide d'installation sur Windows pour digna Release 2026.06

**Release :** 2026.06

**Dernière mise à jour :** 30 août 2026


---

## Table des matières

1. [Introduction](#introduction)
2. [Exigences système](#system-requirements)
3. [Préparation avant installation](#pre-installation-setup)
4. [Configuration du serveur PostgreSQL](#postgresql-server-setup)
5. [Configuration du serveur Web](#web-server-configuration)
6. [Installation initiale](#initial-installation)
7. [Configuration du backend](#backend-configuration)
8. [Configuration du dashboard](#dashboard-configuration)
9. [Exécution de digna en tant que service Windows](#running-digna-as-a-windows-service)
10. [Mise à niveau vers une nouvelle version](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### À propos de digna

digna est une plateforme complète pilotée par l'IA conçue pour optimiser la gestion de la qualité des données dans divers environnements de données tels que les entrepôts, les data lakes et les lakehouses. Conçue pour être hautement extensible et adaptable, digna répond aux défis modernes des données via l'automatisation, la surveillance en temps réel et la détection d'anomalies.

digna est composée de deux composants principaux :

- **dignabackend** : Le moteur principal de l'application, responsable du traitement des données et de l'exécution des contrôles de qualité.
- **dignadashboard** : Une interface web hébergée sur un serveur web, offrant un moyen convivial d'interagir avec la plateforme digna et de visualiser les métriques de qualité des données.

### Nouveautés de la Release 2026.06

Cette version apporte des capacités d'observabilité des données directement dans votre code, permettant aux développeurs de surveiller la qualité des données à la source. Consultez les [release notes](http://docs.digna.ai/changelog/Release_202606/) pour les détails complets.

---

## Exigences système {: #system-requirements }

Avant de commencer l'installation, assurez-vous que votre système respecte les exigences minimales suivantes :

| Exigence | Spécification |
|---|---|
| **Système d'exploitation** | Windows Server ou Windows 10/11 |
| **Mémoire (Configuration minimale)** | 16 GB RAM |
| **Espace disque** | 10 GB d'espace disponible |
| **Base de données** | PostgreSQL Server 12 ou supérieur |
| **Serveur Web** | IIS, Apache Tomcat, ou équivalent |

### Options d'installation de la base de données

**Si PostgreSQL est déjà installé :**
Vous pouvez ajouter une nouvelle base de données pour digna sur votre serveur PostgreSQL existant.

**Si vous installez PostgreSQL sur la même machine que digna :**

!!! info "Spécifications recommandées"

    - **Mémoire** : 32 GB RAM (au lieu de 16 GB)
    - **Espace disque** : 50 GB d'espace disponible (au lieu de 10 GB)

    Ces spécifications supérieures permettent d'exécuter simultanément digna et la base de données PostgreSQL.

---

## Préparation avant installation {: #pre-installation-setup }

Avant d'installer digna, assurez-vous que deux prérequis clés sont en place :

1. **Serveur PostgreSQL** – pour stocker les métriques calculées et les données de performance
2. **Serveur Web** – pour héberger le Dashboard digna

Si ces composants ne sont pas encore configurés, suivez les sections ci-dessous pour les installer et les configurer.

---

## Configuration du serveur PostgreSQL {: #postgresql-server-setup }

### Si PostgreSQL est déjà installé

Si PostgreSQL est déjà installé et en fonctionnement sur votre machine locale ou si vous utilisez un serveur PostgreSQL distant géré, vous pouvez passer à la [section suivante](#web-server-configuration).

### Installation de PostgreSQL

Suivez ces étapes pour installer PostgreSQL sur Windows :

#### Étape 1 : Télécharger PostgreSQL

1. Rendez-vous sur la [page de téléchargement PostgreSQL](https://www.postgresql.org/download/)
2. Sélectionnez **Windows**
3. Téléchargez le dernier installateur

#### Étape 2 : Exécuter l'installateur

1. Double-cliquez sur le fichier d'installation téléchargé
2. Suivez les invites de l'assistant d'installation

#### Étape 3 : Choisir le répertoire d'installation

Sélectionnez le répertoire où PostgreSQL sera installé. L'emplacement par défaut est généralement approprié.

#### Étape 4 : Sélectionner les composants

Pour une configuration standard, conservez les options de composants par défaut.

#### Étape 5 : Définir le mot de passe du superutilisateur PostgreSQL

Saisissez et confirmez un mot de passe pour le superutilisateur PostgreSQL (`postgres`). **Sauvegardez ce mot de passe en lieu sûr** — vous en aurez besoin plus tard.

#### Étape 6 : Configurer le numéro de port

Le port PostgreSQL par défaut est `5432`. Vous pouvez utiliser le port par défaut ou spécifier un port différent si nécessaire.

!!! tip "Astuce"

    Si le port 5432 est déjà utilisé, choisissez un port alternatif et notez-le pour la configuration ultérieure.

#### Étape 7 : Choisir la locale

Sélectionnez la locale pour votre base de données. La valeur par défaut convient généralement à la plupart des installations.

#### Étape 8 : Terminer l'installation

Cliquez sur **Next** pour les étapes restantes, puis cliquez sur **Finish**.

#### Étape 9 : Vérifier l'installation

Ouvrez l'invite de commandes et vérifiez que PostgreSQL est installé :

```bash
psql --version
```

Vous devriez voir la version de PostgreSQL si l'installation a réussi.

---

## Configuration du serveur Web {: #web-server-configuration }

digna nécessite un serveur web pour héberger le dashboard. Choisissez l'une des options suivantes :

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Vous n'avez besoin d'installer et de configurer **qu'un seul** de ces serveurs.

### Configuration IIS {: #iis-setup }

#### Vue d'ensemble

Internet Information Services (IIS) est le serveur web de Microsoft pour héberger des sites web et des applications web.

#### Activer IIS

1. **Ouvrir le Panneau de configuration**
   - Appuyez sur `Win + R`
   - Tapez `control` puis appuyez sur Entrée

2. **Accéder aux fonctionnalités Windows**
   - Cliquez sur **Programs**
   - Sélectionnez **Turn Windows features on or off**

3. **Activer Internet Information Services**
   - Faites défiler et trouvez **Internet Information Services (IIS)**
   - Cochez la case pour l'activer
   - Cliquez sur le **+** pour développer et vérifiez que ces sous-composants sont sélectionnés :
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Cliquez sur OK** pour appliquer les modifications

5. **Vérifier l'installation d'IIS**
   - Ouvrez votre navigateur
   - Rendez-vous sur `http://localhost`
   - Vous devriez voir la page d'accueil IIS

#### Requis : Module URL Rewrite

IIS requiert le composant URL Rewrite. Téléchargez et installez-le depuis la [page officielle Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Requis : Type MIME pour les fichiers Markdown

Pour garantir que les fichiers Markdown (`.md`) soient correctement servis par IIS :

1. Ouvrez **IIS Manager** (appuyez sur `Win + R`, tapez `inetmgr`, appuyez sur Entrée)
2. Naviguez vers **Your Site > MIME Types**
3. Cliquez sur **Add...**
4. Configurez :
   - **File name extension** : `.md`
   - **MIME type** : `text/markdown`

!!! warning "Important"

    Sans ce paramètre, les fichiers `.md` peuvent ne pas être servis correctement.

---

### Configuration Apache Tomcat {: #apache-tomcat-setup }

#### Vue d'ensemble

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
   - Rendez-vous sur `http://localhost:8080`
   - Vous devriez voir la page d'accueil Apache Tomcat

!!! tip "Astuce"

    Apache Tomcat démarre généralement automatiquement après l'installation. S'il ne démarre pas, allez dans le dossier `bin` et exécutez `startup.bat`.

---

## Installation initiale {: #initial-installation }

### Étape 1 : Configurer le repository digna

Le repository digna stocke toutes les métriques calculées par digna. Il sert de base centrale pour les données analytiques et de performance.

#### Créer le schéma et l'utilisateur du repository

Ouvrez votre client PostgreSQL (pgAdmin, psql ou similaire) et exécutez les commandes SQL suivantes :

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Remplacez les espaces réservés suivants :**

- `<digna_repo_schema>` — Le nom de schéma souhaité (ex. `dignarepo`)
- `<digna_repo_user>` — Le nom d'utilisateur souhaité (ex. `digna_user`)
- `<digna_repo_password>` — Un mot de passe sécurisé pour cet utilisateur

**Exemple :**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Bonne pratique"

    Utilisez des mots de passe forts et complexes pour les utilisateurs de base de données. Évitez les identifiants facilement devinables.

---

### Étape 2 : Extraire le paquet d'installation digna

1. Localisez le fichier ZIP d'installation de digna qui vous a été fourni
2. Extrayez-le à l'emplacement d'installation souhaité
3. Après extraction, vous devriez voir les éléments suivants :
   - `dashboard/` — Interface web du dashboard
   - `digna` — Exécutable principal (backend + CLI combinés)
   - `config.toml` — Fichier de configuration
   - `license.toml` — Fichier de licence (copiez le vôtre ici)

### Étape 3 : Installer le fichier de licence

!!! warning "Important"

    Le fichier de licence **n'est pas** inclus dans le paquet d'installation et vous sera fourni séparément par digna.

1. Localisez le fichier `license.toml` qui vous a été fourni
2. Copiez-le dans le répertoire racine de l'installation digna (là où se trouvent `config.toml` et l'exécutable `digna`)

**Pourquoi c'est important :**
Le fichier de licence contient les informations client, la date d'expiration de la licence et la signature numérique. **Ne modifiez pas ce fichier** — toute modification l'invalidera.

**Structure du répertoire après configuration :**

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

Le fichier `config_template.toml` est fourni dans votre répertoire d'installation digna. Vous n'avez qu'à le renommer en `config.toml`.

**Emplacement :** `digna_installation/config.toml`

Ouvrez `config.toml` dans un éditeur de texte et configurez chaque section ci-dessous.

#### Section [app]

Cette section configure les paramètres de l'application backend digna :

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `digna_APP_HOST` | `localhost` ou adresse IP | Nom d'hôte ou IP où est hébergé dignabackend |
| `digna_APP_PORT` | `8082` (par défaut) | Port pour les endpoints REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL du frontend | Si le dashboard est sur un serveur différent, incluez son URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requis pour CORS avec des credentials |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Autorise toutes les méthodes HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Autorise tous les en-têtes |

#### Section [repo]

Cette section configure la connexion à la base de données PostgreSQL :

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `digna_REPO_HOST` | `localhost` ou IP | Nom d'hôte/IP du serveur PostgreSQL |
| `digna_REPO_PORT` | `5432` (par défaut) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nom de la base de données |
| `digna_REPO_SCHEMA` | `dignarepo` | Schéma créé précédemment |
| `digna_REPO_USER` | `digna_user` | Utilisateur créé lors de la configuration PostgreSQL |
| `digna_REPO_PASSWORD` | Votre mot de passe | Mot de passe défini lors de la création du schéma |

#### Section [base]

Cette section contient les paramètres de sécurité et des cookies :

```toml
[base]
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `digna_FERNET_KEY` | Clé de chiffrement | Utilisée pour chiffrer les tokens et les cookies (valeur par défaut fournie) |
| `digna_COOKIE_DOMAIN` | `localhost` | Doit correspondre au domaine de votre frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Utilisez `true` pour les connexions HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Toujours activé pour la sécurité |
| `digna_COOKIE_SAME_SITE` | `lax` | Prévoit la protection contre les attaques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 heures) | Durée de session en secondes |
| `digna_MAX_WORKERS` | Nombre de cœurs CPU - 1 | Nombre de tâches d'inspection parallèles |

#### Section [logging]

Cette section configure le comportement des journaux :

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Paramètre | Valeur | Remarques |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ou `DEBUG` | `INFO` pour la production, `DEBUG` pour le dépannage |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Nombre de sauvegardes journalières des logs à conserver |

---

### Étape 3 : Initialiser le repository

1. Ouvrez l'invite de commandes
2. Naviguez vers votre répertoire d'installation digna (là où se trouvent `config.toml` et l'exécutable `digna`)
3. Exécutez le test de connexion :

```bash
digna repo check
```

Vous devriez voir une confirmation que la connexion est établie (le repository lui-même n'est pas encore initialisé).

### Étape 4 : Installer le schéma du repository

Dans le même répertoire, exécutez :

```bash
digna repo install
```

Cette commande installe les tables et le schéma nécessaires dans votre base de données PostgreSQL.

### Étape 5 : Démarrer le serveur digna

Dans le répertoire d'installation digna, démarrez le serveur avec :

```bash
digna serve --address <host> --port <port>
```

**Paramètres :**
- `--address` — Nom d'hôte/IP du serveur
- `--port` — Port du serveur

Vous devriez voir des messages de démarrage confirmant que le serveur fonctionne :

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Étape 6 : Créer un utilisateur administrateur

1. Ouvrez une nouvelle fenêtre d'invite de commandes
2. Naviguez vers votre répertoire d'installation digna
3. Exécutez la commande suivante pour créer un utilisateur administrateur :

```bash
digna user add <username> "<full_name>" <password> --su
```

**Exemple :**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

Cela crée un utilisateur avec les privilèges administratifs complets.

!!! tip "Bonne pratique"

    Utilisez un mot de passe fort avec un mélange de majuscules, minuscules, chiffres et caractères spéciaux.

---

## Configuration du dashboard {: #dashboard-configuration }

### Étape 1 : Déployer le dashboard sur le serveur Web

Le dashboard digna dispose de son propre fichier `config.toml` situé dans le répertoire `dashboard/`. Cette configuration est fournie et ne nécessite pas de modifications lors de l'installation initiale. Vous ne devez la modifier que si vous avez besoin de personnaliser la connexion au backend.

Si vous devez modifier la configuration du dashboard (par exemple pour des déploiements multi-instance), référez-vous à la documentation du dashboard.

Choisissez votre serveur Web et suivez les étapes de déploiement correspondantes.

#### Déploiement sur IIS

1. **Ouvrez IIS Manager**
   - Appuyez sur `Win + R`, tapez `inetmgr`, appuyez sur Entrée

2. **Créer un nouveau site Web**
   - Dans le panneau de gauche, faites un clic droit sur **Sites**
   - Sélectionnez **Add Website...**

3. **Configurer le site**
   - **Site Name** : Entrez un nom (ex. "dignaDashboard")
   - **Physical Path** : Cliquez sur Browse et sélectionnez votre dossier `dashboard`
   - **Binding** : Définissez l'adresse IP et le port (port 80 par défaut pour HTTP, 443 pour HTTPS)

4. **Démarrer le site**
   - Cliquez sur **OK** pour créer le site
   - Faites un clic droit sur le nouveau site et sélectionnez **Start**

5. **Tester l'installation**
   - Ouvrez votre navigateur
   - Rendez-vous sur `http://localhost` (ou l'URL configurée)
   - Vous devriez voir la page de connexion du dashboard digna

#### Déploiement sur Apache Tomcat

1. **Copier le dashboard dans Tomcat**
   - Copiez le dossier `dashboard` dans le répertoire `webapps` de Tomcat
   - Renommez-le si nécessaire (ex. en `digna`)
   - Exemple : `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Vérifier le déploiement**
   - Actualisez ou rechargez la page de gestion Tomcat (http://localhost:8080)
   - Vous devriez voir "digna" (ou le nom choisi) listé parmi les applications déployées

3. **Accéder au dashboard**
   - Ouvrez votre navigateur
   - Rendez-vous sur `http://localhost:8080/digna`
   - Vous devriez voir la page de connexion du dashboard digna

---

## Exécution de digna en tant que service Windows {: #running-digna-as-a-windows-service }

### Pourquoi utiliser un service Windows ?

Exécuter le backend digna en tant que service Windows garantit qu'il :
- Démarre automatiquement au démarrage du serveur
- S'exécute en arrière-plan sans qu'une invite de commandes soit ouverte
- Redémarre automatiquement en cas de plantage
- Peut être géré via les Services Windows

### Fichiers de gestion du service

Tous les fichiers nécessaires se trouvent dans le répertoire d'installation digna sous : `bin/`

Les fichiers batch suivants sont disponibles :
- `install_service.bat` — Enregistre digna en tant que service Windows
- `uninstall_service.bat` — Désenregistre le service
- `start_service.bat` — Démarre le service
- `stop_service.bat` — Arrête le service

!!! warning "Administrateur requis"

    Tous les fichiers batch doivent être exécutés avec les privilèges Administrateur.

### Installation du service

1. **Ouvrez l'invite de commandes en tant qu'administrateur**
   - Clic droit sur Invite de commandes
   - Sélectionnez "Run as Administrator"

2. **Naviguez vers le dossier bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Exécutez le script d'installation**
   ```bash
   install_service.bat
   ```

Le serveur digna est maintenant enregistré comme service Windows avec le démarrage **automatique** activé. Le service ne démarre pas immédiatement — voir la section suivante pour le démarrer.

### Démarrer et arrêter le service

#### Pour démarrer le service

1. Ouvrez l'invite de commandes en tant qu'administrateur
2. Naviguez vers `digna\bin`
3. Exécutez :
   ```bash
   start_service.bat
   ```

#### Pour arrêter le service

1. Ouvrez l'invite de commandes en tant qu'administrateur
2. Naviguez vers `digna\bin`
3. Exécutez :
   ```bash
   stop_service.bat
   ```

!!! tip "Astuce"

    Arrêtez toujours le service avant de mettre à jour les fichiers de l'application.

### Déplacer le service vers un nouveau répertoire

Si vous devez déplacer l'installation digna :

1. **Désinstaller le service actuel**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Déplacer les fichiers de l'application**
   - Déplacez l'ensemble du dossier d'installation digna vers le nouvel emplacement

3. **Réinstaller le service**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Démarrer le service**
   ```bash
   start_service.bat
   ```

### Désinstaller le service

1. **Arrêter le service en cours d'exécution**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Désinstaller le service**
   ```bash
   uninstall_service.bat
   ```

Le serveur digna est maintenant désenregistré en tant que service Windows.

---

## Mise à niveau vers une nouvelle version {: #upgrading-to-a-new-release }

### Avant la mise à niveau

**La création d'une sauvegarde du repository digna est OBLIGATOIRE**

Avant de mettre à niveau digna, sauvegardez votre repository (PostgreSQL) pour vous protéger contre toute perte de données.
Une sauvegarde vous permet de restaurer l'état si la mise à niveau rencontre des problèmes inattendus.

### Processus de mise à niveau

#### Étape 1 : Arrêter le service digna

Si digna fonctionne en tant que service Windows, arrêtez-le d'abord :

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Étape 2 : Sauvegarder l'installation backend actuelle

Dans votre répertoire d'installation digna :

```bash
# Renommer le dossier contenant dignabackend
ren dignabackend dignabackend_old
```
```bash
# Renommer le dashboard
ren dashboard dashboard_old
```

#### Étape 3 : Extraire et déployer la nouvelle version

1. Extrayez le nouveau fichier ZIP d'installation digna
2. Copiez le nouvel exécutable `digna` et le dossier `dashboard` dans votre répertoire d'installation


!!! warning "Important"

    Le fichier `config.toml` n'est **jamais** inclus dans le ZIP d'installation. Votre configuration existante reste intacte.

### Étape 4 : Restaurer vos fichiers de configuration

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Étape 5 : Mettre à jour le schéma du repository

Rendez-vous dans votre répertoire d'installation digna et exécutez :

```bash
digna repo upgrade
```

Cela met à jour le schéma PostgreSQL vers la dernière version tout en préservant toutes les données existantes.

### Étape 6 : Redémarrer les services

Si vous utilisez un service Windows :

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Si vous exécutez manuellement, redémarrez le serveur :

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Si vous utilisez IIS ou Tomcat, redémarrez le serveur web concerné.

#### Étape 7 : Vérifier la mise à niveau

1. Accédez au dashboard digna
2. Vérifiez que l'interface se charge correctement
3. Consultez les logs du serveur pour détecter d'éventuelles erreurs