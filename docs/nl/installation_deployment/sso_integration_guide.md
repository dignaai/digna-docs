---
title: Single Sign-On (SSO) Integratiegids | digna Documentatie
description: Stapsgewijze handleiding voor het configureren van Single Sign-On (SSO) voor digna met OpenID Connect (OIDC). Behandelt dashboard- en backendconfiguratie, testen, oplossen van problemen en ondersteunde identity providers zoals Microsoft Entra ID, Google Workspace en Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integratie
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integratie
  - enterprise authenticatie
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integratiegids
og_description: Configureer Single Sign-On voor digna met OpenID Connect. Stapsgewijze setup voor Microsoft Entra ID, Google Workspace, Okta en andere OIDC-conforme identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integration Guide

---

## Table of Contents

1. [Introductie en Overzicht](#introduction-and-overview)
2. [Configuratiestappen](#configuration-steps)
3. [Dashboardconfiguratie](#dashboard-configuration)
4. [Backendconfiguratie](#backend-configuration)
5. [Login testen](#testing-login)
6. [Probleemoplossing](#troubleshooting)
7. [Ondersteunde providers](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Deze gids geeft stapsgewijze instructies voor het integreren van Single Sign-On (SSO) met het digna-platform met behulp van **OpenID Connect (OIDC)**.

### Wat is SSO?

Single Sign-On stelt gebruikers in staat om veilig in te loggen bij digna met hun bedrijfsreferenties via externe identity providers. Gebruikers kunnen zich authenticeren met hun corporate inloggegevens in plaats van aparte digna-wachtwoorden te beheren.

### Hoe werkt het

SSO in digna is geïmplementeerd met het OIDC-protocol. Meerdere identity providers kunnen parallel worden geconfigureerd door twee belangrijke configuratiebestanden aan te passen:

- **`dashboard_config.toml`** — Stuurt de frontend login-interface
- **`config.toml`** — Configureert de backend OIDC-verbindingen

### Ondersteunde providers {: #supported-providers-overview }

De voorbeelden in deze gids gebruiken **Microsoft** en **Google**, maar **elke OIDC-conforme provider** kan worden geïntegreerd met dezelfde structuur.

Veelvoorkomende OIDC-providers zijn:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Andere OIDC-conforme identity providers

---

## Configuration Steps {: #configuration-steps }

SSO-configuratie vereist aanpassingen in twee bestanden. Deze sectie legt uit hoe je elk bestand configureert.

### Overzicht van configuratiebestanden

| Bestand | Locatie | Doel |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login-interface |
| **config.toml** | `/config.toml` | Backend OIDC-verbindingen |

Beide bestanden moeten correct worden geconfigureerd om SSO te laten werken.

---

## Dashboard Configuration {: #dashboard-configuration }

### Bestandslocatie

```
dashboard/dashboard_config.toml
```

### Stap 1: Voeg OIDC-providers toe

Voeg entries toe onder de `[[login.oidc]]` array voor elke identity provider die je wilt ondersteunen.

**Voorbeeld met Microsoft en Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Stap 2: Configureer login-opties

Geef op of wachtwoordgebaseerde login toegestaan moet zijn:

```toml
[login]
usePassword = true
```

### Configuratieparameters

#### `[[login.oidc]]` Sectie

| Parameter | Type | Verplicht | Beschrijving |
|---|---|---|---|
| `key` | string | Ja | Unieke identificatie voor de OIDC-verbinding (moet overeenkomen met key in config.toml) |
| `label` | string | Ja | Tekst die op de loginknop wordt weergegeven (bijv. "Login with Microsoft") |

#### `[login]` Sectie

| Parameter | Type | Standaard | Beschrijving |
|---|---|---|---|
| `usePassword` | boolean | false | Sta wachtwoordgebaseerde login toe naast SSO |

### Begrip van usePassword

**Als `usePassword = true`:**
- Het login-scherm toont SSO-knoppen (bijv. "Login with Microsoft")
- Het login-scherm toont ook velden voor gebruikersnaam en wachtwoord
- Gebruikers kunnen via beide methoden authenticeren
- Maakt hybride setups mogelijk waarin sommige gebruikers SSO gebruiken en anderen wachtwoorden

**Als `usePassword = false` (of weggelaten):**
- Het login-scherm toont alleen SSO-knoppen
- Geen gebruikersnaam/wachtwoordvelden
- Alleen OIDC-authenticatie is beschikbaar

!!! tip "Tip"

    Wachtwoordgebaseerde login is alleen beschikbaar voor gebruikers die zijn aangemaakt met wachtwoorden via het `digna user add` commando of via het dashboard.

### Volledig voorbeeld

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

### Bestandslocatie

```
/config.toml
```

(Root van de digna-installatiemap)

### Stap 1: Voeg OIDC-providersecties toe

Elke provider moet een eigen `[oidc.<key>]` sectie hebben. De key moet overeenkomen met de `key` die is gedefinieerd in `dashboard_config.toml`.

### Microsoft-configuratie

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google-configuratie

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Configuratieparameters

| Parameter | Type | Verplicht | Beschrijving | Voorbeeld |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client ID van de identity provider | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client secret van de identity provider | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL na authenticatie | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-configuratie-eindpunt | `https://login.microsoftonline.com/...` |

!!! warning "Belangrijk"

    Vervang placeholder-waarden (`<client_id>`, `<client_secret>`, `<tenant_id>`) door echte gegevens uit het developer- of app-portaal van je identity provider.

### Redirect URI

De redirect URI moet hetzelfde zijn als in de configuratie van je identity provider:

```
http://localhost:5173/oidc/callback
```

Als digna op een ander domein wordt gehost, werk deze dan overeenkomstig bij:
- Lokaal: `http://localhost:5173/oidc/callback`
- Productie: `https://digna.yourdomain.com/oidc/callback`

### Volledig voorbeeld

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

Na het voltooien van de configuratie, verifieer dat SSO correct werkt.

### Pre-test checklist

Zorg vóór het testen dat:

- [ ] `dashboard_config.toml` is bijgewerkt met OIDC-providers
- [ ] `config.toml` is bijgewerkt met OIDC-credentials
- [ ] Beide bestanden zijn opgeslagen
- [ ] Credentials kloppen (client ID, client secret)
- [ ] Redirect URI komt overeen met je deployment-URL
- [ ] Identity provider-applicatie is geconfigureerd met de redirect URI

### Teststappen

#### Stap 1: Herstart services

Herstart de digna-backend en webserver om wijzigingen toe te passen.

**Als uitgevoerd als Windows-service:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Als handmatig uitgevoerd:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Als je IIS of Tomcat gebruikt:**
Herstart je webserver-service.

#### Stap 2: Open het dashboard

Open het digna-dashboard in je browser:

```
http://localhost:5173
```

(of je geconfigureerde dashboard-URL)

#### Stap 3: Controleer loginknoppen

Controleer of loginknoppen verschijnen voor elke geconfigureerde provider:

- Je zou de knop "Login with Microsoft" moeten zien
- Je zou de knop "Login with Google" moeten zien
- (Als usePassword = true) Je zou velden voor gebruikersnaam/wachtwoord moeten zien

Als knoppen niet verschijnen:
- Controleer of `dashboard_config.toml` is opgeslagen
- Controleer of de dashboard-service is herstart
- Bekijk de browserconsole (F12) op fouten

#### Stap 4: Test SSO-login

Klik op een van de SSO-knoppen (bijv. "Login with Microsoft"):

1. Je zou worden doorgestuurd naar de inlogpagina van de identity provider
2. Log in met je bedrijfsreferenties
3. Je zou teruggestuurd moeten worden naar digna
4. Je zou ingelogd moeten zijn op digna

#### Stap 5: Verifieer gebruikersaanmaak

Na een succesvolle SSO-login:

- Gebruiker zou automatisch in digna moeten worden aangemaakt
- Gebruiker zou ingelogd moeten zijn
- Het gebruikersprofiel zou je identity-providergegevens moeten weergeven
- Je zou het digna-dashboard moeten zien

#### Stap 6: Test wachtwoordlogin (indien ingeschakeld)

Als `usePassword = true`:

1. Log uit van digna
2. Vul op de loginpagina een gebruikersnaam en wachtwoord in
3. Je zou moeten kunnen inloggen met wachtwoordgegevens

---

## Troubleshooting {: #troubleshooting }

### Loginknoppen verschijnen niet

**Symptomen:**
- OIDC-loginknoppen niet zichtbaar op de loginpagina
- Alleen wachtwoordvelden te zien (als usePassword = true)

**Oorzaken & Oplossingen:**
1. Controleer of `dashboard_config.toml` in de `dashboard/` map staat
2. Verifieer dat `[[login.oidc]]` secties aanwezig zijn met correcte syntax
3. Herstart de dashboard-service
4. Maak de browsercache leeg (Ctrl+Shift+Delete of Cmd+Shift+Delete)
5. Controleer de browserconsole (F12 → Console tab) op fouten

---

### Redirect URI mismatch-fout

**Symptomen:**
- Na klikken op SSO-knop fout over "redirect_uri mismatch"
- "The redirect URI is not registered" foutmelding

**Oorzaken & Oplossingen:**
1. Verifieer dat `DIGNA_OIDC_REDIRECT_URI` in `config.toml` correct is
2. Controleer of de redirect URI is geregistreerd in de instellingen van de identity provider
3. Zorg dat beide identieke URLs gebruiken (inclusief protocol, domein, pad)
4. Controleer op typfouten in de redirect URI
5. Als je HTTPS gebruikt, zorg dat het certificaat geldig is

---

### Ongeldige client-credentials fout

**Symptomen:**
- "Invalid client ID or secret" fout
- Authenticatie faalt met credential-fout

**Oorzaken & Oplossingen:**
1. Verifieer dat `DIGNA_OIDC_CLIENT_ID` en `DIGNA_OIDC_CLIENT_SECRET` correct zijn
2. Zorg dat er geen extra spaties of onbedoelde karakters aanwezig zijn
3. Controleer of de credentials niet verlopen of ingetrokken zijn
4. Herstart de backend-service na het bijwerken van de config
5. Controleer de identity provider-console om te bevestigen dat de credentials actief zijn

---

### Login blijft hangen of time-out

**Symptomen:**
- Klikken op SSO-knop doet niets
- Time-out na enkele seconden
- Browser toont "Failed to connect" of soortgelijke melding

**Oorzaken & Oplossingen:**
1. Verifieer dat de digna-backend draait: `digna repo check`
2. Controleer netwerkconnectiviteit naar de identity provider
3. Verifieer dat `DIGNA_OIDC_CONFIGURATION_URL` bereikbaar is
4. Controleer firewallregels die uitgaande HTTPS-verbindingen kunnen blokkeren
5. Controleer dat backend en dashboard elkaar kunnen bereiken

---

### Gebruikers worden niet automatisch aangemaakt

**Symptomen:**
- SSO-login slaagt maar gebruiker wordt niet in digna aangemaakt
- Krijg permissiefout na SSO-login

**Oorzaken & Oplossingen:**
1. Verifieer dat de OIDC-configuratie correct is
2. Controleer of gebruikerspermissies goed zijn ingesteld
3. Bekijk digna-logs voor foutmeldingen
4. Herstart de backend-service
5. Neem contact op met support@digna.ai als het probleem aanhoudt

---

## Supported Providers {: #supported-providers }

### Getest & ondersteund

De volgende OIDC-providers zijn getest en werken:

| Provider | Configuratie-URL | Setupgids |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Andere OIDC-providers

Elke provider die OpenID Connect ondersteunt kan worden geïntegreerd. Benodigde informatie:

- Client ID
- Client secret
- OpenID-configuratie-URL (meestal op `/.well-known/openid-configuration`)
- Ondersteunde scopes (typisch `openid profile email`)

Neem contact op met support@digna.ai als je hulp nodig hebt bij het integreren van een specifieke provider.

---

## Best Practices

**DO:**
- Gebruik HTTPS in productie (niet HTTP)
- Bewaar client secrets veilig (gebruik indien mogelijk omgevingsvariabelen)
- Verwissel secrets periodiek
- Test eerst in een niet-productieomgeving
- Documenteer welke providers zijn geconfigureerd
- Monitor loginlogs op ongewoon gedrag
- Houd de identity provider-configuratie in sync met de digna-config

**DON'T:**
- Bewaar client secrets in versiebeheer
- Gebruik HTTP-redirect-URI's in productie
- Configureer meerdere providers met dezelfde key
- Laat standaard/test-credentials in productie staan
- Maak configbestanden met secrets publiek
- Meng ontwikkel- en productiecredentials

---

## Support

Heb je hulp nodig bij SSO-configuratie?

- **Email:** support@digna.ai
- **Documentatie:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Laatst bijgewerkt:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**