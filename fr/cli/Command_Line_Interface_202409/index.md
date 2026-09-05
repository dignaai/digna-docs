# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basics

---

###   help

L'option --help fournit des informations sur les commandes disponibles et leur utilisation. Il existe deux façons principales d'utiliser cette option :

1. **Affichage de l'aide générale :**
   
    Utilisez --help immédiatement après le mot-clé ***digna*** CLI  
   bash
   dignacli --help

3.  **Obtenir de l'aide pour des commandes spécifiques :**  
  
    Pour des informations détaillées sur une commande particulière, ajoutez --help à cette commande.
    Par exemple, pour obtenir de l'aide sur la commande add-user, exécutez :
     bash
     dignacli add-user --help
     

     ### sortie :
      
     - **Description de la commande :** Offre une description détaillée de ce que fait la commande.  
     - **Syntaxe :** Affiche la syntaxe exacte, y compris les arguments requis et optionnels.  
     - **Options :** Liste les options spécifiques à la commande, avec leurs explications.  
     - **Exemples :** Fournit des exemples d'exécution efficace de la commande.

  
###   check-repo-connection

La commande check-repo-connection est un utilitaire de la CLI ***digna*** conçu pour tester la connectivité et l'accès à un dépôt ***digna*** spécifié. Cette commande vérifie que la CLI peut interagir avec le dépôt.
      
##### Utilisation de la commande
bash
dignacli check-repo-connection


Lors d'une exécution réussie, la commande affiche une confirmation de la connexion, ainsi que des détails sur le dépôt : version du dépôt, hôte, base de données et schéma.  
  
Si la connexion au dépôt échoue, vérifiez le fichier config.toml pour vous assurer que les paramètres de configuration sont corrects.

###   version

Pour vérifier la version installée de *dignacli*, utilisez l'option --version.  
  
#### Utilisation de la commande
bash
dignacli --version

  
#### Exemple de sortie
bash
dignacli version 2024.09


###   logging options
  
Par défaut, la sortie console des commandes ***digna*** est conçue pour être minimaliste. La plupart des commandes offrent la possibilité d'afficher des informations supplémentaires à l'aide des options suivantes :  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
« verbose » et « debug » définissent le niveau de détail, tandis que l'option « logfile » permet de rediriger la sortie vers un fichier plutôt que vers la console.

## User Management

###   add-user
  
La commande add-user de la CLI ***digna*** est utilisée pour ajouter un nouvel utilisateur au système ***digna***.
  
#### Utilisation de la commande
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME** : Le nom d'utilisateur du nouvel utilisateur (requis).
- **USER_FULL_NAME** : Le nom complet du nouvel utilisateur (requis).
- **USER_PASSWORD** : Le mot de passe du nouvel utilisateur (requis).

#### Options

- --is_superuser, -su : Indique que le nouvel utilisateur est un administrateur.
- --valid_until, -vu : Définit une date d'expiration pour le compte utilisateur au format YYYY-MM-DD HH:MI:SS. Si non défini, le compte n'a pas de date d'expiration.

#### Exemple

Pour ajouter un nouvel utilisateur avec le nom d'utilisateur jdoe, le nom complet John Doe et le mot de passe password123 :

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Pour ajouter un nouvel utilisateur et définir une date d'expiration du compte :
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
La commande delete-user de la CLI ***digna*** est utilisée pour supprimer un utilisateur existant du système ***digna***.
  
##### Utilisation de la commande
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME** : Le nom d'utilisateur de l'utilisateur à supprimer (requis). C'est le seul argument requis par la commande.

#### Exemple
bash
dignacli delete-user jdoe

  
L'exécution de cette commande supprime l'utilisateur jdoe du système ***digna***, révoque son accès et supprime ses données et autorisations associées du dépôt.

###   modify-user

La commande modify-user de la CLI ***digna*** est utilisée pour mettre à jour les informations d'un utilisateur existant dans le système ***digna***.

##### Utilisation de la commande
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME** : Le nom d'utilisateur de l'utilisateur à modifier (requis).
- **USER_FULL_NAME** : Le nouveau nom complet de l'utilisateur (requis).
  
#### Options  
  
- --is_superuser, -su : Définit l'utilisateur comme superutilisateur, accordant des privilèges élevés. Ce flag ne nécessite pas de valeur.  
- --valid_until, -vu : Définit une date d'expiration pour le compte utilisateur au format YYYY-MM-DD HH:MI:SS. Si non fourni, le compte reste valide indéfiniment.  
  
