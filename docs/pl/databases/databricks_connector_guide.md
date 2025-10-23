---
title: Konektor Databricks z Unity Catalog – Integracja bazy danych | Dokumentacja digna
description: Skonfiguruj digna, aby łączył się z Databricks z Unity Catalog, używając natywnego konektora Python lub sterownika ODBC. Obsługa uwierzytelniania za pomocą tokenów oraz elastyczne opcje łączności.
image: /assets/logo_square.png
---

# Konektor źródłowy dla Databricks - z Unity Catalog

Ten przewodnik opisuje, jak skonfigurować *digna*, aby połączyć się z Databricks, używając albo natywnego konektora Python, albo sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Utwórz połączenie z bazą danych](images/data_source_config_input_mask.png)

---

## Natywny sterownik Python

**Library:** `databricks-sql-connector`  
**Obsługiwane uwierzytelnianie:** tylko Personal Access Token (PAT)

> ⚠️ Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Personal Access Token (PAT)

Aby uwierzytelnić się za pomocą Personal Access Token, zapoznaj się z oficjalną dokumentacją Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### Konfiguracja *digna* (natywny sterownik)

Podaj następujące informacje w ekranie **"Create a Database Connection"**:

```
Technology:      Databricks
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   Name of the catalog to use. 
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## Sterownik ODBC

Sterownik ODBC obsługuje szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu za pomocą tokena przy użyciu **Simba Spark ODBC Driver**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Simba Spark ODBC Driver**, postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj następujące kroki, aby skonfigurować nowe źródło danych ODBC używając Personal Access Token:

#### Krok 1
![Krok 1](images/databricks/create_odbc_data_source_step1.png)

#### Krok 2
![Krok 2](images/databricks/create_odbc_data_source_step2.png)

#### Krok 3
![Krok 3](images/databricks/create_odbc_data_source_step3.png)

#### Krok 4
![Krok 4](images/databricks/create_odbc_data_source_step4.png)

#### Krok 5 – Test połączenia

Kliknij przycisk **TEST**. Pomyślne połączenie powinno wyglądać tak:

![Krok 5](images/databricks/create_odbc_data_source_step5.png)

---

Teraz możesz skonfigurować *digna*, aby używał połączenia ODBC, albo z **DSN (Data Source Name)**, albo w konfiguracji **bez DSN**.

---

### A. Konfiguracja oparta na DSN

#### Konfiguracja *digna*

W ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji Twojego sterownika ODBC.

---

### B. Konfiguracja bez DSN

#### Konfiguracja *digna*

W ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### Właściwości ODBC

```
name = "Driver",          value = "{Simba Spark ODBC Driver}"
name = "Host",            value = "xxxxxxxxxxxxxxxxxxx.databricks.com"
name = "Port",            value = "443"
name = "HTTPPath",        value = "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
name = "SSL",             value = "1"
name = "ThriftTransport", value = "2"
name = "AuthMech",        value = "3"
name = "UID",             value = "token"
name = "PWD",             value = "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```