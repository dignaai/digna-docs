# Referencja CLI digna 2026.06
**2026-09-05**

Ta strona dokumentuje pełny zestaw poleceń dostępnych w wydaniu **2026.06** CLI ***digna***, wraz z przykładami użycia i opcjami.

Plik wykonywalny nazywa się `digna`.

---

## Podstawy CLI

---

### Przegląd i składnia

CLI wydania **2026.06** korzysta z uporządkowanej, opartej na kategoriach hierarchii poleceń:

```bash
digna [GLOBAL_OPTIONS] <COMMAND_CATEGORY> <SUBCOMMAND> [OPTIONS] [ARGUMENTS]
```

`version` i `serve` to pojedyncze polecenia bez podpolecenia:

```bash
digna [GLOBAL_OPTIONS] <COMMAND> [OPTIONS] [ARGUMENTS]
```

### Opcje globalne

Poniższe opcje globalne obowiązują we wszystkich poleceniach:

- `--help`, `-h`: Wyświetla informacje pomocy dotyczące CLI albo konkretnej kategorii poleceń lub podpolecenia.
- `--stacktrace`: W razie błędu wyświetla pełny łańcuch błędów zamiast samego komunikatu najwyższego poziomu.

`--stacktrace` jest opcją globalną w ścisłym sensie: należy ją podać **przed** kategorią polecenia, a nie po niej.

```bash
digna --stacktrace repo check     # correct
digna repo check --stacktrace     # rejected: unknown argument
```

