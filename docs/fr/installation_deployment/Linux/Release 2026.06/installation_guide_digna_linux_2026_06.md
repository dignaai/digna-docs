---
title: Guide d'installation Linux – digna Release 2026.06 | Documentation digna
description: Guide étape par étape pour installer digna Release 2026.06 sur Linux — exigences système, configuration de PostgreSQL, configuration de nginx ou Apache, configuration du backend et du tableau de bord, exécution de digna en tant que service systemd et mise à niveau vers une nouvelle version.
keywords: installation digna linux, guide de déploiement digna, configuration backend digna, installation tableau de bord digna, postgresql linux, nginx linux, service digna systemd, guide de mise à niveau digna
image: /assets/logo_square.png
---

# Guide d'installation Linux pour digna Release 2026.06

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
9. [Exécution de digna en tant que service systemd](#running-digna-as-a-systemd-service)
10. [Mise à niveau vers une nouvelle version](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### À propos de digna

digna est une plateforme complète pilotée par l'IA conçue pour optimiser la gestion de la qualité des données dans divers environnements de données tels que les entrepôts, les lacs et les lakehouses. Conçue pour être hautement évolutive et adaptable, digna répond aux défis modernes des données grâce à l'automatisation, la surveillance en temps réel et la détection d'anomalies.

digna se compose de deux éléments principaux :

- **dignabackend** : Le moteur principal de l'application, responsable du traitement des données et de l'exécution des contrôles qualité.
- **dignadashboard** : Une interface web hébergée sur un serveur web, offrant un moyen convivial d'interagir avec la plateforme digna et de visualiser les métriques de qualité des données.

### Nouveautés de la Release 2026.06

Cette version apporte des capacités d'observabilité des données directement dans votre code, permettant aux développeurs de surveiller la qualité des données à la source. Consultez les [release notes](http://docs.digna.ai/changelog/Release_202606/) pour tous les détails.

### Vous cherchez Windows ou macOS ?

Ce guide couvre Linux. Pour d'autres plateformes, voir le [Windows Installation Guide](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) ou le [macOS Installation Guide](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Quelle distribution couvre ce guide ?

Les instructions sont rédigées pour les deux familles de serveurs les plus courantes. Lorsque les deux diffèrent, les deux commandes sont fournies :

- **famille Debian** — Debian, Ubuntu. Gestionnaire de paquets : `apt`.
- **famille RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Gestionnaire de paquets : `dnf`.

Toute distribution moderne avec `systemd` fonctionnera ; seuls les noms de paquets et quelques chemins de configuration changent.

---

## Exigences système {: #system-requirements }

Avant de commencer l'installation, assurez-vous que votre système respecte les exigences minimales suivantes :

| Exigence | Spécification |
|---|---|
| **Système d'exploitation** | Ubuntu 22.04 LTS ou ultérieur, Debian 12 ou ultérieur, RHEL 9 / Rocky 9 / AlmaLinux 9 ou ultérieur |
| **Architecture** | x86_64 (amd64) ou arm64 |
| **Système d'init** | systemd |
| **Mémoire (installation minimale)** | 16 GB RAM |
| **Espace disque** | 10 GB d'espace disponible |
| **Base de données** | PostgreSQL Server 12 ou supérieur |
| **Serveur Web** | nginx, Apache httpd, ou équivalent |

### Options d'installation de la base de données

**Si PostgreSQL est déjà installé :**
Vous pouvez ajouter une nouvelle base de données pour digna à votre serveur PostgreSQL existant.

**Si vous installez PostgreSQL sur la même machine que digna :**

!!! info "Spécifications recommandées"

    - **Mémoire** : 32 GB RAM (au lieu de 16 GB)
    - **Espace disque** : 50 GB d'espace disponible (au lieu de 10 GB)

    Ces spécifications supérieures accommodent à la fois digna et le serveur PostgreSQL fonctionnant simultanément.

### Vérifier votre distribution et votre architecture

Plusieurs commandes de ce guide diffèrent entre les familles Debian et RHEL. Pour vérifier laquelle vous utilisez, lancez :

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` ou `ID=debian` — utilisez les commandes `apt`.
- `ID=rhel`, `rocky`, `almalinux` ou `fedora` — utilisez les commandes `dnf`.
- `x86_64` ou `aarch64` — l'architecture du paquet d'installation dont vous avez besoin.

---

## Préparation avant l'installation {: #pre-installation-setup }

Avant d'installer digna, assurez-vous que deux prérequis clés sont en place :

1. **Serveur PostgreSQL** – pour stocker les métriques calculées et les données de performance
2. **Serveur Web** – pour héberger le Dashboard de digna

Si ces composants ne sont pas déjà configurés, suivez les sections ci-dessous pour les installer et les configurer.

### Actualisation de l'index des paquets

Mettez à jour vos listes de paquets avant d'installer quoi que ce soit :

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Remarque"

    Tout au long de ce guide, la première commande d'une paire est pour la **famille Debian** et la seconde pour la **famille RHEL**. Exécutez uniquement celle qui correspond à votre système.

---

## Configuration du serveur PostgreSQL {: #postgresql-server-setup }

### Si vous avez déjà PostgreSQL

Si PostgreSQL est déjà installé et en cours d'exécution sur votre machine locale ou si vous utilisez un serveur PostgreSQL géré à distance, vous pouvez passer à la [section suivante](#web-server-configuration).

### Installation de PostgreSQL

#### Étape 1 : Installer le paquet serveur

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Astuce"

    Les paquets des distributions peuvent être en retard par rapport à la version actuelle de PostgreSQL. Si vous avez besoin d'une version plus récente spécifique, utilisez le dépôt officiel [PostgreSQL apt ou yum](https://www.postgresql.org/download/linux/).

#### Étape 2 : Initialiser le cluster de bases

Sur la **famille Debian**, le paquet crée et démarre automatiquement un cluster — passez à l'étape suivante.

Sur la **famille RHEL**, le cluster doit être créé explicitement :

```bash
sudo postgresql-setup --initdb
```

#### Étape 3 : Démarrer et activer le service

```bash
sudo systemctl enable --now postgresql
```

Cela démarre PostgreSQL immédiatement et le configure pour redémarrer automatiquement au démarrage.

#### Étape 4 : Vérifier l'installation

```bash
psql --version
sudo systemctl status postgresql
```

Vous devriez voir la version de PostgreSQL et un service `active (running)`.

#### Étape 5 : Se connecter au serveur

Un paquet PostgreSQL Linux crée un compte système `postgres` qui possède le cluster. Connectez-vous via ce compte :

```bash
sudo -u postgres psql
```

!!! note "Remarque — Différence avec Windows"

    L'installateur Windows vous invite à définir un mot de passe pour le superutilisateur `postgres` pendant l'installation. Les paquets Linux ne le font pas. À la place, les connexions locales sont authentifiées par **peer authentication** : l'utilisateur système `postgres` est autorisé à se connecter en tant qu'utilisateur de base de données `postgres` sans mot de passe.

    C'est pourquoi la commande ci‑dessus utilise `sudo -u postgres`. Le backend digna se connecte via TCP avec un nom d'utilisateur et un mot de passe, donc vous créerez un utilisateur digna explicite dans [Installation initiale](#initial-installation).

#### Étape 6 : Confirmer le port

Le port PostgreSQL par défaut est `5432`. Pour confirmer le port sur lequel votre serveur écoute :

```bash
sudo -u postgres psql -c "SHOW port;"
```

Notez la valeur — vous en aurez besoin lors de la configuration du backend digna.

#### Étape 7 : Autoriser l'authentification par mot de passe pour l'utilisateur digna

digna se connecte à PostgreSQL via TCP en tant que `digna_user`, ce qui nécessite l'authentification par mot de passe plutôt que par peer authentication. Vérifiez que votre `pg_hba.conf` le permet.

Localisez le fichier :

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Ouvrez-le dans un éditeur et confirmez que les lignes TCP locales utilisent `scram-sha-256` (ou `md5` sur les serveurs plus anciens) plutôt que `ident` :

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Rechargez PostgreSQL après toute modification :

```bash
sudo systemctl reload postgresql
```

!!! warning "Important"

    Si digna signale `FATAL: Ident authentication failed for user "digna_user"`, ce paramètre en est la cause.

#### Étape 8 : Si PostgreSQL fonctionne sur une autre machine

Pour accepter les connexions depuis un hôte différent, définissez `listen_addresses` dans `postgresql.conf` et ajoutez une ligne `host` correspondante pour votre réseau dans `pg_hba.conf` :

```
listen_addresses = '*'
```

Ensuite, ouvrez le port dans le pare-feu et redémarrez le service :

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Configuration du serveur Web {: #web-server-configuration }

digna nécessite un serveur web pour héberger le tableau de bord. Choisissez l'une des options suivantes :

- [nginx](#nginx-setup) — léger et recommandé
- [Apache httpd](#apache-setup) — alternative largement déployée

Vous n'avez besoin d'installer et de configurer **qu'un seul** de ces serveurs.

Les deux sections configurent deux éléments dont dépend le tableau de bord :

- **Un fallback pour application monopage (single-page-application)**, afin qu'un rafraîchissement d'URL du tableau de bord ne retourne pas un 404
- **Un type MIME `.md`**, pour que les fichiers Markdown soient servis correctement

### Configuration de nginx {: #nginx-setup }

#### Vue d'ensemble

nginx est un serveur web léger et performant, bien adapté pour servir le tableau de bord statique de digna.

#### Installation

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Démarrage de nginx

```bash
sudo systemctl enable --now nginx
```

#### Vérifier l'installation

1. Ouvrez votre navigateur
2. Allez à `http://localhost`
3. Vous devriez voir la page d'accueil nginx

#### Ouverture du pare-feu

Si le serveur est atteint depuis d'autres machines, autorisez le trafic HTTP :

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Configuration d'un site pour le tableau de bord

nginx inclut tous les fichiers de son répertoire `conf.d` pour les deux familles de distribution. Créez un fichier de configuration dédié pour digna à cet emplacement :

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Collez ce qui suit, en remplaçant `/opt/digna/dashboard` par le chemin réel vers votre dossier `dashboard` extrait :

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
    index  index.html;

    # Servir les fichiers Markdown avec le type MIME correct.
    types {
        text/markdown  md;
    }

    # Fallback pour application monopage : les chemins inconnus retournent index.html
    # au lieu d'un 404, afin que les routes du tableau de bord survivent à un rafraîchissement du navigateur.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Important"

    Sans la directive `try_files`, le rechargement de toute page du tableau de bord autre que l'URL racine renverra un 404. C'est l'équivalent nginx du module URL Rewrite requis par IIS sous Windows.

#### Désactiver le site par défaut

Un seul bloc server peut être `default_server` pour un port. Sur la **famille Debian**, supprimez le site par défaut packagé pour qu'il ne rentre pas en conflit :

```bash
sudo rm /etc/nginx/sites-enabled/default
```

Sur la **famille RHEL**, commentez ou supprimez le bloc `server { ... }` à l'intérieur de `/etc/nginx/nginx.conf`.

#### Appliquer la configuration

Testez la configuration pour les erreurs de syntaxe, puis rechargez nginx :

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Configuration d'Apache httpd {: #apache-setup }

#### Vue d'ensemble

Apache httpd est disponible dans les dépôts par défaut de toutes les distributions prises en charge. Le paquet s'appelle `apache2` dans la famille Debian et `httpd` dans la famille RHEL.

#### Installation

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Démarrage d'Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Vérifier l'installation

1. Ouvrez votre navigateur
2. Allez à `http://localhost`
3. Vous devriez voir la page par défaut Apache de la distribution

#### Requis : activer mod_rewrite

Le tableau de bord nécessite la réécriture d'URL.

Sur la **famille Debian**, activez le module et redémarrez :

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

Sur la **famille RHEL**, `mod_rewrite` est chargé par défaut. Confirmez-le :

```bash
httpd -M | grep rewrite
```

#### Requis : autoriser les overrides .htaccess

Ouvrez le fichier de configuration pour votre document root :

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Localisez le bloc `<Directory>` couvrant votre document root (`/var/www/html` sur les deux familles) et remplacez :

```apache
AllowOverride None
```

par :

```apache
AllowOverride All
```

#### Requis : type MIME pour les fichiers Markdown

Dans le même fichier, ajoutez la ligne suivante afin que les fichiers Markdown soient servis correctement :

```apache
AddType text/markdown .md
```

!!! warning "Important"

    Sans ce paramètre, les fichiers `.md` peuvent ne pas être servis correctement.

#### Appliquer la configuration

Vérifiez la configuration pour les erreurs de syntaxe, puis redémarrez Apache :

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
```

---

## Installation initiale {: #initial-installation }

### Étape 1 : Configurer le repository digna

Le repository digna stocke toutes les métriques calculées par digna. Il sert de base de données centrale pour les données analytiques et de performance.

#### Créer le schéma du repository et l'utilisateur

Ouvrez votre client PostgreSQL (psql, pgAdmin ou similaire) et exécutez les commandes SQL suivantes :

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Remplacez les paramètres suivants :**

- `<digna_repo_schema>` — le nom de schéma souhaité (par ex. `dignarepo`)
- `<digna_repo_user>` — le nom d'utilisateur souhaité (par ex. `digna_user`)
- `<digna_repo_password>` — un mot de passe sécurisé pour cet utilisateur

**Exemple :**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

Pour exécuter ces commandes depuis le shell en une seule étape :

```bash
sudo -u postgres psql
```

Puis collez les instructions à l'invite `postgres=#` et tapez `\q` pour quitter.

!!! tip "Bonne pratique"

    Utilisez des mots de passe forts et complexes pour les utilisateurs de base de données. Évitez des identifiants facilement devinables.

---

### Étape 2 : Extraire le paquet d'installation digna

1. Localisez le fichier ZIP d'installation de digna qui vous a été fourni
2. Extrayez-le à l'emplacement d'installation souhaité — par exemple `/opt/digna`
3. Après extraction, vous devriez voir les éléments suivants :
   - `dashboard/` — interface du tableau de bord Web
   - `digna` — exécutable principal (backend + CLI combinés)
   - `config.toml` — fichier de configuration
   - `license.toml` — fichier de licence (copiez le vôtre ici)

Pour extraire depuis le shell :

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Remarque"

    Si `unzip` n'est pas installé, ajoutez-le avec `sudo apt install -y unzip` ou `sudo dnf install -y unzip`.

#### Rendre l'exécutable exécutable

Selon la manière dont l'archive a été transférée, le bit exécutable peut ne pas avoir été conservé. Réglez-le explicitement :

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Créer un compte de service

Il est recommandé d'exécuter le backend sous un utilisateur dédié sans privilèges pour les déploiements en production :

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Remarque"

    Sur la famille RHEL, le chemin de shell équivalent est `/sbin/nologin`.

### Étape 3 : Installer le fichier de licence

!!! warning "Important"

    Le fichier de licence **n'est pas** inclus dans le paquet d'installation et vous sera fourni séparément par digna.

1. Localisez le fichier `license.toml` qui vous a été fourni
2. Copiez-le dans le répertoire racine d'installation de digna (là où se trouvent `config.toml` et l'exécutable `digna`)

**Pourquoi c'est important :**
Le fichier de licence contient vos informations client, la date d'expiration de la licence et la signature numérique. **Ne modifiez pas ce fichier** — toute modification l'invalidera.

**Arborescence après la configuration :**

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

### Étape 1 : Créer et éditer le fichier de configuration

Le fichier `config_template.toml` est fourni dans votre répertoire d'installation digna. Vous devez simplement le renommer en `config.toml`.

```bash
cd /opt/digna
sudo mv config_template.toml config.toml
```

**Emplacement :** `/opt/digna/config.toml`

Ouvrez `config.toml` dans un éditeur de texte et configurez chaque section ci‑dessous.

#### Section [app]

Cette section configure les paramètres de l'application backend de digna :

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Paramètre | Valeur | Notes |
|---|---|---|
| `digna_APP_HOST` | `localhost` ou adresse IP | Nom d'hôte ou IP où est hébergé dignabackend |
| `digna_APP_PORT` | `8082` (par défaut) | Port pour les endpoints REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL du frontend | Si le tableau de bord est sur un serveur différent, incluez son URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Requis pour le CORS avec des identifiants |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Autoriser toutes les méthodes HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Autoriser tous les en-têtes |

!!! note "Remarque"

    Si vous servez le tableau de bord depuis nginx ou Apache sur le port HTTP par défaut, l'origine à autoriser est `http://localhost` — ou l'URL publique du serveur lorsque le tableau de bord est atteint depuis d'autres machines.

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

| Paramètre | Valeur | Notes |
|---|---|---|
| `digna_REPO_HOST` | `localhost` ou IP | Nom d'hôte/IP du serveur PostgreSQL |
| `digna_REPO_PORT` | `5432` (par défaut) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nom de la base de données |
| `digna_REPO_SCHEMA` | `dignarepo` | Schéma créé précédemment |
| `digna_REPO_USER` | `digna_user` | Utilisateur créé lors de la configuration PostgreSQL |
| `digna_REPO_PASSWORD` | Votre mot de passe | Mot de passe défini lors de la création du schéma |

!!! tip "Bonne pratique"

    `config.toml` contient un mot de passe de base de données en clair. Restreignez ses permissions afin que seul le compte de service puisse le lire :

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

| Paramètre | Valeur | Notes |
|---|---|---|
| `digna_FERNET_KEY` | Clé de chiffrement | Utilisée pour chiffrer les tokens et les cookies (valeur par défaut fournie) |
| `digna_COOKIE_DOMAIN` | `localhost` | Doit correspondre au domaine de votre frontend |
| `digna_COOKIE_SECURE` | `false` (local) / `true` (production) | Utilisez `true` pour les connexions HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Toujours activé pour la sécurité |
| `digna_COOKIE_SAME_SITE` | `lax` | Prévient les attaques CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 heures) | Durée d'expiration de la session en secondes |
| `digna_MAX_WORKERS` | Nombre de cœurs CPU - 1 | Nombre de tâches d'inspection parallèles |

