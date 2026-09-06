---
title: Référence CLI digna 2026.06 – Commandes et exemples | Documentation digna
description: Référence complète de la version 2026.06 du CLI digna
image: /assets/logo_square.png
---

# Référence CLI digna 2026.06
**2026-09-05**

Cette page documente l'ensemble complet des commandes disponibles dans la version **2026.06** du CLI ***digna***, avec des exemples d'utilisation et les options.

L'exécutable s'appelle `digna`.

---

## Notions de base du CLI

---

### Aperçu et syntaxe

Le CLI de la version **2026.06** utilise une hiérarchie de commandes structurée, organisée par catégories :

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` et `serve` sont des commandes uniques, sans sous-commande :

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Options globales

Les options globales suivantes s'appliquent à toutes les commandes :

- `--help`, `-h` : Affiche l'aide pour le CLI ou pour une catégorie de commandes ou une sous-commande précise.
- `--stacktrace` : Affiche la chaîne d'erreurs complète en cas d'échec, au lieu du seul message de premier niveau.

`--stacktrace` est une option globale au sens strict : elle doit être indiquée **avant** la catégorie de commandes, et non après.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Il n'existe pas d'indicateur `--version`. Utilisez la commande [`version`](#version) à la place.

### Prérequis

La plupart des commandes ont besoin d'un fichier `config.toml` lisible et valide ; certaines exigent en plus une licence valide.
Le tableau suivant récapitule ce que chaque catégorie de commandes charge avant toute autre action :

| Catégorie de commandes | Nécessite `config.toml` | Nécessite une licence valide |
|---|---|---|
| `version` | non | non |
| `config check` | non (c'est précisément ce sur quoi la commande fait rapport) | non |
| `license check` | non | c'*est* la vérification |
| `crypt` | oui | non |
| `serve` | oui | non |
| `project` | oui | non |
| `user` | oui | oui |
| `inspection` | oui | oui |
| `repo` | oui | oui |

Lorsqu'une licence est requise, sa signature et sa date d'expiration sont toutes deux vérifiées, et la commande s'interrompt avant de toucher au référentiel si l'une des deux échoue.

### Codes de sortie

- `0` : la commande a réussi.
- `1` : la commande a échoué. Le message d'erreur est écrit sur stderr, précédé du préfixe `Error: `.

### help

L'option `--help` fournit des informations sur les catégories de commandes, les sous-commandes et les options disponibles :

1. **Afficher l'aide générale :**
   ```bash
   digna --help
   ```

2. **Obtenir l'aide de catégories et de commandes précises :**
   ```bash
   digna user --help
   digna user add --help
   ```

   **La sortie comprend :**
   - **Description de la commande :** Résumé de l'objectif de la commande.
   - **Syntaxe :** Arguments obligatoires et facultatifs.
   - **Options :** Indicateurs et paramètres propres à la commande.

### version

La commande `version` affiche la version de ***digna*** installée. Elle ne lit aucune configuration et ne valide aucune licence : elle fonctionne donc aussi sur une installation dont le fichier `config.toml` ou la licence est absent ou invalide.

La version de la release est indépendante de la version du schéma du référentiel indiquée par [`repo check`](#repo-check).

#### Utilisation de la commande
```bash
digna version
```

#### Exemple de sortie
```text
2026.06
```

---

## Gestion de la configuration

---

### config check

La commande `config check` valide le fichier de configuration (`config.toml`) en vérifiant que toutes les sections et tous les paramètres obligatoires sont présents et correctement formatés. Chaque section est validée séparément : une section `[app]` défectueuse ne masque donc pas l'état de `[repo]`.

Les sections faisant l'objet d'un rapport sont :

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — facultatif ; une clé absente réussit la validation, une liste présente mais mal formée échoue

La commande ne charge délibérément pas la configuration de l'application comme le font les autres commandes, afin de pouvoir diagnostiquer un fichier `config.toml` qui empêcherait ***digna*** de démarrer.

#### Utilisation de la commande
```bash
digna config check [OPTIONS]
```

#### Options
- `--configpath`, `-c` : Chemin vers le fichier de configuration ou vers un répertoire contenant `config.toml` (par défaut : `./config.toml`).
- `--json` : Produit le rapport de validation au format JSON. Prioritaire sur `--quiet`.
- `--quiet`, `-q` : Supprime le rapport et s'appuie uniquement sur le code de sortie.

#### Exemple
```bash
digna config check
```

Valider un fichier de configuration précis et formater la sortie en JSON :
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Exemple de sortie
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Un fichier absent ou une erreur de syntaxe TOML ne laisse rien à valider section par section et est signalé comme une erreur unique plutôt que comme un rapport, indépendamment de `--quiet` ou `--json`.

---

## Gestion du référentiel

---

### repo check

La commande `repo check` teste la connexion à la base de données et vérifie l'installation et la version du référentiel. Elle échoue si le schéma configuré n'existe pas, ou s'il existe mais ne contient aucun référentiel ***digna***.

La version indiquée est celle du schéma du référentiel, versionné séparément de la release ***digna*** affichée par [`version`](#version).

#### Utilisation de la commande
```bash
digna repo check
```

#### Exemple de sortie
```text
Repo version 3.0.0 installed
```

### repo install

La commande `repo install` installe un nouveau référentiel ***digna*** dans le schéma configuré dans `config.toml`, en créant toutes les séquences, tables, index, contraintes et enregistrements initiaux nécessaires.

Le schéma lui-même n'est **pas** créé par cette commande — il doit exister au préalable. La commande refuse également de s'exécuter si un référentiel est déjà installé dans ce schéma, et renvoie vers [`repo upgrade`](#repo-upgrade) si la version installée est plus ancienne.

#### Utilisation de la commande
```bash
digna repo install
```

#### Exemple de sortie
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

La commande `repo upgrade` applique les migrations du schéma de base de données afin d'amener un référentiel existant à la version attendue par la release installée. Les mises à niveau sont appliquées une version à la fois, le long d'un chemin de mise à niveau fixe, et chaque étape achevée est enregistrée dans le référentiel.

Si le référentiel est déjà à la version attendue, la commande indique qu'aucune mise à niveau n'est nécessaire et n'effectue aucune modification.

#### Utilisation de la commande
```bash
digna repo upgrade
```

#### Exemple de sortie
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Gestion du chiffrement

---

### crypt gen-key

La commande `crypt gen-key` génère une nouvelle clé de chiffrement AES-GCM, destinée à servir de clé de chiffrement dans `config.toml`. Un fichier `config.toml` chargeable doit déjà être présent, même si la clé générée n'en dépend pas.

#### Utilisation de la commande
```bash
digna crypt gen-key
```

#### Exemple de sortie
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

La commande `crypt encrypt` chiffre une chaîne de caractères (par exemple un mot de passe de base de données) à l'aide de la clé AES-GCM configurée dans `config.toml`, puis affiche le texte chiffré.

#### Utilisation de la commande
```bash
digna crypt encrypt <VALUE>
```

#### Arguments
- **VALUE** : La chaîne en clair à chiffrer (obligatoire).

#### Exemple
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

La commande `crypt decrypt` déchiffre une chaîne chiffrée en AES-GCM à l'aide de la clé configurée dans `config.toml`, puis affiche le texte en clair.

#### Utilisation de la commande
```bash
digna crypt decrypt <VALUE>
```

#### Arguments
- **VALUE** : La chaîne chiffrée à déchiffrer (obligatoire).

#### Exemple
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Gestion des utilisateurs

---

### user add

La commande `user add` crée un nouveau compte utilisateur dans le référentiel ***digna***. La commande échoue si un utilisateur portant l'adresse e-mail indiquée existe déjà.

#### Utilisation de la commande
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Arguments
- **EMAIL** : L'adresse e-mail de l'utilisateur (obligatoire).
- **PASSWORD** : Le mot de passe initial de l'utilisateur (obligatoire).
- **DISPLAY_NAME** : Le nom d'affichage complet de l'utilisateur (obligatoire).

#### Options
- `--admin`, `-a` : Crée l'utilisateur avec les privilèges d'administrateur (superutilisateur).

#### Exemple
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Pour créer un compte administrateur :
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Exemple de sortie
```text
User created with ID: 42
```

### user list

La commande `user list` répertorie tous les utilisateurs enregistrés sous forme de tableau, avec l'ID, l'adresse e-mail, le nom d'affichage et l'indicateur d'administrateur.

#### Utilisation de la commande
```bash
digna user list
```

#### Exemple de sortie
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

La commande `user modify` met à jour le nom d'affichage et les privilèges d'administrateur d'un compte utilisateur existant, identifié par son adresse e-mail.

Le nom d'affichage et l'indicateur d'administrateur sont toujours écrits tous les deux. `--admin` est un commutateur, pas une valeur : **l'omettre révoque les privilèges d'administrateur**, indiquez-le donc chaque fois que l'utilisateur doit les conserver ou les obtenir.

#### Utilisation de la commande
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Arguments
- **EMAIL** : L'adresse e-mail de l'utilisateur à modifier (obligatoire).
- **DISPLAY_NAME** : Le nom d'affichage mis à jour (obligatoire).

#### Options
- `--admin`, `-a` : Accorde les privilèges d'administrateur. À omettre pour les révoquer.
- `--valid-until`, `-v` : Accepté pour compatibilité, mais **actuellement sans effet**. Son utilisation affiche un avertissement et ne change rien.

#### Exemple
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Exemple de sortie
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

La commande `user modify-pwd` met à jour le mot de passe d'un compte utilisateur existant.

#### Utilisation de la commande
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Arguments
- **EMAIL** : L'adresse e-mail de l'utilisateur dont le mot de passe doit être mis à jour (obligatoire).
- **PASSWORD** : Le nouveau mot de passe (obligatoire).

#### Exemple
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

La commande `user delete` supprime un compte utilisateur du système.

#### Utilisation de la commande
```bash
digna user delete <EMAIL>
```

#### Arguments
- **EMAIL** : L'adresse e-mail de l'utilisateur à supprimer (obligatoire).

#### Exemple
```bash
digna user delete jdoe@example.com
```

---

## Gestion des projets et des sources de données

---

### project list

La commande `project list` répertorie tous les projets disponibles dans le référentiel, en indiquant leur ID, leur nom et leur description.

#### Utilisation de la commande
```bash
digna project list
```

#### Exemple de sortie
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

La commande `project list-ds` répertorie toutes les sources de données associées à un projet donné, en affichant leur ID, leur nom, leur type, leur schéma et leur nom de table.

#### Utilisation de la commande
```bash
digna project list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet dont les sources de données doivent être répertoriées (obligatoire). Le nom doit correspondre exactement.

