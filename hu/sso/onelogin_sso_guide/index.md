# SSO beállítása OneLogin segítségével

A OneLogin OIDC-kompatibilis. Megkülönböztető jellemzője, hogy a csatlakozó típusa az alkalmazás létrehozásakor a katalógusból választandó ki, és utólag nem változtatható meg.

Ez az útmutató a **OneLogin oldalát** fedi le: az alkalmazás létrehozása és azoknak az értékeknek az összegyűjtése, amelyekre a digna-nak szüksége van. A digna oldal — `dashboard_config.toml`, tesztelés és hibakeresés — minden szolgáltatónál azonos, és le van írva a [Single Sign-On áttekintésében](overview.md).

---

## Mielőtt elkezdené

| Követelmény | Megjegyzés |
|---|---|
| **OneLogin szerepkör** | Fióktulajdonos vagy olyan rendszergazda, akinek joga van alkalmazásokat hozzáadni |
| **Aldomain** | pl. `yourcompany.onelogin.com` |
| **digna redirect URI** | Az URL, ahová a felhasználók visszatérnek bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: OIDC alkalmazás létrehozása

1. Jelentkezzen be a OneLogin Admin portálra
2. Menjen az **Applications → Applications** menüponthoz
3. Kattintson az **Add App** gombra
4. Keressen rá az `OpenId Connect`-re és válassza az **OpenId Connect (OIDC)** csatlakozót
5. Állítsa be a **Display Name**-et `digna`-ra
6. Kattintson a **Save** gombra

!!! warning "A csatlakozó típusa a létrehozáskor rögzített"

    A OneLogin külön katalógusbejegyzéseket használ a SAML és az OIDC számára, és egy alkalmazás nem konvertálható egyik protokollról a másikra. Ha véletlenül SAML csatlakozót választ, törölje az alkalmazást és adja hozzá újra — nincs olyan beállítás, amivel protokollt lehetne váltani.

---

## 2. lépés: A Redirect URI konfigurálása

1. Nyissa meg a **Configuration** fület
2. A **Redirect URI's** mezőbe írja be a digna callback URL-jét:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcionálisan állítsa be a **Post Logout Redirect URIs** mezőt a dashboard URL-jére
4. Kattintson a **Save** gombra

!!! note "Egy URI soronként"

    Ellentétben azokkal a szolgáltatókkal, amelyek vesszővel elválasztott listát várnak, a OneLogin **Redirect URI's** mezője egy URI-t fogad soronként.

---

## 3. lépés: Az alkalmazás típusa és a hitelesítési mód beállítása

1. Nyissa meg az **SSO** fület
2. Ellenőrizze, hogy az **Application Type** *Web*
3. Állítsa a **Token Endpoint → Authentication Method**-ot *POST* (`client_secret_post`) vagy *Basic* (`client_secret_basic`) értékre

!!! warning "Ne válassza a None opciót"

    Ha az authentication method-ot *None*-ra állítja, az alkalmazás publikus klienssé válik titok nélkül, és a digna backend kódcseréjét el fogják utasítani. A POST vagy a Basic közül bármelyik működik.

---

## 4. lépés: A hitelesítő adatok összegyűjtése

Még mindig az **SSO** fülön:

- **Client ID** → lesz `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → lesz `DIGNA_OIDC_CLIENT_SECRET` (kattintson a **Show client secret**-re)

Az oldalon megjelenik az **Issuer URL** is, amely megerősíti a felfedezési (discovery) URL-t a következő lépésben.

---

## 5. lépés: Felhasználók hozzárendelése

1. Nyissa meg az **Access** fület
2. Adja hozzá azokat a szerepköröket vagy csoportokat, amelyek tagjai használhatják a digna-t
3. Kattintson a **Save** gombra

!!! note "A kioszatlan felhasználókat elutasítják bejelentkezés után"

    Mint a legtöbb szolgáltatónál, a OneLogin először hitelesíti a felhasználót, majd ellenőrzi az jogosultságot. A kioszatlan felhasználó sikeresen bejelentkezik, majd elutasítják — ez digna hibaként jelenhet meg ahelyett, hogy egyszerű hozzáférés-vezérlési döntés lenne.

---

## 6. lépés: A felfedezési (Discovery) URL összeállítása

Helyettesítse be az OneLogin aldomain-jét:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Például:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "A /2 az API verzió"

    A OneLogin jelenlegi OIDC megvalósítása az `/oidc/2/` alatt található. A régebbi dokumentációk `/oidc/` nélküli útvonalat mutatnak, ami az elavult első verzióra mutat. Ha bizonytalan, ellenőrizze az **Issuer URL**-t az SSO fülön — a felfedezési URL az issuer plusz `/.well-known/openid-configuration`.

---

## 7. lépés: A digna konfigurálása

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "onelogin"
label = "Login with OneLogin"
```

### `config.toml`

```toml
[oidc.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

A `key` mindkét fájlban meg kell egyezzen — itt `onelogin`.

---

## 8. lépés: Tesztelés

Indítsa újra a backendet és a web szervert, majd nyissa meg a dashboardot. A teljes ellenőrzőlistát lásd a [Bejelentkezés tesztelése](overview.md#testing-login) szakaszban.

---

## OneLogin hibakeresés

### `redirect_uri` nem egyezett

A callback URL hiányzik a **Configuration → Redirect URI's** mezőből, vagy az elemeket vesszővel választották el új sorok helyett.

### `invalid_client` a token lépésnél

A **Token Endpoint → Authentication Method** *None*-ra van állítva, vagy a `config.toml`-ban szereplő kliens titok elavult. Mutassa meg a titkot az **SSO** fülön és hasonlítsa össze.

### Az alkalmazás nem jelenik meg a felhasználóknál

Egyetlen szerepkörnek vagy csoportnak sem lett hozzáadva hozzáférés az **Access** fülön.

### 404 a felfedezési URL-en

Az aldomain hibás, vagy az URLből hiányzik a `/oidc/2/`. Hasonlítsa össze az **Issuer URL**-lel az SSO fülön.

---

## Lásd még

- [Single Sign-On áttekintés](overview.md) — konfigurációs referencia, tesztelés és általános hibakeresés
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)