!!! tip "Astuce"

    Pour connaître le nombre de cœurs CPU disponibles sur votre serveur, exécutez `nproc`.

#### Section [logging]

Cette section configure le comportement de journalisation :

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Paramètre | Valeur | Notes |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` ou `DEBUG` | `INFO` pour la production, `DEBUG` pour le dépannage |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Nombre de sauvegardes journalières des journaux à conserver |

---

### Étape 2 : Initialiser le repository

1. Ouvrez un terminal
2. Placez-vous dans votre répertoire d'installation digna (là où se trouvent `config.toml` et l'exécutable `digna`)
3. Lancez le test de connexion :

```bash
cd /opt/digna
./digna repo check
```

Vous devriez voir une confirmation que la connexion est établie (le repository lui‑même n'a pas encore été initialisé).

!!! note "Remarque"

    Sur Linux, le répertoire courant n'est pas dans votre PATH, donc l'exécutable est invoqué en tant que `./digna` plutôt que `digna`. Pour utiliser la forme plus courte partout, ajoutez un lien symbolique :

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
    ```

### Étape 3 : Installer le schéma du repository

Dans le même répertoire, exécutez :

```bash
./digna repo install
```

Cette commande installe les tables et le schéma nécessaires dans votre base PostgreSQL.

### Étape 4 : Démarrer le serveur digna

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

    Si le tableau de bord est servi depuis une machine différente du backend, ouvrez également le port API dans le pare-feu :

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

