# Configurer l'authentification unique (SSO) avec PingOne

PingOne est compatible OIDC. Deux valeurs nécessitent de l'attention : l'**Environment ID** (identifiant d'environnement), qui apparaît dans chaque URL d'endpoint, et le **domaine régional**, qui diffère entre les locataires nord-américain, européen, canadien, Asie-Pacifique et australien.

Ce guide couvre le **côté PingOne** : création de l'application et collecte des valeurs dont digna a besoin. Le côté digna — `dashboard_config.toml`, les tests et le dépannage — est identique pour tous les fournisseurs et est décrit dans la [Présentation de l'authentification unique](overview.md).

---

## Avant de commencer

| Prérequis | Remarques |
|---|---|
| **Rôle PingOne** | Environment Admin ou Identity Data Admin sur l'environnement ciblé |
| **Environnement** | L'environnement PingOne auquel appartiennent vos utilisateurs digna |
| **URI de redirection digna** | L'URL de retour des utilisateurs après connexion, p. ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Étape 1 : Créer l'application

1. Connectez-vous à la console d'administration PingOne et sélectionnez votre environnement
2. Allez dans **Applications → Applications**
3. Cliquez sur le bouton **+**
4. Saisissez `digna` comme **Application Name**
5. Sélectionnez **OIDC Web App**
6. Cliquez sur **Save**

!!! warning "Choisissez OIDC Web App, pas Single-Page App"

    *Single-Page App* et *Native App* créent des clients publics incapables de conserver un secret. digna échange le code d'autorisation depuis son backend et a besoin du type confidentiel **OIDC Web App**.

---

## Étape 2 : Configurer l'URI de redirection

1. Ouvrez l'onglet **Configuration** de l'application
2. Cliquez sur l'icône du crayon pour modifier
3. Confirmez que **Response Type** est *Code* et que **Grant Type** est *Authorization Code*
4. Sous **Redirect URIs**, saisissez votre URL de callback digna :

```
https://digna.yourdomain.com/oidc/callback
```

5. Définissez **Token Endpoint Authentication Method** sur *Client Secret Post* ou *Client Secret Basic*
6. Cliquez sur **Save**

---

## Étape 3 : Activer l'application

Sur la ligne ou le panneau de détail de l'application, basculez l'interrupteur sur **enabled**.

!!! warning "Les nouvelles applications démarrent désactivées"

    PingOne crée les applications en état désactivé. Une application désactivée produit une erreur à l'étape d'autorisation qui ne mentionne pas l'interrupteur, il est donc utile de vérifier cela avant de dépanner autre chose.

---

## Étape 4 : Accorder les scopes

1. Ouvrez l'onglet **Resources**
2. Confirmez que `openid` est accordé, et ajoutez `profile` et `email` depuis la ressource **OpenID Connect**
3. Cliquez sur **Save**

---

## Étape 5 : Assigner les utilisateurs

1. Ouvrez l'onglet **Access**
2. Ajoutez la population ou les groupes dont les membres peuvent utiliser digna
3. Cliquez sur **Save**

---

## Étape 6 : Récupérer les identifiants et l'Environment ID

Dans l'onglet **Configuration**, développez **General** :

- **Client ID** → devient `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → devient `DIGNA_OIDC_CLIENT_SECRET` (cliquez sur l'icône œil)
- **Environment ID** → entre dans l'URL de discovery

Le même onglet liste l'**OIDC Discovery Endpoint** prêt à l'emploi, que vous pouvez copier directement au lieu de le composer manuellement.

---

## Étape 7 : Construire l'URL de discovery

Substituez l'identifiant d'environnement et le domaine correspondant à votre région :

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Région | Domaine |
|---|---|
| North America | `auth.pingone.com` |
| Europe | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Pour un environnement européen :

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Copiez-le plutôt que de le retaper"

    Le domaine régional est l'erreur la plus fréquente dans une intégration PingOne, et une région erronée renvoie un 404 plutôt qu'un message utile. Utilisez la valeur **OIDC Discovery Endpoint** de l'Étape 6.

---

## Étape 8 : Configurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Se connecter avec PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

La `key` dans les deux fichiers doit correspondre — `pingone` ici.

---

## Étape 9 : Tester

Redémarrez le backend et le serveur web, puis ouvrez le dashboard. Voir [Test de connexion](overview.md#testing-login) pour la checklist complète.

---

## Dépannage PingOne

### 404 sur l'URL de discovery

Le domaine régional ou l'identifiant d'environnement est incorrect. Comparez avec l'**OIDC Discovery Endpoint** affiché dans l'onglet Configuration de l'application.

### NOT_FOUND ou application désactivée

L'interrupteur de l'application de l'Étape 3 est toujours désactivé.

### Incohérence de l'URI de redirection

PingOne compare la chaîne complète. Vérifiez **Configuration → Redirect URIs** pour une barre oblique finale ou une différence de schéma.

### Connexion réussie mais aucune revendication email n'atteint digna

Les scopes `email` et `profile` n'ont pas été accordés dans l'onglet **Resources**.

### L'utilisateur ne voit pas l'application

Aucune population ou groupe n'a reçu d'accès dans l'onglet **Access**.

---

## Voir aussi

- [Présentation de l'authentification unique](overview.md) — référence de configuration, tests et dépannage général
- [PingOne : configuration de l'application OIDC](https://docs.pingidentity.com/pingone/)