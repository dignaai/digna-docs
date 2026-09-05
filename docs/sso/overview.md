---
title: Single Sign-On (SSO) Overview | digna Documentation
description: How Single Sign-On works in digna using OpenID Connect (OIDC). Covers dashboard and backend configuration, testing, troubleshooting, and links to per-provider setup guides for Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne and AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Overview

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Provider Guides](#provider-guides)
3. [Configuration Steps](#configuration-steps)
4. [Dashboard Configuration](#dashboard-configuration)
5. [Backend Configuration](#backend-configuration)
6. [Testing Login](#testing-login)
7. [Troubleshooting](#troubleshooting)
8. [Supported Providers](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

This guide provides step-by-step instructions for integrating Single Sign-On (SSO) with the digna platform using **OpenID Connect (OIDC)**.

### What is SSO?

Single Sign-On allows users to log in to digna securely using their enterprise credentials through external identity providers. Users can authenticate with their corporate credentials instead of managing separate digna passwords.

### How It Works

SSO in digna is implemented using the OIDC protocol. Multiple identity providers can be configured in parallel by adjusting two key configuration files:

- **`dashboard_config.toml`** — Controls the frontend login interface
- **`config.toml`** — Configures the backend OIDC connections

### Supported Providers {: #supported-providers-overview }

Examples in this guide use **Microsoft** and **Google**, but **any OIDC-compliant provider** can be integrated following the same structure.

---

## Provider Guides {: #provider-guides }

Every provider needs the same four values — a client ID, a client secret, a redirect URI and a discovery URL — but each one puts them in a different place in its admin console, and several have a provider-specific step that the others do not. The guides below cover that half of the work; this page covers the digna half, which is identical for all of them.

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Self-hosted; the only provider here where you control the token service |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL is per-tenant, and custom domains change it |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Consent screen must be published before non-test users can log in |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Self-hosted; discovery URL is per-realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID appears in the discovery URL; secrets expire |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Authorization server choice changes the discovery URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | The OIDC app type must be chosen at creation and cannot be changed |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment ID appears in the discovery URL |

Any other OIDC-compliant provider works the same way — see [Other OIDC Providers](#supported-providers).

---

## Configuration Steps {: #configuration-steps }

SSO configuration requires updates to two files. This section explains how to configure each one.

### Overview of Configuration Files

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

Both files must be configured for SSO to work properly.

---

## Dashboard Configuration {: #dashboard-configuration }

### File Location

```
dashboard/dashboard_config.toml
```

### Step 1: Add OIDC Providers

Add entries under the `[[login.oidc]]` array for each identity provider you want to support.

**Example with Microsoft and Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Step 2: Configure Login Options

Specify whether password-based login should be allowed:

```toml
[login]
usePassword = true
```

### Configuration Parameters

#### `[[login.oidc]]` Section

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Unique identifier for the OIDC connection (must match key in config.toml) |
| `label` | string | Yes | Text displayed on the login button (e.g., "Login with Microsoft") |

#### `[login]` Section

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Allow password-based login in addition to SSO |

### Understanding usePassword

**If `usePassword = true`:**
- Login screen shows SSO buttons (e.g., "Login with Microsoft")
- Login screen also shows username and password fields
- Users can authenticate with either method
- Allows hybrid setups where some users use SSO and others use passwords

**If `usePassword = false` (or omitted):**
- Login screen shows only SSO buttons
- No username/password fields
- Only OIDC authentication is available

!!! tip "Tip"

    Password-based login is only available for users who were created with passwords using the `digna user add` command or via the dashboard.

### Complete Example

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend Configuration {: #backend-configuration }

### File Location

```
/config.toml
```

(Root digna installation directory)

### Step 1: Add OIDC Provider Sections

Each provider must have a dedicated `[oidc.<key>]` section. The key must match the `key` defined in `dashboard_config.toml`.

### Microsoft Configuration

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google Configuration

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Configuration Parameters

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID from identity provider | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret from identity provider | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Callback URL after authentication | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC configuration endpoint | `https://login.microsoftonline.com/...` |

!!! warning "Important"

    Replace placeholder values (`<client_id>`, `<client_secret>`, `<tenant_id>`) with actual credentials from your identity provider's developer portal.

### Redirect URI

The redirect URI must be the same in your identity provider configuration:

```
http://localhost:5173/oidc/callback
```

If digna is hosted at a different domain, update accordingly:
- Local: `http://localhost:5173/oidc/callback`
- Production: `https://digna.yourdomain.com/oidc/callback`

### Complete Example

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Testing Login {: #testing-login }

After completing the configuration, verify that SSO is working correctly.

### Pre-Testing Checklist

Before testing, ensure:

- [ ] `dashboard_config.toml` has been updated with OIDC providers
- [ ] `config.toml` has been updated with OIDC credentials
- [ ] Both files have been saved
- [ ] Credentials are correct (client ID, client secret)
- [ ] Redirect URI matches your deployment URL
- [ ] Identity provider application is configured with the redirect URI

### Testing Steps

#### Step 1: Restart Services

Restart the digna backend and web server to apply changes.

**If running as a service on Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**If running as a service on Linux or macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**If running manually:**
```bash
digna serve --address localhost --port 8082
```

**Restart the web server too** — IIS or Tomcat on Windows, nginx or Apache on Linux and macOS.

#### Step 2: Open Dashboard

Open the digna dashboard in your browser:

```
http://localhost:5173
```

(or your configured dashboard URL)

#### Step 3: Verify Login Buttons

Check that login buttons appear for each configured provider:

- Should see "Login with Microsoft" button
- Should see "Login with Google" button
- (If usePassword = true) Should see username/password fields

If buttons don't appear:
- Check that `dashboard_config.toml` was saved
- Check that dashboard service was restarted
- Check browser console (F12) for errors

#### Step 4: Test SSO Login

Click one of the SSO buttons (e.g., "Login with Microsoft"):

1. You should be redirected to the identity provider's login page
2. Log in with your enterprise credentials
3. You should be redirected back to digna
4. You should be logged in to digna

#### Step 5: Verify User Creation

After successful SSO login:

- User should be automatically created in digna
- User should be logged in
- User profile should display your identity provider credentials
- You should see the digna dashboard

#### Step 6: Test Password Login (If Enabled)

If `usePassword = true`:

1. Log out of digna
2. On the login page, enter a username and password
3. You should be able to log in with password credentials

---

## Troubleshooting {: #troubleshooting }

### Login Buttons Don't Appear

**Symptoms:**
- OIDC login buttons not visible on login page
- Only see password fields (if usePassword = true)

**Causes & Solutions:**
1. Check `dashboard_config.toml` is in `dashboard/` directory
2. Verify `[[login.oidc]]` sections are present with correct syntax
3. Restart dashboard service
4. Clear browser cache (Ctrl+Shift+Delete or Cmd+Shift+Delete)
5. Check browser console (F12 → Console tab) for errors

---

### Redirect URI Mismatch Error

**Symptoms:**
- After clicking SSO button, error about "redirect_uri mismatch"
- "The redirect URI is not registered" error

**Causes & Solutions:**
1. Verify `DIGNA_OIDC_REDIRECT_URI` in `config.toml` is correct
2. Verify redirect URI is registered in identity provider settings
3. Ensure both use identical URLs (including protocol, domain, path)
4. Check for typos in the redirect URI
5. If using HTTPS, ensure certificate is valid

---

### Invalid Client Credentials Error

**Symptoms:**
- "Invalid client ID or secret" error
- Authentication fails with credentials error

**Causes & Solutions:**
1. Verify `DIGNA_OIDC_CLIENT_ID` and `DIGNA_OIDC_CLIENT_SECRET` are correct
2. Ensure no extra spaces or special characters
3. Check credentials haven't expired or been revoked
4. Restart backend service after updating config
5. Check identity provider console to confirm credentials are active

---

### Login Hangs or Times Out

**Symptoms:**
- Clicking SSO button does nothing
- Timeout after several seconds
- Browser shows "Failed to connect" or similar

**Causes & Solutions:**
1. Verify digna backend is running: `digna repo check`
2. Check network connectivity to identity provider
3. Verify `DIGNA_OIDC_CONFIGURATION_URL` is accessible
4. Check firewall rules allow outbound HTTPS connections
5. Verify backend and dashboard can reach each other

---

### Users Not Automatically Created

**Symptoms:**
- SSO login succeeds but user not created in digna
- Get permission error after SSO login

**Causes & Solutions:**
1. Verify OIDC configuration is correct
2. Check user permissions are set up
3. Review digna logs for error messages
4. Restart backend service
5. Contact support@digna.ai if issue persists

---

## Supported Providers {: #supported-providers }

### Tested & Supported

The following OIDC providers have been tested and are known to work:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Other OIDC Providers

Any provider that supports OpenID Connect can be integrated. Required information:

- Client ID
- Client secret
- OpenID configuration URL (usually at `/.well-known/openid-configuration`)
- Supported scopes (typically `openid profile email`)

Contact support@digna.ai if you need help integrating a specific provider.

---

## Best Practices

**DO:**
- Use HTTPS in production (not HTTP)
- Store client secrets securely (use environment variables if possible)
- Rotate secrets periodically
- Test in a non-production environment first
- Document which providers are configured
- Monitor login logs for unusual activity
- Keep identity provider configuration in sync with digna config

**DON'T:**
- Store client secrets in version control
- Use HTTP redirect URIs in production
- Configure multiple providers with the same key
- Leave default/test credentials in production
- Expose config files containing secrets
- Mix development and production credentials

---

## Support

Need help with SSO configuration?

- **Email:** support@digna.ai
- **Documentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
