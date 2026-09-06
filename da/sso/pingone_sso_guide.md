# Opsæt SSO med PingOne

PingOne er OIDC-kompatibel. To af dens værdier kræver særlig opmærksomhed: **environment ID**, som indgår i enhver endpoint-URL, og det **regionale domæne**, som varierer mellem nordamerikanske, europæiske, canadiske, Asien-Stillehav- og australske tenants.

Denne vejledning dækker **PingOne-siden**: oprettelse af applikationen og indsamling af de værdier, digna har brug for. Digna-siden — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og er beskrevet i [Oversigt over Single Sign-On](overview.md).

---

## Før du går i gang

| Krav | Bemærkninger |
|---|---|
| **PingOne-rolle** | Environment Admin eller Identity Data Admin på det valgte miljø |
| **Environment** | Det PingOne-miljø, dine digna-brugere tilhører |
| **digna redirect URI** | Den URL, brugerne returnerer til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Opret applikationen

1. Log ind i PingOne admin-konsollen og vælg dit environment
2. Gå til **Applications → Applications**
3. Klik på **+**-knappen
4. Angiv `digna` som **Application Name**
5. Vælg **OIDC Web App**
6. Klik på **Save**

!!! warning "Vælg OIDC Web App, ikke Single-Page App"

    *Single-Page App* og *Native App* opretter public clients, som ikke kan indeholde en secret. digna veksler autorisationskoden fra sin backend og har brug for den fortrolige **OIDC Web App**-type.

---

## Trin 2: Konfigurer Redirect URI

1. Åbn applikationens **Configuration**-fane
2. Klik på blyantikonet for at redigere
3. Bekræft at **Response Type** er *Code* og **Grant Type** er *Authorization Code*
4. Under **Redirect URIs** indtast din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. Sæt **Token Endpoint Authentication Method** til *Client Secret Post* eller *Client Secret Basic*
6. Klik på **Save**

---

## Trin 3: Aktivér applikationen

På applikationens række eller detalje-panel, skift toggle til **enabled**.

!!! warning "Nye applikationer starter deaktiverede"

    PingOne opretter applikationer i en deaktiveret tilstand. En deaktiveret applikation giver en fejl i autorisationssteget, som ikke nævner toggle-status, så det er værd at bekræfte dette inden yderligere fejlsøgning.

---

## Trin 4: Tildel scopes

1. Åbn **Resources**-fanen
2. Bekræft at `openid` er tildelt, og tilføj `profile` og `email` fra **OpenID Connect**-resource
3. Klik på **Save**

---

## Trin 5: Tildel brugere

1. Åbn **Access**-fanen
2. Tilføj populationen eller grupperne, hvis medlemmer må bruge digna
3. Klik på **Save**

---

## Trin 6: Indsaml credentials og Environment ID

På **Configuration**-fanen, udvid **General**:

- **Client ID** → bliver `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → bliver `DIGNA_OIDC_CLIENT_SECRET` (klik på øje-ikonet)
- **Environment ID** → indgår i discovery-URL'en

Den samme fane viser den færdiglavede **OIDC Discovery Endpoint**, som du kan kopiere direkte i stedet for at sammensætte den manuelt.

---

## Trin 7: Byg Discovery-URL'en

Erstat environment ID og domænet for din region:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domæne |
|---|---|
| North America | `auth.pingone.com` |
| Europe | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

For et europæisk environment:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopier den i stedet for at taste den"

    Det regionale domæne er den hyppigst forekommende fejl i en PingOne-integration, og en forkert region giver en 404 i stedet for en informativ besked. Brug **OIDC Discovery Endpoint**-værdien fra Trin 6.

---

## Trin 8: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

`key` i begge filer skal stemme overens — `pingone` her.

---

## Trin 9: Test

Genstart backend og webserver, og åbn derefter dashboardet. Se [Test af login](overview.md#testing-login) for den komplette tjekliste.

---

## Fejlfinding for PingOne

### 404 på discovery-URL'en

Det regionale domæne eller environment ID er forkert. Sammenlign med **OIDC Discovery Endpoint** vist på applikationens Configuration-fane.

### NOT_FOUND eller applikationen er deaktiveret

Applikationens toggle fra Trin 3 er stadig slået fra.

### Redirect URI-mismatch

PingOne matcher hele strengen. Tjek **Configuration → Redirect URIs** for et trailing slash eller forskel i scheme.

### Login lykkes, men ingen email-claim når digna

Scopes `email` og `profile` er ikke blevet tildelt på **Resources**-fanen.

### Brugeren kan ikke se applikationen

Ingen population eller gruppe har fået adgang på **Access**-fanen.

---

## Se også

- [Oversigt over Single Sign-On](overview.md) — konfigurationsreference, test og generel fejlfinding
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)