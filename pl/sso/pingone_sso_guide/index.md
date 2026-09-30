# Skonfiguruj SSO z PingOne

PingOne jest zgodny z OIDC. Dwie z jego wartości wymagają uwagi: **environment ID**, który występuje w każdym URL endpointu, oraz **domena regionalna**, która różni się dla tenantów w Ameryce Północnej, Europie, Kanadzie, regionie Azji i Pacyfiku oraz Australii.

Ten przewodnik obejmuje **stronę PingOne**: tworzenie aplikacji i zebranie wartości, których potrzebuje digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Przegląd Single Sign-On](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Rola w PingOne** | Environment Admin lub Identity Data Admin w docelowym środowisku |
| **Środowisko** | Środowisko PingOne, do którego należą użytkownicy digna |
| **Redirect URI digna** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Utwórz aplikację

1. Zaloguj się do konsoli administracyjnej PingOne i wybierz swoje środowisko
2. Przejdź do **Applications → Applications**
3. Kliknij przycisk **+**
4. Wpisz `digna` jako **Application Name**
5. Wybierz **OIDC Web App**
6. Kliknij **Save**

!!! warning "Wybierz OIDC Web App, a nie Single-Page App"

    *Single-Page App* i *Native App* tworzą klientów publicznych, którzy nie mogą przechowywać sekretu. digna wymienia kod autoryzacji z backendu i potrzebuje poufnego (confidential) typu **OIDC Web App**.

---

## Krok 2: Skonfiguruj redirect URI

1. Otwórz kartę **Configuration** aplikacji
2. Kliknij ikonę ołówka, aby edytować
3. Potwierdź, że **Response Type** to *Code*, a **Grant Type** to *Authorization Code*
4. W sekcji **Redirect URIs** wpisz callback URL digna:

```
https://digna.yourdomain.com/oidc/callback
```

5. Ustaw **Token Endpoint Authentication Method** na *Client Secret Post* lub *Client Secret Basic*
6. Kliknij **Save**

---

## Krok 3: Włącz aplikację

W wierszu aplikacji lub w jej panelu szczegółów przełącz przełącznik na **enabled**.

!!! warning "Nowe aplikacje są początkowo wyłączone"

    PingOne tworzy aplikacje w stanie wyłączonym. Wyłączona aplikacja powoduje na etapie autoryzacji błąd, który nie wspomina o przełączniku, więc warto to potwierdzić przed debugowaniem czegokolwiek innego.

---

## Krok 4: Nadaj zakresy (scopes)

1. Otwórz kartę **Resources**
2. Potwierdź, że `openid` jest nadany, i dodaj `profile` oraz `email` z zasobu **OpenID Connect**
3. Kliknij **Save**

---

## Krok 5: Przypisz użytkowników

1. Otwórz kartę **Access**
2. Dodaj populację (population) lub grupy, których członkowie mogą korzystać z digna
3. Kliknij **Save**

---

## Krok 6: Zbierz poświadczenia i environment ID

Na karcie **Configuration** rozwiń **General**:

- **Client ID** → staje się `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → staje się `DIGNA_OIDC_CLIENT_SECRET` (kliknij ikonę oka)
- **Environment ID** → trafia do discovery URL

Ta sama karta zawiera gotowy **OIDC Discovery Endpoint**, który możesz skopiować bezpośrednio zamiast składać go ręcznie.

---

## Krok 7: Zbuduj discovery URL

Podstaw environment ID i domenę dla swojego regionu:

```
https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration
```

| Region | Domena |
|---|---|
| Ameryka Północna | `auth.pingone.com` |
| Europa | `auth.pingone.eu` |
| Kanada | `auth.pingone.ca` |
| Azja i Pacyfik | `auth.pingone.asia` |
| Australia | `auth.pingone.com.au` |

Dla środowiska europejskiego:

```
https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration
```

!!! tip "Skopiuj zamiast przepisywać"

    Domena regionalna to najczęstszy błąd w integracji z PingOne, a zły region daje błąd 404 zamiast pomocnego komunikatu. Użyj wartości **OIDC Discovery Endpoint** z Kroku 6.

---

## Krok 8: Skonfiguruj digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "pingone"
label = "Login with PingOne"
```

### `config.toml`

```toml
[oidc_clients.pingone]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 6>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://auth.pingone.eu/12345678-1234-1234-1234-123456789012/as/.well-known/openid-configuration"
```

Klucz `key` w obu plikach musi się zgadzać — tutaj `pingone`.

---

## Krok 9: Testowanie

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z PingOne

### 404 dla discovery URL

Domena regionalna lub environment ID są błędne. Porównaj z **OIDC Discovery Endpoint** pokazanym na karcie Configuration aplikacji.

### NOT_FOUND lub aplikacja wyłączona

Przełącznik aplikacji z Kroku 3 jest nadal wyłączony.

### Niezgodność redirect URI

PingOne dopasowuje cały ciąg znaków. Sprawdź w **Configuration → Redirect URIs**, czy nie ma końcowego ukośnika lub różnicy w schemacie.

### Logowanie się udaje, ale claim email nie dociera do digna

Zakresy `email` i `profile` nie zostały nadane na karcie **Resources**.

### Użytkownik nie widzi aplikacji

Żadna populacja ani grupa nie otrzymała dostępu na karcie **Access**.

---

## Zobacz także

- [Przegląd Single Sign-On](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [PingOne: OIDC application configuration](https://docs.pingidentity.com/pingone/)