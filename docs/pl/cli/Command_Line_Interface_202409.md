---
title: digna CLI Reference 2024.09 – Commands & Examples | digna Documentation
description: Complete reference for digna CLI release 2024.09. Learn how to manage users, repositories, and data with commands such as add-user, check-repo-connection, upgrade-repo, inspect, tls-status, and more.
canonical_url: https://docs.digna.ai/cli/Command_Line_Interface_202408/
image: /assets/logo_square.png
---

# digna CLI Reference 2024.09
**2024-08-24**

---

## CLI Basics

---

###   help

Opcja --help dostarcza informacji o dostępnych poleceniach i ich użyciu. Istnieją dwa główne sposoby użycia tej opcji:

1. **Wyświetlanie pomocy ogólnej:**
   
    Użyj --help bezpośrednio po słowie kluczowym ***digna***cl  
   bash
   dignacli --help

3.  **Uzyskanie pomocy dla konkretnych poleceń:**  
  
    Aby uzyskać szczegółowe informacje o konkretnym poleceniu, dołącz --help do tego polecenia.
    Na przykład, aby otrzymać pomoc dla polecenia add-user, uruchom:
     bash
     dignacli add-user --help
     

     ### output:
      
     - **Opis polecenia:** Szczegółowy opis działania polecenia.  
     - **Składnia:** Pokazuje dokładną składnię, w tym argumenty wymagane i opcjonalne.  
     - **Opcje:** Wymienia opcje specyficzne dla polecenia wraz z ich wyjaśnieniami.  
     - **Przykłady:** Zawiera przykłady efektywnego wykonania polecenia.

  
###   check-repo-connection

Polecenie check-repo-connection jest narzędziem w CLI ***digna*** służącym do przetestowania łączności i dostępu do wskazanego repozytorium ***digna***. Polecenie to sprawdza, czy CLI może komunikować się z repozytorium.
      
##### Command Usage
bash
dignacli check-repo-connection


Po pomyślnym wykonaniu polecenie wyświetla potwierdzenie połączenia oraz szczegóły dotyczące repozytorium: wersję repozytorium, hosta, bazę danych i schemat.  
  
Jeśli połączenie z repozytorium nie powiodło się, sprawdź plik config.toml, czy ustawienia konfiguracyjne są poprawne.

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
 
„verbose” i „debug” określają poziom szczegółowości, natomiast przełącznik „logfile” umożliwia przekierowanie wyjścia do pliku zamiast wyświetlania go w konsoli.

## User Management

###   add-user
  
Polecenie add-user w CLI ***digna*** służy do dodawania nowego użytkownika do systemu ***digna***.
  
#### Command Usage
bash
dignacli add-user [OPTIONS] USER_NAME USER_FULL_NAME USER_PASSWORD

  
#### Arguments

- **USER_NAME**: Nazwa użytkownika dla nowego konta (wymagane).
- **USER_FULL_NAME**: Pełne imię i nazwisko nowego użytkownika (wymagane).
- **USER_PASSWORD**: Hasło dla nowego użytkownika (wymagane).

#### Options

- --is_superuser, -su: Flaga, która wyznacza nowego użytkownika jako administratora.
- --valid_until, -vu: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie ustawiona, konto nie ma daty wygaśnięcia.

#### Example

Aby dodać nowego użytkownika o nazwie jdoe, pełnym imieniu John Doe i haśle password123:

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
- **USER_NAME**: Nazwa użytkownika, który ma zostać usunięty (wymagane). Jest to jedyny wymagany argument tego polecenia.

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
  
- **USER_NAME**: Nazwa użytkownika, którego dane mają zostać zmienione (wymagane).
- **USER_FULL_NAME**: Nowe pełne imię i nazwisko użytkownika (wymagane).
  
#### Options  
  
- --is_superuser, -su: Ustawia użytkownika jako superużytkownika, przyznając podwyższone uprawnienia. Ta flaga nie wymaga wartości.  
- --valid_until, -vu: Ustawia datę wygaśnięcia konta w formacie YYYY-MM-DD HH:MI:SS. Jeśli nie zostanie podana, konto pozostaje ważne bezterminowo.  
  
