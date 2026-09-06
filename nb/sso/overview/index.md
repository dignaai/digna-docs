# Oversikt over Single Sign-On

---

## Innholdsfortegnelse

1. [Introduksjon og oversikt](#introduction-and-overview)
2. [Leverandørguider](#provider-guides)
3. [Konfigurasjonssteg](#configuration-steps)
4. [Dashbordkonfigurasjon](#dashboard-configuration)
5. [Backend-konfigurasjon](#backend-configuration)
6. [Testing av innlogging](#testing-login)
7. [Feilsøking](#troubleshooting)
8. [Støttede leverandører](#supported-providers)

---

## Introduksjon og oversikt {: #introduction-and-overview }

Denne guiden gir trinnvise instruksjoner for å integrere Single Sign-On (SSO) med digna-plattformen ved bruk av **OpenID Connect (OIDC)**.

### Hva er SSO?

Single Sign-On lar brukere logge seg sikkert inn i digna ved hjelp av sine bedriftslegitimasjoner gjennom eksterne identity providers. Brukere kan autentisere seg med sine bedriftskontoer i stedet for å administrere separate digna-passord.

### Hvordan det fungerer

SSO i digna er implementert ved bruk av OIDC-protokollen. Flere identity providers kan konfigureres parallelt ved å justere to sentrale konfigurasjonsfiler:

- **`dashboard_config.toml`** — Kontrollerer frontend-innloggingsgrensesnittet
- **`config.toml`** — Konfigurerer backend OIDC-tilkoblinger

### Støttede leverandører {: #supported-providers-overview }

Eksemplene i denne guiden bruker **Microsoft** og **Google**, men **enhver OIDC-kompatibel leverandør** kan integreres ved å følge samme struktur.

---

## Leverandørguider {: #provider-guides }

Hver leverandør trenger de samme fire verdiene — en client ID, en client secret, en redirect URI og en discovery URL — men hver av dem legger dem forskjellige steder i administrasjonskonsollen, og flere har et leverandørspesifikt steg som de andre ikke har. Guidene nedenfor dekker den halvdelen av arbeidet; denne siden dekker digna-delen, som er identisk for alle.

| Leverandør | Guide | Viktig å vite |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Selvhostet; den eneste leverandøren her hvor du kontrollerer token-tjenesten |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL er per-tenant, og egendefinerte domener endrer den |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Samtykkeskjermen må publiseres før ikke-testbrukere kan logge inn |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Selvhostet; discovery URL er per-realm |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID vises i discovery URL; secrets utløper |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Valg av authorization server endrer discovery URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | OIDC app-typen må velges ved opprettelse og kan ikke endres |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Environment ID vises i discovery URL |

Enhver annen OIDC-kompatibel leverandør fungerer på samme måte — se [Other OIDC Providers](#supported-providers).

---

## Konfigurasjonssteg {: #configuration-steps }

SSO-konfigurasjon krever oppdateringer i to filer. Denne seksjonen forklarer hvordan du konfigurerer hver av dem.

### Oversikt over konfigurasjonsfiler

| Fil | Plassering | Formål |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend-innloggingsgrensesnitt |
| **config.toml** | `/config.toml` | Backend OIDC-tilkoblinger |

Begge filer må konfigureres for at SSO skal fungere riktig.

---

## Dashbordkonfigurasjon {: #dashboard-configuration }

### Filplassering

```
dashboard/dashboard_config.toml
```

### Steg 1: Legg til OIDC-leverandører

Legg til oppføringer under `[[login.oidc]]`-arrayen for hver identity provider du vil støtte.

**Eksempel med Microsoft og Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Logg inn med Microsoft"

[[login.oidc]]
key = "google"
label = "Logg inn med Google"
```

### Steg 2: Konfigurer innloggingsalternativer

Angi om passordbasert innlogging skal være tillatt:

```toml
[login]
usePassword = true
```

### Konfigurasjonsparametere

#### `[[login.oidc]]`-seksjonen

| Parameter | Type | Påkrevd | Beskrivelse |
|---|---|---|---|
| `key` | string | Ja | Unik identifikator for OIDC-tilkoblingen (må samsvare med key i config.toml) |
| `label` | string | Ja | Tekst som vises på innloggingsknappen (f.eks. "Logg inn med Microsoft") |

#### `[login]`-seksjonen

| Parameter | Type | Standard | Beskrivelse |
|---|---|---|---|
| `usePassword` | boolean | false | Tillat passordbasert innlogging i tillegg til SSO |

### Forstå usePassword

**Hvis `usePassword = true`:**
- Innloggingssiden viser SSO-knapper (f.eks. "Logg inn med Microsoft")
- Innloggingssiden viser også brukernavn- og passordfelt
- Brukere kan autentisere seg med begge metodene
- Tillater hybride oppsett hvor noen brukere bruker SSO og andre passord

**Hvis `usePassword = false` (eller utelatt):**
- Innloggingssiden viser kun SSO-knapper
- Ingen brukernavn-/passordfelt
- Kun OIDC-autentisering er tilgjengelig

!!! tip "Tips"

    Passordbasert innlogging er kun tilgjengelig for brukere som ble opprettet med passord ved hjelp av `digna user add`-kommandoen eller via dashbordet.

### Komplett eksempel

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Logg inn med Microsoft"

[[login.oidc]]
key = "google"
label = "Logg inn med Google"

[[login.oidc]]
key = "okta"
label = "Logg inn med Okta"
```

---

## Backend-konfigurasjon {: #backend-configuration }

### Filplassering

```
/config.toml
```

(Rotmappen for digna-installasjonen)

### Steg 1: Legg til OIDC-leverandørseksjoner

Hver leverandør må ha en dedikert `[oidc.<key>]`-seksjon. Key må samsvare med `key` definert i `dashboard_config.toml`.

### Microsoft-konfigurasjon

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google-konfigurasjon

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurasjonsparametere

| Parameter | Type | Påkrevd | Beskrivelse | Eksempel |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client ID fra identity provider | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client secret fra identity provider | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL etter autentisering | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-konfigurasjonsendepunkt | `https://login.microsoftonline.com/...` |

!!! warning "Viktig"

    Erstatt plassholderverdiene (`<client_id>`, `<client_secret>`, `<tenant_id>`) med faktiske legitimasjoner fra identity providerens utviklerportal.

### Redirect URI

Redirect URI må være den samme i identity provider-konfigurasjonen:

```
http://localhost:5173/oidc/callback
```

Hvis digna er hostet på et annet domene, oppdater tilsvarende:
- Lokalt: `http://localhost:5173/oidc/callback`
- Produksjon: `https://digna.yourdomain.com/oidc/callback`

### Komplett eksempel

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

## Testing av innlogging {: #testing-login }

Etter å ha fullført konfigurasjonen, verifiser at SSO fungerer korrekt.

### Sjekkliste før testing

Før testing, sørg for at:

- [ ] `dashboard_config.toml` er oppdatert med OIDC-leverandører
- [ ] `config.toml` er oppdatert med OIDC-legitimasjonene
- [ ] Begge filer er lagret
- [ ] Legitimasjonene er korrekte (client ID, client secret)
- [ ] Redirect URI samsvarer med din deployerte URL
- [ ] Identity provider-applikasjonen er konfigurert med redirect URI

### Teststeg

#### Steg 1: Start tjenester på nytt

Start digna backend og webserver på nytt for å bruke endringene.

**Hvis det kjører som en tjeneste på Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Hvis det kjører som en tjeneste på Linux eller macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Hvis det kjøres manuelt:**
```bash
digna serve --address localhost --port 8082
```

**Start også webserveren på nytt** — IIS eller Tomcat på Windows, nginx eller Apache på Linux og macOS.

#### Steg 2: Åpne dashbordet

Åpne digna-dashbordet i nettleseren:

```
http://localhost:5173
```

(eller din konfigurerte dashbord-URL)

#### Steg 3: Verifiser innloggingsknapper

Sjekk at innloggingsknapper vises for hver konfigurert leverandør:

- Skal se knappen "Logg inn med Microsoft"
- Skal se knappen "Logg inn med Google"
- (Hvis usePassword = true) Skal se brukernavn-/passordfelt

Hvis knappene ikke vises:
- Sjekk at `dashboard_config.toml` ble lagret
- Sjekk at dashbordtjenesten ble startet på nytt
- Sjekk nettleserkonsollen (F12) for feil

#### Steg 4: Test SSO-innlogging

Klikk en av SSO-knappene (f.eks. "Logg inn med Microsoft"):

1. Du skal bli omdirigert til identity providerens innloggingsside
2. Logg inn med dine bedriftslegitimasjoner
3. Du skal bli omdirigert tilbake til digna
4. Du skal være innlogget i digna

#### Steg 5: Verifiser brukeropprettelse

Etter vellykket SSO-innlogging:

- Bruker skal automatisk opprettes i digna
- Bruker skal være innlogget
- Brukerprofilen skal vise dine identity provider-opplysninger
- Du skal se digna-dashbordet

#### Steg 6: Test passordinnlogging (hvis aktivert)

Hvis `usePassword = true`:

1. Logg ut av digna
2. På innloggingssiden, skriv inn brukernavn og passord
3. Du skal kunne logge inn med passordlegitimasjonene

---

## Feilsøking {: #troubleshooting }

### Innloggingsknapper vises ikke

**Symptomer:**
- OIDC-innloggingsknapper ikke synlige på innloggingssiden
- Ser kun passordfelt (hvis usePassword = true)

**Årsaker og løsninger:**
1. Sjekk at `dashboard_config.toml` ligger i `dashboard/`-katalogen
2. Verifiser at `[[login.oidc]]`-seksjonene er til stede med korrekt syntaks
3. Start dashbordtjenesten på nytt
4. Tøm nettleserens cache (Ctrl+Shift+Delete eller Cmd+Shift+Delete)
5. Sjekk nettleserkonsollen (F12 → Console-fanen) for feil

---

### Redirect URI mismatch-feil

**Symptomer:**
- Etter å ha klikket SSO-knappen, feil om "redirect_uri mismatch"
- "The redirect URI is not registered" feil

**Årsaker og løsninger:**
1. Verifiser at `DIGNA_OIDC_REDIRECT_URI` i `config.toml` er korrekt
2. Verifiser at redirect URI er registrert i identity provider-innstillingene
3. Sørg for at begge bruker identiske URLer (inkludert protokoll, domene, sti)
4. Sjekk for skrivefeil i redirect URI
5. Hvis du bruker HTTPS, forsikre deg om at sertifikatet er gyldig

---

### Ugyldige klientlegitimasjoner-feil

**Symptomer:**
- "Invalid client ID or secret" feil
- Autentisering feiler med legitimasjonsfeil

**Årsaker og løsninger:**
1. Verifiser at `DIGNA_OIDC_CLIENT_ID` og `DIGNA_OIDC_CLIENT_SECRET` er korrekte
2. Sørg for at det ikke er ekstra mellomrom eller spesialtegn
3. Sjekk at legitimasjonene ikke har utløpt eller blitt tilbakekalt
4. Start backend-tjenesten på nytt etter å ha oppdatert konfig
5. Sjekk identity provider-konsollen for å bekrefte at legitimasjonene er aktive

---

### Innlogging henger eller går ut på tid

**Symptomer:**
- Klikk på SSO-knappen gjør ingenting
- Timeout etter noen sekunder
- Nettleser viser "Failed to connect" eller lignende

**Årsaker og løsninger:**
1. Verifiser at digna-backend kjører: `digna repo check`
2. Sjekk nettverksforbindelsen til identity provider
3. Verifiser at `DIGNA_OIDC_CONFIGURATION_URL` er tilgjengelig
4. Sjekk at brannmurregler tillater utgående HTTPS-tilkoblinger
5. Verifiser at backend og dashbord kan nå hverandre

---

### Brukere blir ikke opprettet automatisk

**Symptomer:**
- SSO-innlogging lykkes, men bruker blir ikke opprettet i digna
- Får tillatelsesfeil etter SSO-innlogging

**Årsaker og løsninger:**
1. Verifiser at OIDC-konfigurasjonen er korrekt
2. Sjekk at brukerrettigheter er konfigurert riktig
3. Gå gjennom digna-loggene for feilmeldinger
4. Start backend-tjenesten på nytt
5. Kontakt support@digna.ai hvis problemet vedvarer

---

## Støttede leverandører {: #supported-providers }

### Testet og støttet

Følgende OIDC-leverandører er testet og kjent for å fungere:

| Leverandør | Konfigurasjons-URL | Oppsettsguide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Andre OIDC-leverandører

Enhver leverandør som støtter OpenID Connect kan integreres. Påkrevd informasjon:

- Client ID
- Client secret
- OpenID konfigurasjons-URL (vanligvis på `/.well-known/openid-configuration`)
- Støttede scopes (typisk `openid profile email`)

Kontakt support@digna.ai hvis du trenger hjelp med å integrere en spesifikk leverandør.

---

## Beste praksis

**GJØR:**
- Bruk HTTPS i produksjon (ikke HTTP)
- Lagre client secrets sikkert (bruk miljøvariabler om mulig)
- Roter secrets periodisk
- Test i et ikke-produksjonsmiljø først
- Dokumenter hvilke leverandører som er konfigurert
- Overvåk innloggingslogger for uvanlig aktivitet
- Hold identity provider-konfigurasjon i sync med digna-konfigurasjonen

**IKKE GJØR:**
- Lagre client secrets i versjonskontroll
- Bruk HTTP redirect URIs i produksjon
- Konfigurer flere leverandører med samme key
- La standard/test-legitimasjoner være i produksjon
- Eksponer konfigurasjonsfiler som inneholder secrets
- Bland utviklings- og produksjonslegitimasjoner

---

## Support

Trenger du hjelp med SSO-konfigurasjon?

- **E-post:** support@digna.ai
- **Dokumentasjon:** https://docs.digna.ai
- **Nettside:** https://www.digna.ai

---

**Sist oppdatert:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**