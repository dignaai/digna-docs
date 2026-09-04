---
title: digna CLI Reference 2025.04 – Polecenia i przykłady | dokumentacja digna
description: Kompletny przewodnik po wydaniu digna CLI 2025.04. Dowiedz się, jak zarządzać użytkownikami, repozytoriami i danymi za pomocą poleceń takich jak add-user, check-repo-connection, upgrade-repo, inspect i innych.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202504/
image: /assets/logo_square.png
---

# digna CLI Reference 2025.04
**2025-04-01**

Ta strona dokumentuje pełny zestaw poleceń dostępnych w CLI ***digna***, wydanie **2025.04**, wraz z przykładami użycia i opcjami.

---

## Podstawy CLI

---

## Korzystanie z opcji `--help`

Opcja `--help` udostępnia informacje o dostępnych poleceniach i sposobie ich użycia. Istnieją dwa główne sposoby korzystania z tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
   Użyj --help bezpośrednio po słowie kluczowym ***dignacli***
   ```bash
   dignacli --help
   ```

2. **Uzyskanie pomocy dla konkretnego polecenia:**  
  
   Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dołącz `--help` do tego polecenia.  
   Na przykład, aby uzyskać pomoc dotyczącą polecenia `add-user`, uruchom:
   ```bash
   dignacli add-user --help
   ```

   ### output:
      
   - **Opis polecenia:** Szczegółowy opis działania polecenia.  
   - **Składnia:** Pokazuje dokładną składnię, w tym argumenty wymagane i opcjonalne.  
   - **Opcje:** Wymienia opcje specyficzne dla polecenia wraz z wyjaśnieniami.  
   - **Przykłady:** Zawiera przykłady efektywnego wykonania polecenia.

  
## Korzystanie z polecenia `check-repo-connection`

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do określonego repozytorium ***digna***. To polecenie sprawdza, czy CLI może komunikować się z repozytorium.
      
#### Użycie polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wypisuje potwierdzenie połączenia wraz ze szczegółami repozytorium: wersja repozytorium, host, baza danych i schema.  
  
Jeżeli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.

## Korzystanie z polecenia `--version`

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
#### Użycie polecenia
```bash
dignacli --version
```
  
#### Przykładowy wynik
```bash
dignacli version 2025.04
```

## Korzystanie z opcji logowania
  
Domyślnie wyjście konsolowe poleceń ***digna*** jest minimalistyczne. Większość poleceń oferuje możliwość uzyskania dodatkowych informacji, używając następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” określają poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast na konsolę.

## Zarządzanie użytkownikami

### Korzystanie z polecenia `add-user`
  
Polecenie add-user w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
##### Argumenty

- **USER_NAME**: Nazwa użytkownika nowego konta (wymagane).
- **USER_FULL_NAME**: Pełna nazwa nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło nowego użytkownika (wymagane).

#### Opcje

- `--is_superuser`, `-su`: Flaga oznaczająca, że nowy użytkownik ma być administratorem.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

#### Przykład

