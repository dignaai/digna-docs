---
title: Auth0 SSO – Intégration Single Sign-On | documentation digna
description: Configurez le Single Sign-On pour digna avec Auth0 en utilisant OpenID Connect — configuration pour Regular Web Applications, URL de callback autorisées, identifiants client, domaine du tenant et configuration digna correspondante.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regular web application, callback urls, openid connect, authentification d'entreprise
---

# Configurer le SSO avec Auth0

Auth0 est compatible OIDC et expose un endpoint de découverte par tenant. L'élément principal à bien configurer est le domaine du tenant, qui apparaît dans l'URL de découverte et change si vous activez un domaine personnalisé.

Ce guide couvre le **côté Auth0** : création de l'application et collecte des valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, tests et dépannage — est identique pour tous les fournisseurs et est décrit dans la [Single Sign-On Overview](overview.md).

---

## Avant de commencer

| Exigence | Remarques |
|---|---|
| **Rôle Auth0** | Administrateur du tenant |
| **Domaine du tenant** | ex. `yourcompany.eu.auth0.com` — le segment régional est important |
| **URI de redirection digna** | L'URL vers laquelle les utilisateurs reviennent après l'authentification, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Créer l'application

1. Connectez-vous au [Auth0 Dashboard](https://manage.auth0.com)
2. Allez dans **Applications → Applications**
3. Cliquez sur **Create Application**
4. Nommez-la `digna` et choisissez **Regular Web Applications**
5. Cliquez sur **Create**

!!! warning "Choisir Regular Web Applications"

    *Single Page Application* et *Native* créent des clients publics sans secret. digna effectue l'échange de code depuis son backend et a besoin d'un client confidentiel, donc **Regular Web Applications** est le bon type. Contrairement à certains fournisseurs, Auth0 permet de changer le type plus tard via **Settings → Application Type**.

---

## Étape 2 : Ajouter l'URL de callback

Dans l'onglet **Settings** de l'application :

1. Trouvez **Allowed Callback URLs**
2. Saisissez votre URL de callback digna :

```
https://digna.yourdomain.com/oidc/callback
```

3. Facultativement, définissez **Allowed Logout URLs** sur l'URL de votre dashboard
4. Descendez en bas de la page et cliquez sur **Save Changes**

!!! note "Séparé par des virgules, pas par des retours à la ligne"

    Auth0 accepte plusieurs URL de callback dans ce champ, séparées par des virgules. Une liste séparée uniquement par des retours à la ligne est lue comme une seule URL mal formée et ne correspondra silencieusement à rien.

---

## Étape 3 : Récupérer les identifiants

Toujours dans **Settings**, dans le panneau **Basic Information** :

- **Domain** → est utilisé pour l'URL de découverte
- **Client ID** → devient `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → devient `DIGNA_OIDC_CLIENT_SECRET` (cliquez pour le révéler)

---

## Étape 4 : Confirmer le type de grant

1. Allez dans **Settings → Advanced Settings → Grant Types**
2. Confirmez que **Authorization Code** est coché

Il est activé par défaut pour les Regular Web Applications. S'il a été décoché, la connexion de digna échoue avec `unauthorized_client`.

---

## Étape 5 : Construire l'URL de découverte

Remplacez le **Domain** de l'étape 3 :

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Par exemple :

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Les domaines personnalisés modifient l'issuer"

    Si votre tenant utilise un domaine personnalisé tel que `login.yourcompany.com`, utilisez ce domaine dans l'URL de découverte. Mélanger les deux — le domaine canonique dans l'URL de découverte et le domaine personnalisé dans le navigateur — provoque un mismatch d'issuer, et le token est rejeté après une connexion par ailleurs réussie.

---

## Étape 6 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `auth0` ici.

---

## Étape 7 : Test

Redémarrez le backend et le serveur web, puis ouvrez le dashboard. Voir [Testing Login](overview.md#testing-login) pour la checklist complète.

---

## Dépannage Auth0

### Mismatch d'URL de callback

La page d'erreur d'Auth0 indique l'URL qu'elle a reçue. Ajoutez-la à **Allowed Callback URLs**, en vérifiant que les entrées sont séparées par des virgules.

### unauthorized_client

**Authorization Code** n'est pas activé sous **Advanced Settings → Grant Types**, ou le type d'application n'est pas Regular Web Applications.

### Accès refusé après une connexion réussie

Une Rule, Action ou trigger Post-Login dans le tenant rejette l'utilisateur. Vérifiez **Actions → Flows → Login** et les logs du tenant sous **Monitoring → Logs**, qui indiquent la raison exacte.

### Mismatch d'issuer

L'URL de découverte et le domaine vers lequel le navigateur a été redirigé diffèrent — généralement le domaine canonique du tenant versus un domaine personnalisé. Utilisez un seul domaine de manière cohérente.

---

## Voir aussi

- [Single Sign-On Overview](overview.md) — référence de configuration, tests et dépannage général
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)