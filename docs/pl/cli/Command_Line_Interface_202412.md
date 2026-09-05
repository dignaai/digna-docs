---
title: digna CLI Reference 2024.12 – Komendy i przykłady | digna Documentation
description: Pełne odniesienie do digna CLI wydanie 2024.12. Naucz się zarządzać użytkownikami, repozytoriami i danymi za pomocą poleceń takich jak add-user, check-repo-connection, upgrade-repo, inspect i innych.
image: /assets/logo_square.png
---


# digna CLI Reference 2024.12
**2024-12-09**

Ta strona dokumentuje pełny zestaw poleceń dostępnych w CLI ***digna***, wydanie **2024.12**, w tym przykłady użycia i opcje.

---


**2024-12-09**


---

## Podstawy CLI

---

## Użycie opcji `--help`

Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby korzystania z tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
   Użyj --help bezpośrednio po słowie kluczowym ***dignacli***
   ```bash
   dignacli --help
   ```

3.  **Uzyskanie pomocy dla konkretnych poleceń:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dołącz `--help` do tego polecenia.
    Na przykład, aby otrzymać pomoc dla polecenia `add-user`, uruchom:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis działania polecenia.  
     - **Składnia:** Pokazuje dokładną składnię, włączając wymagane i opcjonalne argumenty.  
     - **Opcje:** Lista opcji specyficznych dla polecenia wraz z ich wyjaśnieniami.  
     - **Przykłady:** Przykłady efektywnego wykonania polecenia.

  
## Użycie polecenia `check-repo-connection`

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do wskazanego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może poprawnie komunikować się z repozytorium.
      
### Składnia polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu, polecenie wyświetla potwierdzenie połączenia wraz ze szczegółami repozytorium: wersja repozytorium, host, baza danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.

## Użycie polecenia `--version`

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
### Składnia polecenia
```bash
dignacli --version
```
  
### Przykładowy wynik
```bash
dignacli version 2024.12
```

## Użycie opcji logowania
  
Domyślnie wyjście konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń pozwala na uzyskanie dodatkowych informacji, korzystając z następujących opcji:  
  
--verbose (-v)  
--debug (-d)  
--logfile (lf)  
 
„verbose” i „debug” definiują poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

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
- **USER_PASSWORD**: Hasło nowego użytkownika (wymagane).

### Opcje

- `--is_superuser`, `-su`: Flaga wyznaczająca nowego użytkownika jako administratora.
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
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). Jest to jedyny wymagany argument dla tego polecenia.

### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia spowoduje usunięcie użytkownika `jdoe` z systemu ***digna***, cofnięcie jego dostępu oraz usunięcie powiązanych danych i uprawnień z repozytorium.

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
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superużytkownika, przyznając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje aktywne bezterminowo.  
  
### Przykład
  
Aby zmienić pełne imię użytkownika `jdoe` na „Johnathan Doe” i ustawić go jako superużytkownika:
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
- **USER_PWD**: Nowe hasło użytkownika (wymagane).
  
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

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli listę wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełne imię i nazwisko, status superużytkownika oraz znaczniki czasowe wygaśnięcia.

# Zarządzanie repozytorium

### Użycie polecenia `upgrade-repo`
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. Polecenie to jest niezbędne do zastosowania aktualizacji lub do pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
### Składnia polecenia

```bash
dignacli upgrade-repo [options]
```
  
### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu, opcja ta uruchamia polecenie w trybie symulacji, który wypisuje instrukcje SQL, które zostałyby wykonane, ale ich nie wykonuje. Jest to przydatne do podglądu zmian bez modyfikowania repozytorium.  

  
### Przykład
  
Aby zaktualizować repozytorium ***digna***, możesz uruchomić polecenie bez żadnych opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są aktualne względem najnowszej wersji oprogramowania.

## Użycie polecenia `encrypt`
  
Polecenie `encrypt` w CLI ***digna*** służy do zaszyfrowania hasła.
  
### Składnia polecenia
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenty
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
### Przykład
  
Aby zaszyfrować hasło, musisz podać hasło jako argument.   
Na przykład, aby zaszyfrować hasło `mypassword123`, użyj:
```bash
dignacli encrypt mypassword123
```
To polecenie zwróci zaszyfrowaną wersję podanego hasła, którą można następnie wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd wskazujący brakujący argument.

## Użycie polecenia `generate-key`
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczenia haseł przechowywanych w repozytorium ***digna***.
  
### Składnia polecenia
```bash
dignacli generate-key
```
  
# Zarządzanie danymi

## Użycie polecenia `clean-up`

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji i danych systemu świateł drogowych (Traffic Light System) dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych przez oczyszczanie przestarzałych lub niepotrzebnych danych.

### Składnia polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia usuwania danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia usuwania danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr, który ogranicza clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla informacje pomocnicze dla polecenia clean-up i kończy działanie.
  
### Przykład
  
Aby usunąć dane z projektu ProjectA między 1 stycznia 2023 a 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią danych i zapewnia, że repozytorium zawiera jedynie istotne informacje.

## Użycie polecenia `inspect`

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji i danych systemu świateł drogowych dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitoringu danych w określonym okresie.

### Składnia polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają zostać zbadane dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie nakazuje ***digna*** iterować po wszystkich istniejących projektach i zastosować to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr, aby inspekcja objęła tylko tabele zawierające określony podciąg w nazwie.
- `--do-profile`: Wymusza ponowne zebranie profili. Domyślnie włączone (do-profile).
- `--no-do-profile`: Zapobiega ponownemu zbieraniu profili.
- `--do-prediction`: Wymusza ponowne obliczenie predykcji. Domyślnie włączone (do-prediction).
- `--no-do-prediction`: Zapobiega ponownemu obliczaniu predykcji.
- `--do-alert-status`: Wymusza ponowne obliczenie statusów alertów. Domyślnie włączone (do-alert-status).
- `--no-do-alert-status`: Zapobiega ponownemu obliczaniu statusów alertów.
- `--iterative`: Wykonuje inspekcję okresu przy użyciu iteracji dziennych. Domyślnie włączone (iterative).
- `--no-iterative`: Wykonuje inspekcję całego okresu jednorazowo.
- `--timing`, `-tm`: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
  
### Przykład
  
Aby przeprowadzić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby sprawdzić tylko konkretną tabelę i wymusić ponowne obliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest przydatne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektu.

## Użycie polecenia `tls-status`

Polecenie `tls-status` w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie na wskazaną datę. System świateł drogowych dostarcza informacji o stanie i jakości danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
### Składnia polecenia
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego sprawdzany jest status TLS (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której potrzebny jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
### Przykład
  
Aby sprawdzić status TLS dla tabeli UserData w projekcie ProjectA na dzień 1 lipca 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając jasny i praktyczny raport statusu na podstawie zdefiniowanych kryteriów.

## Użycie polecenia `list-projects`
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
### Składnia polecenia
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

## Użycie polecenia `list-ds`

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to jest przydatne do zrozumienia zasobów danych dostępnych do analizy i zarządzania w systemie ***digna***.

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
  
To polecenie daje użytkownikom przegląd źródeł danych dostępnych w projekcie, pomagając w nawigacji i zarządzaniu krajobrazem danych.