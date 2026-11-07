---
title: Przewodnik instalacji dla macOS – digna Release 2026.11 | Dokumentacja digna
description: Przewodnik krok po kroku instalacji digna Release 2026.11 na macOS — wymagania systemowe, konfiguracja Homebrew i PostgreSQL, konfiguracja nginx lub Apache, konfiguracja backendu i dashboardu, uruchamianie digna jako usługi w tle oraz aktualizacja z wydania 2026.06.
keywords: digna instalacja macos, przewodnik wdrożenia digna na mac, konfiguracja backendu digna, instalacja dashboardu digna, postgresql homebrew, nginx macos, usługa launchd digna, przewodnik aktualizacji digna
image: /assets/logo_square.png
---

# Przewodnik instalacji digna Release 2026.11 dla macOS

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
9. [Uruchamianie digna jako usługi w tle](#running-digna-as-a-background-service)
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

### Szukasz Windows lub Linux?

Ten przewodnik dotyczy macOS. Dla innych platform zobacz [Przewodnik instalacji dla Windows](../../Windows/Release%202026.11/installation_guide_digna_windows_2026_11.md) lub [Przewodnik instalacji dla Linux](../../Linux/Release%202026.11/installation_guide_digna_linux_2026_11.md).

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
unzip digna-2026.11-macos.zip -d /opt/digna
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

!!! note "Uwaga"

    Jeśli serwujesz dashboard z nginx z Homebrew na jego domyślnym porcie, dozwolonym originem jest `http://localhost:8080`.

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
DIGNA_LOGGING_MODE = "INFO"
DIGNA_LOGGING_DIR = "logs"
DIGNA_LOGGING_MAX_FILES = 30
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_LOGGING_MODE` | `INFO` lub `DEBUG` | `INFO` dla produkcji, `DEBUG` do rozwiązywania problemów. Akceptowane są również `TRACE`, `WARN` i `ERROR` |
| `DIGNA_LOGGING_DIR` | `logs` (domyślnie) | Opcjonalne. Katalog rotowanych plików logów, względem katalogu roboczego |
| `DIGNA_LOGGING_MAX_FILES` | `30` (domyślnie) | Opcjonalne. Liczba przechowywanych rotowanych plików logów |

#### Sekcja [duckdb] (opcjonalna) {: #duckdb-section }

Nowość w wydaniu 2026.11. Ta sekcja określa zasoby **digna Engine**, który profiluje
dane wewnątrz digna dla połączeń z bazami danych, których lokalizacja profilowania to **Silnik digna**, oraz
wykonuje kontrole integralności referencyjnej między źródłami danych w różnych połączeniach z bazami danych. Zobacz
[Lokalizacja profilowania](../../../platform/profiling/profiling_location.md).

Sekcja jest opcjonalna. Bez niej obowiązują poniższe wartości domyślne.

```toml
[duckdb]
DIGNA_DUCKDB_MEMORY_LIMIT_MB = 1024
DIGNA_DUCKDB_TEMP_DIRECTORY = "/opt/digna/tmp"
```

| Parametr | Wartość | Uwagi |
|---|---|---|
| `DIGNA_DUCKDB_MEMORY_LIMIT_MB` | `1024` (domyślnie) | Pamięć w MB, z której może korzystać jedno uruchomienie digna Engine. Jednocześnie może być aktywnych do `DIGNA_MAX_WORKERS` uruchomień |
| `DIGNA_DUCKDB_TEMP_DIRECTORY` | Domyślnie: katalog tymczasowy systemu (`$TMPDIR` konta, na którym działa digna) | Katalog na pliki tymczasowe, gdy dane nie mieszczą się w pamięci |

!!! tip "Dobór zasobów dla digna Engine"

    Zaplanuj na hoście digna do `DIGNA_MAX_WORKERS` × `DIGNA_DUCKDB_MEMORY_LIMIT_MB` pamięci
    ponad to, czego używa sama digna, oraz tyle wolnego miejsca na dysku w katalogu tymczasowym,
    aby zmieścić największą inspekcjonowaną datę spośród źródeł danych korzystających z digna Engine.
    Wskaż w `DIGNA_DUCKDB_TEMP_DIRECTORY` dysk z takim miejscem, z prawem zapisu dla konta, na którym
    działa digna:

    ```bash
    mkdir -p /opt/digna/tmp
    ```

    Ta sekcja jest potrzebna tylko wtedy, gdy co najmniej jedno połączenie z bazą danych korzysta z digna Engine
    albo kontrola integralności referencyjnej porównuje źródła danych w różnych połączeniach.

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
 - Template overrides: OK
 - Unknown keys: OK

Overall: OK
```

Popraw wszystko, co zostało zgłoszone jako FAILED, i uruchom polecenie ponownie przed kontynuowaniem. Ostrzeżenie (WARNING) w pozycji **Unknown keys** wymienia klucze w `config.toml`, których digna nie odczytuje; nie mają one żadnego efektu, więc usuń je lub popraw ich pisownię. Pełną listę opcji znajdziesz w [dokumentacji CLI](../../../cli/Command_Line_Interface_202611.md).

### Krok 3: Zainicjuj repozytorium

1. Otwórz **Terminal**
2. Przejdź do katalogu instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)
3. Uruchom test połączenia:

