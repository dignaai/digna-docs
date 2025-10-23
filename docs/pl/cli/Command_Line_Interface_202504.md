---
title: digna CLI — Podręcznik odniesienia 2025.04 – Polecenia i przykłady | Dokumentacja digna
description: Pełne odniesienie dotyczące wydania digna CLI 2025.04. Dowiedz się, jak zarządzać użytkownikami, repozytoriami i danymi za pomocą poleceń takich jak add-user, check-repo-connection, upgrade-repo, inspect i innych.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Ta strona dokumentuje pełen zestaw poleceń dostępnych w CLI ***digna***, wydanie **2025.04**, włączając przykłady użycia i opcje.

---

## Podstawy CLI

---

## Używanie opcji `help`

Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby użycia tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj --help bezpośrednio po słowie kluczowym ***dignacli***  
   ```bash
   dignacli --help

2. **Uzyskanie pomocy dla konkretnych poleceń:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dopisz `--help` do tego polecenia.  
    Na przykład, aby otrzymać pomoc dotyczącą polecenia `add-user`, uruchom:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis działania polecenia.  
     - **Składnia:** Pokazuje dokładną składnię, w tym argumenty wymagane i opcjonalne.  
     - **Opcje:** Wymienia opcje specyficzne dla polecenia wraz z ich wyjaśnieniami.  
     - **Przykłady:** Zawiera przykłady efektywnego wykonywania polecenia.

  
## Używanie polecenia `check-repo-connection`

Polecenie check-repo-connection jest narzędziem w ramach CLI ***digna***, zaprojektowanym do testowania łączności i dostępu do określonego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może komunikować się z repozytorium.
      
#### Użycie polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wypisuje potwierdzenie połączenia oraz szczegóły dotyczące repozytorium: wersję repozytorium, host, bazę danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.

## Używanie polecenia ‘version’

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
#### Użycie polecenia
```bash
dignacli --version
```
  
#### Przykładowy wynik
```bash
dignacli version 2025.04
```

## Używanie opcji logowania
  
Domyślnie wyjście konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń oferuje możliwość dostarczenia dodatkowych informacji, korzystając z następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” określają poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

## Zarządzanie użytkownikami

### Używanie polecenia ‘add-user’
  
Polecenie add-user w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenty

- **USER_NAME**: Nazwa użytkownika dla nowego użytkownika (wymagane).
- **USER_FULL_NAME**: Pełna nazwa nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

#### Opcje

- `--is_superuser`, `-su`: Flaga wyznaczająca nowego użytkownika jako administratora.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta użytkownika w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

#### Przykład

Aby dodać nowego użytkownika o nazwie użytkownika `jdoe`, pełnej nazwie `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Używanie polecenia `delete-user`
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenty
- **USER_NAME**: Nazwa użytkownika, którego konto ma zostać usunięte (wymagane). To jedyny wymagany argument dla tego polecenia.

#### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia usunie użytkownika `jdoe` z systemu ***digna***, odbierając mu dostęp i usuwając powiązane dane oraz uprawnienia z repozytorium.

### Używanie polecenia `modify-user`

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

#### Użycie polecenia
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowa pełna nazwa użytkownika (wymagane).
  
#### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superużytkownika, nadając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bez ograniczeń czasowych.  
  
#### Przykład
  
Aby zmienić pełną nazwę użytkownika `jdoe` na „Johnathan Doe” i nadać mu uprawnienia superużytkownika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Używanie polecenia `modify-user-pwd`
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
#### Użycie polecenia
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego hasło ma zostać zmienione (wymagane).
- **USER_PWD**: Nowe hasło użytkownika (wymagane).
  
#### Przykład
  
Aby zmienić hasło użytkownika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Używanie polecenia `list-users`

Polecenie `list-users` w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

#### Użycie polecenia

```bash
dignacli list-users
```

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełną nazwę, status superużytkownika oraz znaczniki czasowe wygaśnięcia.

## Zarządzanie repozytorium

### Używanie polecenia `upgrade-repo`
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do uaktualnienia lub zainicjowania repozytorium ***digna***. Polecenie to jest niezbędne do zastosowania aktualizacji lub do pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
#### Użycie polecenia

```bash
dignacli upgrade-repo [options]
```
  
#### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu opcja uruchamia polecenie w trybie symulacji, który wypisuje instrukcje SQL, które zostałyby wykonane, ale ich faktycznie nie wykonuje. Przydatne do podglądu zmian bez modyfikowania repozytorium.  

  
#### Przykład
  
Aby zaktualizować repozytorium ***digna***, możesz uruchomić polecenie bez opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić upgrade w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są aktualne względem najnowszej wersji oprogramowania.

### Używanie polecenia `encrypt`
  
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
To polecenie zwraca zaszyfrowaną wersję podanego hasła, którą można następnie wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

## Używanie polecenia `generate-key`
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczania haseł przechowywanych w repozytorium ***digna***.
  
#### Użycie polecenia
```bash
dignacli generate-key
```
  
## Zarządzanie danymi

## Używanie polecenia `clean-up`

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji i danych systemu sygnalizacji świetlnej (traffic light system) dla jednego lub więcej źródeł danych w ramach określonego projektu. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

#### Użycie polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia usuwania danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia usuwania danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr ograniczający clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla informacje pomocnicze dla polecenia clean-up i kończy działanie.
  
#### Przykład
  
Aby usunąć dane z projektu ProjectA w okresie od 1 stycznia 2023 do 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane wyłącznie z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga zarządzać przestrzenią danych i zapewnia, że repozytorium zawiera tylko istotne informacje.

## Używanie polecenia `list-projects`
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
#### Użycie polecenia
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie użyteczne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

