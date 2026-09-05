# Single Sign-On Integration Guide

---

## Table of Contents

1. [Introduction and Overview](#introduction-and-overview)
2. [Configuration Steps](#configuration-steps)
3. [Dashboard Configuration](#dashboard-configuration)
4. [Backend Configuration](#backend-configuration)
5. [Testing Login](#testing-login)
6. [Troubleshooting](#troubleshooting)
7. [Supported Providers](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Ta vodnik nudi korak za korakom navodila za integracijo Single Sign-On (SSO) s platformo digna z uporabo **OpenID Connect (OIDC)**.

### Kaj je SSO?

Single Sign-On omogoča uporabnikom, da se v digna prijavijo varno z njihovimi korporativnimi poverilnicami prek zunanjih ponudnikov identitete. Uporabniki se lahko avtenticirajo z uporabo svojih podjetniških poverilnic namesto upravljanja ločenih gesel za digna.

### Kako deluje

SSO v digna je implementiran z uporabo protokola OIDC. Več ponudnikov identitete je mogoče konfigurirati vzporedno z nastavitvijo dveh ključnih konfiguracijskih datotek:

- **`dashboard_config.toml`** — nadzoruje prijavni vmesnik v frontend-u
- **`config.toml`** — konfigurira backend OIDC povezave

### Podprti ponudniki {: #supported-providers-overview }

Primeri v tem vodniku uporabljajo **Microsoft** in **Google**, vendar je mogoče integrirati **kateregakoli ponudnika, združljivega z OIDC**, z uporabo iste strukture.

Pogosti OIDC ponudniki vključujejo:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Drugi OIDC-kompatibilni ponudniki identitete

---

## Configuration Steps {: #configuration-steps }

Konfiguracija SSO zahteva posodobitve dveh datotek. Ta razdelek pojasnjuje, kako konfigurirati vsako od njih.

### Pregled konfiguracijskih datotek

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend login interface |
| **config.toml** | `/config.toml` | Backend OIDC connections |

Obe datoteki morata biti konfigurirani, da bo SSO pravilno deloval.

---

## Dashboard Configuration {: #dashboard-configuration }

### Lokacija datoteke

```
dashboard/dashboard_config.toml
```

### Korak 1: Dodajte OIDC ponudnike

Dodajte vnose pod poljem `[[login.oidc]]` za vsakega ponudnika identitete, ki ga želite podpreti.

**Primer z Microsoft in Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Korak 2: Konfigurirajte možnosti prijave

Določite, ali naj bo dovoljena prijava z geslom:

```toml
[login]
usePassword = true
```

### Parametri konfiguracije

#### `[[login.oidc]]` razdelek

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Enolični identifikator za OIDC povezavo (mora ustrezati ključu v config.toml) |
| `label` | string | Yes | Besedilo, prikazano na gumbu za prijavo (npr. "Login with Microsoft") |

#### `[login]` razdelek

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Dovoli prijavo z geslom poleg SSO |

### Razumevanje usePassword

**Če je `usePassword = true`:**
- Na zaslonu za prijavo so prikazani gumbi SSO (npr. "Login with Microsoft")
- Na zaslonu so tudi polja za uporabniško ime in geslo
- Uporabniki se lahko avtenticirajo z enim ali drugim načinom
- Omogoča hibridne nastavitve, kjer nekateri uporabniki uporabljajo SSO, drugi pa gesla

**Če je `usePassword = false` (ali izpuščeno):**
- Na zaslonu za prijavo so prikazani samo SSO gumbi
- Ni polj za uporabniško ime/geslo
- Na voljo je samo OIDC avtentikacija

!!! tip "Nasvet"

    Prijava z geslom je na voljo samo za uporabnike, ki so bili ustvarjeni z gesli z ukazom `digna user add` ali prek nadzorne plošče.

### Celoten primer

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

## Backend Configuration {: #backend-configuration }

### Lokacija datoteke

```
/config.toml
```

(Root digna installation directory)

### Korak 1: Dodajte razdelke za OIDC ponudnike

Vsak ponudnik mora imeti namenski razdelek `[oidc.<key>]`. Ključ mora ustrezati `key`, definiranemu v `dashboard_config.toml`.

### Microsoft konfiguracija

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google konfiguracija

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parametri konfiguracije

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID iz ponudnikovega portala | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret iz ponudnikovega portala | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | Callback URL po avtentikaciji | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | OIDC konfiguracijska točka | `https://login.microsoftonline.com/...` |

!!! warning "Pomembno"

    Zamenjajte nadomestne vrednosti (`<client_id>`, `<client_secret>`, `<tenant_id>`) z dejavnimi poverilnicami iz razvijalskega konzola vašega ponudnika identitete.

### Redirect URI

Redirect URI mora biti enaka kot v konfiguraciji ponudnika identitete:

```
http://localhost:5173/oidc/callback
```

Če je digna gostovan na drugačnem domeni, posodobite primerno:
- Lokalno: `http://localhost:5173/oidc/callback`
- Produkcija: `https://digna.yourdomain.com/oidc/callback`

### Celoten primer

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

Po dokončani konfiguraciji preverite, ali SSO deluje pravilno.

### Predtestni kontrolni seznam

Pred testiranjem zagotovite:

- [ ] `dashboard_config.toml` je posodobljen z OIDC ponudniki
- [ ] `config.toml` je posodobljen z OIDC poverilnicami
- [ ] Obe datoteki sta shranjeni
- [ ] Poverilnice so pravilne (client ID, client secret)
- [ ] Redirect URI ustreza vaši namestitveni URL
- [ ] Aplikacija pri ponudniku identitete je konfigurirana z redirect URI

### Koraki testiranja

#### Korak 1: Ponovni zagon storitev

Ponovno zaženite backend in spletni strežnik digna, da uveljavite spremembe.

**Če tečete kot Windows storitev:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Če tečete ročno:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Če uporabljate IIS ali Tomcat:**
Ponovno zaženite storitev vašega spletnega strežnika.

#### Korak 2: Odprite nadzorno ploščo

Odprite digna nadzorno ploščo v brskalniku:

```
http://localhost:5173
```

(ali vaša konfigurirana URL nadzorne plošče)

#### Korak 3: Preverite gumbe za prijavo

Preverite, ali se za vsakega konfiguriranega ponudnika prikažejo gumbi za prijavo:

- Morali bi videti gumb "Login with Microsoft"
- Morali bi videti gumb "Login with Google"
- (Če je usePassword = true) Morali bi videti polja za uporabniško ime/geslo

Če se gumbi ne prikažejo:
- Preverite, da je `dashboard_config.toml` shranjen
- Preverite, da je storitev nadzorne plošče ponovno zagnana
- Preverite konzolo brskalnika (F12) za napake

#### Korak 4: Preizkusite SSO prijavo

Kliknite enega od SSO gumbov (npr. "Login with Microsoft"):

1. Preusmerjeni boste na prijavno stran ponudnika identitete
2. Prijavite se s svojimi podjetniškimi poverilnicami
3. Preusmerjeni boste nazaj v digna
4. Prisotni boste prijavljeni v digna

#### Korak 5: Preverite ustvarjanje uporabnika

Po uspešni SSO prijavi:

- Uporabnik bi moral biti samodejno ustvarjen v digna
- Uporabnik bi moral biti prijavljen
- Profil uporabnika bi moral prikazati poverilnice ponudnika identitete
- Videli bi morali digna nadzorno ploščo

#### Korak 6: Preizkus prijave z geslom (če omogočeno)

Če je `usePassword = true`:

1. Odjavite se iz digna
2. Na strani za prijavo vnesite uporabniško ime in geslo
3. Morali bi se lahko prijaviti z geselnimi poverilnicami

---

## Troubleshooting {: #troubleshooting }

### Gumbi za prijavo se ne prikažejo

**Simptomi:**
- OIDC gumbi za prijavo niso vidni na strani za prijavo
- Vidite samo polja za geslo (če je usePassword = true)

**Vzroki in rešitve:**
1. Preverite, da je `dashboard_config.toml` v mapi `dashboard/`
2. Preverite, da so prisotni razdelki `[[login.oidc]]` s pravilno sintakso
3. Ponovno zaženite storitev nadzorne plošče
4. Počistite predpomnilnik brskalnika (Ctrl+Shift+Delete ali Cmd+Shift+Delete)
5. Preverite konzolo brskalnika (F12 → Console) za napake

---

### Napaka neusklajenosti Redirect URI

**Simptomi:**
- Po kliku na SSO gumb napaka o "redirect_uri mismatch"
- Napaka "The redirect URI is not registered"

**Vzroki in rešitve:**
1. Preverite, da je `DIGNA_OIDC_REDIRECT_URI` v `config.toml` pravilen
2. Preverite, da je redirect URI registriran v nastavitvah ponudnika identitete
3. Zagotovite, da obe strani uporabljata enake URL-je (vključno s protokolom, domeno, potjo)
4. Preverite tipkarske napake v redirect URI
5. Če uporabljate HTTPS, zagotovite veljavno potrdilo

---

### Napaka neveljavnih odjemalčevih poverilnic

**Simptomi:**
- Napaka "Invalid client ID or secret"
- Avtentikacija ne uspe zaradi napake s podatki

**Vzroki in rešitve:**
1. Preverite, da sta `DIGNA_OIDC_CLIENT_ID` in `DIGNA_OIDC_CLIENT_SECRET` pravilna
2. Zagotovite, da ni dodatnih presledkov ali neveljavnih znakov
3. Preverite, da poverilnice niso potekle ali bile preklicane
4. Ponovno zaženite backend po posodobitvi konfiguracije
5. Preverite konzolo ponudnika identitete, da potrdite, da so poverilnice aktivne

---

### Prijava se zatika ali poteče čas

**Simptomi:**
- Klik na SSO gumb ne naredi nič
- Po nekaj sekundah poteče čas
- Brskalnik prikaže "Failed to connect" ali podobno

**Vzroki in rešitve:**
1. Preverite, da je digna backend zagnan: `digna repo check`
2. Preverite omrežno povezljivost do ponudnika identitete
3. Preverite, da je `DIGNA_OIDC_CONFIGURATION_URL` dostopen
4. Preverite, da požarni zidovi dovolijo odhodne HTTPS povezave
5. Preverite, da se backend in nadzorna plošča lahko povežeta med seboj

---

### Uporabniki se ne ustvarijo samodejno

**Simptomi:**
- SSO prijava uspe, vendar uporabnik ni ustvarjen v digna
- Po SSO prijavi dobite napako o dovoljenjih

**Vzroki in rešitve:**
1. Preverite pravilnost OIDC konfiguracije
2. Preverite, ali so ustrezne nastavitve dovoljenj za uporabnike
3. Preverite digna loge za sporočila o napakah
4. Ponovno zaženite backend storitev
5. Kontaktirajte support@digna.ai, če težava ostane

---

## Supported Providers {: #supported-providers }

### Preizkušeni in podprti

Naslednji OIDC ponudniki so preizkušeni in delujejo:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Drugi OIDC ponudniki

Kateri koli ponudnik, ki podpira OpenID Connect, je mogoče integrirati. Potrebne informacije:

- Client ID
- Client secret
- OpenID konfiguracijska URL (običajno na `/.well-known/openid-configuration`)
- Podprti scope-i (običajno `openid profile email`)

Kontaktirajte support@digna.ai, če potrebujete pomoč pri integraciji specifičnega ponudnika.

---

## Best Practices

DO:
- Uporabljajte HTTPS v produkciji (ne HTTP)
- Hranite client secret varno (po možnosti v okolijskih spremenljivkah)
- Občasno rotirajte (zamenjajte) skrivnosti
- Najprej testirajte v neprodukcijskem okolju
- Dokumentirajte, kateri ponudniki so konfigurirani
- Spremljajte prijavne zapise zaradi sumljivih dejavnosti
- Ohranjajte sinhronizacijo nastavitev ponudnika identitete z digna konfiguracijo

DON'T:
- Ne shranjujte client secret v sistem za nadzor različic
- Ne uporabljajte HTTP redirect URI v produkciji
- Ne konfigurirajte več ponudnikov z istim ključem
- Ne pustite privzetih/testnih poverilnic v produkciji
- Ne razkrivajte konfiguracijskih datotek, ki vsebujejo skrivnosti
- Ne mešajte razvojnih in produkcijskih poverilnic

---

## Support

Potrebujete pomoč pri konfiguraciji SSO?

- **Email:** support@digna.ai
- **Dokumentacija:** https://docs.digna.ai
- **Spletna stran:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**