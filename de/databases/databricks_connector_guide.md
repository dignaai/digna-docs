# Quell-Connector für Databricks – mit Unity Catalog

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Databricks entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `databricks-sql-connector`  
**Unterstützte Authentifizierung:** Personal Access Token (PAT) (nur)

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### Personal Access Token (PAT)

Um sich mit einem Personal Access Token zu authentifizieren, lesen Sie die offizielle Databricks-Dokumentation:  
[Wie Sie ein PAT erhalten](https://docs.databricks.com/aws/en/dev-tools/auth/pat)

### *digna* Konfiguration (nativer Treiber)

Geben Sie auf dem Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Dies wird verwendet, um die Verbindung in anderen Bildschirmen zu referenzieren.
Technology:         Databricks
Host Address:       Databricks-Hostname, z. B. "xxxxxxxxxxxxxxxxxxx.databricks.com"
Host Port:          z. B. 443
Database Name:      Name des zu verwendenden Katalogs.
User Name:          HTTP-Pfad, der von Databricks bereitgestellt wird, z. B. "/sql/1.0/warehouses/xxxxxxxxxxxxxxx"
User Password:      Personal Access Token, z. B. "dapixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
Profiling Mode:     Der Profiling-Modus bestimmt, wie *digna* Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den untersuchten Tag werden in eine permanente Tabelle kopiert und die Metriken auf diesen kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber unterstützt eine größere Auswahl an Authentifizierungs- und Konnektivitätsoptionen. Dieser Abschnitt konzentriert sich auf tokenbasierte Authentifizierung mit dem **Simba Spark ODBC Driver**.

### 1. Installieren Sie den ODBC-Treiber

Installieren Sie den **Simba Spark ODBC Driver** gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren Sie die ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit einem Personal Access Token zu konfigurieren:

#### Schritt 1
![Schritt 1](images/databricks/create_odbc_data_source_step1.png)

#### Schritt 2
![Schritt 2](images/databricks/create_odbc_data_source_step2.png)

#### Schritt 3
![Schritt 3](images/databricks/create_odbc_data_source_step3.png)

#### Schritt 4
![Schritt 4](images/databricks/create_odbc_data_source_step4.png)

#### Schritt 5 – Verbindung testen

Klicken Sie auf die **TEST**-Schaltfläche. Eine erfolgreiche Verbindung sollte so aussehen:

![Schritt 5](images/databricks/create_odbc_data_source_step5.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder einer **DSN-less** Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie auf dem Bildschirm **"Create a Database Connection"** die folgenden Angaben ein:

```
Name:               Name der Verbindung. Dies wird verwendet, um die Verbindung in anderen Bildschirmen zu referenzieren.
Technology:         Databricks
Database Name:      Name des zu verwendenden Katalogs.
Profiling Mode:     Der Profiling-Modus bestimmt, wie *digna* Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den untersuchten Tag werden in eine permanente Tabelle kopiert und die Metriken auf diesen kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",    value: "*digna*data_databricks"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less Konfiguration

#### *digna* Konfiguration

Geben Sie auf dem Bildschirm **"Create a Database Connection"** die folgenden Angaben ein:

```
Name:               Name der Verbindung. Dies wird verwendet, um die Verbindung in anderen Bildschirmen zu referenzieren.
Technology:         Databricks
Database Name:      Name des zu verwendenden Katalogs.
Profiling Mode:     Der Profiling-Modus bestimmt, wie *digna* Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den untersuchten Tag werden in eine permanente Tabelle kopiert und die Metriken auf diesen kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
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