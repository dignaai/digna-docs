---
title: Auth0 SSO – Single Sign-On-integratie | digna Documentatie
description: Configureer Single Sign-On voor digna met Auth0 via OpenID Connect — instellen van een regular web application, toegestane callback-URL's, clientgegevens, tenantdomein en de bijbehorende digna-configuratie.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regular web application, callback-url's, openid connect, zakelijke authenticatie
---

# SSO instellen met Auth0

Auth0 is OIDC-conform en biedt per tenant een discovery-endpoint. Het belangrijkste om goed te krijgen is het tenantdomein, dat in de discovery-URL staat en verandert als je een custom domain inschakelt.

Deze gids behandelt de **Auth0-kant**: het aanmaken van de applicatie en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **Auth0-rol** | Admin op de tenant |
| **Tenantdomein** | bijv. `yourcompany.eu.auth0.com` — het regiosegment is van belang |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Maak de applicatie aan

1. Log in op het [Auth0 Dashboard](https://manage.auth0.com)
2. Ga naar **Applications → Applications**
3. Klik **Create Application**
4. Noem hem `digna` en kies **Regular Web Applications**
5. Klik **Create**

!!! warning "Kies Regular Web Applications"

    *Single Page Application* en *Native* maken public clients aan zonder secret. digna voert de code-uitwisseling uit vanuit zijn backend en heeft een confidential client nodig, dus **Regular Web Applications** is het juiste type. Anders dan bij sommige providers kun je het type in Auth0 later nog wijzigen onder **Settings → Application Type**.

---

## Stap 2: Voeg de callback-URL toe

Op het tabblad **Settings** van de applicatie:

1. Zoek **Allowed Callback URLs**
2. Voer je digna callback-URL in:

```
https://digna.yourdomain.com/oidc/callback
```

3. Stel optioneel **Allowed Logout URLs** in op de URL van je dashboard
4. Scrol naar beneden en klik **Save Changes**

!!! note "Gescheiden door komma's, niet door nieuwe regels"

    Auth0 accepteert in dit veld meerdere callback-URL's, gescheiden door komma's. Een lijst die alleen door nieuwe regels is gescheiden, wordt gelezen als één ongeldige URL en komt stilzwijgend met niets overeen.

---

## Stap 3: Verzamel de gegevens

Nog steeds op **Settings**, in het paneel **Basic Information**:

- **Domain** → gaat in de discovery-URL
- **Client ID** → wordt `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → wordt `DIGNA_OIDC_CLIENT_SECRET` (klik om te tonen)

---

## Stap 4: Controleer het grant type

1. Ga naar **Settings → Advanced Settings → Grant Types**
2. Controleer of **Authorization Code** is aangevinkt

Dit is standaard ingeschakeld voor Regular Web Applications. Als het is uitgevinkt, mislukt het inloggen bij digna met `unauthorized_client`.

---

## Stap 5: Bouw de discovery-URL

Vul het **Domain** uit Stap 3 in:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Bijvoorbeeld:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Custom domains veranderen de issuer"

    Als je tenant een custom domain gebruikt, zoals `login.yourcompany.com`, gebruik dan dat domein in de discovery-URL. Als je de twee mengt — het canonieke domein in de discovery-URL, het custom domain in de browser — ontstaat een issuer-mismatch en wordt het token na een verder geslaagde login geweigerd.

---

## Stap 6: Configureer digna

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

De `key` moet in beide bestanden overeenkomen — hier `auth0`.

---

## Stap 7: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met Auth0

### Callback-URL komt niet overeen

De foutpagina van Auth0 noemt de URL die is ontvangen. Voeg die toe aan **Allowed Callback URLs** en controleer of de items door komma's zijn gescheiden.

### unauthorized_client

**Authorization Code** is niet ingeschakeld onder **Advanced Settings → Grant Types**, of het applicatietype is geen Regular Web Applications.

### Toegang geweigerd na een geslaagde login

Een Rule, Action of Post-Login-trigger in de tenant weigert de gebruiker. Controleer **Actions → Flows → Login** en de tenantlogs onder **Monitoring → Logs**, die de exacte reden tonen.

### Issuer-mismatch

De discovery-URL en het domein waarnaar de browser is gestuurd verschillen — meestal het canonieke tenantdomein tegenover een custom domain. Gebruik consequent één van beide.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
