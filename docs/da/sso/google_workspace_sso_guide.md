---
title: Google Workspace SSO – Single Sign-On-integration | digna Dokumentation
description: Konfigurer Single Sign-On for digna med Google Workspace ved hjælp af OpenID Connect — OAuth-samtykkeskærm, OAuth-klient-id, autoriserede redirect-URI'er og den tilsvarende digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth samtykkeskærm, openid connect, virksomhedsautentificering
---

# Opsæt SSO med Google Workspace

Googles identitetsplatform er OIDC-kompatibel og bruger en enkelt, velkendt discovery-URL for alle kunder, så de eneste værdier, der er per organisation, er client ID og secret.

Denne vejledning dækker **Google-delen**: oprettelse af OAuth-klienten og indsamling af de værdier, digna har brug for. Digna-delen — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og beskrives i [Oversigt: Single Sign-On](overview.md).

---

## Før du går i gang

| Krav | Bemærkninger |
|---|---|
| **Google Cloud project** | Ethvert projekt i samme organisation som dit Workspace-domæne |
| **Role** | Editor eller Owner på projektet |
| **digna redirect URI** | URL'en, brugerne returnerer til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Konfigurer OAuth-samtykkeskærmen

Google udsteder ikke legitimationsoplysninger, før samtykkeskærmen er oprettet.

1. Åbn [Google Cloud Console](https://console.cloud.google.com) og vælg dit projekt
2. Gå til **APIs & Services → OAuth consent screen**
3. Vælg brugertype:
   - **Internal** — kun konti i dit Workspace-domæne kan logge ind. Anbefales.
   - **External** — enhver Google-konto kan forsøge at logge ind.
4. Udfyld app-navn, bruger-support-email og udviklerkontakt-email
5. På **Scopes**-trinet, tilføj `openid`, `.../auth/userinfo.email` og `.../auth/userinfo.profile`
6. Gem

!!! warning "Eksterne apps skal publiceres"

    En **External** samtykkeskærm starter i *Testing*-status, hvor kun de konti, der eksplicit er tilføjet test-brugerliste, kan gennemføre et login. Alle andre ser "digna has not completed the Google verification process". Enten skift appen til **In production** under **Publishing status**, eller brug **Internal** — som ikke har denne begrænsning og er det rigtige valg for en Workspace-only-udrulning.

---

## Trin 2: Opret OAuth-klienten

1. Gå til **APIs & Services → Credentials**
2. Klik **Create Credentials → OAuth client ID**
3. Sæt **Application type** til **Web application**
4. Giv den et navn, f.eks. `digna`
5. Under **Authorized redirect URIs**, klik **Add URI** og indtast:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klik **Create**

!!! note "Autoriserede JavaScript-origin'er er ikke nødvendige"

    digna udveksler autorisationskoden fra backend, ikke browseren, så feltet **Authorized JavaScript origins** kan stå tomt. Kun redirect-URI'en har betydning.

---

## Trin 3: Indsaml legitimationsoplysninger

Dialogboksen, der vises efter oprettelsen, viser:

- **Client ID** — slutter på `.apps.googleusercontent.com` → bliver `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → bliver `DIGNA_OIDC_CLIENT_SECRET`

Begge kan hentes senere fra credential-detaljesiden, i modsætning til de fleste andre udbydere.

---

## Trin 4: Discovery-URL'en

Google bruger én discovery-URL for alle kunder — der er intet, der skal erstattes:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Trin 5: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Værdien `key` i begge filer skal matche — `google` her.

---

## Trin 6: Test

Genstart backend og webserver, og åbn derefter dashboardet. Se [Test af login](overview.md#testing-login) for den komplette tjekliste.

---

## Fejlfinding for Google Workspace

### Fejl 400: redirect_uri_mismatch

URI'en i `DIGNA_OIDC_REDIRECT_URI` er ikke på listen over **Authorized redirect URIs**, eller den adskiller sig ved en afsluttende skråstreg eller scheme. Googles fejlside viser den URI, den modtog — sammenlign den tegn for tegn med den registrerede.

### Denne app er blokeret / har ikke gennemført verifikation

Samtykkeskærmen er **External** og stadig i *Testing*. Publicer den, eller skift appen til **Internal**.

### Adgang blokeret: Autorisationsfejl

Kontoen, der forsøger at logge ind, er uden for dit Workspace-domæne, mens samtykkeskærmen er **Internal**. Dette er forventet adfærd — Internal-apps accepterer kun konti i organisationen.

### Ændringer tager flere minutter

Google propagere ændringer i legitimationsoplysninger og samtykkeskærm asynkront. En nyligt tilføjet redirect-URI kan tage et par minutter om at træde i kraft; hvis en ændring ser ud til at blive ignoreret, vent og prøv igen, før du undersøger yderligere.

---

## Se også

- [Oversigt: Single Sign-On](overview.md) — konfigurationsreference, test og generel fejlfinding
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)