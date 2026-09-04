---
title: Przewodnik integracji Single Sign-On (SSO) | Dokumentacja digna
description: Krok po kroku instrukcja konfigurowania Single Sign-On (SSO) dla digna przy użyciu OpenID Connect (OIDC). Zawiera konfigurację dashboardu i backendu, testowanie, rozwiązywanie problemów oraz obsługiwane dostawcy tożsamości, w tym Microsoft Entra ID, Google Workspace i Okta.
image: /assets/logo_square.png
keywords:
  - digna sso
  - single sign-on
  - integracja oidc
  - openid connect
  - microsoft entra id
  - azure ad sso
  - google workspace sso
  - integracja okta
  - uwierzytelnianie przedsiębiorstw
lang: pl
robots: index, follow
og_title: digna Przewodnik integracji Single Sign-On (SSO)
og_description: Skonfiguruj Single Sign-On dla digna przy użyciu OpenID Connect. Instrukcja krok po kroku dla Microsoft Entra ID, Google Workspace, Okta oraz innych dostawców zgodnych z OIDC.
og_image: /assets/logo_square.png
og_type: article
twitter_card: summary_large_image
---

# Przewodnik integracji Single Sign-On

---

## Spis treści

1. [Wprowadzenie i przegląd](#introduction-and-overview)
2. [Kroki konfiguracji](#configuration-steps)
3. [Konfiguracja dashboardu](#dashboard-configuration)
4. [Konfiguracja backendu](#backend-configuration)
5. [Testowanie logowania](#testing-login)
6. [Rozwiązywanie problemów](#troubleshooting)
7. [Obsługiwani dostawcy](#supported-providers)

---

## Introduction and Overview {: #introduction-and-overview }

Ten przewodnik zawiera instrukcje krok po kroku dotyczące integracji Single Sign-On (SSO) z platformą digna przy użyciu protokołu **OpenID Connect (OIDC)**.

### Czym jest SSO?

Single Sign-On pozwala użytkownikom zalogować się do digna bezpiecznie, używając poświadczeń firmowych za pośrednictwem zewnętrznych dostawców tożsamości. Użytkownicy mogą uwierzytelniać się za pomocą danych swojej organizacji zamiast zarządzać oddzielnymi hasłami do digna.

### Jak to działa

SSO w digna jest zaimplementowany przy użyciu protokołu OIDC. Można skonfigurować wiele dostawców tożsamości równolegle, modyfikując dwa kluczowe pliki konfiguracyjne:

- **`dashboard_config.toml`** — Steruje interfejsem logowania frontendu
- **`config.toml`** — Konfiguruje połączenia OIDC w backendzie

### Obsługiwani dostawcy {: #supported-providers-overview }

Przykłady w tym przewodniku używają **Microsoft** i **Google**, ale **każdy dostawca zgodny z OIDC** może zostać zintegrowany, stosując tę samą strukturę.

Typowi dostawcy OIDC obejmują:
- Microsoft Entra ID (Azure AD)
- Google Workspace
- Okta
- Auth0
- Keycloak
- Inni dostawcy zgodni z OpenID Connect

---

## Configuration Steps {: #configuration-steps }

Konfiguracja SSO wymaga aktualizacji dwóch plików. W tej sekcji wyjaśniono, jak skonfigurować każdy z nich.

### Przegląd plików konfiguracyjnych

| File | Location | Purpose |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfejs logowania frontendu |
| **config.toml** | `/config.toml` | Połączenia OIDC w backendzie |

Oba pliki muszą być skonfigurowane, aby SSO działało poprawnie.

---

## Dashboard Configuration {: #dashboard-configuration }

### Lokalizacja pliku

```
dashboard/dashboard_config.toml
```

### Krok 1: Dodaj dostawców OIDC

Dodaj wpisy w tablicy `[[login.oidc]]` dla każdego dostawcy tożsamości, którego chcesz obsługiwać.

**Przykład z Microsoft i Google:**

```toml
[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"
```

### Krok 2: Skonfiguruj opcje logowania

Określ, czy logowanie za pomocą hasła ma być dozwolone:

```toml
[login]
usePassword = true
```

### Parametry konfiguracji

#### Sekcja `[[login.oidc]]`

| Parameter | Type | Required | Description |
|---|---|---|---|
| `key` | string | Yes | Unikalny identyfikator połączenia OIDC (musi zgadzać się z kluczem w config.toml) |
| `label` | string | Yes | Tekst wyświetlany na przycisku logowania (np. "Login with Microsoft") |

#### Sekcja `[login]`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `usePassword` | boolean | false | Pozwala na logowanie za pomocą hasła oprócz SSO |

### Zrozumienie usePassword

**Jeśli `usePassword = true`:**
- Ekran logowania pokazuje przyciski SSO (np. "Login with Microsoft")
- Ekran logowania pokazuje także pola nazwy użytkownika i hasła
- Użytkownicy mogą uwierzytelniać się za pomocą obu metod
- Pozwala na rozwiązania hybrydowe, gdzie niektórzy użytkownicy korzystają z SSO, a inni z haseł

**Jeśli `usePassword = false` (lub pominięte):**
- Ekran logowania pokazuje tylko przyciski SSO
- Brak pól nazwy użytkownika/hasła
- Dostępne jest wyłącznie uwierzytelnianie OIDC

> **Wskazówka**
>
> Logowanie za pomocą hasła jest dostępne tylko dla użytkowników utworzonych z hasłem przy użyciu polecenia `digna user add` lub poprzez dashboard.

### Pełny przykład

```toml
[login]
usePassword = true

[[login.oidc]]
key = "microsoft"
label = "Login with Microsoft"

[[login.oidc]]
key = "google"
label = "Login with Google"

[[login.oidc]]
key = "okta"
label = "Login with Okta"
```

---

## Backend Configuration {: #backend-configuration }

### Lokalizacja pliku

```
/config.toml
```

(Katalog główny instalacji digna)

### Krok 1: Dodaj sekcje dla dostawców OIDC

Każdy dostawca musi mieć dedykowaną sekcję `[oidc.<key>]`. Klucz musi odpowiadać `key` zdefiniowanemu w `dashboard_config.toml`.

### Konfiguracja Microsoft

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration"
```

### Konfiguracja Google

```toml
[oidc.google]
DIGNA_OIDC_CLIENT_ID = "<client_id>"
DIGNA_OIDC_CLIENT_SECRET = "<client_secret>"
DIGNA_OIDC_REDIRECT_URI = "http://localhost:5173/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

### Parametry konfiguracji

| Parameter | Type | Required | Description | Example |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Yes | Client ID od dostawcy tożsamości | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Yes | Client secret od dostawcy tożsamości | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Yes | URL przekierowania po uwierzytelnieniu | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Yes | Punkt końcowy konfiguracji OIDC | `https://login.microsoftonline.com/...` |

> **Ważne**
>
> Zastąp wartości zastępcze (`<client_id>`, `<client_secret>`, `<tenant_id>`) rzeczywistymi danymi z panelu deweloperskiego Twojego dostawcy tożsamości.

### Redirect URI

Redirect URI musi być taki sam jak w konfiguracji dostawcy tożsamości:

```
http://localhost:5173/oidc/callback
```

Jeśli digna jest hostowane pod inną domeną, zaktualizuj odpowiednio:
- Lokalnie: `http://localhost:5173/oidc/callback`
- Produkcja: `https://digna.yourdomain.com/oidc/callback`

### Pełny przykład

```toml
[oidc.microsoft]
DIGNA_OIDC_CLIENT_ID = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
DIGNA_OIDC_CLIENT_SECRET = "abc123xyz789def456ghi"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://login.microsoftonline.com/12345678-1234-1234-1234-123456789012/v2.0/.well-known/openid-configuration"

[oidc.google]
DIGNA_OIDC_CLIENT_ID = "123456789-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com"
DIGNA_OIDC_CLIENT_SECRET = "google_secret_xyz789"
DIGNA_OIDC_REDIRECT_URI = "https://digna.yourdomain.com/oidc/callback"
DIGNA_OIDC_CONFIGURATION_URL = "https://accounts.google.com/.well-known/openid-configuration"
```

---

## Testing Login {: #testing-login }

Po zakończeniu konfiguracji zweryfikuj, czy SSO działa poprawnie.

### Lista kontrolna przed testowaniem

Zanim rozpoczniesz testy, upewnij się, że:

- [ ] `dashboard_config.toml` został zaktualizowany z dostawcami OIDC
- [ ] `config.toml` został zaktualizowany z poświadczeniami OIDC
- [ ] Oba pliki zostały zapisane
- [ ] Poświadczenia są poprawne (Client ID, Client Secret)
- [ ] Redirect URI zgadza się z adresem wdrożenia
- [ ] Aplikacja w ustawieniach dostawcy tożsamości ma skonfigurowany redirect URI

### Kroki testowe

#### Krok 1: Zrestartuj usługi

Uruchom ponownie backend digna i serwer WWW, aby zastosować zmiany.

**Jeśli uruchomione jako usługa Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Jeśli uruchamiasz ręcznie:**
```bash
cd C:\path\to\digna
digna serve --address localhost --port 8082
```

**Jeśli używasz IIS lub Tomcat:**
Zrestartuj usługę serwera WWW.

#### Krok 2: Otwórz dashboard

Otwórz dashboard digna w przeglądarce:

```
http://localhost:5173
```

(lub Twój skonfigurowany URL dashboardu)

#### Krok 3: Sprawdź przyciski logowania

Sprawdź, czy przyciski logowania pojawiają się dla każdego skonfigurowanego dostawcy:

- Powinien być widoczny przycisk "Login with Microsoft"
- Powinien być widoczny przycisk "Login with Google"
- (Jeśli usePassword = true) Powinny być widoczne pola nazwy użytkownika/hasła

Jeśli przyciski się nie pojawiają:
- Sprawdź, czy `dashboard_config.toml` został zapisany
- Sprawdź, czy usługa dashboardu została zrestartowana
- Sprawdź konsolę przeglądarki (F12) pod kątem błędów

#### Krok 4: Przetestuj logowanie SSO

Kliknij jeden z przycisków SSO (np. "Login with Microsoft"):

1. Powinieneś zostać przekierowany na stronę logowania dostawcy tożsamości
2. Zaloguj się używając poświadczeń służbowych
3. Powinieneś zostać przekierowany z powrotem do digna
4. Powinieneś być zalogowany do digna

#### Krok 5: Sprawdź tworzenie użytkownika

Po pomyślnym logowaniu SSO:

- Użytkownik powinien zostać automatycznie utworzony w digna
- Użytkownik powinien być zalogowany
- Profil użytkownika powinien pokazywać dane z dostawcy tożsamości
- Powinieneś zobaczyć dashboard digna

#### Krok 6: Przetestuj logowanie hasłem (jeśli włączone)

Jeśli `usePassword = true`:

1. Wyloguj się z digna
2. Na stronie logowania wpisz nazwę użytkownika i hasło
3. Powinieneś móc zalogować się za pomocą poświadczeń hasła

---

## Troubleshooting {: #troubleshooting }

### Przyciski logowania nie pojawiają się

**Objawy:**
- Przyciski logowania OIDC nie widoczne na stronie logowania
- Widzisz tylko pola hasła (jeśli usePassword = true)

**Przyczyny i rozwiązania:**
1. Sprawdź, czy `dashboard_config.toml` znajduje się w katalogu `dashboard/`
2. Zweryfikuj, czy sekcje `[[login.oidc]]` są obecne i mają poprawną składnię
3. Zrestartuj usługę dashboardu
4. Wyczyść pamięć podręczną przeglądarki (Ctrl+Shift+Delete lub Cmd+Shift+Delete)
5. Sprawdź konsolę przeglądarki (F12 → zakładka Console) pod kątem błędów

---

### Błąd niezgodności Redirect URI

**Objawy:**
- Po kliknięciu przycisku SSO pojawia się błąd dotyczący "redirect_uri mismatch"
- Błąd "The redirect URI is not registered"

**Przyczyny i rozwiązania:**
1. Zweryfikuj `DIGNA_OIDC_REDIRECT_URI` w `config.toml`
2. Upewnij się, że redirect URI jest zarejestrowane w ustawieniach dostawcy tożsamości
3. Upewnij się, że oba URI są identyczne (włącznie z protokołem, domeną, ścieżką)
4. Sprawdź literówki w redirect URI
5. Jeśli używasz HTTPS, upewnij się, że certyfikat jest ważny

---

### Błąd nieprawidłowych poświadczeń klienta

**Objawy:**
- Błąd "Invalid client ID or secret"
- Uwierzytelnianie kończy się błędem poświadczeń

**Przyczyny i rozwiązania:**
1. Sprawdź, czy `DIGNA_OIDC_CLIENT_ID` i `DIGNA_OIDC_CLIENT_SECRET` są poprawne
2. Upewnij się, że nie ma dodatkowych spacji lub niepożądanych znaków
3. Sprawdź, czy poświadczenia nie wygasły ani nie zostały cofnięte
4. Zrestartuj usługę backendu po aktualizacji konfiguracji
5. Sprawdź panel dostawcy tożsamości, aby potwierdzić, że poświadczenia są aktywne

---

### Logowanie zawiesza się lub następuje timeout

**Objawy:**
- Kliknięcie przycisku SSO nic nie robi
- Timeout po kilku sekundach
- Przeglądarka pokazuje "Failed to connect" lub podobny komunikat

**Przyczyny i rozwiązania:**
1. Sprawdź, czy backend digna działa: `digna repo check`
2. Sprawdź łączność sieciową z dostawcą tożsamości
3. Zweryfikuj, czy `DIGNA_OIDC_CONFIGURATION_URL` jest dostępny
4. Sprawdź reguły firewalla umożliwiające wychodzące połączenia HTTPS
5. Upewnij się, że backend i dashboard mogą się wzajemnie osiągnąć

---

### Użytkownicy nie są automatycznie tworzeni

**Objawy:**
- Logowanie SSO się powiodło, ale użytkownik nie został utworzony w digna
- Po logowaniu SSO występuje błąd uprawnień

**Przyczyny i rozwiązania:**
1. Zweryfikuj konfigurację OIDC
2. Sprawdź, czy ustawienia uprawnień użytkownika są poprawne
3. Przejrzyj logi digna pod kątem komunikatów o błędach
4. Zrestartuj usługę backendu
5. Skontaktuj się z support@digna.ai, jeśli problem będzie się powtarzał

---

## Supported Providers {: #supported-providers }

### Testowani i wspierani

Poniżsi dostawcy OIDC zostali przetestowani i są znani jako działające:

| Provider | Configuration URL | Setup Guide |
|---|---|---|
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Microsoft Doc](https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-auth-code-flow) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Google Doc](https://developers.google.com/identity/protocols/oauth2/openid-connect) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Okta Doc](https://developer.okta.com/docs/guides/implement-oauth/openid-connect) |

### Inni dostawcy OIDC

Każdy dostawca obsługujący OpenID Connect może zostać zintegrowany. Wymagane informacje:

- Client ID
- Client secret
- URL konfiguracji OpenID (zwykle `/.well-known/openid-configuration`)
- Obsługiwane zakresy (zwykle `openid profile email`)

Skontaktuj się z support@digna.ai, jeśli potrzebujesz pomocy przy integracji konkretnego dostawcy.

---

## Najlepsze praktyki

DO:
- Używaj HTTPS w środowisku produkcyjnym (nie HTTP)
- Przechowuj client secret bezpiecznie (używaj zmiennych środowiskowych, jeśli to możliwe)
- Okresowo rotuj sekrety
- Testuj najpierw w środowisku nieprodukcyjnym
- Dokumentuj, które dostawcy są skonfigurowani
- Monitoruj logi logowań pod kątem nieprawidłowej aktywności
- Utrzymuj konfigurację dostawcy tożsamości w synchronizacji z konfiguracją digna

DON'T:
- Przechowuj client secret w systemie kontroli wersji
- Używaj HTTP redirect URI w produkcji
- Konfiguruj wielu dostawców z tym samym kluczem
- Pozostawiaj domyślnych/testowych poświadczeń w produkcji
- Ujawniaj plików konfiguracyjnych zawierających sekrety
- Mieszaj poświadczenia developerskie i produkcyjne

---

## Support

Potrzebujesz pomocy z konfiguracją SSO?

- **Email:** support@digna.ai
- **Dokumentacja:** https://docs.digna.ai
- **Strona:** https://www.digna.ai

---

**Last Updated:** August 30, 2026  
**Release:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**