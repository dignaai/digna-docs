---
title: Przewodnik instalacji dla Linux – digna Release 2026.06 | Dokumentacja digna
description: Przewodnik krok po kroku instalacji digna Release 2026.06 na Linux — wymagania systemowe, konfiguracja PostgreSQL, konfiguracja nginx lub Apache, konfiguracja backendu i dashboardu, uruchamianie digna jako usługi systemd oraz aktualizacja do nowego wydania.
keywords: digna instalacja linux, przewodnik wdrożenia digna, konfiguracja backendu digna, instalacja dashboardu digna, postgresql linux, nginx linux, usługa systemd digna, przewodnik aktualizacji digna
image: /assets/logo_square.png
---

# Przewodnik instalacji digna Release 2026.06 dla Linux

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
9. [Uruchamianie digna jako usługi systemd](#running-digna-as-a-systemd-service)
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

### Szukasz Windows lub macOS?

Ten przewodnik dotyczy Linux. Dla innych platform zobacz [Przewodnik instalacji dla Windows](../../Windows/Release%202026.06/installation_guide_digna_windows_2026_06.md) lub [Przewodnik instalacji dla macOS](../../macOS/Release%202026.06/installation_guide_digna_macos_2026_06.md).

### Których dystrybucji dotyczy ten przewodnik?

Instrukcje zostały napisane dla dwóch najpopularniejszych rodzin systemów serwerowych. Tam, gdzie się one różnią, podano oba polecenia:

- **Rodzina Debian** — Debian, Ubuntu. Menedżer pakietów: `apt`.
- **Rodzina RHEL** — Red Hat Enterprise Linux, Rocky Linux, AlmaLinux, Fedora. Menedżer pakietów: `dnf`.

Zadziała każda nowoczesna dystrybucja z `systemd`; zmieniają się jedynie nazwy pakietów i kilka ścieżek konfiguracyjnych.

---

## Wymagania systemowe {: #system-requirements }

Zanim rozpoczniesz instalację, upewnij się, że system spełnia następujące minimalne wymagania:

| Wymaganie | Specyfikacja |
|---|---|
| **System operacyjny** | Ubuntu 22.04 LTS lub nowszy, Debian 12 lub nowszy, RHEL 9 / Rocky 9 / AlmaLinux 9 lub nowszy |
| **Architektura** | x86_64 (amd64) lub arm64 |
| **System init** | systemd |
| **Pamięć (Minimalna konfiguracja)** | 16 GB RAM |
| **Miejsce na dysku** | 10 GB dostępnego miejsca |
| **Baza danych** | PostgreSQL Server 12 lub nowszy |
| **Serwer WWW** | nginx, Apache httpd lub równoważny |

### Opcje instalacji bazy danych

**Jeśli PostgreSQL jest już zainstalowany:**
Możesz dodać nową bazę danych dla digna do istniejącego serwera PostgreSQL.

**Jeśli instalujesz PostgreSQL na tej samej maszynie co digna:**

!!! info "Zalecane specyfikacje"

    - **Pamięć**: 32 GB RAM (zamiast 16 GB)
    - **Miejsce na dysku**: 50 GB dostępnego miejsca (zamiast 10 GB)

    Te wyższe specyfikacje uwzględniają równoczesne uruchomienie digna i bazy PostgreSQL.

### Sprawdzanie dystrybucji i architektury

Kilka poleceń w tym przewodniku różni się między rodzinami Debian i RHEL. Aby sprawdzić, z której korzystasz, uruchom:

```bash
cat /etc/os-release
uname -m
```

- `ID=ubuntu` lub `ID=debian` — używaj poleceń `apt`.
- `ID=rhel`, `rocky`, `almalinux` lub `fedora` — używaj poleceń `dnf`.
- `x86_64` lub `aarch64` — architektura potrzebnego pakietu instalacyjnego.

---

## Przygotowanie przed instalacją {: #pre-installation-setup }

Przed instalacją digna upewnij się, że są spełnione dwa kluczowe warunki wstępne:

1. **Serwer PostgreSQL** – do przechowywania wyliczonych metryk i danych wydajnościowych
2. **Serwer WWW** – do hostowania Dashboardu digna

Jeśli te komponenty nie są jeszcze skonfigurowane, postępuj zgodnie z poniższymi sekcjami, aby je zainstalować i skonfigurować.

### Odświeżanie indeksu pakietów

Zaktualizuj listy pakietów, zanim cokolwiek zainstalujesz:

```bash
sudo apt update
```
```bash
sudo dnf check-update
```

!!! note "Uwaga"

    W całym przewodniku pierwsze polecenie z pary jest przeznaczone dla **rodziny Debian**, a drugie dla **rodziny RHEL**. Uruchamiaj tylko to, które pasuje do Twojego systemu.

---

## Konfiguracja serwera PostgreSQL {: #postgresql-server-setup }

### Jeśli masz już PostgreSQL

Jeśli PostgreSQL jest już zainstalowany i działa lokalnie lub jeśli używasz zarządzanego zdalnego serwera PostgreSQL, możesz przejść do [następnej sekcji](#web-server-configuration).

### Instalacja PostgreSQL

#### Krok 1: Zainstaluj pakiet serwera

```bash
sudo apt install -y postgresql postgresql-contrib
```
```bash
sudo dnf install -y postgresql-server postgresql-contrib
```

!!! tip "Wskazówka"

    Pakiety dystrybucji mogą nie nadążać za bieżącym wydaniem PostgreSQL. Jeśli potrzebujesz konkretnej, nowszej wersji, użyj zamiast tego oficjalnego [repozytorium apt lub yum PostgreSQL](https://www.postgresql.org/download/linux/).

#### Krok 2: Zainicjuj klaster bazy danych

W **rodzinie Debian** pakiet automatycznie tworzy i uruchamia klaster — przejdź do następnego kroku.

W **rodzinie RHEL** klaster trzeba utworzyć jawnie:

```bash
sudo postgresql-setup --initdb
```

#### Krok 3: Uruchom i włącz usługę

```bash
sudo systemctl enable --now postgresql
```

To polecenie natychmiast uruchamia PostgreSQL i konfiguruje go tak, aby automatycznie uruchamiał się ponownie przy starcie systemu.

#### Krok 4: Zweryfikuj instalację

```bash
psql --version
sudo systemctl status postgresql
```

Powinieneś zobaczyć wersję PostgreSQL oraz usługę w stanie `active (running)`.

#### Krok 5: Połącz się z serwerem

Pakiet PostgreSQL dla Linux tworzy konto systemowe `postgres`, które jest właścicielem klastra. Połącz się za jego pośrednictwem:

```bash
sudo -u postgres psql
```

!!! note "Uwaga — tutaj Linux różni się od Windows"

    Instalator dla Windows prosi podczas instalacji o ustawienie hasła superużytkownika `postgres`. Pakiety dla Linux tego nie robią. Zamiast tego połączenia lokalne są uwierzytelniane za pomocą **uwierzytelniania peer**: użytkownik systemu operacyjnego `postgres` może łączyć się jako użytkownik bazy danych `postgres` bez hasła.

    Dlatego powyższe polecenie używa `sudo -u postgres`. Backend digna łączy się przez TCP z nazwą użytkownika i hasłem, więc w sekcji [Instalacja początkowa](#initial-installation) utworzysz dedykowanego użytkownika digna.

#### Krok 6: Potwierdź port

Domyślny port PostgreSQL to `5432`. Aby potwierdzić port, na którym nasłuchuje Twój serwer:

```bash
sudo -u postgres psql -c "SHOW port;"
```

Zanotuj tę wartość — będzie potrzebna podczas konfigurowania backendu digna.

#### Krok 7: Włącz uwierzytelnianie hasłem dla użytkownika digna

digna łączy się z PostgreSQL przez TCP jako `digna_user`, co wymaga uwierzytelniania hasłem zamiast uwierzytelniania peer. Sprawdź, czy Twój plik `pg_hba.conf` na to pozwala.

Znajdź plik:

```bash
sudo -u postgres psql -c "SHOW hba_file;"
```

Otwórz go w edytorze i upewnij się, że lokalne wiersze TCP używają metody `scram-sha-256` (lub `md5` na starszych serwerach), a nie `ident`:

```
# TYPE  DATABASE  USER  ADDRESS         METHOD
host    all       all   127.0.0.1/32    scram-sha-256
host    all       all   ::1/128         scram-sha-256
```

Po każdej zmianie przeładuj PostgreSQL:

```bash
sudo systemctl reload postgresql
```

!!! warning "Ważne"

    Jeśli digna zgłasza `FATAL: Ident authentication failed for user "digna_user"`, przyczyną jest właśnie to ustawienie.

#### Krok 8: Jeśli PostgreSQL działa na innej maszynie

Aby przyjmować połączenia z innego hosta, ustaw `listen_addresses` w `postgresql.conf` i dodaj w `pg_hba.conf` odpowiedni wiersz `host` dla swojej sieci:

```
listen_addresses = '*'
```

Następnie otwórz port w zaporze sieciowej i zrestartuj usługę:

```bash
sudo ufw allow 5432/tcp
```
```bash
sudo firewall-cmd --permanent --add-port=5432/tcp && sudo firewall-cmd --reload
```
```bash
sudo systemctl restart postgresql
```

---

## Konfiguracja serwera WWW {: #web-server-configuration }

digna wymaga serwera WWW do hostowania dashboardu. Wybierz jedną z poniższych opcji:

- [nginx](#nginx-setup) — lekki i zalecany
- [Apache httpd](#apache-setup) — szeroko stosowana alternatywa

Wystarczy zainstalować i skonfigurować **jeden** z tych serwerów.

Obie sekcje konfigurują dwie rzeczy, od których zależy dashboard:

- **Mechanizm awaryjny dla aplikacji jednostronicowej (SPA)**, aby odświeżenie adresu URL dashboardu nie zwracało błędu 404
- **Typ MIME dla `.md`**, aby pliki Markdown były serwowane poprawnie

### Konfiguracja nginx {: #nginx-setup }

#### Przegląd

nginx to lekki, wydajny serwer WWW, dobrze nadający się do serwowania statycznego dashboardu digna.

#### Instalacja

```bash
sudo apt install -y nginx
```
```bash
sudo dnf install -y nginx
```

#### Uruchamianie nginx

```bash
sudo systemctl enable --now nginx
```

#### Zweryfikuj instalację

1. Otwórz przeglądarkę
2. Przejdź do `http://localhost`
3. Powinieneś zobaczyć stronę powitalną nginx

#### Otwieranie zapory sieciowej

Jeśli serwer jest osiągany z innych maszyn, zezwól na ruch HTTP:

```bash
sudo ufw allow 'Nginx Full'
```
```bash
sudo firewall-cmd --permanent --add-service=http && sudo firewall-cmd --reload
```

#### Konfigurowanie witryny dla dashboardu

W obu rodzinach dystrybucji nginx dołącza każdy plik ze swojego katalogu `conf.d`. Utwórz tam dedykowany plik konfiguracyjny dla digna:

```bash
sudo nano /etc/nginx/conf.d/digna.conf
```

Wklej poniższą treść, zastępując `/opt/digna/dashboard` rzeczywistą ścieżką do rozpakowanego folderu `dashboard`:

```nginx
server {
    listen       80 default_server;
    listen       [::]:80 default_server;
    server_name  _;

    root   /opt/digna/dashboard;
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

#### Wyłącz domyślną witrynę

Tylko jeden blok server może być `default_server` dla danego portu. W **rodzinie Debian** usuń domyślną witrynę z pakietu, aby nie powodowała konfliktu:

```bash
sudo rm /etc/nginx/sites-enabled/default
```

W **rodzinie RHEL** zakomentuj lub usuń blok `server { ... }` w pliku `/etc/nginx/nginx.conf`.

#### Zastosuj konfigurację

Sprawdź konfigurację pod kątem błędów składni, a następnie przeładuj nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

---

### Konfiguracja Apache httpd {: #apache-setup }

#### Przegląd

Apache httpd jest dostępny w domyślnych repozytoriach każdej obsługiwanej dystrybucji. Pakiet nazywa się `apache2` w rodzinie Debian i `httpd` w rodzinie RHEL.

#### Instalacja

```bash
sudo apt install -y apache2
```
```bash
sudo dnf install -y httpd
```

#### Uruchamianie Apache

```bash
sudo systemctl enable --now apache2
```
```bash
sudo systemctl enable --now httpd
```

#### Zweryfikuj instalację

1. Otwórz przeglądarkę
2. Przejdź do `http://localhost`
3. Powinieneś zobaczyć domyślną stronę Apache danej dystrybucji

#### Wymagane: włącz mod_rewrite

Dashboard wymaga przepisywania adresów URL.

W **rodzinie Debian** włącz moduł i zrestartuj serwer:

```bash
sudo a2enmod rewrite
sudo systemctl restart apache2
```

W **rodzinie RHEL** moduł `mod_rewrite` jest ładowany domyślnie. Potwierdź to:

```bash
httpd -M | grep rewrite
```

#### Wymagane: zezwól na nadpisywanie przez .htaccess

Otwórz plik konfiguracyjny dla katalogu głównego dokumentów:

```bash
sudo nano /etc/apache2/apache2.conf
```
```bash
sudo nano /etc/httpd/conf/httpd.conf
```

Znajdź blok `<Directory>` obejmujący katalog główny dokumentów (`/var/www/html` w obu rodzinach) i zmień:

```apache
AllowOverride None
```

na:

```apache
AllowOverride All
```

#### Wymagane: typ MIME dla plików Markdown

W tym samym pliku dodaj następujący wiersz, aby pliki Markdown były serwowane poprawnie:

```apache
AddType text/markdown .md
```

!!! warning "Ważne"

    Bez tego ustawienia pliki `.md` mogą nie być serwowane poprawnie.

#### Zastosuj konfigurację

Sprawdź konfigurację pod kątem błędów składni, a następnie zrestartuj Apache:

```bash
sudo apachectl configtest
sudo systemctl restart apache2
```
```bash
sudo apachectl configtest
sudo systemctl restart httpd
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

Aby wykonać je z powłoki w jednym kroku:

```bash
sudo -u postgres psql
```

Następnie wklej polecenia w wierszu zachęty `postgres=#` i wpisz `\q`, aby zakończyć.

!!! tip "Dobra praktyka"

    Używaj silnych, złożonych haseł dla użytkowników bazy danych. Unikaj łatwych do odgadnięcia danych uwierzytelniających.

---

### Krok 2: Rozpakuj pakiet instalacyjny digna

1. Znajdź plik ZIP instalacji digna dostarczony Ci
2. Rozpakuj go do wybranej lokalizacji instalacyjnej — na przykład `/opt/digna`
3. Po rozpakowaniu powinieneś zobaczyć następujące elementy:
   - `dashboard/` — interfejs webowy
   - `digna` — główny plik wykonywalny (backend + CLI w jednym)

!!! info "Plików konfiguracyjnych i pliku licencji nie ma w pakiecie"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nie są dostarczane z instalacją — oba
    tworzysz samodzielnie, w sekcjach [Konfiguracja backendu](#backend-configuration) i
    [Konfiguracja dashboardu](#dashboard-configuration). `license.toml` również nie jest dołączany;
    digna dostarcza go osobno, zgodnie z opisem w kroku 3.

Aby rozpakować archiwum z powłoki:

```bash
sudo mkdir -p /opt/digna
sudo unzip digna-2026.06-linux-x86_64.zip -d /opt/digna
```

!!! note "Uwaga"

    Jeśli `unzip` nie jest zainstalowany, dodaj go poleceniem `sudo apt install -y unzip` lub `sudo dnf install -y unzip`.

#### Nadaj plikowi wykonywalnemu prawo do uruchamiania

W zależności od sposobu przesłania archiwum bit wykonywalności może nie zachować się po rozpakowaniu. Ustaw go jawnie:

```bash
cd /opt/digna
sudo chmod +x digna
```

#### Utwórz konto usługi

W wdrożeniach produkcyjnych zaleca się uruchamianie backendu jako dedykowany, nieuprzywilejowany użytkownik:

```bash
sudo useradd --system --no-create-home --shell /usr/sbin/nologin digna
sudo chown -R digna:digna /opt/digna
```

!!! note "Uwaga"

    W rodzinie RHEL odpowiednia ścieżka powłoki to `/sbin/nologin`.

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
sudo mv config_template.toml config.toml
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

    Jeśli serwujesz dashboard z nginx lub Apache na domyślnym porcie HTTP, dozwolonym originem jest `http://localhost` — albo publiczny adres URL serwera, jeśli dashboard jest otwierany z innych maszyn.

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

!!! tip "Dobra praktyka"

    `config.toml` zawiera hasło do bazy danych zapisane otwartym tekstem. Ogranicz uprawnienia do pliku tak, aby mogło go odczytać wyłącznie konto usługi:

    ```bash
    sudo chown digna:digna /opt/digna/config.toml
    sudo chmod 600 /opt/digna/config.toml
    ```

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

    Aby sprawdzić liczbę rdzeni CPU dostępnych na serwerze, uruchom `nproc`.

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

1. Otwórz terminal
2. Przejdź do katalogu instalacji digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)
3. Uruchom test połączenia:

```bash
cd /opt/digna
./digna repo check
```

Powinieneś zobaczyć potwierdzenie, że połączenie zostało nawiązane (repozytorium samo w sobie nie zostało jeszcze zainicjowane).

!!! note "Uwaga"

    W systemie Linux bieżący katalog nie znajduje się w zmiennej PATH, dlatego plik wykonywalny wywołuje się jako `./digna`, a nie `digna`. Aby wszędzie używać krótszej formy, dodaj dowiązanie symboliczne:

    ```bash
    sudo ln -s /opt/digna/digna /usr/local/bin/digna
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

    Umieść hasło w pojedynczych cudzysłowach. `bash` i `zsh` traktują znaki takie jak `!`, `$` i `*` w szczególny sposób, a hasło zawierające je bez cudzysłowów nie zostanie przekazane w takiej postaci, w jakiej je wpisano.

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

    Jeśli dashboard jest serwowany z innej maszyny niż backend, otwórz również port API w zaporze sieciowej:

    ```bash
    sudo ufw allow 8082/tcp
    ```
    ```bash
    sudo firewall-cmd --permanent --add-port=8082/tcp && sudo firewall-cmd --reload
    ```

!!! note "Serwer zajmuje terminal"

    `serve` działa na pierwszym planie i pracuje, dopóki nie zatrzymasz go skrótem ++ctrl+c++. Zostaw go uruchomionego, dopóki nie dokończysz konfiguracji; aby zamiast tego uruchamiał się automatycznie przy starcie systemu, zobacz [Uruchamianie digna jako usługi systemd](#running-digna-as-a-systemd-service).

---

## Konfiguracja dashboardu {: #dashboard-configuration }

### Krok 1: Wdróż dashboard na serwerze WWW

Dashboard digna odczytuje własną konfigurację z pliku `dashboard/dashboard_config.toml`. Ten plik nie jest dostarczany z instalacją — tworzysz go w katalogu `dashboard/`, obok plików dashboardu.

Jego zawartość opisano w sekcji [Logowanie jednokrotne (SSO)](../../../sso/overview.md), bo właśnie tam ten plik jest potrzebny: zawiera opcje logowania oferowane przez dashboard oraz, w przypadku wdrożeń wieloinstancyjnych, połączenie z backendem.

Wybierz serwer WWW i postępuj zgodnie z odpowiednimi krokami wdrożeniowymi.

#### Wdrażanie w nginx

Jeśli wykonano kroki z sekcji [Konfiguracja nginx](#nginx-setup), blok server wskazuje już na folder `dashboard` i kopiowanie nie jest potrzebne.

1. **Potwierdź ścieżkę**
   - Otwórz `/etc/nginx/conf.d/digna.conf`
   - Sprawdź, czy `root` wskazuje na rozpakowany folder `dashboard`

2. **Upewnij się, że folder jest czytelny**
   ```bash
   sudo chmod -R a+rX /opt/digna/dashboard
   ```

3. **Przeładuj nginx**
   ```bash
   sudo nginx -t
   sudo systemctl reload nginx
   ```

4. **Przetestuj instalację**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost` (lub skonfigurowanego adresu URL)
   - Powinieneś zobaczyć stronę logowania dashboardu digna

#### Wdrażanie w Apache httpd

1. **Skopiuj dashboard do katalogu głównego dokumentów**
   ```bash
   sudo cp -R /opt/digna/dashboard /var/www/html/digna
   ```

2. **Dodaj reguły przepisywania**

   Utwórz plik `.htaccess` we wdrożonym folderze, aby trasy dashboardu działały po odświeżeniu przeglądarki:

   ```bash
   sudo nano /var/www/html/digna/.htaccess
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
   sudo systemctl restart apache2
   ```
   ```bash
   sudo systemctl restart httpd
   ```

4. **Otwórz dashboard**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost/digna`
   - Powinieneś zobaczyć stronę logowania dashboardu digna

### Krok 2: SELinux (tylko rodzina RHEL)

W systemach RHEL, Rocky, AlmaLinux i Fedora SELinux domyślnie działa w trybie enforcing i blokuje serwerowi WWW odczyt plików spoza oczekiwanych lokalizacji. Sprawdź, czy jest aktywny:

```bash
getenforce
```

Jeśli wynik to `Enforcing`, a dashboard jest serwowany z `/opt/digna/dashboard`, nadaj katalogowi etykietę, która pozwoli serwerowi WWW go odczytywać:

```bash
sudo semanage fcontext -a -t httpd_sys_content_t "/opt/digna/dashboard(/.*)?"
sudo restorecon -Rv /opt/digna/dashboard
```

!!! note "Uwaga"

    Jeśli polecenie `semanage` nie zostanie znalezione, zainstaluj je poleceniem `sudo dnf install -y policycoreutils-python-utils`.

!!! warning "Ważne"

    Dashboard zwracający **403 Forbidden** na świeżo skonfigurowanym serwerze RHEL niemal zawsze oznacza problem z etykietami SELinux, a nie z uprawnieniami do plików. Potwierdź to poleceniem `sudo ausearch -m avc -ts recent`.

---

## Uruchamianie digna jako usługi systemd {: #running-digna-as-a-systemd-service }

### Dlaczego uruchamiać digna jako usługę?

Uruchomienie backendu digna jako usługi systemd zapewnia, że:

- Uruchamia się automatycznie podczas startu maszyny
- Działa w tle bez otwartego okna terminala
- Automatycznie się restartuje w razie awarii
- Można nim zarządzać za pomocą `systemctl`, standardowego menedżera usług w systemie Linux

### Pliki zarządzania usługą

Wszystkie niezbędne pliki znajdują się w katalogu instalacji digna w: `bin/`

Dostępne skrypty powłoki:

- `install_service.sh` — rejestruje digna w systemd
- `uninstall_service.sh` — usuwa rejestrację usługi
- `start_service.sh` — uruchamia zarejestrowaną usługę
- `stop_service.sh` — zatrzymuje działającą usługę

!!! warning "Wymagane uprawnienia root"

    Wszystkie skrypty muszą być uruchamiane przez `sudo`, ponieważ rejestracja usługi uruchamianej przy starcie systemu zapisuje plik jednostki w `/etc/systemd/system`.

### Nadawanie skryptom prawa do uruchamiania

Rozpakowanie może nie zachować bitu wykonywalności. Przed pierwszym użyciem wykonaj:

```bash
cd /opt/digna/bin
sudo chmod +x *.sh
```

### Instalacja usługi

1. **Otwórz terminal**

2. **Przejdź do folderu bin**
   ```bash
   cd /opt/digna/bin
   ```

3. **Uruchom skrypt instalacyjny**
   ```bash
   sudo ./install_service.sh
   ```

Serwer digna jest teraz zarejestrowany w systemd z włączonym **automatycznym uruchamianiem**. Usługa nie uruchamia się od razu — zobacz następną sekcję, aby ją uruchomić.

### Uruchamianie i zatrzymywanie usługi

#### Aby uruchomić usługę

1. Otwórz terminal
2. Przejdź do `/opt/digna/bin`
3. Uruchom:
   ```bash
   sudo ./start_service.sh
   ```

#### Aby zatrzymać usługę

1. Otwórz terminal
2. Przejdź do `/opt/digna/bin`
3. Uruchom:
   ```bash
   sudo ./stop_service.sh
   ```

!!! tip "Wskazówka"

    Zawsze zatrzymuj usługę przed aktualizacją plików aplikacji.

### Zarządzanie usługą za pomocą systemctl

Po zarejestrowaniu usługą można też sterować standardowymi poleceniami systemd z dowolnego katalogu:

```bash
sudo systemctl start digna
sudo systemctl stop digna
sudo systemctl restart digna
sudo systemctl status digna
```

### Weryfikacja usługi

Aby potwierdzić, że usługa jest zarejestrowana i działa:

```bash
systemctl is-enabled digna
systemctl is-active digna
```

`enabled` oznacza, że usługa uruchamia się przy starcie systemu; `active` oznacza, że działa w tej chwili.

### Przeglądanie logów usługi

systemd przechwytuje wszystko, co backend wypisuje na konsolę. Aby to odczytać:

```bash
sudo journalctl -u digna -n 100
```

Aby śledzić log na bieżąco podczas odtwarzania problemu:

```bash
sudo journalctl -u digna -f
```

!!! tip "Wskazówka"

    To najszybszy sposób zdiagnozowania usługi, która uruchamia się i natychmiast zatrzymuje. Błąd połączenia z repozytorium lub brak pliku `license.toml` są zgłaszane właśnie tutaj.

### Przenoszenie usługi do nowego katalogu

Plik jednostki przechowuje bezwzględną ścieżkę do pliku wykonywalnego, więc przeniesienie instalacji wymaga ponownej rejestracji usługi:

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

Serwer digna jest teraz wyrejestrowany z systemd.

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

Aby utworzyć kopię zapasową z powłoki:

```bash
pg_dump -h localhost -p 5432 -U digna_user -n dignarepo postgres > digna_repo_backup.sql
```

### Proces aktualizacji

#### Krok 1: Zatrzymaj usługę digna

Jeśli digna działa jako usługa systemd, najpierw ją zatrzymaj:

```bash
cd /opt/digna/bin
sudo ./stop_service.sh
```

Jeśli digna działa na pierwszym planie, naciśnij `Ctrl + C` w jej oknie terminala.

#### Krok 2: Wykonaj kopię bieżącej instalacji

W katalogu instalacyjnym digna zmień nazwy folderów bieżącej instalacji, aby nowe wydanie mogło zostać wdrożone obok nich:

```bash
cd /opt/digna
sudo mv dignabackend dignabackend_old
```
```bash
sudo mv dignacli dignacli_old
```
```bash
sudo mv dashboard dashboard_old
```

!!! info "dignabackend i dignacli nie są już używane"

    Od wydania 2026.06 `dignabackend` i `dignacli` są zastąpione pojedynczym plikiem wykonywalnym `digna`, który łączy backend i CLI. Zachowaj `dignabackend_old` i `dignacli_old` tylko do czasu zweryfikowania aktualizacji — potem możesz usunąć oba foldery. Zachowaj `dashboard_old`, dopóki nie odtworzysz z niego swoich plików konfiguracyjnych (patrz krok 4).

#### Krok 3: Rozpakuj i wdróż nową wersję

1. Rozpakuj nowy plik ZIP instalacji digna
2. Skopiuj nowy plik wykonywalny `digna` oraz folder `dashboard` do katalogu instalacyjnego
3. Przywróć bit wykonywalności i własność konta usługi:

```bash
sudo chmod +x /opt/digna/digna
sudo chown -R digna:digna /opt/digna
```

!!! warning "Ważne"

    Ani `config.toml`, ani `dashboard/dashboard_config.toml` nigdy nie są dołączane do pliku ZIP
    instalacji — zespół digna nigdy nie dostarcza żadnego z tych plików. Aktualizacja nie narusza więc
    Twojej istniejącej konfiguracji, a kopie w folderach `*_old` o zmienionych nazwach są
    jedynymi, jakie posiadasz.

#### Krok 4: Przywróć pliki konfiguracyjne

```bash
sudo cp dashboard_old/dashboard_config.toml dashboard/dashboard_config.toml
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
a następnie przeładuj stronę z wymuszonym odświeżeniem (++ctrl+f5++).

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
sudo cp /path/to/new/license.toml /opt/digna/license.toml
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

Jeśli digna działa jako usługa systemd:

```bash
cd /opt/digna/bin
sudo ./start_service.sh
```

Jeśli uruchamiasz ręcznie, zrestartuj serwer:

```bash
cd /opt/digna
./digna serve --address <address> --port <port>
```

Jeśli korzystasz z nginx lub Apache, przeładuj odpowiedni serwer WWW:

```bash
sudo systemctl reload nginx
```
```bash
sudo systemctl restart apache2
```

W rodzinie RHEL ponownie nadaj etykiety SELinux, jeśli katalog `dashboard` został zastąpiony:

```bash
sudo restorecon -Rv /opt/digna/dashboard
```

#### Krok 10: Zweryfikuj aktualizację

1. Uzyskaj dostęp do dashboardu digna
2. Sprawdź, czy interfejs ładuje się poprawnie
3. Sprawdź logi serwera pod kątem ewentualnych błędów
4. Przestaw na ODBC każde połączenie, które jeszcze z niego nie korzystało, a następnie przetestuj wszystkie połączenia
   — zobacz [Testowanie połączenia](../../../databases/overview.md#testing-a-connection):

```bash
sudo journalctl -u digna -n 100
```
