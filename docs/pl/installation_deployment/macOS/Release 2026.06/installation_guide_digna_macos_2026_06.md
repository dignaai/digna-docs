---
title: Przewodnik instalacji dla macOS – digna Release 2026.06 | Dokumentacja digna
description: Przewodnik krok po kroku instalacji digna Release 2026.06 na macOS — wymagania systemowe, konfiguracja Homebrew i PostgreSQL, konfiguracja nginx lub Apache, konfiguracja backendu i dashboardu, uruchamianie digna jako usługi w tle oraz aktualizacja do nowego wydania.
keywords: digna instalacja macos, przewodnik wdrożenia digna na mac, konfiguracja backendu digna, instalacja dashboardu digna, postgresql homebrew, nginx macos, usługa launchd digna, przewodnik aktualizacji digna
image: /assets/logo_square.png
---

# Przewodnik instalacji digna Release 2026.06 dla macOS

**Wydanie:** 2026.06

**Ostatnia aktualizacja:** 5 września 2026


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
9. [Uruchamianie digna jako usługi w tle](#running-digna-as-a-background-service)
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

### Szukasz Windows lub Linux?

Ten przewodnik dotyczy macOS. Dla innych platform zobacz [Przewodnik instalacji dla Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) lub [Przewodnik instalacji dla Linux](../../Linux/Release%202026.06/installation_guide_digna_linux_2026_06.md).

---

## Wymagania systemowe {: #system-requirements }

Zanim rozpoczniesz instalację, upewnij się, że system spełnia następujące minimalne wymagania:

| Wymaganie | Specyfikacja |
|---|---|
| **System operacyjny** | macOS 13 (Ventura) lub nowszy |
| **Architektura** | Apple Silicon (arm64) lub Intel (x86_64) |
| **Pamięć (Minimalna konfiguracja)** | 16 GB RAM |
| **Miejsce na dysku** | 10 GB dostępnego miejsca |
| **Baza danych** | PostgreSQL Server 12 lub nowszy |
| **Serwer WWW** | nginx, Apache httpd lub równoważny |
| **Narzędzia wiersza poleceń** | Xcode Command Line Tools (wymagane przez Homebrew) |

### Opcje instalacji bazy danych

**Jeśli PostgreSQL jest już zainstalowany:**
Możesz dodać nową bazę danych dla digna do istniejącego serwera PostgreSQL.

**Jeśli instalujesz PostgreSQL na tej samej maszynie co digna:**

!!! info "Zalecane specyfikacje"

    - **Pamięć**: 32 GB RAM (zamiast 16 GB)
    - **Miejsce na dysku**: 50 GB dostępnego miejsca (zamiast 10 GB)

    Te wyższe specyfikacje uwzględniają równoczesne uruchomienie digna i bazy PostgreSQL.

### Sprawdzanie architektury

Kilka ścieżek w tym przewodniku różni się między komputerami Mac z Apple Silicon i z procesorem Intel. Aby sprawdzić, który masz, otwórz **Terminal** i uruchom:

```bash
uname -m
```

- `arm64` — Apple Silicon. Homebrew instaluje się w `/opt/homebrew`.
- `x86_64` — Intel. Homebrew instaluje się w `/usr/local`.

!!! tip "Wskazówka"

    Zamiast wpisywać na sztywno którąkolwiek ze ścieżek, ten przewodnik używa `$(brew --prefix)`, co rozwija się do właściwej lokalizacji na obu architekturach. Polecenia możesz kopiować bez zmian.

---

## Przygotowanie przed instalacją {: #pre-installation-setup }

Przed instalacją digna upewnij się, że są spełnione trzy kluczowe warunki wstępne:

1. **Homebrew** – menedżer pakietów używany do instalacji poniższych komponentów
2. **Serwer PostgreSQL** – do przechowywania wyliczonych metryk i danych wydajnościowych
3. **Serwer WWW** – do hostowania Dashboardu digna

Jeśli te komponenty nie są jeszcze skonfigurowane, postępuj zgodnie z poniższymi sekcjami, aby je zainstalować i skonfigurować.

### Instalacja Homebrew

Homebrew to standardowy menedżer pakietów dla macOS, używany w całym przewodniku do instalacji PostgreSQL i nginx.

#### Krok 1: Sprawdź, czy Homebrew jest już zainstalowany

Otwórz **Terminal** (naciśnij `Cmd + Space`, wpisz `Terminal` i naciśnij Enter) i uruchom:

```bash
brew --version
```

Jeśli zostanie zwrócony numer wersji, przejdź do sekcji [Konfiguracja serwera PostgreSQL](#postgresql-server-setup).

#### Krok 2: Zainstaluj Homebrew

Jeśli polecenie nie zostało znalezione, zainstaluj Homebrew zgodnie z instrukcjami na [oficjalnej stronie Homebrew](https://brew.sh). Instalator instaluje również Xcode Command Line Tools, jeśli nie są jeszcze obecne.

#### Krok 3: Dodaj Homebrew do zmiennej PATH

Na komputerach z Apple Silicon instalator wypisuje dwa polecenia, które dodają Homebrew do środowiska powłoki. Uruchom je zgodnie z instrukcją, a następnie sprawdź:

```bash
brew --prefix
```

Powinno zostać wypisane `/opt/homebrew` na Apple Silicon lub `/usr/local` na komputerach z procesorem Intel.

---

## Konfiguracja serwera PostgreSQL {: #postgresql-server-setup }

### Jeśli masz już PostgreSQL

Jeśli PostgreSQL jest już zainstalowany i działa lokalnie lub jeśli używasz zarządzanego zdalnego serwera PostgreSQL, możesz przejść do [następnej sekcji](#web-server-configuration).

### Opcje instalacji

macOS oferuje dwa proste sposoby instalacji PostgreSQL. Wybierz **jeden**:

- [Homebrew](#postgresql-homebrew) — instalacja z wiersza poleceń, zalecana dla wdrożeń serwerowych
- [Postgres.app](#postgresql-app) — instalacja graficzna, wygodna do lokalnej oceny

### Instalacja PostgreSQL za pomocą Homebrew {: #postgresql-homebrew }

#### Krok 1: Zainstaluj formułę PostgreSQL

```bash
brew install postgresql@16
```

#### Krok 2: Dodaj PostgreSQL do zmiennej PATH

Wersjonowane formuły PostgreSQL są typu *keg-only*, co oznacza, że Homebrew nie dołącza automatycznie ich poleceń do zmiennej PATH. Dodaj je samodzielnie:

```bash
echo 'export PATH="'$(brew --prefix)'/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

!!! note "Uwaga"

    Zakłada to domyślną powłokę `zsh` używaną przez macOS. Jeśli używasz `bash`, dopisz ten sam wiersz do `~/.bash_profile`.

#### Krok 3: Uruchom usługę PostgreSQL

```bash
brew services start postgresql@16
```

To polecenie natychmiast uruchamia PostgreSQL i konfiguruje go tak, aby automatycznie uruchamiał się ponownie po zalogowaniu.

#### Krok 4: Zweryfikuj instalację

```bash
psql --version
```

Jeśli instalacja się powiodła, powinieneś zobaczyć wersję PostgreSQL.

#### Krok 5: Połącz się z serwerem

```bash
psql postgres
```

!!! warning "Ważne — tutaj macOS różni się od Windows"

    Instalator dla Windows prosi o utworzenie superużytkownika `postgres` i hasła. Homebrew tego nie robi. Zamiast tego tworzy superużytkownika o nazwie Twojego **konta macOS**, bez hasła, dostępnego wyłącznie z lokalnej maszyny.

    Oznacza to, że w świeżej instalacji Homebrew nie ma roli `postgres`. Gdy potrzebujesz superużytkownika, użyj nazwy własnego konta, a dedykowanego użytkownika digna utwórz zgodnie z opisem w sekcji [Instalacja początkowa](#initial-installation).

#### Krok 6: Potwierdź port

Domyślny port PostgreSQL to `5432`. Aby potwierdzić port, na którym nasłuchuje Twój serwer:

```bash
psql postgres -c "SHOW port;"
```

Zanotuj tę wartość — będzie potrzebna podczas konfigurowania backendu digna.

### Instalacja PostgreSQL za pomocą Postgres.app {: #postgresql-app }

Jeśli wolisz instalację graficzną:

1. Pobierz [Postgres.app](https://postgresapp.com) i przeciągnij aplikację do folderu **Applications**
2. Otwórz aplikację i kliknij **Initialize**, aby utworzyć nowy serwer
3. Postępuj zgodnie z instrukcjami aplikacji, aby dodać jej narzędzia wiersza poleceń do zmiennej PATH
4. Zweryfikuj instalację:

```bash
psql --version
```

Postgres.app również tworzy superużytkownika o nazwie Twojego konta macOS.

---

## Konfiguracja serwera WWW {: #web-server-configuration }

digna wymaga serwera WWW do hostowania dashboardu. Wybierz jedną z poniższych opcji:

- [nginx](#nginx-setup) — instalowany przez Homebrew, zalecany
- [Apache httpd](#apache-setup) — dołączony do macOS

Wystarczy zainstalować i skonfigurować **jeden** z tych serwerów.

Obie sekcje konfigurują dwie rzeczy, od których zależy dashboard:

- **Mechanizm awaryjny dla aplikacji jednostronicowej (SPA)**, aby odświeżenie adresu URL dashboardu nie zwracało błędu 404
- **Typ MIME dla `.md`**, aby pliki Markdown były serwowane poprawnie

### Konfiguracja nginx {: #nginx-setup }

#### Przegląd

nginx to lekki, wydajny serwer WWW, dobrze nadający się do serwowania statycznego dashboardu digna.

#### Instalacja

```bash
brew install nginx
```

#### Uruchamianie nginx

```bash
brew services start nginx
```

#### Zweryfikuj instalację

1. Otwórz przeglądarkę
2. Przejdź do `http://localhost:8080`
3. Powinieneś zobaczyć stronę powitalną nginx

!!! note "Uwaga — domyślny port to 8080, a nie 80"

    Homebrew konfiguruje nginx do nasłuchiwania na porcie `8080`, aby mógł działać bez uprawnień administratora. W macOS powiązanie z portem `80` lub dowolnym innym portem poniżej 1024 wymaga uprawnień root.

    Aby serwować dashboard na porcie 80, zmień `listen 8080;` na `listen 80;` w poniższej konfiguracji i uruchom nginx poleceniem `sudo brew services start nginx`.

#### Konfigurowanie witryny dla dashboardu

Konfiguracja nginx z Homebrew dołącza każdy plik ze swojego katalogu `servers`. Utwórz tam dedykowany plik konfiguracyjny dla digna:

```bash
nano $(brew --prefix)/etc/nginx/servers/digna.conf
```

Wklej poniższą treść, zastępując `/path/to/digna/dashboard` rzeczywistą ścieżką do rozpakowanego folderu `dashboard`:

```nginx
server {
    listen       8080;
    server_name  localhost;

    root   /path/to/digna/dashboard;
    index  index.html;

    # Serve Markdown files with the correct MIME type.
    types {
        text/markdown  md;
    }

    # Single-page-application fallback: unknown paths return index.html
    # instead of a 404, so dashboard routes survive a browser refresh.
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

!!! warning "Ważne"

    Bez dyrektywy `try_files` przeładowanie dowolnej strony dashboardu innej niż główny adres URL zwraca błąd 404. Jest to odpowiednik modułu URL Rewrite wymaganego przez IIS w systemie Windows.

#### Zastosuj konfigurację

Sprawdź konfigurację pod kątem błędów składni, a następnie przeładuj nginx:

```bash
nginx -t
brew services restart nginx
```

---

### Konfiguracja Apache httpd {: #apache-setup }

#### Przegląd

macOS zawiera Apache httpd, więc instalacja nie jest potrzebna. Domyślnie jest on wyłączony.

#### Uruchamianie Apache

```bash
sudo apachectl start
```

#### Zweryfikuj instalację

1. Otwórz przeglądarkę
2. Przejdź do `http://localhost`
3. Powinieneś zobaczyć komunikat "It works!"

#### Wymagane: włącz mod_rewrite

Dashboard wymaga przepisywania adresów URL. Otwórz konfigurację Apache:

```bash
sudo nano /etc/apache2/httpd.conf
```

Znajdź następujący wiersz i usuń początkowy znak `#`, aby go odkomentować:

```apache
LoadModule rewrite_module libexec/apache2/mod_rewrite.so
```

#### Wymagane: zezwól na nadpisywanie przez .htaccess

W tym samym pliku znajdź blok `<Directory "/Library/WebServer/Documents">` i zmień:

```apache
AllowOverride None
```

na:

```apache
AllowOverride All
```

#### Wymagane: typ MIME dla plików Markdown

Nadal w `httpd.conf` dodaj następujący wiersz, aby pliki Markdown były serwowane poprawnie:

```apache
AddType text/markdown .md
```

!!! warning "Ważne"

    Bez tego ustawienia pliki `.md` mogą nie być serwowane poprawnie.

#### Zastosuj konfigurację

Sprawdź konfigurację pod kątem błędów składni, a następnie zrestartuj Apache:

```bash
sudo apachectl configtest
sudo apachectl restart
```

---

## Instalacja początkowa {: #initial-installation }

### Krok 1: Skonfiguruj repozytorium digna

Repozytorium digna przechowuje wszystkie metryki wyliczane przez digna. Działa jako centralna baza danych dla danych analitycznych i wydajnościowych.

#### Utwórz schemat repozytorium i użytkownika

Otwórz klienta PostgreSQL (psql, pgAdmin lub podobny) i wykonaj poniższe polecenia SQL:

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

Aby wykonać je z Terminala w jednym kroku:

```bash
psql postgres
```

Następnie wklej polecenia w wierszu zachęty `postgres=#` i wpisz `\q`, aby zakończyć.

!!! tip "Dobra praktyka"

    Używaj silnych, złożonych haseł dla użytkowników bazy danych. Unikaj łatwych do odgadnięcia danych uwierzytelniających.

---

### Krok 2: Rozpakuj pakiet instalacyjny digna

1. Znajdź plik ZIP instalacji digna dostarczony Ci
2. Rozpakuj go do wybranej lokalizacji instalacyjnej — na przykład `/opt/digna` lub `~/digna`
3. Po rozpakowaniu powinieneś zobaczyć następujące elementy:
   - `dashboard/` — interfejs webowy
   - `digna` — główny plik wykonywalny (backend + CLI w jednym)

!!! info "Plików konfiguracyjnych i pliku licencji nie ma w pakiecie"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nie są dostarczane z instalacją — oba
    tworzysz samodzielnie, w sekcjach [Konfiguracja backendu](#backend-configuration) i
    [Konfiguracja dashboardu](#dashboard-configuration). `license.toml` również nie jest dołączany;
    digna dostarcza go osobno, zgodnie z opisem w kroku 3.

Aby rozpakować archiwum z Terminala:

```bash
unzip digna-2026.06-macos.zip -d /opt/digna
```

#### Nadaj plikowi wykonywalnemu prawo do uruchamiania

W zależności od sposobu przesłania archiwum bit wykonywalności może nie zachować się po rozpakowaniu. Ustaw go jawnie:

```bash
cd /opt/digna
chmod +x digna
```

#### Jeśli macOS blokuje aplikację

Pliki pobrane przez przeglądarkę lub klienta poczty są oznaczane atrybutem kwarantanny. Jeśli macOS zgłasza, że aplikacji *"nie można otworzyć, ponieważ nie można zweryfikować dewelopera"*, usuń ten atrybut z katalogu instalacyjnego:

```bash
xattr -dr com.apple.quarantine /opt/digna
```

Możesz też otworzyć **Ustawienia systemowe → Prywatność i ochrona**, znaleźć zablokowany element u dołu strony i kliknąć **Otwórz mimo to**.

!!! note "Uwaga"

    Ten krok jest potrzebny tylko wtedy, gdy macOS faktycznie blokuje plik wykonywalny. Pakiety przesłane przez SSH lub z wewnętrznych udziałów plików zwykle nie są objęte kwarantanną.

### Krok 3: Zainstaluj plik licencji

!!! warning "Ważne"

    Plik licencji **nie jest** dołączony do pakietu instalacyjnego i zostanie dostarczony oddzielnie przez digna.

1. Znajdź plik `license.toml` dostarczony Ci
2. Skopiuj go do katalogu głównego instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)

**Dlaczego to ważne:**
Plik licencji zawiera informacje o kliencie, datę wygaśnięcia licencji i podpis cyfrowy. **Nie modyfikuj tego pliku** — jakiekolwiek zmiany unieważnią licencję.

**Struktura katalogów po konfiguracji:**

```
/opt/digna/
├── config.toml         (plik konfiguracyjny)
├── license.toml        (TWÓJ PLIK LICENCYJNY - skopiuj tutaj)
├── digna               (główny plik wykonywalny)
├── bin/                (skrypty zarządzania usługą)
└── dashboard/          (interfejs webowy)
    └── (pliki dashboardu)
```

---

## Konfiguracja backendu {: #backend-configuration }

### Krok 1: Utwórz i edytuj plik konfiguracyjny

Plik `config_template.toml` jest dostarczony w katalogu instalacyjnym digna. Wystarczy zmienić jego nazwę na `config.toml`.

```bash
cd /opt/digna
mv config_template.toml config.toml
```

**Lokalizacja:** `/opt/digna/config.toml`

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

!!! note "Uwaga"

    Jeśli serwujesz dashboard z nginx z Homebrew na jego domyślnym porcie, dozwolonym originem jest `http://localhost:8080`.

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

!!! tip "Wskazówka"

    Aby sprawdzić liczbę rdzeni CPU dostępnych na Twoim komputerze Mac, uruchom `sysctl -n hw.ncpu`.

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

    Ten klucz jest wartością stałą, identyczną we wszystkich instalacjach digna, i to on odszyfrowuje
    wrażliwe wartości w Twoim repozytorium. Ogranicz dostęp do `config.toml` do konta, na którym działa
    digna, trzymaj plik poza systemem kontroli wersji i dyskami współdzielonymi oraz wyłącz go z każdej kopii
    zapasowej przechowywanej mniej bezpiecznie niż samo repozytorium.

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
./digna config check
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

1. Otwórz **Terminal**
2. Przejdź do katalogu instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)
3. Uruchom test połączenia:

```bash
cd /opt/digna
./digna repo check
```

Powinieneś zobaczyć potwierdzenie, że połączenie zostało nawiązane (repozytorium samo w sobie nie zostało jeszcze zainicjowane).

!!! note "Uwaga"

    W macOS polecenia z bieżącego katalogu nie znajdują się w zmiennej PATH, dlatego plik wykonywalny wywołuje się jako `./digna`, a nie `digna`. Aby wszędzie używać krótszej formy, dodaj katalog instalacyjny do zmiennej PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Krok 4: Zainstaluj schemat repozytorium

W tym samym katalogu uruchom:

```bash
./digna repo install
```

To polecenie instaluje niezbędne tabele i schemat w Twojej bazie PostgreSQL.

### Krok 5: Utwórz użytkownika administratora

Użytkownik administratora jest tworzony bezpośrednio w schemacie repozytorium, więc serwer nie musi jeszcze działać. W katalogu instalacji digna uruchom:

```bash
./digna user add <email> <password> "<display_name>" --admin
```

**Przykład:**

```bash
./digna user add admin@example.com 'AdminPassword123!' "Admin User" --admin
```

To tworzy użytkownika o adresie e-mail `admin@example.com` z pełnymi uprawnieniami administracyjnymi.

!!! tip "Wskazówka"

    Umieść hasło w pojedynczych cudzysłowach. `zsh` traktuje znaki takie jak `!`, `$` i `*` w szczególny sposób, a hasło zawierające je bez cudzysłowów nie zostanie przekazane w takiej postaci, w jakiej je wpisano.

!!! tip "Dobra praktyka"

    Używaj silnego hasła zawierającego wielkie i małe litery, cyfry oraz znaki specjalne.

### Krok 6: Uruchom serwer digna

W katalogu instalacyjnym digna uruchom serwer poleceniem:

```bash
./digna serve --address <host> --port <port>
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

!!! tip "Wskazówka"

    Przy pierwszym uruchomieniu serwera macOS może zapytać, czy aplikacja ma przyjmować przychodzące połączenia sieciowe. Kliknij **Zezwalaj**, w przeciwnym razie dashboard nie będzie mógł połączyć się z backendem.

!!! note "Serwer zajmuje terminal"

    `serve` działa na pierwszym planie i pracuje, dopóki nie zatrzymasz go skrótem ++ctrl+c++. Zostaw go uruchomionego, dopóki nie dokończysz konfiguracji; aby zamiast tego uruchamiał się automatycznie przy starcie systemu, zobacz [Uruchamianie digna jako usługi w tle](#running-digna-as-a-background-service).

---

## Konfiguracja dashboardu {: #dashboard-configuration }

### Krok 1: Wdróż dashboard na serwerze WWW

Dashboard digna odczytuje własną konfigurację z pliku `dashboard/dashboard_config.toml`. Ten plik nie jest dostarczany z instalacją — tworzysz go w katalogu `dashboard/`, obok plików dashboardu.

Jego zawartość opisano w sekcji [Logowanie jednokrotne (SSO)](../../../sso/overview.md), bo właśnie tam ten plik jest potrzebny: zawiera opcje logowania oferowane przez dashboard oraz, w przypadku wdrożeń wieloinstancyjnych, połączenie z backendem.

Wybierz serwer WWW i postępuj zgodnie z odpowiednimi krokami wdrożeniowymi.

#### Wdrażanie w nginx

Jeśli wykonano kroki z sekcji [Konfiguracja nginx](#nginx-setup), blok server wskazuje już na folder `dashboard` i kopiowanie nie jest potrzebne.

1. **Potwierdź ścieżkę**
   - Otwórz `$(brew --prefix)/etc/nginx/servers/digna.conf`
   - Sprawdź, czy `root` wskazuje na rozpakowany folder `dashboard`

2. **Upewnij się, że folder jest czytelny**
   ```bash
   chmod -R a+rX /opt/digna/dashboard
   ```

3. **Przeładuj nginx**
   ```bash
   nginx -t
   brew services restart nginx
   ```

4. **Przetestuj instalację**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost:8080` (lub skonfigurowanego adresu URL)
   - Powinieneś zobaczyć stronę logowania dashboardu digna

#### Wdrażanie w Apache httpd

1. **Skopiuj dashboard do katalogu głównego dokumentów**
   ```bash
   sudo cp -R /opt/digna/dashboard /Library/WebServer/Documents/digna
   ```

2. **Dodaj reguły przepisywania**

   Utwórz plik `.htaccess` we wdrożonym folderze, aby trasy dashboardu działały po odświeżeniu przeglądarki:

   ```bash
   sudo nano /Library/WebServer/Documents/digna/.htaccess
   ```

   Wklej poniższą treść:

   ```apache
   RewriteEngine On
   RewriteBase /digna/

   # Serve existing files and directories as-is.
   RewriteCond %{REQUEST_FILENAME} -f [OR]
   RewriteCond %{REQUEST_FILENAME} -d
   RewriteRule ^ - [L]

   # Everything else falls back to the single-page application entry point.
   RewriteRule ^ index.html [L]
   ```

3. **Zrestartuj Apache**
   ```bash
   sudo apachectl restart
   ```

4. **Otwórz dashboard**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost/digna`
   - Powinieneś zobaczyć stronę logowania dashboardu digna

---

## Uruchamianie digna jako usługi w tle {: #running-digna-as-a-background-service }

### Dlaczego uruchamiać digna jako usługę?

Uruchomienie backendu digna jako usługi w tle zapewnia, że:

- Uruchamia się automatycznie podczas startu maszyny
- Działa w tle bez otwartego okna Terminala
- Automatycznie się restartuje w razie awarii
- Można nim zarządzać za pomocą `launchctl`, menedżera usług systemu macOS

### Pliki zarządzania usługą

Wszystkie niezbędne pliki znajdują się w katalogu instalacji digna w: `bin/`

Dostępne skrypty powłoki:

- `install_service.sh` — rejestruje digna w launchd
- `uninstall_service.sh` — usuwa rejestrację usługi
- `start_service.sh` — uruchamia zarejestrowaną usługę
- `stop_service.sh` — zatrzymuje działającą usługę

!!! warning "Wymagane uprawnienia administratora"

    Wszystkie skrypty muszą być uruchamiane przez `sudo`, ponieważ rejestracja usługi uruchamianej przy starcie systemu zapisuje dane w `/Library/LaunchDaemons`.

### Nadawanie skryptom prawa do uruchamiania

Rozpakowanie może nie zachować bitu wykonywalności. Przed pierwszym użyciem wykonaj:

```bash
cd /opt/digna/bin
chmod +x *.sh
```

### Instalacja usługi

1. **Otwórz Terminal**

2. **Przejdź do folderu bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Uruchom skrypt instalacyjny**
   ```bash
   sudo ./install_service.sh
   ```

Serwer digna jest teraz zarejestrowany w launchd z włączonym **automatycznym uruchamianiem**. Usługa nie uruchamia się od razu — zobacz następną sekcję, aby ją uruchomić.

### Uruchamianie i zatrzymywanie usługi

#### Aby uruchomić usługę

1. Otwórz Terminal
2. Przejdź do `/opt/digna/bin`
3. Uruchom:
   ```bash
   sudo ./start_service.sh
   ```

#### Aby zatrzymać usługę

1. Otwórz Terminal
2. Przejdź do `/opt/digna/bin`
3. Uruchom:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Wskazówka"

    Zawsze zatrzymuj usługę przed aktualizacją plików aplikacji.

### Weryfikacja usługi

Aby potwierdzić, że usługa jest zarejestrowana i działa:

```bash
sudo launchctl list | grep digna
```

Wiersz zaczynający się od identyfikatora procesu oznacza, że usługa działa. Znak `-` w pierwszej kolumnie oznacza, że usługa jest zarejestrowana, ale zatrzymana.

### Przenoszenie usługi do nowego katalogu

launchd przechowuje bezwzględną ścieżkę do pliku wykonywalnego, więc przeniesienie instalacji wymaga ponownej rejestracji usługi:

1. **Odinstaluj aktualną usługę**
   ```bash
   cd /old/path/digna/bin
   sudo ./uninstall_service.sh
   ```

2. **Przenieś pliki aplikacji**
   ```bash
   sudo mv /old/path/digna /new/path/digna
   ```

3. **Zainstaluj usługę ponownie**
   ```bash
   cd /new/path/digna/bin
   sudo ./install_service.sh
   ```

4. **Uruchom usługę**
   ```bash
   sudo ./start_service.sh
   ```

### Odinstalowywanie usługi

1. **Zatrzymaj działającą usługę**
   ```bash
   cd /opt/digna/bin
   sudo ./stop_service.sh
   ```

2. **Odinstaluj usługę**
   ```bash
   sudo ./uninstall_service.sh
   ```

Serwer digna jest teraz wyrejestrowany z launchd.

---

## Aktualizacja do nowego wydania {: #upgrading-to-a-new-release }

### Przed aktualizacją

**Najpierw zweryfikuj wszystkie połączenia z bazami danych**

Od wydania 2026.06 digna łączy się z każdą technologią źródłową przez **ODBC**. Wcześniejsze wydania
dawały wybór między sterownikiem właściwym dla danej technologii a ODBC, wskazywany przełącznikiem **Use ODBC**.
Zespół digna zdecydował się oprzeć wyłącznie na ODBC, ponieważ jeden standardowy interfejs daje więcej
niż zestaw sterowników pisanych na miarę:

- **Uwierzytelnianie** — uwierzytelnianie jest częścią ODBC, więc połączenie może korzystać ze wszystkiego, co obsługuje
  jego sterownik: haseł, tokenów i PAT-ów, Kerberosa i Active Directory, MFA i logowania jednokrotnego przez
  przeglądarkę, tożsamości chmurowych, certyfikatów klienta i TLS. Nowe metody pojawiają się wraz z aktualizacją
  sterownika, a nie po oczekiwaniu na wydanie digna.
- **Sterowniki utrzymywane przez dostawców baz danych** — sterownik producenta nadąża za nowymi wersjami serwera
  i poprawkami bezpieczeństwa, a Ty możesz aktualizować go we własnym tempie, niezależnie od digna.
- **Jeden sposób konfigurowania wszystkiego** — każda technologia to lista właściwości klucz–wartość, z tym samym
  interfejsem, tym samym szyfrowaniem wartości wrażliwych i tą samą diagnostyką, zamiast innego zestawu pól
  dla każdego źródła.
- **Strojenie i zasięg** — opcje sterownika, takie jak limity czasu, ustawienia TLS, serwery proxy i rozmiary
  pobierania, są dostępne dla każdego źródła, a podłączyć można każdą technologię ze zgodnym sterownikiem ODBC,
  również taką, dla której digna nie publikuje osobnego przewodnika.

W praktyce oznacza to, że przełącznik **Use ODBC** oraz osobne pola hosta, portu, bazy danych, użytkownika
i hasła już nie istnieją. **Każde połączenie, które nie korzysta jeszcze z ODBC, musi zostać przestawione
na ODBC** — nie ma automatycznej konwersji, więc zaplanuj to przed aktualizacją:

1. Przejrzyj każde połączenie z bazą danych zdefiniowane w Twojej instalacji i wypisz te, które nie używają
   jeszcze ODBC — każde z nich trzeba skonfigurować od nowa.
2. Zainstaluj odpowiedni sterownik ODBC na hoście digna — połączenia otwierane są z serwera, na którym działa
   backend digna, a nie z przeglądarki. Zobacz
   [Instalacja sterownika ODBC na hoście digna](../../../databases/overview.md#install-the-driver).
3. Przygotuj właściwości ODBC dla każdego objętego zmianą połączenia.
   [Przewodniki technologiczne](../../../databases/overview.md#technology-guides) podają dla każdego źródła
   sprawdzony zestaw właściwości.

Po aktualizacji przestaw każde objęte zmianą połączenie na ODBC i przetestuj je z poziomu pulpitu —
zobacz [Tworzenie połączenia z bazą danych](../../../databases/overview.md#create-a-database-connection)
oraz [Testowanie połączenia](../../../databases/overview.md#testing-a-connection).

!!! warning "Połączenia Databricks Legacy"

    Łącznik Databricks Legacy został usunięty w tym wydaniu. Przenieś te połączenia
    na łącznik [Databricks](../../../databases/databricks_connector_guide.md).

**Utworzenie kopii zapasowej repozytorium digna jest obowiązkowe**

Przed aktualizacją digna wykonaj kopię zapasową repozytorium (PostgreSQL), aby zabezpieczyć się przed utratą danych.
Kopia zapasowa pozwoli przywrócić stan w razie napotkania problemów podczas aktualizacji.

Aby utworzyć kopię zapasową z Terminala:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Proces aktualizacji

#### Krok 1: Zatrzymaj usługę digna

Jeśli digna działa jako usługa w tle, najpierw ją zatrzymaj:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jeśli digna działa na pierwszym planie, naciśnij `Ctrl + C` w jej oknie Terminala.

#### Krok 2: Wykonaj kopię bieżącej instalacji

W katalogu instalacyjnym digna zmień nazwy folderów bieżącej instalacji, aby nowe wydanie mogło zostać wdrożone obok nich:

```bash
cd /opt/digna
mv dignabackend dignabackend_old
```
```bash
mv dignacli dignacli_old
```
```bash
mv dashboard dashboard_old
```

!!! info "dignabackend i dignacli nie są już używane"

    Od wydania 2026.06 `dignabackend` i `dignacli` są zastąpione pojedynczym plikiem wykonywalnym `digna`, który łączy backend i CLI. Zachowaj `dignabackend_old` i `dignacli_old` tylko do czasu zweryfikowania aktualizacji — potem możesz usunąć oba foldery. Zachowaj `dashboard_old`, dopóki nie odtworzysz z niego swoich plików konfiguracyjnych (patrz krok 4).

#### Krok 3: Rozpakuj i wdróż nową wersję

1. Rozpakuj nowy plik ZIP instalacji digna
2. Skopiuj nowy plik wykonywalny `digna` oraz folder `dashboard` do katalogu instalacyjnego
3. Przywróć bit wykonywalności i w razie potrzeby usuń atrybut kwarantanny:

```bash
chmod +x /opt/digna/digna
xattr -dr com.apple.quarantine /opt/digna
```

!!! warning "Ważne"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nigdy nie są dołączane do pliku ZIP
    instalacji — zespół digna nigdy nie dostarcza żadnego z tych plików. Aktualizacja nie narusza więc
    Twojej istniejącej konfiguracji, a kopie w folderach `*_old` o zmienionych nazwach są
    jedynymi, jakie posiadasz.

#### Krok 4: Przywróć pliki konfiguracyjne

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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

    Wydanie 2026.06 zastępuje tablicę tabel pojedynczą tabelą dla każdego dostawcy, nazwaną kluczem
    dostawcy. `DIGNA_OIDC_KEY` znika — klucz jest teraz częścią nagłówka sekcji.

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

    Powtórz sekcję dla każdego dostawcy i zadbaj, aby każdy klucz odpowiadał wartości `key` z
    `dashboard_config.toml`. `digna config check` zgłasza `oidc_clients` jako FAILED, dopóki
    stara forma pozostaje na miejscu. Dotyczy to wyłącznie instalacji korzystających z logowania jednokrotnego.

#### Krok 5: Przeładuj serwer WWW

Dashboard to zestaw plików statycznych, więc serwer WWW — i przeglądarka — mogą nadal
serwować poprzednią wersję. Przeładuj lub zrestartuj serwer WWW, który udostępnia folder `dashboard`,
a następnie przeładuj stronę z wymuszonym odświeżeniem (++cmd+shift+r++).

#### Krok 6: Sprawdź konfigurację

Upewnij się, że zaktualizowany `config.toml` jest kompletny, zanim dotkniesz repozytorium:

```bash
./digna config check
```

Każda sekcja musi zgłosić OK. Popraw wszystko, co zostało zgłoszone jako FAILED, i uruchom polecenie ponownie przed kontynuowaniem.

#### Krok 7: Wymień plik licencji

Każde wydanie jest licencjonowane osobno. Skopiuj plik `license.toml` dostarczony przez zespół digna dla
tego wydania do katalogu instalacyjnego, zastępując stary:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nie zachowuj poprzedniej licencji"

    Plik `license.toml` wystawiony dla wcześniejszego wydania nie obejmuje obecnego, a każde polecenie,
    które sprawdza licencję — `user`, `inspection`, `repo` — przerywa działanie, zanim dotknie
    repozytorium, jeśli kontrola się nie powiedzie. Sprawdź licencję, zanim przejdziesz dalej:

    ```bash
    ./digna license check
    ```

#### Krok 8: Zaktualizuj schemat repozytorium

Przejdź do katalogu instalacyjnego digna i uruchom:

```bash
cd /opt/digna
./digna repo upgrade
```

To zaktualizuje schemat PostgreSQL do najnowszej wersji, zachowując wszystkie istniejące dane.

#### Krok 9: Uruchom ponownie usługi

Jeśli digna działa jako usługa w tle:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Jeśli uruchamiasz ręcznie, zrestartuj serwer:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Jeśli korzystasz z nginx lub Apache, zrestartuj odpowiedni serwer WWW:

```bash
brew services restart nginx
```
```bash
sudo apachectl restart
```

#### Krok 10: Zweryfikuj aktualizację

1. Uzyskaj dostęp do dashboardu digna
2. Sprawdź, czy interfejs ładuje się poprawnie
3. Sprawdź logi serwera pod kątem ewentualnych błędów
4. Przestaw na ODBC każde połączenie, które jeszcze z niego nie korzystało, a następnie przetestuj wszystkie połączenia
   — zobacz [Testowanie połączenia](../../../databases/overview.md#testing-a-connection)
