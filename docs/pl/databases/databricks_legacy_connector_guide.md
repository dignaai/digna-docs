---
title: Łącznik Databricks (Legacy, bez Unity Catalog) | digna Dokumentacja
description: Skonfiguruj digna tak, aby łączyła się z Databricks bez Unity Catalog, używając natywnego konektora Python lub sterownika Simba Spark ODBC. Wspiera uwierzytelnianie oparte na tokenie oraz elastyczne opcje łączności.
image: /assets/logo_square.png
---

# Source Connector for Databricks - without Unity Catalog

Ten przewodnik opisuje, jak skonfigurować *digna*, aby połączyć się z Databricks, używając natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> ⚠️ Dla innych metod uwierzytelniania użyj proszę sterownika ODBC.

### Personal Access Token (PAT)

Aby uwierzytelnić się za pomocą personal access token, odnieś się do oficjalnej dokumentacji Databricks:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Technology:      Databricks (Legacy)
Host Address:    Databricks hostname, e.g. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:       443
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
User Name:       HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:   Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Use ODBC:        Disabled (default)
```

---

## ODBC Driver

Sterownik ODBC obsługuje szerszy zakres metod uwierzytelniania i opcji łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na tokenie przy użyciu **Simba Spark ODBC Driver**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Simba Spark ODBC Driver**, postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Skonfiguruj źródło danych ODBC

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC przy użyciu Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test połączenia

Kliknij przycisk **TEST**. Pomyślne połączenie powinno wyglądać tak:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo za pomocą **DSN (Data Source Name)**, albo w konfiguracji **DSN-less**.

---

### A. Konfiguracja oparta na DSN

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 Wartość `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji sterownika ODBC.

---

### B. Konfiguracja DSN-less

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC Properties

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