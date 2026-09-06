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

- **dignabackend**: rdzeń aplikacji, odpowiedzialny za przetwarzanie danych i wykonywanie kontroli jakości.
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
   - `config.toml` — plik konfiguracyjny
   - `license.toml` — plik licencyjny (skopiuj tutaj swoją licencję)

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
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `digna_APP_HOST` | `localhost` lub adres IP | Nazwa hosta lub IP, gdzie jest hostowany dignabackend |
| `digna_APP_PORT` | `8082` (domyślnie) | Port dla endpointów REST API |
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
digna_FERNET_KEY = "your-fernet-key"
digna_COOKIE_DOMAIN = "localhost"
digna_COOKIE_PATH = "/"
digna_COOKIE_SECURE = false
digna_COOKIE_HTTPONLY = true
digna_COOKIE_SAME_SITE = "lax"
digna_TOKEN_EXPIRES_IN = 86400
digna_MAX_WORKERS = 4
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `digna_FERNET_KEY` | Klucz szyfrowania | Używany do szyfrowania tokenów i ciasteczek (domyślnie dostarczony) |
| `digna_COOKIE_DOMAIN` | `localhost` | Dopasuj do domeny frontendu |
| `digna_COOKIE_SECURE` | `false` (lokalnie) / `true` (produkcja) | Ustaw `true` dla połączeń HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Zawsze włączone dla bezpieczeństwa |
| `digna_COOKIE_SAME_SITE` | `lax` | Zapobiega atakom CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 godziny) | Czas wygasania sesji w sekundach |
| `digna_MAX_WORKERS` | Liczba rdzeni CPU - 1 | Liczba równoległych zadań inspekcji |

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

### Krok 5: Uruchom serwer digna

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

### Krok 6: Utwórz użytkownika administratora

1. Otwórz **nowe** okno Wiersza poleceń
2. Przejdź do katalogu instalacji digna
3. Uruchom poniższe polecenie, aby utworzyć użytkownika admin:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Przykład:**

```bash
digna user add admin "Admin User" AdminPassword123! --su
```

To tworzy użytkownika z pełnymi uprawnieniami administracyjnymi.

!!! tip "Dobra praktyka"

    Używaj silnego hasła zawierającego wielkie i małe litery, cyfry oraz znaki specjalne.

---

## Konfiguracja dashboardu {: #dashboard-configuration }

### Krok 1: Wdróż dashboard na serwerze WWW

Dashboard digna posiada własny plik `config.toml` znajdujący się w katalogu `dashboard/`. Ta konfiguracja jest już dostarczona i nie wymaga zmian podczas instalacji początkowej. Trzeba ją zmodyfikować tylko wtedy, gdy chcesz dostosować połączenie z backendem.

Jeśli musisz zmodyfikować konfigurację dashboardu (np. dla wdrożeń wieloinstancyjnych), odwołaj się do dokumentacji dashboardu.

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

### Pliki zarządzania usługą

Wszystkie niezbędne pliki znajdują się w katalogu instalacji digna w: `bin/`

Dostępne pliki wsadowe:
- `install_service.bat` — rejestruje digna jako usługę Windows
- `uninstall_service.bat` — usuwa rejestrację usługi
- `start_service.bat` — uruchamia usługę
- `stop_service.bat` — zatrzymuje usługę

!!! warning "Wymagane uprawnienia administratora"

    Wszystkie pliki wsadowe muszą być uruchamiane z uprawnieniami Administratora.

### Instalacja usługi

1. **Otwórz Wiersz poleceń jako Administrator**
   - Kliknij prawym przyciskiem myszy Wiersz poleceń
   - Wybierz "Uruchom jako administrator"

2. **Przejdź do folderu bin**
   ```bash
   cd C:\path\to\digna\bin
   ```

3. **Uruchom skrypt instalacyjny**
   ```bash
   install_service.bat
   ```

