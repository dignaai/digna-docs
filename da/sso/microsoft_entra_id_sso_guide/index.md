# Opsæt SSO med Microsoft Entra ID

Microsoft Entra ID (tidligere Azure Active Directory) er en fuldt OIDC-kompatibel udbyder, så digna integrerer med den via standard discovery-endpointet.

Denne guide dækker **Entra ID-siden**: registrering af applikationen og indsamling af de fire værdier, digna har brug for. digna-siden — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og er beskrevet i [Oversigt over Single Sign-On](overview.md).

---

## Før du går i gang

| Krav | Bemærkninger |
|---|---|
| **Entra ID role** | Application Administrator, Cloud Application Administrator, or Global Administrator |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | The directory your users sign in to |

---

## Trin 1: Registrer applikationen

1. Log ind på [Microsoft Entra admin center](https://entra.microsoft.com)
2. Gå til **Identity → Applications → App registrations**
3. Klik **New registration**
4. Konfigurér:
   - **Name**: `digna` (vises for brugerne på consent-skærmen)
   - **Supported account types**: *Accounts in this organizational directory only* for a single-tenant deployment
5. Under **Redirect URI**, vælg platform **Web** og indtast din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klik **Register**

!!! warning "Vigtigt"

    Platformen skal være **Web**, ikke *Single-page application*. digna bytter autorisationskoden fra backend ved hjælp af en client secret, hvilket SPA-platformtypen ikke tillader.

---

## Trin 2: Indsaml Client- og Tenant-ID'er

På applikationens **Overview**-side, kopier:

- **Application (client) ID** → bliver `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → indsættes i discovery-URL'en

---

## Trin 3: Opret en Client Secret

1. Gå til **Certificates & secrets → Client secrets**
2. Klik **New client secret**
3. Indtast en beskrivelse og vælg en udløbstid
4. Klik **Add**
5. Kopiér kolonnen **Value** med det samme

!!! warning "Kopiér Value, ikke Secret ID"

    **Value** vises kun én gang, på denne side, og kan ikke hentes igen. **Secret ID** ved siden af ligner, men er ikke selve secret — brug af den giver en `invalid_client`-fejl ved login. Hvis du navigerer væk før kopiering, slet secret'en og opret en ny.

!!! tip "Tip"

    Entra ID begrænser secret-livstiden til 24 måneder, så hver SSO-integration har en udløbsdato. Notér den et sted, hvor du ser den — en udløbet secret slukker SSO for alle brugere samtidigt, uden advarsel på login-siden.

---

## Trin 4: Bekræft API-tilladelserne

1. Gå til **API permissions**
2. Bekræft at **Microsoft Graph → User.Read** (delegated) er til stede — det tilføjes som standard

De `openid`, `profile` og `email` scopes, som digna anmoder om, er del af standard OIDC-sættet og kræver ingen separat grant. Hvis din tenant kræver admin-consent for alle applikationer, klik **Grant admin consent for <tenant>**.

---

## Trin 5: Byg Discovery-URL'en

Indsæt **Directory (tenant) ID** fra Trin 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Brug v2.0-endpointet"

    Segmentet `/v2.0/` er vigtigt. v1.0-endpointet på `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` udsteder tokens i et ældre format og returnerer ikke de standard OIDC-claims, som digna forventer.

Åbn URL'en i en browser før du fortsætter. Et JSON-dokument bekræfter, at tenant-id'et er korrekt.

---

## Trin 6: Konfigurer digna

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

`key` i begge filer skal matche — `microsoft` her.

---

## Trin 7: Test

Genstart backend og webserver, og åbn derefter dashboardet. Se [Test af login](overview.md#testing-login) for den fulde tjekliste.

---

## Fejlfinding for Entra ID

### AADSTS50011: Redirect URI-mismatch

URI'en i `DIGNA_OIDC_REDIRECT_URI` er forskellig fra den, der er registreret i Trin 1. Entra ID sammenligner hele strengværdien, så en afsluttende skråstreg, `http` kontra `https`, eller en anden port tæller alle som mismatch. Tjek **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Enten blev **Secret ID** kopieret i stedet for **Value**, eller secret'en er udløbet. Opret en ny secret og kopier kolonnen Value.

### AADSTS650057: Invalid Resource

Applikationsregistreringen blev slettet eller tilhører en anden tenant end den i discovery-URL'en. Bekræft Directory (tenant) ID på Overview-siden.

### Brugere logger ind, men der sker ingenting

Hvis tenant'en kræver admin-consent og det ikke er blevet givet, returnerer redirecten uden et brugbart token. Giv admin-consent under **API permissions**.

---

## Se også

- [Oversigt over Single Sign-On](overview.md) — konfigurationsreference, test og generel fejlfinding
- [Microsoft: OAuth 2.0 autorisationskodeflow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)