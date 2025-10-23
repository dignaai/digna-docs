---
title: PostgreSQL Connector – Database Integration | digna Documentation
description: Configure digna to connect to PostgreSQL using the psycopg Python driver or the PostgreSQL ODBC driver. Supports password-based authentication with DSN or DSN-less setups.
image: /assets/logo_square.png
---


# Quell-Connector für PostgreSQL

Diese Anleitung beschreibt, wie man *digna* konfiguriert, um sich mit Postgres zu verbinden, entweder über den nativen Python-Connector oder den ODBC-Treiber.

Es bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `psycopg`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> ⚠️ Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (Nativer Treiber)

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Technology:      Postgres
Host Address:    Server name or IP address
Host Port:       Port number, e.g. 5432
Database Name:   Database name
Schema Name:     Schema that contains the source data
User Name:       Database user name
User Password:   Password for the user
Use ODBC:        Disabled (default)
```

---

## ODBC-Treiber

Der ODBC-Treiber unterstützt möglicherweise eine größere Bandbreite an Authentifizierungs- und Konnektivitätsoptionen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **PostgreSQL Unicode(x64)**.

### 1. ODBC-Treiber installieren

Installieren Sie den **PostgreSQL Unicode(x64)** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. ODBC-Datenquelle konfigurieren

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/postgres/create_odbc_data_source_step1.png)

Hinweis: Wenn Ihre Datenbankkonfiguration erfordert, dass Sie einen bestimmten "SSLMode" auswählen, stellen Sie sicher, dass Sie diesen auch bei der Definition einer DSN-less Konfiguration verwenden.

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **Test Connection**.

![Schritt 2](images/postgres/create_odbc_data_source_step2.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einer **DSN (Data Source Name)** oder einer **DSN-less** Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Technology:      PostgreSQL
Database Name:   Database that contains the source schema
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "PostgreSQL35W"
```

> 🔹 Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Technology:      PostgreSQL
Database Name:   Schema that contains the source data (same as Schema Name)
Schema Name:     Schema that contains the source data
Use ODBC:        Enabled
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "your server name or IP address"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres or other name of your database"
name: "UID",        value: "your postgres user'
name: "PWD",        value: "your postgres password"
name: "SSLMode",    value: "require"
```