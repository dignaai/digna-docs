---
title: OneLogin SSO – Single Sign-On Integration | digna Documentation
description: Configure Single Sign-On for digna with OneLogin using OpenID Connect — OIDC app creation, redirect URIs, client credentials, token endpoint authentication and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, token endpoint authentication, enterprise authentication
---

# Set up SSO with OneLogin

OneLogin is OIDC-compliant. Its distinguishing feature is that the connector type is chosen from a catalogue when the app is created and cannot be changed afterwards.

This guide covers the **OneLogin side**: creating the application and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **OneLogin role** | Account owner or an administrator permitted to add applications |
| **Subdomain** | e.g. `yourcompany.onelogin.com` |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Create the OIDC Application

1. Sign in to the OneLogin Admin portal
2. Go to **Applications → Applications**
3. Click **Add App**
4. Search for `OpenId Connect` and select the **OpenId Connect (OIDC)** connector
5. Set the **Display Name** to `digna`
6. Click **Save**

!!! warning "The Connector Type Is Fixed at Creation"

    OneLogin has separate catalogue entries for SAML and OIDC, and an application cannot be converted from one to the other. If you pick a SAML connector by mistake, delete the app and add it again — there is no setting to switch protocols.

---

## Step 2: Configure the Redirect URI

1. Open the **Configuration** tab
2. In **Redirect URI's**, enter your digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Optionally set **Post Logout Redirect URIs** to your dashboard URL
4. Click **Save**

!!! note "One URI per Line"

    Unlike providers that expect a comma-separated list, OneLogin's **Redirect URI's** field takes one URI per line.

---

## Step 3: Set the Application Type and Authentication Method

1. Open the **SSO** tab
2. Confirm **Application Type** is *Web*
3. Set **Token Endpoint → Authentication Method** to *POST* (`client_secret_post`) or *Basic* (`client_secret_basic`)

!!! warning "Do Not Choose None"

    Setting the authentication method to *None* makes the application a public client with no secret, and digna's backend code exchange will be rejected. Either POST or Basic works.

---

## Step 4: Collect the Credentials

Still on the **SSO** tab:

- **Client ID** → becomes `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → becomes `DIGNA_OIDC_CLIENT_SECRET` (click **Show client secret**)

The page also shows the **Issuer URL**, which confirms the discovery URL in the next step.

---

## Step 5: Assign Users

1. Open the **Access** tab
2. Add the roles or groups whose members may use digna
3. Click **Save**

!!! note "Unassigned Users Are Refused After Login"

    As with most providers, OneLogin authenticates the user first and checks entitlement second. An unassigned user signs in successfully and is then refused, which looks like a digna error rather than an access-control decision.

---

## Step 6: Build the Discovery URL

Substitute your OneLogin subdomain:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

For example:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "The /2 Is the API Version"

    OneLogin's current OIDC implementation lives under `/oidc/2/`. Older documentation shows `/oidc/` without a version, which points at the retired first version. Check the **Issuer URL** on the SSO tab if in doubt — the discovery URL is the issuer plus `/.well-known/openid-configuration`.

---

## Step 7: Configure digna

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

The `key` in both files must match — `onelogin` here.

---

## Step 8: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting OneLogin

### redirect_uri did not match

The callback URL is missing from **Configuration → Redirect URI's**, or the entries were separated by commas rather than newlines.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** is set to *None*, or the client secret in `config.toml` is stale. Reveal the secret on the **SSO** tab and compare.

### The App Does Not Appear for Users

No role or group has been granted access on the **Access** tab.

### 404 on the Discovery URL

The subdomain is wrong, or the URL omits `/oidc/2/`. Compare against the **Issuer URL** shown on the SSO tab.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)
