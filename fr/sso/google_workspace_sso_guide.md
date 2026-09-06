# Configurer l'authentification unique (SSO) avec Google Workspace

La plateforme d'identité de Google est compatible OIDC et utilise une URL de découverte unique et bien connue pour tous les clients ; les seules valeurs propres à chaque organisation sont l'ID client et le secret.

Ce guide couvre le **côté Google** : création du client OAuth et collecte des valeurs nécessaires à digna. Le côté digna — `dashboard_config.toml`, tests et dépannage — est identique pour tous les fournisseurs et est décrit dans la [Présentation de l'authentification unique](overview.md).

---

## Avant de commencer

| Exigence | Remarques |
|---|---|
| **Projet Google Cloud** | N'importe quel projet dans la même organisation que votre domaine Workspace |
| **Rôle** | Éditeur ou Propriétaire sur le projet |
| **URI de redirection digna** | L'URL vers laquelle les utilisateurs reviennent après la connexion, p. ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Configurer l'écran de consentement OAuth

Google n'émettra pas d'identifiants tant que l'écran de consentement n'existe pas.

1. Ouvrez la [Google Cloud Console](https://console.cloud.google.com) et sélectionnez votre projet
2. Allez dans **APIs & Services → OAuth consent screen**
3. Choisissez le type d'utilisateur :
   - **Internal** — seuls les comptes de votre domaine Workspace peuvent se connecter. Recommandé.
   - **External** — tout compte Google peut tenter de se connecter.
4. Remplissez le nom de l'application, l'email de support utilisateur et l'email de contact développeur
5. À l'étape **Scopes**, ajoutez `openid`, `.../auth/userinfo.email` et `.../auth/userinfo.profile`
6. Enregistrez

!!! warning "Les applications externes doivent être publiées"

    Un écran de consentement **External** commence en statut *Testing*, où seuls les comptes ajoutés explicitement à la liste des testeurs peuvent compléter une connexion. Tous les autres voient le message « digna has not completed the Google verification process ». Passez l'application en **In production** sous **Publishing status**, ou utilisez **Internal** — qui n'a pas cette restriction et est le bon choix pour un déploiement réservé à Workspace.

---

## Étape 2 : Créer le client OAuth

1. Allez dans **APIs & Services → Credentials**
2. Cliquez sur **Create Credentials → OAuth client ID**
3. Définissez **Application type** sur **Web application**
4. Donnez-lui un nom, p. ex. `digna`
5. Sous **Authorized redirect URIs**, cliquez sur **Add URI** et saisissez :

```
https://digna.yourdomain.com/oidc/callback
```

6. Cliquez sur **Create**

!!! note "Les Authorized JavaScript Origins ne sont pas nécessaires"

    digna échange le code d'autorisation depuis le backend, pas depuis le navigateur, donc le champ **Authorized JavaScript origins** peut rester vide. Seule l'URI de redirection compte.

---

## Étape 3 : Récupérer les identifiants

La boîte de dialogue qui apparaît après la création affiche :

- **Client ID** — se termine par `.apps.googleusercontent.com` → devient `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → devient `DIGNA_OIDC_CLIENT_SECRET`

Les deux restent récupérables plus tard depuis la page de détails des identifiants, contrairement à la plupart des autres fournisseurs.

---

## Étape 4 : L'URL de découverte

Google utilise une URL de découverte unique pour tous les clients — rien à remplacer :

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Étape 5 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `google` ici.

---

## Étape 6 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le dashboard. Voir [Tester la connexion](overview.md#testing-login) pour la liste de contrôle complète.

---

## Dépannage Google Workspace

### Erreur 400 : redirect_uri_mismatch

L'URI dans `DIGNA_OIDC_REDIRECT_URI` n'est pas dans la liste **Authorized redirect URIs**, ou diffère par un slash final ou le schéma. La page d'erreur de Google affiche l'URI reçue — comparez-la caractère par caractère avec celle enregistrée.

### This App Is Blocked / Has Not Completed Verification

L'écran de consentement est **External** et est toujours en *Testing*. Publiez-le, ou passez l'application en **Internal**.

### Access Blocked: Authorization Error

Le compte qui tente de se connecter est en dehors de votre domaine Workspace alors que l'écran de consentement est **Internal**. C'est le comportement prévu — les applications Internal n'acceptent que les comptes de l'organisation.

### Les changements prennent plusieurs minutes

Google propage les modifications des identifiants et de l'écran de consentement de manière asynchrone. Un nouvel URI de redirection peut mettre quelques minutes à être effectif ; si un changement semble ignoré, attendez et réessayez avant d'aller plus loin dans le diagnostic.

---

## Voir aussi

- [Présentation de l'authentification unique](overview.md) — référence de configuration, tests et dépannage général
- [Google : OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)