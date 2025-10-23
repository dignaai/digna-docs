---
title: Snowflake Connector – Datenbankintegration | digna-Dokumentation
description: Konfigurieren Sie digna so, dass eine Verbindung zu Snowflake über den Python-Connector oder den Snowflake ODBC-Treiber hergestellt wird. Unterstützt passwortbasierte Authentifizierung mit DSN- oder DSN-losen Setups.
image: /assets/logo_square.png
---


# Quell-Connector für Snowflake

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Snowflake entweder über den nativen Python-Connector oder über den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `snowflake-connector-python`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> ⚠️ Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

```
Technology:      Snowflake
Host Address:    Snowflake account name
Host Port:       Not needed
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
User Name:       User name and warehouse in the format "user<@>warehouse"
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mithilfe des **SnowflakeDSIIDriver**.

### 1. ODBC-Treiber installieren

Installieren Sie den **SnowflakeDSIIDriver** gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. ODBC-Datenquelle konfigurieren

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/snowflake/create_odbc_data_source_step1.png)

Hinweise:
- Wenn Sie keine Werte für Database, Schema und Warehouse angeben, müssen Sie diese als ODBC-Eigenschaften während der *digna*-Datenquellenkonfiguration angeben.
- Der Wert für "Server" besteht aus Ihrem Snowflake-Kontonamen, gefolgt von ".snowflakecomputing.com"

#### Schritt 2 – Verbindung testen

Klicken Sie auf die **TEST**-Schaltfläche. Eine erfolgreiche Verbindung sollte so aussehen:

![Schritt 2](images/snowflake/create_odbc_data_source_step2.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-less**-Konfiguration verwendet wird.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Snowflake
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",            value: "snowflake_demo_2"
name: "PWD",            value: "{your password in curly braces}"

optionally:
name: "Database",       value: "Database that contains the source schema"
name: "Schema",         value: "Schema that contains the source data"
name: "Warehouse",      value: "Warehouse to use for the execution of the SQLs"
```

> 🔹 Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less-Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Snowflake
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "Driver",     value: "{SnowflakeDSIIDriver}"
name: "Server",     value: "your-account-name.snowflakecomputing.com'
name: "UID",        value: "your snowflake user'
name: "PWD",        value: "your snowflake password"
name: "Database",   value: "Database that contains the source schema"
name: "Schema",     value: "Schema that contains the source data"
name: "Warehouse",  value: "Warehouse to use for the execution of the SQLs"
```