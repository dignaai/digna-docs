# Quell-Connector für Oracle

Dieser Leitfaden beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Oracle DB entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **„Datenbankverbindung erstellen“**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `python-oracledb`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna*-Konfiguration (Nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **„Datenbankverbindung erstellen“** an:

```
Name:               Name der Verbindung. Dieser wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technologie:        Oracle
Host-Adresse:       Servername oder IP-Adresse
Host-Port:          Portnummer, z. B. 1521
Datenbankname:      Instanzname, Service-Name
Schema-Name:        Schema, das die Quell-Daten enthält
Benutzername:       Datenbank-Benutzername
Benutzer-Passwort:  Passwort des Benutzers
Profiling-Modus:    Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Arbeits-Schema-Name: Bei Verwendung des Profiling-Modus „Permanent“ werden Arbeitstabellen in diesem Schema abgelegt.
ODBC verwenden:     Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **Oracle in OraDB21Home1**.

### 1. Installation des ODBC-Treibers

Installieren Sie **Oracle in OraDB21Home1** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren der ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Hinweis:
Der TNS Service Name muss in der tnsnames.ora-Datei Ihrer Oracle-Client-Installation konfiguriert sein. Hier geben Sie den Verbindungs-Deskriptor an (Host, Port, Service-Name).

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **Verbindung testen**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Geben Sie das Passwort ein und klicken Sie auf die **OK**-Schaltfläche.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung entweder mit einem **DSN (Data Source Name)** oder einer **DSN-less**-Konfiguration verwendet wird.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** Folgendes an:

```
Name:               Name der Verbindung. Dieser wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technologie:        Oracle
Datenbankname:      Datenbank, die das Quellschema enthält
Profiling-Modus:    Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Arbeits-Schema-Name: Bei Verwendung des Profiling-Modus „Permanent“ werden Arbeitstabellen in diesem Schema abgelegt.
ODBC verwenden:     Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "Ihr Oracle-Benutzer"
name: "PWD",            value: "{Ihr Passwort in geschweiften Klammern}"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiber-Konfiguration definierten Namen übereinstimmen.

---

### B. DSN-less-Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **„Datenbankverbindung erstellen“** Folgendes an:

```
Name:               Name der Verbindung. Dieser wird zur Referenzierung der Verbindung in anderen Bildschirmen verwendet.
Technologie:        Oracle
Datenbankname:      Schema, das die Quell-Daten enthält (gleich dem Schema-Name)
Profiling-Modus:    Der Profiling-Modus bestimmt, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert und die Metriken auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert und Metriken auf diesen temporären Daten berechnet.
Arbeits-Schema-Name: Bei Verwendung des Profiling-Modus „Permanent“ werden Arbeitstabellen in diesem Schema abgelegt.
ODBC verwenden:     Aktiviert
```

#### ODBC-Eigenschaften

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "Ihr Oracle-Benutzer"
name: "PWD",        value: "Ihr Oracle-Passwort"
```