---
title: digna CLI Reference 2024.11 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.11. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Ta strona dokumentuje pełen zestaw poleceń dostępnych w CLI ***digna***, wydanie **2024.11**, w tym przykłady użycia i opcje.


---
## Podstawy CLI

---

## Użycie opcji `help`

Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby użycia tej opcji:

1. **Wyświetlanie ogólnej pomocy:**
   
    Użyj –help bezpośrednio po słowie kluczowym ***digna***cl  
   ```bash
   dignacli --help
   ```

3.  **Uzyskiwanie pomocy dla konkretnych poleceń:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dołącz `--help` do tego polecenia.
    Na przykład, aby uzyskać pomoc dla polecenia `add-user`, uruchom:
     ```bash
     dignacli add-user --help
     ```

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis tego, co robi polecenie.  
     - **Składnia:** Pokazuje dokładną składnię, w tym wymagane i opcjonalne argumenty.  
     - **Opcje:** Wykaz opcji specyficznych dla polecenia wraz z ich wyjaśnieniami.  
     - **Przykłady:** Przykłady efektywnego wykonania polecenia.  

  
## Użycie polecenia `check-repo-connection`

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do określonego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może komunikować się z repozytorium.
      
### Użycie polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wyświetla potwierdzenie połączenia oraz szczegóły dotyczące repozytorium: wersję repozytorium, hosta, bazę danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnej konfiguracji.

## Użycie polecenia ‘version’

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
### Użycie polecenia
```bash
dignacli --version
```
  
### Przykładowy wynik
```bash
dignacli version 2024.11
```

## Użycie opcji logowania
  
Domyślnie wyjście konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń oferuje możliwość dostarczenia dodatkowych informacji za pomocą następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” określają poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

# Zarządzanie użytkownikami

## Użycie polecenia ‘add-user’
  
Polecenie add-user w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
### Użycie polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenty

- **USER_NAME**: Nazwa użytkownika dla nowego użytkownika (wymagane).
- **USER_FULL_NAME**: Pełna nazwa nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

### Opcje

- `--is_superuser`, `-su`: Flaga oznaczająca, że nowy użytkownik ma status administratora.
- `--valid_until`, `-vu`: Ustawia datę ważności konta użytkownika w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

### Przykład

