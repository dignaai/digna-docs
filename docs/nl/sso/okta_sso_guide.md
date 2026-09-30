---
title: Okta SSO – Single Sign-On-integratie | digna Documentatie
description: Configureer Single Sign-On voor digna met Okta via OpenID Connect — app integration, sign-in redirect-URI's, clientgegevens, keuze van de authorization server en de bijbehorende digna-configuratie.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, app integration, authorization server, openid connect, zakelijke authenticatie
---

# SSO instellen met Okta

Okta is OIDC-conform, met één eigenaardigheid waar de meeste eerste integraties over struikelen: een Okta-org biedt meer dan één authorization server, en elk daarvan heeft een eigen discovery-URL.

Deze gids behandelt de **Okta-kant**: het aanmaken van de app integration en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **Okta-rol** | Super Administrator, of een beheerdersrol die app integrations mag aanmaken |
| **Okta-domein** | bijv. `yourcompany.okta.com`, of een custom domain als dat is geconfigureerd |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Maak de app integration aan

1. Log in op de Okta Admin Console
2. Ga naar **Applications → Applications**
3. Klik **Create App Integration**
4. Selecteer:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klik **Next**

!!! warning "Het applicatietype kan niet worden gewijzigd"

    Als je *Single-Page Application* kiest in plaats van *Web Application*, wordt een public client zonder secret aangemaakt, en mislukt de code-uitwisseling in de digna-backend met `invalid_client`. Het type ligt vast bij het aanmaken — een verkeerde keuze betekent de app verwijderen en opnieuw beginnen.

---

## Stap 2: Configureer de integratie

1. **App integration name**: `digna`
2. **Grant type**: laat *Authorization Code* geselecteerd
3. **Sign-in redirect URIs**: voer je digna callback-URL in:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: optioneel
5. Kies onder **Assignments** wie de integratie mag gebruiken — een specifieke groep is veiliger dan *Allow everyone in your organization to access*
6. Klik **Save**

!!! note "Toewijzing is verplicht"

    Okta authenticeert de gebruiker en controleert daarna of die aan de applicatie is toegewezen. Een niet-toegewezen gebruiker komt op de inlogpagina van Okta, logt succesvol in en wordt bij de redirect terug geweigerd. Als inloggen voor jou werkt maar niet voor collega's, controleer dan eerst de toewijzing.

---

## Stap 3: Verzamel de gegevens

Op het tabblad **General** van de applicatie, onder **Client Credentials**:

- **Client ID** → wordt `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → wordt `DIGNA_OIDC_CLIENT_SECRET` (klik op het oogpictogram om het te tonen)

---

## Stap 4: Kies de authorization server

Deze stap bepaalt je discovery-URL. Ga naar **Security → API** om de authorization servers in je org te zien.

**Org authorization server** — geeft tokens uit voor de Okta-org zelf:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — inclusief de server `default` die Okta aanmaakt:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Voor de ingebouwde server is `<auth_server_id>` letterlijk `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Welke kies je?"

    Gebruik de **org** authorization server, tenzij je organisatie voor API-toegangsbeleid al standaard een custom server gebruikt. Okta Developer-accounts gebruiken standaard `default`; veel zakelijke orgs schakelen die uit. Open beide URL's in een browser — de URL die JSON retourneert in plaats van een fout, is de URL die voor jou beschikbaar is.

---

## Stap 5: Configureer digna

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

De `key` moet in beide bestanden overeenkomen — hier `okta`.

---

## Stap 6: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met Okta

### De redirect URI is niet geregistreerd

Okta noemt de betreffende URI in de foutmelding. Vergelijk die met **General → Sign-in redirect URIs**; Okta vergelijkt de volledige string, inclusief een eventuele afsluitende slash.

### De gebruiker is niet toegewezen aan de clientapplicatie

Het account staat niet in de toewijzingslijst van de applicatie. Voeg de gebruiker of diens groep toe onder **Assignments**.

### 400 Bad Request: Invalid Authorization Server

De `<auth_server_id>` in de discovery-URL bestaat niet, meestal `default` in een org waar die is verwijderd. Controleer onder **Security → API** welke servers daadwerkelijk beschikbaar zijn.

### invalid_client bij de tokenstap

De integratie is aangemaakt als Single-Page Application en heeft geen client secret. Maak hem opnieuw aan als Web Application.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
