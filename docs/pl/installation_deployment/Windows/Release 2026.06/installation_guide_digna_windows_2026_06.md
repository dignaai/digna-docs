---
title: Przewodnik instalacji na Windows – digna Release 2026.06 | digna Documentation
description: Przewodnik krok po kroku instalacji digna Release 2026.06 na Windows — wymagania systemowe, konfiguracja PostgreSQL, konfiguracja serwera WWW, konfiguracja backendu i dashboardu, uruchamianie digna jako usługi Windows oraz aktualizacja do nowego wydania.
keywords: digna windows installation, digna deployment guide, digna backend setup, digna dashboard installation, postgresql setup, digna windows service, digna upgrade guide
image: /assets/logo_square.png
---

# Windows Installation Guide for digna Release 2026.06

**Wydanie:** 2026.06

**Ostatnia aktualizacja:** 30 sierpnia 2026


---

## Table of Contents

1. [Introduction](#introduction)
2. [System Requirements](#system-requirements)
3. [Pre-Installation Setup](#pre-installation-setup)
4. [PostgreSQL Server Setup](#postgresql-server-setup)
5. [Web Server Configuration](#web-server-configuration)
6. [Initial Installation](#initial-installation)
7. [Backend Configuration](#backend-configuration)
8. [Dashboard Configuration](#dashboard-configuration)
9. [Running digna as a Windows Service](#running-digna-as-a-windows-service)
10. [Upgrading to a New Release](#upgrading-to-a-new-release)

---

## Introduction {: #introduction }

### O digna

digna to kompleksowa platforma napędzana AI, zaprojektowana w celu optymalizacji zarządzania jakością danych w różnych środowiskach danych, takich jak magazyny danych, data lake i lakehouse. Zbudowana tak, aby była wysoko skalowalna i elastyczna, digna rozwiązuje współczesne wyzwania związane z danymi poprzez automatyzację, monitorowanie w czasie rzeczywistym oraz wykrywanie anomalii.

digna składa się z dwóch głównych komponentów:

- **dignabackend**: rdzeń aplikacji, odpowiedzialny za przetwarzanie danych i wykonywanie kontroli jakości.
- **dignadashboard**: interfejs webowy hostowany na serwerze WWW, zapewniający przyjazny sposób interakcji z platformą digna i wizualizację metryk jakości danych.

### Co nowego w wydaniu 2026.06

To wydanie wprowadza możliwości obserwowalności danych bezpośrednio w Twoim kodzie, umożliwiając deweloperom monitorowanie jakości danych u źródła. Pełne informacje znajdziesz w [release notes](http://docs.digna.ai/changelog/Release_202606/).

---

## System Requirements {: #system-requirements }

Zanim rozpoczniesz instalację, upewnij się, że Twój system spełnia poniższe minimalne wymagania:

| Requirement | Specification |
|---|---|
| **Operating System** | Windows Server lub Windows 10/11 |
| **Memory (Minimal Setup)** | 16 GB RAM |
| **Disk Space** | 10 GB dostępnego miejsca |
| **Database** | PostgreSQL Server 12 lub nowszy |
| **Web Server** | IIS, Apache Tomcat lub równoważny |

### Opcje instalacji bazy danych

**Jeśli PostgreSQL jest już zainstalowany:**
Możesz dodać nową bazę danych dla digna do istniejącego serwera PostgreSQL.

**Jeśli instalujesz PostgreSQL na tej samej maszynie co digna:**

!!! info "Zalecane specyfikacje"

    - **Pamięć**: 32 GB RAM (zamiast 16 GB)
    - **Miejsce na dysku**: 50 GB dostępnego miejsca (zamiast 10 GB)

    Te wyższe specyfikacje uwzględniają równoczesne działanie digna oraz serwera PostgreSQL.

---

## Pre-Installation Setup {: #pre-installation-setup }

Przed instalacją digna upewnij się, że są spełnione dwa kluczowe wymagania wstępne:

1. **PostgreSQL Server** – do przechowywania obliczonych metryk i danych o wydajności
2. **Web Server** – do hostowania digna Dashboard

Jeżeli te komponenty nie są jeszcze skonfigurowane, postępuj zgodnie z poniższymi sekcjami, aby je zainstalować i skonfigurować.

---

## PostgreSQL Server Setup {: #postgresql-server-setup }

### Jeśli masz już PostgreSQL

Jeśli PostgreSQL jest już zainstalowany i działa na Twojej lokalnej maszynie lub jeśli korzystasz z zarządzanego, zdalnego serwera PostgreSQL, możesz przejść do [następnej sekcji](#web-server-configuration).

### Instalacja PostgreSQL

Wykonaj poniższe kroki, aby zainstalować PostgreSQL na Windows:

#### Krok 1: Pobierz PostgreSQL

1. Odwiedź stronę [PostgreSQL Downloads page](https://www.postgresql.org/download/)
2. Wybierz **Windows**
3. Pobierz najnowszy instalator

#### Krok 2: Uruchom instalator

1. Kliknij dwukrotnie pobrany plik instalatora
2. Postępuj zgodnie z instrukcjami kreatora instalacji

#### Krok 3: Wybierz katalog instalacji

Wskaż katalog, w którym PostgreSQL ma być zainstalowany. Domyślna lokalizacja zazwyczaj jest odpowiednia.

#### Krok 4: Wybierz komponenty

Dla standardowej instalacji pozostaw domyślne opcje komponentów.

#### Krok 5: Ustaw hasło superużytkownika PostgreSQL

Wprowadź i potwierdź hasło dla superużytkownika PostgreSQL (`postgres`). **Zapisz to hasło w bezpiecznym miejscu** — będzie potrzebne później.

#### Krok 6: Skonfiguruj numer portu

Domyślny port PostgreSQL to `5432`. Możesz użyć domyślnego lub wskazać inny port, jeśli zajdzie taka potrzeba.

!!! tip "Wskazówka"

    Jeśli port 5432 jest już zajęty, wybierz alternatywny port i zapamiętaj go do późniejszej konfiguracji.

#### Krok 7: Wybierz locale

Wybierz locale dla swojej bazy danych. Domyślne ustawienie zazwyczaj jest odpowiednie.

#### Krok 8: Zakończ instalację

Klikaj **Dalej** przez pozostałe kroki, a następnie kliknij **Zakończ**.

#### Krok 9: Zweryfikuj instalację

Otwórz Wiersz poleceń i sprawdź, czy PostgreSQL został poprawnie zainstalowany:

```bash
psql --version
```

Powinieneś zobaczyć wersję PostgreSQL, jeśli instalacja zakończyła się pomyślnie.

---

## Web Server Configuration {: #web-server-configuration }

digna wymaga serwera WWW do hostowania dashboardu. Wybierz jedną z poniższych opcji:

- [Internet Information Services (IIS)](#iis-setup)
- [Apache Tomcat](#apache-tomcat-setup)

Musisz zainstalować i skonfigurować tylko **jeden** z tych serwerów.

### IIS Setup {: #iis-setup }

#### Przegląd

Internet Information Services (IIS) to serwer WWW Microsoftu do hostowania stron i aplikacji webowych.

#### Włączenie IIS

1. **Otwórz Panel sterowania**
   - Naciśnij `Win + R`
   - Wpisz `control` i naciśnij Enter

2. **Przejdź do funkcji systemu Windows**
   - Kliknij **Programy**
   - Wybierz **Włącz lub wyłącz funkcje systemu Windows**

3. **Włącz Internet Information Services**
   - Przewiń i znajdź **Internet Information Services (IIS)**
   - Zaznacz pole wyboru, aby je włączyć
   - Kliknij **+**, aby rozwinąć i upewnić się, że zaznaczone są te podkomponenty:
     - **Web Management Tools**
     - **World Wide Web Services**

4. **Kliknij OK**, aby zastosować zmiany

5. **Zweryfikuj instalację IIS**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost`
   - Powinieneś zobaczyć stronę powitalną IIS

#### Wymagane: URL Rewrite Module

IIS wymaga komponentu URL Rewrite. Pobierz i zainstaluj go ze [strony Microsoft](https://www.iis.net/downloads/microsoft/url-rewrite).

#### Wymagane: Typ MIME dla plików Markdown

Aby upewnić się, że pliki Markdown (`.md`) będą serwowane poprawnie przez IIS:

1. Otwórz **IIS Manager** (naciśnij `Win + R`, wpisz `inetmgr`, naciśnij Enter)
2. Przejdź do **Twoja Strona > MIME Types**
3. Kliknij **Add...**
4. Skonfiguruj:
   - **Rozszerzenie pliku**: `.md`
   - **Typ MIME**: `text/markdown`

!!! warning "Ważne"

    Bez tego ustawienia pliki `.md` mogą nie być serwowane poprawnie.

---

### Apache Tomcat Setup {: #apache-tomcat-setup }

#### Przegląd

Apache Tomcat to open-source’owy kontener servletów Java i serwer WWW.

#### Instalacja

1. **Pobierz Apache Tomcat**
   - Odwiedź [Apache Tomcat Downloads](https://tomcat.apache.org/download-90.cgi)
   - Pobierz dystrybucję ZIP dla Windows

2. **Wypakuj archiwum**
   - Wypakuj plik ZIP do katalogu na swoim systemie
   - Przykład: `C:\Program Files\Apache Tomcat`

3. **Zweryfikuj działanie Tomcata**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost:8080`
   - Powinieneś zobaczyć stronę powitalną Apache Tomcat

!!! tip "Wskazówka"

    Apache Tomcat zwykle uruchamia się automatycznie po instalacji. Jeśli tak się nie stanie, przejdź do folderu `bin` i uruchom `startup.bat`.

---

## Initial Installation {: #initial-installation }

### Krok 1: Utwórz repozytorium digna

Repozytorium digna przechowuje wszystkie metryki obliczone przez digna. Pełni rolę centralnej bazy danych dla danych analitycznych i wydajnościowych.

#### Utwórz schemat repozytorium i użytkownika

Otwórz klienta PostgreSQL (pgAdmin, psql lub inny) i wykonaj następujące polecenia SQL:

```sql
CREATE SCHEMA <digna_repo_schema>;

CREATE USER <digna_repo_user> WITH PASSWORD '<digna_repo_password>';

GRANT ALL PRIVILEGES ON SCHEMA <digna_repo_schema> TO <digna_repo_user>;
```

**Zastąp poniższe symbole zastępcze:**

- `<digna_repo_schema>` — Nazwa schematu (np. `dignarepo`)
- `<digna_repo_user>` — Nazwa użytkownika (np. `digna_user`)
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

### Krok 2: Wypakuj pakiet instalacyjny digna

1. Znajdź plik ZIP instalacji digna otrzymany od dostawcy
2. Wypakuj go do wybranego katalogu instalacyjnego
3. Po rozpakowaniu powinieneś zobaczyć następujące elementy:
   - `dashboard/` — interfejs webowy dashboardu
   - `digna` — główny plik wykonywalny (backend + CLI w jednym)
   - `config.toml` — plik konfiguracyjny
   - `license.toml` — plik licencyjny (skopiuj tutaj swój plik)

### Krok 3: Zainstaluj plik licencji

!!! warning "Ważne"

    Plik licencji **nie** jest dołączony do pakietu instalacyjnego i zostanie dostarczony oddzielnie przez digna.

1. Znajdź plik `license.toml` przekazany Ci przez dostawcę
2. Skopiuj go do głównego katalogu instalacyjnego digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)

**Dlaczego to ważne:**
Plik licencji zawiera informacje o kliencie, datę wygaśnięcia licencji oraz podpis cyfrowy. **Nie modyfikuj tego pliku** — każda zmiana unieważni licencję.

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

## Backend Configuration {: #backend-configuration }

### Krok 1: Utwórz i edytuj plik konfiguracyjny

Plik `config_template.toml` jest dostarczony w katalogu instalacyjnym digna. Wystarczy, że zmienisz jego nazwę na `config.toml`.

**Lokalizacja:** `digna_installation/config.toml`

Otwórz `config.toml` w edytorze tekstu i skonfiguruj każdą sekcję poniżej.

#### Sekcja [app]

Ta sekcja konfiguruje ustawienia aplikacji backend:

```toml
[app]
digna_APP_HOST = "localhost"
digna_APP_PORT = 8082
digna_APP_CORS_ALLOW_ORIGINS = ["http://localhost:5173"]
digna_APP_CORS_ALLOW_CREDENTIALS = true
digna_APP_CORS_ALLOW_METHODS = ["*"]
digna_APP_CORS_ALLOW_HEADERS = ["*"]
```

| Parameter | Wartość | Uwagi |
|---|---|---|
| `digna_APP_HOST` | `localhost` lub adres IP | Host lub adres IP, na którym hostowany jest dignabackend |
| `digna_APP_PORT` | `8082` (domyślnie) | Port dla endpointów REST API |
| `digna_APP_CORS_ALLOW_ORIGINS` | URL frontendu | Jeśli dashboard jest na innym serwerze, dodaj jego URL |
| `digna_APP_CORS_ALLOW_CREDENTIALS` | `true` | Wymagane dla CORS z poświadczeniami |
| `digna_APP_CORS_ALLOW_METHODS` | `["*"]` | Zezwól na wszystkie metody HTTP |
| `digna_APP_CORS_ALLOW_HEADERS` | `["*"]` | Zezwól na wszystkie nagłówki |

#### Sekcja [repo]

Ta sekcja konfiguruje połączenie z bazą PostgreSQL:

```toml
[repo]
digna_REPO_HOST = "localhost"
digna_REPO_PORT = 5432
digna_REPO_DB = "postgres"
digna_REPO_SCHEMA = "dignarepo"
digna_REPO_USER = "digna_user"
digna_REPO_PASSWORD = "YourSecurePassword123!"
```

| Parameter | Wartość | Uwagi |
|---|---|---|
| `digna_REPO_HOST` | `localhost` lub adres IP | Hostlub adres IP serwera PostgreSQL |
| `digna_REPO_PORT` | `5432` (domyślnie) | Port PostgreSQL |
| `digna_REPO_DB` | `postgres` | Nazwa bazy danych |
| `digna_REPO_SCHEMA` | `dignarepo` | Schemat utworzony wcześniej |
| `digna_REPO_USER` | `digna_user` | Użytkownik utworzony w konfiguracji PostgreSQL |
| `digna_REPO_PASSWORD` | Twoje hasło | Hasło ustawione podczas tworzenia użytkownika |

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

| Parameter | Wartość | Uwagi |
|---|---|---|
| `digna_FERNET_KEY` | Klucz szyfrujący | Używany do szyfrowania tokenów i ciasteczek (domyślny dostarczony) |
| `digna_COOKIE_DOMAIN` | `localhost` | Dopasuj do domeny frontendu |
| `digna_COOKIE_SECURE` | `false` (lokalnie) / `true` (produkcyjnie) | Ustaw `true` dla połączeń HTTPS |
| `digna_COOKIE_HTTPONLY` | `true` | Zawsze włączone dla bezpieczeństwa |
| `digna_COOKIE_SAME_SITE` | `lax` | Zapobiega atakom CSRF |
| `digna_TOKEN_EXPIRES_IN` | `86400` (24 godziny) | Czas życia sesji w sekundach |
| `digna_MAX_WORKERS` | Liczba rdzeni CPU - 1 | Liczba równoległych zadań inspekcji |

#### Sekcja [logging]

Ta sekcja konfiguruje zachowanie logowania:

```toml
[logging]
digna_LOGGING_MODE = "INFO"
digna_LOGGING_BACKUP_COUNT = 10
```

| Parameter | Wartość | Uwagi |
|---|---|---|
| `digna_LOGGING_MODE` | `INFO` lub `DEBUG` | `INFO` dla produkcji, `DEBUG` dla rozwiązywania problemów |
| `digna_LOGGING_BACKUP_COUNT` | `10` | Liczba codziennych kopii logów do zachowania |

---

### Krok 3: Przetestuj połączenie z repozytorium

1. Otwórz Wiersz poleceń
2. Przejdź do katalogu instalacyjnego digna (tam, gdzie znajdują się `config.toml` i plik wykonywalny `digna`)
3. Uruchom test połączenia:

```bash
digna repo check
```

Powinieneś zobaczyć potwierdzenie, że połączenie zostało nawiązane (repozytorium jako takie nie zostało jeszcze zainicjowane).

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
- `--address` — Nazwa hosta / adres IP serwera
- `--port` — Port serwera

Powinieneś zobaczyć komunikaty startowe potwierdzające uruchomienie serwera:

```
INFO:     Started server process [1234]
INFO:     Waiting for application startup.
INFO:     Application startup complete
INFO:     Uvicorn running on http://localhost:8082
```

### Krok 6: Utwórz użytkownika administratora

1. Otwórz **nowe** okno Wiersza poleceń
2. Przejdź do katalogu instalacyjnego digna
3. Uruchom następujące polecenie, aby utworzyć użytkownika administratorskiego:

```bash
digna user add <username> "<full_name>" <password> --su
```

**Przykład:**

```bash
digna user add "Admin User" AdminPassword123! --su
```

To utworzy użytkownika z pełnymi uprawnieniami administracyjnymi.

!!! tip "Dobra praktyka"

    Używaj silnego hasła z kombinacją wielkich liter, małych liter, cyfr i znaków specjalnych.

---

## Dashboard Configuration {: #dashboard-configuration }

### Krok 1: Wdróż dashboard na serwerze WWW

Dashboard digna ma własny, oddzielny plik `config.toml` znajdujący się w katalogu `dashboard/`. Ta konfiguracja jest już dostarczona i nie wymaga zmian podczas instalacji początkowej. Należy ją zmodyfikować tylko wtedy, gdy trzeba dostosować połączenie z backendem.

Jeśli musisz zmodyfikować konfigurację dashboardu (np. dla środowisk z wieloma instancjami), odnieś się do dokumentacji dashboardu.

Wybierz serwer WWW i postępuj zgodnie z odpowiednimi krokami wdrożeniowymi.

#### Wdrażanie na IIS

1. **Otwórz IIS Manager**
   - Naciśnij `Win + R`, wpisz `inetmgr`, naciśnij Enter

2. **Utwórz nową witrynę**
   - W panelu po lewej kliknij prawym przyciskiem myszy **Sites**
   - Wybierz **Add Website...**

3. **Skonfiguruj witrynę**
   - **Site Name**: Wpisz nazwę (np. "dignaDashboard")
   - **Physical Path**: Kliknij Browse i wybierz folder `dashboard`
   - **Binding**: Ustaw adres IP i port (domyślny port 80 dla HTTP, 443 dla HTTPS)

4. **Uruchom witrynę**
   - Kliknij **OK** aby utworzyć witrynę
   - Kliknij prawym przyciskiem nową witrynę i wybierz **Start**

5. **Przetestuj instalację**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost` (lub skonfigurowanego URL)
   - Powinieneś zobaczyć stronę logowania dashboardu digna

#### Wdrażanie na Apache Tomcat

1. **Skopiuj dashboard do Tomcata**
   - Skopiuj folder `dashboard` do katalogu `webapps` Tomcata
   - Zmień nazwę jeśli potrzeba (np. na `digna`)
   - Przykład: `C:\Program Files\Apache Tomcat\webapps\digna`

2. **Zweryfikuj wdrożenie**
   - Odśwież lub przeładuj stronę zarządzania Tomcatem (http://localhost:8080)
   - Powinieneś zobaczyć "digna" (lub wybraną nazwę) na liście wdrożonych aplikacji

3. **Uzyskaj dostęp do dashboardu**
   - Otwórz przeglądarkę
   - Przejdź do `http://localhost:8080/digna`
   - Powinieneś zobaczyć stronę logowania dashboardu digna

---

## Running digna as a Windows Service {: #running-digna-as-a-windows-service }

### Dlaczego warto uruchamiać jako usługę Windows?

Uruchamianie backendu digna jako usługi Windows zapewnia, że:
- Uruchamia się automatycznie przy starcie systemu
- Działa w tle bez otwartego okna Wiersza poleceń
- Automatycznie się restartuje po awarii
- Może być zarządzana przez narzędzie Usługi Windows

### Pliki do zarządzania usługą

Wszystkie niezbędne pliki znajdują się w katalogu instalacyjnym digna w: `bin/`

Dostępne pliki wsadowe:
- `install_service.bat` — rejestruje digna jako usługę Windows
- `uninstall_service.bat` — usuwa rejestrację usługi
- `start_service.bat` — uruchamia zarejestrowaną usługę
- `stop_service.bat` — zatrzymuje uruchomioną usługę

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

Serwer digna jest teraz zarejestrowany jako usługa Windows z ustawionym **automatycznym uruchamianiem**. Usługa nie uruchamia się od razu — zobacz następną sekcję, aby ją uruchomić.

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

    Zawsze zatrzymaj usługę przed aktualizacją plików aplikacji.

### Przenoszenie usługi do nowego katalogu

Jeśli musisz przenieść instalację digna:

1. **Odinstaluj bieżącą usługę**
   ```bash
   cd C:\old\path\digna\bin
   uninstall_service.bat
   ```

2. **Przenieś pliki aplikacji**
   - Przenieś cały katalog instalacyjny digna do nowej lokalizacji

3. **Zainstaluj ponownie usługę**
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

Serwer digna został teraz odrejestrowany jako usługa Windows.

---

## Upgrading to a New Release {: #upgrading-to-a-new-release }

### Przed aktualizacją

**Utworzenie kopii zapasowej repozytorium digna jest obowiązkowe**

Przed aktualizacją digna wykonaj kopię zapasową repozytorium (PostgreSQL), aby zabezpieczyć się przed utratą danych.
Kopia zapasowa pozwala na odzyskanie stanu w przypadku problemów podczas aktualizacji.

### Proces aktualizacji

#### Krok 1: Zatrzymaj usługę digna

Jeśli digna działa jako usługa Windows, najpierw ją zatrzymaj:

```bash
cd C:\path\to\digna\bin
stop_service.bat
```

#### Krok 2: Zrób kopię aktualnej instalacji backendu

W katalogu instalacyjnym digna:

```bash
# Zmień nazwę folderu zawierającego dignabackend
ren dignabackend dignabackend_old
```
```bash
# Zmień nazwę dashboardu
ren dashboard dashboard_old
```

#### Krok 3: Wypakuj i wdroż nową wersję

1. Wypakuj nowy plik ZIP instalacji digna
2. Skopiuj nowy plik wykonywalny `digna` oraz folder `dashboard` do katalogu instalacyjnego


!!! warning "Ważne"

    Plik `config.toml` **nigdy** nie jest dołączany do pliku ZIP instalacji. Twoja istniejąca konfiguracja pozostaje nienaruszona.

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

### Krok 6: Uruchom usługi ponownie

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

Jeśli używasz IIS lub Tomcata, zrestartuj odpowiedni serwer WWW.

#### Krok 7: Zweryfikuj aktualizację

1. Uzyskaj dostęp do dashboardu digna
2. Sprawdź, czy interfejs ładuje się poprawnie
3. Sprawdź logi serwera pod kątem błędów