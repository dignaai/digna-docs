---
title: Auth0 SSO – Single Sign-On-integrasjon | digna-dokumentasjon
description: Konfigurer Single Sign-On for digna med Auth0 ved hjelp av OpenID Connect — oppsett av Regular Web Application, tillatte callback-URL-er, klientlegitimasjon, tenant-domene og tilhørende digna-konfigurasjon.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regular web application, callback-url-er, openid connect, bedriftsautentisering
---

# Sett opp SSO med Auth0

Auth0 er OIDC-kompatibel og eksponerer ett discovery-endepunkt per tenant. Det viktigste å få riktig er tenant-domenet, som inngår i discovery-URL-en og endres hvis du aktiverer et tilpasset domene.

Denne veiledningen dekker **Auth0-siden**: opprette applikasjonen og samle verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Single Sign-On-oversikt](overview.md).

---

## Før du begynner

| Krav | Merknader |
|---|---|
| **Auth0-rolle** | Admin på tenanten |
| **Tenant-domene** | f.eks. `yourcompany.eu.auth0.com` — regionsdelen har betydning |
| **digna redirect URI** | URL-en brukere returnerer til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Opprett applikasjonen

1. Logg på [Auth0 Dashboard](https://manage.auth0.com)
2. Gå til **Applications → Applications**
3. Klikk **Create Application**
4. Gi den navnet `digna` og velg **Regular Web Applications**
5. Klikk **Create**

!!! warning "Velg Regular Web Applications"

    *Single Page Application* og *Native* oppretter public clients uten secret. digna utfører kodeutvekslingen fra sin backend og trenger en konfidensiell klient, så **Regular Web Applications** er riktig type. I motsetning til enkelte leverandører lar Auth0 deg endre typen senere under **Settings → Application Type**.

---

## Trinn 2: Legg til callback-URL-en

På applikasjonens **Settings**-fane:

1. Finn **Allowed Callback URLs**
2. Legg inn din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Sett eventuelt **Allowed Logout URLs** til dashbord-URL-en din
4. Rull helt ned og klikk **Save Changes**

!!! note "Kommaseparert, ikke linjeskiftseparert"

    Auth0 godtar flere callback-URL-er i dette feltet, separert med komma. En liste som bare er separert med linjeskift, leses som én ugyldig URL og samsvarer i stillhet ikke med noe.

---

## Trinn 3: Hent legitimasjonen

Fortsatt på **Settings**, i panelet **Basic Information**:

- **Domain** → brukes i discovery-URL-en
- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klikk for å vise)

---

## Trinn 4: Bekreft grant-typen

1. Gå til **Settings → Advanced Settings → Grant Types**
2. Bekreft at **Authorization Code** er avkrysset

Den er aktivert som standard for Regular Web Applications. Hvis avkrysningen er fjernet, feiler innloggingen i digna med `unauthorized_client`.

---

## Trinn 5: Bygg discovery-URL-en

Sett inn **Domain** fra trinn 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

For eksempel:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Tilpassede domener endrer utstederen"

    Hvis tenanten din bruker et tilpasset domene som `login.yourcompany.com`, bruker du det domenet i discovery-URL-en. Blander du de to — det kanoniske domenet i discovery-URL-en og det tilpassede i nettleseren — oppstår et avvik i utsteder (issuer mismatch), og tokenet avvises etter en ellers vellykket innlogging.

---

## Trinn 6: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

`key` i begge filer må samsvare — `auth0` her.

---

## Trinn 7: Test

Start backend og webserver på nytt, og åpne dashbordet. Se [Test av innlogging](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking for Auth0

### Callback-URL samsvarer ikke

Auth0s feilside oppgir URL-en den mottok. Legg den til i **Allowed Callback URLs**, og kontroller at oppføringene er kommaseparert.

### unauthorized_client

**Authorization Code** er ikke aktivert under **Advanced Settings → Grant Types**, eller applikasjonstypen er ikke Regular Web Applications.

### Tilgang nektet etter en vellykket innlogging

En Rule, Action eller Post-Login-trigger i tenanten avviser brukeren. Sjekk **Actions → Flows → Login** og tenant-loggene under **Monitoring → Logs**, som viser den nøyaktige årsaken.

### Avvik i utsteder (issuer mismatch)

Discovery-URL-en og domenet nettleseren ble sendt til er forskjellige — vanligvis det kanoniske tenant-domenet kontra et tilpasset domene. Bruk ett av dem konsekvent.

---

## Se også

- [Single Sign-On-oversikt](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
