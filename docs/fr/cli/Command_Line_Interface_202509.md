---
title: Référence CLI digna 2025.09 – Commandes & Exemples | Documentation digna
description: Référence complète pour la CLI digna release 2025.109. Apprenez à gérer les utilisateurs, les repositories et les données avec des commandes telles que add-user, check-config, check-repo-connection, inspect, inspect-async, et plus.
image: /assets/logo_square.png
---

# digna CLI Reference 2025.09
**2025-09-29**

Cette page documente l’ensemble complet des commandes disponibles dans la CLI ***digna*** release **2025.09**, incluant des exemples d’utilisation et les options.

---

## Bases de la CLI

---

### help
L’option `--help` fournit des informations sur les commandes disponibles et leur utilisation. Il existe deux manières principales d’utiliser cette option :

1. **Afficher l’aide générale :**
   
    Utilisez --help immédiatement après le mot-clé ***digna***  
   ```bash
   dignacli --help
   ```

2. **Obtenir l’aide pour une commande spécifique :**  
  
    Pour des informations détaillées sur une commande précise, ajoutez `--help` après cette commande.  
    Par exemple, pour obtenir l’aide de la commande `add-user`, exécutez :
     ```bash
     dignacli add-user --help
     ```

     ### sortie :
      
     - **Description de la commande :** Fournit une description détaillée de ce que fait la commande.  
     - **Syntaxe :** Affiche la syntaxe exacte, incluant les arguments requis et optionnels.  
     - **Options :** Liste les options spécifiques à la commande, avec leurs explications.  
     - **Exemples :** Fournit des exemples d’exécution efficaces de la commande.

### check-config

La commande check-config est un utilitaire de la CLI ***digna*** conçu pour tester la configuration de ***digna***. Cette commande vérifie que les composants de ***digna*** peuvent trouver les éléments de configuration nécessaires dans le fichier config.toml.

#### Options

- `--configpath`, `-cp` : Fichier ou répertoire contenant la configuration. Si omis, ../config.toml sera utilisé.
      
#### Utilisation de la commande
```bash
dignacli check-config
```

Après exécution réussie, la commande affiche une confirmation de complétude de la configuration.  
  
Si la configuration semble incomplète, les éléments de configuration manquants seront listés.

  
### check-repo-connection

La commande check-repo-connection est un utilitaire de la CLI ***digna*** conçu pour tester la connectivité et l’accès à un repository ***digna*** spécifié. Cette commande vérifie que la CLI peut interagir avec le repository.
      
#### Utilisation de la commande
```bash
dignacli check-repo-connection
```

Après exécution réussie, la commande affiche une confirmation de la connexion, ainsi que des détails sur le repository : version du repository, hôte, base de données et schéma.  
  
Si la connexion au repository échoue, vérifiez le fichier config.toml pour les paramètres de configuration corrects.


### version

Pour vérifier la version installée de *dignacli*, utilisez l’option --version.  
  
#### Utilisation de la commande
```bash
dignacli --version
```
  
#### Exemple de sortie
```bash
dignacli version 2025.09
```

### options de journalisation
  
Par défaut, la sortie console des commandes ***digna*** est conçue pour être minimaliste. La plupart des commandes offrent la possibilité de fournir des informations supplémentaires, en utilisant les options suivantes :  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 « verbose » et « debug » définissent le niveau de détail, tandis que l’option « logfile » permet de rediriger la sortie vers un fichier plutôt que vers la console.

## Gestion des utilisateurs

### add-user
  
La commande add-user de la CLI ***digna*** est utilisée pour ajouter un nouvel utilisateur au système ***digna***.
  
#### Utilisation de la commande
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Arguments

- **USER_NAME** : Le nom d’utilisateur du nouvel utilisateur (requis).
- **USER_FULL_NAME** : Le nom complet du nouvel utilisateur (requis).
- **USER_PASSWORD** : Le mot de passe du nouvel utilisateur (requis).

#### Options

- `--is_superuser`, `-su` : Indique que le nouvel utilisateur est un administrateur.
- `--valid_until`, `-vu` : Définit une date d’expiration pour le compte utilisateur au format `YYYY-MM-DD HH:MI:SS`. Si non défini, le compte n’a pas de date d’expiration.

#### Exemple

