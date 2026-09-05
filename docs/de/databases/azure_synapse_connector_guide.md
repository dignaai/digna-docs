---
title: Azure Synapse Connector – Database Integration | digna Documentation
description: Configure digna to connect to Azure Synapse Analytics using either the native Python driver or the ODBC driver. Supports both serverless and dedicated SQL pools.
image: /assets/logo_square.png
---


# Source-Connector für Azure Synapse Analytics

Dieser Leitfaden beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Azure Synapse Analytics entweder über den nativen Python-Connector oder über den ODBC-Treiber hergestellt wird.
Beide Varianten werden unterstützt: serverless und dedicated SQL pools.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python-Treiber

**Library:** `pymssql`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (Native Driver)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

```
Technology:      MS SQL Server
Host Address:    <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette von Authentifizierungs- und Verbindungsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf die passwortbasierte Authentifizierung unter Verwendung des Treibers **ODBC Driver 18 for SQL Server**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den Treiber **ODBC Driver 18 for SQL Server** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren der ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Füllen Sie das Feld "Server" aus.
Verwenden Sie den Namen des Synapse-Workspaces und hängen Sie ".sql.azuresynapse.net" an.  
**Achtung**, wenn Sie eine Verbindung zu einem serverless SQL Pool herstellen möchten, stellen Sie sicher, dass Sie "-ondemand" wie in der folgenden Abbildung angegeben hinzufügen.

Klicken Sie auf die **Next >**-Schaltfläche.

#### Schritt 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Wählen Sie die Authentifizierungsmethode (z. B. Benutzername und Passwort)
und geben Sie die erforderlichen Daten ein.

Klicken Sie auf die **Next >**-Schaltfläche.

#### Schritt 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Wählen Sie die ANSI-konformen Einstellungen und klicken Sie dann auf **Next >**.

#### Schritt 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Sie können die Standardeinstellungen belassen oder nach Bedarf Optionen auswählen 
und dann auf **Finish** klicken.

#### Schritt 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klicken Sie nun auf die **Test datasource**-Schaltfläche.

#### Schritt 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Wenn Sie den Erfolgsbildschirm erhalten, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-less**-Konfiguration verwendet wird.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      MS SQL Server
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",        value: "azure-synopse-serverless-1"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      MS SQL Server
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```

**Hinweis** zur SERVER-Eigenschaft:  
Verwenden Sie den Namen des Synapse-Workspaces und hängen Sie ".sql.azuresynapse.net" an. Wenn Sie eine Verbindung zu einem serverless SQL Pool herstellen möchten, stellen Sie sicher, dass Sie "-ondemand" wie in der folgenden Abbildung angegeben hinzufügen.