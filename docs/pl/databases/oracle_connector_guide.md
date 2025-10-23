---
title: Oracle Connector – integracja z bazą danych | dokumentacja digna
description: Skonfiguruj digna, aby łączyła się z Oracle przy użyciu sterownika python-oracledb lub sterownika Oracle ODBC. Obsługuje uwierzytelnianie na podstawie hasła z konfiguracją DSN lub bez DSN.
image: /assets/logo_square.png
---


# Konektor źródłowy dla Oracle

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z bazą Oracle DB przy użyciu natywnego konektora Pythona lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Pythona

**Biblioteka:** `python-oracledb`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie na podstawie hasła

> ⚠️ W przypadku innych metod uwierzytelniania prosimy o użycie sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technologia:      Oracle
Adres hosta:      Nazwa serwera lub adres IP
Port hosta:       Numer portu, np. 1521
Nazwa bazy danych: Nazwa instancji, service name
Schemat:          Schemat zawierający źródłowe dane
Nazwa użytkownika: Nazwa użytkownika bazy danych
Hasło użytkownika: Hasło dla użytkownika
Użyj ODBC:        Wyłączone (domyślnie)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą hasła przy użyciu sterownika **Oracle in OraDB21Home1**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Oracle in OraDB21Home1** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem na podstawie hasła:

#### Krok 1
![Krok 1](images/oracle/create_odbc_data_source_step1.png)

Uwaga:
Nazwa usługi TNS musi być skonfigurowana w pliku tnsnames.ora instalacji klienta Oracle. To tam podajesz deskryptor połączenia (host, port, service name).

#### Krok 2 – Test połączenia

Kliknij przycisk **Test Connection**.

![Krok 2](images/oracle/create_odbc_data_source_step2.png)

Podaj hasło i kliknij przycisk **OK**.

![Krok 2](images/oracle/create_odbc_data_source_step3.png)

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo z konfiguracją **DSN (Data Source Name)**, albo bez DSN.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technologia:      Oracle
Nazwa bazy danych: Baza danych zawierająca źródłowy schemat
Schemat:          Schemat zawierający źródłowe dane
Użyj ODBC:        Włączone
```

#### Właściwości ODBC

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technologia:      Oracle
Nazwa bazy danych: Schemat zawierający źródłowe dane (taka sama jak Schemat)
Schemat:          Schemat zawierający źródłowe dane
Użyj ODBC:        Włączone
```

#### Właściwości ODBC

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```