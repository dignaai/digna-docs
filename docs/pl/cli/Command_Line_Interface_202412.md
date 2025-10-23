---
title: digna CLI Reference 2024.12 – Komendy i przykłady | digna Dokumentacja
description: Kompletny przewodnik po digna CLI wydanie 2024.12. Dowiedz się, jak zarządzać użytkownikami, repozytoriami i danymi za pomocą poleceń takich jak add-user, check-repo-connection, upgrade-repo, inspect i innych.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202412/
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Ta strona dokumentuje pełen zestaw poleceń dostępnych w narzędziu CLI ***digna*** w wydaniu **2024.12**, w tym przykłady użycia i dostępne opcje.

---


**2024-12-09**


---

## Podstawy CLI

---

## Użycie opcji `help`

Opcja `--help` udostępnia informacje o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby użycia tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj --help bezpośrednio po poleceniu ***dignacli***  
   ```bash
   dignacli --help
   ```

2. **Uzyskanie pomocy dla konkretnego polecenia:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dołącz `--help` do tego polecenia.  
    Na przykład, aby otrzymać pomoc dotyczącą polecenia `add-user`, uruchom:
     ```bash
     dignacli add-user --help
     ```

     ### Wyjście:
      
     - **Opis polecenia:** Szczegółowy opis działania polecenia.  
     - **Składnia:** Pokazuje dokładną składnię, w tym argumenty wymagane i opcjonalne.  
     - **Opcje:** Wyszczególnia opcje specyficzne dla polecenia wraz z objaśnieniami.  
     - **Przykłady:** Zawiera przykłady efektywnego użycia polecenia.

  
## Użycie polecenia `check-repo-connection`

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do wskazanego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może poprawnie komunikować się z repozytorium.
      
### Składnia polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenia wyświetlana jest informacja potwierdzająca połączenie oraz szczegóły dotyczące repozytorium: wersja repozytorium, host, baza danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnej konfiguracji.

## Użycie polecenia `version`

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
### Składnia polecenia
```bash
dignacli --version
```
  
### Przykładowe wyjście
```bash
dignacli version 2024.12
```

## Użycie opcji logowania
  
Domyślnie wyjście konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń pozwala jednak na uzyskanie dodatkowych informacji, korzystając z następujących opcji:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
„verbose” i „debug” definiują poziom szczegółowości, natomiast przełącznik „logfile” umożliwia przekierowanie wyjścia do pliku zamiast na konsolę.

# Zarządzanie użytkownikami

## Użycie polecenia `add-user`
  
Polecenie add-user w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
### Składnia polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenty

- **USER_NAME**: Nazwa użytkownika nowego konta (wymagane).
- **USER_FULL_NAME**: Pełne imię i nazwisko nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

### Opcje

- `--is_superuser`, `-su`: Flaga oznaczająca, że nowy użytkownik ma mieć uprawnienia administratora.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

### Przykład

