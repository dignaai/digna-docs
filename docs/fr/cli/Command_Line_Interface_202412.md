---
title: digna CLI Reference 2024.12 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.12. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Cette page documente l'ensemble des commandes disponibles dans le CLI ***digna***, version **2024.12**, incluant des exemples d'utilisation et les options.

---


**2024-12-09**


---

## Principes de base du CLI

---

## Utilisation de l'option `--help`

L'option `--help` fournit des informations sur les commandes disponibles et leur utilisation. Il existe deux manières principales d'utiliser cette option :

1. **Afficher l'aide générale :**
   
    Utilisez --help immédiatement après le mot-clé ***dignacli***  
   ```bash
   dignacli --help
   ```

3.  **Obtenir de l'aide pour des commandes spécifiques :**  
  
    Pour des informations détaillées sur une commande particulière, ajoutez `--help` à cette commande.
    Par exemple, pour obtenir de l'aide sur la commande `add-user`, exécutez :
     ```bash
     dignacli add-user --help
     ```

     ### sortie :
      
     - **Description de la commande :** Fournit une description détaillée de ce que fait la commande.  
     - **Syntaxe :** Affiche la syntaxe exacte, incluant les arguments requis et optionnels.  
     - **Options :** Liste les options spécifiques à la commande, avec leurs explications.  
     - **Exemples :** Donne des exemples d'exécution de la commande de manière efficace.

  
## Utilisation de la commande `check-repo-connection`

La commande check-repo-connection est un utilitaire du CLI ***digna*** conçu pour tester la connectivité et l'accès à un dépôt ***digna*** spécifié. Cette commande vérifie que le CLI peut interagir avec le dépôt.
      
### Utilisation de la commande
```bash
dignacli check-repo-connection
```

Après exécution avec succès, la commande affiche une confirmation de la connexion, ainsi que des détails sur le dépôt : version du dépôt, hôte, base de données et schéma.  
  
Si la connexion au dépôt échoue, vérifiez le fichier config.toml pour vous assurer que les paramètres de configuration sont corrects.

## Utilisation de la commande `version`

Pour vérifier la version installée de *dignacli*, utilisez l'option --version.  
  
### Utilisation de la commande
```bash
dignacli --version
```
  
### Exemple de sortie
```bash
dignacli version 2024.12
```

## Utilisation des options de journalisation
  
Par défaut, la sortie console des commandes ***digna*** est conçue pour être minimaliste. La plupart des commandes offrent la possibilité d'afficher des informations supplémentaires en utilisant les options suivantes :  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
 "verbose" et "debug" définissent le niveau de détail, tandis que l'option "logfile" permet de rediriger la sortie vers un fichier au lieu de la console.

# Gestion des utilisateurs

## Utilisation de la commande `add-user`
  
La commande add-user du CLI ***digna*** est utilisée pour ajouter un nouvel utilisateur au système ***digna***.
  
### Utilisation de la commande
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Arguments

- **USER_NAME** : Le nom d'utilisateur du nouvel utilisateur (obligatoire).
- **USER_FULL_NAME** : Le nom complet du nouvel utilisateur (obligatoire).
- **USER_PASSWORD** : Le mot de passe du nouvel utilisateur (obligatoire).

### Options

- `--is_superuser`, `-su` : Indique que le nouvel utilisateur est administrateur.
- `--valid_until`, `-vu` : Définit une date d'expiration pour le compte utilisateur au format `YYYY-MM-DD HH:MI:SS`. Si non définie, le compte n'a pas de date d'expiration.

### Exemple

Pour ajouter un nouvel utilisateur avec le nom d'utilisateur `jdoe`, le nom complet `John Doe` et le mot de passe `password123` :

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Pour ajouter un nouvel utilisateur et définir une date d'expiration du compte :
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Utilisation de la commande `delete-user`
  
La commande `delete-user` du CLI ***digna*** est utilisée pour supprimer un utilisateur existant du système ***digna***.
  
### Utilisation de la commande
```bash
dignacli delete-user USER_NAME
```
  
### Arguments
- **USER_NAME** : Le nom d'utilisateur de l'utilisateur à supprimer (obligatoire). C'est le seul argument requis par la commande.

### Exemple
```bash
dignacli delete-user jdoe
```
  
L'exécution de cette commande retirera l'utilisateur `jdoe` du système ***digna***, révoquera son accès et supprimera ses données et permissions associées du dépôt.

## Utilisation de la commande `modify-user`

La commande `modify-user` du CLI ***digna*** est utilisée pour mettre à jour les informations d'un utilisateur existant dans le système ***digna***.

### Utilisation de la commande
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Arguments
  
- **USER_NAME** : Le nom d'utilisateur de l'utilisateur à modifier (obligatoire).
- **USER_FULL_NAME** : Le nouveau nom complet de l'utilisateur (obligatoire).
  
### Options  
  
