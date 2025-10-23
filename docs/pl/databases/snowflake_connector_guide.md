---
title: Konektor Snowflake – integracja bazy danych | Dokumentacja digna
description: Skonfiguruj digna do łączenia ze Snowflake przy użyciu natywnego konektora Pythona lub sterownika ODBC Snowflake. Obsługuje uwierzytelnianie oparte na haśle w konfiguracjach z DSN lub bez DSN.
image: /assets/logo_square.png
---


# Konektor źródłowy dla Snowflake

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyło się ze Snowflake przy użyciu natywnego konektora Pythona lub sterownika ODBC.

Odwołuje się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natywny sterownik Pythona

**Biblioteka:** `snowflake-connector-python`  
**Obsługiwane uwierzytelnianie:** tylko uwierzytelnianie oparte na haśle

> ⚠️ Dla innych metod uwierzytelniania proszę użyć sterownika ODBC.

### *digna* — konfiguracja (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Baza danych zawierająca schemat źródłowy
Schema Name:     Schemat zawierający dane źródłowe
User Name:       Nazwa użytkownika i warehouse w formacie "user<@>warehouse"
User Password:   Hasło użytkownika
Use ODBC:        Disabled (default)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle przy użyciu **SnowflakeDSIIDriver**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **SnowflakeDSIIDriver**, postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Krok 1
![Step 1](images/snowflake/create_odbc_data_source_step1.png)

Uwagi:
- Jeśli nie podasz wartości dla Database, Schema i Warehouse, będziesz musiał podać je jako właściwości ODBC podczas konfiguracji źródła danych w *digna*.
- Wartość dla "Server" składa się z nazwy twojego konta Snowflake, po której następuje ".snowflakecomputing.com"

#### Krok 2 – Test połączenia

Kliknij przycisk **TEST**. Poprawne połączenie powinno wyglądać tak:

![Step 2](images/snowflake/create_odbc_data_source_step2.png)

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC, albo za pomocą **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      Snowflake
Database Name:   Baza danych zawierająca schemat źródłowy
Schema Name:     Schemat zawierający dane źródłowe
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{twoje hasło w nawiasach klamrowych}"

opcjonalnie:
name: "Database",       value: "Baza danych zawierająca schemat źródłowy"
name: "Schema",         value: "Schemat zawierający dane źródłowe"
name: "Warehouse",      value: "Warehouse używany do wykonywania zapytań SQL"
```

> 🔹 The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. Konfiguracja bez DSN (DSN-less)

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      Snowflake
Database Name:   Schemat zawierający dane źródłowe (taki sam jak Schema Name)
Schema Name:     Schemat zawierający dane źródłowe
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "twój użytkownik Snowflake'
name: "PWD",        value: "twoje hasło Snowflake"
name: "Database",   value: "Baza danych zawierająca schemat źródłowy"
name: "Schema",     value: "Schemat zawierający dane źródłowe"
name: "Warehouse",  value: "Warehouse używany do wykonywania zapytań SQL"
```