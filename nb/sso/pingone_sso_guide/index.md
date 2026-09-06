# Sett opp SSO med PingOne

PingOne er OIDC-kompatibelt. To av verdiene krever spesiell oppmerksomhet: **environment ID**, som vises i hver endepunkts-URL, og det **regionale domenet**, som varierer mellom Nord-Amerika, Europa, Canada, Asia-Stillehav og Australia.

Denne guiden dekker **PingOne-siden**: opprette applikasjonen og samle verdiene digna trenger. Digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Oversikt over Single Sign-On](overview.md).

---

## Før du begynner

| Krav | Notater |
|---|---|
| **PingOne-rolle** | Environment Admin eller Identity Data Admin på målmiljøet |
| **Environment** | PingOne-miljøet brukerne dine i digna tilhører |
| **digna redirect URI** | URLen brukerne returnerer til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Opprett applikasjonen

1. Logg inn i PingOne admin-konsollen og velg miljøet ditt
2. Gå til **Applications → Applications**
3. Klikk på **+**-knappen
4. Angi `digna` som **Application Name**
5. Velg **OIDC Web App**
6. Klikk **Save**

!!! warning "Velg OIDC Web App, ikke Single-Page App"

    *Single-Page App* og *Native App* oppretter public clients som ikke kan holde en secret. digna bytter autorisasjonskoden fra sin backend og trenger den konfidensielle **OIDC Web App**-typen.

---

## Trinn 2: Konfigurer Redirect URI

1. Åpne applikasjonens **Configuration**-fane
2. Klikk på blyantikonet for å redigere
3. Bekreft at **Response Type** er *Code* og **Grant Type** er *Authorization Code*
4. Under **Redirect URIs**, legg inn digna callback-URLen din:

```
https://digna.yourdomain.com/oidc/callback
```

5. Sett **Token Endpoint Authentication Method** til *Client Secret Post* eller *Client Secret Basic*
6. Klikk **Save**

---

## Trinn 3: Aktiver applikasjonen

På applikasjonens rad eller i detaljpanelet, sett toggelen til **enabled**.

!!! warning "Nye applikasjoner starter deaktivert"

    PingOne oppretter applikasjoner i deaktivert tilstand. En deaktivert applikasjon gir en feil på autorisasjonssteget som ikke nevner toggelen, så dette er verdt å sjekke før du starter annen feilsøking.

---

## Trinn 4: Gi rettigheter til scopes

1. Åpne **Resources**-fanen
2. Bekreft at `openid` er gitt, og legg til `profile` og `email` fra **OpenID Connect**-ressursen
3. Klikk **Save**

---

## Trinn 5: Tildel brukere

1. Åpne **Access**-fanen
2. Legg til populasjonen eller gruppene hvis medlemmer kan bruke digna
3. Klikk **Save**

---

## Trinn 6: Hent legitimasjon og Environment ID

På **Configuration**-fanen, ekspander **General**:

- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klikk på øye-ikonet)
- **Environment ID** → går inn i discovery-URLen

Den samme fanen viser den ferdiglagde **OIDC Discovery Endpoint**, som du kan kopiere direkte i stedet for å bygge den manuelt.

---

## Trinn 7: Bygg discovery-URLen

Bytt ut environment ID og domenet for din region:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domene |
|---|---|
| Nord-Amerika | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Stillehav | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

For et europeisk miljø:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopier den i stedet for å skrive den"

    Det regionale domenet er den vanligste feilen i en PingOne-integrasjon, og feil region gir en 404 i stedet for en nyttig melding. Bruk **OIDC Discovery Endpoint**-verdien fra Trinn 6.

---

## Trinn 8: Konfigurer digna

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

Nøkkelen `key` i begge filene må samsvare — `pingone` her.

---

## Trinn 9: Test

Restart backend og webserver, og åpne deretter dashboardet. Se [Oversikt over Single Sign-On](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking for PingOne

### 404 på discovery-URLen

Det regionale domenet eller environment ID er feil. Sammenlign med **OIDC Discovery Endpoint** vist på applikasjonens Configuration-fane.

### NOT_FOUND eller applikasjonen er deaktivert

Applikasjonstoggelen fra Trinn 3 er fortsatt av.

### Redirect URI mismatch

PingOne matcher hele strengen. Sjekk **Configuration → Redirect URIs** for et slutt-skråstrek eller forskjell i scheme.

### Innlogging lykkes, men ingen email-claim når digna

Scope-ene `email` og `profile` er ikke gitt på **Resources**-fanen.

### Brukeren ser ikke applikasjonen

Ingen populasjon eller gruppe har fått tilgang på **Access**-fanen.

---

## Se også

- [Oversikt over Single Sign-On](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)