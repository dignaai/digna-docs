# Opsæt SSO med Auth0

Auth0 er OIDC-kompatibel og eksponerer et discovery-endpoint per tenant. Det vigtigste at få rigtigt er tenant-domænet, som indgår i discovery-URL'en og ændrer sig, hvis du aktiverer et custom domain.

Denne vejledning dækker **Auth0-siden**: oprettelse af applikationen og indsamling af de værdier, digna har brug for. digna-siden — `dashboard_config.toml`, test og fejlsøgning — er den samme for alle udbydere og beskrives i [Single Sign-On Overview](overview.md).

---

## Før du starter

| Krav | Bemærkninger |
|---|---|
| **Auth0-rolle** | Admin på tenant |
| **Tenant-domæne** | f.eks. `yourcompany.eu.auth0.com` — regionssegmentet betyder noget |
| **digna redirect URI** | URL'en brugere vender tilbage til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Opret applikationen

1. Log ind på [Auth0-dashboard](https://manage.auth0.com)
2. Gå til **Applications → Applications**
3. Klik **Create Application**
4. Navngiv den `digna` og vælg **Regular Web Applications**
5. Klik **Create**

!!! warning "Vælg Regular Web Applications"

    *Single Page Application* og *Native* opretter public clients uden secret. digna udfører code exchange fra sin backend og behøver en confidential client, så **Regular Web Applications** er den korrekte type. I modsætning til nogle udbydere lader Auth0 dig ændre typen senere under **Settings → Application Type**.

---

## Trin 2: Tilføj callback-URL'en

På applikationens **Settings**-fane:

1. Find **Allowed Callback URLs**
2. Indtast din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Sæt eventuelt **Allowed Logout URLs** til din dashboard-URL
4. Rul ned og klik **Save Changes**

!!! note "Komma-separeret, ikke adskilt med linjeskift"

    Auth0 accepterer flere callback-URL'er i dette felt, adskilt med kommaer. En liste kun adskilt af linjeskift læses som én ugyldig URL og matcher stilfærdigt ingenting.

---

## Trin 3: Indsaml legitimationsoplysningerne

Stadig under **Settings**, i panelet **Basic Information**:

- **Domain** → går ind i discovery-URL'en
- **Client ID** → bliver `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → bliver `DIGNA_OIDC_CLIENT_SECRET` (klik for at vise)

---

## Trin 4: Bekræft grant-typen

1. Gå til **Settings → Advanced Settings → Grant Types**
2. Bekræft at **Authorization Code** er markeret

Den er som standard aktiveret for Regular Web Applications. Hvis den er afmarkeret, fejler dignas login med `unauthorized_client`.

---

## Trin 5: Opbyg discovery-URL'en

Indsæt **Domain** fra Trin 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

For eksempel:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Custom Domains ændrer issuer"

    Hvis din tenant bruger et custom domain som `login.yourcompany.com`, skal du bruge det domæne i discovery-URL'en. At blande de to — det kanoniske domæne i discovery-URL'en og det custom i browseren — giver issuer-mismatch, og tokenet bliver afvist efter et ellers vellykket login.

---

## Trin 6: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Log ind med Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

`key` i begge filer skal matche — `auth0` her.

---

## Trin 7: Test

Genstart backend og webserver, og åbn derefter dashboardet. Se [Testing Login](overview.md#testing-login) for den fulde tjekliste.

---

## Fejlfinding for Auth0

### Callback URL-mismatch

Auth0s fejlside navngiver den URL, den modtog. Tilføj den til **Allowed Callback URLs**, og sørg for, at indtastninger er komma-separerede.

### unauthorized_client

**Authorization Code** er ikke aktiveret under **Advanced Settings → Grant Types**, eller applikationstypen er ikke Regular Web Applications.

### Adgang nægtet efter vellykket login

En Rule, Action eller post-login trigger i tenant'en afviser brugeren. Tjek **Actions → Flows → Login** og tenant-loggene under **Monitoring → Logs**, som viser den præcise årsag.

### Issuer-mismatch

Discovery-URL'en og det domæne, browseren blev sendt til, er forskellige — normalt det kanoniske tenant-domæne versus et custom domain. Brug ét konsistent domæne.

---

## Se også

- [Single Sign-On Overview](overview.md) — konfigurationsreference, test og generel fejlsøgning
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)