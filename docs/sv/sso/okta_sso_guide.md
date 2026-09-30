---
title: Okta SSO – Single Sign-On-integration | digna Dokumentation
description: Konfigurera Single Sign-On för digna med Okta via OpenID Connect — appintegration, redirect-URI:er för inloggning, klientuppgifter, val av auktoriseringsserver och motsvarande digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, appintegration, auktoriseringsserver, openid connect, företagsautentisering
---

# Ställ in SSO med Okta

Okta följer OIDC-standarden, med en egenhet som överraskar de flesta vid första integrationen: en Okta-org exponerar mer än en auktoriseringsserver, och var och en har sin egen discovery-URL.

Denna guide täcker **Okta-sidan**: skapa appintegrationen och samla de värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är densamma för alla leverantörer och beskrivs i [Översikt över Single Sign-On](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **Okta-roll** | Super Administrator, eller en administratörsroll med behörighet att skapa appintegrationer |
| **Okta-domän** | t.ex. `yourcompany.okta.com`, eller en anpassad domän om en sådan är konfigurerad |
| **digna redirect URI** | URL:en dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Skapa appintegrationen

1. Logga in i Okta Admin Console
2. Gå till **Applications → Applications**
3. Klicka på **Create App Integration**
4. Välj:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klicka på **Next**

!!! warning "Applikationstypen kan inte ändras"

    Om du väljer *Single-Page Application* i stället för *Web Application* skapas en publik klient utan hemlighet, och kodutbytet i dignas backend misslyckas med `invalid_client`. Typen bestäms när appen skapas — ett felaktigt val innebär att du måste ta bort appen och börja om.

---

## Steg 2: Konfigurera integrationen

1. **App integration name**: `digna`
2. **Grant type**: låt *Authorization Code* vara valt
3. **Sign-in redirect URIs**: ange din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: valfritt
5. Under **Assignments**, välj vem som får använda integrationen — en specifik grupp är säkrare än *Allow everyone in your organization to access*
6. Klicka på **Save**

!!! note "Tilldelning krävs"

    Okta autentiserar användaren och kontrollerar sedan om hen är tilldelad applikationen. En användare som inte är tilldelad når Oktas inloggningssida, loggar in utan problem och nekas sedan vid omdirigeringen tillbaka. Om inloggningen fungerar för dig men inte för kollegor är tilldelningen det första du ska kontrollera.

---

## Steg 3: Samla in inloggningsuppgifterna

På applikationens flik **General**, under **Client Credentials**:

- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klicka på ögonikonen för att visa)

---

## Steg 4: Välj auktoriseringsserver

Det här steget avgör din discovery-URL. Gå till **Security → API** för att se auktoriseringsservrarna i din org.

**Org authorization server** — utfärdar token för själva Okta-orgen:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — inklusive den som Okta skapar med namnet `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

För den inbyggda servern är `<auth_server_id>` bokstavligen `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Vilken ska jag välja?"

    Använd **org**-auktoriseringsservern om inte din organisation redan har standardiserat på en anpassad server för API-åtkomstpolicyer. Okta Developer-konton använder `default` som standard; många företagsorgar inaktiverar den. Öppna båda URL:erna i en webbläsare — den som returnerar JSON i stället för ett fel är den som är tillgänglig för dig.

---

## Steg 5: Konfigurera digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc_clients.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

`key` i båda filerna måste matcha — här `okta`.

---

## Steg 6: Testa

Starta om backend och webbserver och öppna sedan dashboarden. Se [Testa inloggningen](overview.md#testing-login) för den fullständiga checklistan.

---

## Felsökning av Okta

### The redirect URI Is Not Registered

Okta anger den felaktiga URI:n i felmeddelandet. Jämför den med **General → Sign-in redirect URIs**; Okta matchar hela strängen, inklusive eventuellt avslutande snedstreck.

### User Is Not Assigned to the Client Application

Kontot finns inte i applikationens tilldelningslista. Lägg till användaren eller dennes grupp under **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` i discovery-URL:en finns inte, oftast `default` i en org där den har tagits bort. Kontrollera under **Security → API** vilka servrar som faktiskt finns.

### invalid_client i token-steget

Integrationen skapades som en Single-Page Application och har ingen klienthemlighet. Skapa den på nytt som en Web Application.

---

## Se även

- [Översikt över Single Sign-On](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