- `--is_superuser`, `-su` : Définit l'utilisateur comme superuser, accordant des privilèges élevés. Ce flag ne nécessite pas de valeur.  
- `--valid_until`, `-vu` : Définit une date d'expiration pour le compte utilisateur au format YYYY-MM-DD HH:MI:SS. Si non fournie, le compte reste valide indéfiniment.  
  
### Exemple
  
Pour modifier le nom complet de l'utilisateur `jdoe` en « Johnathan Doe » et définir l'utilisateur comme superuser :
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Utilisation de la commande `modify-user-pwd`
  
La commande `modify-user-pwd` du CLI ***digna*** est utilisée pour changer le mot de passe d'un utilisateur existant dans le système ***digna***.
  
### Utilisation de la commande
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Arguments
  
- **USER_NAME** : Le nom d'utilisateur dont on veut changer le mot de passe (obligatoire).
- **USER_PWD** : Le nouveau mot de passe de l'utilisateur (obligatoire).
  
### Exemple
  
Pour changer le mot de passe de l'utilisateur `jdoe` en `newpassword123` :
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Utilisation de la commande `list-users`

La commande `list-users` du CLI ***digna*** affiche la liste de tous les utilisateurs enregistrés dans le système ***digna***.

### Utilisation de la commande

```bash
dignacli list-users
```

L'exécution de cette commande dans le CLI ***digna*** se connectera au dépôt ***digna*** et listera tous les utilisateurs, affichant leur ID, nom d'utilisateur, nom complet, statut superuser et timestamps d'expiration.

# Gestion des dépôts

### Utilisation de la commande `upgrade-repo`
  
La commande `upgrade-repo` du CLI ***digna*** est utilisée pour migrer ou initialiser le dépôt ***digna***. Cette commande est essentielle pour appliquer des mises à jour ou pour configurer l'infrastructure du dépôt pour la première fois.
  
### Utilisation de la commande

```bash
dignacli upgrade-repo [options]
```
  
### Options
  
- `--simulation-mode`, `-s` : Lorsqu'elle est activée, cette option exécute la commande en mode simulation, ce qui affiche les instructions SQL qui seraient exécutées sans réellement les appliquer. Utile pour prévisualiser les changements sans modifier le dépôt.  

  
### Exemple
  
Pour migrer le dépôt ***digna***, vous pouvez exécuter la commande sans options :
  
```bash
dignacli upgrade-repo
```  
Pour exécuter la migration en mode simulation (voir les requêtes SQL sans les appliquer) :
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
Cette commande est cruciale pour maintenir le système ***digna***, en s'assurant que le schéma de la base de données et les autres composants du dépôt sont à jour avec la dernière version du logiciel.

## Utilisation de la commande `encrypt`
  
La commande `encrypt` du CLI ***digna*** est utilisée pour chiffrer un mot de passe.
  
### Utilisation de la commande
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Arguments
- **PASSWORD** : Le mot de passe à chiffrer (obligatoire).
  
### Exemple
  
Pour chiffrer un mot de passe, vous devez fournir le mot de passe en argument.   
Par exemple, pour chiffrer le mot de passe `mypassword123`, utilisez :
```bash
dignacli encrypt mypassword123
```
Cette commande renverra la version chiffrée du mot de passe fourni, qui pourra ensuite être utilisée dans des contextes sécurisés. Si l'argument du mot de passe n'est pas fourni, le CLI affichera une erreur indiquant l'argument manquant.

## Utilisation de la commande `generate-key`
  
La commande `generate-key` est utilisée pour générer une clé Fernet, essentielle pour sécuriser les mots de passe stockés dans le dépôt ***digna***.
  
### Utilisation de la commande
```bash
dignacli generate-key
```
  
# Gestion des données

## Utilisation de la commande `clean-up`

La commande `clean-up` du CLI ***digna*** est utilisée pour supprimer les profils, prédictions et les données du système de feux tricolores pour une ou plusieurs sources de données au sein d'un projet spécifié. Cette commande est essentielle pour la gestion du cycle de vie des données, aidant à maintenir un environnement de données organisé et efficace en supprimant les données obsolètes ou inutiles.

### Utilisation de la commande

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME** : Le nom du projet depuis lequel les données doivent être supprimées (obligatoire). L'utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d'itérer sur tous les projets existants et d'appliquer la commande.
- **FROM_DATE** : La date et l'heure de début pour la suppression des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S ou %Y-%m-%d %H:%M:%S (obligatoire).
- **TO_DATE** : La date et l'heure de fin pour la suppression des données, selon les mêmes formats que FROM_DATE (obligatoire).
  
### Options
  
- `--table-name`, `-tn` : Limite l'opération de nettoyage à une table spécifique dans le projet.
- `--table-filter`, `-tf` : Filtre pour limiter le nettoyage aux tables contenant la sous-chaîne spécifiée dans leur nom.
- `--timing`, `-tm` : Affiche la durée du processus de nettoyage après son achèvement.
- `--help` : Affiche l'aide pour la commande clean-up et quitte.
  
