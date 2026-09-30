# SSO instellen met Microsoft Entra ID

Microsoft Entra ID (voorheen Azure Active Directory) is een volledig OIDC-conforme provider, dus digna integreert ermee via het standaard discovery-endpoint.

Deze gids behandelt de **Entra ID-kant**: het registreren van de applicatie en het verzamelen van de vier waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **Entra ID-rol** | Application Administrator, Cloud Application Administrator of Global Administrator |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | De directory waarin je gebruikers inloggen |

---

## Stap 1: Registreer de applicatie

1. Log in op het [Microsoft Entra admin center](https://entra.microsoft.com)
2. Ga naar **Identity → Applications → App registrations**
3. Klik **New registration**
4. Configureer:
   - **Name**: `digna` (wordt aan gebruikers getoond op het toestemmingsscherm)
   - **Supported account types**: *Accounts in this organizational directory only* voor een single-tenant deployment
5. Selecteer onder **Redirect URI** het platform **Web** en voer je digna callback-URL in:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klik **Register**

!!! warning "Belangrijk"

    Het platform moet **Web** zijn, niet *Single-page application*. digna wisselt de autorisatiecode uit vanuit de backend met een client secret, en dat staat het platformtype SPA niet toe.

---

## Stap 2: Verzamel de client- en tenant-ID

Kopieer op de pagina **Overview** van de applicatie:

- **Application (client) ID** → wordt `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → gaat in de discovery-URL

---

## Stap 3: Maak een client secret aan

1. Ga naar **Certificates & secrets → Client secrets**
2. Klik **New client secret**
3. Voer een beschrijving in en kies een vervaltermijn
4. Klik **Add**
5. Kopieer direct de kolom **Value**

!!! warning "Kopieer de Value, niet de Secret ID"

    De **Value** wordt maar één keer getoond, op deze pagina, en kan daarna niet meer worden opgehaald. De **Secret ID** ernaast lijkt erop, maar is niet het secret — als je die gebruikt, krijg je bij het inloggen de fout `invalid_client`. Als je de pagina verlaat voordat je hebt gekopieerd, verwijder het secret dan en maak een nieuw aan.

!!! tip "Tip"

    Entra ID beperkt de levensduur van een secret tot 24 maanden, dus elke SSO-integratie heeft een vervaldatum. Noteer die op een plek waar je hem ziet — een verlopen secret legt SSO voor alle gebruikers tegelijk plat, zonder waarschuwing op de inlogpagina.

---

## Stap 4: Controleer de API-rechten

1. Ga naar **API permissions**
2. Controleer of **Microsoft Graph → User.Read** (delegated) aanwezig is — dit wordt standaard toegevoegd

De scopes `openid`, `profile` en `email` die digna aanvraagt, horen bij de standaard OIDC-set en hebben geen aparte toekenning nodig. Als je tenant voor alle applicaties admin consent vereist, klik dan op **Grant admin consent for &lt;tenant&gt;**.

---

## Stap 5: Bouw de discovery-URL

Vul de **Directory (tenant) ID** uit Stap 2 in:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Gebruik het v2.0-endpoint"

    Het segment `/v2.0/` is van belang. Het v1.0-endpoint op `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` geeft tokens uit in een ouder formaat en retourneert niet de standaard OIDC-claims die digna verwacht.

Open de URL in een browser voordat je verdergaat. Een JSON-document bevestigt dat de tenant-ID klopt.

---

## Stap 6: Configureer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

De `key` moet in beide bestanden overeenkomen — hier `microsoft`.

---

## Stap 7: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met Entra ID

### AADSTS50011: Redirect URI Mismatch

De URI in `DIGNA_OIDC_REDIRECT_URI` wijkt af van de URI die in Stap 1 is geregistreerd. Entra ID vergelijkt de volledige string, dus een afsluitende slash, `http` tegenover `https` of een andere poort gelden allemaal als afwijking. Controleer **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Ofwel is de **Secret ID** gekopieerd in plaats van de **Value**, ofwel is het secret verlopen. Maak een nieuw secret aan en kopieer de kolom Value.

### AADSTS650057: Invalid Resource

De app-registratie is verwijderd of hoort bij een andere tenant dan die in de discovery-URL. Controleer de Directory (tenant) ID op de pagina Overview.

### Gebruikers loggen in, maar er gebeurt niets

Als de tenant admin consent vereist en die niet is gegeven, keert de redirect terug zonder bruikbaar token. Geef admin consent onder **API permissions**.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)