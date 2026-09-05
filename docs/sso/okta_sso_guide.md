---
title: Okta SSO – Single Sign-On Integration | digna Documentation
description: Configure Single Sign-On for digna with Okta using OpenID Connect — app integration, sign-in redirect URIs, client credentials, authorization server choice and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, app integration, authorization server, openid connect, enterprise authentication
---

# Set up SSO with Okta

Okta is OIDC-compliant, with one wrinkle that catches most first-time integrations: an Okta org exposes more than one authorization server, and each has its own discovery URL.

This guide covers the **Okta side**: creating the app integration and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator, or an admin role permitted to create app integrations |
| **Okta domain** | e.g. `yourcompany.okta.com`, or a custom domain if configured |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Create the App Integration

1. Sign in to the Okta Admin Console
2. Go to **Applications → Applications**
3. Click **Create App Integration**
4. Select:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Click **Next**

!!! warning "Application Type Cannot Be Changed"

    Choosing *Single-Page Application* instead of *Web Application* creates a public client with no secret, and digna's backend code exchange will fail with `invalid_client`. The type is fixed at creation — a wrong choice means deleting the app and starting again.

---

## Step 2: Configure the Integration

1. **App integration name**: `digna`
2. **Grant type**: leave *Authorization Code* selected
3. **Sign-in redirect URIs**: enter your digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: optional
5. Under **Assignments**, choose who may use the integration — a specific group is safer than *Allow everyone in your organization to access*
6. Click **Save**

!!! note "Assignment Is Required"

    Okta authenticates the user and then checks whether they are assigned to the application. An unassigned user reaches the Okta login page, signs in successfully, and is refused at the redirect back. If login works for you but not for colleagues, assignment is the first thing to check.

---

## Step 3: Collect the Credentials

On the application's **General** tab, under **Client Credentials**:

- **Client ID** → becomes `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → becomes `DIGNA_OIDC_CLIENT_SECRET` (click the eye icon to reveal)

---

## Step 4: Choose the Authorization Server

This is the step that determines your discovery URL. Go to **Security → API** to see the authorization servers in your org.

**Org authorization server** — issues tokens for the Okta org itself:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — including the one Okta creates called `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

For the built-in server, `<auth_server_id>` is literally `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Which One?"

    Use the **org** authorization server unless your organization already standardizes on a custom one for API access policies. Okta Developer accounts default to `default`; many enterprise orgs disable it. Open both URLs in a browser — the one that returns JSON rather than an error is the one available to you.

---

## Step 5: Configure digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

The `key` in both files must match — `okta` here.

---

## Step 6: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting Okta

### The redirect URI Is Not Registered

Okta names the offending URI in the error. Compare it with **General → Sign-in redirect URIs**; Okta matches the full string including any trailing slash.

### User Is Not Assigned to the Client Application

The account is not in the application's assignment list. Add the user or their group under **Assignments**.

### 400 Bad Request: Invalid Authorization Server

The `<auth_server_id>` in the discovery URL does not exist, most often `default` on an org where it has been removed. Check **Security → API** for the servers actually available.

### invalid_client at the Token Step

The integration was created as a Single-Page Application and has no client secret. Recreate it as a Web Application.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
