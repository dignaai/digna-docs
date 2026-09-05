---
title: AD FS SSO – integracja Single Sign-On | dokumentacja digna
description: Skonfiguruj Single Sign-On dla digna z Active Directory Federation Services używając OpenID Connect — grupa aplikacji, aplikacja serwerowa, wspólny sekret, dozwolone zakresy i odpowiadająca konfiguracja digna.
image: /assets/logo_square.png
keywords: digna sso, adfs sso, usługa Active Directory Federation Services, adfs oidc, application group, openid connect, lokalny dostawca tożsamości
---

# Skonfiguruj SSO z AD FS

Active Directory Federation Services to opcja lokalna: Twoje własne serwery wydają tokeny, a discovery URL to Twoja własna nazwa hosta. AD FS obsługuje OpenID Connect od **Windows Server 2016** wzwyż.

Ten przewodnik opisuje stronę **AD FS**: tworzenie application group i zebranie wartości potrzebnych digna. Strona digna — `dashboard_config.toml`, testowanie i rozwiązywanie problemów — jest taka sama dla każdego dostawcy i opisana w [Single Sign-On Overview](overview.md).

---

## Zanim zaczniesz

| Wymaganie | Uwagi |
|---|---|
| **Wersja AD FS** | Windows Server 2016 lub nowszy — wcześniejsze wersje nie obsługują OIDC |
| **Dostęp** | Lokalny administrator na serwerze AD FS |
| **Nazwa usługi federation** | np. `adfs.yourdomain.com` |
| **digna redirect URI** | URL, na który użytkownicy wracają po logowaniu, np. `https://digna.yourdomain.com/oidc/callback` |

---

## Krok 1: Utwórz grupę aplikacji

1. Na serwerze AD FS otwórz **AD FS Management**
2. Kliknij prawym przyciskiem **Application Groups** i wybierz **Add Application Group**
3. Wprowadź `digna` jako nazwę
4. Pod **Standalone applications** — lub **Client-Server applications** w zależności od wersji — wybierz **Server application accessing a web API**
5. Kliknij **Next**

---

## Krok 2: Skonfiguruj aplikację serwerową

1. **Name**: `digna backend`
2. **Client Identifier**: AD FS wygeneruje GUID. Skopiuj go — to będzie `DIGNA_OIDC_CLIENT_ID`
3. **Redirect URI**: wprowadź adres callback digna i kliknij **Add**:

```
https://digna.yourdomain.com/oidc/callback
```

4. Kliknij **Next**

!!! warning "Kliknij Dodaj, nie tylko Dalej"

    Pole redirect URI ma swój własny przycisk **Add**. Wpisanie URI i kliknięcie **Next** bez naciśnięcia **Add** spowoduje jego odrzucenie, a kreator nie wyświetli żadnego ostrzeżenia. Potwierdź, że URI pojawia się na liście pod polem, zanim przejdziesz dalej.

---

## Krok 3: Wygeneruj wspólny sekret

1. Zaznacz **Generate a shared secret**
2. Skopiuj wygenerowany sekret → to stanie się `DIGNA_OIDC_CLIENT_SECRET`
3. Kliknij **Next**

!!! warning "Sekret jest wyświetlany tylko raz"

    AD FS pokazuje wspólny sekret tylko na tej stronie kreatora i nie może go ponownie wyświetlić. Jeśli go zgubisz, zresetuj go później w właściwościach application group.

---

## Krok 4: Skonfiguruj Web API

1. **Identifier**: wprowadź ten sam client identifier z Kroku 2 i kliknij **Add**
2. Kliknij **Next**
3. Wybierz **Access Control Policy** — *Zezwól wszystkim* jest najprostszym punktem wyjścia; w produkcji ogranicz to do konkretnej grupy
4. Kliknij **Next**

---

## Krok 5: Przyznaj dozwolone zakresy

Na kroku **Configure Application Permissions** zaznacz:

- `openid`
- `profile`
- `email`

Następnie kliknij **Next** i dokończ kreatora.

!!! warning "openid nie jest domyślnie zaznaczone"

    AD FS w niektórych wersjach wstępnie wybiera tylko `user_impersonation`. Bez `openid` endpoint tokenów zwróci token dostępu OAuth zamiast ID tokenu, i digna nie będzie mogła zidentyfikować użytkownika.

---

## Krok 6: Potwierdź punkt odkrywania

Podstaw swoją nazwę usługi federation:

```
https://<adfs_host>/adfs/.well-known/openid-configuration
```

Na przykład:

```
https://adfs.yourdomain.com/adfs/.well-known/openid-configuration
```

Otwórz go w przeglądarce. Dokument JSON potwierdzi, że OIDC jest włączony i nazwa hosta jest poprawna.

!!! note "Backend musi ufać certyfikatowi"

    Wewnętrzne urzędy certyfikacji są powszechne w przypadku AD FS. Maszyna uruchamiająca backend digna wykonuje własne wychodzące wywołanie HTTPS do tego URL, więc urząd certyfikacji musi znajdować się w magazynie zaufania tej maszyny — nie tylko w przeglądarkach osób logujących się.

---

## Krok 7: Skonfiguruj digna

### `dashboard/dashboard_config.toml`

```toml
[login]
usePassword = true

[[login.oidc]]
key = "adfs"
label = "Zaloguj się przez Active Directory"
```

### `config.toml`

```toml
[oidc.adfs]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "<wspólny sekret skopiowany w Kroku 3>"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://adfs.yourdomain.com/adfs/.well-known/openid-configuration"
```

Wartość `key` w obu plikach musi się zgadzać — tutaj `adfs`.

---

## Krok 8: Test

Zrestartuj backend i serwer WWW, a następnie otwórz dashboard. Zobacz [Testing Login](overview.md#testing-login) po pełną listę kontrolną.

---

## Rozwiązywanie problemów z AD FS

### MSIS9611: Klient nie ma uprawnień do dostępu do zasobu

Identifier web API z Kroku 4 nie zgadza się z client identifier, lub zakresy z Kroku 5 nie zostały przyznane. Oba można edytować w właściwościach application group.

### MSIS9602: Nieprawidłowe redirect_uri

URI zostało wpisane, ale nie dodane przyciskiem **Add**, lub różni się od `DIGNA_OIDC_REDIRECT_URI`. Sprawdź **Application Groups → digna → digna backend → Properties**.

### Nie zwrócono ID tokenu

Brakuje zakresu `openid` w uprawnieniach aplikacji.

### Backend nie może uzyskać dostępu do adresu discovery

Albo DNS na hoście backendu nie rozwiązuje nazwy federation service, albo certyfikat AD FS nie jest tam zaufany. Przetestuj poleceniem `curl https://adfs.yourdomain.com/adfs/.well-known/openid-configuration` bezpośrednio z serwera digna.

### Zdarzenia do sprawdzenia

Serwer AD FS loguje błędy w **Applications and Services Logs → AD FS → Admin** w Podglądzie zdarzeń, zwykle z bardziej szczegółowym powodem niż ten pokazany w przeglądarce.

---

## Zobacz także

- [Single Sign-On Overview](overview.md) — odniesienie konfiguracyjne, testowanie i ogólne rozwiązywanie problemów
- [Microsoft: scenariusze AD FS OpenID Connect](https://learn.microsoft.com/en-us/windows-server/identity/ad-fs/development/ad-fs-openid-connect-oauth-flows-scenarios)