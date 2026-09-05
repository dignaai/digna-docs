# Source Connector for Teradata

Dieses Handbuch beschreibt, wie *digna* so konfiguriert wird, dass eine Verbindung zu Teradata entweder über den nativen Python-Connector oder über den ODBC-Treiber hergestellt wird.

Es bezieht sich auf den Bildschirm **"Create a Database Connection"**.

![Datenbankverbindung erstellen](images/data_source_config_input_mask.png)

---

## Native Python Driver

**Library:** `teradatasql`  
**Unterstützte Authentifizierung:** Nur passwortbasierte Authentifizierung

> Für andere Authentifizierungsmethoden verwenden Sie bitte den ODBC-Treiber.

### *digna* Konfiguration (Native Driver)

Geben Sie die folgenden Informationen im Bildschirm **"Create a Database Connection"** an:

```
Technologie:      Teradata
Host-Adresse:     Servername oder IP-Adresse
Host-Port:        Portnummer, z. B. 1025
Datenbankname:    Name der Datenbank
Schema-Name:      Name der Datenbank
Benutzername:     Datenbank-Benutzername
Benutzerpasswort: Passwort für den Benutzer
ODBC verwenden:   Deaktiviert (Standard)
```

---

## ODBC Driver

Der ODBC-Treiber kann eine größere Bandbreite an Authentifizierungs- und Verbindungsoptionen unterstützen. Dieser Abschnitt konzentriert sich auf passwortbasierte Authentifizierung mit dem Treiber **Teradata Database ODBC Driver 20.00**.

### 1. Installation des ODBC-Treibers

Installieren Sie den Treiber **Teradata Database ODBC Driver 20.00** (oder eine ähnliche Version) gemäß der offiziellen Installationsanleitung des Herstellers.

### 2. Konfigurieren der ODBC-Datenquelle

Befolgen Sie diese Schritte, um eine neue ODBC-Datenquelle mit passwortbasierter Authentifizierung zu konfigurieren:

#### Schritt 1
![Step 1](images/teradata/create_odbc_data_source_step1.png)

Klicken Sie auf die Schaltfläche **Test**.

#### Schritt 2
![Step 2](images/teradata/create_odbc_data_source_step2.png)

Geben Sie Benutzername und Passwort ein.

Klicken Sie auf die **OK**-Schaltfläche.  
Wenn Sie den Erfolgsscreen erhalten, ist ODBC korrekt konfiguriert.

---

Nun können Sie *digna* so konfigurieren, dass die ODBC-Verbindung verwendet wird — entweder mit einem **DSN (Data Source Name)** oder in einer **DSN-less** Konfiguration.

---

### A. DSN-basierte Konfiguration

#### *digna* Konfiguration

Im Bildschirm **"Create a Database Connection"** geben Sie Folgendes an:

```
Technologie:      Teradata
Datenbankname:    Datenbank, die das Quellschema enthält
Schema-Name:      Schema, das die Quelldaten enthält
ODBC verwenden:   Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DSN",        value: "*digna*data_teradata"
name: "UID",        value: "Ihr Datenbankbenutzer"
name: "PWD",        value: "Ihr Datenbankpasswort"
```

> Der `DSN` muss mit dem in Ihrer ODBC-Treiberkonfiguration definierten Namen übereinstimmen.

---

### B. DSN-less Konfiguration

#### *digna* Konfiguration

Im Bildschirm **"Create a Database Connection"** geben Sie Folgendes an:

```
Technologie:      Teradata
Datenbankname:    Schema, das die Quelldaten enthält (gleich wie Schema-Name)
Schema-Name:      Schema, das die Quelldaten enthält
ODBC verwenden:   Aktiviert
```

#### ODBC-Eigenschaften

```
name: "DRIVER",     value: "Teradata Database ODBC Driver 20.00"
name: "DBCNAME",    value: "Ihr Servername oder Ihre IP-Adresse"
name: "UID",        value: "Ihr Datenbankbenutzer"
name: "PWD",        value: "Ihr Datenbankpasswort"
```