#### Exemple
  
Pour modifier le nom complet de l'utilisateur jdoe en « Johnathan Doe » et définir l'utilisateur comme superutilisateur :
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
La commande modify-user-pwd de la CLI ***digna*** est utilisée pour changer le mot de passe d'un utilisateur existant dans le système ***digna***.
  
##### Utilisation de la commande
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME** : Le nom d'utilisateur de l'utilisateur dont le mot de passe doit être modifié (requis).
- **USER_PWD** : Le nouveau mot de passe de l'utilisateur (requis).
  
#### Exemple
  
Pour changer le mot de passe de l'utilisateur jdoe en newpassword123 :
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

La commande list-users de la CLI ***digna*** affiche la liste de tous les utilisateurs enregistrés dans le système ***digna***.

##### Utilisation de la commande

bash
dignacli list-users


L'exécution de cette commande dans la CLI ***digna*** se connecte au dépôt ***digna*** et liste tous les utilisateurs, en montrant leur ID, nom d'utilisateur, nom complet, statut de superutilisateur et les horodatages d'expiration.

# Repository Management

###   upgrade-repo
  
La commande upgrade-repo de la CLI ***digna*** est utilisée pour mettre à niveau ou initialiser le dépôt ***digna***. Cette commande est essentielle pour appliquer des mises à jour ou configurer l'infrastructure du dépôt pour la première fois.
  
#### Utilisation de la commande

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s : Lorsqu'elle est activée, cette option exécute la commande en mode simulation, ce qui affiche les instructions SQL qui seraient exécutées sans réellement les exécuter. Utile pour prévisualiser les changements sans modifier le dépôt.  

  
#### Exemple
  
Pour mettre à niveau le dépôt ***digna***, vous pouvez exécuter la commande sans options :
  
bash
dignacli upgrade-repo
  
Pour exécuter la mise à niveau en mode simulation (voir les instructions SQL sans les appliquer) :
  
bash
dignacli upgrade-repo --simulation-mode

  
Cette commande est cruciale pour maintenir le système ***digna***, en s'assurant que le schéma de la base de données et les autres composants du dépôt sont à jour avec la dernière version du logiciel.

###   encrypt
  
La commande encrypt de la CLI ***digna*** est utilisée pour chiffrer un mot de passe.
  
#### Utilisation de la commande
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD** : Le mot de passe à chiffrer (requis).
  
#### Exemple
  
Pour chiffrer un mot de passe, vous devez fournir le mot de passe en argument.   
Par exemple, pour chiffrer le mot de passe mypassword123, vous utiliseriez :
bash
dignacli encrypt mypassword123

Cette commande affiche la version chiffrée du mot de passe fourni, qui peut ensuite être utilisée dans des contextes sécurisés. Si l'argument du mot de passe n'est pas fourni, la CLI affichera une erreur indiquant l'argument manquant.

###   generate-key
  
La commande generate-key est utilisée pour générer une clé Fernet, essentielle pour sécuriser les mots de passe stockés dans le dépôt ***digna***.
  
#### Utilisation de la commande
bash
dignacli generate-key

  
## Data Management

###   clean-up

La commande clean-up de la CLI ***digna*** est utilisée pour supprimer les profils, les prédictions et les données du système de feux tricolores (Traffic Light System) pour une ou plusieurs sources de données au sein d'un projet spécifié. Cette commande est essentielle pour la gestion du cycle de vie des données, aidant à maintenir un environnement de données organisé et efficace en supprimant les données obsolètes ou non nécessaires.

#### Utilisation de la commande

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet à partir duquel les données doivent être supprimées (requis). L'utilisation du mot-clé all-projects pour cet argument indique à ***digna*** d'itérer sur tous les projets existants et d'appliquer cette commande.
- **FROM_DATE** : La date et l'heure de début pour la suppression des données. Les formats acceptables incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l'heure de fin pour la suppression des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options
  
- --table-name, -tn : Limite l'opération de nettoyage à une table spécifique dans le projet.
- --table-filter, -tf : Filtre pour limiter le nettoyage aux tables contenant la sous-chaîne spécifiée dans leur nom.
- --timing, -tm : Affiche la durée du processus de nettoyage après son achèvement.
- --help : Affiche les informations d'aide pour la commande clean-up et quitte.
  
#### Exemple
  
