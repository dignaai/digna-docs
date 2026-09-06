# Seadista SSO OneLoginiga

OneLogin on OIDC-ühilduv. Selle eripära on, et connector type valitakse kataloogist rakenduse loomisel ja seda ei saa hiljem muuta.

See juhend käsitleb **OneLogini poolt**: rakenduse loomist ja väärtuste kogumist, mida digna vajab. Digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on iga pakkuja puhul sama ja on kirjeldatud [Ühekordne sisselogimine — ülevaade](overview.md).

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **OneLogini roll** | Konto omanik või administraator, kellel on õigus lisada rakendusi |
| **Alamdomeen** | nt `yourcompany.onelogin.com` |
| **digna ümbersuunamise URI** | URL, millele kasutajad pärast sisselogimist naasevad, nt `https://digna.yourdomain.com/oidc/callback` |

---

## Samm 1: Loo OIDC-rakendus

1. Logi sisse OneLogin Admin portaali
2. Mine **Applications → Applications**
3. Klõpsa **Add App**
4. Otsi `OpenId Connect` ja vali **OpenId Connect (OIDC)** konnektor
5. Sea **Display Name** väärtuseks `digna`
6. Klõpsa **Save**

!!! warning "Konnektori tüüp on fikseeritud loomisel"

    OneLoginil on kataloogikanded SAML-i ja OIDC jaoks eraldi ning rakendust ei saa ühest teiseks konverteerida. Kui valite ekslikult SAML-konnektori, kustutage rakendus ja lisage see uuesti — puudub seadistus, mis lubaks protokolli vahetada.

---

## Samm 2: Konfigureeri ümbersuunamise URI

1. Ava **Configuration** vahekaart
2. Väljale **Redirect URI's** sisesta oma digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Või alternatiivina määra **Post Logout Redirect URIs** oma dashboardi URL-iks
4. Klõpsa **Save**

!!! note "Iga URI eraldi reale"

    Erinevalt pakkujatest, kes ootavad koma-eraldatud loendit, võtab OneLogin'i **Redirect URI's** väli ühe URI rea kohta.

---

## Samm 3: Määra rakenduse tüüp ja autentimismeetod

1. Ava **SSO** vahekaart
2. Kinnita, et **Application Type** on *Web*
3. Sea **Token Endpoint → Authentication Method** väärtuseks *POST* (`client_secret_post`) või *Basic* (`client_secret_basic`)

!!! warning "Ära vali 'None'"

    Kui autentimismeetodiks määratakse *None*, muutub rakendus avalikuks kliendiks ilma salajata ning digna backend'i kood vahetusel lükkab selle tagasi. Kasuta kas POSTi või Basicut.

---

## Samm 4: Hangi mandaadid

Endiselt **SSO** vahekaardil:

- **Client ID** → saab `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → saab `DIGNA_OIDC_CLIENT_SECRET` (klõpsake **Show client secret**)

Lehel kuvatakse ka **Issuer URL**, mis kinnitab järgmises etapis kasutatavat avastamise URL-i.

---

## Samm 5: Määra kasutajad

1. Ava **Access** vahekaart
2. Lisa rollid või grupid, mille liikmed tohib dignat kasutada
3. Klõpsa **Save**

!!! note "Määramata kasutajaid pärast sisselogimist tagasi lükatakse"

    Nagu enamik pakkujaid, autentib OneLogin kasutaja esmalt ja kontrollib seejärel õigusi. Määramata kasutaja logib sisse edukalt ja lükatakse seejärel tagasi, mis näeb välja nagu digna viga, mitte ligipääsuotsus.

---

## Samm 6: Koosta Discovery URL

Asenda oma OneLogin alamdomeen:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Näiteks:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 on API versioon"

    OneLogini praegune OIDC-i implementatsioon asub aadressil `/oidc/2/`. Vanem dokumentatsioon näitab `/oidc/` ilma versioonita, mis viitab pensionile jäänud esimesel versioonile. Kontrolli vajadusel **Issuer URL** väärtust SSO vahekaardil — avastamise URL on issuer pluss `/.well-known/openid-configuration`.

---

## Samm 7: Konfigureeri digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Logi sisse OneLoginiga"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Mõlemas failis peab `key` kattuma — siin on see `onelogin`.

---

## Samm 8: Testimine

Taaskäivita backend ja veebiserver ning ava dashboard. Täieliku kontrollnimekirja leiad lehelt [Sisselogimise testimine](overview.md#testing-login).

---

## OneLogini tõrkeotsing

### redirect_uri ei klapi

Callback URL puudub **Configuration → Redirect URI's** seadetest või kirjed olid eraldatud komadega, mitte uutega ridadega.

### invalid_client tokeni sammus

**Token Endpoint → Authentication Method** on seatud väärtusele *None* või `config.toml`-is olev kliendisaladus on aegunud. Näita salajasust **SSO** vahekaardil ja võrdle.

### Rakendus ei ilmu kasutajatele

Ühelgi rollil ega grupil pole **Access** vahekaardil juurdepääsu antud.

### 404 Discovery URL-il

Alamdomeen on vale või URL jätab ära `/oidc/2/`. Võrdle SSO vahekaardil kuvatud **Issuer URL**-iga.

---

## Vaata ka

- [Ühekordne sisselogimine — ülevaade](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)