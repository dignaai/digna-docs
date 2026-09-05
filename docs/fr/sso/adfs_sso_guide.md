---
title: AD FS SSO – Intégration Single Sign-On | documentation digna
description: Configurez le Single Sign-On pour digna avec Active Directory Federation Services en utilisant OpenID Connect — groupe d'applications, application serveur, secret partagé, scopes autorisés et la configuration correspondante pour digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, Active Directory Federation Services, adfs oidc, groupe d'applications, OpenID Connect, fournisseur d'identité sur site
---

# Configurer le SSO avec AD FS

Active Directory Federation Services est l'option sur site : vos propres serveurs émettent les jetons, et l'URL de découverte est votre propre nom d'hôte. AD FS prend en charge OpenID Connect à partir de **Windows Server 2016**.

Ce guide couvre le **côté AD FS** : création du groupe d'applications et collecte des valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, tests et dépannage — est identique pour tous les fournisseurs et est décrit dans la [Vue d'ensemble du Single Sign-On](overview.md).

---

## Avant de commencer

| Prérequis | Remarques |
|---|---|
| **Version d'AD FS** | Windows Server 2016 ou ultérieur — les versions antérieures ne supportent pas OIDC |
| **Accès** | Administrateur local sur le serveur AD FS |
| **Nom du service de fédération** | ex. `adfs.yourdomain.com` |
| **URI de redirection digna** | L'URL vers laquelle les utilisateurs reviennent après la connexion, ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Créer le groupe d'applications

1. Sur le serveur AD FS, ouvrez **AD FS Management**
2. Clic droit sur **Application Groups** et choisissez **Add Application Group**
3. Entrez `digna` comme nom
4. Sous **Standalone applications** — ou **Client-Server applications** selon votre version — sélectionnez **Server application accessing a web API**
5. Cliquez sur **Next**

---

## Étape 2 : Configurer l'application serveur

1. **Nom** : `digna backend`
2. **Client Identifier** : AD FS génère un GUID. Copiez-le — il devient `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI** : entrez votre URL de callback digna et cliquez sur **Add** :

```
https://digna.yourdomain.com/oidc/callback
```

4. Cliquez sur **Next**

!!! warning "Cliquez sur Ajouter, pas seulement sur Suivant"

    Le champ de l'URI de redirection a son propre bouton **Add**. Taper une URI et cliquer sur **Next** sans appuyer sur **Add** la supprime, et l'assistant n'affiche aucun avertissement. Vérifiez que l'URI apparaît dans la liste sous le champ avant de continuer.

---

## Étape 3 : Générer le secret partagé

1. Cochez **Generate a shared secret**
2. Copiez le secret généré → il devient `DIGNA_OIDC_CLIENT_SECRET`
3. Cliquez sur **Next**

!!! warning "Le secret n'est affiché qu'une seule fois"

    AD FS affiche le secret partagé uniquement sur cette page de l'assistant et ne peut pas le réafficher. Si vous le perdez, réinitialisez-le plus tard depuis les propriétés du groupe d'applications.

---

## Étape 4 : Configurer l'API Web

1. **Identifier** : entrez le même client identifier que dans l'Étape 2 et cliquez sur **Add**
2. Cliquez sur **Next**
3. Choisissez une **Access Control Policy** — *Permit everyone* est le plus simple pour commencer ; restreignez-la à un groupe en production
4. Cliquez sur **Next**

---

## Étape 5 : Accorder les scopes autorisés

À l'étape **Configure Application Permissions**, cochez :

- `openid`
- `profile`
- `email`

Puis cliquez sur **Next** et terminez l'assistant.

!!! warning "openid n'est pas coché par défaut"

    AD FS pré-sélectionne parfois seulement `user_impersonation`. Sans `openid`, le endpoint des jetons renvoie un jeton d'accès OAuth plutôt qu'un ID token, et digna ne peut pas identifier l'utilisateur.

---

## Étape 6 : Confirmer l'URL de découverte

Substituez votre nom de service de fédération :

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Par exemple :

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Ouvrez cette URL dans un navigateur. Un document JSON confirme qu'OIDC est activé et que le nom d'hôte est correct.

!!! note "Le backend doit faire confiance au certificat"

    Une autorité de certification interne est courante pour AD FS. La machine exécutant le backend digna effectue elle-même un appel HTTPS sortant vers cette URL, donc l'AC émettrice doit être présente dans le magasin de confiance de cette machine — pas seulement dans les navigateurs des personnes qui se connectent.

---

## Étape 7 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `adfs` ici.

---

## Étape 8 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le dashboard. Voir [Tester la connexion](overview.md#testing-login) pour la liste complète de contrôle.

---

## Dépannage AD FS

### MSIS9611 : The Client Is Not Allowed to Access the Resource

L'identifiant de l'API Web de l'Étape 4 ne correspond pas à l'identifiant du client, ou les scopes de l'Étape 5 n'ont pas été accordés. Les deux sont modifiables depuis les propriétés du groupe d'applications.

### MSIS9602 : Invalid redirect_uri

L'URI a été tapée mais non ajoutée avec le bouton **Add**, ou diffère de `DIGNA_OIDC_REDIRECT_URI`. Vérifiez **Application Groups → digna → digna backend → Properties**.

### Aucun ID Token n'est renvoyé

Le scope `openid` est manquant dans les permissions de l'application.

### Le backend ne peut pas atteindre l'URL de découverte

Soit le DNS sur l'hôte backend ne résout pas le nom du service de fédération, soit le certificat AD FS n'est pas approuvé sur cette machine. Testez avec `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` depuis le serveur digna lui-même.

### Événements à vérifier

Le serveur AD FS enregistre les échecs dans **Applications and Services Logs → AD FS → Admin** dans l'Observateur d'événements, généralement avec une raison plus précise que celle affichée par le navigateur.

---

## Voir aussi

- [Vue d'ensemble du Single Sign-On](overview.md) — référence de configuration, tests et dépannage général
- [Microsoft : Scénarios OpenID Connect pour AD FS](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)