---
title: digna CLI Reference 2026.04 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2026.04
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202604/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.04
**2026-04-08**

Ta strona dokumentuje pełen zestaw poleceń dostępnych w CLI ***digna*** w wydaniu **2026.04**, w tym przykłady użycia i opcje.

---

## CLI Basics

---

### help
Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby korzystania z tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj --help bezpośrednio po słowie kluczowym ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Uzyskanie pomocy dla konkretnych poleceń:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dopisz `--help` do tego polecenia.
    Na przykład, aby uzyskać pomoc dla polecenia `add-user`, uruchom:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis działania polecenia.  
     - **Składnia:** Pokazuje dokładną składnię, w tym argumenty wymagane i opcjonalne.  
     - **Opcje:** Wymienia opcje specyficzne dla polecenia wraz z ich objaśnieniami.  
     - **Przykłady:** Zawiera przykłady skutecznego wykonania polecenia.

### check-config

Polecenie check-config jest narzędziem w CLI ***digna*** zaprojektowanym do testowania konfiguracji ***digna***. To polecenie zapewnia, że komponenty ***digna*** potrafią odnaleźć potrzebne elementy konfiguracyjne w pliku config.toml.

#### Options

- `--configpath`, `-cp`: Plik lub katalog zawierający konfigurację. Jeśli pominięte, użyty zostanie ../config.toml.
      
#### Command Usage
```bash
dignacli check-config
```

Po pomyślnym wykonaniu polecenie wyświetla potwierdzenie kompletności konfiguracji.  
  
Jeśli konfiguracja wydaje się niekompletna, zostaną wypisane brakujące elementy konfiguracji.

  
### check-repo-connection

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** zaprojektowanym do testowania łączności i dostępu do określonego repozytorium ***digna***. To polecenie zapewnia, że CLI może komunikować się z repozytorium.
      
#### Command Usage
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wyświetla potwierdzenie połączenia wraz ze szczegółami dotyczącymi repozytorium: wersja repozytorium, host, baza danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.


### version

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
#### Command Usage
```bash
dignacli --version
```
  
#### Example Output
```bash
dignacli version 2026.04
```

### logging options
  
Domyślnie wyjście konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń oferuje możliwość uzyskania dodatkowych informacji, używając następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” określają poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

## User Management

### add-user
  
Polecenie add-user w CLI ***digna*** służy do dodawania nowego użytkownika do systemu ***digna***.
  
#### Command Usage
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Arguments

- **USER_NAME**: Nazwa użytkownika dla nowego konta (wymagane).
- **USER_FULL_NAME**: Pełne imię i nazwisko nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

#### Options

- `--is_superuser`, `-su`: Flaga oznaczająca, że nowy użytkownik ma być administratorem.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta użytkownika w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie ustawione, konto nie ma daty wygaśnięcia.

#### Example

