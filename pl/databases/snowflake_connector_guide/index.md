# Konektor źródłowy dla Snowflake

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia ze Snowflake przez **ODBC**,
używając ciągu połączenia **bez DSN**.

Część konfiguracji po stronie digna jest taka sama dla każdej technologii — gdzie tworzy się
połączenia, jak szyfrowane są wartości właściwości, jak testuje się połączenie i co oznaczają
tryby profilowania. Opisano to w
[Przeglądzie połączeń z bazami danych](overview.md). Ta strona omawia to, co jest specyficzne
dla Snowflake.

---

## 1. Zainstaluj sterownik ODBC {: #1-install-the-odbc-driver }

Zainstaluj **Snowflake ODBC Driver** na maszynie, na której działa backend *digna*, postępując
zgodnie z
[instrukcją instalacji Snowflake](https://docs.snowflake.com/en/developer-guide/odbc/odbc).

Sterownik rejestruje się jako **SnowflakeDSIIDriver**. Odczytaj dokładną zarejestrowaną nazwę na
swoim hoście, jak opisano w
[Instalacji sterownika ODBC na hoście digna](overview.md#install-the-driver).

---

## 2. Właściwości ODBC {: #2-odbc-properties }

Do Snowflake sięga się za pomocą **programowego tokenu dostępu (PAT)** — ścieżki
uwierzytelniania, względem której *digna* jest zweryfikowana, i tej, której Snowflake wymaga dla
kont z zablokowanym logowaniem wyłącznie hasłem.

!!! important "Przykład, nie specyfikacja"

    Poniższy zestaw to jedna z kombinacji, o których wiadomo, że działają. Właściwości należą do
    sterownika ODBC Snowflake, więc ich nazwy, wartości domyślne i akceptowane wartości różnią
    się między wersjami sterownika i platformami, a o tym, jakie opcje uwierzytelniania
    dopuszcza Twoje konto, decyduje jego polityka bezpieczeństwa. Potraktuj to jako punkt
    wyjścia i sprawdź dokumentację zainstalowanej wersji sterownika.

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Driver` | `{SnowflakeDSIIDriver}` | Musi odpowiadać nazwie sterownika zarejestrowanej na hoście *digna* |
| `Server` | `<account>.snowflakecomputing.com` | Identyfikator konta wraz z sufiksem, np. `rx42698.switzerland-north.azure.snowflakecomputing.com` |
| `UID` | `digna` | Użytkownik Snowflake, do którego należy token |
| `Database` | `TEST` | Baza danych zawierająca schematy źródłowe. To jedyna baza, którą to połączenie może profilować |
| `Schema` | `PUBLIC` | Domyślny schemat sesji |
| `authenticator` | `PROGRAMMATIC_ACCESS_TOKEN` | Wybiera uwierzytelnianie tokenem |
| `token` | `<programmatic access token>` | Zaznacz **Encrypted** |

Powstały ciąg połączenia wygląda tak:

```
Driver={SnowflakeDSIIDriver};Server=<account>.snowflakecomputing.com;UID=digna;Database=TEST;Schema=PUBLIC;authenticator=PROGRAMMATIC_ACCESS_TOKEN;token=<programmatic access token>
```

### Magazyn i rola

Zapytania potrzebują magazynu. Jeśli użytkownik *digna* ma domyślny magazyn i domyślną rolę,
sesja je przejmuje i nic nie trzeba konfigurować. W przeciwnym razie dodaj:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `Warehouse` | `DIGNA_WH` | Magazyn wykonujący zapytania profilujące |
| `Role` | `DIGNA_READER` | Rola, z której uprawnień korzysta sesja |

!!! tip "Daj digna własny magazyn"

    Osobny, niewielki magazyn z automatycznym zawieszaniem utrzymuje koszt profilowania w polu
    widzenia i zapobiega konkurowaniu *digna* z użytkownikami interaktywnymi o moc obliczeniową.

### Uwierzytelnianie hasłem

Tam, gdzie konto nadal na to pozwala, zamiast tokenu działa hasło — usuń `authenticator` i
`token`, a dodaj:

| Klucz | Przykładowa wartość | Uwagi |
|---|---|---|
| `PWD` | `<password>` | Zaznacz **Encrypted** |

---

## 3. Konfiguracja *digna* {: #3-digna-configuration }

W ekranie **Add DB Connection** podaj następujące dane:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Profiling Mode:     Standard, Permanent or Session
Work Schema:        Schema for the work tables of "Permanent" profiling, e.g. "PUBLIC"
```

---

## 4. Uwagi dotyczące Snowflake {: #4-notes-on-snowflake }

- **Tokeny wygasają.** Programowy token dostępu jest wydawany z określonym czasem ważności, a
  profilowanie zatrzymuje się w dniu jego wygaśnięcia. Zanotuj datę wygaśnięcia przy tworzeniu
  tokenu i wprowadź nowy token we właściwości `token` — zaszyfrowanych wartości nie można
  odczytać, można je jedynie zastąpić.
- **Jedno połączenie widzi jedną bazę danych.** *digna* udostępnia schematy bazy wskazanej w
  `Database`, ponieważ Snowflake zgłasza jako katalog tylko bieżącą bazę. Tabele źródłowe w
  innej bazie wymagają własnego połączenia.
- **Identyfikatory są zapisane wielkimi literami**, o ile nie utworzono ich w cudzysłowach.
  *digna* używa nazw w takiej postaci, w jakiej zgłasza je Snowflake.
- **Tryby profilowania.** *Permanent* tworzy tabele robocze w **Work Schema**, więc rola
  potrzebuje tam uprawnienia `CREATE TABLE`. *Session* używa `CREATE TEMPORARY TABLE` i nie
  dotyka **Work Schema**. *Standard* wymaga wyłącznie dostępu do odczytu — i żadnych uprawnień
  do zapisu.

---

## 5. Weryfikacja sterownika (opcjonalnie) {: #5-verifying-the-driver-optional }

Konfigurowanie źródła danych ODBC nie jest wymagane dla połączenia bez DSN, ale okno dialogowe
samego sterownika to wygodny sposób, aby przed wprowadzeniem danych w *digna* potwierdzić, że
sterownik, adres URL konta i Twoje poświadczenia działają.

#### Krok 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Uwagi:

- Wartość **Server** składa się z identyfikatora Twojego konta Snowflake, po którym następuje
  `.snowflakecomputing.com`.
- **Database**, **Schema** i **Warehouse** wprowadzone tutaj odpowiadają właściwościom
  `Database`, `Schema` i `Warehouse` z [sekcji 2](#2-odbc-properties).

#### Krok 2 – Przetestuj połączenie

Kliknij przycisk **TEST**. Udane połączenie powinno wyglądać tak:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)