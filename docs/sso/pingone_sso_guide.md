---
title: PingOne SSO – Single Sign-On Integration | digna Documentation
description: Configure Single Sign-On for digna with PingOne using OpenID Connect — OIDC web app setup, redirect URIs, client credentials, environment ID, regional domains and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, environment id, openid connect, enterprise authentication
---

# Set up SSO with PingOne

PingOne is OIDC-compliant. Two of its values need care: the **environment ID**, which appears in every endpoint URL, and the **regional domain**, which differs between the North American, European, Canadian, Asia-Pacific and Australian tenants.

This guide covers the **PingOne side**: creating the application and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **PingOne role** | Environment Admin or Identity Data Admin on the target environment |
| **Environment** | The PingOne environment your digna users belong to |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Create the Application

1. Sign in to the PingOne admin console and select your environment
2. Go to **Applications → Applications**
3. Click the **+** button
4. Enter `digna` as the **Application Name**
5. Select **OIDC Web App**
6. Click **Save**

!!! warning "Pick OIDC Web App, Not Single-Page App"

    *Single-Page App* and *Native App* create public clients that cannot hold a secret. digna exchanges the authorization code from its backend and needs the confidential **OIDC Web App** type.

---

## Step 2: Configure the Redirect URI

1. Open the application's **Configuration** tab
2. Click the pencil icon to edit
3. Confirm **Response Type** is *Code* and **Grant Type** is *Authorization Code*
4. Under **Redirect URIs**, enter your digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. Set **Token Endpoint Authentication Method** to *Client Secret Post* or *Client Secret Basic*
6. Click **Save**

---

## Step 3: Enable the Application

On the application's row or detail panel, switch the toggle to **enabled**.

!!! warning "New Applications Start Disabled"

    PingOne creates applications in a disabled state. A disabled application produces an error at the authorization step that does not mention the toggle, so this is worth confirming before debugging anything else.

---

## Step 4: Grant the Scopes

1. Open the **Resources** tab
2. Confirm that `openid` is granted, and add `profile` and `email` from the **OpenID Connect** resource
3. Click **Save**

---

## Step 5: Assign Users

1. Open the **Access** tab
2. Add the population or groups whose members may use digna
3. Click **Save**

---

## Step 6: Collect the Credentials and Environment ID

On the **Configuration** tab, expand **General**:

- **Client ID** → becomes `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → becomes `DIGNA_OIDC_CLIENT_SECRET` (click the eye icon)
- **Environment ID** → goes into the discovery URL

The same tab lists the ready-made **OIDC Discovery Endpoint**, which you can copy directly instead of assembling it by hand.

---

## Step 7: Build the Discovery URL

Substitute the environment ID and the domain for your region:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domain |
|---|---|
| North America | `auth.pingone.com` |
| Europe | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

For a European environment:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Copy It Rather Than Type It"

    The regional domain is the single most common mistake in a PingOne integration, and a wrong region gives a 404 rather than a helpful message. Use the **OIDC Discovery Endpoint** value from Step 6.

---

## Step 8: Configure digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

The `key` in both files must match — `pingone` here.

---

## Step 9: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting PingOne

### 404 on the Discovery URL

The regional domain or the environment ID is wrong. Compare with the **OIDC Discovery Endpoint** shown on the application's Configuration tab.

### NOT_FOUND or Application Disabled

The application toggle from Step 3 is still off.

### Redirect URI Mismatch

PingOne matches the full string. Check **Configuration → Redirect URIs** for a trailing slash or a scheme difference.

### Login Succeeds but No Email Claim Reaches digna

The `email` and `profile` scopes have not been granted on the **Resources** tab.

### The User Cannot See the Application

No population or group has been granted access on the **Access** tab.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)
