---
title: Översikt över Single Sign-On (SSO) | digna Dokumentation
description: Så fungerar Single Sign-On i digna med OpenID Connect (OIDC). Omfattar konfiguration av dashboard och backend, testning, felsökning samt länkar till installationsguider per leverantör för Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne och AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc-integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta-integration
  - företagsautentisering
lang: sv
robots: index, follow
og_title: Guide för Single Sign-On (SSO)-integration i digna
og_description: Konfigurera Single Sign-On för digna med OpenID Connect. Steg-för-steg-konfiguration för Microsoft Entra ID, Google Workspace, Okta och andra identitetsleverantörer som följer OIDC-standarden.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Översikt över Single Sign-On

---

## Innehållsförteckning

1. [Introduktion och översikt](#introduction-and-overview)
2. [Guider per leverantör](#provider-guides)
3. [Konfigurationssteg](#configuration-steps)
4. [Konfiguration av dashboarden](#dashboard-configuration)
5. [Konfiguration av backenden](#backend-configuration)
6. [Testa inloggningen](#testing-login)
7. [Felsökning](#troubleshooting)
8. [Leverantörer som stöds](#supported-providers)

---

## Introduktion och översikt {: #introduction-and-overview }

Denna guide ger steg-för-steg-instruktioner för att integrera Single Sign-On (SSO) med digna-plattformen via **OpenID Connect (OIDC)**.

### Vad är SSO?

Single Sign-On låter användare logga in säkert i digna med sina företagsuppgifter via externa identitetsleverantörer. Användarna kan autentisera sig med sina företagsinloggningar i stället för att hantera separata lösenord för digna.

### Så fungerar det

SSO i digna är implementerat med OIDC-protokollet. Flera identitetsleverantörer kan konfigureras parallellt genom att justera två centrala konfigurationsfiler:

- **`dashboard_config.toml`** — styr inloggningsgränssnittet i frontend
- **`config.toml`** — konfigurerar OIDC-anslutningarna i backend

### Leverantörer som stöds {: #supported-providers-overview }

Exemplen i denna guide använder **Microsoft** och **Google**, men **alla leverantörer som följer OIDC-standarden** kan integreras enligt samma struktur.

---

## Guider per leverantör {: #provider-guides }

Varje leverantör behöver samma fyra värden — ett klient-ID, en klienthemlighet, en redirect URI och en discovery-URL — men var och en placerar dem på olika ställen i sin administrationskonsol, och flera har ett leverantörsspecifikt steg som de andra saknar. Guiderna nedan täcker den delen av arbetet; denna sida täcker digna-delen, som är identisk för alla.

| Leverantör | Guide | Bra att veta |
|---|---|---|
| **AD FS** | [Ställ in SSO med AD FS](adfs_sso_guide.md) | Egenhostad; den enda leverantören här där du själv kontrollerar tokentjänsten |
| **Auth0** | [Ställ in SSO med Auth0](auth0_sso_guide.md) | Discovery-URL:en är per tenant, och anpassade domäner ändrar den |
| **Google Workspace** | [Ställ in SSO med Google Workspace](google_workspace_sso_guide.md) | Samtyckesskärmen måste publiceras innan andra än testanvändare kan logga in |
| **Keycloak** | [Ställ in SSO med Keycloak](keycloak_sso_guide.md) | Egenhostad; discovery-URL:en är per realm |
| **Microsoft Entra ID** | [Ställ in SSO med Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant-ID:t ingår i discovery-URL:en; hemligheter går ut |
| **Okta** | [Ställ in SSO med Okta](okta_sso_guide.md) | Valet av auktoriseringsserver ändrar discovery-URL:en |
| **OneLogin** | [Ställ in SSO med OneLogin](onelogin_sso_guide.md) | OIDC-apptypen måste väljas när appen skapas och kan inte ändras |
| **PingOne** | [Ställ in SSO med PingOne](pingone_sso_guide.md) | Miljö-ID:t ingår i discovery-URL:en |

Alla andra leverantörer som följer OIDC-standarden fungerar på samma sätt — se [Andra OIDC-leverantörer](#supported-providers).

---

## Konfigurationssteg {: #configuration-steps }

SSO-konfigurationen kräver ändringar i två filer. Detta avsnitt förklarar hur var och en konfigureras.

### Översikt över konfigurationsfilerna

| Fil | Plats | Syfte |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Inloggningsgränssnitt i frontend |
| **config.toml** | `/config.toml` | OIDC-anslutningar i backend |

Båda filerna måste konfigureras för att SSO ska fungera korrekt.

---

## Konfiguration av dashboarden {: #dashboard-configuration }

### Filens plats

```
dashboard/dashboard_config.toml
```

### Steg 1: Lägg till OIDC-leverantörer

Lägg till poster under arrayen `[[login.oidc]]` för varje identitetsleverantör som du vill stödja.

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

#### Avsnittet `[[login.oidc]]`

| Parameter | Typ | Obligatorisk | Beskrivning |
|---|---|---|---|
| `key` | string | Ja | Unik identifierare för OIDC-anslutningen (måste matcha key i config.toml) |
| `label` | string | Ja | Text som visas på inloggningsknappen (t.ex. "Login with Microsoft") |

#### Avsnittet `[login]`

| Parameter | Typ | Standard | Beskrivning |
|---|---|---|---|
| `usePassword` | boolean | false | Tillåt lösenordsbaserad inloggning utöver SSO |

### Förstå usePassword

**Om `usePassword = true`:**
- Inloggningsskärmen visar SSO-knappar (t.ex. "Login with Microsoft")
- Inloggningsskärmen visar även fält för användarnamn och lösenord
- Användarna kan autentisera sig med vilken metod som helst
- Möjliggör hybridupplägg där vissa användare använder SSO och andra lösenord

**Om `usePassword = false` (eller utelämnat):**
- Inloggningsskärmen visar endast SSO-knappar
- Inga fält för användarnamn/lösenord
- Endast OIDC-autentisering är tillgänglig

!!! tip "Tips"

    Lösenordsbaserad inloggning är endast tillgänglig för användare som skapats med lösenord via kommandot `digna user add` eller via dashboarden.

### Fullständigt exempel

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

## Konfiguration av backenden {: #backend-configuration }

### Filens plats

```
/config.toml
```

(Rotkatalogen för digna-installationen)

### Steg 1: Lägg till avsnitt för OIDC-leverantörer

Varje leverantör måste ha ett eget avsnitt `[oidc_clients.<key>]`. Nyckeln måste matcha den `key` som definierats i `dashboard_config.toml`.

### Konfiguration för Microsoft

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Konfiguration för Google

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurationsparametrar

| Parameter | Typ | Obligatorisk | Beskrivning | Exempel |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Klient-ID från identitetsleverantören | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Klienthemlighet från identitetsleverantören | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL efter autentisering | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-konfigurationsendpoint | `https://login.microsoftonline.com/...` |

!!! warning "Viktigt"

    Ersätt platshållarvärdena (`<client_id>`, `<client_secret>`, `<tenant_id>`) med de faktiska uppgifterna från din identitetsleverantörs utvecklarportal.

### Redirect URI

Redirect URI:n måste vara densamma i konfigurationen hos din identitetsleverantör:

```
http://localhost:5173/oidc/callback
```

Om digna körs på en annan domän, uppdatera därefter:
- Lokalt: `http://localhost:5173/oidc/callback`
- Produktion: `https://digna.yourdomain.com/oidc/callback`

### Fullständigt exempel

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Testa inloggningen {: #testing-login }

När konfigurationen är klar, kontrollera att SSO fungerar korrekt.

### Checklista före testning

Säkerställ före testningen att:

- [ ] `dashboard_config.toml` har uppdaterats med OIDC-leverantörer
- [ ] `config.toml` har uppdaterats med OIDC-uppgifter
- [ ] Båda filerna har sparats
- [ ] Uppgifterna är korrekta (klient-ID, klienthemlighet)
- [ ] Redirect URI:n matchar din installations-URL
- [ ] Applikationen hos identitetsleverantören är konfigurerad med redirect URI:n

### Teststeg

#### Steg 1: Starta om tjänsterna

Starta om digna-backenden och webbservern för att tillämpa ändringarna.

**Om digna körs som en tjänst på Windows:**
```bash
cd C:\path\to\digna
digna windows stop
digna windows start
```

**Om digna körs som en tjänst på Linux eller macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Om digna körs manuellt:**
```bash
digna serve --address localhost --port 8082
```

**Starta även om webbservern** — IIS eller Tomcat på Windows, nginx eller Apache på Linux och macOS.

#### Steg 2: Öppna dashboarden

Öppna digna-dashboarden i din webbläsare:

```
http://localhost:5173
```

(eller din konfigurerade dashboard-URL)

#### Steg 3: Kontrollera inloggningsknapparna

Kontrollera att inloggningsknappar visas för varje konfigurerad leverantör:

- Knappen "Login with Microsoft" ska visas
- Knappen "Login with Google" ska visas
- (Om usePassword = true) Fält för användarnamn/lösenord ska visas

Om knapparna inte visas:
- Kontrollera att `dashboard_config.toml` har sparats
- Kontrollera att dashboard-tjänsten har startats om
- Kontrollera webbläsarens konsol (F12) efter fel

#### Steg 4: Testa SSO-inloggning

Klicka på en av SSO-knapparna (t.ex. "Login with Microsoft"):

1. Du ska omdirigeras till identitetsleverantörens inloggningssida
2. Logga in med dina företagsuppgifter
3. Du ska omdirigeras tillbaka till digna
4. Du ska vara inloggad i digna

#### Steg 5: Kontrollera att användaren skapats

Efter en lyckad SSO-inloggning:

- Användaren ska ha skapats automatiskt i digna
- Användaren ska vara inloggad
- Användarprofilen ska visa uppgifterna från din identitetsleverantör
- Du ska se digna-dashboarden

#### Steg 6: Testa lösenordsinloggning (om aktiverad)

Om `usePassword = true`:

1. Logga ut från digna
2. Ange ett användarnamn och lösenord på inloggningssidan
3. Du ska kunna logga in med lösenordsuppgifterna

---

## Felsökning {: #troubleshooting }

### Inloggningsknapparna visas inte

**Symtom:**
- OIDC-inloggningsknapparna syns inte på inloggningssidan
- Endast lösenordsfälten visas (om usePassword = true)

**Orsaker och lösningar:**
1. Kontrollera att `dashboard_config.toml` ligger i katalogen `dashboard/`
2. Kontrollera att avsnitten `[[login.oidc]]` finns och har korrekt syntax
3. Starta om dashboard-tjänsten
4. Rensa webbläsarens cache (Ctrl+Shift+Delete eller Cmd+Shift+Delete)
5. Kontrollera webbläsarens konsol (F12 → fliken Console) efter fel

---

### Fel om redirect URI mismatch

**Symtom:**
- Efter klick på SSO-knappen visas ett fel om "redirect_uri mismatch"
- Felet "The redirect URI is not registered"

**Orsaker och lösningar:**
1. Kontrollera att `DIGNA_OIDC_REDIRECT_URI` i `config.toml` är korrekt
2. Kontrollera att redirect URI:n är registrerad i identitetsleverantörens inställningar
3. Säkerställ att båda använder identiska URL:er (inklusive protokoll, domän och sökväg)
4. Kontrollera om det finns stavfel i redirect URI:n
5. Om du använder HTTPS, säkerställ att certifikatet är giltigt

---

### Fel om ogiltiga klientuppgifter

**Symtom:**
- Felet "Invalid client ID or secret"
- Autentiseringen misslyckas med ett fel om inloggningsuppgifter

**Orsaker och lösningar:**
1. Kontrollera att `DIGNA_OIDC_CLIENT_ID` och `DIGNA_OIDC_CLIENT_SECRET` är korrekta
2. Säkerställ att det inte finns extra mellanslag eller specialtecken
3. Kontrollera att uppgifterna inte har gått ut eller återkallats
4. Starta om backend-tjänsten efter att konfigurationen uppdaterats
5. Kontrollera i identitetsleverantörens konsol att uppgifterna är aktiva

---

### Inloggningen hänger sig eller får timeout

**Symtom:**
- Ett klick på SSO-knappen gör ingenting
- Timeout efter flera sekunder
- Webbläsaren visar "Failed to connect" eller liknande

**Orsaker och lösningar:**
1. Kontrollera att digna-backenden körs: `digna repo check`
2. Kontrollera nätverksanslutningen till identitetsleverantören
3. Kontrollera att `DIGNA_OIDC_CONFIGURATION_URL` är nåbar
4. Kontrollera att brandväggsreglerna tillåter utgående HTTPS-anslutningar
5. Kontrollera att backend och dashboard kan nå varandra

---

### Användare skapas inte automatiskt

**Symtom:**
- SSO-inloggningen lyckas men användaren skapas inte i digna
- Ett behörighetsfel visas efter SSO-inloggningen

**Orsaker och lösningar:**
1. Kontrollera att OIDC-konfigurationen är korrekt
2. Kontrollera att användarbehörigheterna är konfigurerade
3. Gå igenom digna-loggarna efter felmeddelanden
4. Starta om backend-tjänsten
5. Kontakta support@digna.ai om problemet kvarstår

---

## Leverantörer som stöds {: #supported-providers }

### Testade och stödda

Följande OIDC-leverantörer har testats och är kända för att fungera:

| Leverantör | Konfigurations-URL | Installationsguide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Ställ in SSO med AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Ställ in SSO med Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Ställ in SSO med Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Ställ in SSO med Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Ställ in SSO med Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Ställ in SSO med Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Ställ in SSO med OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Ställ in SSO med PingOne](pingone_sso_guide.md) |

### Andra OIDC-leverantörer

Alla leverantörer som stöder OpenID Connect kan integreras. Nödvändig information:

- Klient-ID
- Klienthemlighet
- OpenID-konfigurations-URL (oftast under `/.well-known/openid-configuration`)
- Scopes som stöds (vanligtvis `openid profile email`)

Kontakta support@digna.ai om du behöver hjälp att integrera en viss leverantör.

---

## Bästa praxis

**GÖR:**
- Använd HTTPS i produktion (inte HTTP)
- Förvara klienthemligheter säkert (använd miljövariabler om möjligt)
- Rotera hemligheter regelbundet
- Testa först i en miljö som inte är produktion
- Dokumentera vilka leverantörer som är konfigurerade
- Övervaka inloggningsloggarna efter ovanlig aktivitet
- Håll konfigurationen hos identitetsleverantören synkroniserad med digna-konfigurationen

**GÖR INTE:**
- Lagra klienthemligheter i versionshantering
- Använda HTTP-redirect-URI:er i produktion
- Konfigurera flera leverantörer med samma key
- Lämna standard- eller testuppgifter kvar i produktion
- Exponera konfigurationsfiler som innehåller hemligheter
- Blanda uppgifter för utveckling och produktion

---

## Support

Behöver du hjälp med SSO-konfigurationen?

- **E-post:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Webbplats:** https://www.digna.ai

---

**Senast uppdaterad:** 30 augusti 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
