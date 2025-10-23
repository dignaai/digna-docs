---
title: Konnektor PostgreSQL – Integracja bazy danych | dokumentacja digna
description: Skonfiguruj digna tak, aby łączyło się z PostgreSQL za pomocą natywnego sterownika Python psycopg lub sterownika ODBC PostgreSQL. Obsługuje uwierzytelnianie na podstawie hasła w konfiguracjach z DSN lub bez DSN.
image: /assets/logo_square.png
---


# Źródłowy konektor dla PostgreSQL

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyło się z Postgres przy użyciu natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natywny sterownik Python

**Biblioteka:** `psycopg`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie oparte na haśle

> ⚠️ Dla innych metod uwierzytelniania prosimy użyć sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technology:      Postgres
Host Address:    Nazwa serwera lub adres IP
Host Port:       Numer portu, np. 5432
Database Name:   Nazwa bazy danych
Schema Name:     Schemat zawierający źródłowe dane
User Name:       Nazwa użytkownika bazy danych
User Password:   Hasło użytkownika
Use ODBC:        Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres metod uwierzytelniania i opcji łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle przy użyciu sterownika **PostgreSQL Unicode(x64)**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **PostgreSQL Unicode(x64)** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj następujące kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Krok 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Uwaga: Jeśli w konfiguracji bazy danych musisz wybrać konkretny "SSLMode", upewnij się, że użyjesz tej samej wartości podczas definiowania konfiguracji bez DSN (DSN-less).

#### Krok 2 – Test połączenia

Kliknij przycisk **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC, albo przy użyciu **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      PostgreSQL
Database Name:   Baza danych zawierająca schemat źródłowy
Schema Name:     Schemat zawierający źródłowe dane
Use ODBC:        Włączone
```

#### Właściwości ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji Twojego sterownika ODBC.

---

### B. Konfiguracja bez DSN (DSN-less)

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      PostgreSQL
Database Name:   Schemat zawierający źródłowe dane (to samo co Schema Name)
Schema Name:     Schemat zawierający źródłowe dane
Use ODBC:        Włączone
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "nazwa serwera lub adres IP"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres lub inna nazwa Twojej bazy danych"
name: "UID",        value: "Twój użytkownik postgres"
name: "PWD",        value: "Twoje hasło postgres"
name: "SSLMode",    value: "require"
```