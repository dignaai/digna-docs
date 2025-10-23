---
title: Databricks-Connector mit Unity Catalog – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna, um sich mit Databricks und Unity Catalog über den nativen Python-Connector oder den ODBC-Treiber zu verbinden. Unterstützt tokenbasierte Authentifizierung und flexible Konnektivität.
image: /assets/logo_square.png
---

# Source Connector für Databricks - mit Unity Catalog

Dieser Leitfaden beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Databricks entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `databricks-sql-connector`  
**Unterstützte Authentifizierung:** Personal Access Token (PAT) nur

> ⚠️ Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### Personal Access Token (PAT)

Um sich mit einem Personal Access Token zu authentifizieren, lesen Sie die offizielle Databricks-Dokumentation:  
👉 [How to obtain a PAT](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Konfiguration (nativ)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

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

## ODBC-Treiber

Der ODBC-Treiber unterstützt eine größere Bandbreite an Authentifizierungs- und Konnektivitätsoptionen. Dieser Abschnitt konzentriert sich auf tokenbasierte Authentifizierung mit dem **Simba Spark ODBC Driver**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den **Simba Spark ODBC Driver** gemäß der offiziellen Installationsanleitung des Herstellers.

### 2. Konfigurieren der ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit einem Personal Access Token zu konfigurieren:

#### Schritt 1
![Step 1](images/databricks/create_odbc_data_source_step1.png)

#### Schritt 2
![Step 2](images/databricks/create_odbc_data_source_step2.png)

#### Schritt 3
![Step 3](images/databricks/create_odbc_data_source_step3.png)

#### Schritt 4
![Step 4](images/databricks/create_odbc_data_source_step4.png)

#### Schritt 5 – Verbindung testen

Klicken Sie auf die **TEST**-Schaltfläche. Eine erfolgreiche Verbindung sollte so aussehen:

![Step 5](images/databricks/create_odbc_data_source_step5.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder ohne DSN.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "*digna*data_databricks"
```

> 🔹 Der `DSN` muss mit dem Namen übereinstimmen, der in Ihrer ODBC-Treiberkonfiguration definiert ist.

---

### B. DSN-less Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Databricks
Database Name:   Name of the catalog to use.
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