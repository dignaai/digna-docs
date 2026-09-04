---
title: Integrationsguide för Single Sign-On (SSO) | digna Dokumentation
description: Steg-för-steg-guide för att konfigurera Single Sign-On (SSO) för digna med OpenID Connect (OIDC). Täcker dashboard- och backend-konfiguration, testning, felsökning och stöd för identitetsleverantörer inklusive Microsoft Entra ID, Google Workspace och Okta.
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
lang: sv
robots: index, follow
og_title: digna Single Sign-On (SSO) Integrationsguide
og_description: Konfigurera Single Sign-On för digna med OpenID Connect. Steg-för-steg-setup för Microsoft Entra ID, Google Workspace, Okta och andra OIDC-kompatibla identitetsleverantörer.
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

Denna guide ger steg-för-steg-instruktioner för att integrera Single Sign-On (SSO) med digna-plattformen med hjälp av **OpenID Connect (OIDC)**.

### Vad är SSO?

Single Sign-On låter användare logga in i digna säkert med sina företagsuppgifter via externa identitetsleverantörer. Användare kan autentisera sig med sina företagsuppgifter istället för att hantera separata digna-lösenord.

### Hur det fungerar

SSO i digna implementeras med OIDC-protokollet. Flera identitetsleverantörer kan konfigureras parallellt genom att justera två centrala konfigurationsfiler:

- **`dashboard_config.toml`** — Styr frontend-inloggningsgränssnittet
- **`config.toml`** — Konfigurerar backend OIDC-anslutningarna

### Stödda leverantörer {: #supported-providers-overview }

Exemplen i denna guide använder **Microsoft** och **Google**, men **vilken OIDC-kompatibel leverantör som helst** kan integreras genom samma struktur.

Vanliga OIDC-leverantörer inkluderar:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Andra OIDC-kompatibla identitetsleverantörer

---

## Configuration Steps {: #configuration-steps }

SSO-konfiguration kräver uppdateringar i två filer. Denna sektion förklarar hur du konfigurerar vardera.

### Översikt över konfigurationsfilerna

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend-inloggningsgränssnitt |
| **config.toml** | `/config.toml` | Backend OIDC-anslutningar |

Båda filerna måste konfigureras för att SSO ska fungera korrekt.

---

## Dashboard Configuration {: #dashboard-configuration }

### File Location

```
dashboard/dashboard_config.toml
```

### Steg 1: Lägg till OIDC-leverantörer

Lägg till poster under arrayen `[[login.oidc]]` för varje identitetsleverantör du vill stödja.

**Exempel med Microsoft och Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Steg 2: Konfigurera inloggningsalternativ

Ange om lösenordsbaserad inloggning ska tillåtas:

```toml
[login]
usePassword = true
```

### Konfigurationsparametrar

#### `[[login.oidc]]` Sektion

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Unikt identifierare för OIDC-anslutningen (måste matcha key i config.toml) |
| `label` | string | Yes | Text som visas på inloggningsknappen (t.ex. "Login with Microsoft") |

#### `[login]` Sektion

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Tillåt lösenordsbaserad inloggning utöver SSO |

### Förstå usePassword

**Om `usePassword = true`:**
- Inloggningsskärmen visar SSO-knappar (t.ex. "Login with Microsoft")
- Inloggningsskärmen visar också användarnamn- och lösenordsfält
- Användare kan autentisera sig med antingen metod
- Tillåter hybrida upplägg där vissa användare använder SSO och andra lösenord

**Om `usePassword = false` (eller utelämnad):**
- Inloggningsskärmen visar endast SSO-knappar
- Inga användarnamn-/lösenordsfält visas
- Endast OIDC-autentisering är tillgänglig

> **Tip**
>
> Lösenordsbaserad inloggning är endast tillgänglig för användare som skapats med lösenord via kommandot `digna user add` eller via dashboarden.

### Komplett exempel

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

(Rotkatalog för digna-installationen)

### Steg 1: Lägg till OIDC-sektioner

