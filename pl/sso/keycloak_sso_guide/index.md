# Konfiguracja SSO z Keycloak

Keycloak to samodzielnie hostowany, w pełni zgodny z OIDC dostawca tożsamości. Ponieważ uruchamiasz go samodzielnie, adres odkrywania (discovery URL) jest zbudowany z Twojej nazwy hosta i realm, a nie z domeny dostawcy.

Ten przewodnik obejmuje **stronę Keycloak**: tworzenie klienta i zebranie wartości potrzebnych digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Przegląd Single Sign-On](overview.md).

---

## Zanim zaczniesz

| Wymóg | Uwagi |
|---|---|
| **Wersja Keycloak** | 17 lub nowsza dla ścieżek URL używanych tutaj — zobacz uwagę w Kroku 4 |
| **Rola w Keycloak** | `realm-admin` w docelowym realm, lub administrator serwera |
| **Realm** | Realm, do którego należą użytkownicy digna, niekoniecznie `master` |
| **URI przekierowania digna** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Wybierz realm

1. Otwórz konsolę administracyjną Keycloak
2. Użyj selektora realm w lewym górnym rogu, aby przełączyć się na realm, w którym są Twoi użytkownicy

!!! warning "Nie używaj realm `master`"

    Realm `master` służy do administrowania samym Keycloak. Klienci aplikacji powinni być umieszczani w dedykowanym realm; umieszczenie digna w `master` da jego użytkownikom dostęp do konsoli administracyjnej Keycloak.

---

## Krok 2: Utwórz klienta

1. Przejdź do **Clients** i kliknij **Create client**
2. Skonfiguruj:
   - **Client type**: *OpenID Connect*
   - **Client ID**: `digna` — to stanie się `DIGNA_OIDC_CLIENT_ID`
3. Kliknij **Next**
4. Na kroku **Capability config** włącz **Client authentication** **On**
5. Pozostaw włączony **Standard flow**; pozostałe flow nie są potrzebne
6. Kliknij **Next**

!!! warning "Uwierzytelnianie klienta musi być włączone"

    Przy wyłączonym **Client authentication** Keycloak tworzy klienta *publicznego*, który nie ma żadnych poświadczeń — karta **Credentials** w Kroku 4 nie będzie istniała. digna potrzebuje klienta poufnego (confidential). Przełącznik można zmienić po utworzeniu, jeśli się pomylisz.

---

## Krok 3: Ustaw URI przekierowania

Na kroku **Login settings** (lub na karcie **Settings** później):

1. **Valid redirect URIs**: wpisz URL callback digna:

```
https://digna.yourdomain.com/oidc/callback
```

2. **Web origins**: pozostaw puste, lub ustaw na `+`, aby odzwierciedlić redirect URIs
3. Kliknij **Save**

!!! tip "Unikaj wildcardów"

    Keycloak akceptuje wzorce takie jak `https://digna.yourdomain.com/*`. Wildcard pozwala każdej ścieżce na tym hoście odbierać kod autoryzacji, więc lepiej użyć dokładnego URL callback.

---

## Krok 4: Pobierz sekret klienta

1. Otwórz kartę **Credentials**
2. Potwierdź, że **Client Authenticator** to *Client Id and Secret*
3. Skopiuj **Client secret** → stanie się `DIGNA_OIDC_CLIENT_SECRET`

Sekret pozostaje dostępny do pobrania tutaj i można go zregenerować za pomocą **Regenerate**.

---

## Krok 5: Zbuduj URL odkrywania (Discovery URL)

Podstaw swój host Keycloak i nazwę realm:

```
https://<keycloak_host>/realms/<realm>/.well-known/openid-configuration
```

Na przykład:

```
https://sso.yourdomain.com/realms/company/.well-known/openid-configuration
```

!!! note "Keycloak 16 i wcześniejsze zawierały /auth"

    Przed Keycloak 17 każdy endpoint znajdował się pod prefiksem `/auth`:

    ```
    https://sso.yourdomain.com/auth/realms/company/.well-known/openid-configuration
    ```

    Dystrybucje, które ustawiają `KC_HTTP_RELATIVE_PATH=/auth`, zachowują stary układ również w obecnych wersjach. Jeśli URL bez `/auth` zwraca 404, spróbuj go z prefiksem.

Otwórz URL w przeglądarce przed kontynuacją. Dokument JSON potwierdzi, że host i realm są poprawne.

---

## Krok 6: Skonfiguruj digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "keycloak"
label = "Zaloguj się przez Keycloak"
```

### `config.toml`

```toml
[oidc.keycloak]
DIGNA_OIDC_CLIENT_ID = "digna"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 4>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://sso.yourdomain.com/realms/company/.well-known/openid-configuration"
```

Klucz (`key`) w obu plikach musi się zgadzać — tutaj `keycloak`. Zauważ, że nie musi on równać się Keycloak **Client ID**, chociaż utrzymanie ich takich samych ułatwia śledzenie.

---

## Krok 7: Testowanie

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z Keycloak

### Invalid parameter: redirect_uri

URL callback nie jest objęty przez **Valid redirect URIs**. Keycloak loguje odebrane URI w logach serwera, co jest najszybszym sposobem, żeby zobaczyć dokładne niedopasowanie.

### Karta Credentials jest niewidoczna

Klient jest publiczny. Włącz **Client authentication** w **Settings → Capability config**.

### 404 dla Discovery URL

Albo nazwa realm jest błędna, albo wdrożenie używa prefiksu `/auth`. Sprawdź listę realm w konsoli administracyjnej i spróbuj obu form URL.

### unauthorized_client or invalid_client

**Standard flow** jest wyłączony w **Capability config**, lub sekret został zregenerowany w Keycloak bez aktualizacji `config.toml`.

### Błędy certyfikatu po stronie backendu

Samodzielnie hostowany Keycloak z prywatnym lub samopodpisanym certyfikatem spowoduje niepowodzenie wywołania HTTPS z digna do discovery URL. Zainstaluj wystawiający CA w magazynie zaufania maszyny uruchamiającej backend digna.

---

## Zobacz także

- [Przegląd Single Sign-On](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [Keycloak: Zabezpieczanie aplikacji](https://www.keycloak.org/docs/latest/securing_apps/)