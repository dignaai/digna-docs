---
title: Konektor Teradata – Integracja baz danych | digna Dokumentacja
description: Skonfiguruj digna do połączenia z Teradata przez ODBC za pomocą ciągu połączenia bez DSN. Obejmuje sterownik ODBC Teradata, właściwość DBCNAME, mechanizmy logowania oraz ustawienia połączenia po stronie digna.
image: /assets/logo_square.png
---


# Konektor źródłowy dla Teradata

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Teradata przez **ODBC**,
używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla Teradata.

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj **ODBC Driver for Teradata** na maszynie, na której działa backend *digna*,
postępując zgodnie z oficjalną instrukcją instalacji producenta.

Sterownik rejestruje się z wersją w nazwie, na przykład
**Teradata Database ODBC Driver 20.00**. Odczytaj dokładną zarejestrowaną nazwę na swoim hoście,
jak opisano w [Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Właściwości ODBC {: #2-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika ODBC Teradata, więc ich nazwy, wartości domyślne i akceptowane wartości różnią się
    między wersjami sterownika — wersja jest częścią samej nazwy sterownika — oraz między
    platformami. Potraktuj to jako punkt wyjścia i sprawdź dokumentację zainstalowanej wersji
    sterownika.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `DRIVER` | `Teradata Database ODBC Driver 20.00` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `DBCNAME` | `teradata.example.com` | Nazwa serwera lub adres IP. Własna nazwa Teradata dla właściwości hosta |
| `UID` | `digna_source_user` | Użytkownik bazy danych |
| `PWD` | `<password>` | Zaznacz **Encrypted** |

Powstały ciąg połączenia wygląda tak:

```
DRIVER=Teradata Database ODBC Driver 20.00;DBCNAME=teradata.example.com;UID=digna_source_user;PWD=<password>
```

Przydatne dodatkowe właściwości:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `MechanismName` | `TD2` | Mechanizm logowania. `TD2` to domyślny mechanizm Teradata; użyj `LDAP` do uwierzytelniania katalogowego |
| `DefaultDatabase` | `dad` | Baza danych, w której rozpoczyna się sesja |
| `CharacterSet` | `UTF8` | Ustaw to tam, gdzie domyślny zestaw znaków sesji zniekształciłby dane spoza ASCII |

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Database for the work tables of "Permanent" profiling, e.g. "Digna_Work"
```

---

## 4. Uwagi dotyczące Teradata {: #4-notes-on-teradata }

- **Baza danych Teradata jest katalogiem, nie schematem.** *digna* wyświetla jako katalogi bazy,
  które użytkownik może zobaczyć (z `DBC.DatabasesV`), a poziom schematu nie ma zastosowania.
  Dodając źródło danych, wybierz bazę jako katalog; schemat jest zgłaszany jako *nie dotyczy*.
- **Jedno połączenie sięga do każdej dozwolonej bazy**, więc pojedyncze połączenie może
  obsługiwać źródła w wielu bazach — w odróżnieniu od technologii, w których połączenie jest
  przypisane do jednej bazy.
- **Work Schema to baza danych.** Dla profilowania *Permanent* wskaż bazę Teradata zawierającą
  tabele robocze i nadaj użytkownikowi uprawnienia `CREATE TABLE` oraz przydział przestrzeni
  `PERM` w tej bazie — baza bez przestrzeni perm nie może przechowywać tabeli.
- **Tryby profilowania.** *Permanent* tworzy tabele w **Work Schema**. *Session* używa tabeli
  `VOLATILE`, która wymaga przestrzeni `SPOOL`, ale nie wymaga przestrzeni perm ani uprawnień w
  **Work Schema**. *Standard* wymaga wyłącznie dostępu do odczytu.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale okno dialogowe
samego sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że
sterownik i Twoje poświadczenia działają.

#### Krok 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Pole **Name or IP address** odpowiada tutaj właściwości `DBCNAME` z
[sekcji 2](#2-odbc-properties).

Kliknij przycisk **Test**.

#### Krok 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Podaj nazwę użytkownika i hasło, a następnie kliknij przycisk **OK**. Ekran powodzenia
potwierdza, że sterownik i poświadczenia działają.
