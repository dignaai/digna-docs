---
title: Single Sign-On (SSO) Integrasjonsguide | digna Dokumentasjon
description: Trinnvis veiledning for å konfigurere Single Sign-On (SSO) for digna ved bruk av OpenID Connect (OIDC). Dekker dashboard- og backend-konfigurasjon, testing, feilsøking og støttede identitetsleverandører inkludert Microsoft Entra ID, Google Workspace og Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integrasjon
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integrasjon
  - enterprise authentication
lang: no
robots: index, follow
og_title: digna Single Sign-On (SSO) Integrasjonsguide
og_description: Konfigurer Single Sign-On for digna ved bruk av OpenID Connect. Trinnvis oppsett for Microsoft Entra ID, Google Workspace, Okta og andre OIDC-kompatible identitetsleverandører.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integrasjonsguide

---

## Innholdsfortegnelse

1. [Introduksjon og oversikt](#introduction-and-overview)
2. [Konfigurasjonstrinn](#configuration-steps)
3. [Dashboard-konfigurasjon](#dashboard-configuration)
4. [Backend-konfigurasjon](#backend-configuration)
5. [Testing av innlogging](#testing-login)
6. [Feilsøking](#troubleshooting)
7. [Støttede leverandører](#supported-providers)

---

## Introduksjon og oversikt {: #introduction-and-overview }

Denne veiledningen gir trinnvise instruksjoner for å integrere Single Sign-On (SSO) med digna-plattformen ved bruk av **OpenID Connect (OIDC)**.

### Hva er SSO?

Single Sign-On lar brukere logge seg på digna sikkert ved å bruke sine bedriftslegitimasjoner gjennom eksterne identitetsleverandører. Brukere kan autentisere seg med sine bedriftskontoer i stedet for å håndtere separate digna-passord.

### Hvordan det fungerer

SSO i digna er implementert ved hjelp av OIDC-protokollen. Flere identitetsleverandører kan konfigureres parallelt ved å justere to viktige konfigurasjonsfiler:

- **`dashboard_config.toml`** — Kontrollerer frontend-innloggingsgrensesnittet
- **`config.toml`** — Konfigurerer backend OIDC-tilkoblinger

### Støttede leverandører {: #supported-providers-overview }

Eksemplene i denne veiledningen bruker **Microsoft** og **Google**, men **enhver OIDC-kompatibel leverandør** kan integreres ved å følge samme struktur.

Vanlige OIDC-leverandører inkluderer:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Andre OIDC-kompatible identitetsleverandører

---

## Konfigurasjonstrinn {: #configuration-steps }

SSO-konfigurasjon krever oppdateringer i to filer. Denne delen forklarer hvordan hver av dem konfigureres.

### Oversikt over konfigurasjonsfiler

| Fil | Plassering | Formål |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend-innloggingsgrensesnitt |
| **config.toml** | `/config.toml` | Backend OIDC-tilkoblinger |

Begge filene må være konfigurert for at SSO skal fungere riktig.

---

## Dashboard-konfigurasjon {: #dashboard-configuration }

### Filplassering

```
dashboard/dashboard_config.toml
```

### Trinn 1: Legg til OIDC-leverandører

Legg inn oppføringer under `[[login.oidc]]`-arrayen for hver identitetsleverandør du ønsker å støtte.

**Eksempel med Microsoft og Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Trinn 2: Konfigurer innloggingsalternativer

Angi om passordbasert innlogging skal tillates:

```toml
[login]
usePassword = true
```

### Konfigurasjonsparametere

#### `[[login.oidc]]` Seksjon

| Parameter | Type | Påkrevd | Beskrivelse |
|---|---|---|---|
| `key` | string | Ja | Unik identifikator for OIDC-tilkoblingen (må samsvare med key i config.toml) |
| `label` | string | Ja | Tekst som vises på innloggingsknappen (f.eks. "Login with Microsoft") |

#### `[login]` Seksjon

| Parameter | Type | Standard | Beskrivelse |
|---|---|---|---|
| `usePassword` | boolean | false | Tillat passordbasert innlogging i tillegg til SSO |

### Forstå usePassword

**Hvis `usePassword = true`:**
- Innloggingsskjermen viser SSO-knapper (f.eks. "Login with Microsoft")
- Innloggingsskjermen viser også brukernavn- og passordfelt
- Brukere kan autentisere seg med enten metode
- Tillater hybride oppsett der noen brukere bruker SSO og andre bruker passord

**Hvis `usePassword = false` (eller utelatt):**
- Innloggingsskjermen viser kun SSO-knapper
- Ingen brukernavn-/passordfelt
- Kun OIDC-autentisering er tilgjengelig

> **💡 Tips**
>
> Passordbasert innlogging er kun tilgjengelig for brukere som ble opprettet med passord ved hjelp av `digna user add`-kommandoen eller via dashboardet.

### Fullstendig eksempel

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

## Backend-konfigurasjon {: #backend-configuration }

### Filplassering

```
/config.toml
```

(Roten av digna-installasjonskatalogen)

### Trinn 1: Legg til OIDC-leverandørseksjoner

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
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client ID fra identitetsleverandøren | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client secret fra identitetsleverandøren | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL etter autentisering | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-konfigurasjonsendepunkt | `https://login.microsoftonline.com/...` |

> **⚠️ Viktig**
>
> Erstatt plassholderverdier (`<client_id>`, `<client_secret>`, `<tenant_id>`) med faktiske legitimasjoner fra identitetsleverandørens developer-portal.

### Redirect URI

Redirect URI må være identisk i konfigurasjonen hos identitetsleverandøren:

```
http://localhost:5173/oidc/callback
```

Hvis digna er hostet på et annet domene, oppdater deretter:
- Lokal: `http://localhost:5173/oidc/callback`
- Produksjon: `https://digna.yourdomain.com/oidc/callback`

### Fullstendig eksempel

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

Etter at konfigurasjonen er fullført, verifiser at SSO fungerer som forventet.

### Sjekkliste før testing

Før testing, sørg for:

- [ ] `dashboard_config.toml` er oppdatert med OIDC-leverandører
- [ ] `config.toml` er oppdatert med OIDC-legitimasjon
- [ ] Begge filene er lagret
- [ ] Legitimasjonene er korrekte (client ID, client secret)
- [ ] Redirect URI samsvarer med din distribusjons-URL
- [ ] Identitetsleverandørens applikasjon er konfigurert med redirect URI

### Testtrinn

#### Trinn 1: Start tjenester på nytt

Start digna-backend og webserver på nytt for å bruke endringene.

**Hvis du kjører som Windows-tjeneste:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Hvis du kjører manuelt:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Hvis du bruker IIS eller Tomcat:**
Start webserver-tjenesten på nytt.

#### Trinn 2: Åpne dashboard

Åpne digna-dashboardet i nettleseren:

```
http://localhost:5173
```

(eller din konfigurerte dashboard-URL)

#### Trinn 3: Verifiser innloggingsknapper

Sjekk at innloggingsknapper vises for hver konfigurert leverandør:

- ✅ Skal vise "Login with Microsoft"-knapp
- ✅ Skal vise "Login with Google"-knapp
- ✅ (Hvis usePassword = true) Skal vise brukernavn-/passordfelt

Hvis knappene ikke vises:
- Sjekk at `dashboard_config.toml` ble lagret
- Sjekk at dashboard-tjenesten ble startet på nytt
- Sjekk nettleserkonsollen (F12) for feil

#### Trinn 4: Test SSO-innlogging

Klikk en av SSO-knappene (f.eks. "Login with Microsoft"):

1. Du skal bli omdirigert til identitetsleverandørens innloggingsside
2. Logg inn med dine bedriftslegitimasjoner
3. Du skal bli omdirigert tilbake til digna
4. Du skal være innlogget i digna

#### Trinn 5: Verifiser brukerskapning

Etter vellykket SSO-innlogging:

- ✅ Bruker skal automatisk opprettes i digna
- ✅ Bruker skal være innlogget
- ✅ Brukerprofil skal vise dine identitetsleverandøropplysninger
- ✅ Du skal se digna-dashboardet

#### Trinn 6: Test passordinnlogging (hvis aktivert)

Hvis `usePassword = true`:

1. Logg ut av digna
2. På innloggingssiden, skriv inn brukernavn og passord
3. Du skal kunne logge inn med passordlegitimasjon

---

## Feilsøking {: #troubleshooting }

### Innloggingsknapper vises ikke

**Symptomer:**
- OIDC-innloggingsknapper ikke synlige på innloggingssiden
- Ser kun passordfelt (hvis usePassword = true)

**Årsaker & løsninger:**
1. Sjekk at `dashboard_config.toml` ligger i `dashboard/`-katalogen
2. Verifiser at `[[login.oidc]]`-seksjonene er til stede med korrekt syntaks
3. Start dashboard-tjenesten på nytt
4. Tøm nettleserens cache (Ctrl+Shift+Delete eller Cmd+Shift+Delete)
5. Sjekk nettleserkonsollen (F12 → Console-fanen) for feil

---

### Redirect URI mismatch-feil

**Symptomer:**
- Etter å ha klikket SSO-knapp, feil om "redirect_uri mismatch"
- "The redirect URI is not registered" feil

**Årsaker & løsninger:**
1. Verifiser `DIGNA_OIDC_REDIRECT_URI` i `config.toml` er korrekt
2. Verifiser at redirect URI er registrert i identitetsleverandørens innstillinger
3. Sørg for at begge bruker identiske URLer (inkludert protokoll, domene, path)
4. Sjekk for skrivefeil i redirect URI
5. Hvis du bruker HTTPS, sørg for at sertifikatet er gyldig

---

### Ugyldig klientlegitimasjon-feil

**Symptomer:**
- "Invalid client ID or secret" feil
- Autentisering feiler med legitimasjonsfeil

**Årsaker & løsninger:**
1. Verifiser `DIGNA_OIDC_CLIENT_ID` og `DIGNA_OIDC_CLIENT_SECRET` er korrekte
2. Sørg for at det ikke er ekstra mellomrom eller uønskede tegn
3. Sjekk at legitimasjonen ikke har gått ut eller blitt tilbakekalt
4. Start backend-tjenesten på nytt etter at konfig er oppdatert
5. Sjekk identitetsleverandør-konsollen for å bekrefte at legitimasjonen er aktiv

---

### Innlogging henger eller timeouter

**Symptomer:**
- Å klikke SSO-knappen gjør ingenting
- Timeout etter noen sekunder
- Nettleseren viser "Failed to connect" eller lignende

**Årsaker & løsninger:**
1. Verifiser at digna-backend kjører: `digna repo check`
2. Sjekk nettverkstilkobling til identitetsleverandøren
3. Verifiser at `DIGNA_OIDC_CONFIGURATION_URL` er tilgjengelig
4. Sjekk at brannmurregler tillater utgående HTTPS-tilkoblinger
5. Verifiser at backend og dashboard kan nå hverandre

---

### Brukere opprettes ikke automatisk

**Symptomer:**
- SSO-innlogging lykkes men bruker opprettes ikke i digna
- Får tillatelsesfeil etter SSO-innlogging

**Årsaker & løsninger:**
1. Verifiser at OIDC-konfigurasjonen er korrekt
2. Sjekk at brukerrettigheter er satt opp
3. Gå gjennom digna-loggene for feilmeldinger
4. Start backend-tjenesten på nytt
5. Kontakt support@digna.ai hvis problemet vedvarer

---

## Støttede leverandører {: #supported-providers }

### Testet og støttet

Følgende OIDC-leverandører er testet og er kjent for å fungere:

| Leverandør | Konfigurasjons-URL | Oppsettsveiledning |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Andre OIDC-leverandører

Enhver leverandør som støtter OpenID Connect kan integreres. Krevd informasjon:

- Client ID
- Client secret
- OpenID-konfigurasjons-URL (vanligvis på `/.well-known/openid-configuration`)
- Støttede scopes (typisk `openid profile email`)

Kontakt support@digna.ai hvis du trenger hjelp med å integrere en spesifikk leverandør.

---

## Beste praksis

✅ **GJØR:**
- Bruk HTTPS i produksjon (ikke HTTP)
- Lagre client secrets sikkert (bruk miljøvariabler hvis mulig)
- Roter secrets jevnlig
- Test i et ikke-produksjonsmiljø først
- Dokumenter hvilke leverandører som er konfigurert
- Overvåk innloggingslogger for uvanlig aktivitet
- Hold identitetsleverandørkonfigurasjonen synkronisert med digna-konfig

❌ **IKKE:**
- Lagre client secrets i versjonskontroll
- Bruk HTTP redirect-URIer i produksjon
- Konfigurer flere leverandører med samme key
- La standard-/test-legitimasjon bli værende i produksjon
- Eksponer konfigurasjonsfiler som inneholder secrets
- Bland utviklings- og produksjonslegitimasjon

---

## Support

Trenger du hjelp med SSO-konfigurasjon?

- 📧 **E-post:** support@digna.ai
- 📚 **Dokumentasjon:** https://docs.digna.ai
- 🌐 **Nettsted:** https://www.digna.ai

---

**Sist oppdatert:** 30. august 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**