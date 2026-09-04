---
title: Konektor Databricks z Unity Catalog – Integracja bazy danych | Dokumentacja digna
description: Skonfiguruj digna, aby łączyła się z Databricks z Unity Catalog przy użyciu natywnego konektora Python lub sterownika ODBC. Obsługuje uwierzytelnianie oparte na tokenach i elastyczną łączność.
image: /assets/logo_square.png
---

# Source Connector for Databricks - with Unity Catalog

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Databricks przy użyciu natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Personal Access Token (PAT)

Aby uwierzytelnić się przy użyciu personal access token, odnieś się do oficjalnej dokumentacji Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Podaj następujące informacje na ekranie **"Create a Database Connection"**:

```
Name:               Nazwa połączenia. Służy do odwołań do połączenia w innych ekranach.
Technology:         Databricks
Host Address:       Nazwa hosta Databricks, np. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:          np. 443
Database Name:      Nazwa katalogu (catalog), którego chcesz używać. 
User Name:          HTTP Path udostępniony przez Databricks, np. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:      Personal Access Token, np. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do stałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Disabled (domyślnie)
```

---

## ODBC Driver

Sterownik ODBC obsługuje szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na tokenie przy użyciu **Simba Spark ODBC Driver**.

### 1. Zainstaluj sterownik ODBC

Zainstaluj **Simba Spark ODBC Driver**, postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

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

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC, albo z konfiguracją **DSN (Data Source Name)**, albo w trybie **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Służy do odwołań do połączenia w innych ekranach.
Technology:         Databricks
Database Name:      Nazwa katalogu (catalog), którego chcesz używać.
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do stałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> `DSN` musi odpowiadać nazwie zdefiniowanej w konfiguracji Twojego sterownika ODBC.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Służy do odwołań do połączenia w innych ekranach.
Technology:         Databricks
Database Name:      Nazwa katalogu (catalog), którego chcesz używać.
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do stałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do tabeli sesyjnej lub tymczasowej, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent", tabele robocze zostaną umieszczone w tym schemacie.
Use ODBC:           Enabled
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