Varje leverantör måste ha en dedikerad `[oidc.<key>]`-sektion. Key måste matcha `key` som definierats i `dashboard_config.toml`.

### Microsoft-konfiguration

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google-konfiguration

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurationsparametrar

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID från identitetsleverantören | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret från identitetsleverantören | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Callback-URL efter autentisering | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC-konfigurationsendpoint | `https://login.microsoftonline.com/...` |

> **Important**
>
> Ersätt platshållarvärden (`<client_id>`, `<client_secret>`, `<tenant_id>`) med verkliga referenser från din identitetsleverantörs utvecklarportal.

### Redirect URI

Redirect-URI måste vara densamma i din identitetsleverantörskonfiguration:

```
http://localhost:5173/oidc/callback
```

Om digna är hostad på en annan domän, uppdatera därefter:
- Lokalt: `http://localhost:5173/oidc/callback`
- Produktion: `https://digna.yourdomain.com/oidc/callback`

### Komplett exempel

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

Efter att konfigurationen är klar, verifiera att SSO fungerar korrekt.

### Förtest-checklista

Innan test, säkerställ:

- [ ] `dashboard_config.toml` har uppdaterats med OIDC-leverantörer
- [ ] `config.toml` har uppdaterats med OIDC-referenser
- [ ] Båda filerna har sparats
- [ ] Referenserna är korrekta (client ID, client secret)
- [ ] Redirect URI matchar din deployment-URL
- [ ] Identitetsleverantörens applikation är konfigurerad med redirect URI

### Teststeg

#### Steg 1: Starta om tjänster

Starta om digna-backend och webbserver för att tillämpa ändringarna.

**Om du kör som Windows-tjänst:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Om du kör manuellt:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Om du använder IIS eller Tomcat:**
Starta om din webbserver-tjänst.

#### Steg 2: Öppna dashboard

Öppna digna-dashboarden i din webbläsare:

```
http://localhost:5173
```

(eller din konfigurerade dashboard-URL)

#### Steg 3: Verifiera inloggningsknappar

Kontrollera att inloggningsknappar visas för varje konfigurerad leverantör:

- Ska visa "Login with Microsoft"-knappen
- Ska visa "Login with Google"-knappen
- (Om usePassword = true) Ska visa användarnamn-/lösenordsfält

Om knappar inte visas:
- Kontrollera att `dashboard_config.toml` sparades
- Kontrollera att dashboard-tjänsten startades om
- Kontrollera webbläsarens konsol (F12) för fel

#### Steg 4: Testa SSO-inloggning

Klicka på en av SSO-knapparna (t.ex. "Login with Microsoft"):

1. Du ska omdirigeras till identitetsleverantörens inloggningssida
2. Logga in med dina företagsuppgifter
3. Du ska omdirigeras tillbaka till digna
4. Du ska vara inloggad i digna

#### Steg 5: Verifiera användarskapande

Efter lyckad SSO-inloggning:

- Användare ska skapas automatiskt i digna
- Användare ska vara inloggad
- Användarprofil ska visa dina identitetsleverantörsuppgifter
- Du ska se digna-dashboarden

#### Steg 6: Testa lösenordsinloggning (om aktiverat)

Om `usePassword = true`:

1. Logga ut från digna
2. På inloggningssidan, ange ett användarnamn och lösenord
3. Du ska kunna logga in med lösenordsuppgifterna

---

## Troubleshooting {: #troubleshooting }

### Inloggningsknappar visas inte

**Symptom:**
- OIDC-inloggningsknappar syns inte på inloggningssidan
- Ser endast lösenordsfält (om usePassword = true)

**Orsaker & Lösningar:**
1. Kontrollera att `dashboard_config.toml` ligger i `dashboard/`-katalogen
2. Verifiera att `[[login.oidc]]`-sektionerna finns med korrekt syntax
3. Starta om dashboard-tjänsten
4. Rensa webbläsarens cache (Ctrl+Shift+Delete eller Cmd+Shift+Delete)
5. Kontrollera webbläsarkonsolen (F12 → Console-fliken) efter fel

