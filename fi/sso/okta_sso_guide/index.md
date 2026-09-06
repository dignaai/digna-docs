# SSO:n määrittäminen Oktan kanssa

Okta noudattaa OIDC-standardia, mutta yksi yksityiskohta hämää useimpia ensimmäisen kerran integroivia: Okta-organisaatio tarjoaa useamman kuin yhden authorization serverin, ja jokaisella on oma discovery-URL.

Tämä ohje kattaa **Oktan puolen**: sovellusin­tegraation luomisen ja arvot, jotka digna tarvitsee. dignan puoli — `dashboard_config.toml`, testaus ja vianmääritys — on sama kaikille tarjoajille ja on kuvattu [Single Sign-On Overview](overview.md) -sivulla.

---

## Ennen aloittamista

| Requirement | Notes |
|---|---|
| **Okta role** | Super Administrator, or an admin role permitted to create app integrations |
| **Okta domain** | e.g. `yourcompany.okta.com`, or a custom domain if configured |
| **digna redirect URI** | The URL users return to after login, e.g. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Luo sovellusin­tegraatio

1. Kirjaudu sisään Okta Admin Consoleen
2. Siirry kohtaan **Applications → Applications**
3. Klikkaa **Create App Integration**
4. Valitse:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Klikkaa **Next**

!!! warning "Sovellustyyppiä ei voi muuttaa"

    Jos valitset *Single-Page Application*n *Web Applicationin* sijaan, luot julkisen clientin ilman secret:iä, ja dignan backendin koodivaihto epäonnistuu virheellä `invalid_client`. Tyyppi lukittuu luomishetkellä — väärä valinta tarkoittaa sovelluksen poistamista ja uudelleenaloittamista.

---

## Vaihe 2: Konfiguroi integraatio

1. **App integration name**: `digna`
2. **Grant type**: jätä valittuna *Authorization Code*
3. **Sign-in redirect URIs**: syötä digna callback -URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: valinnainen
5. Kohdassa **Assignments** valitse, kuka saa käyttää integraatiota — tietty ryhmä on turvallisempi kuin *Allow everyone in your organization to access*
6. Klikkaa **Save**

!!! note "Määrittely (Assignment) on pakollinen"

    Okta todentaa käyttäjän ja tarkistaa sitten, onko hän määritelty sovellukseen. Määrittelemätön käyttäjä pääsee Okta-kirjautumissivulle, kirjautuu onnistuneesti sisään, mutta hylätään uudelleenohjauksessa takaisin. Jos kirjautuminen toimii sinulle mutta ei kollegoille, tarkista ensin sovelluksen määritykset (Assignments).

---

## Vaihe 3: Kerää tunnistetiedot

Sovelluksen **General**-välilehdellä, kohdassa **Client Credentials**:

- **Client ID** → muuttuu ympäristömuuttujaksi `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → muuttuu ympäristömuuttujaksi `DIGNA_OIDC_CLIENT_SECRET` (klikkaa silmäikonia paljastaaksesi)

---

## Vaihe 4: Valitse authorization server

Tämä vaihe määrää discovery-URL:in. Siirry kohtaan **Security → API** nähdäksesi organisaatiosi authorization serverit.

**Org authorization server** — antaa tokenit koko Okta-organisaatiolle:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — mukaan lukien Okta:n luoma `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Sisäänrakennetulle palvelimelle `<auth_server_id>` on kirjaimellisesti `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Kumpaa käytän?"

    Käytä **org**-authorization serveria, ellei organisaatiosi käytä jo vakiintunutta custom-serveriä API-käytännöissä. Okta Developer -tilit käyttävät oletuksena `default`-palvelinta; monissa yritysorganisaatioissa se on poistettu käytöstä. Avaa molemmat URL:it selaimessa — se, joka palauttaa JSON:ia virheen sijaan, on käytettävissäsi.

---

## Vaihe 5: Konfiguroi digna

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
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

`key` molemmissa tiedostoissa pitää täsmätä — tässä se on `okta`.

---

## Vaihe 6: Testaa

Käynnistä backend ja web-palvelin uudelleen, ja avaa dashboard. Katso täydellinen tarkistuslista kohdasta [Testing Login](overview.md#testing-login).

---

## Okta-vianmääritys

### Uudelleenohjaus-URI:tä ei ole rekisteröity

Okta ilmoittaa virheilmoituksessa ongelmallisen URI:n. Vertaa sitä kohtaan **General → Sign-in redirect URIs**; Okta vertailee koko merkkijonoa mukaan lukien mahdollinen perään tuleva kauttaviiva.

### Käyttäjä ei ole määritelty client-sovellukseen

Tiliä ei ole lisätty sovelluksen assignment-listalle. Lisää käyttäjä tai hänen ryhmänsä kohdassa **Assignments**.

### 400 Bad Request: Invalid Authorization Server

Discovery-URL:issa käytetty `<auth_server_id>` ei ole olemassa; yleisin syy on että `default` on poistettu organisaatiosta. Tarkista **Security → API** nähdäksesi käytettävissä olevat palvelimet.

### invalid_client token-vaiheessa

Integraatio on luotu Single-Page Application -tyyppisenä eikä sillä ole client secret:iä. Luo integraatio uudelleen valiten Web Application.

---

## Katso myös

- [Single Sign-On Overview](overview.md) — konfiguraatio, testaus ja yleinen vianmääritys
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)