# Référence digna CLI 2024.11
**2024-11-03**

Cette page documente l’ensemble des commandes disponibles dans la CLI ***digna*** version **2024.11**, y compris des exemples d’utilisation et les options.


---
## Notions de base de la CLI

---

## Utilisation de l’option `--help`

L’option `--help` fournit des informations sur les commandes disponibles et leur utilisation. Il y a deux façons principales d’utiliser cette option :

1. **Afficher l’aide générale :**
   
    Utilisez `--help` immédiatement après le mot-clé `dignacli`  
   ```bash
   dignacli --help
   ```

3.  **Obtenir de l’aide pour des commandes spécifiques :**  
  
    Pour obtenir des informations détaillées sur une commande spécifique, ajoutez `--help` à cette commande.
    Par exemple, pour obtenir de l’aide sur la commande `add-user`, exécutez :
     ```bash
     dignacli add-user --help
     ```

     ### sortie:
      
     - **Description de la commande :** Offre une description détaillée de ce que fait la commande.  
     - **Syntaxe :** Montre la syntaxe exacte, y compris les arguments requis et optionnels.  
     - **Options :** Liste les options spécifiques à la commande, avec leurs explications.  
     - **Exemples :** Fournit des exemples montrant comment exécuter la commande efficacement.

  
## Utilisation de la commande `check-repo-connection`

La commande `check-repo-connection` est un utilitaire de la CLI ***digna*** conçu pour tester la connectivité et l’accès à un dépôt ***digna*** spécifié. Cette commande vérifie que la CLI peut interagir avec le dépôt.
      
### Utilisation de la commande
```bash
dignacli check-repo-connection
```

Après exécution réussie, la commande affiche une confirmation de la connexion, ainsi que des détails sur le dépôt : version du dépôt, hôte, base de données et schéma.  
  
Si la connexion au dépôt échoue, vérifiez le fichier config.toml pour vous assurer que les paramètres de configuration sont corrects.

## Utilisation de la commande ‘version’

Pour vérifier la version installée de *dignacli*, utilisez l’option `--version`.  
  
### Utilisation de la commande
```bash
dignacli --version
```
  
### Exemple de sortie
```bash
dignacli version 2024.11
```

## Utilisation des options de journalisation
  
Par défaut, la sortie console des commandes ***digna*** est conçue pour être minimaliste. La plupart des commandes offrent la possibilité d’afficher des informations supplémentaires en utilisant les options suivantes :  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 « verbose » et « debug » définissent le niveau de détail, tandis que l’option « logfile » permet de rediriger la sortie vers un fichier au lieu de la fenêtre de la console.

# Gestion des utilisateurs

## Utilisation de la commande ‘add-user’
  
La commande add-user de la CLI ***digna*** est utilisée pour ajouter un nouvel utilisateur au système ***digna***.
  
### Utilisation de la commande
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Arguments

- **USER_NAME** : Le nom d’utilisateur du nouvel utilisateur (requis).
- **USER_FULL_NAME** : Le nom complet du nouvel utilisateur (requis).
- **USER_PASSWORD** : Le mot de passe du nouvel utilisateur (requis).

### Options

- `--is_superuser`, `-su` : Indique que le nouvel utilisateur est administrateur.
- `--valid_until`, `-vu` : Définit une date d’expiration pour le compte utilisateur au format `YYYY-MM-DD HH:MI:SS`. Si non définie, le compte n’a pas de date d’expiration.

### Exemple

Pour ajouter un nouvel utilisateur avec le nom d’utilisateur `jdoe`, le nom complet `John Doe` et le mot de passe `password123` :

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pour ajouter un nouvel utilisateur et définir une date d’expiration du compte :
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Utilisation de la commande `delete-user`
  
La commande `delete-user` de la CLI ***digna*** est utilisée pour supprimer un utilisateur existant du système ***digna***.
  
### Utilisation de la commande
```bash
dignacli delete-user USER_NAME
```
  
### Arguments
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur à supprimer (requis). C’est le seul argument requis par la commande.

### Exemple
```bash
dignacli delete-user jdoe
```
  
L’exécution de cette commande supprimera l’utilisateur `jdoe` du système ***digna***, révoquant son accès et supprimant ses données et permissions associées dans le dépôt.

## Utilisation de la commande `modify-user`

La commande `modify-user` de la CLI ***digna*** permet de mettre à jour les informations d’un utilisateur existant dans le système ***digna***.

### Utilisation de la commande
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Arguments
  
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur à modifier (requis).
- **USER_FULL_NAME** : Le nouveau nom complet pour l’utilisateur (requis).
  
