---
title: Keycloak SSO – Intégration Single Sign-On | Documentation digna
description: Configurez le Single Sign-On pour digna avec Keycloak via OpenID Connect — configuration du realm et du client, authentification du client, URIs de redirection valides, secret du client et configuration digna correspondante.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, client confidentiel, openid connect, fournisseur d'identité auto-hébergé
---

# Configuration du SSO avec Keycloak

Keycloak est un fournisseur d'identité auto-hébergé, pleinement compatible OIDC. Comme vous l'exécutez vous-même, l'URL de discovery est construite à partir de votre propre nom d'hôte et du realm plutôt que d'un domaine fournisseur.

Ce guide couvre le **côté Keycloak** : création du client et collecte des valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, tests et dépannage — est identique pour tous les fournisseurs et est décrit dans la [Vue d'ensemble du Single Sign-On](overview.md).

---

## Avant de commencer

| Exigence | Remarques |
|---|---|
| **Version de Keycloak** | 17 ou plus pour les chemins d'URL utilisés ici — voir la note à l'étape 4 |
| **Rôle Keycloak** | `realm-admin` sur le realm ciblé, ou un administrateur serveur |
| **Realm** | Le realm auquel appartiennent vos utilisateurs digna, pas nécessairement `master` |
| **URI de redirection digna** | L'URL vers laquelle les utilisateurs reviennent après la connexion, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Sélectionner le realm

1. Ouvrez la console d'administration Keycloak
2. Utilisez le sélecteur de realm en haut à gauche pour passer au realm dans lequel se trouvent vos utilisateurs

!!! warning "N'utilisez pas le realm master"

    Le realm `master` est destiné à l'administration de Keycloak lui-même. Les clients d'application doivent être dans un realm dédié ; placer digna dans `master` donnerait à ses utilisateurs un accès à la console d'administration de Keycloak.

---

## Étape 2 : Créer le client

1. Allez dans **Clients** et cliquez sur **Create client**
2. Configurez :
   - **Client type** : *OpenID Connect*
   - **Client ID** : `digna` — ceci devient `DIGNA_OIDC_CLIENT_ID`
3. Cliquez sur **Next**
4. À l'étape **Capability config**, activez **Client authentication** (**On**)
5. Laissez **Standard flow** activé ; les autres flows ne sont pas nécessaires
6. Cliquez sur **Next**

!!! warning "L'authentification du client doit être activée"

    Si **Client authentication** est désactivé, Keycloak crée un client *public*, qui n'a aucune crédentialisation — l'onglet **Credentials** de l'étape 4 n'existera pas. digna a besoin d'un client confidentiel. Ce réglage peut être modifié après création si vous vous êtes trompé.

---

## Étape 3 : Définir l'URI de redirection

À l'étape **Login settings** (ou dans l'onglet **Settings** ensuite) :

1. **Valid redirect URIs** : saisissez votre URL de callback digna :

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins** : laissez vide, ou mettez `+` pour refléter les redirect URIs
3. Cliquez sur **Save**

!!! tip "Évitez les caractères génériques"

    Keycloak accepte des motifs tels que `https://digna.yourdomain.com/*`. Un caractère générique permet à n'importe quel chemin sur cet hôte de recevoir un code d'autorisation ; préférez donc l'URL de callback exacte.

---

## Étape 4 : Récupérer le secret du client

1. Ouvrez l'onglet **Credentials**
2. Confirmez que **Client Authenticator** est *Client Id and Secret*
3. Copiez le **Client secret** → devient `DIGNA_OIDC_CLIENT_SECRET`

Le secret reste récupérable ici et peut être régénéré avec **Regenerate**.

---

## Étape 5 : Construire l'URL de discovery

Remplacez par votre hôte Keycloak et le nom du realm :

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Par exemple :

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 et versions antérieures incluent /auth"

    Avant Keycloak 17, tous les endpoints étaient sous le préfixe `/auth` :

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Les distributions qui définissent `KC_HTTP_RELATIVE_PATH=/auth` conservent l'ancien agencement même sur les versions récentes. Si l'URL sans `/auth` renvoie 404, essayez avec.

Ouvrez l'URL dans un navigateur avant de continuer. Un document JSON confirme que l'hôte et le realm sont corrects.

---

## Étape 6 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `keycloak` ici. Notez qu'elle n'a pas à être identique au **Client ID** Keycloak, bien que les garder identiques soit plus facile à suivre.

---

## Étape 7 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le tableau de bord. Voir [Testing Login](overview.md#testing-login) pour la liste de contrôle complète.

---

## Dépannage Keycloak

### Invalid parameter: redirect_uri

L'URL de callback n'est pas couverte par **Valid redirect URIs**. Keycloak consigne l'URI reçue dans le journal serveur, ce qui est le moyen le plus rapide pour voir la non-concordance exacte.

### L'onglet Credentials est manquant

Le client est public. Activez **Client authentication** sous **Settings → Capability config**.

### 404 sur l'URL de discovery

Soit le nom du realm est incorrect, soit le déploiement utilise le préfixe `/auth`. Vérifiez la liste des realms dans la console d'administration et essayez les deux formes d'URL.

### unauthorized_client ou invalid_client

Le **Standard flow** est désactivé dans **Capability config**, ou le secret a été régénéré dans Keycloak sans mise à jour de `config.toml`.

### Erreurs de certificat depuis le backend

Un Keycloak auto-hébergé derrière un certificat privé ou autosigné fera échouer l'appel HTTPS sortant de digna vers l'URL de discovery. Installez l'AC émettrice dans le magasin de confiance de la machine exécutant le backend digna.

---

## Voir aussi

- [Vue d'ensemble du Single Sign-On](overview.md) — référence de configuration, tests et dépannage général
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)