Serwer digna jest teraz zarejestrowany jako usługa Windows z włączonym **automatycznym uruchamianiem**. Usługa nie uruchamia się od razu — zobacz następną sekcję, aby ją uruchomić.

### Uruchamianie i zatrzymywanie usługi

#### Aby uruchomić usługę

1. Otwórz Wiersz poleceń jako Administrator
2. Przejdź do `digna\bin`
3. Uruchom:
   ```bash
   start_service.bat
   ```

#### Aby zatrzymać usługę

1. Otwórz Wiersz poleceń jako Administrator
2. Przejdź do `digna\bin`
3. Uruchom:
   ```bash
   stop_service.bat
   ```

!!! tip "Wskazówka"

    Zawsze zatrzymuj usługę przed aktualizacją plików aplikacji.

### Przenoszenie usługi do nowego katalogu

Jeśli musisz przenieść instalację digna:

1. **Odinstaluj aktualną usługę**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Przenieś pliki aplikacji**
   - Przenieś cały folder instalacji digna do nowej lokalizacji

3. **Zainstaluj usługę ponownie**
   ```bash
   cd C:\new\path\digna\bin
   install_service.bat
   ```

4. **Uruchom usługę**
   ```bash
   start_service.bat
   ```

### Odinstalowywanie usługi

1. **Zatrzymaj działającą usługę**
   ```bash
   cd C:\path\to\digna\bin
   stop_service.bat
   ```

2. **Odinstaluj usługę**
   ```bash
   uninstall_service.bat
   ```

Serwer digna jest teraz wyrejestrowany jako usługa Windows.

---

## Aktualizacja do nowego wydania {: #upgrading-to-a-new-release }

### Przed aktualizacją

**Utworzenie kopii zapasowej repozytorium digna jest obowiązkowe**

Przed aktualizacją digna wykonaj kopię zapasową repozytorium (PostgreSQL), aby zabezpieczyć się przed utratą danych.
Kopia zapasowa pozwoli przywrócić stan w razie napotkania problemów podczas aktualizacji.

### Proces aktualizacji

#### Krok 1: Zatrzymaj usługę digna

Jeśli digna działa jako usługa Windows, najpierw ją zatrzymaj:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Krok 2: Zrób kopię zapasową bieżącej instalacji backendu

W katalogu instalacyjnym digna:

```bash
# Rename folder containing dignabackend
ren dignabackend dignabackend_old
```
```bash
# Rename dashboard
ren dashboard dashboard_old
```

#### Krok 3: Rozpakuj i wdroż nową wersję

1. Rozpakuj nowy plik ZIP instalacji digna
2. Skopiuj nowy plik wykonywalny `digna` oraz folder `dashboard` do katalogu instalacyjnego

!!! warning "Ważne"

    Plik `config.toml` **nigdy** nie jest dołączany do pliku ZIP instalacji. Twoja istniejąca konfiguracja pozostaje bezpieczna.

### Krok 4: Przywróć pliki konfiguracyjne

```bash
copy dashboard_old\dashboard_config.toml dashboard\dashboard_config.toml
```
### Krok 5: Zaktualizuj schemat repozytorium

Przejdź do katalogu instalacyjnego digna i uruchom:

```bash
digna repo upgrade
```

To zaktualizuje schemat PostgreSQL do najnowszej wersji, zachowując wszystkie istniejące dane.

### Krok 6: Uruchom ponownie usługi

Jeśli działasz jako usługa Windows:

```bash
cd C:\path\to\digna\bin
start_service.bat
```

Jeśli uruchamiasz ręcznie, zrestartuj serwer:

```bash
cd C:\path\to\digna
digna serve --address <address> --port <port>
```

Jeśli korzystasz z IIS lub Tomcata, zrestartuj odpowiedni serwer WWW.

#### Krok 7: Zweryfikuj aktualizację

1. Uzyskaj dostęp do dashboardu digna
2. Sprawdź, czy interfejs ładuje się poprawnie
3. Sprawdź logi serwera pod kątem ewentualnych błędów