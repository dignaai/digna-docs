---
title: Przewodnik instalacji dla Windows – digna Release 2026.11 | Dokumentacja digna
description: Przewodnik krok po kroku instalacji digna Release 2026.11 na Windows — wymagania systemowe, konfiguracja PostgreSQL, konfiguracja serwera WWW, konfiguracja backendu i dashboardu, uruchamianie digna jako usługi Windows oraz aktualizacja z wydania 2026.06.
keywords: digna instalacja windows, przewodnik wdrożenia digna, konfiguracja backendu digna, instalacja dashboardu digna, konfiguracja postgresql, usługa windows digna, przewodnik aktualizacji digna
image: /assets/logo_square.png
---

# Przewodnik instalacji digna Release 2026.11 dla Windows

**Wydanie:** 2026.11

**Ostatnia aktualizacja:** 7 listopada 2026


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

### Co nowego w wydaniu 2026.11

To wydanie wprowadza digna Data Reconciliation, digna Agentic z digna MCP Server oraz digna Engine, który potrafi profilować dane wewnątrz digna i sprawdzać integralność referencyjną między różnymi technologiami baz danych. Pełne szczegóły znajdziesz w [notatkach o wydaniu](../../../changelog/Release_202611.md).

Z punktu widzenia instalacji wydanie wprowadza nowy mechanizm migracji repozytorium, opcjonalną sekcję `[duckdb]` w `config.toml` dla digna Engine oraz nowy plik licencji. Każdy z tych elementów omawia [sekcja o aktualizacji](#upgrading-to-a-new-release).

### Szukasz macOS lub Linux?

Ten przewodnik dotyczy Windows. Dla innych platform zobacz [Przewodnik instalacji dla macOS](../../macOS/Release%202026.11/installation_guide_digna_macos_2026_11.md) lub [Przewodnik instalacji dla Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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

!!! info "digna Engine"

    Połączenia z bazami danych, które jako lokalizację profilowania wykorzystują digna Engine, są profilowane
    bezpośrednio na hoście digna. Zaplanuj dla nich dodatkową pamięć i miejsce na dysku, zobacz
    [sekcję \[duckdb\]](#duckdb-section).

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

Ta sekcja konfiguruje mechanizm CORS (cross-origin resource sharing) między dashboardem a backendem:

```toml
[app]
DIGNA_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
DIGNA_APP_CORS_ALLOW_CREDENTIALS = true
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_APP_CORS_ALLOW_ORIGINS` | Adresy URL dashboardu | Adresy URL, z których serwowany jest dashboard. Żądania przeglądarki z każdego innego originu są odrzucane |
| `DIGNA_APP_CORS_ALLOW_CREDENTIALS` | `true` | Wymagane, aby przeglądarka wysyłała ciasteczko sesji z każdym żądaniem |

!!! info "Sekcja [app] jest opcjonalna"

    Od wydania 2026.11 można pominąć oba klucze, a nawet całą sekcję `[app]`. To właściwa
    konfiguracja, gdy reverse proxy serwuje dashboard i backend pod jednym originem: przeglądarka
    nie wysyła wtedy żądań między originami, a domyślnie żadne takie żądanie nie jest dozwolone.

#### Sekcja [repo]

Ta sekcja konfiguruje połączenie z bazą danych PostgreSQL:

```toml
[repo]
DIGNA_REPO_HOST = "localhost"
DIGNA_REPO_PORT = 5432
DIGNA_REPO_DB = "postgres"
DIGNA_REPO_SCHEMA = "dignarepo"
DIGNA_REPO_USER = "digna_user"
DIGNA_REPO_PASSWORD = "YourSecurePassword123!"
DIGNA_REPO_SSLMODE = "prefer"
DIGNA_REPO_NUM_CONNS = 16
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_REPO_HOST` | `localhost` lub adres IP | Nazwa hosta/IP serwera PostgreSQL |
| `DIGNA_REPO_PORT` | `5432` (domyślnie) | Port PostgreSQL |
| `DIGNA_REPO_DB` | `postgres` | Nazwa bazy danych |
| `DIGNA_REPO_SCHEMA` | `dignarepo` | Schemat utworzony wcześniej |
| `DIGNA_REPO_USER` | `digna_user` | Użytkownik utworzony w konfiguracji PostgreSQL |
| `DIGNA_REPO_PASSWORD` | Twoje hasło | Hasło ustawione podczas tworzenia schematu |
| `DIGNA_REPO_SSLMODE` | `prefer` (domyślnie) | Opcjonalne. Tryb SSL PostgreSQL: `disable`, `allow`, `prefer`, `require`, `verify-ca` lub `verify-full` |
| `DIGNA_REPO_NUM_CONNS` | `16` (domyślnie) | Opcjonalne. Liczba połączeń z repozytorium, które digna utrzymuje otwarte |

#### Sekcja [base]

Ta sekcja zawiera ustawienia bezpieczeństwa, ciasteczek i inspekcji:

```toml
[base]
DIGNA_FERNET_KEY = "DU4a0yJ-OqvbKCL4hNQn_CsknH-V1vWmHZqBUl-AY44="
DIGNA_COOKIE_DOMAIN = "localhost"
DIGNA_COOKIE_SECURE = false
DIGNA_COOKIE_HTTPONLY = true
DIGNA_TOKEN_EXPIRES_IN = 86400
DIGNA_MAX_WORKERS = 4
DIGNA_FRONTEND_BASEURL = "http://localhost/"
DIGNA_SOURCE_QUERY_TIMEOUT_SEC = 3600
DIGNA_SOURCE_LOGIN_TIMEOUT_SEC = 30
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_FERNET_KEY` | Wartość pokazana powyżej | Klucz szyfrowania używanego przez wcześniejsze wydania. Musi być obecny; zachowaj pokazaną wartość |
| `DIGNA_COOKIE_DOMAIN` | `localhost` | Host, pod którym dostępny jest dashboard. `""` nie ustawia domeny, co jest właściwe za proxy, które serwuje dashboard i backend pod jednym originem |
| `DIGNA_COOKIE_SECURE` | `false` (HTTP) / `true` (HTTPS) | Musi mieć wartość `true` zawsze, gdy digna jest serwowana przez HTTPS |
| `DIGNA_COOKIE_HTTPONLY` | `true` | Chroni ciasteczko sesji przed dostępem ze skryptów |
| `DIGNA_TOKEN_EXPIRES_IN` | `86400` (24 godziny) | Czas wygasania sesji w sekundach |
| `DIGNA_MAX_WORKERS` | Liczba rdzeni CPU - 1 | Liczba inspekcji, które mogą działać jednocześnie |
| `DIGNA_FRONTEND_BASEURL` | URL dashboardu | Wymagane. Używany w linkach w powiadomieniach, więc musi to być adres URL, który odbiorcy mogą otworzyć |
| `DIGNA_SOURCE_QUERY_TIMEOUT_SEC` | `3600` (domyślnie) | Opcjonalne. Liczba sekund, przez które pojedyncze zapytanie do źródłowej bazy danych może działać, zanim zostanie przerwane; `0` wyłącza limit czasu |
| `DIGNA_SOURCE_LOGIN_TIMEOUT_SEC` | `30` (domyślnie) | Opcjonalne. Liczba sekund oczekiwania na połączenie ze źródłową bazą danych; `0` oznacza oczekiwanie bez limitu |

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` lub `DEBUG` | `INFO` dla produkcji, `DEBUG` do rozwiązywania problemów. Akceptowane są również `TRACE`, `WARN` i `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (domyślnie) | Opcjonalne. Katalog rotowanych plików logów, względem katalogu roboczego |
| `DIGNA_LOGGING_MAX_FILES` | `30` (domyślnie) | Opcjonalne. Liczba przechowywanych rotowanych plików logów |

!!! warning "Zachowaj katalog logów, gdy digna działa jako usługa"

    Usługa Windows nie ma konsoli, więc pliki logów są jedynym zapisem tego, co robi usługa.
    Nie ustawiaj `DIGNA_LOGGING_DIR` na pusty ciąg znaków, ponieważ wyłącza to pliki logów.

#### Sekcja [duckdb] (opcjonalna) {: #duckdb-section }

Nowość w wydaniu 2026.11. Ta sekcja określa zasoby **digna Engine**, który profiluje
dane wewnątrz digna dla połączeń z bazami danych, których lokalizacja profilowania to **Silnik digna**, oraz
wykonuje kontrole integralności referencyjnej między źródłami danych w różnych połączeniach z bazami danych. Zobacz
[Lokalizacja profilowania](../../../platform/profiling/profiling_location.md).

Sekcja jest opcjonalna. Bez niej obowiązują poniższe wartości domyślne.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "C:\\path\\to\\digna\\tmp"
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (domyślnie) | Pamięć w MB, z której może korzystać jedno uruchomienie digna Engine. Jednocześnie może być aktywnych do `DIGNA_MAX_WORKERS` uruchomień |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Domyślnie: katalog tymczasowy konta, na którym działa digna (`%TEMP%`) | Katalog na pliki tymczasowe, gdy dane nie mieszczą się w pamięci |

!!! tip "Dobór zasobów dla digna Engine"

    Zaplanuj na hoście digna do `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` pamięci
    ponad to, czego używa sama digna, oraz tyle wolnego miejsca na dysku w katalogu tymczasowym,
    aby zmieścić największą inspekcjonowaną datę spośród źródeł danych korzystających z digna Engine.
    Wskaż w `DIGNA_DUCKDB_TEMP_DIRECTORY` dysk z takim miejscem, z prawem zapisu dla konta, na którym
    działa digna:

    ```cmd
    mkdir C:\path\to\digna\tmp
    ```

    Ta sekcja jest potrzebna tylko wtedy, gdy co najmniej jedno połączenie z bazą danych korzysta z digna Engine
    albo kontrola integralności referencyjnej porównuje źródła danych w różnych połączeniach.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Popraw wszystko, co zostało zgłoszone jako FAILED, i uruchom polecenie ponownie przed kontynuowaniem. Ostrzeżenie (WARNING) w pozycji **Unknown keys** wymienia klucze w `config.toml`, których digna nie odczytuje; nie mają one żadnego efektu, więc usuń je lub popraw ich pisownię. Pełną listę opcji znajdziesz w [dokumentacji CLI](../../../cli/Command_Line_Interface_202611.md).

### Krok 3: Zainicjuj repozytorium

1. Otwórz Wiersz poleceń
2. Przejdź do katalogu instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)
3. Uruchom test połączenia:

```bash
digna repo check
```

W nowym schemacie polecenie łączy się, a następnie zgłasza, że repozytorium nie jest jeszcze zainstalowane:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Na tym etapie jest to oczekiwany wynik: potwierdza, że digna dociera do PostgreSQL i do schematu. Błąd połączenia lub uwierzytelniania wskazuje natomiast na sekcję `[repo]` lub na konfigurację PostgreSQL.

### Krok 4: Zainstaluj schemat repozytorium

W tym samym katalogu uruchom:

```bash
digna repo upgrade
```

To polecenie instaluje niezbędne tabele w schemacie repozytorium i kończy się komunikatem:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instaluje i aktualizuje"

    Od wydania 2026.11 `repo upgrade` instaluje nowe repozytorium i aktualizuje istniejące.
    `repo install` nadal działa jako inna nazwa tego samego polecenia.

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
- `--address` — nazwa hosta/IP serwera (domyślnie `127.0.0.1`)
- `--port` — port serwera (domyślnie `8000`)

Po uruchomieniu serwer wypisuje adres, na którym nasłuchuje:

```text
Server running on http://127.0.0.1:8082
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
lista opcji znajduje się w [dokumentacji CLI](../../../cli/Command_Line_Interface_202611.md).

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

Ta sekcja opisuje aktualizację instalacji wydania 2026.06 do wydania 2026.11. Jeśli Twoja
instalacja jest starsza, najpierw przeczytaj [Aktualizacja z wydania wcześniejszego niż 2026.06](#upgrading-from-a-release-before-2026-06).

### Przed aktualizacją

**Utworzenie kopii zapasowej repozytorium digna jest obowiązkowe**

Przed aktualizacją digna wykonaj kopię zapasową repozytorium (PostgreSQL), aby zabezpieczyć się przed utratą danych.
Kopia zapasowa pozwoli przywrócić stan w razie napotkania problemów podczas aktualizacji.

**Zamów plik licencji dla wydania 2026.11**

Wydanie 2026.11 wymaga nowego pliku `license.toml`. Poproś o niego zespół digna przed rozpoczęciem
i przygotuj go na [krok 7](#step-7-replace-the-license-file).

### Aktualizacja z wydania wcześniejszego niż 2026.06 {: #upgrading-from-a-release-before-2026-06 }

Wydanie 2026.06 wprowadziło trzy zmiany, które nadal obowiązują, gdy aktualizujesz starszą instalację
bezpośrednio do wydania 2026.11:

- **Tylko ODBC.** digna łączy się z każdą technologią źródłową przez ODBC. Każde połączenie z bazą danych, które
  nie korzysta jeszcze z ODBC, trzeba po aktualizacji przestawić na ODBC; nie ma automatycznej
  konwersji. Wcześniej zainstaluj sterowniki ODBC na hoście digna, zobacz
  [Instalacja sterownika ODBC na hoście digna](../../../databases/overview.md#install-the-driver),
  i przygotuj właściwości każdego połączenia na podstawie
  [przewodników technologicznych](../../../databases/overview.md#technology-guides). Łącznik Databricks Legacy
  już nie istnieje; przenieś te połączenia na łącznik
  [Databricks](../../../databases/databricks_connector_guide.md).
- **Jeden plik wykonywalny.** `dignabackend` i `dignacli` zostały zastąpione pojedynczym plikiem wykonywalnym `digna`,
  który łączy backend i CLI.
- **config.toml.** Sekcja `[encryption]` jest wymagana, a `DIGNA_APP_HOST` i
  `DIGNA_APP_PORT` nie są już odczytywane: adres i port serwer pobiera z `digna serve`.
  Porównaj swój plik z [Konfiguracją backendu](#backend-configuration).

Poniższe kroki wskazują, w których miejscach starsza instalacja wymaga innego postępowania. Aktualizacja
repozytorium w kroku 8 przenosi repozytorium z dowolnego wcześniejszego wydania bezpośrednio do wydania 2026.11.

### Proces aktualizacji

#### Krok 1: Zatrzymaj usługę digna {: #step-1-stop-the-digna-service }

Otwórz Wiersz poleceń jako administrator i zatrzymaj usługę za pomocą pliku wykonywalnego `digna`
bieżącej instalacji:

```bash
cd C:\path\to\digna
digna windows stop
```

Usługa pozostaje zarejestrowana. Nowy plik wykonywalny zajmuje miejsce starego w tym samym
katalogu, więc rejestracja nadal wskazuje właściwy plik.

Jeśli digna działa na pierwszym planie, naciśnij ++ctrl+c++ w jej oknie Wiersza poleceń.

!!! warning "Aktualizacja z wydania wcześniejszego niż 2026.06"

    Wydania wcześniejsze niż 2026.06 rejestrowały usługę za pomocą plików wsadowych. Zatrzymaj i wyrejestruj ją
    plikami wsadowymi bieżącej instalacji, **zanim** w kroku 2 zmienisz nazwę czegokolwiek:

    ```bash
    cd C:\path\to\digna\bin
    stop_service.bat
    uninstall_service.bat
    ```

    Zanotuj konto, na którym działała usługa, oraz adres i port, na których nasłuchiwała. Usługę
    zarejestrujesz ponownie w kroku 9.

#### Krok 2: Wykonaj kopię bieżącej instalacji {: #step-2-backup-current-installation }

W katalogu instalacyjnym digna zmień nazwy pliku wykonywalnego i folderu dashboardu bieżącej
instalacji, aby nowe wydanie mogło zostać wdrożone obok nich:

```bash
cd C:\path\to\digna
ren digna.exe digna_old.exe
ren dashboard dashboard_old
```

Zachowaj `digna_old.exe` do czasu zweryfikowania aktualizacji, a `dashboard_old`, dopóki nie odtworzysz
z niego swoich plików konfiguracyjnych (patrz krok 4). Potem możesz usunąć oba.

!!! info "Aktualizacja z wydania wcześniejszego niż 2026.06"

    Zamiast pliku wykonywalnego zmień nazwy folderów `dignabackend` i `dignacli`:
    `ren dignabackend dignabackend_old` i `ren dignacli dignacli_old`. Wydanie 2026.11 nie używa żadnego z tych folderów ani folderu `bin` z plikami wsadowymi.

#### Krok 3: Rozpakuj i wdróż nową wersję {: #step-3-extract-and-deploy-new-version }

1. Rozpakuj nowy plik ZIP instalacji digna
2. Skopiuj nowy plik wykonywalny `digna` oraz folder `dashboard` do katalogu instalacyjnego

!!! warning "Ważne"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nigdy nie są dołączane do pliku ZIP
    instalacji — zespół digna nigdy nie dostarcza żadnego z tych plików. Aktualizacja nie narusza więc
    Twojej istniejącej konfiguracji, a kopie w folderach `*_old` o zmienionych nazwach są
    jedynymi, jakie posiadasz.

#### Krok 4: Przywróć pliki konfiguracyjne {: #step-4-restore-your-configuration-files }

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```

Wydanie 2026.11 nie wymaga żadnych zmian w `config.toml`: plik, który działa z wydaniem 2026.06, działa
nadal. Dwie zmiany są opcjonalne:

- Dodaj [sekcję `[duckdb]`](#duckdb-section), jeśli połączenia z bazami danych mają korzystać z digna Engine,
  a jego wartości domyślne nie pasują do Twojego hosta.
- Pomiń sekcję `[app]`, jeśli reverse proxy serwuje dashboard i backend pod jednym
  originem.

!!! warning "Ustawienia, których digna nie odczytuje"

    Wcześniejsze wersje tego przewodnika pokazywały niektóre ustawienia, których digna nie odczytuje. Nie mają
    one żadnego efektu, a `config check` wymienia je w kroku 6 w pozycji **Unknown keys**. Usuń je lub
    popraw:

    - `DIGNA_SCHEDULER_MAX_DELAY`, `DIGNA_CLEANUP_TIME`, `digna_COOKIE_PATH`,
      `digna_COOKIE_SAME_SITE`, `digna_APP_CORS_ALLOW_METHODS`, `digna_APP_CORS_ALLOW_HEADERS` i
      `digna_LOGGING_BACKUP_COUNT` nie istnieją. Usuń je.
    - W nazwach ustawień rozróżniana jest wielkość liter. digna odczytuje `DIGNA_REPO_HOST`, a nie `digna_REPO_HOST`.
      Zapisuj każdą nazwę wielkimi literami, tak jak w [Konfiguracji backendu](#backend-configuration).

!!! warning "Logowanie jednokrotne: zachowaj [[oidc_clients]]"

    digna odczytuje dostawców logowania jednokrotnego jako listę wpisów `[[oidc_clients]]`, z których każdy ma własny
    `DIGNA_OIDC_KEY`. Jeśli zmieniłeś dostawców na sekcje `[oidc_clients.<key>]`, jak pokazywała
    wcześniejsza wersja tego przewodnika, przywróć poprzednią formę. `config check` zgłasza
    `OIDC config(s)` jako FAILED, dopóki ta forma pozostaje na miejscu:

    ```toml
    [[oidc_clients]]
    DIGNA_OIDC_KEY = 'microsoft'
    DIGNA_OIDC_CLIENT_ID = '<client_id>'
    DIGNA_OIDC_CLIENT_SECRET = '<client_secret>'
    DIGNA_OIDC_REDIRECT_URI = 'http://localhost:3000/oidc/callback'
    DIGNA_OIDC_CONFIGURATION_URL = 'https://login.microsoftonline.com/<tenant_id>/v2.0/.well-known/openid-configuration'
    ```

    Powtórz wpis dla każdego dostawcy i zadbaj, aby każdy `DIGNA_OIDC_KEY` odpowiadał wartości `key` w
    `dashboard_config.toml`. Dotyczy to wyłącznie instalacji korzystających z logowania jednokrotnego.

#### Krok 5: Przeładuj serwer WWW {: #step-5-reload-the-web-server }

Dashboard to zestaw plików statycznych, więc serwer WWW — i przeglądarka — mogą nadal
serwować poprzednią wersję. Przeładuj lub zrestartuj serwer WWW, który udostępnia folder `dashboard`,
a następnie przeładuj stronę z wymuszonym odświeżeniem (++ctrl+f5++).

#### Krok 6: Sprawdź konfigurację {: #step-6-validate-the-configuration }

Upewnij się, że `config.toml` jest kompletny, zanim dotkniesz repozytorium:

```bash
digna config check
```

Każda sekcja musi zgłosić OK. Popraw wszystko, co zostało zgłoszone jako FAILED, usuń klucze wymienione w pozycji
**Unknown keys** i uruchom polecenie ponownie przed kontynuowaniem.

#### Krok 7: Wymień plik licencji {: #step-7-replace-the-license-file }

Plik licencji zwykle przechodzi bez zmian z jednego wydania do następnego. Wydanie 2026.11 jest
wyjątkiem: dodaje dwa licencjonowane moduły, digna Data Reconciliation i digna Agentic, a licencja
wystawiona przed wydaniem 2026.11 ich nie zawiera. Skopiuj plik `license.toml` dostarczony przez zespół digna
dla wydania 2026.11 do katalogu instalacyjnego, zastępując stary:

```bash
copy /Y C:\path\to\new\license.toml license.toml
```

!!! warning "Nie zachowuj poprzedniej licencji"

    Z poprzednią licencją digna nadal się uruchamia, ale digna Data Reconciliation i digna
    MCP Server pozostają wyłączone. Każde polecenie, które sprawdza licencję — `user`,
    `inspection`, `repo` — przerywa działanie, zanim dotknie repozytorium, jeśli kontrola się nie powiedzie.
    Sprawdź nową licencję, zanim przejdziesz dalej:

    ```bash
    digna license check
    ```

#### Krok 8: Zaktualizuj schemat repozytorium {: #step-8-upgrade-the-repository-schema }

W katalogu instalacyjnym digna uruchom:

```bash
digna repo upgrade
```

Wydanie 2026.11 zarządza schematem repozytorium za pomocą wersjonowanych migracji. Pierwsza aktualizacja
z wcześniejszego wydania doprowadza schemat do ostatniej wersji poprzedniego mechanizmu, zapisuje ją jako
punkt wyjścia, a następnie stosuje migracje wydania 2026.11. Kończy się komunikatem:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Wszystkie istniejące dane zostają zachowane. Aby w dowolnym momencie sprawdzić stan repozytorium, uruchom
`digna repo check`: polecenie pokazuje ostatnią zastosowaną migrację oraz migracje oczekujące.

!!! warning "digna nie uruchamia się na nieaktualnym repozytorium"

    Od wydania 2026.11 serwer odmawia uruchomienia, dopóki repozytorium wymaga aktualizacji, i
    informuje o tym, na przykład:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Uruchom `repo upgrade`, zanim uruchomisz serwer lub usługę.

#### Krok 9: Uruchom ponownie usługi {: #step-9-restart-services }

Jeśli digna działa jako usługa Windows, uruchom ją ponownie:

```bash
cd C:\path\to\digna
digna windows start
```

Jeśli aktualizujesz z wydania wcześniejszego niż 2026.06 i w kroku 1 wyrejestrowałeś usługę, najpierw
zarejestruj ją ponownie za pomocą pliku wykonywalnego `digna`:

```bash
digna windows install --address <address> --port <port>
digna windows start
```

Podaj w `--address` i `--port` wartości, na których nasłuchiwała stara usługa, chyba że chcesz użyć
wartości domyślnych `127.0.0.1` i `8000`. Dodaj `--account` i `--password`, jeśli stara usługa działała
na koncie domenowym. Pełną listę opcji znajdziesz w sekcji
[Uruchamianie digna jako usługi Windows](#running-digna-as-a-windows-service).

Jeśli uruchamiasz ręcznie, zrestartuj serwer:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jeśli korzystasz z IIS lub Tomcata, zrestartuj odpowiedni serwer WWW.

#### Krok 10: Zweryfikuj aktualizację {: #step-10-verify-the-upgrade }

1. Potwierdź wydanie nowego pliku wykonywalnego:

    ```bash
    digna version
    ```

    Pierwszy wiersz musi brzmieć `Release: 2026.11`.

2. Otwórz dashboard digna i sprawdź, czy interfejs ładuje się poprawnie.
3. Sprawdź pliki w katalogu `logs` instalacji pod kątem błędów.
4. Przetestuj połączenia z bazami danych — zobacz
   [Testowanie połączenia](../../../databases/overview.md#testing-a-connection). Po aktualizacji
   z wydania wcześniejszego niż 2026.06 najpierw przestaw na ODBC każde połączenie, które jeszcze
   z niego nie korzystało.

Aby zacząć pracę z nowymi modułami, zobacz [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Podłączanie agenta AI](../../../platform/agentic/connect_ai_agent.md) w przypadku digna MCP Server oraz
[Lokalizacja profilowania](../../../platform/profiling/profiling_location.md) w przypadku digna Engine.
