# Source Connector for Databricks - without Unity Catalog

Ten przewodnik opisuje, jak skonfigurować *digna*, aby połączyć się z Databricks, używając albo natywnego konektora Python, albo sterownika ODBC.

Odwołuje się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `databricks-sql-connector`  
**Supported Authentication:** Personal Access Token (PAT) only

> Dla innych metod uwierzytelniania użyj sterownika ODBC.

### Personal Access Token (PAT)

Aby uwierzytelnić się za pomocą personal access token, odnieś się do oficjalnej dokumentacji Databricks:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Configuration (Native Driver)

Podaj następujące informacje w ekranie **"Create a Database Connection"**:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Databricks (Legacy)
Host Address:       Nazwa hosta Databricks, np. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:          443
Database Name:      This parameter is not in use for databricks without unity catalog
User Name:          HTTP Path provided by Databricks, e.g. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:      Personal Access Token, e.g. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do trwałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do sesyjnej lub tymczasowej tabeli, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze będą umieszczane w tym schemacie.
Use ODBC:           Disabled (default)
```

---

## ODBC Driver

Sterownik ODBC obsługuje szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu opartym na tokenie przy użyciu **Simba Spark ODBC Driver**.

### 1. Install the ODBC Driver

Zainstaluj **Simba Spark ODBC Driver** postępując zgodnie z oficjalnym przewodnikiem instalacji dostawcy.

### 2. Configure the ODBC Data Source

Wykonaj następujące kroki, aby skonfigurować nowe źródło danych ODBC używając Personal Access Token:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Kliknij przycisk **TEST**. Udane połączenie powinno wyglądać tak:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC, albo przy użyciu **DSN (Data Source Name)**, albo konfiguracji **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

W ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Databricks (Legacy)
Database Name:      This parameter is not in use for databricks without unity catalog
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do trwałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do sesyjnej lub tymczasowej tabeli, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze będą umieszczane w tym schemacie.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DSN",    value: "*digna*data_databricks"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

W ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Nazwa połączenia. Używana do odwoływania się do połączenia w innych ekranach.
Technology:         Databricks (Legacy)
Database Name:      This parameter is not in use for databricks without unity catalog
Profiling Mode:     Tryb profilowania określa, jak digna przetwarza dane i oblicza metryki:
                    - Standard: Metryki są obliczane bezpośrednio na tabelach źródłowych bez kopiowania danych.
                    - Permanent: Dane dla inspektowanego dnia są kopiowane do trwałej tabeli, a metryki są obliczane na skopiowanych danych.
                    - Session: Dane są kopiowane do sesyjnej lub tymczasowej tabeli, a metryki są obliczane na tych tymczasowych danych.
Work Schema Name:   Przy użyciu trybu "Permanent" tabele robocze będą umieszczane w tym schemacie.
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