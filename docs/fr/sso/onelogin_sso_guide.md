---
title: OneLogin SSO – Intégration Single Sign-On | Documentation digna
description: Configurer le Single Sign-On pour digna avec OneLogin en utilisant OpenID Connect — création de l'application OIDC, URIs de redirection, identifiants client, authentification du token endpoint et configuration correspondante de digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, authentification du token endpoint, authentification d'entreprise
---

# Configurer le SSO avec OneLogin

OneLogin est compatible OIDC. Sa caractéristique distinctive est que le type de connecteur est choisi depuis un catalogue lors de la création de l'application et ne peut pas être modifié ensuite.

Ce guide couvre le **côté OneLogin** : création de l'application et collecte des valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, tests et dépannage — est identique pour tous les fournisseurs et est décrit dans l'[Aperçu du Single Sign-On](overview.md).

---

## Avant de commencer

| Exigence | Remarques |
|---|---|
| **Rôle OneLogin** | Propriétaire du compte ou administrateur autorisé à ajouter des applications |
| **Sous-domaine** | ex. `yourcompany.onelogin.com` |
| **URI de redirection digna** | L'URL vers laquelle les utilisateurs reviennent après la connexion, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Créer l'application OIDC

1. Connectez-vous au portail d'administration OneLogin
2. Allez dans **Applications → Applications**
3. Cliquez sur **Add App**
4. Recherchez `OpenId Connect` et sélectionnez le connecteur **OpenId Connect (OIDC)**
5. Définissez le **Display Name** sur `digna`
6. Cliquez sur **Save**

!!! warning "Le type de connecteur est fixé lors de la création"

    OneLogin propose des entrées de catalogue distinctes pour SAML et OIDC, et une application ne peut pas être convertie de l'une à l'autre. Si vous choisissez par erreur un connecteur SAML, supprimez l'application et ajoutez-la de nouveau — il n'existe pas de paramètre pour changer de protocole.

---

## Étape 2 : Configurer l'URI de redirection

1. Ouvrez l'onglet **Configuration**
2. Dans **Redirect URI's**, saisissez votre URL de callback digna :

```
https://digna.yourdomain.com/oidc/callback
```

3. Facultativement, définissez **Post Logout Redirect URIs** sur l'URL de votre dashboard
4. Cliquez sur **Save**

!!! note "Une URI par ligne"

    Contrairement aux fournisseurs qui attendent une liste séparée par des virgules, le champ **Redirect URI's** de OneLogin accepte une URI par ligne.

---

## Étape 3 : Définir le type d'application et la méthode d'authentification

1. Ouvrez l'onglet **SSO**
2. Vérifiez que **Application Type** est *Web*
3. Définissez **Token Endpoint → Authentication Method** sur *POST* (`client_secret_post`) ou *Basic* (`client_secret_basic`)

!!! warning "Ne choisissez pas 'None'"

    Définir la méthode d'authentification sur *None* rend l'application cliente publique sans secret, et l'échange de code côté backend de digna sera rejeté. Soit POST soit Basic fonctionne.

---

## Étape 4 : Récupérer les identifiants

Toujours dans l'onglet **SSO** :

- **Client ID** → devient `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → devient `DIGNA_OIDC_CLIENT_SECRET` (cliquez sur **Show client secret**)

La page affiche également l'**Issuer URL**, qui confirme l'URL de discovery à l'étape suivante.

---

## Étape 5 : Affecter des utilisateurs

1. Ouvrez l'onglet **Access**
2. Ajoutez les rôles ou groupes dont les membres pourront utiliser digna
3. Cliquez sur **Save**

!!! note "Les utilisateurs non affectés sont refusés après la connexion"

    Comme pour la plupart des fournisseurs, OneLogin authentifie d'abord l'utilisateur puis vérifie l'attribution d'accès. Un utilisateur non affecté s'authentifie avec succès puis se voit refuser l'accès, ce qui ressemble à une erreur digna plutôt qu'à une décision de contrôle d'accès.

---

## Étape 6 : Construire l'URL de discovery

Substituez votre sous-domaine OneLogin :

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Par exemple :

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "Le /2 correspond à la version de l'API"

    L'implémentation OIDC actuelle de OneLogin se trouve sous `/oidc/2/`. Des documents plus anciens montrent `/oidc/` sans version, qui pointe vers la première version retirée. Vérifiez l'**Issuer URL** dans l'onglet SSO en cas de doute — l'URL de discovery est l'issuer suivi de `/.well-known/openid-configuration`.

---

## Étape 7 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `onelogin` ici.

---

## Étape 8 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le dashboard. Voir [Test de connexion](overview.md#testing-login) pour la liste de vérification complète.

---

## Dépannage OneLogin

### redirect_uri did not match

L'URL de callback est absente de **Configuration → Redirect URI's**, ou les entrées ont été séparées par des virgules au lieu de nouvelles lignes.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** est réglé sur *None*, ou le client secret dans `config.toml` est périmé. Affichez le secret dans l'onglet **SSO** et comparez.

### L'application n'apparaît pas pour les utilisateurs

Aucun rôle ni groupe n'a été autorisé sur l'onglet **Access**.

### 404 sur l'URL de discovery

Le sous-domaine est incorrect, ou l'URL omet `/oidc/2/`. Comparez avec l'**Issuer URL** affiché dans l'onglet SSO.

---

## Voir aussi

- [Aperçu du Single Sign-On](overview.md) — référence de configuration, tests et dépannage général
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)