---
title: Okta SSO – Intégration Single Sign-On | Documentation digna
description: Configurez le Single Sign-On pour digna avec Okta en utilisant OpenID Connect — intégration de l'application, URIs de redirection après connexion, identifiants client, choix du serveur d'autorisation et la configuration digna correspondante.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, intégration d'application, serveur d'autorisation, openid connect, authentification d'entreprise
---

# Configurer le SSO avec Okta

Okta est compatible OIDC, avec une particularité qui surprend la plupart des intégrations la première fois : une organisation Okta expose plus d'un serveur d'autorisation, et chacun a sa propre URL de découverte.

Ce guide couvre le **côté Okta** : créer l'intégration d'application et collecter les valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, les tests et le dépannage — est le même pour tous les fournisseurs et est décrit dans l'[Aperçu Single Sign-On](overview.md).

---

## Avant de commencer

| Prérequis | Remarques |
|---|---|
| **Rôle Okta** | Super Administrator, ou un rôle administrateur autorisé à créer des intégrations d'application |
| **Domaine Okta** | ex. `yourcompany.okta.com`, ou un domaine personnalisé si configuré |
| **URI de redirection digna** | L'URL à laquelle les utilisateurs reviennent après la connexion, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Créer l'intégration d'application

1. Connectez-vous à la console d'administration Okta
2. Allez dans **Applications → Applications**
3. Cliquez sur **Create App Integration**
4. Sélectionnez :
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Cliquez sur **Next**

!!! warning "Le type d'application ne peut pas être modifié"

    Choisir *Single-Page Application* au lieu de *Web Application* crée un client public sans secret, et l'échange côté backend de digna échouera avec `invalid_client`. Le type est figé à la création — un mauvais choix implique de supprimer l'application et de recommencer.

---

## Étape 2 : Configurer l'intégration

1. **App integration name** : `digna`
2. **Grant type** : laissez *Authorization Code* sélectionné
3. **Sign-in redirect URIs** : saisissez l'URL de callback de digna :

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs** : facultatif
5. Sous **Assignments**, choisissez qui peut utiliser l'intégration — un groupe spécifique est plus sûr que *Allow everyone in your organization to access*
6. Cliquez sur **Save**

!!! note "L'affectation est requise"

    Okta authentifie l'utilisateur puis vérifie s'il est affecté à l'application. Un utilisateur non affecté arrive à la page de connexion Okta, s'authentifie correctement, puis se voit refuser l'accès lors de la redirection de retour. Si la connexion fonctionne pour vous mais pas pour des collègues, l'affectation est la première chose à vérifier.

---

## Étape 3 : Récupérer les identifiants

Dans l'onglet **General** de l'application, sous **Client Credentials** :

- **Client ID** → devient `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → devient `DIGNA_OIDC_CLIENT_SECRET` (cliquez sur l'icône œil pour révéler)

---

## Étape 4 : Choisir le serveur d'autorisation

C'est l'étape qui détermine votre URL de découverte. Allez dans **Security → API** pour voir les serveurs d'autorisation dans votre organisation.

**Org authorization server** — émet des jetons pour l'organisation Okta elle-même :

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — y compris celui qu'Okta crée appelé `default` :

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Pour le serveur intégré, `<auth_server_id>` est littéralement `default` :

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Lequel ?"

    Utilisez le serveur d'autorisation **org** sauf si votre organisation standardise déjà sur un serveur personnalisé pour des politiques d'accès API. Les comptes Okta Developer ont `default` par défaut ; beaucoup d'organisations d'entreprise le désactivent. Ouvrez les deux URLs dans un navigateur — celle qui renvoie du JSON plutôt qu'une erreur est celle qui vous est disponible.

---

## Étape 5 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `okta` ici.

---

## Étape 6 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le tableau de bord. Voir [Tests de connexion](overview.md#testing-login) pour la checklist complète.

---

## Dépannage Okta

### L'URI de redirection n'est pas enregistrée

Okta indique l'URI en cause dans l'erreur. Comparez-la avec **General → Sign-in redirect URIs** ; Okta fait correspondre la chaîne complète, y compris tout slash final.

### L'utilisateur n'est pas affecté à l'application cliente

Le compte n'est pas dans la liste d'affectation de l'application. Ajoutez l'utilisateur ou son groupe sous **Assignments**.

### 400 Bad Request : Invalid Authorization Server

Le `<auth_server_id>` dans l'URL de découverte n'existe pas, le plus fréquent étant `default` sur une organisation où il a été supprimé. Vérifiez **Security → API** pour connaître les serveurs réellement disponibles.

### invalid_client à l'étape du token

L'intégration a été créée comme Single-Page Application et n'a pas de secret client. Recréez-la en tant que Web Application.

---

## Voir aussi

- [Aperçu Single Sign-On](overview.md) — référence de configuration, tests et dépannage général
- [Okta : OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)