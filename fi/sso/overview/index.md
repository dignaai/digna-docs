# Single Sign-On Overview

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Provider Guides](#provider-guides)
3. [Configuration Steps](#configuration-steps)
4. [Dashboard Configuration](#dashboard-configuration)
5. [Backend Configuration](#backend-configuration)
6. [Testing Login](#testing-login)
7. [Troubleshooting](#troubleshooting)
8. [Supported Providers](#supported-providers)

---

## Johdanto ja yleiskatsaus {: #introduction-and-overview }

Tässä oppaassa on vaiheittaiset ohjeet Single Sign-Onin (SSO) integroimiseksi digna-alustaan käyttämällä **OpenID Connect (OIDC)** -protokollaa.

### Mikä on SSO?

Yhden kirjautumisen (SSO) avulla käyttäjät voivat kirjautua dignaan turvallisesti yrityksen tunnuksilla ulkoisten identiteetin tarjoajien kautta. Käyttäjät voivat todentaa itsensä yritystunnuksilla sen sijaan, että ylläpitäisivät erillistä digna-salasanaa.

### Miten se toimii

SSO dignassa toteutetaan OIDC-protokollalla. Useita identiteetin tarjoajia voidaan määrittää rinnakkain muokkaamalla kahta keskeistä konfiguraatiotiedostoa:

- **`dashboard_config.toml`** — Ohjaa käyttöliittymän kirjautumisnäkymää
- **`config.toml`** — Määrittää backendin OIDC-yhteydet

### Tuetut palveluntarjoajat {: #supported-providers-overview }

Tämän oppaan esimerkeissä käytetään **Microsoftia** ja **Googlea**, mutta **mikä tahansa OIDC-yhteensopiva tarjoaja** voidaan integroida samalla rakenteella.

---

## Palveluntarjoajien ohjeet {: #provider-guides }

Jokainen palveluntarjoaja tarvitsee samat neljä arvoa — client ID:n, client secretin, redirect URI:n ja discovery URLin — mutta kukin löytää ne eri paikasta hallintakonsolissaan, ja useilla on oma palveluntarjoajakohtainen vaiheensa, jota muilla ei ole. Alla olevat ohjeet käsittelevät tätä osaa; tämä sivu kattaa dignan puolen, joka on kaikille sama.

| Provider | Guide | Worth knowing |
|---|---|---|
| **AD FS** | [Aseta SSO AD FS:llä](adfs_sso_guide.md) | Itseisännöity; ainoa tässä listassa, jossa hallitset token-palvelinta |
| **Auth0** | [Aseta SSO Auth0:lla](auth0_sso_guide.md) | Discovery-URL on tenant-kohtainen, ja mukautetut domainit muuttavat sitä |
| **Google Workspace** | [Aseta SSO Google Workspacelle](google_workspace_sso_guide.md) | Suostumusnäyttö on julkaistava ennen kuin ei-testikäyttäjät voivat kirjautua |
| **Keycloak** | [Aseta SSO Keycloakilla](keycloak_sso_guide.md) | Itseisännöity; discovery-URL on realm-kohtainen |
| **Microsoft Entra ID** | [Aseta SSO Microsoft Entra ID:llä](microsoft_entra_id_sso_guide.md) | Tenant ID näkyy discovery-URLissa; salaisuudet vanhenevat |
| **Okta** | [Aseta SSO Oktalla](okta_sso_guide.md) | Autorisointipalvelimen valinta muuttaa discovery-URLia |
| **OneLogin** | [Aseta SSO OneLoginilla](onelogin_sso_guide.md) | OIDC-sovellustyyppi pitää valita luomisvaiheessa eikä sitä voi muuttaa |
| **PingOne** | [Aseta SSO PingOnella](pingone_sso_guide.md) | Environment ID näkyy discovery-URLissa |

Mikä tahansa muu OIDC-yhteensopiva tarjoaja toimii samalla tavalla — katso [Other OIDC Providers](#supported-providers).

---

## Määritysaskeleet {: #configuration-steps }

SSO-määritys vaatii päivityksiä kahteen tiedostoon. Tässä osiossa selitetään, miten kumpikin määritetään.

### Yleiskatsaus konfiguraatiotiedostoihin

| Tiedosto | Sijainti | Tarkoitus |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Kojelaudan kirjautumisliittymä |
| **config.toml** | `/config.toml` | Backendin OIDC-yhteydet |

Molemmat tiedostot on määritettävä, jotta SSO toimii oikein.

---

## Kojelaudan määritys {: #dashboard-configuration }

### Tiedoston sijainti

```
dashboard/dashboard_config.toml
```

### Vaihe 1: Lisää OIDC-palveluntarjoajat

Lisää merkinnät `[[login.oidc]]`-taulukkoon jokaista identiteetin tarjoajaa varten, jota haluat tukea.

**Esimerkki Microsoftilla ja Googlella:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Vaihe 2: Määritä kirjautumisvaihtoehdot

Määritä, sallitaanko salasanaan perustuva kirjautuminen:

```toml
[login]
usePassword = true
```

### Konfiguraatioparametrit

#### `[[login.oidc]]`-osio

| Parametri | Tyyppi | Pakollinen | Kuvaus |
|---|---|---|---|
| `key` | string | Kyllä | Yksilöivä tunniste OIDC-yhteydelle (täytyy vastata config.toml:n key-arvoa) |
| `label` | string | Kyllä | Teksti, joka näytetään kirjautumispainikkeessa (esim. "Login with Microsoft") |

#### `[login]`-osio

| Parametri | Tyyppi | Oletus | Kuvaus |
|---|---|---|---|
| `usePassword` | boolean | false | Sallii salasanaan perustuvan kirjautumisen SSO:n lisäksi |

### usePasswordin ymmärtäminen

**Jos `usePassword = true`:**
- Kirjautumisnäytössä näkyy SSO-painikkeet (esim. "Login with Microsoft")
- Näytössä näkyvät myös käyttäjätunnus- ja salasanakentät
- Käyttäjät voivat todentaa itsensä kumpaa tahansa menetelmää käyttämällä
- Mahdollistaa hybridiasetukset, joissa osa käyttäjistä käyttää SSO:ta ja osa salasanoja

**Jos `usePassword = false` (tai arvo jätetty pois):**
- Kirjautumisnäytössä näkyy vain SSO-painikkeet
- Ei käyttäjätunnus-/salasanakenttiä
- Vain OIDC-todennus on käytettävissä

!!! tip "Vinkki"

    Salasanaan perustuva kirjautuminen on saatavilla vain käyttäjille, jotka on luotu salasanoilla `digna user add` -komennolla tai kojelaudan kautta.

### Täydellinen esimerkki

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend-määritys {: #backend-configuration }

### Tiedoston sijainti

```
/config.toml
```

(Juuri digna-asennushakemistossa)

### Vaihe 1: Lisää OIDC-palveluntarjoajaosiot

Jokaisella tarjoajalla on oltava oma `[oidc.<key>]`-osionsa. Key-arvon täytyy vastata `dashboard_config.toml`-tiedostossa määriteltyä `key`-arvoa.

### Microsoftin määritys

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Googlen määritys

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfiguraatioparametrit

| Parametri | Tyyppi | Pakollinen | Kuvaus | Esimerkki |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Kyllä | Client ID identiteetin tarjoajalta | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Kyllä | Client secret identiteetin tarjoajalta | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Kyllä | Callback-URL todennuksen jälkeen | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Kyllä | OIDC-konfiguraatioendpiste | `https://login.microsoftonline.com/...` |

!!! warning "Tärkeää"

    Korvaa paikkamerkkien arvot (`<client_id>`, `<client_secret>`, `<tenant_id>`) todellisilla tunnuksilla identiteetin tarjoajan kehittäjäportaalista.

### Redirect URI

Redirect URI:n on oltava sama kuin identiteetin tarjoajan konfiguraatiossa:

```
http://localhost:5173/oidc/callback
```

Jos digna on isännöity eri domainissa, päivitä vastaavasti:
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

## Kirjautumisen testaus {: #testing-login }

Kun määritykset on tehty, varmista että SSO toimii oikein.

### Ennen testausta — tarkistuslista

Varmista ennen testausta:

- [ ] `dashboard_config.toml` on päivitetty OIDC-palveluntarjoajilla
- [ ] `config.toml` on päivitetty OIDC-tunnuksilla
- [ ] Molemmat tiedostot on tallennettu
- [ ] Tunnukset ovat oikeat (client ID, client secret)
- [ ] Redirect URI vastaa käyttöönoton URL:ia
- [ ] Identiteetin tarjoajan sovellus on konfiguroitu redirect URI:lla

### Testausaskeleet

#### Vaihe 1: Käynnistä palvelut uudelleen

Käynnistä dignan backend ja web-palvelin uudelleen, jotta muutokset tulevat voimaan.

**Jos ajetaan palveluna Windowsissa:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Jos ajetaan palveluna Linuxissa tai macOS:ssä:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Jos ajetaan manuaalisesti:**
```bash
digna serve --address localhost --port 8082
```

**Käynnistä myös web-palvelin uudelleen** — IIS tai Tomcat Windowsissa, nginx tai Apache Linuxissa ja macOS:ssä.

#### Vaihe 2: Avaa kojelauta

Avaa digna-kojelauta selaimessasi:

```
http://localhost:5173
```

(tai konfiguroitu kojelaudan URL)

#### Vaihe 3: Varmista kirjautumispainikkeet

Tarkista, että jokaiselle konfiguroidulle tarjoajalle näkyy kirjautumispainike:

- Näkyvissä tulisi olla "Login with Microsoft" -painike
- Näkyvissä tulisi olla "Login with Google" -painike
- (Jos usePassword = true) Näkyvissä tulisi olla käyttäjätunnus-/salasanakentät

Jos painikkeet eivät näy:
- Tarkista, että `dashboard_config.toml` on tallennettu
- Tarkista, että kojelaudan palvelu on käynnistetty uudelleen
- Tarkista selaimen konsoli (F12) virheilmoituksia varten

#### Vaihe 4: Testaa SSO-kirjautuminen

Klikkaa yhtä SSO-painikkeista (esim. "Login with Microsoft"):

1. Sinut pitäisi ohjata identiteetin tarjoajan kirjautumissivulle
2. Kirjaudu yritystunnuksillasi
3. Sinut pitäisi ohjata takaisin dignaan
4. Sinut pitäisi olla kirjautuneena dignaan

#### Vaihe 5: Varmista käyttäjän luonti

Onnistuneen SSO-kirjautumisen jälkeen:

- Käyttäjän pitäisi luoda automaattisesti dignaan
- Käyttäjän pitäisi olla kirjautuneena
- Käyttäjäprofiilissa pitäisi näkyä identiteetin tarjoajan tiedot
- Näkyvissä pitäisi olla dignan kojelauta

#### Vaihe 6: Testaa salasanaan perustuva kirjautuminen (jos käytössä)

Jos `usePassword = true`:

1. Kirjaudu ulos dignasta
2. Kirjautumissivulla syötä käyttäjätunnus ja salasana
3. Sinun pitäisi pystyä kirjautumaan sisään salasanalla

---

## Vianetsintä {: #troubleshooting }

### Kirjautumispainikkeet eivät näy

**Oireet:**
- OIDC-kirjautumispainikkeita ei näy kirjautumissivulla
- Näkyvissä vain salasanakentät (jos usePassword = true)

**Mahdolliset syyt ja ratkaisut:**
1. Tarkista, että `dashboard_config.toml` on `dashboard/`-hakemistossa
2. Varmista, että `[[login.oidc]]`-osiot ovat paikallaan ja syntaksi on oikea
3. Käynnistä kojelaudan palvelu uudelleen
4. Tyhjennä selaimen välimuisti (Ctrl+Shift+Delete tai Cmd+Shift+Delete)
5. Tarkista selaimen konsoli (F12 → Console) virheilmoituksia varten

---

### Redirect URI -sopimattomuusvirhe

**Oireet:**
- Klikkauksen jälkeen virhe "redirect_uri mismatch"
- Virhe "The redirect URI is not registered"

**Mahdolliset syyt ja ratkaisut:**
1. Varmista, että `DIGNA_OIDC_REDIRECT_URI` `config.toml`-tiedostossa on oikein
2. Varmista, että redirect URI on rekisteröity identiteetin tarjoajan asetuksissa
3. Varmista, että molemmat käyttävät täsmälleen samaa URL:ia (mukaan lukien protokolla, domain, polku)
4. Tarkista kirjoitusvirheet redirect URI:ssa
5. Jos käytät HTTPS:ää, varmista että sertifikaatti on voimassa

---

### Virhe: Invalid Client Credentials

**Oireet:**
- Virheilmoitus "Invalid client ID or secret"
- Todennus epäonnistuu tunnusvirheellä

**Mahdolliset syyt ja ratkaisut:**
1. Varmista, että `DIGNA_OIDC_CLIENT_ID` ja `DIGNA_OIDC_CLIENT_SECRET` ovat oikein
2. Varmista, ettei arvoissa ole ylimääräisiä välilyöntejä tai erikoismerkkejä
3. Tarkista, etteivät tunnukset ole vanhentuneet tai peruutettu
4. Käynnistä backend-palvelu uudelleen konfiguraation päivittämisen jälkeen
5. Tarkista identiteetin tarjoajan konsolista, että tunnukset ovat aktiivisia

---

### Kirjautuminen jää jumiin tai aikakatkaistuu

**Oireet:**
- SSO-painikkeen klikkaaminen ei tee mitään
- Aikakatkaisu muutaman sekunnin jälkeen
- Selain näyttää "Failed to connect" tai vastaavaa

**Mahdolliset syyt ja ratkaisut:**
1. Varmista, että dignan backend on käynnissä: `digna repo check`
2. Tarkista verkkoyhteys identiteetin tarjoajaan
3. Varmista, että `DIGNA_OIDC_CONFIGURATION_URL` on saavutettavissa
4. Tarkista palomuurisäännöt, jotka sallivat ulospäin suuntautuvat HTTPS-yhteydet
5. Varmista, että backend ja kojelauta tavoittavat toisensa

---

### Käyttäjiä ei luoda automaattisesti

**Oireet:**
- SSO-kirjautuminen onnistuu mutta käyttäjää ei luoda dignaan
- Saat oikeusvirheen SSO-kirjautumisen jälkeen

**Mahdolliset syyt ja ratkaisut:**
1. Varmista, että OIDC-konfiguraatio on oikein
2. Tarkista, että käyttäjäoikeudet on määritetty oikein
3. Tarkastele dignan lokitiedostoja virheilmoituksia varten
4. Käynnistä backend-palvelu uudelleen
5. Ota yhteyttä support@digna.ai, jos ongelma jatkuu

---

## Tuetut palveluntarjoajat {: #supported-providers }

### Testatut ja tuetut

Seuraavat OIDC-palveluntarjoajat on testattu ja ne toimivat tunnetusti:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Aseta SSO AD FS:llä](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Aseta SSO Auth0:lla](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Aseta SSO Google Workspacelle](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Aseta SSO Keycloakilla](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Aseta SSO Microsoft Entra ID:llä](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Aseta SSO Oktalla](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Aseta SSO OneLoginilla](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Aseta SSO PingOnella](pingone_sso_guide.md) |

### Muut OIDC-palveluntarjoajat

Mikä tahansa OpenID Connectia tukevaja tarjoaja voidaan integroida. Tarvittavat tiedot:

- Client ID
- Client secret
- OpenID-konfiguraatio-URL (yleensä osoitteessa `/.well-known/openid-configuration`)
- Tuetut scopet (tyypillisesti `openid profile email`)

Ota yhteyttä support@digna.ai, jos tarvitset apua tietyn tarjoajan integroimisessa.

---

## Parhaat käytännöt

**TEE:**
- Käytä HTTPS:ää tuotannossa (älä HTTP:tä)
- Säilytä client secretit turvallisesti (käytä ympäristömuuttujia aina kun mahdollista)
- Kierätä salaisuuksia säännöllisesti
- Testaa ensin ei-tuotantoympäristössä
- Dokumentoi mitkä tarjoajat on konfiguroitu
- Seuraa kirjautumislokeja epäilyttävän toiminnan varalta
- Pidä identiteetin tarjoajan konfiguraatio synkronissa dignan konfiguraation kanssa

**ÄLÄ:**
- Säilytä client secretteja versionhallinnassa
- Käytä HTTP-redirect-URI:ita tuotannossa
- Konfiguroi useita tarjoajia samalla key-arvolla
- Jätä oletus/testitunnuksia tuotantoon
- Julkaise konfiguraatiotiedostoja, jotka sisältävät salaisuuksia
- Sekoita kehitys- ja tuotantotunnuksia

---

## Tuki

Tarvitsetko apua SSO-määrityksissä?

- **Sähköposti:** support@digna.ai
- **Dokumentaatio:** https://docs.digna.ai
- **Verkkosivusto:** https://www.digna.ai

---

**Viimeksi päivitetty:** 30. elokuuta 2026  
**Julkaisu:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**