---
title: Keycloak SSO — Single Sign-On integrācija | digna dokumentācija
description: Konfigurējiet Single Sign-On (SSO) digna, izmantojot Keycloak un OpenID Connect — realm un klienta iestatīšana, klienta autentifikācija, derīgie redirect URI, klienta slepenā atslēga un atbilstošā digna konfigurācija.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, konfidenciāls klients, OpenID Connect, pašmitināts identitātes nodrošinātājs
---

# Iestatīt SSO ar Keycloak

Keycloak ir pašmitināts (self-hosted) identitātes nodrošinātājs, kas pilnībā atbilst OIDC standartam. Tā kā jūs to darbināt paši, atklāšanas (discovery) URL tiek veidots no jūsu pašu resursdatora nosaukuma un realm, nevis no piegādātāja domēna.

Šis ceļvedis aptver **Keycloak pusi**: klienta izveidi un vērtību vākšanu, kas nepieciešamas digna. digna puse — `dashboard_config.toml`, testēšana un problēmu novēršana — ir vienāda visiem pakalpojumu sniedzējiem un aprakstīta [Single Sign-On pārskatā](overview.md).

---

## Pirms sākat

| Prasība | Piezīmes |
|---|---|
| **Keycloak versija** | 17 vai jaunāka šeit izmantotajiem URL ceļiem — skatiet piezīmi 4. solī |
| **Keycloak loma** | `realm-admin` mērķa realm vai servera administrators |
| **Realm** | Realm, kurā atrodas jūsu digna lietotāji, ne obligāti `master` |
| **digna redirect URI** | URL, uz kuru lietotāji atgriežas pēc pieteikšanās, piem. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. solis: Izvēlēties realm

1. Atveriet Keycloak administrācijas konsoli
2. Ar realm izvēlni augšējā kreisajā stūrī pārslēdzieties uz realm, kurā atrodas jūsu lietotāji

!!! warning "Neizmantojiet master realm"

    `master` realm ir paredzēts pašas Keycloak administrēšanai. Lietotņu klientiem jāatrodas atsevišķā realm; ievietojot digna realm `master`, tās lietotāji iegūst ceļu uz Keycloak administrācijas konsoli.

---

## 2. solis: Izveidot klientu

1. Dodieties uz **Clients** un noklikšķiniet **Create client**
2. Konfigurējiet:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — tas kļūst par `DIGNA_OIDC_CLIENT_ID`
3. Noklikšķiniet **Next**
4. Solī **Capability config** ieslēdziet **Client authentication** stāvoklī **On**
5. Atstājiet iespējotu **Standard flow**; pārējās plūsmas nav nepieciešamas
6. Noklikšķiniet **Next**

!!! warning "Client authentication jābūt ieslēgtam"

    Ja **Client authentication** ir izslēgts, Keycloak izveido *publisku* klientu, kuram vispār nav akreditācijas datu — cilne **Credentials** 4. solī nepastāvēs. digna nepieciešams konfidenciāls klients. Ja kļūdāties, šo slēdzi var mainīt arī pēc izveides.

---

## 3. solis: Iestatīt redirect URI

Solī **Login settings** (vai vēlāk cilnē **Settings**):

1. **Valid redirect URIs**: ievadiet savu digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: atstājiet tukšu vai iestatiet `+`, lai atspoguļotu redirect URI
3. Noklikšķiniet **Save**

!!! tip "Izvairieties no aizstājējzīmēm"

    Keycloak pieņem šablonus, piemēram, `https://digna.yourdomain.com/*`. Aizstājējzīme ļauj jebkuram ceļam šajā resursdatorā saņemt autorizācijas kodu, tāpēc dodiet priekšroku precīzam callback URL.

---

## 4. solis: Savākt klienta slepeno atslēgu

1. Atveriet cilni **Credentials**
2. Pārliecinieties, ka **Client Authenticator** ir *Client Id and Secret*
3. Nokopējiet **Client secret** → kļūst par `DIGNA_OIDC_CLIENT_SECRET`

Slepenā atslēga šeit paliek pieejama, un to var ģenerēt no jauna ar **Regenerate**.

---

## 5. solis: Izveidot discovery URL

Ievietojiet sava Keycloak resursdatora un realm nosaukumu:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Piemēram:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 un vecākās versijās ir /auth"

    Pirms Keycloak 17 visi gala punkti atradās zem prefiksa `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribūcijas, kas iestata `KC_HTTP_RELATIVE_PATH=/auth`, saglabā veco struktūru arī pašreizējās versijās. Ja URL bez `/auth` atgriež 404, mēģiniet ar to.

Pirms turpināt, atveriet URL pārlūkā. JSON dokuments apstiprina, ka resursdators un realm ir pareizi.

---

## 6. solis: Konfigurēt digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Login with Keycloak"
```

### `config.toml`

```toml
[oidc_clients.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Abos failos `key` vērtībai jāsakrīt — šeit `keycloak`. Ņemiet vērā, ka tai nav jābūt vienādai ar Keycloak **Client ID**, lai gan vienādas vērtības ir vieglāk pārskatāmas.

---

## 7. solis: Testēt

Restartējiet backend un web serveri, pēc tam atveriet dashboard. Pilnu pārbaudes sarakstu skatiet sadaļā [Pieteikšanās testēšana](overview.md#testing-login).

---

## Keycloak problēmu novēršana

### Invalid parameter: redirect_uri

Callback URL neietilpst **Valid redirect URIs**. Keycloak servera žurnālā reģistrē saņemto URI — tas ir ātrākais veids, kā redzēt precīzu neatbilstību.

### Nav cilnes Credentials

Klients ir publisks. Ieslēdziet **Client authentication** sadaļā **Settings → Capability config**.

### 404 pie discovery URL

Vai nu realm nosaukums ir nepareizs, vai arī izvietojums izmanto prefiksu `/auth`. Pārbaudiet realm sarakstu administrācijas konsolē un izmēģiniet abas URL formas.

### unauthorized_client vai invalid_client

Sadaļā **Capability config** ir atspējots **Standard flow**, vai arī slepenā atslēga Keycloak tika ģenerēta no jauna, neatjauninot `config.toml`.

### Sertifikātu kļūdas no backend

Pašmitināts Keycloak aiz privāta vai pašparakstīta sertifikāta izraisīs digna izejošā HTTPS pieprasījuma uz discovery URL kļūmi. Instalējiet izdevēju CA tā datora uzticamo sertifikātu krātuvē, kurā darbojas digna backend.

---

## Skatīt arī

- [Single Sign-On pārskats](overview.md) — konfigurācijas atsauce, testēšana un vispārīga problēmu novēršana
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)
