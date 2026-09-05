# digna CLI Reference 2025.04
**2025-04-01**

Cette page documente l’ensemble des commandes disponibles dans le CLI ***digna***, version **2025.04**, incluant des exemples d’utilisation et les options.

---

## Notions de base du CLI

---

## Utilisation de l’option `help`

L’option `--help` fournit des informations sur les commandes disponibles et leur utilisation. Il existe deux principales façons d’utiliser cette option :

1. **Afficher l’aide générale :**
   
    Utilisez --help immédiatement après le mot-clé ***dignacli***
   ```bash
   dignacli --help
   ```

2. **Obtenir l’aide pour une commande spécifique :**  
  
    Pour des informations détaillées sur une commande précise, ajoutez `--help` à cette commande.
    Par exemple, pour obtenir l’aide sur la commande `add-user`, exécutez :
     ```bash
     dignacli add-user --help
     ```

     ### sortie :
      
     - **Description de la commande :** Donne une description détaillée de ce que fait la commande.  
     - **Syntaxe :** Montre la syntaxe exacte, incluant les arguments requis et optionnels.  
     - **Options :** Liste les options spécifiques à la commande, avec leurs explications.  
     - **Exemples :** Fournit des exemples d’exécution efficace de la commande.

  
## Utilisation de la commande `check-repo-connection`

La commande check-repo-connection est un utilitaire du CLI ***digna*** conçu pour tester la connectivité et l’accès à un dépôt ***digna*** spécifié. Cette commande vérifie que le CLI peut interagir avec le dépôt.
      
#### Utilisation de la commande
```bash
dignacli check-repo-connection
```

Après exécution réussie, la commande affiche une confirmation de la connexion, ainsi que des détails sur le dépôt : version du dépôt, hôte, base de données et schéma.  
  
Si la connexion au dépôt échoue, vérifiez le fichier config.toml pour vous assurer que les paramètres de configuration sont corrects.

## Utilisation de la commande ‘version’

Pour vérifier la version installée de *dignacli*, utilisez l’option --version.  
  
#### Utilisation de la commande
```bash
dignacli --version
```
  
#### Exemple de sortie
```bash
dignacli version 2025.04
```

## Utilisation des options de journalisation
  
Par défaut, la sortie console des commandes ***digna*** est minimaliste. La plupart des commandes offrent la possibilité d’afficher des informations supplémentaires en utilisant les options suivantes :  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 « verbose » et « debug » définissent le niveau de détail, tandis que l’option « logfile » permet de rediriger la sortie vers un fichier plutôt que vers la console.

## Gestion des utilisateurs

### Utilisation de la commande ‘add-user’
  
La commande add-user du CLI ***digna*** sert à ajouter un nouvel utilisateur au système ***digna***.
  
#### Utilisation de la commande
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Arguments

- **USER_NAME** : Le nom d’utilisateur du nouvel utilisateur (requis).
- **USER_FULL_NAME** : Le nom complet du nouvel utilisateur (requis).
- **USER_PASSWORD** : Le mot de passe du nouvel utilisateur (requis).

#### Options

- `--is_superuser`, `-su` : Indique que le nouvel utilisateur est administrateur.
- `--valid_until`, `-vu` : Définit une date d’expiration pour le compte utilisateur au format `YYYY-MM-DD HH:MI:SS`. Si non défini, le compte n’a pas de date d’expiration.

#### Exemple

Pour ajouter un nouvel utilisateur avec le nom d’utilisateur `jdoe`, nom complet `John Doe` et mot de passe `password123` :

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pour ajouter un nouvel utilisateur et définir une date d’expiration du compte :
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Utilisation de la commande `delete-user`
  
La commande `delete-user` du CLI ***digna*** sert à supprimer un utilisateur existant du système ***digna***.
  
#### Utilisation de la commande
```bash
dignacli delete-user USER_NAME
```
  
##### Arguments
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur à supprimer (requis). C’est le seul argument requis par la commande.

#### Exemple
```bash
dignacli delete-user jdoe
```
  
L’exécution de cette commande supprimera l’utilisateur `jdoe` du système ***digna***, révoquant son accès et supprimant ses données et permissions associées dans le dépôt.

### Utilisation de la commande `modify-user`

