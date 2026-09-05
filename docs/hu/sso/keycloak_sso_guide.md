---
title: Keycloak SSO – Single Sign-On integráció | digna Dokumentáció
description: Konfigurálja a Single Sign-On-t a digna számára Keycloakdal OpenID Connect használatával — realm és kliens beállítása, kliens hitelesítés, érvényes átirányítási URI-k, kliens titok és a megfelelő digna konfiguráció.
image: /assets/logo_square.png
keywords: digna sso, keycloak sso, keycloak oidc, realm, confidential client, openid connect, önállóan üzemeltetett identitásszolgáltató
---

# SSO beállítása Keycloakkal

A Keycloak egy önállóan üzemeltetett, teljes mértékben OIDC-kompatibilis identitásszolgáltató. Mivel Ön üzemelteti, a discovery URL a saját hosztnevéből és realmjéből épül fel, nem egy szolgáltató domainjéből.

Ez az útmutató a **Keycloak-oldalt** fedi le: a kliens létrehozását és azokat az értékeket gyűjti össze, amelyekre a dignának szüksége van. A digna-oldal — `dashboard_config.toml`, tesztelés és hibakeresés — minden szolgáltató esetén ugyanaz, és a [Single Sign-On áttekintésében](overview.md) található.

---

## Mielőtt elkezdi

| Követelmény | Megjegyzés |
|---|---|
| **Keycloak verzió** | 17 vagy újabb a használt URL-útvonalakhoz — lásd a 4. lépés megjegyzését |
| **Keycloak szerepkör** | `realm-admin` a céltárhelyen (realm), vagy szerveradminisztrátor |
| **Realm** | Az a realm, amelyhez a digna felhasználói tartoznak — nem feltétlenül a `master` |
| **digna átirányítási URI** | Az az URL, ahova a felhasználók visszatérnek bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: Válassza ki a realmet

1. Nyissa meg a Keycloak admin konzolt
2. Használja a bal felső sarokban található realm választót, és válts arra a realmre, amelyben a felhasználói vannak

!!! warning "Ne használja a `master` realmet"

    A `master` realm a Keycloak adminisztrációjára szolgál. Az alkalmazásklienseknek külön realmben kell lenniük; ha a dignát a `master`-be teszi, annak felhasználói hozzáférést kapnak a Keycloak admin konzoljához.

---

## 2. lépés: Hozza létre a klienst

1. Menjen a **Clients** menüponthoz, és kattintson a **Create client** gombra
2. Konfigurálja:
   - **Client típusa**: *OpenID Connect*
   - **Client ID**: `digna` — ez lesz `DIGNA_OIDC_CLIENT_ID`
3. Kattintson a **Next** gombra
4. A **Capability config** lépésnél kapcsolja be a **Client authentication** opciót (**On**)
5. Hagyja engedélyezve a **Standard flow**-t; a többi flow nem szükséges
6. Kattintson a **Next** gombra

!!! warning "A Client authentication-nek be kell lennie kapcsolva"

    Ha a **Client authentication** ki van kapcsolva, a Keycloak *public* klienst hoz létre, amelynek nincsenek hitelesítő adatai — a 4. lépésben szereplő **Credentials** fül nem fog megjelenni. A digna számára egy confidential kliens szükséges. Ezt a beállítást a létrehozás után is meg lehet változtatni, ha hibázik.

---

## 3. lépés: Állítsa be az átirányítási URI-t

A **Login settings** lépésnél (vagy később a **Settings** fülön):

1. **Valid redirect URIs**: adja meg a digna callback URL-jét:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: hagyja üresen, vagy állítsa `+`-ra, hogy tükrözze az átirányítási URI-kat
3. Kattintson a **Save** gombra

!!! tip "Kerülje a helyettesítő karaktereket (wildcardokat)"

    A Keycloak elfogad mintákat, például `https://digna.yourdomain.com/*`. A wildcard bármely útvonalat engedélyez azon a hoszton az engedélyezett átirányításhoz, ezért előnyösebb a pontos callback URL megadása.

---

## 4. lépés: Szerezze be a kliens titkot

1. Nyissa meg a **Credentials** fület
2. Győződjön meg róla, hogy a **Client Authenticator** *Client Id and Secret*
3. Másolja ki a **Client secret** értéket → ez lesz `DIGNA_OIDC_CLIENT_SECRET`

A titok innen bármikor lekérdezhető, és szükség esetén a **Regenerate** gombbal újragenerálható.

---

## 5. lépés: Építse fel a discovery URL-t

Helyettesítse be a Keycloak hosztját és a realm nevét:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Például:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "A Keycloak 16 és korábbi verziók az /auth előtagot tartalmazzák"

    Keycloak 17 előtt minden végpont az `/auth` előtag alatt volt:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Azok a disztribúciók, amelyeknél be van állítva a `KC_HTTP_RELATIVE_PATH=/auth`, a jelenlegi verziókon is megtartják a régi elrendezést. Ha az `/auth` nélküli URL 404-et ad vissza, próbálja meg az előtaggal is.

Nyissa meg az URL-t a böngészőben a folytatás előtt. Egy JSON dokumentum megerősíti, hogy a hoszt és a realm helyes.

---

## 6. lépés: Konfigurálja a dignát

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Bejelentkezés Keycloak-kal"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

A `key` mindkét fájlban meg kell, hogy egyezzen — itt `keycloak`. Jegyezze meg, hogy nem szükséges, hogy megegyezzen a Keycloak **Client ID**-vel, bár könnyebb követni, ha ugyanaz.

---

## 7. lépés: Tesztelés

Indítsa újra a háttérszolgáltatást és a web szervert, majd nyissa meg a dashboardot. A teljes ellenőrző listáért lásd a [Testing Login](overview.md#testing-login) részt.

---

## Keycloak hibakeresés

### Invalid parameter: redirect_uri

Az átirányítási URL nincs benne a **Valid redirect URIs** listában. A Keycloak a szerverlogban naplózza a fogadott URI-t, ez a legegyszerűbb módja a pontos eltérés megtekintésének.

### Hiányzik a Credentials fül

A kliens public. Kapcsolja be a **Client authentication** opciót a **Settings → Capability config** alatt.

### 404 a discovery URL-en

Vagy a realm neve helytelen, vagy a telepítés az `/auth` előtagot használja. Ellenőrizze a realm listát az admin konzolban, és próbálja mindkét URL-formát.

### unauthorized_client vagy invalid_client

A **Standard flow** ki van kapcsolva a **Capability config** alatt, vagy a titkot újragenerálták a Keycloakban anélkül, hogy frissítették volna a `config.toml`-t.

### Tanúsítványhibák a háttérből

Egy önállóan üzemeltetett Keycloak privát vagy önaláírt tanúsítvánnyal meghiúsíthatja a digna backend kimenő HTTPS hívását a discovery URL-re. Telepítse a kibocsátó CA-t abba a trust store-ba, ahol a digna backendet futtató gép megbízik benne.

---

## Kapcsolódó hivatkozások

- [Single Sign-On áttekintés](overview.md) — konfigurációs referencia, tesztelés és általános hibakeresés
- [Keycloak: Securing applications](https://www.keycloak.org/docs/latest/securing_apps/)