# SSO beállítása Google Workspace-szel

A Google identitásplatformja OIDC-kompatibilis, és minden ügyfélhez ugyanazt a jól ismert discovery URL-t használja, így az egyes szervezetekre vonatkozó egyedi értékek csak a kliensazonosító (client ID) és a titok (secret).

Ez az útmutató a **Google-oldalt** fedi le: az OAuth kliens létrehozását és a digna számára szükséges értékek begyűjtését. A digna-oldal — a `dashboard_config.toml`, tesztelés és hibakeresés — minden szolgáltatónál ugyanaz, és a [Single Sign-On áttekintés](overview.md) dokumentumban található.

---

## Mielőtt elkezdi

| Követelmény | Megjegyzés |
|---|---|
| **Google Cloud projekt** | Bármely projekt ugyanabban a szervezetben, mint a Workspace domain |
| **Szerepkör** | Editor vagy Owner a projekten |
| **digna átirányítási URI** | Az URL, ahová a felhasználók visszatérnek bejelentkezés után, pl. `https://digna.yourdomain.com/oidc/callback` |

---

## 1. lépés: Az OAuth hozzájárulási képernyő konfigurálása

A Google nem ad ki hitelesítő adatokat, amíg a hozzájárulási képernyő nem létezik.

1. Nyissa meg a [Google Cloud Console](https://console.cloud.google.com) oldalt, és válassza ki a projektjét
2. Menjen az **APIs & Services → OAuth consent screen** oldalra
3. Válassza ki a felhasználótípust:
   - **Internal** — csak a Workspace domainen belüli fiókok jelentkezhetnek be. Ajánlott.
   - **External** — bármely Google-fiók megkísérelheti a bejelentkezést.
4. Töltse ki az alkalmazás nevét, a támogatási e-mailt és a fejlesztői kapcsolattartó e-mailjét
5. A **Scopes** lépésnél adja hozzá az `openid`, `.../auth/userinfo.email` és `.../auth/userinfo.profile` scope-okat
6. Mentés

!!! warning "A külső alkalmazásokat közzé kell tenni"

    Egy **External** hozzájárulási képernyő *Testing* státusszal indul, ilyenkor csak azok a fiókok tudnak befejezni egy bejelentkezést, melyeket kifejezetten hozzáadtak a tesztfelhasználók listájához. Mindenki más ezt látja: "digna has not completed the Google verification process". Vagy állítsa az alkalmazást **In production** státuszra a **Publishing status** alatt, vagy használja az **Internal** típust — ennek nincs ilyen korlátozása, és Workspace-only telepítéshez ez a helyes választás.

---

## 2. lépés: OAuth kliens létrehozása

1. Menjen az **APIs & Services → Credentials** oldalra
2. Kattintson a **Create Credentials → OAuth client ID** gombra
3. Állítsa az **Application type** értékét **Web application**-re
4. Adjon neki egy nevet, pl. `digna`
5. Az **Authorized redirect URIs** alatt kattintson az **Add URI**-ra, és adja meg:

```
https://digna.yourdomain.com/oidc/callback
```

6. Kattintson a **Create** gombra

!!! note "Az Authorized JavaScript Origins nem szükséges"

    A digna a backendről cseréli le az authorization code-ot, nem a böngészőből, ezért az **Authorized JavaScript origins** mező üresen hagyható. Csak az átirányítási URI számít.

---

## 3. lépés: A hitelesítő adatok begyűjtése

A létrehozás után megjelenő párbeszédablak tartalmazza:

- **Client ID** — `.apps.googleusercontent.com`-nel végződik → ez lesz a `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → ez lesz a `DIGNA_OIDC_CLIENT_SECRET`

Mindkettő később is lekérdezhető a hitelesítő adat részletei oldaláról, ellentétben sok más szolgáltatóval.

---

## 4. lépés: A discovery URL

A Google minden ügyfélhez ugyanazt a discovery URL-t használja — nincs mit kicserélni:

```
https://accounts.google.com/.well-known/openid-configuration
```

---

## 5. lépés: digna konfigurálása

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### `config.toml`

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

A `key` mindkét fájlban meg kell, hogy egyezzen — itt `google`.

---

## 6. lépés: Tesztelés

Indítsa újra a backend-et és a webszervert, majd nyissa meg a dashboardot. A teljes ellenőrzőlistát lásd a [Bejelentkezés tesztelése](overview.md#testing-login) szakaszban.

---

## Hibakeresés Google Workspace esetén

### Error 400: redirect_uri_mismatch

A `DIGNA_OIDC_REDIRECT_URI`-ben szereplő URI nincs az **Authorized redirect URIs** listában, vagy eltér egy lezáró perjellel vagy a séma miatt. A Google hibája megmutatja a fogadott URI-t — hasonlítsa össze karakterenként a regisztráltal.

### This App Is Blocked / Has Not Completed Verification

A hozzájárulási képernyő **External** típusú és még *Testing* státuszban van. Tegye közzé, vagy válassza az **Internal** típust.

### Access Blocked: Authorization Error

A bejelentkezést kezdeményező fiók kívül esik a Workspace domainen, miközben a hozzájárulási képernyő **Internal**. Ez a szándékolt viselkedés — az Internal alkalmazások csak a szervezet fiókjait fogadják.

### A változtatások érvénybe lépése több percet is igénybe vehet

A Google aszinkron módon propagálja a hitelesítő adatok és a hozzájárulási képernyő módosításait. Egy újonnan hozzáadott átirányítási URI hatása pár percet is igénybe vehet; ha egy változás nem lép életbe azonnal, várjon és próbálja újra, mielőtt tovább vizsgálódna.

---

## Kapcsolódó anyagok

- [Single Sign-On áttekintés](overview.md) — konfigurációs referencia, tesztelés és általános hibakeresés
- [Google: OpenID Connect](https://developers.google.com/identity/protocols/oauth2/openid-connect)