### Exemple
  
Pour supprimer des données du projet ProjectA entre le 1er janvier 2023 et le 30 juin 2023 :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Pour supprimer des données uniquement d'une table spécifique nommée `Table1` :
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
Cette commande aide à gérer le stockage des données et à s'assurer que le dépôt ne contient que des informations pertinentes.

## Utilisation de la commande `inspect`

La commande `inspect` du CLI ***digna*** est utilisée pour créer des profils, des prédictions et les données du système de feux tricolores pour une ou plusieurs sources de données au sein d'un projet spécifié. Cette commande aide à analyser et à surveiller les données sur une période définie.

### Utilisation de la commande

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel les données doivent être inspectées (obligatoire). L'utilisation du mot-clé all-projects dans cet argument indique à ***digna*** d'itérer sur tous les projets existants et d'appliquer la commande.
- **FROM_DATE** : La date et l'heure de début pour l'inspection des données. Les formats acceptés incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S ou %Y-%m-%d %H:%M:%S (obligatoire).
- **TO_DATE** : La date et l'heure de fin pour l'inspection des données, selon les mêmes formats que FROM_DATE (obligatoire).
  
### Options

- `--table-name`, `-tn` : Limite l'inspection à une table spécifique dans le projet.
- `--table-filter`, `-tf` : Filtre pour n'inspecter que les tables contenant la sous-chaîne spécifiée dans leur nom.
- `--do-profile` : Active la recollection des profils. Par défaut, do-profile est activé.
- `--no-do-profile` : Empêche la recollection des profils.
- `--do-prediction` : Active le recalcul des prédictions. Par défaut, do-prediction est activé.
- `--no-do-prediction` : Empêche le recalcul des prédictions.
- `--do-alert-status` : Active le recalcul des statuts d'alerte. Par défaut, do-alert-status est activé.
- `--no-do-alert-status` : Empêche le recalcul des statuts d'alerte.
- `--iterative` : Active l'inspection de la période en itérations journalières. Par défaut, iterative est activé.
- `--no-iterative` : Effectue l'inspection de la période entière en une seule exécution.
- `--timing`, `-tm` : Affiche la durée du processus d'inspection après son achèvement.
  
### Exemple
  
Pour inspecter les données du projet `ProjectA` du 1er janvier 2024 au 31 janvier 2024 :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Pour n'inspecter qu'une table spécifique et forcer le recalcul des prédictions :
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
Cette commande est utile pour générer des profils et des prédictions à jour, surveiller l'intégrité des données et gérer les systèmes d'alerte dans une période donnée pour un projet spécifié.

## Utilisation de la commande `tls-status`

La commande `tls-status` du CLI ***digna*** est utilisée pour interroger le statut du système de feux tricolores (TLS) pour une table spécifique d'un projet à une date donnée. Le système de feux tricolores fournit des indications sur la santé et la qualité des données, signalant les problèmes ou alertes nécessitant une attention.
  
### Utilisation de la commande
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel le statut TLS est interrogé (obligatoire).
- **TABLE_NAME** : La table spécifique dans le projet pour laquelle le statut TLS est requis (obligatoire).
- **DATE** : La date pour laquelle le statut TLS est interrogé, typiquement au format %Y-%m-%d (obligatoire).
  
### Exemple
  
Pour vérifier le statut TLS d'une table nommée UserData dans le projet ProjectA le 1er juillet 2024 :

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

Cette commande aide les utilisateurs à surveiller et maintenir la qualité des données en fournissant un rapport clair et exploitable basé sur des critères prédéfinis.

## Utilisation de la commande `list-projects`
  
La commande `list-projects` du CLI ***digna*** est utilisée pour afficher la liste de tous les projets disponibles dans le système ***digna***.
  
### Utilisation de la commande
  
```bash
dignacli list-projects
```

Cette commande est particulièrement utile pour les administrateurs et les utilisateurs gérant plusieurs projets, offrant un aperçu rapide des projets disponibles dans le dépôt ***digna***.

## Utilisation de la commande `list-ds`

La commande `list-ds` du CLI ***digna*** est utilisée pour afficher la liste de toutes les sources de données disponibles dans un projet spécifié. Cette commande est utile pour comprendre les actifs de données disponibles pour l'analyse et la gestion dans le système ***digna***.

### Utilisation de la commande
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Arguments
- **PROJECT_NAME** : Le nom du projet pour lequel les sources de données sont listées (obligatoire).
  
### Exemple
  
Pour lister toutes les sources de données du projet nommé `ProjectA` :
  
```bash
dignacli list-ds ProjectA
```
  
Cette commande fournit aux utilisateurs un aperçu des sources de données disponibles dans un projet, les aidant à naviguer et gérer le paysage des données plus efficacement.