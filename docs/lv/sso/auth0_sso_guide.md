---
title: Auth0 SSO — Single Sign-On integrācija | digna dokumentācija
description: Konfigurējiet Single Sign-On (SSO) digna, izmantojot Auth0 un OpenID Connect — Regular Web Application iestatīšana, atļautie callback URL, klienta akreditācijas dati, tenant domēns un atbilstošā digna konfigurācija.
image: /assets/logo_square.png
keywords: digna sso, auth0 sso, auth0 oidc, regular web application, callback URL, OpenID Connect, uzņēmuma autentifikācija
---

# Iestatīt SSO ar Auth0

Auth0 atbilst OIDC standartam un nodrošina atklāšanas (discovery) gala punktu katram tenantam. Galvenais, kas jāiestata pareizi, ir tenant domēns, kas parādās discovery URL un mainās, ja iespējojat pielāgotu domēnu.

Šis ceļvedis aptver **Auth0 pusi**: lietotnes izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **Auth0 loma** | Admin attiecīgajā tenantā |
| **Tenant domēns** | piem. `yourcompany.eu.auth0.com` — reģiona segments ir svarīgs |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Izveidot lietotni

1. Piesakieties [Auth0 Dashboard](https://manage.auth0.com)
2. Dodieties uz **Applications → Applications**
3. Noklikšķiniet **Create Application**
4. Nosauciet to `digna` un izvēlieties **Regular Web Applications**
5. Noklikšķiniet **Create**

!!! warning "Izvēlieties Regular Web Applications"

    *Single Page Application* un *Native* izveido publiskus klientus bez slepenās atslēgas (secret). digna veic koda apmaiņu no sava backend, un tai nepieciešams konfidenciāls klients, tāpēc pareizais tips ir **Regular Web Applications**. Atšķirībā no dažiem citiem pakalpojumu sniedzējiem Auth0 ļauj mainīt tipu arī vēlāk sadaļā **Settings → Application Type**.

---

## 2. solis: Pievienot callback URL

Lietotnes cilnē **Settings**:

1. Atrodiet **Allowed Callback URLs**
2. Ievadiet savu digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Pēc izvēles iestatiet **Allowed Logout URLs** uz sava dashboard URL
4. Ritiniet līdz lapas apakšai un noklikšķiniet **Save Changes**

!!! note "Atdaliet ar komatiem, nevis jaunām rindām"

    Auth0 šajā laukā pieņem vairākus callback URL, kas atdalīti ar komatiem. Saraksts, kas atdalīts tikai ar jaunām rindām, tiek nolasīts kā viens nekorekts URL un bez brīdinājuma neatbilst nekam.

---

## 3. solis: Savākt akreditācijas datus

Joprojām cilnē **Settings**, panelī **Basic Information**:

- **Domain** → tiek izmantots discovery URL
- **Client ID** → kļūst par `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → kļūst par `DIGNA_OIDC_CLIENT_SECRET` (noklikšķiniet, lai parādītu)

---

## 4. solis: Pārbaudīt grant tipu

1. Dodieties uz **Settings → Advanced Settings → Grant Types**
2. Pārliecinieties, ka **Authorization Code** ir atzīmēts

Regular Web Applications tas ir iespējots pēc noklusējuma. Ja atzīme ir noņemta, digna pieteikšanās neizdodas ar kļūdu `unauthorized_client`.

---

## 5. solis: Izveidot discovery URL

Ievietojiet **Domain** vērtību no 3. soļa:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Piemēram:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Pielāgoti domēni maina izdevēju (issuer)"

    Ja jūsu tenants izmanto pielāgotu domēnu, piemēram, `login.yourcompany.com`, izmantojiet šo domēnu discovery URL. Ja abi tiek jaukti — kanoniskais domēns discovery URL, bet pielāgotais pārlūkā —, rodas issuer neatbilstība, un tokens tiek noraidīts pēc citādi veiksmīgas pieteikšanās.

---

## 6. solis: Konfigurēt digna

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
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Abos failos `key` vērtībai jāsakrīt — šeit `auth0`.

---

## 7. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet sadaļā [Pieteikšanās testēšana](overview.md#testing-login).

---

## Auth0 problēmu novēršana

### Callback URL neatbilstība

Auth0 kļūdas lapā norādīts saņemtais URL. Pievienojiet to laukam **Allowed Callback URLs** un pārbaudiet, vai ieraksti ir atdalīti ar komatiem.

### unauthorized_client

Sadaļā **Advanced Settings → Grant Types** nav iespējots **Authorization Code**, vai arī lietotnes tips nav Regular Web Applications.

### Piekļuve liegta pēc veiksmīgas pieteikšanās

Tenantā kāds Rule, Action vai Post-Login trigeris noraida lietotāju. Pārbaudiet **Actions → Flows → Login** un tenanta žurnālus sadaļā **Monitoring → Logs**, kuros redzams precīzs iemesls.

### Issuer neatbilstība

Discovery URL un domēns, uz kuru tika novirzīts pārlūks, atšķiras — parasti tas ir kanoniskais tenant domēns pret pielāgoto domēnu. Konsekventi izmantojiet vienu no tiem.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)