Aby dodać nowego użytkownika o nazwie użytkownika `jdoe`, pełnym imieniu `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### delete-user
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
#### Command Usage
```bash
dignacli delete-user USER_NAME
```
  
#### Arguments
- **USER_NAME**: Nazwa użytkownika, którego konto ma zostać usunięte (wymagane). To jedyny wymagany argument dla tego polecenia.

#### Example
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia usunie użytkownika `jdoe` z systemu ***digna***, cofając jego dostęp i usuwając powiązane dane oraz uprawnienia z repozytorium.

### modify-user

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

#### Command Usage
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
#### Arguments
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowe pełne imię i nazwisko użytkownika (wymagane).
  
#### Options  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superużytkownika, przyznając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta użytkownika w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
#### Example
  
Aby zmodyfikować pełne imię użytkownika `jdoe` na „Johnathan Doe” i ustawić go jako superużytkownika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### modify-user-pwd
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
#### Command Usage
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
#### Arguments
  
- **USER_NAME**: Nazwa użytkownika, którego hasło ma zostać zmienione (wymagane).
- **USER_PWD**: Nowe hasło dla użytkownika (wymagane).
  
#### Example
  
Aby zmienić hasło użytkownika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### list-users

Polecenie `list-users` w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

#### Command Usage

```bash
dignacli list-users
```

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełne imię i nazwisko, status superużytkownika oraz znaczniki czasu wygaśnięcia.

## Repository Management

### upgrade-repo
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do uaktualnienia lub zainicjowania repozytorium ***digna***. To polecenie jest niezbędne do stosowania aktualizacji lub do pierwszego skonfigurowania infrastruktury repozytorium.
  
#### Command Usage

```bash
dignacli upgrade-repo [options]
```
  
#### Options
  
- `--simulation-mode`, `-s`: Po włączeniu to polecenie uruchamia tryb symulacji, który wypisuje instrukcje SQL, które zostałyby wykonane, ale ich nie uruchamia. Przydatne do podglądu zmian bez modyfikowania repozytorium.  

  
#### Example
  
Aby zaktualizować repozytorium ***digna***, możesz uruchomić polecenie bez żadnych opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są zgodne z najnowszą wersją oprogramowania.

### encrypt
  
Polecenie `encrypt` w CLI ***digna*** służy do zaszyfrowania hasła.
  
#### Command Usage
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Arguments
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
#### Example
  
Aby zaszyfrować hasło, należy podać hasło jako argument.   
Na przykład, aby zaszyfrować hasło `mypassword123`, użyj:
```bash
dignacli encrypt mypassword123
```
To polecenie zwraca zaszyfrowaną wersję podanego hasła, którą można następnie wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd wskazujący brakujący argument.

### generate-key
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczania haseł przechowywanych w repozytorium ***digna***.
  
#### Command Usage
```bash
dignacli generate-key
```
  
## Data Management

### clean-up

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji i danych systemu sygnalizacji świetlnej dla jednego lub większej liczby źródeł danych w określonym projekcie. To polecenie jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

#### Command Usage

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby iterowało przez wszystkie istniejące projekty i zastosowało to polecenie.
- **FROM_DATE**: Data i czas początkowy usuwania danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas końcowy usuwania danych, w tych samych formatach co FROM_DATE (wymagane).
  
#### Options
  
- `--table-name`, `-tn`: Ogranicza operację czyszczenia do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr ograniczający czyszczenie do tabel zawierających podany podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu czyszczenia po jego zakończeniu.
- `--help`: Wyświetla informacje pomocy dla polecenia clean-up i kończy działanie.
  
#### Example
  
Aby usunąć dane z projektu ProjectA w okresie od 1 stycznia 2023 do 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią danych i zapewnia, że repozytorium zawiera tylko istotne informacje.

### remove-orphans
  
Polecenie `remove-orphans` w CLI ***digna*** służy do porządkowania w repozytorium ***digna***.  
Kiedy użytkownik usuwa projekty lub źródła danych, profile i predykcje pozostają w repozytorium. Dzięki temu poleceniu takie osierocone wiersze zostaną usunięte z repozytorium.
  
#### Command Usage
  
```bash
dignacli list-projects
```

### list-projects
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
#### Command Usage
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

### list-ds

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. To polecenie pomaga zrozumieć zasoby danych dostępne do analizy i zarządzania w systemie ***digna***.

#### Command Usage
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Arguments
- **PROJECT_NAME**: Nazwa projektu, dla którego wymieniane są źródła danych (wymagane).
  
#### Example
  
Aby wyświetlić wszystkie źródła danych w projekcie o nazwie `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
To polecenie daje użytkownikom przegląd dostępnych źródeł danych w projekcie, pomagając im lepiej nawigować i zarządzać krajobrazem danych.


### inspect

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji i danych systemu sygnalizacji świetlnej dla jednego lub większej liczby źródeł danych w określonym projekcie. To polecenie pomaga w analizie i monitorowaniu danych w określonym okresie. Po zakończeniu inspekcji zwracana jest wartość obliczonego systemu sygnalizacji świetlnej:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Command Usage

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają być sprawdzone dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby iterowało przez wszystkie istniejące projekty i zastosowało to polecenie.
- **FROM_DATE**: Data i czas początkowy inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas końcowy inspekcji danych, w tych samych formatach co FROM_DATE (wymagane).
  
#### Options

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby sprawdzać tylko tabele zawierające określony podciąg w nazwie.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.
- `--bypass-backend`, `-bb`: Pomija backend i uruchamia inspekcję bezpośrednio z CLI (tylko do celów testowych!).

  
#### Example
  
Aby przeprowadzić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby sprawdzić tylko konkretną tabelę i wymusić ponowne obliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest przydatne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemami alertów w określonym przedziale czasowym projektu.

### inspect-async

