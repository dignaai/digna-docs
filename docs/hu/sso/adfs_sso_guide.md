---
title: AD FS SSO – Single Sign-On integráció | digna dokumentáció
description: Configure Single Sign-On for digna with Active Directory Federation Services using OpenID Connect — application group, server application, shared secret, permitted scopes and the matching digna configuration.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, active directory federation services, adfs oidc, application group, openid connect, on-premises identity provider
---

# SSO beállítása AD FS-sel

Az Active Directory Federation Services az on-premises opció: a saját szervere(i)d bocsátják ki a tokeneket, és a discovery URL a saját hostneved lesz. Az AD FS az **OpenID Connect**-et a **Windows Server 2016** verziótól támogatja.

Ez a leírás az **AD FS oldalát** fedi: az alkalmazáscsoport létrehozása és azoknak az értékeknek az összegyűjtése, amire a dignának szüksége van. A digna oldala — `dashboard_config.toml`, tesztelés és hibakeresés — minden szolgáltatónál ugyanaz, és a [Single Sign-On Overview](overview.md) fejezetben található.

---

## Mielőtt elkezdené

| Követelmény | Megjegyzés |
|---|---|
| **AD FS verzió** | Windows Server 2016 vagy újabb — korábbi verziókban nincs OIDC támogatás |
| **Hozzáférés** | Helyi rendszergazda az AD FS szerveren |
| **Federációs szolgáltatás neve** | pl. `adfs.yourdomain.com` |
| **digna átirányítási URI** | Az a URL, ahova a felhasználók visszatérnek bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: Alkalmazáscsoport létrehozása

1. Az AD FS szerveren nyissa meg az **AD FS Management**-et
2. Kattintson jobb gombbal az **Application Groups**-ra, majd válassza az **Add Application Group**-ot
3. Adja meg a nevet: `digna`
4. Válassza a **Standalone applications** — vagy a **Client-Server applications** lehetőséget a verziótól függően — majd jelölje ki a **Server application accessing a web API** opciót
5. Kattintson a **Next** gombra

---

## 2. lépés: A szerveralkalmazás konfigurálása

1. **Name**: `digna backend`
2. **Client Identifier**: az AD FS generál egy GUID-ot. Másolja ki — ez lesz a `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: adja meg a digna callback URL-jét és kattintson az **Add**-ra:

```
https://digna.yourdomain.com/oidc/callback
```

4. Kattintson a **Next** gombra

!!! warning "Kattintson az Add gombra, ne csak a Next-re"

    A redirect URI mezőhöz külön **Add** gomb tartozik. Ha beírja az URI-t és a **Next**-re kattint anélkül, hogy az **Add**-ot megnyomná, az URI elveszik, és a varázsló nem figyelmeztet. Győződjön meg róla, hogy az URI megjelenik a mező alatti listában, mielőtt tovább lép.

---

## 3. lépés: A megosztott titok generálása

1. Jelölje be a **Generate a shared secret** opciót
2. Másolja ki a generált titkot → ez lesz a `DIGNA_OIDC_CLIENT_SECRET`
3. Kattintson a **Next** gombra

!!! warning "A titok csak egyszer látható"

    Az AD FS ezt a megosztott titkot csak ezen a varázslóoldalon jeleníti meg, később nem tudja újra megmutatni. Ha elveszti, később az alkalmazáscsoport tulajdonságaiból állítsa vissza.

---

## 4. lépés: A Web API konfigurálása

1. **Identifier**: adja meg ugyanazt a kliens azonosítót, amelyet a 2. lépésben kapott, majd kattintson az **Add**-ra
2. Kattintson a **Next** gombra
3. Válasszon egy **Access Control Policy**-t — a *Permit everyone* a legegyszerűbb kiindulási pont; éles környezetben szűkítse egy csoporthoz
4. Kattintson a **Next** gombra

---

## 5. lépés: A megengedett scope-ok engedélyezése

A **Configure Application Permissions** lépésen jelölje be:

- `openid`
- `profile`
- `email`

Ezután kattintson a **Next**-re és fejezze be a varázslót.

!!! warning "Az openid nincs alapértelmezés szerint bejelölve"

    Egyes verziókban az AD FS csak a `user_impersonation`-t jelöli ki alapból. `openid` nélkül a token endpoint OAuth access token-t ad vissza az ID token helyett, és a digna nem tudja azonosítani a felhasználót.

---

## 6. lépés: A discovery végpont ellenőrzése

Helyettesítse be a saját federációs szolgáltatás nevét:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Például:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Nyissa meg egy böngészőben. Egy JSON dokumentum megerősíti, hogy az OIDC engedélyezve van és a hostnév helyes.

!!! note "A backendnek megbíznia kell a tanúsítványban"

    Belső tanúsítványkibocsátó gyakori AD FS telepítéseknél. A digna backendet futtató gép saját kimenő HTTPS hívást indít erre az URL-re, ezért az aláíró CA-nak szerepelnie kell annak a gépnek a megbízható tanúsítványtárában — nem elég, ha csak a bejelentkezők böngészőiben van telepítve.

---

## 7. lépés: digna konfigurálása

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Login with Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the shared secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

A `key` mindkét fájlban egyezzen — itt `adfs`.

---

## 8. lépés: Tesztelés

Indítsa újra a backendet és a webszervert, majd nyissa meg a dashboardot. A teljes ellenőrzőlistát lásd a [Testing Login](overview.md#testing-login) szakaszban.

---

## AD FS hibakeresés

### MSIS9611: The Client Is Not Allowed to Access the Resource

A web API azonosító a 4. lépésben nem egyezik a kliens azonosítóval, vagy a 5. lépésben nem lettek megadva a szükséges scope-ok. Mindkettő szerkeszthető az alkalmazáscsoport tulajdonságaiban.

### MSIS9602: Invalid redirect_uri

Az URI be volt írva, de nem adták hozzá az **Add** gombbal, vagy eltér a `DIGNA_OIDC_REDIRECT_URI`-től. Ellenőrizze: **Application Groups → digna → digna backend → Properties**.

### Nincs visszaadva ID token

Hiányzik az `openid` scope az alkalmazásengedélyek közül.

### A backend nem éri el a discovery URL-t

Vagy a backend hoszt DNS-e nem oldja fel a federációs szolgáltatás nevét, vagy az AD FS tanúsítvány nincs megbízhatóként beállítva ott. Tesztelje a következővel a digna szerverről:

curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration

### Események, amelyeket érdemes ellenőrizni

Az AD FS szerver az Event Viewerben az **Applications and Services Logs → AD FS → Admin** alatt rögzíti a hibákat, általában konkrétabb oka van, mint amit a böngésző mutat.

---

## Lásd még

- [Single Sign-On Overview](overview.md) — konfigurációs referencia, tesztelés és általános hibakeresés
- [Microsoft: AD FS OpenID Connect scenarios](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)