Pour ajouter un nouvel utilisateur avec le nom d’utilisateur `jdoe`, le nom complet `John Doe`, et le mot de passe `password123` :

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pour ajouter un nouvel utilisateur et définir une date d’expiration du compte :
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
La commande `delete-user` de la CLI ***digna*** est utilisée pour supprimer un utilisateur existant du système ***digna***.
  
#### Utilisation de la commande
```bash
dignacli delete-user USER_NAME
```
  
#### Arguments
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur à supprimer (requis). C’est le seul argument requis par la commande.

#### Exemple
```bash
dignacli delete-user jdoe
```
  
L’exécution de cette commande supprimera l’utilisateur `jdoe` du système ***digna***, révoquera son accès et supprimera ses données et permissions associées du repository.

### modify-user

La commande `modify-user` de la CLI ***digna*** est utilisée pour mettre à jour les informations d’un utilisateur existant dans le système ***digna***.

#### Utilisation de la commande
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Arguments
  
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur à modifier (requis).
- **USER_FULL_NAME** : Le nouveau nom complet de l’utilisateur (requis).
  
#### Options  
  
- `--is_superuser`, `-su` : Définit l’utilisateur comme superutilisateur, lui accordant des privilèges élevés. Ce drapeau n’exige pas de valeur.  
- `--valid_until`, `-vu` : Définit une date d’expiration pour le compte utilisateur au format YYYY-MM-DD HH:MI:SS. Si non fournie, le compte reste valide indéfiniment.  
  
#### Exemple
  
Pour modifier le nom complet de l’utilisateur `jdoe` en « Johnathan Doe » et définir l’utilisateur comme superutilisateur :
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
La commande `modify-user-pwd` de la CLI ***digna*** est utilisée pour changer le mot de passe d’un utilisateur existant dans le système ***digna***.
  
#### Utilisation de la commande
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Arguments
  
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur dont le mot de passe doit être modifié (requis).
- **USER_PWD** : Le nouveau mot de passe de l’utilisateur (requis).
  
#### Exemple
  
Pour changer le mot de passe de l’utilisateur `jdoe` en `newpassword123` :
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

La commande `list-users` de la CLI ***digna*** affiche la liste de tous les utilisateurs enregistrés dans le système ***digna***.

#### Utilisation de la commande

```bash
dignacli list-users
```

L’exécution de cette commande dans la CLI ***digna*** se connectera au repository ***digna*** et listera tous les utilisateurs, montrant leur ID, nom d’utilisateur, nom complet, statut de superutilisateur et les horodatages d’expiration.

## Gestion du repository

### upgrade-repo
  
La commande `upgrade-repo` de la CLI ***digna*** est utilisée pour mettre à niveau ou initialiser le repository ***digna***. Cette commande est essentielle pour appliquer des mises à jour ou configurer l’infrastructure du repository pour la première fois.
  
