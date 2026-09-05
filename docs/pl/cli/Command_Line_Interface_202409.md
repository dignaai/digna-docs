---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basics

---

###   help

Opcja --help dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby użycia tej opcji:

1. **Wyświetlenie ogólnej pomocy:**
   
    Użyj --help bezpośrednio po słowie kluczowym ***dignacli***  
   bash
   dignacli --help

3.  **Uzyskanie pomocy dla konkretnego polecenia:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dołącz --help do tego polecenia.
    Na przykład, aby otrzymać pomoc dotyczącą polecenia add-user, uruchom:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis tego, co robi dane polecenie.  
     - **Składnia:** Pokazuje dokładną składnię, włączając wymagane i opcjonalne argumenty.  
     - **Opcje:** Wymienia opcje specyficzne dla polecenia wraz z ich wyjaśnieniami.  
     - **Przykłady:** Zawiera przykłady skutecznego wykonania polecenia.

  
###   check-repo-connection

Polecenie check-repo-connection w narzędziu ***digna*** CLI służy do testowania łączności i dostępu do określonego repozytorium ***digna***. To polecenie sprawdza, czy CLI może komunikować się z repozytorium.
      
##### Command Usage
bash
dignacli check-repo-connection


Po pomyślnym wykonaniu polecenie zwraca potwierdzenie połączenia oraz szczegóły dotyczące repozytorium: wersję repozytorium, hosta, bazę danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiodło się, sprawdź plik config.toml pod kątem poprawnych ustawień konfiguracyjnych.

###   version

Aby sprawdzić zainstalowaną wersję *dignacli*, użyj opcji --version.  
  
#### Command Usage
bash
dignacli --version

  
#### Example Output
bash
dignacli version 2024.09


###   logging options
  
Domyślnie wyjście konsoli poleceń ***digna*** jest zaprojektowane jako minimalistyczne. Większość poleceń oferuje możliwość uzyskania dodatkowych informacji, używając następujących opcji:  
  
-- verbose (-v)  
-- debug (-d)  
-- logfile (lf)  
 
„verbose” i „debug” definiują poziom szczegółowości, natomiast przełącznik „logfile” pozwala przekierować wyjście do pliku zamiast wyświetlania go w oknie konsoli.

## User Management

###   add-user
  
Polecenie add-user w CLI ***digna*** służy do dodania nowego użytkownika do systemu ***digna***.
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Nazwa użytkownika nowego konta (wymagane).
- **USER_FULL_NAME**: Pełne imię i nazwisko nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło nowego użytkownika (wymagane).

#### Options

- --is_superuser, -su: Flaga wskazująca, że nowy użytkownik ma uprawnienia administratora.
- --valid_until, -vu: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

#### Example

Aby dodać nowego użytkownika o nazwie użytkownika jdoe, pełnym imieniu John Doe i haśle password123:

bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
Aby dodać nowego użytkownika i ustawić datę wygaśnięcia konta:
bash
dignacli add-user jdoe "John Doe" password123 --valid_until "2024-12-31 23:59:59"


###   delete-user
  
Polecenie delete-user w CLI ***digna*** służy do usunięcia istniejącego użytkownika z systemu ***digna***.
  
##### Command Usage
bash
dignacli delete-user USER_NAME

  
#### Arguments
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). To jedyny wymagany argument dla tego polecenia.

#### Example
bash
dignacli delete-user jdoe

  
Wykonanie tego polecenia usunie użytkownika jdoe z systemu ***digna***, cofając jego dostęp i usuwając powiązane dane oraz uprawnienia z repozytorium.

###   modify-user

Polecenie modify-user w CLI ***digna*** służy do aktualizacji danych istniejącego użytkownika w systemie ***digna***.

##### Command Usage
  
bash
dignacli modify-user <user> <USER_FULL_NAME> [options]

  
#### Arguments
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmodyfikowane (wymagane).
- **USER_FULL_NAME**: Nowe pełne imię i nazwisko użytkownika (wymagane).
  
#### Options  
  
- --is_superuser, -su: Ustawia użytkownika jako superusera, nadając mu podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- --valid_until, -vu: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
#### Example
  
Aby zmienić pełne imię użytkownika jdoe na „Johnathan Doe” i ustawić go jako superusera:
bash
dignacli modify-user jdoe "Johnathan Doe" --is_superuser


###   modify-user-pwd
  
Polecenie modify-user-pwd w CLI ***digna*** służy do zmiany hasła istniejącego użytkownika w systemie ***digna***.
  
##### Command Usage
bash
dignacli modify-user-pwd <user> <USER_PWD>

  
#### Arguments
  
- **USER_NAME**: Nazwa użytkownika, którego hasło ma zostać zmienione (wymagane).
- **USER_PWD**: Nowe hasło dla użytkownika (wymagane).
  
#### Example
  
Aby zmienić hasło użytkownika jdoe na newpassword123:
bash
dignacli modify-user-pwd jdoe newpassword123


###   list-users

Polecenie list-users w CLI ***digna*** wyświetla listę wszystkich użytkowników zarejestrowanych w systemie ***digna***.

##### Command Usage

bash
dignacli list-users


Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełne imię i nazwisko, status superusera oraz znaczniki czasu wygaśnięcia.

# Repository Management

###   upgrade-repo
  
Polecenie upgrade-repo w CLI ***digna*** służy do uaktualnienia lub inicjalizacji repozytorium ***digna***. To polecenie jest niezbędne do zastosowania aktualizacji lub do pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Po włączeniu uruchamia polecenie w trybie symulacji, które wypisuje instrukcje SQL, które zostałyby wykonane, ale ich faktycznie nie wykonuje. Jest to przydatne do podglądu zmian bez wprowadzania modyfikacji w repozytorium.  

  
#### Example
  
