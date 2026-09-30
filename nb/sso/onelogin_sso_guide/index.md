# Sett opp SSO med OneLogin

OneLogin er OIDC-kompatibel. Det som skiller den ut, er at connector-typen velges fra en katalog når appen opprettes, og ikke kan endres etterpå.

Denne veiledningen dekker **OneLogin-siden**: opprette applikasjonen og samle verdiene digna trenger. digna-siden — `dashboard_config.toml`, testing og feilsøking — er den samme for alle leverandører og beskrives i [Single Sign-On-oversikt](overview.md).

---

## Før du begynner

| Krav | Merknader |
|---|---|
| **OneLogin-rolle** | Kontoeier eller en administrator med tillatelse til å legge til applikasjoner |
| **Underdomene** | f.eks. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL-en brukere returnerer til etter innlogging, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trinn 1: Opprett OIDC-applikasjonen

1. Logg på OneLogin Admin-portalen
2. Gå til **Applications → Applications**
3. Klikk **Add App**
4. Søk etter `OpenId Connect` og velg connectoren **OpenId Connect (OIDC)**
5. Sett **Display Name** til `digna`
6. Klikk **Save**

!!! warning "Connector-typen låses ved opprettelse"

    OneLogin har separate katalogoppføringer for SAML og OIDC, og en applikasjon kan ikke konverteres fra den ene til den andre. Hvis du velger en SAML-connector ved en feil, sletter du appen og legger den til på nytt — det finnes ingen innstilling for å bytte protokoll.

---

## Trinn 2: Konfigurer omdirigerings-URI-en

1. Åpne fanen **Configuration**
2. I **Redirect URI's** legger du inn din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Sett eventuelt **Post Logout Redirect URIs** til dashbord-URL-en din
4. Klikk **Save**

!!! note "Én URI per linje"

    I motsetning til leverandører som forventer en kommaseparert liste, tar OneLogins felt **Redirect URI's** én URI per linje.

---

## Trinn 3: Angi applikasjonstype og autentiseringsmetode

1. Åpne fanen **SSO**
2. Bekreft at **Application Type** er *Web*
3. Sett **Token Endpoint → Authentication Method** til *POST* (`client_secret_post`) eller *Basic* (`client_secret_basic`)

!!! warning "Ikke velg None"

    Setter du autentiseringsmetoden til *None*, blir applikasjonen en public client uten secret, og dignas kodeutveksling fra backend vil bli avvist. Både POST og Basic fungerer.

---

## Trinn 4: Hent legitimasjonen

Fortsatt på fanen **SSO**:

- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klikk **Show client secret**)

Siden viser også **Issuer URL**, som bekrefter discovery-URL-en i neste trinn.

---

## Trinn 5: Tildel brukere

1. Åpne fanen **Access**
2. Legg til rollene eller gruppene hvis medlemmer skal kunne bruke digna
3. Klikk **Save**

!!! note "Ikke-tildelte brukere avvises etter innlogging"

    Som hos de fleste leverandører autentiserer OneLogin brukeren først og sjekker tilgangsrettigheten etterpå. En ikke-tildelt bruker logger inn vellykket og blir deretter avvist, noe som ser ut som en feil i digna og ikke som en beslutning i tilgangskontrollen.

---

## Trinn 6: Bygg discovery-URL-en

Sett inn OneLogin-underdomenet ditt:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

For eksempel:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 er API-versjonen"

    OneLogins nåværende OIDC-implementasjon ligger under `/oidc/2/`. Eldre dokumentasjon viser `/oidc/` uten versjon, som peker på den utfasede første versjonen. Sjekk **Issuer URL** på SSO-fanen hvis du er i tvil — discovery-URL-en er utstederen pluss `/.well-known/openid-configuration`.

---

## Trinn 7: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

`key` i begge filer må samsvare — `onelogin` her.

---

## Trinn 8: Test

Start backend og webserver på nytt, og åpne dashbordet. Se [Test av innlogging](overview.md#testing-login) for full sjekkliste.

---

## Feilsøking for OneLogin

### redirect_uri did not match

Callback-URL-en mangler i **Configuration → Redirect URI's**, eller oppføringene ble separert med komma i stedet for linjeskift.

### invalid_client ved token-steget

**Token Endpoint → Authentication Method** er satt til *None*, eller client secret i `config.toml` er utdatert. Vis secret på fanen **SSO** og sammenlign.

### Appen vises ikke for brukerne

Ingen rolle eller gruppe har fått tilgang på fanen **Access**.

### 404 på discovery-URL-en

Underdomenet er feil, eller URL-en mangler `/oidc/2/`. Sammenlign med **Issuer URL** som vises på SSO-fanen.

---

## Se også

- [Single Sign-On-oversikt](overview.md) — konfigurasjonsreferanse, testing og generell feilsøking
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)