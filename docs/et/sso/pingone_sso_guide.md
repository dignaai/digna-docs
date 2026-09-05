---
title: PingOne SSO – Single Sign-On integreerimine | digna dokumentatsioon
description: Konfigureeri Single Sign-On (SSO) digna jaoks kasutades PingOne'i ja OpenID Connecti — OIDC veebirakenduse seadistus, ümbersuunamise URI-d, kliendi mandaadid, environment ID, piirkondlikud domeenid ja vastav digna konfiguratsioon.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, Ping Identity, PingOne OIDC, environment id, OpenID Connect, ettevõtte autentimine
---

# SSO seadistamine PingOne'iga

PingOne järgib OIDC standardit. Kaks väärtust vajavad erilist tähelepanu: **environment ID**, mis ilmub igas lõpp-punkti URL-is, ja **piirkondlik domeen**, mis erineb Põhja-Ameerika, Euroopa, Kanada, Aasia-Vaikse ookeani ja Austraalia tenantide vahel.

See juhend käsitleb **PingOne'i poolt** tehtavaid toiminguid: rakenduse loomist ja väärtuste kogumist, mida digna vajab. digna pool — `dashboard_config.toml`, testimine ja veaotsing — on sama iga pakkuja puhul ning on kirjeldatud jaotises [Single Sign-On Overview](overview.md).

---

## Enne alustamist

| Requirement | Notes |
|---|---|
| **PingOne role** | Environment Admin või Identity Data Admin sihtkeskkonnas |
| **Environment** | PingOne keskkond, mille alla kuuluvad teie digna kasutajad |
| **digna redirect URI** | URL, kuhu kasutaja naaseb peale sisselogimist, nt `https://digna.yourdomain.com/oidc/callback` |

---

## 1. samm: Loo rakendus

1. Logi sisse PingOne administraatori konsooli ja vali oma keskkond
2. Mine menüüsse **Applications → Applications**
3. Klõpsa nuppu **+**
4. Sisesta **Application Name**-iks `digna`
5. Vali **OIDC Web App**
6. Klõpsa **Save**

!!! warning "Vali OIDC Web App, mitte Single-Page App"

    *Single-Page App* ja *Native App* loovad avalikke kliente, kes ei saa hoidma saladust (secret). digna vahetab autoriseerimiskoodi oma backendis ja vajab konfidentsiaalset tüüpi **OIDC Web App**.

---

## 2. samm: Seadista ümbersuunamise URI

1. Ava rakenduse **Configuration** vahekaart
2. Klõpsa pliiatsiikooni, et redigeerida
3. Kinnita, et **Response Type** on *Code* ja **Grant Type** on *Authorization Code*
4. Jaotises **Redirect URIs** sisesta oma digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. Sea **Token Endpoint Authentication Method** väärtuseks *Client Secret Post* või *Client Secret Basic*
6. Klõpsa **Save**

---

## 3. samm: Luba rakendus

Rakenduse real või detailpaneelil lülita lüliti olekusse **enabled**.

!!! warning "Uued rakendused on vaikimisi keelatud"

    PingOne loob rakendused vaikimisi keelatuna. Keelatud rakendus annab autoriseerimise sammule minnes vea, mis ei maini seda lülitit, seega tasub seda enne muu veaotsingu alustamist kontrollida.

---

## 4. samm: Anna andmed (scopes)

1. Ava **Resources** vahekaart
2. Kinnita, et `openid` on antud, ning lisa **OpenID Connect** ressursist `profile` ja `email`
3. Klõpsa **Save**

---

## 5. samm: Määra kasutajad

1. Ava **Access** vahekaart
2. Lisa populatsioon või grupid, mille liikmed võivad digna kasutada
3. Klõpsa **Save**

---

## 6. samm: Kogu kliendi mandaadid ja environment ID

Configuration vahekaardil laienda **General**:

- **Client ID** → muutub `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → muutub `DIGNA_OIDC_CLIENT_SECRET` (klõpsa silmaikooni)
- **Environment ID** → läheb avastamise (discovery) URL-i

Sama vahekaart kuvab valmis **OIDC Discovery Endpoint** väärtuse, mida võid kopeerida otse selle asemel, et seda käsitsi kokku panna.

---

## 7. samm: Koosta Discovery URL

Asenda environment ID ja domeen vastavalt oma piirkonnale:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domain |
|---|---|
| North America | `auth.pingone.com` |
| Europe | `auth.pingone.eu` |
| Canada | `auth.pingone.ca` |
| Asia-Pacific | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Euroopa keskkonna puhul:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopeeri, ära tippu"

    Piirkondlik domeen on kõige tavalisem viga PingOne'i integratsioonis, ja vale piirkond annab 404 vea, mitte kasulikku teate. Kasuta Step 6 vahekaardilt leitud **OIDC Discovery Endpoint** väärtust.

---

## 8. samm: Konfigureeri digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Logi sisse PingOne'iga"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Mõlema faili `key` peab klappima — siin on see `pingone`.

---

## 9. samm: Testi

Taaskäivita backend ja veebiserver, seejärel ava dashboard. Täielik kontrollnimekiri on kirjas jaotises [Testing Login](overview.md#testing-login).

---

## PingOne veaotsing

### 404 Discovery URL-il

Vale on piirkondlik domeen või environment ID. Võrdle väärtust rakenduse Configuration vahekaardil näidatava **OIDC Discovery Endpoint**-iga.

### NOT_FOUND või rakendus on keelatud

Rakenduse lüliti Step 3-s on endiselt välja lülitatud.

### Redirect URI ei klapi

PingOne võrdleb täisteksti. Kontrolli **Configuration → Redirect URIs** olemasolu tühiku (trailing slash) või skeemi erinevuse suhtes.

### Sisselogimine õnnestub, kuid dignasse ei jõua emaili claim

`email` ja `profile` õigused pole antud **Resources** vahekaardil.

### Kasutaja ei näe rakendust

Ühtegi populatsiooni ega gruppi ei ole antud õigusteks **Access** vahekaardil.

---

## Vt ka

- [Single Sign-On Overview](overview.md) — konfiguratsiooni viide, testimine ja üldine veaotsing
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)