Aby dodać nowego użytkownika o nazwie `jdoe`, pełnej nazwie `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

### Korzystanie z polecenia `delete-user`
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
#### Użycie polecenia
```bash
dignacli delete-user USER_NAME
```
  
##### Argumenty
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). Jest to jedyny wymagany argument polecenia.

#### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia usunie użytkownika `jdoe` z systemu ***digna***, cofając jego dostęp i usuwając powiązane dane oraz uprawnienia z repozytorium.

### Korzystanie z polecenia `modify-user`

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

#### Użycie polecenia
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
##### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowa pełna nazwa użytkownika (wymagane).
  
#### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superusera, przyznając podwyższone uprawnienia. Flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie podano, konto pozostaje ważne bez ograniczeń czasowych.  
  
#### Przykład
  
Aby zmienić pełną nazwę użytkownika `jdoe` na „Johnathan Doe” i ustawić go jako superusera:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

### Korzystanie z polecenia `modify-user-pwd`
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
#### Użycie polecenia
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
##### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego hasło ma zostać zmienione (wymagane).
- **USER_PWD**: Nowe hasło dla użytkownika (wymagane).
  
#### Przykład
  
Aby zmienić hasło użytkownika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

### Korzystanie z polecenia `list-users`

Polecenie `list-users` w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

#### Użycie polecenia

```bash
dignacli list-users
```

Wykonanie tego polecenia połączy się z repozytorium ***digna*** i wypisze wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełną nazwę, status superusera oraz znaczniki czasu wygaśnięcia.

## Zarządzanie repozytorium

### Korzystanie z polecenia `upgrade-repo`
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. Polecenie to jest niezbędne do zastosowania aktualizacji lub pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
#### Użycie polecenia

```bash
dignacli upgrade-repo [options]
```
  
#### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu ta opcja uruchamia polecenie w trybie symulacji, które wypisuje polecenia SQL, które zostałyby wykonane, ale ich nie wykonuje. Przydatne do podglądu zmian bez wprowadzania modyfikacji w repozytorium.  

  
#### Przykład
  
Aby zaktualizować repozytorium ***digna***, możesz uruchomić polecenie bez opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć polecenia SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są zgodne z najnowszą wersją oprogramowania.

### Korzystanie z polecenia `encrypt`
  
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
Polecenie zwróci zaszyfrowaną wersję podanego hasła, którą można wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

## Korzystanie z polecenia `generate-key`
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczenia haseł przechowywanych w repozytorium ***digna***.
  
#### Użycie polecenia
```bash
dignacli generate-key
```
  
## Zarządzanie danymi

## Korzystanie z polecenia `clean-up`

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji oraz danych systemu Traffic Light dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać porządek i efektywność środowiska przez usuwanie przestarzałych lub niepotrzebnych danych.

#### Użycie polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować polecenie.
- **FROM_DATE**: Data i czas rozpoczęcia usuwania danych. Akceptowane formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia usuwania danych, w tych samych formatach co FROM_DATE (wymagane).
  
#### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby ograniczyć clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla pomoc dla polecenia clean-up i kończy działanie.
  
#### Przykład
  
Aby usunąć dane z projektu ProjectA między 1 stycznia 2023 a 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią dyskową i zapewnia, że repozytorium zawiera jedynie istotne informacje.

## Korzystanie z polecenia `list-projects`
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
#### Użycie polecenia
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, dostarczając szybkiego przeglądu dostępnych projektów w repozytorium ***digna***.

## Korzystanie z polecenia `list-ds`

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie jest pomocne w zrozumieniu zasobów danych dostępnych do analizy i zarządzania w systemie ***digna***.

#### Użycie polecenia
  
```bash
dignacli list-ds <PROJECT_NAME>
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, dla którego wyświetlane są źródła danych (wymagane).
  
#### Przykład
  
Aby wylistować wszystkie źródła danych w projekcie o nazwie `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
To polecenie daje użytkownikom przegląd źródeł danych dostępnych w projekcie, ułatwiając nawigację i zarządzanie krajobrazem danych.


## Korzystanie z polecenia `inspect`

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji oraz danych systemu Traffic Light dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie pomaga w analizie i monitorowaniu danych w zdefiniowanym przedziale czasowym.

#### Użycie polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, który ma zostać poddany inspekcji (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować polecenie.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji. Akceptowane formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji, w tych samych formatach co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby inspekcja obejmowała tylko tabele zawierające określony podciąg w nazwie.
- `--do-profile`: Wymusza ponowne zebranie profili. Domyślnie do-profile jest włączone.
- `--no-do-profile`: Zapobiega ponownemu zbieraniu profili.
- `--do-prediction`: Wymusza przeliczenie predykcji. Domyślnie do-prediction jest włączone.
- `--no-do-prediction`: Zapobiega przeliczeniu predykcji.
- `--do-alert-status`: Wymusza przeliczenie statusów alertów. Domyślnie do-alert-status jest włączone.
- `--no-do-alert-status`: Zapobiega przeliczeniu statusów alertów.
- `--iterative`: Wykonuje inspekcję okresu w iteracjach dziennych. Domyślnie iterative jest włączone.
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

## Korzystanie z polecenia `tls-status`

Polecenie `tls-status` w CLI ***digna*** służy do sprawdzenia statusu Traffic Light System (TLS) dla konkretnej tabeli w projekcie na wskazaną datę. Traffic Light System dostarcza informacji o stanie zdrowia i jakości danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
#### Użycie polecenia
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego sprawdzany jest status TLS (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której wymagany jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zazwyczaj w formacie %Y-%m-%d (wymagane).
  
#### Przykład
  
Aby sprawdzić status TLS dla tabeli UserData w projekcie ProjectA na dzień 1 lipca 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając jasny i praktyczny raport statusu oparty na zdefiniowanych kryteriach.

## Korzystanie z polecenia `inspect-async`

Polecenie `inspect-async` w CLI ***digna*** służy do polecenia backendowi asynchronicznego przeprowadzenia inspekcji dla jednego lub więcej źródeł danych w danym projekcie. Jeśli PROJECT_NAME ustawiony jest na all-projects, inspekcja będzie iterować po wszystkich dostępnych projektach i wykona inspekcję. Polecenie zwraca identyfikator żądania, który może być użyty do śledzenia postępu inspekcji.

#### Użycie polecenia

```bash
dignacli inspect-async <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
#### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, który ma zostać poddany inspekcji (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować polecenie.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji. Akceptowane formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji, w tych samych formatach co FROM_DATE (wymagane).
  
#### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby inspekcja obejmowała tylko tabele zawierające określony podciąg w nazwie.

  
#### Przykład
  
Aby asynchronicznie przeprowadzić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect-async ProjectA 2024-01-01 2024-01-31
```
  
## Korzystanie z polecenia `inspect-status`

Polecenie `inspect-status` w CLI ***digna*** służy do sprawdzenia postępu asynchronicznej inspekcji na podstawie identyfikatora żądania.

#### Użycie polecenia

```bash
dignacli inspect-status <REQUEST ID> [options]
```
  
#### Argumenty
  
- **REQUEST_ID**: Identyfikator żądania zwrócony przez polecenie `inspect-async`. 
  
#### Opcje

- `--report_level`, `-rl`: Ustawia poziom raportu: 'task' lub 'step' [domyślnie: task]
  
#### Przykład
  
Aby sprawdzić postęp inspekcji o identyfikatorze żądania 12345 na szczegółowym poziomie kroków:
  
```bash
dignacli inspect-status 12345 --report-level step
```
  
## Korzystanie z polecenia `export-ds`

Polecenie `export-ds` w CLI ***digna*** służy do utworzenia eksportu źródeł danych z repozytorium ***digna***. Domyślnie eksportowane są wszystkie źródła danych z danego projektu.

#### Użycie polecenia
  
```bash
dignacli export-ds <PROJECT_NAME> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, z którego będą eksportowane źródła danych.

#### Opcje

- `--table_name`, `-tn`: Eksportuje konkretne źródło danych z projektu.
- `--exportfile`, `-ef`: Określa nazwę pliku dla eksportu.
    
#### Przykład
  
Aby wyeksportować wszystkie źródła danych z projektu `ProjectA`:
  
```bash
dignacli export-ds ProjectA
```
  
To polecenie eksportuje wszystkie źródła danych z `ProjectA` jako dokument JSON, który może zostać zaimportowany do innego projektu lub repozytorium ***digna***.


## Korzystanie z polecenia `import-ds`

Polecenie `import-ds` w CLI ***digna*** służy do importowania źródeł danych do docelowego projektu oraz wygenerowania raportu z importu.

#### Użycie polecenia
  
```bash
dignacli import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego będą importowane źródła danych.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych, który ma zostać zaimportowany.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu z importu (jeśli nie określono, raport jest drukowany w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu z importu (json, csv).
    
#### Przykład
  
Aby zaimportować wszystkie źródła danych z pliku eksportu `my_export.json` do `ProjectB`:
  
```bash
dignacli import-ds ProjectB my_export.json
```
  
Po imporcie to polecenie pokaże również raport zaimportowanych i pominiętych obiektów. Do `ProjectB` zostaną zaimportowane tylko nowe źródła danych. Aby dowiedzieć się, które obiekty zostałyby zaimportowane, a które pominięte, możesz użyć polecenia `plan-import-ds`.

## Korzystanie z polecenia `plan-import-ds`

Polecenie `plan-import-ds` w CLI ***digna*** służy do przeanalizowania pliku eksportu źródeł danych przed wykonaniem rzeczywistego importu i wygenerowania planu importu.

#### Użycie polecenia
  
```bash
dignacli plan-import-ds <PROJECT_NAME> <EXPORT_FILE> [options]
```

#### Argumenty
- **PROJECT_NAME**: Nazwa projektu, do którego źródła danych zostałyby zaimportowane.
- **EXPORT_FILE**: Nazwa pliku eksportu źródeł danych do analizy przed importem.

#### Opcje

- `--output-file`, `-o`: Plik do zapisania raportu planu importu (jeśli nie określono, drukuje się w terminalu w formie tabelarycznej).
- `--output-format`, `-f`: Format zapisu raportu planu importu (json, csv).
    
#### Przykład
  
Aby sprawdzić, które źródła danych zostałyby zaimportowane, a które pominięte z pliku eksportu `my_export.json` przy imporcie do `ProjectB`:
  
```bash
dignacli plan-import-ds ProjectB my_export.json
```
  
To polecenie pokaże jedynie plan importu obiektów, które zostaną zaimportowane i które zostaną pominięte.