Pour supprimer des données du projet ProjectA entre le 1er janvier 2023 et le 30 juin 2023 :
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Pour supprimer des données uniquement d'une table spécifique nommée Table1 :
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
Cette commande aide à gérer le stockage des données et à garantir que le dépôt ne contient que des informations pertinentes.

###   inspect

La commande inspect de la CLI ***digna*** est utilisée pour créer des profils, des prédictions et des données du système de feux tricolores pour une ou plusieurs sources de données au sein d'un projet spécifié. Cette commande aide à analyser et surveiller les données sur une période définie.

#### Utilisation de la commande

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel les données doivent être inspectées (requis). L'utilisation du mot-clé all-projects pour cet argument indique à ***digna*** d'itérer sur tous les projets existants et d'appliquer cette commande.
- **FROM_DATE** : La date et l'heure de début pour l'inspection des données. Les formats acceptables incluent %Y-%m-%d, %Y-%m-%dT%H:%M:%S ou %Y-%m-%d %H:%M:%S (requis).
- **TO_DATE** : La date et l'heure de fin pour l'inspection des données, suivant les mêmes formats que FROM_DATE (requis).
  
#### Options

- --table-name, -tn : Limite l'inspection à une table spécifique dans le projet.
- --table-filter, -tf : Filtre pour n'inspecter que les tables contenant la sous-chaîne spécifiée dans leur nom.
- --force-profile : Force la recollection des profils. La valeur par défaut est force-profile.
- --no-force-profile : Empêche la recollection des profils.
- --force-prediction : Force le recalcul des prédictions. La valeur par défaut est force-prediction.
- --no-force-prediction : Empêche le recalcul des prédictions.
- --force-alert-status : Force le recalcul des statuts d'alerte. La valeur par défaut est force-alert-status.
- --no-force-alert-status : Empêche le recalcul des statuts d'alerte.
- --timing, -tm : Affiche la durée du processus d'inspection après son achèvement.
- --alert-notification, -an : Envoie des notifications d'alerte aux canaux abonnés.
  
#### Exemple
  
Pour inspecter les données du projet ProjectA du 1er janvier 2024 au 31 janvier 2024 :
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Pour inspecter une table spécifique et forcer le recalcul des prédictions :
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

Cette commande est utile pour générer des profils et prédictions à jour, surveiller l'intégrité des données et gérer les systèmes d'alerte dans une période de projet spécifiée.

###   tls-status

La commande tls-status de la CLI ***digna*** est utilisée pour interroger le statut du Traffic Light System (TLS) pour une table spécifique d'un projet à une date donnée. Le Traffic Light System fournit des informations sur la santé et la qualité des données, indiquant d'éventuels problèmes ou alertes nécessitant une attention.
  
#### Utilisation de la commande
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME** : Le nom du projet pour lequel le statut TLS est demandé (requis).
- **TABLE_NAME** : La table spécifique du projet pour laquelle le statut TLS est nécessaire (requis).
- **DATE** : La date pour laquelle le statut TLS est interrogé, typiquement au format %Y-%m-%d (requis).
  
#### Exemple
  
Pour vérifier le statut TLS d'une table nommée UserData dans le projet ProjectA le 1er juillet 2024 :

bash
dignacli tls-status ProjectA UserData 2024-07-01


Cette commande aide les utilisateurs à surveiller et maintenir la qualité des données en fournissant un rapport de statut clair et exploitable basé sur des critères prédéfinis.

###   list-projects
  
La commande list-projects de la CLI ***digna*** est utilisée pour afficher la liste de tous les projets disponibles dans le système ***digna***.
  
#### Utilisation de la commande
  
bash
dignacli list-projects


Cette commande est particulièrement utile pour les administrateurs et les utilisateurs gérant plusieurs projets, offrant un aperçu rapide des projets disponibles dans le dépôt ***digna***.

###   list-ds

La commande list-ds de la CLI ***digna*** est utilisée pour afficher la liste de toutes les sources de données disponibles dans un projet spécifié. Cette commande est utile pour comprendre les actifs de données disponibles pour l'analyse et la gestion dans le système ***digna***.

#### Utilisation de la commande
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME** : Le nom du projet pour lequel les sources de données sont listées (requis).
  
#### Exemple
  
Pour lister toutes les sources de données du projet nommé ProjectA :
  
bash
dignacli list-ds ProjectA

  
Cette commande fournit aux utilisateurs un aperçu des sources de données disponibles dans un projet, les aidant à naviguer et à gérer le paysage des données plus efficacement.