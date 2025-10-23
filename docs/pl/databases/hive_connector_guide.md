---
title: Apache Hive Connector – Database Integration | digna Documentation
description: Configure digna to connect to Apache Hive using the native PyHive driver or the Cloudera ODBC driver. Supports password-based authentication and DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Źródłowy konektor dla Hive

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyło się z Hive przy użyciu natywnego konektora Pythona lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Python

**Biblioteka:** `PyHive`  
**Obsługiwane uwierzytelnianie:** tylko uwierzytelnianie za pomocą hasła

> ⚠️ Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technologia:      Apache Hive
Adres hosta:      Nazwa serwera lub adres IP
Port hosta:       Numer portu, np. 10000
Nazwa bazy danych: Schemat zawierający dane źródłowe
Nazwa schematu:   Schemat zawierający dane źródłowe
Nazwa użytkownika: Nazwa użytkownika bazy danych
Hasło użytkownika: Hasło dla użytkownika
Użyj ODBC:        Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą hasła przy użyciu sterownika **Cloudera ODBC Driver for Apache Hive**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Cloudera ODBC Driver for Apache Hive** (lub podobny) zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj następujące kroki, aby skonfigurować nowe źródło danych ODBC używając uwierzytelniania za pomocą hasła:

#### Krok 1
![Krok 1](images/hive/create_odbc_data_source_step1.png)


#### Krok 2 – Przetestuj połączenie

Podaj hasło i kliknij przycisk **Test**.

![Krok 2](images/hive/create_odbc_data_source_step2.png)

Po pomyślnym teście kliknij przycisk **OK**.

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC, albo z użyciem **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technologia:      Apache Hive
Nazwa bazy danych: Schemat zawierający dane źródłowe (taki sam jak Nazwa schematu)
Nazwa schematu:   Schemat zawierający dane źródłowe
Użyj ODBC:        Włączone
```

#### Właściwości ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{twoje hasło w nawiasach klamrowych}"
```

> 🔹 `DSN` musi zgadzać się z nazwą zdefiniowaną w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technologia:      Apache Hive
Nazwa bazy danych: Schemat zawierający dane źródłowe (taki sam jak Nazwa schematu)
Nazwa schematu:   Schemat zawierający dane źródłowe
Użyj ODBC:        Włączone
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "nazwa Twojego serwera lub adres IP"
name: "PORT",       value: "Numer portu, np. 10000"
name: "Schema",     value: "Schemat zawierający dane źródłowe"
name: "UID",        value: "Twój użytkownik Hive"
name: "PWD",        value: "Twoje hasło Hive"
name: "AuthMech",   value: "3"
```