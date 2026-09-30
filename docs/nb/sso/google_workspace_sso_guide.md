---
title: Google Workspace SSO – Single Sign-On-integrasjon | digna-dokumentasjon
description: Konfigurer Single Sign-On for digna med Google Workspace ved hjelp av OpenID Connect — OAuth-samtykkeskjerm, OAuth-klient-ID, autoriserte omdirigerings-URIer og tilhørende digna-konfigurasjon.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth-samtykkeskjerm, openid connect, bedriftsautentisering
---

# Sett opp SSO med Google Workspace

Googles identitetsplattform er OIDC-kompatibel og bruker én felles, velkjent discovery-URL for alle kunder, så de eneste organisasjonsspesifikke verdiene er klient-ID og secret.

Denne veiledningen dekker **Google-siden**: opprette OAuth-klienten og samle verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Single Sign-On-oversikt](overview.md).

---

## Før du begynner

| Krav | Merknader |
|---|---|
| **Google Cloud-prosjekt** | Et hvilket som helst prosjekt i samme organisasjon som Workspace-domenet ditt |
| **Rolle** | Editor eller Owner på prosjektet |
| **digna redirect URI** | URL-en brukere returnerer til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Konfigurer OAuth-samtykkeskjermen

Google utsteder ikke legitimasjon før samtykkeskjermen finnes.

1. Åpne [Google Cloud Console](https://console.cloud.google.com) og velg prosjektet ditt
2. Gå til **APIs & Services → OAuth consent screen**
3. Velg brukertype:
   - **Internal** — bare kontoer i Workspace-domenet ditt kan logge inn. Anbefalt.
   - **External** — enhver Google-konto kan forsøke å logge inn.
4. Fyll ut appnavn, e-postadresse for brukerstøtte og e-postadresse for utviklerkontakt
5. I **Scopes**-steget legger du til `openid`, `.../auth/userinfo.email` og `.../auth/userinfo.profile`
6. Lagre

!!! warning "External-apper må publiseres"

    En **External**-samtykkeskjerm starter i statusen *Testing*, der bare kontoer som er eksplisitt lagt til i listen over testbrukere, kan fullføre en innlogging. Alle andre ser "digna has not completed the Google verification process". Bytt enten appen til **In production** under **Publishing status**, eller bruk **Internal** — som ikke har en slik begrensning og er riktig valg for en ren Workspace-installasjon.

---

## Trinn 2: Opprett OAuth-klienten

1. Gå til **APIs & Services → Credentials**
2. Klikk **Create Credentials → OAuth client ID**
3. Sett **Application type** til **Web application**
4. Gi den et navn, f.eks. `digna`
5. Under **Authorized redirect URIs** klikker du **Add URI** og legger inn:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klikk **Create**

!!! note "Authorized JavaScript origins er ikke nødvendig"

    digna utveksler autorisasjonskoden fra backend, ikke fra nettleseren, så feltet **Authorized JavaScript origins** kan stå tomt. Bare omdirigerings-URI-en har betydning.

---

## Trinn 3: Hent legitimasjonen

Dialogboksen som vises etter opprettelsen, viser:

- **Client ID** — slutter på `.apps.googleusercontent.com` → blir `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → blir `DIGNA_OIDC_CLIENT_SECRET`

Begge kan hentes senere fra legitimasjonens detaljside, i motsetning til hos de fleste andre leverandører.

---

## Trinn 4: Discovery-URL-en

Google bruker én discovery-URL for alle kunder — det er ingenting å erstatte:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Trinn 5: Konfigurer digna

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
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

`key` i begge filer må samsvare — `google` her.

---

## Trinn 6: Test

Start backend og webserver på nytt, og åpne dashbordet. Se [Test av innlogging](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking for Google Workspace

### Error 400: redirect_uri_mismatch

URI-en i `DIGNA_OIDC_REDIRECT_URI` står ikke i listen **Authorized redirect URIs**, eller avviker med en avsluttende slash eller et annet skjema. Googles feilside viser URI-en den mottok — sammenlign den tegn for tegn med den registrerte.

### Appen er blokkert / har ikke fullført verifisering

Samtykkeskjermen er **External** og står fortsatt i *Testing*. Publiser den, eller bytt appen til **Internal**.

### Tilgang blokkert: autorisasjonsfeil

Kontoen som forsøker å logge inn, er utenfor Workspace-domenet ditt mens samtykkeskjermen er **Internal**. Dette er tilsiktet oppførsel — Internal-apper godtar bare kontoer i organisasjonen.

### Endringer tar flere minutter

Google sprer endringer i legitimasjon og samtykkeskjerm asynkront. En nylig lagt til omdirigerings-URI kan bruke noen minutter på å tre i kraft; hvis en endring ser ut til å bli ignorert, vent og prøv igjen før du undersøker videre.

---

## Se også

- [Single Sign-On-oversikt](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
