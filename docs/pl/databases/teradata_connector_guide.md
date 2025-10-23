---
title: Konektor Teradata – Integracja bazy danych | digna Documentation
description: Skonfiguruj digna do połączenia z Teradata przy użyciu sterownika Python teradatasql lub sterownika Teradata ODBC. Obsługuje uwierzytelnianie oparte na haśle w konfiguracjach z DSN lub bez DSN.
image: /assets/logo_square.png
---


# Źródłowy konektor dla Teradata

Ten przewodnik opisuje, jak skonfigurować *digna* do połączenia z Teradata przy użyciu albo natywnego konektora Pythona, albo sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Pythona

**Biblioteka:** `teradatasql`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie oparte na haśle

> ⚠️ Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Wprowadź następujące informacje na ekranie **"Create a Database Connection"**:

```
Technologia:      Teradata
Adres hosta:      Nazwa serwera lub adres IP
Port hosta:       Numer portu, np. 1025
Nazwa bazy danych:  Nazwa bazy danych
Nazwa schematu:     Nazwa bazy danych
Nazwa użytkownika:  Nazwa użytkownika bazy danych
Hasło użytkownika:  Hasło użytkownika
Użyj ODBC:         Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle przy użyciu sterownika **Teradata Database ODBC Driver 20.00**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj sterownik **Teradata Database ODBC Driver 20.00** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Krok 1
![Krok 1](images/teradata/create_odbc_data_source_step1.png)

Kliknij przycisk **Test**.

#### Krok 2
![Krok 2](images/teradata/create_odbc_data_source_step2.png)

Podaj nazwę użytkownika i hasło.

Kliknij przycisk **OK**.  
Gdy zobaczysz ekran potwierdzający, ODBC jest poprawnie skonfigurowane.

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC, albo z ustawieniem **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące dane:

```
Technologia:      Teradata
Nazwa bazy danych:   Baza danych zawierająca schemat źródłowy
Nazwa schematu:      Schemat zawierający źródłowe dane
Użyj ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "twój użytkownik bazy danych"
name: "PWD",        value: "twoje hasło do bazy danych"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące dane:

```
Technologia:      Teradata
Nazwa bazy danych:   Schemat zawierający źródłowe dane (taka sama jak Nazwa schematu)
Nazwa schematu:      Schemat zawierający źródłowe dane
Użyj ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "nazwa twojego serwera lub adres IP"
name: "UID",        value: "twój użytkownik bazy danych"
name: "PWD",        value: "twoje hasło do bazy danych"
```