Aby dodać nowego użytkownika o nazwie `jdoe`, pełnym imieniu `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Użycie polecenia `delete-user`
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
### Składnia polecenia
```bash
dignacli delete-user USER_NAME
```
  
### Argumenty
- **USER_NAME**: Nazwa użytkownika, którego konto ma zostać usunięte (wymagane). To jedyny wymagany argument dla tego polecenia.

### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia spowoduje usunięcie użytkownika `jdoe` z systemu ***digna***, odebranie mu dostępu oraz usunięcie powiązanych danych i uprawnień z repozytorium.

## Użycie polecenia `modify-user`

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

### Składnia polecenia
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowe pełne imię i nazwisko użytkownika (wymagane).
  
### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superużytkownika, nadając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
### Przykład
  
Aby zmodyfikować pełne imię użytkownika `jdoe` na „Johnathan Doe” i ustawić go jako superużytkownika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Użycie polecenia `modify-user-pwd`
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
### Składnia polecenia
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego hasło ma zostać zmienione (wymagane).
- **USER_PWD**: Nowe hasło dla użytkownika (wymagane).
  
### Przykład
  
Aby zmienić hasło użytkownika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Użycie polecenia `list-users`

Polecenie `list-users` w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

### Składnia polecenia

```bash
dignacli list-users
```

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełne imię i nazwisko, status superużytkownika oraz znaczniki czasowe wygaśnięcia.

# Zarządzanie repozytorium

### Użycie polecenia `upgrade-repo`
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. Polecenie to jest niezbędne do zastosowania aktualizacji lub do pierwszego skonfigurowania infrastruktury repozytorium.
  
### Składnia polecenia

```bash
dignacli upgrade-repo [options]
```
  
### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu uruchamia polecenie w trybie symulacji, które wypisuje instrukcje SQL, które zostałyby wykonane, ale ich nie wykonuje. Przydatne do podglądu zmian bez wprowadzania modyfikacji w repozytorium.  

  
### Przykład
  
Aby zaktualizować repozytorium ***digna***, można uruchomić polecenie bez opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są zgodne z najnowszą wersją oprogramowania.

## Użycie polecenia `encrypt`
  
Polecenie `encrypt` w CLI ***digna*** służy do zaszyfrowania hasła.
  
### Składnia polecenia
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenty
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
### Przykład
  
Aby zaszyfrować hasło, należy podać je jako argument.   
Na przykład, aby zaszyfrować hasło `mypassword123`, użyj:
```bash
dignacli encrypt mypassword123
```
Polecenie zwróci zaszyfrowaną wersję podanego hasła, którą można wykorzystać w bezpiecznych kontekstach. Jeśli argument z hasłem nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

## Użycie polecenia `generate-key`
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczania haseł przechowywanych w repozytorium ***digna***.
  
### Składnia polecenia
```bash
dignacli generate-key
```
  
# Zarządzanie danymi

## Użycie polecenia `clean-up`

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji oraz danych systemu sygnalizacji świetlnej (traffic light system) dla jednego lub wielu źródeł danych w obrębie określonego projektu. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

### Składnia polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego all-projects spowoduje, że ***digna*** przeiteruje przez wszystkie istniejące projekty i zastosuje polecenie dla każdego z nich.
- **FROM_DATE**: Data i czas rozpoczęcia usuwania danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia usuwania danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr ograniczający clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla informacje pomocnicze dotyczące polecenia clean-up i kończy działanie.
  
### Przykład
  
Aby usunąć dane z projektu ProjectA w okresie od 1 stycznia 2023 do 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią danych i zapewnia, że repozytorium zawiera wyłącznie istotne informacje.

## Użycie polecenia `inspect`

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji oraz danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w obrębie wskazanego projektu. Polecenie to pomaga w analizie i monitorowaniu danych w określonym okresie.

### Składnia polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, którego dane mają zostać zinspekcjonowane (wymagane). Użycie słowa kluczowego all-projects spowoduje, że ***digna*** przeiteruje przez wszystkie istniejące projekty i zastosuje polecenie dla każdego z nich.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr do inspekcji tylko tabel zawierających określony podciąg w nazwie.
- `--do-profile`: Wymusza ponowne zebranie profili. Domyślnie włączone (do-profile).
- `--no-do-profile`: Zapobiega ponownemu zbieraniu profili.
- `--do-prediction`: Wymusza ponowne obliczenie predykcji. Domyślnie włączone (do-prediction).
- `--no-do-prediction`: Zapobiega ponownemu obliczaniu predykcji.
- `--do-alert-status`: Wymusza ponowne obliczenie statusów alertów. Domyślnie włączone (do-alert-status).
- `--no-do-alert-status`: Zapobiega ponownemu obliczaniu statusów alertów.
- `--iterative`: Wykonuje inspekcję okresu w iteracjach dziennych. Domyślnie włączone (iterative).
- `--no-iterative`: Wykonuje inspekcję całego okresu jednorazowo.
- `--timing`, `-tm`: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
  
### Przykład
  
Aby zinspekcjonować dane dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby zinspekcjonować tylko konkretną tabelę i wymusić przeliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest użyteczne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektu.

## Użycie polecenia `tls-status`

Polecenie `tls-status` w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie dla wskazanej daty. System sygnalizacji świetlnej dostarcza informacji o stanie jakości i zdrowia danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
### Składnia polecenia
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego sprawdzany jest status TLS (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której potrzebny jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
### Przykład
  
Aby sprawdzić status TLS dla tabeli o nazwie UserData w projekcie ProjectA na dzień 1 lipca 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

To polecenie pomaga użytkownikom w monitorowaniu i utrzymaniu jakości danych, dostarczając przejrzysty i praktyczny raport statusu oparty na zdefiniowanych kryteriach.

## Użycie polecenia `list-projects`
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
### Składnia polecenia
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

## Użycie polecenia `list-ds`

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to pomaga zrozumieć zasoby danych dostępne do analizy i zarządzania w systemie ***digna***.

### Składnia polecenia
  
```bash
dignacli list-ds <PROJECT_NAME>
```

### Argumenty
- **PROJECT_NAME**: Nazwa projektu, dla którego wyświetlane są źródła danych (wymagane).
  
### Przykład
  
Aby wyświetlić wszystkie źródła danych w projekcie o nazwie `ProjectA`:
  
```bash
dignacli list-ds ProjectA
```
  
To polecenie daje użytkownikom przegląd źródeł danych dostępnych w projekcie, pomagając efektywniej nawigować i zarządzać krajobrazem danych.