#### Example
  
Aby zmodyfikować pełne imię użytkownika jdoe na „Johnathan Doe” i ustawić go jako superużytkownika:
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


Wykonanie tego polecenia w CLI ***digna*** połączy się z repozytorium ***digna*** i wyświetli wszystkich użytkowników, pokazując ich ID, nazwę użytkownika, pełne imię i nazwisko, status superużytkownika oraz znaczniki daty wygaśnięcia.

# Repository Management

###   upgrade-repo
  
Polecenie upgrade-repo w CLI ***digna*** służy do aktualizacji lub inicjalizacji repozytorium ***digna***. To polecenie jest niezbędne do zastosowania aktualizacji lub do pierwszorazowego skonfigurowania infrastruktury repozytorium.
  
#### Command Usage

bash
dignacli upgrade-repo [options]

  
#### Options
  
- --simulation-mode, -s: Po włączeniu uruchamia polecenie w trybie symulacji, które wypisuje instrukcje SQL, które zostałyby wykonane, ale ich nie wykonuje. Przydatne do podglądu zmian bez modyfikowania repozytorium.  

  
#### Example
  
Aby zaktualizować repozytorium ***digna***, można uruchomić polecenie bez żadnych opcji:
  
bash
dignacli upgrade-repo
  
Aby uruchomić aktualizację w trybie symulacji (zobaczyć instrukcje SQL bez ich zastosowania):
  
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
  
Aby zaszyfrować hasło, musisz podać hasło jako argument.   
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

Polecenie clean-up w CLI ***digna*** służy do usuwania profili, prognoz i danych Traffic Light System dla jednego lub więcej źródeł danych w określonym projekcie. To polecenie jest istotne dla zarządzania cyklem życia danych, pomagając utrzymać uporządkowane i wydajne środowisko danych poprzez usuwanie przestarzałych lub niepotrzebnych danych.

#### Command Usage

bash
dignacli clean-up <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, z którego mają być usunięte dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby iterowało po wszystkich istniejących projektach i zastosowało to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia usuwania danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia usuwania danych, zgodne z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Options
  
- --table-name, -tn: Ogranicza operację clean-up do konkretnej tabeli w projekcie.
- --table-filter, -tf: Filtr ograniczający clean-up do tabel zawierających określony podciąg w nazwie.
- --timing, -tm: Wyświetla czas trwania procesu clean-up po jego zakończeniu.
- --help: Wyświetla informacje pomocnicze dla polecenia clean-up i kończy działanie.
  
#### Example
  
Aby usunąć dane z projektu ProjectA w okresie między 1 stycznia 2023 a 30 czerwca 2023:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30

  
Aby usunąć dane tylko z określonej tabeli o nazwie Table1:
  
bash
dignacli clean-up ProjectA 2023-01-01 2023-06-30 --table-name Table1

  
To polecenie pomaga zarządzać przestrzenią danych i zapewnia, że w repozytorium pozostają wyłącznie istotne informacje.

###   inspect

Polecenie inspect w CLI ***digna*** służy do tworzenia profili, prognoz i danych Traffic Light System dla jednego lub więcej źródeł danych w określonym projekcie. Polecenie to pomaga w analizie i monitorowaniu danych w zadanym okresie.

#### Command Usage

bash
dignacli inspect <PROJECT_NAME> <FROM_DATE> <TO_DATE> [options]

  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, dla którego mają być inspectowane dane (wymagane). Użycie słowa kluczowego all-projects w tym argumencie instruuje ***digna***, aby iterowało po wszystkich istniejących projektach i zastosowało to polecenie.
- **FROM_DATE**: Data i godzina rozpoczęcia inspekcji danych. Akceptowane formaty to %Y-%m-%d, %Y-%m-%dT%H:%M:%S lub %Y-%m-%d %H:%M:%S (wymagane).
- **TO_DATE**: Data i godzina zakończenia inspekcji danych, zgodna z tymi samymi formatami co FROM_DATE (wymagane).
  
