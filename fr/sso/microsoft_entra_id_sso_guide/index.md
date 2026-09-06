# Configurer la connexion unique (SSO) avec Microsoft Entra ID

Microsoft Entra ID (anciennement Azure Active Directory) est un fournisseur pleinement compatible OIDC, donc digna s'intègre via le point de découverte standard.

Ce guide couvre le **côté Entra ID** : l'enregistrement de l'application et la collecte des quatre valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, les tests et le dépannage — est identique pour tous les fournisseurs et est décrit dans l'[Aperçu de la connexion unique](overview.md).

---

## Avant de commencer

| Exigence | Remarques |
|---|---|
| **Rôle Entra ID** | Application Administrator, Cloud Application Administrator, ou Global Administrator |
| **URI de redirection digna** | L'URL vers laquelle les utilisateurs reviennent après la connexion, p.ex. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | L'annuaire dans lequel vos utilisateurs se connectent |

---

## Étape 1 : Enregistrer l'application

1. Connectez-vous au [centre d'administration Microsoft Entra](https://entra.microsoft.com)
2. Allez dans **Identity → Applications → App registrations**
3. Cliquez sur **New registration**
4. Configurez :
   - **Name** : `digna` (affiché aux utilisateurs sur l'écran de consentement)
   - **Supported account types** : *Accounts in this organizational directory only* pour un déploiement mono-tenant
5. Sous **Redirect URI**, sélectionnez la plateforme **Web** et saisissez votre URL de callback digna :

```
https://digna.yourdomain.com/oidc/callback
```

6. Cliquez sur **Register**

!!! warning "Important"

    La plateforme doit être **Web**, pas *Single-page application*. digna échange le code d'autorisation depuis le backend en utilisant un client secret, ce que le type de plateforme SPA n'autorise pas.

---

## Étape 2 : Récupérer les ID Client et Tenant

Sur la page **Overview** de l'application, copiez :

- **Application (client) ID** → devient `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → sert dans l'URL de découverte

---

## Étape 3 : Créer un Client Secret

1. Allez dans **Certificates & secrets → Client secrets**
2. Cliquez sur **New client secret**
3. Entrez une description et choisissez une durée d'expiration
4. Cliquez sur **Add**
5. Copiez immédiatement la colonne **Value**

!!! warning "Copiez la colonne Value, pas le Secret ID"

    La **Value** est affichée une seule fois, sur cette page, et ne peut pas être récupérée ultérieurement. Le **Secret ID** à côté ressemble à la Value mais n'est pas le secret — l'utiliser génère une erreur `invalid_client` lors de la connexion. Si vous quittez la page avant d'avoir copié, supprimez le secret et créez-en un nouveau.

!!! tip "Astuce"

    Entra ID limite la durée de vie des secrets à 24 mois, donc chaque intégration SSO a une date d'expiration. Notez-la quelque part où vous la verrez — un secret expiré coupe l'accès SSO pour tous les utilisateurs en même temps, sans avertissement sur la page de connexion.

---

## Étape 4 : Confirmer les autorisations d'API

1. Allez dans **API permissions**
2. Confirmez que **Microsoft Graph → User.Read** (délégué) est présent — il est ajouté par défaut

Les scopes `openid`, `profile` et `email` que digna demande font partie de l'ensemble OIDC standard et n'ont pas besoin d'une autorisation séparée. Si votre tenant exige le consentement administrateur pour toutes les applications, cliquez sur **Grant admin consent for <tenant>**.

---

## Étape 5 : Construire l'URL de découverte

Substituez le **Directory (tenant) ID** de l'Étape 2 :

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Utilisez le point de terminaison v2.0"

    Le segment `/v2.0/` est important. Le point de terminaison v1.0 à `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` délivre des tokens dans un format plus ancien et ne renvoie pas les claims OIDC standard que digna attend.

Ouvrez l'URL dans un navigateur avant de continuer. Un document JSON confirme que l'ID du tenant est correct.

---

## Étape 6 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `microsoft` ici.

---

## Étape 7 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le tableau de bord. Voir [Test de connexion](overview.md#testing-login) pour la liste de vérification complète.

---

## Dépannage Entra ID

### AADSTS50011 : Incompatibilité de l'URI de redirection

L'URI dans `DIGNA_OIDC_REDIRECT_URI` diffère de celui enregistré à l'étape 1. Entra ID compare la chaîne complète, donc une barre oblique finale, `http` versus `https`, ou un port différent comptent tous comme une incompatibilité. Vérifiez **Authentication → Web → Redirect URIs**.

### AADSTS7000215 : Client Secret invalide

Soit le **Secret ID** a été copié au lieu de la **Value**, soit le secret a expiré. Créez un nouveau secret et copiez la colonne Value.

### AADSTS650057 : Resource invalide

L'enregistrement de l'application a été supprimé ou appartient à un tenant différent de celui indiqué dans l'URL de découverte. Confirmez le Directory (tenant) ID sur la page Overview.

### Les utilisateurs se connectent mais rien ne se passe

Si le tenant nécessite un consentement administrateur et qu'il n'a pas été accordé, la redirection revient sans token exploitable. Accordez le consentement administrateur sous **API permissions**.

---

## Voir aussi

- [Aperçu de la connexion unique](overview.md) — référence de configuration, tests et dépannage général
- [Microsoft : Flux d'autorisation OAuth 2.0](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)