Aby zaktualizować repozytorium ***digna***, można uruchomić polecenie bez żadnych opcji:
  
bash
dignacli upgrade-repo
  
Aby uruchomić aktualizację w trybie symulacji (aby zobaczyć instrukcje SQL bez ich zastosowania):
  
bash
dignacli upgrade-repo --simulation-mode

  
To polecenie jest kluczowe dla utrzymania systemu ***digna***, zapewniając, że schemat bazy danych i inne komponenty repozytorium są zgodne z najnowszą wersją oprogramowania.

###   encrypt
  
Polecenie encrypt w CLI ***digna*** służy do zaszyfrowania hasła.
  
#### Command Usage
  
bash
dignacli encrypt <PASSWORD>

    
#### Arguments
- **PASSWORD**: Hasło, które ma zostać zaszyfrowane (wymagane).
  
#### Example
  
Aby zaszyfrować hasło, należy przekazać je jako argument.   
Na przykład, aby zaszyfrować hasło mypassword123, użyj:
bash
dignacli encrypt mypassword123

To polecenie zwraca zaszyfrowaną wersję podanego hasła, którą można następnie wykorzystać w bezpiecznych kontekstach. Jeśli argument hasła nie zostanie podany, CLI wyświetli błąd informujący o brakującym argumencie.

###   generate-key
  
Polecenie generate-key służy do wygenerowania klucza Fernet, który jest niezbędny do zabezpieczenia haseł przechowywanych w repozytorium ***digna***.
  
#### Command Usage
bash
dignacli generate-key

  
## Data Management

###   clean-up

Polecenie clean-up w CLI ***digna*** służy do usuwania profili, prognoz i danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. To polecenie jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają zostać usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie powoduje, że ***digna*** przeiteruje po wszystkich istniejących projektach i zastosuje to polecenie.
- **FROM_DATE**: Data i czas rozpoczęcia usuwania danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia usuwania danych, w tych samych formatach co FROM_DATE (wymagane).
  
#### Options
  
- --table-name, -tn: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- --table-filter, -tf: Filtr ograniczający clean-up do tabel zawierających określony podciąg w nazwie.
- --timing, -tm: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- --help: Wyświetla informacje pomocnicze dotyczące polecenia clean-up i kończy działanie.
  
#### Example
  
Aby usunąć dane z projektu ProjectA między 1 stycznia 2023 a 30 czerwca 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Aby usunąć dane tylko z konkretnej tabeli o nazwie Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
To polecenie pomaga w zarządzaniu przestrzenią danych i zapewnieniu, że repozytorium zawiera tylko istotne informacje.

###   inspect

Polecenie inspect w CLI ***digna*** służy do tworzenia profili, prognoz i danych systemu sygnalizacji świetlnej dla jednego lub więcej źródeł danych w określonym projekcie. To polecenie pomaga w analizie i monitorowaniu danych w określonym przedziale czasowym.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają być analizowane dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie powoduje, że ***digna*** przeiteruje po wszystkich istniejących projektach i zastosuje to polecenie.
- **FROM_DATE**: Data i czas rozpoczęcia inspekcji danych. Akceptowalne formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i czas zakończenia inspekcji danych, w tych samych formatach co FROM_DATE (wymagane).
  
#### Options

- --table-name, -tn: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- --table-filter, -tf: Filtruje, aby sprawdzać tylko tabele zawierające określony podciąg w nazwie.
- --force-profile: Wymusza ponowne pobranie profili. Domyślnie jest włączone force-profile.
- --no-force-profile: Zapobiega ponownemu pobraniu profili.
- --force-prediction: Wymusza ponowne obliczenie prognoz. Domyślnie jest włączone force-prediction.
- --no-force-prediction: Zapobiega ponownemu obliczeniu prognoz.
- --force-alert-status: Wymusza ponowne obliczenie statusów alertów. Domyślnie jest włączone force-alert-status.
- --no-force-alert-status: Zapobiega ponownemu obliczeniu statusów alertów.
- --timing, -tm: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
- --alert-notification, -an: Wysyła powiadomienia o alertach do subskrybowanych kanałów.
  
#### Example
  
Aby przeprowadzić inspekcję danych dla projektu ProjectA od 1 stycznia 2024 do 31 stycznia 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Aby sprawdzić tylko konkretną tabelę i wymusić ponowne obliczenie prognoz:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

To polecenie jest przydatne do generowania zaktualizowanych profili i prognoz, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym dla projektu.

###   tls-status

Polecenie tls-status w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie na wskazaną datę. Traffic Light System dostarcza informacji o stanie zdrowia i jakości danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, dla którego sprawdzany jest status TLS (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której potrzebny jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
#### Example
  
Aby sprawdzić status TLS dla tabeli o nazwie UserData w projekcie ProjectA w dniu 1 lipca 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając czytelny i praktyczny raport statusu oparty na zdefiniowanych kryteriach.

###   list-projects
  
Polecenie list-projects w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
#### Command Usage
  
bash
dignacli list-projects


To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

###   list-ds

Polecenie list-ds w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. To polecenie jest przydatne do zrozumienia zasobów danych dostępnych do analizy i zarządzania w systemie ***digna***.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Nazwa projektu, dla którego wyświetlane są źródła danych (wymagane).
  
#### Example
  
Aby wyświetlić wszystkie źródła danych w projekcie o nazwie ProjectA:
  
bash
dignacli list-ds ProjectA

  
To polecenie daje użytkownikom przegląd dostępnych źródeł danych w projekcie, pomagając w nawigacji i zarządzaniu krajobrazem danych.