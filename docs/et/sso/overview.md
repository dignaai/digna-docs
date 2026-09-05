---
title: Sisselogimine ühe kontoga (SSO) — ülevaade | digna Documentation
description: Kuidas Single Sign-On töötab dignas, kasutades OpenID Connecti (OIDC). Katab juhtpaneeli ja backend'i seadistuse, testimise, tõrkeotsingu ning lingid iga-pakkuja juhenditele Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne ja AD FS jaoks.
image: /assets/logo_square.png
keywords:
  - digna sso
  - ühe-kontoga sisselogimine
  - oidc integratsioon
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - okta integratsioon
  - ettevõtte autentimine
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Sisselogimine ühe kontoga (SSO) — ülevaade

---

## Sisukord

1. [Sissejuhatus ja ülevaade](#introduction-and-overview)
2. [Pakkujate juhendid](#provider-guides)
3. [Seadistusastmed](#configuration-steps)
4. [Juhtpaneeli seadistus](#dashboard-configuration)
5. [Backend'i seadistus](#backend-configuration)
6. [Sisselogimise testimine](#testing-login)
7. [Tõrkeotsing](#troubleshooting)
8. [Toetatud pakkujad](#supported-providers)

---

## Sissejuhatus ja ülevaade {: #introduction-and-overview }

See juhend annab samm-sammulised juhised Single Sign-On (SSO) integreerimiseks digna platvormiga, kasutades **OpenID Connecti (OIDC)**.

### Mis on SSO?

Single Sign-On võimaldab kasutajatel turvaliselt dignasse sisse logida oma ettevõtte volitustega läbi välist identiteedipakkujat. Kasutajad saavad autentida end ettevõtte konto andmetega, selle asemel et hallata eraldi digna paroole.

### Kuidas see töötab

SSO on dignas rakendatud OIDC protokolli abil. Mitut identiteedipakkujat saab konfigureerida paralleelselt, muutes kahte peamist konfiguratsioonifaili:

- **`dashboard_config.toml`** — juhtpaneeli sisselogimise liidese juhtelemendid
- **`config.toml`** — backend'i OIDC ühenduste seadistus

### Toetatud pakkujad {: #supported-providers-overview }

Selles juhendis kasutatud näited kasutavad **Microsofti** ja **Google'i**, kuid **iga OIDC-ga ühilduv pakkuja** saab integreerida sama struktuuri järgides.

---

## Pakkujate juhendid {: #provider-guides }

Iga pakkuja jaoks on vaja samu nelja väärtust — client ID, client secret, redirect URI ja discovery URL — kuid igaüks paigutab need oma admin-konsoolis eri kohta ning mitmel on konkreetne samm, mida teised ei nõua. Allpool olevad juhendid katavad selle osa; see leht katab digna poole, mis on kõigi puhul identselt sama.

| Pakkuja | Juhend | Tasub teada |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Self-hostitud; ainus siin olev pakkuja, kus te kontrollite tokeniteenust |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Discovery URL on tenant-spetsiifiline ja kohandatud domeenid muudavad seda |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Nõusoleku ekraan peab enne mitte-testkasutajate sisselogimist avalikustama |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Self-hostitud; discovery URL on realm-põhine |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID ilmub discovery URL-i; salajased võtmed aeguvad |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Autoriseerimisteenuse valik muudab discovery URL-i |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | OIDC rakenduse tüüp tuleb valida loomisel ja seda ei saa muuta |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Keskkonna ID ilmub discovery URL-i |

Iga muu OIDC-ga ühilduv pakkuja töötab samamoodi — vaata [Other OIDC Providers](#supported-providers).

---

## Seadistusastmed {: #configuration-steps }

SSO seadistamine nõuab kahe faili uuendamist. See jaotis selgitab, kuidas iga faili seadistada.

### Konfiguratsioonifailide ülevaade

| Fail | Asukoht | Eesmärk |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Juhtpaneeli sisselogimise liides |
| **config.toml** | `/config.toml` | Backend'i OIDC ühendused |

Mõlemad failid peavad olema SSO korralikult töötamiseks seadistatud.

---

## Juhtpaneeli seadistus {: #dashboard-configuration }

### Faili asukoht

```
dashboard/dashboard_config.toml
```

### Samm 1: OIDC pakkujate lisamine

Lisa kirjed `[[login.oidc]]` massiivi iga identiteedipakkuja jaoks, keda soovid toetada.

**Näide Microsofti ja Google'iga:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Logi sisse Microsofti abil"

[[login.oidc]]
key = "google"
label = "Logi sisse Google'i abil"
```

### Samm 2: Sisselogimise valikute seadistamine

Määra, kas paroolipõhine sisselogimine peaks olema lubatud:

```toml
[login]
usePassword = true
```

### Konfiguratsiooniparameetrid

#### `[[login.oidc]]` sektsioon

| Parameeter | Tüüp | Nõutav | Kirjeldus |
|---|---|---|---|
| `key` | string | Jah | OIDC ühenduse unikaalne identifikaator (peab vastama config.toml-is olevale key-le) |
| `label` | string | Jah | Tekst, mis kuvatakse sisselogimisnupul (nt "Logi sisse Microsofti abil") |

#### `[login]` sektsioon

| Parameeter | Tüüp | Vaikeväärtus | Kirjeldus |
|---|---|---|---|
| `usePassword` | boolean | false | Luba paroolipõhist sisselogimist lisaks SSO-le |

### usePassword tähendus

**Kui `usePassword = true`:**
- Sisselogimise ekraanil kuvatakse SSO nupud (nt "Logi sisse Microsofti abil")
- Sisselogimise ekraanil kuvatakse ka kasutajanime ja parooli väljad
- Kasutajad saavad autentida mõlemal viisil
- Võimaldab hübriidset ülesehitust, kus mõned kasutajad kasutavad SSO-d ja teised paroole

**Kui `usePassword = false` (või jäetud välja):**
- Sisselogimise ekraanil kuvatakse ainult SSO nupud
- Ei ole kasutajanime/parooli välju
- Saadaval on ainult OIDC autentimine

!!! tip "Vihje"

    Paroolipõhine sisselogimine on saadaval ainult kasutajatele, kes loodi paroolidega, kasutades käsku `digna user add` või juhtpaneeli kaudu.

### Täielik näide

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Logi sisse Microsofti abil"

[[login.oidc]]
key = "google"
label = "Logi sisse Google'i abil"

[[login.oidc]]
key = "okta"
label = "Logi sisse Okta abil"
```

---

## Backend'i seadistus {: #backend-configuration }

### Faili asukoht

```
/config.toml
```

(Põhiskataloog digna installatsioonis)

### Samm 1: Lisa OIDC pakkujate sektsioonid

Iga pakkuja jaoks peab olema pühendatud `[oidc.<key>]` sektsioon. Key peab vastama `dashboard_config.toml`-is määratud `key`-le.

### Microsofti seadistus

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google'i seadistus

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfiguratsiooniparameetrid

| Parameeter | Tüüp | Nõutav | Kirjeldus | Näide |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Jah | Client ID identiteedipakkujalt | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Jah | Client secret identiteedipakkujalt | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Jah | Callback URL pärast autentimist | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Jah | OIDC konfiguratsiooni endpoint | `https://login.microsoftonline.com/...` |

!!! warning "Tähtis"

    Asenda kohatäite väärtused (`<client_id>`, `<client_secret>`, `<tenant_id>`) tegelike volitustega oma identiteedipakkuja arendajaportaalist.

### Redirect URI

Redirect URI peab olema sama, mis sinu identiteedipakkuja konfiguratsioonis:

```
http://localhost:5173/oidc/callback
```

Kui digna on hostitud teisel domeenil, uuenda vastavalt:
- Kohalik: `http://localhost:5173/oidc/callback`
- Tootmine: `https://digna.yourdomain.com/oidc/callback`

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

Pärast seadistuse lõpetamist kinnita, et SSO töötab õigesti.

### Enne testimist kontrollnimekiri

Enne testimist veendu, et:

- [ ] `dashboard_config.toml` on uuendatud OIDC pakkujate võrra
- [ ] `config.toml` on uuendatud OIDC volitustega
- [ ] Mõlemad failid on salvestatud
- [ ] Volitused on õiged (client ID, client secret)
- [ ] Redirect URI vastab sinu juurutuse URL-ile
- [ ] Identiteedipakkuja rakendus on konfigureeritud redirect URI-ga

### Testimise sammud

#### Samm 1: Teenuste taaskäivitamine

Taaskäivita digna backend ja veebiserver, et muudatused jõustuksid.

**Kui töötab teenusena Windowsis:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Kui töötab teenusena Linuxis või macOS-is:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Kui jookseb käsitsi:**
```bash
digna serve --address localhost --port 8082
```

**Taaskäivita ka veebiserver** — IIS või Tomcat Windowsis, nginx või Apache Linuxis ja macOS-is.

#### Samm 2: Ava juhtpaneel

Ava digna juhtpaneel brauseris:

```
http://localhost:5173
```

(või sinu konfigureeritud juhtpaneeli URL)

#### Samm 3: Kontrolli sisselogimisnuppe

Kontrolli, et sisselogimisnupud kuvatakse iga konfigureeritud pakkuja jaoks:

- Peaks olema näha nupp "Logi sisse Microsofti abil"
- Peaks olema näha nupp "Logi sisse Google'i abil"
- (Kui usePassword = true) Peaks olema näha kasutajanime/parooli väljad

Kui nuppe ei paista:
- Kontrolli, et `dashboard_config.toml` on salvestatud
- Kontrolli, et juhtpaneeli teenus on taaskäivitatud
- Kontrolli brauseri konsooli (F12) vigade jaoks

#### Samm 4: Testi SSO sisselogimist

Klõpsa ühte SSO nupudest (nt "Logi sisse Microsofti abil"):

1. Sind suunatakse identiteedipakkuja sisselogimise lehele
2. Logi sisse oma ettevõtte volitustega
3. Sind suunatakse tagasi dignasse
4. Sa peaksid olema dignasse sisse logitud

#### Samm 5: Kontrolli kasutaja loomist

Pärast õnnestunud SSO sisselogimist:

- Kasutaja peaks automaatselt looma saama dignas
- Kasutaja peaks olema sisse logitud
- Kasutaja profiilis peaks ilmnema su identiteedipakkuja andmed
- Sa peaksid nägema digna juhtpaneeli

#### Samm 6: Testi parooli-põhist sisselogimist (kui lubatud)

Kui `usePassword = true`:

1. Logi dignast välja
2. Sisselogimise lehel sisesta kasutajanimi ja parool
3. Sa peaksid saama parooliga sisse logida

---

## Tõrkeotsing {: #troubleshooting }

### Sisselogimisnupud ei ilmu

**Sümptomid:**
- OIDC sisselogimise nupud pole sisselogimislehel nähtavad
- Näed ainult paroolivälju (kui usePassword = true)

**Põhjused & lahendused:**
1. Kontrolli, et `dashboard_config.toml` on `dashboard/` kataloogis
2. Veendu, et `[[login.oidc]]` sektsioonid on olemas ja süntaks õige
3. Taaskäivita juhtpaneeli teenus
4. Tühjenda brauseri vahemälu (Ctrl+Shift+Delete või Cmd+Shift+Delete)
5. Kontrolli brauseri konsooli (F12 → Console) vigade jaoks

---

### Redirect URI sobimatusviga

**Sümptomid:**
- Pärast SSO nupule klõpsamist ilmub viga "redirect_uri mismatch"
- Viga "The redirect URI is not registered"

**Põhjused & lahendused:**
1. Kontrolli, et `DIGNA_OIDC_REDIRECT_URI` `config.toml`-is on õige
2. Veendu, et redirect URI on registreeritud identiteedipakkuja seadetes
3. Veendu, et mõlemad kasutavad identselt sama URL-i (sh protokoll, domeen, path)
4. Kontrolli kirjavigu redirect URI-s
5. Kui kasutad HTTPS-i, veendu, et sertifikaat on kehtiv

---

### Vale kliendi volituste viga

**Sümptomid:**
- Viga "Invalid client ID or secret"
- Autentimine ebaõnnestub volituste veaga

**Põhjused & lahendused:**
1. Kontrolli, et `DIGNA_OIDC_CLIENT_ID` ja `DIGNA_OIDC_CLIENT_SECRET` on õiged
2. Veendu, et ees/tekohti ei ole lisaruume ega erimärke
3. Kontrolli, et volitused pole aegunud või tagasivõetud
4. Taaskäivita backend teenus pärast konfiguratsiooni uuendamist
5. Kontrolli identiteedipakkuja konsoolist, et volitused on aktiivsed

---

### Sisselogimine hangub või aegub

**Sümptomid:**
- SSO nupule klõpsates ei juhtu midagi
- Mitme sekundi pärast aegub
- Brauser näitab "Failed to connect" või sarnast

**Põhjused & lahendused:**
1. Veendu, et digna backend töötab: `digna repo check`
2. Kontrolli võrguühendust identiteedipakkujaga
3. Veendu, et `DIGNA_OIDC_CONFIGURATION_URL` on ligipääsetav
4. Kontrolli tulemüüri reegleid, mis lubavad väljaminevaid HTTPS-ühendusi
5. Veendu, et backend ja juhtpaneel saavad teineteisele ligi

---

### Kasutajad ei looda automaatselt

**Sümptomid:**
- SSO sisselogimine õnnestub, kuid kasutajat ei looda dignas
- Pärast SSO sisselogimist tekib luba puudub viga

**Põhjused & lahendused:**
1. Kontrolli, et OIDC konfiguratsioon on korrektne
2. Kontrolli kasutajate õigusi ja sätted
3. Vaata digna logisid veateadete osas
4. Taaskäivita backend teenus
5. Kui probleem püsib, võta ühendust support@digna.ai

---

## Toetatud pakkujad {: #supported-providers }

### Testitud ja toetatud

Järgnevad OIDC pakkujad on testitud ja teadaolevalt töötavad:

| Pakkuja | Konfiguratsiooni URL | Seadistuse juhend |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Muud OIDC pakkujad

Iga pakkuja, mis toetab OpenID Connecti, saab integreerida. Nõutav info:

- Client ID
- Client secret
- OpenID konfiguratsiooni URL (tavaliselt `/.well-known/openid-configuration`)
- Toetatavad scopes (tavaliselt `openid profile email`)

Kui vajad abi konkreetse pakkuja integreerimisel, võta ühendust support@digna.ai.

---

## Parimad tavad

**TEE:**
- Kasuta tootmises HTTPS-i (mitte HTTP)
- Hoia client secret-id turvaliselt (kasuta keskkonnamuutujaid, kui võimalik)
- Rotatsiooni kaudu vaheta salajased võtmed perioodiliselt
- Testi esmalt mitte-tootmiskeskkonnas
- Dokumenteeri, millised pakkujad on konfigureeritud
- Jälgi sisselogimise logisid ebatavade avastamiseks
- Hoia identiteedipakkuja konfiguratsioon kooskõlas digna konfiguratsiooniga

**ÄRA:**
- Ära hoia client secret-e versioonikontrollis
- Ära kasuta tootmises HTTP redirect URI-sid
- Ära konfigureeri mitut pakkujat sama key-ga
- Ära jäta tootmises vaikimisi/testvolitusi
- Ära eksponeeri konfiguroodud faile, mis sisaldavad salajasi võtmeid
- Ära sega arendus- ja tootmiskasutajaid/volitusi

---

## Tugi

Vajate abi SSO seadistamisel?

- **E-post:** support@digna.ai
- **Dokumentatsioon:** https://docs.digna.ai
- **Veebileht:** https://www.digna.ai

---

**Viimati uuendatud:** 30. august 2026  
**Väljaanne:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**