# Set up SSO with Keycloak

Keycloak is a self-hosted, fully OIDC-compliant identity provider. Because you run it yourself, the discovery URL is built from your own host name and realm rather than a vendor domain.

This guide covers the **Keycloak side**: creating the client and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **Keycloak version** | 17 or later for the URL paths used here — see the note in Step 4 |
| **Keycloak role** | `realm-admin` on the target realm, or a server administrator |
| **Realm** | The realm your digna users belong to, not necessarily `master` |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Select the Realm

1. Open the Keycloak admin console
2. Use the realm selector in the top-left to switch to the realm your users are in

!!! warning "Do Not Use the master Realm"

    The `master` realm is intended for administering Keycloak itself. Application clients belong in a dedicated realm; putting digna in `master` gives its users a route into the Keycloak administration console.

---

## Step 2: Create the Client

1. Go to **Clients** and click **Create client**
2. Configure:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — this becomes `DIGNA_OIDC_CLIENT_ID`
3. Click **Next**
4. On the **Capability config** step, turn **Client authentication** **On**
5. Leave **Standard flow** enabled; the other flows are not needed
6. Click **Next**

!!! warning "Client Authentication Must Be On"

    With **Client authentication** off, Keycloak creates a *public* client, which has no credentials at all — the **Credentials** tab in Step 4 will not exist. digna needs a confidential client. This toggle can be changed after creation if you get it wrong.

---

## Step 3: Set the Redirect URI

On the **Login settings** step (or the **Settings** tab afterwards):

1. **Valid redirect URIs**: enter your digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: leave empty, or set to `+` to mirror the redirect URIs
3. Click **Save**

!!! tip "Avoid Wildcards"

    Keycloak accepts patterns such as `https://digna.yourdomain.com/*`. A wildcard lets any path on that host receive an authorization code, so prefer the exact callback URL.

---

## Step 4: Collect the Client Secret

1. Open the **Credentials** tab
2. Confirm **Client Authenticator** is *Client Id and Secret*
3. Copy the **Client secret** → becomes `DIGNA_OIDC_CLIENT_SECRET`

The secret stays retrievable here and can be regenerated with **Regenerate**.

---

## Step 5: Build the Discovery URL

Substitute your Keycloak host and realm name:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

For example:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 and Earlier Include /auth"

    Before Keycloak 17, every endpoint sat under an `/auth` prefix:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distributions that set `KC_HTTP_RELATIVE_PATH=/auth` keep the old layout on current versions too. If the URL without `/auth` returns 404, try it with.

Open the URL in a browser before continuing. A JSON document confirms the host and realm are right.

---

## Step 6: Configure digna

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

The `key` in both files must match — `keycloak` here. Note that it does not have to equal the Keycloak **Client ID**, though keeping them the same is easier to follow.

---

## Step 7: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting Keycloak

### Invalid parameter: redirect_uri

The callback URL is not covered by **Valid redirect URIs**. Keycloak logs the URI it received in the server log, which is the quickest way to see the exact mismatch.

### The Credentials Tab Is Missing

The client is public. Turn **Client authentication** on under **Settings → Capability config**.

### 404 on the Discovery URL

Either the realm name is wrong, or the deployment uses the `/auth` prefix. Check the realm list in the admin console and try both URL forms.

### unauthorized_client or invalid_client

**Standard flow** is disabled under **Capability config**, or the secret was regenerated in Keycloak without updating `config.toml`.

### Certificate Errors from the Backend

A self-hosted Keycloak behind a private or self-signed certificate will fail digna's outbound HTTPS call to the discovery URL. Install the issuing CA into the trust store of the machine running the digna backend.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)