#### Exemple
```bash
digna project list-ds ProjectA
```

#### Exemple de sortie
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

La commande `project export-ds` exporte les sources de données d'un projet dans un document JSON.

Si ni `--table-name` ni `--table-id` n'est indiqué, toutes les sources de données du projet sont exportées.

#### Utilisation de la commande
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet depuis lequel exporter les sources de données (obligatoire).

#### Options
- `--table-name`, `-n` : Noms des sources de données à exporter. Plusieurs noms peuvent être indiqués, séparés par des espaces.
- `--table-id`, `-i` : ID des sources de données à exporter. Plusieurs ID peuvent être indiqués, séparés par des espaces.
- `--exportfile`, `-f` : Chemin d'enregistrement des sources de données exportées (par défaut : `data_sources_export.json`).

#### Exemple
Pour exporter toutes les sources de données de `ProjectA` :
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Pour exporter des tables précises :
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Exemple de sortie
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

La commande `project import-ds` importe des sources de données depuis un fichier d'export vers un projet cible et indique, objet par objet, ce qui a été créé, mis à jour ou ignoré.

#### Utilisation de la commande
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME** : Nom du projet cible dans lequel importer (obligatoire).
- **EXPORT_FILE** : Chemin du fichier d'export JSON (obligatoire).

