---
title: Overzicht Single Sign-On (SSO) | digna Documentatie
description: Hoe Single Sign-On in digna werkt met OpenID Connect (OIDC). Behandelt dashboard- en backendconfiguratie, testen, probleemoplossing en links naar installatiegidsen per provider voor Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne en AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc-integratie
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta-integratie
  - zakelijke authenticatie
lang: nl
robots: index, follow
og_title: digna Single Sign-On (SSO) integratiegids
og_description: Configureer Single Sign-On voor digna met OpenID Connect. Stapsgewijze instelling voor Microsoft Entra ID, Google Workspace, Okta en andere OIDC-conforme identiteitsproviders.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Overzicht Single Sign-On

---

## Inhoudsopgave

1. [Introductie en overzicht](#introduction-and-overview)
2. [Gidsen per provider](#provider-guides)
3. [Configuratiestappen](#configuration-steps)
4. [Dashboardconfiguratie](#dashboard-configuration)
5. [Backendconfiguratie](#backend-configuration)
6. [Inloggen testen](#testing-login)
7. [Problemen oplossen](#troubleshooting)
8. [Ondersteunde providers](#supported-providers)

---

## Introductie en overzicht {: #introduction-and-overview }

Deze gids geeft stapsgewijze instructies voor het integreren van Single Sign-On (SSO) met het digna-platform via **OpenID Connect (OIDC)**.

### Wat is SSO?

Met Single Sign-On kunnen gebruikers veilig inloggen bij digna met hun zakelijke inloggegevens via externe identiteitsproviders. Gebruikers authenticeren zich met hun bedrijfsaccount in plaats van aparte digna-wachtwoorden te beheren.

### Hoe het werkt

SSO in digna is geïmplementeerd met het OIDC-protocol. Meerdere identiteitsproviders kunnen parallel worden geconfigureerd door twee belangrijke configuratiebestanden aan te passen:

- **`dashboard_config.toml`** — bepaalt de inloginterface van de frontend
- **`config.toml`** — configureert de OIDC-verbindingen van de backend

### Ondersteunde providers {: #supported-providers-overview }

De voorbeelden in deze gids gebruiken **Microsoft** en **Google**, maar **elke OIDC-conforme provider** kan volgens dezelfde structuur worden geïntegreerd.

---

## Gidsen per provider {: #provider-guides }

Elke provider heeft dezelfde vier waarden nodig — een client ID, een client secret, een redirect URI en een discovery-URL — maar elke provider zet ze op een andere plek in zijn beheerconsole, en een aantal heeft een providerspecifieke stap die de andere niet hebben. De onderstaande gidsen behandelen die helft van het werk; deze pagina behandelt de digna-helft, die voor alle providers identiek is.

| Provider | Gids | Goed om te weten |
|---|---|---|
| **AD FS** | [SSO instellen met AD FS](adfs_sso_guide.md) | Zelfgehost; de enige provider hier waarbij je zelf de tokenservice beheert |
| **Auth0** | [SSO instellen met Auth0](auth0_sso_guide.md) | De discovery-URL is per tenant, en custom domains veranderen hem |
| **Google Workspace** | [SSO instellen met Google Workspace](google_workspace_sso_guide.md) | Het toestemmingsscherm moet gepubliceerd zijn voordat niet-testgebruikers kunnen inloggen |
| **Keycloak** | [SSO instellen met Keycloak](keycloak_sso_guide.md) | Zelfgehost; de discovery-URL is per realm |
| **Microsoft Entra ID** | [SSO instellen met Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | De tenant-ID staat in de discovery-URL; secrets verlopen |
| **Okta** | [SSO instellen met Okta](okta_sso_guide.md) | De keuze van de authorization server verandert de discovery-URL |
| **OneLogin** | [SSO instellen met OneLogin](onelogin_sso_guide.md) | Het type OIDC-app moet bij het aanmaken worden gekozen en kan niet worden gewijzigd |
| **PingOne** | [SSO instellen met PingOne](pingone_sso_guide.md) | De environment-ID staat in de discovery-URL |

Elke andere OIDC-conforme provider werkt op dezelfde manier — zie [Andere OIDC-providers](#supported-providers).

---

## Configuratiestappen {: #configuration-steps }

Voor de SSO-configuratie moeten twee bestanden worden bijgewerkt. Dit gedeelte legt uit hoe je elk bestand configureert.

### Overzicht van de configuratiebestanden

| Bestand | Locatie | Doel |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Inloginterface van de frontend |
| **config.toml** | `/config.toml` | OIDC-verbindingen van de backend |

Beide bestanden moeten geconfigureerd zijn om SSO correct te laten werken.

---

## Dashboardconfiguratie {: #dashboard-configuration }

### Bestandslocatie

```
dashboard/dashboard_config.toml
```

### Stap 1: OIDC-providers toevoegen

Voeg onder de array `[[login.oidc]]` een item toe voor elke identiteitsprovider die je wilt ondersteunen.

**Voorbeeld met Microsoft en Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Stap 2: Inlogopties configureren

Geef aan of inloggen met een wachtwoord is toegestaan:

```toml
[login]
usePassword = true
```

### Configuratieparameters

#### Sectie `[[login.oidc]]`

| Parameter | Type | Verplicht | Beschrijving |
|---|---|---|---|
| `key` | string | Ja | Unieke identificatie van de OIDC-verbinding (moet overeenkomen met de key in config.toml) |
| `label` | string | Ja | Tekst op de inlogknop (bijv. "Login with Microsoft") |

#### Sectie `[login]`

| Parameter | Type | Standaard | Beschrijving |
|---|---|---|---|
| `usePassword` | boolean | false | Inloggen met wachtwoord toestaan naast SSO |

### usePassword begrijpen

**Als `usePassword = true`:**
- Het inlogscherm toont SSO-knoppen (bijv. "Login with Microsoft")
- Het inlogscherm toont ook velden voor gebruikersnaam en wachtwoord
- Gebruikers kunnen zich met beide methoden authenticeren
- Maakt hybride opstellingen mogelijk waarin sommige gebruikers SSO gebruiken en andere een wachtwoord

**Als `usePassword = false` (of weggelaten):**
- Het inlogscherm toont alleen SSO-knoppen
- Geen velden voor gebruikersnaam/wachtwoord
- Alleen OIDC-authenticatie is beschikbaar

!!! tip "Tip"

    Inloggen met een wachtwoord is alleen mogelijk voor gebruikers die met een wachtwoord zijn aangemaakt via het commando `digna user add` of via het dashboard.

### Volledig voorbeeld

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backendconfiguratie {: #backend-configuration }

### Bestandslocatie

```
/config.toml
```

(Hoofdmap van de digna-installatie)

### Stap 1: OIDC-providersecties toevoegen

Elke provider moet een eigen sectie `[oidc_clients.<key>]` hebben. De key moet overeenkomen met de `key` die in `dashboard_config.toml` is gedefinieerd.

### Microsoft-configuratie

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google-configuratie

```toml
[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Configuratieparameters

| Parameter | Type | Verplicht | Beschrijving | Voorbeeld |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Ja | Client ID van de identiteitsprovider | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Ja | Client secret van de identiteitsprovider | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Ja | Callback-URL na authenticatie | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Ja | OIDC-configuratie-endpoint | `https://login.microsoftonline.com/...` |

!!! warning "Belangrijk"

    Vervang de placeholders (`<client_id>`, `<client_secret>`, `<tenant_id>`) door de echte gegevens uit het ontwikkelaarsportaal van je identiteitsprovider.

### Redirect URI

De redirect URI moet identiek zijn aan die in de configuratie van je identiteitsprovider:

```
http://localhost:5173/oidc/callback
```

Als digna op een ander domein wordt gehost, pas je dit overeenkomstig aan:
- Lokaal: `http://localhost:5173/oidc/callback`
- Productie: `https://digna.yourdomain.com/oidc/callback`

### Volledig voorbeeld

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc_clients.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Inloggen testen {: #testing-login }

Controleer na het afronden van de configuratie of SSO correct werkt.

### Checklist vóór het testen

Zorg vóór het testen dat:

- [ ] `dashboard_config.toml` is bijgewerkt met de OIDC-providers
- [ ] `config.toml` is bijgewerkt met de OIDC-gegevens
- [ ] beide bestanden zijn opgeslagen
- [ ] de gegevens kloppen (client ID, client secret)
- [ ] de redirect URI overeenkomt met de URL van je deployment
- [ ] de applicatie bij de identiteitsprovider is geconfigureerd met de redirect URI

### Teststappen

#### Stap 1: Services herstarten

Herstart de digna-backend en de webserver om de wijzigingen toe te passen.

**Als digna als service op Windows draait:**
```bash
cd C:\path\to\digna
digna windows stop
digna windows start
```

**Als digna als service op Linux of macOS draait:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Als digna handmatig wordt gestart:**
```bash
digna serve --address localhost --port 8082
```

**Herstart ook de webserver** — IIS of Tomcat op Windows, nginx of Apache op Linux en macOS.

#### Stap 2: Dashboard openen

Open het digna-dashboard in je browser:

```
http://localhost:5173
```

(of de URL van je geconfigureerde dashboard)

#### Stap 3: Inlogknoppen controleren

Controleer of er voor elke geconfigureerde provider een inlogknop verschijnt:

- De knop "Login with Microsoft" moet zichtbaar zijn
- De knop "Login with Google" moet zichtbaar zijn
- (Als usePassword = true) Velden voor gebruikersnaam/wachtwoord moeten zichtbaar zijn

Als de knoppen niet verschijnen:
- Controleer of `dashboard_config.toml` is opgeslagen
- Controleer of de dashboardservice is herstart
- Controleer de browserconsole (F12) op fouten

#### Stap 4: SSO-login testen

Klik op een van de SSO-knoppen (bijv. "Login with Microsoft"):

1. Je wordt doorgestuurd naar de inlogpagina van de identiteitsprovider
2. Log in met je zakelijke inloggegevens
3. Je wordt teruggestuurd naar digna
4. Je bent ingelogd bij digna

#### Stap 5: Aanmaken van de gebruiker controleren

Na een geslaagde SSO-login:

- De gebruiker wordt automatisch in digna aangemaakt
- De gebruiker is ingelogd
- Het gebruikersprofiel toont de gegevens van je identiteitsprovider
- Je ziet het digna-dashboard

#### Stap 6: Inloggen met wachtwoord testen (indien ingeschakeld)

Als `usePassword = true`:

1. Log uit bij digna
2. Voer op de inlogpagina een gebruikersnaam en wachtwoord in
3. Je moet kunnen inloggen met je wachtwoordgegevens

---

## Problemen oplossen {: #troubleshooting }

### Inlogknoppen verschijnen niet

**Symptomen:**
- OIDC-inlogknoppen zijn niet zichtbaar op de inlogpagina
- Alleen wachtwoordvelden zichtbaar (als usePassword = true)

**Oorzaken en oplossingen:**
1. Controleer of `dashboard_config.toml` in de map `dashboard/` staat
2. Controleer of de secties `[[login.oidc]]` aanwezig zijn en de syntaxis klopt
3. Herstart de dashboardservice
4. Wis de browsercache (Ctrl+Shift+Delete of Cmd+Shift+Delete)
5. Controleer de browserconsole (F12 → tabblad Console) op fouten

---

### Fout: redirect URI komt niet overeen

**Symptomen:**
- Na een klik op de SSO-knop verschijnt een fout over "redirect_uri mismatch"
- Foutmelding "The redirect URI is not registered"

**Oorzaken en oplossingen:**
1. Controleer of `DIGNA_OIDC_REDIRECT_URI` in `config.toml` klopt
2. Controleer of de redirect URI is geregistreerd in de instellingen van de identiteitsprovider
3. Zorg dat beide exact dezelfde URL gebruiken (inclusief protocol, domein en pad)
4. Controleer de redirect URI op typefouten
5. Als je HTTPS gebruikt, zorg dan dat het certificaat geldig is

---

### Fout: ongeldige clientgegevens

**Symptomen:**
- Foutmelding "Invalid client ID or secret"
- Authenticatie mislukt met een fout over de inloggegevens

**Oorzaken en oplossingen:**
1. Controleer of `DIGNA_OIDC_CLIENT_ID` en `DIGNA_OIDC_CLIENT_SECRET` kloppen
2. Zorg dat er geen extra spaties of speciale tekens in staan
3. Controleer of de gegevens niet verlopen of ingetrokken zijn
4. Herstart de backendservice na het bijwerken van de configuratie
5. Controleer in de console van de identiteitsprovider of de gegevens actief zijn

---

### Inloggen blijft hangen of loopt af op een time-out

**Symptomen:**
- Klikken op de SSO-knop doet niets
- Time-out na enkele seconden
- De browser toont "Failed to connect" of iets vergelijkbaars

**Oorzaken en oplossingen:**
1. Controleer of de digna-backend draait: `digna repo check`
2. Controleer de netwerkverbinding met de identiteitsprovider
3. Controleer of `DIGNA_OIDC_CONFIGURATION_URL` bereikbaar is
4. Controleer of de firewallregels uitgaande HTTPS-verbindingen toestaan
5. Controleer of backend en dashboard elkaar kunnen bereiken

---

### Gebruikers worden niet automatisch aangemaakt

**Symptomen:**
- SSO-login slaagt, maar de gebruiker wordt niet in digna aangemaakt
- Een toegangsfout na de SSO-login

**Oorzaken en oplossingen:**
1. Controleer of de OIDC-configuratie klopt
2. Controleer of de gebruikersrechten zijn ingesteld
3. Bekijk de digna-logs op foutmeldingen
4. Herstart de backendservice
5. Neem contact op met support@digna.ai als het probleem aanhoudt

---

## Ondersteunde providers {: #supported-providers }

### Getest en ondersteund

De volgende OIDC-providers zijn getest en werken aantoonbaar:

| Provider | Configuratie-URL | Installatiegids |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [SSO instellen met AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [SSO instellen met Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [SSO instellen met Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [SSO instellen met Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [SSO instellen met Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [SSO instellen met Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [SSO instellen met OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [SSO instellen met PingOne](pingone_sso_guide.md) |

### Andere OIDC-providers

Elke provider die OpenID Connect ondersteunt, kan worden geïntegreerd. Benodigde gegevens:

- Client ID
- Client secret
- OpenID-configuratie-URL (meestal op `/.well-known/openid-configuration`)
- Ondersteunde scopes (meestal `openid profile email`)

Neem contact op met support@digna.ai als je hulp nodig hebt bij het integreren van een specifieke provider.

---

## Best practices

**WEL:**
- Gebruik HTTPS in productie (geen HTTP)
- Bewaar client secrets veilig (gebruik indien mogelijk omgevingsvariabelen)
- Vernieuw secrets regelmatig
- Test eerst in een niet-productieomgeving
- Documenteer welke providers geconfigureerd zijn
- Houd de inloglogs in de gaten op ongebruikelijke activiteit
- Houd de configuratie van de identiteitsprovider in sync met de digna-configuratie

**NIET:**
- Client secrets in versiebeheer opslaan
- HTTP-redirect-URI's in productie gebruiken
- Meerdere providers met dezelfde key configureren
- Standaard- of testgegevens in productie laten staan
- Configuratiebestanden met secrets openbaar maken
- Ontwikkel- en productiegegevens door elkaar gebruiken

---

## Ondersteuning

Hulp nodig bij de SSO-configuratie?

- **E-mail:** support@digna.ai
- **Documentatie:** https://docs.digna.ai
- **Website:** https://www.digna.ai

---

**Laatst bijgewerkt:** 30 augustus 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
