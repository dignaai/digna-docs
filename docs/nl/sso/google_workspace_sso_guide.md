---
title: Google Workspace SSO – Single Sign-On-integratie | digna Documentatie
description: Configureer Single Sign-On voor digna met Google Workspace via OpenID Connect — OAuth-toestemmingsscherm, OAuth client ID, geautoriseerde redirect-URI's en de bijbehorende digna-configuratie.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth-toestemmingsscherm, openid connect, zakelijke authenticatie
---

# SSO instellen met Google Workspace

Het identiteitsplatform van Google is OIDC-conform en gebruikt voor elke klant één en dezelfde, bekende discovery-URL, dus de enige waarden per organisatie zijn de client ID en het secret.

Deze gids behandelt de **Google-kant**: het aanmaken van de OAuth-client en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **Google Cloud-project** | Elk project in dezelfde organisatie als je Workspace-domein |
| **Rol** | Editor of Owner op het project |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Configureer het OAuth-toestemmingsscherm

Google geeft geen credentials uit zolang het toestemmingsscherm niet bestaat.

1. Open de [Google Cloud Console](https://console.cloud.google.com) en selecteer je project
2. Ga naar **APIs & Services → OAuth consent screen**
3. Kies het gebruikerstype:
   - **Internal** — alleen accounts in je Workspace-domein kunnen inloggen. Aanbevolen.
   - **External** — elk Google-account kan proberen in te loggen.
4. Vul de appnaam, het e-mailadres voor gebruikersondersteuning en het contactadres van de ontwikkelaar in
5. Voeg bij de stap **Scopes** `openid`, `.../auth/userinfo.email` en `.../auth/userinfo.profile` toe
6. Sla op

!!! warning "External-apps moeten gepubliceerd zijn"

    Een toestemmingsscherm van het type **External** start met de status *Testing*, waarin alleen accounts die expliciet aan de lijst met testgebruikers zijn toegevoegd een login kunnen voltooien. Alle anderen zien "digna has not completed the Google verification process". Zet de app onder **Publishing status** op **In production**, of gebruik **Internal** — dat kent die beperking niet en is de juiste keuze voor een deployment die alleen voor Workspace bedoeld is.

---

## Stap 2: Maak de OAuth-client aan

1. Ga naar **APIs & Services → Credentials**
2. Klik **Create Credentials → OAuth client ID**
3. Stel **Application type** in op **Web application**
4. Geef hem een naam, bijv. `digna`
5. Klik onder **Authorized redirect URIs** op **Add URI** en voer in:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klik **Create**

!!! note "Authorized JavaScript origins zijn niet nodig"

    digna wisselt de autorisatiecode uit vanuit de backend, niet vanuit de browser, dus het veld **Authorized JavaScript origins** kan leeg blijven. Alleen de redirect URI telt.

---

## Stap 3: Verzamel de gegevens

Het dialoogvenster dat na het aanmaken verschijnt, toont:

- **Client ID** — eindigt op `.apps.googleusercontent.com` → wordt `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → wordt `DIGNA_OIDC_CLIENT_SECRET`

Anders dan bij de meeste andere providers blijven beide later op te vragen via de detailpagina van de credential.

---

## Stap 4: De discovery-URL

Google gebruikt één discovery-URL voor alle klanten — er hoeft niets te worden ingevuld:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Stap 5: Configureer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

De `key` moet in beide bestanden overeenkomen — hier `google`.

---

## Stap 6: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met Google Workspace

### Error 400: redirect_uri_mismatch

De URI in `DIGNA_OIDC_REDIRECT_URI` staat niet in de lijst **Authorized redirect URIs**, of wijkt af door een afsluitende slash of het schema. De foutpagina van Google toont de ontvangen URI — vergelijk die teken voor teken met de geregistreerde.

### Deze app is geblokkeerd / heeft de verificatie niet voltooid

Het toestemmingsscherm is **External** en staat nog op *Testing*. Publiceer het, of zet de app op **Internal**.

### Access Blocked: Authorization Error

Het account dat probeert in te loggen valt buiten je Workspace-domein, terwijl het toestemmingsscherm **Internal** is. Dit is het bedoelde gedrag — Internal-apps accepteren alleen accounts binnen de organisatie.

### Wijzigingen duren enkele minuten

Google verwerkt wijzigingen aan credentials en het toestemmingsscherm asynchroon. Een nieuw toegevoegde redirect URI kan een paar minuten nodig hebben om actief te worden; als een wijziging genegeerd lijkt, wacht dan even en probeer het opnieuw voordat je verder zoekt.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)
