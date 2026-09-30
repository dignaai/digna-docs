# Skonfiguruj SSO z Microsoft Entra ID

Microsoft Entra ID (dawniej Azure Active Directory) jest w pełni zgodnym z OIDC dostawcą, więc digna integruje się z nim przez standardowy endpoint discovery.

Ten przewodnik obejmuje **stronę Entra ID**: rejestrację aplikacji i zebranie czterech wartości, których potrzebuje digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Przegląd Single Sign-On](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Rola w Entra ID** | Application Administrator, Cloud Application Administrator lub Global Administrator |
| **Redirect URI digna** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |
| **Tenant** | Katalog, do którego logują się Twoi użytkownicy |

---

## Krok 1: Zarejestruj aplikację

1. Zaloguj się do [Microsoft Entra admin center](https://entra.microsoft.com)
2. Przejdź do **Identity → Applications → App registrations**
3. Kliknij **New registration**
4. Skonfiguruj:
   - **Name**: `digna` (wyświetlana użytkownikom na ekranie zgody)
   - **Supported account types**: *Accounts in this organizational directory only* dla wdrożenia z jednym tenantem
5. W sekcji **Redirect URI** wybierz platformę **Web** i wpisz callback URL digna:

```
https://digna.yourdomain.com/oidc/callback
```

6. Kliknij **Register**

!!! warning "Ważne"

    Platformą musi być **Web**, a nie *Single-page application*. digna wymienia kod autoryzacji z backendu przy użyciu sekretu klienta, na co typ platformy SPA nie pozwala.

---

## Krok 2: Zbierz identyfikatory klienta i tenanta

Na stronie **Overview** aplikacji skopiuj:

- **Application (client) ID** → staje się `DIGNA_OIDC_CLIENT_ID`
- **Directory (tenant) ID** → trafia do discovery URL

---

## Krok 3: Utwórz sekret klienta

1. Przejdź do **Certificates & secrets → Client secrets**
2. Kliknij **New client secret**
3. Wpisz opis i wybierz okres ważności
4. Kliknij **Add**
5. Natychmiast skopiuj kolumnę **Value**

!!! warning "Skopiuj Value, nie Secret ID"

    **Value** jest wyświetlana tylko raz, na tej stronie, i nie można jej później odzyskać. **Secret ID** obok wygląda podobnie, ale nie jest sekretem — jego użycie powoduje błąd `invalid_client` przy logowaniu. Jeśli opuścisz stronę przed skopiowaniem, usuń sekret i utwórz nowy.

!!! tip "Wskazówka"

    Entra ID ogranicza okres ważności sekretu do 24 miesięcy, więc każda integracja SSO ma datę wygaśnięcia. Zanotuj ją w miejscu, w którym ją zobaczysz — wygasły sekret wyłącza SSO dla wszystkich użytkowników jednocześnie, bez żadnego ostrzeżenia na stronie logowania.

---

## Krok 4: Potwierdź uprawnienia API

1. Przejdź do **API permissions**
2. Potwierdź, że **Microsoft Graph → User.Read** (delegated) jest obecne — jest dodawane domyślnie

Zakresy `openid`, `profile` i `email`, o które prosi digna, należą do standardowego zestawu OIDC i nie wymagają osobnego nadania. Jeśli Twój tenant wymaga zgody administratora dla wszystkich aplikacji, kliknij **Grant admin consent for &lt;tenant&gt;**.

---

## Krok 5: Zbuduj discovery URL

Podstaw **Directory (tenant) ID** z Kroku 2:

```
https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration
```

!!! note "Użyj endpointu v2.0"

    Segment `/v2.0/` ma znaczenie. Endpoint v1.0 pod adresem `https://login.microsoftonline.com/<tenant_id>/.well-known/openid-configuration` wystawia tokeny w starszym formacie i nie zwraca standardowych claimów OIDC, których oczekuje digna.

Otwórz URL w przeglądarce przed kontynuacją. Dokument JSON potwierdzi, że identyfikator tenanta jest poprawny.

---

## Krok 6: Skonfiguruj digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"
```

### `config.toml`

```toml
[oidc_clients.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<the Value copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"
```

Klucz `key` w obu plikach musi się zgadzać — tutaj `microsoft`.

---

## Krok 7: Testowanie

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z Entra ID

### AADSTS50011: niezgodność redirect URI

URI w `DIGNA_OIDC_REDIRECT_URI` różni się od zarejestrowanego w Kroku 1. Entra ID porównuje cały ciąg znaków, więc końcowy ukośnik, `http` zamiast `https` albo inny port — wszystko to liczy się jako niezgodność. Sprawdź **Authentication → Web → Redirect URIs**.

### AADSTS7000215: nieprawidłowy sekret klienta

Skopiowano **Secret ID** zamiast **Value** albo sekret wygasł. Utwórz nowy sekret i skopiuj kolumnę Value.

### AADSTS650057: nieprawidłowy zasób

Rejestracja aplikacji została usunięta lub należy do innego tenanta niż ten w discovery URL. Potwierdź Directory (tenant) ID na stronie Overview.

### Użytkownicy się logują, ale nic się nie dzieje

Jeśli tenant wymaga zgody administratora, a nie została ona udzielona, przekierowanie wraca bez użytecznego tokenu. Udziel zgody administratora w **API permissions**.

---

## Zobacz także

- [Przegląd Single Sign-On](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [Microsoft: OAuth 2.0 authorization code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow)