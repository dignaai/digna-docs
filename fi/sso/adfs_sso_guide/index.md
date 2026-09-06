# SSO:n käyttöönotto AD FS:llä

Active Directory Federation Services on paikallinen vaihtoehto: omat palvelimesi myöntävät tokenit, ja discovery URL on oma isäntänimesi. AD FS tukee OpenID Connectiä **Windows Server 2016**:sta lähtien.

Tämä ohje kattaa **AD FS -puolen**: sovellusryhmän luomisen ja ne arvot, jotka digna tarvitsee. digna-puoli — `dashboard_config.toml`, testaus ja vianmääritys — on sama kaikille tarjoajille ja on kuvattu [Single Sign-On -yleiskatsauksessa](overview.md).

---

## Ennen kuin aloitat

| Vaatimus | Huomautuksia |
|---|---|
| **AD FS -versio** | Windows Server 2016 tai uudempi — vanhemmissa versioissa ei ole OIDC-tukea |
| **Pääsy** | Paikallinen järjestelmänvalvoja AD FS -palvelimella |
| **Federation-palvelun nimi** | esim. `adfs.yourdomain.com` |
| **digna:n redirect URI** | URL, johon käyttäjät palaavat kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Luo sovellusryhmä

1. AD FS -palvelimella avaa **AD FS Management**
2. Klikkaa hiiren oikealla **Application Groups** ja valitse **Add Application Group**
3. Anna nimeksi `digna`
4. Valitse **Standalone applications** — tai **Client-Server applications** riippuen versiostasi — ja valitse **Server application accessing a web API**
5. Klikkaa **Next**

---

## Vaihe 2: Määritä palvelinsovellus

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS generoi GUIDin. Kopioi se — tästä tulee `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: syötä digna callback -URL ja klikkaa **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Klikkaa **Next**

!!! warning "Klikkaa Add, älä vain Nextiä"

    Redirect URI -kentällä on oma **Add**-painike. Jos kirjoitat URI:n ja klikkaat **Next** ilman **Add**-painiketta, se hylätään eikä ohjattu ikkuna anna varoitusta. Varmista, että URI näkyy kentän alla olevassa listassa ennen kuin jatkat.

---

## Vaihe 3: Generoi jaettu salaisuus

1. Ruksaa **Generate a shared secret**
2. Kopioi generoitu salaisuus → tästä tulee `DIGNA_OIDC_CLIENT_SECRET`
3. Klikkaa **Next**

!!! warning "Salaisuus näytetään vain kerran"

    AD FS näyttää jaetun salaisuuden vain tällä ohjatun toiminnon sivulla eikä sitä voi näyttää uudelleen. Jos menetät sen, nollaa se myöhemmin sovellusryhmän asetuksista.

---

## Vaihe 4: Määritä Web API

1. **Identifier**: syötä sama client identifier kuin Vaiheessa 2 ja klikkaa **Add**
2. Klikkaa **Next**
3. Valitse **Access Control Policy** — *Permit everyone* on helpoin lähtökohta; rajoita tuotannossa esimerkiksi ryhmään
4. Klikkaa **Next**

---

## Vaihe 5: Myönnä sallitut scopet

Configure Application Permissions -vaiheessa valitse:

- `openid`
- `profile`
- `email`

Klikkaa sitten **Next** ja viimeistele ohjattu toiminto.

!!! warning "openid ei ole valittuna oletuksena"

    Joissain AD FS -versioissa valittuna on vain `user_impersonation`. Ilman `openid`-scopea token-endpoint palauttaa OAuth-access-tokenin ID-tokenin sijaan, eikä digna pysty tunnistamaan käyttäjää.

---

## Vaihe 6: Vahvista discovery-endpoint

Korvaa federation-palvelun nimi:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Esimerkiksi:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Avaa tämä selaimessa. JSON-dokumentti vahvistaa, että OIDC on käytössä ja isäntänimi on oikein.

!!! note "Backendin on luotettava sertifikaattiin"

    Sisäinen varmenneviranomainen on AD FS:ssä yleinen. Kone, joka ajaa digna-backendia, tekee itse ulospäin suuntautuvan HTTPS-kutsun tähän URL:iin, joten varmentajan CA:n on oltava kyseisen koneen luottamusvarastossa — ei vain niiden käyttäjien selaimissa, jotka kirjautuvat sisään.

---

## Vaihe 7: Konfiguroi digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Kirjaudu Active Directoryllä"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Molempien tiedostojen `key`-arvon on vastattava toisiaan — tässä `adfs`.

---

## Vaihe 8: Testaa

Käynnistä backend ja web-palvelin uudelleen, ja avaa sitten dashboard. Katso [Testing Login](overview.md#testing-login) saadaksesi täydellisen tarkistuslistan.

---

## AD FS:n vianmääritys

### MSIS9611: The Client Is Not Allowed to Access the Resource

Web API -identifier Vaiheessa 4 ei vastaa client identifieria, tai Vaiheen 5 scopet eivät ole myönnettyjä. Molempia voi muokata sovellusryhmän ominaisuuksista.

### MSIS9602: Invalid redirect_uri

URI syötettiin mutta sitä ei lisätty **Add**-painikkeella, tai se poikkeaa `DIGNA_OIDC_REDIRECT_URI`-arvosta. Tarkista **Application Groups → digna → digna backend → Properties**.

### ID-tokenia ei palauteta

Sovellusluvan scopesta puuttuu `openid`.

### Backend ei pääse discovery-URL:iin

Tai DNS ei ratkaise federation-palvelun nimeä backend-koneessa, tai AD FS:n sertifikaattia ei luoteta siellä. Testaa komennolla `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` suoraan digna-palvelimelta.

### Tarkistettavat tapahtumat

AD FS -palvelin kirjaa virheistä Event Vieweriin kohtaan **Applications and Services Logs → AD FS → Admin**, yleensä siellä on selainvirhettä tarkempi syy.

---

## Katso myös

- [Single Sign-On -yleiskatsaus](overview.md) — konfiguraatioviite, testaus ja yleinen vianmääritys
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)