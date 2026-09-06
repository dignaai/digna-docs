# Ota SSO käyttöön Microsoft Entra ID:llä

Microsoft Entra ID (entinen Azure Active Directory) on täysin OIDC-yhteensopiva palveluntarjoaja, joten digna integroituu siihen standardin discovery-endpointin kautta.

Tämä ohje kattaa **Entra ID -puolen**: sovelluksen rekisteröinnin ja neljän dignan tarvitsemien arvon keräämisen. digna-puoli — `dashboard_config.toml`, testaus ja vianmääritys — on sama kaikille tarjoajille ja on kuvattu [Single Sign-On Overview](overview.md)-sivulla.

---

## Ennen kuin aloitat

| Vaatimus | Huomautuksia |
|---|---|
| **Entra ID -rooli** | Application Administrator, Cloud Application Administrator tai Global Administrator |
| **digna redirect URI** | URL johon käyttäjät palaavat kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Hakemisto, johon käyttäjänne kirjautuvat |

---

## Vaihe 1: Rekisteröi sovellus

1. Kirjaudu sisään [Microsoft Entra admin centeriin](https://entra.microsoft.com)
2. Siirry kohtaan **Identity → Applications → App registrations**
3. Klikkaa **New registration**
4. Määritä:
   - **Name**: `digna` (näkyy käyttäjille suostumusnäytöllä)
   - **Supported account types**: *Accounts in this organizational directory only* yksittäistenanttista asennusta varten
5. Kohdassa **Redirect URI**, valitse alusta **Web** ja syötä dignan callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klikkaa **Register**

!!! warning "Tärkeää"

    Alustan on oltava **Web**, ei *Single-page application*. digna vaihtaa valtuutuskoodin backendissä käyttäen client secretia, mitä SPA-alustatyyppi ei salli.

---

## Vaihe 2: Kerää Client- ja Tenant-ID:t

Sovelluksen **Overview**-sivulla kopioi:

- **Application (client) ID** → muuttuu `DIGNA_OIDC_CLIENT_ID`-arvoksi
- **Directory (tenant) ID** → käytetään discovery-URLissa

---

## Vaihe 3: Luo client secret

1. Siirry kohtaan **Certificates & secrets → Client secrets**
2. Klikkaa **New client secret**
3. Anna kuvaus ja valitse vanhenemisaika
4. Klikkaa **Add**
5. Kopioi **Value**-sarake heti

!!! warning "Kopioi Value, älä Secret ID:tä"

    **Value** näytetään vain kerran, tällä sivulla, eikä sitä voi hakea jälkikäteen. Sen vieressä oleva **Secret ID** näyttää samankaltaiselta mutta ei olekaan salaisuus — sen käyttäminen aiheuttaa `invalid_client`-virheen kirjautumisessa. Jos poistut sivulta ennen kopiointia, poista salaisuus ja luo uusi.

!!! tip "Vinkki"

    Entra ID rajoittaa salaisuuksien eliniän 24 kuukauteen, joten jokaisella SSO-integraatiolla on vanhenemispäivä. Merkitse se paikkaan, josta näet sen — vanhentunut salaisuus katkaisee SSO:n kaikilta käyttäjiltä kerralla ilman varoitusta kirjautumissivulla.

---

## Vaihe 4: Vahvista API-luvat

1. Siirry kohtaan **API permissions**
2. Varmista, että **Microsoft Graph → User.Read** (delegated) on listassa — se lisätään oletuksena

`openid`, `profile` ja `email` scopet, joita digna pyytää, ovat osa OIDC:n standardisettiä eikä niille tarvita erillistä suostumusta. Jos tenantissasi vaaditaan admin-suostumus kaikille sovelluksille, klikkaa **Grant admin consent for <tenant>**.

---

## Vaihe 5: Rakenna discovery-URL

Korvaa **Directory (tenant) ID** vaiheesta 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Käytä v2.0-endpointia"

    `/v2.0/`-segmentti on tärkeä. v1.0-endpoint `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` antaa tokeneita vanhemmassa muodossa eikä palauta standardeja OIDC-claimseja, joita digna odottaa.

Avaa URL selaimessa ennen jatkamista. JSON-dokumentti vahvistaa, että tenant ID on oikein.

---

## Vaihe 6: Konfiguroi digna

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
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Molempien tiedostojen `key`-arvon on vastattava toisiaan — tässä `microsoft`.

---

## Vaihe 7: Testaa

Käynnistä backend ja web-palvelin uudelleen, ja avaa sitten dashboard. Katso täydellinen tarkistuslista [Testing Login](overview.md#testing-login)-sivulta.

---

## Vianmääritys Entra ID:ssä

### AADSTS50011: Redirect URI Mismatch

`DIGNA_OIDC_REDIRECT_URI`-arvo eroaa rekisteröidystä URI:sta vaiheessa 1. Entra ID vertaa koko merkkijonoa, joten loppuviiva, `http` vs `https` tai eri portti kaikki lasketaan virheeksi. Tarkista **Authentication → Web → Redirect URIs**.

### AADSTS7000215: Invalid Client Secret

Joko **Secret ID** kopioitiin **Value**-kentän sijaan tai salaisuus on vanhentunut. Luo uusi secret ja kopioi Value-sarake.

### AADSTS650057: Invalid Resource

Sovellusrekisteröinti on poistettu tai se kuuluu eri tenanttiin kuin discovery-URLissa on. Varmista Directory (tenant) ID Overview-sivulta.

### Käyttäjät kirjautuvat, mutta mitään ei tapahdu

Jos tenantti vaatii admin-suostumusta eikä sitä ole myönnetty, uudelleenohjaus palautuu ilman käyttökelpoista tokenia. Myönnä admin-suostumus **API permissions** -kohdasta.

---

## Katso myös

- [Single Sign-On Overview](overview.md) — konfiguraatioviite, testaus ja yleinen vianmääritys
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)