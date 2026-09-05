# Quell-Connector für Hive

Diese Anleitung beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Hive entweder über den nativen Python-Connector oder über den ODBC-Treiber hergestellt wird.

Sie bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Nativer Python-Treiber

**Bibliothek:** `PyHive`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna*-Konfiguration (nativer Treiber)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

```
Technology:      Apache Hive
Host Address:    Servername oder IP-Adresse
Host Port:       Portnummer, z. B. 10000
Database Name:   Schema, das die Quelldaten enthält
Schema Name:     Schema, das die Quelldaten enthält
User Name:       Datenbank-Benutzername
User Password:   Passwort für den Benutzer
Use ODBC:        Deaktiviert (Standard)
```

---

## ODBC-Treiber

Der ODBC-Treiber kann eine breitere Palette an Authentifizierungs- und Konnektivitätsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **Cloudera ODBC Driver for Apache Hive**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den **Cloudera ODBC Driver for Apache Hive** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Herstellers.

### 2. Konfigurieren der ODBC-Datenquelle

Befolgen Sie diese Schritte, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/hive/create_odbc_data_source_step1.png)


#### Schritt 2 – Verbindung testen

Geben Sie das Passwort ein und klicken Sie auf die **Test**-Schaltfläche.

![Step 2](images/hive/create_odbc_data_source_step2.png)

Nach einem erfolgreichen Test klicken Sie auf die **OK**-Schaltfläche.

---

Jetzt können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einer **DSN (Data Source Name)**- oder einer **DSN-less**-Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna*-Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Apache Hive
Database Name:   Schema, das die Quelldaten enthält (gleich wie Schema Name)
Schema Name:     Schema, das die Quelldaten enthält
Use ODBC:        Aktiviert
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

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technology:      Apache Hive
Database Name:   Schema, das die Quelldaten enthält (gleich wie Schema Name)
Schema Name:     Schema, das die Quelldaten enthält
Use ODBC:        Aktiviert
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