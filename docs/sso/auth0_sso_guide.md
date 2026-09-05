---
title: Auth0 SSO – Single Sign-On Integration | digna Documentation
description: Configure Single Sign-On for digna with Auth0 using OpenID Connect — regular web application setup, allowed callback URLs, client credentials, tenant domain and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regular web application, callback urls, openid connect, enterprise authentication
---

# Set up SSO with Auth0

Auth0 is OIDC-compliant and exposes a discovery endpoint per tenant. The main thing to get right is the tenant domain, which appears in the discovery URL and changes if you enable a custom domain.

This guide covers the **Auth0 side**: creating the application and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **Auth0 role** | Admin on the tenant |
| **Tenant domain** | e.g. `yourcompany.eu.auth0.com` — the region segment matters |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Create the Application

1. Sign in to the [Auth0 Dashboard](https://manage.auth0.com)
2. Go to **Applications → Applications**
3. Click **Create Application**
4. Name it `digna` and choose **Regular Web Applications**
5. Click **Create**

!!! warning "Choose Regular Web Applications"

    *Single Page Application* and *Native* create public clients with no secret. digna performs the code exchange from its backend and needs a confidential client, so **Regular Web Applications** is the correct type. Unlike some providers, Auth0 does let you change the type later under **Settings → Application Type**.

---

## Step 2: Add the Callback URL

On the application's **Settings** tab:

1. Find **Allowed Callback URLs**
2. Enter your digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Optionally set **Allowed Logout URLs** to your dashboard URL
4. Scroll to the bottom and click **Save Changes**

!!! note "Comma-Separated, Not Newline-Separated"

    Auth0 accepts several callback URLs in this field, separated by commas. A list separated only by newlines is read as one malformed URL and silently matches nothing.

---

## Step 3: Collect the Credentials

Still on **Settings**, in the **Basic Information** panel:

- **Domain** → goes into the discovery URL
- **Client ID** → becomes `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → becomes `DIGNA_OIDC_CLIENT_SECRET` (click to reveal)

---

## Step 4: Confirm the Grant Type

1. Go to **Settings → Advanced Settings → Grant Types**
2. Confirm **Authorization Code** is ticked

It is enabled by default for Regular Web Applications. If it has been unticked, digna's login fails with `unauthorized_client`.

---

## Step 5: Build the Discovery URL

Substitute the **Domain** from Step 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

For example:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Custom Domains Change the Issuer"

    If your tenant uses a custom domain such as `login.yourcompany.com`, use that domain in the discovery URL. Mixing the two — the canonical domain in the discovery URL, the custom one in the browser — produces an issuer mismatch, and the token is rejected after an otherwise successful login.

---

## Step 6: Configure digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

The `key` in both files must match — `auth0` here.

---

## Step 7: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting Auth0

### Callback URL Mismatch

Auth0's error page names the URL it received. Add it to **Allowed Callback URLs**, checking that entries are comma-separated.

### unauthorized_client

**Authorization Code** is not enabled under **Advanced Settings → Grant Types**, or the application type is not Regular Web Applications.

### Access Denied After a Successful Login

A Rule, Action or Post-Login trigger in the tenant is rejecting the user. Check **Actions → Flows → Login** and the tenant logs under **Monitoring → Logs**, which show the exact reason.

### Issuer Mismatch

The discovery URL and the domain the browser was sent to differ — usually the canonical tenant domain versus a custom domain. Use one consistently.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
