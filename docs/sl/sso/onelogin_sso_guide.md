---
title: OneLogin SSO – Integracija Single Sign-On | digna Dokumentacija
description: Konfigurirajte Single Sign-On za digna z OneLogin preko OpenID Connect — ustvarjanje OIDC aplikacije, redirect URI-ji, poverilnice odjemalca, overjanje na token endpointu in ustrezna konfiguracija digna.
image: /assets/logo_square.png
keywords: digna sso, onelogin sso, onelogin oidc, openid connect, preverjanje končne točke žetona, podjetniška avtentikacija
---

# Nastavitev SSO z OneLogin

OneLogin je združljiv z OIDC. Njegova posebnost je, da se tip konektorja izbere iz kataloga ob ustvarjanju aplikacije in ga pozneje ni mogoče spremeniti.

Ta vodič pokriva **OneLogin stran**: ustvarjanje aplikacije in zbiranje vrednosti, ki jih potrebuje digna. Digna stran — `dashboard_config.toml`, testiranje in odpravljanje težav — je enaka za vse ponudnike in je opisana v [Pregledu Single Sign-On](overview.md).

---

## Preden začnete

| Zahteva | Opombe |
|---|---|
| **Vloga v OneLogin** | Lastnik računa ali skrbnik z dovoljenjem za dodajanje aplikacij |
| **Poddomena** | npr. `yourcompany.onelogin.com` |
| **digna redirect URI** | URL, na katerega se uporabniki vrnejo po prijavi, npr. `https://digna.yourdomain.com/oidc/callback` |

---

## Korak 1: Ustvarite OIDC aplikacijo

1. Prijavite se v OneLogin Admin portal
2. Pojdite na **Applications → Applications**
3. Kliknite **Add App**
4. Poiščite `OpenId Connect` in izberite konektor **OpenId Connect (OIDC)**
5. Nastavite **Display Name** na `digna`
6. Kliknite **Save**

!!! warning "Vrsta konektorja je določena ob ustvarjanju"

    OneLogin ima ločene vnose v katalogu za SAML in OIDC, aplikacije pa ni mogoče pretvoriti iz enega protokola v drugega. Če po pomoti izberete SAML konektor, izbrišite aplikacijo in jo dodajte znova — ni nastavitve za preklop protokolov.

---

## Korak 2: Konfigurirajte Redirect URI

1. Odprite zavihek **Configuration**
2. V polje **Redirect URI's** vnesite vaš digna callback URL:

```
https://digna.yourdomain.com/oidc/callback
```

3. Po želji nastavite **Post Logout Redirect URIs** na URL nadzorne plošče
4. Kliknite **Save**

!!! note "En URI na vrstico"

    Za razliko od ponudnikov, ki pričakujejo seznam ločen z vejicami, polje OneLogin **Redirect URI's** sprejme en URI na vrstico.

---

## Korak 3: Nastavite tip aplikacije in metodo overjanja

1. Odprite zavihek **SSO**
2. Potrdite, da je **Application Type** *Web*
3. Nastavite **Token Endpoint → Authentication Method** na *POST* (`client_secret_post`) ali *Basic* (`client_secret_basic`)

!!! warning "Ne izberite None"

    Nastavitev metode overjanja na *None* naredi aplikacijo javnega odjemalca brez skrivnosti, in izmenjava kode na digna backendu bo zavrnjena. Tako POST kot Basic delujeta.

---

## Korak 4: Zberite poverilnice

Še vedno na zavihku **SSO**:

- **Client ID** → postane `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → postane `DIGNA_OIDC_CLIENT_SECRET` (kliknite **Show client secret**)

Stran prikazuje tudi **Issuer URL**, ki potrjuje discovery URL v naslednjem koraku.

---

## Korak 5: Dodelite uporabnike

1. Odprite zavihek **Access**
2. Dodajte vloge ali skupine, katerih člani smejo uporabljati digna
3. Kliknite **Save**

!!! note "Ne dodeljeni uporabniki so po prijavi zavrnjeni"

    Kot pri večini ponudnikov, OneLogin najprej overi uporabnika in šele nato preveri upravičenost. Nedodeljen uporabnik se uspešno prijavi in je nato zavrnjen, kar izgleda kot napaka digna namesto odločitev nadzora dostopa.

---

## Korak 6: Sestavite Discovery URL

Zamenjajte vašo OneLogin poddomeno:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Na primer:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 je različica API-ja"

    Trenutna OIDC implementacija OneLogin živi pod `/oidc/2/`. Starejša dokumentacija prikazuje `/oidc/` brez različice, kar kaže na upokojeno prvo različico. Če niste prepričani, preverite **Issuer URL** na zavihku SSO — discovery URL je issuer plus `/.well-known/openid-configuration`.

---

## Korak 7: Konfigurirajte digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Prijava z OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Ključ `key` v obeh datotekah mora biti enak — tukaj `onelogin`.

---

## Korak 8: Testiranje

Znova zaženite backend in spletni strežnik, nato odprite nadzorno ploščo. Celoten kontrolni seznam najdete v [Preizkušanje prijave](overview.md#testing-login).

---

## Odpravljanje težav z OneLogin

### redirect_uri did not match

Callback URL manjka v **Configuration → Redirect URI's**, ali so vnosi ločeni z vejicami namesto z novimi vrsticami.

### invalid_client at the Token Step

**Token Endpoint → Authentication Method** je nastavljen na *None*, ali pa je klientska skrivnost v `config.toml` zastarela. Razkrijte skrivnost na zavihku **SSO** in primerjajte.

### Aplikacija se ne prikaže uporabnikom

Nobenemu vlogi ali skupini ni dodeljen dostop na zavihku **Access**.

### 404 na Discovery URL

Poddomena je napačna, ali pa URL izpušča `/oidc/2/`. Primerjajte z **Issuer URL** na zavihku SSO.

---

## Glej tudi

- [Pregled Single Sign-On](overview.md) — referenca konfiguracije, testiranje in splošno odpravljanje težav
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)