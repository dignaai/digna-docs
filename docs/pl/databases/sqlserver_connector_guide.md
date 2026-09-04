---
title: MS SQL Server Connector – Integracja bazy danych | digna Documentation
description: Skonfiguruj digna, aby łączyć się z Microsoft SQL Server przy użyciu sterownika Python pymssql lub sterownika ODBC dla SQL Server. Obsługuje uwierzytelnianie oparte na haśle w konfiguracjach DSN lub bez DSN.
image: /assets/logo_square.png
---


# Źródłowy konektor dla MS SQL Server

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z SQL Server przy użyciu natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Utwórz połączenie z bazą danych"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Python

**Biblioteka:** `pymssql`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie oparte na haśle

> Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Konfiguracja *digna* (sterownik natywny)

Podaj następujące informacje na ekranie **"Utwórz połączenie z bazą danych"**:

```
Name:               Nazwa połączenia. Służy do odwoływania się do połączenia w innych ekranach.
Technology:         MS SQL Server
Host Address:       Nazwa serwera lub adres IP
Host Port:          Numer portu, np. 1433
Database Name:      Nazwa bazy danych
User Name:          Nazwa użytkownika bazy danych
User Password:      Hasło użytkownika
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do trwałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może wspierać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle z użyciem sterownika **SQL Server**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj sterownik **SQL Server** (lub podobny) postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC używając uwierzytelniania opartego na haśle:

#### Krok 1
![Krok 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknij przycisk **Dalej >**.

#### Krok 2
![Krok 2](images/sqlserver/create_odbc_data_source_step2.png)

Wybierz metodę uwierzytelniania (np. nazwa użytkownika i hasło)
i podaj wymagane dane.

Kliknij przycisk **Dalej >**.

#### Krok 3
![Krok 3](images/sqlserver/create_odbc_data_source_step3.png)

Wybierz ustawienia zgodne z ANSI, a następnie kliknij przycisk **Dalej >**.

#### Krok 4
![Krok 4](images/sqlserver/create_odbc_data_source_step4.png)

Możesz pozostawić ustawienia domyślne lub wybrać opcje logowania w razie potrzeby
i kliknąć przycisk **Zakończ**.

#### Krok 5
![Krok 5](images/sqlserver/create_odbc_data_source_step5.png)

Teraz kliknij przycisk **Test datasource**.

#### Krok 6
![Krok 1](images/sqlserver/create_odbc_data_source_step6.png)

Gdy zobaczysz ekran sukcesu, ODBC jest poprawnie skonfigurowane.

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo za pomocą **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Utwórz połączenie z bazą danych"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Służy do odwoływania się do połączenia w innych ekranach.
Technology:         MS SQL Server
Database Name:      Baza danych zawierająca schematy źródłowe
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do trwałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DSN",        value: "sqlserver-1"
name: "UID",        value: "twój użytkownik bazy danych"
name: "PWD",        value: "twoje hasło do bazy danych"
name: "DATABASE",   value: "nazwa bazy danych zawierającej schemat źródłowy"
```

> `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Utwórz połączenie z bazą danych"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Służy do odwoływania się do połączenia w innych ekranach.
Technology:         MS SQL Server
Database Name:      Nazwa bazy danych zawierającej schematy danych źródłowych
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do trwałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "nazwa serwera lub adres IP"
name: "UID",        value: "twój użytkownik bazy danych"
name: "PWD",        value: "twoje hasło do bazy danych"
name: "DATABASE",   value: "nazwa bazy danych zawierającej schematy danych źródłowych"
```