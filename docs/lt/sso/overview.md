---
title: Vienkartinis prisijungimas (SSO) — apžvalga | digna dokumentacija
description: Kaip veikia vienkartinis prisijungimas (SSO) digna platformoje naudojant OpenID Connect (OIDC). Apima prietaisų skydelio ir serverio konfigūraciją, testavimą, trikčių šalinimą ir nuorodas į atskirus tiekėjų nustatymų vadovus Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne ir AD FS.
image: /assets/logo_square.png
keywords:
  - digna sso
  - vienkartinis prisijungimas
  - OIDC integracija
  - OpenID Connect
  - microsoft entra id
  - Azure AD SSO
  - google workspace sso
  - okta integration
  - įmonės autentifikacija
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Vienkartinis prisijungimas — apžvalga

---

## Turinys

1. [Įvadas ir apžvalga](#introduction-and-overview)
2. [Tiekėjų vadovai](#provider-guides)
3. [Konfigūracijos žingsniai](#configuration-steps)
4. [Prietaisų skydelio konfigūracija](#dashboard-configuration)
5. [Serverio konfigūracija](#backend-configuration)
6. [Prisijungimo testavimas](#testing-login)
7. [Trikčių šalinimas](#troubleshooting)
8. [Palaikomi tiekėjai](#supported-providers)

---

## Įvadas ir apžvalga {: #introduction-and-overview }

Šis vadovas pateikia žingsnis po žingsnio instrukcijas, kaip integruoti vienkartinį prisijungimą (SSO) su digna platforma naudojant **OpenID Connect (OIDC)**.

### Kas yra SSO?

Vienkartinis prisijungimas leidžia vartotojams saugiai prisijungti prie digna naudodami savo įmonės paskyras per išorinius identiteto tiekėjus. Vartotojai gali autentifikuotis naudodami korporacines paskyras vietoje atskirų digna slaptažodžių tvarkymo.

### Kaip tai veikia

SSO digna įgyvendinamas naudojant OIDC protokolą. Keli identiteto tiekėjai gali būti sukonfigūruoti lygiagrečiai, keičiant du pagrindinius konfigūracijos failus:

- **`dashboard_config.toml`** — valdo priekopos (frontend) prisijungimo sąsają
- **`config.toml`** — konfigūruoja serverio (backend) OIDC jungtis

### Palaikomi tiekėjai {: #supported-providers-overview }

Šio vadovo pavyzdžiai naudoja **Microsoft** ir **Google**, bet **bet koks OIDC suderinamas tiekėjas** gali būti integruotas laikantis tos pačios struktūros.

---

## Tiekėjų vadovai {: #provider-guides }

Kiekvienam tiekėjui reikia tų pačių keturių verčių — klientų ID, kliento slaptojo rakto, peradresavimo URI ir atradimo (discovery) URL — tačiau kiekvienas tiekėjas juos pateikia skirtingose administravimo konsolės vietose, ir keli turi tiekėjui specifinį žingsnį, kurio kiti neturi. Žemiau pateikti vadovai apima tą tiekėjo pusę; ši puslapio dalis apima digna konfigūraciją, kuri yra identiška visiems.

| Tiekėjas | Vadovas | Svarbu žinoti |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Savarankiškai talpinamas; vienintelis tiekėjas, kurio žetonų paslaugą valdote patys |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | Atrankos (discovery) URL yra priskiriamas nuominio lygiu, o pasirinktiniai domenai jį keičia |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | Leidimo ekranas turi būti paskelbtas, kad nepriskirti testiniai vartotojai galėtų prisijungti |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Savarankiškai talpinamas; atrankos URL yra priskiriamas realm’ui |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Nuominio ID matomas atrankos URL; slaptieji raktai gali pasibaigti |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Autorizacijos serverio pasirinkimas keičia atrankos URL |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | OIDC programos tipas turi būti pasirinktas kuriant ir to pakeisti negalima |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Aplinkos ID matomas atrankos URL |

Bet koks kitas OIDC suderinamas tiekėjas veikia taip pat — žr. [Other OIDC Providers](#supported-providers).

---

## Konfigūracijos žingsniai {: #configuration-steps }

SSO konfigūracija reikalauja atnaujinimų dviejuose failuose. Ši dalis paaiškina, kaip konfigūruoti kiekvieną iš jų.

### Konfigūracijų failų apžvalga

| Failas | Vieta | Paskirtis |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Priekopos (frontend) prisijungimo sąsaja |
| **config.toml** | `/config.toml` | Serverio (backend) OIDC jungtys |

Abu failai turi būti sukonfigūruoti, kad SSO veiktų tinkamai.

---

## Prietaisų skydelio konfigūracija {: #dashboard-configuration }

### Failo vieta

```
dashboard/dashboard_config.toml
```

### 1 žingsnis: pridėti OIDC tiekėjus

Pridėkite įrašus po masyvo `[[login.oidc]]` kiekvienam identiteto tiekėjui, kurį norite palaikyti.

**Pavyzdys su Microsoft ir Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### 2 žingsnis: sukonfigūruokite prisijungimo parinktis

Nurodykite, ar leisti prisijungimą naudojant slaptažodį:

```toml
[login]
usePassword = true
```

### Konfigūracijos parametrai

#### `[[login.oidc]]` sekcija

| Parametras | Tipas | Privalomas | Aprašymas |
|---|---:|---:|---|
| `key` | string | Taip | Unikalus OIDC jungties identifikatorius (turi sutapti su key config.toml) |
| `label` | string | Taip | Tekstas, rodomas prisijungimo mygtuke (pvz., "Login with Microsoft") |

#### `[login]` sekcija

| Parametras | Tipas | Numatytoji reikšmė | Aprašymas |
|---|---:|---:|---|
| `usePassword` | boolean | false | Leisti prisijungimą naudojant slaptažodį papildomai prie SSO |

### Ką reiškia usePassword

**Jei `usePassword = true`:**
- Prisijungimo ekrane rodomi SSO mygtukai (pvz., "Login with Microsoft")
- Taip pat rodomi vartotojo vardo ir slaptažodžio laukai
- Vartotojai gali autentifikuotis bet kuria iš šių metodų
- Leidžia hibridinį nustatymą, kai dalis vartotojų naudoja SSO, o kiti — slaptažodžius

**Jei `usePassword = false` (arba nepasirinkta):**
- Prisijungimo ekrane rodomi tik SSO mygtukai
- Vartotojo vardo/slaptažodžio laukų nėra
- Prieinama tik OIDC autentifikacija

!!! tip "Patarimas"

    Prisijungimas naudojant slaptažodį prieinamas tik vartotojams, kurie buvo sukurti su slaptažodžiais naudojant komandą `digna user add` arba per prietaisų skydelį.

### Pilnas pavyzdys

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

## Serverio konfigūracija {: #backend-configuration }

### Failo vieta

```
/config.toml
```

(Šakninis digna diegimo katalogas)

### 1 žingsnis: pridėti OIDC tiekėjų sekcijas

Kiekvienam tiekėjui turi būti atskira `[oidc.<key>]` sekcija. Key turi sutapti su `key`, apibrėžtu `dashboard_config.toml`.

### Microsoft konfigūracija

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google konfigūracija

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigūracijos parametrai

| Parametras | Tipas | Privalomas | Aprašymas | Pavyzdys |
|---|---:|---:|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Taip | Kliento ID iš identiteto tiekėjo | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Taip | Kliento slaptasis raktas iš identiteto tiekėjo | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Taip | Grįžimo (callback) URL po autentifikacijos | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Taip | OIDC konfigūracijos galinis taškas | `https://login.microsoftonline.com/...` |

!!! warning "Svarbu"

    Pakeiskite žymių reikšmes (`<client_id>`, `<client_secret>`, `<tenant_id>`) tikromis savo identiteto tiekėjo kūrėjo (developer) portalo reikšmėmis.

### Redirect URI

Peradresavimo (redirect) URI turi sutapti su jūsų identiteto tiekėjo konfigūracija:

```
http://localhost:5173/oidc/callback
```

Jei digna talpinama kitame domene, atnaujinkite atitinkamai:
- Vietiniam testavimui: `http://localhost:5173/oidc/callback`
- Gamybai (production): `https://digna.yourdomain.com/oidc/callback`

### Pilnas pavyzdys

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

## Prisijungimo testavimas {: #testing-login }

Baigus konfigūraciją, patikrinkite, ar SSO veikia teisingai.

### Prieš testavimą — kontrolinis sąrašas

Prieš testavimą įsitikinkite:

- [ ] `dashboard_config.toml` atnaujintas su OIDC tiekėjais
- [ ] `config.toml` atnaujintas su OIDC kredencialais
- [ ] Abu failai išsaugoti
- [ ] Kredencialai yra teisingi (client ID, client secret)
- [ ] Redirect URI atitinka jūsų diegimo URL
- [ ] Identiteto tiekėjo aplikacija sukonfigūruota su redirect URI

### Testavimo žingsniai

#### 1 žingsnis: perkraukite paslaugas

Perkraukite digna serverį ir žiniatinklio serverį, kad pritaikytumėte pakeitimus.

**Jei veikiate kaip paslauga Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Jei veikiate kaip paslauga Linux arba macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Jei veikiate rankiniu būdu:**
```bash
digna serve --address localhost --port 8082
```

**Taip pat perkraukite web serverį** — IIS arba Tomcat Windows sistemoje, nginx arba Apache Linux ir macOS.

#### 2 žingsnis: atidarykite prietaisų skydelį

Atidarykite digna prietaisų skydelį savo naršyklėje:

```
http://localhost:5173
```

(arba jūsų sukonfigūruotas prietaisų skydelio URL)

#### 3 žingsnis: patikrinkite prisijungimo mygtukus

Patikrinkite, ar kiekvienam sukonfigūruotam tiekėjui rodomi prisijungimo mygtukai:

- Turėtumėte matyti mygtuką "Login with Microsoft"
- Turėtumėte matyti mygtuką "Login with Google"
- (Jei usePassword = true) Turėtumėte matyti vartotojo vardo/slaptažodžio laukus

Jei mygtukų nematote:
- Patikrinkite, ar `dashboard_config.toml` išsaugotas
- Patikrinkite, ar prietaisų skydelio paslauga buvo perkrauta
- Patikrinkite naršyklės konsolę (F12) dėl klaidų

#### 4 žingsnis: išbandykite SSO prisijungimą

Spustelėkite vieną iš SSO mygtukų (pvz., "Login with Microsoft"):

1. Turėtumėte būti peradresuoti į identiteto tiekėjo prisijungimo puslapį
2. Prisijunkite naudodami savo įmonės kredencialus
3. Turėtumėte būti peradresuoti atgal į digna
4. Turėtumėte būti prisijungę prie digna

#### 5 žingsnis: patikrinkite vartotojo kūrimą

Po sėkmingo SSO prisijungimo:

- Vartotojas turėtų būti automatiškai sukurtas digna
- Vartotojas turėtų būti prisijungęs
- Vartotojo profilyje turėtų matytis jūsų identiteto tiekėjo informacija
- Turėtumėte matyti digna prietaisų skydelį

#### 6 žingsnis: išbandykite prisijungimą slaptažodžiu (jei įjungta)

Jei `usePassword = true`:

1. Atsijunkite iš digna
2. Prisijungimo puslapyje įveskite vartotojo vardą ir slaptažodį
3. Turėtumėte sugebėti prisijungti naudodami slaptažodį

---

## Trikčių šalinimas {: #troubleshooting }

### Prisijungimo mygtukai nerodomi

**Simptomai:**
- OIDC prisijungimo mygtukai nematomi prisijungimo puslapyje
- Matote tik slaptažodžio laukus (jei usePassword = true)

**Priežastys ir sprendimai:**
1. Patikrinkite, ar `dashboard_config.toml` yra `dashboard/` kataloge
2. Patikrinkite, ar `[[login.oidc]]` sekcijos yra ir sintaksė teisinga
3. Perkraukite prietaisų skydelio paslaugą
4. Išvalykite naršyklės talpyklą (Ctrl+Shift+Delete arba Cmd+Shift+Delete)
5. Patikrinkite naršyklės konsolę (F12 → Console tab) dėl klaidų

---

### Redirect URI neatitikimo klaida

**Simptomai:**
- Po SSO mygtuko paspaudimo gaunate klaidą apie "redirect_uri mismatch"
- Klaida "The redirect URI is not registered"

**Priežastys ir sprendimai:**
1. Patikrinkite, ar `DIGNA_OIDC_REDIRECT_URI` `config.toml` yra teisingas
2. Patikrinkite, ar redirect URI yra užregistruotas identiteto tiekėjo nustatymuose
3. Užtikrinkite, kad abu URL būtų identiški (įskaitant protokolą, domeną, kelią)
4. Patikrinkite dėl rašybos klaidų redirect URI
5. Jei naudojate HTTPS, įsitikinkite, kad sertifikatas galioja

---

### Neteisingi kliento kredencialai

**Simptomai:**
- Klaida "Invalid client ID or secret"
- Autentifikacija nepavyksta dėl kredencialų klaidos

**Priežastys ir sprendimai:**
1. Patikrinkite, ar `DIGNA_OIDC_CLIENT_ID` ir `DIGNA_OIDC_CLIENT_SECRET` yra teisingi
2. Įsitikinkite, kad nėra papildomų tarpų ar nespauktų simbolių
3. Patikrinkite, ar kredencialai nepasibaigę ir neanuliuoti
4. Po konfigūracijos atnaujinimo perkraukite serverio paslaugą
5. Patikrinkite identiteto tiekėjo konsolę, ar kredencialai aktyvūs

---

### Prisijungimas užstringa arba praeina laiko limitą

**Simptomai:**
- Paspaudus SSO mygtuką nieko nevyksta
- Praeina kelios sekundės ir gaunate laiko limitą
- Naršyklė rodo "Failed to connect" arba panašią klaidą

**Priežastys ir sprendimai:**
1. Patikrinkite, ar digna serveris veikia: `digna repo check`
2. Patikrinkite tinklo ryšį su identiteto tiekėju
3. Patikrinkite, ar `DIGNA_OIDC_CONFIGURATION_URL` pasiekiamas
4. Patikrinkite, ar ugniasienės taisyklės leidžia išeinančius HTTPS ryšius
5. Patikrinkite, ar backend ir prietaisų skydelis pasiekia vienas kitą

---

### Vartotojai nesukuriami automatiškai

**Simptomai:**
- SSO prisijungimas pavyksta, bet vartotojas nėra sukurtas digna
- Gavote leidimų klaidą po SSO prisijungimo

**Priežastys ir sprendimai:**
1. Patikrinkite OIDC konfigūraciją
2. Patikrinkite, ar vartotojų leidimai (permissions) tinkamai nustatyti
3. Peržiūrėkite digna žurnalus (logs) dėl klaidų pranešimų
4. Perkraukite serverio paslaugą
5. Jei problema išlieka, kreipkitės: support@digna.ai

---

## Palaikomi tiekėjai {: #supported-providers }

### Išbandyti ir palaikomi

Toliau pateikti OIDC tiekėjai buvo išbandyti ir žinomi kaip veikiančią:

| Tiekėjas | Konfigūracijos URL | Nustatymo vadovas |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Kiti OIDC tiekėjai

Bet koks tiekėjas, palaikantis OpenID Connect, gali būti integruotas. Reikalinga informacija:

- Kliento ID
- Kliento slaptasis raktas
- OpenID konfigūracijos URL (dažniausiai `/.well-known/openid-configuration`)
- Palaikomi scope’ai (dažniausiai `openid profile email`)

Jei reikia pagalbos integruojant konkretų tiekėją, kreipkitės: support@digna.ai

---

## Geriausios praktikos

**DARYK:**
- Naudokite HTTPS gamybinėje aplinkoje (ne HTTP)
- Laikykite klientų slaptuosius raktus saugiai (jei įmanoma, naudokite aplinkos kintamuosius)
- Periodiškai keičiame slaptuosius raktus
- Išbandykite pakeitimus ne gamybinėje aplinkoje pirmiausia
- Dokumentuokite, kurie tiekėjai yra sukonfigūruoti
- Stebėkite prisijungimų žurnalus dėl neįprastos veiklos
- Laikykite identiteto tiekėjo konfigūraciją suderintą su digna konfigūracija

**NEDARYK:**
- Laikyti klientų slaptuosius raktus versijų valdymo sistemoje
- Naudoti HTTP redirect URI gamyboje
- Konfigūruoti kelis tiekėjus su tuo pačiu key
- Palikti numatytuosius/testinius kredencialus gamyboje
- Viešinti konfigūracinius failus, kuriuose yra slaptieji raktai
- Maišyti vystymo ir gamybos kredencialus

---

## Pagalba

Reikia pagalbos konfigūruojant SSO?

- **El. paštas:** support@digna.ai
- **Dokumentacija:** https://docs.digna.ai
- **Tinklalapis:** https://www.digna.ai

---

**Paskutinį kartą atnaujinta:** August 30, 2026  
**Išleidimas:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**