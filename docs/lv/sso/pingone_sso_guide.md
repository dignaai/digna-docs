---
title: PingOne SSO — Single Sign-On integrācija | digna dokumentācija
description: Konfigurējiet Single Sign-On (SSO) digna, izmantojot PingOne un OpenID Connect — OIDC web lietotnes iestatīšana, pāradresācijas URI, klienta akreditācijas dati, Environment ID, reģionālie domēni un atbilstošā digna konfigurācija.
image: /assets/logo_square.png
keywords: digna sso, pingone sso, ping identity, pingone oidc, vides ID, OpenID Connect, uzņēmuma autentifikācija
---

# Iestatīt SSO ar PingOne

PingOne atbilst OIDC standartam. Divām no tā vērtībām jāpievērš īpaša uzmanība: **Environment ID**, kas parādās katrā gala punktā (endpoint) URL, un **reģionālais domēns**, kas atšķiras starp Ziemeļamerikas, Eiropas, Kanādas, Āzijas‑Kliedes un Austrālijas tenantiem.

Šis ceļvedis aptver **PingOne pusi**: lietotnes izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **PingOne loma** | Environment Admin vai Identity Data Admin mērķa vidē |
| **Environment** | PingOne vide, kurā atrodas jūsu digna lietotāji |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Izveidot lietotni

1. Piesakieties PingOne administrācijas konsolē un izvēlieties savu vidi
2. Dodieties uz **Applications → Applications**
3. Noklikšķiniet uz pogas ar **+**
4. Ievadiet `digna` kā **Application Name**
5. Atlasiet **OIDC Web App**
6. Noklikšķiniet **Save**

!!! warning "Izvēlieties OIDC Web App, nevis Single-Page App"

    *Single-Page App* un *Native App* izveido publiskus klientus, kas nevar glabāt slepeni. digna apmaina autorizācijas kodu no sava backend un nepieciešams konfidenciāls **OIDC Web App** tips.

---

## 2. solis: Konfigurēt redirect URI

1. Atveriet lietotnes cilni **Configuration**
2. Noklikšķiniet uz zīmuļa ikonas, lai rediģētu
3. Pārliecinieties, ka **Response Type** ir *Code* un **Grant Type** ir *Authorization Code*
4. Sadaļā **Redirect URIs** ievadiet savu digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

5. Iestatiet **Token Endpoint Authentication Method** uz *Client Secret Post* vai *Client Secret Basic*
6. Noklikšķiniet **Save**

---

## 3. solis: Ieslēgt lietotni

Lietotnes rindā vai detaļu panelī pārslēdziet slēdzi uz **enabled**.

!!! warning "Jaunas lietotnes sākotnēji ir atslēgtas"

    PingOne izveido lietotnes atslēgtā stāvoklī. Atslēgta lietotne radīs kļūdu autorizācijas solī, kas nesauks ārā slēdža stāvokli, tāpēc šo ir vērts pārbaudīt pirms cita meklēšanas.

---

## 4. solis: Piešķirt scope

1. Atveriet cilni **Resources**
2. Pārliecinieties, ka `openid` ir piešķirts, un pievienojiet `profile` un `email` no **OpenID Connect** resursa
3. Noklikšķiniet **Save**

---

## 5. solis: Piešķirt piekļuvi lietotājiem

1. Atveriet cilni **Access**
2. Pievienojiet populāciju vai grupas, kuru dalībnieki var izmantot digna
3. Noklikšķiniet **Save**

---

## 6. solis: Savākt akreditācijas datus un Environment ID

Cilnē **Configuration** izvērst **General**:

- **Client ID** → kļūst par `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → kļūst par `DIGNA_OIDC_CLIENT_SECRET` (noklikšķiniet uz acu ikonas)
- **Environment ID** → tiek izmantots atklāšanas (discovery) URL

Tajā pašā cilnē ir pieejams gatavs **OIDC Discovery Endpoint**, ko varat kopēt tieši, neassemblējot to pašrocīgi.

---

## 7. solis: Izveidot Discovery URL

Aizvietojiet environment ID un domēnu atbilstoši jūsu reģionam:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Reģions | Domēns |
|---|---|
| Ziemeļamerika | `auth.pingone.com` |
| Eiropa | `auth.pingone.eu` |
| Kanāda | `auth.pingone.ca` |
| Āzijas‑Kliede | `auth.pingone.asia` |
| Austrālija | `auth.pingone.com.au` |

Eiropas videi piemērs:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Kopējiet, nevis rakstiet"

    Reģionālais domēns ir visizplatītākā kļūda PingOne integrācijā, un nepareizs reģions dod 404 kļūdu, nevis saprotamu ziņojumu. Izmantojiet **OIDC Discovery Endpoint** vērtību no 6. soļa.

---

## 8. solis: Konfigurēt digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Abi failos `key` vērtībai jābūt sakrītošai — šeit `pingone`.

---

## 9. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet [Pieteikšanās testēšana](overview.md#testing-login).

---

## PingOne problēmu novēršana

### 404 pie Discovery URL

Reģionālais domēns vai environment ID ir nepareizs. Salīdziniet ar **OIDC Discovery Endpoint**, kas redzams lietotnes cilnē Configuration.

### NOT_FOUND vai lietotne atspējota

Lietotnes slēdzis no 3. soļa joprojām ir izslēgts.

### Redirect URI nesakritība

PingOne salīdzina pilnu virkni. Pārbaudiet **Configuration → Redirect URIs** vai nav liekas slīpsvītras (trailing slash) vai shēmas atšķirības.

### Pieteikšanās izdevusies, bet digna nesaņem e-pasta claim

Sadaļā **Resources** nav piešķirti `email` un `profile` scope.

### Lietotājs neredz lietotni

Sadaļā **Access** nav piešķirta piekļuve attiecīgajai populācijai vai grupai.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)