---
title: Konektor PostgreSQL – Integracja z bazą danych | Dokumentacja digna
description: Skonfiguruj digna, aby łączył się z PostgreSQL przy użyciu sterownika Pythona `psycopg` lub sterownika ODBC PostgreSQL. Obsługuje uwierzytelnianie oparte na haśle w konfiguracjach z DSN lub bez DSN.
image: /assets/logo_square.png
---


# Konektor źródłowy dla PostgreSQL

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyło się z Postgresem przy użyciu albo natywnego connectora Pythona, albo sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Natywny sterownik Pythona

**Biblioteka:** `psycopg`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie za pomocą hasła

> ⚠️ Dla innych metod uwierzytelniania prosimy użyć sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Postgres
Host Address:       Nazwa serwera lub adres IP
Host Port:          Numer portu, np. 5432
Database Name:      Nazwa bazy danych
User Name:          Nazwa użytkownika bazy danych
User Password:      Hasło użytkownika
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspekcjonowanego dnia są kopiowane do trwałej tabeli, a metryki obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą hasła przy użyciu sterownika **PostgreSQL Unicode(x64)**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **PostgreSQL Unicode(x64)** (lub podobny) postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC używając uwierzytelniania opartego na haśle:

#### Krok 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Uwaga: Jeśli konfiguracja bazy wymaga wybrania konkretnego "SSLMode", upewnij się, że użyjesz go również definiując konfigurację bez DSN.

#### Krok 2 – Test połączenia

Kliknij przycisk **Test Connection**.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC — albo z **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         PostgreSQL
Database Name:      Baza danych zawierająca schematy źródłowe
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspekcjonowanego dnia są kopiowane do trwałej tabeli, a metryki obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         PostgreSQL
Database Name:      Baza danych zawierająca schematy źródłowe
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspekcjonowanego dnia są kopiowane do trwałej tabeli, a metryki obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "nazwa twojego serwera lub adres IP"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres lub inna nazwa twojej bazy danych"
name: "UID",        value: "twój użytkownik postgres'
name: "PWD",        value: "twoje hasło postgres"
name: "SSLMode",    value: "require"
```