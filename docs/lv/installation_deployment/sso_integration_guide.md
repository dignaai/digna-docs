---
title: Single Sign-On (SSO) integrācijas rokasgrāmata | digna dokumentācija
description: Soli pa solim rokasgrāmata, kā konfigurēt Single Sign-On (SSO) digna platformai, izmantojot OpenID Connect (OIDC). Apskata informācijas paneli un backenda konfigurāciju, testēšanu, problēmu novēršanu un atbalstītus identitātes pakalpojumu sniedzējus, tostarp Microsoft Entra ID, Google Workspace un Okta.
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
lang: lv
robots: index, follow
og_title: digna Single Sign-On (SSO) integrācijas rokasgrāmata
og_description: Konfigurējiet Single Sign-On priekš digna, izmantojot OpenID Connect. Soli pa solim iestatījums Microsoft Entra ID, Google Workspace, Okta un citiem OIDC saderīgiem identitātes sniedzējiem.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On integrācijas rokasgrāmata

---

## Saturs

1. [Ievads un pārskats](#introduction-and-overview)
2. [Konfigurācijas soļi](#configuration-steps)
3. [Informācijas paneļa konfigurācija](#dashboard-configuration)
4. [Backenda konfigurācija](#backend-configuration)
5. [Pieteikšanās testēšana](#testing-login)
6. [Problēmu novēršana](#troubleshooting)
7. [Atbalstītie sniedzēji](#supported-providers)

---

## Ievads un pārskats {: #introduction-and-overview }

Šī rokasgrāmata sniedz soli pa solim norādījumus Single Sign-On (SSO) integrēšanai ar digna platformu, izmantojot **OpenID Connect (OIDC)**.

### Kas ir SSO?

Single Sign-On ļauj lietotājiem droši pierakstīties digna, izmantojot viņu uzņēmuma akreditācijas datus caur ārējiem identitātes sniedzējiem. Lietotāji var autentizēties ar korporatīvajiem akreditācijas datiem, nevis pārvaldīt atsevišķas digna paroles.

### Kā tas darbojas

SSO digna tiek īstenots, izmantojot OIDC protokolu. Var konfigurēt vairākus identitātes sniedzējus paralēli, pielāgojot divus galvenos konfigurācijas failus:

- **`dashboard_config.toml`** — Kontrolē frontend pieteikšanās saskarni
- **`config.toml`** — Konfigurē backenda OIDC savienojumus

### Atbalstītie sniedzēji {: #supported-providers-overview }

Piemēri šajā rokasgrāmatā izmanto **Microsoft** un **Google**, taču **jebkuru OIDC-saderīgu sniedzēju** var integrēt, sekojot tai pašai struktūrai.

Bieži izmantotie OIDC sniedzēji:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Citi OIDC-saderīgi identitātes sniedzēji

---

## Konfigurācijas soļi {: #configuration-steps }

SSO konfigurācija prasa izmaiņas divos failos. Šī sadaļa paskaidro, kā konfigurēt katru no tiem.

### Konfigurācijas failu pārskats

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend pieteikšanās saskarne |
| **config.toml** | `/config.toml` | Backenda OIDC savienojumi |

Abiem failiem jābūt konfigurētiem, lai SSO darbotos pareizi.

---

## Informācijas paneļa konfigurācija {: #dashboard-configuration }

### Faila atrašanās vieta

```
dashboard/dashboard_config.toml
```

### 1. solis: Pievienot OIDC sniedzējus

Pievienojiet ierakstus zem masīva `[[login.oidc]]` katram identitātes sniedzējam, kuru vēlaties atbalstīt.

**Piemērs ar Microsoft un Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Pierakstīties ar Microsoft"

[[login.oidc]]
key = "google"
label = "Pierakstīties ar Google"
```

### 2. solis: Konfigurēt pieteikšanās opcijas

Norādiet, vai jāļauj pieteikšanās, izmantojot paroli:

```toml
[login]
usePassword = true
```

### Konfigurācijas parametri

#### `[[login.oidc]]` sadaļa

| Parametrs | Tips | Obligāts | Apraksts |
|---|---|---|---|
| `key` | string | Jā | Unikāls identificētājs OIDC savienojumam (jāsakrīt ar atslēgu config.toml) |
| `label` | string | Jā | Teksts, kas tiek parādīts uz pieteikšanās pogas (piem., "Pierakstīties ar Microsoft") |

#### `[login]` sadaļa

| Parametrs | Tips | Noklusējums | Apraksts |
|---|---|---|---|
| `usePassword` | boolean | false | Ļaut pieteikšanos, izmantojot paroli papildus SSO |

### Izpratne par usePassword

**Ja `usePassword = true`:**
- Pieteikšanās ekrānā tiek rādītas SSO pogas (piem., "Pierakstīties ar Microsoft")
- Pieteikšanās ekrānā tiek rādīti arī lietotājvārda un paroles lauki
- Lietotāji var autentizēties ar jebkuru no metodēm
- Iespējams hibrīda režīms, kur daži lietotāji izmanto SSO un citi paroles

**Ja `usePassword = false` (vai netiek norādīts):**
- Pieteikšanās ekrānā tiek rādītas tikai SSO pogas
- Nav lietotājvārda/paroles lauku
- Pieejama tikai OIDC autentifikācija

> **💡 Padoms**
>
> Pieteikšanās ar paroli ir pieejama tikai tiem lietotājiem, kuri tika izveidoti ar parolēm, izmantojot komandu `digna user add` vai caur informācijas paneli.

### Pilns piemērs

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Pierakstīties ar Microsoft"

[[login.oidc]]
key = "google"
label = "Pierakstīties ar Google"

[[login.oidc]]
key = "okta"
label = "Pierakstīties ar Okta"
```

---

## Backenda konfigurācija {: #backend-configuration }

### Faila atrašanās vieta

```
/config.toml
```

(Root digna instalācijas direktorija)

### 1. solis: Pievienot OIDC sniedzēju sadaļas

Katram sniedzējam jābūt atsevišķai `[oidc.<key>]` sadaļai. Atslēgai jāatkārto `key`, kas definēts `dashboard_config.toml`.

### Microsoft konfigurācija

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google konfigurācija

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurācijas parametri

| Parametrs | Tips | Obligāts | Apraksts | Piemērs |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Jā | Klienta ID no identitātes sniedzēja | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Jā | Klienta noslēpums no identitātes sniedzēja | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Jā | Pāradresācijas (callback) URL pēc autentifikācijas | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Jā | OIDC konfigurācijas beigu punkts | `https://login.microsoftonline.com/...` |

> **⚠️ Svarīgi**
>
> Aizstājiet vietturu vērtības (`<client_id>`, `<client_secret>`, `<tenant_id>`) ar reālām akreditācijām no jūsu identitātes sniedzēja izstrādātāju paneļa.

### Redirect URI

Pāradresācijas URI jābūt vienādai arī jūsu identitātes sniedzēja konfigurācijā:

```
http://localhost:5173/oidc/callback
```

Ja digna tiek hostēta citā domēnā, atjauniniet atbilstoši:
- Lokāli: `http://localhost:5173/oidc/callback`
- Ražošanā: `https://digna.yourdomain.com/oidc/callback`

### Pilns piemērs

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

## Pieteikšanās testēšana {: #testing-login }

Pēc konfigurācijas pabeigšanas pārliecinieties, ka SSO darbojas pareizi.

### Pārbaudes iepriekšējā kontrolsaraksta punkts

Pirms testēšanas pārliecinieties:

- [ ] `dashboard_config.toml` ir atjaunināts ar OIDC sniedzējiem
- [ ] `config.toml` ir atjaunināts ar OIDC akreditācijām
- [ ] Abi faili ir saglabāti
- [ ] Akreditācijas dati ir pareizi (client ID, client secret)
- [ ] Redirect URI atbilst jūsu izvietošanas URL
- [ ] Identitātes sniedzēja lietotne ir konfigurēta ar redirect URI

### Testēšanas soļi

#### 1. solis: Restartēt servisus

Restartējiet digna backend un web serveri, lai piemērotu izmaiņas.

**Ja darbojas kā Windows serviss:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Ja darbojat manuāli:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Ja izmantojat IIS vai Tomcat:**
Restartējiet attiecīgo web servera servisu.

#### 2. solis: Atvērt informācijas paneli

Atveriet digna informācijas paneli pārlūkprogrammā:

```
http://localhost:5173
```

( vai jūsu konfigurētais informācijas paneļa URL )

#### 3. solis: Pārbaudīt pieteikšanās pogas

Pārliecinieties, ka pieteikšanās pogas parādās katram konfigurētajam sniedzējam:

- ✅ Jāredz poga "Pierakstīties ar Microsoft"
- ✅ Jāredz poga "Pierakstīties ar Google"
- ✅ (Ja usePassword = true) Jāredz lietotājvārda/paroles lauki

Ja pogas neparādās:
- Pārbaudiet, vai `dashboard_config.toml` ir saglabāts
- Pārbaudiet, vai dashboard serviss ir restartēts
- Pārbaudiet pārlūkprogrammas konsoli (F12) kļūdu ziņojumiem

#### 4. solis: Pārbaudīt SSO pieteikšanos

Noklikšķiniet uz vienas no SSO pogām (piem., "Pierakstīties ar Microsoft"):

1. Jums jābūt pāradresētam uz identitātes sniedzēja pieteikšanās lapu
2. Pierakstieties ar saviem uzņēmuma akreditācijas datiem
3. Jums jābūt pāradresētam atpakaļ uz digna
4. Jums jābūt pieteikušamies digna

#### 5. solis: Pārbaudīt lietotāja izveidi

Pēc veiksmīgas SSO pieteikšanās:

- ✅ Lietotājs jāizveido automātiski digna sistēmā
- ✅ Lietotājs jābūt pieteiktam
- ✅ Lietotāja profilā jābūt parādītiem identitātes sniedzēja datiem
- ✅ Jums jāredz digna informācijas panelis

#### 6. solis: Pārbaudīt pieteikšanos ar paroli (ja ieslēgta)

Ja `usePassword = true`:

1. Atslēdzieties no digna
2. Pieteikšanās lapā ievadiet lietotājvārdu un paroli
3. Jums jāspēj pieteikties, izmantojot paroli

---

## Problēmu novēršana {: #troubleshooting }

### Pieteikšanās pogas neparādās

**Simptomi:**
- OIDC pieteikšanās pogas neredzamas pieteikšanās lapā
- Redzami tikai paroles lauki (ja usePassword = true)

**Cēloņi un risinājumi:**
1. Pārbaudiet, vai `dashboard_config.toml` atrodas `dashboard/` direktorijā
2. Pārliecinieties, ka `[[login.oidc]]` sadaļas ir klāt un sintakse pareiza
3. Restartējiet dashboard servisu
4. Notīriet pārlūkprogrammas kešu (Ctrl+Shift+Delete vai Cmd+Shift+Delete)
5. Pārbaudiet pārlūkprogrammas konsoli (F12 → Console) kļūdām

---

### Redirect URI neatbilstības kļūda

**Simptomi:**
- Pēc SSO pogas nospiešanas kļūda par "redirect_uri mismatch"
- "The redirect URI is not registered" kļūda

**Cēloņi un risinājumi:**
1. Pārbaudiet `DIGNA_OIDC_REDIRECT_URI` `config.toml` — vai tā ir pareiza
2. Pārbaudiet, vai redirect URI ir reģistrēts identitātes sniedzēja iestatījumos
3. Pārliecinieties, ka abi URL ir identiski (īpaši protokols, domēns, ceļš)
4. Pārbaudiet, vai nav rakstības kļūdu redirect URI
5. Ja izmantojat HTTPS, pārliecinieties, ka sertifikāts ir derīgs

---

### Nepareizas klienta akreditācijas kļūda

**Simptomi:**
- "Invalid client ID or secret" kļūda
- Autentifikācija neizdodas akreditāciju kļūdas dēļ

**Cēloņi un risinājumi:**
1. Pārbaudiet, vai `DIGNA_OIDC_CLIENT_ID` un `DIGNA_OIDC_CLIENT_SECRET` ir pareizi
2. Pārliecinieties, ka nav papildu atstarpju vai nevēlamu simbolu
3. Pārbaudiet, vai akreditācijas nav beigušās vai atceltas
4. Restartējiet backenda servisu pēc konfigurācijas atjaunināšanas
5. Pārbaudiet identitātes sniedzēja konsoli, lai pārliecinātos, ka akreditācijas ir aktīvas

---

### Pieteikšanās karājas vai notiek taimauts

**Simptomi:**
- Noklikšķinot uz SSO pogas, nekas nenotiek
- Pēc dažām sekundēm notiek taimauts
- Pārlūkprogramma rāda "Failed to connect" vai līdzīgu paziņojumu

**Cēloņi un risinājumi:**
1. Pārbaudiet, vai digna backend darbojas: `digna repo check`
2. Pārbaudiet tīkla savienojumu līdz identitātes sniedzējam
3. Pārliecinieties, ka `DIGNA_OIDC_CONFIGURATION_URL` ir pieejams
4. Pārbaudiet, vai ugunsmūris ļauj iziet ārā uz HTTPS
5. Pārliecinieties, ka backend un dashboard var savstarpēji sazvanīties

---

### Lietotāji netiek izveidoti automātiski

**Simptomi:**
- SSO pieteikšanās izdodas, bet lietotājs netiek izveidots digna
- Pēc SSO pieteikšanās rodas piekļuves tiesību kļūda

**Cēloņi un risinājumi:**
1. Pārbaudiet OIDC konfigurācijas pareizību
2. Pārbaudiet lietotāju atļauju iestatījumus
3. Pārskatiet digna žurnālus kļūdu ziņojumiem
4. Restartējiet backenda servisu
5. Ja problēma saglabājas, sazinieties: support@digna.ai

---

## Atbalstītie sniedzēji {: #supported-providers }

### Testēti un atbalstīti

Šie OIDC sniedzēji ir testēti un zināmi kā darbojošies:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft dokumentācija](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google dokumentācija](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta dokumentācija](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Citi OIDC sniedzēji

Jebkurš sniedzējs, kas atbalsta OpenID Connect, var tikt integrēts. Nepieciešamā informācija:

- Client ID
- Client secret
- OpenID konfigurācijas URL (parasti pie `/.well-known/openid-configuration`)
- Atbalstītās scopes (parasti `openid profile email`)

Sazinieties ar support@digna.ai, ja nepieciešama palīdzība ar konkrēta sniedzēja integrāciju.

---

## Labākās prakses

✅ DARĪT:
- Izmantojiet HTTPS ražošanā (nevis HTTP)
- Glabājiet klienta noslēpumus droši (ja iespējams, izmantojiet vides mainīgos)
- Periodiski mainiet noslēpumus
- Testējiet vispirms neto ražošanas vidē
- Dokumentējiet, kuri sniedzēji ir konfigurēti
- Uzraugiet pieteikšanās žurnālus, lai noteiktu neparastu aktivitāti
- Sinhronizējiet identitātes sniedzēja konfigurāciju ar digna konfigurāciju

❌ NEDARĪT:
- Glabāt klienta noslēpumus versiju kontrolē
- Izmantot HTTP redirect URI ražošanā
- Konfigurēt vairākus sniedzējus ar vienādu atslēgu
- Atstāt noklusējuma/testa akreditācijas ražošanā
- Izpaust konfigurācijas failus, kas satur noslēpumus
- Sajaukt izstrādes un ražošanas akreditācijas

---

## Atbalsts

Nepieciešama palīdzība SSO konfigurācijā?

- 📧 **E-pasts:** support@digna.ai
- 📚 **Dokumentācija:** https://docs.digna.ai
- 🌐 **Tīmeklis:** https://www.digna.ai

---

**Pēdējo reizi atjaunināts:** 30. augusts, 2026  
**Izlaidums:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
