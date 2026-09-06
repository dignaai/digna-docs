# Opsæt SSO med OneLogin

OneLogin er OIDC-kompatibel. Dens karakteristiske træk er, at connector-typen vælges fra et katalog, når appen oprettes, og ikke kan ændres efterfølgende.

Denne vejledning dækker **OneLogin-siden**: oprettelse af applikationen og indsamling af de værdier, digna behøver. digna-siden — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og er beskrevet i [Single Sign-On Overview](overview.md).

---

## Før du begynder

| Krav | Bemærkninger |
|---|---|
| **OneLogin role** | Kontoindehaver eller en administrator med tilladelse til at tilføje applikationer |
| **Subdomain** | f.eks. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL'en brugere returnerer til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Opret OIDC-applikationen

1. Log ind på OneLogin Admin-portalen
2. Gå til **Applications → Applications**
3. Klik **Add App**
4. Søg efter `OpenId Connect` og vælg **OpenId Connect (OIDC)** connectoren
5. Sæt **Display Name** til `digna`
6. Klik **Save**

!!! warning "Connector-typen er fast ved oprettelse"

    OneLogin har separate katalogindgange for SAML og OIDC, og en applikation kan ikke konverteres fra den ene til den anden. Hvis du ved en fejl vælger en SAML-connector, slet appen og tilføj den igen — der findes ingen indstilling til at skifte protokol.

---

## Trin 2: Konfigurer Redirect URI

1. Åbn fanen **Configuration**
2. I **Redirect URI's**, indtast din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Valgfrit: sæt **Post Logout Redirect URIs** til din dashboard-URL
4. Klik **Save**

!!! note "Én URI per linje"

    I modsætning til udbydere, der forventer en komma-separeret liste, accepterer OneLogin-feltet **Redirect URI's** én URI per linje.

---

## Trin 3: Indstil applikationstype og autentificeringsmetode

1. Åbn fanen **SSO**
2. Bekræft at **Application Type** er *Web*
3. Sæt **Token Endpoint → Authentication Method** til *POST* (`client_secret_post`) eller *Basic* (`client_secret_basic`)

!!! warning "Vælg ikke None"

    At sætte autentificeringsmetoden til *None* gør applikationen til en public client uden secret, og dignas backend-kodeudveksling vil blive afvist. Enten POST eller Basic fungerer.

---

## Trin 4: Indsaml legitimationsoplysninger

Fortsat på fanen **SSO**:

- **Client ID** → bliver `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → bliver `DIGNA_OIDC_CLIENT_SECRET` (klik **Show client secret**)

Siden viser også **Issuer URL**, som bekræfter discovery-URL'en i næste trin.

---

## Trin 5: Tildel brugere

1. Åbn fanen **Access**
2. Tilføj de roller eller grupper, hvis medlemmer må bruge digna
3. Klik **Save**

!!! note "Uden tildeling afvises brugere efter login"

    Som med de fleste udbydere godkender OneLogin først brugeren og tjekker derefter rettigheder. En ikke-tildelt bruger logger ind succesfuldt og bliver derefter afvist, hvilket fremstår som en digna-fejl i stedet for en adgangskontrolbeslutning.

---

## Trin 6: Sammensæt Discovery-URL'en

Indsæt dit OneLogin-subdomæne:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

For eksempel:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip " /2 er API-versionen"

    OneLogins nuværende OIDC-implementering ligger under `/oidc/2/`. Ældre dokumentation viser `/oidc/` uden en version, hvilket peger på den pensionerede første version. Tjek **Issuer URL** på SSO-fanen hvis du er i tvivl — discovery-URL'en er issuer plus `/.well-known/openid-configuration`.

---

## Trin 7: Konfigurer digna

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
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

`key` i begge filer skal stemme overens — `onelogin` her.

---

## Trin 8: Test

Genstart backend- og webserveren, og åbn derefter dashboardet. Se [Testing Login](overview.md#testing-login) for den fulde tjekliste.

---

## Fejlfinding af OneLogin

### redirect_uri matchede ikke

Callback-URL'en mangler i **Configuration → Redirect URI's**, eller indtastningerne var adskilt med kommaer i stedet for nye linjer.

### invalid_client ved token-trinnet

**Token Endpoint → Authentication Method** er sat til *None*, eller klientsecret i `config.toml` er forældet. Vis secret på fanen **SSO** og sammenlign.

### Appen vises ikke for brugere

Ingen roller eller grupper har fået adgang på fanen **Access**.

### 404 på Discovery-URL'en

Subdomeinet er forkert, eller URL'en udelader `/oidc/2/`. Sammenlign med **Issuer URL** vist på SSO-fanen.

---

## Se også

- [Oversigt over Single Sign-On](overview.md) — konfigurationsreference, test og generel fejlfinding
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)