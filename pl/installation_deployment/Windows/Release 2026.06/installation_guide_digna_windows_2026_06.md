# Windows Installation Guide for digna Release 2026.06

**Wydanie:** 2026.06

**Ostatnia aktualizacja:** 30 sierpnia 2026


---

## Spis treści

1. [Wprowadzenie](#introduction)
2. [Wymagania systemowe](#system-requirements)
3. [Przygotowanie przed instalacją](#pre-installation-setup)
4. [Konfiguracja serwera PostgreSQL](#postgresql-server-setup)
5. [Konfiguracja serwera WWW](#web-server-configuration)
6. [Instalacja początkowa](#initial-installation)
7. [Konfiguracja backendu](#backend-configuration)
8. [Konfiguracja dashboardu](#dashboard-configuration)
9. [Uruchamianie digna jako usługi Windows](#running-digna-as-a-windows-service)
10. [Aktualizacja do nowego wydania](#upgrading-to-a-new-release)

---

## Wprowadzenie {: #introduction }

### O digna

digna to kompleksowa platforma napędzana sztuczną inteligencją, zaprojektowana do optymalizacji zarządzania jakością danych w różnych środowiskach danych, takich jak hurtownie, data lake i lakehouse. Zbudowana z myślą o dużej skalowalności i elastyczności, digna rozwiązuje współczesne wyzwania związane z danymi dzięki automatyzacji, monitorowaniu w czasie rzeczywistym i wykrywaniu anomalii.

digna składa się z dwóch głównych komponentów:

- **digna**: rdzeń aplikacji, odpowiedzialny za przetwarzanie danych i wykonywanie kontroli jakości. Łączy backend i interfejs wiersza poleceń w jednym pliku wykonywalnym, zastępując osobne programy `dignabackend` i `dignacli` z wcześniejszych wydań.
- **dignadashboard**: interfejs webowy hostowany na serwerze WWW, zapewniający przyjazny sposób interakcji z platformą digna oraz wizualizację wskaźników jakości danych.

### Co nowego w wydaniu 2026.06

To wydanie wprowadza możliwości obserwowalności danych bezpośrednio w kodzie, umożliwiając deweloperom monitorowanie jakości danych u źródła. Zobacz [notatki o wydaniu](http://docs.digna.ai/changelog/Release_202606/) po pełne szczegóły.

### Szukasz macOS lub Linux?

Ten przewodnik dotyczy Windows. Dla innych platform zobacz [Przewodnik instalacji dla macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md) lub [Przewodnik instalacji dla Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Wymagania systemowe {: #system-requirements }

Zanim rozpoczniesz instalację, upewnij się, że system spełnia następujące minimalne wymagania:

| Wymaganie | Specyfikacja |
|---|---|
| **System operacyjny** | Windows Server lub Windows 10/11 |
| **Pamięć (Minimalna konfiguracja)** | 16 GB RAM |
| **Miejsce na dysku** | 10 GB dostępnego miejsca |
| **Baza danych** | PostgreSQL Server 12 lub nowszy |
| **Serwer WWW** | IIS, Apache Tomcat lub równoważny |

### Opcje instalacji bazy danych

**Jeśli PostgreSQL jest już zainstalowany:**
Możesz dodać nową bazę danych dla digna do istniejącego serwera PostgreSQL.

**Jeśli instalujesz PostgreSQL na tej samej maszynie co digna:**

!!! info "Zalecane specyfikacje"

    - **Pamięć**: 32 GB RAM (zamiast 16 GB)
    - **Miejsce na dysku**: 50 GB dostępnego miejsca (zamiast 10 GB)

    Te wyższe specyfikacje uwzględniają równoczesne uruchomienie digna i bazy PostgreSQL.

---

## Przygotowanie przed instalacją {: #pre-installation-setup }

Przed instalacją digna upewnij się, że są spełnione dwa kluczowe warunki wstępne:

1. **Serwer PostgreSQL** – do przechowywania wyliczonych metryk i danych wydajnościowych
2. **Serwer WWW** – do hostowania Dashboardu digna

Jeśli te komponenty nie są jeszcze skonfigurowane, postępuj zgodnie z poniższymi sekcjami, aby je zainstalować i skonfigurować.

---

## Konfiguracja serwera PostgreSQL {: #postgresql-server-setup }

### Jeśli masz już PostgreSQL

Jeśli PostgreSQL jest już zainstalowany i działa lokalnie lub jeśli używasz zarządzanego zdalnego serwera PostgreSQL, możesz przejść do [następnej sekcji](#web-server-configuration).

### Instalacja PostgreSQL

Wykonaj poniższe kroki, aby zainstalować PostgreSQL na Windows:

#### Krok 1: Pobierz PostgreSQL

1. Odwiedź stronę [PostgreSQL Downloads](https://www.postgresql.org/download/)
2. Wybierz **Windows**
3. Pobierz najnowszy instalator

#### Krok 2: Uruchom instalator

1. Kliknij dwukrotnie pobrany plik instalatora
2. Postępuj zgodnie z instrukcjami kreatora instalacji

#### Krok 3: Wybierz katalog instalacji

Wybierz katalog, w którym PostgreSQL zostanie zainstalowany. Domyślna lokalizacja zazwyczaj jest odpowiednia.

#### Krok 4: Wybierz składniki

Dla standardowej instalacji pozostaw domyślne opcje składników.

#### Krok 5: Ustaw hasło superużytkownika PostgreSQL

Wprowadź i potwierdź hasło dla superużytkownika PostgreSQL (`postgres`). **Zapisz to hasło w bezpiecznym miejscu** — będzie potrzebne później.

#### Krok 6: Skonfiguruj numer portu

Domyślny port PostgreSQL to `5432`. Możesz użyć domyślnego lub określić inny port w razie potrzeby.

!!! tip "Wskazówka"

    Jeśli port 5432 jest już używany, wybierz inny port i zapamiętaj go do późniejszej konfiguracji.

#### Krok 7: Wybierz lokalizację (locale)

Wybierz locale dla bazy danych. Domyślna wartość zazwyczaj jest odpowiednia dla większości instalacji.

#### Krok 8: Zakończ instalację

Kliknij **Dalej** przez kolejne kroki, a następnie kliknij **Zakończ**.

#### Krok 9: Zweryfikuj instalację

Otwórz Wiersz poleceń i sprawdź, czy PostgreSQL został zainstalowany:

```bash
psql --version
```

Powinieneś zobaczyć wersję PostgreSQL, jeśli instalacja zakończyła się sukcesem.

---

## Konfiguracja serwera WWW {: #web-server-configuration }

digna wymaga serwera WWW do hostowania dashboardu. Wybierz jedną z poniższych opcji:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Wystarczy zainstalować i skonfigurować **jeden** z tych serwerów.

### Konfiguracja IIS {: #iis-setup }

#### Przegląd

Internet Information Services (IIS) to serwer WWW firmy Microsoft do hostowania stron i aplikacji webowych.

#### Włączanie IIS

1. **Otwórz Panel sterowania**
   - Naciśnij `Win + R`
   - Wpisz `control` i naciśnij Enter

2. **Przejdź do funkcji systemu Windows**
   - Kliknij **Programy**
   - Wybierz **Włącz lub wyłącz funkcje systemu Windows**

3. **Włącz Internet Information Services**
   - Przewiń w dół i znajdź **Internet Information Services (IIS)**
   - Zaznacz pole, aby go włączyć
   - Kliknij przycisk **+**, aby rozwinąć i upewnić się, że wybrane są podskładniki:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Kliknij OK**, aby zastosować zmiany

5. **Zweryfikuj instalację IIS**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost`
   - Powinieneś zobaczyć stronę powitalną IIS

#### Wymagane: moduł URL Rewrite

IIS wymaga komponentu URL Rewrite. Pobierz i zainstaluj go ze [strony Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Wymagane: typ MIME dla plików Markdown

Aby pliki Markdown (`.md`) były poprawnie serwowane przez IIS:

1. Otwórz **IIS Manager** (naciśnij `Win + R`, wpisz `inetmgr`, naciśnij Enter)
2. Przejdź do **Twoja witryna > MIME Types**
3. Kliknij **Add...**
4. Skonfiguruj:
   - **File name extension**: `.md`
   - **MIME type**: `text/markdown`

!!! warning "Ważne"

    Bez tego ustawienia pliki `.md` mogą nie być serwowane poprawnie.

---

### Konfiguracja Apache Tomcat {: #apache-tomcat-setup }

#### Przegląd

Apache Tomcat to otwartoźródłowy kontener serwletów Java i serwer WWW.

#### Instalacja

1. **Pobierz Apache Tomcat**
   - Odwiedź [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Pobierz dystrybucję ZIP dla Windows

2. **Rozpakuj archiwum**
   - Rozpakuj plik ZIP do katalogu na systemie
   - Przykład: `C:\Program Files\Apache Tomcat`

3. **Zweryfikuj, że Tomcat działa**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost:8080`
   - Powinieneś zobaczyć stronę powitalną Apache Tomcat

!!! tip "Wskazówka"

    Apache Tomcat zazwyczaj uruchamia się automatycznie po instalacji. Jeśli tak się nie dzieje, przejdź do folderu `bin` i uruchom `startup.bat`.

---

## Instalacja początkowa {: #initial-installation }

### Krok 1: Skonfiguruj repozytorium digna

Repozytorium digna przechowuje wszystkie metryki wyliczane przez digna. Działa jako centralna baza danych dla danych analitycznych i wydajnościowych.

#### Utwórz schemat repozytorium i użytkownika

Otwórz klienta PostgreSQL (pgAdmin, psql lub podobny) i wykonaj poniższe polecenia SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Zastąp następujące zmienne:**

- `<digna_repo_schema>` — Wybrana nazwa schematu (np. `dignarepo`)
- `<digna_repo_user>` — Wybrana nazwa użytkownika (np. `digna_user`)
- `<digna_repo_password>` — Bezpieczne hasło dla tego użytkownika

**Przykład:**

```sql
CREATE SCHEMA dignarepo;

CREATE USER digna_user WITH PASSWORD 'YourSecurePassword123!';

GRANT ALL PRIVILEGES ON SCHEMA dignarepo TO digna_user;
```

!!! tip "Dobra praktyka"

    Używaj silnych, złożonych haseł dla użytkowników bazy danych. Unikaj łatwych do odgadnięcia danych uwierzytelniających.

---

### Krok 2: Rozpakuj pakiet instalacyjny digna

1. Znajdź plik ZIP instalacji digna dostarczony Ci
2. Rozpakuj go do wybranej lokalizacji instalacyjnej
3. Po rozpakowaniu powinieneś zobaczyć następujące elementy:
   - `dashboard/` — interfejs webowy
   - `digna` — główny plik wykonywalny (backend + CLI w jednym)

!!! info "Plików konfiguracyjnych i pliku licencji nie ma w pakiecie"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nie są dostarczane z instalacją — oba
    tworzysz samodzielnie, w sekcjach [Konfiguracja backendu](#backend-configuration) i
    [Konfiguracja dashboardu](#dashboard-configuration). `license.toml` również nie jest dołączany;
    digna dostarcza go osobno, zgodnie z opisem w kroku 3.

### Krok 3: Zainstaluj plik licencji

!!! warning "Ważne"

    Plik licencji **nie jest** dołączony do pakietu instalacyjnego i zostanie dostarczony oddzielnie przez digna.

1. Znajdź plik `license.toml` dostarczony Ci
2. Skopiuj go do katalogu głównego instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)

**Dlaczego to ważne:**
Plik licencji zawiera informacje o kliencie, datę wygaśnięcia licencji i podpis cyfrowy. **Nie modyfikuj tego pliku** — jakiekolwiek zmiany unieważnią licencję.

**Struktura katalogów po konfiguracji:**

```
digna_installation/
├── config.toml         (plik konfiguracyjny)
├── license.toml        (TWÓJ PLIK LICENCYJNY - skopiuj tutaj)
├── digna               (główny plik wykonywalny)
└── dashboard/          (interfejs webowy)
    └── (pliki dashboardu)
```

---

## Konfiguracja backendu {: #backend-configuration }

### Krok 1: Utwórz i edytuj plik konfiguracyjny

Plik `config_template.toml` jest dostarczony w katalogu instalacyjnym digna. Wystarczy go zmienić nazwę na `config.toml`.

**Lokalizacja:** `digna_installation/config.toml`

Otwórz `config.toml` w edytorze tekstu i skonfiguruj każdą z poniższych sekcji.

#### Sekcja [app]

Ta sekcja konfiguruje ustawienia aplikacji backend digna:

```toml
[app]
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontendu | Jeśli dashboard jest na innym serwerze, dodaj jego URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Wymagane dla CORS z poświadczeniami |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Zezwalaj na wszystkie metody HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Zezwalaj na wszystkie nagłówki |

#### Sekcja [repo]

Ta sekcja konfiguruje połączenie z bazą danych PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `digna_REPO_HOST` | `localhost` lub adres IP | Nazwa hosta/IP serwera PostgreSQL |
| `digna_REPO_PORT` | `5432` (domyślnie) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nazwa bazy danych |
| `digna_REPO_SCHEMA` | `dignarepo` | Schemat utworzony wcześniej |
| `digna_REPO_USER` | `digna_user` | Użytkownik utworzony w konfiguracji PostgreSQL |
| `digna_REPO_PASSWORD` | Twoje hasło | Hasło ustawione podczas tworzenia schematu |

#### Sekcja [base]

Ta sekcja zawiera ustawienia bezpieczeństwa i ciasteczek:

```toml
[base]
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
DIGNA_SCHEDULER_MAX_DELAY = 100
DIGNA_CLEANUP_TIME = "12:00"
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `digna_COOKIE_DOMAIN` | `localhost` | Dopasuj do domeny frontendu |
| `digna_COOKIE_SECURE` | `false` (lokalnie) / `true` (produkcja) | Ustaw `true` dla połączeń HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Zawsze włączone dla bezpieczeństwa |
| `digna_COOKIE_SAME_SITE` | `lax` | Zapobiega atakom CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 godziny) | Czas wygasania sesji w sekundach |
| `digna_MAX_WORKERS` | Liczba rdzeni CPU - 1 | Liczba równoległych zadań inspekcji |
| `DIGNA_SCHEDULER_MAX_DELAY` | `100` | Maksymalne opóźnienie w sekundach, jakie harmonogram może dodać przed uruchomieniem zaległego zadania |
| `DIGNA_CLEANUP_TIME` | `"12:00"` | Godzina (format 24-godzinny `HH:MM`), o której rozpoczyna się codzienne czyszczenie |

#### Sekcja [encryption]

Ta sekcja zawiera klucz służący do szyfrowania wrażliwych wartości przechowywanych w repozytorium. Jest **wymagana** — `config check` zgłasza sekcję `[encryption]` jako FAILED, jeśli klucza brakuje.

```toml
[encryption]
DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_ENCRYPTION_KEY` | Klucz zakodowany w Base64 | Szyfruje wrażliwe wartości przechowywane w repozytorium digna |

!!! warning "Chroń plik config.toml"

    Ten klucz jest wartością stałą, identyczną we wszystkich instalacjach digna, i to on odszyfrowuje wrażliwe wartości w Twoim repozytorium. Ogranicz dostęp do `config.toml` do konta, na którym działa digna, trzymaj plik poza systemem kontroli wersji i dyskami współdzielonymi oraz wyłącz go z każdej kopii zapasowej przechowywanej mniej bezpiecznie niż samo repozytorium.

#### Sekcja [logging]

Ta sekcja konfiguruje zachowanie logowania:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` lub `DEBUG` | `INFO` dla produkcji, `DEBUG` do rozwiązywania problemów |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Liczba codziennych kopii zapasowych logów do przechowania |

---

### Krok 2: Sprawdź konfigurację

Przed zainicjowaniem repozytorium sprawdź, czy `config.toml` jest kompletny i poprawnie zbudowany. W katalogu instalacyjnym digna uruchom:

```bash
digna config check
```

Każda sekcja jest sprawdzana osobno, więc pojedynczy błąd nie zasłania stanu pozostałych:

```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: OK
 - OIDC config(s): OK

Overall: OK
```

Popraw wszystko, co zostało zgłoszone jako FAILED, i uruchom polecenie ponownie przed kontynuowaniem. Pełną listę opcji znajdziesz w [dokumentacji CLI](../../../cli/Command_Line_Interface_202606.md).

### Krok 3: Zainicjuj repozytorium

1. Otwórz Wiersz poleceń
2. Przejdź do katalogu instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)
3. Uruchom test połączenia:

```bash
digna repo check
```

Powinieneś zobaczyć potwierdzenie, że połączenie zostało nawiązane (repozytorium samo w sobie nie zostało jeszcze zainicjowane).

### Krok 4: Zainstaluj schemat repozytorium

W tym samym katalogu uruchom:

```bash
digna repo install
```

To polecenie instaluje niezbędne tabele i schemat w Twojej bazie PostgreSQL.

### Krok 5: Utwórz użytkownika administratora

1. Otwórz **nowe** okno Wiersza poleceń
2. Przejdź do katalogu instalacji digna
3. Uruchom poniższe polecenie, aby utworzyć użytkownika admin:

```bash
digna user add <email> <password> "<display_name>" --admin
```

**Przykład:**

```bash
digna user add admin@example.com "AdminPassword123!" "Admin User" --admin
```

To tworzy użytkownika z pełnymi uprawnieniami administracyjnymi.

!!! tip "Dobra praktyka"

    Używaj silnego hasła zawierającego wielkie i małe litery, cyfry oraz znaki specjalne.

---

### Krok 6: Uruchom serwer digna

W katalogu instalacyjnym digna uruchom serwer poleceniem:

```bash
digna serve --address <host> --port <port>
```

**Parametry:**
- `--address` — nazwa hosta/IP serwera
- `--port` — port serwera

Powinieneś zobaczyć komunikaty startowe potwierdzające uruchomienie serwera:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

!!! note "Serwer zajmuje terminal"

    `serve` działa na pierwszym planie i pracuje, dopóki nie zatrzymasz go skrótem ++ctrl+c++. Zostaw go uruchomionego, dopóki nie dokończysz konfiguracji; aby zamiast tego uruchamiał się automatycznie przy starcie systemu, zobacz [Uruchamianie digna jako usługi Windows](#running-digna-as-a-windows-service).

## Konfiguracja dashboardu {: #dashboard-configuration }

### Krok 1: Wdróż dashboard na serwerze WWW

Dashboard digna odczytuje własną konfigurację z pliku `dashboard/dashboard_config.toml`. Ten plik nie jest dostarczany z instalacją — tworzysz go w katalogu `dashboard/`, obok plików dashboardu.

Jego zawartość opisano w sekcji [Logowanie jednokrotne (SSO)](../../../sso/overview.md), bo właśnie tam ten plik jest potrzebny: zawiera opcje logowania oferowane przez dashboard oraz, w przypadku wdrożeń wieloinstancyjnych, połączenie z backendem.

Wybierz serwer WWW i postępuj zgodnie z odpowiednimi krokami wdrożeniowymi.

#### Wdrażanie w IIS

1. **Otwórz IIS Manager**
   - Naciśnij `Win + R`, wpisz `inetmgr`, naciśnij Enter

2. **Utwórz nową witrynę**
   - W lewym panelu kliknij prawym przyciskiem myszy **Sites**
   - Wybierz **Add Website...**

3. **Skonfiguruj witrynę**
   - **Site Name**: Wpisz nazwę (np. "dignaDashboard")
   - **Physical Path**: Kliknij Przeglądaj i wybierz folder `dashboard`
   - **Binding**: Ustaw adres IP i port (domyślny port 80 dla HTTP, 443 dla HTTPS)

4. **Uruchom witrynę**
   - Kliknij **OK**, aby utworzyć witrynę
   - Kliknij prawym przyciskiem myszy nową witrynę i wybierz **Start**

5. **Przetestuj instalację**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost` (lub skonfigurowanego URL)
   - Powinieneś zobaczyć stronę logowania dashboardu digna

#### Wdrażanie w Apache Tomcat

1. **Skopiuj dashboard do Tomcat**
   - Skopiuj folder `dashboard` do katalogu `webapps` Tomcata
   - Zmień nazwę, jeśli potrzeba (np. na `digna`)
   - Przykład: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Zweryfikuj wdrożenie**
   - Odśwież lub przeładuj stronę zarządzania Tomcatem (http://localhost:8080)
   - Powinieneś zobaczyć "digna" (lub wybraną nazwę) na liście wdrożonych aplikacji

3. **Dostęp do dashboardu**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost:8080/digna`
   - Powinieneś zobaczyć stronę logowania dashboardu digna

---

## Uruchamianie digna jako usługi Windows {: #running-digna-as-a-windows-service }

### Dlaczego używać usługi Windows?

Uruchomienie backendu digna jako usługi Windows zapewnia, że:
- Uruchamia się automatycznie podczas startu serwera
- Działa w tle bez otwartego okna Wiersza poleceń
- Automatycznie się restartuje w razie awarii
- Może być zarządzana za pomocą narzędzia Usługi systemu Windows

### Polecenia `windows`

Usługą zarządza sam plik wykonywalny `digna`, za pomocą podpoleceń `digna windows`.
Nie ma żadnych plików wsadowych do uruchamiania.

| Polecenie | Przeznaczenie |
|---|---|
| `digna windows install` | Rejestruje digna jako usługę Windows |
| `digna windows start` | Uruchamia zarejestrowaną usługę |
| `digna windows stop` | Zatrzymuje działającą usługę |
| `digna windows uninstall` | Usuwa rejestrację usługi |

!!! warning "Wymagane uprawnienia administratora"

    Wszystkie cztery polecenia muszą być uruchamiane z Wiersza poleceń otwartego jako Administrator.

Każde polecenie przyjmuje `--name`, aby wskazać usługę zarejestrowaną pod nazwą inną niż domyślna. Pełna
lista opcji znajduje się w [dokumentacji CLI](../../../cli/Command_Line_Interface_202606.md).

### Instalacja usługi

1. **Otwórz Wiersz poleceń jako Administrator**
   - Kliknij prawym przyciskiem myszy Wiersz poleceń
   - Wybierz "Uruchom jako administrator"

2. **Przejdź do katalogu instalacyjnego digna**
   ```bash
   cd C:\path\to\digna
   ```

3. **Zarejestruj usługę**
   ```bash
   digna windows install
   ```

!!! important "Podaj adres i port, chyba że wartości domyślne Ci odpowiadają"

    `install` zapisuje adres i port w rejestracji usługi, a usługa nasłuchuje dokładnie na
    zapisanych wartościach. Domyślnie są to `127.0.0.1` i `8000`, które przyjmują połączenia
    wyłącznie z tej samej maszyny. Dashboard na innym hoście nie może się z nimi połączyć, więc podaj
    adres, na którym backend ma nasłuchiwać:

    ```bash
    digna windows install --address 0.0.0.0 --port 8082
    ```

    Te wartości nie są odczytywane z `config.toml`. Aby je później zmienić, odinstaluj usługę i
    zainstaluj ją ponownie z nowymi wartościami.

Usługa jest rejestrowana z **automatycznym uruchamianiem**, więc będzie startować razem z systemem Windows. Nie
uruchamia się od razu — zobacz następną sekcję.

#### Opcje instalacji

| Opcja | Wartość domyślna | Przeznaczenie |
|---|---|---|
| `--name` | `digna` | Nazwa, pod którą usługa ma zostać zarejestrowana |
| `--display-name` | `digna` | Nazwa wyświetlana w services.msc |
| `--description` | `digna data quality backend` | Opis wyświetlany w services.msc |
| `--address` | `127.0.0.1` | Adres, na którym usługa udostępnia swoje API |
| `--port` | `8000` | Port, na którym usługa udostępnia swoje API |
| `--working-dir` | katalog pliku wykonywalnego `digna` | Katalog zawierający `config.toml` i `license.toml`, który usługa ustawia jako swój katalog roboczy |
| `--start-type` | `auto` | `auto` uruchamia usługę razem z systemem Windows, `manual` tylko na żądanie, `disabled` rejestruje usługę, ale nie pozwala jej uruchomić |
| `--account` | `LocalSystem` | Konto, na którym usługa ma działać, np. `DOMAIN\user` lub `.\user` |
| `--password` | | Hasło konta `--account` |

!!! tip "Uruchamianie na koncie domenowym"

    `LocalSystem` nie ma tożsamości sieciowej, więc uwierzytelnianie Windows w SQL Server i każdy
    dostęp do udziału sieciowego zakończą się niepowodzeniem. Zainstaluj usługę z `--account` i `--password`, jeśli
    musi ona uzyskiwać dostęp do zasobów jako określony użytkownik.

### Uruchamianie i zatrzymywanie usługi

#### Aby uruchomić usługę

```bash
digna windows start
```

#### Aby zatrzymać usługę

```bash
digna windows stop
```

!!! tip "Wskazówka"

    Zawsze zatrzymuj usługę przed aktualizacją plików aplikacji.

### Przenoszenie usługi do nowego katalogu

Jeśli musisz przenieść instalację digna:

1. **Zatrzymaj i wyrejestruj aktualną usługę**
   ```bash
   cd C:\old\path\digna
   digna windows stop
   digna windows uninstall
   ```

2. **Przenieś pliki aplikacji**
   - Przenieś cały folder instalacji digna do nowej lokalizacji

3. **Zarejestruj usługę ponownie z nowej lokalizacji**
   ```bash
   cd C:\new\path\digna
   digna windows install
   ```

   Powtórz wszystkie wartości `--address`, `--port` lub `--account` użyte za pierwszym razem — poprzednia
   rejestracja już nie istnieje.

4. **Uruchom usługę**
   ```bash
   digna windows start
   ```

### Odinstalowywanie usługi

1. **Zatrzymaj działającą usługę**
   ```bash
   cd C:\path\to\digna
   digna windows stop
   ```

2. **Wyrejestruj usługę**
   ```bash
   digna windows uninstall
   ```

Serwer digna jest teraz wyrejestrowany jako usługa Windows.

---

## Aktualizacja do nowego wydania {: #upgrading-to-a-new-release }

### Przed aktualizacją

**Najpierw zweryfikuj wszystkie połączenia z bazami danych**

Od wydania 2026.06 digna łączy się z każdą technologią źródłową przez **ODBC**. Wcześniejsze wydania dawały wybór między sterownikiem właściwym dla danej technologii a ODBC, wskazywany przełącznikiem **Use ODBC**. Zespół digna zdecydował się oprzeć wyłącznie na ODBC, ponieważ jeden standardowy interfejs daje więcej niż zestaw sterowników pisanych na miarę:

- **Uwierzytelnianie** — uwierzytelnianie jest częścią ODBC, więc połączenie może korzystać ze wszystkiego, co obsługuje jego sterownik: haseł, tokenów i PAT-ów, Kerberosa i Active Directory, MFA i logowania jednokrotnego przez przeglądarkę, tożsamości chmurowych, certyfikatów klienta i TLS. Nowe metody pojawiają się wraz z aktualizacją sterownika, a nie po oczekiwaniu na wydanie digna.
- **Sterowniki utrzymywane przez dostawców baz danych** — sterownik producenta nadąża za nowymi wersjami serwera i poprawkami bezpieczeństwa, a Ty możesz aktualizować go we własnym tempie, niezależnie od digna.
- **Jeden sposób konfigurowania wszystkiego** — każda technologia to lista właściwości klucz–wartość, z tym samym interfejsem, tym samym szyfrowaniem wartości wrażliwych i tą samą diagnostyką, zamiast innego zestawu pól dla każdego źródła.
- **Strojenie i zasięg** — opcje sterownika, takie jak limity czasu, ustawienia TLS, serwery proxy i rozmiary pobierania, są dostępne dla każdego źródła, a podłączyć można każdą technologię ze zgodnym sterownikiem ODBC, również taką, dla której digna nie publikuje osobnego przewodnika.

W praktyce oznacza to, że przełącznik **Use ODBC** oraz osobne pola hosta, portu, bazy danych, użytkownika i hasła już nie istnieją. **Każde połączenie, które nie korzysta jeszcze z ODBC, musi zostać przestawione na ODBC** — nie ma automatycznej konwersji, więc zaplanuj to przed aktualizacją:

1. Przejrzyj każde połączenie z bazą danych zdefiniowane w Twojej instalacji i wypisz te, które nie używają jeszcze ODBC — każde z nich trzeba skonfigurować od nowa.
2. Zainstaluj odpowiedni sterownik ODBC na hoście digna — połączenia otwierane są z serwera, na którym działa backend digna, a nie z przeglądarki. Zobacz [Instalacja sterownika ODBC na hoście digna](../../../databases/overview.md#install-the-driver).
3. Przygotuj właściwości ODBC dla każdego objętego zmianą połączenia. [Przewodniki technologiczne](../../../databases/overview.md#technology-guides) podają dla każdego źródła sprawdzony zestaw właściwości.

Po aktualizacji przestaw każde objęte zmianą połączenie na ODBC i przetestuj je z poziomu pulpitu — zobacz [Tworzenie połączenia z bazą danych](../../../databases/overview.md#create-a-database-connection) oraz [Testowanie połączenia](../../../databases/overview.md#testing-a-connection).

!!! warning "Połączenia Databricks Legacy"

    Łącznik Databricks Legacy został usunięty w tym wydaniu. Przenieś te połączenia na łącznik [Databricks](../../../databases/databricks_connector_guide.md).

**Utworzenie kopii zapasowej repozytorium digna jest obowiązkowe**

Przed aktualizacją digna wykonaj kopię zapasową repozytorium (PostgreSQL), aby zabezpieczyć się przed utratą danych.
Kopia zapasowa pozwoli przywrócić stan w razie napotkania problemów podczas aktualizacji.

### Proces aktualizacji

#### Krok 1: Zatrzymaj i wyrejestruj starą usługę

Jeśli digna działa jako usługa Windows, zatrzymaj ją za pomocą **plików wsadowych bieżącej
instalacji** — polecenia `digna windows` należą do nowego wydania i nie są jeszcze
dostępne:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

Następnie wyrejestruj usługę, ponownie za pomocą starego pliku wsadowego. Rejestracja wskazuje na stary
plik wykonywalny i jego skrypty, które ta aktualizacja zastępuje, więc nie można jej użyć ponownie:

```bash
uninstall_service.bat
```

!!! warning "Wyrejestruj usługę, zanim zmienisz nazwę czegokolwiek"

    `uninstall_service.bat` znajduje się w folderze `bin`, którego nazwę zaraz zmienisz, i tylko on
    może usunąć utworzoną przez siebie rejestrację. Uruchom go, dopóki stara instalacja jest jeszcze
    na miejscu. Jeśli nazwa folderu została już zmieniona, przywróć ją, wyrejestruj usługę, a następnie kontynuuj.

    Zanotuj konto, na którym działała usługa, oraz adres i port, na których nasłuchiwała — będą
    potrzebne w kroku 9.

#### Krok 2: Wykonaj kopię bieżącej instalacji

W katalogu instalacyjnym digna zmień nazwy folderów bieżącej instalacji, aby nowe wydanie mogło zostać wdrożone obok nich:

```bash
# Rename the folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename the folder containing dignacli
ren dignacli dignacli_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

!!! info "dignabackend i dignacli nie są już używane"

    Od wydania 2026.06 `dignabackend` i `dignacli` są zastąpione pojedynczym plikiem wykonywalnym `digna`, który łączy backend i CLI. Zachowaj `dignabackend_old` i `dignacli_old` tylko do czasu zweryfikowania aktualizacji — potem możesz usunąć oba foldery. Zachowaj `dashboard_old`, dopóki nie odtworzysz z niego swoich plików konfiguracyjnych (patrz krok 4). Folder `bin` również przestaje być potrzebny: jego pliki wsadowe obsługiwały starą usługę, a wydanie 2026.06 ich nie zawiera, więc po wyrejestrowaniu usługi w kroku 1 mogą jedynie wprowadzać w błąd.

#### Krok 3: Rozpakuj i wdroż nową wersję

1. Rozpakuj nowy plik ZIP instalacji digna
2. Skopiuj nowy plik wykonywalny `digna` oraz folder `dashboard` do katalogu instalacyjnego

!!! warning "Ważne"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nigdy nie są dołączane do pliku ZIP
    instalacji — zespół digna nigdy nie dostarcza żadnego z tych plików. Aktualizacja nie narusza więc
    Twojej istniejącej konfiguracji, a kopie w folderach `*_old` o zmienionych nazwach są
    jedynymi, jakie posiadasz.

#### Krok 4: Przywróć pliki konfiguracyjne

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
!!! warning "Wydanie 2026.06 zmienia plik config.toml"

    Trzy ustawienia są nowe i wymagane, a trzy nie są już używane. Plik `config.toml` przeniesiony z wcześniejszego wydania nie zawiera nowych ustawień, a digna nie uruchomi się, dopóki ich brakuje. Dodaj do istniejącego `config.toml` następujące wpisy:

    ```toml
    [base]
    DIGNA_SCHEDULER_MAX_DELAY = 100
    DIGNA_CLEANUP_TIME = "12:00"

    [encryption]
    DIGNA_ENCRYPTION_KEY = 'ycELf6IbcO55dYIZHpPv6kQv/bbnUXoIaHLh2bh1kMg='
    ```

    Dodaj dwa klucze `[base]` do istniejącej sekcji `[base]` i dodaj `[encryption]` jako nową sekcję. Następnie usuń ustawienia, które nie są już używane: **`digna_FERNET_KEY`** z sekcji `[base]` oraz **`digna_APP_HOST`** i **`digna_APP_PORT`** z sekcji `[app]` — adres i port serwer pobiera teraz z `digna serve`.

    Znaczenie poszczególnych ustawień opisano w [Konfiguracji backendu](#backend-configuration).

!!! warning "Logowanie jednokrotne: format [oidc_clients] uległ zmianie"

    Wydanie 2026.06 zastępuje tablicę tabel pojedynczą tabelą dla każdego dostawcy, nazwaną kluczem dostawcy. `DIGNA_OIDC_KEY` znika — klucz jest teraz częścią nagłówka sekcji.

    Przed:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Po:

    ```toml
    [oidc_clients.microsoft]
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Powtórz sekcję dla każdego dostawcy i zadbaj, aby każdy klucz odpowiadał wartości `key` z `dashboard_config.toml`. `digna config check` zgłasza `oidc_clients` jako FAILED, dopóki stara forma pozostaje na miejscu. Dotyczy to wyłącznie instalacji korzystających z logowania jednokrotnego.

#### Krok 5: Przeładuj serwer WWW

Dashboard to zestaw plików statycznych, więc serwer WWW — i przeglądarka — mogą nadal
serwować poprzednią wersję. Przeładuj lub zrestartuj serwer WWW, który udostępnia folder `dashboard`,
a następnie przeładuj stronę z wymuszonym odświeżeniem (++ctrl+f5++).

#### Krok 6: Sprawdź konfigurację

Upewnij się, że zaktualizowany `config.toml` jest kompletny, zanim dotkniesz repozytorium:

```bash
digna config check
```

Każda sekcja musi zgłosić OK. Popraw wszystko, co zostało zgłoszone jako FAILED, i uruchom polecenie ponownie przed kontynuowaniem.

#### Krok 7: Wymień plik licencji

Każde wydanie jest licencjonowane osobno. Skopiuj plik `license.toml` dostarczony przez zespół digna dla
tego wydania do katalogu instalacyjnego, zastępując stary:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nie zachowuj poprzedniej licencji"

    Plik `license.toml` wystawiony dla wcześniejszego wydania nie obejmuje obecnego, a każde polecenie,
    które sprawdza licencję — `user`, `inspection`, `repo` — przerywa działanie, zanim dotknie
    repozytorium, jeśli kontrola się nie powiedzie. Sprawdź licencję, zanim przejdziesz dalej:

    ```bash
    digna license check
    ```

#### Krok 8: Zaktualizuj schemat repozytorium

Przejdź do katalogu instalacyjnego digna i uruchom:

```bash
digna repo upgrade
```

To zaktualizuje schemat PostgreSQL do najnowszej wersji, zachowując wszystkie istniejące dane.

#### Krok 9: Zarejestruj i uruchom usługę

Stara rejestracja została usunięta w kroku 1, więc usługę rejestruje się ponownie — tym razem za pomocą
pliku wykonywalnego `digna`, bez plików wsadowych:

```bash
cd C:\path\to\digna
digna windows install --address <address> --port <port>
digna windows start
```

Podaj w `--address` i `--port` wartości, na których nasłuchiwała stara usługa, chyba że chcesz użyć nowych
wartości domyślnych `127.0.0.1` i `8000`; są one zapisywane w rejestracji i nie są już odczytywane
z `config.toml`. Dodaj `--account` i `--password`, jeśli stara usługa działała na koncie
domenowym. Pełną listę opcji znajdziesz w sekcji
[Uruchamianie digna jako usługi Windows](#running-digna-as-a-windows-service).

Jeśli uruchamiasz ręcznie, zrestartuj serwer:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jeśli korzystasz z IIS lub Tomcata, zrestartuj odpowiedni serwer WWW.

#### Krok 10: Zweryfikuj aktualizację

1. Uzyskaj dostęp do dashboardu digna
2. Sprawdź, czy interfejs ładuje się poprawnie
3. Sprawdź logi serwera pod kątem ewentualnych błędów
4. Przestaw na ODBC każde połączenie, które jeszcze z niego nie korzystało, a następnie przetestuj wszystkie połączenia — zobacz [Testowanie połączenia](../../../databases/overview.md#testing-a-connection)