### Étape 5 : Créer un utilisateur administrateur

1. Ouvrez un **nouveau** terminal
2. Placez-vous dans votre répertoire d'installation digna
3. Exécutez la commande suivante pour créer un utilisateur admin :

```bash
./digna user add <username> "<full_name>" <password> --su
```

**Exemple :**

```bash
./digna user add admin "Admin User" 'AdminPassword123!' --su
```

Ceci crée un utilisateur avec le nom d'utilisateur `admin` et des privilèges administratifs complets.

!!! tip "Astuce"

    Entourez le mot de passe de guillemets simples. `bash` et `zsh` traitent des caractères tels que `!`, `$` et `*` de façon spéciale, et un mot de passe non cité les contenant ne sera pas transmis tel quel.

!!! tip "Bonne pratique"

    Utilisez un mot de passe fort mélangeant majuscules, minuscules, chiffres et caractères spéciaux.

---

## Configuration du tableau de bord {: #dashboard-configuration }

### Étape 1 : Déployer le tableau de bord sur le serveur Web

Le tableau de bord digna possède son propre fichier `config.toml` séparé situé dans le répertoire `dashboard/`. Cette configuration est déjà fournie et ne nécessite pas de modification lors de l'installation initiale. Vous ne devez la modifier que si vous voulez personnaliser la connexion au backend.

