---
title: Google Workspace SSO – Ühekordne sisselogimine (Single Sign-On) | digna dokumentatsioon
description: Seadistage digna jaoks Single Sign-On Google Workspace'i abil, kasutades OpenID Connecti — OAuth nõusoleku ekraan, OAuth kliendi ID, lubatud suunamis-URI-d ja vastav digna konfiguratsioon.
image: /assets/logo_square.png
keywords: digna sso, google workspace sso, google oidc, oauth nõusoleku ekraan, openid connect, ettevõtte autentimine
---

# Seadista SSO Google Workspace'iga

Google'i identiteediplatvorm vastab OIDC standardile ja kasutab iga kliendi jaoks ühte, hästi teadaolevat avastuse (discovery) URL-i, nii et ainukesed organisatsioonipõhised väärtused on klient ID ja secret.

See juhend käsitleb **Google'i poolt tehtavat**: OAuth kliendi loomist ja väärtuste kogumist, mida digna vajab. digna pool — `dashboard_config.toml`, testimine ja tõrkeotsing — on sama iga pakkuja puhul ning on kirjeldatud jaotises [Single Sign-On Overview](overview.md).

---

## Enne alustamist

| Nõue | Märkused |
|---|---|
| **Google Cloud project** | Mis tahes projekt samas organisatsioonis kui teie Workspace domeen |
| **Role** | Editor või Owner projektis |
| **digna redirect URI** | URL, kuhu kasutajad pärast sisselogimist tagasi suunatakse, nt `https://digna.yourdomain.com/oidc/callback` |

---

## 1. samm: OAuth nõusoleku ekraani seadistamine

Google ei väljastata mandaate enne, kui nõusoleku ekraan on loodud.

1. Avage [Google Cloud Console](https://console.cloud.google.com) ja valige oma projekt
2. Minge **APIs & Services → OAuth consent screen**
3. Valige kasutajatüüp:
   - **Internal** — ainult teie Workspace domeenis olevad kontod saavad sisse logida. Soovitatav.
   - **External** — mis tahes Google'i konto võib proovida sisse logida.
4. Täitke rakenduse nimi, kasutajatoe e-posti aadress ja arendaja kontakt e-posti aadress
5. **Scopes** sammul lisage `openid`, `.../auth/userinfo.email` ja `.../auth/userinfo.profile`
6. Salvesta

!!! warning "Väliseid rakendusi tuleb avaldada"

    **External** tüüpi nõusoleku ekraan algab *Testing* olekus, kus ainult testkasutajate nimekirja otseselt lisatud kontod saavad sisselogimise lõpetada. Kõik teised näevad sõnumit "digna has not completed the Google verification process". Lülitage rakendus kas **In production** olekusse alal **Publishing status**, või kasutage **Internal** — see ei oma sellist piirangut ja on õige valik ainult Workspace'i kasutuse puhul.

---

## 2. samm: OAuth kliendi loomine

1. Minge **APIs & Services → Credentials**
2. Klõpsake **Create Credentials → OAuth client ID**
3. Määrake **Application type** väärtuseks **Web application**
4. Andke sellele nimi, nt `digna`
5. Jaotises **Authorized redirect URIs** klõpsake **Add URI** ja sisestage:

```
https://digna.yourdomain.com/oidc/callback
```

6. Klõpsake **Create**

!!! note "Lubatud JavaScript-päritolud pole vajalikud"

    digna vahetab autoriseerimiskoodi tagaosas (backend), mitte brauseris, seega võib välja **Authorized JavaScript origins** tühjaks jätta. Ainult redirect URI on oluline.

---

## 3. samm: mandaadi kogumine

Pärast loomist kuvatav dialoog näitab:

- **Client ID** — lõpeb `.apps.googleusercontent.com` → muutub `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → muutub `DIGNA_OIDC_CLIENT_SECRET`

Mõlemat on hiljem võimalik tagasi vaadata mandaadi detailide lehelt, erinevalt enamikust teistest pakkujatest.

---

## 4. samm: avastuse (Discovery) URL

Google kasutab kõigi klientide jaoks ühte avastuse URL-i — asendamist pole vaja:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## 5. samm: digna seadistamine

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

Mõlemas failis olev `key` peab kattuma — siin `google`.

---

## 6. samm: Testimine

Taaskäivitage backend ja veebiserver, seejärel avage dashboard. Täismahus kontrolleirja leiate jaotisest [Testing Login](overview.md#testing-login).

---

## Tõrkeotsing Google Workspace'i jaoks

### Error 400: redirect_uri_mismatch

`DIGNA_OIDC_REDIRECT_URI`-s olev URI ei kuulu **Authorized redirect URIs** nimekirja või erineb lõputähtaja (tühik, kaldkriips) või skeemi poolest. Google'i vealeht kuvab vastu võetud URI — võrrelge seda tähemärgipõhiselt registreeritud URI-ga.

### This App Is Blocked / Has Not Completed Verification

Nõusoleku ekraan on **External** ja on endiselt *Testing* olekus. Avaldage see või lülitage rakendus **Internal**-iks.

### Access Blocked: Authorization Error

Sisselogimist püüab teha konto, mis on väljaspool teie Workspace domeeni, samal ajal kui nõusoleku ekraan on **Internal**. See on ootuspärane käitumine — Internal tüüpi rakendused võtavad vastu ainult organisatsiooni kontosid.

### Muutuste levik võtab mitu minutit

Google levitab mandaadi- ja nõusolekuekraani muudatusi asünkroonselt. Väsimuselt lisatud redirect URI võib hakata kehtima alles mõne minuti pärast; kui muudatus näib ignoreeritavat, oodake ja proovige uuesti enne edasise veaotsingu alustamist.

---

## Vaata ka

- [Single Sign-On Overview](overview.md) — konfiguratsiooni viide, testimine ja üldine tõrkeotsing
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)