---
title: Keycloak SSO – Single Sign-On-integration | digna-dokumentation
description: Konfigurer Single Sign-On for digna med Keycloak via OpenID Connect — realm- og client-opsætning, klientautentifikation, gyldige redirect URI'er, client secret og den tilsvarende digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, confidential client, openid connect, selvhostet identitetsudbyder
---

# Opsæt SSO med Keycloak

Keycloak er en selvhostet, fuldt OIDC-kompatibel identitetsudbyder. Da du selv hoster den, bygges discovery-URL'en ud fra dit eget værtsnavn og din realm i stedet for et leverandørdomæne.

Denne vejledning dækker **Keycloak-delen**: oprettelse af client og indsamling af de værdier, digna har brug for. digna-delen — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og er beskrevet i [Single Sign-On Overview](overview.md).

---

## Før du går i gang

| Krav | Bemærkninger |
|---|---|
| **Keycloak version** | 17 eller nyere for de URL-stier, der bruges her — se bemærkningen i Trin 4 |
| **Keycloak-rolle** | `realm-admin` på den pågældende realm, eller en serveradministrator |
| **Realm** | Den realm, dine digna-brugere tilhører, ikke nødvendigvis `master` |
| **digna redirect URI** | URL'en brugerne returneres til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Vælg realmet

1. Åbn Keycloak admin-konsollen
2. Brug realm-vælgeren øverst til venstre for at skifte til det realm, dine brugere er i

!!! warning "Brug ikke master-realm"

    `master`-realmet er beregnet til administration af Keycloak selv. Applikationsclients hører hjemme i et dedikeret realm; at placere digna i `master` giver dets brugere adgang til Keycloak-administrationskonsollen.

---

## Trin 2: Opret clienten

1. Gå til **Clients** og klik **Create client**
2. Konfigurer:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — dette bliver `DIGNA_OIDC_CLIENT_ID`
3. Klik **Next**
4. På trinnet **Capability config**, sæt **Client authentication** **On**
5. Lad **Standard flow** være aktiveret; de andre flows er ikke nødvendige
6. Klik **Next**

!!! warning "Client authentication skal være On"

    Hvis **Client authentication** er slået fra, opretter Keycloak en *public* client, som ingen legitimationsoplysninger har — fanen **Credentials** i Trin 4 vil ikke eksistere. digna kræver en confidential client. Denne indstilling kan ændres efter oprettelsen, hvis du kommer til at vælge forkert.

---

## Trin 3: Indstil Redirect URI

På trinnet **Login settings** (eller fanen **Settings** bagefter):

1. **Valid redirect URIs**: indtast din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: lad være tom, eller sæt til `+` for at spejle redirect URIs
3. Klik **Save**

!!! tip "Undgå wildcards"

    Keycloak accepterer mønstre som `https://digna.yourdomain.com/*`. Et wildcard lader enhver sti på det host-modtager et authorization code, så foretræk den præcise callback-URL.

---

## Trin 4: Indsaml client secret

1. Åbn fanen **Credentials**
2. Bekræft at **Client Authenticator** er *Client Id and Secret*
3. Kopiér **Client secret** → bliver `DIGNA_OIDC_CLIENT_SECRET`

Secret'et kan altid hentes her og kan regenereres med **Regenerate**.

---

## Trin 5: Byg discovery-URL'en

Erstat dit Keycloak-host og realm-navn:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

For eksempel:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 og tidligere inkluderer /auth"

    Før Keycloak 17 lå alle endpoints under et `/auth`-præfiks:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distributioner, der sætter `KC_HTTP_RELATIVE_PATH=/auth`, bevarer det gamle layout også på nyere versioner. Hvis URL'en uden `/auth` returnerer 404, prøv den med.

Åbn URL'en i en browser før du fortsætter. Et JSON-dokument bekræfter, at host og realm er korrekte.

---

## Trin 6: Konfigurer digna

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

Nøglen (`key`) i begge filer skal matche — `keycloak` her. Bemærk, at den ikke behøver at være lig med Keycloak **Client ID**, selvom det er nemmere at følge, hvis de er ens.

---

## Trin 7: Test

Genstart backend og webserver, og åbn derefter dashboardet. Se [Testing Login](overview.md#testing-login) for den fulde tjekliste.

---

## Fejlfinding for Keycloak

### Invalid parameter: redirect_uri

Callback-URL'en er ikke dækket af **Valid redirect URIs**. Keycloak logger den URI, den modtog, i serverloggen, hvilket er den hurtigste måde at se den nøjagtige mismatch på.

### Fanen Credentials mangler

Clienten er public. Sæt **Client authentication** til On under **Settings → Capability config**.

### 404 på discovery-URL'en

Enten er realm-navnet forkert, eller deploymenten bruger `/auth`-præfikset. Tjek ream-listen i admin-konsollen og prøv begge URL-former.

### unauthorized_client eller invalid_client

**Standard flow** er deaktiveret under **Capability config**, eller secret'et er regenereret i Keycloak uden opdatering af `config.toml`.

### Certifikatfejl fra backenden

En selvhostet Keycloak bag et privat eller selvsigneret certifikat vil få digna's udgående HTTPS-kald til discovery-URL'en til at fejle. Installer den udstedende CA i trust store på maskinen, der kører digna-backenden.

---

## Se også

- [Single Sign-On Overview](overview.md) — konfigurationsreference, test og generel fejlfinding
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)