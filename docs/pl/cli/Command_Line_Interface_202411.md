---
title: digna CLI Reference 2024.11 – Polecenia i przykłady | digna Documentation
description: Kompletny przewodnik po digna CLI w wersji 2024.11. Dowiedz się, jak zarządzać użytkownikami, repozytoriami i danymi za pomocą poleceń takich jak add-user, check-repo-connection, upgrade-repo, inspect, tls-status i innych.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202411/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.11
**2024-11-03**

Ta strona dokumentuje pełny zestaw poleceń dostępnych w CLI ***digna*** w wydaniu **2024.11**, włącznie z przykładami użycia i opcjami.


---
## Podstawy CLI

---

## Używanie opcji `--help`

Opcja `--help` dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby korzystania z tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj `--help` bezpośrednio po poleceniu `dignacli`  
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
     - **Opcje:** Lista opcji specyficznych dla polecenia wraz z ich wyjaśnieniami.  
     - **Przykłady:** Przykłady efektywnego wykonania polecenia.

  
## Używanie polecenia `check-repo-connection`

Polecenie `check-repo-connection` jest narzędziem w CLI ***digna*** służącym do testowania łączności i dostępu do określonego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może komunikować się z repozytorium.
      
### Składnia polecenia
```bash
dignacli check-repo-connection
```

Po pomyślnym wykonaniu polecenie wyświetla potwierdzenie połączenia oraz szczegóły dotyczące repozytorium: wersję repozytorium, hosta, bazę danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiedzie się, sprawdź plik config.toml pod kątem poprawnej konfiguracji.

## Używanie polecenia `--version`

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji `--version`.  
  
### Składnia polecenia
```bash
dignacli --version
```
  
### Przykładowe wyjście
```bash
dignacli version 2024.11
```

## Używanie opcji logowania
  
Domyślnie wyjście konsolekowe poleceń ***digna*** jest zwięzłe. Większość poleceń daje możliwość uzyskania dodatkowych informacji, używając następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” określają poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast do okna konsoli.

# Zarządzanie użytkownikami

## Używanie polecenia `add-user`
  
Polecenie `add-user` w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
### Składnia polecenia
```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
### Argumenty

- **USER_NAME**: Nazwa użytkownika nowego konta (wymagane).
- **USER_FULL_NAME**: Pełna nazwa nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło nowego użytkownika (wymagane).

### Opcje

- `--is_superuser`, `-su`: Flaga nadająca nowemu użytkownikowi uprawnienia administratora.
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie `YYYY-MM-DD HH:MI:SS`. Jeśli nie jest ustawiona, konto nie ma daty wygaśnięcia.

### Przykład

Aby dodać nowego użytkownika o nazwie `jdoe`, pełnej nazwie `John Doe` i haśle `password123`:

```bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD
```
  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
```bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"
```

## Używanie polecenia `delete-user`
  
Polecenie `delete-user` w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
### Składnia polecenia
```bash
dignacli delete-user USER_NAME
```
  
### Argumenty
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). To jedyny wymagany argument dla tego polecenia.

### Przykład
```bash
dignacli delete-user jdoe
```
  
Wykonanie tego polecenia usunie użytkownika `jdoe` z systemu ***digna***, cofając jego dostęp i usuwając powiązane uprawnienia oraz dane z repozytorium.

## Używanie polecenia `modify-user`

Polecenie `modify-user` w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

### Składnia polecenia
  
```bash
dignacli modify-user <USER_NAME> <USER_FULL_NAME> [options]
```
  
### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmienione (wymagane).
- **USER_FULL_NAME**: Nowa pełna nazwa użytkownika (wymagane).
  
### Opcje  
  
- `--is_superuser`, `-su`: Ustawia użytkownika jako superużytkownika, nadając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- `--valid_until`, `-vu`: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
### Przykład
  
Aby zmodyfikować pełną nazwę użytkownika `jdoe` na „Johnathan Doe” i ustawić go jako superużytkownika:
```bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser
```

## Używanie polecenia `modify-user-pwd`
  
Polecenie `modify-user-pwd` w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
### Składnia polecenia
```bash
dignacli modify-user-pwd <USER_NAME> <USER_PWD>
```
  
### Argumenty
  
- **USER_NAME**: Nazwa użytkownika, dla którego ma zostać zmienione hasło (wymagane).
- **USER_PWD**: Nowe hasło użytkownika (wymagane).
  
### Przykład
  
Aby zmienić hasło użytkownika `jdoe` na `newpassword123`:
```bash
dignacli modify-user-pwd jdoe newpassword123
```

## Używanie polecenia `list-users`

Polecenie `list-users` w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

### Składnia polecenia

```bash
dignacli list-users
```

Wykonanie tego polecenia spowoduje połączenie z repozytorium ***digna*** i wyświetlenie wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełną nazwę, status superużytkownika oraz znaczniki czasowe wygaśnięcia.

# Zarządzanie repozytorium

### Używanie polecenia `upgrade-repo`
  
Polecenie `upgrade-repo` w CLI ***digna*** służy do uaktualnienia lub inicjalizacji repozytorium ***digna***. Polecenie to jest niezbędne do zastosowania aktualizacji lub do przygotowania infrastruktury repozytorium przy pierwszym uruchomieniu.
  
### Składnia polecenia

```bash
dignacli upgrade-repo [options]
```
  
### Opcje
  
- `--simulation-mode`, `-s`: Po włączeniu to polecenie działa w trybie symulacji, drukując instrukcje SQL, które zostałyby wykonane, ale nie wykonuje ich faktycznie. Przydatne do podglądu zmian bez modyfikowania repozytorium.  

  
### Przykład
  
Aby zaktualizować repozytorium ***digna***, możesz uruchomić polecenie bez opcji:
  
```bash
dignacli upgrade-repo
```  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
```bash
dignacli upgrade-repo --simulation-mode
```
  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są zgodne z najnowszą wersją oprogramowania.

## Używanie polecenia `encrypt`
  
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
Polecenie zwróci zaszyfrowaną wersję podanego hasła, która może być użyta w bezpiecznych kontekstach. Jeśli argument z hasłem nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

## Używanie polecenia `generate-key`
  
Polecenie `generate-key` służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczenia haseł przechowywanych w repozytorium ***digna***.
  
### Składnia polecenia
```bash
dignacli generate-key
```
  
# Zarządzanie danymi

## Używanie polecenia `clean-up`

Polecenie `clean-up` w CLI ***digna*** służy do usuwania profili, predykcji oraz danych Traffic Light System dla jednego lub więcej źródeł danych w obrębie określonego projektu. Polecenie to jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać porządek i wydajność poprzez usuwanie przestarzałych lub niepotrzebnych danych.

### Składnia polecenia

```bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego `all-projects` w tym argumencie instruuje ***digna***, aby iterowało po wszystkich istniejących projektach i zastosowało polecenie dla każdego z nich.
- **FROM_DATE**: Data i czas rozpoczęcia usuwania danych. Akceptowane formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia usuwania danych, w tych samych formatach co FROM_DATE (wymagane).
  
