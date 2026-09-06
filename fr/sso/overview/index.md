# Présentation de l’authentification unique (SSO)

---

## Table des matières

1. [Introduction et aperçu](#introduction-and-overview)
2. [Guides des fournisseurs](#provider-guides)
3. [Étapes de configuration](#configuration-steps)
4. [Configuration du tableau de bord](#dashboard-configuration)
5. [Configuration du backend](#backend-configuration)
6. [Test de connexion](#testing-login)
7. [Dépannage](#troubleshooting)
8. [Fournisseurs pris en charge](#supported-providers)

---

## Introduction et aperçu {: #introduction-and-overview }

Ce guide fournit des instructions pas à pas pour intégrer l’authentification unique (SSO) à la plateforme digna en utilisant **OpenID Connect (OIDC)**.

### Qu’est-ce que le SSO ?

L’authentification unique permet aux utilisateurs de se connecter à digna en toute sécurité en utilisant leurs identifiants d’entreprise via des fournisseurs d’identité externes. Les utilisateurs peuvent s’authentifier avec leurs identifiants professionnels au lieu de gérer des mots de passe séparés pour digna.

### Comment ça fonctionne

Le SSO dans digna est implémenté via le protocole OIDC. Plusieurs fournisseurs d’identité peuvent être configurés en parallèle en ajustant deux fichiers de configuration clés :

- **`dashboard_config.toml`** — Contrôle l’interface de connexion front-end
- **`config.toml`** — Configure les connexions OIDC côté backend

### Fournisseurs pris en charge {: #supported-providers-overview }

Les exemples de ce guide utilisent **Microsoft** et **Google**, mais **tout fournisseur compatible OIDC** peut être intégré en suivant la même structure.

---

## Guides des fournisseurs {: #provider-guides }

Chaque fournisseur nécessite les mêmes quatre valeurs — un client ID, un client secret, une URI de redirection et une URL de découverte — mais chacun les place à un endroit différent dans sa console d’administration, et plusieurs ont une étape propre au fournisseur que les autres n’ont pas. Les guides ci-dessous couvrent cette moitié du travail ; cette page couvre la partie digna, qui est identique pour tous.

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Configurer SSO avec AD FS](adfs_sso_guide.md) | Self-hosted; the only provider here where you control the token service |
| **Auth0** | [Configurer SSO avec Auth0](auth0_sso_guide.md) | Discovery URL is per-tenant, and custom domains change it |
| **Google Workspace** | [Configurer SSO avec Google Workspace](google_workspace_sso_guide.md) | Consent screen must be published before non-test users can log in |
| **Keycloak** | [Configurer SSO avec Keycloak](keycloak_sso_guide.md) | Self-hosted; discovery URL is per-realm |
| **Microsoft Entra ID** | [Configurer SSO avec Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID appears in the discovery URL; secrets expire |
| **Okta** | [Configurer SSO avec Okta](okta_sso_guide.md) | Authorization server choice changes the discovery URL |
| **OneLogin** | [Configurer SSO avec OneLogin](onelogin_sso_guide.md) | The OIDC app type must be chosen at creation and cannot be changed |
| **PingOne** | [Configurer SSO avec PingOne](pingone_sso_guide.md) | Environment ID appears in the discovery URL |

Tout autre fournisseur compatible OIDC fonctionne de la même manière — voir [Autres fournisseurs OIDC](#supported-providers).

---

## Étapes de configuration {: #configuration-steps }

La configuration du SSO nécessite des mises à jour de deux fichiers. Cette section explique comment configurer chacun d’eux.

### Aperçu des fichiers de configuration

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

Les deux fichiers doivent être configurés pour que le SSO fonctionne correctement.

---

## Configuration du tableau de bord {: #dashboard-configuration }

### Emplacement du fichier

```
dashboard/dashboard_config.toml
```

### Étape 1 : Ajouter des fournisseurs OIDC

Ajoutez des entrées sous le tableau `[[login.oidc]]` pour chaque fournisseur d’identité que vous souhaitez prendre en charge.

**Exemple avec Microsoft et Google :**

```toml
[[login.oidc]]
key = "microsoft"
label = "Se connecter avec Microsoft"

[[login.oidc]]
key = "google"
label = "Se connecter avec Google"
```

### Étape 2 : Configurer les options de connexion

Spécifiez si la connexion par mot de passe doit être autorisée :

```toml
[login]
usePassword = true
```

### Paramètres de configuration

#### `[[login.oidc]]` Section

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Identifiant unique pour la connexion OIDC (doit correspondre à la key dans config.toml) |
| `label` | string | Yes | Texte affiché sur le bouton de connexion (par ex., "Se connecter avec Microsoft") |

#### `[login]` Section

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Autoriser la connexion par mot de passe en plus du SSO |

### Comprendre usePassword

**Si `usePassword = true` :**
- L’écran de connexion affiche les boutons SSO (par ex., "Se connecter avec Microsoft")
- L’écran de connexion affiche également les champs nom d’utilisateur et mot de passe
- Les utilisateurs peuvent s’authentifier avec l’une ou l’autre méthode
- Permet des configurations hybrides où certains utilisateurs utilisent le SSO et d’autres des mots de passe

**Si `usePassword = false` (ou omis) :**
- L’écran de connexion affiche uniquement les boutons SSO
- Pas de champs nom d’utilisateur/mot de passe
- Seule l’authentification OIDC est disponible

!!! tip "Astuce"

    La connexion par mot de passe n’est disponible que pour les utilisateurs créés avec des mots de passe via la commande `digna user add` ou via le tableau de bord.

### Exemple complet

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Se connecter avec Microsoft"

[[login.oidc]]
key = "google"
label = "Se connecter avec Google"

[[login.oidc]]
key = "okta"
label = "Se connecter avec Okta"
```

---

## Configuration du backend {: #backend-configuration }

### Emplacement du fichier

```
/config.toml
```

(Répertoire racine d’installation de digna)

### Étape 1 : Ajouter des sections fournisseur OIDC

Chaque fournisseur doit avoir une section dédiée `[oidc.<key>]`. La key doit correspondre à la `key` définie dans `dashboard_config.toml`.

### Configuration Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Configuration Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Paramètres de configuration

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID fourni par le fournisseur d’identité | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Secret client fourni par le fournisseur d’identité | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | URL de callback après l’authentification | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | Endpoint de configuration OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Important"

    Remplacez les valeurs de remplacement (`<client_id>`, `<client_secret>`, `<tenant_id>`) par les identifiants réels provenant du portail développeur de votre fournisseur d’identité.

### URI de redirection

L’URI de redirection doit être identique à celle configurée chez votre fournisseur d’identité :

```
http://localhost:5173/oidc/callback
```

Si digna est hébergé sur un domaine différent, mettez-la à jour en conséquence :
- Local : `http://localhost:5173/oidc/callback`
- Production : `https://digna.yourdomain.com/oidc/callback`

### Exemple complet

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Test de connexion {: #testing-login }

Après avoir terminé la configuration, vérifiez que le SSO fonctionne correctement.

### Liste de vérification avant test

Avant de tester, assurez-vous :

- [ ] `dashboard_config.toml` a été mis à jour avec les fournisseurs OIDC
- [ ] `config.toml` a été mis à jour avec les identifiants OIDC
- [ ] Les deux fichiers ont été enregistrés
- [ ] Les identifiants sont corrects (client ID, client secret)
- [ ] L’URI de redirection correspond à l’URL de déploiement
- [ ] L’application chez le fournisseur d’identité est configurée avec l’URI de redirection

### Étapes de test

#### Étape 1 : Redémarrer les services

Redémarrez le backend digna et le serveur web pour appliquer les modifications.

**Si exécuté en tant que service sur Windows :**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Si exécuté en tant que service sur Linux ou macOS :**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Si exécuté manuellement :**
```bash
digna serve --address localhost --port 8082
```

**Redémarrez également le serveur web** — IIS ou Tomcat sur Windows, nginx ou Apache sur Linux et macOS.

#### Étape 2 : Ouvrir le tableau de bord

Ouvrez le tableau de bord digna dans votre navigateur :

```
http://localhost:5173
```

(ou votre URL de tableau de bord configurée)

#### Étape 3 : Vérifier les boutons de connexion

Vérifiez que des boutons de connexion apparaissent pour chaque fournisseur configuré :

- Le bouton "Se connecter avec Microsoft" devrait être visible
- Le bouton "Se connecter avec Google" devrait être visible
- (Si usePassword = true) Les champs nom d’utilisateur/mot de passe devraient être visibles

Si les boutons n’apparaissent pas :
- Vérifiez que `dashboard_config.toml` a bien été enregistré
- Vérifiez que le service du tableau de bord a été redémarré
- Consultez la console du navigateur (F12) pour les erreurs

#### Étape 4 : Tester la connexion SSO

Cliquez sur un des boutons SSO (par ex., "Se connecter avec Microsoft") :

1. Vous devriez être redirigé vers la page de connexion du fournisseur d’identité
2. Connectez-vous avec vos identifiants d’entreprise
3. Vous devriez être redirigé vers digna
4. Vous devriez être connecté à digna

#### Étape 5 : Vérifier la création d’utilisateur

Après une connexion SSO réussie :

- L’utilisateur devrait être créé automatiquement dans digna
- L’utilisateur devrait être connecté
- Le profil utilisateur devrait afficher les informations de votre fournisseur d’identité
- Vous devriez voir le tableau de bord digna

#### Étape 6 : Tester la connexion par mot de passe (si activée)

Si `usePassword = true` :

1. Déconnectez-vous de digna
2. Sur la page de connexion, entrez un nom d’utilisateur et un mot de passe
3. Vous devriez pouvoir vous connecter avec ces identifiants

---

## Dépannage {: #troubleshooting }

### Les boutons de connexion n’apparaissent pas

**Symptômes :**
- Les boutons de connexion OIDC ne sont pas visibles sur la page de connexion
- Vous voyez uniquement des champs mot de passe (si usePassword = true)

**Causes & Solutions :**
1. Vérifiez que `dashboard_config.toml` se trouve dans le répertoire `dashboard/`
2. Vérifiez que les sections `[[login.oidc]]` sont présentes avec la syntaxe correcte
3. Redémarrez le service du tableau de bord
4. Videz le cache du navigateur (Ctrl+Shift+Delete ou Cmd+Shift+Delete)
5. Consultez la console du navigateur (F12 → onglet Console) pour des erreurs

---

### Erreur de type « redirect URI mismatch »

**Symptômes :**
- Après avoir cliqué sur un bouton SSO, erreur relative à "redirect_uri mismatch"
- Erreur "The redirect URI is not registered"

**Causes & Solutions :**
1. Vérifiez que `DIGNA_OIDC_REDIRECT_URI` dans `config.toml` est correct
2. Vérifiez que l’URI de redirection est bien enregistrée dans les paramètres du fournisseur d’identité
3. Assurez-vous que les deux utilisent des URL identiques (y compris protocole, domaine, chemin)
4. Vérifiez les fautes de frappe dans l’URI de redirection
5. Si vous utilisez HTTPS, assurez-vous que le certificat est valide

---

### Erreur d’identifiants client invalides

**Symptômes :**
- Erreur "Invalid client ID or secret"
- Échec d’authentification avec une erreur d’identifiants

**Causes & Solutions :**
1. Vérifiez que `DIGNA_OIDC_CLIENT_ID` et `DIGNA_OIDC_CLIENT_SECRET` sont corrects
2. Assurez-vous qu’il n’y a pas d’espaces supplémentaires ou de caractères inattendus
3. Vérifiez que les identifiants n’ont pas expiré ou été révoqués
4. Redémarrez le service backend après mise à jour de la configuration
5. Consultez la console du fournisseur d’identité pour confirmer que les identifiants sont actifs

---

### Connexion bloquée ou timeout

**Symptômes :**
- Cliquer sur le bouton SSO ne provoque rien
- Timeout après quelques secondes
- Le navigateur affiche "Failed to connect" ou similaire

**Causes & Solutions :**
1. Vérifiez que le backend digna fonctionne : `digna repo check`
2. Vérifiez la connectivité réseau vers le fournisseur d’identité
3. Vérifiez que `DIGNA_OIDC_CONFIGURATION_URL` est accessible
4. Vérifiez les règles de pare-feu autorisant les connexions HTTPS sortantes
5. Assurez-vous que le backend et le tableau de bord peuvent se joindre mutuellement

---

### Les utilisateurs ne sont pas créés automatiquement

**Symptômes :**
- La connexion SSO réussit mais l’utilisateur n’est pas créé dans digna
- Erreur d’autorisation après la connexion SSO

**Causes & Solutions :**
1. Vérifiez que la configuration OIDC est correcte
2. Vérifiez les permissions utilisateur
3. Consultez les logs digna pour les messages d’erreur
4. Redémarrez le service backend
5. Contactez support@digna.ai si le problème persiste

---

## Fournisseurs pris en charge {: #supported-providers }

### Testés et pris en charge

Les fournisseurs OIDC suivants ont été testés et fonctionnent :

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Configurer SSO avec AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Configurer SSO avec Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Configurer SSO avec Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Configurer SSO avec Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Configurer SSO avec Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Configurer SSO avec Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Configurer SSO avec OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Configurer SSO avec PingOne](pingone_sso_guide.md) |

### Autres fournisseurs OIDC

Tout fournisseur prenant en charge OpenID Connect peut être intégré. Informations requises :

- Client ID
- Client secret
- URL de configuration OpenID (généralement `/.well-known/openid-configuration`)
- Scopes pris en charge (typiquement `openid profile email`)

Contactez support@digna.ai si vous avez besoin d’aide pour intégrer un fournisseur spécifique.

---

## Bonnes pratiques

**À FAIRE :**
- Utiliser HTTPS en production (pas HTTP)
- Stocker les secrets clients de manière sécurisée (utiliser des variables d’environnement si possible)
- Faire une rotation régulière des secrets
- Tester d’abord dans un environnement non-production
- Documenter les fournisseurs configurés
- Surveiller les journaux de connexion pour détecter toute activité inhabituelle
- Maintenir la configuration du fournisseur d’identité en cohérence avec la configuration digna

**À NE PAS FAIRE :**
- Stocker les secrets clients dans le contrôle de version
- Utiliser des URI de redirection HTTP en production
- Configurer plusieurs fournisseurs avec la même key
- Laisser des identifiants par défaut/test en production
- Exposer des fichiers de configuration contenant des secrets
- Mélanger les identifiants de développement et de production

---

## Support

Besoin d’aide pour la configuration du SSO ?

- **Email :** support@digna.ai
- **Documentation :** https://docs.digna.ai
- **Site web :** https://www.digna.ai

---

**Dernière mise à jour :** 30 août 2026  
**Version :** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**