---

### Redirect URI mismatch-fel

**Symptom:**
- Efter att ha klickat på SSO-knappen visas fel om "redirect_uri mismatch"
- "The redirect URI is not registered" fel

**Orsaker & Lösningar:**
1. Verifiera att `DIGNA_OIDC_REDIRECT_URI` i `config.toml` är korrekt
2. Verifiera att redirect URI är registrerad i identitetsleverantörens inställningar
3. Säkerställ att båda använder identiska URL:er (inklusive protokoll, domän, sökväg)
4. Kontrollera stavfel i redirect URI
5. Om du använder HTTPS, säkerställ att certifikatet är giltigt

---

### Ogiltiga klientreferenser-fel

**Symptom:**
- "Invalid client ID or secret" fel
- Autentisering misslyckas med referensfel

**Orsaker & Lösningar:**
1. Verifiera att `DIGNA_OIDC_CLIENT_ID` och `DIGNA_OIDC_CLIENT_SECRET` är korrekta
2. Säkerställ att inga extra mellanslag eller tecken finns
3. Kontrollera att referenserna inte har gått ut eller återkallats
4. Starta om backend-tjänsten efter att ha uppdaterat konfigurationen
5. Kontrollera identitetsleverantörens konsol för att bekräfta att referenserna är aktiva

---

### Inloggning hänger sig eller time-out

**Symptom:**
- Klick på SSO-knappen ger inget
- Timeout efter några sekunder
- Webbläsaren visar "Failed to connect" eller liknande

**Orsaker & Lösningar:**
1. Verifiera att digna-backend körs: `digna repo check`
2. Kontrollera nätverksanslutning till identitetsleverantören
3. Verifiera att `DIGNA_OIDC_CONFIGURATION_URL` är åtkomlig
4. Kontrollera att brandväggsregler tillåter utgående HTTPS-anslutningar
5. Verifiera att backend och dashboard kan nå varandra

---

### Användare skapas inte automatiskt

**Symptom:**
- SSO-inloggning lyckas men användare skapas inte i digna
- Får behörighetsfel efter SSO-inloggning

**Orsaker & Lösningar:**
1. Verifiera att OIDC-konfigurationen är korrekt
2. Kontrollera att användarbehörigheter är korrekt uppsatta
3. Granska digna-loggar för felmeddelanden
4. Starta om backend-tjänsten
5. Kontakta support@digna.ai om problemet kvarstår

---

## Supported Providers {: #supported-providers }

### Testade & stödda

Följande OIDC-leverantörer har testats och är kända att fungera:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Andra OIDC-leverantörer

Vilken leverantör som helst som stöder OpenID Connect kan integreras. Nödvändig information:

- Client ID
- Client secret
- OpenID-konfigurations-URL (vanligtvis vid `/.well-known/openid-configuration`)
- Stödda scopes (typiskt `openid profile email`)

Kontakta support@digna.ai om du behöver hjälp med att integrera en specifik leverantör.

---

## Best Practices

**GÖR:**
- Använd HTTPS i produktion (inte HTTP)
- Spara client secrets säkert (använd miljövariabler om möjligt)
- Rotera secrets regelbundet
- Testa i en icke-produktionsmiljö först
- Dokumentera vilka leverantörer som är konfigurerade
- Övervaka inloggningsloggar för ovanlig aktivitet
- Håll identitetsleverantörens konfiguration i synk med digna-konfigurationen

**GÖR INTE:**
- Spara client secrets i versionshantering
- Använd HTTP redirect-URIs i produktion
- Konfigurera flera leverantörer med samma key
- Lämna default/test-referenser i produktion
- Exponera konfigurationsfiler som innehåller secrets
- Blanda utvecklings- och produktionsreferenser

---

## Support

Behöver du hjälp med SSO-konfiguration?

- **Email:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Webbplats:** https://www.digna.ai

---

**Senast uppdaterad:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**