# Skonfiguruj SSO z Auth0

Auth0 jest zgodny z OIDC i udostępnia osobny endpoint discovery dla każdego tenanta. Najważniejsze jest poprawne ustalenie domeny tenanta, która występuje w discovery URL i zmienia się po włączeniu domeny niestandardowej (custom domain).

Ten przewodnik obejmuje **stronę Auth0**: tworzenie aplikacji i zebranie wartości, których potrzebuje digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Przegląd Single Sign-On](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Rola w Auth0** | Admin w tenancie |
| **Domena tenanta** | np. `yourcompany.eu.auth0.com` — segment regionu ma znaczenie |
| **Redirect URI digna** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Utwórz aplikację

1. Zaloguj się do [Auth0 Dashboard](https://manage.auth0.com)
2. Przejdź do **Applications → Applications**
3. Kliknij **Create Application**
4. Nazwij ją `digna` i wybierz **Regular Web Applications**
5. Kliknij **Create**

!!! warning "Wybierz Regular Web Applications"

    *Single Page Application* i *Native* tworzą klientów publicznych bez sekretu. digna wykonuje wymianę kodu z backendu i potrzebuje klienta poufnego (confidential), więc właściwym typem jest **Regular Web Applications**. W przeciwieństwie do niektórych dostawców Auth0 pozwala zmienić typ później w **Settings → Application Type**.

---

## Krok 2: Dodaj callback URL

Na karcie **Settings** aplikacji:

1. Znajdź **Allowed Callback URLs**
2. Wpisz callback URL digna:

```
https://digna.yourdomain.com/oidc/callback
```

3. Opcjonalnie ustaw **Allowed Logout URLs** na URL dashboardu
4. Przewiń na dół i kliknij **Save Changes**

!!! note "Oddzielone przecinkami, nie znakami nowej linii"

    Auth0 akceptuje w tym polu kilka callback URL oddzielonych przecinkami. Lista oddzielona wyłącznie znakami nowej linii jest odczytywana jako jeden błędny URL i po cichu nie pasuje do niczego.

---

## Krok 3: Zbierz poświadczenia

Nadal na karcie **Settings**, w panelu **Basic Information**:

- **Domain** → trafia do discovery URL
- **Client ID** → staje się `DIGNA_OIDC_CLIENT_ID`
- **Client Secret** → staje się `DIGNA_OIDC_CLIENT_SECRET` (kliknij, aby odsłonić)

---

## Krok 4: Potwierdź typ grantu

1. Przejdź do **Settings → Advanced Settings → Grant Types**
2. Potwierdź, że **Authorization Code** jest zaznaczony

Jest on domyślnie włączony dla Regular Web Applications. Jeśli został odznaczony, logowanie do digna kończy się błędem `unauthorized_client`.

---

## Krok 5: Zbuduj discovery URL

Podstaw **Domain** z Kroku 3:

```
https://<your_tenant_domain>/.well-known/openid-configuration
```

Na przykład:

```
https://yourcompany.eu.auth0.com/.well-known/openid-configuration
```

!!! warning "Domeny niestandardowe zmieniają issuer"

    Jeśli Twój tenant używa domeny niestandardowej, takiej jak `login.yourcompany.com`, użyj tej domeny w discovery URL. Mieszanie obu — domeny kanonicznej w discovery URL i niestandardowej w przeglądarce — powoduje niezgodność issuer, a token zostaje odrzucony po skądinąd udanym logowaniu.

---

## Krok 6: Skonfiguruj digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "auth0"
label = "Login with Auth0"
```

### `config.toml`

```toml
[oidc_clients.auth0]
DIGNA_OIDC_CLIENT_ID = "aBcDeFgHiJkLmNoPqRsTuVwXyZ123456"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.eu.auth0.com/.well-known/openid-configuration"
```

Klucz `key` w obu plikach musi się zgadzać — tutaj `auth0`.

---

## Krok 7: Testowanie

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z Auth0

### Niezgodność callback URL

Strona błędu Auth0 podaje URL, który otrzymała. Dodaj go do **Allowed Callback URLs** i sprawdź, czy wpisy są oddzielone przecinkami.

### unauthorized_client

**Authorization Code** nie jest włączony w **Advanced Settings → Grant Types** albo typ aplikacji nie jest Regular Web Applications.

### Odmowa dostępu po udanym logowaniu

Rule, Action lub wyzwalacz Post-Login w tenancie odrzuca użytkownika. Sprawdź **Actions → Flows → Login** oraz logi tenanta w **Monitoring → Logs**, które pokazują dokładną przyczynę.

### Niezgodność issuer

Discovery URL i domena, na którą została skierowana przeglądarka, różnią się — zwykle chodzi o kanoniczną domenę tenanta w porównaniu z domeną niestandardową. Używaj konsekwentnie jednej z nich.

---

## Zobacz także

- [Przegląd Single Sign-On](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [Auth0: OpenID Connect Discovery](https://auth0.com/docs/get-started/applications/configure-applications-with-oidc-discovery)