# Sett opp SSO med Microsoft Entra ID

Microsoft Entra ID (tidligere Azure Active Directory) er en fullt OIDC-kompatibel leverandør, så digna integreres med den via standard discovery-endepunktet.

Denne guiden dekker **Entra ID-siden**: registrering av applikasjonen og innhenting av de fire verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og er beskrevet i [Oversikt over Single Sign-On](overview.md).

---

## Før du begynner

| Krav | Notater |
|---|---|
| **Entra ID-rolle** | Application Administrator, Cloud Application Administrator, or Global Administrator |
| **digna redirect URI** | URL-en brukerne returnerer til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Katalogen brukerne dine logger på |

---

## Trinn 1: Registrer applikasjonen

1. Logg inn på [Microsoft Entra admin center](https://entra.microsoft.com)
2. Gå til **Identity → Applications → App registrations**
3. Klikk **New registration**
4. Konfigurer:
   - **Name**: `digna` (vises for brukerne på samtykkeskjermen)
   - **Supported account types**: *Accounts in this organizational directory only* for a single-tenant deployment
5. Under **Redirect URI**, velg plattform **Web** og skriv inn din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klikk **Register**

!!! warning "Viktig"

    Plattformen må være **Web**, ikke *Single-page application*. digna bytter autorisasjonskoden fra backend ved hjelp av en client secret, noe SPA-plattformtypen ikke tillater.

---

## Trinn 2: Hent klient- og tenant-ID-er

På applikasjonens **Overview**-side, kopier:

- **Application (client) ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → brukes i discovery-URL-en

---

## Trinn 3: Opprett en client secret

1. Gå til **Certificates & secrets → Client secrets**
2. Klikk **New client secret**
3. Skriv inn en beskrivelse og velg utløpstid
4. Klikk **Add**
5. Kopier kolonnen **Value** umiddelbart

!!! warning "Kopier Value, ikke Secret ID"

    **Value** vises kun én gang, på denne siden, og kan ikke hentes igjen senere. **Secret ID** ved siden av ser lik ut, men er ikke selve secret — å bruke den gir en `invalid_client`-feil ved innlogging. Hvis du navigerer bort før du har kopiert, slett secret og opprett en ny.

!!! tip "Tips"

    Entra ID begrenser secret-levetid til 24 måneder, så hver SSO-integrasjon har en utløpsdato. Noter den et sted du vil se den — en utløpt secret stopper SSO for alle brukere samtidig, uten advarsel på innloggingssiden.

---

## Trinn 4: Bekreft API-tillatelser

1. Gå til **API permissions**
2. Bekreft at **Microsoft Graph → User.Read** (delegert) er til stede — den legges til som standard

Scopesene `openid`, `profile` og `email` som digna ber om er en del av standard OIDC-settet og trenger ingen separat samtykke. Hvis tenant-en din krever admin-samtykke for alle applikasjoner, klikk **Grant admin consent for &lt;tenant&gt;**.

---

## Trinn 5: Bygg discovery-URL-en

Sett inn **Directory (tenant) ID** fra Trinn 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Bruk v2.0-endepunktet"

    Segmentet `/v2.0/` er viktig. v1.0-endepunktet på `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` utsteder tokens i et eldre format og returnerer ikke de standard OIDC-claims digna forventer.

Åpne URL-en i en nettleser før du fortsetter. Et JSON-dokument bekrefter at tenant-ID-en er korrekt.

---

## Trinn 6: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

`key` i begge filene må stemme overens — `microsoft` her.

---

## Trinn 7: Test

Start backend og webserver på nytt, og åpne så dashboardet. Se [Teste innlogging](overview.md#testing-login) for hele sjekklisten.

---

## Feilsøking for Entra ID

### AADSTS50011: Redirect URI Mismatch

URI-en i `DIGNA_OIDC_REDIRECT_URI` avviker fra den som er registrert i Trinn 1. Entra ID sammenligner hele strengen, så en trailing slash, `http` vs `https` eller en annen port teller som mismatch. Sjekk **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Enten ble **Secret ID** kopiert i stedet for **Value**, eller så har secret utløpt. Opprett en ny secret og kopier kolonnen Value.

### AADSTS650057: Invalid Resource

Applikasjonsregistreringen ble slettet eller tilhører en annen tenant enn den i discovery-URL-en. Bekreft Directory (tenant) ID på Overview-siden.

### Brukere logger inn, men ingenting skjer

Hvis tenant-en krever admin-samtykke og det ikke er gitt, returnerer redirect uten et brukbart token. Gi admin-samtykke under **API permissions**.

---

## Se også

- [Oversikt over Single Sign-On](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [Microsoft: OAuth 2.0 autorisasjonskodeflyt](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)