# SSO instellen met PingOne

PingOne is OIDC-conform. Twee waarden vragen extra aandacht: de **environment-ID**, die in elke endpoint-URL staat, en het **regionale domein**, dat verschilt tussen Noord-Amerikaanse, Europese, Canadese, Aziatisch-Pacifische en Australische tenants.

Deze gids behandelt de **PingOne-kant**: het aanmaken van de applicatie en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **PingOne-rol** | Environment Admin of Identity Data Admin op de doelomgeving |
| **Omgeving** | De PingOne-omgeving waartoe je digna-gebruikers behoren |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Maak de applicatie aan

1. Log in op de PingOne-beheerconsole en selecteer je omgeving
2. Ga naar **Applications → Applications**
3. Klik op de knop **+**
4. Voer `digna` in als **Application Name**
5. Selecteer **OIDC Web App**
6. Klik **Save**

!!! warning "Kies OIDC Web App, niet Single-Page App"

    *Single-Page App* en *Native App* maken public clients aan die geen secret kunnen bewaren. digna wisselt de autorisatiecode uit vanuit zijn backend en heeft het confidential type **OIDC Web App** nodig.

---

## Stap 2: Configureer de redirect URI

1. Open het tabblad **Configuration** van de applicatie
2. Klik op het potloodpictogram om te bewerken
3. Controleer of **Response Type** op *Code* staat en **Grant Type** op *Authorization Code*
4. Voer onder **Redirect URIs** je digna callback-URL in:

```
https://digna.yourdomain.com/oidc/callback
```

5. Stel **Token Endpoint Authentication Method** in op *Client Secret Post* of *Client Secret Basic*
6. Klik **Save**

---

## Stap 3: Schakel de applicatie in

Zet in de rij of het detailpaneel van de applicatie de schakelaar op **enabled**.

!!! warning "Nieuwe applicaties starten uitgeschakeld"

    PingOne maakt applicaties aan in uitgeschakelde toestand. Een uitgeschakelde applicatie geeft bij de autorisatiestap een fout die de schakelaar niet noemt, dus het loont om dit te controleren voordat je iets anders gaat debuggen.

---

## Stap 4: Ken de scopes toe

1. Open het tabblad **Resources**
2. Controleer of `openid` is toegekend, en voeg `profile` en `email` toe uit de resource **OpenID Connect**
3. Klik **Save**

---

## Stap 5: Wijs gebruikers toe

1. Open het tabblad **Access**
2. Voeg de population of groepen toe waarvan de leden digna mogen gebruiken
3. Klik **Save**

---

## Stap 6: Verzamel de gegevens en de environment-ID

Klap op het tabblad **Configuration** het onderdeel **General** uit:

- **Client ID** → wordt `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → wordt `DIGNA_OIDC_CLIENT_SECRET` (klik op het oogpictogram)
- **Environment ID** → gaat in de discovery-URL

Hetzelfde tabblad toont ook het kant-en-klare **OIDC Discovery Endpoint**, dat je direct kunt kopiëren in plaats van het zelf samen te stellen.

---

## Stap 7: Bouw de discovery-URL

Vul de environment-ID en het domein voor je regio in:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Regio | Domein |
|---|---|
| Noord-Amerika | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Azië-Pacific | `auth.pingone.asia` |
| Australië | `auth.pingone.com.au` |

Voor een Europese omgeving:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopieer hem in plaats van hem te typen"

    Het regionale domein is veruit de meest gemaakte fout bij een PingOne-integratie, en een verkeerde regio geeft een 404 in plaats van een behulpzame melding. Gebruik de waarde **OIDC Discovery Endpoint** uit Stap 6.

---

## Stap 8: Configureer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

De `key` moet in beide bestanden overeenkomen — hier `pingone`.

---

## Stap 9: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met PingOne

### 404 op de discovery-URL

Het regionale domein of de environment-ID is onjuist. Vergelijk met het **OIDC Discovery Endpoint** op het tabblad Configuration van de applicatie.

### NOT_FOUND of applicatie uitgeschakeld

De schakelaar van de applicatie uit Stap 3 staat nog uit.

### Redirect URI komt niet overeen

PingOne vergelijkt de volledige string. Controleer **Configuration → Redirect URIs** op een afsluitende slash of een verschil in schema.

### Inloggen slaagt, maar er komt geen e-mailclaim bij digna aan

De scopes `email` en `profile` zijn niet toegekend op het tabblad **Resources**.

### De gebruiker ziet de applicatie niet

Er is geen population of groep toegang verleend op het tabblad **Access**.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)