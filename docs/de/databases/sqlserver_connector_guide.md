---
title: MS SQL Server Connector – Datenbankintegration | digna Documentation
description: Konfigurieren Sie digna so, dass eine Verbindung zu Microsoft SQL Server über den pymssql Python-Treiber oder den SQL Server ODBC-Treiber hergestellt wird. Unterstützt passwortbasierte Authentifizierung mit DSN- oder DSN-less-Konfigurationen.
image: /assets/logo_square.png
---


# Source Connector für MS SQL Server

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu SQL Server entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `pymssql`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> ⚠️ Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (nativ)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

```
Technology:      MS SQL Server
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 1433
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Verbindungsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf die passwortbasierte Authentifizierung mit dem Treiber **SQL Server**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den Treiber **SQL Server** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren der ODBC-Datenquelle

Gehen Sie wie folgt vor, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/sqlserver/create_odbc_data_source_step1.png)

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 2
![Schritt 2](images/sqlserver/create_odbc_data_source_step2.png)

Wählen Sie die Authentifizierungsmethode (z. B. Benutzername und Passwort)
und geben Sie die erforderlichen Daten ein.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 3
![Schritt 3](images/sqlserver/create_odbc_data_source_step3.png)

Wählen Sie die ANSI-kompatiblen Einstellungen und klicken Sie dann auf **Next >**.

#### Schritt 4
![Schritt 4](images/sqlserver/create_odbc_data_source_step4.png)

Sie können die Standardeinstellungen belassen oder bei Bedarf Protokollierungsoptionen wählen
und dann auf **Finish** klicken.

#### Schritt 5
![Schritt 5](images/sqlserver/create_odbc_data_source_step5.png)

Klicken Sie nun auf die Schaltfläche **Test datasource**.

#### Schritt 6
![Schritt 6](images/sqlserver/create_odbc_data_source_step6.png)

Wenn Sie den Erfolgsbildschirm erhalten, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-less**-Konfiguration.

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
name: "DSN",        value: "SQLServerDext"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"

```

> 🔹 Der `DSN` muss dem in Ihrer ODBC-Treiberkonfiguration definierten Namen entsprechen.

---

### B. DSN-less-Konfiguration

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
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "your server name or IP address"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schema"
```