### Opcje
  
- `--table-name`, `-tn`: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, ograniczając clean-up do tabel zawierających określony podciąg w nazwie.
- `--timing`, `-tm`: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- `--help`: Wyświetla informacje pomocy dla polecenia clean-up i kończy działanie.
  
### Przykład
  
Aby usunąć dane z projektu ProjectA w okresie od 1 stycznia 2023 do 30 czerwca 2023:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30
```
  
Aby usunąć dane tylko z konkretnej tabeli o nazwie `Table1`:
  
```bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1
```
  
To polecenie pomaga w zarządzaniu przestrzenią danych i zapewnianiu, że repozytorium zawiera tylko istotne informacje.

## Używanie polecenia `inspect`

Polecenie `inspect` w CLI ***digna*** służy do tworzenia profili, predykcji oraz danych Traffic Light System dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitorowaniu danych w zdefiniowanym okresie.

### Składnia polecenia

```bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają zostać przeprowadzone inspekcje danych (wymagane). Użycie słowa kluczowego `all-projects` w tym argumencie instruuje ***digna***, aby iterowało po wszystkich istniejących projektach i zastosowało polecenie dla każdego z nich.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji. Akceptowane formaty obejmują %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji, w tych samych formatach co FROM_DATE (wymagane).
  
### Opcje

- `--table-name`, `-tn`: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- `--table-filter`, `-tf`: Filtruje, aby inspekcja dotyczyła jedynie tabel zawierających określony podciąg w nazwie.
- `--do-profile`: Wymusza ponowne zebranie profili. Domyślnie do-profile jest włączone.
- `--no-do-profile`: Zapobiega ponownemu zbieraniu profili.
- `--do-prediction`: Wymusza ponowne obliczenie predykcji. Domyślnie do-prediction jest włączone.
- `--no-do-prediction`: Zapobiega ponownemu obliczaniu predykcji.
- `--do-alert-status`: Wymusza ponowne obliczenie statusów alertów. Domyślnie do-alert-status jest włączone.
- `--no-do-alert-status`: Zapobiega ponownemu obliczaniu statusów alertów.
- `--timing`, `-tm`: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
  
### Przykład
  
Aby przeprowadzić inspekcję danych dla projektu `ProjectA` od 1 stycznia 2024 do 31 stycznia 2024:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31
```
  
Aby przeprowadzić inspekcję tylko dla konkretnej tabeli i wymusić przeliczenie predykcji:
  
```bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction
```
To polecenie jest przydatne do generowania zaktualizowanych profili i predykcji, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektów.

## Używanie polecenia `tls-status`

Polecenie `tls-status` w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie na podaną datę. Traffic Light System dostarcza informacji o stanie i jakości danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
### Składnia polecenia
  
```bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>
```
  
### Argumenty
  
- **PROJECT_NAME**: Nazwa projektu, dla którego sprawdzany jest status TLS (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której wymagany jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
### Przykład
  
Aby sprawdzić status TLS dla tabeli o nazwie UserData w projekcie ProjectA na dzień 1 lipca 2024:

```bash
dignacli tls-status ProjectA UserData 2024-07-01
```

To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając jasny i użyteczny raport statusu oparty na zdefiniowanych kryteriach.

## Używanie polecenia `list-projects`
  
Polecenie `list-projects` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
### Składnia polecenia
  
```bash
dignacli list-projects
```

To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

## Używanie polecenia `list-ds`

Polecenie `list-ds` w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to jest pomocne w zrozumieniu zasobów danych dostępnych do analizy i zarządzania w systemie ***digna***.

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
  
To polecenie daje użytkownikom przegląd dostępnych źródeł danych w projekcie, ułatwiając nawigację i zarządzanie obszarem danych.