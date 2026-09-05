# Single Sign-On -integraatio-opas

---

## Sisällysluettelo

1. [Johdanto ja yleiskatsaus](#introduction-and-overview)
2. [Konfigurointivaiheet](#configuration-steps)
3. [Dashboardin konfigurointi](#dashboard-configuration)
4. [Backendin konfigurointi](#backend-configuration)
5. [Kirjautumisen testaus](#testing-login)
6. [Vianmääritys](#troubleshooting)
7. [Tuetut tarjoajat](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Tässä oppaassa annetaan vaiheittaiset ohjeet Single Sign-On (SSO) -integraation määrittämiseksi digna-alustalle käyttäen **OpenID Connect (OIDC)** -protokollaa.

### Mikä on SSO?

Single Sign-On mahdollistaa käyttäjien turvallisen kirjautumisen dignaan yritystunnuksillaan ulkoisten identiteetin tarjoajien kautta. Käyttäjät voivat autentikoitua yrityksen tunnuksilla sen sijaan, että hallinnoisivat erillisiä digna-salasanoja.

### Miten se toimii

SSO dignassa toteutetaan OIDC-protokollaa käyttäen. Useita identiteetin tarjoajia voidaan konfiguroida rinnakkain muokkaamalla kahta keskeistä konfigurointitiedostoa:

- **`dashboard_config.toml`** — Ohjaa frontendin kirjautumisliittymää
- **`config.toml`** — Määrittää backendin OIDC-yhteydet

### Tuetut tarjoajat {: #supported-providers-overview }

Tämän oppaan esimerkeissä käytetään **Microsoftia** ja **Googlea**, mutta **mitä tahansa OIDC-yhteensopivaa tarjoajaa** voidaan integroida saman rakenteen mukaisesti.

Yleisiä OIDC-tarjoajia ovat:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Muut OIDC-yhteensopivat identiteetin tarjoajat

---

## Configuration Steps {: #configuration-steps }

SSO:n konfigurointi vaatii päivitykset kahteen tiedostoon. Tässä osiossa selitetään, miten kumpikin tiedosto konfiguroidaan.

### Yleiskatsaus konfigurointitiedostoista

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontendin kirjautumisliittymä |
| **config.toml** | `/config.toml` | Backendin OIDC-yhteydet |

Molemmat tiedostot on konfiguroitava, jotta SSO toimii oikein.

---

## Dashboard Configuration {: #dashboard-configuration }

### Tiedoston sijainti

```
dashboard/dashboard_config.toml
```

### Vaihe 1: Lisää OIDC-tarjoajat

Lisää merkinnät `[[login.oidc]]`-taulukkoon jokaiselle identiteetin tarjoajalle, jota haluat tukea.

**Esimerkki Microsoftin ja Googlen kanssa:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Kirjaudu Microsoftilla"

[[login.oidc]]
key = "google"
label = "Kirjaudu Googlella"
```

### Vaihe 2: Määritä kirjautumisvaihtoehdot

Määritä, sallitaanko salasanapohjainen kirjautuminen:

```toml
[login]
usePassword = true
```

### Konfigurointiparametrit

#### `[[login.oidc]]` -osio

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Yksilöllinen tunniste OIDC-yhteydelle (täytyy vastata avainta config.toml:ssa) |
| `label` | string | Yes | Kirjautumispainikkeessa näytettävä teksti (esim. "Kirjaudu Microsoftilla") |

#### `[login]` -osio

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Sallii salasanapohjaisen kirjautumisen SSO:n lisäksi |

### Mikä on usePassword

**Jos `usePassword = true`:**
- Kirjautumisnäytössä näytetään SSO-painikkeet (esim. "Kirjaudu Microsoftilla")
- Kirjautumisnäytössä näytetään myös käyttäjätunnus- ja salasana-kentät
- Käyttäjät voivat autentikoitua joko SSO:lla tai salasanalla
- Mahdollistaa hybridiasetukset, joissa osa käyttäjistä käyttää SSO:ta ja osa salasanoja

**Jos `usePassword = false` (tai puuttuu):**
- Kirjautumisnäytössä näkyvät vain SSO-painikkeet
- Ei käyttäjätunnus/salasana-kenttiä
- Vain OIDC-autentikointi on käytettävissä

!!! tip "Vinkki"

    Salasanapohjainen kirjautuminen on käytettävissä vain käyttäjille, jotka on luotu salasanoilla `digna user add` -komennolla tai dashboardin kautta.

### Täydellinen esimerkki

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Kirjaudu Microsoftilla"

[[login.oidc]]
key = "google"
label = "Kirjaudu Googlella"

[[login.oidc]]
key = "okta"
label = "Kirjaudu Oktalla"
```

---

## Backend Configuration {: #backend-configuration }

### Tiedoston sijainti

```
/config.toml
```

(Juuri digna-asennuskansiossa)

### Vaihe 1: Lisää OIDC-tarjoajaosiot

Jokaiselle tarjoajalle tulee oma `[oidc.<key>]` -osio. Avain tulee vastata `dashboard_config.toml`-tiedostossa määriteltyä `key`-arvoa.

### Microsoftin konfigurointi

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Googlen konfigurointi

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurointiparametrit

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID identiteetin tarjoajalta | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret identiteetin tarjoajalta | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Callback-URL autentikoinnin jälkeen | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC-konfiguraatio-päätepiste | `https://login.microsoftonline.com/...` |

!!! warning "Tärkeää"

    Korvaa paikkamerkkien arvot (`<client_id>`, `<client_secret>`, `<tenant_id>`) todellisilla tunnuksilla identiteetin tarjoajan kehittäjäportaalista.

### Redirect URI

Redirect URI:n on oltava sama identiteetin tarjoajan konfiguraatiossa:

```
http://localhost:5173/oidc/callback
```

Jos digna on isännöity eri domainissa, päivitä osoite vastaavasti:
- Paikallinen: `http://localhost:5173/oidc/callback`
- Tuotanto: `https://digna.yourdomain.com/oidc/callback`

### Täydellinen esimerkki

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Testing Login {: #testing-login }

Kun konfigurointi on valmis, varmista että SSO toimii oikein.

### Ennen testausta tarkistuslista

Varmista ennen testausta:

- [ ] `dashboard_config.toml` on päivitetty OIDC-tarjoajilla
- [ ] `config.toml` on päivitetty OIDC-tunnuksilla
- [ ] Molemmat tiedostot on tallennettu
- [ ] Tunnukset ovat oikein (client ID, client secret)
- [ ] Redirect URI vastaa käyttöönotettua URL:ia
- [ ] Identiteetin tarjoajan sovellus on konfiguroitu redirect URI:lla

### Testausvaiheet

#### Vaihe 1: Käynnistä palvelut uudelleen

Käynnistä digna-backend ja web-palvelin uudelleen, jotta muutokset tulevat voimaan.

**Jos ajetaan Windows-palveluna:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Jos ajetaan manuaalisesti:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Jos käytössä on IIS tai Tomcat:**
Käynnistä web-palvelin uudelleen.

#### Vaihe 2: Avaa dashboard

Avaa digna-dashboard selaimessa:

```
http://localhost:5173
```

( tai konfiguroitu dashboard-URL )

#### Vaihe 3: Varmista kirjautumispainikkeet

Tarkista, että konfiguroiduille tarjoajille näkyy kirjautumispainikkeet:

- Näkyy "Kirjaudu Microsoftilla" -painike
- Näkyy "Kirjaudu Googlella" -painike
- (Jos usePassword = true) Näkyy käyttäjätunnus/salasana-kentät

Jos painikkeita ei näy:
- Tarkista, että `dashboard_config.toml` on tallennettu
- Tarkista, että dashboard-palvelu on käynnistetty uudelleen
- Tarkista selaimen konsoli (F12) virheilmoituksia varten

#### Vaihe 4: Testaa SSO-kirjautuminen

Klikkaa yhtä SSO-painikkeista (esim. "Kirjaudu Microsoftilla"):

1. Sinut pitäisi ohjata identiteetin tarjoajan kirjautumissivulle
2. Kirjaudu sisään yritystunnuksillasi
3. Sinut pitäisi ohjata takaisin dignaan
4. Sinut pitäisi kirjata sisään dignaan

#### Vaihe 5: Varmista käyttäjän luonti

Onnistuneen SSO-kirjautumisen jälkeen:

- Käyttäjä luodaan automaattisesti dignaan
- Käyttäjä kirjautuu sisään
- Käyttäjäprofiilissa näkyvät identiteetin tarjoajan tiedot
- Näet digna-dashboardin

#### Vaihe 6: Testaa salasana-kirjautuminen (jos käytössä)

Jos `usePassword = true`:

1. Kirjaudu ulos dignasta
2. Kirjautumisnäkymässä syötä käyttäjätunnus ja salasana
3. Pitäisi pystyä kirjautumaan myös salasanalla

---

## Troubleshooting {: #troubleshooting }

### Kirjautumispainikkeet eivät näy

**Oireet:**
- OIDC-kirjautumispainikkeet eivät näy kirjautumissivulla
- Näkyvissä vain salasana-kentät (jos usePassword = true)

**Syyt & ratkaisut:**
1. Tarkista, että `dashboard_config.toml` on `dashboard/`-hakemistossa
2. Varmista, että `[[login.oidc]]` -osiot ovat paikallaan ja syntaksi on oikein
3. Käynnistä dashboard-palvelu uudelleen
4. Tyhjennä selaimen välimuisti (Ctrl+Shift+Delete tai Cmd+Shift+Delete)
5. Tarkista selaimen konsoli (F12 → Console) virheilmoitusten varalta

---

### Redirect URI -virhe (mismatch)

**Oireet:**
- Klikkaamisen jälkeen virheilmoitus "redirect_uri mismatch"
- "The redirect URI is not registered" -virhe

**Syyt & ratkaisut:**
1. Varmista, että `DIGNA_OIDC_REDIRECT_URI` `config.toml`-tiedostossa on oikein
2. Varmista, että sama redirect URI on rekisteröity identiteetin tarjoajan asetuksissa
3. Varmista, että molemmat käyttävät täsmälleen samaa URL:ia (protokolli, domain, polku)
4. Tarkista kirjoitusvirheet redirect URI:ssa
5. Jos käytät HTTPS:ää, varmista, että sertifikaatti on voimassa

---

### Virhe: Virheelliset client-tunnukset

**Oireet:**
- "Invalid client ID or secret" -virhe
- Autentikointi epäonnistuu tunnistusvirheellä

**Syyt & ratkaisut:**
1. Varmista `DIGNA_OIDC_CLIENT_ID` ja `DIGNA_OIDC_CLIENT_SECRET` ovat oikein
2. Varmista, ettei arvoissa ole ylimääräisiä välilyöntejä tai erikoismerkkejä
3. Tarkista, ettei tunnuksille ole asetettu vanhenemista tai revokaatioita
4. Käynnistä backend-palvelu uudelleen konfiguroinnin jälkeen
5. Tarkista identiteetin tarjoajan konsolista, että tunnukset ovat aktiivisia

---

### Kirjautuminen jumittuu tai aikakatkaistuu

**Oireet:**
- SSO-painikkeen klikkaaminen ei reagoi
- Aikakatkaisu muutaman sekunnin jälkeen
- Selain näyttää "Failed to connect" tai vastaavaa

**Syyt & ratkaisut:**
1. Varmista, että digna-backend on käynnissä: `digna repo check`
2. Tarkista verkkoyhteys identiteetin tarjoajaan
3. Varmista, että `DIGNA_OIDC_CONFIGURATION_URL` on saavutettavissa
4. Tarkista palomuurisäännöt, jotka sallivat ulospäin suuntautuvat HTTPS-yhteydet
5. Varmista, että backend ja dashboard pääsevät toisiinsa käsiksi

---

### Käyttäjiä ei luoda automaattisesti

**Oireet:**
- SSO-kirjautuminen onnistuu, mutta käyttäjää ei luoda dignaan
- SSO-kirjautumisen jälkeen saat oikeusvirheen

**Syyt & ratkaisut:**
1. Varmista OIDC-konfiguraation oikeellisuus
2. Tarkista käyttäjäoikeudet ja -määritykset
3. Tarkista digna-lokit virheilmoitusten varalta
4. Käynnistä backend-palvelu uudelleen
5. Ota yhteyttä support@digna.ai, jos ongelma jatkuu

---

## Supported Providers {: #supported-providers }

### Testatut ja tuetut

Seuraavat OIDC-tarjoajat on testattu ja niiden pitäisi toimia:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Muut OIDC-tarjoajat

Mikä tahansa OpenID Connectia tukeva tarjoaja voidaan integroida. Tarvittavat tiedot:

- Client ID
- Client secret
- OpenID-konfiguraatio-URL (yleensä osoitteessa `/.well-known/openid-configuration`)
- Tuetut scopet (tyypillisesti `openid profile email`)

Ota yhteyttä support@digna.ai, jos tarvitset apua tietyn tarjoajan integroinnissa.

---

## Best Practices

**TEKE:**
- Käytä HTTPS:ää tuotannossa (ei HTTP:tä)
- Säilytä client-secret turvallisesti (käytä ympäristömuuttujia jos mahdollista)
- Kierrätä salaisuuksia säännöllisesti
- Testaa ensin ei-tuotantoympäristössä
- Dokumentoi mitkä tarjoajat on konfiguroitu
- Seuraa kirjautumislokeja poikkeavuuksien varalta
- Pidä identiteetin tarjoajan konfiguraatio synkronoituna digna-konfiguraation kanssa

**ÄLÄ:**
- Tallenna client-secretoja versionhallintaan
- Käytä HTTP-redirect URI:ta tuotannossa
- Konfiguroi useita tarjoajia samalla key-arvolla
- Jätä oletus/testitunnukset tuotantoon
- Paljasta konfiguraatiotiedostoja, jotka sisältävät salaisuuksia
- Sekoita kehitys- ja tuotantotunnuksia

---

## Support

Tarvitsetko apua SSO-konfiguroinnissa?

- **Sähköposti:** support@digna.ai
- **Dokumentaatio:** https://docs.digna.ai
- **Verkkosivusto:** https://www.digna.ai

---

**Päivitetty:** 30. elokuu 2026  
**Julkaisu:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**