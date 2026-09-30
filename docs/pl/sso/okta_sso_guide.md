---
title: Okta SSO – integracja Single Sign-On | Dokumentacja digna
description: Skonfiguruj Single Sign-On dla digna z Okta przez OpenID Connect — integracja aplikacji, sign-in redirect URI, poświadczenia klienta, wybór serwera autoryzacji oraz odpowiadająca konfiguracja digna.
image: /assets/logo_square.png
keywords: digna sso, okta sso, okta oidc, integracja aplikacji, serwer autoryzacji, openid connect, uwierzytelnianie przedsiębiorstw
---

# Skonfiguruj SSO z Okta

Okta jest zgodna z OIDC, z jednym haczykiem, na który natrafia większość pierwszych integracji: organizacja Okta (org) udostępnia więcej niż jeden serwer autoryzacji, a każdy z nich ma własny discovery URL.

Ten przewodnik obejmuje **stronę Okta**: tworzenie integracji aplikacji i zebranie wartości, których potrzebuje digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Przegląd Single Sign-On](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Rola w Okta** | Super Administrator lub rola administratora uprawniona do tworzenia integracji aplikacji |
| **Domena Okta** | np. `yourcompany.okta.com` lub domena niestandardowa, jeśli została skonfigurowana |
| **Redirect URI digna** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Utwórz integrację aplikacji

1. Zaloguj się do Okta Admin Console
2. Przejdź do **Applications → Applications**
3. Kliknij **Create App Integration**
4. Wybierz:
   - **Sign-in method**: *OIDC - OpenID Connect*
   - **Application type**: *Web Application*
5. Kliknij **Next**

!!! warning "Typu aplikacji nie można zmienić"

    Wybranie *Single-Page Application* zamiast *Web Application* tworzy klienta publicznego bez sekretu, a wymiana kodu w backendzie digna zakończy się błędem `invalid_client`. Typ jest ustalany przy tworzeniu — zły wybór oznacza usunięcie aplikacji i rozpoczęcie od nowa.

---

## Krok 2: Skonfiguruj integrację

1. **App integration name**: `digna`
2. **Grant type**: pozostaw zaznaczony *Authorization Code*
3. **Sign-in redirect URIs**: wpisz callback URL digna:

```
https://digna.yourdomain.com/oidc/callback
```

4. **Sign-out redirect URIs**: opcjonalnie
5. W sekcji **Assignments** wybierz, kto może korzystać z integracji — konkretna grupa jest bezpieczniejsza niż *Allow everyone in your organization to access*
6. Kliknij **Save**

!!! note "Przypisanie jest wymagane"

    Okta uwierzytelnia użytkownika, a następnie sprawdza, czy jest on przypisany do aplikacji. Nieprzypisany użytkownik dociera do strony logowania Okta, loguje się pomyślnie i zostaje odrzucony przy przekierowaniu z powrotem. Jeśli logowanie działa u Ciebie, ale nie u współpracowników, w pierwszej kolejności sprawdź przypisanie.

---

## Krok 3: Zbierz poświadczenia

Na karcie **General** aplikacji, w sekcji **Client Credentials**:

- **Client ID** → staje się `DIGNA_OIDC_CLIENT_ID`
- **Client secret** → staje się `DIGNA_OIDC_CLIENT_SECRET` (kliknij ikonę oka, aby odsłonić)

---

## Krok 4: Wybierz serwer autoryzacji

Ten krok określa Twój discovery URL. Przejdź do **Security → API**, aby zobaczyć serwery autoryzacji w Twojej organizacji.

**Org authorization server** — wystawia tokeny dla samej organizacji Okta:

```
https://<your_okta_domain>/.well-known/openid-configuration
```

**Custom authorization server** — w tym serwer o nazwie `default`, tworzony przez Okta:

```
https://<your_okta_domain>/oauth2/<auth_server_id>/.well-known/openid-configuration
```

Dla wbudowanego serwera `<auth_server_id>` to dosłownie `default`:

```
https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration
```

!!! tip "Który wybrać?"

    Używaj serwera autoryzacji **org**, chyba że Twoja organizacja już standardowo korzysta z serwera niestandardowego (custom) na potrzeby polityk dostępu do API. Konta Okta Developer domyślnie używają `default`; wiele organizacji korporacyjnych go wyłącza. Otwórz oba URL w przeglądarce — ten, który zwraca JSON zamiast błędu, jest dla Ciebie dostępny.

---

## Krok 5: Skonfiguruj digna

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
[oidc_clients.okta]
DIGNA_OIDC_CLIENT_ID = "0oa1b2c3d4EXAMPLE5"
DIGNA_OIDC_CLIENT_SECRET = "<the client secret copied in Step 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://yourcompany.okta.com/oauth2/default/.well-known/openid-configuration"
```

Klucz `key` w obu plikach musi się zgadzać — tutaj `okta`.

---

## Krok 6: Testowanie

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testowanie logowania](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z Okta

### The redirect URI Is Not Registered

Okta podaje w komunikacie błędu problematyczne URI. Porównaj je z **General → Sign-in redirect URIs**; Okta dopasowuje cały ciąg znaków, łącznie z ewentualnym końcowym ukośnikiem.

### User Is Not Assigned to the Client Application

Konta nie ma na liście przypisań aplikacji. Dodaj użytkownika lub jego grupę w sekcji **Assignments**.

### 400 Bad Request: Invalid Authorization Server

`<auth_server_id>` w discovery URL nie istnieje — najczęściej chodzi o `default` w organizacji, w której został on usunięty. Sprawdź w **Security → API**, które serwery są faktycznie dostępne.

### invalid_client na etapie tokenu

Integracja została utworzona jako Single-Page Application i nie ma sekretu klienta. Utwórz ją ponownie jako Web Application.

---

## Zobacz także

- [Przegląd Single Sign-On](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [Okta: OpenID Connect & OAuth 2.0](https://developer.okta.com/docs/guides/implement-oauth-for-okta/main/)
