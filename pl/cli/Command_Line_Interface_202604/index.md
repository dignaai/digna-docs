# digna CLI Reference 2026.04
**2026-04-08**

Ta strona dokumentuje pełen zestaw poleceń dostępnych w CLI ***digna*** w wydaniu **2026.04**, wraz z przykładami użycia i opcjami.

---

## CLI Basics

---

### help
Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby użycia tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj –help bezpośrednio po słowie kluczowym ***digna***cl  
   ```bash
   dignacli --help
   ```

2. **Uzyskanie pomocy dla konkretnego polecenia:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dopisz `--help` do tego polecenia.
    Na przykład, aby uzyskać pomoc dla polecenia `add-user`, uruchom:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis tego, co robi polecenie.  
     - **Składnia:** Pokazuje dokładną składnię, w tym argumenty wymagane i opcjonalne.  
     - **Opcje:** Wykaz opcji specyficznych dla polecenia wraz z wyjaśnieniami.  
     - **Przykłady:** Podaje przykłady efektywnego wykonania polecenia.

### check-config

Polecenie check-config jest narzędziem w CLI ***digna*** zaprojektowanym do testowania konfiguracji ***digna***. To polecenie sprawdza, czy komponenty ***digna*** mogą znaleźć wymagane elementy konfiguracyjne w pliku config.toml.

#### Opcje

- `--configpath`, `-cp`: Plik lub katalog zawierający konfigurację. Jeśli pominięte, użyty zostanie ../config.toml.
      
#### Użycie polecenia
```bash
dignacli check-config
```

Po pomyślnym wykonaniu polecenie wypisze potwierdzenie kompletności konfiguracji.  
  
Jeżeli konfiguracja wydaje się niekompletna, zostaną wypisane brakujące elementy konfiguracji.

  
### check-repo-connection

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do wskazanego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może komunikować się z repozytorium.
      
#### Użycie polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wypisze potwierdzenie połączenia oraz szczegóły dotyczące repozytorium: wersję repozytorium, hosta, bazę danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.


### version

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
#### Użycie polecenia
```bash
dignacli --version
```
  
#### Przykładowy output
```bash
dignacli version 2026.04
```

### logging options
  
Domyślnie wyjście w konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń oferuje możliwość dostarczenia dodatkowych informacji przy użyciu następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” definiują poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

## User Management

### add-user
  
Polecenie add-user w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenty

- **USER_NAME**: Nazwa użytkownika dla nowego użytkownika (wymagane).
- **USER_FULL_NAME**: Pełna nazwa nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

#### Opcje

- `--is_superuser`, `-su`: Flaga oznaczająca, że nowy użytkownik ma uprawnienia administratora.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie ustawione, konto nie ma daty wygaśnięcia.

#### Przykład

Aby dodać nowego użytkownika o nazwie użytkownika `jdoe`, pełnej nazwie `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenty
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). To jedyny argument wymagany przez to polecenie.

#### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia usunie użytkownika `jdoe` z systemu ***digna***, cofając jego dostęp i usuwając powiązane dane oraz uprawnienia z repozytorium.

### modify-user

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

#### Użycie polecenia
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowa pełna nazwa użytkownika (wymagane).
  
#### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superusera, nadając podwyższone uprawnienia. Flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie podano, konto pozostaje ważne bezterminowo.  
  
#### Przykład
  
Aby zmienić pełną nazwę użytkownika `jdoe` na „Johnathan Doe” i ustawić użytkownika jako superusera:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
#### Użycie polecenia
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego hasło ma zostać zmienione (wymagane).
- **USER_PWD**: Nowe hasło dla użytkownika (wymagane).
  
#### Przykład
  
Aby zmienić hasło użytkownika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Polecenie `list-users` w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

#### Użycie polecenia

```bash
dignacli list-users
```

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełną nazwę, status superusera oraz znaczniki czasowe wygaśnięcia.

## Repository Management

### upgrade-repo
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. To polecenie jest niezbędne do zastosowania aktualizacji lub do pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
#### Użycie polecenia

```bash
dignacli upgrade-repo [options]
```
  
#### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu ta opcja uruchamia polecenie w trybie symulacji, który wypisuje instrukcje SQL, które zostałyby wykonane, ale ich faktycznie nie wykonuje. Jest to przydatne do podglądu zmian bez modyfikowania repozytorium.  

  
#### Przykład
  
Aby zaktualizować repozytorium ***digna***, można uruchomić polecenie bez żadnych opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są aktualne względem najnowszej wersji oprogramowania.

### encrypt
  
Polecenie `encrypt` w CLI ***digna*** służy do zaszyfrowania hasła.
  
#### Użycie polecenia
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenty
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
#### Przykład
  
Aby zaszyfrować hasło, należy podać hasło jako argument.   
Na przykład, aby zaszyfrować hasło `mypassword123`, użyj:
```bash
dignacli encrypt mypassword123
```
To polecenie wypisze zaszyfrowaną wersję podanego hasła, którą można następnie wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

### generate-key
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczania haseł przechowywanych w repozytorium ***digna***.
  
#### Użycie polecenia
```bash
dignacli generate-key
```
  
## Data Management

### clean-up

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji i danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. To polecenie jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i efektywne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

#### Użycie polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego dane mają zostać usunięte (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterację po wszystkich istniejących projektach i zastosowanie tego polecenia.
- **FROM_DATE**: Data i czas rozpoczęcia usuwania danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia usuwania danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr ograniczający clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla informacje pomocnicze dla polecenia clean-up i kończy działanie.
  
#### Przykład
  
Aby usunąć dane z projektu ProjectA między 1 stycznia 2023 a 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią danych oraz zapewnia, że repozytorium zawiera tylko istotne informacje.

### remove-orphans
  
Polecenie `remove-orphans` w CLI ***digna*** służy do porządkowania w repozytorium ***digna***.  
Gdy użytkownik usuwa projekty lub źródła danych, profile i predykcje pozostają w repozytorium. Dzięki temu poleceniu takie porzucone wiersze zostaną usunięte z repozytorium.
  
#### Użycie polecenia
  
```bash
dignacli list-projects
```

### list-projects
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
#### Użycie polecenia
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

### list-ds

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to jest użyteczne do zrozumienia zasobów danych dostępnych do analizy i zarządzania w systemie ***digna***.

#### Użycie polecenia
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, dla którego wyświetlane są źródła danych (wymagane).
  
#### Przykład
  
Aby wyświetlić wszystkie źródła danych w projekcie o nazwie `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
To polecenie daje użytkownikom przegląd źródeł danych dostępnych w projekcie, pomagając w nawigacji i zarządzaniu krajobrazem danych.