### Options  
  
- `--is_superuser`, `-su` : Définit l’utilisateur comme superutilisateur, accordant des privilèges élevés. Ce flag ne nécessite pas de valeur.  
- `--valid_until`, `-vu` : Définit une date d’expiration pour le compte utilisateur au format YYYY-MM-DD HH:MI:SS. Si non fournie, le compte reste valide indéfiniment.  
  
### Exemple
  
Pour modifier le nom complet de l’utilisateur `jdoe` en « Johnathan Doe » et définir l’utilisateur comme superutilisateur :
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Utilisation de la commande `modify-user-pwd`
  
La commande `modify-user-pwd` de la CLI ***digna*** est utilisée pour changer le mot de passe d’un utilisateur existant dans le système ***digna***.
  
### Utilisation de la commande
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Arguments
  
- **USER_NAME** : Le nom d’utilisateur de l’utilisateur dont le mot de passe doit être modifié (requis).
- **USER_PWD** : Le nouveau mot de passe de l’utilisateur (requis).
  
### Exemple
  
Pour changer le mot de passe de l’utilisateur `jdoe` en `newpassword123` :
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Utilisation de la commande `list-users`

La commande `list-users` de la CLI ***digna*** affiche la liste de tous les utilisateurs enregistrés dans le système ***digna***.

### Utilisation de la commande

```bash
dignacli list-users
```

L’exécution de cette commande dans la CLI ***digna*** se connectera au dépôt ***digna*** et listera tous les utilisateurs, affichant leur ID, nom d’utilisateur, nom complet, statut de superutilisateur et timestamps d’expiration.

# Gestion des dépôts

### Utilisation de la commande `upgrade-repo`
  
La commande `upgrade-repo` de la CLI ***digna*** est utilisée pour mettre à jour ou initialiser le dépôt ***digna***. Cette commande est essentielle pour appliquer des mises à jour ou configurer l’infrastructure du dépôt pour la première fois.
  