Nie ma flagi `--version`. Zamiast niej użyj polecenia [`version`](#version).

### Wymagania wstępne

Większość poleceń wymaga czytelnego, poprawnego pliku `config.toml`; niektóre dodatkowo wymagają ważnej licencji.
Poniższa tabela pokazuje, co każda kategoria poleceń wczytuje, zanim cokolwiek zrobi:

| Kategoria poleceń | Wymaga `config.toml` | Wymaga ważnej licencji |
|---|---|---|
| `version` | nie | nie |
| `config check` | nie (to właśnie jest to, co polecenie sprawdza) | nie |
| `license check` | nie | to *jest* ta kontrola |
| `crypt` | tak | nie |
| `serve` | tak | nie |
| `project` | tak | nie |
| `user` | tak | tak |
| `inspection` | tak | tak |
| `repo` | tak | tak |

Tam, gdzie licencja jest wymagana, sprawdzane są zarówno jej podpis, jak i data wygaśnięcia, a polecenie przerywa działanie, zanim dotknie repozytorium, jeśli którakolwiek z tych kontroli się nie powiedzie.

### Kody wyjścia

- `0`: polecenie zakończyło się powodzeniem.
- `1`: polecenie się nie powiodło. Komunikat o błędzie jest zapisywany na stderr, poprzedzony prefiksem `Error: `.

### help

Opcja `--help` udostępnia informacje o dostępnych kategoriach poleceń, podpoleceniach i opcjach:

1. **Wyświetlanie pomocy ogólnej:**
   ```bash
   digna --help
   ```

2. **Uzyskiwanie pomocy dla konkretnych kategorii i poleceń:**
   ```bash
   digna user --help
   digna user add --help
   ```

   **Wyjście zawiera:**
   - **Opis polecenia:** Podsumowanie przeznaczenia polecenia.
   - **Składnię:** Argumenty wymagane i opcjonalne.
   - **Opcje:** Flagi i parametry właściwe dla danego polecenia.

### version

Polecenie `version` wypisuje zainstalowane wydanie ***digna***. Nie wczytuje żadnej konfiguracji ani nie weryfikuje licencji, więc działa również w instalacji, w której `config.toml` lub licencja są nieobecne albo nieprawidłowe.

Wersja wydania jest niezależna od wersji schematu repozytorium raportowanej przez [`repo check`](#repo-check).

#### Użycie polecenia
```bash
digna version
```

#### Przykładowe wyjście
```text
2026.06
```

---

## Zarządzanie konfiguracją

---

### config check

Polecenie `config check` weryfikuje plik konfiguracyjny (`config.toml`), sprawdzając, czy wszystkie obowiązkowe sekcje i ustawienia są obecne i poprawnie sformatowane. Każda sekcja jest weryfikowana osobno, dzięki czemu uszkodzona sekcja `[app]` nie przesłania stanu sekcji `[repo]`.

Raportowane są następujące sekcje:

- `App config` (`[app]`)
- `Repository config` (`[repo]`)
- `Base config` (`[base]`)
- `Logging config` (`[logging]`)
- `Encryption config` (`[encryption]`)
- `OIDC config(s)` (`oidc_clients`) — opcjonalna; brak klucza przechodzi kontrolę, obecna, lecz niepoprawnie zbudowana lista jej nie przechodzi

Polecenie celowo nie wczytuje konfiguracji aplikacji w taki sposób, jak robią to pozostałe polecenia, aby móc zdiagnozować plik `config.toml`, który w ogóle uniemożliwiłby uruchomienie ***digna***.

#### Użycie polecenia
```bash
digna config check [OPTIONS]
```

#### Opcje
- `--configpath`, `-c`: Ścieżka do pliku konfiguracyjnego lub do katalogu zawierającego `config.toml` (domyślnie `./config.toml`).
- `--json`: Wypisuje raport weryfikacji w formacie JSON. Ma pierwszeństwo przed `--quiet`.
- `--quiet`, `-q`: Pomija raport i opiera się wyłącznie na kodzie wyjścia.

#### Przykład
```bash
digna config check
```

Weryfikacja konkretnego pliku konfiguracyjnego z wyjściem w formacie JSON:
```bash
digna config check --configpath /etc/digna/config.toml --json
```

#### Przykładowe wyjście
```text
Configuration validation report (source: config.toml):
 - App config: OK
 - Repository config: OK
 - Base config: OK
 - Logging config: OK
 - Encryption config: FAILED
    missing field `aes_gcm_key`
 - OIDC config(s): OK

Overall: FAILED
```

Brakujący plik lub błąd składni TOML nie pozostawia niczego, co można by weryfikować sekcja po sekcji, i jest zgłaszany jako pojedynczy błąd zamiast raportu, niezależnie od `--quiet` czy `--json`.

---

## Zarządzanie repozytorium

---

### repo check

Polecenie `repo check` testuje połączenie z bazą danych oraz weryfikuje instalację i wersję repozytorium. Kończy się niepowodzeniem, jeśli skonfigurowany schemat nie istnieje albo istnieje, lecz nie zawiera repozytorium ***digna***.

Raportowana wersja to wersja schematu repozytorium, która jest wersjonowana niezależnie od wydania ***digna*** wypisywanego przez [`version`](#version).

#### Użycie polecenia
```bash
digna repo check
```

#### Przykładowe wyjście
```text
Repo version 3.0.0 installed
```

### repo install

Polecenie `repo install` instaluje nowe repozytorium ***digna*** w schemacie skonfigurowanym w `config.toml`, tworząc wszystkie wymagane sekwencje, tabele, indeksy, ograniczenia i rekordy początkowe.

Sam schemat **nie** jest tworzony przez to polecenie — musi istnieć wcześniej. Polecenie odmawia też działania, jeśli w tym schemacie zainstalowano już repozytorium, i wskazuje na [`repo upgrade`](#repo-upgrade), jeśli zainstalowana wersja jest starsza.

#### Użycie polecenia
```bash
digna repo install
```

#### Przykładowe wyjście
```text
Installing repo version 3.0.0
✅ Sequences created.
✅ Tables and Indices created.
✅ Constraints created.
✅ Records inserted.
✅ Repo version 3.0.0 successfully installed.
```

### repo upgrade

Polecenie `repo upgrade` stosuje migracje schematu bazy danych, aby doprowadzić istniejące repozytorium do wersji oczekiwanej przez zainstalowane wydanie. Aktualizacje są stosowane po jednym skoku wersji naraz wzdłuż ustalonej ścieżki aktualizacji, a każdy ukończony skok jest zapisywany w repozytorium.

Jeśli repozytorium jest już w oczekiwanej wersji, polecenie zgłasza, że aktualizacja nie jest potrzebna, i nie wprowadza żadnych zmian.

#### Użycie polecenia
```bash
digna repo upgrade
```

#### Przykładowe wyjście
```text
Upgrading from 2.3.1 to 2.3.2...
Upgrading from 2.3.2 to 3.0.0...
✅ Repo successfully upgraded to version 3.0.0.
```

---

## Zarządzanie szyfrowaniem

---

### crypt gen-key

Polecenie `crypt gen-key` generuje nowy klucz szyfrujący AES-GCM, przeznaczony do użycia jako klucz szyfrowania w `config.toml`. Musi już istnieć możliwy do wczytania plik `config.toml`, mimo że wygenerowany klucz od niego nie zależy.

#### Użycie polecenia
```bash
digna crypt gen-key
```

#### Przykładowe wyjście
```text
Encryption key: <base64-encoded key>
```

### crypt encrypt

Polecenie `crypt encrypt` szyfruje ciąg znaków (na przykład hasło do bazy danych) przy użyciu klucza AES-GCM skonfigurowanego w `config.toml` i wypisuje szyfrogram.

#### Użycie polecenia
```bash
digna crypt encrypt <VALUE>
```

#### Argumenty
- **VALUE**: Jawny ciąg znaków do zaszyfrowania (wymagany).

#### Przykład
```bash
digna crypt encrypt mysecretpassword
```

### crypt decrypt

Polecenie `crypt decrypt` odszyfrowuje ciąg znaków zaszyfrowany algorytmem AES-GCM przy użyciu klucza skonfigurowanego w `config.toml` i wypisuje tekst jawny.

#### Użycie polecenia
```bash
digna crypt decrypt <VALUE>
```

#### Argumenty
- **VALUE**: Zaszyfrowany ciąg znaków do odszyfrowania (wymagany).

#### Przykład
```bash
digna crypt decrypt "encrypted_string_here"
```

---

## Zarządzanie użytkownikami

---

### user add

Polecenie `user add` tworzy nowe konto użytkownika w repozytorium ***digna***. Polecenie kończy się niepowodzeniem, jeśli użytkownik o podanym adresie e-mail już istnieje.

#### Użycie polecenia
```bash
digna user add <EMAIL> <PASSWORD> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenty
- **EMAIL**: Adres e-mail użytkownika (wymagany).
- **PASSWORD**: Początkowe hasło użytkownika (wymagane).
- **DISPLAY_NAME**: Pełna nazwa wyświetlana użytkownika (wymagana).

#### Opcje
- `--admin`, `-a`: Tworzy użytkownika z uprawnieniami administratora (superużytkownika).

#### Przykład
```bash
digna user add jdoe@example.com "SecurePass123!" "John Doe"
```

Aby utworzyć konto administratora:
```bash
digna user add admin@example.com "AdminPass123!" "Admin User" --admin
```

#### Przykładowe wyjście
```text
User created with ID: 42
```

### user list

Polecenie `user list` wyświetla wszystkich zarejestrowanych użytkowników w formie tabeli, z identyfikatorem, adresem e-mail, nazwą wyświetlaną i flagą administratora.

#### Użycie polecenia
```bash
digna user list
```

#### Przykładowe wyjście
```text
ID                   EMAIL                          DISPLAY NAME                   ADMIN
-----------------------------------------------------------------------------------------------
42                   jdoe@example.com               John Doe                       false
43                   admin@example.com              Admin User                     true
```

### user modify

Polecenie `user modify` aktualizuje nazwę wyświetlaną i uprawnienia administratora istniejącego konta użytkownika, wskazanego adresem e-mail.

Zarówno nazwa wyświetlana, jak i flaga administratora są zapisywane za każdym razem. `--admin` jest przełącznikiem, a nie wartością: **jej pominięcie odbiera uprawnienia administratora**, dlatego podawaj ją zawsze, gdy użytkownik ma je zachować lub uzyskać.

#### Użycie polecenia
```bash
digna user modify <EMAIL> <DISPLAY_NAME> [OPTIONS]
```

#### Argumenty
- **EMAIL**: Adres e-mail modyfikowanego użytkownika (wymagany).
- **DISPLAY_NAME**: Zaktualizowana nazwa wyświetlana (wymagana).

#### Opcje
- `--admin`, `-a`: Nadaje uprawnienia administratora. Pomiń, aby je odebrać.
- `--valid-until`, `-v`: Akceptowana ze względu na zgodność, ale **obecnie nieuwzględniana**. Jej podanie powoduje wypisanie ostrzeżenia i niczego nie zmienia.

#### Przykład
```bash
digna user modify jdoe@example.com "Johnathan Doe" --admin
```

#### Przykładowe wyjście
```text
User jdoe@example.com modified successfully
```

### user modify-pwd

Polecenie `user modify-pwd` aktualizuje hasło istniejącego konta użytkownika.

#### Użycie polecenia
```bash
digna user modify-pwd <EMAIL> <PASSWORD>
```

#### Argumenty
- **EMAIL**: Adres e-mail użytkownika, którego hasło ma zostać zaktualizowane (wymagany).
- **PASSWORD**: Nowe hasło (wymagane).

#### Przykład
```bash
digna user modify-pwd jdoe@example.com "NewSecurePass456!"
```

### user delete

Polecenie `user delete` usuwa konto użytkownika z systemu.

#### Użycie polecenia
```bash
digna user delete <EMAIL>
```

#### Argumenty
- **EMAIL**: Adres e-mail użytkownika do usunięcia (wymagany).

#### Przykład
```bash
digna user delete jdoe@example.com
```

---

## Zarządzanie projektami i źródłami danych

---

### project list

Polecenie `project list` wyświetla wszystkie dostępne projekty w repozytorium wraz z ich identyfikatorem, nazwą i opisem.

#### Użycie polecenia
```bash
digna project list
```

#### Przykładowe wyjście
```text
ID                   NAME                           DESCRIPTION
------------------------------------------------------------------------------------------------------
7                    ProjectA                       Sales data quality
8                    ProjectB                       Finance data quality
```

### project list-ds

Polecenie `project list-ds` wyświetla wszystkie źródła danych powiązane z danym projektem, pokazując ich identyfikator, nazwę, rodzaj, schemat i nazwę tabeli.

#### Użycie polecenia
```bash
digna project list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, którego źródła danych mają zostać wyświetlone (wymagana). Nazwa musi być dokładnie zgodna.

#### Przykład
```bash
digna project list-ds ProjectA
```

#### Przykładowe wyjście
```text
ID                   NAME                           KIND            SCHEMA               TABLE
-------------------------------------------------------------------------------------------------------------
101                  orders                         Table           sales                orders
102                  customers                      Table           sales                customers
```

### project export-ds

Polecenie `project export-ds` eksportuje źródła danych z projektu do dokumentu JSON.

Jeśli nie podano ani `--table-name`, ani `--table-id`, eksportowane są wszystkie źródła danych projektu.

#### Użycie polecenia
```bash
digna project export-ds <PROJECT_NAME> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać wyeksportowane źródła danych (wymagana).

#### Opcje
- `--table-name`, `-n`: Nazwy źródeł danych do wyeksportowania. Można podać wiele nazw oddzielonych spacjami.
- `--table-id`, `-i`: Identyfikatory źródeł danych do wyeksportowania. Można podać wiele identyfikatorów oddzielonych spacjami.
- `--exportfile`, `-f`: Ścieżka, pod którą zostaną zapisane wyeksportowane źródła danych (domyślnie: `data_sources_export.json`).

#### Przykład
Aby wyeksportować wszystkie źródła danych z `ProjectA`:
```bash
digna project export-ds ProjectA --exportfile my_export.json
```

Aby wyeksportować wybrane tabele:
```bash
digna project export-ds ProjectA --table-name users orders -f users_orders_export.json
```

#### Przykładowe wyjście
```text
Successfully exported 2 data source(s) to users_orders_export.json
```

### project import-ds

Polecenie `project import-ds` importuje źródła danych z pliku eksportu do projektu docelowego i raportuje dla każdego obiektu, co zostało utworzone, zaktualizowane lub pominięte.

#### Użycie polecenia
```bash
digna project import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu docelowego, do którego następuje import (wymagana).
- **EXPORT_FILE**: Ścieżka do pliku eksportu JSON (wymagana).

#### Opcje
- `--output-file`, `-o`: Plik, do którego zostanie zapisany raport importu. Bez tej opcji raport trafia na stdout.
- `--output-format`, `-f`: Format raportu importu — `table`, `json` lub `csv` (domyślnie: `table`).

#### Przykład
```bash
digna project import-ds ProjectB my_export.json
```

Aby uzyskać raport w formacie nadającym się do przetwarzania maszynowego:
```bash
digna project import-ds ProjectB my_export.json --output-format json --output-file import_report.json
```

Raport obejmuje cztery poziomy obiektów — źródło danych, definicję zbioru danych, atrybut i regułę walidacji — każdy wraz z akcją importu, wynikiem, identyfikatorem powstałego obiektu oraz ewentualnymi dodatkowymi informacjami.

### project plan-import-ds

Polecenie `project plan-import-ds` pokazuje podgląd importu źródeł danych do projektu docelowego, wskazując, które obiekty zostałyby utworzone, zaktualizowane lub pominięte, bez wprowadzania jakichkolwiek zmian. Przyjmuje ten sam plik eksportu i te same opcje raportowania co [`project import-ds`](#project-import-ds), a dodatkowo podaje numer kroku dla każdego zaplanowanego obiektu.

#### Użycie polecenia
```bash
digna project plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu docelowego (wymagana).
- **EXPORT_FILE**: Ścieżka do pliku eksportu (wymagana).

#### Opcje
- `--output-file`, `-o`: Plik, do którego zostanie zapisany plan importu. Bez tej opcji plan trafia na stdout.
- `--output-format`, `-f`: Format planu importu — `table`, `json` lub `csv` (domyślnie: `table`).

#### Przykład
```bash
digna project plan-import-ds ProjectB my_export.json
```

---

## Zarządzanie inspekcjami

---

### inspection run

Polecenie `inspection run` tworzy żądanie inspekcji dla projektu i zakresu dat, a następnie — zależnie od podanych opcji — albo na nie czeka, albo natychmiast kończy działanie, albo wykonuje je we własnym procesie.

Trzy tryby wykonania to:

- **Domyślny (bez flagi)**: żądanie trafia do kolejki backendu, a CLI odpytuje je co dwie sekundy, wypisując postęp zadań, dopóki inspekcja nie osiągnie stanu końcowego. Wymagany jest działający `digna serve`, w przeciwnym razie nic nie odbierze żądania.
- **`--async-mode`**: żądanie trafia do kolejki, a jego identyfikator jest wypisywany natychmiast. Do jego śledzenia użyj [`inspection status`](#inspection-status).
- **`--bypass-backend`**: inspekcja jest wykonywana przez sam proces CLI i nie trafia do kolejki, więc działający serwer nie jest potrzebny.

`--async-mode` i `--bypass-backend` wzajemnie się wykluczają.

W każdym trybie polecenie kończy się niezerowym kodem wyjścia, jeśli inspekcja nie zakończyła się powodzeniem.

#### Użycie polecenia
```bash
digna inspection run <PROJECT_NAME> <START_DATE> <END_DATE> [OPTIONS]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu docelowego (wymagana). Nazwa musi być dokładnie zgodna.
- **START_DATE**: Data początkowa zakresu dat w formacie `YYYY-MM-DD` (wymagana).
- **END_DATE**: Data końcowa zakresu dat w formacie `YYYY-MM-DD` (wymagana).

#### Opcje
- `--table-name`: Ogranicza inspekcję do jednego źródła danych projektu, wskazanego nazwą tego źródła. Bez tej opcji inspekcji podlegają wszystkie źródła danych projektu.
- `--async-mode`: Umieszcza inspekcję w kolejce i wypisuje identyfikator żądania zamiast na nie czekać. Nie można łączyć z `--bypass-backend`.
- `--bypass-backend`: Uruchamia inspekcję bezpośrednio w procesie CLI zamiast umieszczać ją w kolejce backendu. Nie można łączyć z `--async-mode`.

#### Przykład
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31
```

Aby zlecić inspekcję asynchroniczną:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --async-mode
```

Aby przeprowadzić inspekcję jednego źródła danych:
```bash
digna inspection run ProjectA 2024-01-01 2024-01-31 --table-name orders
```

#### Przykładowe wyjście
Tryb domyślny:
```text
Inspection request submitted. Waiting for completion (Request ID: 1024)...
Progress: 3/10 tasks completed (0 failed)
Progress: 10/10 tasks completed (0 failed)
Inspection completed successfully.
Inspection successful for project: ProjectA
```

Tryb asynchroniczny:
```text
Inspection request submitted successfully. Request ID: 1024
```

### inspection status

Polecenie `inspection status` odpytuje o stan i postęp zadań żądania inspekcji na podstawie jego identyfikatora.

#### Użycie polecenia
```bash
digna inspection status <INSPECTION_REQUEST_ID>
```

#### Argumenty
- **INSPECTION_REQUEST_ID**: Liczbowy identyfikator żądania inspekcji (wymagany).

#### Przykład
```bash
digna inspection status 1024
```

#### Przykładowe wyjście
```text
Inspection Request ID: 1024
Status: Running
Project ID: 7
Date Range: 2024-01-01 to 2024-01-31
Progress: 3/10 tasks completed (0 failed)
```

### inspection abort

Polecenie `inspection abort` zgłasza żądanie anulowania trwających lub oczekujących żądań inspekcji. Zapisuje zdarzenie zatrzymania dla każdego objętego nim żądania; działa na nie backend, więc przerwanie jest prośbą o zatrzymanie, a nie natychmiastowym zabiciem procesu.

#### Użycie polecenia
```bash
digna inspection abort [INSPECTION_REQUEST_ID] [OPTIONS]
```

#### Argumenty
- **INSPECTION_REQUEST_ID**: Identyfikator żądania inspekcji do przerwania. Wymagany, chyba że podano `--killall`.

#### Opcje
- `--killall`: Przerywa wszystkie aktualnie trwające i oczekujące żądania inspekcji. Ma pierwszeństwo przed identyfikatorem żądania podanym obok niej.

#### Przykład
Aby przerwać konkretne żądanie:
```bash
digna inspection abort 1024
```

Aby przerwać wszystkie aktywne i oczekujące w kolejce inspekcje:
```bash
digna inspection abort --killall
```

#### Przykładowe wyjście
`--killall` raportuje, co zrobiła; przerwanie pojedynczego żądania nie daje żadnego wyjścia i sygnalizuje powodzenie kodem wyjścia.
```text
All running and pending inspections have been aborted.
```

---

## Zarządzanie licencjami

---

### license check

Polecenie `license check` weryfikuje plik `license.toml`, sprawdzając jego podpis przy użyciu klucza publicznego dostarczanego wraz z instalacją oraz kontrolując, czy licencja nie wygasła. Nie wczytuje żadnej konfiguracji aplikacji, więc działa również zanim `config.toml` zostanie skonfigurowany.

#### Użycie polecenia
```bash
digna license check
```

#### Przykładowe wyjście
```text
License is valid
```

Nieprawidłowy podpis i wygasła licencja są zgłaszane jako odrębne błędy, oba z kodem wyjścia 1.

---

## Serwer i usługi działające w tle

---

### serve

Polecenie `serve` uruchamia serwer REST API ***digna*** wraz z działającymi w tle harmonogramem inspekcji i menedżerem inspekcji. Podczas uruchamiania oznacza także jako nieudaną każdą inspekcję, którą repozytorium wciąż zapisuje jako trwającą, ponieważ nic nie mogło przetrwać z wcześniejszego procesu.

Polecenie działa na pierwszym planie, dopóki nie zostanie zatrzymane.

#### Użycie polecenia
```bash
digna serve [OPTIONS]
```

#### Opcje
- `--address`: Adres sieciowy, na którym nasłuchuje serwer API (domyślnie: `127.0.0.1`).
- `--port`: Numer portu, na którym prowadzone jest nasłuchiwanie (domyślnie: `8000`).

#### Przykład
```bash
digna serve --address 0.0.0.0 --port 8000
```

#### Przykładowe wyjście
```text
Server running on http://0.0.0.0:8000
```