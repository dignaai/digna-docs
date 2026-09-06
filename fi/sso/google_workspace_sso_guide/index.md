# Ota SSO käyttöön Google Workspacen kanssa

Googlen identiteettialusta on OIDC-yhteensopiva ja käyttää yhtä, hyvin tunnettua discovery-URL:ia kaikille asiakkaille, joten ainoat organisaatiokohtaiset arvot ovat client ID ja secret.

Tämä ohje kattaa **Google-puolen**: OAuth-asiakkaan luomisen ja dignan tarvitsemien arvojen keräämisen. digna-puoli — `dashboard_config.toml`, testaus ja vianmääritys — on sama kaikille palveluntarjoajille ja kuvataan [Single Sign-On - Yleiskatsaus](overview.md).

---

## Ennen aloittamista

| Vaatimus | Huomautukset |
|---|---|
| **Google Cloud -projekti** | Mikä tahansa projekti samassa organisaatiossa kuin Workspace-domainisi |
| **Rooli** | Editor tai Owner projektissa |
| **digna-uudelleenohjaus-URI** | URL johon käyttäjät palaavat kirjautumisen jälkeen, esim. `https://digna.yourdomain.com/oidc/callback` |

---

## Vaihe 1: Määritä OAuth-suostumusnäyttö

Google ei myönnä tunnistetietoja ennen kuin suostumusnäyttö on olemassa.

1. Avaa [Google Cloud -konsoli](https://console.cloud.google.com) ja valitse projektisi
2. Siirry kohtaan **APIs & Services → OAuth consent screen**
3. Valitse käyttäjätyyppi:
   - **Internal** — vain tilit Workspace-domainissasi voivat kirjautua. Suositeltava.
   - **External** — mikä tahansa Google-tili voi yrittää kirjautua.
4. Täytä sovelluksen nimi, käyttäjätuki-sähköposti ja kehittäjän yhteyssähköposti
5. Kohdassa **Scopes** lisää `openid`, `.../auth/userinfo.email` ja `.../auth/userinfo.profile`
6. Tallenna

!!! warning "Ulkoiset sovellukset on julkaistava"

    **External**-tyyppinen suostumusnäyttö aloittaa *Testing*-tilassa, jossa vain nimenomaisesti testikäyttäjälistaan lisätyt tilit voivat suorittaa kirjautumisen loppuun. Muut käyttäjät näkevät viestin "digna has not completed the Google verification process". Vaihda sovellus **In production** -tilaan kohdasta **Publishing status**, tai käytä **Internal**-tyyppiä — sillä ei ole tätä rajoitusta ja se on oikea valinta vain Workspacea varten otettaessa käyttöön.

---

## Vaihe 2: Luo OAuth-asiakas

1. Siirry kohtaan **APIs & Services → Credentials**
2. Napsauta **Create Credentials → OAuth client ID**
3. Aseta **Application type** kohtaan **Web application**
4. Anna nimi, esim. `digna`
5. Kohtaan **Authorized redirect URIs** napsauta **Add URI** ja syötä:

```
https://digna.yourdomain.com/oidc/callback
```

6. Napsauta **Create**

!!! note "Valtuutettuja JavaScript-origin-ei tarvita"

    digna vaihtaa valtuutuskoodin backendissä, ei selaimessa, joten kenttä **Authorized JavaScript origins** voidaan jättää tyhjäksi. Ainoastaan uudelleenohjaus-URI on merkityksellinen.

---

## Vaihe 3: Kerää tunnistetiedot

Luo-muodon jälkeen avautuva dialogi näyttää:

- **Client ID** — päättyy `.apps.googleusercontent.com` → tästä tulee `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → tästä tulee `DIGNA_OIDC_CLIENT_SECRET`

Molemmat ovat myöhemmin haettavissa tunnistetietojen yksityiskohtasivulta, toisin kuin useimmilla muilla palveluntarjoajilla.

---

## Vaihe 4: Discovery-URL

Google käyttää yhtä discovery-URL:ia kaikille asiakkaillle — mitään arvojen korvaamista ei tarvita:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## Vaihe 5: Konfiguroi digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Molempien tiedostojen `key`-arvon on täsmättävä — tässä `google`.

---

## Vaihe 6: Testaa

Käynnistä backend ja web-palvelin uudelleen, ja avaa sen jälkeen dashboard. Katso [Kirjautumisen testaus](overview.md#testing-login) täydellinen tarkistuslista.

---

## Vianmääritys Google Workspacessa

### Error 400: redirect_uri_mismatch

DIGNA_OIDC_REDIRECT_URI:ssa oleva URI ei ole **Authorized redirect URIs** -listalla, tai se poikkeaa loppuviivan tai protokollan (http/https) osalta. Googlen virhesivu näyttää vastaanotetun URI:n — vertaa sitä merkki merkiltä rekisteröityyn URI:hin.

### This App Is Blocked / Has Not Completed Verification

Suostumusnäyttö on **External** ja edelleen *Testing*-tilassa. Julkaise se tai vaihda sovellus **Internal**-tyyppiin.

### Access Blocked: Authorization Error

Kirjautumista yrittävä tili on Workspace-domainisi ulkopuolella, kun suostumusnäyttö on **Internal**. Tämä on odotettu käytös — Internal-sovellukset hyväksyvät vain organisaation tilejä.

### Muutosten leviämiseen kuluu useita minuutteja

Google levittää tunnistetieto- ja suostumusnäyttömuutoksia asynkronisesti. Äskettäin lisäyksiin rekisteröity uudelleenohjaus-URI voi ottaa muutaman minuutin ennen kuin se tulee voimaan; jos muutos vaikuttaa ohitetulta, odota hetki ja yritä uudelleen ennen kuin alat tutkia muita syitä.

---

## Katso myös

- [Single Sign-On - Yleiskatsaus](overview.md) — konfiguraatioreferenssi, testaus ja yleinen vianmääritys
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)