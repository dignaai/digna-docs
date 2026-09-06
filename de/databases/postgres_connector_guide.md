# Quell-Connector für PostgreSQL

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Postgres entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **„Datenbankverbindung erstellen“**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `psycopg`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna*-Konfiguration (nativer Treiber)

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird verwendet, um die Verbindung in anderen Bildschirmen zu referenzieren.
Technology:         Postgres
Host Address:       Servername oder IP-Adresse
Host Port:          Portnummer, z. B. 5432
Database Name:      Name der Datenbank
User Name:          Datenbank-Benutzername
User Password:      Passwort des Benutzers
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten des inspizierten Tages werden in eine permanente Tabelle kopiert und Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Beim Einsatz des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine größere Bandbreite an Authentifizierungs- und Verbindungsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **PostgreSQL Unicode(x64)**.

### 1. ODBC-Treiber installieren

Installieren Sie **PostgreSQL Unicode(x64)** (oder einen ähnlichen Treiber) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. ODBC-Datenquelle konfigurieren

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/postgres/create_odbc_data_source_step1.png)

Hinweis: Falls Ihre Datenbankkonfiguration die Auswahl eines bestimmten "SSLMode" erfordert, stellen Sie bitte sicher, dass Sie diesen beim Definieren einer DSN-losen Konfiguration ebenfalls verwenden.

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **Test Connection**.

![Schritt 2](images/postgres/create_odbc_data_source_step2.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-losen** Konfiguration verwendet wird.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** Folgendes an:

```
Name:               Name der Verbindung. Wird verwendet, um die Verbindung in anderen Bildschirmen zu referenzieren.
Technology:         PostgreSQL
Database Name:      Datenbank, die die Quellschemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten des inspizierten Tages werden in eine permanente Tabelle kopiert und Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Beim Einsatz des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "PostgreSQL35W"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-losen Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** Folgendes an:

```
Name:               Name der Verbindung. Wird verwendet, um die Verbindung in anderen Bildschirmen zu referenzieren.
Technology:         PostgreSQL
Database Name:      Datenbank, die die Quellschemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten des inspizierten Tages werden in eine permanente Tabelle kopiert und Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Beim Einsatz des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
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