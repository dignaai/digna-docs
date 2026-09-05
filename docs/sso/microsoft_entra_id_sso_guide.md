---
title: Microsoft Entra ID SSO – Single Sign-On Integration | digna Documentation
description: Configure Single Sign-On for digna with Microsoft Entra ID (formerly Azure AD) using OpenID Connect — app registration, redirect URI, client secret, tenant ID and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, microsoft entra id, azure ad sso, oidc integration, app registration, enterprise authentication
---

# Set up SSO with Microsoft Entra ID

Microsoft Entra ID (formerly Azure Active Directory) is a fully OIDC-compliant provider, so digna integrates with it through the standard discovery endpoint.

This guide covers the **Entra ID side**: registering the application and collecting the four values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **Entra ID role** | Application Administrator, Cloud Application Administrator, or Global Administrator |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | The directory your users sign in to |

---

## Step 1: Register the Application

1. Sign in to the [Microsoft Entra admin center](https://entra.microsoft.com)
2. Go to **Identity → Applications → App registrations**
3. Click **New registration**
4. Configure:
   - **Name**: `digna` (shown to users on the consent screen)
   - **Supported account types**: *Accounts in this organizational directory only* for a single-tenant deployment
5. Under **Redirect URI**, select platform **Web** and enter your digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Click **Register**

!!! warning "Important"

    The platform must be **Web**, not *Single-page application*. digna exchanges the authorization code from the backend using a client secret, which the SPA platform type does not permit.

---

## Step 2: Collect the Client and Tenant IDs

On the application's **Overview** page, copy:

- **Application (client) ID** → becomes `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → goes into the discovery URL

---

## Step 3: Create a Client Secret

1. Go to **Certificates & secrets → Client secrets**
2. Click **New client secret**
3. Enter a description and choose an expiry
4. Click **Add**
5. Copy the **Value** column immediately

!!! warning "Copy the Value, Not the Secret ID"

    The **Value** is shown only once, on this page, and cannot be retrieved afterwards. The **Secret ID** next to it looks similar but is not the secret — using it produces an `invalid_client` error at login. If you navigate away before copying, delete the secret and create a new one.

!!! tip "Tip"

    Entra ID caps secret lifetime at 24 months, so every SSO integration has an expiry date. Note it somewhere you will see it — an expired secret takes SSO down for every user at once, with no warning on the login page.

---

## Step 4: Confirm the API Permissions

1. Go to **API permissions**
2. Confirm that **Microsoft Graph → User.Read** (delegated) is present — it is added by default

The `openid`, `profile` and `email` scopes digna requests are part of the standard OIDC set and need no separate grant. If your tenant requires admin consent for all applications, click **Grant admin consent for &lt;tenant&gt;**.

---

## Step 5: Build the Discovery URL

Substitute the **Directory (tenant) ID** from Step 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Use the v2.0 Endpoint"

    The `/v2.0/` segment matters. The v1.0 endpoint at `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` issues tokens in an older format and does not return the standard OIDC claims digna expects.

Open the URL in a browser before continuing. A JSON document confirms the tenant ID is correct.

---

## Step 6: Configure digna

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

The `key` in both files must match — `microsoft` here.

---

## Step 7: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting Entra ID

### AADSTS50011: Redirect URI Mismatch

The URI in `DIGNA_OIDC_REDIRECT_URI` differs from the one registered in Step 1. Entra ID compares the full string, so a trailing slash, `http` versus `https`, or a different port all count as a mismatch. Check **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Either the **Secret ID** was copied instead of the **Value**, or the secret has expired. Create a new secret and copy the Value column.

### AADSTS650057: Invalid Resource

The application registration was deleted or belongs to a different tenant than the one in the discovery URL. Confirm the Directory (tenant) ID on the Overview page.

### Users Log In but Nothing Happens

If the tenant requires admin consent and it has not been granted, the redirect returns without a usable token. Grant admin consent under **API permissions**.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)