Si vous devez modifier la configuration du tableau de bord (par ex. pour des déploiements multi‑instance), reportez-vous à la documentation du tableau de bord.

Choisissez votre serveur web et suivez les étapes de déploiement correspondantes.

#### Déploiement sur nginx

Si vous avez suivi la section [nginx Setup](#nginx-setup), le bloc server pointe déjà vers votre dossier `dashboard` et aucune copie n'est requise.

1. **Confirmez le chemin**
   - Ouvrez `/etc/nginx/conf.d/digna.conf`
   - Vérifiez que `root` pointe vers votre dossier `dashboard` extrait

2. **Assurez-vous que le dossier est lisible**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Rechargez nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Tester l'installation**
   - Ouvrez votre navigateur
   - Allez à `http://localhost` (ou votre URL configurée)
   - Vous devriez voir la page de connexion du tableau de bord digna

#### Déploiement sur Apache httpd

1. **Copiez le tableau de bord dans le document root**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Ajouter les règles de réécriture**

   Créez un fichier `.htaccess` dans le dossier déployé afin que les routes du tableau de bord survivent à un rafraîchissement du navigateur :

   ```bash
   sudo nano /var/www/html/digna/.htaccess
   ```

   Collez ce qui suit :

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Servir les fichiers et répertoires existants tels quels.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Tout le reste retombe sur le point d'entrée de l'application monopage.
   RewriteRule ^ index.html [L]
   ```

3. **Redémarrer Apache**
   ```bash
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Accéder au tableau de bord**
   - Ouvrez votre navigateur
   - Allez à `http://localhost/digna`
   - Vous devriez voir la page de connexion du tableau de bord digna

### Étape 2 : SELinux (famille RHEL uniquement)

Sur RHEL, Rocky, AlmaLinux et Fedora, SELinux est en mode enforcing par défaut et bloquera le serveur web qui tente de lire des fichiers en dehors de ses emplacements attendus. Vérifiez s'il est actif :

```bash
getenforce
```

Si le résultat est `Enforcing` et que vous servez le tableau de bord depuis `/opt/digna/dashboard`, étiquetez le répertoire pour que le serveur web puisse le lire :

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Remarque"

    Si `semanage` est introuvable, installez-le avec `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Important"

    Un tableau de bord qui renvoie **403 Forbidden** sur un serveur RHEL fraîchement configuré est presque toujours dû à un problème d'étiquetage SELinux plutôt qu'à un problème de permissions de fichiers. Confirmez avec `sudo ausearch -m avc -ts recent`.

---

## Exécution de digna en tant que service systemd {: #running-digna-as-a-systemd-service }

### Pourquoi exécuter digna en tant que service ?

Exécuter le backend digna en tant que service systemd garantit qu'il :

- Démarre automatiquement au démarrage de la machine
- S'exécute en arrière-plan sans terminal ouvert
- Redémarre automatiquement en cas de crash
- Peut être géré via `systemctl`, le gestionnaire de services standard de Linux

### Fichiers de gestion du service

Tous les fichiers nécessaires se trouvent dans le répertoire d'installation digna sous : `bin/`

Les scripts shell suivants sont disponibles :

- `install_service.sh` — Enregistre digna auprès de systemd
- `uninstall_service.sh` — Désenregistre le service
- `start_service.sh` — Démarre le service enregistré
- `stop_service.sh` — Arrête le service en cours d'exécution

!!! warning "Privilèges root requis"

    Tous les scripts doivent être exécutés avec `sudo`, car l'enregistrement d'un service qui démarre au démarrage écrit un fichier d'unité dans `/etc/systemd/system`.

### Rendre les scripts exécutables

L'extraction peut ne pas préserver le bit exécutable. Avant la première utilisation :

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Installer le service

1. **Ouvrez un terminal**

2. **Placez-vous dans le dossier bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Exécutez le script d'installation**
   ```bash
   sudo ./install_service.sh
   ```

Le serveur digna est maintenant enregistré auprès de systemd avec le démarrage **automatique** activé. Le service ne démarre pas immédiatement — voir la section suivante pour le démarrer.

### Démarrer et arrêter le service

#### Pour démarrer le service

1. Ouvrez un terminal
2. Placez-vous dans `/opt/digna/bin`
3. Exécutez :
   ```bash
   sudo ./start_service.sh
   ```

#### Pour arrêter le service

1. Ouvrez un terminal
2. Placez-vous dans `/opt/digna/bin`
3. Exécutez :
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Astuce"

    Arrêtez toujours le service avant de mettre à jour les fichiers de l'application.

### Gérer le service avec systemctl

Une fois enregistré, le service peut également être contrôlé avec les commandes systemd standard depuis n'importe quel répertoire :

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Vérifier le service

Pour confirmer que le service est enregistré et en cours d'exécution :

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` signifie que le service démarre au démarrage ; `active` signifie qu'il est en cours d'exécution maintenant.

### Voir les journaux du service

systemd capture tout ce que le backend écrit sur la console. Pour le lire :

```bash
sudo journalctl -u digna -n 100
```

Pour suivre le journal en direct pendant que vous reproduisez un problème :

```bash
sudo journalctl -u digna -f
```

!!! tip "Astuce"

    C'est le moyen le plus rapide pour diagnostiquer un service qui démarre puis s'arrête immédiatement. Une défaillance de connexion au repository ou un fichier `license.toml` manquant y est signalé.

### Déplacer le service vers un nouveau répertoire

Le fichier d'unité stocke le chemin absolu vers l'exécutable, donc déplacer l'installation nécessite de ré-enregistrer le service :

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

Le serveur digna est maintenant désenregistré de systemd.

---

## Mise à niveau vers une nouvelle version {: #upgrading-to-a-new-release }

### Avant de mettre à niveau

**La création d'une sauvegarde du repository digna est OBLIGATOIRE**

Avant de mettre à niveau digna, sauvegardez votre repository (PostgreSQL) pour vous protéger contre la perte de données.
Une sauvegarde vous permet de restaurer en cas de problème inattendu pendant la mise à niveau.

Pour créer une sauvegarde depuis le shell :

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Processus de mise à niveau

#### Étape 1 : Arrêter le service digna

Si digna s'exécute en tant que service systemd, arrêtez-le d'abord :

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Si digna s'exécute au premier plan, appuyez sur `Ctrl + C` dans sa fenêtre de terminal.

#### Étape 2 : Sauvegarder l'installation backend actuelle

Dans votre répertoire d'installation digna :

```bash
cd /opt/digna
sudo mv digna digna_old
```
```bash
sudo mv dashboard dashboard_old
```

#### Étape 3 : Extraire et déployer la nouvelle version

1. Extrayez le nouveau fichier ZIP d'installation digna
2. Copiez le nouvel exécutable `digna` et le dossier `dashboard` vers votre répertoire d'installation
3. Restaurez le bit exécutable et la propriété du compte de service :

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Important"

    Le fichier `config.toml` **n'est jamais** inclus dans le ZIP d'installation. Votre configuration existante reste en sécurité.

### Étape 4 : Restaurer vos fichiers de configuration

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
```

### Étape 5 : Mettre à niveau le schéma du repository

Placez-vous dans votre répertoire d'installation digna et exécutez :

```bash
cd /opt/digna
./digna repo upgrade
```

Cela met à jour le schéma PostgreSQL vers la dernière version tout en préservant toutes les données existantes.

### Étape 6 : Redémarrer les services

Si vous l'exécutez en tant que service systemd :

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Si vous l'exécutez manuellement, redémarrez le serveur :

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Si vous utilisez nginx ou Apache, rechargez le serveur web respectif :

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

Sur la famille RHEL, réappliquez l'étiquetage SELinux si le répertoire `dashboard` a été remplacé :

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Étape 7 : Vérifier la mise à niveau

1. Accédez au tableau de bord digna
2. Vérifiez que l'interface se charge correctement
3. Consultez les journaux du serveur pour détecter des erreurs :

```bash
sudo journalctl -u digna -n 100
```