### Utilisation de la commande

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s` : En activant cette option, la commande s’exécute en mode simulation, ce qui affiche les instructions SQL qui seraient exécutées sans les appliquer réellement. Utile pour prévisualiser les changements sans modifier le dépôt.  

  
### Exemple
  
Pour mettre à jour le dépôt ***digna***, vous pouvez exécuter la commande sans options :
  
```bash
dignacli upgrade-repo
```  
Pour exécuter la mise à jour en mode simulation (voir les instructions SQL sans les appliquer) :
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Cette commande est cruciale pour la maintenance du système ***digna***, en veillant à ce que le schéma de la base de données et d’autres composants du dépôt soient à jour avec la version la plus récente du logiciel.

## Utilisation de la commande `encrypt`
  
La commande `encrypt` de la CLI ***digna*** est utilisée pour chiffrer un mot de passe.
  
### Utilisation de la commande
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Arguments
- **PASSWORD** : Le mot de passe à chiffrer (requis).
  
### Exemple
  
Pour chiffrer un mot de passe, vous devez fournir le mot de passe en argument.   
Par exemple, pour chiffrer le mot de passe `mypassword123`, vous utiliserez :
```bash
dignacli encrypt mypassword123
```
Cette commande affiche la version chiffrée du mot de passe fourni, qui peut ensuite être utilisée dans des contextes sécurisés. Si l’argument mot de passe n’est pas fourni, la CLI affichera une erreur indiquant l’argument manquant.

## Utilisation de la commande `generate-key`
  
La commande `generate-key` est utilisée pour générer une clé Fernet, essentielle pour sécuriser les mots de passe stockés dans le dépôt ***digna***.
  
### Utilisation de la commande
```bash
dignacli generate-key
```
  
# Gestion des données

## Utilisation de la commande `clean-up`

La commande `clean-up` de la CLI ***digna*** est utilisée pour supprimer des profils, des prédictions et des données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande est essentielle pour la gestion du cycle de vie des données, aidant à maintenir un environnement de données organisé et efficace en supprimant les données obsolètes ou inutiles.

### Utilisation de la commande

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME** : Le nom du projet depuis lequel les données seront supprimées (requis). L’utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début pour la suppression des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin pour la suppression des données, suivant les mêmes formats que FROM_DATE (requis).
  
### Options
  
- `--table-name`, `-tn` : Limite l’opération de nettoyage à une table spécifique du projet.
- `--table-filter`, `-tf` : Filtre pour limiter le nettoyage aux tables dont le nom contient la sous-chaîne spécifiée.
- `--timing`, `-tm` : Affiche la durée du processus de nettoyage après son achèvement.
- `--help` : Affiche l’aide pour la commande clean-up et quitte.
  
### Exemple
  
Pour supprimer des données du projet ProjectA entre le 1er janvier 2023 et le 30 juin 2023 :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pour supprimer des données uniquement d’une table spécifique nommée `Table1` :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Cette commande aide à gérer le stockage des données et à garantir que le dépôt ne contient que des informations pertinentes.

## Utilisation de la commande `inspect`

La commande `inspect` de la CLI ***digna*** est utilisée pour créer des profils, des prédictions et des données du système de feux tricolores pour une ou plusieurs sources de données au sein d’un projet spécifié. Cette commande aide à analyser et surveiller les données sur une période définie.

### Utilisation de la commande

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel les données doivent être inspectées (requis). L’utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d’itérer sur tous les projets existants et d’appliquer cette commande.
- **FROM_DATE** : La date et l’heure de début pour l’inspection des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S, ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l’heure de fin pour l’inspection des données, suivant les mêmes formats que FROM_DATE (requis).
  
### Options

- `--table-name`, `-tn` : Limite l’inspection à une table spécifique du projet.
- `--table-filter`, `-tf` : Filtre pour inspecter uniquement les tables dont le nom contient la sous-chaîne spécifiée.
- `--do-profile` : Déclenche la recollection des profils. La valeur par défaut est do-profile.
- `--no-do-profile` : Empêche la recollection des profils.
- `--do-prediction` : Déclenche le recalcul des prédictions. La valeur par défaut est do-prediction.
- `--no-do-prediction` : Empêche le recalcul des prédictions.
- `--do-alert-status` : Déclenche le recalcul des statuts d’alerte. La valeur par défaut est do-alert-status.
- `--no-do-alert-status` : Empêche le recalcul des statuts d’alerte.
- `--timing`, `-tm` : Affiche la durée du processus d’inspection après son achèvement.
  
### Exemple
  
Pour inspecter les données du projet `ProjectA` du 1er janvier 2024 au 31 janvier 2024 :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pour n’inspecter qu’une table spécifique et forcer le recalcul des prédictions :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Cette commande est utile pour générer des profils et des prédictions à jour, surveiller l’intégrité des données et gérer les systèmes d’alerte dans une période projetée.

## Utilisation de la commande `tls-status`

La commande `tls-status` de la CLI ***digna*** est utilisée pour interroger l’état du Traffic Light System (TLS) pour une table spécifique d’un projet à une date donnée. Le Traffic Light System fournit des informations sur la santé et la qualité des données, indiquant les problèmes ou alertes susceptibles d’exiger une attention.
  
### Utilisation de la commande
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel l’état TLS est interrogé (requis).
- **TABLE_NAME** : La table spécifique du projet pour laquelle l’état TLS est demandé (requis).
- **DATE** : La date pour laquelle l’état TLS est interrogé, généralement au format %Y-%m-%d (requis).
  
### Exemple
  
Pour vérifier l’état TLS d’une table nommée UserData dans le projet ProjectA le 1er juillet 2024 :

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Cette commande aide les utilisateurs à surveiller et maintenir la qualité des données en fournissant un rapport d’état clair et exploitable basé sur des critères prédéfinis.

## Utilisation de la commande `list-projects`
  
La commande `list-projects` de la CLI ***digna*** est utilisée pour afficher la liste de tous les projets disponibles dans le système ***digna***.
  
### Utilisation de la commande
  
```bash
dignacli list-projects
```

Cette commande est particulièrement utile pour les administrateurs et les utilisateurs gérant plusieurs projets, fournissant un aperçu rapide des projets disponibles dans le dépôt ***digna***.

## Utilisation de la commande `list-ds`

La commande `list-ds` de la CLI ***digna*** est utilisée pour afficher la liste de toutes les sources de données disponibles au sein d’un projet spécifié. Cette commande est utile pour comprendre les actifs de données disponibles pour l’analyse et la gestion dans le système ***digna***.

### Utilisation de la commande
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Arguments
- **PROJECT_NAME** : Le nom du projet pour lequel les sources de données sont listées (requis).
  
### Exemple
  
Pour lister toutes les sources de données dans le projet nommé `ProjectA` :
  
```bash
dignacli list-ds ProjectA
```
  
Cette commande fournit aux utilisateurs une vue d’ensemble des sources de données disponibles dans un projet, les aidant à naviguer et à gérer le paysage des données plus efficacement.