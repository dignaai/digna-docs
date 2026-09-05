---
title: Single Sign-On (SSO) integrációs útmutató | digna Dokumentáció
description: Lépésről lépésre útmutató a Single Sign-On (SSO) beállításához digna számára OpenID Connect (OIDC) használatával. Lefedi a dashboard és backend konfigurációt, tesztelést, hibakeresést és a támogatott identitásszolgáltatókat, beleértve a Microsoft Entra ID-t, Google Workspace-t és Okta-t.
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
lang: hu
robots: index, follow
og_title: digna Single Sign-On (SSO) integrációs útmutató
og_description: Konfigurálja a Single Sign-On-t a digna számára OpenID Connect használatával. Lépésről lépésre útmutató Microsoft Entra ID, Google Workspace, Okta és más OIDC-kompatibilis identitásszolgáltatókhoz.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On integrációs útmutató

---

## Tartalomjegyzék

1. [Bevezetés és áttekintés](#introduction-and-overview)
2. [Konfigurációs lépések](#configuration-steps)
3. [Dashboard konfiguráció](#dashboard-configuration)
4. [Backend konfiguráció](#backend-configuration)
5. [Bejelentkezés tesztelése](#testing-login)
6. [Hibakeresés](#troubleshooting)
7. [Támogatott szolgáltatók](#supported-providers)

---

## Bevezetés és áttekintés {: #introduction-and-overview }

Ez az útmutató lépésről lépésre ismerteti a Single Sign-On (SSO) integrációját a digna platformon az **OpenID Connect (OIDC)** protokoll segítségével.

### Mi az az SSO?

A Single Sign-On lehetővé teszi, hogy a felhasználók vállalati hitelesítő adataikkal jelentkezzenek be a digna rendszerbe külső identitásszolgáltatókon keresztül. A felhasználók a vállalati hitelesítőikkel autentikálhatnak, ahelyett, hogy külön digna jelszavakat kezelnének.

### Hogyan működik

A digna SSO-ja az OIDC protokollt használja. Több identitásszolgáltató is párhuzamosan konfigurálható a két kulcsfontosságú konfigurációs fájl módosításával:

- **`dashboard_config.toml`** — Szabályozza a frontend bejelentkezési felületet
- **`config.toml`** — Konfigurálja a backend OIDC kapcsolatokat

### Támogatott szolgáltatók {: #supported-providers-overview }

Az útmutató példái **Microsoft** és **Google** használatát mutatják be, de **bármely OIDC-kompatibilis szolgáltató** integrálható ugyanilyen szerkezet szerint.

Gyakori OIDC szolgáltatók:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Egyéb OIDC-kompatibilis identitásszolgáltatók

---

## Konfigurációs lépések {: #configuration-steps }

Az SSO konfigurálásához két fájl módosítása szükséges. Ez a rész leírja, hogyan kell mindkettőt beállítani.

### A konfigurációs fájlok áttekintése

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend bejelentkezési felület |
| **config.toml** | `/config.toml` | Backend OIDC kapcsolatok |

Mindkét fájlt be kell állítani ahhoz, hogy az SSO megfelelően működjön.

---

## Dashboard konfiguráció {: #dashboard-configuration }

### Fájl helye

```
dashboard/dashboard_config.toml
```

### 1. lépés: OIDC szolgáltatók hozzáadása

Adjunk hozzá bejegyzéseket a `[[login.oidc]]` tömbhöz minden olyan identitásszolgáltatóhoz, amelyet támogatni szeretnénk.

**Példa Microsoft és Google esetén:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Bejelentkezés Microsofttal"

[[login.oidc]]
key = "google"
label = "Bejelentkezés Google-fiókkal"
```

### 2. lépés: Bejelentkezési opciók konfigurálása

Adja meg, hogy engedélyezett-e jelszó alapú bejelentkezés:

```toml
[login]
usePassword = true
```

### Konfigurációs paraméterek

#### `[[login.oidc]]` szakasz

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Igen | Egyedi azonosító az OIDC kapcsolathoz (meg kell egyeznie a config.toml-ban található kulccsal) |
| `label` | string | Igen | A bejelentkezés gombon megjelenő szöveg (pl. "Bejelentkezés Microsofttal") |

#### `[login]` szakasz

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Engedélyezi a jelszó alapú bejelentkezést az SSO mellett |

### A usePassword megértése

**Ha `usePassword = true`:**
- A bejelentkezési képernyő megjeleníti az SSO gombokat (pl. "Bejelentkezés Microsofttal")
- A képernyőn megjelennek a felhasználónév- és jelszómezők is
- A felhasználók mindkét módszerrel autentikálhatnak
- Lehetővé teszi a hibrid beállításokat, ahol egyes felhasználók SSO-val, mások jelszóval jelentkeznek

**Ha `usePassword = false` (vagy elmarad):**
- A bejelentkezési képernyő csak az SSO gombokat mutatja
- Nincsenek felhasználónév/jelszó mezők
- Csak OIDC hitelesítés érhető el

!!! tip "Tipp"

    A jelszó alapú bejelentkezés csak azoknál a felhasználóknál érhető el, akiket jelszóval hoztak létre a `digna user add` parancs segítségével vagy a dashboardon keresztül.

### Teljes példa

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Bejelentkezés Microsofttal"

[[login.oidc]]
key = "google"
label = "Bejelentkezés Google-fiókkal"

[[login.oidc]]
key = "okta"
label = "Bejelentkezés Okta-val"
```

---

## Backend konfiguráció {: #backend-configuration }

### Fájl helye

```
/config.toml
```

(A digna telepítés gyökérkönyvtára)

### 1. lépés: OIDC szolgáltató szakaszok hozzáadása

Minden szolgáltatónak külön `[oidc.<key>]` szakasza kell legyen. A kulcsnak meg kell egyeznie a `dashboard_config.toml`-ban definiált `key` értékkel.

### Microsoft konfiguráció

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Google konfiguráció

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Konfigurációs paraméterek

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Igen | A szolgáltatótól kapott Client ID | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Igen | A szolgáltatótól kapott Client Secret | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Igen | Visszahívási URL hitelesítés után | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Igen | Az OIDC konfigurációs végpont | `https://login.microsoftonline.com/...` |

!!! warning "Fontos"

    Cserélje ki a helykitöltő értékeket (`<client_id>`, `<client_secret>`, `<tenant_id>`) a szolgáltatójától kapott valós adatokra a fejlesztői/konzolos felületen.

### Redirect URI

A redirect URI-nek meg kell egyeznie az identitásszolgáltatónál beállított értékkel:

```
http://localhost:5173/oidc/callback
```

Ha a digna más domainen fut, módosítsa ennek megfelelően:
- Local: `http://localhost:5173/oidc/callback`
- Production: `https://digna.yourdomain.com/oidc/callback`

### Teljes példa

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

## Bejelentkezés tesztelése {: #testing-login }

A konfiguráció befejezése után ellenőrizze, hogy az SSO helyesen működik.

### Előzetes ellenőrző lista

Mielőtt tesztelné:

- [ ] A `dashboard_config.toml` frissítve lett OIDC szolgáltatókkal
- [ ] A `config.toml` frissítve lett OIDC hitelesítő adatokkal
- [ ] Mindkét fájl el lett mentve
- [ ] A hitelesítő adatok helyesek (client ID, client secret)
- [ ] A redirect URI megegyezik a telepített URL-lel
- [ ] Az identitásszolgáltató alkalmazás beállítva van a redirect URI-val

### Tesztelési lépések

#### 1. lépés: Szolgáltatások újraindítása

Indítsa újra a digna backend-et és a web szervert a változtatások érvényesítéséhez.

**Windows szolgáltatásként futtatva:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Manuális futtatás esetén:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**IIS vagy Tomcat használata esetén:**
Indítsa újra a web szerver szolgáltatását.

#### 2. lépés: Dashboard megnyitása

Nyissa meg a digna dashboardot a böngészőben:

```
http://localhost:5173
```

(vagy az Ön által konfigurált dashboard URL)

#### 3. lépés: Bejelentkezési gombok ellenőrzése

Ellenőrizze, hogy megjelennek-e a bejelentkezési gombok minden konfigurált szolgáltatóhoz:

- Meg kell jelennie a "Bejelentkezés Microsofttal" gombnak
- Meg kell jelennie a "Bejelentkezés Google-fiókkal" gombnak
- (Ha usePassword = true) Meg kell jelennie a felhasználónév/jelszó mezőknek

Ha a gombok nem jelennek meg:
- Ellenőrizze, hogy a `dashboard_config.toml` el lett-e mentve
- Ellenőrizze, hogy a dashboard szolgáltatást újraindították-e
- Nézze meg a böngésző konzolját (F12) hibákért

#### 4. lépés: SSO bejelentkezés tesztelése

Kattintson valamelyik SSO gombra (például "Bejelentkezés Microsofttal"):

1. Azonosításszolgáltató bejelentkezési oldalára irányítja
2. Jelentkezzen be vállalati hitelesítő adataival
3. Visszairányít az alkalmazásba (digna)
4. Be kell legyen jelentkezve a digna-ba

#### 5. lépés: Felhasználó létrehozásának ellenőrzése

Sikeres SSO bejelentkezés után:

- A felhasználó automatikusan létrejön a digna-ban
- A felhasználó be van jelentkezve
- A felhasználói profil megjeleníti az identitásszolgáltató adatait
- Látnia kell a digna dashboardot

#### 6. lépés: Jelszavas bejelentkezés tesztelése (ha engedélyezve)

Ha `usePassword = true`:

1. Jelentkezzen ki a digna-ból
2. A bejelentkezési oldalon adja meg a felhasználónevet és jelszót
3. Jelszóval is be kell tudni jelentkezni

---

## Hibakeresés {: #troubleshooting }

### A bejelentkezési gombok nem jelennek meg

**Tünetek:**
- Az OIDC bejelentkezési gombok nem láthatóak a bejelentkezési oldalon
- Csak a jelszómezők jelennek meg (ha usePassword = true)

**Okok és megoldások:**
1. Ellenőrizze, hogy a `dashboard_config.toml` a `dashboard/` könyvtárban van-e
2. Ellenőrizze, hogy a `[[login.oidc]]` szakaszok helyes szintaxissal jelennek-e meg
3. Indítsa újra a dashboard szolgáltatást
4. Törölje a böngésző gyorsítótárát (Ctrl+Shift+Delete vagy Cmd+Shift+Delete)
5. Nézze meg a böngésző konzolját (F12 → Console fül) hibákért

---

### Redirect URI mismatch hiba

**Tünetek:**
- Az SSO gombra kattintás után "redirect_uri mismatch" jellegű hiba
- "The redirect URI is not registered" hibaüzenet

**Okok és megoldások:**
1. Ellenőrizze a `DIGNA_OIDC_REDIRECT_URI` értékét a `config.toml`-ban
2. Ellenőrizze, hogy a redirect URI regisztrálva van-e az identitásszolgáltatónál
3. Győződjön meg arról, hogy a protokoll, domain és útvonal teljesen megegyezik
4. Ellenőrizze az esetleges elgépeléseket a redirect URI-ban
5. Ha HTTPS-t használ, győződjön meg a tanúsítvány érvényességéről

---

### Érvénytelen kliens hitelesítő adatok hiba

**Tünetek:**
- "Invalid client ID or secret" jellegű hibák
- Az autentikáció a hitelesítő adatok hibájával meghiúsul

**Okok és megoldások:**
1. Ellenőrizze a `DIGNA_OIDC_CLIENT_ID` és `DIGNA_OIDC_CLIENT_SECRET` helyességét
2. Ügyeljen rá, hogy ne legyenek környező szóközök vagy nem kívánt karakterek
3. Ellenőrizze, hogy a hitelesítő adatok nem jártak le vagy lettek visszavonva
4. Indítsa újra a backend szolgáltatást a konfiguráció frissítése után
5. Nézze meg az identitásszolgáltató konzolját, hogy a hitelesítők aktívak-e

---

### A bejelentkezés lefagy vagy időtúllép

**Tünetek:**
- Az SSO gombra kattintás után semmi sem történik
- Néhány másodperc múlva időtúllépés
- A böngésző "Failed to connect" vagy hasonló üzenetet mutat

**Okok és megoldások:**
1. Ellenőrizze, hogy a digna backend fut: `digna repo check`
2. Ellenőrizze a hálózati kapcsolatot az identitásszolgáltató felé
3. Győződjön meg róla, hogy a `DIGNA_OIDC_CONFIGURATION_URL` elérhető
4. Ellenőrizze a tűzfal szabályokat, hogy engedélyezik-e a kimenő HTTPS kapcsolatokat
5. Ellenőrizze, hogy a backend és a dashboard eléri-e egymást

---

### Felhasználók nem jönnek létre automatikusan

**Tünetek:**
- Az SSO bejelentkezés sikeres, de a felhasználó nem jött létre a digna-ban
- Jogosultsági hiba SSO bejelentkezés után

**Okok és megoldások:**
1. Ellenőrizze az OIDC konfiguráció helyességét
2. Ellenőrizze a felhasználói jogosultságok beállítását
3. Tekintse át a digna logokat hibajelzésekért
4. Indítsa újra a backend szolgáltatást
5. Ha a probléma továbbra is fennáll, lépjen kapcsolatba a support@digna.ai címmel

---

## Támogatott szolgáltatók {: #supported-providers }

### Tesztelt és támogatott

Az alábbi OIDC szolgáltatókat teszteltük és működnek:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Egyéb OIDC szolgáltatók

Bármely szolgáltató, amely támogatja az OpenID Connect-et, integrálható. Szükséges információk:

- Client ID
- Client secret
- OpenID konfigurációs URL (általában `/.well-known/openid-configuration`)
- Támogatott scope-ok (általában `openid profile email`)

Ha segítségre van szüksége egy konkrét szolgáltató integrálásához, lépjen kapcsolatba a support@digna.ai címmel.

---

## Legjobb gyakorlatok

DO:
- Használjon HTTPS-t éles környezetben (ne HTTP-t)
- Tárolja biztonságosan a kliens titkokat (lehetőleg környezeti változóban)
- Rendszeresen forgassa a titkokat
- Először teszteljen nem éles környezetben
- Dokumentálja, mely szolgáltatók vannak konfigurálva
- Figyelje a bejelentkezési naplókat szokatlan aktivitásért
- Tartsa szinkronban az identitásszolgáltató konfigurációját a digna beállításokkal

DON'T:
- Ne tárolja a kliens titkokat verziókezelésben
- Ne használjon HTTP redirect URI-kat éles környezetben
- Ne konfiguráljon több szolgáltatót ugyanazzal a kulccsal
- Ne hagyjon éles környezetben alapértelmezett/teszt hitelesítő adatokat
- Ne tegye ki a konfigurációs fájlokat, amelyek titkokat tartalmaznak
- Ne keverje a fejlesztési és éles hitelesítő adatokat

---

## Támogatás

Szüksége van segítségre az SSO konfigurálásához?

- **Email:** support@digna.ai
- **Dokumentáció:** https://docs.digna.ai
- **Weboldal:** https://www.digna.ai

---

**Utolsó frissítés:** August 30, 2026  
**Kiadás:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**
