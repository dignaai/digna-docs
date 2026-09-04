---
title: Guide d'intégration Single Sign-On (SSO) | documentation digna
description: Guide étape par étape pour configurer le Single Sign-On (SSO) pour digna en utilisant OpenID Connect (OIDC). Couvre la configuration du tableau de bord et du backend, les tests, le dépannage et les fournisseurs d'identité pris en charge, notamment Microsoft Entra ID, Google Workspace et Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - authentification unique
  - intégration oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - intégration okta
  - authentification entreprise
lang: fr
robots: index, follow
og_title: Guide d'intégration Single Sign-On (SSO) digna
og_description: Configurez le Single Sign-On pour digna en utilisant OpenID Connect. Configuration étape par étape pour Microsoft Entra ID, Google Workspace, Okta et autres fournisseurs d'identité compatibles OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Guide d'intégration Single Sign-On

---

## Table des matières

1. [Introduction et aperçu](#introduction-et-aperçu)
2. [Étapes de configuration](#étapes-de-configuration)
3. [Configuration du tableau de bord](#configuration-du-tableau-de-bord)
4. [Configuration du backend](#configuration-du-backend)
5. [Test de connexion](#test-de-connexion)
6. [Dépannage](#dépannage)
7. [Fournisseurs pris en charge](#fournisseurs-pris-en-charge)

---

## Introduction et aperçu {: #introduction-and-overview }

Ce guide fournit des instructions pas à pas pour intégrer le Single Sign-On (SSO) avec la plateforme digna en utilisant **OpenID Connect (OIDC)**.

### Qu'est-ce que le SSO ?

Le Single Sign-On permet aux utilisateurs de se connecter à digna de manière sécurisée en utilisant leurs identifiants d'entreprise via des fournisseurs d'identité externes. Les utilisateurs peuvent s'authentifier avec leurs identifiants d'entreprise au lieu de gérer des mots de passe séparés pour digna.

### Comment ça fonctionne

Le SSO dans digna est implémenté en utilisant le protocole OIDC. Plusieurs fournisseurs d'identité peuvent être configurés en parallèle en ajustant deux fichiers de configuration clés :

- **`dashboard_config.toml`** — Contrôle l'interface de connexion côté frontend
- **`config.toml`** — Configure les connexions OIDC côté backend

### Fournisseurs pris en charge {: #supported-providers-overview }

Les exemples de ce guide utilisent **Microsoft** et **Google**, mais **tout fournisseur compatible OIDC** peut être intégré en suivant la même structure.

Fournisseurs OIDC courants :
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Autres fournisseurs d'identité compatibles OIDC

---

## Étapes de configuration {: #configuration-steps }

La configuration du SSO nécessite des mises à jour dans deux fichiers. Cette section explique comment configurer chacun d'eux.

### Vue d'ensemble des fichiers de configuration

| Fichier | Emplacement | Objectif |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interface de connexion frontend |
| **config.toml** | `/config.toml` | Connexions OIDC côté backend |

Les deux fichiers doivent être configurés pour que le SSO fonctionne correctement.

---

## Configuration du tableau de bord {: #dashboard-configuration }

### Emplacement du fichier

```
dashboard/dashboard_config.toml
```

### Étape 1 : Ajouter des fournisseurs OIDC

Ajoutez des entrées sous le tableau `[[login.oidc]]` pour chaque fournisseur d'identité que vous souhaitez prendre en charge.

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

#### Section `[[login.oidc]]`

| Paramètre | Type | Obligatoire | Description |
|---|---|---|---|
| `key` | string | Oui | Identifiant unique pour la connexion OIDC (doit correspondre à la key dans config.toml) |
| `label` | string | Oui | Texte affiché sur le bouton de connexion (p. ex. "Se connecter avec Microsoft") |

#### Section `[login]`

| Paramètre | Type | Valeur par défaut | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Autoriser la connexion par mot de passe en complément du SSO |

### Comprendre usePassword

**Si `usePassword = true` :**
- L'écran de connexion affiche les boutons SSO (par ex., "Se connecter avec Microsoft")
- L'écran de connexion affiche aussi les champs nom d'utilisateur et mot de passe
- Les utilisateurs peuvent s'authentifier par l'une ou l'autre méthode
- Permet des configurations hybrides où certains utilisateurs utilisent le SSO et d'autres des mots de passe

**Si `usePassword = false` (ou omis) :**
- L'écran de connexion n'affiche que les boutons SSO
- Aucun champ nom d'utilisateur/mot de passe
- Seule l'authentification OIDC est disponible

> **💡 Astuce**
>
> La connexion par mot de passe n'est disponible que pour les utilisateurs créés avec un mot de passe via la commande `digna user add` ou via le tableau de bord.

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

(Répertoire d'installation racine de digna)

### Étape 1 : Ajouter des sections pour les fournisseurs OIDC

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

| Paramètre | Type | Obligatoire | Description | Exemple |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Oui | ID client fourni par le fournisseur d'identité | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Oui | Secret client fourni par le fournisseur d'identité | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Oui | URL de rappel après authentification | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Oui | Endpoint de configuration OIDC | `https://login.microsoftonline.com/...` |

> **⚠️ Important**
>
> Remplacez les valeurs factices (`<client_id>`, `<client_secret>`, `<tenant_id>`) par les identifiants réels depuis le portail développeur de votre fournisseur d'identité.

### URI de redirection

L'URI de redirection doit être la même que dans la configuration de votre fournisseur d'identité :

```
http://localhost:5173/oidc/callback
```

Si digna est hébergé sur un domaine différent, mettez-le à jour en conséquence :
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

Après avoir complété la configuration, vérifiez que le SSO fonctionne correctement.

### Liste de vérification avant test

Avant de tester, assurez-vous que :

- [ ] `dashboard_config.toml` a été mis à jour avec les fournisseurs OIDC
- [ ] `config.toml` a été mis à jour avec les identifiants OIDC
- [ ] Les deux fichiers ont été sauvegardés
- [ ] Les identifiants sont corrects (client ID, client secret)
- [ ] L'URI de redirection correspond à l'URL de votre déploiement
- [ ] L'application du fournisseur d'identité est configurée avec l'URI de redirection

### Étapes de test

#### Étape 1 : Redémarrer les services

Redémarrez le backend et le serveur web digna pour appliquer les changements.

**Si exécuté en tant que service Windows :**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Si exécuté manuellement :**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Si vous utilisez IIS ou Tomcat :**
Redémarrez le service de votre serveur web.

#### Étape 2 : Ouvrir le tableau de bord

Ouvrez le tableau de bord digna dans votre navigateur :

```
http://localhost:5173
```

(ou l'URL de tableau de bord que vous avez configurée)

#### Étape 3 : Vérifier les boutons de connexion

Vérifiez que les boutons de connexion apparaissent pour chaque fournisseur configuré :

- ✅ Vous devriez voir le bouton "Se connecter avec Microsoft"
- ✅ Vous devriez voir le bouton "Se connecter avec Google"
- ✅ (Si usePassword = true) Vous devriez voir les champs nom d'utilisateur/mot de passe

Si les boutons n'apparaissent pas :
- Vérifiez que `dashboard_config.toml` a été sauvegardé
- Vérifiez que le service du tableau de bord a été redémarré
- Consultez la console du navigateur (F12) pour voir les erreurs

#### Étape 4 : Tester la connexion SSO

Cliquez sur l'un des boutons SSO (par ex., "Se connecter avec Microsoft") :

1. Vous devriez être redirigé vers la page de connexion du fournisseur d'identité
2. Connectez-vous avec vos identifiants d'entreprise
3. Vous devriez être redirigé vers digna
4. Vous devriez être connecté à digna

#### Étape 5 : Vérifier la création d'utilisateur

Après une connexion SSO réussie :

- ✅ L'utilisateur devrait être créé automatiquement dans digna
- ✅ L'utilisateur devrait être connecté
- ✅ Le profil utilisateur devrait afficher vos informations du fournisseur d'identité
- ✅ Vous devriez voir le tableau de bord digna

#### Étape 6 : Tester la connexion par mot de passe (si activée)

Si `usePassword = true` :

1. Déconnectez-vous de digna
2. Sur la page de connexion, saisissez un nom d'utilisateur et un mot de passe
3. Vous devriez pouvoir vous connecter avec les identifiants par mot de passe

---

## Dépannage {: #troubleshooting }

### Les boutons de connexion n'apparaissent pas

**Symptômes :**
- Les boutons de connexion OIDC ne sont pas visibles sur la page de connexion
- Vous ne voyez que les champs mot de passe (si usePassword = true)

**Causes & Solutions :**
1. Vérifiez que `dashboard_config.toml` est dans le répertoire `dashboard/`
2. Vérifiez que les sections `[[login.oidc]]` sont présentes et ont la bonne syntaxe
3. Redémarrez le service du tableau de bord
4. Videz le cache du navigateur (Ctrl+Shift+Delete ou Cmd+Shift+Delete)
5. Consultez la console du navigateur (F12 → onglet Console) pour les erreurs

---

### Erreur de type "redirect URI mismatch"

**Symptômes :**
- Après avoir cliqué sur le bouton SSO, erreur concernant "redirect_uri mismatch"
- Erreur "The redirect URI is not registered"

**Causes & Solutions :**
1. Vérifiez que `DIGNA_OIDC_REDIRECT_URI` dans `config.toml` est correct
2. Vérifiez que l'URI de redirection est enregistré dans les paramètres du fournisseur d'identité
3. Assurez-vous que les deux utilisent des URLs identiques (protocole, domaine, chemin)
4. Vérifiez les fautes de frappe dans l'URI de redirection
5. Si vous utilisez HTTPS, assurez-vous que le certificat est valide

---

### Erreur d'identifiants client invalides

**Symptômes :**
- Erreur "Invalid client ID or secret"
- L'authentification échoue avec une erreur d'identifiants

**Causes & Solutions :**
1. Vérifiez que `DIGNA_OIDC_CLIENT_ID` et `DIGNA_OIDC_CLIENT_SECRET` sont corrects
2. Vérifiez qu'il n'y a pas d'espaces supplémentaires ou de caractères indésirables
3. Vérifiez que les identifiants n'ont pas expiré ou été révoqués
4. Redémarrez le service backend après la mise à jour de la configuration
5. Vérifiez sur la console du fournisseur d'identité que les identifiants sont actifs

---

### La connexion bloque ou expire

**Symptômes :**
- Cliquer sur le bouton SSO ne fait rien
- Délai d'attente après quelques secondes
- Le navigateur affiche "Failed to connect" ou message similaire

**Causes & Solutions :**
1. Vérifiez que le backend digna est en cours d'exécution : `digna repo check`
2. Vérifiez la connectivité réseau vers le fournisseur d'identité
3. Vérifiez que `DIGNA_OIDC_CONFIGURATION_URL` est accessible
4. Vérifiez que les règles de pare-feu autorisent les connexions HTTPS sortantes
5. Vérifiez que le backend et le tableau de bord peuvent communiquer entre eux

---

### Les utilisateurs ne sont pas créés automatiquement

**Symptômes :**
- La connexion SSO réussit mais l'utilisateur n'est pas créé dans digna
- Erreur d'autorisation après la connexion SSO

**Causes & Solutions :**
1. Vérifiez que la configuration OIDC est correcte
2. Vérifiez la configuration des permissions utilisateur
3. Consultez les logs de digna pour les messages d'erreur
4. Redémarrez le service backend
5. Contactez support@digna.ai si le problème persiste

---

## Fournisseurs pris en charge {: #supported-providers }

### Testés et pris en charge

Les fournisseurs OIDC suivants ont été testés et fonctionnent :

| Fournisseur | URL de configuration | Guide de configuration |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Documentation Microsoft](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Documentation Google](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Documentation Okta](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Autres fournisseurs OIDC

Tout fournisseur prenant en charge OpenID Connect peut être intégré. Informations requises :

- Client ID
- Client secret
- URL de configuration OpenID (généralement à `/.well-known/openid-configuration`)
- Scopes pris en charge (typiquement `openid profile email`)

Contactez support@digna.ai si vous avez besoin d'aide pour intégrer un fournisseur spécifique.

---

## Bonnes pratiques

✅ **À FAIRE :**
- Utiliser HTTPS en production (pas HTTP)
- Stocker les secrets clients de manière sécurisée (utiliser des variables d'environnement si possible)
- Faire pivoter les secrets périodiquement
- Tester d'abord dans un environnement non production
- Documenter les fournisseurs configurés
- Surveiller les journaux de connexion pour toute activité anormale
- Tenir la configuration du fournisseur d'identité synchronisée avec la configuration digna

❌ **À NE PAS FAIRE :**
- Stocker les secrets clients dans le contrôle de version
- Utiliser des URI de redirection HTTP en production
- Configurer plusieurs fournisseurs avec la même key
- Laisser des identifiants par défaut/de test en production
- Exposer des fichiers de configuration contenant des secrets
- Mélanger des identifiants de développement et de production

---

## Support

Besoin d'aide pour la configuration SSO ?

- 📧 **Email :** support@digna.ai
- 📚 **Documentation :** https://docs.digna.ai
- 🌐 **Site web :** https://www.digna.ai

---

**Dernière mise à jour :** 30 août 2026  
**Version :** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
