---
title: Konektor MS SQL Server – Integracja baz danych | digna Dokumentacja
description: Skonfiguruj digna do połączenia z Microsoft SQL Server przez ODBC za pomocą ciągu połączenia bez DSN. Obejmuje sterownik ODBC Microsoft, wymagane właściwości ODBC, ustawienia szyfrowania oraz ustawienia połączenia po stronie digna.
image: /assets/logo_square.png
---


# Konektor źródłowy dla MS SQL Server

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Microsoft SQL Server przez
**ODBC**, używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla SQL Server.

!!! note "Azure Synapse Analytics"

    Synapse również konfiguruje się jako połączenie SQL Server, z inną nazwą hosta i kilkoma
    dodatkowymi kwestiami — zobacz [Azure Synapse](azure_synapse_connector_guide.md).

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj **ODBC Driver 18 for SQL Server** na maszynie, na której działa backend *digna*,
postępując zgodnie z
[instrukcją instalacji Microsoft](https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server).

Sterownik dostarczany z systemem Windows pod prostą nazwą **SQL Server** również działa, ale jest
dawno przestarzały i nie obsługuje ani nowoczesnych ustawień TLS, ani uwierzytelniania Azure.
Używaj go tylko tam, gdzie zainstalowanie aktualnego sterownika nie wchodzi w grę.

Odczytaj dokładną nazwę zarejestrowanego sterownika na swoim hoście, jak opisano w
[Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Właściwości ODBC {: #2-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika ODBC Microsoft, więc ich nazwy, wartości domyślne i akceptowane wartości różnią
    się między wersjami sterownika — Driver 18 szyfruje domyślnie, czego Driver 17 nie robił —
    oraz między platformami. Potraktuj to jako punkt wyjścia i sprawdź dokumentację
    zainstalowanej wersji sterownika.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `DRIVER` | `ODBC Driver 18 for SQL Server` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `SERVER` | `sql.example.com` | Nazwa serwera lub adres IP. Instancje nazwane: `host\instance`; port inny niż domyślny: `host,1433` |
| `PORT` | `1433` | Pomiń, gdy port jest już częścią `SERVER` |
| `DATABASE` | `digna_source_db` | Baza danych zawierająca schematy źródłowe. To jedyna baza, którą to połączenie może profilować |
| `UID` | `digna_source_user` | Użytkownik bazy danych |
| `PWD` | `<password>` | Zaznacz **Encrypted** |

Powstały ciąg połączenia wygląda tak:

```
DRIVER=ODBC Driver 18 for SQL Server;SERVER=sql.example.com;PORT=1433;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>
```

### Szyfrowanie w ODBC Driver 18

Driver 18 domyślnie szyfruje połączenia i weryfikuje certyfikat serwera. Wobec serwera z
certyfikatem, któremu host *digna* nie ufa — zwykle certyfikatem samopodpisanym — połączenie
kończy się błędem łańcucha certyfikatów. Dodaj:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Encrypt` | `yes` | Domyślne w Driver 18; ustaw `no` tylko wtedy, gdy serwer nie obsługuje TLS |
| `TrustServerCertificate` | `yes` | Pomija weryfikację certyfikatu. Wygodne w środowiskach testowych; w produkcji lepiej zainstalować certyfikat |

### Uwierzytelnianie Windows

Aby łączyć się jako konto, na którym działa usługa *digna*, zamiast za pomocą loginu SQL, usuń
`UID` i `PWD`, a dodaj:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Trusted_Connection` | `yes` | Konto usługi *digna* musi mieć uprawnienia do bazy danych |

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         SQL Server
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Uwagi dotyczące MS SQL Server {: #4-notes-on-ms-sql-server }

- **Jedno połączenie widzi jedną bazę danych.** *digna* udostępnia schematy bazy wskazanej w
  `DATABASE`, ponieważ SQL Server zgłasza jako katalog tylko bieżącą bazę. Tabele źródłowe w
  innej bazie wymagają własnego połączenia.
- **Tryby profilowania.** *Permanent* tworzy tabele robocze w **Work Schema**, więc użytkownik
  potrzebuje tam uprawnienia `CREATE TABLE`. *Session* używa lokalnych tabel tymczasowych
  (`#wt_…`) w `tempdb` i nie dotyka **Work Schema**. *Standard* wymaga wyłącznie dostępu do
  odczytu.
- **`SERVER` zawiera instancję i port.** Przy instancji nazwanej `host\instance` wymaga
  dostępności usługi SQL Server Browser; `host,port` tego unika.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale kreator samego
sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że sterownik
działa, a serwer akceptuje Twoje poświadczenia.

#### Krok 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknij przycisk **Next >**.

#### Krok 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Wybierz metodę uwierzytelniania (np. nazwa użytkownika i hasło)
i podaj wymagane dane.

Kliknij przycisk **Next >**.

#### Krok 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Wybierz ustawienia zgodne z ANSI, a następnie kliknij przycisk **Next >**.

#### Krok 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Możesz pozostawić ustawienia domyślne albo wybrać opcje rejestrowania według potrzeb
i kliknąć przycisk **Finish**.

#### Krok 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Teraz kliknij przycisk **Test datasource**.

#### Krok 6
![Step 6](images/sqlserver/create_odbc_data_source_step6.png)

Ekran powodzenia potwierdza, że sterownik i poświadczenia działają. Wprowadzone wartości to
dokładnie te same wartości, które przyjmują właściwości z [sekcji 2](#2-odbc-properties).