#### Utilisation de la commande

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s` : Lorsqu’activée, cette option exécute la commande en mode simulation, ce qui affiche les instructions SQL qui seraient exécutées sans les appliquer réellement. Utile pour prévisualiser les changements sans modifier le repository.  

  
#### Exemple
  
Pour mettre à niveau le repository ***digna***, vous pouvez exécuter la commande sans options :
  
```bash
dignacli upgrade-repo
```  
Pour exécuter la mise à niveau en mode simulation (voir les instructions SQL sans les appliquer) :
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Cette commande est cruciale pour maintenir le système ***digna***, en s’assurant que le schéma de la base de données et les autres composants du repository sont à jour avec la dernière version du logiciel.

### encrypt
  
La commande `encrypt` de la CLI ***digna*** est utilisée pour chiffrer un mot de passe.
  
#### Utilisation de la commande
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD** : Le mot de passe à chiffrer (requis).
  
#### Exemple
  
Pour chiffrer un mot de passe, vous devez fournir le mot de passe en argument.   
Par exemple, pour chiffrer le mot de passe `mypassword123`, vous utiliseriez :
```bash
dignacli encrypt mypassword123
```
Cette commande renvoie la version chiffrée du mot de passe fourni, qui peut ensuite être utilisée dans des contextes sécurisés. Si l’argument mot de passe n’est pas fourni, la CLI affichera une erreur indiquant l’argument manquant.

### generate-key
  
La commande `generate-key` est utilisée pour générer une clé Fernet, essentielle pour sécuriser les mots de passe stockés dans le repository ***digna***.
  
#### Utilisation de la commande
```bash
dignacli generate-key
```
  
## Gestion des données

### clean-up

La commande `clean-up` de la CLI ***digna*** est utilisée pour supprimer des profils, des prédictions et les données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande est essentielle pour la gestion du cycle de vie des données, aidant à maintenir un environnement de données organisé et efficace en supprimant les données obsolètes ou non nécessaires.

#### Utilisation de la commande

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet à partir duquel les données doivent être supprimées (requis). L’utilisation du mot-clé all-projects dans cet argument ordonne à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début pour la suppression des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin pour la suppression des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options
  
- `--table-name`, `-tn` : Limite l’opération de nettoyage à une table spécifique dans le projet.
- `--table-filter`, `-tf` : Filtre pour limiter le nettoyage aux tables contenant la sous-chaîne spécifiée dans leur nom.
- `--timing`, `-tm` : Affiche la durée du processus de nettoyage après son achèvement.
- `--help` : Affiche l’aide pour la commande clean-up et quitte.
  
#### Exemple
  
Pour supprimer des données du projet ProjectA entre le 1er janvier 2023 et le 30 juin 2023 :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pour supprimer des données seulement d’une table spécifique nommée `Table1` :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Cette commande aide à gérer le stockage des données et à s’assurer que le repository ne contient que des informations pertinentes.

### remove-orphans
  
La commande `remove-orphans` de la CLI ***digna*** est utilisée pour la maintenance du repository ***digna***.  
Lorsqu’un utilisateur supprime des projets ou des sources de données, les profils et prédictions restent dans le repository. Avec cette commande, ces lignes orphelines seront supprimées du repository.
  
#### Utilisation de la commande
  
```bash
dignacli list-projects
```

### list-projects
  
La commande `list-projects` de la CLI ***digna*** est utilisée pour afficher la liste de tous les projets disponibles dans le système ***digna***.
  
#### Utilisation de la commande
  
```bash
dignacli list-projects
```

Cette commande est particulièrement utile pour les administrateurs et les utilisateurs gérant plusieurs projets, fournissant une vue d’ensemble rapide des projets disponibles dans le repository ***digna***.

### list-ds

La commande `list-ds` de la CLI ***digna*** est utilisée pour afficher la liste de toutes les sources de données disponibles au sein d’un projet spécifié. Cette commande est utile pour comprendre les actifs de données disponibles pour l’analyse et la gestion dans le système ***digna***.

#### Utilisation de la commande
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet pour lequel les sources de données sont listées (requis).
  
#### Exemple
  
Pour lister toutes les sources de données du projet nommé `ProjectA` :
  
```bash
dignacli list-ds ProjectA
```
  
Cette commande fournit aux utilisateurs un aperçu des sources de données disponibles dans un projet, les aidant à naviguer et à gérer plus efficacement le paysage des données.


### inspect

La commande `inspect` de la CLI ***digna*** est utilisée pour créer des profils, des prédictions et des données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande aide à analyser et surveiller les données sur une période définie. Après l’achèvement de l’inspection, la valeur du système de feux tricolores calculée est retournée :  
- 0 : OK  
- 1 : INFO  
- 2 : WARNING

#### Utilation de la commande

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel les données doivent être inspectées (requis). L’utilisation du mot-clé all-projects dans cet argument ordonne à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début pour l’inspection des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin pour l’inspection des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options

- `--table-name`, `-tn` : Limite l’inspection à une table spécifique dans le projet.
- `--table-filter`, `-tf` : Filtre pour n’inspecter que les tables contenant la sous-chaîne spécifiée dans leur nom.
- `--enable_notification`, `-en` : Active l’envoi de notifications en cas d’alertes.
- `--bypass-backend`, `-bb` : Contourne le backend et exécute l’inspection directement depuis la CLI (à utiliser uniquement à des fins de test !).

  
#### Exemple
  
Pour inspecter les données du projet `ProjectA` du 1er janvier 2024 au 31 janvier 2024 :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pour n’inspecter qu’une table spécifique et forcer le recalcul des prédictions :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Cette commande est utile pour générer des profils et prédictions mis à jour, surveiller l’intégrité des données et gérer les systèmes d’alerte sur une période de projet spécifiée.

### inspect-async

La commande `inspect-async` de la CLI ***digna*** est utilisée pour créer des profils, des prédictions et des données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande aide à analyser et surveiller les données sur une période définie. Contrairement à la commande `inspect`, celle-ci n’attend pas l’achèvement de l’inspection.
Elle retourne plutôt l’identifiant de requête pour la demande d’inspection soumise. Pour interroger l’avancement du processus d’inspection, utilisez la commande `inspect-status`.

#### Utilisation de la commande

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel les données doivent être inspectées (requis). L’utilisation du mot-clé all-projects dans cet argument ordonne à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début pour l’inspection des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin pour l’inspection des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options

- `--table-name`, `-tn` : Limite l’inspection à une table spécifique dans le projet.
- `--table-filter`, `-tf` : Filtre pour n’inspecter que les tables contenant la sous-chaîne spécifiée dans leur nom.
- `--enable_notification`, `-en` : Active l’envoi de notifications en cas d’alertes.

  
#### Exemple
  
Pour inspecter les données du projet `ProjectA` du 1er janvier 2024 au 31 janvier 2024 :
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

La commande `inspect-status` de la CLI ***digna*** est utilisée pour vérifier l’avancement d’une inspection asynchrone à partir de l’identifiant de requête.

#### Utilisation de la commande

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Arguments
  
- **REQUEST_ID** : L’identifiant de requête renvoyé par la commande `inspect-async`. 
  
#### Exemple
  
Pour vérifier l’avancement d’une inspection avec l’identifiant de requête 12345 :
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

La commande `inspect-cancel` de la CLI ***digna*** est utilisée pour annuler des inspections en se basant sur l’identifiant de requête ou peut être utilisée pour annuler toutes les requêtes en cours.

#### Utilisation de la commande

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Arguments
  
- **REQUEST_ID** : L’identifiant de requête renvoyé par la commande `inspect-async`. 
  
#### Exemple
  
Pour annuler l’inspection avec l’identifiant de requête 12345 :
  
```bash
dignacli inspect-cancel 12345
```

Pour annuler toutes les requêtes actuellement en cours ou en attente :
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

La commande `export-ds` de la CLI ***digna*** est utilisée pour créer une exportation des sources de données depuis le repository ***digna***. Par défaut, toutes les sources de données d’un projet donné seront exportées.

#### Utilisation de la commande
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet depuis lequel les sources de données seront exportées.

#### Options

- `--table_name`, `-tn` : Exporter une source de données particulière d’un projet.
- `--exportfile`, `-ef` : Spécifier le nom de fichier pour l’export.
    
#### Exemple
  
Pour exporter toutes les sources de données du projet nommé `ProjectA` :
  
```bash
dignacli export-ds ProjectA
```
  
Cette commande exporte toutes les sources de données de `ProjectA` sous la forme d’un document JSON pouvant être importé dans un autre projet ou repository ***digna***.


### import-ds

La commande `import-ds` de la CLI ***digna*** est utilisée pour importer des sources de données dans un projet cible et créer un rapport d’importation.

#### Utilisation de la commande
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet dans lequel les sources de données seront importées.
- **EXPORT_FILE** : Le nom de fichier de l’export des sources de données à importer.

#### Options

- `--output-file`, `-o` : Fichier pour sauvegarder le rapport d’importation (si non spécifié, affiche dans le terminal sous forme tabulaire).
- `--output-format`, `-f` : Format pour sauvegarder le rapport d’importation (json, csv).
    
#### Exemple
  
Pour importer toutes les sources de données du fichier d’export `my_export.json` dans `ProjectB` :
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Après l’importation, cette commande affichera également un rapport des objets importés et ignorés. Seules les nouvelles sources de données seront importées dans `ProjectB`. Pour savoir quels objets seraient importés et ignorés, vous pouvez utiliser la commande `plan-import-ds`.

### plan-import-ds

La commande `plan-import-ds` de la CLI ***digna*** est utilisée pour analyser un fichier d’export avant import et créer un rapport préliminaire d’importation.

#### Utilisation de la commande
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet dans lequel les sources de données seraient importées.
- **EXPORT_FILE** : Le nom de fichier de l’export des sources de données à analyser avant l’import.

#### Options

- `--output-file`, `-o` : Fichier pour sauvegarder le rapport d’importation (si non spécifié, affiche dans le terminal sous forme tabulaire).
- `--output-format`, `-f` : Format pour sauvegarder le rapport d’importation (json, csv).
    
#### Exemple
  
Pour vérifier quelles sources de données seraient importées et lesquelles seraient ignorées depuis le fichier d’export `my_export.json` lors d’un import dans `ProjectB` :
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Cette commande affichera uniquement un plan d’importation des objets à importer et à ignorer.