---
title: Oracle Connector – Datenbankintegration | digna Dokumentation
description: Konfigurieren Sie digna, um eine Verbindung zu Oracle über den python-oracledb-Treiber oder den Oracle ODBC-Treiber herzustellen. Unterstützt kennwortbasierte Authentifizierung mit DSN- oder DSN-losen Setups.
image: /assets/logo_square.png
---


# Source Connector for Oracle

Dieser Leitfaden beschreibt, wie Sie *digna* so konfigurieren, dass eine Verbindung zu Oracle DB entweder über den nativen Python-Connector oder den ODBC-Treiber hergestellt wird.

Er bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Create a database connection](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `python-oracledb`  
**Unterstützte Authentifizierung:** ausschließlich kennwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (nativer Treiber)

Geben Sie im Bildschirm **"Create a Database Connection"** die folgenden Informationen an:

```
Technologie:      Oracle
Host-Adresse:     Servername oder IP-Adresse
Host-Port:        Portnummer, z. B. 1521
Datenbankname:    Instanzname, Service-Name
Schema-Name:      Schema, das die Quelldaten enthält
Benutzername:     Datenbank-Benutzername
Benutzerpasswort: Passwort für den Benutzer
ODBC verwenden:   Deaktiviert (Standard)
```

---

## ODBC Driver

Der ODBC-Treiber kann eine größere Bandbreite an Authentifizierungs- und Verbindungsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf kennwortbasierte Authentifizierung mit dem Treiber **Oracle in OraDB21Home1**.

### 1. Installieren des ODBC-Treibers

Installieren Sie den **Oracle in OraDB21Home1** (oder einen ähnlichen) gemäß der offiziellen Installationsanleitung des Anbieters.

### 2. Konfigurieren der ODBC-Datenquelle

Führen Sie die folgenden Schritte aus, um eine neue ODBC-Datenquelle mit kennwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/oracle/create_odbc_data_source_step1.png)

Hinweis:
Der TNS Service Name muss in der tnsnames.ora-Datei Ihrer Oracle-Client-Installation konfiguriert sein. Dort geben Sie den Verbindungsdescriptor an (Host, Port, Service-Name).

#### Schritt 2 – Verbindung testen

Klicken Sie auf die Schaltfläche **Test Connection**.

![Step 2](images/oracle/create_odbc_data_source_step2.png)

Geben Sie das Passwort ein und klicken Sie auf die Schaltfläche **OK**.

![Step 2](images/oracle/create_odbc_data_source_step3.png)

---

Jetzt können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird, entweder mit einem **DSN (Data Source Name)** oder einem **DSN-losen** Setup.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technologie:      Oracle
Datenbankname:    Datenbank, die das Quellschema enthält
Schema-Name:      Schema, das die Quelldaten enthält
ODBC verwenden:   Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",            value: "*digna*data_oracle"
name: "UID",            value: "your oracle user"
name: "PWD",            value: "{your password in curly braces}"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-loses Setup

#### *digna* Konfiguration

Geben Sie im Bildschirm **"Create a Database Connection"** Folgendes an:

```
Technologie:      Oracle
Datenbankname:    Schema, das die Quelldaten enthält (gleich dem Schema-Name)
Schema-Name:      Schema, das die Quelldaten enthält
ODBC verwenden:   Aktiviert
```

#### ODBC-Eigenschaften

```
name: "Driver",     value: "Oracle in OraDB21Home1"
name: "DBQ",        value: "(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST=localhost)(PORT=1521))(CONNECT_DATA=(SERVICE_NAME=XEPDB1)))"
name: "UID",        value: "your oracle user'
name: "PWD",        value: "your oracle password"
```