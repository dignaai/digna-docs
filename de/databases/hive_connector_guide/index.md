# Quell-Connector für Hive

Diese Anleitung beschreibt, wie *digna* so konfiguriert wird, dass es sich mit Hive verbindet, entweder über den nativen Python-Connector oder den ODBC-Treiber.

Sie bezieht sich auf den Bildschirm **"Datenbankverbindung erstellen"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Library:** `PyHive`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna*-Konfiguration (nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **"Datenbankverbindung erstellen"** an:

```
Name:               Name der Verbindung. Dieser Name wird in anderen Bildschirmen zur Referenzierung der Verbindung verwendet.
Technology:         Apache Hive
Host Address:       Servername oder IP-Adresse
Host Port:          Portnummer, z. B. 10000
Database Name:      Schema, das die Quelldaten enthält
User Name:          Datenbank-Benutzername
User Password:      Passwort für den Benutzer
Profiling Mode:     Der Profiling-Modus legt fest, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert, und Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert, und Metriken werden auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung unter Verwendung des Treibers **Cloudera ODBC Driver for Apache Hive**.

### 1. ODBC-Treiber installieren

Installieren Sie den **Cloudera ODBC Driver for Apache Hive** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. ODBC-Datenquelle konfigurieren

Gehen Sie wie folgt vor, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Schritt 1](images/hive/create_odbc_data_source_step1.png)


#### Schritt 2 – Verbindung testen

Geben Sie das Passwort ein und klicken Sie auf die Schaltfläche **Test**.

![Schritt 2](images/hive/create_odbc_data_source_step2.png)

Nach einem erfolgreichen Test klicken Sie auf **OK**.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder einer **DSN-less**-Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **"Datenbankverbindung erstellen"** Folgendes an:

```
Name:               Name der Verbindung. Dieser Name wird in anderen Bildschirmen zur Referenzierung der Verbindung verwendet.
Technology:         Apache Hive
Database Name:      Schema, das die Quelldaten enthält
Profiling Mode:     Der Profiling-Modus legt fest, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert, und Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert, und Metriken werden auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",            value: "*digna*data_hdp"
name: "PWD",            value: "{Ihr Passwort in geschweiften Klammern}"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less-Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **"Datenbankverbindung erstellen"** Folgendes an:

```
Name:               Name der Verbindung. Dieser Name wird in anderen Bildschirmen zur Referenzierung der Verbindung verwendet.
Technology:         Apache Hive
Database Name:      Schema, das die Quelldaten enthält
Profiling Mode:     Der Profiling-Modus legt fest, wie digna Daten verarbeitet und Metriken berechnet:
                    - Standard: Metriken werden direkt auf den Quelltabellen berechnet, ohne die Daten zu kopieren.
                    - Permanent: Daten für den inspizierten Tag werden in eine permanente Tabelle kopiert, und Metriken werden auf den kopierten Daten berechnet.
                    - Session: Daten werden in eine Session- oder temporäre Tabelle kopiert, und Metriken werden auf diesen temporären Daten berechnet.
Work Schema Name:   Bei Verwendung des Profiling-Modus "Permanent" werden Arbeitstabellen in diesem Schema abgelegt.
Use ODBC:           Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "Cloudera ODBC Driver for Apache Hive"
name: "HOST",       value: "Ihr Servername oder Ihre IP-Adresse"
name: "PORT",       value: "Portnummer, z. B. 10000"
name: "Schema",     value: "Schema, das die Quelldaten enthält"
name: "UID",        value: "Ihr Hive-Benutzer"
name: "PWD",        value: "Ihr Hive-Passwort"
name: "AuthMech",   value: "3"
```