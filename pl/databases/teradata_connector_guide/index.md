# Source Connector for Teradata

Ten przewodnik opisuje, jak skonfigurować *digna*, aby łączyła się z Teradata przy użyciu natywnego konektora Python lub sterownika ODBC.

Odnosi się do ekranu **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Supported Authentication:** Password-based authentication only

> For other authentication methods, please use the ODBC driver.

### *digna* Configuration (Native Driver)

Wprowadź następujące informacje na ekranie **"Create a Database Connection"**:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Host Address:       Server name or IP address
Host Port:          Port number, e.g. 1025
Database Name:      Can be left empty. Digna treats databases as schemas for Teradata.
User Name:          Database user name
User Password:      Password for the user
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Disabled (default)
```

---

## ODBC Driver

Sterownik ODBC może obsługiwać szerszy zakres opcji uwierzytelniania i łączności. Ta sekcja skupia się na uwierzytelnianiu opartym na haśle z użyciem sterownika **Teradata Database ODBC Driver 20.00**.

### 1. Install the ODBC Driver

Zainstaluj sterownik **Teradata Database ODBC Driver 20.00** (lub podobny) zgodnie z oficjalnym przewodnikiem instalacyjnym producenta.

### 2. Configure the ODBC Data Source

Wykonaj poniższe kroki, aby skonfigurować nowe źródło danych ODBC z uwierzytelnianiem opartym na haśle:

#### Step 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Kliknij przycisk **Test**.

#### Step 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Podaj nazwę użytkownika i hasło.

Kliknij przycisk **OK**.  
Kiedy pojawi się ekran potwierdzający powodzenie, ODBC jest poprawnie skonfigurowany.

---

Teraz możesz skonfigurować *digna*, aby używała połączenia ODBC — albo z wykorzystaniem **DSN (Data Source Name)**, albo w konfiguracji **bez DSN (DSN-less)**.

---

### A. DSN-Based Configuration

#### *digna* Configuration

Na ekranie **"Create a Database Connection"** podaj następujące informacje:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Teradata
Database Name:      Can be left empty. Digna treats databases as schemas for Teradata.
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DSN",        value: "*digna*data_teradata"
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
Technology:         Teradata
Database Name:      Can be left empty. Digna treats databases as schemas for Teradata.
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC Properties

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
```