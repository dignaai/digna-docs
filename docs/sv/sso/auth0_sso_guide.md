---
title: Auth0 SSO – Single Sign-On-integration | digna Dokumentation
description: Konfigurera Single Sign-On för digna med Auth0 via OpenID Connect — konfiguration av en Regular Web Application, tillåtna callback-URL:er, klientuppgifter, tenant-domän och motsvarande digna-konfiguration.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regular web application, callback-URL:er, openid connect, företagsautentisering
---

# Ställ in SSO med Auth0

Auth0 följer OIDC-standarden och exponerar en discovery-endpoint per tenant. Det viktigaste att få rätt är tenant-domänen, som ingår i discovery-URL:en och ändras om du aktiverar en anpassad domän.

Denna guide täcker **Auth0-sidan**: skapa applikationen och samla de värden digna behöver. digna-sidan — `dashboard_config.toml`, testning och felsökning — är densamma för alla leverantörer och beskrivs i [Översikt över Single Sign-On](overview.md).

---

## Innan du börjar

| Krav | Noteringar |
|---|---|
| **Auth0-roll** | Admin i tenanten |
| **Tenant-domän** | t.ex. `yourcompany.eu.auth0.com` — regionsegmentet spelar roll |
| **digna redirect URI** | URL:en dit användarna återvänder efter inloggning, t.ex. `https://digna.yourdomain.com/oidc/callback` |

---

## Steg 1: Skapa applikationen

1. Logga in i [Auth0 Dashboard](https://manage.auth0.com)
2. Gå till **Applications → Applications**
3. Klicka på **Create Application**
4. Ge den namnet `digna` och välj **Regular Web Applications**
5. Klicka på **Create**

!!! warning "Välj Regular Web Applications"

    *Single Page Application* och *Native* skapar publika klienter utan hemlighet. digna utför kodutbytet från sin backend och behöver en konfidentiell klient, så **Regular Web Applications** är rätt typ. Till skillnad från vissa leverantörer låter Auth0 dig ändra typen i efterhand under **Settings → Application Type**.

---

## Steg 2: Lägg till callback-URL:en

På applikationens flik **Settings**:

1. Leta upp **Allowed Callback URLs**
2. Ange din digna callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Ange vid behov **Allowed Logout URLs** till din dashboard-URL
4. Scrolla längst ned och klicka på **Save Changes**

!!! note "Kommaseparerade, inte radseparerade"

    Auth0 accepterar flera callback-URL:er i detta fält, separerade med kommatecken. En lista som bara är separerad med radbrytningar tolkas som en enda felaktig URL och matchar tyst ingenting.

---

## Steg 3: Samla in inloggningsuppgifterna

Fortfarande under **Settings**, i panelen **Basic Information**:

- **Domain** → används i discovery-URL:en
- **Client ID** → blir `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → blir `DIGNA_OIDC_CLIENT_SECRET` (klicka för att visa)

---

## Steg 4: Bekräfta grant-typen

1. Gå till **Settings → Advanced Settings → Grant Types**
2. Bekräfta att **Authorization Code** är ikryssad

Den är aktiverad som standard för Regular Web Applications. Om den har avmarkerats misslyckas inloggningen i digna med `unauthorized_client`.

---

## Steg 5: Bygg discovery-URL:en

Ersätt med **Domain** från Steg 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Till exempel:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Anpassade domäner ändrar utfärdaren"

    Om din tenant använder en anpassad domän som `login.yourcompany.com`, använd den domänen i discovery-URL:en. Att blanda de två — den kanoniska domänen i discovery-URL:en och den anpassade i webbläsaren — ger en issuer mismatch, och token avvisas efter en i övrigt lyckad inloggning.

---

## Steg 6: Konfigurera digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

`key` i båda filerna måste matcha — här `auth0`.

---

## Steg 7: Testa

Starta om backend och webbserver och öppna sedan dashboarden. Se [Testa inloggningen](overview.md#testing-login) för den fullständiga checklistan.

---

## Felsökning av Auth0

### Callback URL Mismatch

Auth0:s felsida anger den URL som togs emot. Lägg till den i **Allowed Callback URLs** och kontrollera att posterna är kommaseparerade.

### unauthorized_client

**Authorization Code** är inte aktiverad under **Advanced Settings → Grant Types**, eller så är applikationstypen inte Regular Web Applications.

### Åtkomst nekas efter en lyckad inloggning

En Rule, Action eller Post-Login-trigger i tenanten avvisar användaren. Kontrollera **Actions → Flows → Login** och tenantloggarna under **Monitoring → Logs**, som visar den exakta orsaken.

### Issuer mismatch

Discovery-URL:en och domänen som webbläsaren skickades till skiljer sig åt — oftast den kanoniska tenant-domänen jämfört med en anpassad domän. Använd en av dem konsekvent.

---

## Se även

- [Översikt över Single Sign-On](overview.md) — konfigurationsreferens, testning och allmän felsökning
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
