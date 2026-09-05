---
title: Azure Synapse Connector – Datenbank-Integration | digna Dokumentation
description: Konfigurieren Sie digna, um sich mit Azure Synapse Analytics über den nativen Python-Treiber oder den ODBC-Treiber zu verbinden. Unterstützt sowohl serverlose als auch dedizierte SQL-Pools.
image: /assets/logo_square.png
---


# Quell-Connector für Azure Synapse Analytics

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Azure Synapse Analytics entweder über den nativen Python-Connector oder über den ODBC-Treiber hergestellt wird.
Er unterstützt sowohl serverlose als auch dedizierte SQL-Pools.

Diese Konfiguration bezieht sich auf den Bildschirm **"INTEGRATIONS" &rarr;  "DB CONNECTIONS" &rarr; "+ ADD DB CONNECTION"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `pymssql`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna*-Konfiguration (Nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **"Create Database Connection"** ein:

```
Name:               Name der Verbindung. Wird zum Referenzieren der Verbindung in anderen Bildschirmen verwendet.
Technology:         MS SQL Server
Host Address:       <synapse-workspace>[-ondemand].sql.azuresynapse.net
Host Port:          Portnummer, z. B. 1433
Database Name:      Name der Datenbank
User Name:          Benutzername für die Datenbank
User Password:      Passwort für den Benutzer
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten des inspizierten Tages werden in eine permanente Tabelle kopiert, und Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert, und Metriken werden auf diesen temporären Daten berechnet.
                    Für serverlosen SQL-Pool wird nur "Standard" unterstützt.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine größere Bandbreite an Authentifizierungs- und Verbindungsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **ODBC Driver 18 for SQL Server**.

### 1. Installieren Sie den ODBC-Treiber

Installieren Sie den Treiber **ODBC Driver 18 for SQL Server** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren Sie die ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/azure_synapse/create_odbc_data_source_step1.png)

Füllen Sie das Feld "Server" aus.
Verwenden Sie den Namen des Synapse-Workspaces und erweitern Sie ihn mit ".sql.azuresynapse.net".   
Achtung: Wenn Sie eine Verbindung zu einem serverlosen SQL-Pool herstellen möchten, stellen Sie sicher, dass Sie "-ondemand" wie im folgenden Screenshot einschließen.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 2
![Step 2](images/azure_synapse/create_odbc_data_source_step2.png)

Wählen Sie die Authentifizierungsmethode (z. B. Benutzername und Passwort)
und geben Sie die erforderlichen Daten ein.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 3
![Step 3](images/azure_synapse/create_odbc_data_source_step3.png)

Wählen Sie die ANSI-konformen Einstellungen und klicken Sie dann auf die Schaltfläche **Next >**.

#### Schritt 4
![Step 4](images/azure_synapse/create_odbc_data_source_step4.png)

Sie können die Standardeinstellungen belassen oder nach Bedarf Optionen wählen 
und dann auf die Schaltfläche **Finish** klicken. 

#### Schritt 5
![Step 5](images/azure_synapse/create_odbc_data_source_step5.png)

Klicken Sie nun auf die Schaltfläche **Test datasource**.

#### Schritt 6
![Step 1](images/azure_synapse/create_odbc_data_source_step6.png)

Wenn Sie den Erfolgsscreen erhalten, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird — entweder mit einem **DSN (Data Source Name)** oder einer **DSN-losen** Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **"Create Database Connection"** Folgendes an:

```
Name:               Name der Verbindung. Wird zum Referenzieren der Verbindung in anderen Bildschirmen verwendet.
Technology:         MS SQL Server
Database Name:      Datenbank, die die Quellschemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten des inspizierten Tages werden in eine permanente Tabelle kopiert, und Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert, und Metriken werden auf diesen temporären Daten berechnet.
                    Für serverlosen SQL-Pool wird nur "Standard" unterstützt.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
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

### B. DSN-loste Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Name:               Name der Verbindung. Wird zum Referenzieren der Verbindung in anderen Bildschirmen verwendet.
Technology:         MS SQL Server
Database Name:      Name der Datenbank, die das Quell-Datenbankschema enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten des inspizierten Tages werden in eine permanente Tabelle kopiert, und Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert, und Metriken werden auf diesen temporären Daten berechnet.
                    Für serverlosen SQL-Pool wird nur "Standard" unterstützt.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "ODBC Driver 18 for SQL Server"
name: "SERVER",     value: "<synapse-workspace>[-ondemand].sql.azuresynapse.net"
name: "UID",        value: "your database user"
name: "PWD",        value: "your database password"
name: "DATABASE",   value: "name of the database that contains the source data schemata"
```

**Hinweis** zur SERVER-Eigenschaft:  
Verwenden Sie den Namen des Synapse-Workspaces und erweitern Sie ihn mit ".sql.azuresynapse.net". Wenn Sie eine Verbindung zu einem serverlosen SQL-Pool herstellen möchten, stellen Sie sicher, dass Sie "-ondemand" wie im folgenden Screenshot einschließen.