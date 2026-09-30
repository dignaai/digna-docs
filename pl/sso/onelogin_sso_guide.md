# Skonfiguruj SSO z OneLogin

OneLogin jest zgodny z OIDC. Jego cechą wyróżniającą jest to, że typ konektora wybiera się z katalogu podczas tworzenia aplikacji i nie można go później zmienić.

Ten przewodnik obejmuje **stronę OneLogin**: tworzenie aplikacji i zebranie wartości, których potrzebuje digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Przegląd Single Sign-On](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Rola w OneLogin** | Właściciel konta lub administrator uprawniony do dodawania aplikacji |
| **Subdomena** | np. `yourcompany.onelogin.com` |
| **Redirect URI digna** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Utwórz aplikację OIDC

1. Zaloguj się do OneLogin Admin portal
2. Przejdź do **Applications → Applications**
3. Kliknij **Add App**
4. Wyszukaj `OpenId Connect` i wybierz konektor **OpenId Connect (OIDC)**
5. Ustaw **Display Name** na `digna`
6. Kliknij **Save**

!!! warning "Typ konektora jest ustalany przy tworzeniu"

    OneLogin ma osobne pozycje katalogu dla SAML i OIDC, a aplikacji nie można przekonwertować z jednego na drugi. Jeśli przez pomyłkę wybierzesz konektor SAML, usuń aplikację i dodaj ją ponownie — nie ma ustawienia pozwalającego przełączyć protokół.

---

## Krok 2: Skonfiguruj redirect URI

1. Otwórz kartę **Configuration**
2. W polu **Redirect URI's** wpisz callback URL digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcjonalnie ustaw **Post Logout Redirect URIs** na URL dashboardu
4. Kliknij **Save**

!!! note "Jedno URI na linię"

    W przeciwieństwie do dostawców oczekujących listy oddzielonej przecinkami, pole **Redirect URI's** w OneLogin przyjmuje jedno URI na linię.

---

## Krok 3: Ustaw typ aplikacji i metodę uwierzytelniania

1. Otwórz kartę **SSO**
2. Potwierdź, że **Application Type** to *Web*
3. Ustaw **Token Endpoint → Authentication Method** na *POST* (`client_secret_post`) lub *Basic* (`client_secret_basic`)

!!! warning "Nie wybieraj None"

    Ustawienie metody uwierzytelniania na *None* czyni aplikację klientem publicznym bez sekretu, a wymiana kodu w backendzie digna zostanie odrzucona. Działa zarówno POST, jak i Basic.

---

## Krok 4: Zbierz poświadczenia

Nadal na karcie **SSO**:

- **Client ID** → staje się `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → staje się `DIGNA_OIDC_CLIENT_SECRET` (kliknij **Show client secret**)

Strona pokazuje również **Issuer URL**, który potwierdza discovery URL z następnego kroku.

---

## Krok 5: Przypisz użytkowników

1. Otwórz kartę **Access**
2. Dodaj role lub grupy, których członkowie mogą korzystać z digna
3. Kliknij **Save**

!!! note "Nieprzypisani użytkownicy są odrzucani po zalogowaniu"

    Podobnie jak większość dostawców, OneLogin najpierw uwierzytelnia użytkownika, a dopiero potem sprawdza uprawnienia. Nieprzypisany użytkownik loguje się pomyślnie, a następnie zostaje odrzucony, co wygląda jak błąd digna, a nie jak decyzja kontroli dostępu.

---

## Krok 6: Zbuduj discovery URL

Podstaw swoją subdomenę OneLogin:

```
https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration
```

Na przykład:

```
https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration
```

!!! tip "/2 to wersja API"

    Obecna implementacja OIDC w OneLogin znajduje się pod `/oidc/2/`. Starsza dokumentacja pokazuje `/oidc/` bez wersji, co wskazuje na wycofaną pierwszą wersję. W razie wątpliwości sprawdź **Issuer URL** na karcie SSO — discovery URL to issuer z dopisanym `/.well-known/openid-configuration`.

---

## Krok 7: Skonfiguruj digna

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
[oidc_clients.onelogin]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d0-1234-5678-9abc-def012345678"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.onelogin.com/oidc/2/.well-known/openid-configuration"
```

Klucz `key` w obu plikach musi się zgadzać — tutaj `onelogin`.

---

## Krok 8: Testowanie

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z OneLogin

### redirect_uri did not match

Brakuje callback URL w **Configuration → Redirect URI's** albo wpisy zostały oddzielone przecinkami zamiast znakami nowej linii.

### invalid_client na etapie tokenu

**Token Endpoint → Authentication Method** jest ustawione na *None* albo sekret klienta w `config.toml` jest nieaktualny. Odsłoń sekret na karcie **SSO** i porównaj.

### Aplikacja nie jest widoczna dla użytkowników

Żadna rola ani grupa nie otrzymała dostępu na karcie **Access**.

### 404 dla discovery URL

Subdomena jest błędna albo w URL brakuje `/oidc/2/`. Porównaj z **Issuer URL** pokazanym na karcie SSO.

---

## Zobacz także

- [Przegląd Single Sign-On](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [OneLogin: OpenID Connect](https://developers.onelogin.com/openid-connect)