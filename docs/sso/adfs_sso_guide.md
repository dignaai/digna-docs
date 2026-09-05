---
title: AD FS SSO – Single Sign-On Integration | digna Documentation
description: Configure Single Sign-On for digna with Active Directory Federation Services using OpenID Connect — application group, server application, shared secret, permitted scopes and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, application group, openid connect, on-premises identity provider
---

# Set up SSO with AD FS

Active Directory Federation Services is the on-premises option: your own servers issue the tokens, and the discovery URL is your own host name. AD FS supports OpenID Connect from **Windows Server 2016** onwards.

This guide covers the **AD FS side**: creating the application group and collecting the values digna needs. The digna side — `dashboard_config.toml`, testing and troubleshooting — is the same for every provider and is described in the [Single Sign-On Overview](overview.md).

---

## Before You Start

| Requirement | Notes |
|---|---|
| **AD FS version** | Windows Server 2016 or later — earlier versions have no OIDC support |
| **Access** | Local administrator on the AD FS server |
| **Federation service name** | e.g. `adfs.yourdomain.com` |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Step 1: Create the Application Group

1. On the AD FS server, open **AD FS Management**
2. Right-click **Application Groups** and choose **Add Application Group**
3. Enter `digna` as the name
4. Under **Standalone applications** — or **Client-Server applications** depending on your version — select **Server application accessing a web API**
5. Click **Next**

---

## Step 2: Configure the Server Application

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS generates a GUID. Copy it — this becomes `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: enter your digna callback URL and click **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Click **Next**

!!! warning "Click Add, Not Just Next"

    The redirect URI field has its own **Add** button. Typing a URI and clicking **Next** without pressing **Add** discards it, and the wizard gives no warning. Confirm the URI appears in the list below the field before continuing.

---

## Step 3: Generate the Shared Secret

1. Tick **Generate a shared secret**
2. Copy the generated secret → becomes `DIGNA_OIDC_CLIENT_SECRET`
3. Click **Next**

!!! warning "The Secret Is Shown Once"

    AD FS displays the shared secret only on this wizard page and cannot show it again. If you lose it, reset it later from the application group's properties.

---

## Step 4: Configure the Web API

1. **Identifier**: enter the same client identifier from Step 2 and click **Add**
2. Click **Next**
3. Choose an **Access Control Policy** — *Permit everyone* is the simplest starting point; restrict it to a group for production
4. Click **Next**

---

## Step 5: Grant the Permitted Scopes

On the **Configure Application Permissions** step, tick:

- `openid`
- `profile`
- `email`

Then click **Next** and complete the wizard.

!!! warning "openid Is Not Ticked by Default"

    AD FS pre-selects only `user_impersonation` in some versions. Without `openid`, the token endpoint returns an OAuth access token rather than an ID token, and digna cannot identify the user.

---

## Step 6: Confirm the Discovery Endpoint

Substitute your federation service name:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

For example:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Open it in a browser. A JSON document confirms OIDC is enabled and the host name is right.

!!! note "The Backend Must Trust the Certificate"

    An internal certificate authority is common for AD FS. The machine running the digna backend makes its own outbound HTTPS call to this URL, so the issuing CA must be in that machine's trust store — not only in the browsers of the people logging in.

---

## Step 7: Configure digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

The `key` in both files must match — `adfs` here.

---

## Step 8: Test

Restart the backend and web server, then open the dashboard. See [Testing Login](overview.md#testing-login) for the full checklist.

---

## Troubleshooting AD FS

### MSIS9611: The Client Is Not Allowed to Access the Resource

The web API identifier in Step 4 does not match the client identifier, or the scopes in Step 5 were not granted. Both are editable from the application group's properties.

### MSIS9602: Invalid redirect_uri

The URI was typed but not added with the **Add** button, or differs from `DIGNA_OIDC_REDIRECT_URI`. Check **Application Groups → digna → digna backend → Properties**.

### No ID Token Is Returned

The `openid` scope is missing from the application permissions.

### The Backend Cannot Reach the Discovery URL

Either DNS on the backend host does not resolve the federation service name, or the AD FS certificate is not trusted there. Test with `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` from the digna server itself.

### Events to Check

The AD FS server logs failures to **Applications and Services Logs → AD FS → Admin** in Event Viewer, usually with a more specific reason than the browser shows.

---

## See Also

- [Single Sign-On Overview](overview.md) — configuration reference, testing and general troubleshooting
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)
