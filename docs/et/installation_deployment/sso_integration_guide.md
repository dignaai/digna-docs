---
title: Single Sign-On (SSO) integratsiooni juhend | digna dokumentatsioon
description: Samm-sammult juhend Single Sign-On (SSO) konfigureerimiseks digna jaoks, kasutades OpenID Connect (OIDC). Käsitleb juhtpaneeli ja backend'i seadistust, testimist, tõrkeotsingut ning toetatud identiteedipakkujaid nagu Microsoft Entra ID, Google Workspace ja Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - oidc integration
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integration
  - enterprise authentication
lang: et
robots: index, follow
og_title: digna Single Sign-On (SSO) integratsiooni juhend
og_description: Konfigureeri Single Sign-On digna jaoks, kasutades OpenID Connecti. Samm-sammuline seadistus Microsoft Entra ID, Google Workspace, Okta ja teiste OIDC-ühilduvate identiteedipakkujate jaoks.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On Integratsiooni juhend

---

## Sisukord

1. [Sissejuhatus ja ülevaade](#introduction-and-overview)
2. [Seadistusetapid](#configuration-steps)
3. [Juhtpaneeli konfiguratsioon](#dashboard-configuration)
4. [Backend'i konfiguratsioon](#backend-configuration)
5. [Sisselogimise testimine](#testing-login)
6. [Tõrkeotsing](#troubleshooting)
7. [Toetatud pakkujad](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

See juhend annab samm-sammult juhised Single Sign-On (SSO) integreerimiseks digna platvormiga, kasutades **OpenID Connect (OIDC)**.

### Mis on SSO?

Single Sign-On võimaldab kasutajatel logida digna'sse turvaliselt nende ettevõtte volitustega läbi väliste identiteedipakkujate. Kasutajad saavad autentida end oma korporatiivsete volitustega, selle asemel et hallata eraldi digna paroole.

### Kuidas see töötab

SSO digna's on rakendatud kasutades OIDC protokolli. Mitut identiteedipakkujat saab seadistada paralleelselt, muutes kahte põhilist konfiguratsioonifaili:

- **`dashboard_config.toml`** — juhib frontendi sisselogimise liidest
- **`config.toml`** — konfigureerib backend'i OIDC ühendusi

### Toetatud pakkujad {: #supported-providers-overview }

Selles juhendis on näited **Microsofti** ja **Google'i** kasutamisest, kuid **iga OIDC-ühilduv pakkuja** on sama struktuuri järgides integreeritav.

Levinud OIDC pakkujate hulka kuuluvad:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Muud OIDC-ühilduvad identiteedipakkujad

---

## Seadistusetapid {: #configuration-steps }

SSO seadistamine nõuab kahe faili uuendamist. See jaotis selgitab, kuidas igaüht konfigureerida.

### Konfiguratsioonifailide ülevaade

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontendi sisselogimise liides |
| **config.toml** | `/config.toml` | Backend'i OIDC ühendused |

Mõlemad failid peavad olema seadistatud, et SSO korralikult töötaks.

---

## Juhtpaneeli konfiguratsioon {: #dashboard-configuration }

### Faili asukoht

```
dashboard/dashboard_config.toml
```

### Samm 1: Lisa OIDC pakkujad

Lisa kirjed `[[login.oidc]]` massiivi iga identiteedipakkuja jaoks, keda soovid toetada.

**Näide Microsofti ja Google'i kohta:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Samm 2: Konfigureeri sisselogimisvalikud

Määra, kas paroolipõhine sisselogimine peaks olema lubatud:

```toml
[login]
usePassword = true
```

### Konfiguratsiooniparameetrid

#### `[[login.oidc]]` sektsioon

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Unikaalne identifikaator OIDC ühenduse jaoks (peab vastama `config.toml`-is olevale võtmele) |
| `label` | string | Yes | Tekst, mis kuvatakse sisselogimisnupul (nt "Login with Microsoft") |

#### `[login]` sektsioon

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Lubab paroolipõhist sisselogimist SSO kõrval |

### usePassword mõistmine

**Kui `usePassword = true`:**
- Sisselogimisekraanil kuvatakse SSO nupud (nt "Login with Microsoft")
- Sisselogimisekraanil kuvatakse ka kasutajanime ja parooli väljad
- Kasutajad saavad autentida mõlemal meetodil
- Lubab hübriidseadistusi, kus mõned kasutajad kasutavad SSO-d ja teised paroole

**Kui `usePassword = false` (või jäetud välja):**
- Sisselogimisekraanil kuvatakse ainult SSO nuppe
- Ühtegi kasutajanime/parooli välja ei kuvata
- Aineteid ainult OIDC autentimine on võimalik

> **Näpunäide**
>
> Paroolipõhine sisselogimine on saadaval ainult kasutajatele, kes loodi parooliga kasutades käsku `digna user add` või läbi juhtpaneeli.

### Täielik näide

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend'i konfiguratsioon {: #backend-configuration }

### Faili asukoht

```
/config.toml
```

(Root digna installatsiooni kataloog)

### Samm 1: Lisa OIDC pakkujate sektsioonid

Igal pakkujal peab olema pühendatud `[oidc.<key>]` sektsioon. Võti peab vastama `dashboard_config.toml`-is määratletud `key`-le.

### Microsofti konfiguratsioon

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google'i konfiguratsioon

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfiguratsiooniparameetrid

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Klientide ID identiteedipakkujalt | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Klientide salajane võti identiteedipakkujalt | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Tagasi suunamise URL pärast autentimist | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC konfiguratsiooni lõpp-punkt | `https://login.microsoftonline.com/...` |

> **Tähtis**
>
> Asenda kohatäited (`<client_id>`, `<client_secret>`, `<tenant_id>`) tegelike volitustega, mis saadakse sinu identiteedipakkuja arendajapaneelilt.

### Redirect URI

Redirect URI peab olema sama, mis sinu identiteedipakkuja konfiguratsioonis:

```
http://localhost:5173/oidc/callback
```

Kui digna majutatakse teisel domeenil, uuenda vastavalt:
- Local: `http://localhost:5173/oidc/callback`
- Production: `https://digna.yourdomain.com/oidc/callback`

### Täielik näide

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Sisselogimise testimine {: #testing-login }

Pärast konfiguratsiooni lõpetamist kontrolli, et SSO töötab korrektselt.

### Eeltestimise kontrollnimekiri

Enne testimist veendu, et:

- [ ] `dashboard_config.toml` on värskendatud OIDC pakkujate osas
- [ ] `config.toml` on värskendatud OIDC volitustega
- [ ] Mõlemad failid on salvestatud
- [ ] Volitused on õiged (client ID, client secret)
- [ ] Redirect URI vastab sinu juurutuse URL-ile
- [ ] Identiteedipakkuja rakendus on konfigureeritud redirect URI-ga

### Testimise sammud

#### Samm 1: Taaskäivita teenused

Taaskäivita digna backend ja veebiserver, et muudatused rakenduksid.

**Kui jookseb Windowsi teenusena:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Kui jookseb käsitsi:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Kui kasutad IIS-i või Tomcat'i:**
Taaskäivita oma veebiserveri teenus.

#### Samm 2: Ava juhtpaneel

Ava digna juhtpaneel brauseris:

```
http://localhost:5173
```

(või sinu konfigureeritud juhtpaneeli URL)

#### Samm 3: Kinnita sisselogimisnupud

Kontrolli, et iga seadistatud pakkuja nupp oleks nähtav:

- Peaks olema nähtav "Login with Microsoft" nupp
- Peaks olema nähtav "Login with Google" nupp
- (Kui usePassword = true) Peaks olema nähtavad kasutajanime/parooli väljad

Kui nuppe ei kuvata:
- Kontrolli, et `dashboard_config.toml` on salvestatud
- Kontrolli, et juhtpaneeli teenus taaskäivitas
- Kontrolli brauseri konsooli (F12) vigade osas

#### Samm 4: Testi SSO sisselogimist

Klõpsa ühel SSO nupul (nt "Login with Microsoft"):

1. Sind suunatakse identiteedipakkuja sisselogimislehele
2. Logi sisse oma ettevõtte volitustega
3. Sind suunatakse tagasi digna'sse
4. Sa oled sisselogitud digna'sse

#### Samm 5: Kinnita kasutaja loomine

Pärast edukat SSO sisselogimist:

- Kasutaja peaks automaatselt loodama saama digna's
- Kasutaja peaks olema sisse logitud
- Kasutaja profiilis peaksid olema nähtavad sinu identiteedipakkuja andmed
- Sa peaksid nägema digna juhtpaneeli

#### Samm 6: Testi parooliga sisselogimist (kui lubatud)

Kui `usePassword = true`:

1. Logi ennast välja digna's
2. Sisselogimislehel sisesta kasutajanimi ja parool
3. Sa peaksid suutma sisselogida parooli abil

---

## Tõrkeotsing {: #troubleshooting }

### Sisselogimisnupud ei ilmu

**Sümptomid:**
- OIDC sisselogimisnupud ei ilmu sisselogimislehel
- Näidatakse ainult paroolivälju (kui usePassword = true)

**Põhjused ja lahendused:**
1. Kontrolli, et `dashboard_config.toml` asub `dashboard/` kataloogis
2. Veendu, et `[[login.oidc]]` sektsioonid on olemas ja süntaks õige
3. Taaskäivita juhtpaneeli teenus
4. Tühjenda brauseri vahemälu (Ctrl+Shift+Delete või Cmd+Shift+Delete)
5. Kontrolli brauseri konsooli (F12 → Console tab) vigade jaoks

---

### Redirect URI sobimatusviga

**Sümptomid:**
- Pärast SSO nupu klõpsamist ilmub viga "redirect_uri mismatch"
- Viga "The redirect URI is not registered"

**Põhjused ja lahendused:**
1. Kontrolli, et `DIGNA_OIDC_REDIRECT_URI` `config.toml`-is on õige
2. Veendu, et redirect URI on registreeritud identiteedipakkuja seadetes
3. Veendu, et mõlemad kasutavad identset URL-i (sh protokoll, domeen, path)
4. Kontrolli trükivigu redirect URI-s
5. Kui kasutad HTTPS-i, veendu, et sertifikaat on kehtiv

---

### Vigased kliendivolitused

**Sümptomid:**
- Viga "Invalid client ID or secret"
- Autentimine ebaõnnestub volituste veaga

**Põhjused ja lahendused:**
1. Kontrolli, et `DIGNA_OIDC_CLIENT_ID` ja `DIGNA_OIDC_CLIENT_SECRET` on õiged
2. Veendu, et pole lisatühikuid ega ebasobilikke märke
3. Kontrolli, et volitused pole aegunud ega tagasi kutsutud
4. Taaskäivita backend teenus pärast konfiguratsiooni uuendust
5. Kontrolli identiteedipakkuja konsooli, et kinnitada volituste aktiivsus

---

### Sisselogimine hangub või aegub

**Sümptomid:**
- SSO nupu klõpsamisel ei juhtu midagi
- Mõne sekundi pärast aegumine
- Brauser näitab "Failed to connect" või sarnast teadet

**Põhjused ja lahendused:**
1. Veendu, et digna backend töötab: `digna repo check`
2. Kontrolli võrguühendust identiteedipakkujaga
3. Veendu, et `DIGNA_OIDC_CONFIGURATION_URL` on ligipääsetav
4. Kontrolli tulemüüri reegleid, mis lubaksid väljaminevaid HTTPS ühendusi
5. Veendu, et backend ja juhtpaneel pääsevad üksteisele ligi

---

### Kasutajad ei loo automaatselt

**Sümptomid:**
- SSO sisselogimine õnnestub, kuid kasutajat ei loo digna's
- Pärast SSO sisselogimist tekib õiguste viga

**Põhjused ja lahendused:**
1. Veendu, et OIDC konfiguratsioon on õige
2. Kontrolli, et kasutajate õigused on korrektselt seadistatud
3. Vaata digna logisid vigade sõnumite jaoks
4. Taaskäivita backend teenus
5. Kui probleem püsib, võta ühendust support@digna.ai

---

## Toetatud pakkujad {: #supported-providers }

### Testitud ja toetatud

Järgnevad OIDC pakkujad on testitud ja on teadaolevalt töökorras:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Muud OIDC pakkujad

Iga pakkuja, mis toetab OpenID Connecti, on integreeritav. Vajalikud andmed:

- Client ID
- Client secret
- OpenID konfiguratsiooni URL (tavaliselt `/.well-known/openid-configuration`)
- Toetatud skoopid (tavaliselt `openid profile email`)

Võta ühendust support@digna.ai, kui vajad abi konkreetse pakkuja integreerimisel.

---

## Parimad tavad

DO:
- Kasuta tootmiskeskkonnas HTTPS-i (mitte HTTP)
- Hoia kliendisaladusi turvaliselt (kasuta keskkonnamuutujad, kui võimalik)
- Keera salajasi võtmeid perioodiliselt
- Testi esmalt mitte-tootmiskeskkonnas
- Dokumenteeri, millised pakkujad on konfigureeritud
- Jälgi sisselogimislogisid ebatavalise tegevuse jaoks
- Hoia identiteedipakkuja konfiguratsioon sünkroonis digna seadistusega

DON'T:
- Ära hoia kliendisaladusi versioonihalduses
- Ära kasuta HTTP redirect URI-sid tootmises
- Ära konfigureeri mitut pakkujat sama võtmega
- Ära jäta vaikimisi/testvolitusi tootmisesse
- Ära avalikusta konfiguratsioonifaile, mis sisaldavad salajasi võtmeid
- Ära segi ajada arendus- ja tootmisvolitusi

---

## Tugi

Vajad abi SSO seadistusega?

- **E-post:** support@digna.ai
- **Dokumentatsioon:** https://docs.digna.ai
- **Veebileht:** https://www.digna.ai

---

**Viimati uuendatud:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