La commande `modify-user` du CLI ***digna*** sert à mettre à jour les informations d’un utilisateur existant dans le système ***digna***.

#### Utilisation de la commande
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Arguments
  
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur à modifier (requis).
- **USER_FULL_NAME** : Le nouveau nom complet de l’utilisateur (requis).
  
#### Options  
  
- `--is_superuser`, `-su` : Définit l’utilisateur comme superutilisateur, accordant des privilèges élevés. Ce flag ne requiert pas de valeur.  
- `--valid_until`, `-vu` : Définit une date d’expiration pour le compte utilisateur au format YYYY-MM-DD HH:MI:SS. Si non fourni, le compte reste valide indéfiniment.  
  
#### Exemple
  
Pour modifier le nom complet de l’utilisateur `jdoe` en « Johnathan Doe » et définir l’utilisateur comme superutilisateur :
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Utilisation de la commande `modify-user-pwd`
  
La commande `modify-user-pwd` du CLI ***digna*** sert à changer le mot de passe d’un utilisateur existant dans le système ***digna***.
  
#### Utilisation de la commande
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Arguments
  
- **USER_NAME** : Le nom d’utilisateur dont le mot de passe doit être modifié (requis).
- **USER_PWD** : Le nouveau mot de passe de l’utilisateur (requis).
  
#### Exemple
  
Pour changer le mot de passe de l’utilisateur `jdoe` en `newpassword123` :
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Utilisation de la commande `list-users`

La commande `list-users` du CLI ***digna*** affiche la liste de tous les utilisateurs enregistrés dans le système ***digna***.

#### Utilisation de la commande

```bash
dignacli list-users
```

L’exécution de cette commande dans le CLI ***digna*** se connectera au dépôt ***digna*** et listera tous les utilisateurs, affichant leur ID, nom d’utilisateur, nom complet, statut de superutilisateur et timestamps d’expiration.

## Gestion du dépôt

### Utilisation de la commande `upgrade-repo`
  
La commande `upgrade-repo` du CLI ***digna*** sert à mettre à niveau ou initialiser le dépôt ***digna***. Cette commande est essentielle pour appliquer des mises à jour ou configurer l’infrastructure du dépôt pour la première fois.
  
