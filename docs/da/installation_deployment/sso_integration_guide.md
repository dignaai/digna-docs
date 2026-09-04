---
title: Single Sign-On (SSO) Integration Guide | digna Documentation
description: Trin-for-trin-guide til konfiguration af Single Sign-On (SSO) for digna ved brug af OpenID Connect (OIDC). Dækker dashboard- og backend-konfiguration, test, fejlfinding og understøttede identitetsudbydere inklusive Microsoft Entra ID, Google Workspace og Okta.
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
og_description: Konfigurer Single Sign-On for digna ved brug af OpenID Connect. Trin-for-trin opsætning for Microsoft Entra ID, Google Workspace, Okta og andre OIDC-kompatible identitetsudbydere.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integration Guide

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Configuration Steps](#configuration-steps)
3. [Dashboard Configuration](#dashboard-configuration)
4. [Backend Configuration](#backend-configuration)
5. [Testing Login](#testing-login)
6. [Troubleshooting](#troubleshooting)
7. [Supported Providers](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Denne guide giver trin-for-trin-instruktioner til integration af Single Sign-On (SSO) med digna-platformen ved brug af **OpenID Connect (OIDC)**.

### What is SSO?

Single Sign-On tillader brugere at logge ind på digna sikkert ved hjælp af deres virksomhedslegitimationsoplysninger gennem eksterne identitetsudbydere. Brugere kan autentificere sig med deres corporate credentials i stedet for at administrere separate digna-adgangskoder.

### How It Works

SSO i digna implementeres ved brug af OIDC-protokollen. Flere identitetsudbydere kan konfigureres parallelt ved at justere to centrale konfigurationsfiler:

- **`dashboard_config.toml`** — Styrer frontend login-grænsefladen
- **`config.toml`** — Konfigurerer backend OIDC-forbindelserne

### Supported Providers {: #supported-providers-overview }

Eksempler i denne guide bruger **Microsoft** og **Google**, men **enhver OIDC-kompatibel udbyder** kan integreres ved at følge samme struktur.

Almindelige OIDC-udbydere inkluderer:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Andre OIDC-kompatible identitetsudbydere

---

## Configuration Steps {: #configuration-steps }

SSO-konfiguration kræver opdateringer af to filer. Denne sektion forklarer, hvordan man konfigurerer hver af dem.

### Overview of Configuration Files

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login-grænseflade |
| **config.toml** | `/config.toml` | Backend OIDC-forbindelser |

Begge filer skal konfigureres for at SSO fungerer korrekt.

---

## Dashboard Configuration {: #dashboard-configuration }

### File Location

```
dashboard/dashboard_config.toml
```

### Step 1: Add OIDC Providers

Tilføj poster under `[[login.oidc]]`-arrayet for hver identitetsudbyder, du vil understøtte.

**Eksempel med Microsoft og Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Step 2: Configure Login Options

Angiv, om login baseret på adgangskode skal være tilladt:

```toml
[login]
usePassword = true
```

### Configuration Parameters

#### `[[login.oidc]]` Section

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Unik identifikator for OIDC-forbindelsen (skal matche key i config.toml) |
| `label` | string | Yes | Teksten der vises på login-knappen (fx "Login with Microsoft") |

#### `[login]` Section

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Tillad login med adgangskode ud over SSO |

### Understanding usePassword

**Hvis `usePassword = true`:**
- Login-skærmen viser SSO-knapper (fx "Login with Microsoft")
- Login-skærmen viser også brugernavn- og adgangskodefelter
- Brugere kan godkendes med enten metode
- Tillader hybride opsætninger, hvor nogle brugere bruger SSO og andre bruger adgangskoder

**Hvis `usePassword = false` (eller udeladt):**
- Login-skærmen viser kun SSO-knapper
- Ingen brugernavn-/adgangskodefelter
- Kun OIDC-godkendelse er tilgængelig

> **Tip**
>
> Login med adgangskode er kun tilgængeligt for brugere, der blev oprettet med adgangskoder ved hjælp af `digna user add`-kommandoen eller via dashboardet.

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

Hver udbyder skal have en dedikeret `[oidc.<key>]`-sektion. Key'en skal matche `key` defineret i `dashboard_config.toml`.

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
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID fra identitetsudbyderen | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret fra identitetsudbyderen | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Callback-URL efter autentificering | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC-konfigurations-endpoint | `https://login.microsoftonline.com/...` |

> **Important**
>
> Erstat pladsholder-værdierne (`<client_id>`, `<client_secret>`, `<tenant_id>`) med faktiske legitimationsoplysninger fra din identitetsudbyders developer-portal.

### Redirect URI

Redirect URI skal være den samme i din identitetsudbyderkonfiguration:

```
http://localhost:5173/oidc/callback
```

Hvis digna er hostet på et andet domæne, opdater tilsvarende:
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

Efter færdiggørelse af konfigurationen, verificer at SSO fungerer korrekt.

### Pre-Testing Checklist

Før test, sørg for:

- [ ] `dashboard_config.toml` er opdateret med OIDC-udbydere
- [ ] `config.toml` er opdateret med OIDC-legitimationsoplysninger
- [ ] Begge filer er gemt
- [ ] Legitimationsoplysninger er korrekte (client ID, client secret)
- [ ] Redirect URI matcher din deployment-URL
- [ ] Identitetsudbyder-applikationen er konfigureret med redirect URI

### Testing Steps

#### Step 1: Restart Services

Genstart digna backend og webserver for at anvende ændringer.

**If running as Windows service:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**If running manually:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**If using IIS or Tomcat:**
Genstart din webserver-service.

#### Step 2: Open Dashboard

Åbn digna-dashboardet i din browser:

```
http://localhost:5173
```

(eller din konfigurerede dashboard-URL)

#### Step 3: Verify Login Buttons

Tjek at login-knapper vises for hver konfigureret udbyder:

- Skal se "Login with Microsoft" knap
- Skal se "Login with Google" knap
- (Hvis usePassword = true) Skal se brugernavn/adgangskode-felter

Hvis knapper ikke vises:
- Tjek at `dashboard_config.toml` blev gemt
- Tjek at dashboard-servicen blev genstartet
- Tjek browserkonsollen (F12) for fejl

#### Step 4: Test SSO Login

Klik en af SSO-knapperne (fx "Login with Microsoft"):

1. Du bør blive omdirigeret til identitetsudbyderens login-side
2. Log ind med dine virksomhedslegitimationsoplysninger
3. Du bør blive omdirigeret tilbage til digna
4. Du bør være logget ind på digna

#### Step 5: Verify User Creation

Efter succesfuld SSO-login:

- Bruger bør automatisk oprettes i digna
- Bruger bør være logget ind
- Brugerprofilen bør vise dine identitetsudbyder-oplysninger
- Du bør se digna-dashboardet

#### Step 6: Test Password Login (If Enabled)

Hvis `usePassword = true`:

1. Log ud af digna
2. På login-siden, indtast brugernavn og adgangskode
3. Du bør kunne logge ind med adgangskode-legitimationsoplysninger

---

## Troubleshooting {: #troubleshooting }

### Login Buttons Don't Appear

**Symptoms:**
- OIDC-login-knapper ikke synlige på login-siden
- Ser kun adgangskodefelter (hvis usePassword = true)

**Causes & Solutions:**
1. Tjek at `dashboard_config.toml` er i `dashboard/`-mappen
2. Bekræft at `[[login.oidc]]`-sektionerne er til stede med korrekt syntaks
3. Genstart dashboard-servicen
4. Ryd browsercache (Ctrl+Shift+Delete eller Cmd+Shift+Delete)
5. Tjek browserkonsollen (F12 → Console) for fejl

---

### Redirect URI Mismatch Error

**Symptoms:**
- Efter klik på SSO-knap, fejl om "redirect_uri mismatch"
- "The redirect URI is not registered" fejl

**Causes & Solutions:**
1. Bekræft at `DIGNA_OIDC_REDIRECT_URI` i `config.toml` er korrekt
2. Bekræft at redirect URI er registreret i identitetsudbyderens indstillinger
3. Sørg for at begge bruger identiske URLs (inkl. protokol, domæne, sti)
4. Tjek for stavefejl i redirect URI
5. Hvis du bruger HTTPS, sørg for at certifikatet er gyldigt

---

### Invalid Client Credentials Error

**Symptoms:**
- "Invalid client ID or secret" fejl
- Autentificering fejler med legitimationsfejl

**Causes & Solutions:**
1. Bekræft at `DIGNA_OIDC_CLIENT_ID` og `DIGNA_OIDC_CLIENT_SECRET` er korrekte
2. Sørg for ingen ekstra mellemrum eller usædvanlige tegn
3. Tjek at legitimationsoplysninger ikke er udløbet eller blevet tilbagekaldt
4. Genstart backend-servicen efter opdatering af config
5. Tjek identitetsudbyderens konsol for at bekræfte at legitimationsoplysningerne er aktive

---

### Login Hangs eller Times Out

**Symptoms:**
- Klik på SSO-knappen gør ingenting
- Timeout efter flere sekunder
- Browser viser "Failed to connect" eller lignende

**Causes & Solutions:**
1. Bekræft at digna-backend kører: `digna repo check`
2. Tjek netværksforbindelse til identitetsudbyderen
3. Bekræft at `DIGNA_OIDC_CONFIGURATION_URL` er tilgængelig
4. Tjek firewall-regler tillader udgående HTTPS-forbindelser
5. Bekræft at backend og dashboard kan nå hinanden

---

### Users Not Automatically Created

**Symptoms:**
- SSO-login lykkes, men bruger oprettes ikke i digna
- Får tilladelsesfejl efter SSO-login

**Causes & Solutions:**
1. Bekræft at OIDC-konfigurationen er korrekt
2. Tjek at brugerrettigheder er sat korrekt op
3. Gennemse digna-logs for fejlnotifikationer
4. Genstart backend-servicen
5. Kontakt support@digna.ai hvis problemet fortsætter

---

## Supported Providers {: #supported-providers }

### Tested & Supported

Følgende OIDC-udbydere er testet og kendt for at virke:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Other OIDC Providers

Enhver udbyder, der understøtter OpenID Connect, kan integreres. Påkrævet information:

- Client ID
- Client secret
- OpenID configuration URL (typisk ved `/.well-known/openid-configuration`)
- Understøttede scopes (typisk `openid profile email`)

Kontakt support@digna.ai hvis du har brug for hjælp til at integrere en specifik udbyder.

---

## Best Practices

**DO:**
- Brug HTTPS i produktion (ikke HTTP)
- Opbevar client secrets sikkert (brug miljøvariabler hvis muligt)
- Roter secrets regelmæssigt
- Test i et ikke-produktionsmiljø først
- Dokumentér hvilke udbydere der er konfigureret
- Overvåg login-logs for usædvanlig aktivitet
- Hold identitetsudbyderens konfiguration i sync med digna-config

**DON'T:**
- Gem client secrets i versionskontrol
- Brug HTTP redirect URIs i produktion
- Konfigurer flere udbydere med samme key
- Lad standard/test-legitimationsoplysninger være i produktion
- Eksponer config-filer der indeholder secrets
- Bland udviklings- og produktions-legitimationsoplysninger

---

## Support

Brug for hjælp til SSO-konfiguration?

- **Email:** support@digna.ai
- **Documentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
