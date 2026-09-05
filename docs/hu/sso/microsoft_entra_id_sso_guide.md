---
title: Microsoft Entra ID SSO – Single Sign-On integráció | digna dokumentáció
description: Konfigurálja a Single Sign-On-t a digna számára Microsoft Entra ID-vel (korábban Azure AD) OpenID Connect használatával — alkalmazásregisztráció, átirányítási URI, kliens titok, tenant ID és a hozzáillő digna konfiguráció.
image: /assets/logo_square.png
keywords: digna sso, Microsoft Entra ID, Azure AD SSO, OIDC integráció, app regisztráció, vállalati hitelesítés
---

# SSO beállítása Microsoft Entra ID-vel

A Microsoft Entra ID (korábban Azure Active Directory) teljesen OIDC-kompatibilis szolgáltató, így a digna a szabványos discovery végponton keresztül integrálható vele.

Ez az útmutató az **Entra ID oldalt** fedi: az alkalmazás regisztrálását és a digna által igényelt négy érték összegyűjtését. A digna-oldal — `dashboard_config.toml`, tesztelés és hibaelhárítás — minden szolgáltatónál azonos, és a [Single Sign-On Overview](overview.md) dokumentumban található.

---

## Mielőtt elkezdi

| Követelmény | Megjegyzések |
|---|---|
| **Entra ID szerepkör** | Application Administrator, Cloud Application Administrator vagy Global Administrator |
| **digna átirányítási URI** | Az URL, ahová a felhasználók visszatérnek bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Az a könyvtár (directory), amelybe a felhasználói bejelentkeznek |

---

## 1. lépés: Alkalmazás regisztrálása

1. Jelentkezzen be a [Microsoft Entra admin központba](https://entra.microsoft.com)
2. Menjen a **Identity → Applications → App registrations** részre
3. Kattintson a **New registration**-re
4. Konfigurálja:
   - **Name**: `digna` (a felhasználóknak megjelenő név a hozzájárulási képernyőn)
   - **Supported account types**: *Accounts in this organizational directory only* egyetlen tenant telepítéshez
5. A **Redirect URI** alatt válassza a platformot **Web** és adja meg a digna callback URL-jét:

```
https://digna.yourdomain.com/oidc/callback
```

6. Kattintson a **Register**-re

!!! warning "Fontos"

    A platformnak **Web**-nek kell lennie, nem *Single-page application*. A digna a backendről cseréli le az authorization code-ot egy kliens titokra, amit a SPA platform típus nem engedélyez.

---

## 2. lépés: A kliens és tenant ID gyűjtése

Az alkalmazás **Overview** oldalán másolja ki:

- **Application (client) ID** → ebből lesz a `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → ez kerül a discovery URL-be

---

## 3. lépés: Kliens titok létrehozása

1. Menjen a **Certificates & secrets → Client secrets**
2. Kattintson a **New client secret**-re
3. Adjon meg egy leírást és válasszon lejáratot
4. Kattintson az **Add**-ra
5. Másolja ki rögtön a **Value** oszlopot

!!! warning "Másolja a Value-t, ne a Secret ID-t"

    A **Value** csak egyszer jelenik meg, ezen az oldalon, és később nem nyerhető vissza. A mellette látható **Secret ID** hasonló kinézetű, de nem a titok — ha azt használja, `invalid_client` hibát kap bejelentkezéskor. Ha elnavigál az oldalról a másolás nélkül, törölje a titkot és hozzon létre újat.

!!! tip "Tipp"

    Az Entra ID maximálisan 24 hónapra korlátozza a titok élettartamát, így minden SSO integrációnak lesz lejárati ideje. Jegyezze fel egy jól látható helyre — egy lejárt titok egyszerre minden felhasználó SSO-ját leállítja, a bejelentkezési oldalon nincs előzetes figyelmeztetés.

---

## 4. lépés: API jogosultságok megerősítése

1. Menjen az **API permissions** részre
2. Ellenőrizze, hogy a **Microsoft Graph → User.Read** (delegated) jelen van — ez alapértelmezés szerint hozzáadásra kerül

Az `openid`, `profile` és `email` scope-ok, amelyeket a digna kér, az OIDC szabvány részei, és külön engedélyezést nem igényelnek. Ha a tenantja megköveteli az admin hozzájárulást minden alkalmazásra, kattintson a **Grant admin consent for <tenant>**-re.

---

## 5. lépés: Discovery URL összeállítása

Helyettesítse a 2. lépésben szerzett **Directory (tenant) ID**-t:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Használja a v2.0 végpontot"

    A `/v2.0/` szegmens számít. A v1.0 végpont (`https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration`) régebbi formátumban ad tokeneket, és nem adja vissza a standard OIDC claim-eket, amelyeket a digna elvár.

Nyissa meg a URL-t a böngészőben a folytatás előtt. Egy JSON dokumentum megerősíti, hogy a tenant ID helyes.

---

## 6. lépés: digna konfigurálása

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Bejelentkezés Microsoft-fiókkal"
```

### `config.toml`

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

A `key` mindkét fájlban meg kell, hogy egyezzen — itt `microsoft`.

---

## 7. lépés: Tesztelés

Indítsa újra a backendet és a webszervert, majd nyissa meg a dashboardot. A teljes ellenőrzőlistáért lásd a [Testing Login](overview.md#testing-login) részt.

---

## Hibaelhárítás Entra ID esetén

### AADSTS50011: Redirect URI Mismatch

A `DIGNA_OIDC_REDIRECT_URI`-ben szereplő URI eltér a 1. lépésben regisztráltól. Az Entra ID a teljes stringet hasonlítja össze, így egy záróperjel, `http` versus `https`, vagy más port is eltérésnek számít. Ellenőrizze az **Authentication → Web → Redirect URIs** beállítást.

### AADSTS7000215: Invalid Client Secret

Vagy a **Secret ID** lett véletlenül másolva a **Value** helyett, vagy a titok lejárt. Hozzon létre egy új titkot és másolja ki a Value oszlopot.

### AADSTS650057: Invalid Resource

Az alkalmazásregisztráció törölve lett, vagy más tenanthez tartozik, mint amely a discovery URL-ben szerepel. Ellenőrizze a Directory (tenant) ID-t az Overview oldalon.

### A felhasználók bejelentkeznek, de semmi sem történik

Ha a tenantja admin hozzájárulást követel és ez nincs megadva, az átirányítás visszatér anélkül, hogy használható tokent kapnának. Adja meg az admin hozzájárulást az **API permissions** alatt.

---

## Lásd még

- [Single Sign-On Overview](overview.md) — konfigurációs referencia, tesztelés és általános hibaelhárítás
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)