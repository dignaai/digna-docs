---
title: Okta SSO — Single Sign-On integrācija | digna dokumentācija
description: Konfigurējiet Single Sign-On (SSO) digna, izmantojot Okta un OpenID Connect — lietotnes integrācija, pieteikšanās pāradresācijas URI, klienta akreditācijas dati, autorizācijas servera izvēle un atbilstošā digna konfigurācija.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, lietotnes integrācija, autorizācijas serveris, OpenID Connect, uzņēmuma autentifikācija
---

# Iestatīt SSO ar Okta

Okta atbilst OIDC standartam, taču ar vienu īpatnību, kas pārsteidz lielāko daļu pirmreizējo integrāciju: Okta organizācijai (org) ir vairāk nekā viens autorizācijas serveris, un katram no tiem ir savs atklāšanas (discovery) URL.

Šis ceļvedis aptver **Okta pusi**: lietotnes integrācijas izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **Okta loma** | Super Administrator vai administratora loma, kurai atļauts izveidot lietotņu integrācijas |
| **Okta domēns** | piem. `yourcompany.okta.com` vai pielāgots domēns, ja tāds ir konfigurēts |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Izveidot lietotnes integrāciju

1. Piesakieties Okta Admin Console
2. Dodieties uz **Applications → Applications**
3. Noklikšķiniet **Create App Integration**
4. Atlasiet:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Noklikšķiniet **Next**

!!! warning "Lietotnes tipu nevar mainīt"

    Ja *Web Application* vietā izvēlaties *Single-Page Application*, tiek izveidots publisks klients bez slepenās atslēgas (secret), un digna backend koda apmaiņa neizdosies ar kļūdu `invalid_client`. Tips tiek noteikts izveides brīdī — nepareiza izvēle nozīmē, ka lietotne jādzēš un jāsāk no jauna.

---

## 2. solis: Konfigurēt integrāciju

1. **App integration name**: `digna`
2. **Grant type**: atstājiet atlasītu *Authorization Code*
3. **Sign-in redirect URIs**: ievadiet savu digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: nav obligāti
5. Sadaļā **Assignments** izvēlieties, kas drīkst izmantot integrāciju — konkrēta grupa ir drošāka nekā *Allow everyone in your organization to access*
6. Noklikšķiniet **Save**

!!! note "Piešķiršana ir obligāta"

    Okta autentificē lietotāju un pēc tam pārbauda, vai viņš ir piešķirts lietotnei. Nepiešķirts lietotājs nonāk Okta pieteikšanās lapā, veiksmīgi piesakās, bet tiek atraidīts, kad notiek pāradresācija atpakaļ. Ja pieteikšanās darbojas jums, bet ne kolēģiem, vispirms pārbaudiet piešķiršanu.

---

## 3. solis: Savākt akreditācijas datus

Lietotnes cilnē **General**, sadaļā **Client Credentials**:

- **Client ID** → kļūst par `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → kļūst par `DIGNA_OIDC_CLIENT_SECRET` (noklikšķiniet uz acs ikonas, lai to parādītu)

---

## 4. solis: Izvēlēties autorizācijas serveri

Šis solis nosaka jūsu discovery URL. Dodieties uz **Security → API**, lai redzētu jūsu organizācijas autorizācijas serverus.

**Org autorizācijas serveris** — izsniedz tokenus pašai Okta organizācijai:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Pielāgots autorizācijas serveris** — ieskaitot to, ko Okta izveido ar nosaukumu `default`:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Iebūvētajam serverim `<auth_server_id>` burtiski ir `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Kuru izvēlēties?"

    Izmantojiet **org** autorizācijas serveri, ja vien jūsu organizācija jau nav standartizējusi pielāgotu serveri API piekļuves politikām. Okta Developer kontos noklusējums ir `default`; daudzas uzņēmumu organizācijas to atspējo. Atveriet abus URL pārlūkā — tas, kas atgriež JSON, nevis kļūdu, ir jums pieejamais.

---

## 5. solis: Konfigurēt digna

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
[oidc_clients.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Abos failos `key` vērtībai jāsakrīt — šeit `okta`.

---

## 6. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet sadaļā [Pieteikšanās testēšana](overview.md#testing-login).

---

## Okta problēmu novēršana

### Redirect URI nav reģistrēts

Okta kļūdas ziņojumā norāda problemātisko URI. Salīdziniet to ar **General → Sign-in redirect URIs**; Okta salīdzina pilnu virkni, ieskaitot jebkuru beigu slīpsvītru.

### Lietotājs nav piešķirts klienta lietotnei

Konts nav lietotnes piešķīrumu sarakstā. Pievienojiet lietotāju vai viņa grupu sadaļā **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` discovery URL neeksistē — visbiežāk tas ir `default` organizācijā, kurā tas ir noņemts. Pārbaudiet **Security → API**, lai redzētu faktiski pieejamos serverus.

### invalid_client tokena solī

Integrācija tika izveidota kā Single-Page Application, un tai nav klienta slepenās atslēgas. Izveidojiet to no jauna kā Web Application.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
