---
title: Single Sign-On (SSO) Oversigt | digna Dokumentation
description: Hvordan Single Sign-On fungerer i digna ved hjælp af OpenID Connect (OIDC). Dækker dashboard- og backend-konfiguration, test, fejlfinding og links til opsætningsvejledninger per udbyder for Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne og AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - Single Sign-On
  - OIDC-integration
  - OpenID Connect
  - Microsoft Entra ID
  - Azure AD SSO
  - Google Workspace SSO
  - Okta-integration
  - virksomhedsautentificering
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Oversigt

---

## Indholdsfortegnelse

1. [Introduktion og oversigt](#introduction-and-overview)
2. [Udbydervejledninger](#provider-guides)
3. [Konfigurationstrin](#configuration-steps)
4. [Dashboard-konfiguration](#dashboard-configuration)
5. [Backend-konfiguration](#backend-configuration)
6. [Test af login](#testing-login)
7. [Fejlfinding](#troubleshooting)
8. [Understøttede udbydere](#supported-providers)

---

## Introduktion og oversigt {: #introduction-and-overview }

Denne vejledning giver trin-for-trin instruktioner til at integrere Single Sign-On (SSO) med digna-platformen ved hjælp af **OpenID Connect (OIDC)**.

### Hvad er SSO?

Single Sign-On giver brugere mulighed for at logge sikkert ind på digna ved at bruge deres virksomhedslegitimationsoplysninger gennem eksterne identitetsudbydere. Brugere kan godkende med deres virksomhedsoplysninger i stedet for at administrere separate digna-adgangskoder.

### Hvordan det virker

SSO i digna er implementeret ved hjælp af OIDC-protokollen. Flere identitetsudbydere kan konfigureres parallelt ved at justere to nøglekonfigurationsfiler:

- **`dashboard_config.toml`** — Styrer frontend-logingrænsefladen
- **`config.toml`** — Konfigurerer backend OIDC-forbindelser

### Understøttede udbydere {: #supported-providers-overview }

Eksempler i denne vejledning bruger **Microsoft** og **Google**, men **enhver OIDC-kompatibel udbyder** kan integreres ved at følge samme struktur.

---

## Udbydervejledninger {: #provider-guides }

Hver udbyder har brug for de samme fire værdier — en client ID, en client secret, en redirect URI og en discovery URL — men hver enkelt placerer dem forskellige steder i sin administrationskonsol, og flere har et udbyderspecifikt trin, som de andre ikke har. Vejledningerne nedenfor dækker den del af arbejdet; denne side dækker digna-delen, som er identisk for alle.

| Udbyder | Guide | Godt at vide |
|---|---|---|
| **AD FS** | [Konfigurer SSO med AD FS](adfs_sso_guide.md) | Selvhostet; den eneste udbyder her, hvor du styrer token-servicen |
| **Auth0** | [Konfigurer SSO med Auth0](auth0_sso_guide.md) | Discovery URL er per-tenant, og brugerdefinerede domæner ændrer den |
| **Google Workspace** | [Konfigurer SSO med Google Workspace](google_workspace_sso_guide.md) | Samtykkeskærmen skal publiceres før ikke-testbrugere kan logge ind |
| **Keycloak** | [Konfigurer SSO med Keycloak](keycloak_sso_guide.md) | Selvhostet; discovery URL er per-realm |
| **Microsoft Entra ID** | [Konfigurer SSO med Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID vises i discovery URL; secrets udløber |
| **Okta** | [Konfigurer SSO med Okta](okta_sso_guide.md) | Valg af authorization server ændrer discovery URL |
| **OneLogin** | [Konfigurer SSO med OneLogin](onelogin_sso_guide.md) | OIDC-app-typen skal vælges ved oprettelse og kan ikke ændres |
| **PingOne** | [Konfigurer SSO med PingOne](pingone_sso_guide.md) | Environment ID vises i discovery URL |

Enhver anden OIDC-kompatibel udbyder fungerer på samme måde — se [Andre OIDC-udbydere](#supported-providers).

---

## Konfigurationstrin {: #configuration-steps }

SSO-konfiguration kræver opdateringer til to filer. Dette afsnit forklarer, hvordan hver enkelt konfigureres.

### Oversigt over konfigurationsfiler

| Fil | Placering | Formål |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend-logingrænseflade |
| **config.toml** | `/config.toml` | Backend OIDC-forbindelser |

Begge filer skal konfigureres for at SSO fungerer korrekt.

---

## Dashboard-konfiguration {: #dashboard-configuration }

### Filplacering

```
dashboard/dashboard_config.toml
```

### Trin 1: Tilføj OIDC-udbydere

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

### Trin 2: Konfigurer loginmuligheder

Angiv, om login baseret på adgangskode skal være tilladt:

```toml
[login]
usePassword = true
```

### Konfigurationsparametre

#### `[[login.oidc]]`-sektionen

| Parameter | Type | Påkrævet | Beskrivelse |
|---|---|---|---|
| `key` | string | Ja | Unik identifikator for OIDC-forbindelsen (skal matche key i config.toml) |
| `label` | string | Ja | Tekst vist på loginknappen (f.eks. "Login with Microsoft") |

#### `[login]`-sektionen

| Parameter | Type | Standard | Beskrivelse |
|---|---|---|---|
| `usePassword` | boolean | false | Tillad login baseret på adgangskode ud over SSO |

### Forstå usePassword

**Hvis `usePassword = true`:**
- Login-skærmen viser SSO-knapper (f.eks. "Login with Microsoft")
- Login-skærmen viser også brugernavn- og adgangskodefelter
- Brugere kan godkende med enten metode
- Giver hybride opsætninger, hvor nogle brugere bruger SSO og andre bruger adgangskoder

**Hvis `usePassword = false` (eller udeladt):**
- Login-skærmen viser kun SSO-knapper
- Ingen brugernavn-/adgangskodefelter
- Kun OIDC-godkendelse er tilgængelig

!!! tip "Tip"

    Login med adgangskode er kun tilgængeligt for brugere, som blev oprettet med adgangskoder ved hjælp af kommandoen `digna user add` eller via dashboardet.

### Færdigt eksempel

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

## Backend-konfiguration {: #backend-configuration }

### Filplacering

```
/config.toml
```

(Rodmappen for digna-installationen)

### Trin 1: Tilføj OIDC-udbydersektioner

Hver udbyder skal have en dedikeret `[oidc.<key>]`-sektion. Key'en skal matche `key` defineret i `dashboard_config.toml`.

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

### Konfigurationsparametre

| Parameter | Type | Påkrævet | Beskrivelse | Eksempel |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client ID fra identitetsudbyderen | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client secret fra identitetsudbyderen | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL efter godkendelse | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-konfigurationsendpoint | `https://login.microsoftonline.com/...` |

!!! warning "Vigtigt"

    Erstat pladsholderværdier (`<client_id>`, `<client_secret>`, `<tenant_id>`) med faktiske legitimationsoplysninger fra din identitetsudbyders developer-konsol.

### Redirect URI

Redirect URI skal være den samme i din identitetsudbyderkonfiguration:

```
http://localhost:5173/oidc/callback
```

Hvis digna hostes på et andet domæne, opdater tilsvarende:
- Lokalt: `http://localhost:5173/oidc/callback`
- Produktion: `https://digna.yourdomain.com/oidc/callback`

### Færdigt eksempel

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

## Test af login {: #testing-login }

Efter at have gennemført konfigurationen, bekræft at SSO fungerer korrekt.

### Tjekliste før test

Før test, sørg for:

- [ ] `dashboard_config.toml` er opdateret med OIDC-udbydere
- [ ] `config.toml` er opdateret med OIDC-legitimationsoplysninger
- [ ] Begge filer er gemt
- [ ] Legitimationsoplysninger er korrekte (client ID, client secret)
- [ ] Redirect URI matcher din deployment-URL
- [ ] Identitetsudbyder-applikationen er konfigureret med redirect URI

### Testtrin

#### Trin 1: Genstart tjenester

Genstart digna-backend og webserver for at anvende ændringerne.

**Hvis kørt som service på Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Hvis kørt som service på Linux eller macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Hvis kørt manuelt:**
```bash
digna serve --address localhost --port 8082
```

**Genstart også webserveren** — IIS eller Tomcat på Windows, nginx eller Apache på Linux og macOS.

#### Trin 2: Åbn dashboard

Åbn digna-dashboardet i din browser:

```
http://localhost:5173
```

(eller din konfigurerede dashboard-URL)

#### Trin 3: Bekræft loginknapper

Kontroller, at loginknapper vises for hver konfigureret udbyder:

- Du bør se "Login with Microsoft"-knappen
- Du bør se "Login with Google"-knappen
- (Hvis usePassword = true) Du bør se brugernavn-/adgangskodefelter

Hvis knapper ikke vises:
- Tjek at `dashboard_config.toml` blev gemt
- Tjek at dashboard-tjenesten blev genstartet
- Tjek browserkonsollen (F12) for fejl

#### Trin 4: Test SSO-login

Klik på en af SSO-knapperne (f.eks. "Login with Microsoft"):

1. Du bør blive omdirigeret til identitetsudbyderens login-side
2. Log ind med dine virksomhedslegitimationsoplysninger
3. Du bør blive omdirigeret tilbage til digna
4. Du bør være logget ind i digna

#### Trin 5: Bekræft brugeroprettelse

Efter succesfuldt SSO-login:

- Brugeren bør blive oprettet automatisk i digna
- Brugeren bør være logget ind
- Brugerprofilen bør vise dine identitetsudbyderoplysninger
- Du bør se digna-dashboardet

#### Trin 6: Test login med adgangskode (hvis aktiveret)

Hvis `usePassword = true`:

1. Log ud af digna
2. På login-siden indtast et brugernavn og en adgangskode
3. Du bør kunne logge ind med adgangskodelegitimationsoplysninger

---

## Fejlfinding {: #troubleshooting }

### Loginknapper vises ikke

**Symptomer:**
- OIDC-loginknapper vises ikke på login-siden
- Ser kun adgangskodefelter (hvis usePassword = true)

**Årsager og løsninger:**
1. Tjek at `dashboard_config.toml` er i `dashboard/`-biblioteket
2. Verificer at `[[login.oidc]]`-sektionerne er til stede med korrekt syntaks
3. Genstart dashboard-tjenesten
4. Ryd browsercache (Ctrl+Shift+Delete eller Cmd+Shift+Delete)
5. Tjek browserkonsollen (F12 → Console-fanen) for fejl

---

### Fejl ved mismatch af Redirect URI

**Symptomer:**
- Efter klik på SSO-knappen, fejl om "redirect_uri mismatch"
- "The redirect URI is not registered" fejl

**Årsager og løsninger:**
1. Verificer `DIGNA_OIDC_REDIRECT_URI` i `config.toml` er korrekt
2. Verificer at redirect URI er registreret i identitetsudbyderens indstillinger
3. Sørg for, at begge bruger identiske URL'er (inkl. protokol, domæne, sti)
4. Tjek for stavefejl i redirect URI
5. Hvis du bruger HTTPS, sørg for at certifikatet er gyldigt

---

### Ugyldige klientlegitimationsoplysninger

**Symptomer:**
- "Invalid client ID or secret" fejl
- Godkendelse fejler med legitimationsfejl

**Årsager og løsninger:**
1. Verificer `DIGNA_OIDC_CLIENT_ID` og `DIGNA_OIDC_CLIENT_SECRET` er korrekte
2. Sørg for ingen ekstra mellemrum eller specialtegn
3. Tjek at legitimationsoplysninger ikke er udløbet eller tilbagekaldt
4. Genstart backend-tjenesten efter opdatering af config
5. Tjek identitetsudbyderens konsol for at bekræfte at legitimationsoplysningerne er aktive

---

### Login hænger eller timeouter

**Symptomer:**
- Klik på SSO-knappen sker intet
- Timeout efter flere sekunder
- Browser viser "Failed to connect" eller lignende

**Årsager og løsninger:**
1. Verificer at digna-backend kører: `digna repo check`
2. Tjek netværksforbindelse til identitetsudbyderen
3. Verificer `DIGNA_OIDC_CONFIGURATION_URL` er tilgængelig
4. Tjek firewall-regler tillader udgående HTTPS-forbindelser
5. Verificer backend og dashboard kan nå hinanden

---

### Brugere oprettes ikke automatisk

**Symptomer:**
- SSO-login lykkes, men bruger oprettes ikke i digna
- Får tilladelsesfejl efter SSO-login

**Årsager og løsninger:**
1. Verificer OIDC-konfigurationen er korrekt
2. Tjek at brugerrettigheder er sat op
3. Gennemgå digna-logs for fejlmeddelelser
4. Genstart backend-tjenesten
5. Kontakt support@digna.ai hvis problemet fortsætter

---

## Understøttede udbydere {: #supported-providers }

### Testede og understøttede

Følgende OIDC-udbydere er testet og vides at fungere:

| Udbyder | Konfigurations-URL | Opsætningsguide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Konfigurer SSO med AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Konfigurer SSO med Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Konfigurer SSO med Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Konfigurer SSO med Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Konfigurer SSO med Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Konfigurer SSO med Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Konfigurer SSO med OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Konfigurer SSO med PingOne](pingone_sso_guide.md) |

### Andre OIDC-udbydere

Enhver udbyder, der understøtter OpenID Connect, kan integreres. Påkrævet information:

- Client ID
- Client secret
- OpenID-konfigurations-URL (typisk ved `/.well-known/openid-configuration`)
- Understøttede scopes (typisk `openid profile email`)

Kontakt support@digna.ai hvis du har brug for hjælp til at integrere en specifik udbyder.

---

## Bedste praksis

**GØR:**
- Brug HTTPS i produktion (ikke HTTP)
- Opbevar client secrets sikkert (brug miljøvariabler hvis muligt)
- Rotér secrets periodisk
- Test i et ikke-produktionsmiljø først
- Dokumentér hvilke udbydere der er konfigureret
- Overvåg login-logs for usædvanlig aktivitet
- Hold identitetsudbyderkonfigurationen i sync med digna-konfigurationen

**GØR IKKE:**
- Gem client secrets i versionsstyring
- Brug HTTP redirect URIs i produktion
- Konfigurer flere udbydere med samme key
- Lad standard/test-legitimationsoplysninger blive i produktion
- Eksponér konfigurationsfiler, der indeholder secrets
- Bland udviklings- og produktionslegitimationsoplysninger

---

## Support

Brug for hjælp til SSO-konfiguration?

- **Email:** support@digna.ai
- **Dokumentation:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Sidst opdateret:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**