---
title: "Single Sign-On (SSO) áttekintés | digna Documentation"
description: "Hogyan működik a Single Sign-On a digna rendszeren keresztül OpenID Connect (OIDC) használatával. Lefedi a dashboard és backend beállításokat, tesztelést, hibakeresést, valamint hivatkozásokat szolgáltató-specifikus telepítési útmutatókra Microsoft Entra ID, Google Workspace, Okta, Auth0, Keycloak, OneLogin, PingOne és AD FS esetén."
image: /assets/logo_square.png
keywords:
  - "digna sso"
  - "single sign-on"
  - "oidc integráció"
  - "OpenID Connect"
  - "microsoft entra id"
  - "azure ad sso"
  - "google workspace sso"
  - "okta integráció"
  - "vállalati hitelesítés"
lang: en
robots: index, follow
og_title: digna Single Sign-On (SSO) Integration Guide
og_description: Configure Single Sign-On for digna using OpenID Connect. Step-by-step setup for Microsoft Entra ID, Google Workspace, Okta, and other OIDC-compliant identity providers.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Single Sign-On áttekintés

---

## Tartalomjegyzék

1. [Bevezetés és áttekintés](#introduction-and-overview)
2. [Szolgáltató-specifikus útmutatók](#provider-guides)
3. [Konfigurációs lépések](#configuration-steps)
4. [Dashboard konfiguráció](#dashboard-configuration)
5. [Backend konfiguráció](#backend-configuration)
6. [Bejelentkezés tesztelése](#testing-login)
7. [Hibakeresés](#troubleshooting)
8. [Támogatott szolgáltatók](#supported-providers)

---

## Bevezetés és áttekintés {: #introduction-and-overview }

Ez az útmutató lépésről lépésre bemutatja, hogyan integrálható a Single Sign-On (SSO) a digna platformon keresztül **OpenID Connect (OIDC)** használatával.

### Mi az SSO?

A Single Sign-On lehetővé teszi, hogy a felhasználók a vállalati hitelesítő adataikkal biztonságosan jelentkezzenek be a digna-ba külső identitásszolgáltatókon keresztül. A felhasználók vállalati azonosítóikkal hitelesíthetnek ahelyett, hogy külön digna jelszavakat kezelnének.

### Hogyan működik

A digna SSO az OIDC protokollt használja. Több identitásszolgáltató is párhuzamosan konfigurálható a két kulcsfontosságú konfigurációs fájl módosításával:

- **`dashboard_config.toml`** — a frontend bejelentkezési felületet szabályozza
- **`config.toml`** — a backend OIDC kapcsolatokat konfigurálja

### Támogatott szolgáltatók {: #supported-providers-overview }

Az útmutató példái **Microsoft** és **Google** használatával mutatnak be példákat, de **bármely OIDC-kompatibilis szolgáltató** integrálható ugyanazon felépítés követésével.

---

## Szolgáltató-specifikus útmutatók {: #provider-guides }

Minden szolgáltatóhoz ugyanaz a négy érték szükséges — client ID, client secret, redirect URI és discovery URL —, de ezeket a szolgáltatók admin konzoljában különböző helyeken találod, és többnek vannak szolgáltató-specifikus lépései, amelyek másoknál nem jelennek meg. Az alábbi útmutatók az admin konzolban végzendő feladatokra térnek ki; ez az oldal a digna-oldali beállításokat ismerteti, amelyek minden szolgáltatónál azonosak.

| Szolgáltató | Útmutató | Érdemes tudni |
|---|---|---|
| **AD FS** | [Set up SSO with AD FS](adfs_sso_guide.md) | Saját hosztolás; ez az egyetlen itt szereplő szolgáltató, ahol te vezérelheted a token szolgáltatást |
| **Auth0** | [Set up SSO with Auth0](auth0_sso_guide.md) | A discovery URL tenant-specifikus, és egyedi domain-ek megváltoztathatják |
| **Google Workspace** | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) | A beleegyezési képernyőt publikálni kell, mielőtt nem teszt felhasználók be tudnának jelentkezni |
| **Keycloak** | [Set up SSO with Keycloak](keycloak_sso_guide.md) | Saját hosztolás; a discovery URL realm-specifikus |
| **Microsoft Entra ID** | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | A tenant ID megjelenik a discovery URL-ben; a titkok lejárhatnak |
| **Okta** | [Set up SSO with Okta](okta_sso_guide.md) | Az authorization server választása megváltoztatja a discovery URL-t |
| **OneLogin** | [Set up SSO with OneLogin](onelogin_sso_guide.md) | Az OIDC app típust létrehozáskor kell kiválasztani, és azt nem lehet később megváltoztatni |
| **PingOne** | [Set up SSO with PingOne](pingone_sso_guide.md) | Az environment ID megjelenik a discovery URL-ben |

Bármely más OIDC-kompatibilis szolgáltató ugyanígy integrálható — lásd [Other OIDC Providers](#supported-providers).

---

## Konfigurációs lépések {: #configuration-steps }

Az SSO konfigurálásához két fájl módosítása szükséges. Ez a szakasz elmagyarázza, hogyan kell mindkettőt beállítani.

### Konfigurációs fájlok áttekintése

| Fájl | Hely | Cél |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Frontend bejelentkezési felület |
| **config.toml** | `/config.toml` | Backend OIDC kapcsolatok |

Mindkét fájlt konfigurálni kell ahhoz, hogy az SSO megfelelően működjön.

---

## Dashboard konfiguráció {: #dashboard-configuration }

### Fájl helye

```
dashboard/dashboard_config.toml
```

### 1. lépés: OIDC szolgáltatók hozzáadása

Adj bejegyzéseket a `[[login.oidc]]` tömb alá minden olyan identitásszolgáltatóhoz, amelyet támogatni szeretnél.

**Példa Microsoft és Google szolgáltatókkal:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### 2. lépés: Bejelentkezési opciók konfigurálása

Add meg, hogy engedélyezett-e a jelszóalapú bejelentkezés:

```toml
[login]
usePassword = true
```

### Konfigurációs paraméterek

#### `[[login.oidc]]` szakasz

| Paraméter | Típus | Kötelező | Leírás |
|---|---|---|---|
| `key` | string | Igen | Az OIDC kapcsolat egyedi azonosítója (meg kell egyezzen a config.toml-ban lévő kulccsal) |
| `label` | string | Igen | A bejelentkezés gombon megjelenő szöveg (pl. "Login with Microsoft") |

#### `[login]` szakasz

| Paraméter | Típus | Alapértelmezett | Leírás |
|---|---|---|---|
| `usePassword` | boolean | false | Engedélyezi a jelszóalapú bejelentkezést az SSO mellett |

### A usePassword megértése

**Ha `usePassword = true`:**
- A bejelentkezési képernyő megjeleníti az SSO gombokat (pl. "Login with Microsoft")
- A bejelentkezési képernyő megjeleníti a felhasználónév és jelszó mezőket is
- A felhasználók bármelyik módszerrel hitelesíthetnek
- Lehetővé tesz hibrid beállításokat, ahol egyes felhasználók SSO-val, mások jelszóval jelentkeznek

**Ha `usePassword = false` (vagy ki van hagyva):**
- A bejelentkezési képernyő csak az SSO gombokat mutatja
- Nincsenek felhasználónév/jelszó mezők
- Csak OIDC hitelesítés érhető el

!!! tip "Tipp"

    A jelszóalapú bejelentkezés csak azok számára érhető el, akiket jelszóval hoztak létre a `digna user add` parancs segítségével vagy a dashboardon keresztül.

### Teljes példa

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

## Backend konfiguráció {: #backend-configuration }

### Fájl helye

```
/config.toml
```

(Root digna telepítési könyvtár)

### 1. lépés: OIDC szolgáltató szakaszok hozzáadása

Minden szolgáltatónak dedikált `[oidc.<key>]` szakasza kell legyen. A kulcsnak meg kell egyeznie a `dashboard_config.toml`-ban megadott `key` értékkel.

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

| Paraméter | Típus | Kötelező | Leírás | Példa |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Igen | Client ID az identitásszolgáltatótól | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Igen | Client secret az identitásszolgáltatótól | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Igen | Callback URL a hitelesítés után | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Igen | OIDC konfigurációs végpont | `https://login.microsoftonline.com/...` |

!!! warning "Fontos"

    Cseréld ki a helyőrző értékeket (`<client_id>`, `<client_secret>`, `<tenant_id>`) a saját identitásszolgáltatód fejlesztői portálján található hitelesítő adatokra.

### Redirect URI

A redirect URI-nek meg kell egyeznie az identitásszolgáltató konfigurációjában megadottal:

```
http://localhost:5173/oidc/callback
```

Ha a digna más domainen van hosztolva, frissítsd ennek megfelelően:
- Lokális: `http://localhost:5173/oidc/callback`
- Éles: `https://digna.yourdomain.com/oidc/callback`

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

Miután befejezted a konfigurációt, ellenőrizd, hogy az SSO helyesen működik.

### Előzetes ellenőrző lista a tesztelés előtt

Győződj meg az alábbiakról:

- [ ] A `dashboard_config.toml` frissítve van az OIDC szolgáltatókkal
- [ ] A `config.toml` frissítve van az OIDC hitelesítő adatokkal
- [ ] Mindkét fájlt elmentetted
- [ ] A hitelesítő adatok helyesek (client ID, client secret)
- [ ] A redirect URI megfelel a telepítésed URL-jének
- [ ] Az identitásszolgáltató alkalmazása konfigurálva van a redirect URI-val

### Tesztelési lépések

#### 1. lépés: Szolgáltatások újraindítása

Indítsd újra a digna backend-et és a web szervert, hogy a változtatások érvénybe lépjenek.

**Ha Windows szolgáltatásként fut:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Ha Linux vagy macOS szolgáltatásként fut:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Ha kézzel futtatod:**
```bash
digna serve --address localhost --port 8082
```

**Indítsd újra a web szervert is** — IIS vagy Tomcat Windows-on, nginx vagy Apache Linuxon és macOS-en.

#### 2. lépés: Nyisd meg a Dashboardot

Nyisd meg a digna dashboardot a böngésződben:

```
http://localhost:5173
```

(vagy a beállított dashboard URL-ed)

#### 3. lépés: Ellenőrizd a bejelentkezési gombokat

Ellenőrizd, hogy megjelennek-e a bejelentkezési gombok az egyes konfigurált szolgáltatókhoz:

- Meg kell jelennie a "Login with Microsoft" gombnak
- Meg kell jelennie a "Login with Google" gombnak
- (Ha usePassword = true) Meg kell jelenniük a felhasználónév/jelszó mezőknek is

Ha a gombok nem jelennek meg:
- Ellenőrizd, hogy a `dashboard_config.toml` el lett-e mentve
- Ellenőrizd, hogy a dashboard szolgáltatás újra lett-e indítva
- Nézd meg a böngésző konzolját (F12) hibákért

#### 4. lépés: SSO bejelentkezés tesztelése

Kattints az egyik SSO gombra (pl. "Login with Microsoft"):

1. Át kell irányítania az identitásszolgáltató bejelentkezési oldalára
2. Jelentkezz be a vállalati hitelesítő adataiddal
3. Vissza kell irányítania a digna oldalára
4. Be kell legyen jelentkezve a digna rendszerbe

#### 5. lépés: Felhasználó létrehozásának ellenőrzése

Sikeres SSO bejelentkezés után:

- A felhasználónak automatikusan létre kell jönnie a digna-ban
- A felhasználónak be kell legyen jelentkezve
- A felhasználói profilban meg kell jelennie az identitásszolgáltató adatai
- Látnod kell a digna dashboardot

#### 6. lépés: Jelszó alapú bejelentkezés tesztelése (ha engedélyezve van)

Ha `usePassword = true`:

1. Jelentkezz ki a digna-ból
2. A bejelentkezési oldalon add meg a felhasználónevet és jelszót
3. Jelszóval is be kell tudnod jelentkezni

---

## Hibakeresés {: #troubleshooting }

### A bejelentkezési gombok nem jelennek meg

**Tünetek:**
- Az OIDC bejelentkezési gombok nem láthatók a bejelentkezési oldalon
- Csak a jelszó mezőket látod (ha usePassword = true)

**Okok és megoldások:**
1. Ellenőrizd, hogy a `dashboard_config.toml` a `dashboard/` könyvtárban van-e
2. Győződj meg róla, hogy a `[[login.oidc]]` szakaszok jelen vannak és helyes a szintaxis
3. Indítsd újra a dashboard szolgáltatást
4. Töröld a böngésző gyorsítótárát (Ctrl+Shift+Delete vagy Cmd+Shift+Delete)
5. Nézd meg a böngésző konzolját (F12 → Console fül) hibákért

---

### Redirect URI mismatch hiba

**Tünetek:**
- Az SSO gombra kattintás után "redirect_uri mismatch" hiba
- "The redirect URI is not registered" hibaüzenet

**Okok és megoldások:**
1. Ellenőrizd, hogy a `DIGNA_OIDC_REDIRECT_URI` a `config.toml`-ban helyes-e
2. Ellenőrizd, hogy a redirect URI regisztrálva van-e az identitásszolgáltató beállításaiban
3. Győződj meg róla, hogy mindkettő azonos URL-t használ (beleértve a protokollt, domaint, és az elérési utat)
4. Keress elírásokat a redirect URI-ban
5. Ha HTTPS-t használsz, ellenőrizd a tanúsítvány érvényességét

---

### Érvénytelen kliens hitelesítő adatok hiba

**Tünetek:**
- "Invalid client ID or secret" hiba
- A hitelesítés hitelesítő adatok hibájával meghiúsul

**Okok és megoldások:**
1. Ellenőrizd, hogy a `DIGNA_OIDC_CLIENT_ID` és `DIGNA_OIDC_CLIENT_SECRET` helyesek-e
2. Ügyelj rá, hogy ne legyenek felesleges szóközök vagy speciális karakterek
3. Ellenőrizd, hogy a hitelesítő adatok nem jártak-e le vagy nem lettek visszavonva
4. Indítsd újra a backend szolgáltatást a konfiguráció frissítése után
5. Ellenőrizd az identitásszolgáltató konzolját, hogy a hitelesítő adatok aktívak-e

---

### A bejelentkezés megakad vagy időtúllépés történik

**Tünetek:**
- Az SSO gombra kattintva semmi sem történik
- Néhány másodperc után időtúllépés
- A böngésző "Failed to connect" vagy hasonló üzenetet mutat

**Okok és megoldások:**
1. Ellenőrizd, hogy a digna backend fut-e: `digna repo check`
2. Ellenőrizd a hálózati kapcsolatot az identitásszolgáltató felé
3. Győződj meg róla, hogy a `DIGNA_OIDC_CONFIGURATION_URL` elérhető
4. Ellenőrizd a tűzfal szabályokat, hogy engedélyezik-e a kimenő HTTPS kapcsolatokat
5. Ellenőrizd, hogy a backend és a dashboard elérik-e egymást

---

### A felhasználók nem jönnek létre automatikusan

**Tünetek:**
- Az SSO bejelentkezés sikeres, de a felhasználó nem jön létre a digna-ban
- Jogosultsági hiba az SSO bejelentkezés után

**Okok és megoldások:**
1. Ellenőrizd az OIDC konfigurációt
2. Győződj meg róla, hogy a felhasználói jogosultságok megfelelően be vannak állítva
3. Nézd át a digna logokat hibaüzenetekért
4. Indítsd újra a backend szolgáltatást
5. Ha a probléma továbbra is fennáll, lépj kapcsolatba a support@digna.ai címmel

---

## Támogatott szolgáltatók {: #supported-providers }

### Tesztelt és támogatott

A következő OIDC szolgáltatókat tesztelték és működnek:

| Szolgáltató | Konfigurációs URL | Telepítési útmutató |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Set up SSO with AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Set up SSO with Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Set up SSO with Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Set up SSO with Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Set up SSO with Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Set up SSO with Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Set up SSO with OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Set up SSO with PingOne](pingone_sso_guide.md) |

### Egyéb OIDC szolgáltatók

Bármely szolgáltató, amely támogatja az OpenID Connect-et, integrálható. Szükséges információk:

- Client ID
- Client secret
- OpenID konfigurációs URL (általában `/.well-known/openid-configuration` alatt)
- Támogatott scope-ok (tipikusan `openid profile email`)

Ha segítségre van szükséged egy konkrét szolgáltató integrálásához, lépj kapcsolatba a support@digna.ai címmel.

---

## Legjobb gyakorlatok

**AJÁNLOTT:**
- Használj HTTPS-t éles környezetben (ne HTTP-t)
- Tárold biztonságosan a client secret-eket (ha lehetséges, használj környezeti változókat)
- Rendszeresen forgasd/rotáld a titkokat
- Tesztelj először nem éles környezetben
- Dokumentáld, mely szolgáltatók vannak konfigurálva
- Figyeld a bejelentkezési naplókat szokatlan tevékenységekért
- Tartsd szinkronban az identitásszolgáltató beállításait a digna konfigurációval

**NE TEDD:**
- Ne tárold a client secret-eket verziókezelésben
- Ne használj HTTP redirect URI-kat éles környezetben
- Ne konfigurálj több szolgáltatót ugyanolyan kulccsal
- Ne hagyd az alapértelmezett/teszt hitelesítő adatokat éles környezetben
- Ne tedd ki a konfigurációs fájlokat, amelyek titkokat tartalmaznak
- Ne keverd a fejlesztési és éles hitelesítő adatokat

---

## Támogatás

Szükséged van segítségre az SSO konfigurációhoz?

- **Email:** support@digna.ai
- **Dokumentáció:** https://docs.digna.ai
- **Weboldal:** https://www.digna.ai

---

**Utoljára frissítve:** 2026. augusztus 30.  
**Verzió:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**