### inspect

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji i danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitorowaniu danych w zadanym okresie. Po zakończeniu inspekcji zwracana jest wartość obliczonego systemu sygnalizacji świetlnej:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Użycie polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, którego dane mają zostać sprawdzone (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterację po wszystkich istniejących projektach i zastosowanie tego polecenia.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje inspekcję do tabel zawierających określony podciąg w nazwie.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.
- `--bypass-backend`, `-bb`: Obejście backendu i uruchomienie inspekcji bezpośrednio z CLI (tylko do celów testowych!).

  
#### Przykład
  
Aby sprawdzić dane dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby sprawdzić tylko konkretną tabelę i wymusić ponowne obliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest użyteczne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemami alertów w określonym przedziale czasowym projektu.

### inspect-async

Polecenie `inspect-async` w CLI ***digna*** służy do tworzenia profili, predykcji i danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitorowaniu danych w zadanym okresie. W przeciwieństwie do polecenia `inspect`, to polecenie nie oczekuje na zakończenie inspekcji.
Zamiast tego zwraca identyfikator żądania dla przesłanego zadania inspekcji. Aby zapytać o postęp procesu inspekcji, użyj polecenia `inspect-status`.

#### Użycie polecenia

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, którego dane mają zostać sprawdzone (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterację po wszystkich istniejących projektach i zastosowanie tego polecenia.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje inspekcję do tabel zawierających określony podciąg w nazwie.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.

  
#### Przykład
  
Aby sprawdzić dane dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Polecenie `inspect-status` w CLI ***digna*** służy do sprawdzenia postępu asynchronicznej inspekcji na podstawie identyfikatora żądania.

#### Użycie polecenia

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Argumenty
  
- **REQUEST_ID**: Identyfikator żądania zwrócony przez polecenie `inspect-async` 
  
#### Przykład
  
Aby sprawdzić postęp inspekcji o identyfikatorze żądania 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Polecenie `inspect-cancel` w CLI ***digna*** służy do anulowania inspekcji na podstawie identyfikatora żądania lub może być użyte do anulowania wszystkich bieżących żądań.

#### Użycie polecenia

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Argumenty
  
- **REQUEST_ID**: Identyfikator żądania zwrócony przez polecenie `inspect-async` 
  
#### Przykład
  
Aby anulować inspekcję o identyfikatorze żądania 12345:
  
```bash
dignacli inspect-cancel 12345
```

Aby anulować wszystkie żądania, które są obecnie uruchomione lub oczekujące:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Polecenie `export-ds` w CLI ***digna*** służy do utworzenia eksportu źródeł danych z repozytorium ***digna***. Domyślnie wszystkie źródła danych z danego projektu zostaną wyeksportowane.

#### Użycie polecenia
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, z którego źródła danych będą eksportowane.

#### Opcje

- `--table_name`, `-tn`: Eksportuje konkretne źródło danych z projektu.
- `--exportfile`, `-ef`: Określa nazwę pliku dla eksportu.
    
#### Przykład
  
Aby wyeksportować wszystkie źródła danych z projektu o nazwie `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
To polecenie eksportuje wszystkie źródła danych z `ProjectA` jako dokument JSON, który można zaimportować do innego projektu lub repozytorium ***digna***.


### import-ds

Polecenie `import-ds` w CLI ***digna*** służy do importowania źródeł danych do docelowego projektu oraz do wygenerowania raportu importu.

#### Użycie polecenia
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego zostaną zaimportowane źródła danych.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać zaimportowany.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu importu (jeśli nie zostanie określony, raport jest drukowany w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu importu (json, csv).
    
#### Przykład
  
Aby zaimportować wszystkie źródła danych z pliku eksportu `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po imporcie to polecenie pokaże również raport zaimportowanych i pominiętych obiektów. Do `ProjectB` zostaną zaimportowane tylko nowe źródła danych. Aby dowiedzieć się, które obiekty zostałyby zaimportowane, a które pominięte, możesz użyć polecenia `plan-import-ds`.

### plan-import-ds

Polecenie `plan-import-ds` w CLI ***digna*** służy do przygotowania planu importu źródeł danych do docelowego projektu i wygenerowania raportu importu.

#### Użycie polecenia
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego źródła danych byłyby importowane.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać przeanalizowany przed importem.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu importu (jeśli nie zostanie określony, raport jest drukowany w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu importu (json, csv).
    
#### Przykład
  
Aby sprawdzić, które źródła danych zostałyby zaimportowane, a które pominięte z pliku eksportu `my_export.json` przy imporcie do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
To polecenie pokaże jedynie plan importu obiektów, które zostaną zaimportowane i pominięte.