Aby dodać nowego użytkownika o nazwie użytkownika `jdoe`, pełnej nazwie `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Użycie polecenia `delete-user`
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
### Użycie polecenia
```bash
dignacli delete-user USER_NAME
```
  
### Argumenty
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). Jest to jedyny wymagany argument dla tego polecenia.

### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia usunie użytkownika `jdoe` z systemu ***digna***, cofając jego dostęp i usuwając powiązane dane oraz uprawnienia z repozytorium.

## Użycie polecenia `modify-user`

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

### Użycie polecenia
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają być zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowa pełna nazwa użytkownika (wymagane).
  
### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superużytkownika, przyznając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
### Przykład
  
Aby zmienić pełną nazwę użytkownika `jdoe` na „Johnathan Doe” i ustawić go jako superużytkownika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Użycie polecenia `modify-user-pwd`
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła dla istniejącego użytkownika w systemie ***digna***.
  
### Użycie polecenia
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

### Użycie polecenia

```bash
dignacli list-users
```

Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełną nazwę, status superużytkownika oraz znaczniki czasowe wygaśnięcia.

# Zarządzanie repozytorium

### Użycie polecenia `upgrade-repo`
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. To polecenie jest niezbędne do zastosowania aktualizacji lub do początkowego skonfigurowania infrastruktury repozytorium.
  
### Użycie polecenia

```bash
dignacli upgrade-repo [options]
```
  
### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu ta opcja uruchamia polecenie w trybie symulacji, który wyświetla instrukcje SQL, które zostałyby wykonane, ale ich faktycznie nie wykonuje. Jest to przydatne do podglądu zmian bez wprowadzania modyfikacji w repozytorium.  

  
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
  
### Użycie polecenia
  
```bash
dignacli encrypt <PASSWORD>
```
    
### Argumenty
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
### Przykład
  
Aby zaszyfrować hasło, należy podać hasło jako argument.   
Na przykład, aby zaszyfrować hasło `mypassword123`, użyj:
```bash
dignacli encrypt mypassword123
```
To polecenie zwraca zaszyfrowaną wersję podanego hasła, która może być następnie użyta w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

## Użycie polecenia `generate-key`
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczania haseł przechowywanych w repozytorium ***digna***.
  
### Użycie polecenia
```bash
dignacli generate-key
```
  
# Zarządzanie danymi

## Użycie polecenia `clean-up`

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, prognoz oraz danych systemu sygnalizacji świetlnej (Traffic Light System) dla jednego lub większej liczby źródeł danych w określonym projekcie. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

### Użycie polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają być usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby przetworzyło wszystkie istniejące projekty i zastosowało to polecenie.
- **FROM_DATE**: Data i czas początkowy dla usuwania danych. Akceptowalne formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas końcowy dla usuwania danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtr ograniczający clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po zakończeniu.
- `--help`: Wyświetla informacje pomocy dla polecenia clean-up i kończy działanie.
  
### Przykład
  
Aby usunąć dane z projektu ProjectA między 1 stycznia 2023 a 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią danych i zapewnia, że repozytorium zawiera tylko istotne informacje.

## Użycie polecenia `inspect`

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, prognoz oraz danych systemu sygnalizacji świetlnej dla jednego lub większej liczby źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitorowaniu danych w określonym okresie.

### Użycie polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają być zbadane dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby przetworzyło wszystkie istniejące projekty i zastosowało to polecenie.
- **FROM_DATE**: Data i czas początkowy dla inspekcji danych. Akceptowalne formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas końcowy dla inspekcji danych, zgodnie z tymi samymi formatami co FROM_DATE (wymagane).
  
### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby inspekcja obejmowała tylko tabele zawierające określony podciąg w nazwie.
- `--do-profile`: Wyzwala ponowne zbieranie profili. Domyślnie do-profile jest włączone.
- `--no-do-profile`: Zapobiega ponownemu zbieraniu profili.
- `--do-prediction`: Wyzwala przeliczenie prognoz. Domyślnie do-prediction jest włączone.
- `--no-do-prediction`: Zapobiega przeliczeniu prognoz.
- `--do-alert-status`: Wyzwala ponowne obliczenie statusów alertów. Domyślnie do-alert-status jest włączone.
- `--no-do-alert-status`: Zapobiega ponownemu obliczeniu statusów alertów.
- `--timing`, `-tm`: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
  
### Przykład
  
Aby sprawdzić dane dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby skontrolować tylko konkretną tabelę i wymusić przeliczenie prognoz:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest przydatne do generowania zaktualizowanych profili i prognoz, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektu.

## Użycie polecenia `tls-status`

Polecenie `tls-status` w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie na wskazaną datę. System sygnalizacji świetlnej dostarcza informacji o kondycji i jakości danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
### Użycie polecenia
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego zapytanie o status TLS jest wykonywane (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której potrzebny jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
### Przykład
  
Aby sprawdzić status TLS dla tabeli o nazwie UserData w projekcie ProjectA w dniu 1 lipca 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając przejrzysty i praktyczny raport statusu oparty na zdefiniowanych kryteriach.

## Użycie polecenia `list-projects`
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
### Użycie polecenia
  
```bash
dignacli list-projects
```

Jest to szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

## Użycie polecenia `list-ds`

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to jest przydatne do zrozumienia aktywów danych dostępnych do analizy i zarządzania w systemie ***digna***.

### Użycie polecenia
  
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
  
To polecenie daje użytkownikom przegląd dostępnych w projekcie źródeł danych, pomagając skuteczniej poruszać się i zarządzać krajobrazem danych.