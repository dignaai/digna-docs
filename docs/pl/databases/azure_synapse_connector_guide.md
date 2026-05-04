---
title: Azure Synapse Connector – Integracja bazy danych | digna Documentation
description: Skonfiguruj digna, aby łączyła się z Azure Synapse Analytics przy użyciu natywnego sterownika Pythona lub sterownika ODBC. Obsługuje zarówno serverless, jak i dedykowane pule SQL.
image: /assets/logo_square.png
canonical_url: https://docs.digna.ai/databases/azure_synapse_connector_guide/
---


# Źródłowy konektor dla Azure Synapse Analytics

Niniejszy przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Azure Synapse Analytics przy użyciu natywnego konektora Pythona lub sterownika ODBC. Obsługiwane są zarówno serverless, jak i dedykowane pule SQL.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Pythona

**Biblioteka:** `pymssql`  
**Obsługiwane uwierzytelnianie:** Tylko uwierzytelnianie za pomocą hasła

> ⚠️ W przypadku innych metod uwierzytelniania użyj sterownika ODBC.

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## Sterownik ODBC

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą hasła przy użyciu sterownika **ODBC Driver 18 for SQL Server**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj sterownik **ODBC Driver 18 for SQL Server** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC używając uwierzytelniania za pomocą hasła:

#### Krok 1
![Krok 1](images/azure_synapse/create_odbc_data_source_step1.png)

Wypełnij pole "Server".
Użyj nazwy workspace Synapse i dopisz ".sql.azuresynapse.net".  
**Uwaga**, jeśli chcesz połączyć się przy użyciu serverless SQL pool, upewnij się, że do nazwy dodasz "-ondemand", jak pokazano na poniższym zrzucie ekranu.

Kliknij przycisk **Next >**.

#### Krok 2
![Krok 2](images/azure_synapse/create_odbc_data_source_step2.png)

Wybierz metodę uwierzytelniania (np. nazwa użytkownika i hasło)
i podaj wymagane dane.

Kliknij przycisk **Next >**.

#### Krok 3
![Krok 3](images/azure_synapse/create_odbc_data_source_step3.png)

Wybierz ustawienia zgodne z ANSI, a następnie kliknij przycisk **Next >**.

#### Krok 4
![Krok 4](images/azure_synapse/create_odbc_data_source_step4.png)

Możesz pozostawić ustawienia domyślne lub wybrać opcje zgodnie z potrzebami 
i kliknąć przycisk **Finish**. 

#### Krok 5
![Krok 5](images/azure_synapse/create_odbc_data_source_step5.png)

Teraz kliknij przycisk **Test datasource**.

#### Krok 6
![Krok 6](images/azure_synapse/create_odbc_data_source_step6.png)

Gdy pojawi się ekran potwierdzający powodzenie, ODBC jest poprawnie skonfigurowane.

---

Teraz możesz skonfigurować *digna*, aby korzystała z połączenia ODBC, albo przy użyciu **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące dane:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

Na ekranie **"Create a Database Connection"** podaj następujące dane:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Uwaga** dotycząca właściwości SERVER:  
Użyj nazwy workspace Synapse i dopisz ".sql.azuresynapse.net". Jeśli chcesz połączyć się przy użyciu serverless SQL pool, upewnij się, że do nazwy dodasz "-ondemand", jak pokazano na poniższym zrzucie ekranu.