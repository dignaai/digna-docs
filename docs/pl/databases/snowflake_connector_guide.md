---
title: Snowflake Connector – Integracja z bazą danych | Dokumentacja digna
description: Skonfiguruj digna, aby łączyła się ze Snowflake przy użyciu natywnego konektora Python lub sterownika ODBC. Obsługuje uwierzytelnianie oparte na haśle z konfiguracjami DSN lub bez DSN.
image: /assets/logo_square.png
---


# Source Connector for Snowflake

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się ze Snowflake, używając natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `snowflake-connector-python`  
**Supported Authentication:** Tylko uwierzytelnianie oparte na haśle

> Dla innych metod uwierzytelniania użyj sterownika ODBC.

### *digna* Configuration (Native Driver)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia na innych ekranach.
Technology:         Snowflake
Host Address:       Nazwa konta Snowflake
Host Port:          Niepotrzebne
Database Name:      Baza danych zawierająca źródłowy schemat
User Name:          Nazwa użytkownika i warehouse w formacie "user<@>warehouse"
User Password:      Hasło użytkownika
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla analizowanego dnia są kopiowane do stałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu profilowania "Permanent" lub "Session", tabele robocze będą umieszczane w tym schemacie.
Use ODBC:           Wyłączone (domyślnie)
```

---

## ODBC Driver

Sterownik ODBC może obsługiwać szerszy zakres metod uwierzytelniania i opcji łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle z użyciem **SnowflakeDSIIDriver**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **SnowflakeDSIIDriver**, postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Krok 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Uwagi:
- Jeśli nie podasz wartości dla Database, Schema i Warehouse, będziesz musiał je podać jako właściwości ODBC podczas konfiguracji źródła danych w *digna*.
- Wartość pola "Server" składa się z nazwy Twojego konta Snowflake, po której następuje ".snowflakecomputing.com"

#### Krok 2 – Test połączenia

Kliknij przycisk **TEST**. Pomyślne połączenie powinno wyglądać tak:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo z konfiguracją **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia na innych ekranach.
Technology:         Snowflake
Database Name:      Baza danych zawierająca źródłowe schematy
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla analizowanego dnia są kopiowane do stałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu profilowania "Permanent" lub "Session", tabele robocze będą umieszczane w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

opcjonalnie:
name: "Database",       value: "Baza danych zawierająca źródłowe schematy"
name: "Warehouse",      value: "Warehouse używany do wykonywania zapytań SQL"
```

> Wartość `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:         Snowflake
Database Name:      Baza danych zawierająca źródłowe schematy
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla analizowanego dnia są kopiowane do stałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu profilowania "Permanent" lub "Session", tabele robocze będą umieszczane w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Baza danych zawierająca źródłowy schemat"
name: "Warehouse",  value: "Warehouse używany do wykonywania zapytań SQL"
```