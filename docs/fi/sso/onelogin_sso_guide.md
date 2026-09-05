---
title: OneLogin SSO – Single Sign-On -integraatio | digna-dokumentaatio
description: Määritä Single Sign-On dignalle OneLoginin avulla käyttäen OpenID Connectiä — OIDC-sovelluksen luominen, uudelleenohjaus-URI:t, asiakastiedot, token-endpointin autentikointi ja vastaava digna-konfiguraatio.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, token-endpointin autentikointi, yritystason autentikointi
---

# SSO:n määrittäminen OneLoginilla

OneLogin on OIDC-yhteensopiva. Sen erottuva piirre on, että liitostyyppi valitaan luettelosta sovellusta luotaessa eikä sitä voi muuttaa jälkikäteen.

Tämä opas käsittelee **OneLoginin puolta**: sovelluksen luomista ja arvojen keräämistä, joita digna tarvitsee. dignan puoli — `dashboard_config.toml`, testaaminen ja vianmääritys — on sama kaikille tarjoajille ja on kuvattu [Single Sign-On Overview](overview.md):ssä.

---

## Ennen kuin aloitat

| Vaatimus | Huomioita |
|---|---|
| **OneLogin-rooli** | Tilin omistaja tai järjestelmänvalvoja, jolla on oikeus lisätä sovelluksia |
| **Aliverkkotunnus** | esim. `yourcompany.onelogin.com` |
| **digna:n uudelleenohjaus-URI** | URL, johon käyttäjä palaa kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Luo OIDC-sovellus

1. Kirjaudu OneLoginin Admin-portaaliin
2. Siirry kohtaan **Applications → Applications**
3. Klikkaa **Add App**
4. Etsi `OpenId Connect` ja valitse **OpenId Connect (OIDC)** -liitin
5. Aseta **Display Name** arvoksi `digna`
6. Klikkaa **Save**

!!! warning "Liitostyyppi on kiinteä luomishetkellä"

    OneLoginilla on erilliset luettelokohteet SAML:ille ja OIDC:lle, eikä sovellusta voi muuntaa yhdestä toiseen. Jos valitset vahingossa SAML-liittimen, poista sovellus ja lisää se uudelleen — asetusta protokollan vaihtamiseksi ei ole.

---

## Vaihe 2: Määritä uudelleenohjaus-URI

1. Avaa **Configuration**-välilehti
2. kohtaan **Redirect URI's** syötä digna-kutsutusosoitteesi:

```
https://digna.yourdomain.com/oidc/callback
```

3. Halutessasi aseta **Post Logout Redirect URIs** kojetaulusi URL-osoitteeksi
4. Klikkaa **Save**

!!! note "Yksi URI per rivi"

    Toisin kuin tarjoajat, jotka odottavat pilkulla eroteltua listaa, OneLoginin **Redirect URI's** -kenttä ottaa yhden URI:n per rivi.

---

## Vaihe 3: Aseta sovellustyyppi ja autentikointimenetelmä

1. Avaa **SSO**-välilehti
2. Varmista, että **Application Type** on *Web*
3. Aseta **Token Endpoint → Authentication Method** arvoksi *POST* (`client_secret_post`) tai *Basic* (`client_secret_basic`)

!!! warning "Älä valitse None-arvoa"

    Authentication Methodin asettaminen arvoksi *None* tekee sovelluksesta julkisen clientin ilman salaisuutta, ja dignan backendin koodinvaihto hylätään. Sekä POST että Basic toimivat.

---

## Vaihe 4: Kerää tunnistetiedot

Edelleen **SSO**-välilehdellä:

- **Client ID** → muuttuu `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → muuttuu `DIGNA_OIDC_CLIENT_SECRET` (klikkaa **Show client secret**)

Sivulla näkyy myös **Issuer URL**, joka vahvistaa seuraavassa vaiheessa käytettävän discovery-URLin.

---

## Vaihe 5: Määrittele käyttäjät

1. Avaa **Access**-välilehti
2. Lisää roolit tai ryhmät, joiden jäsenet voivat käyttää dignaa
3. Klikkaa **Save**

!!! note "Määrittelemättömät käyttäjät hylätään kirjautumisen jälkeen"

    Kuten useimmilla tarjoajilla, OneLogin todentaa käyttäjän ensin ja tarkistaa käyttöoikeudet vasta sen jälkeen. Määrittelemätön käyttäjä kirjautuu onnistuneesti sisään ja hylätään sitten, mikä näyttää dignan virheeltä eikä käyttöoikeuspäätökseltä.

---

## Vaihe 6: Kokoa discovery-URL

Korvaa OneLogin-aliverkkotunnuksesi:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Esimerkiksi:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "Path /2 on API-versioni"

    OneLoginin nykyinen OIDC-toteutus sijaitsee polussa `/oidc/2/`. Vanhemmissa dokumenteissa näkyy `/oidc/` ilman versiota, joka osoittaa käytöstä poistetun ensimmäisen version. Tarkista **Issuer URL** SSO-välilehdeltä, jos epäilet — discovery-URL on issuer plus `/.well-known/openid-configuration`.

---

## Vaihe 7: Määritä digna

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
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Molemmissa tiedostoissa oleva `key` täytyy täsmätä — tässä tapauksessa `onelogin`.

---

## Vaihe 8: Testaa

Käynnistä backend ja web-palvelin uudelleen ja avaa sitten kojelauta. Katso [Testing Login](overview.md#testing-login) täydellinen tarkistuslista.

---

## OneLoginin vianmääritys

### redirect_uri did not match

Kutsutus-URL puuttuu **Configuration → Redirect URI's** -kohdasta, tai merkinnät on erotettu pilkuilla rivinvaihtojen sijaan.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** on asetettu arvoksi *None*, tai `config.toml`-tiedoston client secret on vanhentunut. Näytä secret **SSO**-välilehdellä ja vertaa.

### Sovellus ei näy käyttäjille

Yksikään rooli tai ryhmä ei ole saanut käyttöoikeutta **Access**-välilehdellä.

### 404 discovery-URLissa

Aliverkkotunnus on väärä, tai URL puuttuu `/oidc/2/`. Vertaa **Issuer URL** -arvoon SSO-välilehdellä.

---

## Katso myös

- [Single Sign-On Overview](overview.md) — konfiguraatio, testaus ja yleinen vianmääritys
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)