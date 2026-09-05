# Source Connector for Netezza

Niniejszy przewodnik opisuje, jak skonfigurować *digna*, aby łączyło się z Netezza przy użyciu sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## ODBC Driver

Sterownik ODBC może obsługiwać różne opcje uwierzytelniania i łączności. Ta sekcja koncentruje się na uwierzytelnianiu na podstawie hasła przy użyciu sterownika **NetezzaSQL**.

### 1. Install the ODBC Driver

Zainstaluj sterownik **NetezzaSQL** (lub podobny), postępując zgodnie z oficjalnym przewodnikiem instalacyjnym dostawcy.

### 2. Configure the ODBC Data Source

Wykonaj następujące kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem na podstawie hasła:

#### Step 1
![Step 1](images/netezza/create_odbc_data_source_step1.png)

W zależności od sterownika Netezza, wymagań instalacyjnych i zabezpieczeń, może być konieczne podanie danych również na kartach **Advanced DSN Options**, **SSL DSN Options** lub **Driver Options**. Dla najprostszej konfiguracji wystarczy podać dane na karcie **DSN Options**.

Kliknij przycisk **Test Connection**.

#### Step 2
![Step 2](images/netezza/create_odbc_data_source_step2.png)

Gdy zobaczysz ekran potwierdzający powodzenie, ODBC jest poprawnie skonfigurowany.

---

Teraz możesz skonfigurować *digna*, aby używało połączenia ODBC — albo z wykorzystaniem **DSN (Data Source Name)**, albo w konfiguracji **DSN-less**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Database Name:      Database that contains the source schemas
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "NZSQL"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```

> The `DSN` must match the name defined in your ODBC driver configuration.

---

### B. DSN-less Configuration

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Netezza
Database Name:      Database that contains the source schemas
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "NetezzaSQL"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "Port number, e.g. 5480"
name: "DATABASE",   value: "name of the database that contains the source data schema"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```