#### Options
- `--output-file`, `-o` : Fichier dans lequel écrire le rapport d'import. Sans cette option, le rapport est envoyé sur stdout.
- `--output-format`, `-f` : Format du rapport d'import — `table`, `json` ou `csv` (par défaut : `table`).

#### Exemple
```bash
digna project import-ds ProjectB my_export.json
```

Pour obtenir un rapport exploitable par une machine :
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Le rapport couvre quatre niveaux d'objets — source de données, définition de jeu de données, attribut et règle de validation — chacun avec son action d'import, son résultat, l'ID de l'objet obtenu et toute information complémentaire.

### project plan-import-ds

La commande `project plan-import-ds` prévisualise l'import de sources de données vers un projet cible, en montrant quels objets seraient créés, mis à jour ou ignorés, sans rien modifier. Elle accepte le même fichier d'export et les mêmes options de rapport que [`project import-ds`](#project-import-ds), et ajoute un numéro d'étape par objet planifié.

#### Utilisation de la commande
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME** : Nom du projet cible (obligatoire).
- **EXPORT_FILE** : Chemin du fichier d'export (obligatoire).

#### Options
- `--output-file`, `-o` : Fichier dans lequel écrire le plan d'import. Sans cette option, le plan est envoyé sur stdout.
- `--output-format`, `-f` : Format du plan d'import — `table`, `json` ou `csv` (par défaut : `table`).

#### Exemple
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Gestion des inspections

---

### inspection run

La commande `inspection run` crée une demande d'inspection pour un projet et une plage de dates, puis — selon les options indiquées — attend son achèvement, rend la main immédiatement, ou l'exécute dans son propre processus.

Les trois modes d'exécution sont les suivants :

- **Par défaut (aucun indicateur)** : la demande est mise en file d'attente pour le backend, et le CLI l'interroge toutes les deux secondes en affichant la progression des tâches jusqu'à ce que l'inspection atteigne un état final. Un `digna serve` en cours d'exécution est nécessaire, faute de quoi personne ne prend la demande en charge.
- **`--async-mode`** : la demande est mise en file d'attente et son ID est affiché immédiatement. Utilisez [`inspection status`](#inspection-status) pour la suivre.
- **`--bypass-backend`** : l'inspection est exécutée par le processus du CLI lui-même et n'est pas mise en file d'attente ; aucun serveur en cours d'exécution n'est donc nécessaire.

`--async-mode` et `--bypass-backend` sont mutuellement exclusifs.

Dans tous les modes, la commande se termine par un code de sortie non nul si l'inspection ne s'est pas achevée correctement.

#### Utilisation de la commande
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet cible (obligatoire). Le nom doit correspondre exactement.
- **START_DATE** : Date de début de la plage, au format `YYYY-MM-DD` (obligatoire).
- **END_DATE** : Date de fin de la plage, au format `YYYY-MM-DD` (obligatoire).

#### Options
- `--table-name` : Restreint l'inspection à une seule source de données du projet, désignée par son nom. Sans cette option, toutes les sources de données du projet sont inspectées.
- `--async-mode` : Met l'inspection en file d'attente et affiche l'ID de la demande au lieu d'en attendre l'achèvement. Ne peut pas être combiné avec `--bypass-backend`.
- `--bypass-backend` : Exécute l'inspection directement dans le processus du CLI au lieu de la mettre en file d'attente pour le backend. Ne peut pas être combiné avec `--async-mode`.

#### Exemple
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Pour soumettre une inspection asynchrone :
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Pour inspecter une seule source de données :
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Exemple de sortie
Mode par défaut :
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Mode asynchrone :
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

La commande `inspection status` interroge l'état et la progression des tâches d'une demande d'inspection à partir de son ID de demande.

#### Utilisation de la commande
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Arguments
- **INSPECTION_REQUEST_ID** : L'ID numérique de la demande d'inspection (obligatoire).

#### Exemple
```bash
digna inspection status 1024
```

#### Exemple de sortie
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

La commande `inspection abort` demande l'annulation des demandes d'inspection en cours ou en attente. Elle enregistre un événement d'arrêt pour chaque demande concernée ; c'est le backend qui agit ensuite, un abandon est donc une demande d'arrêt et non une interruption immédiate.

#### Utilisation de la commande
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Arguments
- **INSPECTION_REQUEST_ID** : L'ID de la demande d'inspection à abandonner. Obligatoire sauf si `--killall` est indiqué.

#### Options
- `--killall` : Abandonne toutes les demandes d'inspection en cours et en attente. Prioritaire sur un ID de demande indiqué en parallèle.

#### Exemple
Pour abandonner une demande précise :
```bash
digna inspection abort 1024
```

Pour abandonner toutes les inspections actives et en file d'attente :
```bash
digna inspection abort --killall
```

#### Exemple de sortie
`--killall` indique ce qu'il a fait ; l'abandon d'une demande unique ne produit aucune sortie et signale sa réussite par son code de sortie.
```text
All running and pending inspections have been aborted.
```

---

## Gestion des licences

---

### license check

La commande `license check` valide le fichier `license.toml` en vérifiant sa signature à l'aide de la clé publique livrée avec l'installation et en contrôlant qu'il n'a pas expiré. Elle ne lit aucune configuration d'application et fonctionne donc également avant que `config.toml` ne soit configuré.

#### Utilisation de la commande
```bash
digna license check
```

#### Exemple de sortie
```text
License is valid
```

Une signature invalide et une licence expirée sont signalées comme deux erreurs distinctes, toutes deux avec le code de sortie 1.

---

## Serveur et services en arrière-plan

---

### serve

La commande `serve` lance le serveur d'API REST ***digna***, ainsi que le planificateur d'inspections en arrière-plan et le gestionnaire d'inspections. Au démarrage, elle fait également échouer toute inspection que le référentiel considère encore comme en cours, puisque rien n'a pu survivre à un processus antérieur.

La commande s'exécute au premier plan jusqu'à son arrêt.

#### Utilisation de la commande
```bash
digna serve [OPTIONS]
```

#### Options
- `--address` : Adresse réseau sur laquelle lier le serveur d'API (par défaut : `127.0.0.1`).
- `--port` : Numéro du port d'écoute (par défaut : `8000`).

#### Exemple
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Exemple de sortie
```text
Server running on http://0.0.0.0:8000
```
