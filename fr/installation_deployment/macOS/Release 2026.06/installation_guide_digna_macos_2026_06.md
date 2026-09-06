# Guide d'installation macOS pour digna Release 2026.06

**Release :** 2026.06

**Dernière mise à jour :** 5 septembre 2026


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

- **dignabackend** : Le moteur central de l'application, responsable du traitement des données et de l'exécution des contrôles de qualité.
- **dignadashboard** : Une interface web hébergée sur un serveur web, fournissant un moyen convivial d'interagir avec la plateforme digna et de visualiser les indicateurs de qualité des données.

### Nouveautés de la Release 2026.06

Cette version apporte des capacités d'observabilité des données directement dans votre code, permettant aux développeurs de surveiller la qualité des données à la source. Voir les [notes de version](http://docs.digna.ai/changelog/Release_202606/) pour les détails complets.

### Besoin d'un guide pour Windows ou Linux ?

Ce guide couvre macOS. Pour d'autres plateformes, consultez le [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ou le [Linux Installation Guide](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

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
   - `config.toml` — Fichier de configuration
   - `license.toml` — Fichier de licence (copiez le vôtre ici)

Pour extraire depuis le Terminal :

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
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
| `digna_APP_HOST` | `localhost` ou adresse IP | Nom d'hôte ou IP où dignabackend est hébergé |
| `digna_APP_PORT` | `8082` (par défaut) | Port des endpoints REST |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL du frontend | Si le tableau de bord est sur un serveur différent, incluez son URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requis pour le CORS avec identifiants |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Autorise toutes les méthodes HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Autorise tous les en-têtes |

!!! note "Remarque"

    Si vous servez le tableau de bord depuis le nginx de Homebrew sur son port par défaut, l'origine à autoriser est `http://localhost:8080`.

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

Cette section contient les paramètres de sécurité et de cookie :

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
| `digna_COOKIE_DOMAIN` | `localhost` | Doit correspondre à votre domaine frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Utilisez `true` pour les connexions HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Toujours activé pour la sécurité |
| `digna_COOKIE_SAME_SITE` | `lax` | Aide à prévenir les attaques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 heures) | Durée de session en secondes |
| `digna_MAX_WORKERS` | Nombre de cœurs CPU - 1 | Nombre de tâches d'inspection parallèles |

!!! tip "Astuce"

    Pour connaître le nombre de cœurs CPU disponibles sur votre Mac, exécutez `sysctl -n hw.ncpu`.

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

### Étape 2 : Initialiser le dépôt

1. Ouvrez **Terminal**
2. Allez dans votre répertoire d'installation digna (là où se trouvent `config.toml` et l'exécutable `digna`)
3. Exécutez le test de connexion :

```bash
cd /opt/digna
./digna repo check
```

Vous devriez voir une confirmation que la connexion est établie (le dépôt lui-même n'a pas encore été initialisé).

!!! note "Remarque"

    Sur macOS, les commandes du répertoire courant ne sont pas dans votre PATH, donc l'exécutable est invoqué en tant que `./digna` plutôt que `digna`. Pour pouvoir utiliser la forme courte partout, ajoutez le répertoire d'installation à votre PATH :

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Étape 3 : Installer le schéma du dépôt

Dans le même répertoire, exécutez :

```bash
./digna repo install
```

Cette commande installe les tables et le schéma nécessaires dans votre base de données PostgreSQL.

### Étape 4 : Démarrer le serveur digna

Dans le répertoire d'installation digna, démarrez le serveur avec :

```bash
./digna serve --address <host> --port <port>
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

!!! tip "Astuce"

    La première fois que vous démarrez le serveur, macOS peut demander si vous souhaitez autoriser l'application à accepter des connexions réseau entrantes. Cliquez sur **Allow**, sinon le tableau de bord ne pourra pas joindre le backend.

### Étape 5 : Créer un utilisateur administrateur

1. Ouvrez une **nouvelle** fenêtre Terminal
2. Allez dans votre répertoire d'installation digna
3. Exécutez la commande suivante pour créer un utilisateur administrateur :

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Exemple :**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Cela crée un utilisateur avec le nom d'utilisateur `admin` et des privilèges administratifs complets.

!!! tip "Astuce"

    Entourez le mot de passe de guillemets simples. `zsh` traite des caractères tels que `!`, `$` et `*` de manière spéciale, et un mot de passe non cité contenant ces caractères ne sera pas transmis tel quel.

!!! tip "Bonne pratique"

    Utilisez un mot de passe fort contenant un mélange de majuscules, minuscules, chiffres et caractères spéciaux.

---

## Configuration du tableau de bord {: #dashboard-configuration }

### Étape 1 : Déployer le tableau de bord sur le serveur Web

Le tableau de bord digna possède son propre fichier `config.toml` situé dans le répertoire `dashboard/`. Cette configuration est déjà fournie et ne nécessite pas de modifications lors de l'installation initiale. Vous n'avez besoin de la modifier que si vous devez personnaliser la connexion au backend.

Si vous devez ajuster la configuration du tableau de bord (par ex., pour des déploiements multi-instance), consultez la documentation du tableau de bord.

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

### Avant la mise à niveau

**La création d'une sauvegarde du dépôt digna est OBLIGATOIRE**

Avant de mettre à niveau digna, sauvegardez votre dépôt (PostgreSQL) pour vous protéger contre la perte de données.
Une sauvegarde vous permettra de récupérer en cas de problème imprévu lors de la mise à niveau.

Pour créer une sauvegarde depuis le Terminal :

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Processus de mise à niveau

#### Étape 1 : Arrêter le service digna

Si digna s'exécute en tant que service d'arrière-plan, arrêtez-le d'abord :

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Si digna s'exécute au premier plan, appuyez sur `Ctrl + C` dans sa fenêtre Terminal.

#### Étape 2 : Sauvegarder l'installation actuelle du backend

Dans votre répertoire d'installation digna :

```bash
cd /opt/digna
mv digna digna_old
```
```bash
mv dashboard dashboard_old
```

#### Étape 3 : Extraire et déployer la nouvelle version

1. Extrayez le nouveau fichier ZIP d'installation digna
2. Copiez le nouvel exécutable `digna` et le dossier `dashboard` dans votre répertoire d'installation
3. Restaurez le bit exécutable et, si nécessaire, supprimez l'attribut de quarantaine :

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Important"

    Le fichier `config.toml` **n'est jamais** inclus dans le ZIP d'installation. Votre configuration existante reste protégée.

### Étape 4 : Restaurer vos fichiers de configuration

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Étape 5 : Mettre à niveau le schéma du dépôt

Allez dans votre répertoire d'installation digna et exécutez :

```bash
cd /opt/digna
./digna repo upgrade
```

Cela met à jour le schéma PostgreSQL vers la dernière version tout en conservant toutes les données existantes.

### Étape 6 : Redémarrer les services

Si vous exécutez digna en tant que service d'arrière-plan :

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

#### Étape 7 : Vérifier la mise à niveau

1. Accédez au tableau de bord digna
2. Vérifiez que l'interface se charge correctement
3. Consultez les journaux du serveur pour détecter d'éventuelles erreurs