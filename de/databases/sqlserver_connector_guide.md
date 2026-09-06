# Quell-Connector für MS SQL Server

Diese Anleitung beschreibt, wie Sie *digna* konfigurieren, um sich mit SQL Server entweder über den nativen Python-Connector oder den ODBC-Treiber zu verbinden.

Sie bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `pymssql`  
**Unterstützte Authentifizierung:** Nur kennwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (nativ)

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird in anderen Bildschirmen zur Referenz verwendet.
Technology:         MS SQL Server
Host Address:       Servername oder IP-Adresse
Host Port:          Portnummer, z. B. 1433
Database Name:      Name der Datenbank
User Name:          Datenbankbenutzername
User Password:      Passwort für den Benutzer
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema angelegt.
Use ODBC:           Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf kennwortbasierte Authentifizierung mit dem Treiber **SQL Server**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den Treiber **SQL Server** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren der ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit kennwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/sqlserver/create_odbc_data_source_step1.png)

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 2
![Schritt 2](images/sqlserver/create_odbc_data_source_step2.png)

Wählen Sie die Authentifizierungsmethode (z. B. Benutzername und Passwort) und geben Sie die erforderlichen Daten ein.

Klicken Sie auf die Schaltfläche **Next >**.

#### Schritt 3
![Schritt 3](images/sqlserver/create_odbc_data_source_step3.png)

Wählen Sie die ANSI-konformen Einstellungen und klicken Sie dann auf die Schaltfläche **Next >**.

#### Schritt 4
![Schritt 4](images/sqlserver/create_odbc_data_source_step4.png)

Sie können die Standardeinstellungen belassen oder bei Bedarf Protokollierungsoptionen wählen und dann auf die Schaltfläche **Finish** klicken.

#### Schritt 5
![Schritt 5](images/sqlserver/create_odbc_data_source_step5.png)

Klicken Sie jetzt auf die Schaltfläche **Test datasource**.

#### Schritt 6
![Schritt 6](images/sqlserver/create_odbc_data_source_step6.png)

Wenn Sie die Erfolgsmeldung erhalten, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird — entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-losen** Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird in anderen Bildschirmen zur Referenz verwendet.
Technology:         MS SQL Server
Database Name:      Datenbank, die die Quell-Schemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema angelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",        value: "sqlserver-1"
name: "UID",        value: "Ihr Datenbankbenutzer"
name: "PWD",        value: "Ihr Datenbankpasswort"
name: "DATABASE",   value: "Name der Datenbank, die das Quell-Datenschema enthält"
```

> Der Wert von `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-lose Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Name:               Name der Verbindung. Wird in anderen Bildschirmen zur Referenz verwendet.
Technology:         MS SQL Server
Database Name:      Name der Datenbank, die die Quell-Daten-Schemata enthält
Profiling Mode:     Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und die Metriken auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema angelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "SQL Server"
name: "SERVER",     value: "Ihr Servername oder IP-Adresse"
name: "UID",        value: "Ihr Datenbankbenutzer"
name: "PWD",        value: "Ihr Datenbankpasswort"
name: "DATABASE",   value: "Name der Datenbank, die die Quell-Daten-Schemata enthält"
```