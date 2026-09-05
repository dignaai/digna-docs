# Single Sign-On Integration Guide

---

## Turinys

1. [Įvadas ir apžvalga](#introduction-and-overview)
2. [Konfigūracijos veiksmai](#configuration-steps)
3. [Dashboard konfigūracija](#dashboard-configuration)
4. [Backend konfigūracija](#backend-configuration)
5. [Prisijungimo testavimas](#testing-login)
6. [Trikčių šalinimas](#troubleshooting)
7. [Palaikomi tiekėjai](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Šis vadovas pateikia žingsnis po žingsnio instrukcijas, kaip integruoti Single Sign-On (SSO) su digna platforma naudojant **OpenID Connect (OIDC)**.

### Kas yra SSO?

Single Sign-On leidžia vartotojams saugiai prisijungti prie digna naudodami savo įmonės prisijungimo duomenis per išorinius identiteto tiekėjus. Vartotojai gali autentifikuotis naudodami savo korporacinius duomenis vietoje atskirų digna slaptažodžių valdymo.

### Kaip tai veikia

SSO digna įgyvendinamas naudojant OIDC protokolą. Keli identiteto tiekėjai gali būti sukonfigūruoti lygiagrečiai keičiant du pagrindinius konfigūracijos failus:

- **`dashboard_config.toml`** — kontroliuoja frontend prisijungimo sąsają
- **`config.toml`** — konfigūruoja backend OIDC ryšius

### Palaikomi tiekėjai {: #supported-providers-overview }

Šio vadovo pavyzdžiai naudoja **Microsoft** ir **Google**, tačiau **bet kuris OIDC suderinamas tiekėjas** gali būti integruotas pagal tą patį struktūros principą.

Dažniausi OIDC tiekėjai:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Kiti OIDC suderinami identiteto tiekėjai

---

## Configuration Steps {: #configuration-steps }

SSO konfigūracija reikalauja atnaujinimų dviejuose failuose. Ši skiltis paaiškina, kaip sukonfigūruoti kiekvieną iš jų.

### Konfigūracijų failų apžvalga

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend prisijungimo sąsaja |
| **config.toml** | `/config.toml` | Backend OIDC ryšiai |

Abu failai turi būti sukonfigūruoti, kad SSO veiktų tinkamai.

---

## Dashboard Configuration {: #dashboard-configuration }

### Failo vieta

```
dashboard/dashboard_config.toml
```

### 1 žingsnis: pridėkite OIDC tiekėjus

Pridėkite įrašus po `[[login.oidc]]` masyvu kiekvienam identiteto tiekėjui, kurį norite palaikyti.

**Pavyzdys su Microsoft ir Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Prisijungti su Microsoft"

[[login.oidc]]
key = "google"
label = "Prisijungti su Google"
```

### 2 žingsnis: sukonfigūruokite prisijungimo parinktis

Nurodykite, ar turi būti leidžiamas prisijungimas naudojant slaptažodį:

```toml
[login]
usePassword = true
```

### Konfigūracijos parametrai

#### `[[login.oidc]]` skyrius

| Parametras | Tipas | Privalomas | Aprašymas |
|---|---|---|---|
| `key` | string | Taip | Unikalus identifikatorius OIDC ryšiui (turi atitikti raktą config.toml) |
| `label` | string | Taip | Tekstas, rodomas prisijungimo mygtuke (pvz., "Prisijungti su Microsoft") |

#### `[login]` skyrius

| Parametras | Tipas | Numatytoji reikšmė | Aprašymas |
|---|---|---|---|
| `usePassword` | boolean | false | Leidžia prisijungimą naudojant slaptažodį papildomai prie SSO |

### Kaip veikia usePassword

**Jei `usePassword = true`:**
- Prisijungimo ekrane rodomi SSO mygtukai (pvz., "Prisijungti su Microsoft")
- Prisijungimo ekrane taip pat rodomi naudotojo vardo ir slaptažodžio laukai
- Vartotojai gali autentifikuotis bet kuriuo metodu
- Leidžiama hibridinė konfigūracija, kai kai kurie vartotojai naudoja SSO, o kiti — slaptažodžius

**Jei `usePassword = false` (arba praleista):**
- Prisijungimo ekrane rodomi tik SSO mygtukai
- Nėra naudotojo vardo/slaptažodžio laukų
- Galima tik OIDC autentifikacija

!!! tip "Patarimas"

    Slaptažodžiu pagrįstas prisijungimas yra prieinamas tik vartotojams, kurie buvo sukurti su slaptažodžiais naudojant komandą `digna user add` arba per dashboard.

### Pilnas pavyzdys

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Prisijungti su Microsoft"

[[login.oidc]]
key = "google"
label = "Prisijungti su Google"

[[login.oidc]]
key = "okta"
label = "Prisijungti su Okta"
```

---

## Backend Configuration {: #backend-configuration }

### Failo vieta

```
/config.toml
```

(Šakninė digna diegimo direktorija)

### 1 žingsnis: pridėkite OIDC tiekėjų skyrius

Kiekvienam tiekėjui turi būti atskiras `[oidc.<key>]` skyrius. Raktas turi atitikti `key`, apibrėžtą `dashboard_config.toml`.

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
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Taip | Kliento ID iš identiteto tiekėjo | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Taip | Kliento slaptasis raktas iš identiteto tiekėjo | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Taip | Atgalinio kvietimo (callback) URL po autentifikacijos | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Taip | OIDC konfigūracijos galinė vieta | `https://login.microsoftonline.com/...` |

!!! warning "Svarbu"

    Pakeiskite vietos užpildo reikšmes (`<client_id>`, `<client_secret>`, `<tenant_id>`) tikromis kredencialų reikšmėmis iš jūsų identiteto tiekėjo kūrėjo portalo.

### Redirect URI

Redirect URI turi būti toks pat, kaip nurodyta identiteto tiekėjo konfigūracijoje:

```
http://localhost:5173/oidc/callback
```

Jei digna talpinama kitoje domene, atnaujinkite atitinkamai:
- Vietinei aplinkai: `http://localhost:5173/oidc/callback`
- Produkcijai: `https://digna.yourdomain.com/oidc/callback`

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

## Testing Login {: #testing-login }

Baigus konfigūravimą, patikrinkite, ar SSO veikia teisingai.

### Prieš testavimą — kontrolinis sąrašas

Prieš testuojant įsitikinkite:

- [ ] `dashboard_config.toml` atnaujintas su OIDC tiekėjais
- [ ] `config.toml` atnaujintas su OIDC kredencialais
- [ ] Abu failai įrašyti
- [ ] Kredencialai yra teisingi (client ID, client secret)
- [ ] Redirect URI atitinka jūsų diegimo URL
- [ ] Identiteto tiekėjo programoje užregistruotas redirect URI

### Testavimo veiksmai

#### 1 žingsnis: perkraukite paslaugas

Perkraukite digna backend ir web serverį, kad pritaikytumėte pakeitimus.

**Jei veikia kaip Windows paslauga:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Jei paleidžiate rankiniu būdu:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Jei naudojate IIS arba Tomcat:**
Perkraukite savo web serverio paslaugą.

#### 2 žingsnis: atidarykite dashboard

Atidarykite digna dashboard savo naršyklėje:

```
http://localhost:5173
```

(ar jūsų sukonfigūruotas dashboard URL)

#### 3 žingsnis: patikrinkite prisijungimo mygtukus

Patikrinkite, ar atsirado prisijungimo mygtukai kiekvienam sukonfigūruotam tiekėjui:

- Turėtumėte matyti mygtuką "Prisijungti su Microsoft"
- Turėtumėte matyti mygtuką "Prisijungti su Google"
- (Jei usePassword = true) Turėtumėte matyti naudotojo vardo/slaptažodžio laukus

Jei mygtukų nematote:
- Patikrinkite, ar `dashboard_config.toml` įrašytas
- Patikrinkite, ar dashboard paslauga perkrauta
- Patikrinkite naršyklės konsolę (F12) dėl klaidų

#### 4 žingsnis: išbandykite SSO prisijungimą

Spustelėkite vieną iš SSO mygtukų (pvz., "Prisijungti su Microsoft"):

1. Turėtumėte būti nukreipti į identiteto tiekėjo prisijungimo puslapį
2. Prisijunkite naudodami savo įmonės kredencialus
3. Turėtumėte būti grąžinti į digna
4. Turėtumėte būti prisijungę prie digna

#### 5 žingsnis: patikrinkite vartotojo kūrimą

Sėkmingo SSO prisijungimo metu:

- Vartotojas turėtų būti automatiškai sukurtas digna
- Vartotojas turėtų būti prisijungęs
- Vartotojo profilyje turėtų matytis jūsų identiteto tiekėjo informacija
- Turėtumėte matyti digna dashboard

#### 6 žingsnis: išbandykite prisijungimą slaptažodžiu (jei įjungta)

Jei `usePassword = true`:

1. Atsijunkite iš digna
2. Prisijungimo puslapyje įveskite naudotojo vardą ir slaptažodį
3. Turėtumėte sugebėti prisijungti su slaptažodžiu

---

## Troubleshooting {: #troubleshooting }

### Prisijungimo mygtukai neatsiranda

**Simptomai:**
- OIDC prisijungimo mygtukai nematomi prisijungimo puslapyje
- Matomi tik slaptažodžių laukai (jei usePassword = true)

**Priežastys ir sprendimai:**
1. Patikrinkite, ar `dashboard_config.toml` yra `dashboard/` kataloge
2. Patikrinkite, ar `[[login.oidc]]` skyriai yra ir sintaksė teisinga
3. Perkraukite dashboard paslaugą
4. Išvalykite naršyklės talpyklą (Ctrl+Shift+Delete arba Cmd+Shift+Delete)
5. Patikrinkite naršyklės konsolę (F12 → Console tab) dėl klaidų

---

### Redirect URI neatitikimo klaida

**Simptomai:**
- Po SSO mygtuko paspaudimo rodoma klaida apie "redirect_uri mismatch"
- "The redirect URI is not registered" klaida

**Priežastys ir sprendimai:**
1. Patikrinkite, ar `DIGNA_OIDC_REDIRECT_URI` config.toml yra teisingas
2. Patikrinkite, ar redirect URI užregistruotas identiteto tiekėjo nustatymuose
3. Užtikrinkite, kad abu URL yra identiški (įskaitant protokolą, domeną, kelią)
4. Patikrinkite dėl rašybos klaidų redirect URI
5. Jei naudojate HTTPS, įsitikinkite, kad sertifikatas galioja

---

### Netinkami kliento kredencialai

**Simptomai:**
- "Invalid client ID or secret" klaida
- Autentifikacija nepavyksta dėl kredencialų klaidos

**Priežastys ir sprendimai:**
1. Patikrinkite, ar `DIGNA_OIDC_CLIENT_ID` ir `DIGNA_OIDC_CLIENT_SECRET` yra teisingi
2. Užtikrinkite, kad nėra papildomų tarpų ar netinkamų simbolių
3. Patikrinkite, ar kredencialai nepasibaigė ir nebuvo atšaukti
4. Perkraukite backend paslaugą po konfiguracijos atnaujinimo
5. Patikrinkite identiteto tiekėjo konsolę, kad įsitikintumėte, jog kredencialai aktyvūs

---

### Prisijungimas stringa arba baigiasi laikas

**Simptomai:**
- Paspaudus SSO mygtuką niekas nevyksta
- Po kelių sekundžių įvyksta timeout
- Naršyklė rodo "Failed to connect" ar panašų pranešimą

**Priežastys ir sprendimai:**
1. Patikrinkite, ar digna backend veikia: `digna repo check`
2. Patikrinkite tinklo ryšį su identiteto tiekėju
3. Patikrinkite, ar `DIGNA_OIDC_CONFIGURATION_URL` pasiekiamas
4. Patikrinkite ugniasienės taisykles, ar leidžiami išeinantys HTTPS ryšiai
5. Patikrinkite, ar backend ir dashboard gali pasiekti vienas kitą

---

### Vartotojai nesukuriami automatiškai

**Simptomai:**
- SSO prisijungimas pavyksta, bet vartotojas nesukuriamas digna
- Po SSO prisijungimo gaunate leidimų klaidą

**Priežastys ir sprendimai:**
1. Patikrinkite OIDC konfigūraciją
2. Patikrinkite, ar nustatyti vartotojų leidimai
3. Peržiūrėkite digna log'us dėl klaidų pranešimų
4. Perkraukite backend paslaugą
5. Jei problema išlieka, susisiekite su support@digna.ai

---

## Supported Providers {: #supported-providers }

### Išbandyti ir palaikomi

Šie OIDC tiekėjai buvo išbandyti ir žinoma, kad veikia:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Kiti OIDC tiekėjai

Bet kuris tiekėjas, palaikantis OpenID Connect, gali būti integruotas. Reikalinga informacija:

- Client ID
- Client secret
- OpenID konfigūracijos URL (dažniausiai `/.well-known/openid-configuration`)
- Palaikomi scope'ai (paprastai `openid profile email`)

Jei reikia pagalbos integruojant konkretų tiekėją, susisiekite su support@digna.ai.

---

## Geriausios praktikos

DARYKITE:
- Naudokite HTTPS produkcijoje (ne HTTP)
- Saugokite klientų slaptuosius raktus saugiai (jei galima, naudokite aplinkos kintamuosius)
- Periodiškai keiskite slaptuosius raktus
- Išbandykite neprodukcinėje aplinkoje prieš diegiant į produkciją
- Dokumentuokite, kurie tiekėjai sukonfigūruoti
- Stebėkite prisijungimo žurnalus dėl neįprastos veiklos
- Laikykite identiteto tiekėjo konfigūraciją sinchronizuotą su digna konfigūracija

NEDARYKITE:
- Nelaikykite klientų slaptųjų raktų versijų valdyme (version control)
- Nenaudokite HTTP redirect URI produkcijoje
- Nekonfigūruokite kelių tiekėjų su tuo pačiu raktu
- Ne palikite numatytųjų/testo kredencialų produkcijoje
- Neatskleiskite konfigūracijos failų, kuriuose yra slaptieji raktai
- Nemaišykite vystymo ir produkcijos kredencialų

---

## Pagalba

Reikia pagalbos su SSO konfigūracija?

- **El. paštas:** support@digna.ai
- **Dokumentacija:** https://docs.digna.ai
- **Svetainė:** https://www.digna.ai

---

**Paskutinį kartą atnaujinta:** 2026 m. rugpjūčio 30 d.  
**Leidimas:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**