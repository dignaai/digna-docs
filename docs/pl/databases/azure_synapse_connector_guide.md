---
title: Konektor Azure Synapse – Integracja baz danych | digna Dokumentacja
description: Skonfiguruj digna do połączenia z Azure Synapse Analytics przez ODBC za pomocą ciągu połączenia bez DSN. Obsługuje bezserwerowe i dedykowane pule SQL, wraz z wymaganymi właściwościami ODBC i ustawieniami połączenia po stronie digna.
image: /assets/logo_square.png
---


# Konektor źródłowy dla Azure Synapse Analytics

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Azure Synapse Analytics przez
**ODBC**, używając ciągu połączenia **bez DSN**. Obsługiwane są zarówno bezserwerowe, jak i
dedykowane pule SQL.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla Azure Synapse.

!!! note "Technologia"

    Synapse posługuje się dialektem SQL Server, więc połączenie tworzy się z **Technology:
    SQL Server**. Dla serwera lokalnego zobacz [MS SQL Server](sqlserver_connector_guide.md).

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj **ODBC Driver 18 for SQL Server** na maszynie, na której działa backend *digna*,
postępując zgodnie z
[instrukcją instalacji Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server),
i odczytaj dokładną nazwę zarejestrowanego sterownika na swoim hoście, jak opisano w
[Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Właściwości ODBC {: #2-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika ODBC Microsoft, więc ich nazwy, wartości domyślne i akceptowane wartości różnią
    się między wersjami sterownika i platformami, a to, czego wymaga obszar roboczy, zależy od
    jego konfiguracji — typu puli, metody uwierzytelniania, zapory. Potraktuj to jako punkt
    wyjścia i sprawdź dokumentację zainstalowanej wersji sterownika.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `SERVER` | `<workspace>-ondemand.sql.azuresynapse.net` | Nazwa obszaru roboczego wraz z sufiksem punktu końcowego — patrz niżej |
| `DATABASE` | `dignadata` | Baza danych zawierająca schematy źródłowe. To jedyna baza, którą to połączenie może profilować |
| `UID` | `sqladminuser` | Login SQL |
| `PWD` | `<password>` | Zaznacz **Encrypted** |

Powstały ciąg połączenia wygląda tak:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=<workspace>-ondemand.sql.azuresynapse.net;DATABASE=dignadata;UID=sqladminuser;PWD=<password>
```

### Wartość `SERVER`

Weź nazwę obszaru roboczego Synapse i dołącz sufiks punktu końcowego:

| Pula | `SERVER` |
|---|---|
| **Bezserwerowa pula SQL** | `<workspace>-ondemand.sql.azuresynapse.net` |
| **Dedykowana pula SQL** | `<workspace>.sql.azuresynapse.net` |

!!! warning "Fragment `-ondemand` łatwo przeoczyć"

    Bez niego nazwa rozwiązuje się do punktu końcowego dedykowanego, a połączenie albo zawodzi,
    albo po cichu trafia do innej puli niż zamierzona. Oba punkty końcowe są widoczne na stronie
    przeglądu obszaru roboczego w portalu Azure.

### Zapora

Zapora obszaru roboczego Synapse musi zezwalać na adres wychodzący hosta *digna*. Dodaj go w
sekcji **Networking** w obszarze roboczym przed przetestowaniem połączenia — zablokowany adres
objawia się jako przekroczenie limitu czasu połączenia, a nie jako błąd uwierzytelniania.

### Uwierzytelnianie Microsoft Entra ID

Zamiast loginu SQL sterownik może uwierzytelniać się względem Entra ID. Zastąp `UID`/`PWD`
metodą uwierzytelniania, której oczekuje Twój obszar roboczy, na przykład:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Authentication` | `ActiveDirectoryServicePrincipal` | `UID` przyjmuje wtedy identyfikator aplikacji (klienta), a `PWD` klucz tajny klienta |
| `Authentication` | `ActiveDirectoryMSI` | Tożsamość zarządzana hosta *digna*, bez potrzeby poświadczeń |

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Serverless SQL pool: Standard
                    Dedicated SQL pool:  Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Uwagi dotyczące Azure Synapse {: #4-notes-on-azure-synapse }

- **Pule bezserwerowe obsługują wyłącznie profilowanie *Standard*.** Bezserwerowa pula SQL nie
  może tworzyć tabel w bazie danych, więc nie da się uruchomić ani profilowania *Permanent*, ani
  *Session*. *Standard* oblicza metryki bezpośrednio na źródle, co jest również tańszą opcją,
  ponieważ rozwiązanie bezserwerowe rozliczane jest według przetworzonych danych.
- **Jedno połączenie widzi jedną bazę danych.** *digna* udostępnia schematy bazy wskazanej w
  `DATABASE`, ponieważ Synapse, podobnie jak SQL Server, zgłasza jako katalog tylko bieżącą
  bazę.
- **Szyfrowanie jest domyślnie włączone** w Driver 18, a punkty końcowe Synapse przedstawiają
  ważne certyfikaty publiczne, więc właściwość `Encrypt` ani `TrustServerCertificate` nie jest
  potrzebna.
- **Bezserwerowy punkt końcowy może wybudzać się ze stanu bezczynności** przy pierwszym
  połączeniu. Jeśli test połączenia przekroczy limit czasu na puli nieużywanej od dłuższego
  czasu, ponów go.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale kreator samego
sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że sterownik
działa, a obszar roboczy akceptuje Twoje poświadczenia.

#### Krok 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Wypełnij pole „Server”.
Użyj nazwy obszaru roboczego Synapse i rozszerz ją o „.sql.azuresynapse.net”.  
**Uwaga**: jeśli chcesz łączyć się przez bezserwerową pulę SQL, pamiętaj o dodaniu „-ondemand”,
jak pokazano na zrzucie ekranu powyżej.

Kliknij przycisk **Next >**.

#### Krok 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Wybierz metodę uwierzytelniania (np. nazwa użytkownika i hasło)
i podaj wymagane dane.

Kliknij przycisk **Next >**.

#### Krok 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Wybierz ustawienia zgodne z ANSI, a następnie kliknij przycisk **Next >**.

#### Krok 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Możesz pozostawić ustawienia domyślne albo wybrać opcje według potrzeb
i kliknąć przycisk **Finish**.

#### Krok 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Teraz kliknij przycisk **Test datasource**.

#### Krok 6
![Step 6](images/azure_synapse/create_odbc_data_source_step6.png)

Ekran powodzenia potwierdza, że sterownik, punkt końcowy i poświadczenia działają. Wprowadzone
wartości to dokładnie te same wartości, które przyjmują właściwości z
[sekcji 2](#2-odbc-properties).