#### Options

- --table-name, -tn: Ogranicza inspekcję do konkretnej tabeli w projekcie.
- --table-filter, -tf: Filtruje, aby inspectować tylko tabele zawierające określony podciąg w nazwie.
- --force-profile: Wymusza ponowne zbieranie profili. Domyślnie jest force-profile.
- --no-force-profile: Zapobiega ponownemu zbieraniu profili.
- --force-prediction: Wymusza ponowne obliczenie prognoz. Domyślnie jest force-prediction.
- --no-force-prediction: Zapobiega ponownemu obliczeniu prognoz.
- --force-alert-status: Wymusza ponowne obliczenie statusów alertów. Domyślnie jest force-alert-status.
- --no-force-alert-status: Zapobiega ponownemu obliczeniu statusów alertów.
- --timing, -tm: Wyświetla czas trwania procesu inspekcji po jego zakończeniu.
- --alert-notification, -an: Wysyła powiadomienia o alertach do subskrybowanych kanałów.
  
#### Example
  
Aby inspectować dane dla projektu ProjectA od 1 stycznia 2024 do 31 stycznia 2024:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31

  
Aby inspectować tylko konkretną tabelę i wymusić ponowne obliczenie prognoz:
  
bash
dignacli inspect ProjectA 2024-01-01 2024-01-31 --table-name Table1 --force-prediction

To polecenie jest przydatne do generowania zaktualizowanych profili i prognoz, monitorowania integralności danych oraz zarządzania systemem alertów w określonym przedziale czasowym projektu.

###   tls-status

Polecenie tls-status w CLI ***digna*** służy do zapytania o status Traffic Light System (TLS) dla konkretnej tabeli w projekcie na wskazaną datę. Traffic Light System dostarcza informacji o kondycji i jakości danych, wskazując ewentualne problemy lub alerty wymagające uwagi.
  
#### Command Usage
  
bash
dignacli tls-status <PROJECT_NAME> <TABLE_NAME> <DATE>

  
#### Arguments
  
- **PROJECT_NAME**: Nazwa projektu, dla którego zapytanie o status TLS jest wykonywane (wymagane).
- **TABLE_NAME**: Konkretna tabela w projekcie, dla której potrzebny jest status TLS (wymagane).
- **DATE**: Data, dla której sprawdzany jest status TLS, zwykle w formacie %Y-%m-%d (wymagane).
  
#### Example
  
Aby sprawdzić status TLS dla tabeli o nazwie UserData w projekcie ProjectA w dniu 1 lipca 2024:

bash
dignacli tls-status ProjectA UserData 2024-07-01


To polecenie pomaga użytkownikom monitorować i utrzymywać jakość danych, dostarczając przejrzystego i możliwego do działania raportu statusu opartego na zdefiniowanych kryteriach.

###   list-projects
  
Polecenie list-projects w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych projektów w systemie ***digna***.
  
#### Command Usage
  
bash
dignacli list-projects


To polecenie jest szczególnie przydatne dla administratorów i użytkowników zarządzających wieloma projektami, zapewniając szybki przegląd dostępnych projektów w repozytorium ***digna***.

###   list-ds

Polecenie list-ds w CLI ***digna*** służy do wyświetlenia listy wszystkich dostępnych źródeł danych w określonym projekcie. Polecenie to pomaga zrozumieć zasoby danych dostępne do analizy i zarządzania w systemie ***digna***.

#### Command Usage
  
bash
dignacli list-ds <PROJECT_NAME>


#### Arguments
- **PROJECT_NAME**: Nazwa projektu, dla którego wyświetlane są źródła danych (wymagane).
  
#### Example
  
Aby wyświetlić wszystkie źródła danych w projekcie o nazwie ProjectA:
  
bash
dignacli list-ds ProjectA

  
To polecenie daje użytkownikom przegląd źródeł danych dostępnych w projekcie, ułatwiając poruszanie się i zarządzanie krajobrazem danych.