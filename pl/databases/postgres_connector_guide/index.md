# Konektor źródłowy dla PostgreSQL

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z PostgreSQL przez **ODBC**,
używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla PostgreSQL.

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj sterownik ODBC dla PostgreSQL (**psqlODBC**) na maszynie, na której działa backend
*digna*, postępując zgodnie z oficjalną instrukcją instalacji producenta.

Sterownik rejestruje się pod nazwą zależną od platformy i pakietu — najczęściej
**PostgreSQL Unicode(x64)** w systemie Windows i **PostgreSQL ODBC Driver(UNICODE)** w systemie
Linux. Odczytaj dokładną nazwę na swoim hoście, jak opisano w
[Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver), i użyj tej nazwy
dla właściwości `DRIVER` poniżej.

---

## 2. Właściwości ODBC {: #2-odbc-properties }

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika psqlODBC, więc ich nazwy, wartości domyślne i akceptowane wartości różnią się
    między wersjami sterownika i platformami, a to, czego wymaga Twój serwer — zwłaszcza w
    zakresie SSL — również może się różnić. Potraktuj to jako punkt wyjścia i sprawdź
    dokumentację zainstalowanej wersji sterownika.

Dodaj następujące właściwości w ekranie **Add DB Connection**:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `DRIVER` | `PostgreSQL ODBC Driver(UNICODE)` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `SERVER` | `db.example.com` | Nazwa serwera lub adres IP |
| `PORT` | `5432` | |
| `DATABASE` | `digna_source_db` | Baza danych zawierająca schematy źródłowe. To jedyna baza, którą to połączenie może profilować |
| `UID` | `digna_source_user` | Użytkownik bazy danych |
| `PWD` | `<password>` | Zaznacz **Encrypted** |
| `SSLMode` | `prefer` | `disable`, `allow`, `prefer`, `require`, `verify-ca` lub `verify-full` — musi być akceptowane przez serwer |

Powstały ciąg połączenia wygląda tak:

```
DRIVER=PostgreSQL ODBC Driver(UNICODE);SERVER=db.example.com;PORT=5432;DATABASE=digna_source_db;UID=digna_source_user;PWD=<password>;SSLMode=prefer
```

Każdą kolejną opcję psqlODBC można dodać jako dodatkową właściwość — na przykład `ReadOnly=1`
dla sesji tylko do odczytu albo `ConnSettings`, aby wykonać instrukcje `SET` przy nawiązywaniu
połączenia.

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Postgres
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "digna_work"
```

---

## 4. Uwagi dotyczące PostgreSQL {: #4-notes-on-postgresql }

- **`SSLMode` musi pasować do serwera.** Serwer skonfigurowany z `hostssl` odrzuca
  `SSLMode=disable`, a `verify-ca` lub `verify-full` dodatkowo wymagają, aby certyfikat główny
  był dostępny dla sterownika na hoście *digna*. Jeśli podczas testowania sterownika trzeba było
  wybrać konkretny tryb, użyj tutaj tego samego.
- **Jedno połączenie widzi jedną bazę danych.** *digna* udostępnia schematy bazy wskazanej w
  `DATABASE`, ponieważ PostgreSQL zgłasza jako katalog tylko bieżącą bazę. Tabele źródłowe w
  innej bazie wymagają własnego połączenia.
- **Tryby profilowania.** *Permanent* tworzy tabele robocze w **Work Schema**, więc użytkownik
  potrzebuje uprawnienia `CREATE` w tym schemacie. *Session* używa `CREATE TEMPORARY TABLE` i
  nie dotyka **Work Schema**. *Standard* wymaga wyłącznie dostępu do odczytu.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale okno dialogowe
samego sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że
sterownik działa, a serwer akceptuje Twoje poświadczenia i tryb SSL.

#### Krok 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

#### Krok 2 – Przetestuj połączenie

Kliknij przycisk **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

Wartości wprowadzone tutaj to dokładnie te same wartości, które przyjmują właściwości z
[sekcji 2](#2-odbc-properties).