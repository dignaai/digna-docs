---
title: Okta SSO – Single Sign-On-integration | digna-dokumentation
description: Konfigurer Single Sign-On for digna med Okta ved brug af OpenID Connect — app-integration, sign-in redirect URIs, klientlegitimationsoplysninger, valg af autoriseringsserver og den matchende digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, app integration, authorization server, openid connect, virksomhedsautentificering
---

# Opsæt SSO med Okta

Okta er OIDC-kompatibel, men der er én detalje, der fanger de fleste førstegangsintegrationer: en Okta-org eksponerer mere end én autoriseringsserver, og hver har sin egen discovery-URL.

Denne vejledning dækker **Okta-siden**: oprettelse af app-integrationen og indsamling af de værdier, digna har brug for. digna-siden — `dashboard_config.toml`, test og fejlfinding — er den samme for alle udbydere og er beskrevet i [Single Sign-On-oversigten](overview.md).

---

## Før du begynder

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator, eller en adminrolle med rettighed til at oprette app-integrations |
| **Okta domain** | f.eks. `yourcompany.okta.com`, eller et custom domain hvis det er konfigureret |
| **digna redirect URI** | Den URL, brugere returnerer til efter login, f.eks. `https://digna.yourdomain.com/oidc/callback` |

---

## Trin 1: Opret App Integration

1. Log ind på Okta Admin Console
2. Gå til **Applications → Applications**
3. Klik **Create App Integration**
4. Vælg:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klik **Next**

!!! warning "Applikationstypen kan ikke ændres"

    Hvis du vælger *Single-Page Application* i stedet for *Web Application* oprettes en public client uden secret, og digna's backend code exchange vil fejle med `invalid_client`. Typen er fast ved oprettelse — et forkert valg betyder, at appen skal slettes og oprettes igen.

---

## Trin 2: Konfigurer integrationen

1. **App integration name**: `digna`
2. **Grant type**: lad *Authorization Code* stå valgt
3. **Sign-in redirect URIs**: indtast din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: valgfrit
5. Under **Assignments**, vælg hvem der må bruge integrationen — en specifik gruppe er sikrere end *Allow everyone in your organization to access*
6. Klik **Save**

!!! note "Tildeling er påkrævet"

    Okta autentificerer brugeren og tjekker derefter, om brugeren er tildelt applikationen. En ikke-tildelt bruger når Okta-login-siden, logger ind korrekt, men bliver afvist ved redirect tilbage. Hvis login virker for dig, men ikke for kolleger, er tildeling det første, du bør kontrollere.

---

## Trin 3: Indsaml legitimationsoplysninger

På applikationens **General**-fane, under **Client Credentials**:

- **Client ID** → bliver `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → bliver `DIGNA_OIDC_CLIENT_SECRET` (klik på øje-ikonet for at vise)

---

## Trin 4: Vælg autoriseringsserver

Dette trin bestemmer din discovery-URL. Gå til **Security → API** for at se autoriseringsserverne i din org.

**Org authorization server** — udsender tokens for selve Okta-org'en:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — inklusive den Okta opretter kaldet `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

For den indbyggede server er `<auth_server_id>` bogstaveligt talt `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Hvilken skal jeg vælge?"

    Brug **org**-autoriseringsserveren medmindre din organisation allerede standardiserer på en custom server til API-adgangspolitikker. Okta Developer-konti bruger som standard `default`; mange enterprise-orgs deaktiverer den. Åbn begge URL'er i en browser — den, der returnerer JSON i stedet for en fejl, er den, der er tilgængelig for dig.

---

## Trin 5: Konfigurer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Log ind med Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<den klienthemmelighed kopieret i trin 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Værdien af `key` i begge filer skal matche — `okta` her.

---

## Trin 6: Test

Genstart backend og webserver, og åbn dashboardet. Se [Testing Login](overview.md#testing-login) for den komplette tjekliste.

---

## Fejlfinding — Okta

### Redirect URI'en er ikke registreret

Okta angiver den problematiske URI i fejlen. Sammenlign den med **General → Sign-in redirect URIs**; Okta matcher hele strengen inklusive eventuel afsluttende skråstreg.

### Brugeren er ikke tildelt klientapplikationen

Kontoen er ikke på applikationens tildelingsliste. Tilføj brugeren eller deres gruppe under **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` i discovery-URL'en findes ikke, oftest `default` i en org hvor den er fjernet. Tjek **Security → API** for de servere, der faktisk er tilgængelige.

### invalid_client ved token-trinnet

Integrationen blev oprettet som en Single-Page Application og har ingen client secret. Opret den igen som Web Application.

---

## Se også

- [Single Sign-On-oversigten](overview.md) — konfigurationsreference, test og generel fejlfinding
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)