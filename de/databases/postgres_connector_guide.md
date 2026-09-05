# Quell-Connector für PostgreSQL

Diese Anleitung beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Postgres entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Sie bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `psycopg`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (Nativertreiber)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

```
Name:               Name der Verbindung. Wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technology:         Postgres
Host Address:       Servername oder IP-Adresse
Host Port:          Portnummer, z. B. 5432
Database Name:      Name der Datenbank
User Name:          Benutzername der Datenbank
User Password:      Passwort für den Benutzer
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Disabled (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **PostgreSQL Unicode(x64)**.

### 1. Installieren Sie den ODBC-Treiber

Installieren Sie **PostgreSQL Unicode(x64)** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren Sie die ODBC-Datenquelle

Gehen Sie wie folgt vor, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/postgres/create_odbc_data_source_step1.png)

Hinweis: Falls Ihre Datenbankkonfiguration erfordert, dass Sie einen bestimmten "SSLMode" wählen, stellen Sie sicher, dass Sie diesen auch bei der Definition einer DSN-less-Konfiguration verwenden.

#### Schritt 2 – Verbindung testen

Klicken Sie auf die **Test Connection**-Schaltfläche.

![Step 2](images/postgres/create_odbc_data_source_step2.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder einer **DSN-less**-Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Name:               Name der Verbindung. Wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technology:         PostgreSQL
Database Name:      Datenbank, die die Quell-Schemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Enabled
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "PostgreSQL35W"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less-Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Name:               Name der Verbindung. Wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technology:         PostgreSQL
Database Name:      Datenbank, die die Quell-Schemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Enabled
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "PostgreSQL Unicode(x64)"
name: "SERVER",     value: "Ihr Servername oder IP-Adresse"
name: "PORT",       value: "5432"
name: "DATABASE",   value: "postgres oder anderer Name Ihrer Datenbank"
name: "UID",        value: "Ihr postgres-Benutzer"
name: "PWD",        value: "Ihr postgres-Passwort"
name: "SSLMode",    value: "require"
```