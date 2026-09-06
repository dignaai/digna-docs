# SSO beállítása Auth0-val

Az Auth0 OIDC-kompatibilis és tenantonként kitesz egy discovery végpontot. A legfontosabb, hogy helyesen adja meg a tenant domain-t, mert ez szerepel a discovery URL-ben és megváltozik, ha egyedi domaint engedélyez.

Ez az útmutató az **Auth0-oldalt** fedi le: az alkalmazás létrehozását és azoknak az értékeknek az összegyűjtését, amelyeket a digna igényel. A digna-oldal — a `dashboard_config.toml`, a tesztelés és a hibakeresés — minden szolgáltatónál ugyanaz, és a [Single Sign-On áttekintés](overview.md) oldalon található.

---

## Mielőtt elkezdené

| Követelmény | Megjegyzés |
|---|---|
| **Auth0 szerepkör** | Admin a tenanton |
| **Tenant domain** | pl. `yourcompany.eu.auth0.com` — a régió szegmens számít |
| **digna redirect URI** | Az URL, ahová a felhasználó visszatér bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: Alkalmazás létrehozása

1. Jelentkezzen be az [Auth0 Dashboard](https://manage.auth0.com) oldalra
2. Menjen a **Applications → Applications** részre
3. Kattintson a **Create Application** gombra
4. Nevezze el `digna`-nak és válassza a **Regular Web Applications** típust
5. Kattintson a **Create** gombra

!!! warning "Válassza a Regular Web Applications típust"

    *Single Page Application* és *Native* nyilvános klienseket hoznak létre titok nélkül. A digna a backendjéről végzi a kódcserét, és titkosított (confidential) kliensre van szüksége, ezért a helyes típus a **Regular Web Applications**. Ellentétben néhány szolgáltatóval, az Auth0 lehetővé teszi a típus későbbi megváltoztatását a **Settings → Application Type** alatt.

---

## 2. lépés: Callback URL hozzáadása

Az alkalmazás **Settings** fülén:

1. Keresse meg az **Allowed Callback URLs** mezőt
2. Adja meg a digna callback URL-jét:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcionálisan állítsa be az **Allowed Logout URLs** mezőt a dashboard URL-jére
4. Görgessen le és kattintson a **Save Changes** gombra

!!! note "Vesszővel elválasztva, ne új sorral"

    Az Auth0 több callback URL-t is elfogad ebben a mezőben, vesszővel elválasztva. Új sorokkal elválasztott lista egyetlen hibás URL-ként olvasódik be, és csendben nem egyezik semmivel.

---

## 3. lépés: Hitelesítő adatok összegyűjtése

Ugyanitt, a **Settings** alatt, a **Basic Information** panelben:

- **Domain** → ide kerül a discovery URL
- **Client ID** → ez lesz a `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → ez lesz a `DIGNA_OIDC_CLIENT_SECRET` (kattintson a megjelenítéshez)

---

## 4. lépés: Ellenőrizze a Grant Type-ot

1. Menjen a **Settings → Advanced Settings → Grant Types** részre
2. Ellenőrizze, hogy az **Authorization Code** be van-e pipálva

Ez alapértelmezés szerint engedélyezett a Regular Web Applications esetén. Ha ki van véve a pipából, a digna bejelentkezés `unauthorized_client` hibával meghiúsul.

---

## 5. lépés: Discovery URL összeállítása

Helyettesítse a 3. lépésben megadott **Domain**-t:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Például:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Az egyedi domainek megváltoztatják az issuer-t"

    Ha a tenant egyedi domain-t használ, például `login.yourcompany.com`, azt a domaint használja a discovery URL-ben. Ha keveri a kettőt — a canonical domain a discovery URL-ben, az egyedi domain a böngészőben — issuer mismatch történik, és a token elutasításra kerül egy egyébként sikeres bejelentkezés után.

---

## 6. lépés: digna konfigurálása

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Bejelentkezés Auth0-val"
```

### `config.toml`

```toml
[oidc.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

A `key` mindkét fájlban meg kell, hogy egyezzen — itt `auth0`.

---

## 7. lépés: Tesztelés

Indítsa újra a backendet és a web szervert, majd nyissa meg a dashboardot. A teljes ellenőrzőlistát lásd a [Testing Login](overview.md#testing-login) résznél.

---

## Auth0 hibakeresés

### Callback URL eltérés

Az Auth0 hibaképe megnevezi a kapott URL-t. Adja hozzá az **Allowed Callback URLs**-hez, ügyelve rá, hogy az elemek vesszővel legyenek elválasztva.

### unauthorized_client

Az **Authorization Code** nincs engedélyezve az **Advanced Settings → Grant Types** alatt, vagy az alkalmazás típusa nem Regular Web Applications.

### Hozzáférés megtagadva sikeres bejelentkezés után

A tenantban lévő Rule, Action vagy Post-Login trigger elutasítja a felhasználót. Ellenőrizze az **Actions → Flows → Login** részt és a tenant logjait a **Monitoring → Logs** alatt, amelyek pontos okot mutatják.

### Issuer mismatch

A discovery URL és az a domain, amelyre a böngészőt irányították, eltérnek — általában a canonical tenant domain és az egyedi domain közötti eltérés. Használjon mindig egy konzisztens domaint.

---

## Lásd még

- [Single Sign-On áttekintés](overview.md) — konfigurációs referencia, tesztelés és általános hibakeresés
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)