---
title: Konektor Apache Hive – integracja bazy danych | Dokumentacja digna
description: Skonfiguruj digna do łączenia się z Apache Hive przy użyciu natywnego sterownika PyHive lub sterownika ODBC firmy Cloudera. Obsługuje uwierzytelnianie za pomocą hasła oraz konfiguracje DSN i bez DSN.
image: /assets/logo_square.png
---


# Konektor źródłowy dla Hive

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Hive za pomocą natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Python

**Biblioteka:** `PyHive`  
**Obsługiwane uwierzytelnianie:** wyłącznie uwierzytelnianie za pomocą hasła

> ⚠️ Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Konfiguracja *digna* (nattywny sterownik)

Podaj następujące informacje w ekranie **"Create a Database Connection"**:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Apache Hive
Host Address:       Nazwa serwera lub adres IP
Host Port:          Numer portu, np. 10000
Database Name:      Schemat zawierający źródłowe dane
User Name:          Nazwa użytkownika bazy danych
User Password:      Hasło użytkownika
Profiling Mode:     Tryb profilowania określa, w jaki sposób digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do tabeli trwałej, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane są kopiowane do sesyjnej lub tymczasowej tabeli, a metryki obliczane są na tych tymczasowych danych.
Work Schema Name:   Przy wyborze trybu "Permanent" tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą hasła przy użyciu sterownika **Cloudera ODBC Driver for Apache Hive**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Cloudera ODBC Driver for Apache Hive** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj następujące kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem za pomocą hasła:

#### Krok 1
![Krok 1](images/hive/create_odbc_data_source_step1.png)


#### Krok 2 – Test połączenia

Wprowadź hasło i kliknij przycisk **Testuj**.

![Krok 2](images/hive/create_odbc_data_source_step2.png)

Po pomyślnym teście kliknij przycisk **OK**.

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo przy użyciu **DSN (Data Source Name)**, albo konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

W ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Apache Hive
Database Name:      Schemat zawierający źródłowe dane
Profiling Mode:     Tryb profilowania określa, w jaki sposób digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do tabeli trwałej, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane są kopiowane do sesyjnej lub tymczasowej tabeli, a metryki obliczane są na tych tymczasowych danych.
Work Schema Name:   Przy wyborze trybu "Permanent" tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

W ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Apache Hive
Database Name:      Schemat zawierający źródłowe dane
Profiling Mode:     Tryb profilowania określa, w jaki sposób digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do tabeli trwałej, a metryki obliczane są na skopiowanych danych.
                    - Session: Dane są kopiowane do sesyjnej lub tymczasowej tabeli, a metryki obliczane są na tych tymczasowych danych.
Work Schema Name:   Przy wyborze trybu "Permanent" tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Włączone
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "nazwa serwera lub adres IP"
name: "PORT",       value: "Numer portu, np. 10000"
name: "Schema",     value: "Schemat zawierający źródłowe dane"
name: "UID",        value: "your hive user'
name: "PWD",        value: "your hive password"
name: "AuthMech",   value: "3"
```