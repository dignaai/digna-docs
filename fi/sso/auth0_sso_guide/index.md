# Ota SSO käyttöön Auth0:n kanssa

Auth0 on OIDC-yhteensopiva ja tarjoaa discovery-pisteen jokaista tenantia varten. Pääkysymys on saada tenantin domain oikein, sillä se näkyy discovery-URL:ssa ja muuttuu, jos otat käyttöön mukautetun domainin.

Tämä opas käsittelee **Auth0-puolta**: sovelluksen luomista ja arvojen keräämistä, joita digna tarvitsee. digna-puoli — `dashboard_config.toml`, testaus ja vianmääritys — on sama kaikille tarjoajille ja on kuvattu [Single Sign-On Overview](overview.md) -sivuilla.

---

## Ennen kuin aloitat

| Vaatimus | Huomautukset |
|---|---|
| **Auth0 role** | Tenantin ylläpitäjä |
| **Tenant domain** | esim. `yourcompany.eu.auth0.com` — alueen segmentti on olennaista |
| **digna redirect URI** | URL johon käyttäjät palaavat kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Luo sovellus

1. Kirjaudu sisään [Auth0-hallintapaneeliin](https://manage.auth0.com)
2. Siirry kohtaan **Applications → Applications**
3. Klikkaa **Create Application**
4. Nimeä se `digna` ja valitse **Regular Web Applications**
5. Klikkaa **Create**

!!! warning "Valitse Regular Web Applications"

    *Single Page Application* ja *Native* luovat julkisia clientteja ilman salaisuutta. digna suorittaa koodinvaihdon omasta backendistaan ja tarvitsee salaisen clientin (confidential client), joten oikea tyyppi on **Regular Web Applications**. Toisin kuin jotkut tarjoajat, Auth0 antaa muuttaa tyyppiä myöhemmin kohdassa **Settings → Application Type**.

---

## Vaihe 2: Lisää callback-URL

Sovelluksen **Settings**-välilehdellä:

1. Etsi **Allowed Callback URLs**
2. Syötä dignan callback-URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Aseta halutessasi **Allowed Logout URLs** dashboard-osoitteeksesi
4. Selaa alas ja klikkaa **Save Changes**

!!! note "Erottele pilkuilla, älä rivinvaihdoilla"

    Auth0 hyväksyy useita callback-URL:eja tässä kentässä, erotettuna pilkuilla. Rivinvaihdoilla eroteltu lista luetaan yhdeksi virheelliseksi URL:ksi, eikä se vastaa mihinkään.

---

## Vaihe 3: Kerää tunnistetiedot

Yhä **Settings**-välilehdellä, **Basic Information** -paneelissa:

- **Domain** → menee discovery-URL:iin
- **Client ID** → muuttuu `DIGNA_OIDC_CLIENT_ID`:ksi
- **Client Secret** → muuttuu `DIGNA_OIDC_CLIENT_SECRET`:ksi (klikkaa näyttääksesi)

---

## Vaihe 4: Vahvista Grant Type

1. Siirry kohtaan **Settings → Advanced Settings → Grant Types**
2. Varmista, että **Authorization Code** on valittuna

Se on oletuksena käytössä Regular Web Applications -tyyppisissä sovelluksissa. Jos se on poistettu valinnasta, dignan kirjautuminen epäonnistuu virheellä `unauthorized_client`.

---

## Vaihe 5: Rakenna discovery-URL

Korvaa Step 3:n **Domain**:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Esimerkiksi:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Mukautetut domainit muuttavat issuer-arvoa"

    Jos tenantillasi on mukautettu domain kuten `login.yourcompany.com`, käytä sitä discovery-URL:ssa. Kahden eri domainin — canonical domain discovery-URL:ssa ja mukautettu domain selaimessa — sekoittaminen aiheuttaa issuer-epäsopivuuden, ja token hylätään muuten onnistuneen kirjautumisen jälkeen.

---

## Vaihe 6: Konfiguroi digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Molemmissa tiedostoissa oleva `key`-arvon pitää täsmätä — tässä tapauksessa `auth0`.

---

## Vaihe 7: Testaa

Käynnistä backend ja web-palvelin uudelleen, avaa sitten dashboard. Katso täydellinen tarkistuslista [Kirjautumisen testaus](overview.md#testing-login) -kohdasta.

---

## Auth0:n vianmääritys

### Callback-URL-ristiriita

Auth0:n virhesivu näyttää sille annetun URL:n. Lisää se **Allowed Callback URLs** -kenttään ja varmista, että merkinnät on eroteltu pilkuilla.

### unauthorized_client

**Authorization Code** ei ole valittuna kohdassa **Advanced Settings → Grant Types**, tai sovellustyyppi ei ole Regular Web Applications.

### Pääsy estetty onnistuneen kirjautumisen jälkeen

Tenantissa oleva Rule, Action tai Post-Login-triggeri voi hylätä käyttäjän. Tarkista **Actions → Flows → Login** ja tenantin lokit kohdasta **Monitoring → Logs**, joista selviää tarkka syy.

### Issuer-epäsopivuus

Discovery-URL ja se domain, johon selaimella ohjattiin, eroavat — yleensä canonical tenant -domain vs. mukautettu domain. Käytä samaa domainia johdonmukaisesti.

---

## Katso myös

- [Single Sign-On Overview](overview.md) — konfiguraatioviite, testaus ja yleinen vianmääritys
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)