## Używanie polecenia `list-ds`

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w ramach określonego projektu. Polecenie to jest pomocne w zrozumieniu zasobów danych dostępnych do analizy i zarządzania w systemie ***digna***.

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
  
To polecenie daje użytkownikom przegląd dostępnych źródeł danych w projekcie, pomagając w nawigacji i zarządzaniu krajobrazem danych.

## Używanie polecenia `inspect`

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji oraz danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitorowaniu danych w zadanym okresie.

#### Użycie polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, który ma zostać poddany inspekcji (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia inspekcji danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr do inspekcji tylko tabel zawierających określony podciąg w nazwie.
- `--do-profile`: Wymusza ponowne zebranie profili. Domyślnie do-profile jest włączone.
- `--no-do-profile`: Zapobiega ponownemu zbieraniu profili.
- `--do-prediction`: Wymusza przeliczenie predykcji. Domyślnie do-prediction jest włączone.
- `--no-do-prediction`: Zapobiega przeliczeniu predykcji.
- `--do-alert-status`: Wymusza przeliczenie statusów alertów. Domyślnie do-alert-status jest włączone.
- `--no-do-alert-status`: Zapobiega przeliczeniu statusów alertów.
- `--iterative`: Wymusza inspekcję okresu z użyciem iteracji dziennych. Domyślnie iterative jest włączone.
- `--no-iterative`: Wykonuje inspekcję całego okresu jednorazowo.
- `--enable_notification`, `-en`: Włącza wysyłanie powiadomień w przypadku alertów.
- `--timing`, `-tm`: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
  
#### Przykład
  
Aby przeprowadzić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby przeprowadzić inspekcję tylko konkretnej tabeli i wymusić przeliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest przydatne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektu.

## Używanie polecenia `tls-status`

Polecenie `tls-status` w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie na dany dzień. System sygnalizacji świetlnej dostarcza informacji o zdrowiu i jakości danych, wskazując ewentualne problemy lub alerty, które wymagają uwagi.
  
#### Użycie polecenia
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego sprawdzany jest status TLS (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której potrzebny jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
#### Przykład
  
Aby sprawdzić status TLS dla tabeli o nazwie UserData w projekcie ProjectA na dzień 1 lipca 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając jasny i możliwy do działania raport statusu opartego na zdefiniowanych kryteriach.

## Używanie polecenia `inspect-async`

Polecenie `inspect-async` w CLI ***digna*** służy do zlecenia backendowi asynchronicznego wykonania inspekcji dla jednego lub więcej źródeł danych dla danego projektu. Jeśli project_name ustawiony jest na all-projects, inspekcja zostanie przeprowadzona we wszystkich dostępnych projektach. Polecenie zwraca identyfikator żądania (request id), który można wykorzystać do śledzenia postępu inspekcji.

#### Użycie polecenia

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, który ma zostać poddany inspekcji (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia inspekcji danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr do inspekcji tylko tabel zawierających określony podciąg w nazwie.

  
#### Przykład
  
Aby zlecić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Używanie polecenia `inspect-status`

Polecenie `inspect-status` w CLI ***digna*** służy do sprawdzenia postępów inspekcji asynchronicznej na podstawie identyfikatora żądania.

#### Użycie polecenia

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenty
  
- **REQUEST_ID**: Identyfikator żądania zwrócony przez polecenie `inspect-async` 
  
#### Opcje

- `--report_level`, `-rl`: Ustaw poziom raportu: 'task' lub 'step' [domyślnie: task]
  
#### Przykład
  
Aby sprawdzić postęp inspekcji o identyfikatorze żądania 12345 na szczegółowym poziomie kroków:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Używanie polecenia `export-ds`

Polecenie `export-ds` w CLI ***digna*** służy do utworzenia eksportu źródeł danych z repozytorium ***digna***. Domyślnie eksportowane są wszystkie źródła danych z danego projektu.

#### Użycie polecenia
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, z którego będą eksportowane źródła danych.

#### Opcje

- `--table_name`, `-tn`: Eksport konkretnego źródła danych z projektu.
- `--exportfile`, `-ef`: Określenie nazwy pliku dla eksportu.
    
#### Przykład
  
Aby wyeksportować wszystkie źródła danych z projektu o nazwie `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
To polecenie eksportuje wszystkie źródła danych z `ProjectA` jako dokument JSON, który można zaimportować do innego projektu lub repozytorium ***digna***.


## Używanie polecenia `import-ds`

Polecenie `import-ds` w CLI ***digna*** służy do importu źródeł danych do docelowego projektu oraz wygenerowania raportu importu.

#### Użycie polecenia
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego zostaną zaimportowane źródła danych.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać zaimportowany.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu importu (jeśli nie podano, raport drukowany jest w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu importu (json, csv).
    
#### Przykład
  
Aby zaimportować wszystkie źródła danych z pliku eksportu `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po imporcie to polecenie pokaże także raport zaimportowanych i pominiętych obiektów. Do `ProjectB` zostaną zaimportowane tylko nowe źródła danych. Aby dowiedzieć się, które obiekty zostałyby zaimportowane, a które pominięte, możesz użyć polecenia `plan-import-ds`

## Używanie polecenia `plan-import-ds`

Polecenie `plan-import-ds` w CLI ***digna*** służy do przygotowania planu importu źródeł danych do docelowego projektu i wygenerowania raportu planu importu.

#### Użycie polecenia
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego źródła danych byłyby zaimportowane.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać przeanalizowany przed importem.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu planu importu (jeśli nie podano, raport drukowany jest w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu planu importu (json, csv).
    
#### Przykład
  
Aby sprawdzić, które źródła danych zostałyby zaimportowane, a które pominięte z pliku eksportu `my_export.json` przy imporcie do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
To polecenie pokaże jedynie plan importu obiektów, które zostałyby zaimportowane i pominięte.