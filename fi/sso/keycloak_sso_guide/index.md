# SSO:n määrittäminen Keycloakin kanssa

Keycloak on itseisännöity, täysin OIDC-yhteensopiva identiteetin tarjoaja. Koska ajat sitä itse, discovery-URL rakennetaan oman isäntäsi ja realmisi perusteella eikä vendor-domainin mukaan.

Tämä ohje kattaa **Keycloak-puolen**: clientin luomisen ja arvot, jotka digna tarvitsee. digna-puoli — `dashboard_config.toml`, testaus ja vianmääritys — on sama kaikille tarjoajille ja on kuvattu [Yhden kirjautumisen yleiskatsaus](overview.md).

---

## Ennen aloittamista

| Vaatimus | Huomautuksia |
|---|---|
| **Keycloak-versio** | Versio 17 tai uudempi käytetyille URL-poluille — katso huomautus kohdassa 4 |
| **Keycloak-rooli** | `realm-admin` kohderealmissa, tai palvelimen ylläpitäjä |
| **Realm** | Realm, johon dignan käyttäjät kuuluvat — ei välttämättä `master` |
| **digna redirect URI** | URL, johon käyttäjät palaavat kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Valitse realm

1. Avaa Keycloakin admin-konsoli
2. Vaihda ylävasemmasta realm-valikosta siihen realmiin, jossa käyttäjäsi ovat

!!! warning "Älä käytä master-realmia"

    `master`-realm on tarkoitettu Keycloakin hallinnointiin. Sovellusclientit kuuluvat omaan realminsa; dignan sijoittaminen `master`-realmille antaa sen käyttäjille pääsyn Keycloak-hallintakonsoliin.

---

## Vaihe 2: Luo client

1. Siirry kohtaan **Clients** ja klikkaa **Create client**
2. Konfiguroi:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — tästä tulee `DIGNA_OIDC_CLIENT_ID`
3. Klikkaa **Next**
4. **Capability config** -vaiheessa laita **Client authentication** **On**
5. Jätä **Standard flow** käytöksi; muita flow’ita ei tarvita
6. Klikkaa **Next**

!!! warning "Client authentication pitää olla päällä"

    Jos **Client authentication** on pois päältä, Keycloak luo *public* clientin, jolla ei ole lainkaan tunnistetietoja — **Credentials**-välilehteä kohdassa 4 ei tule olemaan. digna tarvitsee confidential-clientin. Tämä asetus voidaan korjata myös luomisen jälkeen.

---

## Vaihe 3: Aseta redirect URI

Login settings -vaiheessa (tai myöhemmin **Settings**-välilehdellä):

1. **Valid redirect URIs**: syötä dignan callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: jätä tyhjäksi, tai aseta `+` peilaamaan redirect-URI:ita
3. Klikkaa **Save**

!!! tip "Vältä jokerimerkkejä"

    Keycloak hyväksyy malleja kuten `https://digna.yourdomain.com/*`. Jokerimerkki sallii minkä tahansa polun kyseisellä isännällä vastaanottaa authorizaatiokoodin, joten suosittelemme käyttämään tarkkaa callback-URL:ia.

---

## Vaihe 4: Hanki client-salaisuus

1. Avaa **Credentials**-välilehti
2. Varmista, että **Client Authenticator** on *Client Id and Secret*
3. Kopioi **Client secret** → tästä tulee `DIGNA_OIDC_CLIENT_SECRET`

Salaisuus säilyy haettavana täällä ja sen voi generoida uudelleen painikkeella **Regenerate**.

---

## Vaihe 5: Rakenna discovery-URL

Korvaa Keycloakin isäntä ja realmin nimi:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Esimerkiksi:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 ja sitä vanhemmat käyttävät /auth-polun osaa"

    Ennen Keycloak 17:ää kaikki endpointit sijaitsivat `/auth`-etuliitteen alla:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Jakelut, jotka asettavat `KC_HTTP_RELATIVE_PATH=/auth`, säilyttävät vanhan rakenne myös nykyisissä versioissa. Jos URL ilman `/auth` palauttaa 404:n, kokeile sitä kanssa.

Avaa URL selaimessa ennen jatkamista. JSON-dokumentti vahvistaa, että isäntä ja realm ovat oikein.

---

## Vaihe 6: Konfiguroi digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Kirjaudu Keycloakilla"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Molemmissa tiedostoissa oleva `key` täytyy täsmätä — tässä `keycloak`. Huomaa, että sen ei tarvitse olla sama kuin Keycloakin **Client ID**, vaikka saman pitäminen helpottaa seuraamista.

---

## Vaihe 7: Testaa

Käynnistä backend ja web-palvelin uudelleen, ja avaa dashboard. Katso [Kirjautumisen testaus](overview.md#testing-login) täydellinen tarkistuslista.

---

## Keycloakin vianmääritys

### Invalid parameter: redirect_uri

Callback-URL ei sisälly **Valid redirect URIs** -kenttään. Keycloak kirjaa vastaanotetun URI:n server-logiin, mikä on nopein tapa nähdä tarkka erimielisyys.

### Credentials-välilehti puuttuu

Client on public. Laita **Client authentication** päälle kohdassa **Settings → Capability config**.

### 404 discovery-URL:lla

Joko realmin nimi on väärin, tai asennus käyttää `/auth`-etuliitettä. Tarkista realm-lista admin-konsolista ja kokeile molempia URL-muotoja.

### unauthorized_client tai invalid_client

**Standard flow** on pois päältä kohdassa **Capability config**, tai salaisuus on regeneroitu Keycloakissa ilman, että `config.toml` on päivitetty.

### Sertifikaattivirheet backendistä

Itseisännöity Keycloak yksityisellä tai itseallekirjoitetulla sertifikaatilla epäonnistuu dignan ulospäin suuntautuvassa HTTPS-kutsussa discovery-URL:iin. Asenna allekirjoittavan CA:n varmenne koneen trust storeen, jolla digna-backend ajetaan.

---

## Katso myös

- [Yhden kirjautumisen yleiskatsaus](overview.md) — konfiguraatioviite, testaus ja yleinen vianmääritys
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)