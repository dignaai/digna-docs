---
title: Keycloak SSO – integracija enkratne prijave (Single Sign-On) | Dokumentacija digna
description: Konfigurirajte enkratno prijavo za digna z Keycloak preko OpenID Connect — nastavitev realm in klienta, overjanje klienta, veljavne URI-ji za preusmeritev, skrivnost klienta in ustrezna konfiguracija digna.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, zaupni odjemalec, openid connect, samostojni ponudnik identitete
---

# Nastavite SSO z Keycloak

Keycloak je samostojno gostujoč ponudnik identitete, popolnoma skladen z OIDC. Ker ga gostite sami, je discovery URL sestavljen iz vaše lastne domene in imena realm, ne iz domene ponudnika.

Ta vodnik pokriva **stran Keycloak**: ustvarjanje klienta in zbiranje vrednosti, ki jih potrebuje digna. Stran digna — `dashboard_config.toml`, testiranje in odpravljanje napak — je enaka za vse ponudnike in je opisana v [Single Sign-On Overview](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Keycloak verzija** | 17 ali novejša za URL poti uporabljene tukaj — glejte opombo v 4. koraku |
| **Vloga v Keycloak** | `realm-admin` na ciljnem realm, ali strežniški administrator |
| **Realm** | Realm, kateremu pripadajo vaši digna uporabniki, ne nujno `master` |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## Korak 1: Izberite realm

1. Odprite Keycloak admin konzolo
2. Uporabite izbirnik realm v zgornjem levem kotu, da preklopite na realm, v katerem so vaši uporabniki

!!! warning "Ne uporabljajte reama master"

    Realm `master` je namenjen upravljanju samega Keycloak-a. Aplikacijski klienti naj bodo v namenskem realm; postavitev digna v `master` daje njegovim uporabnikom pot v Keycloak administracijsko konzolo.

---

## Korak 2: Ustvarite klienta

1. Pojdite na **Clients** in kliknite **Create client**
2. Konfigurirajte:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — to postane `DIGNA_OIDC_CLIENT_ID`
3. Kliknite **Next**
4. Na koraku **Capability config** vklopite **Client authentication** (**On**)
5. Pustite omogočen **Standard flow**; drugi flovi niso potrebni
6. Kliknite **Next**

!!! warning "Client authentication mora biti vklopljen"

    Ko je **Client authentication** izklopljen, Keycloak ustvari *public* klienta, ki nima nobenih poverilnic — zavihka **Credentials** v Koraku 4 ne bo. digna potrebuje zaupnega (confidential) klienta. Ta stikalo se da spremeniti tudi po kreaciji, če ste naredili napako.

---

## Korak 3: Nastavite Redirect URI

Na koraku **Login settings** (ali kasneje na zavihku **Settings**):

1. **Valid redirect URIs**: vnesite vaš digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: pustite prazno, ali nastavite na `+`, da zrcali redirect URIs
3. Kliknite **Save**

!!! tip "Izogibajte se wildcardom"

    Keycloak sprejema vzorce kot `https://digna.yourdomain.com/*`. Wildcard dovoli katerikoli path na tem gostitelju, da prejme avtentikacijsko kodo, zato raje uporabite točen callback URL.

---

## Korak 4: Pridobite client secret

1. Odprite zavihek **Credentials**
2. Potrdite, da je **Client Authenticator** *Client Id and Secret*
3. Kopirajte **Client secret** → postane `DIGNA_OIDC_CLIENT_SECRET`

Skrivnost je tukaj dostopna in se jo da tudi regenerirati z **Regenerate**.

---

## Korak 5: Sestavite Discovery URL

Zamenjajte svoj Keycloak host in ime realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Na primer:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 in starejši vključujejo /auth"

    Pred Keycloak 17 so bili vsi endpointi pod prefiksom `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Distribucije, ki nastavijo `KC_HTTP_RELATIVE_PATH=/auth`, obdržijo staro postavitev tudi na trenutnih verzijah. Če URL brez `/auth` vrne 404, poskusite z `/auth`.

Odprite URL v brskalniku preden nadaljujete. JSON dokument potrdi, da sta host in realm pravilna.

---

## Korak 6: Konfigurirajte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Prijava z Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Ključ `key` v obeh datotekah se mora ujemati — tukaj `keycloak`. Upoštevajte, da ni nujno enak Keycloak **Client ID**, čeprav je lažje slediti, če sta enaka.

---

## Korak 7: Testirajte

Ponovno zaženite backend in spletni strežnik, nato odprite dashboard. Za celoten kontrolni seznam glejte [Testing Login](overview.md#testing-login).

---

## Odpravljanje težav s Keycloak

### Invalid parameter: redirect_uri

Callback URL ni zajet v **Valid redirect URIs**. Keycloak zabeleži URI, ki ga je prejel, v strežniški log, kar je najhitrejši način za odkrivanje natanko neskladja.

### Zavihek Credentials manjka

Klient je public. Vklopite **Client authentication** v **Settings → Capability config**.

### 404 na Discovery URL

Bodisi je ime realm napačno, bodisi deployment uporablja prefix `/auth`. Preverite seznam realm v admin konzoli in poskusite oboje.

### unauthorized_client ali invalid_client

**Standard flow** je onemogočen v **Capability config**, ali pa je bila skrivnost regenerirana v Keycloak brez posodobitve v `config.toml`.

### Napake s certifikatom iz backend-a

Samostojno gostovan Keycloak za zasebnim ali samopodpisanim certifikatom bo odpovedal odhodne HTTPS klice digna na discovery URL. Namestite izdajni CA v trust store stroja, na katerem teče digna backend.

---

## Povezave

- [Single Sign-On Overview](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje napak
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)