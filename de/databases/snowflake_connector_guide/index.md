# Quell-Connector für Snowflake

Dieses Handbuch beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Snowflake entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Es bezieht sich auf den Bildschirm **„Datenbankverbindung erstellen“**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `snowflake-connector-python`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (nativer Treiber)

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** die folgenden Informationen an:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Host Address:       Snowflake account name
Host Port:          Not needed
Database Name:      Database that contains the source schema
User Name:          User name and warehouse in the format "user<@>warehouse"
User Password:      Password for the user
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" or "Session" profiling mode, work tables will be placed in this schema.
Use ODBC:           Disabled (default)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem **SnowflakeDSIIDriver**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den **SnowflakeDSIIDriver** gemäß der offiziellen Installationsanleitung des Herstellers.

### 2. Konfigurieren der ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/snowflake/create_odbc_data_source_step1.png)

Hinweise:
- Wenn Sie keine Werte für Database, Schema und Warehouse angeben, müssen Sie diese als ODBC-Eigenschaften während der *digna*-Datenquellenkonfiguration angeben.
- Der Wert für "Server" besteht aus Ihrem Snowflake-Kontonamen gefolgt von ".snowflakecomputing.com"

#### Schritt 2 – Verbindung testen

Klicken Sie auf die **TEST**-Schaltfläche. Eine erfolgreiche Verbindung sollte so aussehen:

![Schritt 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-losen** Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** die folgenden Angaben ein:

```
Name:               Name of the connection. This is used for referencing the connection in other screens.
Technology:         Snowflake
Database Name:      Database that contains the source schemas
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" or "Session" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schemas"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiber-Konfiguration definierten Namen übereinstimmen.

---

### B. DSN-loser Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** die folgenden Angaben ein:

```
Technology:         Snowflake
Database Name:      Database that contains the source schemas
Profiling Mode:     The profiling mode determines how digna processes data and calculates metrics:
                    - Standard: Metrics are calculated directly on the source tables without copying the data.
                    - Permanent: Data for the inspected day is copied into a permanent table, and metrics are calculated on the copied data.
                    - Session: Data is copied into a session or temporary table, and metrics are calculated on this temporary data.
Work Schema Name:   When using "Permanent" or "Session" profiling mode, work tables will be placed in this schema.
Use ODBC:           Enabled
```

#### ODBC-Eigenschaften

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```