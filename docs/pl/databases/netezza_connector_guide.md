---
title: Konektor Netezza – Integracja z bazą danych | dokumentacja digna
description: Skonfiguruj *digna*, aby łączyła się z Netezza przy użyciu sterownika ODBC NetezzaSQL. Obsługuje uwierzytelnianie na podstawie hasła zarówno z użyciem DSN, jak i konfiguracji bez DSN dla elastycznego połączenia.
image: /assets/logo_square.png
---


# Konektor źródłowy dla Netezza

Niniejszy przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Netezza przy użyciu sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać różne opcje uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na haśle przy użyciu sterownika **NetezzaSQL**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj sterownik **NetezzaSQL** (lub podobny) zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Krok 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

W zależności od sterownika Netezza, wymagań dotyczących konfiguracji i bezpieczeństwa, może być konieczne podanie dodatkowych danych na kartach **Advanced DSN Options**, **SSL DSN Options** lub **Driver Options**. Dla najprostszej konfiguracji wystarczy podać dane w **DSN Options**.

Kliknij przycisk **Test Connection**.

#### Krok 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Gdy pojawi się ekran potwierdzający powodzenie, ODBC jest poprawnie skonfigurowane.

---

Teraz możesz skonfigurować *digna*, aby korzystała z połączenia ODBC, albo z użyciem **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące wartości:

```
Technology:      Netezza
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji Twojego sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące wartości:

```
Technology:      Netezza
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```