```bash
cd /opt/digna
./digna repo check
```

W nowym schemacie polecenie łączy się, a następnie zgłasza, że repozytorium nie jest jeszcze zainstalowane:

```text
Error: No repo installed. Use the 'digna repo upgrade' command to install it.
```

Na tym etapie jest to oczekiwany wynik: potwierdza, że digna dociera do PostgreSQL i do schematu. Błąd połączenia lub uwierzytelniania wskazuje natomiast na sekcję `[repo]` lub na konfigurację PostgreSQL.

!!! note "Uwaga"

    W macOS polecenia z bieżącego katalogu nie znajdują się w zmiennej PATH, dlatego plik wykonywalny wywołuje się jako `./digna`, a nie `digna`. Aby wszędzie używać krótszej formy, dodaj katalog instalacyjny do zmiennej PATH:

    ```bash
    echo 'export PATH="/opt/digna:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

### Krok 4: Zainstaluj schemat repozytorium

W tym samym katalogu uruchom:

```bash
./digna repo upgrade
```

To polecenie instaluje niezbędne tabele w schemacie repozytorium i kończy się komunikatem:

```text
✅ Repo schema 'dignarepo' is up to date.
```

!!! note "repo upgrade instaluje i aktualizuje"

    Od wydania 2026.11 `repo upgrade` instaluje nowe repozytorium i aktualizuje istniejące.
    `repo install` nadal działa jako inna nazwa tego samego polecenia.

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
- `--address` — nazwa hosta/IP serwera (domyślnie `127.0.0.1`)
- `--port` — port serwera (domyślnie `8000`)

Po uruchomieniu serwer wypisuje adres, na którym nasłuchuje:

```text
Server running on http://127.0.0.1:8082
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

