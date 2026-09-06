# Przegląd Single Sign-On

---

## Spis treści

1. [Wprowadzenie i przegląd](#introduction-and-overview)
2. [Przewodniki dla dostawców](#provider-guides)
3. [Kroki konfiguracji](#configuration-steps)
4. [Konfiguracja dashboardu](#dashboard-configuration)
5. [Konfiguracja backendu](#backend-configuration)
6. [Testowanie logowania](#testing-login)
7. [Rozwiązywanie problemów](#troubleshooting)
8. [Obsługiwani dostawcy](#supported-providers)

---

## Wprowadzenie i przegląd {: #introduction-and-overview }

Ten przewodnik zawiera instrukcje krok po kroku dotyczące integracji Single Sign-On (SSO) z platformą digna przy użyciu protokołu **OpenID Connect (OIDC)**.

### Czym jest SSO?

Single Sign-On pozwala użytkownikom logować się do digna w bezpieczny sposób, używając firmowych poświadczeń zewnętrznych dostawców tożsamości. Użytkownicy mogą uwierzytelniać się przy użyciu swoich danych korporacyjnych zamiast zarządzać oddzielnymi hasłami dla digna.

### Jak to działa

SSO w digna jest implementowane przy użyciu protokołu OIDC. Można skonfigurować wielu dostawców tożsamości równolegle, modyfikując dwa kluczowe pliki konfiguracyjne:

- **`dashboard_config.toml`** — kontroluje interfejs logowania frontend
- **`config.toml`** — konfiguruje połączenia OIDC w backendzie

### Obsługiwani dostawcy {: #supported-providers-overview }

Przykłady w tym przewodniku używają **Microsoft** i **Google**, ale **każdy dostawca zgodny z OIDC** może zostać zintegrowany według tej samej struktury.

---

## Przewodniki dla dostawców {: #provider-guides }

Każdy dostawca wymaga tych samych czterech wartości — client ID, client secret, redirect URI i discovery URL — lecz każdy umieszcza je w innym miejscu w konsoli administracyjnej, a kilku z nich ma specyficzny krok konfiguracyjny, którego inni nie potrzebują. Poniższe przewodniki obejmują tę część pracy; ta strona opisuje część dotyczącą digna, która jest identyczna dla wszystkich dostawców.

| Dostawca | Przewodnik | Warto wiedzieć |
|---|---|---|
| **AD FS** | [Skonfiguruj SSO z AD FS](adfs_sso_guide.md) | Hostowany samodzielnie; jedyny dostawca tutaj, gdzie kontrolujesz usługę tokenów |
| **Auth0** | [Skonfiguruj SSO z Auth0](auth0_sso_guide.md) | Discovery URL jest per-tenant, a niestandardowe domeny go zmieniają |
| **Google Workspace** | [Skonfiguruj SSO z Google Workspace](google_workspace_sso_guide.md) | Ekran zgody musi być opublikowany, zanim użytkownicy spoza testów będą mogli się logować |
| **Keycloak** | [Skonfiguruj SSO z Keycloak](keycloak_sso_guide.md) | Hostowany samodzielnie; discovery URL jest per-realm |
| **Microsoft Entra ID** | [Skonfiguruj SSO z Microsoft Entra ID](microsoft_entra_id_sso_guide.md) | Tenant ID pojawia się w discovery URL; sekrety wygasają |
| **Okta** | [Skonfiguruj SSO z Okta](okta_sso_guide.md) | Wybór serwera autoryzacji zmienia discovery URL |
| **OneLogin** | [Skonfiguruj SSO z OneLogin](onelogin_sso_guide.md) | Typ aplikacji OIDC musi być wybrany przy tworzeniu i nie można go zmienić |
| **PingOne** | [Skonfiguruj SSO z PingOne](pingone_sso_guide.md) | Environment ID pojawia się w discovery URL |

Każdy inny dostawca zgodny z OIDC działa w ten sam sposób — zobacz [Inni dostawcy OIDC](#supported-providers).

---

## Kroki konfiguracji {: #configuration-steps }

Konfiguracja SSO wymaga aktualizacji dwóch plików. Ta sekcja wyjaśnia, jak skonfigurować każdy z nich.

### Przegląd plików konfiguracyjnych

| Plik | Lokalizacja | Przeznaczenie |
|---|---|---|
| **dashboard_config.toml** | `dashboard/dashboard_config.toml` | Interfejs logowania frontend |
| **config.toml** | `/config.toml` | Połączenia OIDC w backendzie |

Oba pliki muszą być skonfigurowane, aby SSO działało poprawnie.

---

## Konfiguracja dashboardu {: #dashboard-configuration }

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

Określ, czy logowanie przez hasło ma być dozwolone:

```toml
[login]
usePassword = true
```

### Parametry konfiguracji

#### Sekcja `[[login.oidc]]`

| Parametr | Typ | Wymagane | Opis |
|---|---|---|---|
| `key` | string | Tak | Unikalny identyfikator połączenia OIDC (musi pasować do klucza w config.toml) |
| `label` | string | Tak | Tekst wyświetlany na przycisku logowania (np. "Login with Microsoft") |

#### Sekcja `[login]`

| Parametr | Typ | Domyślnie | Opis |
|---|---|---|---|
| `usePassword` | boolean | false | Pozwala na logowanie przy użyciu hasła oprócz SSO |

### Zrozumienie usePassword

**Jeśli `usePassword = true`:**
- Ekran logowania pokazuje przyciski SSO (np. "Login with Microsoft")
- Ekran logowania pokazuje także pola nazwy użytkownika i hasła
- Użytkownicy mogą się uwierzytelniać dowolną z metod
- Pozwala to na konfiguracje hybrydowe, gdzie część użytkowników używa SSO, a inni hasła

**Jeśli `usePassword = false` (lub pominięty):**
- Ekran logowania pokazuje tylko przyciski SSO
- Brak pól nazwy użytkownika/hasła
- Dostępne jest tylko uwierzytelnianie OIDC

!!! tip "Wskazówka"

    Logowanie oparte na haśle jest dostępne tylko dla użytkowników utworzonych z hasłami za pomocą polecenia `digna user add` lub poprzez dashboard.

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

## Konfiguracja backendu {: #backend-configuration }

### Lokalizacja pliku

```
/config.toml
```

(Katalog główny instalacji digna)

### Krok 1: Dodaj sekcje dostawców OIDC

Każdy dostawca musi mieć dedykowaną sekcję `[oidc.<key>]`. Klucz musi pasować do `key` zdefiniowanego w `dashboard_config.toml`.

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

| Parametr | Typ | Wymagane | Opis | Przykład |
|---|---|---|---|---|
| `DIGNA_OIDC_CLIENT_ID` | string | Tak | Client ID od dostawcy tożsamości | `abc123xyz789` |
| `DIGNA_OIDC_CLIENT_SECRET` | string | Tak | Client secret od dostawcy tożsamości | `secret_xyz789abc123` |
| `DIGNA_OIDC_REDIRECT_URI` | string | Tak | URL przekierowania po uwierzytelnieniu | `http://localhost:5173/oidc/callback` |
| `DIGNA_OIDC_CONFIGURATION_URL` | string | Tak | Punkt końcowy konfiguracji OIDC | `https://login.microsoftonline.com/...` |

!!! warning "Ważne"

    Zastąp wartości zastępcze (`<client_id>`, `<client_secret>`, `<tenant_id>`) rzeczywistymi poświadczeniami z portalu deweloperskiego dostawcy tożsamości.

### Redirect URI

Redirect URI musi być taki sam w konfiguracji dostawcy tożsamości:

```
http://localhost:5173/oidc/callback
```

Jeżeli digna jest hostowane pod inną domeną, zaktualizuj odpowiednio:
- Lokalnie: `http://localhost:5173/oidc/callback`
- Produkcyjnie: `https://digna.yourdomain.com/oidc/callback`

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

## Testowanie logowania {: #testing-login }

Po zakończeniu konfiguracji, zweryfikuj, czy SSO działa poprawnie.

### Lista kontrolna przed testami

Przed testowaniem upewnij się, że:

- [ ] `dashboard_config.toml` został zaktualizowany o dostawców OIDC
- [ ] `config.toml` został zaktualizowany o poświadczenia OIDC
- [ ] Oba pliki zostały zapisane
- [ ] Poświadczenia są poprawne (client ID, client secret)
- [ ] Redirect URI odpowiada Twojej domenie deploymentu
- [ ] Aplikacja w dostawcy tożsamości ma skonfigurowany redirect URI

### Kroki testowe

#### Krok 1: Uruchom ponownie usługi

Uruchom ponownie backend digna i serwer WWW, aby zastosować zmiany.

**Jeśli uruchamiasz jako usługę na Windows:**
```bash
cd C:\path\to\digna\bin
stop_service.bat
start_service.bat
```

**Jeśli uruchamiasz jako usługę na Linux lub macOS:**
```bash
cd /opt/digna/bin
sudo ./stop_service.sh
sudo ./start_service.sh
```

**Jeśli uruchamiasz ręcznie:**
```bash
digna serve --address localhost --port 8082
```

**Uruchom ponownie także serwer WWW** — IIS lub Tomcat na Windows, nginx lub Apache na Linux i macOS.

#### Krok 2: Otwórz dashboard

Otwórz dashboard digna w przeglądarce:

```
http://localhost:5173
```

(lub Twój skonfigurowany URL dashboardu)

#### Krok 3: Sprawdź przyciski logowania

Sprawdź, czy pojawiają się przyciski logowania dla każdego skonfigurowanego dostawcy:

- Powinien być widoczny przycisk "Login with Microsoft"
- Powinien być widoczny przycisk "Login with Google"
- (Jeśli usePassword = true) Powinny być widoczne pola nazwy użytkownika/hasła

Jeśli przyciski się nie pojawiają:
- Sprawdź, czy `dashboard_config.toml` został zapisany
- Sprawdź, czy usługa dashboard została ponownie uruchomiona
- Sprawdź konsolę przeglądarki (F12) pod kątem błędów

#### Krok 4: Przetestuj logowanie SSO

Kliknij jeden z przycisków SSO (np. "Login with Microsoft"):

1. Powinieneś zostać przekierowany na stronę logowania dostawcy tożsamości
2. Zaloguj się przy użyciu firmowych poświadczeń
3. Powinieneś zostać przekierowany z powrotem do digna
4. Powinieneś być zalogowany do digna

#### Krok 5: Zweryfikuj tworzenie użytkownika

Po pomyślnym logowaniu SSO:

- Użytkownik powinien zostać automatycznie utworzony w digna
- Użytkownik powinien być zalogowany
- Profil użytkownika powinien wyświetlać poświadczenia dostawcy tożsamości
- Powinieneś zobaczyć dashboard digna

#### Krok 6: Przetestuj logowanie hasłem (jeśli włączone)

Jeśli `usePassword = true`:

1. Wyloguj się z digna
2. Na stronie logowania wpisz nazwę użytkownika i hasło
3. Powinieneś móc zalogować się przy użyciu poświadczeń hasła

---

## Rozwiązywanie problemów {: #troubleshooting }

### Przyciski logowania nie pojawiają się

**Objawy:**
- Przyciski OIDC nie widoczne na stronie logowania
- Widać tylko pola hasła (jeśli usePassword = true)

**Przyczyny i rozwiązania:**
1. Sprawdź, czy `dashboard_config.toml` znajduje się w katalogu `dashboard/`
2. Zweryfikuj, czy sekcje `[[login.oidc]]` są obecne i mają poprawną składnię
3. Uruchom ponownie usługę dashboard
4. Wyczyść pamięć podręczną przeglądarki (Ctrl+Shift+Delete lub Cmd+Shift+Delete)
5. Sprawdź konsolę przeglądarki (F12 → zakładka Console) pod kątem błędów

---

### Błąd rozbieżności Redirect URI

**Objawy:**
- Po kliknięciu przycisku SSO błąd o "redirect_uri mismatch"
- Błąd "The redirect URI is not registered"

**Przyczyny i rozwiązania:**
1. Zweryfikuj `DIGNA_OIDC_REDIRECT_URI` w `config.toml`
2. Zweryfikuj, że redirect URI jest zarejestrowane w ustawieniach dostawcy tożsamości
3. Upewnij się, że oba URI są identyczne (w tym protokół, domena, ścieżka)
4. Sprawdź literówki w redirect URI
5. Jeśli używasz HTTPS, sprawdź ważność certyfikatu

---

### Błąd nieprawidłowych poświadczeń klienta

**Objawy:**
- Błąd "Invalid client ID or secret"
- Uwierzytelnianie kończy się błędem poświadczeń

**Przyczyny i rozwiązania:**
1. Sprawdź, czy `DIGNA_OIDC_CLIENT_ID` i `DIGNA_OIDC_CLIENT_SECRET` są poprawne
2. Upewnij się, że nie ma dodatkowych spacji ani niepożądanych znaków
3. Sprawdź, czy poświadczenia nie wygasły lub nie zostały unieważnione
4. Uruchom ponownie backend po aktualizacji konfiguracji
5. Sprawdź w konsoli dostawcy tożsamości, czy poświadczenia są aktywne

---

### Logowanie zawiesza się lub przekracza limit czasu

**Objawy:**
- Kliknięcie przycisku SSO nic nie robi
- Timeout po kilku sekundach
- Przeglądarka pokazuje "Failed to connect" lub podobny komunikat

**Przyczyny i rozwiązania:**
1. Sprawdź, czy backend digna działa: `digna repo check`
2. Sprawdź łączność sieciową do dostawcy tożsamości
3. Zweryfikuj, czy `DIGNA_OIDC_CONFIGURATION_URL` jest dostępny
4. Sprawdź reguły zapory, czy zezwalają na wychodzące połączenia HTTPS
5. Upewnij się, że backend i dashboard mają do siebie dostęp

---

### Użytkownicy nie są tworzeni automatycznie

**Objawy:**
- Logowanie SSO przebiega pomyślnie, ale użytkownik nie jest tworzony w digna
- Po logowaniu SSO pojawia się błąd uprawnień

**Przyczyny i rozwiązania:**
1. Zweryfikuj poprawność konfiguracji OIDC
2. Sprawdź ustawienia uprawnień użytkowników
3. Przejrzyj logi digna w poszukiwaniu komunikatów o błędach
4. Uruchom ponownie backend
5. Skontaktuj się z support@digna.ai jeśli problem będzie się powtarzał

---

## Obsługiwani dostawcy {: #supported-providers }

### Przetestowane i obsługiwane

Poniższe dostawcy OIDC zostały przetestowane i działają:

| Dostawca | URL konfiguracji | Przewodnik konfiguracji |
|---|---|---|
| **AD FS** | `https://<adfs_host>/adfs/.well-known/openid-configuration` | [Skonfiguruj SSO z AD FS](adfs_sso_guide.md) |
| **Auth0** | `https://<tenant>.<region>.auth0.com/.well-known/openid-configuration` | [Skonfiguruj SSO z Auth0](auth0_sso_guide.md) |
| **Google Workspace** | `https://accounts.google.com/.well-known/openid-configuration` | [Skonfiguruj SSO z Google Workspace](google_workspace_sso_guide.md) |
| **Keycloak** | `https://<host>/realms/<realm>/.well-known/openid-configuration` | [Skonfiguruj SSO z Keycloak](keycloak_sso_guide.md) |
| **Microsoft Entra ID (Azure AD)** | `https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration` | [Skonfiguruj SSO z Microsoft Entra ID](microsoft_entra_id_sso_guide.md) |
| **Okta** | `https://<domain>/.well-known/openid-configuration` | [Skonfiguruj SSO z Okta](okta_sso_guide.md) |
| **OneLogin** | `https://<subdomain>.onelogin.com/oidc/2/.well-known/openid-configuration` | [Skonfiguruj SSO z OneLogin](onelogin_sso_guide.md) |
| **PingOne** | `https://auth.pingone.com/<environment_id>/as/.well-known/openid-configuration` | [Skonfiguruj SSO z PingOne](pingone_sso_guide.md) |

### Inni dostawcy OIDC

Każdy dostawca, który obsługuje OpenID Connect, może zostać zintegrowany. Wymagane informacje:

- Client ID
- Client secret
- URL konfiguracji OpenID (zazwyczaj pod `/.well-known/openid-configuration`)
- Obsługiwane zakresy (zwykle `openid profile email`)

Skontaktuj się z support@digna.ai, jeśli potrzebujesz pomocy przy integracji konkretnego dostawcy.

---

## Najlepsze praktyki

**RÓB:**
- Używaj HTTPS w środowisku produkcyjnym (nie HTTP)
- Przechowuj sekrety klienta bezpiecznie (jeśli to możliwe, używaj zmiennych środowiskowych)
- Okresowo rotuj sekrety
- Testuj najpierw w środowisku nieprodukcyjnym
- Dokumentuj, którzy dostawcy są skonfigurowani
- Monitoruj logi logowań pod kątem nietypowej aktywności
- Utrzymuj konfigurację dostawcy tożsamości w zgodzie z konfiguracją digna

**NIE RÓB:**
- Nie przechowuj sekretów klienta w systemie kontroli wersji
- Nie używaj HTTP redirect URI w produkcji
- Nie konfiguruj wielu dostawców z tym samym kluczem
- Nie zostawiaj domyślnych/testowych poświadczeń w produkcji
- Nie ujawniaj plików konfiguracyjnych zawierających sekrety
- Nie mieszaj poświadczeń deweloperskich i produkcyjnych

---

## Wsparcie

Potrzebujesz pomocy przy konfiguracji SSO?

- **Email:** support@digna.ai
- **Dokumentacja:** https://docs.digna.ai
- **Strona:** https://www.digna.ai

---

**Ostatnia aktualizacja:** 30 sierpnia 2026  
**Wydanie:** 2026.04  
**© 2026 digna GmbH — [www.digna.ai](https://www.digna.ai)**