Polecenie `inspect-async` w CLI ***digna*** służy do tworzenia profili, predykcji i danych systemu sygnalizacji świetlnej dla jednego lub większej liczby źródeł danych w określonym projekcie. To polecenie pomaga w analizie i monitorowaniu danych w określonym okresie. W przeciwieństwie do polecenia `inspect`, to polecenie nie czeka na zakończenie inspekcji.
Zamiast tego zwraca identyfikator żądania dla przesłanej inspekcji. Aby sprawdzić postęp procesu inspekcji, użyj polecenia `inspect-status`.

#### Command Usage

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają być sprawdzone dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby iterowało przez wszystkie istniejące projekty i zastosowało to polecenie.
- **FROM_DATE**: Data i czas początkowy inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas końcowy inspekcji danych, w tych samych formatach co FROM_DATE (wymagane).
  
#### Options

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby sprawdzać tylko tabele zawierające określony podciąg w nazwie.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.

  
#### Example
  
Aby uruchomić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
### inspect-status

Polecenie `inspect-status` w CLI ***digna*** służy do sprawdzenia postępu asynchronicznej inspekcji na podstawie identyfikatora żądania.

#### Command Usage

```bash
dignacli inspect-status <REQUEST ID>
```
  
#### Arguments
  
- **REQUEST_ID**: Identyfikator żądania zwrócony przez polecenie `inspect-async` 
  
#### Example
  
Aby sprawdzić postęp inspekcji o identyfikatorze żądania 12345:
  
```bash
dignacli inspect-status 12345
```

### inspect-cancel

Polecenie `inspect-cancel` w CLI ***digna*** służy do anulowania inspekcji na podstawie identyfikatora żądania lub może być użyte do anulowania wszystkich aktualnych żądań.

#### Command Usage

```bash
dignacli inspect-cancel <REQUEST ID>
dignacli inspect-cancel --killall

```
  
#### Arguments
  
- **REQUEST_ID**: Identyfikator żądania zwrócony przez polecenie `inspect-async` 
  
#### Example
  
Aby anulować inspekcję o identyfikatorze żądania 12345:
  
```bash
dignacli inspect-cancel 12345
```

Aby anulować wszystkie żądania, które są obecnie uruchomione lub oczekujące:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Polecenie `export-ds` w CLI ***digna*** służy do utworzenia eksportu źródeł danych z repozytorium ***digna***. Domyślnie wyeksportowane zostaną wszystkie źródła danych z danego projektu.

#### Command Usage
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Arguments
- **PROJECT_NAME**: Nazwa projektu, z którego będą eksportowane źródła danych.

#### Options

- `--table_name`, `-tn`: Eksportuje konkretne źródło danych z projektu.
- `--exportfile`, `-ef`: Określa nazwę pliku dla eksportu.
    
#### Example
  
Aby wyeksportować wszystkie źródła danych z projektu o nazwie `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
To polecenie eksportuje wszystkie źródła danych z `ProjectA` jako dokument JSON, który można zaimportować do innego projektu lub repozytorium ***digna***.


### import-ds

Polecenie `import-ds` w CLI ***digna*** służy do importowania źródeł danych do docelowego projektu oraz do utworzenia raportu z importu.

#### Command Usage
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: Nazwa projektu, do którego będą importowane źródła danych.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać zaimportowany.

#### Options

- `--output-file`, `-o`: Plik do zapisania raportu z importu (jeśli nie określono, wydruk w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu z importu (json, csv).
    
#### Example
  
Aby zaimportować wszystkie źródła danych z pliku eksportu `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po imporcie to polecenie wyświetli również raport zaimportowanych i pominiętych obiektów. Do `ProjectB` zostaną zaimportowane tylko nowe źródła danych. Aby dowiedzieć się, które obiekty zostałyby zaimportowane, a które pominięte, możesz użyć polecenia `plan-import-ds`.

### plan-import-ds

Polecenie `plan-import-ds` w CLI ***digna*** służy do przeanalizowania importu źródeł danych do docelowego projektu i utworzenia raportu importu (plan importu).

#### Command Usage
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Arguments
- **PROJECT_NAME**: Nazwa projektu, do którego źródła danych byłyby importowane.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać przeanalizowany przed importem.

#### Options

- `--output-file`, `-o`: Plik do zapisania raportu z importu (jeśli nie określono, wydruk w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu z importu (json, csv).
    
#### Example
  
Aby sprawdzić, które źródła danych zostałyby zaimportowane, a które pominięte z pliku eksportu `my_export.json` podczas importu do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
To polecenie pokaże tylko plan importu obiektów, które miałyby zostać zaimportowane i pominięte.