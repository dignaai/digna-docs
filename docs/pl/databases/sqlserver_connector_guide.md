---
title: Konektor MS SQL Server – Integracja bazy danych | dokumentacja digna
description: Skonfiguruj digna do połączenia z Microsoft SQL Server za pomocą sterownika Python pymssql lub sterownika ODBC dla SQL Server. Obsługuje uwierzytelnianie oparte na haśle z konfiguracjami DSN lub bez DSN.
image: /assets/logo_square.png
---


# Source Connector for MS SQL Server

Ten przewodnik opisuje, jak skonfigurować *digna* do łączenia się z SQLServer przy użyciu natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Biblioteka:** `pymssql`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie oparte na haśle

> ⚠️ W przypadku innych metod uwierzytelniania użyj sterownika ODBC.

### *digna* Configuration (Native Driver)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technologia:      MS SQL Server
Adres hosta:      Nazwa serwera lub adres IP
Port hosta:       Numer portu, np. 1433
Nazwa bazy danych: Nazwa bazy danych
Nazwa schematu:   Schemat zawierający dane źródłowe
Nazwa użytkownika: Nazwa użytkownika bazy danych
Hasło użytkownika: Hasło dla użytkownika
Use ODBC:         Disabled (default)
```

---

## ODBC Driver

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle przy użyciu sterownika **SQL Server**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj sterownik **SQL Server** (lub podobny) postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Krok 1
![Step 1](images/sqlserver/create_odbc_data_source_step1.png)

Kliknij przycisk **Next >**.

#### Krok 2
![Step 2](images/sqlserver/create_odbc_data_source_step2.png)

Wybierz metodę uwierzytelniania (np. nazwa użytkownika i hasło)
i podaj wymagane dane.

Kliknij przycisk **Next >**.

#### Krok 3
![Step 3](images/sqlserver/create_odbc_data_source_step3.png)

Wybierz ustawienia zgodne z ANSI, a następnie kliknij przycisk **Next >**.

#### Krok 4
![Step 4](images/sqlserver/create_odbc_data_source_step4.png)

Możesz pozostawić ustawienia domyślne lub wybrać opcje logowania w razie potrzeby
i kliknąć przycisk **Finish**. 

#### Krok 5
![Step 5](images/sqlserver/create_odbc_data_source_step5.png)

Teraz kliknij przycisk **Test datasource**.

#### Krok 6
![Step 1](images/sqlserver/create_odbc_data_source_step6.png)

Gdy zobaczysz ekran potwierdzający powodzenie, ODBC jest poprawnie skonfigurowane.

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC, albo przy użyciu **DSN (Data Source Name)**, albo konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące dane:

```
Technologia:      MS SQL Server
Nazwa bazy danych: Baza zawierająca schemat źródłowy
Nazwa schematu:   Schemat zawierający dane źródłowe
Use ODBC:         Enabled
```

#### Właściwości ODBC

```
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące dane:

```
Technologia:      MS SQL Server
Nazwa bazy danych: Schemat zawierający dane źródłowe (takie samo jak Nazwa schematu)
Nazwa schematu:   Schemat zawierający dane źródłowe
Use ODBC:         Enabled
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```