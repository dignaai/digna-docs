# Guide d'installation macOS pour digna Release 2026.11

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
9. [Exécution de digna en tant que service d'arrière-plan](#running-digna-as-a-background-service)
10. [Mise à niveau vers une nouvelle version](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### À propos de digna

digna est une plateforme complète pilotée par l'IA conçue pour optimiser la gestion de la qualité des données dans divers environnements tels que les entrepôts, les data lakes et les lakehouses. Conçue pour être hautement évolutive et adaptable, digna répond aux défis modernes des données grâce à l'automatisation, à la surveillance en temps réel et à la détection d'anomalies.

digna se compose de deux composants principaux :

- **digna** : le cœur de l'application, chargé du traitement des données et de l'exécution des contrôles de qualité. Il réunit le backend et l'interface en ligne de commande dans un seul exécutable, remplaçant les programmes distincts `dignabackend` et `dignacli` des versions précédentes.
- **dignadashboard** : Une interface web hébergée sur un serveur web, fournissant un moyen convivial d'interagir avec la plateforme digna et de visualiser les indicateurs de qualité des données.

### Nouveautés de la Release 2026.11

Cette version ajoute digna Data Reconciliation, digna Agentic avec le digna MCP Server, et le digna Engine, qui peut profiler les données au sein de digna et contrôler l'intégrité référentielle entre différentes technologies de bases de données. Consultez les [notes de version](../../../changelog/Release_202611.md) pour tous les détails.

Pour une installation, cette version apporte un nouveau mécanisme de migration du référentiel, une section `[duckdb]` facultative dans `config.toml` pour le digna Engine, et un nouveau fichier de licence. La [section sur la mise à niveau](#upgrading-to-a-new-release) traite chacun de ces points.

### Besoin d'un guide pour Windows ou Linux ?

Ce guide couvre macOS. Pour d'autres plateformes, consultez le [Windows Installation Guide](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) ou le [Linux Installation Guide](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

---

## Exigences système {: #system-requirements }

Avant de commencer l'installation, assurez-vous que votre système répond aux exigences minimales suivantes :

| Exigence | Spécification |
|---|---|
| **Système d'exploitation** | macOS 13 (Ventura) ou ultérieur |
| **Architecture** | Apple Silicon (arm64) ou Intel (x86_64) |
| **Mémoire (Configuration minimale)** | 16 Go RAM |
| **Espace disque** | 10 Go d'espace disponible |
| **Base de données** | Serveur PostgreSQL 12 ou supérieur |
| **Serveur Web** | nginx, Apache httpd, ou équivalent |

!!! info "digna Engine"

    Les connexions de base de données qui utilisent le digna Engine comme emplacement de profilage
    sont profilées sur l'hôte digna lui-même. Prévoyez pour elles de la mémoire et de l'espace
    disque supplémentaires, voir la [section \[duckdb\]](#duckdb-section).
| **Outils en ligne de commande** | Xcode Command Line Tools (requis par Homebrew) |

### Options d'installation de la base de données

**Si PostgreSQL est déjà installé :**
Vous pouvez ajouter une nouvelle base de données pour digna à votre serveur PostgreSQL existant.

**Si vous installez PostgreSQL sur la même machine que digna :**

!!! info "Spécifications recommandées"

    - **Mémoire** : 32 Go RAM (au lieu de 16 Go)
    - **Espace disque** : 50 Go d'espace disponible (au lieu de 10 Go)

    Ces spécifications plus élevées accommodent à la fois digna et le serveur PostgreSQL s'exécutant simultanément.

### Vérifier votre architecture

Plusieurs chemins dans ce guide diffèrent entre les Mac Apple Silicon et Intel. Pour vérifier votre architecture, ouvrez **Terminal** et exécutez :

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew s'installe dans `/opt/homebrew`.
- `x86_64` — Intel. Homebrew s'installe dans `/usr/local`.

!!! tip "Astuce"

    Plutôt que d'écrire en dur l'un ou l'autre chemin, ce guide utilise `$(brew --prefix)`, qui s'évalue vers l'emplacement correct sur les deux architectures. Vous pouvez copier les commandes telles quelles.

---

## Préparation avant l'installation {: #pre-installation-setup }

Avant d'installer digna, assurez-vous que trois prérequis essentiels sont en place :

1. **Homebrew** – le gestionnaire de paquets utilisé pour installer les composants ci-dessous
2. **Serveur PostgreSQL** – pour stocker les métriques calculées et les données de performance
3. **Serveur Web** – pour héberger le Dashboard digna

Si ces composants ne sont pas encore configurés, suivez les sections ci-dessous pour les installer et les configurer.

### Installation de Homebrew

Homebrew est le gestionnaire de paquets standard pour macOS et est utilisé tout au long de ce guide pour installer PostgreSQL et nginx.

#### Étape 1 : Vérifier si Homebrew est déjà installé

Ouvrez **Terminal** (appuyez sur `Cmd + Space`, tapez `Terminal`, appuyez sur Entrée) et exécutez :

```bash
brew --version
```

Si un numéro de version est renvoyé, passez à la section [Configuration du serveur PostgreSQL](#postgresql-server-setup).

#### Étape 2 : Installer Homebrew

Si la commande n'a pas été trouvée, installez Homebrew en suivant les instructions sur le [site officiel de Homebrew](https://brew.sh). L'installateur installe également les Xcode Command Line Tools s'ils ne sont pas déjà présents.

#### Étape 3 : Ajouter Homebrew à votre PATH

Sur Apple Silicon, l'installateur affiche deux commandes pour ajouter Homebrew à votre environnement shell. Exécutez-les comme indiqué, puis vérifiez :

```bash
brew --prefix
```

Cela doit afficher `/opt/homebrew` sur Apple Silicon ou `/usr/local` sur Intel.

---

## Configuration du serveur PostgreSQL {: #postgresql-server-setup }

### Si vous avez déjà PostgreSQL

Si PostgreSQL est déjà installé et en cours d'exécution sur votre machine locale ou si vous utilisez un serveur PostgreSQL distant géré, vous pouvez passer à la [section suivante](#web-server-configuration).

### Options d'installation

macOS propose deux façons simples d'installer PostgreSQL. Choisissez **une seule** :

- [Homebrew](#postgresql-homebrew) — installation en ligne de commande, recommandée pour les déploiements serveur
- [Postgres.app](#postgresql-app) — installation graphique, pratique pour l'évaluation locale

### Installation de PostgreSQL avec Homebrew {: #postgresql-homebrew }

#### Étape 1 : Installer la formule PostgreSQL

```bash
brew install postgresql@16
```

#### Étape 2 : Ajouter PostgreSQL à votre PATH

Les formules PostgreSQL versionnées sont *keg-only*, ce qui signifie que Homebrew n'ajoute pas automatiquement leurs commandes à votre PATH. Ajoutez-les vous-même :

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Remarque"

    Ceci suppose l'utilisation du shell `zsh` par défaut sur macOS. Si vous utilisez `bash`, ajoutez la même ligne à `~/.bash_profile` à la place.

#### Étape 3 : Démarrer le service PostgreSQL

```bash
brew services start postgresql@16
```

Ceci démarre PostgreSQL immédiatement et le configure pour redémarrer automatiquement à chaque connexion.

#### Étape 4 : Vérifier l'installation

```bash
psql --version
```

Vous devriez voir la version de PostgreSQL si l'installation a réussi.

#### Étape 5 : Se connecter au serveur

```bash
psql postgres
```

!!! warning "Important — macOS diffère de Windows ici"

    L'installateur Windows vous invite à créer un superutilisateur `postgres` et un mot de passe. Homebrew ne le fait pas. À la place, il crée un superutilisateur nommé d'après votre **compte macOS**, sans mot de passe, accessible uniquement depuis la machine locale.

    Cela signifie qu'il n'existe pas de rôle `postgres` sur une installation Homebrew fraîche. Utilisez votre propre nom de compte lorsque vous avez besoin d'un superutilisateur, et créez un utilisateur digna explicite comme décrit dans [Installation initiale](#initial-installation).

#### Étape 6 : Confirmer le port

Le port PostgreSQL par défaut est `5432`. Pour confirmer le port sur lequel votre serveur écoute :

```bash
psql postgres -c "SHOW port;"
```

Notez la valeur — vous en aurez besoin lors de la configuration du backend digna.

### Installation de PostgreSQL avec Postgres.app {: #postgresql-app }

Si vous préférez une installation graphique :

1. Téléchargez [Postgres.app](https://postgresapp.com) et glissez-le dans votre dossier **Applications**
2. Ouvrez l'application et cliquez sur **Initialize** pour créer un nouveau serveur
3. Suivez les instructions de l'application pour ajouter ses outils en ligne de commande à votre PATH
4. Vérifiez l'installation :

```bash
psql --version
```

Postgres.app crée également un superutilisateur nommé d'après votre compte macOS.

---

## Configuration du serveur Web {: #web-server-configuration }

digna nécessite un serveur Web pour héberger le tableau de bord. Choisissez l'une des options suivantes :

- [nginx](#nginx-setup) — installé via Homebrew, recommandé
- [Apache httpd](#apache-setup) — inclus avec macOS

Vous n'avez besoin d'installer et de configurer **qu'un seul** de ces serveurs.

Les deux sections configurent deux éléments dont dépend le tableau de bord :

- **Un fallback pour les applications monopage**, afin qu'actualiser une URL du tableau de bord n'entraîne pas un 404
- **Un type MIME pour les fichiers `.md`**, afin que les fichiers Markdown soient servis correctement

### Configuration nginx {: #nginx-setup }

#### Vue d'ensemble

nginx est un serveur Web léger et performant bien adapté pour servir le tableau de bord statique digna.

#### Installation

```bash
brew install nginx
```

#### Démarrer nginx

```bash
brew services start nginx
```

#### Vérifier l'installation

1. Ouvrez votre navigateur
2. Accédez à `http://localhost:8080`
3. Vous devriez voir la page d'accueil nginx

!!! note "Remarque — le port par défaut est 8080, pas 80"

    Homebrew configure nginx pour écouter sur le port `8080` afin qu'il puisse s'exécuter sans privilèges administrateur. Sur macOS, lier le port `80` ou tout port inférieur à 1024 requiert les droits root.

    Pour servir le tableau de bord sur le port 80, changez `listen 8080;` en `listen 80;` dans la configuration ci-dessous et démarrez nginx avec `sudo brew services start nginx` à la place.

#### Configurer un site pour le tableau de bord

La configuration nginx de Homebrew inclut tous les fichiers de son répertoire `servers`. Créez un fichier de configuration dédié pour digna là-bas :

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Collez ce qui suit en remplaçant `/path/to/digna/dashboard` par le chemin réel vers votre dossier `dashboard` extrait :

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Important"

    Sans la directive `try_files`, recharger une page du tableau de bord autre que l'URL racine renverra un 404. C'est l'équivalent nginx du module URL Rewrite requis par IIS sur Windows.

#### Appliquer la configuration

Testez la configuration pour les erreurs de syntaxe, puis rechargez nginx :

```bash
nginx -t
brew services restart nginx
```

---

### Configuration Apache httpd {: #apache-setup }

#### Vue d'ensemble

macOS inclut Apache httpd, aucune installation n'est donc requise. Il est désactivé par défaut.

#### Démarrer Apache

```bash
sudo apachectl start
```

#### Vérifier l'installation

1. Ouvrez votre navigateur
2. Accédez à `http://localhost`
3. Vous devriez voir le message "It works!"

#### Requis : Activer mod_rewrite

Le tableau de bord requiert la réécriture d'URL. Ouvrez la configuration d'Apache :

```bash
sudo nano /etc/apache2/httpd.conf
```

Trouvez la ligne suivante et supprimez le `#` initial pour la décommenter :

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Requis : Autoriser les overrides .htaccess

Dans le même fichier, localisez le bloc `<Directory "/Library/WebServer/Documents">` et changez :

```apache
AllowOverride None
```

en :

```apache
AllowOverride All
```

#### Requis : Type MIME pour les fichiers Markdown

Toujours dans `httpd.conf`, ajoutez la ligne suivante afin que les fichiers Markdown soient servis correctement :

```apache
AddType text/markdown .md
```

!!! warning "Important"

    Sans cette configuration, les fichiers `.md` peuvent ne pas être servis correctement.

#### Appliquer la configuration

Vérifiez la configuration pour les erreurs de syntaxe, puis redémarrez Apache :

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Installation initiale {: #initial-installation }

### Étape 1 : Configurer le dépôt digna

Le dépôt digna stocke toutes les métriques calculées par digna. Il sert de base de données centrale pour les données analytiques et de performance.

#### Créer le schéma du dépôt et l'utilisateur

Ouvrez votre client PostgreSQL (psql, pgAdmin ou équivalent) et exécutez les commandes SQL suivantes :

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Remplacez les paramètres suivants :**

- `<digna_repo_schema>` — Le nom de schéma souhaité (par ex., `dignarepo`)
- `<digna_repo_user>` — Le nom d'utilisateur souhaité (par ex., `digna_user`)
- `<digna_repo_password>` — Un mot de passe sécurisé pour cet utilisateur

**Exemple :**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Pour exécuter ces commandes depuis le Terminal en une seule étape :

```bash
psql postgres
```

Puis collez les instructions à l'invite `postgres=#` et tapez `\q` pour sortir.

!!! tip "Bonne pratique"

    Utilisez des mots de passe forts et complexes pour les utilisateurs de base de données. Évitez des identifiants facilement devinables.

---

### Étape 2 : Extraire le paquet d'installation digna

1. Localisez le fichier ZIP d'installation digna qui vous a été fourni
2. Extrayez-le à l'emplacement d'installation souhaité — par exemple `/opt/digna` ou `~/digna`
3. Après extraction, vous devriez voir les éléments suivants :
   - `dashboard/` — Interface Web du tableau de bord
   - `digna` — Exécutable principal (backend + CLI combinés)

!!! info "Les fichiers de configuration et de licence ne font pas partie du paquet"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` ne sont livrés avec l'installation — vous créez les deux vous-même, dans [Configuration du backend](#backend-configuration) et [Configuration du tableau de bord](#dashboard-configuration). `license.toml` n'est pas livré non plus ; digna le fournit séparément, comme le décrit l'étape 3.

Pour extraire depuis le Terminal :

```bash
unzip digna-2026.11-macos.zip -d /opt/digna
```

#### Rendre l'exécutable exécutable

Selon la manière dont l'archive a été transférée, le bit exécutable peut ne pas avoir été préservé. Définissez-le explicitement :

```bash
cd /opt/digna
chmod +x digna
```

#### Si macOS bloque l'application

Les fichiers téléchargés via un navigateur ou un client mail sont marqués avec un attribut de quarantaine. Si macOS signale que l'application « cannot be opened because the developer cannot be verified », supprimez l'attribut de quarantaine du répertoire d'installation :

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Alternativement, ouvrez **System Settings → Privacy & Security**, trouvez l'élément bloqué en bas de la page et cliquez sur **Open Anyway**.

!!! note "Remarque"

    Cette étape n'est nécessaire que si macOS bloque effectivement l'exécutable. Les paquets transférés via SSH ou depuis des partages internes ne sont généralement pas mis en quarantaine.

### Étape 3 : Installer le fichier de licence

!!! warning "Important"

    Le fichier de licence **n'est pas** inclus dans le paquet d'installation et vous sera fourni séparément par digna.

1. Localisez le fichier `license.toml` qui vous a été fourni
2. Copiez-le dans le répertoire racine d'installation digna (là où se trouvent `config.toml` et l'exécutable `digna`)

**Pourquoi c'est important :**
Le fichier de licence contient vos informations client, la date d'expiration de la licence et la signature numérique. **Ne modifiez pas ce fichier** — toute modification l'invalidera.

**Arborescence après configuration :**

```
/opt/digna/
├── config.toml         (fichier de configuration)
├── license.toml        (VOTRE FICHIER DE LICENCE - copiez-le ici)
├── digna               (exécutable principal)
├── bin/                (scripts de gestion du service)
└── dashboard/          (interface web)
    └── (fichiers du dashboard)
```

---

## Configuration du backend {: #backend-configuration }

### Étape 1 : Créer et éditer le fichier de configuration

Le fichier `config_template.toml` est fourni dans votre répertoire d'installation digna. Renommez-le simplement en `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Emplacement :** `/opt/digna/config.toml`

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

!!! note "Remarque"

    Si vous servez le tableau de bord depuis le nginx de Homebrew sur son port par défaut, l'origine à autoriser est `http://localhost:8080`.

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
| `DIGNA_MAX_WORKERS` | Nombre de cœurs CPU - 1 | Nombre d'inspections pouvant s'exécuter en même temps |
| `DIGNA_FRONTEND_BASEURL` | URL du tableau de bord | Obligatoire. Utilisée pour les liens des messages de notification ; ce doit donc être une URL que les destinataires peuvent ouvrir |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (par défaut) | Facultatif. Nombre de secondes pendant lesquelles une requête sur une base de données source peut s'exécuter avant d'être interrompue ; `0` désactive le délai |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (par défaut) | Facultatif. Nombre de secondes d'attente d'une connexion à une base de données source ; `0` attend indéfiniment |

!!! tip "Astuce"

    Pour connaître le nombre de cœurs CPU disponibles sur votre Mac, exécutez `sysctl -n hw.ncpu`.

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

Cette section configure le comportement des journaux :

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
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Paramètre | Valeur | Notes |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (par défaut) | Mémoire, en MB, qu'une exécution du digna Engine peut utiliser. Jusqu'à `DIGNA_MAX_WORKERS` exécutions peuvent être actives en même temps |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Par défaut : le répertoire temporaire du système (`$TMPDIR` du compte qui exécute digna) | Répertoire des fichiers temporaires lorsque les données ne tiennent pas en mémoire |

!!! tip "Dimensionner le digna Engine"

    Prévoyez jusqu'à `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` de mémoire sur l'hôte
    digna, en plus de ce que digna utilise lui-même, ainsi que suffisamment d'espace disque libre
    dans le répertoire temporaire pour contenir le jour inspecté le plus volumineux des sources de
    données qui utilisent le digna Engine. Faites pointer `DIGNA_DUCKDB_TEMP_DIRECTORY` vers un
    disque disposant de cet espace, accessible en écriture au compte qui exécute digna :

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Cette section n'est nécessaire que si au moins une connexion de base de données utilise le
    digna Engine, ou si un contrôle d'intégrité référentielle compare des sources de données situées
    sur des connexions différentes.

---

### Étape 2 : Vérifier la configuration

Avant d'initialiser le référentiel, vérifiez que `config.toml` est complet et correctement formé. Depuis votre répertoire d'installation digna, exécutez :

```bash
./digna config check
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

### Étape 3 : Initialiser le dépôt

1. Ouvrez **Terminal**
2. Allez dans votre répertoire d'installation digna (là où se trouvent `config.toml` et l'exécutable `digna`)
3. Exécutez le test de connexion :

```bash
cd /opt/digna
./digna repo check
```

Sur un nouveau schéma, la commande se connecte puis signale qu'aucun référentiel n'est encore installé :

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

À ce stade, c'est le résultat attendu : il confirme que digna atteint PostgreSQL et le schéma. Une erreur de connexion ou d'authentification indique au contraire un problème dans la section `[repo]` ou dans la configuration de PostgreSQL.

!!! note "Remarque"

    Sur macOS, les commandes du répertoire courant ne sont pas dans votre PATH, donc l'exécutable est invoqué en tant que `./digna` plutôt que `digna`. Pour pouvoir utiliser la forme courte partout, ajoutez le répertoire d'installation à votre PATH :

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Étape 4 : Installer le schéma du dépôt

Dans le même répertoire, exécutez :

```bash
./digna repo upgrade
```

Cette commande installe les tables nécessaires dans le schéma du référentiel et se termine par :

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade installe et met à niveau"

    À partir de la Release 2026.11, `repo upgrade` installe un nouveau référentiel et met à niveau
    un référentiel existant. `repo install` fonctionne toujours comme autre nom de la même commande.

### Étape 5 : Créer un utilisateur administrateur

1. Ouvrez une **nouvelle** fenêtre Terminal
2. Allez dans votre répertoire d'installation digna
3. Exécutez la commande suivante pour créer un utilisateur administrateur :

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Exemple :**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

Ceci crée un utilisateur avec l'adresse e-mail `admin@example.com` et des privilèges administratifs complets.

!!! tip "Astuce"

    Entourez le mot de passe de guillemets simples. `zsh` traite des caractères tels que `!`, `$` et `*` de manière spéciale, et un mot de passe non cité contenant ces caractères ne sera pas transmis tel quel.

!!! tip "Bonne pratique"

    Utilisez un mot de passe fort contenant un mélange de majuscules, minuscules, chiffres et caractères spéciaux.

---

### Étape 6 : Démarrer le serveur digna

Dans le répertoire d'installation digna, démarrez le serveur avec :

```bash
./digna serve --address <host> --port <port>
```

**Paramètres :**
- `--address` — Nom d'hôte/IP du serveur (par défaut `127.0.0.1`)
- `--port` — Port du serveur (par défaut `8000`)

Une fois le serveur démarré, il affiche l'adresse sur laquelle il écoute :

```text
Server running on http://127.0.0.1:8082
```

!!! tip "Astuce"

    La première fois que vous démarrez le serveur, macOS peut demander si vous souhaitez autoriser l'application à accepter des connexions réseau entrantes. Cliquez sur **Allow**, sinon le tableau de bord ne pourra pas joindre le backend.

!!! note "Le serveur occupe le terminal"

    `serve` s'exécute au premier plan et continue de tourner jusqu'à ce que vous l'arrêtiez avec ++ctrl+c++. Laissez-le tourner pendant que vous terminez la configuration ; pour le démarrer automatiquement au démarrage, voir [Exécuter digna en tant que service en arrière-plan](#running-digna-as-a-background-service).

## Configuration du tableau de bord {: #dashboard-configuration }

### Étape 1 : Déployer le tableau de bord sur le serveur Web

Le tableau de bord digna lit sa propre configuration dans `dashboard/dashboard_config.toml`. Ce fichier n'est pas livré avec l'installation — vous le créez dans le répertoire `dashboard/`, à côté des fichiers du tableau de bord.

Son contenu est décrit sous [Authentification unique (SSO)](../../../sso/overview.md), là où le fichier est également nécessaire : il contient les options de connexion proposées par le tableau de bord et, pour les déploiements multi‑instance, la connexion au backend.

Choisissez votre serveur Web et suivez les étapes de déploiement correspondantes.

#### Déployer sur nginx

Si vous avez suivi la section [Configuration nginx](#nginx-setup), le bloc serveur pointe déjà vers votre dossier `dashboard` et aucune copie n'est requise.

1. **Confirmer le chemin**
   - Ouvrez `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Vérifiez que `root` pointe vers votre dossier `dashboard` extrait

2. **S'assurer que le dossier est lisible**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Recharger nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Tester l'installation**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost:8080` (ou votre URL configurée)
   - Vous devriez voir la page de connexion du tableau de bord digna

#### Déployer sur Apache httpd

1. **Copier le tableau de bord dans la racine du document**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Ajouter les règles de réécriture**

   Créez un fichier `.htaccess` dans le dossier déployé afin que les routes du tableau de bord survivent à un rafraîchissement du navigateur :

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Collez ce qui suit :

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Redémarrer Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Accéder au tableau de bord**
   - Ouvrez votre navigateur
   - Accédez à `http://localhost/digna`
   - Vous devriez voir la page de connexion du tableau de bord digna

---

## Exécution de digna en tant que service d'arrière-plan {: #running-digna-as-a-background-service }

### Pourquoi exécuter digna en tant que service ?

Exécuter le backend digna en tant que service d'arrière-plan garantit qu'il :

- Démarre automatiquement au démarrage de la machine
- S'exécute en arrière-plan sans fenêtre Terminal ouverte
- Redémarre automatiquement en cas de plantage
- Peut être géré via `launchctl`, le gestionnaire de services de macOS

### Fichiers de gestion du service

Tous les fichiers nécessaires se trouvent dans le répertoire d'installation digna sous : `bin/`

Les scripts shell suivants sont disponibles :

- `install_service.sh` — Enregistre digna auprès de launchd
- `uninstall_service.sh` — Désenregistre le service
- `start_service.sh` — Démarre le service enregistré
- `stop_service.sh` — Arrête le service en cours d'exécution

!!! warning "Requiert les droits administrateur"

    Tous les scripts doivent être exécutés avec `sudo`, car l'enregistrement d'un service démarrant au boot écrit dans `/Library/LaunchDaemons`.

### Rendre les scripts exécutables

L'extraction peut ne pas préserver le bit exécutable. Avant la première utilisation :

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Installer le service

1. **Ouvrez Terminal**

2. **Allez dans le dossier bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Exécutez le script d'installation**
   ```bash
   sudo ./install_service.sh
   ```

Le serveur digna est maintenant enregistré auprès de launchd avec le démarrage **automatique** activé. Le service ne démarre pas immédiatement — voir la section suivante pour le démarrer.

### Démarrer et arrêter le service

#### Pour démarrer le service

1. Ouvrez Terminal
2. Allez dans `/opt/digna/bin`
3. Exécutez :
   ```bash
   sudo ./start_service.sh
   ```

#### Pour arrêter le service

1. Ouvrez Terminal
2. Allez dans `/opt/digna/bin`
3. Exécutez :
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Astuce"

    Arrêtez toujours le service avant de mettre à jour les fichiers de l'application.

### Vérifier le service

Pour confirmer que le service est enregistré et en cours d'exécution :

```bash
sudo launchctl list | grep digna
```

Une ligne commençant par un PID indique que le service est en cours d'exécution. Un `-` dans la première colonne signifie qu'il est enregistré mais arrêté.

### Déplacer le service vers un nouveau répertoire

launchd stocke le chemin absolu vers l'exécutable, donc déplacer l'installation nécessite de réenregistrer le service :

1. **Désinstaller le service actuel**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Déplacer les fichiers de l'application**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Réinstaller le service**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Démarrer le service**
   ```bash
   sudo ./start_service.sh
   ```

### Désinstaller le service

1. **Arrêter le service en cours d'exécution**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Désinstaller le service**
   ```bash
   sudo ./uninstall_service.sh
   ```

Le serveur digna est maintenant désenregistré de launchd.

---

## Mise à niveau vers une nouvelle version {: #upgrading-to-a-new-release }

Cette section décrit la mise à niveau d'une installation de la Release 2026.06 vers la Release
2026.11. Si votre installation est plus ancienne, lisez d'abord
[Mise à niveau depuis une release antérieure à 2026.06](#upgrading-from-a-release-before-2026-06).

### Avant de mettre à niveau

**La création d'une sauvegarde du référentiel digna est obligatoire**

Avant de mettre à niveau digna, sauvegardez votre référentiel (PostgreSQL) pour vous protéger contre la perte de données.
Une sauvegarde vous permet de restaurer en cas de problème inattendu pendant la mise à niveau.

Pour créer une sauvegarde depuis le Terminal :

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

**Demander le fichier de licence de la Release 2026.11**

La Release 2026.11 nécessite un nouveau `license.toml`. Demandez-le à l'équipe digna avant de
commencer, et gardez-le à portée de main pour l'[étape 7](#step-7-replace-the-license-file).

### Mise à niveau depuis une release antérieure à 2026.06 {: #upgrading-from-a-release-before-2026-06 }

La Release 2026.06 a apporté trois changements qui s'appliquent toujours lorsque vous mettez à
niveau une installation plus ancienne directement vers la 2026.11 :

- **ODBC uniquement.** digna atteint chaque technologie source via ODBC. Toute connexion de base de
  données qui n'utilise pas encore ODBC doit être convertie à ODBC après la mise à niveau ; il n'y
  a pas de conversion automatique. Installez au préalable les pilotes ODBC sur l'hôte digna, voir
  [Installer le pilote ODBC sur l'hôte digna](../../../databases/overview.md#install-the-driver),
  et préparez les propriétés de chaque connexion à partir des
  [guides par technologie](../../../databases/overview.md#technology-guides). Le connecteur
  Databricks Legacy n'existe plus ; migrez ces connexions vers le connecteur
  [Databricks](../../../databases/databricks_connector_guide.md).
- **Un seul exécutable.** `dignabackend` et `dignacli` sont remplacés par l'exécutable unique
  `digna`, qui réunit le backend et la CLI.
- **config.toml.** La section `[encryption]` est obligatoire, et `DIGNA_APP_HOST` et
  `DIGNA_APP_PORT` ne sont plus lus : le serveur tire son adresse et son port de `digna serve`.
  Comparez votre fichier avec [Configuration du backend](#backend-configuration).

Les étapes ci-dessous signalent les points où une installation plus ancienne demande une démarche
différente. La mise à niveau du référentiel à l'étape 8 amène directement un référentiel de
n'importe quelle release antérieure à la 2026.11.

### Processus de mise à niveau

#### Étape 1 : Arrêter le service digna {: #step-1-stop-the-digna-service }

Si digna s'exécute en tant que service d'arrière-plan, arrêtez-le d'abord :

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Si digna s'exécute au premier plan, appuyez sur ++ctrl+c++ dans sa fenêtre Terminal.

#### Étape 2 : Sauvegarder l'installation actuelle {: #step-2-backup-current-installation }

Dans votre répertoire d'installation digna, renommez l'exécutable et le dossier du tableau de bord
de votre installation actuelle, afin que la nouvelle version puisse être déployée à côté :

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Conservez `digna_old` jusqu'à ce que vous ayez vérifié la mise à niveau, et `dashboard_old` jusqu'à
ce que vous en ayez restauré vos fichiers de configuration (voir l'étape 4). Vous pourrez ensuite
supprimer les deux.

!!! info "Mise à niveau depuis une release antérieure à 2026.06"

    Renommez les dossiers `dignabackend` et `dignacli` au lieu de l'exécutable :
    `mv dignabackend dignabackend_old` et `mv dignacli dignacli_old`. Aucun des deux n'est utilisé par la Release 2026.11.

#### Étape 3 : Extraire et déployer la nouvelle version {: #step-3-extract-and-deploy-new-version }

1. Extrayez le nouveau fichier ZIP d'installation digna
2. Copiez le nouvel exécutable `digna` et le dossier `dashboard` vers votre répertoire d'installation
3. Restaurez le bit exécutable et, si nécessaire, supprimez l'attribut de quarantaine :

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Important"

    Ni `config.toml` ni `dashboard/dashboard_config.toml` ne sont jamais inclus dans le ZIP
    d'installation — l'équipe digna ne livre jamais aucun de ces deux fichiers. Votre configuration
    existante n'est donc pas touchée par la mise à niveau, et les copies se trouvant dans les
    dossiers renommés `*_old` sont les seules dont vous disposez.

#### Étape 4 : Restaurer vos fichiers de configuration {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
(++cmd+shift+r++).

#### Étape 6 : Vérifier la configuration {: #step-6-validate-the-configuration }

Assurez-vous que `config.toml` est complet avant de toucher au référentiel :

```bash
./digna config check
```

Chaque section doit être signalée OK. Corrigez tout ce qui est signalé comme FAILED, supprimez les
clés listées sous **Unknown keys**, et relancez la commande avant de continuer.

#### Étape 7 : Remplacer le fichier de licence {: #step-7-replace-the-license-file }

Un fichier de licence est normalement repris d'une release à la suivante. La Release 2026.11 fait
exception : elle ajoute deux modules sous licence, digna Data Reconciliation et digna Agentic, et
une licence émise avant la 2026.11 ne les contient pas. Copiez le `license.toml` fourni par
l'équipe digna pour la Release 2026.11 dans le répertoire d'installation, en remplaçant l'ancien :

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Ne conservez pas la licence précédente"

    Avec la licence précédente, digna démarre toujours, mais digna Data Reconciliation et le digna
    MCP Server restent désactivés. Chaque commande qui vérifie la licence — `user`, `inspection`,
    `repo` — s'interrompt avant de toucher au référentiel lorsque la vérification échoue. Vérifiez
    la nouvelle licence avant d'aller plus loin :

    ```bash
    ./digna license check
    ```

#### Étape 8 : Mettre à niveau le schéma du référentiel {: #step-8-upgrade-the-repository-schema }

Dans votre répertoire d'installation digna, exécutez :

```bash
cd /opt/digna
./digna repo upgrade
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
exécutez `./digna repo check` : la commande liste la dernière migration appliquée et celles qui sont
encore en attente.

!!! warning "digna ne démarre pas sur un référentiel obsolète"

    À partir de la Release 2026.11, le serveur refuse de démarrer tant que le référentiel nécessite
    une mise à niveau, et l'indique, par exemple :

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Exécutez `repo upgrade` avant de démarrer le serveur ou le service.

#### Étape 9 : Redémarrer les services {: #step-9-restart-services }

Si vous l'exécutez en tant que service d'arrière-plan :

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Si vous l'exécutez manuellement, redémarrez le serveur :

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Si vous utilisez nginx ou Apache, redémarrez le serveur web correspondant :

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Étape 10 : Vérifier la mise à niveau {: #step-10-verify-the-upgrade }

1. Vérifiez la release du nouvel exécutable :

    ```bash
    ./digna version
    ```

    La première ligne doit indiquer `Release: 2026.11`.

2. Accédez au tableau de bord digna et vérifiez que l'interface se charge correctement.
3. Consultez la sortie du serveur et les fichiers du répertoire `logs` pour détecter des erreurs.
4. Testez vos connexions de base de données — voir
   [Tester une connexion](../../../databases/overview.md#testing-a-connection). Après une mise à
   niveau depuis une release antérieure à 2026.06, convertissez d'abord à ODBC chaque connexion
   qui ne l'utilisait pas encore.

Pour commencer avec les nouveaux modules, voir [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Connecter un agent IA](../../../platform/agentic/connect_ai_agent.md) pour le digna MCP Server, et
[Emplacement de profilage](../../../platform/profiling/profiling_location.md) pour le digna Engine.