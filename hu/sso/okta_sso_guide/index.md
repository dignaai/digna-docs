# SSO beállítása Okta-val

Az Okta OIDC-kompatibilis, de van egy buktató, amibe a legtöbb első alkalommal integrálódó belefut: egy Okta szervezet több authorization server-t is kitesz, és mindegyiknek saját discovery URL-je van.

Ez az útmutató az **Okta oldalt** fedi: az alkalmazásintegráció létrehozása és azok az értékek összegyűjtése, amelyekre a digna-nak szüksége van. A digna-oldal — `dashboard_config.toml`, tesztelés és hibakeresés — minden szolgáltatónál ugyanaz, és a [Single Sign-On áttekintésében](overview.md) van leírva.

---

## Előfeltételek

| Követelmény | Megjegyzések |
|---|---|
| **Okta szerep** | Super Administrator, vagy olyan adminisztrátori szerep, amely engedélyezi az alkalmazásintegrációk létrehozását |
| **Okta domain** | pl. `yourcompany.okta.com`, vagy egy egyedi domain, ha be van állítva |
| **digna átirányítási URI** | A bejelentkezés utáni visszatérési URL, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: Hozza létre az alkalmazásintegrációt

1. Jelentkezzen be az Okta Admin Console-ba
2. Menjen a **Applications → Applications** oldalra
3. Kattintson a **Create App Integration** gombra
4. Válassza:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Kattintson a **Next** gombra

!!! warning "Az alkalmazás típusát nem lehet megváltoztatni"

    Ha *Single-Page Application*-et választ Web Application helyett, akkor nyilvános kliens jön létre titok nélkül, és a digna backend kód-exchange lépése `invalid_client` hibával fog megbukni. A típus létrehozáskor rögzül — ha rosszul választ, törölni kell az alkalmazást és újra kezdeni.

---

## 2. lépés: Konfigurálja az integrációt

1. **App integration name**: `digna`
2. **Grant type**: hagyja kiválasztva az *Authorization Code*-ot
3. **Sign-in redirect URIs**: adja meg a digna callback URL-jét:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: opcionális
5. Az **Assignments** alatt válassza ki, kik használhatják az integrációt — egy konkrét csoport biztonságosabb, mint a *Allow everyone in your organization to access*
6. Kattintson a **Save** gombra

!!! note "Hozzárendelés szükséges"

    Az Okta hitelesíti a felhasználót, majd ellenőrzi, hogy az alkalmazáshoz hozzá van-e rendelve. Egy nem hozzárendelt felhasználó eléri az Okta bejelentkezési oldalt, sikeresen bejelentkezik, majd elutasítást kap a visszairányításnál. Ha Önnek működik a bejelentkezés, de a kollégáinak nem, a hozzárendelés az első dolog, amit ellenőrizzen.

---

## 3. lépés: Gyűjtse össze a hitelesítő adatokat

Az alkalmazás **General** fülén, a **Client Credentials** alatt:

- **Client ID** → lesz `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → lesz `DIGNA_OIDC_CLIENT_SECRET` (a titok megjelenítéséhez kattintson a szem ikonra)

---

## 4. lépés: Válassza ki az authorization servert

Ez a lépés határozza meg a discovery URL-t. Menjen a **Security → API** részre, hogy lássa a szervezetben elérhető authorization server-eket.

**Org authorization server** — a szervezet saját maga számára bocsát ki tokent:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — beleértve azt is, amit az Okta létrehoz `default` néven:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

A beépített szerver esetén `<auth_server_id>` ténylegesen `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Melyiket válasszam?"

    Használja az **org** authorization servert, hacsak a szervezet már nem szabványosít egyedi szerverre az API-hozzáférési szabályok miatt. Az Okta Developer fiókok alapértelmezettje a `default`; sok vállalati szervezet letiltja. Nyissa meg mindkét URL-t a böngészőben — amelyik JSON-t ad vissza hibák helyett, az érhető el Önnek.

---

## 5. lépés: Konfigurálja a digna-t

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

### `config.toml`

```toml
[oidc.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

A `key` mindkét fájlban meg kell egyezzen — itt `okta`.

---

## 6. lépés: Tesztelés

Indítsa újra a backendet és a web szervert, majd nyissa meg a dashboardot. A teljes ellenőrzőlistáért lásd a [Testing Login](overview.md#testing-login) részt.

---

## Okta hibakeresés

### A redirect URI nincs regisztrálva

Az Okta a hibában megnevezi a problémás URI-t. Hasonlítsa össze a **General → Sign-in redirect URIs** bejegyzésekkel; az Okta a teljes karakterláncot egyezteti, beleértve az esetleges lezáró perjelet is.

### A felhasználó nincs hozzárendelve a kliensalkalmazáshoz

A fiók nincs az alkalmazás hozzárendelési listájában. Adja hozzá a felhasználót vagy a csoportját az **Assignments** alatt.

### 400 Bad Request: Invalid Authorization Server

A discovery URL-ben szereplő `<auth_server_id>` nem létezik; leggyakrabban a `default` hiányzik azon a szervezeten. Ellenőrizze a **Security → API** résznél, hogy mely szerverek érhetők el.

### invalid_client a token lépésnél

Az integrációt Single-Page Application típusúként hozták létre, így nincs kliens titok. Hozza létre újra Web Application típusban.

---

## Kapcsolódó anyagok

- [Single Sign-On áttekintés](overview.md) — konfigurációs referencia, tesztelés és általános hibakeresés
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)