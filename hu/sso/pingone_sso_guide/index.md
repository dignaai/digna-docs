# SSO beállítása PingOne-nal

A PingOne OIDC-kompatibilis. Két értékre kell különösen figyelni: a **Environment ID**, amely minden végpont URL-jében megjelenik, és a **regionális domain**, amely eltér az észak-amerikai, európai, kanadai, ázsia-csendes-óceáni és ausztrál bérlők esetén.

Ez az útmutató a **PingOne-oldalt** fedi le: az alkalmazás létrehozását és azokat az értékeket, amelyeket a digna igényel. A digna-oldal — `dashboard_config.toml`, tesztelés és hibaelhárítás — minden szolgáltatónál ugyanaz, és a [Single Sign-On áttekintés](overview.md) ismerteti.

---

## Mielőtt elkezdi

| Követelmény | Megjegyzések |
|---|---|
| **PingOne szerepkör** | Environment Admin vagy Identity Data Admin a célnak megfelelő környezetben |
| **Environment** | Az a PingOne-környezet, amelyhez a digna felhasználói tartoznak |
| **digna redirect URI** | Az a URL, amelyre a felhasználók visszatérnek bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: Alkalmazás létrehozása

1. Jelentkezzen be a PingOne admin konzolba és válassza ki a környezetet
2. Menjen az **Applications → Applications** részhez
3. Kattintson a **+** gombra
4. Adja meg a `digna` nevet **Application Name**-ként
5. Válassza az **OIDC Web App** típust
6. Kattintson a **Save** gombra

!!! warning "Válassza az OIDC Web App típust, ne a Single-Page App-ot"

    *Single-Page App* és *Native App* nyilvános klienset hoznak létre, amelyek nem tárolhatnak titkot. A digna a backendjéből cseréli az authorization code-ot, ezért szüksége van a titkosított, azaz a **OIDC Web App** típusra.

---

## 2. lépés: Az átirányítási URI konfigurálása

1. Nyissa meg az alkalmazás **Configuration** fülét
2. Kattintson a ceruza ikonra a szerkesztéshez
3. Ellenőrizze, hogy a **Response Type** *Code*, a **Grant Type** pedig *Authorization Code*
4. A **Redirect URIs** mezőbe adja meg a digna callback URL-jét:

```
https://digna.yourdomain.com/oidc/callback
```

5. Állítsa a **Token Endpoint Authentication Method** értékét *Client Secret Post* vagy *Client Secret Basic* értékre
6. Kattintson a **Save** gombra

---

## 3. lépés: Az alkalmazás engedélyezése

Az alkalmazás sorában vagy részletező paneljén kapcsolja be a toggle-t **enabled** állásba.

!!! warning "Az új alkalmazások alapértelmezés szerint le vannak tiltva"

    A PingOne az alkalmazásokat alapértelmezés szerint letiltott állapotban hozza létre. A letiltott alkalmazás a jogosultság megadásakor olyan hibát ad, amely nem említi a kapcsolót, ezért érdemes ezt először ellenőrizni, mielőtt mást hibakeresne.

---

## 4. lépés: Jogosultságok (scopes) megadása

1. Nyissa meg a **Resources** fület
2. Győződjön meg róla, hogy az `openid` engedélyezve van, majd adja hozzá a `profile` és `email` scope-okat az **OpenID Connect** erőforrásból
3. Kattintson a **Save** gombra

---

## 5. lépés: Felhasználók hozzárendelése

1. Nyissa meg az **Access** fület
2. Adja hozzá azt a populációt vagy csoportokat, amelyek tagjai használhatják a dignát
3. Kattintson a **Save** gombra

---

## 6. lépés: Hitelesítő adatok és az Environment ID begyűjtése

A **Configuration** fülön bontsa ki a **General** részt:

- **Client ID** → bekerül `DIGNA_OIDC_CLIENT_ID`-be
- **Client Secret** → bekerül `DIGNA_OIDC_CLIENT_SECRET`-be (kattintson a szem ikonra)
- **Environment ID** → a discovery URL-hez szükséges

Ugyanezen a fülön megtalálható a kész **OIDC Discovery Endpoint**, amelyet közvetlenül másolhat a kézi összerakás helyett.

---

## 7. lépés: A discovery URL összeállítása

Helyettesítse be az Environment ID-t és a régiójának megfelelő domaint:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Régió | Domain |
|---|---|
| Észak-Amerika | `auth.pingone.com` |
| Európa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Ázsia-Csendes-óceán | `auth.pingone.asia` |
| Ausztrália | `auth.pingone.com.au` |

Egy európai környezethez:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Másolja, ne gépelje be"

    A regionális domain a PingOne integráció leggyakoribb hibaforrása, és a rossz régió 404-et ad vissza, nem pedig hasznos üzenetet. Használja a 6. lépésben megjelenített **OIDC Discovery Endpoint** értékét.

---

## 8. lépés: digna konfigurálása

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Bejelentkezés PingOne segítségével"
```

### `config.toml`

```toml
[oidc.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<a 6. lépésben másolt kliens titok>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

A `key` értékének mindkét fájlban egyeznie kell — itt ez `pingone`.

---

## 9. lépés: Tesztelés

Indítsa újra a backendet és a webszervert, majd nyissa meg a dashboardot. A teljes ellenőrző listáért lásd a [Bejelentkezés tesztelése](overview.md#testing-login) részt.

---

## Hibaelhárítás PingOne esetén

### 404 a Discovery URL-en

A regionális domain vagy az Environment ID hibás. Hasonlítsa össze a **OIDC Discovery Endpoint** értékével az alkalmazás Configuration fülén.

### NOT_FOUND vagy az alkalmazás le van tiltva

Az alkalmazás kapcsolója a 3. lépésben még ki van kapcsolva.

### Redirect URI mismatch

A PingOne a teljes stringet egyezteti. Ellenőrizze a **Configuration → Redirect URIs** mezőt a végződő perjel vagy a séma eltérés miatt.

### A bejelentkezés sikeres, de az email claim nem érkezik meg a dignához

Nem lettek engedélyezve az `email` és `profile` scope-ok a **Resources** fülön.

### A felhasználó nem látja az alkalmazást

Nincs hozzáadva populáció vagy csoport az **Access** fülön.

---

## Lásd még

- [Single Sign-On áttekintés](overview.md) — konfigurációs referencia, tesztelés és általános hibaelhárítás
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)