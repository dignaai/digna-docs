# Sett opp SSO med Keycloak

Keycloak er en selv-hostet, fullt OIDC-kompatibel identitetsleverandør. Fordi du kjører den selv, bygges discovery-URLen fra ditt eget vertsnavn og realm i stedet for et leverandørdomene.

Denne guiden dekker **Keycloak-siden**: opprette klienten og samle verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Oversikt for Single Sign-On](overview.md).

---

## Før du begynner

| Krav | Merknader |
|---|---|
| **Keycloak-versjon** | 17 eller nyere for URL-stiene som brukes her — se merknaden i Trinn 4 |
| **Keycloak-rolle** | `realm-admin` i målrealm, eller en serveradministrator |
| **Realm** | Realm brukerne dine i digna hører til i, ikke nødvendigvis `master` |
| **digna redirect URI** | URL-en brukerne kommer tilbake til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Velg realm

1. Åpne Keycloak admin-konsoll
2. Bruk realm-velgeren øverst til venstre for å bytte til realm brukerne dine ligger i

!!! warning "Ikke bruk `master`-realm"

    `master`-realm er ment for administrasjon av Keycloak selv. Applikasjonsklienter hører hjemme i et dedikert realm; å plassere digna i `master` gir dets brukere tilgang til Keycloak-administrasjonskonsollen.

---

## Trinn 2: Opprett klienten

1. Gå til **Clients** og klikk **Create client**
2. Konfigurer:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — dette blir `DIGNA_OIDC_CLIENT_ID`
3. Klikk **Next**
4. På steget **Capability config**, slå **Client authentication** **On**
5. La **Standard flow** være aktivert; de andre flowene er ikke nødvendige
6. Klikk **Next**

!!! warning "Client Authentication må være på"

    Med **Client authentication** av, oppretter Keycloak en *public* klient, som ikke har noen legitimasjon overhodet — fanen **Credentials** i Trinn 4 vil ikke eksistere. digna trenger en konfidensiell klient. Denne bryteren kan endres etter opprettelse hvis det blir feil.

---

## Trinn 3: Angi Redirect URI

På steget **Login settings** (eller fanen **Settings** i ettertid):

1. **Valid redirect URIs**: skriv inn din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: la stå tomt, eller sett til `+` for å speile redirect-URIene
3. Klikk **Save**

!!! tip "Unngå wildcards"

    Keycloak aksepterer mønstre som `https://digna.yourdomain.com/*`. Et wildcard lar hvilken som helst sti på det hostnavnet motta en autorisasjonskode, så foretrekk den eksakte callback-URLen.

---

## Trinn 4: Hent klienthemmeligheten

1. Åpne fanen **Credentials**
2. Bekreft at **Client Authenticator** er *Client Id and Secret*
3. Kopier **Client secret** → blir `DIGNA_OIDC_CLIENT_SECRET`

Hemmeligheten kan hentes her senere og kan regenereres med **Regenerate**.

---

## Trinn 5: Bygg discovery-URLen

Bytt ut din Keycloak-host og realm-navn:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

For eksempel:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 og tidligere inkluderer /auth"

    Før Keycloak 17 lå alle endepunkter under et `/auth`-prefiks:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribusjoner som setter `KC_HTTP_RELATIVE_PATH=/auth` beholder det gamle oppsettet også i nyere versjoner. Hvis URLen uten `/auth` returnerer 404, prøv med.

Åpne URLen i en nettleser før du fortsetter. Et JSON-dokument bekrefter at host og realm er riktige.

---

## Trinn 6: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Nøkkelen (`key`) i begge filer må stemme — `keycloak` her. Merk at den ikke trenger å være lik Keycloak **Client ID**, selv om det er enklere å holde dem like.

---

## Trinn 7: Test

Start backend og webserver på nytt, og åpne så dashboardet. Se [Testing Login](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking for Keycloak

### Invalid parameter: redirect_uri

Callback-URLen dekkes ikke av **Valid redirect URIs**. Keycloak logger URIen den mottok i serverloggen, som er raskeste måte å se den eksakte mismatchen på.

### Fanen Credentials mangler

Klienten er public. Slå på **Client authentication** under **Settings → Capability config**.

### 404 på Discovery-URLen

Enten er realm-navnet feil, eller distribusjonen bruker `/auth`-prefikset. Sjekk listen over realms i admin-konsollen og prøv begge URL-formene.

### unauthorized_client eller invalid_client

**Standard flow** er deaktivert under **Capability config**, eller hemmeligheten ble regenerert i Keycloak uten å oppdatere `config.toml`.

### Sertifikatfeil fra backend

En selv-hostet Keycloak bak et privat eller selvsignert sertifikat vil feile ved dignas utgående HTTPS-kall til discovery-URLen. Installer utstedende CA i trust store på maskinen som kjører digna-backenden.

---

## Se også

- [Oversikt for Single Sign-On](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)