#### Utilisation de la commande

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s` : Lorsqu’elle est activée, cette option exécute la commande en mode simulation, affichant les instructions SQL qui seraient exécutées sans les appliquer réellement. Utile pour prévisualiser les changements sans modifier le dépôt.  

  
#### Exemple
  
Pour mettre à niveau le dépôt ***digna***, vous pouvez exécuter la commande sans options :
  
```bash
dignacli upgrade-repo
```  
Pour exécuter la mise à niveau en mode simulation (voir les instructions SQL sans les appliquer) :
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Cette commande est cruciale pour maintenir le système ***digna***, en s’assurant que le schéma de la base de données et les autres composants du dépôt sont à jour avec la dernière version du logiciel.

### Utilisation de la commande `encrypt`
  
La commande `encrypt` du CLI ***digna*** sert à chiffrer un mot de passe.
  
#### Utilisation de la commande
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD** : Le mot de passe à chiffrer (requis).
  
#### Exemple
  
Pour chiffrer un mot de passe, fournissez le mot de passe en argument.   
Par exemple, pour chiffrer le mot de passe `mypassword123`, utilisez :
```bash
dignacli encrypt mypassword123
```
Cette commande affiche la version chiffrée du mot de passe fourni, qui peut ensuite être utilisée dans des contextes sécurisés. Si l’argument mot de passe n’est pas fourni, le CLI affichera une erreur indiquant l’argument manquant.

## Utilisation de la commande `generate-key`
  
La commande `generate-key` est utilisée pour générer une clé Fernet, essentielle pour sécuriser les mots de passe stockés dans le dépôt ***digna***.
  
#### Utilisation de la commande
```bash
dignacli generate-key
```
  
## Gestion des données

## Utilisation de la commande `clean-up`

La commande `clean-up` du CLI ***digna*** sert à supprimer les profils, prédictions et données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande est essentielle pour la gestion du cycle de vie des données, aidant à maintenir un environnement de données organisé et efficace en supprimant les données obsolètes ou inutiles.

#### Utilisation de la commande

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet depuis lequel les données doivent être supprimées (requis). L’utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début pour la suppression des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin pour la suppression des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options
  
- `--table-name`, `-tn` : Limite l’opération de nettoyage à une table spécifique du projet.
- `--table-filter`, `-tf` : Filtre pour limiter le nettoyage aux tables contenant la sous-chaîne spécifiée dans leur nom.
- `--timing`, `-tm` : Affiche la durée du processus de nettoyage après son exécution.
- `--help` : Affiche l’aide pour la commande clean-up et quitte.
  
#### Exemple
  
Pour supprimer les données du projet ProjectA entre le 1er janvier 2023 et le 30 juin 2023 :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pour supprimer les données d’une table spécifique nommée `Table1` uniquement :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Cette commande aide à gérer le stockage des données et à garantir que le dépôt ne contient que les informations pertinentes.

## Utilisation de la commande `list-projects`
  
La commande `list-projects` du CLI ***digna*** sert à afficher la liste de tous les projets disponibles dans le système ***digna***.
  
#### Utilisation de la commande
  
```bash
dignacli list-projects
```

Cette commande est particulièrement utile pour les administrateurs et utilisateurs gérant plusieurs projets, fournissant un aperçu rapide des projets disponibles dans le dépôt ***digna***.

## Utilisation de la commande `list-ds`

La commande `list-ds` du CLI ***digna*** sert à afficher la liste de toutes les sources de données disponibles au sein d’un projet spécifié. Cette commande est utile pour comprendre les actifs de données disponibles pour l’analyse et la gestion dans le système ***digna***.

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
  
Cette commande offre aux utilisateurs une vue d’ensemble des sources de données disponibles dans un projet, les aidant à naviguer et gérer plus efficacement le paysage des données.


## Utilisation de la commande `inspect`

La commande `inspect` du CLI ***digna*** sert à créer des profils, des prédictions et des données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande aide à analyser et surveiller les données sur une période définie.

#### Utilisation de la commande

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet à inspecter (requis). L’utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début de l’inspection des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin de l’inspection des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options

- `--table-name`, `-tn` : Limite l’inspection à une table spécifique du projet.
- `--table-filter`, `-tf` : Filtre pour n’inspecter que les tables contenant la sous-chaîne spécifiée dans leur nom.
- `--do-profile` : Déclenche la recollection des profils. Par défaut : do-profile.
- `--no-do-profile` : Empêche la recollection des profils.
- `--do-prediction` : Déclenche le recalcul des prédictions. Par défaut : do-prediction.
- `--no-do-prediction` : Empêche le recalcul des prédictions.
- `--do-alert-status` : Déclenche le recalcul des statuts d’alerte. Par défaut : do-alert-status.
- `--no-do-alert-status` : Empêche le recalcul des statuts d’alerte.
- `--iterative` : Déclenche l’inspection de la période en itérations quotidiennes. Par défaut : iterative.
- `--no-iterative` : Effectue l’inspection de l’ensemble de la période en une seule exécution.
- `--enable_notification`, `-en` : Active l’envoi de notifications en cas d’alerte.
- `--timing`, `-tm` : Affiche la durée du processus d’inspection après exécution.
  
#### Exemple
  
Pour inspecter les données du projet `ProjectA` du 1er janvier 2024 au 31 janvier 2024 :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pour n’inspecter qu’une table spécifique et forcer le recalcul des prédictions :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Cette commande est utile pour générer des profils et prédictions à jour, surveiller l’intégrité des données et gérer les systèmes d’alerte sur une période donnée dans un projet.

## Utilisation de la commande `tls-status`

La commande `tls-status` du CLI ***digna*** sert à interroger le statut du Traffic Light System (TLS) pour une table spécifique au sein d’un projet à une date donnée. Le Traffic Light System fournit des informations sur la santé et la qualité des données, indiquant les éventuels problèmes ou alertes nécessitant une attention.
  
#### Utilisation de la commande
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel le statut TLS est demandé (requis).
- **TABLE_NAME** : La table spécifique du projet pour laquelle le statut TLS est nécessaire (requis).
- **DATE** : La date pour laquelle le statut TLS est demandé, généralement au format %Y-%m-%d (requis).
  
#### Exemple
  
Pour vérifier le statut TLS d’une table nommée UserData dans le projet ProjectA le 1er juillet 2024 :

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Cette commande aide les utilisateurs à surveiller et maintenir la qualité des données en fournissant un rapport clair et exploitable basé sur des critères prédéfinis.

## Utilisation de la commande `inspect-async`

La commande `inspect-async` du CLI ***digna*** sert à demander au backend d’exécuter de manière asynchrone l’inspection d’une ou plusieurs sources de données pour un projet donné. Si PROJECT_NAME est défini sur all-projects, l’inspection itérera sur tous les projets disponibles et effectuera l’inspection. Elle renvoie un identifiant de requête utilisable pour suivre l’avancement de l’inspection.

#### Utilisation de la commande

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet à inspecter (requis). L’utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début de l’inspection des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin de l’inspection des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options

- `--table-name`, `-tn` : Limite l’inspection à une table spécifique du projet.
- `--table-filter`, `-tf` : Filtre pour n’inspecter que les tables contenant la sous-chaîne spécifiée dans leur nom.

  
#### Exemple
  
Pour inspecter les données du projet `ProjectA` du 1er janvier 2024 au 31 janvier 2024 :
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Utilisation de la commande `inspect-status`

La commande `inspect-status` du CLI ***digna*** sert à vérifier l’avancement d’une inspection asynchrone à partir de l’identifiant de requête.

#### Utilisation de la commande

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Arguments
  
- **REQUEST_ID** : L’identifiant de requête retourné par la commande `inspect-async` 
  
#### Options

- `--report_level`, `-rl` : Définit le niveau de rapport : 'task' ou 'step' [par défaut : task]
  
#### Exemple
  
Pour vérifier l’avancement d’une inspection avec l’identifiant de requête 12345 au niveau détaillé des étapes :
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Utilisation de la commande `export-ds`

La commande `export-ds` du CLI ***digna*** sert à créer une exportation des sources de données depuis le dépôt ***digna***. Par défaut, toutes les sources de données d’un projet donné seront exportées.

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
  
Cette commande exporte toutes les sources de données de `ProjectA` sous forme de document JSON pouvant être importé dans un autre projet ou dépôt ***digna***.


## Utilisation de la commande `import-ds`

La commande `import-ds` du CLI ***digna*** sert à importer des sources de données dans un projet cible et à générer un rapport d’importation.

#### Utilisation de la commande
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet dans lequel les sources de données seront importées.
- **EXPORT_FILE** : Le nom de fichier de l’export des sources de données à importer.

#### Options

- `--output-file`, `-o` : Fichier pour sauvegarder le rapport d’import (si non spécifié, affiche dans le terminal sous forme tabulaire).
- `--output-format`, `-f` : Format pour sauvegarder le rapport d’import (json, csv).
    
#### Exemple
  
Pour importer toutes les sources de données depuis le fichier d’export `my_export.json` dans `ProjectB` :
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Après l’import, cette commande affichera également un rapport des objets importés et ignorés. Seules les nouvelles sources de données seront importées dans `ProjectB`. Pour savoir quels objets seraient importés et ignorés, vous pouvez utiliser la commande `plan-import-ds`.

## Utilisation de la commande `plan-import-ds`

La commande `plan-import-ds` du CLI ***digna*** sert à analyser un export de sources de données et à produire un plan d’importation (objets qui seraient importés et ceux qui seraient ignorés).

#### Utilisation de la commande
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME** : Le nom du projet dans lequel les sources de données seraient importées.
- **EXPORT_FILE** : Le nom de fichier de l’export des sources de données à analyser avant l’import.

#### Options

- `--output-file`, `-o` : Fichier pour sauvegarder le rapport d’import (si non spécifié, affiche dans le terminal sous forme tabulaire).
- `--output-format`, `-f` : Format pour sauvegarder le rapport d’import (json, csv).
    
#### Exemple
  
Pour vérifier quelles sources de données seraient importées et lesquelles seraient ignorées depuis le fichier d’export `my_export.json` lors d’un import dans `ProjectB` :
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
Cette commande affichera uniquement un plan d’importation des objets à importer et à ignorer.