---
title: digna CLI Reference 2026.01 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2026.01 Learn how to manage users, repositories, and data with commands such as add-user, check-config, check-repo-connection, inspect, inspect-async, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202601/
image: /assets/logo_square.png
---

# digna CLI Reference 2026.01
**2026-01-15**

Ta strona dokumentuje pełen zestaw poleceń dostępnych w CLI ***digna*** w wydaniu **2026.01**, w tym przykłady użycia i opcje.

---

## Podstawy CLI

---

### help
Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby korzystania z tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj --help bezpośrednio po słowie kluczowym ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Uzyskanie pomocy dla konkretnego polecenia:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dodaj `--help` do tego polecenia.
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

Polecenie check-config jest narzędziem w CLI ***digna*** służącym do testowania konfiguracji ***digna***. Polecenie to sprawdza, czy komponenty ***digna*** mogą znaleźć wymagane elementy konfiguracyjne w pliku config.toml.

#### Opcje

- `--configpath`, `-cp`: Plik lub katalog zawierający konfigurację. Jeśli pominięte, zostanie użyty ../config.toml.
      
#### Użycie polecenia
```bash
dignacli check-config
```

Po pomyślnym wykonaniu polecenie wypisuje potwierdzenie kompletności konfiguracji.  
  
Jeśli konfiguracja wydaje się niekompletna, zostaną wypisane brakujące elementy konfiguracyjne.

  
### check-repo-connection

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do określonego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może komunikować się z repozytorium.
      
#### Użycie polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wypisuje potwierdzenie połączenia wraz ze szczegółami repozytorium: wersja repozytorium, host, baza danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.


### version

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
#### Użycie polecenia
```bash
dignacli --version
```
  
#### Przykładowy wynik
```bash
dignacli version 2026.01
```

### opcje logowania
  
Domyślnie wyjście konsoli poleceń ***digna*** jest minimalistyczne. Większość poleceń oferuje możliwość uzyskania dodatkowych informacji, korzystając z następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” definiują poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

## Zarządzanie użytkownikami

### add-user
  
Polecenie add-user w CLI ***digna*** służy do dodawania nowego użytkownika do systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
#### Argumenty

- **USER_NAME**: Nazwa użytkownika dla nowego konta (wymagane).
- **USER_FULL_NAME**: Pełne imię i nazwisko nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

#### Opcje

- `--is_superuser`, `-su`: Flaga oznaczająca nowego użytkownika jako administratora.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

#### Przykład

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
  
#### Użycie polecenia
```bash
dignacli delete-user USER_NAME
```
  
#### Argumenty
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). To jedyny argument wymagany przez polecenie.

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
- **USER_FULL_NAME**: Nowe pełne imię i nazwisko użytkownika (wymagane).
  
#### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superusera, przyznając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
#### Przykład
  
Aby zmodyfikować pełne imię użytkownika `jdoe` na „Johnathan Doe” i ustawić użytkownika jako superuser:
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

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełne imię i nazwisko, status superusera oraz znaczniki czasu wygaśnięcia.

## Zarządzanie repozytorium

### upgrade-repo
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. To polecenie jest niezbędne do zastosowania aktualizacji lub pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
#### Użycie polecenia

```bash
dignacli upgrade-repo [options]
```
  
#### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu to polecenie działa w trybie symulacji, który wypisuje instrukcje SQL, które zostałyby wykonane, ale ich faktycznie nie wykonuje. Przydatne do przejrzenia zmian bez wprowadzania modyfikacji w repozytorium.  

  
#### Przykład
  
Aby zaktualizować repozytorium ***digna***, można uruchomić polecenie bez opcji:
  
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
  
#### Użycie polecenia
  
```bash
dignacli encrypt <PASSWORD>
```
    
#### Argumenty
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
#### Przykład
  
Aby zaszyfrować hasło, należy podać je jako argument.   
Na przykład, aby zaszyfrować hasło `mypassword123`, użyj:
```bash
dignacli encrypt mypassword123
```
Polecenie zwróci zaszyfrowaną wersję podanego hasła, którą można wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd wskazujący brakujący argument.

### generate-key
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczenia haseł przechowywanych w repozytorium ***digna***.
  
#### Użycie polecenia
```bash
dignacli generate-key
```
  
## Zarządzanie danymi

### clean-up

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji oraz danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w ramach określonego projektu. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać porządek i wydajność środowiska danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

#### Użycie polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego dane mają zostać usunięte (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna*** o iteracji po wszystkich istniejących projektach i zastosowaniu polecenia.
- **FROM_DATE**: Data i godzina początkowa dla usuwania danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina końcowa dla usuwania danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr pozwalający ograniczyć clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla informacje pomocnicze dla polecenia clean-up i kończy działanie.
  
#### Przykład
  
Aby usunąć dane z projektu ProjectA pomiędzy 1 stycznia 2023 a 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu miejscem na dane i zapewnia, że repozytorium zawiera tylko istotne informacje.

### remove-orphans
  
Polecenie `remove-orphans` w CLI ***digna*** służy do porządkowania repozytorium ***digna***.  
Gdy użytkownik usuwa projekty lub źródła danych, profile i predykcje mogą pozostać w repozytorium. Dzięki temu poleceniu takie osierocone wiersze zostaną usunięte z repozytorium.
  
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

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to pomaga zrozumieć zasoby danych dostępne do analizy i zarządzania w systemie ***digna***.

