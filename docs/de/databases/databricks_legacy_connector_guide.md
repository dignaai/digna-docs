---
title: Databricks Connector (Legacy, ohne Unity Catalog) | digna Dokumentation
description: Konfigurieren Sie digna, um sich mit Databricks ohne Unity Catalog zu verbinden, entweder über den nativen Python-Connector oder den Simba Spark ODBC-Treiber. Unterstützt tokenbasierte Authentifizierung und flexible Konnektivität.
image: /assets/logo_square.png
---

# Quell-Connector für Databricks – ohne Unity Catalog

Dieser Leitfaden beschreibt, wie Sie *digna* konfigurieren, um eine Verbindung zu Databricks herzustellen, entweder mit dem nativen Python-Connector oder dem ODBC-Treiber.

Es bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python-Treiber

**Bibliothek:** `databricks-sql-connector`  
**Unterstützte Authentifizierung:** Nur Personal Access Token (PAT)

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### Personal Access Token (PAT)

Um sich mit einem Personal Access Token zu authentifizieren, lesen Sie die offizielle Databricks-Dokumentation:  
[How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Konfiguration (nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** ein:

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

## ODBC-Treiber

Der ODBC-Treiber unterstützt eine größere Bandbreite an Authentifizierungs- und Konnektivitätsoptionen. Dieser Abschnitt konzentriert sich auf tokenbasierte Authentifizierung mit dem **Simba Spark ODBC Driver**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den **Simba Spark ODBC Driver**, indem Sie der offiziellen Installationsanleitung des Anbieters folgen.

### 2. Konfigurieren der ODBC-Datenquelle

Folgen Sie diesen Schritten, um eine neue ODBC-Datenquelle mit einem Personal Access Token zu konfigurieren:

#### Step 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Step 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Step 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Step 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Step 5 – Test the connection

Klicken Sie auf die **TEST**-Schaltfläche. Eine erfolgreiche Verbindung sollte so aussehen:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder über eine **DSN (Data Source Name)** oder eine **DSN-less**-Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "*digna*data_databricks"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less-Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Databricks (Legacy)
Database Name:   This parameter is not in use for databricks without unity catalog
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

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