# SSO instellen met Keycloak

Keycloak is een zelfgehoste, volledig OIDC-conforme identiteitsprovider. Omdat je het zelf draait, is de discovery-URL opgebouwd uit je eigen hostnaam en realm in plaats van een vendor-domein.

Deze gids behandelt de **Keycloak-kant**: het aanmaken van de client en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Single Sign-On Overview](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **Keycloak-versie** | 17 of later voor de hier gebruikte URL-paden — zie de opmerking in Stap 4 |
| **Keycloak-rol** | `realm-admin` op de doel-realm, of een serverbeheerder |
| **Realm** | De realm waartoe je digna-gebruikers behoren, niet per se `master` |
| **digna redirect URI** | De URL waar gebruikers na inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Selecteer de Realm

1. Open de Keycloak beheerconsole
2. Gebruik de realm-selector linksboven om te schakelen naar de realm waarin je gebruikers zitten

!!! warning "Gebruik de master Realm niet"

    De `master` realm is bedoeld voor het beheren van Keycloak zelf. Applicatieclients horen in een aparte realm; digna in `master` plaatsen geeft zijn gebruikers toegang tot de Keycloak-beheerconsole.

---

## Stap 2: Maak de Client aan

1. Ga naar **Clients** en klik **Create client**
2. Configureer:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — dit wordt `DIGNA_OIDC_CLIENT_ID`
3. Klik **Next**
4. Op de stap **Capability config**, zet **Client authentication** **On**
5. Laat **Standard flow** ingeschakeld; de andere flows zijn niet nodig
6. Klik **Next**

!!! warning "Client Authentication moet Aan staan"

    Als **Client authentication** uit staat maakt Keycloak een *public* client aan, die helemaal geen credentials heeft — de **Credentials** tab in Stap 4 zal dan niet bestaan. digna heeft een confidential client nodig. Deze schakel kun je achteraf aanpassen als je het verkeerd doet.

---

## Stap 3: Stel de Redirect URI in

Op de stap **Login settings** (of later op het tabblad **Settings**):

1. **Valid redirect URIs**: voer je digna callback-URL in:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: leeg laten, of instellen op `+` om de redirect URIs te spiegelen
3. Klik **Save**

!!! tip "Vermijd wildcardtekens"

    Keycloak accepteert patronen zoals `https://digna.yourdomain.com/*`. Een wildcard geeft elk pad op die host toestemming om een authorisatiecode te ontvangen, dus geef de voorkeur aan de exacte callback-URL.

---

## Stap 4: Verzamel het Client Secret

1. Open het tabblad **Credentials**
2. Bevestig dat **Client Authenticator** *Client Id and Secret* is
3. Kopieer het **Client secret** → wordt `DIGNA_OIDC_CLIENT_SECRET`

Het secret blijft hier opvraagbaar en kan worden vernieuwd met **Regenerate**.

---

## Stap 5: Bouw de Discovery-URL

Vervang je Keycloak-host en realm-naam:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Bijvoorbeeld:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 en eerder gebruiken /auth"

    Voor Keycloak 17 bevonden alle endpoints zich onder een `/auth`-prefix:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distributies die `KC_HTTP_RELATIVE_PATH=/auth` instellen behouden ook op huidige versies de oude indeling. Als de URL zonder `/auth` een 404 geeft, probeer dan de variant met `/auth`.

Open de URL in een browser voordat je verdergaat. Een JSON-document bevestigt dat host en realm kloppen.

---

## Stap 6: Configureer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Inloggen met Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<het in Stap 4 gekopieerde client secret>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

De `key` in beide bestanden moet overeenkomen — `keycloak` hier. Let op dat deze niet per se gelijk hoeft te zijn aan de Keycloak **Client ID**, hoewel ze hetzelfde houden eenvoudiger is.

---

## Stap 7: Test

Herstart de backend en de webserver, en open dan het dashboard. Zie [Testing Login](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met Keycloak

### Invalid parameter: redirect_uri

De callback-URL wordt niet gedekt door **Valid redirect URIs**. Keycloak logt de ontvangen URI in het serverlog, wat de snelste manier is om de exacte mismatch te zien.

### Het Credentials-tabblad ontbreekt

De client is public. Zet **Client authentication** aan onder **Settings → Capability config**.

### 404 op de Discovery-URL

Ofwel is de realm-naam onjuist, of de deployment gebruikt het `/auth`-prefix. Controleer de lijst met realms in de beheerconsole en probeer beide URL-vormen.

### unauthorized_client of invalid_client

**Standard flow** is uitgeschakeld onder **Capability config**, of het secret is in Keycloak vernieuwd zonder `config.toml` bij te werken.

### Certificaatafwijzingen vanuit de backend

Een zelfgehoste Keycloak achter een privé- of self-signed certificaat faalt bij digna's uitgaande HTTPS-aanroep naar de discovery-URL. Installeer de uitgevende CA in de truststore van de machine die de digna-backend draait.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)