#### Użycie polecenia
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, dla którego wymieniane są źródła danych (wymagane).
  
#### Przykład
  
Aby wyświetlić wszystkie źródła danych w projekcie o nazwie `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
To polecenie daje użytkownikom przegląd źródeł danych dostępnych w projekcie, ułatwiając nawigację i zarządzanie krajobrazem danych.


### inspect

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji oraz danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga analizować i monitorować dane w zdefiniowanym okresie. Po zakończeniu inspekcji zwracana jest wartość obliczonego systemu sygnalizacji świetlnej:  
- 0: OK  
- 1: INFO  
- 2: WARNING

#### Użycie polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, którego dane mają zostać poddane inspekcji (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna*** o iteracji po wszystkich istniejących projektach i zastosowaniu polecenia.
- **FROM_DATE**: Data i godzina początkowa inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina końcowa inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby inspekcja objęła tylko tabele zawierające podany podciąg w nazwie.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.
- `--bypass-backend`, `-bb`: Pomija backend i uruchamia inspekcję bezpośrednio z CLI (tylko do celów testowych!).

  
#### Przykład
  
Aby przeprowadzić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby sprawdzić tylko konkretną tabelę i wymusić przeliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest przydatne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektu.

### inspect-async

Polecenie `inspect-async` w CLI ***digna*** służy do tworzenia profili, predykcji oraz danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga analizować i monitorować dane w zdefiniowanym okresie. W przeciwieństwie do polecenia `inspect-async`, to polecenie nie czeka na zakończenie inspekcji.
Zamiast tego zwraca identyfikator żądania dla zgłoszonej inspekcji. Aby sprawdzić postęp procesu inspekcji, użyj polecenia `inspect-status`

#### Użycie polecenia

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, którego dane mają zostać poddane inspekcji (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna*** o iteracji po wszystkich istniejących projektach i zastosowaniu polecenia.
- **FROM_DATE**: Data i godzina początkowa inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina końcowa inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby inspekcja objęła tylko tabele zawierające podany podciąg w nazwie.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.

  
#### Przykład
  
Aby uruchomić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  

### inspect-status

Polecenie `inspect-status` w CLI ***digna*** służy do sprawdzania postępu asynchronicznej inspekcji na podstawie identyfikatora żądania.

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

Polecenie `inspect-cancel` w CLI ***digna*** służy do anulowania inspekcji na podstawie identyfikatora żądania lub może zostać użyte do anulowania wszystkich bieżących żądań.

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

Aby anulować wszystkie żądania, które są aktualnie uruchomione lub oczekujące:
  
```bash
dignacli inspect-cancel --killall
```

  
### export-ds

Polecenie `export-ds` w CLI ***digna*** służy do utworzenia eksportu źródeł danych z repozytorium ***digna***. Domyślnie eksportowane są wszystkie źródła danych z danego projektu.

#### Użycie polecenia
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, z którego źródła danych zostaną wyeksportowane.

#### Opcje

- `--table_name`, `-tn`: Eksport konkretnego źródła danych z projektu.
- `--exportfile`, `-ef`: Określenie nazwy pliku dla eksportu.
    
#### Przykład
  
Aby wyeksportować wszystkie źródła danych z projektu o nazwie `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
To polecenie eksportuje wszystkie źródła danych z `ProjectA` jako dokument JSON, który można zaimportować do innego projektu lub repozytorium ***digna***.


### import-ds

Polecenie `import-ds` w CLI ***digna*** służy do importowania źródeł danych do docelowego projektu oraz utworzenia raportu z importu.

#### Użycie polecenia
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego źródła danych zostaną zaimportowane.
- **EXPORT_FILE**: Nazwa pliku z eksportem źródeł danych do zaimportowania.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu z importu (jeśli nie zostanie podany, raport zostanie wypisany w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu z importu (json, csv).
    
#### Przykład
  
Aby zaimportować wszystkie źródła danych z pliku eksportu `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po imporcie polecenie pokaże raport zaimportowanych i pominiętych obiektów. Do `ProjectB` zostaną zaimportowane tylko nowe źródła danych. Aby dowiedzieć się, które obiekty zostałyby zaimportowane, a które pominięte, można użyć polecenia `plan-import-ds`

### plan-import-ds

Polecenie `plan-import-ds` w CLI ***digna*** służy do przeanalizowania importu źródeł danych do docelowego projektu i wygenerowania raportu planu importu.

#### Użycie polecenia
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego źródła danych miałyby zostać zaimportowane.
- **EXPORT_FILE**: Nazwa pliku z eksportem źródeł danych, który ma zostać przeanalizowany przed importem.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu planu importu (jeśli nie zostanie podany, raport zostanie wypisany w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu planu importu (json, csv).
    
#### Przykład
  
Aby sprawdzić, które źródła danych zostałyby zaimportowane, a które pominięte z pliku eksportu `my_export.json` przy imporcie do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
To polecenie pokaże jedynie plan importu obiektów, które zostałyby zaimportowane i pominięte.