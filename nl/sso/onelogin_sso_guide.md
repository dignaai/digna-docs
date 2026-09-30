# SSO instellen met OneLogin

OneLogin is OIDC-conform. Het onderscheidende kenmerk is dat het connectortype bij het aanmaken van de app uit een catalogus wordt gekozen en daarna niet meer kan worden gewijzigd.

Deze gids behandelt de **OneLogin-kant**: het aanmaken van de applicatie en het verzamelen van de waarden die digna nodig heeft. De digna-kant — `dashboard_config.toml`, testen en oplossen van problemen — is voor elke provider hetzelfde en wordt beschreven in het [Overzicht Single Sign-On](overview.md).

---

## Voordat je begint

| Vereiste | Opmerkingen |
|---|---|
| **OneLogin-rol** | Accounteigenaar of een beheerder die applicaties mag toevoegen |
| **Subdomein** | bijv. `yourcompany.onelogin.com` |
| **digna redirect URI** | De URL waar gebruikers na het inloggen naar terugkeren, bijv. `https://digna.yourdomain.com/oidc/callback` |

---

## Stap 1: Maak de OIDC-applicatie aan

1. Log in op het OneLogin Admin-portaal
2. Ga naar **Applications → Applications**
3. Klik **Add App**
4. Zoek naar `OpenId Connect` en selecteer de connector **OpenId Connect (OIDC)**
5. Stel de **Display Name** in op `digna`
6. Klik **Save**

!!! warning "Het connectortype ligt vast bij het aanmaken"

    OneLogin heeft aparte catalogusitems voor SAML en OIDC, en een applicatie kan niet van het ene naar het andere worden omgezet. Als je per ongeluk een SAML-connector kiest, verwijder de app dan en voeg hem opnieuw toe — er is geen instelling om van protocol te wisselen.

---

## Stap 2: Configureer de redirect URI

1. Open het tabblad **Configuration**
2. Voer in **Redirect URI's** je digna callback-URL in:

```
https://digna.yourdomain.com/oidc/callback
```

3. Stel optioneel **Post Logout Redirect URIs** in op de URL van je dashboard
4. Klik **Save**

!!! note "Eén URI per regel"

    Anders dan providers die een door komma's gescheiden lijst verwachten, neemt het veld **Redirect URI's** van OneLogin één URI per regel.

---

## Stap 3: Stel het applicatietype en de authenticatiemethode in

1. Open het tabblad **SSO**
2. Controleer of **Application Type** op *Web* staat
3. Stel **Token Endpoint → Authentication Method** in op *POST* (`client_secret_post`) of *Basic* (`client_secret_basic`)

!!! warning "Kies niet None"

    Als je de authenticatiemethode op *None* zet, wordt de applicatie een public client zonder secret, en wordt de code-uitwisseling in de digna-backend geweigerd. Zowel POST als Basic werkt.

---

## Stap 4: Verzamel de gegevens

Nog steeds op het tabblad **SSO**:

- **Client ID** → wordt `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → wordt `DIGNA_OIDC_CLIENT_SECRET` (klik **Show client secret**)

De pagina toont ook de **Issuer URL**, die de discovery-URL in de volgende stap bevestigt.

---

## Stap 5: Wijs gebruikers toe

1. Open het tabblad **Access**
2. Voeg de rollen of groepen toe waarvan de leden digna mogen gebruiken
3. Klik **Save**

!!! note "Niet-toegewezen gebruikers worden na het inloggen geweigerd"

    Zoals bij de meeste providers authenticeert OneLogin eerst de gebruiker en controleert daarna pas de rechten. Een niet-toegewezen gebruiker logt succesvol in en wordt vervolgens geweigerd, wat eruitziet als een digna-fout in plaats van een beslissing van het toegangsbeheer.

---

## Stap 6: Bouw de discovery-URL

Vul je OneLogin-subdomein in:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Bijvoorbeeld:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "De /2 is de API-versie"

    De huidige OIDC-implementatie van OneLogin staat onder `/oidc/2/`. Oudere documentatie toont `/oidc/` zonder versie, wat verwijst naar de uitgefaseerde eerste versie. Controleer bij twijfel de **Issuer URL** op het tabblad SSO — de discovery-URL is de issuer plus `/.well-known/openid-configuration`.

---

## Stap 7: Configureer digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

De `key` moet in beide bestanden overeenkomen — hier `onelogin`.

---

## Stap 8: Test

Herstart de backend en de webserver, en open daarna het dashboard. Zie [Inloggen testen](overview.md#testing-login) voor de volledige checklist.

---

## Problemen oplossen met OneLogin

### redirect_uri did not match

De callback-URL ontbreekt in **Configuration → Redirect URI's**, of de items zijn gescheiden door komma's in plaats van nieuwe regels.

### invalid_client bij de tokenstap

**Token Endpoint → Authentication Method** staat op *None*, of het client secret in `config.toml` is verouderd. Toon het secret op het tabblad **SSO** en vergelijk.

### De app verschijnt niet voor gebruikers

Er is geen rol of groep toegang verleend op het tabblad **Access**.

### 404 op de discovery-URL

Het subdomein is onjuist, of de URL mist `/oidc/2/`. Vergelijk met de **Issuer URL** op het tabblad SSO.

---

## Zie ook

- [Overzicht Single Sign-On](overview.md) — configuratiereferentie, testen en algemene probleemoplossing
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)