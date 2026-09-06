# Set up SSO with Google Workspace

Google's identity platform is OIDC-compliant and uses a single, well-known discovery URL for every customer, so the only per-organization values are the client ID and secret.

This guide covers the **Google side**: creating the OAuth client and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **Google Cloud project** | Any project in the same organization as your Workspace domain |
| **Role** | Editor or Owner on the project |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Configure the OAuth Consent Screen

Google will not issue credentials until the consent screen exists.

1. Open the [Google Cloud Console](https://console.cloud.google.com) and select your project
2. Go to **APIs & Services → OAuth consent screen**
3. Choose the user type:
   - **Internal** — only accounts in your Workspace domain can log in. Recommended.
   - **External** — any Google account can attempt to log in.
4. Fill in the app name, user support email and developer contact email
5. On the **Scopes** step, add `openid`, `.../auth/userinfo.email` and `.../auth/userinfo.profile`
6. Save

!!! warning "External Apps Must Be Published"

    An **External** consent screen starts in *Testing* status, where only accounts explicitly added to the test-user list can complete a login. Everyone else sees "digna has not completed the Google verification process". Either switch the app to **In production** under **Publishing status**, or use **Internal** — which has no such restriction and is the right choice for a Workspace-only deployment.

---

## Step 2: Create the OAuth Client

1. Go to **APIs & Services → Credentials**
2. Click **Create Credentials → OAuth client ID**
3. Set **Application type** to **Web application**
4. Give it a name, e.g. `digna`
5. Under **Authorized redirect URIs**, click **Add URI** and enter:

```
https://digna.yourdomain.com/oidc/callback
```

6. Click **Create**

!!! note "Authorized JavaScript Origins Are Not Needed"

    digna exchanges the authorization code from the backend, not the browser, so the **Authorized JavaScript origins** field can be left empty. Only the redirect URI matters.

---

## Step 3: Collect the Credentials

The dialog that appears after creation shows:

- **Client ID** — ends in `.apps.googleusercontent.com` → becomes `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → becomes `DIGNA_OIDC_CLIENT_SECRET`

Both remain retrievable later from the credential's detail page, unlike most other providers.

---

## Step 4: The Discovery URL

Google uses one discovery URL for all customers — there is nothing to substitute:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Step 5: Configure digna

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

The `key` in both files must match — `google` here.

---

## Step 6: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting Google Workspace

### Error 400: redirect_uri_mismatch

The URI in `DIGNA_OIDC_REDIRECT_URI` is not in the **Authorized redirect URIs** list, or differs by a trailing slash or scheme. Google's error page shows the URI it received — compare it character for character with the registered one.

### This App Is Blocked / Has Not Completed Verification

The consent screen is **External** and still in *Testing*. Publish it, or switch the app to **Internal**.

### Access Blocked: Authorization Error

The account attempting to log in is outside your Workspace domain while the consent screen is **Internal**. This is the intended behaviour — Internal apps accept only accounts in the organization.

### Changes Take Several Minutes

Google propagates credential and consent-screen changes asynchronously. A newly added redirect URI can take a few minutes to take effect; if a change looks ignored, wait and retry before investigating further.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)