Ta sekcja opisuje aktualizację instalacji wydania 2026.06 do wydania 2026.11. Jeśli Twoja
instalacja jest starsza, najpierw przeczytaj [Aktualizacja z wydania wcześniejszego niż 2026.06](#upgrading-from-a-release-before-2026-06).

### Przed aktualizacją

**Utworzenie kopii zapasowej repozytorium digna jest obowiązkowe**

Przed aktualizacją digna wykonaj kopię zapasową repozytorium (PostgreSQL), aby zabezpieczyć się przed utratą danych.
Kopia zapasowa pozwoli przywrócić stan w razie napotkania problemów podczas aktualizacji.

Aby utworzyć kopię zapasową z Terminala:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

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

Jeśli digna działa jako usługa w tle, najpierw ją zatrzymaj:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jeśli digna działa na pierwszym planie, naciśnij ++ctrl+c++ w jej oknie Terminala.

#### Krok 2: Wykonaj kopię bieżącej instalacji {: #step-2-backup-current-installation }

W katalogu instalacyjnym digna zmień nazwy pliku wykonywalnego i folderu dashboardu bieżącej
instalacji, aby nowe wydanie mogło zostać wdrożone obok nich:

```bash
cd /opt/digna
mv digna digna_old
mv dashboard dashboard_old
```

Zachowaj `digna_old` do czasu zweryfikowania aktualizacji, a `dashboard_old`, dopóki nie odtworzysz
z niego swoich plików konfiguracyjnych (patrz krok 4). Potem możesz usunąć oba.

!!! info "Aktualizacja z wydania wcześniejszego niż 2026.06"

    Zamiast pliku wykonywalnego zmień nazwy folderów `dignabackend` i `dignacli`:
    `mv dignabackend dignabackend_old` i `mv dignacli dignacli_old`. Żaden z nich nie jest używany przez wydanie 2026.11.

#### Krok 3: Rozpakuj i wdróż nową wersję {: #step-3-extract-and-deploy-new-version }

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

#### Krok 4: Przywróć pliki konfiguracyjne {: #step-4-restore-your-configuration-files }

```bash
cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
a następnie przeładuj stronę z wymuszonym odświeżeniem (++cmd+shift+r++).

#### Krok 6: Sprawdź konfigurację {: #step-6-validate-the-configuration }

Upewnij się, że `config.toml` jest kompletny, zanim dotkniesz repozytorium:

```bash
./digna config check
```

Każda sekcja musi zgłosić OK. Popraw wszystko, co zostało zgłoszone jako FAILED, usuń klucze wymienione w pozycji
**Unknown keys** i uruchom polecenie ponownie przed kontynuowaniem.

#### Krok 7: Wymień plik licencji {: #step-7-replace-the-license-file }

Plik licencji zwykle przechodzi bez zmian z jednego wydania do następnego. Wydanie 2026.11 jest
wyjątkiem: dodaje dwa licencjonowane moduły, digna Data Reconciliation i digna Agentic, a licencja
wystawiona przed wydaniem 2026.11 ich nie zawiera. Skopiuj plik `license.toml` dostarczony przez zespół digna
dla wydania 2026.11 do katalogu instalacyjnego, zastępując stary:

```bash
cp /path/to/new/license.toml /opt/digna/license.toml
```

!!! warning "Nie zachowuj poprzedniej licencji"

    Z poprzednią licencją digna nadal się uruchamia, ale digna Data Reconciliation i digna
    MCP Server pozostają wyłączone. Każde polecenie, które sprawdza licencję — `user`,
    `inspection`, `repo` — przerywa działanie, zanim dotknie repozytorium, jeśli kontrola się nie powiedzie.
    Sprawdź nową licencję, zanim przejdziesz dalej:

    ```bash
    ./digna license check
    ```

#### Krok 8: Zaktualizuj schemat repozytorium {: #step-8-upgrade-the-repository-schema }

W katalogu instalacyjnym digna uruchom:

```bash
./digna repo upgrade
```

Wydanie 2026.11 zarządza schematem repozytorium za pomocą wersjonowanych migracji. Pierwsza aktualizacja
z wcześniejszego wydania doprowadza schemat do ostatniej wersji poprzedniego mechanizmu, zapisuje ją jako
punkt wyjścia, a następnie stosuje migracje wydania 2026.11. Kończy się komunikatem:

```text
✅ Baseline migration recorded as applied.
✅ Repo schema 'dignarepo' is up to date.
```

Wszystkie istniejące dane zostają zachowane. Aby w dowolnym momencie sprawdzić stan repozytorium, uruchom
`./digna repo check`: polecenie pokazuje ostatnią zastosowaną migrację oraz migracje oczekujące.

!!! warning "digna nie uruchamia się na nieaktualnym repozytorium"

    Od wydania 2026.11 serwer odmawia uruchomienia, dopóki repozytorium wymaga aktualizacji, i
    informuje o tym, na przykład:

    ```text
    Error: Legacy repo version 3.0.2 installed. Use the 'digna repo upgrade' command to upgrade it.
    ```

    Uruchom `repo upgrade`, zanim uruchomisz serwer lub usługę.

#### Krok 9: Uruchom ponownie usługi {: #step-9-restart-services }

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

#### Krok 10: Zweryfikuj aktualizację {: #step-10-verify-the-upgrade }

1. Potwierdź wydanie nowego pliku wykonywalnego:

    ```bash
    ./digna version
    ```

    Pierwszy wiersz musi brzmieć `Release: 2026.11`.

2. Otwórz dashboard digna i sprawdź, czy interfejs ładuje się poprawnie.
3. Sprawdź dane wyjściowe serwera oraz pliki w katalogu `logs` pod kątem błędów.
4. Przetestuj połączenia z bazami danych — zobacz
   [Testowanie połączenia](../../../databases/overview.md#testing-a-connection). Po aktualizacji
   z wydania wcześniejszego niż 2026.06 najpierw przestaw na ODBC każde połączenie, które jeszcze
   z niego nie korzystało.

Aby zacząć pracę z nowymi modułami, zobacz [digna Data Reconciliation](../../../platform/data_reconciliation/Introduction.md),
[Podłączanie agenta AI](../../../platform/agentic/connect_ai_agent.md) w przypadku digna MCP Server oraz
[Lokalizacja profilowania](../../../platform/profiling/profiling_location.md) w przypadku digna Engine.
