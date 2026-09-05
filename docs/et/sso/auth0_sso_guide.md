---
title: Auth0 SSO – Single Sign-On Integratsioon | digna Dokumentatsioon
description: Seadista digna jaoks Single Sign-On Auth0 abil kasutades OpenID Connecti — regulaarsed veebirakenduse seaded, lubatud callback URL-id, kliendi mandaadid, tenant'i domeen ja vastav digna konfiguratsioon.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regulaarsed veebirakendused, callback url-id, openid connect, ettevõtte autentimine
---

# Seadista SSO Auth0-ga

Auth0 on OIDC-ühilduv ja pakub iga tenant'i jaoks avastuse (discovery) lõpp-punkti. Peamine, mis peab õigesti olema, on tenant'i domeen, mis ilmub avastuse URL-is ja muutub, kui lubate kohandatud domeeni.

See juhend käsitleb **Auth0 poolt** tehtavat: rakenduse loomist ja väärtuste kogumist, mida digna vajab. Digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on sama iga pakkuja puhul ning on kirjeldatud jaotises [Single Sign-On Overview](overview.md).

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **Auth0 role** | Tenant'i administraator |
| **Tenant domain** | nt `yourcompany.eu.auth0.com` — regiooni segment on oluline |
| **digna redirect URI** | URL, kuhu kasutaja pärast sisselogimist tagasi suunatakse, nt `https://digna.yourdomain.com/oidc/callback` |

---

## Samm 1: Loo rakendus

1. Logi sisse [Auth0 Dashboardi](https://manage.auth0.com)
2. Mine **Applications → Applications**
3. Klõpsa **Create Application**
4. Pane nimi `digna` ja vali **Regular Web Applications**
5. Klõpsa **Create**

!!! warning "Vali Regular Web Applications"

    *Single Page Application* ja *Native* loovad avalikke kliente ilma salajase võtmeta. digna vahetab koodi oma backendis ja vajab konfidentsiaalset klienti, seega on õige tüüp **Regular Web Applications**. Erinevalt mõnest muust pakkujast lubab Auth0 tüübi hiljem muuta **Settings → Application Type** all.

---

## Samm 2: Lisa callback URL

Rakenduse **Settings** vahekaardil:

1. Leia **Allowed Callback URLs**
2. Sisesta oma digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Võimalusel sea **Allowed Logout URLs** oma dashboardi URL-iks
4. Kerige alla ja klõpsake **Save Changes**

!!! note "Komadega eraldatud, mitte reavahetusega"

    Auth0 aktsepteerib selles väljal mitut callback URL-i, eraldatuna komadega. Uute ridadega eraldatud loend loetakse üheks vigaseks URL-iks ja ei vasta vaikimisi millelegi.

---

## Samm 3: Kogu mandaadid

Endiselt **Settings** vahekaardil, paneelis **Basic Information**:

- **Domain** → läheb avastuse (discovery) URL-i
- **Client ID** → muutub `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → muutub `DIGNA_OIDC_CLIENT_SECRET` (klõpsa, et paljastada)

---

## Samm 4: Kinnita Grant Type

1. Mine **Settings → Advanced Settings → Grant Types**
2. Kinnita, et **Authorization Code** on märgitud

See on vaikimisi lubatud Regular Web Applications jaoks. Kui see on tühistatud, ebaõnnestub digna sisselogimine tõrkega `unauthorized_client`.

---

## Samm 5: Koosta avastuse URL

Asenda Step 3-st saadud **Domain**:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Näiteks:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Kohandatud domeenid muudavad väljastajat (issuer)"

    Kui teie tenant kasutab kohandatud domeeni nagu `login.yourcompany.com`, kasutage avastuse URL-is seda domeeni. Nende kahe segamine — kanoniline domeen avastuse URL-is ja kohandatud domeen brauseris — tekitab issuer-i mittevastavuse ja token lükatakse tagasi pärast muidu edukat sisselogimist.

---

## Samm 6: Konfigureeri digna

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

Mõlemas failis peab `key` ühtima — siin on see `auth0`.

---

## Samm 7: Testi

Taaskäivitage backend ja veebiserver, seejärel avage dashboard. Täielik kontrollnimekiri on kirjas jaotises [Testing Login](overview.md#testing-login).

---

## Tõrkeotsing Auth0

### Callback URL-i mittevastavus

Auth0 vea leht näitab URL-i, mida see sai. Lisa see **Allowed Callback URLs** väljale, kontrollides, et kirjed on komadega eraldatud.

### unauthorized_client

**Authorization Code** ei ole lubatud **Advanced Settings → Grant Types** all, või ei ole rakenduse tüüp Regular Web Applications.

### Ligipääs keelatud pärast edukat sisselogimist

Tenant'is olev Rule, Action või Post-Login trigger lükkab kasutaja tagasi. Kontrolli **Actions → Flows → Login** ning tenant'i logisid (Monitoring → Logs), kus on täpne põhjus nähtav.

### Issuersi mittevastavus

Avastuse URL ja domeen, kuhu brauser saadeti, erinevad — tavaliselt kanoniline tenant'i domeen vs kohandatud domeen. Kasutage ühtset domeeni.

---

## Vaata ka

- [Single Sign-On Overview](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)